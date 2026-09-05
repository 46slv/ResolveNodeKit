# ResolveNodeKit autonomous orchestration plan — v2

This is the long-horizon execution contract for ResolveNodeKit. It is designed to keep useful work moving across Codex sessions without relying on chat history, while stopping before unobservable or irreversible host changes.

Live user instruction, local Git/worktree, remote Git/PR, and live Resolve readback always outrank this document. Read `docs/CURRENT_STATE.md` for the current ready queue and blockers.

## 1. Mission and completion levels

ResolveNodeKit should become a practical node-workflow toolkit for both DaVinci Resolve Fusion and Color.

Current user goals include:

- organize Fusion graphs without changing image logic;
- preserve nested `GroupOperator` hierarchy;
- recursively tidy nested group contents;
- keep groups as groups while making nested contents visibly accessible;
- add frequent node editing/selection/connection helpers;
- support Color through its actual scripting capabilities rather than pretending it has Fusion FlowView parity.

### Useful milestone vs mission completion

`USABLE_BETA` may be checkpointed before every research blocker is solved, but it must document limitations accurately.

`MISSION_COMPLETE` is stricter. It requires all explicit mission-critical user requirements to pass or the user to explicitly waive/change them. At present, visual nested-group access is mission-critical: an agent may not silently redefine completion to “recursive tidy while still collapsed.”

A missing Color XY-position API blocks that specific Color feature unless the user explicitly makes physical Color layout mandatory; it does not automatically block other Color utilities.

## 2. Source precedence and required recovery order

Every long run starts in this order:

1. current user instruction;
2. local `git status`, current branch, HEAD, remotes, and uncommitted work;
3. current remote branch / main / Draft PR;
4. `AGENTS.md`;
5. `docs/CURRENT_STATE.md`;
6. this document;
7. relevant feature contract (`GROUPS`, `HOST_VALIDATION`, `COLOR_API`);
8. newest applicable checkpoint;
9. installed/current Resolve docs and live host probes.

Never pull/reset/checkout over unknown local changes merely because the remote branch advanced.

## 3. Roles

### Parent orchestrator — Codex

Owns Mission state, phase choice, mutation authority, evidence acceptance, checkpoints, Git integration, and final status.

The parent:

- fresh-reads live state;
- chooses the smallest ready gate from the dependency graph;
- delegates only when useful;
- verifies worker events/readback independently;
- commits/pushes accepted task-branch progress;
- updates Draft PR and `CURRENT_STATE`;
- keeps feature-local blockers local when independent work remains.

### Resolve host worker — OpenCode / Muse / MCP

Preferred measured route:

`Codex -> OpenCode CLI -> Muse Spark -> OpenCode MCP -> davinci-resolve MCP -> Resolve`

Use a bounded Work Package containing only Goal, Done, Constraints, exact target if already bound, allowed mutations, and required evidence. Do not forward the whole orchestration document or chat transcript to Muse.

Structured tool-use events and host readback are evidence. Muse narration is not acceptance evidence.

For one continuing host investigation, retain the exact OpenCode session if continuity is useful. A historical session ID is not automatically reusable in a later run.

### Repo implementation lane

May be the parent or a bounded worker. It owns source/tests/docs within the authorized task branch, reproduces host failures offline when possible, adds regression tests, and implements the smallest correction.

### Fresh verifier lane

Use when a mutation is risky, a blocker repeats, or an implementation worker’s conclusion needs independent review. The verifier starts from evidence/live state, not from the prior worker’s conclusion.

## 4. Prompt and evidence contracts

### Work Package

A delegated worker normally receives:

- Task / Goal
- owned scope
- required references
- non-goals
- acceptance criteria
- validation expectation
- stop/escalation condition
- compact return schema

### Evidence Packet

Worker returns:

- task / current state
- changed surface
- exact tests/runtime/host evidence
- postcondition/readback
- invariant comparison
- remaining gap
- exact blocker/failure fingerprint when applicable

Raw transcripts are retained only where necessary; the parent consumes compact evidence.

## 5. Program status semantics

Statuses may apply to a **feature lane** or the **whole current run**.

