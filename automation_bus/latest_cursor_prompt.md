---
work_id: BATCH2-REMAINING-BLOCKERS-1_remaining_batch2_blocker_resolution_and_gated_activation
branch: work/BATCH2-REMAINING-BLOCKERS-1-remaining-batch2-blocker-resolution-and-gated-activation
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# BATCH2-REMAINING-BLOCKERS-1 — Remaining Batch 2 Blocker Resolution and Gated Activation

## Purpose

Resolve the remaining blocked Batch 2 packages in one outcome-based sprint.

This sprint must address all remaining non-active Batch 2 packages:

```text
1. FT3 low ×1
2. Androgen panel ×8
3. eGFR ×2
````

The goal is not to wait for perfect future medical intelligence. The goal is to decide what can be safely activated now with enforceable gates, and what must remain formally blocked because the current runtime cannot safely enforce the required context or authority rules.

Do not split this into separate marker-by-marker sprints.

---

## Current Batch 2 state

Runtime active:

```text
creatine_kinase ×2
eosinophil_pct ×2
eosinophils_abs ×2
free_t3_high
free_t4_high
free_t4_low
```

Still inactive / blocked:

```text
free_t3_low ×1
androgen ×8
eGFR ×2
```

The previous investigation concluded:

```text
FT3 low:
- requires TSH + FT4 + illness / medication context
- remains formally blocked until runtime context capability exists

Androgen:
- context-heavy
- depends on sex, age, SHBG, medication / hormone use, steroids / supplements and symptoms
- context modifiers exist in governance but are not runtime-active
- remains blocked unless a safe runtime gate can be enforced

eGFR:
- authority conflict with creatinine / eGFR escalation
- must avoid duplicate renal dysfunction signalling
- requires renal authority decision before activation
```

The prior Batch 2 remainder investigation confirmed these blockers and recommended thyroid TSH gating first, with eGFR and androgen remaining as defined resolution paths. 

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
BATCH2-THYROID-GATE-1 merged
BATCH2-ACTIVATION-1 merged
BATCH2-REMAINDER-RESOLUTION-1 merged
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
- Batch 2 remainder resolution register is missing
- thyroid gate execution register is missing
- medical frame identity index is missing
- context modifier catalogue is missing
```

---

## Required inputs

Read before implementation:

```text
knowledge_bus/governance/batch2_remainder_resolution_register_v1.yaml
knowledge_bus/governance/batch2_thyroid_gate_execution_register_v1.yaml
knowledge_bus/governance/batch2_runtime_activation_execution_register_v1.yaml
knowledge_bus/governance/batch2_final_promotion_decision_register_v1.yaml
knowledge_bus/governance/batch2_androgen_panel_medical_review_v1.yaml
knowledge_bus/governance/batch2_androgen_context_modifier_binding_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
docs/Medical Research Documents/thyroid_blood_marker_interpretation_clinical_signoff.md
docs/audit-papers/BATCH2-REMAINDER-RESOLUTION-1_remaining_batch2_package_resolution_investigation.md
docs/audit-papers/BATCH2-THYROID-GATE-1_mandatory_tsh_gating_and_runtime_activation.md
docs/sprints/launch_core_carry_forward_register.md
```

Inspect the remaining package folders:

```text
knowledge_bus/packages/pkg_kb47_free_t3_low_low_t3_syndrome/

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

Inspect runtime gating and authority code:

```text
backend/core/analytics/signal_evaluator.py
SignalRegistry / package registry loader
signal evaluation tests
renal / domain scoring or duplicate-signal handling if present
context modifier runtime handling if present
```

---

## Sprint principle

This sprint must not become another investigation-only loop unless implementation is genuinely impossible.

For every remaining package, reach one of these outcomes:

```text
1. runtime activate with enforceable gates
2. keep inactive with formal blocker recorded
3. create one consolidated runtime capability requirement if current architecture cannot safely support activation
```

Do not create new carry-forwards for individual markers unless unavoidable.

---

## In-scope package groups

### Group A — FT3 low

```text
pkg_kb47_free_t3_low_low_t3_syndrome
```

Known requirement:

```text
TSH + FT4 + illness / medication context
```

### Group B — androgen panel

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

Known requirement:

```text
sex / age / SHBG / medication / hormone / steroid / supplement / symptom context
```

### Group C — eGFR

```text
pkg_kb47_egfr_low_chronic_kidney_function_reduction
pkg_kb47_egfr_low_hemodynamic_filtration_drop
```

Known requirement:

```text
renal authority decision and anti-double-counting against creatinine/eGFR escalation
```

---

## Explicitly out of scope

Do not modify already-active Batch 2 packages except if required by validators and explicitly justified:

```text
creatine_kinase ×2
eosinophil_pct ×2
eosinophils_abs ×2
free_t3_high
free_t4_high
free_t4_low
```

Do not change:

```text
clinical wording
thresholds
reference ranges
signal IDs
activation keys
frontend
SSOT
scoring
domain score assembly
report compiler
```

---

## Phase 1 — Unified blocker resolution analysis

Before implementation, produce a concise decision table for all 11 remaining packages:

```yaml
package_id:
current_state:
known_blocker:
can_be_safely_gated_now:
requires_runtime_code_change:
requires_medical_research:
requires_architecture_decision:
recommended_action:
```

Allowed `recommended_action` values:

```text
ACTIVATE_WITH_GATE_THIS_SPRINT
KEEP_BLOCKED_RUNTIME_CAPABILITY_MISSING
KEEP_BLOCKED_AUTHORITY_DECISION_REQUIRED
KEEP_BLOCKED_MEDICAL_SIGNOFF_REQUIRED
DO_NOT_ACTIVATE
```

STOP only if package state cannot be reconciled.

---

## Phase 2 — eGFR renal authority decision

Resolve the eGFR authority model.

Answer and implement only if safe:

```text
1. Is eGFR-low allowed to become an independent runtime signal?
2. Does eGFR-low duplicate existing creatinine-high / eGFR escalation?
3. Are anti-double-counting rules already present?
4. Can both creatinine-high and eGFR-low exist safely with authority metadata / collision rules?
5. If not, should eGFR remain inactive?
```

Preferred safe outcome unless anti-double-counting is already enforceable:

```text
Keep both eGFR packages inactive.
Record formal blocker:
renal_authority_and_anti_double_counting_required
```

Only activate eGFR if the current architecture can demonstrably prevent duplicate renal dysfunction signalling without broad redesign.

Do not invent renal scoring rules.

Do not modify creatinine package logic unless explicitly required and safe.

---

## Phase 3 — androgen context-gated decision

Resolve whether any androgen package can be safely activated now.

Required checks:

```text
1. Are sex and age available at runtime to SignalEvaluator or equivalent signal context?
2. Is SHBG available as a biomarker input and accessible to the gate?
3. Are medication / hormone / steroid / supplement context values runtime-consumed?
4. Are existing context modifiers runtime-active?
5. Can the androgen signal be suppressed unless required context exists?
6. Would activation risk misleading interpretation without Layer B context evaluation?
```

Preferred safe outcome unless all required runtime context gates are enforceable:

```text
Keep all 8 androgen packages inactive.
Record formal blocker:
androgen_runtime_context_evaluation_required
```

If a subset can be safely activated with strict fail-closed context gates, implement only that subset and document why.

Do not activate androgen packages merely because governance placeholders exist.

---

## Phase 4 — FT3 low decision

Resolve whether FT3 low can be safely activated now.

Required checks:

```text
1. Can TSH presence be required?
2. Can FT4 presence be required?
3. Can illness / medication context be required before signal emission?
4. Is illness / medication context runtime-consumed?
5. If context is unavailable, can FT3 low be safely emitted as a strictly gated or context-missing state?
```

Preferred safe outcome unless full gating is enforceable:

```text
Keep FT3 low inactive.
Record formal blocker:
ft3_low_requires_layer_b_context
```

Do not activate FT3 low without TSH + FT4 + illness / medication context.

---

## Phase 5 — Implementation allowed if safe

Allowed implementation actions:

```text
- add fail-closed pre-emission gates where existing architecture supports them
- update signal_library.yaml only for packages being safely gated
- update frame index state only for packages activated after STOP approval
- update package manifest metadata only for activated packages
- create / update a remaining blockers execution register
- create / update audit report
- update carry-forward register
- add regression tests for any new gate
```

Not allowed:

```text
- broad runtime redesign
- hardcoded global ranges
- new clinical claims
- changes to medical wording
- changes to thresholds
- changes to unrelated packages
- activation without enforceable gates
```

---

## Mandatory STOP gate

After analysis and any gating implementation, STOP before any runtime activation.

Report:

```text
READY_FOR_HUMAN_STOP_GATE
```

The STOP report must include:

```text
- packages proposed for activation, if any
- packages remaining blocked
- exact blockers
- files changed
- tests added
- validation results
- rollback path
- confirmation no clinical wording / thresholds changed
```

Approval phrase:

```text
APPROVE BATCH2 REMAINING GATED ACTIVATION
```

No runtime activation may occur without that approval.

---

## Runtime activation after STOP approval

If approval is received, activate only packages that meet all conditions:

```text
- blocker resolved by enforceable gate or authority rule
- package validates
- activation key unique
- no duplicate clinical signalling risk
- regression tests pass
- rollback path exists
```

If no package meets the bar, close the sprint with all remaining packages formally blocked and no activation.

---

## Required register

Create:

```text
knowledge_bus/governance/batch2_remaining_blockers_execution_register_v1.yaml
```

Required structure:

```yaml
schema_version:
runtime_consumed: false
status:
work_id:
source_remainder_resolution:
human_stop_gate:
  required: true
  approval_received:
  approval_phrase:
  approval_recorded_at:
runtime_activation_performed:
package_count:
activated_package_count:
blocked_package_count:
groups:
  thyroid_ft3_low:
    outcome:
    blocker:
    required_next_action:
  androgen:
    outcome:
    blocker:
    required_next_action:
  egfr:
    outcome:
    blocker:
    required_next_action:
packages:
  - package_id:
    package_path:
    group:
    current_state:
    blocker_before_sprint:
    blocker_after_sprint:
    gate_implemented:
    activated:
    final_state:
    required_next_action:
    notes:
```

---

## Required report

Create:

```text
docs/audit-papers/BATCH2-REMAINING-BLOCKERS-1_remaining_batch2_blocker_resolution_and_gated_activation.md
```

Report must include:

```text
- executive verdict
- artefacts inspected
- 11-package decision table
- eGFR authority decision
- androgen context decision
- FT3 low decision
- gates implemented, if any
- packages activated, if any
- packages remaining blocked
- exact remaining blockers
- tests added / updated
- validation output pasted in full
- architecture gate output pasted in full
- STOP gate outcome
- rollback path
- carry-forward updates
- confirmation no clinical wording / thresholds changed
- confirmation no unrelated runtime behaviour changed
```

---

## Required tests

If any new gate or authority rule is implemented, add regression tests proving:

```text
- signal does not emit when required gate input is missing
- signal does not emit when required condition fails
- signal emits only when all required gate conditions pass
- unrelated signals remain unaffected
- blocked packages remain inactive
```

If no activation is performed and packages remain formally blocked, tests are only required for any changed runtime/gating code.

---

## Carry-forward handling

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Expected handling:

```text
CF-BATCH2-007 — eGFR adjudication
Resolve only if eGFR is activated safely or formally closed with a final blocker.

CF-BATCH2-010 — androgen clinical sign-off
Resolve only if androgen activation is completed or formal blocker replaces it.

CF-CONTEXT-MOD-3 — runtime context evaluation
Keep open if needed as a broader platform capability.
Update to include FT3 low and androgen if they remain blocked by context runtime.
```

Do not create new marker-specific carry-forwards unless there is no alternative.

---

## Required validations

Run and paste actual output:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

Validate all 11 remaining packages:

```powershell
python backend/scripts/validate_knowledge_package.py --package-dir <package_dir>
```

Run any new or affected regression tests.

---

## Runtime boundary

Runtime changes are allowed only if they are minimal, fail-closed, tested, and directly required to enforce known gates.

Do not modify:

```text
frontend
SSOT
scoring thresholds
unit conversion
domain score assembly
report compiler
ranking
clinical wording
reference ranges
unrelated signal behaviour
```

STOP if this requires broad redesign.

---

## STOP conditions

STOP and report if:

```text
1. package state cannot be reconciled
2. runtime gates cannot be enforced fail-closed
3. eGFR would cause duplicate renal dysfunction signalling
4. androgen context is not runtime-consumed
5. FT3 low illness / medication context is not runtime-consumed
6. activation would require hardcoded global ranges
7. activation would require broad runtime redesign
8. validators fail
9. architecture gate fails
10. rollback path cannot be defined
```

---

## Success criteria

This sprint is complete only if:

```text
1. all 11 remaining Batch 2 packages have final state
2. any activated package has enforceable fail-closed gates
3. unsafe packages remain inactive with formal blocker
4. no package is left ambiguous
5. no clinical wording or thresholds change
6. no unrelated runtime behaviour changes
7. validators pass
8. architecture gate passes
9. rollback path is documented
10. Batch 2 remaining blocker status is closed or consolidated into a single platform capability blocker
```

```
```
