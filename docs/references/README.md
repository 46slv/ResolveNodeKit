# Visual references

This directory stores visual references used to define ResolveNodeKit layout intent.

These images are **design references**, not golden pixel outputs.

## semantic-layout-reference-01

Demonstrates:

- root-level left-to-right backbone;
- large parent `GroupOperator` remaining visually explicit;
- nested Group frame inside the overall graph;
- Group-local Merge chains;
- branch sources positioned above receiving Merge nodes;
- readable relationship between Group-local flows and the outer main rail.

Normative takeaway:

> The graph should read as a hierarchy of understandable local modules rather than one globally compacted flat DAG.

## semantic-layout-reference-02

Demonstrates the same hierarchy-aware layout with a more important spacing decision:

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
- exact node labels/names;
- theme colors;
- exact total width/height;
- exact wire curvature/appearance.

See:

- `../SEMANTIC_LAYOUT.md`
- `../SEMANTIC_LAYOUT_ACCEPTANCE.md`
