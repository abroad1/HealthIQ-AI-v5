# LC-S4 — Launch-core report carriage (completion note)

**Work ID:** LC-S4-LAUNCH-CORE-REPORT-CARRIAGE  
**Branch:** `sprint4/launch-core-report-carriage`  
**Date:** 2026-05-12

## Report surfaces changed

- **Results (`frontend/app/(app)/results/page.tsx`)** — governed narrative carriage, mock-mode honesty, legacy insight gating, default disclosure for “What this means”.
- **Actions hub (`frontend/app/(app)/actions/page.tsx`)** — action cards built only from cluster and panel recommendations (no `insights[]` fold-in).
- **Clinician report renderer (`frontend/app/components/results/ClinicianReportRenderer.tsx`)** — deterministic `clinician_synthesis` display strips simple markdown markers.
- **Backend formatter (`backend/core/analytics/intervention_annotation_formatter_v1.py`)** — consumer statin context line only (plain language; no internal appendix leak).

Supporting modules:

- `frontend/app/lib/legacyInsightsVisibility.ts` — `legacy_v1` filtering and `NEXT_PUBLIC_HEALTHIQ_LEGACY_INSIGHTS` debug gate.
- `frontend/app/lib/lcS4ResultsCopy.ts` — sprint-approved mock-mode disclosure string (single source of truth).

## How `body_overview` is now carried

`ResultsBodyOverview` is rendered inside the **“What this means”** section **before** the investigation spine, with `compiledBodyOverview={narrativeReport?.body_overview}` so the backend-compiled cross-system posture text is preferred over the heuristic primary sentence when present.

## How `retail_summary` is now carried

`NarrativeRetailSummaryCard` is rendered on the main results column **after** the primary hero and **before** driving signals, with `narrative={narrativeReport}` so `retail_summary` stays visible even when IDL records exist (the card reads `retail_summary` internally).

## How mock-mode honesty is shown

When `narrativeRuntime?.synthesizer_allow_llm_resolved === false`, an `Alert` appears between the page header block and the hero, using the **exact** approved copy from `lcS4ResultsCopy.ts` (matches sprint prompt).

## How legacy `insights[]` is gated / removed from consumer paths

- **Results & Actions:** `buildActionCardModels` is called **without** the `insights` option, so legacy recommendation lines no longer populate consumer action cards.
- **Advanced “narrative summaries” alert:** Shown only when `consumerInsights.length > 0` (after legacy filter), so legacy-only payloads do not trigger the “short narrative summaries available” message.
- **`InsightsPanel`:** The “Narrative summaries” block is omitted unless `NEXT_PUBLIC_HEALTHIQ_LEGACY_INSIGHTS` is `true`/`1` **or** there is at least one non-`legacy_v1` insight after filtering. Legacy rows remain in the DTO but are not shown on the default consumer path.
- **`Insight` type:** Optional `manifest_id` added for alignment with backend DTOs.

## How statin wording changed

`format_intervention_annotation_consumer_cv_suffix_v1()` now returns a short, consumer-readable statin context line (questionnaire-sourced, framing-only) instead of echoing the technical Layer B appendix. Appendix/clinician formatting is unchanged.

## How clinician synthesis display was cleaned

`deterministicClinicianSynthesis` is passed through a small normaliser that removes common markdown emphasis / code markers before rendering as plain text in the advanced section.

## Tests run (targeted)

**Frontend (Jest):**

```text
npm test -- tests/lib/legacyInsightsVisibility.test.ts tests/lib/lcS4ResultsCopy.test.ts tests/components/DeterministicNarrativeSurface.lc-s4.test.tsx tests/components/ResultsBodyOverview.lc-s4.test.tsx tests/components/ResultsDisclosureSection.lc-s4.test.tsx tests/components/ClinicianReportRenderer.test.tsx tests/components/InterpretationPatternsSection.test.tsx
```

Result: **7 suites passed, 19 tests passed.**

**Backend (pytest):**

```text
python -m pytest backend/tests/unit/test_lc_s2_statin_context_integration.py::test_s5_visible_narrative_and_consumer_suffix_difference_when_annotation_present -q
```

Result: **1 passed.**

## Known limitations

- **Automation Bus Stage 2:** `latest_prompt_hardening.json` was aligned to this `work_id` for kernel preflight after WP3 `finish`; **full Stage 2C hardening evidence from Claude should still be completed for merge governance** on this HIGH-risk package.
- **Stash:** `stash@{0}` on `feature/questionnaire-visual-redesign` was **not** modified; disposition is left to the operator (governed triage).
- **Sentinel:** Not changed per sprint instructions.

## Scope confirmations (non-goals)

- **No** `backend/ssot/` changes.
- **No** `knowledge_bus/` changes.
- **No** questionnaire asset or interpretation-logic changes.
- **No** `narrative_compiler_lc_s3_assembly_v1` or `NarrativePayloadV1` changes.
- **No** deletion of `AnalysisDTO.insights` / backend `insights` array.
- **No** Automation Bus control-plane script edits.

## Merge governance

This package is **HIGH risk** (includes `backend/core/analytics/intervention_annotation_formatter_v1.py`). **Claude audit summary and GPT architectural review are required before merge**, per `AUTOMATION_BUS_SOP_v1.3.1` and the sprint prompt.
