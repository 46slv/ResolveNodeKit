# Strict Orthogonal Arrange — Astra → Sol continuation

Updated: 2026-09-08 JST / AS-HANDOFF-1  
Program: RNK-STRICT-ORTHOGONAL  
Plan: READY_FOR_RUNTIME_PREFLIGHT  
Runtime handoff / product execution: NOT_STARTED_BY_THIS_PUBLICATION

## Goalと変えない完成条件

参考資料の水平主列・縦枝・上部region・実topologyに沿う右側reduction・余白を再構成し、実配線も水平垂直にする。whole-comp preserveと非空nested Groupの全解除を、実データおよび1100+ original non-Group toolsで実証する。処理保存、Undo、run2=0、実UIと同一runのbusy/result、性能・復旧・cleanupは必須のまま。

## 入口と責任

Astraで初期計画・実行可能性の差分監査 → 独立Solが受領 → 単独実行所有権と最初の着手を確認 → Astra初期担当終了。以後はSolだけが進行管理し、Astraは限定Advisor。手順と二重起動対策の正本は[HANDOFF.md](HANDOFF.md)。計画保存だけで引き継ぎDoneにしない。

新しいAstraはlive Git → AGENTS → CURRENT_STATE → HANDOFFを読み、[DESIGN](../../design/strict-orthogonal/DESIGN.md)、[SOURCES](../../design/strict-orthogonal/SOURCES.md)、[PLAN](PLAN.md)、[RUNBOOK](RUNBOOK.md)、[acceptance.json](acceptance.json)を必要箇所から点検する。Solは同じ契約をexact revisionで受領する。過去会話やLibraryを実行時の必須入力にしない。

Repo: 46slv/ResolveNodeKit。統合正本はPR #5の`feat/semantic-arrange-v1-20260906`。元設計publicationは`dc074981bc01d1df618c2dc09cc703f58b7bf164`。実行時はremote HEAD/local worktree/installed sourceをfresh-readし、旧`feat/arrange-uia-e2e-20260906`の変更を保全する。既存Sol ownerがいる場合はamendment受領で継続し、新Coordinatorを二重起動しない。

## 実行原則

SolはGoal・Done・権限を変えない範囲でtaskを追加/分割/並べ替えできる。通常修正や次工程をAstra返答待ちにしない。Workerは分離context、fresh Verifierは修正しない、shared writerとResolve操作担当は各一人。既存のSkills/Harnessを使い、新規汎用orchestrator構築を前提にしない。

旧SAV1の任意扱い・繰り返しblocker・当然のhuman smoke待ちより、このscopeの最新契約を優先する。独立したready workを進め、checkpointやWorker完了で全programを止めない。要件を削ってHumanNeed=NOにしない。認証・費用・保全不能なデータ・所有権等の真の境界だけ人間へ上げる。技術未達は完成ではない。

## 最小起動指示 — Astraへ

```text
ResolveNodeKit PR #5をAstra Bootstrapとして継続する。
Start: live repoとAGENTSを確認し、docs/execution/strict-orthogonal/README.mdから最新契約を読む。
Goal: 既存設計を差分監査し、Solへ完成までの実行管理を引き継ぐ。
Done: HANDOFF.mdに従い、Solの実効設定・計画受領・単独所有・最初の着手を証拠で確認して初期担当を閉じる。その後はAdvisorのみ。
Authority: RUNBOOKの範囲で自律実行。Resolveの全面操作・スクリプト実行・起動・終了・再起動を事前確認なしで許可する。main merge・project saveは禁止。
Evidence: 計画revision、受領/所有/着手証拠、製品gate状態。起動不明時に二重作成せず、未実行を引き継ぎ完了としない。
```

Solへの短いpacketは、実行時に確定したhandoff_id、repo/cwd、plan revision、最初のtask、検証入口、HANDOFF/RUNBOOK参照だけを中心に作る。表の全工程や過去failureをpromptへ再掲しない。

## 完了状態

BOOTSTRAP_DONEとSTRICT_LAYOUT_RELEASE_CANDIDATEは別。後者は全G01–G14の実証とfresh Verifierが必要。main未merge、広いResolveNodeKit全体のMISSION_COMPLETEとは別。今回の公開は資料と契約検査のみで、Sol/Resolveは起動していない。
