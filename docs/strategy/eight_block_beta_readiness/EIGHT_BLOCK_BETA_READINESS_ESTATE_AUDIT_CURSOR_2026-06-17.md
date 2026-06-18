# HealthIQ AI — Eight-Block Beta Readiness Estate Audit

> Post-audit note: see `EIGHT_BLOCK_BETA_READINESS_LATE_DOCUMENT_ADDENDUM_2026-06-17.md` and `docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md` for later-discovered authority documents.

**Auditor:** Cursor (independent evidence discovery)  
**Date:** 2026-06-17  
**Mode:** Read-only — no code, documentation, branch, or implementation changes  
**Repository:** `c:\Users\abroa\HealthIQ-AI-v5`  
**Branch inspected:** `main` (working tree at audit time)

---

## Executive verdict

- **Overall maturity assessment:** **MEDIUM for internal deterministic analysis; LOW–MEDIUM for controlled external beta.** The estate has substantial Layer B compilation, a large Knowledge Bus, Wave 1 health-system cards, governance gates, and a broad test harness. It does **not** yet meet the architectural bar for “Gemini writes a short synthesis from a complete Layer B prose substrate” across all domains, nor for retail-grade consumer UX.
- **Strongest existing assets:** Day-one architecture closure and launch estate gate (`day_one_launch_estate_gate_v1.yaml`); deterministic three-layer pipeline (`orchestrator.py`, `report_compiler_v1.py`, `narrative_report_compiler_v1.py`); **186** `pkg_*` packages; **153** Pass 3 investigation specs; Wave 1 domain assembler + compiled subsystem card evidence; `NarrativePayloadV1` Layer B→C contract (ADR WP2); AB/VR/golden panel test estate; extensive audit-paper corpus.
- **Biggest gaps:** Only **3 of 6** launch-core consumer domains implemented on results page; subsystem depth deliberately collapsed to **2 visible scored subsystems**; Pass 3 hypothesis/contradiction richness largely **not promoted** to runtime cards; **production Gemini narrative synthesis not wired**; retail UX trust issues documented in UAT; beta gate **NOT_READY** on security hygiene (committed secrets per `BETA-READINESS-RECHECK-1`).
- **Areas where we risk reinventing work:** 8-domain consumer model (`User Health to Systems Map_FINAL.md`); Wave 1 subsystem YAML (`knowledge_bus/compiled/health_system_cards/`); domain narrative contract (`DOMAIN_NARRATIVE_CONTRACT_WAVE1.md`); Layer B/C ADR and `NarrativePayloadV1`; Pass 3 utilisation investigation; launch-core / LC-S / FE-R audit series; phenotype and AB/VR harnesses.
- **Areas where documentation and runtime differ:** Docs describe **6 launch-core domains**; runtime emits **`consumer_domain_scores` for 3** only. Docs describe rich subsystem trees; **MED-REV-1** hides 5 of 7 subsystems from default DTO. Pass 3 contains full hypothesis graphs; packages/runtime cards use **compiled marker lists**, not full Pass 3 semantics. Strategic docs still reference older signal counts (137–186 packages vs stale governance snapshots).
- **Whether the estate is currently beta-ready:** **CONFIRMED: No** for controlled external beta. **PARTIAL: Yes** for continued internal validation on Wave 1 panels with known reservations (`INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_6bcbf1de_2026-06-16.md`: “PASS WITH RESERVATIONS … not for external users”; `BETA-READINESS-RECHECK-1`: `NOT_READY_PENDING_BLOCKERS`).

---

## Evidence search scope

- **Directories searched:** `backend/core/`, `backend/app/`, `backend/tests/`, `backend/ssot/`, `backend/tools/`, `frontend/app/`, `knowledge_bus/` (packages, research, governance, compiled), `docs/` (architecture, intelligence, audit-papers, testing, governance, frontend, sprints, strategy), `architecture/`, `sentinel/`
- **File types searched:** `.py`, `.ts`, `.tsx`, `.yaml`, `.json`, `.md`
- **Search terms used:** systems, subsystems, Wave 1, consumer_domain_scores, clinician_report_v1, narrative_report_v1, interpretation_display_layer_v1, Layer B, Layer C, Gemini, Pass 3, investigation_specs, promotion protocol, result_version, replay_manifest, fixtures, phenotype, beta readiness, active_signal_context_gate, suppression, medical LLM, boilerplate, evidence_for, UAT
- **Known areas not accessible:** Live production database contents; external Google Docs referenced in strategy; runtime Gemini API behaviour without keys; full browser re-walk of all UAT screenshots (metadata read from audit docs)
- **Limits of audit:** Single-pass repo search; did not execute full pytest suite (282 test files counted); did not re-run architecture validators; counts are filesystem snapshots at audit time

---

## Block-by-block maturity table

| Block | Current maturity | Strongest evidence | Runtime proof | Documentation proof | Main gaps | Reuse priority |
|-------|------------------|-------------------|---------------|---------------------|-----------|----------------|
| **1 — Core health systems model** | **MEDIUM** | `User Health to Systems Map_FINAL.md`; `scoring_policy.yaml`; `domain_score_assembler.py` | 8 SSOT scoring systems; 3 Wave 1 `consumer_domain_scores` | Strategy A 6+2 domain model; DOMAIN_NARRATIVE_CONTRACT_WAVE1 | 3 launch domains not on cards; no single “medical LLM systems report” file | **HIGH** |
| **2 — Subsystems and depth model** | **MEDIUM** | Compiled card YAML; `wave1_subsystem_evidence.py`; MED-REV-1 report | 7 compiled subsystems; 2 user-visible scored | User Health Map splitting rules; MED-REV-1 visibility | 5 subsystems hidden; Wave 2 domains absent; iron/thyroid/kidney subsystems not built | **HIGH** |
| **3 — Layer B deterministic intelligence & prose** | **MEDIUM–HIGH** | `report_compiler_v1.py`, `narrative_report_compiler_v1.py`, IDL YAML, compiled cards | `clinician_report_v1`, `narrative_report_v1`, `interpretation_display_layer_v1` on DTO | LAYER-B-1 report; ADR-007; RETAIL_EXPLAINER boundaries | Full biomarker boilerplate library incomplete; Pass 3 prose not fully compiled to triggers | **HIGH** |
| **4 — Gemini / Layer C synthesis contract** | **LOW–MEDIUM** | `NarrativePayloadV1`; ADR_WP2; `validator_v2.py`; `narrative_runtime_policy.py` | Default NO-LLM; `layer_c_features` modules; upload parse uses Gemini | CLAUDE_TRANSLATION_SPEC; wp2 audit; LAYER-B-1 deferrals | Production narrative Gemini inactive; synthesis not consuming full brief | **HIGH** (contract) / **LOW** (runtime) |
| **5 — Results page / UX** | **MEDIUM** | `results/page.tsx`; Wave1 components; UAT audits | Full journey renders; stale banner logic | HealthIQ_Final_Results_Journey v6; DOMAIN-UX1 audit | Retail polish; hero/IDL mismatch; internal vocabulary leakage | **MEDIUM** |
| **6 — Medical safety & provenance** | **MEDIUM–HIGH** | Pass 3 corpus; promotion protocol; day-one gate; frame identity index | No raw Pass 3 runtime reads; context gates; validators | PASS3 utilisation audit; KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL v1.1 | Automated Pass 3 compile pipeline incomplete; some packages pre-Pass 3 lineage | **HIGH** |
| **7 — Auditability & reproducibility** | **MEDIUM** | `persisted_replay_contract_v1.py`; `result_versioning_policy_v1.py`; golden runner | `result_version`, `replay_manifest`; stale detection | LAUNCH-CORE-3 policy; ARCH-COMPLETION-3 manifest | Not Class II-grade; prompt/compiler version capture partial | **MEDIUM** |
| **8 — Phenotype panels & beta validation gates** | **MEDIUM** | AB/VR profiles; phenotype suite; governance reachability tests | `panel_acceptance_profiles_v1.yaml`; phenotype_expectations_v1 | BETA-READINESS gates; Sentinel brief | Missing-marker/contradiction matrix incomplete for all domains; no single beta checklist artefact | **HIGH** |

