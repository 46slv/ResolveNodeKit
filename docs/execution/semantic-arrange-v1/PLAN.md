# Semantic Arrange v1 — continuation plan

Status: READY
Updated: 2026-09-08 JST
Mission owner: ResolveNodeKit / Semantic Arrange v1
Runtime state owner: `docs/CURRENT_STATE.md`
Recovery / authority owner: `docs/execution/semantic-arrange-v1/RUNBOOK.md`

## 0. Starting point

Fresh remote state at plan authoring:

- repo: `46slv/ResolveNodeKit`
- accepted continuation branch: `feat/arrange-uia-e2e-20260906`
- accepted continuation HEAD: `8634b209ceef28c280d339ba80b6bef34e66c60c`
- PR #5 branch: `feat/semantic-arrange-v1-20260906`
- PR #5 remote HEAD at plan authoring: `bf42239bbdca6903db2a48e38c01293ca32c7bf1`
- whole-comp FIRST_USABLE contract: `ArrangeDialogState(include_unselected=True, ungroup=False)`
- whole-comp host smoke evidence: `docs/checkpoints/2026-09-07-semantic-arrange-whole-comp-host-smoke.{md,json}`
- measured host: Resolve Studio 21.0.3.7
- current known valuable host baseline after accepted smoke: `PSD2Fusion / Timeline 1 / Fusion`, 967 tools, `COMPB_Modified=false`, no RNK disposable remnants, no save

This plan is not the runtime state ledger. Before every task, fresh-read local Git/worktree, remote refs, `docs/CURRENT_STATE.md`, and live Resolve state as applicable.

## 1. Mission outcome

Bring the accepted whole-comp Semantic Arrange v1 preserve-mode implementation onto the PR #5 candidate branch and close the remaining release-candidate evidence that can be obtained autonomously.

Target user flow:

```text
Workspace -> Scripts -> Comp -> ResolveNodeKit_Arrange
-> whole active Fusion composition is the arrangement scope
-> existing GroupOperators are preserved
-> semantic whole-comp layout is applied
-> connections/tool identity/processing structure remain unchanged
-> Undo restores the exact pre-layout state
-> second identical run is stable (`moved=0` / identical position signature)
```

Target delivery state:

- PR #5 branch contains the accepted whole-comp production seam, tests, docs, installer state, and evidence references;
- PR #5 candidate is reinstallable and host-smoked;
- PSD2Fusion-scale large-host evidence is completed with transport-fitting compact signatures, or a narrow host/transport blocker is checkpointed without invalidating the already-passed FIRST_USABLE small-host path;
- no merge to `main`;
- human release smoke is deferred until all autonomous gates are complete and is at most one final action.

## 2. Scope classification

| Capability | required_for_first_usable | required_for_this_mission_done | Current interpretation |
|---|---:|---:|---|
| Whole active comp scope, preserve mode | true | true | Host-PASS on continuation branch |
| Connection/tool identity preservation | true | true | Host-PASS on continuation branch |
| Undo exact | true | true | Host-PASS on continuation branch |
| Second run stable / `moved=0` | true | true | Host-PASS on continuation branch |
| PR #5 integration + reinstall + host smoke | false | true | Pending |
| Non-empty nested Group revalidation on integrated candidate | true by product contract | true | Prior host proof exists; same-candidate revalidation preferred |
| Large PSD2Fusion-scale stress | false | true | Pending; transport-limited historically |
| Busy stage UI | false | false | `UIDispatcher` unavailable on measured direct host path; feature-local blocker |
| AskUser semantic UI automation | false | false | `BLOCKED_HOST_ACCESSIBILITY_HARD`; closed capability investigation |
| Selection-only fixed-obstacle behavior | false | false | Experimental/regression lane; not a release blocker |
| Ungroup mode | false | false | Fail-closed; not exposed by FIRST_USABLE UI |
| Runtime visual Group expansion / fit-to-contents | false for this mission | true for overall ResolveNodeKit mission | Separate program lane; does not block this Semantic Arrange candidate |

`PROGRAM_STATUS`, `FIRST_USABLE`, and this mission's candidate-completion state must remain separate.

## 3. Progress route

```text
SAV1-00 reconcile live refs
  -> SAV1-10 integrate accepted continuation into PR #5
  -> SAV1-20 integrated offline/install verification
  -> SAV1-30 small integrated host smoke
       -> SAV1-40 nested non-empty Group evidence
       -> SAV1-50 large-host transport envelope
            -> SAV1-60 PSD2Fusion-scale whole-comp stress
  -> SAV1-70 docs / PR / evidence reconciliation
  -> SAV1-80 fresh independent verification
  -> SAV1-90 conditional one-click human release smoke
```

