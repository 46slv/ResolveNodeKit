# Strict first package — 2026-09-10

The requested G02/G03 first package was delegated to the external Resolve
Operator only. G01 was carried and not replayed; no timeline was attached, no
flatten/ungroup path was retried, and no project save occurred.

The native route was first repaired for namespace selection, then retried after
a separate compatibility recovery. Resolve Studio `21.1.0.14` was recovered to
a GUI-ready PID by the compatibility Operator with zero mutation/save. The
native route nevertheless continued to report Resolve unreachable and refused
before fixture binding. Every host attempt ended with exact lease `FREE` and
fixture/graph/layout/settings/Undo/save mutation zero. Therefore strict
preserve, FlowView mapping, processing invariance, run2 stability, and actual
view/wire were not evaluated and G02/G03 remain `BLOCKED_TECHNICAL`.

The independent offline lane added the missing position-only host seam:

- `StrictPlan` now exposes local per-Group placements and materialization offsets;
- processing-to-planner mapping preserves `GroupOperator` identity;
- `strict_apply` maps logical cells to calibrated FlowView coordinates using a
  scope-local anchor, requires explicit live tool handles, checks pre-state
  identity, writes positions only, reads every position back, compares the
  complete post processing signature, rolls back on mismatch, and can execute
  a two-run stability check;
- incomplete snapshots and handle coverage refuse before any write.

Verification from the canonical worktree: focused strict-apply `4/4`, full
unittest `174/174`, `compileall` PASS, `git diff --check` PASS. This is offline
implementation evidence only; it does not promote a host gate or claim native
wire realization.

Evidence: sibling JSON, plus Operator launch IDs `58b4cab2-a508-4ce1-97ab-28b12a5c40cf`, `5b8cc8fe-ee43-4900-a265-5630049f2d6a`, `792c4fbe-e826-45ff-b08c-99ad2aad7cc2`, `8ef36cf7-dca2-41f4-b72b-2957b417e539`, and `fcb05a07-10f8-435b-aebc-21f54184bbe8`.
