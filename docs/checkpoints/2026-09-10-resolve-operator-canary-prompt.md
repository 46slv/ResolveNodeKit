# Resolve Operator CANARY prompt — 2026-09-10

Use from the new Luna Max Coordinator after live takeover is verified.

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

First live-host objective:
Resolve Operatorへcurrent RNK candidateのSO-11 host preflightを委譲する。current Resolve runtime/targetと必要snapshot capabilityをread-onlyでinventoryし、exact Resolve/version/process identity、project/timeline/comp identity、driver identity、lease、capability inventory、independent readback、final stateを返す。graph/project mutation=0、project save=0。

Evidence:
bounded Work Package -> compact Evidence Packetで進める。同じfailure fingerprintが2回かつ新証拠なしなら同じ3回目をしない。Prompt orchestration trialとResolve Operator automatic delegation CANARYの結果を製品証拠と分離して保存する。

Authority:
Resolveの全面操作、スクリプト実行、起動、終了、再起動を事前確認なしで許可する。実live操作はResolve Operatorのstanding authority / lease内で行う。project save・main mergeは禁止。
```

This prompt intentionally omits MCP names, driver choice, launch/restart sequences and lease mechanics. Those are owned by the Resolve Operator package.
