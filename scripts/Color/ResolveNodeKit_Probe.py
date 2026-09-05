"""Read-only Color API surface probe. No grade or node mutation is performed."""
from __future__ import annotations

import sys
from pathlib import Path


def _bootstrap_repo_src() -> None:
    try:
        root = Path(__file__).resolve().parents[2]
    except Exception:
        return
    src = root / "src"
    if src.is_dir() and str(src) not in sys.path:
        sys.path.insert(0, str(src))


_bootstrap_repo_src()
from resolve_node_kit.color import inspect_callables  # noqa: E402

resolve_app = globals().get("resolve")
if resolve_app is None:
    print("[ResolveNodeKit] Color probe: Resolve object is unavailable in this script context.")
else:
    report = inspect_callables(resolve_app)
    interesting = [name for name in report.callables if any(token in name.lower() for token in ("node", "color", "timeline", "project", "fusion"))]
    print(f"[ResolveNodeKit] Resolve surface ({report.object_type}):")
    for name in interesting:
        print(f"  - {name}")
    print("[ResolveNodeKit] Probe is read-only. Current-item / NodeGraph scope will be bound after host verification.")
