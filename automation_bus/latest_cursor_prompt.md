---
work_id: FE-R1
branch: frontend/fe-r1-consumer-prose-cleanup
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# FE-R1 — Consumer Prose Cleanup and Narrative Safety

## Classification

This is a HIGH-risk MIXED sprint.

Reason: this sprint may touch backend narrative compilers, report compiler output, IDL/display labels, consumer-facing DTO prose, limited frontend rendering guards, regression tests, Sentinel packs, and audit documentation. It directly affects emitted user-facing interpretation.

This is not a page redesign sprint.  
This is not a frontend journey restructure sprint.  
This is not a Knowledge Bus expansion sprint.  
This is not a Gemini/LLM sprint.  
This is not a medication-overlay sprint.  
This is not a broad UX polish sprint.

## Purpose

Clean unsafe, incoherent, repetitive, or internal-facing prose from the current retail results page before any page restructuring begins.

The FE-R0 audit found that the current page does not match the intended guided reasoning journey and that multiple user-visible text blocks are raw compiler output, raw Knowledge Bus mechanism text, internal labels, repeated template strings, or numerical internal confidence values. :contentReference[oaicite:0]{index=0}

The goal of FE-R1 is to make the existing consumer-facing prose safe, readable, non-repetitive, and suitable for a retail user.

This sprint must fix source prose first. Do not simply hide problems in the frontend unless the correct disposition is explicitly “omit from UX”.

## Controlling authority

Read before doing anything:

```text
docs/audit-papers/FE_R0_results_page_prose_source_trace_audit.md
docs/frontend/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md
docs/architecture/HealthIQ_AI_runtime_architecture_map_v1.md
docs/developer-guides/healthiq_scaffold_guardrails_v1.md
docs/audit-papers/LC_SCAFFOLD_CLOSEOUT_transition_review.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
````

Also inspect if present:

```text
docs/audit-papers/LC-S16_knowledge_asset_frontend_surface_audit.md
docs/audit-papers/LC-S19_payload_contract_hardening_notes.md
docs/audit-papers/LC-S13_lifestyle_coherence_narrative_notes.md
docs/audit-papers/LC-S14_direction_aware_scoring_notes.md
docs/audit-papers/LC-S20_22_persisted_replay_sentinel_phase2_notes.md
```

If `docs/audit-papers/FE_R0_results_page_prose_source_trace_audit.md` is missing or untracked, STOP before kernel start. The FE-R0 audit must be committed to `main` before FE-R1 begins.

## Required output documentation

Create:

```text
docs/audit-papers/FE-R1_consumer_prose_cleanup_narrative_safety_notes.md
```

This document must include:

1. preflight results
2. FE-R0 audit findings addressed
3. exact source fields changed
4. exact frontend-visible prose before/after examples
5. which issues were fixed at backend/compiler source
6. which issues were omitted from UX
7. which issues were deferred
8. balanced systems investigation result
9. ALP critical-status investigation result
10. tests added/updated
11. Sentinel updates
12. residual risks
13. recommendation for FE-R2

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

* `work_id` is `FE-R1`
* branch is `frontend/fe-r1-consumer-prose-cleanup`

If token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

## Cross-sprint guard preflight

Run the current scaffold smoke pack before implementation.

At minimum:

```powershell
python -m pytest backend/tests/regression/test_lc_s8f_phase_b_true_conversions.py -q
python -m pytest backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py -q
python -m pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q
python -m pytest backend/tests/regression/test_lc_s10b_launch_core_protection.py -q
python -m pytest backend/tests/regression/test_lc_s11a_trust_blocker_correction.py -q
python -m pytest backend/tests/regression/test_lc_s13_lifestyle_coherence_narrative.py -q
python -m pytest backend/tests/regression/test_lc_s14_direction_aware_scoring.py -q
python -m pytest backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py -q
python -m pytest backend/tests/regression/test_lc_s18_root_cause_why_registration.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
python -m pytest backend/tests/regression/test_lc_s21_23_23b_orchestrator_docs_ssot.py -q
python -m pytest backend/tests/regression/test_lc_s18a_package_estate_inventory.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

If a prior guard fails, STOP unless GPT/human authority explicitly authorises continuation.

## Phase 1 — Source trace confirmation

Before editing, confirm the current source of each FE-R0 high-damage text block.

Trace at minimum:

```text
narrative_report_v1.retail_summary
narrative_report_v1.lead_narrative
narrative_report_v1.secondary_narratives
narrative_report_v1.next_steps_narrative
clinician_report_v1.sections.page1.runner_up_why_not_lead_line
clinician_report_v1.sections.page1.runner_up_topic_line
clinician_report_v1.sections.page1.confidence_and_missing_data
interpretation_display_layer_v1.records[].retail_display_label
balanced_systems_v1
ALP status / severity for ALP 38 U/L
```

Known actual files to inspect:

```text
backend/core/analytics/narrative_report_compiler_v1.py
backend/core/analytics/report_compiler_v1.py
backend/core/analytics/domain_narrative_wave1.py
backend/core/analytics/domain_score_assembler.py
backend/core/analytics/balanced_systems_presentation_v1.py
backend/core/analytics/interpretation_display_layer_governance_v1.py
backend/core/analytics/interpretation_display_layer_publish_v1.py
backend/core/scoring/**/*
backend/ssot/scoring_policy.yaml
backend/ssot/biomarkers.yaml
frontend/app/(app)/results/page.tsx
frontend/app/components/**/*
frontend/app/lib/**/*
frontend/app/types/analysis.ts
```

STOP if the source cannot be traced.

## Phase 2 — Consumer prose safety rules

Implement or enforce consumer prose safety rules.

Consumer-facing prose must not include:

```text
"(governed label)"
"moderate_by_default"
"confidence weight"
"structured ranking only"
"ranked lead pattern"
"lab anchor"
"thread"
"Functional read —"
"Prioritised follow-up (governed assets)"
"Clinician-structured"
"0.90"
"0.60"
"vs 0.90"
raw signal IDs such as "Lh High", "Alp Low", "Hypercortisolism"
template phrases like ": is outside the optimal range on this panel"
```

Do not remove clinically useful content merely because it is technical. The goal is compiler-mediated consumer copy, not dumbed-down generic prose.

## Phase 3 — Required fixes

### A. `narrative_report_v1.retail_summary`

Rewrite at source so the retail summary:

* does not describe compiler ranking mechanics
* does not say “The ranked lead pattern is…”
* does not use “lab anchor” or “thread”
* does not contain internal safety/meta commentary such as “This wording stays descriptive…”
* does not duplicate the IDL pattern-card why-it-matters text verbatim
* is concise enough for a summary card
* starts with a consumer-readable interpretation

Expected style:

```text
Your main result pattern is centred on raised homocysteine. This can point towards strain in one-carbon / methylation pathways, especially when interpreted alongside B-vitamin and blood-cell context. The wider panel also shows several stable areas, so this should be read as a focused follow-up pattern rather than a sign that the whole panel is off track.
```

Do not use that exact wording unless supported by the available data.

### B. `narrative_report_v1.lead_narrative`

Rewrite at source so the lead narrative:

* is compact
* is not a raw KB mechanism dump
* does not list all hypotheses with confidence weights
* does not expose governed labels
* does not expose internal ranking terms
* does not duplicate confirmatory tests already shown elsewhere
* uses 2–4 short paragraphs maximum
* explains the lead finding in consumer language

It may use mechanism/pathway content only after compiler-mediated summarisation.

### C. `narrative_report_v1.secondary_narratives`

Rewrite at source so secondary narratives:

* do not dump long raw lipid transport mechanism text
* do not list raw internal signal names
* do not repeat “is outside the optimal range…”
* do not include “Lh High on Lh”, “Alp Low on Alp”, etc.
* give a concise consumer explanation of relevant secondary context only

If secondary narrative content cannot be made safe, omit from retail UX and document why.

### D. `narrative_report_v1.next_steps_narrative`

Remove or rewrite internal headers:

```text
Prioritised follow-up (governed assets)
Functional read —
```

Keep useful follow-up actions, but present them in plain English.

### E. Runner-up and confidence prose

Rewrite at source in `backend/core/analytics/report_compiler_v1.py`:

```text
runner_up_why_not_lead_line
runner_up_topic_line
confidence_and_missing_data
```

These must not expose raw numerical confidence values such as `0.90 vs 0.90`.

Consumer-friendly confidence may say:

```text
Several findings were close in priority.
The panel has enough information to identify a lead pattern, but some confirmatory markers would make the interpretation more specific.
```

