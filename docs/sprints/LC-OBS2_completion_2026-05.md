# LC-OBS2 — questionnaire semantics investigation & closure (2026-05)

## Work package

- **work_id:** `LC-OBS2-QUESTIONNAIRE-SEMANTICS-INVESTIGATION`
- **Branch:** `feature/lc-obs2-questionnaire-semantics-investigation`

## Original observation (proving harness)

From launch-core proving outputs and prior completion notes (**OBS-2**): **AB** `consumer_domain_scores` **band labels** diverged between **baseline** (no `questionnaire_data`) and **statin_off** (payload `long_term_medications: ["None"]`) — second domain moved **stable → watch** without an intentional analytical difference.

## Approved semantic ruling (GPT)

- **No questionnaire answer** ≡ **unknown**, not a scored default.
- Absence of exercise answers must **not** be interpreted as **zero exercise**.
- **Baseline** and explicit **`"None"`** on medications-only payloads must **not** diverge solely because missing exercise fields were coerced to **`0`** and activated the lifestyle overlay.

## Root cause (confirmed in code review)

1. **Baseline:** `questionnaire_data` absent → orchestrator skips questionnaire mapping → no injected `lifestyle_factors` for scoring defaults path.
2. **Partial questionnaire:** `questionnaire_data` truthy → `map_submission` runs → `_map_exercise_minutes` returned **`0`** when neither `vigorous_exercise_days` nor `resistance_training_days` was present → **`exercise_minutes_per_week=0`** in context → exercise overlay **VERY_POOR** → metabolic/blood-sugar band penalty.

## Narrow fix implemented

- **`QuestionnaireMapper._map_exercise_minutes`:** returns **`None`** when **both** exercise keys are **absent** (unknown).
- **`MappedLifestyleFactors.exercise_minutes_per_week`:** **`Optional[int]`** (`None` = unknown).
- **`AnalysisOrchestrator`:** omits **`exercise_minutes_per_week`** from the **`lifestyle_factors`** dict when mapped value is **`None`**, so downstream **`get(..., 150)`** retains the neutral default (no false zero-exercise signal).

**Files:** `backend/core/pipeline/questionnaire_mapper.py`, `backend/core/pipeline/orchestrator.py`

## Classification (closure)

| Area | Paths |
|------|--------|
| Governance / prompt | `automation_bus/latest_cursor_prompt.md`, `automation_bus/latest_prompt_hardening.json` |
| Investigation / closure artefact | This note |
| Runtime bridge (narrow) | `questionnaire_mapper.py`, `orchestrator.py` |
| Regression tests | `backend/tests/unit/test_questionnaire_mapper.py`, `backend/tests/unit/test_lc_obs2_exercise_unknown_bridge.py` |

No changes to **`backend/tools/run_golden_panel.py`**, proving harness driver, or analytical scoring formulas beyond the questionnaire→context bridge above (**no tooling leakage** into unrelated automation).

## Verification

- Unit: mapper partial payloads (`long_term_medications` only) → exercise **unknown**; explicit exercise keys still map non-`None` totals.
- Integration: orchestrator **AB/VR** baseline vs statin_off **band alignment**; statin_off vs statin_on **invariants** preserved; **lifestyle_minimal** + partial questionnaire smoke.
- Baseline gate suite (`run_baseline_tests.py`) executed during kernel finish.

## Status

Targeted re-audit **passed**. OBS-2 closure recorded here; Stage 4A **finish** authorised after clean tree + kernel lifecycle.
