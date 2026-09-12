# ResolveNodeKit current continuation

Updated: 2026-09-12 JST
Status: `CHECKPOINTED_WITH_TECHNICAL_GAP` / product not complete

Live Git/PR/installed/runtime evidence always outranks this locator.

## Active goal

`RNK-STRICT-ORTHOGONAL`

Complete the existing strict horizontal/vertical whole-comp layout, actual orthogonal displayed wires, safe preserve and flatten-all, installed UI flow, processing preservation, exact Undo/rollback, run2 stability, real/1100+ qualification, performance, recovery, cleanup and final independent verification.

Required product gates remain G01–G14. Do not lower or delete a gate to claim completion.

## Current execution policy — Direct Guarded reset

The dedicated/external Resolve Operator is no longer part of the RNK product critical path. It is retained only as research/legacy evidence.

Default execution:

```text
Luna Max Product Worker / Coordinator
  -> direct current Resolve capability
  -> minimal mechanical Host Guard
  -> DaVinci Resolve
```

The old Operator-isolation invariant `parent Resolve visibility = 0` is retired. If current local configuration still disables direct Resolve capability solely to preserve that architecture, repair/enable the direct Product Worker route with rollback available.

The historical D/S/H matrix and WP1 HostLocalSemanticReceipt experiments are not product dependencies. Do not replay them for normal RNK progress.

## Safety retained

For mutable/concurrent live-host work preserve the useful mechanical invariants without requiring another agent/process:

- one integration/state writer;
- one live Resolve writer or equivalent user-wide serialization;
- exact target identity before valuable writes;
- owned/disposable scratch state;
- no blind retry after ambiguous mutation;
- reversible mutation / Undo or discardable fixture where practical;
- before/after readback;
- cleanup/recovery;
- no valuable project save unless separately authorized.

## Product status

Current gate status carried from the latest verified checkpoint:

- G01: `PASS`
- G02: `BLOCKED_TECHNICAL`
- G03: `PASS`
- G04: `PASS`
- G05: `BLOCKED_TECHNICAL`
- G06: `PASS`
- G07–G08: `PASS`
- G09: `PENDING`
- G10: `BLOCKED_TECHNICAL`
- G11: `PENDING`
- G12: `PASS`
- G13–G14: `PENDING`

Latest pre-reset product/operator verification reported:

- RNK canonical suite: `174/174 PASS`
- compileall: PASS
- diff-check: PASS
- strict contract checker: PASS
- Operator research suite: `30/30 PASS` for `HostLocalSemanticReceipt`
- graph/layout/Undo/save writes in the final WP1 transport probes: `0`
- final lease: `FREE`

These facts do not equal product completion.

## Direct guarded reset and product continuation — 2026-09-11

Checkpoint: `docs/checkpoints/2026-09-11-direct-guarded-reset.json`

- `C:\Users\shiro\.codex\config.toml` now exposes both direct `davinci-resolve` and `native-resolve` MCP servers to the Luna Max Product Worker. The global AGENTS route is direct guarded execution; the legacy Operator profile/skill/config remain available only for explicit research.
- Native direct status was visible (`running=false`, Resolve `21.1`), but its one launch attempt timed out after 60 seconds. It caused no mutation and is closed without a blind retry.
- Direct compatibility minimum smoke passed on Resolve `21.1.0.14` / MCP `2.203.0`: owned Fusion context, exact position read, one reversible position write with readback, owned fixture discard after Undo did not restore, and cleanup with no project save.
- The installed RNK seam then passed on the same direct compatibility route: `execute_arrange_request` moved 4 of 5 tools on Run 1 and performed 0 writes on Run 2. Tool identity, connections, parent membership, and basic processing attributes were preserved; the owned project was deleted and absent on readback.
- After the checkpoint commit, the user install was refreshed and read back at commit `5306b4b52f2707219cd89092d56f12764a8d2a1d` with 20 files and installed-root import PASS; the product smoke itself remains tied to source candidate `239ac09eb72291281bde4a1c95f25a62060aaffb`.
- UI Run/Cancel/busy/displayed-wire and full processing/render equivalence are not claimed. The inline `COMPB_Modified` transport value differed from the direct MCP pre-probe, so this is a product seam smoke, not SO-30/SO-50 qualification.
- Final independent scripting/process readback: Resolve `21.1.0.14`, GUI responsive, Fusion page, `Untitled Project`, zero timelines, owned fixture absent, and project-save count `0`.
- Learning Gate: `NO_REUSABLE_DELTA`. Keep the existing mechanical guard and readback/cleanup rules; do not add a generic Resolve execution framework or restore Operator routing.

