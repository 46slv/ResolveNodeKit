# Semantic Arrange v1 — continuation runbook

Status: READY
Updated: 2026-09-08 JST
Plan: `docs/execution/semantic-arrange-v1/PLAN.md`
Runtime state: `docs/CURRENT_STATE.md`

## 1. Authority and boundaries

Current user direction for this continuation (the dated amendment below is
latest when it conflicts with older wording):

- proceed autonomously through the documented ready tasks;
- whole active Fusion composition is the FIRST_USABLE arrangement scope;
- preserve GroupOperators for the default FIRST_USABLE path; the amended
  continuation separately requires safe flatten-all behind a measured
  identity-preserving host primitive;
- DaVinci Resolve operation, script execution, normal exit, restart, and exact Resolve/fuscript recovery are authorized for this development/test lane;
- use disposable fixtures for mutations; do not save the valuable project;
- task-branch code/tests/docs edits, commits, pushes, and Draft PR updates are authorized;
- do not merge `main`, publish a release, force-push shared history, delete unrelated work, or rewrite unrelated user changes.

`AGENTS.md` and fresh live state remain authoritative. This runbook does not broaden repository authority.

## 2. Roles

| Role | Responsibility |
|---|---|
| Coordinator | fresh-state reconciliation; task selection; branch/host ownership; blocker localization; candidate integration; final evidence reconciliation |
| Worker | implement/fix only the active task; run focused tests; return candidate + evidence; do not redefine Goal or acceptance |
| Host Worker | operate Resolve only within exact target/fixture boundaries; snapshot before writes; read back after writes; Undo/rollback/cleanup; no save |
| Verifier | fresh context; independently inspect a fixed candidate and evidence; do not repair the candidate during verification |

One integration writer owns PR #5 branch at a time. One Host Worker owns the Resolve project/session at a time.

## 3. Mandatory startup sequence

Before acting:

1. inspect local Git branch, HEAD, status, worktrees, and remotes;
2. fresh-read remote `feat/arrange-uia-e2e-20260906` and `feat/semantic-arrange-v1-20260906`;
3. fresh-read PR #5;
4. read `AGENTS.md`;
5. read `docs/CURRENT_STATE.md`;
6. read this plan/runbook;
7. read `docs/SEMANTIC_LAYOUT.md`, `docs/SEMANTIC_LAYOUT_ACCEPTANCE.md`, `docs/EVIDENCE_PROTOCOL.md`, and newest relevant checkpoints;
8. if a host task is next, perform a bounded read-only Resolve identity sanity before mutation.

Historical SHAs in the plan are locators, not permission to overwrite newer work.

## 4. Git / branch discipline

- Preserve dirty or unknown local work before checkout/integration.
- Never start recovery with `reset --hard`, `git clean`, or destructive stash/drop.
- Integrate the continuation branch into PR #5 non-destructively.
- No force push.
- If remote PR #5 advanced, read its changes first and reconcile rather than replacing it with the old authored base.
- After each pushed checkpoint, fresh-read the remote ref and relevant files before claiming publication.
- `docs/CURRENT_STATE.md` is the runtime state pointer. Do not turn PLAN.md into a second mutable queue ledger.

## 5. Resolve / Fusion safety contract

Every mutation-capable host task uses:

```text
exact target bind
-> pre snapshot / compact signatures
-> bounded mutation
-> readback
-> invariant comparison
-> rollback/Undo when owned by the command
-> exact cleanup
-> final valuable-host readback
```

Hard requirements:

- current project/timeline/comp identity must be known before mutation;
- no valuable project save;
- no blind keyboard/mouse automation;
- no global shortcut mutation;
- no unrelated process termination;
- no reuse of known-bad hand-written single-Paste / long full-graph evidence route;
- no guessed `DoAction`/`QueueAction` action is an Ungroup primitive; no
  delete/recreate or settings reconstruction may substitute for it;
