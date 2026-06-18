# HealthIQ AI — Eight-Block Beta Readiness Estate Audit

> Post-audit note: see `EIGHT_BLOCK_BETA_READINESS_LATE_DOCUMENT_ADDENDUM_2026-06-17.md` and `docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md` for later-discovered authority documents.

**Auditor:** Claude Code (claude-sonnet-4-6)  
**Date:** 2026-06-17  
**Mode:** READ-ONLY evidence discovery. No code changed, no commits, no branches created.  
**Method:** Parallel independent search across all eight blocks; findings merged into this report.  
**Companion:** This same prompt was issued independently to Cursor. GPT will compare outputs.

---

## Executive verdict

**Overall maturity:** MEDIUM — structurally sound architecture, significant implementation gaps before external beta.

**Strongest existing assets:**
- Layer B is the strongest block. All three deterministic artifacts (`ClinicianReportV1`, `NarrativeReportV1`, `InterpretationDisplayLayerBundleV1`) are confirmed in production. The Layer B → Layer C handoff contract (`NarrativePayloadV1` v1.1) is architecturally complete with anti-hallucination rules.
- The systems taxonomy document (`docs/architecture/User Health to Systems Map_FINAL.md`) is the authoritative 8-domain model — this is the "medical LLM systems report" the prompt was searching for.
- ReplayManifestV1 with 25+ component-level version strings and deterministic hashes is exceptional for a pre-beta product.
- 187 Knowledge Bus packages, 11 phenotype fixtures, 16 Sentinel-guarded defect classes, and rich signal suppression tests give the test estate real depth.

**Biggest gaps:**
1. Only 3 of 6 launch-core health domains are implemented — blood/iron, thyroid and kidney are missing from the Wave 1 assembler.
2. Gemini Layer C is entirely inactive for narrative synthesis; no prompt template consuming `NarrativePayloadV1` exists.
3. Retail explainer registry covers only 17 of ~79 biomarkers typically in a panel.
4. 6 HIGH-severity UAT defects (2026-06-16) are unresolved.
5. No formal beta readiness gate / checklist document.
6. Layer C test suite is effectively empty (Gemini inactive).

**Areas where we risk reinventing work:**
- The `User Health to Systems Map_FINAL.md` taxonomy already defines the full 8-domain model with medical rationale, confidence framework, scoring bands and splitting rules. Do not rebuild this from scratch.
- `NarrativePayloadV1` is the Layer B → Layer C contract. Do not reinvent it; consume it.
- `validator_v2.py`, `DEFAULT_LLM_PROHIBITED_ACTIONS`, `DEFAULT_PROHIBITED_CLAIM_PATTERNS` are the anti-hallucination stack. Extend, do not replace.
- The `wave1_subsystem_evidence.py` pattern and existing KB packages (`pkg_thyroid_tsh_context`, `pkg_iron_deficiency_context`) contain the raw material needed for the 3 missing domains.
- `LAUNCH-CORE-3` auditability policy is already written and partially implemented. Extend the missing fields; do not redesign the model.

**Documentation vs runtime drift:**
- `narrative_report_compiler_v1.py` is labelled "N-8 Layer C" but is deterministic (no LLM) — the current "Layer C" is a deterministic compiler, not Gemini. Naming creates conceptual confusion.
- `prompts.py` has a `NARRATIVE_GENERATION` template that predates `NarrativePayloadV1` and should not be used for Layer C without a full rewrite.
- `scoring_policy.yaml` covers 8 internal systems; `domain_score_assembler.py` only returns 3. The mapping between SSOT system names and consumer domain labels is implicit in assembler code.

**Beta readiness verdict:** NOT READY for external beta. Ready for controlled internal validation with a small cohort IF the 6 HIGH UAT issues are resolved first. External beta requires: 3 missing domains, Gemini Layer C activation, UAT defect resolution, formal beta gate, expanded explainer coverage, consumer persona testing.

---

## Evidence search scope

**Directories searched:**
- `backend/core/analytics/` — scoring, narration, domain assembly, subsystems, replay
- `backend/core/contracts/` — typed Layer B contracts, replay manifest, versioning
- `backend/core/dto/` — DTOs and versioning policy
- `backend/core/llm/` — Gemini client, prompts, validator
- `backend/core/insights/` — synthesis.py
- `backend/core/knowledge/` — health system card evidence, flat card evidence
- `backend/ssot/` — scoring policy, retail explainer registry
- `backend/tests/regression/`, `enforcement/`, `integration/`, `fixtures/`
- `frontend/app/(app)/results/` — results page
- `frontend/app/components/results/` — all results components
- `frontend/tests/components/`
- `knowledge_bus/packages/` — 187 packages
- `knowledge_bus/pathway_explainers_v1/`, `interpretation_entities_v1/`
- `knowledge_bus/research/investigation_specs/`
- `sentinel/packs/`, `sentinel/sentinel_runner.py`
- `docs/architecture/` — ADRs, domain narrative, architecture maps
- `docs/governance/` — SOPs and promotion protocols
- `docs/testing/` — UAT documents, Sentinel reports

**File types searched:** `.py`, `.tsx`, `.ts`, `.yaml`, `.json`, `.md`

**Key search terms used:**
- `consumer_domain_scores`, `domain_score_assembler`, `wave1`, `headline_systems`, `system_taxonomy`
- `subsystem`, `insulin_resistance`, `lipid_transport`, `hepatic`, `proof_of_pathway`
- `clinician_report_v1`, `narrative_report_v1`, `interpretation_display_layer_v1`
- `report_compiler`, `boilerplate`, `explainer`, `evidence_for`, `evidence_against`
- `gemini`, `Layer C`, `synthesis`, `hallucination`, `NarrativePayloadV1`
- `ResultsPage`, `UAT`, `Wave1DomainCards`, `body_overview`, `StaleResultBanner`
- `Pass 3`, `investigation_spec`, `promotion_protocol`, `source_provenance`, `lab_range`
- `result_version`, `replay_manifest`, `analysis_id`, `hash`, `immutable`
- `fixture`, `phenotype`, `suppression`, `pregnancy`, `AAS`, `DHEA`, `thyroid`

**Known limits:**
- Did not fully read every KB package manifest (187 packages)
- `retail_explainer_v1/registry.yaml` read to ~60 of 364 lines
- `domain_narrative_wave1.py` confirmed to exist; full function bodies not read
- `docs/CLAUDE_TRANSLATION_SPEC_v1.md` — referenced in STATE_OF_TRUTH_REVIEW but not read in this audit

---

## Block-by-block maturity table

| Block | Maturity | Strongest evidence | Runtime proof | Documentation proof | Main gaps | Reuse priority |
|-------|----------|--------------------|---------------|---------------------|-----------|----------------|
| 1 — Core health systems | MEDIUM | `User Health to Systems Map_FINAL.md` + `domain_score_assembler.py` | 3/6 launch-core domains in production assembler | Strong — 8-domain taxonomy + scoring policy SSOT | 3 launch-core domains not implemented | HIGH |
| 2 — Subsystems | MEDIUM | `wave1_subsystem_evidence.py` + 12+ KB packages | 7 Wave 1 subsystems assembled across 3 domains | PARTIAL — no standalone subsystem spec doc | No subsystem assembly for blood/iron, thyroid, kidney | HIGH |
| 3 — Layer B intelligence | HIGH | `report_compiler_v1.py` + `narrative_report_compiler_v1.py` + `NarrativePayloadV1` | All three Layer B artifacts deterministic in production | Strong — ADR, domain narrative contract, multiple architecture docs | Boilerplate coverage partial; N-5/N-7 pathway coverage partial | HIGH |
| 4 — Gemini / Layer C | LOW (runtime) / MEDIUM (contract) | `ADR_WP2_layer_b_layer_c_contract_path_b.md` + `NarrativePayloadV1` | Gemini INACTIVE for narrative; active only for PDF parsing (Layer A) | Good — ADR accepted, contract in code | No Gemini prompt template consuming NarrativePayloadV1; prompts.py stale; no activation plan | HIGH |
| 5 — Results page / UX | MEDIUM-HIGH | 984-line results page, 18+ components, UAT 2026-06-16 | All three DTO sources confirmed rendering | Strong — UAT defect register, journey ordering in code | 6 HIGH UAT issues open; Gemini slot empty; no external user testing | HIGH (defect resolution) |
| 6 — Safety / provenance | MEDIUM | 187 KB packages, promotion protocol v1.1, `consumer_prose_safety_v1.py`, lab range enforcement | Lab range protection confirmed; prohibited substring filter confirmed; output authority provenance built | Strong — LAUNCH-CORE-3, traceability matrix, content boundary policy | 17/79 biomarker explainers; no unified rejected-signal registry; no automated clinical safety gate | HIGH |
| 7 — Auditability / reproducibility | MEDIUM | `ReplayManifestV1` (25+ hashes), result_versioning working, LAUNCH-CORE-3 policy | Stale/incompatible detection working (UAT verified) | Strong — LAUNCH-CORE-3 locked policy, ADR-RT-004 | No raw_input_hash; no parent lineage; no formal end-to-end replay verification | MEDIUM |
| 8 — Test estate / panels | MEDIUM | 16 Sentinel guards, 11 phenotype fixtures, 14+ panels, rich signal suppression tests | Regression, enforcement, integration tests confirmed; Sentinel Phase 1 active | Sentinel implementation report, testing strategy, testing operating model | No beta checklist; no Layer C tests; limited e2e; no contradictory panel fixture | HIGH |

---

## Block 1 — Core health systems model

### Confirmed assets

| Asset | File path | Evidence class |
|---|---|---|
| Systems taxonomy document (8 domains, 6 launch-core) | `docs/architecture/User Health to Systems Map_FINAL.md` | CONFIRMED — documentation |
| Scoring policy systems list (8 internal systems) | `backend/ssot/scoring_policy.yaml` | CONFIRMED — runtime SSOT |
| Wave 1 domain assembler (3 domains implemented) | `backend/core/analytics/domain_score_assembler.py` | CONFIRMED — runtime code |
| Domain scores contract | `backend/core/models/results.py` → `ConsumerDomainScoreV1` | CONFIRMED — typed contract |
| State of Truth document | `docs/STATE_OF_TRUTH_REVIEW_2026-05.md` | CONFIRMED — audit paper |

### Implementation evidence — CONFIRMED (Wave 1 only; PARTIAL for full 6-domain)

`backend/core/analytics/domain_score_assembler.py` implements exactly **three Wave 1 consumer domains:**
- `wave1_cardiovascular` — Consumer label: "Cardiovascular health"; Clinical label: "Cardiometabolic / Vascular Risk Status"
- `wave1_blood_sugar` — Consumer label: "Blood sugar control"; Clinical label: "Glycaemic Regulation / Insulin Resistance Status"
- `wave1_liver` — Consumer label: "Liver health"; Clinical label: "Hepatic-Metabolic Strain Status"

The function `assemble_consumer_domain_scores_v1()` always returns exactly these three entries (line 769: `out_rows = [cv_block(), met_block(), liv_block()]`).

Scoring rails in `backend/ssot/scoring_policy.yaml` cover 8 internal systems: `metabolic`, `cardiovascular`, `inflammatory`, `hormonal`, `nutritional`, `kidney`, `liver`, `cbc`. Biomarker→system mappings are hardcoded in the scoring policy (e.g., cardiovascular: total_cholesterol, ldl_cholesterol, hdl_cholesterol, triglycerides, tc_hdl_ratio; metabolic: glucose, hba1c, insulin). Score bands: strong (80–100), stable (65–79), watch (45–64), review (0–44) — implemented at lines 97–105 of domain_score_assembler.py.

UAT confirmed (2026-06-16): CV 86, Blood Sugar 100, Liver 73 — all three domains rendering with correct data.

### Documentation evidence — CONFIRMED

`docs/architecture/User Health to Systems Map_FINAL.md` (v0.4) is the authoritative systems model. It defines:
- **6 launch-core domains:** Cardiovascular health, Blood sugar control, Liver health, Blood iron & oxygen, Thyroid & energy regulation, Kidney function
- **2 second-wave domains:** Silent inflammation, Hormone balance
- Three-layer naming: consumer label / clinical handout label / internal engine mapping
- Score interpretation framework (0–100, 4 bands)
- Confidence framework (high/good/moderate/limited)
- Splitting rules for sub-scores
- Domain-by-domain readiness assessment with embedded medical review conclusions

**Note:** There is no separate "medical LLM report" as a standalone document. `User Health to Systems Map_FINAL.md` IS that document — it contains the clinical taxonomy definition. Do not search for or commission a replacement.

### Gaps

