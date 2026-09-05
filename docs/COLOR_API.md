# Color node API boundary

Color support is intentionally capability-driven rather than modeled after Fusion FlowView.

## Confirmed from published scripting material / prior current implementations

Blackmagic's Resolve 19 New Features Guide documented scripting support for querying timeline and group node graphs and enumerating tools in a node. Current Resolve 21 also has a Color Node Editor layer-list UI, but UI capability is not treated as scripting capability.

Published Resolve scripting README mirrors expose a `Graph` object with read surfaces including:

- `GetNumNodes()`
- `GetNodeLabel(nodeIndex)`
- `GetToolsInNode(nodeIndex)`
- `GetLUT(nodeIndex)`
- `GetNodeCacheMode(nodeIndex)`

`TimelineItem.GetNodeGraph()` and timeline graph access are also documented in current API mirrors. Node indices are treated as 1-based by the probe code.

## Still host-gated

- exact installed Resolve version and object acquisition path;
- whether `GetCurrentVideoItem()` exists in the user's current host context;
- clip/timeline/group graph differences;
- write operations and their readback guarantees;
- any Color-node XY position API or safe alternative.

Until those are measured, Color implementation remains read-only. `scripts/Color/ResolveNodeKit_Probe.py` inventories timeline/current-item graph data without mutating grades.
