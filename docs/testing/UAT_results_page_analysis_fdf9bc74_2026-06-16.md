# HealthIQ AI — Results page browser UAT (read-only)

**Date:** 2026-06-16  
**Environment:** `http://localhost:3000/results?analysis_id=fdf9bc74-70db-4d36-be8a-8c709c654df8`  
**Account:** `test-user3@example.com` (authenticated session)  
**Role:** Read-only browser UAT; no code changes.  
**Baseline:** Same checklist as [`UAT_results_page_analysis_b2dfa0c4_2026-05-12.md`](UAT_results_page_analysis_b2dfa0c4_2026-05-12.md).  
**API evidence:** `automation_bus/_uat_fdf9bc74.json` (fetched during session).

---

## 1. Overall verdict

**Classification: not launch-ready — materially improved vs prior run, but this analysis is on a stale contract**

Compared with the earlier UAT on `b2dfa0c4`, most **Layer B/C / compiler / markdown / slug** blockers are **gone**. Journey structure, Actions hub, and health-system cards are much stronger.

This specific run (`fdf9bc74`) is flagged **`result_versioning.compatible: false`** with render blocker `clinician_report_v1`, so the page shows a **stale-result banner** and missing pattern groups. **Regenerate with latest engine** is the right next step before treating this as a fair launch-readiness sample.

---

## 2. Top 5 strengths

1. **Clear journey framing** — “Your results” intro + ordered sections (overview → finding → stable systems → domains → confidence → patterns → markers → follow-up).
2. **Hero aligned to homocysteine lead** — Primary finding is **“Raised homocysteine pattern”** (not the old Vascular Inflammation headline mismatch).
3. **Internal pipeline vocabulary largely removed** — No Layer B/C, deterministic compiler, arbitration, or slug hits in default view.
4. **Actions hub wired** — 5 follow-ups from the latest completed analysis (MMA, repeat homocysteine, etc.); no empty-state contradiction.
5. **Health Systems Cards consumer-grade** — “Your health systems” (no “Wave 1”); expanded CV card shows **“Used in this score”** chips, not raw `score_contributor`.

---

## 3. Top 10 issues (ordered by user impact)

1. **Stale-result banner** — “This saved result uses an older format / cannot be displayed with the current results page contract” + **Regenerate with latest engine** CTA.
2. **Pattern groups unavailable** — “Pattern groups are not available for this result yet” (API: `pattern_groups: []`, versioning incompatible).
3. **B12-associated pattern heading** — Still shown under “Primary finding and why” while evidence bullet correctly says B12 is in range.
4. **79 markers vs 9 of 9** — Toolbar shows **79 markers**; confidence section says **“We received 9 of 9 expected markers for this interpretation.”**
5. **Secondary hero framing** — “Most relevant area: Vascular Inflammation Risk” under a homocysteine-primary hero (softer than old mismatch, still confusing).
6. **Technical detail strip** — Exposes **analysis UUID**, **COMPLETED / N/A**, marker count (acceptable behind toggle, but UUID is consumer-hostile).
7. **Transferrin 2 g/L · Critical** in “What’s driving this” — visually alarming; unit/range sanity not fully verified this pass.
8. **HbA1c dual representation** — Analytical card in mmol/mol (26.0) plus uploaded panel **4.53 %** — intentional but easy to misread.
9. **IDL vs hero divergence** — API IDL top strong signal is **Vascular Inflammation Risk**; hero uses homocysteine narrative (resolution logic working, but backend signals mixed).
10. **Some raw-ish marker labels** — e.g. **“Apob Apoa1 Ratio”**, **“dhea s”** in the all-markers grid (upload naming, not snake_case slugs).

---

## 4. Blockers (must fix before any external user sees this)

| Item | Evidence |
|------|----------|
| **Stale / incompatible result contract** | Banner on page; API `result_versioning.compatible: false`, `render_blockers: ["clinician_report_v1"]` |
| **B12-associated pattern title vs in-range B12** | Visible under “Primary finding and why” |
| **Marker-count trust contradiction** | 79 vs 9 of 9 without explanation |
| **Pattern groups missing on incompatible snapshot** | Body overview fallback copy |

**Resolved vs `b2dfa0c4` (no longer blockers):** Layer B/C, narrative compiler subtitle, raw `**markdown**`, lifestyle slugs, chain_001 in default scroll, Actions hub empty state, “Wave 1”, governance **“AI-per”** typo.

---

## 5. Important but non-blocking issues (HIGH / MEDIUM)

