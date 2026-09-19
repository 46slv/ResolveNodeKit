# ResolveNodeKit

Node workflow tools for **DaVinci Resolve Fusion and Color**.

The project is not a Blender Node Wrangler port. It targets Resolve-specific node workflow friction with independent implementations and host-specific adapters.

## Current status

The current product direction is `v1 Arrange / Preserve`. v1 keeps Groups and
protects processing structure; it does not automatically Ungroup or Flatten All.
The official workflow for users who want a flat graph is:

```text
Arrange -> optional Resolve native GUI manual Ungroup -> Re-Arrange
```

The current release lane is tracked in `docs/execution/v1-arrange/`. The old
strict G01–G14 and flatten material is retained under
`docs/execution/strict-orthogonal/` as v2/research evidence and does not block
the v1 release candidate. The project is active and remains separate from the
broader ResolveNodeKit `MISSION_COMPLETE` state.

Host-verified on the current measured Resolve Studio 21.0.3.7 environment:

- Flat Fusion **Tidy Graph**
- hierarchy-preserving **Tidy Nested** for collapsed/nested GroupOperator scopes
- Undo/readback/rollback behavior for the validated layout paths
- Color read-only capability mapping

Current known limitations:

- visual runtime Group expansion is still unproven; the serialized `LoadSettings(Expanded=true)` path is disproven on the measured host;
- large ~1100-tool stress is currently transport-limited by long MCP/bridge calls, not by a demonstrated layout failure;
- physical Color-node XY positioning is absent from the measured Color Graph API surface.

See `docs/PRODUCT_DIRECTION_BRIEF.md`, `docs/CURRENT_STATE.md` and
`docs/execution/v1-arrange/` for the current product contract and evidence.

## Fusion scope

Implemented / under validation:

- deterministic flat **Tidy Graph** layout;
- **Tidy Nested**: recursively arrange nested GroupOperator child scopes without changing visual expanded/collapsed state;
- strict **Tidy + Expand Groups** remains a separate fail-closed research path and must not silently degrade to `Tidy Nested`;
- v1 **Arrange / Preserve** is the installed whole-composition product path and preserves existing Groups;
- automatic Ungroup / Flatten All is v2-only and is not exposed by the normal v1 Arrange UI;
- disconnected/isolated tools included so they are not silently overlapped;
- cycle detection before writes;
- `StartUndo` / `EndUndo` integration where exposed;
- position/settings snapshot, readback verification, rollback on failure;
- no connection, parameter, keyframe, tool creation, grade, media, or render mutation in layout commands.

Development entrypoints include:

- `scripts/Fusion/ResolveNodeKit_Tidy.py`
- `scripts/Fusion/ResolveNodeKit_TidyNested.py`
- `scripts/Fusion/ResolveNodeKit_TidyGroups.py`

## Semantic layout direction

The next layout-quality layer is **Group-local semantic layout**.

Rather than packing the whole composition as one uniform DAG, ResolveNodeKit should make every root/Group/nested-Group scope read as a small local graph:

- main flow left-to-right;
- Merge-heavy chains as a horizontal rail;
- branch sources above receiving Merge nodes where practical;
- child Groups treated as semantic boxes in the parent scope;
- the same policy recursively applied inside Groups;
- **Merge-side spacing may widen** when branch, Group, or wire clearance improves readability.

Uniform density is therefore not a hard goal. Semantic readability wins when the two conflict.

This policy is design-ready but does not replace the current host-verified generic commands yet. The intended rollout is a separate semantic planner/entrypoint first, followed by offline fixtures and host canaries.

See:

- `docs/SEMANTIC_LAYOUT.md`
- `docs/SEMANTIC_LAYOUT_ACCEPTANCE.md`
- `docs/decisions/0001-group-local-semantic-layout.md`
- `docs/references/`

## Group behavior

ResolveNodeKit treats hierarchy-aware layout, runtime visual expansion, and fit-to-contents as separate capabilities.

`Tidy Nested` and v1 Arrange are hierarchy-preserving layout features. They do not
automatically flatten Groups. Runtime visual expansion and fit-to-contents remain
separate broader-program capabilities; their status does not redefine the v1
Arrange release candidate.

See `docs/GROUPS.md`.

## Color scope

Color uses a separate adapter and does not inherit Fusion FlowView assumptions.

Current read-only probing on the measured host found Graph access for current items and readback surfaces including node count, label, LUT, cache, enabled state, and tools where available. Physical Color-node XY positioning was not present in the measured callable surface.

Future Color mutations are limited to operations with observable postconditions/readback.

See `docs/COLOR_API.md`.

## Large graph evidence

For hundreds/thousands of Fusion tools, ResolveNodeKit avoids transporting the entire graph through MCP as one payload. Use the versioned compact signature protocol in `docs/EVIDENCE_PROTOCOL.md`, establish a transport-fitting chunk size, and keep host calls bounded.

## Development

```bash
python -m pip install -e . --no-build-isolation
python -m unittest discover -s tests -v
```

Current offline suite and exact host evidence are tracked in `docs/CURRENT_STATE.md` and `docs/checkpoints/` rather than hard-coded here.

## Long-running agent entrypoint

Long autonomous runs should read:

1. live local Git/worktree + remote state
2. `AGENTS.md`
3. `docs/CURRENT_STATE.md`
4. `docs/ORCHESTRATION.md`
5. `docs/EVIDENCE_PROTOCOL.md`
6. relevant feature contracts/checkpoints

Host-specific claims require structured OpenCode/MCP evidence, exact target identity, pre/post readback, invariant comparison, and parent verification. Worker narration alone is not acceptance evidence.

## Prior art

`SoumyA16-git/Auto-Node-Tree` was reviewed as prior art for graph layout and failure modes. ResolveNodeKit does not vendor or fork that implementation. Blender Node Wrangler is a UX reference only, not a naming, shortcut, UI, or code compatibility target.
