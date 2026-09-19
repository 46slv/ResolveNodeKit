# Semantic Arrange v1 — SAV1-80 fresh verifier

Date: 2026-09-08 JST  
Task branch: `feat/arrange-uia-e2e-20260906`  
PR branch: `feat/semantic-arrange-v1-20260906`  
Product candidate: `59eeffbce5efd0a73a0fed2a4f3418faf71d5852` (`fix: keep complete output edge scans bounded`)  
Verifier context: fresh read-only verification after the amended SAV1-55 → SAV1-70 continuation.  The publication/docs ref is the live task/PR head; the product evidence remains anchored to the unchanged candidate above.

## Verification result

`SAV1-80 PASS`.

The verifier independently checked:

- clean task worktree and task/PR remote refs aligned;
- bootstrap branch is an ancestor; current branch is not `main`, and PR #5 is not merged;
- changed-file scope is the ResolveNodeKit Semantic Arrange continuation;
- `python -m unittest discover -s tests -q`: `127/127 PASS`;
- `python -m compileall -q src scripts tests`: PASS;
- `git diff --check`: PASS;
- both amended evidence JSON files parse and retain their required PASS/refusal semantics;
- product candidate SHA is an ancestor of the publication head;
- installed manifest commit equals the publication head, all 13 package hashes and byte counts match, the installed entry hash matches, and `fusion/flatten.py` is installed;
- PR #5 remains OPEN/Draft, base `feat/bootstrap-nodekit-20260905`, head branch aligned, `merged=false`, and its body reports the amendment statuses;
- final Resolve readback is one `Timeline 1` in `PSD2Fusion` on Fusion, 967 valuable tools, `COMPB_Modified=false`, `COMPB_Rendering=false`, responsive runtime, no save, and no RNK disposable/archive remnants.

## Gate interpretation

SAV1-60R is PASS on installed production whole-comp preserve runs at 977 and
1110 tools (run 2 `moved=0`, structural hashes/Undo exact, overlap-free,
endpoint healthy).  SAV1-55/56 implementation and offline nested exact-Undo
proof are present, while the measured Resolve host has no explicit
identity-preserving Ungroup callable; the installed flatten request refuses
before write with identical pre/post hashes.  Therefore SAV1-65 remains the
specific `BLOCKED_HOST_API` gate, not a UIA/MSAA blocker, and flatten remains
unexposed.  `processing_hash_status=NOT_COLLECTED_BY_HOST_ADAPTER` is not
promoted to a processing PASS.

This verifier did not mutate the candidate or save the project.  Human
`SAV1-90` smoke remains last and is not requested while the amended flatten
gate is unresolved.
