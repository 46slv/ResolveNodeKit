# ResolveNodeKit current state

Updated: 2026-09-06 JST

This file is the short-lived operational pointer for the next Codex run. Live local Git/worktree, remote Git/PR, and live Resolve state outrank it. Historical detail belongs in `docs/checkpoints/`.

## Program status

`BLOCKED_HOST`

Reason: the current DaVinci Resolve process became persistently unresponsive during a disposable nested-group validation run. Parent-side read-only observation reported `Responding=false`; Resolve MCP reported `Not connected`. Per the hard-stop contract, no kill/restart was attempted because the active user project may contain unsaved state.

This is a **host-recovery boundary**, not a code failure and not `MISSION_COMPLETE`.

Do not launch further Resolve/OpenCode host workers until the user confirms the Resolve session is healthy.

## Canonical repo state

- repo: `46slv/ResolveNodeKit`
- task branch: `feat/bootstrap-nodekit-20260905`
- current remote HEAD locator: `3f3d5c27b9d896accd80917cf8e17bf0f17991e9`
- Draft PR: #1, open/draft
- reported worktree at stop: clean, remote in sync
- current offline suite at stop: 36/36 unittest PASS + `compileall` PASS

Treat these as locators and fresh-read on resume.

## Closed gates

### P0R — reconciliation: PASS

The host-measured grid/readback/settings fixes were preserved, reconciled with the newer remote orchestration branch, tested, committed, and pushed.

### P2C — Flat Tidy host closeout: PASS

Real Resolve Studio 21.0.3.7 disposable validation established:

- serial / Merge / EffectMask / isolated-node handling;
- connection invariance;
- measured FlowView grid/readback handling;
- second-run `moved=0`;
- Undo restoring positions;
- fail-closed rollback behavior.

Flat Tidy is HOST-PASS on the canonical task branch.

### P3A collapsed-child position canary: PASS

A real collapsed nested GroupOperator canary proved that child positions can be changed/read back without changing hierarchy, group display state, connections, or processing state, and Undo restores positions.

## Tidy Nested implementation

`tidy_nested_comp(...)` and `scripts/Fusion/ResolveNodeKit_TidyNested.py` are implemented.

Host validation round 1 found a real second-run settle drift:

- run1 moved=7;
- run2 moved=1 (`InnerG` y settled by one grid row);
- run3 moved=0;
- hierarchy/connections/collapsed-state/geometry remained invariant.

Root cause was reproduced offline: layout row ordering depends on input Y and measured host readback offsets can perturb anchor/order.

Fix: `f1c2982` makes `tidy_nested_comp` iterate `_layout_step` to a fixed point (cap 16) before one host write. `tidy_groups_comp` was intentionally left unchanged because no measured failure exists there.

Regression coverage encodes the measured drift. Current offline result: 36/36 PASS + `compileall` PASS.

### Tidy Nested host re-validation

Status: **PENDING ONLY BECAUSE HOST HUNG**.

A second disposable validation (`RNK_P3B2`) hung during nested Paste before the fixed command could be revalidated. This is not evidence that the fixed command caused the hang; the hang occurred during disposable setup/Paste and must be treated as an unresolved host event.

## Current host blocker

Historical host locator from the stopped run:

- Resolve Studio 21.0.3.7
- process PID observed: 27928
- parent readback: `Responding=false`
- MCP: `Not connected`
- disposable timeline: `RNK_P3B2` may still exist in unknown partial state
- Timeline 1 was not intentionally modified
- no project save was issued

Detailed evidence: `docs/checkpoints/2026-09-06-resolve-hang-p3aval2.md`.

### Human boundary

The user must first make Resolve healthy. They may restart Resolve themselves if necessary. Do not kill/restart the process autonomously.

## Mandatory recovery sequence after user confirmation

Before resuming product work:

1. fresh-read local/remote Git and verify clean canonical task branch;
2. run `opencode mcp list` and re-establish the proven OpenCode/Muse/Resolve MCP route;
3. bind the actual current Resolve project/timeline/comp from live state; do not assume historical identity;
4. verify the original Timeline 1 data is intact before cleanup;
5. locate `RNK_P3B2*` disposable artifacts only if they still exist;
6. inspect enough state to distinguish safe disposable cleanup from user data;
7. delete only confirmed ResolveNodeKit disposable artifacts;
8. restore Timeline 1 as current if necessary;
9. verify final timeline list / current target and that original comps are not unexpectedly modified;
10. only then resume host validation of the fixed `tidy_nested_comp`.

If target identity or disposable ownership cannot be proven, stop `BLOCKED_SAFETY` rather than guessing cleanup.

## Ready queue after host recovery

### R1 — Tidy Nested fixed-command re-validation

Re-run the smallest disposable nested-group validation using the current fixed code. Acceptance:

- run1 reaches intended layout;
- run2 `moved=0` / identical quantized position hash;
- hierarchy, membership, connections, processing-state evidence, and collapsed/expanded display state unchanged;
- Undo/rollback understood;
- disposable cleanup complete;
- original Timeline 1 remains untouched/unmodified.

### P5 — large nested stress

After R1 PASS, exercise a duplicate of the large real composition using `docs/EVIDENCE_PROTOCOL.md`. Do not serialize all ~1100 tools through MCP. Compute compact in-host counts/hashes/timing and expand only mismatches.

### P6 — low-risk Fusion operations

After host recovery, independent of visual Group expansion: Align, Distribute, selection traversal, selected/component tidy, etc., each with readback and Undo/rollback contracts.

### P8 — Color read-only capability map

Independent read-only lane after host recovery.

### P3B — visual Group expansion research

Mission-critical but independent of Tidy Nested. The serialized `LoadSettings(Expanded=true)` path is disproven on the measured host. Investigate only a deterministic/readback-verifiable runtime Expand/Collapse action path. No blind keystrokes, new desktop automation stack, global shortcut mutation, ungrouping, or flattening merely to bypass this blocker.

### P4 — fit to contents

Runs only after real runtime visual expansion is proven.

## Visual Group requirement

The explicit mission remains:

- keep nested groups as GroupOperators;
- actually open nested groups in the runtime/UI sense;
- tidy their internals;
- make all contents visible.

`Tidy Nested` is a useful independent feature but does not satisfy visual expansion. `MISSION_COMPLETE` cannot be declared until visual nested-group access is proven or the user explicitly changes scope.

## Status semantics for the next run

- While Resolve remains unhealthy: whole current run = `BLOCKED_HOST`.
- Once the user restores Resolve and host transport is available: return to the dependency-driven orchestration in `docs/ORCHESTRATION.md`.
- A later feature-local blocker must not stop independent ready lanes.
- Any ambiguous cleanup/write without independent readback is a hard stop.

## Required reading on resume

1. live local Git/worktree + remote state
2. `AGENTS.md`
3. this file
4. `docs/ORCHESTRATION.md`
5. `docs/EVIDENCE_PROTOCOL.md`
6. `docs/HOST_VALIDATION.md`
7. `docs/GROUPS.md`
8. `docs/checkpoints/2026-09-06-resolve-hang-p3aval2.md`
9. other relevant checkpoints only as needed

## R1 — Tidy Nested fixed-command re-validation: PASS 2026-09-06

Recovery executed first (fresh bind, Timeline 1 intact, RNK_R1* deleted, list [Timeline 1], no save). Fresh disposable RNK_R2 (deleted afterwards): run1 `moved=7` settling directly on the fixed point, run2 `moved=0 identical=True`, membership/connections/display-state/params invariant, Undo restoring all 8 positions exactly. Evidence: `docs/checkpoints/2026-09-06-tidy-nested-r1-pass.md`, events `%TEMP%\rnk-recover2\events.jsonl`. `Tidy Nested` is HOST-PASS. Next: P5 large-stress, P6 low-risk ops, P8 Color map, P3B expansion research.