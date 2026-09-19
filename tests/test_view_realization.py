import copy
import json
import unittest

from resolve_node_kit.fusion.view_realization import (
    VIEW_REALIZATION_SCHEMA,
    canonical_edge_id,
    qualify_view_evidence,
    require_qualified_view_evidence,
)


RUN_ID = "view-run-001"
EDGE_A = canonical_edge_id("Loader", "Output", "Merge", "Background", 0)
EDGE_B = canonical_edge_id("Loader", "Aux", "Merge", "Mask", 0)


def _sample(sample_id, kind, edge_ids, zoom):
    return {
        "sample_id": sample_id,
        "kind": kind,
        "run_id": RUN_ID,
        "viewport": {"x": 0, "y": 0, "width": 1200, "height": 800, "zoom": zoom},
        "edge_ids": list(edge_ids),
        "region": "all-edges" if kind == "overview" else "aggregation-and-mask",
    }


def _observation(stage, mode):
    return {
        "stage": stage,
        "run_id": RUN_ID,
        "mode": mode,
        "node_rectangles": {
            "Loader": {"x": 10, "y": 20, "width": 80, "height": 40},
            "Merge": {"x": 220, "y": 20, "width": 100, "height": 60},
        },
        "group_rectangles": {"Group-A": {"x": 0, "y": 0, "width": 360, "height": 160}},
        "port_positions": {
            "Loader:Output": {"node_id": "Loader", "port_id": "Output", "x": 90, "y": 30, "role": "output"},
            "Loader:Aux": {"node_id": "Loader", "port_id": "Aux", "x": 90, "y": 50, "role": "auxiliary"},
            "Merge:Background": {"node_id": "Merge", "port_id": "Background", "x": 220, "y": 30, "role": "input"},
            "Merge:Mask": {"node_id": "Merge", "port_id": "Mask", "x": 220, "y": 50, "role": "mask"},
        },
        "viewport": {"x": 0, "y": 0, "width": 1200, "height": 800, "zoom": 1.0},
        "edge_ids": [EDGE_A, EDGE_B],
    }


def _base_payload():
    mode_pre = {"raw_value": 0, "name": "straight", "evidence_source": "same-view-readback", "scope": "target-view"}
    mode_post = {"raw_value": 1, "name": "orthogonal", "evidence_source": "same-view-readback", "scope": "target-view"}
    return {
        "schema": VIEW_REALIZATION_SCHEMA,
        "run_id": RUN_ID,
        "target_id": "comp-view-01",
        "mode": mode_post,
        "pre": _observation("pre", mode_pre),
        "post": _observation("post", mode_post),
        "restored": _observation("restored", mode_pre),
        "edge_ids": [EDGE_A, EDGE_B],
        "edge_geometry": [
            {
                "edge_id": EDGE_A,
                "source": "Loader",
                "source_output_id": "Output",
                "target": "Merge",
                "target_input_id": "Background",
                "ordinal": 0,
                "geometry_coverage": "measured",
                "sample_ids": ["overview-1", "difficult-1"],
            },
            {
                "edge_id": EDGE_B,
                "source": "Loader",
                "source_output_id": "Aux",
                "target": "Merge",
                "target_input_id": "Mask",
                "ordinal": 0,
                "geometry_coverage": "native-contract",
                "sample_ids": ["overview-1", "difficult-1"],
            },
        ],
        "coverage": {"mask": "complete", "boundary": "complete", "multiedge": "complete", "all_edges": "complete"},
        "native_renderer_contract": {
            "status": "pass",
            "evidence_source": "same-view-readback",
            "scope": "target-view",
            "run_id": RUN_ID,
        },
        "samples": [
            _sample("overview-1", "overview", [EDGE_A, EDGE_B], 1.0),
            _sample("difficult-1", "difficult-region", [EDGE_A, EDGE_B], 2.5),
        ],
    }


