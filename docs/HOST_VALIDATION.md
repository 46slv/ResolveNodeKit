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

## Color capability gate

- [ ] current Resolve object acquisition;
- [ ] current timeline/current clip acquisition path;
- [ ] clip/timeline/group NodeGraph acquisition, if exposed;
- [ ] read-only probe enumerates node count, labels, LUT/cache state, and tools where supported;
- [ ] determine which mutations provide readback;
- [ ] do not claim node XY positioning until an actual API or verified alternative exists.
