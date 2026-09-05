# ResolveNodeKit autonomous orchestration plan

This document is the long-horizon execution contract for continuing ResolveNodeKit with Codex as the parent orchestrator and OpenCode/Muse as the bounded DaVinci Resolve MCP worker.

It is intentionally written so that work can resume after a stopped session without relying on chat history. Live repository and live host state always outrank example SHAs, old reports, or this document's snapshot wording.

## Mission

Build a practical node-workflow toolkit for DaVinci Resolve that supports both Fusion and Color, with Fusion first because it exposes the stronger graph/FlowView surface.

The near-term user-visible goal is:

1. organize existing Fusion node graphs without changing image logic;
2. keep nested `GroupOperator` hierarchy intact;
3. recursively expand and tidy nested groups;
4. make every expanded group show its contents rather than leaving clipped/hidden internal nodes;
5. then add frequent node-editing operations;
6. build Color operations only from the actual installed Resolve API boundary.

This is not a Blender Node Wrangler port and not an Auto-Node-Tree fork. Prior art may inform tests and design, but ResolveNodeKit owns its implementation and Resolve-specific UX.

---

## Authority order

Every run must resolve conflicts in this order:

1. the user's current instruction;
2. live repository state, current tests, current Draft PR, and live Resolve/Fusion readback;
3. installed/current Resolve scripting documentation and measured API behavior;
4. committed ResolveNodeKit docs and prior-art notes;
5. inference.

Never treat a SHA, branch name, project name, timeline name, or active comp captured in an old prompt as source of truth. Fresh-read first.

---

## Orchestration roles

### Parent Orchestrator — Codex

Owns the mission and acceptance decision.

Responsibilities:

- fresh-read repo/branch/PR before work;
- choose the smallest next unresolved gate;
- keep implementation writes inside ResolveNodeKit task workspaces;
- launch bounded OpenCode workers for Resolve MCP access;
- preserve the exact OpenCode session ID when a host investigation needs continuity;
- independently verify structured tool-use events, host readback, Git diff, and tests;
- classify terminal state;
- checkpoint enough evidence for another session to resume without chat history.

The parent must not accept a worker's textual claim as proof of host success.

### Host Worker — OpenCode CLI / Muse / Resolve MCP

Standard route:

`Codex -> OpenCode CLI -> Muse Spark 1.3 -> OpenCode MCP layer -> davinci-resolve MCP -> DaVinci Resolve`

Baseline invocation shape:

`opencode run --model opencode-go/muse-spark-1.3-contributor --agent build --format json "<bounded task>"`

Responsibilities:

- perform Resolve/Fusion observation and bounded host mutation only;
- return structured tool-use evidence;
- never broaden the mission from layout/display operations into grade/media/project changes;
- never switch project/timeline/comp unless the parent mission explicitly authorizes it;
- never blind-retry an ambiguous write.

If a host investigation spans multiple calls, reuse the exact OpenCode session rather than relying on conversational similarity.

### Repo Worker / Implementation lane

May be the parent Codex itself or a separate bounded worker.

Responsibilities:

- inspect code/tests/docs;
- reproduce observed host failures offline where possible;
- implement the smallest correction;
- add regression tests;
- keep Fusion and Color adapters separate;
- avoid inventing APIs that were not observed.

### Verifier lane

The parent performs the final verification. For risky or repeated failures, it may launch a fresh read-only worker to independently inspect evidence or diff.

A fresh verifier should not inherit the implementation worker's conclusion as a premise.

---

## Worker prompt rule

Do not dump the entire project history into Muse. A host worker receives only:

- Goal
- Done
- Constraints
- exact target identity if already measured
- Evidence required
- bounded mutation authority

The parent retains the larger orchestration state.

---

## Global execution loop

For every phase:

1. **Recover** — fresh-read Git state, PR state, tests, and relevant docs.
2. **Bind target** — identify exact project/timeline/comp or Color graph scope.
3. **Snapshot** — record everything the planned write must preserve.
4. **Observe first** — determine actual host API/values before inventing a fix.
5. **Plan smallest mutation** — no adjacent refactor unless needed to pass the gate.
6. **Offline implement/test** — deterministic regression first when possible.
7. **Host canary** — execute only the bounded operation.
8. **Read back** — verify the desired state and invariants independently.
9. **Repeat once** — prove idempotence where applicable.
10. **Checkpoint** — record evidence, commit, and next unresolved gate.
11. **Continue automatically** if the next phase is within autonomous authority.

