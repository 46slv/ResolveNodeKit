# ResolveNodeKit Product Direction Brief

Status: `PRODUCT_DIRECTION_RESET`

Effective: 2026-09-20 JST

Current release owner: [`docs/execution/v1-arrange/`](execution/v1-arrange/)

Preserved v2/research owner: [`docs/execution/strict-orthogonal/`](execution/strict-orthogonal/)

## Decision

ResolveNodeKit v1 is a practical automatic node-arrangement product:

> Arrange a Fusion graph quickly and reliably without damaging its processing
> structure.

v1 preserves existing `GroupOperator`s. It does not automatically Ungroup or
Flatten All.

The formal v1 workflow for users who want to work on a flat graph is:

```text
Arrange -> optional Resolve native GUI manual Ungroup -> Re-Arrange
```

Manual Ungroup is an intentional product boundary, not a temporary workaround.
Resolve remains the authority for the structural edit; RNK returns to its
preserve-mode Arrange path after that edit.

## v1 product scope

The v1 release candidate must provide and verify:

- flat, Group-preserving and nested-Group Arrange;
- representative fan-out, multi-edge, Mask and branch topology;
- processing topology, tool identity and Group parent/membership preservation;
- zero endpoint loss;
- exact Undo/rollback, stable second run and safe recovery;
- installed Run / Cancel / busy / result behavior;
- real-project duplicate and a practical `>=1100` non-Group Arrange fixture;
- acceptable performance, cleanup, and source/install/package identity;
- a fresh independent verifier.

Logical or real-screen evidence is required when it is needed to show that the
product is readable and not visually broken. A machine-readable rectangle/grid
surface that the measured Resolve host does not publish is not itself a v1
release blocker. An actually broken visual result is still a failure.

## v1 UI boundary

The normal installed v1 UI presents the whole-composition Arrange confirmation
and does not expose automatic Flatten / `UngroupFirst`. If a future prototype
needs to remain reachable for research, it must be disabled, explicitly marked
v2/future, or isolated from the normal Arrange surface. The current
text-only confirmation already maps to `include_unselected=True, ungroup=False`.

## v2 backlog: Automatic Flatten

The following remain intentionally deferred:

- Automatic Ungroup;
- `UngroupFirst` as a normal product option;
- Flatten All;
- installed RNK dispatch to an identity-preserving native Ungroup action;
- large automatic-flatten qualification;
- flatten-specific processing/render preservation;
- automatic flatten rollback as a single product workflow.

The old strict G01–G14 acceptance, strict planner/apply code, flatten adapter,
checkpoints and host findings are not deleted or rewritten into v1 PASS. They
remain the v2 / strict research contract. Their `BLOCKED_*`, `PENDING` and
`NOT_COLLECTED` states remain evidence of the research lane, not v1 blockers.

## Why the split exists

The preserve path has independent, useful host evidence at small, nested,
real-project and large scale. The measured host does not expose a callable
identity-preserving Ungroup primitive, while the strict large-graph geometry
surface is also incomplete. Keeping these capabilities coupled would make a
useful Arrange product wait on a separate structural operation and would invite
unsupported UI/API guesses. The split keeps the v1 promise narrow and testable.

## v1 done and v2 resume trigger

`V1_RELEASE_CANDIDATE` is allowed only after the v1 acceptance file is PASS or
explicitly scoped, the carried evidence has been identity-checked, any genuine
missing v1 gate is run on disposable/duplicate state, and a fresh verifier
accepts the exact candidate. It is not a main merge or an actual release.

Resume v2 Automatic Flatten only when all of the following are available:

1. a measured host-native identity-preserving Ungroup primitive or a documented
   equivalent bridge;
2. complete pre/post processing, endpoint, identity, parent and render
   readback on a disposable nested fixture;
3. exact rollback/Undo semantics and a bounded large-scale route;
4. a separately owned v2 acceptance update and fresh verifier.

Do not resume v2 merely because a generic `DoAction`/`QueueAction` exists or a
screen label is visible. Do not weaken the v1 acceptance to absorb v2 gaps.

## Execution authority

Normal Resolve work remains:

```text
Luna Max Product Worker -> direct Resolve MCP/scripting/GUI
  -> minimal mechanical Host Guard -> Resolve
```

Do not restore the retired Operator/WP1/HostSession topology for ordinary v1
work. Keep exact target binding, owned/disposable state, no-blind-retry,
readback, rollback/recovery and cleanup.
