# Fusion GroupOperator tidy contract

ResolveNodeKit must support deeply nested Fusion `GroupOperator` trees without ungrouping them.

## Required behavior

`Tidy + Expand Groups` treats every GroupOperator as both a node in its parent scope and a container with its own child scope.

- preserve GroupOperator membership;
- recursively discover children with `GetChildrenList()` and parent ownership via `ParentTool` / `TOOLH_GroupParent`;
- expand every GroupOperator by setting `ViewInfo.Flags.Expanded = true` through `SaveSettings` / `LoadSettings`;
- run deterministic layout independently at root and inside every nested group;
- project cross-boundary connections to the visible group node for layout planning only;
- never rewire a connection to achieve layout;
- verify hierarchy, connection signatures, positions, and Expanded readback;
- wrap the operation in one Undo event when available;
- rollback positions and group settings if any expansion or position write fails.

This is intentionally separate from `tidy_comp()` until the real Resolve/Fusion host behavior is verified.

## Why per-scope layout is necessary

Flattening a nested graph loses the visual meaning of a GroupOperator. For an edge from a node inside `GroupB` to a sibling node inside `GroupA`, the `GroupA` layout sees `GroupB -> sibling`, while the `GroupB` layout sees the real internal edge. The connection itself is not changed.

## Offline validation

Focused recursive-group tests cover:

1. two nested GroupOperators remain grouped, both expand, and root/parent/nested scopes each receive a layout;
2. a second run is position-identical and performs no unnecessary expansion;
3. failure while expanding a nested group restores earlier group state and original positions and discards the Undo event;
4. a malformed parent-group cycle fails before any position write.

Current focused result: **4/4 PASS** with `compileall` PASS. This is mock/API-contract evidence only, not a Resolve/Fusion host claim.

## Host-only gate: fit to contents

Offline mocks can prove recursive discovery, scope projection, deterministic positions, expansion-state handling, and rollback. They cannot prove the Fusion UI's `GroupInfo.Size`, `Scale`, and `Offset` behavior.

The user-visible requirement is stricter than merely setting `Expanded = true`: after host validation, every expanded group must show all direct children without clipping. Do not invent a `GroupInfo.Size` formula from setting-file examples. Measure the installed Resolve/Fusion behavior first, then either:

1. confirm Fusion automatically sizes/frames the expanded group after the child positions are written; or
2. add a measured, readback-verifiable `Size` / `Scale` / `Offset` fit step.

Until that host gate passes, report the feature as recursive expand + tidy, not fully host-verified fit-to-contents.

## Evidence basis

Fusion's scripting reference documents `TOOLH_GroupParent`, the `Operator.ParentTool` convenience property, `Operator.GetChildrenList()`, and `Operator.SaveSettings()` / `LoadSettings()`. Real GroupOperator settings serialize nested tools under `Tools = ordered() { ... }` and expanded UI state under `ViewInfo = GroupInfo { Flags = { Expanded = true, ... } }`.

## Host measurement (Studio 21.0.3.7, 2026-09-05, project PSD2Fusion / Timeline 1)

Measured live via the OpenCode worker path (`opencode-go/muse-spark-1.3-contributor`,
agent `build`, davinci-resolve MCP over `run_inline`). The previously open
Timeline 1 (5 items, 1107-tool Fusion comp, 31 nested `GroupOperator`) was the
target; disposable/duplicate timelines used for validation were removed afterwards.

- `GetToolList` / `CurrentFrame.FlowView` / `GetPosTable {1:x,2:y}` / `SetPos` /
  `QueueSetPos` / `FlushSetPosQueue` / `StartUndo` / `EndUndo` / `Undo` all present.
- FlowView grid snap (GridSnap on): X snaps to 0.5, Y to whole numbers, ties snap
  down. Readback carries a stable per-type frame offset (normal tools +0.009 on Y;
  e.g. `EllipseMask` +0.073/+0.054). `tidy.py` snaps desired positions to that grid
  (`_snap_position`) and verifies readback with `FLOW_POSITION_TOLERANCE = 0.1`,
  which still fails closed on real grid differences (>= 0.2). Regression tests:
  `tests/test_fusion_host_grid.py`.
- `SaveSettings` deserialization evals `OrderedDict(...)`; without `OrderedDict`
  in builtins the call succeeds but returns `Tools=None`. Guarded by
  `_ensure_ordered_dict()`.
- `tidy_comp` on a disposable comp: BG+FG->Merge, serial chain, `EffectMask`
  branch, isolated node all PASS; second run `moved=0`; one Undo restores.
- Group expansion is BLOCKED on this host: live `ViewInfo` is
  `GroupInfo {Pos,Flags,Size,Direction,PipeStyle,Scale,Offset}` with no `Expanded`
  key when collapsed. Setting `Flags.Expanded=true` + `LoadSettings` returns True
  but is silently discarded on readback (empty and 7-child groups, with and without
  Undo; `Size`/`Scale`/`Offset` unchanged). No `Expanded` in `GetAttrs`; guessed
  FlowView `DoAction` names all return False. `tidy_groups_comp` therefore keeps its
  fail-closed expand+readback contract and refuses on this host instead of guessing.
- Full 1107-tool snapshot over remote `run_inline` times out (55k+ remote calls);
  large-graph tidy must run in-process (Resolve Scripts menu entrypoint
  `scripts/Fusion/ResolveNodeKit_TidyGroups.py`), not via remote calls.
