import json
from pathlib import Path
import unittest

from resolve_node_kit.fusion.processing_snapshot import (
    REQUIRED_PROCESSING_FIELDS,
    SnapshotState,
    SnapshotWriteError,
    audit_layout_reference,
    build_processing_snapshot,
    require_complete_snapshot,
    validate_structure_write,
)


REFERENCE = Path(__file__).parents[1] / "docs" / "reference" / "2026-09-06-fusion-timeline1-layout.json"


class ProcessingSnapshotTests(unittest.TestCase):
    def test_reference_audit_checks_all_source_sections(self):
        result = audit_layout_reference(REFERENCE)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["observed"]["tool_count"], 1109)
        self.assertEqual(result["observed"]["group_count"], 29)
        self.assertEqual(result["observed"]["merge_count"], 257)
        self.assertTrue(result["checks"]["merge_inputs"]["ok"])
        self.assertTrue(result["checks"]["parent_cycles"]["ok"])

    def test_reference_audit_does_not_fill_unknown_parent(self):
        data = {"tool_rows": [{"name": "A", "parent": "Missing", "x": 0, "y": 0, "sx": 0, "sy": 0}], "groups": {}, "merge_rows": []}
        result = audit_layout_reference(data)
        self.assertFalse(result["ok"])
        self.assertFalse(result["checks"]["parent_references"]["ok"])

    def test_port_and_field_states_are_preserved(self):
        snapshot = build_processing_snapshot(
            {
                "nodes": [{"name": "A", "type": {"state": "unsupported", "detail": "host API"}, "parent": None}],
                "connections": [{
                    "source": "A",
                    "source_output_id": "Output",
                    "target": "B",
                    "target_input_id": "Foreground",
                    "state": "absent",
                }],
                "fields": {"parameters": {"state": "error", "detail": "read failed"}},
            },
            source="fixture",
        )
        self.assertEqual(snapshot.nodes["A"].node_type.state, SnapshotState.UNSUPPORTED)
        self.assertEqual(snapshot.connections[0].state, SnapshotState.ABSENT)
        self.assertEqual(snapshot.fields["parameters"].state, SnapshotState.ERROR)
        ok, unresolved = validate_structure_write(snapshot)
        self.assertFalse(ok)
        self.assertTrue(any("unsupported" in item for item in unresolved))
        with self.assertRaises(SnapshotWriteError):
            require_complete_snapshot(snapshot)

    def test_complete_snapshot_is_accepted(self):
        snapshot = build_processing_snapshot(
            {
                "nodes": [
                    {"name": "A", "type": "Loader", "parent": None, "position": [0, 0]},
                    {"name": "M", "type": "Merge", "parent": None, "position": [1, 0]},
                ],
                "connections": [{
                    "source": "A",
                    "source_output_id": "Output",
                    "target": "M",
                    "target_input_id": "Foreground",
                }],
                "fields": {name: {"state": "complete", "value": True} for name in REQUIRED_PROCESSING_FIELDS},
            }
        )
        ok, unresolved = validate_structure_write(snapshot)
        self.assertTrue(ok)
        self.assertEqual(unresolved, ())
        require_complete_snapshot(snapshot)

    def test_missing_connections_are_absent_not_empty_complete(self):
        snapshot = build_processing_snapshot({"nodes": [{"name": "A", "type": "Loader", "parent": None, "position": [0, 0]}]})
        self.assertEqual(snapshot.fields["connections"].state, SnapshotState.ABSENT)
        self.assertFalse(validate_structure_write(snapshot)[0])

    def test_missing_processing_coverage_is_never_complete(self):
        snapshot = build_processing_snapshot(
            {
                "nodes": [{"name": "A", "type": "Loader", "parent": None, "position": [0, 0]}],
                "connections": [],
            }
        )
        ok, unresolved = validate_structure_write(snapshot)
        self.assertFalse(ok)
        self.assertIn("fields.parameters:absent", unresolved)

    def test_both_edge_port_ids_are_required(self):
        snapshot = build_processing_snapshot(
            {
                "nodes": [{"name": "A", "type": "Loader", "parent": None, "position": [0, 0]}],
                "connections": [{"source": "A", "target": "B", "target_input_id": "Foreground"}],
                "fields": {name: {"state": "complete", "value": True} for name in REQUIRED_PROCESSING_FIELDS},
            }
        )
        ok, unresolved = validate_structure_write(snapshot)
        self.assertFalse(ok)
        self.assertIn("connections[0]:error", unresolved)


if __name__ == "__main__":
    unittest.main()
