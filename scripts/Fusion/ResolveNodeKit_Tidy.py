"""ResolveNodeKit Fusion entrypoint: deterministic graph tidy."""
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
from resolve_node_kit.fusion import FusionHostError, tidy_comp  # noqa: E402


def _current_comp():
    comp_obj = globals().get("comp")
    if comp_obj is not None:
        return comp_obj
    fusion_obj = globals().get("fusion") or globals().get("fu")
    if fusion_obj is not None:
        getter = getattr(fusion_obj, "GetCurrentComp", None)
        if callable(getter):
            return getter()
    return None


composition = _current_comp()
if composition is None:
    raise FusionHostError("No active Fusion composition. Open a comp and run the script again.")
result = tidy_comp(composition)
print(f"[ResolveNodeKit] Tidy Graph: nodes={result.node_count}, edges={result.edge_count}, moved={result.moved_count}, anchor={result.anchor}")
