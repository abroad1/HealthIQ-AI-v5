# Analytical Assets Inventory
## Biomarker Clustering, Correlations, Ratios, and Health System Scoring

**Version:** 5.2  
**Status:** Active  
**Type:** Architecture Baseline Freeze  
**Scope:** Documentation Hardening Only (No Runtime Changes)

**Report Type:** Factual Research Audit (No Recommendations)  
**Scope:** HealthIQ-AI v5 Backend  
**Date:** February 2025

Previous versions should be stored under /docs/archive/.

---

## 1. Existing Analytical Assets

### Correlation / Network / Interaction Analysis
| Search Term | Location | Finding |
|-------------|----------|---------|
| **correlation** | `core/clustering/rules.py` | `BiomarkerCorrelationRule` class with `correlation_threshold: float` (default 0.6); `ClusteringRule` dataclass with `correlation_threshold` |
| | `core/clustering/engine.py` | `ClusteringAlgorithm.WEIGHTED_CORRELATION` – algorithm exists but correlation logic is name-based grouping, not statistical correlation |
| | `core/clustering/validation.py` | `min_coherence_threshold` – coherence, not correlation |
| **network** | *None found* | No network/graph analysis |
| **interaction** | *None found* | No interaction analysis |
| **matrix** | *None found* | No correlation matrices |

### Clustering Logic
| Component | Location | Description |
|-----------|----------|-------------|
| **ClusteringEngine** (runtime) | `core/clustering/engine.py` | Wired to orchestrator. Algorithms: `RULE_BASED`, `WEIGHTED_CORRELATION`, `HEALTH_SYSTEM_GROUPING` (default: `RULE_BASED`). Uses `ClusteringRuleEngine` and `ClusterValidator`. |
| **Cluster Engine v2** | `core/clustering/cluster_engine_v2.py` | **Not wired to runtime.** Sprint 16 engine-only. Reads `ssot/cluster_rules.yaml` (currently `rules: []`). Expects `biomarkers` and `derived` lists. Uses SSOT `system` field for 8 clusters: metabolic, cardiovascular, hepatic, renal, inflammatory, hematological, hormonal, nutritional. |
| **ClusteringRuleEngine** | `core/clustering/rules.py` | Rule-based clustering: metabolic_dysfunction, cardiovascular_risk, inflammatory_burden, nutritional_deficiency, organ_function, hormonal_imbalance. Requires `score_thresholds`; no actual correlation computation. |
| **ClusterValidator** | `core/clustering/validation.py` | Validates cluster size, coherence. Hard-coded health-system→biomarker mapping. |

### Exploratory / Analysis Scripts
| Asset | Location | Purpose |
|-------|----------|---------|
| **smoke_cluster_engine_v2.py** | `scripts/smoke_cluster_engine_v2.py` | Smoke test for `cluster_engine_v2.score_clusters`; not part of main pipeline |
| **verify_singleton_request.py** | `scripts/verify_singleton_request.py` | Verifies alias registry singleton |
| **pre_pr_check.ps1** | `scripts/pre_pr_check.ps1` | Runs smoke_cluster_engine_v2 as pre-PR check |

**Notebooks:** None (`.ipynb` files).

---

## 2. Current Cluster Architecture

### Health Systems (Scoring Rules)
Source: `core/scoring/rules.py` – `_load_biomarker_rules()`

| Cluster | Biomarkers | Weights | Min Required | System Weight |
|---------|------------|---------|--------------|---------------|
| **metabolic** | glucose, hba1c, insulin | 0.4, 0.4, 0.2 | 2 | 0.25 |
| **cardiovascular** | total_cholesterol, ldl_cholesterol, hdl_cholesterol, triglycerides, tc_hdl_ratio | 0.2, 0.3, 0.3, 0.2, 0.1 | 3 | 0.25 |
| **inflammatory** | crp | 1.0 | 1 | 0.15 |
| **hormonal** | *(empty)* | — | 0 | 0.0 |
| **nutritional** | *(empty)* | — | 0 | 0.0 |
| **kidney** | creatinine, bun | 0.6, 0.4 | 1 | 0.15 |
| **liver** | alt, ast | 0.5, 0.5 | 1 | 0.1 |
| **cbc** | hemoglobin, hematocrit, white_blood_cells, platelets | 0.4, 0.3, 0.2, 0.1 | 2 | 0.1 |

### Clustering Engine (Runtime) Health System Mapping
Source: `core/clustering/engine.py` – `_group_biomarkers_by_health_system()`

