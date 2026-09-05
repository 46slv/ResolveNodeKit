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

## Current next gates

1. Keep `python -m unittest discover -s tests -v` green.
2. Run Fusion Tidy Graph against a disposable host comp, then a duplicate of a real graph.
3. Verify position readback, repeat-run stability, Undo, save/reopen, and connection/parameter invariance.
4. Host-verify `Tidy + Expand Groups` on 2–3 nested levels; prove Expanded readback, membership/connection invariance, and whether expanded `GroupInfo` automatically fits all direct children. Measure `Size`/`Scale`/`Offset` before implementing fit-to-contents.
5. Run the read-only Color probe against the installed Resolve version and record the actual graph API boundary before implementing Color writes.
