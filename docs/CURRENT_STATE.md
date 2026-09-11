# ResolveNodeKit current continuation

Updated: 2026-09-11 JST
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
- G04: `BLOCKED_CONTRACT`
- G05: `PENDING`
- G06: `PASS`
- G07–G08: `PASS`
- G09–G14: `PENDING`

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

## Direct product-gate run — 2026-09-11 (SO-30 / SO-40 / SO-50 / SO-60) [v3]

Checkpoint: `docs/checkpoints/2026-09-11-so30-so40-so50-direct-host-v2.json`

- Fresh owned Resolve Studio `21.1.0.14` / compatibility MCP `2.203.0` work used one live writer and window `6301810`. The SO-30/SO-40 disposable fixture was a non-empty depth-2 Group graph (16 tools after the SO-30 additions, 8 labelled edges) with TextPlus, RectangleMask, Blur, branch, isolated node, and protected input readback.
- SO-30 was proven in the actual Fusion FlowView by ordinary GUI context-menu operation: Flow context menu `Options > Orthogonal Pipes` (Japanese label `直交パイプ`) changed the displayed TextPlus->Merge, mask, serial, branch, and difficult-edge routing; the menu state was re-opened and read back. The same setting remained selected after opening a second owned timeline/comp, so the measured scope is application-level preference (not comp-local or Flow-local). It was restored to `Straight Pipes` before cleanup. This is an actual displayed-wire result, not a coordinate inference; `SO-30/G03 = PASS`.
- SO-40 used Fusion's normal Group context-menu `Ungroup` (`グループを解除`) on the deepest Group and then its parent. Readback immediately after the second operation was 14 tools, Groups `2 -> 0`, preserved non-Group IDs/RegIDs, parent membership `null`, exact labelled connections (including Background/Foreground/EffectMask), and protected TextPlus/Blur/Mask state. Standard Undo was measured: first Ctrl+Z restored the outer Group, second was a structural no-op, third restored the nested Group. The GUI semantic is identity-preserving evidence, but the one-owned-Undo exact contract is not met; `SO-40/G04 = BLOCKED_CONTRACT` and no product flatten PASS is claimed.
- SO-50 installed identity was fresh-read from `Workspace > Scripts > ResolveNodeKit_Arrange`: source and installed `ResolveNodeKit_Arrange.py` SHA256 are `9C35CA8984163DA0AD2E00899C0EBA2B2C9B08FE039C32EFA235DC367A85AFCE`. The RNK-owned window was obtained by title/shape identity inside Resolve (not OS foreground activation). Cancel run `45ed02daee914c3b9e29774a1db31de1` produced two visible Cancel attempts and `event=cancelled`; the 16-tool graph remained unchanged (zero write). A nested Run `1cfb001b535f460ea993818e268e1997` correctly showed busy/result events but refused on Group rollback, so it is failure evidence only. A flat 9-tool SO-30 fixture then completed Run `b44bd2bea0c442bebdf4e390f1e2fec0`: setup/OK widget, same-controller target bind, `busy shown -> snapshot/readback -> busy hidden -> result shown`, 9 tools / 5 edges, and identity/port/TextPlus/Mask/Blur/Blend readback. The installed UI gate is `SO-50/G06 = PASS`; the fast busy phase was event-read from RNK's run log rather than a separately retained screenshot.
- SO-60 used a fresh disposable still-media timeline/comp (`RNK_SO60_E2E_20260911`, `コンポジション5`) with flat, fan-out, mask, isolated, and GUI-created non-empty Group content. The first installed run refused only because Resolve exposed unpositioned `Left AudioDisplay`/`Right AudioDisplay` tools; those two owned fixture-only display tools were deleted and the controller then completed on 10 positioned tools. Run `0800c59026864165b66176ed540ee23e` moved 9 tools and preserved labelled connections plus TextPlus/Mask/Blur/Blend values. A same-controller stability run `7c9fa40309cc4f93a9c6622fc58e04e3` reported `moved=0` with identical geometry. A GUI-created Group containing `RNK_SO60_BG` and `RNK_SO60_BLUR` was preserved by run `96a6c85a102e4466bb0a72a8639b19fc` (`moved=3`) and run `883b4277cace4fd7873358f77f44a292` (`moved=0`): non-Group IDs/RegIDs, Group parent identity, exact labelled ports and protected inputs stayed intact. Undo probe run `08c2ff6a8aa644b09f236d2d77c59c99` was changed once, then one standard Ctrl+Z restored the complete pre-run snapshot (`equal=true`, Group remained), so `SO-60/G07/G08 = PASS`.
- Cleanup used the same writer with no project save: the SO-60 live timeline and its two auto-created archive timelines were deleted via exact confirmation (`3 -> 0`), the imported `img20.jpg` clip was deleted via exact confirmation, `folder.get_clips` returned `[]`, the final timeline list is empty, and current project remains `RNK_DIRECT_GATES_20260911_PROJECT`.
- G01–G14 after these gates: `G01 PASS`, `G02 BLOCKED_TECHNICAL`, `G03 PASS`, `G04 BLOCKED_CONTRACT`, `G05 PENDING`, `G06 PASS`, `G07 PASS`, `G08 PASS`, `G09–G14 PENDING`. SO-61 remains dependent on the SO-40 contract blocker; SO-70 and SO-80 are the next preserve/recovery lanes after their explicit prerequisites.
- The evidence-only docs were published on the task branch and pushed to PR #5 at evidence commit `3871dac`; PR #5 remains OPEN/Draft and `main` is untouched. The final remote ref is re-read after the metadata push and reported with the exact SHA below.

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

1. resolve the SO-40 one-owned-Undo product flatten contract, using the already-proven GUI Ungroup semantic without rebuilding execution infrastructure;
2. continue SO-70/SO-80 only when their explicit preserve/recovery prerequisites are ready;
3. preserve the direct route and existing mechanical guard; do not rebuild the retired Operator/WP1 transport;
4. if one product gate blocks, continue another authorized independent ready gate.

## Stop boundary

Do not stop merely because a historical Operator/WP1 route is blocked.

Stop only for a genuine authority/input boundary, unrecoverable valuable-state risk, no remaining authorized ready product work, or actual completion of the existing acceptance contract.

## Authority

Authorized: task-branch code/tests/docs, backup-backed install, commit/push/Draft PR updates, direct Resolve MCP/scripting/GUI, Resolve launch/quit/restart, owned scratch/disposable fixtures and reversible validation mutations.

Not authorized by this state file: valuable project save, main merge/release, force-push shared history, credential changes, unrelated destructive OS/process work, PC reboot, global shortcut mutation or permanent service/startup installation.

## Historical evidence

Older detailed execution history remains in Git history and `docs/checkpoints/`. Do not reconstruct the active plan from old narrative sections; use them only as evidence for the exact candidate/runtime they measured.
