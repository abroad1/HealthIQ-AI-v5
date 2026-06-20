# P1-1 — Launch-Core Domain Build-Materials Map

**Work ID:** P1-1  
**Date:** 2026-06-20  
**Sprint type:** Discovery and mapping only (no runtime changes)

---

## 1. Executive summary

This sprint mapped build materials for the three missing launch-core consumer domains identified in the definitive beta-readiness strategy: **blood / iron / oxygen**, **thyroid / energy regulation**, and **kidney function**.

**Readiness judgement (implementation-ready for a domain-card sprint, not for full beta completion):**

| Domain | Implementation-ready? | Overall readiness |
|---|---|---|
| Blood / iron / oxygen | Partial — richest package estate, but no compiled card, no domain assembler wiring, heavy signal adjudication backlog | Partial |
| Thyroid / energy regulation | Partial — kb47 hormone signals runtime-active with gates, but no domain card, register drift on FT3 low, kb52c/kb59 not loaded | Partial |
| Kidney function | Partial — smallest bounded scope, clearest active signal subset and collision tests, but no compiled card or domain wiring | Partial |

**Safest first implementation domain for P1-2:** **Kidney function.**

Rationale: bounded biomarker scope (creatinine, eGFR, urea); canonical runtime-active signals for eGFR and kb52c creatinine with tested `renal_filtration_axis` collision enforcement (`knowledge_bus/governance/signal_authority_collision_model_v1.yaml`, `backend/tests/regression/test_signal_authority_collision_enforcement.py`); existing kidney scoring rail in `backend/ssot/scoring_policy.yaml`; lower context-gate complexity than thyroid FT3 low; smaller adjudication surface than full blood/iron/CBC.

**Main blockers / carry-forwards:** All three domains lack compiled Wave 1 health-system cards, `wave1_subsystem_evidence.py` registration, and `domain_score_assembler.py` consumer-domain rows. Layer B prose is thin across all three (partial retail explainers; no dedicated pathway explainers). Signal promotion and medical-review dependencies remain open for many packages.

**Evidence gaps / ambiguity:** Register drift for FT3 low across governance files; urea signals not indexed in `medical_frame_identity_index_v1.yaml`; TIBC/UIBC absent from SSOT and packages; exact legacy s24 creatinine frame activation mix; whether albuminuric kidney damage should remain UACR-override-only or receive a dedicated package.

**Knowledge Bus package count:** Command `(Get-ChildItem knowledge_bus/packages -Directory).Count` → **187 packages**. Matches the strategy's 186–187 upper bound; no discrepancy requiring programme escalation.

---

## 2. Scope and non-goals

This sprint mapped build materials only.

Confirmed explicitly:

- no runtime code changed;
- no tests changed;
- no frontend changed;
- no parser/scoring/report/Gemini logic changed;
- no signals activated;
- no Knowledge Bus packages promoted;
- no Pass 3 material promoted;
- no reference ranges altered;
- no Layer C presentation logic changed;
- no new clinical interpretation logic created;
- no assets inferred from memory.

---

## 3. Authority documents used

| Document | Path | How it informed the map |
|---|---|---|
| Final definitive strategy baseline | `docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md` | Defines three missing launch-core domains, P1 sequencing, Layer A/B/C model, package-count verification task, and prohibition on implementation before mapping |
| Layer Boundary Reconciliation ADR | `docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md` | Confirms domain interpretation belongs to Layer B; mapping stays off Layer C medical reasoning |
| Eight-block programme recommendation | `docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_COMPARISON_AND_PROGRAMME_RECOMMENDATION_2026-06-18.md` | Confirms Block 1 gap: three of six launch-core domains missing |
| Layer authority index (r2 only) | `docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md` | Used for layer vocabulary; r1 not used per sprint instruction |
| User Health to Systems Map | `docs/architecture/User Health to Systems Map_FINAL.md` | Confirms consumer-facing health-system framing for launch-core domains |
| Document authority map | `docs/AUTHORITY_MAP.md` | Confirms strategy baseline registration; not modified in this sprint |
| Build deliverable register | `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md` | Prior sprint carry-forward requiring P1-1; updated at closure |
| Scoring policy | `backend/ssot/scoring_policy.yaml` | Shows partial system coverage: `cbc` (Hgb/Hct only), `kidney` (creatinine/urea), empty `hormonal` and `nutritional` systems |
| Wave 1 subsystem evidence | `backend/core/analytics/wave1_subsystem_evidence.py` | Confirms only CV, blood sugar, liver registered — missing domains return `[]` |
| Domain score assembler | `backend/core/analytics/domain_score_assembler.py` | Confirms three Wave 1 consumer rows only; no missing-domain assembly |
| Retail explainer registry | `backend/ssot/retail_explainer_v1/registry.yaml` | Partial Layer B prose coverage per domain |
| Pathway explainers | `knowledge_bus/pathway_explainers_v1/pathway_explainers_v1.yaml` | No dedicated pathways for any missing domain |
| Compiled estate index | `knowledge_bus/compiled/estate_index_v1.yaml` | Seven Wave 1 subsystems — none renal, thyroid, or blood/iron/oxygen |
| Metabolic pathway coverage audit | `docs/intelligence/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md` | Thyroid-driven metabolic disturbance marked PARTIAL |

