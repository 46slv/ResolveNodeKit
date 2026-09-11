"""Fail-closed host application seam for a validated strict plan.

``strict_request`` intentionally stops after pure snapshot/plan validation.
This module is the small adapter boundary that may follow it on a qualified
Fusion host.  It owns only position writes: the caller supplies the exact live
tool handles captured with the snapshot, and a post-write snapshot reader must
prove that processing state did not change.  No graph, settings, media, or
project-save surface is touched here.

The planner exposes both global placements and per-scope placements.  Fusion
GroupOperator FlowViews are scope-local, so this adapter derives one host
origin per scope from a canonical pre-state anchor instead of applying global
coordinates blindly to nested children.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Any, Callable, Mapping

from .host_snapshot import build_host_processing_snapshot
from .processing_snapshot import ProcessingSnapshot, SnapshotState
from .strict_planner import GridPoint
from .strict_request import StrictPreparation, StrictPreparationError, prepare_strict_plan
from .tidy import (
    FLOW_GRID_X,
    FLOW_GRID_Y,
    FLOW_POSITION_TOLERANCE,
    _close_enough,
    _restore_positions_batch,
    _xy_from_pos_table,
)


class StrictHostApplyError(RuntimeError):
    """Raised when a strict host write cannot be proven safe."""


@dataclass(frozen=True, slots=True)
class FlowViewCalibration:
    """Measured logical-cell to FlowView mapping.

    The defaults are the measured Fusion grid values used by the existing
    tidy adapter.  A future host qualification may supply a different
    calibration, but it must be explicit rather than inferred from a failed
    readback.
    """

    # Logical cell scale and host snap quantum are separate.  The planner's
    # default pitch is expressed in logical cells; the measured host merely
    # constrains the final write lattice (X=0.5, Y=1.0).
    cell_x: float = 1.0
    cell_y: float = 1.0
    snap_x: float = FLOW_GRID_X
    snap_y: float = FLOW_GRID_Y
    tolerance: float = FLOW_POSITION_TOLERANCE

    def __post_init__(self) -> None:
        for name in ("cell_x", "cell_y", "snap_x", "snap_y", "tolerance"):
            value = getattr(self, name)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(float(value)):
                raise StrictHostApplyError(f"{name} must be a finite number")
            if float(value) <= 0:
                raise StrictHostApplyError(f"{name} must be positive")

    @staticmethod
    def _snap(value: float, step: float) -> float:
        snapped = math.floor(float(value) / float(step) + 0.5 - 1e-9) * float(step)
        return 0.0 if snapped == 0 else snapped

    def snap_origin(self, x: float, y: float) -> tuple[float, float]:
        return self._snap(x, self.snap_x), self._snap(y, self.snap_y)

    def host_position(self, point: GridPoint, origin: tuple[float, float]) -> tuple[float, float]:
        return self._snap(origin[0] + point.column * self.cell_x, self.snap_x), self._snap(
            origin[1] + point.row * self.cell_y, self.snap_y
        )


@dataclass(frozen=True, slots=True)
class StrictRunResult:
    """Compact evidence for one bounded strict preserve run."""

    moved_count: int
    desired_positions: Mapping[str, tuple[float, float]]
    readback_positions: Mapping[str, tuple[float, float]]
    scope_origins: Mapping[str | None, tuple[float, float]]
    processing_unchanged: bool
    pre_signature: str
    post_signature: str
    handle_names: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        def scope_key(scope: str | None) -> str:
            return "<root>" if scope is None else str(scope)

        return {
            "moved_count": self.moved_count,
            "desired_positions": {
                name: [float(value[0]), float(value[1])] for name, value in sorted(self.desired_positions.items())
            },
            "readback_positions": {
                name: [float(value[0]), float(value[1])] for name, value in sorted(self.readback_positions.items())
            },
            "scope_origins": {
                scope_key(scope): [float(value[0]), float(value[1])]
                for scope, value in sorted(self.scope_origins.items(), key=lambda item: scope_key(item[0]))
            },
            "processing_unchanged": self.processing_unchanged,
            "pre_signature": self.pre_signature,
            "post_signature": self.post_signature,
            "handle_names": list(self.handle_names),
        }


@dataclass(frozen=True, slots=True)
class StrictPreserveResult:
    """Evidence for run1/run2 strict preserve qualification."""

    run1: StrictRunResult
    run2: StrictRunResult
    stable: bool

    def as_dict(self) -> dict[str, Any]:
        return {"run1": self.run1.as_dict(), "run2": self.run2.as_dict(), "stable": self.stable}


SnapshotReader = Callable[..., ProcessingSnapshot]


def _field_value(field: Any, *, path: str) -> Any:
    state = getattr(field, "state", None)
    if state is not None and state is not SnapshotState.COMPLETE and str(getattr(state, "value", state)) != "complete":
        raise StrictHostApplyError(f"{path} is not complete: {state}")
    value = getattr(field, "value", field)
    if value is None:
        raise StrictHostApplyError(f"{path} has no value")
    return value


def _processing_positions(preparation: StrictPreparation) -> dict[str, tuple[float, float]]:
    result: dict[str, tuple[float, float]] = {}
    for uid, node in sorted(preparation.processing.nodes.items()):
        raw = _field_value(node.position, path=f"nodes.{uid}.position")
        if not isinstance(raw, (list, tuple)) or len(raw) < 2:
            raise StrictHostApplyError(f"nodes.{uid}.position is not an x/y pair")
        try:
            result[uid] = (float(raw[0]), float(raw[1]))
        except (TypeError, ValueError) as exc:
            raise StrictHostApplyError(f"nodes.{uid}.position is not numeric") from exc
    return result


def _signature(snapshot: ProcessingSnapshot) -> str:
    """Hash all processing evidence except position values and source label."""

    payload = snapshot.as_dict()
    payload.pop("source", None)
    for node in payload.get("nodes", {}).values():
        if isinstance(node, dict):
            node.pop("position", None)
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _flow_for(comp: Any, flow: Any | None) -> Any:
    if flow is not None:
        return flow
    frame = getattr(comp, "CurrentFrame", None)
    resolved = getattr(frame, "FlowView", None) if frame is not None else None
    if resolved is None:
        raise StrictHostApplyError("Fusion CurrentFrame.FlowView is unavailable")
    return resolved


def _read_positions(flow: Any, tools: Mapping[str, Any]) -> dict[str, tuple[float, float]]:
    getter = getattr(flow, "GetPosTable", None)
    if not callable(getter):
        raise StrictHostApplyError("FlowView.GetPosTable is unavailable")
    result: dict[str, tuple[float, float]] = {}
    for name in sorted(tools):
        try:
            result[name] = _xy_from_pos_table(getter(tools[name]))
        except Exception as exc:
            raise StrictHostApplyError(f"position readback failed for {name!r}: {exc}") from exc
    return result


def _scope_members(preparation: StrictPreparation) -> dict[str | None, tuple[str, ...]]:
    members: dict[str | None, list[str]] = {}
    for node in preparation.strict.nodes:
        members.setdefault(node.parent_uid, []).append(node.uid)
    return {scope: tuple(sorted(values)) for scope, values in members.items()}


def _scope_anchor(preparation: StrictPreparation, scope: str | None, members: tuple[str, ...]) -> str:
    for module in preparation.plan.modules:
        if module.scope == scope and module.kind == "rail":
            for member in module.members:
                if member in members:
                    return member
    return members[0]


def map_strict_plan_to_host(
    preparation: StrictPreparation,
    *,
    calibration: FlowViewCalibration | None = None,
) -> tuple[dict[str, tuple[float, float]], dict[str | None, tuple[float, float]]]:
    """Map validated per-scope logical placements onto host coordinates.

    Origins are derived from the pre-state anchor in each FlowView scope.  A
    missing local scope map or position refuses before any host write.
    """

    calibration = calibration or FlowViewCalibration()
    plan = preparation.plan
    pre_positions = _processing_positions(preparation)
    scope_members = _scope_members(preparation)
    origins: dict[str | None, tuple[float, float]] = {}
    desired: dict[str, tuple[float, float]] = {}
    for scope, members in sorted(scope_members.items(), key=lambda item: "<root>" if item[0] is None else str(item[0])):
        local = plan.scope_placements.get(scope)
        if not isinstance(local, Mapping):
            # A flat legacy StrictPlan can still be mapped at the root.  Nested
            # plans must expose explicit local scopes to avoid global-coordinate
            # writes into a child FlowView.
            if scope is not None:
                raise StrictHostApplyError(f"strict plan lacks local placement scope {scope!r}")
            local = plan.placements
        anchor = _scope_anchor(preparation, scope, members)
        if anchor not in local or anchor not in pre_positions:
            raise StrictHostApplyError(f"scope {scope!r} lacks a complete anchor position")
        point = local[anchor]
        origin = calibration.snap_origin(
            pre_positions[anchor][0] - point.column * calibration.cell_x,
            pre_positions[anchor][1] - point.row * calibration.cell_y,
        )
        origins[scope] = origin
        occupied: dict[tuple[float, float], str] = {}
        for uid in members:
            point = local.get(uid)
            if point is None:
                raise StrictHostApplyError(f"scope {scope!r} lacks placement for {uid!r}")
            position = calibration.host_position(point, origin)
            previous = occupied.get(position)
            if previous is not None and previous != uid:
                raise StrictHostApplyError(f"host coordinate collision in scope {scope!r}: {previous}/{uid}")
            occupied[position] = uid
            desired[uid] = position
    if set(desired) != set(plan.placements):
        missing = sorted(set(plan.placements) - set(desired))
        extra = sorted(set(desired) - set(plan.placements))
        raise StrictHostApplyError(f"scope mapping coverage mismatch missing={missing} extra={extra}")
    return desired, origins


def _restore_positions(
    flow: Any,
    tools: Mapping[str, Any],
    positions: Mapping[str, tuple[float, float]],
    tolerance: float,
    *,
    order: list[str] | None = None,
) -> list[str]:
    return _restore_positions_batch(
        flow,
        tools,
        positions,
        order=order,
        tolerance=tolerance,
    )


def _restore_order(preparation: StrictPreparation, positions: Mapping[str, tuple[float, float]]) -> list[str]:
    """Return parent-first order for nested strict snapshots."""
    parents: dict[str, str | None] = {}
    for name, node in preparation.processing.nodes.items():
        try:
            raw = _field_value(node.parent, path=f"nodes.{name}.parent")
        except StrictHostApplyError:
            raw = None
        parents[name] = None if raw in (None, "", "root") else str(raw)

    def depth(name: str) -> int:
        seen: set[str] = set()
        value = 0
        current = name
        while parents.get(current) is not None and current not in seen:
            seen.add(current)
            parent = parents.get(current)
            if parent is None:
                break
            value += 1
            current = parent
        return value

    return sorted(positions, key=lambda name: (depth(name), name))


def _write_positions(
    flow: Any,
    tools: Mapping[str, Any],
    writes: Mapping[str, tuple[float, float]],
    *,
    order: list[str] | None = None,
) -> None:
    names = list(order) if order is not None else sorted(writes)
    queue_set_pos = getattr(flow, "QueueSetPos", None)
    flush_set_pos = getattr(flow, "FlushSetPosQueue", None)
    if writes and callable(queue_set_pos) and callable(flush_set_pos):
        for name in names:
            result = queue_set_pos(tools[name], *writes[name])
            if result is False:
                raise StrictHostApplyError(f"FlowView position queue rejected {name!r}")
        result = flush_set_pos()
        if result is False:
            raise StrictHostApplyError("FlowView position queue flush was rejected")
        return
    setter = getattr(flow, "SetPos", None)
    if not callable(setter):
        raise StrictHostApplyError("FlowView.SetPos is unavailable")
    for name in names:
        result = setter(tools[name], *writes[name])
        if result is False:
            raise StrictHostApplyError(f"FlowView.SetPos rejected {name!r}")


def apply_strict_plan(
    preparation: StrictPreparation,
    comp: Any,
    tools: Mapping[str, Any],
    flow: Any | None = None,
    *,
    calibration: FlowViewCalibration | None = None,
    snapshot_reader: SnapshotReader = build_host_processing_snapshot,
    source: str = "resolve-fusion-host",
    manage_undo: bool = True,
) -> StrictRunResult:
    """Apply one validated strict plan with position-only mutation.

    The explicit ``tools`` mapping is required.  Rediscovering handles between
    snapshot and write would defeat the standalone-comp retention contract.
    """

    if not isinstance(preparation, StrictPreparation):
        raise TypeError("preparation must be StrictPreparation")
    if not isinstance(tools, Mapping) or not tools:
        raise StrictHostApplyError("explicit live tool handles are required")
    expected = set(preparation.plan.placements)
    if set(tools) != expected or any(tools[name] is None for name in expected):
        raise StrictHostApplyError("live tool handle coverage does not match strict plan identities")
    flow = _flow_for(comp, flow)
    calibration = calibration or FlowViewCalibration()
    pre_positions = _processing_positions(preparation)
    live_positions = _read_positions(flow, tools)
    if set(live_positions) != set(pre_positions) or any(
        not _close_enough(live_positions[name], pre_positions[name], epsilon=calibration.tolerance)
        for name in pre_positions
    ):
        raise StrictHostApplyError("live FlowView state changed after strict snapshot; refusing write")
    desired, origins = map_strict_plan_to_host(preparation, calibration=calibration)
    writes = {
        name: position
        for name, position in desired.items()
        if not _close_enough(live_positions[name], position, epsilon=calibration.tolerance)
    }
    before_signature = _signature(preparation.processing)
    start_undo = getattr(comp, "StartUndo", None)
    end_undo = getattr(comp, "EndUndo", None)
    undo_started = bool(manage_undo and writes and callable(start_undo) and callable(end_undo))
    if undo_started:
        start_undo("ResolveNodeKit: Strict Preserve")
    try:
        _write_positions(flow, tools, writes, order=_restore_order(preparation, writes))
        readback = _read_positions(flow, tools)
        mismatched = [
            name
            for name in sorted(desired)
            if not _close_enough(readback[name], desired[name], epsilon=calibration.tolerance)
        ]
        if mismatched:
            raise StrictHostApplyError("strict position readback mismatch: " + ", ".join(mismatched[:12]))
        try:
            post_snapshot = snapshot_reader(comp, flow, source=source)
        except Exception as exc:
            raise StrictHostApplyError("post-write processing readback failed: " + str(exc)) from exc
        if not isinstance(post_snapshot, ProcessingSnapshot):
            raise StrictHostApplyError("post-write snapshot reader returned an invalid type")
        after_signature = _signature(post_snapshot)
        if after_signature != before_signature:
            raise StrictHostApplyError("strict preserve changed processing/structure signature")
    except Exception as exc:
        restore_failures = _restore_positions(
            flow,
            tools,
            pre_positions,
            calibration.tolerance,
            order=_restore_order(preparation, pre_positions),
        )
        if undo_started:
            end_undo(False)
        if restore_failures:
            raise StrictHostApplyError(
                "strict write failed and rollback was incomplete for: " + ", ".join(restore_failures[:12])
            ) from exc
        if isinstance(exc, StrictHostApplyError):
            raise
        raise StrictHostApplyError(str(exc)) from exc
    else:
        if undo_started:
            end_undo(True)
    return StrictRunResult(
        moved_count=len(writes),
        desired_positions=desired,
        readback_positions=readback,
        scope_origins=origins,
        processing_unchanged=True,
        pre_signature=before_signature,
        post_signature=after_signature,
        handle_names=tuple(sorted(tools)),
    )


def execute_strict_preserve(
    comp: Any,
    tools: Mapping[str, Any],
    flow: Any | None = None,
    *,
    calibration: FlowViewCalibration | None = None,
    snapshot_reader: SnapshotReader = build_host_processing_snapshot,
    source: str = "resolve-fusion-host",
    require_first_move: bool = False,
) -> StrictPreserveResult:
    """Prepare/apply the same strict preserve request twice on one handle set."""

    runs: list[StrictRunResult] = []
    for index in (1, 2):
        try:
            preparation = prepare_strict_plan(
                comp,
                flow,
                snapshot_reader=snapshot_reader,
                source=source,
            )
        except StrictPreparationError:
            raise
        result = apply_strict_plan(
            preparation,
            comp,
            tools,
            flow,
            calibration=calibration,
            snapshot_reader=snapshot_reader,
            source=source,
        )
        runs.append(result)
        if index == 1 and require_first_move and result.moved_count == 0:
            raise StrictHostApplyError("strict preserve first run was a no-op; disordered fixture was not proven")
    stable = (
        runs[1].moved_count == 0
        and runs[1].readback_positions == runs[0].readback_positions
        and runs[1].post_signature == runs[0].post_signature
    )
    return StrictPreserveResult(runs[0], runs[1], stable)


__all__ = [
    "FlowViewCalibration",
    "StrictHostApplyError",
    "StrictPreserveResult",
    "StrictRunResult",
    "apply_strict_plan",
    "execute_strict_preserve",
    "map_strict_plan_to_host",
]
