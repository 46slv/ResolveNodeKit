# ResolveNodeKit current state

Updated: 2026-09-08 JST

This file is the short-lived operational pointer for the next Codex run. Live local Git/worktree, remote Git/PR, and live Resolve state always outrank it. Historical detail belongs in `docs/checkpoints/`.

## Program status

`CHECKPOINTED`

The Resolve host recovered successfully and was clean/responsive at the end of the latest run. ResolveNodeKit is not globally blocked and is not `MISSION_COMPLETE`.

The mission-critical unresolved requirement remains runtime visual nested-group access: groups must remain GroupOperators, actually open in the Fusion runtime/UI sense, have their internals tidied, and show all contents.

## Canonical repo state

- repo: `46slv/ResolveNodeKit`
- task branch: `feat/arrange-uia-e2e-20260906` (production seam continuation; do not merge to `main`)
- current candidate code commit: `716d6a4506b021d27b82057b17e3ca589d579d6a`
- PR #5 head branch: `feat/semantic-arrange-v1-20260906` (Draft; candidate head is kept aligned non-destructively)
- latest published candidate ref: `1cbbeae1fff76f495d6b521a3f166117c5b3acb8` (docs-only after SAV1-80; no product code changed)
- Draft PR: #1 (bootstrap) plus #5 (Semantic Arrange v1, stacked on the bootstrap branch), both open/draft
- branch locator immediately before this state normalization: `716d6a4506b021d27b82057b17e3ca589d579d6a`
- reported worktree at latest run end: clean; task and PR remote refs are in sync at the latest published candidate ref
- offline suite: 122/122 unittest PASS + `compileall` PASS

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
Orphan RNK_NEST names adopted and deleted with guardrails 2026-09-06 JST afternoon; host clean ([Timeline 1] current, all comps unmodified, no save). Install PASS 2026-09-06 JST afternoon: user-scoped entry plus package plus manifest installed with verified hashes; Resolve-side import from installed tree proven read-only; Comp entry listed. Dialog cause proven 2026-09-06 JST evening from run log: menu exec provides no __file__, bootstrap found nothing, import-error exit 4, Console-only print. Fix installed (host-native root discovery via MapPath plus APPDATA, unconditional entry with run logging, shape-tolerant dialog). User clicks 16:20-16:24 JST: bootstrap fix verified, list-shape AskUser proven with Japanese keys, Ungroup correctly refused twice, then a live-comp selection run exposed a hostile parent structure plus a None GetInputList plus one silent stall. Hardened list getters, added phase progress plus target logging plus visible busy and result dialogs, reinstalled and verified. Next: one user menu press with nodes selected.

Review-3 fixes installed 2026-09-06 JST evening (branch 1244721): busy is always hidden before the result dialog on success and refusal paths; readback and verify begin markers fire before their phase work; interactive writes require live current and fail closed with exit 5 when unproven. Locked by 4 focused tests. Suite 97/97 green, compileall PASS, reinstalled with entry and package hash match, manifest stamped 1244721. Next: one user click on the same 4 nodes.

Dialog-first reorder installed 2026-09-06 JST midday (branch 7d971f2): setup dialog runs on the UI-owner comp before any target bind, Cancel exits with zero mutation, Run binds live current with require_live and shows a visible refusal on failure, then busy, arrange, busy close, result. Locked by 3 dialog-first tests. Suite 100/100 green, compileall PASS, reinstalled with entry and package hash match, manifest stamped 7d971f2. Next: one user click on the same 4 nodes.

## Arrange UIA E2E recovery — 2026-09-07

The existing `feat/arrange-uia-e2e-20260906` branch was recovered at `bf42239`
with the worker's two untracked host verifier files and its OpenCode/Muse UIA
artifacts. The exact resume point was step 5: bind the real `UiMainWindowImp`,
repair the transient-popup menu route, and continue from the existing
`RNK_UIA_E2E` fixture. The identity-based menu Invoke now passes through
`Workspace > Scripts > ResolveNodeKit_Arrange`; Resolve 21.0.3.7 does not expose
the `Comp` category node, so the evidence records a direct identity entry route
with `category_element_exposed=false`.

