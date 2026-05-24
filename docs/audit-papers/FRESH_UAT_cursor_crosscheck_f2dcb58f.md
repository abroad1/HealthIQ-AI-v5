# Fresh UAT Cursor Cross-Check — f2dcb58f

**Auditor:** Cursor (independent browser + API spot-check)  
**Claude report compared:** `docs/audit-papers/FRESH_UAT_results_journey_quality_audit_f2dcb58f.md` (read only after independent assessment)  
**Scope:** Investigate only — no code changes

---

## 1. Executive verdict

| Item | Assessment |
|------|------------|
| **Overall score** | **6 / 10** |
| **Verdict** | **PASS WITH RESERVATIONS** |
| **Claude report accuracy** | **Broadly accurate** — core defects reproduced; a few claims are slightly overstated or missing nuance (see §9) |
| **Defect sprint before KB-WAVE-1?** | **Yes** — biomarker depth for lead markers, journey-structure leakage, and next-step formatting should be fixed before KB-WAVE-1 content is added |

The page loads, reads as a guided journey, and FE-R5A patterns render safely. However, retail-surface leakage (`analytical model`, `interpretation confidence`, `Linked to …`), contradictory pattern counters, thin Homocysteine expansion (DTO + UI), and messy next-step rendering keep it below commercial bar.

---

## 2. Page inspected

| Field | Value |
|-------|--------|
| **URL** | `http://localhost:3000/results?analysis_id=f2dcb58f-e816-4ff6-9011-e93c5d48b82c` |
| **analysis_id** | `f2dcb58f-e816-4ff6-9011-e93c5d48b82c` |
| **Login** | `test-user3@example.com` / `Subaru@555` |
| **Date/time** | 2026-05-24 ~21:42 UTC (browser session) |
| **Git HEAD** | `main` @ `c741be9` (chore(bus): FE-R5A kernel COMPLETE status) |
| **Method** | Cursor IDE browser (accessibility snapshot + CDP `Runtime.evaluate` for expansion text) + authenticated API GET |
| **Backend/frontend** | Both returned HTTP 200 when probed; **not restarted** for this audit — assumed already running on current `main` |
| **Fresh vs persisted** | **Fresh generated result** — `created_at` `2026-05-24T21:07:46Z`; listed on dashboard as completed 5/24/2026 9:07:46 PM, Score 97% |

---

## 3. Independent rendered journey order

### Actual order observed (top → bottom)

