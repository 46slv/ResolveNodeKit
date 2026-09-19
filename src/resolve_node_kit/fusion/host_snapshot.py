"""Read-only Fusion host adapter for :mod:`processing_snapshot`.

The Resolve scripting surface is intentionally loose (different releases and
test doubles expose different combinations of ``Get*List`` methods).  This
module keeps that looseness at the boundary and emits the strict SO-10
``ProcessingSnapshot`` schema.  It never guesses a missing port, parent, or
processing field: fields that cannot be read are represented by an explicit
``SnapshotField`` state and ambiguous graph structure raises
``HostSnapshotError``.

Only read operations are used here.  In particular, this adapter does not
call ``SetPos``, ``LoadSettings``, ``Undo``, save APIs, or any other mutation.
It is therefore suitable for a host preflight before a structural write.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
import json
from typing import Any

from .processing_snapshot import (
    REQUIRED_PROCESSING_FIELDS,
    NodeSnapshot,
    PortConnection,
    ProcessingSnapshot,
    SnapshotField,
    SnapshotState,
)


class HostSnapshotError(RuntimeError):
    """Raised when the host graph cannot be discovered without guessing."""


_INPUT_ID_KEYS = ("INPS_ID", "INPS_Name", "INPN_Name", "Name", "ID")
_OUTPUT_ID_KEYS = ("OUTS_ID", "OUTS_Name", "OUTN_Name", "Name", "ID")


def _safe_call(obj: Any, method: str, *args: Any) -> Any:
    """Call one known read method, converting host exceptions to our error."""

    getter = getattr(obj, method, None)
    if not callable(getter):
        raise HostSnapshotError(f"host object lacks read method {method}")
    try:
        return getter(*args)
    except Exception as exc:  # pragma: no cover - exact host exceptions vary
        raise HostSnapshotError(f"{method} failed: {type(exc).__name__}: {exc}") from exc


def _as_items(value: Any, *, label: str) -> list[Any]:
    """Normalize Resolve list/dict return values without treating ``None`` as empty."""

    if value is None:
        raise HostSnapshotError(f"{label} returned no value")
    if isinstance(value, Mapping):
        return list(value.values())
    if isinstance(value, (str, bytes, bytearray)):
        raise HostSnapshotError(f"{label} returned a scalar")
    try:
        return list(value)
    except Exception as exc:
        raise HostSnapshotError(f"{label} is not iterable") from exc


def _attrs(obj: Any, *, label: str) -> Mapping[str, Any]:
    getter = getattr(obj, "GetAttrs", None)
    if not callable(getter):
        raise HostSnapshotError(f"{label} has no GetAttrs")
    try:
        value = getter()
    except Exception as exc:  # pragma: no cover - host-specific
        raise HostSnapshotError(f"{label}.GetAttrs failed: {type(exc).__name__}: {exc}") from exc
    if value is None:
        raise HostSnapshotError(f"{label}.GetAttrs returned no value")
    if not isinstance(value, Mapping):
        raise HostSnapshotError(f"{label}.GetAttrs returned {type(value).__name__}, not a mapping")
    return value


def _read_name(obj: Any, *, label: str) -> str:
    """Read the stable Fusion tool name without accepting an empty identity."""

    attrs = _attrs(obj, label=label)
    value = attrs.get("TOOLS_Name")
    if value is None:
        value = getattr(obj, "Name", None)
    if value is None:
        value = attrs.get("Name")
    if value is None:
        raise HostSnapshotError(f"{label} has no tool name")
    name = str(value)
    if not name:
        raise HostSnapshotError(f"{label} has an empty tool name")
    return name


def _read_type(obj: Any, *, label: str) -> SnapshotField:
    """Read ``TOOLS_RegID``/``ID`` as a field, preserving capability errors."""

    try:
        attrs = _attrs(obj, label=label)
    except HostSnapshotError as exc:
        return SnapshotField.unsupported(str(exc))
    value = attrs.get("TOOLS_RegID")
    if value is None:
        value = getattr(obj, "ID", None)
    if value is None:
        return SnapshotField.unsupported(f"{label} has no TOOLS_RegID/ID")
    return SnapshotField.complete(str(value))


def _read_tool_id(obj: Any, *, label: str) -> str | None:
    """Read Resolve's stable per-tool identity when the host exposes it."""

    try:
        attrs = _attrs(obj, label=label)
    except HostSnapshotError:
        return None
    value = attrs.get("TOOLI_ID")
    if value is None:
        value = getattr(obj, "TOOLI_ID", None)
    if value is None or not str(value):
        return None
    return str(value)


