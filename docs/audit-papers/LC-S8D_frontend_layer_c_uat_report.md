# LC-S8D Frontend / Layer C UAT Report

**Analysis:** `e4dc8e59-2588-4943-b37b-a299c89f9442`  
**URL:** http://localhost:3000/results?analysis_id=e4dc8e59-2588-4943-b37b-a299c89f9442  
**Date:** 2026-05-16  
**Method:** Browser (logged in as `test-user3@example.com`) + authenticated API inspection + read-only code cross-check.

---

## 1. Overall verdict: PASS WITH GAPS

| Area | Result |
|------|--------|
| Page/API health | **Pass** — results load; API 200; no failed XHR |
| Backend Layer B / analytical payload | **Pass** — canonical units, duplicate collapse, BUN→urea, no `0.438 %` haematocrit |
| Layer C Mode B (analytical report surfaces) | **Mostly pass** — dials + narrative use canonical analytical rows |
| Layer C Mode A (uploaded-panel fidelity) | **Fail (frontend)** — backend ships `upload_panel_observations`; UI does not consume it |
| LC-S8D merge | **Accept backend with follow-up frontend sprint** for Mode A fidelity |

---

## 2. Page / API health

| Check | Result |
|-------|--------|
| `/results` loads | **Yes** — “Your results”, **24 markers**, biomarker evidence after expanding **Advanced & clinician report** |
| Console errors | **None** — only dev warnings (React DevTools, hydration `data-cursor-ref`, Cursor dialog override) and store debug logs |
| Failed network calls | **None** on results load |
| `GET /api/analysis/result?analysis_id=bd17f7b4-74af-4668-9d25-e6bfdbbd957c` | **200**, 24 biomarkers |
| `GET /api/analysis/result?analysis_id=e4dc8e59-2588-4943-b37b-a299c89f9442` | **200**, valid JSON |
| `clinician_report_v1` | **Present** |
| `meta.upload_panel_observations` | **Present** — 20 uploaded keys (incl. `hba1c` + `hba1c_pct`) |
| `meta.display_unit_policy` | **Present** — version `1.0.0` |

Browser result fetch: `GET http://127.0.0.1:8000/api/analysis/result?analysis_id=e4dc8e59-...` → **200**.

---

## 3. Raw payload summary

| Field | Value |
|-------|--------|
| Biomarker count (`biomarkers[]`) | **24** (includes derived ratios) |
| Upload observations (`meta.upload_panel_observations`) | **20** rows |
| Missing `unit` / `value` | **None** on scored rows |
| `unscored_reason` | **None** on main panel markers |
| Empty `reference_range` | **`remnant_cholesterol` only** — `min`/`max` null, status `unknown`, interpretation *“Not scored - no compatible policy bounds”* |
| Duplicate HbA1c in `biomarkers[]` | **No** — only `hba1c` @ 42 mmol/mol; `hba1c_pct` (6 %) **only** in `upload_panel_observations` |
| Haematocrit in `biomarkers[]` | **0.438 L/L** (not `%`) |
| BUN / urea | Upload `urea` 14 mg/dL; analytical `urea` 4.998 mmol/L; **`urate` separate** @ 5.8 mg/dL |

---

## 4. Layer C Mode A — Uploaded-panel fidelity

**Verdict: Backend-ready; frontend incomplete (partial / fail for full Mode A).**

| Rule | Backend | Frontend UI |
|------|---------|-------------|
| All uploaded rows visible where safe | `upload_panel_observations` has 20 originals (mixed units) | Dials built **only** from `biomarkers[]` (24 canonical/derived) — **no** upload-fidelity surface |
| Duplicate-equivalent rows not silently dropped | `hba1c_pct` preserved in meta | **Not shown** — no second HbA1c card, no “6 %” row |
| HbA1c mmol/mol + % both visible / linked | Both in meta | **Only** mmol/mol HbA1c dial |
| No frontend conversion maths | N/A | **Pass** — `page.tsx` passes `biomarker.unit` / `reference_range` through; no `upload_panel` usage anywhere in `frontend/` |

`frontend/app/(app)/results/page.tsx` builds `biomarkerDialData` exclusively from `biomarkers[]` (lines 486–520). **Zero** references to `upload_panel_observations` or `display_unit_policy` in frontend types or components.

---

## 5. Layer C Mode B — Analytical-report mode

**Verdict: Largely compliant** on this run (backend collapse + frontend renderer-only on canonical DTO).

| Rule | Evidence |
|------|----------|
| Collapse duplicate HbA1c | Single `hba1c` in clusters, metabolic pattern, dials, Layer C `elevated_hba1c` flag — **no** `%` duplicate scored |
| Haematocrit not `0.438 %` | API & UI: **0.438 L/L** |
| BUN → urea, not urate | Upload `urea` 14 mg/dL; analytical `urea` mmol/L; **Urate** separate dial |
| Canonical analytical units | Glucose/cholesterol mmol/L, creatinine µmol/L, platelets/WBC **10^9/L**, electrolytes **mmol/L**, vitamin D **nmol/L** |
| Phase B–sensitive markers not mis-scored | Ca, Mg, free T4, Hb, urate: **same mg/dL (or g/dL) in upload and analytical** — scored with lab ranges, not bogus conversions |
| Frontend renderer-only | Confirmed — no conversion constants in dial path |

**Caveats (non-blocking for Mode B unit rules, but visible in product):**

- Hero primary finding: **“No governed WHY for signal_renal_metabolic_stress”** (copy/compile gap, not unit math).
- Trust strip: **“We received 3 of 3 expected markers”** on a **24-marker** panel — misleading DQ copy.
- **Vitamin D:** upload **32 ng/mL** → analytical **80 nmol/L** (governed canonical conversion per SSOT `nmol/L`); scored normal — intentional Layer B, not frontend conversion.

