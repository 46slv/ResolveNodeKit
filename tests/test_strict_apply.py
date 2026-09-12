import unittest

from resolve_node_kit.fusion.processing_snapshot import REQUIRED_PROCESSING_FIELDS, build_processing_snapshot
from resolve_node_kit.fusion.strict_apply import (
    FlowViewCalibration,
    StrictHostApplyError,
    execute_strict_preserve,
    map_strict_plan_to_host,
)
from resolve_node_kit.fusion.strict_request import prepare_strict_plan


def _fields(value=True):
    return {name: {"state": "complete", "value": value} for name in REQUIRED_PROCESSING_FIELDS}


class MockTool:
    def __init__(self, name):
        self.Name = name

    def GetAttrs(self):
        return {"TOOLS_Name": self.Name}


class MockFlow:
    def __init__(self, positions):
        self.positions = {name: (float(x), float(y)) for name, (x, y) in positions.items()}
        self.writes = []

    def GetPosTable(self, tool):
        x, y = self.positions[tool.Name]
        return {1: x, 2: y}

    def SetPos(self, tool, x, y):
        self.writes.append((tool.Name, float(x), float(y)))
        self.positions[tool.Name] = (float(x), float(y))
        return True


class MockComp:
    def __init__(self, flow):
        self.CurrentFrame = type("Frame", (), {"FlowView": flow})()
        self.undo = []

    def StartUndo(self, name):
        self.undo.append(("start", name))

    def EndUndo(self, keep):
        self.undo.append(("end", bool(keep)))


def _payload(flow, *, nested=False, changed=False):
    if nested:
        nodes = [
            {"name": "RootSource", "type": "Loader", "parent": None},
            {"name": "OuterGroup", "type": "GroupOperator", "parent": None},
            {"name": "OuterProcess", "type": "Blur", "parent": "OuterGroup"},
            {"name": "InnerGroup", "type": "GroupOperator", "parent": "OuterGroup"},
            {"name": "InnerSource", "type": "Loader", "parent": "InnerGroup"},
            {"name": "RootOut", "type": "MediaOut", "parent": None},
        ]
        connections = [
            {"source": "RootSource", "source_output_id": "Output", "target": "OuterGroup", "target_input_id": "Input"},
            {"source": "InnerSource", "source_output_id": "Output", "target": "InnerGroup", "target_input_id": "Input"},
            {"source": "InnerGroup", "source_output_id": "MainOutput1", "target": "OuterProcess", "target_input_id": "Input"},
            {"source": "OuterGroup", "source_output_id": "MainOutput1", "target": "RootOut", "target_input_id": "Input"},
        ]
    else:
        nodes = [
            {"name": "Source", "type": "Loader", "parent": None},
            {"name": "Merge", "type": "Merge", "parent": None},
            {"name": "Output", "type": "MediaOut", "parent": None},
        ]
        connections = [
            {"source": "Source", "source_output_id": "Output", "target": "Merge", "target_input_id": "Background"},
            {"source": "Merge", "source_output_id": "Output", "target": "Output", "target_input_id": "Input"},
        ]
    for node in nodes:
        node["position"] = list(flow.positions[node["name"]])
    fields = _fields(True)
    if changed:
        fields["parameters"] = {"state": "complete", "value": {"changed": True}}
    return {"nodes": nodes, "connections": connections, "fields": fields}


class StrictApplyTests(unittest.TestCase):
    def _flat_fixture(self):
        positions = {"Source": (8.0, 4.0), "Merge": (2.0, 9.0), "Output": (4.0, 1.0)}
        flow = MockFlow(positions)
        comp = MockComp(flow)
        tools = {name: MockTool(name) for name in positions}

        def reader(_comp, _flow, *, source):
            return build_processing_snapshot(_payload(flow), source=source)

        return comp, flow, tools, reader

    def test_small_fixture_maps_plan_and_is_stable_on_run2(self):
        comp, flow, tools, reader = self._flat_fixture()
        result = execute_strict_preserve(
            comp,
            tools,
            snapshot_reader=reader,
            require_first_move=True,
        )
        self.assertGreater(result.run1.moved_count, 0)
        self.assertEqual(result.run2.moved_count, 0)
        self.assertTrue(result.stable)
        self.assertTrue(result.run1.processing_unchanged)
        self.assertEqual(result.run1.readback_positions, result.run2.readback_positions)
        self.assertEqual(result.run1.scope_origins[None], (8.0, 4.0))
        self.assertEqual(result.run1.desired_positions["Source"], (8.0, 4.0))
        self.assertEqual(result.run1.desired_positions["Merge"], (12.0, 4.0))
        self.assertEqual(comp.undo[-2:], [("start", "ResolveNodeKit: Strict Preserve"), ("end", True)])

    def test_incomplete_handle_coverage_refuses_before_write(self):
        comp, flow, tools, reader = self._flat_fixture()
        preparation = prepare_strict_plan(comp, flow, snapshot_reader=reader)
        with self.assertRaises(StrictHostApplyError):
            from resolve_node_kit.fusion.strict_apply import apply_strict_plan

            apply_strict_plan(preparation, comp, {"Source": tools["Source"]}, flow, snapshot_reader=reader)
        self.assertEqual(flow.writes, [])

    def test_processing_signature_mismatch_rolls_back(self):
        comp, flow, tools, _reader = self._flat_fixture()
        before = dict(flow.positions)
        calls = {"count": 0}

        def reader(_comp, _flow, *, source):
            calls["count"] += 1
            return build_processing_snapshot(
                _payload(flow, changed=calls["count"] >= 2),
                source=source,
            )

        preparation = prepare_strict_plan(comp, flow, snapshot_reader=reader)
        with self.assertRaises(StrictHostApplyError):
            from resolve_node_kit.fusion.strict_apply import apply_strict_plan

            apply_strict_plan(preparation, comp, tools, flow, snapshot_reader=reader)
        self.assertEqual(flow.positions, before)
        self.assertEqual(comp.undo[-1], ("end", False))

    def test_nested_plan_exposes_local_scope_mapping(self):
        positions = {
            "RootSource": (0.0, 0.0),
            "OuterGroup": (4.0, 0.0),
            "OuterProcess": (1.0, 2.0),
            "InnerGroup": (3.0, 2.0),
            "InnerSource": (0.0, 1.0),
            "RootOut": (8.0, 0.0),
        }
        flow = MockFlow(positions)
        comp = MockComp(flow)
        tools = {name: MockTool(name) for name in positions}

        def reader(_comp, _flow, *, source):
            return build_processing_snapshot(_payload(flow, nested=True), source=source)

        preparation = prepare_strict_plan(comp, flow, snapshot_reader=reader)
        self.assertIn("OuterGroup", preparation.plan.scope_placements)
        self.assertIn("InnerGroup", preparation.plan.scope_placements)
        desired, origins = map_strict_plan_to_host(preparation, calibration=FlowViewCalibration())
        self.assertEqual(set(desired), set(tools))
        self.assertEqual(set(origins), {None, "OuterGroup", "InnerGroup"})
        encoded = preparation.plan.as_dict()
        self.assertIn("scope_placements", encoded)
        self.assertIn("scope_offsets", encoded)


if __name__ == "__main__":
    unittest.main()
