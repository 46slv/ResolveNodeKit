# Semantic Arrange v1 — continuation plan

Status: READY / amended by `AMENDMENT_2026-09-08_LARGE_FLATTEN.md`
Updated: 2026-09-08 JST
Mission owner: ResolveNodeKit / Semantic Arrange v1
Runtime state owner: `docs/CURRENT_STATE.md`
Recovery / authority owner: `docs/execution/semantic-arrange-v1/RUNBOOK.md`

## 0. Starting point

Fresh remote state at plan authoring:

- repo: `46slv/ResolveNodeKit`
- accepted continuation branch: `feat/arrange-uia-e2e-20260906`
- accepted continuation HEAD at plan authoring: `8634b209ceef28c280d339ba80b6bef34e66c60c`
- PR #5 branch: `feat/semantic-arrange-v1-20260906`
- PR #5 remote HEAD at plan authoring: `bf42239bbdca6903db2a48e38c01293ca32c7bf1`
- whole-comp FIRST_USABLE contract: `ArrangeDialogState(include_unselected=True, ungroup=False)`
- whole-comp host smoke evidence: `docs/checkpoints/2026-09-07-semantic-arrange-whole-comp-host-smoke.{md,json}`
- measured host: Resolve Studio 21.0.3.7
- current known valuable host baseline after accepted smoke: `PSD2Fusion / Timeline 1 / Fusion`, 967 tools, `COMPB_Modified=false`, no RNK disposable remnants, no save

This plan is not the runtime state ledger. Before every task, fresh-read local Git/worktree, remote refs, `docs/CURRENT_STATE.md`, and live Resolve state as applicable.

The dated large-flatten amendment is the latest user direction.  It
supersedes the older optional-Ungroup and transport-only completion clauses
below wherever they conflict; the preserve-mode FIRST_USABLE contract remains
the regression baseline.

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
- PSD2Fusion-scale whole-comp preserve evidence is completed with a bounded
  production execution and compact signatures;
- safe flatten-all is implemented behind an explicit host primitive and is
  host-proven on nested small and >=1100-tool disposable fixtures, or a
  specific host API blocker is checkpointed without weakening the preserve
  baseline;
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
| Large PSD2Fusion-scale preserve stress | false | true | `SAV1-60R` host PASS at 977 and 1110 tools; processing hash status remains explicit |
| Flatten-all small / nested / large | false | true | Required by the dated amendment; current Resolve host lacks a measured identity-preserving Ungroup primitive |
| Busy stage UI | false | false | `UIDispatcher` unavailable on measured direct host path; feature-local blocker |
| AskUser semantic UI automation | false | false | `BLOCKED_HOST_ACCESSIBILITY_HARD`; closed capability investigation |
| Selection-only fixed-obstacle behavior | false | false | Experimental/regression lane; not a release blocker |
| Ungroup / flatten-all mode | false | true | Explicit primitive + exact structural readback/Undo required; current host is fail-closed and UI is not exposed |
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
            -> SAV1-55 flatten capability + small proof
                 -> SAV1-56 nested flatten correctness
            -> SAV1-60R large preserve optimization / host PASS
                 -> SAV1-65 large flatten-all stress
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
| **SAV1-55 — implement safe flatten-all on small fixture** | SAV1-40 + amendment | Worker + Host Worker; code/tests plus disposable nested fixture | explicit host primitive only; full snapshot; all eligible Groups removed; non-Group identity/processing/edges accounted for; semantic Arrange; one owned Undo; exact rollback; no guessed UI/delete-recreate path | If no measured primitive exists, keep the code fail-closed and record the exact host API blocker; do not expose a checkbox |
| **SAV1-56 — nested/recursive flatten correctness** | SAV1-55 | Host Worker on disposable nested fixture | deterministic deepest-first (or measured equivalent), crossing boundaries preserved, exact topology/Undo, run2 `moved=0` | Same host API blocker remains feature-local; preserve and large-preserve lanes continue |
| **SAV1-60R — optimized PSD2Fusion-scale preserve stress** | SAV1-50 + candidate identity fixed | Host Worker; disposable duplicate / exact owned fixture | compact stage timings for bind through Undo close; installed production seam completes at ~967 and >=1100 tools; first run moves, run2 `moved=0`, structural hashes exact, endpoint stays healthy, Undo exact where exercised; no save/cleanup exact | Adapt product execution and evidence route; do not replay the old oversized call |
| **SAV1-65 — large flatten-all stress** | SAV1-55 + SAV1-56 + SAV1-60R | Host Worker; largest safe disposable + >=1100 fixture | `group_count_post=0`, non-Group identity preserved, connections/processing evidence accounted for, overlap-free Arrange, exact grouped Undo restoration, run2 stable, endpoint healthy, no save | Stop only at a specific host primitive/Undo/restoration blocker after bounded alternatives; do not mark PASS from transport alone |
| **SAV1-70 — docs / PR reconciliation** | SAV1-20 and all completed host gates | Integration writer; docs + PR #5 metadata | all feature docs describe preserve PASS, large-preserve evidence, flatten implementation and exact host blocker/PASS, processing evidence status, accessibility/busy limitations, latest candidate SHA and cleanup; amendment precedence is explicit | Do not lower a required gate to optional. Record exact blocker/resume condition and preserve FIRST_USABLE vs PROGRAM_STATUS distinction |
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
5. PSD2Fusion-scale whole-comp preserve stress passes compact structural evidence and stable second run; the amended flatten-all small/nested/large gates are either host-PASS or carry a specific measured host API blocker without fabricating a PASS.
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
- guessed/UI-driven ungroup implementation; flatten-all is allowed only through the dated amendment's explicit host primitive and rollback gates;
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

The first execution task was `SAV1-00`; after the amended continuation evidence,
the smallest next task is `SAV1-70` documentation/PR reconciliation followed by
`SAV1-80` fresh independent verification.  `SAV1-65` remains unpassed when the
host cannot expose an identity-preserving primitive.

The executor should continue through every ready task without returning for routine approval. Human interaction is reserved for `SAV1-90` or a true authority/safety boundary defined in the RUNBOOK.
