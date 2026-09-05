# Architecture

ResolveNodeKit uses a small host-independent core plus separate host adapters.

```text
commands / future UI
        |
        +------------------+
        |                  |
   Fusion adapter      Color adapter
        |                  |
        +------ core ------+
              layout
              selection (planned)
              command contracts (planned)
```

## Why separate adapters

Fusion exposes a composition/tool/FlowView model. Color exposes a different node-graph model and its scripting surface changes by Resolve version and graph scope. A shared command name may exist, but capability detection and execution remain adapter-owned.

## Tidy Graph contract

Input: tool identities, directed connections, current positions.

Output: deterministic positions only.

Safety sequence:

1. snapshot all tool positions and connections used for planning;
2. compute the layout without host mutation;
3. refuse cyclic/invalid graphs before writing;
4. open an Undo event when available;
5. write positions;
6. read positions back;
7. on any failure, restore the full snapshot and discard the Undo event;
8. keep the Undo event only after successful readback.

Isolated nodes are components, not ignored obstacles. This explicitly avoids a prior-art failure where connected nodes could be placed on top of untouched isolated nodes.