1. **3 of 6 launch-core domains are NOT implemented.** Blood iron & oxygen, Thyroid & energy regulation, Kidney function are absent from `domain_score_assembler.py`. They appear in `scoring_policy.yaml` as `cbc`/`nutritional`/`kidney` systems but have no Wave 1 consumer card assembler.
2. The mapping between SSOT internal system names and consumer domain labels is implicit in assembler code only — not documented in a standalone file.
3. `hormonal` and `nutritional` systems have `system_weight: 0.0` in SSOT — correct for wave phasing but could confuse future maintainers without documentation.

### Reusable source material

- `docs/architecture/User Health to Systems Map_FINAL.md` — **DO NOT reinvent.** This is the system model authority.
- `backend/ssot/scoring_policy.yaml` — biomarker→system mappings already exist for all 8 systems. Extend for remaining 3 Wave 1 domains.
- `domain_score_assembler.py` cv_block/met_block/liv_block pattern — template for the 3 missing domains.

### Recommended next action

Map which signal assets and KB packages already exist for blood/iron, thyroid and kidney (confirmed: `pkg_thyroid_tsh_context`, `pkg_iron_deficiency_context`, `pkg_iron_overload_context`) before commissioning any implementation sprint. The build materials likely exist.

---

## Block 2 — Subsystems and depth model

### Confirmed assets

| Asset | File path | Evidence class |
|---|---|---|
| Wave 1 subsystem assembly engine | `backend/core/analytics/wave1_subsystem_evidence.py` | CONFIRMED — runtime code |
| Subsystem→domain mapping (7 subsystems, 3 domains) | `backend/core/analytics/wave1_subsystem_evidence.py` lines 20–34 | CONFIRMED |
| Compiled subsystem card evidence loader | `backend/core/knowledge/health_system_card_evidence.py` | CONFIRMED — runtime code |
| Proof-of-pathway KB package (insulin resistance) | `knowledge_bus/packages/pkg_insulin_resistance/` | CONFIRMED — full package |
| Lipid transport KB package | `knowledge_bus/packages/pkg_lipid_transport/` | CONFIRMED — full package |
| Hepatic stress KB package | `knowledge_bus/packages/pkg_hepatic_metabolic_stress/` | CONFIRMED — full package |
| Homocysteine elevation KB package | `knowledge_bus/packages/pkg_homocysteine_elevation_context/` | CONFIRMED — full package |
| Iron deficiency KB package | `knowledge_bus/packages/pkg_iron_deficiency_context/` | CONFIRMED — has signal_library |
| Iron overload KB package | `knowledge_bus/packages/pkg_iron_overload_context/` | CONFIRMED — has signal_library |
| Thyroid TSH context KB package | `knowledge_bus/packages/pkg_thyroid_tsh_context/` | CONFIRMED — has package_manifest + research_brief |

### Implementation evidence — PARTIAL (Wave 1 domains only)

`backend/core/analytics/wave1_subsystem_evidence.py` defines `_WAVE1_DOMAIN_SUBSYSTEM_ORDER` mapping 3 domains to 7 subsystems:

```
wave1_cardiovascular:
  - wave1_cv_lipid_transport        (scored_subsystem tier — visible)
  - wave1_cv_homocysteine_pathway   (hidden/support tier)
  - wave1_cv_vascular_strain        (hidden/support tier)

wave1_blood_sugar:
  - wave1_met_glycaemic_control     (scored_subsystem tier — visible)
  - wave1_met_insulin_metabolic     (hidden/support tier)

wave1_liver:
  - wave1_liv_enzyme_pattern        (support tier)
  - wave1_liv_processing_context    (support tier)
```

`PILOT_COMPILED_SUBSYSTEM_IDS` in `health_system_card_evidence.py` controls which subsystems are live vs shells.

### Subsystem classification

| Subsystem | Status |
|---|---|
| wave1_cv_lipid_transport | IMPLEMENTED — visible scored subsystem |
| wave1_cv_homocysteine_pathway | IMPLEMENTED — support/hidden subsystem |
| wave1_cv_vascular_strain | IMPLEMENTED — support/hidden subsystem |
| wave1_met_glycaemic_control | IMPLEMENTED — visible scored subsystem |
| wave1_met_insulin_metabolic | IMPLEMENTED — support/hidden subsystem |
| wave1_liv_enzyme_pattern | IMPLEMENTED — flat domain evidence |
| wave1_liv_processing_context | IMPLEMENTED — flat domain evidence |
| Blood/iron subsystems | NOT FOUND — no assembler entry despite KB packages |
| Thyroid subsystems | NOT FOUND — pkg_thyroid_tsh_context exists but no subsystem assembler |
| Kidney subsystems | NOT FOUND — no assembler entry |
| Inflammation subsystems | NOT FOUND in assembler — pkg_chronic_inflammation exists |
| Hormone subsystems | DEFERRED — per User Health to Systems Map strategy |

### Gaps

1. Only cardiovascular and blood sugar have visible scored subsystems. Liver has flat domain evidence, not scored subsystems.
2. 3 remaining launch-core domains have no subsystem assembly despite KB packages existing for their key markers.
3. Minimum subsystem depth for beta: at least one scored visible subsystem per live domain (existing PoP pattern).

### Reusable source material

- `wave1_subsystem_evidence.py` — the subsystem assembly pattern. Extend, do not rebuild.
- `PILOT_COMPILED_SUBSYSTEM_IDS` mechanism — extend for new domain subsystems.
- `pkg_thyroid_tsh_context`, `pkg_iron_deficiency_context`, `pkg_iron_overload_context` — KB packages supporting thyroid and blood/iron subsystem card evidence.

### Recommended next action

Before implementing new subsystem assembly for the 3 missing domains, confirm which signals each KB package contributes and how they map to the Wave 1 subsystem tiers — this should be a discovery/mapping sprint before any code sprint.

---

## Block 3 — Layer B deterministic intelligence, clinician report and boilerplate prose estate

### Confirmed assets

| Asset | File path | Evidence class |
|---|---|---|
| Clinician report compiler | `backend/core/analytics/report_compiler_v1.py` | CONFIRMED — runtime code |
| Clinician report contract | `backend/core/contracts/clinician_report_v1.py` | CONFIRMED — typed contract |
| Narrative report compiler (N-8) | `backend/core/analytics/narrative_report_compiler_v1.py` | CONFIRMED — runtime code |
| Narrative report contract | `backend/core/contracts/narrative_report_v1.py` | CONFIRMED — typed contract |
| IDL contract | `backend/core/contracts/interpretation_display_layer_v1.py` | CONFIRMED |
| Layer B → Layer C handoff object | `backend/core/contracts/narrative_payload_v1.py` | CONFIRMED — v1.1 schema |
| Narrative payload builder | `backend/core/analytics/narrative_payload_builder_v1.py` | CONFIRMED |
| Retail biomarker explainer registry | `backend/ssot/retail_explainer_v1/registry.yaml` | CONFIRMED — 364 lines, 17 biomarkers + 9 systems |
| Pathway explainers (N-5) | `knowledge_bus/pathway_explainers_v1/pathway_explainers_v1.yaml` | CONFIRMED |
| Interpretation entities (N-7) | `knowledge_bus/interpretation_entities_v1/benchmark_interpretation_entities_v1.yaml` | CONFIRMED |
| Lifestyle consumer surface (LC-S13) | `backend/core/analytics/lifestyle_consumer_surface_v1.py` | CONFIRMED |
| Consumer prose safety | `backend/core/analytics/consumer_prose_safety_v1.py` | CONFIRMED — 16 prohibited substrings |
| Domain narrative functions (Wave 1) | `backend/core/analytics/domain_narrative_wave1.py` | CONFIRMED |
| LLM translation constraints | `backend/core/contracts/narrative_payload_v1.py` lines 171–179 | CONFIRMED |
| Domain narrative contract | `docs/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` | CONFIRMED — active contract |
| Layer B / Layer C ADR | `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md` | CONFIRMED — accepted |
| Retail content boundaries | `docs/architecture/RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md` | CONFIRMED |

### Key answers

**1. Is the clinician report deterministic and DB/code-driven?**  
CONFIRMED YES. `report_compiler_v1.py` ("KB-S32 deterministic report compiler") produces `ClinicianReportV1` by calling `compile_root_cause_v1()`, `build_intervention_annotations_v1()`, and `load_confirmatory_tests_registry_v1()` — all deterministic, registry-driven. No LLM in the clinician report path.

**2. Which files produce clinician_report_v1?**  
CONFIRMED: `backend/core/analytics/report_compiler_v1.py` → `ClinicianReportV1` (defined in `backend/core/contracts/clinician_report_v1.py`). Called from the orchestrator pipeline.

**3. Which files produce narrative_report_v1?**  
CONFIRMED: `backend/core/analytics/narrative_report_compiler_v1.py` (N-8) → `NarrativeReportV1` (defined in `backend/core/contracts/narrative_report_v1.py`). Module docstring: "Consumes governed knowledge_bus assets (N-5..N-7) and orchestrator meta; no LLM."

**4. Which files produce interpretation_display_layer_v1?**  
CONFIRMED: `backend/core/contracts/interpretation_display_layer_v1.py` defines `InterpretationDisplayLayerBundleV1`. Assembled by `domain_score_assembler.py` which calls `_select_primary_idl()`. UAT confirmed 11 IDL records produced at runtime.

**5. Where does prose currently come from?**  
CONFIRMED — Multiple deterministic sources:
- `domain_narrative_wave1.py` — Wave 1 headline/contributor/consequence/confidence sentences compiled from IDL records and signal states
- `narrative_report_compiler_v1.py` — consumes N-5 (pathway explainers), N-6 (functional interpretation), N-7 (interpretation entities) from knowledge_bus YAML
- `lifestyle_consumer_surface_v1.py` — deterministic lifestyle context paragraphs (LC-S13)
- `intervention_annotation_formatter_v1.py` — deterministic statin/medication annotation suffix
- `consumer_prose_safety_v1.py` — safety filters and retail display label sanitization

**6. Is prose hardcoded, package-driven, YAML-driven or compiler-generated?**  
CONFIRMED — **Compiler-generated from YAML assets.** The narrative compiler reads `pathway_explainers_v1.yaml` (N-5), `functional_interpretation_v1.yaml` (N-6), `benchmark_interpretation_entities_v1.yaml` (N-7), and `retail_explainer_v1/registry.yaml`. Domain narrative sentences are compiled from IDL records and signal state values — not free-text hardcoded.

**7. Do we already have boilerplate explainer libraries?**  
PARTIAL. `retail_explainer_v1/registry.yaml` (v1.0.1, 364 lines) contains biomarker-level boilerplate explainers. Confirmed entries: glucose, hba1c, insulin, total_cholesterol, ldl_cholesterol, hdl_cholesterol, triglycerides, non_hdl_cholesterol, apob, creatinine, egfr, alt, ast, hemoglobin, ferritin, vitamin_d, tsh — **17 biomarkers** plus 9 system-level explainers. Every entry ends with the standard disclaimer. Full panel coverage is NOT confirmed. `pathway_explainers_v1.yaml` has multi-paragraph pathway explainers for one_carbon_methylation_homocysteine and lipid_transport pathways.

**8. Is there research material that can become such libraries?**  
CONFIRMED YES. 20+ `knowledge_bus/research/investigation_specs/inv_*.yaml` files cover individual biomarker findings (alt, crp, ferritin, hba1c, homocysteine, ldl, triglycerides, tsh, uric acid, vitamins, etc.). 187 KB packages contain `research_brief.yaml` files for pathway topics. This raw material can be promoted to expanded explainer libraries via the existing KB promotion pipeline.

**9. Can Layer B currently provide Gemini with structured source material?**  
CONFIRMED YES (architecturally) / PARTIAL (not yet activated). `NarrativePayloadV1` (v1.1) bundles: `report_v1`, `top_findings`, `root_cause_v1`, `section_intents`, `evidence_boundaries`, `score_hierarchy`, `claim_boundaries` (allowed_claim_strength, prohibited_claim_patterns), and `future_llm_translation_constraints` (llm_role = "translate_governed_brief_only"). Built by `narrative_payload_builder_v1.py` deterministically. Gemini is not yet consuming it in production.

**10. What is missing before Layer B is Gemini-ready?**  
- Activation of the `live_gemini` runtime mode in production (currently inactive)
- Gemini prompt template consuming `NarrativePayloadV1` structure — `prompts.py` predates this contract and must be rewritten
- Validation of Gemini output against `NarrativePayloadV1` section intents (validator_v2.py covers some prohibited patterns but NarrativePayload-specific validation is not confirmed)
- Decision on whether `NarrativeReportV1` (deterministic compiler) is replaced by or supplemented with Gemini output

