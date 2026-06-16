# Internal UAT Results Page Full Audit — 6bcbf1de

**Date:** 2026-06-16  
**Auditor role:** healthiq-qa-uat (investigation only)  
**Mode:** Read-only — no code, commits, or branches changed

---

## Executive verdict

| Question | Assessment |
|----------|------------|
| **Structurally working?** | **Yes** — page loads, API 200, full journey renders, versioning fix verified |
| **Coherent enough for further internal validation?** | **Yes, with reservations** — homocysteine-led story is mostly intelligible; health-system cards and evidence blocks work |
| **Retail / external-ready?** | **No** — several HIGH-trust copy and hierarchy issues remain |
| **Unsafe or materially misleading?** | **No BLOCKER-class safety failures** — language is mostly cautious and non-diagnostic; severity labels are lab-grounded but sometimes alarmist in presentation |
| **Trust-damaging?** | **Yes at HIGH level** — B12 heading mismatch, pattern-group placeholder, marker-count dissonance, and internal vocabulary leakage undermine credibility |

**Overall:** **PASS WITH RESERVATIONS** for internal product validation. Suitable as a baseline for the next fix sprint, not for external users.

---

## Test environment

| Item | Value |
|------|--------|
| **Branch** | `main` |
| **Commit** | `211c188c20ebf68be077407e98e767eb936f823c` |
| **Frontend URL** | `http://localhost:3000/results?analysis_id=6bcbf1de-d97f-4a1c-9556-e3a6e0625fd1` |
| **Backend URL** | `http://localhost:8000` |
| **Analysis ID** | `6bcbf1de-d97f-4a1c-9556-e3a6e0625fd1` |
| **Account** | `test-user3@example.com` (session: **Log out** visible) |
| **Browser** | Cursor IDE browser (Chromium) |
| **Timestamp** | 2026-06-16 ~21:45 UTC session |

**Evidence artefacts:**

- API: `automation_bus/_uat_6bcbf1de_result_api.json`
- Screenshots: `docs/testing/screenshots/uat_6bcbf1de_results_page/` (01–05)
- Prior UAT: `docs/testing/UAT_results_page_analysis_fdf9bc74_2026-06-16.md`
- Versioning investigation: `docs/testing/INVESTIGATION_fdf9bc74_result_versioning_false_incompatible_2026-06-16.md`

---

## Versioning / compatibility confirmation

| Check | Result |
|-------|--------|
| `GET /api/analysis/result` | **HTTP 200** |
| `result_versioning.compatible` | **`true`** |
| `result_status` | **`current`** |
| `render_blockers` | **`[]`** |
| `stale_reasons` | **`[]`** |
| `user_message` | **`null`** |
| Stale/incompatible banner | **Absent** |
| Regenerate CTA | **Absent** |
| `clinician_report_v1` | **Present and populated** |
| `narrative_report_v1` | **Present** |
| `interpretation_display_layer_v1` | **Present** (11 records) |
| `consumer_domain_scores` | **Present** (3 Wave 1 domains) |
| `clusters` | **Present** (3) |
| `biomarkers` | **79** |

False stale/incompatible banner bug is **resolved** on this analysis.

---

## API-to-UI mapping

