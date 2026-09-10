# ResolveNodeKit current continuation

Updated: 2026-09-11 JST. Live Git/PR/installed/runtime evidence always outranks this locator.

## Active goal

RNK-STRICT-ORTHOGONAL: reference-guided horizontal/vertical whole-comp layout, actual orthogonal wire display, safe flatten-all, and automated installed-user-flow qualification at 1100+ non-Group tools.

Entry: [strict continuation](execution/strict-orthogonal/README.md). Initial route: Astra Bootstrap → HANDOFF receipt/ownership/start proof → Sol SO-00 and ready independent packages through SO-90. Read DESIGN/SOURCES/PLAN/RUNBOOK/acceptance.json from that entry. If Sol is already active, preserve its lease and use amendment receipt instead of creating another Coordinator. Do not use the old appended ready queues as the execution plan.

## Git authority

Canonical integration branch: `feat/semantic-arrange-v1-20260906`, PR #5 OPEN/Draft, based on `feat/bootstrap-nodekit-20260905`. The last host-evidenced product candidate remains `eedd62e4265a6ddc8a7d291a3e72f1987f1b5b79`; the new offline-only successor is `8e540e67fe2a95c2dc521f8bdaedef56e2419fa0` (publication/docs head `e174424`). Prior publication locator was `17aa6f1783418a1810f58163e3a04874ab27182f`. Earlier product/design evidence remains historical and is not silently promoted to the successor. Read the actual new remote HEAD before work. Older task branch `feat/arrange-uia-e2e-20260906` may hold local work: preserve and reconcile it, never reset blindly. main merge/release remains unauthorized.

AS-HANDOFF-1 updates execution design and a read-only contract checker. Product source/installer and live host are not changed or retested. Existing product evidence is not reset or promoted by this publication.

## Baseline evidence, not new strict qualification

- Existing whole-comp preserve: historical FIRST_USABLE PASS.
- Large preserve: 977/1110 tools, second run moved=0, about17s and structure/Undo checks; see [large checkpoint](checkpoints/2026-09-08-semantic-arrange-v1-large-preserve-optimized.json).
- Offline suite at baseline: reported127/127, compile/install checks PASS. Not rerun during this design publication.
- Actual flatten: BLOCKED_HOST_API on measured callable surface; zero-write refusal is not success.
- Complete processing hash: NOT_COLLECTED_BY_HOST_ADAPTER.
- AskUser UIA/MSAA identity: historical hard limitation; do not repeat unchanged probes.
- UIDispatcher absence: observed in the direct scripting context, not proven across every Comp Script/UI context.
- Historical final host: PSD2Fusion / Timeline1 / Fusion, 967 tools, Modified=false, no-save/cleanup reported. Current host is NOT_OBSERVED_THIS_AUTHORING_RUN; fresh identity/baseline required.

## New status

Plan: CHECKPOINTED_WITH_TECHNICAL_GAP at product candidate `eedd62e`. Sol handoff is
EXECUTION_CONFIRMED at program owner epoch 1. SO-10 and SO-20 are offline PASS;
SO-11/G01 now have a qualified standalone nested-fixture host snapshot PASS;
G02 and G03 remain BLOCKED_TECHNICAL because their host portions are unproven.
SO-00, SO-30, SO-50 and all downstream host gates retain technical gaps.
Strict/flatten/installed-UI product acceptance remains NOT_YET_PROVEN. See the
[execution checkpoint](checkpoints/2026-09-08-astra-sol-execution.json) and
[deadline handoff](checkpoints/2026-09-08-sol-deadline-handoff.json), plus the
[Luna SO-20 checkpoint](checkpoints/2026-09-08-luna-so20-offline.json) and
[Luna SO-30 checkpoint](checkpoints/2026-09-08-luna-so30-offline.json).

The earlier long current-state document is preserved byte-for-byte at [pre-strict archive](checkpoints/2026-09-08-pre-strict-current-state.md); previous AGENTS at [instruction archive](checkpoints/2026-09-08-pre-strict-AGENTS.md). Read historical sections only for relevant evidence.

## Live Bootstrap — 2026-09-08 10:07 JST invocation