Do not stop merely because one hypothesis failed. Stop only under the stop criteria below.

---

## Terminal / checkpoint status vocabulary

Every substantial run ends with exactly one primary status:

- `PASS` — phase acceptance is completely proven.
- `CHECKPOINTED` — meaningful progress is committed; a later phase remains.
- `BLOCKED_HOST` — Resolve/OpenCode/MCP/runtime prevents progress.
- `BLOCKED_API` — required operation is not exposed or cannot be safely verified.
- `BLOCKED_DATA` — current active data cannot exercise the required case and creating/switching target data is outside authority.
- `BLOCKED_SCOPE` — completing the next step would exceed the user's authorized mutation scope.
- `BLOCKED_SAFETY` — rollback, target identity, or invariance cannot be trusted.
- `FAILED_ROLLBACK` — a mutation failed and full restoration could not be proven. This is an immediate hard stop.

A non-terminal implementation failure is not a status by itself; investigate and continue if safe.

---

# Phase plan

## P0 — Recovery and baseline

### Work

- fresh-read `main`, task branch, Draft PRs, AGENTS, README, docs, tests;
- identify current branch HEAD and base;
- run the relevant offline suite;
- verify no unrelated working-tree changes are being absorbed;
- record current OpenCode version/model/agent/MCP availability before a host phase.

### Acceptance

- exact live repo state is known;
- existing tests pass or every pre-existing failure is classified;
- next unresolved phase is selected from live evidence rather than chat memory.

### Autonomous range

Full read-only repo inspection, test execution, temporary local diagnostics, and creation of a task branch are autonomous.

### Stop

Stop only if the repository cannot be located/read, the target branch has unrelated uncommitted user work that cannot be isolated, or authority is ambiguous for destructive cleanup.

---

## P1 — Host transport and target lock

### Work

- run `opencode mcp list`;
- prove the Muse worker can make a structured davinci-resolve MCP call;
- identify the currently open Resolve project, current timeline, and active Fusion comp without switching them;
- collect a read-only graph summary: tool count, group count/depth, connection signature, current positions, group expanded states where available;
- assign a run-local target identity and keep checking that identity before writes.

### Acceptance

- structured MCP tool-use evidence exists;
- active target is unambiguous;
- the parent can distinguish host evidence from Muse narration;
- pre-mutation snapshot is sufficient to detect unintended structural changes.

### Autonomous range

Reconnect/relaunch the OpenCode CLI harness, retry a read-only query, inspect MCP listings, and adjust bounded worker prompts without asking the user.

### Expected stops

- MCP absent from OpenCode;
- Muse route cannot call MCP;
- Resolve is closed or no active Fusion comp exists;
- project/timeline/comp changes during the run;
- returned objects cannot be identified consistently.

### Stop rule

If the same transport failure occurs three times without new evidence, stop `BLOCKED_HOST` instead of looping.

---

## P2 — Flat Fusion Tidy host gate

### Work

Validate existing `Tidy Graph` against the active comp or an explicitly authorized target:

- capture positions and connection signature;
- run Tidy;
- verify positions changed as intended;
- verify connections, parameters/keyframes sampled for invariance, tool identities, and group membership did not change;
- run Tidy a second time;
- verify zero drift;
- verify Undo behavior if host evidence allows a safe test;
- verify rollback path on a controlled canary only when such a fault can be injected safely.

### Acceptance

- no overlapping layout regression in representative chains/merges;
- second run is position-identical;
- layout-only invariants are unchanged;
- one Undo restores prior layout when this is safely testable;
- no host crash or partial write remains.

### Autonomous range

Layout algorithm corrections, spacing corrections, deterministic ordering, readback hardening, and new offline tests are autonomous.

### Stop

Immediate hard stop if a layout command changes graph connections, processing parameters, keyframes, tools, media, or render state, or if rollback is incomplete.

---

## P3 — Nested GroupOperator recursive tidy

### Work

Use the existing `Tidy + Expand Groups` path on real nested data.

Measure and verify:

- `GetChildrenList()` results;
- `ParentTool` / `TOOLH_GroupParent` hierarchy;
- group depth and direct membership;
- pre/post connection signature;
- `SaveSettings`/`LoadSettings` behavior;
- `ViewInfo.Flags.Expanded` readback;
- root scope, parent-group scope, and deeper nested scopes;
- second-run stability.

### Acceptance

- all targeted GroupOperators remain groups;
- every direct parent/child membership is identical before/after;
- every connection is identical before/after;
- all intended groups read back expanded;
- internal nodes receive deterministic non-overlapping positions;
- second run is position-identical;
- a failure at a deeper group does not leave earlier groups/positions partially changed.

### Autonomous range

Fix hierarchy discovery, path/identity handling, cross-boundary projection, settings reacquisition after `LoadSettings`, and regression tests without asking the user.

### Expected stops

- `LoadSettings` recreates tools in a way that invalidates stable identity;
- group children are not visible through expected APIs;
- nested tools can have duplicate names and the current identity model cannot distinguish them;
- expanded-state readback is inconsistent;
- Undo behavior across `LoadSettings` and `SetPos` is not reliable.

### Response to expected stops

Do not immediately stop. First attempt a safer identity/readback model, e.g. hierarchical path or live object reacquisition. Stop only when no readback-verifiable mutation path remains.

---

## P4 — Fit expanded groups to contents

This is the next major current gate.

### Work

After real groups are expanded and child positions are arranged:

1. determine whether Fusion automatically resizes the visible Group frame;
2. if children are clipped, record actual `GroupInfo.Size`, `Scale`, `Offset`, group position, child positions/bounds, and UI result;
3. change one controlled variable at a time on a bounded canary;
4. infer the host's actual geometry semantics from repeated measurements;
5. implement a minimal fit-to-contents calculation with padding;
6. read settings back and visually/structurally verify all direct children are visible;
7. repeat for 2–3 nesting depths.

### Acceptance

- every expanded group shows all direct children without clipping;
- nested groups themselves remain visible as children of their parent groups;
- no arbitrary oversized canvas when a tighter stable fit is possible;
- result is stable on a second run;
- fit operation preserves group membership/connections and does not alter processing state;
- measured host evidence, not `.setting` guesswork, explains the calculation.

### Autonomous range

Measurements, small canary geometry changes, algorithm fitting, padding/config tuning, and tests are autonomous within the authorized group-display mutation scope.

### Expected stops

- `Size`/`Scale`/`Offset` cannot be written or read back;
- settings write is accepted but UI does not update deterministically;
- group visual bounds depend on undocumented UI-only state that MCP/API cannot observe;
- fitting requires destructive ungroup/regroup.

### Stop

If the only path requires ungrouping, flattening, UI macro guessing with no readback, or unrelated project changes, stop `BLOCKED_API`/`BLOCKED_SCOPE` and preserve recursive expand+tidy as a separate proven feature.

---

## P5 — Complex graph / PSD2Fusion-style stress gate

### Work

Exercise real large/nested compositions representative of the reason this project exists.

Cover:

- many GroupOperators;
- several nesting levels;
- multiple merges/masks/branches;
- disconnected tools;
- long chains;
- hundreds to roughly thousand-node scale where available;
- repeated runs.

### Acceptance

- completes without Resolve crash/hang;
- structural signature remains unchanged;
- every target group remains expanded/fitted;
- no duplicate coordinates within the same visible scope unless intentionally identical;
- repeated run is stable;
- performance is operationally usable and no unbounded algorithmic loop appears.

### Autonomous range

Profiling, algorithmic optimization that preserves deterministic output, caching graph discovery for one run, and reducing unnecessary writes are autonomous.

### Stop

If Resolve itself becomes unstable, stop host writes, record the last safe graph size/case, and continue offline/performance analysis rather than repeatedly crashing the host.

---

## P6 — Fusion low-risk node operations

Implement low-risk, reversible operations before graph-rewiring features.

Recommended order:

1. Align selected nodes — horizontal / vertical.
2. Distribute selected nodes — horizontal / vertical.
3. Tidy selected connected component / selection scope.
4. Expand all groups / collapse selected groups where safe.
5. Fit selected/all expanded groups.
6. Select upstream.
7. Select downstream.
8. Select connected component.
9. Frame/center selected where API support is real.

### Acceptance per command

