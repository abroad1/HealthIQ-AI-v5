# HealthIQ AI — Sprint Plan (Sprints 15–25)

Version: 1.0  
Scope: Backend + Frontend + LLM narration  
Cadence: Short, tightly‑scoped PRs per sprint stage  
Guardrail: End‑to‑end Upload→Parse→Render smoke must remain green after every PR.

---

## Programme non‑negotiables
- Lab‑ranges‑first: always use the user’s own laboratory reference ranges for interpretation.  
- Deterministic engines: scoring, thresholds, clusters and risk calculations in code; LLM narrates only from structured JSON.  
- No fallback parsers: only the real parser is permitted.  
- Feature flags for new engines; dark by default until validated.  
- Validation gates: completeness and confidence must be computed and surfaced.  

---

## Sprint map (at a glance)

| Sprint | Goal | Primary artefacts | Flag | User‑visible change |
|---|---|---|---|---|
| 15 | SSOT metadata foundation | `ssot/biomarkers.yaml`, validator, additive DTO fields | N/A | None (metadata only) |
| 16 | Cluster Engine v2 (deterministic) | `core/clustering/engine_v2.py`, `ssot/cluster_rules.yaml` | `ENABLE_CLUSTER_ENGINE_V2` | None (flag off) |
| 17 | Prompt Builder v2 + LLM output validator | `prompt_builder/v2.py`, Pydantic schemas | `ENABLE_PROMPT_V2` | None (flag off) |
| 18 | Stabilisation + hygiene | Cleanup artefacts, tighter pre‑PR checks, branch clarity | N/A | None |
| 19 | Biomarker expansion batch 2 (~40) | SSOT entries, converters, aliases | N/A | Expanded coverage in results |
| 20 | Cluster/UI surfaces | Cluster grid, dial polish, biomarker→cluster links | `ENABLE_CLUSTER_UI` | New dashboards |
| 21 | Longitudinal trends | Trend engine + FE sparklines | `ENABLE_TRENDS` | Trends views |
| 22 | Behavioural rec engine v2 | Rec library + selector (LLM narrates only) | `ENABLE_RECS_V2` | Action cards |
| 23 | World‑class UX polish | Tokens, typography, PDF v2, clinician summary | N/A | Premium visual finish |
| 24 | Performance & scalability | Caching, SSE tuning, Lighthouse | N/A | Faster app |
| 25 | Launch readiness & docs | Runbooks, error taxonomy, monitoring | N/A | Operational quality |

---

## Definition of Done (DoD) – common to all sprints
- Existing Upload→Parse→Render smoke stays green (two‑line paste = 2 biomarkers; empty = 400 by contract).  
- Unit tests + selective snapshot tests pass locally.  
- No fallback/dummy code paths introduced.  
- CI (where present) includes lint + new validations.  
- Feature flags default **OFF** for new engines; no change to live API unless stated.
- CI guardrails green (validator + smokes + no-fallback grep). No manual evidence required.  

---

## Sprint 15 — SSOT metadata foundation (PR8)
**Objective**: Give each biomarker the metadata required for system‑ and cluster‑level reasoning.

**Scope**
- Extend `ssot/biomarkers.yaml` with: `system`, `clusters`, `roles`, `key_risks_when_high`, `key_risks_when_low`, `known_modifiers`, `clinical_weight` (0–1).  
- Validator at `core/ssot/validate.py` fails if any shipped biomarker is missing fields or types are invalid.  
- Additive DTO enrichment: include `ssot` block per biomarker in API responses.

**Deliverables**
- Updated SSOT YAML for all shipped biomarkers.  
- Validator + helper script and unit tests.  
- Integration test asserting `ssot` appears in parsed output.

**Acceptance**
- Validator: 100% of shipped biomarkers valid.  
- Smoke unchanged; FE still renders as before.  

**Out of scope**: Scoring, clusters, UI changes.

---

## Sprint 16 — Cluster Engine v2 (feature‑flagged)
**Objective**: Deterministic 0–100 cluster scores using SSOT weights and optional rule‑based compensations.

**Scope**
- `core/clustering/engine_v2.py` evaluates clusters: per‑biomarker z‑scores vs lab ranges, weighted by `clinical_weight`; aggregates by `ssot.clusters`; applies optional `cluster_rules.yaml` compensations; scales to 0–100; bands to green/amber/red; computes confidence from presence ratio.  
- `core/clustering/rules.py` loads `ssot/cluster_rules.yaml`.  
- Minimal default `cluster_rules.yaml` structure (bands, optional compensations, weights, required sets).  
- Unit + snapshot tests only.  

**Flag**: `ENABLE_CLUSTER_ENGINE_V2` (default OFF).  
**Acceptance**: All tests pass; no live API/FE changes.

**Out of scope**: Routing the scores to API/FE.

---

## Sprint 16 (Engine Only) — Implementation Summary

**Status**: ✅ Engine module implemented, not wired to runtime.

