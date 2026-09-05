# ResolveNodeKit host evidence protocol

Purpose: make host verification compact, deterministic, and reviewable, especially for large Fusion graphs that are impractical to serialize wholesale through MCP.

This protocol defines evidence transport, not product behavior. Live host/API reality still decides which fields can be populated.

## 1. Evidence envelope

A host verification result should return a compact versioned envelope similar to:

```text
schema: resolve-node-kit.host-evidence/v1
target: project/timeline/comp identity
host: Resolve/Fusion version
tool_count
group_count
max_group_depth
identity_status
connection_hash
membership_hash
position_hash
processing_hash_status
duplicate_position_summary
elapsed_ms
mismatches[]
```

Do not transfer every node/settings row by default. Expand only mismatching categories.

## 2. Stable tool identity

Preferred identity is a hierarchical path derived from verified parent ownership plus tool name, with RegID/type retained as metadata.

Conceptually:

`/OuterGroup/InnerGroup/ToolName`

Rules:

- parent chain must be read from live host data;
- do not assume flat tool names are globally unique;
- if two tools cannot be uniquely distinguished within the same verified parent scope, set `identity_status=ambiguous` and fail closed for mutations requiring exact identity;
- do not invent a volatile list index as a stable identity unless the host proves it stable for the operation.

## 3. Canonical signatures

Use UTF-8 canonical rows, sorted lexicographically, then SHA-256 the joined rows. Record the schema/version used.

### Membership signature

One row per tool:

`<tool_path>\t<parent_group_path-or-root>\t<reg_id>`

For layout/display commands this hash must remain unchanged.

### Connection signature

One row per connected edge using every stable endpoint field the host exposes:

`<source_path>\t<source_output_id>\t<target_path>\t<target_input_id>`

If an output/input identifier is unavailable, leave that field empty and record the limitation. Do not replace an unavailable stable ID with a guessed semantic label.

For layout/display commands this hash must remain unchanged.

### Position signature

One row per managed tool:

`<scope_path>\t<tool_path>\t<x_quantized>\t<y_quantized>`

Quantization/tolerance must be explicit in the evidence envelope and derived from current adapter/host behavior. Do not hard-code a historical tolerance as universal truth.

Expected behavior for a tidy command:

- first run: position hash may change;
- second run: position hash must remain identical under the same quantization policy.

### Duplicate-position summary

Within each managed visual/layout scope, group quantized `(x,y)` coordinates and report only coordinates with more than one tool, including the affected hierarchical paths.

A duplicate is not automatically a defect if the command contract intentionally permits it, but it must be classified.

## 4. Processing-state evidence

Structural hashes do not prove all processing parameters/keyframes are unchanged.

Preferred route for large-host validation:

1. if current host settings can be deterministically canonicalized, compute an in-host aggregate processing hash while excluding known layout-only/UI fields;
2. prove the canonicalization itself on a small canary first;
3. otherwise report `processing_hash_status=unavailable` and perform documented representative parameter/keyframe sampling rather than claiming full processing invariance.

Never claim full parameter invariance from connection/membership hashes alone.

## 5. Pre/post comparison

For layout/display commands:

Required unchanged categories:

- target identity;
- tool count unless the command explicitly creates/removes tools;
- membership hash;
- connection hash;
- processing hash/samples according to the evidence level.

Expected changed category:

- position hash on the first layout run, when movement is needed.

Required stable category on repeat:

- position hash on the second identical run.

When a required unchanged hash differs:

1. stop further host writes;
2. request/emit only the rows needed to localize that category's mismatch;
3. rollback if the current operation owns the mutation;
4. do not dump the whole graph unless compact localization cannot identify the issue and transport bounds permit it.

## 6. Large graph transport rule

For graphs on the order of hundreds/thousands of tools:

- compute signatures inside Resolve/Fusion whenever possible;
- return counts/hashes/timing/focused mismatches through MCP;
- do not repeat a known full-snapshot timeout with materially identical payload;
- keep structured MCP tool-use events as transport evidence;
- parent Codex independently verifies the compact pre/post evidence before accepting the gate.

A repo diagnostic such as `scripts/Fusion/ResolveNodeKit_Evidence.py` may be added to mechanize this protocol. Its output schema should remain versioned and tested independently of product layout code.

## 7. Evidence limitations

If an API cannot expose a stable identity, UI state, processing state, or readback necessary for a claim, say so and narrow the claim. An explicit `unavailable`/blocked field is better than a fabricated proof.
