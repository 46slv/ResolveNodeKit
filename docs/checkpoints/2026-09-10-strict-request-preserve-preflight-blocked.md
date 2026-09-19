# Strict request preserve preflight — fail-closed

The installed `eedd62e` candidate was exercised against the same qualified
standalone `nested_group_v1` composition on Resolve Studio `21.1.0.14`.
Structure and port inventory were readable, but `strict_request` refused before
plan validation because the host did not provide FlowView positions and the
required processing coverage was incomplete.

Exact unresolved paths were:

- all ten node positions (`unsupported`);
- `expressions`, `group_boundary_proxies`, `instances`, `keyframes`, `media`,
  `parameters`, and `time_range` (`unsupported`);
- `tool_state` (`error`).

No preserve write, flatten/ungroup, Undo, or project save ran. The fixture was
closed once, current comp absence was read back, protected state was unchanged,
and the external launcher ended with lease `FREE`.

This is not a timeline-based rejection of SO-11. It is the precise strict
writer capability gap for the standalone comp. Preserve remains fail-closed
until the missing readback is qualified. The next independent gate is a
read-only actual view/wire capability inventory using the same fixture.
