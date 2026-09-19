# Arrange live host acceptance recovery — 2026-09-07

## Scope

This is the bounded continuation after `abe53f6`.  It does not change the
production seam and does not repeat UIA/MSAA, step-5 menu Invoke, OpenCode/Muse,
or the blocked `LoadComp`/`Paste` route.

## Phase 0 result

The first and only fresh connection was a read-only, bounded
`davinci_resolve.script_plugin.run_inline` Python probe requesting the current
project, timeline, Fusion comp, tool count, and page.  It produced no response
for more than 60 seconds despite the requested 15-second bound.  The call was
terminated once the material hang was established; no second Resolve probe was
sent.

Local process observation at the stop point:

- Resolve PID `23240`: `Responding=True`, title
  `DaVinci Resolve Studio - _mcp_RNK_SEAM_20260907`.
- embedded `fuscript.exe` PID `8636`, parent Resolve: `Responding=True`.
- scripting endpoint: unavailable / no readback.

This is `BLOCKED_HOST`, not a product or handler failure.  A Resolve/embedded
Fusion scripting endpoint restart is operationally required before the next
acceptance attempt; no restart was performed in this run.

## Safety boundary

Because the read-only gate did not return:

- prior disposable cleanup was not attempted;
- `PSD2Fusion` / `Timeline 1` restore was not claimed;
- no new fixture, handler run, busy/result observation, Undo, or second run was
  performed;
- no save occurred;
- no host PASS was emitted.

The exact machine-readable record is
`2026-09-07-arrange-live-host-blocked.json` beside this checkpoint.

## Next gate

After a Resolve restart or equivalent endpoint recovery, perform one successful
read-only identity probe first.  Then delete only the exact
`_mcp_RNK_SEAM_20260907` disposable remnant, restore `PSD2Fusion` / `Timeline 1`
and verify `COMPB_Modified=false`, and only then run the existing direct-handler
fixture on a fresh bounded AddTool/API path.  Do not repeat the blocked
`LoadComp`/`Paste` route or any accessibility probe.
