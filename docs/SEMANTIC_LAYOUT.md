# Fusion semantic layout architecture — v1

Status: design contract / implementation-ready architecture

This document defines the next layout-quality direction for ResolveNodeKit Fusion graphs. It is intentionally separate from the currently host-verified generic `Tidy Graph` / `Tidy Nested` behavior. Existing proven commands remain the safety baseline until this semantic policy is independently tested and host-verified.

## 1. Design decision

ResolveNodeKit should optimize for **semantic readability before uniform density**.

A layout is allowed to become wider when the extra width makes the composition easier to read. In particular, **Merge-side spacing may expand beyond the default rail spacing** when needed to preserve a clear composition backbone, branch provenance, Group boundaries, or wire readability.

Uniform compactness is not a hard requirement.

The intended visual language is:

- main processing flow reads left-to-right;
- Merge chains form a visible horizontal rail;
- branch sources usually feed vertically from above;
- nested `GroupOperator`s remain groups and read as framed local subgraphs;
- the same layout philosophy is applied recursively inside every Group scope;
- local readability beats whole-composition packing density.

Visual references:

- [`references/semantic-layout-reference-01.svg`](references/semantic-layout-reference-01.svg)
- [`references/semantic-layout-reference-02.svg`](references/semantic-layout-reference-02.svg)

Reference 02 is especially important: the wider spacing around the Merge rail is **intentional and acceptable** when it improves readability.

## 2. Non-negotiable invariants

Semantic layout remains a layout-only feature.

It must not:

- change any Fusion connection;
- change tool processing parameters;
- change keyframes/expressions;
- create/delete tools merely to improve layout;
- alter media, render state, or grade state;
- flatten or ungroup `GroupOperator`s;
- alter parent/child Group membership;
- silently change Group expanded/collapsed state unless the explicit command owns that display mutation;
- rely on blind UI automation.

Host writes still follow:

`target bind -> snapshot -> pure planning -> bounded write -> readback -> invariant comparison -> rollback on mismatch`

## 3. Layout model: local scopes, not one flat graph

The composition is treated as a hierarchy of **layout scopes**.

A scope is one of:

- root composition;
- direct interior of a `GroupOperator`;
- direct interior of a nested `GroupOperator`.

Example:

```text
root scope
├─ Background
├─ Merge_A
├─ Group_A
│  ├─ Merge_A1
│  ├─ Merge_A2
│  └─ Group_B
│     ├─ Merge_B1
│     └─ Merge_B2
└─ MediaOut
```

Rules:

1. each scope is planned independently;
2. a child Group is treated as one semantic box/node in its parent scope;
3. the child Group interior is planned separately and recursively;
4. cross-boundary edges may be projected to the visible child Group for planning only;
5. real Fusion connections never change to match the planning projection.

This prevents the entire PSD2Fusion-style graph from collapsing into one giant global optimization problem.

## 4. Semantic roles

Before coordinates are solved, tools in each scope are classified into layout roles.

### 4.1 Backbone nodes

Nodes participating in the main path toward the scope output.

Preferred appearance:

```text
Input -> Process -> Merge -> Merge -> Output
```

The backbone is the primary horizontal rail.

### 4.2 Merge rail nodes

Consecutive Merge-like composition nodes on the backbone.

Preferred appearance:

```text
              Branch_A
                  |
                  v
Input -> Merge -> Merge -> Merge -> Output
                    ^       ^
                    |       |
                 Branch_B Branch_C
```

A Merge rail receives special spacing and branch-placement treatment.

### 4.3 Branch sources

Nodes, chains, or child Groups feeding a backbone/Merge node from outside the current backbone.

Default preference: place above the receiving node or above the horizontal interval immediately upstream of it.

### 4.4 Mask / auxiliary branches

Mask-like or secondary-control paths should not be allowed to destroy the readability of the primary Merge rail.

v1 does not require a universal lower-mask lane, but the planner should preserve room for a later policy that separates mask/auxiliary branches from image branches.

### 4.5 Child Groups

A child `GroupOperator` is both:

- a semantic node/box in the parent scope;
- a recursively planned child scope.

The parent planner must not reason directly about all grandchildren as if the Group boundary did not exist.

### 4.6 Disconnected / weakly related components

Disconnected nodes/components remain layout citizens, but they should be placed in a peripheral or auxiliary lane so they do not interrupt the primary rail.

## 5. Backbone selection