**Deliverables**:
- `backend/core/clustering/cluster_engine_v2.py`: Engine module with `load_cluster_rules()` and `score_clusters()` functions
- `backend/ssot/cluster_rules.yaml`: Minimal stub rules file (empty rules array)
- `backend/tests/fixtures/panels/`: Three synthetic test panels (green_metabolic.json, amber_hepatic.json, red_metabolic.json)
- `backend/scripts/smoke_cluster_engine_v2.py`: Smoke script that runs engine and prints 8 cluster objects
- `backend/tests/unit/test_cluster_engine_v2.py`: Unit tests for happy path, hepatic scoring, and confidence behavior

**Banding**: 0–49 green, 50–69 amber, 70+ red (temporary bands for smoke testing)

**Confidence**: Fraction of required cluster members present (temporary heuristic)

**Runtime Status**: Engine is **not wired** to FastAPI routes, orchestrator, or frontend. No runtime behavior changes. Upload parse still returns same shape.

**Next Steps**: Sprint 17+ will wire engine to runtime via feature flag `ENABLE_CLUSTER_ENGINE_V2`.

---

## Sprint 17 — Prompt Builder v2 + LLM Output Validator
**Objective**: Replace loose prompts with structured JSON context and strict output validation.

**Scope**
- `prompt_builder/v2.py` assembles JSON: user, clusters (when enabled), insight stubs, red‑flags, policy.  
- Pydantic schema validates LLM output; reject unknown fields, numeric invention, or medical claims.  
- Snapshot several canonical panels.  

**Flag**: `ENABLE_PROMPT_V2` (default OFF).  
**Acceptance**: Validator prevents hallucinations; no live API/FE change.

**Out of scope**: Insight logic; FE rendering.

---

## Sprint 17 (Prompt Builder v2 + LLM Output Validator) — Implementation Summary

**Status**: ✅ Compute-only implementation, not wired to runtime.

**Deliverables**:
- `backend/core/prompt_builder/v2.py`: Deterministic prompt builder emitting strict JSON
- `backend/core/llm/schemas_v2.py`: Pydantic schemas with `extra="forbid"` and constraints
- `backend/core/llm/validator_v2.py`: Validator with numeric invention and evidence referencing checks
- `backend/tests/fixtures/panels/canonical_small.json`: Test panel with 2-4 biomarkers
- `backend/tests/snapshots/prompt_v2_canonical.json`: Frozen expected prompt structure
- `backend/tests/fixtures/llm/`: Valid and invalid LLM result fixtures
- `backend/tests/unit/test_prompt_builder_v2.py`: Prompt builder unit tests
- `backend/tests/unit/test_llm_validator_v2.py`: Validator unit tests
- `backend/scripts/smoke_prompt_v2.py`: Local smoke script
- `backend/config/flags.py`: Feature flag definition (`ENABLE_PROMPT_V2 = False`)

**Validation Rules**:
- Schema validation: `extra="forbid"` rejects unknown fields
- Numeric invention detector: Rejects numeric values not present in prompt
- Evidence referencing: Ensures evidence IDs reference prompt biomarkers/clusters
- Red flag safety: Red flags must reference prompt red flags or IDs

**Runtime Status**: Prompt Builder v2 and LLM Validator v2 are **not wired** to FastAPI routes, orchestrator, or frontend. No runtime behavior changes. Feature flag defined but unused.

**Commands**:
```bash
# Run SSOT validator
python -m backend.core.ssot.validate

# Run unit tests
pytest backend/tests/unit/test_prompt_builder_v2.py -q
pytest backend/tests/unit/test_llm_validator_v2.py -q

# Run smoke script
python backend/scripts/smoke_prompt_v2.py
```

**Next Steps**: Sprint 18+ will wire Prompt Builder v2 to runtime via feature flag `ENABLE_PROMPT_V2`.

---

## Sprint 18 — Stabilisation + hygiene (short sprint)
**Objective**: Reduce friction and prevent accidental artefacts or missing files from slowing development.

**Scope**
- Remove tracked artefacts (`tatus`, `tatus --porcelain`, `.tsbuildinfo`, `result.json`) and add minimal ignore rules to prevent recurrence.  
- Keep pre‑PR checks lightweight and Windows‑friendly; document any required local services (upload parse requires `localhost:8000`).  
- Clarify branch usage and backup expectations (no new runtime behaviour).  

**Acceptance**
- `git status --porcelain` is clean after the cleanup steps.  
- `.gitignore` blocks known artefacts without masking real source files.  
- No fallback/dummy parsers introduced; no runtime changes.  

**Out of scope**: New engines, feature flags, or UI changes.

---

## Sprint 19 — Biomarker expansion batch 2 (~40)
**Objective**: Broaden coverage now that intelligence is ready to use it.