| UI section | API source field(s) | Status | Notes |
|------------|---------------------|--------|-------|
| Toolbar “79 markers” | `biomarkers.length` | OK | Counts full uploaded/scored panel |
| Governance strip | `lcS4ResultsCopy.ts` constant (not API) | Expected | Static copy; not from DTO |
| Stale banner | `result_versioning` | OK | Hidden when `current` |
| Hero title | `resolveHeroPrimaryStory()` ← `clinician_report_v1.sections.page1` + IDL | Partial | Hero homocysteine-led; IDL strong signal is Vascular Inflammation |
| Hero subline “Most relevant area…” | Hero resolver / page1 fields | Partial | Vascular framing under homocysteine headline |
| Body overview prose | `narrative_report_v1.body_overview` | **Leakage** | Contains `**Cardiovascular 4 Biomarkers**` markdown |
| Pattern-groups placeholder | `clusters[]` + `showPatternGroupBuckets={showDetails}` | **Misleading** | 3 clusters exist; buckets hidden by default |
| Primary finding and why — hypothesis title | `clinician_report_v1.sections.root_cause.hypotheses[0].title` | **Mismatch** | “B12-associated pattern” |
| Supports / complicates bullets | `hypotheses[0].evidence_for/against` | OK | B12 counter-evidence present |
| What’s working well | `balanced_systems_v1` | OK | Hematological, Renal stable |
| Health system cards | `consumer_domain_scores[]` | OK | CV 86, BS 100, Liver 73 |
| Card completeness lines | `evidence_completeness_numerator/denominator` | OK | Per-domain expected marker sets |
| Confidence section | `clinician_report_v1.sections.page1` + WhyThisLeadWon | OK | Appropriate uncertainty |
| Data quality “9 of 9” | `clinician_report_v1.data_quality.panel_completeness_*` | **Confusing** | 9 primary metrics, not 79 biomarkers |
| Patterns across body | IDL / interpretation patterns + clusters narrative | OK | Methylation pathway visible |
| What’s driving this | Subset of `biomarkers[]` by driver logic | Partial | Transferrin **Critical** prominent |
| All markers grid | `biomarkers[]` + `display_label` | Partial | Upload naming oddities (`dhea s`, etc.) |
| Uploaded panel values | `meta.upload_panel_observations` | OK | HbA1c % equivalent shown |
| Next steps | `narrative_report_v1.next_steps_narrative` + confirmatory tests | OK | Appropriate clinician framing |
| Actions hub link | Frontend route `/actions` | OK | Wired (verified in prior session) |
| Clinician / Advanced (collapsed) | `clinician_report_v1`, meta insight graph | OK | Gated behind Show |

---

## Full page walkthrough

### Header / session / loading

- Hydration briefly shows **Sign in** then settles to **Log out** — acceptable.
- No loading spinner stuck; full ~14k char body renders.
- **No console errors** observed in-session (hook returned empty; no visible runtime faults).

### Hero / primary finding

- **Primary finding:** “Raised homocysteine pattern: warrants attention on this panel” — **correct lead**.
- **Subline:** “Most relevant area: Vascular Inflammation Risk” — creates **dual framing** (methylation/homocysteine vs vascular inflammation).
- Driver line lists Homocysteine, Vitamin B12, Folate, Transferrin — clinically busy but data-backed.
- Severity badge “Needs attention” — proportionate.

### Governance strip

- “AI-personalised narrative is not active in this view” — **expected for internal UAT** (`lcS4ResultsCopy.ts`).
- Does not break journey; slightly technical for consumers — defer reword/hide decision.

### Body overview

- Compiled `body_overview` renders alcohol → homocysteine context **without slugs** — good.
- **Issues:** raw markdown `**Cardiovascular 4 Biomarkers**`; phrase “adjust how systems are weighted in the **analytical model**”; mojibake em-dash (`model � not`).
- Pattern-groups box says **“not available”** while **3 clusters** exist in API.

### Primary finding and why

- Section title shows **“B12-associated pattern”** while bullets explicitly say B12 is **in range** and pulls against the hypothesis — **trust contradiction**.
- Lead-pattern bridge correctly references homocysteine hero title.
- Technical ranking gated behind “Show technical detail” — good.

### What’s working well

- Hematological and Renal marked stable — helps contextualise concern.
- Copy references “Cardiovascular” as headline focus — consistent with vascular subline tension.

### Health systems cards

- Three cards render with scores, reliability tiers, completeness (5/5, 1/2, 5/6).
- Expanded copy uses consumer chip roles (“Used in this score”) — **improved** vs prior `score_contributor` leakage.
- Blood sugar **100/100** with **Limited reliability** (1 of 2 markers) — numerically honest but cognitively odd.

### Confidence / data quality

- Confidence caveats appropriately non-diagnostic.
- **“We received 9 of 9 expected markers for this interpretation”** sits under toolbar **“79 markers”** — user cannot reconcile without engineering knowledge.

### Patterns / clusters