Use actual data-driven logic where available.

### F. IDL retail labels

Fix labels generated through the IDL governance/publish path:

```text
backend/core/analytics/interpretation_display_layer_governance_v1.py
backend/core/analytics/interpretation_display_layer_publish_v1.py
```

Fix labels such as:

```text
Homocysteine Elevation Context: is outside the optimal range on this panel
Homocysteine High: is outside the optimal range on this panel
```

Consumer labels must be concise and readable.

Example style:

```text
Raised homocysteine pattern
Homocysteine elevation
Methylation pathway pattern
```

Do not break internal IDs. This is display-label work only.

### G. Domain narrative duplication and contradictions

Inspect and update source where needed:

```text
backend/core/analytics/domain_narrative_wave1.py
backend/core/analytics/domain_score_assembler.py
```

Fix or document:

* repeated cardiovascular contributor sentence appearing in hero and domain card
* blood sugar card contradiction: `100 / 100`, `Strong`, `Limited confidence`, and “active signals to address”
* any internal signal/cluster labels appearing as consumer anchor text

### H. Duplicate suppression

Prevent the same prose block from appearing in multiple places.

At minimum, deduplicate:

* IDL pattern why-it-matters appearing in both summary and pattern card
* cardiovascular contributor sentence repeated in hero and domain card
* confirmatory tests repeated across lead narrative, next steps, and primary finding
* “is outside the optimal range…” template repetitions

Use source-level suppression where possible. Use frontend omission only where the text is duplicative by design.

### I. Balanced systems investigation

Investigate in:

```text
backend/core/analytics/balanced_systems_presentation_v1.py
```

Why `balanced_systems_v1` is empty for the audited analysis despite domain scores of 92, 100, and 94.

Outcome must be one of:

1. fix `balanced_systems_v1` compilation if it is clearly wrong
2. improve fallback copy if absence is valid
3. document as deferred if it requires wider scoring/system policy work

Do not fabricate stable-system claims.

### J. ALP critical investigation

Investigate why `ALP 38 U/L` rendered as `Critical`.

Known clue from hardening:

```text
ALP direction_class: high_only_concern in scoring_policy.yaml strongly suggests ALP 38 U/L being classified as Critical is a scoring/status error.
```

Outcome must be one of:

1. fix scoring/status classification if the current policy is wrong
2. document why the current classification is governed and correct
3. defer with explicit blocker if source cannot be safely changed

Do not silently alter scoring policy without test coverage.

## Phase 4 — Frontend display cleanup only where source cannot be fixed

Frontend changes are allowed only for:

* removing retail-hostile labels such as `Clinician-structured "why" and evidence`
* avoiding title collision where “What this means” appears twice
* omitting unsafe source fields if backend cannot make them safe in this sprint
* adding guards preventing internal tokens from rendering

Do not restructure the whole page in FE-R1. That belongs to FE-R2.

## Required tests

Add or update deterministic tests proving:

### Prose safety

* no user-facing retail prose contains internal labels
* no user-facing retail prose contains raw confidence weights
* no user-facing retail prose contains raw numerical ranking comparisons
* no consumer narrative contains `governed label`
* no consumer narrative contains `moderate_by_default`
* no consumer narrative contains `structured ranking only`
* no consumer narrative contains `Functional read —`
* no consumer narrative contains raw signal phrases like `Lh High`, `Alp Low`, `Hypercortisolism`
* no consumer display label contains `: is outside the optimal range on this panel`

### Narrative quality

* `retail_summary` is concise and does not duplicate pattern-card why-it-matters text
* `lead_narrative` is bounded in length and does not include raw hypothesis dumps
* `secondary_narratives` is bounded in length and excludes raw internal signal lists
* next steps omit internal governed-asset headers
* runner-up/confidence copy is consumer-safe

### Balanced systems / ALP

* balanced systems behaviour is covered according to the chosen outcome
* ALP status behaviour is covered according to the chosen outcome
* LC-S14 direction-aware scoring remains intact

### Regression preservation

* LC-S8F/G unit and display fidelity still passes
* LC-S13 lifestyle/coherence protections still pass
* LC-S14 direction-aware scoring protections still pass
* LC-S18 WHY registration protections still pass
* LC-S20/22 persisted replay protections still pass
* LC-S18A package estate protections still pass

