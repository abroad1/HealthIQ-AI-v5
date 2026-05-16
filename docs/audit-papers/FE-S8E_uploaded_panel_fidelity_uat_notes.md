# FE-S8E — Uploaded-panel fidelity rendering (UAT notes)

**Work ID:** FE-S8E  
**Branch:** `launch-core/fe-s8e-uploaded-panel-fidelity-rendering`  
**Test analysis:** `e4dc8e59-2588-4943-b37b-a299c89f9442`  
**URL:** http://localhost:3000/results?analysis_id=e4dc8e59-2588-4943-b37b-a299c89f9442  
**Account:** test-user3@example.com  

## 1. Files changed

| File | Change |
|------|--------|
| `frontend/app/types/analysis.ts` | Types for `upload_panel_observations`, `display_unit_policy`, `AnalysisResultMetaV1` |
| `frontend/app/lib/uploadPanelFidelity.ts` | Renderer-only row builder (no conversion) |
| `frontend/app/components/biomarkers/UploadedPanelFidelity.tsx` | Mode A UI section |
| `frontend/app/(app)/results/page.tsx` | Wire meta → fidelity rows under biomarker dials |
| `frontend/app/components/biomarkers/BiomarkerDials.tsx` | `white_blood_cells` display label |
| `frontend/tests/lib/uploadPanelFidelity.test.ts` | Unit tests |

## 2. UI behaviour before

- Results page built biomarker dials only from `biomarkers[]`.
- `meta.upload_panel_observations` and `meta.display_unit_policy` were ignored.
- HbA1c `%` (`hba1c_pct`), upload K/uL, mEq/L, and haematocrit `%` were not visible in Mode A.

## 3. UI behaviour after

- Under **Biomarker evidence** (inside **Advanced & clinician report**), an **Uploaded panel values** grid lists upload rows where the unit differs from the canonical dial or where the key is an equivalent observation (e.g. `hba1c_pct`).
- Canonical dials unchanged (still from `biomarkers[]` only).
- Equivalent rows carry an **Equivalent** badge and copy stating they are not scored separately.

## 4. How `upload_panel_observations` is rendered

`buildUploadedPanelFidelityRows()` reads `currentAnalysis.meta.upload_panel_observations`, parses each `{ value, unit }` from the API, and renders cards via `UploadedPanelFidelity` with no numeric transformation.

## 5. Duplicate-equivalent annotation

- `hba1c_pct` → linked to `hba1c`, badge **Equivalent**, note: “Uploaded representation of HbA1c — not scored separately.”
- Same-key unit mismatches (e.g. haematocrit `%` vs analytical `L/L`) use **Uploaded unit** badge and note referencing the canonical analytical value/unit from `biomarkers[]`.

## 6. Renderer-only confirmation

- No conversion constants added in frontend app code.
- `Select-String` scan on `frontend/app/**` for common conversion factors: **no hits** in new code paths.
- Row values and units are displayed as returned in `upload_panel_observations`.

## 7. Validation commands run

| Command | Result |
|---------|--------|
| `npm run type-check` | **Pass** |
| `npx jest tests/lib/uploadPanelFidelity.test.ts` | **Pass** (3 tests) |
| `npm run lint` | **Fail** — pre-existing: `Failed to load config "next/core-web-vitals"` from repo `.eslintrc.json` |
| `npm run test` (full suite) | **Not used as gate** — unrelated failures in clusterStore, uiStore, BiomarkerForm, etc. |

## 8. Browser UAT result

**Date:** 2026-05-16  
**Session:** test-user3 (logged in)

| Check | Result |
|-------|--------|
| Page loads, API 200 | **Pass** |
| Canonical HbA1c dial `42 mmol/mol` | **Pass** |
| Uploaded **HbA1c (%)** `6 %` with equivalent note | **Pass** |
| Haematocrit upload `43.8 %` vs dial `0.438 L/L` | **Pass** |
| Platelets `225 K/uL`, WBC `6.4 K/uL` | **Pass** |
| Na/K/Cl `mEq/L` upload rows | **Pass** |
| Dial label **White Blood Cells** (not slug) | **Pass** |
| Console/network errors | **None observed** during UAT |

**Note:** Expand **Advanced & clinician report** → **Show** to reach biomarker dials and the uploaded-panel section.

## 9. Known gaps deferred

- Upload-review / upload-edit surfaces not updated in this sprint (results page only).
- `meta.display_unit_policy` from API currently omits per-biomarker blocks; equivalence linking uses `_pct` suffix inference plus policy map when present.
- Trust strip “3 of 3 expected markers” on 24-marker panel (pre-existing DQ copy).
- Full `npm run lint` / full Jest suite blocked by pre-existing environment/test debt.

## Explicit non-authority

Implementation only. Architecture sign-off and merge remain human-governed.
