---
work_id: FE-R6A
branch: frontend/fe-r6a-fresh-uat-defect-cleanup
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# FE-R6A — Fresh UAT Defect Cleanup and Evidence Surface Readiness

## Classification

This is a HIGH-risk MIXED sprint.

Reason: this sprint fixes defects found during fresh human UAT after FE-R1 through FE-R5A. It may touch frontend rendering, limited DTO field consumption, limited backend compiler/output sanitisation if required, tests, Sentinel packs and audit documentation.

This is not a broad redesign sprint.  
This is not KB-WAVE-1.  
This is not PATTERN-C1.  
This is not a Knowledge Bus expansion sprint.  
This is not a Gemini/LLM sprint.  
This is not a scoring/unit-governance sprint unless explicitly required for a documented display defect.

## Purpose

Resolve the remaining retail-surface defects that prevent the current results page from being commercially credible and ready to display future KB-WAVE intelligence.

The fresh UAT and Cursor cross-check both concluded:

- the page is materially better than FE-R0
- the guided journey broadly works
- FE-R5A pattern surfacing is safe
- but the page still feels prototype-like in key places
- KB-WAVE-1 should not start until the evidence surface is more reliable

The goal of FE-R6A is:

```text
Clean up the remaining fresh-UAT defects and prove the biomarker evidence surface is ready before adding new Knowledge Bus intelligence.
````

## Controlling authority

Read before doing anything:

```text
docs/audit-papers/FRESH_UAT_results_journey_quality_audit_f2dcb58f.md
docs/audit-papers/FRESH_UAT_cursor_crosscheck_f2dcb58f.md
docs/frontend/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md
docs/audit-papers/FE-R1_consumer_prose_cleanup_narrative_safety_notes.md
docs/audit-papers/FE-R2_results_journey_restructure_notes.md
docs/audit-papers/FE-R3_evidence_depth_ux_quality_pass_notes.md
docs/audit-papers/FE-R4_patterns_layer_gate_and_implementation_decision.md
docs/audit-papers/FE-R5A_limited_idl_pattern_surface_notes.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
```

If either fresh UAT report is missing, STOP.

## Required output documentation

Create:

```text
docs/audit-papers/FE-R6A_fresh_uat_defect_cleanup_notes.md
```

This document must include:

1. preflight results
2. FE-R1 through FE-R5A merge confirmation
3. fresh UAT defects addressed
4. fresh UAT defects deferred
5. exact files changed
6. before/after examples for visible text changes
7. biomarker expansion diagnosis
8. Homocysteine / Transferrin DTO-field diagnosis
9. whether fixes were frontend, DTO, compiler, or deferred content/asset work
10. tests added/updated
11. Sentinel updates
12. browser/manual UAT result if performed
13. residual risks
14. recommendation on whether KB-WAVE-1 can start next

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

* `work_id` is `FE-R6A`
* branch is `frontend/fe-r6a-fresh-uat-defect-cleanup`

If token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

## Merge precondition

Before implementation, confirm FE-R1, FE-R2, FE-R3, FE-R4 and FE-R5A are merged to `main`.

Evidence may include:

```text
test_fe_r1_consumer_prose_cleanup.py
test_fe_r2_results_journey_restructure.py
test_fe_r3_evidence_depth_ux_quality.py
test_fe_r5a_limited_idl_pattern_surface.py
FE-R1/2/3/4/5A audit notes
main ancestry commits
```

If these are not on main, STOP.

## Cross-sprint guard preflight

Run current FE/scaffold guards before implementation:

```powershell
python -m pytest backend/tests/regression/test_fe_r1_consumer_prose_cleanup.py -q
python -m pytest backend/tests/regression/test_fe_r2_results_journey_restructure.py -q
python -m pytest backend/tests/regression/test_fe_r3_evidence_depth_ux_quality.py -q
python -m pytest backend/tests/regression/test_fe_r5a_limited_idl_pattern_surface.py -q
python -m pytest backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

If a guard fails, STOP unless GPT/human explicitly authorises continuation.

## Target test page

Fresh UAT result:

```text
http://localhost:3000/results?analysis_id=f2dcb58f-e816-4ff6-9011-e93c5d48b82c
```

Login:

```text
test-user3@example.com
Subaru@555
```

Do not assume this persisted result will regenerate backend prose. Use it for rendering/UI verification. If a defect depends on newly generated analysis output, document that and test through deterministic fixtures instead.

---

# Required defect cleanup scope

## A. Remove/demote “How to read this page” wrapper

Problem:
The fresh UAT found that the hero/body overview are nested under an h2 labelled “How to read this page”, making the page feel like an instruction guide rather than a results journey.

Required outcome:

* “Your body overview” should be the first named journey section
* the “how to read this page” text should be demoted to a small framing note inside or near the body overview
* the hero should not appear as child content under an instructional heading
* do not remove useful orientation copy; reposition it correctly

