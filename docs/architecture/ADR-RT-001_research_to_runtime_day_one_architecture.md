# ADR-RT-001 — Research to Runtime Day-One Architecture

| Field | Value |
|-------|-------|
| **Status** | ACCEPTED |
| **Date** | 2026-05-28 |
| **Work package** | ARCH-RT-0 |
| **Supersedes** | Informal parallel authorities documented in ARCH-R1 reviews |

## Context

HealthIQ holds a large Pass 3 investigation-spec corpus and 186 knowledge packages, but runtime intelligence is assembled from **compiled package views**, **hand-maintained root-cause YAML**, and **hard-coded card evidence**. Research is not read at runtime.

Inputs: `docs/architecture/ARCH-R1_research_asset_to_runtime_intelligence_architecture_review.md`, `docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL.md`, ARCH-RT-0 inventories.

## Decision

### Canonical research authority

**`investigation_spec` v3.0.0** under `knowledge_bus/research/investigation_specs/` is the **single canonical research authority** for new compile work.

Legacy packages and YAML remain **temporary runtime inputs** until governed regeneration replaces them.

### Compiled runtime artefact model

Runtime consumes **immutable compiled artefacts** only:

| Artefact | Purpose |
|----------|---------|
| `signal_library.yaml` (+ manifest, research_brief) | Signal activation |
| `promoted_signal_intelligence.yaml` | Optional signal-layer semantics (ADR-008) |
| Compiled hypothesis assets | WHY / root-cause (future) |
| Compiled Health Systems Card evidence | Subsystem marker roles (future) |

### Accepted target pipeline

```text
investigation_spec (validated)
  → governed compile (manifest-emitting)
    → package triple + optional PSI + hypothesis artefact + card evidence artefact
      → thin runtime loaders (registry, evaluator, compilers, assembler)
        → presentation-safe DTOs
          → frontend render-only
```

### Non-negotiable constraints

1. **No raw research reads at runtime** (no Pass 3 JSON/YAML in orchestrator).  
2. **No frontend medical inference** — components render DTO fields only.  
3. **Packages are compile targets**, not parallel research authorities.  
4. **IDL / retail explainer** gate presentation, not medical graph truth.

### Relationship to sprint plan

This ADR ratifies the **ARCH-RT-0 → ARCH-RT-1 → ARCH-RT-2 → ARCH-RT-3** sequence in `healthiq_day_one_architecture_rework_sprint_plan_FINAL.md`. Implementation must not skip inventory-backed compile foundation.

## Consequences

- All estate regeneration work must emit **compile manifests** (ADR-RT-004).  
- LC-S18A review-queue packages remain non-authoritative until compile + promotion gates pass.  
- Current `SignalRegistry` lexicographic collision policy is **technical debt**, not target architecture.

## References

- `docs/architecture/intelligence_authority_inventory.md`  
- `docs/architecture/activation_compile_gap_report.md`  
- `architecture/ADR-008-promoted-signal-intelligence-contract-v1.md`