- ambiguous side effect means read back first; do not blindly resend.

Expected final valuable host state after each host phase:

```text
project: PSD2Fusion
timeline: Timeline 1
page: Fusion
valuable comp: COMPB_Modified=false
RNK-owned disposable remnants: none
project save: false
```

If the live project differs because the user intentionally changed context, do not force this historical target; fresh-read and protect the actual valuable state.

## 6. Endpoint recovery

If Resolve UI is responsive but scripting endpoint hangs:

1. do not repeat the same long call;
2. one short bounded read-only identity probe may be attempted if the previous failure path materially differed;
3. if endpoint is still unhealthy, Resolve recovery is authorized:
   - record exact Resolve PID/path and child fuscript PID/path;
   - attempt normal Resolve close without saving;
   - bounded wait;
   - if still running, terminate only the exact Resolve process and verified child fuscript tree;
   - do not touch unrelated processes;
   - relaunch Resolve;
   - first post-restart scripting call must be a short read-only identity probe;
4. if that first post-restart probe also hangs, stop the host lane as `BLOCKED_HOST`; do not modify product code merely to explain an unavailable endpoint.

PC reboot is outside this runbook unless separately authorized later.

## 7. Large-graph transport recovery

The known ~1100-tool full evidence walk timed out previously. Do not replay it materially unchanged.

Adaptation order:

1. establish a medium-scope successful envelope;
2. measure elapsed time and returned payload size;
3. compute canonical counts/hashes in-host;
4. return compact signatures only;
5. chunk evidence by scope/category where required;
6. expand only mismatching rows;
7. separate product execution from evidence transport where possible: run the real whole-comp product action once, then verify with bounded compact readback calls;
8. if one envelope fails, one materially unchanged retry maximum; then change chunk/payload/aggregation strategy.

A transport timeout does not equal a product failure. Keep claims narrow.

## 8. Nested Group fixture rule

For non-empty nested Group host evidence:

- prefer the already host-proven nested fixture recipe referenced by current checkpoints;
- do not invent a new hand-written single-Paste shape;
- if the host does not expose a direct child-add API, do not fake membership;
- prior evidence may be carried only if the relevant recursion/layout code is unchanged and focused tests prove the integration seam did not alter that contract;
- mark carried evidence explicitly as `CARRIED_EVIDENCE`, never as a fresh host run.

## 9. Optional / feature-local blockers

These must remain localized unless they invalidate the whole-comp preserve path:

### AskUser UI accessibility

Measured status: `BLOCKED_HOST_ACCESSIBILITY_HARD` for semantic Run/Cancel/checkbox identity on Resolve Studio 21.0.3.7.

Do not repeat UIA/MSAA capability exploration in this mission. A final human release smoke may remain conditional.

### Busy stage UI

If `UIDispatcher`/native modeless busy capability remains unavailable on the relevant Comp Script path:

- record `BUSY_UI=BLOCKED_HOST_CAPABILITY`;
- do not fabricate stage visibility;
- do not add unsafe threads or blocking RunLoop behavior merely to satisfy UI polish;
- this does not invalidate core whole-comp Arrange safety/behavior unless the product contract is explicitly changed.

### Selection-only

Selection-only/fixed-obstacle semantics are experimental/regression coverage and not a release blocker for this mission.

### Ungroup / flatten-all (amended continuation)

The default preserve-mode UI remains unchanged and does not expose a checkbox
while the host capability is unproven.  The amended flatten path is a separate
structural command contract:

```text
explicit measured host primitive
-> full snapshot
-> deterministic deepest-first Group removal
-> flat topology/identity readback
-> semantic Arrange in the same Undo transaction
-> exact grouped Undo restoration on any failure
```

Only an adapter callback with that contract may be supplied to
`flatten_all_comp`.  Generic `DoAction`/`QueueAction`, blind UI operations,
delete/recreate, and guessed settings transformations are not accepted.  If
the host exposes no such primitive, `ungroup=True` refuses before mutation and
the gate is recorded as `BLOCKED_HOST_API`; this is independent of the UIA/MSAA
accessibility blocker.

