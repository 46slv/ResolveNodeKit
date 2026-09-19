# Astra → Sol 引き継ぎ・Advisor契約

Revision: AS-HANDOFF-1 / 2026-09-08 JST  
Applies to: RNK-STRICT-ORTHOGONAL / ResolveNodeKit PR #5  
Status: ADOPTED_FOR_THIS_PLAN / LIVE_HANDOFF_NOT_RUN

## 1. 今回の採用範囲

ユーザー提供の「Astraで起動・計画、Solが継続実行、Astraは必要時Advisor」を、この既存missionへ採用する。モデルの一般的な優劣、全repoの恒久routing、未確認の実機能力を示すものではない。DESIGNのstrict配置・参考profile・1100+全Group解除・処理保存・Undo・実UIのDoneは変更しない。

Astraの初期Doneは「実行可能な計画を保存し、Solの受領・単独所有・最初の着手を確認した」。資料作成完了、thread作成、製品完成とはそれぞれ別である。Sol受領後、Astraを常時監督者として残さない。

## 2. 責任と保存先

| 担当 | 所有する仕事 | 所有しない仕事 |
|---|---|---|
| Astra / Bootstrap | fresh repo・Goal・Done・主要設計・実行可能性・重要前提の限定probe、計画保存、引き継ぎ成立確認 | 全製品の実装完了、受領後の通常queue管理 |
| Sol / Coordinator | 受領後の唯一の実行queue/state/integration writer、Worker選択、局所計画修正、復旧、検証・統合、次工程 | ユーザーのDone/権限の変更、Worker自己申告の無検証採用 |
| Astra / Advisor | 個別相談に対する判断案・根拠・不確実性・最小の反証試験 | 共有state書込、Workerへの直接指示、Solのlease取得、自動的な必須要件削除 |
| Worker / Verifier | Workerは限定task実装、Verifierは別contextでexact candidateを独立検証 | Workerの上位Goal変更、Verifier自身による候補修正と自己承認 |

AGENTSは恒久境界と入口。DESIGNは製品契約。PLANは到達点と依存。RUNBOOKは実行権限と復旧。本書は引き継ぎ/相談手順。acceptance.jsonのhandoff_stateは最新転送状態、既存checkpointsはimmutable receipt/evidence。実効model/effort/cwd/権限と起動syntaxは既存Harness/role設定をlive確認する。新しい設定・手順を全ファイルへ複製しない。

## 3. Astraの初期工程

**AP-10 現在地と実行面**: 正しいGit root、remote/branch/worktree、未commit差分、現在の候補/installed差、既存runとhost所有者を確認する。古いローカルpathはlocatorとして探索し、実在確認した絶対pathを受渡す。実行中のSolが同missionを所有しているなら、新規Solを二重起動せず§6の既存owner引き継ぎへ進む。

**AP-20 計画の成立性**: 既存設計を全面的に考え直さず差分監査する。重要前提は、snapshot完全性、native直交表示、非空nestedの解除/復元、実UIイベント、独立Sol起動/再開。既存の適用可能な証拠を先に使い、未確認の前提だけ限定probeする。各前提に観測・confidence・適用host/context・未解消時の最初のtaskを付ける。原JSONの欠落を推測で埋めない。

全APIを解明するまで計画段階に留まらない。限定probeで未確定なら、調査/実装/代替の分岐と依存を具体化してSolへ渡せる。ただし「実装方法未確認」と「実行タスク自体を起動/受領確認できない」は別。後者は引き継ぎ完了にできない。技術的未確定がある計画のREADYは、製品実現性が全証明されたという意味ではない。

**AP-30 保存・点検**: 直近taskは具体的、遠い工程は成果とDone中心にする。書込済み計画のrevisionとfile hashes、candidate、既存証拠、未解決前提、最初のready taskと検証入口を固定する。AGENTSを毎回書き直さず、恒久ルール変更が必要なときだけ変更する。repoへcommit/push/readbackし、SolがLibraryや設計会話全文を読めなくても着手できることを点検する。

**AP-40 受領・所有移行・着手確認**: 以下のprotocolを実行する。これが成立してからAstraの初期担当を終了し、以後はAdvisorへ移る。現在の資料公開はAP-40実行済みを意味しない。

## 4. 受け渡しprotocol

次の名前は本projectの正規化状態であり、Codex APIの公式field名ではない。adapterは現行Harnessが実際に返したevent/metadataを証拠として紐付ける。