## Direct product-gate run — 2026-09-11 (SO-30 / SO-40 / SO-50 / SO-60) [v3, superseded SO-40 wording]

Checkpoint: `docs/checkpoints/2026-09-11-so30-so40-so50-direct-host-v2.json`

- Fresh owned Resolve Studio `21.1.0.14` / compatibility MCP `2.203.0` work used one live writer and window `6301810`. The SO-30/SO-40 disposable fixture was a non-empty depth-2 Group graph (16 tools after the SO-30 additions, 8 labelled edges) with TextPlus, RectangleMask, Blur, branch, isolated node, and protected input readback.
- SO-30 was proven in the actual Fusion FlowView by ordinary GUI context-menu operation: Flow context menu `Options > Orthogonal Pipes` (Japanese label `直交パイプ`) changed the displayed TextPlus->Merge, mask, serial, branch, and difficult-edge routing; the menu state was re-opened and read back. The same setting remained selected after opening a second owned timeline/comp, so the measured scope is application-level preference (not comp-local or Flow-local). It was restored to `Straight Pipes` before cleanup. This is an actual displayed-wire result, not a coordinate inference; `SO-30/G03 = PASS`.
- SO-40's original record treated the extra native no-op Undo as a one-owned-Undo contract failure. That interpretation is superseded by the 2026-09-12 fresh exact-rollback record below; the historical observation itself remains unchanged.
- SO-50 installed identity was fresh-read from `Workspace > Scripts > ResolveNodeKit_Arrange`: source and installed `ResolveNodeKit_Arrange.py` SHA256 are `9C35CA8984163DA0AD2E00899C0EBA2B2C9B08FE039C32EFA235DC367A85AFCE`. The RNK-owned window was obtained by title/shape identity inside Resolve (not OS foreground activation). Cancel run `45ed02daee914c3b9e29774a1db31de1` produced two visible Cancel attempts and `event=cancelled`; the 16-tool graph remained unchanged (zero write). A nested Run `1cfb001b535f460ea993818e268e1997` correctly showed busy/result events but refused on Group rollback, so it is failure evidence only. A flat 9-tool SO-30 fixture then completed Run `b44bd2bea0c442bebdf4e390f1e2fec0`: setup/OK widget, same-controller target bind, `busy shown -> snapshot/readback -> busy hidden -> result shown`, 9 tools / 5 edges, and identity/port/TextPlus/Mask/Blur/Blend readback. The installed UI gate is `SO-50/G06 = PASS`; the fast busy phase was event-read from RNK's run log rather than a separately retained screenshot.
- SO-60 used a fresh disposable still-media timeline/comp (`RNK_SO60_E2E_20260911`, `コンポジション5`) with flat, fan-out, mask, isolated, and GUI-created non-empty Group content. The first installed run refused only because Resolve exposed unpositioned `Left AudioDisplay`/`Right AudioDisplay` tools; those two owned fixture-only display tools were deleted and the controller then completed on 10 positioned tools. Run `0800c59026864165b66176ed540ee23e` moved 9 tools and preserved labelled connections plus TextPlus/Mask/Blur/Blend values. A same-controller stability run `7c9fa40309cc4f93a9c6622fc58e04e3` reported `moved=0` with identical geometry. A GUI-created Group containing `RNK_SO60_BG` and `RNK_SO60_BLUR` was preserved by run `96a6c85a102e4466bb0a72a8639b19fc` (`moved=3`) and run `883b4277cace4fd7873358f77f44a292` (`moved=0`): non-Group IDs/RegIDs, Group parent identity, exact labelled ports and protected inputs stayed intact. Undo probe run `08c2ff6a8aa644b09f236d2d77c59c99` was changed once, then one standard Ctrl+Z restored the complete pre-run snapshot (`equal=true`, Group remained), so `SO-60/G07/G08 = PASS`.
- Cleanup used the same writer with no project save: the SO-60 live timeline and its two auto-created archive timelines were deleted via exact confirmation (`3 -> 0`), the imported `img20.jpg` clip was deleted via exact confirmation, `folder.get_clips` returned `[]`, the final timeline list is empty, and current project remains `RNK_DIRECT_GATES_20260911_PROJECT`.
- G01–G14 at that time: `G01 PASS`, `G02 BLOCKED_TECHNICAL`, `G03 PASS`, `G04 BLOCKED_CONTRACT`, `G05 PENDING`, `G06 PASS`, `G07 PASS`, `G08 PASS`, `G09–G14 PENDING`. This point-in-time matrix is superseded by the continuation checkpoint below.
- The evidence-only docs were published on the task branch and pushed to PR #5 at evidence commit `3871dac`; PR #5 remains OPEN/Draft and `main` is untouched. The final remote ref is re-read after the metadata push and reported with the exact SHA below.

