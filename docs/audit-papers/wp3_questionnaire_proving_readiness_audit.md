# WP3 Questionnaire Proving Readiness Audit

**Date:** 2026-05-10
**Auditor:** Claude Code — audit / investigation mode
**Work being prepared:** `WP3-LAUNCH-CORE-PROVING-QUESTIONNAIRE-SHARPENING`
**Evidence standard:** Every factual claim cites a file path and line number. Nothing assumed from memory or conversational summaries.
**Files modified by this audit:** None — docs only.

---

## 1. Executive Summary

The current questionnaire SSOT (`backend/ssot/questionnaire.json`) contains **59 questions**, 55 of which are marked `required: true`. This is confirmed as a blocker for Sprint 5 human proving in every prior authority document, most recently `gate_compliance_audit_sprint3_readiness_second_pass.md:37`.

Of the 59 questions, a **meaningful minority** currently affect launch-core analytical output. The majority are either admin/account fields, physical/cognitive assessment fields with no current downstream consumption, or secondary lifestyle fields whose mapper outputs are not verifiably consumed by the launch-core signal path.

The minimum field set to prove the launch-core personalisation pipeline on the AB/VR panels is approximately **9–13 fields**, depending on which QRISK-3 flags are included.

**Recommended architecture:** One SSOT, separate governed profile file (`backend/ssot/questionnaire_profiles.json`) referencing canonical question IDs — Option B. This preserves SSOT integrity, adds zero duplicate authority, and is the shape the Automation Bus governance can protect going forward.

**WP3 readiness verdict:**
- Architecture direction is clear and can be authored.
- Implementation touches `backend/ssot/` (HIGH risk per SOP).
- The statin questionnaire capture (adding `"Statins (cholesterol medication)"` to `long_term_medications`) was decided in the Pre-Sprint 2 Statin Gate Pack but not yet implemented — WP3 should carry this along with the profile mechanism.
- WP3 can be authored. The prompt must be classified `HIGH / MIXED`.

---

## 2. Current Questionnaire Inventory

**Source:** `backend/ssot/questionnaire.json` — read in full, 2026-05-10.

### 2.1 Question count

| Metric | Value |
|--------|-------|
| Total questions | **59** |
| `required: true` | **55** |
| `required: false` | **4** |

### 2.2 Optional fields (required: false)

| ID | Section | Notes |
|----|---------|-------|
| `state_province` | demographics | Admin field |
| `body_composition` | demographics | Body fat % / lean mass % — group type; no downstream consumption found |
| `blood_pressure_reading` | medical_history | Group type; consumed by `extract_objective_lifestyle_inputs` when provided |
| `supplements` | lifestyle | Checkbox; mapped to `MappedMedicalHistory.supplements` but not verifiably consumed downstream |

### 2.3 Sections and question counts

| Section | Count | Notes |
|---------|-------|-------|
| `demographics` | 15 | Includes full_name, email_address, phone_number, country, state_province, date_of_birth, biological_sex, height, weight, waist_circumference, body_composition, ethnicity, overall_health_rating, menstrual_hormonal_status, low_testosterone_symptoms |
| `medical_history` | 8 | blood_pressure_reading, current_medications, long_term_medications, chronic_conditions, medical_conditions, recent_blood_work, food_sensitivities, antibiotics_past_two_years |
| `symptoms` | 4 | energy_level, current_symptoms, regular_migraines, recent_infections |
| `lifestyle` | 22 | Full set of diet, exercise, alcohol, tobacco, sleep, stress questions |
| `physical_assessment` | 5 | balance_ability, stair_climbing_ability, push_up_capacity, grip_strength_assessment, physical_recovery_time |
| `cognitive_assessment` | 1 | memory_changes |
| `family_history` | 4 | family_cardiovascular_disease, family_diabetes_metabolic, family_cancer_history, family_lifespan |

### 2.4 Answer types

| Type | Count |
|------|-------|
| dropdown | 28 |
| checkbox | 9 |
| group | 4 |
| slider | 3 |
| text | 1 |
| email | 1 |
| phone | 1 |
| date | 1 |
| number | 1 |

### 2.5 Conditional display questions

Two questions have `conditionalDisplay` logic:
- `menstrual_hormonal_status` — shown only when `biological_sex == "Female"` (`questionnaire.json:222–226`)
- `low_testosterone_symptoms` — shown only when `biological_sex == "Male"` (`questionnaire.json:231–238`)

Both are currently `required: true`. In a proving mode, requiredness must respect conditional display — an absent sex-contextual question must not block submission.

The frontend enforces this correctly: `QuestionnaireForm.tsx:235` — `validateQuestion()` returns `undefined` if `!isQuestionVisible(question, responses)`, so the backend validator is the concern.

**Backend validation behaviour (confirmed at `backend/core/models/questionnaire.py:183–185`):** The `validate_submission` loop checks all questions with `required=True` against `submission.responses`. If a conditional question is not answered and not present in `responses`, it will raise a validation error regardless of the `conditionalDisplay` metadata in the JSON — because the validator does not parse `conditionalDisplay`.

