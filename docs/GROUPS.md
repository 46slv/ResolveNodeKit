# Fusion GroupOperator tidy contract

ResolveNodeKit must support deeply nested Fusion `GroupOperator` trees without ungrouping them.

## Required behavior

`Tidy + Expand Groups` treats every GroupOperator as both a node in its parent scope and a container with its own child scope.

- preserve GroupOperator membership;
- recursively discover children with `GetChildrenList()` and parent ownership via `ParentTool` / `TOOLH_GroupParent`;
- expand every GroupOperator by setting `ViewInfo.Flags.Expanded = true` through `SaveSettings` / `LoadSettings`;
- run deterministic layout independently at root and inside every nested group;
- project cross-boundary connections to the visible group node for layout planning only;
- never rewire a connection to achieve layout;
- verify hierarchy, connection signatures, positions, and Expanded readback;
- wrap the operation in one Undo event when available;
- rollback positions and group settings if any expansion or position write fails.

This is intentionally separate from `tidy_comp()` until the real Resolve/Fusion host behavior is verified.

## Why per-scope layout is necessary

Flattening a nested graph loses the visual meaning of a GroupOperator. For an edge from a node inside `GroupB` to a sibling node inside `GroupA`, the `GroupA` layout sees `GroupB -> sibling`, while the `GroupB` layout sees the real internal edge. The connection itself is not changed.

## Host-only gate: fit to contents

Offline mocks can prove recursive discovery, scope projection, deterministic positions, expansion-state handling, and rollback. They cannot prove the Fusion UI's `GroupInfo.Size`, `Scale`, and `Offset` behavior.

The user-visible requirement is stricter than merely setting `Expanded = true`: after host validation, every expanded group must show all direct children without clipping. Do not invent a `GroupInfo.Size` formula from setting-file examples. Measure the installed Resolve/Fusion behavior first, then either:

1. confirm Fusion automatically sizes/frames the expanded group after the child positions are written; or
2. add a measured, readback-verifiable `Size` / `Scale` / `Offset` fit step.

Until that host gate passes, report the feature as recursive expand + tidy, not fully host-verified fit-to-contents.

## Evidence basis

Fusion's scripting reference documents `TOOLH_GroupParent`, the `Operator.ParentTool` convenience property, `Operator.GetChildrenList()`, and `Operator.SaveSettings()` / `LoadSettings()`. Real GroupOperator settings serialize nested tools under `Tools = ordered() { ... }` and expanded UI state under `ViewInfo = GroupInfo { Flags = { Expanded = true, ... } }`.
