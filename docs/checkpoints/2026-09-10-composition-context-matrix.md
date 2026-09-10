# Composition execution context matrix — 2026-09-10

This was one fresh context/route qualification after the earlier Lane A/B
results. The standalone LoadComp and boolean-only Undo probes were not replayed.
Both invocations were owned by the external Resolve Operator and ended with an
authoritative `FREE` lease.

## Compatibility route

The Operator created an owned disposable project/timeline/Fusion item. In the
timeline-item-bound context (B), `CurrentFrame` was readable but FlowView was
not. In the materially different Fusion-page active context (C), a scoped
sample position `[3.5, 1.009]` was readable. The public MCP exposed advertised
SetPos/StartUndo/EndUndo wrappers, but no callable Undo operation and no raw
StartUndo return/type. The opaque comp identity and direct GUI-active-comp ID
were not exported, so C is not an owned rollback candidate.

The Operator deleted the scratch project and independently verified that it was
absent. No graph/layout/settings/Undo/project-save mutation occurred. The
pre/post opaque identity for the empty `Untitled Project` differed; because no
valuable project was loaded or saved, no speculative restore was attempted.

## Native route

The native bridge was tested once on an Operator-owned scratch composition. The
new composition did not retain/rebind as `CurrentComp`; `CurrentFrame`,
FlowView, and position methods were unavailable. Undo method names were present
but ownership and target binding were not proven, so the first write was
forbidden. The scratch comp was closed and its absence was independently read
back. No project save occurred.

## Acceptance

No context proved both a retained FlowView-bearing target and an owned Undo
boundary. WP2 therefore ran zero moves and zero Undo calls. WP3's full
processing-preservation fingerprint and sensitivity matrix, and WP4's actual
displayed-wire evidence, remain `NOT_COLLECTED`. G02/G03 remain
`BLOCKED_TECHNICAL`; G08 remains pending. Partial FlowView or wrapper success
was not promoted to any RNK PASS.

Structured evidence: [`2026-09-10-composition-context-matrix.json`](2026-09-10-composition-context-matrix.json)
