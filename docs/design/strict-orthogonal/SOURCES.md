# Sources and interpretation boundary

Updated: 2026-09-08 JST. Source-derived observations、previous authored analysis、new design decisionsを区別する。

## A. Repository baseline

Authoring時にGitHub readで確認したPR #5はOPEN/Draft、head `562405079aa6bffa6d25668b294a26ac4142a680`、base `feat/bootstrap-nodekit-20260905`。product証拠の基準は`59eeffbce5efd0a73a0fed2a4f3418faf71d5852`。main未merge。

[large preserve checkpoint](../../checkpoints/2026-09-08-semantic-arrange-v1-large-preserve-optimized.json)は977/1110 toolsのpreserve、run2 moved=0、約17秒、structural/Undo検査を報告する。processing hashはNOT_COLLECTED_BY_HOST_ADAPTER。旧overlap指標は全rectangle/全wire検査を意味しない。

[flatten capability](../../checkpoints/2026-09-08-semantic-arrange-v1-flatten-capability.json)は既知callable表面のprimitive不在とzero-write refusal。実flatten PASSではない。旧SAV1-80 PASSは独立監査の判定であり、required flattenの達成証拠ではない。

この文書作成中、Resolve実機は操作/再検証していない。historical host versionや967/977/1110等の個数を現在のtarget identityに使わない。

## B. Empirical JSON

[元JSON](../../reference/2026-09-06-fusion-timeline1-layout.json)と[元メモ](../../reference/2026-09-06-fusion-merge-parallel-note.md)を保持する。

固定参照blob: `8288565398e77fc1c0c0853e9013158fd73201f0`、reported size 339236 bytes。schema `resolve-node-kit.layout-ref/v1`。declared tool_count=1109、group_count=29、Merge=257。

先行ChatGPT監査はsource-line照合、29 Groupのparent照合と主要Merge入力の確認であり、339KB全体をJSON parserにかけた全件検算ではない。完全graphや全入力証明へ昇格させない。SO-10でrepoの実bytesを解析し、宣言countとの一致/不一致も記録する。

### 照合済みの具体例

- 29 Groupの内訳はroot直下15、別Group内14。子Groupを持つ親が6個。親→子は d39e1b3dd7→11607d455a/0d70b78658/9157efa641、b6521522fc→2862be7104/1b04005c54、162461e9f9→d697e206cc/1e2a7bad8e/d623af7e3a、a1bb2f4d0a→3a8384af06/c499c24cf5/e47107af2d、2cdcd869ea→7edb87c28a/c58b72621f、140aae8caf→ed6fd1ff06。各tokenは`Group_` suffix。
- x=29の6 Mergeは6段BG chainではない。`GroupCanvasRII_15a9fea850 -> MergeRII_a1bb2f4d0a -> MergeRII_1829a7e279 -> MergeRII_2cdcd869ea -> MergeRII_d39e1b3dd7 -> MergeRII_162461e9f9`がBG接続、その終端は`MergeRI_15a9fea850.Foreground`へ入る。receiverのBGは`MergeRI_140aae8caf`。
- x=31.5では`MergeR_fbfee71607 -> MergeR_aad6b9c882 -> MergeR_48d6509e64`がBGで連なる。MediaOutへの最後のedgeはMerge入力表だけでは確定できない。
- `Merge2.Background=Glow1`、`Merge2.Foreground=MergeRII_e774bc83c3`。見た目のcontinuityをBG固定にしてはいけない。
- 同じx=-6.5の`LayerBlendCoverageRIII_cab248ac0a`と`LayerBlendSourceMixRIII_cab248ac0a`は、同じXというだけで連続BG chainではない。
- `MergeRII_daf8601c0f`はこの記録ではBG入力のみ。名前からFGを補わない。`GroupCanvas`はBackgroundでありGroupOperatorではない。

JSONのtool_rowsは名前/type/parent/raw/snapped座標、merge_rowsは取得されたMerge入力を持つ。全non-Merge入力、全source-output IDs、処理parameters、keyframes、全view矩形/pipe geometryは未収録。全件parseが成功しても、この情報欠落が埋まるわけではない。

## C. User screenshots

以下はユーザー提供の2枚。capture日時・host version・JSONとの同一run対応は確定していない。

| Reference | 原ファイル | Size | Original SHA256 |
|---|---|---|---|
| V-A | d78515a3-f61e-4976-8d54-6280843a9ef7.png | 2048x1076 / 167222 bytes | 9b6423378a7e1232b1d66ccfbd2cfc26d2a19dfaeacd4da8790210d027932473 |
| V-B | 3205d12d-8cf7-477a-a7fa-b85fbe479d74.png | 2048x966 / 201267 bytes | faf8a85daee75470a85252b34806a67eaf31e631381d25eb11743be5e15b1e3c |

原PNGは今回のGit treeに含めず、別添source bundleへ保持する。sandbox URLをCodex用の必須入力にしない。以下の観測とDESIGNの配置契約はrepoだけで読め、実装開始は原PNGの再アップロード待ちにしない。画像そのものと比較したとclaimするのは、元画像bytes/hashを実行側で確認できた時だけ。

観測: 下側の長い水平列、各合流点の上側の短い縦列、右上の独立した水平subgraph、そこから下への長い縦接続、右側の縦集約と横枝、最後のMergeより下にある出力、region間の広い空白。緑/灰/黄等の色は見えるが、色だけからRegIDや処理意味を確定しない。

補正: 少数の斜線は画像に存在するため、strict要求がpixel再現より上位。node数、正確なport接続、hidden Group内部を画像から断定しない。「上部region」「右側reduction」は本referenceに合うstyleであり、存在しないtopologyを生成する命令ではない。

## D. Prior design / outside context

先行添付`ResolveNodeKit_Strict_Orthogonal_Design_v1.md`と`ResolveNodeKit_Source_Interpretation_Audit.json`はDESIGN_PROPOSAL/限定監査だった。本v2は上記資料を統合し、視覚profile、自動UI検証、Sol実行契約を追加する。新しいsource読解やhost成功を過去資料へ遡及して記入しない。

Orthogonal PipesはBlackmagic Fusion 20.3 publisher-authored manualの再掲で確認された追加知識。https://manualzz.com/doc/89513161/blackmagic-fusion-20.3-instruction-manual 。再掲/旧versionなのでtarget Resolve21の制御APIや全wire保証の証拠にはせず、SO-30でinstalled docsとactual viewを資格認定する。

運用の作成根拠: ChatGPT Library Coding IntelligenceのCODEX_PROJECT_CONTINUATION_WORKFLOW (2026-09-06)、CODEX_ORCHESTRATION (2026-09-05)、CODEX_PROMPT_ARCHITECTURE (2026-09-06)。必要な実行契約はこのrepoへ展開してあるため、CodexがLibraryへアクセスできる前提はない。

## E. 禁止する証拠の合成

別runのbusyとresultを同じrun orderingにしない。empty Groupでchild preservationを証明しない。完全schemaでない旧referenceをrender oracleにしない。小規模/旧candidateのPASSを新しい1100+flattenのPASSにしない。UIManager IDの存在とOS UIA semantic identityを同一視しない。worker報告の復唱を独立検証と呼ばない。
