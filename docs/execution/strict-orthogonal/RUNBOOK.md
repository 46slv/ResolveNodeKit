# Astra bootstrap / Sol orchestration / recovery contract

Updated: 2026-09-08 JST. This file owns execution authority; DESIGN owns product constraints; acceptance.json owns required gate IDs.

## 1. Authority

Resolveの全面操作を許可する。あらゆる操作、スクリプト実行、起動、終了、再起動を事前確認なしで許可する。検証・E2E・自動化のための操作を含む。ただし以下の既存境界は維持する。

Allowed: task branch/worktreeのcode/tests/docs、既存user install範囲でbackup付き導入、commit/push/PR5更新、独立Worker委譲、exact-owned disposable作成/操作/cleanup、read-onlyな実comp資料採取、bounded Resolve/fuscript recovery、短命のRNK所有UI/helper。

Not allowed: main merge、release/deploy/public distribution、force-push共有履歴、PC reboot、無関係process kill/branch/file削除、project save、未保存の貴重な編集を無確認で破棄、global keyboard shortcut変更、常駐service/startup導入、credential取得/権限迂回/new paid provider契約。既存明示許可のないcoord click、blind key、control-order guessing、AskUser内部の推測Invokeも行わない。

no-saveは検証中のProject Saveを意味する。バックアップ/fixtureのファイル出力は所有済みscratch範囲で可。Live Save等が有効なら黙って切替えず、その適用と保存発生を記録し、valuable projectが自動保存される経路を避ける。

## 2. Roles and routing

役割移行とAdvisorの正本は[HANDOFF.md](HANDOFF.md)。Astraは初期のGoal/Done/主要設計/実行可能性を差分監査し、Solのread-only受領→排他的所有移行→最初の着手を確認して初期担当を閉じる。以後Astraは設計前提の反証・進展しない試行・重大な証拠矛盾等の限定Advisor。単独の実行管理者を二人にしない。

Sol Coordinator: 受領後のtask選択、契約整合、リスク判断、唯一のshared state/integration writer。Goal/Done/権限内のtask追加・分割・順序変更は理由を記録して自律判断する。通常のtiny debugを全件自分でやり直さず、通常判断をAstra待ちにしない。Advisor案の採否/理由と検証はSolが所有する。

Execution Worker: current work packageのみを実装/検証しcompact evidenceを返す。既存で使えるLuna Max等をroutine laneとし、Sol自身を必要なbounded workへ使うのも可。model名/CLI flags/価格は固定せず現runtimeからbindする。OpenCode/Museは必須でなく旧rate-limited runを再起動しない。

Fresh Verifier: independent contextでexact candidateを検査する。Worker説明より先にcontract/diff/tests/raw summariesを見る。修正はしない。修正後は新candidateとして再資格認定する。

既存のrepo-local Skills/Harness/起動機構を再利用する。新しい一般purpose orchestratorの開発をmissionの前提にしない。通常は同時Worker最大2、所有pathとworktreeを分ける。host操作は一名だけ。他Workerはoffline作業を進め、host requestをそのownerへ渡す。多context利用が実在しない時はunsupportedを記録し、単独self-reviewを独立Verifierと呼ばない。

## 3. Opening and durable state

開始/再開時は先にhandoff/active ownerを照合する。作成/起動のtimeoutは失敗を保証しないため既存thread/requestを照会し、二重起動・leaseの無断奪取をしない。Astraは移管後read-only、Solが以後のstateを更新する。

開始順: Git status/remote → AGENTS/CURRENT → latest strict contract → relevant evidence → active runtime/host lease。既存作業を保全するまでpull/checkout/rebaseしない。PR5 headをcanonical integrationへ一本化し、旧task branchとのforward/divergenceを照合する。

移管前は初期担当/既存Harnessのsingle-writer、移管後はSolがCURRENT_STATEとacceptance.jsonのhandoff_state/status、exact candidate、stage、evidence location、next_ready、active writer/host leaseをcheckpointする。raw会話全文をWorkerへ転送しない。Task packetはgoal、owned paths、Done、必要refs、authority、compact返却だけ。

