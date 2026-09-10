# Luna Max オーケストレーションと新規task引き継ぎ

Revision: LM-TAKEOVER-20260910-2 / RO-CANARY-20260910-1  
Mission: RNK-STRICT-ORTHOGONAL / 46slv/ResolveNodeKit / PR #5

## Requirements-first migration overlay — current

The old external-Operator-always interpretation is retired for new work. The
external Operator remains the rollback baseline and a qualified specialist
route, while the Coordinator selects the minimum sufficient execution locus
per requirement:

| Mode | Use when | Current qualification boundary |
|---|---|---|
| D / direct guarded | product context already has the required host-local capability | candidate only; every live write still uses Host Guard |
| S / dedicated Resolve Worker | host work is separable and independent host evidence earns the boundary | promoted for structural fixture readback only |
| H / host-local executor | CurrentComp, Comp Script, FlowView, Undo, or GUI-local context is required | candidate; semantic receipt qualification is the next WP1 route |

The Host Guard is topology-independent and mandatory for every mutable path:
exclusive user-wide lease, exact target identity, owned disposable state,
no-blind-retry after ambiguous calls, reversible/discardable mutation,
independent readback, cleanup/recovery, and terminal receipt with final `FREE`.
Raw comp/FlowView/Undo handles never cross the boundary; host-local code must
convert them to detached JSON-safe semantic evidence.

The source contracts are CodexOperations PR #10 at
`93b2e8008d27fa5c3afbf6dc94bd26c0d2d097b5` and PR #11 at
`e6b9c1f7e0db7504d53a56a4901eb034684a999e`. The matched readback and current
next-ready item are in
`docs/checkpoints/2026-09-11-requirements-first-topology.json`.

This overlay does not change G01–G14, downgrade a required gate, authorize a
project save, or authorize main merge.

## 1. Goal / completion boundary

新しいLuna Max Coordinatorが既存成果を引き継ぎ、参考profileに沿うwhole-comp整列、全ノードと実配線の水平垂直、非空nestedを含む全Group解除、実データ規模と元non-Group >=1100、処理保存、Undo exact、run2 moved=0、installed UI / same-run busy-result、性能、cleanupまで進める。

SO-10/SO-20/SO-30等の既存成果を再実装しない。G01–G14、no-save、main未merge、processing preservationは維持する。旧invocationの期限やAstra→Sol Bootstrapを新規taskへ自動継承しない。

## 2. Roles

| Lane | Owner | Contract |
|---|---|---|
| Coordinator | new Luna Max task | canonical queue/state/integrationの唯一のwriter。Goal選択、bounded委譲、証拠受領、統合、次工程へ進む |
| Worker | independent Luna Max context | 一つのcoherent outcomeだけを実装。focused testとEvidence Packetを返す |
| Verifier | fresh independent Luna Max context | exact candidateを反証的に判定。候補を修正しない |
| Resolve Host Owner | selected D/S/H lane; external Operator remains qualified fallback | live Resolveの唯一のHost Guard owner。driver/lease/host lifecycle/readback/cleanup/evidenceを所有 |

Coordinator/Worker/Verifierはruntime metadataで実model/effortを確認する。promptの自己申告だけでLuna Maxと判定しない。選択されたResolve Host Ownerは要件に必要な実行境界を所有し、既にqualification済みのexternal Operator profile/modelを名前合わせのため変更しない。

## 3. New-task takeover

1. live Git/common-dir/worktree/HEAD/dirty、remote PR、installed manifest、最新checkpoint、現在のprogram ownerと未完operationを読む。
2. 旧taskが実行中なら、勝手にownerを奪わずsafe checkpoint/停止を確認する。別missionは止めない。
3. 新task自身のpersisted IDとLuna Max runtime bindingを確認する。
4. current owner/epochを再読し、既存mechanical lease/owner contractでcompare-and-setする。epochを決め打ちしない。
5. old writer fenced、新owner readback、first bounded work startまで確認してtakeover成立。
6. takeover記録だけを成果にせず、そのまま次のready Goalへ進む。

