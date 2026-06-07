---
work_id: CF-AUTHORITY-RUNTIME-1_runtime_signal_authority_collision_enforcement
branch: work/CF-AUTHORITY-RUNTIME-1-runtime-signal-authority-collision-enforcement
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# CF-AUTHORITY-RUNTIME-1 — Runtime Signal Authority / Collision Enforcement

## Purpose

Implement runtime consumption of the reusable signal authority / collision model and use it to safely close out the Batch 2 eGFR activation blocker.

This sprint must deliver two outcomes in one work package:

```text
1. Reusable runtime authority / anti-double-counting enforcement.
2. Safe eGFR runtime activation, if enforcement is proven and human STOP approval is given.
````

Do not split this into separate architecture, runtime, test, and activation sprints.

`BATCH2-EGFR-AUTHORITY-1` created the governance model but left it `runtime_consumed: false`, with eGFR inactive pending runtime support. This sprint must close that gap. 

---

## Strategic framing

HealthIQ will repeatedly have overlapping biomarker families:

```text
- creatinine / eGFR / uACR / cystatin C
- ALT / AST / GGT / bilirubin
- HbA1c / glucose / fasting insulin / HOMA-IR
- ferritin / CRP / inflammation
- testosterone / SHBG / FAI / free testosterone
- TSH / FT3 / FT4
```

The platform must avoid double-counting the same biology.

This sprint must make the authority/collision model usable at runtime for the renal-filtration case, while keeping the implementation reusable for future axes.

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
BATCH2-EGFR-AUTHORITY-1 merged
BATCH2-REMAINING-BLOCKERS-1 merged
BATCH2-THYROID-GATE-1 merged
BATCH2-ACTIVATION-1 merged
BATCH2-PROMOTE-1 merged
BATCH2-CLOSURE-1 merged
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
- signal_authority_collision_model_v1.yaml is missing
- eGFR packages cannot be found
- creatinine frames/packages cannot be found
- architecture gate fails at baseline
```

---

## Required inputs

Read before implementation:

```text
knowledge_bus/governance/signal_authority_collision_model_v1.yaml
knowledge_bus/governance/batch2_egfr_authority_execution_register_v1.yaml
knowledge_bus/governance/batch2_remaining_blockers_execution_register_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
docs/audit-papers/BATCH2-EGFR-AUTHORITY-1_renal_signal_authority_and_reusable_collision_model.md
docs/audit-papers/BATCH2-REMAINING-BLOCKERS-1_remaining_batch2_blocker_resolution_and_gated_activation.md
docs/sprints/launch_core_carry_forward_register.md
```

Inspect runtime and package files:

```text
backend/core/analytics/signal_evaluator.py
SignalRegistry / package registry loader
report assembly / signal result assembly paths
domain score / output consolidation paths if relevant
knowledge_bus/packages/pkg_kb47_egfr_low_chronic_kidney_function_reduction/
knowledge_bus/packages/pkg_kb47_egfr_low_hemodynamic_filtration_drop/
knowledge_bus/packages/*creatinine*
```

---

## In-scope packages

eGFR packages:

```text
pkg_kb47_egfr_low_chronic_kidney_function_reduction
pkg_kb47_egfr_low_hemodynamic_filtration_drop
```

Related authority family to inspect:

```text
signal_creatinine_high
signal_egfr_low
renal_filtration_axis
```

Do not modify unrelated marker families.

---

## Required runtime behaviour

Implement runtime authority/collision enforcement for the renal filtration axis.

Required behaviour:

```text
1. eGFR-low is treated as the primary renal-filtration authority when active and present.
2. creatinine-high can remain available as supporting renal evidence.
3. The system must not surface low eGFR and high creatinine as two independent renal-filtration problems.
4. Distinct acute complication layers, such as hyperkalemia / electrolyte danger, must remain allowed where medically distinct.
5. Unrelated signal families must behave exactly as before.
```

The implementation must be reusable. Do not hardcode a one-off `if eGFR then suppress creatinine` hack.

