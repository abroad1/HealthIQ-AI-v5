# LAUNCH-CORE-4 — Results Page Narrative Hierarchy and Score Rationalisation Audit

**Analysis:** `746f2b0a-b470-4d87-8ed8-e2c3d1e68c02`  
**URL:** `http://localhost:3000/results?analysis_id=746f2b0a-b470-4d87-8ed8-e2c3d1e68c02`  
**Account:** `test-user3@example.com`  
**Repo:** `main` @ `ff83dbe` (audit branch cut from aligned `main`)  
**Date:** 2026-05-30  
**Mode:** Investigation only — no production code changes.

---

## 1. Executive verdict

### **PASS WITH RESERVATIONS — UX hierarchy needs a dedicated sprint before feature expansion**

Technical correctness from ARCH-RT / LAUNCH-CORE-1 is largely intact on this post-merge analysis. The **consumer experience problem is real**: the page reads as a **stack of competent widgets**, not a **guided health report**.

| Dimension | Assessment |
|-----------|------------|
| Main story discoverable in 30s | **No** — lead pattern repeats; scores compete |
| Narrative flow | **Weak** — section order deviates from ideal journey |
| Score hierarchy | **Confusing** — 6+ score families visible before advanced |
| Repetition | **High** — homocysteine / lead pattern / vascular framing recur |
| Launch blocker | **No** clinical runtime defect |
| Pre-launch UX fix needed | **Yes** — hierarchy + de-duplication sprint recommended |

**Refresh/regenerate button timing:** Build **page hierarchy and score rationalisation first**, then add regenerate. A regenerate button on the current page would preserve the same overwhelming structure; LC-3 metadata already marks this result `incompatible` / `regeneration_available: false` with no user-visible explanation banner.

---

## 2. Preflight evidence

| Check | Result |
|-------|--------|
| Branch at start | `main` @ `ff83dbe` |
| `HEAD == origin/main` | **Yes** |
| Working tree | **Clean** |
| LAUNCH-CORE-3 merged | **Yes** (`e4d8fda`, `470a227`, …) |
| Stash | **Empty** |
| Audit branch | `work/LAUNCH-CORE-4-results-page-narrative-hierarchy-and-score-rationalisation-audit` |

---

## 3. Screenshots

| File | Content |
|------|---------|
| `docs/audit-papers/assets/lc4-results-hero.png` | Journey intro + primary finding hero |
| `docs/audit-papers/assets/lc4-results-health-systems.png` | Expanded Health Systems Cards (liver subsystems) |
| `docs/audit-papers/assets/lc4-results-primary-finding.png` | Primary finding and why — evidence blocks |
| `docs/audit-papers/assets/lc4-results-full-page.png` | Viewport capture (page length exceeds single capture; full scroll documented via snapshot) |

---

## 4. Console, network, validators

| Item | Result |
|------|--------|
| Page load | **OK** |
| Login | **OK** |
| API `GET /api/analysis/result` | **200** |
| Console errors | **None** observed |
| `validate_day_one_architecture.py` | **PASS** |
| `pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q` | **4 passed** |

Runtime API inspection: `automation_bus/_lc4_746f2b0a.json` (local, not committed).

---

## 5. Overall user story assessment

### What story would a user take away?

> **Raised homocysteine / vascular inflammation pattern** — likely linked to **B12 / methylation / MCV context** — with **cardiovascular** as the main system frame; several other areas (blood sugar, liver enzymes) have **partial marker coverage** but still show **high numeric scores**.

### Is it obvious within 30 seconds?

**Partially.** The hero states “Raised homocysteine pattern” and “Strong Signal,” but within the first screenful the user also sees:

- A long journey preamble
- Mock-mode / structured-rules disclosure
- Body overview repeating the same lead
- Bridge text explaining section order (meta-instruction, not health content)

The **hypothesis story (B12-associated pattern)** does not surface until **Primary finding and why**, well below Health Systems Cards.

### Guide vs overwhelm?

**Overwhelm.** The page exposes multiple confidence systems, duplicate lead framing, three 0–100 system gauges, pattern cards, marker-level scores, and trust-strip completeness — before the user reaches a single consolidated “what to do next.”

---

## 6. Score inventory table

