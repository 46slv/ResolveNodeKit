import unittest

from scripts.host.verify_arrange_behavior import SCHEMA, build_handler_source, classify_behavior


class ArrangeBehaviorVerifierTests(unittest.TestCase):
    def test_source_calls_shared_handler_and_explicit_state(self):
        source = build_handler_source(r"D:\temp\uia\seam.json")
        self.assertIn("execute_arrange_request", source)
        self.assertIn("ArrangeDialogState", source)
        self.assertIn("include_unselected", source)
        self.assertIn('\\"include_unselected\\": true', source)
        self.assertIn("result_ask=ask", source)
        self.assertNotIn("InvokePattern", source)
        self.assertNotIn("menu-invoke", source)

    def test_classifier_accepts_whole_comp_as_canonical_fixture(self):
        payload = {
            "state": {"include_unselected": True, "ungroup": False},
            "pre": {
                "positions": {"A": [0, 0], "B": [1, 1], "C": [2, 2], "D": [3, 3]},
                "connections": ["A->B.Input"],
                "parents": {"A": None, "B": None, "C": None, "D": None},
                "groups": [],
                "selected": ["A"],
            },
            "runs": [
                {"status": "success", "result": {"moved_count": 4, "arranged_count": 4}},
                {"status": "success", "result": {"moved_count": 0, "arranged_count": 4}},
            ],
            "post_first": {
                "positions": {"A": [0, 0], "B": [3, 0], "C": [6, 0], "D": [9, 0]},
                "connections": ["A->B.Input"],
                "parents": {"A": None, "B": None, "C": None, "D": None},
                "groups": [],
            },
            "post_second": {},
            "undo_snapshots": [{
                "positions": {"A": [0, 0], "B": [1, 1], "C": [2, 2], "D": [3, 3]},
                "connections": ["A->B.Input"],
                "parents": {"A": None, "B": None, "C": None, "D": None},
            }],
        }
        result = classify_behavior(payload)
        self.assertEqual(result["HOST_PRODUCT_BEHAVIOR"]["status"], "PASS")
        self.assertEqual(result["HOST_PRODUCT_BEHAVIOR"]["scope_mode"], "whole_comp")
        self.assertTrue(result["HOST_PRODUCT_BEHAVIOR"]["whole_comp_scope_complete"])
        self.assertEqual(result["HOST_INVARIANTS"]["status"], "PASS")

    def test_classifier_emits_behavior_layers(self):
        payload = {
            "state": {"include_unselected": False, "ungroup": False},
            "pre": {
                "positions": {"A": [0, 0], "B": [1, 1], "C": [2, 2], "D": [3, 3], "U": [50, 50]},
                "connections": ["A->B.Input"],
                "parents": {"A": None, "B": None, "C": None, "D": None, "U": None},
                "groups": [],
                "selected": ["A", "B", "C", "D"],
            },
            "runs": [
                {"status": "success", "result": {"moved_count": 1}},
                {"status": "success", "result": {"moved_count": 0}},
            ],
            "post_first": {
                "positions": {"A": [2, 0], "B": [3, 1], "C": [4, 2], "D": [5, 3], "U": [50, 50]},
                "connections": ["A->B.Input"],
                "parents": {"A": None, "B": None, "C": None, "D": None, "U": None},
                "groups": [],
            },
            "post_second": {},
            "undo_snapshots": [{
                "positions": {"A": [0, 0], "B": [1, 1], "C": [2, 2], "D": [3, 3], "U": [50, 50]},
                "connections": ["A->B.Input"],
                "parents": {"A": None, "B": None, "C": None, "D": None, "U": None},
            }],
        }
        result = classify_behavior(payload)
        self.assertEqual(result["schema"], SCHEMA)
        self.assertEqual(result["HOST_PRODUCT_BEHAVIOR"]["status"], "PASS")
        self.assertEqual(result["HOST_PRODUCT_BEHAVIOR"]["effective_include_unselected"], "PASS_BEHAVIORAL")
        self.assertEqual(result["HOST_INVARIANTS"]["status"], "PASS")
        self.assertEqual(result["ACCESSIBILITY_LIMITATION"]["status"], "BLOCKED_HOST_ACCESSIBILITY_HARD")
