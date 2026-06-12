# CONTEXT-THREADING-1 — Runtime Context Orchestrator Threading

---
work_id: CONTEXT-THREADING-1_runtime_context_orchestrator_threading
branch: work/CONTEXT-THREADING-1-runtime-context-orchestrator-threading
status: IMPLEMENTATION_COMPLETE
---

## Executive verdict

Runtime context is now threaded from raw `questionnaire_data` into `SignalEvaluator.evaluate_all()` via `build_runtime_context_snapshot()` at orchestrator Step 1.6. This is an **interim bridge** — not final orchestrator architecture. No package activation. Active signals without `runtime_context_requirements` are unchanged.

---

## Files changed

```text
backend/core/pipeline/orchestrator.py
backend/core/pipeline/orchestrator_phases_v1.py
backend/tests/regression/test_context_threading.py
docs/audit-papers/CONTEXT-THREADING-1_runtime_context_orchestrator_threading.md
docs/sprints/launch_core_carry_forward_register.md
```

---

## Threading path

```text
questionnaire_data (AnalysisOrchestrator.run parameter)
→ build_runtime_context_snapshot(questionnaire_responses=questionnaire_data)
→ evaluate_signal_evaluation_phase(..., runtime_context=runtime_ctx)
→ SignalEvaluator.evaluate_all(..., runtime_context=runtime_ctx)
```

`create_analysis_context()` still runs at Step 2 (after signal evaluation). Mapped `lifestyle_factors` / `medical_history` are **not** used in this sprint.

---

## Package activation

None. FT3 low and all 8 androgen packages remain inactive in frame index.

---

## Confirmations

- No `signal_evaluator.py` / `runtime_context_evaluator.py` changes
- No package `signal_library.yaml` changes
- No clinical wording / thresholds / reference ranges changed
- No frontend / SSOT / scoring / report compiler changes

---

## Rollback path

Revert orchestrator.py and orchestrator_phases_v1.py threading changes; remove test file and audit/carry-forward updates.

---

## Residual architecture

Final day-one architecture still requires orchestrator phase reordering so context assembly precedes context-dependent evaluation. Recorded as **ARCH-ORCH-RESTRUCTURE-1** in carry-forward register.
