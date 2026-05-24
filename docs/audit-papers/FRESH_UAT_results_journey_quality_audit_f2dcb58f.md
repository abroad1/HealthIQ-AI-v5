# Fresh UAT — Results Journey Quality Audit

---

## 1. Executive verdict

**Overall score: 5.5 / 10**  
**Verdict: PASS WITH RESERVATIONS**

The page is materially better than the pre-FE-R1 baseline. The core consumer safety work (FE-R1 prose cleanup) held — none of the specific internal strings listed in the audit brief appear in the default retail view. The journey order is broadly correct and the page does read left-to-right as a guided sequence rather than a report dump.

However, the page still falls short of the v6 recommendation in four areas that matter commercially:

1. **The primary finding hero is buried inside a section labelled "How to read this page".** A paying user's first framing above the body overview is a section header that sounds like an instruction guide, not an analysis. The hero card — the single most important piece of content on the page — sits under that confusing wrapper.
2. **Biomarker card expansions are almost empty.** Homocysteine — the primary marker of concern — expands to show only "Scored using lab reference range." No interpretation, no clinical meaning, no contribution context. FE-R3 intended rich expansion content; in practice it does not render for this panel.
3. **The body overview contains model-explainer language** ("This is used only to adjust how systems are weighted in the analytical model") that should never reach a retail user.
4. **Two internal field labels ("Linked to tc hdl ratio", "Linked to hba1c")** appear verbatim in the Uploaded panel values section — an FE-R1 safety remnant.

Is the page coherent to a retail user? Barely. A user who reads carefully will follow the journey, but they will stumble on structural confusion (What section am I in?), empty biomarker expansions (Why did I click "Expand"?), and contradictory signals (the body overview says zero patterns need attention; the rest of the page is about a strong homocysteine signal).

Does it show HealthIQ's differentiation? Not clearly enough. The primary finding, uncertainty, and patterns sections individually have the right ingredients, but the entry point is muddled.

Ready for KB-WAVE-1? **No.** KB-WAVE-1 would add interpretation depth that cannot render properly given the current biomarker card expansion failure. A targeted frontend defect sprint must come first.

---

## 2. Page inspected

| Field | Value |
|---|---|
| URL | `http://localhost:3000/results?analysis_id=f2dcb58f-e816-4ff6-9011-e93c5d48b82c` |
| analysis_id | `f2dcb58f-e816-4ff6-9011-e93c5d48b82c` |
| Login used | test-user3@example.com / Subaru@555 |
| Date/time | 2026-05-24, ~21:20 UTC+1 |
| Method | Playwright browser_snapshot (accessibility tree) + targeted grepping of full-page DOM snapshot |
| Fresh report? | Yes — page loaded fresh after login redirect |
| Limitations | Biomarker cards read in collapsed state from initial snapshot; one card (Homocysteine) expanded via click to confirm expansion state. Full-page screenshot taken. Collapsed accordions (Clinician summary, Health domains, Advanced analysis) not opened — assessed from their headings and descriptions only. |

---

## 3. Rendered journey order

**Actual visible order:**

| # | Section visible | Status | Quality (1–10) |
|---|---|---|---|
| — | Header: "Your results" + description + 77 markers count | Present, visible | 7 |
| — | AI disclaimer banner | Present, visible | 6 |
| — | "How to read this page" [h2] wrapper containing: | Container section — confusing label | 3 |
| 1 | → Primary finding hero card ("Homocysteine Elevation Context") | Present, visible — but nested under wrong heading | 6 |
| 2 | → "Your body overview" | Present, visible — but nested under "How to read this page" | 5 |
| — | → "Summary" (separate card inside same wrapper) | Redundant — same content as body overview, repeated | 3 |
| 3 | "What's working well" | Present, visible | 6 |
| 4 | "Primary finding and why" | Present, visible | 6 |
| 5 | "Why this lead won · uncertainty" | Present, visible | 6 |
| 6 | "Patterns across your body" | Present, visible — one IDL pattern | 7 |
| 7 | "Marker-level evidence" (all markers grid) | Present, visible — very large section | 5 |
| 8 | "What to do next" | Present, visible | 5 |
| — | "Health domains" | Collapsed | n/a |
| — | "Additional interpretation context" | Collapsed | n/a |
| 9 | "Clinician summary" | Collapsed — appropriately separated | 6 |
| — | "Advanced analysis" | Collapsed | n/a |

**Comparison against intended v6 order:**

