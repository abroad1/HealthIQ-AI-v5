---
work_id: BATCH2-CLOSURE-1_final_batch2_promotion_decision
branch: work/BATCH2-CLOSURE-1-final-batch2-promotion-decision
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# BATCH2-CLOSURE-1 — Final Batch 2 Promotion Decision

## Purpose

Consolidate all Batch 2 governance, review, indexing, provenance and readiness work into one final promotion decision.

This sprint must decide whether Batch 2 is ready to proceed to a controlled promotion sprint, and if so, exactly which packages are cleared.

This sprint must not promote packages.

The output must be a final go/no-go decision register for Batch 2.

---

## Strategic framing

We are stopping the micro-sprint pattern.

Batch 2 has already been:

```text
- registered as canonical research
- validated
- provenance-corrected
- indexed into the medical frame identity index
- added to the human-readable tree
- reviewed for promotion readiness
- androgen-reviewed
- androgen context-bound
````

This sprint must now consolidate that evidence and make the final decision.

The next sprint after this should be either:

```text
BATCH2-PROMOTE-1
```

or:

```text
Batch 2 paused / closed with blockers documented
```

Do not create new sub-sprints unless a genuine safety blocker is found.

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
PASS3-BATCH2-INGEST-1 merged
PASS3-BATCH2-PROVENANCE-1 merged
PASS3-BATCH2-FRAME-INDEX-1 merged
PASS3-BATCH2-FRAME-INDEX-2 merged
BATCH2-PROMOTION-READINESS-1 merged
BATCH2-MEDREVIEW-1 merged
BATCH2-CONTEXT-MOD-1 merged
ARCH-SENTINEL-1 merged
CI-ARCH-GATE-1 / CI-ARCH-GATE-1A merged
MED-FRAME-TREE-1 merged
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
- any required Batch 2 governance register is missing
```

---

## Required inputs

Read before work:

```text
knowledge_bus/governance/pass3_batch2_research_asset_register_v1.yaml
knowledge_bus/governance/pass3_batch2_kb47_manifest_realign_register_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/batch2_promotion_readiness_register_v1.yaml
knowledge_bus/governance/batch2_androgen_panel_medical_review_v1.yaml
knowledge_bus/governance/batch2_androgen_context_modifier_binding_v1.yaml
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
docs/architecture/biomarker_medical_frame_tree.md
docs/sprints/launch_core_carry_forward_register.md
```

Read the relevant audit reports:

```text
docs/audit-papers/PASS3-BATCH2-INGEST-1_batch2_pass3_research_asset_registration_report.md
docs/audit-papers/PASS3-BATCH2-PROVENANCE-1_kb47_manifest_canonical_source_realign_report.md
docs/audit-papers/PASS3-BATCH2-FRAME-INDEX-1_batch2_multiframe_identity_index_expansion_report.md
docs/audit-papers/PASS3-BATCH2-FRAME-INDEX-2_remaining_single_frame_batch2_identity_index_expansion_report.md
docs/audit-papers/BATCH2-PROMOTION-READINESS-1_batch2_indexed_frame_promotion_readiness_review.md
docs/audit-papers/BATCH2-MEDREVIEW-1_androgen_panel_medical_review.md
docs/audit-papers/BATCH2-CONTEXT-MOD-1_androgen_panel_context_modifier_binding.md
```

Also inspect:

```text
knowledge_bus/packages/pkg_kb47_*
backend/scripts/validate_knowledge_package.py
backend/scripts/run_architecture_validation_gate.py
```

---

## Required decision

This sprint must produce one final Batch 2 promotion decision.

Allowed final decision values:

```text
PROCEED_TO_PROMOTION_WITH_CLEARED_SUBSET
PAUSE_BATCH2_PROMOTION_PENDING_BLOCKERS
DO_NOT_PROMOTE_BATCH2_AT_THIS_STAGE
```

Expected likely outcome:

```text
PROCEED_TO_PROMOTION_WITH_CLEARED_SUBSET
```

where blocked items are excluded from the promotion sprint.

---

## Required package classifications

Every one of the 20 Batch 2 packages must be placed into one of these final groups:

```text
CLEARED_FOR_BATCH2_PROMOTE_1
EXCLUDE_ANDROGEN_PENDING_CLINICAL_SIGNOFF
EXCLUDE_EGFR_PENDING_CREATININE_EGFR_ADJUDICATION
EXCLUDE_PENDING_CONTEXT_RUNTIME_EVALUATION
EXCLUDE_OTHER_BLOCKER
```

Do not create more groups unless absolutely necessary.

---

## Required consolidation questions

Answer explicitly:

```text
1. Are all 20 Batch 2 packages validated?
2. Are all 20 package manifests provenance-corrected to canonical Batch_2_Pass_3.json?
3. Are all 16 Batch 2 signal families indexed?
4. Are all Batch 2 frames present in the generated biomarker tree?
5. Which packages are cleared for BATCH2-PROMOTE-1?
6. Which packages are excluded and why?
7. Are androgen packages still blocked?
8. Are thyroid packages allowed into the cautious promotion wave or excluded?
9. Are eGFR packages excluded due to creatinine/eGFR adjudication?
10. Is any further review required before promotion of the cleared subset?
```

