# ADR-0002: Arrange UI, editable Group policy, and orthogonal grid

Status: proposed; flatten-all continuation amended 2026-09-08
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

### 1. FIRST_USABLE Arrange dialog

The first usable product path arranges the entire active Fusion composition:

```text
ResolveNodeKit - Arrange
現在のFusionコンポジション全体を整列します。

[実行] [キャンセル]
```

The production state is `include_unselected=True, ungroup=False`.  The former
selection checkbox is retained only for regression/experimental coverage, not
as a first-release gate.

### 2. Group preservation is default

When `Ungroup before arranging` is OFF:

- preserve GroupOperators;
- recursively arrange their interiors;
- do not create new Groups solely to show semantic regions.

### 3. Ungroup is not exposed in FIRST_USABLE

The default UI `ungroup=True` request remains fail-closed:

- no production UI control exposes it;
- the direct request now delegates to the amended `flatten_all_comp` seam, but
  refuses mutation until an explicit host-native primitive and exact
  structural restoration are host-proven;
- preserve-mode recursive layout is the only release scope.

The 2026-09-08 amendment makes flatten-all a required continuation gate rather
than an optional future behavior. It must remove only eligible Groups,
preserve non-Group identity and endpoint mappings, arrange in the same owned
Undo transaction, and restore the original hierarchy exactly on failure. The
current Resolve Studio 21.0.3.7 host exposes no measured primitive, so the
capability is `BLOCKED_HOST_API`, not a UIA/MSAA blocker, and the checkbox
remains hidden.

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
- selection-only and ungroup scope semantics remain future/experimental lanes;
- some diagonals may remain unless routing nodes are introduced in a future explicit feature;
- visually uniform cells need separate X/Y host calibration because Fusion snap units differ.

## Related contracts

- `docs/ARRANGE_DIALOG.md`
- `docs/ORTHOGONAL_GRID.md`
- `docs/SEMANTIC_LAYOUT.md`
- `docs/SEMANTIC_LAYOUT_ACCEPTANCE.md`
- `docs/GROUPS.md`
