# Resolve Operator routing correction — 2026-09-10

Revision: RO-CANARY-20260910-1

## Why

RNKの旧Luna continuationは、2026-09-08の局所checkpoint `MCP surface unavailable to resolve_operator` を次回の主復旧課題として扱っていた。しかしLibrary/current shared authorityでは、Codex 0.153.4でsame-session child roleへMCPを載せる経路は正規経路ではなく、専用external Resolve Operatorがqualification済み。

Current shared operator authority: `46slv/CodexOperations` PR #5 / `docs/resolve-operator-package-20260908` / `9958e78e382ba5a312cd0a6cc4887aaab2fe4a08`.

Shared result: `FIRST_USABLE: PASS`, `FULL_QUALIFICATION: PARTIAL_PASS`; parent Resolve MCP visibility 0、external Operator、exclusive lease、native/compatibility routing、high-level orchestration E2E、independent readback、cleanup/recovery、restart/reconnectが証拠化されている。

## Correction

Parent Luna MaxはResolve MCP/GUI/scriptの手順を持たない。live Resolveが必要になった時点でResolve Operatorへ次だけを渡す。

- objective
- target/scope
- observable Done
- restore policy
- required evidence

Operatorがinventory -> lease -> driver selection -> operation -> independent readback -> cleanup/recovery -> final readback -> release -> structured evidenceを所有する。

Codex 0.153.4のsame-session role-local MCP enablementを再デバッグしない。parentへMCPを直接有効化しない。native/36-tool/scripting/GUIの選択を親promptへ固定しない。現在のqualified package/launcher自体が欠ける場合は `routing / launcher / lease / driver / capability / restore / evidence` に分類してOperator側を修復する。

## Trial use

`CODEX_PROMPT_ORCHESTRATION_RESEARCH_2026-08-28.md` の `Resolve Operator automatic delegation` は `PROVISIONAL / CANARY`。RNKを代表実タスクとして使い、親のhigh-level依頼からOperatorが余計な確認なしに起動し、正しいrouting、lease、readback、cleanup/recovery、evidence returnまで成立するか測る。

一回の成功だけでglobal durable routingへ昇格しない。失敗一回だけで方式を廃止しない。修復後は同じsemantic taskで再qualificationする。

## Product impact

Docs/routing correction only. G01–G14、product Done、no-save、main未merge、処理保存、strict layout/flatten/1100+ requirementsは変更しない。過去のRNK host checkpointは当時の経路に対する正しい証拠として保持するが、current Operator capabilityの正本にはしない。
