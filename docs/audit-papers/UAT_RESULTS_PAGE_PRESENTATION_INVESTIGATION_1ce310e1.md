# Human UAT — Full Results Page Presentation Investigation

**Analysis ID:** `1ce310e1-0467-4482-a2f6-56c412329c2e`  
**URL inspected:** `http://localhost:3000/results?analysis_id=1ce310e1-0467-4482-a2f6-56c412329c2e`  
**Inspection date:** 2026-08-05  
**Mode:** Read-only investigation (no code, DB, migration, or result mutation)

---

## Verdict

**`RESULTS_PAGE_REQUIRES_PRODUCT_COPY_DECISION`**

Clinical ranking / concern-set priority is correct for this result. The remaining defect is **consumer presentation**: the page now correctly elevates the hepatic lead, but several retail surfaces render **internal concern-set fields** (snake_case finding `label`, urgency enum) and still interleave **legacy narrative / IDL / cluster** copy that was never designed as the consumer lead story.

A coherent consumer page cannot be finished by inventing finding titles or urgency prose in the frontend. A governed consumer-label (and urgency-display) decision is required for HEP-F1 and peer findings. Separately, several **frontend structure / suppression** fixes can proceed without medical judgement once product copy authority exists (or while suppressing unsafe raw fields).

---

## Branch / HEAD / change confirmation

| Item | Value |
| --- | --- |
| **Branch inspected** | `fix/uat-alt-prioritisation` |
| **HEAD** | `c3f457e146950f6b033d15e16ba50dcfa82e430c` |
| **Why this branch** | Contains the recent presentation-authority fix that users already see (MCV → hepatic lead). Investigation authorised on current runtime; user allowed remaining on `main`, but this branch is the live presentation under audit. |
| **Working tree after investigation** | Clean (no code/config changes). **Only this audit document is added under `docs/audit-papers/`.** |
| **Migrations / DB / result mutation** | None |
| **Commits during this task** | None |

---

## Executive summary

1. **Priority authority works:** `clinical_concern_set` lead is HEP-F1 (`consolidated_hepatocellular_enzyme_elevation`), urgency `within_days`, severity `marked`, tier 1. Mild MCV is nested contextual; CN-F7 is secondary.
2. **Consumer copy authority fails:** Hero, body overview, clinical-priority section, and “Primary focus” all surface a **mechanically title-cased internal `label`**, not a governed consumer display name.
3. **The quoted sentence is frontend-generated** by `buildDiscussFirstSentence` in `clinicalConcernPresentationAuthority.ts` (introduced by the ALT presentation-authority fix). It is **not** persisted on the analysis record.
4. **`(within days)`** is `urgency_time_band` with underscores replaced, injected into that generated sentence and repeated on Clinical Priority rows.
5. **Legacy narrative still leaks** after the lead sentence is replaced: lifestyle / cardiovascular-context / related-systems paragraphs from `narrative_report_v1.body_overview` remain; disclosure “What this means” still carries one-carbon / macrocytosis prose.
6. **IDL is subordinate in labelling** (“Broader pattern context”) but the first retail-safe IDL is **One-carbon pathway pattern** (MCV/homocysteine family), while the hepatic-aligned IDL **Liver Stress Pattern** exists but is `frontend_allowed_term: clinical_only` and therefore hidden from the consumer Patterns section.
7. **Multiple competing narrative sources** remain visible on one page.

---

## 1. Complete rendered page inventory

Observed with technical detail **on** and disclosure sections **expanded** (Additional interpretation context, Clinician summary, Advanced analysis).

### Chrome / page chrome
- Nav: Dashboard, Upload, Actions, Trends, Pricing, Reports, My account, Settings
- Title: **Your results**
- Intro: walks through results in order… clinician summary below
- Controls: Show/Hide technical detail, Export, Share
- Meta (technical on): Completed N/A · 80 uploaded markers · analysis reference UUID
- Disclosure: *Your report is built from structured clinical rules… AI-personalised narrative is not active in this view.*

### Hero (`ResultsPrimaryHero`)
- Eyebrow: **PRIMARY FINDING**
- Title: **Consolidated hepatocellular enzyme elevation**
- Broader line: **Broader pattern context: One-carbon pathway pattern**
- Badge: **marked**
- Summary: **Your results highlight consolidated hepatocellular enzyme elevation as the main pattern to discuss first (within days).**
- CTA: Download report

