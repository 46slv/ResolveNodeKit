# Arrange dialog / execution UX — v1

Status: FIRST_USABLE product contract

This document defines the first user-facing execution flow for ResolveNodeKit
arrangement commands.  The FIRST_USABLE path arranges the active Fusion
composition as a whole while preserving GroupOperators. Selection-only remains
an experimental lane. Flatten-all is a separate amendment-required,
host-capability-gated lane and is not exposed by this default dialog.

The tool is run from Resolve/Fusion with a small confirmation dialog before
any graph mutation, followed by the existing visible busy/progress state.
The default UI is preserve-mode. The 2026-09-08 continuation amendment adds
flatten-all as a separate host-gated structural lane; it is not shown until
the host supplies an identity-preserving Ungroup primitive and exact Undo
evidence.

## 1. User flow

```text
Run ResolveNodeKit Arrange script
        |
        v
+----------------------------------+
| ResolveNodeKit - Arrange         |
|                                  |
| 現在のFusionコンポジション全体を |
| 整列します。                     |
|                                  |
|            [実行] [キャンセル]   |
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

Japanese UI copy is:

```text
現在のFusionコンポジション全体を整列します。

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

The production request is always `include_unselected=True` and
`ungroup=False`.  Selection-only and ungroup controls are not exposed in the
FIRST_USABLE setup dialog.

## 2. Whole-composition scope (FIRST_USABLE)

The active Fusion composition is the arrangement scope.  The production
handler receives:

```text
ArrangeDialogState(include_unselected=True, ungroup=False)
```

Every root/local Group scope is planned recursively.  Selection-only behavior
(`include_unselected=False`) remains available to regression tests and a future
experimental lane, but it is not part of the FIRST_USABLE release gate.

## 3. Group policy (FIRST_USABLE preserve mode)

The first usable path always preserves Groups:

- preserve every existing GroupOperator;
- preserve direct parent/child membership;
- recursively arrange Group interiors using the same semantic/grid policy;
- do not create new Groups merely for readability;
- semantic regions may be expressed by spacing and alignment alone;
- `ungroup=True` remains fail-closed and is not exposed by FIRST_USABLE UI until
  exact structural restoration is host-proven. The current measured host has
  no such primitive, so the installed product intentionally remains
  preserve-only.

### 3.1 Amended flatten-all lane

The production API now contains a guarded `flatten_all_comp` seam for a host
adapter to supply an explicit primitive. Its contract is:

```text
snapshot -> deepest-first ungroup -> flat readback
-> semantic Arrange in one Undo transaction -> exact grouped Undo/rollback
```

Generic `DoAction`/`QueueAction`, blind UI, delete/recreate, and guessed
settings transformations are not accepted. The live Resolve 21.0.3.7
capability probe found no callable primitive and `ungroup=True` refused with
zero writes; therefore no checkbox is exposed and no flatten PASS is claimed.

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

Before the user presses the confirmation button, the implementation may only
perform bounded read-only inspection needed to:

- identify the active composition;
- count nodes and Groups;
- determine whether preserve-mode recursive layout is supported.

`Cancel` performs zero graph mutation.

If validation fails immediately after confirmation, show a clear visible
message. Do not enter a silent no-op state.

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

1. validate the active-composition and preserve-mode preconditions;
2. show the running-state UI;
3. bind exact project/timeline/comp;
4. resolve arrangement scope;
5. snapshot positions, membership, and structural invariants;
6. build the recursive semantic snapshot;
7. plan on the logical grid without host writes;
8. apply bounded position writes;
9. read back positions/structure;
10. verify invariants;
11. rollback on mismatch;
12. commit one Undo event where the host path is proven;
13. close the running-state UI and present completion/error state.

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

The initial product should remain: script -> whole-composition confirmation ->
Run/Cancel -> visible running state -> automatic finish/error.