`AS-BOOTSTRAP-20260908-1` / handoff `RNK-SO-20260908T010727Z-01a07e8e`:
EXECUTION_CONFIRMED, corrected receiver owns epoch 1 and SO-00 has started. Differential
audit and normalized plan hashes are in
[Bootstrap checkpoint](checkpoints/2026-09-08-astra-sol-bootstrap.md) and its JSON.
The old checkout is preserved. Product source is unchanged; all G01–G14 remain
PENDING. The current invocation deadline, including Sol continuation, is
2026-09-08 11:07:27 JST. RUNBOOK section 9 records the user grant and required
Resolve Operator route. On receipt/transfer Sol becomes the only progress writer.

Sol thread `01a07e95-b55e-70a1-8366-b80d785bbaa4` / corrected receipt turn
`01a07ea1-c26e-7940-b8d5-2ca970191cd8` is authenticated as
`gpt-5.6-sol/max`, approval `never`, sandbox `danger-full-access`, cwd
`C:/Users/shiro/.codex/worktrees/c22a/ResolveNodeKit`. The native creation mismatch
was repaired through the same persisted thread, with its idle App writer released
by archive/restore before CLI resume. No second Sol exists and global config is
unchanged. The updated Resolve Operator instruction hash was explicitly accepted.

See [verified receipt](checkpoints/2026-09-08-astra-sol-receipt.json) and
[runtime events](checkpoints/2026-09-08-astra-sol-receiver-runtime.json).
Plan digest is `ebc124049dbb1dfa863cd499c13c2cd1a232774ae754a26edc30ee14668dbc20`.
The durable program lease at
`D:/Documents/ResolveNodeKit/.git/rnk-strict-orthogonal-owner.json` completed its
single CAS from Astra/epoch0 to Sol/epoch1 with the old writer fenced. Sol is the
only shared state/integration writer. This transition promotes no product gate.

## Luna execution continuation — 2026-09-08 14:56 JST

The same persisted Coordinator thread resumed as `gpt-5.6-luna/max` under the
unchanged owner epoch 1 and canonical worktree. The SO-20 candidate was
independently reviewed against the current strict contracts, then hardened and
published as the SO-20 product candidate `d7a1610`: exact port-labelled multiedges,
role/continuity separation, recursive bounds, rectangle validation, explicit
SO-10 state mapping, fail-closed omitted coverage, O01–O18 coverage split, and
1101-node/29-group offline stress are covered by 146/146 canonical tests.
Resolve was not queried in this lane. The prior dedicated operator acquired and
released its exact lease but had no callable `davinci-resolve` MCP surface, so
host identity and G02 host evidence remain unobserved.

## Luna SO-30 offline continuation — 2026-09-08 15:15 JST

The pure view-realization seam was independently reviewed and published as
product candidate `dd0069a`. It requires an explicit contract schema, native mode
raw value/name/source/scope, same-run pre/post/restored stages, canonical
port-complete edge IDs, endpoint port positions with directional roles, node/group
rectangles, per-edge coverage and sample linkage, mask/boundary/multiedge/all-edge
coverage, an overview plus difficult-region zoom, and JSON-safe output. Focused
view tests are 12/12 and the canonical suite is 158/158, with compile/import and
diff checks passing. This is host-agnostic evidence normalization only; no Resolve
API or runtime call was made. SO-30 and G03 therefore remain BLOCKED_TECHNICAL
until the dedicated Resolve Operator can observe and qualify the installed native
renderer on the exact target view. The latest exact host lease was released and
the runtime surface was unavailable (`docs/checkpoints/2026-09-08-luna-host-recheck.json`).

## Scope boundary (unchanged)

Strict Arrange preserve/flatten is the current completion target. Runtime Group-preserving expansion/fit-to-contents, Color work and generic helpers remain separate unresolved/product lanes where applicable. Do not claim wider MISSION_COMPLETE from this milestone.

## New Luna Max takeover — 2026-09-10

The prior Sol owner was fresh-read as quiescent: its task readback is `notLoaded`, its recorded process IDs are absent, the durable owner lock is acquirable, and its 2026-09-08 deadline is expired. A mechanical CAS transferred the owner record to the current Luna task `01a087e9-0cb8-77f3-908d-e0163103ac50` at epoch 2, with `old_writer_fenced=true`. The immutable Sol receipt and epoch 1 remain historical; they were not overwritten. Evidence is in `docs/checkpoints/2026-09-10-luna-takeover.json` and the external owner record.

