# Host checkpoint - P3A collapsed-group child-position canary - 2026-09-05

Status: `PASS`. Child tools inside collapsed `GroupOperator`s can be read and repositioned without changing membership, connections, processing samples, or group display state. This unblocks implementing the separate `Tidy Nested` command (`tidy_nested_comp`). It does not change the visual-expansion blocker.

Worker route: OpenCode CLI 1.18.29 -> model flag `opencode-go/muse-spark-1.3-contributor` (agent `build`) -> davinci-resolve MCP 2.203.0 -> Resolve Studio 21.0.3.7. Structured events: `%TEMP%\rnk-p3a\events.jsonl` (248 lines). History note: two launcher attempts failed at CLI arg parsing with full-text positional; the working invocation passes a short message plus the work package via `-f <file>` (message before `-f`).

## Target

- Project PSD2Fusion, disposable timeline RNK_P3A (created, verified, deleted afterwards). Timeline list before and after: exactly [Timeline 1]. No project save.
- Timeline 1 restored current, page fusion; all 5 Timeline 1 comps read back `Modified=false` afterwards.
- Repo HEAD `5da1276` untouched by worker (read-only; `git status` clean).

## Measured host facts (structure)

- `comp.AddTool('GroupOperator', x, y)` creates a real GroupOperator (`Group1`, RegID `GroupOperator`); `AddTool('Group', ...)` returns None.
- Assigning `tool.ParentTool = group` does NOT stick (readback None, `GetChildrenList()` empty). Direct parenting is not a host path.
- Settings-assembled nested groups (Lua `Paste`-style construction) DO produce real hierarchy: `GetChildrenList()` + `ParentTool` agree.
- Collapsed groups expose no `Expanded` key (`Expanded=nil`); `Size`/`Scale`/`Offset`/`Pos` readable per group.

## Canary (disposable 2-level case)

- Outer `P3A_Outer` (root) owns `P3A_Inner` + `P3A_Sib`; inner owns `P3A_A` + `P3A_B`. Both groups collapsed.
- Snapshot positions: A/B at (-0.499,-0.224). Wrote grid-snapped (+1.0 x) targets; readback exactly (0.5,0.009) for both.
- Post-write: parents unchanged (A/B still under `P3A_Inner`), outer/inner positions unchanged, children lists intact (`outer: Inner,Sib`; `inner: A,B`), both groups still `Expanded=nil` with byte-identical `Size`/`Scale`/`Offset` strings.
- One Undo: stack depth 10 -> 10, every position restored to snapshot values exactly.
- Post-Undo: membership intact; sampled keyframes/params present (2 keyframes each on A/B/Sib); geometry unchanged.
- Caveat: canary nodes were unconnected, so connection invariance is trivially true here (zero edges). Connected-nested proof deferred to P5 duplicate stress.

## Decision

P3A canary PASS. Proceed to implement `tidy_nested_comp(...)` + `scripts/Fusion/ResolveNodeKit_TidyNested.py` reusing the per-scope snapshot/layout/write/readback/rollback machinery, with no expand/restore step and no visual-expansion claim.

## Next ordered gates

1. Implement + offline-test `Tidy Nested` (repo only).
2. P5 nested stress on a duplicate of the large composition with compact in-host hashes.
3. P6 low-risk Fusion ops and P8 Color read-only map (independent).
4. P3B runtime-expansion research remains the mission-critical blocker track.
