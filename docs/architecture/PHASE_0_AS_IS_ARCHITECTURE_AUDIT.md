# Phase 0 – Full As-Is Architecture Audit

**HealthIQ AI v5 – Structural Forensic Audit (Read-Only)**

**Date:** 2025-02-11  
**Purpose:** Produce a precise structural map of the current analytical architecture for HealthIQ Analytical Substrate (HAS) design without duplication or drift.

---

## 1️⃣ End-to-End Analytical Data Flow

### High-Level Flow Diagram (Text-Based)

```
┌─────────────────┐
│  API Entry      │  POST /api/analysis/start
│  analysis.py    │  Request: { biomarkers, user }
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌────────────────────────────────────────┐
│ ContextFactory   │     │ normalize_biomarkers_with_metadata()     │
│ create_context() │◀────│ normalize.py (preserves reference_range) │
└────────┬────────┘     └────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│ AnalysisOrchestrator.run(biomarkers, user, assume_canonical=True) │
└────────┬────────────────────────────────────────────────────────┘
         │
         │ Step 1: Quarantine unmapped biomarkers (alias_service.resolve)
         │ Step 2: Extract simple_biomarkers + input_reference_ranges
         ▼
┌─────────────────────────────────────────────────────────────────┐
│ SCORING: score_biomarkers() → ScoringEngine.score_biomarkers()  │
│   - normalize_biomarkers() (if raw dict)                        │
│   - _score_health_system() x8 (metabolic, cardio, inflam, etc.) │
│   - rules.calculate_biomarker_score() [position-in-range]       │
│   - LifestyleOverlays.apply_lifestyle_overlays() [modifiers]     │
└────────┬────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│ CONTEXT: create_analysis_context() → AnalysisContext            │
│   - QuestionnaireMapper.map_submission() if questionnaire_data  │
│   - lifestyle_factors, medical_history → user_data               │
└────────┬────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│ CLUSTERING: cluster_biomarkers() → ClusteringEngine               │
│   - RULE_BASED algorithm (ClusteringRuleEngine.apply_rules)     │
│   - Uses biomarker_values + biomarker_scores from scoring       │
└────────┬────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│ INSIGHTS: synthesize_insights() → InsightSynthesizer            │
│   - LLM-driven (GeminiClient or MockLLMClient)                  │
│   - InsightPromptTemplates per category                         │
│   - Consumes biomarker_scores, clustering_results, lifestyle    │
└────────┬────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│ DTO BUILD: Inline in orchestrator.run() (Steps 6–9)            │
│   - BiomarkerScoreDTO from scoring + resolver (unit, ref_range)  │
│   - ClusterHit from clustering_result                           │
│   - InsightResult from insights_result                           │
│   - AnalysisDTO final assembly                                  │
└────────┬────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐     ┌────────────────────────────────────────┐
│ _analysis_results│     │ GET /api/analysis/result               │
│ (in-memory dict) │───▶│ build_analysis_result_dto(result)       │
└─────────────────┘     └────────────────────────────────────────┘
```

### Stage-by-Stage Map