| System | Biomarkers |
|--------|------------|
| metabolic | glucose, hba1c, insulin, homa_ir |
| cardiovascular | total_cholesterol, ldl_cholesterol, hdl_cholesterol, triglycerides |
| inflammatory | crp, esr, il6 |
| kidney | creatinine, bun, egfr |
| liver | alt, ast, bilirubin, alp |
| cbc | hemoglobin, hematocrit, wbc, platelets |
| hormonal | tsh, free_t4, testosterone, estradiol |
| nutritional | vitamin_d, b12, folate, iron, ferritin |

**Note:** `homa_ir` and `wbc` appear in clustering but not in scoring rules. Scoring uses `white_blood_cells`; clustering uses `wbc`.

### Cluster Engine v2 (Not Wired)
Source: `core/clustering/cluster_engine_v2.py` – reads `ssot/biomarkers.yaml` `system` field. Defines 8 clusters: metabolic, cardiovascular, hepatic, renal, inflammatory, hematological, hormonal, nutritional. Naming differs from scoring (e.g. hepatic vs liver, renal vs kidney, hematological vs cbc).

### Cluster Types (Rule Engine)
Source: `core/clustering/rules.py`

- `METABOLIC_DYSFUNCTION`
- `CARDIOVASCULAR_RISK`
- `INFLAMMATORY_BURDEN`
- `NUTRITIONAL_DEFICIENCY`
- `ORGAN_FUNCTION`
- `HORMONAL_IMBALANCE`
- `GENERAL_HEALTH`

---

## 3. Ratio Infrastructure

### Defined Derived Ratios (Scoring)
Source: `core/scoring/rules.py`

| Ratio | In DERIVED_RATIOS | In DERIVED_RATIO_BOUNDS | Notes |
|-------|-------------------|---------------------------|-------|
| **tc_hdl_ratio** | Yes | Yes (min: 0, max: 5.0) | Total cholesterol / HDL. Scored when lab provides value or via bounds |
| **tg_hdl_ratio** | Yes | Yes (min: 0, max: 4.0) | Triglycerides / HDL |
| **ldl_hdl_ratio** | Yes | Yes (min: 0, max: 3.5) | LDL / HDL |
| **chol_hdl_ratio** | Yes | No | Alias/synonym for tc_hdl_ratio; no bounds |
| **apoB_apoA1_ratio** | Yes | No | No bounds; unscored when lab doesn't supply |
| **non_hdl_cholesterol** | Yes | No | No bounds; unscored when lab doesn't supply |

### Ratio Computation Locations
| Location | Ratios Computed | Usage |
|----------|-----------------|-------|
| **core/insights/modules/metabolic_age.py** | tc_hdl_ratio, tg_hdl_ratio | Ad-hoc for metabolic age insight; not fed to scoring |
| **core/insights/modules/heart_insight.py** | ldl_hdl_ratio, tc_hdl_ratio, tg_hdl_ratio | Ad-hoc for heart insight; not fed to scoring |

### Pipeline Integration
- **Normalizer** (`core/canonical/normalize.py`): Does not compute derived ratios.
- **Orchestrator / Scoring Engine**: Expects ratios to be present in input; does not compute them.
- **safe_ratio** (`core/analytics/primitives.py`): Generic `numerator/denominator` with zero-safety; not used in scoring pipeline.

### Alias Registry
- `biomarker_alias_registry.yaml` defines canonical IDs: tc_hdl_ratio, tg_hdl_ratio, ldl_hdl_ratio, apoB_apoA1_ratio, non_hdl_cholesterol.
- Labs can supply ratios under lab-specific aliases (e.g. `total_cholesterol/hdl_ratio_calculation_(venous)`).

### AST/ALT Ratio
- Not present in `DERIVED_RATIOS` or scoring.
- Referenced in `cluster_engine_v2` docstring as example derived metric ID (`alt_ast`).

---

## 4. SSOT Metadata Depth

### File
`backend/ssot/biomarkers.yaml`

### Fields Per Biomarker
| Field | Present | Example | Notes |
|-------|---------|---------|------|
| **aliases** | Yes | ["ldl", "ldl_chol"] | Used for resolution |
| **unit** | Yes | "mg/dL" | |
| **description** | Yes | "Low-density lipoprotein cholesterol" | |
| **category** | Yes | "cardiovascular" | |
| **data_type** | Yes | "numeric" | |
| **system** | Yes | "cardiovascular" | Organ/system; used by cluster_engine_v2 |
| **clusters** | Yes | [] | Empty for all biomarkers |
| **roles** | Yes | [] or ["insulin_sensitivity_marker"] | Rarely populated |
| **key_risks_when_high** | Yes | [] | Empty |
| **key_risks_when_low** | Yes | [] | Empty |
| **known_modifiers** | Yes | [] or ["fasting_state", "alcohol"] | |
| **clinical_weight** | Yes | 0.6–0.8 | Used in upload SSOT enrichment |