The canonical worktree was fast-forwarded to remote PR #5 head `c590d8d7e617be76b44ad577cebd89082369f3fe`; the current R1 product source candidate is `55119cd8b20e227284516b95f77a4b3e05384438` (the PR head may include docs-only evidence commits), and PR #5 remains OPEN/Draft. The bounded R1 offline worker used explicit import provenance (`c22a/src`): contract 30/30, canonical 169/169 after the host adapter and strict preparation seam, and focused snapshot/strict/view/UI 28/28 passed for the latest integration lane. A disposable install previously verified 18 files without deleting a foreign file; the final install is refreshed after the remaining docs commit. Host qualification remains independent.

The first live package is delegated to the external Resolve Operator as the SO-11 read-only preflight. Parent direct Resolve visibility remains zero. Until the Operator returns independent target/capability readback, no host gate is promoted and no user project is saved.

The first automatic-delegation canary completed with a passing launcher/lease envelope but a semantic `BLOCKED` result. The external Operator selected its compatibility lane, held the exact user-wide lease, observed one running Resolve instance, then found scripting unavailable and no database attached; project/timeline/comp and SO-11 processing/port capability were therefore unavailable. Independent runtime readback was consistent, graph/project mutation and save were both zero, and the launcher returned final lease `FREE`. Failure fingerprint is `DRIVER_CAPABILITY_GAP:scripting_unavailable_and_database_unattached` (attempt 1). This is trial evidence, not a product gate; one Operator-side recovery/qualified-route requalification remains before classifying the lane.

The second canary attempt used materially different Operator evidence and is recorded separately. It read back Resolve Studio `21.1.0.14`, compatibility MCP `v2.203.0`, and the current `Untitled Project` id `8f2d80d4-a15c-40a9-a2e7-65b574b5ecb8`; no timeline or Fusion comp exists, so SO-11 processing/port snapshot capability is `NOT_QUALIFIED`. Operator-owned launch/quit recovery completed with graph/project mutation=0 and project_save=0; the final lease is `FREE`, but runtime still reports one instance with `database_attached=false`/wedged guidance. This is `CAPABILITY_GAP:NO_ACTIVE_TIMELINE_OR_COMP_WEDGED_RUNTIME` (attempt 2), not a product PASS. The retry guard now forbids a third identical preflight. Next host work must change the semantic target to an owned disposable fixture or remain offline until the Operator can qualify one.

The first disposable-target qualification was launched before the R1 adapter install completed. Operator readback found the then-installed candidate `3315bc7` lacked `host_snapshot.py`; the bounded run timed out before returning scratch cleanup/final Resolve readback. The external launcher recovered its stale holder and left the lease `FREE`; project save remained 0 and parent direct-host fallback remained 0. This is a separate `HOST_QUALIFICATION_TIMEOUT:operator_started_against_stale_installed_candidate` attempt, not a third identical preflight and not a product gate. Recovery inventory/cleanup is required before any one requalification on the exact installed candidate. Evidence is in `docs/execution/strict-orthogonal/luna_execution.json#r1_disposable_operator_attempt`.

The follow-up Operator recovery package completed with `PASS_NO_OWNED_RESIDUE`. Resolve Studio `21.1.0.14` (GUI, one instance, Local Database) independently read back the unsaved `Untitled Project` (`206a53ff-8d46-4ddc-bd51-88f1abbe5ebc`), with zero timelines/media, zero launch-owned residues, zero project/graph mutation, project_save=0, and final lease `FREE`. No cleanup write was needed because the blank unsaved project had no ownership marker. This closes the previous timeout's restore evidence only; SO-11 and product gates remain unpromoted. Evidence is in `docs/execution/strict-orthogonal/luna_execution.json#r1_disposable_recovery` and the dated recovery checkpoint.

The one requalification attempt on exact installed candidate `bce01df` created an operation-owned scratch project, timeline, and Fusion item, but the current host refused `GroupOperator.AddTool` and a valid nested `Paste`. The non-empty nested fixture therefore could not be constructed, and the Operator timed out before returning adapter/final cleanup readback. Launcher cleanup recovered the stale holder and left the lease `FREE`; valuable project save remained 0 and parent direct-host fallback remained 0. This is new `HOST_CAPABILITY_GAP:NESTED_GROUP_CREATION_REFUSED_WITH_TIMEOUT` evidence, not a product PASS. No third identical qualification is allowed; the scratch residue must be recovered, then host work needs a materially different qualified fixture route or remains blocked. Evidence is in `docs/execution/strict-orthogonal/luna_execution.json#r1_disposable_requalification_attempt`.

