from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CapabilityReport:
    object_type: str
    callables: tuple[str, ...]


def inspect_callables(obj: Any) -> CapabilityReport:
    """Read-only capability inventory for host probes.

    Color node APIs vary by Resolve version and scope. This deliberately does not infer
    missing operations or mutate the graph.
    """
    names: list[str] = []
    for name in dir(obj):
        if name.startswith("_"):
            continue
        try:
            value = getattr(obj, name)
        except Exception:
            continue
        if callable(value):
            names.append(name)
    return CapabilityReport(type(obj).__name__, tuple(sorted(set(names))))