一つのouter invocationで複数goalを進める。checkpointは終了条件ではない。context rolloverはdurable stateからfresh contextへ移り、済みgateを全面再演しない。

## 4. Host execution boundary

最初に短いread-only identity/health probe。project/timeline/compは名前+tool数だけでなく実ID/参照をbindする。旧967 toolsやPSD2Fusionという文字列だけでmutation先を決めない。current valuable baselineがModified=trueでも勝手にfalseへ戻さない。元状態を保全し、fixtureへ隔離する。

graph APIsはqualified host thread/contextのみ。高価な全graph処理はin-processで一回実行し、短いlaunch/status/readbackを分離する。transport timeout後に同じwriteを再発行せず、operation run_id/commit状態を先に照合する。timeoutは実行取消を保証しない。

snapshot/plan/commit間のユーザー編集はgeneration再検証で検出する。Undo開始前にmutation planが完全か確認。成功run2は直後に実施し、その後最初の実変更を所有するUndoを検査する。no-op run2がUndoを作る/作らない差もrecordする。

cleanupはprefix一致だけで削除しない。作成台帳のexact IDs/ownershipと内容を照合し、disposableだけ削除する。最終はfresh valuable baselineのproject/timeline/page/selection等へ戻し、unexpected save/dirty deltaが無いことをreadbackする。

## 5. UI without repeated human gates

既知AskUser metadata不足を再調査し続けない。installed menu invocationが過去に成功した意味identity経路は、capability研究の再演ではなく新candidate smokeとして使ってよい。

UIAで無理な部分はRNK所有UIのstateとactual event配送を設計する。UI内部ID→state→event→production controller→actual graph→same-run busy/resultを追跡する。direct controller呼出だけのproofはHOST_BEHAVIORであってUI_E2Eではない。外側NO_UI環境変数や違うテストalgorithmでrelease E2Eを置換しない。

actual Comp Script contextと外部direct contextのUIDispatcher能力を分けて測る。必要なら最小のRNK所有modeless UIへ変更する。UI/runtime能力が確認できないまま大規模GUI frameworkを導入しない。標準/導入済み依存を優先し、新依存の供給元・license・配布方法を確認する。

実UIの可視性、状態、Run/Cancelの配線を機械で確認できればhuman smokeを既定で要求しない。provider残骸の存在だけでvisible/hiddenを判定せずwindow visibilityとcontroller lifecycleを関連付ける。別runのwindowを閉じない。

## 6. Recovery matrix

| Fingerprint | 自律復旧 | 停止/再開境界 |
|---|---|---|
| stale local / remote divergence | dirty workをbranch/patchに保全、non-force統合、affected tests | ownership conflictが解消不能ならS-OWNER。履歴削除しない |
| endpoint hang | producer状態を確認し、exact Resolve/子fuscript tree記録。通常終了→bounded wait→必要時exact forced cleanup→通常再起動→短いread-only再bind | 1 recovery cycle後も同じ無応答ならhost lane停止。unrelated offline続行 |
| valuable unsaved work during recovery | 非保存backupや既存復元経路を確認、data lossなしのrestartを選ぶ | 保存/破棄を安全に決定できない場合だけS-DATA、人間判断。権限でdata-loss proofを置換しない |
| long host call / payload | profiling、in-process index再利用、compact hashes、launch/status分離 | 同じtimeout callを反復しない。launch後unknownならreadbackまでnew write禁止 |
| Ungroup method absent | installed docs/registryに根拠のあるnative command/action/menuを小fixtureで測定。host/context限定結果を記録 | 意味identityまたはexact restorationが無ければ当該経路拒否。全経路なく復元不能ならS-HOST-API。機能をoptionalにしない |
| AskUser UIA/MSAA hard limit | RNK-owned UI/testability経路へ。現providerの再探索終了 | UI gateが未証明なら未達。他ready workを続行 |
| Orthogonal display control absent | documented/identity-based native view操作を資格認定、scope/rollback測定 | 斜線を許容せずS-VIEW局所gap。position-only PASSをstrictへ昇格しない |
| rectangle/row/port mismatch | failed constraintsを固定fixtureへ、module再配置/整数gap拡張 | bad planはwrite前拒否。budget超過はrepair/性能work |
| mutation invariant or rollback mismatch | 新write停止、before/after/evidence保全、owned Undo/readback | exact restoration不能はS-DATA。後続host mutationを禁止 |
| 429/quota/context exhaustion | process/session/dirty work保全、既存許可laneへ切替またはsupported backoff/resume | tight polling/retryなし。新課金providerはS-AUTH。再開はexact last verified point |

