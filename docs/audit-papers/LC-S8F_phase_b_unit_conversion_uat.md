# LC-S8F Phase B Unit Conversion — Human UAT Report

**Date:** 2026-05-16  
**Method:** Authenticated API inspection (`test-user3@example.com`) + browser results UI (user-assisted load)  
**Scope:** Investigate only — no code changes.

| Brief label | Analysis ID | URL |
|-------------|-------------|-----|
| **Report A** (brief: US → UK/SI conversion) | `b24ce358-02e3-4058-a667-34328a4168a2` | `http://localhost:3000/results?analysis_id=b24ce358-02e3-4058-a667-34328a4168a2` |
| **Report B** (brief: UK/SI pass-through) | `7cc8b2d5-c8f0-4138-ba18-8540eece06a1` | `http://localhost:3000/results?analysis_id=7cc8b2d5-c8f0-4138-ba18-8540eece06a1` |

**API payloads archived (local run):** `automation_bus/_uat_lc_s8f_A.json`, `automation_bus/_uat_lc_s8f_B.json`  
**Comparison script:** `automation_bus/_uat_lc_s8f_compare.py`

---

## 1. Overall verdict: PASS

| Area | Result |
|------|--------|
| Phase B US → UK/SI conversions (true US panel) | **Pass** — all six markers within expected tolerances (API + UI) |
| UK/SI pass-through (true UK panel) | **Pass** — values and lab ranges unchanged (API + UI) |
| Mode A `upload_panel_observations` | **Pass** — US source units preserved on conversion panel; API present on both |
| Reference-range governance | **Pass** — all observed RRs `source: lab`; no generic policy replacement |
| Frontend conversion maths | **Pass** — display-only; Uploaded panel copy states backend analytical values |
| Browser / rendered UI | **Pass** (user-loaded session) — both pages fully rendered; API 200 |
| Test brief URL ↔ fixture mapping | **Gap** — analysis IDs swapped relative to brief labels (test-setup, not product) |

**Merge recommendation:** **Merge** LC-S8F Phase B conversion logic.  
**Follow-up only:** Correct the two analysis IDs in the human test brief; confirm whether **Uploaded panel values** should always render on pass-through panels (visible on conversion panel only in this UI run).

**Blocks LC-S8F merge?** **No** (conversion and pass-through behaviour verified).

---

## 2. Critical finding — brief labels vs fixtures

The **analysis IDs are wired opposite** to the Report A / Report B descriptions in the UAT brief:

| Analysis ID | Brief says | Actual panel behaviour |
|-------------|------------|-------------------------|
| `b24ce358-…` | Report A — US conversion | **UK/SI pass-through** — upload already mmol/L, g/L, pmol/L, µmol/L; analytical matches upload |
| `7cc8b2d5-…` | Report B — UK pass-through | **US upload → converted analytical** — matches Report A *expectations* in the brief |

**How to judge Phase B:**

- **Conversion behaviour** → judge on **`7cc8b2d5-…`**
- **Pass-through behaviour** → judge on **`b24ce358-…`**

This is a **test-matrix / labelling issue**, not a conversion-engine defect.

---

## 3. Page / API health

| Check | Report A URL (`b24ce358-…`) | Report B URL (`7cc8b2d5-…`) |
|-------|----------------------------|----------------------------|
| Page loads (browser) | Yes — “Your results”, 6 markers | Yes |
| `GET /api/analysis/result` | **HTTP 200** | **HTTP 200** |
| Console (loaded session) | No errors; 6 biomarkers in store | No errors; 6 biomarkers in store |
| Failed network (loaded session) | None | None |
| `meta.upload_panel_observations` | Present (6 keys, UK/SI) | Present (6 keys, US) |
| `meta.display_unit_policy` | Present v1.0.0 | Present v1.0.0 |
| `unit_normalised` (insight graph) | `true` | `true` |

**Note:** An earlier automated browser pass failed with CORS (`localhost:3000` → `127.0.0.1:8000`). User-assisted loading succeeded; API and UI aligned in that session.

---

## 4. Marker-by-marker comparison

Verdict columns use **brief intent for that URL**. **Behaviour verdict** reflects correct engine behaviour for the actual fixture on that ID.

