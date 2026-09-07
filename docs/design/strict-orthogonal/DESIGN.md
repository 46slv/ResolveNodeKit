# Strict Orthogonal Arrange — 設計契約 v2

Updated: 2026-09-08 JST  
Status: DESIGN_READY / IMPLEMENTATION_AND_HOST_QUALIFICATION_PENDING  
Scope: ResolveNodeKit / Fusion whole-comp preserve + explicit flatten-all  
Baseline: PR #5, `562405079aa6bffa6d25668b294a26ac4142a680`  
Source interpretation: [SOURCES.md](SOURCES.md)  
Execution entry: [README](../../execution/strict-orthogonal/README.md)

## 1. 完成させる体験

現在のFusion comp全体を一度の操作で整理する。基本はGroup保持、明示的に選んだ場合は全GroupOperatorを解除して整理する。実データと、元non-Group toolが1100個以上ある非空nested fixtureの両方で動作させる。

目標は「全部を一列にする」「ノードを格子に乗せるだけ」「直角配線モードに変えるだけ」のいずれでもない。長い下側の水平主列、上から入る縦の処理列、必要な上部サブグラフ、終端付近の縦集約、まとまりを区別する余白を持つ配置にする。元の処理接続は視覚都合で変更しない。

ユーザーの「必ず水平垂直」をhard constraintとする。ノードの行列整列と、実際に表示される全接続線分の直交性を両方検査する。90度の折れ線は許容する。斜線は許容しない。Mask、fan-out、Group境界、未知のノード種を検査対象から除外してゼロを作ってはいけない。

この契約は旧SEMANTIC_LAYOUT、ORTHOGONAL_GRID、SAV1計画の競合部分を、このscope内で更新する。既存preserveの実機PASSは回帰基準として保存するが、新しいstrict/flatten/UIのPASSには流用しない。ColorやGroupを保持したまま開く別機能を完成済み扱いにしない。

## 2. 参考画像を仕様へ変換する

添付2枚は配置の意図を示す資料であり、全接続の正本やpixel-goldenではない。次を取り込む。

- 下側に、左から右へ読める長い水平railを置く。画面の固定pixel位置ではなく、comp内の相対配置で定義する。
- 短い前処理は受け先の上に縦に揃える。同型の列は同じ列間隔、同じ終端行を共有する。長さが違う列を同じ高さにするためのdummy toolは作らない。
- 独立して解釈できる上流subgraphは上側のregionとして置き、その内部にも同じrail/branch規則を適用する。
- BG等の実際の連続関係を持つreductionは縦列になり得る。終端寄りの集約を右側に置くのは、このtopologyがある場合の配置規則であり、全graphへ架空の「塔」を強制しない。
- 終端MediaOutは参考画像のように最終Mergeの下へ置いてよい。「MediaOutまで全部同じ水平行」は要求しない。
- 空白を残し、Merge間隔を整数セル単位で広げる。狭く詰めるために列を崩さない。

参考画像には局所的な斜線が残る。最新のstrict要求が優先し、その斜線は再現対象にしない。画像から読み取れない入力役割・処理意味は推測で補わない。従来回答の「全体一本の主経路」「高入次数なら集約塔」「ノード中心が揃えば配線も直交」は採用しない。

## 3. 優先順位

接続・処理の保存、全ノードの対象化、strict直交、矩形非重複、復旧可能性を同格の必須条件とする。その上で、主列/枝/regionの読みやすさ、局所pitchの統一、交差とwire長の削減、余白の適量化の順に改善する。重なり回避を美観より低い任意項目にしない。

ソースの形を模倣するためにBG/FGを交換する、処理順を変える、shared sourceを複製する、生成名だけから接続を作ることは禁止する。

## 4. 三層モデル

### ProcessingGraph

port付き有向multigraphを唯一の処理正本とする。Nodeはstable identity、display name、正確なRegID、direct parent、入出力metadata、処理状態の取得範囲を持つ。Edgeのkeyは `(source_uid, source_output_id, target_uid, target_input_id)`。同じnode対でもBGとFG等の異なるport接続を潰さない。

各取得結果はcomplete / absent / unsupported / errorを区別する。取得失敗を空listや未接続と同一視しない。全ノードとは、rootだけでなく再帰的なGroup内部を含む。non-visual modifiers、instance/expression dependenciesは配置対象でなくても処理保存検査に残す。

Group内部のterminalから外部consumerへ出る実edgeはそのまま保存する。親scopeの配置に限り可視Group境界へ投影し、元edgeとproxy mappingを失わない。生成名のsuffixとノードの近さは補助hintであり接続証拠ではない。

### LayoutModel

