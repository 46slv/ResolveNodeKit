# Luna Max オーケストレーションと新規task引き継ぎ

Revision: LM-TAKEOVER-20260908-1 / 2026-09-08 JST  
Mission: RNK-STRICT-ORTHOGONAL / 46slv/ResolveNodeKit / PR #5  
Status: 実行手順を準備済み。所有移行・新規実行は未実施。

## 1. 変える範囲、変えない範囲

現在の明示依頼により、新しいLuna Max Coordinatorが継続実行を引き継ぐ。通常の実装と独立検証もLuna Maxを既定とする。Astra Bootstrapの再実行、Sol常駐管理、Muse/OpenCode経由は前提にしない。既存設計・SO task ID・G01–G14・成果・失敗証拠は保持する。

この文書はモデル役割、新しい実行回、所有移行の旧記述を更新する。旧RUNBOOKの処理保存/権限/復旧は継続し、現行personal resolve_operator Skillの厳しい条件を迂回しない。旧期限2026-09-08 11:07:27 JSTは完了した一回のinvocationだけのもの。本手順を使って開始する新規実行に流用しない。新たな時刻・回数・無期限のbackground稼働は勝手に指定しない。今回の実行面に実在する上限、ユーザーの新しいstop指示には従う。

Goalは引き続き、参考profileに沿う全comp整列、全ノードと実配線の水平垂直、非空nestedを含む全Group解除、実データ規模と元non-Group >=1100の実機試験、処理保存、Undo exact、run2 moved=0、installed UI/同一run busy-result、性能とcleanupである。旧preserve FIRST_USABLEを新しいstrict/flatten完了に読み替えない。

## 2. 役割を最小構成にする

| Lane | 実行者 / 責任 | 書込・受渡し境界 |
|---|---|---|
| Coordinator | 新規Luna Max task。live state、次のcoherent Goal、委譲、統合、証拠判定、復旧を管理 | canonical queue/state/PRの唯一のwriter。実装Workerの作業を横から二重実装しない |
| Worker | 独立Luna Max context。固定された一つの成果を実装し、focused tests→必要な検証→報告 | isolated worktree/pathを所有。勝手に次Goalを決めず、自分で製品Doneにしない |
| Verifier | Workerとは別のLuna Max context。exact candidateを契約・diff・実測から反証的に確認 | 候補を修正しない。FAILはWorkerへ返し、新candidateを別判定 |
| Resolve Operator | personal `resolve_operator`の現在の資格認定済み設定 | live read/write/API/script/GUI/起動/終了/再起動すべての唯一のhost担当。user-wide lease内で実施 |

CoordinatorとWorkerの分離はモデル種類でなくcontextと責任の分離である。通常は一Worker＋順次fresh Verifierで開始し、独立したoffline作業にだけ第二Workerを追加する。host操作は常に一人。parallel実行不可なら順次別contextを使い、並列不足を停止理由にしない。独立context自体がなければ、その未達を記録し自己レビューを独立Verifierと呼ばない。

Luna Maxは実効model familyとreasoning effort=maxをruntime metadataで確認する。公開モデル名や過去のCLI flagをそのまま使わず、導入済みruntimeに対応する設定を選ぶ。prompt内の自己紹介だけでは証明にならない。親がMaxでもchildへ継承したと仮定しない。

Operatorはモデル代替ではなく能力境界である。現在のOperatorが別modelで資格認定済みなら、その事実を記録して既存設定を使う。Luna-onlyに見せるためにglobal agent/MCP/権限を無断改変しない。Operatorのmodel変更が必要なら別の限定qualificationとする。通常のCoordinator/Worker/VerifierはLuna Maxのまま。

強いモデルを既定の相談先・停止解除条件にしない。通常失敗はLunaで修復する。異なる妥当な試行でも意味論や証拠の矛盾が解けなければ、まずfresh Luna diagnosisを使う。Astra/Solへの相談を自動で増やさず、別モデルが本当に必要なときだけ現行許可を確認する。助言者はqueue/owner/Doneを変更できない。

## 3. 新規taskへのtakeover — 一度だけ行う

**読む。** 新task自身のID/実model/cwd、Git common-dir/worktree/HEAD/dirty、remote PR、installed manifest、最新checkpoint、program ownerと未完host operationを照合する。最後に観測された旧ownerはcheckpointの`coordinator_thread_id`から読む。旧名がSolでも、最後のturnはLunaだったのでモデル名からprocessを識別しない。

