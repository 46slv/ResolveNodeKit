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
              semantic layout (planned)
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

The host-verified `Tidy Nested` command uses this hierarchy-preserving model without changing Group expanded/collapsed display state.

`Tidy + Expand Groups` remains a separate strict research path because runtime visual Group expansion is not yet proven on the measured host.

Group frame fit-to-contents is host-specific. `GroupInfo.Size`, `Scale`, and `Offset` are not guessed offline; see `docs/GROUPS.md` and the host-validation gate.

## Semantic Fusion layout — next policy layer

The next layout-quality layer is **semantic layout** rather than increasingly aggressive generic DAG packing.

The design rule is:

> semantic readability before uniform density.

The composition is still solved as local root/Group/nested-Group scopes, but each scope receives semantic roles before coordinates are assigned:

```text
Fusion snapshot
      |
      v
SemanticGraphSnapshot
      |
      +--> ScopeBuilder
      +--> RoleClassifier
      +--> BackboneSelector
      +--> MergeRailDetector
      +--> BranchPlanner
      +--> SpacingSolver
      +--> RecursiveScopeComposer
      |
      v
PlannedLayout
      |
      v
Fusion host adapter
(snapshot / snap / write / readback / rollback)
```

Key behavior:

- choose an output-oriented left-to-right backbone;
- recognize Merge-heavy runs as a composition rail;
- place branch sources above their receiving Merge where practical;
- treat nested Groups as semantic boxes in the parent scope;
- recursively apply the same policy inside every Group;
- allow Merge-to-Merge spacing to widen when branch/Group/wire clearance requires it;
- never require all horizontal gaps to be equal;
- keep generic `Tidy Graph` / `Tidy Nested` as the proven safety baseline until the semantic policy is independently tested and host-verified.

The semantic planner remains pure/core-side. Host-specific grid snapping, tolerance, Undo, readback, and rollback remain adapter-owned.

Normative documents:

- `docs/SEMANTIC_LAYOUT.md` — architecture/policy
- `docs/SEMANTIC_LAYOUT_ACCEPTANCE.md` — hard/soft acceptance contract and fixture matrix
- `docs/decisions/0001-group-local-semantic-layout.md` — design decision rationale
- `docs/references/` — project-neutral visual references

## Architecture boundary: layout vs runtime Group UI

Semantic layout does not solve runtime Group expansion by itself.

These remain separate capabilities:

1. hierarchy-aware position planning;
2. runtime visual Group Expand/Collapse;
3. fit-to-contents of an already expanded Group frame.

This separation prevents a layout policy from pretending an unproven Fusion UI state change succeeded.
