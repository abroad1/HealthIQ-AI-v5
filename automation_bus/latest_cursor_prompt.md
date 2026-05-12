---
work_id: LC-S4-LAUNCH-CORE-REPORT-CARRIAGE
branch: sprint4/launch-core-report-carriage
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# LC-S4 — Launch-Core Report Carriage

## Objective

Implement Sprint 4: make the frontend results experience faithfully carry the governed launch-core report now produced by the backend.

The backend now produces governed narrative output through:

`ReportV1 → NarrativePayloadV1 → NarrativeReportV1`

Sprint 4 must make that governed output visible, coherent, honest, and non-placeholder across the launch-core report surfaces.

This is not an analytical engine sprint.

Do not change biomarker interpretation logic.  
Do not change questionnaire logic.  
Do not change Knowledge Bus assets.  
Do not change the LC-S3 narrative compiler assembly logic unless a STOP condition is reached and explicit approval is given.

## Authority and evidence

Primary implementation authority:

- This LC-S4 SOP prompt

Primary evidence source:

- `docs/audit-papers/lc_s4_report_carriage_readiness_audit.md`

Claude has already completed the LC-S4 readiness audit. Cursor should use that audit as the factual source for file locations, current gaps, and recommended implementation scope.

Historical authority, for conflict resolution only:

- `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md`
- `docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md`

Do not reread the full historical planning pack unless the LC-S4 audit and this prompt conflict or are unclear.

## Risk classification

This work package is HIGH risk because Task 6 touches:

`backend/core/analytics/intervention_annotation_formatter_v1.py`

Although the intended change is bounded wording/formatter work and must not alter analytical logic, the file path is mechanically HIGH risk under the Automation Bus SOP.

Therefore this package requires Claude audit and GPT architectural review before merge.

## Pre-start requirement

Before starting LC-S4 implementation, the stale WP3 Automation Bus token must be resolved.

Known issue:

`automation_bus/state/work_package_active.json` may still record:

`WP3-QUESTIONNAIRE-RATIONALISATION`

as `STARTED`, even though WP3 has been merged to `main`.

Cursor must resolve this through the SOP-compliant closure path before starting LC-S4.

Preferred command:

```bash
python backend/scripts/run_work_package.py finish
````

If the command cannot run because WP3 is already merged or the token state is inconsistent, STOP and report the exact error and the SOP-compliant token resolution path.

Do not manually edit control-plane state unless explicitly instructed after reporting.

## Key audit findings to address

The LC-S4 audit found that the backend is producing governed narrative fields, but the frontend is not carrying them sufficiently:

* `body_overview` is produced but not rendered anywhere.
* `retail_summary` is bypassed on IDL panels and is effectively invisible in AB/VR launch-core cases.
* `lead_narrative` and `next_steps_narrative` exist but are hidden inside a collapsed “What this means” section.
* `insights[]` / `legacy_v1` still leaks into consumer-facing paths.
* mock-mode honesty wording is not implemented.
* statin context reaches the frontend in technical wording rather than consumer-readable language.
* `clinician_synthesis` can render literal markdown tokens.

## Scope

Implement bounded report-carriage changes only.

Expected focus:

* frontend results page wiring
* frontend Actions hub legacy-insights gating
* mock-mode honesty disclosure
* consumer-safe statin formatter wording
* clinician synthesis rendering cleanup
* focused tests
* Sprint 4 completion note

## Task 1 — Wire `body_overview`

File:

* `frontend/app/(app)/results/page.tsx`

Required:

* import `ResultsBodyOverview`
* render it using `narrativeReport?.body_overview`
* keep existing props expected by the component, including `clinicianReport` and `clusters`
* recommended placement: inside “What this means”, before the investigation spine / lead narrative components

Purpose:

`body_overview` is the cross-system posture section. It is currently produced by the backend but invisible to users. It also carries medication/context appendix content where available.

Do not alter backend narrative compiler output.

## Task 2 — Wire `NarrativeRetailSummaryCard`

Files:

* `frontend/app/(app)/results/page.tsx`
* existing component in `frontend/app/components/results/DeterministicNarrativeSurface.tsx`

Required:

* import and render `NarrativeRetailSummaryCard`
* pass the full `narrativeReport` object to the component, not `narrativeReport?.retail_summary`
* expected JSX shape should be equivalent to:

```tsx
<NarrativeRetailSummaryCard narrative={narrativeReport} />
```

Purpose:

`retail_summary` must be visible even when IDL records exist. It must not remain only a hero fallback.

The component itself reads `narrative?.retail_summary` internally.

## Task 3 — Make “What this means” open by default

File:

* `frontend/app/(app)/results/page.tsx`
* or `frontend/app/components/results/ResultsDisclosureSection.tsx` if that is where default state is controlled

Required:

* default the “What this means” section to open

Purpose:

This section contains the core governed explanation. Keeping it collapsed hides the most valuable part of the report and weakens the visible personalisation payoff.

Do not default all advanced/clinician sections open. Only “What this means”.

## Task 4 — Implement mock-mode honesty disclosure

File:

* `frontend/app/(app)/results/page.tsx`

Required:

* show a visible but non-intrusive disclosure near the top of the report, preferably between the page header and hero card
* use existing `narrativeRuntime` extraction
* condition: show when `narrativeRuntime?.synthesizer_allow_llm_resolved === false` or equivalent deterministic/mock runtime condition

Use this exact approved wording:

> Your report is built from governed clinical rules applied to your lab data. AI-personalised narrative is not active in this view.

Use existing UI primitives if available, such as `Alert` and `AlertDescription`.

Do not invent alternative wording unless the current component requires minor punctuation only.

## Task 5 — Retire `insights[]` from consumer-visible paths

Files likely involved:

* `frontend/app/(app)/results/page.tsx`
* `frontend/app/(app)/actions/page.tsx`
* possibly `frontend/app/lib/resultsPageLayout.ts`
* possibly `frontend/app/state/clusterStore.ts`

Required:

1. Stop passing `insights` into `buildActionCardModels` on the results page.
2. Stop passing `insights` into `buildActionCardModels` on the Actions page.
3. Remove or gate the advanced-section alert that says short narrative summaries are available when the only available data is legacy `insights[]`.
4. Remove or gate `InsightsPanel` on the launch-core report path when the content is `manifest_id: "legacy_v1"`.
5. Do not delete backend `AnalysisDTO.insights` in this sprint.

Acceptable approaches:

* remove consumer rendering of legacy insights entirely
* or gate behind an explicit development/debug flag such as `HEALTHIQ_LEGACY_INSIGHTS`

Do not allow `legacy_v1` recommendations to appear in the consumer Actions hub.

## Task 6 — Improve statin consumer wording

File:

* `backend/core/analytics/intervention_annotation_formatter_v1.py`

Required:

* update `format_intervention_annotation_consumer_cv_suffix_v1()` so it produces consumer-readable wording
* preserve the meaning: statin context is user-reported, framing only, and must not alter signal states, bands, or rankings
* do not change the intervention annotation engine
* do not change signal scoring
* do not change statin detection logic

The wording should be understandable to a paying user.

Acceptable style:

> Statin medication noted — this may help explain lower LDL-related readings on this panel.

Do not make treatment claims.
Do not advise medication use.
Do not imply causality beyond cautious context.

## Task 7 — Strip markdown tokens from clinician synthesis rendering

File:

* `frontend/app/components/results/ClinicianReportRenderer.tsx`

Required:

* prevent visible raw markdown tokens such as `**` and backticks appearing in `clinician_synthesis`
* either strip simple markdown markers before rendering or render safely with an existing markdown-capable component if one already exists
* do not introduce a large new markdown dependency unless already present in the repo

This is a display cleanup only.

## Task 8 — Tests

Add or update focused tests.

Required coverage:

### Narrative carriage

* `body_overview` renders when non-empty
* `retail_summary` renders even when IDL records are present
* “What this means” defaults open
* `lead_narrative` remains rendered
* `next_steps_narrative` remains rendered

### Mock-mode honesty

* approved disclosure appears when `synthesizer_allow_llm_resolved === false`
* disclosure does not appear when LLM/personalisaton mode is active, if such a fixture exists

### Legacy insights retirement

* `legacy_v1 insights[]` do not feed Actions hub cards
* advanced “narrative summaries available” alert does not render for legacy-only insights
* `InsightsPanel` is not visible on the launch-core consumer path unless explicitly debug-gated

### Consumer / clinician boundary

* clinician synthesis remains only in the advanced/clinician section
* clinician synthesis renders without raw markdown markers
* existing IDL `clinical_only` exclusion test still passes

### Statin wording

* consumer statin formatter output is human-readable
* output does not include internal phrases such as:

  * `Layer B intervention annotation`
  * `direction=`
  * raw biomarker ID lists
* output does not recommend medication or treatment

## Sentinel consideration

Before merge, ask Claude/Sentinel owner whether any LC-S4 tests should be promoted to Sentinel.

Strong Sentinel candidates:

* legacy `insights[]` not visible on consumer Actions path
* IDL `clinical_only` gate remains protected
* mock-mode honesty disclosure appears when LLM is inactive
* `body_overview` / `retail_summary` carriage does not regress

Do not modify Sentinel unless instructed through the correct Sentinel ownership process.

## Expected files touched

Expected frontend:

* `frontend/app/(app)/results/page.tsx`
* `frontend/app/(app)/actions/page.tsx`
* `frontend/app/components/results/ClinicianReportRenderer.tsx`
* relevant frontend tests

Expected backend:

* `backend/core/analytics/intervention_annotation_formatter_v1.py`
* relevant backend formatter tests

Expected docs:

* `docs/sprints/LC-S4_launch_core_report_carriage_completion_2026-05.md`

Possibly expected:

* `frontend/app/lib/resultsPageLayout.ts`
* `frontend/app/state/clusterStore.ts`
* component test fixtures / mocks

Not expected:

* `backend/ssot/`
* `knowledge_bus/`
* `backend/core/models/results.py`
* `backend/core/analytics/narrative_report_compiler_v1.py`
* `backend/core/analytics/narrative_compiler_lc_s3_assembly_v1.py`
* `backend/core/contracts/narrative_payload_v1.py`
* questionnaire files
* biomarker interpretation logic
* Automation Bus control-plane scripts
* Sentinel files unless separately approved

## Stop conditions

STOP and report before implementation if:

* the WP3 active token cannot be resolved through the SOP-compliant finish path
* `body_overview` is not present on `NarrativeReportV1`
* `ResultsBodyOverview` no longer exists
* `NarrativeRetailSummaryCard` no longer exists
* mock-mode runtime metadata is unavailable on the results page
* removing `insights` from action-card inputs leaves the Actions hub empty with no governed fallback
* statin consumer wording requires changing intervention annotation semantics
* any change requires touching Knowledge Bus, SSOT, biomarker scoring, narrative compiler assembly, or AnalysisDTO structure
* any frontend report change requires broad redesign outside the results/action surfaces
* Sentinel changes appear necessary but Claude/Sentinel owner has not approved them

## Explicit non-goals

Do not:

* change the analytical engine
* change signal ranking
* change confidence or banding
* change questionnaire logic
* change Knowledge Bus assets
* change SSOT files
* change `NarrativePayloadV1`
* change LC-S3 narrative assembly logic
* activate Gemini
* implement Sprint 5 proving harness CHECKs
* add new WHY assets
* implement longitudinal narrative
* delete backend `AnalysisDTO.insights`

## Completion note

Create:

`docs/sprints/LC-S4_launch_core_report_carriage_completion_2026-05.md`

It must record:

* report surfaces changed
* how `body_overview` is now carried
* how `retail_summary` is now carried
* how mock-mode honesty is shown
* how legacy `insights[]` is gated/removed from consumer paths
* how statin wording changed
* how clinician synthesis display was cleaned
* tests run
* known limitations
* confirmation that no SSOT, Knowledge Bus, questionnaire, biomarker interpretation, or LC-S3 compiler files were changed
* confirmation Claude audit and GPT architectural review are required before merge because this is HIGH risk

## Validation commands

Inspect repo scripts and run targeted tests first.

At minimum, run:

* frontend results-page/component tests touched by Sprint 4
* frontend actions-page tests if available
* frontend IDL clinical-only gate test
* backend intervention annotation formatter test
* any affected result layout tests

Then run broader frontend/backend tests if feasible.

Report every command and result.

## Closure evidence required

Before finish, report:

* branch
* work_id
* files changed
* whether `body_overview` is rendered
* whether `retail_summary` is rendered
* whether “What this means” defaults open
* whether mock-mode honesty wording appears
* whether legacy `insights[]` are removed/gated from consumer paths
* whether statin wording is consumer-readable
* whether clinician synthesis renders without raw markdown tokens
* tests run and results
* confirmation no SSOT files changed
* confirmation no Knowledge Bus files changed
* confirmation no questionnaire files changed
* confirmation no biomarker interpretation logic changed
* confirmation no LC-S3 narrative compiler assembly logic changed
* confirmation Claude audit and GPT architectural review are completed before merge

## Final expected outcome

After LC-S4, the launch-core report should visibly carry the governed backend output.

The report should feel coherent, honest, and production-facing rather than hiding governed narrative in collapsed sections or leaking legacy placeholder `insights[]`.