This is a standing validation gap that WP3 must address in the proving profile design.

### 2.6 Burdensome fields for repeated testing

Fields that are high-burden for a human completing the form repeatedly:
- All **5 physical assessment** questions — require self-performed physical tests
- **3 sleep fields** beyond `sleep_hours_nightly` (sleep_quality_rating, sleep_schedule_consistency, sleep_disorders) — fine-grained but not clearly consumed
- **4 stress fields** beyond `stress_level_rating` (stress_control_frequency, major_life_stressors, stress_management_method) — partially consumed
- **fasting_hours** — captured only, not consumed
- **caffeine_beverages_daily** — maps to MappedLifestyleFactors.caffeine_consumption but not consumed in launch-core output
- **daily_fluid_intake** — maps to MappedLifestyleFactors.fluid_intake_liters but not consumed in launch-core output
- **pollution_exposure** — captured only
- **antibiotics_past_two_years** — captured only
- **3 family history questions** beyond cardiovascular/metabolic — cancer, lifespan not clearly consumed
- **Admin fields** (full_name, email_address, phone_number, country) — burden without analytical value

---

## 3. Field-by-Field Consumption Map

Classification codes:
- **A** — admin/account field only; no analytical consumption
- **B** — captured only; present in `questionnaire_responses` but no mapper consumption found
- **C** — mapped but downstream consumption unclear (in MappedLifestyleFactors/MappedMedicalHistory but not traceable to launch-core output)
- **D** — consumed by LifestyleModifierEngine or lifestyle bridge; visibly influences analytical output
- **E** — consumed by statin/QRISK/medication path
- **F** — demographic/context input that affects interpretation

**Evidence sources:** `backend/core/pipeline/questionnaire_mapper.py` (full read), `backend/core/pipeline/orchestrator.py` (grep), `backend/core/analytics/lifestyle_interpretation_bridge_engine.py` (grep), `backend/core/analytics/lifestyle_modifier_engine.py` (grep).

### Demographics section

| Field | Required | Classification | Evidence |
|-------|----------|---------------|---------|
| `full_name` | true | **A** | Not consumed in any mapper or analytics code |
| `email_address` | true | **A** | Not consumed in any mapper or analytics code |
| `phone_number` | true | **A** | Not consumed in any mapper or analytics code |
| `country` | true | **A** | Not consumed in any mapper or analytics code |
| `state_province` | false | **A** | Not consumed in any mapper or analytics code |
| `date_of_birth` | true | **F** | `orchestrator.py:1090` → age for fib_4; `questionnaire_mapper.py:614–627` → `demographics["age"]` |
| `biological_sex` | true | **F** | `questionnaire_mapper.py:629–634` → `demographics["gender"]`; gates menstrual/testosterone conditional questions |
| `height` | true | **F** | `questionnaire_mapper.py:637–648` → `demographics["height"]` → height_cm → BMI/WHR via lifestyle engine |
| `weight` | true | **F** | `questionnaire_mapper.py:650–660` → `demographics["weight"]` → weight_kg → BMI via lifestyle engine |
| `waist_circumference` | true | **D** | `questionnaire_mapper.py:514–528` → `waist_circumference_cm` → LifestyleModifierEngine (`lifestyle_registry.yaml:46`) |
| `body_composition` | false | **B** | Not consumed in mapper or analytics |
| `ethnicity` | true | **F** | `questionnaire_mapper.py:662–663` → `demographics["ethnicity"]`; may influence reference ranges (not confirmed in launch-core path) |
| `overall_health_rating` | true | **B** | Not consumed in any mapper or analytics code |
| `menstrual_hormonal_status` | true | **B** | Not consumed downstream; conditional on biological_sex=Female |
| `low_testosterone_symptoms` | true | **B** | Not consumed downstream; conditional on biological_sex=Male |

### Medical history section

| Field | Required | Classification | Evidence |
|-------|----------|---------------|---------|
| `blood_pressure_reading` | false | **D** | `questionnaire_mapper.py:530–548` → `systolic_bp`, `diastolic_bp` → LifestyleModifierEngine (`lifestyle_registry.yaml:48–53`) |
| `current_medications` | true | **C** | `questionnaire_mapper.py:186–187` → `MappedMedicalHistory.medications` (coarse band, not drug identities) |
| `long_term_medications` | true | **D/E** | `questionnaire_mapper.py:204–207` → `long_term_medication_classes`; `questionnaire_mapper.py:221–224` → QRISK flags; `questionnaire_mapper.py:71–107` → `user_intervention_document` (statin path) |
| `chronic_conditions` | true | **C** | `questionnaire_mapper.py:183` → `MappedMedicalHistory.conditions`; downstream consumption not traced in launch-core signal path |
| `medical_conditions` | true | **E** | `questionnaire_mapper.py:218–220` → QRISK booleans (AF, RA, SLE) passed to context |
| `recent_blood_work` | true | **B** | Not consumed in any mapper or analytics code |
| `food_sensitivities` | true | **C** | `questionnaire_mapper.py:214–215` → `MappedMedicalHistory.allergies`; not consumed in launch-core signal path |
| `antibiotics_past_two_years` | true | **B** | Not consumed in any mapper or analytics code |