- `PASS` — the selected phase acceptance is proven.
- `CHECKPOINTED` — meaningful progress exists and another authorized ready gate remains.
- `BLOCKED_HOST` — current host/transport/runtime prevents this gate.
- `BLOCKED_API` — required operation has no safe/readback-verifiable API/path.
- `BLOCKED_DATA` — current data cannot exercise the gate and creating/switching target is outside authority.
- `BLOCKED_SCOPE` — next action needs authority not currently granted.
- `BLOCKED_SAFETY` — target/invariants/rollback cannot be trusted.
- `FAILED_ROLLBACK` — mutation failed and complete restoration cannot be proven; hard stop.

### Important rule

A single blocked feature does **not** make the program globally blocked while an independent authorized gate is ready. In that situation:

1. checkpoint the feature blocker;
2. update `CURRENT_STATE`;
3. select another ready gate;
4. overall program status remains `CHECKPOINTED`.

A whole-run `BLOCKED_*` is terminal only when no independent ready gate remains, a safety hard stop occurs, resource bounds end the run, or new user authority is genuinely required.

## 6. Global execution loop

For every phase:

1. **Recover** — fresh-read local/remote state; reconcile ambiguity before mutation.
2. **Select ready gate** — use prerequisites, not fixed numerical order.
3. **Bind target** — identify exact repo/worktree and exact host project/timeline/comp or Color graph scope.
4. **Snapshot** — capture only the state needed to prove invariants/rollback.
5. **Observe first** — inspect actual API/values before inventing a write.
6. **Implement smallest change** — add deterministic tests where possible.
7. **Canary** — smallest disposable/duplicate target first for new mutation semantics.
8. **Read back** — prove intended state and preserved invariants.
9. **Repeat once** — prove idempotence where relevant.
10. **Checkpoint/commit** — do not leave accepted measured fixes as anonymous dirty work when commit authority exists.
11. **Continue** — choose the next ready independent gate.

Do not stop merely because a hypothesis failed.

## 7. Git and local-state reconciliation rule

This rule is mandatory because the project has already encountered a real host run that left valuable dirty fixes while the remote branch advanced.

When local worktree and remote diverge:

1. inspect and classify every local change;
2. preserve valuable dirty work on a temporary branch/checkpoint commit or patch;
3. fetch remote state;
4. integrate/rebase/cherry-pick only after preservation;
5. run the complete relevant suite;
6. inspect diff attribution;
7. commit/push the canonical task branch;
8. update Draft PR and `CURRENT_STATE`.

Do not begin with `reset --hard`, `clean`, branch deletion, or blind checkout.

Current project authority allows commits/pushes on task branches and Draft PR updates. Main merge/release/force-push/unrelated cleanup remain outside autonomous authority.

## 8. Large-graph evidence protocol

Do not assume a 1000+ tool graph can be serialized through MCP as one remote snapshot. A prior 1107-tool snapshot path timed out.

For large graphs:

1. run a bounded in-Resolve/Fusion diagnostic that computes canonical summaries locally;
2. return compact evidence only: tool count, group count/depth, connection-signature hash, membership-signature hash, position-signature hash, optional sampled parameter hash, duplicate-coordinate counts by visible scope, timings, and focused mismatch rows;
3. perform pre/post hash comparison inside the host where practical;
4. expand mismatches only when a hash differs;
5. avoid repeating a known whole-graph transport timeout with the same approach.

If needed, add a repo diagnostic script to make this deterministic. Large-graph verification is not allowed to degrade into “worker says unchanged.”

## 9. Dependency graph and phase gates

The phase labels are stable references, not a requirement to execute strictly numerically.

```text
P0R reconciliation
  -> P2C flat tidy closeout
       -> P3A Tidy Nested canary -> P5 large stress
       -> P6 low-risk Fusion ops -> P7 rewiring
       -> P8 Color map -> P9 Color reversible ops

P1 host transport/target bind is required before any host gate in a new run.

P3B visual expansion research depends on P1, but is independent of P3A/P6/P8.
P3B PASS -> P4 fit-to-contents.

Stable feature set -> P10 unified command surface -> P11 packaging.
P12 PSD2Fusion integration is optional and one-directional.
P13 USABLE_BETA can be reached with accurately documented feature blockers.
P14 MISSION_COMPLETE requires all explicit mission-critical user requirements, including visual nested-group access, or explicit user waiver.
```

