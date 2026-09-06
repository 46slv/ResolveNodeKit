from __future__ import annotations

import math
from collections import OrderedDict  # noqa: F401  (see _ensure_ordered_dict)
import builtins
from dataclasses import dataclass
from typing import Any

from resolve_node_kit.core.layout import Edge, LayoutConfig, LayoutError, layout_graph


def _ensure_ordered_dict() -> None:
    """Fusion's SaveSettings bridge evals ``OrderedDict(...)`` on deserialize.

    Measured on Studio 21.0.3.7: without ``OrderedDict`` in builtins the call
    still succeeds but ``Tools`` comes back as ``None`` (plus console spam).
    Ensuring it here keeps group-state handling fail-closed instead of silent.
    """
    if not hasattr(builtins, "OrderedDict"):
        builtins.OrderedDict = OrderedDict  # type: ignore[attr-defined]


_ensure_ordered_dict()

# Host-measured FlowView grid (Studio 21.0.3.7, GridSnap on):
# X snaps to 0.5, Y snaps to whole numbers. Most tools read back with a stable
# +0.009 Y offset; mask/operator tools (e.g. EllipseMask +0.073/+0.054) carry a
# larger per-type frame offset. Snapping desired positions to that grid keeps
# readback verification and second-run idempotence meaningful; tolerance covers
# the largest measured frame offset but still fails closed on real grid snaps
# (which differ by >=0.2).
FLOW_GRID_X = 0.5
FLOW_GRID_Y = 1.0
FLOW_POSITION_TOLERANCE = 0.1


class FusionHostError(RuntimeError):
    pass


@dataclass(frozen=True)
class TidyResult:
    node_count: int
    edge_count: int
    moved_count: int
    anchor: tuple[float, float]


def _iter_values(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, dict):
        return list(value.values())
    values = getattr(value, "values", None)
    if callable(values):
        try:
            return list(values())
        except Exception:
            pass
    if isinstance(value, (list, tuple)):
        return list(value)
    try:
        return list(value)
    except Exception:
        return []


def _call_list(obj, method):
    """Call a host list getter tolerantly: missing, None, or non-callable yields []."""
    getter = getattr(obj, method, None)
    if not callable(getter):
        return []
    try:
        return _iter_values(getter())
    except Exception:
        return []


def _attrs(obj: Any) -> dict[str, Any]:
    getter = getattr(obj, "GetAttrs", None)
    if not callable(getter):
        return {}
    try:
        value = getter()
        return value if isinstance(value, dict) else dict(value or {})
    except Exception:
        return {}


def _tool_name(tool: Any) -> str:
    name = getattr(tool, "Name", None)
    if name:
        return str(name)
    name = _attrs(tool).get("TOOLS_Name")
    if not name:
        raise FusionHostError("Fusion tool has no stable name")
    return str(name)


def _xy_from_pos_table(table: Any) -> tuple[float, float]:
    if table is None:
        raise FusionHostError("FlowView.GetPosTable returned no position")
    if isinstance(table, dict):
        numeric = [(key, value) for key, value in table.items() if isinstance(key, (int, float))]
        if numeric:
            numeric.sort(key=lambda item: float(item[0]))
            values = [item[1] for item in numeric]
        else:
            values = list(table.values())
    else:
        values_method = getattr(table, "values", None)
        values = list(values_method()) if callable(values_method) else list(table)
    if len(values) < 2:
        raise FusionHostError(f"unexpected FlowView position table: {table!r}")
    return float(values[0]), float(values[1])


def _classify_input(input_obj: Any) -> str:
    attrs = _attrs(input_obj)
    input_id = str(attrs.get("INPS_ID", "")).lower()
    input_name = str(attrs.get("INPN_Name", attrs.get("INPS_Name", ""))).lower()
    text = f"{input_id} {input_name}"
    if "mask" in text:
        return "mask"
    if "background" in text or input_id in {"input", "imageinput"}:
        return "background"
    if "foreground" in text:
        return "foreground"
    return "other"


