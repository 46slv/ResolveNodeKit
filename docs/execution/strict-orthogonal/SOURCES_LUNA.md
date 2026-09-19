# Luna continuation の根拠・適用範囲

確認日: 2026-09-10 / LM-TAKEOVER-20260910-2 / RO-CANARY-20260910-1

## 2026-09-11 routing amendment

The source below is historical canary evidence. It does not require external
Resolve Operator delegation for every new task. The current repository contract
is the Requirements-first D/S/H overlay; the external Operator remains the
rollback baseline and a per-task specialist option. See
`README.md`, `PLAN.md`, `RUNBOOK.md`, and
`checkpoints/2026-09-11-requirements-first-topology.json`.

## Primary Library source now found

今回、ユーザー指定のexact sourceをChatGPT Libraryから取得できた。

`/AI Operating Context/Coding Intelligence/CODEX_PROMPT_ORCHESTRATION_RESEARCH_2026-08-28.md`

Relevant current additions:

- short task contract / durable repo knowledge / bounded delegation
- Luna execution + evidence-aware non-sticky escalation
- `Resolve Operator automatic delegation (2026-09-10)` — `PROVISIONAL / CANARY`
- parentはResolveのhigh-level objective / target / Done / restore expectation / required evidenceだけを渡す
- Resolve Operatorがinventory、exclusive lease、driver selection、launch/quit/restart、operation、independent readback、cleanup/recovery、final readback、lease release、structured evidence returnを所有
- Operator内部でBlackmagic native MCP、qualified compatibility MCP、scripting、GUIをcurrent qualified capabilityに応じて選択
- failureは`routing / launcher / lease / driver / capability / restore / evidence`へ分類し、Operator procedure/script/Skill/Harnessを修復して同じsemantic taskで再qualification
- 親Agentのdirect Resolve accessを恒久fallbackにしない

このsourceはCANARYであり、まだglobal durable defaultへ昇格済みとは扱わない。RNKは代表実タスクとして有効性を測る。

## Resolve domain / package authority

Library `DAVINCI_RESOLVE.md` と `CODEX_AGENTS_DESIGN.md` のcurrent sections、およびGitHub `46slv/CodexOperations` PR #5を照合した。

Shared package authority at check time:

- repo: `46slv/CodexOperations`
- PR: #5 OPEN/Draft
- branch: `docs/resolve-operator-package-20260908`
- head: `9958e78e382ba5a312cd0a6cc4887aaab2fe4a08`
- `FIRST_USABLE: PASS`
- `FULL_QUALIFICATION: PARTIAL_PASS`

Qualified high-level boundary:

```text
Orchestrator / Agent
 -> Resolve Operator
 -> exclusive lease
 -> capability router
 -> Blackmagic native MCP / qualified compatibility MCP / scripting / GUI
 -> Resolve
```

Current shared evidence includes parent Resolve MCP visibility 0、external Operator、native/compatibility driver routing、lease/no-steal/race/stale recovery、high-level orchestration E2E、independent readback、owned cleanup、restart/reconnect、structured result return。

Codex 0.153.4では`global MCP disabled + same-session child role enables MCP`をcurrent isolation designにしない。role/Skill/modelがloadしてもrole-local MCP startの証拠にならない。worker-only Resolve capabilityはexternal worker/runtimeへ分離する。

## Current bounded limitations

- pre-existing unsaved/default `Untitled Project` はdisplay name/empty structure相当へ戻せてもunique project ID exact restorationが未qualified
- Deliver current-settings inspectionはcompatibility APIにgap
- broad native-primary promotionはworkflow-scoped
- native/compatibility tool countだけでcapability parityを推測しない

したがってRNK側はdriverを指定せず、Operatorのqualified routingへ任せる。stable saved/scratch・qualified surfaceではnative-first候補、未qualified/guarded workflowではcompatibility等のfallbackをOperatorが選択できる。

## RNK repository state at correction

RNKでは過去checkpointに`resolve_operator`がleaseを取得しても`davinci-resolve` callable surfaceが見えなかった証拠がある。これは当時のRNK実行経路には正しいが、current external Resolve Operator packageの能力不存在を示さない。

そのため2026-09-10 correctionでは、RNK parent Lunaがchild MCP visibilityを直接修復する手順を外し、current external Resolve Operatorへのhigh-level delegationへ変更した。

Product requirementsは変更していない。SO-10/SO-20/SO-30のoffline成果、G01–G14、strict/flatten/1100+/UI/processing/Undo/performance gatesはそのまま。

## Other Library rules retained

- `CODEX_PROJECT_CONTINUATION_WORKFLOW.md`: live stateを読み、遠い工程をpromptへ固定しすぎない
- `CODEX_ORCHESTRATION.md`: Coordinator/Worker context separation、coherent Goal、bounded evidence
- `CODEX_LUNA_FIRST_OPERATIONS.md`: Lunaをroutine workへ、escalationはcondition/evidence based
- `CODEX_REVIEW_EVAL_LOOP.md`: fresh verifier / execution evidence
- `AUTOMATIC_KNOWLEDGE_CAPTURE.md`: verified reusable deltaをowner/test/guardへ昇格
- `CODEX_OPERATIONS_INDEX.md`: AGENTSはmapでありmanualにしない

今回のLuna Max Coordinatorはユーザー明示のproject-specific routing。Libraryが普遍的にLuna Max Coordinatorを要求しているとは主張しない。
