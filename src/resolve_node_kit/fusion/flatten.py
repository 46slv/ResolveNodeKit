"""Fail-closed structural flattening for Fusion compositions.

Fusion's public scripting surface does not expose a portable ``Ungroup``
operation on the measured Resolve build.  This module therefore keeps the
structural part behind an explicit host-adapter primitive instead of guessing
from a UI action, deleting/recreating tools, or rewriting settings.  When a
host adapter supplies such a primitive, the wrapper enforces the complete
snapshot -> deepest-first ungroup -> flat readback -> semantic Arrange -> one
Undo transaction contract.
"""
from __future__ import annotations

import hashlib
import time
from collections.abc import Callable, Mapping
from typing import Any

from .recursive_groups import (
    _Snapshot,
    _collect_edges,
    _collect_tools,
    _depth,
    _edge_signature,
    _snapshot,
    _validate_hierarchy,
)
from .tidy import FusionHostError


UngroupPrimitive = Callable[[Any, Any], Any]


def _hash_lines(lines: list[str]) -> str:
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def _max_group_depth(parents: Mapping[str, str | None]) -> int:
    maximum = 0
    for name in parents:
        seen: set[str] = set()
        depth = 0
        current = name
        while parents.get(current) is not None:
            parent = parents[current]
            assert parent is not None
            if parent in seen:
                raise FusionHostError(f"group hierarchy cycle detected at {parent!r}")
            seen.add(parent)
            depth += 1
            current = parent
        maximum = max(maximum, depth)
    return maximum


def _compact_snapshot(snapshot: _Snapshot) -> dict[str, Any]:
    parent_lines = [f"{name}\t{snapshot.parents[name] or ''}" for name in sorted(snapshot.parents)]
    non_groups = [
        name for name, tool in sorted(snapshot.tools.items())
        if (getattr(tool, "GetAttrs", lambda: {})() or {}).get("TOOLS_RegID") != "GroupOperator"
    ]
    edge_lines = [
        f"{edge.source}\t{edge.target}\t{edge.kind}"
        for edge in sorted(snapshot.edges, key=lambda item: (item.source, item.target, item.kind))
    ]
    position_lines = [
        f"{name}\t{x:.9f}\t{y:.9f}"
        for name, (x, y) in sorted(snapshot.positions.items())
    ]
    return {
        "tool_count": len(snapshot.tools),
        "edge_count": len(snapshot.edges),
        "group_count": len(snapshot.groups),
        "max_group_depth": _max_group_depth(snapshot.parents),
        "non_group_identity_hash": _hash_lines(non_groups),
        "parent_hash": _hash_lines(parent_lines),
        "connection_hash": _hash_lines(edge_lines),
        "position_hash": _hash_lines(position_lines),
    }


def _primitive_result(value: Any) -> dict[str, str]:
    """Normalize the optional endpoint mapping returned by a host primitive."""
    if value is False:
        raise FusionHostError("host ungroup primitive rejected the GroupOperator")
    if value is None or value is True:
        return {}
    if not isinstance(value, Mapping):
        raise FusionHostError("host ungroup primitive returned an unsupported result")
    raw = value.get("endpoint_map", {})
    if raw is None:
        return {}
    if not isinstance(raw, Mapping):
        raise FusionHostError("host ungroup endpoint_map is not a mapping")
    mapping: dict[str, str] = {}
    for source, target in raw.items():
        if not isinstance(source, str) or not isinstance(target, str) or not target:
            raise FusionHostError("host ungroup endpoint_map contains an invalid endpoint")
        mapping[source] = target
    return mapping


def _map_endpoint(name: str, mapping: Mapping[str, str]) -> str:
    seen: set[str] = set()
    current = name
    while current in mapping:
        if current in seen:
            raise FusionHostError(f"flatten endpoint map cycle detected at {current!r}")
        seen.add(current)
        current = mapping[current]
    return current


def _expected_edges(snapshot: _Snapshot, endpoint_map: Mapping[str, str]) -> tuple[tuple[str, str, str], ...]:
    return tuple(
        sorted(
            (
                _map_endpoint(edge.source, endpoint_map),
                _map_endpoint(edge.target, endpoint_map),
                edge.kind,
            )
            for edge in snapshot.edges
        )
    )