def _snapshot(comp: Any, flow: Any) -> tuple[dict[str, Any], dict[str, tuple[float, float]], list[Edge]]:
    tools = {_tool_name(tool): tool for tool in _call_list(comp, "GetToolList")}
    if not tools:
        return {}, {}, []
    positions = {name: _xy_from_pos_table(flow.GetPosTable(tools[name])) for name in sorted(tools)}
    edges: list[Edge] = []
    for target_name in sorted(tools):
        target = tools[target_name]
        for input_obj in _call_list(target, "GetInputList"):
            get_connected = getattr(input_obj, "GetConnectedOutput", None)
            if not callable(get_connected):
                continue
            output = get_connected()
            get_tool = getattr(output, "GetTool", None) if output is not None else None
            if not callable(get_tool):
                continue
            source_tool = get_tool()
            if source_tool is None:
                continue
            source_name = _tool_name(source_tool)
            if source_name in tools:
                edges.append(Edge(source_name, target_name, _classify_input(input_obj)))
    return tools, positions, edges


def _snap_position(x: float, y: float) -> tuple[float, float]:
    # Ties snap down on the measured host (1.50 -> 1.009, 1.51 -> 2.009),
    # so use floor-half-down rather than banker's round().
    snapped_x = math.floor(float(x) / FLOW_GRID_X + 0.5 - 1e-9) * FLOW_GRID_X
    snapped_y = math.floor(float(y) / FLOW_GRID_Y + 0.5 - 1e-9) * FLOW_GRID_Y
    # Avoid -0.0 noise in readback comparisons.
    if snapped_x == 0:
        snapped_x = 0.0
    if snapped_y == 0:
        snapped_y = 0.0
    return snapped_x, snapped_y


def _close_enough(a: tuple[float, float], b: tuple[float, float], epsilon: float = FLOW_POSITION_TOLERANCE) -> bool:
    return abs(a[0] - b[0]) <= epsilon and abs(a[1] - b[1]) <= epsilon


def _restore(flow: Any, tools: dict[str, Any], original: dict[str, tuple[float, float]]) -> list[str]:
    failures: list[str] = []
    for name in sorted(original):
        try:
            x, y = original[name]
            flow.SetPos(tools[name], x, y)
            readback = _xy_from_pos_table(flow.GetPosTable(tools[name]))
            if not _close_enough(readback, (x, y)):
                failures.append(name)
        except Exception:
            failures.append(name)
    return failures


def tidy_comp(comp: Any, config: LayoutConfig | None = None) -> TidyResult:
    frame = getattr(comp, "CurrentFrame", None)
    flow = getattr(frame, "FlowView", None) if frame is not None else None
    if flow is None:
        raise FusionHostError("current Fusion FlowView is unavailable")
    if not callable(getattr(flow, "GetPosTable", None)) or not callable(getattr(flow, "SetPos", None)):
        raise FusionHostError("required FlowView position API is unavailable")
    tools, original, edges = _snapshot(comp, flow)
    if not tools:
        return TidyResult(0, 0, 0, (0.0, 0.0))
    relative = layout_graph(tools.keys(), edges, original_positions=original, config=config)
    anchor_x = min(x for x, _ in original.values())
    anchor_y = min(y for _, y in original.values())
    desired = {
        name: _snap_position(anchor_x + xy[0], anchor_y + xy[1])
        for name, xy in relative.items()
    }
    writes = {name: xy for name, xy in desired.items() if not _close_enough(original[name], xy)}
    if not writes:
        return TidyResult(len(tools), len(edges), 0, (anchor_x, anchor_y))
    start_undo = getattr(comp, "StartUndo", None)
    end_undo = getattr(comp, "EndUndo", None)
    undo_started = False
    if callable(start_undo) and callable(end_undo):
        start_undo("ResolveNodeKit: Tidy Graph")
        undo_started = True
    try:
        for name in sorted(writes):
            flow.SetPos(tools[name], *writes[name])
        mismatched = [name for name in sorted(writes) if not _close_enough(_xy_from_pos_table(flow.GetPosTable(tools[name])), desired[name])]
        if mismatched:
            raise FusionHostError(f"position readback mismatch: {', '.join(mismatched[:12])}")
    except Exception as exc:
        restore_failures = _restore(flow, tools, original)
        if undo_started:
            end_undo(False)
        if restore_failures:
            raise FusionHostError(f"tidy failed and rollback was incomplete for: {', '.join(restore_failures[:12])}") from exc
        if isinstance(exc, (FusionHostError, LayoutError)):
            raise
        raise FusionHostError(f"tidy failed; original positions restored: {exc}") from exc
    else:
        if undo_started:
            end_undo(True)
    return TidyResult(len(tools), len(edges), len(writes), (anchor_x, anchor_y))
