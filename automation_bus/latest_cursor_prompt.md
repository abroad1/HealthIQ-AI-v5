---
work_id: BATCH2-REMAINDER-RESOLUTION-1_remaining_batch2_package_resolution_investigation
branch: work/BATCH2-REMAINDER-RESOLUTION-1-remaining-batch2-package-resolution-investigation
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# BATCH2-REMAINDER-RESOLUTION-1 — Remaining Batch 2 Package Resolution Investigation

## Purpose

Investigate all remaining non-active Batch 2 packages and produce a complete, evidence-grounded resolution plan that enables GPT to author the final execution work package for promotion / activation.

This is an investigation and decision-preparation sprint only.

Do not promote packages.
Do not activate packages.
Do not change runtime behaviour.
Do not modify package logic.
Do not modify frontend, evaluator, loader, scoring, SSOT, thresholds or clinical wording.

The goal is to leave no unanswered question about the remaining Batch 2 packages.

Current known Batch 2 state:

```text
Runtime active:
- creatine_kinase ×2
- eosinophil_pct ×2
- eosinophils_abs ×2

Governance-promoted but runtime-deferred:
- free_t3 ×2
- free_t4 ×2

Still blocked:
- androgen ×8
- eGFR ×2
````

The latest activation audit confirms this split: 6 runtime-active, 4 thyroid deferred, 8 androgen excluded, and 2 eGFR excluded. 

---

## Strategic framing

This sprint must not create another chain of micro-sprints.

It must answer every remaining question needed to decide the fate of the remaining 14 Batch 2 packages:

```text
4 thyroid packages
8 androgen packages
2 eGFR packages
```

Each package must end this investigation with one of these recommendations:

```text
READY_FOR_EXECUTION_PROMOTION_OR_ACTIVATION
READY_FOR_EXECUTION_WITH_RUNTIME_GATE
FORMALLY_BLOCKED_PENDING_SPECIFIC_PREREQUISITE
REQUIRES_MEDICAL_RESEARCH_REVIEW
REQUIRES_ARCHITECTURAL_AUTHORITY_DECISION
DO_NOT_PROMOTE
```

The output must be detailed enough that GPT can write the next execution sprint without asking Cursor to rediscover the same facts again.

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
BATCH2-ACTIVATION-1 merged
BATCH2-PROMOTE-1 merged
BATCH2-CLOSURE-1 merged
BATCH2-CONTEXT-MOD-1 merged
BATCH2-MEDREVIEW-1 merged
BATCH2-PROMOTION-READINESS-1 merged
PASS3-BATCH2-FRAME-INDEX-1 merged
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
- Batch 2 activation register is missing
- Batch 2 final promotion decision register is missing
- medical frame identity index is missing
- context modifier catalogue is missing
```

---

## Required inputs

Read all of the following before producing findings:

```text
knowledge_bus/governance/batch2_runtime_activation_execution_register_v1.yaml
knowledge_bus/governance/batch2_promote_1_execution_register_v1.yaml
knowledge_bus/governance/batch2_final_promotion_decision_register_v1.yaml
knowledge_bus/governance/batch2_promotion_readiness_register_v1.yaml
knowledge_bus/governance/batch2_androgen_panel_medical_review_v1.yaml
knowledge_bus/governance/batch2_androgen_context_modifier_binding_v1.yaml
knowledge_bus/governance/pass3_batch2_research_asset_register_v1.yaml
knowledge_bus/governance/pass3_batch2_kb47_manifest_realign_register_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
knowledge_bus/current/latest_knowledge_status.json
docs/Medical Research Documents/thyroid_blood_marker_interpretation_clinical_signoff.md
docs/audit-papers/BATCH2-ACTIVATION-1_runtime_activate_cleared_non_thyroid_subset.md
docs/audit-papers/BATCH2-PROMOTE-1_cleared_wave_package_promotion.md
docs/audit-papers/BATCH2-CLOSURE-1_final_batch2_promotion_decision.md
docs/audit-papers/BATCH2-CONTEXT-MOD-1_androgen_panel_context_modifier_binding.md
docs/audit-papers/BATCH2-MEDREVIEW-1_androgen_panel_medical_review.md
docs/sprints/launch_core_carry_forward_register.md
```

Also inspect the remaining package folders:

```text
knowledge_bus/packages/pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis/
knowledge_bus/packages/pkg_kb47_free_t3_low_low_t3_syndrome/
knowledge_bus/packages/pkg_kb47_free_t4_high_thyrotoxicosis_context/
knowledge_bus/packages/pkg_kb47_free_t4_low_thyroid_hormone_deficiency/

knowledge_bus/packages/pkg_kb47_dhea_high_androgen_excess_context/
knowledge_bus/packages/pkg_kb47_dhea_low_adrenal_androgen_reduction/
knowledge_bus/packages/pkg_kb47_fai_high_biochemical_hyperandrogenism/
knowledge_bus/packages/pkg_kb47_fai_low_reduced_free_androgen_availability/
knowledge_bus/packages/pkg_kb47_free_testosterone_high_androgen_excess_context/
knowledge_bus/packages/pkg_kb47_free_testosterone_low_androgen_deficiency_context/
knowledge_bus/packages/pkg_kb47_free_testosterone_pct_high_elevated_free_androgen_fraction/
knowledge_bus/packages/pkg_kb47_free_testosterone_pct_low_reduced_free_androgen_fraction/

knowledge_bus/packages/pkg_kb47_egfr_low_chronic_kidney_function_reduction/
knowledge_bus/packages/pkg_kb47_egfr_low_hemodynamic_filtration_drop/
```

