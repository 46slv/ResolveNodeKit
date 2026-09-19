#!/usr/bin/env python3
"""Busy-window watcher for the Arrange UIA E2E (Phase B).

Polls Resolve-owned top-level windows for TITLE in ONE powershell process
(poll interval 200 ms), sampling any Text descendant values while present.
Emits one JSON record: first_seen_s / last_seen_s / observed_texts /
sample counts. Stdlib only, ASCII-only PowerShell source.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import subprocess
import sys
import tempfile

PS_BODY = r"""
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$ErrorActionPreference = 'Stop'
$TrueCond = [System.Windows.Automation.Condition]::TrueCondition
$title = '__TITLE__'
$budget = __BUDGET__
$iv = 200
$r = Get-Process | Where-Object { $_.ProcessName -eq 'Resolve' } | Select-Object -First 1
$root = [System.Windows.Automation.AutomationElement]::RootElement
$t0 = [DateTime]::UtcNow
$texts = @()
$firstSeen = -1
$lastSeen = -1
$samples = 0
$present = 0
while (([DateTime]::UtcNow - $t0).TotalSeconds -lt $budget) {
  $el = ([DateTime]::UtcNow - $t0).TotalSeconds
  $samples++
  $kids = @($root.FindAll([System.Windows.Automation.TreeScope]::Children, $TrueCond))
  $windows = @($kids | Where-Object { try { $_.Current.ProcessId -eq $r.Id } catch { $false } })
  $main = $windows | Where-Object { try { [string]$_.Current.ClassName -eq 'UiMainWindowImp' } catch { $false } } | Select-Object -First 1
  if ($main) {
    $windows += @($main.FindAll([System.Windows.Automation.TreeScope]::Descendants, $TrueCond) | Where-Object { try { $_.Current.ControlType -eq [System.Windows.Automation.ControlType]::Window } catch { $false } })
  }
  foreach ($w in $windows) {
    try { $hit = [string]$w.Current.Name -eq $title }
    catch { $hit = $false }
    if ($hit) {
      $present++
      if ($firstSeen -lt 0) { $firstSeen = [math]::Round($el, 2) }
      $lastSeen = [math]::Round($el, 2)
      try {
        $desc = @($w.FindAll([System.Windows.Automation.TreeScope]::Descendants, $TrueCond))
        foreach ($d in $desc) {
          try { $ct = [string]$d.Current.ControlType.ProgrammaticName } catch { $ct = '' }
          if ($ct -eq 'ControlType.Text') {
            try { $v = [string]$d.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value } catch { $v = '' }
            try { $nm = [string]$d.Current.Name } catch { $nm = '' }
            $txt = ($nm + '|' + $v).Trim()
            if ($txt.Length -gt 1 -and -not ($texts -contains $txt)) { $texts += $txt }
          }
        }
      } catch {}
    }
  }
  Start-Sleep -Milliseconds $iv
}
$o = New-Object psobject
$o | Add-Member ok $true
$o | Add-Member first_seen_s $firstSeen
$o | Add-Member last_seen_s $lastSeen
$o | Add-Member observed_texts $texts
$o | Add-Member samples $samples
$o | Add-Member present_count $present
$json = ($o | ConvertTo-Json -Depth 5 -Compress)
[System.IO.File]::WriteAllText('__OUT__', $json, [System.Text.Encoding]::UTF8)
Write-Output '{\"ok\":true}'
"""


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--evidence", default=None)
    ap.add_argument("--step", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--budget", type=int, default=45)
    args = ap.parse_args(argv)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json",
                                      delete=False) as fh:
        out_path = fh.name
    script = (PS_BODY.replace("__TITLE__", args.title)
              .replace("__BUDGET__", str(args.budget))
              .replace("__OUT__", out_path.replace("\\", "\\\\")))
    with tempfile.NamedTemporaryFile(mode="w", suffix=".ps1", delete=False,
                                      encoding="utf-8-sig") as fh:
        fh.write(script)
        path = fh.name
    try:
        proc = subprocess.run(
            ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass",
             "-File", path],
            capture_output=True, timeout=args.budget + 60)
        ok = proc.returncode == 0
    except subprocess.TimeoutExpired:
        ok = False
    try:
        with open(out_path, encoding="utf-8-sig") as fh:
            data = json.load(fh)
    except Exception as exc:
        data = {"ok": False, "note": "no sidecar: %r" % (exc,)}
    finally:
        for p in (path, out_path):
            try:
                os.unlink(p)
            except OSError:
                pass
    rec = {"step": args.step, "op": "busy-watch", "title": args.title,
           "budget_s": args.budget}
    if isinstance(data, dict):
        rec.update(data)
    fs = rec.get("first_seen_s", -1)
    rec["status"] = ("PASS" if (ok and rec.get("ok") and fs is not None
                                and fs >= 0) else "FAIL")
    rec["ts"] = datetime.datetime.now().isoformat(timespec="seconds")
    line = json.dumps(rec, ensure_ascii=False)
    print(line)
    if args.evidence:
        with open(args.evidence, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


if __name__ == "__main__":
    main()