Independent feature-local lanes such as busy UI or accessibility must not stop ready core tasks.

## 4. Task table

| ID / outcome | depends_on / ready_when | owner / write_scope | done_when / evidence | on_fail / resume_when |
|---|---|---|---|---|
| **SAV1-00 — reconcile live authority** | Start | Coordinator; read broadly, no mutation until identity is clear | local branch/worktree, remote continuation HEAD, PR #5 HEAD/body, current tests, installed tree, live Resolve project/timeline/comp are fresh-read; unrelated dirty work preserved | Preserve unknown local work before branch operations. If refs conflict, checkpoint and choose a non-destructive reconciliation path; no `reset --hard` / force push |
| **SAV1-10 — integrate accepted whole-comp continuation into PR #5** | SAV1-00 | Single integration writer; `feat/semantic-arrange-v1-20260906` and task docs only | accepted continuation changes through the fresh source HEAD are incorporated non-destructively; PR #5 branch contains production seam, whole-comp defaults/UI, verifier/harness changes, docs/checkpoints; no unrelated regressions | Resolve conflicts by preserving PR #5 design work and accepted continuation behavior. No history rewrite. If ownership is ambiguous, checkpoint before editing |
| **SAV1-20 — integrated offline/install qualification** | SAV1-10 | Worker; code/tests/install/docs on candidate | full unit suite PASS at or above current baseline, `compileall` PASS, `git diff --check` PASS; per-user reinstall succeeds; installed entry/package/manifest hashes correspond to integrated candidate; Resolve-side import/read-only sanity succeeds | Diagnose and fix within mission scope. If host install path unavailable, finish offline qualification and mark host subgate waiting; do not call candidate host-accepted |
| **SAV1-30 — small integrated whole-comp host smoke** | SAV1-20 + healthy endpoint | Host Worker on disposable fixture only | exact current target bind; whole-comp OFF-selection semantics (`include_unselected=True`, `ungroup=False`); first run moves expected tools; connection/membership/tool identity invariant; Undo exact; second run `moved=0`; no save; exact cleanup; final valuable host restored | On scripting endpoint hang, one bounded read-only sanity then one authorized exact Resolve/fuscript restart path from RUNBOOK. Do not repeat known `LoadComp/Paste` timeout route |
| **SAV1-40 — nested non-empty Group evidence on candidate** | SAV1-30 | Host Worker; proven nested-fixture route only | at least one GroupOperator with real child membership is exercised on the integrated candidate; Group remains GroupOperator; direct parent/child membership and connections unchanged; recursive local layout stable; Undo exact; run2 stable | Prefer the previously host-proven nested fixture recipe. Do not invent/repeat the banned hand-written single-Paste route. If fixture generation is unavailable, carry prior host evidence only when relevant recursion code is unchanged and record `CARRIED_EVIDENCE`; otherwise keep this task open |
| **SAV1-50 — establish large-host transport envelope** | SAV1-30 | Coordinator + Host Worker; evidence tooling may be added under `scripts/host`/tests | medium/bounded graph probes establish safe call size/time; compact in-host counts/hashes are returned using `docs/EVIDENCE_PROTOCOL.md`; no whole-graph payload; envelope and timing recorded | Same materially unchanged timeout may be retried at most once. Then change payload/chunk/aggregation strategy. A transport blocker is local unless product mutation itself is disproven |
| **SAV1-60 — PSD2Fusion-scale whole-comp stress** | SAV1-50 + candidate identity fixed | Host Worker; disposable duplicate / exact owned fixture, never valuable original | pre evidence includes target identity, tool/group counts, membership hash, connection hash, processing evidence status, position hash; production whole-comp Arrange runs; required hashes stay unchanged; intended position hash changes first run; second run position hash identical / `moved=0`; overlap diagnostics accepted; Undo/rollback evidence obtained where contract requires; bounded runtime; exact cleanup; no save | If evidence transport fails, shrink/chunk evidence without changing product semantics. If product mutation fails, rollback/stop writes and localize mismatch only. Do not dump 1000+ node rows through MCP |
| **SAV1-70 — docs / PR reconciliation** | SAV1-20 and all completed host gates | Integration writer; docs + PR #5 metadata | `SEMANTIC_LAYOUT.md`, `SEMANTIC_LAYOUT_ACCEPTANCE.md`, `ARRANGE_DIALOG.md`, `CURRENT_STATE.md`, relevant checkpoints and PR #5 describe whole-comp preserve-mode accurately; selection-only marked experimental; Ungroup fail-closed/not exposed; accessibility/busy limitations narrow; latest tests/evidence/candidate SHA referenced | Do not lower a required gate to optional merely because it failed. Record exact blocker/resume condition and preserve FIRST_USABLE vs PROGRAM_STATUS distinction |
| **SAV1-80 — fresh independent verifier** | SAV1-70 | Fresh verifier context; read-only on candidate except disposable host actions explicitly required | verifier independently checks candidate SHA, diff scope, tests, installer hashes, evidence consistency, required host gates, final host state, and PR readiness; it does not fix its own candidate during verification | On FAIL, return issue to a Worker, produce new candidate/evidence, then run a fresh verifier again. Verifier PASS is not main merge authority |
| **SAV1-90 — conditional human release smoke** | SAV1-80 PASS and only if UI shell remains unautomatable | User at machine; one normal product invocation | user performs one real `Workspace -> Scripts -> Comp -> ResolveNodeKit_Arrange -> Run` on a safe target; setup UI appears and whole-comp result matches the accepted contract; run log makes any failure diagnosable in one attempt | Do not ask early. If automated installed-entry proof becomes sufficient under the repo contract, Coordinator may mark this `NOT_REQUIRED` with evidence. Otherwise return exactly one smoke instruction and resume point |

