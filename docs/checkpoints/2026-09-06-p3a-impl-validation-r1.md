# Host checkpoint - Tidy Nested implementation validation round 1 - 2026-09-06

Status: `CHECKPOINTED` (feature-local drift found, fixed offline, re-validation pending). Flat Tidy HOST-PASS stands; strict expansion still blocked on the known path.

Worker route: OpenCode CLI 1.18.29 -> model flag `opencode-go/muse-spark-1.3-contributor` (agent `build`) -> davinci-resolve MCP 2.203.0 -> Resolve Studio 21.0.3.7. Structured events: `%TEMP%\rnk-p3aval\events.jsonl` (175 lines). Repo HEAD under test: `89dbbcc`.

## Target

- Project PSD2Fusion, disposable timeline RNK_P3AVAL (+ one archived variant, both deleted afterwards). Timeline list before and after: exactly [Timeline 1]. No project save.
- Timeline 1 restored current, page fusion; all 5 Timeline 1 comps read back `Modified=false` afterwards.
- Repo untouched by worker (`git status` clean).

## Measured results (from structured tool-use events, independently verified)

- Nested 2-level disposable case: outer group with inner group + chain siblings, both collapsed.
- Run1 of repo `tidy_nested_comp`: `node=8 edge=3 moved=7`; edge list pre == post (3/3); tool count 8 -> 8; both groups still `Expanded=nil` with identical `Size`/`Scale`/`Offset`; sampled params intact.
- Run2: `moved=1` (InnerG y 3.009 -> 4.009). Run3: `moved=0`. Strict second-run stability NOT met.
- Rollback: full position rollback proven. Undo note: each command call is one Undo event, so reverting run1+run2 took two Undos; second Undo restored all 8 positions to snapshot exactly. This is correct behavior, not a defect.
- Cleanup verified: RNK_P3AVAL + archived variant deleted; Timeline 1 current with `Modified=false` on all comps.

## Root cause

The shared layout core (`core/layout.py`) orders rank rows by input Y (`_stable_key`). Run1 PRE had every child at the identical pasted position, so rows fell back to name order; host readback offsets (+0.001 X / +0.009 Y) then perturbed the anchor and row order on run2, moving InnerG one grid unit. Offline replica with identical PRE plus offsets reproduces exactly: d1 InnerG (-0.5, 3.0) vs d2 (-0.5, 4.0).

## Fix (offline, `f1c2982`)

- `tidy_nested_comp` now iterates `_layout_step` to a fixed point (cap 16) and writes once, keeping a single Undo event.
- `_layout` single-step semantics unchanged for `tidy_groups_comp` (no measured failure there).
- Regression test replicates the exact host drift (asserts single-step instability under offsets) and proves the fixed point holds under offset perturbation plus second-run `moved=0`.
- Offline: 36/36 unittest PASS + `compileall` PASS.

## Next

Host re-validation of the fixed command on a fresh disposable nested case: run1 settles directly, run2 `moved=0`, Undo restores, cleanup verified.