### Gaps

1. Boilerplate explainer library: 17 of ~79 biomarkers in a typical panel are covered. Coverage for renal, blood/iron and additional thyroid markers not confirmed.
2. N-5 pathway explainers and N-7 interpretation entities confirmed for homocysteine/one-carbon and lipid pathways. Coverage for renal, thyroid, blood/iron pathways not confirmed from this audit.
3. "Do not say" vocabulary (`_FORBIDDEN_SUBSTRINGS`) is distributed across code constants, not in a standalone governance document.
4. Missing-marker handling language exists in `ClinicianReportV1.data_quality` but completeness for all edge cases is INFERRED.

### Reusable source material

- `NarrativePayloadV1` — the Layer B → Layer C contract. **DO NOT reinvent.** Extend if needed.
- `retail_explainer_v1/registry.yaml` — biomarker education boilerplate. Extend, do not replace.
- `pathway_explainers_v1.yaml` (N-5), `benchmark_interpretation_entities_v1.yaml` (N-7) — build further entries on this established pattern.
- `DEFAULT_LLM_PROHIBITED_ACTIONS` and `DEFAULT_PROHIBITED_CLAIM_PATTERNS` — the anti-hallucination list. Do not reinvent.

---

## Block 4 — Gemini / Layer C personalised synthesis contract

### Confirmed assets

| Asset | File path | Evidence class |
|---|---|---|
| Layer B → Layer C ADR | `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md` | CONFIRMED — accepted ADR |
| Layer B handoff contract | `backend/core/contracts/narrative_payload_v1.py` | CONFIRMED — typed contract, v1.1 |
| LLM translation constraints | `backend/core/contracts/narrative_payload_v1.py` lines 171–179 | CONFIRMED |
| LLM output validator | `backend/core/llm/validator_v2.py` | CONFIRMED — prohibits diagnosis, confirms, rules_out, guarantees, treatment/medication recommendations |
| Gemini client (production) | `backend/core/llm/gemini_client.py` | CONFIRMED — active for PDF parsing only |
| LLM prompt templates | `backend/core/llm/prompts.py` | CONFIRMED — contains NARRATIVE_GENERATION type (predates NarrativePayloadV1; stale) |
| Legacy synthesis path disabled | `backend/core/insights/synthesis.py` line 510 | CONFIRMED — explicit "Runtime purity violation" block |
| Layer C synthesis contract freeze test | `backend/tests/enforcement/test_production_synthesis_contract_freeze.py` | CONFIRMED |
| Layer B narrative brief maturity test | `backend/tests/regression/test_layer_b1_narrative_brief_maturity.py` | CONFIRMED |
| NarrativePayloadV1 regression test | `backend/tests/regression/test_narrative_payload_compiler_regression.py` | CONFIRMED |

### Key answers

**1. Is there already a Layer B → Layer C input contract?**  
CONFIRMED YES. `NarrativePayloadV1` (schema v1.1) accepted via `ADR_WP2_layer_b_layer_c_contract_path_b.md`. Contains: typed `ReportV1`, `top_findings`, `root_cause_v1`, `section_intents`, `evidence_boundaries`, `score_hierarchy`, `claim_boundaries`, and `future_llm_translation_constraints` with `llm_role: "translate_governed_brief_only"`.

**2. Is there a Gemini output contract?**  
PARTIAL. Prohibited claims regex in `validator_v2.py` (lines 17–21) prevents diagnosis, confirms, rules_out, guarantees, treatment/supplement recommendation language. `NarrativeClaimBoundaryV1` enforces `allowed_claim_strength: pattern_and_association_only`. However, a complete Gemini **output schema** (what Gemini must return, in what structure, with what field types) is NOT confirmed as a standalone document.

**3. Are there rules preventing Gemini from adding new medical claims?**  
CONFIRMED. Multiple layers:
- `DEFAULT_LLM_PROHIBITED_ACTIONS`: `reason_independently`, `inspect_raw_biomarkers_outside_brief`, `decide_findings_or_hierarchy`, `expose_raw_pass3_hypotheses`
- `DEFAULT_PROHIBITED_CLAIM_PATTERNS`: diagnosis, confirms, rules_out, guarantees, treatment/medication/supplement recommendation
- `validator_v2.py` enforces `_PROHIBITED_CLAIM_RE` against LLM output text
- `NarrativeSectionIntentV1` has `fallback_rule: omit_section_if_sources_missing`
- `NarrativeClaimBoundaryV1.clinician_only_reserved: True`

**4. Is there a deterministic clinician report separate from Gemini?**  
CONFIRMED YES. `ClinicianReportV1` is produced entirely by `report_compiler_v1.py` — no LLM, no Gemini. Clinician report and Gemini narrative synthesis are separate parallel outputs.

**5. Does Gemini consume boilerplate/prose modules or only raw findings?**  
INFERRED / NOT YET DESIGNED. The `NarrativePayloadV1` is the proposed input (structured Layer B findings + section intents + evidence boundaries). Whether future Gemini Layer C also receives pre-assembled N-5/N-7 prose modules is deferred to sprint-level design per the ADR.

**6. Is Gemini currently inactive in the UI?**  
CONFIRMED INACTIVE for narrative synthesis.
- `synthesis.py` line 510: explicit "Runtime purity violation: legacy insight synthesis path disabled in production"
- `docs/intelligence/2026-04-12_results_why_narrative_runtime_investigation.md` line 98: "Gemini: Only when `runtime_mode` reflects `live_gemini` — otherwise not the active path for narrative text"
- `test_production_synthesis_contract_freeze.py` enforces synthesis gating
- Gemini IS active for **biomarker parsing** (PDF upload route) — this is Layer A, not Layer C

**7. What documents define the intended Layer C behaviour?**  
- `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md` — ACCEPTED ADR, primary authority
- `backend/core/contracts/narrative_payload_v1.py` — formal contract (code is the living spec)
- `docs/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` — Wave 1 narrative contract authority
- `docs/architecture/RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md` — retail scope governance
- `docs/CLAUDE_TRANSLATION_SPEC_v1.md` — referenced in STATE_OF_TRUTH_REVIEW; not read in this audit (potential Layer C scope document — read before any Layer C sprint)

### Gaps

1. No Gemini prompt template consuming `NarrativePayloadV1`. `prompts.py` `NARRATIVE_GENERATION` type predates this architecture.
2. `NarrativeReportV1` (deterministic compiler output) vs Gemini output relationship not resolved — does Gemini replace or supplement it?
3. No integration test proving Gemini would actually refuse to add new medical claims when given a `NarrativePayloadV1`.
4. No Layer C activation plan confirmed as a sprint prompt or implementation brief.
5. `LayerCInsightSection` in the frontend renders empty in current mode — no graceful consumer-facing empty state designed.

### Reusable source material

- `NarrativePayloadV1` — the input contract. **Use as the spec for Gemini prompt construction.** Do not reinvent.
- `validator_v2.py` — the LLM output validator. Extend for NarrativePayload-aware checks.
- `DEFAULT_LLM_PROHIBITED_ACTIONS`, `DEFAULT_PROHIBITED_CLAIM_PATTERNS` — reference in Gemini prompt constraints.
- `ADR_WP2_layer_b_layer_c_contract_path_b.md` — accepted architectural decision. Implement it, do not re-debate.
- `docs/CLAUDE_TRANSLATION_SPEC_v1.md` — **read this before writing any Gemini prompt template.**

---

## Block 5 — Results page / UX product layer

### Confirmed assets

**Page implementation:**
- `frontend/app/(app)/results/page.tsx` — 984-line orchestrating results page. CONFIRMED.

**Results components (all confirmed, `frontend/app/components/results/`):**
- `ResultsPrimaryHero` — hero block with severity, summary, phenotype label
- `ResultsBodyOverview` — compiled body_overview from narrative_report_v1
- `PrimaryFindingAndWhy` — clinician_report_v1 hypothesis section
- `BalancedSystemsSummary` — "What's working well" from balanced_systems_v1
- `Wave1DomainCards` — consumer_domain_scores Wave 1 health system cards
- `WhyThisLeadWonSection` — confidence / arbitration transparency
- `InterpretationPatternsSection` — IDL pattern records (retail-safe)
- `BiomarkerDials` — full marker grid with lab reference ranges
- `ResultsDrivingSignals` — top driver markers
- `UploadedPanelFidelity` — upload fidelity table
- `NarrativeLeadAndSupportingSections` / `NarrativeLongitudinalAndNextSteps` — narrative_report_v1 sections
- `ConfirmatoryTestsNextSteps` — confirmatory tests from clinician_report_v1
- `ResultsActionCardsBlock` — actions cards
- `LayerCInsightSection` — Layer C features slot (wired but shows disclosure; Gemini inactive)
- `StaleResultBanner` — result_versioning stale/incompatible display
- `ClinicianReportRenderer` — collapsed clinician view
- `ResultsDisclosureSection` — progressive disclosure wrapper
- `ResultsInvestigationSpine` — investigation context

**Frontend component tests (confirmed):**
- `frontend/tests/components/ResultsBodyOverview.lc-s4.test.tsx`
- `frontend/tests/components/ResultsDisclosureSection.lc-s4.test.tsx`
- `frontend/tests/components/Wave1DomainCards.test.tsx`
- `frontend/tests/components/Wave1SubsystemEvidenceSection.test.tsx`
- `frontend/tests/components/ClinicianReportRenderer.test.tsx`
- `frontend/tests/components/InterpretationPatternsSection.test.tsx`
- `frontend/tests/components/StaleResultBanner.test.tsx`
- And 8+ further component tests

### Key answers

**1. What is the current visible results journey?**  
Hero → Body overview → Primary finding/why → What's working well → Health system cards (Wave 1, 3 domains) → Confidence/data quality → Patterns → Marker evidence/dials → Next steps → [Clinician collapsed] → [Advanced collapsed]

**2. Which sections are temporary Layer B fallback vs intended final UI?**  
`LayerCInsightSection` is explicitly the Gemini slot — currently shows "AI-personalised narrative is not active in this view" (LC-S4 honesty copy). `NarrativeLeadAndSupportingSections` surfaces deterministic compiler output; this section may gain Gemini personalisation when Layer C is active.

**3. What will be replaced once Gemini Layer C is active?**  
`LayerCInsightSection` content, governance strip, likely portions of `NarrativeLeadAndSupportingSections`. Hero summary will gain an LLM synthesis layer.

**4. What UX components already exist?**  
18+ result-specific components confirmed. See confirmed assets above.

**5. What design documents exist?**  
UAT reports in `docs/testing/` are the primary authoritative UX evidence. No separate Figma/design spec confirmed in this audit.

**6. What known MEDIUM/LOW issues remain?**  
From UAT 2026-06-16: 6 HIGH, 6 MEDIUM, 3 LOW issues. Key:

| ID | Severity | Issue |
|----|----------|-------|
| IUAT-001 | HIGH | "B12-associated pattern" heading contradicts B12 counter-evidence |
| IUAT-002 | HIGH | "Pattern groups unavailable" despite 3 clusters existing |
| IUAT-003 | HIGH | "79 markers" vs "9 of 9 expected" — user cannot reconcile |
| IUAT-004 | HIGH | Raw markdown `**Cardiovascular 4 Biomarkers**` visible in body overview |
| IUAT-005 | HIGH | Hero/subline dual framing (homocysteine vs Vascular Inflammation Risk) |
| IUAT-006 | HIGH | Transferrin "Critical" without ferritin context |

**7. What should not be polished until architecture is stable?**  
Deterministic Layer B compiler copy sections that will be replaced by Gemini personalisation. Governance strip wording. Hero subline framing. Pattern group explanatory copy.

### Gaps

- 6 HIGH UAT issues unresolved at time of audit
- No consumer-validated persona testing (external user sessions)
- No mobile/responsive UX audit documented
- `LayerCInsightSection` has no graceful consumer-facing empty state beyond disclosure text
- Post-r2 commits may address some HIGH issues — a closure UAT has not been published

### Reusable source material

- UAT defect register (IUAT-001 to IUAT-015) — canonical input for next results-page fix sprint
- `FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS` — controls section order; do not redesign without reviewing
- `frontend/app/lib/lcS4ResultsCopy.ts` — LC-S4 honesty/disclosure copy source

---

## Block 6 — Medical safety, research provenance and governance

### Confirmed assets

