# ResolveNodeKit

Node workflow tools for **DaVinci Resolve Fusion and Color**.

ResolveNodeKit targets Resolve-specific node workflow friction. It is not a Blender Node Wrangler port and not an Auto-Node-Tree fork.

## Current status

The project is actively host-validating its first Fusion layout features.

- **Flat Fusion Tidy** — real-host canary evidence exists on Resolve Studio 21.0.3.7. Host-measured grid/readback fixes still need to be reconciled into the current canonical task branch before this is called current-branch HOST-PASS.
- **Nested hierarchy layout** — per-group-scope layout exists offline. A separate `Tidy Nested` host canary is next; it must keep groups collapsed/expanded exactly as they were while arranging their children safely.
- **Visual Group expansion** — the tested serialized `Expanded=true` / `LoadSettings` path is disproven on the measured host because the state does not persist on readback. Runtime Expand/Collapse action research remains open.
- **Fit to contents** — intentionally deferred until real runtime Group expansion is proven.
- **Color** — read-only graph capability work exists; current-host capability mapping is still required before mutations.

The user's nested-group visibility requirement remains mission-critical. ResolveNodeKit will not call the mission complete by silently replacing “open nested groups” with “tidy hidden contents.”

For the operational source of truth, read:

- `AGENTS.md`
- `docs/CURRENT_STATE.md`
- `docs/ORCHESTRATION.md`
- `docs/HOST_VALIDATION.md`

## Fusion design

Layout commands are designed to be deterministic, reversible, and structural-state preserving:

- no connection changes;
- no processing parameter/keyframe changes;
- no tool/media/render mutation;
- explicit position/settings snapshot;
- bounded write;
- readback verification;
- rollback on mismatch;
- Undo integration where host behavior is proven.

Nested GroupOperators are modeled per hierarchy scope. Cross-boundary edges may be projected to the visible Group node for planning only; the real graph is never rewired to match that projection.

## Feature lanes

### Fusion layout

- `Tidy Graph` — flat/whole-comp deterministic layout.
- planned `Tidy Nested` — recursively arrange children inside nested GroupOperators without requiring visual expansion.
- strict `Tidy + Expand Groups` — separate mission-critical feature that must perform real runtime expansion, not merely edit serialized settings.
- fit-to-contents — measured only after expansion works.

### Fusion workflow operations

Planned order after Flat Tidy closeout:

- align/distribute selected nodes;
- selected/component-scope tidy;
- upstream/downstream/connected-component selection;
- then bounded rewiring commands such as insert-between, reconnect, Merge input swap, and detach with exact edge readback/rollback.

### Color

Fusion and Color do not share one assumed API. Color support is capability-driven:

- read current graph/node state where exposed;
- map actual timeline/clip/group Graph surfaces on the installed host;
- add only mutations with observable postconditions and rollback/exclusion contracts;
- treat physical Color node XY layout as a separate capability question.

## Large graph validation

PSD2Fusion-scale graphs can exceed practical MCP snapshot payloads. Large-host validation must compute compact canonical signatures inside Resolve/Fusion and return counts/hashes/timing plus focused mismatches rather than repeatedly serializing an entire 1000+ node graph.

## Development

```bash
python -m pip install -e . --no-build-isolation
python -m unittest discover -s tests -v
```

Development entrypoints currently include:

- `scripts/Fusion/ResolveNodeKit_Tidy.py`
- `scripts/Fusion/ResolveNodeKit_TidyGroups.py` (strict expansion path; host-blocked on the measured serialized-settings method)
- `scripts/Color/ResolveNodeKit_Probe.py` (read-only)

A separate `ResolveNodeKit_TidyNested.py` should be added only after the collapsed-group child-position host canary passes.

## Roadmap / completion

Work is dependency-driven rather than blocked behind one feature:

1. reconcile the local host-measured fixes with the fresh remote task branch;
2. close current-branch Flat Tidy host acceptance;
3. canary/implement `Tidy Nested`;
4. stress nested tidy on a large duplicate using compact in-host evidence;
5. build low-risk Fusion helpers;
6. map/add Color capabilities independently;
7. continue runtime Group Expand/Collapse research in parallel;
8. if expansion succeeds, measure and implement fit-to-contents;
9. build unified command surface and safe packaging;
10. produce an accurately limited usable beta;
11. close `MISSION_COMPLETE` only when all explicit mission-critical requirements pass or the user explicitly changes scope.

See `docs/ORCHESTRATION.md` for prerequisites, stop criteria, autonomous authority, and checkpoint rules.

## Prior art

`SoumyA16-git/Auto-Node-Tree` was reviewed for graph-layout ideas and failure modes. ResolveNodeKit does not vendor or fork it. Blender Node Wrangler is a UX reference for workflow value, not a naming, shortcut, UI, or code compatibility target.