- selection scope is explicit;
- deterministic result;
- one Undo when the host supports it;
- no processing-state change;
- readback verifies the expected selection/position/display mutation;
- command has offline tests where host-independent logic exists.

### Autonomous range

These commands can be implemented and host-canary tested without user confirmation while they remain reversible and inside the current comp.

---

## P7 — Fusion rewiring operations

Higher-risk commands come only after layout/display commands are stable.

Recommended order:

1. Insert selected tool between source and target.
2. Connect/reconnect selected tools.
3. Swap Merge foreground/background inputs.
4. Detach node while preserving surrounding connection where defined.
5. Bypass/toggle pass-through only where current state can be read back.
6. Duplicate-with-connections only after duplication semantics are proven.

### Required safety contract

Before any rewiring:

- snapshot the exact affected edge set and input IDs;
- validate all source/output/target/input identities;
- perform the minimal write set;
- read back the complete affected edge set;
- rollback to the exact snapshot on mismatch;
- never guess which input is foreground/background/mask if host metadata is ambiguous.

### Acceptance

- operation changes exactly the intended edges and no others;
- processing parameters/keyframes are unchanged unless the command explicitly owns them;
- rollback has a tested path;
- representative host tests pass.

### Stop

Any ambiguous connection mutation without complete readback is `BLOCKED_API` rather than a reason to blind-retry.

---

## P8 — Color read-only boundary map

Color is a separate adapter and should not block Fusion progress.

### Work

Using current Resolve host:

- map current project/timeline/current-item acquisition;
- map timeline/clip/group `GetNodeGraph()` availability;
- snapshot node count, labels, LUT, cache, and tools when exposed;
- record which item types return no graph (titles/generators/etc.);
- discover actual callable surfaces rather than extrapolating from Fusion.

### Acceptance

- committed capability matrix describes observed current-host behavior;
- unsupported vs unavailable-current-context is distinguished;
- all probe operations are read-only.

### Autonomous range

Full read-only probing and documentation are autonomous.

---

## P9 — Color reversible operations

Only add operations with an observable postcondition.

Candidates, subject to current API evidence:

- node enable/disable;
- cache mode;
- LUT helpers;
- node/graph inspection utilities;
- group/timeline graph navigation;
- other operations only when readback is available.

Color node XY layout is a separate research item. Do not pretend Fusion `FlowView` semantics apply to Color.

### Acceptance

Each operation must have:

- target graph scope;
- pre-state snapshot;
- documented mutation;
- post-state readback;
- rollback or a clearly defined reason the operation is excluded.

### Stop

If Color physical node positioning has no scriptable/readback-verifiable API, classify that feature `BLOCKED_API` and continue other Color utilities. It does not block ResolveNodeKit as a whole.

---

## P10 — Unified command surface

Once core host operations are stable, build the user-facing surface.

### Goal

One ResolveNodeKit vocabulary across Fusion and Color, backed by separate adapters.

Possible command families:

- Arrange
- Select
- Connect
- Group
- Inspect
- Color

### UX principles

- do not replace standard Resolve shortcuts by default;
- manual menu/script/UI invocation first;
- show only commands supported by the current page/context;
- default to the smallest current selection/scope that makes sense;
- destructive/high-risk commands must be visibly distinct from layout/display commands;
- provide diagnostics rather than silently doing nothing.

### Acceptance

- context detection is reliable;
- unsupported commands are disabled/explained;
- Fusion/Color implementation differences are hidden behind a coherent UX without faking parity.

---

## P11 — Packaging and installation

### Work

After host behavior is proven:

- establish one canonical install location per script category;
- add an install/update/uninstall workflow with backup/readback;
- avoid duplicate copies across multiple Resolve script folders;
- no background watcher or login-start behavior by default;
- no global keyboard shortcut mutation by default;
- provide version/diagnostic output.

### Acceptance

- install is idempotent;
- uninstall restores/removes only ResolveNodeKit-owned files;
- exact installed source/version can be identified;
- update does not overwrite user data/settings unexpectedly.

---

## P12 — PSD2Fusion integration gate

ResolveNodeKit remains a standalone utility. Integration is optional and must not make PSD2Fusion responsible for layout logic.

### Possible integration