**保全する。** remoteより進んだlocal commit、未commitファイル、稼働中Worker、実行途中のhost操作を破棄しない。旧taskの正常停止・終了したturn・owned worker停止・保全checkpointを、既存runtimeの観測で確認する。ユーザーが新規taskを希望したことはtakeover方針の許可であって、活動中writerを無条件に消す許可ではない。同missionの旧taskがまだ動いていれば、既存の許可済み管理経路で安全なcheckpoint停止を調整し、その完了を確認する。別missionは止めない。

**一度だけ移管する。** 新taskは旧taskと別のpersisted IDであることを確認する。正しいplan revisionと実効権限を受領し、既存program leaseのcurrent owner/epochを再読取してcompare-and-setで新ownerへ移す。epochを1や2へ決め打ちしない。旧writerを停止/fenceし、新ownerだけが書けることをreadbackする。metadataの書換えだけで実排他を主張しない。Git branchの先送りだけも実排他ではない。

**続行する。** 新ownerが最初のbounded workを実際に開始した記録でtakeover成立。Astra/Solにもう一度受領させる必要はない。takeover記録を作って終わらず、そのまま§5の未達へ進む。

所有者が不明ならcanonical branch/共有state/hostへのwriteを保留する。その間も独立したread-only分析や自身の隔離領域の試験は可能。期限切れleaseだけでstaleと断定せず、process作成時刻・実mutex・unfinished operationを確認する。二重起動の疑いがある場合は照会が先で、new workerを乱発しない。

新規taskは同じproduct lineageを使う。既存branchが別worktreeでcheckout中なら、無理に二重checkoutせず、受け渡された既存worktreeまたは隔離continuation branchからnon-force統合する。canonical PR #5は変えない。source/installed/plan/publicationのrevisionを分け、古いテスト件数やchecksumへ合わせる修正をしない。

### 状態の置き場所

[luna_execution.json](luna_execution.json)は今回の役割と未実施takeover slotだけを持つ。[acceptance.json](acceptance.json)は製品task/gate証拠の正本を継続する。既存`handoff_state`とAstra/Solのreceiptは歴史的な成功記録として保存し、新LunaのIDを`sol_thread_id`へ偽装代入しない。

旧check_contract.pyが確認するAstra→Sol recordは過去の整合検査で、新規Luna所有者の実証ではない。現在の実行権限はactual lease＋新しいtakeover receiptで判断し、製品完了は現candidateの全必須gateで判断する。必要なら実行側がこの区別を保った最小validator拡張を行う。旧receiptを上書きする「テスト修正」は禁止。

新しいplan digestはLUNA_RUNBOOK、入口、DESIGN/PLAN/RUNBOOKとacceptanceの規範部分を含め、mutable state・receipt・自身のdigest・publication SHAは除外する。旧digestをそのまま最新として使わない。

Coordinatorだけがtakeover slotを更新する。記録は新/旧ID、fresh source/plan revision、実効model/effort/権限、旧owner停止証拠、CAS前後epoch、新owner readback、最初の着手証拠への参照。今回のauthoringではすべて未取得のままである。

## 4. 専任Operator経路を復旧する — 最初の重要作業

最新のSO-20記録では、Operatorはleaseを取得/解放したが、`davinci-resolve` MCP callable surfaceが無かった。過去の「FREEなので操作しなかった」とは状況が違う。**排他取得、tool公開、接続、実host応答を別々に判定する。**