class ViewRealizationEvidenceTests(unittest.TestCase):
    def test_valid_synthetic_evidence_is_qualified_and_json_safe(self):
        result = qualify_view_evidence(_base_payload())
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["status"], "HOST_RENDERER_CONTRACT_PASS")
        self.assertEqual(result["evidence"]["run_id"], RUN_ID)
        json.dumps(result, allow_nan=False)
        normalized = require_qualified_view_evidence(_base_payload())
        self.assertEqual(normalized.edge_ids, (EDGE_A, EDGE_B))

    def test_numeric_mode_value_alone_is_refused(self):
        payload = _base_payload()
        payload["mode"] = 1
        result = qualify_view_evidence(payload)
        self.assertFalse(result["ok"])
        self.assertIn("numeric mode alone", result["reasons"][0])

    def test_missing_or_wrong_schema_is_refused(self):
        for schema in (None, "other-schema/v9"):
            with self.subTest(schema=schema):
                payload = _base_payload()
                if schema is None:
                    payload.pop("schema")
                else:
                    payload["schema"] = schema
                result = qualify_view_evidence(payload)
                self.assertFalse(result["ok"])
                self.assertIn("schema", result["reasons"][0])

    def test_observation_stage_slot_mismatch_is_refused(self):
        payload = _base_payload()
        payload["pre"]["stage"] = "post"
        result = qualify_view_evidence(payload)
        self.assertFalse(result["ok"])
        self.assertIn("must be pre", result["reasons"][0])

    def test_edge_endpoint_ports_and_node_rectangles_are_required(self):
        payload = _base_payload()
        payload["post"]["port_positions"].pop("Merge:Mask")
        result = qualify_view_evidence(payload)
        self.assertFalse(result["ok"])
        self.assertIn("endpoint ports", result["reasons"][0])

        payload = _base_payload()
        payload["post"]["node_rectangles"].pop("Merge")
        result = qualify_view_evidence(payload)
        self.assertFalse(result["ok"])
        self.assertIn("node rectangles", result["reasons"][0])

    def test_edge_endpoint_roles_are_directionally_validated(self):
        payload = _base_payload()
        payload["post"]["port_positions"]["Loader:Output"]["role"] = "input"
        result = qualify_view_evidence(payload)
        self.assertFalse(result["ok"])
        self.assertIn("not output/auxiliary", result["reasons"][0])

    def test_overview_only_evidence_is_refused(self):
        payload = _base_payload()
        payload["samples"] = [payload["samples"][0]]
        result = qualify_view_evidence(payload)
        self.assertFalse(result["ok"])
        self.assertIn("difficult-region", result["reasons"][0])

    def test_center_only_evidence_is_refused(self):
        payload = _base_payload()
        payload["post"]["port_positions"] = {
            "Loader": {"center": {"x": 50, "y": 40}},
            "Merge": {"center": {"x": 270, "y": 50}},
        }
        result = qualify_view_evidence(payload)
        self.assertFalse(result["ok"])
        self.assertIn("port_positions", result["reasons"][0])

    def test_missing_mask_boundary_or_multiedge_coverage_is_refused(self):
        for missing in ("mask", "boundary", "multiedge"):
            with self.subTest(missing=missing):
                payload = _base_payload()
                payload["coverage"][missing] = "missing"
                result = qualify_view_evidence(payload)
                self.assertFalse(result["ok"])
                self.assertIn(missing, result["reasons"][0])

    def test_mixed_run_records_are_refused(self):
        payload = _base_payload()
        payload["samples"][1]["run_id"] = "other-run"
        result = qualify_view_evidence(payload)
        self.assertFalse(result["ok"])
        self.assertIn("different run", result["reasons"][0])

    def test_noncanonical_or_incomplete_edge_id_is_refused(self):
        payload = _base_payload()
        payload["edge_geometry"][0]["edge_id"] = "Loader->Merge"
        result = qualify_view_evidence(payload)
        self.assertFalse(result["ok"])
        self.assertIn("canonical", result["reasons"][0])

    def test_observation_without_explicit_ports_is_refused(self):
        payload = _base_payload()
        payload["pre"].pop("port_positions")
        result = qualify_view_evidence(payload)
        self.assertFalse(result["ok"])
        self.assertIn("port_positions", result["reasons"][0])


if __name__ == "__main__":
    unittest.main()
