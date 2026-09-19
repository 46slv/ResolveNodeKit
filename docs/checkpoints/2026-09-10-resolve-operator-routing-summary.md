# Corrected Resolve Operator delegation summary

Current docs head before this summary: `7f80fc97b19c127dc7b8e35aae4c71f231d6f968`.

The new Luna Max continuation must not treat RNK's old same-session `MCP surface unavailable` checkpoint as the current Resolve Operator implementation path.

Current routing contract:

```text
Luna Max Coordinator
 -> high-level objective/target/Done/restore/evidence
 -> qualified external Resolve Operator
 -> inventory / exclusive lease / driver routing / operation / independent readback / cleanup-recovery / final readback / release
 -> structured evidence
```

The first live-host package is read-only SO-11 preflight. Parent specifies no MCP/GUI/script driver and no lease mechanics. Operator result is consumed as product evidence or BLOCKED/INTEGRATION_GAP; parent direct Resolve is not the fallback.

This is also the RNK field test for the `Resolve Operator automatic delegation` PROVISIONAL/CANARY in `CODEX_PROMPT_ORCHESTRATION_RESEARCH_2026-08-28.md`.