---

## 4. Domain readiness summary table

| Domain | Current implementation status | Package/spec evidence | Biomarker coverage clarity | Signal safety clarity | Subsystem readiness | Prose/explainer readiness | Test readiness | Overall readiness | Recommended sequencing |
|---|---|---|---|---|---|---|---|---|---|
| Blood / iron / oxygen | Missing launch-core domain card and assembler wiring; legacy insight/scoring fragments only | **Strong** — 30+ KB packages (kb52c, kb58, kb61, s24, context packages); Pass 3 investigation specs; root-cause hypotheses | **Strong** for core CBC/iron markers in `backend/ssot/biomarkers.yaml`; **Weak** for TIBC/UIBC (absent) | **Partial** — ferritin frames adjudicated in `knowledge_bus/governance/medical_frame_identity_index_v1.yaml`; many families `blocked_pending_frame_adjudication` in `pass3_frame_coverage_audit_v1.yaml` | **Weak** — no compiled card; `wave1_subsystem_evidence.py` returns empty for `blood_iron_oxygen` | **Partial** — Hgb/ferritin + hematological system in retail registry; no dedicated pathway explainer | **Strong** — extensive `test_signal_evaluator.py`, phenotype fixtures, launch-core panel fixture | **Partial** | 2nd or 3rd — rich assets but highest breadth and adjudication load |
| Thyroid / energy regulation | Missing domain card; kb47 hormone signals runtime-active; kb52c TSH and kb59 antibodies not loaded | **Partial** — 13 thyroid packages; investigation specs and medical reviews present | **Strong** in `biomarkers.yaml` (TSH, FT3, FT4, TPO-Ab, TgAb) | **Weak** — FT3 low multi-gate + register drift; TSH mandatory gating on FT3/FT4; kb52c/kb59 inactive | **Weak** — no compiled card or Wave 1 subsystem IDs | **Partial** — TSH + thyroid system overview only; no FT3/FT4/antibody retail entries | **Strong** for kb47 gates (`test_batch2_thyroid_tsh_gating.py`, `test_runtime_context_evaluation.py`); none for kb59/kb52c | **Partial** | 3rd — highest clinical gating and governance drift risk |
| Kidney function | Missing domain card; eGFR + kb52c creatinine runtime-active; legacy s24 creatinine mixed; kidney scoring partial | **Partial** — 8 primary packages + pilots; no standalone ACR/UACR package | **Strong** for creatinine, eGFR, urea, uacr in `biomarkers.yaml`; ACR has SSOT only, no signal package | **Partial** — collision model tested; legacy s24 potassium frame inactive; urea not in frame index | **Weak** — no compiled card; `detox_filtration` insight module exists but not launch-core domain row | **Partial** — creatinine, eGFR, renal system retail entries; no urea/uacr retail keys | **Partial** — collision + scoring + phenotype tests; no domain-card assembly tests | **Partial** | **1st (P1-2)** — smallest bounded scope, clearest active signal subset |

Ratings used: **Strong**, **Partial**, **Weak**, **Unknown** — applied conservatively; no domain rated Strong overall because all lack compiled cards and domain assembler wiring.

---

## 5. Blood / iron / oxygen build-materials map

### 5.1 Existing packages and research material

**Knowledge Bus packages (representative; 30+ total in estate):**