1. Page header — **Your results** (+ 77 markers, action buttons)
2. **How to read this page** [h2] — framing copy
3. → **Primary finding hero** — *Homocysteine Elevation Context: warrants attention on this panel* (nested inside #2)
4. → **Your body overview** [h3] — includes pattern-group counters (nested inside #2)
5. → **Summary** [h3] — retail summary prose (nested inside #2)
6. **What's working well** [h2]
7. **Primary finding and why** [h3] — *B12-associated pattern*
8. **Why this lead won and uncertainty** [h2] / **Why this lead won · uncertainty** [h3]
9. **Trust strip** (within uncertainty block)
10. **Patterns across your body** [h2] — *Methylation pathway pattern*
11. **Marker-level evidence** [h2]
12. → **What's driving this** [h3]
13. → **All markers on this run** [h2] — 77 dial cards
14. **Uploaded panel values** [h3]
15. **What to do next** [h2]
16. **Health domains** [h3] — supplementary
17. **Additional interpretation context** [h3] — supplementary
18. **Clinician summary** [h3]
19. **Advanced analysis** [h3]

### Comparison to intended v6 order

| # | Intended section | Observed | Match? |
|---|------------------|----------|--------|
| 1 | Your body overview | Present, but **preceded by hero** and wrapped under **How to read this page** | **Partial** |
| 2 | What's working well | Present, after Summary | **Partial** (order OK relative to primary-finding section, but hero/body order inverted vs v6) |
| 3 | Primary finding and why | Present (also duplicated as hero) | **Partial** — content duplicated |
| 4 | Why this lead won / uncertainty | Present | **Yes** |
| 5 | Patterns across your body | Present | **Yes** |
| 6 | Marker-level evidence | Present | **Yes** |
| 7 | What to do next | Present | **Yes** |
| 8 | Clinician summary | Present (bottom, collapsed heading) | **Yes** |

**Extra / structural drift:** `How to read this page` wrapper; **Summary** section; **Trust strip**; **Uploaded panel values**; supplementary domain/context blocks.

---

## 4. Independent defect findings

Only defects personally reproduced in browser/API:

| Defect | Exact visible text | Location | Severity | Likely source | Blocks KB-WAVE-1? |
|--------|-------------------|----------|----------|---------------|-------------------|
| Hero nested under tutorial heading | Section heading **"How to read this page"** contains primary finding hero + body overview | Top of journey | High | FE-R2 journey wrapper / layout | Soft |
| Model language on retail surface | `This is used only to adjust how systems are weighted in the analytical model — not to alter the lab values on this panel.` | Your body overview | High | `narrative_report_v1.body_overview` | Soft |
| Pattern counter contradicts lead | `Needs attention` **0** / `Explore further` **0** / `Stable on this panel` **3** while hero + patterns show **Strong Signal** homocysteine concern | Your body overview → Pattern groups on this panel | High | Pattern-group counter vs lead-finding display logic | **Yes** |
| Summary duplicates hero/overview | `Your main result pattern centres on homocysteine elevation context…` / `Homocysteine Elevation Context warrants attention on this panel, with homocysteine as the main marker on this panel.` | Summary [h3] | Medium | `narrative_report_v1.retail_summary` surfaced twice | No |
| Technical confidence in stable systems | `(interpretation confidence for this read: insufficient)` | What's working well — Hematological, Renal | Medium | `balanced_systems_v1` copy on consumer surface | No |
| Homocysteine expansion thin | **WHAT THIS RESULT MEANS NOW** → `Scored using lab reference range` only | Homocysteine (venous) card → Expand/Close | High | DTO: no `contribution_context`, no `biomarker_educational_explainer`; `interpretation` is scoring-only | **Yes** |
| Internal upload labels | `Linked to hba1c` / `Linked to tc hdl ratio` | Uploaded panel values | High | Mode A fidelity `linked_to` display | Soft |
| Next steps not real list markup | Single `DIV`: `Next steps• Discuss these findings…\n• Monitor trends…` (bullet chars, not `<ul><li>`) | What to do next → Next steps | Medium | Frontend renders prose block | No |
| Dangling subsection label | `Suggested follow-up themes:` then separate **Tests to discuss with your clinician** | What to do next | Low | Compiled next-steps layout | No |
| Raw fallback message | `No separate checklist of follow-up lines was packaged with this result. The sections below still describe what to discuss next.` | What to do next | Medium | Conditional fallback in results page | No |
| Scoring engine message on card | `Not scored - result unit and lab reference range unit cannot be aligned for this marker (incompatible units); check units on the report.` | Total Cholesterol/hdl Ratio Calculation (venous) | Medium | Scoring/DTO error surfaced verbatim | No |
| Lead label mismatch | Hero: **Homocysteine Elevation Context** vs section: **B12-associated pattern** | Hero vs Primary finding and why | Medium | Different narrative source fields | No |

---

## 5. Specific checks against Claude’s claims

| Claude claim | Cursor observed? | Evidence | Comment |
|--------------|------------------|----------|---------|
| 1. “How to read this page” incorrectly wraps hero/body overview | **Yes** | h2 **How to read this page** → hero region → **Your body overview** → **Summary** | Confirmed |
| 2. Homocysteine expansion only shows “Scored using lab reference range” | **Yes** | Expanded card text: `WHAT THIS RESULT MEANS NOW` / `Scored using lab reference range` | Confirmed |
| 3. No contribution_context in Homocysteine expansion | **Yes** | API: `contribution_context: None`; UI: no “HOW IT CONNECTS” block | Confirmed — **absent from DTO** |
| 4. No biomarker educational explainer in Homocysteine expansion | **Yes** | API: `biomarker_educational_explainer` absent; UI: no education block | Confirmed — **absent from DTO** |
| 5. Body overview includes “analytical model” language | **Yes** | Exact sentence quoted in §4 | Confirmed |
| 6. Pattern groups “Needs attention: 0” while strong signal exists | **Yes** | Counters 0/0/3 vs **Strong Signal** pattern + elevated homocysteine narrative | Confirmed |
| 7. Summary duplicates hero/body overview | **Yes** | Summary section text overlaps retail_summary / hero | Confirmed |
| 8. “interpretation confidence for this read: insufficient” in What's working well | **Yes** | Exact parenthetical on Hematological and Renal rows | Confirmed |
| 9. “Linked to tc hdl ratio” / “Linked to hba1c” appears | **Yes** | Uploaded panel values section | Confirmed |
| 10. What to do next concatenated bullets / dangling “Suggested follow-up themes” | **Partial** | Bullets present as `•` in one DIV (not list items); `Suggested follow-up themes:` visible before Tests subsection | Bullets exist but **not proper list UI**; dangling label confirmed |
| 11. Raw FE-R1 forbidden strings absent | **Yes** | No matches for `ranked lead pattern`, `lab anchor`, `thread`, `confidence weight`, `structured ranking only`, `Functional read`, `Clinician-structured`, `0.90 vs 0.90` in visible text | Confirmed |
| 12. Patterns section correct and safe | **Yes** | **Methylation pathway pattern** with consumer copy, supporting markers, no raw cluster names | Confirmed FE-R5A behaviour |

---

## 6. Biomarker expansion forensic check

| Biomarker | Expanded content visible | interpretation present? | contribution_context present? | educational_explainer present? | Notes |
|-----------|-------------------------|----------------------|------------------------------|----------------------------------|-------|
| **Homocysteine (venous)** | Value 16.2 µmol/L; range 3.7–13.9; **WHAT THIS RESULT MEANS NOW** → `Scored using lab reference range` | Yes (scoring-only) | **No** | **No** | API: `interpretation: "Scored using lab reference range"`, `contribution_context: null`, no explainer → **field absent from DTO** |
| **Haemoglobin (hgb)** (stable) | **WHAT THIS RESULT MEANS NOW** → `Scored 100.0/100`; **HOW IT CONNECTS TO YOUR WIDER PATTERN** + cluster membership statement; **GENERAL MARKER EDUCATION** header | Yes | **Yes** | **Yes** (header visible; body truncated in extract) | Proves expansion zones **render when DTO supplies fields** |

**Transferrin** (elevated driver, not expanded in UI but API-checked): `interpretation: Scored using lab reference range`, no contribution_context, no explainer — same DTO gap class as Homocysteine.

---

## 7. Action / next-step rendering check

**Visible block (exact structure from DOM):**

```
Next steps
• Discuss these findings with a clinician who knows your history.
• Monitor trends on the cadence your clinician recommends.
• Repeat priority markers when your clinician advises retesting.
• Consider discussing Methylmalonic acid (MMA) with your clinician.
• Consider discussing Full blood count (MCV/haemoglobin/RDW) with your clinician.
• Consider discussing Repeat homocysteine with your clinician.

Suggested follow-up themes:
Tests to discuss with your clinician

Methylmalonic acid (MMA)
Consider discussing methylmalonic acid (MMA) testing with your clinician to evaluate functional B12 deficiency.

No separate checklist of follow-up lines was packaged with this result. The sections below still describe what to discuss next.
```

| Check | Result |
|-------|--------|
| Separate bullets | **Partial** — line breaks + `•` characters in one DIV; only **1** `<li>` in section (MMA test row) |
| Confirmatory tests with rationale | **Yes** — MMA with clinician-facing rationale |
| Fallback text | **Yes** — raw packaging fallback visible |
| Duplicate recommendations | **Yes** — MMA appears in bullets and again under Tests subsection |

---

## 8. Internal leakage check

| Search term | Found? | Exact visible context |
|-------------|--------|------------------------|
| ranked lead pattern | **No** | — |
| lab anchor | **No** | — |
| thread | **No** | — |
| governed label | **No** | — |
| moderate_by_default | **No** | — |
| confidence weight | **No** | — |
| structured ranking only | **No** | — |
| Functional read — | **No** | — |
| Prioritised follow-up | **No** | — |
| Clinician-structured | **No** | — |
| 0.90 vs 0.90 | **No** | — |
| Linked to | **Yes** | `Linked to hba1c`; `Linked to tc hdl ratio` |
| analytical model | **Yes** | `…weighted in the analytical model — not to alter the lab values…` |
| interpretation confidence | **Yes** | `(interpretation confidence for this read: insufficient)` |
| Not scored - result unit | **Yes** | `Not scored - result unit and lab reference range unit cannot be aligned…` |

---

## 9. Disagreement analysis

| Topic | Claude said | Cursor found | Which is more likely correct? | Why |
|-------|-------------|--------------|-------------------------------|-----|
| Overall score (5.5/10) | Prototype-like; severe biomarker failure | Same defects; Haemoglobin expansion works when DTO rich | **Cursor slightly higher (6/10)** | FE-R3 UI path is not globally broken — lead-marker gap is partly **missing DTO content**, not only render failure |
| Homocysteine expansion root cause | FE-R3 rendering failure | DTO lacks contribution_context + explainer; interpretation is scoring-only string | **Cursor nuance** | API proves absent fields; fix may need **backend/content + conditional UI**, not frontend-only |
| Next steps “concatenated bullets” | Single text block | DIV with newline-separated `•` items, not semantic list | **Both partially right** | Reads as one block; not as broken as pure concatenation but **not proper list rendering** |
| What's working well before primary finding | FE-R2 PASS — stable section before primary-finding section | True for sections 6→7, but **hero appears earlier** | **Claude correct with caveat** | Journey still opens with concern hero before reassurance block |
| KB-WAVE-1 blocked | Yes | Yes — lipid WHY content would use same expansion surface | **Agree** | Even if LDL/ApoB content added, Homocysteine-class gaps and retail leakage should be fixed first |

---

## 10. Recommended next step

**Proceed to FE-R6A defect cleanup** (small targeted sprint), **not** KB-WAVE-1 yet.

**Why:**

1. **Confirmed retail leakage** — `analytical model`, `interpretation confidence`, `Linked to …`, raw scoring errors — undermines trust on a paying-user surface.
2. **Confirmed journey-structure issues** — tutorial wrapper, duplicate Summary, contradictory pattern counters.
3. **Confirmed thin lead-marker expansion** — Homocysteine (primary concern) has no rich DTO fields; Haemoglobin shows the UI **can** render depth when supplied.
4. **FE-R5A patterns pass** — no need to reopen PATTERN-C1; patterns section is safe and well-placed.
5. **Claude report is broadly accurate** — independent audit reproduces the same defect set; disagreements are severity/nuance, not direction.

**After FE-R6A:** re-run human UAT on the same analysis ID (or a fresh run), then **proceed to KB-WAVE-1**.

**Not recommended now:** “no action needed”; **PATTERN-C1** (patterns already pass); skip straight to KB-WAVE-1.

---

*Independent audit complete. No repository code modified.*
