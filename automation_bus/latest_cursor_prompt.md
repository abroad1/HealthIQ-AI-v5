---
work_id: DOMAIN-UX1B
branch: domain-ux/domain-ux1b-premium-card-visuals
risk_level: LOW
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# DOMAIN-UX1B — Premium Health Systems Card Visual Hierarchy

## Classification

This is a LOW-risk frontend presentation sprint.

Reason: this sprint improves the visual hierarchy of the Wave 1 Health Systems Cards after DOMAIN-UX1A and DOMAIN-UX1A-PATCH. It must not alter backend logic, scoring, DTO structure, clinical interpretation, evidence completeness, reliability logic, or subsystem grouping.

Escalate to STANDARD or HIGH and STOP if implementation requires changes to:

- backend DTO models
- domain score assembler
- scoring policy
- evidence completeness logic
- reliability/confidence logic
- marker-to-subsystem grouping
- Knowledge Bus
- IDL
- root-cause / narrative compilers
- pipeline behaviour

## Purpose

DOMAIN-UX1A successfully surfaced the Wave 1 Health Systems Cards and DOMAIN-UX1A-PATCH corrected label hierarchy and zero-evidence states.

This sprint should make the cards feel more premium, visual and aligned with the agreed Health Systems Card design.

The aim is not to add new intelligence.  
The aim is to improve the presentation of already-governed data.

## Controlling authority

Read before doing anything:

```text
docs/planning-papers/DOMAIN_UX_health_systems_card_scaffold_sprint_plan_FINAL.md
docs/discussion documents/healthiq_health_systems_card_discussion_FINAL.md
docs/audit-papers/DOMAIN-UX1A_wave1_health_systems_card_scaffold_notes.md
docs/audit-papers/DOMAIN-UX1A_PATCH_card_labels_low_evidence_notes.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
````

If the planning document or DOMAIN-UX1A-PATCH notes are missing, STOP.

## Required output documentation

Create:

```text
docs/audit-papers/DOMAIN-UX1B_premium_health_systems_card_visuals_notes.md
```

This document must include:

1. preflight results
2. source documents reviewed
3. visual hierarchy changes made
4. score visual implementation
5. zero-evidence visual handling
6. partial-evidence visual handling
7. mobile/desktop layout notes
8. tests added/updated
9. Sentinel updates
10. confirmation that no backend/governed logic changed
11. residual gaps for DOMAIN-UX1C
12. recommendation for next sprint

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

* `work_id` is `DOMAIN-UX1B`
* branch is `domain-ux/domain-ux1b-premium-card-visuals`

If token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

## Baseline verification

Before implementation, confirm:

* Wave 1 Health Systems Cards are visible in the main journey
* `Score reliability` label is visible
* `Evidence completeness` label is visible
* zero-evidence cards render as `Not enough data`
* no subsystem chips or marker groupings are currently rendered
* existing card data comes from backend DTO fields

If this baseline is false, STOP and report.

## Required implementation

### A. Premium score visual

Replace or enhance the plain large text score with a premium score visual.

Acceptable forms:

* radial score device
* compact gauge
* refined numeric score card with visual arc/bar
* other clear premium visual treatment

Rules:

* use the existing backend-emitted score
* do not calculate new scores
* do not change score bands
* do not change thresholds
* do not alter backend data

For zero-evidence cards, do not show a score visual implying a true 0/100 health score.

### B. Refined collapsed-card layout

Improve the collapsed card layout so the user can quickly understand:

* domain name
* descriptor
* score or insufficient-data state
* band/status
* score reliability
* evidence completeness
* short health-system read

The card should feel calmer, clearer and less like a plain text report.

### C. Zero-evidence visual state

Make the zero-evidence state visually distinct and calm.

For cards where:

```text
evidence_completeness_numerator === 0
and evidence_completeness_denominator > 0
```

the card should clearly present:

```text
Not enough data
```

or equivalent, without making it look like a poor health score.

It should still show:

* score reliability
* evidence completeness
* short explanation that more markers are needed

### D. Partial-evidence visual state

For partial-evidence cards, such as:

```text
100 / 100
Limited reliability
1 of 5 expected markers included
```

the score may remain visible, but the visual hierarchy must prevent overconfidence.

Reliability and evidence completeness should be visually prominent enough that the user understands the score is limited by marker coverage.

### E. Compact missing-marker display

Improve the current missing-marker list visually if already present in the expanded card.

Allowed:

* chips
* small muted pills
* compact list
* greyed-out non-card marker states

Do not build full biomarker mini-cards in this sprint unless it can be done entirely frontend-side without new data needs.

Do not group markers by subsystem.

### F. No subsystem work

Do not add:

* Lipid transport chip
* Vascular strain chip
* Homocysteine pathway chip
* Glycaemic regulation chip
* Liver strain chip
* marker-to-subsystem grouping
* subsystem score/status

These remain DOMAIN-UX1C because Claude confirmed structured subsystem data is not yet available as governed DTO output.

### G. Mobile and desktop layout

Ensure the improved cards work on:

* desktop
* tablet-ish widths
* mobile

The cards must not become visually crowded.

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
* subsystem labels
* marker-to-subsystem groupings
* fake precision

## Potentially allowed files

```text
frontend/app/components/results/Wave1DomainCards.tsx
frontend/app/lib/wave1HealthSystemCardDisplay.ts
frontend/app/components/results/**/*
frontend/tests/components/Wave1DomainCards.test.tsx
backend/tests/regression/test_domain_ux1a_wave1_health_systems_card_scaffold.py
sentinel/packs/escaped_defects_v1.json
docs/audit-papers/DOMAIN-UX1B_premium_health_systems_card_visuals_notes.md
```

If a new purely presentational frontend component is created, keep it under:

```text
frontend/app/components/results/
```

## Required tests

Add or update deterministic tests proving:

### Premium score visual

* scored cards render a score visual or score-device wrapper
* zero-evidence cards do not render the score visual as a true health score
* score value still comes from DTO

### Label preservation

* `Score reliability` label remains visible
* `Evidence completeness` label remains visible
* reliability value remains visible
* evidence completeness value remains visible

### Zero-evidence preservation

* zero-evidence card shows `Not enough data` or equivalent
* zero-evidence card does not show `0 / 100`
* zero-evidence card does not show `Needs attention`

### No subsystem invention

* no subsystem placeholder UI
* no hardcoded supporting-system chips
* no marker-to-subsystem grouping

### Renderer-only guarantee

* frontend does not calculate evidence completeness from `missing_marker_ids`
* frontend does not calculate score/band/reliability
* frontend only renders DTO values

## Required Sentinel obligations

Add or update active deterministic Sentinel defect classes as appropriate, for example:

```text
health_system_card_score_visual_missing
health_system_card_zero_evidence_score_visual_visible
health_system_card_partial_evidence_overconfidence
health_system_card_frontend_invents_subsystem_chips
```

Each Sentinel class must point to an active deterministic test.

No placeholder Sentinel entries.

## Required validation commands

Run:

```powershell
python -m pytest backend/tests/regression/test_domain_ux1a_wave1_health_systems_card_scaffold.py -q
python -m pytest backend/tests/regression/test_fe_r1_consumer_prose_cleanup.py -q
python -m pytest backend/tests/regression/test_fe_r6a_fresh_uat_defect_cleanup.py -q
python -m pytest backend/tests/regression/test_canonical_mapping_star_suffix_failure.py -q
python -m pytest backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
python -m pytest backend/tests/unit/test_domain_score_assembler_v1.py -q
```

Also run any new DOMAIN-UX1B tests.

Run frontend validation:

```powershell
npm run type-check
```

If frontend component test command exists, run it.

If browser tools are available, inspect:

```text
http://localhost:3000/results?analysis_id=d7417288-7e11-48da-8716-d0f63f77c491
```

Confirm:

* cards look visually clearer than DOMAIN-UX1A-PATCH
* score visual is present for scored cardiovascular card
* zero-evidence cards do not show score visual as if they are true 0/100 scores
* reliability and evidence completeness remain visible
* no unsupported subsystem chips appear

Do not claim browser UAT passed unless actually inspected.

## Acceptance criteria

This sprint is complete only if:

* scored Wave 1 cards have a premium score visual or equivalent score device
* zero-evidence cards retain calm insufficient-data presentation
* partial-evidence cards do not visually overstate certainty
* reliability and evidence completeness remain labelled and visible
* missing-marker display is clearer if touched
* no subsystem labels or groupings are invented
* no backend/governed logic is changed
* no clinician-facing output is changed
* tests pass
* Sentinel guards are active
* notes document the remaining DOMAIN-UX1C subsystem gap

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

* if `automation_bus/latest_cursor_status.json` is the only dirty file and shows kernel-generated COMPLETE status for `DOMAIN-UX1B`, commit it automatically as:
  `chore(bus): DOMAIN-UX1B kernel COMPLETE status`
* if any other Automation Bus artefact is dirty, STOP and escalate

Do not merge.

Do not start DOMAIN-UX1C.

## Cursor completion statement

Cursor implements DOMAIN-UX1B only.

Cursor may not self-certify merge readiness, clinical correctness, or permission to begin DOMAIN-UX1C.

```
```
