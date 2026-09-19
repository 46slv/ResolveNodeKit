#!/usr/bin/env python3
"""One-shot MSAA/IAccessible probe for the existing Arrange UIA candidates.

This is deliberately narrower than ``verify_arrange_ui.py``.  It does not
dump or classify a new UIA tree and it never invokes a control.  The caller
opens the existing ``ResolveNodeKit - Arrange`` dialog, then this command:

* asks only the known Fusion checkbox/button candidates for
  ``LegacyIAccessiblePattern`` data; and
* falls back to the Windows standard ``oleacc.dll`` IAccessible surface for
  the same dialog HWND and its accessible children.

The output is machine-readable and records the raw semantic fields needed to
decide whether Run, Cancel, or either checkbox can be targeted safely.  An
element is identity-safe only when its semantic name and role match the
expected action; control order, coordinates, and runtime IDs are never used.
"""
from __future__ import annotations

import argparse
import ctypes
import datetime
import json
import os
import subprocess
import sys
import tempfile
from ctypes import wintypes
from typing import Any, Iterable


TITLE = "ResolveNodeKit - Arrange"
ARRANGE_LABELS = (
    "選択されていないノードも整列",
    "グループ化を解除して整列",
)
RUN_NAMES = ("Run", "OK", "実行", "適用")
CANCEL_NAMES = ("Cancel", "キャンセル", "中止")

# These are the exact classes present in the earlier 4-checkbox / 5-button
# UIA candidate set.  Matching only this set prevents this probe from silently
# becoming another whole-dialog UIA discovery pass.
CANDIDATE_CLASSES = (
    "Fusion::CheckBoxControl",
    "Fusion::CustomCheckBox",
    "Fusion::ButtonControl",
    "Fusion::CustomButton",
)

