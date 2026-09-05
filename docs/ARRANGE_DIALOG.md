# Arrange dialog / execution UX — v1

Status: design contract

This document defines the first user-facing execution flow for ResolveNodeKit arrangement commands.

The tool is intended to be run manually from Resolve/Fusion, then configured in a small modal dialog before any graph mutation occurs.

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
```

Japanese UI copy may use:

```text
[ ] 選択されていないノードも整列
[ ] グループ化を解除して整列

[実行] [キャンセル]
```

Both checkboxes are **OFF by default**.

The dialog is intentionally small. Spacing/style tuning should not become a wall of options in v1.

## 2. Scope checkbox

### `[ ] 選択されていないノードも整列`

OFF:

- arrange only the current explicit selection;
- if a selected item is a GroupOperator and Group preservation is active, its interior may be arranged recursively under the same policy;
- nodes outside the selected arrangement scope are not moved;
- if no usable selection exists, `Run` should fail closed with a clear message rather than silently arranging the whole comp.

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

Opening the dialog performs no layout writes.

Before the user presses `Run`, the implementation may only perform bounded read-only inspection needed to:

- inspect selection;
- count affected nodes/Groups;
- determine whether the requested mode is supported.

`Cancel` performs zero graph mutation.

## 6. Run safety sequence

After `Run`:

1. bind exact project/timeline/comp;
2. resolve arrangement scope;
3. snapshot positions, membership, and structural invariants;
4. if flatten mode: perform bounded ungroup operation and read back structure;
5. build semantic snapshot;
6. plan on the logical grid without host writes;
7. apply bounded position writes;
8. read back positions/structure;
9. verify invariants;
10. rollback on mismatch;
11. commit one Undo event where the host path is proven.

Flatten mode must not be implemented as a blind `Ungroup -> hope -> Tidy` sequence.

## 7. v1 intentionally does not expose

Do not add these controls to the first dialog unless later evidence requires them:

- raw X/Y spacing numeric fields;
- crossing-weight sliders;
- backbone heuristics;
- Merge rail orientation controls;
- host readback tolerance;
- Group geometry internals;
- automatic visual Group expansion.

These remain policy/diagnostic concerns, not ordinary user choices.

## 8. Future optional controls

Only after the basic modal is proven useful:

- `[ ] プレビューのみ` / dry-run summary;
- semantic policy selector (`Standard` / `Semantic`);
- a compact `Advanced...` section;
- saved per-user defaults.

The initial product should remain: script -> two checkboxes -> Run/Cancel.
