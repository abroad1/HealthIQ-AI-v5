# R-8 — WHY coverage expansion, Wave 1

**Work package:** R-8  
**Branch:** `feature/why-coverage-expansion-wave-1`

## Added signal IDs (governed WHY)

| Signal ID | Hypothesis asset |
|-----------|------------------|
| `signal_total_cholesterol_high` | `knowledge_bus/root_cause/hypotheses/total_cholesterol_high_hypotheses_v1.yaml` |
| `signal_vitamin_d_low` | `knowledge_bus/root_cause/hypotheses/vitamin_d_low_hypotheses_v1.yaml` |

## Compiler wiring

- `backend/core/knowledge/load_root_cause_hypotheses.py` — `load_total_cholesterol_high_hypotheses_v1`, `load_vitamin_d_low_hypotheses_v1`
- `backend/core/analytics/root_cause_compiler_v1.py` — `_ROOT_CAUSE_TARGETS` entries for both signals

## Confirmatory registry

- **Total cholesterol:** uses existing `confirmatory_tests_v1` IDs (`test_hba1c_repeat_v1`, `test_thyroid_tsh_ft4_v1`, `test_fasting_glucose_insulin_context_v1`, `test_ty_g_component_markers_panel_v1`).
- **Vitamin D:** `confirmatory_tests: []` in the asset — repeat 25(OH)D is not yet in the registry; loader allows an empty list with asset notes.

## Tests

- `backend/tests/unit/test_root_cause_v1_homocysteine.py` — R-8 regression: governed hypotheses for both signals; fallback still used for an unregistered lead signal.

## Wave 2 (not in scope)

- Iron, inflammatory, renal, expanded thyroid, and other lipid signals per `docs/RESET_SPRINT_PLAN_2026-04.md` Sprint 8 remain follow-up work.