The follow-up cleanup-only package identified `_mcp_RNK_SO11_9b291a91` by operation prefix and creation timestamp, deleted it with the host-safe project delete, and independently verified it absent from the project list and attributes. Resolve Studio `21.1.0.14` remained at the unsaved `Untitled Project` (`b4c37b66-5d7d-4021-bbdb-2ad5809f9f86`), unchanged with zero timelines; the package reported one scratch mutation, qualification/new fixtures 0, project_save=0, and final lease `FREE`. This closes the nested-fixture cleanup boundary, not the host capability gate. Evidence is in `docs/execution/strict-orthogonal/luna_execution.json#r1_nested_fixture_recovery` and the dated cleanup checkpoint.

## Luna exact install readback — 2026-09-10

The final backup-backed per-user installer was rerun from `bd2b6294293e1f0664249cd3c327830ed688309d`. The installed manifest reports the same repository commit, 18 manifest files plus the menu entry (19 total), and a source/installed SHA-256 comparison with zero mismatches. Installed imports for `resolve_node_kit`, `fusion.host_snapshot`, `fusion.strict_request`, `fusion.strict_planner`, `fusion.view_realization`, and `fusion.processing_snapshot` resolve from the intended `%APPDATA%/Blackmagic Design/DaVinci Resolve/Support/Fusion/ResolveNodeKit/src` root. This is an install/provenance PASS only; it does not promote any Resolve host or G01–G14 gate. Evidence is in `docs/execution/strict-orthogonal/luna_execution.json#install_readback` and the dated install checkpoint.

## R1 offline adapter — 2026-09-10

The bounded Luna Max Worker package `host_snapshot_adapter` added a read-only Fusion host adapter at `src/resolve_node_kit/fusion/host_snapshot.py`. It discovers root and nested `GroupOperator` tools, preserves exact source/target tool and port identities when the host exposes them, and leaves unsupported/error capabilities explicit instead of treating them as empty graph data. Duplicate names, invalid parent references, missing Group child discovery, and hierarchy cycles refuse closed. The adapter never calls position/settings/Undo/save mutation surfaces. Parent-side verification passed focused 38/38 and canonical 165/165 with explicit `c22a/src` import provenance. This is an offline implementation PASS only; SO-11 host qualification, strict mutation integration, and all G01–G14 remain pending. Evidence is in `docs/execution/strict-orthogonal/luna_execution.json#r1_offline_adapter` and `docs/checkpoints/2026-09-10-r1-host-snapshot-adapter.json`.

## SO-11 qualified standalone fixture — 2026-09-10

The external Resolve Operator loaded `nested_group_v1` through the qualified
standalone registry capability on Resolve Studio `21.1.0.14`, then invoked the
canonical `host_snapshot.py` adapter against the live comp. AddTool/Paste
fixture construction was not retried. Independent readback proved 10 unique
tools, 2 non-empty groups, depth 2, exact nested membership, both `MainOutput1`
aliases, `TOOLS_Name`/`TOOLS_RegID`/`TOOLI_ID`, and 7 direct port-labelled edges
including inner-to-outer and outer-to-root crossings. The adapter reconciles the
measured flattened root inventory with `GetChildrenList()` only for matching
live identity; ambiguous duplicates still fail closed.

Operator mutation counters were layout/graph/settings/Undo/save = 0. The
standalone comp was loaded once and closed once in the same invocation; current
comp absence and protected state equality were read back, cleanup was exact,
and the launcher ended at lease `FREE`. G01 and SO-11 adapter qualification
are `PASS`.

The snapshot keeps its remaining processing/position gaps explicit: FlowView
position was not supplied; `group_boundary_proxies`, parameters, keyframes,
expressions, instances, media, and time range are unsupported; `tool_state` has
an explicit JSON-safety read error. Therefore `strict_request` remains
fail-closed until a complete required snapshot is available. Full evidence is
in `docs/checkpoints/2026-09-10-so11-nested-group-host-pass.json`.

## Strict request preserve preflight — 2026-09-10

The installed `eedd62e` candidate was run against the same standalone fixture.
`strict_request` refused before independent plan validation because FlowView
position readback was unavailable and the required processing fields were not
complete. Exact unresolved coverage is recorded in
`docs/checkpoints/2026-09-10-strict-request-preserve-preflight-blocked.json`:
all ten positions, expressions, group-boundary proxies, instances, keyframes,
media, parameters, time range, and a tool-state read error.