既存`handoff_state`のAstra/Sol receiptは歴史的証拠として保存する。新Luna IDを`sol_thread_id`へ上書きしない。今回のownerは`luna_execution.json`とactual lease/readbackで記録する。

## 4. Guarded host execution — current route

### 4.1 Trigger

live DaVinci Resolveの状態観測、実機validation、Fusion/Timeline等のhost behavior、Resolve-side readback、restart/reconnect、host-only acceptanceが必要になった時だけ、Requirement Briefに基づくD/S/H Host Ownerを選ぶ。静的コード読解、unit test、docsだけなら起動しない。

### 4.2 Parent -> Host Owner envelope

親Lunaは「どう操作するか」ではなく「何を成立させるか」だけを渡す。

```yaml
objective: <Resolve上で成立させる目的>
target:
  project: <known identity or current-policy>
  timeline: <optional>
  comp: <optional>
done:
  - <observable condition>
restore_policy: restore | keep_requested_changes | scratch_disposable
evidence:
  - resolve_version
  - driver
  - lease
  - before_after
  - verification
```

通常parent promptへMCP tool名、driver指定、Python method、GUI sequence、lease手順、restart手順を書かない。

### 4.3 Selected Host Owner owns the lifecycle

選択されたHost Ownerが次を一つのcapabilityとして閉じる。external Operatorを使う場合はそのpackageがこの責務を持つ。

```text
RECEIVE
 -> INVENTORY
 -> ACQUIRE_LEASE
 -> SELECT_DRIVER
 -> CAPTURE_PRE_STATE
 -> ACT
 -> VERIFY
 -> CLEANUP_OR_COMMIT_REQUESTED_CHANGE
 -> FINAL_READBACK
 -> RELEASE_LEASE
 -> RETURN_EVIDENCE
```

Operator内部のdriver候補は、current qualified surfaceに基づくBlackmagic native MCP、qualified compatibility MCP、scripting、GUI。driver選択はOperator内部責務。21.1 native MCPはqualified surfaceでは優先候補だが、未保存/default projectや未qualified workflowで無条件primaryにしない。

### 4.4 Current implementation boundary

Codex 0.153.4では `global MCP disabled + same-session child role enables MCP` を正規経路にしない。parent Resolve MCP visibility 0は維持し、external Resolve Operatorはrollback/capability baselineとして保持する。

概念経路:

```text
Luna Coordinator
 -> selected D/S/H Host Guard owner
 -> exclusive user-wide lease
 -> capability router or host-local executor
 -> native MCP / qualified compatibility MCP / scripting / GUI
 -> Resolve
```

RNKの古いcheckpointでsame-session系Operatorに`davinci-resolve` surfaceが見えなかったことを、current Operator方式の失敗やResolve API不存在へ一般化しない。新規taskはまずRequirement BriefとAG-V2を通し、選択したHost Ownerにdriver選択を任せる。external Operatorを使う場合は既存package/launcherを通常通り呼ぶ。

### 4.5 If automatic delegation fails

一回の失敗で経路を捨てない。`routing / launcher / lease / driver / capability / restore / evidence / boundary` に分類し、同一failure fingerprintを新証拠なしで再実行しない。

- `routing`: parentからexternal Operatorへ入れていない。Operator package/launcher routingを修復。
- `launcher`: external runtimeが開始/継続できない。launcher/actual configを限定修復。
- `lease`: BUSYならhostへ触れずqueue/offline継続。lease機構を迂回しない。
- `driver`: selected driverが必要capabilityを持たない。Operator内部でqualified fallbackを選択。
- `capability`: qualifiedな安全routeがない。materially differentなD/S/H probeへ切り替えるか、`BLOCKED` / `INTEGRATION_GAP`を返す。parent direct accessへの恒久fallbackはしない。
- `restore`: restoration boundaryを満たせない。writeを拡張しない。
- `evidence`:操作はできても独立readbackが不足。PASSにしない。