| Intended position | Intended section | Present? | Quality | Notes |
|---|---|---|---|---|
| 1 | Your body overview | Partial | 5/10 | Nested inside "How to read this page" wrapper — wrong outer label |
| 2 | What's working well | Present | 6/10 | Technical parenthetical ("interpretation confidence for this read: insufficient") leaking through |
| 3 | Primary finding and why | Present | 6/10 | Section label ("B12-associated pattern") differs from hero label ("Homocysteine Elevation Context") |
| 4 | Why this lead won / uncertainty | Present | 6/10 | Appropriately separate |
| 5 | Patterns across your body | Present | 7/10 | FE-R5A pattern correctly placed and guarded |
| 6 | Marker-level evidence | Present | 5/10 | Expansion content nearly empty for primary markers |
| 7 | What to do next | Present | 5/10 | Fallback message visible; bullet formatting broken |
| 8 | Clinician summary | Collapsed | 6/10 | Appropriately gated |

---

## 4. Section-by-section human quality audit

| Section | Exact representative prose | Asset/source (if identifiable) | Human quality score | Issue | Recommendation |
|---|---|---|---|---|---|
| Header | "Your results" / "This page walks through your results in order: whole-body context, what looks stable, your main finding, uncertainty, marker evidence, and follow-up — with a separate clinician summary below." | `results/page.tsx` static | 7/10 | Good description of the journey; concise | Minor: "whole-body context" could be "body overview" to match section names |
| AI disclaimer | "Your report is built from structured clinical rules applied to your lab data. AI-personalised narrative is not active in this view." | Static | 6/10 | Accurate but slightly clinical | Acceptable; consider softening "not active in this view" |
| "How to read this page" framing | "Sections below build on each other: orientation first, then what looks stable, your main finding and why it led, how confident we are, patterns across your body when available, marker evidence, and suggested follow-up. Open optional sections at the bottom for health domains, extra context, or the clinician handoff." | Static / `feR2ResultsJourneyOrder.ts` | 4/10 | The framing text is decent, but it is labeled as "How to read this page" [h2] while also containing the hero card and body overview — section identity is broken | Rename outer wrapper. The hero card should be inside "Your body overview", not inside a section called "How to read this page". Or demote "How to read this page" to a non-heading disclosure block. |
| Primary finding hero | "Homocysteine Elevation Context: warrants attention on this panel" / "Main system context: Vascular Inflammation Risk" / "Accumulating vascular-risk signals warrant cardiometabolic review and lifestyle action. A pattern combining inflammation and homocysteine signals associated with vascular risk — Homocysteine, Vitamin B12, Folate, Transferrin" | `arbitration_result` / IDL hero fields | 6/10 | Clear signal; appropriate framing. But "A pattern combining inflammation and homocysteine signals associated with vascular risk Homocysteine…" is missing a dash/separator before the biomarker list, reads as a run-on | Minor prose fix. Also the "Download report" button inside the hero card is unexpected placement. |
| Your body overview | "Your results highlight homocysteine elevation context as the main pattern to discuss first, alongside the wider marker and domain context below. Your questionnaire suggests moderate alcohol intake, which can be relevant when interpreting homocysteine because alcohol intake may increase demand on one-carbon nutrients such as folate and B vitamins. This does not change your biomarker score, but it helps explain why this pathway is worth reviewing. **Your lifestyle inputs suggest additional metabolic context on this panel (for example weight, sleep, alcohol, or smoking patterns). This is used only to adjust how systems are weighted in the analytical model — not to alter the lab values on this panel.**" | `narrative_report_v1.body_overview` | 4/10 | **Critical**: "This is used only to adjust how systems are weighted in the analytical model" — this is model-explainer language that breaks the consumer surface. Also "Related systems also noted on this panel: Autonomic, Cardiovascular, Hematological, Hepatic, Hormonal, Immune, Metabolic, Musculoskeletal, plus 3 other related areas" is a dumped system list, not a narrative. Dense single paragraph. | Backend/compiler prose cleanup required. The model-explainer sentence must be removed or replaced with consumer-facing language. System list needs prose wrapping. |
| Pattern groups counter | "Needs attention: 0 / Explore further: 0 / Stable on this panel: 3 / 3 pattern groups in this run." | `system_capacity_scores` or pattern group count | 2/10 | **Critical mismatch**: The page then presents a "Strong Signal" homocysteine finding, but the pattern counter says "Needs attention: 0". This directly contradicts the lead finding. A paying user will ask: "If nothing needs attention, why am I worried about homocysteine?" | Data integrity / display logic bug. The counter must reflect the lead finding status, or the counter must be removed/reframed. |
| Summary (redundant section) | "Your main result pattern centres on homocysteine elevation context, with Homocysteine as the primary marker on this panel. Other areas of the panel still matter, but this pattern is the best starting point for follow-up with your clinician. Homocysteine Elevation Context warrants attention on this panel, with homocysteine as the main marker on this panel." | `narrative_report_v1` or compiled summary | 3/10 | **Redundant**: Last sentence is near-verbatim repetition of the first. The entire section duplicates what the hero card and body overview already say. | Remove or consolidate. This section adds no user value. |
| What's working well | "On this panel, markers grouped under this system look broadly within expected ranges (interpretation confidence for this read: insufficient)." | `balanced_systems_v1` | 4/10 | **Technical parenthetical**: "(interpretation confidence for this read: insufficient)" is a scoring artifact visible to users. Also only 2 systems shown (Hematological, Renal) — a thin set for a 77-marker panel. | Remove "interpretation confidence for this read: insufficient" from consumer view; show it only behind the "Show technical detail" toggle. |
| Primary finding and why | Sub-label: "B12-associated pattern" / "MCV is elevated, which can be consistent with a megaloblastic nutrient pattern in context." / "B12 appears clearly within range, which makes a B12-driven pattern less likely on this panel alone." / "Methylmalonic Acid: MMA can help evaluate functional B12 deficiency when homocysteine is elevated." | `root_cause_v1` / evidence chains | 7/10 | Good: shows supports / pulls-against / what would clarify. Real reasoning chain. **BUT**: Label "B12-associated pattern" conflicts with "Homocysteine Elevation Context" from the hero — two different names for the same finding. | Fix label to match hero label, or clarify the relationship. Evidence structure is correct and should be preserved. |
| Why this lead won · uncertainty | "The panel has enough information to identify a lead pattern. Some confirmatory markers were not included, which limits how specific the story can be." / "Given available markers, confidence is constrained by missing or partial reference-range context." / "We received 8 of 8 expected markers for this interpretation. Core quality checks passed." | `clinician_report_v1` confidence fields | 6/10 | Appropriate framing. Trust strip ("8 of 8 expected markers") is a good differentiator. "Confidence is constrained by missing or partial reference-range context" is a slightly technical phrase but acceptable. | Minor polish. |
| Patterns across your body | "Methylation pathway pattern" / "Homocysteine elevation with larger red-cell index suggesting one-carbon / marrow context" / "This pattern links nutrient–cofactor networks to vascular and blood-cell maturation questions that deserve coherent follow-up, not a single-marker snapshot." / Supporting markers: Homocysteine, Vitamin B12, Folate, Transferrin | IDL `records[]` via `selectSafeIdlPatternRecords` | 7/10 | Consumer-safe label. Good "why it matters" copy. Supporting markers correctly listed. Correct placement (after uncertainty, before marker evidence). | Acceptable. "one-carbon / marrow context" in the subtitle may need polish in KB-WAVE but is not a blocker. |
| Marker-level evidence (biomarker cards collapsed) | "Transferrin 2 g/L · Critical" / "Cholesterol (venous) 5.3 mmol/L / Range: 0–5.18 mmol/L / Scored 30.5/100" / "Total Cholesterol/hdl Ratio Calculation (venous): Range: 0–5 mmol/L — Not scored - result unit and lab reference range unit cannot be aligned for this marker (incompatible units); check units on the report." | DTO biomarker cards | 4/10 | **Multiple issues**: (1) "Transferrin · Critical" is alarming without context — Transferrin 2 g/L looks like it may be within lab range; "Critical" label needs explanation or softening. (2) TC/HDL Ratio unit error ("0–5 mmol/L" for a ratio). (3) "Not scored - result unit and lab reference range unit cannot be aligned… check units on the report" is a raw technical error message. (4) ALT 7.0 U/L is below its range (10–49 U/L) yet "Scored 73.1/100" — this is confusing. | Fix unit label on TC/HDL ratio. Replace technical error message with consumer-safe fallback. "Critical" label needs review. |
| Biomarker card expansion (Homocysteine) | Heading: "Homocysteine" / Sub-heading: "What this result means now" / Content: "Scored using lab reference range" | `interpretation` field from DTO | 1/10 | **Critical FE-R3 failure**: Homocysteine expanded card shows only the scoring method, not interpretation text. No contribution context, no education, no explanation of clinical meaning. This is the primary marker of concern and it has the most important expansion opportunity — wasted. | FE-R3 intended `interpretation`, `contribution_context.factual_statement`, and `biomarker_educational_explainer` to populate these zones. Either the DTO is not supplying these fields for this marker, or the rendering is not triggered. Must be diagnosed and fixed. |
| What to do next | "• Discuss these findings with a clinician who knows your history. • Monitor trends on the cadence your clinician recommends. • Repeat priority markers when your clinician advises retesting. • Consider discussing Methylmalonic acid (MMA) with your clinician. • Consider discussing Full blood count (MCV/haemoglobin/RDW) with your clinician. • Consider discussing Repeat homocysteine with your clinician. Suggested follow-up themes:" | `next_steps` fields | 5/10 | Steps are clinically appropriate. **But**: (1) All bullets are concatenated into a single text block with "Suggested follow-up themes:" dangling at the end — looks like a rendering artefact. (2) "No separate checklist of follow-up lines was packaged with this result. The sections below still describe what to discuss next." is a raw fallback message. (3) Only 1 confirmatory test shown (MMA). | Fix bullet rendering. Remove/replace the fallback message with clean copy. |
| Internal field labels (uploaded values) | "Linked to tc hdl ratio" / "Linked to hba1c" | `uploaded_panel_values` source fields | — | **FE-R1 safety remnant**: Raw internal field labels appearing in user-facing expanded section | Remove. Replace with consumer-friendly source note or omit entirely. |
| Clinician summary | Collapsed ("Professional handoff, export-oriented synthesis, and technical detail for clinical review.") | Collapsed disclosure | 7/10 | Appropriately gated. Separator line is clear. Description is good. | Acceptable. Not opened in this audit. |