- PSD2Fusion generates the structurally correct comp;
- ResolveNodeKit is invoked afterward as an optional tidy/expand pass;
- failure to tidy does not invalidate the generated graph structure;
- no PSD2Fusion rendering/parity logic is moved into ResolveNodeKit.

### Acceptance

- integration is one-directional and optional;
- generated graph connection/parameter parity is unchanged;
- ResolveNodeKit can still operate on hand-built Fusion comps independently.

---

## P13 — Release gate

A first usable release does not require every future NodeKit idea.

### Minimum release target

Fusion:

- flat Tidy;
- recursive Tidy + Expand Groups;
- fit-to-contents if host-accessible;
- align/distribute;
- safe selection helpers;
- verified Undo/readback/rollback behavior.

Color:

- capability/inspection utilities and any reversible operations already proven;
- clearly documented absence of XY layout if still blocked.

Packaging:

- simple manual install/update/uninstall;
- no daemon/watchers;
- concise docs and diagnostics.

### Release acceptance

- all release commands pass offline tests where applicable;
- host validation matrix records exact tested Resolve version(s);
- no known rollback failure;
- Draft PR is reviewed against this orchestration and HOST_VALIDATION;
- README accurately distinguishes proven features from host/API limitations.

---

# Global stop criteria

## Immediate hard stop

Stop the current host mutation sequence immediately when any of these occurs:

- project/timeline/comp identity changes unexpectedly;
- a layout/display command changes node connections;
- a layout/display command changes processing parameters, keyframes, grades, media, tools, or render state;
- rollback is incomplete or cannot be verified;
- Resolve crashes or becomes persistently unresponsive after the mutation;
- the only proposed recovery is a destructive project reload/switch not authorized by the mission;
- a write result is ambiguous and no independent readback exists;
- credentials/secrets/permissions would need to be exposed or changed.

## Escalation stop

For one blocker/hypothesis:

1. first failure: inspect evidence and correct the hypothesis;
2. second failure: use a fresh approach or fresh read-only verifier;
3. third materially identical failure with no new evidence: stop and classify rather than loop.

This is a failure-of-hypothesis rule, not a blanket three-command limit.

## Do not stop for

The parent should continue autonomously when:

- an offline test exposes a deterministic bug;
- a method name/version differs but can be discovered safely;
- layout aesthetics need tuning while invariants remain intact;
- a helper needs refactoring to support readback/rollback;
- new tests/docs/checkpoints are required;
- a worker session dies but the host/repo state is known and can be recovered;
- one optional feature is API-blocked but independent backlog items remain.

When one feature is blocked, checkpoint it and proceed to the next independent phase where doing so does not hide a release-critical safety defect.

---

# Expected blockers and default autonomous response

| Expected blocker | First autonomous response | Terminal only when |
| --- | --- | --- |
| OpenCode MCP missing | inspect `opencode mcp list`, config, CLI harness; retry read-only | route cannot be restored without new credentials/manual install |
| Muse worker fails | relaunch bounded worker, preserve/compare structured events | repeated route failure with no new evidence |
| Active comp unavailable | re-query current Resolve context | selecting/creating/switching target data requires user authority |
| Group child discovery incomplete | compare `GetChildrenList`, parent attrs, saved settings | no stable hierarchy can be read |
| Tool identity unstable after LoadSettings | reacquire by stable name/path; add hierarchical identity | no unique/stable readback identity exists |
| Duplicate names in nested groups | implement hierarchical path/object identity | host exposes no distinguishable identity |
| Expanded flag does not persist | measure save/load/readback and UI refresh | no readback-verifiable expansion path exists |
| Group contents clipped | measure Size/Scale/Offset and child bounds | fit requires ungroup/destructive/UI-only guessing |
| Large graph slow | profile, reduce repeated scans/writes, keep algorithm iterative | Resolve becomes unstable before useful scale |
| Color graph absent on some items | classify item type/context and continue others | requested operation has no graph in any relevant scope |
| Color XY API absent | document blocker and continue non-XY Color tools | only that specific feature remains blocked |
| Undo unreliable | rely on explicit snapshots/rollback where safe; document | neither Undo nor explicit rollback is trustworthy |
| Save/reopen proof needed | defer until an explicitly safe save target is authorized | release gate requires persistence proof and no safe target exists |

---

# Autonomous mutation authority

