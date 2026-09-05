# ResolveNodeKit

Node workflow tools for **DaVinci Resolve Fusion and Color**.

The project is not a Blender Node Wrangler port. It targets Resolve-specific node workflow friction with independent implementations and host-specific adapters.

## Current scope

### Fusion — implementation started

- deterministic **Tidy Graph** layout;
- disconnected and isolated tools included so they cannot be silently overlapped;
- cycle detection: fail closed before any position write;
- `StartUndo` / `EndUndo` when the host exposes them;
- original-position snapshot, readback verification, and rollback on failed writes;
- no connection, parameter, keyframe, tool creation, or render mutation in Tidy Graph.

### Color — capability work started

Fusion and Color do **not** share one assumed API. Color support starts with a read-only capability probe. Node graph query/manipulation features are added only after current Resolve host verification.

## Roadmap

1. **F1 — Fusion Tidy Graph**: host-verify on small, branched, mask, disconnected, and large graphs.
2. **F2 — Fusion node operations**: align/distribute, insert-between, connect/reconnect, swap inputs, detach/bypass, upstream/downstream selection.
3. **C1 — Color API boundary**: verify current clip/timeline/group NodeGraph acquisition and available operations on the installed Resolve version.
4. **C2 — Color node operations**: implement only supported, readback-verifiable commands.
5. **UX — command surface**: one ResolveNodeKit command vocabulary with separate Fusion/Color adapters. Default Resolve keyboard shortcuts are not changed.

## Development

```bash
python -m pip install -e . --no-build-isolation
python -m unittest discover -s tests -v
```

The repository ships two development entrypoints:

- `scripts/Fusion/ResolveNodeKit_Tidy.py`
- `scripts/Color/ResolveNodeKit_Probe.py` (read-only)

They currently assume the repository layout is intact so `src/` can be bootstrapped relative to the script. Packaging/install UX is intentionally deferred until host behavior is verified.

## Evidence boundary

Offline tests prove layout and adapter behavior against mocks only. They do **not** prove the current DaVinci Resolve host surface, UI layout semantics, saved-project persistence, or Color-page API availability. Host-specific claims require a current-machine probe and readback.

## Prior art

`SoumyA16-git/Auto-Node-Tree` was reviewed as prior art for graph layout and failure modes. ResolveNodeKit does not vendor or fork that implementation. See `docs/PRIOR_ART.md`.