| Asset type | Examples | Source path |
|---|---|---|
| CBC / anaemia | `pkg_kb52c_hgb_low_normocytic_underproduction_context`, `pkg_kb52c_hematocrit_low_anemia_or_hemodilution`, `pkg_s24_hgb_low_anemia` | `knowledge_bus/packages/` |
| RBC indices | `pkg_kb58_rbc_low_iron_restricted_anemia_pattern`, `pkg_kb58_mch_low_iron_restricted_erythropoiesis`, `pkg_kb58_mchc_low_hypochromic_iron_restriction`, RDW packages | `knowledge_bus/packages/` |
| Iron stores / transport | `pkg_kb52c_ferritin_low_iron_store_depletion`, `pkg_s24_ferritin_low_iron_deficiency`, `pkg_kb61_transferrin_high_iron_deficiency_transport_upregulation`, `pkg_iron_deficiency_context`, `pkg_iron_overload_context` | `knowledge_bus/packages/` |
| B12 / folate (relevant to macrocytosis) | `pkg_kb52c_vitamin_b12_low_b12_deficiency_context`, `pkg_kb45_active_b12_low_deficiency`, `pkg_kb52c_folate_low_folate_deficiency`, s24 variants | `knowledge_bus/packages/` |
| Pass 3 / investigation specs | TIBC references in batch specs | `knowledge_bus/research/investigation_specs/investigation_spec_contract_version_20_gold_final.yaml` (`inv_tibc_high`) |
| CBC tranche blocker | Research note | `knowledge_bus/research/KB-S57_CBC_TRANCHE_BLOCKER_REPORT.md` |
| Compiled card evidence | **None** for blood/iron/oxygen | `knowledge_bus/compiled/estate_index_v1.yaml` — seven Wave 1 cards, all CV/met/liver |
| Pathway explainers | Partial via homocysteine pathway only | `knowledge_bus/pathway_explainers_v1/pathway_explainers_v1.yaml` (`one_carbon_methylation_homocysteine_v1`) |
| Root-cause hypotheses | Ferritin, Hgb, iron, transferrin, MCV, oxygen transport | `knowledge_bus/root_cause/hypotheses/` (e.g. `oxygen_transport_capacity_hypotheses_v1.yaml`) |

**Gap:** No packages for TIBC, UIBC, or standalone oxygen biomarker.

### 5.2 Biomarker scope

| Biomarker | In `backend/ssot/biomarkers.yaml` | KB packages found | Notes |
|---|---|---|---|
| haemoglobin / hemoglobin | Yes (~733) | Yes (`pkg_kb52c_hgb_*`, `pkg_s24_hgb_*`) | Aliases hgb, hb |
| hematocrit | Yes (~749) | Yes (`pkg_kb52c_hematocrit_*`) | |
| rbc | Yes (~917) | Yes (kb58 RBC packages) | |
| mcv | Yes (~936) | Yes | Macrocytosis + iron patterns |
| mch / mchc | Yes (~958, ~975) | Yes (kb58) | |
| rdw_cv / rdw_sd | Yes (~992, ~1012) | Yes (kb58) | |
| ferritin | Yes (~586) | Yes | System tagged `immune` in SSOT |
| iron | Yes (~1824) | Context packages | |
| transferrin | Yes (~1844) | Yes (kb61) | |
| transferrin_saturation | Yes (~1865) | Unknown dedicated package | SSOT only |
| tibc / uibc | **No** | **No** | Spec references only |
| vitamin_b12 / active_b12 / folate | Yes | Yes | Relevant to MCV/macrocytosis |
| oxygen (biomarker) | **No** | **No** | Hypothesis asset only: `oxygen_transport_capacity_hypotheses_v1.yaml` |

Lab-range dependency: domain markers expect lab-provided reference ranges per biomarker SSOT; scoring bands exist only for Hgb/Hct in `scoring_policy.yaml`.

### 5.3 Signal and interpretation status

Governance split across:

- `knowledge_bus/governance/medical_frame_identity_index_v1.yaml` — ferritin frames: legacy s24 low partially **active** with `blocked_pending_medical_review`; Pass 3 ferritin frames `none` / `required_before_activation`
- `knowledge_bus/governance/pass3_frame_coverage_audit_v1.yaml` — families including `signal_iron_deficiency_context`, `signal_hemoglobin_low`, `signal_mcv_high`: mostly `blocked_pending_frame_adjudication`; `signal_ferritin_low`, `signal_folate_low`, `signal_vitamin_b12_low`: `safe_after_documented_divergence_acceptance`

| Signal family | Authority status (pass3 audit) | Safety note |
|---|---|---|
| `signal_ferritin_high` / `signal_ferritin_low` | runtime_loaded; mixed promotion safety | Medical review required for several frames |
| `signal_iron_deficiency_context` / `signal_iron_overload_context` | runtime_loaded; blocked_pending_frame_adjudication | Do not activate without adjudication |
| `signal_hemoglobin_low` / `signal_mcv_high` | blocked_pending_frame_adjudication | |
| Transferrin, hematocrit, RDW, RBC families | Not in pass3 audit excerpt | Status **Unknown** without per-package review |

Medical review appears required before broad runtime use of anaemia/iron interpretation frames.

### 5.4 Subsystem candidates

From existing assets only (no invented names):

| Candidate grouping | Supporting evidence | Readiness |
|---|---|---|
| Oxygen carrying capacity | Hgb/Hct packages, `oxygen_transport_capacity_hypotheses_v1.yaml` | Partial — no compiled subsystem |
| Iron storage | Ferritin packages | Partial |
| Iron transport | kb61 transferrin packages | Partial |
| Red-cell indices | kb58 MCH/MCHC/RDW/RBC packages | Partial |
| One-carbon / erythropoiesis link | Homocysteine pathway explainer references B12/folate/MCV | Partial — cross-domain only |

