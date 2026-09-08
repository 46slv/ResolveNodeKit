# Astra Bootstrap differential audit

Plan revision: `AS-BOOTSTRAP-20260908-1`.
Handoff ID: `RNK-SO-20260908T010727Z-01a07e8e`.
Planner thread: `01a07e8e-41f3-7d30-b190-3f621b5cdb64`.

## Read-only findings

PR #5 was OPEN/Draft at `856bf39c21e4f71f0d42499d61c86e212b6ea3e1`,
base `feat/bootstrap-nodekit-20260905`. The existing clean checkout at
`D:/Documents/ResolveNodeKit`, branch `feat/arrange-uia-e2e-20260906`,
HEAD `562405079aa6bffa6d25668b294a26ac4142a680`, is preserved. Bootstrap uses
`D:/Documents/ResolveNodeKit-strict-bootstrap-20260908` on its own task branch.
The live thread inventory (50 recent tasks plus all pinned tasks), local
worktrees, program-named processes and published handoff state showed no active
Sol owner for this mission. Older NodeKit tasks were notLoaded, not active.
No existing Sol or unrelated task was restarted or interrupted.

The planner's persisted turn metadata records `gpt-6-astra`, effort `xhigh`,
approval `never`, sandbox `danger-full-access`, cwd the original checkout.
The independent receiver will be requested as `gpt-5.6-sol` / `max`; request
values alone will not count as observed runtime configuration.

Product paths `src`, `scripts`, and `tests` are unchanged from product candidate
`59eeffbce5efd0a73a0fed2a4f3418faf71d5852`. The installed manifest still names
`5624050`; all 13 installed package files match their manifest and the original
checkout byte-for-byte, as does the installed entry. Six package files plus the
entry differ from the newly checked-out worktree only in CRLF/LF line endings
(`core.autocrlf=true`). No reinstall or product edit was performed. Do not claim
raw byte identity between those two trees; rebind installed hashes in SO-00.

The referenced environment workflow was absent under the supplied D: relative
locations and found at `C:/Users/shiro/Documents/CodexOperations/operations/ENVIRONMENT_WORKFLOW.md`.
Only the relevant environment/Git observation contract was read.

## Important assumptions and first resolving tasks

| Assumption | Evidence and confidence | First resolving task |
| --- | --- | --- |
| Complete processing snapshot | Historical large JSON explicitly reports NOT_COLLECTED_BY_HOST_ADAPTER. High confidence this is a gap, not full processing proof. | SO-10 complete schema/source audit, SO-11 host adapter; reject incomplete structural-write snapshots. |
| Native orthogonal wire display | Current design cites a historical publisher manual; target-host control, scope and all-wire guarantee are unqualified. Unknown on current context. | SO-30 installed docs/meaningful native view route, readback and same-run visual samples. |
| Nonempty nested flatten and exact restoration | Historical Resolve 21.0.3.7 callable probes and installed wrapper refusal did not flatten. High confidence refusal is not success; other native paths remain unknown. | SO-40 only after SO-11; qualify documented/identity-based operation and exact Undo. |
| Actual UI events and busy/result | Historical AskUser accessibility limitation is context-specific; direct controller proof is not UI E2E. Actual owned UI event path unqualified. | SO-50 after SO-00; qualify real Comp Script context and RNK-owned observable UI. |
| Independent persistent Sol execution | Native Codex create/read/send/wait tools are exposed; actual created thread, turn metadata, receipt, lease and first action still required. | AP-40 read-only receipt, then transfer and SO-00. |
| Exclusive Resolve access | Other unrelated Resolve-related tasks are active. Current host has not been queried by Bootstrap. | Sol/resolve_operator must bind actual host ownership; continue offline while unavailable. |

No new host probe is needed to make these bounded work packages executable.
The existing DESIGN/SOURCES, 13 tasks and 14 mandatory gates are retained. The
only normative amendment adds the user's one-hour deadline and current required
Resolve Operator routing. It does not reduce product requirements.

## Validation and handoff boundary

`python docs/execution/strict-orthogonal/check_contract.py`: consistent;
`python -m unittest discover -s docs/execution/strict-orthogonal -p test_contract.py -q`:
30/30 PASS. These are static contract tests, not authenticated runtime proof.
The historical 127 product tests and historical host passes are not reported as
new runs. All G01–G14 remain PENDING; strict product status is NOT_YET_PROVEN.

The paired JSON fixes normalized plan hashes and the requested runtime binding.
AP-40 receipt/transfer/start evidence will be separate immutable checkpoint
records. After ownership transfer only Sol updates shared execution state and
records first-action evidence. Astra independently reads those actual events
without becoming a second writer.
