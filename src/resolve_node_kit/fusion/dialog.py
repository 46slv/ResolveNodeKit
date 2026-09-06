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
