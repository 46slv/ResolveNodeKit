# Prompt orchestration trial — Luna Max continuation

Revision: PO-TRIAL-20260910-1  
Mission: RNK-STRICT-ORTHOGONAL / PR #5  
Status: READY / prospective operational trial, not product evidence

## 0. Source status

User requested `/AI Operating Context/Coding Intelligence/CODEX_PROMPT_ORCHESTRATION_RESEARCH_2026-08-28.md` as the research basis and wants the continuation itself to serve as a test.

ChatGPT Library search in the authoring session did **not** return that exact filename. The closest same-date current source that was retrievable was `CODEX_PROMPT_AUTHORING_LUNA_FIRST_REFERENCE.md` (2026-08-28), plus the current `CODEX_OPERATIONS_INDEX.md` and `CODEX_ORCHESTRATION.md`. Do not claim the retrievable file is byte-identical to the requested research file.

Therefore the trial begins with a source-retrieval check:

1. New Luna task attempts to read the requested exact Library path if its environment exposes it.
2. If exact content is available, record path/version/hash and use it as the primary research source.
3. If unavailable, record `EXACT_RESEARCH_SOURCE=UNAVAILABLE` and use the retrievable same-date prompt-authoring reference as the fallback operational source. This is not a blocker for product work.
4. If the exact source later becomes available, compare it with the fallback and record only decision-relevant deltas before changing the trial.

## 1. What is being tested

The research/reference proposes that prompt/orchestration quality comes primarily from **short task contracts + durable repo knowledge + bounded Work Packages + compact Evidence Packets**, not from repeatedly sending project-wide prompts.

This continuation tests the following hypotheses without weakening any product gate:

- **H1 — Short top-level prompt is sufficient.** The user-facing/new-task prompt contains only Goal/Done/Constraints/Start/Evidence. Durable rules stay in AGENTS/docs/Skill/Harness.
- **H2 — Bounded Work Packages improve execution clarity.** Each Worker receives one coherent outcome with owned scope, explicit validation, and return schema. No project transcript dump.
- **H3 — Compact Evidence Packets are sufficient for coordination.** Worker returns only current state, changed surface, verified behavior, tests/host evidence, exact blocker/fingerprint, and next bounded decision.
- **H4 — Routine work stays with Luna.** Repository read, implementation, debugging, tests and host checks remain Luna work. Stronger-model consultation is not sticky.
- **H5 — Escalation is evidence-triggered, not frustration-triggered.** If the **same failure fingerprint** occurs twice with **no new evidence**, do not blindly perform the third same attempt. Change route or, if a higher-level ambiguity genuinely remains and an authorized Sol advisor lane is available, use one bounded Sol diagnostic/adjudication turn, then return implementation to Luna.
- **H6 — Important repeated rules should migrate to mechanical enforcement.** A verified recurring defect should become a test/validator/Skill/Harness guard where appropriate, not another permanent prompt paragraph.

### Explicit deviation under test

The accessible 2026-08-28 reference's standard preference is `Sol supervisor -> Luna worker`. The current user instruction instead requests a **new Luna Max Coordinator**. This trial intentionally keeps Luna Max as Coordinator and Worker/Verifier family, while retaining only the research's **conditional, non-sticky Sol escalation rule**. This is a project-specific experiment, not a claim that the source recommends Luna-only coordination.

## 2. Trial invariants

The experiment is secondary to product truth. It may not:

- change G01–G14, product Done, authority, no-save, no-main-merge, exclusive host ownership, or processing-preservation rules;
- relabel a host blocker as PASS;
- force a Sol escalation merely to generate experiment data;
- keep Sol as implementer after a bounded consultation;
- re-run a harmful/ambiguous write just to count attempts;
- make prompts artificially tiny by omitting necessary references or validation;
- make prompts artificially long to improve the comparison baseline.

Current/live repo, runtime, tests and host evidence outrank Library research.

## 3. Work Package schema

Every delegated Luna Worker packet should fit this shape unless the task genuinely needs less:

```text
Task: <single coherent outcome>
Owned: <files/subsystem/worktree or host lane>
Read/Start: <1-4 authoritative references>
Do: <necessary actions>
Do not: <only task-relevant hard boundaries>
Validation: <observable checks>
Return: <Evidence Packet fields>
```

Do not include the Coordinator transcript, old successful cycles, generic coding rules, full PLAN text, or raw host logs when references are enough.

## 4. Evidence Packet schema

Worker/Verifier returns:

```text
TASK
STATE
CHANGED
VERIFIED
TESTS
HOST_EVIDENCE
REMAINING
BLOCKER
FAILURE_FINGERPRINT
ATTEMPT_COUNT
NEXT_DECISION
```

Raw transcripts are artifacts, not the packet itself.