Preserve, flatten/ungroup, Undo, and project save were all zero. Cleanup and
protected-state readback passed and the external lease ended `FREE`. This is a
strict-writer capability gap, not a reason to require a timeline for SO-11. The
next ready host package is read-only actual view/wire capability inventory on
the same qualified fixture; preserve remains fail-closed until complete
position/processing coverage exists.

## Actual view/wire inventory — 2026-09-10

The same qualified standalone fixture loaded and closed safely, but the current
compatibility driver cannot retain its standalone handle for FlowView,
connected-endpoint, pipe-mode, port-display, Group-boundary, or edge-geometry
readback. This is a driver capability gap, not proof that an active timeline is
required. Graph/layout/settings/Undo/save remained zero, protected state was
unchanged, cleanup was exact, and the lease ended `FREE`.

G03 remains blocked. The next view/wire attempt must use a materially different
Operator capability that retains the standalone handle; no blind timeline
attachment or parent-side Resolve access is allowed. Evidence is in
`docs/checkpoints/2026-09-10-actual-view-wire-standalone-blocked.json`.

## SO-40 flatten canary — 2026-09-10

The guarded `flatten_all_comp` canary stopped fail-closed with
`BLOCKED_HOST_API_ZERO_WRITE`. The compatibility surface did not return an
active standalone comp or the required identity-preserving ungroup, recursive
identity/endpoint, complete processing snapshot, and bounded Undo/rollback
readback callbacks. No flatten write, Undo, or save occurred; the project stayed
the unsaved `Untitled Project` with no timeline/current Fusion comp, and the
launcher ended `FREE`. This is not evidence that a timeline is required and it
does not promote G04. Exact evidence is in
`docs/checkpoints/2026-09-10-flatten-canary-zero-write.json`.

## Fresh offline verifier — 2026-09-10

An independent verifier process audited candidate `eedd62e` after the new host
evidence. Required IDs, the main-merge prohibition, G01 PASS, G02/G03 blocks,
G04–G14 non-promotion, exact nested structure, strict/view/flatten fail-closed
zero-write results, and installed/source provenance all passed the audit. The
strict contract is 30/30, the canonical suite is 170/170, compileall and diff
check pass, and the 1101-node planner stress is PASS (0.307s). This is an
offline readiness audit only: host 1100+, UI, performance, processing, and
recovery remain unverified. The focused offline UI/flatten/owned-Undo recovery
seams are 16/16 PASS. Evidence is in
`docs/checkpoints/2026-09-10-fresh-offline-verifier.json`.

The parent then added `fusion/strict_request.py`, a pure fail-closed preparation seam that composes a complete `ProcessingSnapshot` into the existing strict planner and requires independent plan validation before any future writer can act. It does not perform host writes, save, settings, or Undo. The integration lane passed dedicated tests and the canonical suite at 28/28 and 169/169 respectively; this advances only offline integration and does not qualify SO-11 or a host mutation path.

## Prompt orchestration CANARY result — 2026-09-10

The automatic delegation trial is recorded separately in `PROMPT_ORCHESTRATION_TRIAL_RESULT.{md,json}`. Six bounded Operator launches acquired and released the exact lease; parent direct-host fallback and human intervention were both 0. Two current-target preflights, a stale-install disposable attempt, exact-candidate nested-fixture attempt, and two cleanup packages produced structured readback. The nested fixture route remains an integration gap because `GroupOperator.AddTool` and valid nested `Paste` were refused; no product gate moved. Learning Gate outcome is RNK-specific reuse of the short parent envelope, exact installed-candidate precondition, and mechanical no-identical-third-retry guard, with no global policy promotion.

The fresh independent Luna Max verifier audited the exact pre-docs candidate `bd2b629` without repairs. It confirmed the required gates were not complete, the recorded Operator leases were `FREE`, and the install/trial/test evidence was internally consistent. The subsequent `3bf91d3` change is docs-only; the parent reran the install and independent test/readback checks after that change. Durable verifier evidence is in `docs/checkpoints/2026-09-10-fresh-final-verifier.json`.

## Luna strict first package — 2026-09-10

The requested G02/G03 first package was delegated only to the external Resolve
Operator. G01 was carried rather than replayed; no timeline workaround,
flatten/ungroup retry, project save, or parent-side Resolve access was used.

