# Publication readiness audit

Date: 2026-09-08 JST  
Verdict: READY_FOR_RUNTIME_PREFLIGHT  
Scope: design/execution contract only; no new product or Resolve qualification.

## Checked and corrected before publication

1. The latest actual PR5 head was read at 562405079aa6bffa6d25668b294a26ac4142a680; product claims were taken from repository evidence, not inferred from chat.
2. The prior design and source-audit attachments were read. Both screenshot files were present and their sizes/SHA256 matched SOURCES. The original PNGs are kept in a separate source bundle, not falsely linked as repo files.
3. Source completeness is explicit: the previous source-line audit is not a whole-JSON parse or complete processing graph. The executing Worker has a first-stage parse/schema task rather than permission to fill missing edges by name.
4. Visual corrections are explicit: orthogonal style wins over the few diagonal reference segments; final output may be below the last Merge; a right aggregation tower and a single horizontal output path are not invented for unrelated graphs.
5. Scope/evidence corrections: native renderer contract, actual visual samples, full geometry readback, direct handler, actual UI event wiring and processing render/state each have distinct proof levels.
6. Host snapshot was split into SO-11. Preserve integration/stress (SO-60/70) and flatten integration/stress (SO-61/71) are separate so a flatten API gap cannot block otherwise-ready strict preserve qualification.
7. Legacy mandatory human-click waiting is replaced by an actual UI testability work package. It is not replaced by a constant HumanNeed=NO or a NO_UI-only release test.
8. Flatten remains mandatory. Primitive refusal, API limitation, empty Group, old preserve PASS and an audit that accurately reports a blocker cannot make the new flatten gate PASS.
9. Task authority allows current scoped work and Resolve restart, but not main merge, unrelated deletion, credential bypass, new spending or loss of unpreserved valuable edits.
10. Previous CURRENT_STATE and AGENTS are archived by reusing their exact Git blobs. New root pointers remove stale execution-queue ambiguity without rewriting old evidence.

## Local mechanical validation performed

12 authoring checks passed: 13 unique work packages; 14 mandatory gates with valid owners; acyclic dependencies; initial plan cannot qualify the product; omitted flatten gate rejected; cyclic dependency rejected; unknown owner rejected; required-gate demotion rejected; main merge grant rejected; blocked host cannot complete; missing evidence cannot complete; mixed candidates cannot complete; relative links resolved and two source PNG hashes verified. Some checks contain multiple assertions; this count is not a product unittest count.

The completion checks used artificial schema-only records for negative tests, not host evidence. No such artificial PASS is included in acceptance.json. All work packages/gates in the published initial state remain PENDING and execution_started=false.

## Remaining prerequisites, not hidden assumptions

SO-00 must bind actual available Sol/Worker/Verifier runtime and current Windows/Resolve access. This authoring session found no exposed DevExec runtime through plugin discovery and does not claim to launch Sol or the host. No CLI/model ID is invented.

SO-11/SO-30/SO-40/SO-50 must qualify complete host snapshot, native orthogonal view, safe native flatten and actual owned UI events early. Failure has a recovery/alternate route and cannot silently lower the completion contract. An exhausted real technical limitation can still leave an incomplete checkpoint; no document can turn an absent capability into runtime evidence.

## Learning captured

The recurring false-completion risks are now explicit contract checks: default OFF/OFF controller proof is not GUI-button proof; missing metadata is not absent graph data; legacy port-pair deduplication loses multiedges; reference image coordinates are not processing identity; no-op timings are not first-run performance proof; empty Groups cannot prove flatten preservation; moving count/old overlap=0 cannot prove all-wire strict layout. Preserve these as focused regressions in SO-10–SO-90 rather than repeatedly adding long prompts.

## AS-HANDOFF-1 — 2026-09-08追加監査

今回のユーザー提供文をこのmissionに反映し、Astra Bootstrap→Sol受領→排他所有移行→最初の着手→Astra Advisorという責任移行を追加した。新規起動と既存Solへの追補は別modeとし、timeoutやAstra中断時に二重Coordinatorを作らない。AGENTSは恒久ルールと入口だけ、可変のモデル役割/receipt/進捗はmission資料へ置いた。

実施した今回の検査: `python -m unittest discover -s docs/execution/strict-orthogonal -p test_contract.py` **30/30 PASS**、二つのchecker/test Pythonのcompileall PASS。threadだけ作成、turnだけ開始、model/plan/permission不一致、二重writer、旧epoch、着手証拠なし、Advisor権限拡張、flattenの格下げ、依存循環、bootstrapだけで製品Doneなどを拒否した。合成fixtureはruntime証拠ではなく、checkerも認証済みとは返さない。

DESIGN.md/SOURCES.mdは前publicationとbyte一致。既存13 work packages、14 required gates、profile、performance、completion条件、各PENDING状態も変更なし。新handoff_stateはNOT_STARTED、実ID/receipt/ownerなし。製品127件のsuite、Windows/Resolve host、Sol実起動は今回未実行。製品コード/installer、globalモデル設定を変更していない。

学習の保存先はHANDOFF.mdとread-only check_contract.py/test_contract.py。汎用orchestratorや新しい常駐runtimeを追加したものではない。反例を静的に検出できることと、実event/権限/leaseが成立した証明を分けた。最終受領時の実証は既存Harness/実行側が担当する。