`backend/core/analytics/wave1_subsystem_evidence.py` — **no** `wave1_blood_iron_oxygen` domain. Test sentinel: `backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py` expects empty list for `domain_id="blood_iron_oxygen"`.

### 5.5 Prose, explainer and clinician-report assets

| Asset type | Present | Path |
|---|---|---|
| Retail biomarker explainers | Hgb, ferritin only | `backend/ssot/retail_explainer_v1/registry.yaml` |
| Retail system overview | `hematological` | Same |
| Pathway explainer | Indirect (B12/folate/MCV via homocysteine) | `knowledge_bus/pathway_explainers_v1/pathway_explainers_v1.yaml` |
| Narrative payload | Generic non-diagnostic pattern language | `backend/core/contracts/narrative_payload_v1.py` |
| Clinician report sections | No dedicated blood/iron domain section mapped | **Gap** |

Missing retail keys: hematocrit, rbc, mcv, mch, mchc, rdw, iron, transferrin, B12, folate.

### 5.6 Tests and fixtures

| Category | Path | Coverage |
|---|---|---|
| Signal evaluator | `backend/tests/unit/test_signal_evaluator.py` | Iron, ferritin, B12, folate, MCV, transferrin fixtures |
| Phenotype panels | `backend/tests/fixtures/panels/phenotypes/ph_iron_deficiency_inflammation_v1.json`, `ph_iron_overload_v1.json`, `ph_one_carbon_homocysteine_macrocytosis_v1.json` | Iron and macrocytosis |
| Launch-core fixture | `backend/tests/fixtures/persisted_results/lc_s20_ab_launch_core_v1.json` | Broad blood/iron panel |
| Scoring | `backend/tests/unit/test_scoring_rules.py` | Hgb/Hct CBC system only |
| Domain subsystem evidence | `backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py` | Confirms gap for `blood_iron_oxygen` |
| Pass 3 pilot | `backend/tests/regression/test_kb_util2_pass3_pilot_compiler.py` | Ferritin pilot |

**Gap:** No domain-card assembly test for blood/iron/oxygen.

### 5.7 Gaps and carry-forwards

- No compiled Wave 1 health-system card or manifest for blood/iron/oxygen
- No `wave1_subsystem_evidence.py` / `domain_score_assembler.py` domain registration
- TIBC/UIBC absent from SSOT and packages
- Scoring policy covers Hgb/Hct only under `cbc`; `nutritional` system empty
- Many signals blocked pending frame adjudication or medical review
- Partial retail explainers; no dedicated pathway explainer
- Ferritin SSOT system classification (`immune`) may need reconciliation for domain assembly
- CBC tranche blocker report indicates unresolved batch governance

### 5.8 Implementation-readiness judgement

**Candidate for P1-2:** Yes, but **not recommended first**.

Richest asset base and strongest test fixtures, but highest breadth (CBC + iron + B12/folate), heaviest signal adjudication backlog, and TIBC/UIBC gaps make it a higher-risk first domain implementation than kidney function.

---

## 6. Thyroid / energy regulation build-materials map

### 6.1 Existing packages and research material

| Marker / pattern | Packages | Source path |
|---|---|---|
| TSH (kb52c Pass 3) | `pkg_kb52c_tsh_high_primary_hypothyroid_pattern`, `pkg_kb52c_tsh_low_thyrotoxic_pattern` | `knowledge_bus/packages/` — **not runtime-loaded** per `knowledge_bus/governance/package_estate_KB-S49_v1.yaml` |
| TSH (legacy s24) | `pkg_s24_tsh_high_hypothyroidism`, `pkg_s24_tsh_low_hyperthyroidism` | Runtime-loaded, not launch-visible — `non_pass3_package_revalidation_register_v1.yaml` |
| TSH context anchor | `pkg_thyroid_tsh_context` | Internal-only, architecture-doc blocked |
| Free T3 | `pkg_kb47_free_t3_low_low_t3_syndrome`, `pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis` | **runtime_active_canonical** with gates |
| Free T4 | `pkg_kb47_free_t4_low_thyroid_hormone_deficiency`, `pkg_kb47_free_t4_high_thyrotoxicosis_context` | **runtime_active_canonical** with TSH gates |
| TPO-Ab / TgAb | kb59 packages (4) | **Inactive** — not runtime-loaded |
| Investigation specs | `inv_tsh_high_hypothyroidism_v1.yaml`, Batch 2/4 Pass 3 JSON | `knowledge_bus/research/investigation_specs/` |
| Medical reviews | `batch2_thyroid_androgen_context_authority_review_v1.md`, clinical sign-off doc | `knowledge_bus/research/medical_reviews/`, `docs/Medical Research Documents/` |
| Phenotypes | `ph_thyroid_lipid_disturbance_v1`, `ph_tsh_axis_metabolic_v1` | `knowledge_bus/phenotypes/phenotype_map_v1.yaml` |
| Compiled cards | **None** | `knowledge_bus/compiled/` |
| Pathway explainers | **None** for thyroid | `pathway_explainers_v1.yaml` |

