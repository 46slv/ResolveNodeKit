import unittest

from scripts.host.verify_arrange_ui import (
    ARRANGE_LABELS,
    WHOLE_COMP_MESSAGE,
    classify_window,
    parse_moved,
)


class ArrangeUiAClassificationTests(unittest.TestCase):
    def test_whole_comp_confirmation_is_the_first_usable_setup(self):
        result = classify_window([
            {"control": "ControlType.Text", "class": "QLabel", "name": WHOLE_COMP_MESSAGE},
            {"control": "ControlType.Button", "class": "QPushButton", "name": "OK"},
            {"control": "ControlType.Button", "class": "QPushButton", "name": "Cancel"},
        ])

        self.assertEqual(result["kind"], "setup")
        self.assertTrue(result["scope_message_exposed"])
        self.assertEqual(result["scope_mode"], "whole_comp")
        self.assertEqual(result["checkbox_readback_status"], "NOT_APPLICABLE_WHOLE_COMP")

    def test_qt_group_checkboxes_without_labels_are_not_safe_to_invoke(self):
        nodes = [
            {"control": "ControlType.Group", "class": "Fusion::CheckBoxControl"},
            {"control": "ControlType.Text", "class": "QLabel"},
            {"control": "ControlType.Group", "class": "Fusion::CustomCheckBox"},
            {"control": "ControlType.Text", "class": "QLabel"},
            {"control": "ControlType.Group", "class": "Fusion::CheckBoxControl"},
            {"control": "ControlType.Group", "class": "Fusion::CustomCheckBox"},
        ]

        result = classify_window(nodes)

        self.assertEqual(result["kind"], "setup")
        self.assertEqual(len(result["checkboxes"]), 4)
        self.assertEqual(result["expected_labels"], list(ARRANGE_LABELS))
        self.assertFalse(result["labels_exposed"])
        self.assertEqual(result["exposed_labels"], [])

    def test_standard_labelled_checkboxes_are_detectable(self):
        nodes = [
            {
                "control": "ControlType.CheckBox",
                "class": "QCheckBox",
                "name": ARRANGE_LABELS[0],
                "toggle": "Off",
            },
            {
                "control": "ControlType.CheckBox",
                "class": "QCheckBox",
                "name": ARRANGE_LABELS[1],
                "toggle": "Off",
            },
        ]

        result = classify_window(nodes)

        self.assertEqual(result["kind"], "setup")
        self.assertTrue(result["labels_exposed"])
        self.assertEqual(result["exposed_labels"], sorted(ARRANGE_LABELS))
        self.assertEqual([row["toggle"] for row in result["checkboxes"]], ["Off", "Off"])

    def test_result_and_moved_count_are_readable(self):
        result = classify_window([
            {"control": "ControlType.Text", "name": "Result", "class": "QLabel"},
        ])

        self.assertEqual(result["kind"], "result")
        self.assertEqual(parse_moved("Arrange complete: moved=3"), 3)
        self.assertEqual(parse_moved("moved=0"), 0)
        self.assertIsNone(parse_moved("no movement field"))

    def test_accessibility_and_behavioral_layers_are_separate(self):
        result = classify_window([
            {"control": "ControlType.Group", "class": "Fusion::CheckBoxControl"},
            {"control": "ControlType.Group", "class": "Fusion::CustomCheckBox"},
            {"control": "ControlType.Group", "class": "Fusion::CustomButton",
             "patterns": "InvokePatternIdentifiers.Pattern"},
        ])

        self.assertEqual(result["checkbox_readback_status"], "BLOCKED_HOST_ACCESSIBILITY")
        self.assertFalse(result["run_button_identity"])
        self.assertFalse(result["cancel_button_identity"])
        self.assertEqual(result["behavioral_default_status"], "UNVERIFIED")

    def test_named_invoke_buttons_have_safe_identity_flags(self):
        result = classify_window([
            {"control": "ControlType.CheckBox", "class": "QCheckBox",
             "name": ARRANGE_LABELS[0],
             "patterns": "TogglePatternIdentifiers.Pattern"},
            {"control": "ControlType.CheckBox", "class": "QCheckBox",
             "name": ARRANGE_LABELS[1],
             "patterns": "TogglePatternIdentifiers.Pattern"},
            {"control": "ControlType.Button", "class": "QPushButton",
             "name": "OK", "patterns": "InvokePatternIdentifiers.Pattern"},
            {"control": "ControlType.Button", "class": "QPushButton",
             "name": "Cancel", "patterns": "InvokePatternIdentifiers.Pattern"},
        ])

        self.assertTrue(result["run_button_identity"])
        self.assertTrue(result["cancel_button_identity"])
        self.assertEqual(result["checkbox_readback_status"], "PASS")


if __name__ == "__main__":
    unittest.main()
