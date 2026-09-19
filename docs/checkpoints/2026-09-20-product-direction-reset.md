# 2026-09-20 — Product direction reset and v1 Arrange/Preserve checkpoint

## Result

`PRODUCT_DIRECTION_RESET: PASS`

The current mission is now formally separated:

```text
v1: Arrange / Preserve
    Arrange -> optional Resolve native GUI manual Ungroup -> Re-Arrange

v2: RNK Automatic Ungroup / UngroupFirst / Flatten All
```

The pre-reset PR head was `1035217b71f62b2347da20460ff30cdf5d03b8b3`. The
direction-reset contract is committed as
`1ab8a458e0c1e4731bc66a67a564fc4d89b984d8` and pushed to PR #5's head branch.
The follow-up evidence/checkpoint commit is
`66ff8886a88bd96ed07387cdd5f6702401ea7592`.

## Durable contract changes

- `docs/PRODUCT_DIRECTION_BRIEF.md` is the product decision record.
- `docs/execution/v1-arrange/` is the active v1 execution and acceptance owner.
- `docs/CURRENT_STATE.md` and the repository `AGENTS.md` now route current work
  to v1 Arrange/Preserve.
- The old strict G01-G14 lane and its flatten evidence remain under
  `docs/execution/strict-orthogonal/` as preserved v2/research material.
- The old semantic-arrange continuation remains historical evidence; its
  flatten amendment is not v1 authority.
- Normal v1 UI does not expose automatic Ungroup, UngroupFirst or Flatten All.
  The installed production confirmation is preserve-only.

## v1 acceptance state

The machine-readable contract is
`docs/execution/v1-arrange/acceptance.json`.

| Area | State |
| --- | --- |
| Flat, Group-preserving and nested Arrange | PASS / PASS_WITH_SCOPE |
| Fan-out, multiedge, Mask, branch, identity, parents and endpoints | PASS / PASS_WITH_SCOPE |
| Undo/rollback and stable run 2 | PASS / PASS_WITH_SCOPE |
| Installed Run/Cancel/busy/result UI | PASS_WITH_SCOPE |
| Real duplicate and large preserve/performance evidence | PASS / PASS_WITH_SCOPE |
| Recovery and cleanup | PASS |
| Candidate source/install/package identity | PASS |
| Same-fixture Arrange -> native manual Ungroup -> Re-Arrange | NEEDS_SMALL_RECHECK |
| Fresh independent verifier | PASS; overall candidate still awaits the host E2E |

Automatic flatten, large flatten, flatten processing/render equivalence,
automatic flatten rollback, strict machine-readable geometry surfaces and
strict displayed-wire collection are explicitly v2/research items. They do not
block v1 unless the actual Arrange result is visually broken.

## Candidate install readback

The backup-backed user install was refreshed from the direction-reset commit
and again from the follow-up checkpoint commit. Both readbacks passed. The
final docs-only checkpoint is followed by one last install/readback so the
manifest's `repo_commit` matches the final PR head; the immutable package
identity is:

- install root: `C:/Users/shiro/AppData/Roaming/Blackmagic Design/DaVinci Resolve/Support/Fusion/ResolveNodeKit`
- manifest package count: `19`; total installed files reported by installer: `20`
- package mismatches: `0`
- source and installed entry SHA256:
  `9C35CA8984163DA0AD2E00899C0EBA2B2C9B08FE039C32EFA235DC367A85AFCE`
- production confirmation: `include_unselected=True, ungroup=False`
- production confirmation contains no checkbox
- installed entry contains no `UngroupFirst` label

## Fresh independent verifier

A fresh read-only verifier inspected the follow-up checkpoint and returned
`CHECKPOINTED_PENDING_RECHECK`:

- documentation workflow and active v1 owner: PASS;
- v1 acceptance JSON and all referenced evidence paths: PASS;
- all old strict G01-G14 statuses and evidence: preserved, PASS;
- live manifest/package hashes and preserve-only production confirmation: PASS;
- explicit-src offline tests and `git diff --check`: PASS;
- same-fixture installed Arrange -> native GUI Ungroup -> installed Re-Arrange:
  not evidenced, `NEEDS_SMALL_RECHECK`.

The verifier correctly treated the separate SO-40 and SO-60 fixtures as
insufficient for the combined workflow.

## Verification and host boundary

- `python -m unittest discover -s tests -q`: `175 tests`, `OK` with the PR
  worktree's explicit `src` path.
- Strict contract tests: `30/30`, `OK`.
- `compileall`: pass.
- JSON acceptance/evidence-path validation and `git diff --check`: pass.
- Resolve restart was attempted against the exact installed executable. The
  post-restart process is responsive and shows the project manager to Windows,
  but no targetable Resolve app/window is exposed through the available CUA.
- No Resolve graph mutation, valuable-project save, main merge, release or
  tag was performed during this reset.

The existing SO-40 native Ungroup evidence and SO-60 Arrange evidence are
separate fixtures. They must not be relabelled as the required same-fixture
workflow. Therefore the manual E2E remains `NEEDS_SMALL_RECHECK` rather than a
synthetic PASS.

## v2 resume trigger

Resume the preserved strict/flatten lane only after a measured,
identity-preserving native ungroup bridge exists with complete readback,
rollback/render qualification, a transport-fitting large route and a separate
v2 verifier. Do not revive the legacy Operator/WP1/HostSession architecture.
