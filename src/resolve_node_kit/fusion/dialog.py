"""Arrange dialog invocation helper (host-independent logic).

Measured on Resolve Studio 21.0.3.7: `comp.AskUser` never raises for a bad
controls shape; it returns None, which is indistinguishable from the user
pressing Cancel. This helper therefore tries the known wire shapes in order
and treats None as ambiguous: move to the next shape, and only conclude
Cancel after every shape returns None. Each attempt is reported through the
optional logger so silent rejections stay debuggable.
"""
from __future__ import annotations

from typing import Any, Callable


def _map_result(result: Any, include_label: str, ungroup_label: str) -> dict[str, Any]:
    from .semantic import ArrangeDialogState

    if not isinstance(result, dict):
        raise ValueError(f"unexpected dialog result: {result!r}")
    return {
        "IncludeUnselected": result.get("IncludeUnselected", result.get(include_label, 0)),
        "UngroupFirst": result.get("UngroupFirst", result.get(ungroup_label, 0)),
    }


def ask_arrange_options(
    ask: Callable[..., Any],
    title: str,
    include_label: str,
    ungroup_label: str,
    log: Callable[[str], None] | None = None,
) -> Any:
    """Run the two-checkbox Arrange dialog; None means Cancel (or rejection)."""
    from .semantic import ArrangeDialogState

    def note(message: str) -> None:
        if log is not None:
            try:
                log(message)
            except Exception:
                pass

    shapes = [
        [
            [include_label, "Checkbox", {"Default": 0}],
            [ungroup_label, "Checkbox", {"Default": 0}],
        ],
        {
            1: {1: include_label, 2: "Checkbox", 3: {"Default": 0}},
            2: {1: ungroup_label, 2: "Checkbox", 3: {"Default": 0}},
        },
    ]
    for index, controls in enumerate(shapes):
        try:
            result = ask(title, controls)
        except Exception as exc:
            note(f"dialog attempt {index + 1}/{len(shapes)} raised {exc!r}")
            continue
        if result is None:
            note(f"dialog attempt {index + 1}/{len(shapes)} returned None (rejected or Cancel)")
            continue
        note(f"dialog attempt {index + 1}/{len(shapes)} returned keys {sorted(result) if isinstance(result, dict) else type(result)}")
        try:
            return ArrangeDialogState.from_askuser(_map_result(result, include_label, ungroup_label))
        except ValueError as exc:
            note(f"dialog attempt {index + 1}/{len(shapes)} parse failed: {exc!r}")
            continue
    return None


STAGE_TEXTS = {
    "snapshot": "読み取り中…",
    "plan": "配置を計算中…",
    "writes": "整列を適用中…",
    "readback": "確認中…",
    "verify": "確認中…",
}

BUSY_TITLE = "ResolveNodeKit - Arrange"
BUSY_INITIAL_TEXT = "整列しています…"


def stage_text(phase):
    for key, text in STAGE_TEXTS.items():
        if key in str(phase):
            return text
    return BUSY_INITIAL_TEXT


def show_busy_window(fusion_obj, title=BUSY_TITLE, text=BUSY_INITIAL_TEXT, log=None):
    """Best-effort modeless busy window; always returns a handle or None."""
    def note(message):
        if log is not None:
            try:
                log(message)
            except Exception:
                pass

    try:
        ui = getattr(fusion_obj, "UIManager", None)
        if ui is None:
            note("busy unavailable: no UIManager")
            return None
        dispatcher_cls = getattr(fusion_obj, "UIDispatcher", None)
        if dispatcher_cls is None:
            import __main__ as host_main
            dispatcher_cls = getattr(host_main, "bmd", None)
            dispatcher_cls = getattr(dispatcher_cls, "UIDispatcher", None) if dispatcher_cls is not None else None
        if dispatcher_cls is None:
            note("busy unavailable: no UIDispatcher")
            return None
        disp = dispatcher_cls(ui)
        label = ui.Label({"ID": "RNKBusyText", "Text": text})
        window = disp.AddWindow(
            {"WindowTitle": title, "ID": "RNKBusyWindow"},
            [ui.VGroup([label])],
        )
        show = getattr(window, "Show", None)
        if not callable(show):
            note("busy unavailable: window has no Show")
            return None
        show()
        note("busy shown")
        return {"disp": disp, "window": window}
    except Exception as exc:
        note(f"busy unavailable: {exc!r}")
        return None


def set_busy_text(handle, text, log=None):
    if not handle:
        return False
    try:
        window = handle.get("window")
        finder = getattr(window, "Find", None)
        if not callable(finder):
            return False
        label = finder("RNKBusyText")
        setter = getattr(label, "SetText", None)
        if callable(setter):
            setter(text)
            return True
        try:
            label.Text = text
            return True
        except Exception:
            return False
    except Exception:
        return False


def hide_busy_window(handle, log=None):
    if not handle:
        return
    try:
        hider = getattr(handle.get("window"), "Hide", None)
        if callable(hider):
            hider()
        if log is not None:
            log("busy hidden")
    except Exception:
        pass


def show_result(ask, title, message, log=None):
    """Visible result/error dialog; True when something was displayed."""
    def note(text):
        if log is not None:
            try:
                log(text)
            except Exception:
                pass

    if not callable(ask):
        note("result unavailable: no AskUser")
        return False
    shapes = [
        [["Result", "Text", {"Default": message, "Lines": 6, "Wrap": True}]],
        {"1": {"1": "Result", "2": "Text", "3": {"Default": message, "Lines": 6}}},
    ]
    for index, controls in enumerate(shapes):
        try:
            ask(title, controls)
            note(f"result shown via shape {index + 1}")
            return True
        except Exception as exc:
            note(f"result shape {index + 1} raised {exc!r}")
            continue
    note("result unavailable: all shapes failed")
    return False
