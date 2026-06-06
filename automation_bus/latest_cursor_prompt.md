---
work_id: BATCH2-PROMOTION-READINESS-1_batch2_indexed_frame_promotion_readiness_review
branch: work/BATCH2-PROMOTION-READINESS-1-batch2-indexed-frame-promotion-readiness-review
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# BATCH2-PROMOTION-READINESS-1 — Batch 2 Indexed Frame Promotion Readiness Review

## Purpose

Review all 16 Batch 2 indexed signal families / frames in one controlled promotion-readiness sprint.

This sprint must determine which Batch 2 `pkg_kb47_*` packages are ready to proceed toward governed package promotion, which require medical review, and which should remain blocked.

This is not a package-promotion sprint.

Do not activate packages.
Do not retire packages.
Do not modify runtime package logic.
Do not change frontend, SignalEvaluator, SignalRegistry, scoring, SSOT or runtime loaders.

The goal is to move out of micro-sprint mode by using the governance scaffold now in place:

```text
Batch 2 canonical research registered
→ pkg_kb47 provenance corrected
→ all Batch 2 frames indexed
→ biomarker tree regenerated
→ architecture gate active
→ now assess promotion readiness for the whole Batch 2 estate
````

---

## Strategic framing

The previous Batch 2 work has brought Batch 2 into line with the wider Pass_3 architecture.

Current known state:

```text
- Batch_2_Pass_3.json is canonical and validated
- 20 Batch 2 specs validated
- 20 pkg_kb47_* manifests realigned to canonical Batch_2_Pass_3.json
- all 16 Batch 2 signal families are now indexed
- all Batch 2 frames are currently compiled_not_promoted / inactive / required_before_activation
- androgen-panel frames require explicit medical-review caution
```

This sprint should produce the decision map for what can move forward next.

It must not turn each individual marker into a separate sprint unless evidence shows that is necessary.

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
PASS3-BATCH2-INGEST-1 merged
PASS3-BATCH2-PROVENANCE-1 merged
PASS3-BATCH2-FRAME-INDEX-1 merged
PASS3-BATCH2-FRAME-INDEX-2 merged
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
change_type: CONTENT
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint makes promotion-readiness decisions for a full group of medically governed packages. It must not alter runtime, but its outputs will govern future promotion and activation work.

---

## Required inputs

Read before work:

```text
knowledge_bus/research/investigation_specs/multi_llm_research/Batch_2_Pass_3.json
knowledge_bus/governance/pass3_batch2_research_asset_register_v1.yaml
knowledge_bus/governance/pass3_batch2_kb47_manifest_realign_register_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/medical_frame_identity_expansion_candidates_v1.yaml
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
docs/audit-papers/PASS3-BATCH2-INGEST-1_batch2_pass3_research_asset_registration_report.md
docs/audit-papers/PASS3-BATCH2-PROVENANCE-1_kb47_manifest_canonical_source_realign_report.md
docs/audit-papers/PASS3-BATCH2-FRAME-INDEX-1_batch2_multiframe_identity_index_expansion_report.md
docs/audit-papers/PASS3-BATCH2-FRAME-INDEX-2_remaining_single_frame_batch2_identity_index_expansion_report.md
docs/architecture/biomarker_medical_frame_tree.md
docs/sprints/launch_core_carry_forward_register.md
```

Also inspect:

```text
knowledge_bus/packages/pkg_kb47_*
backend/scripts/validate_knowledge_package.py
backend/scripts/run_architecture_validation_gate.py
```

---

## Required scope

Review all Batch 2 / `pkg_kb47_*` packages and indexed frames.

Expected package/spec count:

```text
20 pkg_kb47_* packages
20 Batch 2 specs
16 Batch 2 signal families
```

Confirm actual counts from repo evidence.

Do not restrict this to androgen-only review.

Do not split thyroid, androgen, eosinophil, renal, CK, or other Batch 2 groups into separate sprints unless the audit proves they need separate follow-up.

---

## Required readiness classifications

For every Batch 2 package/frame, assign one promotion-readiness status:

```text
READY_FOR_PROMOTION_CANDIDATE
READY_WITH_DOCUMENTED_CAUTION
BLOCKED_PENDING_MEDICAL_REVIEW
BLOCKED_PENDING_FRAME_ADJUDICATION
BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING
BLOCKED_PENDING_PROVENANCE_OR_VALIDATION
DUPLICATE_OR_OVERLAP_REVIEW_REQUIRED
```

Definitions:

### READY_FOR_PROMOTION_CANDIDATE

Use only where:

```text
- Batch 2 spec is valid
- pkg_kb47 package exists
- manifest provenance points to canonical Batch_2_Pass_3.json
- frame is indexed
- no medical-review caution is flagged
- no activation-key or frame collision exists
- no known context modifier dependency blocks promotion
```

### READY_WITH_DOCUMENTED_CAUTION

Use where technically ready, but promotion should retain clear non-runtime caution notes.

### BLOCKED_PENDING_MEDICAL_REVIEW

Use for androgen-panel frames and any other frame where medical truth, interpretation, or safety cannot be accepted by architecture alone.

### BLOCKED_PENDING_FRAME_ADJUDICATION

Use where signal identity or frame overlap needs architecture/clinical adjudication.

### BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING

Use where the frame is heavily dependent on questionnaire/medication context before useful interpretation.

### BLOCKED_PENDING_PROVENANCE_OR_VALIDATION

Use only if package/spec validation or canonical provenance is not clean.

### DUPLICATE_OR_OVERLAP_REVIEW_REQUIRED

Use if the Batch 2 frame appears to duplicate an existing indexed or runtime-active frame.

---

## Required grouping

Group the Batch 2 estate into sensible promotion waves.

Expected grouping may include:

```text
Wave A — technically clean promotion candidates
Wave B — thyroid-panel cautious candidates
Wave C — androgen-panel medical-review required
Wave D — multi-frame / adjudication required
Wave E — blocked / duplicate / provenance issues
```

Cursor must derive the final waves from evidence, not assume this list.

---

## Required androgen-panel handling

For at least these families:

```text
dhea
fai
free_testosterone
free_testosterone_pct
```

The sprint must explicitly answer:

```text
1. Which androgen-panel frames exist?
2. Which package/spec supports each frame?
3. Why medical review is required before promotion readiness.
4. Whether they should be excluded from the first promotion wave.
5. What exact decision is required before they can move forward.
```

Do not clear androgen-panel medical review in this sprint.

Do not mark androgen frames as safe for promotion unless there is explicit medical-review evidence already present in repo governance.

---

## Required thyroid-panel handling

For:

```text
free_t3
free_t4
```

The sprint must explicitly answer:

```text
1. Which thyroid-panel frames exist?
2. Whether package/spec/provenance/index evidence is complete.
3. Whether these are promotion candidates or require medical review.
4. Whether they should be grouped separately from androgen frames.
```

---

## Required multi-frame handling

For Batch 2 multi-frame families already indexed in `PASS3-BATCH2-FRAME-INDEX-1`:

```text
creatine_kinase
egfr
eosinophil_pct
eosinophils_abs
```

The sprint must explicitly answer:

```text
1. Are the frames distinct and correctly indexed?
2. Are there activation-key collisions?
3. Do they require frame adjudication before promotion?
4. Are any eligible for a first promotion candidate wave?
```

---

## Required readiness table

Create a full Batch 2 readiness table covering every `pkg_kb47_*` package:

```yaml
package_id:
package_path:
spec_id:
signal_id:
primary_biomarker_id:
signal_family_id:
medical_frame_id:
panel_group:
batch2_spec_valid:
manifest_provenance_canonical:
package_validator_status:
frame_indexed:
activation_key:
collision_status:
clinical_adjudication_status:
context_modifier_dependency:
promotion_readiness_status:
recommended_wave:
recommended_next_action:
medical_review_required:
notes:
```

Allowed `panel_group` values:

```text
renal
muscle_injury
eosinophil
thyroid
androgen
other
```

Allowed `recommended_wave` values:

```text
Wave_A_first_promotion_candidates
Wave_B_cautious_promotion_candidates
Wave_C_medical_review_required
Wave_D_frame_adjudication_required
Wave_E_blocked_or_duplicate
```

---

## Required artefacts

Create:

```text
docs/audit-papers/BATCH2-PROMOTION-READINESS-1_batch2_indexed_frame_promotion_readiness_review.md
knowledge_bus/governance/batch2_promotion_readiness_register_v1.yaml
```

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Do not update:

```text
knowledge_bus/packages/*
knowledge_bus/current/latest_knowledge_status.json
```

Do not update the frame index unless correcting a documentation-only typo found during review and explicitly justified.

Do not regenerate the tree unless the frame index changes, which is not expected.

---

## Required register content

`batch2_promotion_readiness_register_v1.yaml` must include:

```yaml
schema_version:
runtime_consumed: false
status:
work_id:
source_batch:
package_count:
summary_counts:
  READY_FOR_PROMOTION_CANDIDATE:
  READY_WITH_DOCUMENTED_CAUTION:
  BLOCKED_PENDING_MEDICAL_REVIEW:
  BLOCKED_PENDING_FRAME_ADJUDICATION:
  BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING:
  BLOCKED_PENDING_PROVENANCE_OR_VALIDATION:
  DUPLICATE_OR_OVERLAP_REVIEW_REQUIRED:
promotion_waves:
  Wave_A_first_promotion_candidates:
  Wave_B_cautious_promotion_candidates:
  Wave_C_medical_review_required:
  Wave_D_frame_adjudication_required:
  Wave_E_blocked_or_duplicate:
packages:
  - package_id:
    package_path:
    spec_id:
    signal_id:
    primary_biomarker_id:
    signal_family_id:
    medical_frame_id:
    panel_group:
    batch2_spec_valid:
    manifest_provenance_canonical:
    package_validator_status:
    frame_indexed:
    activation_key:
    collision_status:
    clinical_adjudication_status:
    context_modifier_dependency:
    promotion_readiness_status:
    recommended_wave:
    recommended_next_action:
    medical_review_required:
    notes:
```

---

## Required validations

Run and paste actual output:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

Validate all 20 `pkg_kb47_*` packages using repo-standard package validation.

If batch package validation is not available, loop through each package and run:

```powershell
python backend/scripts/validate_knowledge_package.py --package-dir <package_dir>
```

Paste actual validation output or a clear per-package PASS table with command evidence.

---

## Required report content

The report must include:

```text
- executive verdict
- artefacts inspected
- package/spec/frame counts
- full readiness methodology
- full readiness table or link to register
- Wave A/B/C/D/E summary
- androgen-panel assessment
- thyroid-panel assessment
- multi-frame family assessment
- package validation results
- architecture gate output
- promotion candidates
- blocked packages and exact blockers
- recommended next promotion sprint
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
CF-BATCH2-003
Should be marked Resolved only if this sprint completes promotion-readiness review for all Batch 2 frames.

CF-BATCH2-005
Should remain Open unless medical review of androgen-panel frames is completed, which is not expected in this sprint.

Possible new carry-forward:
CF-BATCH2-006 — promote Wave A Batch 2 candidates.
CF-BATCH2-007 — adjudicate Wave D multi-frame candidates.
CF-BATCH2-008 — thyroid-panel cautious promotion or review.
```

Do not mark package promotion complete.

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

## Out of scope

Do not:

```text
- modify package manifests
- modify signal_library.yaml
- modify research_brief.yaml
- promote packages
- activate packages
- retire packages
- implement Layer B frame assembly
- implement context modifier evaluation
- change frontend
- adjudicate androgen medical truth
- change frame index except justified documentation-only correction
```

---

## STOP conditions

STOP and report if:

```text
1. Batch 2 package/spec/frame counts cannot be reconciled
2. any pkg_kb47 package fails validation
3. any package provenance is not canonical
4. any Batch 2 frame is missing from the frame index
5. readiness classification requires clinical judgement beyond available governance
6. architecture gate fails
7. any runtime/package/frontend change appears necessary
```

---

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. files inspected
3. Batch 2 package/spec/frame counts
4. package validation evidence
5. readiness classification counts
6. wave grouping summary
7. androgen-panel handling
8. thyroid-panel handling
9. multi-frame handling
10. governance files created/updated
11. carry-forward updates
12. actual validation output
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
- current branch matches work/BATCH2-PROMOTION-READINESS-1-batch2-indexed-frame-promotion-readiness-review
- only in-scope docs/governance/register files changed
- no runtime package files changed
- no frontend/runtime evaluator files changed
- no ambiguous stash exists
- all package validators pass
- architecture gate passes
```

---

## Success criteria

This sprint is complete only if:

```text
1. all 20 Batch 2 packages are reviewed
2. every package has a promotion-readiness classification
3. Wave A/B/C/D/E groupings are produced
4. androgen-panel frames remain medical-review gated
5. thyroid-panel frames are explicitly assessed
6. multi-frame families are explicitly assessed
7. package validators pass
8. architecture gate passes
9. CF-BATCH2-003 is accurately updated
10. no runtime/package/frontend changes occur
```

```
```