### Symptoms section

| Field | Required | Classification | Evidence |
|-------|----------|---------------|---------|
| `energy_level` | true | **B** | Not consumed in any mapper or analytics code |
| `current_symptoms` | true | **B** | Not consumed in any mapper or analytics code |
| `regular_migraines` | true | **E** | `questionnaire_mapper.py:224` → `migraines` QRISK boolean |
| `recent_infections` | true | **B** | Not consumed in any mapper or analytics code |

### Lifestyle section

| Field | Required | Classification | Evidence |
|-------|----------|---------------|---------|
| `diet_quality_rating` | true | **B** | Not consumed by `map_submission`, `extract_objective_lifestyle_inputs`, or `extract_behavioural_lifestyle_inputs` |
| `fasting_hours` | true | **B** | Not consumed in any mapper or analytics code |
| `sugar_beverages_weekly` | true | **C** | `questionnaire_mapper.py:274–283` → `diet_level` score; downstream consumption of `diet_level` not traced |
| `alcohol_drinks_weekly` | true | **D** | `questionnaire_mapper.py:572–585` → `alcohol_units_per_week` → LifestyleModifierEngine + one-carbon bridge (`lifestyle_interpretation_bridge_engine.py:64`) |
| `fruit_vegetable_servings` | true | **C** | `questionnaire_mapper.py:262–271` → `diet_level` score |
| `supplements` | false | **C** | `questionnaire_mapper.py:201` → `MappedMedicalHistory.supplements`; not consumed in launch-core signal path |
| `dietary_pattern` | true | **C** | `questionnaire_mapper.py:249–259` → `diet_level` score |
| `vigorous_exercise_days` | true | **C** | `questionnaire_mapper.py:327–330` → `exercise_minutes_per_week`; not confirmed consumed in launch-core signal path |
| `sitting_hours_daily` | true | **C** | `questionnaire_mapper.py:448–460` → `sedentary_hours_per_day`; not confirmed consumed |
| `resistance_training_days` | true | **C** | `questionnaire_mapper.py:337–346` → `exercise_minutes_per_week` |
| `tobacco_use` | true | **D** | `questionnaire_mapper.py:587–597` → `smoking_status` → LifestyleModifierEngine (`lifestyle_registry.yaml:58–60`) |
| `caffeine_beverages_daily` | true | **C** | `questionnaire_mapper.py:462–476` → `caffeine_consumption`; not consumed in launch-core signal path |
| `daily_fluid_intake` | true | **C** | `questionnaire_mapper.py:479–490` → `fluid_intake_liters`; not consumed in launch-core signal path |
| `pollution_exposure` | true | **B** | Not consumed in any mapper or analytics code |
| `sleep_hours_nightly` | true | **D** | `questionnaire_mapper.py:562–571` → `sleep_hours` → LifestyleModifierEngine (`lifestyle_registry.yaml:64–66`) |
| `sleep_quality_rating` | true | **B** | Not consumed by any extract_* function; mapped lifestyle factors |
| `sleep_schedule_consistency` | true | **B** | Not consumed in any mapper or analytics code |
| `sleep_disorders` | true | **C** | `questionnaire_mapper.py:210–211` → `MappedMedicalHistory.sleep_disorders`; not consumed in launch-core signal path |
| `stress_level_rating` | true | **C** | `questionnaire_mapper.py:396–408` → `stress_level`; not confirmed consumed in launch-core signal path |
| `stress_control_frequency` | true | **C** | `questionnaire_mapper.py:411–419` → `stress_level` contribution |
| `major_life_stressors` | true | **C** | `questionnaire_mapper.py:422–430` → `stress_level` contribution |
| `stress_management_method` | true | **B** | Not consumed in any mapper or analytics code |

### Physical assessment section

| Field | Required | Classification | Evidence |
|-------|----------|---------------|---------|
| `balance_ability` | true | **B** | Not consumed in any mapper or analytics code |
| `stair_climbing_ability` | true | **B** | Not consumed in any mapper or analytics code |
| `push_up_capacity` | true | **B** | Not consumed in any mapper or analytics code |
| `grip_strength_assessment` | true | **B** | Not consumed in any mapper or analytics code |
| `physical_recovery_time` | true | **B** | Not consumed in any mapper or analytics code |

### Cognitive assessment section

| Field | Required | Classification | Evidence |
|-------|----------|---------------|---------|
| `memory_changes` | true | **B** | Not consumed in any mapper or analytics code |

### Family history section

| Field | Required | Classification | Evidence |
|-------|----------|---------------|---------|
| `family_cardiovascular_disease` | true | **C** | `questionnaire_mapper.py:191` → `MappedMedicalHistory.family_history`; not confirmed consumed in launch-core signal path |
| `family_diabetes_metabolic` | true | **C** | `questionnaire_mapper.py:193` → `family_history` |
| `family_cancer_history` | true | **C** | `questionnaire_mapper.py:195` → `family_history` |
| `family_lifespan` | true | **C** | `questionnaire_mapper.py:197` → `family_history` |

