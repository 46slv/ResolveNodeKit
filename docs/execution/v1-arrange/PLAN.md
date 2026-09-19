# v1 Arrange / Preserve plan

Status: `ACTIVE`

Owner: `docs/execution/v1-arrange/`

## Gate order

1. `V1-00` — product-direction reset and live identity reconciliation.
2. `V1-10` — v1 acceptance and evidence carry-forward matrix.
3. `V1-20` — installed source/package/UI identity and offline qualification.
4. `V1-30` — flat and representative topology Arrange proof.
5. `V1-40` — Group-preserving and nested-Group Arrange proof.
6. `V1-50` — manual Ungroup -> Re-Arrange E2E on owned disposable/duplicate.
7. `V1-60` — real-project duplicate and `>=1100` non-Group Arrange, run2,
   Undo, performance and cleanup.
8. `V1-70` — fresh independent verifier and PR/state reconciliation.

Automatic Ungroup / Flatten All is deliberately absent from this dependency
graph. It is a v2 resume trigger, not a v1 release gate.

## Carry-forward decision

The existing direct-guarded checkpoints already prove or substantially prove
the v1 preserve path:

- installed Run / Cancel / busy / result and small Arrange E2E;
- non-empty Group-preserving Arrange and exact Undo/run2;
- real PSD2Fusion duplicate at `1198` tools / `1173` non-Group tools;
- constructed depth-4 `1134`-tool fixture with `1100` non-Group tools;
- three real-changing large runs under 60 seconds;
- endpoint loss `0`, topology/identity/parent readback and cleanup;
- source/install hash parity and fresh historical verifier records.

The carry-forward matrix must keep the exact scope visible. In particular, the
`1100` number includes 25 explicitly created disconnected padding tools while
the source-derived graph contributed 1075 non-Group tools. This is a valid
v1 scale fixture, not a source-derived 1100 claim.

## Small remaining qualification

The one genuinely v1-specific host item is the same-fixture workflow:

```text
installed RNK Arrange
 -> protected-state readback
 -> Resolve native GUI manual Ungroup
 -> installed RNK Re-Arrange
 -> protected-state/readback + run2 + Undo/recovery + cleanup
```

Use a fresh owned/disposable nested fixture or safe duplicate. Do not search for
or guess an automatic Ungroup primitive. If the live host surface is not
available, keep this item explicitly `NEEDS_SMALL_RECHECK` and do not invent a
PASS from separate fixtures.

## Stop rules

- Do not lower a v1 criterion because a v2 host primitive is unavailable.
- Do not treat strict rectangle/grid machine-readable gaps as v1 failures when
  real/logical evidence shows the Arrange result is not visually broken.
- Do not repeat a materially identical Resolve timeout or ambiguous mutation.
- Do not save a valuable project, merge `main`, publish a release, or force-push.

## Completion wording

Preferred final state:

```text
PRODUCT_DIRECTION_RESET: PASS
V1_ARRANGE_STATUS: RELEASE_CANDIDATE
V1_RELEASE_CANDIDATE: PASS
V2_AUTOMATIC_FLATTEN: DEFERRED_RESEARCH
MAIN_MERGE: NOT_DONE
ACTUAL_RELEASE: NOT_DONE
```
