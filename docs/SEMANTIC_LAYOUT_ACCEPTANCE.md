# Fusion semantic layout acceptance — v1

This document defines what counts as a successful implementation of `docs/SEMANTIC_LAYOUT.md`.

It separates **hard correctness requirements** from **soft visual preferences** so the project does not accidentally reject a readable layout merely because spacing is wider than average.

## 1. Hard invariants

Every semantic-layout command must preserve:

- tool count, unless the command explicitly owns tool creation/removal (semantic tidy does not);
- `GroupOperator` membership / parent chain;
- every connection and connected input/output identity available to the host;
- processing parameters;
- keyframes/expressions;
- media / grade / render state;
- visual Group expanded/collapsed state unless the explicit command owns that state;
- current project/timeline/comp target identity during the write batch.

A mismatch is a hard failure and triggers rollback/stop under existing host safety rules.

## 2. Hard layout properties

### 2.1 Deterministic convergence

For the same normalized graph snapshot and policy:

- planning output is deterministic;
- host run 2 must be zero-move / position-signature identical;
- measured host coordinate offsets must not cause row-order oscillation;
- bounded fixed-point planning must fail closed if convergence cannot be reached.

### 2.2 No unintended overlap

Within each managed layout scope, distinct visible nodes/boxes must not overlap after current host quantization/readback, except where a future explicit command contract intentionally permits it.

Overlap is evaluated per local scope, not by flattening all nested Group descendants into root coordinates.

### 2.3 Monotonic backbone

The selected main backbone should be left-to-right monotonic in X unless a measured host constraint makes that impossible.

For every adjacent backbone pair `(A -> B)`:

`x(B) > x(A)`

under the normalized host grid policy.

### 2.4 Merge rail legibility

For each detected Merge run:

- consecutive Merge nodes remain on a common horizontal rail within configured tolerance;
- downstream order is visually monotonic;
- branch wires do not require nodes to be packed so tightly that branch provenance becomes ambiguous.

### 2.5 Recursive scope correctness

Every nested Group scope is laid out independently using the same policy family.

The parent layout treats each child Group as one box/node. It must not flatten grandchildren into the parent layout calculation.

## 3. Explicitly allowed behavior

The following are **not defects by themselves**:

- Merge-to-Merge gaps wider than ordinary rail spacing;
- different horizontal gaps along the same graph;
- a Group being wider than the minimum mathematical bound if padding/readability requires it;
- the final composition occupying more total width than the generic tidy layout;
- branch nodes not being perfectly centered if a nearby Group/branch requires clearance.

Reference 02 specifically establishes that a wider Merge side can be the preferred result.

## 4. Soft visual preferences

These should be optimized after hard constraints:

1. reduce unnecessary wire crossings;
2. keep branch roots close to their receiving Merge;
3. align branch columns when doing so does not create congestion;
4. minimize unused Group interior area;
5. minimize total scope width/height;
6. prefer visually regular spacing where semantic clearance does not require expansion.

Soft preferences may trade off against each other. They must never override hard invariants or deterministic convergence.

## 5. Reference images

- [`references/semantic-layout-reference-01.svg`](references/semantic-layout-reference-01.svg)
- [`references/semantic-layout-reference-02.svg`](references/semantic-layout-reference-02.svg)

The images are normative for **visual principles**, not exact coordinates.

### Normative principles visible in the references

- root flow is readable as a horizontal backbone;
- Group frames remain visible and semantically meaningful;
- nested Group contents are arranged as local graphs;
- Merge chains are easy to scan horizontally;
- branch sources sit above receiving Merge nodes where practical;
- Group-to-backbone relationships remain traceable;
- wider Merge spacing is acceptable.

### Non-normative details

Do not test against:

- exact pixel coordinates;
- exact frame dimensions;
- exact zoom level;
- exact node names;
- exact colors/theme;
- exact total graph width.

## 6. Required fixture matrix

The pure-core test suite should eventually include at least the following semantic fixtures.

### F1 — simple Merge rail

```text
BG -> M1 -> M2 -> M3 -> Out
      ^     ^     ^
      A     B     C
```

Acceptance:

- `M1/M2/M3` horizontal;
- A/B/C above corresponding Merge targets;
- downstream X monotonic;
- no overlap;
- second plan identical.

### F2 — Merge rail requiring widening

