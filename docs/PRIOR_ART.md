# Prior art notes

## Auto-Node-Tree

Reviewed source: `SoumyA16-git/Auto-Node-Tree`, commit `fb751986b6a75059e3b6ac0de7b154c34382cd37` (2026-08-31).

Useful ideas:

- topological layering for Fusion graphs;
- barycenter-style ordering to reduce crossings;
- FlowView position-only writes;
- offline fixtures for graph-layout behavior.

Observed risks that ResolveNodeKit treats as regression requirements rather than inherited behavior:

- merge inputs can be re-collapsed after collision prevention;
- repeated runs can drift when anchoring depends on moved sink coordinates;
- untouched isolated nodes can be overlapped;
- partial SetPos failure can leave partial layout without explicit rollback/readback;
- malformed cycles need a bounded fail-closed path.

ResolveNodeKit is an independent implementation. No upstream source is vendored here.

## Fusion GroupOperator

Fusion scripting/reference material exposes `TOOLH_GroupParent`, `Operator.ParentTool`, `Operator.GetChildrenList()`, and `SaveSettings()` / `LoadSettings()`. Real GroupOperator setting examples serialize children under nested `Tools` and expanded UI state as `ViewInfo = GroupInfo { Flags = { Expanded = true } }`.

ResolveNodeKit uses those facts only for hierarchy discovery and expansion-state handling. It does not copy another layout implementation. `GroupInfo.Size`, `Scale`, and `Offset` remain host-measurement inputs rather than guessed constants; see `docs/GROUPS.md`.

## Blender Node Wrangler

Node Wrangler is a UX reference for the value of fast node operations, not a naming, shortcut, UI, or code compatibility target. ResolveNodeKit should favor operations that fit Resolve's own Fusion and Color models.
