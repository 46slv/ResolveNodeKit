# SO-11 qualified standalone nested fixture host readback

Observed 2026-09-10 JST on the Luna Max continuation. The external Resolve
Operator loaded the already-qualified `nested_group_v1` registry composition on
DaVinci Resolve Studio `21.1.0.14` through the compatibility MCP lane and
closed it in the same invocation. No AddTool/Paste construction was retried.

The independent live structure readback and the RNK `host_snapshot.py` adapter
agree on the required structural evidence:

- 10 unique tools, 2 non-empty `GroupOperator`s, maximum depth 2;
- `OuterGroup = [OuterSource, InnerGroup, OuterProcess]`;
  `InnerGroup = [InnerSource, InnerMask, InnerProcess]`;
- `MainOutput1` present for both groups and `TOOLS_Name`/`TOOLS_RegID`/
  `TOOLI_ID` identity read back for every tool;
- 7 direct labelled edges, including `InnerProcess -> OuterProcess` and
  `OuterProcess -> RootProcess` boundary crossings;
- adapter output JSON-safe with `ports=complete` and no empty substitution for
  unsupported/error fields.

The adapter repair reconciles the measured Resolve 21.1 flattened root
inventory with `GetChildrenList()` only when object identity or `TOOLI_ID` plus
stable metadata agree. Ambiguous duplicate names still fail closed. Focused
adapter tests are 8/8 and the canonical suite is 170/170.

Mutation and safety evidence: layout/graph/settings/Undo/project save all 0;
fixture load=1, close=1; protected project/timeline/Master state unchanged;
post-close current comp absent; cleanup exact; launcher final lease `FREE`.

G01 is promoted to `PASS`. The snapshot still records exact non-complete
coverage (`position`, `group_boundary_proxies`, parameters, keyframes,
expressions, instances, media, time range, and a `tool_state` read error), so
`strict_request` must remain fail-closed until its complete-snapshot contract is
met. This checkpoint does not promote G02–G14 or product completion.

Evidence JSON: [`2026-09-10-so11-nested-group-host-pass.json`](2026-09-10-so11-nested-group-host-pass.json)