---

## Block 1 — Core health systems model

### Confirmed assets

| Asset | Classification | Evidence |
|-------|----------------|----------|
| 8 consumer-facing domain taxonomy (6 launch + 2 deferred) | **CONFIRMED** | `docs/architecture/User Health to Systems Map_FINAL.md` L197–230: launch-core six + Silent inflammation & Hormone balance second-wave |
| 8 SSOT scoring systems with weights | **CONFIRMED** | `backend/ssot/scoring_policy.yaml` L4–50: metabolic, cardiovascular, inflammatory, hormonal, nutritional, kidney, liver, cbc |
| Wave 1 = 3 customer domains implemented | **CONFIRMED** | `backend/core/analytics/domain_score_assembler.py` L47–51, L90–94: cardiovascular, metabolic/blood sugar, liver rails |
| Domain scoring bands 80/65/45 | **CONFIRMED** | `domain_score_assembler.py` L96–104 `_band_label_from_0_100` |
| Medical rationale for domains | **PARTIAL** | `User Health to Systems Map_FINAL.md` L234–248 medical review; `DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` per-domain narrative |
| Marker mappings per system | **CONFIRMED** | `scoring_policy.yaml` biomarker lists; `domain_score_assembler.py` `_CV_RAIL_BIOMARKERS`, `_MET_CORE`, `_HEP_CONFIDENCE_POOL` |

### Implementation evidence

- **Wave 1 consumer cards:** `assemble_consumer_domain_scores_v1()` in `domain_score_assembler.py` produces `ConsumerDomainScoreV1` for `wave1_cardiovascular`, `wave1_blood_sugar`, `wave1_liver` (**CONFIRMED** — regression tests `test_domain_ux1a_wave1_health_systems_card_scaffold.py`, `test_med_rev2_domain_card_copy_and_regeneration.py`).
- **Burden/capacity track:** `system_capacity_scores` on AnalysisDTO referenced in `DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` L35.
- **Parked/deferred:** Blood/iron/oxygen, Thyroid, Kidney, Silent inflammation, Hormone balance — **documented** in Strategy A blueprint (`docs/archive/working-papers/STRATEGY_A_IMPLEMENTATION_BLUEPRINT.md` L25–34) but **NOT FOUND** as `consumer_domain_scores` runtime rows.

### Documentation evidence

- **Authoritative consumer model:** `docs/architecture/User Health to Systems Map_FINAL.md` (v0.4) — **CONFIRMED** strongest systems taxonomy doc.
- **Wave 1 narrative contract:** `docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` (2026-04-26) — three domains only.
- **Intelligence model (schema, not systems list):** `docs/intelligence/HealthIQ_Intelligence_Model_Design_Second_Pass.md` — contradiction/longitudinal triage; authority for investigation spec schema v3.

### Priority search: “medical LLM report” defining systems/subsystems

| Search target | Result | Classification |
|---------------|--------|----------------|
| Standalone file titled “medical LLM systems report” | **NOT FOUND** | — |
| `multi_llm_research/*_Pass_3.json` (153 specs) | **CONFIRMED** | `docs/audit-papers/PASS3_research_asset_utilisation_investigation_cursor.md` L5–38 |
| `User Health to Systems Map_FINAL.md` | **CONFIRMED** | Closest **governed 8-domain consumer + subsystem** authority with medical review |
| `HealthIQ_Intelligence_Model_Design_Second_Pass.md` | **CONFIRMED** | Medical **reasoning primitive** authority, not headline systems card model |
| `STRATEGY_A_IMPLEMENTATION_BLUEPRINT.md` | **CONFIRMED** | Repo-grounded 6-domain implementation research |

### Gaps

- Launch-core **6 domains planned; 3 implemented** on consumer cards (**CONFIRMED** drift).
- Scoring policy has **8 engine systems**; consumer map has **8 domains** — mapping is many-to-many, not 1:1 (**CONFIRMED** in User Health Map L329–346).
- `hormonal` and `nutritional` scoring rails are placeholders (weight 0.0, empty biomarkers) — **CONFIRMED** `scoring_policy.yaml` L31–38.

### Reusable source material

- `User Health to Systems Map_FINAL.md` — do not rebuild domain taxonomy.
- `DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` — reuse for CV/BS/Liver copy logic.
- `STRATEGY_A_IMPLEMENTATION_BLUEPRINT.md` — gap analysis per remaining domains.
- Pass 3 batches — biomarker/system medical rationale at spec level.

### Recommended next action

Recover and ratify **one canonical systems authority index** linking: consumer domain → scoring rail → subsystem IDs → Pass 3 spec IDs — extending existing `card_authority_register_v1.yaml` / `day_one_full_traceability_manifest_v1.yaml` rather than authoring a new taxonomy from memory.

---

## Block 2 — Subsystems and depth model

### Confirmed assets

**Planned subsystems under Wave 1 headline systems** (`wave1_subsystem_evidence.py` L20–34):

| Domain | Subsystem IDs |
|--------|---------------|
| wave1_cardiovascular | `wave1_cv_lipid_transport`, `wave1_cv_homocysteine_pathway`, `wave1_cv_vascular_strain` |
| wave1_blood_sugar | `wave1_met_glycaemic_control`, `wave1_met_insulin_metabolic` |
| wave1_liver | `wave1_liv_enzyme_pattern`, `wave1_liv_processing_context` |

### Subsystem classification

| Subsystem ID | Status | Evidence |
|--------------|--------|----------|
| `wave1_met_glycaemic_control` | **implemented** (proof-of-pathway pilot) | `health_system_card_evidence.py` L25: `PILOT_SUBSYSTEM_ID`; compiled YAML with `mechanism_line`, marker roles |
| `wave1_cv_lipid_transport` | **implemented** (visible scored) | MED-REV-1: `scored_subsystem` |
| `wave1_met_insulin_metabolic` | **partially implemented** (compiled; hidden) | `visibility_tier: hidden_v1` per MED-REV-1 |
| `wave1_cv_homocysteine_pathway` | **partially implemented** (compiled; hidden) | MED-REV-1 |
| `wave1_cv_vascular_strain` | **partially implemented** (compiled; hidden) | MED-REV-1 |
| `wave1_liv_enzyme_pattern` | **partially implemented** (compiled; hidden) | MED-REV-1; liver uses flat card |
| `wave1_liv_processing_context` | **partially implemented** (compiled; hidden) | MED-REV-1 |
| Iron / thyroid / kidney subsystems | **documented but not implemented** | User Health Map L171–183; no `wave1_*` IDs in codebase |
| Silent inflammation / hormone subsystems | **parked/deferred** | User Health Map L207–213 second-wave |

