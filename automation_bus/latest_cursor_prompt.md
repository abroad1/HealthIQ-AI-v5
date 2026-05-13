---
work_id: LC-S6-RESULTS-RETAIL-HARDENING
branch: sprint6/results-retail-hardening
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# LC-S6 — Results Retail Hardening

## Objective

Make the default HealthIQ AI results page read like a credible patient-facing product, not an internal technical report.

This sprint must harden the visible results experience following browser UAT of:

`/results?analysis_id=b2dfa0c4-efd6-467f-9f2a-84bdf20d8d51`

Primary UAT evidence:

- `UAT_results_page_analysis_b2dfa0c4_2026-05-12.md`

The UAT verdict was **not launch-ready** because consumer-visible pages contain internal architecture language, raw markdown, backend slugs, conflicting primary framing, and an empty Actions hub despite rich next-step content.

This is a retail presentation hardening sprint.

Do not change analytical scoring.
Do not change signal ranking.
Do not change Knowledge Bus assets.
Do not change questionnaire logic.
Do not change backend narrative compiler logic unless a STOP condition is reached and GPT approves.

## Authority and evidence

Primary implementation authority:

- this LC-S6 SOP prompt

Primary evidence source:

- `UAT_results_page_analysis_b2dfa0c4_2026-05-12.md`

Use the UAT report as the factual evidence source for browser-visible defects.

Do not reread historical planning packs unless this prompt and the UAT report conflict.

## Scope

Fix the default consumer-facing results experience.

Expected focus:

- results page copy/rendering
- technical-language filtering/gating
- markdown rendering/stripping
- primary finding alignment
- Actions hub empty-state contradiction
- advanced/clinician section gating
- focused frontend tests
- completion note

## Task 1 — Remove internal architecture language from consumer-visible copy

Inspect the results page and components rendering:

- Summary
- body overview
- lead narrative
- next steps
- domain cards
- advanced teaser
- Actions hub

Remove or rewrite user-visible internal terms including:

- Layer B
- Layer C
- deterministic narrative compiler
- deterministic arbitration
- governed capacity score
- compiler
- payload
- manifest
- runtime
- IDL
- backend slugs
- `cardiovascular_4_biomarkers`
- `chain_001`
- `chain_002`
- `alcohol_intake_moderate_or_higher_with_one_carbon_lab_coherence`
- snake_case marker references where user-facing labels should be shown

Consumer-facing copy should use plain English.

Acceptable replacements:

- “This report is generated from structured clinical rules applied to your lab data.”
- “The main pattern in this result is…”
- “This section explains how the markers fit together.”
- “This context may help explain the pattern, but it does not prove a cause.”

Do not hide uncertainty. Remove the machinery, not the caution.

## Task 2 — Fix raw markdown rendering

The UAT showed literal markdown such as:

- `**Homocysteine Elevation Context**`
- `**does not**`
- `**Methylmalonic acid (MMA)**`

Fix user-visible rendering so raw markdown tokens do not appear.

Acceptable approach:

- strip simple markdown decorators before rendering, or
- render safely using existing markdown utility/component if one already exists

Do not introduce a large new markdown dependency unless already present and approved.

Apply consistently to:

- retail summary
- body overview
- lead narrative
- next steps
- clinician synthesis/advanced content if not already handled

## Task 3 — Align primary story

The UAT found a confusing mismatch:

- hero says: `Vascular Inflammation Risk`
- summary/body says ranked lead is: `Homocysteine Elevation Context`

This must be made coherent.

Required:

- inspect the source of the hero title and the source of the ranked lead narrative
- ensure the default consumer page has one clear primary story
- either align the hero to the ranked lead, or explicitly explain the relationship between the consumer domain label and the ranked lead pattern

Preferred consumer wording style:

- “Primary finding: Homocysteine elevation pattern”
- “Main system context: vascular / cardiovascular risk”
- avoid making the user choose between two apparent primary findings

Do not change backend ranking logic.

If alignment requires backend analytical changes, STOP and report.

## Task 4 — Rewrite Summary subtitle and intro copy

Remove:

- “Plain-language overview from the deterministic narrative compiler.”

Replace with consumer-safe wording, for example:

- “A plain-language summary of the main pattern in your results.”

Also remove copy that says:

- “Layer B frames this…”
- “Layer C…”

The Summary section should be understandable without any knowledge of system architecture.

## Task 5 — Clean body overview and next steps

The UAT found body overview and next steps contain:

- deterministic system snapshot
- deterministic arbitration
- governed capacity score
- Layer C
- system slugs
- internal bridge codes

Fix the rendered body overview and next-step text so consumer view does not expose these tokens.

If these tokens are generated upstream and cannot be safely filtered in the frontend, STOP and report the exact source.

Preferred approach:

- frontend retail sanitiser/gate for known internal tokens, if safe
- or route only approved narrative fields to the consumer view

Do not alter LC-S3 narrative compiler unless approved.

## Task 6 — Gate advanced/clinician technical content more strongly

The UAT found chain IDs, ranking lines and internal marker IDs visible in the default scroll path.

Required:

- ensure clinician/advanced content is clearly separated from consumer content
- keep technical detail behind explicit “technical / clinician” disclosure
- do not show chain IDs or snake_case evidence labels in default consumer sections
- where marker IDs appear, use display labels where available

Advanced content may remain technical, but it must not leak into the default retail journey.

## Task 7 — Fix Actions hub contradiction

The UAT found the Actions hub says:

“No actions to show yet”

while the results page contains rich next-step/follow-up content.

Required:

- inspect why Actions hub receives no action cards
- either:
  - wire it to the governed `actions` / `interventions_v1` / next-step source already present in the result, or
  - remove/de-emphasise the Actions hub entry point until real action cards are available

Do not show generic legacy insights.

Do not reintroduce `legacy_v1 insights[]`.

If safe wiring requires backend DTO changes, STOP and report.

## Task 8 — Fix mock-mode honesty banner wording

The UAT found the banner wording is partially garbled:

- “AI-per narrative is not active…”

Fix display wording to exactly:

“Your report is built from structured clinical rules applied to your lab data. AI-personalised narrative is not active in this view.”

Use “structured clinical rules” rather than “governed clinical rules” for consumer clarity.

## Task 9 — Remove internal roadmap labels

Remove or rewrite:

- “Wave 1”

from user-facing domain headings.

Preferred:

- “Your health domains”
- “Main health areas reviewed”
- “System-level patterns”

## Task 10 — Tests

Add or update frontend tests proving:

- no `Layer B` visible in default results page
- no `Layer C` visible in default results page
- no `deterministic narrative compiler` visible
- no `deterministic arbitration` visible
- no backend system slug such as `cardiovascular_4_biomarkers` visible
- no raw markdown `**` appears in summary/body/next-step rendering
- no bridge slug such as `alcohol_intake_moderate_or_higher_with_one_carbon_lab_coherence` appears
- Summary subtitle uses consumer-safe copy
- mock-mode banner uses approved wording
- Actions hub does not show contradictory empty state when governed actions/interventions exist
- legacy `insights[]` remain hidden from consumer paths

## Expected files touched

Expected:

- `frontend/app/(app)/results/page.tsx`
- `frontend/app/(app)/actions/page.tsx`
- frontend result components under `frontend/app/components/results/`
- frontend copy/sanitisation helpers if needed
- frontend tests
- `docs/sprints/LC-S6_results_retail_hardening_completion_2026-05.md`

Possibly expected:

- frontend types if needed for safe action/intervention wiring

Not expected:

- `backend/ssot/`
- `knowledge_bus/`
- `backend/core/analytics/`
- `backend/core/pipeline/`
- `backend/core/contracts/`
- questionnaire files
- narrative compiler files
- biomarker scoring logic
- Automation Bus control-plane scripts
- Sentinel files

## Stop conditions

STOP and report before implementation if:

- fixing consumer copy requires changing analytical ranking logic
- fixing hero alignment requires backend scoring/ranking changes
- removing internal language requires changing LC-S3 narrative compiler logic
- Actions hub wiring requires backend DTO/schema changes
- any Knowledge Bus, SSOT, pipeline, analytics, or contract files appear necessary
- legacy `insights[]` would need to be reintroduced to populate Actions hub
- safe markdown rendering requires adding a large dependency

## Explicit non-goals

Do not:

- change analytical scoring
- change signal ranking
- change biomarker interpretation
- change questionnaire logic
- change Knowledge Bus assets
- change SSOT
- change narrative compiler assembly
- activate Gemini
- build frontend Sentinel infrastructure
- perform full biomarker unit/status QA in this sprint
- change PDF/export structure unless the same rendered components are reused automatically

## Completion note

Create:

`docs/sprints/LC-S6_results_retail_hardening_completion_2026-05.md`

It must record:

- UAT blockers addressed
- internal terms removed/gated
- markdown rendering fix
- hero/summary alignment decision
- Actions hub decision
- tests run
- known limitations
- confirmation no backend analytical, SSOT, Knowledge Bus, questionnaire, narrative compiler, or control-plane files changed

## Validation

Run relevant frontend tests.

At minimum:

- results page/component tests
- Actions page tests
- legacy insights visibility tests
- LC-S4 report-carriage tests
- any new LC-S6 leakage tests

Then run broader frontend test suite if feasible.

Report all commands and results.

## Closure evidence required

Before finish, report:

- branch
- work_id
- files changed
- before/after summary of major copy fixes
- whether internal terms are absent from default consumer page
- whether raw markdown is absent
- whether hero and ranked lead are coherent
- whether Actions hub contradiction is resolved
- whether legacy insights remain hidden
- tests run and results
- confirmation no backend analytical files changed
- confirmation no SSOT files changed
- confirmation no Knowledge Bus files changed
- confirmation no questionnaire files changed
- confirmation no narrative compiler files changed
- confirmation no Automation Bus control-plane scripts changed

## Final expected outcome

After LC-S6, the default results page should feel like a credible patient-facing HealthIQ AI report.

It should show the user the main finding clearly, explain the result in plain English, preserve appropriate caution, and hide internal system machinery unless deliberately opened in a technical/clinician view.