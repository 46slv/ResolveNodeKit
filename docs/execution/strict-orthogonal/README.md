# Strict Orthogonal Arrange — Luna Max continuation entry

Revision: DIRECT-GUARDED-RESET-20260911-1
Mission: RNK-STRICT-ORTHOGONAL / 46slv/ResolveNodeKit / PR #5

## Current execution decision — 2026-09-11

The dedicated/external Resolve Operator is retired from the RNK product critical path and retained only as research/legacy evidence.

RNK now uses the simplest operational shape:

```text
Luna Max Product Worker / Coordinator
  -> direct Resolve capability
  -> mechanical Host Guard where required
  -> DaVinci Resolve
```

Do not require external Operator routing, D/S/H qualification, HostLocalSemanticReceipt qualification, raw-handle serialization, or matched topology matrices before normal product work.

The previous WP1 compatibility/native/host-local receipt experiments remain valid historical evidence of boundary cost, but **WP1 is no longer a product dependency**. Do not replay those routes unless the task is explicitly research about that architecture.

## Core rule

`Requirements first. Topology second. Delegation must earn itself.`

Additional stop rule:

> If safety/proof/orchestration infrastructure becomes harder than safely performing the target Resolve operation, question or remove that boundary before adding more infrastructure.

For this project, direct guarded Resolve operation is the default because strict layout work needs current host/Fusion/FlowView/Undo/UI context and the user has explicitly authorized normal Resolve operation for development and validation.

## Host Guard — keep the useful part

Direct does not mean unguarded. For mutable or concurrent live-host work, preserve the smallest applicable safeguards:

- one integration/state writer;
- one live Resolve writer / user-wide serialization when concurrent access is possible;
- fresh target identity before valuable writes;
- owned/disposable scratch state for probes;
- no blind retry after ambiguous mutation;
- reversible mutation / Undo or discardable fixture where practical;
- before/after readback and cleanup/recovery;
- no valuable project save unless separately authorized.

These safeguards do not require a dedicated agent/process boundary.

## Product Goal / Done

Continue the existing strict-orthogonal mission unchanged:

- reference-guided whole-comp horizontal/vertical layout;
- actual orthogonal displayed wires;
- preserve mode keeps Groups and processing semantics;
- flatten-all removes all Groups while preserving non-Group identity/processing semantics;
- exact Undo/rollback where required;
- second run stable (`moved=0`);
- installed UI Run/Cancel/busy/result user flow;
- real-scale and >=1100 original non-Group qualification;
- performance, recovery, cleanup and final independent verification;
- all required G01–G14 PASS on the final candidate before product completion.

Do not lower an acceptance requirement merely because a host/API path is difficult.

## Start / source of truth

At every continuation:

1. inspect live Git/worktree/remote PR #5 and preserve unknown dirty work;
2. read `AGENTS.md` and `docs/CURRENT_STATE.md` as state/evidence locators;
3. read this file, `PLAN.md`, `LUNA_RUNBOOK.md`, `acceptance.json`, DESIGN/SOURCES as needed;
4. verify current installed candidate and current Resolve/runtime capability instead of trusting historical SHAs/tool counts;
5. continue from the highest-value ready product task, not from an obsolete Operator/WP1 dependency.

Current user instruction and live repo/runtime evidence outrank historical checkpoints.

## Direct Resolve operation

The current Luna/Product Worker may directly use the available Resolve control surface needed by the task, including Blackmagic native MCP, current scripting, or GUI operation.

- Parent/direct Resolve capability visibility is no longer required to stay zero.
- If direct capability is disabled by an old Operator-isolation config, repair/enable the direct product-worker route instead of launching a dedicated Operator merely to preserve the old topology.
- Prefer the simplest current qualified surface for the exact semantic operation; do not infer parity from tool count or marketing.
- Host-local objects such as Comp/FlowView/Undo handles may remain ordinary in-process/live objects. Do not build serialization infrastructure just to move them across a boundary that the product no longer needs.
- A small host-local helper/script is fine when it is the shortest implementation path; it is not a new agent authority domain.

## Execution order

Use the existing product task graph, but remove WP1/topology qualification from its dependencies.

Near-term priority:

1. restore/confirm a direct Resolve-capable Luna Max product-worker path;
2. run one minimum useful disposable/current-safe host smoke that proves the worker can bind the intended Fusion context, read layout/view state, perform a tiny reversible owned mutation when required, Undo/restore, and read back;
3. if that works, immediately return to product gates rather than expanding infrastructure;
4. progress SO-30 / SO-50 / SO-60 preserve first where ready;
5. progress SO-40 / SO-61 flatten independently as its capability becomes available;
6. progress SO-70/71 large qualification, SO-80 recovery and SO-90 final independent verification;
7. a local blocker does not stop independent ready product work.

Use minimum useful smoke early. Add stronger evidence machinery only for an observed failure class or a final acceptance gate that actually needs it.

## Historical Operator/WP1 evidence

Keep the existing checkpoints, Operator branches, HostSession code, semantic receipt code and qualification results as research evidence. They may inform future tooling research, concurrency guards or comparative experiments.

They are not current RNK execution authority and must not be used to block product work.

## Short continuation prompt

```text
Goal:
Continue ResolveNodeKit PR #5 to the existing G01–G14 strict-orthogonal completion target.

Done:
Final candidate satisfies the existing acceptance contract with real Resolve evidence, installed user flow, large-scale qualification, recovery/cleanup and fresh independent verification.

Constraints:
Read live repo/runtime first. Dedicated Resolve Operator and WP1 semantic-receipt qualification are research-only and are not product dependencies. Default to direct guarded Resolve operation. Preserve processing semantics, required gates, no-blind-retry and no valuable project save.

Authority:
Use Luna Max. Direct Resolve MCP/scripting/GUI, Resolve launch/quit/restart, owned disposable fixtures and reversible validation mutations are authorized. Task-branch code/tests/docs/install/commit/push/PR updates are authorized. No main merge/release/force-push/credential change.

Starting point:
Read AGENTS.md, CURRENT_STATE.md, this README, PLAN.md, LUNA_RUNBOOK.md and acceptance.json; fresh-read PR #5 and current installed/runtime state. Do not replay closed Operator/WP1 probes.

Evidence:
Prefer minimum useful real-host smoke, then gate-specific readback. Keep candidate/source/install identity explicit. Use a fresh verifier for final/high-risk gates. If one route blocks, change the product approach or continue another ready gate rather than rebuilding orchestration infrastructure.
```
