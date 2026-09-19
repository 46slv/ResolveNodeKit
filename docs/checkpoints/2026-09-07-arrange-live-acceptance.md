# Arrange live host acceptance — 2026-09-07

## Result

The production seam is host-accepted for direct behavior on the restarted
Resolve 21.0.3.7 host.  The GUI accessibility lane remains a separate hard
limitation.

## Restart and recovery

The old Resolve PID `23240` and its exact child `fuscript.exe` PID `8636` did
not close through `CloseMainWindow()` and remained after a 10-second bounded
wait.  The exact Resolve path was then force-terminated once; no unrelated
process was touched.  Resolve returned as PID `29244` with child fuscript PID
`92096`, both responsive.  No project save and no PC reboot occurred.

The first post-restart scripting endpoint responded immediately.  Its initial
inline source used the wrong `resolve.GetFusion()` spelling and returned a
script-side error; the measured host API is `resolve.Fusion()`.  Read-only
project/timeline/comp actions then returned normally.

## Cleanup and fixture lanes

Exact owned projects `_mcp_RNK_SEAM_20260907` and
`_mcp_RNK_SEAM_ACCEPT_20260907` were deleted and confirmed absent.  No
`LoadComp/Paste` route was used.

B1 used six tools on a fresh timeline: four selected, two unselected, three
deterministic connections.  The existing generated verifier called the same
`execute_arrange_request` handler with OFF/OFF state.  Because the host comp
has an empty `COMPS_Name`, the direct verifier passed `ui_comp=None`; the
handler itself bound the exact live current comp and still required
`require_live=True`.

B1 passed: selected nodes moved (`moved=4`), unselected nodes stayed exact,
connections/tool identities stayed exact, Undo reached the exact pre-snapshot,
and the second run reported `moved=0`.

B2 used a fresh GroupOperator scope.  The GroupOperator remained, group scope
and connections were unchanged, the first run succeeded (`moved=5`), and the
second run reported `moved=0`.  `GroupOperator.AddTool` is not exposed on this
host in either Python or Lua, so the group was empty; the membership proof is
therefore exact but vacuous.

## Busy/result limitation

The handler log records `busy unavailable: no UIDispatcher`, so no live busy
stage text was accepted.  A result window with title `ResolveNodeKit - Arrange`
and text `Result|` was observed from the UI-enabled attempt and closed through
identity `WindowPattern.Close`; it is not claimed as same-run ordering proof
for the successful no-result-dialog diagnostic.  This is a host UI capability
limitation, not a failure of the direct product behavior gate.

## Final state

Resolve was restored to `PSD2Fusion` / `Timeline 1` / Fusion.  Timeline list is
exactly `[Timeline 1]`; the valuable comp has 967 tools and
`COMPB_Modified=false`; no RNK-owned disposable projects remain; no project
save occurred.

Machine-readable evidence:
`2026-09-07-arrange-live-acceptance.json`.
