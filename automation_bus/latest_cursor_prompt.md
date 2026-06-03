---
work_id: PASS3-FRAME-INDEX-3_next_high_risk_signal_family_expansion
branch: work/PASS3-FRAME-INDEX-3-next-high-risk-signal-family-expansion
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# PASS3-FRAME-INDEX-3 — Next High-Risk Signal Family Expansion

## Purpose

Continue expanding the governed medical frame identity index beyond the initial indexed families.

This sprint must add the next highest-risk biomarker signal families from the estate-wide frame coverage audit into:

```text
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
````

The goal is to keep building the governed biomarker → medical-frame architecture so the generated human-readable tree becomes progressively more complete.

This is not a package-promotion sprint.

Do not activate, retire, overwrite, or modify runtime packages.

---

## Strategic framing

The human-readable biomarker tree is generated from the medical frame identity index.

Therefore:

```text
medical frame index expands
→ generated biomarker tree expands
```

This sprint should add the next batch of high-risk signal families to the index so that HealthIQ can continue moving away from flat biomarker interpretation and toward:

```text
one biomarker signal family
→ multiple medically distinct frames
→ supporting evidence
→ context modifiers
→ governed Layer B interpretation
```

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
PASS3-FRAME-COVERAGE-1 merged
PASS3-FRAME-INDEX-2 merged
MED-FRAME-TREE-1 merged
ARCH-SENTINEL-1 merged
CI-ARCH-GATE-1 / CI-ARCH-GATE-1A merged
MED-FRAME-2 merged
CONTEXT-MOD-1 merged
```

Before starting, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 12
git rev-parse HEAD
git rev-parse origin/main
```

STOP if:

```text
- current branch is not main
- local main does not equal origin/main
- working tree is not clean
- medical_frame_identity_index_v1.yaml is missing
- pass3_frame_coverage_audit_v1.yaml is missing
- biomarker_medical_frame_tree.md is missing
- architecture gate script is missing
```

---

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint updates governed medical frame identity infrastructure. It must not change runtime behaviour, but it affects future medical-intelligence promotion and safety gates.

---

## Required inputs

Read before work:

```text
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/pass3_frame_coverage_audit_v1.yaml
knowledge_bus/governance/medical_frame_identity_expansion_candidates_v1.yaml
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
docs/architecture/biomarker_medical_frame_tree.md
docs/audit-papers/PASS3-FRAME-COVERAGE-1_estate_wide_multiframe_research_coverage_audit.md
docs/audit-papers/PASS3-FRAME-INDEX-2_high_risk_signal_family_index_expansion_report.md
docs/audit-papers/MED-FRAME-TREE-1_generated_human_readable_biomarker_frame_tree_report.md
docs/sprints/launch_core_carry_forward_register.md
```

Also inspect relevant source artefacts for selected families:

```text
knowledge_bus/packages/**
knowledge_bus/research/investigation_specs/multi_llm_research/**/*Pass_3*.json
knowledge_bus/governance/pass3_legacy_package_mapping_plan_v1.yaml
```

---

## Family selection

Cursor must not choose families by instinct.

Rank the next candidate families using the estate audit and existing expansion-candidate file.

Selection criteria:

```text
1. edge_case_loss_risk = high
2. promotion_safety_status = blocked_pending_frame_adjudication
3. promotion_safety_status = blocked_pending_pass3_enrichment
4. multiple Pass_3 frames exist
5. legacy package contains override/escalation logic
6. currently absent from medical_frame_identity_index_v1.yaml
7. clinically important system area
8. needed before package promotion can safely resume
```

Before editing the index, report a ranked shortlist.

Do not index every remaining family.

Expected scope:

```text
Add 2–4 new high-risk signal families.
```

Do not re-index families already covered:

```text
- signal_creatinine_high
- signal_alt_high
- signal_crp_high
- signal_ferritin_high
```

unless only adding minor notes required by validation.

---

## Required index update

Update:

```text
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

For each selected family, add medically distinct frames with all required fields:

```yaml
signal_family_id:
primary_biomarker_id:
medical_frame_id:
frame_label:
frame_role:
research_spec_id:
source_package_id:
source_package_path:
activation_key:
signal_id:
promotion_state:
runtime_authority_status:
clinical_adjudication_status:
context_inputs_supported:
  biomarker_evidence:
  questionnaire_modifiers:
  medication_modifiers:
collision_group_id:
collision_status:
supersedes:
superseded_by:
notes:
```

Do not introduce duplicate active activation keys.

Do not mark unadjudicated frames as resolved.

Do not make the index runtime-consumed.

---

## Required frame classification rules

Use existing allowed values only.

Allowed `promotion_state` values include:

```text
runtime_active_canonical
runtime_active_legacy_unadjudicated
compiled_not_promoted
superseded
retired
deferred
```

Allowed `clinical_adjudication_status` values include:

```text
not_required
required_before_activation
accepted_with_rationale
blocked_pending_medical_review
```

Allowed `collision_status` values include:

```text
none
real_collision_active_blocker
allowed_non_runtime_collision
resolved_by_supersession
requires_adjudication
```