---

## 5. FE-R1 safety regression check

**Verdict: CONDITIONAL PASS**

Core FE-R1 forbidden strings — searched across full rendered accessibility tree:
- `ranked lead` — NOT FOUND
- `lab anchor` — NOT FOUND
- `thread` — NOT FOUND
- `governed label` — NOT FOUND
- `moderate_by_default` — NOT FOUND
- `confidence weight` — NOT FOUND
- `structured ranking only` — NOT FOUND
- `Functional read —` — NOT FOUND
- `Prioritised follow-up (governed assets)` — NOT FOUND
- `Clinician-structured` — NOT FOUND
- `0.90 vs 0.90` — NOT FOUND
- `Hypercortisolism` — NOT FOUND
- raw signal labels (e.g., `Lh High`, `Alp Low`) — NOT FOUND
- `": is outside the optimal range on this panel"` — NOT FOUND

**Leakage found (outside core FE-R1 list):**

| String | Location | Likely source | Severity |
|---|---|---|---|
| `"Linked to tc hdl ratio"` | Uploaded panel values section (Tc Hdl Ratio card) | Raw `linked_to` field from DTO — internal alias reference | High — internal field label visible to users |
| `"Linked to hba1c"` | Uploaded panel values section (HbA1c equivalent card) | Same | High |
| `"Not scored - result unit and lab reference range unit cannot be aligned for this marker (incompatible units); check units on the report."` | TC/HDL Ratio biomarker card | Internal scoring engine error message surfaced directly | Medium — raw technical error |
| `"interpretation confidence for this read: insufficient"` | What's working well — Hematological and Renal entries | `balanced_systems_v1` confidence field exposed in consumer copy | Medium — technical scoring artifact |

