# Strict Orthogonal Arrange — 新規 Luna Max task の入口

Revision: LM-TAKEOVER-20260908-1 + PO-TRIAL-20260910-1  
Authoring: READY_FOR_LOCAL_TAKEOVER / runtime takeover not executed here

## 今回の指示

新しいLuna MaxのCodex taskが、既存ResolveNodeKitの成果と同じPR #5を引き継ぎ、実装・導入・実機検証を進める。AstraでBootstrapをやり直さず、旧Sol threadを再開することを既定にしない。新規taskは新規開発や進捗初期化を意味しない。

最初にlive Git、AGENTS、[CURRENT_STATE](../../CURRENT_STATE.md)、[LUNA_RUNBOOK](LUNA_RUNBOOK.md)を読む。製品のGoal/Doneは[DESIGN](../../design/strict-orthogonal/DESIGN.md)、[PLAN](PLAN.md)、[acceptance.json](acceptance.json)を継続する。

今回の継続は、Libraryのprompt/orchestration研究を実運用で試す[Prompt orchestration trial](PROMPT_ORCHESTRATION_TRIAL.md)も併走する。trialは製品gateより下位で、短いtask prompt、bounded Work Package、compact Evidence Packet、same-fingerprint/no-new-evidence時のroute変更/条件付き非sticky escalationを測る。研究のために余分な失敗・Sol呼出し・人間操作を作らない。

現在の役割・新規所有移行・期限の正本はLUNA_RUNBOOKと[luna_execution.json](luna_execution.json)。旧HANDOFF/RUNBOOK/acceptance.rolesに残るAstra→Sol起動、Sol固定名、旧invocationの11:07:27 JST期限より、この限定変更を優先する。処理保存・専任Operator・排他・no-save・main未merge・G01–G14は緩和しない。

## 取り戻す現在地

保存直前に確認したpublicationは`853c6b18596559d7e6dd6ea3a18662b24a471e77`、productは`dd0069abde35526b8164beae2c5753b95a1e12af`。SO-10/SO-20はoffline PASS、SO-30もoffline契約の成果あり、158/158 reported。ただしG02/G03のhost部分は未証明。これらはlocatorであり起動時のlive refが優先。

最新host記録は「専任Operatorがleaseを取得・解放したが、MCP callable surfaceがなかった」。単なるFREE待ちやResolve再起動から始めない。具体的な分岐はLUNA_RUNBOOK §4。trialの最初のbounded Work PackageもこのOperator経路のread-only復旧証明である。

## 新規Luna Max taskへ渡す短い指示

```text
ResolveNodeKit PR #5を、新規Luna Max Coordinatorとして引き継いで進める。
Goal: 既存strict配置・1100個以上・全Group解除の完成条件まで実装と実機検証を進める。
Done: G01–G14を最終candidateで実証し、install/host/PR/cleanupを整合。未達を削らない。
Constraints: 旧task/未完operationを照合して正規takeover。live Resolveは専任resolve_operatorのみ。project save・main merge禁止。
Start: live GitとAGENTS、docs/execution/strict-orthogonal/README.md、LUNA_RUNBOOK.md、PROMPT_ORCHESTRATION_TRIAL.mdを読む。既存SO-10/SO-20/SO-30 offline成果を再実装しない。
Evidence: bounded Work Package→compact Evidence Packetで進め、same failure fingerprintが2回かつ新証拠なしなら同じ3回目を禁止。必要時だけ非stickyな診断escalation。製品証拠とtrial計測を分離して保存。
Authority: Resolveの全面操作、スクリプト実行、起動、終了、再起動を事前確認なしで許可する。その他はRUNBOOKに従う。
```

今回の公開は手順書のみ。新規task/lease/Resolve操作は開始していない。詳細のLibrary根拠と今回の適用変更は[SOURCES_LUNA](SOURCES_LUNA.md)。
