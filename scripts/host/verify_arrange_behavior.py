#!/usr/bin/env python3
"""Build and classify direct production-handler host evidence.

This helper intentionally contains no UIA/MSAA probe and no control invoke.
The generated source is run by Fusion on a disposable whole-composition
fixture by default and imports the installed package, so it calls the same
``execute_arrange_request`` used by the menu script.  ``--selection-only`` is
reserved for regression/experimental coverage.
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path
from typing import Any


TITLE = "ResolveNodeKit - Arrange"
SCHEMA = "resolve-node-kit.arrange-behavior/v1"


def build_handler_source(
    output_path: str,
    *,
    include_unselected: bool = True,
    ungroup: bool = False,
    run_second: bool = True,
    undo_after_runs: bool = True,
) -> str:
    """Return an in-host Python source for one direct-handler evidence run."""
    config = {
        "include_unselected": bool(include_unselected),
        "ungroup": bool(ungroup),
        "run_second": bool(run_second),
        "undo_after_runs": bool(undo_after_runs),
        "title": TITLE,
        "schema": SCHEMA,
    }
    config_literal = json.dumps(json.dumps(config, ensure_ascii=False))
    lines = [
        "import json",
        "from pathlib import Path",
        "from resolve_node_kit.fusion import ArrangeDialogState, execute_arrange_request",
        "from resolve_node_kit.fusion.recursive_groups import _snapshot",
        "CONFIG = json.loads(" + config_literal + ")",
        "OUTPUT = " + repr(str(output_path)),
        "",
        "def names(value):",
        "    if isinstance(value, dict): value = value.values()",
        "    try: values = list(value or [])",
        "    except Exception: values = []",
        "    result = []",
        "    for tool in values:",
        "        name = getattr(tool, 'Name', None)",
        "        if name is None:",
        "            try: name = (tool.GetAttrs() or {}).get('TOOLS_Name')",
        "            except Exception: name = None",
        "        if name is not None: result.append(str(name))",
        "    return sorted(set(result))",
        "",
        "def snapshot(comp):",
        "    flow = getattr(getattr(comp, 'CurrentFrame', None), 'FlowView', None)",
        "    snap = _snapshot(comp, flow)",
        "    positions = {name: [float(x), float(y)] for name, (x, y) in snap.positions.items()}",
        "    edges = sorted(f'{edge.source}->{edge.target}.{edge.kind}' for edge in snap.edges)",
        "    return {'tool_count': len(snap.tools), 'positions': positions,",
        "            'connections': edges, 'parents': dict(snap.parents),",
        "            'groups': list(snap.groups), 'selected': names(comp.GetToolList(True)),",
        "            'modified': bool((comp.GetAttrs() or {}).get('COMPB_Modified', False))}",
        "",
        "fusion_obj = globals().get('fusion') or globals().get('fu')",
        "resolve_obj = globals().get('resolve')",
        "comp_obj = globals().get('comp')",
        "if comp_obj is None and fusion_obj is not None: comp_obj = fusion_obj.GetCurrentComp()",
        "if comp_obj is None: raise RuntimeError('no live current Fusion composition')",
        "log_lines = []",
        "def log(message):",
        "    log_lines.append(str(message))",
        "    print('[RNK-SEAM] ' + str(message))",
        "",
        "pre = snapshot(comp_obj)",
        "state = ArrangeDialogState(include_unselected=CONFIG['include_unselected'], ungroup=CONFIG['ungroup'])",
        "ask = getattr(comp_obj, 'AskUser', None)",
        "runs = []",
        "runs.append(execute_arrange_request(comp_obj, fusion_obj, resolve_obj, state, result_ask=ask, title=CONFIG['title'], log=log))",
        "post_first = snapshot(comp_obj)",
        "if CONFIG['run_second']:",
        "    runs.append(execute_arrange_request(comp_obj, fusion_obj, resolve_obj, state, result_ask=ask, title=CONFIG['title'], log=log))",
        "post_second = snapshot(comp_obj)",
        "undo_snapshots = []",
        "if CONFIG['undo_after_runs']:",
        "    for _ in range(3):",
        "        undo = getattr(comp_obj, 'Undo', None)",
        "        if not callable(undo): break",
        "        try:",
        "            if undo() is False: break",
        "        except Exception: break",
        "        undo_snapshots.append(snapshot(comp_obj))",
        "payload = {'schema': CONFIG['schema'], 'state': {'include_unselected': state.include_unselected, 'ungroup': state.ungroup},",
        "           'pre': pre, 'runs': [item.to_dict() for item in runs], 'post_first': post_first,",
        "           'post_second': post_second, 'undo_snapshots': undo_snapshots, 'log': log_lines}",
        "Path(OUTPUT).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')",
        "print(json.dumps(payload, ensure_ascii=False))",
    ]
    return "\n".join(lines) + "\n"


def classify_behavior(payload: dict[str, Any]) -> dict[str, Any]:
    """Turn sidecar handler output into the stable evidence-layer shape."""
    runs = payload.get("runs") or []
    first = runs[0] if runs else {}
    second = runs[1] if len(runs) > 1 else {}
    pre = payload.get("pre") or {}
    post = payload.get("post_first") or {}
    selected = set(pre.get("selected") or [])
    positions = pre.get("positions") or {}
    unselected = set(positions) - selected
    state = payload.get("state") or {}
    include_unselected = bool(state.get("include_unselected", True))
    fixture_shape = len(positions) >= 4
    selection_fixture_shape = len(selected) >= 4 and len(unselected) >= 1
    selected_moved = any(positions.get(name) != (post.get("positions") or {}).get(name) for name in selected)
    unselected_unchanged = all(positions.get(name) == (post.get("positions") or {}).get(name) for name in unselected)
    edges_unchanged = pre.get("connections") == post.get("connections")
    parents_unchanged = pre.get("parents") == post.get("parents")
    tool_identities_unchanged = set(positions) == set(post.get("positions") or {})
    second_zero = bool(second) and second.get("result", {}).get("moved_count") == 0
    first_pass = first.get("status") == "success"
    arranged_count = first.get("result", {}).get("arranged_count")
    whole_comp_scope_complete = (
        fixture_shape
        and first_pass
        and tool_identities_unchanged
        and arranged_count == len(positions)
    )
    undo_exact = any(
        item.get("positions") == pre.get("positions")
        and item.get("connections") == pre.get("connections")
        and item.get("parents") == pre.get("parents")
        for item in (payload.get("undo_snapshots") or [])
    )
    if include_unselected:
        behavior_status = "PASS" if whole_comp_scope_complete and first.get("result", {}).get("moved_count", 0) > 0 else "UNVERIFIED"
    else:
        behavior_status = "PASS" if selection_fixture_shape and first_pass and selected_moved and unselected_unchanged else "UNVERIFIED"
    invariant_status = (
        "PASS"
        if behavior_status == "PASS" and edges_unchanged and parents_unchanged and second_zero and undo_exact
        else "UNVERIFIED"
    )
    return {
        "schema": SCHEMA,
        "UI_VISIBILITY": {
            "status": "NOT_RUN_DIRECT_HANDLER",
            "note": "UIA/MSAA visibility is recorded by the existing verifier; no control was invoked here.",
        },
        "HOST_PRODUCT_BEHAVIOR": {
            "status": behavior_status,
            "handler": "execute_arrange_request",
            "state": state,
            "scope_mode": "whole_comp" if include_unselected else "selection_only_experimental",
            "first_status": first.get("status"),
            "first_moved": first.get("result", {}).get("moved_count") if first else None,
            "arranged_count": arranged_count,
            "whole_comp_scope_complete": whole_comp_scope_complete,
            "second_moved": second.get("result", {}).get("moved_count") if second else None,
            "effective_include_unselected": "PASS_BEHAVIORAL" if behavior_status == "PASS" else "UNVERIFIED",
            "effective_ungroup": (
                "PASS_BEHAVIORAL"
                if first_pass and bool(pre.get("groups")) and parents_unchanged and edges_unchanged
                else "UNVERIFIED"
            ),
        },
        "HOST_INVARIANTS": {
            "status": invariant_status,
            "selected_only_movement": selected_moved,
            "unselected_unchanged": unselected_unchanged,
            "whole_comp_scope_complete": whole_comp_scope_complete,
            "tool_identities_unchanged": tool_identities_unchanged,
            "connections_unchanged": edges_unchanged,
            "group_membership_unchanged": parents_unchanged,
            "second_run_moved_zero": second_zero,
            "undo_exact": undo_exact,
            "undo_snapshots": payload.get("undo_snapshots", []),
        },
        "ACCESSIBILITY_LIMITATION": {
            "status": "BLOCKED_HOST_ACCESSIBILITY_HARD",
            "run_cancel_checkbox_identity": "BLOCKED_HOST_ACCESSIBILITY_HARD",
        },
    }


def emit(record: dict[str, Any], output: str | None = None) -> None:
    record = dict(record)
    record.setdefault("ts", datetime.datetime.now().isoformat(timespec="seconds"))
    line = json.dumps(record, ensure_ascii=False)
    print(line)
    if output:
        Path(output).write_text(line + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    source = sub.add_parser("source")
    source.add_argument("--output", required=True)
    source.add_argument("--source-file")
    scope = source.add_mutually_exclusive_group()
    scope.add_argument(
        "--include-unselected", dest="include_unselected", action="store_true",
        default=True, help="arrange the whole active composition (default)",
    )
    scope.add_argument(
        "--selection-only", dest="include_unselected", action="store_false",
        help="experimental regression lane: arrange only the explicit selection",
    )
    source.add_argument("--ungroup", action="store_true")
    source.add_argument("--no-second", action="store_true")
    source.add_argument("--no-undo", action="store_true")
    classify = sub.add_parser("classify")
    classify.add_argument("--input", required=True)
    classify.add_argument("--output")
    args = parser.parse_args(argv)
    if args.command == "source":
        text = build_handler_source(
            args.output,
            include_unselected=args.include_unselected,
            ungroup=args.ungroup,
            run_second=not args.no_second,
            undo_after_runs=not args.no_undo,
        )
        if args.source_file:
            Path(args.source_file).write_text(text, encoding="utf-8")
        else:
            sys.stdout.write(text)
        return
    payload = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
    classified = classify_behavior(payload)
    if args.output:
        Path(args.output).write_text(json.dumps(classified, ensure_ascii=False, indent=2), encoding="utf-8")
    emit(classified)


if __name__ == "__main__":
    main()
