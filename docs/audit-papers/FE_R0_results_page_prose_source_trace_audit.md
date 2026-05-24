# FE-R0 — Results Page Prose Source Trace Audit

---

## 1. Executive verdict

**The current page does not match the intended guided reasoning journey.** The prose does not tell a coherent story. The problems are structural, ordering-related, and source-level — all three simultaneously.

**Structural:** The v6 section hierarchy (body overview → reassurance → primary finding → uncertainty → patterns → evidence → insights → next steps → clinician) does not exist. The page is a mixture of hero, cards, a disclosure accordion, and collapsed sections, with no clear guided sequence.

**Ordering:** `BalancedSystemsSummary` ("What's working well") appears after three other sections and shows an empty fallback. `Wave1DomainCards` — not in the v6 journey at all — sit above the first trust-building section. The biomarker evidence is buried behind a collapsed "Advanced" accordion. The clinician-level hypothesis block appears in the middle of the retail journey, labelled "Clinician-structured 'why' and evidence", which is a retail-hostile heading.

**Source prose:** The single most damaging issue is `narrative_report_v1.lead_narrative`. This field is surfaced verbatim into a section titled "What this means" as the "Primary focus" block. Its content is hundreds of words of raw mechanism text including internal labels (`(governed label): moderate_by_default`), raw numerical confidence weights (`confidence weight 0.60 — structured ranking only`), and a full dump of all four hypotheses with their evidence structures. This is KB asset content that has not been compiled into consumer copy — it is rendered directly to retail users.

The `narrative_report_v1.retail_summary` ("Summary" card) is the second most damaging block. It opens with "The ranked lead pattern is Homocysteine Elevation Context (suboptimal), centred on Homocysteine" — a compiler describing its own output. The card contains a self-referential meta-commentary line: "This wording stays descriptive and does not replace clinician judgement or imply certainty beyond what the markers support." This is an internal compiler guard, not consumer copy.

The hero title — "Homocysteine Elevation Context: is outside the optimal range on this panel" — is a raw template string from the clinician compiler. It is not a consumer headline. The colon and the phrase "is outside the optimal range on this panel" are template artifacts.

Confidence scores are exposed numerically throughout the page: "0.90 vs 0.90" in the runner-up section, "confidence weight 0.60" in the lead narrative, "Overall confidence for this lead pattern: 0.90" in the confidence block.

**The main problem is not presentation or ordering alone.** Several key prose blocks are raw compiler output or unedited KB content rendered directly to the consumer surface. No amount of reordering will fix them. They need backend/compiler fixes first.

---

## 2. Page inspected

| Field | Value |
|---|---|
| URL | `http://localhost:3000/results?analysis_id=7aacc734-95cf-4ea5-a19c-0d03d98dd2e9` |
| analysis_id | `7aacc734-95cf-4ea5-a19c-0d03d98dd2e9` |
| Login used | test-user3@example.com |
| Date / time | 2026-05-24 |
| Method | Playwright browser snapshot (accessibility tree + screenshot) |
| Limitations | Backend CORS issues from Playwright context; page was loaded via user's browser session and confirmed loaded. Snapshot reflects actual rendered DOM. "Advanced & clinician report" and "Actions" sections were collapsed at load — not captured in this audit. |

---

## 3. Intended journey reference

Per `docs/frontend/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md`:

1. **Your body overview** — calm, balanced whole-body orientation; embedded short "how to read this page" framing; `arbitration_result`, `system_capacity_scores`, `clinician_report_v1.sections.page1`
2. **What's working well** — stable/resilient systems before strain; `balanced_systems_v1`
3. **Primary finding and why** — lead pattern with explanatory depth; `top_hypothesis_line`, `chains[]`, `root_cause_v1`
4. **Why this lead won / uncertainty** — transparency immediately after lead; `runner_up_topic_line`, `runner_up_why_not_lead_line`, `confidence_and_missing_data`
5. **Patterns across your body** — Phase 2, gated
6. **Marker-level evidence** — biomarkers with contribution context and educational expansion
7. **Key body-level insights** — optional, deterministic Layer C features only when robust
8. **What to do next** — prioritised by safety class; `confirmatory_tests[]`, `actions`, `next_steps[]`
9. **Clinician summary** — professional handoff, separate from retail flow

---

## 4. Current rendered page order

As seen on the page (top to bottom):

1. Page header: "Your results" + utility buttons + marker count
2. Mock mode disclosure alert
3. **Primary finding hero** (ResultsPrimaryHero) — hero title, severity badge, summary body, download button
4. **Summary card** (NarrativeRetailSummaryCard) — "Summary" heading, long retail summary text
5. **What's driving this** (ResultsDrivingSignals) — 2 marker rows
6. **Your health domains** (Wave1DomainCards) — 3 domain cards: Cardiovascular, Blood sugar, Liver
7. **Your system health** (BalancedSystemsSummary) — EMPTY FALLBACK
8. **Data quality** (PipelineStatus) — trust strip
9. **"What this means" disclosure** (open by default), containing in order:
   - a. Body overview (ResultsBodyOverview)
   - b. Your investigation path (ResultsInvestigationSpine)
   - c. Patterns across your body (InterpretationPatternsSection)
   - d. How to understand your results (SystemUnderstandingSection)
   - e. Why this lead won · uncertainty (WhyThisLeadWonSection)
   - f. What this means (NarrativeLeadAndSupportingSections) ← TITLE COLLISION with parent accordion
   - g. Direction and follow-up (NarrativeLongitudinalAndNextSteps)
   - h. Clinician-structured "why" and evidence (PrimaryFindingAndWhy)
10. **Actions** disclosure (collapsed)
11. **Advanced & clinician report** disclosure (collapsed)
12. Footer buttons (Start New Analysis, Export results)

---

## 5. Section-by-section prose source map

