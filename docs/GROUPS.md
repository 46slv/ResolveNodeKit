# Fusion GroupOperator contracts

ResolveNodeKit must support deeply nested Fusion `GroupOperator` trees without flattening or ungrouping them.

This document separates three different behaviors that must not be conflated:

1. hierarchy-aware layout;
2. runtime visual expansion;
3. fit-to-contents of an already expanded group.

## 1. Shared hierarchy model

Every GroupOperator is both:

- a node in its parent scope; and
- a container owning a child scope.

Shared invariants:

- preserve direct parent/child membership;
- discover children through `GetChildrenList()` and parent ownership through `ParentTool` / `TOOLH_GroupParent` where available;
- layout each hierarchy scope independently;
- project cross-boundary connections to the visible GroupOperator for layout planning only;
- never rewire the real graph to match the projection;
- preserve processing parameters/keyframes/media/render state;
- snapshot/readback/rollback every host mutation path.

For an edge from a node inside `GroupB` to a sibling inside `GroupA`, the `GroupA` layout may see `GroupB -> sibling` while the `GroupB` layout sees its actual internal edge. This is only a planning projection.

## 2. `Tidy Nested` — recursive layout without requiring visual expansion

This is the independent fallback/product feature intended to keep progress useful even when runtime Group expansion is not yet scriptable.

Target API/script:

- `tidy_nested_comp(...)`
- `scripts/Fusion/ResolveNodeKit_TidyNested.py`

Required behavior:

- leave every GroupOperator's visual expanded/collapsed state unchanged;
- recursively tidy direct children in every managed scope;
- preserve membership and connections;
- be deterministic on repeated runs;
- fail closed if nested identity/hierarchy cannot be resolved safely.

### Host gate

Do not declare this feature ready from mocks alone. First prove on a real collapsed GroupOperator that child positions can be read and changed while the group remains collapsed, and that those writes do not alter membership, connections, processing state, or display state.

If collapsed child positions cannot be safely written/read back, classify this feature separately as host/API blocked. Do not weaken invariants to make it pass.

## 3. `Tidy + Expand Groups` — strict runtime visual-expansion contract

The user-visible meaning is strict:

- groups remain GroupOperators;
- nested groups are actually opened in the Fusion UI/runtime sense;
- their internals are tidied;
- a second run is stable;
- structure and processing state are unchanged.

It must never silently degrade to `Tidy Nested`.

### Disproven serialized-settings path

A real-host run on DaVinci Resolve Studio 21.0.3.7 measured:

1. obtain GroupOperator settings;
2. set `ViewInfo.Flags.Expanded = true`;
3. call `LoadSettings`;
4. host returns `True`;
5. immediate `SaveSettings` readback does **not** retain the expanded state.

The same behavior was reported with and without Undo and on both empty and populated groups. `Size`, `Scale`, and `Offset` did not change and `GetAttrs` did not expose a usable expanded flag.

Therefore `LoadSettings(Expanded=true)` is not a proven runtime expansion API on that host. Do not keep retrying it without new evidence.

### Current expansion hypothesis

Fusion's real UI has an Expand/Collapse operation for Group nodes. The next research target is therefore a runtime command/action path, not another serialized-settings rewrite.

Investigation must remain bounded and readback-verifiable:

1. inspect already-configured OpenCode/MCP/Fusion runtime actions;
2. inspect scriptable named actions/commands if exposed;
3. canary one disposable Group only after exact target selection is proven;
4. invoke one action;
5. independently verify actual expanded/subflow state, membership, connections, Undo, and cleanup;
6. prove deterministic targeting before recursive bulk expansion.

Do not install a new desktop automation stack, change global shortcuts, or send blind keystrokes merely to bypass this blocker without new user authority.

If no safe action route exists after evidence-driven investigation, classify visual expansion `BLOCKED_API`. Other ResolveNodeKit lanes continue, but `MISSION_COMPLETE` remains open under the current user requirement.

## 4. Fit to contents

Fit-to-contents depends on a real runtime-expanded group. It is not meaningful to infer a fit formula while expansion itself is unproven.

Once expansion passes:

- measure actual `GroupInfo.Size`, `Scale`, `Offset`, group position, direct-child positions/bounds, and visible UI result;
- change one variable at a time on a canary;
- derive semantics from repeated measurements;
- implement a minimal fit with padding;
- read back geometry and verify all direct children are visible;
- repeat through 2–3 nesting depths;
- prove second-run stability and Undo/rollback.

Never infer the formula from `.setting` examples alone.

## 5. Identity model

Nested groups may eventually expose duplicate tool names or host objects that are reacquired after settings/action operations. The implementation must not assume a flat tool name is globally unique if host evidence disproves it.

Escalation order:

1. stable live object where valid;
2. reacquisition by verified unique name within scope;
3. hierarchical path / parent-qualified identity;
4. other measured stable host identifier.

If no unique/readback-stable identity exists for a mutation, fail closed.

## 6. Offline evidence

Existing offline recursive-group tests prove only the modeled contracts, including hierarchy projection, deterministic scope layout, rollback behavior, and hierarchy-cycle refusal. They do not prove current runtime expansion semantics or UI geometry.

The real-host checkpoint is recorded in `docs/checkpoints/2026-09-05-host-group-expansion-blocker.md`.

## 7. Evidence basis

Fusion scripting references expose Group parent/child relationships and operator settings surfaces. Serialized Group settings can contain `ViewInfo = GroupInfo` and an `Expanded` flag, but the measured host result demonstrates that serialized presence does not itself prove a runtime-writable expansion state. Runtime behavior always outranks the serialized-file inference.