| Asset | File path | Evidence class |
|---|---|---|
| Promotion protocol (active) | `docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md` | CONFIRMED |
| KB SOP (active governance) | `docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md` | CONFIRMED |
| Consumer prose safety filter | `backend/core/analytics/consumer_prose_safety_v1.py` | CONFIRMED — 16 prohibited substrings |
| Retail explainer registry | `backend/ssot/retail_explainer_v1/registry.yaml` | CONFIRMED — 17 biomarkers + 9 systems |
| Lab range protection test | `backend/tests/test_scoring_lab_range_only.py` | CONFIRMED |
| No SSOT during scoring test | `backend/tests/test_scoring_no_ssot_hooks.py` | CONFIRMED |
| SSOT integrity test | `backend/tests/test_ssot_integrity.py` | CONFIRMED |
| Medical frame identity governance | `docs/architecture/MED-FRAME-1_signal_family_contextual_frame_architecture.md` | CONFIRMED |
| Context modifier governance | `docs/architecture/CONTEXT-MOD-1_questionnaire_and_medication_modifier_governance.md` | CONFIRMED |
| Output authority provenance contract | `backend/core/contracts/output_authority_provenance_v1.py` | CONFIRMED |
| Output authority provenance builder | `backend/core/analytics/output_authority_provenance_builder_v1.py` | CONFIRMED |
| Output authority provenance test | `backend/tests/regression/test_output_authority_provenance.py` | CONFIRMED |
| Research-to-runtime traceability matrix | `docs/architecture/research_to_runtime_traceability_matrix.md` | CONFIRMED |
| Package provenance policy | `docs/architecture/package_provenance_policy.md` | CONFIRMED |
| Research-to-runtime ADR | `docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md` | CONFIRMED |
| 187 KB packages | `knowledge_bus/packages/` | CONFIRMED — counted |
| 20+ investigation specs | `knowledge_bus/research/investigation_specs/` | CONFIRMED |
| Pass 3 classification audit | `knowledge_bus/research/KB-S52A_PREFLIGHT_AUDIT_Batches_3-7_Pass3.md` | CONFIRMED |

### Key answers

**1. Where is the medical research stored?**  
`knowledge_bus/packages/` (187 packages with `package_manifest.yaml`, `research_brief.yaml`, `signal_library.yaml`), `knowledge_bus/research/` (investigation specs, study documents, Pass 3 audits, medical reviews).

**2. How does research become runtime intelligence?**  
KB packages contain `signal_library.yaml` files consumed by backend `signal_evaluator.py`. Promotion is governed by `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md` and tracked by KB SOP v1.3.1.

**3. Are source materials preserved?**  
PARTIAL. Package manifests record `source_document` paths. `source_field_preservation_audit.yaml` seen in pilot packages. Not confirmed for all 187 packages.

**4. Are medical claims traceable to research?**  
PARTIAL. `research_to_runtime_traceability_matrix.md` exists. Research brief in each package records study provenance. End-to-end traceability not systematically asserted by tests.

**5. Are package promotions governed?**  
YES. Promotion protocol v1.1 documented. KB SOP v1.3.1 active.

**6. Are rejected/deferred signals tracked?**  
PARTIAL. Classification audits exist (KB-S52A, KB-S53, KB-S57). No systematic runtime registry for rejected signals found.

**7. Are safety rules enforced by tests/validators?**  
YES. `consumer_prose_safety_v1.py` with `PROHIBITED_CONSUMER_SUBSTRINGS` (16 entries) runtime-enforced. `test_scoring_lab_range_only.py`, `test_scoring_no_ssot_hooks.py`, Sentinel `test_lc_s16_17_19_kb_surface_payload_contract.py` (consumer payload internal field leakage).

**8. Are lab-provided ranges protected?**  
YES. Scoring engine uses lab reference ranges when provided; `UNSCORED_REASON = "missing_lab_reference_range"` when absent. `test_scoring_no_ssot_hooks.py` enforces no SSOT during scoring. `test_scoring_lab_range_only.py` confirms test cases: `test_hdl_with_lab_bounds_gets_scored`, `test_ldl_without_lab_bounds_is_unscored_with_reason`.

**9. Is there evidence that raw Pass 3 material is not read at runtime?**  
INFERRED. Signal libraries in packages are the runtime assets. `research_brief.yaml` is source preservation only. KB SOP governs this separation. Not directly asserted by an end-to-end test.

### Gaps

- No systematic test asserting that raw Pass 3 study files are not imported at runtime
- No automated clinical safety gate in CI
- Retail explainer registry covers only 17 of ~79 biomarkers in a typical panel — major gap for consumer education depth
- Source field preservation audit not confirmed across all 187 packages
- No runtime rejected-signals registry for transparency

---

## Block 7 — Auditability, reproducibility and regulatory-grade traceability

### Confirmed assets

| Asset | File path | Evidence class |
|---|---|---|
| Replay manifest contract | `backend/core/contracts/replay_manifest_v1.py` | CONFIRMED — v1.0.0, 25+ component version strings and hashes |
| Result versioning policy | `backend/core/dto/result_versioning_policy_v1.py` | CONFIRMED — three-state: current/stale/incompatible |
| Persisted replay contract | `backend/core/dto/persisted_replay_contract_v1.py` | CONFIRMED |
| Frontend contract (result_version) | `backend/core/dto/frontend_contract_v1.py` | CONFIRMED — result_version in export list |
| Replay manifest builder | `backend/core/analytics/replay_manifest_builder.py` | CONFIRMED |
| Snapshot linker | `backend/core/analytics/snapshot_linker.py` | CONFIRMED — longitudinal linkage |
| Stale result banner component | `frontend/app/components/results/StaleResultBanner.tsx` | CONFIRMED — consumes result_versioning DTO |
| Stale result banner test | `frontend/tests/components/StaleResultBanner.test.tsx` | CONFIRMED |
| Replay sentinel pack | `sentinel/packs/scaffold_lc_s20_22_replay_render_v1.json` | CONFIRMED |
| Launch core protection sentinel | `sentinel/packs/lc_s20_ab_launch_core_v1.json` | CONFIRMED |
| LAUNCH-CORE-3 policy | `docs/architecture/LAUNCH-CORE-3_result_versioning_replay_and_regeneration_policy.md` | CONFIRMED — LOCKED |
| Compile manifest ADR | `docs/architecture/ADR-RT-004_compile_manifest_and_package_provenance_policy.md` | CONFIRMED |

**ReplayManifestV1 confirmed fields (lines 22–160):**
- `unit_registry_version`, `ratio_registry_version`, `cluster_schema_version`, `cluster_schema_hash`
- `insight_graph_version`, `confidence_model_version`, `derived_markers_registry_version`
- `relationship_registry_version/hash`, `biomarker_context_version/hash`
- `scoring_policy_version/hash`, `evidence_registry_version/hash`
- `state_transition_version/hash`, `state_engine_version/hash`, `precedence_engine_version/hash`
- `causal_layer_version/hash`, `calibration_version/hash`
- `conflict_registry_version/hash`, `arbitration_registry_version/hash`, `arbitration_version/hash`
- `explainability_version/hash`, `bio_stats_engine_version`, `system_burden_engine_version`
- `burden_hash`, `linked_snapshot_ids`, `analysis_result_version`

**LAUNCH-CORE-3 lineage table (from doc):**

| Field | Status |
|-------|--------|
| `analysis_id` | YES — implemented |
| `result_version` | YES — implemented |
| `replay_manifest` | YES — implemented |
| `raw_biomarkers` | YES — stored |
| `questionnaire_data` | YES — stored |
| `engine_version` / `pipeline_version` | PARTIAL |
| `result_version_id` / parent linkage | NO |
| `supersedes_*` / `superseded_by_*` | NO |
| `raw_input_hash` / payload hashes | NO — not persisted on analysis row |
| `knowledge_estate_index_hash` | PARTIAL — inside replay manifest |
| `active_authority_manifest_hash` | NO |

### Key answers

**1. Can a result be reproduced exactly?**  
PARTIAL. Replay manifest captures component versions and hashes. Raw biomarkers and questionnaire_data stored. Engine/pipeline version partial. Full deterministic replay not yet end-to-end tested with hash verification of output.

**2. Are hashes used?**  
YES — extensively. 15+ deterministic hashes in `ReplayManifestV1` for every major registry and engine component.

**3. Are runtime packages versioned?**  
YES — per component in `ReplayManifestV1`.

**4. Are prompts/prose/compiler versions captured?**  
PARTIAL — compiler versions are captured. Gemini prompt versions not captured (Gemini inactive).

**5. Are user inputs preserved?**  
YES — `raw_biomarkers` and `questionnaire_data` stored per LAUNCH-CORE-3.

**6. Is result_versioning working?**  
YES — confirmed by UAT 2026-06-16 (compatible=true, stale=false, render_blockers=[]).

**7. Are stale/incompatible result protections implemented?**  
YES — `result_versioning_policy_v1.py` three-state detection and `StaleResultBanner` in UI.

**8. Are analysis artefacts immutable?**  
YES per principle — `PersistenceService.save_live_analysis_after_run` writes immutable snapshot. Policy: never silently overwrite (per LAUNCH-CORE-3).

**9. What would be needed for Class II-style auditability?**  
Missing: `raw_input_hash` on analysis row, parent/supersedes linkage, `knowledge_estate_index_hash` (not fully implemented), `active_authority_manifest_hash`, formal audit log of who approved each analysis, regulatory claim inventory, design history file, systematic change control documentation.

### Gaps

- No `raw_input_hash` persisted on analysis row (LAUNCH-CORE-3 acknowledges this gap explicitly)
- No parent/supersedes lineage for regenerated results
- No `active_authority_manifest_hash`
- No formal end-to-end replay test demonstrating same inputs → same outputs (hash verified)
- No audit log of user-level access or clinician review events

---

## Block 8 — Phenotype panels, edge-case estate and beta validation gates

### Confirmed assets

**Named panel fixtures (`backend/tests/fixtures/panels/`):**
- `ab_full_panel.json`, `ab_full_panel_with_profiles.json`, `ab_full_panel_with_ranges.json`, `ab_full_panel_with_ranges_test0.json`, `ab_n9b_lifestyle_bridge.json`
- `vr_full_panel.json`, `vr_full_panel_with_ranges.json`
- `amber_hepatic.json`, `canonical_small.json`, `green_metabolic.json`, `red_metabolic.json`, `lab_reference_profile_micro.json`
- `panel_acceptance_profiles_v1.yaml`

**Top-level fixtures:**
- `backend/tests/fixtures/golden_panel_160.json`, `golden_panel_160_collision_free.json`
- `backend/tests/fixtures/golden_panel_sprint14_2_thyroid_immune_mini.json`

**Phenotype fixtures (`backend/tests/fixtures/panels/phenotypes/`) — 11 confirmed:**
- `ph_hba1c_metabolic_stress_v1.json`
- `ph_hepatic_alt_inflammatory_v1.json`
- `ph_iron_deficiency_inflammation_v1.json`
- `ph_iron_overload_v1.json`
- `ph_lipid_residual_ldl_favourable_transport_v1.json`
- `ph_metabolic_early_ir_v1.json`
- `ph_one_carbon_homocysteine_macrocytosis_v1.json`
- `ph_renal_stress_v1.json`
- `ph_thyroid_lipid_disturbance_v1.json`
- `ph_tsh_axis_metabolic_v1.json`
- `ph_vascular_hcy_inflammation_v1.json`
- `phenotype_expectations_v1.yaml`

**Lifestyle fixtures:**
- `backend/tests/fixtures/lifestyle_minimal.json`
- `backend/tests/fixtures/lifestyle_musculoskeletal_only.json`

**Sentinel packs — 16 guarded defect classes:**

| Defect class | Guarding test |
|---|---|
| `ggt_alias_miss` | `test_ggt_alias_regression.py` |
| `bilirubin_canonical_mismatch` | `test_bilirubin_alias_regression.py` |
| `slug_leakage` | `test_slug_leakage_regression.py` |
| `wave1_contradiction` | `test_lc_s5_proving_checks.py` |
| `persisted_result_replay` | `test_lc_s20_22_persisted_replay_sentinel_phase2.py` |
| `narrative_compiler_why_surface` | `test_narrative_compiler_why_surface_regression.py` |
| `questionnaire_exercise_unknown` | `test_obs2_questionnaire_exercise_unknown_regression.py` |
| `narrative_payload_assembly` | `test_narrative_payload_compiler_regression.py` |
| `statin_signal_isolation` | `test_lc_s4_statin_signal_isolation_regression.py` |
| `biomarker_value_reference_unit_incoherence` | `test_lc_s8_biomarker_unit_reference_incoherence_regression.py` |
| `frontend_section_not_backed_by_governed_source` | `test_lc_s16_17_19_kb_surface_payload_contract.py` |
| `knowledge_asset_not_surfaced_when_available` | `test_lc_s16_17_19_kb_surface_payload_contract.py` |
| `generic_fallback_used_when_governed_asset_exists` | `test_lc_s16_17_19_kb_surface_payload_contract.py` |
| `consumer_payload_internal_field_leakage` | `test_lc_s16_17_19_kb_surface_payload_contract.py` |
| `dto_frontend_contract_breakage` | `test_lc_s16_17_19_kb_surface_payload_contract.py` |
| `raw_signal_or_internal_id_visible` | `test_lc_s16_17_19_kb_surface_payload_contract.py` |