Backbone selection should be output-oriented and deterministic.

Preferred order of evidence:

1. path(s) feeding the scope's effective output / externally consumed output;
2. longest or most semantically continuous directed path toward that output;
3. Merge-heavy path preference where multiple similar candidates exist;
4. stable tie-breakers independent of small host readback offsets.

The algorithm must not rely on raw input Y as the only semantic tie-breaker. The project has already measured real-host drift caused by readback offsets influencing row ordering; semantic planning must preserve fixed-point/idempotence guarantees.

## 6. Merge-special layout policy

This is the central v1 design rule.

### 6.1 Merge rail alignment

Consecutive Merge nodes on the selected backbone should remain horizontally aligned whenever graph topology allows it.

### 6.2 Elastic horizontal spacing

Horizontal spacing is **not globally uniform**.

A Merge-to-Merge gap may widen to satisfy readability constraints.

Conceptually:

```text
gap = max(
    minimum_rail_gap,
    branch_clearance,
    child_group_clearance,
    wire_clearance,
    host_snap_clearance
)
```

The exact numeric formula is intentionally not frozen in this architecture document. It belongs in tested layout policy/configuration.

Important invariant:

`merge_spacing_x >= regular_rail_spacing_x`

when additional clearance is required.

A wider Merge interval is not a failure by itself.

### 6.3 Why widening is allowed

Wider spacing is desirable when it:

- keeps vertical branch wires visually distinct;
- prevents child Group boxes from crowding the rail;
- avoids branch labels/nodes overlapping adjacent Merge nodes;
- reduces ambiguous crossings;
- makes the left-to-right composition order easier to scan.

The planner should not compress a readable Merge rail merely to minimize total width.

## 7. Branch placement policy

Default rule for a branch feeding a backbone node:

1. place the branch root above its receiving node;
2. place upstream branch members recursively/vertically above that root when practical;
3. reserve enough horizontal clearance so branch wires do not collapse into adjacent rail wires;
4. keep child Group branch boxes readable as boxes, not as invisible flattened internals.

When multiple branches feed nearby Merge nodes, the spacing solver may widen the Merge rail rather than forcing all branches into the same narrow vertical corridor.

## 8. Group-local recursion

The same semantic policy is applied inside Groups.

For each Group scope:

1. identify the Group-local backbone;
2. detect its Merge rail(s);
3. place branch sources relative to that local rail;
4. treat nested child Groups as semantic boxes;
5. recursively solve each child Group interior;
6. compose child boxes with the parent scope;
7. normalize to host grid/readback constraints;
8. verify fixed-point stability.

This means the project should visually read as a hierarchy of small understandable graphs, rather than one giant globally packed graph.

## 9. Scope box model

A planner needs a logical bounding box for every child Group.

Before runtime visual Group expansion/fit-to-contents is solved, the box may come from:

- current measurable Group geometry when available;
- conservative logical bounds derived from the child layout;
- an explicitly documented placeholder size used only for planning.

After P3B/P4 visual expansion and fit-to-contents become host-proven, the actual runtime Group box should replace conservative estimates.

Do not invent host `GroupInfo.Size/Scale/Offset` semantics offline.

## 10. Spacing classes

Semantic layout should expose named spacing classes rather than one global X/Y spacing pair.

Suggested policy surface:

```text
regular_rail_spacing_x
merge_rail_spacing_x
branch_spacing_y
branch_cluster_gap_x
component_gap_y
group_gap_x
group_gap_y
group_padding_x
group_padding_y
```

The first implementation can map multiple classes to existing values, but the policy names should remain semantically distinct so later tuning does not require rewriting the planner.

### Hard vs soft spacing

Hard:

- no overlap after host quantization/readback;
- sufficient Group-to-node clearance;
- deterministic minimum gap.

Soft:

- compact total graph width;
- visually even spacing;
- branch centering.

When hard readability constraints conflict with soft compactness, readability wins.

## 11. Proposed pure-core architecture

Semantic planning should remain host-independent.

Suggested conceptual layers:

```text
Fusion host snapshot
        |
        v
SemanticGraphSnapshot
        |
        +--> ScopeBuilder
        +--> RoleClassifier
        +--> BackboneSelector
        +--> MergeRailDetector
        +--> BranchPlanner
        +--> SpacingSolver
        +--> RecursiveScopeComposer
        |
        v
PlannedLayout
        |
        v
Fusion host adapter
(snapshot/write/readback/rollback)
```