### 6.2 Biomarker scope

| Biomarker | SSOT (`biomarkers.yaml`) | Packages | Notes |
|---|---|---|---|
| tsh | Yes (~713) | kb52c, s24, context | Clinical weight 0.8 |
| free_t3 | Yes (~1158) | kb47 | Illness/fasting/medication modifiers |
| free_t4 | Yes (~678) | kb47 | TSH-present gate |
| tpo_ab | Yes (~1177) | kb59 | Not runtime-loaded |
| tgab | Yes (~698) | kb59 | Not runtime-loaded |

### 6.3 Signal and interpretation status

| Signal | Status | Gate / safety | Source |
|---|---|---|---|
| `signal_free_t3_high` | runtime_active_canonical | TSH suppressed mandatory | `batch2_thyroid_gate_execution_register_v1.yaml`, `signal_evaluator.py` |
| `signal_free_t4_high` | runtime_active_canonical | TSH suppressed | Same |
| `signal_free_t4_low` | runtime_active_canonical | TSH present | Same |
| `signal_free_t3_low` | runtime_active_canonical (with register conflict) | TSH + FT4 + illness/medication/calorie/fasting gates; fail-closed | `pkg_kb47_free_t3_low_low_t3_syndrome/signal_library.yaml`, `active_signal_context_gate_reachability_policy_v1.yaml` |
| kb52c TSH patterns | inactive / not loaded | Requires review | `package_estate_KB-S49_v1.yaml` |
| kb59 antibodies | inactive | Medical review before activation | Same |
| Legacy s24 TSH | runtime_loaded, not launch-visible | Pass 3 revalidation required | `non_pass3_package_revalidation_register_v1.yaml` |

**Register drift (ambiguous):** FT3 low marked deferred in `batch2_thyroid_gate_execution_register_v1.yaml`, activated in `batch2_full_coverage_activation_execution_register_v1.yaml`, still inactive in `batch2_context_clearance_register_v1.yaml`. Must be reconciled before domain implementation.

**Root-cause gap:** `root_cause_authority_register_v1.yaml` — `ROOT_CAUSE_REQUIRES_FUTURE_MAPPING` for `signal_free_t3_low`.

**Do not casually recommend activating context-dependent thyroid signals** — clinical sign-off and multi-layer gates documented in medical review assets.

### 6.4 Subsystem candidates

| Candidate | Evidence | Readiness |
|---|---|---|
| TSH-axis metabolic pattern | `ph_tsh_axis_metabolic_v1` phenotype | Partial — test/harness only |
| Thyroid–lipid disturbance | `ph_thyroid_lipid_disturbance_v1`, interaction map edges | Partial — cross-domain |
| Hormone deficiency / thyrotoxicosis (kb47) | Active kb47 packages | Partial — signals without domain card |

No Wave 1 thyroid subsystem IDs in `wave1_subsystem_evidence.py`.

### 6.5 Prose, explainer and clinician-report assets

| Asset | Status | Path |
|---|---|---|
| Retail TSH explainer | Present | `backend/ssot/retail_explainer_v1/registry.yaml` |
| Retail thyroid system overview | Present | Same |
| FT3, FT4, TPO-Ab, TgAb retail | **Absent** | |
| Pathway explainer | **Absent** | |
| IDL display records | Phenotype labels only | `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml` |

### 6.6 Tests and fixtures

| Test | Path |
|---|---|
| TSH pre-emission gating | `backend/tests/regression/test_batch2_thyroid_tsh_gating.py` |
| FT3 low context gates | `backend/tests/regression/test_runtime_context_evaluation.py` |
| Context reachability | `backend/tests/regression/test_active_signal_context_gate_reachability.py` |
| Full-coverage activation | `backend/tests/regression/test_batch2_full_coverage_activation.py` |
| Governance registers | `backend/tests/governance/test_batch2_context_clearance_register.py`, `test_batch2_minimum_coverage_decision_register.py` |
| Phenotype fixtures | `ph_thyroid_lipid_disturbance_v1.json`, `ph_tsh_axis_metabolic_v1.json` |
| Golden panel | `backend/tests/fixtures/golden_panel_sprint14_2_thyroid_immune_mini.json` |

**Gap:** No tests for kb59 or kb52c TSH packages (not runtime-loaded).