**Additional sentinel packs:**
- `sentinel/packs/day_one_architecture_guardrails_v1.json`
- `sentinel/packs/lc_s10b_launch_core_protection_v1.json`
- `sentinel/packs/lc_s8d_unit_governance_v1.json`
- `sentinel/packs/medical_intelligence_architecture_guardrails_v1.json`

**Signal suppression/trigger tests (`backend/tests/regression/test_active_signal_context_gate_reachability.py` — CONFIRMED):**
- Pregnancy suppression: FAI high, FT3 low, free testosterone high with pregnancy answered yes
- AAS suppression: `test_genuine_aas_suppresses_fai_high`
- DHEA supplementation: `test_dhea_supplementation_answered_yes_still_suppresses_fai_and_ft_high`
- Missing field handling: `test_missing_sex_suppresses_fai_high`, `test_missing_age_suppresses_free_testosterone_high`
- Not-answered vs absent distinction: `test_pregnancy_not_answered_allows_when_answered_no_also_valid`
- Ordinary supplements non-suppression: `test_ordinary_supplements_do_not_suppress_fai_high`
- Low testosterone symptoms: `test_free_testosterone_low_reachable_via_low_testosterone_symptoms`

**Thyroid gating (`backend/tests/regression/test_batch2_thyroid_tsh_gating.py`):**
- `test_ft3_high_does_not_emit_when_tsh_absent`
- `test_ft4_high_does_not_emit_when_tsh_absent`

**Missing marker / incomplete panel tests (confirmed in integration):**
- `test_analysis_missing_hba1c_returns_meta_with_downgrades`
- `test_incomplete_biomarker_panel_scoring_integration`
- `test_empty_biomarker_panel_scoring_integration`

**Beta readiness documents:**
- `docs/testing/HealthIQ_AI_Agentic_Testing_Strategy_Background_and_Proposal.md`
- `docs/testing/HealthIQ_AI_Background_Testing_Operating_Model_v1.md`
- `docs/testing/HealthIQ_AI_Phase_1_Sentinel_Execution_Brief.md`
- `docs/testing/healthiq_sentinel_phase1_implementation_report.md`
- `docs/architecture/ARCH-RT-5_full_regeneration_and_launch_gate_report.md`

### Key answers

**1. What test panels already exist?**  
AB (4 variants), VR (3 variants), amber_hepatic, canonical_small, green_metabolic, red_metabolic, lab_reference_profile_micro, golden_panel_160 (2 variants), thyroid/immune mini, 11 phenotype panels, 2 lifestyle panels, 2 arbitration scenario files.

**2. Which phenotypes are covered?**  
11 phenotypes: HbA1c metabolic stress, hepatic ALT inflammatory, iron deficiency + inflammation, iron overload, lipid/LDL residual, early insulin resistance, one-carbon/homocysteine/macrocytosis, renal stress, thyroid-lipid disturbance, TSH axis metabolic, vascular Hcy/inflammation.

**3. Which active signals have trigger/suppression tests?**  
FAI high, free testosterone high/low, FT3 high/low, FT4 high, with pregnancy/AAS/DHEA/supplements/missing-sex/missing-age suppression. Statin isolation covered. TSH absence gating for thyroid signals.

**4. Which systems have panel fixtures?**  
Metabolic (AB/VR), hepatic (amber_hepatic), thyroid (thyroid_immune_mini, ph_thyroid, ph_tsh), renal (ph_renal_stress), hematological (iron panels). NOT FOUND: dedicated cardiovascular fixture.

**5. Which lifestyle questionnaire states are tested?**  
`lifestyle_minimal.json`, `lifestyle_musculoskeletal_only.json`. Context gate tests cover pregnancy yes/no/not_answered, supplements present/absent, AAS identified, missing sex/age. Full questionnaire permutation coverage: PARTIAL.

**6. Are there negative tests to prevent unsafe activation?**  
YES — `test_fai_high_suppresses_pregnancy_answered_yes`, `test_genuine_aas_suppresses_fai_high`, `test_missing_sex_suppresses_fai_high`, `test_ft3_high_does_not_emit_when_tsh_absent`, and others.

**7. Are missing-marker scenarios tested?**  
YES — `test_analysis_missing_hba1c_returns_meta_with_downgrades`, `test_incomplete_biomarker_panel_scoring_integration`, `test_empty_biomarker_panel_scoring_integration`.

**8. Are contradictory-marker scenarios tested?**  
PARTIAL — Sentinel `wave1_contradiction` class covers domain card band label vs consequence copy contradiction. `arbitration_scenarios_v1.json` and `v2.json` cover arbitration conflict scenarios. Dedicated contradictory biomarker panel fixture (e.g. high ferritin + low Hb) not found.

**9. Is there a beta release checklist?**  
NOT FOUND as a standalone document. Closest: UAT report verdict (PASS WITH RESERVATIONS), `ARCH-RT-5_full_regeneration_and_launch_gate_report.md`, `HealthIQ_AI_Background_Testing_Operating_Model_v1.md`.

**10. What test estate is missing before beta?**  
- Formal beta readiness checklist / gate document
- Contradictory biomarker panel fixture
- Full Layer C / Gemini test suite (Gemini inactive — no meaningful Layer C test suite)
- Consumer-facing UX regression tests (Playwright e2e is smoke/persistence only, not full journey)
- Age/sex demographic variation panels beyond missing-sex suppression
- Supplement/medication matrix beyond AAS/DHEA
- Full lifestyle questionnaire permutation coverage
- Edge-case fixtures: single-marker panel, all-normal panel, all-critical panel as named fixtures

### Gaps

- No formal beta readiness checklist
- No dedicated contradictory biomarker panel fixture
- No Layer C / Gemini test suite
- Playwright e2e coverage minimal (smoke and persistence only)
- No demographic variation panel set
- Sentinel Phase 1 is "report only" — does not block CI on new failures

---

## Key source documents found

| File path | Title | Version / Date | Block(s) | Why it matters | Confidence |
|-----------|-------|----------------|----------|----------------|------------|
| `docs/architecture/User Health to Systems Map_FINAL.md` | Health Systems Taxonomy | v0.4 | 1, 2 | The systems model authority — 8 domains, medical rationale, confidence framework | CONFIRMED |
| `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md` | Layer B → Layer C Contract ADR | Accepted | 3, 4, 5 | Accepted ADR defining NarrativePayloadV1 handoff and LLM constraints | CONFIRMED |
| `docs/architecture/LAUNCH-CORE-3_result_versioning_replay_and_regeneration_policy.md` | Immutable Result and Replay Policy | LOCKED | 7 | Defines auditability intent, current gaps, and the authoritative lineage table | CONFIRMED |
| `docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md` | KB Promotion Protocol | v1.1 | 6 | Active protocol governing research → runtime promotion | CONFIRMED |
| `docs/architecture/research_to_runtime_traceability_matrix.md` | Research-to-Runtime Traceability Matrix | — | 6 | Maps research claims to runtime assets | CONFIRMED |
| `docs/architecture/RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md` | Retail Content Class Boundaries | v1 | 3, 4, 6 | Defines what can/cannot appear in retail-facing content | CONFIRMED |
| `docs/architecture/MED-FRAME-1_signal_family_contextual_frame_architecture.md` | Medical Frame Identity Governance | — | 6 | Defines signal family contextual frame architecture | CONFIRMED |
| `docs/architecture/CONTEXT-MOD-1_questionnaire_and_medication_modifier_governance.md` | Context Modifier Governance | — | 6, 8 | Governs questionnaire and medication modifier logic | CONFIRMED |
| `docs/testing/INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_6bcbf1de_2026-06-16.md` | Full Internal UAT Results Page Audit | 2026-06-16 | 5, 8 | Most authoritative current UX state — 6 HIGH issues, 15 total defects | CONFIRMED |
| `docs/testing/HealthIQ_AI_Background_Testing_Operating_Model_v1.md` | Testing Operating Model | v1 | 8 | Framework for ongoing test governance | CONFIRMED |
| `docs/STATE_OF_TRUTH_REVIEW_2026-05.md` | State of Truth Review | 2026-05-04 | 1, 2, 3 | Cross-system state audit — key reference for what was confirmed complete | CONFIRMED |
| `docs/architecture/ARCH-RT-5_full_regeneration_and_launch_gate_report.md` | Full Regeneration and Launch Gate Report | — | 7, 8 | Prior launch gate evidence | CONFIRMED |
| `docs/architecture/package_provenance_policy.md` | Package Provenance Policy | — | 6, 7 | Governs KB package provenance | CONFIRMED |
| `docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md` | Research-to-Runtime Day One ADR | — | 6 | Foundational provenance architecture decision | CONFIRMED |
| `docs/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` | Wave 1 Domain Narrative Contract | Active | 3, 5 | Active contract for Wave 1 domain narrative structure | CONFIRMED |
| `docs/CLAUDE_TRANSLATION_SPEC_v1.md` | Claude Translation Spec | v1 | 4 | Potential Layer C scope document — referenced but not read in this audit | INFERRED |

---

## Key runtime/code assets found

| File path | Function/module | Block(s) | Runtime role | Confidence |
|-----------|----------------|----------|-------------|------------|
| `backend/core/analytics/domain_score_assembler.py` | `assemble_consumer_domain_scores_v1()` | 1, 2, 3 | Produces Wave 1 domain cards and IDL bundle | CONFIRMED |
| `backend/core/analytics/wave1_subsystem_evidence.py` | `_WAVE1_DOMAIN_SUBSYSTEM_ORDER` | 2 | Assembles 7 Wave 1 subsystems across 3 domains | CONFIRMED |
| `backend/core/analytics/report_compiler_v1.py` | `compile_clinician_report_v1()` | 3 | Produces ClinicianReportV1 — fully deterministic, no LLM | CONFIRMED |
| `backend/core/analytics/narrative_report_compiler_v1.py` | N-8 compiler | 3, 4 | Produces NarrativeReportV1 — deterministic, consumes N-5..N-7 | CONFIRMED |
| `backend/core/analytics/narrative_payload_builder_v1.py` | `build_narrative_payload_v1()` | 3, 4 | Builds NarrativePayloadV1 Layer B → Layer C handoff object | CONFIRMED |
| `backend/core/contracts/narrative_payload_v1.py` | `NarrativePayloadV1`, `NarrativeLlmTranslationConstraintsV1` | 3, 4 | Formal Layer B → Layer C contract with anti-hallucination rules | CONFIRMED |
| `backend/core/analytics/consumer_prose_safety_v1.py` | `PROHIBITED_CONSUMER_SUBSTRINGS` | 3, 6 | Runtime filter for 16 prohibited consumer strings | CONFIRMED |
| `backend/core/analytics/lifestyle_consumer_surface_v1.py` | LC-S13 lifestyle paragraphs | 3 | Deterministic lifestyle context paragraphs | CONFIRMED |
| `backend/core/llm/gemini_client.py` | Gemini API client | 4 | Active for PDF parsing (Layer A); inactive for narrative synthesis | CONFIRMED |
| `backend/core/llm/validator_v2.py` | `_PROHIBITED_CLAIM_RE` | 4 | LLM output validator — prohibits diagnosis/confirm/rules_out/guarantees | CONFIRMED |
| `backend/core/llm/prompts.py` | `NARRATIVE_GENERATION` | 4 | Stale prompt template — predates NarrativePayloadV1; do not use as-is | CONFIRMED |
| `backend/core/insights/synthesis.py` | Line 510 | 4 | Legacy synthesis path explicitly blocked in production | CONFIRMED |
| `backend/core/contracts/replay_manifest_v1.py` | `ReplayManifestV1` | 7 | Immutable execution manifest with 25+ component hashes | CONFIRMED |
| `backend/core/dto/result_versioning_policy_v1.py` | Three-state stale detection | 7 | LAUNCH-CORE-3 stale/compatible/incompatible classification | CONFIRMED |
| `backend/ssot/retail_explainer_v1/registry.yaml` | Retail explainer registry | 3, 5, 6 | 17 biomarker + 9 system educational explainers | CONFIRMED |
| `backend/ssot/scoring_policy.yaml` | 8-system scoring policy | 1, 2 | Biomarker→system mappings and score weights | CONFIRMED |
| `backend/core/contracts/output_authority_provenance_v1.py` | `OutputAuthorityProvenanceV1` | 6 | Compiled output authority provenance contract | CONFIRMED |
| `backend/core/analytics/replay_manifest_builder.py` | `build_replay_manifest_v1()` | 7 | Builds ReplayManifestV1 at run time | CONFIRMED |
| `frontend/app/(app)/results/page.tsx` | ResultsPage | 5 | 984-line results page orchestrator | CONFIRMED |
| `sentinel/sentinel_runner.py` | Sentinel runner | 8 | Phase 1 report-only regression guard | CONFIRMED |