同じunchanged failureのretryは最大1回。次は新しい証拠を得る別仮説/別経路へ変える。3回同じblockerを数えただけでprogramをblockedにしない。Coordinatorはremaining ready workを必ず再評価する。

## 7. Stop and completion

HumanNeedはデフォルトNOという報告定数ではない。通常の開発検証は無人を目標にするが、実証前はNOT_YET_PROVEN。停止はS-AUTH、S-DATA、S-OWNER、S-INPUT、S-HOST-API等を具体的なevidenceとともに記録する。何が人間だけの入力か、何が単なる技術未達かを分ける。

required host gapが残っても独立ready taskは進める。全部のready workを尽くした時はCHECKPOINTED_WITH_TECHNICAL_GAP。全required gate PASS時だけSTRICT_LAYOUT_RELEASE_CANDIDATE、human release smokeは自動UI proofが成立すればNOT_REQUIRED。残る場合は最後の一件だけ具体的に提示する。

最終報告は exact candidate / required gate matrix / same-run UI proof / 1100+ preserve+flatten timings / processing+Undo+run2 / final host / installed+remote hash / real blockers / human-only action。plan publicationや監査PASSを実装完了と混ぜない。

## 8. Evidence-based advice and initial Done

Astra相談にraw全会話を送らず、consult_id・candidate/plan・反証された前提・試行結果・判断点・候補と最小検証を渡す。返答は助言でありwrite/権限変更の許可ではない。Solがadopt/reject/needs-user-decisionを記録し、独立ready workを続行する。Advisorが不在でも通常修正は進める。危険な前提だけ保留し、人間判断が必要な理由を特定する。

初期DoneはHANDOFFのEXECUTION_CONFIRMED、製品Doneは既存全gateの最終証明。thread作成だけ、Astraが計画を保存しただけ、Solの自己申告だけでは前者も閉じない。App Server等の具体syntaxは導入済みschemaを確認し、存在未確認のlaunch tool/IDを作らない。実機未接続ならその限定境界を報告する。

## 9. Current invocation grant — AS-BOOTSTRAP-20260908-1

User request began at 2026-09-08T01:07:27Z (10:07:27 JST). This invocation,
including the independent Sol continuation, has a hard deadline of
2026-09-08T02:07:27Z (11:07:27 JST). Complete within that hour if possible;
otherwise Sol writes a handoff report to the existing checkpoints directory,
updates CURRENT_STATE/acceptance/PR #5 with actual evidence and remaining gates,
leaves no ambiguous owned mutation, and ends this invocation at the deadline.
Do not start a new host operation that cannot safely settle before the deadline.
The deadline does not waive G01–G14 or permit a product completion claim.

The current user routing requires all live Resolve observation/control through
the personal `resolve_operator` custom agent. Sol remains the sole execution
Coordinator; it delegates bounded live work to that agent and retains queue,
integration and evidence acceptance ownership. Read the installed
`C:/Users/shiro/.agents/skills/resolve-operator/SKILL.md` before the first live
delegation. Other active tasks may use the same Resolve instance: acquire an
exclusive host owner only after checking their live ownership. Their presence
does not block independent offline work and is not permission to interrupt them.

This grant retains full Resolve operation/restart authority, no project save,
no main merge, and all existing data-preservation boundaries. Normal failures
and checkpoints are not stop conditions before completion, a true boundary, or
this deadline. Astra's Bootstrap role ends after verified Sol receipt, transfer
and first action; subsequent normal progress belongs to Sol alone.
