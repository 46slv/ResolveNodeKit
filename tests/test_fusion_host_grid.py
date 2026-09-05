"""Regression tests for host-measured FlowView behavior.

Measured on DaVinci Resolve Studio 21.0.3.7 (GUI, GridSnap on) via the
OpenCode worker path against live comps (see docs/GROUPS.md host evidence):

- FlowView positions snap to a grid: X to 0.5, Y to whole numbers, ties down.
- Position readback carries small stable per-type frame offsets (normal tools
  +0.009 on Y; e.g. EllipseMask +0.073/+0.054), so readback verification needs
  a tolerance that still fails closed on real grid differences (>= 0.2).
"""
import builtins
import math
import unittest

from resolve_node_kit.fusion.tidy import (
    FLOW_GRID_X,
    FLOW_GRID_Y,
    FLOW_POSITION_TOLERANCE,
    _close_enough,
    _ensure_ordered_dict,
    _snap_position,
    tidy_comp,
)


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
    def __init__(self, positions):
        self.positions, self.written = dict(positions), []
    def GetPosTable(self, tool): return {1: self.positions[tool.Name][0], 2: self.positions[tool.Name][1]}
    def SetPos(self, tool, x, y):
        self.written.append((tool.Name, float(x), float(y)))
        self.positions[tool.Name] = (float(x), float(y))
        return True


class HostLikeFlow(MockFlow):
    """Mimics the measured host: grid-snapped storage plus a stable Y offset."""

    OFFSET_Y = 0.009

    def GetPosTable(self, tool):
        x, y = self.positions[tool.Name]
        return {1: x, 2: y + self.OFFSET_Y}


class MockComp:
    def __init__(self, tools, flow):
        self.tools, self.CurrentFrame, self.undo = tools, type("Frame", (), {"FlowView": flow})(), []
    def GetToolList(self): return list(self.tools)
    def StartUndo(self, name): self.undo.append(("start", name))
    def EndUndo(self, keep): self.undo.append(("end", bool(keep)))


def connect(source, target, input_id): target.inputs.append(MockInput(source, input_id))


def chain(names):
    tools = [MockTool(name) for name in names]
    for source, target in zip(tools, tools[1:]):
        connect(source, target, "Input")
    return tools


class HostGridTests(unittest.TestCase):
    def test_grid_constants_match_host_measurement(self):
        self.assertEqual(FLOW_GRID_X, 0.5)
        self.assertEqual(FLOW_GRID_Y, 1.0)
        self.assertEqual(FLOW_POSITION_TOLERANCE, 0.1)

    def test_snap_position_snaps_to_host_grid(self):
        self.assertEqual(_snap_position(1.26, 2.51), (1.5, 3.0))
        self.assertEqual(_snap_position(1.24, 2.49), (1.0, 2.0))

    def test_snap_position_ties_snap_down(self):
        # Measured: 1.50 stays on the lower grid line, 1.51 moves up.
        self.assertEqual(_snap_position(0.0, 1.50), (0.0, 1.0))
        self.assertEqual(_snap_position(0.0, 1.51), (0.0, 2.0))
        self.assertEqual(_snap_position(1.25, 0.0), (1.0, 0.0))

    def test_snap_position_avoids_negative_zero(self):
        snapped = _snap_position(-0.1, -0.1)
        self.assertEqual(snapped, (0.0, 0.0))
        self.assertFalse(str(snapped[0]).startswith("-"))
        self.assertFalse(str(snapped[1]).startswith("-"))

    def test_close_enough_tolerates_measured_frame_offsets(self):
        self.assertTrue(_close_enough((7.0, 8.0), (7.0, 8.009)))
        self.assertTrue(_close_enough((0.0, 0.0), (0.073, 0.054)))

    def test_close_enough_still_fails_closed_on_grid_differences(self):
        self.assertFalse(_close_enough((0.0, 0.0), (0.0, 0.11)))
        self.assertFalse(_close_enough((0.0, 0.0), (0.2, 0.0)))
        self.assertFalse(_close_enough((1.0, 2.0), (1.5, 2.0)))

    def test_tidy_comp_writes_grid_snapped_positions(self):
        tools = chain(["A", "B", "C"])
        flow = MockFlow({"A": (9.13, 4.71), "B": (2.62, 8.05), "C": (5.44, 3.33)})
        tidy_comp(MockComp(tools, flow))
        self.assertTrue(flow.written)
        for _, x, y in flow.written:
            self.assertAlmostEqual(x / FLOW_GRID_X, round(x / FLOW_GRID_X))
            self.assertAlmostEqual(y / FLOW_GRID_Y, round(y / FLOW_GRID_Y))

    def test_second_run_stable_under_host_like_readback_offset(self):
        tools = chain(["A", "B", "C"])
        flow = HostLikeFlow({"A": (9.13, 4.71), "B": (2.62, 8.05), "C": (5.44, 3.33)})
        tidy_comp(MockComp(tools, flow))
        result = tidy_comp(MockComp(tools, flow))
        self.assertEqual(result.moved_count, 0)

    def test_ensure_ordered_dict_restores_builtins_guard(self):
        had = hasattr(builtins, "OrderedDict")
        saved = getattr(builtins, "OrderedDict", None)
        try:
            if had:
                delattr(builtins, "OrderedDict")
            _ensure_ordered_dict()
            import collections
            self.assertIs(builtins.OrderedDict, collections.OrderedDict)
        finally:
            if had:
                builtins.OrderedDict = saved
            elif hasattr(builtins, "OrderedDict"):
                delattr(builtins, "OrderedDict")


if __name__ == "__main__":
    unittest.main()