def _same_tool_identity(first: Any, second: Any, *, label: str) -> bool:
    """Return whether two host wrappers are the same live tool.

    Resolve 21.1 may expose one child both in a flattened ``GetToolList`` and
    through its owning group's ``GetChildrenList``.  Object identity is the
    strongest signal, while ``TOOLI_ID`` is the measured cross-wrapper
    identity.  A name-only match is deliberately never enough: two distinct
    tools with the same name remain an error.
    """

    if first is second:
        return True
    first_id = _read_tool_id(first, label=f"{label} first")
    second_id = _read_tool_id(second, label=f"{label} second")
    if first_id is None or second_id is None or first_id != second_id:
        return False
    try:
        first_attrs = _attrs(first, label=f"{label} first")
        second_attrs = _attrs(second, label=f"{label} second")
    except HostSnapshotError:
        return False
    # TOOLI_ID is authoritative, but conflicting stable metadata indicates
    # ambiguous host readback rather than an alias we may silently merge.
    for key in ("TOOLS_Name", "TOOLS_RegID"):
        first_value = first_attrs.get(key)
        second_value = second_attrs.get(key)
        if first_value is not None and second_value is not None and str(first_value) != str(second_value):
            return False
    return True


def _type_value(field: SnapshotField) -> str | None:
    if field.state is SnapshotState.COMPLETE and field.value is not None:
        return str(field.value)
    return None


def _read_parent_obj(obj: Any, *, label: str) -> tuple[bool, Any | None, str | None]:
    """Return ``(available, parent, detail)`` for the optional parent surface."""

    marker = object()
    try:
        value = getattr(obj, "ParentTool", marker)
    except Exception as exc:  # pragma: no cover - host-specific descriptors
        return False, None, f"{label}.ParentTool read failed: {type(exc).__name__}: {exc}"
    if value is marker:
        try:
            attrs = _attrs(obj, label=label)
        except HostSnapshotError as exc:
            return False, None, str(exc)
        if "TOOLH_GroupParent" not in attrs:
            return False, None, f"{label} has no ParentTool/TOOLH_GroupParent"
        value = attrs.get("TOOLH_GroupParent")
    # A few wrappers expose ParentTool as a zero-argument method.  Calling it
    # is still a read and avoids treating a bound method object as identity.
    if callable(value):
        try:
            value = value()
        except Exception as exc:  # pragma: no cover - host-specific
            return False, None, f"{label}.ParentTool failed: {type(exc).__name__}: {exc}"
    return True, value, None


def _read_port_id(obj: Any, keys: tuple[str, ...], *, label: str) -> tuple[str | None, str | None]:
    """Return a port identity and an explicit detail when it is unavailable."""

    attrs_getter = getattr(obj, "GetAttrs", None)
    attrs: Mapping[str, Any] | None = None
    if callable(attrs_getter):
        try:
            raw = attrs_getter()
            if isinstance(raw, Mapping):
                attrs = raw
        except Exception as exc:  # pragma: no cover - host-specific
            return None, f"{label}.GetAttrs failed: {type(exc).__name__}: {exc}"
    if attrs is not None:
        for key in keys:
            value = attrs.get(key)
            if value is not None and str(value):
                return str(value), None
    # Some minimal host wrappers expose Name/ID directly but no attrs table.
    for key in keys:
        value = getattr(obj, key, None)
        if value is not None and not callable(value) and str(value):
            return str(value), None
    return None, f"{label} port identity unavailable (GetAttrs/Name/ID)"


def _connected_output(input_obj: Any, *, label: str) -> tuple[bool, Any | None, str | None]:
    getter = getattr(input_obj, "GetConnectedOutput", None)
    if not callable(getter):
        return False, None, f"{label} has no GetConnectedOutput"
    try:
        return True, getter(), None
    except Exception as exc:  # pragma: no cover - host-specific
        return True, None, f"{label}.GetConnectedOutput failed: {type(exc).__name__}: {exc}"