| # | Visible label | Value (this panel) | DTO / source | Frontend component | User likely thinks | Necessary? |
|---|---------------|-------------------|--------------|-------------------|-------------------|------------|
| 1 | **Strong Signal** (hero badge) | Qualitative | `interpretation_display_layer_v1.records[].severity_state` → `resolvePrimaryFindingSeverity()` | `ResultsPrimaryHero` | “This is bad / urgent” | Useful but **duplicative** with IDL cards |
| 2 | **Primary finding title** | Raised homocysteine pattern… | `clinician_report_v1.sections.page1.primary_concern` (scrubbed) | `ResultsPrimaryHero` | Main headline | **Yes** — primary |
| 3 | **Main system context** | Vascular Inflammation Risk | IDL `retail_display_label` via `resolveHeroPrimaryStory()` | `ResultsPrimaryHero` | System anchor | **Useful** but jargon-adjacent |
| 4 | **CV card score** | 86 / 100 · Strong | `consumer_domain_scores[].score`, `band_label` | `Wave1HealthSystemScoreVisual` | “Heart health grade” | **Yes** — if hierarchy clarified |
| 5 | **Score reliability** | Good / Limited reliability | `confidence_tier` | `Wave1DomainCards` + `wave1ScoreReliabilityLabel()` | “Can I trust the number?” | **Yes** — keep one place |
| 6 | **Evidence completeness** | 7/7, 2/4, 5/6 | `evidence_completeness_*` | `Wave1DomainCards` | “How much data was used?” | **Yes** — post LC-1 aligned |
| 7 | **Score qualification** | Score based on available markers (only) | Derived from limited coverage + score ≥90 | `wave1ScoreQualificationLine()` | Partial-data warning | **Useful** — highlights 100/100 + 2/4 tension |
| 8 | **Blood sugar 100/100** | 100 / 100 · Strong | Same as #4 | Wave1 cards | “Perfect blood sugar” | **Confusing** with 2/4 markers + limited reliability |
| 9 | **IDL severity** | Strong Signal | `severity_state` | `InterpretationPatternsSection` | Second urgency signal | **Duplicative** with hero |
| 10 | **Per-marker Scored X/100** | e.g. Scored 30.5/100, 100.0/100 | `biomarkers[].score` | `BiomarkerDials` | “Each test has a grade” | **Confusing** vs system scores |
| 11 | **Trust strip completeness** | 8 of 8 expected markers | `clinician_report_v1.data_quality` | `PipelineStatus` | Third completeness metric | **Duplicative** with card 7/7/2/4/5/6 |
| 12 | **Overall score** (collapsed) | 97 | `overall_score` | Advanced analysis card | “Whole-panel grade” | **Hidden OK** — but conflicts if found |
| 13 | **Risk summary bars** (collapsed) | Engine risk object | `risk_assessment` | Advanced analysis | Another scoring layer | **Hide** by default |
| 14 | **Marker status chips** | Elevated / Optimal etc. | `biomarkers[].status` | Biomarker dials | Lab interpretation | **Useful** in marker section |
| 15 | **Hypothesis title** | B12-associated pattern | `clinician_report_v1 root_cause` | `PrimaryFindingAndWhy` | Clinical sub-story | **Useful** — should be earlier or tied to hero |

### Score hierarchy diagnosis

There is **no single “master score.”** Users see **system card scores**, **marker scores**, **overall score**, **severity badges**, and **completeness counts** without guidance on precedence.

**Most confusing pair:** Blood sugar **100/100 Strong** alongside **Limited reliability** and **2 of 4 markers** — technically qualified but emotionally reads as “excellent.”

---

## 7. Repetition audit

