# Semantic Arrange v1 — large-graph flatten amendment

Status: READY / SUPERSEDES conflicting clauses in PLAN.md and RUNBOOK.md
Updated: 2026-09-08 JST
Applies to: `feat/semantic-arrange-v1-20260906` / PR #5

## 1. User direction change

The mission target is raised beyond the already-passed small-host whole-comp preserve-mode FIRST_USABLE.

Required end-state now includes both:

1. **Large whole-comp arrangement:** a PSD2Fusion-scale composition on the order of ~1100 tools must complete successfully without relying on a human click or a single oversized MCP payload.
2. **Flatten-all mode:** ResolveNodeKit must be able to ungroup all eligible `GroupOperator`s in the active composition, then semantically arrange the resulting flat graph while preserving processing semantics.

The existing preserve-mode FIRST_USABLE remains a valid passed baseline and regression oracle. It is not rolled back. However, this amendment makes large-scale execution and safe flatten-all implementation required for the new completion target.

## 2. Completion states

Keep these separate:

```text
FIRST_USABLE_PRESERVE: PASS   # already proven
LARGE_PRESERVE: REQUIRED
FLATTEN_ALL_SMALL: REQUIRED
FLATTEN_ALL_LARGE: REQUIRED
RELEASE_CANDIDATE: only after all required gates below pass
```

`SAV1-90` human UI smoke is not the next task. Autonomous large/flatten gates come first.

## 3. Revised progress route

```text
existing SAV1-30/40/50 PASS
  -> SAV1-55 flatten capability discovery + small disposable proof
  -> SAV1-56 recursive/nested flatten correctness
  -> SAV1-60R large preserve optimization + host PASS
  -> SAV1-65 large flatten-all stress (~1100 tools target)
  -> SAV1-70 docs / product UI reconciliation
  -> SAV1-80 fresh verifier rerun on new candidate
  -> SAV1-90 conditional one-click release smoke only if still required
```

A prior `SAV1-80 PASS` predating this amendment is not sufficient for the amended candidate because required behavior changed.

## 4. SAV1-55 — implement safe flatten-all on small fixtures

### Goal

Implement a production path equivalent to:

```text
active comp
-> exact target bind
-> full structural snapshot
-> recursively ungroup every eligible GroupOperator
-> verify flattened structure
-> semantic whole-comp planning on the resulting flat graph
-> bounded position writes
-> readback/invariant verification
-> one owned Undo transaction
```

### Discovery budget

Use real Resolve/Fusion host behavior. Investigate bounded, reversible host APIs/operations for Group ungrouping. Do not assume an API exists from docs alone.

Allowed:
- measured GroupOperator methods/actions
- documented/host-proven structural operations
- settings transformations only if they preserve existing child tools/processing identity and can be read back exactly
- Resolve restart / fuscript recovery under the existing RUNBOOK authority

Forbidden:
- blind UI/keyboard automation
- coordinate clicks
- recreating the graph from guessed semantics
- deleting/recreating child tools as a shortcut
- bypassing invariants because a fixture looks visually correct

### Small-host acceptance

Use a disposable graph with nested non-empty Groups.

Required post-flatten facts:
- all eligible `GroupOperator`s removed from the flattened scope;
- every non-Group child tool remains present;
- child tool semantic identity is preserved; runtime object identity should remain when the host permits and any limitation must be explicit;
- connection signature is unchanged except for container membership representation that necessarily disappears;
- processing parameters / keyframes / expressions / media state are unchanged at the evidence level available to the host;
- no accidental tool duplication/deletion;
- resulting root graph is semantically arranged with no unintended overlaps;
- Undo restores the exact original Group hierarchy, membership, connections, and positions;
- second flatten+arrange run is stable (`group_count=0`, `moved=0`).

If exact restoration cannot be proven, the write must fail closed and this gate remains open.

## 5. SAV1-56 — nested/recursive flatten correctness

Exercise at least:
- Group containing ordinary children;
- nested Group inside Group;
- Group feeding a Merge rail;
- connections crossing former Group boundaries.

Flatten order must be deterministic and safe (e.g. deepest-first if that is what host evidence supports). Do not choose an order by guess.

Acceptance:
- post state has the expected flat topology;
- all former child nodes are arranged as normal semantic nodes/regions;
- no residual parent chains for removed Groups;
- exact connection hash preserved;
- Undo exact;
- run2 stable.

## 6. SAV1-60R — make large preserve-mode actually complete

The previous ~967-tool direct `execute_arrange_request` timeout is not accepted as the final large-graph state.

The worker must profile the production stages with compact timings:

```text
bind
snapshot
selection/scope resolution
hierarchy validation
semantic snapshot build
plan/fixed-point
desired-position build
writes
position readback
hierarchy readback
connection verification
Undo close
```

Optimize the real bottleneck rather than only shrinking evidence payloads.

