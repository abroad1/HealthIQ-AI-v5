# Post-FE-R6A Fresh UAT Investigation — d8cfe1a8

**Auditor:** Cursor (browser + authenticated API)  
**Scope:** Investigate only — no code changes  
**Compared prior fresh run:** `f2dcb58f-e816-4ff6-9011-e93c5d48b82c` (2026-05-24 21:07 UTC)

---

## 1. Executive verdict

| Question | Answer |
|----------|--------|
| **Is the lead finding change explainable?** | **Yes.** The new run lost **canonical mapping for homocysteine** (and 13 other markers). Homocysteine remains in uploaded fidelity as `unmapped_homocysteine_(venous)*` at **16.23 µmol/L** but is **not** in the scored `biomarkers` array. With homocysteine signals absent, **`signal_total_cholesterol_high`** becomes the governed lead — same elevated total cholesterol (5.26 mmol/L) as the prior run. |
| **Likely correct, questionable, or display bug?** | **Likely correct for the data the engine actually scored**, but **questionable as a user-facing story** because narrative still discusses homocysteine/methylation while the lead biomarker is total cholesterol and homocysteine is unmapped. This is a **pipeline/mapping + narrative alignment** issue, not a random frontend pick. |
| **Is frontend showing the selected lead correctly?** | **Mostly yes** for page1/clinician authority: hero title and primary-finding section use **Total Cholesterol High** / **Total cholesterol elevation in atherogenic lipid panel context**, matching `clinician_report_v1.sections.page1` and `narrative_report_v1.retail_summary`. **Partial split-brain:** hero subline uses first enabled IDL (**Vascular Inflammation Risk**), and patterns still surface **Methylation pathway pattern** — both from backend IDL, not invented in UI. |
| **Why does prose still feel thin/mechanical?** | **Mixed:** (1) compiler templates repeat the same lead sentence; (2) lead hypothesis copy is signal/evidence-chain oriented (“signal fired, anchoring governed… WHY”); (3) biomarker `interpretation` for the lead is still **Scored 30.5/100** despite general education existing in DTO; (4) homocysteine-specific governed WHY cannot run when the marker is unmapped; (5) hero body pulls IDL vascular-risk copy, not lipid-led depth. |
| **Issue class** | **Mixed — primarily backend/pipeline (mapping regression) + compiler/narrative alignment; secondary frontend presentation limits; KB-WAVE content deferred but not the main blocker on this run.** |

**Bottom line:** Do **not** treat the lead change as a display bug. Treat it as **expected arbitration given unmapped homocysteine**, then fix **why this run mapped fewer markers** before KB-WAVE-1.

---

## 2. Page inspected

| Field | Value |
|-------|--------|
| **URL** | `http://localhost:3000/results?analysis_id=d8cfe1a8-c0e7-4f8b-99ea-8152b05f1579` |
| **analysis_id** | `d8cfe1a8-c0e7-4f8b-99ea-8152b05f1579` |
| **Login** | `test-user3@example.com` / `Subaru@555` |
| **Date/time** | 2026-05-25 ~08:31 UTC (browser); result `created_at` **2026-05-24T22:28:21Z** |
| **Browser method** | Cursor IDE browser — accessibility snapshot + CDP `Runtime.evaluate` |
| **API/DTO method** | `POST /api/auth/login` → `GET /api/analysis/result?analysis_id=…` (Bearer token) |
| **Git / runtime** | `main` @ `9bfa43d`; backend and frontend returned 200; **not restarted** for this audit |
| **Evidence files** | `automation_bus/_uat_post_r6a_d8cfe1a8.json`, `_uat_post_r6a_f2dcb58f.json`, `_uat_post_r6a_trace.json` |

---

## 3. Current visible result summary

Exact or near-exact visible copy from the rendered page (post-FE-R6A).

### Primary hero

- **Title:** `Total Cholesterol High: also stood out on this panel`
- **Subline:** `Main system context: Vascular Inflammation Risk`
- **Severity chip:** `Watch`
- **Hero body (excerpt):** `Accumulating vascular-risk signals warrant cardiometabolic review and lifestyle action. A pattern combining inflammation and homocysteine signals associated with vascular risk Crp, Nlr, Sii`

### Body overview (first paragraph)

`Your results highlight total cholesterol high as the main pattern to discuss first, alongside the wider marker and domain context below.`