### Body overview (`ResultsBodyOverview`)
- Heading: Your body overview
- Lead paragraph (assembled):
  - Generated: *Your results highlight consolidated hepatocellular enzyme elevation as the main pattern to discuss first (within days).*
  - Then retained legacy fragments from compiled body overview (MCV lead sentence stripped; rest kept):
    - Lifestyle inputs / metabolic context…
    - *Your main finding sits in a cardiovascular markers on this panel context…*
    - Related systems list: Autonomic, Cardiovascular, Hematological, Hepatic, Hormonal, Immune, Metabolic, Musculoskeletal, plus 3 other related areas…
    - Most other system groups look broadly stable…
- Pattern-groups note: Detailed pattern groups hidden; 3 pattern summaries covered below

### Journey bridge copy (static FE)
- *Sections below build on each other: your main finding and why…*

### Clinical priority (`ClinicalConcernPrioritySection`)
- Mode: *Priority order is supplied by the clinical concern set.*
- **LEAD:** consolidated hepatocellular enzyme elevation  
  - Tier 1 · within days · marked  
  - Constituent signals → **confidence reduced ast absent** (raw caveat)
- **OTHER CONCERNS:** functional b12 concern · Tier 1 · within weeks

### Primary finding and why (`PrimaryFindingAndWhy`)
- Title line: **Consolidated hepatocellular enzyme elevation** (`concernSetLeadTitle`)
- (Intro duplicate omitted — hero already showed lead)

### What’s working well (`BalancedSystemsSummary`)
- Intro from `balanced_systems_v1`
- Hematological / Renal stable items
- Context line still names **Cardiovascular** as headline focus (legacy balanced framing)

### Your health systems (`Wave1DomainCards`)
- Cardiovascular health — 95 / Strong — Based mainly on: Atherogenic lipid pattern
- Blood sugar control — 100 / Strong — Long-term blood sugar
- Liver health — 0 / Needs attention — Based mainly on: **Liver Stress Pattern**

### How confident (`WhyThisLeadWon` + `PipelineStatus`)
- Clinical priority shown in concern set above
- Confidence: panel has enough information… / missing reference-range context
- Data quality: Quality checks passed · 8 of 8 key markers…

### Patterns across your body (`InterpretationPatternsSection`)
- Only retail-safe enabled pattern shown: **One-carbon pathway pattern** (Watch / Health pattern)
- Supporting markers: Mcv, Vitamin B12, Folate, Ggt  
- (Vascular Inflammation Risk and Liver Stress Pattern are enabled but `clinical_only` — not in this consumer section)

### Marker-level evidence
- What’s driving this: Alt 250 U/L Above range; Transferrin 2 g/L Needs review; eGFR 84 Below range
- Full dial grid including MCV 99.5 (80–96), ALT 250 (10–49), etc.
- Uploaded panel fidelity block

### What to do next
- Next steps from `narrative_report_v1.next_steps_narrative` (generic clinician discuss / monitor / retest)
- Confirmatory: Fasting glucose with insulin…
- Actions hub link

### Additional interpretation context (expanded)
- Investigation spine mentioning **One-carbon pathway pattern**
- System understanding: Cardiovascular Health Pattern + HDL/LDL near “headline pattern above” (cluster fallback while primaryDriver nulled)
- **What this means / PRIMARY FOCUS:** generated discuss-first sentence **plus** legacy one-carbon / macrocytosis `lead_narrative`
- Secondary patterns: lipid transport prose…

### Clinician summary (expanded)
- Clinician report renderer; ranking context notes concern set governs priority
- Still contains legacy page1 MCV-centric fields in technical views

### Advanced analysis (expanded)
- Overall score 100
- Additional key findings: **Primary metric: mcv.**
- Clinical concern set governs priority + ranking policy version string
- Layer C insight cards (metabolic age, heart resilience, …)

---

## 2. Payload fields that drive visible presentation

Source: live `GET /api/analysis/result?analysis_id=1ce310e1-…` (200).

