# Strict Orthogonal Arrange — 新規 Luna Max task の入口

Revision: LM-TAKEOVER-20260910-2 + PO-TRIAL-20260910-2 + RO-CANARY-20260910-1  
Authoring: READY_FOR_LOCAL_TAKEOVER / runtime takeover not executed here

## Requirements-first topology amendment — 2026-09-11

This amendment is the current execution contract for this continuation. It
supersedes the old interpretation that every Resolve operation must originate
from the external Resolve Operator. The external Operator remains the
qualified rollback/capability baseline; execution locus is selected per
requirement after a bounded capability preflight.

The order is fixed:

```text
user intent -> Requirement Brief -> capability/locality analysis
  -> direct preflight when uncertain -> minimum sufficient topology
  -> bounded work package -> evidence -> Coordinator decision
```

The Requirement Brief must state `MISSION`, `CURRENT_GOAL`, `DONE_ACCEPTANCE`,
`REQUIRED_CAPABILITIES`, `CAPABILITY_LOCALITY`, `DIRECT_PATH`,
`DELEGATED_PATH`, `BOUNDARY_LOSS_RISK`, `SAFETY_AUTHORITY`, `EVIDENCE`,
`STOP_ESCALATION`, and `MINIMUM_SUFFICIENT_TOPOLOGY`. A task is not allowed to
choose a worker merely because it mentions Resolve.

The available execution loci are:

- **D — direct guarded:** use when the product context already retains the
  required host-local capability and delegation would lose it.
- **S — dedicated Resolve Worker:** use when host work is separable and the
  worker earns the boundary through specialist operation or independent host
  evidence.
- **H — host-local executor:** use when CurrentComp, Comp Script, FlowView,
  Undo, or GUI-local state is required. Opaque host handles stay inside the
  host context and leave only detached JSON-safe evidence.

D/S/H are execution loci, not safety boundaries. Every live mutable path uses
the same Host Guard: user-wide exclusive lease, exact target identity before
write, owned disposable state, no blind retry after timeout, reversible or
discardable mutation, independent readback, cleanup/recovery, and a terminal
receipt with final lease `FREE`. `UNKNOWN` is never normalized to `PASS`.

The fresh migration readback is recorded in
`docs/checkpoints/2026-09-11-requirements-first-topology.json`: the dedicated
worker is promoted for structural fixture readback only; CurrentComp/FlowView/
Undo/GUI-local semantics remain unqualified. The external Operator is retained
unchanged as rollback baseline until a matched replacement qualifies.

### Authoring Gate AG-V2

Before each new package, the Coordinator must verify from this repository:

1. remote PR #5 head and local source/install/publication identities are fresh;
2. the PR #10/#11 source SHAs and the migration checkpoint are read;
3. exactly one shared integration writer and one live Resolve lease owner exist;
4. the selected D/S/H locus has a bounded requirement brief and a materially
   different probe from any closed failure fingerprint;
5. the package names its gate mapping, independent readback, cleanup, and
   alternate path on failure.

AG-V2 passing authorizes the next bounded package only. It does not promote a
host gate, authorize a project save, or authorize main merge.

## 今回の指示

新しいLuna MaxのCodex taskが、既存ResolveNodeKitの成果と同じPR #5を引き継ぎ、実装・導入・実機検証を進める。Astra Bootstrapをやり直さず、旧Sol thread再開を既定にせず、新規taskの実所有を正規takeoverする。新規taskは進捗初期化を意味しない。

最初にlive Git、AGENTS、CURRENT_STATE、[LUNA_RUNBOOK](LUNA_RUNBOOK.md)、[PROMPT_ORCHESTRATION_TRIAL](PROMPT_ORCHESTRATION_TRIAL.md)を読む。製品Goal/DoneはDESIGN / PLAN / acceptance.jsonを継続する。

## Resolve live host routing — corrected

live DaVinci Resolveの状態観測・操作・実機validationが必要なら、親LunaはまずRequirements BriefとHost Guardを満たす最小十分なD/S/H経路を選ぶ。external Resolve Operatorは分離host作業の既定候補およびrollback baselineであり、direct/host-localが要件上必要な場合に一律で置き換えない。

親が渡すのは原則これだけ:

```text
objective / target / observable Done / restore policy / required evidence
```

選択されたhost ownerがinventory、exclusive lease、launch/quit/restart、operation、independent readback、cleanup/recovery、final readback、lease releaseを所有する。external Operatorを使う場合も、native MCP / qualified compatibility MCP / scripting / GUIの選択を親promptへ固定しない。

Codex 0.153.4の`global MCP disabled + same-session child roleでMCP enable`を再デバッグしない。current shared authorityはHost Guardであり、qualified **external Resolve Operator**はrollback/capability baselineである。過去RNK checkpointの`MCP surface unavailable`は当時の経路の証拠として保存するが、current Operator capabilityの正本にしない。

選択経路が失敗したら`routing / launcher / lease / driver / capability / restore / evidence / boundary`へ分類し、同じfailure fingerprintを新証拠なしで再試行しない。materially differentなD/S/H経路へ切り替えるか、BLOCKED/INTEGRATION_GAPとして独立ready workを続ける。parent direct host accessへの恒久fallbackも、external Operatorの一律強制も行わない。

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
live DaVinci Resolve操作・host validation・Resolve-side readbackが必要になったら、Requirement Briefに基づきD/S/Hを選ぶ。親Lunaは目的・対象・Done・restore policy・必要evidenceだけを渡し、選択されたhost ownerにlease、readback、cleanup/recoveryを持たせる。
選択経路で安全境界を満たせない場合は同一経路を盲 retryせず、別のqualified locusをbounded probeするか、BLOCKED/INTEGRATION_GAPとして独立ready workを続ける。

Evidence:
bounded Work Package -> compact Evidence Packetで進める。同じfailure fingerprintが2回かつ新証拠なしなら同じ3回目をしない。Prompt orchestration trialとResolve Operator automatic delegation CANARYの結果を製品証拠と分離して記録する。

Authority:
Resolveの全面操作、スクリプト実行、起動、終了、再起動を事前確認なしで許可する。実live操作は選択されたHost Guard ownerのstanding authority / lease内で行う。project save・main mergeは禁止。
```

今回のdocs更新は新規task/lease/Resolve操作を開始していない。Library/Resolve Operator authorityの根拠は[SOURCES_LUNA](SOURCES_LUNA.md)、routing correctionは`docs/checkpoints/2026-09-10-resolve-operator-routing-correction.md`。
