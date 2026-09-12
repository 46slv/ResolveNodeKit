"""Shared production seam for a single Arrange execution.

The Resolve AskUser dialog is only a transport for options.  Once an
``ArrangeDialogState`` exists, both the interactive script and an automated
host verifier enter this module.  Keeping the target bind, busy lifecycle,
semantic mutation, and result presentation here prevents a verifier from
silently exercising a second Arrange implementation.
"""
from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Any, Callable

from .dialog import (
    ArrangeUiSession,
    BUSY_INITIAL_TEXT,
    TargetMismatch,
    bind_target,
    hide_busy_window,
    set_busy_text,
    show_busy_window,
    show_result,
    stage_text,
)
from .semantic import ArrangeDialogState, arrange_comp
from .tidy import FusionHostError


@dataclass(frozen=True)
class ArrangeExecutionResult:
    """Stable, JSON-friendly summary of one production Arrange request."""

    status: str
    exit_code: int
    message: str = ""
    result: dict[str, Any] | None = None
    target_name: str = ""
    target_tools: int = -1
    busy_shown: bool = False
    busy_hidden: bool = False
    result_shown: bool = False
    error: str = ""
    run_id: str = ""
    ui_state: str = ""
    ui_events: tuple[dict[str, Any], ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "exit_code": self.exit_code,
            "message": self.message,
            "result": self.result,
            "target_name": self.target_name,
            "target_tools": self.target_tools,
            "busy_shown": self.busy_shown,
            "busy_hidden": self.busy_hidden,
            "result_shown": self.result_shown,
            "error": self.error,
            "run_id": self.run_id,
            "ui_state": self.ui_state,
            "ui_events": [dict(item) for item in self.ui_events],
        }


def _note(log: Callable[[str], None] | None, message: str) -> None:
    if log is None:
        return
    try:
        log(message)
    except Exception:
        pass


def _identity(handle: Any) -> tuple[str, int]:
    try:
        attrs = getattr(handle, "GetAttrs", lambda: {})()
    except Exception:
        attrs = {}
    name = ""
    if isinstance(attrs, dict):
        for key in ("COMPS_Name", "COMPN_Name", "Name"):
            if attrs.get(key):
                name = str(attrs[key])
                break
    if not name:
        try:
            value = getattr(handle, "Name", None)
            if value and not callable(value):
                name = str(value)
        except Exception:
            pass
    try:
        tools = handle.GetToolList()
        count = len(tools) if isinstance(tools, dict) else len(list(tools))
    except Exception:
        count = -1
    return name, count


def _fusion_handle(fusion: Any, resolve: Any) -> Any:
    if fusion is not None:
        return fusion
    if resolve is not None:
        try:
            return resolve.Fusion()
        except Exception:
            pass
    return None


def _message_for_result(result: dict[str, Any]) -> str:
    diagnostics = result.get("diagnostics", {}) if isinstance(result, dict) else {}
    summary = (
        "[ResolveNodeKit] Arrange: nodes=%s edges=%s moved=%s arranged=%s "
        "avoidable_diagonals=%s expanded_gaps=%s"
        % (
            result.get("node_count"),
            result.get("edge_count"),
            result.get("moved_count"),
            result.get("arranged_count"),
            diagnostics.get("avoidable_diagonal_edge_count"),
            diagnostics.get("expanded_gap_count"),
        )
    )
    if result.get("moved_count"):
        return "整列しました。" + summary
    return "すでに整列済みのため、移動はありませんでした。" + summary