### `meta.insight_graph.clinical_concern_set` (ranking authority — correct)

| Field | Value |
| --- | --- |
| `presentation_mode` | `principal` |
| `no_forced_lead` | false |
| `lead_finding_ids` | `hepatic:HEP-F1:ad85c27f42c2e5e1` |
| Lead `label` | `consolidated_hepatocellular_enzyme_elevation` |
| Lead `finding_type` | `HEP-F1` |
| Lead `urgency_time_band` | `within_days` |
| Lead `severity_band` | `marked` |
| Lead `concern_tier` | 1 |
| Lead `nested_constituent_labels` | `alt_abnormal`, `mcv_mild_macrocytosis`, `transferrin_low` |
| Lead caveats | `confidence_reduced_ast_absent` |
| Secondary finding | CN-F7 `functional_b12_concern`, `within_weeks`, tier 1 |

**No consumer display title field exists on findings.** Label is the internal rule identifier string set in `concern_constructor.py`.

### `narrative_report_v1` (persisted legacy consumer narrative — still MCV-led)

| Field | Content character |
| --- | --- |
| `retail_summary` | Centres on **mcv high** |
| `body_overview` | Opens with **mcv high as the main pattern to discuss first**, then lifestyle / **Cardiovascular 4 Biomarkers** / related systems list |
| `lead_narrative` | One-carbon pathway textbook prose + **Macrocytosis morphology anchor** / MCV elevated |
| `next_steps_narrative` | Generic discuss/monitor/retest |

Persisted narrative **conflicts** with concern-set lead. FE now prepends/replaces lead sentences but **retains non-“discuss first” remainder**.

### `clinician_report_v1.sections.page1` (legacy ranking narrative)

- `primary_concern`: Mcv High…
- `primary_concern_mode`: `distinct_lead`
- `key_findings`: MCV-centric
- `top_hypothesis_line`: Macrocytosis morphology anchor (confidence 0.90)

### `interpretation_display_layer_v1`

Notable records:

| retail_display_label | enabled | frontend_allowed_term | severity |
| --- | --- | --- | --- |
| Vascular Inflammation Risk | true | clinical_only | watch |
| Liver Stress Pattern | true | clinical_only | attention |
| One-carbon pathway pattern | true | phenotype_allowed | watch |

Consumer Patterns section only shows **phenotype_allowed** → One-carbon.

### Other
- `primary_driver_system_id`: `cardiovascular_4_biomarkers`
- `balanced_systems_v1`: Hematological, Renal (+ Cardiovascular named in context line)

---

## 3. Surface-to-source map

