# Arrange UIA E2E recovery checkpoint — 2026-09-07

## Recovery boundary

- Branch: `feat/arrange-uia-e2e-20260906`
- Recovered HEAD: `bf42239bbdca6903db2a48e38c01293ca32c7bf1`
- No tracked changes, staged changes, or deleted files were present at recovery.
- The only local implementation artifacts were the untracked
  `scripts/host/verify_arrange_ui.py` and `scripts/host/busy_watch.py`.
- `D:\temp\uia_worker.log` and the pre-existing `D:\temp\uia\` directory were absent.
  The recovered OpenCode artifacts were `uia_e2e.jsonl`, `uia_managed_out*.json`,
  `uia_chain.json`, `uia_rnk.json`, and related probe scripts.
- Muse's last successful boundary was the disposable fixture/pre-snapshot and
  managed UIA menu probing. Its repeated step-5 menu route then stalled and the
  worker ended at HTTP 429; no worker commit, cleanup, or final E2E report was
  present.

## Exact resume and completed local work

The resume point was step 5: identity-bind the real `UiMainWindowImp`, repair the
menu route, and continue from the existing fixture rather than recreating it.

- The menu route now binds the Resolve main window by UIA identity instead of the
  transient `MainWindowHandle` (which can be a `QMenu` popup).
- `Workspace > Scripts > ResolveNodeKit_Arrange` is invoked by `InvokePattern`.
  On Resolve Studio 21.0.3.7 the `Comp` category element is not exposed, so the
  evidence records the safe direct-entry route and `category_element_exposed=false`.
- Window enumeration/dumping now includes Resolve-owned descendants, and the
  verifier preserves automation id, label association, supported patterns, and
  toggle evidence.
- `busy_watch.py` follows the same main-window descendant boundary.
- The wait probe now bounds each PowerShell probe by the caller's deadline; a
  short fail-closed wait cannot silently become a fixed 30-second wait.
- Three focused tests were added under `tests/host_ui/` for Qt checkbox
  classification, labelled CheckBox/Toggle readback, and result `moved=` parsing.

## Host evidence

The disposable `RNK_UIA_E2E` comp was read back before and after the setup
interaction: six tools, four explicitly selected (`MediaOut1`, `RNK_BG1`,
`RNK_BG2`, `RNK_M1`), all positions at `(0, 0.009)`, three unchanged edges,
`TOOLH_GroupParent=null` for all tools, zero groups, and `COMPB_Modified=false`.

The setup window was found by UIA with 17 descendants, but the two required
labels were not exposed. The four apparent checkbox controls are
`Fusion::CheckBoxControl` / `Fusion::CustomCheckBox` `ControlType.Group` nodes
with empty `Name`, `Value`, `HelpText`, and `LabeledBy`; none exposes
`ControlType.CheckBox` or `TogglePattern`. No order-based or coordinate-based
fallback was attempted. `WindowPattern.Close` was observed once, but a persistent
Fusion `QWidget` provider remained in the tree, so logical dialog absence is not
claimed as PASS. This is the narrow UIA capability blocker.

Machine-readable evidence: `D:\temp\uia\arrange_uia_e2e_codex_20260907_final.jsonl`
and its assembled `D:\temp\uia\arrange_uia_e2e_codex_20260907_final.json`.
The earlier raw dump is retained at `D:\temp\uia\arrange_uia_e2e_codex_20260907.jsonl`.

## Cleanup and verification

The exact disposable timeline and two worker-created archive timelines were
deleted only after identity/name verification and the MCP confirmation guard:

- `RNK_UIA_E2E`
- `RNK_UIA_E2E_archived_v01`
- `RNK_UIA_E2E_archived_v02`

The saved Resolve state token restored Fusion page and `Timeline 1`. A fresh list
contains only `Timeline 1`; no project save was performed.

Offline verification: `103/103` unittest tests pass and `python -m compileall -q
src scripts tests` passes.

## Smallest next gate

Expose the AskUser checkbox labels and a label-associated `ControlType.CheckBox`
or `TogglePattern` through the Resolve/Fusion accessibility provider (or provide a
documented accessibility identity for those controls). Then resume at setup step
7 only: verify OFF/OFF by label, invoke Cancel/Run, and continue busy/result,
Undo, and second-run checks. Do not replay the recovered fixture/menu probes or
use coordinates, blind keys, or control-order guesses.
