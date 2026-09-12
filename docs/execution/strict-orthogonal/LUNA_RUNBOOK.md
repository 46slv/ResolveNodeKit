# Luna Max orchestration — Direct Guarded Resolve runbook

Revision: DIRECT-GUARDED-RESET-20260911-1
Mission: RNK-STRICT-ORTHOGONAL / 46slv/ResolveNodeKit / PR #5

## 1. Operating model

RNK product development no longer uses a dedicated/external Resolve Operator as a mandatory route.

Default:

```text
Luna Max Coordinator / Product Worker
  -> direct current Resolve capability
  -> minimal mechanical Host Guard
  -> DaVinci Resolve
```

The historical external Operator, D/S/H matrix, Transactional HostSession and HostLocalSemanticReceipt remain research/legacy assets. They are not prerequisites for SO/G gates and must not be repaired merely to continue RNK.

## 2. Goal and completion boundary

Keep the existing product goal and G01–G14 acceptance unchanged: strict horizontal/vertical layout, actual orthogonal wires, safe preserve and flatten-all, processing preservation, exact Undo/rollback, run2 stability, installed UI flow, 1100+ qualification, performance, recovery, cleanup and fresh independent final verification.

Do not reinterpret `BLOCKED` historical Operator evidence as product impossibility. Do not mark a required gate PASS from offline mocks or worker narration.

## 3. Opening protocol

At the start of a continuation:

1. inspect live Git/common-dir/worktrees/HEAD/dirty and remote PR #5;
2. preserve unknown dirty work and active ownership; do not reset blindly;
3. read `AGENTS.md`, `docs/CURRENT_STATE.md`, strict `README.md`, `PLAN.md`, `acceptance.json` and relevant latest product checkpoint;
4. verify source/install/publication identities;
5. inspect current Resolve version and the direct capabilities actually visible to the current Luna task;
6. choose the highest-value ready product gate.

Historical SHAs, process IDs, project IDs, model sessions and tool counts are locators only.

## 4. Direct capability reset

Parent/direct Resolve capability visibility is allowed and expected when the task needs Resolve.

If old configuration intentionally disabled Resolve MCP/tool access to enforce Operator isolation, change the local runtime/profile/config so the active Luna Max Product Worker can use the required Resolve surface directly. Preserve rollback of the config change, but do not preserve `parent visibility = 0` as an invariant.

Control-surface selection is pragmatic:

1. inspect the current available capability;
2. prefer the simplest documented/qualified path that performs the exact task;
3. use Blackmagic native MCP where it exposes the needed operation;
4. use current Python/Lua scripting or GUI when they are the shorter correct path;
5. do not build another transport/agent bridge merely to keep a historical architecture alive.

Host-local Comp/FlowView/Undo/UI objects may remain local live objects in the current execution context. They do not need a detached semantic receipt just to permit development.

## 5. Host Guard

Apply safety proportional to the operation. For live mutation or possible concurrent writers, retain:

- one shared integration/state writer;
- one live Resolve writer or equivalent user-wide serialization;
- exact target identity before valuable writes;
- owned/disposable scratch targets for experiments;
- no blind retry after an ambiguous mutation/timeout;
- reversible mutation, Undo, or discardable fixture where practical;
- before/after readback;
- cleanup/recovery and final state check;
- no valuable project save unless explicitly authorized for that task.

Do not turn these invariants back into a dedicated-agent requirement.

Read-only inventory does not need artificial transaction infrastructure beyond what is necessary to avoid racing a concurrent mutable operation.

## 6. Minimum useful host smoke

Before more infrastructure work, establish the direct product-worker path with one bounded real-host smoke.

Use an owned disposable or otherwise safe current Fusion context and demonstrate, as applicable:

```text
bind target
 -> observe comp identity/current context
 -> read relevant FlowView/position state
 -> invoke actual RNK/product seam or one tiny owned reversible mutation
 -> read back
 -> Undo/restore or discard owned fixture
 -> verify cleanup
```

This smoke is not final G01–G14 qualification. Its purpose is to prove that the product worker can actually operate the host and resume product development.

If it succeeds, move immediately to the next product gate. Do not respond by creating a broader generic execution framework.

