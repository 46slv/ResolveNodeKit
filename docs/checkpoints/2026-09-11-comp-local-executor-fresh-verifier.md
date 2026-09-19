# WP1 fresh verifier and install readback — 2026-09-11

An independent parent-side readback followed the two WP1 Operator probes. The
PR #5 worktree and remote branch both resolve to `649ce7d`; the source/script
change from the product parent is empty, and the worktree is clean before this
verifier checkpoint is added.

- RNK canonical suite: `174/174 PASS` with explicit worktree `src` import.
- Operator focused suite: `15/15 PASS`.
- `compileall`, `git diff --check`, and the strict contract checker pass; the
  checker correctly reports `product_completion_record_consistent=false`,
  `runtime_evidence_authenticated=false`, and `host_tests_executed=false`.
- The backup-backed installer was rerun from the PR HEAD after the prior
  manifest/blob provenance mismatch. It now records `repo_commit=649ce7d`,
  19 package files plus the entry, zero raw source/installed mismatches, and
  19/19 normalized source blobs matching the commit. The old entry was backed
  up under the installer-owned backup tree. Imports from `%TEMP%` resolve all
  strict modules inside the installed root.
- Operator revision
  `21ac220fe0877194fbe8c01687642729906cf1c333cdaf80f148cf9d12bfa90a`
  remains unchanged with 17 files; parent direct Resolve access is zero.

The fresh verifier does not promote any host gate: WP1 remains `BLOCKED`, WP2
position/Undo counters are zero, the final Operator lease is `FREE`, G02/G03
remain `BLOCKED_TECHNICAL`, G08/G04 remain pending, and product completion is
false. Machine-readable evidence is
[`2026-09-11-comp-local-executor-fresh-verifier.json`](2026-09-11-comp-local-executor-fresh-verifier.json).