| Page section / location | Exact visible prose | Frontend component/file | DTO/API field | Backend/compiler/source asset | Source classification | Human-quality issue | Recommended disposition |
|---|---|---|---|---|---|---|---|
| Page h1 | "Your results" | `results/page.tsx:579` | — | — | frontend static copy | Acceptable — neutral | keep |
| Page subtitle | "Start with your primary finding, then open deeper sections for patterns, actions, and the full technical report when you need it." | `results/page.tsx:580–583` | — | — | frontend static copy | Describes structure that doesn't match the page | rewrite frontend copy |
| Metadata line | "77 markers" | `results/page.tsx:623` | `biomarkers.length` | Orchestrator | DTO structured field | Acceptable | keep |
| Mock mode alert | "Your report is built from structured clinical rules applied to your lab data. AI-personalised narrative is not active in this view." | `lib/lcS4ResultsCopy.ts` | `meta.narrative_runtime` | Orchestrator meta | frontend static copy | Clinically honest; appropriate | keep |
| **Hero** label | "Primary finding" | `ResultsHeroBlocks.tsx:82` | — | — | frontend static copy | Acceptable label | keep |
| **Hero title** | "Homocysteine Elevation Context: is outside the optimal range on this panel" | `ResultsHeroBlocks.tsx:82–84`, `lib/resultsPageLayout.ts:resolveHeroPrimaryStory()` | `interpretation_display_layer_v1.records[0].retail_display_label` | `publish_interpretation_display_layer_v1` ← IDL YAML | governed Knowledge Bus asset | **Critical.** Colon and "is outside the optimal range on this panel" are raw template artifacts from the IDL label field. Not a consumer headline. | rewrite at backend source (IDL label field) |
| **Hero system context** | "Main system context: Vascular Inflammation Risk" | `ResultsHeroBlocks.tsx:85–87`, `resolveHeroPrimaryStory()` | derived from clusters/IDL | Frontend layout derivation | frontend-derived text | "Vascular Inflammation Risk" is an internal cluster/signal name, not consumer copy | rewrite at backend source |
| **Hero severity badge** | "Attention" | `ResultsHeroBlocks.tsx:89–95`, `resolvePrimaryFindingSeverity()` | `interpretation_display_layer_v1.records[0].severity_state` | IDL publish compiler | DTO structured field (formatted) | Acceptable — "Attention" is readable; amber tone appropriate | keep |
| **Hero body** | "Accumulating vascular-risk signals warrant cardiometabolic review and lifestyle action. A pattern combining inflammation and homocysteine signals associated with vascular risk Homocysteine, Vitamin B12, Folate, Transferrin" | `ResultsHeroBlocks.tsx:99`, `buildPrimaryHeroSummary()` | `narrative_report_v1.retail_summary` (first sentence) or clinician fields | `narrative_report_compiler_v1` | deterministic backend compiler prose | **Problem.** Biomarker names "Homocysteine, Vitamin B12, Folate, Transferrin" are concatenated directly onto the end of the prose sentence without grammatical connection — reads as a raw list appended to the sentence | rewrite at backend source |
| **Summary card** title | "Summary" | `DeterministicNarrativeSurface.tsx:51` | — | — | frontend static copy | Acceptable label | keep |
| **Summary card** desc | "A plain-language summary of the main pattern in your results." | `DeterministicNarrativeSurface.tsx:53` | — | — | frontend static copy | Acceptable | keep |
| **Summary card** body — sentence 1 | "The ranked lead pattern is Homocysteine Elevation Context (suboptimal), centred on Homocysteine." | `DeterministicNarrativeSurface.tsx` → `narrative_report_v1.retail_summary` | `narrative_report_v1.retail_summary` | `narrative_report_compiler_v1` | deterministic backend compiler prose | **Critical.** Compiler self-describing its own output. "The ranked lead pattern is..." is internal framing language. | rewrite at backend source |
| **Summary card** body — sentence 2 | "This is the priority focus for interpretation on this panel." | same | same | same | deterministic backend compiler prose | Acceptable message, but follows a bad opener | rewrite at backend source |
| **Summary card** body — sentence 3 | "Homocysteine Elevation Context is outside the optimal range on this panel." | same | same | same | deterministic backend compiler prose | Verbatim repeat of hero title (third time this phrase appears) | rewrite at backend source |
| **Summary card** body — sentence 4 | "The main lab anchor on this panel for this thread is homocysteine." | same | same | same | deterministic backend compiler prose | "Lab anchor" and "thread" are internal framing terms, not consumer language | rewrite at backend source |
| **Summary card** body — sentence 5 | "This wording stays descriptive and does not replace clinician judgement or imply certainty beyond what the markers support." | same | same | same | deterministic backend compiler prose | **Critical.** Internal compiler self-commentary rendered directly to consumer. Should never appear on the user-facing surface. | rewrite at backend source / omit from UX |
| **Summary card** body — IDL secondary content | "Methylation pathway pattern (pattern to watch): Homocysteine elevation with larger red-cell index suggesting one-carbon / marrow context. This pattern links nutrient–cofactor networks to vascular and blood-cell maturation questions that deserve coherent follow-up, not a single-marker snapshot." | same | same | same | deterministic backend compiler prose + governed Knowledge Bus asset (IDL) | Content duplicates the "Patterns" card below verbatim. Two separate sections showing identical text. | combine/deduplicate |
| **Driving signals** title | "What's driving this" | `ResultsHeroBlocks.tsx:142` | — | — | frontend static copy | Acceptable | keep |
| **Driving signals** desc | "Key markers behind the main pattern, using the values returned for this run." | `ResultsHeroBlocks.tsx:143` | — | — | frontend static copy | Acceptable | keep |
| **Driving signals** — Homocysteine row | "Homocysteine / 16.93 umol/L / · Elevated / Scored using lab reference range" | `ResultsHeroBlocks.tsx:148–164`, `oneLineMarkerInterpretation()` | `biomarkers[].biomarker_name`, `.value`, `.unit`, `.status`, `.interpretation` | Orchestrator biomarker scoring | DTO structured field + frontend-derived fallback | "Scored using lab reference range" is a boilerplate fallback when `interpretation` field is absent. Not informative. | rewrite at backend source |
| **Driving signals** — Alp row | "Alp / 38 U/L / · Critical / Scored using lab reference range" | same | same | same | DTO structured field + frontend-derived fallback | **Two problems:** (1) "Alp" is the raw snake_case key, not a display name. `formatBiomarkerDisplayName()` is called but not transforming this correctly. (2) "Critical" for ALP 38 is incorrect — ALP 38 is LOW, not critical by standard reference ranges. This may be a scoring engine error. | rewrite at backend source (status scoring) + fix display name |
| **Health domains** heading | "Your health domains" | `Wave1DomainCards.tsx:57` | — | — | frontend static copy | Acceptable | keep but move |
| **Health domains** desc | "High-level scores for three focus areas. Open a card for detail — not a diagnosis." | `Wave1DomainCards.tsx:59–61` | — | — | frontend static copy | Acceptable as a disclaimer | keep but move |
| **Cardiovascular card** desc | "A pattern combining inflammation and homocysteine signals associated with vascular risk" | `Wave1DomainCards.tsx:67–71` → `d.contributor_sentence` | `consumer_domain_scores[].contributor_sentence` | `assemble_consumer_domain_scores_v1` + `domain_narrative_wave1.py` | governed DTO (domain narrative compiler) | **Verbatim repeat** of hero body text opening. This same phrase has now appeared 3 times on the page. | rewrite at backend source |
| **Cardiovascular card** anchor | "Based mainly on: Vascular Inflammation Risk" | `Wave1DomainCards.tsx:78–82` → `d.evidence_anchor_sentence` | `consumer_domain_scores[].evidence_anchor_sentence` | domain narrative compiler | governed DTO | "Vascular Inflammation Risk" is an internal signal/cluster name, not consumer copy. | rewrite at backend source |
| **Cardiovascular card** headline | "Your cardiovascular read on this panel is not a simple all-clear: the leading pattern here still deserves clinical context alongside your numbers." | `Wave1DomainCards.tsx:91` → `d.headline_sentence` | `consumer_domain_scores[].headline_sentence` | domain narrative compiler | governed DTO | Acceptable consumer framing. Honest and non-alarming. | keep |
| **Blood sugar card** score | "100 / 100 / Strong / Limited confidence" | `Wave1DomainCards.tsx:86–90` | `consumer_domain_scores[].score`, `.band_label`, `.confidence_tier` | domain score assembler | DTO structured field | **Incoherent.** Score is 100/100 and band is "Strong" but confidence is "Limited". The headline then says "Your blood sugar and metabolic context still has active signals to address in care planning." A perfect score with an active-signals warning is contradictory. | rewrite at backend source |
| **Blood sugar card** desc | "HbA1c is within range on this panel. Glucose and insulin were not included, so a fuller glycaemic read would require those markers." | same → `d.contributor_sentence` | same | same | governed DTO | Acceptable and honest | keep |
| **Blood sugar card** headline | "Your blood sugar and metabolic context still has active signals to address in care planning, even if some results look in range on the surface." | same → `d.headline_sentence` | same | same | governed DTO | Contradicts the 100/100 score | rewrite at backend source |
| **Liver card** desc | "Your liver enzyme markers are within their reference ranges." | same | same | same | governed DTO | Acceptable | keep |
| **Liver card** headline | "Your liver health looks strong based on your current enzyme markers." | same | same | same | governed DTO | Acceptable but "Limited confidence" still appears below it | keep |
| **System health** title | "Your system health" | `BalancedSystemsSummary.tsx:74–76` | — | — | frontend static copy | Title is fine | keep |
| **System health** empty body | "No clearly stable systems are highlighted in this panel — we'll guide you through the key findings below." | `BalancedSystemsSummary.tsx:31` — `EMPTY_STABLE_COPY` constant | `balanced_systems_v1` (null/absent) | `compile_balanced_systems_v1` (not populated) | fallback text | **Critical structural gap.** This is the most important trust-building section in the v6 journey (Section 2, "What's working well"). It is empty. The fallback copy is dismissive and does not reassure the user. Three domain cards show scores of 92, 100, and 94 — this system clearly has stable areas, yet balanced_systems_v1 is not populated for this analysis. | needs new governed asset / rewrite at backend source |
| **Data quality** heading | "Trust strip" | `PipelineStatus` component | — | — | frontend static copy | "Trust strip" is an internal name. Not a consumer heading. | rewrite frontend copy |
| **Data quality** status | "Quality checks passed" | PipelineStatus | `clinician_report_v1.data_quality.data_quality_passed` | clinician report compile | DTO structured field | Acceptable | keep |
| **Data quality** body | "We received 9 of 9 expected markers for this interpretation. Core quality checks passed." | PipelineStatus | `clinician_report_v1.data_quality.panel_completeness_present/expected` | clinician report compile | deterministic backend compiler prose | Acceptable | keep |
| **Body overview** title | "Body overview" | `ResultsBodyOverview.tsx:49` | — | — | frontend static copy | Acceptable heading | keep |
| **Body overview** primary paragraph — opening | "Lead ranked finding Homocysteine Elevation Context (suboptimal) is interpreted alongside the wider structured snapshot of this panel below." | `ResultsBodyOverview.tsx:54` → `narrative_report_v1.body_overview` or `buildBodyOverviewPrimarySentence()` | `narrative_report_v1.body_overview` | `narrative_report_compiler_v1` | deterministic backend compiler prose | **Problem.** "Lead ranked finding" is internal framing. "(suboptimal)" is an internal severity tag. First sentence reads like a report header, not an orienting consumer summary. | rewrite at backend source |
| **Body overview** — alcohol context | "Your questionnaire suggests moderate alcohol intake, which can be relevant when interpreting homocysteine because alcohol intake may increase demand on one-carbon nutrients such as folate and B vitamins. This does not change your biomarker score, but it helps explain why this pathway is worth reviewing." | same | same | same | deterministic backend compiler prose | Content is clinically useful and personalised — good. Language is reasonable. But it is buried inside a paragraph-wall. | keep but reorder/restructure |
| **Body overview** — lifestyle block | "Your lifestyle inputs suggest additional metabolic context on this panel (for example weight, sleep, alcohol, or smoking patterns). This is used only to adjust how systems are weighted in the analytical model — not to alter the lab values on this panel." | same | same | same | deterministic backend compiler prose | "Analytical model" is internal framing. The disclaimer is appropriate but phrased for internal documentation, not users. | rewrite at backend source |
| **Body overview** — system context | "Your main finding sits in a Cardiovascular 4 Biomarkers context" | same | same | same | deterministic backend compiler prose | **"Cardiovascular 4 Biomarkers"** is a raw internal cluster identifier, not a consumer label. | rewrite at backend source |
| **Body overview** — related systems list | "Related systems also noted on this panel: Autonomic, Cardiovascular, Hematological, Hepatic, Hormonal, Immune, Metabolic, Musculoskeletal, plus 3 other related areas." | same | same | same | deterministic backend compiler prose | List dump of internal system names. Adds noise, not orientation. | omit from UX |
| **Body overview** — interpretation themes | "Related interpretation themes on this panel: Functional read — one-carbon pathway and homocysteine patterning; Functional read — lipid transport and residual particle exposure." | same | same | same | deterministic backend compiler prose | "Functional read — one-carbon pathway" is an internal signal thread label. Not consumer copy. | omit from UX or rewrite at backend source |
| **Body overview** — pattern counts | "0 Needs attention / 0 Explore further / 3 Stable / 3 pattern groups in this run." | `ResultsBodyOverview.tsx:57–75` → `summarizeClusterPatternBuckets()` | `clusters[].severity` | Orchestrator cluster severity | frontend-derived text | **Incoherent.** 0 needs attention contradicts the hero showing "Attention" severity. The buckets are derived from cluster severity labels which are clearly not mapping correctly to the IDL-driven primary finding. | rewrite at backend source (severity mapping) |
| **Investigation path** prose | "Primary finding states the headline read for this panel. Next: what looks stable, the lead finding and evidence, why that lead ranked, then Patterns across your body (including Methylation pathway pattern), then deeper evidence—each block adds detail instead of repeating the same headline." | `ResultsInvestigationSpine.tsx:41–54` | `interpretation_display_layer_v1.records[0].retail_display_label` (for cross-body label) | IDL (label only) + frontend static copy | frontend static copy + frontend-derived text | Useful navigation hint, but positioned inside the content area, not before it. Reads as a system note, not a user benefit. | keep but move (to top of disclosure or page intro) |
| **Patterns** heading | "Patterns across your body" | `InterpretationPatternsSection` | — | — | frontend static copy | Acceptable heading | keep |
| **Methylation pattern card** title | "Methylation pathway pattern" | IDL bundle | `interpretation_display_layer_v1.records[0].retail_display_label` | `publish_interpretation_display_layer_v1` ← IDL YAML | governed Knowledge Bus asset | Acceptable — clinically meaningful label | keep |
| **Methylation pattern card** body | "Homocysteine elevation with larger red-cell index suggesting one-carbon / marrow context" | same | `interpretation_display_layer_v1.records[0].subtitle` or equivalent | IDL asset | governed Knowledge Bus asset | Good clinical description | keep |
| **Methylation pattern card** badge | "Watch" | same | IDL severity | IDL asset | governed Knowledge Bus asset | Appropriate | keep |
| **Methylation pattern card** why-it-matters | "This pattern links nutrient–cofactor networks to vascular and blood-cell maturation questions that deserve coherent follow-up, not a single-marker snapshot." | same | IDL asset | IDL asset | governed Knowledge Bus asset | Good — but appears here for third time (also in retail_summary and hero bridge) | combine/deduplicate |
| **Methylation pattern card** markers | "Supporting markers: Homocysteine, Vitamin B12, Folate, Transferrin" | same | IDL asset | IDL asset | governed Knowledge Bus asset | Acceptable | keep |
| **SystemUnderstanding** — grouping block | "We organise markers into body systems so related results read together instead of in isolation. Cardiovascular Health Pattern brings together markers such as Hdl Cholesterol and Ldl Cholesterol, in the same neighbourhood as the headline pattern above." | `SystemUnderstandingSection.tsx:62–63` | `clusters[].name`, `clusters[].biomarkers` | Orchestrator clusters | frontend-derived text | "Hdl Cholesterol" and "Ldl Cholesterol" — title-case from `formatMarkerLabel()` on raw keys. Reasonable, but "Cardiovascular Health Pattern" as a section name appears nowhere else on the page, creating an orphaned reference. | rewrite frontend copy |
| **SystemUnderstanding** — stable/strain block | "Here, stable means a system looks broadly within range for this snapshot. Strain means several markers align in the same direction—often where Cardiovascular Health Pattern leads—and that is where we narrow attention, without implying a diagnosis on its own." | `SystemUnderstandingSection.tsx:101–103` | same | same | frontend-derived text | Educational content but positioned at the wrong point in the journey — should appear earlier as orientation, not after the hypothesis detail | keep but move |
| **SystemUnderstanding** — markers-to-pattern block | "Individual markers are single signals; the useful story is how they combine across systems. Cardiovascular Health Pattern organises markers for comparison, while the cross-body read 'Methylation pathway pattern' summarises how related signals line up across the panel—both are on this page, answering different layers of the same investigation." | `SystemUnderstandingSection.tsx:110` | clusters + IDL label | same | frontend-derived text | Reasonable educational framing | keep but move |
| **Why lead won** title | "Why this lead won · uncertainty" | `WhyThisLeadWonSection.tsx:49` | — | — | frontend static copy | Acceptable heading | keep |
| **Why lead won** desc | "How the headline was chosen, what else was close, and how much room for doubt remains on this panel." | `WhyThisLeadWonSection.tsx:52–54` | — | — | frontend static copy | Acceptable | keep |
| **Why lead won** — runner_up_why | "Homocysteine Elevation Context and Homocysteine High are similarly strong on this panel (0.90 vs 0.90); the headline shows one pattern first so the discussion has a single starting point." | `WhyThisLeadWonSection.tsx:28` → `p1.runner_up_why_not_lead_line` | `clinician_report_v1.sections.page1.runner_up_why_not_lead_line` | clinician report compiler | deterministic backend compiler prose | **Problem.** "(0.90 vs 0.90)" exposes raw internal numerical confidence scores to consumer. | rewrite at backend source |
| **Why lead won** — closest alternative | "Homocysteine High: is outside the optimal range on this panel" | `WhyThisLeadWonSection.tsx:29` → `p1.runner_up_topic_line` | `clinician_report_v1.sections.page1.runner_up_topic_line` | clinician report compiler | deterministic backend compiler prose | Same template pattern as hero title — "[Signal]: is outside the optimal range on this panel". Internal compiler string. | rewrite at backend source |
| **Why lead won** — close call note | "Several findings were similarly important on this panel; we still surface one lead first so the story has a clear starting point." | `WhyThisLeadWonSection.tsx:75–78` | — | — | frontend static copy | Reasonable fallback message | keep |
| **Why lead won** — confidence | "Overall confidence for this lead pattern: 0.90. Some expected confirmatory markers are not on this panel, which limits how specific the story can be." | `buildConfidenceBlocksForSection4()` | `clinician_report_v1.sections.page1.confidence_and_missing_data` | clinician report compiler | deterministic backend compiler prose | **Problem.** "0.90" is a raw internal confidence score. | rewrite at backend source |
| **Why lead won** — panel caveat | "Given available markers, confidence is constrained by missing or partial reference-range context." | same | same | same | deterministic backend compiler prose | Acceptable message but attached to a numeric score that undermines it | keep, rewrite numeric framing |
| **"What this means"** section title (NarrativeLeadAndSupportingSections) | "What this means" | `DeterministicNarrativeSurface.tsx:88` | — | — | frontend static copy | **Title collision** — same title as the parent disclosure accordion. Creates two "What this means" headings on the same page. | rewrite frontend copy |
| **"What this means"** — "Primary focus" label | "Primary focus" | `DeterministicNarrativeSurface.tsx:99` | — | — | frontend static copy | Acceptable sub-label | keep |
| **"What this means"** — lead_narrative body | Full 700+ word block starting "The one-carbon (methyl-group) network supplies methyl units for DNA synthesis..." through all four hypotheses, evidence, confirmatory tests, including "(governed label): moderate_by_default" and "confidence weight 0.60 — structured ranking only" | `DeterministicNarrativeSurface.tsx` → `narrative_report_v1.lead_narrative` | `narrative_report_v1.lead_narrative` | `narrative_report_compiler_v1` | deterministic backend compiler prose | **Most damaging prose block on the page.** Contains: (1) raw internal labels — "(governed label): moderate_by_default"; (2) raw numerical weights — "confidence weight 0.60 — structured ranking only"; (3) verbatim KB mechanism text for the one-carbon pathway (hundreds of words); (4) all four hypotheses listed with their evidence structures; (5) "Clarification paths:" bullet header — internal compiler terminology; (6) duplicate confirmatory test entries. This is not consumer copy. It is compiled KB + hypothesis text rendered raw. | rewrite at backend source — entire `lead_narrative` field needs compiler pass |
| **"What this means"** — "Secondary patterns" label | "Secondary patterns" | `DeterministicNarrativeSurface.tsx:103` | — | — | frontend static copy | Acceptable sub-label | keep |
| **"What this means"** — secondary_narratives body | Full 500+ word block starting "The bloodstream moves lipids as water-insoluble cargo..." then ending with "Other patterns considered on this panel: Homocysteine High (suboptimal) on Homocysteine... Lh High (suboptimal) on Lh... Alp Low (suboptimal) on Alp..." | same → `narrative_report_v1.secondary_narratives` | `narrative_report_v1.secondary_narratives` | `narrative_report_compiler_v1` | deterministic backend compiler prose | **Critical.** (1) Lipid transport mechanism text runs 400+ words — raw KB asset content; (2) "Other patterns considered on this panel:" section lists internal signal IDs: "Lh High (suboptimal) on Lh", "Alp Low (suboptimal) on Alp", "Hypercortisolism (suboptimal) on Cortisol" — these are raw internal signal slugs rendered to consumer; (3) Same template string "is outside the optimal range on this panel" repeated for each | rewrite at backend source — entire `secondary_narratives` field needs compiler pass |
| **Direction and follow-up** title | "Direction and follow-up" | `DeterministicNarrativeSurface.tsx:143` | — | — | frontend static copy | Acceptable heading | keep |
| **Direction and follow-up** — next steps body | "• Discuss these findings with a clinician who knows your history. [+7 more bullets]... Prioritised follow-up (governed assets): Functional read — one-carbon pathway..." | same → `narrative_report_v1.next_steps_narrative` | `narrative_report_v1.next_steps_narrative` | `narrative_report_compiler_v1` | deterministic backend compiler prose | "Prioritised follow-up (governed assets):" is an internal header. "Functional read — one-carbon pathway" is an internal signal thread label. The content is largely useful but peppered with internal labels. | rewrite at backend source |
| **"Clinician-structured 'why' and evidence"** h3 heading | Clinician-structured "why" and evidence | `results/page.tsx:706–708` | — | — | frontend static copy | **Severe.** This is a retail-hostile heading. "Clinician-structured" is internal framing, not consumer language. It names an internal concept in the middle of the retail results page. | rewrite frontend copy |
| **PrimaryFindingAndWhy** title | "Primary finding and why" | `PrimaryFindingAndWhy.tsx:93` | — | — | frontend static copy | Acceptable heading | keep |
| **PrimaryFindingAndWhy** subtitle | "B12-associated pattern" | `PrimaryFindingAndWhy.tsx:96–98` → `hyp0.title` | `clinician_report_v1.sections.root_cause.hypotheses[0].title` | `root_cause_compiler_v1` | deterministic backend compiler prose | Clinically meaningful title. Acceptable. | keep |
| **PrimaryFindingAndWhy** — technical ranking hidden note | "Technical ranking references and evidence-chain wording are hidden by default. Turn on Show technical detail above to review them when you need them." | `PrimaryFindingAndWhy.tsx:147–150` | — | — | frontend static copy | Appropriate gating note | keep |
| **PrimaryFindingAndWhy** — against evidence | "B12 appears clearly within range, which makes a B12-driven pattern less likely on this panel alone. (related markers: Vitamin B12)" | same → `hyp0.evidence_against[0]` | `clinician_report_v1.sections.root_cause.hypotheses[0].evidence_against[]` | `root_cause_compiler_v1` | deterministic backend compiler prose | Clinically useful and honest. Good. | keep |
| **PrimaryFindingAndWhy** — missing data | "Methylmalonic Acid: MMA can help evaluate functional B12 deficiency when homocysteine is elevated." | same → `hyp0.missing_data[]` | same | same | deterministic backend compiler prose | Clinically appropriate | keep |
| **PrimaryFindingAndWhy** — confirmatory | "Methylmalonic acid (MMA): Consider discussing methylmalonic acid (MMA) testing with your clinician to evaluate functional B12 deficiency." | same → `confirmatory_tests[]` | `clinician_report_v1.sections.confirmatory_tests[]` | clinician report compiler | deterministic backend compiler prose | Acceptable. Duplicate of content already in "Direction and follow-up" section. | combine/deduplicate |

