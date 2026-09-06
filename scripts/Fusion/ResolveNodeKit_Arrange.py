"""ResolveNodeKit Fusion entrypoint: semantic Arrange with a small dialog.

User flow on the Fusion page:

1. optionally select nodes,
2. run this script from Workspace -> Scripts -> Comp,
3. set the two checkboxes (both default OFF),
4. press OK to arrange or Cancel to change nothing.

The script finds its package without a repo checkout:

1. $RNK_SUPPORT_ROOT/ResolveNodeKit/src when the variable is set,
2. <Fusion Support>/ResolveNodeKit/src located by walking up from this file,
3. the repo src tree two levels above this file (developer fallback).

Automated canary override (no dialog click needed):

    RNK_ARRANGE_NO_UI=1
    RNK_ARRANGE_INCLUDE_UNSELECTED=0|1 (default 0)
    RNK_ARRANGE_UNGROUP=0|1 (default 0; 1 stays fail-closed until host-proven)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path


def _candidate_src_dirs(script_file=None):
    """Ordered candidate package roots; first existing directory wins."""
    found = []
    override = os.environ.get("RNK_SUPPORT_ROOT", "")
    if override:
        found.append(Path(override) / "ResolveNodeKit" / "src")
    try:
        here = Path(script_file).resolve() if script_file else Path(__file__).resolve()
    except Exception:
        return found
    for parent in [here.parent, *here.parents]:
        if parent.name == "Fusion":
            found.append(parent / "ResolveNodeKit" / "src")
            break
    try:
        repo_src = here.parents[2] / "src"
    except IndexError:
        repo_src = None
    if repo_src is not None:
        found.append(repo_src)
    return found


def _bootstrap_package(script_file=None):
    for candidate in _candidate_src_dirs(script_file):
        try:
            if candidate.is_dir() and str(candidate) not in sys.path:
                sys.path.insert(0, str(candidate))
                return str(candidate)
            if candidate.is_dir():
                return str(candidate)
        except Exception:
            continue
    return ""


_BOOTSTRAPPED_FROM = _bootstrap_package()

from resolve_node_kit.fusion import ArrangeDialogState, FusionHostError, arrange_comp  # noqa: E402


TITLE = "ResolveNodeKit - Arrange"
LABEL_INCLUDE = "選択されていないノードも整列"
LABEL_UNGROUP = "グループ化を解除して整列"


def _current_comp():
    comp_obj = globals().get("comp")
    if comp_obj is not None:
        return comp_obj
    fusion_obj = globals().get("fusion") or globals().get("fu")
    if fusion_obj is not None:
        getter = getattr(fusion_obj, "GetCurrentComp", None)
        if callable(getter):
            try:
                return getter()
            except Exception:
                return None
    return None


def _state_from_env():
    return ArrangeDialogState(
        include_unselected=os.environ.get("RNK_ARRANGE_INCLUDE_UNSELECTED", "0") == "1",
        ungroup=os.environ.get("RNK_ARRANGE_UNGROUP", "0") == "1",
    )


def _ask_user(ask):
    shapes = [
        [
            [LABEL_INCLUDE, "Checkbox", {"Default": 0}],
            [LABEL_UNGROUP, "Checkbox", {"Default": 0}],
        ],
        {
            1: {1: LABEL_INCLUDE, 2: "Checkbox", 3: {"Default": 0}},
            2: {1: LABEL_UNGROUP, 2: "Checkbox", 3: {"Default": 0}},
        },
    ]
    last_error = None
    for controls in shapes:
        try:
            return ("ok", ask(TITLE, controls))
        except Exception as exc:
            last_error = exc
    return ("unavailable", last_error)


def _to_state(result):
    if result is None:
        return None
    if isinstance(result, dict):
        mapped = {
            "IncludeUnselected": result.get("IncludeUnselected", result.get(LABEL_INCLUDE, 0)),
            "UngroupFirst": result.get("UngroupFirst", result.get(LABEL_UNGROUP, 0)),
        }
        return ArrangeDialogState.from_askuser(mapped)
    return ArrangeDialogState.from_askuser(result)


def main() -> int:
    composition = _current_comp()
    if composition is None:
        print("[ResolveNodeKit] Arrange: no active Fusion composition. Open a comp and run again.")
        return 2
    if os.environ.get("RNK_ARRANGE_NO_UI", "0") == "1":
        state = _state_from_env()
    else:
        ask = getattr(composition, "AskUser", None)
        if not callable(ask):
            print("[ResolveNodeKit] Arrange: dialog is unavailable on this host; nothing changed.")
            return 2
        status, payload = _ask_user(ask)
        if status == "unavailable":
            print("[ResolveNodeKit] Arrange: dialog wire shape unsupported; nothing changed.")
            print(str(payload))
            return 2
        state = _to_state(payload)
        if state is None:
            print("[ResolveNodeKit] Arrange canceled; nothing changed.")
            return 0
    try:
        result = arrange_comp(
            composition,
            include_unselected=state.include_unselected,
            ungroup=state.ungroup,
        )
    except FusionHostError as exc:
        print("[ResolveNodeKit] Arrange refused: " + str(exc))
        return 3
    diag = result.get("diagnostics", {})
    template = "[ResolveNodeKit] Arrange: nodes=%s edges=%s moved=%s arranged=%s avoidable_diagonals=%s expanded_gaps=%s"
    print(template % (
        result.get("node_count"),
        result.get("edge_count"),
        result.get("moved_count"),
        result.get("arranged_count"),
        diag.get("avoidable_diagonal_edge_count"),
        diag.get("expanded_gap_count"),
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