| Repeated idea / phrase | Occurrences (visible) | Classification | Recommendation |
|------------------------|----------------------|----------------|----------------|
| “Raised homocysteine pattern…” | Hero title, body overview, primary finding intro, card contributor copy | **Confusing repetition** | **Merge** — one lead block; downstream sections reference “this pattern” |
| Homocysteine / vascular risk wording | Hero summary, CV card, IDL cards, driving markers | **Harmless duplication** → borderline confusing | Keep once in hero + once in patterns |
| **Strong Signal** | Hero badge + each IDL card | **Confusing repetition** | Hero only; patterns use plain “Needs attention” |
| **Vascular Inflammation Risk** | Hero context line + CV card anchor | **Should be merged** | One consumer label across hero + card |
| Journey meta-instructions | Page intro + bridge paragraph under hero | **Should be hidden** under help or first-visit tooltip | Shorten to one line |
| “What's working well” heading | Appears multiple times in accessibility tree | **Harmless** (sr-only duplicate) | Verify DOM — possible duplicate headings |
| Lead pattern + hypothesis | Hero concern vs B12-associated pattern | **Should be merged** narratively | Single “Main finding” + “What we think is going on” |
| Completeness metrics | Trust strip 8/8 + three card ratios | **Confusing repetition** | Trust strip → collapsed; cards authoritative |
| Confirmatory / next steps | Narrative next steps + confirmatory section + action cards | Partial dedup exists | Further merge action cards when narrative present |
| “on this panel” | Very frequent boilerplate | **Should be merged** via copy edit | Backend + FE scrub |

---

## 8. Narrative flow assessment

### Ideal vs actual order

| Step | Ideal | Current page (default visible order) | Deviation |
|------|-------|--------------------------------------|-----------|
| 1 Main finding | Hero | Hero + immediate body overview repeat | **Duplicate** |
| 2 Why it matters | Near top | Buried in hero summary + CV card prose | **Too late / scattered** |
| 3 Confidence | One block | Trust strip + card reliability + uncertainty section + qualifications | **Fragmented** |
| 4 Body systems | After story | **Health Systems Cards before Primary finding and why** | **Major order bug (UX)** |
| 5 Supporting markers | Mid page | Driving signals + all markers | OK placement |
| 6 Missing / limits | Before next steps | Card missing chips + trust strip + uncertainty | **Scattered** |
| 7 Next steps | Clear CTA | Bottom — good | OK |
| 8 Technical detail | Collapsed | Partially (`Show technical detail`, disclosure sections) | OK foundation |

**Critical structural issue:** `Wave1DomainCards` is rendered **before** `PrimaryFindingAndWhy` in `results/page.tsx` (lines 717–729), interrupting the “why” story with three scored widgets.

---

## 9. Section-by-section UX audit

### Hero / journey introduction (`ResultsPrimaryHero`, page header)

| Aspect | Assessment |
|--------|------------|
| Purpose | Establish lead finding |
| Clear? | **Yes** for headline; summary paragraph is dense |
| Duplicates | Body overview, primary finding, patterns |
| Default visibility | Correct |
| Wording | “Strong Signal” mechanical; “Vascular Inflammation Risk” internal-adjacent |

### Body overview (`ResultsBodyOverview`)

| Aspect | Assessment |
|--------|------------|
| Purpose | Whole-body framing |
| Clear? | Moderate |
| Duplicates | **Hero almost entirely** |
| Recommendation | **Merge into hero** or collapse behind “Read more” |

### What's working well (`BalancedSystemsSummary`)

| Aspect | Assessment |
|--------|------------|
| Purpose | Reassurance / balance |
| Clear? | Yes |
| Duplicates | Low |
| Recommendation | **Keep** — good counterweight; move after main finding |

### Health Systems Cards (`Wave1DomainCards`)

| Aspect | Assessment |
|--------|------------|
| Purpose | System-level scores + marker coverage |
| Clear? | Per-card yes; **in aggregate overwhelming** |
| Duplicates | Contributor sentences repeat vascular/homocysteine themes |
| Default visibility | Expanded on user action — good |
| Recommendation | **Move after** primary finding; consider **one-at-a-time** focus |

### Primary finding and why (`PrimaryFindingAndWhy`)

| Aspect | Assessment |
|--------|------------|
| Purpose | Hypothesis + evidence for/against |
| Clear? | **Best clinical prose on page** |
| Duplicates | Re-states lead pattern in intro |
| Recommendation | **Promote earlier**; trim intro sentence |

### Why this lead won / Trust strip (`WhyThisLeadWonSection`, `PipelineStatus`)

| Aspect | Assessment |
|--------|------------|
| Purpose | Confidence + arbitration transparency |
| Clear? | Trust strip line 1 conflicts with card completeness semantics |
| Recommendation | **Collapse trust strip** by default; keep uncertainty narrative |

