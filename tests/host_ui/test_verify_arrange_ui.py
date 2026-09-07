import unittest

from scripts.host.verify_arrange_ui import ARRANGE_LABELS, classify_window, parse_moved


class ArrangeUiAClassificationTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