**Scope**
- Add ~40 biomarkers across lipid, thyroid, iron, vitamins, inflammation, renal, hepatic, hormonal.  
- Update SSOT entries, alias mapping, conversions, and initial `clinical_weight` and cluster memberships.  
- Unit tests for conversions/flags; integration test to prove new biomarkers traverse the pipeline.

**Acceptance**: New biomarkers appear end‑to‑end; smoke unchanged for legacy cases.

**Out of scope**: UI redesigns; engine rewrites.

---

## Sprint 20 — Cluster/UI surfaces
**Objective**: Make system‑level intelligence visible and traceable.

**Scope**
- FE: Cluster grid, cluster dials, drivers list, biomarker→cluster highlighting (use scaffolds from PR6).  
- Accessibility and medical‑grade contrast; no animation gimmicks.  
- If `ENABLE_CLUSTER_ENGINE_V2` is ON, render read‑only cluster results; otherwise keep current view.

**Flag**: `ENABLE_CLUSTER_UI` (default OFF).  
**Acceptance**: Visual regression + a11y pass; togglable without affecting existing flows.

**Out of scope**: Trends; recommendations.

---

## Sprint 21 — Longitudinal trends
**Objective**: Persist and present biomarker and cluster trajectories.

**Scope**
- Backend: store time‑series; compute improving/stable/worsening labels.  
- FE: sparkline component, cluster trajectory labels, simple “You improved by X%” metric.

**Flag**: `ENABLE_TRENDS` (default OFF).  
**Acceptance**: Synthetic fixtures prove trends; FE renders behind flag; smoke unchanged.

**Out of scope**: Advanced forecasting; cohort analytics.

---

## Sprint 22 — Behavioural recommendation engine v2
**Objective**: Grounded, specific next‑step actions chosen deterministically; LLM narrates only.

**Scope**
- Evidence‑tagged library (JSON) mapped to patterns/clusters.  
- Selector chooses ≤3 actions per insight; LLM narrates text from the structured selection.  
- Safety filters and disclaimers enforced.

**Flag**: `ENABLE_RECS_V2` (default OFF).  
**Acceptance**: Selector tests pass; API returns actions behind flag; FE hides unless enabled.

**Out of scope**: Free‑text advice generation by the LLM.

---

## Sprint 23 — World‑class UX polish
**Objective**: Raise perceived quality and exportability.

**Scope**
- Design tokens adoption, typography, micro‑interactions.  
- PDF v2 deterministic reports and clinician‑friendly summary.  
- Dark mode and device regression checks.

**Acceptance**: PDF snapshot tests; Lighthouse visual stability; accessibility meets target.

**Out of scope**: New engines or data models.

---

## Sprint 24 — Performance & scalability
**Objective**: Hit performance targets under load.

**Scope**
- Backend caching of hot computations; SSE tuning; cold‑start improvements.  
- Frontend Suspense/prefetch; Lighthouse ≥ 90.  
- Load tests and memory/regression checks.

**Acceptance**: P95 latency targets met; no regressions in smoke or a11y.

**Out of scope**: Feature work.

---

## Sprint 25 — Launch readiness & documentation
**Objective**: Operational hardening for v1 launch.

**Scope**
- API + architecture docs; deployment runbooks; rollback plan.  
- Error taxonomy; monitoring dashboards and alerting.  
- Manual UAT with sign‑off criteria.

**Acceptance**: UAT green; rollback tested; docs complete and linked.

**Out of scope**: New features.

---

## Testing & safety framework (applies across sprints)
- **Smokes**: Upload two‑line sample → 200; empty → 400. Must stay green.  
- **Unit**: Parsers, conversions, validators, engines.  
- **Snapshots**: Cluster and insight outputs on canonical fixtures.  
- **Property‑based checks**: Monotonicity invariants (e.g., TG:HDL ↑ should not reduce metabolic stress).  
- **Safety**: Red‑flag routing; no diagnostic language; strict LLM schema with allow‑listed fields.

### CI-enforced governance (no hand-pasted evidence)

To reduce overhead, sprint governance is enforced by CI:

- Smokes: Upload two-line sample → 200; empty → 400.

- Validator: SSOT schema and biomarker completeness.

- Safety grep: forbids fallback/dummy parsers.

- Feature flags default **OFF**; no new engines wired unless the PR explicitly enables a flag.

Developer responsibility:

- Keep changes additive and behind flags.

- Let CI enforce gates; **do not paste logs** into PRs (CI artifacts carry evidence).

---

## Rollback & failure capture
- Revert policy: if a PR fails smoke or introduces runtime errors, revert immediately; investigate on a throwaway branch.  
- Capture kit: run `audit_imports.py` and `run_upload_smoke.py` to snapshot failures; attach artefacts to PRs.

---

## Governance
- One PR per narrowly defined change; keep flags OFF until validated.  
- Do not switch import bases wholesale; prefer additive shims for new code only.  
- No fallback parsers under any circumstance.  

---

This plan is the reference for execution. Save it alongside the PRD and update version when scope changes are formally agreed.