## Required Sentinel / test harness obligations

Sentinel update is required.

Add or update defect classes such as:

```text
consumer_prose_internal_label_leakage
consumer_prose_raw_confidence_weight_visible
consumer_prose_raw_signal_id_visible
consumer_narrative_unbounded_mechanism_dump
consumer_summary_compiler_self_description
consumer_display_label_template_artifact
retail_page_duplicate_prose_block
balanced_systems_false_empty_state
alp_low_misclassified_critical
```

Each must point to an active deterministic test or validator.

No placeholder Sentinel entries.

## Potentially allowed files

```text
backend/core/analytics/narrative_report_compiler_v1.py
backend/core/analytics/report_compiler_v1.py
backend/core/analytics/domain_narrative_wave1.py
backend/core/analytics/domain_score_assembler.py
backend/core/analytics/balanced_systems_presentation_v1.py
backend/core/analytics/interpretation_display_layer_governance_v1.py
backend/core/analytics/interpretation_display_layer_publish_v1.py
backend/core/scoring/**/*
backend/ssot/scoring_policy.yaml
backend/ssot/biomarkers.yaml
frontend/app/(app)/results/page.tsx
frontend/app/components/**/*
frontend/app/lib/**/*
frontend/app/types/**/*
backend/tests/regression/**/*
backend/tests/unit/**/*
sentinel/packs/**/*
docs/audit-papers/FE-R1_consumer_prose_cleanup_narrative_safety_notes.md
```

## Forbidden unless GPT explicitly approves

```text
backend/core/units/**/*
backend/core/pipeline/**/*
knowledge_bus/packages/**/*   # no medical package content edits
knowledge_bus/governance/package_estate_KB-S49_v1.yaml
frontend redesign / broad page reorder
Gemini / LLM activation
automation_bus/state/*
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
```

Do not edit medical Knowledge Bus package content in FE-R1.

If medical package content appears to be the only source of the bad prose, STOP and report. The correct fix may be compiler mediation, not changing the package content.

## Required validation commands

Run targeted tests and relevant scaffold guards.

At minimum:

```powershell
python -m pytest backend/tests/regression/test_fe_r1_consumer_prose_cleanup.py -q
python -m pytest backend/tests/regression/test_lc_s13_lifestyle_coherence_narrative.py -q
python -m pytest backend/tests/regression/test_lc_s14_direction_aware_scoring.py -q
python -m pytest backend/tests/regression/test_lc_s18_root_cause_why_registration.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
python -m pytest backend/tests/regression/test_lc_s18a_package_estate_inventory.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

If frontend files changed:

```powershell
npm run type-check
```

If browser tools are available, inspect the same report after changes:

```text
http://localhost:3000/results?analysis_id=7aacc734-95cf-4ea5-a19c-0d03d98dd2e9
```

Confirm the 10 most damaging blocks from FE-R0 no longer appear in consumer-facing form.

Do not claim browser UAT passed unless the page was actually inspected.

## Acceptance criteria

This sprint is complete only if:

* FE-R0 audit report is committed to main before FE-R1 starts
* internal labels are removed from consumer-facing narrative fields
* raw confidence weights and score comparisons are removed from consumer-facing prose
* raw signal names and template artifacts are removed from display labels
* retail summary is consumer-readable and concise
* lead narrative is bounded and compiler-mediated
* secondary narratives no longer dump raw mechanism text or internal signal lists
* next steps no longer expose governed-asset/internal headers
* duplicate prose blocks are reduced or suppressed
* balanced systems absence is investigated and fixed or documented
* ALP critical status is investigated and fixed or documented
* Sentinel guards are active and deterministic
* no page restructuring is smuggled into this sprint
* no Knowledge Bus medical content is edited
* prior scaffold guards still pass

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

* if `automation_bus/latest_cursor_status.json` is the only dirty file and shows kernel-generated COMPLETE status for `FE-R1`, commit it automatically as:
  `chore(bus): FE-R1 kernel COMPLETE status`
* if any other Automation Bus artefact is dirty, STOP and escalate

Do not merge.

Do not claim FE-R2 readiness. This sprint prepares the page for FE-R2 but does not authorise it.

## Cursor completion statement

Cursor implements consumer prose safety only.

Cursor may not self-certify clinical correctness, frontend journey completion, merge readiness, or permission to begin FE-R2.

```
```