---

## 6. Repetition and incoherence findings

| Repeated / incoherent text | Where it appears | Source | Why it is a problem | Recommended fix type |
|---|---|---|---|---|
| "Homocysteine Elevation Context: is outside the optimal range on this panel" | Hero title; retail_summary sentence 3; runner_up_why_not_lead_line preamble | IDL label → clinician compiler templates | Same template string appears ≥3 times on the page in different sections. User reads the identical phrase repeatedly. | rewrite at backend source |
| "A pattern combining inflammation and homocysteine signals associated with vascular risk" | Hero body (appended); Cardiovascular domain card contributor_sentence | `narrative_report_v1.retail_summary` excerpt; `consumer_domain_scores[0].contributor_sentence` | Verbatim in two different sections. | rewrite at backend source |
| "Methylation pathway pattern" description (pattern links nutrient–cofactor networks...) | Summary card body (inside retail_summary); Patterns card (IDL) | `narrative_report_v1.retail_summary`; IDL record | IDL pattern description appears in retail_summary then again as the actual pattern card below | combine/deduplicate |
| "is outside the optimal range on this panel" (as template) | Hero title; runner_up_topic_line; secondary_narratives signal list (×6 signals) | Compiler template across multiple fields | Template string used as substitute for actual prose. Appears 8+ times across the page. | rewrite at backend source |
| MMA / Full blood count confirmatory test references | "What this means" lead_narrative (twice, once per hypothesis); "Direction and follow-up" next_steps; "Primary finding and why" clarify block | Multiple compiled fields pulling from same root_cause data | Same test recommendation appears 3–4 times across the page. | combine/deduplicate |
| "Functional read — one-carbon pathway and homocysteine patterning" (as a label) | Body overview "related themes"; Direction/follow-up "prioritised follow-up"; (secondary_narratives) | `narrative_report_v1.*` compiled fields | Internal signal-thread label surfaced as consumer copy in multiple locations | rewrite at backend source |
| 100/100 "Strong" blood sugar score alongside "Limited confidence" + "still has active signals" headline | Wave1DomainCards blood sugar card | `consumer_domain_scores` | Score, band, confidence and headline all contradict each other. | rewrite at backend source |
| "What this means" as heading | Parent disclosure accordion heading; NarrativeLeadAndSupportingSections heading inside the same accordion | `results/page.tsx` and `DeterministicNarrativeSurface.tsx` | Two identical headings nested on the same page; the inner one is directly under the open outer one | rewrite frontend copy |
| "0 Needs attention" pattern count | Body overview pattern bucket grid | `summarizeClusterPatternBuckets()` from cluster severity | Hero shows severity "Attention" but clusters map to 0 needs-attention; incoherent to user who sees both | rewrite at backend source (severity mapping) |

