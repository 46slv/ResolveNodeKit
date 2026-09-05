# Orchestration audit — 2026-09-05

Purpose: verify whether the repository documentation could actually drive a long autonomous Codex/OpenCode/Resolve run to useful completion without repeatedly stopping on the already-measured Group expansion blocker.

## Inputs reviewed

- `AGENTS.md`
- `README.md`
- `docs/ORCHESTRATION.md`
- `docs/HOST_VALIDATION.md`
- `docs/GROUPS.md`
- `docs/checkpoints/2026-09-05-host-group-expansion-blocker.md`
- Draft PR #1 state
- current remote task-branch state
- durable Codex prompt/orchestration guidance from the user's Coding Intelligence library

## Findings before v2

### 1. Linear dependency on visual expansion could deadlock the program

Old P3/P4/P5 wording still assumed all target groups could be expanded and fitted. Real-host evidence had already disproven the serialized `Expanded=true` write path. As written, one feature-local host blocker could prevent large-graph stress and downstream work that does not actually depend on visual expansion.

Correction: split `P3A Tidy Nested` from `P3B visual expansion`, make P5 depend on P3A rather than P3B/P4, and use a dependency graph rather than fixed phase order.

### 2. Program-level vs feature-level blocker semantics were ambiguous

A previous real-host report ended overall `BLOCKED_HOST` even though Flat Tidy passed and independent Fusion/Color work remained.

Correction: blockers are lane-local by default. If an independent authorized gate remains, overall program status is `CHECKPOINTED`. Whole-run `BLOCKED_*` is terminal only when no ready gate remains or a hard safety/authority boundary is reached.

### 3. The user’s visual nested-group requirement could be accidentally weakened

Allowing a flag such as `require_expansion=False` on `Tidy + Expand Groups` would make the command name and acceptance misleading.

Correction: keep strict expansion fail-closed and define separate `Tidy Nested`. `MISSION_COMPLETE` still requires real visual nested-group access unless the user explicitly changes scope.

### 4. Local measured fixes vs newer remote documentation had no mandatory reconciliation gate

Real-host fixes were reported dirty/uncommitted while remote task branch later advanced. A new agent could pull/reset and lose the only measured implementation fixes.

Correction: `P0R` is now the first executable gate; inspect/preserve local dirty work before fetch/rebase/cherry-pick. `reset --hard`/`clean` cannot be the first response.

### 5. Large-graph validation could repeat the known transport timeout

The current real comp has about 1107 tools; a remote full snapshot timed out. Old orchestration simply asked to stress large graphs.

Correction: add an in-host compact evidence protocol using canonical counts/hashes/timing and focused mismatch expansion instead of serializing the whole graph through MCP.

### 6. Durable and volatile state were mixed

`AGENTS.md` contained a stale current-next-gates list. Long-term rules and current operational state need different owners.

Correction: add `docs/CURRENT_STATE.md`; keep `AGENTS.md` as a short entrypoint/map and `ORCHESTRATION.md` as durable dependency/authority policy.

### 7. Commit authority was inconsistent with actual project authorization

The user has authorized work in ResolveNodeKit, and the existing orchestration already allows task-branch commits/pushes/Draft PR updates. A host run nevertheless left accepted measured fixes dirty because commit authority was treated as absent.

Correction: make current repo authority explicit: task-branch commit/push and Draft PR update are autonomous; main merge/release/force-push/unrelated cleanup are not.

### 8. Runtime Group expansion hypothesis needed to change

Host evidence shows serialized settings accept a write call but discard expanded state on immediate readback. Repeating that path is not evidence-driven.

Correction: mark the serialized-settings path disproven and move research to a bounded runtime Expand/Collapse action path only when deterministic targeting and independent readback are available. Blind keystrokes/new desktop automation are not authorized as a shortcut.

## Result

The v2 documentation is designed to be finishable in the following sense:

- it can continue useful independent work after a lane-specific blocker;
- it preserves a mission-critical unresolved requirement instead of declaring false completion;
- it defines a concrete reconciliation gate for local/remote divergence;
- it defines evidence transport that scales to the known large graph;
- it gives a later Codex session one operational current-state file and one durable orchestration contract;
- it distinguishes `USABLE_BETA` from `MISSION_COMPLETE`.

This does not guarantee the host exposes every desired API. It guarantees the orchestration can prove a supported path, classify a real API blocker without looping, continue independent work, and avoid falsely declaring the mission complete.