| State | 必要な観測 | 共有writer |
|---|---|---|
| PLAN_READY | 保存/readback済み計画、exact candidateとdirty状態、最初のtask、未解決前提、起動契約 | 初期担当 |
| LAUNCH_REQUESTED | 一意handoff_id、期待するrepo/cwd/model/effort/権限、既存起動照会結果、launch request ID | 初期担当 |
| THREAD_CREATED | 独立したpersisted Sol thread IDと実作成event。Astra終了で消える子processだけでは不可 | 初期担当 |
| TURN_STARTED | 同threadの実turn開始event。thread作成だけでは不可 | 初期担当 |
| RECEIPT_VERIFIED | Solのread-only受領とmetadataが期待値に一致し、Goal・計画hash・最初のtask・検証入口を確認 | 初期担当 |
| OWNERSHIP_TRANSFERRED | 旧owner/epochを照合してSolへ一度だけ移管、Solが新leaseをreadback | Solのみ |
| EXECUTION_CONFIRMED | 移管後のSolが最初のbounded taskまたはWorker委譲を実際に開始したevent | Solのみ |

受領turn中のSolは共有state/製品/hostを変更しない。immutable receiptのみ返し、lease付与を待つ。初期担当または既存Harnessのsingle-writerがcompare-and-setで移管し、その後Solへ継続を通知する。Solは同じthreadで実行を開始する。Astraは移管後read-onlyで着手証拠を確認して初期Doneを報告する。確認のためAstraが再びCURRENT_STATEを書き換える必要はない。

Harnessのatomic owner/lease機構を優先する。無ければ最小のexclusive lock＋revision確認で同等の排他を作る。Gitへのpush単独はhost/process間の排他を保証しない。ロック/epochはcredentialではなく競合検出であり、実権限を拡張しない。

### 受領記録の必須情報

handoff_id、expected/observed bindings、AstraとSolのthread/context ID、実model/effort、実cwd/Git identity、branch、source revision/dirty fingerprint、plan digest、instruction manifest、権限digest、最初のtask/検証入口、作成/開始/受領event refs、所有権epoch/新owner確認、着手event refsを記録する。role名にSolと書いたpromptはmodel証明ではない。instructionSourcesが使える場合は実返却値を取り、無ければsupportedな指示読込証拠と明示的file readbackを記録する。未確認なら未確認のまま。

plan digestはDESIGN/PLAN/RUNBOOK/README/HANDOFFおよびacceptanceの規範部分を対象にし、mutable state・自身のdigest・receipt・publication commitは対象外にする。product sourceとplan/publicationのrevisionを分離する。動的stateの一行更新で全試験をやり直さず、Done/権限/指示変更は再受領させる。

### 既存Solへの計画追補

上表はmode=NEW_OWNERの場合。mode=AMEND_EXISTINGでは、Astraは現Solからwriter権限を取り戻さない。Solが現作業を安全なcheckpointへ置き、同じthreadで変更planをread-only検討/受領し、唯一のwriterとして自身のepoch/revisionを一度進める。旧epochを失効させ、新epochで作業再開を記録する。既存threadの作成証拠を再利用し、今回のturn/receipt/再開証拠は新しく結び付ける。既存の製品task状態・candidate・証拠を初期化しない。

このmodeのprevious_ownerとownerはともに現Solであり、NEW_OWNERだけprevious_ownerが初期担当になる。Astraは追補の受領/再開をreadbackして初期Doneを閉じる。新しいCoordinatorを作るための例外ではない。

## 5. 実行基盤と起動方法

既存のrepo-local Skills、Codex/Dev Exec等の許可済み起動・再開・永続化機構を優先する。未接続runtimeの導入、汎用orchestrator新築、EPHEMERAのテスト専用canary流用は本missionの前提にしない。

Codex App Serverを使う場合、公式資料ではthread/startとturn/startは別操作であり、cwd/modelを指定したthread生成、threadのread/resume、instructionSourcesの返却が案内されている。これは利用候補の契約で、ローカル導入版/公開toolが使える証拠ではない。actual schema/helpを読み、対応しないmethod/flagを推測しない。独立寿命、永続thread、復旧可能性、実効権限を確認する。

起動surfaceが無ければ計画はPLAN_READY / handoffはBLOCKED_RUNTIMEとし、launchを成功扱いにしない。別の既存許可routeがあるなら切替える。どうしても人間が必要なら、その起動だけを一度依頼し、以後の検証クリック待ちとは切り分ける。今回の資料更新自体はlocal runを起動しない。

## 6. 重複・中断・古い状態の復旧

