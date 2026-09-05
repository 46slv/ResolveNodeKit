# Host validation checklist

Offline tests are necessary but insufficient. Before calling a host feature ready, record the exact Resolve/Fusion version and test on a disposable or duplicated graph.

## Fusion Tidy Graph

- [ ] script loads from the intended Resolve script context;
- [ ] `GetToolList`, `CurrentFrame.FlowView`, `GetPosTable`, and `SetPos` match current host behavior;
- [ ] simple serial graph;
- [ ] BG + FG -> Merge;
- [ ] mask branch;
- [ ] multiple disconnected components;
- [ ] isolated nodes;
- [ ] large PSD2Fusion-style graph;
- [ ] second run is position-identical;
- [ ] one Undo returns the original layout;
- [ ] injected/real write failure restores all original positions;
- [ ] connections and relevant tool parameters are unchanged;
- [ ] save/reopen retains the arranged positions.

## Fusion Tidy + Expand Groups

- [ ] `GroupOperator.GetChildrenList()` returns the expected direct children;
- [ ] `ParentTool` / `TOOLH_GroupParent` identifies the same direct hierarchy;
- [ ] 1-level group expands and its children are arranged;
- [ ] 2–3 nested group levels expand recursively;
- [ ] all GroupOperators read back `ViewInfo.Flags.Expanded = true` after the command;
- [ ] GroupOperator membership is unchanged before/after;
- [ ] connection signature is unchanged before/after;
- [ ] root, parent-group, and nested-group scopes each have stable non-overlapping layouts;
- [ ] second run is position-identical and performs no unnecessary expansion;
- [ ] one Undo restores both positions and prior expanded/collapsed states;
- [ ] expansion or position-write failure restores original positions and group settings;
- [ ] save/reopen preserves group membership, layout, and intended expanded state;
- [ ] every expanded group visually shows all direct children without clipping.

If the last check fails, capture the actual `GroupInfo.Size`, `Scale`, `Offset`, child bounds, and host behavior first. Add a fit-to-contents calculation only from measured host evidence; do not infer a formula from `.setting` examples.

## Color capability gate

- [ ] current Resolve object acquisition;
- [ ] current timeline/current clip acquisition path;
- [ ] clip/timeline/group NodeGraph acquisition, if exposed;
- [ ] read-only probe enumerates node count, labels, LUT/cache state, and tools where supported;
- [ ] determine which mutations provide readback;
- [ ] do not claim node XY positioning until an actual API or verified alternative exists.
