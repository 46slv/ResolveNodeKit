# Host checkpoint — Group expansion blocker — 2026-09-05

Status: `BLOCKED_HOST` for programmatic GroupOperator expansion. Flat Fusion tidy is host-validated on a disposable canary.

This checkpoint captures a Codex/OpenCode/Muse real-host run. On resume, fresh-read live Git and host state; values below are evidence/locators, not permanent authority.

## Measured host

- DaVinci Resolve Studio 21.0.3.7 GUI
- project observed: `PSD2Fusion`
- timeline observed: `Timeline 1`
- active Fusion composition: 1107 tools
- nested `GroupOperator` count: 31
- project was not saved by the validation run
- disposable/duplicate test artifacts were removed and the original timeline/comp was left unmodified (`Modified=false` reported)

## Worker route evidence

Measured worker route:

`Codex -> OpenCode CLI 1.18.29 -> build agent -> opencode-go/muse-spark-1.3-contributor -> davinci-resolve MCP -> Resolve`

Structured event logs were reported under `%TEMP%\rnk-worker` (`probe.jsonl`, `main2.jsonl`, `cont.jsonl`). Exact OpenCode session IDs from the run must be treated as historical locators and revalidated if reused.

## Flat Tidy host result

PASS on a disposable Fusion graph covering:

- BG + FG -> Merge
- serial chain
- EffectMask branch
- isolated node
- connection invariance
- second-run idempotence (`moved=0`)
- one Undo restoring positions
- fail-closed rollback behavior

Two host-measured implementation corrections were produced locally during that run:

1. FlowView grid/readback handling: X snaps to 0.5 units, Y to integer units in the measured cases; observed readback offsets required snapped writes plus a 0.1 comparison tolerance.
2. `SaveSettings` bridge handling: an `OrderedDict` builtins guard was required in the measured worker/runtime path.

Nine regression tests were added locally and the reported local suite became 29/29 PASS with `compileall` PASS.

### Important repository reconciliation note

At the end of the host run these fixes were **uncommitted local work**:

- modified `tidy.py`
- modified `recursive_groups.py`
- modified `docs/GROUPS.md`
- new `tests/test_fusion_host_grid.py`

The remote task branch has since advanced with orchestration/documentation commits. Therefore the next Codex run must not reset or overwrite the local dirty state. First preserve it as a patch or checkpoint commit on a temporary local branch, fetch the current remote branch, then rebase/cherry-pick the measured fixes onto the fresh remote head and rerun the full suite before pushing.

## Group expansion host result

The expansion path was tested on a duplicate of the real graph and on both empty and populated groups.

Measured behavior:

- mutate `ViewInfo.Flags.Expanded = true` in settings
- call `LoadSettings`
- host returns success (`True`)
- immediate `SaveSettings` readback does **not** retain `Expanded=true`
- same result with and without Undo
- same result on an empty group and a seven-child group
- `Size`, `Scale`, and `Offset` did not change
- `GetAttrs` exposed no usable `Expanded` state
- attempted FlowView expansion-style actions returned false/unavailable

The current `tidy_groups_comp` fail-closed behavior is therefore correct: it refuses to claim expansion when host readback disproves it.

## Decision

Keep the strict `Tidy + Expand Groups` contract fail-closed. Do not weaken its meaning with a boolean that silently turns expansion off.

Add a **separate command/API** for recursive hierarchy-preserving tidy without requiring visual expansion, tentatively:

- API: `tidy_nested_comp(...)`
- script: `ResolveNodeKit_TidyNested.py`

This command may proceed only after a real-host canary proves that positions of children inside collapsed GroupOperators can be read/written without changing membership, connections, parameters, or group display state. If that works, it becomes an independent usable feature while expansion remains blocked.

## New expansion hypothesis

Blackmagic Fusion manuals document the runtime expand/collapse operation as selecting a Group and invoking the UI Expand/Collapse command (`Ctrl-E` on Windows), after which the group becomes a separately pannable/scalable/resizable subflow.

This makes runtime UI expansion a distinct hypothesis from serialized `ViewInfo.Flags.Expanded` settings.

Next investigation order:

1. inspect the current OpenCode MCP list for any already-configured, bounded UI/keyboard command path;
2. inspect current Fusion scripting/runtime surfaces for a named Expand/Collapse command or action that can be invoked and read back;
3. only if an already-authorized UI automation path exists, canary: select one disposable Group -> invoke the equivalent of Ctrl-E -> verify actual visual/subflow state and hierarchy invariance -> Undo/cleanup;
4. do not install a new desktop automation stack, alter global shortcuts, or send blind keystrokes merely to bypass this blocker without a separate authority decision.

If no readback-verifiable UI/action route exists, classify visual expansion as `BLOCKED_API` while continuing recursive tidy and other independent Fusion features.

## Next ordered gates

1. **P0 reconciliation** — recover the dirty host-measured fixes and integrate them onto the fresh remote task-branch head without losing either side.
2. **P2 closeout** — rerun full offline suite and a minimal flat-Tidy host canary with the integrated grid/readback fixes.
3. **P3A recursive-tidy-only canary** — prove nested child SetPos while groups remain grouped/collapsed; if safe, implement the separate command and stress it on a duplicate.
4. **P3B expansion action research** — investigate actual runtime UI/action expansion path; do not keep retrying `LoadSettings(Expanded=true)` unless new evidence changes the hypothesis.
5. **P5 stress** — after P3A passes, exercise the 1107-tool / 31-group duplicate with recursive tidy-only; snapshot structural signatures and measure runtime.
6. Continue independent P6 low-risk Fusion node operations even if P3B remains blocked.
7. Color remains independent and may proceed through read-only capability mapping.

## Stop criteria specific to this blocker

Immediate stop for the current host sequence if:

- group membership changes;
- any connection changes;
- processing parameters/keyframes/media/grade state changes during layout/display work;
- target project/timeline/comp identity changes unexpectedly;
- a UI keystroke/action is ambiguous and has no independent readback;
- rollback cannot be proven.

Do **not** stop the whole project because visual group expansion is unavailable. Checkpoint the specific blocker and continue independent node-layout/selection/inspection work.
