from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from resolve_node_kit.core.layout import Edge, LayoutConfig, LayoutError, layout_graph
from .tidy import (
    FusionHostError,
    _attrs,
    _classify_input,
    _close_enough,
    _ensure_ordered_dict,
    _iter_values,
    _snap_position,
    _tool_name,
    _xy_from_pos_table,
)


_ensure_ordered_dict()


@dataclass(frozen=True)
class GroupTidyResult:
    node_count: int
    edge_count: int
    moved_count: int
    group_count: int
    expanded_count: int
    scope_count: int


@dataclass(frozen=True)
class _Snapshot:
    tools: dict[str, Any]
    positions: dict[str, tuple[float, float]]
    edges: tuple[Edge, ...]
    parents: dict[str, str | None]
    groups: tuple[str, ...]


def _reg_id(tool: Any) -> str:
    value = _attrs(tool).get("TOOLS_RegID") or getattr(tool, "ID", None)
    return str(value) if value else ""


def _parent_obj(tool: Any) -> Any | None:
    parent = getattr(tool, "ParentTool", None)
    if parent is not None and not callable(parent):
        return parent
    return _attrs(tool).get("TOOLH_GroupParent")


def _collect_tools(comp: Any) -> tuple[dict[str, Any], dict[str, str | None]]:
    tools: dict[str, Any] = {}
    fallback_parent: dict[str, str | None] = {}
    queue = [(tool, None) for tool in _iter_values(getattr(comp, "GetToolList", lambda: None)())]
    scanned_groups: set[str] = set()
    while queue:
        tool, discovered_parent = queue.pop(0)
        name = _tool_name(tool)
        known_parent = fallback_parent.get(name)
        if known_parent is not None and discovered_parent is not None and known_parent != discovered_parent:
            raise FusionHostError(
                f"duplicate tool name {name!r} appears under both {known_parent!r} and {discovered_parent!r}"
            )
        if name not in tools:
            tools[name] = tool
        if name not in fallback_parent or (fallback_parent[name] is None and discovered_parent is not None):
            fallback_parent[name] = discovered_parent
        if _reg_id(tool) == "GroupOperator" and name not in scanned_groups:
            scanned_groups.add(name)
            getter = getattr(tool, "GetChildrenList", None)
            if callable(getter):
                for child in _iter_values(getter()):
                    queue.append((child, name))

    parents: dict[str, str | None] = {}
    for name, tool in tools.items():
        parent = _parent_obj(tool)
        parents[name] = _tool_name(parent) if parent is not None else fallback_parent.get(name)
    return tools, parents


def _validate_hierarchy(tools: dict[str, Any], parents: dict[str, str | None]) -> tuple[str, ...]:
    groups = {name for name, tool in tools.items() if _reg_id(tool) == "GroupOperator"}
    for name, parent in parents.items():
        if parent is None:
            continue
        if parent not in tools or parent not in groups:
            raise FusionHostError(f"invalid GroupOperator parent {parent!r} for {name!r}")
    for name in tools:
        seen = {name}
        current = name
        while parents[current] is not None:
            parent = parents[current]
            assert parent is not None
            if parent in seen:
                raise FusionHostError(f"group hierarchy cycle detected at {parent!r}")
            seen.add(parent)
            current = parent
    return tuple(sorted(groups))


def _snapshot(comp: Any, flow: Any) -> _Snapshot:
    tools, parents = _collect_tools(comp)
    if not tools:
        return _Snapshot({}, {}, (), {}, ())
    groups = _validate_hierarchy(tools, parents)
    positions = {name: _xy_from_pos_table(flow.GetPosTable(tool)) for name, tool in sorted(tools.items())}
    edges: list[Edge] = []
    for target_name, target in sorted(tools.items()):
        for input_obj in _iter_values(getattr(target, "GetInputList", lambda: None)()):
            get_output = getattr(input_obj, "GetConnectedOutput", None)
            output = get_output() if callable(get_output) else None
            get_tool = getattr(output, "GetTool", None) if output is not None else None
            source = get_tool() if callable(get_tool) else None
            if source is None:
                continue
            source_name = _tool_name(source)
            if source_name not in tools:
                raise FusionHostError(f"connected source was not discovered: {source_name!r}")
            edges.append(Edge(source_name, target_name, _classify_input(input_obj)))
    return _Snapshot(tools, positions, tuple(edges), parents, groups)


def _depth(name: str, parents: dict[str, str | None]) -> int:
    depth, current = 0, name
    while parents[current] is not None:
        depth += 1
        current = parents[current]  # type: ignore[assignment]
    return depth


def _project(name: str, scope: str | None, parents: dict[str, str | None]) -> str | None:
    current = name
    while True:
        parent = parents[current]
        if parent == scope:
            return current
        if parent is None:
            return None
        current = parent


