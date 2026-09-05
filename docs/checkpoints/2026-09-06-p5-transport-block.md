# Host checkpoint - P5 large stress transport block - 2026-09-06

Status: `BLOCKED_HOST` (MCP transport, feature-local). Resolve itself stayed alive and responsive throughout. No product-code failure was measured; the stress mutations never ran.

Worker route: OpenCode CLI 1.18.29 -> model flag `opencode-go/muse-spark-1.3-contributor` (agent `build`) -> davinci-resolve MCP 2.203.0 -> Resolve Studio 21.0.3.7. Structured events: `%TEMP%\rnk-p5\events.jsonl` (129 lines). Repo HEAD `b4988d5`, clean, no writes.

## Measured sequence

- Phase 0 PASS: PSD2Fusion bound, Timeline 1 with item tool counts [1107,1,1,1,1], 31 top groups on item 0.
- Phase 1 PASS: Timeline 1 duplicated to RNK_STRESS and verified identical; Timeline 1 re-verified untouched. Side effect observed: the duplicate op auto-created Timeline 1_archived_v02 (version-on-mutate archive copy, benign but must be cleaned).
- Phase 2 FAILED at transport: full in-host evidence walk over the 1107-tool comp timed out over MCP (-32001); chunked retry dropped the connection (-32000); MCP tools deregistered. One disciplined retry after cooldown, no hammering.
- No writes beyond the duplicate. No save issued. Rollback: not applicable (no mutation); cleanup: NOT performed (bridge unreachable).

## Stale host state (cleanup pending)

- RNK_STRESS (c7e676df-7bdc-4917-b87d-91b575db5280, last-known).
- Timeline 1_archived_v02 (fbfb2c80-e2dc-4e25-abbc-f869dc27dc65, auto-versioning side effect).
- Possibly an RNK_STRESS archived variant. Timeline 1 content untouched.

## Infra finding (out of repo scope, do not fix from here)

- The davinci-resolve MCP bridge collapses under sustained heavy walks: long in-host call -> -32001 timeout -> -32000 connection closed -> tools deregistered. Resolve itself stays responsive.
- Light calls (bind/list/counts/small pastes) work reliably in the same session.
- Consequence for future runs: keep every single in-host call SHORT and chunked; never one giant recursive walk; fresh opencode run = fresh bridge after a collapse.
- The bridge timeout knobs live in the davinci-mcp repo (`C:\Users\shiro\Documents\Codex\2026-09-01\davinci-mcp`), outside ResolveNodeKit task-branch authority.

## Next

1. Tiny cleanup run (light calls only): delete RNK_STRESS + Timeline 1_archived_v02 + any RNK_STRESS archived variant; verify [Timeline 1], Modified=false.
2. P5 retry with a transport-fitting strategy (medium-scope subtree stress with short chunked calls) OR defer P5 until bridge timeouts are raised out-of-band.
3. P6 low-risk ops (offline implement + small-disposable canary with light calls) and P3B remain independent.