### Interpretation patterns (`InterpretationPatternsSection`)

| Aspect | Assessment |
|--------|------------|
| Purpose | Cross-body patterns |
| Clear? | Yes but **overlaps hero + primary finding** |
| Recommendation | **Keep** but dedupe titles/severity; max 2 visible |

### Marker-level evidence (`BiomarkerDials`, `UploadedPanelFidelity`)

| Aspect | Assessment |
|--------|------------|
| Purpose | Raw marker values |
| Clear? | Values clear; **Scored X/100** adds noise |
| Recommendation | Default to **value + status**; hide numeric score unless technical detail |

### Next steps (`NarrativeLongitudinalAndNextSteps`, confirmatory, action cards)

| Aspect | Assessment |
|--------|------------|
| Purpose | Actionable follow-up |
| Clear? | Reasonably clear |
| Recommendation | **Keep**; ensure single bullet list priority |

### Collapsed sections (interpretation context, clinician, advanced)

| Aspect | Assessment |
|--------|------------|
| Purpose | Depth on demand |
| Recommendation | **Correct pattern** — extend to trust strip, duplicate narrative |

### LC-3 stale versioning (`StaleResultBanner`)

| Aspect | Assessment |
|--------|------------|
| API | `result_status: "incompatible"`, `stale_reasons: ["completeness_policy_missing"]` |
| UI | **No banner shown** — component only renders `result_status === 'stale'` |
| Impact | User gets no explanation that completeness policy differs from current engine |
| Classification | **Pre-launch UX fix** (product + FE) |

---

## 10. Source trace — confusing items

| Visible item | API field | Backend / FE | Issue class |
|--------------|-----------|--------------|-------------|
| Blood sugar 100/100 + 2/4 | `consumer_domain_scores[wave1_blood_sugar].score=1.0`, completeness 2/4 | Rail scoring vs LC-1 completeness | **Product hierarchy** + backend semantics |
| Strong Signal (hero) | IDL `severity_state: strong_signal` | `resolvePrimaryFindingSeverity()` | Frontend mapping |
| Vascular Inflammation Risk | IDL `retail_display_label` | Hero `systemContextLine` | DTO copy / IDL label |
| Lead repeated | `primary_concern`, `body_overview`, `narrative_report_v1` | Multiple render surfaces | **Frontend layout** + backend duplication |
| Scored 30.5/100 on marker row | `biomarkers[].score` | `BiomarkerDials` | Frontend display choice |
| Trust strip 8/8 vs card 2/4 | `data_quality.panel_completeness_*` vs subsystem union | Different counting bases | **DTO / product** — rationalise metrics |
| No stale banner | `result_versioning.result_status=incompatible` | `StaleResultBanner` guard | **Frontend gap** (LC-3) |

---

## 11. User-facing language samples

| Text | Issue |
|------|-------|
| “Strong Signal” | Mechanical severity enum |
| “Vascular Inflammation Risk” | Construct name, not plain language |
| “Main system context: …” | Product scaffolding visible to user |
| “Lead pattern on this panel: Raised homocysteine pattern: warrants attention on this panel.” | **Triple redundancy** |
| “Score based on available markers only” | Good qualification but admits confusion |
| “USED IN THIS SCORE” / “CONTEXT MARKER” | Improved vs LC-0 but still taxonomy-flavoured |
| “Trust strip” | Internal wireframe name in UI title |
| “Why this lead won · uncertainty” | Arbitration jargon |
| “Technical ranking references and evidence-chain wording are hidden by default.” | Engineering vocabulary |
| “Pattern groups are not available for this result yet” | Apologetic filler — low value |

---

## 12. Recommended revised page hierarchy

### Keep visible by default

1. **One hero block:** main finding + one-sentence why + single confidence line  
2. **Primary finding and why** (hypothesis + top 2 evidence bullets)  
3. **What's working well** (short reassurance)  
4. **Health Systems Cards** (collapsed by default except lead-aligned system)  
5. **Patterns across your body** (max 2 cards, no duplicate severity badge)  
6. **What to do next** (merged narrative + confirmatory)  
7. **Marker-level evidence** (values/status; hide marker 0–100 scores)

### Move into expandable detail