The native route was first corrected for namespace selection, then retried after
a separate compatibility recovery. Compatibility recovery brought Resolve
Studio `21.1.0.14` to GUI-ready PID `28584` with the unsaved `Untitled Project`,
no timeline, and zero graph/project/view/save mutation. The native route still
reported Resolve unreachable before fixture binding. All host attempts ended
with exact lease `FREE` and mutation counters zero. FlowView mapping,
strict-request application, processing invariance, run2, and actual view/wire
were not evaluated; G02/G03 remain `BLOCKED_TECHNICAL`. This is a runtime/route
gap, not evidence that a timeline is required. Full evidence is in
`checkpoints/2026-09-10-strict-first-package.json` and the Operator launch IDs
listed in its sibling Markdown checkpoint.

The independent offline lane added `fusion/strict_apply.py` and its focused
tests. `StrictPlan` now exposes per-scope logical placements/offsets, and the
processing-to-planner mapping preserves `GroupOperator` identity. The new
position-only seam requires explicit live tool handles and complete snapshot
coverage, maps logical cells to scope-local FlowView coordinates, verifies
pre-state identity, reads every position back, compares post processing
signatures, rolls back on mismatch, and supports a two-run stability check. It
never touches graph/settings/media/save surfaces and refuses unknown fields.
Focused strict-apply tests are `4/4`; canonical unittest is `174/174`,
`compileall` and `git diff --check` pass. These are offline implementation
results only and do not promote any host gate.

The offline seam and checkpoint were committed as `8e540e6` on the canonical
task branch and installed through the backup-backed per-user installer. The
manifest/source hashes match (20 files including entry and manifest), and the
installed import root resolves `fusion.strict_apply` from the intended user
package. Install readback is provenance-only; no Resolve call or project save
occurred.

## Luna Max capability qualification continuation — 2026-09-10

Fresh-read live state now resolves the canonical branch HEAD and installed
manifest to `e616966d935c93980ecf0c4b3cd05689926ab56f`. The parent effective
model was `gpt-5.6-luna/max`; the external Resolve Operator profile was
`gpt-5.6-terra/high`. The Operator workspace has no commit history, so its
non-cache source/test tree is recorded by deterministic revision
`21ac220fe0877194fbe8c01687642729906cf1c333cdaf80f148cf9d12bfa90a`.

Lane A used a materially different Operator-owned registry fixture probe
(`85d54d87-2aed-48a6-905f-ce77ce5acef6`). It loaded and closed
`nested_group_v1` once, observed 10 tools, 2 groups, and 7 processing edges,
including the mask edge and both Group-boundary crossings. Only `ports` was
complete; `group_boundary_proxies`, parameters, keyframes, expressions,
instances, media, and time range were unsupported, while `tool_state` had an
explicit read error. FlowView positions, viewport/zoom/provenance, and actual
displayed wire geometry were unsupported. All mutation/save counters remained
zero, protected state was unchanged, cleanup was exact, and the launcher ended
`FREE`. Processing-port or position evidence was not promoted to G03.

Lane B compatibility (`30712be3-3eac-47a1-b7d1-2d7a21d6b6f2`) could not expose a
retained target or owned Undo boundary, so the first write was forbidden and
all counters stayed zero. A separate native comparison
(`c290d6a7-a755-4c54-aea6-c21d0a297fcd`) inspected a 10-node/2-group graph but
could not retain position context or prove owned Undo; it also stayed zero
write. Both final leases were `FREE`. The historical `StartUndo=false` result
remains context-specific and was not generalized.

The Operator owner added transport-neutral contracts for processing coverage,
FlowView readback, displayed-wire edge coverage, and a dedicated
`qualify_undo_transaction()` seam with ownership-before-write and exactly-one
mutation/Undo tests. Focused Operator tests are `15/15 PASS`; compileall and
diff checks pass. Durable details are in
`checkpoints/2026-09-10-operator-capability-qualification.{md,json}`.

G02/G03 remain `BLOCKED_TECHNICAL`, G08 remains pending, and the integrated
G02/G03 HostSession, G04, save, main merge, and release were not run.

The Mandatory Learning Gate for this continuation records only an RNK/host-
specific reusable delta: retain the short semantic envelope, exact installed
candidate precondition, four-state capability contracts, mask/Group-boundary
edge gate, ownership-before-write gate, and no-identical-third-retry guard.
No global routing policy was promoted. Complete processing serialization,
displayed wire capture, owned Undo, integrated G02/G03/G04, and large-scale
qualification remain `NOT_COLLECTED`.

## Composition execution context matrix follow-up — 2026-09-10