### Implementation evidence

- Compiled artefacts: `knowledge_bus/compiled/health_system_cards/wave1_*.yaml` — **CONFIRMED** (7 files).
- Example richness: `wave1_met_glycaemic_control.yaml` L11–29 — `mechanism_line`, per-marker `rationale_short`, `presence_policy`.
- DTO assembly: `assemble_wave1_subsystem_evidence()` — **CONFIRMED**; returns empty for non-Wave-1 domain IDs (Wave 2 protection) L61–65.
- Minimum beta depth: **INFERRED** — MED-REV-1 deliberately limited to 2 visible scored subsystems; medical review doc states liver is **flat card** only.

### Documentation evidence

- `docs/audit-papers/MED-REV-1_wave1_subsystem_visibility_and_label_alignment_report.md` — authoritative visibility decision.
- `docs/audit-papers/DOMAIN-UX1_health_systems_card_codebase_reality_audit.md` — subsystem gap analysis (pre-DOMAIN-UX1C).

### Gaps

- User Health Map describes hierarchical sub-scores for iron, thyroid, kidney — **not implemented**.
- Pass 3 `relationship_kind` / hypotheses **not on subsystem cards** (PASS3 utilisation audit).

### Reusable source material

- All `knowledge_bus/compiled/health_system_cards/wave1_*.yaml`
- `wave1_subsystem_evidence.py` ordering constants
- MED-REV-1 visibility partition in `health_system_card_evidence.py` L38–47

### Recommended next action

Before expanding subsystem depth, **inventory hidden_v1 artefacts** for promotion candidates vs net-new subsystem design — do not rebuild the 7 compiled YAML files.

---

## Block 3 — Layer B deterministic intelligence, clinician report and boilerplate prose estate

### Specific answers

| # | Question | Answer | Confidence |
|---|----------|--------|------------|
| 1 | Is clinician report deterministic and DB/code driven? | **Yes** — compiled from insight graph + root cause via `compile_clinician_report_v1()`; not LLM-generated | **CONFIRMED** |
| 2 | Files producing `clinician_report_v1`? | `backend/core/analytics/report_compiler_v1.py` (`compile_clinician_report_v1`); `backend/core/dto/builders.py` L49; orchestrator → DTO | **CONFIRMED** |
| 3 | Files producing `narrative_report_v1`? | `backend/core/analytics/narrative_report_compiler_v1.py` (`compile_narrative_report_v1`); called from `orchestrator.py` L2219 | **CONFIRMED** |
| 4 | Files producing `interpretation_display_layer_v1`? | `backend/core/analytics/interpretation_display_layer_publish_v1.py`; source `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml` | **CONFIRMED** |
| 5 | Where does prose currently come from? | Mix: YAML KB assets, `domain_narrative_wave1.py` templates, `narrative_report_compiler_v1.py` assembly, `root_cause_compiler_v1.py` hypotheses, `consumer_prose_safety_v1.py` | **CONFIRMED** |
| 6 | Prose source types? | **Compiler-generated + YAML-driven + package explanation fields** (compile-time enrichment); not DB-driven; not ad-hoc frontend | **CONFIRMED** |
| 7 | Boilerplate explainer libraries exist? | **PARTIAL** — `pathway_explainers_v1.yaml`, `functional_interpretation_v1.yaml`, `retail_explainer_v1` SSOT, IDL records, compiled health system cards | **CONFIRMED** |
| 8 | Research promotable to libraries? | **Yes** — Pass 3 `narrative.*`, `hypotheses[]`, `supporting_markers[].rationale` per PASS3 utilisation audit | **CONFIRMED** |
| 9 | Can Layer B provide Gemini structured source material? | **PARTIAL** — `NarrativePayloadV1` with section intents, evidence boundaries, LLM constraints (`narrative_payload_v1.py`); digest in meta; not full brief on DTO | **CONFIRMED** |
| 10 | Missing before Gemini-ready? | Full brief persistence on DTO; complete boilerplate per biomarker/system triggers; Pass 3 hypothesis surfacing (CF-KBUTIL1-002); production synthesis wiring | **CONFIRMED** LAYER-B-1 |

### Confirmed assets

- **Evidence for/against/counter-evidence:** `report_compiler_v1.py` L368–492 maps `evidence_for`, `evidence_against`; IUAT-001 neutralisation L400–413 — **CONFIRMED**.
- **Missing-marker handling:** clinician `data_quality.missing_data`; domain `missing_marker_ids`; subsystem `missing_marker_ids` — **CONFIRMED**.
- **Confidence/completeness language:** `confidence_sentence_for`, `evidence_completeness_numerator/denominator` on domain cards — **CONFIRMED**.
- **Do-not-say / safety:** `consumer_prose_safety_v1.py`, `narrative_brief_enforcement_v1.py`, `NarrativeLlmTranslationConstraintsV1` — **CONFIRMED**.
- **Lifestyle modifier prose:** `lifestyle_consumer_surface_v1.py` — **CONFIRMED**.

### Documentation evidence

- `docs/audit-papers/LAYER-B-1_narrative_brief_maturity_report.md`
- `architecture/ADR-007-clinician-summary-report.md` (per AUTHORITY_MAP)
- `docs/architecture/RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md`
- `docs/audit-papers/FE_R0_results_page_prose_source_trace_audit.md`

### Gaps

- Per-biomarker triggered boilerplate library (all fields in audit prompt) — **NOT FOUND** as unified artefact.
- `NarrativeReportV1` is **deterministic Layer C output of compiler**, not Gemini — naming can confuse (**CONFIRMED** ADR_WP2 L17).
- Root-cause WHY limited to fixed target list historically (`PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` — six signals); estate may have grown — treat as **PARTIAL** until re-counted.

### Reusable source material

- Entire `report_compiler_v1.py` / `narrative_report_compiler_v1.py` chain
- `knowledge_bus/compiled/health_system_cards/`
- `NarrativePayloadV1` schema v1.1

### Recommended next action

Complete **boilerplate coverage matrix** (biomarker × trigger type × source package/IDL) from existing assets before any Gemini sprint — reuse PASS3 utilisation audit §3 as starting index.

---

## Block 4 — Gemini / Layer C personalised synthesis contract

### Specific answers

