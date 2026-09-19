"""Fail-closed integration seam from SO-11 snapshots to the SO-20 planner.

This module deliberately stops before a host write.  A qualified host adapter
can use :func:`prepare_strict_plan` as the single composition point: complete
processing coverage is required, the existing strict planner is invoked, and
its independent validator must pass before a later writer is allowed to act.
Unknown host fields are never converted into an empty graph or a best-effort
layout.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from .host_snapshot import build_host_processing_snapshot
from .processing_snapshot import (
    ProcessingSnapshot,
    SnapshotWriteError,
    require_complete_snapshot,
)
from .strict_planner import (
    StrictPlan,
    StrictPolicy,
    StrictSnapshot,
    build_strict_snapshot_from_processing,
    plan_strict,
    validate_strict_plan,
)


class StrictPreparationError(RuntimeError):
    """Raised when a strict plan cannot be prepared without guessing."""


@dataclass(frozen=True, slots=True)
class StrictPreparation:
    """Complete snapshot, strict snapshot, plan, and independent validation."""

    processing: ProcessingSnapshot
    strict: StrictSnapshot
    plan: StrictPlan
    validation: Mapping[str, Any]

    def as_dict(self) -> dict[str, Any]:
        strict = {
            "nodes": [
                {
                    "uid": node.uid,
                    "display_name": node.display_name,
                    "reg_id": node.reg_id,
                    "parent": node.parent_uid,
                    "width": node.width,
                    "height": node.height,
                    "processing_role": node.processing_role,
                    "visual_continuity": node.visual_continuity,
                    "is_group": node.is_group,
                    "input_state": node.input_state,
                    "metadata": dict(node.metadata),
                }
                for node in self.strict.nodes
            ],
            "edges": [
                {
                    "source": edge.source,
                    "source_output_id": edge.source_output_id,
                    "target": edge.target,
                    "target_input_id": edge.target_input_id,
                    "ordinal": edge.ordinal,
                    "uid": edge.uid,
                    "processing_role": edge.processing_role,
                    "visual_continuity": edge.visual_continuity,
                    "state": edge.state,
                }
                for edge in self.strict.edges
            ],
            "source": self.strict.source,
            "input_coverage": self.strict.input_coverage,
            "unresolved_inputs": list(self.strict.unresolved_inputs),
        }
        return {
            "schema": "resolve-node-kit.strict-preparation/v1",
            "processing": self.processing.as_dict(),
            "strict": strict,
            "plan": self.plan.as_dict(),
            "validation": dict(self.validation),
        }


SnapshotReader = Callable[..., ProcessingSnapshot]


def _prepare(processing: ProcessingSnapshot, *, policy: StrictPolicy | None, source: str | None) -> StrictPreparation:
    try:
        require_complete_snapshot(processing)
    except SnapshotWriteError as exc:
        raise StrictPreparationError(str(exc)) from exc
    try:
        strict = build_strict_snapshot_from_processing(processing, source=source)
        plan = plan_strict(strict, policy)
    except Exception as exc:
        raise StrictPreparationError(str(exc)) from exc
    validation = validate_strict_plan(strict, plan)
    if not validation.get("ok", False):
        raise StrictPreparationError("strict plan validation failed: " + repr(dict(validation)))
    return StrictPreparation(processing, strict, plan, dict(validation))


def prepare_strict_plan(
    comp: Any,
    flow: Any | None = None,
    *,
    snapshot_reader: SnapshotReader = build_host_processing_snapshot,
    policy: StrictPolicy | None = None,
    source: str | None = "resolve-fusion-host",
) -> StrictPreparation:
    """Read a host snapshot and prepare one independently validated strict plan.

    ``snapshot_reader`` is an explicit seam for the qualified host adapter or a
    deterministic test double.  It must return :class:`ProcessingSnapshot` and
    must not mutate the host.  This function itself never calls a host write,
    save, settings, or Undo surface.
    """

    try:
        processing = snapshot_reader(comp, flow, source=source or "resolve-fusion-host")
    except StrictPreparationError:
        raise
    except Exception as exc:
        raise StrictPreparationError("host snapshot read failed: " + str(exc)) from exc
    if not isinstance(processing, ProcessingSnapshot):
        raise StrictPreparationError("snapshot_reader must return ProcessingSnapshot")
    return _prepare(processing, policy=policy, source=source)


def prepare_strict_plan_from_processing(
    payload: Any,
    *,
    policy: StrictPolicy | None = None,
    source: str | None = None,
) -> StrictPreparation:
    """Prepare a strict plan from an already captured SO-11 snapshot."""

    if not isinstance(payload, ProcessingSnapshot):
        raise StrictPreparationError("payload must be ProcessingSnapshot")
    return _prepare(payload, policy=policy, source=source)


__all__ = [
    "StrictPreparation",
    "StrictPreparationError",
    "prepare_strict_plan",
    "prepare_strict_plan_from_processing",
]