ROLE_NAMES = {
    0x00: "ROLE_SYSTEM_TITLEBAR",
    0x01: "ROLE_SYSTEM_MENUBAR",
    0x02: "ROLE_SYSTEM_SCROLLBAR",
    0x03: "ROLE_SYSTEM_GRIP",
    0x04: "ROLE_SYSTEM_SOUND",
    0x05: "ROLE_SYSTEM_CURSOR",
    0x06: "ROLE_SYSTEM_CARET",
    0x07: "ROLE_SYSTEM_ALERT",
    0x08: "ROLE_SYSTEM_WINDOW",
    0x09: "ROLE_SYSTEM_CLIENT",
    0x0A: "ROLE_SYSTEM_MENUPOPUP",
    0x0B: "ROLE_SYSTEM_MENUITEM",
    0x0C: "ROLE_SYSTEM_TOOLTIP",
    0x0D: "ROLE_SYSTEM_APPLICATION",
    0x0E: "ROLE_SYSTEM_DOCUMENT",
    0x0F: "ROLE_SYSTEM_PANE",
    0x10: "ROLE_SYSTEM_CHART",
    0x11: "ROLE_SYSTEM_DIALOG",
    0x12: "ROLE_SYSTEM_BORDER",
    0x13: "ROLE_SYSTEM_GROUPING",
    0x14: "ROLE_SYSTEM_SEPARATOR",
    0x15: "ROLE_SYSTEM_TOOLBAR",
    0x16: "ROLE_SYSTEM_STATUSBAR",
    0x17: "ROLE_SYSTEM_TABLE",
    0x18: "ROLE_SYSTEM_COLUMNHEADER",
    0x19: "ROLE_SYSTEM_ROWHEADER",
    0x1A: "ROLE_SYSTEM_COLUMN",
    0x1B: "ROLE_SYSTEM_ROW",
    0x1C: "ROLE_SYSTEM_CELL",
    0x1D: "ROLE_SYSTEM_LINK",
    0x1E: "ROLE_SYSTEM_HELPBALLOON",
    0x1F: "ROLE_SYSTEM_CHARACTER",
    0x20: "ROLE_SYSTEM_LIST",
    0x21: "ROLE_SYSTEM_LISTITEM",
    0x22: "ROLE_SYSTEM_OUTLINE",
    0x23: "ROLE_SYSTEM_OUTLINEITEM",
    0x24: "ROLE_SYSTEM_PAGETAB",
    0x25: "ROLE_SYSTEM_PROPERTYPAGE",
    0x26: "ROLE_SYSTEM_INDICATOR",
    0x27: "ROLE_SYSTEM_GRAPHIC",
    0x28: "ROLE_SYSTEM_STATICTEXT",
    0x29: "ROLE_SYSTEM_TEXT",
    0x2A: "ROLE_SYSTEM_TEXT",
    0x2B: "ROLE_SYSTEM_PUSHBUTTON",
    0x2C: "ROLE_SYSTEM_CHECKBUTTON",
    0x2D: "ROLE_SYSTEM_RADIOBUTTON",
    0x2E: "ROLE_SYSTEM_COMBOBOX",
    0x2F: "ROLE_SYSTEM_DROPLIST",
    0x30: "ROLE_SYSTEM_PROGRESSBAR",
    0x31: "ROLE_SYSTEM_DIAL",
    0x32: "ROLE_SYSTEM_HOTKEYFIELD",
    0x33: "ROLE_SYSTEM_SLIDER",
    0x34: "ROLE_SYSTEM_SPINBUTTON",
    0x35: "ROLE_SYSTEM_DIAGRAM",
    0x36: "ROLE_SYSTEM_ANIMATION",
    0x37: "ROLE_SYSTEM_EQUATION",
    0x38: "ROLE_SYSTEM_BUTTONDROPDOWN",
    0x39: "ROLE_SYSTEM_BUTTONMENU",
    0x3A: "ROLE_SYSTEM_BUTTONDROPDOWNGRID",
    0x3B: "ROLE_SYSTEM_WHITESPACE",
    0x3C: "ROLE_SYSTEM_PAGETAB",
    0x3D: "ROLE_SYSTEM_PROPERTYPAGE",
    0x3E: "ROLE_SYSTEM_IPADDRESS",
    0x3F: "ROLE_SYSTEM_OUTLINEBUTTON",
}

# PowerShell is used only to ask the already-known candidates for the legacy
# provider.  The script intentionally does not collect arbitrary descendants.
PS_PRELUDE = (
    "Add-Type -AssemblyName UIAutomationClient\n"
    "Add-Type -AssemblyName UIAutomationTypes\n"
    "$ErrorActionPreference = 'Stop'\n"
    "$TrueCond = [System.Windows.Automation.Condition]::TrueCondition\n"
)