(Followed by questionnaire alcohol → homocysteine/folate bridge, lifestyle context line, Cardiovascular 4 Biomarkers weighting, related systems list, stable-systems framing.)

Also visible: `Pattern groups are not available for this result yet — the sections below still walk through your markers and findings.`

### What's working well

`Not every system group shows strain on this panel. The patterns below look broadly stable or well-regulated, based on the same structured engine that flags concerns.`

Example row: `Hematological` — `On this panel, markers grouped under this system look broadly within expected ranges.`

Bridge: `The headline interpretation above focuses on Cardiovascular. Several other groups still look broadly in-range—this helps place concerns in context rather than suggesting the whole panel is off track.`

### Primary finding and why

- **Heading content:** `Total cholesterol elevation in atherogenic lipid panel context`
- **Bridge:** `Lead pattern on this panel: Total Cholesterol High: also stood out on this panel. The hypothesis below explains how that pattern is being interpreted from your markers.`
- **Evidence lines:** `A total-cholesterol-high signal fired, anchoring governed total-cholesterol WHY on this run. (related markers: Total Cholesterol)` / `Total cholesterol is above the lab reference range, supporting an elevation pattern. (related markers: Total Cholesterol)`

### Uncertainty

Section present (`Why this lead won and uncertainty`); trust strip visible. Technical ranking hidden unless “Show technical detail” enabled (FE-R6A default).

### Patterns across your body

`Methylation pathway pattern` — `Homocysteine elevation with larger red-cell index suggesting one-carbon / marrow context` — `Watch`

`WHY THIS MATTERS` — `This pattern links nutrient–cofactor networks to vascular and blood-cell maturation questions that deserve coherent follow-up, not a single-marker snapshot.`

`SUPPORTING MARKERS` — `Mcv, Vitamin B12, Folate, Ggt`

### Lead biomarker expansion (Total Cholesterol / Cholesterol card)

- **What this result means now:** `Scored 30.5/100`
- **How it connects:** `This marker aligns more closely with Cardiovascular Health Pattern than with the highlighted Hematological Health Pattern pattern.`
- **Contribution:** `For this analysis, the marker total_cholesterol appears in the following pattern grouping(s): "Cardiovascular Health Pattern". This describes how markers were grouped for review only.`
- **Education:** `Total cholesterol is the sum of cholesterol carried in the blood across major particle types…` (general marker education present)

### What to do next

`NEXT STEPS` as separate lines (improved vs pre-FE-R6A blob):

- `Discuss these findings with a clinician who knows your history.`
- `Monitor trends on the cadence your clinician recommends.`
- `Repeat priority markers when your clinician advises retesting.`
- `Consider discussing Repeat HbA1c with your clinician.`
- … TSH, TyG-related markers …

`Tests to discuss with your clinician` — e.g. `Fasting glucose with insulin` with rationale paragraph.

No visible `No separate checklist of follow-up lines was packaged` fallback (FE-R6A removed).

---

## 4. Lead finding trace