## 7. What not to retry

The following are historical research paths and are closed for product work unless explicitly studying the Operator architecture:

- compatibility WP1 host-local semantic receipt route;
- native WP1 semantic receipt route;
- constructor-local opaque-table receipt route;
- matched D/S/H qualification solely to choose an agent topology;
- parent-isolated external-Operator routing as a prerequisite to host access.

Their evidence remains useful for research. Their failure fingerprints do not need to be defeated before RNK continues.

## 8. Product execution route

Use the existing task graph in `PLAN.md`.

Recommended continuation priority after direct-host smoke:

| Stage | Outcome |
|---|---|
| R2 preserve | SO-30 view realization + SO-50 installed UI + SO-60 small preserve E2E |
| R3 flatten | SO-40 actual flatten + SO-61 processing-preserving small E2E |
| R4 large | SO-70 preserve and SO-71 flatten at real/1100+ scale, including run2/performance |
| R5 finish | SO-80 recovery/fault cases + SO-90 exact-candidate fresh verifier and remote readback |

G01 already has qualified evidence; carry it unless product changes invalidate it. G02/G03 remain blocked until direct product-host evidence closes them. G04–G14 remain required and pending until their actual criteria pass.

A flatten blocker must not stop an independent preserve/UI/recovery task. A view blocker must not trigger another orchestration redesign if another product-level route can be tested.

## 9. Worker / verifier topology

Do not spawn agents by default.

- Coordinator may implement directly when the scope is coherent.
- Use one bounded Worker only when scope separation clearly saves time or protects ownership.
- Use parallel Workers only for genuinely independent write scopes.
- Use a fresh independent Verifier for final/high-risk acceptance where independence adds real evidence.
- The old Resolve Operator is not a Worker default; use only for explicit research/comparison or a task-specific demonstrated advantage.

The fastest correct topology is usually one capable Product Worker plus deterministic tests and final independent verification.

## 10. Failure handling

Classify the smallest failing layer: product logic, host API, runtime, current context, UI, transport, install/provenance, restore, or evidence.

After a failure:

- first reconcile actual state;
- retry only when the next attempt changes hypothesis or expected evidence;
- do not create a new agent/process boundary just because the direct attempt failed once;
- if a public API is missing, consider a documented host-local script or GUI route before infrastructure work;
- keep blocked gates explicit and continue independent ready product work.

Complexity-inversion trigger:

> If the proposed safety/proof/orchestration repair is harder than the underlying guarded Resolve action, stop and simplify the boundary.

## 11. Evidence discipline

Keep proof surfaces separate:

- source/unit/offline result;
- installed package provenance;
- direct controller execution;
- real Resolve host state;
- actual widget/user flow;
- FlowView/displayed-wire observation;
- processing state/render invariance;
- Undo/restore;
- large-scale/performance;
- fresh independent final verification.

For every gate, record only the evidence its criterion needs. Do not force all host observations through one universal receipt schema.

Source candidate, publication/docs HEAD, installed candidate and evidence candidate must remain distinguishable.

## 12. Authority

Authorized without repeated confirmation inside this project scope:

- task-branch code/tests/docs changes;
- backup-backed local install/update;
- commits/pushes/Draft PR #5 updates;
- direct Resolve native MCP/scripting/GUI operation;
- Resolve launch/quit/restart when needed;
- owned scratch/disposable project/timeline/comp creation and cleanup;
- reversible validation mutations and Undo/restore.

Not authorized by this runbook:

- valuable project save unless separately required/authorized;
- main merge/release;
- force-push shared history;
- credential bypass/change;
- unrelated deletion/process kill/OS destructive action;
- PC reboot;
- global shortcut mutation;
- permanent service/startup installation.

## 13. Closeout

After meaningful product progress:

1. run focused validation and required canonical checks;
2. perform gate-specific host readback where applicable;
3. run the Mandatory Learning Gate;
4. update durable checkpoint/state without rewriting history;
5. commit/push authorized branch changes;
6. fresh-read remote PR/head and installed provenance when relevant;
7. continue to the next ready product task instead of stopping after infrastructure success.

Completion means the existing product acceptance is met. A successfully configured direct Resolve path is only an unlock, not product completion.
