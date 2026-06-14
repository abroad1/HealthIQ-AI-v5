# ARCH-COMPLETION-1 — Final Runtime Context and Orchestrator Restructure

---
work_id: ARCH-COMPLETION-1_final_runtime_context_and_orchestrator_restructure
branch: work/ARCH-COMPLETION-1-final-runtime-context-and-orchestrator-restructure
status: IMPLEMENTATION_COMPLETE
---

## Executive verdict

Orchestrator phase order corrected: `AnalysisContext` is now assembled before context-dependent signal evaluation. Runtime context passed to `SignalEvaluator` is derived via `build_runtime_context_snapshot_from_analysis_context()` from governed post-context fields. Raw `questionnaire_data` bridge before context assembly removed. All context-dependent Batch 2 packages remain inactive. Architecture validators pass.

---

## Previous orchestrator phase order

```text
unit_normalisation → quarantine → scoring_inputs → derived_markers
→ signal_evaluation (runtime_ctx from raw questionnaire_data)
→ create_analysis_context
→ scoring → clustering → ...
```

## New orchestrator phase order

```text
unit_normalisation → quarantine → scoring_inputs → derived_markers
→ create_analysis_context
→ build_runtime_context_snapshot_from_analysis_context(context)
→ signal_evaluation
→ scoring → clustering → ...
```

`PIPELINE_PHASE_ORDER` updated: `analysis_context` now precedes `signal_evaluation`.

---

## Files changed

- `backend/core/pipeline/orchestrator.py`
- `backend/core/pipeline/orchestrator_phases_v1.py`
- `backend/core/analytics/runtime_context_evaluator.py`
- `backend/tests/regression/test_context_threading.py`
- `docs/sprints/launch_core_carry_forward_register.md`

---

## Confirmations

- Raw questionnaire bridge before AnalysisContext removed from signal evaluation path
- SignalEvaluator interface unchanged (`runtime_context` kwarg)
- All 8 androgen packages remain inactive
- FT3 low remains inactive
- No package metadata changed
- No clinical thresholds / SSOT / scoring / report compiler / frontend changes

---

## Validator output

```
validation_status: PASS
errors: 0
index_path: C:\Users\abroa\HealthIQ-AI-v5\knowledge_bus\governance\medical_frame_identity_index_v1.yaml
validation_status: PASS
errors: 0
catalogue_path: C:\Users\abroa\HealthIQ-AI-v5\knowledge_bus\governance\context_modifier_catalogue_draft_v1.yaml
day_one_architecture_validation: PASS
medical_intelligence_architecture_validation: PASS
.......s..                                                               [100%]
=========================== short test summary info ===========================
SKIPPED [1] backend\tests\architecture\test_medical_intelligence_architecture_sentinels.py:67: full gate already executed by run_architecture_validation_gate.py
.....................                                                    [100%]
[architecture-gate] validate_medical_frame_identity_index
[architecture-gate] validate_context_modifier_catalogue
[architecture-gate] validate_day_one_architecture
[architecture-gate] validate_medical_intelligence_architecture
[architecture-gate] pytest_architecture_guardrails
[architecture-gate] pytest_governance_regression
architecture_validation_gate: PASS
day_one_architecture_validation: PASS
validation_status: PASS
errors: 0
index_path: C:\Users\abroa\HealthIQ-AI-v5\knowledge_bus\governance\medical_frame_identity_index_v1.yaml
validation_status: PASS
errors: 0
catalogue_path: C:\Users\abroa\HealthIQ-AI-v5\knowledge_bus\governance\context_modifier_catalogue_draft_v1.yaml
OK: no secret env files are git-tracked.
```

## Test output

```
.................................                                        [100%]
```

(33 tests: `test_context_threading.py`, `test_runtime_context_evaluation.py`, `test_orchestrator_unit_normalisation.py`)

---

## Carry-forward impact

`ARCH-ORCH-RESTRUCTURE-1`: **Resolved** — signal evaluation now receives runtime context derived from AnalysisContext.

---

## Rollback path

Revert orchestrator phase reorder, remove `build_runtime_context_snapshot_from_analysis_context`, restore `PIPELINE_PHASE_ORDER`, revert tests and carry-forward register.
