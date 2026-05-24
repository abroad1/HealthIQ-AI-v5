---
work_id: FE-R3
branch: frontend/fe-r3-evidence-depth-ux-quality-pass
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# FE-R3 — Evidence Depth and UX Quality Pass

## Classification

This is a HIGH-risk MIXED sprint.

Reason: this sprint changes the consumer-facing results experience by improving biomarker evidence depth, contribution-context surfacing, educational expansion, next-step clarity, duplicate suppression and page quality. It may touch frontend rendering, DTO field consumption, limited backend DTO exposure if required, regression tests, Sentinel packs and audit documentation.

This is not a backend clinical reasoning sprint.  
This is not a Knowledge Bus expansion sprint.  
This is not a Gemini/LLM sprint.  
This is not a scoring/unit-governance sprint.  
This is not a medication-overlay sprint.  
This is not the Phase 2 patterns-layer sprint.  
This is not a broad visual redesign sprint.

## Purpose

Make the newly restructured FE-R2 results journey feel richer, clearer and more useful to a human user.

FE-R1 made consumer prose safer.  
FE-R2 put the results page into the Phase 1 guided journey order.  
FE-R3 must now improve the depth and quality of the evidence layer without changing clinical logic.

The main goal is:

```text
When a user reads the page or opens a biomarker, they should understand not only the value, but why the marker matters and how it connects to the wider finding.
````

## Controlling authority

Read before doing anything:

```text
docs/frontend/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md
docs/audit-papers/FE_R0_results_page_prose_source_trace_audit.md
docs/audit-papers/FE-R1_consumer_prose_cleanup_narrative_safety_notes.md
docs/audit-papers/FE-R2_results_journey_restructure_notes.md
docs/architecture/HealthIQ_AI_runtime_architecture_map_v1.md
docs/developer-guides/healthiq_scaffold_guardrails_v1.md
docs/audit-papers/LC_SCAFFOLD_CLOSEOUT_transition_review.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
```

Also inspect if present:

```text
docs/audit-papers/LC-S16_knowledge_asset_frontend_surface_audit.md
docs/audit-papers/LC-S19_payload_contract_hardening_notes.md
docs/audit-papers/LC-S20_22_persisted_replay_sentinel_phase2_notes.md
```

If FE-R1 notes, FE-R2 notes, or the v6 recommendation paper are missing, STOP.

## FE-R2 merge precondition

Before implementation, confirm FE-R2 is merged to `main`.

Evidence may include:

* FE-R2 merge commit on main ancestry
* `test_fe_r2_results_journey_restructure.py` exists and passes
* FE-R2 notes exist
* FE-R2 Sentinel classes exist
* page structure contains the seven FE-R2 journey sections

If FE-R2 is not on main, STOP.

## Required output documentation

Create:

```text
docs/audit-papers/FE-R3_evidence_depth_ux_quality_pass_notes.md
```

This document must include:

1. preflight results
2. FE-R2 merge confirmation
3. current FE-R2 page-quality baseline
4. biomarker expansion changes
5. contribution-context surfacing changes
6. educational explainer surfacing changes
7. next-step/action quality changes
8. duplicate suppression changes
9. frontend files changed
10. DTO/API fields consumed or exposed
11. browser/manual UAT evidence if performed
12. tests added/updated
13. Sentinel updates
14. residual risks
15. recommendation for FE-R4

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

* `work_id` is `FE-R3`
* branch is `frontend/fe-r3-evidence-depth-ux-quality-pass`

If token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

## Cross-sprint guard preflight

Run current FE/scaffold guards before implementation.

At minimum:

```powershell
python -m pytest backend/tests/regression/test_fe_r1_consumer_prose_cleanup.py -q
python -m pytest backend/tests/regression/test_fe_r2_results_journey_restructure.py -q
python -m pytest backend/tests/regression/test_lc_s13_lifestyle_coherence_narrative.py -q
python -m pytest backend/tests/regression/test_lc_s14_direction_aware_scoring.py -q
python -m pytest backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
python -m pytest backend/tests/regression/test_lc_s18a_package_estate_inventory.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