| # | Question | Answer | Confidence |
|---|----------|--------|------------|
| 1 | Layer B → Layer C input contract? | **Yes** — `NarrativePayloadV1` + `ReportV1` / `meta.insight_graph.report_v1` (Path B) | **CONFIRMED** ADR_WP2 |
| 2 | Gemini output contract? | **PARTIAL** — `validator_v2.py`; insight JSON schema; no final consumer synthesis DTO | **CONFIRMED** |
| 3 | Rules preventing new medical claims? | **PARTIAL** — validator scaffold + narrative brief prohibited actions; not production-complete | **CONFIRMED** LAYER-B-1 |
| 4 | Deterministic clinician report separate from Gemini? | **Yes** | **CONFIRMED** |
| 5 | Gemini consumes boilerplate or raw findings? | **Raw structured findings** via insight graph / prompts; not full boilerplate modules | **INFERRED** from `synthesis.py` |
| 6 | Gemini inactive in UI? | **Yes for narrative** — default NO-LLM; mock disclosure on results page; `layer_c_features` are deterministic modules | **CONFIRMED** |
| 7 | Documents defining Layer C behaviour? | ADR_WP2, `healthiq_pre_sprint1_decision_pack_FINAL.md` §3.9, `CLAUDE_TRANSLATION_SPEC_v1.md`, `wp2_layer_b_layer_c_implementation_readiness_audit.md`, LC-S3 completion note | **CONFIRMED** |

### Confirmed assets

- **Gemini integration (upload only active by default):** `backend/app/routes/upload.py` L53 — parse uses Gemini — **CONFIRMED**.
- **Double opt-in for narrative LLM:** `narrative_runtime_policy.py` L4–7 — `HEALTHIQ_NARRATIVE_LLM` + `HEALTHIQ_ENABLE_LLM` — **CONFIRMED**.
- **Test enforcement:** `test_golden_runner_default_mode_does_not_instantiate_gemini` — **CONFIRMED**.
- **Layer C UI:** `LayerCInsightSection.tsx` renders `layer_c_features` (metabolic_age, heart_insight, etc.) — **CONFIRMED**.
- **LC-S3 deterministic assembly:** `narrative_compiler_lc_s3_assembly_v1.py` — payload-driven Layer C **without** live Gemini — **CONFIRMED**.

### Gaps

- Production personalised holistic Gemini synthesis — **NOT FOUND** wired.
- `insights[]` LLM path quarantined/separate from main narrative — **CONFIRMED** card_authority_register / launch gate.
- Full validator coverage for ranked findings preservation — **OPEN** per wp2 audit C-3.

### Reusable source material

- `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md`
- `backend/core/contracts/narrative_payload_v1.py`
- `backend/core/llm/validator_v2.py`
- `docs/frontend/CLAUDE_TRANSLATION_SPEC_v1.md`

### Recommended next action

Do **not** start Gemini implementation until Layer B brief is persisted and boilerplate matrix is complete — per prompt constraints and LAYER-B-1 explicit deferral.

---

## Block 5 — Results page / UX product layer

### Specific answers

| # | Question | Answer |
|---|----------|--------|
| 1 | Current visible results journey? | Hero → body overview → primary finding/why → balanced systems → Wave 1 cards → patterns → driving signals → biomarker dials → next steps → actions link → collapsed clinician/advanced (`results/page.tsx`) |
| 2 | Temporary Layer B fallback vs final UI? | `DeterministicNarrativeSurface`, `Wave1DomainCards`, `ClinicianReportRenderer` are **governed Layer B surfaces**; `LayerCInsightSection` is deterministic feature bundle; mock-mode disclosure is **honesty fallback** |
| 3 | Replaced when Gemini Layer C active? | **INFERRED:** short holistic synthesis would subordinate mock disclosure + possibly compress narrative lead; ADR defers restructuring |
| 4 | UX components exist? | **Yes** — extensive list in `page.tsx` imports L10–39 |
| 5 | Design documents? | `HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md` (AUTHORITATIVE); `Interpretation_Display_Layer_Design_Lock.md` |
| 6 | MEDIUM/LOW issues? | UAT 6bcbf1de: B12 heading mismatch, pattern placeholder, marker-count dissonance, markdown leakage — **HIGH trust** |
| 7 | Do not polish until architecture stable? | Health system cards, hero/IDL coherence, completeness semantics — per UAT and LAUNCH-CORE audits |

### Confirmed assets

- Layout orchestration: `frontend/app/lib/resultsPageLayout.ts`
- Wave 1 cards: `Wave1DomainCards.tsx`, subsystem sections
- UAT evidence: `docs/testing/INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_6bcbf1de_2026-06-16.md`
- Stale result UX: `StaleResultBanner.tsx` + versioning policy

### Gaps

- No dial/gauge component — numeric score only (DOMAIN-UX1) — **CONFIRMED**
- Retail polish backlog implicit in multiple FE-R/LC-S audits — **CONFIRMED**
- `insights[]` legacy path still present with visibility filters — **CONFIRMED**

### Reusable source material

- Results Journey Paper v6
- FE-R1 through FE-R6 audit series
- DOMAIN-UX1 audit

### Recommended next action

Fix **HIGH-trust copy coherence** (IUAT issues) before visual polish — evidence in trust-hardening regression tests already started.

---

## Block 6 — Medical safety, research provenance and governance

### Specific answers

| # | Question | Answer | Confidence |
|---|----------|--------|------------|
| 1 | Where is medical research stored? | `knowledge_bus/research/investigation_specs/` (68 files); `multi_llm_research/*_Pass_3.json` | **CONFIRMED** |
| 2 | Research → runtime intelligence? | Packages (`signal_library.yaml`) → SignalRegistry → evaluator; compiled cards; root_cause YAML; promotion protocol | **CONFIRMED** |
| 3 | Source materials preserved? | `source_field_preservation_audit.yaml` in pilots; package `source_document` fields; compile manifests | **PARTIAL** |
| 4 | Claims traceable to research? | Package manifests + `research_brief.sources`; output authority provenance builder | **PARTIAL** |
| 5 | Package promotions governed? | `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md`; batch2 registers; validators | **CONFIRMED** |
| 6 | Rejected/deferred signals tracked? | `batch2_*_execution_register_v1.yaml`; inactive androgen packages in launch gate | **CONFIRMED** |
| 7 | Safety rules enforced by tests? | Architecture guardrails, `test_active_signal_context_gate_reachability.py`, `consumer_prose_safety` regressions | **CONFIRMED** |
| 8 | Lab-provided ranges protected? | ADR/platform non-negotiables; lab range policy docs; evaluator uses lab ranges | **CONFIRMED** (with known historical bugs flagged in PRODUCT_REALITY audit) |
| 9 | Raw Pass 3 not read at runtime? | **Yes** — `intelligence_authority_inventory.md` L10; `day_one_launch_estate_gate_v1.yaml` L18–19 | **CONFIRMED** |

### Confirmed assets

- **186** packages; Pass 3 promotion pilots under `knowledge_bus/generated_pilot/`
- `medical_frame_identity_index_v1.yaml`, `context_modifier_catalogue_draft_v1.yaml`
- `validate_day_one_launch_estate_gate.py`, `run_architecture_validation_gate.py`

### Gaps

- Promotion protocol v1.1 status: **DRAFT FOR GOVERNANCE REVIEW** — **CONFIRMED** L4
- Pass 3 hypotheses not compile-through — **CONFIRMED** PASS3 utilisation audit
- CRP example: Pass 3 specs exist; legacy package still runtime — **CONFIRMED** PASS3 audit §2.3

### Reusable source material

- PASS3 utilisation investigation (cursor)
- KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL v1.1
- `day_one_full_traceability_manifest_v1.yaml`

