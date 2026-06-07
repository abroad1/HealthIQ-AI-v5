---
work_id: BATCH2-ACTIVATION-1_runtime_activate_cleared_non_thyroid_subset
branch: work/BATCH2-ACTIVATION-1-runtime-activate-cleared-non-thyroid-subset
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# BATCH2-ACTIVATION-1 — Runtime Activate Cleared Non-Thyroid Batch 2 Subset

## Purpose

Runtime-activate only the six Batch 2 packages that remain clear after final promotion closure and thyroid clinical sign-off review.

This sprint must activate:

```text
pkg_kb47_creatine_kinase_high_exertional_muscle_injury
pkg_kb47_creatine_kinase_high_persistent_nonexertional_muscle_injury
pkg_kb47_eosinophil_pct_high_reactive_atopic_eosinophilia
pkg_kb47_eosinophil_pct_high_secondary_or_systemic_eosinophilia
pkg_kb47_eosinophils_abs_high_reactive_eosinophilic_inflammation
pkg_kb47_eosinophils_abs_high_hypereosinophilic_or_secondary_eosinophilia
````

This sprint must not activate thyroid, androgen, or eGFR packages.

The thyroid clinical sign-off returned `APPROVE_SUBSET`, with TSH mandatory before all four thyroid patterns are activated. FT3 low additionally requires TSH + FT4 + illness/medication context. Therefore thyroid remains governance-promoted but runtime-deferred. 

---

## Strategic framing

Batch 2 is no longer a discovery or readiness problem.

The current state is:

```text
- 20 Batch 2 packages exist
- 10 were governance-promoted
- 6 are runtime activation candidates
- 4 thyroid packages are deferred pending TSH-gated activation logic
- 8 androgen packages remain blocked pending clinical sign-off/context runtime work
- 2 eGFR packages remain blocked pending creatinine/eGFR adjudication
```

This sprint completes runtime activation for the six genuinely cleared packages only.

Do not reopen Batch 2 scoping.
Do not create another readiness sprint.
Do not broaden the package set.

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
BATCH2-PROMOTE-1 merged
BATCH2-PROMOTE-1-CONTINUATION merged
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
- BATCH2-PROMOTE-1 execution register is missing
- BATCH2-PROMOTE-1-CONTINUATION execution register is missing
- final Batch 2 promotion decision register is missing
- runtime activation mechanism cannot be identified
```

---

## Required inputs

Read before work:

```text
knowledge_bus/governance/batch2_promote_1_execution_register_v1.yaml
knowledge_bus/governance/batch2_runtime_activation_execution_register_v1.yaml
knowledge_bus/governance/batch2_final_promotion_decision_register_v1.yaml
knowledge_bus/governance/batch2_promotion_readiness_register_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
docs/audit-papers/BATCH2-PROMOTE-1_cleared_wave_package_promotion.md
docs/audit-papers/BATCH2-PROMOTE-1-CONTINUATION_runtime_activation_stop_gated_completion.md
docs/audit-papers/BATCH2-CLOSURE-1_final_batch2_promotion_decision.md
docs/sprints/launch_core_carry_forward_register.md
```

Also ingest the thyroid clinical sign-off content if present in repo. If not present, create a governance summary from the supplied sign-off:

```text
thyroid sign-off verdict: APPROVE_SUBSET
TSH mandatory before all thyroid activation
FT3 low requires TSH + FT4 + illness/medication context
```

Do not activate thyroid in this sprint.

---

## Runtime activation candidate subset

Only these six packages may be runtime-activated:

```text
pkg_kb47_creatine_kinase_high_exertional_muscle_injury
pkg_kb47_creatine_kinase_high_persistent_nonexertional_muscle_injury
pkg_kb47_eosinophil_pct_high_reactive_atopic_eosinophilia
pkg_kb47_eosinophil_pct_high_secondary_or_systemic_eosinophilia
pkg_kb47_eosinophils_abs_high_reactive_eosinophilic_inflammation
pkg_kb47_eosinophils_abs_high_hypereosinophilic_or_secondary_eosinophilia
```