### Absent or Unused
- **Directionality:** Not explicit (e.g. “higher is worse” vs “lower is worse”); inferred in rules.
- **ideal vs reference:** No explicit “ideal” range; scoring uses lab-provided or `DERIVED_RATIO_BOUNDS`.
- **Cluster tagging:** `clusters: []` for all; no cluster IDs populated.

---

## 5. Questionnaire Capability

### Schema
`backend/ssot/questionnaire.json` – ~58 questions.

### Sections & Question IDs

| Section | Question IDs |
|---------|--------------|
| **demographics** | full_name, email_address, phone_number, country, state_province, date_of_birth, biological_sex, height, weight, waist_circumference, body_composition, ethnicity, overall_health_rating, menstrual_hormonal_status, low_testosterone_symptoms |
| **medical_history** | blood_pressure_reading, current_medications, long_term_medications, chronic_conditions, medical_conditions, recent_blood_work |
| **symptoms** | energy_level, current_symptoms, regular_migraines, recent_infections |
| **lifestyle** | diet_quality_rating, fasting_hours, sugar_beverages_weekly, alcohol_drinks_weekly, fruit_vegetable_servings, supplements, dietary_pattern, vigorous_exercise_days, sitting_hours_daily, resistance_training_days, tobacco_use, caffeine_beverages_daily, daily_fluid_intake, pollution_exposure, sleep_hours_nightly, sleep_quality_rating, sleep_schedule_consistency, sleep_disorders, stress_level_rating, stress_control_frequency, major_life_stressors, stress_management_method |
| **functional** | balance_ability, stair_climbing_ability, push_up_capacity, grip_strength_assessment, physical_recovery_time |
| **other** | memory_changes, food_sensitivities, antibiotics_past_two_years, family_cardiovascular_disease, family_diabetes_metabolic, family_cancer_history, family_lifespan |

### Questions That Influence Scoring
Source: `core/pipeline/questionnaire_mapper.py` → `MappedLifestyleFactors` → `create_lifestyle_profile` → `LifestyleOverlays.apply_lifestyle_overlays`

**Mapped to lifestyle overlays:**
- dietary_pattern, fruit_vegetable_servings, sugar_beverages_weekly → diet_level
- sleep_hours_nightly (plus sleep_quality_rating, sleep_schedule_consistency, major_life_stressors) → sleep_hours, stress_level
- vigorous_exercise_days, resistance_training_days → exercise_minutes_per_week
- alcohol_drinks_weekly (or alcohol_consumption) → alcohol_units_per_week
- tobacco_use (or smoking_status) → smoking_status
- stress_level_rating, stress_control_frequency, major_life_stressors → stress_level

**Additional mapped but not used in overlays:**
- sitting_hours_daily → sedentary_hours_per_day
- caffeine_beverages_daily → caffeine_consumption
- daily_fluid_intake → fluid_intake_liters

### Medical History (QRISK3-relevant)
Mapped in `MappedMedicalHistory`: atrial_fibrillation, rheumatoid_arthritis, systemic_lupus, corticosteroids, atypical_antipsychotics, hiv_treatments, migraines. Used in insight/risk context; not in scoring pipeline.

### Collected but Unused for Scoring
- full_name, email_address, phone_number, country, state_province
- body_composition
- overall_health_rating
- energy_level, current_symptoms, recent_infections
- diet_quality_rating, fasting_hours, supplements
- pollution_exposure, sleep_quality_rating, sleep_schedule_consistency, sleep_disorders
- stress_management_method
- balance_ability, stair_climbing_ability, push_up_capacity, grip_strength_assessment, physical_recovery_time
- memory_changes, food_sensitivities, antibiotics_past_two_years
- family_* (cardiovascular_disease, diabetes_metabolic, cancer_history, lifespan)

---

## 6. Scoring Infrastructure

### HAS v1 Primitives
**Location:** `backend/core/analytics/primitives.py`

| Primitive | Purpose | Used By |
|-----------|---------|---------|
| **position_in_range(value, low, high)** | 0..1 position in range; extends beyond for out-of-range | `core/scoring/rules.py` → `_calculate_score_from_range` |
| **map_position_to_status(pos)** | Maps position to status: low_critical, low_borderline, normal, optimal, high_borderline, high_critical | Same |
| **calculate_confidence(n_present, n_expected)** | Confidence from presence ratio | Scoring, clustering, insights |
| **safe_ratio(numerator, denominator)** | Safe division; returns None on zero/None | Tested; not used in scoring pipeline |