## B. Remove duplicate Summary section

Problem:
The Summary section repeats the hero/body overview without adding value.

Required outcome:

* remove the standalone Summary section from the main retail journey
* do not remove the source field from backend unless required
* do not remove clinically important information unless already present elsewhere
* verify no duplicate homocysteine-centred summary appears in adjacent sections

## C. Fix or remove contradictory pattern counter

Problem:
The page shows “Needs attention: 0” while the same page presents a Strong Signal / homocysteine concern.

Required outcome:

Choose one safe approach:

1. fix the counter logic if it can be made consistent with the lead pattern, or
2. remove/hide the counter from retail view if it is not trustworthy, or
3. gate it behind technical detail if it is useful only internally

Do not show a counter that contradicts the lead finding.

## D. Hide technical confidence text in “What’s working well”

Problem:
Stable systems contain:

```text
interpretation confidence for this read: insufficient
```

Required outcome:

* do not show this phrase in retail view
* if needed, show only behind Show technical detail
* stable-system copy should remain reassuring but not overstate certainty

## E. Remove “Linked to …” internal labels

Problem:
Uploaded panel values show strings such as:

```text
Linked to hba1c
Linked to tc hdl ratio
```

Required outcome:

* remove these internal labels from retail-facing Uploaded panel values
* if equivalence needs to be shown, use consumer-friendly wording or omit
* do not break uploaded-panel fidelity or canonical-linked behaviour

## F. Fix “What to do next” rendering

Problems:

* bullets are rendered as a single text block
* “Suggested follow-up themes:” appears as a dangling label
* fallback text appears: “No separate checklist of follow-up lines was packaged...”
* MMA appears both in narrative bullets and confirmatory test section

Required outcome:

* render next steps as proper list items where possible
* suppress dangling headings
* remove raw fallback packaging text from retail view
* avoid obvious duplication between narrative bullets and confirmatory-test cards
* preserve clinically useful next-step content

## G. Replace raw technical scoring/unit error text

Problem:
Biomarker cards may show raw technical messages such as:

```text
Not scored - result unit and lab reference range unit cannot be aligned for this marker (incompatible units); check units on the report.
```

Required outcome:

* do not expose raw engineering/scoring errors in retail card text
* replace with consumer-safe wording such as “This result is shown for reference, but HealthIQ could not score it reliably because the units or reference range need review.”
* preserve technical detail somewhere only if appropriate and gated
* do not change actual scoring logic unless separately required and tested

## H. Align finding labels across hero and Primary finding section

Problem:
Hero says:

```text
Homocysteine Elevation Context
```

Primary finding says:

```text
B12-associated pattern
```

Required outcome:

* either align labels where they represent the same finding, or
* clarify relationship if one is the lead pattern and the other is a hypothesis
* do not misrepresent the hypothesis
* do not invent clinical labels in frontend

## I. Diagnose biomarker expansion richness gap

Problem:
Homocysteine and Transferrin show thin expansion content because DTO fields are absent or generic:

```text
Scored using lab reference range
```

Cursor cross-check found:

* Homocysteine: `contribution_context` absent from DTO
* Homocysteine: `biomarker_educational_explainer` absent from DTO
* Haemoglobin: richer expansion works when fields are supplied

Required outcome:

* diagnose whether the gap is frontend, DTO, compiler, SSOT, or content/asset coverage
* do not fabricate explanation in frontend
* if safe existing metadata can be surfaced without new medical logic, implement it
* if this requires new Knowledge Bus/SSOT content, document as deferred to KB-WAVE or a content sprint
* ensure generic `Scored using lab reference range` does not appear as the only expanded insight for a lead marker if avoidable
* if no richer content exists, show a consumer-safe limited-state message rather than method-only text

Do not turn FE-R6A into KB-WAVE-1.

---

# Potentially allowed files

```text
frontend/app/(app)/results/page.tsx
frontend/app/components/biomarkers/**/*
frontend/app/components/results/**/*
frontend/app/components/pipeline/**/*
frontend/app/lib/**/*
frontend/app/types/**/*
frontend/tests/**/*
backend/tests/regression/**/*
backend/tests/unit/**/*
sentinel/packs/**/*
docs/audit-papers/FE-R6A_fresh_uat_defect_cleanup_notes.md
```

Backend DTO files are allowed only if an already-existing field is present in backend data but not exposed to frontend type/DTO:

```text
backend/core/dto/**/*
```

Backend analytics files are allowed only for tightly scoped consumer-prose sanitisation or retail-display cleanup identified above:

```text
backend/core/analytics/narrative_report_compiler_v1.py
backend/core/analytics/report_compiler_v1.py
backend/core/analytics/balanced_systems_presentation_v1.py
backend/core/analytics/consumer_prose_safety_v1.py
```

