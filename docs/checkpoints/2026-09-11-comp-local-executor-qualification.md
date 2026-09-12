# WP1 comp-local executor qualification — 2026-09-11

This checkpoint records two materially different, read-only comp-local route
probes after the completed B/C/native context matrix. The known timeline-item,
native `CurrentComp` retention, standalone `LoadComp`, and boolean-only Undo
routes were not replayed.

## Results

1. `script_plugin.run_inline → fusion.Execute(lua)` ran in Resolve Studio
   `21.1.0.14`, but the fresh runtime was `Untitled Project` with no timeline,
   no current composition, and `Fusion.GetCurrentComp()` returned no comp.
   Exact binding, CurrentFrame, FlowView, fixture fingerprint, processing
   serialization, and Undo were therefore not observable.

2. `script_plugin.execute` with a Comp-category Lua script was attempted once.
   The host returned `success=false` without error detail (Lua `print` is
   Console-only). A local composition and its identity were not observable;
   no fixture or candidate mutation ran. The temporary script was removed and
   the Comp script list was independently empty afterward.

Both launcher envelopes acquired an exact-live lease and ended with
authoritative `FREE`. No graph/layout/position/settings/connection/processing/
keyframe/media/selection/Undo/project-save mutation was performed or accepted.
The Operator workspace remained the uncommitted revision
`21ac220fe0877194fbe8c01687642729906cf1c333cdaf80f148cf9d12bfa90a` with its
17-file tree unchanged.

## Qualification

`WP1 = BLOCKED`: no invocation proved the required combination of exact comp
identity, CurrentFrame, FlowView, tool handles, owned Undo, and processing
serialization/readback. Consequently WP2 position/Undo qualification was not
run; WP3 processing sensitivity and WP4 actual displayed-wire qualification
remain `NOT_COLLECTED`. G02/G03 stay `BLOCKED_TECHNICAL`, G08 stays `PENDING`,
and integrated G02/G03/G04, save, main merge, and release were not run.

The machine-readable evidence is
[`2026-09-11-comp-local-executor-qualification.json`](2026-09-11-comp-local-executor-qualification.json).