### Recommended next action

Extend traceability manifest for **each consumer-visible prose line** → compiled artefact → package → Pass 3 spec id.

---

## Block 7 — Auditability, reproducibility and regulatory-grade traceability

### Specific answers

| # | Question | Answer | Confidence |
|---|----------|--------|------------|
| 1 | Result reproducible exactly? | **PARTIAL** — golden runner + deterministic pipeline; timestamps stripped in phenotype tests | **CONFIRMED** |
| 2 | Hashes used? | Package/compile manifests; fingerprint harness — **PARTIAL** | **CONFIRMED** launch-core proving |
| 3 | Runtime packages versioned? | `policy_version` in scoring_policy; package manifests; `result_version` on persisted DTO | **CONFIRMED** |
| 4 | Prompts/prose/compiler versions captured? | `replay_manifest`; narrative digest meta; not full prompt capture for Gemini | **PARTIAL** |
| 5 | User inputs preserved for replay? | Persisted fixtures include biomarkers, questionnaire; LC-S20 contract | **CONFIRMED** |
| 6 | result_versioning working? | **Yes** after INTERNAL-UAT-RESULT-VERSIONING-1 fix — UAT 6bcbf1de compatible=true | **CONFIRMED** |
| 7 | Stale/incompatible protections? | `StaleResultBanner`, `assess_persisted_result_compatibility`, `detect_launch_core_stale_reasons` | **CONFIRMED** |
| 8 | Analysis artefacts immutable? | **PARTIAL** — policy IDs and version checks; regeneration path exists | **CONFIRMED** LAUNCH-CORE-3 |
| 9 | Class II-style auditability? | **NOT FOUND** — would need end-to-end signed manifests, prompt versioning, immutable store, formal hazard analysis | **INFERRED** |

### Confirmed assets

- `backend/core/dto/persisted_replay_contract_v1.py` — `CURRENT_RESULT_VERSION = "1.0.0"`, required keys L17–28
- `backend/core/dto/result_versioning_policy_v1.py`
- `knowledge_bus/governance/day_one_full_traceability_manifest_v1.yaml`
- `output_authority_provenance_builder_v1.py`

### Gaps

- Full compiler version pinning on every persisted result — **PARTIAL**
- Regulatory-grade audit log — **NOT FOUND**

### Reusable source material

- LAUNCH-CORE-3 audit and policy docs
- ARCH-COMPLETION-3 manifest
- LC-S20 persisted replay strategy

### Recommended next action

Expand `replay_manifest` to include **compiler module versions + package manifest hashes** for all governed outputs on each analysis.

---

## Block 8 — Phenotype panels, edge-case estate and beta validation gates

### Specific answers

| # | Question | Answer |
|---|----------|--------|
| 1 | Test panels exist? | **Yes** — AB, VR, golden_panel_160, lab profile variants (`panel_acceptance_profiles_v1.yaml`) |
| 2 | Phenotypes covered? | **≥10** in `phenotype_expectations_v1.yaml` (vascular HCY, renal stress, early IR, thyroid-lipid, iron deficiency/overload, HbA1c stress, hepatic ALT, TSH axis, one-carbon macrocytosis, …) |
| 3 | Active signals with trigger/suppression tests? | DHEA-S, FAI, FT3, free testosterone, pregnancy, supplements/AAS (`test_active_signal_context_gate_reachability.py`, `test_dhea_s_high_activation.py`) |
| 4 | Systems with panel fixtures? | Wave 1 via AB/VR; phenotypes per-domain synthetic fixtures |
| 5 | Lifestyle questionnaire states tested? | Statin context (`test_lc_s2_statin_context_integration.py`); lifestyle coherence (`test_lc_s13_lifestyle_coherence_narrative.py`); pregnancy scenarios |
| 6 | Negative tests for unsafe activation? | Context gate reachability governance tests — **CONFIRMED** |
| 7 | Missing-marker scenarios? | Domain missing lists; clinician data_quality; IUAT tests — **PARTIAL** |
| 8 | Contradictory-marker scenarios? | Collision fixture; historical dual high/low signal bug documented — **PARTIAL** |
| 9 | Beta release checklist? | `BETA-READINESS-RECHECK-1`, `WAVE1-LAUNCH-READINESS-1`, `day_one_launch_estate_gate_v1.yaml` — **CONFIRMED** (distributed, not single checklist) |
| 10 | Missing test estate? | Full 6-domain card matrix; Gemini synthesis validation; retail UAT automation; contradictory-marker regression for all analytes |

### Confirmed assets

- `.github/workflows/golden_gate.yml`
- `backend/tools/run_golden_panel.py`, `launch_core_proving_harness.py`
- `sentinel/` classifier and escaped defects pack
- `backend/tests/fixtures/persisted_results/lc_s20_ab_launch_core_v1.json`

### Gaps

- Beta gate failed on **committed secrets** — **CONFIRMED** BETA-READINESS-RECHECK-1
- Phenotype chain coverage still **pending** for several phenotypes — **CONFIRMED** phenotype_expectations_v1.yaml

### Reusable source material

- panel_acceptance_profiles_v1.yaml
- phenotype_expectations_v1.yaml
- BETA-READINESS sprint papers

### Recommended next action

Consolidate distributed gates into **one beta readiness scorecard** referencing existing validators (do not rewrite gate logic).

---

## Key source documents found

| File path | Title / description | Date/version | Block(s) | Why it matters | Confidence |
|-----------|---------------------|--------------|----------|----------------|------------|
| `docs/architecture/User Health to Systems Map_FINAL.md` | Customer-Facing Health Scores Mapping v0.4 | v0.4 | 1, 2 | 8-domain consumer model + subsystem splitting rules | **HIGH** |
| `docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` | Wave 1 domain narrative contract | 2026-04-26 | 1, 3 | Per-domain copy assembly rules | **HIGH** |
| `docs/intelligence/HealthIQ_Intelligence_Model_Design_Second_Pass.md` | Intelligence model design | — | 1, 6 | Schema/triage authority; not systems taxonomy | **HIGH** |
| `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md` | Layer B→C ADR | WP2 closure | 3, 4 | Binding contract path | **HIGH** |
| `docs/audit-papers/PASS3_research_asset_utilisation_investigation_cursor.md` | Pass 3 utilisation | 2026-05-28 | 3, 6 | Pass 3 vs runtime gap map | **HIGH** |
| `docs/audit-papers/LAYER-B-1_narrative_brief_maturity_report.md` | Layer B brief maturity | 2026-05-31 | 3, 4 | NarrativePayload v1.1 status | **HIGH** |
| `docs/audit-papers/MED-REV-1_wave1_subsystem_visibility_and_label_alignment_report.md` | Subsystem visibility | — | 2 | Hidden vs visible subsystems | **HIGH** |
| `docs/frontend/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md` | Results journey authority | v6 | 5 | UX north star | **HIGH** |
| `knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml` | Launch estate gate | v1.0.0 | 6, 7, 8 | Runtime gate conditions | **HIGH** |
| `docs/audit-papers/BETA-READINESS-RECHECK-1_post_launch_fixes_readiness_gate.md` | Beta readiness recheck | 2026-06-14 | 8 | NOT_READY verdict | **HIGH** |
| `docs/testing/INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_6bcbf1de_2026-06-16.md` | Results page UAT | 2026-06-16 | 5, 8 | Trust/coherence findings | **HIGH** |
| `docs/AUTHORITY_MAP.md` | Document authority index | 2026-05-04 | All | Prevents reading stale docs | **HIGH** |
| `docs/architecture/intelligence_authority_inventory.md` | Authority inventory | 2026-05-28 | 1, 3, 6 | Runtime vs research authority | **HIGH** |
| `docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md` | Pass 3 promotion protocol | v1.1 DRAFT | 6 | Research→package governance | **MEDIUM** |
| `docs/archive/working-papers/STRATEGY_A_IMPLEMENTATION_BLUEPRINT.md` | Strategy A blueprint | 2026-04-26 | 1 | 6-domain repo grounding | **HIGH** |