These four strings are not in the original FE-R1 forbidden list but represent the same class of safety concern: internal artifacts visible on the retail surface.

---

## 6. FE-R2 journey restructure check

**Verdict: PASS WITH STRUCTURAL NOTE**

- ✓ Page is no longer accordion-dominated — the main content is open by default
- ✓ Body overview appears near the top (nested inside the "How to read this page" container, immediately after hero)
- ✓ What's working well appears before primary finding
- ✓ Primary finding appears before uncertainty
- ✓ Marker evidence is in the main journey (not collapsed)
- ✓ Clinician summary is separate, at the bottom, collapsed

**Structural note (not a hard FE-R2 failure but a real UX problem):**  
The outer container heading is "How to read this page" [h2], but it contains the primary finding hero card, the body overview, and a summary card. A user reading the page structure would see:  
> *How to read this page → [Lead finding hero] → [Body overview] → [Summary]*

This is semantically broken. "How to read this page" communicates "tutorial framing," not "primary findings." The correct fix is to demote the framing text to a non-heading inline note inside the body overview section, so the user sees a clean journey with "Your body overview" as the first named section.

---

## 7. FE-R3 evidence depth check

**Verdict: FAIL**

- ✗ **Biomarker expansion content is absent for primary markers.** Homocysteine card expanded → shows only "What this result means now" / "Scored using lab reference range." No interpretation text, no contribution context, no biomarker education.
- ✓ Biomarker cards are visible in the main journey (not collapsed behind Advanced accordion)
- ✓ "What's driving this" section shows a short driver list (Homocysteine 16.23 · Elevated, Total Cholesterol 5.26 · Elevated, Transferrin 2 · Critical)
- ✗ Contribution context ("How this fits the wider pattern") — not visible in expanded Homocysteine card
- ✗ Biomarker education — not visible in expanded Homocysteine card
- ✗ FE-R3 `BiomarkerDetailZones` expansion zones (`interpretation`, `contribution_context.factual_statement`, `biomarker_educational_explainer`) do not appear to be populating for this panel's primary biomarkers
- ✓ "Tests to discuss" section exists (MMA listed with rationale)
- ~ Confirmatory test duplication: MMA appears in "Primary finding and why" (what would clarify) and "Tests to discuss" — some duplication but tolerable given the different context framing

