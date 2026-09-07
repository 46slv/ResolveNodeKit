# Semantic Arrange whole-comp host smoke — 2026-09-07

## Result

The updated installed package and direct production seam passed a disposable
whole-composition smoke with `include_unselected=True, ungroup=False`.

## B1 whole composition

The fixture contained six tools, three deterministic connections, and no
selected tools.  The handler arranged all six (`arranged=6`, `moved=5`),
preserved connections/tool identities, restored the first handler-owned Undo
snapshot exactly, and reported `moved=0` on the second identical run.

## B2 Group preserve

The fixture contained seven tools, one explicit GroupOperator, and three
connections.  The handler arranged all seven (`arranged=7`, `moved=6`), kept
the GroupOperator and parent map unchanged, preserved connections/tool
identities, restored the exact first Undo snapshot, and reported `moved=0` on
the second run.  Resolve 21.0.3.7 does not expose `GroupOperator.AddTool` on
this measured route, so the GroupOperator was empty; child-membership
recursion remains a separate host capability limitation.

## Host/UI boundary

The updated installed tree imported successfully and reported the new default
state plus `ask_arrange_confirmation`.  The direct handler still logs
`busy unavailable: no UIDispatcher`; busy/result UI ordering was therefore not
claimed.  No UIA/MSAA, menu Invoke, LoadComp/Paste, or project save was used.

The first generated direct verifier call passed a wrapped `comp` as the UI
owner and correctly failed closed on identity mismatch without writes.  The
verifier now passes `ui_comp=None` and binds the live Fusion current comp while
retaining the wrapper for readback; this is the route used for the PASS smoke.

## Final host state

Both disposable projects were deleted by exact name.  Resolve was restored to
`PSD2Fusion` / `Timeline 1` / Fusion with one timeline, 967 valuable tools,
`COMPB_Modified=false`, no RNK-owned disposable projects, and no save.

Machine-readable evidence is in
`2026-09-07-semantic-arrange-whole-comp-host-smoke.json`.