---

## 7. Fallback and boilerplate findings

| Exact prose | Why fallback triggered | Acceptable? | Disposition |
|---|---|---|---|
| "No clearly stable systems are highlighted in this panel — we'll guide you through the key findings below." | `balanced_systems_v1` is null or has no items for this analysis. `compile_balanced_systems_v1` did not populate the field. | **No.** Three domain cards show high scores (92, 100, 94). The system clearly has stable areas. The fallback masks this. | Replace with needs new governed asset — `balanced_systems_v1` should populate for this analysis |
| "Scored using lab reference range" (×2 in driving signals) | `oneLineMarkerInterpretation()` fallback when `biomarker.interpretation` is empty | No. It is not informative. It describes the method, not the finding. | rewrite at backend source — populate `interpretation` field for driving signal markers |
| "Deeper hypothesis detail is limited on this result — use the clinical interpretation notes and system groups below for the next level of context." | Not triggered for this analysis (root cause is present). Would show when `!hasRootNarrative && !chains.length && !bodyB && page1` | N/A for this panel but acceptable as a fallback if it were triggered | keep |
| "No separate checklist of follow-up lines was packaged with this result." | Would show when `actionCards.length === 0` | Acceptable if truly empty | keep |
| "Alp / 38 U/L / · Critical" | Status "critical" assigned by scoring engine for ALP 38 | **No.** ALP 38 U/L is LOW by most reference ranges, not critical. This appears to be a scoring engine error on this marker. | investigate at backend source — ALP critical classification at 38 U/L |

