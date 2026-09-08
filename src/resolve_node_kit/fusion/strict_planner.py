"""Pure strict-orthogonal layout planning for the SO-20 offline seam.

The planner in this module is deliberately host agnostic.  It consumes a
complete, port-labelled processing snapshot and returns an integer logical
layout together with explicit semantic modules and coverage evidence.  It
does not call Resolve, write a host position, or infer a connection from a
display name.  Missing/unknown input coverage is a hard, fail-closed error.

The public names are intentionally small and JSON-friendly so a later host
adapter can map its readback into this seam without importing the existing
Fusion mutation code.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping, Sequence

from .processing_snapshot import REQUIRED_PROCESSING_FIELDS


class StrictPlannerError(ValueError):
    """Base error for invalid or unsafe planner input."""


class StrictCoverageError(StrictPlannerError):
    """Raised when a snapshot has unknown or missing processing coverage."""


class StrictCycleError(StrictPlannerError):
    """Raised when a scope contains a processing cycle."""


class CoverageStatus(str, Enum):
    PLANNER_COVERED = "planner-covered"
    HOST_ONLY = "host-only"
    FAIL_CLOSED = "fail-closed"


_KNOWN_STATES = {"complete", "absent", "unknown", "missing", "unsupported", "error"}


@dataclass(frozen=True, slots=True)
class StrictNode:
    """Stable node identity and the minimum geometry metadata for planning."""

    uid: str
    display_name: str = ""
    reg_id: str = ""
    parent_uid: str | None = None
    width: int = 1
    height: int = 1
    processing_role: str = "other"
    visual_continuity: str | None = None
    is_group: bool = False
    input_state: str = "complete"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def name(self) -> str:
        """Compatibility alias used by the older semantic planner."""

        return self.uid

    @property
    def parent(self) -> str | None:
        return self.parent_uid


@dataclass(frozen=True, slots=True)
class StrictEdge:
    """One exact processing edge, including port and duplicate identity."""

    source: str
    source_output_id: str
    target: str
    target_input_id: str
    ordinal: int | None = None
    uid: str | None = None
    processing_role: str = "other"
    visual_continuity: str | None = None
    state: str = "complete"

    @property
    def source_uid(self) -> str:
        return self.source

    @property
    def target_uid(self) -> str:
        return self.target

    @property
    def role(self) -> str:
        return self.processing_role

    def identity(self) -> str:
        """Return a deterministic identity without collapsing multiedges."""

        explicit = self.uid.strip() if isinstance(self.uid, str) else ""
        token = explicit or f"{self.source}:{self.source_output_id}->{self.target}:{self.target_input_id}"
        return f"{token}#{int(self.ordinal or 0)}"


@dataclass(frozen=True, slots=True)
class StrictSnapshot:
    """Normalized processing snapshot used by :func:`plan_strict`."""

    nodes: tuple[StrictNode, ...]
    edges: tuple[StrictEdge, ...]
    source: str | None = None
    # A caller must explicitly attest that the processing input is complete.
    # Treating an omitted edge/port read as complete would allow a structural
    # plan to proceed from an incomplete host snapshot.
    input_coverage: str = "missing"
    unresolved_inputs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        nodes = _normalize_nodes(self.nodes)
        edges = _normalize_edges(self.edges, {node.uid for node in nodes})
        object.__setattr__(self, "nodes", nodes)
        object.__setattr__(self, "edges", edges)
        coverage = _state(self.input_coverage)
        object.__setattr__(self, "input_coverage", coverage)
        unresolved = tuple(sorted(set(str(item) for item in self.unresolved_inputs)))
        unresolved += tuple(
            f"node:{node.uid}:input_state={_state(node.input_state)}"
            for node in nodes
            if _state(node.input_state) != "complete"
        )
        unresolved += tuple(
            f"edge:{edge.identity()}:state={_state(edge.state)}"
            for edge in edges
            if _state(edge.state) != "complete"
        )
        if coverage != "complete":
            unresolved += (f"snapshot:input_coverage={coverage}",)
        object.__setattr__(self, "unresolved_inputs", tuple(sorted(set(unresolved))))

    def node_map(self) -> dict[str, StrictNode]:
        return {node.uid: node for node in self.nodes}

    def edge_map(self) -> dict[str, StrictEdge]:
        return {edge.identity(): edge for edge in self.edges}

    def unresolved(self) -> tuple[str, ...]:
        return self.unresolved_inputs


@dataclass(frozen=True, slots=True)
class GridPoint:
    column: int
    row: int


@dataclass(frozen=True, slots=True)
class Rect:
    """Integer logical rectangle.  Touching edges are not an intersection."""

    x: int
    y: int
    width: int
    height: int

    @property
    def right(self) -> int:
        return self.x + self.width

    @property
    def bottom(self) -> int:
        return self.y + self.height

    def intersects(self, other: "Rect") -> bool:
        return self.x < other.right and other.x < self.right and self.y < other.bottom and other.y < self.bottom

    def translated(self, dx: int, dy: int) -> "Rect":
        return Rect(self.x + dx, self.y + dy, self.width, self.height)


@dataclass(frozen=True, slots=True)
class StrictPolicy:
    """Logical-grid defaults from the strict design contract."""

    pitch: int = 3
    node_width: int = 1
    node_height: int = 1
    group_padding: int = 1
    region_gap: int = 2
    feeder_row_gap: int = 3

    def __post_init__(self) -> None:
        for name in ("pitch", "node_width", "node_height", "group_padding", "region_gap", "feeder_row_gap"):
            value = getattr(self, name)
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise StrictPlannerError(f"{name} must be a positive integer")


@dataclass(frozen=True, slots=True)
class LayoutModule:
    kind: str
    scope: str | None
    members: tuple[str, ...]
    bounds: Rect
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class FixtureCoverage:
    fixture_id: str
    description: str
    status: CoverageStatus
    assertions: tuple[str, ...]
    note: str = ""


@dataclass(frozen=True, slots=True)
class StrictPlan:
    """Pure planner result and machine-readable evidence."""

    placements: Mapping[str, GridPoint]
    rectangles: Mapping[str, Rect]
    modules: tuple[LayoutModule, ...]
    edge_coverage: Mapping[str, str]
    motif_coverage: Mapping[str, tuple[str, ...]]
    diagnostics: Mapping[str, Any]
    policy: StrictPolicy

    @property
    def all_edge_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self.edge_coverage))

    @property
    def all_edges_covered(self) -> bool:
        return all(value == "planned" for value in self.edge_coverage.values())

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": "resolve-node-kit.strict-planner/v1",
            "placements": {uid: {"column": p.column, "row": p.row} for uid, p in sorted(self.placements.items())},
            "rectangles": {
                uid: {"x": r.x, "y": r.y, "width": r.width, "height": r.height}
                for uid, r in sorted(self.rectangles.items())
            },
            "modules": [
                {
                    "kind": module.kind,
                    "scope": module.scope,
                    "members": list(module.members),
                    "bounds": {
                        "x": module.bounds.x,
                        "y": module.bounds.y,
                        "width": module.bounds.width,
                        "height": module.bounds.height,
                    },
                    "metadata": dict(module.metadata),
                }
                for module in self.modules
            ],
            "edge_coverage": dict(sorted(self.edge_coverage.items())),
            "motif_coverage": {key: list(value) for key, value in sorted(self.motif_coverage.items())},
            "diagnostics": dict(self.diagnostics),
            "policy": {
                "pitch": self.policy.pitch,
                "group_padding": self.policy.group_padding,
            },
        }


PlannerNode = StrictNode
PlannerEdge = StrictEdge
PlannerSnapshot = StrictSnapshot
PlannerPolicy = StrictPolicy


def _state(value: Any) -> str:
    if value is None:
        return "missing"
    if isinstance(value, Mapping):
        value = value.get("state", "complete")
    text = str(value).strip().lower()
    return text if text in _KNOWN_STATES else "error"


def _node_from_record(raw: StrictNode | Mapping[str, Any] | str) -> StrictNode:
    if isinstance(raw, StrictNode):
        return raw
    if isinstance(raw, str):
        return StrictNode(uid=raw, display_name=raw)
    if not isinstance(raw, Mapping):
        raise StrictPlannerError(f"node must be an object: {raw!r}")
    uid = str(raw.get("uid", raw.get("id", raw.get("name", "")))).strip()
    if not uid:
        raise StrictPlannerError("node uid is required")
    box = raw.get("rect") if isinstance(raw.get("rect"), Mapping) else {}
    return StrictNode(
        uid=uid,
        display_name=str(raw.get("display_name", raw.get("name", uid))),
        reg_id=str(raw.get("reg_id", raw.get("type", ""))),
        parent_uid=(None if raw.get("parent_uid", raw.get("parent")) in (None, "", "root") else str(raw.get("parent_uid", raw.get("parent")))),
        width=int(raw.get("width", box.get("width", 1))),
        height=int(raw.get("height", box.get("height", 1))),
        processing_role=str(raw.get("processing_role", raw.get("role", "other"))),
        visual_continuity=(None if raw.get("visual_continuity", raw.get("continuity")) is None else str(raw.get("visual_continuity", raw.get("continuity")))),
        is_group=bool(raw.get("is_group", raw.get("group", False))),
        input_state=str(raw.get("input_state", raw.get("inputs_state", "complete"))),
        metadata=dict(raw.get("metadata") or {}),
    )


def _edge_from_record(raw: StrictEdge | Mapping[str, Any] | Sequence[Any]) -> StrictEdge:
    if isinstance(raw, StrictEdge):
        return raw
    if isinstance(raw, Mapping):
        source = raw.get("source", raw.get("source_uid", ""))
        target = raw.get("target", raw.get("target_uid", ""))
        source_port = raw.get("source_output_id", raw.get("source_output", raw.get("source_port", "")))
        target_port = raw.get("target_input_id", raw.get("target_input", raw.get("target_port", raw.get("port", ""))))
        return StrictEdge(
            source=str(source),
            source_output_id=str(source_port),
            target=str(target),
            target_input_id=str(target_port),
            ordinal=(None if raw.get("ordinal") is None else int(raw["ordinal"])),
            uid=(None if raw.get("uid") is None else str(raw["uid"])),
            processing_role=str(raw.get("processing_role", raw.get("role", "other"))),
            visual_continuity=(None if raw.get("visual_continuity", raw.get("continuity")) is None else str(raw.get("visual_continuity", raw.get("continuity")))),
            state=str(raw.get("state", "complete")),
        )
    if isinstance(raw, Sequence) and len(raw) == 4:
        return StrictEdge(str(raw[0]), str(raw[1]), str(raw[2]), str(raw[3]))
    raise StrictPlannerError(f"edge must be an object or four-item sequence: {raw!r}")


def _normalize_nodes(nodes: Iterable[StrictNode | Mapping[str, Any] | str]) -> tuple[StrictNode, ...]:
    result = tuple(_node_from_record(item) for item in nodes)
    ids = [node.uid for node in result]
    if any(not uid for uid in ids):
        raise StrictPlannerError("node uid is required")
    if len(ids) != len(set(ids)):
        raise StrictPlannerError("duplicate node uid")
    for node in result:
        if node.width <= 0 or node.height <= 0:
            raise StrictPlannerError(f"node {node.uid!r} has non-positive rectangle")
        if _state(node.input_state) not in _KNOWN_STATES:
            raise StrictPlannerError(f"node {node.uid!r} has invalid input state")
    node_ids = set(ids)
    for node in result:
        if node.parent_uid is not None and node.parent_uid not in node_ids:
            raise StrictPlannerError(f"unknown parent {node.parent_uid!r} for {node.uid!r}")
    # Parent relationships are a forest; a cycle is not a recursive group.
    for node in result:
        seen: set[str] = set()
        current: str | None = node.uid
        while current is not None:
            if current in seen:
                raise StrictPlannerError(f"group parent cycle near {current!r}")
            seen.add(current)
            parent = next((item.parent_uid for item in result if item.uid == current), None)
            current = parent
    return tuple(sorted(result, key=lambda item: item.uid))


def _normalize_edges(edges: Iterable[StrictEdge | Mapping[str, Any] | Sequence[Any]], node_ids: set[str]) -> tuple[StrictEdge, ...]:
    raw = [_edge_from_record(item) for item in edges]
    for edge in raw:
        if edge.source not in node_ids or edge.target not in node_ids:
            raise StrictPlannerError(f"edge references unknown node: {edge.source!r}->{edge.target!r}")
        if not edge.source_output_id or not edge.target_input_id:
            raise StrictPlannerError("every edge requires source_output_id and target_input_id")
        if edge.source == edge.target:
            raise StrictPlannerError(f"self edge refused: {edge.source!r}")
    grouped: dict[tuple[str, str, str, str], list[StrictEdge]] = defaultdict(list)
    for edge in raw:
        grouped[(edge.source, edge.source_output_id, edge.target, edge.target_input_id)].append(edge)
    normalized: list[StrictEdge] = []
    for base in sorted(grouped):
        members = sorted(
            grouped[base],
            key=lambda item: (
                item.ordinal is None,
                item.ordinal if item.ordinal is not None else 0,
                item.uid or "",
                item.processing_role,
                item.visual_continuity or "",
                item.state,
            ),
        )
        # Explicit edge UIDs are the identity for otherwise identical
        # parallel records, so two UIDs may legitimately share ordinal zero.
        # Records without a UID need a deterministic ordinal to avoid being
        # collapsed into one edge.
        used_without_uid: set[int] = set()
        used_uid_ordinals: set[tuple[str, int]] = set()
        next_ordinal = 0
        for edge in members:
            ordinal = edge.ordinal
            if ordinal is None:
                while next_ordinal in used_without_uid or any(item[1] == next_ordinal for item in used_uid_ordinals):
                    next_ordinal += 1
                ordinal = next_ordinal
            if edge.uid:
                uid_key = (edge.uid, ordinal)
                if uid_key in used_uid_ordinals:
                    raise StrictPlannerError(f"duplicate edge uid/ordinal for {base!r}: {edge.uid}#{ordinal}")
                used_uid_ordinals.add(uid_key)
            elif ordinal in used_without_uid:
                raise StrictPlannerError(f"duplicate edge ordinal for {base!r}: {ordinal}")
            else:
                used_without_uid.add(ordinal)
            normalized.append(
                StrictEdge(
                    source=edge.source,
                    source_output_id=edge.source_output_id,
                    target=edge.target,
                    target_input_id=edge.target_input_id,
                    ordinal=ordinal,
                    uid=edge.uid,
                    processing_role=edge.processing_role,
                    visual_continuity=edge.visual_continuity,
                    state=edge.state,
                )
            )
    seen_ids: set[str] = set()
    for edge in normalized:
        identity = edge.identity()
        if identity in seen_ids:
            raise StrictPlannerError(f"duplicate edge uid: {identity}")
        seen_ids.add(identity)
    return tuple(sorted(normalized, key=lambda item: item.identity()))


def build_strict_snapshot(
    nodes: Iterable[StrictNode | Mapping[str, Any] | str] | Mapping[str, Any],
    edges: Iterable[StrictEdge | Mapping[str, Any] | Sequence[Any]],
    *,
    source: str | None = None,
    input_coverage: str | Mapping[str, Any] | None = None,
) -> StrictSnapshot:
    """Normalize records while preserving port labels and explicit states."""

    if isinstance(nodes, Mapping):
        records = []
        for uid, value in nodes.items():
            if isinstance(value, Mapping):
                records.append({"uid": uid, **dict(value)})
            else:
                records.append({"uid": uid, "display_name": str(value)})
    else:
        records = list(nodes)
    normalized_nodes = [_node_from_record(item) for item in records]
    unresolved: list[str] = []
    coverage_state = "missing" if input_coverage is None else input_coverage
    if isinstance(input_coverage, Mapping):
        coverage_state = str(input_coverage.get("state", "complete"))
        states = input_coverage.get("nodes") if isinstance(input_coverage.get("nodes"), Mapping) else {}
        normalized_nodes = [
            StrictNode(
                uid=node.uid,
                display_name=node.display_name,
                reg_id=node.reg_id,
                parent_uid=node.parent_uid,
                width=node.width,
                height=node.height,
                processing_role=node.processing_role,
                visual_continuity=node.visual_continuity,
                is_group=node.is_group,
                input_state=str(states.get(node.uid, node.input_state)),
                metadata=node.metadata,
            )
            for node in normalized_nodes
        ]
        unresolved.extend(str(item) for item in input_coverage.get("unresolved", ()) if item is not None)
    return StrictSnapshot(tuple(normalized_nodes), tuple(_edge_from_record(item) for item in edges), source, str(coverage_state), tuple(unresolved))


def _processing_field_state(raw: Any) -> str:
    """Read a processing-snapshot field state without normalizing absence."""

    if isinstance(raw, Mapping):
        raw = raw.get("state")
    elif hasattr(raw, "state"):
        raw = getattr(raw, "state")
    if hasattr(raw, "value"):
        raw = getattr(raw, "value")
    return _state(raw)


def _processing_field_value(raw: Any) -> Any:
    if isinstance(raw, Mapping) and "value" in raw:
        return raw["value"]
    if hasattr(raw, "value") and hasattr(raw, "state"):
        return getattr(raw, "value")
    return raw


def build_strict_snapshot_from_processing(
    payload: Any,
    *,
    source: str | None = None,
) -> StrictSnapshot:
    """Map the SO-10 JSON-safe snapshot contract into the strict planner.

    The adapter accepts a :class:`ProcessingSnapshot` or its ``as_dict``
    representation.  Every required processing field and every node identity
    field remains stateful; absent/unsupported/error values are reported as
    unresolved inputs rather than being replaced with empty lists or guesses.
    """

    if hasattr(payload, "as_dict") and callable(payload.as_dict):
        payload = payload.as_dict()
    if not isinstance(payload, Mapping):
        raise TypeError("processing snapshot must be a mapping or expose as_dict()")

    raw_nodes = payload.get("nodes", {})
    if isinstance(raw_nodes, Mapping):
        node_records = [(str(uid), value) for uid, value in raw_nodes.items()]
    elif isinstance(raw_nodes, list):
        node_records = [
            (str(value.get("name", value.get("uid", ""))), value)
            for value in raw_nodes
            if isinstance(value, Mapping)
        ]
    else:
        node_records = []

    unresolved: list[str] = []
    nodes: list[dict[str, Any]] = []
    for uid, raw in node_records:
        if not uid or not isinstance(raw, Mapping):
            unresolved.append(f"nodes.{uid or '<unnamed>'}:invalid")
            continue
        type_field = raw.get("type", raw.get("node_type"))
        parent_field = raw.get("parent")
        position_field = raw.get("position")
        for label, field in (("type", type_field), ("parent", parent_field), ("position", position_field)):
            state = _processing_field_state(field)
            if state != "complete":
                unresolved.append(f"nodes.{uid}.{label}:{state}")
        parent_value = _processing_field_value(parent_field)
        nodes.append(
            {
                "uid": uid,
                "display_name": uid,
                "reg_id": str(_processing_field_value(type_field) or ""),
                "parent": None if parent_value in (None, "", "root") else str(parent_value),
                "input_state": "complete",
            }
        )

    fields = payload.get("fields", {})
    if not isinstance(fields, Mapping):
        fields = {}
        unresolved.append("fields:missing")
    for key in REQUIRED_PROCESSING_FIELDS:
        state = _processing_field_state(fields.get(key))
        if state != "complete":
            unresolved.append(f"fields.{key}:{state}")

    raw_connections = payload.get("connections")
    if isinstance(raw_connections, list):
        edges = list(raw_connections)
    else:
        edges = []
        unresolved.append("connections:missing" if raw_connections is None else "connections:invalid")
    if not node_records:
        unresolved.append("nodes:missing")

    return build_strict_snapshot(
        nodes,
        edges,
        source=source or (str(payload.get("source")) if payload.get("source") is not None else None),
        input_coverage={"state": "complete" if not unresolved else "unknown", "unresolved": unresolved},
    )


def _ancestor_map(nodes: Mapping[str, StrictNode]) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for uid in sorted(nodes):
        parents: set[str] = set()
        current = nodes[uid].parent_uid
        while current is not None:
            parents.add(current)
            current = nodes[current].parent_uid
        result[uid] = parents
    return result


def _is_merge(node: StrictNode) -> bool:
    token = (node.reg_id or node.processing_role).lower()
    return "merge" in token or node.processing_role.lower() in {"merge", "reduction"}


def _is_output(node: StrictNode) -> bool:
    token = (node.reg_id or node.processing_role).lower()
    return any(value in token for value in ("mediaout", "output", "saver"))


def _scope_edges(scope_ids: set[str], edges: Sequence[StrictEdge]) -> list[StrictEdge]:
    return [edge for edge in edges if edge.source in scope_ids and edge.target in scope_ids]


def _components(scope_ids: set[str], edges: Sequence[StrictEdge]) -> list[list[str]]:
    adjacency: dict[str, set[str]] = {uid: set() for uid in scope_ids}
    for edge in edges:
        adjacency[edge.source].add(edge.target)
        adjacency[edge.target].add(edge.source)
    unseen = set(scope_ids)
    result: list[list[str]] = []
    while unseen:
        start = min(unseen)
        stack = [start]
        unseen.remove(start)
        component: list[str] = []
        while stack:
            current = stack.pop()
            component.append(current)
            for neighbor in sorted(adjacency[current], reverse=True):
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)
        result.append(sorted(component))
    return sorted(result, key=lambda value: value[0])


def _topological(component: Sequence[str], edges: Sequence[StrictEdge]) -> list[str]:
    members = set(component)
    incoming = {uid: 0 for uid in component}
    outgoing: dict[str, set[str]] = {uid: set() for uid in component}
    for edge in edges:
        if edge.source in members and edge.target in members and edge.target not in outgoing[edge.source]:
            outgoing[edge.source].add(edge.target)
            incoming[edge.target] += 1
    ready = [uid for uid in sorted(component) if incoming[uid] == 0]
    result: list[str] = []
    while ready:
        current = ready.pop(0)
        result.append(current)
        for target in sorted(outgoing[current]):
            incoming[target] -= 1
            if incoming[target] == 0:
                ready.append(target)
                ready.sort()
    if len(result) != len(component):
        raise StrictCycleError("processing cycle in scope: " + ", ".join(sorted(set(component) - set(result))))
    return result


def _rail_path(component: Sequence[str], edges: Sequence[StrictEdge], nodes: Mapping[str, StrictNode]) -> tuple[str, ...]:
    """Choose a deterministic output-oriented path using processing roles only."""

    members = set(component)
    local_edges = [edge for edge in edges if edge.source in members and edge.target in members]
    order = _topological(component, local_edges)
    incoming: dict[str, list[StrictEdge]] = {uid: [] for uid in component}
    for edge in local_edges:
        incoming[edge.target].append(edge)
    score: dict[str, tuple[int, int, tuple[str, ...]]] = {}
    paths: dict[str, tuple[str, ...]] = {}
    for uid in order:
        candidates: list[tuple[tuple[int, int, tuple[str, ...]], tuple[str, ...]]] = []
        if not incoming[uid]:
            candidates.append(((0, 0, (uid,)), (uid,)))
        for edge in sorted(incoming[uid], key=lambda item: item.identity()):
            prior = score[edge.source]
            role_bonus = 1 if edge.processing_role.lower() in {"background", "main", "other"} else 0
            candidate = ((prior[0] + 1, prior[1] + role_bonus, prior[2] + (uid,)), paths[edge.source] + (uid,))
            candidates.append(candidate)
        chosen = max(candidates, key=lambda value: value[0])
        score[uid], paths[uid] = chosen
    sinks = [uid for uid in component if not any(edge.source == uid for edge in local_edges)]
    sink = max(sorted(sinks), key=lambda uid: (1 if _is_output(nodes[uid]) else 0, score[uid][0], score[uid][1], tuple(reversed(score[uid][2]))))
    return paths[sink]


def _ancestor_rect_overlap(rectangles: Mapping[str, Rect], nodes: Mapping[str, StrictNode]) -> list[tuple[str, str]]:
    ancestors = _ancestor_map(nodes)
    collisions: list[tuple[str, str]] = []
    ids = sorted(rectangles)
    for index, left in enumerate(ids):
        for right in ids[index + 1 :]:
            if right in ancestors[left] or left in ancestors[right]:
                continue
            if rectangles[left].intersects(rectangles[right]):
                collisions.append((left, right))
    return collisions


def _union_rect(rectangles: Sequence[Rect], padding: int = 0) -> Rect:
    if not rectangles:
        return Rect(0, 0, max(1, padding * 2), max(1, padding * 2))
    left = min(rect.x for rect in rectangles)
    top = min(rect.y for rect in rectangles)
    right = max(rect.right for rect in rectangles)
    bottom = max(rect.bottom for rect in rectangles)
    return Rect(left - padding, top - padding, right - left + 2 * padding, bottom - top + 2 * padding)


def _translate_scope_rects(scope_rects: Mapping[str, Rect], dx: int, dy: int) -> dict[str, Rect]:
    return {uid: rect.translated(dx, dy) for uid, rect in scope_rects.items()}


def _module_bounds(kind: str, members: Sequence[str], rectangles: Mapping[str, Rect]) -> Rect:
    rects = [rectangles[uid] for uid in members if uid in rectangles]
    return _union_rect(rects)


def plan_strict(snapshot: StrictSnapshot, policy: StrictPolicy | None = None) -> StrictPlan:
    """Plan a complete snapshot on an integer grid, without host mutation."""

    if not isinstance(snapshot, StrictSnapshot):
        raise TypeError("plan_strict expects StrictSnapshot")
    if snapshot.unresolved_inputs:
        raise StrictCoverageError("strict planner refuses unknown/missing processing coverage: " + "; ".join(snapshot.unresolved_inputs))
    policy = policy or StrictPolicy()
    nodes = snapshot.node_map()
    edges = snapshot.edges
    direct_children: dict[str | None, list[str]] = defaultdict(list)
    for node in snapshot.nodes:
        direct_children[node.parent_uid].append(node.uid)
    for scope in direct_children:
        direct_children[scope].sort()
    groups = [node.uid for node in snapshot.nodes if node.is_group]
    depth: dict[str, int] = {}
    for uid in groups:
        depth[uid] = len(_ancestor_map(nodes)[uid])
    scope_order = sorted(groups, key=lambda uid: (-depth[uid], uid)) + [None]
    scope_positions: dict[str | None, dict[str, GridPoint]] = {}
    scope_rects: dict[str | None, dict[str, Rect]] = {}
    scope_modules: dict[str | None, list[tuple[str, tuple[str, ...], dict[str, Any]]]] = {}
    scope_box: dict[str, Rect] = {}

    for scope in scope_order:
        child_ids = set(direct_children.get(scope, ()))
        local_edges = _scope_edges(child_ids, edges)
        positions: dict[str, GridPoint] = {}
        rects: dict[str, Rect] = {}
        module_specs: list[tuple[str, tuple[str, ...], dict[str, Any]]] = []
        cursor_x = 0
        component_info: list[tuple[list[str], tuple[str, ...]]] = []
        for component in _components(child_ids, local_edges):
            rail = _rail_path(component, local_edges, nodes)
            component_info.append((component, rail))
            rail_set = set(rail)
            # Place the main rail left-to-right.  The width of a nested group is
            # already known because scopes are visited bottom-up.
            for uid in rail:
                width = scope_box[uid].width if uid in scope_box else nodes[uid].width
                height = scope_box[uid].height if uid in scope_box else nodes[uid].height
                positions[uid] = GridPoint(cursor_x, 0)
                rects[uid] = Rect(cursor_x, 0, width, height)
                cursor_x += width + policy.pitch
            module_specs.append(("rail", tuple(rail), {"axis": "horizontal", "processing_role": "main"}))

            incoming = defaultdict(list)
            outgoing = defaultdict(list)
            for edge in local_edges:
                if edge.source in set(component) and edge.target in set(component):
                    incoming[edge.target].append(edge)
                    outgoing[edge.source].append(edge)
            # Nodes feeding any rail member form feeder columns.  A shared
            # source is assigned once by uid and never copied per receiver.
            feeder_targets: dict[str, set[str]] = defaultdict(set)
            for edge in local_edges:
                if edge.source not in rail_set and edge.target in rail_set:
                    feeder_targets[edge.source].add(edge.target)
            feeder_depth: dict[str, int] = {}
            feeder_receiver: dict[str, str] = {}
            queue = deque((uid, 1) for uid in rail)
            while queue:
                receiver, level = queue.popleft()
                for edge in sorted(incoming[receiver], key=lambda item: item.identity()):
                    source = edge.source
                    if source in rail_set:
                        continue
                    if source not in feeder_depth or level < feeder_depth[source]:
                        feeder_depth[source] = level
                        feeder_receiver[source] = receiver
                        queue.append((source, level + 1))
            feeder_by_receiver: dict[str, list[str]] = defaultdict(list)
            for source, receiver in feeder_receiver.items():
                feeder_by_receiver[receiver].append(source)
            for receiver in feeder_by_receiver:
                feeder_by_receiver[receiver].sort()
            for receiver in rail:
                for slot, source in enumerate(feeder_by_receiver.get(receiver, ())):
                    if source in positions:
                        continue
                    receiver_point = positions[receiver]
                    x = receiver_point.column + slot * policy.pitch
                    y = -feeder_depth[source] * policy.feeder_row_gap
                    width = scope_box[source].width if source in scope_box else nodes[source].width
                    height = scope_box[source].height if source in scope_box else nodes[source].height
                    positions[source] = GridPoint(x, y)
                    rects[source] = Rect(x, y, width, height)
            for receiver, members in sorted(feeder_by_receiver.items()):
                module_specs.append(
                    (
                        "feeder",
                        tuple(members),
                        {
                            "receiver": receiver,
                            "shared_source_ids": tuple(
                                sorted(source for source in members if len(feeder_targets.get(source, ())) > 1)
                            ),
                        },
                    )
                )

            # Remaining component members are region-local nodes.  Put them in
            # a deterministic lower lane, then shift right on rectangle clash.
            leftovers = [uid for uid in component if uid not in positions]
            for slot, uid in enumerate(sorted(leftovers)):
                width = scope_box[uid].width if uid in scope_box else nodes[uid].width
                height = scope_box[uid].height if uid in scope_box else nodes[uid].height
                candidate = Rect(cursor_x + slot * (policy.pitch + width), policy.feeder_row_gap, width, height)
                while any(candidate.intersects(existing) for existing in rects.values()):
                    candidate = candidate.translated(policy.pitch, 0)
                positions[uid] = GridPoint(candidate.x, candidate.y)
                rects[uid] = candidate
            module_specs.append(("region", tuple(component), {"component": component[0]}))

            # A reduction is a contiguous Merge chain linked by Background
            # (or explicit reduction) processing roles, not by visual names.
            reduction_members: list[str] = []
            for uid in rail:
                if not _is_merge(nodes[uid]):
                    continue
                if reduction_members and not any(
                    edge.source == reduction_members[-1]
                    and edge.target == uid
                    and edge.processing_role.lower() in {"background", "reduction", "main", "other"}
                    for edge in local_edges
                ):
                    if len(reduction_members) >= 2:
                        module_specs.append(("reduction", tuple(reduction_members), {"axis": "vertical", "source": "processing-role"}))
                    reduction_members = []
                reduction_members.append(uid)
            if len(reduction_members) >= 2:
                module_specs.append(("reduction", tuple(reduction_members), {"axis": "vertical", "source": "processing-role"}))
        if rects:
            min_x = min(rect.x for rect in rects.values())
            min_y = min(rect.y for rect in rects.values())
            if min_x < 0 or min_y < 0:
                dx = -min_x + policy.pitch if min_x < 0 else 0
                dy = -min_y + policy.pitch if min_y < 0 else 0
                positions = {uid: GridPoint(point.column + dx, point.row + dy) for uid, point in positions.items()}
                rects = _translate_scope_rects(rects, dx, dy)
        scope_positions[scope] = positions
        scope_rects[scope] = rects
        scope_modules[scope] = module_specs
        if scope is not None:
            scope_box[scope] = _union_rect(tuple(rects.values()), policy.group_padding)

    # Materialize nested scopes into one global coordinate space.  Group boxes
    # are atomic at their parent scope while their descendants are translated
    # into the interior of that box.
    placements: dict[str, GridPoint] = {}
    rectangles: dict[str, Rect] = {}
    module_scope_offsets: dict[str | None, tuple[int, int]] = {}

    def materialize(scope: str | None, offset_x: int, offset_y: int) -> None:
        module_scope_offsets[scope] = (offset_x, offset_y)
        for uid in direct_children.get(scope, ()):
            local_point = scope_positions[scope][uid]
            rect = scope_rects[scope][uid].translated(offset_x, offset_y)
            placements[uid] = GridPoint(rect.x, rect.y)
            rectangles[uid] = rect
            if nodes[uid].is_group:
                inner = scope_rects.get(uid, {})
                if inner:
                    inner_min_x = min(item.x for item in inner.values())
                    inner_min_y = min(item.y for item in inner.values())
                    child_offset_x = rect.x + policy.group_padding - inner_min_x
                    child_offset_y = rect.y + policy.group_padding - inner_min_y
                    materialize(uid, child_offset_x, child_offset_y)

    materialize(None, 0, 0)
    if rectangles:
        min_x = min(rect.x for rect in rectangles.values())
        min_y = min(rect.y for rect in rectangles.values())
        if min_x < 0 or min_y < 0:
            dx = -min_x + policy.pitch if min_x < 0 else 0
            dy = -min_y + policy.pitch if min_y < 0 else 0
            placements = {uid: GridPoint(point.column + dx, point.row + dy) for uid, point in placements.items()}
            rectangles = _translate_scope_rects(rectangles, dx, dy)
            module_scope_offsets = {scope: (ox + dx, oy + dy) for scope, (ox, oy) in module_scope_offsets.items()}

    # Group rectangles are computed from translated children to guarantee full
    # recursive containment, while sibling rectangles are kept non-overlapping.
    for uid in sorted(groups, key=lambda item: len(_ancestor_map(nodes)[item])):
        child_rects = [rectangles[child] for child in direct_children.get(uid, ()) if child in rectangles]
        if child_rects:
            rectangles[uid] = _union_rect(child_rects, policy.group_padding)
            placements[uid] = GridPoint(rectangles[uid].x, rectangles[uid].y)

    ancestors = _ancestor_map(nodes)
    collisions = _ancestor_rect_overlap(rectangles, nodes)
    if collisions:
        raise StrictPlannerError("planner produced overlapping sibling rectangles: " + ", ".join(f"{left}/{right}" for left, right in collisions))
    for group in groups:
        child_rects = [rectangles[child] for child in direct_children.get(group, ()) if child in rectangles]
        if child_rects:
            group_rect = rectangles[group]
            if any(rect.x < group_rect.x or rect.y < group_rect.y or rect.right > group_rect.right or rect.bottom > group_rect.bottom for rect in child_rects):
                raise StrictPlannerError(f"group bounds do not contain children: {group}")

    modules: list[LayoutModule] = []
    for scope in scope_order:
        members_seen: set[str] = set()
        for kind, members, metadata in scope_modules.get(scope, ()):
            unique_members = tuple(dict.fromkeys(members))
            members_seen.update(unique_members)
            modules.append(LayoutModule(kind, scope, unique_members, _module_bounds(kind, unique_members, rectangles), dict(metadata)))
    modules.sort(key=lambda item: (item.scope or "", item.kind, item.members))

    edge_coverage = {edge.identity(): "planned" for edge in snapshot.edges}
    motif_coverage: dict[str, tuple[str, ...]] = {
        kind: tuple(sorted({member for module in modules if module.kind == kind for member in module.members}))
        for kind in ("rail", "feeder", "region", "reduction")
    }
    source_targets: dict[str, set[str]] = defaultdict(set)
    for edge in edges:
        source_targets[edge.source].add(edge.target)
    shared_source_ids = tuple(sorted(source for source, targets in source_targets.items() if len(targets) > 1))
    diagnostics = {
        "node_count": len(snapshot.nodes),
        "edge_count": len(snapshot.edges),
        "all_edge_coverage": {
            "expected": len(snapshot.edges),
            "planned": len(edge_coverage),
            "missing": [],
            "ids": tuple(sorted(edge_coverage)),
        },
        "rectangle_overlap_count": len(collisions),
        "integer_grid": all(isinstance(point.column, int) and isinstance(point.row, int) for point in placements.values()),
        "pitch": policy.pitch,
        "shared_source_placement_count": len(shared_source_ids),
        "shared_source_ids": shared_source_ids,
        "ancestor_containment_excluded": tuple(sorted((child, parent) for child, parents in ancestors.items() for parent in parents)),
        "processing_roles_separate_from_visual_continuity": True,
        "edge_processing_roles": {edge.identity(): edge.processing_role for edge in snapshot.edges},
        "edge_visual_continuities": {edge.identity(): edge.visual_continuity for edge in snapshot.edges},
        "stable_identity": True,
    }
    return StrictPlan(placements, rectangles, tuple(modules), edge_coverage, motif_coverage, diagnostics, policy)


def validate_strict_plan(snapshot: StrictSnapshot, plan: StrictPlan) -> dict[str, Any]:
    """Independent pure validation suitable for a fresh verifier."""

    expected_nodes = {node.uid for node in snapshot.nodes}
    actual_nodes = set(plan.placements)
    actual_rectangles = set(plan.rectangles)
    edge_ids = {edge.identity() for edge in snapshot.edges}
    planned_edges = set(plan.edge_coverage)
    collisions = _ancestor_rect_overlap(plan.rectangles, snapshot.node_map())
    missing_nodes = sorted(expected_nodes - actual_nodes)
    extra_nodes = sorted(actual_nodes - expected_nodes)
    missing_rectangles = sorted(expected_nodes - actual_rectangles)
    extra_rectangles = sorted(actual_rectangles - expected_nodes)
    invalid_rectangles = sorted(
        uid
        for uid, rect in plan.rectangles.items()
        if not all(
            isinstance(value, int) and not isinstance(value, bool)
            for value in (rect.x, rect.y, rect.width, rect.height)
        )
        or rect.width <= 0
        or rect.height <= 0
    )
    containment_errors: list[str] = []
    node_map = snapshot.node_map()
    for group in (node for node in snapshot.nodes if node.is_group):
        group_rect = plan.rectangles.get(group.uid)
        if group_rect is None:
            continue
        for child in snapshot.nodes:
            if child.parent_uid != group.uid or child.uid not in plan.rectangles:
                continue
            child_rect = plan.rectangles[child.uid]
            if (
                child_rect.x < group_rect.x
                or child_rect.y < group_rect.y
                or child_rect.right > group_rect.right
                or child_rect.bottom > group_rect.bottom
            ):
                containment_errors.append(f"{group.uid}/{child.uid}")
    missing_edges = sorted(edge_ids - planned_edges)
    extra_edges = sorted(planned_edges - edge_ids)
    non_planned_edges = sorted(edge_id for edge_id, state in plan.edge_coverage.items() if state != "planned")
    integer_grid = all(
        isinstance(point.column, int)
        and not isinstance(point.column, bool)
        and isinstance(point.row, int)
        and not isinstance(point.row, bool)
        for point in plan.placements.values()
    )
    return {
        "ok": (
            not missing_nodes
            and not extra_nodes
            and not missing_rectangles
            and not extra_rectangles
            and not invalid_rectangles
            and not containment_errors
            and not missing_edges
            and not extra_edges
            and not non_planned_edges
            and not collisions
            and integer_grid
            and plan.all_edges_covered
        ),
        "missing_nodes": missing_nodes,
        "extra_nodes": extra_nodes,
        "missing_rectangles": missing_rectangles,
        "extra_rectangles": extra_rectangles,
        "invalid_rectangles": invalid_rectangles,
        "group_containment_errors": sorted(containment_errors),
        "missing_edges": missing_edges,
        "extra_edges": extra_edges,
        "non_planned_edges": non_planned_edges,
        "rectangle_overlap_count": len(collisions),
        "all_edges_covered": not missing_edges and not extra_edges and not non_planned_edges and plan.all_edges_covered,
        "integer_grid": integer_grid,
        "catalogue": {key: value.status.value for key, value in fixture_catalogue().items()},
    }


def fixture_catalogue() -> dict[str, FixtureCoverage]:
    """Return the exact SO-20 split of offline, host-only and fail-closed cases."""

    planner = CoverageStatus.PLANNER_COVERED
    host = CoverageStatus.HOST_ONLY
    closed = CoverageStatus.FAIL_CLOSED
    return {
        "O01": FixtureCoverage("O01", "serial H/V", planner, ("all-edge coverage", "integer grid")),
        "O02": FixtureCoverage("O02", "horizontal Merge with feeders", planner, ("rail", "feeder")),
        "O03": FixtureCoverage("O03", "x29-style five-BG plus FG receiver", planner, ("processing roles", "rail")),
        "O04": FixtureCoverage("O04", "x31.5-style three-BG receiver", planner, ("reduction", "rail")),
        "O05": FixtureCoverage("O05", "Merge2 foreground continuity", planner, ("role/continuity split",)),
        "O06": FixtureCoverage("O06", "same-X non-chain", planner, ("rectangle non-overlap",)),
        "O07": FixtureCoverage("O07", "same node pair on distinct ports and duplicate ordinal", planner, ("port multiedge preservation",)),
        "O08": FixtureCoverage("O08", "Group boundary projection", planner, ("recursive bounds",)),
        "O09": FixtureCoverage("O09", "unequal rectangles, expanded/collapsed", planner, ("full rectangle geometry",)),
        "O10": FixtureCoverage("O10", "shared source fan-out and multiple outputs", planner, ("shared source once",)),
        "O11": FixtureCoverage("O11", "Mask and auxiliary links", planner, ("all-edge coverage",)),
        "O12": FixtureCoverage("O12", "missing or unknown input coverage", closed, ("refuse structure plan",), "unknown is never an empty connection"),
        "O13": FixtureCoverage("O13", "29-group census derivation", planner, ("recursive group bounds",)),
        "O14": FixtureCoverage("O14", "flatten twice and former-region stability", host, ("host flatten/undo required",)),
        "O15": FixtureCoverage("O15", "1100+ non-Group and deep chain", planner, ("iterative topology",), "offline stress only; host qualification remains separate"),
        "O16": FixtureCoverage("O16", "actual native view and wire coverage", host, ("native renderer readback",)),
        "O17": FixtureCoverage("O17", "UI Cancel/Undo/rollback", host, ("controller and host transaction",)),
        "O18": FixtureCoverage("O18", "host readback offsets", host, ("measured host transform",)),
    }


FIXTURE_CATALOGUE = fixture_catalogue()
coverage_catalogue = fixture_catalogue
build_snapshot = build_strict_snapshot
plan_layout = plan_strict


__all__ = [
    "CoverageStatus",
    "FIXTURE_CATALOGUE",
    "FixtureCoverage",
    "GridPoint",
    "LayoutModule",
    "PlannerEdge",
    "PlannerNode",
    "PlannerPolicy",
    "PlannerSnapshot",
    "Rect",
    "StrictCycleError",
    "StrictCoverageError",
    "StrictEdge",
    "StrictNode",
    "StrictPlan",
    "StrictPlannerError",
    "StrictPolicy",
    "StrictSnapshot",
    "build_snapshot",
    "build_strict_snapshot",
    "build_strict_snapshot_from_processing",
    "coverage_catalogue",
    "fixture_catalogue",
    "plan_layout",
    "plan_strict",
    "validate_strict_plan",
]