def _connected_inputs(output_obj: Any, *, label: str) -> tuple[bool, list[Any] | None, str | None]:
    getter = getattr(output_obj, "GetConnectedInputs", None)
    if not callable(getter):
        return False, None, f"{label} has no GetConnectedInputs"
    try:
        raw = getter()
        if raw is None:
            return True, None, f"{label}.GetConnectedInputs returned no value"
        return True, _as_items(raw, label=f"{label}.GetConnectedInputs"), None
    except HostSnapshotError as exc:
        return True, None, str(exc)
    except Exception as exc:  # pragma: no cover - host-specific
        return True, None, f"{label}.GetConnectedInputs failed: {type(exc).__name__}: {exc}"


def _tool_from_port(port: Any, *, label: str) -> Any | None:
    getter = getattr(port, "GetTool", None)
    if callable(getter):
        try:
            return getter()
        except Exception:
            return None
    return None


def _json_safe(value: Any, *, path: str) -> Any:
    """Convert host scalar containers to JSON-safe values, never to guesses."""

    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, item in value.items():
            result[str(key)] = _json_safe(item, path=f"{path}.{key}")
        return result
    if isinstance(value, (list, tuple)):
        return [_json_safe(item, path=f"{path}[]") for item in value]
    raise TypeError(f"{path} contains non-JSON value {type(value).__name__}")


def _read_position(flow: Any, tool: Any, *, label: str) -> SnapshotField:
    if flow is None:
        return SnapshotField.unsupported("FlowView not supplied; position was not read")
    getter = getattr(flow, "GetPosTable", None)
    if not callable(getter):
        return SnapshotField.unsupported("FlowView lacks GetPosTable")
    try:
        raw = getter(tool)
    except Exception as exc:  # pragma: no cover - host-specific
        return SnapshotField.error(f"GetPosTable failed: {type(exc).__name__}: {exc}")
    if not isinstance(raw, Mapping):
        return SnapshotField.error("GetPosTable returned a non-mapping")
    pairs = ((1, 2), ("x", "y"), ("X", "Y"))
    for x_key, y_key in pairs:
        if x_key in raw and y_key in raw:
            try:
                value = [float(raw[x_key]), float(raw[y_key])]
            except (TypeError, ValueError) as exc:
                return SnapshotField.error(f"position values are not numeric: {exc}")
            return SnapshotField.complete(value)
    return SnapshotField.error("GetPosTable lacked an x/y pair")


def _discover_tools(comp: Any) -> tuple[dict[str, Any], dict[str, str | None], dict[str, SnapshotField]]:
    """Discover roots and GroupOperator children with duplicate/cycle guards."""

    root_raw = _safe_call(comp, "GetToolList")
    queue: list[tuple[Any, str | None]] = [(tool, None) for tool in _as_items(root_raw, label="GetToolList")]
    tools: dict[str, Any] = {}
    discovered_parent: dict[str, str | None] = {}
    type_fields: dict[str, SnapshotField] = {}
    scanned_groups: set[str] = set()
    while queue:
        tool, via_parent = queue.pop(0)
        label = f"tool[{len(tools)}]"
        name = _read_name(tool, label=label)
        if name in tools:
            previous = discovered_parent.get(name)
            if not _same_tool_identity(tools[name], tool, label=f"tool[{name!r}]"):
                raise HostSnapshotError(
                    f"duplicate tool name {name!r} discovered with ambiguous identity "
                    f"under {previous!r} and {via_parent!r}"
                )
            # Resolve 21.1 can return the same child once in a flattened root
            # inventory and once from GetChildrenList().  Reconcile only that
            # measured root-vs-owner alias.  Repeated discovery in one scope,
            # or discovery under two different owners, remains fail-closed.
            if previous is None and via_parent is not None:
                discovered_parent[name] = via_parent
                continue
            if previous is not None and via_parent is None:
                continue
            if previous == via_parent:
                raise HostSnapshotError(f"duplicate tool name {name!r} discovered more than once")
            raise HostSnapshotError(
                f"tool {name!r} discovered under conflicting parents {previous!r} and {via_parent!r}"
            )
        tools[name] = tool
        discovered_parent[name] = via_parent
        type_field = _read_type(tool, label=f"tool[{name!r}]")
        type_fields[name] = type_field
        if _type_value(type_field) == "GroupOperator":
            if name in scanned_groups:
                continue
            scanned_groups.add(name)
            children_getter = getattr(tool, "GetChildrenList", None)
            if not callable(children_getter):
                raise HostSnapshotError(f"GroupOperator {name!r} lacks GetChildrenList")
            try:
                children_raw = children_getter()
            except Exception as exc:  # pragma: no cover - host-specific
                raise HostSnapshotError(
                    f"GroupOperator {name!r}.GetChildrenList failed: {type(exc).__name__}: {exc}"
                ) from exc
            for child in _as_items(children_raw, label=f"GroupOperator {name!r}.GetChildrenList"):
                queue.append((child, name))
    if not tools:
        return {}, {}, {}

    parents: dict[str, str | None] = {}
    for name, tool in tools.items():
        available, parent_obj, detail = _read_parent_obj(tool, label=f"tool[{name!r}]")
        fallback = discovered_parent.get(name)
        if available and parent_obj is not None:
            parent_name = _read_name(parent_obj, label=f"parent of {name!r}")
            if fallback is not None and parent_name != fallback:
                raise HostSnapshotError(f"parent mismatch for {name!r}: {fallback!r} != {parent_name!r}")
            parents[name] = parent_name
        elif fallback is not None:
            parents[name] = fallback
        elif available and parent_obj is None:
            parents[name] = None
        else:
            # A root discovered by GetToolList is known to have no discovered
            # parent; no parent API is needed to represent that root fact.
            parents[name] = None

    # Validate every parent reference and reject cycles before constructing a
    # snapshot.  A malformed hierarchy must never become an apparently flat
    # graph by accident.
    groups = {name for name, field in type_fields.items() if _type_value(field) == "GroupOperator"}
    for name, parent in parents.items():
        if parent is not None and (parent not in tools or parent not in groups):
            raise HostSnapshotError(f"invalid GroupOperator parent {parent!r} for {name!r}")
    for start in sorted(tools):
        seen: set[str] = set()
        current: str | None = start
        while current is not None:
            if current in seen:
                raise HostSnapshotError(f"group hierarchy cycle detected at {current!r}")
            seen.add(current)
            current = parents[current]
    return tools, parents, type_fields