### Consumption summary

| Classification | Count | Description |
|---------------|-------|-------------|
| A — admin only | 5 | full_name, email_address, phone_number, country, state_province |
| B — captured only | 20 | No mapper or analytical consumption found |
| C — mapped, downstream unclear | 17 | In MappedLifestyleFactors/MappedMedicalHistory but not traced to launch-core output |
| D — actively consumed, analytical output | 7 | waist_circumference, blood_pressure_reading, alcohol_drinks_weekly, tobacco_use, sleep_hours_nightly, height, weight |
| E — QRISK/medication path | 3 | long_term_medications, medical_conditions, regular_migraines |
| F — demographic context | 3 | date_of_birth, biological_sex, ethnicity |

**Key finding:** Only 7 fields (D) verifiably influence launch-core analytical output via the LifestyleModifierEngine or interpretation bridge. 3 more (E) are consumed by QRISK/statin paths. 3 (F) provide demographic context. The remaining 46 are either admin, captured only, or mapped to data structures without confirmed launch-core signal consumption.

---

## 4. Launch-Core Proving Field Recommendation

### 4.1 Must include — directly affects analytical output

| Field ID | Reason |
|----------|--------|
| `date_of_birth` | Age computation (fib_4, context) |
| `biological_sex` | Gender-specific thresholds; gates conditional questions |
| `height` | BMI/WHR derivation |
| `weight` | BMI derivation |
| `waist_circumference` | WHR derivation; cardiovascular lifestyle modifier |
| `alcohol_drinks_weekly` | LifestyleModifierEngine + one-carbon methylation bridge |
| `tobacco_use` | LifestyleModifierEngine smoking modifier |
| `sleep_hours_nightly` | LifestyleModifierEngine sleep modifier |
| `long_term_medications` | Statin path (CHECK 3/S-5); QRISK corticosteroids/antipsychotics/HIV flags |

### 4.2 Include if wired and low burden

| Field ID | Reason |
|----------|--------|
| `blood_pressure_reading` | Already optional; consumed by LifestyleModifierEngine when provided; directly relevant to cardiovascular proving |
| `medical_conditions` | QRISK-3 flags (AF, RA, SLE) — consumed, low effort (checkbox) |
| `regular_migraines` | QRISK-3 migraine flag — single dropdown, consumed |
| `chronic_conditions` | Mapped; relevant to clinician context; low effort |

### 4.3 Include for stressed profile only (preserve for future, optional for baseline)

| Field ID | Reason |
|----------|--------|
| `stress_level_rating` | Slider; consumed by stress_level mapping; relevant to stressed profile |
| `vigorous_exercise_days` | Exercise mapping; low burden if already present |
| `dietary_pattern` | Diet level; low burden dropdown |

### 4.4 Preserve in SSOT, exclude from proving profile (no current analytical value)

All **B-classified** fields (20 questions), all **physical assessment** questions (5), `cognitive_assessment` (1), `family_history` (4), and admin fields (5) should be excluded from the proving profile. These total **35 questions** that add burden without affecting the launch-core proving checks.

Also exclude from proving profile:
- `diet_quality_rating` (B — not consumed despite being in lifestyle section)
- `fasting_hours` (B)
- `sleep_quality_rating` (B)
- `sleep_schedule_consistency` (B)
- `sleep_disorders` (C — mapped but no confirmed launch-core consumption)
- `caffeine_beverages_daily` (C)
- `daily_fluid_intake` (C)
- `pollution_exposure` (B)
- `stress_management_method` (B)
- `stress_control_frequency` (C — secondary to stress_level_rating)
- `major_life_stressors` (C — secondary to stress_level_rating)
- `antibiotics_past_two_years` (B)
- `recent_blood_work` (B)
- `overall_health_rating` (B)
- `energy_level` (B)
- `current_symptoms` (B)
- `recent_infections` (B)
- `food_sensitivities` (C)
- `current_medications` (C — coarse band, not analytically used)
- `supplements` (C)
- `family_cardiovascular_disease`, `family_diabetes_metabolic`, `family_cancer_history`, `family_lifespan` (C — mapped, not confirmed launch-core consumption)
- `sugar_beverages_weekly`, `fruit_vegetable_servings` (C — diet level score)
- `sitting_hours_daily`, `resistance_training_days` (C — exercise/sedentary)
- `menstrual_hormonal_status`, `low_testosterone_symptoms` (B — conditional, captured only)
- `ethnicity` (F — mapped but reference range effect not confirmed in launch-core)

---

## 5. Recommended Profile/Mode Architecture

### Option A — Per-question visibility metadata in questionnaire.json