| Layer | Field/source | Value observed (d8cfe1a8) | Notes |
|-------|----------------|---------------------------|-------|
| **Uploaded markers** | Mode A / fidelity | Homocysteine **16.23 µmol/L** under `unmapped_homocysteine_(venous)*`; total cholesterol **5.26 mmol/L** mapped | 19 `unmapped_*` keys on this run vs 0 scored homocysteine |
| **Biomarker scoring** | `biomarkers[]` | **63** markers; lead abnormal: `total_cholesterol` score **0.305** elevated; `transferrin` **0.05** critical; `mcv` elevated | **No `homocysteine` row** (prior run had it) |
| **Consumer domains** | `consumer_domain_scores` | `wave1_cardiovascular`: score **0.874**, band **strong**, signals **`signal_total_cholesterol_high` only** | Prior run also had `signal_homocysteine_elevation_context`, `signal_homocysteine_high` |
| **System/cluster outputs** | `clusters` | `cardiovascular_4_biomarkers` mild; hematological normal | Same cluster IDs as prior run |
| **Arbitration** | `primary_driver_system_id` / meta | **`cardiovascular_4_biomarkers`** | Same driver family both runs |
| **Clinician report** | `sections.page1` | **`Total Cholesterol High: also stood out on this panel`**; mode `distinct_lead`; top hypothesis line for TC atherogenic context | Prior: `Homocysteine Elevation Context: warrants attention on this panel` |
| **Root cause** | `sections.root_cause` | `signal_total_cholesterol_high`, confidence **0.9**, hypothesis **`tc_atherogenic_panel_context_v1`** ranked #1 | Prior run homocysteine-root-cause package path (not re-exported in trace script) |
| **IDL** | `interpretation_display_layer_v1.records` | First **enabled** record: **`ph_vascular_hcy_inflammation_v1`** → retail **Vascular Inflammation Risk** (watch); patterns section also **Methylation pathway pattern** (enabled, priority 10) | Insulin Resistance Phenotype exists but `enabled_for_frontend: false` |
| **Narrative report** | `narrative_report_v1` | `retail_summary` centres **total cholesterol high**; `lead_narrative` TC atherogenic; compiler meta `lead_signal_id`: **`signal_total_cholesterol_high`**; skipped: **`lead_narrative_no_matching_signals`** | Assets: `retail_summary_from_idl`, `lc_s3_payload_primary_assembly`, lifestyle bridge |
| **Frontend** | Hero + sections | Title = page1 concern (**TC High**); context = IDL **Vascular Inflammation Risk**; primary section = TC hypothesis; patterns = **Methylation** | Matches `resolveHeroPrimaryStory` + `pickPhenotypeLabel` precedence in `resultsPageLayout.ts` |

---

## 5. Comparison with previous fresh result

| Item | Previous f2dcb58f | Current d8cfe1a8 | Difference | Likely reason |
|------|-------------------|------------------|------------|---------------|
| **Lead finding** | Homocysteine Elevation Context | Total Cholesterol High | **Changed** | Homocysteine **unmapped** → homocysteine signals never fire |
| **Lead biomarker(s)** | `homocysteine` (scored 16.23 µmol/L elevated) | `total_cholesterol` (5.26 mmol/L elevated) | **Changed** | Scored-set difference, not different TC value |
| **Top abnormal markers** | homocysteine, transferrin, mcv, total_cholesterol, tc_hdl_ratio (unscored) | total_cholesterol, transferrin, mcv (no homocysteine) | Homocysteine dropped from scored set | Canonical mapping regression on upload |
| **Marker count** | **77** scored | **63** scored | **−14** | All 14 names only in f2: `homocysteine`, `active_b12`, `apoa1`, `apob`, `vitamin_b12`, `vitamin_d`, `zinc`, `tsh`, `creatinine`, `rbc`, `lipoprotein_a`, `urea_creatinine_ratio`, `apob_apoa1_ratio`, `corrected_calcium` |
| **Domain scores** | CV signals: homocysteine + TC | CV signals: **TC only** | Fewer active signals | Unmapped markers cannot activate governed signals |
| **Root-cause hypothesis** | Homocysteine-led context (prior UAT) | `tc_atherogenic_panel_context_v1` | **Changed** | `signal_total_cholesterol_high` wins |
| **Pattern card** | Methylation pathway pattern (watch) | Methylation pathway pattern (watch) | **Same IDL record** | IDL still enabled; still references B12/folate though several B-vitamin markers unmapped |
| **Narrative richness** | Homocysteine-centred retail_summary | TC-centred retail_summary + homocysteine lifestyle bridge still in body_overview | **Shifted lead copy; leftover homocysteine prose** | Compiler lifestyle bridge independent of mapping |
| **wave1_aligned_drivers** | `homocysteine`, `total_cholesterol`, `transferrin` | `total_cholesterol`, `transferrin` | Homocysteine removed | Backend meta aligns with scored drivers |

**Uploaded values:** Total cholesterol, transferrin, mcv, crp match between runs where both are scored — this is **not** a new panel chemistry story; it is **interpretation authority shifting because fewer markers mapped**.

---

## 6. Prose quality diagnosis

