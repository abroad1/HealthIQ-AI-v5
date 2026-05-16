# FE-S8E Post-Merge Human UAT — Back-to-Back Comparison Report

**Date:** 2026-05-16  
**Method:** Authenticated API inspection + browser (logged in as `test-user3@example.com`)  
**Scope:** Investigate only — no code changes.

| Report | Analysis ID |
|--------|-------------|
| **Original (LC-S8D reference)** | `e4dc8e59-2588-4943-b37b-a299c89f9442` |
| **New post-merge human test** | `a817efa9-f915-4309-8b25-51c44cf98d62` |

**Important context:** API diff shows **identical** `biomarkers[]` and `upload_panel_observations` between the two runs (same mixed-unit LC-S8D panel, re-analysed after merge). Comparison is therefore **behavioural parity** (post-merge FE + backend) and **stability**, not two different lab files.

---

## 1. Overall verdict: PASS WITH GAPS

| Area | Result |
|------|--------|
| End-to-end stability (both reports) | **Pass** — load, 200 API, no 500, no failed XHR |
| Payload parity (original vs new) | **Pass** — analytical + upload meta match |
| Layer C Mode A (post-merge FE) | **Pass** — uploaded-panel section present on **both** reports when viewed in current build |
| Layer C Mode B | **Pass** — canonical dials; no double HbA1c scoring; no haematocrit `%` bug |
| Regressions vs LC-S8D reference behaviour | **None observed** |
| Release blockers | **None** for unit/Layer C governance; **follow-up polish** only |

---

## 2. Page / API health

| Check | Original `e4dc8e59…` | Post-merge `a817efa9…` |
|-------|----------------------|-------------------------|
| `/results` loads | Yes — 24 markers | Yes — 24 markers |
| Blank screen / 500 | No | No |
| Failed network calls | None | None |
| Material console errors | None (dev warnings only) | None (dev warnings only) |
| `GET /api/analysis/result` | **200** | **200** |
| `clinician_report_v1` | Present | Present |
| `meta.upload_panel_observations` | Present (20 keys) | Present (20 keys) |
| `meta.display_unit_policy` | Present v1.0.0 | Present v1.0.0 |

---

## 3. Payload comparison summary

| Field | Original | Post-merge | Match? |
|-------|----------|------------|--------|
| `biomarkers[]` count | 24 | 24 | Yes |
| Panel markers (excl. derived) | 19 | 19 | Yes |
| Derived markers | 5 (`tc_hdl_ratio`, `ldl_hdl_ratio`, `non_hdl_cholesterol`, `remnant_cholesterol`, `urea_creatinine_ratio`) | 5 | Yes |
| `upload_panel_observations` count | 20 | 20 | Yes |
| `hba1c_pct` in `biomarkers[]` | No | No | Yes |
| Missing unit/value / malformed RR | None on panel | None on panel | Yes |
| `unscored_reason` on panel | None | None | Yes |
| `remnant_cholesterol` | Unscored (empty policy bounds) | Same | Yes |

**Biomarker and upload-observation payloads are equivalent** on scored fields (same values/units/statuses).

---

## 4. Layer C Mode A — Uploaded-panel fidelity

**Verdict: Pass (current FE-S8E build on both report IDs).**

Observed on **both** reports after expanding **Advanced & clinician report**:

- Section **“Uploaded panel values”** with copy that values are shown as received (no browser recalculation).
- **HbA1c (%)** — **6 %**, badge **Equivalent**, note *“Uploaded representation of HbA1c — not scored separately”*, linked to `hba1c`.
- **Haematocrit** — **43.8 %** upload row; analytical dial **L/L** (not `0.438 %`).
- **K/uL** (platelets, WBC), **mEq/L** (Na/K/Cl), **mg/dL** / **ng/mL** preserved on upload rows with footnotes pointing to analytical units.
- **No** `hba1c_pct` in analytical dials; equivalent upload rows are **not** scored separately.

**vs prior LC-S8D UAT (pre–FE-S8E):** Mode A UI was missing then; it is **now present** on the reference analysis too (stored meta + new renderer). That is an **improvement**, not a regression.

**Frontend conversion:** No forbidden conversion constants in `frontend/app` (LC-S8D sentinel pattern clean).

---

## 5. Layer C Mode B — Analytical-report mode

**Verdict: Pass — consistent across both reports.**

| Rule | Both reports |
|------|----------------|
| Dials from `biomarkers[]` only | Yes |
| HbA1c scored once | 42 mmol/mol, elevated — single dial |
| Haematocrit | **0.438 L/L** (never `0.438 %`) |
| Platelets / WBC | **225** / **6.4** **10^9/L** |
| Na / K / Cl | **140** / **4.3** / **102** **mmol/L** |
| Glucose / lipids | **mmol/L** |
| Creatinine | **90.168 µmol/L** |
| BUN → urea | Upload **urea** 14 mg/dL → analytical **urea** 4.998 mmol/L |
| Urate separate | **5.8 mg/dL**, distinct from urea |
| Narrative duplicate HbA1c | No `%` duplicate in metabolic cluster / Layer C flags |

