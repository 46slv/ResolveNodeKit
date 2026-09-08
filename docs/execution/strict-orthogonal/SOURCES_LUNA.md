# Luna continuation の根拠・適用範囲

確認日: 2026-09-08 / LM-TAKEOVER-20260908-1

## 取得範囲

ChatGPT Libraryの限定検索で、root INDEX、Coding Intelligence INDEX、CODEX_OPERATIONS_INDEXから必要な関連本文を取得した。このセッションのFilesは検索を提供するが、full-document read/mclickを公開していない。以下は取得できた該当節に基づき、全文読了やLibrary mirror更新を主張しない。repoの現在状態はLibraryから推測せず、GitHubのexact revisionを確認した。

## Library由来

保存先は原則 `/AI Operating Context/Coding Intelligence/`。日付は本文version、volatileなモデル/価格/APIの現在性を保証する日付ではない。

| 文書 / 本文version | 使用した節と取り込む規則 |
|---|---|
| CODEX_PROJECT_CONTINUATION_WORKFLOW.md / 2026-09-06 | 一括継続計画、役割/置き場所、短い起動指示、非Goal。live→契約→監査→Git/readback、計画作成とruntime開始は別 |
| CODEX_ORCHESTRATION.md / 2026-09-05 | Worker lane、Two-task minimum、Goal over rigid micro-state、Workspace、Retry。Coordinator/Workerは別contextで同じmodel可。coherent成果単位で次Goalへ |
| CODEX_LUNA_FIRST_OPERATIONS.md / 2026-08-21 | Default Luna jobs、Escalate by condition、Keep Luna effective。小さい実装境界・compact evidence・measured no-progressでのみ診断変更 |
| CODEX_PROMPT_AUTHORING_LUNA_FIRST_REFERENCE.md / 2026-08-28 | Default prompt architecture、Work Package、Evidence Packet、anti-pattern。固定規則をpromptへ重複せずbounded委譲 |
| CODEX_PROMPT_ARCHITECTURE.md / 2026-09-06 | Six-field mission、FIRST_USABLE。実入口と観測結果をDoneへ入れ、test greenだけで使用可能にしない |
| MUSE_LONGRUN_AUTONOMOUS_ORCHESTRATION_PATTERN.md / 2026-09-05の該当節 | Core loop、parallel/serial、context rollover、retry、completion。名前はMuseでも必要なのはstate/evidence中心のモデル非依存手順。Museを今回必須にしない |
| CODEX_REVIEW_EVAL_LOOP.md / 2026-08-21 | Evidence hierarchy、Review topology/target。fresh別contextと実行証拠、Verifier自身の修正を避ける |
| CODEX_AGENTS_DESIGN.md / 2026-09-08追補 | dedicated capability agent、Exclusive host lease。parent tool isolation、user-wide mutex、PID+creation identity、same-token restart |
| DAVINCI_RESOLVE.md / 2026-09-08追補 | Operator恒常権限・排他、MCP readiness注意。全live操作を専任lease内、単一runtime flagだけに依存しない |
| AUTOMATIC_KNOWLEDGE_CAPTURE.md / 2026-08-25 | Mandatory Learning Gate。raw logでなくowner/test/guardへverified deltaを保存 |

旧Luna-first資料のlow/medium既定やSol Coordinator推奨は、今回のLuna Max新規Coordinatorの明示要求で限定上書きする。Libraryが元々すべてLuna Max運用を強制していたとは書かない。Sep3のPSD2Fusion用Luna Max multi-cycle案は設計例として参照し、そのHarness/Manager層がRNKで実装済みとは扱わない。

## GitHubの現在地

作成時にPR #5、AGENTS、CURRENT_STATE、RUNBOOK §9、acceptance、SO-20 checkpointをreadした。sourceはpublication `2d54eaf68a0f0dd9807dbe26ec271d44773a3759` / product `d7a1610726171c08ad5617c55e4cc04def786a6b`。

[SO-20証拠](../../checkpoints/2026-09-08-luna-so20-offline.json)は146/146 reportedとoffline plannerを記録。Operatorはleaseを取得/解放済みだがMCP surface unavailableでResolve calls=0。以前の74a497f/8c667e6や136testsへ巻き戻して設計しない。

この文書作成中にWindows、実効model、lease、installed package、Resolveは確認/変更していない。remote記事・自己申告だけで現ローカル実機を認証済みにしない。

## 公式資料で追加確認した範囲

- OpenAI GPT-5.6 Luna model page: reasoning effortにmaxがある。ユーザーの選んだCodex実行面で使えることは別途metadata/help確認が必要。 https://developers.openai.com/api/docs/models/gpt-5.6-luna
- Codex subagents / AGENTSガイド: roleと設定の所在を確認する補助。自動的なchild設定継承・MCP可視性・現在のWindows接続を保証しない。 https://developers.openai.com/codex/subagents/ 、https://developers.openai.com/codex/guides/agents-md/

本手順は公式の固定Luna orchestration方式ではない。今回の要求をLibraryの役割分離/少量prompt/証拠中心の規則へ当てはめたローカル運用契約である。新規task takeover、旧期限の限定、MCP未公開の診断順序、既存Operator維持は今回の状態に対する具体化。

## 保存直前の並行変更

追加readでheadが`dd0069abde35526b8164beae2c5753b95a1e12af`へ進んでいた。2d54eaf以降のhost-recheck、acceptance差分、view_realization.py、exports/testsを比較し、すべて新baseに残して文書だけを重ねる。06:01 UTCのhost-recheckでもMCP未公開・0calls。146/146はd7a1610の報告で、後続コードの再試験結果はここでは主張しない。

続く`853c6b18596559d7e6dd6ea3a18662b24a471e77`でSO-30 checkpointを実取得した。dd0069aの158/158 reported、12 focused、G03 host未達を確認。稼働中Coordinatorの更新を守るため、今回CURRENT_STATE/acceptance/旧receiptとPR本文は書き換えず、既存入口READMEと追加手順・policy・authoring記録だけをpublishする。