- “Methylation pathway pattern” section present and coherent.
- Pattern-group **bucket UI intentionally hidden** unless technical detail on (FE-R6A) — but fallback copy implies data missing.

### Biomarker table / drivers

- **Homocysteine** 16.23 µmol/L · Elevated — matches lab range (3.7–13.9).
- **Transferrin** 2.0 g/L · **Critical** — value below lab min 2.15 g/L; status mapping is **lab-grounded** but **alarmist label** in hero driver band without iron/ferritin narrative tie-in (ferritin 202.7 µg/L in range).
- **ALT** 7 U/L · low (below 10–49) — not in top drivers; grid shows correctly.
- **TC/HDL ratio** card notes unscored units/range — honest handling.
- Display labels: `dhea s`, `Apob Apoa1 Ratio`, `(venous)` suffixes, internal ids in grid headings.

### Next steps / actions

- Sensible non-prescriptive clinician follow-up.
- MMA callout appropriate for homocysteine thread.
- “Consider discussing **Repeat homocysteine**” — awkward grammar.
- Actions hub pointer present.

### Footer / collapsed sections

- Clinician summary and Advanced analysis collapsed by default — appropriate progressive disclosure.

---

## Defect register

| ID | Severity | Section | Issue | Evidence | Likely source | Fix direction | Now / defer |
|----|----------|---------|-------|----------|---------------|---------------|-------------|
| IUAT-001 | **HIGH** | Primary finding and why | “B12-associated pattern” heading while B12 counter-evidence says in-range | UI + API `hypotheses[0].title` | `report_compiler_v1` hypothesis titles; `PrimaryFindingAndWhy.tsx` renders `hyp0.title` raw | Rename hypothesis when counter-evidence dominates; or map to neutral label (“One-carbon / homocysteine context”) | **Fix now** |
| IUAT-002 | **HIGH** | Body overview | “Pattern groups are not available…” despite 3 clusters | UI + API `clusters: 3` | `ResultsBodyOverview.tsx` — fallback when `showPatternGroupBuckets=false` | Separate “hidden by default” vs “unavailable”; or show count without buckets | **Fix now** |
| IUAT-003 | **HIGH** | Toolbar vs data quality | 79 markers vs 9/9 expected markers | UI + `data_quality.panel_completeness_*` | `page.tsx` count vs `PipelineStatus.tsx` primary-metric completeness | Dual-label copy: “79 markers uploaded” vs “9 key markers used for headline completeness” | **Fix now** |
| IUAT-004 | **HIGH** | Body overview | `**Cardiovascular 4 Biomarkers**` markdown + internal system name | API `body_overview`; visible in browser | `narrative_report_compiler_v1` / scrub gap in `scrubKnownInternalPatternNames` | Strip markdown; map system slug to consumer label in compiler or scrubber | **Fix now** |
| IUAT-005 | **HIGH** | Hero | Homocysteine primary + “Vascular Inflammation Risk” subline | UI hero + IDL `strong_signal` | `resolveHeroPrimaryStory` + page1 `primary_concern` vs IDL | Align subline to lead pattern or explain relationship explicitly | **Fix now** |
| IUAT-006 | **HIGH** | What’s driving this | Transferrin shown as **Critical** in lead driver band | API `status: critical`, value 2.0 vs ref 2.15–3.65 | Scoring/status mapping + driver selection UI | Confirm label tier naming (Low vs Critical); add contextual copy when ferritin normal | Fix now (label); defer deep clinical copy |
| IUAT-007 | **MEDIUM** | Body overview | “analytical model” engineering phrasing | API `body_overview` | Narrative compiler lifestyle appendix | Consumer rewrite in compiler/scrub | Defer to retail polish |
| IUAT-008 | **MEDIUM** | Body overview | Mojibake character in lifestyle sentence | API text `` | Encoding in narrative assembly | Fix UTF-8 in compiler output | Defer |
| IUAT-009 | **MEDIUM** | All markers grid | Raw upload labels (`dhea s`, `Apob Apoa1 Ratio`, `(venous)`) | `biomarkers[].display_label` | Upload panel lab naming + display enrichment | SSOT display-name normalisation | Defer |
| IUAT-010 | **MEDIUM** | Blood sugar card | 100/100 Strong + Limited reliability | Domain scores UI | Scoring vs completeness semantics | Add explanatory bridge sentence on card | Defer |
| IUAT-011 | **MEDIUM** | Next steps | “Repeat homocysteine” awkward phrasing | Narrative / next steps list | Compiler copy | Copy edit | Defer |
| IUAT-012 | **MEDIUM** | Governance strip | “AI-personalised narrative is not active” | Static LC-S4 copy | Product decision | Keep for internal UAT; reword or hide for retail | Defer |
| IUAT-013 | **LOW** | What’s working well | Duplicate heading text (visible + sr-only pattern) | Component structure | `BalancedSystemsSummary` / section wrapper | Layout polish | Defer |
| IUAT-014 | **LOW** | Marker grid | Free testosterone % shows score 0 | Biomarker dial | Derived marker scoring edge | Display policy | Defer |
| IUAT-015 | **LOW** | Page length | Long scroll for first-time user | Journey design | Product IA | Progressive disclosure tuning | Defer |

