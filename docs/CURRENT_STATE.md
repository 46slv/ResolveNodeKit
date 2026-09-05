# ResolveNodeKit current state

Updated: 2026-09-05 JST

This file is the short-lived operational state pointer. It must be refreshed when a meaningful phase changes. Live local Git/host state still outranks it.

## Program status

`CHECKPOINTED`

ResolveNodeKit is not globally blocked. Flat Fusion tidy has real-host evidence; nested hierarchy layout has offline evidence; visual Group expansion has a narrowed host-path blocker; several independent Fusion and Color lanes remain ready.

`MISSION_COMPLETE` is **not** reached. The user has explicitly required nested groups to remain groups, be openable, have their internals tidied, and show all contents. That requirement has not been waived.

## Remote locator at this audit

- repo: `46slv/ResolveNodeKit`
- main locator at project start: `a194d550a1eda50e3b18ae2da78e43251326c27b`
- task branch: `feat/bootstrap-nodekit-20260905`
- task-branch locator before orchestration-v2 audit: `3f43ebd1317cce35b7af91c1944e442a2f675e79`
- Draft PR: #1

These values are locators only. Fresh-read on resume.

## Reconciliation state — P0R CLOSED 2026-09-05

P0R is done. Local host-measured work was preserved on checkpoint commit `604b938` (`tmp/p0r-host-measured-fixes`, plus an off-repo patch backup), the task branch was fast-forwarded to `ce879bb`, and the fixes were merged as `9e8726c` with no code-side delta vs the checkpoint. `docs/GROUPS.md` was the only conflict: remote orchestration sections 1-7 kept, host measurement appended as section 8. Verified after merge: 29/29 unittest PASS (`PYTHONPATH=src python -m unittest discover -s tests`) + `compileall` PASS. Pushed to `feat/bootstrap-nodekit-20260905`; Draft PR #1 updated.

## Critical reconciliation state (historical)

A real-host run produced measured fixes locally but intentionally left them uncommitted at the time of that report:

- `src/resolve_node_kit/fusion/tidy.py`
- `src/resolve_node_kit/fusion/recursive_groups.py`
- `docs/GROUPS.md`
- new `tests/test_fusion_host_grid.py`

Reported local evidence after those fixes:

- 29/29 unittest PASS;
- `compileall` PASS;
- measured FlowView grid/readback behavior required snapped writes and a 0.1 comparison tolerance;
- measured bridge/runtime handling required an `OrderedDict` builtins guard around settings handling.

The remote branch later advanced with documentation/orchestration commits. Therefore the **first executable gate is reconciliation**, not another host experiment.

Required recovery:

1. inspect local worktree before any destructive Git action;
2. preserve the measured dirty work as a temporary local branch/checkpoint commit or patch;
3. fetch the current remote task branch;
4. integrate the host-measured changes onto the fresh remote head without losing either side;
5. rerun the full suite and compile checks;
6. commit/push the integrated task-branch work and update Draft PR #1.

Do not use `reset --hard`, `clean`, or blind checkout to erase the measured work.

## Measured host evidence

Historical host locator from the 2026-09-05 run:

- DaVinci Resolve Studio 21.0.3.7 GUI;
- project observed: `PSD2Fusion`;
- timeline observed: `Timeline 1`;
- active Fusion comp observed: 1107 tools;
- nested `GroupOperator`s observed: 31;
- original project was not saved and was reported restored/unmodified at run end.

Worker route was proven through OpenCode/Muse/Resolve MCP with structured events. Revalidate versions/session/target before reuse.

### Flat Tidy

Feature evidence: **HOST-MEASURED PASS on disposable canary with the local measured fixes**.

Covered:

- serial chain;
- BG + FG -> Merge;
- EffectMask branch;
- isolated node;
- connection invariance;
- second-run `moved=0`;
- one Undo restoring positions;
- fail-closed rollback.

Current code acceptance is still **pending reconciliation**, because the measured fixes are not yet proven integrated into the current remote task branch.

### Nested hierarchy layout

Feature evidence: **OFFLINE PASS / HOST CANARY PENDING**.

Per-scope hierarchy discovery/projection exists. The next host question is whether child node positions inside collapsed GroupOperators can be read/written safely without changing membership, connections, processing state, or group display state.

Target separate command/API:

- `tidy_nested_comp(...)`
- `scripts/Fusion/ResolveNodeKit_TidyNested.py`

Do not silently weaken `Tidy + Expand Groups` with a flag.