**Assessment:**
- SSOT integrity: Acceptable — single file, but adds profile metadata to question objects
- Risk of duplicate authority: Low
- Ease of testing: Moderate — profile logic inside SSOT
- Frontend impact: Moderate — form renderer must parse profile metadata
- Mapper compatibility: Requires mapper to be profile-aware
- Future scalability: Poor — adding new profiles requires editing every question's metadata
- SOP risk: CONTENT change to `backend/ssot/` → HIGH per SOP trigger list
- **Verdict: Not recommended.** Tight coupling between SSOT question definitions and profile management.

### Option B — Separate profile file referencing SSOT question IDs

**Assessment:**
- SSOT integrity: Strong — `questionnaire.json` is untouched; profile file contains only question ID references and profile names
- Risk of duplicate authority: None — zero duplication of question text or options
- Ease of testing: High — profile validity is testable as a whitelist check against SSOT IDs
- Frontend impact: Low — frontend queries backend for profile-filtered question list
- Mapper compatibility: Mapper handles partial submissions safely already (OBS-2 protection at `questionnaire_mapper.py:318–321`)
- Future scalability: High — new profiles are additive lines in the profile file
- SOP risk: New file in `backend/ssot/` — HIGH per SOP trigger list, but CONTENT change_type (no executable code)
- **Verdict: Recommended.**

### Option C — Frontend-only filter

**Assessment:**
- SSOT integrity: Strong — SSOT unchanged
- Risk of duplicate authority: None
- Ease of testing: Weak — requires browser/E2E testing; backend validation still enforces all required fields, causing submission failure
- Frontend impact: Low for UI rendering; HIGH for validation mismatch
- Mapper compatibility: Backend validation rejects partial submissions
- Future scalability: Poor — profile logic in frontend only, invisible to backend tests
- SOP risk: Frontend-only change, but backend validation gap creates a correctness problem
- **Verdict: Not recommended.** Backend validation would reject a launch-core proving submission that omits 40+ required fields. This cannot work without backend validation changes — which takes it back to Option B territory anyway.

### Recommended architecture

**One SSOT, separate governed profile file referencing canonical question IDs.**

Schema for `backend/ssot/questionnaire_profiles.json`:

```json
{
  "schema_version": "1.0.0",
  "profiles": {
    "launch_core_proving": {
      "description": "Minimum proving set for launch-core personalisation testing",
      "required_question_ids": [
        "date_of_birth",
        "biological_sex",
        "height",
        "weight",
        "waist_circumference",
        "alcohol_drinks_weekly",
        "tobacco_use",
        "sleep_hours_nightly",
        "long_term_medications"
      ],
      "optional_question_ids": [
        "blood_pressure_reading",
        "medical_conditions",
        "regular_migraines",
        "chronic_conditions",
        "stress_level_rating",
        "vigorous_exercise_days",
        "dietary_pattern"
      ]
    },
    "full": {
      "description": "Full questionnaire — all SSOT questions",
      "required_question_ids": null,
      "optional_question_ids": null
    }
  }
}
```

**Rule:** `required_question_ids: null` means use the SSOT `required` flags directly. This prevents the profile file from becoming a second required-fields authority. Only `launch_core_proving` specifies an explicit override.

---

## 6. Requiredness and Validation Findings

### 6.1 Where requiredness is enforced

**Backend validation** (`backend/core/models/questionnaire.py:183–185`):
```python
for question in self.schema.questions:
    if question.required and question.id not in submission.responses:
        errors.append(f"Required question {question.id} is missing")
```
This iterates all SSOT questions with `required=True`. There are 55 such questions. A proving-mode submission with only 9–13 fields will trigger ~42–46 validation errors. The orchestrator currently prints warnings and continues (`orchestrator.py:284–285`), so pipeline execution is not blocked, but errors are logged.

**Frontend validation** (`QuestionnaireForm.tsx:234–239`):
The frontend's `validateQuestion()` skips hidden conditional questions (`isQuestionVisible` check at line 235). It validates required fields per section during the guided flow. A profile-aware frontend would skip non-profile questions.

### 6.2 Whether proving mode can make non-core fields optional

Yes — the backend validator reads `question.required` from the schema. The proving profile mechanism can be implemented by:
1. A profile-aware schema endpoint that returns the SSOT but with `required` overridden for non-proving-profile questions
2. Or a profile-aware validator that skips required checks for question IDs not in the proving profile

Neither requires modifying `questionnaire.json`.

### 6.3 Effect on mapper assumptions

The mapper handles partial submissions safely via Python's `dict.get()` pattern throughout. The OBS-2 protection (`questionnaire_mapper.py:318–321`) confirms the exercise-unknown case is explicitly handled. Absent fields produce default values or `None`, not errors.

**Verified safe defaults on empty submission** (`test_questionnaire_mapper.py:395–419`): Empty `{}` submission produces `AVERAGE` diet, `7.0` sleep hours, `None` exercise, `5` alcohol units, `"never"` smoking, `AVERAGE` stress, and empty medical history lists.