---

## 6. Marker-by-marker findings

| Marker | Upload (`meta.upload_panel_observations`) | Analytical (`biomarkers[]`) | UI (Biomarker dials) | LC-S8D expectation |
|--------|-------------------------------------------|-----------------------------|----------------------|-------------------|
| **HbA1c** | 42 mmol/mol + **6 %** (`hba1c_pct`) | 42 mmol/mol, elevated | HbA1c **mmol/mol** only | Layer B: mmol/mol only — **pass**; Mode A % row — **not rendered** |
| **Haematocrit** | 43.8 **%** | 0.438 **L/L** | **L/L** | No `0.438 %` — **pass**; upload % not shown — Mode A gap |
| **Platelets** | 225 **K/uL** | 225 **10^9/L** | Platelet Count **10^9/L** | 1:1 equivalence — **pass** |
| **WBC** | 6.4 **K/uL** | 6.4 **10^9/L** | **white blood cells** 10^9/L (raw slug label) | Units **pass**; label polish gap |
| **Sodium** | 140 **mEq/L** | 140 **mmol/L** | sodium **mmol/L** | **pass** |
| **Potassium** | 4.3 **mEq/L** | 4.3 **mmol/L** | potassium **mmol/L** | **pass** |
| **Chloride** | 102 **mEq/L** | 102 **mmol/L** | chloride **mmol/L** | **pass** |
| **Glucose** | 95 **mg/dL** | 5.28 **mmol/L** | Glucose **mmol/L** | Canonical conversion (backend) — **pass** |
| **Total / LDL / HDL chol.** | mg/dL | mmol/L | mmol/L | **pass** |
| **Creatinine** | 1.02 **mg/dL** | 90.17 **µmol/L** | **µmol/L** | Strict conversion — **pass** |
| **BUN / Urea** | urea 14 **mg/dL** | urea 4.998 **mmol/L** | **Urea** mmol/L (not urate) | BUN→urea — **pass** |
| **Vitamin D** | 32 **ng/mL** | 80 **nmol/L** | **nmol/L** | Canonical nmol/L — **pass** (backend conversion) |
| **Calcium / Mg / Free T4 / Hb** | mg/dL or g/dL | Same units | Same | Phase B passthrough — **pass**, not mis-scored |
| **Uric acid / Urate** | 5.8 **mg/dL** | 5.8 **mg/dL** | **Urate** mg/dL | Separate from urea — **pass** |
| **Derived** | — | ratios + remnant chol. | Shown; remnant **not scored** | Correct explicit unscored handling |

---

## 7. Defects

| # | Symptom | Likely root cause | File(s) | Severity | Blocks LC-S8D merge? |
|---|---------|-------------------|---------|----------|----------------------|
| D1 | No upload-fidelity rows; `hba1c_pct` / original K/uL, mEq/L, % not visible in dials | Frontend never reads `meta.upload_panel_observations` or `display_unit_policy` presentation mode | `frontend/app/(app)/results/page.tsx`, `BiomarkerDials.tsx`, `frontend/app/types/analysis.ts` | **High** (Mode A) | **Yes** for full Layer C sign-off; **no** if sprint scope is backend-only |
| D2 | No linking/annotation between equivalent rows (HbA1c % ↔ mmol/mol) | Same as D1 | Same | **Medium** | Same as D1 |
| D3 | Hero: “No governed WHY for signal_renal_metabolic_stress” | Report compile / WHY SSOT gap (pre-existing) | `report_compiler_v1.py`, narrative components | **Medium** (product) | **No** (unit governance) |
| D4 | Trust strip “3 of 3 expected markers” on 24-marker run | DQ copy / completeness logic | Results DQ components | **Low–Medium** | **No** |
| D5 | `white_blood_cells` shown as slug, not “White Blood Cells” | Missing entry in `BIOMARKER_NAMES` | `BiomarkerDials.tsx` | **Low** | **No** |
| D6 | `remnant_cholesterol` dial with empty range | Policy bounds missing — correctly unscored | `scoring_policy` / backend | **Info** | **No** |

---

## 8. Recommendation

**Accept LC-S8D backend unit governance for merge**, with a **dedicated follow-up frontend sprint** to implement Mode A (`uploaded_panel_fidelity`):

1. Render `meta.upload_panel_observations` on dial / upload-review surfaces (or dual-mode rows per `display_unit_policy.yaml`).
2. Surface `hba1c_pct` alongside canonical `hba1c` with governed equivalence copy (no client-side conversion).
3. Optionally add upload-unit footnotes (“uploaded as 43.8 %”) using meta only.

**Do not** block backend merge on D3/D4/D5 unless product owners require polished hero copy in the same release.

---

## Quick reference — what worked well

- Prior **500 on `/api/analysis/result`** is **fixed** for this analysis.
- Mixed-unit LC-S8D panel: **no double HbA1c scoring**, **no haematocrit % bug**, **urea vs urate** separation correct.
- Frontend remains **renderer-only** on the analytical DTO; LC-S7 range suppression path intact in `BiomarkerDials.tsx`.

---

## Files cross-checked (read-only)

- `frontend/app/(app)/results/page.tsx`
- `frontend/app/components/biomarkers/BiomarkerDials.tsx`
- `frontend/app/types/analysis.ts`
- `backend/app/routes/analysis.py`
- `backend/core/units/display_policy.py`
- `backend/ssot/display_unit_policy.yaml`
