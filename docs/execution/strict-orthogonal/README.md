# Strict Orthogonal Arrange — 新規 Luna Max task の入口

Revision: LM-TAKEOVER-20260910-2 + PO-TRIAL-20260910-2 + RO-CANARY-20260910-1  
Authoring: READY_FOR_LOCAL_TAKEOVER / runtime takeover not executed here

## 今回の指示

新しいLuna MaxのCodex taskが、既存ResolveNodeKitの成果と同じPR #5を引き継ぎ、実装・導入・実機検証を進める。Astra Bootstrapをやり直さず、旧Sol thread再開を既定にせず、新規taskの実所有を正規takeoverする。新規taskは進捗初期化を意味しない。

最初にlive Git、AGENTS、CURRENT_STATE、[LUNA_RUNBOOK](LUNA_RUNBOOK.md)、[PROMPT_ORCHESTRATION_TRIAL](PROMPT_ORCHESTRATION_TRIAL.md)を読む。製品Goal/DoneはDESIGN / PLAN / acceptance.jsonを継続する。

## Resolve live host routing — corrected

live DaVinci Resolveの状態観測・操作・実機validationが必要なら、親Lunaは**external Resolve Operatorへ委譲する**。親はResolve MCP / scripting / GUIを直接操作しない。

親が渡すのは原則これだけ:

```text
objective / target / observable Done / restore policy / required evidence
```

driver選択、inventory、exclusive lease、launch/quit/restart、operation、independent readback、cleanup/recovery、final readback、lease releaseはResolve Operatorが所有する。native MCP / qualified compatibility MCP / scripting / GUIの選択を親promptへ固定しない。

Codex 0.153.4の`global MCP disabled + same-session child roleでMCP enable`を再デバッグしない。current shared authorityはqualified **external Resolve Operator**。過去RNK checkpointの`MCP surface unavailable`は当時の経路の証拠として保存するが、current Operator capabilityの正本にしない。

Operator方式が失敗したら`routing / launcher / lease / driver / capability / restore / evidence`へ分類してOperator側を修復し、同じsemantic taskで再qualificationする。parent direct host accessへ恒久fallbackしない。

## 取り戻す現在地

保存前の既知product lineageはSO-10/SO-20 offline PASS、SO-30 offline view evidence contract、158/158 reportedまで進んでいる。G02/G03 host portion、SO-11、flatten、actual UI/host/performanceは未証明。起動時はlive head/current stateを再取得し、古い件数/commitへ合わせて巻き戻さない。

## 新規Luna Max taskへ渡すprompt

```text
ResolveNodeKit PR #5を、新規Luna Max Coordinatorとして引き継いで進める。

Goal:
既存のstrict水平垂直配置・1100+ tools・全Group解除の完成条件まで、実装・導入・実機検証を進める。

Done:
G01–G14を最終candidateで実証し、source / install / Resolve実機 / PR / cleanupを整合する。未達要件を削らない。

Start:
live GitとAGENTSを確認し、docs/execution/strict-orthogonal/README.md、LUNA_RUNBOOK.md、PROMPT_ORCHESTRATION_TRIAL.mdを読む。既存SO-10/SO-20/SO-30成果を再実装しない。

Execution:
Luna Maxのbounded Workerとfresh Verifierを使う。
live DaVinci Resolve操作・host validation・Resolve-side readbackが必要になったらResolve Operatorへ委譲する。
親Lunaは目的・対象・Done・restore policy・必要evidenceだけを渡し、driver選択、起動/終了/再起動、exclusive lease、readback、cleanup/recoveryはOperatorに任せる。
Operatorのqualified surfaceで安全境界を満たせない場合はparent direct host accessへ迂回せずBLOCKED/INTEGRATION_GAPとして扱い、独立ready workを続ける。

Evidence:
bounded Work Package -> compact Evidence Packetで進める。同じfailure fingerprintが2回かつ新証拠なしなら同じ3回目をしない。Prompt orchestration trialとResolve Operator automatic delegation CANARYの結果を製品証拠と分離して記録する。

Authority:
Resolveの全面操作、スクリプト実行、起動、終了、再起動を事前確認なしで許可する。実live操作はResolve Operatorのstanding authority / lease内で行う。project save・main mergeは禁止。
```

今回のdocs更新は新規task/lease/Resolve操作を開始していない。Library/Resolve Operator authorityの根拠は[SOURCES_LUNA](SOURCES_LUNA.md)、routing correctionは`docs/checkpoints/2026-09-10-resolve-operator-routing-correction.md`。