---

## 8. Governed asset surfacing findings

| Asset | Present in DTO? | Surfaced to user? | Where / how | Quality assessment |
|---|---|---|---|---|
| `root_cause_v1` / hypotheses | Yes — `clinician_report_v1.sections.root_cause.hypotheses[]` | Partially — `PrimaryFindingAndWhy` surfaces hyp[0] title, evidence_against, missing_data | Inside "Clinician-structured 'why'" subheading, deep in page | Hypothesis text is good; evidence_against is honest; but surfaced under a retail-hostile heading and after 10+ other blocks |
| `top_hypothesis_line` | Likely in `page1` | Not directly surfaced as a standalone field | Merged into `buildSection3LeadStatement()` / body overview | Unclear if field is populated |
| `chains[]` | In `page1.chains` | Hidden behind "Show technical detail" toggle | `PrimaryFindingAndWhy.tsx` — gated behind `showTechnicalDetail` | Most important connective narrative is completely hidden by default |
| `balanced_systems_v1` | Present in DTO type | Empty for this analysis — fallback shown | `BalancedSystemsSummary` — empty state | **Critical gap** — most important trust-building asset is absent from this result |
| `system_capacity_scores` | Present in DTO (LC-S16 confirms not extracted to top-level DTO) | Not surfaced | Not rendered anywhere on page | As per v6 paper, should drive body overview visual |
| `contribution_context` | Per `biomarkers[].contribution_context.factual_statement` | Surfaced in `BiomarkerDials` expansion (Advanced section, collapsed) | Only visible when user opens Advanced accordion and expands a biomarker | Good asset, completely inaccessible behind two collapse layers |
| `biomarker_educational_explainer` | Per `biomarkers[].biomarker_educational_explainer` | Surfaced in `BiomarkerDials` (Advanced section, collapsed) | Same as above | Same — inaccessible |
| `confirmatory_tests[]` | `clinician_report_v1.sections.confirmatory_tests` | Yes — in PrimaryFindingAndWhy + next_steps | Multiple locations | Surfaced but duplicated 3–4 times |
| `runner_up_topic_line` | `clinician_report_v1.sections.page1.runner_up_topic_line` | Yes — in WhyThisLeadWonSection | Surfaced but contains raw template string | Needs compiler fix not FE fix |
| `runner_up_why_not_lead_line` | Same | Yes — runner_up_why_not_lead_line block | Contains raw score "0.90 vs 0.90" | Needs compiler fix |
| `confidence_and_missing_data` | Same | Yes | Contains raw score "0.90" | Needs compiler fix |
| `clinician_report_v1.sections.page1.primary_concern` | Yes | Indirectly — merged into hero derivation via `buildSection3LeadStatement()` | Not surfaced as standalone readable block | Could be surfaced more cleanly |
| `layer_c_features` | In `meta.insight_graph.layer_c_features` | `LayerCInsightSection` — inside "Advanced" collapsed section | Invisible to retail users | Should be evaluated for Section 7 surfacing |
| IDL `interpretation_display_layer_v1.records[]` | Yes | Yes — `InterpretationPatternsSection` | Inside "What this means" disclosure | Good — best asset on the page, but buried in the middle of the accordion |
| `balanced_systems_v1.intro_line`, `items[]`, `context_line` | Absent for this analysis | Not shown | — | Missing from compilation for this result |
| `arbitration_result` | In DTO (confirmed in v6 paper as available) | Not explicitly surfaced | — | Missing — should drive body overview |