### Status Mapping
| Location | Mapping | Purpose |
|----------|---------|---------|
| `core/scoring/rules.py` | `_HAS_TO_SCORE_RANGE` | HAS status → ScoreRange enum (optimal, normal, borderline, high, very_high, critical) |
| `core/analytics/primitives.py` | `STATUS_FROM_HAS_TO_FRONTEND` | HAS status → frontend: optimal, normal, elevated, low, critical, unknown |
| `core/analytics/primitives.py` | `has_status_to_frontend()` | Wrapper for frontend status |
| `core/analytics/primitives.py` | `frontend_status_from_value_and_range()` | Value + lab range → frontend status |

### Confidence Mapping
- `core/scoring/engine.py`: `_determine_biomarker_confidence()`, `_determine_system_confidence()`, `_determine_overall_confidence()`
- `core/analytics/primitives.py`: `calculate_confidence()` for completeness-based confidence

---

## 7. Gaps & Opportunities

### Unused Assets
| Asset | Location | Status |
|-------|----------|--------|
| Cluster Engine v2 | `core/clustering/cluster_engine_v2.py` | Not wired to orchestrator |
| cluster_rules.yaml | `ssot/cluster_rules.yaml` | Empty (`rules: []`) |
| safe_ratio | `core/analytics/primitives.py` | Not used in scoring/derived-ratio flow |
| WEIGHTED_CORRELATION | `ClusteringAlgorithm` | Algorithm exists; implementation is grouping, not correlation |
| SSOT `clusters` | biomarkers.yaml | Empty for all biomarkers |

### Experimental / Stub Code
| Item | Location | Notes |
|------|----------|-------|
| cluster_engine_v2 | `core/clustering/cluster_engine_v2.py` | Sprint 16 engine-only; docstring says “not wired to runtime” |
| cluster_rules.yaml | `ssot/cluster_rules.yaml` | Minimal stub; “Rules will be expanded in future sprints” |

### Deprecated / Legacy
| Item | Location | Notes |
|------|----------|-------|
| on_event | `app/main.py` | DeprecationWarning |
| ScoredContext | `core/insights/base.py` | “Legacy ScoredContext is fully deprecated and unsupported” |
| legacy payload | `core/context/`, tests | Legacy payload format still supported |

### Duplicated Logic
| Logic | Locations | Notes |
|-------|-----------|-------|
| Health system → biomarkers mapping | `core/clustering/engine.py`, `core/clustering/validation.py` | Hard-coded in both; differs from `core/scoring/rules.py` |
| Cluster/system names | Scoring, clustering, cluster_engine_v2 | liver/hepatic, kidney/renal, cbc/hematological |
| Ratio computation | metabolic_age.py, heart_insight.py | tc_hdl, tg_hdl, ldl_hdl computed locally in insights; not shared with scoring |

### Potential Contradictions
| Area | Contradiction |
|------|---------------|
| Derived ratio computation | DERIVED_RATIOS suggest v5 computes ratios; normalizer and orchestrator do not. Ratios must be supplied by input or computed elsewhere. |
| Cluster engine usage | Orchestrator uses `ClusteringEngine`; `cluster_engine_v2` is separate, uses different cluster names and SSOT `system` field. |
| Biomarker naming | Clustering uses `wbc`; scoring uses `white_blood_cells`. Clustering uses `homa_ir`; not in scoring rules. |

---

## 8. Risks

| Risk | Description |
|------|-------------|
| **Derived ratio gap** | tc_hdl_ratio, tg_hdl_ratio, ldl_hdl_ratio can be scored via DERIVED_RATIO_BOUNDS, but no pipeline step computes and injects them. Labs must supply or upstream must compute. |
| **Dual clustering design** | ClusteringEngine (runtime) and cluster_engine_v2 (standalone) have different models; future unification may cause breaking changes. |
| **Questionnaire validation** | Unknown question IDs cause validation failures; mapper continues with defaults. Strict validation could block incomplete submissions. |
| **Age/sex adjustments** | TODO in scoring rules: “Age/sex adjustments defined but NOT applied in calculate_biomarker_score.” |
| **SSOT cluster tagging** | `clusters: []` for all biomarkers; cluster definitions live in code, not SSOT. |

---

## 9. v5 Migration Strategy

*Amendment v5.2: Documentation hardening; no runtime changes.*

Clarifications for migrating from v4 to v5:

* **v4 YAML correlation rules** will be re-authored manually into v5 schema. No direct file imports from v4.
* **Ratio definitions** will be rewritten into v5 RatioRegistry. No reuse of v4 ratio logic.
* **cluster_engine_v2** will be populated using v4 cluster concepts but with canonical IDs only. Migration is manual, not automated.

> **v4 files are reference-only and must never be imported into runtime.**