**Risk:** The `5` alcohol units default on empty submission (line 369 in mapper: `return 5  # Default moderate`) is a false positive if alcohol question is absent. In a proving profile, alcohol is a required field, so this risk is contained. But if the proving profile were to make alcohol optional and it is absent, the default would silently apply a "moderate" alcohol value that could activate the one-carbon bridge incorrectly. This is the OBS-2 equivalent for alcohol — and must be addressed in WP3.

### 6.4 OBS-2 unknown-vs-zero protection relevance

**Exercise (confirmed protected):** `questionnaire_mapper.py:318–321` — when neither `vigorous_exercise_days` nor `resistance_training_days` is present, `exercise_minutes_per_week` returns `None`, not `0`. This prevents false VERY_POOR exercise overlay.

**Alcohol (not protected, confirmed):** `questionnaire_mapper.py:368–369` — if `alcohol_drinks_weekly` is absent AND `alcohol_consumption` is absent, falls through to `return 5`. A proving submission that makes alcohol optional would need to explicitly set `0` or the mapper must be updated to return `None` when absent.

**Recommendation:** If WP3 makes any currently-consumed field optional in the proving profile, the mapper must be audited to ensure absent = `None` not a false default. Alcohol is the highest-risk case. Sleep (`return 7.0` default at line 309) is lower risk.

---

## 7. Human Proving Profile Presets

### Preset 1 — Baseline healthy

Minimum fields showing a plausible healthy profile for the AB/VR panels.

| Field | Value |
|-------|-------|
| `date_of_birth` | 1985-01-01 (age ~40) |
| `biological_sex` | Male |
| `height` | `{"Feet": 5, "Inches": 10}` |
| `weight` | `{"Weight (lbs)": 165}` |
| `waist_circumference` | 32 (inches) |
| `alcohol_drinks_weekly` | None |
| `tobacco_use` | Never used |
| `sleep_hours_nightly` | 7-8 hours |
| `long_term_medications` | None |

**Expected result:** Lifestyle modifiers fire neutral/positive. Statin annotation absent. No alcohol bridge activation.

### Preset 2 — Stressed lifestyle

Uses the same biomarkers as Preset 1 but stressed lifestyle inputs — designed to activate CHECK 1 and CHECK 2 (alcohol bridge in lead_narrative).

| Field | Value |
|-------|-------|
| `date_of_birth` | 1985-01-01 |
| `biological_sex` | Male |
| `height` | `{"Feet": 5, "Inches": 10}` |
| `weight` | `{"Weight (lbs)": 210}` |
| `waist_circumference` | 40 (inches → BMI ~30, high WHR) |
| `blood_pressure_reading` | `{"Systolic (mmHg)": 158, "Diastolic (mmHg)": 96}` |
| `alcohol_drinks_weekly` | 8-14 drinks (→ 11 units/week) |
| `tobacco_use` | Daily use |
| `sleep_hours_nightly` | Less than 5 hours |
| `long_term_medications` | None |

**Expected result:** Cardiovascular lifestyle modifiers fire negative. Alcohol bridge activates (alcohol_units_per_week ≥ threshold). Pre-Sprint 1 CHECK 1 (lifestyle visible payoff vs baseline) should be satisfied.

### Preset 3 — Statin-off baseline

Identical to Preset 1 with explicit None for medications. Required for the statin comparison CHECK 3/S-5.

| Field | Same as Preset 1 except | `long_term_medications: ["None"]` |

### Preset 4 — Statin-on

Identical to Preset 3 but with statin selection. Required for CHECK S-5.

| Field | Same as Preset 3 except | `long_term_medications: ["Statins (cholesterol medication)"]` |

**Expected result:** `intervention_annotations_v1` non-null. At least one consumer-visible field in `consumer_domain_scores`, `lead_narrative`, or `clinician_report_v1.sections.page1` differs from Preset 3.

**Field count per preset:** 9 required fields (plus optional `blood_pressure_reading` in Preset 2). Against the current 55 required fields, this represents an 84% form reduction.

---

## 8. Test Impact / Required Tests

### 8.1 Existing tests that protect questionnaire mapping

| Test file | Coverage |
|-----------|---------|
| `backend/tests/unit/test_questionnaire_mapper.py` | Full mapper coverage: diet, sleep, exercise, alcohol, smoking, stress, sedentary, caffeine, fluid, medical history, QRISK flags, OBS-2 exercise unknown, extract_objective_lifestyle_inputs, extract_behavioural_lifestyle_inputs |

### 8.2 Required tests for WP3