def _port_record(
    *,
    source_tool: Any | None,
    target_tool: Any | None,
    source_port: Any | None,
    target_port: Any | None,
    target_port_id: str | None,
    source_port_id: str | None,
    detail: str | None = None,
) -> PortConnection:
    source = ""
    target = ""
    errors: list[str] = []
    if source_tool is not None:
        try:
            source = _read_name(source_tool, label="connection source")
        except HostSnapshotError as exc:
            errors.append(str(exc))
    else:
        errors.append("source tool identity unavailable")
    if target_tool is not None:
        try:
            target = _read_name(target_tool, label="connection target")
        except HostSnapshotError as exc:
            errors.append(str(exc))
    else:
        errors.append("target tool identity unavailable")
    if source_port_id is None and source_port is not None:
        source_port_id, error = _read_port_id(source_port, _OUTPUT_ID_KEYS, label="source output")
        if error:
            errors.append(error)
    if target_port_id is None and target_port is not None:
        target_port_id, error = _read_port_id(target_port, _INPUT_ID_KEYS, label="target input")
        if error:
            errors.append(error)
    if source_port_id is None:
        errors.append("source_output_id unavailable")
        source_port_id = ""
    if target_port_id is None:
        errors.append("target_input_id unavailable")
        target_port_id = ""
    state = SnapshotState.COMPLETE if not errors else SnapshotState.UNSUPPORTED
    details = ([detail] if detail else []) + errors
    return PortConnection(source, target, source_port_id, target_port_id, state, "; ".join(details) or None)


def _bound_record(record: PortConnection, tools: Mapping[str, Any]) -> PortConnection:
    """Refuse a connection whose endpoint is outside the discovered comp."""

    missing: list[str] = []
    if record.source not in tools:
        missing.append(f"source tool {record.source!r} was not discovered")
    if record.target not in tools:
        missing.append(f"target tool {record.target!r} was not discovered")
    if not missing:
        return record
    detail = "; ".join(([record.detail] if record.detail else []) + missing)
    return PortConnection(
        record.source,
        record.target,
        record.source_output_id,
        record.target_input_id,
        SnapshotState.UNSUPPORTED,
        detail,
    )