---

## Key runtime/code assets found

| File path | Function/module | Block(s) | Runtime role | Confidence |
|-----------|-----------------|----------|--------------|------------|
| `backend/core/analytics/domain_score_assembler.py` | `assemble_consumer_domain_scores_v1` | 1, 2 | Wave 1 domain cards + confidence | **HIGH** |
| `backend/core/analytics/wave1_subsystem_evidence.py` | `assemble_wave1_subsystem_evidence` | 2 | Subsystem DTO assembly | **HIGH** |
| `backend/core/knowledge/health_system_card_evidence.py` | Compiled card loader | 2, 3 | Governed subsystem evidence | **HIGH** |
| `backend/core/analytics/report_compiler_v1.py` | `compile_clinician_report_v1` | 3 | Clinician report compiler | **HIGH** |
| `backend/core/analytics/narrative_report_compiler_v1.py` | `compile_narrative_report_v1` | 3 | Deterministic narrative | **HIGH** |
| `backend/core/analytics/narrative_payload_builder_v1.py` | Payload builder | 3, 4 | Layer B brief for Layer C | **HIGH** |
| `backend/core/pipeline/orchestrator.py` | Pipeline phases | 3, 4, 7 | End-to-end analysis | **HIGH** |
| `backend/core/insights/synthesis.py` | `InsightSynthesizer` | 4 | Optional Gemini insights path | **HIGH** |
| `backend/core/llm/validator_v2.py` | `validate_llm_output_v2` | 4, 6 | Anti-hallucination scaffold | **HIGH** |
| `frontend/app/(app)/results/page.tsx` | Results page | 5 | Consumer journey shell | **HIGH** |
| `backend/core/dto/persisted_replay_contract_v1.py` | Compatibility assessment | 7 | Replay/stale contract | **HIGH** |
| `backend/ssot/scoring_policy.yaml` | Scoring policy v1.2.0 | 1 | System scores/rails | **HIGH** |
| `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml` | IDL records | 3, 5 | Pattern/phenotype display | **HIGH** |

---

## Key test assets found

| Test file | Areas covered | Block(s) | What it proves | Gaps |
|-----------|---------------|----------|----------------|------|
| `backend/tests/regression/test_med_rev1_wave1_subsystem_visibility.py` | Subsystem visibility | 2 | MED-REV-1 enforcement | Wave 2+ |
| `backend/tests/regression/test_kb_util1_pass3_card_evidence_compile_and_consume.py` | Pass 3 card compile | 3, 6 | Compile→consume path | Full corpus |
| `backend/tests/regression/test_layer_b1_narrative_brief_maturity.py` | Narrative brief | 3, 4 | Payload v1.1 | LLM wire-up |
| `backend/tests/unit/test_clinician_report_runtime_alignment.py` | AB/VR clinician JSON | 3, 8 | Report contract | All domains |
| `backend/tests/governance/test_active_signal_context_gate_reachability_governance.py` | Context gates | 6, 8 | Reachability policy | All signals |
| `backend/tests/regression/test_active_signal_context_gate_reachability.py` | Pregnancy/DHEA/AAS | 8 | Suppression scenarios | Broader matrix |
| `backend/tests/unit/test_phenotype_suite_v1.py` | Phenotype fixtures | 8 | Signal/chain/root-cause | Pending phenotypes |
| `backend/tests/unit/test_golden_panel_runner.py` | Golden panel + NO-LLM | 4, 7, 8 | Deterministic regression | Live Gemini |
| `backend/tests/regression/test_internal_uat_results_trust_hardening.py` | IUAT copy fixes | 3, 5 | Counter-evidence titles | Full UAT set |
| `.github/workflows/golden_gate.yml` | CI gate | 8 | Merge protection | Beta-specific |

---

## Key research/provenance assets found

| Research file / package | Biomarkers/systems | Promotion state | Runtime-consumed | Source preservation | Gaps |
|-------------------------|-------------------|-----------------|------------------|---------------------|------|
| `multi_llm_research/Batch_2_Pass_3.json` | Androgen panel | Batch 2 promoted (partial) | Via packages only | Manifest `source_document` | Inactive androgen pkgs |
| `multi_llm_research/Batch_4_Pass_3.json` | Lipid/metabolic | Many pkg_kb* | SignalRegistry | research_brief | Hypotheses lost in pkg |
| `pkg_s24_*` / `pkg_kb47_*` | Various | Mixed legacy/kb47 | **Yes** | Partial audits | PSI not in main path |
| `knowledge_bus/compiled/health_system_cards/wave1_*.yaml` | Wave 1 subsystems | KB-UTIL-1 compiled | **Yes** | compile_manifest_ref | 3 domains only |
| `knowledge_bus/root_cause/hypotheses/*.yaml` | ~40 signals | Hand-maintained | **Yes** (6-target compiler historically) | YAML files | Pass 3 compile-through |
| `inv_*.yaml` (31 files) | Single-marker specs | Mixed | **No** (not runtime) | In repo | Promotion queue |

---

## Existing reports we should not reinvent

1. **Systems/subsystems:** `User Health to Systems Map_FINAL.md`, `DOMAIN-UX1_health_systems_card_codebase_reality_audit.md`, `MED-REV-1_*`, `DOMAIN-R1_launch_core_health_domain_readiness_audit.md`
2. **Medical LLM / Pass 3 taxonomy:** `PASS3_research_asset_utilisation_investigation_cursor.md`, `MED-RESEARCH-REVIEW-1_*`, `MED-FRAME-TREE-1_*`, batch2 promotion audit series
3. **Runtime architecture:** `DAY-ONE-ARCHITECTURE-CLOSURE-REVIEW.md`, `ARCH-COMPLETION-2/3_*`, `intelligence_authority_inventory.md`, `PRODUCT_REALITY_AND_DIRECTION_AUDIT.md`
4. **Launch/beta readiness:** `WAVE1-LAUNCH-READINESS-1_*`, `BETA-READINESS-RECHECK-1_*`, `BETA-READINESS-SPRINT-2_*`, `day_one_launch_estate_gate_v1.yaml`
5. **Pass 3 utilisation:** `PASS3_research_asset_utilisation_investigation_cursor.md`, `KB-UTIL-1_*`, promotion protocol v1.1
6. **Layer B/C:** `LAYER-B-1_*`, `wp2_layer_b_layer_c_implementation_readiness_audit.md`, `ADR_WP2_*`, LC-S3 completion note
7. **Auditability/replay:** `LAUNCH-CORE-3_*`, `LC-S20_*`, `INTERNAL-UAT-RESULT-VERSIONING-1_*`
8. **UX/UAT:** `INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_*`, `LAUNCH-CORE-0/1B/2_*`, FE-R0–FE-R6 series, `HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md`