- **HIGH:** Regenerate UX is correct but this analysis should be regenerated before beta/UAT sign-off.
- **HIGH:** Evidence-chain wording only behind “Show technical detail” (good gating); chains like “Homocysteine High → Raised homocysteine pattern” appear when expanded.
- **MEDIUM:** TC/HDL ratio card notes units/range need review.
- **MEDIUM:** “Limited reliability” on blood sugar (1 of 2 markers) alongside **100/100 Strong** — numerically correct but cognitively odd.
- **MEDIUM:** Hero lists **“Homocysteine, Vitamin B12, Folate, Transferrin”** under vascular-risk copy — clinically busy.

---

## 6. Polish / backlog (LOW)

- Marker grid label normalisation (Apob/Apoa1, dhea s, etc.).
- “Consider discussing **Repeat homocysteine**” — awkward phrasing.
- Uploaded-panel section duplication for HbA1c / TC:HDL (by design, but dense).

---

## 7. Evidence / screenshots captured (session machine)

Saved under (local Cursor browser screenshots path from session):

`c:\Users\abroa\AppData\Local\Temp\cursor\screenshots\`

| File | What it shows |
|------|----------------|
| `uat-fdf9bc74-hero.png` | Hero, governance strip, action buttons |
| `uat-fdf9bc74-stale-banner.png` | Stale-format warning + regenerate CTA |
| `uat-fdf9bc74-actions-hub.png` | Actions hub with dated analysis + follow-ups |

Authenticated API fetch: `GET /api/analysis/result?analysis_id=fdf9bc74-70db-4d36-be8a-8c709c654df8` → `automation_bus/_uat_fdf9bc74.json`.

---

## 8. Specific text examples that should be rewritten (samples)

- Stale banner body (accurate but alarming on every visit until regenerate).
- **“B12-associated pattern”** → should match counter-evidence (e.g. “Homocysteine elevation — B12 less likely on this panel”).
- **“Most relevant area: Vascular Inflammation Risk”** when homocysteine is the declared lead.

---

## 9. Suspected data / unit / status defects (visible or not verified)

| Concern | Browser observation |
|---------|---------------------|
| Haemoglobin 144 **g/L** vs range in **g/L** | **Verified** — range 130–175 g/L (old g/dL defect not reproduced). |
| Haematocrit **0.4 L/L** | **Verified** — range 0.35–0.48 L/L. |
| **ALT** low vs **critical** status | **Not verified** this pass. |
| **Transferrin** low vs narrative | **Visible:** “transferrin **2 g/L · Critical**” in driver list. |
| **HbA1c** % vs mmol/mol range | **Both shown** — analytical 26.0 mmol/mol; uploaded 4.53 %. |
| **Free testosterone** unknown | Present in marker grid; not hero-relevant this run. |
| **BMI** 53.4593 | **No “BMI”** match — **not verified** on page text this session. |

---

## 10. LC-S4 / LC-S5 surface checklist (browser)

| Surface | Visible? | Location / notes | Readability / leakage |
|--------|----------|------------------|------------------------|
| **Governance / mode strip** | **Yes** | Top strip | “AI-personalised narrative is not active” — **fixed** from “AI-per”. |
| **Hero section** | **Yes** | Primary finding card | Homocysteine-primary; vascular subline remains. |
| **Body overview** | **Yes** | Mid-page card | Alcohol → homocysteine plain-English bridge **without slugs**. |
| **Health systems** | **Yes** | Three domain cards | CV expanded shows human chip roles (“Used in this score”). |
| **Confidence** | **Yes** | “How confident is this read” | Good uncertainty copy; **9/9 vs 79** dissonance. |
| **Patterns across body** | **Yes** | Methylation pathway section | Coherent homocysteine thread. |
| **Marker evidence** | **Yes** | Drivers + 79-marker grid | Mostly human labels; some upload naming oddities. |
| **Next steps** | **Yes** | Direction and follow-up | Sensible clinician framing; MMA callout. |
| **Actions (section + page)** | **Yes** | `/actions` | **5 items** — **fixed** from prior empty state. |
| **Advanced / clinician** | **Collapsed** | Bottom journey | “Show” gates present. |

---

## 11. Legacy “Metabolic / Cardiovascular focus … summarise structured signals …” strings

**Not found** on results (same as `b2dfa0c4` run). **No blocker** for that specific legacy phrasing on this run.

---

## 12. Internal-language leakage table (representative)

| Term / pattern | Classification |
|----------------|----------------|
| **Layer B** | **Absent** |
| **Layer C** | **Absent** |
| **deterministic** / **Deterministic** | **Absent** (default view) |
| **narrative compiler** | **Absent** |
| **deterministic arbitration**, **governed capacity score** | **Absent** |
| **`cardiovascular_4_biomarkers`** (system slug) | **Absent** |
| **`alcohol_intake_…_coherence`** style slug | **Absent** |
| **`chain_001` / `chain_002`**, `mcv evidence; vitamin_b12` | **Hidden** unless technical detail expanded |
| **signal** (hero context) | **Borderline** — less problematic without other pipeline language |
| **signal_id**, **root_cause_v1**, **runtime**, **manifest**, **legacy_v1**, **payload** | **Not observed** in page text scan |
| **compiler** (word “compiler”) | **Absent** |
| **governed** | **Absent** in consumer copy |
| **Wave 1** | **Absent** — replaced by “Your health systems” |
| **score_contributor** (visible chip text) | **Absent** — shows “Used in this score” |
| **analysis UUID** | **Present** when technical detail on |

---

## 13. Clinical / content coherence (against panel content)

- **Why homocysteine leads:** Explained in body overview, methylation section, and next steps (MMA).
- **B12 in range, cause not proven:** **Well handled** in evidence bullets; **undermined** by **“B12-associated pattern”** heading.
- **Avoid claiming exact cause:** Mostly cautious language.
- **Alcohol / MCV / homocysteine in plain English:** Partially improved; no slug leakage.
- **Alarmism / unsupported causality:** Generally restrained; stale banner and transferrin “Critical” chip are the main trust risks.
- **Next steps / no meds:** No supplement/medication prescribing observed; MMA with clinician is appropriate framing.

---

## 14. Visual hierarchy and journey

- **Most important finding:** **Clearer than `b2dfa0c4`** — homocysteine is the headline.
- **Stale banner:** Dominates trust before user reads results — appropriate warning, bad for demo unless regenerated.
- **Page length:** Long but structured; expandables work.
- **Domain cards:** Useful structure; reliability badges are informative.
- **Actions journey:** Results → Actions hub **consistent** (no empty hub).

---

## 15. Recommendation: ready for controlled external testing?

**No** — regenerate this analysis first, then re-run UAT. Structural/copy hardening is much better; this snapshot is explicitly **incompatible** with the current results contract.

---

## 16. Recommended next work package (suggested)

**Title:** “Results retail hardening — stale regeneration, B12 heading, marker-count copy”

**Objective:**

1. **User / ops:** Regenerate `fdf9bc74` (or re-upload panel) and re-UAT on the new `analysis_id`.
2. **Engineering:** Fix B12-associated hypothesis title when B12 counter-evidence is present.
3. **Engineering:** Reconcile **79 markers analysed** vs **9 of 9 expected for interpretation** in UI copy.
4. **Engineering:** Confirm stale-banner + regenerate flow clears `render_blockers` for `clinician_report_v1`.

---

## 17. Reproduction notes (browser)

1. Log in on `/login` with `test-user3@example.com` / `Subaru@555`.
2. Wait for **Log out** in header.
3. Open `http://localhost:3000/results?analysis_id=fdf9bc74-70db-4d36-be8a-8c709c654df8`.
4. Wait for full render (~14k chars body text).
5. Toggle **Show technical detail** for metadata strip and evidence chains.
6. Expand **Cardiovascular health → More detail** for subsystem marker chips.
7. Visit **`/actions`** after session stabilises (hard navigation may briefly show **Sign in** until hydration).

