# Host checkpoint - Tidy Nested fixed-command re-validation (R1) - 2026-09-06

Status: `PASS`. `tidy_nested_comp` with fixed-point iteration is HOST-PASS on the canonical branch.

Worker route: OpenCode CLI 1.18.29 -> model flag `opencode-go/muse-spark-1.3-contributor` (agent `build`) -> davinci-resolve MCP 2.203.0 -> Resolve Studio 21.0.3.7 (fresh user-restarted session). Structured events: `%TEMP%\rnk-recover2\events.jsonl` (161 lines). Repo HEAD under test: `f0b09b0` (code identical to `f1c2982`).

## Recovery (mandatory sequence, all verified)

- Fresh bind: new Resolve session, project PSD2Fusion, no historical identity assumed.
- Timeline 1 verified intact (5 items, all comps `Modified=false`, ~1107-tool / 31-group comp).
- Stale disposables from dead attempt proven disposable and deleted: RNK_R1, RNK_R1_archived_v01.
- Final list exactly [Timeline 1], current Timeline 1, page fusion. No project save. Repo untouched.

## Validation (fresh disposable RNK_R2, deleted afterwards)

- Fixture: 2-level nested Paste (OuterG > InnerG + BGout/BLOut chain siblings; BGin>BLin>MGin chain inside InnerG), all children at identical (-0.499,-0.224), both groups collapsed. Small paste landed cleanly (no hang).
- Run1: `nodes=8 edges=3 moved=7 groups=2 expanded=0 scopes=3`; InnerG directly to (-0.499, 4.009) — the fixed point in ONE run (round 1 needed run2 for this).
- Membership exact (OuterG kids BGout/BLOut/InnerG; InnerG kids BGin/BLin/MGin); edges 3/3 preserved; sampled param (BLin BlurSize) intact; both groups collapsed with unchanged Size/Scale/Offset.
- Undo: all 8 positions restored to snapshot exactly.
- Rerun from snapshot: moved=7 again (deterministic); second run moved=0, identical=True.
- Cleanup: RNK_R2 + auto-archive deleted; Timeline 1 current with all comps `Modified=false`.

## Decision

R1 PASS. The fixed-point fix is proven on host: run1 settles directly, run2 moves nothing. `Tidy Nested` joins Flat Tidy as HOST-PASS. Next: P5 large-stress, P6, P8, P3B per the ready queue.
