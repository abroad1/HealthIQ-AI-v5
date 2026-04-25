# R-1B — Unscored marker trust gaps

**Work package:** R-1B  
**Branch:** `fix/unscored-marker-trust-gaps`

## Files touched

| Area | File |
|------|------|
| Coercion | `backend/core/analytics/primitives.py` — `coerce_optional_float()` for string lab bounds |
| Scoring | `backend/core/scoring/rules.py` — string bounds via coercion; HbA1c % vs mmol/mol harmonisation; `UNSCORED_REASON_HBA1C_UNIT_MISMATCH` |
| Engine | `backend/core/scoring/engine.py` — pass `value_unit` into `calculate_biomarker_score` |
| Orchestrator | `backend/core/pipeline/orchestrator.py` — coerce bounds when building `input_reference_ranges`; include `unscored_reason` in `score_biomarkers` dicts; DTO interpretation prioritises `unscored_reason` / HbA1c message |
| Tests | `backend/tests/unit/test_r1b_unscored_trust_gaps.py` |

## Defect → fix

1. **`unscored_reason` dropped** — `BiomarkerScore.unscored_reason` is now copied into each `biomarker_scores[]` row in the orchestrator serialisation used by Step 6 DTO building, so interpretation logic can read the real reason.

2. **One-sided live markers with string bounds** — Lab JSON often sends `"min": "0.9"` strings; orchestrator and rules now use `coerce_optional_float` so ranges enter `input_reference_ranges` and scoring paths correctly.

3. **HbA1c unit mismatch** — For `hba1c` / `hba1c_pct`, when the measured value unit (e.g. `%`) and the lab range unit (e.g. `mmol/mol`) differ, bounds are converted using the existing `UnitRegistry` IFCC→NGSP linear mapping before scoring. If units cannot be aligned to a known HbA1c family, scoring returns `hba1c_value_and_reference_range_units_incompatible` instead of implying a bounds failure. DTO copy states the HbA1c alignment case explicitly when that reason is present.

## Follow-up (not implemented)

- Display of reference range in the client may still show raw lab units while the score used harmonised bounds; a future UI pass could show both or the aligned view.