Phase B passthrough markers (Ca, Mg, free T4, Hb, urate): **unchanged units**, scored with lab ranges — not silently mis-converted.

---

## 6. Marker-by-marker comparison table

Upload and analytical columns are **identical** for both analysis IDs.

| Marker | Upload (both) | Analytical (both) | Verdict |
|--------|---------------|-------------------|---------|
| HbA1c | 42 mmol/mol | 42 mmol/mol, elevated | **Match** |
| HbA1c % | 6 % (upload only) | Not in `biomarkers[]` | **Match** |
| Haematocrit | 43.8 % | 0.438 L/L | **Match** |
| Platelets | 225 K/uL | 225 10^9/L | **Match** |
| WBC | 6.4 K/uL | 6.4 10^9/L | **Match** |
| Sodium | 140 mEq/L | 140 mmol/L | **Match** |
| Potassium | 4.3 mEq/L | 4.3 mmol/L | **Match** |
| Chloride | 102 mEq/L | 102 mmol/L | **Match** |
| Glucose | 95 mg/dL | 5.277778 mmol/L | **Match** |
| Total cholesterol | 190 mg/dL | 4.9134 mmol/L | **Match** |
| LDL | 115 mg/dL | 2.9739 mmol/L | **Match** |
| HDL | 62 mg/dL | 1.60332 mmol/L | **Match** |
| Creatinine | 1.02 mg/dL | 90.168 µmol/L | **Match** |
| BUN / Urea | 14 mg/dL | 4.998 mmol/L | **Match** |
| Vitamin D | 32 ng/mL | 80 nmol/L | **Match** (governed canonical) |
| Calcium | 9.4 mg/dL | 9.4 mg/dL | **Match** |
| Magnesium | 2.1 mg/dL | 2.1 mg/dL | **Match** |
| Free T4 | 1.2 ng/dL | 1.2 ng/dL | **Match** |
| Urate | 5.8 mg/dL | 5.8 mg/dL | **Match** |
| Haemoglobin | 14.6 g/dL | 14.6 g/dL | **Match** |

**UI (both, current FE):** Same dials + same uploaded-panel rows (incl. HbA1c %, 43.8 %, K/uL, mEq/L).

---

## 7. Regression checks

| Check | Result |
|-------|--------|
| Uploaded-panel section missing | **No** — present on both |
| HbA1c % missing from upload surface | **No** — visible with Equivalent badge |
| HbA1c % separately scored in dials | **No** |
| Haematocrit as `0.438 %` | **No** |
| BUN → urate confusion | **No** |
| Frontend conversion maths | **No** |
| Phase B markers mis-scored / wrong unit | **No** |
| New console/network errors | **No** |

**Ongoing non-regression product gaps (both reports, pre-existing):**

| ID | Symptom | Severity | Blocks release? |
|----|---------|----------|-----------------|
| P1 | Hero: “No governed WHY for signal_renal_metabolic_stress” | Medium (copy) | No |
| P2 | Trust strip “3 of 3 expected markers” on 24-marker panel | Low–Medium | No |
| P3 | Dial label `white blood cells` (slug) vs “White Blood Cells” in upload section | Low | No |
| P4 | `remnant_cholesterol` explicitly not scored | Info | No |

---

## 8. Defects (comparison-specific)

**No new defects** introduced by post-merge run relative to reference payload.

The only meaningful delta vs **first** LC-S8D UAT (before FE-S8E) is **positive**: Mode A upload fidelity UI now works for **both** stored analyses that include `upload_panel_observations`.

---

## 9. Final recommendation

**Release acceptable** for LC-S8D + FE-S8E unit/Layer C behaviour.

- Post-merge human test (`a817efa9…`) is **stable and consistent** with reference analysis (`e4dc8e59…`).
- Treat as **regression confirmation** of the same LC-S8D mixed-unit fixture, not a second independent lab file.
- **Follow-up polish only:** governed WHY copy (P1), trust-strip completeness wording (P2), dial display-name for WBC (P3).

**Do not block release** on unit governance or Mode A/B split.

---

## Related reports

- `LC-S8D_frontend_layer_c_uat_report.md` — pre–FE-S8E frontend/Layer C review (same reference analysis ID)

## Files cross-checked (read-only)

- `frontend/app/(app)/results/page.tsx`
- `frontend/app/lib/uploadPanelFidelity.ts`
- `frontend/app/components/biomarkers/UploadedPanelFidelity.tsx`
- `frontend/app/components/biomarkers/BiomarkerDials.tsx`