def _layout(snapshot: _Snapshot, config: LayoutConfig | None) -> tuple[dict[str, tuple[float, float]], int]:
    desired: dict[str, tuple[float, float]] = {}
    scopes: list[str | None] = [None]
    scopes += sorted(snapshot.groups, key=lambda name: (_depth(name, snapshot.parents), name))
    scope_count = 0
    for scope in scopes:
        children = sorted(name for name, parent in snapshot.parents.items() if parent == scope)
        if not children:
            continue
        child_set = set(children)
        edges: list[Edge] = []
        for edge in snapshot.edges:
            source = _project(edge.source, scope, snapshot.parents)
            target = _project(edge.target, scope, snapshot.parents)
            if source in child_set and target in child_set and source != target:
                edges.append(Edge(source, target, edge.kind))
        original = {name: snapshot.positions[name] for name in children}
        relative = layout_graph(children, edges, original_positions=original, config=config)
        anchor_x = min(x for x, _ in original.values())
        anchor_y = min(y for _, y in original.values())
        for name, (x, y) in relative.items():
            desired[name] = _snap_position(anchor_x + x, anchor_y + y)
        scope_count += 1
    if set(desired) != set(snapshot.tools):
        missing = sorted(set(snapshot.tools) - set(desired))
        raise FusionHostError(f"recursive layout omitted tools: {', '.join(missing[:12])}")
    return desired, scope_count


def _table_get(table: Any, key: str, default: Any = None) -> Any:
    if table is None:
        return default
    if isinstance(table, dict):
        return table.get(key, default)
    try:
        return table[key]
    except Exception:
        return getattr(table, key, default)


def _table_set(table: Any, key: str, value: Any) -> None:
    if isinstance(table, dict):
        table[key] = value
        return
    try:
        table[key] = value
    except Exception:
        try:
            setattr(table, key, value)
        except Exception as exc:
            raise FusionHostError(f"cannot mutate settings field {key!r}") from exc


def _group_block(settings: Any, name: str) -> Any:
    tools = _table_get(settings, "Tools")
    block = _table_get(tools, name) if tools is not None else None
    return block if block is not None else settings


def _is_expanded(settings: Any, name: str) -> bool:
    view = _table_get(_group_block(settings, name), "ViewInfo")
    return bool(_table_get(_table_get(view, "Flags"), "Expanded", False))


def _set_expanded(settings: Any, name: str, value: bool) -> Any:
    view = _table_get(_group_block(settings, name), "ViewInfo")
    if view is None:
        raise FusionHostError(f"GroupOperator {name!r} has no ViewInfo")
    flags = _table_get(view, "Flags")
    if flags is None:
        flags = {}
        _table_set(view, "Flags", flags)
    _table_set(flags, "Expanded", bool(value))
    return settings


def _find_tool(comp: Any, name: str, fallback: dict[str, Any]) -> Any:
    finder = getattr(comp, "FindTool", None)
    if callable(finder):
        try:
            found = finder(name)
            if found is not None:
                return found
        except Exception:
            pass
    if name not in fallback:
        raise FusionHostError(f"cannot reacquire tool {name!r}")
    return fallback[name]


def _save_group_states(snapshot: _Snapshot) -> dict[str, Any]:
    saved: dict[str, Any] = {}
    for name in sorted(snapshot.groups, key=lambda n: (_depth(n, snapshot.parents), n)):
        tool = snapshot.tools[name]
        save, load = getattr(tool, "SaveSettings", None), getattr(tool, "LoadSettings", None)
        if not callable(save) or not callable(load):
            raise FusionHostError(f"GroupOperator {name!r} lacks SaveSettings/LoadSettings")
        original, probe = save(), save()
        if original is None or probe is None:
            raise FusionHostError(f"GroupOperator {name!r} settings snapshot failed")
        original_state = _is_expanded(original, name)
        _set_expanded(probe, name, True)
        if _is_expanded(original, name) != original_state:
            raise FusionHostError(f"GroupOperator {name!r} returned shared mutable settings")
        saved[name] = original
    return saved


def _expand_groups(comp: Any, snapshot: _Snapshot, saved: dict[str, Any]) -> list[str]:
    changed: list[str] = []
    for name in sorted(snapshot.groups, key=lambda n: (_depth(n, snapshot.parents), n)):
        if _is_expanded(saved[name], name):
            continue
        tool = _find_tool(comp, name, snapshot.tools)
        save, load = getattr(tool, "SaveSettings", None), getattr(tool, "LoadSettings", None)
        if not callable(save) or not callable(load):
            raise FusionHostError(f"GroupOperator {name!r} settings API disappeared")
        working = save()
        if working is None:
            raise FusionHostError(f"GroupOperator {name!r} working settings unavailable")
        result = load(_set_expanded(working, name, True))
        if result is False:
            raise FusionHostError(f"GroupOperator {name!r} rejected Expanded=true")
        readback = save()
        if readback is None or not _is_expanded(readback, name):
            raise FusionHostError(f"GroupOperator {name!r} expansion readback failed")
        changed.append(name)
    return changed