### Visual Group expansion

Feature status: **CURRENT SERIALIZED-SETTINGS PATH BLOCKED; RUNTIME-ACTION PATH UNRESOLVED**.

Measured on Resolve Studio 21.0.3.7:

- mutate `ViewInfo.Flags.Expanded = true`;
- `LoadSettings` returns `True`;
- immediate `SaveSettings` readback does not retain the expanded state;
- same outcome with/without Undo and on empty/populated groups;
- `Size`/`Scale`/`Offset` unchanged;
- no usable `Expanded` readback in `GetAttrs`;
- attempted guessed FlowView expansion actions did not establish a working path.

Do not repeat this exact `LoadSettings(Expanded=true)` hypothesis without new evidence.

Next research hypothesis: find a readback-verifiable runtime Expand/Collapse command/action equivalent to the real Fusion UI operation. Blind keystrokes or a new desktop automation stack are not authorized merely to bypass the blocker.

### Fit to contents

Status: **DEPENDENT ON VISUAL EXPANSION**.

Do not infer `GroupInfo.Size` / `Scale` / `Offset` formulas from `.setting` examples. Measure only after a real runtime-expanded group can be produced and observed.

### Large graph stress

Status: **READY AFTER RECONCILIATION + NESTED-TIDY CANARY**.

Do not transfer the entire 1107-tool graph through MCP if that times out. Compute compact canonical signatures/hashes inside Resolve/Fusion and return only counts/hashes/timing plus focused mismatch details.

### Fusion low-risk operations

Status: **INDEPENDENT READY LANE after Flat Tidy closeout**.

Order: align/distribute -> selection traversal -> selected/component tidy -> safe group display helpers supported by host evidence.

### Color

Status: **INDEPENDENT READ-ONLY LANE READY**.

Run current-host capability mapping first. Only add mutations with observable postconditions/readback. Lack of Color XY layout API blocks that specific feature, not the entire Color lane.

## Ready queue

The parent orchestrator should choose the first ready item whose prerequisites are satisfied:

1. `P0R` — DONE (see Reconciliation state above; next: push + PR #1 update, then P2C).
2. `P2C` — DONE (HOST-PASS 2026-09-05, see section above).
3. `P3A` — canary PASS + `tidy_nested_comp` implemented offline (`9b90ea9`); host validation of the real command is next.
4. `P5` — stress `Tidy Nested` on a duplicate of the large 1107-tool / 31-group composition using compact in-host evidence.
5. `P6` — low-risk Fusion node operations.
6. `P8` — Color read-only capability map.
7. `P3B` — visual expansion runtime-action research can run whenever a bounded, readback-verifiable path is available.
8. `P4` — fit-to-contents only after P3B succeeds.

Independent ready lanes should continue when another feature is blocked.

## Program completion semantics

- A phase may return `BLOCKED_HOST` / `BLOCKED_API` locally.
- If another authorized independent gate is ready, the overall program remains `CHECKPOINTED` and continues.
- A whole-run `BLOCKED_*` terminal state is appropriate only when no authorized ready gate remains, a hard safety stop occurs, or the next action needs new user authority.
- `MISSION_COMPLETE` requires the mission-critical visual nested-group requirement to pass or an explicit user scope change/waiver.

## Primary evidence checkpoint

Read `docs/checkpoints/2026-09-05-host-group-expansion-blocker.md` for the detailed measured host run. Do not treat its historical target/session IDs as current bindings.

## P2C flat-Tidy host closeout — PASS 2026-09-05

Worker route: OpenCode CLI 1.18.29 -> `opencode-go/muse-spark-1.3-contributor` (agent `build`) -> davinci-resolve MCP 2.203.0 -> Resolve Studio 21.0.3.7. Structured events: `%TEMP%\rnk-p2c\events2.jsonl` (first attempt died on a file-write permission denial; second attempt forbade worker file writes and completed).

Target: project PSD2Fusion, disposable timeline RNK_P2C (created, verified, deleted afterwards), Timeline 1 restored current with timeline list exactly [Timeline 1] and all 5 Timeline 1 comps read back `Modified=false`. No project save.

Canary comp (10 tools): serial BG->Blur->Merge, BG+FG->Merge, EllipseMask EffectMask branch, isolated node. Repo HEAD (`1c2ca6f`) `tidy_comp` loaded in-process via `run_inline`:

- `TIDY_RESULT nodes=10 edges=5 moved=10`; edge list pre == post (5/5 identical); tool count 10 -> 10;
- `GRID_ALL_OK: True` — all 10 readbacks within grid tolerance incl. mask frame offsets;
- `TIDY_RUN2 moved=0` (idempotent);
- `UNDO_RESTORE: True` — post-Undo positions exactly equal pre-tidy snapshot;
- Rollback: Undo path proven this run; fail-closed mismatch rollback proven on identical code in the prior run.

Flat Tidy is HOST-PASS on the canonical branch and no longer blocks independent node-tool work. Save/reopen persistence remains a separate gate (must not force-save the user project).
## P3A collapsed-group child-position canary — PASS 2026-09-05

Disposable run on timeline RNK_P3A (deleted afterwards; Timeline 1 restored, all comps `Modified=false`, no save). Full evidence: `docs/checkpoints/2026-09-05-p3a-collapsed-child-canary.md`, structured events `%TEMP%\rnk-p3a\events.jsonl`.

Key results on Studio 21.0.3.7: `AddTool('GroupOperator')` works; `ParentTool` assignment does not stick; settings-assembled 2-level nesting is real (children/parent agree); child writes inside collapsed groups read back exactly; membership/geometry/display state unchanged; one Undo restores all positions. Canary nodes were unconnected, so connected-nested proof moves to P5.

Ready next: implement `tidy_nested_comp` + `ResolveNodeKit_TidyNested.py` (repo only), then P5 stress, P6, P8. P3B expansion research stays the mission-critical track.
## Tidy Nested implementation — OFFLINE PASS 2026-09-06 (`9b90ea9`)

`tidy_nested_comp(...)` added to `src/resolve_node_kit/fusion/recursive_groups.py` (+ export, + `scripts/Fusion/ResolveNodeKit_TidyNested.py`, + `tests/test_fusion_nested.py`). Design: same per-scope snapshot/layout/write/readback/rollback machinery as `tidy_groups_comp` but calls no settings API at all, so collapsed/expanded display state cannot be disturbed through this path; post-write hierarchy + edge re-verification included. Offline: 35/35 unittest PASS + `compileall` PASS. Host gate still pending: run the real `tidy_nested_comp` against a collapsed disposable group (membership/connections/display-state invariance, second-run stability, Undo).
## Tidy Nested host validation round 1 — SECOND-RUN DRIFT FOUND AND FIXED OFFLINE

Disposable RNK_P3AVAL run (deleted afterwards; Timeline 1 restored, comps `Modified=false`, no save). Structured events `%TEMP%\rnk-p3aval\events.jsonl`. Run1 `moved=7` with membership/connections/collapsed-state/geometry all unchanged; run2 `moved=1` (InnerG y 3.009 -> 4.009); run3 `moved=0`. Single-Undo caveat: each command call is its own Undo event, so reverting two runs needs two Undos (expected, not a defect); full rollback proven.

Root cause (verified against structured events + offline replica): the shared layout core orders rows by input positions, and host readback offsets (+0.001/+0.009) perturb the anchor and row order, so one step from tied PRE is not a fixed point. Fix (`f1c2982`): `tidy_nested_comp` iterates `_layout_step` to a fixed point (cap 16) before writing once; `tidy_groups_comp` keeps the single step (no measured failure there). Regression test replicates the exact host drift offline (d1 InnerG (-0.5,3.0) vs d2 (-0.5,4.0)) and proves the fixed point holds under offset perturbation. Offline: 36/36 PASS + `compileall` PASS. Host re-validation of the fixed command is next.
## Program status override — BLOCKED_HOST (Resolve hang) 2026-09-06

`BLOCKED_HOST` for all host lanes: Resolve PID 27928 `Responding=false` (parent-side read-only check), MCP `Not connected`, after a nested-Paste timeout on disposable RNK_P3B2. Worker stopped per hard-stop rules (`%TEMP%\rnk-p3aval2\events.jsonl`). Timeline 1 never touched; no save issued; repo untouched. Full evidence: `docs/checkpoints/2026-09-06-resolve-hang-p3aval2.md`.

Do NOT kill/restart the user Resolve process and do NOT launch host workers until the user confirms their session is healthy. On recovery: rebind -> verify Timeline 1 intact -> delete RNK_P3B2* -> restore Timeline 1 current -> verify list [Timeline 1] + comps `Modified=false` -> resume tidy-nested re-validation (`f1c2982`), then P5/P6/P8/P3B.