def _read_ports(tools: Mapping[str, Any]) -> tuple[dict[str, Any], tuple[PortConnection, ...], SnapshotField]:
    """Read both endpoint lists and merge connection observations losslessly."""

    port_rows: dict[str, Any] = {}
    records: list[PortConnection] = []
    input_surface_ok = True
    output_surface_ok = True
    connection_keys: set[tuple[str, str, str, str]] = set()
    unsupported_connection = False

    for target_name, target in sorted(tools.items()):
        input_getter = getattr(target, "GetInputList", None)
        if not callable(input_getter):
            input_surface_ok = False
            port_rows[target_name] = {"inputs": {"state": "unsupported", "detail": "GetInputList unavailable"}}
            continue
        try:
            inputs = _as_items(input_getter(), label=f"{target_name}.GetInputList")
        except HostSnapshotError as exc:
            input_surface_ok = False
            port_rows[target_name] = {"inputs": {"state": "error", "detail": str(exc)}}
            continue
        row_inputs: list[dict[str, Any]] = []
        for index, input_obj in enumerate(inputs):
            input_id, input_detail = _read_port_id(input_obj, _INPUT_ID_KEYS, label=f"{target_name}.input[{index}]")
            row: dict[str, Any] = {"id": input_id, "state": "complete" if input_id else "unsupported"}
            if input_detail:
                row["detail"] = input_detail
                input_surface_ok = False
            connected, output_obj, connect_detail = _connected_output(
                input_obj, label=f"{target_name}.input[{index}]"
            )
            if not connected:
                input_surface_ok = False
                row["connection_state"] = "unsupported"
                row["connection_detail"] = connect_detail
            elif connect_detail:
                row["connection_state"] = "error"
                row["connection_detail"] = connect_detail
                unsupported_connection = True
            elif output_obj is None:
                row["connection_state"] = "complete"
            else:
                source_obj = _tool_from_port(output_obj, label=f"{target_name}.input[{index}].output")
                source_id, source_detail = _read_port_id(
                    output_obj, _OUTPUT_ID_KEYS, label=f"{target_name}.input[{index}].output"
                )
                record = _port_record(
                    source_tool=source_obj,
                    target_tool=target,
                    source_port=output_obj,
                    target_port=input_obj,
                    source_port_id=source_id,
                    target_port_id=input_id,
                    detail=source_detail or input_detail,
                )
                record = _bound_record(record, tools)
                if record.state is not SnapshotState.COMPLETE:
                    unsupported_connection = True
                key = (record.source, record.target, record.source_output_id, record.target_input_id)
                if key not in connection_keys:
                    connection_keys.add(key)
                    records.append(record)
                row["connection_state"] = record.state.value
                if record.detail:
                    row["connection_detail"] = record.detail
            row_inputs.append(row)
        port_rows.setdefault(target_name, {})["inputs"] = {"state": "complete", "value": row_inputs}

    for source_name, source in sorted(tools.items()):
        output_getter = getattr(source, "GetOutputList", None)
        if not callable(output_getter):
            output_surface_ok = False
            port_rows.setdefault(source_name, {})["outputs"] = {
                "state": "unsupported",
                "detail": "GetOutputList unavailable",
            }
            continue
        try:
            outputs = _as_items(output_getter(), label=f"{source_name}.GetOutputList")
        except HostSnapshotError as exc:
            output_surface_ok = False
            port_rows.setdefault(source_name, {})["outputs"] = {"state": "error", "detail": str(exc)}
            continue
        row_outputs: list[dict[str, Any]] = []
        for index, output_obj in enumerate(outputs):
            output_id, output_detail = _read_port_id(
                output_obj,
                _OUTPUT_ID_KEYS,
                label=f"{source_name}.output[{index}]",
            )
            row: dict[str, Any] = {"id": output_id, "state": "complete" if output_id else "unsupported"}
            if output_detail:
                row["detail"] = output_detail
                output_surface_ok = False
            connected, input_list, connect_detail = _connected_inputs(
                output_obj, label=f"{source_name}.output[{index}]"
            )
            if not connected:
                output_surface_ok = False
                row["connection_state"] = "unsupported"
                row["connection_detail"] = connect_detail
            elif connect_detail:
                unsupported_connection = True
                row["connection_state"] = "error"
                row["connection_detail"] = connect_detail
            else:
                row["connection_state"] = "complete"
                for target_input in input_list or []:
                    target_obj = _tool_from_port(target_input, label=f"{source_name}.output[{index}].input")
                    target_id, target_detail = _read_port_id(
                        target_input, _INPUT_ID_KEYS, label=f"{source_name}.output[{index}].input"
                    )
                    record = _port_record(
                        source_tool=source,
                        target_tool=target_obj,
                        source_port=output_obj,
                        target_port=target_input,
                        source_port_id=output_id,
                        target_port_id=target_id,
                        detail=output_detail or target_detail,
                    )
                    record = _bound_record(record, tools)
                    if record.state is not SnapshotState.COMPLETE:
                        unsupported_connection = True
                    key = (record.source, record.target, record.source_output_id, record.target_input_id)
                    if key not in connection_keys:
                        connection_keys.add(key)
                        records.append(record)
            row_outputs.append(row)
        port_rows.setdefault(source_name, {})["outputs"] = {"state": "complete", "value": row_outputs}

    if input_surface_ok and output_surface_ok and not unsupported_connection:
        field = SnapshotField.complete(port_rows)
    elif unsupported_connection:
        field = SnapshotField.unsupported("one or more connected ports lacked complete endpoint identity")
    else:
        details = []
        if not input_surface_ok:
            details.append("input port surface incomplete")
        if not output_surface_ok:
            details.append("output port surface incomplete")
        field = SnapshotField.unsupported("; ".join(details) or "port capability incomplete")
    return port_rows, tuple(records), field


