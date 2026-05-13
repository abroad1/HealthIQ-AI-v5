# LC-S7 preflight triage — post-LC-S6 UAT (read-only investigation)

**Date:** 2026-05-12  
**Scope:** Investigation only — no code changes, no branch, no Automation Bus.  
**Basis:** Repo trace of frontend + narrative compiler paths; post-LC-S6 browser strings treated as observed evidence.

---

## Overall launch-readiness verdict

**Not safe for controlled external testing** until consumer surfaces stop concatenating **registry / compiler diagnostics** with **retail sanitizer** (notably statin appendix + `Layer B` replacement), and until **ranking policy / hypothesis / effect-type** strings are gated or rewritten. Much of this can be **LC-S7 frontend + narrative contract** work; **one band** (intervention appendix and body-overview assembly) is **cleaner if fixed upstream** in the narrative compiler.

---

## 1. Consumer / technical boundary — string → source → view → fix

| Visible text (evidence) | Rendered from | Backend / contract field | Default consumer vs technical toggle | Recommended fix |
|-------------------------|---------------|----------------------------|----------------------------------------|-----------------|
| **“supporting clinical context intervention annotation”** | **Concatenation artefact**: backend emits `Layer B intervention annotation — …` (`intervention_annotation_formatter_v1.py`); frontend `scrubConsumerRetailNarrative` replaces only `Layer B` → `supporting clinical context` (`retailNarrativeSanitize.ts`). | `InterventionAnnotationsV1` → `format_intervention_annotation_narrative_appendix_v1`; appended to `narrative_report_v1.body_overview` in `narrative_report_compiler_v1.py` (`body_overview_with_ia`). | **Default consumer** — `ResultsBodyOverview` always uses `narrativeReport.body_overview` inside “What this means” (`results/page.tsx` + `ResultsBodyOverview.tsx`). | **Upstream (preferred)**: do not append raw appendix to consumer `body_overview`; use short consumer suffix (`format_intervention_annotation_consumer_cv_suffix_v1`) for retail. **Alternatively**: extend sanitizer to replace the full statin appendix line with plain language. |
| **`expected_biomarker_effect`**, **`direction=lower`**, monitoring fragments | Literal effect line built in formatter. | `InterventionAnnotationResolvedV1.effects[].effect_type`, `expected_direction`, `biomarker_ids`, `monitoring_relevance`. | Same as above — **body_overview** (and anywhere else that appendix is concatenated). | **Upstream**: human sentence for consumer; keep machine line in clinician-only or JSON-only. |
| **“Benchmark interpretation themes (governed functional titles): …”** | `_build_body_overview` in `narrative_report_compiler_v1.py` (fixed prose + benchmark titles). | `interpretation_entities` / functional domain `display_title` via `_benchmark_domain_display_titles`. | **Default consumer** — first paragraph of `body_overview`. | **Upstream rewrite** of template sentence **or** FE scrub entry for that phrase **or** split consumer vs technical body overview (see §2). |
| **“Confidence framing (governed label): …”** | `_functional_section` in `narrative_report_compiler_v1.py` wraps `confidence_grade_label`. | `functional_interpretation_v1` domain YAML → `confidence_grade_label`. | Fed into **`narrative_report_v1.clinician_synthesis`** (`_build_clinician_synthesis`); UI: **Advanced** passes `deterministicClinicianSynthesis` into `ClinicianReportRenderer` (`results/page.tsx`). | **Rewrite upstream** to patient language **or** show only under **Show technical detail** / clinician-only panel **or** scrub in advanced renderer. |
| **“supporting clinical context order, deterministic”** (or close) | `_secondary_ranked` in `narrative_compiler_lc_s3_assembly_v1.py`: header **“Secondary ranked patterns (Layer B order, deterministic):”**; FE replaces `Layer B` → `supporting clinical context`. | `NarrativePayloadV1.top_findings[1:]`. | **Default consumer** — `secondary_narratives` in `NarrativeLeadAndSupportingSections` (`DeterministicNarrativeSurface.tsx`) with scrub. | **Upstream**: replace header with plain English **or** FE add scrub rule for whole header **or** move secondary ranked block behind disclosure labelled technical. |
| **`signal_homocysteine_elevation_context`** | Multiple: (a) `_clinician_header` in LC-S3 uses backticks around `lead.signal_id` (`narrative_compiler_lc_s3_assembly_v1.py`); (b) `page1.primary_concern` / key findings as prose; (c) `formatSignalIdForDisplay` only for **co-ranked** lists in `ClinicianReportRenderer.tsx`. | `clinician_report_v1.sections.page1`, payload top findings. | **clinician_synthesis** = advanced path; **primary concern** text can appear in hero shaping / body fallbacks. | **Never show raw `signal_*` in retail** — map to display label everywhere; keep raw id in technical JSON or sr-only audit line. |
| **`PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_V1+…`** | `ClinicianReportRenderer.tsx` `Page1RankingContext`: **visible** `<p className="text-xs">Ranking policy reference: {policyVersion}</p>`. | `clinician_report_v1.sections.page1.ranking_policy_version`. | **Default consumer** whenever that section is on screen (not gated by `showDetails`). | **Move behind technical detail** or **sr-only** + “Ordering policy” tooltip **or** strip version string to human “Policy-guided ranking”. |
| **`chain_001`** (and similar) | `page1.chains[]` strings from report compiler; `PrimaryFindingAndWhy` renders after `scrubConsumerRetailNarrative` (`PrimaryFindingAndWhy.tsx`). | `clinician_report_v1.sections.page1.chains`. | Inside **`<details>`** “Technical ranking and evidence chains” — **still user-accessible without** global technical toggle. | **Rewrite upstream** to “Evidence chain 1: …” without ids **or** gate entire `<details>` behind **Show technical detail**. |
| **`hcy_b12_pattern_v1`** | Typically embedded in **`hyp0.ranking_rationale`** or clinician synthesis / root-cause DTO text from core compiler (not a dedicated React field). | `root_cause.hypotheses[].hypothesis_id`, ranking rationale strings. | Often in **“How this ranks on this panel”** (`hypRanking` in `PrimaryFindingAndWhy.tsx`). | **Upstream**: never emit raw hypothesis_id in user prose; FE: strip `` `...` `` tokens in scrub if they remain. |
| **Suppressed confirmatory test IDs** | `PipelineStatus.tsx`: lists `confirmatoryTests.slice(0, 8)`; shows **`display_name`** + **`rationale`**; `test_id` is React **key** only. | `clinician_report_v1.sections.confirmatory_tests` (+ hypothesis confirmatory). | **Trust strip** — extra detail behind **“More detail”** (`revealed`). | If UAT still sees **IDs**, likely **`display_name` empty** in DTO — **fix data population** (backend) or FE fallback “Test ref {n}” without raw id in visible text. |

