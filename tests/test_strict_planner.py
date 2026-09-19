import unittest
from dataclasses import replace

from resolve_node_kit.fusion import plan_strict as exported_plan_strict
from resolve_node_kit.fusion.strict_planner import (
    CoverageStatus,
    StrictCoverageError,
    build_strict_snapshot,
    build_strict_snapshot_from_processing,
    fixture_catalogue,
    plan_strict,
    validate_strict_plan,
)


class StrictPlannerTests(unittest.TestCase):
    def test_strict_planner_is_exported_from_fusion_package(self):
        self.assertIs(exported_plan_strict, plan_strict)

    def test_so10_processing_snapshot_mapping_preserves_complete_and_unknown_states(self):
        from resolve_node_kit.fusion.processing_snapshot import REQUIRED_PROCESSING_FIELDS, build_processing_snapshot

        fields = {key: {"state": "complete", "value": []} for key in REQUIRED_PROCESSING_FIELDS}
        payload = {
            "source": "synthetic-so10",
            "nodes": {
                "loader": {"name": "loader", "type": "Loader", "parent": None, "position": [0, 0]},
                "out": {"name": "out", "type": "MediaOut", "parent": None, "position": [3, 0]},
            },
            "connections": [
                {
                    "source": "loader",
                    "source_output_id": "Output",
                    "target": "out",
                    "target_input_id": "Input",
                    "state": "complete",
                }
            ],
            "fields": fields,
        }
        processing = build_processing_snapshot(payload)
        snapshot = build_strict_snapshot_from_processing(processing)
        plan = plan_strict(snapshot)
        self.assertTrue(validate_strict_plan(snapshot, plan)["ok"])
        self.assertEqual(snapshot.edges[0].source_output_id, "Output")

        fields["ports"] = {"state": "unknown", "detail": "host did not expose ports"}
        incomplete = build_processing_snapshot(payload)
        incomplete_snapshot = build_strict_snapshot_from_processing(incomplete)
        with self.assertRaises(StrictCoverageError):
            plan_strict(incomplete_snapshot)

    def test_port_labelled_multiedges_and_duplicate_ordinals_are_preserved(self):
        nodes = [
            {"uid": "source", "display_name": "Loader", "reg_id": "Loader"},
            {"uid": "merge", "display_name": "Merge", "reg_id": "Merge"},
            {"uid": "out", "display_name": "MediaOut", "reg_id": "MediaOut"},
        ]
        edges = [
            {
                "source": "source",
                "source_output_id": "Output",
                "target": "merge",
                "target_input_id": "Background",
                "processing_role": "background",
                "visual_continuity": "rail",
            },
            {
                "source": "source",
                "source_output_id": "Output",
                "target": "merge",
                "target_input_id": "Foreground",
                "processing_role": "foreground",
                "visual_continuity": "feeder",
            },
            {
                "uid": "duplicate-b",
                "source": "source",
                "source_output_id": "Aux",
                "target": "merge",
                "target_input_id": "Mask",
                "processing_role": "mask",
            },
            {
                "uid": "duplicate-a",
                "source": "source",
                "source_output_id": "Aux",
                "target": "merge",
                "target_input_id": "Mask",
                "processing_role": "mask",
            },
            {
                "source": "merge",
                "source_output_id": "Output",
                "target": "out",
                "target_input_id": "Input",
                "processing_role": "main",
            },
        ]
        snapshot = build_strict_snapshot(nodes, edges, input_coverage="complete")
        self.assertEqual(len(snapshot.edges), 5)
        duplicate_ids = [edge.identity() for edge in snapshot.edges if edge.source_output_id == "Aux"]
        self.assertEqual(duplicate_ids, ["duplicate-a#0", "duplicate-b#1"])
        plan = plan_strict(snapshot)
        self.assertEqual(set(plan.edge_coverage), {edge.identity() for edge in snapshot.edges})
        self.assertTrue(plan.all_edges_covered)
        roles = plan.diagnostics["edge_processing_roles"]
        continuity = plan.diagnostics["edge_visual_continuities"]
        self.assertEqual(roles["source:Output->merge:Background#0"], "background")
        self.assertEqual(continuity["source:Output->merge:Background#0"], "rail")
        self.assertEqual(roles["source:Output->merge:Foreground#0"], "foreground")
        self.assertEqual(continuity["source:Output->merge:Foreground#0"], "feeder")
        self.assertTrue(validate_strict_plan(snapshot, plan)["ok"])

    def test_processing_role_is_not_derived_from_display_name_and_rename_is_stable(self):
        edges = [
            {"source": "a", "source_output_id": "out", "target": "b", "target_input_id": "background", "processing_role": "background"},
            {"source": "b", "source_output_id": "out", "target": "c", "target_input_id": "input", "processing_role": "main"},
        ]
        original = build_strict_snapshot(
            [
                {"uid": "a", "display_name": "Original Loader", "reg_id": "Loader"},
                {"uid": "b", "display_name": "Original Merge", "reg_id": "Merge"},
                {"uid": "c", "display_name": "Original Output", "reg_id": "MediaOut"},
            ],
            edges,
            input_coverage="complete",
        )
        renamed = build_strict_snapshot(
            [
                {"uid": "a", "display_name": "Renamed Z", "reg_id": "Loader"},
                {"uid": "b", "display_name": "Renamed A", "reg_id": "Merge"},
                {"uid": "c", "display_name": "Renamed Q", "reg_id": "MediaOut"},
            ],
            list(reversed(edges)),
            input_coverage="complete",
        )
        first = plan_strict(original)
        second = plan_strict(renamed)
        self.assertEqual(first.placements, second.placements)
        self.assertEqual(first.rectangles, second.rectangles)
        self.assertEqual(first.edge_coverage, second.edge_coverage)
        self.assertEqual(first.motif_coverage, second.motif_coverage)
        self.assertEqual(first.as_dict()["modules"], second.as_dict()["modules"])

    def test_recursive_group_bounds_and_sibling_rectangle_nonoverlap(self):
        snapshot = build_strict_snapshot(
            [
                {"uid": "group", "is_group": True, "display_name": "Group"},
                {"uid": "child-a", "parent": "group", "width": 2, "height": 2},
                {"uid": "child-b", "parent": "group", "width": 1, "height": 1},
                {"uid": "output", "reg_id": "MediaOut", "width": 3, "height": 2},
            ],
            [
                {"source": "child-a", "source_output_id": "out", "target": "child-b", "target_input_id": "input"},
                # This boundary edge is retained even though it is not a local
                # edge in either scope.
                {"source": "child-b", "source_output_id": "out", "target": "output", "target_input_id": "input"},
            ],
            input_coverage="complete",
        )
        plan = plan_strict(snapshot)
        result = validate_strict_plan(snapshot, plan)
        self.assertTrue(result["ok"], result)
        group_rect = plan.rectangles["group"]
        for child in ("child-a", "child-b"):
            child_rect = plan.rectangles[child]
            self.assertGreaterEqual(child_rect.x, group_rect.x)
            self.assertGreaterEqual(child_rect.y, group_rect.y)
            self.assertLessEqual(child_rect.right, group_rect.right)
            self.assertLessEqual(child_rect.bottom, group_rect.bottom)
        self.assertTrue(plan.all_edges_covered)
        self.assertEqual(plan.diagnostics["rectangle_overlap_count"], 0)

    def test_shared_source_is_placed_once_and_modules_are_explicit(self):
        snapshot = build_strict_snapshot(
            [
                {"uid": "shared", "reg_id": "Loader"},
                {"uid": "merge-a", "reg_id": "Merge"},
                {"uid": "merge-b", "reg_id": "Merge"},
                {"uid": "out", "reg_id": "MediaOut"},
            ],
            [
                {"source": "shared", "source_output_id": "out-a", "target": "merge-a", "target_input_id": "Background", "processing_role": "background"},
                {"source": "shared", "source_output_id": "out-b", "target": "merge-b", "target_input_id": "Background", "processing_role": "background"},
                {"source": "merge-a", "source_output_id": "out", "target": "out", "target_input_id": "Input", "processing_role": "main"},
                {"source": "merge-b", "source_output_id": "out", "target": "out", "target_input_id": "Aux", "processing_role": "auxiliary"},
            ],
            input_coverage="complete",
        )
        plan = plan_strict(snapshot)
        self.assertEqual(len(plan.placements), 4)
        self.assertEqual(len({plan.placements["shared"]}), 1)
        self.assertEqual({module.kind for module in plan.modules}, {"rail", "region", "feeder"})
        self.assertEqual(plan.diagnostics["all_edge_coverage"]["missing"], [])

    def test_unknown_or_missing_input_coverage_fails_closed(self):
        snapshot = build_strict_snapshot(
            [{"uid": "a"}, {"uid": "b", "input_state": "unknown"}],
            [{"source": "a", "source_output_id": "out", "target": "b", "target_input_id": "input"}],
            input_coverage="complete",
        )
        with self.assertRaises(StrictCoverageError):
            plan_strict(snapshot)

        missing_edge = build_strict_snapshot(
            [{"uid": "a"}, {"uid": "b"}],
            [{"source": "a", "source_output_id": "out", "target": "b", "target_input_id": "input", "state": "missing"}],
            input_coverage="complete",
        )
        with self.assertRaises(StrictCoverageError):
            plan_strict(missing_edge)

        omitted = build_strict_snapshot(
            [{"uid": "a"}, {"uid": "b"}],
            [{"source": "a", "source_output_id": "out", "target": "b", "target_input_id": "input"}],
        )
        self.assertIn("snapshot:input_coverage=missing", omitted.unresolved())
        with self.assertRaises(StrictCoverageError):
            plan_strict(omitted)

    def test_fresh_validator_rejects_missing_rectangles(self):
        snapshot = build_strict_snapshot(
            ["a", "b"],
            [{"source": "a", "source_output_id": "out", "target": "b", "target_input_id": "in"}],
            input_coverage="complete",
        )
        plan = plan_strict(snapshot)
        rectangles = dict(plan.rectangles)
        del rectangles["b"]
        tampered = replace(plan, rectangles=rectangles)
        result = validate_strict_plan(snapshot, tampered)
        self.assertFalse(result["ok"])
        self.assertEqual(result["missing_rectangles"], ["b"])

    def test_reference_profile_reduction_and_multigroup_stress(self):
        snapshot = build_strict_snapshot(
            [
                {"uid": "source-bg", "reg_id": "Loader"},
                {"uid": "source-fg", "reg_id": "Loader"},
                {"uid": "merge-a", "reg_id": "Merge"},
                {"uid": "merge-b", "reg_id": "Merge"},
                {"uid": "output", "reg_id": "MediaOut"},
            ],
            [
                {"source": "source-bg", "source_output_id": "out", "target": "merge-a", "target_input_id": "Background", "processing_role": "background"},
                {"source": "source-fg", "source_output_id": "out", "target": "merge-a", "target_input_id": "Foreground", "processing_role": "foreground", "visual_continuity": "feeder"},
                {"source": "merge-a", "source_output_id": "out", "target": "merge-b", "target_input_id": "Background", "processing_role": "background"},
                {"source": "source-fg", "source_output_id": "aux", "target": "merge-b", "target_input_id": "Mask", "processing_role": "mask"},
                {"source": "merge-b", "source_output_id": "out", "target": "output", "target_input_id": "Input", "processing_role": "main"},
            ],
            input_coverage="complete",
        )
        plan = plan_strict(snapshot)
        self.assertIn("reduction", {module.kind for module in plan.modules})
        self.assertEqual(plan.diagnostics["edge_count"], 5)
        self.assertEqual(plan.diagnostics["all_edge_coverage"]["missing"], [])

        groups = [{"uid": f"group-{index}", "is_group": True} for index in range(29)]
        members = [{"uid": f"member-{index}", "parent": f"group-{index}", "width": 2, "height": 1} for index in range(29)]
        census = build_strict_snapshot(groups + members, [], input_coverage="complete")
        census_plan = plan_strict(census)
        self.assertEqual(sum(node.is_group for node in census.nodes), 29)
        self.assertTrue(validate_strict_plan(census, census_plan)["ok"])

        count = 1101
        deep_nodes = [{"uid": f"node-{index}"} for index in range(count)]
        deep_edges = [
            {"source": f"node-{index}", "source_output_id": "out", "target": f"node-{index + 1}", "target_input_id": "in"}
            for index in range(count - 1)
        ]
        deep = build_strict_snapshot(deep_nodes, deep_edges, input_coverage="complete")
        deep_plan = plan_strict(deep)
        self.assertEqual(len(deep_plan.placements), count)
        self.assertEqual(deep_plan.diagnostics["rectangle_overlap_count"], 0)

    def test_grid_run2_and_catalogue_split(self):
        snapshot = build_strict_snapshot(
            ["z", "a", "m"],
            [
                {"source": "a", "source_output_id": "out", "target": "m", "target_input_id": "in"},
                {"source": "m", "source_output_id": "out", "target": "z", "target_input_id": "in"},
            ],
            input_coverage="complete",
        )
        first = plan_strict(snapshot)
        second = plan_strict(snapshot)
        self.assertEqual(first.as_dict(), second.as_dict())
        self.assertTrue(all(value.column % 1 == 0 and value.row % 1 == 0 for value in first.placements.values()))
        self.assertEqual(first.policy.pitch, 3)
        self.assertEqual(first.diagnostics["rectangle_overlap_count"], 0)

        catalogue = fixture_catalogue()
        self.assertEqual(set(catalogue), {f"O{index:02d}" for index in range(1, 19)})
        self.assertEqual(catalogue["O12"].status, CoverageStatus.FAIL_CLOSED)
        self.assertEqual(
            {key for key, item in catalogue.items() if item.status is CoverageStatus.HOST_ONLY},
            {"O14", "O16", "O17", "O18"},
        )
        self.assertEqual(
            {key for key, item in catalogue.items() if item.status is CoverageStatus.PLANNER_COVERED},
            {f"O{index:02d}" for index in range(1, 13)} - {"O12"} | {"O13", "O15"},
        )


if __name__ == "__main__":
    unittest.main()
