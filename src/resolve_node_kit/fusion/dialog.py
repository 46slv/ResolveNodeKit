"""Arrange dialog invocation helper (host-independent logic).

Measured on Resolve Studio 21.0.3.7: `comp.AskUser` never raises for a bad
controls shape; it returns None, which is indistinguishable from the user
pressing Cancel. This helper therefore tries the known wire shapes in order
and treats None as ambiguous: move to the next shape, and only conclude
Cancel after every shape returns None. Each attempt is reported through the
optional logger so silent rejections stay debuggable.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import uuid
from typing import Any, Callable


WHOLE_COMP_MESSAGE = "現在のFusionコンポジション全体を整列します。"


@dataclass
class ArrangeUiSession:
    """Small host-independent observability seam for one UI-owned run.

    The session does not drive Resolve or claim OS accessibility.  It only
    provides an explicit ``run_id`` and a monotonic event/state stream that a
    UI shell or focused test can observe.  Cancellation is deliberately
    accepted only before the production controller starts; an in-flight host
    mutation must use the controller's rollback boundary instead of a second
    thread or an unsafe interrupt.
    """

    run_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    state: str = "setup"
    events: list[dict[str, Any]] = field(default_factory=list)
    cancel_requested: bool = False

    def __post_init__(self) -> None:
        self.emit("setup")

    def emit(self, event: str, **detail: Any) -> dict[str, Any]:
        item = {"run_id": self.run_id, "event": str(event), **detail}
        self.events.append(item)
        return item

    def begin(self) -> bool:
        if self.state != "setup" or self.cancel_requested:
            return False
        self.state = "running"
        self.emit("started")
        return True

    def cancel(self) -> bool:
        if self.state != "setup":
            self.emit("cancel_rejected", state=self.state)
            return False
        self.cancel_requested = True
        self.state = "cancelled"
        self.emit("cancelled")
        return True

    def terminal(self, status: str) -> None:
        self.state = "terminal"
        self.emit("terminal", status=str(status))

    def snapshot(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "state": self.state,
            "cancel_requested": self.cancel_requested,
            "events": [dict(item) for item in self.events],
        }


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


def ask_arrange_confirmation(
    ask: Callable[..., Any],
    title: str,
    message: str = WHOLE_COMP_MESSAGE,
    log: Callable[[str], None] | None = None,
) -> Any:
    """Show the minimal FIRST_USABLE whole-comp confirmation dialog.

    The old two-checkbox wire remains in :func:`ask_arrange_options` for the
    selection-only/experimental lane.  Production Arrange deliberately uses a
    text-only confirmation so the only supported request is the safe default:
    whole active composition, preserve Groups.  Resolve supplies the modal
    confirmation buttons for this AskUser shape; ``None``/``False`` remains
    Cancel or an unsupported host shape.
    """
    from .semantic import ArrangeDialogState

    def note(item: str) -> None:
        if log is not None:
            try:
                log(item)
            except Exception:
                pass

    shapes = [
        [["Scope", "Text", {"Default": message, "Lines": 2, "Wrap": True}]],
        {1: {1: "Scope", 2: "Text", 3: {"Default": message, "Lines": 2, "Wrap": True}}},
    ]
    for index, controls in enumerate(shapes):
        try:
            result = ask(title, controls)
        except Exception as exc:
            note(f"confirmation attempt {index + 1}/{len(shapes)} raised {exc!r}")
            continue
        if result is None or result is False:
            note(f"confirmation attempt {index + 1}/{len(shapes)} returned None (Cancel or rejected)")
            continue
        note(f"confirmation attempt {index + 1}/{len(shapes)} accepted")
        return ArrangeDialogState(include_unselected=True, ungroup=False)
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
        pumped = _pump_display(disp)
        note("busy shown pumped=" + str(pumped))
        return {"disp": disp, "window": window}
    except Exception as exc:
        note(f"busy unavailable: {exc!r}")
        return None


def _pump_display(disp):
    """Best-effort host-safe event pump; never blocks, never raises."""
    if disp is None:
        return False
    for method in ("ProcessEvents", "Step"):
        try:
            action = getattr(disp, method, None)
            if callable(action):
                action()
                return True
        except Exception:
            continue
    return False


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
            _pump_display(handle.get("disp"))
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
        return False
    try:
        hider = getattr(handle.get("window"), "Hide", None)
        if callable(hider):
            hider()
            if log is not None:
                log("busy hidden")
            return True
    except Exception:
        return False
    return False


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


class TargetMismatch(RuntimeError):
    pass


def _identity_text(handle):
    try:
        describe = getattr(handle, "GetAttrs", lambda: {})()
        name = ""
        if isinstance(describe, dict):
            for key in ("COMPS_Name", "COMPN_Name", "TOOLS_Name", "Name"):
                value = describe.get(key)
                if value:
                    name = str(value)
                    break
        if not name:
            for attr in ("Name",):
                value = getattr(handle, attr, None)
                if value and not callable(value):
                    name = str(value)
                    break
    except Exception:
        name = ""
    try:
        tool_list = handle.GetToolList()
        if isinstance(tool_list, dict):
            count = len(tool_list)
        else:
            count = len(list(tool_list))
    except Exception:
        count = -1
    return name, count


def bind_target(comp=None, fusion=None, resolve=None, log=None, require_live=False):
    """Bind the live Fusion current comp with fail-closed mismatch handling."""
    def note(message):
        if log is not None:
            try:
                log(message)
            except Exception:
                pass

    live = None
    if fusion is not None:
        try:
            getter = getattr(fusion, "GetCurrentComp", None)
            live = getter() if callable(getter) else None
        except Exception:
            live = None
    if live is None and resolve is not None:
        try:
            live = resolve.Fusion().GetCurrentComp()
        except Exception:
            live = None
    if live is not None and comp is not None and live is not comp:
        live_name, live_count = _identity_text(live)
        comp_name, comp_count = _identity_text(comp)
        note(f"target live comp={live_name} tools={live_count} global comp={comp_name} tools={comp_count}")
        comparable = bool(live_name) and bool(comp_name)
        if not comparable:
            raise TargetMismatch(
                f"cannot prove global comp matches live current "
                f"(live comp={live_name} tools={live_count}, "
                f"global comp={comp_name} tools={comp_count})"
            )
        if live_name != comp_name or (live_count >= 0 and comp_count >= 0 and live_count != comp_count):
            raise TargetMismatch(
                f"global comp differs from live current "
                f"(live comp={live_name} tools={live_count}, "
                f"global comp={comp_name} tools={comp_count})"
            )
        note("target match; live current adopted")
        return live
    if live is None and require_live:
        comp_name, comp_count = _identity_text(comp) if comp is not None else ("", -1)
        note("target unproven: no live current (global comp=" + comp_name + " tools=" + str(comp_count) + ")")
        raise TargetMismatch("live current unavailable; refusing interactive write without proven target")
    if live is not None:
        live_name, live_count = _identity_text(live)
        note(f"target live comp={live_name} tools={live_count}")
        return live
    if comp is not None:
        comp_name, comp_count = _identity_text(comp)
        note(f"target global comp={comp_name} tools={comp_count} (no live current)")
        return comp
    return None