---

## 2. Body overview — why technical / statin text is still there

**Cause (data path)**

1. `narrative_report_compiler_v1._build_body_overview` builds **structural** sentences: primary driver, arbitration phrasing, capacity scores, **“Benchmark interpretation themes (governed functional titles)”** (`narrative_report_compiler_v1.py` ~160–204).
2. **Statin / intervention appendix** is appended: `body_overview_with_ia = _join_blocks([body_overview_struct, ia_appendix])` with `ia_appendix` from `format_intervention_annotation_narrative_appendix_v1` (`intervention_annotation_formatter_v1.py`).
3. LC-S3 path may **prepend** payload lead sentence (`_body_overview_payload_sentence` in `narrative_compiler_lc_s3_assembly_v1.py` ~158–165).
4. Frontend **`ResultsBodyOverview`** uses that string after **`scrubConsumerRetailNarrative`** only (`ResultsBodyOverview.tsx` ~31–38) — it does **not** remove the appendix, and **Layer B** replacement **creates** the “supporting clinical context intervention annotation” glitch.

**Recommendation (pick one primary strategy)**

- **Best:** **Upstream narrative assembly** — emit **two fields** (e.g. consumer `body_overview_retail` vs technical `body_overview_technical`) *or* stop appending **machine appendix** to the same string used for retail.
- **Acceptable LC-S7:** **Split UI** — consumer paragraph from scrubbed structural sentence only; statin / effect-type lines only when **Show technical detail** or inside Advanced.
- **Insufficient alone:** **More `retailNarrativeSanitize` rules** without removing appendix from the pipeline — you will keep fighting order-of-replacement bugs.

---

