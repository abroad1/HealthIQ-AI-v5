---
work_id: PASS3-BATCH2-FRAME-INDEX-2_remaining_single_frame_batch2_identity_index_expansion
branch: work/PASS3-BATCH2-FRAME-INDEX-2-remaining-single-frame-batch2-identity-index-expansion
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# PASS3-BATCH2-FRAME-INDEX-2 — Remaining Single-Frame Batch 2 Identity Index Expansion

## Purpose

Index the remaining single-frame Batch 2 Pass_3 signal families into the governed medical frame identity index.

This sprint follows:

```text
PASS3-BATCH2-INGEST-1
PASS3-BATCH2-FRAME-INDEX-1
PASS3-BATCH2-PROVENANCE-1
````

Batch 2 is now registered as canonical and the `pkg_kb47_*` manifests have been realigned to `Batch_2_Pass_3.json`.

This sprint must complete the next safe indexing step for the remaining Batch 2 families, while treating androgen-panel signals with explicit medical-review caution.

Do not promote packages.
Do not activate packages.
Do not retire packages.
Do not modify runtime package logic.

---

## Strategic framing

Batch 2 contains validated Pass_3 research and compiled `pkg_kb47_*` packages.

The current architecture requires:

```text
Pass_3 research
→ medical frame identity index
→ generated biomarker tree
→ future promotion readiness review
```

This sprint updates the frame index only.

It must not treat hormone/androgen-related signals as automatically safe just because they are single-frame. Single-frame does not mean low-risk.

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
PASS3-BATCH2-INGEST-1 merged
PASS3-BATCH2-FRAME-INDEX-1 merged
PASS3-BATCH2-PROVENANCE-1 merged
PASS3-FRAME-INDEX-3 merged
MED-FRAME-TREE-1 merged
ARCH-SENTINEL-1 merged
CI-ARCH-GATE-1 / CI-ARCH-GATE-1A merged
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
- Batch_2_Pass_3.json is missing
- pass3_batch2_research_asset_register_v1.yaml is missing
- pass3_batch2_kb47_manifest_realign_register_v1.yaml is missing
- medical_frame_identity_index_v1.yaml is missing
- biomarker_medical_frame_tree.md is missing
```

---

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint updates governed medical frame identity infrastructure using canonical Batch 2 research. It must not change runtime behaviour, but it affects future package promotion and medical-intelligence safety gates.

---

## Required inputs

Read before work:

```text
knowledge_bus/governance/pass3_batch2_research_asset_register_v1.yaml
knowledge_bus/governance/pass3_batch2_kb47_manifest_realign_register_v1.yaml
knowledge_bus/research/investigation_specs/multi_llm_research/Batch_2_Pass_3.json
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/medical_frame_identity_expansion_candidates_v1.yaml
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
docs/audit-papers/PASS3-BATCH2-INGEST-1_batch2_pass3_research_asset_registration_report.md
docs/audit-papers/PASS3-BATCH2-FRAME-INDEX-1_batch2_multiframe_identity_index_expansion_report.md
docs/audit-papers/PASS3-BATCH2-PROVENANCE-1_kb47_manifest_canonical_source_realign_report.md
docs/architecture/biomarker_medical_frame_tree.md
docs/sprints/launch_core_carry_forward_register.md
```

Also inspect relevant compiled packages:

```text
knowledge_bus/packages/pkg_kb47_*
```

---

## Required scope

Index the remaining Batch 2 single-frame families not indexed by `PASS3-BATCH2-FRAME-INDEX-1`.

Expected remaining families include:

```text
dhea
fai
free_t3
free_t4
free_testosterone
free_testosterone_pct
```

Confirm the exact remaining families from:

```text
knowledge_bus/governance/pass3_batch2_research_asset_register_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

Do not assume the list blindly.

---

## Androgen-panel caution

The androgen-related families require explicit medical-review caution before future activation or promotion.

This includes at least:

```text
dhea
fai
free_testosterone
free_testosterone_pct
```

For these, use conservative governance status:

```yaml
promotion_state: compiled_not_promoted
runtime_authority_status: inactive
clinical_adjudication_status: required_before_activation
```

Do not mark androgen-panel frames as `runtime_active_canonical`.

Do not mark medical review as complete.

Do not claim these are simple low-risk frames.

---

## Thyroid-panel caution

Thyroid-related families such as:

```text
free_t3
free_t4
```

may be clinically more straightforward than androgen frames, but still must not be activated in this sprint.

Use conservative governance status unless there is explicit existing governance saying otherwise:

```yaml
promotion_state: compiled_not_promoted
runtime_authority_status: inactive
clinical_adjudication_status: required_before_activation
```

---

## Required preflight

Before editing the index, report:

```text
1. remaining Batch 2 families not yet indexed
2. all matching spec_ids
3. all signal_ids
4. all primary biomarker IDs
5. trigger directions
6. matching pkg_kb47 package paths
7. whether each package manifest now points to canonical Batch_2_Pass_3.json
8. whether source package paths exist
9. whether any activation_key would duplicate an active frame
10. whether the family is androgen-related, thyroid-related or other
11. whether medical review is required before future activation
```

STOP if any selected family cannot be mapped to Batch 2 specs and `pkg_kb47_*` packages with confidence.

---

## Required index fields

Every new frame entry must include all required index fields:

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

Use existing allowed enum values only.

---

## State classification rules

For Batch 2 frames where a compiled `pkg_kb47_*` package exists and provenance has been realigned:

```yaml
promotion_state: compiled_not_promoted
runtime_authority_status: inactive
clinical_adjudication_status: required_before_activation
collision_status: none
```

Use `collision_status: requires_adjudication` only if there is evidence of an activation-key or clinical-frame collision.

Do not introduce duplicate active activation keys.

Do not mark any Batch 2 frame as runtime-active in this sprint.

---

## Required family-level outputs

For each indexed family, document:

```text
- number of frames added
- frame role represented
- matching Batch 2 spec
- matching pkg_kb47 package
- whether package manifest provenance is canonical
- whether medical review is required
- whether future package promotion remains blocked
```

---

## Tree regeneration

After index update, regenerate the human-readable tree:

```powershell
python knowledge_bus/tools/build_biomarker_medical_frame_tree.py
```

Update:

```text
docs/architecture/biomarker_medical_frame_tree.md
```

Do not edit the tree manually.

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
docs/sprints/launch_core_carry_forward_register.md
```

Create:

```text
docs/audit-papers/PASS3-BATCH2-FRAME-INDEX-2_remaining_single_frame_batch2_identity_index_expansion_report.md
```

---

## Carry-forward handling

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Expected handling:

```text
CF-BATCH2-004
Should be marked Resolved only if all remaining single-frame Batch 2 families are indexed.

CF-BATCH2-001
Should be marked Resolved only if all Batch 2 frame indexing is now complete.

CF-BATCH2-003
Should remain Open. Promotion readiness review is after indexing and provenance alignment.

CF-BATCH2-002
Should remain Resolved unless this sprint discovers a provenance regression.
```

Likely new carry-forward if needed:

```text
CF-BATCH2-005 — medical review of androgen-panel Batch 2 frames before promotion readiness.
```

Do not mark promotion readiness complete.

---

## Required report content

The report must include:

```text
- executive verdict
- artefacts inspected
- remaining Batch 2 families identified
- selected families and rationale
- Batch 2 specs indexed
- frame entries added
- family/frame counts before and after
- pkg_kb47 package existence/provenance findings
- androgen-panel caution / medical-review status
- thyroid-panel caution / medical-review status
- collision checks
- clinical adjudication statuses
- tree regeneration summary
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

Also validate that the index and tree contain all newly indexed Batch 2 families.

Do not write only “all tests passed”.

---

## Out of scope

Do not:

```text
- change pkg_kb47 manifests
- compile packages
- promote packages
- activate packages
- retire packages
- modify runtime package files
- implement Layer B frame assembly
- implement context modifier evaluation
- change frontend
- adjudicate medical truth
- add new context modifiers
```

---

## STOP conditions

STOP and report if:

```text
1. remaining Batch 2 families cannot be identified
2. selected families cannot be mapped to Batch 2 specs
3. selected families cannot be mapped to pkg_kb47 packages
4. package provenance is not canonical after PASS3-BATCH2-PROVENANCE-1
5. frame entries would require clinical invention
6. duplicate active activation keys would be introduced
7. tree regeneration omits indexed frames
8. architecture gate fails
9. any runtime/package/frontend change appears necessary
```

---

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. files inspected
3. remaining Batch 2 families
4. selected Batch 2 specs
5. frame entries added
6. family/frame counts before and after
7. pkg_kb47 provenance confirmation
8. androgen/thyroid medical-review handling
9. tree regeneration evidence
10. validation commands run
11. actual validation output
12. carry-forward updates
13. confirmation no runtime/package/frontend changes
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
- current branch matches work/PASS3-BATCH2-FRAME-INDEX-2-remaining-single-frame-batch2-identity-index-expansion
- only in-scope docs/governance/tree/register files changed
- no runtime package files changed
- no frontend/runtime evaluator files changed
- no ambiguous stash exists
- validators and architecture gate pass
```

---

## Success criteria

This sprint is complete only if:

```text
1. remaining Batch 2 single-frame families are identified
2. remaining safe-to-index families are indexed
3. androgen-panel families are explicitly marked medical-review required
4. every new frame validates
5. no duplicate active activation keys are introduced
6. pkg_kb47 provenance is confirmed canonical
7. generated tree includes the new families/frames
8. Batch 2 carry-forwards are updated accurately
9. no runtime/package/frontend changes occur
10. architecture gate passes
```

```
```
