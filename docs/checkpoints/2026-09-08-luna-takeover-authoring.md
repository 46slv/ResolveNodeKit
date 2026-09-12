# 新規Luna Max continuation — authoring checkpoint

Revision: LM-TAKEOVER-20260908-1 / 2026-09-08 JST

## Request / scope

新規Luna Max taskへの引き継ぎと、Libraryに基づくLunaオーケストレーション/手順書を作成した。今回の変更はこのmissionの実行policyと入口だけ。新規task・lease移管・Resolve操作は未開始。

起草開始時点は2d54eaf/d7a1610、SO-10/SO-20 offline、146/146 reportedだった。保存直前に並行変更をfresh-readし、853c6b18596559d7e6dd6ea3a18662b24a471e77 / product dd0069abde35526b8164beae2c5753b95a1e12af、SO-30 offline契約と158/158 reportedを確認した。G02/G03 hostは未証明。MCP surface unavailable、lease正常取得/解放、Resolve calls=0の区別を保持する。

## Publication / concurrency policy

追加: LUNA_RUNBOOK.md、luna_execution.json、SOURCES_LUNA.mdと本authoring記録。変更: 実行入口README.mdのみ。

稼働中Coordinatorの並行変更を消さないため、CURRENT_STATE/acceptance/旧handoff record/PR本文は上書きしない。新しいheadをbaseに文書差分だけを重ねる。AGENTS、DESIGN、PLAN、RUNBOOK、product src/scripts/tests、installer、global runtime configurationは変更しない。後継taskが実leaseを移管してからmutable stateを更新する。

role/invocationの限定precedenceは新しい入口に明記。歴史的なSol receiptをLuna IDへ偽装しない。新takeoverはNOT_STARTED、ID/epoch/evidenceは空で、製品gateは昇格しない。Group解除、strict表示、1100+、処理保存、Undo、run2、実UIと性能のDoneは維持する。

## Static authoring checks

17項目PASS。policy JSON、新規Luna/max、不要な旧Bootstrapなし、専任Operator/排他、未実施takeover、14必須gate参照、旧期限非継承、no-background claim、main merge/no-save境界、最新offline再開点、MCP公開/lease/endpoint分離、歴史receipt保全、docs-only、Library取得範囲、相対リンク、短い起動指示を検査した。

これは文書/初期policyの静的検査で、製品158件の再実行、Windows runtime認証、Operator qualification、Resolve実機試験ではない。相対リンクは新規ファイルまたはGitHubで確認した既存pathへ解決する。Libraryは検索で取得できた関連本文を根拠とし、full-document展開はtool未提供。今回新しいruntime/host/installedは観測していない。

## Learning captured

新規taskと成果の初期化は別。旧invocationの期限/roleは自動継承しない。FREE、MCP未公開、未接続、host無応答を別fingerprintにする。能力agentの実効modelをCoordinatorと同一に見せるため隔離を崩さない。旧所有者が並行更新する状態文書はtakeover前に上書きしない。改善は今回の具体的な手順へ反映し、新しい汎用orchestratorを作らない。
