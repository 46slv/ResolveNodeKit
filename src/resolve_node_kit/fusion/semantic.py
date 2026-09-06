"""Group-local semantic layout planner plus Arrange entrypoint (v1).

Pure planning (no host calls) uses integer logical-grid layout with a
horizontal Merge backbone rail, vertical branch columns, vertical
Merge-reduction columns, elastic whole-cell Merge gaps, and recursive
Group-local scopes. The host adapter (arrange_comp) reuses the established
safe write contract: snapshot, bounded write, readback, invariant comparison,
rollback on mismatch.

Ungroup mode is intentionally fail-closed: arrange_comp refuses any mutation
while ungroup is True until exact structural restoration is host-proven on a
disposable fixture.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class GridPoint:
    column: int
    row: int


@dataclass(frozen=True)
class SemanticEdge:
    source: str
    target: str
    kind: str = "other"


@dataclass(frozen=True)
class SemanticNode:
    name: str
    reg_id: str = ""
    parent: str | None = None
    is_group: bool = False


@dataclass(frozen=True)
class SemanticSnapshot:
    nodes: dict[str, SemanticNode]
    edges: tuple[SemanticEdge, ...]


@dataclass(frozen=True)
class SemanticPolicy:
    """Named spacing classes in whole logical cells."""

    regular_rail_spacing_x: int = 3
    merge_rail_spacing_x: int = 3
    branch_spacing_y: int = 3
    branch_cluster_gap_x: int = 3
    component_gap_y: int = 4
    group_gap_x: int = 4
    group_gap_y: int = 4
    group_padding_x: int = 1
    group_padding_y: int = 1
    cell_x: float = 1.0
    cell_y: float = 1.0


GAP_DEFAULT = "DEFAULT"
GAP_BRANCH_CLEARANCE = "BRANCH_CLEARANCE"
GAP_GROUP_CLEARANCE = "GROUP_CLEARANCE"
GAP_COMPONENT_CLEARANCE = "COMPONENT_CLEARANCE"


def is_merge_like(reg_id: str, name: str = "") -> bool:
    text = f"{reg_id} {name}".lower()
    return "merge" in text


def _is_output_like(reg_id: str, name: str) -> bool:
    text = f"{reg_id} {name}".lower()
    for key in ("mediaout", "saver", "output", "out"):
        if key in text:
            return True
    return False


class SemanticError(RuntimeError):
    pass


@dataclass
class PlannedScope:
    scope: str | None
    placements: dict[str, GridPoint] = field(default_factory=dict)
    backbone: list[str] = field(default_factory=list)
    merge_runs: list[list[str]] = field(default_factory=list)
    gap_reasons: dict[tuple[str, str], str] = field(default_factory=dict)
    box_width: int = 1
    box_height: int = 1


@dataclass
class PlannedLayout:
    scopes: dict[str | None, PlannedScope]
    diagnostics: dict[str, Any]


def build_snapshot(
    names: Iterable[str],
    edges: Iterable[SemanticEdge],
    reg_ids: Mapping[str, str] | None = None,
    parents: Mapping[str, str | None] | None = None,
    group_names: Iterable[str] = (),
) -> SemanticSnapshot:
    node_names = [str(name) for name in names]
    if len(set(node_names)) != len(node_names):
        raise SemanticError("duplicate tool names in semantic snapshot")
    node_set = set(node_names)
    groups = {str(name) for name in group_names}
    norm_edges: list[SemanticEdge] = []
    seen: set[tuple[str, str]] = set()
    for edge in edges:
        if edge.source not in node_set or edge.target not in node_set:
            raise SemanticError(f"edge references unknown node: {edge.source!r} -> {edge.target!r}")
        if edge.source == edge.target:
            raise SemanticError(f"self edge refused: {edge.source!r}")
        key = (edge.source, edge.target)
        if key in seen:
            continue
        seen.add(key)
        norm_edges.append(edge)
    nodes = {
        name: SemanticNode(
            name=name,
            reg_id=str((reg_ids or {}).get(name, "")),
            parent=(parents or {}).get(name),
            is_group=name in groups,
        )
        for name in node_names
    }
    for name, node in nodes.items():
        if node.parent is not None and node.parent not in node_set:
            raise SemanticError(f"unknown parent {node.parent!r} for {name!r}")
    return SemanticSnapshot(nodes=nodes, edges=tuple(norm_edges))


def _children_of(scope: str | None, snapshot: SemanticSnapshot) -> list[str]:
    return sorted(name for name, node in snapshot.nodes.items() if node.parent == scope)


def _scope_edges(scope_children: set[str], snapshot: SemanticSnapshot) -> list[SemanticEdge]:
    return [e for e in snapshot.edges if e.source in scope_children and e.target in scope_children]


def _select_backbone(
    children: list[str],
    edges: list[SemanticEdge],
    snapshot: SemanticSnapshot,
) -> list[str]:
    """Deterministic output-oriented backbone path within one scope."""
    child_set = set(children)
    successors: dict[str, set[str]] = {name: set() for name in children}
    predecessors: dict[str, set[str]] = {name: set() for name in children}
    for edge in edges:
        successors[edge.source].add(edge.target)
        predecessors[edge.target].add(edge.source)
    sinks = sorted(name for name in children if not (successors[name] & child_set))
    if not sinks:
        raise SemanticError(f"cycle detected in scope; refusing to plan: {sorted(child_set)[:12]}")
    sinks.sort(key=lambda name: (0 if _is_output_like(snapshot.nodes[name].reg_id, name) else 1, name))
    sink = sinks[0]
    # Backbone follows the canvas stream: Background and ordinary inputs are
    # mainstream (+1); Foreground and mask inputs are sidestreams (-1). A long
    # side chain therefore cannot hijack the backbone from a shorter canvas
    # stream. Length, Merge density, and group avoidance break remaining ties.
    mainstream = {"background", "other"}
    edge_kind: dict[tuple[str, str], str] = {(e.source, e.target): e.kind for e in edges}
    memo: dict[str, tuple[int, int, int, int, tuple[str, ...]]] = {}

    def best_path(node: str, visiting: frozenset[str]) -> tuple[int, int, int, int, tuple[str, ...]]:
        if node in memo:
            return memo[node]
        if node in visiting:
            raise SemanticError(f"cycle detected near {node!r}; refusing to plan")
        preds = sorted(predecessors[node] & child_set)
        if not preds:
            leaf_groups = 0 if not snapshot.nodes[node].is_group else -1
            leaf_merge = 1 if is_merge_like(snapshot.nodes[node].reg_id, node) else 0
            result = (0, 0, leaf_merge, leaf_groups, (node,))
            memo[node] = result
            return result
        best: tuple[int, int, int, int, tuple[str, ...]] | None = None
        for pred in preds:
            pscore, plen, pmerge, pgroups, ppath = best_path(pred, visiting | {node})
            kind = edge_kind.get((pred, node), "other")
            delta = 1 if kind in mainstream else -1
            groups_here = pgroups + (0 if not snapshot.nodes[node].is_group else -1)
            candidate = (
                pscore + delta,
                plen + 1,
                pmerge + (1 if is_merge_like(snapshot.nodes[node].reg_id, node) else 0),
                groups_here,
                ppath + (node,),
            )
            if best is None or candidate > best:
                best = candidate
        assert best is not None
        memo[node] = best
        return best

    return list(best_path(sink, frozenset())[4])


def _merge_runs(backbone: list[str], snapshot: SemanticSnapshot) -> list[list[str]]:
    runs: list[list[str]] = []
    current: list[str] = []
    for name in backbone:
        if is_merge_like(snapshot.nodes[name].reg_id, name):
            current.append(name)
        else:
            if len(current) >= 2:
                runs.append(list(current))
            current = []
    if len(current) >= 2:
        runs.append(list(current))
    return runs


def _is_vertical_reduction_chain(
    chain: list[str],
    edges: list[SemanticEdge],
    snapshot: SemanticSnapshot,
) -> bool:
    """Merge side chain linked by Background edges with side Foregrounds."""
    if len(chain) < 2:
        return False
    for name in chain:
        if not is_merge_like(snapshot.nodes[name].reg_id, name):
            return False
    by_pair = {(edge.source, edge.target): edge.kind for edge in edges}
    for upper, lower in zip(chain, chain[1:]):
        if by_pair.get((upper, lower)) != "background":
            return False
    return True


def plan_scope(
    scope: str | None,
    snapshot: SemanticSnapshot,
    policy: SemanticPolicy,
    child_boxes: Mapping[str, tuple[int, int]] | None = None,
) -> PlannedScope:
    """Plan one layout scope on the integer logical grid (pure)."""
    child_boxes = child_boxes or {}
    children = _children_of(scope, snapshot)
    planned = PlannedScope(scope=scope)
    if not children:
        return planned
    edges = _scope_edges(set(children), snapshot)
    backbone = _select_backbone(children, edges, snapshot)
    backbone_set = set(backbone)
    planned.backbone = list(backbone)
    planned.merge_runs = _merge_runs(backbone, snapshot)

    incoming: dict[str, list[str]] = {name: [] for name in children}
    outgoing: dict[str, list[str]] = {name: [] for name in children}
    for edge in edges:
        incoming[edge.target].append(edge.source)
        outgoing[edge.source].append(edge.target)
    for name in incoming:
        incoming[name].sort()

    branch_of: dict[str, str] = {}

    def claim_branch(node: str, receiver: str, seen: set[str]) -> None:
        if node in backbone_set or node in branch_of or node in seen:
            return
        seen.add(node)
        branch_of[node] = receiver
        for pred in incoming[node]:
            claim_branch(pred, receiver, seen)

    for node in backbone:
        for pred in incoming[node]:
            if pred not in backbone_set:
                claim_branch(pred, node, set())

    branch_children: dict[str, list[str]] = {}
    for node, receiver in branch_of.items():
        branch_children.setdefault(receiver, []).append(node)
    vertical_chains: list[list[str]] = []
    for receiver in backbone:
        owned = sorted(n for n in branch_children.get(receiver, []) if is_merge_like(snapshot.nodes[n].reg_id, n))
        owned_set = set(owned)
        heads = [n for n in owned if not any(e.source in owned_set and e.target == n for e in edges)]
        heads.sort()
        for head in heads:
            chain = [head]
            while True:
                nxt = sorted(s for s in outgoing[chain[-1]] if s in owned_set and s not in chain)
                bg = [s for s in nxt if (chain[-1], s) in {(e.source, e.target) for e in edges if e.kind == "background"}]
                nxt_node = (bg or nxt)[:1]
                if not nxt_node:
                    break
                chain.append(nxt_node[0])
            if _is_vertical_reduction_chain(chain, edges, snapshot):
                vertical_chains.append(chain)
    vertical_members = {n for chain in vertical_chains for n in chain}

    placements: dict[str, GridPoint] = {}
    occupied: set[tuple[int, int]] = set()
    gap_reasons: dict[tuple[str, str], str] = {}

    def box_size(name: str) -> tuple[int, int]:
        if snapshot.nodes[name].is_group:
            return child_boxes.get(name, (3, 3))
        return (1, 1)

    def reserve(point: GridPoint, name: str) -> GridPoint:
        width, _height = box_size(name)
        while any((point.column + dx, point.row) in occupied for dx in range(width)):
            point = GridPoint(point.column + 1, point.row)
        for dx in range(width):
            occupied.add((point.column + dx, point.row))
        return point

    col = 0
    prev: str | None = None
    for node in backbone:
        clearance = policy.regular_rail_spacing_x
        reason = GAP_DEFAULT
        if prev is not None and any(node in run and prev in run for run in planned.merge_runs):
            clearance = max(clearance, policy.merge_rail_spacing_x)
        owned_here = [n for n in branch_children.get(node, []) if n not in vertical_members]
        if owned_here and prev is not None:
            reason = GAP_BRANCH_CLEARANCE
            clearance = max(clearance, policy.merge_rail_spacing_x + 1)
        if snapshot.nodes[node].is_group and prev is not None:
            if reason == GAP_DEFAULT:
                reason = GAP_GROUP_CLEARANCE
            clearance = max(clearance, policy.group_gap_x)
        if prev is not None and clearance > policy.regular_rail_spacing_x:
            gap_reasons[(prev, node)] = reason
        if prev is not None:
            col = col + clearance + (box_size(prev)[0] - 1)
        placements[node] = reserve(GridPoint(col, 0), node)
        prev = node

    for node in backbone:
        receiver_col = placements[node].column
        owned_here = sorted(
            (n for n in branch_children.get(node, []) if n not in vertical_members),
            key=lambda n: (0 if any(e.source == n and e.target == node for e in edges) else 1, n),
        )
        depth: dict[str, int] = {}

        def branch_depth(n: str) -> int:
            if n in depth:
                return depth[n]
            preds = [p for p in incoming[n] if p in branch_of and branch_of[p] == node]
            depth[n] = 0 if not preds else 1 + max(branch_depth(p) for p in preds)
            return depth[n]

        owned_here.sort(key=lambda n: (branch_depth(n), n))
        used_offsets: set[int] = set()
        for member in owned_here:
            preds_in_branch = [p for p in incoming[member] if p in branch_of and branch_of[p] == node]
            if not preds_in_branch:
                offset = 0
                while offset in used_offsets:
                    offset += 1
                used_offsets.add(offset)
                base_col = receiver_col + offset * policy.branch_cluster_gap_x
                placements[member] = reserve(GridPoint(base_col, -policy.branch_spacing_y), member)
            else:
                parent = sorted(preds_in_branch)[0]
                parent_pt = placements[parent]
                placements[member] = reserve(
                    GridPoint(parent_pt.column, parent_pt.row - policy.branch_spacing_y), member
                )

    for chain in vertical_chains:
        receiver = branch_of[chain[0]]
        recv_pt = placements[receiver]
        chain_col = recv_pt.column - policy.branch_cluster_gap_x
        row = recv_pt.row - policy.branch_spacing_y * (len(chain) - 1)
        for i, member in enumerate(chain):
            placements[member] = reserve(GridPoint(chain_col, row + i * policy.branch_spacing_y), member)
        for member in chain:
            direct = sorted(p for p in incoming[member] if p not in vertical_members and p not in backbone_set)
            slot = 0
            for feeder in direct:
                home = branch_of.get(feeder)
                if home is not None and home != receiver:
                    continue
                upstream = [p for p in incoming[feeder] if branch_of.get(p) == (home or receiver)]
                if upstream:
                    continue
                slot += 1
                side = chain_col + slot * policy.branch_cluster_gap_x
                # Overwrite when the branch lane already placed this feeder;
                # stale occupied cells stay reserved, which is conservative.
                placements[feeder] = reserve(GridPoint(side, placements[member].row), feeder)
                branch_of[feeder] = member

    lane_row = policy.component_gap_y
    lane_col = 0
    for name in children:
        if name in placements:
            continue
        placements[name] = reserve(GridPoint(lane_col, lane_row), name)
        lane_col += policy.branch_cluster_gap_x + box_size(name)[0] - 1
        if lane_col > col + policy.component_gap_y:
            lane_col = 0
            lane_row += policy.branch_spacing_y
        gap_reasons[(name, name)] = GAP_COMPONENT_CLEARANCE

    planned.placements = placements
    planned.gap_reasons = gap_reasons
    if placements:
        min_c = min(p.column for p in placements.values())
        max_c = max(p.column + box_size(n)[0] - 1 for n, p in placements.items())
        min_r = min(p.row for p in placements.values())
        max_r = max(p.row for p in placements.values())
        planned.box_width = max(1, max_c - min_c + 1 + 2 * policy.group_padding_x)
        planned.box_height = max(1, max_r - min_r + 1 + 2 * policy.group_padding_y)
    return planned


def _depth_of(name: str, snapshot: SemanticSnapshot) -> int:
    depth, current = 0, name
    while snapshot.nodes[current].parent is not None:
        depth += 1
        parent = snapshot.nodes[current].parent
        assert parent is not None
        current = parent
    return depth


def plan_layout(
    snapshot: SemanticSnapshot,
    policy: SemanticPolicy | None = None,
    max_iterations: int = 16,
) -> PlannedLayout:
    """Recursively plan every scope; fail closed on non-convergence."""
    policy = policy or SemanticPolicy()
    scopes: list[str | None] = [None]
    groups = sorted(
        (name for name, node in snapshot.nodes.items() if node.is_group),
        key=lambda n: (_depth_of(n, snapshot), n),
    )
    scopes += groups
    planned: dict[str | None, PlannedScope] = {}
    child_boxes: dict[str, tuple[int, int]] = {}
    for scope in reversed(scopes):
        scoped = plan_scope(scope, snapshot, policy, child_boxes)
        planned[scope] = scoped
        if scope is not None:
            child_boxes[scope] = (scoped.box_width, scoped.box_height)
    for scope in scopes:
        planned[scope] = plan_scope(scope, snapshot, policy, child_boxes)

    diagnostics = _diagnostics(snapshot, planned, policy, fixed_point_iterations=1)
    for iteration in range(2, max_iterations + 1):
        boxes: dict[str, tuple[int, int]] = {
            scope: (planned[scope].box_width, planned[scope].box_height)
            for scope in scopes if scope is not None
        }
        replanned = {scope: plan_scope(scope, snapshot, policy, boxes) for scope in scopes}
        identical = all(replanned[scope].placements == planned[scope].placements for scope in scopes)
        diagnostics["fixed_point_iterations"] = iteration
        if identical:
            break
        planned = replanned
    else:
        boxes = {
            scope: (planned[scope].box_width, planned[scope].box_height)
            for scope in scopes if scope is not None
        }
        final_same = all(
            plan_scope(scope, snapshot, policy, boxes).placements == planned[scope].placements
            for scope in scopes
        )
        if not final_same:
            raise SemanticError("semantic planner did not converge; refusing to write")
    diagnostics = _diagnostics(
        snapshot, planned, policy,
        fixed_point_iterations=diagnostics.get("fixed_point_iterations", 1),
    )
    return PlannedLayout(scopes=planned, diagnostics=diagnostics)


def _diagnostics(
    snapshot: SemanticSnapshot,
    planned: dict[str | None, PlannedScope],
    policy: SemanticPolicy,
    fixed_point_iterations: int,
) -> dict[str, Any]:
    overlap_count = 0
    backbone_violations = 0
    branch_lane_violations = 0
    diagonal_count = 0
    avoidable_diagonal_count = 0
    max_gap_x = 0
    expanded_gaps = 0
    for scope, scoped in planned.items():
        children = set(_children_of(scope, snapshot))
        scope_edge_list = _scope_edges(children, snapshot)
        seen_cells: set[tuple[int, int]] = set()
        for _name, point in scoped.placements.items():
            key = (point.column, point.row)
            if key in seen_cells:
                overlap_count += 1
            seen_cells.add(key)
        backbone = scoped.backbone
        for left, right in zip(backbone, backbone[1:]):
            gap = scoped.placements[right].column - scoped.placements[left].column
            max_gap_x = max(max_gap_x, gap)
            if gap > policy.regular_rail_spacing_x:
                expanded_gaps += 1
            if scoped.placements[right].column <= scoped.placements[left].column:
                backbone_violations += 1
            if scoped.placements[right].row != scoped.placements[left].row:
                backbone_violations += 1
        for edge in scope_edge_list:
            source_pt = scoped.placements.get(edge.source)
            target_pt = scoped.placements.get(edge.target)
            if source_pt is None or target_pt is None:
                continue
            same_row = source_pt.row == target_pt.row
            same_col = source_pt.column == target_pt.column
            if not same_row and not same_col:
                diagonal_count += 1
                fan_out = sum(1 for e in scope_edge_list if e.source == edge.source)
                fan_in = sum(1 for e in scope_edge_list if e.target == edge.target)
                box_involved = snapshot.nodes[edge.source].is_group or snapshot.nodes[edge.target].is_group
                if fan_out <= 1 and fan_in <= 1 and not box_involved and edge.kind != "mask":
                    avoidable_diagonal_count += 1
        for node in backbone:
            for edge in scope_edge_list:
                if edge.target == node and edge.source not in set(backbone) and edge.kind != "mask":
                    spt = scoped.placements.get(edge.source)
                    tpt = scoped.placements.get(edge.target)
                    if spt is not None and tpt is not None and spt.row > tpt.row:
                        branch_lane_violations += 1
    widths = [s.box_width for s in planned.values()]
    heights = [s.box_height for s in planned.values()]
    return {
        "scope_count": len(planned),
        "backbone_count": sum(1 for s in planned.values() if s.backbone),
        "merge_rail_count": sum(len(s.merge_runs) for s in planned.values()),
        "node_count": len(snapshot.nodes),
        "logical_group_box_count": sum(1 for s in planned.values() if s.scope is not None),
        "max_group_depth": max((_depth_of(n, snapshot) for n in snapshot.nodes), default=0),
        "overlap_count": overlap_count,
        "backbone_order_violation_count": backbone_violations,
        "branch_lane_violation_count": branch_lane_violations,
        "diagonal_edge_count": diagonal_count,
        "avoidable_diagonal_edge_count": avoidable_diagonal_count,
        "expanded_gap_count": expanded_gaps,
        "max_gap_x": max_gap_x,
        "total_width": max(widths, default=0),
        "total_height": max(heights, default=0),
        "fixed_point_iterations": fixed_point_iterations,
    }


@dataclass(frozen=True)
class ArrangeDialogState:
    """Mirrors ARRANGE_DIALOG.md: both checkboxes default OFF."""

    include_unselected: bool = False
    ungroup: bool = False

    @classmethod
    def from_askuser(cls, result: Any) -> "ArrangeDialogState | None":
        """Parse an AskUser style result mapping; None means Cancel."""
        if result is None or result is False:
            return None
        if isinstance(result, dict):
            include = bool(result.get("IncludeUnselected", result.get("include_unselected", False)))
            ungroup = bool(result.get("UngroupFirst", result.get("ungroup", False)))
            return cls(include_unselected=include, ungroup=ungroup)
        raise SemanticError(f"unexpected dialog result: {result!r}")


class ArrangeError(RuntimeError):
    pass


def resolve_arrange_scope(
    all_names: Iterable[str],
    selected_names: Iterable[str] | None,
    include_unselected: bool,
) -> set[str]:
    """Selection scope semantics; fail closed with no silent fallback."""
    selected = {str(name) for name in (selected_names or [])}
    if include_unselected:
        return {str(name) for name in all_names}
    if not selected:
        raise ArrangeError(
            "no nodes selected and include-unselected is OFF; "
            "refusing to arrange the whole comp implicitly"
        )
    return selected


def _grid_to_host(point: GridPoint, origin: tuple[float, float], policy: SemanticPolicy) -> tuple[float, float]:
    return (origin[0] + point.column * policy.cell_x, origin[1] + point.row * policy.cell_y)


def arrange_comp(
    comp: Any,
    include_unselected: bool = False,
    ungroup: bool = False,
    policy: SemanticPolicy | None = None,
    selected_names: Iterable[str] | None = None,
    progress: Any = None,
) -> dict[str, Any]:
    """Arrange the resolved scope on the semantic orthogonal grid.

    Safety contract mirrors tidy_nested_comp: bind, snapshot, pure plan at a
    fixed point, bounded position writes, readback, invariant comparison,
    rollback on mismatch, inside one Undo group. Connections, parameters,
    keyframes, tools, media, and group membership are never changed here.
    """
    from .recursive_groups import (
        FusionHostError,
        _close_enough,
        _collect_tools,
        _edge_signature,
        _find_tool,
        _restore_positions,
        _snapshot,
        _validate_hierarchy,
    )
    from .tidy import _snap_position, _xy_from_pos_table

    if ungroup:
        raise FusionHostError(
            "Ungroup-before-arrange is fail-closed: exact structural restoration "
            "is not yet host-proven on a disposable fixture, so no mutation ran"
        )
    policy = policy or SemanticPolicy()
    def _note(message):
        if progress is not None:
            try:
                progress(message)
            except Exception:
                pass
    frame = getattr(comp, "CurrentFrame", None)
    flow = getattr(frame, "FlowView", None) if frame is not None else None
    if flow is None or not callable(getattr(flow, "GetPosTable", None)) or not callable(
        getattr(flow, "SetPos", None)
    ):
        raise FusionHostError("required Fusion FlowView position API is unavailable")

    _note("snapshot begin")
    try:
        snapshot = _snapshot(comp, flow)
        if not snapshot.tools:
            return {"node_count": 0, "edge_count": 0, "moved_count": 0, "scope_count": 0}
        _note("snapshot tools=" + str(len(snapshot.tools)) + " edges=" + str(len(snapshot.edges)))

        if selected_names is None:
            selected_names = _read_selection(comp, set(snapshot.tools))
        try:
            scope = resolve_arrange_scope(snapshot.tools, selected_names, include_unselected)
        except ArrangeError as exc:
            raise FusionHostError(str(exc)) from exc

        scope = _expand_group_subtree(scope, snapshot.parents)
        groups = _validate_hierarchy(snapshot.tools, snapshot.parents)

        reg_ids = {name: _reg_id_of(snapshot.tools[name]) for name in snapshot.tools}
        semantic = build_snapshot(
            names=snapshot.tools,
            edges=[SemanticEdge(e.source, e.target, e.kind) for e in snapshot.edges],
            reg_ids=reg_ids,
            parents=snapshot.parents,
            group_names=groups,
        )
        _note("plan begin")
        layout = plan_layout(semantic, policy)
        _note("plan scopes=" + str(len(layout.scopes)))
        if layout.diagnostics["overlap_count"]:
            raise FusionHostError("semantic plan has overlapping cells; refusing to write")

        desired: dict[str, tuple[float, float]] = {}
        for _scope_id, scoped in layout.scopes.items():
            members = [n for n in scoped.placements if n in scope]
            if not members:
                continue
            # Canonical anchor: min-of-members drifts when branches sit above the
            # backbone, so anchor to the backbone head (or first member) and snap
            # the origin itself. Reruns then reproduce the origin exactly.
            if scoped.backbone and scoped.backbone[0] in scope:
                canon = scoped.backbone[0]
            else:
                canon = sorted(members)[0]
            canon_grid = scoped.placements[canon]
            canon_pos = snapshot.positions[canon]
            origin = _snap_position(
                canon_pos[0] - canon_grid.column * policy.cell_x,
                canon_pos[1] - canon_grid.row * policy.cell_y,
            )
            for name in members:
                desired[name] = _grid_to_host(scoped.placements[name], origin, policy)
        desired = {name: _snap_position(x, y) for name, (x, y) in desired.items()}
    except FusionHostError:
        raise
    except Exception as exc:
        raise FusionHostError("arrange pre-write failed; nothing was changed: " + str(exc)) from exc
    start_undo, end_undo = getattr(comp, "StartUndo", None), getattr(comp, "EndUndo", None)
    undo = callable(start_undo) and callable(end_undo)
    if undo:
        start_undo("ResolveNodeKit: Arrange")
    try:
        tools = {name: _find_tool(comp, name, snapshot.tools) for name in desired}
        writes = {name: pos for name, pos in desired.items() if not _close_enough(snapshot.positions[name], pos)}
        _note("writes begin " + str(len(writes)))
        for name in sorted(writes):
            flow.SetPos(tools[name], *writes[name])
        mismatch = [
            name
            for name in sorted(writes)
            if not _close_enough(_xy_from_pos_table(flow.GetPosTable(tools[name])), desired[name])
        ]
        if mismatch:
            raise FusionHostError(f"position readback mismatch: " + ", ".join(mismatch[:12]))
        _note("readback begin")
        live_tools, live_parents = _collect_tools(comp)
        if set(live_tools) != set(snapshot.tools) or live_parents != snapshot.parents:
            raise FusionHostError("arrange changed the discovered hierarchy")
        if _edge_signature(_snapshot(comp, flow)) != _edge_signature(snapshot):
            raise FusionHostError("arrange changed node connections")
        _note("verify begin")
    except Exception as exc:
        position_failures = _restore_positions(comp, flow, snapshot)
        if undo:
            end_undo(False)
        if position_failures:
            raise FusionHostError(
                "arrange failed; rollback incomplete for: " + ", ".join(position_failures[:12])
            ) from exc
        if isinstance(exc, FusionHostError):
            raise
        raise FusionHostError(f"arrange failed; original state restored: {exc}") from exc
    else:
        if undo:
            end_undo(True)
    return {
        "node_count": len(snapshot.tools),
        "edge_count": len(snapshot.edges),
        "moved_count": len(writes),
        "scope_count": len(layout.scopes),
        "arranged_count": len(desired),
        "diagnostics": layout.diagnostics,
    }


def _reg_id_of(tool: Any) -> str:
    getter = getattr(tool, "GetAttrs", None)
    if callable(getter):
        try:
            attrs = getter() or {}
            value = attrs.get("TOOLS_RegID") or getattr(tool, "ID", None)
            return str(value) if value else ""
        except Exception:
            return ""
    return str(getattr(tool, "ID", "") or "")


def _read_selection(comp: Any, known: set[str]) -> set[str]:
    """Read the explicit Fusion selection; ambiguous reads yield empty."""
    getter = getattr(comp, "GetToolList", None)
    if not callable(getter):
        return set()
    # Host-measured 2026-09-06: GetToolList(True) filters to selection, but
    # GetToolList(1) returns every tool, so 1 must never be a fallback.
    calls = (lambda: getter(True),)
    for call in calls:
        try:
            result = call()
        except Exception:
            continue
        if result is None:
            continue
        if isinstance(result, dict):
            values: Any = list(result.values())
        else:
            try:
                values = list(result)
            except Exception:
                continue
        names: set[str] = set()
        for tool in values:
            name = getattr(tool, "Name", None)
            if name is None:
                attrs_getter = getattr(tool, "GetAttrs", None)
                try:
                    attrs = attrs_getter() if callable(attrs_getter) else {}
                    name = (attrs or {}).get("TOOLS_Name")
                except Exception:
                    name = None
            if name is not None and str(name) in known:
                names.add(str(name))
        return names
    try:
        result = getter(selected=True)
    except Exception:
        return set()
    if result is None:
        return set()
    return set()


def _expand_group_subtree(scope: set[str], parents: Mapping[str, str | None]) -> set[str]:
    children: dict[str, set[str]] = {}
    for name, parent in parents.items():
        if parent is not None:
            children.setdefault(parent, set()).add(name)
    expanded = set(scope)
    queue = list(scope)
    while queue:
        current = queue.pop(0)
        for child in children.get(current, ()):
            if child not in expanded:
                expanded.add(child)
                queue.append(child)
    return expanded
