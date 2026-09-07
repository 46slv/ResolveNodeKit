# Work packages and acceptance ownership

Updated: 2026-09-08 JST. Statusは[acceptance.json](acceptance.json)を初期契約とし、実行開始後の進捗はCoordinatorだけが更新する。旧gateを再度全部走らせるのではなく、変わったsurfaceと新しい必須証明に集中する。

## Bootstrapからの受け渡し

AstraのAP-10/20/30/40は[HANDOFF.md](HANDOFF.md)に定義する。製品Doneではなく、現状確認・計画の差分監査・限定probe・保存・Sol受領・所有移行・最初の着手が初期Done。既存設計を白紙に戻さず、重大な未知は根拠/未確定/最初の検証を明示する。Solは受領後SO-00から進め、Astraの同じprobeを無条件に再実行しない。

Goalと必須G01–G14を不変にして、Solがtaskの追加/分割/順序変更を理由付きで行ってよい。required_task_idsの変更は、元task→新task→保全するgateのmappingを記録して契約検査する。Done/権限の緩和や別missionの追加はこの裁量に含まれない。通常失敗やtask再編にAstraの逐次承認は不要。

## Task graph

SO-00 → SO-10(source/schema) → SO-11(host snapshot)。SO-20(planner)とSO-30(view)はSO-10後、SO-50(UI)はSO-00後に独立進行できる。SO-40(flatten)の構造writeはSO-11を待つ。ただしResolve hostは必ずsingle-writer/one lease。SO-60/70はpreserveの統合/large、SO-61/71はflattenの統合/large。flattenが局所blockでもstrict preserveの実機完成を止めない。SO-80が耐障害、SO-90が最終独立検証。

| ID / 完成させるもの | Depends | Owner / 書込scope | Done / evidence | 失敗時・再開 |
|---|---|---|---|---|
| SO-00 実行基盤と正本を固定 | none | Sol Coordinator / state, isolated worktree, runtime binding | 受領したhandoff_id/plan revision/ownershipを照合し、local/remote/installed candidate、実効instruction chain、host PIDとcurrent target、既存run lease、利用可能なWorker/Verifier経路を確認。actual採用ID/権限/再開方法を記録。既存127はbaseline記録で新run PASSではない | dirty work保全、leaseを奪わない。runtimeが無ければ利用可能laneで独立offlineを進め、認証/課金は人間境界 |
| SO-10 ソース全件解釈とsnapshot契約 | SO-00 | Data Worker / schema, pure fixtures, source audit | repo JSONを実parseしunique node/parent/cycle/count/grid/merge inputを全件検算。unknown入力はunknownのまま。完全snapshot schemaと人工complete fixtureを固定し、source由来との違いを明記 | 旧JSONの欠落を埋めたことにしない。hostの未提供能力はSO-11へ分離し、offline planner/UIを止めない |
| SO-11 完全host snapshot adapter | SO-10 | Host Worker / adapter, coverage tests | 非空nested disposableと安全な実データreadからport/proxy/処理stateを取得し、complete/unsupported/errorを機械判別。unknownを含むsnapshotへの構造writeは拒否。最終実データcoverageはSO-70でも検査 | bounded API/serialization readへ切替。host read不足はSO-40/60の依存blockerだがSO-20/30/50は継続 |
| SO-20 参考profileを持つstrict planner | SO-10 | Layout Worker / semantic planner, geometry, tests | multiedge保存、role/continuity分離、recursive bounds、rectangle非重複、整数pitch、rail/feeder/region/reduction、stable run2。O01–O18の対応fixturesで反例を先に固定。plan出力にmotifとall-edge coverageを残す | 衝突はmodule移動/gap拡張、shared sourceは複製しない。budget超過は性能課題として局所化。reference座標hashにfitしない |
| SO-30 native strict view realization | SO-10 | Host/view Worker / adapter, host tests | 実installed docs/contextでOrthogonal Pipes等のnative経路を資格認定。設定scope/pre/post/復元、port表示、実画面samplingとcontractを同一runで確認。node位置だけ/overviewだけではPASS不可 | API不在なら意味identityのnative action/menu。既知AskUser probeは再演しない。native機能を制御できない場合は局所technical gap、斜線許容へ下げない |
| SO-40 safe flattenを実際に動かす | SO-11 | Structural Worker / flatten adapter, tests | document/registry-derived native operationを検証し、非空Group、2+depth、cross-boundary/instances/expressions/animationのsmall fixtureで全Group=0、元non-Group/処理接続保存、1 Undo exact、run2 stable。zero-write refusalはPASS不可 | 既知の不存在methodを再探索せずnative command/menu等へpivot。child再生成・推測設定は禁止。復元不能なら構造write停止、独立laneへ |
| SO-50 人間クリックを要しない実UI検証 | SO-00 | UI Worker / owned UI, controller glue, installer, tests | 簡潔なpreserve/flatten UIと同一controller。実widget state/eventを自動観測/配送し、setup→Cancel zero-write、setup→Run、busy→resultを同一runで証明。installed menu entryも実行。内部controller直呼びは別proof | AskUser metadata再調査ではなくRNK所有のinspectable UIへ変更可。UIManager IDだけのPASS禁止。短命helper可/常駐不可。host所有者へ操作を依頼 |
| SO-60 preserve/UI統合と小規模実機 | SO-11,20,30,50 | Integration writer + Host Worker / candidate branch | full offline/compile/diff、install hash、flat/multiedge/Mask/non-empty nested preserveで実UI→同一controller、processing state、Undo/run2、no-save/exact cleanup。flatten未達でもpreserve qualificationを進める | failed categoryだけWorker修正、影響gate再実行。旧別candidateを無条件合成しない |
| SO-61 flatten統合と処理意味保存 | SO-60,40 | Integration writer + Host Worker / candidate branch | 小規模非空nested flattenで実UI→同一controller、port/proxy/processing stateと複数frame render、Undo/run2、no-save/exact cleanup。保護されたpreserveを壊さない | SO-40の未達はこのlaneに限定。processing取得不十分はPASSにしない |
| SO-70 strict preserveの実データ/1100+ | SO-60 | Host Worker / bounded real duplicate + generated fixture | fresh real PSD2Fusion-scale disposableとnon-Group>=1100+nested fixtureの両方。all-node/edge coverage、rectangle=0、strict display、処理保存、Undo/run2、3回のaction<=60s、endpoint loss=0。compact hashes/actual screenshots保存 | profileとpayload分離。単なるpaddingではなく枝/shared/cross-boundaryを含める。flatten gateが未達でもこのlaneは閉じる |
| SO-71 flattenの実データ/1100+ | SO-61,70 | Host Worker / largest safe duplicate + non-Group>=1100 fixture | 全Group=0、元処理graph保存、strict/profile/rectangle、grouped Undo exact、run2=0、3回のaction<=60s、endpoint loss=0。SO-70からproduct変更があれば影響するpreserve証明も更新 | zero-write refusal/empty Group/old preserveでは閉じない。失敗をprofileして戻し、requiredのまま保持 |
| SO-80 復旧/再開/配布を閉じる | SO-60 | Worker + Coordinator / host runner, package, focused tests | timeout/exception/partial write/cancelの安全境界、rollback mismatch停止、旧endpoint結果の再適用禁止、context再開、一つのouter invocationから2+goal継続、boundedrestart、package再install/uninstallのbackup、no global env leak | ambiguous writeはreadback前にretryしない。復元できない場合は現物保全しhostwrite停止。通常失敗で全programを終えない |
| SO-90 fresh verifier / final publish | SO-71,80 | fresh independent Verifier; shared更新はCoordinatorのみ | required IDs全PASS、実source/installed hash、changed diff、測定coverage、active UI user flow、1100+flatten、Undo/processing/strict/style evidenceを反証的監査。verifierは自分で修正しない。PR5/状態/remote readback整合、final baseline復元 | FAIL→Worker新candidate→影響gate→fresh verifier。technical gapは未完checkpoint。人間一回を全gateの代用にしない |