### `SemanticGraphSnapshot`

Contains only stable planning facts:

- stable/hierarchical tool identity;
- tool type / RegID;
- parent Group identity;
- directed edges with input/output identity where available;
- current quantized/logical positions;
- optional semantic hints derived from input IDs/names.

### `ScopeBuilder`

Builds root and direct-child Group scopes without flattening hierarchy.

### `RoleClassifier`

Classifies backbone candidates, Merge-like nodes, branch nodes, masks/auxiliary nodes, child Groups, and disconnected components.

### `BackboneSelector`

Selects a deterministic output-oriented main rail for one scope.

### `MergeRailDetector`

Finds maximal Merge-heavy runs on the backbone.

### `BranchPlanner`

Assigns branch ownership and preferred lane/anchor.

### `SpacingSolver`

Applies semantic spacing constraints and allows elastic Merge widening.

### `RecursiveScopeComposer`

Places child Group boxes within the parent scope while preserving local layouts.

### Host adapter

Owns only Fusion-specific mutation safety, host grid snapping, readback tolerance, Undo, and rollback. Semantic layout logic must not be hidden in host calls.

## 12. Determinism and fixed-point requirement

The current project has measured host coordinate readback offsets. Therefore semantic layout is accepted only when it converges to a stable fixed point under the current host quantization policy.

Required behavior:

- planning is deterministic from the normalized snapshot;
- a second identical execution produces no movement;
- tiny host readback offsets do not reorder semantically equivalent rows unpredictably;
- host snap/tolerance handling remains adapter-owned and measurable.

## 13. Command/product strategy

Do not replace the current host-verified generic `Tidy Nested` behavior immediately.

Recommended rollout:

1. keep `Tidy Graph` / `Tidy Nested` as proven baseline commands;
2. implement semantic planning behind a distinct policy/entrypoint, tentatively `Tidy Semantic` / `tidy_semantic_comp(...)`;
3. validate semantic fixtures offline;
4. host-canary on small representative Merge/Group graphs;
5. prove second-run stability and invariants;
6. only after sufficient evidence decide whether semantic policy becomes the default `Tidy` behavior.

This protects the current host-verified baseline while allowing aggressive layout-quality work.

## 14. Implementation stages

### S0 — semantic model / fixtures

- build pure semantic snapshot types;
- add representative graph fixtures;
- no host writes.

### S1 — backbone + Merge rail

- deterministic backbone selection;
- Merge-run detection;
- basic horizontal rail.

### S2 — elastic Merge spacing

- branch-clearance constraints;
- explicit Merge widening;
- deterministic spacing policy.

### S3 — Group-local recursion

- apply the same semantic policy to every Group scope;
- compose child Group logical boxes in parents.

### S4 — host canary

- small Merge chain;
- Merge chain with branch Groups;
- nested Group with internal Merge chain;
- Undo/readback/second-run stability.

### S5 — large-graph stress

- use `docs/EVIDENCE_PROTOCOL.md`;
- transport-fitting chunked evidence;
- compare structural hashes and position stability.

### S6 — visual Group integration

After real runtime Group expansion / fit-to-contents is solved, replace logical Group box estimates with measured visible boxes.

## 15. Acceptance overview

Detailed acceptance lives in `docs/SEMANTIC_LAYOUT_ACCEPTANCE.md`.

At minimum:

- all graph invariants preserved;
- main rail reads left-to-right;
- Merge rail is easy to scan;
- branch provenance remains understandable;
- Group interiors use the same local rules recursively;
- wider Merge spacing is explicitly allowed;
- no overlaps after host quantization;
- second execution is position-identical / zero-move;
- exact screenshot-coordinate matching is not required.

## 16. Non-goals

v1 does not require:

- globally minimal graph width/height;
- exact reproduction of the reference screenshots;
- one universal spacing value;
- solving runtime visual Group expansion through undocumented guesses;
- Color-page XY layout;
- automatic rewiring;
- background daemon/watchers;
- shortcut replacement.

## 17. Design summary

The intended architecture is best described as:

> **hierarchical, Group-local semantic layout with a horizontal composition backbone, Merge-aware elastic spacing, vertical branch placement, recursive child-scope planning, and deterministic host-safe convergence.**

The visual goal is not a perfectly compact graph. The goal is a graph whose processing structure can be understood quickly even when PSD2Fusion produces deep Group nesting and large Merge-heavy compositions.
