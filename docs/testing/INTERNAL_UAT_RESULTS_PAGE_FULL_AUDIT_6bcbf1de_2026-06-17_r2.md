# Internal UAT Results Page Full Audit — 6bcbf1de (Revision 2)

**Date:** 2026-06-17  
**Auditor role:** healthiq-qa-uat (investigation only)  
**Mode:** Read-only — no code, commits, or branches changed  
**Prior audit:** [Revision 1 (2026-06-16)](INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_6bcbf1de_2026-06-16.md)  
**Fix sprint:** `INTERNAL-UAT-RESULTS-TRUST-HARDENING-1` (`b55e6e7`, `16297cf`, closure `12f1a7a`)

---

## Executive verdict

| Question | R1 (pre-fix) | R2 (this run) |
|----------|--------------|---------------|
| **Structurally working?** | Yes | **Yes** — full journey renders; API 200; versioning stable |
| **Coherent for internal validation?** | Yes, with reservations | **Yes** — homocysteine-led story is coherent; HIGH trust contradictions largely resolved |
| **Retail / external-ready?** | No | **Closer, not yet** — residual MEDIUM copy/presentation items remain |
| **Unsafe or materially misleading?** | No BLOCKER | **No BLOCKER** |
| **Trust-damaging at HIGH level?** | Yes (6 HIGH) | **No** — prior HIGH items fixed or downgraded |

**Overall:** **PASS** for internal product validation (upgraded from **PASS WITH RESERVATIONS**). Suitable for continued internal UAT and staged retail polish; not yet external-launch ready without MEDIUM backlog clearance.

**Defect delta:** BLOCKER **0 → 0** · HIGH **6 → 0** · MEDIUM **6 → 5** · LOW **3 → 3**

---

## Test environment

| Item | Value |
|------|--------|
| **Branch** | `main` |
| **Commit** | `4c4b3d541a2ef5ac1a3699eae3a63182d46ef26b` |
| **Frontend URL** | `http://localhost:3000/results?analysis_id=6bcbf1de-d97f-4a1c-9556-e3a6e0625fd1` |
| **Backend URL** | `http://localhost:8000` |
| **Analysis ID** | `6bcbf1de-d97f-4a1c-9556-e3a6e0625fd1` |
| **Account** | `test-user3@example.com` (session: **Log out** visible) |
| **Browser** | Cursor IDE browser (Chromium) |
| **Timestamp** | 2026-06-17 session |

**Evidence artefacts:**

- API (refreshed): `automation_bus/_uat_6bcbf1de_result_api.json`
- Screenshots (R2): `docs/testing/screenshots/uat_6bcbf1de_results_page/06_r2_hero_body_overview.png`, `07_r2_primary_finding.png`
- Screenshots (R1): `docs/testing/screenshots/uat_6bcbf1de_results_page/01–05_*.png`
- Regression tests: `frontend/tests/lib/resultsTrustHardening.test.ts`, `backend/tests/regression/test_internal_uat_results_trust_hardening.py`

---

## Versioning / compatibility confirmation

| Check | Result |
|-------|--------|
| `GET /api/analysis/result` | **HTTP 200** (authenticated) |
| `result_versioning.compatible` | **`true`** |
| `result_status` | **`current`** |
| `render_blockers` | **`[]`** |
| Stale/incompatible banner | **Absent** |
| `clinician_report_v1` | **Present** |
| `narrative_report_v1` | **Present** |
| `clusters` | **3** |
| `biomarkers` | **79** |

False incompatible banner remains **resolved**.

---

## Fix verification summary (IUAT-001 – IUAT-006)

| ID | R1 issue | R2 status | Evidence |
|----|----------|-----------|----------|
| **IUAT-001** | "B12-associated pattern" vs B12 counter-evidence | **FIXED** | API `hypotheses[0].title` = `Homocysteine-related pattern`; UI shows same; no `B12-associated` in page text |
| **IUAT-002** | "Pattern groups are not available" with 3 clusters | **FIXED** | UI: `Detailed pattern groups are hidden in this view. 3 pattern summaries are covered in the sections below.` |
| **IUAT-003** | 79 markers vs 9/9 confusion | **FIXED** | Toolbar: `79 uploaded markers`; data quality: `9 of 9 key markers available for this headline interpretation` |
| **IUAT-004** | `**Cardiovascular 4 Biomarkers**` markdown leakage | **FIXED (retail UI)** | UI scrubbed — no `Cardiovascular 4`, no `**`, no `analytical model`. **Note:** persisted API `body_overview` still contains raw compiler text (presentation-layer scrub only). |
| **IUAT-005** | Homocysteine hero + unexplained vascular subline | **FIXED** | Hero lead unchanged; subline now explicit: `Broader system context: Vascular Inflammation Risk` |
| **IUAT-006** | Transferrin **Critical** in driver band | **PARTIAL → MEDIUM** | Band chip: `Needs review` (improved). Subline still: `Value sits in the Critical range for this marker on your panel.` because `interpretation` is generic (`Scored using lab reference range`) and `oneLineMarkerInterpretation` falls back to `humanizeStatus`. |

**Automated regression:** 7/7 frontend + 5/5 backend trust-hardening tests **pass** on current `main`.

---

## API-to-UI mapping (R2)