### 6.7 Gaps and carry-forwards

- No compiled domain card or Wave 1 subsystem wiring
- Register drift on FT3 low must be reconciled
- kb52c TSH and kb59 antibodies exist but not runtime-loaded
- Root-cause blocked for activated thyroid signals
- `hormonal` scoring system empty (`system_weight: 0.0`)
- Thin retail prose; no pathway explainer
- Legacy s24 TSH packages loaded but not launch-visible

### 6.8 Implementation-readiness judgement

**Candidate for P1-2:** Yes, but **not recommended first**.

Highest clinical gating complexity and governance register conflicts. Strong regression tests exist for kb47 gates, but domain-card implementation would surface unresolved adjudication and root-cause gaps immediately.

---

## 7. Kidney function build-materials map

### 7.1 Existing packages and research material

| Package | Signal | Source path |
|---|---|---|
| `pkg_kb52c_creatinine_high_reduced_glomerular_filtration` | `signal_creatinine_high` | `knowledge_bus/packages/` |
| `pkg_kb52c_creatinine_low_low_muscle_mass_or_low_generation` | `signal_creatinine_low` | Same |
| `pkg_kb47_egfr_low_chronic_kidney_function_reduction` | `signal_egfr_low` | Same |
| `pkg_kb47_egfr_low_hemodynamic_filtration_drop` | `signal_egfr_low` | Same |
| `pkg_kb52c_urea_high_prerenal_volume_depletion_or_catabolic_load` | `signal_urea_high` | Same |
| `pkg_kb52c_urea_low_low_protein_or_reduced_urea_cycle_input` | `signal_urea_low` | Same |
| `pkg_s24_creatinine_high_renal` | `signal_creatinine_high` (legacy) | Same |
| `pkg_s24_urea_high_renal` | `signal_urea_high` (legacy) | Same |

Investigation specs: `inv_creatinine_high_renal_v1.yaml`, `inv_urea_high_renal.yaml` — `knowledge_bus/research/investigation_specs/`

Phenotype: `ph_renal_stress_v1` — `knowledge_bus/phenotypes/phenotype_map_v1.yaml`

**ACR/UACR:** SSOT biomarker `uacr` exists; corroborator overrides in creatinine/eGFR signal libraries; **no standalone KB package** — `creatinine_multiframe_authority_decision_v1.yaml` notes albuminuric frame `not_indexed_partially_covered_by_kb52c_uacr_override`.

Compiled cards: **None** — `knowledge_bus/compiled/estate_index_v1.yaml`

### 7.2 Biomarker scope

| Biomarker | SSOT | Packages | Scoring policy |
|---|---|---|---|
| creatinine | Yes | kb52c + s24 | `kidney` system band |
| egfr | Yes | kb47 (2) | **Not** in kidney system biomarkers list |
| urea | Yes | kb52c + s24 | `kidney` system band |
| uacr / acr | Yes (aliases) | Override only in signal libraries | **Not** in scoring |
| cystatin_c, urate, urine ratios | Yes in SSOT | Limited package mapping | Partial |

Lab-range dependency: creatinine scoring uses age/sex adjustment in `backend/core/scoring/rules.py`; eGFR typically lab-calculated — implementation must use lab-provided values, not substitute global defaults.

### 7.3 Signal and interpretation status

| Signal | Status | Source |
|---|---|---|
| `signal_egfr_low` | **active** — both kb47 packages `runtime_active_canonical` | `authority_runtime_execution_register_v1.yaml`, `medical_frame_identity_index_v1.yaml` |
| `signal_creatinine_high` (kb52c) | **active** — `runtime_active_canonical` | `medical_frame_identity_index_v1.yaml` |
| `signal_creatinine_high` (s24 eGFR frame) | **active** — legacy unadjudicated | Same — `blocked_pending_medical_review` |
| `signal_creatinine_high` (s24 potassium frame) | **inactive** | Same |
| `signal_creatinine_low` | kb52c package — lower bound enabled | `signal_library.yaml` |
| `signal_urea_high` / `signal_urea_low` | runtime_loaded (s24/kb52c) — **not in frame index** | `pass3_frame_coverage_audit_v1.yaml` (s24 urea only) |
| UACR signal | **None** | |

Collision enforcement: `renal_filtration_axis` — primary `signal_egfr_low`, supporting `signal_creatinine_high` — `signal_authority_collision_model_v1.yaml`, tested in `test_signal_authority_collision_enforcement.py`.

Non-diagnostic constraint: retail and hypothesis assets include explicit non-diagnosis language; do not introduce diagnostic CKD staging language.

### 7.4 Subsystem candidates

