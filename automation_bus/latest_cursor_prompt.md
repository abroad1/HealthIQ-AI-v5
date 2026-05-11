---
work_id: WP3-QUESTIONNAIRE-RATIONALISATION
branch: wp3/questionnaire-rationalisation
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# WP3 — Questionnaire Rationalisation and Proving Readiness

## Objective

Rationalise the HealthIQ AI questionnaire so it supports practical human proving and improves the quality of personalised biomarker interpretation without forcing users through low-value, unused, duplicative, or poorly worded questions.

This is not just a temporary proving shortcut.

This work package must:

- keep the existing frontend multi-section questionnaire flow
- remove clearly low-value questions from the main questionnaire SSOT
- merge or simplify overlapping medical-history questions where safe
- preserve questions that materially improve interpretation
- introduce question importance/tier metadata
- ensure only mandatory questions block progress
- ensure skipped non-mandatory answers map to unknown, not false healthy/zero/moderate defaults
- preserve future extensibility so questions can be added back later through governed SSOT changes

## Authority documents

Read before implementation:

- `docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md`
- `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md`
  - especially questionnaire minimum proving-set notes
- `docs/planning-papers/healthiq_pre_sprint2_statin_gate_pack_FINAL.md`
- `docs/audit-papers/gate_compliance_audit_sprint3_readiness_second_pass.md`
- `docs/audit-papers/wp3_questionnaire_proving_readiness_audit.md`
- `docs/AUTOMATION_BUS_SOP_v1.3.1.md`

## Authority precedence note

`docs/audit-papers/wp3_questionnaire_proving_readiness_audit.md` is included as factual evidence only.

Its factual findings remain relevant, especially:

- field-by-field consumption map
- mapper default risks
- frontend/backend validation findings
- statin SSOT verification
- conditional validation issues

However, its original recommendation to preserve all questions in `questionnaire.json` and use only a profile-based reduction has been superseded by the product/architecture decision in this work package.

This WP3 prompt is the implementation authority.

Therefore, the audit’s §11 non-goals:

- “Do not remove any question from questionnaire.json”
- “Do not reduce the required flag on any existing SSOT field”

do not apply to this work package.

Cursor must follow this prompt’s explicit question disposition, removal list, tiering model, and validation requirements.

## Current baseline

The current questionnaire SSOT is:

`backend/ssot/questionnaire.json`

It currently contains 59 questions, many of which are required. The WP3 audit found that only a minority currently affect launch-core interpretation, while many are admin-only, captured-only, duplicative, or not clearly consumed downstream.

The frontend questionnaire already uses a multi-section wizard. Do not replace that flow.

## Strategic principle

A question earns its place only if it improves:

- biomarker interpretation
- report personalisation
- clinical/contextual safety
- user-specific explanation
- future governed analytical expansion

Do not keep questions merely because they already exist.

Do not remove useful questions merely to shorten the form.

Question changes are governed but not irreversible. Questions removed now may be reintroduced later through governed SSOT updates if a future analytical system, edge case, or report feature justifies them.

## Required architecture

Use one questionnaire SSOT.

Do not create a second questionnaire authority source.

Questionnaire changes must remain governed through:

`backend/ssot/questionnaire.json`

Each remaining question should have an importance/tier value.

Suggested field:

```json
"importance": "mandatory" | "recommended" | "optional" | "advanced"
````

If a different field name is already more consistent with repo conventions, use that, but do not create multiple competing concepts.

## Tier definitions

### mandatory

Required for the current personalised report.

User cannot proceed without answering, if the question is visible.

### recommended

Improves the report but is not essential.

User can skip it.

UI should label it clearly, for example:

`Improves your report`

### optional

Useful context but not essential.

User can skip it.

### advanced

Future or deeper module context.

Should not burden the core launch questionnaire. May be collapsed, hidden, or lower priority depending on current frontend capability.

## Questions to remove from the main questionnaire SSOT

Remove these questions unless implementation evidence proves a strong reason to retain one:

* `state_province`
* `body_composition`
* `overall_health_rating`
* `current_medications`
* `recent_blood_work`
* `energy_level`
* `current_symptoms`
* `diet_quality_rating`
* `sugar_beverages_weekly`
* `fruit_vegetable_servings`
* `sitting_hours_daily`
* `caffeine_beverages_daily`
* `pollution_exposure`
* `sleep_schedule_consistency`
* `stress_control_frequency`
* `major_life_stressors`
* `stress_management_method`
* `food_sensitivities`

Rationale:

These are currently low-value, vague, duplicative, admin-like, captured-only, or not sufficiently tied to current personalised biomarker interpretation to justify user effort.

If any of these are retained, Cursor must STOP and report the evidence-based reason before proceeding.

## Questions to move out of the health questionnaire

These should not remain part of the health interpretation questionnaire:

* `full_name`
* `email_address`
* `phone_number`

If still needed, they belong in account/profile/report-delivery flow, not the biomarker interpretation questionnaire.

Do not build that separate account/profile flow in this work package.

For now, remove them from the health questionnaire SSOT unless doing so breaks current frontend/API assumptions. If it does, STOP and report the dependency.

## Questions to keep

Keep and tier the following.

### mandatory

* `date_of_birth`
* `biological_sex`
* `height`
* `weight`
* `waist_circumference`
* `long_term_medications`
* `alcohol_drinks_weekly`
* `tobacco_use`
* `sleep_hours_nightly`

### recommended

* `blood_pressure_reading`
* `chronic_conditions`
* `medical_conditions`
* `regular_migraines`
* `recent_infections`
* `fasting_hours`
* `supplements`
* `dietary_pattern`
* `vigorous_exercise_days`
* `resistance_training_days`
* `sleep_quality_rating`
* `sleep_disorders`
* `stress_level_rating`
* `family_cardiovascular_disease`
* `family_diabetes_metabolic`

### optional or advanced

* `country`
* `ethnicity`
* `menstrual_hormonal_status`
* `low_testosterone_symptoms`
* `daily_fluid_intake`
* `balance_ability`
* `stair_climbing_ability`
* `push_up_capacity`
* `grip_strength_assessment`
* `physical_recovery_time`
* `memory_changes`
* `antibiotics_past_two_years`
* `family_cancer_history`
* `family_lifespan`

Use judgement from current frontend capability. If advanced questions cannot be hidden/collapsed safely in this work package, keep them visible but non-blocking and clearly labelled.

## Medical-history rationalisation

There is overlap between:

* `chronic_conditions`
* `medical_conditions`

Do not delete clinically useful condition options.

Preferred approach:

* keep both only if current mapper/tests depend on both
* otherwise merge into one clearer question or rationalise options safely
* preserve AF, RA, SLE because they are QRISK/cardio-relevant
* preserve diabetes, high blood pressure, high cholesterol, thyroid, liver, kidney, autoimmune where useful for future interpretation

If merging would require wider mapper changes than expected, keep both for now but mark only the most important one as recommended and make both skippable.

## Long-term medications

Keep:

* `long_term_medications`

It must include:

* `None`
* `Corticosteroids`
* `Atypical antipsychotics`
* `HIV/AIDS treatments`
* `Statins (cholesterol medication)`

Current evidence indicates `Statins (cholesterol medication)` may already be present in `questionnaire.json`.

Cursor must verify current SSOT state before editing:

* if present exactly once, make no change
* if missing, add it exactly once
* if duplicated, STOP and report

## Frontend requirements

Keep the current multi-section wizard.

Do not redesign the page flow.

Update the frontend so it can display tier labels, for example:

* Mandatory: `Required for your report`
* Recommended: `Improves your report`
* Optional: `Optional context`
* Advanced: `Advanced context`

Frontend validation should block only:

* visible questions with `importance: "mandatory"`

It should not block recommended, optional, or advanced questions.

Conditional questions must remain respected. Hidden conditional questions must not block progress.

## Backend validation requirements

Update backend validation so it does not require every historical `required: true` field after rationalisation.

Validation must align to the new importance model:

* mandatory visible/applicable questions are required
* non-mandatory questions are skippable
* conditional questions are not required when hidden/not applicable

If backend validation cannot determine visibility from `conditionalDisplay`, implement the minimal safe handling needed for existing conditional questions.

Do not let backend validation become noisy for normal launch-core submissions.

## Mapper safety requirements

Skipped non-mandatory answers must be treated as unknown, not:

* zero
* normal
* healthy
* moderate
* average

Specifically inspect and fix:

* alcohol absent behaviour
* exercise absent behaviour
* sleep absent behaviour
* stress absent behaviour

Known issue to address:

`alcohol_drinks_weekly` currently risks defaulting to a moderate value when absent. This must be changed so absent alcohol is unknown/None unless explicitly answered.

Preserve OBS-2 protection: missing exercise answers must not become zero exercise.

## Do not introduce fallback parsers

No fallback parser.

No dummy questionnaire parser.

No silent defaults that make absent lifestyle answers look normal, adverse, moderate, or healthy.

## Expected files touched

Expected:

* `backend/ssot/questionnaire.json`
* `backend/core/models/questionnaire.py`
* `backend/core/pipeline/questionnaire_mapper.py`
* `frontend/app/components/forms/QuestionnaireForm.tsx`
* `frontend/app/lib/questionnaireSchema.ts`
* relevant backend tests
* relevant frontend tests
* `docs/sprints/WP3_questionnaire_rationalisation_completion_2026-05.md`

Possibly expected, only if needed:

* backend questionnaire route/schema response files
* upload page integration if type changes require it

Not expected:

* Knowledge Bus files
* biomarker interpretation logic
* narrative compiler files
* Sentinel runner unless tests need promotion
* Automation Bus control-plane scripts
* report carriage UI
* Sprint 4 planning files

## Required tests

Add or update tests proving:

### SSOT integrity

* questionnaire JSON loads successfully
* removed question IDs are no longer present
* remaining questions have valid `importance`
* mandatory question list matches expected core set
* no duplicate question IDs
* `long_term_medications` contains statin option exactly once
* `sleep_schedule_consistency` is no longer present

### Frontend behaviour

* mandatory visible questions block progress
* recommended questions do not block progress
* optional questions do not block progress
* advanced questions do not block progress
* tier labels render correctly
* hidden conditional questions do not block progress
* existing section navigation still works

### Backend validation

* submission with only mandatory launch-core fields passes validation
* missing mandatory field fails validation
* skipped recommended/optional/advanced fields do not fail validation
* hidden conditional questions do not fail validation

### Mapper safety

* absent alcohol maps to unknown/None, not moderate
* absent exercise remains unknown/None, not zero
* statin-on still produces `user_intervention_document`
* statin-off / none produces no statin intervention document
* omitted optional fields do not crash mapper

### Regression

Run relevant existing questionnaire mapper tests.

Run relevant frontend questionnaire form tests.

Run any existing launch-core proving/profile tests if present.

## Stop conditions

STOP and report before implementation if:

* removing admin fields breaks upload submission or user identity assumptions
* removing any flagged question breaks mapper tests in a way that cannot be fixed locally
* current frontend cannot support `importance` without broad redesign
* backend validation cannot be made importance-aware without broad API redesign
* removing `current_medications` breaks medication context handling
* merging `chronic_conditions` and `medical_conditions` would require unsafe mapper restructuring
* adding tier metadata causes schema parsing failure
* skipped optional fields cause unsafe default assumptions that cannot be fixed within this work package
* any Knowledge Bus change appears necessary
* any biomarker interpretation logic change appears necessary
* any narrative compiler change appears necessary
* any Automation Bus control-plane script change appears necessary

## Explicit non-goals

Do not:

* build a new questionnaire UX
* create a second questionnaire SSOT
* create a user-facing profile chooser
* build account/profile/report-delivery flow
* change biomarker interpretation logic
* change narrative/report compiler logic
* change Knowledge Bus assets
* change blood-test parsing
* change Sentinel unless test promotion is explicitly required
* implement Sprint 4 report carriage
* implement proving harness CHECKs 2, 4, 5, 6
* add new advanced health modules

## Completion note

Create:

`docs/sprints/WP3_questionnaire_rationalisation_completion_2026-05.md`

It must record:

* questions removed
* questions retained
* final mandatory/recommended/optional/advanced counts
* why removals were justified
* how tiering works
* how skipped answers are treated
* tests run
* known limitations
* confirmation that the full questionnaire can still be expanded later through governed SSOT changes

## Validation commands

Inspect repo scripts and run appropriate targeted tests first.

At minimum, run:

* backend questionnaire/model tests
* backend questionnaire mapper tests
* frontend questionnaire form tests
* any relevant upload-page tests

Then run broader backend/frontend tests if feasible.

Report every command and result.

## Closure evidence required

Before finish, report:

* branch
* work_id
* files changed
* final question count
* final mandatory question count
* removed question IDs
* retained question IDs by tier
* whether statin option is present exactly once
* whether skipped alcohol is unknown/None
* whether skipped exercise remains unknown/None
* tests run and results
* confirmation no Knowledge Bus files changed
* confirmation no biomarker interpretation logic changed
* confirmation no narrative compiler files changed
* confirmation no Automation Bus control-plane scripts changed

## Final expected outcome

After WP3, the questionnaire should be shorter, clearer, and more honest.

Users should only be forced to answer questions that materially improve the current personalised report.

Additional questions should remain available only where they improve report quality or preserve future extensibility.

Future question changes remain possible through governed SSOT updates.

````