| Page surface | Exact rendered text (abbrev.) | Frontend component | Helper | DTO/backend field | Authority type | Problem |
| --- | --- | --- | --- | --- | --- | --- |
| Hero title | Consolidated hepatocellular enzyme elevation | `ResultsPrimaryHero` | `resolveClinicalPresentationAuthority` → `humanizeFindingLabel` | `clinical_concern_set.findings[].label` | clinical-priority → **misused as consumer copy** | Internal snake_case label title-cased |
| Hero broader context | Broader pattern context: One-carbon pathway pattern | `ResultsPrimaryHero` | `broaderContextLineFromLegacyLabel` | first retail-safe IDL `retail_display_label` | IDL context | Subordinate label OK; content is MCV-family pattern beside hepatic lead |
| Hero severity badge | marked | `ResultsPrimaryHero` | `severityFromFinding` | `severity_band` | technical metadata | Raw severity enum word |
| Hero summary | Your results highlight … discuss first (within days). | `ResultsPrimaryHero` | `resolveAuthoritativeHeroSummary` ← `buildDiscussFirstSentence` | label + `urgency_time_band` | frontend-generated bridge copy | Mechanical template; urgency enum in narrative |
| Body overview opener | Same discuss-first sentence | `ResultsBodyOverview` | `resolveAuthoritativeBodyOverview` | same generated sentence | frontend-generated | Duplicate of hero; urgency in body prose |
| Body overview remainder | lifestyle… cardiovascular markers… related systems list… | `ResultsBodyOverview` | strip only CONFLICT_LEAD_RE sentences | `narrative_report_v1.body_overview` | legacy fallback / consumer narrative | Still frames “main finding” in cardiovascular context |
| Clinical priority lead | consolidated hepatocellular enzyme elevation | `ClinicalConcernPrioritySection` | `formatLabel` | finding `label` | clinical-priority raw | Same internal label (lowercase) |
| Clinical priority meta | Tier 1 · within days · marked | `FindingRow` | `urgencyLabel` | tier / urgency / severity | technical metadata | Enums exposed on retail journey |
| Constituent signals | confidence reduced ast absent | `FindingRow` details | underscore replace | `caveats[]` | technical metadata | Raw caveat codes |
| Other concerns | functional b12 concern | `ClinicalConcernPrioritySection` | `formatLabel` | CN-F7 `label` | clinical-priority raw | Internal label |
| Primary finding title | Consolidated hepatocellular enzyme elevation | `PrimaryFindingAndWhy` | `concernSetLeadTitle` | same humanized label | clinical-priority → consumer misuse | Third repeat of same title |
| Balanced systems | Hematological / Renal stable; Cardiovascular in context | `BalancedSystemsSummary` | backend copy | `balanced_systems_v1` | consumer narrative (engine) | Context still says headline is Cardiovascular |
| Wave1 Liver card | Liver Stress Pattern / Needs attention | `Wave1DomainCards` | domain DTO | `consumer_domain_scores` | consumer narrative | Good hepatic signal — disconnected from hero wording |
| Patterns section | One-carbon pathway pattern… Mcv… | `InterpretationPatternsSection` | `selectSafeIdlPatternRecords` | IDL records | IDL context | Hepatic IDL hidden (`clinical_only`) |
| Driving markers | Alt 250… | `ResultsDrivingSignals` | layout helpers | biomarker results | consumer / biomarker | Appropriate; ALT first is good |
| Next steps | Discuss with clinician… | `NarrativeLongitudinalAndNextSteps` | — | `narrative_report_v1.next_steps_narrative` | consumer narrative | Generic; OK |
| Investigation spine | …including One-carbon pathway pattern… | `ResultsInvestigationSpine` | — | first retail IDL label | frontend-generated + IDL | Reinforces wrong system family |
| System understanding | Cardiovascular Health Pattern… headline pattern | `SystemUnderstandingSection` | `groupingCopy` | clusters[0] fallback (primaryDriver nulled) | frontend-generated bridge | Contradicts hepatic lead |
| What this means PRIMARY FOCUS | discuss-first + one-carbon/macrocytosis prose | `NarrativeLeadAndSupportingSections` | `resolveAuthoritativeLeadNarrative` | generated + `lead_narrative` | mixed | Conflicting biomedical MCV story kept as “secondary” after opener |
| Advanced / clinician | Primary metric: mcv.; ranking policy string | `ClinicianReportRenderer` / advanced | — | `clinician_report_v1` | legacy / technical | MCV still visible in advanced |

---

## 4. Backend text leakage traces

### 4.1 Finding title — `Consolidated hepatocellular enzyme elevation`

**Origin**
1. Backend constructs finding with  
   `label = "consolidated_hepatocellular_enzyme_elevation"`  
   in `backend/core/analytics/concern_constructor.py` (HEP-F1 paths).
2. Persisted on analysis under `meta.insight_graph.clinical_concern_set.findings[].label`.
3. Frontend `humanizeFindingLabel` / `formatLabel`: replace `_` with spaces, capitalise first character only (hero/primary) or leave lower (priority section).

**Classification:** **Internal compiled-rule / finding key label**, not a governed consumer display label.  
There is **no** `consumer_display_label` / retail title on `ClinicalFindingV1`.  
Contrast: IDL has real `retail_display_label` values (e.g. “Liver Stress Pattern”) but those are not wired as the concern-set lead title.

**Surfaces displaying this title (or underscore variant)**
- Hero primary finding title
- Hero / body-overview / disclosure discuss-first sentence (lowercased mid-sentence)
- Clinical Priority lead row
- Primary finding and why header

### 4.2 Urgency phrase — `within days` / `(within days)`

**Source:** `findings[].urgency_time_band = "within_days"`.  
**Transform:** `formatUrgencyPhrase` / `urgencyLabel` → replace `_` with space.  
**Not** from stored narrative text.

