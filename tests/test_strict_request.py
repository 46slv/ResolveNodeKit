import unittest

from resolve_node_kit.fusion import (
    StrictPreparationError,
    prepare_strict_plan_from_processing,
)
from resolve_node_kit.fusion.processing_snapshot import REQUIRED_PROCESSING_FIELDS, build_processing_snapshot


def _complete_payload():
    return {
        "source": "fixture",
        "nodes": [
            {"name": "Source", "type": "Loader", "parent": None, "position": [0, 0]},
            {"name": "Merge", "type": "Merge", "parent": None, "position": [4, 0]},
            {"name": "Output", "type": "MediaOut", "parent": None, "position": [8, 0]},
        ],
        "connections": [
            {
                "source": "Source",
                "source_output_id": "Output",
                "target": "Merge",
                "target_input_id": "Background",
            },
            {
                "source": "Merge",
                "source_output_id": "Output",
                "target": "Output",
                "target_input_id": "Input",
            },
        ],
        "fields": {name: {"state": "complete", "value": True} for name in REQUIRED_PROCESSING_FIELDS},
    }


class StrictRequestTests(unittest.TestCase):
    def test_complete_processing_snapshot_is_planned_and_independently_validated(self):
        snapshot = build_processing_snapshot(_complete_payload(), source="fixture")
        prepared = prepare_strict_plan_from_processing(snapshot, source="fixture")
        self.assertTrue(prepared.validation["ok"], prepared.validation)
        self.assertTrue(prepared.plan.all_edges_covered)
        self.assertEqual(prepared.plan.diagnostics["node_count"], 3)
        self.assertEqual(prepared.plan.diagnostics["edge_count"], 2)
        payload = prepared.as_dict()
        self.assertEqual(payload["schema"], "resolve-node-kit.strict-preparation/v1")
        self.assertEqual(payload["validation"]["ok"], True)

    def test_missing_processing_coverage_refuses_before_planning(self):
        data = _complete_payload()
        data["fields"]["parameters"] = {"state": "unsupported", "detail": "host API"}
        snapshot = build_processing_snapshot(data, source="fixture")
        with self.assertRaises(StrictPreparationError) as raised:
            prepare_strict_plan_from_processing(snapshot)
        self.assertIn("fields.parameters:unsupported", str(raised.exception))

    def test_missing_position_refuses_even_when_processing_fields_are_complete(self):
        data = _complete_payload()
        del data["nodes"][1]["position"]
        snapshot = build_processing_snapshot(data, source="fixture")
        with self.assertRaises(StrictPreparationError) as raised:
            prepare_strict_plan_from_processing(snapshot)
        self.assertIn("nodes.Merge.position:absent", str(raised.exception))

    def test_host_reader_failure_is_wrapped_without_fallback_or_write(self):
        calls = []

        def reader(*_args, **_kwargs):
            calls.append("read")
            raise RuntimeError("port surface unavailable")

        with self.assertRaises(StrictPreparationError) as raised:
            from resolve_node_kit.fusion.strict_request import prepare_strict_plan

            prepare_strict_plan(object(), snapshot_reader=reader)
        self.assertEqual(calls, ["read"])
        self.assertIn("host snapshot read failed", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