| Marker | Report A uploaded | Report A analytical | Report A verdict (brief / behaviour) | Report B uploaded | Report B analytical | Report B verdict (brief / behaviour) |
|--------|-------------------|---------------------|--------------------------------------|-------------------|---------------------|--------------------------------------|
| **Calcium** | 2.33 mmol/L (API) | 2.33 mmol/L, RR 2.15–2.57 mmol/L | Fail brief / **Pass pass-through** | 9.4 mg/dL | 2.3453 mmol/L, RR 2.1457–2.5449 mmol/L | Fail brief / **Pass conversion** (~2.35) |
| **Corrected Calcium** | 2.25 mmol/L | 2.25 mmol/L, RR 2.20–2.60 | Fail brief / **Pass pass-through** (distinct from Ca 2.33) | 9.4 mg/dL | 2.3453 mmol/L (same as Ca; upload duplicate) | Fail brief / **Pass conversion** (no albumin recalc) |
| **Magnesium** | 0.89 mmol/L | 0.89 mmol/L, RR 0.73–1.06 | Fail brief / **Pass pass-through** | 2.1 mg/dL | 0.86394 mmol/L, RR 0.69938–0.98736 | Fail brief / **Pass** (~0.86) |
| **Free T4** | 16.8 pmol/L | 16.8 pmol/L, RR 12–22 pmol/L | Fail brief / **Pass pass-through** | 1.2 ng/dL | 15.4452 pmol/L, RR 10.2968–23.1678 | Fail brief / **Pass** (~15.45; lab RR converted) |
| **Haemoglobin** | 144 g/L | 144 g/L, RR 130–175 g/L | Fail brief / **Pass pass-through** | 14.6 g/dL | 146 g/L, RR 130–175 g/L | Fail brief / **Pass** (14.6 g/dL → 146 g/L) |
| **Uric Acid / Urate** | 440 µmol/L | 440 µmol/L, RR 220–547 | Fail brief / **Pass pass-through** | 5.8 mg/dL | 345.1 µmol/L, RR 208.25–428.4 | Fail brief / **Pass** (~345 µmol/L) |

### Expected vs observed (conversion panel — `7cc8b2d5-…`)

| Marker | Expected (brief Report A) | API analytical | UI analytical | Match |
|--------|---------------------------|----------------|---------------|-------|
| Calcium | ~2.35 mmol/L from 9.4 mg/dL | 2.3453 mmol/L | 2.3453 mmol/L | Yes |
| Corrected Calcium | ~2.35 mmol/L from 9.4 mg/dL | 2.3453 mmol/L | 2.3453 mmol/L | Yes |
| Magnesium | ~0.86 mmol/L from 2.1 mg/dL | 0.86394 mmol/L | 0.86394 (Uploaded panel footnote) | Yes |
| Free T4 | ~15.45 pmol/L from 1.2 ng/dL | 15.4452 pmol/L | 15.4452 (Uploaded panel footnote) | Yes |
| Haemoglobin | 146 g/L from 14.6 g/dL | 146.0 g/L | 146 g/L | Yes |
| Urate | ~345 µmol/L from 5.8 mg/dL | 345.1 µmol/L | 345.1 (Uploaded panel footnote) | Yes |

### Expected vs observed (pass-through panel — `b24ce358-…`)

| Marker | Expected (brief Report B) | API / UI | Match |
|--------|---------------------------|----------|-------|
| Haemoglobin | 144 g/L, RR 130–175 | 144 g/L | Yes |
| Urate | 440 µmol/L, RR 220–547 | 440 µmol/L | Yes |
| Free T4 | 16.8 pmol/L, RR 12–22 | 16.8 pmol/L | Yes |
| Calcium | 2.33 mmol/L, RR 2.15–2.57 | 2.33 mmol/L | Yes |
| Corrected Calcium | 2.25 mmol/L, RR 2.20–2.60 | 2.25 mmol/L | Yes |
| Magnesium | 0.89 mmol/L, RR 0.73–1.06 | 0.89 mmol/L | Yes |

---

## 5. Brief checklist (items 1–12)

| # | Requirement | Result |
|---|-------------|--------|
| 1 | Both pages load successfully | **Pass** (browser, user session) |
| 2 | Both `/api/analysis/result` return 200 | **Pass** |
| 3 | No console errors or failed network calls | **Pass** (loaded session) |
| 4 | Report A analytical values converted to UK/SI | **Pass on `7cc8b2d5-…`** (not on `b24ce358-…` URL) |
| 5 | Report A lab-derived reference ranges converted coherently | **Pass on `7cc8b2d5-…`** |
| 6 | Report B UK/SI values and ranges pass through | **Pass on `b24ce358-…`** |
| 7 | No generic/default RR replacement | **Pass** — all `source: lab` |
| 8 | Free T4 preserves lab-specific range handling | **Pass** — converted ng/dL band → pmol/L on US panel |
| 9 | Corrected calcium converted as supplied value only | **Pass** — identical upload 9.4 mg/dL → identical analytical; UK panel keeps 2.25 vs Ca 2.33 |
| 10 | Uric acid/urate separate from urea/BUN | **Pass** — `urate` only; no `urea` on panel |
| 11 | Haemoglobin in g/L, not g/dL | **Pass** on conversion panel (146 g/L analytical) |
| 12 | No frontend conversion maths | **Pass** — `uploadPanelFidelity.ts` display-only; Uploaded panel states API analytical values |

