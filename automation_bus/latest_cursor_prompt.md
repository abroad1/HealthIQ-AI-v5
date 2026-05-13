---
work_id: LC-S7-CONSUMER-BOUNDARY-AND-BIOMARKER-DISPLAY-QA
branch: sprint7/consumer-boundary-and-biomarker-display-qa
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# LC-S7 — Consumer Boundary and Biomarker Display QA

## Objective

Fix the remaining release-blocking defects found after LC-S6 browser UAT.

The post-LC-S6 page is materially improved, but it is still not safe for controlled external testing because technical/compiler content is still entering the default consumer journey, and biomarker cards expose unit/range/display inconsistencies.

This sprint must make the results page safe for a human consumer while preserving the governed analytical truth.

Do not change scoring.  
Do not change signal activation.  
Do not change ranking.  
Do not change questionnaire logic.  
Do not change Knowledge Bus assets.  
Do not introduce new clinical claims.

## Authority and evidence

Primary implementation authority:

- this LC-S7 SOP prompt

Primary evidence source:

- `LC-S7_preflight_triage_post_LC-S6_UAT.md`

Use the preflight triage as the factual source for current defects, source paths, and recommended fix direction. The preflight concluded that frontend sanitising alone is insufficient and that the cleaner fix likely requires separating consumer narrative from technical appendix content. :contentReference[oaicite:0]{index=0}

## Risk classification

This package is HIGH risk because the cleanest fix may touch:

- `backend/core/analytics/narrative_report_compiler_v1.py`
- `backend/core/analytics/intervention_annotation_formatter_v1.py`
- `backend/core/analytics/narrative_compiler_lc_s3_assembly_v1.py`

These are HIGH-risk paths under the Automation Bus SOP.

Therefore this package requires Claude audit and GPT architectural review before merge.

## Strategic principle

The consumer report must show:

- what matters
- why it matters
- what is uncertain
- what to discuss next

It must not show:

- compiler scaffolding
- machine appendix lines
- DTO/version/policy identifiers
- signal IDs
- chain IDs
- hypothesis IDs
- effect-type enums
- internal bridge codes
- raw backend slugs

Technical material may remain available only behind a clearly marked clinician/technical-detail boundary.

## Task 1 — Stop machine intervention appendix leaking into consumer Body Overview

Problem observed:

Consumer Body Overview still displays content such as:

- `supporting clinical context intervention annotation`
- `expected_biomarker_effect`
- `[ldl_cholesterol, non_hdl_cholesterol, apob]`
- `direction=lower`
- statin monitoring fragments intended for technical/clinician context

Required:

- inspect `narrative_report_compiler_v1.py`
- inspect `intervention_annotation_formatter_v1.py`
- identify exactly where intervention appendix text is appended to `narrative_report_v1.body_overview`
- prevent raw technical appendix content from being appended into the consumer body overview

Preferred implementation:

- keep `body_overview` consumer-safe
- use the existing consumer-facing statin suffix where appropriate
- keep machine/technical appendix available only in clinician/technical sections if already supported
- do not alter intervention annotation semantics

Acceptable consumer statin wording:

“Statin medication noted — this may help explain lower LDL-related readings on this panel. This is taken from your questionnaire as context only and does not change how signals are scored or ranked.”

Do not include internal biomarker arrays, effect types, or direction fields in consumer prose.

## Task 2 — Clean Body Overview structural wording

Problem observed:

Body Overview still contains technical framing such as:

- `governed functional titles`
- `clinical prioritisation on this panel`
- `confidence score ≥90`
- long system lists that feel like compiler output

Required:

- make Body Overview read as a short consumer summary
- retain the same underlying meaning
- remove internal/compiler phrasing
- reduce long lists where possible

Preferred style:

“Your main finding sits in a cardiovascular/vascular context. Most other system groups look broadly stable on this panel, which helps place the concern in perspective rather than suggesting the whole panel is off track.”

Do not remove clinically relevant reassurance.

## Task 3 — Gate or humanise clinician/technical identifiers

Problem observed:

The visible page still exposes:

- `signal_homocysteine_elevation_context`
- `PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_V1`
- `chain_001`
- `chain_002`
- `hcy_b12_pattern_v1`
- suppressed confirmatory test IDs
- raw hypothesis/ranking identifiers

Required:

- inspect `ClinicianReportRenderer.tsx`
- inspect `PrimaryFindingAndWhy.tsx`
- inspect `results/page.tsx`
- ensure these identifiers are not visible in default consumer scroll paths

Acceptable fixes:

- hide behind explicit “Show technical detail”
- rewrite as human labels
- remove from default rendering
- use display labels instead of IDs

Do not delete underlying data from DTOs.

## Task 4 — Fix secondary ranked pattern heading

Problem observed:

Secondary ranked patterns still use technical ordering language, e.g.:

- `supporting clinical context order, deterministic`

Required:

- inspect `narrative_compiler_lc_s3_assembly_v1.py`
- replace technical heading with consumer-safe wording, or keep secondary-ranked details out of default consumer view

Preferred wording:

“Other patterns considered on this panel”

or:

“Additional patterns the engine reviewed”

Do not change ranking logic.

## Task 5 — Dedupe Actions and Next Steps

Problem observed:

Actions cards duplicate “Safe next-step framing” / repeated follow-up text.

Required:

- inspect `resultsPageLayout.ts`
- inspect results action components
- inspect `/actions/page.tsx`
- ensure actions are not duplicative or awkward when generated from `next_steps_narrative`

Required behaviour:

- no repeated “Safe next-step framing” preamble
- no duplicate cards with the same first sentence
- no legacy insights reintroduced
- no internal source labels that read like data plumbing

Acceptable approach:

- dedupe by normalised text
- strip preamble before card generation
- prefer concise action cards over repeating full narrative blocks

## Task 6 — Biomarker display QA: unit/range coherence

Investigate and fix display-level issues where possible without changing scoring.

Known examples from UAT:

- Haemoglobin displays `144 g/dL` with range `130–175 g/L`
- Haematocrit displays `0.4 %` with range `0.35–0.48 L/L`
- HbA1c displays `%` while reference range may be mmol/mol
- Testosterone displays “Not scored - no reference range available” despite source range concern
- ratio labels such as `tc hdl ratio`
- lower-case labels such as `active b12`, `apoa1`, `non hdl cholesterol`

Required:

- inspect biomarker card display pipeline
- identify whether each issue is:
  - source data/API
  - unit normalisation
  - reference range attachment
  - frontend display formatting
  - label registry gap

Fix frontend display/label issues where safe.

If unit/range inconsistency originates in backend source data or scoring, STOP before changing backend interpretation logic and report the exact file/path and recommended next package.

Allowed frontend fixes:

- improve display labels
- hide incompatible range display if value unit and range unit clearly conflict
- add neutral wording such as “range unit differs from displayed unit” only if product-approved in implementation notes
- fix obvious label registry names

Do not invent clinical unit conversions in frontend unless there is an existing governed conversion utility.

## Task 7 — Improve biomarker labels

Add or update label mapping for common display defects:

- `tc_hdl_ratio` → `TC:HDL ratio`
- `tg_hdl_ratio` → `TG:HDL ratio`
- `ldl_hdl_ratio` → `LDL:HDL ratio`
- `non_hdl_cholesterol` → `Non-HDL cholesterol`
- `active_b12` → `Active B12`
- `apoa1` → `ApoA1`
- `apob` → `ApoB`
- `egfr` → `eGFR`
- `mcv` → `MCV`
- `mch` → `MCH`
- `mchc` → `MCHC`
- `fsh` → `FSH`
- `lh` → `LH`
- `ggt` → `GGT`
- `tsh` → `TSH`

Use existing label registry or frontend mapping pattern if present.

Do not create duplicate competing label registries if one already exists.

## Task 8 — Tests

Add or update tests proving:

### Consumer boundary

- default consumer results view does not show:
  - `supporting clinical context intervention annotation`
  - `expected_biomarker_effect`
  - `direction=lower`
  - `governed functional titles`
  - `confidence framing (governed label)`
  - `supporting clinical context order, deterministic`
  - `signal_homocysteine_elevation_context`
  - `PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY`
  - `chain_001`
  - `hcy_b12_pattern_v1`

### Body overview

- `body_overview` renders consumer-safe prose
- statin context appears only in consumer-safe wording
- technical statin appendix is not visible in consumer Body Overview

### Actions

- no duplicate cards from the same next-step sentence
- “Safe next-step framing” preamble is not rendered as an action card
- legacy insights remain hidden

### Biomarker display

- label mappings render key markers correctly
- unit/range mismatch is handled safely for haemoglobin and haematocrit
- ratio labels render professionally

## Expected files touched

Expected backend, if needed:

- `backend/core/analytics/narrative_report_compiler_v1.py`
- `backend/core/analytics/intervention_annotation_formatter_v1.py`
- `backend/core/analytics/narrative_compiler_lc_s3_assembly_v1.py`
- relevant backend unit tests

Expected frontend:

- `frontend/app/lib/retailNarrativeSanitize.ts`
- `frontend/app/lib/resultsPageLayout.ts`
- `frontend/app/components/results/ResultsBodyOverview.tsx`
- `frontend/app/components/results/ClinicianReportRenderer.tsx`
- `frontend/app/components/results/PrimaryFindingAndWhy.tsx`
- `frontend/app/components/biomarkers/BiomarkerDials.tsx`
- `frontend/app/(app)/results/page.tsx`
- relevant frontend tests

Expected docs:

- `docs/sprints/LC-S7_consumer_boundary_and_biomarker_display_qa_completion_2026-05.md`

Not expected:

- `backend/ssot/`
- `knowledge_bus/`
- questionnaire files
- signal scoring files
- ranking policy files
- Automation Bus control-plane scripts
- Sentinel files unless separately requested
- database migrations

## Stop conditions

STOP and report before implementation if:

- fixing consumer leakage requires changing signal activation
- fixing consumer leakage requires changing ranking logic
- unit/range correction requires clinical unit conversion not already governed
- biomarker display correction requires backend scoring changes
- Knowledge Bus or SSOT changes appear necessary
- DTO/schema shape changes appear necessary
- frontend cannot distinguish default consumer view from technical/clinician view safely
- intervention annotation semantics would change
- Automation Bus control-plane files appear necessary

## Explicit non-goals

Do not:

- change analytical scoring
- change signal ranking
- change signal activation
- change questionnaire logic
- change Knowledge Bus assets
- change SSOT
- activate Gemini
- build frontend Sentinel infrastructure
- perform full clinical biomarker range redesign
- rewrite the whole results page
- create a new report architecture
- add medication/treatment recommendations
- recommend supplements

## Validation

Run targeted tests first.

At minimum:

- relevant backend narrative/formatter tests if backend touched
- frontend results page/component tests
- frontend biomarker display tests
- LC-S6 leakage tests
- Actions layout tests

Then run broader frontend/backend tests if feasible.

```