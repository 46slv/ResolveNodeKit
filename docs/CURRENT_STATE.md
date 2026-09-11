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
- G03: `BLOCKED_TECHNICAL`
- G04–G14: `PENDING`

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

## Direct product-gate run — 2026-09-11 (SO-30 / SO-40 / SO-50)

Checkpoint: `docs/checkpoints/2026-09-11-so30-so40-so50-direct-host.json`

- Fresh owned timeline `RNK_SO30_SO40_20260911` was created on Resolve Studio `21.1.0.14` / compatibility MCP `2.203.0`. The 15-tool fixture contained a non-empty `OuterG -> InnerG` depth-2 hierarchy, 8 edges, a RectangleMask edge, an unconnected branch, and processing readback (`TextPlus`, Blur size, mask dimensions/center).
- SO-30 reached the real Fusion FlowView: the current screenshot showed horizontal BG->Merge->Blur->MediaOut wires, a visible mask wire and collapsed Group boundary, but TextPlus->Merge stayed diagonal despite equal node Y. The direct FlowView surface exposed position methods only (`GetPos`, `GetPosTable`, `QueueSetPos`, `FlushSetPosQueue`, `SetPos`) and no pipe/wire geometry or orthogonal-mode callable. `SO-30/G03` therefore remain `BLOCKED_TECHNICAL`; node coordinates are not treated as a strict-view PASS.
- SO-40 ran the product `flatten_all_comp` seam against the non-empty fixture. The host exposed no explicit identity-preserving `Ungroup` callable; `DoAction`/`QueueAction` were present only as generic methods and are not accepted by the contract. The seam refused before mutation with `FusionHostError: Flatten-all is unavailable...`; tools stayed `15 -> 15`, groups `2 -> 2`. This is `BLOCKED_HOST_API` evidence, not a PASS; `SO-40/G04` remain unqualified.
- SO-50 installed identity is fresh-read: `script_plugin.list(category=Comp, all=true, language=py)` returned `ResolveNodeKit_Arrange.py`; the installed entry hash is `9C35CA...85AFCE`, all 19 manifest package hashes match the current worktree, and the manifest commit is `5306b4b...a8d2a1d` (product files unchanged through the current head). The menu entry could not be safely activated: fresh `list_apps/list_windows/get_window/get_window_state` plus Raise/activation recovery repeatedly returned `failed to activate captured window`. No menu click, Cancel, Run, busy/result, or same-controller UI claim is made; `SO-50/G06` remain `PENDING`.
- Cleanup completed under the same single Resolve writer: `RNK_SO30_SO40_20260911` timeline deleted with verified `1 -> 0`, imported clip `ff07881b-2398-40d8-a93f-ebc913ef5384` deleted and read back absent, current Fusion comp `コンポジション2` has `0` tools, and no project save was issued. Resolve remains GUI-responsive, Fusion page, one instance.
- G01–G14 matrix remains: `G01 PASS`; `G02/G03 BLOCKED_TECHNICAL`; `G04–G14 PENDING`. SO-60 and later remain dependency-gated until SO-30 and SO-50 are actually PASS.

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

1. qualify SO-30 actual strict view and SO-50 installed UI on a fresh owned fixture;
2. continue independent SO-40 flatten/offline work where dependencies are ready;
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
