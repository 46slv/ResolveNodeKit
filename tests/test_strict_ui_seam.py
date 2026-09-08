"""Offline contract tests for the RNK-owned UI observability seam.

These tests do not invoke Resolve, UIA, or the host controller through a
second implementation.  They only verify the shared production seam's
run-id/state/event contract and its pre-start zero-mutation Cancel boundary.
"""

from __future__ import annotations

import unittest
from unittest.mock import patch

from resolve_node_kit.fusion import ArrangeDialogState
from resolve_node_kit.fusion.dialog import ArrangeUiSession
from resolve_node_kit.fusion.arrange_request import execute_arrange_request


class _Comp:
    def GetAttrs(self):
        return {"COMPS_Name": "ui-seam"}

    def GetToolList(self):
        return {"A": object()}


class _Window:
    def Hide(self):
        return None


class StrictUiSeamTests(unittest.TestCase):
    def test_cancel_before_controller_is_zero_mutation_and_observable(self):
        session = ArrangeUiSession(run_id="ui-cancel-1")
        self.assertTrue(session.cancel())
        with patch("resolve_node_kit.fusion.arrange_request.bind_target") as bind:
            result = execute_arrange_request(
                None,
                None,
                None,
                ArrangeDialogState(True, False),
                show_result_dialog=False,
                ui_session=session,
            )
        bind.assert_not_called()
        self.assertEqual(result.status, "cancelled")
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.run_id, "ui-cancel-1")
        self.assertEqual(result.ui_state, "cancelled")
        self.assertEqual([item["event"] for item in result.ui_events], ["setup", "cancelled"])

    def test_busy_result_terminal_events_share_run_id(self):
        session = ArrangeUiSession(run_id="ui-run-1")
        comp = _Comp()
        busy = {"window": _Window()}
        with patch(
            "resolve_node_kit.fusion.arrange_request.bind_target",
            return_value=comp,
        ), patch(
            "resolve_node_kit.fusion.arrange_request.show_busy_window",
            return_value=busy,
        ), patch(
            "resolve_node_kit.fusion.arrange_request.hide_busy_window",
            return_value=True,
        ), patch(
            "resolve_node_kit.fusion.arrange_request.set_busy_text",
        ), patch(
            "resolve_node_kit.fusion.arrange_request.arrange_comp",
            return_value={
                "node_count": 1,
                "edge_count": 0,
                "moved_count": 0,
                "arranged_count": 1,
                "diagnostics": {},
                "stage_timings_ms": {},
            },
        ):
            result = execute_arrange_request(
                None,
                None,
                None,
                ArrangeDialogState(True, False),
                show_result_dialog=False,
                ui_session=session,
            )

        self.assertEqual(result.status, "success")
        self.assertEqual(result.run_id, "ui-run-1")
        self.assertEqual(result.ui_state, "terminal")
        events = [item["event"] for item in result.ui_events]
        self.assertLess(events.index("busy_shown"), events.index("busy_hidden"))
        self.assertLess(events.index("busy_hidden"), events.index("result_shown"))
        self.assertEqual(events[-1], "terminal")
        self.assertTrue(all(item["run_id"] == "ui-run-1" for item in result.ui_events))


if __name__ == "__main__":
    unittest.main()
