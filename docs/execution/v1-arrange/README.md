# ResolveNodeKit v1 Arrange / Preserve execution owner

Status: `ACTIVE`

Product brief: [`../../PRODUCT_DIRECTION_BRIEF.md`](../../PRODUCT_DIRECTION_BRIEF.md)

Acceptance: [`acceptance.json`](acceptance.json)

Evidence matrix: [`EVIDENCE_MATRIX.md`](EVIDENCE_MATRIX.md)

Plan: [`PLAN.md`](PLAN.md)

## Mission

Complete v1 Automatic Node Arrange / Preserve as a useful installed Resolve
workflow. Arrange changes layout only: processing topology, tool identity,
Group membership, endpoint connectivity, parameters, keyframes, expressions,
media and render state are protected by snapshot/readback contracts.

The default request is the whole active Fusion composition with existing Groups
preserved. The supported flat-graph workflow is:

```text
Arrange -> Resolve native GUI manual Ungroup -> Re-Arrange
```

Automatic Ungroup / `UngroupFirst` / Flatten All is not a v1 acceptance item.
It is tracked in the preserved strict/v2 lane.

## Current route

```text
Luna Max Product Worker
  -> direct Resolve capability
  -> minimal mechanical Host Guard
  -> Resolve
```

Use one state writer and one live Resolve writer. Bind the exact target, use an
owned or disposable fixture for mutation, never blindly retry an ambiguous
write, read back the protected state, and clean up without saving valuable
projects.

## Release boundary

The v1 release candidate is not a main merge, tag or public release. It is the
state `V1_RELEASE_CANDIDATE` after a fresh verifier accepts the exact candidate.
The broader ResolveNodeKit mission and the v2 strict contract remain separate.

The normal UI must show Arrange / Preserve only. It must not imply that a
partially implemented automatic flatten path is a normal v1 feature. The
current production confirmation is text-only and maps to
`ArrangeDialogState(include_unselected=True, ungroup=False)`.

## Evidence rules

Existing evidence may be carried when the product tree, installed package and
candidate lineage are proven compatible. It is classified as:

- `PASS`: directly satisfies a v1 criterion;
- `PASS_WITH_SCOPE`: satisfies the criterion with an explicit fixture or
  surface limitation that is acceptable for v1;
- `NEEDS_SMALL_RECHECK`: the evidence is close but not the exact v1 workflow or
  final identity;
- `MISSING`: no evidence exists.

Unknown, refused, not-collected or mixed-candidate evidence is not silently
promoted to PASS. The machine-readable acceptance file owns the current v1
status; this README is the routing contract.

## Preserved lanes

The old strict contract remains at
`../strict-orthogonal/README.md`, `PLAN.md`, `LUNA_RUNBOOK.md` and
`acceptance.json`. The dated `../semantic-arrange-v1/` continuation and its
flatten amendment are also retained. These documents are historical/v2
research owners after the product-direction reset and must not route normal v1
work back to automatic flatten qualification.