## Direct guarded continuation — 2026-09-12 (SO-40 / SO-61 / SO-70 / SO-80)

Checkpoint: `docs/checkpoints/2026-09-12-so40-so61-so70-so80-direct-continuation.json`

- SO-40/G04 is now `PASS`. A fresh owned depth-2 fixture went from 18 tools / 2 Groups to 16 tools / 0 Groups through native Fusion GUI `Ungroup`, deepest Group1 then parent Group2. All 11 port-labelled processing edges, boundary child endpoint/proxy equivalence (no GroupOperator substitution), non-Group IDs/RegIDs, parent semantics, complete input expression/keyframe snapshot, protected TextPlus/Blur/Mask/Merge/MediaIn/MediaOut values, and readback geometry were preserved. The second flatten readback was a no-op. Flat -> Ctrl+Z #1 restored the parent Group2 intermediate; Ctrl+Z #2 restored the exact pre-flatten snapshot (identity, positions, parents, edges, inputs, and static values). The Undo count is 2 and is not a G04 criterion; G08 remains the separate SO-60 one-owned-Undo PASS.
- SO-61 is `BLOCKED_TECHNICAL` / G05 not promoted. Native GUI flatten and the small render probe preserved state; 18 compared frames were byte-identical (nested wrote 150, flat wrote 18 before safe cancel). The installed RNK `UngroupFirst` route still refuses closed because no measured identity-preserving host primitive is wired, so the requested installed-entry flatten E2E is not claimed.
- SO-70 is `BLOCKED_TECHNICAL`; G02 remains blocked and G10 is not qualified. The current disposable PSD2Fusion item3 had 1109 total / 34 Groups / 1075 non-Group / depth 4 / 1345 edges; item9 had 1076 non-Group. The direct product attempt ran once for 46.148s, wrote 1105 positions, then refused at readback with a 12-node rollback-incomplete list. No blind retry, Undo, run2, strict wire, or three-run performance claim is made. The explicit >=1100 non-Group fixture and three real-changing <=60s baseline are still open.
- SO-80/G12 is `PASS` for the existing product recovery path. Current host evidence covers UI Cancel zero-write, safe render timeout/cancel, fail-closed rollback-mismatch stop, and this continuation's independent-lane resume. The 174/174 suite (including 86 recovery-focused tests), strict contract 30/30, compileall, install backup/idempotence/foreign-entry/uninstall tests, current source/install hash parity, and the carried exact Resolve timeout/relaunch/ambiguous-state recovery record all pass within their stated scopes. No generic execution framework or retired Operator route was added.
- Cleanup is exact: the two owned SO-70 timelines were deleted by verified IDs; only valuable `Timeline 1` and pre-existing `Timeline 1_archived_v06` remain. The SO-61 render directory and SO-40 temporary screenshots were removed. PSD2Fusion is current, responsive, unmodified (`COMPB_Modified=false`), and no project save was issued.
- Current matrix: `SO-00/10/11/20/30/40/50/60/80 PASS`; `SO-61 BLOCKED_TECHNICAL`; `SO-70 BLOCKED_TECHNICAL`; `SO-71/90 PENDING`. Gates: `G01 PASS`, `G02 BLOCKED_TECHNICAL`, `G03 PASS`, `G04 PASS`, `G05 BLOCKED_TECHNICAL`, `G06 PASS`, `G07 PASS`, `G08 PASS`, `G09 PENDING`, `G10 BLOCKED_TECHNICAL`, `G11 PENDING`, `G12 PASS`, `G13–G14 PENDING`.
- Source/install identity at the superseded continuation checkpoint was candidate `b0bf8f891bf87d10db23c6d9213cb4b449bfa407`; the parent-first continuation below is the current source/install record.

