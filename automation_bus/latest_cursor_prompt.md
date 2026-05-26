---
work_id: DOMAIN-UX1C
branch: domain-ux/domain-ux1c-governed-subsystem-evidence
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# DOMAIN-UX1C — Governed Subsystem Evidence Model

## Classification

This is a HIGH-risk MIXED sprint.

Reason: this sprint introduces backend-governed subsystem evidence for the Health Systems Cards. It may affect emitted DTO structure and user-facing interpretation surfaces. It must remain deterministic and must not create frontend-invented biological groupings.

This sprint must not change scoring thresholds, signal activation, root-cause arbitration, Knowledge Bus medical content, IDL records, or clinical scoring behaviour unless explicitly re-authorised.

## Purpose

DOMAIN-UX1A surfaced the Wave 1 Health Systems Cards.  
DOMAIN-UX1A-PATCH fixed label hierarchy and low-evidence display.  
DOMAIN-UX1B added premium score visuals and improved presentation.

The remaining major gap is that the cards do not yet show the evidence chain beneath each health system.

This sprint creates the governed backend DTO structure needed to support subsystem evidence in future card expansion.

The goal is to allow the frontend to render, without inventing:

- supporting subsystem labels
- included/scored marker IDs per subsystem
- missing marker IDs per subsystem
- optional subsystem status where safely supported
- source trace for why the subsystem appears

## Controlling authority

Read before doing anything:

```text
docs/planning-papers/DOMAIN_UX_health_systems_card_scaffold_sprint_plan_FINAL.md
docs/discussion documents/healthiq_health_systems_card_discussion_FINAL.md
docs/architecture/User Health to Systems Map_FINAL.md
docs/audit-papers/DOMAIN-UX1_health_systems_card_codebase_reality_audit.md
docs/audit-papers/DOMAIN-UX1A_wave1_health_systems_card_scaffold_notes.md
docs/audit-papers/DOMAIN-UX1A_PATCH_card_labels_low_evidence_notes.md
docs/audit-papers/DOMAIN-UX1B_premium_health_systems_card_visuals_notes.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
````

If any required UX/domain authority document is missing, STOP.

## Required output documentation

Create:

```text
docs/audit-papers/DOMAIN-UX1C_governed_subsystem_evidence_model_notes.md
```

This document must include:

1. preflight results
2. source documents reviewed
3. subsystem model implemented
4. domains covered
5. subsystem-to-marker mapping source
6. included-marker logic
7. missing-marker logic
8. whether subsystem status is emitted or deliberately omitted
9. DTO/model changes
10. frontend type changes, if any
11. tests added/updated
12. Sentinel updates
13. confirmation that scoring thresholds/signals/KB/IDL/root-cause were not changed
14. residual gaps for DOMAIN-UX1D

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

* `work_id` is `DOMAIN-UX1C`
* branch is `domain-ux/domain-ux1c-governed-subsystem-evidence`

If token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

## Baseline verification

Before implementation, confirm:

* `ConsumerDomainScoreV1.subsystems` currently exists but is null/empty
* frontend does not currently render subsystem chips or subsystem sections
* existing Wave 1 cards still render:

  * Cardiovascular health
  * Blood sugar control
  * Liver health
* zero-evidence cards still show “Not enough data”
* score reliability and evidence completeness labels still render
* no subsystem mapping currently exists as structured DTO output

If any assumption is false, STOP and report.

## Required implementation

### A. Define a governed subsystem DTO model

Add a typed subsystem structure beneath `ConsumerDomainScoreV1`.

Suggested structure:

```text
SubsystemEvidenceV1:
- subsystem_id
- subsystem_label
- included_marker_ids
- missing_marker_ids
- status_label optional/null
- evidence_role optional/null
- source_trace
```

Naming may vary if repo conventions require it, but the structure must clearly distinguish:

* subsystem identity
* consumer-safe label
* markers present/scored
* markers missing
* provenance/source trace

### B. Populate subsystem evidence for Wave 1 domains only

In scope:

```text
wave1_cardiovascular
wave1_blood_sugar
wave1_liver
```

Out of scope:

```text
blood_iron_oxygen
thyroid_energy
kidney_function
silent_inflammation
hormone_balance
```

### C. Use backend-governed mappings only

Define subsystem-to-marker mapping in backend code or governed config in one clear authority location.

The frontend must not define this mapping.

Do not scatter mapping across multiple files.

If there is already an appropriate authority source, use it.
If not, create a small clearly named backend mapping helper/module and document it.

### D. Conservative Wave 1 subsystem set

Use only safe, already-supported subsystem labels.

Suggested starting set, subject to repo evidence:

#### Cardiovascular health

* Lipid transport
* Homocysteine pathway
* Vascular strain context

#### Blood sugar control

* Glycaemic control
* Insulin and metabolic context

#### Liver health

* Liver enzyme pattern
* Liver processing context

Do not introduce decorative or over-specific labels unless the backend evidence supports them.

If any proposed label is not safely supported, omit it and document why.

### E. Included and missing marker logic

For each subsystem:

* `included_marker_ids` must contain markers present/scored for that subsystem
* `missing_marker_ids` must contain expected markers for that subsystem that were not present
* both must be backend-emitted
* neither may be calculated in frontend

Use existing scored marker and missing marker sources where possible.

Do not change domain-level evidence completeness logic.

### F. Subsystem status rule

Subsystem status is optional.

Only emit subsystem status if it can be derived safely from existing governed backend values without new scoring logic.

Allowed:

```text
status_label: null
```

Forbidden:

```text
frontend-generated subsystem status
fake subsystem score
new subsystem scoring thresholds
```

If status cannot be safely supported, leave it null and document deferral.

### G. Frontend type support

Update frontend TypeScript types to include the new subsystem structure.

Do not render full subsystem sections in this sprint unless minimal non-visual test rendering is required for type safety.

DOMAIN-UX1D will implement the full expanded card UI.

### H. No visible frontend subsystem UI unless explicitly safe

This sprint is primarily model/DTO scaffold.

Allowed:

* type support
* tests proving frontend does not invent subsystem labels
* optional hidden/non-rendered data availability checks

Forbidden:

* visually adding subsystem chips to cards
* visually adding subsystem sections
* grouping biomarker cards by subsystem

Those are DOMAIN-UX1D.

## Potentially allowed files

```text
backend/core/models/results.py
backend/core/analytics/domain_score_assembler.py
backend/core/analytics/domain_narrative_wave1.py
backend/tests/regression/**/*
backend/tests/unit/**/*
frontend/app/types/analysis.ts
frontend/app/components/results/Wave1DomainCards.tsx
frontend/tests/components/Wave1DomainCards.test.tsx
sentinel/packs/escaped_defects_v1.json
docs/audit-papers/DOMAIN-UX1C_governed_subsystem_evidence_model_notes.md
```

If a new backend helper is needed, keep it narrowly scoped under:

```text
backend/core/analytics/
```

and document why.

## Forbidden unless GPT explicitly approves

```text
backend/ssot/**/*
backend/core/scoring/**/*
backend/core/pipeline/**/*
backend/core/units/**/*
backend/core/analytics/root_cause*
backend/core/analytics/report_compiler*
backend/core/analytics/narrative_report_compiler*
knowledge_bus/**/*
frontend clinician report components
automation_bus/state/*
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
```

## Required tests

Add or update deterministic tests proving:

### Backend DTO

* each Wave 1 domain emits `subsystems`
* each subsystem has:

  * `subsystem_id`
  * `subsystem_label`
  * `included_marker_ids`
  * `missing_marker_ids`
  * `source_trace`
* subsystem IDs are stable strings
* subsystem labels are consumer-safe
* subsystem marker IDs are canonical biomarker IDs
* subsystem marker IDs are backend-emitted

### No frontend invention

* frontend does not define subsystem labels
* frontend does not define subsystem marker mappings
* frontend does not calculate included/missing subsystem markers
* frontend does not render visible subsystem chips in this sprint

### Scope protection

* no Wave 2 domains emit subsystem evidence unless explicitly supported and authorised
* no subsystem score/status is emitted unless safely supported
* no score thresholds changed
* no Knowledge Bus / IDL content changed
* no scoring policy changed

### Regression preservation

* DOMAIN-UX1A tests still pass
* DOMAIN-UX1A-PATCH tests still pass
* DOMAIN-UX1B score visual tests still pass
* FE-R1 prose safety still passes
* FE-R6A guard still passes
* MAP-R1A mapping guard still passes

## Required Sentinel obligations

Add or update active deterministic Sentinel defect classes as appropriate:

```text
health_system_subsystems_missing_from_dto
health_system_subsystem_labels_frontend_defined
health_system_subsystem_marker_grouping_frontend_defined
health_system_subsystem_fake_status_emitted
health_system_wave2_subsystems_prematurely_emitted
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

Also run any new DOMAIN-UX1C tests.

Run frontend validation:

```powershell
npm run type-check
```

If frontend component tests exist, run them.

## Acceptance criteria

This sprint is complete only if:

* `ConsumerDomainScoreV1` has a governed subsystem evidence structure
* Wave 1 domains emit backend-supplied subsystem evidence
* subsystem labels are backend-governed and consumer-safe
* included/missing marker IDs are backend-supplied
* frontend types are updated
* frontend does not invent subsystem labels or groupings
* no visible subsystem UI is introduced prematurely
* no subsystem score/status is emitted unless safely supported
* no scoring, signal, KB, IDL, root-cause or pipeline logic is changed
* all regression tests pass
* Sentinel guards are active
* notes document what DOMAIN-UX1D should render next

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

* if `automation_bus/latest_cursor_status.json` is the only dirty file and shows kernel-generated COMPLETE status for `DOMAIN-UX1C`, commit it automatically as:
  `chore(bus): DOMAIN-UX1C kernel COMPLETE status`
* if any other Automation Bus artefact is dirty, STOP and escalate

Do not merge.

Do not start DOMAIN-UX1D.

## Cursor completion statement

Cursor implements DOMAIN-UX1C only.

Cursor may not self-certify merge readiness, clinical correctness, or permission to begin DOMAIN-UX1D.

```
```
