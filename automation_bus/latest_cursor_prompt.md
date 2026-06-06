---
work_id: BATCH2-CONTEXT-MOD-1_androgen_panel_context_modifier_binding
branch: work/BATCH2-CONTEXT-MOD-1-androgen-panel-context-modifier-binding
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# BATCH2-CONTEXT-MOD-1 — Androgen-Panel Context Modifier Binding

## Purpose

Bind the Batch 2 androgen-panel frames to the governed context-modifier architecture before any future promotion or activation work.

This sprint addresses:

```text
CF-BATCH2-009 — bind androgen-panel context modifiers before promotion.
````

It must also address the audit observation from `BATCH2-MEDREVIEW-1`:

```text
batch2_promotion_readiness_register_v1.yaml currently has context_modifier_dependency: false for androgen-panel entries, but the medical review found all 8 androgen-panel frames are context-dependent.
```

This sprint must correct that governance inconsistency.

This is not a package-promotion sprint.

Do not activate packages.
Do not promote packages.
Do not retire packages.
Do not modify package logic.
Do not modify runtime, frontend, SignalEvaluator, SignalRegistry, SSOT, scoring or runtime loaders.

---

## Strategic framing

The androgen-panel medical review concluded:

```text
- all 8 androgen-panel frames are medically meaningful
- none are ready for immediate promotion
- safe interpretation depends on context such as sex, age, SHBG, medication, supplements and symptoms
- FAI and free testosterone percentage frames are especially dependent on context binding
```

This sprint must ensure the governance layer reflects that dependency before any future promotion action.

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
BATCH2-MEDREVIEW-1 merged
BATCH2-PROMOTION-READINESS-1 merged
PASS3-BATCH2-FRAME-INDEX-2 merged
PASS3-BATCH2-PROVENANCE-1 merged
CONTEXT-MOD-1 merged
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
- batch2_androgen_panel_medical_review_v1.yaml is missing
- batch2_promotion_readiness_register_v1.yaml is missing
- context_modifier_catalogue_draft_v1.yaml is missing
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

This sprint updates governed context-modifier and promotion-readiness metadata for hormone/androgen frames. It must not alter runtime behaviour, but it affects future promotion safety.

---

## Required inputs

Read before work:

```text
knowledge_bus/governance/batch2_androgen_panel_medical_review_v1.yaml
knowledge_bus/governance/batch2_promotion_readiness_register_v1.yaml
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/pass3_batch2_research_asset_register_v1.yaml
docs/audit-papers/BATCH2-MEDREVIEW-1_androgen_panel_medical_review.md
docs/audit-papers/BATCH2-PROMOTION-READINESS-1_batch2_indexed_frame_promotion_readiness_review.md
docs/architecture/CONTEXT-MOD-1_questionnaire_and_medication_modifier_governance.md
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

Apply context-modifier governance to these 8 androgen-panel frames:

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

Do not review thyroid, eGFR, creatine kinase or eosinophil frames in this sprint except where needed for consistency checks.

---

## Required correction

Update:

```text
knowledge_bus/governance/batch2_promotion_readiness_register_v1.yaml
```

For all 8 androgen-panel entries, set:

```yaml
context_modifier_dependency: true
```

Do not otherwise alter their promotion-readiness status unless the change is required to preserve consistency with `batch2_androgen_panel_medical_review_v1.yaml`.

The androgen-panel frames must remain blocked or caution-gated. Do not mark them ready for promotion.

---

## Required context modifier review

For each androgen-panel frame, determine which governed context modifiers are required or missing.

At minimum assess:

```text
- sex
- age
- SHBG
- LH / FSH if represented or missing
- symptoms if collected
- known endocrine condition if represented
- testosterone / hormone medication
- steroid use
- supplements / anabolic-androgenic exposure if represented
- thyroid context if relevant
- liver context if relevant to SHBG interpretation
```

Cursor must not invent clinical rules.

Cursor may classify missing modifiers as required future governance work.

---

## Required catalogue handling

Update:

```text
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

only if the existing catalogue lacks necessary androgen-panel modifier entries that can be added as governance placeholders without inventing clinical thresholds.

Allowed additions:

```text
- modifier placeholders for sex/age/SHBG/hormone medication/supplement context
- links from existing modifiers to androgen-panel medical_frame_ids
- non-runtime metadata only
```

Every modifier must remain:

```yaml
runtime_active: false
```

The catalogue must remain:

```yaml
runtime_consumed: false
```

Do not implement modifier evaluation.

Do not add clinical thresholds.

Do not write user-facing interpretation rules.

---

## Required frame-index handling

Update:

```text
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

only if needed to set:

```yaml
context_inputs_supported:
  questionnaire_modifiers: true
  medication_modifiers: true
```

for androgen-panel frames where context modifier links are now explicitly represented.

Do not mark clinical adjudication as complete.

Do not change:

```yaml
promotion_state
runtime_authority_status
```

unless required to keep the index internally consistent and explicitly justified.

---

## Required output register

Create:

```text
knowledge_bus/governance/batch2_androgen_context_modifier_binding_v1.yaml
```

It must include:

```yaml
schema_version:
runtime_consumed: false
status:
work_id:
source_medical_review:
frame_count:
summary:
  frames_with_context_dependency:
  frames_with_catalogue_links:
  frames_blocked_pending_context_binding:
  frames_remaining_clinical_signoff_required:
frames:
  - frame_id:
    package_id:
    signal_id:
    primary_biomarker_id:
    medical_review_outcome:
    required_context_modifiers:
    catalogue_modifier_ids:
    missing_modifier_governance:
    promotion_readiness_register_updated:
    frame_index_context_flags_updated:
    remains_blocked_for_promotion:
    required_next_action:
    notes:
```

---

## Required report

Create:

```text
docs/audit-papers/BATCH2-CONTEXT-MOD-1_androgen_panel_context_modifier_binding.md
```

Report must include:

```text
- executive verdict
- artefacts inspected
- 8-frame context dependency table
- promotion-readiness register correction
- context modifier catalogue changes
- medical frame index changes, if any
- missing modifier governance
- remaining medical sign-off requirements
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
CF-BATCH2-009
Resolve only if all 8 androgen-panel frames have context_modifier_dependency corrected and context modifier bindings/placeholders are documented.

CF-BATCH2-010
Remain Open. Clinical sign-off before activation is not completed in this sprint.

CF-BATCH2-006
Remain Open. Wave B promotion pilot is separate.

CF-BATCH2-008
Remain Open. Thyroid-panel sign-off is separate.
```

Possible new carry-forward:

```text
CF-CONTEXT-MOD-3 — implement runtime Layer B context modifier evaluation after governance binding is complete.
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

If context modifier catalogue changes are made, also run its regression tests:

```powershell
python -m pytest backend/tests/regression/test_context_modifier_catalogue.py -q
```

If frame index changes are made, also run:

```powershell
python -m pytest backend/tests/regression/test_med_frame_identity_index.py -q
```

Do not write only “all tests passed”.

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
- implement runtime context modifier evaluation
- implement Layer B frame assembly
- change frontend
- change runtime behaviour
- clinically sign off androgen frames
- review thyroid or eGFR
```

---

## STOP conditions

STOP and report if:

```text
1. any androgen frame cannot be found in the medical review register
2. any androgen frame cannot be found in the promotion readiness register
3. context modifier catalogue cannot support required placeholder/binding structure
4. validator fails after catalogue/index updates
5. any package/runtime/frontend change appears necessary
6. architecture gate fails
```

---

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. files inspected
3. 8 androgen frames reviewed for context dependency
4. promotion-readiness register corrections
5. context modifier catalogue changes
6. frame index changes, if any
7. binding register created
8. carry-forward updates
9. actual validation output
10. confirmation no runtime/package/frontend changes
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
- current branch matches work/BATCH2-CONTEXT-MOD-1-androgen-panel-context-modifier-binding
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
1. all 8 androgen-panel context_modifier_dependency flags are corrected to true
2. required context modifiers are documented per frame
3. context catalogue links/placeholders exist where safe
4. androgen frames remain blocked/caution-gated for promotion
5. CF-BATCH2-009 is accurately updated
6. CF-BATCH2-010 remains open
7. validators pass
8. architecture gate passes
9. no runtime/package/frontend changes occur
10. next path toward clinical sign-off is clear
```

```
```