def execute_arrange_request(
    ui_comp: Any,
    fusion: Any,
    resolve: Any,
    state: ArrangeDialogState,
    *,
    result_ask: Callable[..., Any] | None = None,
    title: str = "ResolveNodeKit - Arrange",
    log: Callable[[str], None] | None = None,
    show_result_dialog: bool = True,
    ungroup_primitive: Any = None,
    ui_session: ArrangeUiSession | None = None,
) -> ArrangeExecutionResult:
    """Execute one Arrange request through the production mutation path.

    ``ui_comp`` is the composition that owns the menu/dialog invocation.  It
    is never used as the mutation target until ``bind_target(...,
    require_live=True)`` proves the live current composition identity.
    """
    if not isinstance(state, ArrangeDialogState):
        raise TypeError("state must be ArrangeDialogState")

    session = ui_session or ArrangeUiSession()
    if not session.begin():
        # A setup Cancel is a complete, zero-mutation request.  Keep this
        # return path visible to the UI shell without binding a host target.
        return ArrangeExecutionResult(
            status="cancelled",
            exit_code=0,
            message="整列をキャンセルしました。変更はありません。",
            run_id=session.run_id,
            ui_state=session.state,
            ui_events=tuple(dict(item) for item in session.events),
        )

    live_target = None
    busy = None
    busy_shown = False
    busy_hidden = False
    result_shown = False
    bind_started = time.perf_counter()

    def present(message: str) -> None:
        nonlocal result_shown
        if not show_result_dialog:
            return
        try:
            result_shown = bool(
                show_result(
                    result_ask,
                    title,
                    message,
                    log=lambda item: _note(log, "result " + str(item)),
                )
            )
        except Exception as exc:
            _note(log, "result presentation failed " + repr(exc))

    try:
        try:
            live_target = bind_target(
                ui_comp,
                fusion,
                resolve,
                log=lambda item: _note(log, "target " + str(item)),
                require_live=True,
            )
        except TargetMismatch as exc:
            message = "整列できませんでした。中止し、変更はありません。\n" + str(exc)
            _note(log, "target mismatch " + str(exc))
            present(message)
            session.terminal("target_mismatch")
            return ArrangeExecutionResult(
                status="target_mismatch",
                exit_code=5,
                message=message,
                result=None,
                result_shown=result_shown,
                error=str(exc),
                run_id=session.run_id,
                ui_state=session.state,
                ui_events=tuple(dict(item) for item in session.events),
            )

        if live_target is None:
            message = "整列できませんでした。アクティブな Fusion composition がありません。"
            _note(log, "no active composition")
            present(message)
            session.terminal("no_comp")
            return ArrangeExecutionResult(
                status="no_comp",
                exit_code=2,
                message=message,
                result_shown=result_shown,
                run_id=session.run_id,
                ui_state=session.state,
                ui_events=tuple(dict(item) for item in session.events),
            )

        target_name, target_tools = _identity(live_target)
        bind_ms = round((time.perf_counter() - bind_started) * 1000.0, 1)
        _note(log, "target comp=" + target_name + " tools=" + str(target_tools))
        busy = show_busy_window(
            _fusion_handle(fusion, resolve),
            title,
            BUSY_INITIAL_TEXT,
            log=lambda item: _note(log, "busy " + str(item)),
        )
        busy_shown = bool(busy)
        session.emit("busy_shown", visible=busy_shown)

        def on_progress(phase: str) -> None:
            _note(log, "arrange " + str(phase))
            session.emit("progress", phase=str(phase))
            try:
                set_busy_text(busy, stage_text(phase))
            except Exception:
                pass

        try:
            arrange_result = arrange_comp(
                live_target,
                include_unselected=state.include_unselected,
                ungroup=state.ungroup,
                ungroup_primitive=ungroup_primitive,
                progress=on_progress,
            )
        except FusionHostError as exc:
            message = "整列できませんでした。中止し、変更はありません。\n" + str(exc)
            _note(log, "refused " + str(exc))
            status = "refused"
            exit_code = 3
            error = str(exc)
            arrange_result = None
        except Exception as exc:
            message = "整列に失敗しました。変更を確認してください。\n" + repr(exc)
            _note(log, "failed " + repr(exc))
            status = "failed"
            exit_code = 1
            error = repr(exc)
            arrange_result = None
        else:
            arrange_result = dict(arrange_result)
            stage_timings = dict(arrange_result.get("stage_timings_ms", {}))
            stage_timings["bind"] = bind_ms
            arrange_result["stage_timings_ms"] = stage_timings
            message = _message_for_result(arrange_result)
            _note(log, "ok " + message)
            status = "success"
            exit_code = 0
            error = ""
        finally:
            if busy is not None:
                try:
                    busy_hidden = bool(hide_busy_window(
                        busy,
                        log=lambda item: _note(log, "busy " + str(item)),
                    ))
                except Exception as exc:
                    _note(log, "busy hide failed " + repr(exc))
                session.emit("busy_hidden", visible=not busy_hidden)

        present(message)
        session.emit("result_shown", visible=result_shown)
        session.terminal(status)
        return ArrangeExecutionResult(
            status=status,
            exit_code=exit_code,
            message=message,
            result=arrange_result,
            target_name=target_name,
            target_tools=target_tools,
            busy_shown=busy_shown,
            busy_hidden=busy_hidden,
            result_shown=result_shown,
            error=error,
            run_id=session.run_id,
            ui_state=session.state,
            ui_events=tuple(dict(item) for item in session.events),
        )
    except Exception as exc:
        # The seam must still close a busy window before exposing a failure.
        if busy is not None and not busy_hidden:
            try:
                busy_hidden = bool(hide_busy_window(
                    busy,
                    log=lambda item: _note(log, "busy " + str(item)),
                ))
            except Exception:
                pass
            session.emit("busy_hidden", visible=not busy_hidden)
        message = "整列に失敗しました。変更を確認してください。\n" + repr(exc)
        _note(log, "handler failed " + repr(exc))
        present(message)
        session.emit("result_shown", visible=result_shown)
        session.terminal("failed")
        return ArrangeExecutionResult(
            status="failed",
            exit_code=1,
            message=message,
            busy_shown=busy_shown,
            busy_hidden=busy_hidden,
            result_shown=result_shown,
            error=repr(exc),
            run_id=session.run_id,
            ui_state=session.state,
            ui_events=tuple(dict(item) for item in session.events),
        )
