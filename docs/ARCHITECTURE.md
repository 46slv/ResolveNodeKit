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

## Hierarchical Fusion layout

Nested `GroupOperator` graphs are not flattened. Each group is a visual scope:

```text
root
├─ ordinary tool
└─ Group A
   ├─ ordinary tool
   └─ Group B
      └─ ordinary tools
```

The layout engine runs once for root and once for every GroupOperator's direct children. A connection crossing a nested boundary is projected to the GroupOperator visible at the current scope for layout planning, while the real Fusion connection remains untouched.

`Tidy + Expand Groups` additionally snapshots each GroupOperator settings table, sets `ViewInfo.Flags.Expanded = true`, verifies the hierarchy and connection signature again, writes positions, and restores positions/settings if any step fails.

Group frame fit-to-contents is host-specific. `GroupInfo.Size`, `Scale`, and `Offset` are not guessed offline; see `docs/GROUPS.md` and the host-validation gate.