## P0R — Reconcile measured host fixes

### Goal

Make the current canonical task branch contain both the newer remote orchestration work and the real-host measured local fixes without losing either.

### Acceptance

- local dirty work was inspected and preserved before integration;
- host-measured code/test/doc changes are incorporated or explicitly rejected with evidence;
- full relevant test suite and `compileall` pass;
- diff contains no unrelated work;
- canonical task branch is committed/pushed;
- Draft PR and `CURRENT_STATE` reflect the integrated state.

### Stop

`BLOCKED_SAFETY` if local changes cannot be attributed/preserved safely. Do not erase them to make Git clean.

## P1 — Host transport and target lock

### Goal

Prove OpenCode/Muse/Resolve MCP transport and bind the exact currently authorized host target.

### Acceptance

- actual OpenCode version/model/agent and MCP route are observed;
- structured MCP tool-use evidence exists;
- exact project/timeline/comp or Color scope is recorded;
- target identity is rechecked before every write batch;
- pre-snapshot is sufficient for the gate being attempted.

### Retry/stop

Read-only transport recovery is autonomous. After materially identical transport failure repeats without new evidence, stop that host gate `BLOCKED_HOST` and continue offline/independent lanes if available.

## P2C — Flat Fusion Tidy closeout

### Goal

Close the host acceptance for the integrated, measured grid/readback implementation.

### Acceptance

- representative serial/Merge/mask/isolated canary passes;
- connections and sampled processing state are unchanged;
- writes/readback respect measured FlowView snapping semantics;
- second run produces zero drift;
- Undo restores prior positions when safely testable;
- rollback path remains proven;
- current branch tests pass.

After this passes, flat Tidy is no longer a blocker for independent node-tool development.

## P3A — `Tidy Nested` without visual expansion

### Goal

Provide useful recursive hierarchy-preserving layout even while runtime visual expansion research continues.

This must be a separate command/API from strict `Tidy + Expand Groups`.

### First host canary

With a real collapsed GroupOperator:

- read direct hierarchy;
- read child positions;
- modify child positions only;
- read back positions;
- prove group membership, connections, processing state, and expanded/collapsed display state are unchanged;
- Undo/rollback/cleanup as appropriate.

### Acceptance

- collapsed-group children can be positioned safely;
- nested scopes are deterministic and non-overlapping;
- structural signatures unchanged;
- second run stable;
- command name/contract does not claim visual expansion.

If collapsed child positioning is not host-writable/readback-verifiable, this lane may become `BLOCKED_API`; other lanes still continue.

## P3B — Visual Group expansion runtime action research

### Mission-critical goal

Find a safe, readback-verifiable way to perform the actual runtime Group Expand/Collapse operation while preserving hierarchy.

### Known disproven path

On measured Resolve Studio 21.0.3.7, `SaveSettings` -> set `ViewInfo.Flags.Expanded=true` -> `LoadSettings` returned success but immediate readback discarded the expanded state. Do not repeat that exact hypothesis unless new evidence changes the premise.

### Research order

1. inspect current MCP/tool/runtime surfaces for an existing named Fusion UI action/command route;
2. inspect scripting/runtime surfaces for a real Expand/Collapse command;
3. only if a bounded action path exists, use one disposable Group canary;
4. select exact Group, invoke one action, then independently verify visual/subflow state, hierarchy, connections, Undo/cleanup;
5. do not install a new desktop automation stack, change shortcuts, or send blind keystrokes merely to bypass this gate without new authority.

### Acceptance

- actual runtime expansion occurs;
- result is independently observable/readback-verifiable, not inferred from a return code;
- group remains a GroupOperator with unchanged membership/connections;
- operation can be targeted deterministically across nested groups;
- cleanup/Undo behavior is understood.

If no safe action route exists, mark this lane `BLOCKED_API`, continue independent lanes, and keep `MISSION_COMPLETE` open.

## P4 — Fit runtime-expanded groups to contents

Prerequisite: P3B PASS.

### Goal

Ensure each expanded group visibly contains all direct children, including nested groups, without clipping.

### Method