処理graphとは別に、HorizontalRail、VerticalReduction、SerialPipeline、FeederColumn、GroupRegion、GeneralRegion、DisconnectedComponentを明示する。各moduleはmembers、内部向き、入口/出口attachment、幅/高さ、整列制約、gap理由を持つ。全ノードはちょうど一つのlocal placement ownerを持ち、shared nodeを重複配置しない。

Mergeのprocessing roleとvisual continuityは別属性。BGは多くの合成列の探索hintになるが絶対条件ではない。完全な出力到達性、port metadata、継続する部分graph、共有関係からrail候補を比較する。現在座標は同順位のhintに限定し、label変更やnode列挙順で大きく形が変わらないようにする。曖昧な場合はGeneralRegionとして安全に配置し、誤ったsemantic claimをしない。

### ViewRealization

actual node位置、node/frame矩形、pipe display mode、modeの適用範囲、port表示位置、viewport/zoom、観測方法を保存する。plannerの図が直交でも実Fusionの表示が違えばstrict host PASSにしない。

## 5. 配置手順

1. 完全snapshotを一度取得し、generation/identityを固定する。scope、出力、component、Group境界を検証する。
2. 最大非分岐直列、実接続に基づくrail/reduction、shared feeder、Group boxを抽出する。高入次数・同じX・名前だけでmotif認定しない。
3. child scopeからbottom-upにlayoutとboundsを計算する。保持中のGroupを勝手に解除/展開しない。
4. componentごとに下側の主railと上流regionを配置する。複数outputを一つへ捏造せず、共有subgraphを共通regionへ置く。
5. feederを受け先の列/行へattachする。reference型reductionはBG連続部とterminalから別portへ合流する部分を分離する。
6. rectangle clearanceを検査し、行/列やmodule全体の移動、整数gap拡張で解く。個別nodeの斜め逃がしは禁止。
7. 全edgeの表示経路をrealizeし、独立validatorでcoverage、geometry、処理不変を検査する。
8. 書込直前にtargetとsnapshotが有効か確認する。変更されていればreplanし、古い計画を書かない。
9. 一つのowned Undo内でbounded writesを適用し、actual readbackを検証する。不一致ならrollbackして検証する。

全graphを各nodeから繰り返しwalkしない。adjacency、scope index、proxy map、rectangle spatial indexを再利用する。deep graphはiterative traversalを基本とし、1100-depth fixtureでrecursion overflowを検出する。探索budget超過はTIME_BUDGETであり「数学的に解がない」ではない。

## 6. グリッドと余白

論理座標は整数。raw host座標、論理セル、表示pixelを混同しない。通常nodeの基準pitchは3 logical cellsとする。幅1cellなら2cellsの空白という意味で、「3cells空ける」と混同しない。広いnode/Groupはbox幅とclearanceに応じて整数単位で拡張する。

sourceのx≈0.5/y≈1.0 snapやreadback offsetは当該hostの観測であり、全versionへの保証ではない。adapterが測定したgrid変換/誤差範囲を保持する。snap toleranceで本当の斜線や1cell driftを隠さない。

reference profileの初期値はbase pitch=3、node clearance=1、region clearance=2*pitch。これらは実装初期値で、画像から計測された厳密値ではない。余白の具体的長さはbox、接続corridor、branch高さから決める。画像の大きな空白比率を全graphに固定しない。

表示scope内のrectangle intersectionはゼロ。collapsed Groupはcollapsed nodeのbbox、expanded Groupはframe+内部領域のbbox。親子の包含を兄弟の衝突として数えない。node centers一致だけのoverlap検査は不可。

## 7. 接続表示の直交化

第一候補はFusion自身のOrthogonal Pipes。publisher-authored manual上に存在する表示機能だが、対象Resolveでの制御API、適用scope、readbackは未資格認定。存在未確認のAPI名を仕様として固定しない。

adapterはその場のbundled docs/registry/実menuでnative機能を特定し、変更前設定、変更後設定、対象viewへの効果を実測する。comp/view限定を優先。global設定しかない場合はscopeを記録する。通常成功後は対象viewのstrict表示を維持し、検証cleanup/Undo時に元設定へ復元する。全体設定にしか適用できない副作用はUIで明示する。global keyboard shortcutの変更はしない。

native displayが制御できても、ばらばらなnode配置をpipe表示だけで合格にしない。node/port alignmentとmatrix geometryも検査する。逆にnode中心が同一行でも、actual portがずれる場合は表示実体で判定する。

wireごとに観測/保証のcoverageを記録する。geometry全件readbackが無い場合は、同じhost/viewに適用されたnative orthogonal renderer契約の確証と、十分なzoomでの難所samplingを分けて提示する。この場合の主張はHOST_RENDERER_CONTRACT_PASSであり、全線分を個別測定したとは言わない。設定確認だけ、縮小overviewだけ、generated diagramだけではstrict host PASS不可。