---

## 6. Mode A — `meta.upload_panel_observations`

### API (`7cc8b2d5-…` — US conversion panel)

| Key | Upload (preserved) | Analytical (biomarkers[]) |
|-----|--------------------|---------------------------|
| calcium | 9.4 mg/dL | 2.3453 mmol/L |
| corrected_calcium | 9.4 mg/dL | 2.3453 mmol/L |
| free_t4 | 1.2 ng/dL | 15.4452 pmol/L |
| hemoglobin | 14.6 g/dL | 146 g/L |
| magnesium | 2.1 mg/dL | 0.86394 mmol/L |
| urate | 5.8 mg/dL | 345.1 µmol/L |

### API (`b24ce358-…` — UK pass-through panel)

Upload and analytical units match (mmol/L, g/L, pmol/L, µmol/L) — pass-through fidelity.

### Browser — Uploaded panel values section

On **`7cc8b2d5-…`**, expanding **Advanced & clinician report** showed:

- Section **“Uploaded panel values”** with copy: values shown as received; nothing recalculated in the browser.
- Per-marker rows with **Uploaded unit** badge and footnotes, e.g. *“Uploaded as reported on your panel; analytical review uses 15.4452 pmol/L.”*
- US source units preserved: 9.4 mg/dL, 1.2 ng/dL, 14.6 g/dL, 2.1 mg/dL, 5.8 mg/dL.

On **`b24ce358-…`**, the **Uploaded panel values** section was **not observed** in the expanded advanced area (API meta still present). Minor UI coverage gap for pass-through-only panels.

---

## 7. UI spot-check summary

### Page 1 — `b24ce358-…` (pass-through fixture)

- **What's driving this:** Hemoglobin 144 g/L, Calcium 2.33 mmol/L, Corrected Calcium 2.25 mmol/L.
- **Biomarker evidence:** All six markers in UK/SI units (g/L, mmol/L, pmol/L, µmol/L).
- Dial cards: e.g. Haemoglobin 144.0, range 130–175 g/L; Calcium 2.3 mmol/L (display rounding), range 2.15–2.57.

### Page 2 — `7cc8b2d5-…` (conversion fixture)

- **What's driving this:** Hemoglobin **146 g/L**, Calcium **2.3453 mmol/L**, Corrected Calcium **2.3453 mmol/L**.
- **Uploaded panel values:** Full Mode A table with US upload + analytical cross-reference (see §6).
- Network: `GET …/api/analysis/result?analysis_id=7cc8b2d5-…` → **200**.

---

## 8. Defects and gaps

| ID | Severity | Description | Blocks merge? |
|----|----------|-------------|----------------|
| D1 | Test setup | Report A/B URLs swapped vs brief labels | **No** |
| D2 | UI / minor | Uploaded panel values section not visible on pass-through page (`b24ce358-…`) | **No** for conversion merge |
| D3 | Informational | Corrected Ca analytical equals Ca on US panel when upload rows both 9.4 mg/dL | **No** |
| D4 | Cosmetic | `biomarker_nodes[].hemoglobin.lab_unit` null while `biomarkers[].unit` is g/L (API only) | **No** |
| D5 | Environment | Prior agent browser run: CORS `localhost:3000` ↔ `127.0.0.1:8000` | **No** (resolved in user session) |

---

## 9. Related artefacts

| Document | Relevance |
|----------|-----------|
| `docs/audit-papers/LC-S8F_phase_b_true_conversion_implementation_notes.md` | Implementation scope |
| `docs/audit-papers/LC-S8D_uk_si_unit_governance_remediation_notes.md` | Phase B was blocked pre-LC-S8F |
| `docs/audit-papers/FE-S8E_post_merge_comparison_uat.md` | Mode A UI pattern |
| `docs/audit-papers/LC-S9_launch_core_human_proving_closeout_review.md` | Programme context |

---

## 10. Sign-off summary

| Question | Answer |
|----------|--------|
| Phase B true conversions correct? | **Yes** (on `7cc8b2d5-…`) |
| UK/SI pass-through correct? | **Yes** (on `b24ce358-…`) |
| API ↔ UI consistent? | **Yes** (loaded session) |
| LC-S8F merge? | **Recommended — merge** |
| Human test brief action | Swap or relabel the two analysis IDs |

---

*Report produced as part of LC-S8F human UAT (investigate-only). No repository code was modified for this artefact.*