| Stage | File(s) | Class/Function | Input | Output | Dependencies |
|-------|---------|----------------|-------|--------|--------------|
| **Biomarker input** | `app/routes/analysis.py` | `start_analysis()` | `request.biomarkers` (dict), `request.user` | `normalize_biomarkers_with_metadata()` | `ContextFactory`, `normalize`, `orchestrator` |
| **Canonical normalisation** | `core/canonical/normalize.py` | `BiomarkerNormalizer.normalize_biomarkers()` | `Dict[str, Any]` raw biomarkers | `Tuple[BiomarkerPanel, List[str]]` | `AliasRegistryService`, `CanonicalResolver` |
| | `core/canonical/alias_registry_service.py` | `AliasRegistryService.resolve()` | alias string | canonical or `unmapped_{raw}` | `biomarker_alias_registry.yaml`, `biomarkers.yaml` |
| **Validation (completeness)** | `core/validation/completeness.py` | `DataCompletenessValidator.assess_completeness()` | `Dict` biomarkers | `CompletenessResult` | `BiomarkerNormalizer` |
| **Validation (gaps)** | `core/validation/gaps.py` | `BiomarkerGapAnalyzer.analyze_gaps()` | `Dict` biomarkers | gap analysis dict | `BiomarkerNormalizer` |
| **Scoring** | `core/scoring/engine.py` | `ScoringEngine.score_biomarkers()` | biomarkers dict, age, sex, lifestyle_profile, input_reference_ranges | `ScoringResult` | `ScoringRules`, `LifestyleOverlays`, `BiomarkerNormalizer` |
| **Scoring rules** | `core/scoring/rules.py` | `ScoringRules.calculate_biomarker_score()`, `_calculate_score_from_range()` | value, min, max (from lab or derived) | (score 0–100, ScoreRange, unscored_reason) | None |
| **Cluster engines** | `core/clustering/engine.py` | `ClusteringEngine.cluster_biomarkers()` | `AnalysisContext`, scoring_result | `ClusteringResult` | `ClusteringRuleEngine`, `EngineWeightingSystem`, `ClusterValidator` |
| | `core/clustering/rules.py` | `ClusteringRuleEngine.apply_rules()` | biomarker_values, biomarker_scores | `List[BiomarkerCluster]` | hardcoded rules |
| **Insight engines** | `core/insights/synthesis.py` | `InsightSynthesizer.synthesize_insights()` | context, biomarker_scores, clustering_results, lifestyle_profile | `InsightSynthesisResult` | `InsightPromptTemplates`, `GeminiClient` or `MockLLMClient` |
| **DTO build** | `core/pipeline/orchestrator.py` (inline) | Steps 6–9 in `run()` | scoring_result, clustering_result, insights_result, context | `AnalysisDTO` | `CanonicalResolver`, `core.models.results` |
| **API response** | `app/routes/analysis.py` | `get_analysis_result()` | analysis_id | dict via `build_analysis_result_dto()` | `core/dto/builders.py` |

---

## 2️⃣ Scoring Engines (Current State)

Scoring is implemented as **one master engine** (`ScoringEngine`) that iterates over **8 health-system rule sets**. There are no separate “engines” per health domain; the structure is monolithic with rule-driven dispatch.

### Scoring Engine Summary

| Attribute | Value |
|-----------|-------|
| **File** | `backend/core/scoring/engine.py` |
| **Engine name** | `ScoringEngine` (single unified engine) |
| **Rule source** | `core/scoring/rules.py` – `ScoringRules._load_biomarker_rules()` |

### Per–Health-System Scoring Rules

| Health System | Biomarkers | Weights (per biomarker) | Uses Lab Ranges | Uses Z-Score | Position-in-Range | Hard Thresholds | Weights | Final Score (0–100) | Confidence | Age/Sex Modifiers | Missing Downgrades |
|--------------|------------|-------------------------|-----------------|-------------|-------------------|-----------------|---------|---------------------|------------|-------------------|-------------------|
| **metabolic** | glucose, hba1c, insulin | 0.4, 0.4, 0.2 | ✅ Yes (only lab) | ❌ No | ✅ Yes | ❌ No (lab only) | ✅ Yes | Weighted avg | ✅ Yes | glucose, hba1c: age | ✅ Yes |
| **cardiovascular** | total_cholesterol, ldl, hdl, triglycerides, tc_hdl_ratio | 0.2–0.3 each | ✅ Yes | ❌ No | ✅ Yes | ❌ No | ✅ Yes | Weighted avg | ✅ Yes | hdl: sex | ✅ Yes |
| **inflammatory** | crp | 1.0 | ✅ Yes | ❌ No | ✅ Yes | ❌ No | N/A | Single | ✅ Yes | — | ✅ Yes |
| **hormonal** | (none) | — | — | — | — | — | — | 0.0 | — | — | — |
| **nutritional** | (none) | — | — | — | — | — | — | 0.0 | — | — | — |
| **kidney** | creatinine, bun | 0.6, 0.4 | ✅ Yes | ❌ No | ✅ Yes | ❌ No | ✅ Yes | Weighted avg | ✅ Yes | creatinine: age, sex | ✅ Yes |
| **liver** | alt, ast | 0.5 each | ✅ Yes | ❌ No | ✅ Yes | ❌ No | ✅ Yes | Weighted avg | ✅ Yes | alt: sex | ✅ Yes |
| **cbc** | hemoglobin, hematocrit, white_blood_cells, platelets | 0.4, 0.3, 0.2, 0.1 | ✅ Yes | ❌ No | ✅ Yes | ❌ No | ✅ Yes | Weighted avg | ✅ Yes | hgb, hct: sex | ✅ Yes |