**Surfaces**
- Hero summary / body overview / PRIMARY FOCUS: `(within days)` via `buildDiscussFirstSentence`
- Clinical Priority row: `Tier 1 · within days · marked`
- (Severity badge separately shows `marked` from `severity_band`)

**Authority note:** Urgency belongs in clinical-priority metadata / clinician handoff. **Body-overview and hero prose were not previously authorised to dump the enum into a consumer sentence**; this injection was introduced by the presentation-authority helper.

### 4.3 Quoted body-overview sentence

> Your results highlight consolidated hepatocellular enzyme elevation as the main pattern to discuss first (within days)

| Question | Answer |
| --- | --- |
| Function | `buildDiscussFirstSentence` in `frontend/app/lib/clinicalConcernPresentationAuthority.ts` |
| Inputs | humanized `label`; `urgency_time_band`; presentation mode |
| Persisted? | **No** — generated at render time |
| Introduced by ALT presentation fix? | **Yes** (same helper powers hero summary, body overview opener, lead narrative opener) |
| Shared by other modes? | Yes — co-lead / no-forced-lead / no_concern have alternate templates in the same function; changing the principal template affects all principal-lead renders using this helper |
| Risk if changed carelessly | Co-lead / co-equal / no-forced-lead strings also live here — any edit must preserve those structural modes without inventing clinical ranking |

Wire path for body overview:

`page.tsx` → `resolveAuthoritativeBodyOverview(authority, narrative_report_v1.body_overview, legacyPrimary)` → prefers `authority.discussFirstSentence`, then appends non-conflicting remainder of compiled overview.

---

## 5. Narrative-coherence audit

### Defects
- **Lead repeated ≥4 times** with same technical title (hero, body overview, clinical priority, primary finding).
- **Discuss first** language repeated across hero, body overview, and disclosure PRIMARY FOCUS.
- **Abrupt IDL jump:** hepatic lead → “Broader pattern context: One-carbon pathway pattern”.
- **Legacy body overview** still says main finding sits in **cardiovascular** context.
- **System understanding** ties Cardiovascular Health Pattern to “headline pattern above”.
- **What this means** keeps macrocytosis / MCV explanatory prose immediately under hepatic discuss-first opener.
- **Raw terms:** severity `marked`, urgency `within days`, caveats `confidence reduced ast absent`, labels `functional b12 concern`, domain-ish architecture phrasing (“clinical concern set”, ranking policy version in advanced).
- **Related systems laundry list** in body overview (architecture inventory, not health meaning).
- **Wave1 Liver “Needs attention”** is clinically consistent with ALT but uses different consumer wording than the hero — user sees two hepatic stories with different names.

### Sections that work well (preserve)
- Concern-set **ordering** (hepatic lead, CN-F7 other, MCV nested not lead)
- Marker evidence with ALT 250 prominent in “What’s driving this”
- Wave1 Liver card signalling needs attention (as a domain card — not as fake lead authority)
- Generic next-steps discuss-with-clinician framing
- Mock-mode honesty disclosure
- Demotion of IDL from *primary finding* label (broader-context prefix is the right *structure*, wrong *content choice*)

---

## 6. Authority-boundary review

### Correct use of structured authority
- Which finding is first (`lead_finding_ids`)
- Presentation mode `principal`
- Secondary / other concerns listing
- Suppressing legacy top-finding / retail MCV as hero title
- Not recomputing confidence-based ranking in FE

### Incorrect direct presentation of structured data
- Raw finding `label` as consumer headline
- Urgency enum inside narrative sentences
- Severity enum as retail badge word without governed copy
- Caveat codes in Constituent signals
- Role/architecture sentences (“Priority order is supplied by the clinical concern set”) on the main journey
- Generating “discuss first” consumer prose from structured fields when no approved retail sentence exists

**This is a presentation / copy-boundary defect, not a ranking defect.**

---

## 7. Legacy and fallback path behaviour