Measure real host geometry first. Record `GroupInfo.Size`, `Scale`, `Offset`, group position, child bounds, and UI result. Change one variable at a time on a canary. Implement only a measured readback-verifiable formula with padding.

### Acceptance

- all direct children visible;
- nested groups visible within parents;
- stable second run;
- no destructive ungroup/regroup;
- structural/processing invariants unchanged.

No formula may be invented from `.setting` examples alone.

## P5 — Large/nested stress gate

Prerequisites: P2C + P3A. P3B/P4 are not prerequisites for testing recursive tidy-only.

### Goal

Exercise real PSD2Fusion-scale complexity without transporting the whole graph blindly.

### Acceptance

- large duplicate completes without Resolve crash/hang;
- compact pre/post structural hashes match;
- intended position hash changes first run and stabilizes second run;
- duplicate-coordinate collisions within each managed scope are classified;
- runtime/timing are operationally usable;
- no unbounded loops or repeated full-graph timeout path.

If Resolve becomes unstable, stop host writes and continue profiling/offline optimization from the last safe case.

## P6 — Low-risk Fusion node operations

Prerequisite: P2C.

Implement/test in this order unless evidence suggests a smaller independent gate:

1. align selected nodes horizontal/vertical;
2. distribute selected nodes horizontal/vertical;
3. selected/component-scope tidy;
4. upstream/downstream/connected-component selection;
5. safe group display helpers only where host API is proven;
6. frame/center selected only when a real API/action exists.

Each command needs explicit selection scope, deterministic result, readback, no processing-state change, and Undo/rollback where appropriate.

## P7 — Fusion rewiring operations

Prerequisite: stable P6 safety/readback patterns.

Order:

1. insert-between;
2. explicit connect/reconnect;
3. Swap Merge foreground/background;
4. detach while preserving surrounding connection when contract is defined;
5. bypass/pass-through where state can be read back;
6. duplicate-with-connections only after duplication semantics are proven.

Before every rewiring operation snapshot exact affected input/output identities and edges. Read back the entire affected edge set; rollback on mismatch. Ambiguous connection mutation is `BLOCKED_API`, never a blind retry.

## P8 — Color read-only capability map

Prerequisite: P1 for live host; independent of Fusion feature blockers.

Map current project/timeline/item/group graph acquisition and observed Graph methods. Distinguish unsupported methods from unavailable current context/item types. Commit a capability matrix based on actual installed host evidence.

All P8 operations are read-only.

## P9 — Color reversible operations

Prerequisite: P8.

Implement only operations with observable postconditions, e.g. node enable/disable, cache mode, LUT helpers, graph inspection/navigation, and other measured surfaces.

Each operation requires target scope, pre-state, documented mutation, post-readback, and rollback/exclusion reason.

Color physical XY arrangement is a separate capability question; absence of such an API blocks that feature, not all Color progress.

## P10 — Unified command surface

Build one ResolveNodeKit vocabulary backed by separate Fusion/Color adapters.

Principles:

- manual menu/script/UI invocation first;
- do not replace standard Resolve shortcuts by default;
- context-sensitive availability;
- unsupported operations explain why rather than silently no-op;
- layout/display commands visually distinct from rewiring/destructive commands.

## P11 — Packaging

After stable host surfaces exist:

- one canonical install location per script category;
- install/update/uninstall with backup/readback;
- no duplicate script copies;
- no watcher/startup service by default;
- no global shortcut mutation;
- exact installed version diagnostics.

Installation and uninstallation must be idempotent and only touch ResolveNodeKit-owned files.

## P12 — Optional PSD2Fusion integration

ResolveNodeKit remains standalone. PSD2Fusion may optionally invoke it after structural generation. Tidy failure must not invalidate or alter PSD2Fusion structural/parity semantics. Do not move PSD2Fusion rendering/parity logic into ResolveNodeKit.

## P13 — `USABLE_BETA`

A beta may be produced while one research feature is blocked, but README/PR/release notes must say so clearly.

Minimum beta target should include, subject to host capability:

- flat Tidy;
- `Tidy Nested` if P3A passes;
- representative low-risk Fusion operations;
- Color capability/inspection plus proven reversible helpers;
- coherent command surface;
- safe manual install/update/uninstall;
- host validation matrix and known limitations.