The setup window is visible to UIA, but its four apparent checkbox nodes are
Fusion Qt `ControlType.Group` elements with empty label/name/value metadata and
no `TogglePattern`; the two required labels and OFF/OFF readback therefore cannot
be proven safely. This is a narrow `BLOCKED_UIA_CAPABILITY` gate, not a reason to
replay the menu/fixture work or guess by control order. The persistent QWidget
provider also prevents claiming logical dialog absence from the tree alone.

Fusion API readback showed no graph mutation, and the exact disposable timeline
plus its two worker-created archive timelines were deleted under confirmation
guardrails. Resolve was restored to Fusion page / `Timeline 1`, with no project
save. Full machine-readable evidence is at
`D:\temp\uia\arrange_uia_e2e_codex_20260907_final.json` (raw JSONL plus the
full UIA dump are retained beside it); the durable checkpoint is
`docs/checkpoints/2026-09-07-arrange-uia-recovery.md`.

The earlier checkpoint proposed exposing the AskUser labels through the provider;
that route is intentionally not attempted in this continuation. The measured
behavioral-default gate below uses the existing host as-is.

## Behavioral-default continuation — 2026-09-07

The step-5 menu Invoke evidence was reused without rerunning it. A direct
Fusion `RunScript("Py", installed_entry)` route opened the production setup
dialog in a fresh `_mcp_RNK_UIA_B1` project. This separates the contract into
`UI_ACCESSIBILITY` and `PRODUCT_BEHAVIOR`: checkbox readback is explicitly
`BLOCKED_HOST_ACCESSIBILITY`, while behavioral defaults are only
`PASS_BEHAVIORAL` when a safe Run/Cancel identity and host invariant proof exist.

On Resolve 21.0.3.7, the setup window exposed five button candidates with
InvokePattern/ValuePattern but no Name, AutomationId, or label. Thus Run and
Cancel could not be identity-bound without control-order guessing. B1 stopped
before Run as `BLOCKED_HOST_ACCESSIBILITY`; B2–B5 behavior gates were not run.
No checkbox or graph mutation was performed. The disposable project was deleted
and `PSD2Fusion` / `Timeline 1` restored with `COMPB_Modified=false` and no save.

Evidence: `D:\temp\uia\arrange_uia_behavior_20260907.json` (schema v2).
Durable checkpoint: `docs/checkpoints/2026-09-07-arrange-uia-behavior-defaults.md`.

## MSAA / IAccessible continuation — 2026-09-07

The one permitted semantic-accessibility probe was completed from `c04a58b`.
The existing step-5 menu evidence was reused and OpenCode/Muse were not called.
The earlier 4 checkbox and 5 button candidates were inspected once for
`LegacyIAccessiblePattern`; the host PowerShell UIAutomationClient did not
expose that type for any candidate.  A direct `oleacc.dll` fallback obtained
the dialog's `IAccessible` root (`S_OK`, `ROLE_SYSTEM_CLIENT`, `ChildId=0`) but
`AccessibleChildren` exposed no Run, Cancel, or checkbox semantic rows.

The evidence therefore closes desktop identity exploration as
`BLOCKED_HOST_ACCESSIBILITY_HARD` for Run, Cancel, and both checkboxes.  No
`accDoDefaultAction`, UIA Invoke, checkbox operation, graph mutation, Undo, or
project save was attempted.  Cleanup and final host readback preserved
`PSD2Fusion` / `Timeline 1`, 967 tools, and `COMPB_Modified=false`.

Evidence: `D:\temp\uia\arrange_msaa_20260907.json`.
Durable checkpoint: `docs/checkpoints/2026-09-07-arrange-uia-msaa-blocker.md`.

The recommended next implementation is to extract the post-dialog Arrange
mutation into a common handler accepting explicit default state, then verify
that handler through a disposable Fusion API behavior lane.  Keep AskUser/UIA/
MSAA as a separate visibility-capability lane; its hard provider blocker must
not gate the host behavior proof.

