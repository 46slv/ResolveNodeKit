# WP1 final comp-local executor qualification — 2026-09-11

The bounded WP1 investigation is now closed fail-closed. The completed B/C/
native matrix was not replayed. Three new hypotheses were each tried once:

- `run_inline → fusion.Execute(lua)`: no active timeline or composition;
  `Fusion.GetCurrentComp()` returned none.
- Comp-category Lua execution: the host returned `success=false` and exposed
  no local composition or error detail; the temporary script was removed.
- Constructor-local Lua: one `fusion.NewComp()`-only probe returned an opaque
  `table: ...` with empty stdout. No local comp result, identity, FlowView,
  GetPosTable, fixture fingerprint, processing serialization, Undo ownership,
  or Close absence was serialized, so every such field is `UNKNOWN`.

All three launcher envelopes acquired exact-live ownership and ended with
authoritative `FREE`. No graph/layout/position/settings/connection/processing/
keyframe/media/selection/Undo/project-save mutation ran. The final observed
host was Resolve Studio `21.1.0.14`, GUI instance 1, `Untitled Project`, no
timeline, page `null`; no valuable project was loaded or saved. The Operator
workspace remains revision
`21ac220fe0877194fbe8c01687642729906cf1c333cdaf80f148cf9d12bfa90a` and is
not modified.

`WP1 = BLOCKED`. The exact comp identity + FlowView + owned Undo prerequisite
was not proven, so WP2/WP3/WP4 and integrated G02/G03/G04 remain unrun. G02 /
G03 stay `BLOCKED_TECHNICAL`, G08 stays `PENDING`. No further identical context
probe is allowed without genuinely new host evidence.

Machine-readable evidence: [`2026-09-11-comp-local-executor-final.json`](2026-09-11-comp-local-executor-final.json).
