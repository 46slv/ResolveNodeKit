# Visual references

This directory stores visual references used to define ResolveNodeKit layout intent.

The SVGs here are **architecture abstractions of user-provided Fusion screenshots**, not golden pixel outputs. They intentionally remove project-specific node names and exact coordinates while preserving the layout decisions that matter to the design.

## semantic-layout-reference-01.svg

Demonstrates:

- root-level left-to-right backbone;
- large parent `GroupOperator` remaining visually explicit;
- nested Group frame inside the overall graph;
- Group-local Merge chains;
- branch sources positioned above receiving Merge nodes;
- readable relationship between Group-local flows and the outer main rail.

Normative takeaway:

> The graph should read as a hierarchy of understandable local modules rather than one globally compacted flat DAG.

## semantic-layout-reference-02.svg

Demonstrates the same hierarchy-aware layout with the more important spacing decision:

- wider horizontal spacing on the Merge side is acceptable;
- rail spacing may be asymmetric;
- visual clarity around Merge branches is more important than uniform density;
- a nested Group can occupy a wider box while remaining clearly connected to the main backbone.

Normative takeaway:

> Merge-side widening is an intentional semantic-layout tool, not an error condition.

## What is normative

- hierarchy remains visible;
- Group boundaries remain meaningful;
- main rails are easy to scan left-to-right;
- Merge chains can use elastic spacing;
- branch provenance should be visually obvious;
- the same rules apply recursively inside Group scopes.

## What is not normative

- exact node coordinates;
- exact Group size;
- exact zoom level;
- exact project node labels/names;
- theme colors;
- exact total width/height;
- exact wire curvature/appearance.

The original screenshots remain design-source evidence from the conversation; the repository SVGs are the durable, project-neutral representation used by the architecture contract.

See:

- `../SEMANTIC_LAYOUT.md`
- `../SEMANTIC_LAYOUT_ACCEPTANCE.md`
- `../decisions/0001-group-local-semantic-layout.md`