| Test | Type | Purpose |
|------|------|---------|
| `test_proving_profile_contains_all_required_ids` | Unit | Verify the `launch_core_proving` profile includes all 9 core IDs |
| `test_proving_profile_ids_are_valid_ssot_question_ids` | Unit | Every ID in the profile references an existing SSOT question — no orphaned IDs |
| `test_full_profile_returns_all_ssot_questions` | Unit | `full` profile produces same question list as raw SSOT |
| `test_proving_submission_validates_without_non_core_fields` | Unit | A submission with only 9 core fields passes backend validation when `launch_core_proving` profile is active |
| `test_proving_submission_rejects_if_core_field_missing` | Unit | A submission missing a required core field fails validation |
| `test_mapper_handles_proving_partial_submission_safely` | Unit | Proving-size submission produces `None` (not false defaults) for absent optional fields. Specifically: exercise_minutes_per_week is `None` when exercise fields absent (OBS-2 already covered); verify alcohol returns `None` or `0` explicitly when absent |
| `test_statin_on_proves_intervention_document` | Unit | Statin-on submission via mapper produces valid `user_intervention_document` with `lipid_lowering_statin` |
| `test_statin_off_produces_no_intervention_document` | Unit | `None` long_term_medications or `["None"]` produces `None` from `build_user_intervention_document_for_statin` |
| `test_full_questionnaire_ssot_unchanged` | Unit | Snapshot/hash test asserting `questionnaire.json` question count and required-field count unchanged by WP3 |
| `test_conditional_question_not_required_in_proving_mode` | Unit | `menstrual_hormonal_status` and `low_testosterone_symptoms` do not cause validation failure when absent in proving-profile submission |

---

## 9. Risk Classification

### 9.1 Files likely touched by WP3

| File | SOP classification trigger | Risk level |
|------|---------------------------|------------|
| `backend/ssot/questionnaire.json` | `backend/ssot/` in HIGH trigger list | HIGH |
| `backend/ssot/questionnaire_profiles.json` (new) | New file in `backend/ssot/` | HIGH (precautionary — no existing content, pure new SSOT file) |
| `backend/core/pipeline/questionnaire_mapper.py` | Not in HIGH trigger list directly; touches analytical pipeline indirectly | STANDARD unless output changes |
| `backend/core/models/questionnaire.py` | Validation logic; affects pipeline input gate | STANDARD |
| Frontend questionnaire form | Frontend only | LOW |
| Backend API endpoint for questionnaire schema | Routing/API | LOW |
| Tests | Test additions only | LOW |

### 9.2 Classification analysis

**`questionnaire.json` change:** Adding `"Statins (cholesterol medication)"` to `long_term_medications` options is CONTENT (SSOT data addition). However, the file is in `backend/ssot/` so HIGH risk applies per SOP regardless.

**Profile file creation:** New SSOT file; no modification to existing analytical logic. CONTENT change_type by SOP §4 definition — "SSOT updates, YAML modifications, knowledge expansion, non-executable data." But `backend/ssot/` triggers HIGH regardless.

**Validation change:** If the validator is extended to be profile-aware, this changes pipeline input gate behaviour. This is BEHAVIOUR-adjacent — it determines what data enters the analytical pipeline. MIXED classification would apply.

**Overall WP3 classification:** `HIGH / MIXED` — minimum classification justified by `backend/ssot/` path trigger plus the validation behaviour change.

Dual-approval requirement applies: Claude audit + GPT architectural review before merge.

---

## 10. Recommended WP3 Implementation Scope

### 10.1 Profile architecture

Create `backend/ssot/questionnaire_profiles.json` with:
- `launch_core_proving` profile: 9 required IDs + 7 optional IDs (see §5)
- `full` profile: null (delegate to SSOT)

This file must not duplicate question text, options, or type definitions from `questionnaire.json`.

### 10.2 Core launch-proving question set

9 required fields (see §4.1). `blood_pressure_reading` included as optional (already optional in SSOT). Conditional questions (`menstrual_hormonal_status`, `low_testosterone_symptoms`) excluded from proving profile; their validation must be silenced when profile is active.

### 10.3 How the full questionnaire is preserved

`questionnaire.json` must not be reduced or modified except to add `"Statins (cholesterol medication)"` to `long_term_medications` options (already decided at Pre-Sprint 2 Statin Gate Pack §4.1, 2026-05-09). The profile mechanism is a separate reference layer; the SSOT remains authoritative and complete.

### 10.4 Validation and requiredness handling

A profile-aware API endpoint should exist:
- `GET /api/questionnaire/schema?profile=launch_core_proving` — returns SSOT questions filtered to profile IDs, with `required` flags adjusted per profile
- The backend validator must accept a profile ID that whitelists required fields for that profile
- Absent optional fields in a proving submission must not generate validation errors

The validator already warns and continues on errors (`orchestrator.py:283–285`), so the pipeline is not blocked. But the warning noise should be eliminated for clean proving runs.

### 10.5 Frontend/backend changes likely required

**Backend:**
- `backend/ssot/questionnaire_profiles.json` — new file
- `backend/core/models/questionnaire.py` — profile-aware `validate_submission()` (accepts optional `profile_id: str` parameter)
- `backend/core/pipeline/questionnaire_mapper.py` — alcohol absent-vs-zero protection (ensure `None` not `5` default when field absent in proving submission)
- API endpoint for schema with profile parameter

**Frontend:**
- `QuestionnaireForm.tsx` — render only profile-included questions when profile is active
- Profile selection mechanism (simplest: a constant set in the proving config, not a user-visible choice)

### 10.6 Test plan

See §8.2 for the complete required test list (10 tests).

### 10.7 Explicit non-goals