## Forbidden unless GPT explicitly approves

```text
backend/core/scoring/**/*
backend/core/units/**/*
backend/core/pipeline/**/*
backend/ssot/**/*
knowledge_bus/**/*
Gemini / LLM activation
PATTERN-C1 backend/content contract work
KB-WAVE-1 content expansion
broad frontend visual redesign
automation_bus/state/*
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
```

Do not edit Knowledge Bus medical content.

If Homocysteine educational depth requires new medical content, STOP that part and document it as a deferred KB-WAVE/content issue.

---

# Required tests

Add or update deterministic tests for:

## Fresh UAT defect fixes

* “How to read this page” is not the parent h2 wrapping hero/body overview
* standalone duplicate Summary section is absent from the main retail journey
* pattern counter does not show `Needs attention: 0` when a lead Strong Signal / attention pattern is present
* “interpretation confidence for this read” does not appear in retail visible text
* “Linked to hba1c” / “Linked to tc hdl ratio” / raw `Linked to` labels do not appear in retail view
* next steps render as list items or clearly separated lines, not raw concatenated blob
* “No separate checklist of follow-up lines was packaged” does not appear in retail view
* raw `Not scored - result unit...` text does not appear in retail biomarker cards
* hero/primary-finding labels are aligned or relationship clarified

## Biomarker expansion readiness

* lead-marker expansion does not show only `Scored using lab reference range` as the sole insight
* if contribution_context is present, it renders
* if biomarker_educational_explainer is present, it renders
* if no richer content exists, limited-state text is consumer-safe
* no frontend clinical inference is introduced

## Regression preservation

* FE-R1 prose safety still passes
* FE-R2 journey order still passes
* FE-R3 evidence depth still passes or is updated to the corrected standard
* FE-R5A pattern surface still passes
* uploaded unit display fidelity still passes

## Required Sentinel obligations

Add or update defect classes such as:

```text
fresh_uat_instruction_wrapper_visible
fresh_uat_duplicate_summary_visible
fresh_uat_pattern_counter_contradiction
fresh_uat_interpretation_confidence_leak
fresh_uat_linked_to_internal_label_visible
fresh_uat_next_steps_rendering_artifact
fresh_uat_raw_scoring_error_visible
fresh_uat_thin_lead_marker_expansion
fresh_uat_finding_label_mismatch
```

Each must point to an active deterministic test.

No placeholder Sentinel entries.

---

# Required validation commands

Run:

```powershell
python -m pytest backend/tests/regression/test_fe_r1_consumer_prose_cleanup.py -q
python -m pytest backend/tests/regression/test_fe_r2_results_journey_restructure.py -q
python -m pytest backend/tests/regression/test_fe_r3_evidence_depth_ux_quality.py -q
python -m pytest backend/tests/regression/test_fe_r5a_limited_idl_pattern_surface.py -q
python -m pytest backend/tests/regression/test_fe_r6a_fresh_uat_defect_cleanup.py -q
python -m pytest backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

If frontend files changed:

```powershell
npm run type-check
```

If browser tools are available, inspect:

```text
http://localhost:3000/results?analysis_id=f2dcb58f-e816-4ff6-9011-e93c5d48b82c
```

Login:

```text
test-user3@example.com
Subaru@555
```

Do not claim browser UAT passed unless actually inspected.

---

# Acceptance criteria

This sprint is complete only if:

* FE-R1 through FE-R5A are confirmed merged before start
* all confirmed fresh UAT high-severity retail defects are fixed or explicitly deferred with rationale
* “How to read this page” no longer wraps the hero/body overview
* duplicate Summary section is removed from the main journey
* contradictory pattern counter is fixed, hidden, or gated
* internal labels and technical strings are removed from retail view
* What to do next renders cleanly
* biomarker expansion gap is diagnosed and improved or clearly classified as content/DTO backlog
* no new clinical reasoning is added in frontend
* no Knowledge Bus content is edited
* FE-R1/2/3/5A guards still pass
* Sentinel guards are active and deterministic
* browser/manual UAT is performed if available, or limitation documented
* recommendation on KB-WAVE-1 readiness is included

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

* if `automation_bus/latest_cursor_status.json` is the only dirty file and shows kernel-generated COMPLETE status for `FE-R6A`, commit it automatically as:
  `chore(bus): FE-R6A kernel COMPLETE status`
* if any other Automation Bus artefact is dirty, STOP and escalate

Do not merge.

Do not claim KB-WAVE-1 authorisation.

## Cursor completion statement

Cursor implements fresh UAT defect cleanup only.

Cursor may not self-certify commercial readiness, clinical correctness, KB-WAVE-1 readiness, merge readiness, or permission to begin the next sprint.

```
```