PS_LEGACY = PS_PRELUDE + r'''
$title = '__TITLE__'
$classes = @('Fusion::CheckBoxControl','Fusion::CustomCheckBox','Fusion::ButtonControl','Fusion::CustomButton')
$legacyPatternType = $null
try { $legacyPatternType = [type]::GetType('System.Windows.Automation.LegacyIAccessiblePattern, UIAutomationClient', $false) } catch {}
$legacyPatternById = $null
try { $legacyPatternById = [System.Windows.Automation.AutomationPattern]::LookupById(10018) } catch {}
$r = Get-Process | Where-Object { $_.ProcessName -eq 'Resolve' } | Select-Object -First 1
$root = [System.Windows.Automation.AutomationElement]::RootElement
$top = @($root.FindAll([System.Windows.Automation.TreeScope]::Children, $TrueCond))
$win = $top | Where-Object {
  try { ($_.Current.ProcessId -eq $r.Id) -and ([string]$_.Current.Name -eq $title) }
  catch { $false }
} | Select-Object -First 1
if (-not $win) {
  $main = $top | Where-Object {
    try { $_.Current.ProcessId -eq $r.Id -and [string]$_.Current.ClassName -eq 'UiMainWindowImp' }
    catch { $false }
  } | Select-Object -First 1
  if ($main) {
    $win = $main.FindAll([System.Windows.Automation.TreeScope]::Descendants, $TrueCond) |
      Where-Object {
        try { ([string]$_.Current.Name -eq $title) -and ($_.Current.ControlType -eq [System.Windows.Automation.ControlType]::Window) }
        catch { $false }
      } | Select-Object -First 1
  }
}
if (-not $win) {
  Write-Output '{"ok":false,"reason":"no arrange dialog"}'
  exit 0
}
$rows = @()
$desc = @($win.FindAll([System.Windows.Automation.TreeScope]::Descendants, $TrueCond))
foreach ($d in $desc) {
  try { $cl = [string]$d.Current.ClassName } catch { continue }
  if ($classes -notcontains $cl) { continue }
  try { $ct = [string]$d.Current.ControlType.ProgrammaticName } catch { $ct = '' }
  try { $nm = [string]$d.Current.Name } catch { $nm = '' }
  try { $aid = [string]$d.Current.AutomationId } catch { $aid = '' }
  try { $hwnd = [int64]$d.Current.NativeWindowHandle } catch { $hwnd = 0 }
  $row = [ordered]@{
    class = $cl
    control = $ct
    name = $nm
    automation_id = $aid
    native_hwnd = $hwnd
    legacy_pattern_available = $false
  }
  try {
    if ($legacyPatternType) {
      $pattern = $legacyPatternType.GetField('Pattern').GetValue($null)
    } elseif ($legacyPatternById) {
      $pattern = $legacyPatternById
    } else {
      throw 'LegacyIAccessiblePattern type and pattern id 10018 are unavailable in UIAutomationClient'
    }
    $p = $d.GetCurrentPattern($pattern)
    $c = $p.Current
    $row.legacy_pattern_available = $true
    $row.legacy = [ordered]@{
      name = [string]$c.Name
      role = [string]$c.Role
      state = [string]$c.State
      default_action = [string]$c.DefaultAction
      child_id = [int64]$c.ChildId
      value = [string]$c.Value
      description = [string]$c.Description
    }
  } catch {
    $row.legacy_error = $_.Exception.Message
  }
  $rows += $row
}
$dialogHwnd = 0
try { $dialogHwnd = [int64]$win.Current.NativeWindowHandle } catch {}
$o = [ordered]@{
  ok = $true
  title = $title
  dialog = [ordered]@{
    name = [string]$win.Current.Name
    class = [string]$win.Current.ClassName
    control = [string]$win.Current.ControlType.ProgrammaticName
    native_hwnd = $dialogHwnd
  }
  candidate_count = $rows.Count
  candidates = $rows
}
$json = ($o | ConvertTo-Json -Depth 10 -Compress)
[System.IO.File]::WriteAllText('__OUT__', $json, [System.Text.Encoding]::UTF8)
Write-Output '{"ok":true}'
'''


def _run_ps(script: str, timeout: int) -> tuple[bool, str, str]:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".ps1", delete=False, encoding="utf-8-sig"
    ) as fh:
        fh.write(script)
        path = fh.name
    try:
        proc = subprocess.run(
            ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass",
             "-File", path],
            capture_output=True,
            timeout=timeout,
        )
        return (
            proc.returncode == 0,
            proc.stdout.decode("utf-8", errors="replace"),
            proc.stderr.decode("utf-8", errors="replace"),
        )
    except subprocess.TimeoutExpired as exc:
        out = (exc.stdout or b"").decode("utf-8", errors="replace")
        err = (exc.stderr or b"").decode("utf-8", errors="replace")
        return False, out, "TIMEOUT: " + err
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def _json_last(stdout: str, stderr: str) -> dict[str, Any]:
    for line in reversed(stdout.splitlines()):
        try:
            value = json.loads(line)
        except Exception:
            continue
        if isinstance(value, dict):
            return value
    return {"ok": False, "raw": stdout[-500:], "stderr": stderr[-500:]}