## 10. Failure handling table

| Failure | Autonomous response | Stop / wait condition |
|---|---|---|
| unit/compile/install failure | localize, fix within mission scope, add regression, rerun focused + full required checks | required spec/authority change needed |
| PR #5 advanced remotely | fresh-read, reconcile non-destructively, rerun affected validation | ownership conflict cannot be resolved safely |
| target identity mismatch | fail closed before write, reacquire exact current target, preserve user context | exact target cannot be proven |
| scripting endpoint hang | use §6 bounded recovery | first post-restart read-only probe also hangs |
| large evidence timeout | use §7 transport adaptation | no bounded evidence route remains after changed strategies |
| invariant mismatch after write | stop further writes, localize mismatch, rollback/Undo, verify restoration | restoration cannot be proven |
| cleanup ambiguity | identify exact owned object before delete; read back after delete | ownership cannot be proven |
| verifier FAIL | Worker fixes candidate; new evidence; fresh verifier | acceptance would require lowering a required criterion |
| context/session end | commit/push safe checkpoint; update CURRENT_STATE/checkpoint with exact resume point | no redispatch runtime available; return durable handoff |
| human-only UI boundary | finish all independent tasks first | only final smoke remains or authority is required |

## 11. Checkpoint contents

A meaningful checkpoint records:

- Goal / active task ID;
- candidate branch + exact SHA;
- local/remote worktree status;
- host identity/version when relevant;
- exact fixture/target;
- mutations performed;
- tests / commands and results;
- compact host evidence / hashes;
- Undo/rollback/cleanup result;
- remaining blocker and whether it is local or mission-wide;
- smallest ready next task / exact resume point.

Do not report `CHECKPOINTED` as synonymous with PASS.

## 12. Verification separation

Worker and Verifier responsibilities are separate.

Verifier minimum checks:

- candidate SHA is the one claimed;
- diff matches mission scope;
- PR #5 branch contains accepted continuation changes;
- offline/install evidence is current;
- small-host smoke is on the integrated candidate;
- nested Group evidence is fresh or explicitly valid carried evidence;
- large-host evidence follows the compact protocol and does not infer invariants from incomplete hashes;
- final host cleanup/no-save claim has readback;
- optional UI/accessibility blockers are not silently converted into PASS;
- main is not merged.

Verifier must return FAIL/BLOCKED with specific evidence rather than editing the candidate itself.

## 13. Human boundary

Do not request routine user clicks during the plan.

Only after all autonomous tasks and fresh verification are complete may the Coordinator ask for one release smoke if still required:

```text
Workspace -> Scripts -> Comp -> ResolveNodeKit_Arrange
-> confirm whole-comp Arrange
-> Run
```

Before asking, ensure:

- installed candidate hash is known;
- safe target and expected result are explicit;
- run log is enabled and sufficient to classify one failure;
- exact post-click readback/resume action is ready.

If the existing contract can be fully accepted without that human smoke, mark it `NOT_REQUIRED` with evidence rather than asking anyway.

## 14. Final report schema

Use the repo's existing schema where applicable, and include at minimum:

```text
PROGRAM_STATUS
SEMANTIC_ARRANGE_STATUS
FIRST_USABLE
USER_FLOW
FEATURE_MAP
INVARIANTS
OFFLINE_TESTS
HOST_TESTS
LARGE_HOST
NESTED_GROUP
FINAL_HOST_STATE
PR5
BLOCKERS
NORMAL_DEV_HUMAN_CLICK_REQUIRED
RELEASE_SMOKE_HUMAN_CLICK_REQUIRED
READY_NEXT
```

`MISSION_COMPLETE` is not available from this Semantic Arrange continuation alone while the separate mission-critical visual nested-group expansion requirement remains unresolved.