def _unsupported_processing_fields() -> dict[str, SnapshotField]:
    fields: dict[str, SnapshotField] = {}
    for name in REQUIRED_PROCESSING_FIELDS:
        if name == "ports":
            continue
        fields[name] = SnapshotField.unsupported(
            f"Fusion host adapter does not expose complete {name} readback"
        )
    return fields


def build_host_processing_snapshot(
    comp: Any,
    flow: Any | None = None,
    *,
    source: str = "resolve-fusion-host",
) -> ProcessingSnapshot:
    """Build a JSON-safe read-only processing snapshot from a Fusion comp.

    Structural discovery failures raise :class:`HostSnapshotError`.  A
    capability gap in processing data is retained in ``snapshot.fields`` so a
    caller can refuse writes using ``validate_structure_write`` rather than
    accidentally treating it as an empty graph.
    """

    tools, parents, type_fields = _discover_tools(comp)
    port_rows, connections, ports_field = _read_ports(tools)
    fields = _unsupported_processing_fields()
    fields["ports"] = ports_field
    # ``tool_state`` can be read exactly when every node's attrs are a JSON
    # mapping.  It is deliberately separate from type/position readback.
    tool_state: dict[str, Any] = {}
    tool_state_ok = True
    for name, tool in sorted(tools.items()):
        try:
            attrs = _attrs(tool, label=f"tool[{name!r}]")
            tool_state[name] = _json_safe(dict(attrs), path=f"tool_state.{name}")
        except (HostSnapshotError, TypeError) as exc:
            tool_state_ok = False
            break
    fields["tool_state"] = (
        SnapshotField.complete(tool_state)
        if tool_state_ok
        else SnapshotField.error("one or more tool GetAttrs values were unreadable or non-JSON")
    )

    nodes: dict[str, NodeSnapshot] = {}
    for name, tool in sorted(tools.items()):
        node_inputs = tuple(
            connection for connection in connections if connection.target == name
        )
        parent_field = SnapshotField.complete(parents[name])
        position_field = _read_position(flow, tool, label=f"tool[{name!r}]")
        nodes[name] = NodeSnapshot(
            name=name,
            node_type=type_fields[name],
            parent=parent_field,
            position=position_field,
            inputs=node_inputs,
        )

    snapshot = ProcessingSnapshot(
        nodes=nodes,
        connections=connections,
        fields=fields,
        source=source,
    )
    # Exercise JSON safety at the adapter boundary.  Raising here is safer
    # than returning a snapshot that cannot be serialized for evidence.
    try:
        json.dumps(snapshot.as_dict(), sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise HostSnapshotError(f"snapshot is not JSON-safe: {exc}") from exc
    return snapshot


def read_processing_snapshot(
    comp: Any,
    flow: Any | None = None,
    *,
    source: str = "resolve-fusion-host",
) -> ProcessingSnapshot:
    """Alias with a verb that matches host readback call sites."""

    return build_host_processing_snapshot(comp, flow, source=source)


def snapshot_comp(comp: Any, flow: Any | None = None, *, source: str = "resolve-fusion-host") -> ProcessingSnapshot:
    """Compatibility alias for adapter callers using ``snapshot_comp``."""

    return build_host_processing_snapshot(comp, flow, source=source)


__all__ = [
    "HostSnapshotError",
    "build_host_processing_snapshot",
    "read_processing_snapshot",
    "snapshot_comp",
]