def probe_uia_legacy(title: str, timeout: int) -> dict[str, Any]:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as fh:
        out_path = fh.name
    script = PS_LEGACY.replace("__TITLE__", title).replace(
        "__OUT__", out_path.replace("\\", "\\\\")
    )
    ok, stdout, stderr = _run_ps(script, timeout)
    try:
        with open(out_path, encoding="utf-8-sig") as fh:
            data = json.load(fh)
    except Exception:
        data = _json_last(stdout, stderr)
    finally:
        try:
            os.unlink(out_path)
        except OSError:
            pass
    data.setdefault("transport_ok", ok)
    if stderr:
        data.setdefault("stderr", stderr[-500:])
    candidates = data.get("candidates", [])
    if isinstance(candidates, dict):
        candidates = [candidates]
    data["candidates"] = candidates
    return data


# ---- direct oleacc / IAccessible -------------------------------------------------

VT_I4 = 3
VT_DISPATCH = 9
VT_BSTR = 8
VT_EMPTY = 0
VT_UNKNOWN = 13
CHILDID_SELF = 0
OBJID_CLIENT = -4
S_OK = 0
S_FALSE = 1
RPC_E_CHANGED_MODE = 0x80010106


class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", ctypes.c_uint32),
        ("Data2", ctypes.c_uint16),
        ("Data3", ctypes.c_uint16),
        ("Data4", ctypes.c_ubyte * 8),
    ]


class VARIANT_UNION(ctypes.Union):
    _fields_ = [
        ("llVal", ctypes.c_longlong),
        ("lVal", ctypes.c_long),
        ("bstrVal", ctypes.c_void_p),
        ("pdispVal", ctypes.c_void_p),
        ("punkVal", ctypes.c_void_p),
        ("ptr", ctypes.c_void_p),
    ]


class VARIANT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = [
        ("vt", ctypes.c_ushort),
        ("wReserved1", ctypes.c_ushort),
        ("wReserved2", ctypes.c_ushort),
        ("wReserved3", ctypes.c_ushort),
        ("u", VARIANT_UNION),
    ]


IID_IACCESSIBLE = GUID(
    0x618736E0,
    0x3C3D,
    0x11CF,
    (0x81, 0x0C, 0x00, 0xAA, 0x00, 0x38, 0x9B, 0x71),
)


def _hresult(value: int) -> str:
    return "0x%08X" % (int(value) & 0xFFFFFFFF)


def _variant_i4(value: int) -> VARIANT:
    var = VARIANT()
    var.vt = VT_I4
    var.lVal = int(value)
    return var


def _variant_value(var: VARIANT) -> Any:
    if var.vt == VT_I4:
        return int(var.lVal)
    if var.vt == VT_BSTR and var.bstrVal:
        try:
            return ctypes.wstring_at(var.bstrVal)
        except Exception:
            return None
    if var.vt in (VT_DISPATCH, VT_UNKNOWN):
        return {"pointer": int(var.ptr or 0)}
    if var.vt == VT_EMPTY:
        return None
    return {"vt": int(var.vt), "raw": int(var.llVal)}


def _load_oleacc() -> dict[str, Any]:
    if os.name != "nt":
        return {"available": False, "reason": "non-windows"}
    try:
        oleacc = ctypes.WinDLL("oleacc")
        ole32 = ctypes.WinDLL("ole32")
        user32 = ctypes.WinDLL("user32")
        return {"available": True, "oleacc": oleacc, "ole32": ole32, "user32": user32}
    except Exception as exc:
        return {"available": False, "reason": repr(exc)}


def _com_method(ptr: int, index: int, restype: Any, *argtypes: Any) -> Any:
    table = ctypes.cast(
        ctypes.c_void_p(ptr),
        ctypes.POINTER(ctypes.POINTER(ctypes.c_void_p)),
    ).contents
    address = table[index]
    return ctypes.WINFUNCTYPE(restype, ctypes.c_void_p, *argtypes)(address)


