# Semantic Arrange v1 continuation — 2026-09-08

## Candidate and host

- Branch: `feat/arrange-uia-e2e-20260906`
- Candidate code commit: `716d6a4506b021d27b82057b17e3ca589d579d6a`
- PR #5 head branch: `feat/semantic-arrange-v1-20260906`
- Resolve: Studio `21.0.3.7`
- Valuable final readback: `PSD2Fusion / Timeline 1 / Fusion`, 967 tools,
  exactly one timeline, `COMPB_Modified=false`, no project save.

The machine-readable record is
`docs/checkpoints/2026-09-08-semantic-arrange-v1-continuation.json`.

## SAV1-20 — offline/install

The continuation candidate has the shared production seam and the verifier's
Resolve-handle fallback.  The focused/full offline checks at the integrated
candidate were `python -m unittest discover -s tests -v` (`122/122 PASS`),
`python -m compileall -q src scripts tests` (`PASS`), and `git diff --check`
(`PASS`).  The per-user Resolve tree was reinstalled and its entry/package
hashes matched the candidate tree; final-candidate reinstall qualification is
rerun after the documentation checkpoint is committed.

## SAV1-30 — small whole-comp host smoke: PASS

On disposable `_mcp_RNK_SAV1_probe_20260908`, the installed production seam
ran `ArrangeDialogState(include_unselected=True, ungroup=False)` against a
7-tool / 3-edge whole composition with no selection.  The first run moved 6
and arranged all 7; the second run moved 0.  Tool identity, connections,
selection state, and exact handler-owned Undo readback all held.  Cleanup was
exact and the valuable host was restored.

## SAV1-40 — nested non-empty Group: PASS

Using the already host-proven SaveSettings-derived nested recipe on disposable
`_mcp_RNK_SAV1_40_20260908`, the candidate exercised `InnerG` inside `OuterG`
(8 tools, depth 2).  The first run moved 7 / arranged all 8 and the second
run moved 0.  Direct parent/child membership, connections, Group display
state, and exact Undo readback were unchanged.  No banned hand-written
single-Paste route was used; the disposable project was deleted and the
valuable host restored.

## SAV1-50 — compact large-host envelope: PASS

Position and connection probes on the valuable 967-tool composition established
16, 32, and 64-tool calls as successful; 64 is the selected envelope.  The
duplicate stress pre-read then completed all 16 position and 16 connection
chunks at size 64, returning compact hashes only.  The parent composite hashes
use ordered `offset:chunk_size:row_count:chunk_hash` lines joined with LF and
SHA-256; no 967-row payload was returned through MCP.  Connection endpoint IDs
were stable.  The exact compact records and hashes are in the JSON checkpoint.

## SAV1-60 — PSD2Fusion-scale product stress: BLOCKED_HOST / UNVERIFIED

The disposable duplicate had 967 tools, 24 GroupOperators, depth 2, complete
membership identity, and compact pre position/connection hashes.  A production
`execute_arrange_request` whole-comp call was attempted exactly once.  The
call produced no structured result and timed out at the MCP tool's 300-second
limit.  A 120-second representative processing/keyframe sample also timed out;
this is recorded as `processing_hash_status=UNAVAILABLE_TRANSPORT`, not as a
processing invariant pass.

The endpoint recovery contract was followed: the exact Resolve/fuscript PIDs
and paths were revalidated, normal close was attempted, the non-responsive
tree was terminated, Resolve was relaunched, and the first post-restart
identity probe passed.  One compact position chunk on the duplicate differed
after recovery, so the mutation outcome remains ambiguous and no first-run,
second-run, structural-invariant, or Undo success is claimed.  The exact
duplicate and its generated archive were deleted.  Final valuable host
readback is clean as stated above.  This is a narrow large-host blocker and
does not invalidate SAV1-30 or SAV1-40.

## Remaining autonomous route

SAV1-70 reconciles the durable docs and Draft PR without changing the product
contract.  SAV1-80 must independently inspect the fixed candidate, evidence,
installer hashes, final host state, and PR head; it must not repair the
candidate.  Only after that verifier passes does SAV1-90 remain as the one
conditional human release smoke.  AskUser UIA/MSAA remains
`BLOCKED_HOST_ACCESSIBILITY_HARD`, and the busy-stage `UIDispatcher` gap stays
feature-local.