| Scenario | Current helper behaviour |
| --- | --- |
| Concern set absent | `source: 'legacy'` — hero/body use narrative/IDL/clinician paths (pre-fix behaviour) |
| Single principal lead (this case) | Generates discuss-first from label + urgency; humanizes label |
| Co-leads | Joins humanized labels; “More than one finding shares lead priority…” |
| Same-day co-equal | ClinicalConcernPrioritySection “Same-day co-equal group”; helper noForcedLead/co_lead templates |
| No-forced-lead | Explicit no-single-lead template including raw titles list |
| Narrative conflicts with concern set | Lead “main pattern/discuss first” sentences stripped; **other legacy paragraphs retained** |
| No approved consumer label | **No stop/gate** — falls through to underscore humanize (current defect) |

**Conclusion:** Helper creates **mechanical consumer copy for all modes**, not only ALT. It does **not** require an approved retail label before rendering. That violates the earlier stop-and-report-copy-gap intent when approved wording is unavailable.

---

## 8. Minimum safe correction boundary (do not implement)

| # | Correction | Classification |
| --- | --- | --- |
| 1 | Stop rendering raw `label` / urgency / severity enums as consumer prose until a governed retail map exists; show structured priority in a clearly clinical/metadata block only | presentation structure + product-copy decision |
| 2 | Add governed **consumer display title** (and optional short discuss sentence) per finding_type/label — or explicitly reuse an approved IDL retail title when mapped | governed consumer-label requirement |
| 3 | Remove urgency parenthetical from body-overview / hero narrative templates; keep urgency on Clinical Priority metadata only (or product-approved urgency copy) | frontend copy mapping / narrative-source suppression |
| 4 | When concern set present: **do not append** legacy `body_overview` / `lead_narrative` fragments that still describe a different lead system; suppress or relocate to advanced | narrative-source suppression |
| 5 | Deduplicate: one consumer lead statement (hero); body overview becomes true overview, not second discuss-first | duplication removal / component ordering |
| 6 | Broader IDL context: prefer hepatic-aligned retail pattern if allowed, or omit IDL line when first retail-safe IDL conflicts with concern lead domain | presentation structure / IDL subordination |
| 7 | System understanding / balanced context: do not name cluster driver as “headline” when concern set owns lead | frontend-generated bridge copy fix |
| 8 | If DTO lacks consumer title fields → **backend DTO gap** to carry optional `consumer_display_label` without changing ranking | backend DTO gap |
| 9 | Product must approve urgency retail phrasing (if any) and HEP-F1 / CN-F7 retail titles | product-copy decision required |

**Preserve:** concern construction, prioritisation, urgency/severity assignment values, signal activation, IDL as subordinate context, legacy fallback when concern set absent, scenario behaviour.

---

## 9. Explicit answers

1. **Is `Consolidated hepatocellular enzyme elevation` an approved consumer label?**  
   **No.** It is the internal finding `label` from concern construction, mechanically humanized.

2. **Why is `within days` in the body overview?**  
   Because `buildDiscussFirstSentence` appends ` (${formatUrgencyPhrase(urgency_time_band)})` and `resolveAuthoritativeBodyOverview` uses that sentence as the opener.

3. **Which component created the quoted body-overview sentence?**  
   Not a React component per se — **`buildDiscussFirstSentence`** in `clinicalConcernPresentationAuthority.ts`, rendered via `ResultsBodyOverview` after `page.tsx` resolves `authoritativeBodyOverview`.

4. **How many separate lead-authority or narrative sources are visible?**  
   At least **six**: (1) concern-set structured lead, (2) FE-generated discuss-first template, (3) legacy `narrative_report_v1`, (4) IDL retail patterns, (5) cluster/primary-driver/system-understanding copy, (6) clinician_report_v1 / advanced MCV fields. Wave1 domain cards add a seventh parallel hepatic wording (“Liver Stress Pattern”).

5. **Which source should control each surface?**  
   - **Ranking / what is first:** clinical_concern_set only  
   - **Consumer headline & body story:** governed consumer narrative / labels (missing)  
   - **IDL:** subordinate pattern context only, domain-aligned when shown  
   - **Clinician/advanced:** may show technical enums and legacy ranking with clear demotion  
   - **Legacy narrative:** suppress when it conflicts or describes a different lead

6. **Is IDL still too prominent?**  
   **Partially.** Labelling is subordinate, but One-carbon appears in hero broader context, Patterns section, and investigation spine — competing for attention with the hepatic lead. Hepatic IDL retail title is hidden from consumers.

