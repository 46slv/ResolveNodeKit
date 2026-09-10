# Actual view/wire inventory — standalone handle blocker

The qualified `nested_group_v1` standalone composition loaded and closed
successfully on Resolve Studio `21.1.0.14`. The compatibility driver could not
retain the returned standalone handle for FlowView, connected endpoint, pipe
mode, port-display, Group-boundary, or edge-geometry readback.

This is a driver capability gap, not proof that an active timeline is required:
the fixture route itself is timeline-free and protected state was unchanged.
No layout/graph/settings/Undo mutation or project save occurred. Cleanup was
exact and the launcher ended with lease `FREE`.

G03 remains blocked. A future retry must use a materially different Operator
capability that preserves the standalone handle and exposes the missing
readback; no blind timeline attachment or parent-side Resolve access is allowed.
