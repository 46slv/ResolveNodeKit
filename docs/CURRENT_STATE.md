# ResolveNodeKit current state

Updated: 2026-09-20 JST

Status: `V1_DIRECTION_RESET / CHECKPOINTED`

Live Git/PR/installed/runtime evidence outranks this short operational pointer.

## Current product mission

ResolveNodeKit v1 is **Automatic Node Arrange / Preserve**:

```text
Arrange -> optional Resolve native GUI manual Ungroup -> Re-Arrange
```

v1 preserves GroupOperators and processing structure. Automatic Ungroup,
`UngroupFirst` and Flatten All are v2 research/backlog items. They are not v1
release blockers and are not exposed as normal v1 UI.

Canonical current owner:

- `docs/PRODUCT_DIRECTION_BRIEF.md`
- `docs/execution/v1-arrange/README.md`
- `docs/execution/v1-arrange/PLAN.md`
- `docs/execution/v1-arrange/acceptance.json`
- `docs/execution/v1-arrange/EVIDENCE_MATRIX.md`

Preserved v2/research owner:

- `docs/execution/strict-orthogonal/README.md`
- `docs/execution/strict-orthogonal/PLAN.md`
- `docs/execution/strict-orthogonal/LUNA_RUNBOOK.md`
- `docs/execution/strict-orthogonal/acceptance.json`

The old `docs/execution/semantic-arrange-v1/` continuation is retained as
historical evidence. Its preserve evidence is eligible for v1 carry-forward;
its flatten amendment is not current v1 authority.

## Live identity read at direction reset

- Repository: `46slv/ResolveNodeKit`
- PR: `#5`, OPEN, Draft
- PR head rechecked before this reset: `1035217b71f62b2347da20460ff30cdf5d03b8b3`
- PR head branch: `feat/semantic-arrange-v1-20260906`
- Active PR worktree: `D:/Documents/ResolveNodeKit-pr5-v2-integration`
- Local branch in that worktree: `feat/direct-guarded-reset-20260911`
- Worktree was clean before the direction-reset edits; `main` was not merged
- User install manifest before refresh: `repo_commit=92998ec59c56d2f0ef8568a4a425980dc5093d29`
- Installed package: 19 Python files, entry + package hashes matched the PR
  worktree source tree, installed-root import previously passed
- Resolve executable: `C:/Program Files/Blackmagic Design/DaVinci Resolve/Resolve.exe`
- A fresh launch was requested during this reset; the process was observed as
  PID `6484`, window title `Resolve`, `Responding=false`, and no targetable
  app/window was exposed by the available CUA inventory. No host mutation or
  project save was performed in this reset.

The manifest commit label is stale relative to the PR docs head even though the
package bytes match. Refresh it after the final candidate commit and read back
the manifest, entry hash and package hashes together.

## v1 carry-forward status

The detailed matrix is in `docs/execution/v1-arrange/EVIDENCE_MATRIX.md` and the
machine-readable state is in `acceptance.json`.

Already valid for v1, with scope recorded:

- flat Arrange and whole-comp production seam;
- Group-preserving Arrange and non-empty nested Group behavior;
- fan-out, multi-edge, Mask and branch representative coverage;
- tool identity, parent/membership, topology and endpoint-loss readback;
- exact small-fixture Undo/rollback and stable run2;
- installed Run / Cancel / busy / result behavior;
- real PSD2Fusion duplicate Arrange at 1198 tools / 1173 non-Group tools;
- depth-4 1134-tool scale fixture with 1100 non-Group tools, explicitly
  recorded as 1075 source-derived plus 25 owned padding tools;
- three real-changing large preserve actions at 15.0752s / 12.8013s /
  13.0515s, plus a separate stable run2;
- recovery, no-save cleanup and historical fresh-verifier evidence.

The following are the only open v1 candidate items at reset:

1. same-fixture installed Arrange -> native GUI manual Ungroup -> installed
   Re-Arrange E2E, including readback, run2, Undo/recovery and cleanup;
2. final candidate install/manifest/source identity readback;
3. fresh independent verifier for the new v1 contract and final PR metadata.

If the Resolve control surface remains unavailable, keep item 1 as
`NEEDS_SMALL_RECHECK`; do not convert separate native-Ungroup and Arrange
fixtures into an unearned same-workflow PASS.

## v2 / strict research status — preserved, not rewritten

The old strict contract remains intact as a research lane. Current carried
statuses are:

```text
G01 PASS       G02 BLOCKED_TECHNICAL  G03 PASS
G04 PASS       G05 BLOCKED_TECHNICAL  G06 PASS
G07 PASS       G08 PASS               G09 PENDING
G10 BLOCKED_TECHNICAL                 G11 PENDING
G12 PASS       G13 PENDING            G14 PENDING
```

The strict lane still records the measured absence of an installed-callable
identity-preserving Ungroup primitive, incomplete strict large-graph
rectangle/grid/display surfaces, and flatten-specific processing evidence
gaps. Do not change those records to PASS for the v1 reset.

## Host-safety and architecture

Normal host work remains:

```text
Luna Max Product Worker -> direct Resolve MCP/scripting/GUI
  -> minimal mechanical Host Guard -> Resolve
```

Keep one state writer, one live Resolve writer, exact target binding,
owned/disposable state, no blind retry, bounded mutation, readback,
rollback/recovery, cleanup and no valuable project save. Do not revive the
retired Operator/WP1/HostSession topology.

## Next gates

1. Run the focused/offline contract checks for the new v1 owner.
2. Install the final PR candidate with backup-backed installer and read back
   source/install/package identity.
3. Use a fresh disposable/duplicate for the manual Ungroup -> Re-Arrange E2E if
   a direct Resolve surface becomes available.
4. Add a dated v1 checkpoint with exact evidence and have a fresh verifier
   inspect the final candidate.
5. Update PR #5 title/body and re-read the remote head. Finish at
   `V1_RELEASE_CANDIDATE`; do not merge `main` or publish a release.

## Learning Gate

The product-direction split is the only new generic decision in this reset:
keep v1 preserve independent, retain strict/flatten evidence as v2, and use
manual native Ungroup as the explicit v1 boundary. Do not create another
generic orchestration framework.
