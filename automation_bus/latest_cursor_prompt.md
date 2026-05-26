---
work_id: DOMAIN-UX1D
branch: domain-ux/domain-ux1d-full-wave1-expanded-card
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# DOMAIN-UX1D — Full Wave 1 Expanded Health Systems Card

## Classification

This is a STANDARD-risk frontend presentation sprint.

DOMAIN-UX1C has already created the backend-governed subsystem evidence model. This sprint renders that governed DTO output inside the Health Systems Card expanded reveal.

This sprint must not create new analytical logic.

Escalate to HIGH and STOP if implementation requires changes to:

- backend DTO models
- backend subsystem assembly
- scoring policy
- evidence completeness logic
- reliability/confidence logic
- marker-to-subsystem grouping
- Knowledge Bus
- IDL
- root-cause / narrative compilers
- pipeline behaviour

## Purpose

Render the full Wave 1 expanded Health Systems Card experience using the governed subsystem evidence created by DOMAIN-UX1C.

The user should be able to expand a Health Systems Card and see:

- which supporting subsystems contributed
- which markers were included for each subsystem
- which markers were missing
- the existing reliability and completeness context
- a visual evidence chain showing the score is evidence-built, not opinion-generated

## Controlling authority

Read before doing anything:

```text
docs/planning-papers/DOMAIN_UX_health_systems_card_scaffold_sprint_plan_FINAL.md
docs/discussion documents/healthiq_health_systems_card_discussion_FINAL.md
docs/audit-papers/DOMAIN-UX1B_premium_health_systems_card_visuals_notes.md
docs/audit-papers/DOMAIN-UX1C_governed_subsystem_evidence_model_notes.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
````

If the DOMAIN-UX1C notes file is missing, STOP.

## Required output documentation

Create:

```text
docs/audit-papers/DOMAIN-UX1D_full_wave1_expanded_health_systems_card_notes.md
```

This document must include:

1. preflight results
2. source documents reviewed
3. frontend components changed
4. subsystem rendering approach
5. included-marker rendering approach
6. missing-marker rendering approach
7. biomarker value implementation choice
8. zero-evidence behaviour
9. partial-evidence behaviour
10. tests added/updated
11. Sentinel updates
12. confirmation that no backend/governed logic changed
13. remaining gaps after DOMAIN-UX1D

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

* `work_id` is `DOMAIN-UX1D`
* branch is `domain-ux/domain-ux1d-full-wave1-expanded-card`

If token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

## Baseline verification

Before implementation, confirm:

* Wave 1 cards are visible in the main journey
* premium score visual exists for scored cards
* zero-evidence cards show `Not enough data`
* `Score reliability` label is visible
* `Evidence completeness` label is visible
* `ConsumerDomainScoreV1.subsystems` is typed in frontend
* backend-governed subsystem data is present in DTO/type contract
* frontend does not currently render visible subsystem sections

If any baseline assumption is false, STOP and report.

## Required implementation

### A. Mandatory subsystem sub-component isolation

Subsystem rendering must not be implemented inline inside:

```text
frontend/app/components/results/Wave1DomainCards.tsx
```

Reason:
Existing DOMAIN-UX1C guards assert that subsystem implementation details must not appear in `Wave1DomainCards.tsx`, including strings such as:

* `included_marker_ids`
* `Lipid transport`
* `wave1_cv_lipid_transport`

Required implementation pattern:

Create a dedicated presentational sub-component, for example:

```text
frontend/app/components/results/Wave1SubsystemEvidenceSection.tsx
```

or equivalent.

`Wave1DomainCards.tsx` may only:

* pass the backend-supplied `subsystems` array into the child component
* conditionally render the child component when `subsystems` exists
* avoid direct references to subsystem field names, subsystem IDs, subsystem labels, or marker grouping logic

All subsystem-specific rendering must live inside the dedicated child component.

Tests and Sentinel checks for subsystem rendering must target the new child component file, not `Wave1DomainCards.tsx`.

### B. Render subsystem sections in expanded card

In the expanded reveal of each Wave 1 Health Systems Card, render backend-supplied subsystem evidence.

Each subsystem section should show:

* subsystem label
* included markers
* missing markers
* source trace only if consumer-safe
* no status unless backend supplies a non-null supported status

Do not render subsystem status if `status_label` is null.

Do not invent subsystem labels.

Do not invent subsystem marker groupings.

### C. Biomarker value implementation choice — use Option B

For DOMAIN-UX1D, use marker names only.

Do not thread full `BiomarkerResult[]` into the card in this sprint.

Use the existing approved display-name utility, such as:

```text
wave1ConfidenceMarkerDisplayLabel
```

or the current equivalent marker display-name helper.

Render:

* included marker names
* missing marker names
* missing markers as `Not uploaded`

Do not show biomarker values, units, ranges, scores or statuses in DOMAIN-UX1D.

Document in the audit notes that value/unit/range/status display is deliberately deferred to a later sprint once the compact biomarker evidence component is designed.

### D. Render included markers

For each subsystem, show included marker names from backend-supplied `included_marker_ids`.

The frontend may convert canonical marker IDs into display names using the approved display-name helper.

The frontend must not:

* determine which markers are included
* move markers between subsystems
* invent values, ranges, scores, statuses or interpretations

### E. Render missing markers

For each subsystem, show missing marker names from backend-supplied `missing_marker_ids`.

Missing markers should be visually muted or greyed out and labelled:

```text
Not uploaded
```

Missing markers should feel informative, not punitive.

The frontend must not calculate missing marker lists.

### F. Preserve zero-evidence behaviour

For zero-evidence domain cards:

* keep the collapsed card as `Not enough data`
* expanded reveal may show what marker evidence would be needed
* do not show score ring
* do not show `Needs attention`
* do not imply the domain is unhealthy

### G. Preserve partial-evidence behaviour

For partial-evidence domain cards:

* keep the score visible
* keep limited-coverage treatment visible
* show which subsystem/marker evidence was available
* show what was missing

### H. No backend changes

This sprint should be frontend-only.

Do not modify backend DTOs or backend assembly.

If frontend cannot render the intended experience because required data is missing, STOP and report the missing field.

### I. No Wave 2 domains

Only render subsystem evidence for the existing Wave 1 domain cards.

Do not add or surface Wave 2 cards.

## Explicitly forbidden

Do not modify:

```text
backend/ssot/**/*
backend/core/scoring/**/*
backend/core/pipeline/**/*
backend/core/units/**/*
backend/core/analytics/**/*
backend/core/models/results.py
knowledge_bus/**/*
frontend clinician report components
automation_bus/state/*
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
```

Do not introduce:

* new clinical claims
* new score logic
* new reliability logic
* frontend-calculated evidence completeness
* frontend-calculated missing markers
* frontend-defined subsystem labels
* frontend-defined marker-to-subsystem groupings
* fake subsystem status
* fake subsystem score
* biomarker values/ranges/statuses not already passed into the subsystem component
* Wave 2 domain cards

## Potentially allowed files

```text
frontend/app/components/results/Wave1DomainCards.tsx
frontend/app/components/results/Wave1HealthSystemScoreVisual.tsx
frontend/app/components/results/Wave1SubsystemEvidenceSection.tsx
frontend/app/components/results/**/*
frontend/app/lib/wave1HealthSystemCardDisplay.ts
frontend/app/types/analysis.ts
frontend/tests/components/Wave1DomainCards.test.tsx
frontend/tests/components/Wave1SubsystemEvidenceSection.test.tsx
backend/tests/regression/test_domain_ux1a_wave1_health_systems_card_scaffold.py
backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py
sentinel/packs/escaped_defects_v1.json
docs/audit-papers/DOMAIN-UX1D_full_wave1_expanded_health_systems_card_notes.md
```

If a new frontend component is created, keep it under:

```text
frontend/app/components/results/
```

## Required tests

Add or update deterministic tests proving:

### Sub-component isolation

* subsystem rendering lives in a dedicated child component
* `Wave1DomainCards.tsx` does not contain direct subsystem field references such as:

  * `included_marker_ids`
  * `missing_marker_ids`
  * concrete subsystem labels
  * concrete subsystem IDs
* `Wave1DomainCards.tsx` only passes `subsystems` into the child component

### Subsystem rendering

* expanded card renders subsystem sections when `subsystems` are supplied
* subsystem labels come from DTO
* subsystem IDs come from DTO
* frontend does not define subsystem labels
* frontend does not define subsystem marker mappings

### Included markers

* included marker IDs render under the correct subsystem
* included marker display uses display names only in this sprint
* frontend does not invent biomarker values, ranges, scores or statuses

### Missing markers

* missing marker IDs render under the correct subsystem
* missing markers are visually muted/greyed out
* missing markers show `Not uploaded`
* frontend does not calculate missing marker lists

### Zero-evidence preservation

* zero-evidence cards still show `Not enough data`
* zero-evidence cards do not show score ring
* zero-evidence cards do not show `Needs attention`

### Guard preservation

* score reliability label remains visible
* evidence completeness label remains visible
* no clinical label appears in consumer card
* no raw signal IDs appear
* no internal/compiler/model language appears

## Required Sentinel obligations

Add or update active deterministic Sentinel defect classes as appropriate:

```text
health_system_subsystem_sections_not_rendered
health_system_subsystem_labels_frontend_defined
health_system_included_markers_not_rendered
health_system_missing_markers_not_rendered
health_system_subsystem_fake_status_visible
health_system_subsystem_rendering_not_isolated
health_system_subsystem_marker_values_invented
```

Each Sentinel class must point to an active deterministic test.

No placeholder Sentinel entries.

## Required validation commands

Run:

```powershell
python -m pytest backend/tests/regression/test_domain_ux1a_wave1_health_systems_card_scaffold.py -q
python -m pytest backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py -q
python -m pytest backend/tests/regression/test_fe_r1_consumer_prose_cleanup.py -q
python -m pytest backend/tests/regression/test_fe_r6a_fresh_uat_defect_cleanup.py -q
python -m pytest backend/tests/regression/test_canonical_mapping_star_suffix_failure.py -q
python -m pytest backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
python -m pytest backend/tests/unit/test_domain_score_assembler_v1.py -q
```

Run frontend validation:

```powershell
npm run type-check
```

If frontend component tests exist, run them.

If browser tools are available, inspect:

```text
http://localhost:3000/results?analysis_id=d7417288-7e11-48da-8716-d0f63f77c491
```

Confirm:

* expanded cards show subsystem sections
* included marker names appear under subsystem sections
* missing marker names appear as `Not uploaded`
* no biomarker values/units/ranges/statuses are shown inside subsystem marker lists in this sprint
* zero-evidence cards still show insufficient-data state
* no unsupported subsystem scores/statuses appear
* no Wave 2 cards appear

Do not claim browser UAT passed unless actually inspected.

## Acceptance criteria

This sprint is complete only if:

* expanded Wave 1 cards render governed subsystem sections
* subsystem rendering is isolated in a dedicated child component
* included and missing marker names are shown per subsystem
* subsystem labels and marker groupings come only from DTO
* frontend does not define biological subsystem logic
* frontend does not invent biomarker values/ranges/statuses
* zero-evidence and partial-evidence states remain correct
* no subsystem score/status is shown unless backend supplies it
* no backend/governed logic is changed
* no Wave 2 domains are surfaced
* tests pass
* Sentinel guards are active
* notes document that biomarker value/unit/range/status display is deferred

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

* if `automation_bus/latest_cursor_status.json` is the only dirty file and shows kernel-generated COMPLETE status for `DOMAIN-UX1D`, commit it automatically as:
  `chore(bus): DOMAIN-UX1D kernel COMPLETE status`
* if any other Automation Bus artefact is dirty, STOP and escalate

Do not merge.

Do not start the next sprint.

## Cursor completion statement

Cursor implements DOMAIN-UX1D only.

Cursor may not self-certify merge readiness, clinical correctness, or permission to begin the next sprint.

```
```
