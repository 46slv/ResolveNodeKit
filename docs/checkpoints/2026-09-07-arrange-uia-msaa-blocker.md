# Arrange UIA MSAA/IAccessible checkpoint — 2026-09-07

## Probe boundary

This continuation started from `c04a58b` on
`feat/arrange-uia-e2e-20260906`.  The existing step-5 menu Invoke evidence was
reused; it was not replayed.  OpenCode/Muse were not called.  The single host
probe opened the production AskUser dialog through the already-proven direct
Fusion `RunScript("Py", installed_entry)` route and inspected only the
previously observed four checkbox and five button UIA candidates.

No coordinate, control-order, blind-key, runtime-ID, or control Invoke was
used.  `accDoDefaultAction` was not attempted because no semantic identity was
proven.

## MSAA result

The candidate UIA rows were:

- 4 `Fusion::CheckBoxControl` / `Fusion::CustomCheckBox` rows;
- 5 `Fusion::ButtonControl` / `Fusion::CustomButton` rows;
- all still `ControlType.Group` with empty UIA names and automation IDs.

The Windows PowerShell UIAutomationClient on this host does not expose a
`System.Windows.Automation.LegacyIAccessiblePattern` type, so all nine rows
recorded `legacy_pattern_available=false` and the provider-level type lookup
failed.  The probe then used `oleacc.dll` directly:

- `AccessibleObjectFromWindow(dialog_hwnd, OBJID_CLIENT, IID_IAccessible)`
  returned `S_OK`;
- the accessible object exposed only the dialog root (`ROLE_SYSTEM_CLIENT`,
  `ChildId=0`);
- `AccessibleChildren` returned no semantic child rows for Run, Cancel, or
  either checkbox;
- the root `accName` was `ResolveNodeKit - Arrange`, but no action/checkbox
  semantic identity was present.

Machine-readable evidence is at
`D:\temp\uia\arrange_msaa_20260907.json`.  The repository probe and offline
classifier are `scripts/host/probe_arrange_msaa.py` and
`tests/host_ui/test_probe_arrange_msaa.py`.

Therefore the result is:

```text
MSAA_CAPABILITY: BLOCKED_HOST_ACCESSIBILITY_HARD
RUN_IDENTITY: BLOCKED_HOST_ACCESSIBILITY_HARD
CANCEL_IDENTITY: BLOCKED_HOST_ACCESSIBILITY_HARD
CHECKBOX_IDENTITY: BLOCKED_HOST_ACCESSIBILITY_HARD
```

The external desktop-automation search is closed at this boundary.  The hard
blocker is limited to semantic desktop identity; it does not claim that the
Arrange mutation itself is unsafe or that the host API is unavailable.

## Host cleanup

The dialog was closed once with the existing UIA `WindowPattern.Close` cleanup
route.  No Run/Cancel/checkbox action ran, no graph write or Undo ran, and no
project save occurred.  Final readback remained:

- Resolve Studio `21.0.3.7`, GUI instance responsive;
- project `PSD2Fusion` (`5a77c8a5-b609-4cc2-8224-e8098a96f493`);
- page `fusion`;
- only `Timeline 1` (`49f71479-5230-4c0c-9483-1b7356a911bd`);
- current comp: 967 tools, `COMPB_Modified=false`.

## Recommended product change

Remove the AskUser dialog from the normal development/verification gate by
separating one production handler from two evidence lanes:

1. **Common production handler** — accept an explicit immutable
   `ArrangeDialogState` (`include_unselected=False`, `ungroup=False` by
   default), perform target bind, snapshot, bounded arrange, readback,
   invariant comparison, rollback-on-mismatch, busy/result logging, and return
   a structured outcome.  Keep `ungroup=True` fail-closed until its exact
   restoration contract is proven.
2. **UI visibility proof** — keep the AskUser wrapper as a thin UI adapter.
   UIA/MSAA evidence proves title/candidate/provider capability and records the
   current hard blocker; it is not a prerequisite for the API behavior gate.
3. **Host behavior proof** — invoke the common handler directly on a disposable
   Fusion fixture with explicit default state.  Prove selected-only movement,
   unselected stability, connection/membership preservation, exact Undo,
   second-run `moved=0`, cleanup, Timeline 1 restoration, and no save through
   Fusion API readback.  A separate GroupOperator fixture proves default
   `ungroup=False` by preserving the group and its direct membership.

This preserves the user-facing AskUser path while making ordinary development
and CI behavior repeatable without a human click.  It also prevents an
unavailable desktop accessibility provider from being mistaken for a product
behavior failure.
