---
work_id: DOMAIN-LABEL1
branch: domain-ux/domain-label1-governed-biomarker-display-labels
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# DOMAIN-LABEL1 — Governed Biomarker Display Label Authority

## Classification

This is a HIGH-risk MIXED sprint.

Reason: this sprint resolves biomarker display-name authority across the HealthIQ frontend/backend boundary. It may touch SSOT, DTO emission, subsystem evidence, and frontend rendering. It must prevent the frontend from becoming a parallel biomarker naming authority.

This sprint must not change scoring, signal activation, reference ranges, clinical interpretation, root-cause logic, Knowledge Bus content, or IDL records.

## Purpose

DOMAIN-UX1D exposed a structural label-authority problem.

Subsystem evidence currently renders marker names through:

```text
frontend/app/lib/wave1ConfidenceMarkerLabels.ts
````

This creates poor labels such as:

```text
hba1c
crp
Ldl Cholesterol
Hdl Cholesterol
Tc Hdl Ratio
```

The label-authority trace confirmed there is no single governed consumer-safe biomarker display-name authority today, and that extending `wave1ConfidenceMarkerLabels.ts` would deepen frontend label fragmentation. 

The purpose of this sprint is to resolve the problem permanently by creating or wiring a governed biomarker display-label authority and emitting consumer-safe marker labels through the DTO used by Health Systems Card subsystem evidence.

## Controlling authority

Read before doing anything:

```text
docs/planning-papers/DOMAIN_UX_health_systems_card_scaffold_sprint_plan_FINAL.md
docs/discussion documents/healthiq_health_systems_card_discussion_FINAL.md
docs/audit-papers/DOMAIN-UX1C_governed_subsystem_evidence_model_notes.md
docs/audit-papers/DOMAIN-UX1D_full_wave1_expanded_health_systems_card_notes.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
```

Also use the DOMAIN-UX1D Biomarker Label Authority Trace supplied by GPT/user as controlling context.

## Required output documentation

Create:

```text
docs/audit-papers/DOMAIN-LABEL1_governed_biomarker_display_label_authority_notes.md
```

This document must include:

1. preflight results
2. source documents reviewed
3. current label-authority problem
4. chosen authority source
5. SSOT/backend changes made
6. DTO changes made
7. frontend changes made
8. migration/deprecation decision for frontend label helpers
9. tests added/updated
10. Sentinel updates
11. confirmation that scoring/clinical interpretation did not change
12. residual gaps

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

* `work_id` is `DOMAIN-LABEL1`
* branch is `domain-ux/domain-label1-governed-biomarker-display-labels`

If token is missing or mismatched, STOP.

## Required investigation before implementation

Before changing code, trace and document:

1. all existing frontend biomarker label maps/helpers
2. all existing backend/SSOT biomarker identity fields
3. where uploaded `display_label` is used
4. where main biomarker cards get their labels
5. where subsystem evidence currently gets labels
6. whether `backend/ssot/biomarkers.yaml` can safely hold `consumer_display_name`
7. whether any existing SSOT field already fulfils this role

Do not implement until the authority choice is explicit in the notes.

## Required implementation direction

### A. Establish governed biomarker display-label authority

Preferred architecture:

```text
backend/SSOT biomarker definition
→ resolver/model layer
→ DTO
→ frontend renderer
```

Add or wire a consumer-safe biomarker display label field in the governed backend/SSOT layer.

Preferred field name:

```text
consumer_display_name
```

or repo-consistent equivalent.

This field should be short, retail-safe and suitable for card labels.

Examples:

```text
hba1c → HbA1c
crp → CRP
hs_crp → hs-CRP
ldl_cholesterol → LDL Cholesterol
hdl_cholesterol → HDL Cholesterol
tc_hdl_ratio → TC:HDL ratio
apob → ApoB
apoa1 → ApoA1
lipoprotein_a → Lipoprotein(a)
```

Do not use long SSOT clinical descriptions directly as UI labels.

### B. Emit labels through subsystem evidence DTO

Update subsystem evidence so frontend receives marker display labels directly from backend output.

Preferred DTO shape:

```text
included_markers: [
  {
    id: "hba1c",
    display_label: "HbA1c"
  }
]