def _restore_groups(comp: Any, snapshot: _Snapshot, saved: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for name in sorted(saved, key=lambda n: (_depth(n, snapshot.parents), n)):
        try:
            tool = _find_tool(comp, name, snapshot.tools)
            load = getattr(tool, "LoadSettings", None)
            if not callable(load) or load(saved[name]) is False:
                failures.append(name)
        except Exception:
            failures.append(name)
    return failures


def _restore_positions(comp: Any, flow: Any, snapshot: _Snapshot) -> list[str]:
    failures: list[str] = []
    try:
        live, _ = _collect_tools(comp)
    except Exception:
        live = {}
    for name, (x, y) in sorted(snapshot.positions.items()):
        try:
            tool = live.get(name) or snapshot.tools[name]
            flow.SetPos(tool, x, y)
            if not _close_enough(_xy_from_pos_table(flow.GetPosTable(tool)), (x, y)):
                failures.append(name)
        except Exception:
            failures.append(name)
    return failures


def _edge_signature(snapshot: _Snapshot) -> tuple[tuple[str, str, str], ...]:
    return tuple(sorted((e.source, e.target, e.kind) for e in snapshot.edges))


def tidy_groups_comp(comp: Any, config: LayoutConfig | None = None) -> GroupTidyResult:
    """Expand GroupOperators and deterministically tidy every nested group scope.

    Group membership and connections are never intentionally changed. Cross-boundary
    connections are projected to the visible group node only for layout planning.
    """
    frame = getattr(comp, "CurrentFrame", None)
    flow = getattr(frame, "FlowView", None) if frame is not None else None
    if flow is None or not callable(getattr(flow, "GetPosTable", None)) or not callable(getattr(flow, "SetPos", None)):
        raise FusionHostError("required Fusion FlowView position API is unavailable")

    original = _snapshot(comp, flow)
    if not original.tools:
        return GroupTidyResult(0, 0, 0, 0, 0, 0)
    saved = _save_group_states(original) if original.groups else {}
    start_undo, end_undo = getattr(comp, "StartUndo", None), getattr(comp, "EndUndo", None)
    undo = callable(start_undo) and callable(end_undo)
    if undo:
        start_undo("ResolveNodeKit: Tidy + Expand Groups")

    expanded: list[str] = []
    active = original
    try:
        if saved:
            expanded = _expand_groups(comp, original, saved)
            active = _snapshot(comp, flow)
            if active.parents != original.parents or set(active.tools) != set(original.tools):
                raise FusionHostError("group expansion changed the discovered hierarchy")
            if _edge_signature(active) != _edge_signature(original):
                raise FusionHostError("group expansion changed node connections")

        desired, scope_count = _layout(active, config)
        writes = {name: pos for name, pos in desired.items() if not _close_enough(active.positions[name], pos)}
        for name in sorted(writes):
            flow.SetPos(active.tools[name], *writes[name])
        mismatch = [
            name for name in sorted(writes)
            if not _close_enough(_xy_from_pos_table(flow.GetPosTable(active.tools[name])), desired[name])
        ]
        if mismatch:
            raise FusionHostError(f"position readback mismatch: {', '.join(mismatch[:12])}")
        for name in active.groups:
            tool = _find_tool(comp, name, active.tools)
            settings = getattr(tool, "SaveSettings", lambda: None)()
            if settings is None or not _is_expanded(settings, name):
                raise FusionHostError(f"GroupOperator {name!r} did not remain expanded")
    except Exception as exc:
        position_failures = _restore_positions(comp, flow, original)
        group_failures = _restore_groups(comp, original, saved) if saved else []
        if undo:
            end_undo(False)
        failures = position_failures + [f"group:{name}" for name in group_failures]
        if failures:
            raise FusionHostError(f"recursive tidy failed; rollback incomplete for: {', '.join(failures[:12])}") from exc
        if isinstance(exc, (FusionHostError, LayoutError)):
            raise
        raise FusionHostError(f"recursive tidy failed; original state restored: {exc}") from exc
    else:
        if undo:
            end_undo(True)

    return GroupTidyResult(
        node_count=len(active.tools), edge_count=len(active.edges), moved_count=len(writes),
        group_count=len(active.groups), expanded_count=len(expanded), scope_count=scope_count,
    )