def _expected_parents(
    original: Mapping[str, str | None], removed: set[str]
) -> dict[str, str | None]:
    expected: dict[str, str | None] = {}
    for name in original:
        if name in removed:
            continue
        parent = original[name]
        seen: set[str] = {name}
        while parent in removed:
            if parent in seen:
                raise FusionHostError(f"flatten parent chain cycles at {parent!r}")
            seen.add(parent)
            parent = original.get(parent)  # type: ignore[arg-type]
        expected[name] = parent
    return expected


def _flat_readback(
    comp: Any,
    original: _Snapshot,
    removed: set[str],
    endpoint_map: Mapping[str, str],
) -> _Snapshot:
    frame = getattr(comp, "CurrentFrame", None)
    flow = getattr(frame, "FlowView", None) if frame is not None else None
    if flow is None:
        raise FusionHostError("flatten readback lost the active Fusion FlowView")
    live = _snapshot(comp, flow)
    expected_names = set(original.tools) - removed
    if set(live.tools) != expected_names:
        raise FusionHostError("flatten changed the tool set beyond removed GroupOperators")
    expected_parents = _expected_parents(original.parents, removed)
    if live.parents != expected_parents:
        raise FusionHostError("flatten produced an unexpected parent chain")
    if _edge_signature(live) != _expected_edges(original, endpoint_map):
        raise FusionHostError("flatten changed node connections")
    return live


def _snapshot_exact(left: _Snapshot, right: _Snapshot) -> bool:
    return (
        set(left.tools) == set(right.tools)
        and left.parents == right.parents
        and left.positions == right.positions
        and _edge_signature(left) == _edge_signature(right)
        and left.groups == right.groups
    )


def host_ungroup_capabilities(comp: Any, flow: Any | None = None) -> dict[str, Any]:
    """Report only explicit callable ungroup surfaces; do not invoke them."""
    owners = [("comp", comp)]
    if flow is not None:
        owners.append(("flow", flow))
    names = ("Ungroup", "UnGroup", "UngroupTool")
    callables = [
        f"{owner_name}.{method_name}"
        for owner_name, owner in owners
        for method_name in names
        if callable(getattr(owner, method_name, None))
    ]
    return {
        "supported": bool(callables),
        "callables": callables,
        "note": "Generic DoAction/QueueAction is not treated as an ungroup primitive",
    }