missing_markers: [
  {
    id: "hs_crp",
    display_label: "hs-CRP"
  }
]
```

Maintain backward compatibility if existing `included_marker_ids` / `missing_marker_ids` are still needed.

Acceptable approach:

```text
- keep included_marker_ids / missing_marker_ids
- add included_markers / missing_markers as richer display objects
```

or replace only if tests prove no downstream breakage.

### C. Frontend must render backend-supplied labels

Update:

```text
Wave1SubsystemEvidenceSection.tsx
```

so it renders backend-supplied marker `display_label`.

Frontend must not resolve subsystem marker labels through `wave1ConfidenceMarkerLabels.ts`.

Frontend may only use fallback formatting as a defensive last resort if backend label is absent, and such fallback must be guarded/tested as a defect path, not normal behaviour.

### D. Do not expand the frontend label map

Do not fix this by adding more entries to:

```text
frontend/app/lib/wave1ConfidenceMarkerLabels.ts
```

That is explicitly forbidden as the primary fix.

You may deprecate it, route it to the governed label source if feasible, or leave it untouched if no longer used by subsystem evidence.

### E. Scope marker coverage

At minimum, the governed label authority must cover all Wave 1 subsystem marker IDs:

```text
total_cholesterol
ldl_cholesterol
hdl_cholesterol
triglycerides
tc_hdl_ratio
apob
apoa1
lipoprotein_a
homocysteine
crp
hs_crp
hba1c
glucose
insulin
alt
ast
ggt
alp
bilirubin
albumin
```

If the current subsystem mappings contain additional marker IDs, include them too.

### F. No clinical interpretation changes

This sprint is naming/display authority only.

Do not change:

* scoring thresholds
* evidence completeness
* marker inclusion rules
* subsystem mappings
* confidence logic
* signal logic
* root-cause logic
* IDL/KB content

## Potentially allowed files

```text
backend/ssot/biomarkers.yaml
backend/core/canonical/**/*
backend/core/models/results.py
backend/core/analytics/wave1_subsystem_evidence.py
backend/core/analytics/domain_score_assembler.py
backend/tests/regression/**/*
backend/tests/unit/**/*
frontend/app/types/analysis.ts
frontend/app/components/results/Wave1SubsystemEvidenceSection.tsx
frontend/app/components/results/Wave1DomainCards.tsx
frontend/app/lib/wave1ConfidenceMarkerLabels.ts
frontend/tests/components/Wave1SubsystemEvidenceSection.test.tsx
frontend/tests/components/Wave1DomainCards.test.tsx
sentinel/packs/escaped_defects_v1.json
docs/audit-papers/DOMAIN-LABEL1_governed_biomarker_display_label_authority_notes.md
```

Touch only the minimum necessary files.

## Forbidden unless GPT explicitly approves

```text
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

### SSOT/backend authority

* each Wave 1 subsystem marker has a governed consumer display label
* labels are loaded from backend/SSOT or backend-governed source
* missing markers receive display labels even when not present in `analysis.biomarkers[]`
* subsystem evidence emits marker display labels

### DTO contract

* subsystem evidence includes marker objects or equivalent label-bearing structure
* included markers include `id` and `display_label`
* missing markers include `id` and `display_label`
* legacy ID arrays are preserved if required

### Frontend rendering

* `Wave1SubsystemEvidenceSection` renders backend-supplied labels
* it does not call `wave1ConfidenceMarkerDisplayLabel` for normal subsystem marker display
* it does not render poor fallback labels:

  * `hba1c`
  * `crp`
  * `Ldl Cholesterol`
  * `Hdl Cholesterol`
  * `Tc Hdl Ratio`
* missing markers render proper labels and `Not uploaded`

### Authority protection

* no new frontend biomarker label map is introduced
* `wave1ConfidenceMarkerLabels.ts` is not expanded as the primary fix
* frontend does not define biomarker naming authority
* frontend fallback is defensive only

## Required Sentinel obligations

Add or update active deterministic Sentinel defect classes as appropriate:

```text
biomarker_display_label_frontend_authority_expansion
subsystem_marker_display_label_missing_from_dto
subsystem_marker_poor_fallback_label_visible
subsystem_missing_marker_label_not_governed
wave1_confidence_marker_labels_expanded_as_primary_fix
```

Each Sentinel class must point to an active deterministic test.

No placeholder Sentinel entries.

## Required validation commands

Run:

```powershell
python -m pytest backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py -q
python -m pytest backend/tests/regression/test_domain_ux1a_wave1_health_systems_card_scaffold.py -q
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

Run frontend component tests if available.

If browser tools are available, inspect:

```text
http://localhost:3000/results?analysis_id=d7417288-7e11-48da-8716-d0f63f77c491
```

Confirm expanded subsystem evidence shows proper labels such as:

```text
HbA1c
CRP
LDL Cholesterol
HDL Cholesterol
TC:HDL ratio
Homocysteine
```

Do not claim browser UAT passed unless actually inspected.

## Acceptance criteria

This sprint is complete only if:

* biomarker display labels have a governed backend/SSOT authority
* subsystem evidence DTO carries display labels or equivalent backend-supplied label objects
* frontend renders backend-supplied labels
* poor fallback labels no longer appear in subsystem evidence
* missing markers have proper display labels
* `wave1ConfidenceMarkerLabels.ts` is not expanded as the primary fix
* no scoring, interpretation, KB, IDL, root-cause or pipeline logic is changed
* tests pass
* Sentinel guards are active
* notes clearly document remaining frontend label helpers and deprecation path

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

* if `automation_bus/latest_cursor_status.json` is the only dirty file and shows kernel-generated COMPLETE status for `DOMAIN-LABEL1`, commit it automatically as:
  `chore(bus): DOMAIN-LABEL1 kernel COMPLETE status`
* if any other Automation Bus artefact is dirty, STOP and escalate

Do not merge.

Do not start another sprint.

## Cursor completion statement

Cursor implements DOMAIN-LABEL1 only.

Cursor may not self-certify merge readiness, clinical correctness, or permission to begin the next sprint.

```
```
