---
work_id: BATCH2-MEDREVIEW-1_androgen_panel_medical_review
branch: work/BATCH2-MEDREVIEW-1-androgen-panel-medical-review
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# BATCH2-MEDREVIEW-1 — Batch 2 Androgen-Panel Medical Review

## Purpose

Carry out a focused medical/governance review of the Batch 2 androgen-panel frames before any promotion readiness or package activation work proceeds.

This sprint addresses:

```text
CF-BATCH2-005 — medical review of androgen-panel Batch 2 frames before promotion readiness.
````

The androgen-panel frames are already indexed, provenance-corrected, and marked:

```yaml
promotion_state: compiled_not_promoted
runtime_authority_status: inactive
clinical_adjudication_status: required_before_activation
```

This sprint must decide whether each androgen-panel frame can move from medical-review blocked to promotion-readiness eligible, or whether it remains blocked.

This is not a package-promotion sprint.

Do not activate packages.
Do not retire packages.
Do not modify runtime package logic.
Do not modify frontend, SignalEvaluator, SignalRegistry, scoring, SSOT or runtime loaders.

---

## Strategic framing

The Batch 2 readiness review grouped the estate as:

```text
Wave B — cautious candidates
Wave C — androgen-panel medical-review required
Wave D — eGFR frame adjudication required
```

This sprint focuses only on Wave C androgen-panel review.

The goal is not to decide user-facing claims or write final product copy.

The goal is to determine whether the underlying Pass_3 frame structure is medically coherent enough for future promotion work.

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
BATCH2-PROMOTION-READINESS-1 merged
PASS3-BATCH2-FRAME-INDEX-2 merged
PASS3-BATCH2-PROVENANCE-1 merged
PASS3-BATCH2-INGEST-1 merged
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
- batch2_promotion_readiness_register_v1.yaml is missing
- medical_frame_identity_index_v1.yaml is missing
```

---

## Governance classification

```yaml
risk_level: HIGH
change_type: CONTENT
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint reviews medical-intelligence suitability for hormone/androgen-related frames. It must not change runtime behaviour, but it affects future package promotion decisions.

---

## Required inputs

Read before work:

```text
knowledge_bus/research/investigation_specs/multi_llm_research/Batch_2_Pass_3.json
knowledge_bus/governance/pass3_batch2_research_asset_register_v1.yaml
knowledge_bus/governance/batch2_promotion_readiness_register_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
knowledge_bus/governance/pass3_batch2_kb47_manifest_realign_register_v1.yaml
docs/audit-papers/BATCH2-PROMOTION-READINESS-1_batch2_indexed_frame_promotion_readiness_review.md
docs/sprints/launch_core_carry_forward_register.md
```

Also inspect:

```text
knowledge_bus/packages/pkg_kb47_dhea_*
knowledge_bus/packages/pkg_kb47_fai_*
knowledge_bus/packages/pkg_kb47_free_testosterone_*
knowledge_bus/packages/pkg_kb47_free_testosterone_pct_*
```

---

## Scope

Review the 8 androgen-panel Batch 2 frames:

```text
dhea_high_androgen_excess_context
dhea_low_adrenal_androgen_reduction
fai_high_biochemical_hyperandrogenism
fai_low_reduced_free_androgen_availability
free_testosterone_high_androgen_excess_context
free_testosterone_low_androgen_deficiency_context
free_testosterone_pct_high_elevated_free_androgen_fraction
free_testosterone_pct_low_reduced_free_androgen_fraction
```

Do not review thyroid, eGFR, creatine kinase or eosinophil frames in this sprint except where needed for comparison.

---

## Medical review boundary

Cursor must not independently invent clinical claims.

Cursor may:

```text
- compare Pass_3 content against package artefacts
- identify whether the frame is internally coherent
- identify missing context/modifier dependencies
- classify whether medical review remains required
- recommend whether future promotion should proceed, proceed with caution, or remain blocked
```

Cursor must not:

```text
- invent thresholds
- change medical claims
- decide final clinical truth without source support
- write user-facing medical advice
- activate packages
- change signal logic
```

---

## Required review questions

For each of the 8 frames, answer:

```text
1. Is the frame medically coherent as written in Batch_2_Pass_3.json?
2. Is the direction high/low clinically plausible and internally consistent?
3. Are primary marker, supporting markers and context markers clearly separated?
4. Does the frame require sex, age, medication, supplement, symptom or known-condition context before interpretation?
5. Are any key contradiction markers or caveats missing?
6. Is the package compiled and provenance-corrected?
7. Is the frame already indexed correctly?
8. Is this frame ready to move to promotion-readiness candidate status?
9. If not, what exact blocker remains?
```

---

## Required classification

Assign one review outcome per frame:

```text
MEDICALLY_COHERENT_READY_WITH_CAUTION
MEDICALLY_COHERENT_BUT_CONTEXT_DEPENDENT
BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING
BLOCKED_PENDING_MEDICAL_RESEARCH_ENRICHMENT
BLOCKED_PENDING_CLINICAL_SIGNOFF
POSSIBLE_DUPLICATE_OR_OVERLAP_REVIEW_REQUIRED
```

Definitions:

### MEDICALLY_COHERENT_READY_WITH_CAUTION

Use only where the frame appears coherent, bounded and not critically dependent on missing context.

### MEDICALLY_COHERENT_BUT_CONTEXT_DEPENDENT

Use where the frame is valid but interpretation clearly depends on sex/age/medication/supplement/symptom context.

### BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING

Use where promotion should wait until relevant context modifiers are connected to the frame.

### BLOCKED_PENDING_MEDICAL_RESEARCH_ENRICHMENT

Use where the research frame itself appears incomplete.

### BLOCKED_PENDING_CLINICAL_SIGNOFF

Use where architecture can classify the frame but clinical sign-off is still required.

### POSSIBLE_DUPLICATE_OR_OVERLAP_REVIEW_REQUIRED

Use where DHEA / FAI / free testosterone / free testosterone % overlap creates risk of duplicate androgen interpretation.

---

## Required output register

Create:

```text
knowledge_bus/governance/batch2_androgen_panel_medical_review_v1.yaml
```

It must include:

```yaml
schema_version:
runtime_consumed: false
status:
work_id:
review_scope:
source_batch:
frame_count:
summary_counts:
  MEDICALLY_COHERENT_READY_WITH_CAUTION:
  MEDICALLY_COHERENT_BUT_CONTEXT_DEPENDENT:
  BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING:
  BLOCKED_PENDING_MEDICAL_RESEARCH_ENRICHMENT:
  BLOCKED_PENDING_CLINICAL_SIGNOFF:
  POSSIBLE_DUPLICATE_OR_OVERLAP_REVIEW_REQUIRED:
frames:
  - frame_id:
    package_id:
    spec_id:
    signal_id:
    primary_biomarker_id:
    direction:
    package_path:
    frame_indexed:
    provenance_canonical:
    medical_review_outcome:
    promotion_readiness_recommendation:
    context_dependencies:
    missing_context_or_research:
    duplicate_or_overlap_risk:
    required_next_action:
    notes:
```

---

## Required report

Create:

```text
docs/audit-papers/BATCH2-MEDREVIEW-1_androgen_panel_medical_review.md
```

Report must include:

```text
- executive verdict
- artefacts inspected
- 8-frame review table
- DHEA assessment
- FAI assessment
- free testosterone assessment
- free testosterone percentage assessment
- overlap / duplicate-risk assessment
- context dependency assessment
- package/provenance validation summary
- recommended promotion-readiness status
- carry-forward updates
- validation output pasted in full
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
CF-BATCH2-005
Resolve only if all 8 androgen-panel frames have a clear medical-review outcome and exact next action.

CF-BATCH2-006
Remain Open unless Wave B promotion is started, which is out of scope.

CF-BATCH2-003
Remain Open unless this sprint completes all Batch 2 promotion readiness, which is not expected.

Possible new carry-forward:
CF-BATCH2-009 — bind androgen-panel context modifiers before promotion.
CF-BATCH2-010 — androgen-panel clinical sign-off before activation.
```

Do not mark androgen package promotion complete.

---

## Required validations

Run and paste actual output:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

Validate the 8 relevant packages:

```powershell
python backend/scripts/validate_knowledge_package.py --package-dir <package_dir>
```

Paste actual output or a clear per-package PASS table.

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

Package files must not be edited in this sprint.

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
- implement context modifier binding
- change frontend
- change runtime behaviour
- adjudicate thyroid or eGFR
```

---

## STOP conditions

STOP and report if:

```text
1. any androgen package cannot be found
2. any androgen package fails validation
3. any frame cannot be traced to Batch_2_Pass_3.json
4. review requires new medical research not present in repo
5. activation or runtime change appears necessary
6. architecture gate fails
```

---

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. files inspected
3. 8 androgen frames reviewed
4. review outcome per frame
5. package validation evidence
6. context dependency findings
7. duplicate/overlap findings
8. governance files created/updated
9. carry-forward updates
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
- current branch matches work/BATCH2-MEDREVIEW-1-androgen-panel-medical-review
- only in-scope docs/governance/register files changed
- no runtime package files changed
- no frontend/runtime evaluator files changed
- no ambiguous stash exists
- architecture gate passes
```

---

## Success criteria

This sprint is complete only if:

```text
1. all 8 androgen-panel frames are reviewed
2. each frame has a clear medical-review outcome
3. context dependencies are identified
4. overlap/duplicate risk is assessed
5. package validators pass
6. architecture gate passes
7. CF-BATCH2-005 is accurately updated
8. no runtime/package/frontend changes occur
9. next promotion-readiness path is clear
```

```
```
