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

Every run appends one line plus any traceback to
<Fusion Support>/ResolveNodeKit/logs/arrange-run.log (or the system temp
directory for the repo fallback), so a silent menu press stays diagnosable.

Automated canary override (no dialog click needed):

    RNK_ARRANGE_NO_UI=1
    RNK_ARRANGE_INCLUDE_UNSELECTED=0|1 (default 0)
    RNK_ARRANGE_UNGROUP=0|1 (default 0; 1 stays fail-closed until host-proven)
"""
from __future__ import annotations

import datetime
import os
import sys
import traceback
from pathlib import Path


TITLE = "ResolveNodeKit - Arrange"
LABEL_INCLUDE = "選択されていないノードも整列"
LABEL_UNGROUP = "グループ化を解除して整列"
RUN_LOG_NAME = "arrange-run.log"


def _script_file():
    try:
        return Path(__file__).resolve()
    except Exception:
        return None


def _walk_up_to_fusion(start):
    try:
        current = Path(start)
    except Exception:
        return None
    for parent in [current.parent, *current.parents]:
        try:
            if parent.name == "Fusion":
                return parent
        except Exception:
            continue
    return None


def _root_from_host_map(fusion_obj=None):
    try:
        target = fusion_obj or globals().get("fusion") or globals().get("fu")
        if target is None:
            resolver = globals().get("resolve")
            if resolver is not None:
                target = resolver.Fusion()
        if target is None:
            return None
        mapper = getattr(target, "MapPath", None)
        if not callable(mapper):
            return None
        for key in ("Scripts:", "Comp:"):
            try:
                mapped = mapper(key)
            except Exception:
                continue
            if mapped:
                root = _walk_up_to_fusion(Path(str(mapped)))
                if root is not None:
                    return root
    except Exception:
        pass
    return None


def _root_from_appdata():
    try:
        base = os.environ.get("APPDATA", "")
        if not base:
            return None
        root = Path(base) / "Blackmagic Design" / "DaVinci Resolve" / "Support" / "Fusion"
        return root if root.is_dir() else None
    except Exception:
        return None


def _fusion_support_root(script_file=None):
    here = script_file or _script_file()
    if here is not None:
        root = _walk_up_to_fusion(here)
        if root is not None:
            return root
    root = _root_from_host_map()
    if root is not None:
        return root
    return _root_from_appdata()


def _candidate_src_dirs(script_file=None):
    found = []
    override = os.environ.get("RNK_SUPPORT_ROOT", "")
    if override:
        found.append(Path(override) / "ResolveNodeKit" / "src")
    root = _fusion_support_root(script_file)
    if root is not None:
        found.append(root / "ResolveNodeKit" / "src")
    here = script_file or _script_file()
    if here is not None:
        try:
            found.append(here.parents[2] / "src")
        except IndexError:
            pass
    return found


def _bootstrap_package(script_file=None):
    for candidate in _candidate_src_dirs(script_file):
        try:
            if candidate.is_dir():
                if str(candidate) not in sys.path:
                    sys.path.insert(0, str(candidate))
                return str(candidate)
        except Exception:
            continue
    return ""


def _log_file(script_file=None):
    root = _fusion_support_root(script_file)
    override = os.environ.get("RNK_SUPPORT_ROOT", "")
    if override:
        root = Path(override)
    if root is not None:
        try:
            logs = Path(root) / "ResolveNodeKit" / "logs"
            logs.mkdir(parents=True, exist_ok=True)
            return logs / RUN_LOG_NAME
        except Exception:
            pass
    try:
        import tempfile
        return Path(tempfile.gettempdir()) / ("rnk-" + RUN_LOG_NAME)
    except Exception:
        return None


def _write_log(status, detail=""):
    try:
        path = _log_file()
        if path is None:
            return ""
        stamp = datetime.datetime.now().isoformat(timespec="seconds")
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(stamp + " " + status + (" " + detail if detail else "") + "\n")
        return str(path)
    except Exception:
        return ""


_BOOTSTRAPPED_FROM = _bootstrap_package()

try:
    from resolve_node_kit.fusion import ArrangeDialogState, FusionHostError, arrange_comp
    from resolve_node_kit.fusion import ask_arrange_options
    from resolve_node_kit.fusion.dialog import BUSY_INITIAL_TEXT, show_busy_window, set_busy_text, hide_busy_window, show_result, stage_text, bind_target, TargetMismatch
    _IMPORT_ERROR = ""
except Exception as exc:
    ArrangeDialogState = None
    FusionHostError = RuntimeError
    arrange_comp = None
    ask_arrange_options = None
    BUSY_INITIAL_TEXT = "..."
    show_busy_window = None
    set_busy_text = None
    hide_busy_window = None
    show_result = None
    bind_target = None
    TargetMismatch = RuntimeError
    stage_text = lambda phase: "..."
    _IMPORT_ERROR = repr(exc)


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
    resolve_obj = globals().get("resolve")
    if resolve_obj is not None:
        try:
            fusion_obj = resolve_obj.Fusion()
            getter = getattr(fusion_obj, "GetCurrentComp", None)
            if callable(getter):
                return getter()
        except Exception:
            return None
    return None


def _state_from_env():
    return ArrangeDialogState(
        include_unselected=os.environ.get("RNK_ARRANGE_INCLUDE_UNSELECTED", "0") == "1",
        ungroup=os.environ.get("RNK_ARRANGE_UNGROUP", "0") == "1",
    )


def _fusion_handle():
    fusion_obj = globals().get("fusion") or globals().get("fu")
    if fusion_obj is not None:
        return fusion_obj
    resolve_obj = globals().get("resolve")
    if resolve_obj is not None:
        try:
            return resolve_obj.Fusion()
        except Exception:
            return None
    return None


def _run():
    _write_log("start", "name=" + __name__ + " src=" + _BOOTSTRAPPED_FROM)
    if _IMPORT_ERROR or arrange_comp is None:
        message = "package import failed: " + (_IMPORT_ERROR or "unknown")
        print("[ResolveNodeKit] Arrange: " + message)
        _write_log("import-error", _IMPORT_ERROR)
        return 4
    ui_comp = _current_comp()
    if ui_comp is None:
        print("[ResolveNodeKit] Arrange: no active Fusion composition. Open a comp and run again.")
        _write_log("no-comp", "")
        return 2

    if os.environ.get("RNK_ARRANGE_NO_UI", "0") == "1":
        state = _state_from_env()
    else:
        ui_ask = getattr(ui_comp, "AskUser", None)
        if not callable(ui_ask):
            print("[ResolveNodeKit] Arrange: dialog is unavailable on this host; nothing changed.")
            _write_log("no-dialog", "")
            return 2
        state = ask_arrange_options(
            ui_ask, TITLE, LABEL_INCLUDE, LABEL_UNGROUP,
            log=lambda message: _write_log("dialog", message),
        )
        if state is None:
            print("[ResolveNodeKit] Arrange canceled; nothing changed.")
            _write_log("cancel", "")
            return 0
    try:
        composition = bind_target(
            ui_comp,
            globals().get("fusion") or globals().get("fu"),
            globals().get("resolve"),
            log=lambda message: _write_log("target", message),
            require_live=True,
        )
    except TargetMismatch as exc:
        print("[ResolveNodeKit] Arrange: target mismatch between menu comp and live current; nothing changed.")
        _write_log("target-mismatch", str(exc))
        ui_ask = getattr(ui_comp, "AskUser", None)
        if callable(show_result) and callable(ui_ask):
            show_result(
                ui_ask, TITLE,
                "整列できませんでした。中止し、変更はありません。" + "\n" + str(exc),
                log=lambda message: _write_log("result", message),
            )
        return 5
    if composition is None:
        print("[ResolveNodeKit] Arrange: no active Fusion composition. Open a comp and run again.")
        _write_log("no-comp", "")
        return 2
    try:
        describe = getattr(composition, "GetAttrs", lambda: {})()
        comp_name = (describe or {}).get("COMPS_Name", "?")
    except Exception:
        comp_name = "?"
    try:
        tool_list = composition.GetToolList()
        comp_tools = len(tool_list.values()) if isinstance(tool_list, dict) else len(list(tool_list))
    except Exception:
        comp_tools = -1
    _write_log("target", "comp=" + str(comp_name) + " tools=" + str(comp_tools))
    busy = None
    if callable(show_busy_window):
        busy = show_busy_window(
            _fusion_handle(), TITLE, BUSY_INITIAL_TEXT,
            log=lambda message: _write_log("busy", message),
        )

    def _on_progress(message):
        _write_log("arrange", message)
        try:
            if callable(set_busy_text):
                set_busy_text(busy, stage_text(message))
        except Exception:
            pass

    ask = getattr(composition, "AskUser", None)
    outcome = None
    exit_code = 1
    try:
        try:
            result = arrange_comp(
                composition,
                include_unselected=state.include_unselected,
                ungroup=state.ungroup,
                progress=_on_progress,
            )
        except FusionHostError as exc:
            print("[ResolveNodeKit] Arrange refused: " + str(exc))
            _write_log("refused", str(exc))
            outcome = "整列できませんでした。中止し、変更はありません。" + "\n" + str(exc)
            exit_code = 3
        else:
            diag = result.get("diagnostics", {})
            template = "[ResolveNodeKit] Arrange: nodes=%s edges=%s moved=%s arranged=%s avoidable_diagonals=%s expanded_gaps=%s"
            summary = template % (
                result.get("node_count"),
                result.get("edge_count"),
                result.get("moved_count"),
                result.get("arranged_count"),
                diag.get("avoidable_diagonal_edge_count"),
                diag.get("expanded_gap_count"),
            )
            print(summary)
            _write_log("ok", summary)
            if result.get("moved_count"):
                outcome = "整列しました。" + summary
            else:
                outcome = "すでに整列済みのため、移動はありませんでした。" + summary
            exit_code = 0
    finally:
        if callable(hide_busy_window):
            try:
                hide_busy_window(busy, log=lambda message: _write_log("busy", message))
            except Exception:
                pass
    if outcome is not None and callable(show_result):
        show_result(ask, TITLE, outcome, log=lambda message: _write_log("result", message))
    return exit_code



try:
    _EXIT_CODE = _run()
except Exception:
    _write_log("traceback", traceback.format_exc(limit=8).replace("\n", " | "))
    print("[ResolveNodeKit] Arrange failed unexpectedly; see the run log.")
    _EXIT_CODE = 1
print("[ResolveNodeKit] Arrange exit=" + str(_EXIT_CODE))
raise SystemExit(_EXIT_CODE)