---

## 9. Mismatch against v6 journey

| v6 Section | Present / Partial / Missing | Current page equivalent | Quality 1–10 | Main blocker |
|---|---|---|---|---|
| 1. Your body overview | Partial | `ResultsBodyOverview` inside "What this means" disclosure | 3/10 | Not at the top of the page; contains a wall of raw compiler text including internal labels; not the calm orienting summary the v6 spec describes |
| 2. What's working well | Missing | `BalancedSystemsSummary` shows empty fallback | 1/10 | `balanced_systems_v1` not populated for this analysis; appears after hero/summary/driving signals/domain cards — wrong position even if populated |
| 3. Primary finding and why | Partial | `ResultsPrimaryHero` + `PrimaryFindingAndWhy` (inside disclosure) | 4/10 | Hero title is a raw template string; chains[] hidden by default; evidence-for entirely absent from retail view; `PrimaryFindingAndWhy` buried at bottom of long disclosure accordion |
| 4. Why this lead won / uncertainty | Partial | `WhyThisLeadWonSection` inside disclosure | 5/10 | Content is mostly right but contains raw numerical scores (0.90); runner-up topic is another template string; section position within disclosure is correct relative to primary finding block |
| 5. Patterns across your body | Partial (Phase 2) | `InterpretationPatternsSection` — one IDL card (Methylation pattern) | 6/10 | One good IDL card exists; content is repeated in retail_summary above it; "Phase 2" classification means no full patterns layer — as expected |
| 6. Marker-level evidence | Missing from retail flow | `BiomarkerDials` inside "Advanced & clinician report" collapsed accordion | 1/10 | Completely inaccessible to retail users without clicking "Advanced" — contribution context and educational explainers never seen in normal flow |
| 7. Key body-level insights | Missing from retail flow | `LayerCInsightSection` inside "Advanced" section | 0/10 | Not accessible to retail users |
| 8. What to do next | Partial | `NarrativeLongitudinalAndNextSteps` inside disclosure + "Actions" collapsed | 4/10 | Next steps content exists but is buried inside "What this means" disclosure; "Actions" collapsed by default; contains internal labels ("governed assets", "Functional read —") |
| 9. Clinician summary | Present | `ClinicianReportRenderer` inside "Advanced & clinician report" | 5/10 | Exists and is appropriately gated behind collapsed section; reasonable |

---

## 10. Human-facing diagnosis

**Why does the current page feel poor?**

The page delivers its worst moment immediately after the user arrives. The hero title — "Homocysteine Elevation Context: is outside the optimal range on this panel" — is a template string from the compiler. The next thing the user reads is the Summary card, which opens with "The ranked lead pattern is Homocysteine Elevation Context (suboptimal), centred on Homocysteine. This is the priority focus for interpretation on this panel." This is not a summary — it is the compiler annotating its own output.

Then, when the user opens "What this means" (which is the default state), they hit the NarrativeLeadAndSupportingSections "Primary focus" block — 700+ words of raw mechanism text with internal labels, all four hypotheses with numerical confidence weights, and confirmatory tests listed multiple times. This is KB content served raw to a retail user.

**Is the issue mainly bad source prose or bad presentation/order?**

Both — but source prose is the more urgent problem. Reordering sections will not make the hero title usable. Reordering will not remove "(governed label): moderate_by_default" from the visible text. The narrative compiler (`narrative_report_v1`) is generating fields that contain internal metadata. That must be fixed at source before any presentational improvement will be felt.

**The 10 text blocks doing the most damage:**

1. `narrative_report_v1.lead_narrative` — 700+ words of mechanism text + all hypotheses + internal labels + duplicate confirmatory tests. Rendered as "Primary focus" in "What this means".
2. `narrative_report_v1.retail_summary` — opens with compiler self-description; contains meta-commentary copy; duplicates IDL pattern card content.
3. **Hero title** — raw IDL label field used as consumer headline. "is outside the optimal range on this panel" is a template artifact.
4. **Runner-up confidence copy** — "0.90 vs 0.90" and "Overall confidence for this lead pattern: 0.90" expose internal scores.
5. `narrative_report_v1.secondary_narratives` — another wall of mechanism text + list of internal signal IDs ("Lh High (suboptimal) on Lh").
6. **Body overview primary paragraph** — "Lead ranked finding Homocysteine Elevation Context (suboptimal)" + "Cardiovascular 4 Biomarkers context" + related-systems list dump + "Related interpretation themes: Functional read —".
7. **Cardiovascular domain card contributor_sentence** — verbatim repeat of hero body text.
8. **Blood sugar domain card score/headline mismatch** — 100/100 + "still has active signals to address".
9. **Balanced systems empty fallback** — three domain cards show 92–100/100 yet the reassurance section says no stable systems are highlighted.
10. **"Clinician-structured 'why' and evidence"** heading in the middle of the retail page — exposes internal framing language.