---

## Runtime-deferred thyroid subset

These four packages must remain runtime-deferred:

```text
pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis
pkg_kb47_free_t3_low_low_t3_syndrome
pkg_kb47_free_t4_high_thyrotoxicosis_context
pkg_kb47_free_t4_low_thyroid_hormone_deficiency
```

Deferral reasons:

```yaml
pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis:
  deferred_reason: thyroid_activation_requires_tsh_gating

pkg_kb47_free_t3_low_low_t3_syndrome:
  deferred_reason: thyroid_activation_requires_tsh_ft4_and_illness_medication_context

pkg_kb47_free_t4_high_thyrotoxicosis_context:
  deferred_reason: thyroid_activation_requires_tsh_gating

pkg_kb47_free_t4_low_thyroid_hormone_deficiency:
  deferred_reason: thyroid_activation_requires_tsh_gating
```

---

## Explicitly excluded packages

These 10 packages must remain untouched and inactive:

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

STOP if any excluded package appears in the diff.

---

## Required preflight

Before runtime activation, report:

```text
1. six activation candidate packages found
2. four thyroid packages deferred with correct blocker
3. ten excluded packages confirmed out of scope
4. all six candidate packages validate
5. activation keys are unique
6. no active duplicate activation key exists
7. runtime activation mechanism identified
8. exact files expected to change
9. rollback path
10. confirmation no medical logic needs changing
```

STOP if:

```text
- any candidate package fails validation
- any candidate package is not governance-promoted
- any candidate package is not listed in the final cleared subset
- any thyroid/androgen/eGFR package would be activated
- activation-key collision is detected
- rollback path cannot be defined
- runtime activation requires code changes
```

---

## Mandatory STOP gate

Cursor must STOP before activation and report:

```text
READY_FOR_HUMAN_STOP_GATE
```

The STOP report must include:

```text
- six packages proposed for activation
- four thyroid packages deferred
- ten excluded packages untouched
- activation files proposed
- runtime effect expected
- validator status
- rollback path
- explicit statement that activation has not yet been performed
```

No activation may occur until the human explicitly approves continuation with:

```text
APPROVE BATCH2 RUNTIME ACTIVATION
```

---

## Runtime activation, only if approved

If and only if human approval is given, activate only the six runtime activation candidate packages using the existing Knowledge Bus / runtime authority mechanism.

Allowed changes may include only:

```text
- existing runtime package authority file, if repo convention requires
- latest_knowledge_status.json, if repo convention requires
- medical_frame_identity_index_v1.yaml status updates, if needed to reflect activation
- package manifest governance/runtime status metadata, if repo convention requires
- runtime activation execution register
- audit report
- carry-forward register
```

Do not alter:

```text
signal_library.yaml
research_brief.yaml
promoted_signal_intelligence.yaml
thresholds
activation_key
signal_id
clinical wording
frontend
SignalEvaluator
SignalRegistry code
runtime loaders
SSOT
scoring
```

STOP if activation would require code changes.

---

## Required execution register

Create or update:

```text
knowledge_bus/governance/batch2_runtime_activation_execution_register_v1.yaml
```

It must include:

```yaml
schema_version:
runtime_consumed: false
status:
work_id:
source_governance_promotion_register:
source_stop_gate_register:
human_stop_gate:
  required: true
  approval_received:
  approval_phrase:
  approval_recorded_at:
runtime_activation_performed:
activation_candidate_count:
thyroid_deferred_count:
excluded_package_count:
activated_package_count:
rollback_path:
activation_candidates:
  - package_id:
    package_path:
    signal_id:
    activation_key:
    pre_activation_state:
    post_activation_state:
    package_validator_status:
    duplicate_authority_check:
    activated:
    rollback_action:
    notes:
thyroid_deferred_packages:
  - package_id:
    package_path:
    signal_id:
    activation_key:
    runtime_activation_deferred:
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
docs/audit-papers/BATCH2-ACTIVATION-1_runtime_activate_cleared_non_thyroid_subset.md
```

