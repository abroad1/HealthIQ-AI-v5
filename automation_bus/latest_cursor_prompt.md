---
work_id: PASS3-BATCH2-FRAME-INDEX-1_batch2_multiframe_identity_index_expansion
branch: work/PASS3-BATCH2-FRAME-INDEX-1-batch2-multiframe-identity-index-expansion
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# PASS3-BATCH2-FRAME-INDEX-1 — Batch 2 Multi-Frame Identity Index Expansion

## Purpose

Index the highest-risk Batch 2 Pass_3 signal families into the governed medical frame identity index.

This sprint follows `PASS3-BATCH2-INGEST-1`, which registered `Batch_2_Pass_3.json` as a canonical research asset and identified 16 new signal families not yet represented in the medical frame identity index.

This sprint must start with the Batch 2 ROUTE_C / multi-frame families:

```text
creatine_kinase
egfr
eosinophil_pct
eosinophils_abs
````

The goal is to preserve distinct medical frames before any package promotion or package provenance realignment occurs.

Do not promote packages.
Do not activate packages.
Do not retire packages.
Do not modify runtime package files.

---

## Strategic framing

Batch 2 is now a validated canonical Pass_3 research asset.

The next architecture step is:

```text
Batch 2 Pass_3 research
→ medical frame identity index entries
→ regenerated human-readable biomarker tree
→ future package provenance realignment / promotion readiness review
```

This sprint must not treat each biomarker as a single flat signal. It must preserve distinct frames where Batch 2 contains multiple medically meaningful interpretations.

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
PASS3-BATCH2-INGEST-1 merged
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

This sprint updates governed medical frame identity infrastructure using newly registered canonical research. It must not change runtime behaviour, but it affects future package promotion and medical-intelligence safety gates.

---

## Required inputs

Read before work:

```text
knowledge_bus/governance/pass3_batch2_research_asset_register_v1.yaml
knowledge_bus/research/investigation_specs/multi_llm_research/Batch_2_Pass_3.json
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/medical_frame_identity_expansion_candidates_v1.yaml
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
knowledge_bus/governance/pass3_frame_coverage_audit_v1.yaml
docs/audit-papers/PASS3-BATCH2-INGEST-1_batch2_pass3_research_asset_registration_report.md
docs/architecture/biomarker_medical_frame_tree.md
docs/sprints/launch_core_carry_forward_register.md
```

Also inspect relevant existing compiled packages:

```text
knowledge_bus/packages/pkg_kb47_*
knowledge_bus/packages/**
```

If paths differ, locate and report actual paths.

---

## Required scope

Index the four Batch 2 multi-frame families identified by `PASS3-BATCH2-INGEST-1`:

```text
1. creatine_kinase
2. egfr
3. eosinophil_pct
4. eosinophils_abs
```

For each family, add medically distinct frame entries into:

```text
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

Do not index all 16 Batch 2 families in this sprint.

Do not modify package manifests yet. The `pkg_kb47_*` provenance realignment is CF-BATCH2-002 and remains out of scope unless hardening explicitly approves.

---

## Required preflight

Before editing the index, report:

```text
1. all Batch 2 specs for the four selected families
2. spec_id values
3. signal_id values
4. primary biomarker IDs
5. trigger directions
6. source package candidates, especially pkg_kb47_* packages
7. whether source package paths exist
8. whether any activation_key would duplicate an active frame
9. whether any frame requires medical review before future activation
10. whether current context modifiers already reference these families or frames
```

STOP if a selected family cannot be mapped to Batch 2 specs.

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

Because `PASS3-BATCH2-INGEST-1` found that `pkg_kb47_*` compiled packages already exist but point to archived `Batch_2_Pass_3_Rev1.json`, use careful state language.

For Batch 2 frames where a compiled `pkg_kb47_*` package exists:

```text
promotion_state: compiled_not_promoted
runtime_authority_status: inactive
clinical_adjudication_status: required_before_activation
collision_status: requires_adjudication or none, depending on activation identity
```

Do not mark them `runtime_active_canonical` unless there is clear evidence they are runtime authority.

For Batch 2 frames without a compiled package:

```text
promotion_state: deferred
runtime_authority_status: inactive
clinical_adjudication_status: required_before_activation
```

Do not create duplicate active activation keys.

---

## Required family-level outputs

For each selected family, document:

```text
- number of frames added
- frame roles represented
- whether pkg_kb47 package exists
- whether provenance realignment is needed
- whether medical review is needed
- whether package promotion is blocked until indexing/provenance is complete
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
docs/audit-papers/PASS3-BATCH2-FRAME-INDEX-1_batch2_multiframe_identity_index_expansion_report.md
```

---

## Carry-forward handling

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Expected handling:

```text
CF-BATCH2-001
Should be partially resolved only if the four selected multi-frame families are indexed.
If the CF was written for all 16 families, update it to show this sprint completed the multi-frame subset and leave a residual item for the remaining single-frame families.

CF-BATCH2-002
Remain Open. This sprint must not realign pkg_kb47 manifest provenance unless explicitly approved.

CF-BATCH2-003
Remain Open. Promotion readiness review is after indexing/provenance alignment.

Possible new carry-forward:
CF-BATCH2-004 — index remaining single-frame Batch 2 families.
```

Do not mark all Batch 2 indexing complete unless all 16 families are indexed, which is not expected in this sprint.

---

## Required report content

The report must include:

```text
- executive verdict
- artefacts inspected
- selected Batch 2 families and rationale
- Batch 2 specs indexed
- frame entries added
- family/frame counts before and after
- pkg_kb47 package existence findings
- provenance realignment implications
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

Also validate that the index and tree contain the four selected families.

Do not write only “all tests passed”.

---

## Out of scope

Do not:

```text
- index all 16 Batch 2 families
- change pkg_kb47 manifests
- realign package provenance
- compile packages
- promote packages
- activate packages
- retire packages
- modify runtime package files
- implement Layer B frame assembly
- implement context modifier evaluation
- change frontend
- adjudicate medical truth
```

---

## STOP conditions

STOP and report if:

```text
1. Batch 2 specs for selected families cannot be found
2. selected families cannot be represented without clinical invention
3. source package paths cannot be resolved or classified
4. duplicate active activation keys would be introduced
5. tree regeneration omits indexed frames
6. architecture gate fails
7. any runtime/package/frontend change appears necessary
```

---

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. files inspected
3. selected Batch 2 specs
4. frame entries added
5. family/frame counts before and after
6. pkg_kb47 findings
7. tree regeneration evidence
8. validation commands run
9. actual validation output
10. carry-forward updates
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
- current branch matches work/PASS3-BATCH2-FRAME-INDEX-1-batch2-multiframe-identity-index-expansion
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
1. the four selected Batch 2 multi-frame families are indexed
2. every new frame validates
3. no duplicate active activation keys are introduced
4. pkg_kb47 package existence/provenance implications are documented
5. generated tree includes the new families/frames
6. Batch 2 carry-forwards are updated accurately
7. no runtime/package/frontend changes occur
8. actual validation output is pasted
9. architecture gate passes
10. remaining Batch 2 work is clearly scoped
```

```
```