The FE-R3 goal was to make biomarker cards feel "premium and unusually rich" relative to conventional blood reports. For the most important marker on this panel (Homocysteine), the expansion is empty. This is the most commercially damaging defect on the current page.

---

## 8. FE-R5A pattern surface check

**Verdict: PASS**

- ✓ "Patterns across your body" section appears in the main journey
- ✓ Positioned correctly: after "Why this lead won · uncertainty" and before "Marker-level evidence"
- ✓ Consumer-safe label used: "Methylation pathway pattern" (not a raw cluster name)
- ✓ Scientific class chip: "Health pattern" (not a clinical-only label)
- ✓ Severity chip: "Strong Signal"
- ✓ Why it matters copy present: "This pattern links nutrient–cofactor networks to vascular and blood-cell maturation questions that deserve coherent follow-up, not a single-marker snapshot."
- ✓ Supporting markers listed: Homocysteine, Vitamin B12, Folate, Transferrin
- ✓ `clusters[]` names not used as pattern labels
- ✓ No pretence of being the full phenotype layer

One IDL record surfaced — appropriate given available data. FE-R5A safeguards appear to be working.

---

## 9. Repetition / incoherence / density findings

| Problem text or pattern | Where seen | Why it harms comprehension | Likely source | Fix type |
|---|---|---|---|---|
| Pattern counter "Needs attention: 0" but strong homocysteine signal elsewhere | Body overview → pattern groups block | Direct contradiction — user reads zero concerns then finds a "Strong Signal" finding | Display logic bug — counter not reflecting lead finding status | Frontend copy cleanup / display logic fix |
| "Summary" section repeating hero + body overview content | Inside "How to read this page" wrapper | Three near-identical statements about homocysteine being the main concern; users stop reading | Compiled `summary_section` separate from `body_overview` | Omit from UX — merge into body overview or remove |
| "This is used only to adjust how systems are weighted in the analytical model — not to alter the lab values on this panel" | Body overview | Model-explainer language on retail surface; breaks consumer trust and sounds defensive | `narrative_report_v1.body_overview` compiled prose | Backend/compiler prose cleanup |
| "interpretation confidence for this read: insufficient" | What's working well — Hematological and Renal entries | Technical scoring artifact surfaced in consumer list items | `balanced_systems_v1` | Frontend copy cleanup — hide behind "Show technical detail" toggle |
| "Related systems also noted on this panel: Autonomic, Cardiovascular, Hematological, Hepatic, Hormonal, Immune, Metabolic, Musculoskeletal, plus 3 other related areas" | Body overview | Raw system-group dump; not a narrative; not meaningful to a user | `system_capacity_scores` field join | Frontend copy cleanup — either omit or rewrite as prose |
| "B12-associated pattern" (primary finding sub-label) vs "Homocysteine Elevation Context" (hero label) | Primary finding and why section vs hero card | Two different names for the same lead finding confuses user and reduces product coherence | Different source fields used in different components | Frontend copy cleanup — align labels |
| "Suggested follow-up themes:" dangling at end of bullet block | What to do next | Looks like a rendering artefact; implies more content that isn't there | Compiled next-steps block with trailing label | Frontend copy cleanup |
| "No separate checklist of follow-up lines was packaged with this result. The sections below still describe what to discuss next." | What to do next | Raw fallback message showing in primary user journey | Conditional fallback in `results/page.tsx` | Frontend copy cleanup — replace with clean fallback or omit |
| "Linked to tc hdl ratio" / "Linked to hba1c" | Uploaded panel values | Internal field labels on consumer surface | `linked_to` field from uploaded_panel_values DTO | DTO/source contract issue — strip or rename field before surfacing |
| "Not scored - result unit and lab reference range unit cannot be aligned for this marker (incompatible units); check units on the report." | TC/HDL Ratio biomarker card | Raw engineering error message on retail surface | Scoring engine internal message surfaced through DTO | Frontend copy cleanup — replace with consumer-safe fallback |