**Which existing assets are underused?**

- `chains[]` — most important connective narrative in the entire analysis. Hidden behind "Show technical detail" toggle. Should be visible by default in the primary finding section.
- `contribution_context` — explains why each marker matters in the wider pattern. Buried behind Advanced accordion + biomarker expand. No user will find this.
- `biomarker_educational_explainer` — same as above.
- `system_capacity_scores` — not surfaced anywhere.
- `arbitration_result` — not surfaced anywhere.
- IDL `interpretation_display_layer_v1` — only one pattern card visible and it is buried mid-accordion; its why-it-matters content is repeated in retail_summary above it.
- `PrimaryFindingAndWhy` evidence-for block — `supports` (evidence-for) is empty/not populated for this analysis; only evidence-against is shown. The most important supporting evidence block is absent.

---

## 11. Recommended next sprint

### FE-R1 — Consumer Prose Cleanup and Narrative Safety

Purpose: stop bad prose reaching the user.

Achieves:

removes raw compiler/internal text from retail-facing sections
fixes retail_summary, lead_narrative, secondary_narratives, confidence wording and internal labels
removes phrases like “governed label”, confidence weights, raw signal names and repeated template strings
fixes or suppresses duplicate prose
investigates balanced_systems_v1 absence
investigates ALP 38 U/L being labelled Critical

Why first: the audit says reordering the page will not help if broken prose is still being surfaced.

### FE-R2 — Results Journey Restructure

Purpose: rebuild the page into the v6 guided reasoning journey.

Achieves:

moves the page away from cards/accordion clutter
implements the main journey order:
body overview
what’s working well
primary finding and why
uncertainty
marker evidence
next steps
clinician summary
makes biomarker evidence visible in the retail journey, not buried under Advanced
keeps clinician material separate
removes or demotes sections that do not support the story

Why second: once prose is safe, we can put the right assets in the right order.

### FE-R3 — Evidence Depth and UX Quality Pass

Purpose: make the page feel premium and useful.

Achieves:

improves biomarker expansion depth
surfaces contribution_context
surfaces biomarker_educational_explainer
improves next-step/action ordering
deduplicates repeated evidence
validates the page against the v6 recommendation paper
performs human UAT against the actual rendered page

Why third: this turns the fixed/reordered page into the richer experience described in the v6 paper. The v6 paper specifically says the marker layer should become a second-order “wow” experience, not just a conventional biomarker appendix.

### FE-R4 — Patterns Layer Gate and Implementation Decision

Purpose: decide whether “Patterns across your body” is ready to implement.

Achieves:

checks whether the current system/cluster/phenotype layer is genuinely ready
confirms whether pattern naming fields exist
decides whether Section 5 is a frontend surfacing sprint or a backend/content contract sprint first
prevents us building a fake phenotype/pattern layer before the underlying contract is ready

Why separate: the v6 paper explicitly marks the patterns layer as Phase 2 and says it needs an existence check before implementation.

### Compressed plan summary
FE-R1 — Clean unsafe/incoherent consumer prose
FE-R2 — Restructure page into the guided results journey
FE-R3 — Add evidence depth, biomarker richness and UX quality pass
FE-R4 — Gate/decide the patterns layer

---

## 12. Appendix — raw page transcript

Page order, exact visible text, captured from Playwright accessibility snapshot 2026-05-24:

---

**Page header**
> Your results
> Start with your primary finding, then open deeper sections for patterns, actions, and the full technical report when you need it.
> [Show technical detail] [Export] [Share]
> 77 markers

---

**Alert banner**
> Your report is built from structured clinical rules applied to your lab data. AI-personalised narrative is not active in this view.

---

**PRIMARY FINDING HERO**
> Primary finding
> Homocysteine Elevation Context: is outside the optimal range on this panel
> Main system context: Vascular Inflammation Risk
> [Attention]
> Accumulating vascular-risk signals warrant cardiometabolic review and lifestyle action. A pattern combining inflammation and homocysteine signals associated with vascular risk Homocysteine, Vitamin B12, Folate, Transferrin
> [Download report]

---

**SUMMARY**
> 📖 Summary
> A plain-language summary of the main pattern in your results.
>
> The ranked lead pattern is Homocysteine Elevation Context (suboptimal), centred on Homocysteine. This is the priority focus for interpretation on this panel. Homocysteine Elevation Context is outside the optimal range on this panel. The main lab anchor on this panel for this thread is homocysteine. This wording stays descriptive and does not replace clinician judgement or imply certainty beyond what the markers support. Methylation pathway pattern (pattern to watch): Homocysteine elevation with larger red-cell index suggesting one-carbon / marrow context This pattern links nutrient–cofactor networks to vascular and blood-cell maturation questions that deserve coherent follow-up, not a single-marker snapshot.

---

**WHAT'S DRIVING THIS**
> What's driving this
> Key markers behind the main pattern, using the values returned for this run.
>
> Homocysteine · 16.93 umol/L · Elevated
> Scored using lab reference range
>
> Alp · 38 U/L · Critical
> Scored using lab reference range
>
> See all markers

---

**YOUR HEALTH DOMAINS**
> Your health domains
> High-level scores for three focus areas. Open a card for detail — not a diagnosis.
>
> [Cardiovascular health]
> A pattern combining inflammation and homocysteine signals associated with vascular risk
> Based mainly on: Vascular Inflammation Risk
> 92 / 100 · Strong
> High confidence
> Your cardiovascular read on this panel is not a simple all-clear: the leading pattern here still deserves clinical context alongside your numbers.
> [More detail]
>
> [Blood sugar control]
> HbA1c is within range on this panel. Glucose and insulin were not included, so a fuller glycaemic read would require those markers.
> Based mainly on: your blood sugar and metabolic markers on this panel.
> 100 / 100 · Strong
> Limited confidence
> Your blood sugar and metabolic context still has active signals to address in care planning, even if some results look in range on the surface.
> [More detail]
>
> [Liver health]
> Your liver enzyme markers are within their reference ranges.
> Based mainly on: your liver-related markers on this panel.
> 94 / 100 · Strong
> Limited confidence
> Your liver health looks strong based on your current enzyme markers.
> [More detail]

---

**YOUR SYSTEM HEALTH**
> ✓ Your system health
> No clearly stable systems are highlighted in this panel — we'll guide you through the key findings below.

---

**DATA QUALITY**
> Trust strip
> Quality checks passed
> We received 9 of 9 expected markers for this interpretation. Core quality checks passed.
> [More detail]

---

**WHAT THIS MEANS** (disclosure, open by default)

*Body overview*
> 🔲 Body overview
>
> Lead ranked finding Homocysteine Elevation Context (suboptimal) is interpreted alongside the wider structured snapshot of this panel below. Your questionnaire suggests moderate alcohol intake, which can be relevant when interpreting homocysteine because alcohol intake may increase demand on one-carbon nutrients such as folate and B vitamins. This does not change your biomarker score, but it helps explain why this pathway is worth reviewing. Your lifestyle inputs suggest additional metabolic context on this panel (for example weight, sleep, alcohol, or smoking patterns). This is used only to adjust how systems are weighted in the analytical model — not to alter the lab values on this panel. Your main finding sits in a Cardiovascular 4 Biomarkers context — this is where the panel places most interpretive weight. Related systems also noted on this panel: Autonomic, Cardiovascular, Hematological, Hepatic, Hormonal, Immune, Metabolic, Musculoskeletal, plus 3 other related areas. Most other system groups look broadly stable on this panel compared with the lead focus — that helps place the concern in perspective rather than suggesting the whole panel is off track. Related interpretation themes on this panel: Functional read — one-carbon pathway and homocysteine patterning; Functional read — lipid transport and residual particle exposure.
>
> Pattern groups on this panel:
> Needs attention: 0 | Explore further: 0 | Stable on this panel: 3
> 3 pattern groups in this run.

