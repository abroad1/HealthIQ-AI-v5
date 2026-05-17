# LC-S8G — Uploaded-Unit Display Fidelity Contract

**Work ID:** LC-S8G  
**Branch:** `launch-core/lc-s8f-phase-b-uk-si-true-conversions` (continues LC-S8F, unmerged)

## Defect origin

LC-S8F correctly canonicalises Phase B biomarkers in Layer B, but main biomarker dials rendered `biomarkers[].value/unit` (analytical UK/SI only). Uploaded US units lived only in `meta.upload_panel_observations` (FE-S8E secondary section). Human UAT: calcium 9.4 mg/dL displayed as 2.35 mmol/L on primary cards.

## Fix summary

| Surface | Before | After |
| ------- | ------ | ----- |
| API biomarker row | `value`, `unit`, `reference_range` only | + `display_*`, `analytical_*`, `display_is_uploaded_unit` |
| Main dials | `value` / `unit` | `display_value ?? value`, `display_unit ?? unit` |
| Transparency | None | `Analysed internally as [analytical_unit]` when units differ |

## Files changed

- `backend/core/units/display_fidelity_v1.py` — **new** display field enrichment
- `backend/core/dto/builders.py` — `analysis_route_biomarker_row_with_display`
- `backend/app/routes/analysis.py` — wire upload panel into row shaping
- `backend/ssot/display_unit_policy.yaml` — Phase B + urate/uric_acid policy blocks
- `frontend/app/types/analysis.ts` — display contract types
- `frontend/app/(app)/results/page.tsx` — dial mapping
- `frontend/app/components/biomarkers/BiomarkerDials.tsx` — transparency note
- `backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py` — **new**
- `docs/audit-papers/LC-S8G_uploaded_unit_display_fidelity_notes.md` — this file

**Not changed:** `backend/core/units/registry.py`, SSOT biomarkers/units/scoring (LC-S8F analytical path preserved).

## DTO fields added

- `display_value`, `display_unit`, `display_reference_range`
- `analytical_value`, `analytical_unit`, `analytical_reference_range`
- `display_is_uploaded_unit`
- `analytical_transparency_unit` (when display uses uploaded unit family)

## SSOT-wide guardrail

`test_lc_s8g_uploaded_unit_display_fidelity.py` includes `TestLC_S8GSSOTDisplayCoverageInventory` for biomarkers in the LC-S8G inventory (Phase B + LC-S8D families) and frontend scan for Phase B conversion constants.

## Tests run

| Command | Result |
|---------|--------|
| `pytest backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py -q` | PASS |
| `pytest backend/tests/regression/test_lc_s8f_phase_b_true_conversions.py -q` | PASS |
| `pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q` | PASS |

## UAT replay

Re-run analysis IDs `7cc8b2d5-...` (US) and `b24ce358-...` (UK) after deploy: main dials should show uploaded unit families for US Phase B markers; UK pass-through unchanged.

## Merge recommendation

LC-S8G completes the customer-facing contract required before merging LC-S8F branch. Human sign-off on refreshed UAT still required.

## Verdict

**LC-S8G_IMPLEMENTATION_COMPLETE** (pending human review; not merged).