---

## 10. Commercial/user value assessment

**Would a paying user understand why HealthIQ is better than a normal blood report?**  
Weakly, yes. The journey order, the "Patterns across your body" section, and the evidence-for / evidence-against structure in the primary finding section are differentiated from a standard blood report. But the "wow" is not landing because the entry point is confusing (buried under "How to read this page"), the body overview has model prose in it, and the biomarker expansions are empty.

**Would they feel reassured where appropriate?**  
Partially. "What's working well" exists and names stable systems. But the pattern counter saying "Needs attention: 0" while the main finding is a "Strong Signal" undermines trust rather than building it.

**Would they understand the primary concern?**  
Yes — the homocysteine elevation narrative is clear across the hero, primary finding, and patterns sections. This is the strongest part of the page.

**Would they understand what to do next?**  
Barely. The next steps are clinically appropriate but rendered as a formatting mess (one concatenated text block, dangling heading, fallback message). A user would have to work to extract the actionable items.

**Would they see biomarker-level value?**  
No. They would click "Expand" on the Homocysteine card expecting insight and see "Scored using lab reference range." That is worse than a conventional blood report. This is the single most damaging UX failure.

**Does the page feel premium, or still prototype-like?**  
Prototype-like, but less so than before FE-R1/R2/R3. The navigation and section structure are clean. The content quality is inconsistent — some sections feel polished, others feel unfinished. The empty biomarker expansions, technical leakage strings, and formatting artefacts in "What to do next" tip the page toward prototype.

---

## 11. Remaining blockers before KB-WAVE-1

| Blocker | Severity | Blocks KB-WAVE-1? | Recommended sprint |
|---|---|---|---|
| Biomarker card expansion shows no interpretation content (FE-R3 rendering failure) | Critical | YES — KB-WAVE-1 adds depth that cannot render | Diagnose why `interpretation`, `contribution_context`, and `biomarker_educational_explainer` are not populating expansion zones for this panel. Fix the rendering path. |
| "How to read this page" wrapping hero + body overview — broken section identity | High | Soft — reduces product coherence | FE-R6A frontend defect sprint — demote framing text; rename/restructure outer wrapper |
| Pattern groups counter contradiction ("Needs attention: 0" vs strong homocysteine signal) | High | YES — introduces factual contradiction | FE-R6A defect sprint — fix counter to reflect lead finding, or remove counter |
| Body overview model-explainer prose ("...adjust how systems are weighted in the analytical model") | High | Soft | Backend/compiler prose cleanup sprint |
| "Linked to tc hdl ratio" / "Linked to hba1c" internal labels | High | Soft | FE-R6A defect sprint — strip from DTO surface |
| "Summary" section content duplication | Medium | No | FE-R6A defect sprint — remove section |
| "interpretation confidence for this read: insufficient" in What's working well | Medium | No | FE-R6A defect sprint — gate behind "Show technical detail" |
| What to do next formatting artefacts (concatenated bullets, dangling heading, fallback message) | Medium | No | FE-R6A defect sprint |
| TC/HDL ratio unit error + raw error message | Medium | No | FE-R6A defect sprint |
| Finding label inconsistency ("B12-associated pattern" vs "Homocysteine Elevation Context") | Medium | No | FE-R6A defect sprint |
| Body overview system list dump | Low | No | Backend/compiler prose cleanup — can wait for KB-WAVE |

---

## 12. Recommended next sprint

**Recommendation: Small frontend defect cleanup sprint (FE-R6A or equivalent)**

Do not proceed to KB-WAVE-1 yet. The reason is direct:

KB-WAVE-1's purpose is to add interpretation depth to lipid markers (LDL, ApoB). That depth surfaces through biomarker card expansion. The current expansion rendering path for this panel's primary marker (Homocysteine) shows zero interpretation content. If that rendering path is broken, any content KB-WAVE-1 generates for LDL/ApoB will also fail to display. Building content for a broken render surface is waste.