## Direct guarded continuation — 2026-09-12 parent-first rollback canary

Checkpoint: `docs/checkpoints/2026-09-12-so61-so70-parent-first-canary.json`

- Evidence/install baseline `c26bfdf6b1b918590e22327c0f37de4bb6859d1a` is pushed to PR #5's actual head branch `feat/semantic-arrange-v1-20260906`; the installed manifest matches that baseline with 20 files / 0 package mismatches. The parent-first code change originated in `1e83aec10e6f006932c4c19da581c0dffdb869ec`. Focused tests are 89/89 PASS, full tests 175/175 PASS, compileall and diff check PASS.
- The SO-70 rollback fingerprint was localized without replaying the old 1100+ failure. The repeated node prefix was a symptom across several parent scopes. A minimal measured canary reproduced the mismatch when a nested child was written before its GroupOperator and the parent was normalized later. Parent-first ordering plus one queued batch flush and complete readback fixes the reusable nested FlowView behavior. The helper is shared by tidy, recursive semantic arrange, and strict apply; the regression is node-name-independent.
- A fresh disposable PSD2Fusion duplicate with generated rails reached 1198 tools / 1173 non-Group / 25 Groups / 1341 edges at live depth 2. The installed product ran with all-node/all-edge coverage, endpoint loss 0, identity/parent/edge exactness, logical overlap 0, exact Undo restoration, one no-op run2, and three real-changing runs of 13.692s / 15.018s / 14.477s. This is substantial recovery of the SO-70 lane, but it is not a G02/G10 PASS: the prior relevant depth-4 source case was not reproduced, 60 positions were outside the host grid tolerance, rectangle geometry and strict displayed wires are not exposed by the current FlowView surface, and the distinct generated depth-qualified fixture was not qualified because nested GroupOperator creation was refused.
- SO-61 remains `BLOCKED_TECHNICAL` / G05. Current API/action-registry/UI inspection measured the native GUI label `グループを解除` but no installed-callable identity-preserving action or documented Ungroup method. Installed `UngroupFirst` therefore remains fail-closed; no guessed action ID or generic desktop bridge was added.
- Cleanup is exact: task-owned duplicate `_mcp_RNK_SO70_PSD_DUP_20260912` and auto-archive `Timeline 1_archived_v08` were deleted by verified IDs; `Timeline 1` and pre-existing `Timeline 1_archived_v06` remain. PSD2Fusion is current with 958 tools, generated prefix count 0, `COMPB_Modified=false`, and project save calls 0.
- Current matrix remains `SO-00/10/11/20/30/40/50/60/80 PASS`; `SO-61 BLOCKED_TECHNICAL`; `SO-70 BLOCKED_TECHNICAL`; `SO-71/90 PENDING`. Gates remain `G01 PASS`, `G02 BLOCKED_TECHNICAL`, `G03 PASS`, `G04 PASS`, `G05 BLOCKED_TECHNICAL`, `G06 PASS`, `G07 PASS`, `G08 PASS`, `G09 PENDING`, `G10 BLOCKED_TECHNICAL`, `G11 PENDING`, `G12 PASS`, `G13–G14 PENDING`.

## Direct guarded continuation — 2026-09-12 depth-4 preserve/performance

Checkpoint: `docs/checkpoints/2026-09-12-so70-depth4-direct-preserve.json`

