# Semantic layout empirical baseline — Fusion Timeline 1, 2026-09-06

Status: measured read-only reference

This document connects the semantic-layout architecture to a real 1109-tool Fusion composition captured from the currently open PSD2Fusion project.

Primary files:

- `docs/reference/2026-09-06-fusion-timeline1-layout.json`
- `docs/reference/2026-09-06-fusion-merge-parallel-note.md`

The reference is read-only host evidence. It is not a golden output that every future graph must reproduce exactly.

## 1. Measured envelope

Observed composition:

- 1109 tools
- 29 GroupOperators
- 257 Merge tools
- max observed Group nesting depth: 2
- root scope: 103 tools
- host position snap evidence: X ~0.5, Y ~1.0 logical host increments with small type/readback offsets

The reference JSON contains all measured node names/types/positions/parent Group membership and Merge BG/FG connection information. It does **not** represent a complete all-tool edge list, so it must not be treated as a full topology fixture.

## 2. Motif A — horizontal root Merge cascade

Measured root backbone example:

- snapped row around `y=-16`
- x range approximately `-4.0 -> 31.5`
- typical pitch `2.0-2.5`
- Group outputs are collected into Merge nodes along the row

Design implication:

- horizontal Merge cascades are a first-class rail motif;
- ordinary spacing in the semantic planner should begin near a 2–3 logical-cell cadence rather than arbitrary continuous placement;
- wider intervals remain valid when branch/Group clearance requires them.

## 3. Motif B — vertical Merge reduction columns

Measured columns include:

- six Merge nodes around `x=29`
- three Merge nodes around `x=31.5`

Observed wiring convention:

- Background comes from the Merge above in the same column;
- Foreground arrives from the side from another Group/effect branch.

Design implication:

This is not a failed horizontal layout. It is a meaningful vertical reduction motif.

The semantic planner should explicitly classify and preserve an orthogonal structure like:

```text
       side FG
          |
          v
      [ Merge ]
          |
          | BG
       side FG -> [ Merge ]
                    |
                    | BG
                 [ Merge ]
```

or its visually equivalent left/right side-feed form.

## 4. Motif C — Group-local serial pipelines

Measured Group interiors frequently follow a regular left-to-right processing sequence such as:

```text
Loader -> ChangeDepth / materialize -> alpha operations -> ChannelBoolean -> Merge
```

Typical local x pitch is approximately 3.0 host layout units in the captured arrangement.

Design implication:

- Group-local serial pipelines should use a regular horizontal lattice;
- 2–3 semantic cells is a reasonable initial policy;
- this regular pipeline grammar should still apply if the user later chooses to ungroup the container.

## 5. Group density / editability implication

Only 29 GroupOperators organize more than 1100 tools, with only a small subset nested beyond one level.

This supports a key product distinction:

> semantic organization does not require turning every meaningful region into a GroupOperator.

GroupOperators are useful for containment and hiding complexity, but heavy Group usage increases friction when manually inserting nodes later.

ResolveNodeKit should therefore recognize semantic regions independently of Group containment and allow the user to choose whether existing Groups are preserved or flattened during an Arrange operation.

See `ARRANGE_DIALOG.md` and ADR-0002.

## 6. Orthogonal-grid implication

The reference contains both long same-row chains and same-column Merge clusters.

This supports a layout policy where:

- primary rails share rows;
- branches/reductions share columns;
- node gaps use integer logical-cell increments;
- wider gaps remain aligned to the same grid;
- unnecessary diagonal endpoint relationships are treated as a defect.

See `ORTHOGONAL_GRID.md`.

## 7. Fixture use

The 1109-node JSON is useful for:

- position-distribution regression;
- parent Group membership regression;
- rail/row/column motif detection;
- Merge BG/FG orientation detection;
- spacing-policy tuning;
- synthetic extraction of smaller semantic fixtures;
- large layout hashing/performance tests.

It is not sufficient by itself for:

- proving all node connections unchanged;
- a complete graph-topology reconstruction;
- processing-parameter invariance;
- runtime Group expansion semantics.

Those claims require their separate evidence contracts.

## 8. Initial measured priors

These are starting priors, not immutable constants:

```text
ordinary semantic gap:     2-3 logical cells
horizontal Merge cadence:  ~2-2.5 measured host units
Group serial cadence:      ~3.0 measured host units
vertical reduction cadence: ~2-4 measured host units
host snap evidence:        x ~0.5 / y ~1.0
```

The implementation should express these as semantic/grid policy, then validate them against fixtures and host canaries rather than hard-coding one historical composition.