| 観測 | 次の操作 | やらないこと |
|---|---|---|
| lease FREE | current Skillの既存wrapperでOperator自身が取得し、token/PID/process-start/HELDを確認 | FREEをホスト故障や人間待ちと決めつけない。JSONだけHELDへ変更しない |
| lease BUSY/HELD by other | 所有者を尊重し、offlineを進めて既存待機規則へ | 他repoのOperatorを停止/横取りしない |
| OperatorにMCPツール自体がない | 実際のchild role binding、model/capability、適用config/Skill、MCP enable/filter、wrapperのtool列挙を照合。現在のschemaで誤ったsession設定を直し、新しい専任Operatorへ再bind | parentへMCPを直接有効化しない。別host-access汎用Workerを作らない。Resolve再起動だけでtool公開が直ったとしない |
| ツールはあるが未接続 | 認可済みserver/wrapper processとtransportを診断・復旧し、同じOperator内で再接続 | 認証/接続許可が必要と分かれば迂回しない |
| ツール経路が不足 | current Operator Skillが明示的に認めるAPI/Python/Lua等の経路があれば、同じOperator・lease内で選び、その実routeを証拠化 | parentからの直接script実行、旧Museルートへの無断切替、Skill制限の回避をしない |
| 接続後getterが応答しない | 実行中operationを確認し、既存bounded recoveryに従う。必要時にexact Resolve/fuscript再起動 | timeout後のwrite再送、同じfailureの無意味な連打をしない |

config修正は現在のtask-local/agent-localで許された最小範囲に限定する。global Operatorの信頼境界を変更しなければ直せない場合は、その必要性と影響を分ける。MCP unavailableを製品API unavailableにすり替えない。

最初の成功host callは短いread-only identity。実project/timeline/comp、PID/開始identity、応答を確認する。古い967 tools・project名だけでtargetを決めない。`runtime_mode`等の単一flagだけでreadyを決めず、actual getter/readbackとprocess証拠を使う。全live read/write/GUI/restartをlease内で実施し、restartのquit→launchの間も同じleaseを保持する。

Operatorが失敗しても、scopeを絞ったadapter作成、snapshot fixture、plannerのproduction結線のoffline検証、UI event glueのoffline検証は継続できる。host必要部分は未証明のまま残す。

## 5. 進行ルート — 完了済みを捨てない

作成時点のSO-10/SO-20はoffline PASS。G02はhost分がBLOCKED_TECHNICALである。146/146はそのcandidateの報告で、今のWindowsやinstallに再現した証拠ではない。起動時は最新checkpointへ更新する。

| 次のまとまり | 進める内容 | 判定・対応する既存task |
|---|---|---|
| R0 受け取り | §3のtakeoverとcanonical import元確認 | 新規taskは成立、旧writer不在。製品gateは昇格しない |
| R1 host経路＋並行offline | §4のOperator tool公開/接続、完全snapshot adapter、strict_plannerとcontrollerの結線、UI event glue | SO-00のoffline/host部分を区別。SO-11、SO-50へ進む。SO-20を一から作り直さない |
| R2 strict preserveを実機で通す | 小さな非空nested comp、全port snapshot→strict plan→view適用→readback。native直交表示と実UI Run/Cancel/busy/resultを同じcandidateで検証 | SO-11/30/50→SO-60。先に小さなend-to-endを一つ通す |
| R3 実flattenを閉じる | 測定根拠のあるnative操作、非空nested/cross-boundary、全Group=0、元処理nodeとport意味保存、元の階層へのUndo | SO-40→SO-61。拒否だけのwrapperやempty GroupではPASS不可 |
| R4 大規模preserve/flatten | fresh実データ複製と元non-Group >=1100 fixture。各modeで実変更3run、性能/全edge/rectangle/処理/Undo/run2/host健全性 | SO-70/71。flatten待ちでも独立preserve試験を先に閉じる |
| R5 仕上げ | 故障/cancel/timeout復旧、final install、fresh Verifier、PR/remote/readback、exact cleanup | SO-80/90と全G01–G14。未達をoptionalへ落とさない |

これは既存taskを読みやすく束ねた実行ビューで、新しいmandatory micro-gate群ではない。直近のcoherent成果を具体化し、遠い実装手順は現物に応じてWorkerが決める。小さな可逆実装判断のたびに新規管理書類や上位承認を増やさない。

順序変更/分割は、Goal・gate・権限・安全が不変ならCoordinator裁量。実装と判定条件を同じWorkerが都合よく変えることは禁止。shared state/integrationは一writer、hostも一ownerを維持する。

## 6. 一回の外側実行で複数工程を進める

`current state/差分証拠 → 次のready Goal → bounded Worker → 決定論的試験 → fresh Verifier → 統合/証拠/状態更新 → 次のready Goal`。

Worker完了やcommitはプログラムの停止理由ではない。少なくとも二つのready成果がある実行では、実際に次のGoalへ進んだことを記録する。回数を増やすために架空のtaskを作らない。長い同一修復は同じWorker contextで続け、milestone/肥大化時だけdurable evidenceからfresh化する。