A beta is not `MISSION_COMPLETE` if visual nested-group access remains blocked.

## P14 — `MISSION_COMPLETE`

Requires:

- explicit mission-critical user requirements pass on a real supported host, including keeping nested groups intact while opening them and making contents visible; or the user explicitly changes/waives that requirement;
- release commands/tests/readback/rollback have no unresolved safety defect;
- Color scope is capability-complete for the agreed product target and unsupported APIs are accurately documented;
- current docs and packaging reflect actual proven behavior;
- no known incomplete rollback.

Agents cannot self-waive a mission-critical requirement to declare completion.

## 10. Global hard-stop rules

Immediately stop the current host mutation sequence if:

- project/timeline/comp identity changes unexpectedly;
- layout/display work changes connections, processing parameters, keyframes, tools, media, grades, or render state;
- an ambiguous write has no independent readback;
- rollback is incomplete/unverifiable;
- Resolve crashes or remains persistently unresponsive after mutation;
- recovery would require unauthorized destructive reload/switch/cleanup;
- credentials, account permissions, payment, UAC/elevation, or security boundaries are reached.

`FAILED_ROLLBACK` is always a hard stop for further host mutation until reconciled.

## 11. Escalation/no-progress rule

Count repeated **evidence states**, not generic failures.

- first failure: inspect and change hypothesis;
- second materially similar failure: use a genuinely different approach or fresh verifier;
- repeated same fingerprint with no evidence delta: checkpoint/classify rather than loop.

Do not permanently escalate model/role because one hard problem needed stronger diagnosis. Return routine execution to the cheaper/bounded worker after ambiguity is resolved.

## 12. Do-not-stop cases

Continue autonomously when safe if:

- deterministic offline tests expose a bug;
- API names/version behavior differ but can be safely measured;
- aesthetics/spacing need tuning without invariant risk;
- helper refactoring is needed for snapshot/readback/rollback;
- a worker session dies but repo/host state can be recovered;
- one feature is blocked while independent gates remain;
- docs/tests/checkpoints need updating.

## 13. Autonomous mutation authority

Unless newer user instruction narrows it:

### Repository

Allowed:

- read all ResolveNodeKit state;
- create/use task branches;
- edit code/tests/docs;
- commit/push task-branch work;
- update Draft PRs;
- add diagnostics/regressions.

Not autonomous:

- merge to main;
- publish release;
- force-push shared history;
- delete unrelated branches/work;
- rewrite unrelated user changes.

### Resolve/Fusion

For an explicitly authorized currently-open target, autonomous writes are limited to the phase being validated and its safety contract, including node positions and measured Group display state/geometry. Rewiring is authorized only during its dedicated phase after snapshot/readback/rollback exists.

Do not autonomously switch/save/close/reload projects, alter media/grades during Fusion layout work, change global shortcuts, ungroup/flatten graphs, or install desktop automation/watchers/services.

## 14. Checkpoint/resume contract

At every phase boundary or forced stop, update `docs/CURRENT_STATE.md` and preserve a dated checkpoint when host evidence is materially new.

Minimum report fields:

```text
PROGRAM_STATUS: CHECKPOINTED | MISSION_COMPLETE | BLOCKED_*
PHASE: gate id + feature-lane status
REPO / LOCAL_BRANCH / LOCAL_HEAD / REMOTE_HEAD / PR / BASE
LOCAL_DIRTY: paths + attribution
TESTS: exact command/result
HOST: exact version
TARGET: project/timeline/comp identity for this run
OPENCODE: version/model/agent/session used
MCP: route + structured evidence location/summary
PRE: compact signatures
MUTATIONS: exact bounded writes
POST: compact signatures/readback
ROLLBACK: not-needed | proven | failed
BLOCKERS: feature -> exact blocker/fingerprint
READY_NEXT: ordered ready gates with prerequisites satisfied
```

Never use an old checkpoint SHA/session/target as authority on resume. It is a locator, then fresh-read.

## 15. Current-state pointer

Do not hard-code the current next gate here. `docs/CURRENT_STATE.md` owns the operational ready queue. This orchestration document owns the durable rules and dependency graph.
