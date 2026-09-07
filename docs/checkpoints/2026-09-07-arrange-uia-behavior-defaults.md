# Arrange UIA behavioral-default checkpoint — 2026-09-07

## Contract separation

This continuation did not rerun the step-5 menu probe and did not call
OpenCode/Muse. The existing menu identity evidence was reused. A second route,
`fusion:RunScript("Py", installed_entry)`, opened the production Arrange
setup dialog against a fresh disposable project/comp.

The evidence now has two explicit layers:

- `UI_ACCESSIBILITY`: dialog visibility is observable, but checkbox labels,
  standard CheckBox control types, TogglePattern, and Run/Cancel semantic
  identities are not exposed. These records use `BLOCKED_HOST_ACCESSIBILITY`.
- `PRODUCT_BEHAVIOR`: default values remain unverified because safe Run/Cancel
  identity invocation is unavailable. No checkbox was touched and no control
  order was guessed.

## B1 fixture and result

Disposable project `_mcp_RNK_UIA_B1` contained timeline `RNK_UIA_B1` and a six-
tool comp. Four tools were selected (`MediaOut1`, `RNK_B1_BG1`, `RNK_B1_BG2`,
`RNK_B1_M1`); two unselected tools were placed far away (`RNK_B1_U1`,
`RNK_B1_U2`). Three connections and the pre-snapshot were read back through the
Fusion API.

The setup window had 17 descendants. The four checkbox candidates were
`Fusion::CheckBoxControl` / `Fusion::CustomCheckBox` Group nodes with no name,
value, label association, or TogglePattern. The five button candidates likewise
had empty semantic identity metadata, despite exposing InvokePattern/ValuePattern.
`run_button_identity=false` and `cancel_button_identity=false`; no Run or Cancel
Invoke was attempted. The asynchronous host call was closed only with
WindowPattern.Close for cleanup, not counted as a behavioral Cancel pass.

Therefore:

- B1 effective `include_unselected=false`: `BLOCKED_HOST_ACCESSIBILITY`.
- B2 effective `ungroup=false`: `NOT_RUN` because B1 could not safely Run.
- B3 Cancel: `BLOCKED_HOST_ACCESSIBILITY`.
- B4 busy/result: `NOT_RUN`; no busy text or result dialog is claimed.
- B5 movement/Undo/second-run: `NOT_RUN`; no Arrange mutation was permitted.

## Cleanup and evidence

The disposable project `_mcp_RNK_UIA_B1` was deleted without saving. Resolve was
then loaded back to `PSD2Fusion`, Fusion page, `Timeline 1`; its 967-tool comp
read back `COMPB_Modified=false`. No project save was performed.

Schema-v2 evidence:

- `D:\temp\uia\arrange_uia_behavior_20260907.jsonl`
- `D:\temp\uia\arrange_uia_behavior_20260907.json`

The smallest next gate is a safe, semantic UIA identity for the Run and Cancel
buttons. This checkpoint does not propose or attempt a Resolve accessibility
provider fix; it only records the measured host boundary and preserves the
existing fail-closed policy.