See §11.

---

## 11. Non-Goals

- Do not remove any question from `questionnaire.json`
- Do not reduce the `required` flag on any existing SSOT field
- Do not create a second questionnaire authority source (no duplication of question text or options)
- Do not author a full questionnaire UX redesign (Q-1/Q-2 programmes are separate)
- Do not expand questionnaire scope with new questions beyond the statin option
- Do not introduce fallback parsers or dummy data generators
- Do not implement Sprint 5 proving harness CHECK encoding (pre-Sprint 5 scope)
- Do not build a user-facing profile chooser; the profile should be an implementation/config concern
- Do not change any of the 9 core field mappings in `questionnaire_mapper.py` (except the alcohol absent→None protection)
- Do not modify `backend/ssot/biomarkers.yaml`, `lifestyle_registry.yaml`, or any Knowledge Bus asset

---

## 12. Open Questions / Blockers

### 12.1 Alcohol default on absent field — requires a decision

`questionnaire_mapper.py:368–369`: when `alcohol_drinks_weekly` is absent, the mapper returns `5` (moderate). If alcohol is a required proving field, this never fires. But the mapper should be made explicit about this: if alcohol is absent it should return `None` (like exercise), not a false moderate default.

**Decision required:** Should the mapper be changed to return `None` for alcohol when absent? This is an OBS-2 style issue. The recommended answer is yes — align with the exercise OBS-2 protection.

### 12.2 Statin option in questionnaire.json — confirmed not yet implemented

The Pre-Sprint 2 Statin Gate Pack §4.1 (2026-05-09) decided to add `"Statins (cholesterol medication)"` to `long_term_medications` options. The statin gate pack §5 records `"Statin capture path exists in questionnaire: DOES NOT EXIST"`.

WP3 should carry this addition. The mapper `build_user_intervention_document_for_statin()` already references `STATINS_LONG_TERM_MEDICATION_LABEL = "Statins (cholesterol medication)"` at `questionnaire_mapper.py:16` — so the mapper is ready, the SSOT option just needs to be added.

This is a confirmed gate item from the Pre-Sprint 2 gate (CHECK S-1) and is a WP3 prerequisite blocker.

### 12.3 Conditional question validation in proving profile

`menstrual_hormonal_status` and `low_testosterone_symptoms` are both `required: true` in the SSOT but only meaningful based on `biological_sex`. The backend validator does not currently parse `conditionalDisplay` metadata. A profile-aware validator needs to handle this, otherwise same-sex proving runs will fail validation.

### 12.4 QRISK flags in proving profile — include or exclude?

`medical_conditions` (AF, RA, SLE flags) and `regular_migraines` are consumed by QRISK logic. Their inclusion in the proving profile adds minimal burden (single checkbox/dropdown) but provides more accurate cardiovascular context.

**Recommendation:** Include them in the proving profile optional set. They do not block proving if absent and their presence improves analytical fidelity.

---

## 13. Files Inspected

| File | Read extent |
|------|-------------|
| `docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md` | Full read |
| `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md` | Full read |
| `docs/planning-papers/healthiq_pre_sprint2_statin_gate_pack_FINAL.md` | Full read |
| `docs/audit-papers/gate_compliance_audit_sprint3_readiness_second_pass.md` | Full read |
| `backend/ssot/questionnaire.json` | Full read — 59 questions catalogued |
| `backend/ssot/lifestyle_registry.yaml` | Full read (100 lines) |
| `backend/core/pipeline/questionnaire_mapper.py` | Full read (682 lines) |
| `backend/core/models/questionnaire.py` | Grep — required/validation logic |
| `backend/core/pipeline/orchestrator.py` | Grep — questionnaire-related consumption |
| `backend/core/analytics/lifestyle_modifier_engine.py` | Grep — input keys consumed |
| `backend/core/analytics/lifestyle_interpretation_bridge_engine.py` | Grep — questionnaire field consumption |
| `backend/tests/unit/test_questionnaire_mapper.py` | Full read (533 lines) |
| `frontend/app/lib/questionnaireSchema.ts` | Partial read — interface + required |
| `frontend/app/components/forms/QuestionnaireForm.tsx` | Grep — required/validation |

**Non-document files modified:** None.

---

## Summary — Answers to Final Report Questions

| Question | Answer |
|----------|--------|
| Files read | 15 files — see §13 |
| File created | `docs/audit-papers/wp3_questionnaire_proving_readiness_audit.md` |
| Non-doc files modified | None |
| Recommended profile architecture | Option B — `backend/ssot/questionnaire_profiles.json` referencing SSOT question IDs; no duplication |
| Recommended launch-core proving field count | **9 required fields** (+ up to 7 optional); against 55 currently required — 84% reduction |
| WP3 ready to author | **Yes.** Architecture is clear. Risk: `HIGH / MIXED`. Blockers to record in prompt: (1) statin SSOT option must be added (CHECK S-1 from statin gate); (2) alcohol absent-vs-zero mapper protection decision; (3) conditional question validation handling. |