Report must include:

```text
- executive verdict
- preflight findings
- STOP gate outcome
- human approval status
- six runtime activation candidate packages
- four thyroid runtime-deferred packages
- ten excluded packages
- packages activated, if any
- runtime authority files changed
- rollback path
- validator output pasted in full
- architecture gate output pasted in full
- confirmation no medical logic changed
- confirmation no excluded package changed
- carry-forward updates
- final Batch 2 activation status
```

---

## Carry-forward handling

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Expected handling:

```text
CF-BATCH2-012
Resolve only if six non-thyroid packages are runtime-activated successfully.

CF-BATCH2-013
Remain Open. Thyroid activation requires TSH-gated activation logic and sign-off.

CF-BATCH2-007
Remain Open. eGFR adjudication remains excluded.

CF-BATCH2-010
Remain Open. Androgen clinical sign-off remains excluded.

CF-CONTEXT-MOD-3
Remain Open. Runtime Layer B context evaluation remains excluded.
```

If approval is not provided, leave CF-BATCH2-012 open with status “deferred pending approval”.

---

## Required validations

Before activation, run and paste actual output:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

Validate all six activation candidate packages:

```powershell
python backend/scripts/validate_knowledge_package.py --package-dir <package_dir>
```

After activation, if approved, rerun:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

Paste actual output or a clear per-package PASS table with command evidence.

---

## Runtime boundary

Do not modify:

```text
SignalEvaluator
SignalRegistry code
runtime loader code
domain_score_assembler
report_compiler
frontend
SSOT
scoring thresholds
unit conversion
```

If runtime code changes are required, STOP and report.

---

## Out of scope

Do not:

```text
- activate thyroid packages
- activate androgen packages
- activate eGFR packages
- resolve thyroid clinical sign-off
- resolve androgen clinical sign-off
- resolve eGFR/creatinine adjudication
- implement TSH-gated thyroid activation logic
- implement Layer B context evaluation
- change signal logic
- change thresholds
- write clinical copy
- change frontend
- change runtime evaluator behaviour
- start a new Batch 2 review
```

---

## STOP conditions

STOP and report if:

```text
1. any activation candidate fails validation
2. any candidate is not listed as cleared in final decision register
3. any thyroid package would be activated
4. any androgen or eGFR package would be activated
5. any excluded package would be modified
6. activation-key collision is detected
7. runtime activation mechanism is unclear
8. activation would require runtime code changes
9. validators fail
10. architecture gate fails
11. rollback path cannot be defined
```

---

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. files inspected
3. preflight report
4. STOP gate report
5. human approval status
6. runtime activation candidate packages
7. thyroid deferred packages
8. excluded package confirmation
9. files changed
10. packages activated or deferred
11. rollback path
12. validation output
13. architecture gate output
14. carry-forward updates
15. confirmation no runtime/frontend/evaluator code changes
16. confirmation no medical logic changed
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
- current branch matches work/BATCH2-ACTIVATION-1-runtime-activate-cleared-non-thyroid-subset
- only in-scope authority/governance/docs/register/package-metadata files changed
- no excluded package files changed
- no thyroid package files changed except governance deferral documentation
- no runtime/frontend/evaluator code changed
- no ambiguous stash exists
- validators pass
- architecture gate passes
```

---

## Success criteria

This sprint is complete only if:

```text
1. preflight is complete
2. STOP gate occurs before activation
3. no activation occurs without explicit human approval
4. only six non-thyroid packages are activated if approved
5. thyroid packages are explicitly deferred with sign-off/gating blockers
6. androgen and eGFR packages remain untouched and inactive
7. rollback path is documented
8. no medical logic changes occur
9. no runtime/frontend/evaluator code changes occur
10. architecture gate passes
11. Batch 2 activation status is clearly closed or deferred
```

```
```
