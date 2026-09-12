# Semantic Arrange v1 large preserve optimization — 2026-09-08

Status: `PASS_STRUCTURAL_AND_IDEMPOTENCE`; processing hash remains explicitly `NOT_COLLECTED_BY_HOST_ADAPTER`.

Candidate: `59eeffbce5efd0a73a0fed2a4f3418faf71d5852` on
`feat/arrange-uia-e2e-20260906`, pushed fast-forward to PR #5 head
`feat/semantic-arrange-v1-20260906`.

## What changed

The production seam now records the complete arrange-stage timing envelope,
reuses the snapshot's live tool handles, batches FlowView position writes with
the measured `QueueSetPos` / `FlushSetPosQueue` surface, and reuses the
output-oriented connection walk for structural readback.  Empty output lists
are treated as complete no-edge surfaces; an actually partial output surface
falls back to the compatibility input walk instead of silently dropping edges.

This replaced the historical ~967-tool timeout path with compact, bounded
installed-package executions.  No full graph rows were returned through MCP.

## Host evidence

Resolve Studio `21.0.3.7`, project `PSD2Fusion`, Fusion page, disposable
timelines only, `ArrangeDialogState(include_unselected=True, ungroup=False)`:

- 977-tool fixture: run1 `moved=4`, run2 `moved=0`; each run completed in
  `16.867s` / `15.386s`; tool/group/edge/parent invariants and overlap=0 held;
  one owned Undo restored the exact pre-position and grouped state.
- 1110-tool fixture (the amended `>=1100` target): run1 `moved=992`, run2
  `moved=0`; each run completed in `17.209s` / `17.172s`; tool/group/edge/parent
  invariants and overlap=0 held; one owned Undo restored the exact pre-position
  and grouped state.
- Both runs used the installed per-user package and returned structured
  `success`; the Resolve/fuscript endpoint stayed available.
- The compact hashes, all stage timings, and run2/Undo flags are in the sibling
  JSON checkpoint.

The host adapter did not collect a full processing/keyframe/media hash on this
large pass.  That status is preserved as `NOT_COLLECTED_BY_HOST_ADAPTER`, not
converted into a processing PASS.

## Final host cleanup

The exact four owned IDs (`_mcp_RNK_SAV1_55_20260908`, its `_archived_v01`,
`_mcp_RNK_SAV1_60R_20260908`, and the worker-created
`Timeline 1_archived_v05`) were deleted after returning to `Timeline 1`.
Fresh readback showed exactly one timeline, `Timeline 1` current, 967 tools,
`COMPB_Modified=false`, Fusion page, Resolve responsive, and no project save.
