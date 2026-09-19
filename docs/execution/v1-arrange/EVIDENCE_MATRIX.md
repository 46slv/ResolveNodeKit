# v1 Arrange / Preserve evidence matrix

This matrix is the human-readable companion to `acceptance.json`. It keeps
existing host evidence useful without merging incompatible candidate identities.

| v1 criterion | Status | Evidence / scope | Remaining action |
|---|---|---|---|
| Flat graph Arrange | `PASS` | `docs/checkpoints/2026-09-11-so30-so40-so50-direct-host-v2.json#SO-60` and the earlier Semantic Arrange canaries | Carry after final install identity readback |
| Group-preserving Arrange | `PASS` | SO-60 GUI-created Group runs; Group identity and direct membership unchanged | Carry |
| Nested Group Arrange | `PASS_WITH_SCOPE` | SO-60 non-empty Group plus `2026-09-10-so11-nested-group-host-pass.json`; recursive preserve evidence | Carry with candidate-lineage check |
| Fan-out / multi-edge / Mask / branch | `PASS_WITH_SCOPE` | SO-60 representative fixture and latest 1198-tool duplicate; large run has fan-in/fan-out/multi-edge counts | Carry; Mask is small-fixture evidence |
| Processing topology preservation | `PASS_WITH_SCOPE` | labelled edges, protected TextPlus/Mask/Blur/Blend inputs and processing signatures on qualified preserve runs | Do not claim flatten/render proof |
| Tool identity preservation | `PASS` | exact IDs/RegIDs on small and large preserve runs | Carry |
| Group parent/membership preservation | `PASS` | SO-60 Group readback; parent-first large run | Carry |
| Endpoint loss | `PASS` | latest 1198-tool duplicate and 1134-tool scale fixture report `0` | Carry |
| Undo / rollback | `PASS_WITH_SCOPE` | one-owned Undo exact on SO-60; exact position/structure restoration on large runs; recovery checkpoint | Carry; host Undo count is not a v1 flatten claim |
| Run 2 stable / no-op | `PASS` | SO-60 `moved=0`; latest large stability run `moved=0` with identical geometry | Carry |
| Installed UI Run / Cancel / busy / result | `PASS_WITH_SCOPE` | SO-50 and SO-60 installed UI evidence; Cancel zero-write; busy hidden before result | Re-read final installed identity |
| Real project duplicate | `PASS` | PSD2Fusion duplicate, 1198 tools / 1173 non-Group, exact structural readback | Carry |
| `>=1100` non-Group scale | `PASS_WITH_SCOPE` | depth-4 1134-tool disposable: 1075 source-derived + 25 owned padding = 1100 | Preserve scope; no source-derived 1100 wording |
| Performance | `PASS` | three real-changing actions 15.0752s / 12.8013s / 13.0515s; endpoint loss 0 | Carry; no flatten timing claim |
| Recovery / cleanup | `PASS` | SO-80 and 2026-09-12 exact cleanup; no valuable save | Carry |
| Manual Ungroup -> Re-Arrange | `NEEDS_SMALL_RECHECK` | native GUI Ungroup and preserve Arrange are proven separately, not yet same-fixture E2E | Run once on owned/disposable nested fixture |
| Source/install/package identity | `NEEDS_SMALL_RECHECK` | installed hashes match current product tree; manifest commit is older docs-only candidate | Install final candidate and re-read manifest |
| Fresh final verifier | `NEEDS_SMALL_RECHECK` | historical fresh verifiers exist for earlier candidate; current v1 contract is new | Run after final docs/install/evidence state |

## Evidence that remains v2-only

The following are intentionally not v1 acceptance gates: automatic
Ungroup/Flatten All, `UngroupFirst` installed dispatch, large flatten, flatten
processing/render preservation, single-workflow flatten rollback, strict
rectangle/grid proof and strict displayed-wire machine-readable collection.

Their source material remains under `docs/execution/strict-orthogonal/` and the
existing checkpoints. `BLOCKED_TECHNICAL`, `PENDING`, `NOT_COLLECTED` and
fail-closed refusal states there must remain unchanged as historical evidence.
