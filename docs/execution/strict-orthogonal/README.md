# Strict Orthogonal Arrange — Sol continuation entry

Updated: 2026-09-08 JST  
Program: RNK-STRICT-ORTHOGONAL  
Authoring status: READY_FOR_RUNTIME_PREFLIGHT  
Execution status: NOT_STARTED_BY_THIS_PUBLICATION

## Goal

参考資料の水平主列/縦枝/上部region/右側reduction/余白を、処理graphから再構成する。全comp preserveと全Group解除後のarrangeを1100+ non-Group toolsで実機資格認定し、通常検証とinstalled product entryの反復human clickをなくす。

## One canonical continuation

Repo `46slv/ResolveNodeKit`、PR #5 head branch `feat/semantic-arrange-v1-20260906`を統合正本にする。基準readは`562405079aa6bffa6d25668b294a26ac4142a680`だったが、実行時はremote HEADをfresh-readする。旧`feat/arrange-uia-e2e-20260906`のdirty workや進んだcommitは保存/照合し、resetや無条件checkoutをしない。今回publishはdocs/instructionsだけでproduct code/installed実体は変えない。

Read: repo AGENTS → CURRENT_STATE → [DESIGN](../../design/strict-orthogonal/DESIGN.md) → [SOURCES](../../design/strict-orthogonal/SOURCES.md) → [PLAN](PLAN.md) → [RUNBOOK](RUNBOOK.md) → [acceptance.json](acceptance.json)。詳細な旧checkpointは該当failure時だけ読む。

この一括契約は現在の明示ユーザー要求を実行可能な形へ具体化したもの。旧SAV1の「large/flatten未証明でもcandidate」「busy任意」「human smokeを当然に待つ」「同じ失敗3回でgoal全停止」という競合する規則より、このscopeに限り優先する。main未merge、no-save、処理不変、実証なしPASS禁止は維持する。

## Sol orchestration

SolをCoordinator/acceptance ownerにし、実装Workerとfresh Verifierを独立contextへ分ける。利用可能なruntime/model/tool mappingはSO-00で確認し、名称からCLI引数や接続を捏造しない。Workerは通常Luna Max等の資格認定済みlane、意味解釈/競合/詰まった設計判断はSol。Muse/OpenCodeは必須にせず、旧429 sessionを再起動しない。

一つの外側実行からready taskを継続する。Worker完了をプログラム終了にせず、Coordinatorが証拠を読み次へ進める。全required gateを満たすか、RUNBOOKの真の停止境界へ達するまで継続する。

## HumanNeed policy

人間に毎回Run/Cancel/再起動/次の指示を頼まない。safe reversibleなrepo修正、fixture、Resolve操作、recoveryは自律実行範囲。技術的な失敗はrepair/別経路/局所blockerで扱う。未証明gateを消すことでHumanNeed=NOにしてはいけない。

認証/費用/破壊的な未保存実データ/競合する所有権/復元不能など、現権限では解決できない境界だけ人間へ上げる。必要なhost/APIが本当に無ければ最終状態はCHECKPOINTED_WITH_TECHNICAL_GAPであり完成ではない。人間smokeは既定の必須工程ではなく、実UIがどうしても未証明の時に限った最後の一件。

## Completion

全gate PASS、exact candidateのfresh verifier PASS、install/remote readback/cleanupまで揃ってSTRICT_LAYOUT_RELEASE_CANDIDATE。広いResolveNodeKit全体のMISSION_COMPLETEやmain merge/release権限とは別。計画監査のPASSもproduct完成を意味しない。