## Arrange production seam — 2026-09-07

The post-dialog mutation is now one shared `execute_arrange_request` handler
used by the GUI script and the generated direct-host verifier.  It preserves
live-target binding, fail-closed ungroup behavior, busy/result ordering, and
the existing semantic snapshot/readback/Undo contract.  Cancel exits before
the handler; GUI Run passes one explicit `ArrangeDialogState`.

Offline verification is 115/115 with compileall PASS.  The direct host
behavior lane is prepared but not accepted as PASS: the Resolve scripting
endpoint became unresponsive after a disposable `LoadComp`/`Paste` route, so
no host mutation or cleanup claim is made for that attempt.  The exact UIA /
MSAA hard blocker remains narrow and separate.  Durable details:
`docs/checkpoints/2026-09-07-arrange-production-seam.md`.

## Arrange live host acceptance recovery — 2026-09-07

The first and only fresh read-only scripting connection after `abe53f6` was a
bounded `script_plugin.run_inline` probe for current project/timeline/comp/tool
count/page.  It returned no response for more than 60 seconds, materially
matching the prior blocked endpoint.  Resolve (`PID 23240`) and its embedded
`fuscript.exe` (`PID 8636`) remained process-responsive, but the scripting
endpoint did not return readback.

This gate is `BLOCKED_HOST`.  Resolve/embedded Fusion scripting endpoint restart
is operationally required for the next acceptance attempt; no restart was
performed.  No cleanup, fixture mutation, handler run, busy/result observation,
Undo, second run, or restore claim was made, and no save occurred.  The exact
current title still identifies the disposable project
`_mcp_RNK_SEAM_20260907`; its cleanup remains pending and must not be claimed as
complete.

Machine-readable evidence and the bounded stop record are in
`docs/checkpoints/2026-09-07-arrange-live-host-blocked.json` and
`docs/checkpoints/2026-09-07-arrange-live-host-recovery.md`.

## Arrange live host acceptance — 2026-09-07

After one authorized Resolve restart, the scripting endpoint recovered.  The
old exact Resolve/fuscript tree was terminated only after the bounded normal
close failed; the new Resolve/fuscript pair is responsive.  Exact disposable
projects `_mcp_RNK_SEAM_20260907` and `_mcp_RNK_SEAM_ACCEPT_20260907` were
deleted without saving.

The direct production seam is now host-proven on fresh bounded AddTool/API
fixtures.  B1 passed selected-only movement, unselected preservation,
connection/tool identity preservation, exact Undo, and second-run `moved=0`.
B2 passed with an explicit GroupOperator in scope: success with `ungroup=false`,
GroupOperator retained, membership/connections unchanged, exact Undo, and
second-run `moved=0`.  The host does not expose `GroupOperator.AddTool`, so the
group membership proof uses an empty GroupOperator and is documented as
vacuous.

The host UI layer remains limited: `UIDispatcher` was unavailable to the direct
handler, so busy stage text and same-run busy/result ordering were not accepted.
A result window was observed and closed by identity; this does not invalidate
the direct host behavior proof.  UIA/MSAA remains
`BLOCKED_HOST_ACCESSIBILITY_HARD`.

Final host readback: `PSD2Fusion` / `Timeline 1` / Fusion, exactly one timeline,
967 valuable tools, `COMPB_Modified=false`, no RNK disposable remnants, no save.
Details: `docs/checkpoints/2026-09-07-arrange-live-acceptance.md` and its JSON
evidence file.

## Semantic Arrange FIRST_USABLE scope — 2026-09-07

Product direction has been simplified: the canonical v1 request is now
`ArrangeDialogState(include_unselected=True, ungroup=False)`, meaning all nodes
in the active Fusion composition are arranged recursively while every
GroupOperator is preserved.  The former selection-only/fixed-obstacle path
remains covered by regression tests and an explicit experimental verifier flag;
it is no longer a release blocker.