### Scoring Logic Summary

- **Reference ranges:** Lab ranges from input (e.g. `reference_range` / `referenceRange`) are used first. For lab-provided biomarkers, SSOT and rule fallbacks are never used.
- **Derived ratios:** Only `tc_hdl_ratio`, `tg_hdl_ratio`, `ldl_hdl_ratio` may use hard-coded `DERIVED_RATIO_BOUNDS` when the lab did not supply a range.
- **Position-in-range:** `_calculate_score_from_range(value, min, max)` computes `position = (value - min) / (max - min)` and maps to bands:
  - Optimal: 0.2–0.8 → 100
  - Normal: 0.1–0.9 → 90–100
  - Borderline: 0.05–0.95 → 50–90
  - Low/High/Critical: outside bands → linear decay
- **Confidence:** Per biomarker from `ScoreRange`; per system from biomarker confidence and `min_biomarkers_required`; overall from completeness and system confidence.
- **Age/sex:** `_apply_adjustments()` in rules exists but is not used in `calculate_biomarker_score()`; age/sex are passed but not applied.
- **Missing data:** Missing biomarkers excluded from weighted total; system confidence reduced; overall confidence influenced by completeness validator.

---

## 3️⃣ Shared Analytical Logic (Current State)

| Primitive | Location | Reusable? | Duplicated? | Consistent? |
|-----------|----------|-----------|-------------|-------------|
| **Normalisation** | `core/canonical/normalize.py` – `BiomarkerNormalizer.normalize_biomarkers()` | ✅ Yes | ❌ No central dup | ⚠️ Alias service maps `ldl_cholesterol`→`ldl`, others use `ldl_cholesterol` |
| **Z-score** | — | — | — | **Not implemented** |
| **Percentile** | — | — | — | **Not implemented** |
| **Weighting logic** | `core/scoring/engine.py` – `_score_health_system()` uses `rule.weight` | ⚠️ Local to scoring | ❌ No | N/A |
| **Composite score** | `core/scoring/engine.py` – `_calculate_overall_score()` uses `system_weight` | ⚠️ Local | ❌ No | N/A |
| **Risk banding** | `core/scoring/rules.py` – `ScoreRange` enum, `_calculate_score_from_range()` | ✅ Reusable | ⚠️ Orchestrator reuses for unscored biomarkers | Partial |
| **Modifier overlays** | `core/scoring/overlays.py` – `LifestyleOverlays.apply_lifestyle_overlays()` | ✅ Reusable | ❌ No | N/A |
| **Confidence scoring** | `core/scoring/engine.py` – `_determine_*_confidence()` | ⚠️ Local | ❌ No | N/A |
| **Missing-data handling** | `core/scoring/engine.py`, `core/validation/completeness.py` | ⚠️ Split | ⚠️ Multiple concepts | Partial |

### Canonical Name Inconsistency

- **AliasRegistryService** maps: `ldl_cholesterol` → `ldl`, `hdl_cholesterol` → `hdl`.
- **Scoring rules** use: `ldl`, `hdl`.
- **Clustering rules** use: `ldl_cholesterol`, `hdl_cholesterol`.
- **Heart insight** uses: `ldl_cholesterol`, `hdl_cholesterol`.
- **Completeness validator** uses: `ldl_cholesterol`, `hdl_cholesterol`.