If a prior guard fails, STOP unless GPT/human authority explicitly authorises continuation.

## Phase 1 — Current FE-R2 quality baseline

Inspect the current FE-R2 results page structure and identify where the following are currently rendered:

```text
biomarker values
reference ranges
display units and uploaded-unit fidelity
biomarker status
biomarker short interpretation
contribution_context
biomarker_educational_explainer
confirmatory_tests[]
actions
next_steps[]
narrative_report_v1.next_steps_narrative
Layer C / body insight features if already rendered
```

Known likely files:

```text
frontend/app/(app)/results/page.tsx
frontend/app/components/biomarkers/**/*
frontend/app/components/results/**/*
frontend/app/lib/**/*
frontend/app/types/analysis.ts
backend/core/dto/**/*
```

STOP if the current source of biomarker expansion or action content cannot be established.

## Phase 2 — Biomarker expansion depth

Implement the v6 paper’s biomarker expansion rule where existing data supports it.

Each expanded biomarker card should, where available, present:

```text
1. What this result means now
2. Why this marker matters
3. How it connects to the wider pattern
```

Use existing fields only:

```text
biomarkers[]
display_value
display_unit
display_label
reference_range
status
interpretation
contribution_context
biomarker_educational_explainer
clusters[] / primary finding context where already available
```

Required behaviour:

* value/range/status remain visible
* uploaded unit display fidelity remains intact
* explanation is conditional on available governed fields
* missing deeper content is omitted cleanly
* no frontend clinical inference is added
* no frontend conversion maths is added

Do not fabricate educational content.

## Phase 3 — Contribution context and pattern relevance

Surface `contribution_context` more clearly where present.

Acceptable wording pattern:

```text
How this fits the wider pattern
[contribution_context.factual_statement]
```

If a biomarker can be safely linked to the primary finding or current pattern using existing DTO/cluster membership, show a short pattern relevance line.

Rules:

* no new backend clinical reasoning
* no hardcoded medical claims in frontend
* no invented pattern names
* no raw internal signal IDs
* if the link is not clear, omit the pattern relevance line

## Phase 4 — Educational explainer surfacing

Where `biomarker_educational_explainer` exists, surface it in the biomarker expansion.

The explainer should be:

* clearly separated from this-user interpretation
* labelled as general marker education
* not presented as a personalised diagnosis
* not duplicated elsewhere on the same card
* collapsed or compact enough to avoid overwhelming the user

If the explainer is absent, do not show placeholder text.

## Phase 5 — Action / next-step quality

Improve the “What to do next” section using existing assets.

Use:

```text
confirmatory_tests[]
actions
next_steps[]
narrative_report_v1.next_steps_narrative
safety_class if available
```

Required behaviour:

* confirmatory tests should show rationale where available
* actions should be grouped or prioritised if existing fields support it
* duplicate next steps should be suppressed
* internal labels must not appear
* generic wellness filler must not be added
* clinician-facing recommendations should remain appropriately cautious

Do not create new clinical action logic.

## Phase 6 — Duplicate and density reduction

Reduce obvious duplicated content created by FE-R1/FE-R2 surfacing.

At minimum inspect for duplication between:

```text
retail summary
body overview
primary finding
pattern card
next steps
confirmatory tests
biomarker expansion
clinician summary
```

Allowed:

* suppress duplicate display in one place
* collapse repeated content
* shorten frontend framing copy
* avoid showing the same rationale twice in one section

Forbidden:

* changing backend clinical content to force deduplication unless explicitly required
* hiding clinically important warnings without an alternative visible location

## Phase 7 — Optional browser/manual check

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

* biomarker evidence is easy to find
* expanded biomarker card shows richer content where available
* contribution context is visible where present
* education text is useful but not overwhelming
* next steps feel specific rather than generic
* no FE-R1 internal prose leaks return
* no duplicate text blocks dominate the page

Do not claim browser UAT passed unless the page was actually inspected.

## Required tests

Add or update deterministic tests for:

### Biomarker evidence depth

* biomarker evidence remains in the main retail journey
* biomarker expansion includes value/range/status
* contribution_context is surfaced where available
* biomarker_educational_explainer is surfaced where available
* missing educational content omits cleanly without placeholder text
* display_value/display_unit/display_label are still used correctly
* no frontend unit conversion maths is introduced

### Action layer quality

* confirmatory_tests rationale is renderable where available
* action/next-step section does not expose internal labels
* duplicate next-step lines are suppressed or prevented
* generic placeholder follow-up text is not shown when governed actions exist

### Prose and journey preservation

* FE-R1 unsafe prose guards still pass
* FE-R2 journey order still passes
* no raw signal/internal IDs appear in biomarker/action sections
* clinician summary remains separate
* no Phase 2 pattern-layer claims are introduced

### Regression preservation

* LC-S13 lifestyle/coherence protections still pass
* LC-S14 direction-aware scoring still passes
* LC-S20/22 persisted replay protections still pass
* LC-S18A package estate protections still pass

## Required Sentinel / test harness obligations

Sentinel update is required.

Add or update defect classes such as:

```text
biomarker_contribution_context_not_surfaced
biomarker_educational_explainer_not_surfaced
biomarker_expansion_placeholder_visible
biomarker_display_unit_regression
action_rationale_missing_when_available
next_steps_duplicate_visible
frontend_clinical_inference_added
fe_r2_journey_order_regressed
```

Each must point to an active deterministic test or validator.

No placeholder Sentinel entries.

## Potentially allowed files

```text
frontend/app/(app)/results/page.tsx
frontend/app/components/biomarkers/**/*
frontend/app/components/results/**/*
frontend/app/lib/**/*
frontend/app/types/**/*
frontend/tests/**/*
backend/tests/regression/**/*
backend/tests/unit/**/*
sentinel/packs/**/*
docs/audit-papers/FE-R3_evidence_depth_ux_quality_pass_notes.md
```

Backend DTO files are allowed only if an already-existing field is present in backend data but not exposed to the frontend type/DTO:

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
Phase 2 patterns-layer implementation
frontend visual redesign unrelated to evidence depth
automation_bus/state/*
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
```

Do not modify backend narrative compilers in FE-R3.

If the remaining issue is still bad source prose, document it as a residual or STOP if it blocks quality. Do not silently re-open FE-R1 inside FE-R3.

## Required validation commands

Run targeted tests and relevant guards.

At minimum:

```powershell
python -m pytest backend/tests/regression/test_fe_r1_consumer_prose_cleanup.py -q
python -m pytest backend/tests/regression/test_fe_r2_results_journey_restructure.py -q
python -m pytest backend/tests/regression/test_fe_r3_evidence_depth_ux_quality.py -q
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

* FE-R2 is confirmed merged before FE-R3 starts
* biomarker evidence remains in the main retail journey
* biomarker expansion is richer where governed fields exist
* contribution_context is surfaced where available
* biomarker_educational_explainer is surfaced where available
* missing deeper fields omit cleanly
* uploaded unit display fidelity is preserved
* action/next-step section is clearer and less duplicative
* no frontend clinical inference is introduced
* no backend analytical/prose compiler changes are made
* FE-R1 prose safety guards still pass
* FE-R2 journey order guards still pass
* Sentinel guards are active and deterministic
* browser/manual check is performed if available, or limitation is documented
* residual risks are recorded for FE-R4

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

* if `automation_bus/latest_cursor_status.json` is the only dirty file and shows kernel-generated COMPLETE status for `FE-R3`, commit it automatically as:
  `chore(bus): FE-R3 kernel COMPLETE status`
* if any other Automation Bus artefact is dirty, STOP and escalate

Do not merge.

Do not claim FE-R4 readiness. This sprint prepares the page for FE-R4 but does not authorise it.

## Cursor completion statement

Cursor implements evidence depth and UX quality improvements only.

Cursor may not self-certify clinical correctness, final UX quality, merge readiness, or permission to begin FE-R4.

```
```