The FE-R6A sprint should address:
1. **Diagnose and fix biomarker expansion rendering** — why are `interpretation`, `contribution_context`, and `biomarker_educational_explainer` not populating? Is the DTO returning them for this panel? Is the component logic gating them out?
2. **Fix "How to read this page" structural issue** — demote the framing text to an inline note; "Your body overview" should be the first named section the user sees
3. **Fix pattern groups counter** — zero "Needs attention" while strong signal is present is a direct contradiction
4. **Remove internal field labels** — "Linked to tc hdl ratio", "Linked to hba1c"
5. **Fix What to do next rendering** — concatenated bullets, dangling heading, fallback message
6. **Remove Summary section** (duplicate content)
7. **Gate "interpretation confidence" text** behind Show technical detail toggle
8. **Align finding labels** across hero card and Primary finding and why section

Once those 8 items are resolved, the page will be commercially demonstrable and KB-WAVE-1 will have a render surface that can actually display its content.

After FE-R6A: proceed to KB-WAVE-1 (LDL/ApoB lipid WHY expansion).

---

## 13. Appendix — raw visible transcript (page order)

### Header region
> **Your results**  
> "This page walks through your results in order: whole-body context, what looks stable, your main finding, uncertainty, marker evidence, and follow-up — with a separate clinician summary below."  
> 77 markers | [Show technical detail] [Export] [Share]

### AI disclaimer
> "Your report is built from structured clinical rules applied to your lab data. AI-personalised narrative is not active in this view."

### "How to read this page" [h2]
> "Sections below build on each other: orientation first, then what looks stable, your main finding and why it led, how confident we are, patterns across your body when available, marker evidence, and suggested follow-up. Open optional sections at the bottom for health domains, extra context, or the clinician handoff."

#### Primary finding hero (nested inside "How to read this page")
> **Primary finding**  
> **Homocysteine Elevation Context: warrants attention on this panel**  
> Main system context: Vascular Inflammation Risk | [Strong Signal]  
> "Accumulating vascular-risk signals warrant cardiometabolic review and lifestyle action. A pattern combining inflammation and homocysteine signals associated with vascular risk Homocysteine, Vitamin B12, Folate, Transferrin"  
> [Download report]

#### Your body overview (nested inside "How to read this page")
> "Your results highlight homocysteine elevation context as the main pattern to discuss first, alongside the wider marker and domain context below. Your questionnaire suggests moderate alcohol intake, which can be relevant when interpreting homocysteine because alcohol intake may increase demand on one-carbon nutrients such as folate and B vitamins. This does not change your biomarker score, but it helps explain why this pathway is worth reviewing. Your lifestyle inputs suggest additional metabolic context on this panel (for example weight, sleep, alcohol, or smoking patterns). This is used only to adjust how systems are weighted in the analytical model — not to alter the lab values on this panel. Your main finding sits in a Cardiovascular 4 Biomarkers context — this is where the panel places most interpretive weight. Related systems also noted on this panel: Autonomic, Cardiovascular, Hematological, Hepatic, Hormonal, Immune, Metabolic, Musculoskeletal, plus 3 other related areas. Most other system groups look broadly stable on this panel compared with the lead focus — that helps place the concern in perspective rather than suggesting the whole panel is off track."
>
> Pattern groups on this panel:  
> Needs attention: **0** | Explore further: **0** | Stable on this panel: **3**  
> 3 pattern groups in this run.

#### Summary (nested inside "How to read this page")
> "Your main result pattern centres on homocysteine elevation context, with Homocysteine as the primary marker on this panel. Other areas of the panel still matter, but this pattern is the best starting point for follow-up with your clinician. Homocysteine Elevation Context warrants attention on this panel, with homocysteine as the main marker on this panel."

### What's working well [h2]
> "Not every system group shows strain on this panel. The patterns below look broadly stable or well-regulated, based on the same structured engine that flags concerns."
>
> - **Hematological**: "On this panel, markers grouped under this system look broadly within expected ranges (interpretation confidence for this read: insufficient)."
> - **Renal**: "On this panel, markers grouped under this system look broadly within expected ranges (interpretation confidence for this read: insufficient)."
>
> "The headline interpretation above focuses on Cardiovascular. Several other groups still look broadly in-range—this helps place concerns in context rather than suggesting the whole panel is off track. Groups with reassuring patterns here include: Hematological, Renal."