**Counts:** BLOCKER **0** · HIGH **6** · MEDIUM **6** · LOW **3**

---

## Known issue deep-dives

### 1. B12-associated heading mismatch

| Aspect | Detail |
|--------|--------|
| **Visible** | Section subtitle “B12-associated pattern” under Primary finding and why |
| **Counter-evidence** | “B12 appears clearly within range… makes a B12-driven pattern less likely” |
| **API** | `vitamin_b12` 336 pg/ml normal; `active_b12` 139 pmol/L optimal; hypothesis title from compiler |
| **Justified?** | **No for retail** — hypothesis is structurally valid as differential, but **title over-asserts causality** |
| **Source** | `report_compiler_v1` → `clinician_report_v1.sections.root_cause.hypotheses[0].title`; rendered in `PrimaryFindingAndWhy.tsx:104-106` |

### 2. Pattern-groups placeholder copy

| Aspect | Detail |
|--------|--------|
| **Visible** | “Pattern groups are not available for this result yet…” |
| **API** | `clusters.length === 3` (Cardiovascular mild, Hematological normal, Renal normal) |
| **Intent** | FE-R6A gates bucket counters behind `showDetails` to avoid contradiction |
| **Problem** | Fallback copy asserts **unavailability**, not **“summary hidden until technical detail”** |
| **Source** | `ResultsBodyOverview.tsx:62-85`; `page.tsx:695` |

### 3. Marker count 79 vs 9/9

| Aspect | Detail |
|--------|--------|
| **Visible** | “79 markers” (toolbar) vs “We received 9 of 9 expected markers for this interpretation” |
| **API** | 79 biomarkers; `panel_completeness_present/expected = 9/9` for **primary metric set** (homocysteine, MCV, transferrin, lipids, etc.) |
| **Understandable?** | **No** to a normal user — looks contradictory |
| **Source** | `page.tsx:652`; `PipelineStatus.tsx:57-61`; `clinician_report_v1.data_quality` |

### 4. Homocysteine hierarchy

| Layer | Content |
|-------|---------|
| Hero | Raised homocysteine pattern (lead) |
| Subline | Vascular Inflammation Risk |
| Body | Homocysteine elevation context + methylation pattern |
| IDL | Vascular Inflammation Risk = `strong_signal`; homocysteine context in narrative |
| **Verdict** | Lead is **mostly correct**; vascular/B12/methylation threads **compete** without explicit hierarchy explanation |

### 5. Severity labels / transferrin critical

| Field | Value |
|-------|-------|
| Value | 2.0 g/L |
| Lab range | 2.15–3.65 g/L (source: lab) |
| Status | `critical` (1 of 79 biomarkers) |
| Ferritin | 202.7 µg/L in range |
| **Assessment** | **Lab-grounded low**, not a frontend invention; **“Critical” retail label** in driver band is **disproportionate** without iron-studies context |
| **Source** | Backend scoring/status mapping → biomarker DTO → drivers UI |