---

## Contradictions or drift

| Area | Documentation | Runtime | Classification |
|------|---------------|---------|----------------|
| Launch domains | 6 launch-core (`User Health Map`) | 3 `consumer_domain_scores` | **CONFIRMED drift** |
| Subsystem depth | 3 CV + 2 MET + 2 LIV subsystems designed | 2 visible scored; 5 hidden | **CONFIRMED intentional** (MED-REV-1) |
| Pass 3 authority | Richest medical source | Not read at runtime | **CONFIRMED by design** |
| Pass 3 on cards | Rich hypotheses in specs | Marker checklists on cards | **CONFIRMED gap** (PASS3 audit) |
| Layer C naming | Gemini personalised synthesis (strategy) | Deterministic compiler + mock LLM | **CONFIRMED drift** |
| Signal/package counts | Older docs: 51–74 packages | 186 packages on disk | **STALE docs** |
| Beta readiness | Architecture validators PASS | BETA-READINESS NOT_READY (secrets) | **CONFIRMED** |
| Scoring vs consumer | 8 SSOT systems | 8 consumer domains planned, 3 cards | **PARTIAL overlap** |
| Frontend vs backend hero | IDL vascular inflammation strong | Hero homocysteine-led (UAT) | **CONFIRMED UX tension** |

---

## Missing assets

| Missing asset | Why it matters | Blocks beta? | Blocks Layer C? | Blocks medical credibility? | Priority |
|---------------|----------------|--------------|-----------------|----------------------------|----------|
| Unified systems authority index (domain→rail→subsystem→spec) | Prevents rebuild | No | No | Yes | P1 |
| Launch domains 4–6 consumer cards (iron, thyroid, kidney) | Strategy A completeness | Yes | Partial | Yes | P1 |
| Per-biomarker boilerplate trigger library | Layer B substrate | Partial | **Yes** | Yes | P1 |
| Pass 3 hypothesis compile-through to packages | Medical depth | Partial | **Yes** | **Yes** | P1 |
| Production Gemini synthesis wire-up | Product vision | No | **Yes** | Partial | P2 (after Layer B) |
| Retail UX trust fixes (UAT HIGH items) | External credibility | **Yes** | No | Yes | P1 |
| Committed-secrets remediation | Security gate | **Yes** | No | Yes | P0 |
| Class II audit trail | Regulatory ambition | No | No | Long-term | P3 |
| Single beta readiness scorecard | Programme clarity | Partial | No | No | P2 |

---

## Recommended multi-sprint programme

### 1. Discovery / recovery sprints

| Title | Objective | Blocks | Key inputs | Expected outputs | Dependencies | Risk |
|-------|-----------|--------|------------|------------------|--------------|------|
| **ESTATE-INDEX-1** | Canonical systems/subsystem/spec index | 1, 2, 6 | User Health Map, compiled cards, manifests | Authority index YAML | None | LOW |
| **SECRETS-REMEDIATION-0** | Remove committed credentials; verify gate | 8 | BETA-READINESS-RECHECK-1 | Clean repo + gate PASS | None | **HIGH** if skipped |

### 2. Architecture alignment sprints

| Title | Objective | Blocks | Key inputs | Expected outputs | Dependencies | Risk |
|-------|-----------|--------|------------|------------------|--------------|------|
| **ARCH-ALIGN-1** | Reconcile 6-domain plan vs 3-card runtime | 1, 2 | STRATEGY_A blueprint, DOMAIN-R1 | Gap closure plan per domain | ESTATE-INDEX-1 | MEDIUM |
| **PASS3-PROMOTE-2** | Hypothesis/contradiction compile pipeline | 3, 6 | Promotion protocol v1.1 | Compile manifests | ARCH-ALIGN-1 | HIGH |

### 3. System/subsystem completion sprints

| Title | Objective | Blocks | Key inputs | Expected outputs | Dependencies | Risk |
|-------|-----------|--------|------------|------------------|--------------|------|
| **DOMAIN-D4-D6** | Iron, thyroid, kidney consumer cards | 1, 2 | Scoring rails, Pass 3 specs | `consumer_domain_scores` ×3 | ARCH-ALIGN-1 | HIGH |
| **SUBSYSTEM-PROMOTE-1** | Promote selected hidden_v1 subsystems | 2 | MED-REV-1 artefacts | Medical review + visibility | DOMAIN cards | MEDIUM |

### 4. Layer B prose/clinician report sprints

| Title | Objective | Blocks | Key inputs | Expected outputs | Dependencies | Risk |
|-------|-----------|--------|------------|------------------|--------------|------|
| **BOILERPLATE-MATRIX-1** | Biomarker/system trigger library | 3 | IDL, pathway explainers, Pass 3 | Compiled boilerplate registry | PASS3-PROMOTE-2 | MEDIUM |
| **LAYERB-BRIEF-2** | Persist full NarrativePayload on DTO | 3, 4 | LAYER-B-1 | DTO field + replay manifest | BOILERPLATE-MATRIX-1 | LOW |

### 5. Gemini Layer C sprints

| Title | Objective | Blocks | Key inputs | Expected outputs | Dependencies | Risk |
|-------|-----------|--------|------------|------------------|--------------|------|
| **LLM-NAR-0** | Constrained synthesis pilot | 4 | NarrativePayload, validator_v2 | Governed prompt + eval harness | LAYERB-BRIEF-2 | **HIGH** |

### 6. UX/result-page sprints

| Title | Objective | Blocks | Key inputs | Expected outputs | Dependencies | Risk |
|-------|-----------|--------|------------|------------------|--------------|------|
| **TRUST-HARDEN-2** | IUAT HIGH copy fixes | 5 | INTERNAL_UAT audit | Regression + UAT PASS | None | LOW |
| **RETAIL-POLISH-1** | Journey v6 alignment | 5 | Results Journey v6 | Visual hierarchy | TRUST-HARDEN-2 | MEDIUM |

### 7. Safety/provenance/auditability sprints

| Title | Objective | Blocks | Key inputs | Expected outputs | Dependencies | Risk |
|-------|-----------|--------|------------|------------------|--------------|------|
| **TRACE-EXPAND-1** | Replay manifest enrichment | 7 | LC-S20, ARCH-COMPLETION-3 | Version hashes on persist | LAYERB-BRIEF-2 | MEDIUM |
| **PROMOTION-PROTO-FINAL** | Ratify Pass 3 protocol v1.1 | 6 | Draft protocol | AUTHORITATIVE protocol | PASS3-PROMOTE-2 | LOW |

### 8. Beta validation/test-estate sprints