Priorities:
1. eliminate repeated full-host traversals where equivalent verified data can be reused safely;
2. reduce per-tool host round trips;
3. separate product execution timing from MCP evidence transport;
4. compute compact hashes in-host;
5. preserve the exact mutation/readback/rollback contract.

Acceptance on a real/disposable PSD2Fusion-scale graph:
- approximately current real size (currently measured around 967 tools) completes successfully;
- additionally exercise a synthetic or existing **>=1100-tool** fixture if the real project is below 1100;
- no MCP timeout is used as success evidence;
- no Resolve/fuscript endpoint loss;
- connection/membership/tool-count invariants exact;
- first run completes and changes positions when needed;
- second run completes with `moved=0` / identical position hash;
- Undo exact where exercised;
- bounded wall time and stage timings recorded;
- no save; exact cleanup.

Performance goal: complete with substantial margin below the historical 300-second call limit. If the transport route itself imposes that limit, decouple compact launch/monitoring from evidence collection rather than letting the product action be killed by the transport timeout. Record the measured final wall time; do not fabricate an arbitrary speed PASS.

## 7. SAV1-65 — large flatten-all stress

Run the production flatten-all + semantic arrange path on:

1. the largest safe real PSD2Fusion-scale disposable duplicate available; and
2. a >=1100-tool fixture when the real graph is smaller.

Required compact pre/post evidence:

```text
target identity
host version
tool_count_pre/post
group_count_pre/post
max_group_depth_pre/post
non_group_tool_identity_hash
connection_hash
processing evidence status
position_hash
post_overlap_summary
first_run_moved
second_run_moved
Undo restoration hashes/timings
stage timings
endpoint health
```

Expected structural change for flatten mode:
- `group_count_post == 0` for all eligible Groups;
- non-Group tool set is preserved;
- group container removal is intentional and must be accounted for explicitly rather than treated as generic tool loss.

Hard gates:
- no missing/duplicated non-Group tools;
- no unintended connection change;
- no processing-state regression at the supported evidence level;
- no unresolved overlap caused by layout;
- Undo reconstructs original grouped state exactly;
- second run after successful flatten is stable;
- operation completes without endpoint loss;
- no project save.

A transport blocker alone is not sufficient to mark this gate done. Adapt transport/execution architecture until the product action itself can be proven, or return a specific host API blocker with evidence of why safe flattening cannot be implemented.

## 8. Product/UI direction

The current simplified whole-comp preserve UI remains valid while flatten-all is under development.

Once SAV1-55/56 pass, expose flatten-all only if the host path is fully rollback/Undo proven. The UI must make the structural change explicit, for example:

```text
現在のFusionコンポジション全体を整列します。
[ ] グループをすべて解除してから整列

[実行] [キャンセル]
```

Default remains preserve-mode unless the user explicitly selects flatten-all.

Do not expose a checkbox that only fails closed after it has become a required release feature; either the feature is host-proven and works, or it remains absent while the gate is open.

## 9. Revised mission completion

This amended mission is not complete merely because preserve-mode FIRST_USABLE and the final human smoke pass.

Required before `SEMANTIC_ARRANGE_STATUS: RELEASE_CANDIDATE`:

- existing small preserve host gates remain green;
- SAV1-55 PASS;
- SAV1-56 PASS;
- SAV1-60R PASS on PSD2Fusion-scale and >=1100 tools;
- SAV1-65 PASS on large flatten-all;
- full offline/install suite green on the final candidate;
- final Resolve state safe and clean;
- fresh independent verifier rerun after these changes;
- PR #5 docs/body updated to the new capability and exact limitations;
- main remains unmerged.

Human release smoke is last and cannot substitute for SAV1-60R or SAV1-65.

## 10. Failure policy

Normal implementation/performance failures are recoverable and should lead to profiling, host-safe redesign, focused tests, and another materially changed attempt.

Stop only for:
- exact host API limitation that makes safe flatten impossible after bounded alternative investigation;
- inability to restore/Undo a structural mutation exactly;
- endpoint still unavailable after authorized bounded restart recovery;
- required authority outside the existing user authorization.

Do not close the amended goal as `blocked` solely because the same UIA/MSAA accessibility limitation was observed again; that limitation is unrelated to large execution and flatten-all correctness.

## 11. Final report additions

The final report must include:

```text
FIRST_USABLE_PRESERVE
LARGE_PRESERVE
FLATTEN_ALL_SMALL
FLATTEN_ALL_NESTED
FLATTEN_ALL_LARGE
LARGE_TOOL_COUNT_TESTED
LARGE_WALL_TIME
UNGROUP_UNDO_EXACT
SECOND_RUN
ENDPOINT_HEALTH
RELEASE_SMOKE
```

This amendment supersedes any older statement that `Ungroup` or large-host PASS is optional for the current completion target.