---

## 18. Delta vs `b2dfa0c4` (headline comparison)

| Area | `b2dfa0c4` (2026-05-12) | `fdf9bc74` (this run) |
|------|-------------------------|------------------------|
| Pipeline vocabulary | Widespread blockers | **Largely cleared** |
| Hero story | Vascular vs homocysteine conflict | **Homocysteine-led** (minor vascular subline) |
| Actions hub | Empty | **Populated (5 items)** |
| Health system chips | `score_contributor` visible | **“Used in this score”** |
| Governance strip | “AI-per” typo | **“AI-personalised”** |
| Stale contract | Not reported | **New — regenerate required** |
| Overall verdict | Not launch-ready | Not launch-ready (stale snapshot + residual copy issues) |

---

## API snapshot (key fields)

```json
{
  "status": "completed",
  "biomarker_count": 79,
  "result_versioning": {
    "compatible": false,
    "result_status": "incompatible",
    "launch_user_behaviour": "display_stale_warning",
    "user_message": "This saved result cannot be displayed with the current results page contract.",
    "render_blockers": ["clinician_report_v1"],
    "regeneration_available": true
  },
  "idl_strong_signal": "Vascular Inflammation Risk",
  "primary_concern": "Homocysteine Elevation Context: warrants attention on this panel",
  "hypothesis_title": "B12-associated pattern",
  "pattern_groups_count": 0
}
```