The prior Lane A/B procedures were not replayed. One fresh compatibility
context matrix (`27a845ba-3505-4301-b925-d40ec17051e0`) compared an Operator-
owned timeline-item comp (B) with the same owned comp while the Fusion page was
active (C). B exposed `CurrentFrame` but no FlowView. C exposed a sample
FlowView position `[3.5, 1.009]`, but the public MCP exposed no `Undo`, masked
the raw `StartUndo` value/type behind a wrapper, and did not export stable opaque
comp or GUI-active-comp identity. `GetPosTable` and displayed-wire geometry
were not collected. No write was attempted.

One native route context (`ba69970d-af74-4215-920e-b92de86342b7`) used an
Operator-owned scratch comp. It did not retain as `CurrentComp`, had no
`CurrentFrame`/FlowView position target, and could not prove an owned Undo
boundary despite method names being present. The first write was forbidden.

Both scratch artifacts were cleaned up with independent absence readback and
both launcher envelopes ended `FREE`. Compatibility's empty `Untitled Project`
opaque identity differed pre/post; no valuable project was loaded or saved, so
no speculative restore was attempted. Operator source/test files were
unchanged (compatibility report: 17-file tree hash
`32bfeea6fe37e85c7bcfcf7f5987eb8912670cb84cc113d0e730685414756f61`).

No context proved the combined FlowView-bearing + owned-Undo prerequisite.
WP2 remained zero-write; WP3 full processing fingerprint/sensitivity and WP4
actual wire capture remain `NOT_COLLECTED`. G02/G03 stay
`BLOCKED_TECHNICAL`, G08 stays pending, and integrated G02/G03/G04/save/main
merge/release were not run. Structured evidence is in
`checkpoints/2026-09-10-composition-context-matrix.{md,json}`. Do not issue an
identical third context retry; retain the strict complete-processing and
displayed-wire requirements.

## Context-matrix fresh verification and install readback — 2026-09-10

Parent-side fresh readback found canonical `c22a` publication/docs HEAD and the
remote branch equal at `934060451be68f9b165891a745d903d5acfe3082`; the product
source/install candidate remains `e616966d935c93980ecf0c4b3cd05689926ab56f`.
Source/test/script tracked diff is empty. Operator focused tests are `15/15 PASS`; canonical RNK tests are
`174/174 PASS` with explicit canonical import provenance, plus compileall and
the strict contract checker pass. The per-user installer reports 19 manifest
files plus the entry (20 total), zero source/installed hash mismatches, and
installed-root imports for all strict modules from a temp cwd.

The fresh verifier confirms `candidate=none`, WP2 mutation counters all zero,
final leases `FREE`, G02/G03 `BLOCKED_TECHNICAL`, G08/G04 pending, and no
product gate promotion. Product completion remains false; this is a
`CHECKPOINTED_WITH_TECHNICAL_GAP` continuation, not a release or main merge.
Structured verifier evidence is in
`checkpoints/2026-09-10-context-matrix-fresh-verifier.{md,json}`.

## WP1 comp-local executor qualification — 2026-09-11

After the completed B/C/native matrix, two materially different read-only
routes were tested through the external Resolve Operator. The first
(`a3647c2b-8195-4b30-a20e-aa1cf1e410f9`) ran
`script_plugin.run_inline -> fusion.Execute(lua)` but found Resolve Studio
`21.1.0.14` in `Untitled Project` with no timeline/current comp;
`Fusion.GetCurrentComp()` returned no composition. The second
(`e4e5e5ac-9197-4a69-83e9-e7735729037c`) ran a Comp-category Lua script once;
the host returned `success=false` without an observable local comp or error
detail. Neither route exposed exact comp identity, CurrentFrame, FlowView /
GetPosTable, the 10-tool/2-group fixture fingerprint, complete processing
serialization, or an owned Undo boundary in one invocation.

Both launcher envelopes were transport `PASS` with exact-live ownership and
authoritative final `FREE`. The first created no scratch. The second removed
its temporary Comp script and verified the Comp script list empty; no comp
fixture result was observable, so its fixture-cleanup proof is not claimed.
Graph/layout/position/settings/connection/processing/keyframe/media/
selection/Undo/project-save counters remained zero, and Operator revision
`21ac220fe0877194fbe8c01687642729906cf1c333cdaf80f148cf9d12bfa90a` remained
unchanged. WP1 is `BLOCKED`; WP2 position/Undo, WP3 processing sensitivity,
and WP4 actual displayed-wire qualification were not run. G02/G03 remain
`BLOCKED_TECHNICAL`, G08 remains `PENDING`, and integrated G02/G03/G04, save,
main merge, and release remain unrun.

