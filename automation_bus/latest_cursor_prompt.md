---
work_id: BATCH2-PROMOTE-1_cleared_wave_package_promotion
branch: work/BATCH2-PROMOTE-1-cleared-wave-package-promotion
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# BATCH2-PROMOTE-1 — Cleared Batch 2 Package Promotion

## Purpose

Promote only the 10 cleared Batch 2 packages identified by `BATCH2-CLOSURE-1`.

This sprint must move the approved Batch 2 cleared subset from governed compiled package candidates into the correct promoted package state, without touching the 10 excluded packages.

This is the final promotion sprint for the currently cleared Batch 2 package set.

Do not include androgen-panel packages.
Do not include eGFR packages.
Do not broaden scope.

---

## Strategic framing

Batch 2 has now been:

```text
- registered as canonical Pass_3 research
- validated
- provenance-corrected
- indexed into the medical frame identity index
- represented in the human-readable biomarker tree
- reviewed for promotion readiness
- closed with a final promotion decision
````

`BATCH2-CLOSURE-1` produced the final decision:

```text
PROCEED_TO_PROMOTION_WITH_CLEARED_SUBSET
```

This sprint executes that decision for the cleared subset only.

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
BATCH2-CLOSURE-1 merged
BATCH2-PROMOTION-READINESS-1 merged
PASS3-BATCH2-PROVENANCE-1 merged
PASS3-BATCH2-FRAME-INDEX-1 merged
PASS3-BATCH2-FRAME-INDEX-2 merged
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
- batch2_final_promotion_decision_register_v1.yaml is missing
- any cleared package cannot be located
- architecture gate is failing at baseline
```

---

## Required inputs

Read before work:

```text
knowledge_bus/governance/batch2_final_promotion_decision_register_v1.yaml
knowledge_bus/governance/batch2_promotion_readiness_register_v1.yaml
knowledge_bus/governance/pass3_batch2_kb47_manifest_realign_register_v1.yaml
knowledge_bus/governance/pass3_batch2_research_asset_register_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
docs/audit-papers/BATCH2-CLOSURE-1_final_batch2_promotion_decision.md
docs/sprints/launch_core_carry_forward_register.md
```

Inspect only the cleared package directories:

```text
knowledge_bus/packages/pkg_kb47_creatine_kinase_high_exertional_muscle_injury/
knowledge_bus/packages/pkg_kb47_creatine_kinase_high_persistent_nonexertional_muscle_injury/
knowledge_bus/packages/pkg_kb47_eosinophil_pct_high_reactive_atopic_eosinophilia/
knowledge_bus/packages/pkg_kb47_eosinophil_pct_high_secondary_or_systemic_eosinophilia/
knowledge_bus/packages/pkg_kb47_eosinophils_abs_high_reactive_eosinophilic_inflammation/
knowledge_bus/packages/pkg_kb47_eosinophils_abs_high_hypereosinophilic_or_secondary_eosinophilia/
knowledge_bus/packages/pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis/
knowledge_bus/packages/pkg_kb47_free_t3_low_low_t3_syndrome/
knowledge_bus/packages/pkg_kb47_free_t4_high_thyrotoxicosis_context/
knowledge_bus/packages/pkg_kb47_free_t4_low_thyroid_hormone_deficiency/
```

---

## Explicit in-scope package set

Only these 10 packages are in scope:

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

---

## Explicit out-of-scope package set

Do not modify, promote, activate or reclassify these 10 excluded packages:

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

Before making changes, report:

```text
1. 10 cleared packages found
2. 10 excluded packages confirmed out of scope
3. package validator status for each cleared package
4. provenance canonical status for each cleared package
5. frame indexed status for each cleared package
6. activation_key for each cleared package
7. whether any active duplicate activation key exists
8. current promotion/runtime state
9. exact files expected to change
```

STOP if:

```text
- any cleared package fails validation
- any cleared package has non-canonical provenance
- any cleared package is missing from the frame index
- any activation-key collision exists
- any excluded package is needed for the operation
```

---

## Required promotion action

Promote the 10 cleared packages according to existing Knowledge Bus / package promotion conventions.

If the repo already has an established promoted-package status field, authority register, or latest knowledge state, use the existing convention.

If the promotion mechanism is unclear, STOP and report. Do not invent a new runtime authority mechanism.