*Your investigation path*
> 🗺 Your investigation path
>
> Primary finding states the headline read for this panel. Next: what looks stable, the lead finding and evidence, why that lead ranked, then Patterns across your body (including Methylation pathway pattern), then deeper evidence—each block adds detail instead of repeating the same headline.

*Patterns across your body*
> Patterns across your body
>
> Methylation pathway pattern [Watch]
> Homocysteine elevation with larger red-cell index suggesting one-carbon / marrow context
>
> Why this matters: This pattern links nutrient–cofactor networks to vascular and blood-cell maturation questions that deserve coherent follow-up, not a single-marker snapshot.
> Supporting markers: Homocysteine, Vitamin B12, Folate, Transferrin

*How to understand your results*
> How to understand your results
>
> **Why your results are grouped**
> We organise markers into body systems so related results read together instead of in isolation. Cardiovascular Health Pattern brings together markers such as Hdl Cholesterol and Ldl Cholesterol, in the same neighbourhood as the headline pattern above.
>
> **What "stable" and "strain" mean here**
> Here, stable means a system looks broadly within range for this snapshot. Strain means several markers align in the same direction—often where Cardiovascular Health Pattern leads—and that is where we narrow attention, without implying a diagnosis on its own.
>
> **How markers connect to the bigger picture**
> Individual markers are single signals; the useful story is how they combine across systems. Cardiovascular Health Pattern organises markers for comparison, while the cross-body read "Methylation pathway pattern" summarises how related signals line up across the panel—both are on this page, answering different layers of the same investigation.

*Why this lead won · uncertainty*
> Why this lead won · uncertainty
> How the headline was chosen, what else was close, and how much room for doubt remains on this panel.
>
> WHY THIS LEAD WON
> Homocysteine Elevation Context and Homocysteine High are similarly strong on this panel (0.90 vs 0.90); the headline shows one pattern first so the discussion has a single starting point.
>
> CLOSEST ALTERNATIVE
> Homocysteine High: is outside the optimal range on this panel
>
> CLOSE CALL
> Several findings were similarly important on this panel; we still surface one lead first so the story has a clear starting point.
>
> CONFIDENCE AND LIMITS
> Overall confidence for this lead pattern: 0.90. Some expected confirmatory markers are not on this panel, which limits how specific the story can be.
> Given available markers, confidence is constrained by missing or partial reference-range context.

*What this means* [INNER — title collision]
> 🩺 What this means
> How the main pattern fits with the rest of your markers — written in plain language, with appropriate caution.
>
> PRIMARY FOCUS
> The one-carbon (methyl-group) network supplies methyl units for DNA synthesis, neurotransmitter metabolism, phospholipid production, and numerous cellular methylation reactions. [... 700+ words of mechanism text, pathway text, confidence framing blocks, four hypotheses with evidence, confirmatory tests ...]
> ...Confidence framing (governed label): moderate_by_default...
> ...How the lead pattern may be explained (structured interpretation): Hypothesis — B12-associated pattern: Homocysteine is elevated with a pattern that can be consistent with reduced B12-related methylation capacity. (confidence weight 0.60 — structured ranking only)...
>
> SECONDARY PATTERNS
> The bloodstream moves lipids as water-insoluble cargo inside lipoprotein particles. [... 500+ words of lipid transport mechanism text ...]
> ...Other patterns considered on this panel: Homocysteine High (suboptimal) on Homocysteine: Homocysteine High is outside the optimal range on this panel. Lh High (suboptimal) on Lh: Lh High is outside the optimal range on this panel. Alp Low (suboptimal) on Alp: Alp Low is outside the optimal range on this panel. Hypercortisolism (suboptimal) on Cortisol: Hypercortisolism is outside the optimal range on this panel. Cortisol High (suboptimal) on Cortisol: Cortisol High is outside the optimal range on this panel. Creatine Kinase High (suboptimal) on Creatine Kinase: Creatine Kinase High is outside the optimal range on this panel.

*Direction and follow-up*
> 🗺 Direction and follow-up
> How markers moved relative to prior data when available, and suggested next actions.
>
> NEXT STEPS
> • Discuss these findings with a clinician who knows your history.
> • Monitor trends on the cadence your clinician recommends.
> • Repeat priority markers when your clinician advises retesting.
> • Review lifestyle context already captured in your questionnaire — no new behavioural prescriptions are added here.
> • Consider clinician-guided follow-up on Methylmalonic acid (MMA) (Consider discussing methylmalonic acid (MMA) testing with your clinician to evaluate functional B12 deficiency.).
> • Consider clinician-guided follow-up on Full blood count (MCV/haemoglobin/RDW) (Consider including a full blood count with indices (e.g., MCV) to add context for nutritional or marrow patterns.).
> • Consider clinician-guided follow-up on Repeat homocysteine (Consider repeating homocysteine in 8–12 weeks to confirm persistence and track change over time.).
> • Consider clinician-guided follow-up on Repeat CRP (Consider repeating CRP with a consistent method to see if inflammation markers are persistently elevated.).
>
> Prioritised follow-up (governed assets):
> Functional read — one-carbon pathway and homocysteine patterning:
> • Repeat homocysteine and review B12, folate, and full blood count indices on a stable clinical footing.
> • Where discordance persists, consider directed evaluation for malabsorption, drug effects, or specialist review per local practice.
> • Integrate inflammatory markers and lipid context when vascular framing is the primary concern.
>
> Functional read — lipid transport and residual particle exposure:
> • Repeat lipids under consistent conditions; add non-HDL or apoB-related measures when available to quantify particle burden.
> • Review blood pressure, glycaemic markers, and family history to place transport findings in overall risk context.
> • Use clinician-guided risk tools appropriate to jurisdiction rather than inferring treatment solely from one lipid value.

*Clinician-structured "why" and evidence* [h3 heading in retail flow]
> Clinician-structured "why" and evidence
>
> Primary finding and why
> B12-associated pattern
>
> Technical ranking references and evidence-chain wording are hidden by default. Turn on Show technical detail above to review them when you need them.
>
> PULLS AGAINST OR COMPLICATES IT
> • B12 appears clearly within range, which makes a B12-driven pattern less likely on this panel alone. (related markers: Vitamin B12)
>
> WHAT WOULD CLARIFY THE PICTURE
> • Methylmalonic Acid: MMA can help evaluate functional B12 deficiency when homocysteine is elevated.
> • Methylmalonic acid (MMA): Consider discussing methylmalonic acid (MMA) testing with your clinician to evaluate functional B12 deficiency.

---

**ACTIONS** [collapsed]

**ADVANCED & CLINICIAN REPORT** [collapsed]

---

*End of transcript.*