If a family cannot be safely represented without clinical judgement, do not force it. Mark it deferred and document the blocker.

---

## Required tree regeneration

After updating the index, regenerate the human-readable tree:

```powershell
python knowledge_bus/tools/build_biomarker_medical_frame_tree.py
```

The generated tree must include the newly indexed families and frames.

Update:

```text
docs/architecture/biomarker_medical_frame_tree.md
```

Do not edit the tree manually.

---

## MED-FRAME-TREE carry-forward

Address the minor carry-forward from MED-FRAME-TREE-1 if safe:

```text
CF-MEDTREE-001 — wire generated tree refresh into architecture gate or docs generation workflow and add generate() path guard.
```

For this sprint, do the small safe part:

```text
- add output-path guard inside generate(), not only the CLI wrapper
- add/update regression test proving generate() rejects output outside docs/architecture/
```

Do not wire tree generation into CI in this sprint unless hardening explicitly approves. If not wired, leave CF-MEDTREE-001 open.

---

## Governance helper boundary

Any helper tooling must remain under:

```text
knowledge_bus/tools/
```

Do not create new helper scripts under `backend/scripts/` unless explicitly justified by hardening.

Helper tools must:

```text
- be read-only against governance/package inputs
- write only declared docs/governance outputs
- avoid runtime/evaluator/frontend imports
- avoid modifying package/runtime/frontend files
```

---

## Required artefacts

Update:

```text
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
docs/architecture/biomarker_medical_frame_tree.md
```

Update if needed:

```text
knowledge_bus/governance/medical_frame_identity_expansion_candidates_v1.yaml
knowledge_bus/tools/build_biomarker_medical_frame_tree.py
backend/tests/regression/test_biomarker_medical_frame_tree_generation.py
docs/sprints/launch_core_carry_forward_register.md
```

Create:

```text
docs/audit-papers/PASS3-FRAME-INDEX-3_next_high_risk_signal_family_expansion_report.md
```

---

## Required report content

The report must include:

```text
- executive verdict
- artefacts inspected
- ranked candidate family shortlist
- selected families and rationale
- families deliberately not selected and why
- frame entries added
- collision checks
- clinical adjudication statuses
- Pass_3 enrichment needs
- tree regeneration summary
- family/frame counts before and after
- MED-FRAME-TREE carry-forward handling
- validation output pasted in full
- runtime boundary confirmation
- carry-forward updates
- remaining limitations
- recommended next sprint
```

---

## Runtime boundary

Do not modify:

```text
SignalEvaluator
SignalRegistry
runtime loaders
domain_score_assembler
report_compiler
frontend
SSOT
scoring thresholds
unit conversion
knowledge_bus/packages/*
knowledge_bus/current/latest_knowledge_status.json
```

If any runtime/package/frontend change appears necessary, STOP and report.

---

## Required validations

Run and paste actual output:

```powershell
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
python knowledge_bus/tools/build_biomarker_medical_frame_tree.py
python backend/scripts/run_architecture_validation_gate.py
python -m pytest backend/tests/regression/test_biomarker_medical_frame_tree_generation.py -q
```

Also run, unless already included in the architecture gate output:

```powershell
python -m pytest backend/tests/architecture/test_medical_intelligence_architecture_sentinels.py -q
```

Do not write only “all tests passed”.

---

## Out of scope

Do not:

```text
- enrich Pass_3 specs
- create or promote package artefacts
- activate packages
- retire packages
- modify runtime package files
- implement Layer B frame assembly
- implement context modifier evaluation
- change frontend
- adjudicate medical truth
- index the entire remaining estate
```

---

## STOP conditions

STOP and report if:

```text
1. ranked shortlist cannot be derived from audit artefacts
2. selected family cannot be mapped to package and Pass_3 evidence
3. frame entries would require clinical invention
4. duplicate active activation keys would be introduced
5. tree generation omits indexed frames
6. architecture gate fails
7. any runtime/package/frontend change appears necessary
```

---

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. files inspected
3. ranked shortlist
4. selected families and rationale
5. frame entries added
6. tree regenerated
7. family/frame counts before and after
8. carry-forward updates
9. validation commands run
10. actual validation output
11. confirmation no runtime/package/frontend changes
```

---

## Closure requirements

Before finish, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
git diff --name-only
git diff --cached --name-only
git stash list
```

Do not run finish unless:

```text
- current branch matches work/PASS3-FRAME-INDEX-3-next-high-risk-signal-family-expansion
- only in-scope docs/governance/tooling/test/register files changed
- no runtime package files changed
- no frontend/runtime evaluator files changed
- no ambiguous stash exists
- validators and architecture gate pass
```

---

## Success criteria

This sprint is complete only if:

```text
1. ranked family shortlist is produced from audit evidence
2. 2–4 new high-risk signal families are added to the frame index
3. every new frame validates
4. no duplicate active activation keys are introduced
5. generated tree includes the new families/frames
6. tree remains generated and non-authoritative
7. MED-FRAME-TREE output-path guard is addressed or carried forward
8. no runtime/package/frontend changes occur
9. actual validator output is pasted
10. architecture gate passes
```

```
```
