# Arrange production seam checkpoint — 2026-09-07

## Scope and recovery boundary

This checkpoint continues `feat/arrange-uia-e2e-20260906` after the measured
MSAA boundary.  The existing step-5 menu evidence and the UIA/MSAA candidate
records were reused.  No UIA/MSAA semantic probe, menu Invoke, OpenCode, or
Muse request was repeated.

The host accessibility result remains final:

```text
RUN_IDENTITY: BLOCKED_HOST_ACCESSIBILITY_HARD
CANCEL_IDENTITY: BLOCKED_HOST_ACCESSIBILITY_HARD
CHECKBOX_IDENTITY: BLOCKED_HOST_ACCESSIBILITY_HARD
```

## Implementation

The former inline post-dialog body in
`scripts/Fusion/ResolveNodeKit_Arrange.py` now delegates exactly once to
`resolve_node_kit.fusion.execute_arrange_request`.  The shared handler accepts
an explicit immutable `ArrangeDialogState` and owns:

- exact live target bind with `require_live=True`;
- real busy show/stage updates/hide;
- the existing `arrange_comp` snapshot/plan/write/readback/verify path;
- fail-closed refusal and target-mismatch outcomes;
- result construction and presentation after busy close;
- a JSON-friendly `ArrangeExecutionResult`.

The AskUser wrapper remains UI-only.  Cancel returns before the handler, and
the GUI Run path maps the dialog result to one handler call.  No alternate
Arrange algorithm or control-order fallback was added.

`scripts/host/verify_arrange_behavior.py` generates a Fusion-side source that
calls the same handler with explicit OFF/OFF state and classifies sidecar
readback into `UI_VISIBILITY`, `HOST_PRODUCT_BEHAVIOR`,
`HOST_INVARIANTS`, and `ACCESSIBILITY_LIMITATION`.  The one-shot Lua launcher
is `scripts/host/arrange_seam_launcher.lua`; it is not a UI probe.

## Verification

- Offline suite: 115/115 PASS (108 previous tests + 7 focused seam/verifier
  tests).
- `python -m compileall -q src scripts tests`: PASS.
- User-scoped install/hash verification: PASS at local commit
  `faa369a25e7a288d2d63d791e7a14c33eaa56fbb` before this checkpoint commit.

Focused tests cover Cancel-before-handler, exactly-one handler call with the
parsed state, target-bind refusal with visible result and zero writes, busy
hide-before-result on handler failure, and the behavior evidence classifier.

## Host status

The direct behavior run was not promoted to PASS in this checkpoint.  The
MCP/Fusion scripting endpoint was already blocked by a long-running disposable
`LoadComp`/`Paste` route while Resolve itself remained responsive.  The exact
orphan client was stopped after verifying it was a child `fuscript.exe` of the
Resolve process; Resolve was not restarted.  No UI control action or graph
mutation from the new handler was accepted as evidence.

The disposable project created for the attempted route is therefore a host
cleanup follow-up, not a product PASS.  The next host run must first restore
`PSD2Fusion` / `Timeline 1` through a fresh, short scripting connection, then
run the generated direct-handler source on a new disposable fixture.  Do not
repeat the blocked `LoadComp`/`Paste` call or any UIA/MSAA probe.

## Acceptance interpretation

The normal development seam is closed in source and offline tests; it no
longer requires a human Run/Cancel click.  Release smoke still requires the
separate host behavior evidence until the endpoint is recovered.