---

## Key test assets found

| Test file | Areas covered | Block(s) | What it proves | Gaps |
|-----------|-------------|----------|----------------|------|
| `backend/tests/regression/test_active_signal_context_gate_reachability.py` | Pregnancy, AAS, DHEA, supplements, missing sex/age suppression/activation | 8 | Context-gated signal activation/suppression working correctly | No symptoms matrix; limited lifestyle permutations |
| `backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py` | Consumer payload field leakage, DTO contract stability | 5, 8 | Internal fields do not reach consumer surfaces | Coverage tied to AB panel only |
| `backend/tests/test_scoring_lab_range_only.py` | Lab range protection, no SSOT during scoring | 6 | Lab-provided ranges respected; no global default substitution | No multi-panel permutation |
| `backend/tests/test_scoring_no_ssot_hooks.py` | No SSOT access during scoring | 6 | Scoring engine does not touch SSOT at scoring time | — |
| `sentinel/packs/escaped_defects_v1.json` | 16 named defect classes: alias, slug, replay, narrative, statin, unit coherence | 8, 6, 7 | Named regression prevention suite | Phase 1 report-only; Gemini path unguarded |
| `backend/tests/integration/test_criticality_integration.py` | Missing marker downgrade, criticality | 8, 6 | Missing HbA1c causes correct downgrade | Single missing-marker case only |
| `backend/tests/regression/test_batch2_thyroid_tsh_gating.py` | TSH-absent gating for thyroid signals | 8 | Thyroid signals suppressed without TSH | Limited to 2 signals |
| `backend/tests/enforcement/test_production_synthesis_contract_freeze.py` | Synthesis path gating | 4, 8 | Gemini synthesis is blocked in production | — |
| `backend/tests/enforcement/test_layerc_purity_no_raw_panel_reads.py` | Layer C must not read raw panel | 4, 6 | Layer C purity boundary enforced | — |
| `backend/tests/regression/test_narrative_payload_compiler_regression.py` | NarrativePayloadV1 assembly | 3, 4 | Layer B → Layer C payload assembles correctly | No Gemini consumption test |
| `backend/tests/regression/test_layer_b1_narrative_brief_maturity.py` | Layer B narrative brief maturity | 3 | Layer B brief meets readiness threshold | — |
| `backend/tests/regression/test_med_frame_identity_index.py` | Medical frame identity index | 6 | Frame identity catalogue intact | — |
| `backend/tests/regression/test_context_modifier_catalogue.py` | Context modifier catalogue | 6, 8 | Context modifier registry intact | — |
| `frontend/tests/components/Wave1DomainCards.test.tsx` | Wave 1 domain card rendering | 5 | Cards render from consumer_domain_scores | Coverage for 3 domains only |
| `frontend/tests/components/StaleResultBanner.test.tsx` | Stale result banner | 7, 5 | Versioning state drives correct UI disclosure | — |

---

## Key research/provenance assets found

| Research file / package | Biomarkers/systems covered | Promotion state | Runtime-consumed | Source preservation | Gaps |
|------------------------|---------------------------|----------------|-----------------|--------------------|----|
| `knowledge_bus/packages/pkg_insulin_resistance/` | HbA1c, insulin, glucose, HOMA-IR proxies | PROMOTED — full package | YES — signal_library.yaml consumed | research_brief.yaml preserved | — |
| `knowledge_bus/packages/pkg_lipid_transport/` | LDL, HDL, triglycerides, TC:HDL, ApoB | PROMOTED — full package | YES | research_brief.yaml + clinical_signoff.md | — |
| `knowledge_bus/packages/pkg_hepatic_metabolic_stress/` | ALT, AST, GGT, bilirubin | PROMOTED — full package | YES | research_brief.yaml + clinical_signoff.md | — |
| `knowledge_bus/packages/pkg_chronic_inflammation/` | CRP, WBC, fibrinogen | PROMOTED — package_manifest + research_brief | YES (signal_library) | research_brief.yaml | No clinical_signoff confirmed |
| `knowledge_bus/packages/pkg_homocysteine_elevation_context/` | Homocysteine, B12, folate | PROMOTED — full package | YES | All four files including clinical_signoff | — |
| `knowledge_bus/packages/pkg_thyroid_tsh_context/` | TSH, FT3, FT4 | PARTIAL — package_manifest + research_brief | PARTIAL — signal_library status not confirmed | research_brief.yaml | No subsystem assembler wires it |
| `knowledge_bus/packages/pkg_iron_deficiency_context/` | Ferritin, serum iron, TIBC, haemoglobin | PARTIAL — signal_library confirmed | PARTIAL | Not confirmed | No domain card wires it |
| `knowledge_bus/packages/pkg_iron_overload_context/` | Ferritin (high), transferrin saturation | PARTIAL — signal_library confirmed | PARTIAL | Not confirmed | No domain card wires it |
| `knowledge_bus/packages/pkg_s24_*/` (8 packages) | Various context markers | PROMOTED — series | YES | Per-package manifest | Sprint-specific |
| `knowledge_bus/research/investigation_specs/` (20+ YAMLs) | Individual biomarker findings (alt, crp, ferritin, hba1c, homocysteine, ldl, etc.) | SOURCE SPEC — pre-promotion | NO — source specs only | Preserved as investigation specs | Gap: these need promotion to become runtime explainers |

---

## Existing reports we should not reinvent

| Report | Location | What it answers |
|--------|----------|----------------|
| Systems taxonomy with medical rationale | `docs/architecture/User Health to Systems Map_FINAL.md` | Full 8-domain model, confidence framework, scoring bands — the "medical LLM system taxonomy report" |
| State of Truth Review (2026-05) | `docs/STATE_OF_TRUTH_REVIEW_2026-05.md` | Cross-system implementation state, what is confirmed complete |
| Wave 1 codebase analysis v3 | `docs/Wave1-codebase-analysis_v3.md` | Implementation reality check for Wave 1 |
| UAT Results Page Full Audit | `docs/testing/INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_6bcbf1de_2026-06-16.md` | Definitive results page current state, 15 defects |
| Phase 1 Sentinel implementation report | `docs/testing/healthiq_sentinel_phase1_implementation_report.md` | Phase 1 Sentinel scope and execution evidence |
| LAUNCH-CORE-3 auditability policy | `docs/architecture/LAUNCH-CORE-3_result_versioning_replay_and_regeneration_policy.md` | Replay, versioning, and auditability intent — locked policy |
| Layer B → Layer C ADR | `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md` | Accepted Layer B/C boundary decision |
| Full regeneration and launch gate report | `docs/architecture/ARCH-RT-5_full_regeneration_and_launch_gate_report.md` | Prior launch gate evidence |
| Research-to-runtime traceability matrix | `docs/architecture/research_to_runtime_traceability_matrix.md` | Maps research claims to runtime assets |
| Retail content class boundaries | `docs/architecture/RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md` | Content class governance for consumer surfaces |
| Testing operating model | `docs/testing/HealthIQ_AI_Background_Testing_Operating_Model_v1.md` | Test governance framework |

---

## Contradictions or drift

1. **`narrative_report_compiler_v1.py` is labelled "N-8" and "Layer C" but is deterministic (no LLM).** The current "Layer C" is a deterministic narrative compiler. The ADR makes clear this is transitional. Future Gemini activation would supersede or supplement it. The naming creates confusion: the "Layer C" that exists today is not Gemini. Anyone reading Layer C references must check whether they mean the deterministic compiler path or the intended Gemini path.

2. **`prompts.py` has a `NARRATIVE_GENERATION` template that predates `NarrativePayloadV1`.** This template should not be used for Layer C Gemini synthesis without a complete rewrite against the NarrativePayloadV1 spec. Risk: a future sprint might reuse it naively.

3. **`domain_score_assembler.py` returns exactly 3 domains always** (hardcoded at line 769: `out_rows = [cv_block(), met_block(), liv_block()]`). The `scoring_policy.yaml` covers 8 systems. Adding blood/iron, thyroid and kidney requires explicit extension of the assembler — it will not auto-discover new domains from SSOT.

4. **8-system SSOT model vs 6-domain user model vs 2-second-wave model.** Internal system names (`cbc`, `nutritional`, `kidney`, `metabolic`) differ from consumer domain labels ("Blood, iron & oxygen", "Blood sugar control", "Kidney function"). The mapping is implicit in assembler code. This creates a maintenance trap: adding a domain requires knowing the SSOT-to-consumer mapping without documentation.

5. **Gemini inactive but `LayerCInsightSection` renders in the UI.** The component exists, shows disclosure copy, but does nothing substantive in production. Risk: if Gemini is activated without coordinated UX update, the consumer journey changes significantly without a planned UX sprint.

6. **UAT HIGH issues documented 2026-06-16; post-r2 commits exist.** Some HIGH issues may have been addressed but no closure UAT has been published. The HEAD state of the 6 HIGH defects is unknown from documentation evidence alone.

7. **Sentinel Phase 1 is "report only."** Sentinel guards 16 defect classes but does not block CI on new failures. `sentinel_runner.py` line 339: "Phase 1 — report only. No product code or governed assets were modified." This means Sentinel does not currently prevent regression.

8. **`ReplayManifestV1` says "no timestamps" but `result_versioning_policy_v1.py` uses timestamps for stale detection.** By design — the replay manifest and versioning DTO are separate concerns — but creates a conceptual split that could confuse future auditors.

---

## Missing assets

### Block 1

| Missing asset | Why it matters | Beta blocker | Layer C blocker | Medical credibility | Priority |
|---|---|---|---|---|---|
| Wave 1 assembler for blood/iron, thyroid, kidney domains | Only 3/6 launch-core domains exist | YES — incomplete product | YES — Layer C has nothing to synthesise for these domains | YES — missing core health interpretation areas | P0 |
| SSOT-to-consumer domain mapping documentation | Implicit mapping creates maintenance risk | NO | NO | LOW | P2 |

### Block 2

| Missing asset | Why it matters | Beta blocker | Layer C blocker | Medical credibility | Priority |
|---|---|---|---|---|---|
| Subsystem assembly for blood/iron, thyroid, kidney | No scored visible subsystems for 3 launch-core domains | YES | YES | YES | P0 |
| Minimum subsystem depth standard document | Defines what "complete" means per domain | NO | NO | LOW | P3 |

### Block 3

| Missing asset | Why it matters | Beta blocker | Layer C blocker | Medical credibility | Priority |
|---|---|---|---|---|---|
| Retail explainer registry coverage for ~62 missing biomarkers | Most biomarkers on a typical panel have no educational copy | YES — for quality beta | YES — Gemini has no boilerplate substrate for most markers | YES | P1 |
| N-5/N-7 pathway explainers for renal, thyroid, blood/iron | Narrative compiler has no assets for these domains | YES | YES | YES | P1 |
| Standalone "do not say" governance document | Prohibited vocabulary is distributed in code constants | NO | NO | MEDIUM | P3 |

### Block 4

| Missing asset | Why it matters | Beta blocker | Layer C blocker | Medical credibility | Priority |
|---|---|---|---|---|---|
| Gemini prompt template consuming NarrativePayloadV1 | No activation path exists | NO (Gemini inactive) | YES — blocks all Layer C work | N/A until contract works | P1 (pre-Layer C sprint) |
| Layer C output schema document | What Gemini must return, in what structure | NO | YES | YES | P1 |
| Integration test: Gemini refuses prohibited claims given NarrativePayloadV1 | Validates anti-hallucination contract works in practice | NO | YES | HIGH | P1 |
| Gemini Layer C activation plan (sprint prompt/brief) | No sequenced plan for transitioning from inactive to production | NO | YES | N/A | P2 |
| `docs/CLAUDE_TRANSLATION_SPEC_v1.md` — read and verify | Referenced but not read; may contain key Layer C scope | NO | POSSIBLY | MEDIUM | P2 |

### Block 5