view-only routerを使える場合はnative rendererの一部として資格認定する。処理toolとしてのrouter大量挿入、複製、別viewerでの見た目だけの代替は自動採用しない。routingは実graphの意味を保存し、未対応edgeを除外しない。

## 8. Flatten-all

preserveとflattenは明示的に別operation。通常UIはpreserveを既定にする。flattenを選ぶと全GroupOperatorを対象にし、非空nestedも含めてrootへ展開後、同じplannerへ渡す。Macro等の別typeを名前だけでGroupとみなさない。

現flatten実装は「明示primitiveが渡された時だけ動く」wrapperであり、hostのzero-write refusalはflatten成功ではない。既知callableが無いことだけで全native経路が無いとは結論しない。native command/action/menuを、docs/registry/意味identityで特定できる経路だけ調べる。generic DoAction文字列の総当たりは禁止。

処理nodeの既存identityを保つnative操作を優先する。container-only settings変換を検討する場合もchildをdelete/recreateするshortcutは禁止し、完全snapshotに対して操作前後の一対一対応、port/proxy変換、expression/instance参照を証明する。安全な経路がないときは機能を未達として残し、任意扱いへ下げない。

同一transaction内で、全Groupの解除、flat topology readback、全体整列、final verificationを行う。deepest-firstはhostで安全性を測定して採用する。期待postは全GroupOperator=0、元non-Group set保存。旧referenceなら1109−29=1080であり、総tool数不変を要求しない。1100-scale資格認定は別途non-Groupが1100以上のfixtureも用意する。

Group proxy消失でraw edge表記が変わる場合は正確なboundary mappingによりprocessing graphを比較する。無条件のraw hash同一も、単なるnode数一致も誤ったoracleとなる。Undoは元のGroups、membership、connections、positions、selection、処理状態を復元する。

FormerGroupRegionは近接のsoft hintとして使ってよい。ただし再実行でgroupが消えた途端に配置が変わらないよう、Undo対象の安定metadataまたはgroup無しでも再現できる分類からderiveする。test-only記憶やhidden envへ依存しない。

## 9. 製品UIと自動検証

UI shell、共通production controller、pure planner、host adapterを分離する。GUI Runも自動host実行も同じcontrollerを使い、test専用の別algorithmを作らない。

通常UIは全体整列の説明、明示的flatten選択、Run、Cancel、実行中/結果表示を持つ。処理が開始してから終了まで無言に見える状態を完成扱いにしない。percentageを捏造せず、実stageと件数を表示する。

AskUserの既知UIA/MSAA不足を直すこと自体は目的ではない。既存host contextで利用可能なUIを資格認定し、必要ならRNK所有の観測可能なUI shellへ置き換えてよい。UIManagerの内部IDを付けるだけでOS accessibility対応をclaimしない。

実controlのstate readbackと実event配送を、RNKが所有する明示ID/run_id経由で検証できるtestability境界を用意してよい。単にcontrollerへ既定値を直渡しすることはUI glue/E2Eの代替ではない。自動結果dismissは同じrunのRNK所有windowに限定し、手動UIと自動UIで処理内容を変えない。

busy表示→actual work→busy非表示→結果表示を同じrun_idで観測する。logは副証拠で、Hideを呼んだだけで実際に非表示になったとは言わない。短すぎて観測できないfixtureに人工sleepを足してPASSを作らず、現実に十分長い大規模runも使う。表示が失敗しても必ずterminal status/logを残すが、busy gateは未達として残す。

Cancelは開始前zero mutation。実行中cancelは安全境界で受け、partial flattenを放置しない。host APIを別threadから叩かない。短命のRNK所有UI/helperは許容するが、常駐service/watchersやstartup登録は行わない。

## 10. 安全性・完了

full before/after snapshotのcanonical処理比較を必須とする。layout-only metadata除外は明示allowlistとし、未知fieldを勝手に除外しない。parameters、keyframes、expressions、instances、media参照、time/range、tool enable/pass-throughを取得範囲付きで検査する。flattenはnon-empty representative compの複数frame render比較も行う。renderだけ、hashだけの片方で全意味保存を断言しない。

stage timingを測り、transportの短いlaunch/monitor/readbackとin-host production時間を分離する。1100+ actionは同一hostで3回すべて60秒以内を資格認定budget、30秒以内を改善目標とする。fixture作成/独立render検査は別計時、snapshot/flatten/plan/write/readback/verifyは含める。この数値は新しいengineering targetであり既存達成値ではない。達成できなければoptimizationへ戻し、測定後に黙って基準を下げない。

全required gateを最終installed candidateで証明し、fresh independent verifierが確認した場合のみSTRICT_LAYOUT_RELEASE_CANDIDATE。途中checkpoint、旧127 tests、large preserve PASS、false-PASS監査PASSを新機能の完成と混同しない。no save、exact cleanup、fresh valuable baseline復元を全host runで守る。