Structured evidence is in
`checkpoints/2026-09-11-comp-local-executor-qualification.{md,json}`. Do not
replay either route or issue an identical third context probe without new
host evidence.

## WP1 fresh verifier and install readback — 2026-09-11

Parent-side independent verification found the PR #5 branch and remote head
equal at `649ce7dd73e120b512ac33b4ba6fb2c19c0f32f4`; source/script changes
from the product parent are empty and the worktree is clean before this
checkpoint. RNK canonical tests are `174/174 PASS`, Operator focused tests are
`15/15 PASS`, and compileall, diff-check, and the strict contract checker pass.

The pre-existing manifest/blob provenance mismatch was not accepted. The
backup-backed installer was rerun from this PR HEAD and now records
`repo_commit=649ce7dd73e120b512ac33b4ba6fb2c19c0f32f4`, 19 package files plus
the entry, zero raw source/installed mismatches, and 19/19 normalized source
blobs matching the commit. The prior entry was backed up in the installer-owned
backup tree. Temp-cwd imports for all strict modules resolve inside the
installed root. Operator revision
`21ac220fe0877194fbe8c01687642729906cf1c333cdaf80f148cf9d12bfa90a` remains
unchanged with 17 files.

This readback promotes no host capability: WP1 is still `BLOCKED`, WP2
position/Undo counters are zero, final lease is `FREE`, G02/G03 remain
`BLOCKED_TECHNICAL`, G08/G04 remain pending, and product completion is false.
Details are in
`checkpoints/2026-09-11-comp-local-executor-fresh-verifier.{md,json}`.

## WP1 final bounded route closure — 2026-09-11

One final constructor-local hypothesis was tested exactly once after the two
earlier new routes. A Lua script called the host's composition constructor and
kept its returned object local; the MCP returned only an opaque `table: ...`
value with empty stdout. Local comp success, exact identity, FlowView /
GetPosTable, nested fixture fingerprint, processing serialization, owned Undo,
and close/absence readback are all `UNKNOWN`, not PASS. No current-comp,
timeline, standalone `LoadComp`, graph/layout/settings/Undo write, or save
route was used.

The three new routes are now closed: no identical context probe is allowed
without genuinely new host evidence. All launcher envelopes ended with
authoritative `FREE`; final host readback was Resolve Studio `21.1.0.14`, GUI
instance 1, `Untitled Project`, no timeline, page `null`, with no valuable
project loaded or saved. WP1 remains `BLOCKED`; WP2/WP3/WP4 and integrated
G02/G03/G04 remain unrun. The Operator workspace revision and 17-file tree
remain unchanged. Final evidence is in
`checkpoints/2026-09-11-comp-local-executor-final.{md,json}`.

## Requirements-first topology migration — 2026-09-11

Fresh reconciliation for this continuation read PR #5 as OPEN/Draft at
`191f9a2749e680ff38ce419468fa85f416854ae0`. CodexOperations PR #10 and #11
were read at `93b2e8008d27fa5c3afbf6dc94bd26c0d2d097b5` and
`e6b9c1f7e0db7504d53a56a4901eb034684a999e`. The migration checkpoint is
[`2026-09-11-requirements-first-topology.json`](checkpoints/2026-09-11-requirements-first-topology.json).

The execution contract is now requirements-first: choose D (direct guarded),
S (dedicated Resolve Worker), or H (host-local executor) only after capability
locality and boundary-loss analysis. The Host Guard is independent of that
choice and remains mandatory: exclusive lease, exact target, owned disposable
state, no blind retry, reversible/discardable mutation, detached independent
readback, cleanup/recovery, and final `FREE`. Raw Comp/FlowView/Undo handles
must remain host-local.

Matched migration evidence promotes S for structural fixture readback only.
CurrentComp/FlowView/Undo/GUI-local semantics are still unqualified in D/S/H;
the next safe package is one materially different WP1 host-local semantic
receipt probe. The three closed WP1 context routes must not be replayed. If
that probe blocks, dependent G02/G03/G04/G06–G08 host work remains blocked, but
independent offline/structural work continues. No gate is downgraded and the
qualified external Operator remains the rollback baseline.

Current execution status remains `CHECKPOINTED_WITH_TECHNICAL_GAP`; product
completion is false, main merge/release/project save remain unauthorized, and
the exact next route is recorded in the migration checkpoint.
