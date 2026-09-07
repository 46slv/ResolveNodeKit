#!/usr/bin/env python3
"""ResolveNodeKit arrange UIA end-to-end verifier (Phase B).

Dependency-free (stdlib only). Drives the live DaVinci Resolve UI through
Windows UI Automation via powershell.exe subprocesses -- no coordinate
clicks, no blind keystrokes, no global shortcut changes, no watchers.

Every subcommand prints one machine-readable JSON record to stdout and,
with --evidence FILE, appends it as one JSON line. Agent-side (Fusion/MCP)
steps are recorded with the `record` subcommand so the final evidence file
covers all 20 E2E steps in one place. `assemble` folds the JSONL into a
single {"steps": [...]} document.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile
import time

TITLE = "ResolveNodeKit - Arrange"
ENTRY_NAME = "ResolveNodeKit_Arrange"
SCRIPTS_CODEPOINTS = (0x30B9, 0x30AF, 0x30EA, 0x30D7, 0x30C8)
MENU_WS_INDEX = 12
WORKSPACE_NAMES = ("ワークスペース", "Workspace")
SCRIPTS_NAMES = ("スクリプト", "Scripts")
COMP_NAMES = ("Comp", "コンポ")
ARRANGE_LABELS = (
    "選択されていないノードも整列",
    "グループ化を解除して整列",
)
RUN_BUTTON_NAMES = ("Run", "OK", "実行", "適用")
CANCEL_BUTTON_NAMES = ("Cancel", "キャンセル", "中止")

PS_PRELUDE = (
    "Add-Type -AssemblyName UIAutomationClient\n"
    "Add-Type -AssemblyName UIAutomationTypes\n"
    "$ErrorActionPreference = 'Stop'\n"
    "$TrueCond = [System.Windows.Automation.Condition]::TrueCondition\n"
)


def _run_ps(script, timeout):
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".ps1", delete=False, encoding="utf-8-sig"
    ) as fh:
        fh.write(script)
        path = fh.name
    try:
        proc = subprocess.run(
            ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass",
             "-File", path],
            capture_output=True, timeout=timeout,
        )
        return (proc.returncode == 0,
                proc.stdout.decode("utf-8", errors="replace"),
                proc.stderr.decode("utf-8", errors="replace"))
    except subprocess.TimeoutExpired as exc:
        out = (exc.stdout or b"").decode("utf-8", errors="replace")
        err = (exc.stderr or b"").decode("utf-8", errors="replace")
        return False, out, "TIMEOUT: " + err
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def _now_iso():
    return datetime.datetime.now().isoformat(timespec="seconds")


def _emit(record, evidence):
    record = dict(record)
    record.setdefault("ts", _now_iso())
    sys.stdout.write(json.dumps(record, ensure_ascii=False) + "\n")
    sys.stdout.flush()
    if evidence:
        with open(evidence, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


PS_FIND_MAIN = PS_PRELUDE + (
    "$r = Get-Process | Where-Object { $_.ProcessName -eq 'Resolve' } "
    "| Select-Object -First 1\n"
    "if (-not $r) { Write-Output '{\"ok\":false}'; exit 0 }\n"
    "$root = [System.Windows.Automation.AutomationElement]::RootElement\n"
    "$el = $null\n"
    "for ($try = 0; $try -lt 20 -and -not $el; $try++) {\n"
    "  $el = @($root.FindAll([System.Windows.Automation.TreeScope]::Children, $TrueCond) | Where-Object { try { $_.Current.ProcessId -eq $r.Id -and [string]$_.Current.ClassName -eq 'UiMainWindowImp' } catch { $false } }) | Select-Object -First 1\n"
    "  if (-not $el) { Start-Sleep -Milliseconds 200 }\n"
    "}\n"
    "if (-not $el) { Write-Output '{\"ok\":false,\"reason\":\"no main window\"}'; exit 0 }\n"
    "$o = [ordered]@{ok=$true; pid=$r.Id; "
    "hwnd=$el.Current.NativeWindowHandle; "
    "title=[string]$r.MainWindowTitle; "
    "uia_name=[string]$el.Current.Name; "
    "uia_automation_id=[string]$el.Current.AutomationId; "
    "uia_class=[string]$el.Current.ClassName}\n"
    "Write-Output ($o | ConvertTo-Json -Compress)\n"
)


def cmd_bind(args):
    ok, out, err = _run_ps(PS_FIND_MAIN, args.timeout)
    try:
        data = json.loads(out.strip().splitlines()[-1])
    except Exception:
        data = {"ok": False, "raw": out[-300:], "stderr": err[-300:]}
    rec = {"step": args.step, "op": "uia-bind", "transport_ok": ok}
    if isinstance(data, dict):
        rec.update(data)
    rec["status"] = ("PASS" if (ok and data.get("ok")
                                and data.get("uia_automation_id") == "UiMainWindow")
                     else "FAIL")
    return _emit(rec, args.evidence)


PS_MENU_INVOKE = PS_PRELUDE + (
    "$SC = -join [char[]](__SC__)\n"
    "$itemCond = New-Object System.Windows.Automation.PropertyCondition(\n"
    "  [System.Windows.Automation.AutomationElement]::ControlTypeProperty,\n"
    "  [System.Windows.Automation.ControlType]::MenuItem)\n"
    "$r = Get-Process | Where-Object { $_.ProcessName -eq 'Resolve' } "
    "| Select-Object -First 1\n"
    "$root = [System.Windows.Automation.AutomationElement]::RootElement\n"
    "$main = $null\n"
    "for ($try = 0; $try -lt 20 -and -not $main; $try++) {\n"
    "  $main = @($root.FindAll([System.Windows.Automation.TreeScope]::Children, $TrueCond) | Where-Object { try { $_.Current.ProcessId -eq $r.Id -and [string]$_.Current.ClassName -eq 'UiMainWindowImp' } catch { $false } }) | Select-Object -First 1\n"
    "  if (-not $main) { Start-Sleep -Milliseconds 200 }\n"
    "}\n"
    "if (-not $main) { Write-Output '{\"ok\":false,\"reason\":\"no main window\"}'; exit 0 }\n"
    "$itemType = [System.Windows.Automation.ControlType]::MenuItem\n"
    "$bar = $null\n"
    "for ($try = 0; $try -lt 15 -and -not $bar; $try++) {\n"
    "  try { $bar = @($main.FindAll([System.Windows.Automation.TreeScope]::Children, $TrueCond) | Where-Object { $_.Current.ControlType -eq [System.Windows.Automation.ControlType]::MenuBar }) | Select-Object -First 1 } catch {}\n"
    "  if (-not $bar) { Start-Sleep -Milliseconds 200 }\n"
    "}\n"
    "if (-not $bar) "
    "{ Write-Output '{\"ok\":false,\"reason\":\"no menubar\"}'; exit 0 }\n"
    "$tops = @($bar.FindAll([System.Windows.Automation.TreeScope]::Children, $TrueCond) "
    "| Where-Object { $_.Current.ControlType -eq $itemType })\n"
    "function Info($e) {\n"
    "  $p = @(); try { foreach ($t in $e.GetSupportedPatterns()) "
    "{ $p += [string]$t.ProgrammaticName } } catch {}\n"
    "  [ordered]@{name=[string]$e.Current.Name; control_type=[string]$e.Current.ControlType.ProgrammaticName; "
    "class_name=[string]$e.Current.ClassName; automation_id=[string]$e.Current.AutomationId; "
    "enabled=[string]$e.Current.IsEnabled; offscreen=[string]$e.Current.IsOffscreen; patterns=($p -join ',')}\n"
    "}\n"
    "function ExpandMenu($e, $label) {\n"
    "  $state = ''; try { $state = [string]$e.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern).Current.ExpandCollapseState } catch { return \"${label}:unsupported\" }\n"
    "  if ($state -eq 'Collapsed' -or $state -eq 'PartiallyExpanded') {\n"
    "    try { $e.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern).Expand(); Start-Sleep -Milliseconds 900; return \"${label}:$state->Expanded\" } catch { return \"${label}:expand-failed\" }\n"
    "  }\n"
    "  return \"${label}:$state\"\n"
    "}\n"
    "function MenuItemsUnder($e) {\n"
    "  $desc = @($e.FindAll([System.Windows.Automation.TreeScope]::Descendants, $itemCond))\n"
    "  if ($desc.Count -gt 0) { return $desc }\n"
    "  $kids = @($e.FindAll([System.Windows.Automation.TreeScope]::Children, $TrueCond))\n"
    "  return @($kids | Where-Object { $_.Current.ControlType -eq $itemType })\n"
    "}\n"
    "$ws = $tops | Where-Object { $n=[string]$_.Current.Name; $n -eq 'ワークスペース' -or $n -eq 'Workspace' } | Select-Object -First 1\n"
    "$ws_method = 'name'\n"
    "if (-not $ws -and $tops.Count -gt __WS__) { $ws = $tops[__WS__]; $ws_method = 'indexed-fallback' }\n"
    "if (-not $ws) { Write-Output '{\"ok\":false,\"reason\":\"no workspace\"}'; exit 0 }\n"
    "$states = @(); $states += (ExpandMenu $ws 'workspace')\n"
    "$items = @(MenuItemsUnder $ws)\n"
    "$sc = $items | Where-Object { $n=[string]$_.Current.Name; $n -eq $SC -or $n -eq 'Scripts' } | Select-Object -First 1\n"
    "if (-not $sc) { Write-Output '{\"ok\":false,\"reason\":\"no scripts\",\"workspace\":' + (($ws | ForEach-Object { (Info $_ | ConvertTo-Json -Compress) }) ) + '}'; exit 0 }\n"
    "$path = @((Info $ws)); $states += (ExpandMenu $sc 'scripts'); $path += (Info $sc)\n"
    "$items2 = @(MenuItemsUnder $sc)\n"
    "$cp = $items2 | Where-Object { $n=[string]$_.Current.Name; $n -eq 'Comp' -or $n -eq 'コンポ' } | Select-Object -First 1\n"
    "$names_after_scripts = @($items2 | ForEach-Object { try { [string]$_.Current.Name } catch { '' } } | Where-Object { $_ -ne '' })\n"
    "$comp_candidates = @($sc.FindAll([System.Windows.Automation.TreeScope]::Descendants, $TrueCond) | Where-Object { try { [string]$_.Current.Name -eq 'Comp' -or [string]$_.Current.Name -eq 'コンポ' } catch { $false } } | ForEach-Object { Info $_ })\n"
    "if (-not $cp) {\n"
    "  $direct = $items2 | Where-Object { try { [string]$_.Current.Name -eq '__ENTRY__' } catch { $false } } | Select-Object -First 1\n"
    "  if (-not $direct) { $d = [ordered]@{ok=$false; reason='no comp-or-entry'; names_after_scripts=$names_after_scripts; comp_candidates=$comp_candidates; script=Info $sc}; Write-Output ($d | ConvertTo-Json -Depth 8 -Compress); exit 0 }\n"
    "  $directPath = @((Info $ws),(Info $sc),(Info $direct))\n"
    "  $directInvoke = $direct.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern); $directInvoke.Invoke()\n"
    "  $directOut = [ordered]@{ok=$true; path=$directPath; workspace_selection=$ws_method; route='workspace>scripts>entry-direct'; expected_category='Comp'; category_element_exposed=$false; states=$states; entry_class=[string]$direct.Current.ClassName; entry_patterns=((Info $direct).patterns); entry_enabled=[string]$direct.Current.IsEnabled; entry_offscreen=[string]$direct.Current.IsOffscreen}\n"
    "  try { $sc.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern).Collapse() } catch {}\n"
    "  try { $ws.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern).Collapse() } catch {}\n"
    "  Write-Output ($directOut | ConvertTo-Json -Depth 8 -Compress); exit 0\n"
    "}\n"
    "$states += (ExpandMenu $cp 'comp'); $path += (Info $cp)\n"
    "$items3 = @(MenuItemsUnder $cp)\n"
    "$rnk = $items3 | Where-Object { try { [string]$_.Current.Name -eq '__ENTRY__' } catch { $false } } | Select-Object -First 1\n"
    "if (-not $rnk) { Write-Output '{\"ok\":false,\"reason\":\"no entry\"}'; exit 0 }\n"
    "$path += (Info $rnk)\n"
    "$invoke = $rnk.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern); $invoke.Invoke()\n"
    "$o = [ordered]@{ok=$true; path=$path; workspace_selection=$ws_method; states=$states; "
    "entry_class=[string]$rnk.Current.ClassName; entry_patterns=((Info $rnk).patterns); "
    "entry_enabled=[string]$rnk.Current.IsEnabled; entry_offscreen=[string]$rnk.Current.IsOffscreen}\n"
    "try { $cp.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern).Collapse() } catch {}\n"
    "try { $sc.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern).Collapse() } catch {}\n"
    "try { $ws.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern).Collapse() } catch {}\n"
    "Write-Output ($o | ConvertTo-Json -Depth 8 -Compress)\n"
)


def cmd_menu_invoke(args):
    script = (PS_MENU_INVOKE
              .replace("__SC__", ",".join(str(c) for c in SCRIPTS_CODEPOINTS))
              .replace("__WS__", str(MENU_WS_INDEX))
              .replace("__ENTRY__", ENTRY_NAME))
    ok, out, err = _run_ps(script, args.timeout)
    try:
        data = json.loads(out.strip().splitlines()[-1])
    except Exception:
        data = {"ok": False, "raw": out[-300:], "stderr": err[-300:]}
    rec = {"step": args.step, "op": "menu-invoke", "transport_ok": ok}
    if isinstance(data, dict):
        rec.update(data)
    rec["status"] = "PASS" if (ok and data.get("ok")) else "FAIL"
    return _emit(rec, args.evidence)


PS_WINDOWS = PS_PRELUDE + (
    "$r = Get-Process | Where-Object { $_.ProcessName -eq 'Resolve' } "
    "| Select-Object -First 1\n"
    "$root = [System.Windows.Automation.AutomationElement]::RootElement\n"
    "$rows = @()\n"
    "$top = @($root.FindAll([System.Windows.Automation.TreeScope]::Children, $TrueCond))\n"
    "$main = $top | Where-Object { try { $_.Current.ProcessId -eq $r.Id -and [string]$_.Current.ClassName -eq 'UiMainWindowImp' } catch { $false } } | Select-Object -First 1\n"
    "$seen = @{}\n"
    "foreach ($w in ($top | Where-Object { try { $_.Current.ProcessId -eq $r.Id } catch { $false } })) {\n"
    "  try { $nm = [string]$w.Current.Name; $ct = [string]$w.Current.ControlType.ProgrammaticName; $cl = [string]$w.Current.ClassName } catch { continue }\n"
    "  $key = $nm + '|' + $ct + '|' + $cl\n"
    "  if (-not $seen.ContainsKey($key)) { $seen[$key] = $true; $rows += [ordered]@{name=$nm; control=$ct; class=$cl; source='desktop'} }\n"
    "}\n"
    "if ($main) {\n"
    "  $desc = @($main.FindAll([System.Windows.Automation.TreeScope]::Descendants, $TrueCond) | Where-Object { try { $_.Current.ControlType -eq [System.Windows.Automation.ControlType]::Window } catch { $false } })\n"
    "  foreach ($w in $desc) {\n"
    "    try { $nm = [string]$w.Current.Name; $ct = [string]$w.Current.ControlType.ProgrammaticName; $cl = [string]$w.Current.ClassName } catch { continue }\n"
    "    $key = $nm + '|' + $ct + '|' + $cl\n"
    "    if (-not $seen.ContainsKey($key)) { $seen[$key] = $true; $rows += [ordered]@{name=$nm; control=$ct; class=$cl; source='main-descendant'} }\n"
    "  }\n"
    "}\n"
    "Write-Output (@{owned=$rows} | ConvertTo-Json -Depth 4 -Compress)\n"
)


def _owned_windows(timeout):
    ok, out, err = _run_ps(PS_WINDOWS, timeout)
    try:
        data = json.loads(out.strip().splitlines()[-1])
        owned = data.get("owned", [])
    except Exception:
        return False, [], out[-300:] + err[-300:]
    if isinstance(owned, dict):
        owned = [owned]
    return ok, owned, ""


def cmd_wait_window(args):
    deadline = time.time() + args.timeout
    last_owned, elapsed = [], 0.0
    while True:
        remaining = deadline - time.time()
        if remaining <= 0:
            break
        # Keep the subprocess probe inside the caller's deadline.  The old
        # fixed 30-second probe made a short fail-closed wait appear to hang.
        probe_timeout = min(30, max(1, int(remaining + 0.999)))
        _ok, owned, note = _owned_windows(probe_timeout)
        last_owned = owned
        hits = [w for w in owned if w.get("name") == args.title]
        elapsed = round(args.timeout - (deadline - time.time()), 2)
        if args.absent and not hits:
            return _emit({"step": args.step, "op": "wait-window-absent",
                           "title": args.title, "found": False,
                           "elapsed_s": elapsed, "status": "PASS"},
                          args.evidence)
        if not args.absent and hits:
            return _emit({"step": args.step, "op": "wait-window",
                           "title": args.title, "found": True,
                           "elapsed_s": elapsed, "window": hits[0],
                           "status": "PASS"}, args.evidence)
        if time.time() >= deadline:
            break
        time.sleep(args.poll)
    return _emit({"step": args.step,
                   "op": ("wait-window-absent" if args.absent
                          else "wait-window"),
                   "title": args.title, "found": False,
                   "elapsed_s": elapsed, "owned_snapshot": last_owned,
                   "status": "FAIL"}, args.evidence)


PS_DUMP = PS_PRELUDE + (
    "$title = '__TITLE__'\n"
    "$r = Get-Process | Where-Object { $_.ProcessName -eq 'Resolve' } "
    "| Select-Object -First 1\n"
    "$root = [System.Windows.Automation.AutomationElement]::RootElement\n"
    "$top = @($root.FindAll([System.Windows.Automation.TreeScope]::Children, $TrueCond))\n"
    "$win = $top | Where-Object { try { ($_.Current.ProcessId -eq $r.Id) -and ([string]$_.Current.Name -eq $title) } catch { $false } } | Select-Object -First 1\n"
    "if (-not $win) {\n"
    "  $main = $top | Where-Object { try { $_.Current.ProcessId -eq $r.Id -and [string]$_.Current.ClassName -eq 'UiMainWindowImp' } catch { $false } } | Select-Object -First 1\n"
    "  if ($main) { $win = $main.FindAll([System.Windows.Automation.TreeScope]::Descendants, $TrueCond) | Where-Object { try { ([string]$_.Current.Name -eq $title) -and ($_.Current.ControlType -eq [System.Windows.Automation.ControlType]::Window) } catch { $false } } | Select-Object -First 1 }\n"
    "}\n"
    "if (-not $win) "
    "{ Write-Output '{\"ok\":false}'; exit 0 }\n"
    "$desc = @($win.FindAll([System.Windows.Automation.TreeScope]"
    "::Descendants, $TrueCond))\n"
    "$rows = @()\n"
    "foreach ($d in $desc) {\n"
    "  try { $nm = [string]$d.Current.Name } catch { $nm = '' }\n"
    "  try { $ct = [string]$d.Current.ControlType.ProgrammaticName }"
    " catch { $ct = '' }\n"
    "  try { $cl = [string]$d.Current.ClassName } catch { $cl = '' }\n"
    "  try { $aid = [string]$d.Current.AutomationId } catch { $aid = '' }\n"
    "  try { $help = [string]$d.Current.HelpText } catch { $help = '' }\n"
    "  $label = ''\n"
    "  try { if ($d.Current.LabeledBy) { $label = [string]$d.Current.LabeledBy.Current.Name } } catch {}\n"
    "  $tg = ''\n"
    "  try { $tg = [string]$d.GetCurrentPattern([System.Windows.Automation"
    ".TogglePattern]::Pattern).Current.ToggleState } catch {}\n"
    "  $val = ''\n"
    "  try { $val = [string]$d.GetCurrentPattern([System.Windows.Automation"
    ".ValuePattern]::Pattern).Current.Value } catch {}\n"
    "  $p = @(); try { foreach ($t in $d.GetSupportedPatterns()) "
    "{ $p += [string]$t.ProgrammaticName } } catch {}\n"
    "  $row = [ordered]@{name=$nm; control=$ct; class=$cl; automation_id=$aid; "
    "help_text=$help; labeled_by=$label; patterns=($p -join ','); toggle=$tg}\n"
    "  if ($val.Length -gt 0 -and $val.Length -lt 2000) "
    "{ $row.value = $val }\n"
    "  $rows += $row\n"
    "}\n"
    "$o = [ordered]@{ok=$true; node_count=$rows.Count; nodes=$rows}\n"
    "$json = ($o | ConvertTo-Json -Depth 5 -Compress)\n"
    "[System.IO.File]::WriteAllText('__OUT__', $json, "
    "[System.Text.Encoding]::UTF8)\n"
    "Write-Output ('{\"ok\":true,\"node_count\":' + $rows.Count + '}')\n"
)


def _dump_window(title, timeout):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json",
                                      delete=False) as fh:
        out_path = fh.name
    script = PS_DUMP.replace("__TITLE__", title).replace(
        "__OUT__", out_path.replace("\\", "\\\\"))
    ok, out, err = _run_ps(script, timeout)
    try:
        with open(out_path, encoding="utf-8-sig") as fh:
            data = json.load(fh)
    except Exception:
        data = {"ok": False, "raw": out[-300:], "stderr": err[-300:]}
    finally:
        try:
            os.unlink(out_path)
        except OSError:
            pass
    nodes = data.get("nodes", [])
    if isinstance(nodes, dict):
        nodes = [nodes]
    return ok and data.get("ok", False), nodes, data


def classify_window(nodes):
    """Pure helper: setup/result/busy/other from a UIA descendant dump."""
    checkbox_candidates = [
        n for n in nodes
        if n.get("control") == "ControlType.CheckBox"
        or "CheckBox" in (n.get("class") or "")
    ]
    exposed_labels = sorted({
        value
        for n in nodes
        for value in (n.get("name"), n.get("value"))
        if value in ARRANGE_LABELS
    })
    has_check = len(checkbox_candidates) >= 2
    has_result = any(n.get("name") == "Result"
                     and "Text" in (n.get("control") or "") for n in nodes)
    buttons = sorted({n.get("name", "") for n in nodes
                      if n.get("control") == "ControlType.Button"})
    button_candidates = [
        n for n in nodes
        if n.get("control") == "ControlType.Button"
        or "Button" in (n.get("class") or "")
    ]
    named_invoke_buttons = [
        n for n in button_candidates
        if n.get("name") and "InvokePatternIdentifiers.Pattern" in (n.get("patterns") or "")
    ]
    run_identity = any(
        n.get("name") in RUN_BUTTON_NAMES for n in named_invoke_buttons
    )
    cancel_identity = any(
        n.get("name") in CANCEL_BUTTON_NAMES for n in named_invoke_buttons
    )
    checks = [{"name": n.get("name", ""), "class": n.get("class", ""),
               "control": n.get("control", ""),
               "toggle": n.get("toggle", "")}
              for n in checkbox_candidates]
    if has_check:
        kind = "setup"
    elif has_result:
        kind = "result"
    elif any(n.get("control") == "ControlType.Text" for n in nodes):
        kind = "result-or-busy"
    else:
        kind = "busy-or-unknown"
    checkbox_status = (
        "PASS" if len(exposed_labels) == len(ARRANGE_LABELS)
        and all(n.get("control") == "ControlType.CheckBox" for n in checkbox_candidates)
        and all("TogglePatternIdentifiers.Pattern" in (n.get("patterns") or "")
                 for n in checkbox_candidates[:2])
        else "BLOCKED_HOST_ACCESSIBILITY"
    )
    return {
        "kind": kind,
        "buttons": buttons,
        "checkboxes": checks,
        "expected_labels": list(ARRANGE_LABELS),
        "exposed_labels": exposed_labels,
        "labels_exposed": len(exposed_labels) == len(ARRANGE_LABELS),
        "checkbox_readback_status": checkbox_status,
        "button_candidates": [
            {"name": n.get("name", ""), "class": n.get("class", ""),
             "control": n.get("control", ""),
             "patterns": n.get("patterns", "")}
            for n in button_candidates
        ],
        "named_invoke_buttons": [n.get("name", "") for n in named_invoke_buttons],
        "run_button_identity": run_identity,
        "cancel_button_identity": cancel_identity,
        "behavioral_default_status": "UNVERIFIED",
    }


def parse_moved(text):
    """Pure helper: extract moved=N from an Arrange result message."""
    if not text:
        return None
    m = re.search(r"moved=(\d+)", text)
    return int(m.group(1)) if m else None


def cmd_dump_window(args):
    ok, nodes, data = _dump_window(args.title, args.timeout)
    cls = classify_window(nodes) if ok else {"kind": "undumped"}
    rec = {"step": args.step, "op": "dump-window", "title": args.title,
           "dump_ok": ok, "node_count": data.get("node_count", len(nodes)),
           "classification": cls,
           "status": "PASS" if ok else "FAIL"}
    rec["nodes"] = nodes if args.full else nodes[:40]
    return _emit(rec, args.evidence)


PS_PRESS = PS_PRELUDE + (
    "$title = '__TITLE__'\n"
    "$want = '__BUTTON__'\n"
    "$r = Get-Process | Where-Object { $_.ProcessName -eq 'Resolve' } "
    "| Select-Object -First 1\n"
    "$root = [System.Windows.Automation.AutomationElement]::RootElement\n"
    "$top = @($root.FindAll([System.Windows.Automation.TreeScope]::Children, $TrueCond))\n"
    "$win = $top | Where-Object { try { ($_.Current.ProcessId -eq $r.Id) -and ([string]$_.Current.Name -eq $title) } catch { $false } } | Select-Object -First 1\n"
    "if (-not $win) { $main = $top | Where-Object { try { $_.Current.ProcessId -eq $r.Id -and [string]$_.Current.ClassName -eq 'UiMainWindowImp' } catch { $false } } | Select-Object -First 1; if ($main) { $win = $main.FindAll([System.Windows.Automation.TreeScope]::Descendants, $TrueCond) | Where-Object { try { ([string]$_.Current.Name -eq $title) -and ($_.Current.ControlType -eq [System.Windows.Automation.ControlType]::Window) } catch { $false } } | Select-Object -First 1 } }\n"
    "if (-not $win) "
    "{ Write-Output '{\"ok\":false,\"reason\":\"no window\"}'; exit 0 }\n"
    "$btnCond = New-Object System.Windows.Automation.PropertyCondition(\n"
    "  [System.Windows.Automation.AutomationElement]::ControlTypeProperty,\n"
    "  [System.Windows.Automation.ControlType]::Button)\n"
    "$btn = @($win.FindAll([System.Windows.Automation.TreeScope]"
    "::Descendants, $btnCond)) | Where-Object "
    "{ try { [string]$_.Current.Name -eq $want } catch { $false } } "
    "| Select-Object -First 1\n"
    "if (-not $btn) "
    "{ Write-Output '{\"ok\":false,\"reason\":\"no button\"}'; exit 0 }\n"
    "try { $en = [string]$btn.Current.IsEnabled } catch { $en = '?' }\n"
    "($btn.GetCurrentPattern([System.Windows.Automation.InvokePattern]"
    "::Pattern)).Invoke()\n"
    "$o = [ordered]@{ok=$true; button=$want; was_enabled=$en}\n"
    "Write-Output ($o | ConvertTo-Json -Compress)\n"
)


def cmd_press(args):
    script = PS_PRESS.replace("__TITLE__", args.title).replace(
        "__BUTTON__", args.button)
    if args.detach:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ps1",
                                          delete=False,
                                          encoding="utf-8-sig") as fh:
            fh.write(script)
            path = fh.name
        try:
            proc = subprocess.Popen(
                ["powershell.exe", "-NoProfile", "-ExecutionPolicy",
                 "Bypass", "-File", path],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                out, _err = proc.communicate(timeout=args.timeout)
                data = json.loads(out.decode(
                    "utf-8", errors="replace").strip().splitlines()[-1])
            except Exception as exc:
                data = {"ok": False,
                        "note": "detach invoke did not return: %r" % (exc,)}
                try:
                    proc.kill()
                except OSError:
                    pass
        finally:
            try:
                os.unlink(path)
            except OSError:
                pass
        ok = True
    else:
        ok, out, err = _run_ps(script, args.timeout)
        try:
            data = json.loads(out.strip().splitlines()[-1])
        except Exception:
            data = {"ok": False, "raw": out[-300:], "stderr": err[-300:]}
    rec = {"step": args.step, "op": "press-button", "title": args.title,
           "button": args.button, "detach": bool(args.detach),
           "transport_ok": ok}
    if isinstance(data, dict):
        rec.update(data)
    rec["status"] = "PASS" if (ok and data.get("ok")) else "FAIL"
    return _emit(rec, args.evidence)


PS_CLOSE_WINDOW = PS_PRELUDE + (
    "$title = '__TITLE__'\n"
    "$r = Get-Process | Where-Object { $_.ProcessName -eq 'Resolve' } "
    "| Select-Object -First 1\n"
    "$root = [System.Windows.Automation.AutomationElement]::RootElement\n"
    "$top = @($root.FindAll([System.Windows.Automation.TreeScope]::Children, $TrueCond))\n"
    "$win = $top | Where-Object { try { ($_.Current.ProcessId -eq $r.Id) -and ([string]$_.Current.Name -eq $title) } catch { $false } } | Select-Object -First 1\n"
    "if (-not $win) { $main = $top | Where-Object { try { $_.Current.ProcessId -eq $r.Id -and [string]$_.Current.ClassName -eq 'UiMainWindowImp' } catch { $false } } | Select-Object -First 1; if ($main) { $win = $main.FindAll([System.Windows.Automation.TreeScope]::Descendants, $TrueCond) | Where-Object { try { ([string]$_.Current.Name -eq $title) -and ($_.Current.ControlType -eq [System.Windows.Automation.ControlType]::Window) } catch { $false } } | Select-Object -First 1 } }\n"
    "if (-not $win) { Write-Output '{\"ok\":false,\"reason\":\"no window\"}'; exit 0 }\n"
    "$p = $win.GetCurrentPattern([System.Windows.Automation.WindowPattern]::Pattern)\n"
    "$p.Close()\n"
    "$o = [ordered]@{ok=$true; title=$title; class=[string]$win.Current.ClassName; control=[string]$win.Current.ControlType.ProgrammaticName; close_pattern='WindowPattern.Close'}\n"
    "Write-Output ($o | ConvertTo-Json -Compress)\n"
)


def cmd_close_window(args):
    script = PS_CLOSE_WINDOW.replace("__TITLE__", args.title)
    ok, out, err = _run_ps(script, args.timeout)
    try:
        data = json.loads(out.strip().splitlines()[-1])
    except Exception:
        data = {"ok": False, "raw": out[-300:], "stderr": err[-300:]}
    rec = {"step": args.step, "op": "close-window", "title": args.title,
           "transport_ok": ok}
    if isinstance(data, dict):
        rec.update(data)
    rec["status"] = "PASS" if (ok and data.get("ok")) else "FAIL"
    return _emit(rec, args.evidence)


def cmd_record(args):
    src = args.json
    if src.startswith("@"):
        with open(src[1:], encoding="utf-8-sig") as fh:
            src = fh.read()
    try:
        payload = json.loads(src)
    except Exception as exc:
        payload = {"parse_error": str(exc), "raw": src[-300:]}
    rec = {"step": args.step, "op": "agent-record"}
    if isinstance(payload, dict):
        rec.update(payload)
    rec.setdefault("status", "PASS")
    return _emit(rec, args.evidence)


def cmd_assemble(args):
    steps = []
    with open(args.input, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    steps.append(json.loads(line))
                except Exception:
                    steps.append({"parse_error": line[-300:]})
    layers = {"UI_ACCESSIBILITY": [], "PRODUCT_BEHAVIOR": []}
    for step in steps:
        layer = step.get("layer")
        if layer in layers:
            layers[layer].append(step.get("step"))
    doc = {"schema": "resolve-node-kit.arrange-uia-e2e/v2",
           "title": TITLE, "entry": ENTRY_NAME,
           "verification_contract": {
               "UI_ACCESSIBILITY": {
                   "checkbox_direct_readback": "BLOCKED_HOST_ACCESSIBILITY",
                   "run_cancel_identity_required": True,
               },
               "PRODUCT_BEHAVIOR": {
                   "effective_defaults": "PASS_BEHAVIORAL",
                   "requires_safe_run_cancel_identity": True,
               },
           },
           "layers": layers, "steps": steps}
    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
    return _emit({"op": "assemble", "input": args.input,
                  "output": args.output, "step_count": len(steps),
                  "status": "PASS"}, None)


def build_parser():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--evidence", default=None)
    ap.add_argument("--timeout", type=int, default=60)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("uia-bind")
    p.add_argument("--step", type=int, default=4)
    p.set_defaults(func=cmd_bind)
    p = sub.add_parser("menu-invoke")
    p.add_argument("--step", type=int, default=5)
    p.set_defaults(func=cmd_menu_invoke)
    p = sub.add_parser("wait-window")
    p.add_argument("--step", type=int, required=True)
    p.add_argument("--title", default=TITLE)
    p.add_argument("--timeout", type=int, default=30)
    p.add_argument("--poll", type=float, default=0.5)
    p.add_argument("--absent", action="store_true")
    p.set_defaults(func=cmd_wait_window)
    p = sub.add_parser("dump-window")
    p.add_argument("--step", type=int, required=True)
    p.add_argument("--title", default=TITLE)
    p.add_argument("--timeout", type=int, default=30)
    p.add_argument("--full", action="store_true")
    p.set_defaults(func=cmd_dump_window)
    p = sub.add_parser("press")
    p.add_argument("--step", type=int, required=True)
    p.add_argument("--title", default=TITLE)
    p.add_argument("--button", required=True)
    p.add_argument("--timeout", type=int, default=60)
    p.add_argument("--detach", action="store_true")
    p.set_defaults(func=cmd_press)
    p = sub.add_parser("close-window")
    p.add_argument("--step", type=int, required=True)
    p.add_argument("--title", default=TITLE)
    p.add_argument("--timeout", type=int, default=30)
    p.set_defaults(func=cmd_close_window)
    p = sub.add_parser("record")
    p.add_argument("--step", type=int, required=True)
    p.add_argument("--json", required=True)
    p.set_defaults(func=cmd_record)
    p = sub.add_parser("assemble")
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.set_defaults(func=cmd_assemble)
    return ap


def main(argv=None):
    ap = build_parser()
    args = ap.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
