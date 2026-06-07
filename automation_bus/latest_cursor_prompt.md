---
work_id: BATCH2-PROMOTE-1-CONTINUATION_runtime_activation_stop_gated_completion
branch: work/BATCH2-PROMOTE-1-CONTINUATION-runtime-activation-stop-gated-completion
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# BATCH2-PROMOTE-1-CONTINUATION — Runtime Activation STOP-Gated Completion

## Purpose

Complete the missing STOP-gated runtime activation phase for the Batch 2 packages already governance-promoted in `BATCH2-PROMOTE-1`.

This sprint must not reopen Batch 2 discovery, readiness review, medical review, frame indexing, provenance correction, or promotion scoping.

The goal is:

```text
Take the same 10 governance-promoted Batch 2 packages
→ perform a STOP gate for human approval
→ activate only the runtime-cleared subset if approved
→ defer thyroid packages inside this sprint because sign-off is missing
→ validate runtime authority, rollback, and exclusions
→ close the cleared Batch 2 promotion package
````

Do not include androgen packages.
Do not include eGFR packages.
Do not add new candidates.
Do not split this into another micro-sprint.

---

## Strategic framing

`BATCH2-PROMOTE-1` governance-promoted the cleared subset but did not activate them at runtime.

The correct outcome-based pattern is:

```text
governance promotion
→ STOP gate
→ runtime activation of activation-cleared packages if approved
→ explicit deferral of packages with unresolved blockers
→ validation / rollback / closure
```

This continuation sprint completes that missing activation phase without creating another review sprint.

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
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
- BATCH2-PROMOTE-1 execution register is missing
- final Batch 2 promotion decision register is missing
- runtime activation mechanism cannot be identified
```

---

## Required inputs

Read before work:

```text
knowledge_bus/governance/batch2_promote_1_execution_register_v1.yaml
knowledge_bus/governance/batch2_final_promotion_decision_register_v1.yaml
knowledge_bus/governance/batch2_promotion_readiness_register_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
docs/audit-papers/BATCH2-PROMOTE-1_cleared_wave_package_promotion.md
docs/audit-papers/BATCH2-CLOSURE-1_final_batch2_promotion_decision.md
docs/sprints/launch_core_carry_forward_register.md
```

Inspect runtime authority / package loading mechanisms:

```text
knowledge_bus/current/latest_knowledge_status.json
SignalRegistry / package registry loader
Knowledge Bus package loading code
backend/scripts/validate_knowledge_package.py
backend/scripts/run_architecture_validation_gate.py
```

If paths differ, locate and report actual paths.

---

## Governance-promoted package set

The following 10 packages were governance-promoted in `BATCH2-PROMOTE-1` and remain in scope for reconciliation:

```text
pkg_kb47_creatine_kinase_high_exertional_muscle_injury
pkg_kb47_creatine_kinase_high_persistent_nonexertional_muscle_injury
pkg_kb47_eosinophil_pct_high_reactive_atopic_eosinophilia
pkg_kb47_eosinophil_pct_high_secondary_or_systemic_eosinophilia
pkg_kb47_eosinophils_abs_high_reactive_eosinophilic_inflammation
pkg_kb47_eosinophils_abs_high_hypereosinophilic_or_secondary_eosinophilia
pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis
pkg_kb47_free_t3_low_low_t3_syndrome
pkg_kb47_free_t4_high_thyrotoxicosis_context
pkg_kb47_free_t4_low_thyroid_hormone_deficiency
```

However, governance promotion is not the same as runtime activation.

Only packages without unresolved activation blockers may be runtime-activated.

---

## Runtime activation candidate subset

Expected runtime activation candidate subset:

```text
pkg_kb47_creatine_kinase_high_exertional_muscle_injury
pkg_kb47_creatine_kinase_high_persistent_nonexertional_muscle_injury
pkg_kb47_eosinophil_pct_high_reactive_atopic_eosinophilia
pkg_kb47_eosinophil_pct_high_secondary_or_systemic_eosinophilia
pkg_kb47_eosinophils_abs_high_reactive_eosinophilic_inflammation
pkg_kb47_eosinophils_abs_high_hypereosinophilic_or_secondary_eosinophilia
```

These 6 packages may proceed to STOP-gated runtime activation if all preflight checks pass and human approval is explicitly provided.

---

## Thyroid activation boundary

The four thyroid packages are governance-promoted but must not be runtime-activated in this sprint because clinical sign-off before activation is documented as required and no sign-off record exists in the repo.

Affected packages:

```text
pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis
pkg_kb47_free_t3_low_low_t3_syndrome
pkg_kb47_free_t4_high_thyrotoxicosis_context
pkg_kb47_free_t4_low_thyroid_hormone_deficiency
```

These packages must be included in the execution register as:

```yaml
governance_promoted: true
runtime_activation_deferred: true
deferred_reason: thyroid_clinical_signoff_required_before_activation
activated: false
```

Do not activate thyroid packages unless an explicit clinical sign-off record already exists in the repo.

If no such record exists, defer them inside this sprint and do not create another sprint solely to discover that.

---

## Explicitly excluded package set

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

## Phase 1 — Activation preflight

Before any activation change, produce a preflight report covering:

```text
1. The same 10 packages are governance-promoted in BATCH2-PROMOTE-1.
2. The same 10 packages are listed as cleared in BATCH2-CLOSURE-1.
3. The 10 excluded packages remain blocked.
4. The four thyroid packages are identified as runtime-deferred pending clinical sign-off.
5. The six non-thyroid packages are identified as runtime activation candidates.
6. All 10 governance-promoted packages validate.
7. All runtime activation candidate activation keys are unique.
8. No active duplicate activation key exists.
9. Runtime activation mechanism is identified.
10. Exact files that would change for activation.
11. Rollback path.
12. Confirmation no medical logic needs changing.
```

