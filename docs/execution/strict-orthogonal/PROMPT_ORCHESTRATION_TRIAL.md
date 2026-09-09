# Prompt orchestration trial — Luna Max continuation

Revision: PO-TRIAL-20260910-2  
Mission: RNK-STRICT-ORTHOGONAL / PR #5  
Status: READY / prospective operational trial, not product evidence

## 0. Primary research source

Requested source is now retrievable from ChatGPT Library:

`/AI Operating Context/Coding Intelligence/CODEX_PROMPT_ORCHESTRATION_RESEARCH_2026-08-28.md`

Relevant current section: **Provisional prompt candidate — Resolve Operator automatic delegation (2026-09-10)**, status `PROVISIONAL / CANARY`.

The candidate says that when live DaVinci Resolve operation, host validation, restart/reconnect validation, or Resolve-side readback is materially required, the parent Agent/Orchestrator should delegate the host work to the dedicated Resolve Operator. Parent passes only high-level objective, target/scope, observable Done, restore expectation, required evidence. Resolve Operator owns inventory, exclusive lease, driver selection, launch/quit/restart, operation, independent readback, cleanup/recovery, final readback, lease release, and structured evidence return.

Current detailed operational truth remains in the Resolve Operator package/domain owner rather than this trial memo. Shared package authority checked while authoring: `46slv/CodexOperations` PR #5, branch `docs/resolve-operator-package-20260908`, head `9958e78e382ba5a312cd0a6cc4887aaab2fe4a08`, `FIRST_USABLE: PASS`, `FULL_QUALIFICATION: PARTIAL_PASS`.

## 1. Hypotheses under test

Product truth outranks the experiment. G01–G14 are unchanged.

- **H1 short top-level contract**: Goal/Done/Start/Execution/Evidence/Authorityだけで継続できる。
- **H2 bounded Work Package**: Workerへ一つのcoherent outcome、owned scope、validation、return schemaだけを渡す。
- **H3 compact Evidence Packet**: raw transcriptなしでCoordinatorが次判断できる。
- **H4 Luna stays primary**: routine implementation/debug/testはLuna Max。上位diagnosisはevidence-triggered/non-sticky。
- **H5 same-evidence retry guard**: 同じfailure fingerprintが2回かつ新証拠なしなら同じ3回目を禁止しrouteを変える。
- **H6 mechanical promotion**: 再発するprose ruleはtest/validator/Skill/Harness等へ昇格する。
- **H7 Resolve Operator automatic delegation CANARY**: live Resolveが必要になった時、親Lunaがdriver/lease/GUI/MCP手順を書かずhigh-level objectiveだけを渡し、Operatorが自動で正しいqualified routeを選び、lease、readback、cleanup/recovery、evidence returnまで閉じられる。

今回のLuna Max Coordinatorはユーザー明示方針であり、研究文書の一般的な`Luna executes; Sol decides` preferenceをLuna-only普遍則へ変更する試験ではない。

## 2. Trial invariants

このtrialは次を変更できない。

- G01–G14 / product Done / no-save / no-main-merge / processing preservation
- parent Resolve MCP visibility 0というcurrent isolation intent
- user-wide exclusive Resolve lease
- Resolve Operatorのqualified capability boundary
- missing host evidenceをPASSへ昇格しないこと

研究のために余分なhost mutation、Sol呼出し、人間操作、fake retryを作らない。

## 3. Worker package / Evidence Packet

Worker package:

```text
Task: <single coherent outcome>
Owned: <files/subsystem/worktree or host lane>
Read/Start: <1-4 authoritative refs>
Do: <necessary actions>
Do not: <task-specific boundaries>
Validation: <observable checks>
Return: <Evidence Packet>
```

Evidence Packet:

```text
TASK
STATE
CHANGED
VERIFIED
TESTS
HOST_EVIDENCE
REMAINING
BLOCKER
FAILURE_FINGERPRINT
ATTEMPT_COUNT
NEXT_DECISION
```

## 4. Resolve Operator CANARY package — first live-host package

このtrialでは、旧RNK checkpointのsame-session tool visibility修復を親Lunaの仕事にしない。current external Resolve Operatorを代表taskで呼ぶ。