Allowed changes may include:

```text
- package manifest promotion-state metadata
- governed promotion decision register
- latest knowledge status only if required by existing SOP and validator evidence
- carry-forward register
- sprint report
```

Do not alter medical logic.

Do not alter signal thresholds.

Do not alter activation keys.

Do not alter signal_library semantics.

Do not alter research_brief clinical content.

---

## Runtime activation boundary

This sprint may promote the cleared packages only if the repo’s Knowledge Bus process treats promotion as the correct next state.

Runtime activation is allowed only if explicitly required by existing package promotion convention and safe under validators.

If promotion and runtime activation are separate concepts in the repo, then:

```text
promote packages
do not activate runtime
```

STOP if this distinction is unclear.

---

## Required governance register

Create:

```text
knowledge_bus/governance/batch2_promote_1_execution_register_v1.yaml
```

It must include:

```yaml
schema_version:
runtime_consumed: false
status:
work_id:
source_decision_register:
promotion_scope:
included_package_count:
excluded_package_count:
included_packages:
  - package_id:
    package_path:
    spec_id:
    signal_id:
    medical_frame_id:
    activation_key:
    pre_promotion_state:
    post_promotion_state:
    runtime_activation_changed:
    package_validator_status:
    provenance_canonical:
    frame_indexed:
    promoted:
    notes:
excluded_packages:
  - package_id:
    exclusion_reason:
```

---

## Required report

Create:

```text
docs/audit-papers/BATCH2-PROMOTE-1_cleared_wave_package_promotion.md
```

Report must include:

```text
- executive verdict
- artefacts inspected
- preflight findings
- included packages
- excluded packages
- promotion method used
- files changed
- package validation results
- architecture gate results
- runtime activation status
- confirmation no excluded packages modified
- confirmation no medical logic changed
- carry-forward updates
- remaining blockers
- recommended next step
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
Resolve only if all 10 cleared packages are promoted successfully.

CF-BATCH2-007
Remain Open. eGFR adjudication remains excluded.

CF-BATCH2-010
Remain Open. Androgen clinical sign-off remains excluded.

CF-CONTEXT-MOD-3
Remain Open. Runtime Layer B context evaluation remains excluded.
```

Do not mark androgen or eGFR blockers resolved.

---

## Required validations

Run and paste actual output:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

Validate all 10 included packages:

```powershell
python backend/scripts/validate_knowledge_package.py --package-dir <package_dir>
```

If package promotion updates any package manifests or knowledge status file, re-run validators after the update.

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
```

Do not modify excluded packages.

STOP if runtime code changes appear necessary.

---

## Out of scope

Do not:

```text
- promote androgen packages
- promote eGFR packages
- resolve androgen clinical sign-off
- resolve eGFR/creatinine adjudication
- implement Layer B context evaluation
- change signal logic
- change thresholds
- write clinical copy
- change frontend
- change runtime evaluator behaviour
```

---

## STOP conditions

STOP and report if:

```text
1. any of the 10 included packages fails validation
2. any included package is not listed as cleared in the final decision register
3. any excluded package would be modified
4. activation-key collision is detected
5. promotion mechanism is unclear
6. validators fail
7. architecture gate fails
8. runtime/frontend/evaluator change appears necessary
```

---

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. files inspected
3. included package list
4. excluded package list
5. pre-promotion validator results
6. files changed
7. post-promotion validator results
8. architecture gate output
9. carry-forward updates
10. confirmation no excluded packages modified
11. confirmation no runtime/frontend/evaluator changes
12. confirmation no medical logic changed
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
- current branch matches work/BATCH2-PROMOTE-1-cleared-wave-package-promotion
- only in-scope package metadata/governance/docs/register files changed
- no excluded package files changed
- no runtime/frontend/evaluator files changed
- no ambiguous stash exists
- all included package validators pass
- architecture gate passes
```

---

## Success criteria

This sprint is complete only if:

```text
1. only the 10 cleared packages are promoted
2. all 10 excluded packages remain untouched
3. no medical logic changes occur
4. no runtime/frontend/evaluator changes occur
5. package validators pass
6. architecture gate passes
7. execution register exists
8. CF-BATCH2-011 is accurately updated
9. remaining blockers stay open
10. Batch 2 cleared promotion package is complete
```

```
```