STOP if:

```text
- any governance-promoted package fails validation
- any excluded package is required
- activation mechanism is unclear
- duplicate active authority would be created
- rollback path cannot be defined
- thyroid sign-off is missing but thyroid packages are still proposed for activation
```

---

## Phase 2 — Mandatory STOP gate

After Phase 1, Cursor must STOP and report:

```text
READY_FOR_HUMAN_STOP_GATE
```

The STOP report must include:

```text
- six runtime activation candidate packages
- four thyroid runtime-deferred packages
- ten excluded packages
- activation files proposed
- runtime effect expected
- validator status
- rollback path
- explicit statement that activation has not yet been performed
```

No activation may occur until the human explicitly approves continuation.

The approval phrase is:

```text
APPROVE BATCH2 RUNTIME ACTIVATION
```

If approval is not provided, the sprint must close as:

```text
governance promotion complete / runtime activation deferred
```

---

## Phase 3 — Runtime activation, only if approved

If and only if human approval is given, activate only the six runtime activation candidate packages using the existing Knowledge Bus / runtime authority mechanism.

Allowed changes may include only:

```text
- existing runtime package authority file, if this is the repo convention
- latest_knowledge_status.json, if this is the repo convention
- medical_frame_identity_index_v1.yaml status updates, if needed to reflect activation
- package manifest governance/runtime status metadata, if repo convention requires
- execution register
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

## Runtime activation rules

Activation may proceed only if:

```text
- package was included in BATCH2-PROMOTE-1 execution register
- package is listed as cleared in final decision register
- package is not a thyroid package requiring sign-off
- package validator passes
- activation key is unique
- excluded packages remain inactive
- rollback path exists
- architecture gate passes after activation
```

Thyroid packages must be deferred unless explicit clinical sign-off already exists in the repo.

Androgen and eGFR packages remain excluded.

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
human_stop_gate:
  required: true
  approval_received:
  approval_phrase:
  approval_recorded_at:
runtime_activation_performed:
governance_promoted_package_count:
activation_candidate_count:
thyroid_deferred_count:
excluded_package_count:
activated_package_count:
deferred_package_count:
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
    governance_promoted:
    activated:
    rollback_action:
    notes:
thyroid_deferred_packages:
  - package_id:
    package_path:
    signal_id:
    activation_key:
    governance_promoted:
    runtime_activation_deferred:
    deferred_reason:
    activated:
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
docs/audit-papers/BATCH2-PROMOTE-1-CONTINUATION_runtime_activation_stop_gated_completion.md
```

Report must include:

```text
- executive verdict
- Phase 1 preflight findings
- STOP gate outcome
- whether human approval was received
- six runtime activation candidate packages
- four thyroid runtime-deferred packages
- ten excluded packages
- packages activated, if any
- packages deferred
- excluded package confirmation
- runtime authority files changed
- rollback path
- validator output pasted in full
- architecture gate output pasted in full
- confirmation no medical logic changed
- confirmation no excluded package changed
- carry-forward updates
- final Batch 2 cleared-promotion status
```

---

## Carry-forward handling

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Expected handling:

```text
CF-BATCH2-011
Should already be resolved by BATCH2-PROMOTE-1. Do not reopen unless governance promotion is found invalid.

Add or resolve:
CF-BATCH2-012 — runtime activation of cleared non-thyroid Batch 2 promoted subset.

Add or retain:
CF-BATCH2-013 — thyroid clinical sign-off required before thyroid runtime activation.

CF-BATCH2-007
Remain Open. eGFR adjudication remains excluded.

CF-BATCH2-010
Remain Open. Androgen clinical sign-off remains excluded.

CF-CONTEXT-MOD-3
Remain Open. Runtime Layer B context evaluation remains excluded.
```

If human STOP approval is not provided, leave CF-BATCH2-012 open with status “deferred pending approval”.

---

## Required validations

Before activation, run:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

Validate all 10 governance-promoted packages:

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
- activate thyroid packages without clinical sign-off
- activate androgen packages
- activate eGFR packages
- resolve androgen clinical sign-off
- resolve thyroid clinical sign-off
- resolve eGFR/creatinine adjudication
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
1. any governance-promoted package fails validation
2. any package is not listed as cleared in final decision register
3. any excluded package would be modified
4. thyroid packages are proposed for activation without sign-off evidence
5. activation-key collision is detected
6. runtime activation mechanism is unclear
7. activation would require runtime code changes
8. validators fail
9. architecture gate fails
10. rollback path cannot be defined
```

---

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. files inspected
3. Phase 1 preflight report
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
- current branch matches work/BATCH2-PROMOTE-1-CONTINUATION-runtime-activation-stop-gated-completion
- only in-scope authority/governance/docs/register/package-metadata files changed
- no excluded package files changed
- no thyroid package files changed unless only documenting runtime deferral
- no runtime/frontend/evaluator code changed
- no ambiguous stash exists
- validators pass
- architecture gate passes
```

---

## Success criteria

This sprint is complete only if:

```text
1. Phase 1 preflight is complete
2. STOP gate occurs before activation
3. no activation occurs without explicit human approval
4. only activation-cleared non-thyroid packages are activated if approved
5. thyroid packages are explicitly deferred pending clinical sign-off
6. androgen and eGFR packages remain untouched and inactive
7. rollback path is documented
8. no medical logic changes occur
9. no runtime/frontend/evaluator code changes occur
10. architecture gate passes
11. Batch 2 cleared promotion package is closed with activated and deferred subsets clearly documented
```

```
```