def _release(ptr: int) -> None:
    if not ptr:
        return
    try:
        _com_method(ptr, 2, ctypes.c_ulong)(ptr)
    except Exception:
        pass


def _query_iaccessible(ptr: int) -> int:
    if not ptr:
        return 0
    out = ctypes.c_void_p()
    try:
        query = _com_method(
            ptr, 0, ctypes.c_long,
            ctypes.POINTER(GUID), ctypes.POINTER(ctypes.c_void_p),
        )
        hr = query(ptr, ctypes.byref(IID_IACCESSIBLE), ctypes.byref(out))
        return int(out.value or 0) if hr >= 0 else 0
    except Exception:
        return 0


def _free_bstr(oleaut32: Any, ptr: int) -> None:
    if not ptr:
        return
    try:
        oleaut32.SysFreeString(ctypes.c_void_p(ptr))
    except Exception:
        pass


def _variant_clear(oleaut32: Any, var: VARIANT) -> None:
    try:
        oleaut32.VariantClear(ctypes.byref(var))
    except Exception:
        pass


def _get_bstr(ptr: int, var: VARIANT, index: int, oleaut32: Any) -> tuple[Any, str | None]:
    out = ctypes.c_void_p()
    try:
        method = _com_method(ptr, index, ctypes.c_long, VARIANT, ctypes.POINTER(ctypes.c_void_p))
        hr = int(method(ptr, var, ctypes.byref(out)))
        if hr < 0:
            return None, _hresult(hr)
        value = ctypes.wstring_at(out.value) if out.value else ""
        _free_bstr(oleaut32, int(out.value or 0))
        return value, None
    except Exception as exc:
        _free_bstr(oleaut32, int(out.value or 0))
        return None, repr(exc)


def _get_variant(ptr: int, var: VARIANT, index: int, oleaut32: Any) -> tuple[Any, int | None, str | None]:
    result = VARIANT()
    try:
        method = _com_method(ptr, index, ctypes.c_long, VARIANT, ctypes.POINTER(VARIANT))
        hr = int(method(ptr, var, ctypes.byref(result)))
        if hr < 0:
            return None, None, _hresult(hr)
        value = _variant_value(result)
        numeric = int(value) if isinstance(value, int) else None
        _variant_clear(oleaut32, result)
        return value, numeric, None
    except Exception as exc:
        _variant_clear(oleaut32, result)
        return None, None, repr(exc)


def _accessible_properties(ptr: int, var: VARIANT, child_id: int, oleaut32: Any) -> dict[str, Any]:
    name, name_error = _get_bstr(ptr, var, 10, oleaut32)       # get_accName
    role, role_num, role_error = _get_variant(ptr, var, 13, oleaut32)  # get_accRole
    state, state_num, state_error = _get_variant(ptr, var, 14, oleaut32)  # get_accState
    action, action_error = _get_bstr(ptr, var, 20, oleaut32)   # get_accDefaultAction
    value, value_error = _get_bstr(ptr, var, 11, oleaut32)     # get_accValue
    row: dict[str, Any] = {
        "child_id": int(child_id),
        "acc_name": name or "",
        "acc_role": role_num if role_num is not None else role,
        "acc_role_name": ROLE_NAMES.get(role_num, "") if role_num is not None else "",
        "acc_state": state_num if state_num is not None else state,
        "acc_default_action": action or "",
        "acc_value": value or "",
    }
    errors = {
        "name": name_error,
        "role": role_error,
        "state": state_error,
        "default_action": action_error,
        "value": value_error,
    }
    errors = {key: value for key, value in errors.items() if value}
    if errors:
        row["field_errors"] = errors
    return row


