# Host validation checklist

Offline tests are necessary but insufficient. Before calling a host feature ready, record the exact Resolve/Fusion version and use structured OpenCode/MCP evidence plus independent parent verification.

For current live gate/order, read `docs/CURRENT_STATE.md`. For large graphs, use `docs/EVIDENCE_PROTOCOL.md` rather than whole-graph MCP dumps.

## Fusion Flat Tidy

Current measured status: HOST-PASS on Resolve Studio 21.0.3.7 canaries.

Validated behavior includes:

- script loads in the intended host path;
- `GetToolList`, `CurrentFrame.FlowView`, `GetPosTable`, and `SetPos` usable;
- serial chain;
- BG + FG -> Merge;
- EffectMask branch;
- isolated node;
- measured grid/readback handling;
- second run position-identical / moved=0;
- Undo returns prior positions;
- fail-closed rollback behavior;
- connections preserved;
- sampled processing state unchanged.

Still separate from product readiness:

- save/reopen persistence must only be tested on an explicitly safe save target; never force-save the user's active project merely to close this gate.

## Fusion `Tidy Nested`

Current measured status: HOST-PASS on the fixed canary path.

Required/validated contract:

- nested GroupOperators remain groups;
- direct parent/child membership unchanged;
- collapsed/expanded display state unchanged by `Tidy Nested`;
- root/parent/nested scopes receive deterministic layouts;
- cross-boundary projection is planning-only;
- connections unchanged;
- sampled processing state unchanged;
- second run position-identical / moved=0;
- Undo restores prior positions;
- rollback remains fail-closed.

The fixed implementation uses a bounded fixed-point planning loop before the host write to avoid settle drift caused by measured FlowView readback offsets.

### Large graph stress for `Tidy Nested`

Not yet PASS.

The current large composition (~1107 tools / 31 nested groups in the measured context) exceeded the MCP/bridge transport envelope when one long in-host evidence walk was attempted. Resolve remained responsive and no product mutation ran.

Retry requirements:

- do not repeat the same long whole-graph call;
- establish a safe medium-scope/chunk size first;
- keep each host call short;
- compute compact canonical signatures in-host where possible;
- aggregate bounded evidence deterministically;
- only mutate once pre-evidence can complete reliably;
- compare pre/post/second-run evidence using `docs/EVIDENCE_PROTOCOL.md`.

## Fusion strict `Tidy + Expand Groups`

Current status: runtime visual expansion UNRESOLVED / serialized-settings path disproven.

The strict user-visible contract is:

- groups remain GroupOperators;
- nested groups actually open in the runtime/UI sense;
- internals are tidied;
- all intended contents become visible;
- membership/connections/processing state remain unchanged;
- second run stable;
- Undo/rollback understood.

Measured on Resolve Studio 21.0.3.7:

- `SaveSettings` -> set `ViewInfo.Flags.Expanded=true` -> `LoadSettings` returns success;
- immediate `SaveSettings` readback does not retain the expanded state;
- same path failed to establish runtime expansion on empty/populated groups, with/without Undo;
- no usable expanded flag appeared in `GetAttrs`;
- `Size`/`Scale`/`Offset` did not establish a fit path.

Do not repeat that exact hypothesis without new evidence.

Next research target: a deterministic, readback-verifiable runtime Expand/Collapse command/action path. No blind keystrokes, new desktop automation stack, global shortcut mutation, ungrouping, or flattening merely to bypass this gate without new authority.

## Fusion fit-to-contents

Prerequisite: strict runtime visual expansion PASS.

Only after a real expanded group exists:

- measure `GroupInfo.Size`, `Scale`, `Offset`, group position, direct-child bounds, and visible result;
- change one variable at a time on a canary;
- derive geometry semantics from measured host behavior;
- implement a minimal fit with padding;
- verify all direct children visible through 2–3 nesting depths;
- prove second-run stability and structural/processing invariants.

Do not infer a formula from `.setting` examples alone.

## Fusion low-risk operations

Ready independent lane after Flat Tidy PASS.

Candidate order:

1. Align selected horizontal/vertical;
2. Distribute selected horizontal/vertical;
3. selected/component-scope tidy;
4. upstream/downstream/connected-component selection;
5. safe group display helpers only where host API is proven;
6. frame/center selected only if a real deterministic action/API exists.

Each command requires explicit scope, deterministic result, readback, no processing-state change, and Undo/rollback where appropriate.

## Fusion rewiring operations

Only after low-risk command safety patterns are stable.

Before any rewiring:

- snapshot exact affected edge/input/output identities;
- perform minimal writes;
- read back the complete affected edge set;
- rollback exactly on mismatch;
- fail closed on ambiguous input semantics.

## Color capability gate

Current measured status: read-only capability map PASS for the current project context.

Measured on Resolve Studio 21.0.3.7:

- current-item Graph access available in the measured context;
- measured item Graph contained one node;
- timeline-level Graph available but empty;
- no Color groups exist in the current project, so group Graph behavior remains context-unexercised;
- observed Graph surface includes node count, label, LUT, cache, enabled state, tools, and grade-related operations;
- physical Color-node XY position API absent from the measured callable surface.

### Color mutations

Only add operations with observable postconditions/readback, e.g. enable/disable, cache mode, LUT helpers, inspection/navigation, and other measured surfaces.

Do not claim Color physical XY layout unless a future measured API/action proves it.