| Prose block | Exact visible prose excerpt | Source field | Quality issue | Fix type |
|-------------|----------------------------|--------------|---------------|----------|
| Hero title | `Total Cholesterol High: also stood out on this panel` | `clinician_report_v1.sections.page1.primary_concern` | Template-like, duplicated elsewhere | backend compiler prose |
| Hero context | `Main system context: Vascular Inflammation Risk` | First enabled IDL `retail_display_label` (`ph_vascular_hcy_inflammation_v1`) | **Misaligned with TC lead** (homocysteine-linked IDL) | backend compiler + IDL lead authority alignment |
| Hero body | `Accumulating vascular-risk signals… homocysteine signals… Crp, Nlr, Sii` | IDL `why_it_matters` + `subtitle` via `buildIdlLedHeroSummary` | Reads as different lead than title | backend/compiler IDL single-lead policy |
| Body overview | `Your results highlight total cholesterol high… homocysteine because alcohol intake…` | `narrative_report_v1.body_overview` | Homocysteine narrative **without scored homocysteine** | backend compiler + mapping fix |
| Body overview | `Pattern groups are not available for this result yet` | Frontend / missing pattern-group DTO | Empty buckets replaced by message — better than “0/0/3” but still thin | mixed (data + presentation) |
| Retail hero summary | (not shown as separate Summary card post-FE-R6A) | `narrative_report_v1.retail_summary` | Duplicative sentences in DTO | backend compiler prose |
| Primary finding | `A total-cholesterol-high signal fired, anchoring governed total-cholesterol WHY on this run.` | Root-cause / page1 evidence assembly | Mechanical, internal cadence | backend compiler prose + KB-WAVE governed WHY surfacing |
| What's working well | `markers grouped under this system look broadly within expected ranges` | Balanced systems template | Generic reassurance | backend compiler prose |
| Patterns | `Methylation pathway pattern` … `Homocysteine elevation with larger red-cell index` | IDL `ph_one_carbon_homocysteine_macrocytosis_v1` | **Secondary pattern competes with TC lead**; B12 unmapped | IDL/pattern copy gap + mapping |
| Lead marker expansion | `Scored 30.5/100` | `biomarkers[].interpretation` | Scoring line dominates “means now” | missing KB-WAVE lipid WHY on interpretation; expected backlog partially |
| Lead marker education | `Total cholesterol is the sum of cholesterol carried…` | `biomarker_educational_explainer` | Generic education only — not “why elevated for you” | missing Knowledge Bus asset / governed WHY |
| Next steps | `Consider discussing Repeat HbA1c…` while lead is TC | `confirmatory_tests` + `next_steps_narrative` | Test suggestions **not tightly coupled** to TC lead | backend compiler / root-cause coverage gap |
| What's driving this | `Total Cholesterol 5.26 mmol/L · Elevated Scored 30.5/100` | `meta.wave1_aligned_drivers` | Correct drivers; still score-heavy | expected until KB-WAVE |

---

## 7. Biomarker expansion diagnosis

| Biomarker | Visible expansion | interpretation present? | contribution_context present? | educational_explainer present? | Likely reason for thinness |
|-----------|-------------------|-------------------------|------------------------------|-------------------------------|----------------------------|
| **Total cholesterol (lead)** | Scored 30.5/100 + cluster membership + general education paragraph | Yes (scoring-only in “means now”) | **Yes** (cluster_membership) | **Yes** (generic total cholesterol education) | Governed **lipid WHY** not bound to `interpretation`; UI renders what DTO sends |
| **Transferrin (supporting, critical)** | `Value sits in the Critical range for this marker on your panel.` (driver strip); not fully expanded in audit | Yes (scoring-only) | **No** | **No** | Missing DTO enrichment; signal present (`signal_transferrin_low`) but no retail explainer |
| **Mcv (supporting, methylation pattern)** | Listed under Methylation pattern; not expanded in audit | Yes (scoring-only) | Not checked in UI | Not checked | Pattern uses MCV; expansion not lead-focused |

**UI capability:** Post-FE-R6A, when DTO includes education and contribution (as with total cholesterol), the UI **does** render “How it connects” and education blocks. Thinness is **not** because expansion is broken — it is because **interpretation** remains scoring text and governed WHY is not packaged for the lead.

**Homocysteine:** **Not in biomarker grid** on d8 — cannot expand; value only under uploaded fidelity unmapped key. Explains prior-run vs current-run lead change more than FE-R3/FE-R6A regression.

---

## 8. Knowledge asset surfacing check

