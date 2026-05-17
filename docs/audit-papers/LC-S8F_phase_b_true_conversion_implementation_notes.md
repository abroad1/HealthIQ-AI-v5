# LC-S8F — Phase B UK/SI True Conversion Implementation

**Work ID:** LC-S8F  
**Branch:** `launch-core/lc-s8f-phase-b-uk-si-true-conversions`  
**Evidence:** `docs/audit-papers/Phase_B_UK_SI_Biomarker_Unit_Evidence_Review.md` (committed)

## Phase 1 inventory (pre-change → post-change)

| Biomarker | SSOT unit (before → after) | Registry dispatch | Scoring policy |
|-----------|---------------------------|-------------------|----------------|
| calcium | mg/dL → **mmol/L** | Added mg/dL ↔ mmol/L @ 0.2495 | None |
| corrected_calcium | mg/dL → **mmol/L** | Same factor; no recomputation | None |
| magnesium | mg/dL → **mmol/L** | Added @ 0.4114 | None |
| free_t4 | ng/dL → **pmol/L** | Added ng/dL ↔ pmol/L @ 12.871 | None |
| hemoglobin | g/dL → **g/L** | Existing g/dL ↔ g/L @ 10 | **Migrated** g/dL → g/L bands ×10 |
| urate | umol/L → **µmol/L** | Added mg/dL ↔ µmol/L @ 59.5; µmol/L equiv | None |

## Conversion factors implemented

Exact evidence factors in `backend/ssot/units.yaml` and `backend/core/units/registry.py` dispatch.

## Runtime dispatch

- Biomarker groups: `_CALCIUM_BIOMARKERS`, `_MAGNESIUM_BIOMARKERS`, `_FREE_T4_BIOMARKERS`, `_URATE_BIOMARKERS`
- All six in `_STRICT_CONVERSION_BIOMARKERS`
- `UnitEnum`: added `PMOL_L`, `NG_DL`
- Unit definitions: `pmol_L`, `ng_dL` in `units.yaml`

## Reference-range handling

Lab-supplied ranges convert with values via `apply_unit_normalisation`. UK pass-through vectors tested (Hb, urate, Free T4). No generic/global ranges added.

## Corrected calcium caveat

Unit conversion of supplied corrected-calcium values is implemented. Recalculation from total calcium + albumin is **not** implemented.

## Free T4 caveat

`ng/dL → pmol/L` conversion implemented. Lab-specific pmol/L ranges preserved on UK pass-through; no universal range substitution.

## Haemoglobin migration

Atomic: SSOT `g/L`, scoring_policy `g/L`, bands ×10, Sentinel `LC_S8D_SSOT_SCORING_UNIT_ALIGNMENT["hemoglobin"] = "g/L"`.

## Files changed

- `backend/ssot/biomarkers.yaml`
- `backend/ssot/units.yaml`
- `backend/ssot/scoring_policy.yaml`
- `backend/core/units/registry.py`
- `backend/tests/regression/test_lc_s8f_phase_b_true_conversions.py` (new)
- `backend/tests/regression/test_lc_s8_biomarker_unit_reference_incoherence_regression.py`
- `backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py`
- `backend/tests/unit/test_scoring_rules.py`
- `sentinel/packs/lc_s8d_unit_governance_v1.json`

## Tests run

| Command | Result |
|---------|--------|
| `pytest backend/tests/unit/test_unit_registry.py -q` | PASS |
| `pytest backend/tests/unit/test_scoring_rules.py -q` | PASS |
| `pytest backend/tests/regression/test_lc_s8_biomarker_unit_reference_incoherence_regression.py -q` | PASS |
| `pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q` | PASS |
| `pytest backend/tests/regression/test_lc_s8f_phase_b_true_conversions.py -q` | PASS |
| `pytest backend/tests/unit/test_hba1c_governance.py -q` | PASS |

## Verdict

**LC-S8F_IMPLEMENTATION_COMPLETE** (pending human review; not merged).
