# Semantic Arrange v1 flatten capability — 2026-09-08

Status: `BLOCKED_HOST_API` for live flatten execution; the product path is
implemented and fail-closed, and the preserve path is independent.

Candidate `59eeffbce5efd0a73a0fed2a4f3418faf71d5852` was installed and tested
on Resolve Studio `21.0.3.7`.  On the 1111-tool disposable composition, the
live GroupOperator sample exposed only `DoAction`, `LoadSettings`,
`QueueAction`, and `SaveSettings`; Comp and FlowView exposed only
`DoAction`/`QueueAction` among the candidate action methods.  No explicit
identity-preserving `Ungroup`/`UnGroup`/`UngroupTool` callable was present.
The bounded earlier candidate-action probe returned `false` without changing
the Group children.  Generic action names are intentionally not promoted to a
structural primitive.

The installed production request `arrange_comp(include_unselected=True,
ungroup=True)` refused in `0.1ms`.  Pre/post compact snapshots were identical:
1111 tools, 1180 edges, 28 Groups, depth 2, and the same non-Group identity,
parent, connection, and position hashes.  No Undo or write ran for that
refusal.

`flatten_all_comp` therefore accepts only an explicit host adapter callback.
When one is supplied, the offline nested fixture proves deterministic
deepest-first order (`InnerG`, then `OuterG`), exact endpoint/parent/connection
readback, one outer Undo transaction, exact restoration, and run2 `moved=0`.
The live host callback required by SAV1-55/56/65 is not available, so no live
flatten PASS or processing-preservation PASS is claimed and no UI checkbox is
exposed.  This is the amendment's specific host API stop condition, not the
unrelated UIA/MSAA limitation.