### 6. Raw marker label leakage

| Examples observed | Severity |
|-------------------|----------|
| `dhea s`, `Apob Apoa1 Ratio` | MEDIUM |
| `(venous)`, `(hgb)`, `(wbc)` suffixes | LOW–MEDIUM |
| `Cardiovascular 4 Biomarkers` in prose | HIGH |
| No `signal_`, `pkg_`, UUID on page | Good |

### 7. Governance strip

| Text | “AI-personalised narrative is not active in this view” |
|------|--------------------------------------------------------|
| Expected? | **Yes** for current internal mode |
| Harmful? | **Low–medium** — honest but technical |
| Recommendation | Keep for internal UAT; product decision for retail |

---

## Safety and clinical-caution review

| Rule | Assessment |
|------|------------|
| Overstates causality | **Partial fail** — B12-associated title |
| Implies diagnosis | **Pass** — disclaimers and clinician framing present |
| Alarmist language | **Partial** — Transferrin “Critical” in drivers |
| In-range as abnormal | **Pass** for B12; B12 title contradicts bullets not values |
| Missing-marker claims | **Pass** — completeness caveats present |
| Hides uncertainty | **Pass** — confidence section adequate |
| Non-diagnostic | **Pass** |
| Lab-range grounded | **Pass** — ranges shown with `source: lab` in API |

---

## Technical review

| Item | Result |
|------|--------|
| Console errors | None observed |
| Network | `GET /api/analysis/result` **200**; no failed fetches after load |
| API consistency | DTO fields align with UI sections |
| Dummy/fallback clinician report | **Not used** — real compile from `meta.insight_graph.report_v1` |
| Pass 3 / investigation-spec exposure | **Not observed** in UI text scan |
| Versioning | **Fixed** — assesses assembled DTO |

---

## Recommended work packages

### 1. Immediate high-trust fixes (next sprint)

- IUAT-001 B12 hypothesis title vs counter-evidence
- IUAT-002 Pattern-groups placeholder honesty
- IUAT-003 Dual marker-count labelling
- IUAT-004 Body overview markdown / internal system names
- IUAT-005 Hero / vascular subline alignment
- IUAT-006 Transferrin severity presentation in driver band

### 2. Retail polish

- IUAT-007–009 copy and display-name normalisation
- IUAT-011 next-steps grammar
- IUAT-012 governance strip product decision

### 3. Deeper output-generation

- Narrative compiler consumer scrub expansion (`scrubKnownInternalPatternNames`)
- Hypothesis title selection rules when counter-evidence present
- Primary-metric completeness vs uploaded-marker UX contract

### 4. Deferred internal-only

- Page length / disclosure tuning (IUAT-015)
- Minor grid scoring display edges (IUAT-014)

---

## Do not fix yet (without broader decision)

- Hiding governance strip without product sign-off
- Changing homocysteine/vascular **scoring** or signal activation
- Frontend-side severity inference (must stay render-only)
- Dummy clinician content or compatibility bypasses
- Collapsing health-system cards or removing uncertainty sections

---

## Final recommendation

1. **Fix next:** HIGH items IUAT-001 through IUAT-006 in a focused “retail trust hardening” sprint (compiler + scrub + frontend copy only).
2. **Defer:** Display-name polish, governance strip retail wording, page-length IA.
3. **Re-UAT required:** Yes — after HIGH fixes, re-run this checklist on a **new** analysis_id plus regression on `6bcbf1de`.
4. **Internal validation:** **Proceed** — page is structurally sound and versioning is correct; HIGH issues are copy/hierarchy, not pipeline failure.

---

## Screenshot index

| File | Section |
|------|---------|
| `01-hero-governance.png` | Toolbar, governance strip, journey intro |
| `02-body-overview-primary-why.png` | Body overview + internal vocabulary |
| `03-health-systems-confidence.png` | What’s working well |
| `04-markers-driving.png` | What’s driving this (incl. Transferrin Critical) |
| `05-next-steps-footer.png` | Collapsed clinician/advanced sections |
