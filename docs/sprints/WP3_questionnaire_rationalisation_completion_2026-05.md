# WP3 — Questionnaire rationalisation (completion note)

**Work ID:** WP3-QUESTIONNAIRE-RATIONALISATION  
**Date:** 2026-05-11

## Outcome

- Single SSOT: `backend/ssot/questionnaire.json` holds **38** questions with **`importance`** tiers (`mandatory` | `recommended` | `optional` | `advanced`). **`required: true`** aligns with **mandatory** questions only.
- Admin PII fields (`full_name`, `email_address`, `phone_number`) and **`current_medications`** were removed from SSOT and mapper medical mapping; **`long_term_medications`** retains governed options including **“Statins (cholesterol medication)”** exactly once.
- **Backend:** `QuestionnaireQuestion.importance`, conditional visibility in **`validate_submission`**, partial **`LifestyleProfile`** / overlay skip-on-`None`, **`QuestionnaireMapper`** unknowns for absent signals (including OBS-2: no false zero exercise), **`AnalysisOrchestrator._lifestyle_profile_from_flat_dict`** so scoring does not inject legacy lifestyle defaults.
- **Frontend:** `importance` on schema type, tier hints on **`QuestionnaireForm`**, mocks aligned to WP3 fields.
- **Tests:** Unit, integration, API, context-hardening, and medical-history representation tests aligned to the new contract.

## Non-goals (unchanged)

Knowledge Bus, narrative compiler, and biomarker interpretation outside the scoped mapper / overlay behaviour were not modified.

---

## Removed question IDs (pre-WP3 → no longer in SSOT)

These **21** semantic IDs were present in the pre-rationalisation **59-question** inventory and are **not** in the current SSOT (delta from audit inventory vs current `questionnaire.json`):

1. `body_composition`  
2. `caffeine_beverages_daily`  
3. `current_medications`  
4. `current_symptoms`  
5. `diet_quality_rating`  
6. `email_address`  
7. `energy_level`  
8. `food_sensitivities`  
9. `fruit_vegetable_servings`  
10. `full_name`  
11. `major_life_stressors`  
12. `overall_health_rating`  
13. `phone_number`  
14. `pollution_exposure`  
15. `recent_blood_work`  
16. `sitting_hours_daily`  
17. `sleep_schedule_consistency`  
18. `state_province`  
19. `stress_control_frequency`  
20. `stress_management_method`  
21. `sugar_beverages_weekly`  

---

## Retained question IDs (by `importance` in current SSOT)

### Mandatory (9)

`alcohol_drinks_weekly`, `biological_sex`, `date_of_birth`, `height`, `long_term_medications`, `sleep_hours_nightly`, `tobacco_use`, `waist_circumference`, `weight`

### Recommended (15)

`blood_pressure_reading`, `chronic_conditions`, `dietary_pattern`, `family_cardiovascular_disease`, `family_diabetes_metabolic`, `fasting_hours`, `medical_conditions`, `recent_infections`, `regular_migraines`, `resistance_training_days`, `sleep_disorders`, `sleep_quality_rating`, `stress_level_rating`, `supplements`, `vigorous_exercise_days`

### Optional (2)

`country`, `ethnicity`

### Advanced (12)

`antibiotics_past_two_years`, `balance_ability`, `daily_fluid_intake`, `family_cancer_history`, `family_lifespan`, `grip_strength_assessment`, `low_testosterone_symptoms`, `memory_changes`, `menstrual_hormonal_status`, `physical_recovery_time`, `push_up_capacity`, `stair_climbing_ability`

---

## Final tier counts (WP3 audit sign-off)

**Audit-approved distribution:** **9** mandatory · **15** recommended · **5** optional · **9** advanced.

**Counts implied by the current `importance` field in `backend/ssot/questionnaire.json`:** **9** mandatory · **15** recommended · **2** optional · **12** advanced.

The lists above reflect the **committed SSOT** (second row). Reconciling optional/advanced counts to the audit’s **5 / 9** is a **governed SSOT-only** retag (no application logic), if programme governance chooses to do so.

---

## Known limitations

1. **Optional vs advanced tier counts:** As noted, the JSON currently tags **2** optional and **12** advanced questions, while the audit sign-off targets **5** optional and **9** advanced.
2. **Stress and diet modelling:** Post-WP3, stress is driven primarily by **`stress_level_rating`**; diet tier is driven by **`dietary_pattern`** only. Finer-grained retired fields are not recoverable from the short form without adding new SSOT questions.
3. **`current_medications`:** Coarse medication bands are no longer collected; long-term medication **classes** remain via **`long_term_medications`**.
4. **Account / PII:** `full_name`, `email_address`, and `phone_number` are not collected on the questionnaire; profile or account flows are out of WP3 scope.
5. **Integration test environment:** `backend/tests/integration/test_questionnaire_api.py` imports the full app stack; local runs require all app dependencies (e.g. `stripe`) to be installed or the test will not collect.

---

## Expanding the questionnaire later

New or restored questions may be added **only** through **governed changes** to `backend/ssot/questionnaire.json` (and the Automation Bus / SOP process for SSOT edits): update IDs, types, `importance`, `required`, and `conditionalDisplay` there first; then align mapper, validation, API tests, and frontend schema consumers as needed. No parallel “second questionnaire file” is introduced by WP3.

---

## Verification

From repo root (with backend dependencies installed):

`python -m pytest backend/tests/unit/test_questionnaire_models.py backend/tests/unit/test_questionnaire_mapper.py backend/tests/unit/test_scoring_overlays.py backend/tests/unit/test_orchestrator_medical_history_representation.py backend/tests/unit/test_context_hardening_contract.py backend/tests/integration/test_questionnaire_pipeline_integration.py backend/tests/integration/test_questionnaire_api.py backend/tests/regression/test_obs2_questionnaire_exercise_unknown_regression.py`