After normalisation, panel keys are `ldl` and `hdl`, so clustering and heart insight will not match and will treat these as missing.

---

## 4️⃣ Cluster Engine Architecture

### Active Cluster Engine

| Attribute | Value |
|-----------|-------|
| **File** | `backend/core/clustering/engine.py` |
| **Class** | `ClusteringEngine` |
| **Algorithm** | `ClusteringAlgorithm.RULE_BASED` (default) |
| **How clusters are calculated** | `ClusteringRuleEngine.apply_rules()` – rule-based, biomarker score thresholds |
| **Uses SSOT metadata** | ❌ No – hardcoded `BiomarkerCorrelationRule` instances |
| **Weighting** | `EngineWeightingSystem` present but not used in RULE_BASED path |
| **Confidence** | `_calculate_cluster_confidence()` – variance of scores, size boost |
| **Feeds insights** | ✅ Yes – `clustering_results` passed to `InsightSynthesizer` |

### Cluster Rule Definitions (Hardcoded)

| Rule | Required Biomarkers | Optional | Score Thresholds | Min Size |
|------|---------------------|----------|------------------|----------|
| metabolic_dysfunction | glucose, hba1c | insulin, homa_ir | 0–70 | 2 |
| cardiovascular_risk | total_cholesterol, ldl_cholesterol | hdl_cholesterol, triglycerides | 0–70 (ldl), 30–100 (hdl) | 2 |
| inflammatory_burden | crp | esr, il6 | 0–70 | 1 |
| organ_function | creatinine, alt | bun, ast, egfr | 0–70 | 2 |
| nutritional_deficiency | vitamin_d, b12 | folate, iron, ferritin | 0–70 | 2 |
| hormonal_imbalance | tsh | free_t4, testosterone, estradiol | 0–70 | 1 |

**Note:** Required biomarkers use `ldl_cholesterol` and `hdl_cholesterol`; after alias resolution, keys are `ldl` and `hdl`, so cardiovascular clusters will not form.

### Cluster Engine v2 (Not Wired)

| Attribute | Value |
|-----------|-------|
| **File** | `backend/core/clustering/cluster_engine_v2.py` |
| **Status** | Engine-only; not called by orchestrator |
| **Uses SSOT** | ✅ Yes – `ssot/biomarkers.yaml` for cluster membership |
| **Uses cluster_rules.yaml** | ✅ Yes – `ssot/cluster_rules.yaml` (currently empty `rules: []`) |
| **Scoring** | Custom flag-based logic (high/low) and rule compensations |

---

## 5️⃣ Insight Engine Architecture

### Runtime Insight Path (LLM)

| Attribute | Value |
|-----------|-------|
| **File** | `backend/core/insights/synthesis.py` |
| **Deterministic or LLM** | **LLM-driven** (GeminiClient or MockLLMClient) |
| **Consumes** | `biomarker_scores`, `clustering_results`, `lifestyle_profile` |
| **Recomputes logic** | ❌ No – passes data to LLM via prompts |
| **Modifiers** | Used upstream (scoring overlays); not reapplied in synthesis |
| **Confidence** | Per insight from LLM; overall from average |
| **Red-flag routing** | ❌ No explicit routing |

### Modular Insight Modules (Not Wired)

These are registered in `InsightRegistry` but **not invoked** by `InsightSynthesizer`:

| File | Module | Deterministic | Biomarkers Consumed | Thresholds | Confidence |
|------|--------|---------------|---------------------|------------|------------|
| `modules/metabolic_age.py` | MetabolicAgeInsight | ✅ Yes | glucose, hba1c, insulin, age; opt: lipids, bmi, waist | HOMA-IR >2.5, HbA1c >5.7, TC/HDL >4, etc. | Based on biomarker count |
| `modules/heart_insight.py` | HeartInsight | ✅ Yes | total_cholesterol, hdl_cholesterol, ldl_cholesterol | LDL/HDL >3.5, TC/HDL >4, etc. | Based on biomarker count |
| `modules/inflammation.py` | InflammationInsight | ✅ Yes | crp, esr, il6 | CRP thresholds | Based on biomarker count |
| `modules/fatigue_root_cause.py` | FatigueRootCauseInsight | ✅ Yes | (context-based) | Various | Based on coverage |
| `modules/detox_filtration.py` | DetoxFiltrationInsight | ✅ Yes | creatinine, alt, ast, etc. | Organ thresholds | Based on coverage |

