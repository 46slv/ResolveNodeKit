import copy
import unittest

from resolve_node_kit.fusion import FusionHostError, tidy_nested_comp
from resolve_node_kit.fusion.recursive_groups import GroupTidyResult


class MockOutput:
    def __init__(self, tool): self.tool = tool
    def GetTool(self): return self.tool


class MockInput:
    def __init__(self, source, input_id): self.output, self.input_id = MockOutput(source), input_id
    def GetConnectedOutput(self): return self.output
    def GetAttrs(self): return {"INPS_ID": self.input_id, "INPN_Name": self.input_id}


class MockTool:
    def __init__(self, name, reg_id="Mock", parent=None, *, expanded=None):
        self.Name, self.inputs, self.parent, self.children = name, [], parent, []
        self.reg_id = reg_id
        if reg_id == "GroupOperator":
            flags = {} if expanded is None else {"Expanded": bool(expanded)}
            self.settings = {"Tools": {name: {"ViewInfo": {"Flags": flags}}}}
        else:
            self.settings = None
        if parent is not None:
            parent.children.append(self)

    @property
    def ParentTool(self): return self.parent
    def GetChildrenList(self): return list(self.children)
    def GetInputList(self): return list(self.inputs)
    def GetAttrs(self):
        result = {"TOOLS_Name": self.Name, "TOOLS_RegID": self.reg_id}
        if self.parent is not None: result["TOOLH_GroupParent"] = self.parent
        return result
    def SaveSettings(self): return copy.deepcopy(self.settings)
    def LoadSettings(self, settings):
        self.settings = copy.deepcopy(settings)
        return True


class MockFlow:
    def __init__(self, positions): self.positions, self.calls = dict(positions), 0
    def GetPosTable(self, tool): return {1: self.positions[tool.Name][0], 2: self.positions[tool.Name][1]}
    def SetPos(self, tool, x, y):
        self.calls += 1
        self.positions[tool.Name] = (float(x), float(y))
        return True


class StaleReadbackFlow(MockFlow):
    """Accepts writes but keeps reporting the original positions (host mismatch)."""
    def GetPosTable(self, tool): return {1: self.positions[tool.Name][0], 2: self.positions[tool.Name][1]}
    def SetPos(self, tool, x, y):
        self.calls += 1
        return True


class MockComp:
    def __init__(self, root_tools, flow):
        self.tools, self.CurrentFrame, self.undo = root_tools, type("Frame", (), {"FlowView": flow})(), []
    def GetToolList(self): return list(self.tools)
    def FindTool(self, name):
        queue = list(self.tools)
        while queue:
            tool = queue.pop(0)
            if tool.Name == name: return tool
            queue.extend(tool.children)
        return None
    def StartUndo(self, name): self.undo.append(("start", name))
    def EndUndo(self, keep): self.undo.append(("end", bool(keep)))


def connect(source, target, input_id): target.inputs.append(MockInput(source, input_id))


def nested_comp(expanded=False):
    g1 = MockTool("G1", "GroupOperator", expanded=expanded)
    a = MockTool("A", parent=g1)
    g2 = MockTool("G2", "GroupOperator", parent=g1, expanded=expanded)
    b = MockTool("B", parent=g1)
    c = MockTool("C", parent=g2)
    d = MockTool("D", parent=g2)
    out = MockTool("Out")
    connect(c, d, "Input")
    connect(a, b, "Input")
    connect(d, b, "Foreground")
    connect(b, out, "Input")
    positions = {
        "G1": (30, 10), "A": (9, 9), "G2": (6, 15), "B": (14, 7),
        "C": (8, 20), "D": (2, 3), "Out": (0, 30),
    }
    return MockComp([g1, out], MockFlow(positions)), g1, g2


def snapshot_settings(comp):
    found = {}

    def visit(tool):
        if tool.reg_id == "GroupOperator":
            found[tool.Name] = copy.deepcopy(tool.settings)
        for child in tool.children:
            visit(child)

    for tool in comp.tools:
        visit(tool)
    return found


class TidyNestedTests(unittest.TestCase):
    def test_nested_scopes_tidied_groups_stay_grouped(self):
        comp, g1, g2 = nested_comp()
        flow = comp.CurrentFrame.FlowView
        result = tidy_nested_comp(comp)
        self.assertIsInstance(result, GroupTidyResult)
        self.assertEqual((result.group_count, result.expanded_count, result.scope_count), (2, 0, 3))
        self.assertIs(comp.FindTool("A").ParentTool, g1)
        self.assertIs(comp.FindTool("G2").ParentTool, g1)
        self.assertIs(comp.FindTool("C").ParentTool, g2)
        self.assertLess(flow.positions["G1"][0], flow.positions["Out"][0])
        self.assertLess(flow.positions["G2"][0], flow.positions["B"][0])
        self.assertLess(flow.positions["C"][0], flow.positions["D"][0])

    def test_collapsed_groups_stay_collapsed_and_settings_untouched(self):
        comp, g1, g2 = nested_comp(expanded=False)
        before = snapshot_settings(comp)
        tidy_nested_comp(comp)
        self.assertEqual(snapshot_settings(comp), before)
        self.assertFalse(g1.settings["Tools"]["G1"]["ViewInfo"]["Flags"].get("Expanded", False))
        self.assertFalse(g2.settings["Tools"]["G2"]["ViewInfo"]["Flags"].get("Expanded", False))

    def test_expanded_groups_stay_expanded(self):
        comp, g1, g2 = nested_comp(expanded=True)
        tidy_nested_comp(comp)
        self.assertTrue(g1.settings["Tools"]["G1"]["ViewInfo"]["Flags"]["Expanded"])
        self.assertTrue(g2.settings["Tools"]["G2"]["ViewInfo"]["Flags"]["Expanded"])

    def test_second_run_is_idempotent(self):
        comp, _, _ = nested_comp()
        flow = comp.CurrentFrame.FlowView
        tidy_nested_comp(comp)
        first = dict(flow.positions)
        result = tidy_nested_comp(comp)
        self.assertEqual(first, flow.positions)
        self.assertEqual(result.moved_count, 0)
        self.assertEqual(result.expanded_count, 0)

    def test_readback_mismatch_restores_positions(self):
        comp, _, _ = nested_comp()
        stale = StaleReadbackFlow(dict(comp.CurrentFrame.FlowView.positions))
        comp.CurrentFrame.FlowView = stale
        original = dict(stale.positions)
        with self.assertRaises(FusionHostError):
            tidy_nested_comp(comp)
        self.assertEqual(stale.positions, original)
        self.assertEqual(comp.undo[-1], ("end", False))

    def test_group_parent_cycle_fails_before_any_write(self):
        g1 = MockTool("G1", "GroupOperator", expanded=False)
        g2 = MockTool("G2", "GroupOperator", parent=g1, expanded=False)
        g1.parent = g2
        g2.children.append(g1)
        flow = MockFlow({"G1": (0, 0), "G2": (3, 0)})
        comp = MockComp([g1], flow)
        with self.assertRaises(FusionHostError): tidy_nested_comp(comp)
        self.assertEqual(flow.calls, 0)


if __name__ == "__main__":
    unittest.main()
