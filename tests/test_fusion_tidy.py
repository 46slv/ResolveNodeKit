import unittest

from resolve_node_kit.fusion import FusionHostError, tidy_comp


class MockOutput:
    def __init__(self, tool): self.tool = tool
    def GetTool(self): return self.tool


class MockInput:
    def __init__(self, source, input_id): self.output, self.input_id = MockOutput(source), input_id
    def GetConnectedOutput(self): return self.output
    def GetAttrs(self): return {"INPS_ID": self.input_id, "INPN_Name": self.input_id}


class MockTool:
    def __init__(self, name): self.Name, self.inputs = name, []
    def GetInputList(self): return list(self.inputs)
    def GetAttrs(self): return {"TOOLS_Name": self.Name}


class MockFlow:
    def __init__(self, positions, fail_on_call=None, ignore_writes=False):
        self.positions, self.fail_on_call, self.ignore_writes, self.calls = dict(positions), fail_on_call, ignore_writes, 0
    def GetPosTable(self, tool): return {1: self.positions[tool.Name][0], 2: self.positions[tool.Name][1]}
    def SetPos(self, tool, x, y):
        self.calls += 1
        if self.fail_on_call is not None and self.calls == self.fail_on_call: raise RuntimeError("injected SetPos failure")
        if not self.ignore_writes: self.positions[tool.Name] = (float(x), float(y))
        return True


class MockComp:
    def __init__(self, tools, flow):
        self.tools, self.CurrentFrame, self.undo = tools, type("Frame", (), {"FlowView": flow})(), []
    def GetToolList(self): return list(self.tools)
    def StartUndo(self, name): self.undo.append(("start", name))
    def EndUndo(self, keep): self.undo.append(("end", bool(keep)))


def connect(source, target, input_id): target.inputs.append(MockInput(source, input_id))


class FusionTidyTests(unittest.TestCase):
    def _merge_comp(self):
        bg, fg, merge = MockTool("BG"), MockTool("FG"), MockTool("Merge")
        connect(bg, merge, "Background")
        connect(fg, merge, "Foreground")
        flow = MockFlow({"BG": (0, 0), "FG": (10, 20), "Merge": (20, 0)})
        return MockComp([bg, fg, merge], flow), flow

    def test_merge_sources_are_separated(self):
        comp, flow = self._merge_comp()
        result = tidy_comp(comp)
        self.assertEqual(result.node_count, 3)
        self.assertNotEqual(flow.positions["BG"], flow.positions["FG"])
        self.assertEqual(comp.undo[-1], ("end", True))

    def test_second_run_is_idempotent(self):
        comp, flow = self._merge_comp()
        tidy_comp(comp)
        first = dict(flow.positions)
        result = tidy_comp(comp)
        self.assertEqual(first, flow.positions)
        self.assertEqual(result.moved_count, 0)

    def test_write_failure_restores_original_positions(self):
        tools = [MockTool("A"), MockTool("B"), MockTool("C")]
        connect(tools[0], tools[1], "Input")
        connect(tools[1], tools[2], "Input")
        original = {"A": (9, 4), "B": (2, 8), "C": (5, 3)}
        flow = MockFlow(original, fail_on_call=2)
        comp = MockComp(tools, flow)
        with self.assertRaises(FusionHostError): tidy_comp(comp)
        self.assertEqual(flow.positions, original)
        self.assertEqual(comp.undo[-1], ("end", False))

    def test_readback_mismatch_restores_original_positions(self):
        tools = [MockTool("A"), MockTool("B")]
        connect(tools[0], tools[1], "Input")
        original = {"A": (8, 3), "B": (1, 9)}
        flow = MockFlow(original, ignore_writes=True)
        comp = MockComp(tools, flow)
        with self.assertRaises(FusionHostError): tidy_comp(comp)
        self.assertEqual(flow.positions, original)
        self.assertEqual(comp.undo[-1], ("end", False))


if __name__ == "__main__":
    unittest.main()