- **Duplicate logic:** Metabolic age (HOMA-IR, HbA1c, lipid ratios) and heart insight (LDL/HDL, TC/HDL, TG/HDL) repeat calculations and thresholds.
- **Age/sex:** Applied only in modular insights (metabolic age, heart), not in LLM path.
- **Missing data:** Each module uses its own `can_analyze()` and confidence logic.

---

## 6️⃣ Questionnaire Integration

### Entry Point

| Where | How |
|-------|-----|
| **Orchestrator** | `create_analysis_context()` accepts `questionnaire_data`; maps via `QuestionnaireMapper.map_submission()` |
| **Analysis route** | `request.user` may contain `lifestyle_factors`; questionnaire data is not explicitly passed in the current `/start` flow |
| **User dict** | May include `lifestyle_factors` (diet, sleep, exercise, alcohol, smoking, stress) |

### Transformation

| Component | File | Output |
|-----------|------|--------|
| **QuestionnaireMapper** | `core/pipeline/questionnaire_mapper.py` | `MappedLifestyleFactors`, `MappedMedicalHistory` |
| **Question schema** | `ssot/questionnaire.json` | Semantic IDs for 58 questions |

### Consumer Mapping

| Consumer | Questionnaire Use |
|---------|-------------------|
| **Scoring** | `LifestyleOverlays` – diet_level, sleep_hours, exercise_minutes_per_week, alcohol_units_per_week, smoking_status, stress_level |
| **Insight synthesis** | `lifestyle_profile` dict passed to LLM prompts |
| **Context** | `user_data` updated with `lifestyle_factors`, `medical_history`, demographics |

### Deterministic vs Narrative

- **Deterministic:** `QuestionnaireMapper` produces structured lifestyle and medical fields.
- **Narrative:** LLM prompts receive lifestyle text for insight generation.
- **Hard-coded thresholds:** In `QuestionnaireMapper` (e.g. `_map_diet_level()`, `_map_sleep_level()`).
- **Standardisation:** Logic is centralised in `QuestionnaireMapper`; modifiers applied via `LifestyleOverlays` in scoring.

---

## 7️⃣ DTO / API Layer

### Packaging Flow

1. **Orchestrator** builds `BiomarkerScoreDTO`, `ClusterHit`, `InsightResult` inline in `run()` (Steps 6–9).
2. Stored in `_analysis_results[analysis_id]` as a dict.
3. **GET /result** returns `build_analysis_result_dto(result)`.

### Transformations

| Element | Where | Transformation |
|---------|-------|----------------|
| **Biomarkers** | Orchestrator Step 6 | Scoring → DTO; unscored biomarkers scored via `_calculate_score_from_range()` if ref range available |
| **Unit** | `CanonicalResolver.get_biomarker_metadata()`, input ranges | Input range > SSOT |
| **Reference range** | Input > SSOT > fallback | `reference_range_dict` with min, max, unit, source |
| **Status** | `ScoreRange` → frontend | optimal, normal, elevated, low, critical, unknown |
| **Score** | 0–100 → 0–1 | divided by 100 |
| **Clusters** | Direct mapping | cluster_id, name, biomarkers, description, severity, confidence |
| **Insights** | Direct mapping | id, category, summary, confidence, severity, recommendations, biomarkers_involved |

### Raw vs Scored Consumption

- **Insights:** Consume scored outputs (biomarker_scores, clusters) from upstream; no direct use of raw biomarker values.
- **Confidence:** Survives to API – biomarker confidence in scoring, cluster confidence, insight confidence in synthesis.

---

## 8️⃣ Duplication & Coupling Assessment

### Duplication Map

