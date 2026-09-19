# ADR-0001 — Group-local semantic layout with elastic Merge spacing

Status: Accepted for design / implementation not yet default
Date: 2026-09-06

## Context

ResolveNodeKit already has host-verified generic `Tidy Graph` and hierarchy-preserving `Tidy Nested` behavior. Those commands prove that Fusion node positions can be changed safely with readback/Undo/rollback, but generic DAG layout alone does not fully capture how a large Fusion composition should read visually.

The target compositions are Merge-heavy and deeply grouped. A globally compact layout can be technically valid while still being hard to read because:

- Merge chains lose their visual role as the main composition rail;
- branch provenance becomes ambiguous;
- nested Group boundaries become visually weak;
- uniform spacing can crowd branch Groups and wires;
- a 1000+ node PSD2Fusion-style graph is better understood as nested local modules than as one flat DAG.

User-provided visual references also establish that a wider Merge-side interval can be desirable rather than defective.

## Decision

ResolveNodeKit semantic layout will use **group-local recursive scopes** and will prioritize **semantic readability over uniform density**.

Specifically:

1. root and every `GroupOperator` interior are independent layout scopes;
2. child Groups are treated as semantic boxes in the parent scope;
3. child interiors are laid out recursively using the same policy family;
4. the main output-oriented backbone is placed left-to-right;
5. Merge-heavy backbone runs receive dedicated rail treatment;
6. branch sources normally enter the rail vertically from above;
7. Merge-to-Merge spacing is elastic and may widen beyond ordinary rail spacing;
8. the planner never flattens Group hierarchy or rewires actual connections;
9. visual Group expansion and fit-to-contents remain separate host capabilities;
10. existing generic `Tidy Graph` / `Tidy Nested` remain the safe baseline until semantic layout is independently proven.

## Why elastic Merge spacing

The planner should not minimize total width at the cost of readability.

A Merge interval may widen to satisfy branch clearance, child-Group clearance, wire separation, or host-grid constraints. Unequal horizontal gaps along the same Merge chain are explicitly allowed.

Therefore:

> A wider Merge-side gap is not a layout failure by itself.

It is only a failure if the widening introduces worse overlap, crossing ambiguity, instability, or unbounded expansion.

## Why recursive local scopes

Flattening descendants into one global layout destroys the visual meaning of Group boundaries and makes large graphs harder to reason about.

Local scopes provide:

- bounded planning problems;
- stable parent/child composition;
- reusable semantic rules at every nesting depth;
- a direct path to future fit-to-contents once runtime Group expansion is host-proven.

## Safety consequences

Semantic layout remains a layout-only feature and must preserve:

- tool count;
- Group membership;
- connections;
- parameters/keyframes/expressions;
- media/grade/render state;
- visual Group expanded/collapsed state unless an explicit command owns it.

All host mutation remains snapshot -> plan -> bounded write -> readback -> invariant comparison -> rollback on mismatch.

## Product rollout consequence

Do not silently replace the existing host-verified commands.

Recommended rollout:

1. pure semantic planner and fixtures;
2. `tidy_semantic_comp(...)` / `Tidy Semantic` as a separate policy/entrypoint;
3. small host canaries;
4. nested-group host canaries;
5. large-graph stress using the compact evidence protocol;
6. only then consider making semantic layout the default Tidy policy.

## Related documents

- `../SEMANTIC_LAYOUT.md` — normative architecture
- `../SEMANTIC_LAYOUT_ACCEPTANCE.md` — acceptance/test contract
- `../GROUPS.md` — Group behavior and runtime expansion boundary
- `../EVIDENCE_PROTOCOL.md` — large-graph evidence transport
- `../references/README.md` — visual reference interpretation