## Required fixture catalogue

O01 serial H/V、O02 horizontal Merge+feeders、O03 x29型5BG+FG receiver、O04 x31.5型3BG、O05 Merge2型FG continuity、O06 same-X non-chain、O07 same-node-pair別port、O08 Group boundary projection、O09 unequal rectangles/expanded-vs-collapsed、O10 shared source/fan-out/multiple outputs、O11 Mask/auxiliary links、O12 missing input coverage、O13 29Group census derivation、O14 flatten twice/former-region stability、O15 >=1100 non-Group/deep chain、O16 actual native view and coverage、O17 UI Cancel/Undo/rollback、O18 host readback offsets。

図形goldenはnode enumeration、stable originに対する平行移動、display renameで不要に変わらない。source不明の接続をcanonical fixtureに補う場合は人工fixtureとして明記する。全旧sourceのrender再現をclaimしない。

## User-visible style acceptance

reference-derived mixed fixtureでは、主railのnode y一致/x単調、短いfeederのx一致、subgraph独立bbox、topologyが存在するとき右側reduction整列、最後の出力の単純なH/V接続、region clearanceを検査する。row/column制約、nonoverlap、strict wireは必須。余白の絶対pixel比率や全graphの一本railは要求しない。

actual large canvasはoverviewに加え、主幹/上部region/集約/最難配線/非空Groupまたはflatten後領域を読み取れるzoomでcaptureし、fresh visual reviewerがcontractに沿って確認する。画像の雰囲気だけでsemantic/processingを合格にしない。

## Evidence per run

schema、run_id、candidate/source/installed hashes、target stable IDs、host/build/context、before/after state、all-edge coverage、processing coverage、mode、stage timing、pipe-mode scope、geometry/visual observation level、actual mutations、Undo owner、run2、cleanupとvaluable baselineを関連付ける。大きいfull snapshotsはローカルartifactへ、repoはredacted summary/hashes/必要fixtureを保存する。private media pathやclient画像を無断公開しない。

同じrunのUI timestampsとAPI readbackを結び、外部監視が止まってもproducerのterminal statusを残す。NOT_COLLECTED/UNVERIFIEDがrequired fieldにあるrunはrelease proofにならない。

## Candidate and measurement identity

product source commit/hashとpublication/state commitを分離する。証拠採取後のdocs-only commitは、product treeとinstalled hashes不変を比較で証明できる場合に限り同一candidate evidenceを継承できる。単にHEADが新しいだけで全host試験を再演しないが、コード変更後の証拠を旧candidateへ混ぜない。

性能3回はそれぞれ同等の未整列/未flatten baselineから開始する実変更run。moved=0のno-opだけを3回測って合格にしない。run2安定性は各成功runの後に別途測る。SO-80のflatten専用host faultケースはSO-61の後に行い、未実施はG12/最終完了へ反映する。
