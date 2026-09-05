from __future__ import annotations

from dataclasses import dataclass
from math import inf
from typing import Iterable, Mapping


class LayoutError(RuntimeError):
    pass


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    kind: str = "other"


@dataclass(frozen=True)
class LayoutConfig:
    spacing_x: float = 3.0
    spacing_y: float = 1.8
    component_gap: float = 3.6
    crossing_sweeps: int = 4


def _stable_key(node_id: str, original_positions: Mapping[str, tuple[float, float]]) -> tuple[float, str]:
    return (float(original_positions.get(node_id, (0.0, 0.0))[1]), node_id)


def _normalize_edges(node_ids: set[str], edges: Iterable[Edge]) -> list[Edge]:
    seen: set[tuple[str, str]] = set()
    normalized: list[Edge] = []
    for edge in edges:
        if edge.source not in node_ids or edge.target not in node_ids:
            raise LayoutError(f"edge references unknown node: {edge.source!r} -> {edge.target!r}")
        key = (edge.source, edge.target)
        if key in seen:
            continue
        seen.add(key)
        normalized.append(edge)
    return normalized


def _components(node_ids: set[str], parents: Mapping[str, set[str]], children: Mapping[str, set[str]]) -> list[list[str]]:
    unseen = set(node_ids)
    result: list[list[str]] = []
    while unseen:
        start = min(unseen)
        stack = [start]
        unseen.remove(start)
        component: list[str] = []
        while stack:
            current = stack.pop()
            component.append(current)
            neighbors = parents[current] | children[current]
            for neighbor in sorted(neighbors, reverse=True):
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)
        result.append(sorted(component))
    result.sort(key=lambda comp: comp[0])
    return result


def _topological_order(component: list[str], parents: Mapping[str, set[str]], children: Mapping[str, set[str]], original_positions: Mapping[str, tuple[float, float]]) -> list[str]:
    component_set = set(component)
    indegree = {node: len(parents[node] & component_set) for node in component}
    ready = sorted((node for node in component if indegree[node] == 0), key=lambda n: _stable_key(n, original_positions))
    order: list[str] = []
    while ready:
        current = ready.pop(0)
        order.append(current)
        for child in sorted(children[current] & component_set, key=lambda n: _stable_key(n, original_positions)):
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
                ready.sort(key=lambda n: _stable_key(n, original_positions))
    if len(order) != len(component):
        cyclic = sorted(node for node in component if indegree[node] > 0)
        raise LayoutError(f"cycle detected; refusing to move nodes: {', '.join(cyclic[:12])}")
    return order


def _barycenter(neighbors: set[str], positions: Mapping[str, int]) -> float:
    values = [positions[n] for n in neighbors if n in positions]
    if not values:
        return inf
    return sum(values) / len(values)


def layout_graph(node_ids: Iterable[str], edges: Iterable[Edge], original_positions: Mapping[str, tuple[float, float]] | None = None, config: LayoutConfig | None = None) -> dict[str, tuple[float, float]]:
    """Return deterministic relative positions for a directed acyclic node graph.

    The function is host-agnostic and mutates nothing. Disconnected and isolated nodes are
    included as separate components so later host writes cannot collide with them.
    """
    config = config or LayoutConfig()
    original_positions = original_positions or {}
    node_set = {str(node_id) for node_id in node_ids}
    if not node_set:
        return {}
    normalized_edges = _normalize_edges(node_set, edges)
    parents = {node: set() for node in node_set}
    children = {node: set() for node in node_set}
    for edge in normalized_edges:
        parents[edge.target].add(edge.source)
        children[edge.source].add(edge.target)
    output: dict[str, tuple[float, float]] = {}
    component_y = 0.0
    for component in _components(node_set, parents, children):
        order = _topological_order(component, parents, children, original_positions)
        component_set = set(component)
        rank = {node: 0 for node in component}
        for node in order:
            upstream = parents[node] & component_set
            if upstream:
                rank[node] = max(rank[parent] + 1 for parent in upstream)
        max_rank = max(rank.values(), default=0)
        ranks: dict[int, list[str]] = {r: [] for r in range(max_rank + 1)}
        for node in component:
            ranks[rank[node]].append(node)
        for r in ranks:
            ranks[r].sort(key=lambda n: _stable_key(n, original_positions))
        for _ in range(max(0, config.crossing_sweeps)):
            for r in range(1, max_rank + 1):
                previous_index = {node: idx for idx, node in enumerate(ranks[r - 1])}
                prior_order = {node: idx for idx, node in enumerate(ranks[r])}
                ranks[r].sort(key=lambda node: (_barycenter(parents[node], previous_index), prior_order[node], _stable_key(node, original_positions)))
            for r in range(max_rank - 1, -1, -1):
                next_index = {node: idx for idx, node in enumerate(ranks[r + 1])}
                prior_order = {node: idx for idx, node in enumerate(ranks[r])}
                ranks[r].sort(key=lambda node: (_barycenter(children[node], next_index), prior_order[node], _stable_key(node, original_positions)))
        local_positions: dict[str, tuple[float, float]] = {}
        min_y = inf
        max_y = -inf
        for r in range(max_rank + 1):
            nodes = ranks[r]
            center = (len(nodes) - 1) / 2.0
            for idx, node in enumerate(nodes):
                x = r * config.spacing_x
                y = (idx - center) * config.spacing_y
                local_positions[node] = (x, y)
                min_y = min(min_y, y)
                max_y = max(max_y, y)
        if min_y == inf:
            min_y = max_y = 0.0
        shift_y = component_y - min_y
        for node, (x, y) in local_positions.items():
            output[node] = (x, y + shift_y)
        component_height = max_y - min_y
        component_y += component_height + config.component_gap
    return output
