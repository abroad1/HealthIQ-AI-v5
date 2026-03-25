# ADR-008 — Promoted Signal Intelligence Contract v1 (KB-S47d)

## Status

Accepted — architecture decision and validator foundation.

## Context

Upstream investigation specs (`investigation_spec_schema_v3.0.0.yaml`) encode multi-hypothesis reasoning, narrative, and ranking. The runtime promoted signal layer must remain a **governed, signal-centric contract** without absorbing hypotheses, phenotype definitions, intervention registries, or user-state overlays into a single monolith.

## Decision

1. **Contract**  
   Promoted signal intelligence is defined by `knowledge_bus/schema/promoted_signal_intelligence_schema_v1.yaml` and enforced by `backend/scripts/validate_promoted_signal_intelligence.py`.

2. **Opt-in**  
   `package_manifest.yaml` may include optional `promoted_signal_intelligence: <relative path>`.  
   Packages **without** this field remain valid under the legacy **three-file** contract (manifest + research_brief + signal_library) only.

3. **Coexistence with `intelligence_model`**  
   `intelligence_model` (target schema v1) remains the optional path for packages that embed **hypotheses inside the same YAML** (legacy / transitional).  
   `promoted_signal_intelligence` is the governed home for **signal-layer intelligence only** (no hypotheses, no hypothesis ranking, no narrative).  
   A package may include **neither**, **one**, or **both** optional files during transition; validators run independently. Runtime consumers must treat **signal_library** as authoritative for activation mechanics and must not treat two sources as duplicate primary authorities for the same primitive without an explicit merge policy.

4. **Signal ↔ hypothesis linking**  
   **Authoritative direction:** adjacent hypothesis assets (future or separate files) reference **`owning_signal_id`** (or equivalent) pointing at the signal.  
   Promoted signal YAML **must not** embed `hypotheses` or `hypothesis_ranking`.  
   Optional reverse pointers from signal packages to hypothesis files are discoverability-only, not a second primary authority for hypothesis content.

5. **Translation from investigation spec v3**  
   Translation is a **deterministic reduction**, implemented in `backend/core/knowledge/investigation_spec_to_promoted_signal.py`:
   - **Copied / mapped:** signal identity, research domain, signal system, primary metric, trigger direction, activation, states, supporting markers, rolled-up contradiction markers (stable dedupe by `contradiction_id`), merged `missing_data.policies`, `confidence.evidence_strength`, evidence block (strength, physiological claim, threshold notes, optional sources), confirmatory test refs, override rules.
   - **Not translated:** `hypotheses`, `hypothesis_ranking`, `narrative`.

6. **Loader**  
   `backend/core/knowledge/load_promoted_signal_intelligence.py` loads the optional file when the manifest opts in; returns `None` otherwise.

## Consequences

- New validation stage in `validate_knowledge_package.py` when `promoted_signal_intelligence` is present (`promoted_signal_intelligence_validation` in aggregated status).
- No repo-wide migration required; grandfathering is explicit via manifest omission.

## Related

- `investigation_spec_schema_v3.0.0.yaml`
- `intelligence_model_schema_v1.yaml` (broader target model; hypotheses allowed there)
- KB-S47d work package
