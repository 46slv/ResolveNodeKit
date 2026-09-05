# Host validation matrix

Offline tests are necessary but insufficient. A host feature is accepted only against an exact Resolve/Fusion version with target identity, pre/post readback, invariant comparison, and rollback/Undo evidence appropriate to the command.

For current operational status, read `docs/CURRENT_STATE.md`. Historical host runs belong under `docs/checkpoints/`.

## Evidence levels

- `OFFLINE` — mocks/fixtures/algorithm tests only.
- `HOST-MEASURED` — real host evidence exists, but current canonical branch may still need integration/closeout.
- `HOST-PASS` — current canonical implementation has been run and accepted on the stated host.
- `BLOCKED-CURRENT-PATH` — a specific attempted host path is disproven; other hypotheses may remain.
- `BLOCKED-API` — no safe/readback-verifiable path remains for the feature on the measured host.

Do not turn a return value such as `True` into HOST-PASS without state readback.

## Fusion Flat Tidy

Historical 2026-09-05 evidence: HOST-MEASURED PASS on Resolve Studio 21.0.3.7 disposable canary with local measured fixes. Canonical branch HOST-PASS requires reconciliation and a small closeout canary.

Acceptance checklist:

- [ ] current canonical branch contains the measured FlowView snap/readback fixes;
- [ ] full offline suite + `compileall` pass;
- [ ] script loads in intended Resolve/Fusion context;
- [ ] serial chain canary;
- [ ] BG + FG -> Merge canary;
- [ ] EffectMask branch canary;
- [ ] isolated/disconnected case;
- [ ] connections unchanged;
- [ ] sampled processing parameters/keyframes unchanged;
- [ ] second run position-identical / no drift;
- [ ] one Undo restores positions when safely testable;
- [ ] failure/readback mismatch restores original positions;
- [ ] no project/timeline/comp identity drift.

Save/reopen persistence is a separate persistence gate and must not force saving the user's active project without explicit safe-target authority.

## Fusion `Tidy Nested` — hierarchy-preserving recursive tidy without expansion

This is separate from strict `Tidy + Expand Groups`.

First real-host canary on a collapsed GroupOperator:

- [ ] `GetChildrenList()` direct children match parent ownership via `ParentTool` / `TOOLH_GroupParent`;
- [ ] child positions are readable while parent is collapsed;
- [ ] child positions can be changed and read back while parent remains collapsed;
- [ ] direct group membership unchanged;
- [ ] connection signature unchanged;
- [ ] group expanded/collapsed display state unchanged;
- [ ] sampled processing parameters/keyframes unchanged;
- [ ] Undo/explicit rollback restores positions;
- [ ] nested 2–3-level scopes receive deterministic layouts;
- [ ] second run is position-identical.

Only after this canary passes should `tidy_nested_comp(...)` / `ResolveNodeKit_TidyNested.py` be considered host-ready.

## Fusion visual Group expansion — strict user-visible requirement

Known measured current-path result on Resolve Studio 21.0.3.7:

`SaveSettings -> Expanded=true -> LoadSettings(True result) -> SaveSettings readback` does **not** retain the expanded state. This serialized-settings path is therefore not accepted and should not be retried without new evidence.

Runtime-action research checklist:

- [ ] inspect existing OpenCode/MCP/runtime surfaces for a named/bounded Fusion Expand/Collapse action;
- [ ] avoid blind global keystrokes and avoid installing a new automation stack solely for this blocker;
- [ ] on one disposable Group, bind exact selection/target;
- [ ] invoke exactly one candidate runtime action;
- [ ] independently observe actual expanded/subflow state;
- [ ] verify GroupOperator identity/membership unchanged;
- [ ] verify connections unchanged;
- [ ] verify Undo/cleanup behavior;
- [ ] prove deterministic targeting across nested groups before bulk expansion.

If every readback-verifiable action path is exhausted, classify this feature `BLOCKED-API`. That blocks `MISSION_COMPLETE` under current user requirements, but not independent ResolveNodeKit development.

## Fusion fit-to-contents

Prerequisite: real runtime Group expansion PASS.

Do not infer geometry from `.setting` examples.

- [ ] capture real `GroupInfo.Size`, `Scale`, `Offset` and group/node positions before experiments;
- [ ] capture direct-child bounds and visible clipping result;
- [ ] change one geometry variable at a time on a canary;
- [ ] derive semantics from repeated measured values;
- [ ] implement padding/fit only from measured behavior;
- [ ] all direct children visible, including nested Group nodes;
- [ ] second run stable;
- [ ] membership/connections/processing state unchanged;
- [ ] Undo/rollback proven.

## Large/nested Fusion stress

Prerequisite for recursive-tidy stress: Flat Tidy HOST-PASS + `Tidy Nested` host canary PASS. Visual expansion/fit is a separate lane.

Do not request a full 1000+ tool JSON snapshot if it is known to time out.

Use in-host compact canonical evidence:

- [ ] tool count;
- [ ] group count + maximum nesting depth;
- [ ] connection-signature hash;
- [ ] group-membership-signature hash;
- [ ] position-signature hash;
- [ ] duplicate-coordinate counts per managed visible scope;
- [ ] optional sampled processing-state hash;
- [ ] runtime/timing;
- [ ] focused mismatch rows only when a signature differs.

Stress acceptance:

- [ ] completes without host crash/hang;
- [ ] structural hashes unchanged;
- [ ] intended positions settle deterministically;
- [ ] second run stable;
- [ ] no unbounded loop;
- [ ] operationally usable runtime.

## Fusion low-risk commands

Each Align / Distribute / selection traversal / selected-scope tidy command requires:

- [ ] explicit target/selection scope;
- [ ] deterministic postcondition;
- [ ] readback of position/selection state where exposed;
- [ ] no processing-state mutation;
- [ ] Undo/rollback appropriate to the mutation;
- [ ] offline tests for host-independent logic;
- [ ] one real-host canary.

## Fusion rewiring commands

Each rewiring command requires:

- [ ] exact pre edge/input/output identity snapshot;
- [ ] minimal intended write set;
- [ ] complete affected-edge readback;
- [ ] exact postcondition and no extra edge changes;
- [ ] processing state unchanged unless explicitly owned by the command;
- [ ] rollback to exact pre edge set on mismatch;
- [ ] representative host canary.

No ambiguous input classification may be guessed.

## Color capability gate

Read-only map first:

- [ ] current Resolve/project/timeline acquisition;
- [ ] relevant current item acquisition path;
- [ ] timeline/clip/group `GetNodeGraph()` availability where exposed;
- [ ] distinguish unsupported API from current-context/item unavailability;
- [ ] enumerate node count, labels, LUT/cache state, and tools where exposed;
- [ ] record exact host version and item types that return no graph.

Color writes begin only after capability mapping. Each mutation must have a readable postcondition and rollback/exclusion contract.

Do not claim physical Color node XY layout until a real readback-verifiable API or safe alternative is measured.