7. **Are legacy narrative fragments still displayed after concern-set authority?**  
   **Yes** — body-overview remainder; lead_narrative macrocytosis/one-carbon under PRIMARY FOCUS; clinician/advanced MCV primary metric.

8. **Does the page repeat the lead finding unnecessarily?**  
   **Yes** — hero, body overview, clinical priority, primary finding, plus disclosure PRIMARY FOCUS.

9. **Other raw backend terms leaking?**  
   `marked`; `within days` / `within weeks`; `Tier 1`; `confidence reduced ast absent`; `functional b12 concern`; `consolidated hepatocellular enzyme elevation`; ranking policy version; “clinical concern set” architecture phrasing; sanitized but still awkward “cardiovascular markers on this panel”.

10. **Can the problem be fixed entirely in the frontend?**  
    **Structure/suppression/dedup: mostly yes. Full coherent consumer wording: no** — needs governed labels (or an approved mapping to existing IDL retail titles) without inventing clinical language.

11. **Is a governed consumer-copy map required?**  
    **Yes** (finding titles at minimum; urgency retail phrasing if urgency remains on narrative surfaces).

12. **Would any proposed fix require clinical, product or regulatory decision?**  
    **Yes** for consumer finding titles and any urgency-in-prose wording. **No** for: removing urgency from body overview, suppressing conflicting legacy narrative, deduplicating discuss-first, stopping underscore-humanize as a retail headline, demoting conflicting IDL in hero context.

---

## 10. Items fixable without medical judgement vs needing product authority

### Fixable without medical judgement (FE presentation)
- Remove `(within days)` from narrative templates; keep on metadata row only
- Stop using humanized snake_case as hero title when no consumer label (show safe placeholder / clinical-priority section only)
- Suppress conflicting legacy body_overview / lead_narrative when concern set present
- Deduplicate discuss-first across hero vs body overview
- Avoid cluster “headline” framing in system understanding when concern authority is on
- Hide or relocate architecture sentences from default retail journey

### Requires product-copy (and possibly clinical) authority
- Approved retail title for HEP-F1 (and CN-F7)
- Whether to reuse IDL “Liver Stress Pattern” as the consumer lead title
- Any replacement discuss-first / body-overview sentence
- Whether urgency appears in consumer prose at all, and with what wording
- Whether Clinical Priority block stays on the default retail journey or moves under clinician/advanced

---

## 11. Recommended next implementation task

**Name (suggested):** `FE-RESULTS-CONSUMER-COPY-BOUNDARY-1` — Concern-set ranking stays; retail surfaces stop rendering raw finding labels/urgency enums; suppress conflicting legacy narrative; introduce governed consumer label map (or DTO field) for HEP-F1 before re-enabling a single consumer lead sentence.

**Entry criteria:** Product decision on HEP-F1 (and CN-F7) retail titles; confirm urgency remains metadata-only on retail.

**Out of scope:** concern_constructor, prioritisation rules, thresholds, regen, KB, FIB-4.

---

## 12. Competing / overlapping narrative sources (list)

1. `clinical_concern_set` structured fields (correct ranking; unsafe as raw retail copy)
2. FE `clinicalConcernPresentationAuthority` generated discuss-first templates
3. `narrative_report_v1` (MCV-led retail/body/lead)
4. IDL `retail_display_label` (One-carbon shown; Liver Stress / Vascular clinical_only)
5. Cluster / primary driver / system-understanding governed templates
6. `clinician_report_v1` page1 + advanced (MCV primary metric)
7. `balanced_systems_v1` + Wave1 domain cards (parallel hepatic “Liver Stress Pattern” wording)

---

## Confirmation checklist

- [x] Live page inspected end-to-end (including expanded disclosures / technical detail)
- [x] Live API payload inspected for presentation fields
- [x] Surface-to-source map produced
- [x] Title / urgency / quoted sentence origins traced
- [x] No frontend/backend/DTO/DB/result changes
- [x] No branch created; no commit; no merge
- [x] Credentials not written into this audit

**Verdict: `RESULTS_PAGE_REQUIRES_PRODUCT_COPY_DECISION`**
