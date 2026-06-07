---
work_id: BATCH2-THYROID-GATE-1_mandatory_tsh_gating_and_runtime_activation
branch: work/BATCH2-THYROID-GATE-1-mandatory-tsh-gating-and-runtime-activation
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# BATCH2-THYROID-GATE-1 — Mandatory TSH Gating and Runtime Activation

## Purpose

Implement mandatory TSH gating for the Batch 2 thyroid packages that have been clinically approved with caveats, then runtime-activate only the thyroid packages that can be safely gated.

This sprint must address the remaining thyroid Batch 2 package set in one outcome-based work package.

Do not split this into separate FT3 / FT4 / sign-off / activation sprints.

---

## Strategic framing

`BATCH2-REMAINDER-RESOLUTION-1` concluded:

```text
FT3 high, FT4 high, FT4 low:
READY_IF_RUNTIME_GATE_IMPLEMENTED

FT3 low:
FORMALLY_BLOCKED_KEEP_INACTIVE
````

The thyroid clinical sign-off stated:

```text
TSH is mandatory before all four thyroid patterns are activated.

FT3 low also requires:
- TSH
- FT4
- illness / medication context
```

Therefore, this sprint must:

```text
1. implement mandatory TSH gating for FT3 high, FT4 high and FT4 low
2. runtime-activate those 3 packages only if the gate is enforceable
3. keep FT3 low inactive
4. keep androgen and eGFR excluded
```

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
BATCH2-REMAINDER-RESOLUTION-1 merged
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
- BATCH2-REMAINDER-RESOLUTION-1 artefacts are missing
- thyroid clinical sign-off document is missing
- medical frame identity index is missing
- runtime signal gating mechanism cannot be located
```

---

## Required inputs

Read before implementation:

```text
knowledge_bus/governance/batch2_remainder_resolution_register_v1.yaml
knowledge_bus/governance/batch2_runtime_activation_execution_register_v1.yaml
knowledge_bus/governance/batch2_final_promotion_decision_register_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
docs/Medical Research Documents/thyroid_blood_marker_interpretation_clinical_signoff.md
docs/audit-papers/BATCH2-REMAINDER-RESOLUTION-1_remaining_batch2_package_resolution_investigation.md
docs/audit-papers/BATCH2-ACTIVATION-1_runtime_activate_cleared_non_thyroid_subset.md
docs/sprints/launch_core_carry_forward_register.md
```

Inspect these package folders:

```text
knowledge_bus/packages/pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis/
knowledge_bus/packages/pkg_kb47_free_t3_low_low_t3_syndrome/
knowledge_bus/packages/pkg_kb47_free_t4_high_thyrotoxicosis_context/
knowledge_bus/packages/pkg_kb47_free_t4_low_thyroid_hormone_deficiency/
```

Inspect runtime gating/evaluation code:

```text
SignalEvaluator
SignalRegistry
Knowledge Bus runtime package loader
signal evaluation rule handling
override / escalation rule handling
backend tests covering signal evaluation
```

If paths differ, locate and report actual paths.

---

## In-scope thyroid packages

### Eligible for TSH-gated activation if enforceable

```text
pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis
pkg_kb47_free_t4_high_thyrotoxicosis_context
pkg_kb47_free_t4_low_thyroid_hormone_deficiency
```

### Must remain blocked

```text
pkg_kb47_free_t3_low_low_t3_syndrome
```

Reason:

```text
FT3 low requires TSH + FT4 + illness / medication context.
Current runtime architecture does not yet support that full context pathway.
```

---

## Explicitly excluded packages

Do not modify, activate or reclassify:

```text
pkg_kb47_dhea_high_androgen_excess_context
pkg_kb47_dhea_low_adrenal_androgen_reduction
pkg_kb47_fai_high_biochemical_hyperandrogenism
pkg_kb47_fai_low_reduced_free_androgen_availability
pkg_kb47_free_testosterone_high_androgen_excess_context
pkg_kb47_free_testosterone_low_androgen_deficiency_context
pkg_kb47_free_testosterone_pct_high_elevated_free_androgen_fraction
pkg_kb47_free_testosterone_pct_low_reduced_free_androgen_fraction
pkg_kb47_egfr_low_chronic_kidney_function_reduction
pkg_kb47_egfr_low_hemodynamic_filtration_drop
```

STOP if any excluded androgen or eGFR package appears in the diff.

---

## Required clinical gating rules

The three eligible thyroid packages must not activate from isolated FT3 / FT4 abnormality.

Implement mandatory TSH gating as follows:

### FT3 high

Package:

```text
pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis
```

Required gate:

```text
Free T3 high may emit only when TSH is low/suppressed according to the available lab-specific range / abnormality logic.
```

If TSH is absent or not low/suppressed:

```text
do not emit this signal
```

### FT4 high

Package:

```text
pkg_kb47_free_t4_high_thyrotoxicosis_context
```

Required gate:

```text
Free T4 high may emit only when TSH is low/suppressed according to the available lab-specific range / abnormality logic.
```

If TSH is absent or not low/suppressed:

```text
do not emit this signal
```

### FT4 low

Package:

```text
pkg_kb47_free_t4_low_thyroid_hormone_deficiency
```

Required gate:

```text
Free T4 low may emit only when TSH is available.
```

Interpretation should remain cautious because low FT4 with non-high TSH may indicate central hypothyroidism or non-thyroidal illness rather than simple primary hypothyroidism.

If TSH is absent:

```text
do not emit this signal
```

### FT3 low

Package:

```text
pkg_kb47_free_t3_low_low_t3_syndrome
```

Do not activate.

Reason:

```text
Requires TSH + FT4 + illness / medication context.
Current runtime pathway is not sufficient.
```

---

## Required preflight investigation

Before making changes, report:

```text
1. How current SignalEvaluator emits primary-marker signals.
2. Whether package override / escalation rules currently prevent isolated primary marker emission.
3. Where mandatory supporting-marker gates should live.
4. Whether TSH abnormality state is available during signal evaluation.
5. Whether lab-specific reference range interpretation can identify low/suppressed TSH.
6. Exact files that need to change.
7. Exact packages that will remain untouched.
8. Rollback path.
```

STOP if:

```text
- mandatory TSH gating cannot be enforced before signal emission
- TSH state is not available to the evaluator
- implementation would require broad evaluator redesign
- implementation would affect unrelated packages
- rollback path cannot be defined
```

---

## Implementation scope

Allowed changes:

```text
- minimal runtime gating support if needed to enforce required supporting-marker gates
- package signal metadata/rule metadata for the three eligible thyroid packages
- medical frame identity index state for activated thyroid frames
- package manifest governance/runtime status metadata for activated thyroid packages
- runtime activation execution register
- audit report
- carry-forward register
- tests covering mandatory TSH gating
```

Do not change:

```text
- clinical wording
- thresholds
- activation keys
- signal IDs
- research briefs
- promoted signal intelligence content
- frontend
- scoring
- SSOT
- unrelated runtime behaviour
- androgen packages
- eGFR packages
- FT3 low package activation state
```

---

## Mandatory tests

Add or update regression tests proving:

```text
1. FT3 high does not emit when TSH is absent.
2. FT3 high does not emit when TSH is not low/suppressed.
3. FT3 high may emit when FT3 high and TSH low/suppressed.

4. FT4 high does not emit when TSH is absent.
5. FT4 high does not emit when TSH is not low/suppressed.
6. FT4 high may emit when FT4 high and TSH low/suppressed.

7. FT4 low does not emit when TSH is absent.
8. FT4 low may emit when FT4 low and TSH is present.

9. FT3 low remains inactive / not runtime-active.
10. Androgen and eGFR packages remain inactive.
```

Use lab-specific range logic where available. Do not hardcode global thyroid ranges.

---

## Mandatory STOP gate

After implementation and before activation, STOP and report:

```text
READY_FOR_HUMAN_STOP_GATE
```

The STOP report must include:

```text
- files changed
- TSH gating implementation summary
- test results
- packages proposed for activation
- packages explicitly deferred
- rollback path
- confirmation no excluded packages changed
- confirmation no medical wording / thresholds changed
```

No runtime activation may occur until the human explicitly approves.

Approval phrase:

```text
APPROVE BATCH2 THYROID GATED ACTIVATION
```

---

## Runtime activation after STOP approval

If approval is received, activate only:

```text
pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis
pkg_kb47_free_t4_high_thyrotoxicosis_context
pkg_kb47_free_t4_low_thyroid_hormone_deficiency
```

Do not activate:

```text
pkg_kb47_free_t3_low_low_t3_syndrome
```

After activation, update governance state consistently.

Expected frame state for activated packages:

```yaml
promotion_state: runtime_active_canonical
runtime_authority_status: active
clinical_adjudication_status: accepted_with_rationale
```

Expected frame state for FT3 low:

```yaml
promotion_state: compiled_not_promoted
runtime_authority_status: inactive
clinical_adjudication_status: required_before_activation
```

---

## Required execution register

Create:

```text
knowledge_bus/governance/batch2_thyroid_gate_execution_register_v1.yaml
```

It must include:

```yaml
schema_version:
runtime_consumed: false
status:
work_id:
source_thyroid_signoff:
source_remainder_resolution:
human_stop_gate:
  required: true
  approval_received:
  approval_phrase:
  approval_recorded_at:
tsh_gating_implemented:
runtime_activation_performed:
activated_package_count:
deferred_package_count:
excluded_package_count:
activated_packages:
  - package_id:
    package_path:
    signal_id:
    activation_key:
    required_gate:
    gate_test_status:
    pre_activation_state:
    post_activation_state:
    activated:
    rollback_action:
    notes:
deferred_thyroid_packages:
  - package_id:
    package_path:
    signal_id:
    activation_key:
    deferred_reason:
    activated: false
    required_next_action:
    notes:
excluded_packages:
  - package_id:
    exclusion_reason:
    confirmed_untouched:
```

---

## Required report

Create:

```text
docs/audit-papers/BATCH2-THYROID-GATE-1_mandatory_tsh_gating_and_runtime_activation.md
```

Report must include:

```text
- executive verdict
- artefacts inspected
- preflight findings
- TSH gating implementation details
- packages activated
- packages deferred
- packages excluded
- tests added / updated
- validation output pasted in full
- architecture gate output pasted in full
- STOP gate outcome
- rollback path
- carry-forward updates
- confirmation no medical wording changed
- confirmation no excluded package changed
- confirmation no unrelated runtime behaviour changed
```

---

## Carry-forward handling

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Expected handling:

```text
CF-BATCH2-013
Resolve only if FT3 high, FT4 high and FT4 low are activated with mandatory TSH gating and FT3 low remains explicitly deferred.

CF-BATCH2-007
Remain Open. eGFR adjudication remains excluded.

CF-BATCH2-010
Remain Open. Androgen clinical sign-off remains excluded.

CF-CONTEXT-MOD-3
Remain Open. Runtime Layer B context evaluation remains excluded and still blocks FT3 low and androgen packages.
```

Do not mark FT3 low resolved.

Do not mark androgen or eGFR resolved.

---

## Required validations

Before activation, run and paste actual output:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

Validate the four thyroid packages:

```powershell
python backend/scripts/validate_knowledge_package.py --package-dir <package_dir>
```

Run the new / updated thyroid gating regression tests.

After activation, if approved, rerun:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python -m pytest <thyroid gating test path> -q
```

Paste actual output. Do not provide only summaries.

---

## Runtime boundary

Runtime changes are allowed only to the minimal extent required to enforce mandatory supporting-marker gating before signal emission.

Do not modify:

```text
frontend
SSOT
scoring thresholds
unit conversion
domain score assembly
report compiler
ranking
unrelated signal evaluation behaviour
```

STOP if implementation requires broad runtime redesign.

---

## Out of scope

Do not:

```text
- activate FT3 low
- activate androgen packages
- activate eGFR packages
- resolve androgen clinical sign-off
- resolve eGFR/creatinine authority
- implement full Layer B context evaluation
- add global thyroid reference ranges
- change clinical wording
- change thresholds
- change frontend
- change scoring
- change unrelated package logic
```

---

## STOP conditions

STOP and report if:

```text
1. TSH gating cannot be enforced before signal emission.
2. TSH abnormality state is unavailable to the evaluator.
3. implementation would affect unrelated signals.
4. thyroid activation would require hardcoded global ranges.
5. FT3 low would need to be activated to complete the work.
6. androgen or eGFR packages would be touched.
7. validators fail.
8. architecture gate fails.
9. rollback path cannot be defined.
```

---

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. files inspected
3. preflight findings
4. gating implementation details
5. test evidence for each thyroid gating scenario
6. STOP gate report
7. approval status
8. packages activated
9. packages deferred
10. excluded package confirmation
11. rollback path
12. validation output
13. architecture gate output
14. carry-forward updates
15. confirmation no medical wording or thresholds changed
16. confirmation no unrelated runtime behaviour changed
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

Do not finish unless:

```text
- current branch matches work/BATCH2-THYROID-GATE-1-mandatory-tsh-gating-and-runtime-activation
- only in-scope runtime-gating/package-metadata/governance/docs/test files changed
- no androgen package files changed
- no eGFR package files changed
- FT3 low is not activated
- no frontend/SSOT/scoring/report compiler files changed
- no ambiguous stash exists
- validators pass
- architecture gate passes
```

---

## Success criteria

This sprint is complete only if:

```text
1. mandatory TSH gating is implemented before thyroid signal emission
2. FT3 high, FT4 high and FT4 low have passing gate tests
3. FT3 low remains inactive and formally deferred
4. no isolated FT3/FT4 abnormality can activate the three eligible thyroid packages
5. no hardcoded global thyroid ranges are introduced
6. three eligible thyroid packages are activated only after STOP approval
7. androgen and eGFR packages remain untouched
8. no clinical wording or thresholds change
9. architecture gate passes
10. rollback path is documented
11. CF-BATCH2-013 is accurately updated
```

```
```