---

## Remaining packages in scope

### Thyroid — 4 packages

```text
pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis
pkg_kb47_free_t3_low_low_t3_syndrome
pkg_kb47_free_t4_high_thyrotoxicosis_context
pkg_kb47_free_t4_low_thyroid_hormone_deficiency
```

### Androgen — 8 packages

```text
pkg_kb47_dhea_high_androgen_excess_context
pkg_kb47_dhea_low_adrenal_androgen_reduction
pkg_kb47_fai_high_biochemical_hyperandrogenism
pkg_kb47_fai_low_reduced_free_androgen_availability
pkg_kb47_free_testosterone_high_androgen_excess_context
pkg_kb47_free_testosterone_low_androgen_deficiency_context
pkg_kb47_free_testosterone_pct_high_elevated_free_androgen_fraction
pkg_kb47_free_testosterone_pct_low_reduced_free_androgen_fraction
```

### eGFR — 2 packages

```text
pkg_kb47_egfr_low_chronic_kidney_function_reduction
pkg_kb47_egfr_low_hemodynamic_filtration_drop
```

Do not include the already-active 6 non-thyroid packages except for confirming they are out of scope.

---

## Investigation questions — answer all

### A. Whole remaining Batch 2 estate

For each of the 14 remaining packages, answer:

```text
1. Is the package governance-promoted?
2. Is the package runtime-active?
3. Is the package provenance canonical?
4. Is the package indexed in the medical frame identity index?
5. Does the package validate?
6. What blocker currently prevents activation?
7. Is that blocker medical, architectural, runtime-gating, or context-modifier related?
8. Can the blocker be resolved inside a single future execution sprint?
9. What exact precondition must be satisfied before activation?
10. Recommended final action.
```

### B. Thyroid-specific questions

For each thyroid package, answer:

```text
1. What does the thyroid clinical sign-off require?
2. Is TSH currently available to the runtime signal evaluation path?
3. Can TSH gating be implemented using existing runtime architecture without code changes?
4. If code changes are required, where would they be needed?
5. Can FT3 high be activated with mandatory TSH suppression gating?
6. Can FT3 low be activated only with TSH + FT4 + illness/medication context?
7. Can FT4 high be activated with mandatory TSH low/suppressed gating?
8. Can FT4 low be activated with mandatory TSH interpretation gating?
9. Are medication/supplement caveats represented anywhere in context governance?
10. What is the exact execution path to activate each thyroid package safely?
```

Thyroid must not be recommended for activation unless the investigation proves that mandatory TSH gating can be enforced.

### C. Androgen-specific questions

For each androgen package, answer:

```text
1. What context dependencies were identified in the androgen medical review?
2. Are the necessary context modifiers now present in the context modifier catalogue?
3. Are those modifiers runtime-consumed or only governance placeholders?
4. Is sex context available at runtime?
5. Is age context available at runtime?
6. Is SHBG available as a biomarker input or modifier?
7. Is hormone medication context available at runtime?
8. Is steroid / supplement exposure context available at runtime?
9. Can these packages be safely activated without Layer B context evaluation?
10. If not, what exactly must be built first?
11. Are any androgen packages safe to activate as context-gated/inactive-until-context-present?
12. Or should all 8 remain formally blocked?
```

Do not recommend androgen activation unless the required context dependencies can be enforced by current runtime architecture or a clearly defined gated execution path.

### D. eGFR-specific questions

For each eGFR package, answer:

```text
1. What is the package’s intended interpretation?
2. How does it overlap with the existing creatinine-high / eGFR escalation frame?
3. Is eGFR represented as its own signal family in the medical frame identity index?
4. Is eGFR also present as supporting or escalation evidence under creatinine?
5. Would activating eGFR create duplicate renal dysfunction signalling?
6. Are there existing anti-double-counting rules?
7. If not, where would those rules need to live?
8. Should eGFR be activated as an independent renal signal?
9. Should eGFR remain supporting evidence under creatinine only?
10. Can both exist safely with authority/collision rules?
11. Is medical research input needed, or is this an architecture authority decision?
12. What exact execution path is required?
```

Do not recommend eGFR activation unless duplicate renal interpretation risk is resolved or clearly gateable.

---

## Required output classifications

For every package, assign:

```yaml
package_id:
package_path:
panel_group:
spec_id:
signal_id:
medical_frame_id:
current_state:
  governance_promoted:
  runtime_active:
  indexed:
  provenance_canonical:
  validates:
blocking_status:
  blocker_type:
  blocker_description:
  blocker_source:
  can_resolve_in_next_execution_sprint:
required_before_activation:
recommended_next_action:
final_recommendation:
```

Allowed `blocker_type` values:

```text
none
thyroid_tsh_gating_required
thyroid_tsh_ft4_context_required
androgen_context_runtime_required
androgen_clinical_signoff_required
renal_authority_adjudication_required
anti_double_counting_required
runtime_architecture_gap
medical_research_required
unknown_blocker
```

Allowed `final_recommendation` values:

```text
READY_FOR_NEXT_EXECUTION_SPRINT
READY_IF_RUNTIME_GATE_IMPLEMENTED
FORMALLY_BLOCKED_KEEP_INACTIVE
REQUIRES_MEDICAL_RESEARCH_REVIEW
REQUIRES_ARCHITECTURE_AUTHORITY_DECISION
DO_NOT_PROMOTE_OR_ACTIVATE
```

---

## Required artefacts

Create:

```text
docs/audit-papers/BATCH2-REMAINDER-RESOLUTION-1_remaining_batch2_package_resolution_investigation.md
knowledge_bus/governance/batch2_remainder_resolution_register_v1.yaml
```

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Do not modify:

```text
knowledge_bus/packages/*
knowledge_bus/current/latest_knowledge_status.json
medical_frame_identity_index_v1.yaml
context_modifier_catalogue_draft_v1.yaml
runtime code
frontend code
```

This is investigation only.

---

## Required report content

The report must include:

```text
- executive verdict
- artefacts inspected
- current Batch 2 state summary
- all 14 remaining packages table
- thyroid resolution assessment
- androgen resolution assessment
- eGFR resolution assessment
- exact blockers by package
- whether medical research is still needed
- whether runtime/context architecture is still needed
- recommended next execution sprint scope
- packages that can be resolved together
- packages that must remain blocked
- validation output
- confirmation no runtime/package/frontend changes
```

---

## Required final recommendation

The report must end with one clear recommendation:

```text
Recommended next execution package:
<work_id suggestion>

Scope:
- packages to activate
- packages to keep blocked
- gates to implement
- STOP gates required
- validations required
```

The recommendation must be detailed enough for GPT to write the execution prompt directly.

---

## Carry-forward handling

Update the carry-forward register to consolidate, not fragment.

Expected handling:

```text
CF-BATCH2-013 — thyroid gating
Update with exact required implementation path.

CF-BATCH2-010 — androgen sign-off
Update with exact remaining blocker.

CF-CONTEXT-MOD-3 — runtime context evaluation
Update with whether this blocks all androgen packages.

CF-BATCH2-007 — eGFR adjudication
Update with exact authority decision required.
```

Do not create new carry-forwards unless genuinely necessary.

If a new carry-forward is required, it must consolidate work rather than split one marker into a separate sprint.

---

## Required validations

Run and paste actual output:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

Validate all 14 remaining packages:

```powershell
python backend/scripts/validate_knowledge_package.py --package-dir <package_dir>
```

A clear per-package PASS table is acceptable only if the command used is stated.

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

If investigation reveals runtime code will be needed in a future sprint, document it. Do not implement it.

---

## Out of scope

Do not:

```text
- activate packages
- promote packages
- modify package manifests
- modify signal_library.yaml
- modify research_brief.yaml
- modify frame index
- modify context catalogue
- implement TSH gating
- implement Layer B context evaluation
- adjudicate eGFR authority by changing files
- change frontend
- change runtime behaviour
```

---

## STOP conditions

STOP and report if:

```text
1. any required Batch 2 governance register cannot be found
2. package counts cannot be reconciled
3. current runtime-active state cannot be determined
4. activation blockers cannot be traced to source evidence
5. package validators fail
6. architecture gate fails
7. investigation would require code/package changes
```

---

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. files inspected
3. current state for all 14 packages
4. blocker classification for every package
5. thyroid gating findings
6. androgen context/runtime findings
7. eGFR authority findings
8. package validation evidence
9. architecture gate output
10. governance files created/updated
11. carry-forward updates
12. recommended next execution sprint
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
- current branch matches work/BATCH2-REMAINDER-RESOLUTION-1-remaining-batch2-package-resolution-investigation
- only docs/governance/register files changed
- no package files changed
- no runtime/frontend/evaluator files changed
- no ambiguous stash exists
- validators pass
- architecture gate passes
```

---

## Success criteria

This sprint is complete only if:

```text
1. all 14 remaining Batch 2 packages are investigated
2. every package has a blocker classification
3. thyroid has a concrete gating path or remains formally blocked
4. androgen has a concrete context-runtime path or remains formally blocked
5. eGFR has a concrete authority path or remains formally blocked
6. medical research gaps are explicitly identified or ruled out
7. recommended next execution sprint scope is clear
8. no runtime/package/frontend changes occur
9. architecture gate passes
10. no orphaned Batch 2 packages remain unexplained
```

```
```
