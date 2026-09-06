# Arrange dialog / execution UX — v1

Status: design contract

This document defines the first user-facing execution flow for ResolveNodeKit arrangement commands.

The tool is intended to be run manually from Resolve/Fusion, configured in a small modal dialog before any graph mutation occurs, and to show an explicit busy/progress state while arrangement is running.

## 1. User flow

```text
Run ResolveNodeKit Arrange script
        |
        v
+----------------------------------+
| ResolveNodeKit - Arrange         |
|                                  |
| [ ] Include unselected nodes     |
| [ ] Ungroup before arranging     |
|                                  |
|            [Run] [Cancel]        |
+----------------------------------+
        |
        | Run
        v
+----------------------------------+
| ResolveNodeKit - Arrange         |
|                                  |
| Arranging...                     |
| Reading / Planning / Applying /  |
| Verifying                        |
|                                  |
| Please wait                      |
+----------------------------------+
        |
        +--> success: close automatically
        |
        +--> failure: rollback, close busy UI,
             then show a clear error/result message
```

Japanese UI copy may use:

```text
[ ] 選択されていないノードも整列
[ ] グループ化を解除して整列

[実行] [キャンセル]
```

Running-state copy may use:

```text
整列しています…
読み取り中…
配置を計算中…
整列を適用中…
確認中…
```

Both checkboxes are **OFF by default**.

The setup dialog is intentionally small. Spacing/style tuning should not become a wall of options in v1.

## 2. Scope checkbox

### `[ ] 選択されていないノードも整列`

OFF:

- arrange only the current explicit selection;
- if a selected item is a GroupOperator and Group preservation is active, its interior may be arranged recursively under the same policy;
- nodes outside the selected arrangement scope are not moved;
- if no usable selection exists, `Run` should fail closed with a clear visible message rather than silently arranging the whole comp.

ON:

- arrange the full active Fusion composition;
- every root/local Group scope may be processed under the selected Group policy;
- this is the explicit whole-comp mode.

This checkbox makes scope obvious and prevents a one-click script from unexpectedly moving the entire composition.

## 3. Group policy checkbox

### `[ ] グループ化を解除して整列`

OFF — default / preserve mode:

- preserve every existing GroupOperator;
- preserve direct parent/child membership;
- recursively arrange Group interiors using the same semantic/grid policy;
- do not create new Groups merely for readability;
- semantic regions may be expressed by spacing and alignment alone.

ON — flatten mode:

- ungroup only Groups that belong to the explicit arrangement scope;
- preserve tool identities, connections, parameters, keyframes, and media state;
- after flattening, arrange the resulting flat/local graph using the same semantic-grid policy;
- the operation must be snapshot/readback/rollback protected;
- the UI should display a concise warning because Group membership is a structural change.

Recommended warning text:

> グループ構造を変更します。接続と処理内容は維持したまま整列します。

### Scope rule for ungrouping

To avoid surprising structural changes:

- selection mode: ungroup only GroupOperator nodes explicitly included in the selected arrangement scope;
- whole-comp mode: all GroupOperators in the active comp are eligible;
- selecting ordinary child nodes inside a Group does not implicitly ungroup their parent unless the parent Group itself is in the ungroup scope.

This rule should be host-tested before release.

## 4. Semantic regions are not the same as GroupOperators

ResolveNodeKit should not require every visually meaningful module to be a Fusion GroupOperator.

The planner may recognize logical regions such as:

- horizontal Merge backbone;
- vertical Merge reduction column;
- layer serial pipeline;
- effect branch;
- disconnected/auxiliary cluster;
- PSD-derived semantic region.

These regions may be expressed only by grid alignment and whitespace.

GroupOperator is therefore an optional container/presentation structure, not the only representation of semantic organization.

This is important because heavy Group usage makes later manual insertion/editing more cumbersome.

## 5. No hidden mutations before Run

Opening the setup dialog performs no layout writes.

Before the user presses `Run`, the implementation may only perform bounded read-only inspection needed to:

- inspect selection;
- count affected nodes/Groups;
- determine whether the requested mode is supported.

`Cancel` performs zero graph mutation.

If validation fails immediately after `Run` (for example: empty selection while whole-comp mode is OFF), show a clear visible message. Do not enter a silent no-op state.

## 6. Running-state dialog

After the user presses `Run` and the request passes immediate validation, ResolveNodeKit must show visible execution state **before any potentially noticeable graph traversal, planning, or mutation**.

### Required behavior

- the user must be able to tell that ResolveNodeKit is still working;
- the running-state UI must appear before long snapshot/planning/apply work;
- the initial text may simply be `整列しています…`;
- when the host UI path permits safe updates, show coarse stages:
  1. `読み取り中…`
  2. `配置を計算中…`
  3. `整列を適用中…`
  4. `確認中…`
- do not expose misleading percentage progress unless the total work is genuinely measurable;
- do not require the progress UI itself to know every node-level step;
- logging/evidence continues independently of the visible progress UI.

### Cancellation policy during execution

v1 should **not** provide an active Cancel button once bounded host mutation has begun.

Reason: mid-operation cancellation is not safe unless the implementation has proven cooperative cancellation plus complete rollback for every stage.

Therefore:

- Cancel is available in the setup dialog before execution;
- after execution begins, the running-state dialog is informational only;
- a future Cancel button may be added only after exact rollback/cancellation semantics are host-proven.

### Completion behavior

Success:

- complete readback/invariant verification first;
- close the running-state dialog automatically;
- optionally show a compact completion message such as `整列しました: 12ノード / 8移動` if this does not create unnecessary click friction.

Failure:

- perform rollback according to the host safety contract;
- verify restoration as far as the command contract requires;
- close the running-state dialog;
- show a visible error/refusal message with a concise reason;
- keep the detailed traceback/diagnostic in the run log.

A user must never have to infer failure only from Console output or a hidden log.

## 7. Run safety sequence

After `Run`:

1. validate immediate UI/scope preconditions;
2. show the running-state UI;
3. bind exact project/timeline/comp;
4. resolve arrangement scope;
5. snapshot positions, membership, and structural invariants;
6. if flatten mode: perform bounded ungroup operation and read back structure;
7. build semantic snapshot;
8. plan on the logical grid without host writes;
9. apply bounded position writes;
10. read back positions/structure;
11. verify invariants;
12. rollback on mismatch;
13. commit one Undo event where the host path is proven;
14. close the running-state UI and present completion/error state.

Flatten mode must not be implemented as a blind `Ungroup -> hope -> Tidy` sequence.

## 8. Implementation boundary

The contract requires a visible busy state, but does not force one specific Fusion UI mechanism.

The implementation may use a host-proven `UIManager` / `Dispatcher` window or another Resolve/Fusion-native mechanism if it can:

- render before the long operation starts;
- remain visible while the operation runs;
- update coarse status safely if desired;
- close deterministically on success/failure;
- avoid blind keyboard/mouse automation;
- avoid moving host mutation work to an unsafe background thread merely to keep the UI responsive.

If host UI event pumping is required, it must be measured/proven rather than guessed.

## 9. v1 intentionally does not expose

Do not add these controls to the first setup dialog unless later evidence requires them:

- raw X/Y spacing numeric fields;
- crossing-weight sliders;
- backbone heuristics;
- Merge rail orientation controls;
- host readback tolerance;
- Group geometry internals;
- automatic visual Group expansion;
- percentage progress without a measurable total;
- mid-operation Cancel before rollback semantics are proven.

These remain policy/diagnostic concerns, not ordinary user choices.

## 10. Future optional controls

Only after the basic modal is proven useful:

- `[ ] プレビューのみ` / dry-run summary;
- semantic policy selector (`Standard` / `Semantic`);
- a compact `Advanced...` section;
- saved per-user defaults;
- cooperative cancel after exact rollback semantics are host-proven.

The initial product should remain: script -> two checkboxes -> Run/Cancel -> visible running state -> automatic finish/error.