Unless a newer user instruction narrows it, the current development mission may autonomously:

### Repository

- read all ResolveNodeKit files/history/PRs;
- create task branches;
- edit ResolveNodeKit code/tests/docs;
- commit/push task-branch work;
- update Draft PRs;
- add deterministic tests and diagnostic scripts;
- refactor only as needed to support current gates.

Do not merge to `main`, publish a release, force-push shared history, delete user branches, or rewrite unrelated work without explicit authority.

### Resolve/Fusion host

For a mission explicitly targeting the currently open data, bounded autonomous writes are limited to:

- Fusion node positions;
- GroupOperator expanded/collapsed display state;
- measured Group display geometry required for fit-to-contents;
- later commands only when that command's phase is explicitly being validated and its snapshot/readback/rollback contract is satisfied.

Do not autonomously:

- change media;
- change project/timeline identity;
- alter grades during Fusion layout work;
- modify node processing parameters/keyframes for layout purposes;
- ungroup/flatten nested graphs;
- save/close/reload/switch the user's project unless the mission explicitly authorizes it;
- change global Resolve keyboard shortcuts;
- install watchers/services/startup items.

---

# Checkpoint / resume contract

At every phase boundary or forced stop, record enough state to resume without chat history.

Minimum checkpoint fields:

```text
STATUS: PASS | CHECKPOINTED | BLOCKED_HOST | BLOCKED_API | BLOCKED_DATA | BLOCKED_SCOPE | BLOCKED_SAFETY | FAILED_ROLLBACK
PHASE: Pn / short name
REPO: 46slv/ResolveNodeKit
BRANCH: fresh-read value
HEAD: fresh-read value
PR: current PR and draft/open state
BASE: fresh-read main/base
TESTS: exact command + result
HOST: Resolve/Fusion version if known
TARGET: project / timeline / comp identity if host work occurred
OPENCODE: version / model / agent / session ID
MCP: connected target and structured tool-call evidence location/summary
PRE: graph/group/position signature summary
MUTATIONS: exact bounded writes attempted
POST: readback summary
ROLLBACK: not-needed | proven | failed
BLOCKER: exact unresolved condition, if any
NEXT: one smallest next gate
```

Do not use a prior checkpoint's SHA as authority on resume; it is a locator, then fresh-read.

---

# Evidence standard

## Offline evidence can prove

- deterministic layout logic;
- hierarchy projection logic;
- algorithmic non-overlap properties represented by tests;
- expected rollback behavior against mocks;
- parsers/settings transforms against fixtures.

## Offline evidence cannot prove

- current Resolve object availability;
- FlowView/UI semantics;
- GroupInfo viewport fit behavior;
- actual Undo integration;
- saved-project persistence;
- Color API availability in the user's installed version;
- host stability/performance.

## Host success requires

- structured MCP tool-use evidence;
- exact target identity;
- pre/post readback;
- invariant comparison;
- parent Codex verification independent of Muse's final narration.

---

# Near-term ordered backlog from current state

The parent should normally proceed in this order unless live evidence makes another gate smaller:

1. Host transport + active target snapshot.
2. Flat Tidy real-host canary.
3. Nested `Tidy + Expand Groups` on current real data.
4. Measure whether group frames clip children.
5. If clipped, implement measured fit-to-contents.
6. Repeat nested operation and prove idempotence/structure invariance.
7. Stress on the current large/ugly nested graph.
8. Add Align / Distribute / selection traversal helpers.
9. Add one carefully bounded rewiring command at a time.
10. Run Color read-only API map.
11. Add reversible Color helpers supported by readback.
12. Build unified menu/command surface.
13. Add clean installer/updater/uninstaller.
14. Optional PSD2Fusion post-generation integration.
15. Close first usable release gate.

If one item is independently blocked, checkpoint the blocker and advance to the next item that does not depend on it. Example: absence of Color XY positioning must not stop Fusion node utilities.

---

## Definition of useful autonomy

The objective is not to keep an agent busy indefinitely. Useful autonomy means:

- keep moving while the next action is reversible, bounded, and evidenced;
- turn failures into tests or documented API boundaries;
- stop before an irreversible or unobservable mutation;
- leave a precise checkpoint rather than asking the user questions that live state can answer;
- ask the user only when a new authority decision is genuinely required.
