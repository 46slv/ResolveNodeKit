# SO-40 flatten canary — zero-write host block

The external Resolve Operator was asked to qualify one guarded
`flatten_all_comp` canary against the already-qualified `nested_group_v1`
semantic fixture on Resolve Studio `21.1.0.14`. No AddTool/Paste construction
was retried, and no project or timeline was created or saved.

The compatibility surface did not return an active standalone comp or the
required callback/readback seam. Consequently the canary stopped before any
flatten write, Undo, or save. The exact missing capabilities were standalone
`LoadComp`/owned `FusionComp.Close`, identity-preserving native ungroup,
recursive identity inventory, non-Group endpoint mapping, complete processing
snapshot fields, and bounded Undo/rollback plus structural readback.

This is `BLOCKED_HOST_API` with zero writes, not a flatten PASS and not evidence
that a timeline is required. The same Resolve project remained `Untitled
Project`, with no timeline or current Fusion comp; parent direct-host calls were
zero and the launcher released the lease to `FREE`.
