# ResolveNodeKit

Node workflow tools for **DaVinci Resolve Fusion and Color**.

The project is not a Blender Node Wrangler port. It targets Resolve-specific node workflow friction with independent implementations and host-specific adapters.

## Current scope

### Fusion — implementation started

- deterministic **Tidy Graph** layout;
- **Tidy + Expand Groups** for nested `GroupOperator` trees without ungrouping them;
- each group hierarchy is laid out independently, with cross-boundary edges projected to the visible group node for layout planning only;
- disconnected and isolated tools included so they cannot be silently overlapped;
- cycle detection: fail closed before any position write;
- `StartUndo` / `EndUndo` when the host exposes them;
- original-position/settings snapshot, readback verification, and rollback on failed writes;
- no connection, parameter, keyframe, tool creation, or render mutation in layout commands.

`Tidy + Expand Groups` currently verifies recursive membership, connections, positions, and `Expanded` state offline. Exact Fusion UI fit-to-contents behavior (`GroupInfo.Size` / `Scale` / `Offset`) remains a real-host gate; the implementation does not guess those values.

### Color — capability work started

Fusion and Color do **not** share one assumed API. Color support starts with a read-only capability probe and Graph snapshot layer (`GetNumNodes`, labels/LUT/cache/tool enumeration when exposed). Node graph mutations are added only after current Resolve host verification.

## Roadmap

1. **F1 — Fusion Tidy Graph**: host-verify on small, branched, mask, disconnected, nested-group, and large graphs.
2. **F1G — Group visibility**: prove nested GroupOperator expansion and fit-to-contents on the installed Fusion host; add measured group-frame sizing only if needed.
3. **F2 — Fusion node operations**: align/distribute, insert-between, connect/reconnect, swap inputs, detach/bypass, upstream/downstream selection.
4. **C1 — Color API boundary**: verify current clip/timeline/group NodeGraph acquisition and available operations on the installed Resolve version.
5. **C2 — Color node operations**: implement only supported, readback-verifiable commands.
6. **UX — command surface**: one ResolveNodeKit command vocabulary with separate Fusion/Color adapters. Default Resolve keyboard shortcuts are not changed.

## Development

```bash
python -m pip install -e . --no-build-isolation
python -m unittest discover -s tests -v
```

The repository ships development entrypoints:

- `scripts/Fusion/ResolveNodeKit_Tidy.py`
- `scripts/Fusion/ResolveNodeKit_TidyGroups.py`
- `scripts/Color/ResolveNodeKit_Probe.py` (read-only)

They currently assume the repository layout is intact so `src/` can be bootstrapped relative to the script. Packaging/install UX is intentionally deferred until host behavior is verified.

## Evidence boundary

Offline tests prove layout and adapter behavior against mocks only. They do **not** prove the current DaVinci Resolve host surface, GroupOperator viewport geometry, saved-project persistence, or Color-page API availability. Host-specific claims require a current-machine probe and readback.

## Prior art

`SoumyA16-git/Auto-Node-Tree` was reviewed as prior art for graph layout and failure modes. ResolveNodeKit does not vendor or fork that implementation. See `docs/PRIOR_ART.md`. Color API evidence is tracked in `docs/COLOR_API.md`, and recursive group behavior in `docs/GROUPS.md`.
