import unittest

from scripts.host.probe_arrange_msaa import ARRANGE_LABELS, classify_msaa


class ArrangeMsaaClassificationTests(unittest.TestCase):
    def test_legacy_semantic_button_and_checkbox_are_identity_safe(self):
        uia = {
            "candidates": [
                {
                    "class": "Fusion::CustomButton",
                    "legacy_pattern_available": True,
                    "legacy": {
                        "name": "OK",
                        "role": "43",
                        "state": "0",
                        "default_action": "Press",
                        "child_id": 0,
                    },
                },
                {
                    "class": "Fusion::CustomButton",
                    "legacy_pattern_available": True,
                    "legacy": {
                        "name": "Cancel",
                        "role": "43",
                        "state": "0",
                        "default_action": "Press",
                        "child_id": 0,
                    },
                },
                {
                    "class": "Fusion::CustomCheckBox",
                    "legacy_pattern_available": True,
                    "legacy": {
                        "name": ARRANGE_LABELS[0],
                        "role": "44",
                        "state": "0",
                        "default_action": "Press",
                        "child_id": 0,
                    },
                },
            ]
        }

        result = classify_msaa(uia, {"objects": []})

        self.assertEqual(result["msaa_capability"], "PASS_SEMANTIC_IDENTITY")
        self.assertTrue(result["run_identity"]["semantic_identity"])
        self.assertTrue(result["cancel_identity"]["semantic_identity"])
        self.assertTrue(result["checkbox_identity"]["semantic_identity"])
        self.assertEqual(result["run_identity"]["invocation"], "not_attempted")

    def test_oleacc_rows_can_supply_identity_without_legacy_pattern(self):
        result = classify_msaa(
            {"candidates": [{"legacy_pattern_available": False}]},
            {
                "objects": [
                    {
                        "accessible_object": True,
                        "source": "dialog",
                        "semantic_rows": [
                            {
                                "acc_name": "Run",
                                "acc_role": 43,
                                "acc_role_name": "ROLE_SYSTEM_PUSHBUTTON",
                                "acc_state": 0,
                                "acc_default_action": "Press",
                                "child_id": 4,
                            }
                        ],
                    }
                ]
            },
        )

        self.assertEqual(result["msaa_capability"], "PASS_SEMANTIC_IDENTITY")
        self.assertEqual(result["run_identity"]["name"], "Run")
        self.assertEqual(result["run_identity"]["child_id"], 4)

    def test_empty_or_unnamed_msaa_surface_is_hard_blocked(self):
        result = classify_msaa(
            {
                "candidates": [
                    {
                        "legacy_pattern_available": True,
                        "legacy": {
                            "name": "",
                            "role": "0",
                            "state": "0",
                            "default_action": "",
                        },
                    }
                ]
            },
            {
                "objects": [
                    {
                        "accessible_object": True,
                        "semantic_rows": [
                            {
                                "acc_name": "",
                                "acc_role": 9,
                                "acc_role_name": "ROLE_SYSTEM_CLIENT",
                                "acc_state": 0,
                                "acc_default_action": "",
                            }
                        ],
                    }
                ]
            },
        )

        self.assertEqual(result["msaa_capability"], "BLOCKED_HOST_ACCESSIBILITY_HARD")
        self.assertFalse(result["run_identity"]["semantic_identity"])
        self.assertFalse(result["cancel_identity"]["semantic_identity"])
        self.assertFalse(result["checkbox_identity"]["semantic_identity"])


if __name__ == "__main__":
    unittest.main()
