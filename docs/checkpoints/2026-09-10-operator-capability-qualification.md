# Operator capability qualification — 2026-09-10

This continuation fresh-read the live RNK checkout, installed manifest, local
Operator implementation, and Resolve Operator skill before any host probe.
The canonical RNK HEAD and installed manifest both resolve to
`e616966d935c93980ecf0c4b3cd05689926ab56f` on
`feat/semantic-arrange-v1-20260906`.  The parent effective model was Luna Max
(`gpt-5.6-luna/max`); the external Operator profile was Terra High.

## Lane A

Launch `85d54d87-2aed-48a6-905f-ce77ce5acef6` used the materially different
Operator-owned registry fixture route for `nested_group_v1`.  The standalone
composition loaded once and closed once, with 10 tools, 2 groups, and 7
processing edges.  All seven processing connections were observed, including
`InnerMask -> InnerProcess` and both Group-boundary crossings.

The capability result was `BLOCKED`: `ports=complete`; all other required
processing fields were `unsupported` except `tool_state=error`; FlowView node
positions, viewport/zoom, capture provenance, and displayed wire geometry were
unsupported.  Mask and Group-boundary edges were therefore not displayed-wire
qualified.  No graph/layout/settings/Undo/project-save mutation occurred,
protected state stayed unchanged, cleanup was exact, and the launcher ended
with lease `FREE`.  Position or processing-port evidence was not promoted to
G03.

## Lane B

Compatibility launch `30712be3-3eac-47a1-b7d1-2d7a21d6b6f2` could observe runtime
state but exposed no retained target or owned Undo boundary.  The first write
was forbidden; position/graph/layout/settings/Undo/project-save stayed zero.
Native comparison `c290d6a7-a755-4c54-aea6-c21d0a297fcd` inspected a 10-node,
2-group graph but likewise could not retain a position target or prove owned
Undo.  It also performed zero writes.  Both final leases were `FREE`.

The required PASS sequence remains strict: prove ownership, one position move,
independent post readback, exactly one owned Undo, and exact restoration with
processing/graph invariance.  No direct rollback or `StartUndo=false` inference
was used.

## Reusable Operator seam

The Operator workspace now contains transport-neutral contracts for processing
coverage, FlowView readback, displayed-wire edge coverage, and the dedicated
owned-Undo transaction.  They preserve the four explicit capability states,
require mask/Group-boundary edge coverage, reject position-only promotion, and
keep opaque host bindings private.  Focused tests are `15/15 PASS`; compileall
and `git diff --check` pass.  The workspace has no commits; its deterministic
non-cache source/test tree revision is
  `21ac220fe0877194fbe8c01687642729906cf1c333cdaf80f148cf9d12bfa90a`.

RNK G02/G03 remain `BLOCKED_TECHNICAL` and G08 remains pending.  The integrated
HostSession, G04, project save, main merge, and release were not run.

## Mandatory Learning Gate

Source-supported result: the external Operator acquired/released the exact-live
lease and returned structured zero-write evidence for materially different
compatibility/native probes; the registry fixture processing inventory is
observable.  RNK-specific result: this Resolve host still lacks complete
processing, FlowView/displayed-wire, and retained-target/owned-Undo evidence.

Verified reusable delta: keep the short semantic envelope, exact installed
candidate precondition, four-state capability contracts, mask/Group-boundary
edge gate, ownership-before-write gate, and no-identical-third-retry guard.
Do not promote this single RNK host result to global routing policy.  Complete
processing serialization, displayed wire capture, owned Undo, integrated G02/G03
and G04, and large-scale host qualification remain `NOT_COLLECTED`.

Structured evidence: [`2026-09-10-operator-capability-qualification.json`](2026-09-10-operator-capability-qualification.json)