Preferred pattern:

```text
runtime reads authority group
→ detects overlapping active signal families
→ applies collision policy
→ suppresses / consolidates / annotates duplicate renal-filtration signals
→ leaves distinct risk-layer signals intact
```

If full consolidation into report output is not yet possible without broad redesign, implement the smallest safe runtime enforcement and document the remaining limitation.

---

## Required reusable model consumption

Update `signal_authority_collision_model_v1.yaml` only if needed to make runtime consumption unambiguous.

The model should remain reusable for future axes.

At minimum, runtime must consume:

```yaml
authority_group_id
primary_signal_family
supporting_signal_families
collision_policy.no_duplicate_user_facing_signal
collision_policy.allow_parallel_if_distinct_risk_layer
runtime_action
requires_runtime_support
```

If the current YAML structure is not sufficient, amend it minimally and document the change.

---

## Phase 1 — Runtime design and preflight

Before implementation, report:

```text
1. Where active signal results are assembled.
2. Where authority/collision enforcement should occur.
3. How the renal_filtration_axis model will be loaded.
4. How duplicate renal-filtration outputs will be prevented.
5. How creatinine can remain supporting evidence.
6. How distinct complication layers remain allowed.
7. Exact files proposed for change.
8. Regression tests to be added.
9. Rollback path.
```

STOP if:

```text
- authority model cannot be loaded safely
- there is no safe place to enforce collision policy
- implementation would require broad report pipeline redesign
- enforcement would suppress unrelated clinical risks
- rollback path cannot be defined
```

---

## Phase 2 — Runtime implementation

Implement minimal reusable runtime support.

Allowed changes:

```text
- authority/collision model loader or helper
- SignalEvaluator / result assembly logic only if this is the correct enforcement point
- regression/sentinel tests
- governance execution register
- audit report
- carry-forward register
```

Do not change:

```text
- clinical wording
- thresholds
- reference ranges
- signal IDs
- activation keys
- frontend
- SSOT
- scoring thresholds
- unit conversion
- report compiler unless absolutely required and justified
```

---

## Phase 3 — eGFR activation decision

After authority enforcement exists and tests pass, decide whether the two eGFR packages can be activated.

Allowed outcomes:

```text
A. Activate both eGFR packages after STOP approval.
B. Keep eGFR inactive if runtime enforcement is incomplete.
```

Do not activate eGFR unless anti-double-counting is proven by tests.

---

## Mandatory STOP gate before activation

If eGFR activation is recommended, STOP and report:

```text
READY_FOR_HUMAN_STOP_GATE
```

STOP report must include:

```text
- authority/collision implementation summary
- eGFR packages proposed for activation
- creatinine interaction behaviour
- anti-double-counting test results
- unrelated-signal regression results
- files changed
- rollback path
```

Approval phrase:

```text
APPROVE BATCH2 EGFR AUTHORITY ACTIVATION
```

No eGFR activation may occur without this approval.

---

## Runtime activation after STOP approval

If approval is received, activate only:

```text
pkg_kb47_egfr_low_chronic_kidney_function_reduction
pkg_kb47_egfr_low_hemodynamic_filtration_drop
```

Expected frame state after activation:

```yaml
promotion_state: runtime_active_canonical
runtime_authority_status: active
clinical_adjudication_status: accepted_with_rationale
```

Do not activate or modify androgen packages.

Do not modify creatinine package logic unless strictly required for authority enforcement and explicitly justified.

---

## Required execution register

Create:

```text
knowledge_bus/governance/authority_runtime_execution_register_v1.yaml
```

It must include:

```yaml
schema_version:
runtime_consumed: false
status:
work_id:
source_authority_model:
authority_groups_implemented:
  - authority_group_id:
    biological_axis:
    runtime_enforcement_status:
    primary_signal_family:
    supporting_signal_families:
    collision_policy_applied:
    tests_passed:
human_stop_gate:
  required: true
  approval_received:
  approval_phrase:
  approval_recorded_at:
runtime_activation_performed:
activated_package_count:
blocked_package_count:
activated_packages:
  - package_id:
    signal_id:
    activation_key:
    pre_activation_state:
    post_activation_state:
    authority_group_id:
    activated:
    rollback_action:
blocked_or_deferred_packages:
  - package_id:
    reason:
    required_next_action:
rollback_path:
notes:
```

---

## Required report

Create:

```text
docs/audit-papers/CF-AUTHORITY-RUNTIME-1_runtime_signal_authority_collision_enforcement.md
```

Report must include:

```text
- executive verdict
- artefacts inspected
- authority model consumption design
- runtime implementation details
- eGFR / creatinine interaction decision
- anti-double-counting behaviour
- packages activated or deferred
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

Add or update sentinel/regression tests proving:

```text
1. eGFR-low can emit when active and criteria are met.
2. creatinine-high renal-filtration duplicate does not produce an independent duplicate renal-filtration output when eGFR-low is primary.
3. creatinine may remain as supporting evidence or related signal context where appropriate.
4. distinct acute risk / complication layers are not suppressed.
5. unrelated signals are unaffected.
6. authority model is fail-safe if missing / malformed.
7. eGFR packages remain inactive until STOP approval.
8. After approval, only the two eGFR packages become active.
```

Sentinel tests must fail if future work bypasses or removes authority/collision enforcement.

---

## Carry-forward handling

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Expected handling:

```text
CF-AUTHORITY-RUNTIME-1
Resolve only if runtime authority/collision enforcement exists, tests pass, and eGFR is either activated safely or formally deferred with exact blocker.

CF-BATCH2-007
Should already be resolved by governance authority classification. Do not reopen unless the authority model is invalidated.

CF-CONTEXT-MOD-3
Remain Open. Context runtime evaluation is separate.
```

Do not create new marker-specific carry-forwards unless genuinely unavoidable.

---

## Required validations

Run and paste actual output:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

Validate the two eGFR packages:

```powershell
python backend/scripts/validate_knowledge_package.py --package-dir <package_dir>
```

Run all new authority/collision tests.

If eGFR is activated after STOP approval, rerun:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python -m pytest <authority collision test path> -q
```

---

## Runtime boundary

Runtime changes are allowed only for reusable authority/collision enforcement.

Do not modify:

```text
frontend
SSOT
scoring thresholds
unit conversion
domain score assembly unless enforcement point requires it
clinical wording
reference ranges
unrelated package logic
```

STOP if implementation requires broad redesign.

---

## STOP conditions

STOP and report if:

```text
1. authority model cannot be safely loaded.
2. collision enforcement cannot be applied before duplicate outputs surface.
3. eGFR activation would still allow duplicate renal-filtration signalling.
4. creatinine acute complication layers would be incorrectly suppressed.
5. unrelated signals are affected.
6. eGFR activation would require hardcoded clinical thresholds.
7. validators fail.
8. architecture gate fails.
9. rollback path cannot be defined.
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
- current branch matches work/CF-AUTHORITY-RUNTIME-1-runtime-signal-authority-collision-enforcement
- only in-scope runtime/governance/docs/test/package-metadata files changed
- no androgen package files changed
- no frontend/SSOT/scoring/report compiler files changed unless explicitly justified
- no ambiguous stash exists
- validators pass
- architecture gate passes
```

---

## Success criteria

This sprint is complete only if:

```text
1. runtime consumes the reusable authority/collision model
2. renal_filtration_axis anti-double-counting is enforced
3. eGFR packages are either safely activated after STOP approval or formally deferred with exact blocker
4. duplicate renal-filtration signalling is prevented
5. distinct renal complication layers remain allowed
6. sentinel/regression tests protect the behaviour
7. unrelated signals are unaffected
8. no clinical wording or thresholds change
9. architecture gate passes
10. rollback path is documented
11. future overlapping biomarker families can reuse the runtime pattern
```

```
```