A/B/C branches are themselves small chains or logical boxes wide enough to conflict under default spacing.

Acceptance:

- planner increases one or more Merge gaps;
- no requirement that all Merge gaps remain equal;
- branch provenance remains clear;
- no overlap/crossing regression caused by aggressive compaction.

### F3 — child Group feeding Merge rail

```text
       [Group A]
           |
BG -> M1 -> M2 -> Out
```

Acceptance:

- Group A treated as one box in parent scope;
- Group A interior solved independently;
- parent rail spacing may widen to accommodate Group A.

### F4 — nested Group with internal Merge rail

```text
Group A
  ├─ Input -> M1 -> M2
  ├─ Group B -> M1
  └─ Branch  -> M2
```

Acceptance:

- Group A local rail readable;
- Group B treated as local child box;
- Group B interior independently stable;
- membership unchanged.

### F5 — mask / auxiliary branch

Representative Merge or effect chain with an EffectMask-like input.

Acceptance:

- primary image rail remains readable;
- auxiliary branch does not force rail collapse;
- future lower-lane policy can be added without changing graph identity model.

### F6 — disconnected component

Acceptance:

- disconnected component placed in a peripheral lane/component region;
- it does not overlap/interleave the primary rail;
- result deterministic.

### F7 — multiple child Groups along root backbone

Acceptance:

- child Group boxes remain distinguishable;
- root backbone remains traceable;
- Group spacing may widen asymmetrically.

### F8 — 3+ nesting levels

Acceptance:

- recursion terminates;
- each scope produces a stable local layout;
- hierarchical identity remains unique or fails closed if ambiguity cannot be resolved.

### F9 — host offset fixed-point regression

Encode measured readback-offset/tie behavior that previously caused `Tidy Nested` to settle only on run 3.

Acceptance:

- semantic planner converges before one host write;
- normalized second planning pass is identical.

### F10 — large synthetic semantic fixture

Hundreds/thousands of tools generated offline with nested Groups and Merge-heavy rails.

Acceptance:

- planner remains iterative/bounded;
- no recursion-limit dependence for tool-chain depth;
- deterministic output hash;
- no unbounded spacing explosion.

## 7. Quantitative diagnostics

The semantic planner should expose diagnostics useful for tests and host evidence.

Recommended fields:

```text
scope_count
backbone_count
merge_rail_count
node_count
logical_group_box_count
max_group_depth
overlap_count
backbone_order_violation_count
branch_lane_violation_count
crossing_estimate_before
crossing_estimate_after
expanded_gap_count
max_gap_x
total_width
total_height
fixed_point_iterations
```

These are diagnostics, not all release gates.

## 8. Spacing diagnostics

A widened gap should be explainable.

Recommended reason tags:

```text
DEFAULT
BRANCH_CLEARANCE
GROUP_CLEARANCE
WIRE_CLEARANCE
COMPONENT_CLEARANCE
HOST_GRID_CLEARANCE
```

This makes a wide layout debuggable and prevents arbitrary expansion from being mistaken for semantic spacing.

## 9. Host canary acceptance

Before semantic policy is promoted beyond experimental status, validate on disposable/duplicate Fusion comps.

Minimum canaries:

1. simple Merge rail with 2–3 branches;
2. nested Group containing a Merge rail;
3. child Group feeding a root Merge rail;
4. representative mask branch;
5. repeat-run idempotence;
6. Undo restore;
7. structural/processing invariance.

Use the existing OpenCode/Muse/Resolve MCP evidence contract.

## 10. Large-host acceptance

For PSD2Fusion-scale graphs, use `docs/EVIDENCE_PROTOCOL.md`.

Do not require one whole-graph MCP payload.

Required proof:

- stable hierarchical identity or explicit ambiguity failure;
- unchanged membership/connection hashes;
- intended first-run position change;
- identical second-run position hash;
- bounded runtime;
- no unresolved overlap in managed scopes;
- no repeated known transport timeout path.

## 11. Promotion policy

Semantic layout should initially ship behind a distinct command/policy.

Promotion to default generic Tidy behavior requires:

- all hard invariants green;
- fixture matrix green for implemented roles;
- representative host canaries green;
- second-run zero-move;
- no regression in current Flat Tidy / Tidy Nested safety guarantees;
- visual review showing the semantic policy is consistently preferable, not merely different.

Until then, current host-verified generic Tidy remains the baseline.
