# ResolveNodeKit current state

Updated: 2026-09-06 JST

This file is the short-lived operational pointer for the next Codex run. Live local Git/worktree, remote Git/PR, and live Resolve state always outrank it. Historical detail belongs in `docs/checkpoints/`.

## Program status

`CHECKPOINTED`

The Resolve host recovered successfully and was clean/responsive at the end of the latest run. ResolveNodeKit is not globally blocked and is not `MISSION_COMPLETE`.

The mission-critical unresolved requirement remains runtime visual nested-group access: groups must remain GroupOperators, actually open in the Fusion runtime/UI sense, have their internals tidied, and show all contents.

## Canonical repo state

- repo: `46slv/ResolveNodeKit`
- task branch: `feat/semantic-arrange-v1-20260906` (implements Semantic Arrange v1; design docs merged from PR #2)
- Draft PR: #1 (bootstrap) plus #5 (Semantic Arrange v1, stacked on the bootstrap branch), both open/draft
- branch locator immediately before this state normalization: `f974730f5952a6376feb443d482bbb571e71d59e`
- reported worktree at latest run end: clean, remote in sync
- offline suite: 63/63 unittest PASS + `compileall` PASS (36 baseline plus 27 semantic-arrange)

Fresh-read all locators on resume.

## Closed / proven gates

### P0R — reconciliation: PASS

Host-measured local fixes were preserved, reconciled with the newer remote orchestration work, tested, committed, and pushed.

### P2C — Flat Tidy: HOST-PASS

Real Resolve Studio 21.0.3.7 disposable validation proved serial / Merge / EffectMask / isolated-node handling, connection invariance, measured FlowView grid/readback handling, second-run `moved=0`, Undo restoring positions, and fail-closed rollback.

### P3A collapsed-child canary: PASS

A real collapsed nested GroupOperator canary proved child positions can be changed/read back without changing hierarchy, connections, processing state, or collapsed/expanded display state. Undo restores positions.

### R1 — `Tidy Nested` fixed-command re-validation: HOST-PASS

`tidy_nested_comp(...)` and `scripts/Fusion/ResolveNodeKit_TidyNested.py` are implemented.

A prior host validation found a second-run settle drift (`moved=7 -> 1 -> 0`). The cause was reproduced offline and fixed by iterating `_layout_step` to a fixed point before one host write.

Latest real-host re-validation after Resolve recovery:

- run1 `moved=7`, reaching the fixed point directly;
- run2 `moved=0`, identical positions;
- membership unchanged;
- connections unchanged;
- collapsed/display state unchanged;
- sampled processing state unchanged;
- Undo restored all positions exactly;
- disposable deleted;
- Timeline 1 remained untouched/unmodified;
- no project save.

Evidence: `docs/checkpoints/2026-09-06-tidy-nested-r1-pass.md`.

`Tidy Nested` is HOST-PASS.

### P8 — Color read-only capability map: PASS

Measured on Resolve Studio 21.0.3.7 with zero host writes:

- per-item Color Graphs available on current Timeline 1 items, with one node in the measured context;
- timeline-level Graph available but empty;
- no Color groups exist in the current project, so group-graph behavior remains context-unexercised rather than disproven;
- Graph surface includes LUT/cache/enabled/label/tools/grade-related operations;
- physical Color-node XY position API is absent in the measured callable surface.

Consequence: future Color operations may use readback-verifiable enable/cache/LUT/etc. surfaces, but must not claim physical XY layout.

## Current feature-local blocker

### P5 — large nested stress: `BLOCKED_HOST` (transport only)

The large real composition contains approximately 1107 tools and 31 nested GroupOperators in the measured context.

Latest P5 attempt:

- disposable duplicate was verified identical before the evidence walk;
- Timeline 1 remained untouched;
- no product mutation ran;
- no project save;
- Resolve remained responsive;
- one long in-host evidence walk timed out at the MCP layer (`-32001`), retry then lost/deregistered the bridge (`-32000` / tools unavailable).

This is not evidence that `Tidy Nested` fails at large graph scale. It is a transport-envelope failure: the call was too long for the MCP/bridge path.

Evidence: `docs/checkpoints/2026-09-06-p5-transport-block.md`.

### Cleanup after P5: PASS

A short/light worker run removed stale ResolveNodeKit-owned timelines with exact identity + confirmation guardrails. Final host state was verified:

- timeline list exactly `[Timeline 1]`;
- current timeline `Timeline 1`;
- original comps `Modified=false`;
- no save;
- Resolve healthy/responsive.

## P5 retry strategy

Do not retry the same full 1107-tool single-call walk.

Use `docs/EVIDENCE_PROTOCOL.md` and determine a transport-fitting envelope first:

1. start with a medium real/disposable subtree or bounded subset;
2. keep each Resolve/MCP call short;
3. compute compact counts/hashes locally/in-host;
4. return only compact evidence per chunk;
5. measure elapsed time and successful chunk size;
6. increase scope gradually;
7. combine chunk evidence deterministically on the parent side or via bounded in-host aggregation;
8. only mutate after a pre-evidence strategy can complete reliably;
9. never repeat a materially identical full-graph timeout path.

The next P5 attempt should first establish a stable transport envelope, then run pre -> Tidy Nested -> post -> second-run evidence within that envelope.

## Mission-critical visual Group expansion — P3B OPEN

The serialized-settings hypothesis is disproven on Resolve Studio 21.0.3.7:

`SaveSettings -> Expanded=true -> LoadSettings(True) -> SaveSettings`

does not retain runtime expanded state.

Strict `Tidy + Expand Groups` remains fail-closed and must never silently degrade to `Tidy Nested`.

Next research hypothesis: a deterministic/readback-verifiable runtime Expand/Collapse action/command path.

Do not use blind keystrokes, install a new desktop automation stack, mutate global shortcuts, ungroup, or flatten merely to bypass this blocker without new authority.

P4 fit-to-contents remains gated on P3B PASS.

## Ready queue

Choose the smallest ready gate from live evidence rather than blindly following numeric order.

1. **P5-retry** — establish a transport-fitting chunk size on a medium scope, then scale bounded evidence toward the large graph.
2. **P6** — low-risk Fusion operations: Align / Distribute / selection traversal / selected-component tidy, each with readback and Undo/rollback contracts.
3. **P3B** — runtime visual Group Expand/Collapse action research; mission-critical but independent of P5/P6.
4. **P9** — Color reversible helpers based only on P8-observed readback surfaces (enable/cache/LUT/etc.); no XY layout claim.
5. **P4** — fit-to-contents only after P3B PASS.

A feature-local blocker must be checkpointed, then another independent ready lane should continue if authorized.

## Program completion semantics

- Current overall status: `CHECKPOINTED`.
- `USABLE_BETA` may eventually be checkpointed with accurately documented non-critical limitations.
- `MISSION_COMPLETE` is not allowed while the explicit visual nested-group requirement is unresolved, unless the user explicitly changes/waives that requirement.
- A whole-run `BLOCKED_*` should be used only when no authorized ready gate remains, host/safety conditions block all useful work, or new user authority is required.

## Required reading on resume

1. live local Git/worktree + remote state
2. `AGENTS.md`
3. this file
4. `docs/ORCHESTRATION.md`
5. `docs/EVIDENCE_PROTOCOL.md`
6. `docs/HOST_VALIDATION.md`
7. `docs/GROUPS.md`
8. `docs/checkpoints/2026-09-06-tidy-nested-r1-pass.md`
9. `docs/checkpoints/2026-09-06-p5-transport-block.md`
10. older checkpoints only as needed

## Semantic Arrange v1 status (gate 1 nested PASS, gate 2 selection PASS 2026-09-06 JST)

Flat-fixture preserve-mode Arrange is HOST-PASS (canaries 1-2, evidence in `docs/checkpoints/2026-09-06-semantic-arrange-a8-canary.md`). 
A host-found anchor drift was fixed (canonical backbone-head anchor plus snapped origin) with regression tests that fail before and pass after. 
Nested-Group preserve proof PASSED via the R1-recipe SaveSettings-derived Paste envelope (see gate 1 checkpoint); the hand-written single-Paste shape stays banned (single 8-tool Paste times out with `-32001` and drops session tools; retry with a split envelope, never identically). 
Host is clean: timelines exactly `[Timeline 1]`, current Timeline 1, all comps unmodified, no save.

Adjusted ready queue: (1) DONE nested preserve; (2) DONE selection-only (SetActiveTool setter proven, GetToolList(1) fallback removed as unsafe); 
(3) dialog proof with the user at the machine (AskUser shape, Cancel zero-mutation, menu Run); (4) Comp Scripts install after gate 3; 
(5) Ungroup stays fail-closed until exact restoration is proven on a disposable fixture.

Gate 2 closeout: selection setter is `comp.SetActiveTool(tool)` with `GetToolList(True)` readback; `SetAttrs(TOOLB_Selected)` is a silent no-op; evidence in `docs/checkpoints/2026-09-06-semantic-arrange-gate2-selection.md`. 
Next: adopt-with-guard cleanup of orphan RNK_NEST names from the stalled sibling run, then the dialog human gate (AskUser shape, Cancel, menu Run), then Comp Scripts install.
