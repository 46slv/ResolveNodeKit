# Host checkpoint - Semantic Arrange gate 1 nested preserve - 2026-09-06

Status: `PASS`. Nested-Group preserve-mode Arrange is host-proven on a disposable fixture.

Worker route: OpenCode CLI 1.18.29 -> model `opencode-go/muse-spark-1.3-contributor` (agent `build`) -> davinci-resolve MCP 2.203.0 -> Resolve Studio 21.0.3.7, project PSD2Fusion. Structured events: `%TEMP%\\rnk-nest3\\events.json` (fresh worker; an earlier sibling run stalled during fixture research and was left untouched on its own disposable).

Repo under test: `013a083` on branch `feat/semantic-arrange-v1-20260906`, Draft PR #5.

## Fixture (R1-recipe Paste, proven shape, single attempt, no wrapper)

Python `run_inline`, timeout 200, no Lock/Unlock wrapper. Blocks derived live from `SaveSettings` of temporary flat tools (deleted after capture), explicit `ViewInfo` positions with all children identical, in-payload `SourceOp`/`Source` wiring, nested `OrderedDict` assembly, one `comp.Paste` of top `OuterG`:

- `OuterG` kids `[BGout, BLOut, InnerG]`, `InnerG` kids `[BGin, BLin, MGin]`
- plus root `AddTool` Background BG and Merge M1 (short calls), wired `BLOut -> M1` Foreground, `BG -> M1` Background, `M1 -> MediaOut1` Input
- total 10 nodes, 6 edges; pre positions clustered

Hand-written minimal settings tables were NOT used; an earlier hand-written Lua Paste attempt timed out with `-32001` and dropped session tools. The SaveSettings-derived Python shape is the proven envelope. Never repeat the single 8-tool hand-written Paste.

## Results

- Run1 `arrange_comp(include_unselected=True)`: moved 9, scope_count 3, arranged 10; membership per group identical; edges identical.
- Run2 identical call: moved 0, positions byte-identical to run1.
- `comp.Undo()`: all 10 positions restored to pre exactly.
- Cleanup: `RNK_NEST2` plus auto-archive deleted with identity guard. Final: Timeline 1 current with all comps `Modified=false`; sibling `RNK_NEST` names never touched. No project save.
- Parent independently verified run1 `moved_count 9 / scopes 3 / arranged 10` and run2 `moved_count 0` in the raw event stream.

## Remaining for FIRST_USABLE

- Gate 2: selection-only host API discovery plus disposable proof, or a precise API boundary checkpoint (in flight separately).
- Dialog human gate: AskUser shape, Cancel zero-mutation, menu Run with the user at the machine.
- Comp Scripts install only after the dialog gate.
- Ungroup stays fail-closed until exact restoration is proven on a disposable fixture.