### Primary finding and why [h3]
> Sub-label: **B12-associated pattern**
>
> "Technical ranking references and evidence-chain wording are hidden by default. Turn on **Show technical detail** above to review them when you need them."
>
> **Supports this interpretation:**
> - "MCV is elevated, which can be consistent with a megaloblastic nutrient pattern in context. (related markers: Mcv)"
>
> **Pulls against or complicates it:**
> - "B12 appears clearly within range, which makes a B12-driven pattern less likely on this panel alone. (related markers: Vitamin B12)"
>
> **What would clarify the picture:**
> - **Methylmalonic Acid:** MMA can help evaluate functional B12 deficiency when homocysteine is elevated.

### Why this lead won · uncertainty [h2 / h3]
> "How the headline was chosen, what else was close, and how much room for doubt remains on this panel."
>
> **Confidence and limits**  
> "The panel has enough information to identify a lead pattern. Some confirmatory markers were not included, which limits how specific the story can be."
>
> "Given available markers, confidence is constrained by missing or partial reference-range context."
>
> **Trust strip**: Quality checks passed  
> "We received 8 of 8 expected markers for this interpretation. Core quality checks passed."

### Patterns across your body [h2]
> "These patterns summarise how related markers group together on your panel. They support the story above — they are not a diagnosis on their own."
>
> **Methylation pathway pattern** [Health pattern] [Strong Signal]  
> "Homocysteine elevation with larger red-cell index suggesting one-carbon / marrow context"
>
> **Why this matters:** "This pattern links nutrient–cofactor networks to vascular and blood-cell maturation questions that deserve coherent follow-up, not a single-marker snapshot."  
> **Supporting markers:** Homocysteine, Vitamin B12, Folate, Transferrin

### Marker-level evidence [h2]
> "Values and reference ranges from your uploaded panel. Expand a marker for brief context when available."
>
> **What's driving this [h3]**
> - Homocysteine: 16.23 umol/L · Elevated — Scored using lab reference range
> - Total Cholesterol: 5.26 mmol/L · Elevated — Scored 30.5/100
> - Transferrin: 2 g/L · Critical — Scored using lab reference range
>
> [See all markers]
>
> **All markers on this run [h2]** (77 biomarker cards, all with Expand buttons)
>
> Representative issues:
> - HbA1c (venous): 26.0 mmol/mol — Scored 100.0/100
> - Cholesterol (venous): 5.3 mmol/L — Range: 0–5.18 mmol/L — Scored 30.5/100
> - Total Cholesterol/hdl Ratio Calculation (venous): 2.4 ratio — Range: 0–5 mmol/L — "Not scored - result unit and lab reference range unit cannot be aligned for this marker (incompatible units); check units on the report."
> - Alanine Aminotransferase Alt (venous): 7.0 U/L — Range: 10–49 U/L — Scored 73.1/100
> - Homocysteine (venous): 16.2 µmol/L — Range: 3.7–13.9 µmol/L — Scored using lab reference range — Score dial: 19
>
> **Homocysteine card expanded:**  
> "What this result means now" → "Scored using lab reference range" ← ONLY CONTENT
>
> **Uploaded panel values section:**
> - "Linked to hba1c"
> - "Linked to tc hdl ratio"

### What to do next [h2]
> **Direction and follow-up [h3]**
> "How markers moved relative to prior data when available, and suggested next actions."
>
> Next steps: "• Discuss these findings with a clinician who knows your history. • Monitor trends on the cadence your clinician recommends. • Repeat priority markers when your clinician advises retesting. • Consider discussing Methylmalonic acid (MMA) with your clinician. • Consider discussing Full blood count (MCV/haemoglobin/RDW) with your clinician. • Consider discussing Repeat homocysteine with your clinician. **Suggested follow-up themes:**"
>
> **Tests to discuss with your clinician [h3]**
> - Methylmalonic acid (MMA): "Consider discussing methylmalonic acid (MMA) testing with your clinician to evaluate functional B12 deficiency."
>
> [Open Actions hub] for the full set of follow-ups (up to eight) from your most recent completed analysis.
>
> "**No separate checklist of follow-up lines was packaged with this result. The sections below still describe what to discuss next.**"

### Collapsed sections (bottom of page)
> **Health domains** — "High-level domain scores — supplementary to the main journey above." [Show]  
> **Additional interpretation context** — "Orientation helpers and longer narrative detail when you want more depth." [Show]  
> **Clinician summary** — "Professional handoff, export-oriented synthesis, and technical detail for clinical review." [Show]  
> **Advanced analysis** — "Overall score, system groups, optional narrative summaries, and extended technical views." [Show]