---

## Expected decision logic

Use this default unless evidence proves otherwise:

### Cleared candidates

Consider clearing:

```text
creatine_kinase packages
eosinophil_pct packages
eosinophils_abs packages
free_t3 packages, if thyroid caution is accepted
free_t4 packages, if thyroid caution is accepted
```

### Exclude androgen

Exclude:

```text
dhea packages
fai packages
free_testosterone packages
free_testosterone_pct packages
```

unless there is explicit clinical sign-off evidence already present.

Reason:

```text
androgen-panel frames remain dependent on clinical sign-off and future runtime context evaluation.
```

### Exclude eGFR

Exclude:

```text
egfr packages
```

unless creatinine/eGFR adjudication has been resolved.

Reason:

```text
eGFR frames overlap with existing creatinine/eGFR renal interpretation and should not be promoted until adjudicated.
```

---

## Required final decision register

Create:

```text
knowledge_bus/governance/batch2_final_promotion_decision_register_v1.yaml
```

It must include:

```yaml
schema_version:
runtime_consumed: false
status:
work_id:
source_batch:
final_decision:
package_count:
cleared_package_count:
excluded_package_count:
batch2_promote_1_scope:
  include_packages:
  exclude_packages:
packages:
  - package_id:
    package_path:
    spec_id:
    signal_id:
    primary_biomarker_id:
    medical_frame_id:
    panel_group:
    package_validator_status:
    provenance_canonical:
    frame_indexed:
    tree_visible:
    promotion_readiness_status:
    medical_review_status:
    context_binding_status:
    final_promotion_group:
    final_decision:
    blocker_if_excluded:
    required_next_action:
    notes:
```

---

## Required report

Create:

```text
docs/audit-papers/BATCH2-CLOSURE-1_final_batch2_promotion_decision.md
```

Report must include:

```text
- executive verdict
- artefacts inspected
- summary of Batch 2 work completed
- 20-package final decision table
- packages cleared for BATCH2-PROMOTE-1
- packages excluded and exact blocker
- androgen decision
- thyroid decision
- eGFR decision
- whether Batch 2 promotion can proceed
- exact scope for BATCH2-PROMOTE-1
- validation output pasted in full
- carry-forward updates
- confirmation no runtime/package/frontend changes
```

---

## Carry-forward handling

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Expected handling:

```text
CF-BATCH2-006
Resolve only if the final cleared promotion wave is defined.

CF-BATCH2-010
Remain Open unless androgen clinical sign-off is completed, which is not expected.

CF-CONTEXT-MOD-3
Remain Open unless runtime Layer B context evaluation is implemented, which is out of scope.

CF-BATCH2-007
Remain Open unless eGFR adjudication is completed, which is out of scope.

CF-BATCH2-008
Resolve only if thyroid is explicitly classified as either cleared for cautious promotion or excluded with blocker.
```

Likely new carry-forward:

```text
CF-BATCH2-011 — execute BATCH2-PROMOTE-1 for cleared package subset.
```

---

## Required validations

Run and paste actual output:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

Validate all 20 `pkg_kb47_*` packages:

```powershell
python backend/scripts/validate_knowledge_package.py --package-dir <package_dir>
```

Paste actual output or a clear per-package PASS table with command evidence.

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

Do not modify package files.

Do not activate anything.

---

## Out of scope

Do not:

```text
- promote packages
- activate packages
- retire packages
- modify package files
- modify signal_library.yaml
- modify research_brief.yaml
- implement Layer B context evaluation
- clinically sign off androgen frames
- adjudicate eGFR/creatinine
- change frontend
- change runtime behaviour
```

---

## STOP conditions

STOP and report if:

```text
1. Batch 2 package/spec/frame counts cannot be reconciled
2. any pkg_kb47 package fails validation
3. any package provenance is not canonical
4. any Batch 2 frame is missing from the frame index
5. any cleared package has unresolved blocker
6. architecture gate fails
7. any runtime/package/frontend change appears necessary
```

---

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. files inspected
3. 20-package reconciliation
4. cleared package list
5. excluded package list with blocker
6. thyroid decision
7. androgen decision
8. eGFR decision
9. final promotion decision
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
- current branch matches work/BATCH2-CLOSURE-1-final-batch2-promotion-decision
- only in-scope docs/governance/register files changed
- no package files changed
- no runtime/frontend/evaluator files changed
- no ambiguous stash exists
- all package validators pass
- architecture gate passes
```

---

## Success criteria

This sprint is complete only if:

```text
1. all 20 Batch 2 packages are reconciled
2. final Batch 2 promotion decision exists
3. cleared promotion subset is explicitly defined
4. excluded packages have exact blockers
5. thyroid decision is made
6. androgen remains appropriately blocked or explicitly cleared with evidence
7. eGFR remains appropriately blocked or explicitly cleared with evidence
8. BATCH2-PROMOTE-1 scope is clear
9. no runtime/package/frontend changes occur
10. architecture gate passes
```

```
```
