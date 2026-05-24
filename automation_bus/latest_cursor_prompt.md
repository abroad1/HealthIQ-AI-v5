---
work_id: FE-R5A
branch: frontend/fe-r5a-limited-idl-pattern-surface
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# FE-R5A — Limited IDL Pattern Surface

## Classification

This is a HIGH-risk MIXED sprint.

Reason: this sprint changes the consumer-facing results journey by surfacing governed pattern cards in the main retail flow. It may touch frontend rendering, DTO field consumption, regression tests, Sentinel packs and audit documentation.

This is not the full pattern/phenotype contract sprint.  
This is not a Knowledge Bus expansion sprint.  
This is not a backend pattern-contract sprint.  
This is not a scoring/unit-governance sprint.  
This is not a Gemini/LLM sprint.  
This is not a broad frontend redesign sprint.

## Purpose

Move the existing governed IDL pattern card surface into the main retail journey as a limited “Patterns across your body” section.

The FE-R4 gate concluded:

- GO WITH CONDITIONS
- IDL-only pattern surfacing is viable now
- clusters[] must not be used as consumer pattern names
- full phenotype/pattern implementation requires PATTERN-C1 later

FE-R5A must implement only the safe limited surface.

## Controlling authority

Read before doing anything:

```text
docs/audit-papers/FE-R4_patterns_layer_gate_and_implementation_decision.md
docs/frontend/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md
docs/audit-papers/FE_R0_results_page_prose_source_trace_audit.md
docs/audit-papers/FE-R1_consumer_prose_cleanup_narrative_safety_notes.md
docs/audit-papers/FE-R2_results_journey_restructure_notes.md
docs/audit-papers/FE-R3_evidence_depth_ux_quality_pass_notes.md
docs/architecture/HealthIQ_AI_runtime_architecture_map_v1.md
docs/developer-guides/healthiq_scaffold_guardrails_v1.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
````

If the FE-R4 gate document is missing, STOP.

## Required output documentation

Create:

```text
docs/audit-papers/FE-R5A_limited_idl_pattern_surface_notes.md
```

This document must include:

1. preflight results
2. FE-R4 merge confirmation
3. IDL fields used
4. IDL fields deliberately not used
5. sections/components changed
6. current retail journey position
7. safeguards against raw cluster/internal labels
8. classification/taxonomy display decision
9. fallback behaviour
10. tests added/updated
11. Sentinel updates
12. residual risks
13. recommendation for PATTERN-C1 or next frontend sprint

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

* `work_id` is `FE-R5A`
* branch is `frontend/fe-r5a-limited-idl-pattern-surface`

If token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

## Merge precondition

Before implementation, confirm FE-R4 is merged to `main`.

Evidence may include:

```text
docs/audit-papers/FE-R4_patterns_layer_gate_and_implementation_decision.md
test_fe_r1_consumer_prose_cleanup.py
test_fe_r2_results_journey_restructure.py
test_fe_r3_evidence_depth_ux_quality.py
main ancestry commits
```

If FE-R4 is not on main, STOP.

## Cross-sprint guard preflight

Run current FE/scaffold guards before implementation:

```powershell
python -m pytest backend/tests/regression/test_fe_r1_consumer_prose_cleanup.py -q
python -m pytest backend/tests/regression/test_fe_r2_results_journey_restructure.py -q
python -m pytest backend/tests/regression/test_fe_r3_evidence_depth_ux_quality.py -q
python -m pytest backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
```

If a guard fails, STOP unless GPT/human explicitly authorises continuation.

## Implementation scope

Implement a limited retail journey section:

```text
Patterns across your body
```

It must use only governed IDL fields from:

```text
interpretation_display_layer_v1.records[]
```

Allowed IDL-style fields may include existing equivalents of:

```text
retail_display_label
subtitle
why_it_matters
supporting_markers
severity/status
scientific_class / frontend_allowed_term if already consumer-safe
```

Do not invent missing fields.

## Placement

Add the limited patterns section into the main FE-R2/FE-R3 journey after:

```text
Why this lead won / uncertainty
```

and before:

```text
Marker-level evidence
```

This creates the intended bridge:

```text
body overview
what’s working well
primary finding and why
uncertainty
patterns across your body
marker-level evidence
what to do next
clinician summary
```

## Required safeguards

FE-R5A must not:

* use `clusters[].name` as consumer pattern names
* use raw signal labels
* use raw internal IDs
* use `Functional read — ...` labels
* use labels such as `Cardiovascular 4 Biomarkers`
* imply a full phenotype layer exists
* introduce a broad pattern taxonomy UI unless already safely supported
* edit Knowledge Bus content
* edit backend analytics contracts
* create new clinical interpretation logic

If the only available pattern data is unsafe, do not render the section.

## Classification/taxonomy handling

If `scientific_class` or equivalent is available and consumer-safe, it may be displayed as a restrained chip only if it helps clarity.

If not safe or not consistently present, hide it.

Do not expose internal taxonomy labels unless FE-R4 explicitly identified them as safe.

## Fallback behaviour

If no safe IDL records exist:

* omit the section cleanly
* do not show placeholder text such as “No patterns found”
* do not fall back to clusters[] names
* document the absence in FE-R5A notes

## Frontend copy rules

Allowed copy:

* neutral section heading
* short explanation that patterns summarise related marker evidence
* short caution that this is not a diagnosis

Forbidden copy:

* new clinical claims
* invented phenotype labels
* technical/internal taxonomy explanation
* “debug”, “governed”, “IDL”, “cluster”, “signal” language

## Likely files

Inspect and modify only as needed:

```text
frontend/app/(app)/results/page.tsx
frontend/app/components/results/**/*
frontend/app/lib/**/*
frontend/app/types/analysis.ts
backend/tests/regression/**/*
frontend/tests/**/*
sentinel/packs/**/*
docs/audit-papers/FE-R5A_limited_idl_pattern_surface_notes.md
```

## Forbidden unless GPT explicitly approves

```text
backend/core/analytics/**/*
backend/core/scoring/**/*
backend/core/units/**/*
backend/core/pipeline/**/*
backend/core/dto/**/*
backend/ssot/**/*
knowledge_bus/**/*
Gemini / LLM activation
PATTERN-C1 backend/content contract work
automation_bus/state/*
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
```

No backend runtime files should be changed in FE-R5A.

If backend/DTO change appears necessary, STOP and recommend PATTERN-C1.

## Required tests

Add or update deterministic tests for:

* limited IDL pattern section appears in the intended journey position
* pattern section appears after uncertainty and before marker-level evidence
* section renders only from IDL fields
* clusters[] names are not used as consumer pattern labels
* raw/internal pattern names do not appear
* supporting markers render only when supplied by IDL-safe fields
* section omits cleanly when no safe IDL records exist
* FE-R1 prose safety still passes
* FE-R2 journey order still passes
* FE-R3 evidence-depth guards still pass
* biomarker evidence remains in main journey
* clinician summary remains separate

## Required Sentinel obligations

Add/update Sentinel defect classes such as:

```text
patterns_section_missing_when_idl_safe
patterns_section_wrong_journey_position
raw_cluster_name_used_as_pattern_label
unsafe_pattern_taxonomy_visible
patterns_section_placeholder_visible
fe_r3_marker_evidence_regressed
```

Each must point to an active deterministic test.

No placeholder Sentinel entries.

## Required validation commands

Run:

```powershell
python -m pytest backend/tests/regression/test_fe_r1_consumer_prose_cleanup.py -q
python -m pytest backend/tests/regression/test_fe_r2_results_journey_restructure.py -q
python -m pytest backend/tests/regression/test_fe_r3_evidence_depth_ux_quality.py -q
python -m pytest backend/tests/regression/test_fe_r5a_limited_idl_pattern_surface.py -q
python -m pytest backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
```

If frontend files changed:

```powershell
npm run type-check
```

If browser tools are available, inspect:

```text
http://localhost:3000/results?analysis_id=7aacc734-95cf-4ea5-a19c-0d03d98dd2e9
```

Do not claim browser UAT passed unless actually inspected.

## Acceptance criteria

Complete only if:

* FE-R4 is confirmed merged before start
* limited IDL-only pattern section is surfaced in the main journey
* section uses IDL fields only
* clusters[] labels are not used as consumer pattern names
* section appears after uncertainty and before marker-level evidence
* fallback omission is clean when no safe IDL records exist
* no backend runtime/DTO/Knowledge Bus files are changed
* FE-R1/2/3 guards still pass
* Sentinel guards are active and deterministic
* residual risks for PATTERN-C1 are documented

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

* if `automation_bus/latest_cursor_status.json` is the only dirty file and shows kernel-generated COMPLETE status for `FE-R5A`, commit it automatically as:
  `chore(bus): FE-R5A kernel COMPLETE status`
* if any other Automation Bus artefact is dirty, STOP and escalate

Do not merge.

Do not claim PATTERN-C1 authorisation.

## Cursor completion statement

Cursor implements limited IDL pattern surfacing only.

Cursor may not self-certify final pattern-layer readiness, clinical correctness, merge readiness, or permission to begin PATTERN-C1.

```
```