| Area | Location(s) | Nature |
|------|-------------|--------|
| **Position-in-range logic** | `scoring/rules.py` `_calculate_score_from_range()`, orchestrator inline for unscored | Same algorithm in two places |
| **Status mapping (ScoreRange → frontend)** | Orchestrator (scored + unscored paths) | Repeated `status_map`, borderline/critical refinement |
| **Canonical name inconsistency** | Alias `ldl`/`hdl` vs clustering/insights `ldl_cholesterol`/`hdl_cholesterol` | Structural mismatch |
| **Confidence calculation** | Scoring engine, clustering engine, insight synthesis | Three separate formulas |
| **LDL/HDL, TC/HDL, TG/HDL ratios** | MetabolicAgeInsight, HeartInsight (unwired) | Duplicated ratios and thresholds |
| **Health system → biomarkers** | Completeness, clustering engine, cluster_engine_v2, gaps | Multiple hardcoded maps |
| **Severity bands** | Clustering rules, cluster creation, insight synthesis | Similar bands in multiple places |

### Coupling

| Coupling | Description |
|----------|--------------|
| **Orchestrator → all** | Orchestrator depends on scoring, clustering, insights, validation, DTO construction |
| **Scoring → rules** | Tight: rules define structure; engine is generic dispatcher |
| **Clustering → scoring** | Expects scoring output structure (dict or `ScoringResult`) |
| **Insights → scoring + clustering** | Expects both; no fallback if one is empty |
| **Context creation** | Two paths: `ContextFactory` (route) and `orchestrator.create_analysis_context()` |

### Modifier Inconsistencies

| Modifier | Where Applied | Standardised? |
|----------|---------------|--------------|
| **Age** | Rules define `age_adjustment` but it is not used in `calculate_biomarker_score()` | ❌ No |
| **Sex** | Rules define `sex_adjustment` but it is not used in `calculate_biomarker_score()` | ❌ No |
| **Lifestyle** | `LifestyleOverlays` – multipliers 0.8–1.1 by factor | ✅ Centralised |

### Refactor Hotspots (Structural Only)

1. **Canonical naming:** Align `ldl`/`hdl` vs `ldl_cholesterol`/`hdl_cholesterol` across alias, scoring, clustering, insights.
2. **Position-in-range:** Extract shared primitive from rules and orchestrator.
3. **Status mapping:** Unify ScoreRange → frontend status in one place.
4. **Health system metadata:** Centralise system → biomarkers mapping (SSOT or single module).
5. **Modular insights vs LLM:** Either wire modular insights into pipeline or remove; avoid parallel unused paths.
6. **Cluster engine v2:** Decide wiring vs removal.
7. **Age/sex in scoring:** Implement or remove `_apply_adjustments()` usage.
8. **Context creation:** Single path (ContextFactory or orchestrator) for context creation.

---

## Appendix: File Reference Index

| Concern | Primary Files |
|---------|---------------|
| **Canonical** | `canonical/normalize.py`, `canonical/alias_registry_service.py`, `canonical/resolver.py` |
| **Scoring** | `scoring/engine.py`, `scoring/rules.py`, `scoring/overlays.py` |
| **Clustering** | `clustering/engine.py`, `clustering/rules.py`, `clustering/weights.py`, `clustering/validation.py` |
| **Insights** | `insights/synthesis.py`, `insights/prompts.py`, `insights/modules/*.py`, `insights/registry.py` |
| **Validation** | `validation/completeness.py`, `validation/gaps.py`, `validation/recommendations.py` |
| **Pipeline** | `pipeline/orchestrator.py`, `pipeline/questionnaire_mapper.py`, `pipeline/context_factory.py` |
| **API** | `app/routes/analysis.py` |
| **DTO** | `dto/builders.py`, inline in `orchestrator.run()` |
| **SSOT** | `ssot/biomarkers.yaml`, `ssot/biomarker_alias_registry.yaml`, `ssot/ranges.yaml`, `ssot/cluster_rules.yaml` |

---

*End of Phase 0 As-Is Architecture Audit. No code changes. No refactors. Structural map only.*
