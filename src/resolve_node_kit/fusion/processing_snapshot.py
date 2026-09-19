"""Pure processing graph snapshots and source-reference audits.

This module deliberately does not talk to Resolve.  Host adapters may map
their readback into the small JSON-like schema here, while missing host
capabilities remain explicit (``absent``, ``unsupported`` or ``error``).
Unknown values are never treated as an empty connection and a structural
write must be rejected until the snapshot is complete.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


class SnapshotState(str, Enum):
    COMPLETE = "complete"
    ABSENT = "absent"
    UNSUPPORTED = "unsupported"
    ERROR = "error"


REQUIRED_PROCESSING_FIELDS = (
    "ports",
    "group_boundary_proxies",
    "parameters",
    "keyframes",
    "expressions",
    "instances",
    "media",
    "time_range",
    "tool_state",
)


@dataclass(frozen=True)
class SnapshotField:
    """One readback field with an explicit availability state."""

    state: SnapshotState
    value: Any = None
    detail: str | None = None

    @classmethod
    def complete(cls, value: Any) -> "SnapshotField":
        return cls(SnapshotState.COMPLETE, value)

    @classmethod
    def absent(cls, detail: str | None = None) -> "SnapshotField":
        return cls(SnapshotState.ABSENT, None, detail)

    @classmethod
    def unsupported(cls, detail: str | None = None) -> "SnapshotField":
        return cls(SnapshotState.UNSUPPORTED, None, detail)

    @classmethod
    def error(cls, detail: str) -> "SnapshotField":
        return cls(SnapshotState.ERROR, None, detail)

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"state": self.state.value}
        if self.state is SnapshotState.COMPLETE:
            result["value"] = self.value
        if self.detail:
            result["detail"] = self.detail
        return result


@dataclass(frozen=True)
class PortConnection:
    source: str
    target: str
    source_output_id: str
    target_input_id: str
    state: SnapshotState = SnapshotState.COMPLETE
    detail: str | None = None

    def as_dict(self) -> dict[str, Any]:
        result = {
            "source": self.source,
            "target": self.target,
            "source_output_id": self.source_output_id,
            "target_input_id": self.target_input_id,
            "state": self.state.value,
        }
        if self.detail:
            result["detail"] = self.detail
        return result


@dataclass(frozen=True)
class NodeSnapshot:
    name: str
    node_type: SnapshotField
    parent: SnapshotField
    position: SnapshotField = field(default_factory=lambda: SnapshotField.absent("not read"))
    inputs: tuple[PortConnection, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "type": self.node_type.as_dict(),
            "parent": self.parent.as_dict(),
            "position": self.position.as_dict(),
            "inputs": [item.as_dict() for item in self.inputs],
        }


@dataclass(frozen=True)
class ProcessingSnapshot:
    """Canonical, JSON-safe processing snapshot.

    ``nodes`` is keyed by stable host name.  A missing/unknown field is kept
    as a state object, never represented by an empty list or a guessed value.
    """

    nodes: Mapping[str, NodeSnapshot]
    connections: tuple[PortConnection, ...] = ()
    fields: Mapping[str, SnapshotField] = field(default_factory=dict)
    source: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": "resolve-node-kit.processing-snapshot/v1",
            "source": self.source,
            "nodes": {name: node.as_dict() for name, node in sorted(self.nodes.items())},
            "connections": [item.as_dict() for item in self.connections],
            "fields": {name: value.as_dict() for name, value in sorted(self.fields.items())},
        }

    def unresolved(self) -> list[str]:
        """Return deterministic paths whose state is not complete."""
        paths: list[str] = []
        for name, node in sorted(self.nodes.items()):
            for label, value in (("type", node.node_type), ("parent", node.parent), ("position", node.position)):
                if value.state is not SnapshotState.COMPLETE:
                    paths.append(f"nodes.{name}.{label}:{value.state.value}")
            for index, connection in enumerate(node.inputs):
                if connection.state is not SnapshotState.COMPLETE:
                    paths.append(f"nodes.{name}.inputs[{index}]:{connection.state.value}")
        for index, connection in enumerate(self.connections):
            if connection.state is not SnapshotState.COMPLETE:
                paths.append(f"connections[{index}]:{connection.state.value}")
        for name, value in sorted(self.fields.items()):
            if value.state is not SnapshotState.COMPLETE:
                paths.append(f"fields.{name}:{value.state.value}")
        return paths


class SnapshotWriteError(ValueError):
    """Raised when a structure-changing operation lacks a complete snapshot."""


def validate_structure_write(snapshot: ProcessingSnapshot) -> tuple[bool, tuple[str, ...]]:
    """Pure gate for structural writes.

    The return value is useful for callers that want a refusal result; the
    raising helper below is convenient at a mutation boundary.
    """
    unresolved = tuple(snapshot.unresolved())
    return (not unresolved, unresolved)


def require_complete_snapshot(snapshot: ProcessingSnapshot) -> None:
    ok, unresolved = validate_structure_write(snapshot)
    if not ok:
        raise SnapshotWriteError("structure write requires complete snapshot: " + ", ".join(unresolved))


def _field(value: Any, *, missing: str = "field not supplied") -> SnapshotField:
    if isinstance(value, SnapshotField):
        return value
    if isinstance(value, Mapping) and "state" in value:
        try:
            state = SnapshotState(str(value["state"]))
        except ValueError:
            return SnapshotField.error(f"unknown state {value.get('state')!r}")
        return SnapshotField(state, value.get("value"), value.get("detail"))
    if value is None:
        return SnapshotField.absent(missing)
    return SnapshotField.complete(value)


def _field_from_record(record: Mapping[str, Any], key: str, *, missing: str) -> SnapshotField:
    """Read a record key while preserving an explicit JSON ``null``."""
    if key not in record:
        return SnapshotField.absent(missing)
    if record[key] is None:
        return SnapshotField.complete(None)
    return _field(record[key], missing=missing)


def _connection(raw: Any, *, default_port: str | None = None) -> PortConnection:
    if not isinstance(raw, Mapping):
        return PortConnection("", "", "", default_port or "", SnapshotState.ERROR, "connection must be an object")
    source = str(raw.get("source", ""))
    target = str(raw.get("target", ""))
    source_output_id = str(raw.get("source_output_id", raw.get("source_port", "")))
    target_input_id = str(raw.get("target_input_id", raw.get("port", raw.get("target_port", default_port or ""))))
    state_raw = raw.get("state", SnapshotState.COMPLETE.value)
    try:
        state = SnapshotState(str(state_raw))
    except ValueError:
        state = SnapshotState.ERROR
    detail = raw.get("detail")
    if not source or not target or not source_output_id or not target_input_id:
        state = SnapshotState.ERROR
        detail = detail or "source, source_output_id, target and target_input_id are required"
    return PortConnection(source, target, source_output_id, target_input_id, state, str(detail) if detail else None)


def build_processing_snapshot(payload: Mapping[str, Any], *, source: str | None = None) -> ProcessingSnapshot:
    """Normalize a host-adapter payload without filling in missing data.

    Accepted payload shape is intentionally small: ``nodes`` may be a mapping
    or list of records, and ``connections`` is a list of
    ``{source,target,port,state?}`` objects.  A node's ``inputs`` are retained
    in addition to the global connection list for easy port-local checks.
    """
    if not isinstance(payload, Mapping):
        raise TypeError("processing snapshot payload must be a mapping")
    raw_nodes = payload.get("nodes", {})
    if isinstance(raw_nodes, Mapping):
        records = list(raw_nodes.values())
    elif isinstance(raw_nodes, list):
        records = raw_nodes
    else:
        records = []
    nodes: dict[str, NodeSnapshot] = {}
    for raw in records:
        if not isinstance(raw, Mapping):
            continue
        name = str(raw.get("name", ""))
        if not name:
            continue
        raw_inputs = raw.get("inputs", [])
        inputs = tuple(_connection(item, default_port=None) for item in raw_inputs) if isinstance(raw_inputs, list) else ()
        nodes[name] = NodeSnapshot(
            name=name,
            node_type=(
                _field_from_record(raw, "type", missing="node type not supplied")
                if "type" in raw
                else _field_from_record(raw, "node_type", missing="node type not supplied")
            ),
            parent=_field_from_record(raw, "parent", missing="parent not supplied"),
            position=_field_from_record(raw, "position", missing="position not supplied"),
            inputs=inputs,
        )
    raw_connections = payload.get("connections")
    if raw_connections is None:
        connections: tuple[PortConnection, ...] = ()
        fields = {"connections": SnapshotField.absent("connections not supplied")}
    elif isinstance(raw_connections, list):
        connections = tuple(_connection(item) for item in raw_connections)
        fields = {"connections": SnapshotField.complete(True)}
    else:
        connections = ()
        fields = {"connections": SnapshotField.error("connections must be a list")}
    for key, value in (payload.get("fields") or {}).items() if isinstance(payload.get("fields"), Mapping) else ():
        fields[str(key)] = _field(value)
    for key in REQUIRED_PROCESSING_FIELDS:
        fields.setdefault(key, SnapshotField.absent(f"{key} coverage not supplied"))
    return ProcessingSnapshot(nodes=nodes, connections=connections, fields=fields, source=source)


def _load_reference(reference: str | Path | Mapping[str, Any]) -> tuple[Mapping[str, Any], str]:
    if isinstance(reference, Mapping):
        return reference, "<mapping>"
    path = Path(reference)
    return json.loads(path.read_text(encoding="utf-8")), str(path)


def _duplicates(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def _cycle_nodes(parent: Mapping[str, str | None]) -> list[list[str]]:
    cycles: list[list[str]] = []
    for start in sorted(parent):
        chain: list[str] = []
        seen: dict[str, int] = {}
        current: str | None = start
        while current is not None and current in parent:
            if current in seen:
                cycles.append(chain[seen[current] :])
                break
            seen[current] = len(chain)
            chain.append(current)
            current = parent[current]
    unique: dict[tuple[str, ...], list[str]] = {}
    for cycle in cycles:
        key = tuple(sorted(cycle))
        unique[key] = cycle
    return list(unique.values())


def audit_layout_reference(reference: str | Path | Mapping[str, Any]) -> dict[str, Any]:
    """Audit every source row in the historical layout reference.

    This is evidence about the source file only.  It does not claim that the
    source contains port-complete processing state.
    """
    data, source = _load_reference(reference)
    tool_rows = data.get("tool_rows")
    groups = data.get("groups")
    merge_rows = data.get("merge_rows")
    tool_rows = tool_rows if isinstance(tool_rows, list) else []
    groups = groups if isinstance(groups, Mapping) else {}
    merge_rows = merge_rows if isinstance(merge_rows, list) else []
    names = [str(row.get("name")) for row in tool_rows if isinstance(row, Mapping) and row.get("name") is not None]
    name_set = set(names)
    parent: dict[str, str | None] = {}
    parent_errors: list[str] = []
    for row in tool_rows:
        if not isinstance(row, Mapping) or row.get("name") is None:
            continue
        name = str(row["name"])
        raw_parent = row.get("parent")
        parent[name] = None if raw_parent in (None, "", "root") else str(raw_parent)
        if parent[name] is not None and parent[name] not in name_set and parent[name] not in groups:
            parent_errors.append(f"{name}->{parent[name]}")
    group_members = [str(member) for values in groups.values() if isinstance(values, list) for member in values]
    duplicate_nodes = _duplicates(names)
    duplicate_group_members = _duplicates(group_members)
    unknown_group_members = sorted(set(group_members) - name_set)
    merge_checks: list[dict[str, Any]] = []
    for row in merge_rows:
        if not isinstance(row, Mapping):
            merge_checks.append({"ok": False, "error": "merge row is not an object"})
            continue
        inputs = row.get("inputs")
        parsed: list[tuple[str, str]] = []
        errors: list[str] = []
        if not isinstance(inputs, list):
            errors.append("inputs absent or not a list")
        else:
            for item in inputs:
                if not isinstance(item, (list, tuple)) or len(item) != 2:
                    errors.append(f"invalid input {item!r}")
                    continue
                src, port = str(item[0]), str(item[1])
                parsed.append((src, port))
                if src not in name_set:
                    errors.append(f"unknown source {src}")
                if not port:
                    errors.append("empty port")
            if len({port for _, port in parsed}) != len(parsed):
                errors.append("duplicate input port")
        merge_checks.append({"name": row.get("name"), "ok": not errors, "inputs": parsed, "errors": errors})
    numeric_missing: list[str] = []
    numeric_invalid: list[str] = []
    grid_mismatches: list[str] = []
    for row in tool_rows:
        if not isinstance(row, Mapping):
            continue
        name = str(row.get("name", "<unnamed>"))
        for key in ("x", "y", "sx", "sy"):
            value = row.get(key)
            if value is None:
                numeric_missing.append(f"{name}.{key}")
            elif not isinstance(value, (int, float)):
                numeric_invalid.append(f"{name}.{key}")
        if all(isinstance(row.get(key), (int, float)) for key in ("x", "y", "sx", "sy")):
            # x/y are display coordinates while sx/sy are the source's
            # snapped grid coordinates; a non-zero display offset is valid
            # evidence, not an error to silently normalize away.
            if abs(float(row["x"]) - float(row["sx"])) > 0.02 or abs(float(row["y"]) - float(row["sy"])) > 0.02:
                grid_mismatches.append(name)
    count_checks = {
        "tool_count": {"declared": data.get("tool_count"), "observed": len(names), "ok": data.get("tool_count") == len(names)},
        "group_count": {"declared": data.get("group_count"), "observed": len(groups), "ok": data.get("group_count") == len(groups)},
        "env_fusion_comp_tool_counts": {
            "declared": ((data.get("env") or {}).get("fusion_comp_tool_counts") if isinstance(data.get("env"), Mapping) else None),
            "observed": len(names),
            "ok": not isinstance((data.get("env") or {}).get("fusion_comp_tool_counts") if isinstance(data.get("env"), Mapping) else None, list)
            or len(names) in (data.get("env") or {}).get("fusion_comp_tool_counts", []),
        },
    }
    checks = {
        "unique_nodes": {"ok": not duplicate_nodes, "duplicates": duplicate_nodes},
        "unique_group_members": {"ok": not duplicate_group_members, "duplicates": duplicate_group_members},
        "parent_references": {"ok": not parent_errors, "unknown": sorted(parent_errors)},
        "parent_cycles": {"ok": not _cycle_nodes(parent), "cycles": _cycle_nodes(parent)},
        "group_members": {"ok": not unknown_group_members, "unknown": unknown_group_members},
        "counts": count_checks,
        "grid": {
            "ok": not numeric_missing and not numeric_invalid,
            "missing": numeric_missing,
            "invalid": numeric_invalid,
            "mismatches": grid_mismatches,
        },
        "merge_inputs": {
            "ok": all(item.get("ok") for item in merge_checks),
            "rows": merge_checks,
        },
    }
    ok = all(
        (item.get("ok") if isinstance(item, Mapping) and "ok" in item else all(v.get("ok", False) for v in item.values() if isinstance(v, Mapping)))
        for item in checks.values()
    )
    return {
        "schema": "resolve-node-kit.layout-reference-audit/v1",
        "source": source,
        "ok": bool(ok),
        "observed": {"tool_count": len(names), "group_count": len(groups), "merge_count": len(merge_rows), "unique_node_count": len(name_set)},
        "checks": checks,
    }


__all__ = [
    "NodeSnapshot",
    "PortConnection",
    "ProcessingSnapshot",
    "REQUIRED_PROCESSING_FIELDS",
    "SnapshotField",
    "SnapshotState",
    "SnapshotWriteError",
    "audit_layout_reference",
    "build_processing_snapshot",
    "require_complete_snapshot",
    "validate_structure_write",
]