Worker packetは、Goal、current candidate、owned subsystem/path、必要ref、Done、禁止範囲、検証、返却schema。Coordinator全文脈や全Libraryを転送しない。返却は変更surface、実コマンド/結果、実測、残る未達、failure fingerprint、次の識別試験だけ。model/role名でPASSにしない。

同じ入力/同じ仮説/同じrouteのunchanged retryは最大1回。その後は新しい識別試験かrouteを変える。異なる症状を件数だけ合算して自動昇格・全体停止しない。毎回の短周期pollは避け、runtimeの完了待機/イベントとbounded確認を使う。429なら成果を保全し、対応済みのbackoff/resume。quotaを回避する接続・未許可課金routeを作らない。

context/実行上限が来たら、canonical state、exact source/installed revision、owned process/lease、unfinished operation、次のready Goal、evidenceを保存して安全停止/対応済みのresumeへ渡す。未実行の将来継続を約束しない。自主的なcheckpointのたびにユーザーへ次の一文を送らせる運用はしない。

## 7. 検証・導入・報告

オフライン試験は指定worktreeのsrcをPYTHONPATHにし、importされたmoduleの`__file__`を同時記録する。旧checkoutをimportして起きた失敗が記録されているため、件数より実体を確認する。focused→relevant suite→candidate時のfull/compile/diffへ広げる。既存Python/manifest/scriptを使い、架空のコマンドや絶対pathを固定しない。

installerはcandidate source、package全files、entry、manifest、backupを結び付ける。d7a1610がremoteにあることからinstalledもd7aと推測しない。改行差と実コード差を分け、未知差分を上書きしない。テスト用envやUI回避値をユーザー/システムへ永続化しない。

処理関数の直接呼出、実widgetのRun/Cancel、native view設定、actual wire表示、処理stateとrenderは別proof。必要な全edge/fieldを取得し、unknownを空扱いしない。busy/resultは同じrun_idで観測し、別runのwindowでorderingを作らない。旧UIA/MSAAの限界を再発見する代わりに既存設計のowned UI経路を進める。

host testはdisposableだけに書き、fresh valuable baseline、single Undo/rollback、run2、no-save、exact cleanupを確認する。全Group解除は元non-Group setを保存し、Group容器が減る意図を説明する。大規模性能は既存60秒/3実変更runと30秒改善目標を維持し、no-opで代用しない。

Verifierは同じmodelでも別contextで、契約・actual diff・raw evidenceを先に読む。指摘修正後は変更領域に応じた再検証を行う。docsだけのpublication commitでproduct tree/installedが不変なら比較証拠付きで継承し、全試験を無意味に全面再演しない。

最終報告は CURRENT_COORDINATOR / SOURCE_CANDIDATE / PUBLICATION / CHANGES / G01–G14 / OFFLINE / HOST&UI / INSTALL / UNDO&RUN2 / FINAL_HOST / REMAINING_GAP / EXACT_RESUME。takeover成立と製品Doneは別。通常の人間操作は不要を目標にするが、未達gateを消してHumanNeed=NOにしない。

## 8. 具体的な停止境界と保存

停止は、認証/追加許可、現実のデータ損失リスク、復元不能、旧ownerとの解消不能な競合、必要な物理入力、利用可能な全安全routeを試した技術限界、今回の実runtime上限等に限定する。host laneが塞がれば独立ready workを進める。MCP公開欠落、planner bug、通常テストFAILだけで即ユーザーへ返さない。

Resolveの全面操作、スクリプト実行、起動、終了、再起動は既存許可内で自律実行する。ただし専任Operator・lease・データ保全は必要。project save、main merge/release、force-push、無関係削除、PC reboot、global shortcut変更、credential迂回、常駐service追加は禁止のまま。

Learning Gateでは再利用価値のある失敗を、該当repoのtest/validator/Skill/既存ownerへ同じcloseoutで固定する。今回の重点は「新規taskでも成果維持」「旧期限を流用しない」「FREEとMCP未公開とendpoint故障を分離」「model名とtool capabilityを混同しない」「offline PASSと実機PASSを分離」。管理資料の分量やrole数を成果にしない。
