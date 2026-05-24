---
work_id: FE-R2
branch: frontend/fe-r2-results-journey-restructure
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# FE-R2 — Results Journey Restructure

## Classification

This is a HIGH-risk MIXED sprint.

Reason: this sprint changes the consumer-facing results-page structure and may touch frontend rendering, DTO field consumption, section ordering, visibility defaults, regression tests, Sentinel packs and audit documentation.

This is not a backend prose rewrite sprint.  
This is not a Knowledge Bus expansion sprint.  
This is not a Gemini/LLM sprint.  
This is not a clinical logic/scoring/unit sprint.  
This is not a medication-overlay sprint.  
This is not a full visual redesign sprint.  
This is not a Phase 2 patterns-layer implementation sprint.

## Purpose

Restructure the current results page into the Phase 1 guided reasoning journey defined in the v6 recommendation paper, now that FE-R1 has cleaned the most unsafe consumer prose.

The goal is to make the page understandable to a retail user by putting existing deterministic assets into the correct narrative order.

FE-R2 must implement the page journey structure. It must not attempt to solve every prose/content weakness, visual design issue, or future Phase 2 pattern-layer requirement.

## Controlling authority

Read before doing anything:

```text
docs/frontend/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md
docs/audit-papers/FE_R0_results_page_prose_source_trace_audit.md
docs/audit-papers/FE-R1_consumer_prose_cleanup_narrative_safety_notes.md
docs/architecture/HealthIQ_AI_runtime_architecture_map_v1.md
docs/developer-guides/healthiq_scaffold_guardrails_v1.md
docs/audit-papers/LC_SCAFFOLD_CLOSEOUT_transition_review.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
````

Also inspect if present:

```text
docs/audit-papers/LC-S16_knowledge_asset_frontend_surface_audit.md
docs/audit-papers/LC-S19_payload_contract_hardening_notes.md
docs/audit-papers/LC-S20_22_persisted_replay_sentinel_phase2_notes.md
```

If the FE-R0 audit, FE-R1 notes, or v6 recommendation paper are missing, STOP.

## FE-R1 merge precondition

Before implementation, confirm FE-R1 is merged to `main`.

Evidence may include:

* FE-R1 merge commit on main ancestry
* `test_fe_r1_consumer_prose_cleanup.py` exists and passes
* FE-R1 notes exist
* FE-R1 Sentinel classes exist

If FE-R1 is not on main, STOP. Do not restructure the page on top of pre-FE-R1 prose.

## Required output documentation

Create:

```text
docs/audit-papers/FE-R2_results_journey_restructure_notes.md
```

This document must include:

1. preflight results
2. FE-R1 merge confirmation
3. current page structure before change
4. implemented FE-R2 section order
5. frontend files changed
6. DTO/API fields consumed by each section
7. sections moved, removed, collapsed, or retained
8. explicit list of things not changed
9. tests added/updated
10. Sentinel updates
11. browser/UAT evidence if performed
12. residual risks
13. recommendation for FE-R3

## Mandatory preflight

Run and record:

```powershell
git branch --show-current
git status --short
git log --oneline -n 12
git stash list
```

Verify work-package token:

```powershell
Test-Path automation_bus/state/work_package_active.json
```

Read `automation_bus/state/work_package_active.json` and confirm:

* `work_id` is `FE-R2`
* branch is `frontend/fe-r2-results-journey-restructure`

If token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

## Cross-sprint guard preflight

Run current FE/scaffold guards before implementation.

At minimum:

```powershell
python -m pytest backend/tests/regression/test_fe_r1_consumer_prose_cleanup.py -q
python -m pytest backend/tests/regression/test_lc_s13_lifestyle_coherence_narrative.py -q
python -m pytest backend/tests/regression/test_lc_s14_direction_aware_scoring.py -q
python -m pytest backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py -q
python -m pytest backend/tests/regression/test_lc_s18_root_cause_why_registration.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
python -m pytest backend/tests/regression/test_lc_s18a_package_estate_inventory.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

If a prior guard fails, STOP unless GPT/human authority explicitly authorises continuation.

## Phase 1 — Current page structure confirmation

Before editing, inspect the current results page implementation and document the active section order.

Known likely files:

```text
frontend/app/(app)/results/page.tsx
frontend/app/components/**/*
frontend/app/lib/**/*
frontend/app/types/analysis.ts
backend/core/dto/**/*
```

Confirm where these current sections are rendered:

```text
Primary hero
Narrative retail summary
What's driving this
Wave1DomainCards
BalancedSystemsSummary
PipelineStatus / trust strip
What this means accordion
ResultsBodyOverview
ResultsInvestigationSpine
InterpretationPatternsSection
SystemUnderstandingSection
WhyThisLeadWonSection
NarrativeLeadAndSupportingSections
NarrativeLongitudinalAndNextSteps
PrimaryFindingAndWhy
Actions
Advanced & clinician report
BiomarkerDials
LayerCInsightSection
ClinicianReportRenderer
```

STOP if the current page structure cannot be safely established.

## Phase 2 — Target Phase 1 journey order

