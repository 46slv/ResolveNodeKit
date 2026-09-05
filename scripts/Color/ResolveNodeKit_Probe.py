"""Read-only Color graph probe. No grade or node mutation is performed."""
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
from resolve_node_kit.color import inspect_callables, probe_resolve_graphs  # noqa: E402

resolve_app = globals().get("resolve")
if resolve_app is None:
    print("[ResolveNodeKit] Color probe: Resolve object is unavailable in this script context.")
else:
    report = inspect_callables(resolve_app)
    print(f"[ResolveNodeKit] Resolve surface ({report.object_type}) loaded.")
    graphs = probe_resolve_graphs(resolve_app)
    for scope, snapshot in graphs.items():
        if snapshot is None:
            print(f"[ResolveNodeKit] Color graph {scope}: unavailable in current context")
            continue
        print(f"[ResolveNodeKit] Color graph {scope}: {snapshot.node_count} node(s)")
        for node in snapshot.nodes:
            print(
                f"  #{node.index}: label={node.label!r}, lut={node.lut!r}, "
                f"cache={node.cache_mode!r}, tools={node.tool_count!r}"
            )
    print("[ResolveNodeKit] Probe is read-only; no grade or node state was modified.")
