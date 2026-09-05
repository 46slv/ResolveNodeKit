# ResolveNodeKit agent entrypoint

## Goal

Build compact, reversible node-workflow tools for DaVinci Resolve Fusion and Color. This is a Resolve-specific toolkit, not a Blender Node Wrangler port and not an Auto-Node-Tree fork.

## Authority order

1. current user instruction;
2. live local Git/worktree, current remote branch/PR, current tests, and live Resolve/Fusion readback;
3. `docs/CURRENT_STATE.md`;
4. `docs/ORCHESTRATION.md` and relevant repo contracts;
5. installed/current Resolve scripting documentation and measured host behavior;
6. historical checkpoints / prior-art notes;
7. inference.

Historical SHAs, project names, timeline names, comp identities, worker session IDs, and test counts are locators/evidence only. Fresh-read before acting.

## Required read order for long-running work

For any multi-stage, host-mutating, or autonomous continuation run:

1. inspect live Git status before pull/reset/rebase/checkout;
2. read `docs/CURRENT_STATE.md`;
3. read `docs/ORCHESTRATION.md`;
4. read the relevant feature/evidence contract (`docs/GROUPS.md`, `docs/HOST_VALIDATION.md`, `docs/COLOR_API.md`, `docs/EVIDENCE_PROTOCOL.md`);
5. read the newest applicable checkpoint under `docs/checkpoints/`;
6. choose the smallest ready gate from the dependency graph.

Do not replay chat history as the operating plan.

## Invariants

- Fusion and Color use separate adapters; never assume Fusion APIs exist on Color.
- Layout/display commands must not alter connections, processing parameters, keyframes, tools, media, grades, or render state.
- Preserve every `GroupOperator` and direct parent/child membership. Never flatten or ungroup merely to arrange the graph.
- Cross-boundary edges may be projected to a visible GroupOperator for layout planning only; never rewire the actual graph to match that projection.
- Host writes follow: target bind -> snapshot -> bounded mutation -> readback -> invariant comparison -> rollback on mismatch.
- Worker narration is not proof. Host success needs structured MCP evidence plus independent parent verification.
- Offline mocks do not prove Resolve/Fusion host behavior.
- Never blind-retry an ambiguous write or ambiguous ChatGPT/MCP delivery.
- Do not install watchers/services/startup items or change global Resolve keyboard shortcuts unless explicitly authorized.
- Auto-Node-Tree and Blender Node Wrangler are prior art/UX references only; do not vendor their source without explicit provenance/license review.

## Current repository authority

The current project authorization allows autonomous work inside ResolveNodeKit task branches: code/tests/docs edits, commits, pushes, and Draft PR updates. Do not merge to `main`, publish a release, force-push shared history, delete unrelated branches/work, or rewrite unrelated user changes without explicit authority.

If a host run leaves valuable local dirty work while the remote branch advances, preserve the local work first (temporary branch/checkpoint commit or patch), then reconcile. Never use `reset --hard` or cleanup as the first response to that condition.

## Completion semantics

A blocker belongs to the narrowest affected feature/lane. If another authorized independent gate is ready, the overall program status is `CHECKPOINTED`, not `BLOCKED_*`, and work continues.

The user's visual-group requirement is mission-critical: nested groups must eventually be openable while remaining groups, with their contents visible. A usable beta may checkpoint a host/API limitation, but `MISSION_COMPLETE` requires that requirement to pass or the user to explicitly waive/change it.

Keep strict names strict. `Tidy + Expand Groups` must fail closed when expansion is not proven. A hierarchy-preserving recursive tidy without visual expansion is a separate command/API.

## Current measured orientation

Use `docs/CURRENT_STATE.md` for the live ready queue, but keep these durable facts in mind:

- Flat Fusion Tidy is host-verified on the measured Resolve Studio 21.0.3.7 path.
- `Tidy Nested` is host-verified after fixed-point stabilization; repeated execution is stable and hierarchy/connection/display-state invariants held in the canary.
- Color read-only capability mapping is complete for the current project context; physical Color-node XY positioning is absent from the measured callable surface.
- Large ~1100-tool stress is currently transport-limited by long MCP/bridge calls; establish a transport-fitting chunk size and use compact evidence rather than repeating a whole-graph call.
- Visual runtime Group expansion remains mission-critical and unresolved. The serialized `LoadSettings(Expanded=true)` path is disproven on the measured host.

## Checkpoint discipline

After each meaningful host gate or phase transition:

- commit/push accepted task-branch work when safe;
- update the Draft PR;
- update `docs/CURRENT_STATE.md`;
- add a dated checkpoint only when it contains evidence worth preserving;
- record exact tests, host identity, worker route, mutations, readback, blocker, and smallest next gate.

Large-graph host gates must follow `docs/EVIDENCE_PROTOCOL.md` rather than relying on full-graph MCP dumps or worker narration. Establish a bounded/chunked transport envelope first.

See `docs/ORCHESTRATION.md` for the phase graph, stop rules, large-graph fallback, and resume contract.
