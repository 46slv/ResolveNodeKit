# ResolveNodeKit current continuation

Updated: 2026-09-11 JST
Status: `CHECKPOINTED_WITH_TECHNICAL_GAP` / product not complete

Live Git/PR/installed/runtime evidence always outranks this locator.

## Active goal

`RNK-STRICT-ORTHOGONAL`

Complete the existing strict horizontal/vertical whole-comp layout, actual orthogonal displayed wires, safe preserve and flatten-all, installed UI flow, processing preservation, exact Undo/rollback, run2 stability, real/1100+ qualification, performance, recovery, cleanup and final independent verification.

Required product gates remain G01–G14. Do not lower or delete a gate to claim completion.

## Current execution policy — Direct Guarded reset

The dedicated/external Resolve Operator is no longer part of the RNK product critical path. It is retained only as research/legacy evidence.

Default execution:

```text
Luna Max Product Worker / Coordinator
  -> direct current Resolve capability
  -> minimal mechanical Host Guard
  -> DaVinci Resolve
```

The old Operator-isolation invariant `parent Resolve visibility = 0` is retired. If current local configuration still disables direct Resolve capability solely to preserve that architecture, repair/enable the direct Product Worker route with rollback available.

The historical D/S/H matrix and WP1 HostLocalSemanticReceipt experiments are not product dependencies. Do not replay them for normal RNK progress.

## Safety retained

For mutable/concurrent live-host work preserve the useful mechanical invariants without requiring another agent/process:

- one integration/state writer;
- one live Resolve writer or equivalent user-wide serialization;
- exact target identity before valuable writes;
- owned/disposable scratch state;
- no blind retry after ambiguous mutation;
- reversible mutation / Undo or discardable fixture where practical;
- before/after readback;
- cleanup/recovery;
- no valuable project save unless separately authorized.

## Product status

Current gate status carried from the latest verified checkpoint:

- G01: `PASS`
- G02: `BLOCKED_TECHNICAL`
- G03: `BLOCKED_TECHNICAL`
- G04–G14: `PENDING`

Latest pre-reset product/operator verification reported:

- RNK canonical suite: `174/174 PASS`
- compileall: PASS
- diff-check: PASS
- strict contract checker: PASS
- Operator research suite: `30/30 PASS` for `HostLocalSemanticReceipt`
- graph/layout/Undo/save writes in the final WP1 transport probes: `0`
- final lease: `FREE`

These facts do not equal product completion.

## Historical WP1 boundary — archived research

Checkpoint:
`docs/checkpoints/2026-09-11-wp1-host-local-semantic-receipt.json`

Historical result:

- compatibility route: `BLOCKED_RUNTIME_NO_PROGRESS`
- native route: API discovery reached `LoadComp`, `GetPosTable`, Undo/Close surfaces but timed out before semantic receipt: `BLOCKED_SEMANTIC_RECEIPT_TIMEOUT`
- both routes performed no fixture/product mutation/save and ended lease `FREE`

Decision: preserve this as evidence that the external proof/transport boundary became more expensive than ordinary guarded host operation. It no longer blocks SO/G product work.

## Current product plan

Canonical execution docs:

- `docs/execution/strict-orthogonal/README.md`
- `docs/execution/strict-orthogonal/PLAN.md`
- `docs/execution/strict-orthogonal/LUNA_RUNBOOK.md`
- `docs/execution/strict-orthogonal/acceptance.json`
- `docs/design/strict-orthogonal/DESIGN.md`
- `docs/design/strict-orthogonal/SOURCES.md`

The plan no longer contains WP1/topology qualification as a dependency.

## Exact next action

1. fresh-read PR #5/source/install/current Resolve runtime;
2. confirm the active Luna Max Product Worker has direct Resolve MCP/scripting/GUI capability; repair old isolation config if necessary;
3. run one minimum useful direct-host smoke on owned/disposable safe state: bind Fusion context, observe relevant FlowView/position state, perform the smallest useful RNK path or tiny reversible owned mutation, read back, Undo/restore and clean up;
4. if successful, immediately continue product gates—prefer SO-30/SO-50/SO-60 preserve and SO-40 flatten where ready;
5. do not respond to success by building another generic execution framework;
6. if one product gate blocks, continue another authorized independent ready gate.

## Stop boundary

Do not stop merely because a historical Operator/WP1 route is blocked.

Stop only for a genuine authority/input boundary, unrecoverable valuable-state risk, no remaining authorized ready product work, or actual completion of the existing acceptance contract.

## Authority

Authorized: task-branch code/tests/docs, backup-backed install, commit/push/Draft PR updates, direct Resolve MCP/scripting/GUI, Resolve launch/quit/restart, owned scratch/disposable fixtures and reversible validation mutations.

Not authorized by this state file: valuable project save, main merge/release, force-push shared history, credential changes, unrelated destructive OS/process work, PC reboot, global shortcut mutation or permanent service/startup installation.

## Historical evidence

Older detailed execution history remains in Git history and `docs/checkpoints/`. Do not reconstruct the active plan from old narrative sections; use them only as evidence for the exact candidate/runtime they measured.
