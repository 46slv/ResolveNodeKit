import copy
import unittest

from resolve_node_kit.fusion import FusionHostError, flatten_all_comp, host_ungroup_capabilities
from resolve_node_kit.fusion.recursive_groups import _snapshot


class Output:
    def __init__(self, tool):
        self.tool = tool

    def GetTool(self):
        return self.tool

    def GetConnectedInputs(self):
        return [input_obj for input_obj in self.tool.comp.all_inputs() if input_obj.source is self.tool]


class LegacyOutput:
    """Output placeholder from a host that lacks connected-input readback."""

    pass


class Input:
    def __init__(self, source, target, input_id):
        self.source = source
        self.target = target
        self.input_id = input_id

    def GetConnectedOutput(self):
        return Output(self.source)

    def GetTool(self):
        return self.target

    def GetAttrs(self):
        return {"INPS_ID": self.input_id, "INPB_Connected": True}


class Tool:
    def __init__(self, comp, name, reg_id="Mock", parent=None):
        self.comp = comp
        self.Name = name
        self.reg_id = reg_id
        self.parent = parent
        self.children = []
        self.inputs = []
        if parent is not None:
            parent.children.append(self)

    @property
    def ParentTool(self):
        return self.parent

    def GetChildrenList(self):
        return list(self.children)

    def GetInputList(self):
        return list(self.inputs)

    def GetOutputList(self):
        return {1: Output(self)}

    def GetAttrs(self):
        attrs = {"TOOLS_Name": self.Name, "TOOLS_RegID": self.reg_id}
        if self.parent is not None:
            attrs["TOOLH_GroupParent"] = self.parent
        return attrs


class Flow:
    def __init__(self, positions):
        self.positions = dict(positions)

    def GetPosTable(self, tool):
        return {1: self.positions[tool.Name][0], 2: self.positions[tool.Name][1]}

    def SetPos(self, tool, x, y):
        self.positions[tool.Name] = (float(x), float(y))
        return True


class Comp:
    def __init__(self):
        self.tools = []
        self.CurrentFrame = type("Frame", (), {"FlowView": None})()
        self._undo_state = None
        self.undo = []

    def GetToolList(self):
        return list(self.tools)

    def FindTool(self, name):
        queue = list(self.tools)
        while queue:
            tool = queue.pop(0)
            if tool.Name == name:
                return tool
            queue.extend(tool.children)
        return None

    def all_tools(self):
        out = []

        def visit(tool):
            out.append(tool)
            for child in tool.children:
                visit(child)

        for tool in self.tools:
            visit(tool)
        return out

    def all_inputs(self):
        return [input_obj for tool in self.all_tools() for input_obj in tool.inputs]

    def _raw_state(self):
        rows = []
        for tool in self.all_tools():
            rows.append({
                "name": tool.Name,
                "reg_id": tool.reg_id,
                "parent": tool.parent.Name if tool.parent is not None else None,
                "position": self.CurrentFrame.FlowView.positions[tool.Name],
                "inputs": [(item.source.Name, item.input_id) for item in tool.inputs],
            })
        return {"rows": rows, "roots": [tool.Name for tool in self.tools]}

    def _restore_raw_state(self, state):
        by_name = {}
        for row in state["rows"]:
            by_name[row["name"]] = Tool(self, row["name"], row["reg_id"])
        for row in state["rows"]:
            tool = by_name[row["name"]]
            parent_name = row["parent"]
            if parent_name is not None:
                tool.parent = by_name[parent_name]
                tool.parent.children.append(tool)
            self.CurrentFrame.FlowView.positions[tool.Name] = tuple(row["position"])
        for row in state["rows"]:
            target = by_name[row["name"]]
            for source_name, input_id in row["inputs"]:
                target.inputs.append(Input(by_name[source_name], target, input_id))
        self.tools = [by_name[name] for name in state["roots"]]

    def StartUndo(self, name):
        self.undo.append(("start", name))
        self._undo_state = copy.deepcopy(self._raw_state())

    def EndUndo(self, keep):
        self.undo.append(("end", bool(keep)))

    def Undo(self):
        if self._undo_state is None:
            return None
        self._restore_raw_state(self._undo_state)
        self._undo_state = None
        return None


def connect(source, target, input_id):
    target.inputs.append(Input(source, target, input_id))


