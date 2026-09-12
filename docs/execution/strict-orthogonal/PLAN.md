# Work packages and acceptance ownership

Updated: 2026-09-11 JST
Status: DIRECT_GUARDED_RESET

`acceptance.json` owns the required product gates. Execution progress is updated by the single Coordinator/state writer. Existing verified product evidence is carried unless a product change invalidates it; historical Operator/WP1 experiments are research evidence only.

## Direct-guarded operational reset — 2026-09-11

The old external-Operator-always route and the later D/S/H topology qualification are removed from the product dependency graph.

Current default:

```text
Luna Max Product Worker / Coordinator
  -> direct Resolve capability
  -> minimal mechanical Host Guard
  -> Resolve
```

Rules:

- WP1 semantic-receipt qualification is **not** required before SO-30/SO-40/SO-50/SO-60.
- Do not replay closed WP1 compatibility/native/constructor-local receipt probes for product progress.
- Do not keep parent Resolve capability disabled merely to preserve external-Operator isolation.
- Host-local Comp/FlowView/Undo/UI objects may remain live/local; detached serialization is required only when an actual evidence consumer needs it.
- Preserve one shared integration/state writer and one live Resolve writer/serialization for mutable work.
- Use exact target checks, owned scratch state, no-blind-retry, reversible/discardable mutation, readback and cleanup as mechanical safeguards—not as reasons to spawn another agent.
- Minimum useful real-host smoke precedes new generic infrastructure.
- If proof/orchestration infrastructure becomes harder than the underlying guarded Resolve operation, simplify or remove that boundary.

The dedicated Resolve Operator, Transactional HostSession and HostLocalSemanticReceipt remain archived research/comparison assets. They may be used only for explicit research or when a specific task class later demonstrates a measurable advantage over direct guarded execution.

## Product task graph

```text
SO-00
  -> SO-10 -> SO-11
  -> SO-20
  -> SO-30
  -> SO-50

SO-11 -> SO-40
SO-11 + SO-20 + SO-30 + SO-50 -> SO-60
SO-60 + SO-40 -> SO-61
SO-60 -> SO-70
SO-61 + SO-70 -> SO-71
SO-60 -> SO-80
SO-71 + SO-80 -> SO-90
```

Flatten being locally blocked does not stop strict preserve. A view/UI blocker does not stop independent structural/offline/recovery work. The program stops only when no authorized ready product task exists or a genuine authority/input boundary is reached.

## Work packages

| ID / outcome | Depends | Default owner / scope | Done / evidence | Failure / resume |
|---|---|---|---|---|
| SO-00 execution/source/runtime reconciliation | none | Coordinator | fresh local/remote/installed/runtime identity; active ownership; direct Resolve capability visibility or an explicit direct-route repair plan | preserve dirty work/leases; do not reset blindly |
| SO-10 complete source interpretation and snapshot contract | SO-00 | Product Worker / pure schema+fixtures | parse actual repo source; exact nodes/parents/cycles/grid/merge inputs; unknown remains unknown; complete artificial fixture distinguished from source-derived data | host omissions go to host evidence, not fabricated offline values |
| SO-11 complete host snapshot adapter | SO-10 | Product Worker using direct Resolve | non-empty nested disposable/known fixture read; port/proxy/processing state classified complete/unsupported/error; unknown blocks structural write | use bounded current host reads; do not rebuild Operator transport |
| SO-20 strict semantic planner | SO-10 | Product Worker / pure planner | multiedge preservation, role/continuity separation, recursive bounds, non-overlap, integer pitch, rail/feeder/region/reduction, stable run2, O01–O18 relevant fixtures | solve planner conflicts locally; do not alter processing topology |
| SO-30 actual strict view realization | SO-10 | Product Worker using direct Resolve/FlowView/UI | qualify actual orthogonal displayed-wire path on current host; same-run settings/view readback; masks/boundaries/ports covered; node positions alone are insufficient | pivot among current native/script/GUI surfaces; do not rebuild semantic receipt infrastructure |
| SO-40 safe flatten actually runs | SO-11 | Product Worker using direct Resolve | real non-empty nested 2+ depth fixture; all Groups=0; original non-Group identity/processing preserved; exact Undo/rollback; run2 stable | if public method absent, use documented native action/menu/host-local path; refuse destructive reconstruction |
| SO-50 installed UI without human click dependency | SO-00 | Product Worker / owned UI+controller+installer | inspectable widget state/events; Cancel zero-write; Run path; busy→result; installed entry invokes same controller | prefer RNK-owned inspectable UI; do not resurrect AskUser metadata dead ends |
| SO-60 small strict preserve E2E | SO-11,20,30,50 | Coordinator/Product Worker + direct host | full offline/compile/diff/install hash; flat/multiedge/Mask/non-empty nested preserve; actual UI→controller; processing invariant; Undo/run2; no-save/cleanup | repair only failed category; preserve independent gates |
| SO-61 small flatten E2E | SO-60,40 | Coordinator/Product Worker + direct host | non-empty nested flatten from actual UI; port/proxy/processing state and multi-frame render preserved; Undo/run2; no-save/cleanup | SO-40 gap stays local; no false PASS without processing evidence |
| SO-70 real/1100+ strict preserve | SO-60 | Product Worker / bounded real duplicate + generated fixture | real PSD2Fusion-scale disposable and >=1100 original non-Group nested fixture; all-node/edge coverage; rectangle=0; strict display; processing; Undo/run2; three real-changing actions <=60s; endpoint loss=0 | profile payload/transport separately; flatten gap does not block preserve |
| SO-71 real/1100+ flatten | SO-61,70 | Product Worker / largest safe duplicate+fixture | all Groups=0; processing graph preserved; strict geometry/display; exact grouped Undo; run2=0; three real-changing actions <=60s; endpoint loss=0 | preserve evidence if product changes; zero-write refusal is not success |
| SO-80 recovery/resume/package durability | SO-60 | Product Worker + Coordinator | timeout/exception/partial-write/cancel safety; ambiguous write reconciliation; rollback mismatch stop; multi-goal continuation; bounded restart; backup install/uninstall; no global env leak | unrecoverable state halts host writes but preserves evidence |
| SO-90 fresh final verifier / publish state | SO-71,80 | fresh independent Verifier; Coordinator writes state | all required gates PASS on exact candidate; source/install hashes; active installed UI; 1100+ preserve/flatten; Undo/processing/strict evidence; final cleanup; PR/remote readback consistent | FAIL -> new candidate -> affected gates -> fresh verifier |