| Missing asset | Why it matters | Beta blocker | Layer C blocker | Medical credibility | Priority |
|---|---|---|---|---|---|
| Resolution of 6 HIGH UAT defects (IUAT-001 to IUAT-006) | B12 contradiction, markdown leakage, marker count confusion, hero framing | YES — blocks retail readiness | NO | YES — trust issues | P0 |
| External consumer persona testing | Internal UAT only; no external user validation | YES for external beta | NO | HIGH | P1 |
| Mobile/responsive UX audit | Results page untested on mobile | YES for external beta | NO | LOW | P2 |
| Graceful "Gemini inactive" UX state for LayerCInsightSection | Current state is just disclosure text, no design intent | NO | YES | LOW | P2 |

### Block 6

| Missing asset | Why it matters | Beta blocker | Layer C blocker | Medical credibility | Priority |
|---|---|---|---|---|---|
| Automated clinical safety gate in CI | Safety rules currently human-governed only | NO | NO | HIGH | P1 |
| Rejected/deferred signal runtime registry | Transparency and audit trail for non-activated signals | NO | NO | MEDIUM | P2 |
| Source preservation audit for all 187 packages | Source field preservation confirmed only for pilot subset | NO | NO | MEDIUM | P2 |

### Block 7

| Missing asset | Why it matters | Beta blocker | Layer C blocker | Medical credibility | Priority |
|---|---|---|---|---|---|
| `raw_input_hash` on analysis row | Replay lineage incomplete without it | NO | NO | YES (regulatory) | P2 |
| Parent/supersedes lineage for regenerated results | No way to audit regeneration chain | NO | NO | YES (regulatory) | P2 |
| Formal end-to-end replay test (same inputs → same outputs) | Auditability claim is architectural, not verified | NO | NO | YES (regulatory) | P2 |
| `active_authority_manifest_hash` | Full estate traceability incomplete | NO | NO | YES (regulatory) | P3 |

### Block 8

| Missing asset | Why it matters | Beta blocker | Layer C blocker | Medical credibility | Priority |
|---|---|---|---|---|---|
| Formal beta readiness checklist / gate document | No structured approval gate for beta entry | YES | NO | MEDIUM | P1 |
| Layer C / Gemini test suite | No tests for the most complex future component | NO (Gemini inactive) | YES | HIGH | P1 (pre-Layer C) |
| Contradictory biomarker panel fixture | Signal arbitration confidence unverified for divergent signals | NO | NO | HIGH | P2 |
| Playwright e2e full results journey | Smoke only; regression prevention for full journey absent | YES for external beta | NO | MEDIUM | P2 |
| Demographic variation panels (age, sex beyond suppression) | Unknown behaviour for diverse beta population | YES for external beta | NO | HIGH | P2 |

---

## Recommended multi-sprint programme

### Category 1 — Discovery / recovery sprints

| Title | Objective | Blocks | Key inputs | Expected outputs | Dependencies | Risk |
|-------|-----------|--------|-----------|-----------------|-------------|------|
| S-A1: Read CLAUDE_TRANSLATION_SPEC_v1.md and map Layer C scope | Understand what is already documented for Layer C before writing any Gemini prompt | 4 | `docs/CLAUDE_TRANSLATION_SPEC_v1.md`, `NarrativePayloadV1` | Decision: is the spec complete, partial, or stale? | None | LOW |
| S-A2: Map blood/iron, thyroid, kidney domain build materials | Confirm which KB packages, signals, and SSOT entries exist for 3 missing domains | 1, 2 | `pkg_thyroid_tsh_context`, `pkg_iron_deficiency/overload_context`, `scoring_policy.yaml` | Domain build readiness map — what exists, what must be created | None | LOW |
| S-A3: Retail explainer gap analysis | Count and classify which of the ~79 typical-panel biomarkers are missing from `retail_explainer_v1/registry.yaml` | 3, 6 | `retail_explainer_v1/registry.yaml`, typical panel biomarker list | Gap list prioritised by signal frequency and clinical importance | None | LOW |

### Category 2 — Architecture alignment sprints

| Title | Objective | Blocks | Key inputs | Expected outputs | Dependencies | Risk |
|-------|-----------|--------|-----------|-----------------|-------------|------|
| S-B1: Document SSOT-to-consumer domain label mapping | Create explicit documentation of internal system names → consumer domain labels → Layer B keys | 1, 2 | `scoring_policy.yaml`, `domain_score_assembler.py` | `docs/DOMAIN_LABEL_MAPPING_v1.md` | S-A2 | LOW |
| S-B2: Resolve NarrativeReportV1 vs Gemini Layer C relationship | Decide: does Gemini replace or supplement the deterministic `narrative_report_compiler_v1.py` path? | 3, 4 | ADR, NarrativePayloadV1 contract, NarrativeReportV1 contract | ADR amendment or new ADR defining composition rule | S-A1 | STANDARD |
| S-B3: Write Gemini prompt template consuming NarrativePayloadV1 | Create the Layer C activation prompt spec | 4 | `NarrativePayloadV1`, `docs/CLAUDE_TRANSLATION_SPEC_v1.md`, `DEFAULT_LLM_PROHIBITED_ACTIONS` | Gemini prompt template v1 + output schema v1 | S-A1, S-B2 | HIGH |

### Category 3 — System / subsystem completion sprints

| Title | Objective | Blocks | Key inputs | Expected outputs | Dependencies | Risk |
|-------|-----------|--------|-----------|-----------------|-------------|------|
| S-C1: Blood iron & oxygen domain card | Implement Wave 1 assembler entry for blood/iron domain using existing KB packages | 1, 2 | `pkg_iron_deficiency_context`, `pkg_iron_overload_context`, `wave1_subsystem_evidence.py` pattern | `wave1_blood_iron` domain card in `domain_score_assembler.py` | S-A2 | STANDARD |
| S-C2: Thyroid & energy domain card | Implement Wave 1 assembler entry for thyroid domain | 1, 2 | `pkg_thyroid_tsh_context`, thyroid gating tests | `wave1_thyroid` domain card + subsystem evidence | S-A2 | STANDARD |
| S-C3: Kidney function domain card | Implement Wave 1 assembler entry for kidney domain | 1, 2 | Renal KB packages, `ph_renal_stress` phenotype fixture | `wave1_kidney` domain card | S-A2 | STANDARD |

### Category 4 — Layer B prose / clinician report sprints

| Title | Objective | Blocks | Key inputs | Expected outputs | Dependencies | Risk |
|-------|-----------|--------|-----------|-----------------|-------------|------|
| S-D1: Retail explainer registry expansion (Phase 1) | Promote investigation spec research to explainer registry for the highest-frequency missing biomarkers | 3, 6 | `knowledge_bus/research/investigation_specs/`, `retail_explainer_v1/registry.yaml` | 20+ new biomarker entries in registry | S-A3 | CONTENT |
| S-D2: N-5 pathway explainer entries for thyroid, renal, blood/iron | Add pathway explainer YAML entries for the 3 missing domain pathways | 3 | KB packages, existing N-5 pattern | New entries in `pathway_explainers_v1.yaml` | S-C1, S-C2, S-C3 | CONTENT |
| S-D3: Fix 6 HIGH UAT defects in results page | Resolve IUAT-001 to IUAT-006 | 5 | UAT report 2026-06-16, affected components | Cleared defect register; closure UAT | None | STANDARD |

### Category 5 — Gemini Layer C sprints

| Title | Objective | Blocks | Key inputs | Expected outputs | Dependencies | Risk |
|-------|-----------|--------|-----------|-----------------|-------------|------|
| S-E1: Gemini Layer C integration test harness | Build test suite that proves Gemini respects prohibited claim rules given a NarrativePayloadV1 | 4, 8 | `NarrativePayloadV1`, `validator_v2.py`, Gemini client | Layer C integration test suite | S-B3 | HIGH |
| S-E2: Gemini Layer C controlled activation | Activate Gemini Layer C in `live_gemini` mode for internal test cohort | 4, 5 | Gemini prompt template, NarrativePayloadV1, validator_v2.py | Working Gemini Layer C output in results page | S-B3, S-E1, S-D1 | HIGH |
| S-E3: LayerCInsightSection UX for active Gemini | Design and implement the UI state when Gemini Layer C is active | 5 | S-E2 output, UX design intent | Updated `LayerCInsightSection` component | S-E2 | STANDARD |

### Category 6 — UX / results page sprints

| Title | Objective | Blocks | Key inputs | Expected outputs | Dependencies | Risk |
|-------|-----------|--------|-----------|-----------------|-------------|------|
| S-F1: Resolve UAT HIGH defects (IUAT-001–006) | Fix all 6 HIGH-severity UAT defects | 5 | UAT 2026-06-16 defect register | Closure UAT: PASS | None | STANDARD |
| S-F2: Add 3 new Wave 1 domain cards to results page | Extend Wave 1DomainCards for blood/iron, thyroid, kidney | 5, 1 | S-C1, S-C2, S-C3 domain assembler output | Frontend domain card components for 3 new domains | S-C1, S-C2, S-C3 | STANDARD |
| S-F3: Consumer persona testing | External user sessions with a controlled cohort | 5 | Results page post-S-F1 | Validated UX findings from real users | S-F1 | LOW |

### Category 7 — Safety / provenance / auditability sprints

| Title | Objective | Blocks | Key inputs | Expected outputs | Dependencies | Risk |
|-------|-----------|--------|-----------|-----------------|-------------|------|
| S-G1: `raw_input_hash` on analysis row | Implement missing hash field per LAUNCH-CORE-3 gap table | 7 | `LAUNCH-CORE-3` policy doc, `ReplayManifestV1`, `PersistenceService` | `raw_input_hash` persisted on analysis row | None | STANDARD |
| S-G2: Formal end-to-end replay test | Prove same inputs → same outputs (hash verified) | 7 | `replay_manifest_builder.py`, test fixtures | End-to-end replay integration test | S-G1 | STANDARD |
| S-G3: Source field preservation audit (all 187 packages) | Confirm or remediate source preservation across full KB estate | 6 | `knowledge_bus/packages/` | Audit report; remediation where needed | None | CONTENT |

### Category 8 — Beta validation / test estate sprints

| Title | Objective | Blocks | Key inputs | Expected outputs | Dependencies | Risk |
|-------|-----------|--------|-----------|-----------------|-------------|------|
| S-H1: Formal beta readiness gate document | Create the structured beta approval checklist | 8 | All block audits, UAT state, test estate | `docs/testing/BETA_READINESS_GATE_v1.md` | All prior sprints | LOW |
| S-H2: Contradictory biomarker panel fixture | Add fixture for divergent/contradictory biomarker patterns | 8 | Existing arbitration scenarios, `phenotype_expectations_v1.yaml` | New phenotype fixture + test assertions | None | STANDARD |
| S-H3: Playwright e2e full results journey | Extend e2e from smoke to full results journey | 8, 5 | Results page structure, existing e2e patterns | Full results journey Playwright test | S-F1 | STANDARD |
| S-H4: Sentinel Phase 2 — CI blocking mode | Elevate Sentinel from report-only to CI-blocking on known defect classes | 8 | `sentinel_runner.py`, CI configuration | Sentinel blocks CI on regression | None | STANDARD |

---

## Top 10 recommendations

1. **Resolve the 6 HIGH UAT defects (IUAT-001–006) before any further UX or Layer C work.** These are trust issues. A results page with a B12 heading that contradicts counter-evidence, visible markdown, and inexplicable marker counts is not a foundation for beta.

2. **Run discovery sprints S-A1, S-A2, S-A3 before commissioning any build sprints.** The estate is large and the build materials for blood/iron, thyroid and kidney likely already exist. Do not commission implementation until you know what you have.

3. **Read `docs/CLAUDE_TRANSLATION_SPEC_v1.md` immediately.** It was referenced in the State of Truth Review but not read in this audit. It may contain the Layer C specification that should govern Gemini prompt construction. Do not write a Gemini prompt template before reading it.

4. **Do not touch `prompts.py` for Layer C work without a complete rewrite.** The existing `NARRATIVE_GENERATION` prompt type predates `NarrativePayloadV1` and will produce architecturally wrong Gemini calls if reused as-is.

5. **Extend `retail_explainer_v1/registry.yaml` to cover the high-frequency biomarkers missing from the estate.** 17 of ~79 typical-panel biomarkers have educational copy. Without this, both Layer B and Layer C are educationally thin for most of the user's actual results. This is a content sprint (KB-driven), not a code sprint.

6. **Commission S-C1, S-C2, S-C3 as a sequenced programme after S-A2.** Three of six launch-core health domains are absent from the product. The KB packages likely already exist. This is the biggest structural gap after UAT defect resolution.