| UI section | API source | R2 status | Notes |
|------------|------------|-----------|-------|
| `79 uploaded markers` | `biomarkers.length` | OK | Label clarified |
| Hero title | `resolveHeroPrimaryStory()` + page1 | OK | Homocysteine-led |
| Hero system context | IDL `retail_display_label` | OK | Explicit "Broader system context" line |
| Body overview prose | `narrative_report_v1.body_overview` + `scrubConsumerRetailNarrative` | OK (UI) | API raw still has internal names; scrub at render |
| Pattern-groups note | `clusters[]` + `showPatternGroupBuckets` | OK | Hidden-vs-unavailable distinction correct |
| Hypothesis title | `clinician_report_v1…hypotheses[0].title` | OK | Neutralised at compile (`report_compiler_v1`) |
| Data quality strip | `panel_completeness_*` | OK | "Key markers" wording |
| Driver band — Transferrin | `biomarkers[]` + `formatConsumerDriverBandStatusLabel` | Partial | Chip improved; interpretation line still says Critical |
| Stale banner | `result_versioning` | OK | Hidden |

---

## Full page walkthrough (R2 highlights)

### Hero / primary finding

- **Primary finding:** `Raised homocysteine pattern: warrants attention on this panel` — unchanged, correct.
- **Broader system context:** `Vascular Inflammation Risk` — now labelled explicitly; no longer reads as a competing primary headline.
- Driver markers listed (Homocysteine, B12, Folate, Transferrin) — clinically busy but data-backed.

### Body overview

- Compiled narrative renders with consumer scrub: `Raised homocysteine pattern` (not raw `homocysteine elevation context` slug).
- Lifestyle appendix no longer shows `analytical model` phrasing in UI.
- Pattern-groups box correctly states groups are **hidden**, not **unavailable**.

### Primary finding and why

- Hypothesis heading: **Homocysteine-related pattern** — aligns with B12 counter-evidence bullet ("B12 appears clearly within range…").
- Evidence structure (supports / complicates / clarify) unchanged and appropriate.

### Data quality

- `9 of 9 key markers available for this headline interpretation` — reconcilable with `79 uploaded markers` without engineering knowledge.

### What's driving this

- Homocysteine: `Above range` — correct.
- Transferrin: `2 g/L · Needs review` with subline still referencing **Critical range** — residual trust friction (IUAT-006).

### Unchanged MEDIUM / LOW items (from R1)

| ID | Severity | Issue | R2 |
|----|----------|-------|-----|
| IUAT-006 | **MEDIUM** (downgraded) | Transferrin Critical subline in driver band | Open |
| IUAT-008 | MEDIUM | Mojibake in persisted `body_overview` (`` em-dash) | Open in API; not observed in scrubbed UI |
| IUAT-009 | MEDIUM | Raw upload labels (`dhea s`, `(venous)` suffixes) | Open |
| IUAT-010 | MEDIUM | Blood sugar 100/100 + Limited reliability | Open |
| IUAT-011 | MEDIUM | "Consider discussing Repeat homocysteine" grammar | Open |
| IUAT-012 | MEDIUM | Governance strip technical copy | Open (internal UAT acceptable) |
| IUAT-013 | LOW | Duplicate "What's working well" headings | Open |
| IUAT-014 | LOW | Free testosterone % score 0 display | Open |
| IUAT-015 | LOW | Long scroll / IA | Open |

**Counts:** BLOCKER **0** · HIGH **0** · MEDIUM **5** · LOW **3**

---

## Console / network

- No stale/incompatible banner or blocking fetch errors observed during authenticated load.
- Brief hydration flicker (`Sign in` → `Log out`) during load — same as R1; acceptable.

---

## Comparison to Revision 1

| Metric | R1 | R2 |
|--------|----|----|
| Verdict | PASS WITH RESERVATIONS | **PASS** |
| HIGH defects | 6 | **0** |
| Trust headline contradictions | B12 title, pattern unavailable, marker count | **Resolved** |
| Internal vocabulary in retail surfaces | Cardiovascular 4, analytical model, markdown | **Scrubbed at UI** |
| Hero hierarchy | Dual competing headlines | **Explicit lead + broader context** |
| Transferrin presentation | Critical chip | Needs review chip; Critical subline remains |

---

## Recommended next sprint

1. **IUAT-006 finish:** Extend `oneLineMarkerInterpretation` (or transferrin interpretation enrichment) so driver-band sublines use consumer labels consistent with the chip (`Below range` / `Needs review`), not `Critical`.
2. **Compiler scrub (optional):** Move IUAT-004 / IUAT-007 / IUAT-008 fixes into `narrative_report_compiler_v1` so API exports match retail UI without relying solely on frontend scrub.
3. **Retail polish backlog:** IUAT-009–012 display-name normalisation, next-steps grammar, governance strip product decision.
4. **Re-UAT:** After IUAT-006 subline fix, spot-check `6bcbf1de` plus one **new** upload to confirm compile-time hypothesis neutralisation on fresh analyses.

---

## Do not fix yet (without broader decision)

- Hiding governance strip without product sign-off
- Changing homocysteine/vascular **scoring** or signal activation
- Frontend-side severity **inference** beyond render-only mapping
- Dummy clinician content or compatibility bypasses

---

## Screenshot index (R2)

| File | Section |
|------|---------|
| `06_r2_hero_body_overview.png` | Toolbar, governance strip, marker count |
| `07_r2_primary_finding.png` | Page header / journey intro (top of scroll) |

---

## Final recommendation

1. **Trust hardening sprint:** **Successful** — all six R1 HIGH items addressed in UI and/or compile path; regression tests green.
2. **Internal validation:** **Proceed** — page is structurally sound, versioning correct, and retail trust contradictions are materially reduced.
3. **External readiness:** **Hold** until IUAT-006 subline and MEDIUM retail polish backlog are cleared.
4. **No code changes** were made during this audit run.
