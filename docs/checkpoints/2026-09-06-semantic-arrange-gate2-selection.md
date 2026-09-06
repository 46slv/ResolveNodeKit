# Host checkpoint - Semantic Arrange gate 2 selection-only - 2026-09-06

Status: `PASS` with one honest scope note (multi-node movement implied, see below).

Worker route: OpenCode CLI 1.18.29 -> model `opencode-go/muse-spark-1.3-contributor` (agent `build`) -> davinci-resolve MCP 2.203.0 -> Resolve Studio 21.0.3.7, project PSD2Fusion. Structured events: `%TEMP%\\rnk-sel` (MCP-surface discovery) and `%TEMP%\\rnk-selprobe` (raw-API probe plus arrange proof).

Repo under test: `013a083`, then `4def6a0` for closeout; branch `feat/semantic-arrange-v1-20260906`, Draft PR #5. Code fix `d829754` followed from this gate.

## Discovery (rnk-sel, read-only, Timeline 1 observe-only)

- Every sampled tool exposes readable `TOOLB_Selected: false`. No `TOOLS_Selected` key exists.
- MCP surface has no selection setter: `get_tool_list` takes only a type filter, capabilities list no selection writer, `api_truth` has no `GetToolList` selection gate, timeline actions list none.
- `set_attrs` exists generically but is unproven for selection writes, so the discovery worker correctly skipped any proof and wrote nothing.

## Probe plus proof (rnk-selprobe, disposable RNK_SEL, deleted afterwards)

- `comp.GetToolList()` returns all tools; `GetToolList(True)` returns only selected; `GetToolList(1)` returns every tool. The truthy-arg shape is host-confirmed; the `1` shape is not selection.
- `tool.SetAttrs({TOOLB_Selected: True})` is a silent no-op (readback stays False, selected set empty).
- `comp.SetActiveTool(M1)` returns True, `ActiveTool` reads back M1, and `GetToolList(True)` reads exactly `[M1]`. This is the proven comp-scoped selection setter. `FlowView.Select` also exists but was not needed.
- Fixture note: host rejects `AddTool(Foreground)`, so the branch node used Background type wired to the Foreground input. Same visual grammar, host-legal types.
- Arrange with host-read selection and `include_unselected=False`: arranged 1 (M1), unselected tools byte-identical, run2 moved 0, `comp.Undo` restored pre exactly.
- Cleanup deleted RNK_SEL plus auto-archive; Timeline 1 restored current with comps `Modified=false`. No save.

## Code consequence

`_read_selection` previously fell back to `getter(1)` when `getter(True)` raised. Host evidence proves `GetToolList(1)` returns the full tool list, so that fallback could silently widen selection-only into whole-comp scope. Removed in `d829754`; only `getter(True)` plus `getter(selected=True)` remain, and total read failure stays fail-closed. Regression tests added (65/65 green).

## Scope note

Single-node selection is degenerate for movement (one member cannot drift), so multi-node selection movement on host is implied by whole-comp movement plus offline multi-select tests, not directly measured. The user manual flow (select several nodes, then Run) exercises it naturally at the dialog gate.

## Remaining for FIRST_USABLE

- Dialog human gate: AskUser presence on comp is confirmed (`AskUser` in the 98-method list); wire shape, Cancel zero-mutation, and menu Run need the user at the machine.
- Comp Scripts install only after the dialog gate.
- Ungroup stays fail-closed until exact restoration is proven on a disposable fixture.
- Orphan `RNK_NEST` plus archive from the stalled sibling run still needs adopt-with-guard cleanup.