## Immediate continuation after reset

1. Reconcile current PR/source/install/runtime and current direct Luna Max Resolve capability.
2. If old config has parent Resolve MCP disabled solely for Operator isolation, repair that config with rollback available.
3. Run one **minimum useful direct-host smoke** on owned/disposable safe state: bind Fusion context, observe relevant FlowView/position state, perform the smallest useful RNK path or tiny owned reversible mutation, read back, Undo/restore, cleanup.
4. If the smoke works, do not build more execution infrastructure. Move directly into SO-30/SO-50/SO-60 and SO-40 where ready.
5. If a host operation fails, diagnose the product/API/context layer and try a materially different documented native/script/GUI route. Do not reintroduce a dedicated Operator by default.
6. Continue independent ready packages even when one gate remains blocked.

## Required fixture catalogue

O01 serial H/V; O02 horizontal Merge+feeders; O03 x29-style 5BG+FG receiver; O04 x31.5-style 3BG; O05 Merge2 FG continuity; O06 same-X non-chain; O07 same-node-pair different ports; O08 Group-boundary projection; O09 unequal rectangles/expanded-vs-collapsed; O10 shared source/fan-out/multiple outputs; O11 Mask/auxiliary links; O12 missing input coverage; O13 29-Group census derivation; O14 flatten twice/former-region stability; O15 >=1100 non-Group/deep chain; O16 actual native view and coverage; O17 UI Cancel/Undo/rollback; O18 host readback offsets.

Geometric golden data must not change unnecessarily from node enumeration, display rename or global translation. Artificially completed source gaps must be labelled artificial fixtures; do not claim reproduction of every historical source render.

## User-visible style acceptance

For reference-derived mixed fixtures verify main-rail y alignment/x monotonicity, short feeder alignment, independent subgraph bounding boxes, right-side reduction where topology supports it, simple H/V final output path and region clearance. Row/column constraints, non-overlap and actual strict wires are hard requirements; absolute whitespace ratios and one giant rail are not.

For large canvas evidence, capture overview plus readable zooms for main rail, upper region, reduction, hardest wiring and non-empty Group/flattened region. Visual appearance alone never proves processing semantics.

## Evidence per run

Record only evidence needed by the gate, including as applicable:

- run/candidate/source/installed/publication identities;
- target stable IDs and host/build/context;
- before/after protected state;
- all-node/all-edge/processing coverage;
- FlowView/displayed-wire observation;
- actual mutations and Undo owner;
- run2;
- stage timings;
- cleanup and valuable baseline.

Large full snapshots may remain local artifacts with compact hashes/summaries in repo. Do not publish private media paths/client images.

`NOT_COLLECTED`, `UNKNOWN` and `UNVERIFIED` required fields are not release proof.

## Candidate / measurement identity

Product source commit/hash, docs/publication head, installed manifest and evidence candidate are separate identities. Docs-only commits may inherit host evidence only when product tree and installed hashes are proven unchanged.

Three performance runs must start from equivalent real-changing disordered/grouped baselines. A no-op second run is measured separately for stability and does not count as a performance action run.

## Safety / authority

Task-branch code/tests/docs, backup-backed install, commit/push and Draft PR #5 updates are authorized. Direct Resolve native MCP/scripting/GUI, Resolve launch/quit/restart, owned disposable fixtures and reversible validation mutation are authorized under the runbook.

No valuable project save, main merge, release, force-push shared history, credential change/bypass, unrelated deletion/process kill, PC reboot, global shortcut mutation or permanent service/startup installation is authorized by this plan.
