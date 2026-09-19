"""Fail-closed, host-agnostic evidence for native view realization.

The strict planner describes a logical layout.  This module describes the
separate evidence needed to say that a native viewer rendered that layout.
It deliberately contains no Resolve API names or host calls.  A host adapter
may serialize its readback into this JSON-shaped contract and pass it to
``qualify_view_evidence``.

Missing observations are errors, not empty collections.  In particular, a
numeric pipe-mode value, a node rectangle without port positions, or a small
overview cannot be promoted to strict-view evidence by this module.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from math import isfinite
from typing import Any, Mapping, Sequence


VIEW_REALIZATION_SCHEMA = "resolve-node-kit.view-realization/v1"
_PASS_STATUS = "pass"
_EDGE_COVERAGE = {"measured", "native-contract"}
_PORT_ROLES = {"input", "output", "mask", "auxiliary"}
_SAMPLE_KINDS = {"overview", "difficult-region"}
_HOST_ONLY_CLAUSES = (
    "native renderer mode control and readback",
    "actual viewer port/edge geometry sampling",
    "same-view pre/post/restored observation and cleanup",
)


class ViewEvidenceError(ValueError):
    """Raised when view evidence is incomplete or internally inconsistent."""


class ViewEvidenceRefusal(ViewEvidenceError):
    """Raised for evidence that must remain fail-closed."""


def _text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ViewEvidenceRefusal(f"{field_name} must be a non-empty string")
    return value.strip()


def _number(value: Any, field_name: str, *, positive: bool = False) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(float(value)):
        raise ViewEvidenceRefusal(f"{field_name} must be a finite number")
    if positive and float(value) <= 0:
        raise ViewEvidenceRefusal(f"{field_name} must be positive")
    return value


def _status(value: Any, field_name: str, *, allowed: set[str] | None = None) -> str:
    # A boolean is deliberately not accepted.  ``True`` cannot distinguish
    # complete host coverage from a caller's optimistic assertion.
    if isinstance(value, Mapping):
        value = value.get("status", value.get("state"))
    result = _text(value, field_name).lower()
    if allowed is not None and result not in allowed:
        raise ViewEvidenceRefusal(f"{field_name} has unsupported status {result!r}")
    return result


def _run_id(value: Any, field_name: str = "run_id") -> str:
    return _text(value, field_name)


def _json_safe(value: Any, *, path: str = "evidence") -> Any:
    """Return a JSON-safe copy, rejecting objects that would hide identity."""

    if value is None or isinstance(value, (str, int, float, bool)):
        if isinstance(value, float) and not isfinite(value):
            raise ViewEvidenceRefusal(f"{path} contains a non-finite number")
        return value
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise ViewEvidenceRefusal(f"{path} has a non-string key")
            result[key] = _json_safe(item, path=f"{path}.{key}")
        return result
    if isinstance(value, (list, tuple)):
        return [_json_safe(item, path=f"{path}[{index}]") for index, item in enumerate(value)]
    raise ViewEvidenceRefusal(f"{path} contains a non-JSON value {type(value).__name__}")


@dataclass(frozen=True, slots=True)
class ViewRect:
    x: int | float
    y: int | float
    width: int | float
    height: int | float

    @classmethod
    def from_value(cls, value: Any, field_name: str) -> "ViewRect":
        if isinstance(value, cls):
            return value
        if not isinstance(value, Mapping):
            raise ViewEvidenceRefusal(f"{field_name} must contain x/y/width/height")
        return cls(
            _number(value.get("x"), f"{field_name}.x"),
            _number(value.get("y"), f"{field_name}.y"),
            _number(value.get("width"), f"{field_name}.width", positive=True),
            _number(value.get("height"), f"{field_name}.height", positive=True),
        )

    def as_dict(self) -> dict[str, int | float]:
        return {"x": self.x, "y": self.y, "width": self.width, "height": self.height}


@dataclass(frozen=True, slots=True)
class ViewPoint:
    x: int | float
    y: int | float

    @classmethod
    def from_value(cls, value: Any, field_name: str) -> "ViewPoint":
        if isinstance(value, cls):
            return value
        if not isinstance(value, Mapping):
            raise ViewEvidenceRefusal(f"{field_name} must contain explicit x and y")
        return cls(_number(value.get("x"), f"{field_name}.x"), _number(value.get("y"), f"{field_name}.y"))

    def as_dict(self) -> dict[str, int | float]:
        return {"x": self.x, "y": self.y}


@dataclass(frozen=True, slots=True)
class Viewport:
    x: int | float
    y: int | float
    width: int | float
    height: int | float
    zoom: int | float

    @classmethod
    def from_value(cls, value: Any, field_name: str) -> "Viewport":
        if isinstance(value, cls):
            return value
        if not isinstance(value, Mapping):
            raise ViewEvidenceRefusal(f"{field_name} must contain x/y/width/height/zoom")
        return cls(
            _number(value.get("x"), f"{field_name}.x"),
            _number(value.get("y"), f"{field_name}.y"),
            _number(value.get("width"), f"{field_name}.width", positive=True),
            _number(value.get("height"), f"{field_name}.height", positive=True),
            _number(value.get("zoom"), f"{field_name}.zoom", positive=True),
        )

    def as_dict(self) -> dict[str, int | float]:
        return {"x": self.x, "y": self.y, "width": self.width, "height": self.height, "zoom": self.zoom}


@dataclass(frozen=True, slots=True)
class ViewModeEvidence:
    """The native mode value plus provenance and application scope."""

    raw_value: Any
    name: str
    evidence_source: str
    scope: str

    @classmethod
    def from_value(cls, value: Any, field_name: str = "mode") -> "ViewModeEvidence":
        if isinstance(value, cls):
            return value
        if not isinstance(value, Mapping):
            raise ViewEvidenceRefusal(
                f"{field_name} requires raw_value, name, evidence_source and scope; a numeric mode alone is insufficient"
            )
        if "raw_value" not in value:
            raise ViewEvidenceRefusal(f"{field_name}.raw_value is required")
        raw_value = _json_safe(value["raw_value"], path=f"{field_name}.raw_value")
        # A plain numeric value is accepted only when accompanied by all
        # provenance fields; this prevents PipeStyle-like guesses from passing.
        return cls(
            raw_value=raw_value,
            name=_text(value.get("name"), f"{field_name}.name"),
            evidence_source=_text(value.get("evidence_source", value.get("source")), f"{field_name}.evidence_source"),
            scope=_text(value.get("scope"), f"{field_name}.scope"),
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "raw_value": _json_safe(self.raw_value, path="mode.raw_value"),
            "name": self.name,
            "evidence_source": self.evidence_source,
            "scope": self.scope,
        }


@dataclass(frozen=True, slots=True)
class PortPositionEvidence:
    node_id: str
    port_id: str
    x: int | float
    y: int | float
    role: str

    @classmethod
    def from_value(cls, value: Any, field_name: str, *, key: str | None = None) -> "PortPositionEvidence":
        if isinstance(value, cls):
            return value
        if not isinstance(value, Mapping):
            raise ViewEvidenceRefusal(f"{field_name} requires node_id/port_id/x/y/role; center-only evidence is not valid")
        node_id = value.get("node_id")
        port_id = value.get("port_id")
        # A mapping key of ``node:port`` is a convenience only; it still must
        # carry explicit x/y and role fields, so a rectangle center is not
        # silently reinterpreted as a port.
        if (node_id is None or port_id is None) and isinstance(key, str) and ":" in key:
            node_id, port_id = key.split(":", 1)
        role = _text(value.get("role"), f"{field_name}.role").lower()
        if role not in _PORT_ROLES:
            raise ViewEvidenceRefusal(f"{field_name}.role must identify an input/output/mask/auxiliary port")
        return cls(
            node_id=_text(node_id, f"{field_name}.node_id"),
            port_id=_text(port_id, f"{field_name}.port_id"),
            x=_number(value.get("x"), f"{field_name}.x"),
            y=_number(value.get("y"), f"{field_name}.y"),
            role=role,
        )

    @property
    def key(self) -> str:
        return f"{self.node_id}:{self.port_id}"

    def as_dict(self) -> dict[str, Any]:
        return {"node_id": self.node_id, "port_id": self.port_id, "x": self.x, "y": self.y, "role": self.role}


def canonical_edge_id(
    source: Any,
    source_output_id: Any,
    target: Any,
    target_input_id: Any,
    ordinal: Any = 0,
) -> str:
    """Construct a deterministic ID from both endpoint node/port labels."""

    source_text = _text(source, "source")
    source_port = _text(source_output_id, "source_output_id")
    target_text = _text(target, "target")
    target_port = _text(target_input_id, "target_input_id")
    if isinstance(ordinal, bool) or not isinstance(ordinal, int) or ordinal < 0:
        raise ViewEvidenceRefusal("ordinal must be a non-negative integer")
    return f"{source_text}:{source_port}->{target_text}:{target_port}#{ordinal}"


@dataclass(frozen=True, slots=True)
class EdgeGeometryEvidence:
    edge_id: str
    source: str
    source_output_id: str
    target: str
    target_input_id: str
    ordinal: int
    geometry_coverage: str
    sample_ids: tuple[str, ...]

    @classmethod
    def from_value(cls, value: Any, field_name: str = "edge") -> "EdgeGeometryEvidence":
        if isinstance(value, cls):
            return value
        if not isinstance(value, Mapping):
            raise ViewEvidenceRefusal(f"{field_name} must include canonical endpoint and sample linkage")
        ordinal = value.get("ordinal", 0)
        if isinstance(ordinal, bool) or not isinstance(ordinal, int) or ordinal < 0:
            raise ViewEvidenceRefusal(f"{field_name}.ordinal must be a non-negative integer")
        source = _text(value.get("source"), f"{field_name}.source")
        source_output_id = _text(value.get("source_output_id", value.get("source_output")), f"{field_name}.source_output_id")
        target = _text(value.get("target"), f"{field_name}.target")
        target_input_id = _text(value.get("target_input_id", value.get("target_input")), f"{field_name}.target_input_id")
        edge_id = _text(value.get("edge_id"), f"{field_name}.edge_id")
        expected = canonical_edge_id(source, source_output_id, target, target_input_id, ordinal)
        if edge_id != expected:
            raise ViewEvidenceRefusal(f"{field_name}.edge_id is not the canonical port-complete ID")
        raw_samples = value.get("sample_ids")
        if not isinstance(raw_samples, (list, tuple)) or not raw_samples:
            raise ViewEvidenceRefusal(f"{field_name}.sample_ids must link to at least one sample")
        sample_ids = tuple(_text(item, f"{field_name}.sample_ids[{index}]") for index, item in enumerate(raw_samples))
        if len(set(sample_ids)) != len(sample_ids):
            raise ViewEvidenceRefusal(f"{field_name}.sample_ids contains duplicates")
        coverage = _status(value.get("geometry_coverage", value.get("coverage")), f"{field_name}.geometry_coverage", allowed=_EDGE_COVERAGE)
        return cls(edge_id, source, source_output_id, target, target_input_id, ordinal, coverage, sample_ids)

    def as_dict(self) -> dict[str, Any]:
        return {
            "edge_id": self.edge_id,
            "source": self.source,
            "source_output_id": self.source_output_id,
            "target": self.target,
            "target_input_id": self.target_input_id,
            "ordinal": self.ordinal,
            "geometry_coverage": self.geometry_coverage,
            "sample_ids": list(self.sample_ids),
        }


@dataclass(frozen=True, slots=True)
class ViewSample:
    sample_id: str
    kind: str
    run_id: str
    viewport: Viewport
    edge_ids: tuple[str, ...]
    region: str

    @classmethod
    def from_value(cls, value: Any, field_name: str = "sample") -> "ViewSample":
        if isinstance(value, cls):
            return value
        if not isinstance(value, Mapping):
            raise ViewEvidenceRefusal(f"{field_name} must identify overview or difficult-region sampling")
        kind = _text(value.get("kind"), f"{field_name}.kind").lower()
        if kind not in _SAMPLE_KINDS:
            raise ViewEvidenceRefusal(f"{field_name}.kind must be overview or difficult-region")
        raw_edges = value.get("edge_ids")
        if not isinstance(raw_edges, (list, tuple)) or not raw_edges:
            raise ViewEvidenceRefusal(f"{field_name}.edge_ids must be explicit")
        edge_ids = tuple(_text(item, f"{field_name}.edge_ids[{index}]") for index, item in enumerate(raw_edges))
        if len(set(edge_ids)) != len(edge_ids):
            raise ViewEvidenceRefusal(f"{field_name}.edge_ids contains duplicates")
        return cls(
            sample_id=_text(value.get("sample_id", value.get("id")), f"{field_name}.sample_id"),
            kind=kind,
            run_id=_run_id(value.get("run_id"), f"{field_name}.run_id"),
            viewport=Viewport.from_value(value.get("viewport"), f"{field_name}.viewport"),
            edge_ids=edge_ids,
            region=_text(value.get("region", kind), f"{field_name}.region"),
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "sample_id": self.sample_id,
            "kind": self.kind,
            "run_id": self.run_id,
            "viewport": self.viewport.as_dict(),
            "edge_ids": list(self.edge_ids),
            "region": self.region,
        }


@dataclass(frozen=True, slots=True)
class CoverageEvidence:
    mask: str
    boundary: str
    multiedge: str
    all_edges: str

    @classmethod
    def from_value(cls, value: Any, field_name: str = "coverage") -> "CoverageEvidence":
        if isinstance(value, cls):
            return value
        if not isinstance(value, Mapping):
            raise ViewEvidenceRefusal(f"{field_name} must explicitly cover mask, boundary, multiedge and all_edges")
        return cls(
            _status(value.get("mask"), f"{field_name}.mask", allowed={"complete"}),
            _status(value.get("boundary"), f"{field_name}.boundary", allowed={"complete"}),
            _status(value.get("multiedge"), f"{field_name}.multiedge", allowed={"complete"}),
            _status(value.get("all_edges"), f"{field_name}.all_edges", allowed={"complete"}),
        )

    def as_dict(self) -> dict[str, str]:
        return {"mask": self.mask, "boundary": self.boundary, "multiedge": self.multiedge, "all_edges": self.all_edges}


@dataclass(frozen=True, slots=True)
class NativeRendererContract:
    status: str
    evidence_source: str
    scope: str
    run_id: str

    @classmethod
    def from_value(cls, value: Any, field_name: str = "native_renderer_contract") -> "NativeRendererContract":
        if isinstance(value, cls):
            return value
        if not isinstance(value, Mapping):
            raise ViewEvidenceRefusal(f"{field_name} must include status, evidence_source, scope and run_id")
        return cls(
            status=_status(value.get("status"), f"{field_name}.status"),
            evidence_source=_text(value.get("evidence_source", value.get("source")), f"{field_name}.evidence_source"),
            scope=_text(value.get("scope"), f"{field_name}.scope"),
            run_id=_run_id(value.get("run_id"), f"{field_name}.run_id"),
        )

    def as_dict(self) -> dict[str, str]:
        return {"status": self.status, "evidence_source": self.evidence_source, "scope": self.scope, "run_id": self.run_id}


@dataclass(frozen=True, slots=True)
class ViewObservation:
    stage: str
    run_id: str
    mode: ViewModeEvidence
    node_rectangles: Mapping[str, ViewRect]
    group_rectangles: Mapping[str, ViewRect]
    port_positions: Mapping[str, PortPositionEvidence]
    viewport: Viewport
    edge_ids: tuple[str, ...]

    @classmethod
    def from_value(cls, value: Any, field_name: str, *, expected_stage: str | None = None) -> "ViewObservation":
        if isinstance(value, cls):
            if expected_stage is not None and value.stage != expected_stage:
                raise ViewEvidenceRefusal(f"{field_name}.stage must be {expected_stage}")
            return value
        if not isinstance(value, Mapping):
            raise ViewEvidenceRefusal(f"{field_name} observation is required")
        stage = _text(value.get("stage", field_name), f"{field_name}.stage").lower()
        if stage not in {"pre", "post", "restored"}:
            raise ViewEvidenceRefusal(f"{field_name}.stage must be pre, post or restored")
        if expected_stage is not None and stage != expected_stage:
            raise ViewEvidenceRefusal(f"{field_name}.stage must be {expected_stage}")
        run_id = _run_id(value.get("run_id"), f"{field_name}.run_id")

        def rectangles(key: str) -> dict[str, ViewRect]:
            raw = value.get(key)
            if not isinstance(raw, Mapping):
                raise ViewEvidenceRefusal(f"{field_name}.{key} must be an explicit mapping")
            result: dict[str, ViewRect] = {}
            for item_id, item in raw.items():
                name = _text(item_id, f"{field_name}.{key} key")
                if name in result:
                    raise ViewEvidenceRefusal(f"{field_name}.{key} contains duplicate {name!r}")
                result[name] = ViewRect.from_value(item, f"{field_name}.{key}.{name}")
            return result

        raw_ports = value.get("port_positions")
        if not isinstance(raw_ports, Mapping):
            raise ViewEvidenceRefusal(f"{field_name}.port_positions must be explicit; center-only rectangles are insufficient")
        ports: dict[str, PortPositionEvidence] = {}
        for key, item in raw_ports.items():
            port = PortPositionEvidence.from_value(item, f"{field_name}.port_positions.{key}", key=str(key))
            if port.key in ports:
                raise ViewEvidenceRefusal(f"{field_name}.port_positions contains duplicate {port.key!r}")
            ports[port.key] = port
        raw_edges = value.get("edge_ids")
        if not isinstance(raw_edges, (list, tuple)) or not raw_edges:
            raise ViewEvidenceRefusal(f"{field_name}.edge_ids must be explicit")
        edge_ids = tuple(_text(item, f"{field_name}.edge_ids[{index}]") for index, item in enumerate(raw_edges))
        if len(set(edge_ids)) != len(edge_ids):
            raise ViewEvidenceRefusal(f"{field_name}.edge_ids contains duplicates")
        return cls(
            stage=stage,
            run_id=run_id,
            mode=ViewModeEvidence.from_value(value.get("mode"), f"{field_name}.mode"),
            node_rectangles=rectangles("node_rectangles"),
            group_rectangles=rectangles("group_rectangles"),
            port_positions=ports,
            viewport=Viewport.from_value(value.get("viewport"), f"{field_name}.viewport"),
            edge_ids=edge_ids,
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "run_id": self.run_id,
            "mode": self.mode.as_dict(),
            "node_rectangles": {key: value.as_dict() for key, value in sorted(self.node_rectangles.items())},
            "group_rectangles": {key: value.as_dict() for key, value in sorted(self.group_rectangles.items())},
            "port_positions": {key: value.as_dict() for key, value in sorted(self.port_positions.items())},
            "viewport": self.viewport.as_dict(),
            "edge_ids": list(self.edge_ids),
        }


@dataclass(frozen=True, slots=True)
class ViewRealizationEvidence:
    run_id: str
    target_id: str
    mode: ViewModeEvidence
    pre: ViewObservation
    post: ViewObservation
    restored: ViewObservation
    edge_ids: tuple[str, ...]
    edge_geometry: tuple[EdgeGeometryEvidence, ...]
    coverage: CoverageEvidence
    native_renderer_contract: NativeRendererContract
    samples: tuple[ViewSample, ...]

    @classmethod
    def from_value(cls, value: Any) -> "ViewRealizationEvidence":
        if isinstance(value, cls):
            _validate_cross_record(value)
            return value
        if not isinstance(value, Mapping):
            raise ViewEvidenceRefusal("view evidence must be a mapping")
        if value.get("schema") != VIEW_REALIZATION_SCHEMA:
            raise ViewEvidenceRefusal("schema must identify the supported view-realization contract")
        run_id = _run_id(value.get("run_id"))
        target_id = _text(value.get("target_id", value.get("target")), "target_id")
        raw_edge_ids = value.get("edge_ids")
        if not isinstance(raw_edge_ids, (list, tuple)) or not raw_edge_ids:
            raise ViewEvidenceRefusal("edge_ids must enumerate every canonical port-complete edge")
        edge_ids = tuple(_text(item, f"edge_ids[{index}]") for index, item in enumerate(raw_edge_ids))
        if len(set(edge_ids)) != len(edge_ids):
            raise ViewEvidenceRefusal("edge_ids contains duplicates")
        raw_edges = value.get("edge_geometry")
        if not isinstance(raw_edges, (list, tuple)) or not raw_edges:
            raise ViewEvidenceRefusal("edge_geometry must provide per-edge coverage and sample linkage")
        edge_geometry = tuple(EdgeGeometryEvidence.from_value(item, f"edge_geometry[{index}]") for index, item in enumerate(raw_edges))
        if {edge.edge_id for edge in edge_geometry} != set(edge_ids):
            raise ViewEvidenceRefusal("edge_geometry must match edge_ids exactly")
        raw_samples = value.get("samples")
        if not isinstance(raw_samples, (list, tuple)) or not raw_samples:
            raise ViewEvidenceRefusal("samples must include an overview and difficult-region zoom")
        samples = tuple(ViewSample.from_value(item, f"samples[{index}]") for index, item in enumerate(raw_samples))
        if len({sample.sample_id for sample in samples}) != len(samples):
            raise ViewEvidenceRefusal("samples contains duplicate sample_id")
        observations = {
            "pre": ViewObservation.from_value(value.get("pre"), "pre", expected_stage="pre"),
            "post": ViewObservation.from_value(value.get("post"), "post", expected_stage="post"),
            "restored": ViewObservation.from_value(value.get("restored"), "restored", expected_stage="restored"),
        }
        mode = ViewModeEvidence.from_value(value.get("mode"))
        coverage = CoverageEvidence.from_value(value.get("coverage"))
        contract = NativeRendererContract.from_value(value.get("native_renderer_contract"))
        evidence = cls(run_id, target_id, mode, observations["pre"], observations["post"], observations["restored"], edge_ids, edge_geometry, coverage, contract, samples)
        _validate_cross_record(evidence)
        return evidence

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": VIEW_REALIZATION_SCHEMA,
            "run_id": self.run_id,
            "target_id": self.target_id,
            "mode": self.mode.as_dict(),
            "pre": self.pre.as_dict(),
            "post": self.post.as_dict(),
            "restored": self.restored.as_dict(),
            "edge_ids": list(self.edge_ids),
            "edge_geometry": [edge.as_dict() for edge in self.edge_geometry],
            "coverage": self.coverage.as_dict(),
            "native_renderer_contract": self.native_renderer_contract.as_dict(),
            "samples": [sample.as_dict() for sample in self.samples],
            "host_only_clauses": list(_HOST_ONLY_CLAUSES),
        }


def _validate_cross_record(evidence: ViewRealizationEvidence) -> None:
    if evidence.native_renderer_contract.status != _PASS_STATUS:
        raise ViewEvidenceRefusal("native_renderer_contract.status must be pass")
    if evidence.native_renderer_contract.run_id != evidence.run_id:
        raise ViewEvidenceRefusal("native renderer contract is from a different run")
    if evidence.pre.mode != evidence.restored.mode:
        raise ViewEvidenceRefusal("restored mode does not match pre mode")
    if evidence.post.mode != evidence.mode:
        raise ViewEvidenceRefusal("top-level mode does not match post observation mode")
    observations = (evidence.pre, evidence.post, evidence.restored)
    geometry_by_id = {edge.edge_id: edge for edge in evidence.edge_geometry}
    for observation in observations:
        if observation.run_id != evidence.run_id:
            raise ViewEvidenceRefusal(f"{observation.stage} observation is from a different run")
        if tuple(observation.edge_ids) != evidence.edge_ids:
            raise ViewEvidenceRefusal(f"{observation.stage} observation does not cover the canonical edge set")
        for edge_id in evidence.edge_ids:
            edge = geometry_by_id[edge_id]
            source_key = f"{edge.source}:{edge.source_output_id}"
            target_key = f"{edge.target}:{edge.target_input_id}"
            source_port = observation.port_positions.get(source_key)
            target_port = observation.port_positions.get(target_key)
            if source_port is None or target_port is None:
                missing = [key for key, port in ((source_key, source_port), (target_key, target_port)) if port is None]
                raise ViewEvidenceRefusal(f"{observation.stage} observation is missing edge endpoint ports: {missing}")
            if source_port.role not in {"output", "auxiliary"}:
                raise ViewEvidenceRefusal(f"{observation.stage} source port {source_key!r} is not output/auxiliary")
            if target_port.role not in {"input", "mask", "auxiliary"}:
                raise ViewEvidenceRefusal(f"{observation.stage} target port {target_key!r} is not input/mask/auxiliary")
            if edge.source not in observation.node_rectangles or edge.target not in observation.node_rectangles:
                raise ViewEvidenceRefusal(f"{observation.stage} node rectangles omit edge endpoint nodes")
    sample_by_id = {sample.sample_id: sample for sample in evidence.samples}
    for sample in evidence.samples:
        if sample.run_id != evidence.run_id:
            raise ViewEvidenceRefusal(f"sample {sample.sample_id!r} is from a different run")
        unknown = set(sample.edge_ids) - set(evidence.edge_ids)
        if unknown:
            raise ViewEvidenceRefusal(f"sample {sample.sample_id!r} references unknown edge IDs: {sorted(unknown)}")
    overviews = [sample for sample in evidence.samples if sample.kind == "overview"]
    difficult = [sample for sample in evidence.samples if sample.kind == "difficult-region"]
    if not overviews:
        raise ViewEvidenceRefusal("overview sample is required")
    if not difficult:
        raise ViewEvidenceRefusal("difficult-region zoom sample is required")
    if max(sample.viewport.zoom for sample in difficult) <= min(sample.viewport.zoom for sample in overviews):
        raise ViewEvidenceRefusal("difficult-region samples must have a zoom greater than overview")
    if set().union(*(set(sample.edge_ids) for sample in overviews)) != set(evidence.edge_ids):
        raise ViewEvidenceRefusal("overview samples do not cover every canonical edge")
    for edge in evidence.edge_geometry:
        if any(sample_id not in sample_by_id for sample_id in edge.sample_ids):
            raise ViewEvidenceRefusal(f"edge {edge.edge_id} links to an unknown sample")
        if any(edge.edge_id not in sample_by_id[sample_id].edge_ids for sample_id in edge.sample_ids):
            raise ViewEvidenceRefusal(f"edge {edge.edge_id} sample linkage is inconsistent")


def qualify_view_evidence(payload: Any) -> dict[str, Any]:
    """Return a JSON-safe qualification result without mutating the host."""

    try:
        evidence = ViewRealizationEvidence.from_value(payload)
        result: dict[str, Any] = {
            "schema": VIEW_REALIZATION_SCHEMA,
            "ok": True,
            "status": "HOST_RENDERER_CONTRACT_PASS",
            "reasons": [],
            "evidence": evidence.as_dict(),
            "host_only_clauses": list(_HOST_ONLY_CLAUSES),
        }
        json.dumps(result, allow_nan=False)
        return result
    except (TypeError, ValueError, ViewEvidenceError) as exc:
        return {
            "schema": VIEW_REALIZATION_SCHEMA,
            "ok": False,
            "status": "FAIL_CLOSED",
            "reasons": [str(exc)],
            "host_only_clauses": list(_HOST_ONLY_CLAUSES),
        }


def require_qualified_view_evidence(payload: Any) -> ViewRealizationEvidence:
    """Normalize and require a qualified record at a mutation boundary."""

    evidence = ViewRealizationEvidence.from_value(payload)
    _validate_cross_record(evidence)
    return evidence


__all__ = [
    "CoverageEvidence",
    "EdgeGeometryEvidence",
    "NativeRendererContract",
    "PortPositionEvidence",
    "VIEW_REALIZATION_SCHEMA",
    "ViewEvidenceError",
    "ViewEvidenceRefusal",
    "ViewModeEvidence",
    "ViewObservation",
    "ViewPoint",
    "ViewRect",
    "ViewRealizationEvidence",
    "ViewSample",
    "Viewport",
    "canonical_edge_id",
    "qualify_view_evidence",
    "require_qualified_view_evidence",
]
