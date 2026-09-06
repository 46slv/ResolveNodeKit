# ADR-0002: Arrange UI, editable Group policy, and orthogonal grid

Status: proposed
Date: 2026-09-06

## Context

Two practical findings changed the layout UX direction:

1. existing GroupOperator-based organization is readable, but later inserting/editing nodes inside Groups is cumbersome;
2. the user prefers a visibly regular row/column grid with roughly 2–3 grid spaces between nodes and dislikes unnecessary diagonal connections.

The current measured Fusion reference also shows multiple semantic motifs rather than one universal rail:

- horizontal root Merge cascades;
- vertical Merge reduction columns;
- Group-local serial pipelines.

Therefore ResolveNodeKit should separate:

- semantic organization;
- physical GroupOperator containment;
- arrangement scope;
- orthogonal layout policy.

## Decision

### 1. Manual Arrange dialog

The first arrange UX is:

```text
[ ] 選択されていないノードも整列
[ ] グループ化を解除して整列

[実行] [キャンセル]
```

Both options default OFF.

### 2. Group preservation is default

When `Ungroup before arranging` is OFF:

- preserve GroupOperators;
- recursively arrange their interiors;
- do not create new Groups solely to show semantic regions.

### 3. Ungroup is explicit

When the option is ON:

- flatten only Groups inside the explicit arrangement scope;
- preserve connections and processing state;
- verify structural readback and rollback;
- then apply the same semantic-grid layout to the flattened graph.

### 4. Semantic region != GroupOperator

A visual module may be expressed through spacing/alignment alone. GroupOperator is optional containment, not the sole representation of meaning.

### 5. Orthogonal logical grid

The planner uses integer logical rows/columns and maps them onto the host grid through the adapter.

Ordinary nodes normally use a 2–3-cell pitch. Wider Merge/Group clearance uses whole-cell expansion.

### 6. Avoid unnecessary diagonals

Backbones align horizontally; branches align vertically; vertical reduction rails remain vertical. Avoidable diagonal edges are treated as a layout defect. v1 does not create routing-only tools to eliminate topology-forced diagonals.

## Consequences

Positive:

- arranging after manual edits remains predictable;
- users can choose readable Group preservation or edit-friendly flattening;
- semantic layout no longer depends on aggressive Group creation;
- regular rows/columns should make large Merge-heavy graphs easier to scan;
- spacing can grow without losing grid regularity.

Costs / risks:

- ungroup mode changes structure and therefore requires stronger host validation than position-only tidy;
- selection/Group scope semantics must be exact to avoid flattening unintended Groups;
- some diagonals may remain unless routing nodes are introduced in a future explicit feature;
- visually uniform cells need separate X/Y host calibration because Fusion snap units differ.

## Related contracts

- `docs/ARRANGE_DIALOG.md`
- `docs/ORTHOGONAL_GRID.md`
- `docs/SEMANTIC_LAYOUT.md`
- `docs/SEMANTIC_LAYOUT_ACCEPTANCE.md`
- `docs/GROUPS.md`
