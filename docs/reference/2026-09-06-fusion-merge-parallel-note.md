# Fusion merge-parallel layout reference (2026-09-06)

Source: live read of the currently open Fusion page (project PSD2Fusion /
Timeline 1 / item "Fusion Composition" / comp index 1). Raw data:
`2026-09-06-fusion-timeline1-layout.json` (schema
`resolve-node-kit.layout-ref/v1`).

Read method: external scripting with Get-only calls (GetToolList,
FlowView.GetPosTable, GetAttrs, GetInputList, GetConnectedOutput,
GetChildrenList). No Set/save/timeline operation was issued; host verified
unchanged afterwards (timelines still exactly [Timeline 1], page fusion).

## Envelope

- tools 1109, GroupOperator 29, Merge 257
- position_hash (parent/name/snapped x/y, SHA-256): `c8f92a55cacc921d...`
  (full value inside the JSON)
- type mix: Merge 257, ChannelBoolean 240, AlphaMultiply 161, AlphaDivide 120,
  Loader 100, ChangeDepth 100, BrightnessContrast 62, Background 36,
  GroupOperator 29, MediaOut 1, Glow 1, CineFocus/LensBlur OFX 1 each
- tool names contain no absolute paths (safe to keep in repo)

## Pattern 1: root backbone cascade (horizontal)

One merge row at snapped y=-16, x from -4.0 to 31.5, pitch 2.0-2.5.
Each merge is named `MergeRII_<grouphash>` after the group whose output it
collects, e.g. `MergeRII_3244bad4da` at x=9.0, `Merge1` at 16.5, `Merge2` at
22.0. A second shorter row sits at y=-49 (x 13-26.5).

## Pattern 2: parallel reduction columns (vertical)

- x=29 column: 6 merges, y -21 to -38. x=31.5 column: 3 merges, y -16 to -25.
- Convention per column merge: Background input = merge directly above in the
  same column (serial vertical chain), Foreground input = side branch from a
  group output (`MergeRIII_*`) or effect (e.g. AICineFocus1).
- Example: `MergeRII_2cdcd869ea` (29.0, -33.99): BG=`MergeRII_1829a7e279`,
  FG=`MergeRIII_c58b72621f`.

## Pattern 3: layer-group serial chains

Each Group_* holds one PSD-layer stack: Loader -> ChangeDepth -> Alpha
ops -> ChannelBoolean -> Merge chain, laid left-to-right with x pitch 3.0,
one y lane per stack (group y lanes range 6-74). Group sizes 5-90 tools.

## Pattern 4: nesting

Max depth 2. Six small groups (5-23 tools: Group_140aae8caf,
Group_162461e9f9, Group_2cdcd869ea, Group_a1bb2f4d0a, Group_b6521522fc,
Group_d39e1b3dd7) are nested inside other groups; the rest sit at root.
Root scope itself holds 103 tools.

## Grid observation

Snapped positions sit on x:0.5 / y:1.0 grid; raw readback carries the known
small per-type offsets (e.g. y=-26.99). Consistent with FLOW_GRID_X/Y in
`src/resolve_node_kit/fusion/tidy.py`.

## Use for NodeKit

- Real-world pitch defaults: serial pitch 2.0-3.0, reduction-column pitch 2-4.
- Column detector test case: same-snapped-x merge clusters at root x=29/31.5
  with BG-vertical/FG-horizontal wiring (see `merge_x_clusters`, `merge_rows`
  inputs in the JSON).
- Ungrouping roadmap input: flat root + depth-2 nesting only; group output
  merges are identifiable by `MergeRII_<grouphash>` naming at root.
- The JSON doubles as a 1109-node layout-algorithm fixture (positions only;
  full edge list was intentionally not pulled to keep host calls light).