def flatten_all_comp(
    comp: Any,
    *,
    policy: Any = None,
    ungroup: UngroupPrimitive | None = None,
    progress: Any = None,
) -> dict[str, Any]:
    """Flatten all eligible groups and Arrange the resulting flat graph.

    ``ungroup`` is deliberately an explicit adapter callback with the stable
    signature ``(comp, group_tool)``.  It must perform a host-native ungroup
    without deleting/recreating child tools and may return
    ``{"endpoint_map": {old_group: replacement_tool}}`` when a boundary edge
    is necessarily projected to a child.  Every returned structure is checked
    before the next group is touched.
    """
    if not callable(ungroup):
        raise FusionHostError(
            "Flatten-all is unavailable: the host adapter supplied no measured "
            "identity-preserving ungroup primitive"
        )
    frame = getattr(comp, "CurrentFrame", None)
    flow = getattr(frame, "FlowView", None) if frame is not None else None
    if flow is None or not callable(getattr(flow, "GetPosTable", None)):
        raise FusionHostError("required Fusion FlowView position API is unavailable")

    timings: dict[str, float] = {}

    def timed(name: str, started: float) -> None:
        timings[name] = round((time.perf_counter() - started) * 1000.0, 1)

    def note(message: str) -> None:
        if progress is not None:
            try:
                progress(message)
            except Exception:
                pass

    started = time.perf_counter()
    original = _snapshot(comp, flow)
    timed("flatten_snapshot", started)
    if not original.tools:
        return {
            "node_count": 0,
            "edge_count": 0,
            "group_count": 0,
            "flattened_group_count": 0,
            "moved_count": 0,
            "arranged_count": 0,
            "stage_timings_ms": timings,
        }
    groups = _validate_hierarchy(original.tools, original.parents)
    if not groups:
        # No structural mutation is necessary.  Delegate to the normal
        # preserve path so a no-group second run still owns its own Undo entry
        # when it actually moves nodes.
        from .semantic import arrange_comp

        result = arrange_comp(comp, include_unselected=True, policy=policy, progress=progress)
        result = dict(result)
        result.update({"group_count": 0, "flattened_group_count": 0})
        result["stage_timings_ms"] = {**timings, **result.get("stage_timings_ms", {})}
        return result

    start_undo = getattr(comp, "StartUndo", None)
    end_undo = getattr(comp, "EndUndo", None)
    undo = callable(start_undo) and callable(end_undo)
    if not undo:
        raise FusionHostError("flatten-all requires StartUndo/EndUndo for exact restoration")
    if start_undo("ResolveNodeKit: Flatten All + Arrange") is False:
        raise FusionHostError("flatten-all Undo transaction could not start")

    endpoint_map: dict[str, str] = {}
    removed: set[str] = set()
    try:
        order = sorted(groups, key=lambda name: (-_depth(name, original.parents), name))
        for name in order:
            note("flatten ungroup " + name)
            live_tools, _live_parents = _collect_tools(comp)
            group = live_tools.get(name)
            if group is None:
                raise FusionHostError(f"GroupOperator {name!r} disappeared before ungroup")
            started = time.perf_counter()
            mapping = _primitive_result(ungroup(comp, group))
            endpoint_map.update(mapping)
            removed.add(name)
            _flat_readback(comp, original, removed, endpoint_map)
            timed("ungroup_" + name, started)

        started = time.perf_counter()
        flat = _flat_readback(comp, original, removed, endpoint_map)
        timed("flatten_readback", started)
        if flat.groups:
            raise FusionHostError("flatten left GroupOperators in the active scope")

        from .semantic import arrange_comp

        note("flatten arrange")
        started = time.perf_counter()
        arranged = arrange_comp(
            comp,
            include_unselected=True,
            ungroup=False,
            policy=policy,
            progress=progress,
            manage_undo=False,
        )
        timed("arrange", started)

        started = time.perf_counter()
        final = _snapshot(comp, flow)
        if final.groups:
            raise FusionHostError("flatten Arrange recreated GroupOperators")
        if set(final.tools) != set(original.tools) - removed:
            raise FusionHostError("flatten Arrange changed non-Group tool identities")
        if _edge_signature(final) != _expected_edges(original, endpoint_map):
            raise FusionHostError("flatten Arrange changed node connections")
        timed("final_readback", started)
    except Exception as exc:
        # EndUndo(False) is the first rollback boundary.  If the host leaves a
        # structural delta behind, use exactly one owned Undo and verify the
        # complete original snapshot before reporting the failure.
        try:
            end_undo(False)
        except Exception:
            pass
        restored = False
        try:
            restored = _snapshot_exact(_snapshot(comp, flow), original)
        except Exception:
            restored = False
        if not restored:
            undo_method = getattr(comp, "Undo", None)
            if callable(undo_method):
                try:
                    undo_method()
                    restored = _snapshot_exact(_snapshot(comp, flow), original)
                except Exception:
                    restored = False
        if not restored:
            raise FusionHostError("flatten failed and exact structural rollback was not proven") from exc
        if isinstance(exc, FusionHostError):
            raise
        raise FusionHostError(f"flatten failed; original state restored: {exc}") from exc
    else:
        started = time.perf_counter()
        end_undo(True)
        timed("undo_close", started)

    compact = _compact_snapshot(final)
    arrange_timings = arranged.get("stage_timings_ms", {})
    merged_timings = {**timings, **{"arrange_" + str(key): value for key, value in arrange_timings.items()}}
    return {
        **arranged,
        **compact,
        "group_count_pre": len(original.groups),
        "group_count": 0,
        "flattened_group_count": len(removed),
        "endpoint_map": dict(endpoint_map),
        "processing_evidence": "NOT_COLLECTED_BY_HOST_ADAPTER",
        "stage_timings_ms": merged_timings,
    }