| Asset / layer | Status on d8cfe1a8 |
|-------------|---------------------|
| **`pkg_homocysteine_elevation_context`** (estate KB-S49) | Present in package estate; **not activatable** without mapped `homocysteine` |
| **`signal_homocysteine_elevation_context` / `signal_homocysteine_high`** | **Absent** from `active_signal_ids` (mapping) |
| **`signal_total_cholesterol_high`** | **Active**; root-cause hypotheses `tc_atherogenic_panel_context_v1` surfaced in UI |
| **IDL `ph_vascular_hcy_inflammation_v1`** | Enabled; drives hero context line |
| **IDL `ph_one_carbon_homocysteine_macrocytosis_v1`** | Enabled; drives Methylation pattern card |
| **IDL insulin resistance phenotype** | Present but **`enabled_for_frontend: false`** |
| **KB-WAVE lipid WHY packages** (e.g. `pkg_kb60_total_cholesterol_high_*`) | Exist on disk; **not visibly replacing** `interpretation` on consumer card |
| **Compiler assets resolved** | `retail_summary_from_idl`, `lifestyle_consumer_surface_lc_s13`, `lc_s3_payload_primary_assembly`, `clinician_synthesis_functional` |
| **Compiler skipped** | `lead_narrative_no_matching_signals` (noted in meta) |
| **Frontend** | Renders IDL patterns, page1 concern hero, wave1 drivers, confirmatory tests — **no fabrication** |

**Conclusion:** Knowledge Bus and IDL assets exist, but **marker mapping is the gate**. This run surfaces TC high root-cause and generic cholesterol education while homocysteine governed packages cannot fire.

---

## 9. Is the current page commercially good enough?

| Criterion | Assessment |
|-----------|--------------|
| **Score** | **6 / 10** post-FE-R6A (up from ~5.5–6 pre-cleanup on f2dcb58f, but **not** “wow”) |
| **Better than pre-FE-R6A** | Hero first; no “How to read” wrapper; no duplicate Summary card; cleaner next-steps list; no `Linked to …`; no raw unit-alignment string on cards; technical detail gated |
| **Still prototype-like** | Hero title vs context vs patterns tell **three different stories**; mechanical “signal fired” copy; scoring line as “what this means now”; homocysteine mentioned while unmapped; pattern-group placeholder message |
| **Would a paying user understand value?** | **Partially** — they see a clear **cholesterol** lead and lipid hypothesis, but may be confused by **vascular inflammation / methylation** headings and homocysteine lifestyle text without a homocysteine result card |
| **Blocks KB-WAVE-1?** | **Yes — recommend blocking until mapping regression is understood/fixed and lead/IDL/narrative use one authority.** Adding lipid WHY copy on top of unmapped homocysteine and split IDL would increase confusion |

---

## 10. Recommended next action

**Primary: run lead arbitration/scoring investigation — focused on canonical marker mapping / unmapped regression on fresh upload** (not PATTERN-C1; patterns render correctly).

**Secondary (after mapping stable): backend/compiler prose sprint** to align page1 lead, IDL hero record, and retail_summary to one authority and reduce template repetition.

**Do not yet: proceed to KB-WAVE-1** — governed WHY for lipids/homocysteine cannot land reliably while homocysteine and related markers are `unmapped_*` on upload.

**Do not: another frontend-only defect sprint** as the first move — FE-R6A fixes are visible; remaining issues trace to **DTO/compiler/mapping**.

### Why not other options

| Option | Why not first |
|--------|----------------|
| KB-WAVE-1 | Mapping gate blocks homocysteine signals; split-brain narrative |
| Frontend defect sprint | UI matches DTO; hero split-brain is coded precedence + backend IDL order |
| PATTERN-C1 | Methylation card renders safely; issue is coexisting secondary pattern vs lead |
| No action | Lead change is real, explainable, and user-visible — needs mapping forensics |

---

## Appendix — reproduction

1. Login as `test-user3@example.com`.
2. Open `http://localhost:3000/results?analysis_id=d8cfe1a8-c0e7-4f8b-99ea-8152b05f1579`.
3. API: `GET http://127.0.0.1:8000/api/analysis/result?analysis_id=d8cfe1a8-c0e7-4f8b-99ea-8152b05f1579` with Bearer token from `/api/auth/login`.
4. Compare biomarker name sets and `unmapped_*` keys in uploaded fidelity vs `f2dcb58f` payload.

*Investigation complete. No repository code modified.*