Implement the Phase 1 journey order from the v6 recommendation paper.

The target FE-R2 order is:

```text
1. Your body overview
2. What’s working well
3. Primary finding and why
4. Why this lead won / uncertainty
5. Marker-level evidence
6. What to do next
7. Clinician summary
```

FE-R2 must not implement the full Phase 2 pattern layer.

The existing `Patterns across your body` section may remain available, but it must not be promoted as a completed Phase 2 phenotype/pattern layer. If retained, label/position it cautiously as an early/current pattern view or keep it secondary.

## Required section behaviour

### Section 1 — Your body overview

Must appear at or near the top of the results page after the page header/disclosure banner.

Should include:

* short “how to read this page” framing block
* cleaned FE-R1 primary finding/overview content
* primary result context
* calm whole-body orientation
* no raw compiler/internal strings
* no biomarker grid

Use existing assets only, such as:

```text
clinician_report_v1.sections.page1.primary_concern
narrative_report_v1.body_overview
interpretation_display_layer_v1
consumer_domain_scores
balanced_systems_v1
```

Do not invent new backend fields.

### Section 2 — What’s working well

Must appear immediately after body overview.

Use:

```text
balanced_systems_v1
consumer_domain_scores fallback only if FE-R1 authorised/implemented it
```

If there are stable domains/systems, show them clearly.

If no stable systems are genuinely available, fallback copy must be calm and non-dismissive.

Do not fabricate reassurance.

### Section 3 — Primary finding and why

Must appear before uncertainty and before biomarker evidence.

Use:

```text
top_hypothesis_line if available
clinician_report_v1.sections.page1
root_cause_v1 / clinician_report_v1.sections.root_cause
chains[] if available
primary finding evidence
```

Important:

* `chains[]` must not be hidden only behind technical detail if it is consumer-readable.
* Technical ranking/debug wording must remain hidden.
* The heading must be retail-friendly.
* Do not use “Clinician-structured” in the retail flow.

### Section 4 — Why this lead won / uncertainty

Must appear immediately after primary finding and why.

Use:

```text
runner_up_topic_line
runner_up_why_not_lead_line
confidence_and_missing_data
data_quality.confidence_caveat
```

These should already be consumer-safe from FE-R1.

Do not expose numerical confidence scores or raw ranking values.

### Section 5 — Marker-level evidence

Move biomarker evidence into the retail journey.

This does not mean all advanced/clinician material becomes retail.

Minimum requirement:

* biomarker evidence must no longer be buried only under `Advanced & clinician report`
* user should be able to inspect biomarker values/ranges/status as part of the main journey
* existing display-unit fidelity must remain intact
* contribution/education expansions may remain basic in FE-R2; deeper work belongs to FE-R3

Use:

```text
BiomarkerDials
biomarkers[]
display_value/display_unit/display_label
reference ranges
```

Do not introduce frontend calculation logic.

Do not break FE-R1 prose safety.

### Section 6 — What to do next

Bring action/follow-up content into the main journey.

Use existing:

```text
narrative_report_v1.next_steps_narrative
confirmatory_tests[]
actions
next_steps[]
```

Actions may remain collapsible within this section, but the section itself should not be hidden behind an unrelated accordion.

Do not add generic wellness filler.

### Section 7 — Clinician summary

Keep clinician material separate and lower on the page.

Acceptable:

* collapsed by default
* clearly labelled as clinician/professional summary
* export/handoff oriented

Not acceptable:

* injecting clinician-heading language into the retail explanation flow
* making clinician report the main journey

## Phase 3 — Sections to demote, collapse, or remove from main flow

Review the following and decide whether to keep, move, collapse, or remove:

```text
Wave1DomainCards
ResultsInvestigationSpine
SystemUnderstandingSection
InterpretationPatternsSection
NarrativeLeadAndSupportingSections
NarrativeLongitudinalAndNextSteps
LayerCInsightSection
PipelineStatus
Advanced & clinician report
```

Rules:

* Do not delete valuable sections if they are needed for FE-R3/FE-R4.
* It is acceptable to demote them.
* It is acceptable to keep them collapsed.
* It is acceptable to move explanation/orientation content into Section 1.
* Avoid duplicate headings such as “What this means” inside “What this means”.
* Do not let the page remain accordion-dominated.

## Phase 4 — Frontend copy changes allowed

Frontend copy may be changed where needed to support the new journey.

Allowed:

* page subtitle
* section headings
* section descriptions
* accordion labels
* navigation helper text
* “Advanced” / clinician section labels

Forbidden:

* rewriting clinical interpretation content in frontend
* adding clinical claims in frontend static copy
* calculating or inferring clinical meaning in frontend
* adding new hardcoded medical explanations

## Phase 5 — Browser check

If browser tools are available, inspect:

```text
http://localhost:3000/results?analysis_id=7aacc734-95cf-4ea5-a19c-0d03d98dd2e9
```

Login if required:

```text
test-user3@example.com
Subaru@555
```

Check:

* the page opens with body overview / whole-body framing
* “What’s working well” appears near the top
* primary finding and why appears before uncertainty
* biomarker evidence is visible in the main journey
* actions/next steps are visible in the main journey
* clinician summary is separate
* internal strings from FE-R1 remain absent
* page does not feel like one giant accordion

Do not claim browser UAT passed unless the page was actually inspected.

## Required tests

Add or update deterministic tests for:

### Journey structure

* results page section order matches FE-R2 target order
* body overview appears before primary finding detail
* what’s working well appears before strain-heavy evidence
* uncertainty appears after primary finding
* biomarker evidence is part of main retail journey
* clinician summary remains separate/lower/collapsed

### Prose and safety preservation

* FE-R1 unsafe prose guards still pass
* no “Clinician-structured” heading appears in retail journey
* no duplicate “What this means” title collision
* no internal/governance/debug labels appear in visible section headings
* no frontend clinical inference added

### DTO/display preservation

* uploaded unit display fidelity remains intact
* biomarker dials still use display fields where available
* no frontend conversion maths introduced
* persisted replay fixture still supports required result surface fields

### Regression preservation

* FE-R1 consumer prose cleanup still passes
* LC-S13 lifestyle/coherence protections still pass
* LC-S14 direction-aware scoring still passes
* LC-S20/22 persisted replay protections still pass
* LC-S18A package estate protections still pass

## Required Sentinel / test harness obligations

Sentinel update is required.

Add or update defect classes such as:

```text
retail_results_journey_wrong_order
body_overview_not_first
working_well_section_missing_or_late
biomarker_evidence_hidden_in_advanced_only
clinician_language_in_retail_flow
results_page_accordion_dominated
duplicate_what_this_means_heading
```

Each must point to an active deterministic test or validator.

No placeholder Sentinel entries.

## Potentially allowed files

```text
frontend/app/(app)/results/page.tsx
frontend/app/components/**/*
frontend/app/lib/**/*
frontend/app/types/**/*
frontend/tests/**/*
backend/tests/regression/**/*
backend/tests/unit/**/*
sentinel/packs/**/*
docs/audit-papers/FE-R2_results_journey_restructure_notes.md
```

Backend runtime files are allowed only if absolutely necessary to expose already-existing DTO fields without changing clinical logic:

```text
backend/core/dto/**/*
```

## Forbidden unless GPT explicitly approves

```text
backend/core/analytics/**/*
backend/core/scoring/**/*
backend/core/units/**/*
backend/core/pipeline/**/*
backend/ssot/**/*
knowledge_bus/**/*
Gemini / LLM activation
broad frontend visual redesign unrelated to journey order
automation_bus/state/*
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
```

Do not modify backend narrative compilers in FE-R2.

If prose is still bad after FE-R1, document it as residual or STOP if it blocks the journey. Do not silently re-open FE-R1 inside FE-R2.

## Required validation commands

Run targeted tests and relevant guards.

At minimum:

```powershell
python -m pytest backend/tests/regression/test_fe_r1_consumer_prose_cleanup.py -q
python -m pytest backend/tests/regression/test_fe_r2_results_journey_restructure.py -q
python -m pytest backend/tests/regression/test_lc_s13_lifestyle_coherence_narrative.py -q
python -m pytest backend/tests/regression/test_lc_s14_direction_aware_scoring.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
python -m pytest backend/tests/regression/test_lc_s18a_package_estate_inventory.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

If frontend files changed:

```powershell
npm run type-check
```

If there are existing frontend tests suitable for this page, run them and record exact command/output.

Do not run broad unrelated suites unless targeted failures justify it.

## Acceptance criteria

This sprint is complete only if:

* FE-R1 is confirmed merged before FE-R2 starts
* results page is reorganised into the Phase 1 guided journey
* body overview appears first in the journey
* what’s working well appears near the top
* primary finding and why appears before uncertainty
* biomarker evidence is visible in the retail journey
* actions/next steps are visible in the retail journey
* clinician summary remains separate
* no broad frontend redesign is smuggled into the sprint
* no backend clinical/prose compiler changes are made
* FE-R1 prose safety guards still pass
* display-unit fidelity is preserved
* Sentinel guards are active and deterministic
* browser check is performed if available, or limitation is documented
* residual risks are recorded for FE-R3

## Closure requirements

Before finish, run:

```powershell
git branch --show-current
git status --short
git diff --name-only
git log --oneline -n 8
git stash list
```

Then run:

```powershell
python backend/scripts/run_work_package.py finish
```

After finish, follow SOP v1.3.1:

* if `automation_bus/latest_cursor_status.json` is the only dirty file and shows kernel-generated COMPLETE status for `FE-R2`, commit it automatically as:
  `chore(bus): FE-R2 kernel COMPLETE status`
* if any other Automation Bus artefact is dirty, STOP and escalate

Do not merge.

Do not claim FE-R3 readiness. This sprint prepares the page for FE-R3 but does not authorise it.

## Cursor completion statement

Cursor implements results journey restructuring only.

Cursor may not self-certify clinical correctness, final UX quality, merge readiness, or permission to begin FE-R3.

```
```