## 5. Trial instrumentation

For each meaningful Work Package, append a compact record under a task-owned local evidence file/checkpoint with:

- package id and goal;
- Coordinator model/context id and Worker/Verifier context ids when available;
- top-level task prompt bytes/chars if measurable;
- references read count;
- Work Package bytes/chars if measurable;
- Evidence Packet bytes/chars if measurable;
- wall time if available;
- changed files count;
- tests/host result;
- failure fingerprint and attempt count;
- escalation event: none / changed-route-Luna / Sol-diagnostic / human;
- human intervention count;
- meaningful new evidence produced: yes/no;
- resulting product task/gate movement.

Do not fabricate metrics when the harness does not expose them. Use `NOT_COLLECTED`.

### Minimum trial sample

Use at least **three real Work Packages** if the mission runs long enough:

1. a host/operator recovery or complete snapshot package;
2. a product implementation/integration package;
3. an independent verification/host qualification package.

If the product completes or reaches a genuine stop before three packages, preserve the smaller sample and do not create fake work.

## 6. First Work Package for this continuation

The first useful package should attack the current host boundary, not reimplement the already-passed offline planner.

```text
Task: Restore the qualified resolve_operator tool path far enough to prove one read-only Resolve identity call for the current RNK candidate.

Owned: resolve_operator binding/session/tool-visibility diagnosis and its run-scoped evidence. Product files remain read-only unless an evidence-contract defect is actually found.

Read/Start:
- docs/execution/strict-orthogonal/LUNA_RUNBOOK.md §4
- docs/checkpoints/2026-09-08-luna-host-recheck.json
- current personal resolve-operator Skill/config actually loaded by the new operator
- current PR #5 / live Git state

Do:
- distinguish lease ownership, MCP tool exposure, transport connection, and host responsiveness;
- inspect the actual child/operator role binding and tool list;
- repair only the smallest current task/agent-local binding/configuration surface allowed by the Skill;
- acquire the exclusive lease with exact PID/start identity;
- when and only when the callable surface exists, perform one short read-only identity/getter call and record project/timeline/comp plus process/runtime identity;
- release/retain the lease exactly according to the operation boundary and record final state.

Do not:
- enable Resolve MCP directly on the parent Coordinator;
- bypass the dedicated Operator or lease;
- restart Resolve merely to fix tool visibility before proving the failure is host-side;
- mutate product graph/project or save the project;
- repeat the same unavailable-tool route more than once without new evidence;
- rewrite global agent/MCP policy broadly to make this test pass.

Validation:
- actual operator identity and effective model/capability binding recorded;
- lease HELD readback with exact owner identity;
- davinci-resolve callable tool list observed;
- one read-only host call returns current runtime/target identity;
- zero graph/project mutation and zero save;
- final lease/host state explicit.

Return:
- compact Evidence Packet from §4;
- exact failure fingerprint if not PASS;
- whether next route is SO-11 host snapshot, task-local operator binding repair, or technical stop.
```

## 7. Escalation experiment

Track failure by semantic fingerprint, not just error text. Different failures such as `LEASE_BUSY`, `MCP_TOOL_NOT_EXPOSED`, `MCP_DISCONNECTED`, `HOST_GETTER_TIMEOUT`, and `HOST_API_ABSENT` are not one counter.

When the same fingerprint repeats:

- attempt 1: ordinary Luna diagnosis/repair;
- attempt 2: Luna must use a materially different distinguishing probe or route and state what new evidence is expected;
- if attempt 2 yields no new evidence: do **not** run the same third attempt;
- choose a different safe route. If the remaining problem is architectural/acceptance ambiguity rather than a simple capability repair, and an authorized Sol diagnostic lane exists, send one compact Evidence Packet + one question to Sol;
- after the decision, return implementation/verification to Luna. Sol does not keep the Worker role.

If Sol is not available, use a fresh Luna diagnosis context rather than stopping solely because the research preferred a supervisor.

## 8. Trial result and Learning Gate

At a meaningful milestone or mission close, write `PROMPT_ORCHESTRATION_TRIAL_RESULT.{md,json}` containing:

- exact research source used (requested exact file vs fallback);
- sample Work Packages and Evidence Packet sizes/refs where measurable;
- completion/gate movement;
- same-fingerprint retries and route changes;
- Sol escalation count and whether it was useful;
- human interventions;
- false-completion/duplicate-work incidents;
- what was NOT measured;
- source-supported conclusions vs project-specific inference.

Do not infer causality from one project. Record this as a bounded field test.

Run the Mandatory Learning Gate before closeout. If a reusable finding is verified, prefer a test/validator/Skill/Harness or the existing CodexOperations owner over adding more RNK-specific prose. If there is no reusable delta, record `NO_REUSABLE_DELTA` in the trial result.