| Title | Objective | Blocks | Key inputs | Expected outputs | Dependencies | Risk |
|-------|-----------|--------|------------|------------------|--------------|------|
| **BETA-SCORECARD-1** | Unified readiness scorecard | 8 | Existing gates | Single checklist doc | SECRETS-REMEDIATION-0 | LOW |
| **PHENOTYPE-EXPAND-1** | Complete pending phenotype chains | 8 | phenotype_expectations_v1 | Full chain enforcement | DOMAIN-D4-D6 | MEDIUM |

---

## Top 10 recommendations

1. **P0:** Resolve committed-secrets blocker before any beta environment (`BETA-READINESS-RECHECK-1`).
2. **Do not rebuild** the 8-domain model — extend `User Health to Systems Map_FINAL.md` + manifests.
3. **Do not start Gemini narrative** until `NarrativePayloadV1` is persisted and boilerplate matrix exists (`LAYER-B-1` deferrals).
4. Build **ESTATE-INDEX-1** linking consumer domains → subsystems → Pass 3 specs before new domain implementation.
5. Implement **launch domains 4–6** (iron, thyroid, kidney) using existing scoring rails — highest functional beta gap.
6. Execute **PASS3 hypothesis compile-through** per promotion protocol — highest medical credibility gap.
7. Fix **IUAT HIGH-trust copy issues** before retail polish (B12 heading, marker-count semantics, markdown leakage).
8. Promote **hidden_v1 subsystems** only via medical review — artefacts already exist (MED-REV-1).
9. Expand **replay_manifest** with compiler/package versions for reproducibility.
10. Consolidate **beta gates** into one scorecard referencing existing validators — avoid rewriting gate logic.

---

## Appendix A — Search log

### Search terms and notable hits

| Term | Notable files |
|------|---------------|
| `clinician_report_v1` | `report_compiler_v1.py`, `builders.py`, `persisted_replay_contract_v1.py` |
| `narrative_report_v1` | `narrative_report_compiler_v1.py`, `orchestrator.py` |
| `interpretation_display_layer_v1` | `interpretation_display_layer_publish_v1.py`, `idl_records_v1.yaml` |
| `consumer_domain_scores` | `domain_score_assembler.py`, `results.py`, `Wave1DomainCards.tsx` |
| `Wave 1` / `wave1_` | `wave1_subsystem_evidence.py`, compiled cards, MED-REV-1 |
| `Pass 3` | `investigation_specs/multi_llm_research/`, PASS3 utilisation audit |
| `Gemini` / `Layer C` | `synthesis.py`, `narrative_runtime_policy.py`, ADR_WP2 |
| `replay_manifest` | `persisted_replay_contract_v1.py`, LC-S20 fixtures |
| `beta readiness` | `BETA-READINESS-RECHECK-1`, `day_one_launch_estate_gate_v1.yaml` |
| `active_signal_context_gate` | `test_active_signal_context_gate_reachability.py`, validate script |
| `medical LLM` | No standalone report; Pass 3 multi_llm_research + User Health Map |
| `boilerplate` / `explainer` | `pathway_explainers_v1.yaml`, `retail_explainer_v1`, compiled cards |
| `phenotype` | `phenotype_expectations_v1.yaml`, `test_phenotype_suite_v1.py` |
| `UAT` | `INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_6bcbf1de_2026-06-16.md` |

### Repository scale (audit-time counts)

- `pkg_*` packages: **186**
- `investigation_specs` files: **68**
- `backend/tests/test_*.py`: **282**

---

## Appendix B — Evidence index

All file paths referenced in this audit:

```
docs/AUTHORITY_MAP.md
docs/architecture/User Health to Systems Map_FINAL.md
docs/architecture/intelligence_authority_inventory.md
docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md
docs/architecture/RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md
docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md
docs/intelligence/HealthIQ_Intelligence_Model_Design_Second_Pass.md
docs/intelligence/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md
docs/frontend/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md
docs/frontend/CLAUDE_TRANSLATION_SPEC_v1.md
docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
docs/audit-papers/PASS3_research_asset_utilisation_investigation_cursor.md
docs/audit-papers/LAYER-B-1_narrative_brief_maturity_report.md
docs/audit-papers/MED-REV-1_wave1_subsystem_visibility_and_label_alignment_report.md
docs/audit-papers/DOMAIN-UX1_health_systems_card_codebase_reality_audit.md
docs/audit-papers/wp2_layer_b_layer_c_implementation_readiness_audit.md
docs/audit-papers/BETA-READINESS-RECHECK-1_post_launch_fixes_readiness_gate.md
docs/testing/INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_6bcbf1de_2026-06-16.md
docs/archive/working-papers/STRATEGY_A_IMPLEMENTATION_BLUEPRINT.md
architecture/ADR-007-clinician-summary-report.md
backend/ssot/scoring_policy.yaml
backend/core/analytics/domain_score_assembler.py
backend/core/analytics/domain_narrative_wave1.py
backend/core/analytics/wave1_subsystem_evidence.py
backend/core/knowledge/health_system_card_evidence.py
backend/core/analytics/report_compiler_v1.py
backend/core/analytics/narrative_report_compiler_v1.py
backend/core/analytics/narrative_payload_builder_v1.py
backend/core/analytics/narrative_brief_enforcement_v1.py
backend/core/analytics/narrative_compiler_lc_s3_assembly_v1.py
backend/core/analytics/interpretation_display_layer_publish_v1.py
backend/core/analytics/consumer_prose_safety_v1.py
backend/core/analytics/lifestyle_consumer_surface_v1.py
backend/core/analytics/output_authority_provenance_builder_v1.py
backend/core/pipeline/orchestrator.py
backend/core/dto/builders.py
backend/core/dto/persisted_replay_contract_v1.py
backend/core/dto/result_versioning_policy_v1.py
backend/core/contracts/narrative_payload_v1.py
backend/core/insights/synthesis.py
backend/core/insights/narrative_runtime_policy.py
backend/core/llm/validator_v2.py
backend/app/routes/upload.py
frontend/app/(app)/results/page.tsx
frontend/app/components/results/Wave1DomainCards.tsx
frontend/app/components/results/LayerCInsightSection.tsx
frontend/app/lib/resultsPageLayout.ts
knowledge_bus/compiled/health_system_cards/wave1_met_glycaemic_control.yaml
knowledge_bus/compiled/health_system_cards/wave1_cv_lipid_transport.yaml
knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml
knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml
knowledge_bus/governance/day_one_full_traceability_manifest_v1.yaml
knowledge_bus/research/investigation_specs/multi_llm_research/
backend/tests/fixtures/panels/panel_acceptance_profiles_v1.yaml
backend/tests/fixtures/panels/phenotypes/phenotype_expectations_v1.yaml
backend/tests/regression/test_med_rev1_wave1_subsystem_visibility.py
backend/tests/regression/test_active_signal_context_gate_reachability.py
backend/tests/governance/test_active_signal_context_gate_reachability_governance.py
backend/tests/unit/test_phenotype_suite_v1.py
backend/tests/unit/test_golden_panel_runner.py
.github/workflows/golden_gate.yml
EIGHT_BLOCK_BETA_READINESS_ESTATE_AUDIT_CURSOR_2026-06-17.md
```

---

*End of audit — Cursor independent evidence discovery, 2026-06-17.*
