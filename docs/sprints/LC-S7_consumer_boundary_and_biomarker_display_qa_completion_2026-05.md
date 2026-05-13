# LC-S7 — Consumer boundary and biomarker display QA (completion)

**Work ID:** `LC-S7-CONSUMER-BOUNDARY-AND-BIOMARKER-DISPLAY-QA`  
**Branch:** `sprint7/consumer-boundary-and-biomarker-display-qa`  
**Authority:** `automation_bus/latest_cursor_prompt.md`, `docs/testing/LC-S7_preflight_triage_post_LC-S6_UAT.md`

## Summary

Closed release-blocking presentation gaps after LC-S6 UAT: consumer `body_overview` no longer carries the machine statin intervention appendix; structural body overview copy is plain-language; LC-S3 assembly removes consumer-hostile headers and raw hypothesis/signal IDs from default prose paths; frontend gates ranking policy strings and technical chain blocks behind **Show technical detail**; action cards dedupe and no longer duplicate full `next_steps_narrative` when that block is already shown; retail sanitizer and biomarker cards cover label and unit/range display safety called out in the sprint.

## Backend (Intelligence Core — governed)

| Area | Change |
|------|--------|
| `narrative_report_compiler_v1.py` | Consumer `body_overview` uses `format_intervention_annotation_consumer_cv_suffix_v1` only; machine appendix remains on the clinician synthesis path (`body_overview_with_ia`). `_build_body_overview` rewritten for consumer prose (no arbitration / governed-title scaffolding). |
| `narrative_compiler_lc_s3_assembly_v1.py` | Secondary block header: “Other patterns considered on this panel”; next steps without “Safe next-step framing” preamble; root-cause and clinician header without raw `hypothesis_id` / `` `signal_id` ``; Layer B/C jargon reduced in surfaced strings. |
| `intervention_annotation_formatter_v1.py` | Consumer statin suffix aligned with sprint wording (“This is taken from your questionnaire…”). |

## Frontend

| Area | Change |
|------|--------|
| `retailNarrativeSanitize.ts` | Additional token scrubbing; explicit mapping for `signal_homocysteine_elevation_context` and `hcy_b12_pattern_v1`. |
| `ClinicianReportRenderer.tsx` | `showTechnicalDetail` prop; ranking policy version visible only when enabled (otherwise sr-only + human summary line). |
| `PrimaryFindingAndWhy.tsx` | Technical `<details>` (chains, ranking rationale) only when `showTechnicalDetail`. |
| `results/page.tsx` | Passes `showDetails` into renderer and primary section; `omitNarrativeNextStepsFromCards` when next-steps narrative exists. |
| `resultsPageLayout.ts` | Narrative preamble line filtered; action card dedupe by normalised paragraph; `omitNarrativeNextStepsFromCards`; `formatBiomarkerDisplayName` LC-S7 label map. |
| `BiomarkerDials.tsx` | Extended `BIOMARKER_NAMES`; suppress incompatible value/range unit pairs with a neutral on-card note (no clinical conversion). |

## Task 6 — Backend scoring / unit conversion

Haemoglobin g/dL vs range g/L and similar **source normalisation** issues remain **out of scope** for this sprint per STOP conditions; frontend only hides inconsistent range rows when units clearly conflict.

## Tests run (targeted)

- `python -m pytest` — `test_lc_s2_statin_context_integration`, `test_lc_s3_narrative_payload_compiler`, `test_narrative_report_compiler_v1`, `test_narrative_compiler_why_surface_regression`, `test_lc_s4_statin_signal_isolation_regression`
- `npx jest` — `retailNarrativeSanitize.test.ts`, `resultsPageLayout.lc-s6.test.ts`, `ClinicianReportRenderer.test.tsx`

## Stash (governed, unchanged)

`stash@{0}` on `feature/questionnaire-visual-redesign` (LC-S1) — not created or modified during LC-S7; human triage if still needed.

## Follow-ups (optional)

- Sentinel or slug-leakage guard expansion for new LC-S7 strings if product wants CI enforcement beyond Jest/pytest touched here.
- Engine/API package if biomarker value and reference range units must be normalised at source.
