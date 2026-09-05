# ResolveNodeKit agent entrypoint

## Goal

Build compact, reversible node-workflow tools for both DaVinci Resolve Fusion and Color. The product goal is faster node editing, not parity with Blender Node Wrangler and not a fork of Auto-Node-Tree.

## Authority

1. current user instruction;
2. current repository code/tests/host evidence;
3. current installed Resolve scripting docs and runtime probes;
4. committed docs/prior-art notes;
5. inference.

## Long-running execution

Before a multi-stage, host-mutating, or autonomous continuation run, read `docs/ORCHESTRATION.md`. It defines the parent/worker/verifier roles, ordered phase gates, autonomous mutation authority, stop/escalation rules, expected blockers, and checkpoint/resume contract. Live repo/host state still outranks the document's snapshot wording.

For the current measured Fusion host state, also read `docs/checkpoints/2026-09-05-host-group-expansion-blocker.md`. It records the proven flat-Tidy host behavior, the local-only grid/readback fixes that must be reconciled with the newer remote branch, and the measured failure of `LoadSettings(Expanded=true)` to persist runtime Group expansion on Resolve Studio 21.0.3.7.

## Invariants

- Keep Fusion and Color adapters separate; never assume a Fusion API exists on Color or vice versa.
- Layout-only commands must not alter connections, parameters, keyframes, tools, grades, renders, or media.
- Group layout must preserve every `GroupOperator` and direct parent/child membership. Never flatten or ungroup merely to make a graph easier to arrange.
- Cross-boundary edges may be projected to the visible GroupOperator for layout planning only; never rewire the actual graph to match the projection.
- For host writes: snapshot -> bounded mutation -> readback -> rollback on failure. Use host Undo where verified.
- Offline mocks do not prove Resolve/Fusion host behavior.
- Do not install watchers, services, login-start items, or change the user's Resolve keyboard shortcuts unless explicitly requested.
- Auto-Node-Tree is prior art only. Do not copy its source into this repository without explicit provenance/license review.
- Prefer small commands with deterministic tests over a monolithic automation daemon.
- Keep the strict `Tidy + Expand Groups` meaning fail-closed. A recursive-tidy-only path must be a separate command/API rather than a flag that silently weakens expansion acceptance.

## Current next gates

1. Reconcile the host-run local dirty changes (`tidy.py`, `recursive_groups.py`, `docs/GROUPS.md`, `tests/test_fusion_host_grid.py`) with the fresh remote task-branch head without losing either side; rerun the full suite.
2. Close the flat-Tidy host gate with the measured FlowView grid/readback corrections integrated.
3. Canary a separate recursive hierarchy-preserving tidy path that does not require Group visual expansion. Only implement it if collapsed-group child positions are host-readable/writable with membership/connection invariance.
4. Investigate the actual runtime Group Expand/Collapse action path. Do not continue retrying serialized `Expanded=true` settings without new evidence; the measured host discards that state on readback.
5. If no readback-verifiable expansion action exists, classify visual expansion specifically as `BLOCKED_API` and continue independent Fusion layout/selection utilities.
6. Run the read-only Color probe against the installed Resolve version and record the actual graph API boundary before implementing Color writes.