## 5. Large-host acceptance contract

Large-host work must follow `docs/EVIDENCE_PROTOCOL.md`.

Required compact evidence:

```text
schema/version
target project/timeline/comp identity
Resolve/Fusion version
tool_count
group_count
max_group_depth
identity_status
membership_hash
connection_hash
processing_hash_status or documented sampling
position_hash
quantization/tolerance policy
duplicate_position_summary / overlap diagnostics
first_run_moved
second_run_moved or second_position_hash
elapsed_ms / chunk timings
mismatches[]
```

Rules:

- compute canonical signatures in-host whenever practical;
- return counts/hashes/timings, not every node row;
- expand only mismatching categories;
- the known full ~1100-tool one-call evidence walk must not be repeated materially unchanged;
- a transport failure is not product failure unless product behavior itself is disproven.

## 6. Acceptance for this mission

This mission is complete when all items below are true or explicitly classified by this contract:

1. PR #5 branch contains the accepted whole-comp production implementation and continuation evidence.
2. Integrated candidate passes the complete offline/install qualification.
3. Integrated candidate passes a small real-host whole-comp preserve smoke with exact Undo and stable run2.
4. Nested non-empty Group behavior is fresh-host proven on the candidate, or prior proof is explicitly carried only under unchanged relevant recursion code with justification.
5. PSD2Fusion-scale whole-comp stress passes compact structural evidence and stable second run; if only evidence transport remains blocked after the bounded adaptation budget, candidate status must say so and must not fabricate a PASS.
6. Final Resolve state is read back and safe: valuable project/timeline restored, `COMPB_Modified=false`, no RNK disposable remnants, no project save.
7. PR #5 docs/body and current state are consistent with the actual candidate/evidence.
8. Fresh independent verifier accepts the candidate.
9. `main` is not merged.

### Candidate state wording

Preferred final wording when all autonomous gates pass:

```text
PROGRAM_STATUS: CHECKPOINTED
SEMANTIC_ARRANGE_STATUS: RELEASE_CANDIDATE
FIRST_USABLE: PASS
NORMAL_DEV_HUMAN_CLICK_REQUIRED: NO
RELEASE_SMOKE_HUMAN_CLICK_REQUIRED: YES|NO
```

Overall `MISSION_COMPLETE` remains reserved for the broader ResolveNodeKit program and is not granted by this plan while runtime visual nested-group expansion remains unresolved.

## 7. Non-goals for this continuation

Do not expand this mission into:

- merge to `main` or release publication;
- fixing Resolve's UIA/MSAA accessibility provider;
- selection-only fixed-obstacle redesign;
- automatic ungroup implementation unless separately authorized as a later feature;
- visual Group expand/collapse or fit-to-contents completion;
- Color-page feature work;
- generic repo-wide refactoring unrelated to the acceptance path.

These may remain ready follow-up lanes after this mission checkpoint.

## 8. Evidence / checkpoint discipline

After each meaningful host phase:

- record exact candidate SHA and host identity;
- store compact machine-readable evidence under the existing checkpoint/evidence convention;
- update `docs/CURRENT_STATE.md` rather than maintaining a second runtime-state ledger here;
- commit/push accepted task-branch changes when safe;
- update PR #5 only after the corresponding branch state exists remotely;
- always read back the pushed ref/content before claiming publication.

Worker narration, exit code alone, or offline mocks are not sufficient host evidence.

## 9. Ready next

The first execution task is `SAV1-00`, immediately followed by `SAV1-10` if live refs match the authored starting point.

The executor should continue through every ready task without returning for routine approval. Human interaction is reserved for `SAV1-90` or a true authority/safety boundary defined in the RUNBOOK.