## 3. Actions duplication — “Safe next-step framing” / duplicate follow-up cards

**Sources**

- **Intro line** is **hard-coded** in backend: `_next_steps_from_payload` starts with **`"Safe next-step framing (Layer C, bounded):\n"`** (`narrative_compiler_lc_s3_assembly_v1.py` ~168–197).
- **Same narrative** is shown in full in **`NarrativeLongitudinalAndNextSteps`** (`DeterministicNarrativeSurface.tsx` ~156–162).
- **Action cards** on results: `buildActionCardModels` (`resultsPageLayout.ts` ~447–515) fills from **`clusters[].recommendations`**, then **`analysis.recommendations`**, then insights; **only if still empty** it parses **`narrative_report_v1.next_steps_narrative`** via `parseNarrativeNextStepParagraphs`.
- **Duplicate “same message”** perception usually comes from: **(A)** full next-steps block **plus** cluster/panel rec lines that **repeat** the same clinician-framing bullets, or **(B)** when narrative fallback runs, **each newline chunk** becomes a card whose **`firstSentence`** is similar (less likely for the intro line if bullets are long).

**Component responsibility**

- **Backend:** `_next_steps_from_payload` + `_collect_next_steps` (“Prioritised follow-up (governed assets): …”) concatenation in `narrative_report_compiler_v1.py` / LC-S3 assembly.
- **Frontend:** `buildActionCardModels` + `ResultsActionCardsBlock` (`ResultsHeroBlocks.tsx` ~183–211) + duplicate **surface** `NarrativeLongitudinalAndNextSteps`.

**Classification**

- **Mostly product/design issue** (same payload, two surfaces) with possible **data overlap** (cluster recs echo narrative). Not necessarily a React key bug.

**Minimal fix (conceptual)**

- **Single owner of “next steps”** on results: either **cards only** (short) **or** full narrative block, not both above the fold **or** strip the fixed preamble from cards when narrative is already rendered. Optionally **dedupe** by normalised text hash in `buildActionCardModels` (FE-only, deterministic).

---

## 4. Biomarker display QA — pipeline and likely defect class

| Issue | API / JSON source | Frontend transform | Likely defect locus | Risk |
|-------|-------------------|--------------------|---------------------|------|
| **Haemoglobin 144 g/dL vs range 130–175 g/L** | `BiomarkerResult`: `value`, `unit`, `reference_range.{min,max,unit}` (`analysis.ts` ~81–93). | `results/page.tsx` maps `reference_range` into `BiomarkerDialEntry` (~495–507). `BiomarkerDials.tsx` prints **value** and **range** as given (~331–336); dial uses `calculateDialValue` (~136–152) **without unit coherence check**. | **Source data / scoring** mismatch (g vs g/L) or missing normalisation in **engine**; UI is **pass-through**. | **HIGH** (misread risk). |
| **Haematocrit 0.4 % vs 0.35–0.48 L/L** | Same fields. | Same — displays numbers literally. | **Unit / scale** on API (fraction vs % vs L/L). | **HIGH**. |
| **HbA1c % vs incompatible range** | Same. | Range row only if **both** min and max are numbers (`BiomarkerDials.tsx` ~332–334). | **Source data** (mmol/mol vs %) or engine not converting. | **HIGH** if both shown. |
| **Testosterone “Not scored - no reference range”** (if in `interpretation`) | `BiomarkerResult.interpretation` from API. | Rendered as `d.interpretation` line (~339–341); no local “Not scored” string in FE — **comes from backend text**. | **Scoring / range attachment** on API vs FE gate. | **MEDIUM–HIGH**. |
| **Ratio labels `tc hdl ratio`** | `biomarker_name` key. | `BIOMARKER_NAMES` map or `replace(/_/g, ' ')` (`BiomarkerDials.tsx` ~206, ~310). | **Label registry** gap (`tc_hdl_ratio` etc.). | **MEDIUM** (cosmetic / trust). |
| **`active b12`, `albumin`, `apoa1`** (driving signals) | `biomarker_name` on panel. | `formatBiomarkerDisplayName` in `resultsPageLayout.ts` (~92–108) title-cases tokens; keys not in `BiomarkerDials` `BIOMARKER_NAMES` still become “Apoa1” not “ApoA1”. | **Label registry** + naming convention. | **MEDIUM** (retail polish). |

