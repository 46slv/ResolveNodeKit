# Semantic Arrange FIRST_USABLE scope — 2026-09-07

## Decision

The first usable Semantic Arrange contract is the whole active Fusion
composition in preserve mode:

```text
ArrangeDialogState(include_unselected=True, ungroup=False)
```

This is a product-scope simplification, not a planner rewrite.  The existing
group-local semantic planner remains the layout engine and continues to apply
recursively to root and nested GroupOperator scopes.

## UI

The production Comp entry no longer exposes the two checkbox controls.  It
uses a text-only confirmation:

```text
ResolveNodeKit - Arrange
現在のFusionコンポジション全体を整列します。
[実行] [キャンセル]
```

The host-provided AskUser confirmation buttons remain the transport.  The
selection-only and ungroup states are not reachable from FIRST_USABLE UI.

## Scope boundaries

- `include_unselected=False` remains explicit regression/experimental
  coverage, including fixed-obstacle tests.
- `ungroup=True` remains fail-closed and is not a release gate.
- Required FIRST_USABLE acceptance is recursive Group preservation,
  connection/tool identity invariance, exact Undo, second-run `moved=0`,
  installed-entry smoke, and bounded large-graph stress.
- The existing UIA/MSAA accessibility limitation remains separate; this scope
  change does not retry those probes.

## Implementation and verification

Defaults were aligned in `ArrangeDialogState`, `arrange_comp`, the installed
entry environment override, and `scripts/host/verify_arrange_behavior.py`.
The host launcher now constructs a whole-composition fixture without relying
on an explicit selection.  Selection-only classifier coverage remains in the
regression suite.

Installed-entry real-host smoke and large-graph stress remain the next host
acceptance lanes; this checkpoint records the scope decision and offline
contract only.
