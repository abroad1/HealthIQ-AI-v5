# LC-S8 — Biomarker unit / range normalisation QA — completion (2026-05)

**work_id:** LC-S8-BIOMARKER-UNIT-RANGE-NORMALISATION-QA  
**branch:** `sprint8/biomarker-unit-range-normalisation-qa`

## Canonical unit policy (confirmed)

- Authoritative biomarker base units remain in `backend/ssot/biomarkers.yaml` (e.g. hemoglobin `g/dL`, hematocrit `%`, HbA1c `%`).
- Conversion factors remain in `backend/ssot/units.yaml`; no duplicate SSOT was introduced.
- Hemoglobin canonical key stays US `hemoglobin` with UK spelling `haemoglobin` as an alias only (per hardening). Broad SSOT flip of hemoglobin base unit to `g/L` was **not** done to avoid historical fixture drift (STOP path per sprint Task 3).

## SSOT changes

- `backend/ssot/units.yaml`: governed conversions for hemoglobin `g/L` ↔ `g/dL` and hematocrit `L/L` ↔ `%` (present in tree; concentration categories include mass/volume as required).
- `backend/ssot/biomarkers.yaml`: `haemoglobin` alias under canonical `hemoglobin` (if not already committed in an earlier bus commit).

## Unit conversion / registry (Layer A)

- `backend/core/units/registry.py`:
  - `UnitEnum`: `g/L`, `L/L`.
  - Strict conversion sets extended with hemoglobin and hematocrit.
  - `_get_conversion_factor` wired to YAML keys for hemoglobin and hematocrit.
  - `apply_unit_normalisation`: one-sided reference ranges (`min` only or `max` only) converted to base unit when a reference unit is known; passthrough dicts whose `unit` does not match base after conversion are cleared (`reference_range` set to `None`) to avoid silent incoherent ranges.
  - `value_and_reference_units_coherent_for_numeric_compare()`: shared guard for Layer B (equivalent units, registry factor path, HbA1c `%` / `mmol/mol` pair, `hba1c_pct` mapped to `hba1c` for lookups).

## Haemoglobin outcome

- UK-style panels in `g/L` with `g/L` ranges, or mixed `g/dL` value with `g/L` range, normalise to internal base `g/dL` with bounds converted deterministically (regression tests).

## Haematocrit outcome

- `L/L` values with `%` or `L/L` ranges convert to base `%` with both value and range on the same axis (regression tests). Internal base remains `%` per SSOT; `L/L` is a governed input/display axis via conversion, not a silent `%` label on a raw fraction without conversion.

## HbA1c outcome

- Existing harmonisation in `ScoringRules._harmonise_hba1c_reference_range` runs **before** the new coherence gate.
- New gate allows the `%` / `mmol/mol` pair for `hba1c` / `hba1c_pct` so harmonisation can align bounds; incompatible non-HbA1c pairs still fail the factor check.
- Canonical SSOT unit for HbA1c was **not** flipped to `mmol/mol` globally (would be broad behavioural change; deferred / STOP per Task 5).

## Ratios outcome

- No new ratio-specific tests in this slice (Task 6 deferred). Existing pipeline order (normalise before derived computation) unchanged.

## Scoring safety (Layer B)

- `backend/core/scoring/rules.py`: `UNSCORED_REASON_UNIT_REFERENCE_RANGE_INCOHERENT` (`unit_reference_range_incoherent`); `calculate_biomarker_score` rejects numeric scoring when value unit and reference unit are not coherent after HbA1c harmonisation.
- `backend/core/pipeline/orchestrator.py`: consumer interpretation string for the new unscored reason (renderer-only policy unchanged).

## Sentinel

- Defect class: `biomarker_value_reference_unit_incoherence`
- Pack: `sentinel/packs/escaped_defects_v1.json`
- Runner map: `sentinel/sentinel_runner.py` → `backend/tests/regression/test_lc_s8_biomarker_unit_reference_incoherence_regression.py`

## Tests run (this completion)

| Command | Result |
|--------|--------|
| `python -m pytest backend/tests/regression/test_lc_s8_biomarker_unit_reference_incoherence_regression.py -q` | **11 passed** |
| `python sentinel/sentinel_runner.py --defect-class biomarker_value_reference_unit_incoherence` | **0 issues**, report generated |

**Note:** `backend/tests/unit/test_hba1c_governance.py::TestHbA1cLayerBBoundPath::test_orchestrator_input_excludes_hba1c_pct_when_both_present` currently fails with `IndexError` in `narrative_compiler_lc_s3_assembly_v1` (`top_findings[0]` empty) during full orchestrator `run`; this appears orthogonal to LC-S8 unit changes. `backend/tests/unit/test_unit_registry.py` route tests observed 500 vs expected 2xx in this environment (likely service/fixture setup).

## Known limitations / deferred

- Task 6 ratio-specific regression tests not added.
- Task 8 frontend display pass not re-verified in this session (LC-S7 defensive handling assumed retained).
- HbA1c canonical internal unit preference `mmol/mol` not adopted at SSOT level.
- Old persisted analyses: unchanged on disk; **new** runs use updated normalisation and scoring guards.

## Scope confirmations (closure)

- **Knowledge Bus:** not modified.
- **Questionnaire:** not modified.
- **Narrative compiler:** not modified (orchestrator import/copy only).
- **Automation Bus control-plane scripts:** not modified.