- The direct-native source export was re-read from valuable `PSD2Fusion` before the disposable import: `Timeline 1` item index 3 (`4b396796-377b-43c8-94df-83b43959ed91`) is a real depth-4 comp with 1109 total tools, 1075 non-Group tools, 34 `GroupOperator`s, and 1345 labelled edges. The exact `ExportFusionComp` artifact is 716273 bytes, SHA256 `341c919157d0470a923de4b08fff60bf56900b5b0f03303d5fb0105d6d237103`, with native header `RenderRange={43,59}`. No valuable-project save was issued.
- On the owned `_mcp_RNK_SO40_SO70_SO80_20260911` fixture, the installed package entered the same production `execute_arrange_request` seam through Direct Guarded `script_plugin.run_inline`. Three independent real-changing preserve actions completed in 11.0631s / 11.0085s / 10.8047s (1107 moved, 1109 arranged, 1345 edges each); each had endpoint loss 0, exact topology/parent/edge readback, and one Undo restored position hash `45ee0b5b` exactly. Diagnostics on the first run include logical overlap 0, backbone/branch violations 0, 35 scopes, 34 logical group boxes, and 2 fixed-point iterations. A separate same-controller stability run reported 1107 then 0 moves with identical second geometry and exact Undo.
- This closes a useful depth-4 preserve/performance checkpoint but does not close strict Mission gates: this source case is 1075 (not 1100) non-Group tools, rectangle geometry and integer-grid proof are not exposed by the measured FlowView surface, strict displayed-wire collection is not part of this large run, and the installed flatten route still refuses without an identity-preserving host primitive. Therefore `SO-70/G02/G10` remain `BLOCKED_TECHNICAL`; `G09/G11` remain pending for the required flatten-scoped evidence rather than being inferred from preserve-only runs.
- Cleanup is exact and limited to the owned project: five verified disposable/archive timelines were deleted (`5 -> 0`) and `img20.jpg` was deleted by its exact Media Pool ID; the folder is empty and no current timeline remains. The runtime is left on the dedicated empty project, so the valuable PSD2Fusion timeline was not reloaded or saved after the read-only source export.
- Current matrix remains `SO-00/10/11/20/30/40/50/60/80 PASS`; `SO-61 BLOCKED_TECHNICAL`; `SO-70 BLOCKED_TECHNICAL`; `SO-71/90 PENDING`. Gates remain `G01 PASS`, `G02 BLOCKED_TECHNICAL`, `G03 PASS`, `G04 PASS`, `G05 BLOCKED_TECHNICAL`, `G06 PASS`, `G07 PASS`, `G08 PASS`, `G09 PENDING`, `G10 BLOCKED_TECHNICAL`, `G11 PENDING`, `G12 PASS`, `G13–G14 PENDING`.

## Direct guarded continuation — 2026-09-12 depth-4 1100-threshold preserve

Checkpoint: `docs/checkpoints/2026-09-12-so70-depth4-1100-direct-preserve.json`

