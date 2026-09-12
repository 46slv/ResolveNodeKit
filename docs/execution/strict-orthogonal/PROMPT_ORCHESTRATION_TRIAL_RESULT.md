# Prompt Orchestration Trial Result — RNK strict orthogonal

Status: `PARTIAL_PASS_INTEGRATION_GAP` (trial evidence, not product acceptance)

Research source: `/AI Operating Context/Coding Intelligence/CODEX_PROMPT_ORCHESTRATION_RESEARCH_2026-08-28.md`.
Resolve Operator package authority was `46slv/CodexOperations` PR #5, branch
`docs/resolve-operator-package-20260908`, head
`9958e78e382ba5a312cd0a6cc4887aaab2fe4a08` (`FIRST_USABLE: PASS`,
`FULL_QUALIFICATION: PARTIAL_PASS`).

The parent sent only the required high-level envelope: objective, target, observable
Done, restore policy, and evidence. Parent Resolve visibility and direct-host fallback
were both zero. The Operator selected its compatibility route internally, acquired the
exact live lease, returned structured evidence, and released the lease. Six bounded
launches were used: two current-target preflights, one disposable attempt that exposed
a stale installed candidate, two cleanup/recovery packages, and one requalification on
the exact installed candidate. All final lease states were `FREE`; human intervention
was zero and project save was zero.

The first disposable attempt timed out because it began before the R1 adapter install;
the recovery package independently found no owned residue. After reinstalling the
exact candidate, the next qualification created an operation-owned scratch project,
timeline, and Fusion item, but Resolve refused `GroupOperator.AddTool` and a valid
nested `Paste`. It timed out before final adapter readback; a cleanup-only Operator
package then deleted `_mcp_RNK_SO11_9b291a91` and verified its absence. This is new host
capability evidence, not a successful SO-11 qualification. The same qualification was
not attempted a third time.

The product lane also added a pure `strict_request` preparation seam: a complete
ProcessingSnapshot is converted through the existing strict planner and independently
validated before a future writer can act. It performs no host write or save; dedicated
integration tests and the canonical suite passed 28/28 and 169/169.

Product gate movement is empty. G01 is recorded `BLOCKED_TECHNICAL`; G02–G14 remain
required and are not promoted. The trial therefore supports the RNK-specific conclusion
that short-envelope automatic delegation plus lease/recovery can work, while the host
capability remains unqualified. It does not justify a permanent global routing policy.

Not collected: full parent runtime metadata, exact Worker/Verifier prompt and wall-time
instrumentation, complete nested-host adapter readback, native strict-wire qualification,
and 1100+ preserve/flatten runs. Learning Gate result: keep the short envelope, exact
installed-candidate precondition, and mechanical no-identical-third-retry guard; do not
globally promote from this single RNK case.

Machine-readable details are in [PROMPT_ORCHESTRATION_TRIAL_RESULT.json](PROMPT_ORCHESTRATION_TRIAL_RESULT.json).