- Body overview (merge into hero “Read more”)  
- Why this lead won / full uncertainty  
- Trust strip / data-quality tables  
- Expanded card contributor / consequence / next-step sentences  
- Per-marker numeric scores  
- Overall score + risk summary (already in Advanced — keep there)  
- Full clinician summary  

### Remove or merge

- Duplicate lead pattern intros (keep one)  
- Second “Strong Signal” on pattern cards  
- Bridge paragraph explaining section order (replace with compact progress indicator)  
- Redundant completeness line in trust strip when cards present  

### Rename / reword

| From | To (suggested) |
|------|----------------|
| Strong Signal | Needs attention |
| Trust strip | Data quality |
| Why this lead won · uncertainty | How confident is this read? |
| Main system context: | Most relevant area: |
| Score reliability | How much marker evidence we had |

### Needs backend DTO change

- Single **consumer lead label** emitted once (not repeated across narrative, page1, IDL)  
- Align **trust-strip completeness** with subsystem union OR drop trust-strip count  
- Surface **result_versioning** user_message for `incompatible` not only `stale`  
- Optional: **cap or relabel** domain scores when completeness &lt; 50%

### Needs frontend-only change

- Reorder sections: Primary finding before Health Systems Cards  
- Suppress marker `Scored X/100` unless `showDetails`  
- Dedupe hero vs body overview  
- Expand `StaleResultBanner` for `incompatible` status  

---

## 13. Launch impact classification

| Finding | Severity |
|---------|----------|
| Section order (cards before primary why) | **Pre-launch UX fix** |
| Score proliferation / 100 vs 2/4 | **Product decision** + pre-launch UX |
| Lead pattern repetition | **Pre-launch UX fix** |
| No banner for incompatible versioning | **Pre-launch UX fix** (LC-3 follow-up) |
| Strong Signal / Vascular Inflammation Risk labels | **Launch polish** |
| Trust strip vs card completeness | **Product decision** |
| Marker 0–100 scores in main list | **Launch polish** |
| Advanced overall score hidden | **Post-launch polish** (OK today) |

**No launch blockers** identified for clinical display on this analysis.

---

## 14. Fix backlog (prioritised)

### P0 — Pre-launch UX sprint (recommended: **LAUNCH-CORE-5**)

1. Reorder journey: Hero → Primary finding → Working well → Health systems → Patterns → Markers → Next steps  
2. Merge hero + body overview lead copy  
3. Show versioning banner for `incompatible` results  
4. Hide marker numeric scores by default  

### P1 — Product / copy

1. Rationalise blood-sugar (and similar) **score vs completeness** policy  
2. Consumer-safe IDL anchor labels  
3. Single completeness authority (cards OR trust strip)  

### P2 — Post-launch

1. Backend narrative de-duplication at compile time  
2. Progress stepper replacing meta prose  
3. Advanced section consolidation  

---

## 15. Refresh / regenerate button timing

**Answer: After page hierarchy work.**

Rationale:

1. LC-3 policy requires **versioned regeneration**, not silent refresh — users need a **clear story** when a new version differs.  
2. Current page overload would make “regenerate” feel like **more noise** without hierarchy fixes.  
3. This analysis is `regeneration_available: false` and `incompatible` with **no visible banner** — shipping regenerate before hierarchy + banner fixes would increase confusion.  

**Recommended sequence:**

1. **LAUNCH-CORE-5** — narrative hierarchy + score rationalisation (FE-first, some DTO)  
2. **LAUNCH-CORE-3B** — regeneration UX + incompatible/stale messaging parity  
3. Then enable regenerate button tied to new result version  

---

## 16. Validator / test results

| Command | Result |
|---------|--------|
| `python backend/scripts/validate_day_one_architecture.py` | **PASS** |
| `pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q` | **4 passed** |

---

## 17. Final recommendation

The results page is **technically credible** but ** narratively immature**. Users cannot quickly answer: *“What is wrong, how sure are you, and what should I do?”* without reading repetitive prose and reconciling conflicting scores.

**Proceed to launch only with:**

- A committed **UX hierarchy sprint** (P0 above), and  
- A **regeneration/stale messaging** follow-on before marketing re-run / refresh features.

**Executive verdict:** **PASS WITH RESERVATIONS** for launch-readiness of the **experience**, not the **engine**.