**Note:** `BiomarkerDials` card shows **`value.toFixed(1)`** without appending **unit next to the value** in that row (~331); unit appears on a **separate line** under the title (~323–324) — worth a **UX review** in LC-S7 (not necessarily the unit-mismatch root cause).

---

## 5. LC-S7 preflight output (structured)

### Blockers

- Consumer **`body_overview`** carrying **intervention annotation appendix** + **sanitizer creating nonsense phrases**.
- **Raw ranking policy version** and **raw signal / hypothesis / effect-type** vocabulary in **default** scroll paths.
- Any **value/range unit incoherence** left as-is on biomarker cards (trust).

### HIGH

- Split or rewrite **secondary ranked** header (LC-S3) after Layer sanitization.
- **Deduping / ownership** of next-steps content between **Direction and follow-up** and **Actions** cards.
- **Label registry** for common ratios and UK spellings (`haemoglobin` vs `hemoglobin` key).
- **Clinician_synthesis** phrasing (“Confidence framing (governed label)”) for any surface that is not strictly advanced.

### MEDIUM

- `PipelineStatus` confirmatory list truncation (8 + message) — confirm **no empty `display_name`** leaks `test_id`.
- `parseNarrativeNextStepParagraphs` behaviour when preamble is its own paragraph (card headings).

### Recommended LC-S7 implementation scope (minimum)

1. **Narrative contract:** consumer `body_overview` **without** machine statin appendix; optional `body_overview_technical` or append only under technical flag (**backend** `narrative_report_compiler_v1.py` + formatter; or **FE** split if backend change forbidden — weaker).
2. **Sanitizer:** replace whole **statin appendix pattern** or run **phrase-level** replacements after Layer B replacement (`retailNarrativeSanitize.ts`).
3. **Ranking policy:** hide or humanise in `ClinicianReportRenderer.tsx` unless `showDetails` (**requires lifting `showDetails` into context or prop** from `results/page.tsx`).
4. **Evidence chains / ranking rationale:** strip `` `hypothesis_id` `` / `chain_*` from visible prose or gate `<details>` behind global technical mode (`PrimaryFindingAndWhy.tsx`).
5. **Actions:** dedupe or stop double-rendering next steps (`resultsPageLayout.ts` / `results/page.tsx` layout).
6. **Biomarkers:** unit/range QA — likely **backend normalisation**; FE can add **defensive “range unit differs from value unit”** warning only with product approval (avoid inventing clinical logic per `healthiq-frontend-shell`).

### Expected files to touch

- **Backend (recommended):** `backend/core/analytics/narrative_report_compiler_v1.py`, `backend/core/analytics/intervention_annotation_formatter_v1.py`, `backend/core/analytics/narrative_compiler_lc_s3_assembly_v1.py` (and tests under `backend/tests/unit/`).
- **Frontend:** `frontend/app/lib/retailNarrativeSanitize.ts`, `frontend/app/components/results/ResultsBodyOverview.tsx`, `frontend/app/components/results/ClinicianReportRenderer.tsx`, `frontend/app/components/results/PrimaryFindingAndWhy.tsx`, `frontend/app/(app)/results/page.tsx`, `frontend/app/lib/resultsPageLayout.ts`, `frontend/app/components/biomarkers/BiomarkerDials.tsx` (labels + optional unit display).

### Stop conditions

- No new **clinical claims** in FE; no change to **signal scoring** unless explicit LC-S7 scope includes engine.
- Any required **DTO shape** change must be agreed (version bump / API contract).
- After LC-S7, re-run **slug / policy leakage** regression tests (`frontend/tests/regression/slug-leakage-guard.test.ts`, `test_slug_leakage_regression.py` if applicable).

### HIGH-risk backend paths that may be needed

- **Yes, likely:** `narrative_report_compiler_v1.py` and `intervention_annotation_formatter_v1.py` to stop **machine lines** in consumer `body_overview`.
- **Possibly:** biomarker **unit/range normalisation** where values are assembled for the API (outside `frontend/` — needs Automation Bus / core governance if touched).

---

## Evidence basis

Repo reads of the files cited in the tables above; alignment with post-LC-S6 browser strings is **mechanical** (e.g. `Layer B` + `intervention annotation` → `supporting clinical context intervention annotation`).