The production entry now shows only the whole-composition confirmation text
`現在のFusionコンポジション全体を整列します。`; the two checkbox controls are
not part of FIRST_USABLE UI.  `ungroup=True` remains fail-closed and is not
exposed until exact structural restoration is host-proven.

The offline/host verifier defaults and launcher fixture are aligned to this
whole-comp contract.  Installed-entry real-host smoke then passed on
disposable API fixtures: B1 used 6 tools / 3 edges and arranged all 6
(`moved=5`); B2 used 7 tools / 1 preserved GroupOperator / 3 edges and
arranged all 7 (`moved=6`).  Both second runs returned `moved=0`, graph/tool
invariants held, and the first handler-owned Undo snapshot matched the
pre-snapshot exactly.  `UIDispatcher` remains unavailable, so busy/result UI
ordering is not claimed.  Final host state is PSD2Fusion / Timeline 1 / Fusion
with 967 valuable tools, `COMPB_Modified=false`, no RNK-owned remnants, and no
save.  The installed entry keeps its comp wrapper for AskUser but binds the
mutation target from `Fusion.GetCurrentComp()` through the same seam.  Evidence:
`docs/checkpoints/2026-09-07-semantic-arrange-whole-comp-host-smoke.json`.

Large-graph stress remains the next acceptance lane; no new UIA/MSAA probe is
required for this scope change.  Durable decisions:
`docs/checkpoints/2026-09-07-semantic-arrange-first-usable-scope.md` and
`docs/checkpoints/2026-09-07-semantic-arrange-whole-comp-host-smoke.md`.

## Semantic Arrange v1 continuation — 2026-09-08

SAV1-00 through SAV1-40 are reconciled or freshly host-proven on the
continuation candidate.  SAV1-50 established a compact 64-tool transport
envelope: valuable 967-tool position and connection probes at 16/32/64 all
returned successfully, and the disposable large pre-read completed all 16
position and 16 connection chunks with parent-computed composite hashes.
No full graph payload was returned through MCP.

SAV1-60 is a narrow `BLOCKED_HOST` / `UNVERIFIED` product-stress gate.  One
real production `execute_arrange_request` whole-comp call on disposable
`_mcp_RNK_SAV1_60_20260908` timed out at the 300-second MCP limit without a
structured result.  The representative processing/keyframe sample also timed
out at 120 seconds, so processing preservation is explicitly unavailable for
that large readback.  The same product route was not blindly retried.  The
exact Resolve/fuscript recovery path was followed; a post-restart identity
probe passed, the duplicate and generated archive were deleted, and the final
valuable state is again `PSD2Fusion / Timeline 1 / Fusion`, 967 tools,
`COMPB_Modified=false`, exactly one timeline, no save.  One compact duplicate
position chunk differed after recovery, so no large first-run, second-run,
invariant, or Undo PASS is claimed.

Fresh small-host evidence remains PASS: SAV1-30 whole-comp (7 tools) and
SAV1-40 nested non-empty Groups (8 tools, `InnerG` inside `OuterG`) both moved
on run 1, returned `moved=0` on run 2, preserved structure, and restored exact
Undo state.  Busy UI remains `BLOCKED_HOST_CAPABILITY` (`UIDispatcher` absent),
and AskUser UIA/MSAA remains `BLOCKED_HOST_ACCESSIBILITY_HARD`; neither gates
the autonomous continuation.  Durable details:
`docs/checkpoints/2026-09-08-semantic-arrange-v1-continuation.md` and its JSON
record.

SAV1-80 fresh independent verification is `PASS` for candidate ref
`6b0f1ece9bd5178a2efb36597d0b6d4632380a4d`: task/PR remote refs match, the
worktree is clean, the candidate is based on the bootstrap base, `main` is not
merged, PR #5 is OPEN/Draft, offline/install/Resolve checks pass, and the
final host cleanup/no-save readback matches the checkpoint.  The verifier made
no candidate edits.  SAV1-90 is now the only remaining conditional task: one
human release smoke if the UI shell remains unautomatable.