```text
Task:
Resolve Operatorへ委譲し、current RNK candidateのSO-11 host preflightをread-onlyで実行する。

Parent envelope:
objective: "current RNK candidateのstrict host qualificationを開始できるよう、current Resolve runtime/targetと必要snapshot capabilityをinventoryする"
target:
  project: "current valuable targetはinventoryで確定。暗黙の旧project名へbindしない"
  timeline: "current-policy"
  comp: "current-policy"
done:
  - "exact Resolve version/edition/process identityがreadbackされる"
  - "project/timeline/comp target identityがreadbackされる"
  - "SO-11に必要なread-only processing/port snapshot capabilityの可否が判定される"
  - "graph/project mutation=0、project save=0"
restore_policy: "restore"
evidence:
  - resolve_version
  - driver_identity
  - lease
  - target_identity
  - capability_inventory
  - independent_readback
  - final_state
```

親Lunaはdriverを指定しない。Operatorがcurrent qualified surfaceからnative MCP / compatibility MCP / scripting / GUIを選ぶ。launcher、lease、quit/restart、MCP reconnect、readback、cleanupはOperator内部手順。

Operatorが`BUSY`なら親はhostへ迂回せずoffline ready workを進める。`BLOCKED` / `INTEGRATION_GAP`なら`routing / launcher / lease / driver / capability / restore / evidence`のどこで止まったかをEvidence Packetとして受け、Operator package側のrepair候補へ送る。

## 5. Automatic delegation promotion test

CANARYで記録する。

- parent promptにResolve実装手順が何行入ったか
- Operatorがon-demandで起動したか
- parent Resolve tool visibilityが0のままか
- selected driverと、その選択がqualified surface内か
- exclusive lease acquire/final state
- independent readback
- cleanup/recovery
- user confirmation count
- parent direct-host fallback count（期待0）
- structured evidence completeness
- product gate movement

Representative real taskで安定して成立すれば、trial resultでdurable routingへの昇格候補を提案する。昇格先は長いtask promptではなくglobal/repo AGENTSの短いrouting、Resolve Operator Skill、launcher/Harness等を優先する。

一回の失敗で方式を廃止しない。まずfailureを`routing / launcher / lease / driver / capability / restore / evidence`へ分類し、Operator procedure/script/Skill/Harnessを修復する。修復後に同じsemantic taskで再qualificationする。親が直接Resolveへ入る恒久fallbackは禁止。

## 6. General trial instrumentation

各meaningful Work Packageで取得可能なら記録する。

- package id / goal
- Coordinator / Worker / Verifier model+context IDs
- top-level prompt size
- references count
- Work Package size
- Evidence Packet size
- wall time
- changed files
- tests/host result
- failure fingerprint / attempt count
- escalation: none / changed-route-Luna / Sol-diagnostic / Resolve-Operator-repair / human
- human intervention count
- meaningful new evidence yes/no
- resulting product task/gate movement

計測不能は`NOT_COLLECTED`。

最低sampleは、missionが続くなら (1) Resolve Operator/SO-11 host package、(2) product integration package、(3) independent verification/host qualification package。完成/真の停止が先ならfake workを作らない。

## 7. Failure escalation

semantic fingerprintで数える。`OPERATOR_ROUTING_MISSING`、`OPERATOR_LAUNCH_FAIL`、`LEASE_BUSY`、`DRIVER_CAPABILITY_GAP`、`RESTORE_UNQUALIFIED`、`EVIDENCE_INCOMPLETE`、`HOST_GETTER_TIMEOUT`は別fingerprint。

- attempt 1: Luna/Operatorの通常repair
- attempt 2: materially different distinguishing probe/route、新しいevidence expectationを明示
- same fingerprint x2 + no new evidence: 同じ3回目は禁止
- Resolve固有問題ならまずOperator package側のrepairへ
- architecture/acceptance ambiguityが残り、authorized Sol diagnostic laneが有効なら一回のbounded diagnosisを使ってよい
- 実装/検証はLunaへ戻す。escalationをstickyにしない

## 8. Trial result / Learning Gate

meaningful milestoneまたはmission closeで`PROMPT_ORCHESTRATION_TRIAL_RESULT.{md,json}`を作る。

最低項目:
- exact research source: `CODEX_PROMPT_ORCHESTRATION_RESEARCH_2026-08-28.md`
- Resolve Operator package authority revision
- Work Package/Evidence Packet sample
- automatic delegation CANARY result
- routing/driver/lease/readback/cleanup/restart evidence coverage
- same-fingerprint retry/route change
- Sol diagnostic count/usefulness
- human interventions
- product gate movement
- false completion/duplicate work incidents
- NOT_COLLECTED
- source-supported conclusion vs RNK-specific inference

一案件から因果を一般化しない。Mandatory Learning Gateを実施し、verified reusable deltaは既存CodexOperations/Resolve Operator ownerまたは機械的guardへ昇格する。再利用deltaがなければ`NO_REUSABLE_DELTA`。