| Candidate | Evidence | Readiness |
|---|---|---|
| Glomerular filtration | eGFR + creatinine packages, collision model | Partial |
| Prerenal / catabolic urea pattern | kb52c urea high | Partial |
| Renal stress phenotype | `ph_renal_stress_v1` | Partial |
| Detox/filtration insight module | `backend/core/insights/modules/detox_filtration.py` | Partial — not launch-core domain row |

No Wave 1 kidney subsystem in `wave1_subsystem_evidence.py`.

### 7.5 Prose, explainer and clinician-report assets

| Asset | Status | Path |
|---|---|---|
| creatinine retail explainer | Present | `backend/ssot/retail_explainer_v1/registry.yaml` |
| egfr retail explainer | Present | Same |
| renal system overview | Present | Same |
| urea, uacr retail | **Absent** | |
| Pathway explainer | **Absent** | |
| IDL renal pattern | `ph_renal_stress_v1` — "Kidney Stress Pattern" | `idl_records_v1.yaml` |

### 7.6 Tests and fixtures

| Test / fixture | Path |
|---|---|
| Renal collision enforcement | `backend/tests/regression/test_signal_authority_collision_enforcement.py` |
| Creatinine multiframe index | `backend/tests/regression/test_med_frame_identity_index.py` |
| Signal evaluator (s24 renal) | `backend/tests/unit/test_signal_evaluator.py` |
| Kidney scoring | `backend/tests/unit/test_scoring_rules.py`, `test_scoring_engine.py` |
| Root cause renal | `backend/tests/unit/test_root_cause_v1_homocysteine.py` (KB-S56b creatinine/urea) |
| Phenotype | `backend/tests/fixtures/panels/phenotypes/ph_renal_stress_v1.json` |
| Launch-core fixture | `lc_s20_ab_launch_core_v1.json` (kidney score, renal explainers) |

**Gap:** No domain-card assembly test for kidney launch-core domain.

### 7.7 Gaps and carry-forwards

- No compiled Wave 1 kidney card or domain assembler registration
- eGFR not in `scoring_policy.yaml` kidney system biomarkers (creatinine + urea only)
- No standalone ACR/UACR package or signal
- Urea signals not in medical frame index
- Legacy s24 creatinine frames partially active with medical review pending
- No renal pathway explainer
- urea/uacr retail explainers missing

### 7.8 Implementation-readiness judgement

**Candidate for P1-2:** **Yes — recommended first.**

Smallest bounded biomarker set, clearest runtime-active canonical signals, tested collision model, existing kidney scoring rail, and lower context-gate complexity than thyroid. Prose and compiled-card gaps remain but are structurally similar across all three domains and can be sequenced with P2-1 substrate work.

---

## 8. Cross-domain findings

**Shared assets:**

- Wave 1 domain assembler pattern in `domain_score_assembler.py` and `wave1_subsystem_evidence.py` (reuse target for all three)
- Retail explainer assembly pipeline (`retail_explainer_assembly_v1.py`)
- Root-cause hypothesis YAML estate under `knowledge_bus/root_cause/hypotheses/`
- Phenotype map and IDL records for cross-domain patterns
- Launch-core fixture `lc_s20_ab_launch_core_v1.json` spans all three domains

**Shared gaps:**

- No compiled health-system cards for any missing domain
- No Wave 1 subsystem/domain registration for blood/iron/oxygen, thyroid/energy, or kidney
- No dedicated pathway explainers for any missing domain
- Partial retail explainer coverage for all three
- `scoring_policy.yaml` does not reflect full launch-core domain scoring intent

**Common missing test patterns:**

- Domain-card assembly regression tests for each missing domain
- End-to-end launch-visible consumer domain row tests
- Subsystem evidence golden tests per domain

**Common prose/explainer needs (feed P2-1):**

- Per-biomarker retail entries for markers with active signals but no explainer
- Domain-level pathway explainers
- Clinician-report section completeness per launch-core domain

**Cross-domain dependency risks:**

- Thyroid–lipid phenotype crosses into cardiovascular domain
- B12/folate/macrocytosis links blood/iron to homocysteine cardiovascular pathway
- Renal collision model affects creatinine/eGFR co-emission — must not break when adding blood/iron domain cards on same panel
- Iron-deficiency inflammation phenotype crosses immune/inflammation framing

**Potential domain interaction issues:**

- Multi-domain panels common in launch-core fixtures; domain assembler must handle co-present domains without double-counting or conflicting narratives
- Lab-range dependency universal — all domains require lab-provided ranges, not global defaults

---

## 9. Recommended first implementation domain for P1-2

**Kidney function**

Evidence basis:

| Criterion | Kidney | Blood/iron/oxygen | Thyroid |
|---|---|---|---|
| Package/spec support | Partial (8 primary) | Strong (30+) | Partial (13) |
| Biomarker clarity | Strong (bounded) | Strong but broad | Strong |
| Signal safety | Partial — tested collision; fewer context gates | Partial — heavy adjudication backlog | Weak — FT3 drift, multi-gates |
| Testability | Partial — collision + scoring tests | Strong | Strong for kb47 only |
| Prose availability | Partial | Partial | Partial |
| Implementation risk | **Lowest among three** | Highest breadth | Highest clinical gating |
| Clinical review load | Moderate | High | High |

The evidence supports selecting kidney function as the first missing launch-core domain implementation sprint.

---

## 10. Recommended P1-2 scope

**Proposed work ID:** P1-2 — Kidney function launch-core domain card (implementation)

**What P1-2 should implement:**

- Compiled Wave 1 kidney health-system card(s) and manifest evidence under `knowledge_bus/compiled/` (governed promotion path only)
- Register kidney subsystems in `wave1_subsystem_evidence.py` and consumer domain row in `domain_score_assembler.py`
- Wire existing runtime-active signals (`signal_egfr_low`, kb52c `signal_creatinine_high`/`signal_creatinine_low`, governed urea signals) into domain assembly without activating blocked frames
- Extend scoring policy kidney system to include eGFR if clinically governed (lab-value driven)
- Regression tests for kidney domain-card assembly, subsystem evidence, and collision preservation
- Update BUILD_DELIVERABLE_REGISTER at closure

**What P1-2 must NOT implement:**

- ACR/UACR standalone signal activation without dedicated package and medical review
- Diagnostic CKD staging or disease labelling
- kb59, kb52c TSH, or blood/iron domain work
- Pass 3 promotion of deferred packages
- Gemini, frontend inference, or Layer C medical reasoning
- Global/default reference range substitution
- Activation of legacy s24 creatinine potassium frame or unadjudicated frames

**STOP gates:**

- Stop if collision resolver behaviour regresses (`test_signal_authority_collision_enforcement.py` fails)
- Stop if any blocked/medical-review-pending frame is activated without explicit governance approval
- Stop if implementation touches frontend Layer C reasoning
- Stop if urea signals are launch-visible without frame-index adjudication

**Likely classification:**

- `change_type`: MIXED (compiled assets + behavioural assembler wiring)
- `risk_level`: HIGH
- Audit path: full Automation Bus SOP, Claude audit summary, GPT architectural review, human approval before merge

---

## 11. Carry-forwards for later sprints

### P1 domain implementation

- P1-2: Kidney function domain card and subsystem wiring (recommended first)
- P1-3: Blood / iron / oxygen domain card — after CBC tranche/adjudication hygiene
- P1-4: Thyroid / energy regulation domain card — after FT3 register reconciliation and kb52c/kb59 adjudication plan
- Reconcile FT3 low register drift across governance files before thyroid implementation
- Resolve TIBC/UIBC SSOT and package gap before full iron-transport interpretation
- Index urea signals in medical frame identity index before launch-visible urea emission
- ACR/albuminuric frame decision: override-only vs dedicated package

### P2 Layer B prose/explainer substrate

- Retail explainers for markers with active signals but no entry (urea, uacr, FT3, FT4, antibodies, CBC indices)
- Dedicated pathway explainers: renal filtration, thyroid hormone axis, blood/iron/oxygen transport
- Clinician-report section completeness per launch-core domain
- Feed gaps identified in Sections 5.5, 6.5, 7.5

### P3 safety/provenance/auditability

- Medical frame adjudication backlog for blood/iron signals (`pass3_frame_coverage_audit_v1.yaml`)
- Legacy s24 creatinine medical review (`blocked_pending_medical_review`)
- Root-cause authority mapping for activated Batch 2 thyroid signals
- Pass 3 promotion decisions for kb52c TSH and kb59 antibody packages
- Package count verification complete (187 — no action required)

### P5 UX/results page

- Launch-visible consumer domain rows for three missing domains (depends on P1-2/P1-3/P1-4)
- Defer UX polish until Layer B domain outputs stable
- Kidney score in `detox_filtration` insight is not substitute for launch-core domain card

---

## 12. Final recommendation

| Question | Recommendation |
|---|---|
| Can P1-2 safely proceed? | **Yes**, for kidney function only, within the bounded scope in Section 10 and with HIGH-risk governance |
| Which domain first? | **Kidney function** |
| Should P2-1 run before, after, or in parallel? | **After P1-2 domain wiring, in parallel with P1-3/P1-4** — prose substrate (P2-1) can begin for kidney retail/pathway gaps once domain assembly shape is known; do not block P1-2 on full P2-1 completion |
| Next prompt | **P1-2 — Kidney function launch-core domain card and subsystem wiring** |

---

*Mapping completed under work package P1-1. All evidence paths verified from repository inspection on 2026-06-20. No runtime files modified.*