| 状況 | 対応 |
|---|---|
| 作成/開始がtimeoutして結果不明 | handoff_idと記録済みthread/request IDで照会。実行が存在しない証拠がない限り二重create/turn開始禁止 |
| thread作成済み、turn未開始 | 正しい既存threadへ一度だけturn開始。新threadを作り直さない |
| receipt不一致 | 誤ったrepo/model/planのthreadにwrite leaseを与えない。supportedな修正/再開で確認し直す |
| 所有移管直後にAstra停止 | durable ownerがSolならSolが続行。Astra終了報告がないことを理由に新Coordinatorを作らない |
| Sol停止/429/context不足 | 同一persisted thread/checkpointを照会し、許可済み予算内でbackoff/resume。復帰不能時だけ後継threadへ同じreceipt/lease手順。旧ownerをfenceする |
| 同missionのSolが既に実行中 | active leaseを尊重し、今回のamendmentをbounded requestで渡す。Solのrevision受領と次の実行を確認。既存phase/証拠をリセットしない |
| 計画/AGENTS更新 | 計画だけならexact revisionを明示read/ack。実効instruction chain変更なら現runtimeのreload/resume/new-session挙動を確認し、自動反映を仮定しない |
| lease期限経過 | 期限切れだけで旧writerが停止したとは判断しない。process/thread/未完host operationを照合してから引き継ぐ |

## 7. Solの裁量とAstra Advisor

Goal、必須G01–G14、処理/データ安全、権限が不変なら、Solはtask追加・分割・順序変更・実装方式の選択を理由付きで行える。通常テスト失敗・軽い修正・次task選択をAstra承認待ちにしない。必須結果を維持したtask再編はPLAN/acceptanceの対応を更新し、元のtask/証拠とのmappingを残す。

Astra相談triggerは、設計前提の反証、異なる妥当な試行でも新証拠が得られない停滞、重大な証拠矛盾、必要な上位設計修正に限定する。同じfailureを回数だけ数えて相談/停止しない。相談中も依存しないready workは続行する。

相談packetは、consult_id、Goal/不変制約、candidate/plan refs、観測と実施済み試行、残る仮説、判断してほしい一点、候補案と最小検証、必要な期限/既存予算。raw全会話を渡さない。Astraの返却は、結論案、根拠、未確定前提、反証試験、影響するgate、権限内/外の区別。Astraは共有queueを編集しない。

Solがadopt/reject/needs-user-decisionと理由を記録し、採用案をWorkerへ渡す。助言は証拠でも許可でもなく、Worker検証とfresh Verifierを省略できない。Astraが応答しなければ既存evidenceと権限で進められる部分を継続し、危険な変更だけ保留する。設計を変えずに解ける通常問題を全program停止にしない。

このmissionのAstraは必要時の設計Advisorであり、最終製品の自己承認者ではない。最終Verifierは実装/助言の説明を読む前に契約・diff・evidenceから独立判定する。

## 8. 二つのDoneと報告

BOOTSTRAP_DONE: 正しいSolが計画を受領し、唯一の実行所有者になり、最初の作業に着手したと確認できること。HANDOFF_NOT_RUN、THREAD_CREATEDのみ、受領なし、誤model、旧plan、writer二重、着手不明では未達。

PRODUCT_DONE: DESIGNとacceptanceの全必須結果が最終installed candidateで実証され、fresh Verifier、remote readback、host cleanupまで揃うこと。Astra初期Doneでは製品gateをPASSへ変更しない。Solのtask完了でも新missionを勝手に追加しない。

初期報告はPLAN_REVISION / HANDOFF_STATE / SOL_THREAD / RECEIPT / ACTIVE_OWNER / FIRST_TASK / BOOTSTRAP_DONE / PRODUCT_STATUS。製品closeoutは既存RUNBOOKの形式を使う。どちらも実行していない背景継続を約束しない。

## 9. 根拠と今回の追加設計

ユーザー提供文とLibraryのCODEX_PROJECT_CONTINUATION_WORKFLOW、ASTRA_SOL_ORCHESTRATION_RESEARCH_2026-09-08が役割分離・資料配置・受領確認・Advisor限定の根拠。本missionへの採用は今回の明示依頼による。元の比較研究は未検証候補であり、全モデル/全repoの恒久policyへ昇格しない。

receiptの状態名、二段階所有移管、初期状態のschema、反例検査はこのrepo向けの具体化であり、公式の必須protocolとは主張しない。

公式資料確認 2026-09-08: https://developers.openai.com/codex/app-server/ 、https://developers.openai.com/codex/guides/agents-md/ 、https://developers.openai.com/codex/subagents/ 。実効model/effort/権限の継承はruntime設定にも依存する。これらの再確認はローカル起動成功を意味しない。

## 10. 軽量な契約検査

`python docs/execution/strict-orthogonal/check_contract.py`は静的整合を検査する。
`python -m unittest discover -s docs/execution/strict-orthogonal -p test_contract.py`は合成receiptでfalse-Done等を検査する。

これは起動器・権限機構・evidence認証器ではなくread-only guard。trueの自己申告や文字列refの存在だけで実際のruntime eventが証明されることはない。Astra/既存Harnessが参照先の実データと時系列をreadbackすることが受領判定の前提。validatorの結果は明示的にruntime_evidence_authenticated=falseを返す。製品127件の回帰suiteやResolve実機試験とは別である。