7. **Create the beta readiness gate document (S-H1) before entering any external beta.** There is no formal checklist. "PASS WITH RESERVATIONS" from an internal UAT is not a structured approval. The gate document should explicitly list all conditions required for external beta entry.

8. **Elevate Sentinel to CI-blocking mode (S-H4).** Phase 1 Sentinel guards 16 defect classes but currently only reports — it does not block. This means known regression patterns can ship. Elevating to CI-blocking protects the estate while new domains and features are added.

9. **Do not activate Gemini Layer C without first building and passing S-E1 (Layer C integration test harness).** The anti-hallucination contract (`NarrativePayloadV1`, `validator_v2.py`, `DEFAULT_LLM_PROHIBITED_ACTIONS`) is architecturally correct but untested against actual Gemini behaviour. Medical safety requires that the contract is verified, not assumed.

10. **Do not commission UX polish sprints on Layer B deterministic sections that will be replaced by Gemini Layer C.** The `NarrativeLeadAndSupportingSections` and `LayerCInsightSection` content will change substantially when Gemini is activated. Polish on these sections before Layer C activation is waste.

---

## Appendix A — Search log

**Key search terms used per block:**

Block 1–2: `consumer_domain_scores`, `domain_score_assembler`, `wave1`, `headline_systems`, `system_taxonomy`, `subsystem`, `insulin_resistance`, `lipid_transport`, `hepatic`, `proof_of_pathway`, `PILOT_COMPILED_SUBSYSTEM_IDS`

Block 3: `clinician_report_v1`, `narrative_report_v1`, `interpretation_display_layer_v1`, `report_compiler`, `narrative_report_compiler`, `boilerplate`, `explainer`, `evidence_for`, `evidence_against`, `lifestyle_consumer_surface`, `consumer_prose_safety`, `NarrativePayloadV1`, `DEFAULT_LLM_PROHIBITED_ACTIONS`

Block 4: `gemini`, `Layer C`, `synthesis`, `hallucination`, `NarrativePayloadV1`, `validator_v2`, `synthesis.py`, `prompts.py`, `narrative_generation`, `live_gemini`

Block 5: `ResultsPage`, `results_page`, `UAT`, `Wave1DomainCards`, `body_overview`, `PrimaryFinding`, `LayerCInsightSection`, `StaleResultBanner`, `FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS`

Block 6: `Pass 3`, `investigation_spec`, `promotion_protocol`, `Knowledge Bus`, `source_provenance`, `medical_frame_identity`, `context_modifier`, `signal_library`, `lab_range`, `PROHIBITED`, `consumer_prose_safety`, `retail_explainer`

Block 7: `result_version`, `replay_manifest`, `analysis_id`, `processing_metadata`, `hash`, `manifest`, `immutable`, `stale`, `compatible`, `render_blocker`, `snapshot_linker`, `LAUNCH-CORE-3`

Block 8: `fixture`, `phenotype`, `edge_case`, `beta_readiness`, `suppression`, `pregnancy`, `AAS`, `DHEA`, `thyroid`, `insulin_resistance`, `sentinel`, `escaped_defects`, `active_signal_context_gate_reachability`

**Notable files found during search not cited in main body:**
- `docs/intelligence/2026-04-12_results_why_narrative_runtime_investigation.md` — confirms Gemini inactive for narrative at runtime
- `backend/core/knowledge/domain_flat_card_evidence.py` — flat domain card evidence (liver pattern)
- `backend/tests/fixtures/arbitration_scenarios_v1.json`, `v2.json` — arbitration conflict test scenarios
- `backend/tests/enforcement/test_no_hardcoded_cluster_logic.py`, `test_no_derived_logic_in_insights.py` — architectural enforcement tests
- `backend/tests/enforcement/test_retail_explainer_registry_b1b.py` — guards registry is non-empty

---

## Appendix B — Evidence index

All file paths confirmed to exist during this audit:

**Architecture documents:**
- `docs/architecture/User Health to Systems Map_FINAL.md`
- `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md`
- `docs/architecture/LAUNCH-CORE-3_result_versioning_replay_and_regeneration_policy.md`
- `docs/architecture/RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md`
- `docs/architecture/MED-FRAME-1_signal_family_contextual_frame_architecture.md`
- `docs/architecture/CONTEXT-MOD-1_questionnaire_and_medication_modifier_governance.md`
- `docs/architecture/research_to_runtime_traceability_matrix.md`
- `docs/architecture/package_provenance_policy.md`
- `docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md`
- `docs/architecture/ADR-RT-004_compile_manifest_and_package_provenance_policy.md`
- `docs/architecture/ARCH-RT-5_full_regeneration_and_launch_gate_report.md`
- `docs/architecture/SIGNAL_ARCHITECTURE_COMPLETION_v1.0.md`

**Governance documents:**
- `docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.0.md`
- `docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md`
- `docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md`

**Testing documents:**
- `docs/testing/INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_6bcbf1de_2026-06-16.md`
- `docs/testing/UAT_results_page_analysis_fdf9bc74_2026-06-16.md`
- `docs/testing/UAT_results_page_analysis_b2dfa0c4_2026-05-12.md`
- `docs/testing/INVESTIGATION_fdf9bc74_result_versioning_false_incompatible_2026-06-16.md`
- `docs/testing/UAT1/UAT1_findings.md`
- `docs/testing/HealthIQ_AI_Agentic_Testing_Strategy_Background_and_Proposal.md`
- `docs/testing/HealthIQ_AI_Background_Testing_Operating_Model_v1.md`
- `docs/testing/HealthIQ_AI_Phase_1_Sentinel_Execution_Brief.md`
- `docs/testing/healthiq_sentinel_phase1_implementation_report.md`

**Other docs:**
- `docs/STATE_OF_TRUTH_REVIEW_2026-05.md`
- `docs/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md`
- `docs/Wave1-codebase-analysis_v3.md` (existence confirmed)
- `docs/intelligence/2026-04-12_results_why_narrative_runtime_investigation.md`

**Backend — analytics:**
- `backend/core/analytics/domain_score_assembler.py`
- `backend/core/analytics/wave1_subsystem_evidence.py`
- `backend/core/analytics/report_compiler_v1.py`
- `backend/core/analytics/narrative_report_compiler_v1.py`
- `backend/core/analytics/narrative_payload_builder_v1.py`
- `backend/core/analytics/lifestyle_consumer_surface_v1.py`
- `backend/core/analytics/consumer_prose_safety_v1.py`
- `backend/core/analytics/domain_narrative_wave1.py`
- `backend/core/analytics/replay_manifest_builder.py`
- `backend/core/analytics/snapshot_linker.py`
- `backend/core/analytics/output_authority_provenance_builder_v1.py`
- `backend/core/analytics/narrative_compiler_lc_s3_assembly_v1.py`

**Backend — contracts:**
- `backend/core/contracts/clinician_report_v1.py`
- `backend/core/contracts/narrative_payload_v1.py`
- `backend/core/contracts/interpretation_display_layer_v1.py`
- `backend/core/contracts/narrative_report_v1.py`
- `backend/core/contracts/replay_manifest_v1.py`
- `backend/core/contracts/output_authority_provenance_v1.py`

**Backend — DTOs:**
- `backend/core/dto/result_versioning_policy_v1.py`
- `backend/core/dto/persisted_replay_contract_v1.py`
- `backend/core/dto/frontend_contract_v1.py`

**Backend — LLM:**
- `backend/core/llm/gemini_client.py`
- `backend/core/llm/prompts.py`
- `backend/core/llm/validator_v2.py`
- `backend/core/insights/synthesis.py`

**Backend — knowledge:**
- `backend/core/knowledge/health_system_card_evidence.py`
- `backend/core/knowledge/domain_flat_card_evidence.py`

**Backend — SSOT:**
- `backend/ssot/scoring_policy.yaml`
- `backend/ssot/retail_explainer_v1/registry.yaml`

**Backend — tests:**
- `backend/tests/test_scoring_lab_range_only.py`
- `backend/tests/test_scoring_no_ssot_hooks.py`
- `backend/tests/test_ssot_integrity.py`
- `backend/tests/regression/test_active_signal_context_gate_reachability.py`
- `backend/tests/regression/test_batch2_thyroid_tsh_gating.py`
- `backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py`
- `backend/tests/regression/test_narrative_payload_compiler_regression.py`
- `backend/tests/regression/test_layer_b1_narrative_brief_maturity.py`
- `backend/tests/regression/test_narrative_compiler_why_surface_regression.py`
- `backend/tests/regression/test_context_modifier_catalogue.py`
- `backend/tests/regression/test_med_frame_identity_index.py`
- `backend/tests/regression/test_output_authority_provenance.py`
- `backend/tests/enforcement/test_production_synthesis_contract_freeze.py`
- `backend/tests/enforcement/test_layerc_purity_no_raw_panel_reads.py`
- `backend/tests/enforcement/test_retail_explainer_registry_b1b.py`
- `backend/tests/enforcement/test_no_hardcoded_cluster_logic.py`
- `backend/tests/enforcement/test_no_derived_logic_in_insights.py`
- `backend/tests/integration/test_criticality_integration.py`
- `backend/tests/integration/test_scoring_orchestrator_integration.py`
- `backend/tests/integration/test_confidence_model_isolation.py`
- `backend/tests/fixtures/panels/` (14+ panel fixtures)
- `backend/tests/fixtures/panels/phenotypes/` (11 phenotype fixtures)
- `backend/tests/fixtures/panels/phenotype_expectations_v1.yaml`
- `backend/tests/fixtures/golden_panel_160.json`, `golden_panel_160_collision_free.json`
- `backend/tests/fixtures/golden_panel_sprint14_2_thyroid_immune_mini.json`
- `backend/tests/fixtures/lifestyle_minimal.json`, `lifestyle_musculoskeletal_only.json`
- `backend/tests/fixtures/arbitration_scenarios_v1.json`, `arbitration_scenarios_v2.json`

**Frontend:**
- `frontend/app/(app)/results/page.tsx`
- `frontend/app/components/results/` (18+ component files)
- `frontend/app/lib/lcS4ResultsCopy.ts`
- `frontend/app/lib/narrativeRuntimePresentation.ts`
- `frontend/tests/components/` (12+ test files including Wave1DomainCards, StaleResultBanner, ClinicianReportRenderer, ResultsBodyOverview, etc.)

**Sentinel:**
- `sentinel/sentinel_runner.py`
- `sentinel/packs/escaped_defects_v1.json`
- `sentinel/packs/day_one_architecture_guardrails_v1.json`
- `sentinel/packs/lc_s10b_launch_core_protection_v1.json`
- `sentinel/packs/lc_s8d_unit_governance_v1.json`
- `sentinel/packs/medical_intelligence_architecture_guardrails_v1.json`
- `sentinel/packs/scaffold_lc_s20_22_replay_render_v1.json`
- `sentinel/packs/lc_s20_ab_launch_core_v1.json`

**Knowledge Bus:**
- `knowledge_bus/packages/` (187 packages total)
- `knowledge_bus/packages/pkg_insulin_resistance/` (full package)
- `knowledge_bus/packages/pkg_lipid_transport/` (full package)
- `knowledge_bus/packages/pkg_hepatic_metabolic_stress/` (full package)
- `knowledge_bus/packages/pkg_chronic_inflammation/` (full package)
- `knowledge_bus/packages/pkg_homocysteine_elevation_context/` (full package)
- `knowledge_bus/packages/pkg_thyroid_tsh_context/` (package_manifest + research_brief)
- `knowledge_bus/packages/pkg_iron_deficiency_context/` (signal_library confirmed)
- `knowledge_bus/packages/pkg_iron_overload_context/` (signal_library confirmed)
- `knowledge_bus/packages/pkg_s24_*/` (8 sprint-24 context packages)
- `knowledge_bus/pathway_explainers_v1/pathway_explainers_v1.yaml`
- `knowledge_bus/interpretation_entities_v1/benchmark_interpretation_entities_v1.yaml`
- `knowledge_bus/research/investigation_specs/` (20+ yaml files)
- `knowledge_bus/research/KB-S52A_PREFLIGHT_AUDIT_Batches_3-7_Pass3.md`
- `knowledge_bus/research/KB-S53_WAVE_C_CLASSIFICATION_AUDIT.md`
- `knowledge_bus/research/KB-S57_CBC_TRANCHE_BLOCKER_REPORT.md`

---

*Report written by Claude Code (claude-sonnet-4-6) — 2026-06-17. Read-only audit. No files modified. Parallel search: Blocks 1–4 and Blocks 5–8 searched independently and merged into this document.*
