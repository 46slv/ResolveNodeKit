# Orthogonal semantic grid — v1

Status: layout policy contract

ResolveNodeKit should arrange Fusion nodes on a **logical orthogonal grid** so that rows/columns are visually regular and avoid unnecessary diagonal connections.

This policy is based on the current user preference and the measured Fusion reference data in `docs/reference/2026-09-06-fusion-timeline1-layout.json` / `2026-09-06-fusion-merge-parallel-note.md`.

## 1. Core visual rule

Prefer:

```text
A ---- B ---- C ---- D
       |      |
       X      Y
```

over:

```text
A --- B
       \
        X
```

When an edge can be represented by placing its endpoints on the same row or the same column without creating a harder conflict, the planner should do so.

The target visual language is mostly horizontal and vertical relationships, not arbitrary diagonal chains.

## 2. Logical grid, not raw host coordinates

Fusion host snapping has measured X/Y behavior that is not numerically identical (`x` snapping around 0.5 units, `y` around 1.0 in the measured host path).

Therefore semantic layout should use integer logical coordinates first:

```text
GridPoint(column: int, row: int)
```

and map them to host coordinates through the Fusion adapter:

```text
host_x = origin_x + column * cell_x
host_y = origin_y + row    * cell_y
```

`cell_x` and `cell_y` are calibrated separately so the visible lattice is regular while respecting the host grid.

The planner should never depend on `cell_x == cell_y` numerically.

## 3. Default node pitch

The first semantic policy should use a regular integer-cell pitch.

Recommended starting policy:

```text
minimum_node_gap_cells = 2
default_node_gap_cells = 3
```

Meaning:

- adjacent ordinary nodes normally sit 3 logical cells apart;
- 2 cells is allowed for compact, conflict-free local chains;
- larger gaps are allowed only as integer-cell expansions.

This matches the current preference for roughly 2–3 grid spaces between nodes while preserving a uniform row/column lattice.

## 4. Elastic gaps remain grid-aligned

Merge-side widening remains allowed, but widening must stay on the same logical grid.

For example:

```text
3 cells -> 4 cells -> 5 cells -> 6 cells
```

not arbitrary floating offsets.

Thus the layout may become wider while still looking intentional and regular.

## 5. Horizontal backbone rule

For a horizontal backbone / Merge cascade:

- all backbone nodes share the same logical row;
- downstream order increases by whole columns;
- ordinary pitch defaults to 2–3 cells;
- Merge intervals may expand by whole-cell increments when branch/Group clearance requires it.

Example:

```text
row 0:  BG --- M1 --- M2 ----- M3 --- OUT
                    |          |
row -3:           Branch A   Group B
```

## 6. Vertical branch rule

A branch feeding a backbone node should normally share the receiver's logical column.

```text
Branch
  |
  |
Merge ---- next
```

This produces a vertical connection instead of a diagonal one.

Upstream nodes in the branch should remain on the same column where practical, separated by the same 2–3-cell pitch.

## 7. Vertical Merge reduction columns

The measured 1109-tool reference contains real vertical Merge reduction columns.

For this motif:

- Merge nodes share the same logical column;
- Background chaining runs vertically;
- Foreground sources enter horizontally from a side lane;
- vertical pitch uses regular integer row gaps;
- side branch spacing may widen the horizontal distance by whole cells.

This is a first-class semantic motif, not a malformed horizontal rail.

## 8. Orientation detection

The planner should distinguish at least:

- `HorizontalBackboneRail`
- `VerticalReductionRail`
- `SerialPipeline`
- `BranchColumn`

Orientation should be inferred primarily from graph semantics / BG-FG wiring and only secondarily from current coordinates.

Existing coordinates are useful evidence, but layout must not simply preserve arbitrary historical diagonals.

## 9. Diagonal-edge policy

### Avoidable diagonal

A diagonal is avoidable when one endpoint can be aligned to the other's row/column without:

- violating graph order;
- causing overlap;
- causing a worse crossing conflict;
- breaking a higher-priority semantic rail.

Avoidable diagonals should be treated as layout violations.

### Unavoidable diagonal

Some graph topologies cannot be made fully orthogonal by endpoint placement alone.

v1 may retain an unavoidable diagonal when eliminating it would require:

- creating PipeRouter/dummy tools;
- rewiring;
- destroying another primary rail;
- introducing overlap or a worse crossing.

The planner must not create routing-only tools merely to satisfy orthogonality in v1.

Recommended diagnostic:

```text
diagonal_edge_count
aavoidable_diagonal_edge_count
```

(implementation should use a correctly spelled stable field such as `avoidable_diagonal_edge_count`).

Acceptance target:

```text
avoidable_diagonal_edge_count == 0
```

for supported semantic fixtures.

## 10. Group-local application

The same grid is applied independently in every Group scope.

A child Group's local `(column,row)` coordinates are local to that Group. Parent placement treats the Group as a logical box aligned to the parent's grid.

This gives visual consistency without flattening hierarchy.

## 11. Ungroup mode

If the Arrange dialog's `Ungroup before arranging` option is enabled:

- the resulting flattened nodes are reclassified into semantic rails/regions;
- they are then placed on the same logical orthogonal grid;
- previous Group boundaries do not force spacing unless retained as semantic-region hints;
- graph invariants must be verified before and after flattening.

Ungrouping should make later manual insertion easier while preserving the same visual grammar.

## 12. Acceptance summary

A good v1 layout should look intentionally gridded:

- rows are rows;
- columns are columns;
- ordinary gaps are usually 2–3 cells;
- wider gaps are integer multiples of the same grid;
- horizontal processing uses horizontal rails;
- vertical branches use vertical columns;
- vertical Merge reductions remain vertical;
- avoidable diagonal connections are eliminated;
- no graph semantics are changed merely to make wiring orthogonal.
