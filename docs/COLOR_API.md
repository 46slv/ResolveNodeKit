# Color node API boundary

Color support is capability-driven and separate from Fusion FlowView.

## Current measured host status

Read-only capability mapping is HOST-PASS for the current Resolve Studio 21.0.3.7 project context.

Measured context:

- current project/timeline successfully bound through the proven OpenCode/Muse/Resolve MCP route;
- current Timeline 1 items exposed Color Graph objects in the measured context;
- measured per-item Graph contained one node;
- timeline-level Graph was available but contained zero nodes;
- current project contained no Color groups, so group-graph behavior remains context-unexercised rather than disproven;
- probe performed zero host writes.

## Measured Graph surface

Observed callable/readback surfaces include operations for:

- node count;
- node label;
- LUT get/set;
- cache get/set;
- node enabled state;
- tools in node;
- grade-related methods such as DRX application/reset surfaces exposed by the host.

Exact method availability and semantics must still be read from the live object before each mutation feature is implemented.

## XY positioning

Physical Color-node XY position semantics were absent from the measured Graph callable surface. A callable sweep found no position/layout API equivalent to Fusion `FlowView.GetPosTable` / `SetPos`.

Therefore:

- ResolveNodeKit must not claim Color physical node auto-arrange from the current API evidence;
- do not reuse Fusion FlowView assumptions on Color;
- absence of Color XY blocks that specific feature only, not Color inspection or other reversible operations.

## Next Color lane — P9

Only implement mutations with an observable postcondition and readback.

Candidate order, subject to live re-verification:

1. node enable/disable;
2. cache mode helpers;
3. LUT helpers;
4. graph/node inspection/navigation;
5. other operations only when a pre-state/post-state and rollback/exclusion contract is possible.

Each mutation feature must define:

- exact graph scope (timeline/item/group if available);
- target node identity/index rules;
- pre-state snapshot;
- minimal mutation;
- post-state readback;
- rollback path or explicit exclusion reason;
- item/context limitations.

## Context gaps

The current project has no Color groups, so group Graph behavior has not been host-exercised. Do not report group Graph APIs as broken merely because the current data cannot exercise them.

Similarly, generator/Fusion Composition/current-item types may expose different grading behavior. Distinguish:

- unsupported API;
- unavailable current context;
- item type with no meaningful grade graph;
- transport/runtime failure.

## Evidence rule

Color host claims require structured MCP tool-use evidence, exact target identity, and parent verification. Worker narration or a method's return code alone is not sufficient for mutation acceptance.