def nested_comp():
    comp = Comp()
    flow = Flow({
        "OuterG": (20.0, 20.0), "InnerG": (10.0, 10.0), "A": (0.0, 0.0),
        "B": (2.0, 0.0), "Branch": (0.0, 5.0), "Merge": (8.0, 8.0),
        "Out": (12.0, 8.0),
    })
    comp.CurrentFrame.FlowView = flow
    outer = Tool(comp, "OuterG", "GroupOperator")
    inner = Tool(comp, "InnerG", "GroupOperator", outer)
    a = Tool(comp, "A", parent=inner)
    b = Tool(comp, "B", parent=inner)
    branch = Tool(comp, "Branch", parent=outer)
    merge = Tool(comp, "Merge", "Merge")
    out = Tool(comp, "Out", "MediaOut")
    comp.tools = [outer, merge, branch, out]
    connect(a, b, "Input")
    connect(b, merge, "Background")
    connect(branch, merge, "Foreground")
    connect(merge, out, "Input")
    return comp, outer, inner


def ungroup_primitive(comp, group):
    parent = group.parent
    children = list(group.children)
    if parent is None:
        comp.tools.remove(group)
    else:
        parent.children.remove(group)
    for child in children:
        child.parent = parent
        if parent is None:
            comp.tools.append(child)
        else:
            parent.children.append(child)
    group.children = []
    return True


class FlattenTests(unittest.TestCase):
    def test_partial_output_surface_falls_back_without_losing_edges(self):
        comp, _outer, _inner = nested_comp()
        source = comp.FindTool("A")
        source.GetOutputList = lambda: {1: LegacyOutput()}
        snapshot = _snapshot(comp, comp.CurrentFrame.FlowView)
        self.assertIn(("A", "B", "background"), {
            (edge.source, edge.target, edge.kind) for edge in snapshot.edges
        })

    def test_capability_report_never_invents_generic_doaction(self):
        comp, _, _ = nested_comp()
        report = host_ungroup_capabilities(comp, comp.CurrentFrame.FlowView)
        self.assertFalse(report["supported"])
        self.assertEqual(report["callables"], [])

    def test_missing_primitive_fails_before_mutation(self):
        comp, _, _ = nested_comp()
        before = _snapshot(comp, comp.CurrentFrame.FlowView)
        with self.assertRaises(FusionHostError):
            flatten_all_comp(comp)
        after = _snapshot(comp, comp.CurrentFrame.FlowView)
        self.assertEqual(after.parents, before.parents)
        self.assertEqual(after.positions, before.positions)
        self.assertEqual(comp.undo, [])

    def test_nested_flatten_is_deepest_first_and_run2_stable(self):
        comp, _, _ = nested_comp()
        before = _snapshot(comp, comp.CurrentFrame.FlowView)
        order = []

        def primitive(target, group):
            order.append(group.Name)
            return ungroup_primitive(target, group)

        first = flatten_all_comp(comp, ungroup=primitive)
        self.assertEqual(order, ["InnerG", "OuterG"])
        self.assertEqual(first["group_count_pre"], 2)
        self.assertEqual(first["group_count"], 0)
        self.assertEqual(first["flattened_group_count"], 2)
        self.assertGreater(first["moved_count"], 0)
        flat = _snapshot(comp, comp.CurrentFrame.FlowView)
        self.assertEqual(flat.groups, ())
        self.assertEqual(set(flat.tools), {"A", "B", "Branch", "Merge", "Out"})
        self.assertTrue(all(parent is None for parent in flat.parents.values()))
        self.assertEqual(tuple(sorted((e.source, e.target, e.kind) for e in flat.edges)), tuple(sorted((e.source, e.target, e.kind) for e in before.edges)))

        second = flatten_all_comp(comp, ungroup=primitive)
        self.assertEqual(second["group_count"], 0)
        self.assertEqual(second["flattened_group_count"], 0)
        self.assertEqual(second["moved_count"], 0)

        comp.Undo()
        restored = _snapshot(comp, comp.CurrentFrame.FlowView)
        self.assertEqual(restored.parents, before.parents)
        self.assertEqual(restored.positions, before.positions)
        self.assertEqual(restored.groups, before.groups)
        self.assertEqual(
            tuple(sorted((e.source, e.target, e.kind) for e in restored.edges)),
            tuple(sorted((e.source, e.target, e.kind) for e in before.edges)),
        )

    def test_failed_structural_step_uses_owned_undo_for_exact_restore(self):
        comp, _, _ = nested_comp()
        before = _snapshot(comp, comp.CurrentFrame.FlowView)

        def failing(target, group):
            ungroup_primitive(target, group)
            raise RuntimeError("synthetic host rejection after mutation")

        with self.assertRaises(FusionHostError):
            flatten_all_comp(comp, ungroup=failing)
        after = _snapshot(comp, comp.CurrentFrame.FlowView)
        self.assertEqual(after.parents, before.parents)
        self.assertEqual(after.positions, before.positions)
        self.assertEqual(after.groups, before.groups)
        self.assertEqual(comp.undo[-1], ("end", False))


if __name__ == "__main__":
    unittest.main()