def _accessible_tree(
    root_ptr: int,
    oleacc: Any,
    oleaut32: Any,
    *,
    max_depth: int = 4,
    max_nodes: int = 128,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Read IAccessible semantic fields without invoking any action."""
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    seen: set[int] = set()

    def walk(ptr: int, depth: int, source: str) -> None:
        if not ptr or depth > max_depth or len(rows) >= max_nodes:
            return
        if ptr in seen:
            return
        seen.add(ptr)
        self_var = _variant_i4(CHILDID_SELF)
        row = _accessible_properties(ptr, self_var, CHILDID_SELF, oleaut32)
        row.update({"source": source, "depth": depth, "object_pointer": hex(ptr)})
        rows.append(row)
        try:
            get_count = _com_method(ptr, 8, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
            count = ctypes.c_long(0)
            hr = int(get_count(ptr, ctypes.byref(count)))
            if hr < 0:
                errors.append("get_accChildCount=" + _hresult(hr))
                return
            child_count = min(max(int(count.value), 0), max_nodes - len(rows))
            if child_count <= 0:
                return
            start = _variant_i4(0)
            arr = (VARIANT * child_count)()
            obtained = ctypes.c_long(0)
            acc_children = oleacc.AccessibleChildren
            acc_children.argtypes = [
                ctypes.c_void_p,
                VARIANT,
                ctypes.c_long,
                ctypes.POINTER(VARIANT),
                ctypes.POINTER(ctypes.c_long),
            ]
            acc_children.restype = ctypes.c_long
            hr = int(acc_children(ptr, start, child_count, arr, ctypes.byref(obtained)))
            if hr < 0:
                errors.append("AccessibleChildren=" + _hresult(hr))
                return
            for idx in range(max(int(obtained.value), 0)):
                if len(rows) >= max_nodes:
                    break
                child = arr[idx]
                if child.vt == VT_I4:
                    child_id = int(child.lVal)
                    child_row = _accessible_properties(ptr, child, child_id, oleaut32)
                    child_row.update({"source": source + ".child", "depth": depth + 1})
                    rows.append(child_row)
                elif child.vt == VT_DISPATCH and child.pdispVal:
                    child_ptr = _query_iaccessible(int(child.pdispVal))
                    if child_ptr:
                        walk(child_ptr, depth + 1, source + ".dispatch")
                        _release(child_ptr)
                _variant_clear(oleaut32, child)
        except Exception as exc:
            errors.append("children=" + repr(exc))

    walk(root_ptr, 0, "root")
    return rows, errors


def _hwnd_from_title(user32: Any, title: str) -> int:
    try:
        user32.FindWindowW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]
        user32.FindWindowW.restype = wintypes.HWND
        return int(user32.FindWindowW(None, title) or 0)
    except Exception:
        return 0


def probe_oleacc(uia: dict[str, Any], title: str) -> dict[str, Any]:
    loaded = _load_oleacc()
    if not loaded.get("available"):
        return {"available": False, "reason": loaded.get("reason", "unavailable"), "objects": []}
    oleacc = loaded["oleacc"]
    ole32 = loaded["ole32"]
    user32 = loaded["user32"]
    try:
        oleaut32 = ctypes.WinDLL("oleaut32")
        oleaut32.VariantClear.argtypes = [ctypes.POINTER(VARIANT)]
        oleaut32.VariantClear.restype = ctypes.c_long
        oleaut32.SysFreeString.argtypes = [ctypes.c_void_p]
        oleaut32.SysFreeString.restype = None
    except Exception as exc:
        return {"available": True, "object_surface": False, "reason": repr(exc), "objects": []}

    # COM is initialized for this worker thread only.  Changed mode still
    # permits the already-initialized apartment to be used.
    try:
        ole32.CoInitialize.argtypes = [ctypes.c_void_p]
        ole32.CoInitialize.restype = ctypes.c_long
        init_hr = int(ole32.CoInitialize(None))
    except Exception as exc:
        init_hr = -1
        init_error = repr(exc)
    else:
        init_error = None

    try:
        oleacc.AccessibleObjectFromWindow.argtypes = [
            wintypes.HWND,
            wintypes.DWORD,
            ctypes.POINTER(GUID),
            ctypes.POINTER(ctypes.c_void_p),
        ]
        oleacc.AccessibleObjectFromWindow.restype = ctypes.c_long
        dialog = uia.get("dialog", {}) if isinstance(uia, dict) else {}
        handles: list[tuple[int, str]] = []
        try:
            dialog_hwnd = int(dialog.get("native_hwnd") or 0)
        except Exception:
            dialog_hwnd = 0
        if dialog_hwnd:
            handles.append((dialog_hwnd, "dialog"))
        for candidate in uia.get("candidates", []) if isinstance(uia, dict) else []:
            try:
                hwnd = int(candidate.get("native_hwnd") or 0)
            except Exception:
                hwnd = 0
            if hwnd and all(existing != hwnd for existing, _ in handles):
                handles.append((hwnd, "candidate:" + str(candidate.get("class", ""))))
        if not handles:
            fallback = _hwnd_from_title(user32, title)
            if fallback:
                handles.append((fallback, "FindWindowW:title"))

        objects: list[dict[str, Any]] = []
        any_object = False
        for hwnd, source in handles:
            ptr = ctypes.c_void_p()
            try:
                hr = int(oleacc.AccessibleObjectFromWindow(
                    wintypes.HWND(hwnd), ctypes.c_ulong(OBJID_CLIENT & 0xFFFFFFFF),
                    ctypes.byref(IID_IACCESSIBLE), ctypes.byref(ptr),
                ))
                item: dict[str, Any] = {
                    "hwnd": hwnd,
                    "source": source,
                    "hresult": _hresult(hr),
                    "accessible_object": bool(hr >= 0 and ptr.value),
                }
                if hr >= 0 and ptr.value:
                    any_object = True
                    rows, errors = _accessible_tree(int(ptr.value), oleacc, oleaut32)
                    item["semantic_rows"] = rows
                    item["tree_errors"] = errors
                    _release(int(ptr.value))
                objects.append(item)
            except Exception as exc:
                objects.append({
                    "hwnd": hwnd,
                    "source": source,
                    "accessible_object": False,
                    "error": repr(exc),
                })
        result = {
            "available": True,
            "object_surface": any_object,
            "com_initialize": _hresult(init_hr),
            "objects": objects,
        }
        if init_error:
            result["com_initialize_error"] = init_error
        return result
    finally:
        if init_hr in (S_OK, S_FALSE):
            try:
                ole32.CoUninitialize()
            except Exception:
                pass


def _iter_legacy_rows(uia: dict[str, Any]) -> Iterable[dict[str, Any]]:
    def role_name(value: Any) -> str:
        try:
            number = int(str(value), 0)
        except (TypeError, ValueError):
            return str(value or "")
        return ROLE_NAMES.get(number, "")

    for row in uia.get("candidates", []) if isinstance(uia, dict) else []:
        legacy = row.get("legacy")
        if row.get("legacy_pattern_available") and isinstance(legacy, dict):
            yield {
                "name": legacy.get("name", ""),
                "role": legacy.get("role"),
                "role_name": legacy.get("role_name", "") or role_name(legacy.get("role")),
                "state": legacy.get("state"),
                "default_action": legacy.get("default_action", ""),
                "child_id": legacy.get("child_id"),
                "source": "uia.LegacyIAccessiblePattern",
                "class": row.get("class", ""),
            }


def _iter_oleacc_rows(oleacc: dict[str, Any]) -> Iterable[dict[str, Any]]:
    for obj in oleacc.get("objects", []) if isinstance(oleacc, dict) else []:
        for row in obj.get("semantic_rows", []) if isinstance(obj, dict) else []:
            value = dict(row)
            value["source"] = "oleacc." + str(obj.get("source", "object"))
            yield value


def _identity_from_rows(rows: Iterable[dict[str, Any]], names: tuple[str, ...], role_tokens: tuple[str, ...]) -> dict[str, Any]:
    observed = []
    for row in rows:
        name = str(row.get("name", row.get("acc_name", "")) or "").strip()
        role = str(row.get("role_name", row.get("acc_role_name", "")) or "").upper()
        action = str(row.get("default_action", row.get("acc_default_action", "")) or "").strip()
        if name or role or action:
            observed.append({
                "name": name,
                "role": role,
                "state": row.get("state", row.get("acc_state")),
                "default_action": action,
                "child_id": row.get("child_id"),
                "source": row.get("source", ""),
            })
        if name in names and any(token in role for token in role_tokens) and action:
            return {
                "status": "PASS",
                "semantic_identity": True,
                "name": name,
                "role": role,
                "state": row.get("state", row.get("acc_state")),
                "default_action": action,
                "child_id": row.get("child_id"),
                "source": row.get("source", ""),
                "invocation": "not_attempted",
            }
    return {
        "status": "BLOCKED_HOST_ACCESSIBILITY_HARD",
        "semantic_identity": False,
        "reason": "MSAA/LegacyIAccessible rows did not expose matching name+role+default_action",
        "observed_semantic_rows": observed,
        "invocation": "not_attempted",
    }


def classify_msaa(uia: dict[str, Any], oleacc: dict[str, Any]) -> dict[str, Any]:
    """Classify identity without any host-side action (offline-testable)."""
    legacy_rows = list(_iter_legacy_rows(uia))
    ole_rows = list(_iter_oleacc_rows(oleacc))
    all_rows = legacy_rows + ole_rows
    run = _identity_from_rows(all_rows, RUN_NAMES, ("PUSHBUTTON", "BUTTON"))
    cancel = _identity_from_rows(all_rows, CANCEL_NAMES, ("PUSHBUTTON", "BUTTON"))
    checkbox = _identity_from_rows(all_rows, ARRANGE_LABELS, ("CHECKBUTTON", "CHECKBOX"))
    legacy_count = sum(1 for row in uia.get("candidates", []) if row.get("legacy_pattern_available"))
    ole_object_count = sum(1 for obj in oleacc.get("objects", []) if obj.get("accessible_object"))
    if any(item.get("status") == "PASS" for item in (run, cancel, checkbox)):
        capability = "PASS_SEMANTIC_IDENTITY"
    else:
        capability = "BLOCKED_HOST_ACCESSIBILITY_HARD"
    return {
        "msaa_capability": capability,
        "legacy_pattern_candidates": legacy_count,
        "oleacc_accessible_objects": ole_object_count,
        "run_identity": run,
        "cancel_identity": cancel,
        "checkbox_identity": checkbox,
    }


def run_probe(title: str, timeout: int) -> dict[str, Any]:
    uia = probe_uia_legacy(title, timeout)
    oleacc = probe_oleacc(uia, title)
    classification = classify_msaa(uia, oleacc)
    return {
        "schema": "resolve-node-kit.arrange-msaa/v1",
        "title": title,
        "probe_scope": "existing_uia_checkbox_and_button_candidates_only",
        "menu_step5": "NOT_RERUN",
        "opencode_muse": "NOT_CALLED",
        "uia_legacy": uia,
        "oleacc": oleacc,
        "classification": classification,
        "invocation": "none; accDoDefaultAction not attempted",
        "status": classification["msaa_capability"],
        "ts": datetime.datetime.now().isoformat(timespec="seconds"),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--title", default=TITLE)
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--output", default=None)
    ap.add_argument("--evidence", default=None)
    args = ap.parse_args(argv)
    result = run_probe(args.title, args.timeout)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    print(text)
    for path in (args.output, args.evidence):
        if not path:
            continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
            fh.write("\n")
    return 0 if result.get("status") == "PASS_SEMANTIC_IDENTITY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