修復後は同じsemantic taskで再qualificationする。同一route・同一evidence stateの無意味なretryを増やさない。

### 4.6 Result contract

```yaml
status: PASS | PARTIAL_PASS | BLOCKED | FAIL | BUSY
resolve_version: <exact>
driver:
  type: native_mcp | third_party_mcp | scripting | gui
  identity: <observed>
lease:
  acquired: true|false
  final: FREE|HELD|UNKNOWN
operations: []
verification: []
restore:
  status: exact | equivalent | partial | not_required | failed
remaining_boundary: []
evidence: []
```

親Lunaはこのsemantic resultを製品gateへ照合し、driver detailをRNK側へ複製しない。

## 5. RNK execution route

| Stage | Outcome | Existing tasks |
|---|---|---|
| R0 takeover | 新Luna owner、旧writer不在、canonical source/install把握 | execution-only、product gate昇格なし |
| R1 host preflight + offline integration | Resolve OperatorへSO-11相当のread-only objectiveを委譲。並行してsnapshot adapter / planner integration / UI glue | SO-11, SO-50。SO-20/30を再実装しない |
| R2 strict preserve E2E | small non-empty nested compでsnapshot -> strict plan -> native view -> readback、installed UI Run/Cancel/busy/result | SO-30, SO-50, SO-60 |
| R3 flatten | non-empty nested/cross-boundaryを全Group=0、non-Group/processing意味保存、Undo exact | SO-40, SO-61 |
| R4 large | real-scale duplicate + >=1100 original non-Group fixtureでpreserve/flatten、3 real-changing runs、run2、performance、all-edge/rectangle/processing | SO-70, SO-71 |
| R5 finish | recovery/cancel/timeout、final install、fresh Verifier、PR/readback、exact cleanup | SO-80, SO-90, G01–G14 |

OperatorがBUSY/BLOCKEDでも独立offline作業を進める。flatten blockerがあってもpreserve laneを進める。ただし最終Doneで必須gateをoptionalへ下げない。

## 6. Luna orchestration loop

```text
OBSERVE live state
 -> choose next coherent Goal
 -> bounded Luna Worker
 -> deterministic validation
 -> fresh Luna Verifier where warranted
 -> integrate/evidence/state
 -> choose next ready Goal
```

Worker packetは`Task / Owned / Read-Start / Do / Do not / Validation / Return`。Coordinator transcriptや全PLANを貼らない。返却はcompact Evidence Packet。

同じfailure fingerprintが2回かつ新証拠なしなら、同じ3回目をしない。routeを変える。上位判断が本当に必要な時だけbounded diagnosisへescalateし、実装責任はLunaへ戻す。Resolve固有のrouting/driver/lease問題はまずResolve Operator package側で閉じる。

## 7. Evidence / install / safety

- offline testはcanonical worktreeのimport provenanceを記録する。
- source candidate / publication / installed manifestを分ける。
- direct controller、actual widget、native view、wire display、processing state/renderは別proof。
- live writeはResolve Operatorのlease内、disposable target、before/after/readback、Undo/cleanupで行う。
- project save、main merge/release、force push、unrelated deletion、credential bypass、PC reboot、global shortcut変更は禁止。
- Resolve launch/quit/restart、normal operation、reversible validation mutationは既存standing authority内で、Operatorが必要時に自律実行する。

## 8. Prompt orchestration CANARY

`PROMPT_ORCHESTRATION_TRIAL.md`を同時に実地テストする。特に`Resolve Operator automatic delegation` candidateを代表taskで検証する。

成功条件は、親Lunaがhigh-level objectiveだけを渡し、Operatorが余計な確認を増やさず、自動起動、正しいdriver routing、exclusive lease、independent readback、cleanup/recovery、structured evidence returnまで閉じること。

この一案件だけでglobal durable routingへ昇格しない。結果を`PROMPT_ORCHESTRATION_TRIAL_RESULT.{md,json}`へ記録し、Learning Gateで再利用価値を判定する。