- A fresh disposable depth-4 fixture was built from a direct native `ExportFusionComp` of PSD2Fusion `Timeline 1` item index 3, then padded before the baseline with 25 explicitly named disconnected `Background` tools. Host readback was 1,134 tools / 1,100 non-Group / 34 Groups / max depth 4 / 1,345 edges. The source-derived portion remains 1,075 non-Group; the 1100 numeric threshold is therefore recorded as a constructed-fixture result, not silently rewritten as a source-derived claim.
- The installed production seam was exercised directly three times from equivalent restored baselines. Product stage sums were 15.0752s / 12.8013s / 13.0515s, each moved 1,132 and arranged 1,134 tools, preserved all 1,345 edges and parent/identity sets, reported logical overlap 0, and restored exactly with one owned Undo. A separate stability run reported first moved 1,132 then second moved 0 with identical geometry and exact Undo.
- This materially closes the numeric large-preserve/performance sub-work, but does not close strict Mission gates: FlowView still exposes no node rectangle geometry or integer-grid proof for these nodes, large strict displayed-wire evidence and complete processing-state hashes were not collected, and the installed flatten route remains fail-closed. Consequently `SO-70`, `G02`, and `G10` remain `BLOCKED_TECHNICAL`; `G11` remains pending until flatten-scoped SO-71 evidence exists.
- A fresh read-only Computer Use accessibility observation of the returned Resolve window exposed only generic Fusion `Custom/Group` elements; graph node names, rectangle bounds, wire endpoints, and graph identity were absent. No coordinate-derived claim or blind UI invoke was made; this confirms the current strict display/rectangle capability boundary.
- Cleanup is exact: the disposable project, its two timelines, imported clip, source export, and three full sidecars were deleted/read back absent; current runtime is the dedicated empty `_mcp_RNK_SO40_SO70_SO80_20260911` project with no timeline/clips and no valuable-project save.
- The latest SO-61 action-surface result is unchanged: no callable identity-preserving Ungroup primitive or documented action ID was measured. Do not repeat that route; resume only on a materially different measured bridge.
- Current matrix remains `SO-00/10/11/20/30/40/50/60/80 PASS`; `SO-61 BLOCKED_TECHNICAL`; `SO-70 BLOCKED_TECHNICAL`; `SO-71/90 PENDING`. Gates remain `G01 PASS`, `G02 BLOCKED_TECHNICAL`, `G03 PASS`, `G04 PASS`, `G05 BLOCKED_TECHNICAL`, `G06 PASS`, `G07 PASS`, `G08 PASS`, `G09 PENDING`, `G10 BLOCKED_TECHNICAL`, `G11 PENDING`, `G12 PASS`, `G13–G14 PENDING`.

## Historical WP1 boundary — archived research

Checkpoint:
`docs/checkpoints/2026-09-11-wp1-host-local-semantic-receipt.json`

Historical result:

- compatibility route: `BLOCKED_RUNTIME_NO_PROGRESS`
- native route: API discovery reached `LoadComp`, `GetPosTable`, Undo/Close surfaces but timed out before semantic receipt: `BLOCKED_SEMANTIC_RECEIPT_TIMEOUT`
- both routes performed no fixture/product mutation/save and ended lease `FREE`

Decision: preserve this as evidence that the external proof/transport boundary became more expensive than ordinary guarded host operation. It no longer blocks SO/G product work.

## Current product plan

Canonical execution docs:

- `docs/execution/strict-orthogonal/README.md`
- `docs/execution/strict-orthogonal/PLAN.md`
- `docs/execution/strict-orthogonal/LUNA_RUNBOOK.md`
- `docs/execution/strict-orthogonal/acceptance.json`
- `docs/design/strict-orthogonal/DESIGN.md`
- `docs/design/strict-orthogonal/SOURCES.md`

The plan no longer contains WP1/topology qualification as a dependency.

## Exact next action

1. close SO-61 by qualifying an existing installed-entry/native host bridge for identity-preserving flatten, then rerun the small E2E;
2. close the remaining SO-70 strict rectangle/grid/display and complete processing evidence on the fresh depth-4 1100-threshold fixture; do not treat the numeric threshold or preserve-only runs as G02/G10/G11 completion;
3. keep SO-80's existing recovery contract and direct guarded route; do not rebuild the retired Operator/WP1 transport;
4. after SO-61 + SO-70, continue SO-71 and then request SO-90's fresh independent verifier.

## Stop boundary

Do not stop merely because a historical Operator/WP1 route is blocked.

Stop only for a genuine authority/input boundary, unrecoverable valuable-state risk, no remaining authorized ready product work, or actual completion of the existing acceptance contract.

## Authority

Authorized: task-branch code/tests/docs, backup-backed install, commit/push/Draft PR updates, direct Resolve MCP/scripting/GUI, Resolve launch/quit/restart, owned scratch/disposable fixtures and reversible validation mutations.

Not authorized by this state file: valuable project save, main merge/release, force-push shared history, credential changes, unrelated destructive OS/process work, PC reboot, global shortcut mutation or permanent service/startup installation.

## Historical evidence

Older detailed execution history remains in Git history and `docs/checkpoints/`. Do not reconstruct the active plan from old narrative sections; use them only as evidence for the exact candidate/runtime they measured.
