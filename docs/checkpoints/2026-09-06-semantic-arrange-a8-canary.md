# Host checkpoint - Semantic Arrange A8 preserve-mode canary - 2026-09-06

Status: `CHECKPOINTED` with flat-fixture `HOST-PASS`. Nested-Group preserve proof remains open behind a Paste transport gate.

Worker route (all runs): OpenCode CLI 1.18.29 -> model `opencode-go/muse-spark-1.3-contributor` (agent `build`) -> davinci-resolve MCP 2.203.0 -> Resolve Studio 21.0.3.7, project PSD2Fusion. Structured events: `%TEMP%\\rnk-arrange0` (preflight), `%TEMP%\\rnk-arrange1` (canary 1), `%TEMP%\\rnk-arrange2` (canary 2), `%TEMP%\\rnk-arrange3` (canary 3, nested attempt), `%TEMP%\\rnk-arrange4` (cleanup verification).

Repo under test: `c75a02a` (canary 1), then `f988fa0` (canaries 2-4) on branch `feat/semantic-arrange-v1-20260906`, Draft PR #5 stacked on `feat/bootstrap-nodekit-20260905`.

## Preflight (rnk-arrange0): PASS, transport proven

Nine completed MCP tool uses, read-only. Live state fresh-read: Studio 21.0.3.7, project PSD2Fusion, timelines exactly `[Timeline 1]`, current Timeline 1, item-0 comp 958 tools (note: earlier reference said 1107; the live project changed, so never assume historical counts).

Invocation trap confirmed: this MCP server wants string-form actions such as `{"action":"get_current","params":{}}`. Object-form action values are rejected with a `Valid actions` error. Parent packets prescribing object form were wrong twice; both workers adapted correctly. Future packets must prescribe string form.

## Canary 1 (rnk-arrange1): real bug found, then contained

Disposable `RNK_ARRANGE0`, flat 6-tool Merge fixture (BG, A, M1, B, M2, Out), 5 edges, pre clustered offscreen.

- Run1 `arrange_comp(include_unselected=True)`: nodes=6 edges=5 moved=6, `avoidable_diagonal_edge_count=0`, tool set plus 5/5 edges identical. Post readback orthogonal: backbone row shared, branches above sharing receiver columns, host offsets `+0.001 X / +0.009 Y` exactly as modeled.
- Run2: moved=6, drifted down about 3 Y units. Root cause: min-of-members origin anchoring follows branches placed above the backbone. Worker stopped per constraints before Undo and ungroup steps. Cleanup deleted the disposable plus auto-archive; `[Timeline 1]` intact; no save.

## Anchor fix (repo, offline-proven then host-proven)

`arrange_comp` now anchors to the backbone head (or first member when the head is out of scope) and snaps the origin itself to the host grid, so reruns reproduce the origin exactly. Added `ArrangeAnchorTests` (branches-above fixture modeled on the host pre state): verified to FAIL on the old anchoring and PASS on the new one. Offline suite 63/63 plus `compileall`. Committed as `f988fa0`, pushed.

## Canary 2 (rnk-arrange2): flat preserve-mode HOST-PASS

Fresh disposable `RNK_ARRANGE1`, same flat fixture shape, pre fully clustered at `(0, 0.009)`.

- Run1: moved=5 (BG held as canonical anchor), avoidable diagonals 0, tools, membership, edges identical.
- Run2: moved=0, positions identical to run1. Anchor fix holds on host, no drift.
- `comp.Undo()` restored all six positions exactly to pre.
- `ungroup=True` refused fail-closed with zero writes (positions byte-identical).
- Cleanup deleted `RNK_ARRANGE1` plus auto-archive; final `[Timeline 1]`, current Timeline 1, all comps `COMPB_Modified=false`. No save.
- Parent independently verified run1 `moved_count=5`, run2 `moved=0` with branch positions, and the tested code path in the raw event stream.

## Canary 3 (rnk-arrange3): nested lane BLOCKED_HOST (Paste transport)

Single bounded Paste attempt (Lua `run_inline`, 60 s) of an 8-tool nested payload (`OuterG` containing `BGin -> BLin` plus nested `InnerG` containing `MGin`, plus root `BG, M1, Out` with cross-boundary wiring) into fresh disposable `RNK_ARRANGE2`:

- Result: MCP `-32001 Request timed out` on in-host `comp:Paste`; follow-up call returned `Not connected`. The bridge deregistered `davinci-resolve_*` tools for that worker session only.
- Worker stopped per constraints: no identical retry, no alternate grouping hack, no blind writes. Timeline 1 received zero writes. State of `RNK_ARRANGE2` left unknown rather than guessed.

This matches the known large-call transport envelope failure, now measured for Paste as well: one long in-host call -> `-32001` -> `-32000` / deregistration, while Resolve itself stays alive. Fresh `opencode mcp list` from a new process still showed `davinci-resolve connected`, so the loss is session-scoped and a fresh run recovers.

## Cleanup verification (rnk-arrange4): PASS

Fresh worker found `[Timeline 1, RNK_ARRANGE2, RNK_ARRANGE2_archived_v01]` with Timeline 1 intact (6 items, all `Modified=false`), deleted only the two exact-ID disposable artifacts with confirm-token guardrails, and re-verified final `[Timeline 1]`, current Timeline 1, all six comps `Modified=false`. No save.

## Remaining gates for FIRST_USABLE (in dependency order)

1. Nested-Group preserve proof: retry with a non-identical smaller Paste envelope (split root versus group Paste, or reduced defaults), keeping every call short. Never repeat the single 8-tool Paste.
2. Selection-only host proof: discover a safe selection API on a disposable comp; if none exists without UI clicks, defer to user acceptance.
3. Dialog proof: AskUser wire shape plus Cancel zero-mutation plus Run from the real menu path need the user at the machine (a worker cannot click Resolve dialogs, and must never drive the dialog path headless without new authority).
4. Install `ResolveNodeKit_Arrange.py` into the user Comp Scripts directory only after gate 3 is proven, then verify menu visibility with the user.
5. Whole-comp at Timeline-1 scale stays out of scope until a transport-fitting chunked envelope exists (see P5 strategy).

## Reusable learnings (see Learning Gate in run closeout)

- MCP envelope for this server generation: string action plus params object; object-form action is rejected.
- One long in-host call (full-graph walk, 8-tool nested Paste) collapses the session bridge; recovery is a fresh run, never an identical retry.
- `run_inline` sees `CurrentFrame` as None off the Fusion page; switch pages first, then rebind.
- Min-of-members grid anchoring drifts whenever branches sit above the backbone; canonical backbone-head anchor plus snapped origin is fixed-point stable (mechanized in code plus regression tests).
- Ungroup mode remains fail-closed by design with host-measured zero-write refusal.
