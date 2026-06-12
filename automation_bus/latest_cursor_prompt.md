---
work_id: CONTEXT-RUNTIME-1_reusable_runtime_context_evaluation_layer
branch: work/CONTEXT-RUNTIME-1-reusable-runtime-context-evaluation-layer
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# CONTEXT-RUNTIME-1 — Reusable Runtime Context Evaluation Layer

## Purpose

Build a reusable runtime context evaluation layer that can safely support context-dependent biomarker interpretation.

This sprint must not be a one-off fix for FT3 low or androgen markers.

It must create reusable architecture that future biomarkers can use when interpretation depends on non-biomarker or companion-marker context.

Initial use cases:

```text
1. Batch 2 FT3 low
2. Batch 2 androgen panel ×8
````

Future intended use cases include:

```text
- fasting insulin / HOMA-IR / metabolic syndrome
- testosterone / SHBG / FAI / free testosterone
- ferritin / CRP / inflammation
- thyroid patterns
- renal patterns
- liver patterns
- medication-influenced markers
```

---

## Strategic framing

HealthIQ AI cannot safely interpret some biomarkers from the primary blood marker alone.

Some signals require context such as:

```text
- sex
- age
- medication use
- supplement use
- hormone therapy
- steroid/anabolic exposure
- acute illness / infection / recovery state
- companion biomarkers
- contradiction biomarkers
- symptom or known-condition context
```

Current Batch 2 blockers show this clearly:

```text
FT3 low:
- requires TSH + FT4 + illness / medication context

Androgen panel:
- requires sex, age, SHBG, hormone/medication/steroid/supplement/symptom context
```

This sprint must build the reusable mechanism that lets packages declare required context and ensures runtime only emits, suppresses, or defers signals safely.

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
CF-AUTHORITY-RUNTIME-1B merged
BATCH2-EGFR-AUTHORITY-1 merged
BATCH2-REMAINING-BLOCKERS-1 merged
BATCH2-THYROID-GATE-1 merged
BATCH2-ACTIVATION-1 merged
BATCH2-PROMOTE-1 merged
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
- context_modifier_catalogue_draft_v1.yaml is missing
- batch2_remaining_blockers_execution_register_v1.yaml is missing
- Batch 2 androgen package folders cannot be found
- FT3 low package folder cannot be found
```

---

## Required inputs

Read before implementation:

```text
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
knowledge_bus/governance/batch2_remaining_blockers_execution_register_v1.yaml
knowledge_bus/governance/batch2_androgen_panel_medical_review_v1.yaml
knowledge_bus/governance/batch2_androgen_context_modifier_binding_v1.yaml
knowledge_bus/governance/batch2_remainder_resolution_register_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
docs/audit-papers/BATCH2-REMAINING-BLOCKERS-1_remaining_batch2_blocker_resolution_and_gated_activation.md
docs/audit-papers/BATCH2-CONTEXT-MOD-1_androgen_panel_context_modifier_binding.md
docs/audit-papers/BATCH2-MEDREVIEW-1_androgen_panel_medical_review.md
docs/Medical Research Documents/thyroid_blood_marker_interpretation_clinical_signoff.md
docs/sprints/launch_core_carry_forward_register.md
```

Inspect runtime paths:

```text
backend/core/analytics/signal_evaluator.py
backend/core/analytics/
SignalRegistry / package registry loader
existing context/user profile ingestion paths
existing test fixtures for biomarker context
```

Inspect packages:

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
```

---

## Sprint principle

Do not build bespoke marker logic.

Build a reusable context gate system that packages can declare against.

Preferred pattern:

```yaml
runtime_context_requirements:
  required_context:
    - context_type: demographic
      key: sex
    - context_type: demographic
      key: age
    - context_type: biomarker
      key: shbg
    - context_type: medication
      key: hormone_therapy
    - context_type: clinical_context
      key: acute_illness_or_recovery
  missing_context_behaviour: suppress_signal | emit_context_insufficient | defer_activation
```

Use a minimal schema that is future-proof but not over-engineered.

---

## Required architectural output

Create a reusable runtime context requirements model.

Preferred artefact:

```text
knowledge_bus/governance/runtime_context_requirements_model_v1.yaml
```

It must include:

```yaml
schema_version:
runtime_consumed:
status:
work_id:
supported_context_types:
  - demographic
  - biomarker
  - medication
  - supplement
  - symptom
  - clinical_context
  - known_condition
supported_missing_context_behaviours:
  - suppress_signal
  - emit_context_insufficient
  - defer_activation
runtime_contract:
  fail_closed_on_missing_required_context:
  no_clinical_claim_from_missing_context:
  package_declared_requirements_only:
notes:
```

The model must be reusable for future biomarkers.

---

## Required runtime behaviour

Implement a reusable runtime context evaluator.

Preferred helper:

```text
backend/core/analytics/runtime_context_evaluator.py
```

It should support:

```text
1. required context presence checks
2. required companion biomarker presence checks
3. required companion biomarker abnormality checks, where existing lab-range logic supports it
4. medication/supplement/context presence checks if such data exists in runtime input
5. fail-closed behaviour when required context is missing
6. deterministic result
7. no LLM calls
8. no hardcoded medical thresholds
```

It must not invent unavailable context.

If context data is unavailable in current runtime inputs, the evaluator must return a structured missing-context result and suppress or defer affected signals according to package metadata.

---

## Required package metadata pattern

Add context requirements only where supported by prior governance and medical review.

In scope:

### FT3 low

```text
pkg_kb47_free_t3_low_low_t3_syndrome
```

Known requirements:

```text
- TSH required
- FT4 required
- illness / medication context required
```

Default safe outcome unless all requirements can be enforced:

```text
remain inactive / formally gated
```

### Androgen panel

Known requirements include:

```text
- sex
- age
- SHBG where clinically relevant
- hormone medication context
- steroid / anabolic exposure context
- supplement context
- symptom or endocrine context where available
```

Default safe outcome unless runtime context can be enforced:

```text
remain inactive / formally gated
```

Do not activate androgen packages merely because metadata exists.

---

## Phase 1 — Runtime context capability audit

Before implementation, report:

```text
1. What context data is currently available to SignalEvaluator or adjacent runtime layers?
2. Is sex available?
3. Is age available?
4. Are medications available?
5. Are supplements available?
6. Are symptoms / illness context available?
7. Are known conditions available?
8. Are companion biomarkers available through the same evaluation input?
9. Where should reusable context gating live?
10. Which packages can be safely gated now?
11. Which packages must remain inactive because required context is unavailable?
12. Exact files proposed for change.
13. Rollback path.
```

STOP if:

```text
- no safe runtime location exists for context evaluation
- runtime context shape cannot be determined
- implementation would require broad pipeline redesign
- package activation would require unavailable context
```

---

## Phase 2 — Implement reusable context gate

Implement reusable context evaluation support only if it can be done safely and minimally.

Allowed changes:

```text
- reusable runtime context evaluator/helper
- small SignalEvaluator integration if this is the correct enforcement point
- package signal_library metadata for FT3 low / androgen packages only if governed
- context requirements governance model
- tests
- execution register
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
- scoring
- report compiler
- unrelated package logic
```

---

## Phase 3 — Activation decision

After context runtime support exists, decide whether any blocked Batch 2 package can safely activate.

Allowed outcomes:

```text
A. Activate safe subset after STOP approval.
B. Keep all context-dependent packages inactive but now gated and ready for future activation when context data exists.
C. Keep packages formally blocked if runtime context architecture is still insufficient.
```

Expected likely outcome:

```text
FT3 low remains inactive unless illness/medication context is runtime-consumed.
Androgen packages remain inactive unless required sex/age/SHBG/medication/supplement context is enforceable.
```

Do not force activation.

The success of this sprint is reusable context capability, not maximising the number of activated packages.

---

## Mandatory STOP gate before activation

If any activation is recommended, STOP and report:

```text
READY_FOR_HUMAN_STOP_GATE
```

STOP report must include:

```text
- packages proposed for activation
- packages remaining gated/inactive
- context requirements enforced
- test evidence
- files changed
- rollback path
- confirmation no clinical wording / thresholds changed
```

Approval phrase:

```text
APPROVE BATCH2 CONTEXT GATED ACTIVATION
```

No package activation may occur without approval.

---

## Runtime activation after STOP approval

If approved, activate only packages with fully enforceable context gates.

Expected frame state after activation:

```yaml
promotion_state: runtime_active_canonical
runtime_authority_status: active
clinical_adjudication_status: accepted_with_rationale
```

Packages without fully enforceable context must remain inactive.

---

## Required execution register

Create:

```text
knowledge_bus/governance/context_runtime_execution_register_v1.yaml
```

It must include:

```yaml
schema_version:
runtime_consumed: false
status:
work_id:
source_context_catalogue:
source_batch2_blocker_register:
runtime_context_evaluator:
  implemented:
  path:
  fail_closed:
  deterministic:
supported_context_types:
context_availability:
  sex:
  age:
  medications:
  supplements:
  symptoms:
  illness_context:
  known_conditions:
  companion_biomarkers:
human_stop_gate:
  required: true
  approval_received:
  approval_phrase:
  approval_recorded_at:
runtime_activation_performed:
activated_package_count:
gated_inactive_package_count:
blocked_package_count:
packages:
  - package_id:
    package_path:
    group:
    required_context:
    context_available:
    gate_implemented:
    activated:
    final_state:
    blocker_if_inactive:
    required_next_action:
    notes:
rollback_path:
```

---

## Required report

Create:

```text
docs/audit-papers/CONTEXT-RUNTIME-1_reusable_runtime_context_evaluation_layer.md
```

Report must include:

```text
- executive verdict
- artefacts inspected
- runtime context availability audit
- reusable context model created
- runtime implementation details
- FT3 low decision
- androgen panel decision
- packages activated, if any
- packages remaining gated/inactive
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

Add regression/sentinel tests proving:

```text
1. signal with required demographic context does not emit when context is missing
2. signal with required companion biomarker does not emit when companion marker is missing
3. signal with required medication/supplement context does not emit when that context is missing
4. signal emits only when all required context is present
5. unrelated signals without context requirements are unaffected
6. missing context fails closed
7. FT3 low remains inactive unless TSH + FT4 + illness/medication context requirements are satisfied
8. androgen packages remain inactive unless their required context is satisfied
9. no hardcoded medical thresholds are introduced
```

Tests should use package-declared requirements, not bespoke marker-specific code.

---

## Carry-forward handling

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Expected handling:

```text
CF-CONTEXT-MOD-3
Resolve only if reusable runtime context evaluation exists and is tested.

If FT3 low / androgen packages remain inactive due to unavailable runtime context data, update the CF or create a consolidated follow-on for context data ingestion, not marker-specific fragments.

CF-BATCH2-010
Resolve only if androgen clinical sign-off and runtime context prerequisites are satisfied.
Otherwise keep open with precise blocker.

Do not create separate carry-forwards for each androgen marker.
```

---

## Required validations

Run and paste actual output:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

Validate in-scope packages:

```powershell
python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/pkg_kb47_free_t3_low_low_t3_syndrome
python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/pkg_kb47_dhea_high_androgen_excess_context
python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/pkg_kb47_dhea_low_adrenal_androgen_reduction
python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/pkg_kb47_fai_high_biochemical_hyperandrogenism
python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/pkg_kb47_fai_low_reduced_free_androgen_availability
python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/pkg_kb47_free_testosterone_high_androgen_excess_context
python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/pkg_kb47_free_testosterone_low_androgen_deficiency_context
python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/pkg_kb47_free_testosterone_pct_high_elevated_free_androgen_fraction
python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/pkg_kb47_free_testosterone_pct_low_reduced_free_androgen_fraction
```

Run all new context runtime tests.

---

## Runtime boundary

Runtime changes are allowed only for reusable context evaluation and fail-closed gating.

Do not modify:

```text
frontend
SSOT
scoring thresholds
unit conversion
domain score assembly
report compiler
clinical wording
reference ranges
unrelated signal behaviour
```

STOP if implementation requires broad redesign.

---

## STOP conditions

STOP and report if:

```text
1. runtime context shape cannot be determined
2. context gates cannot be enforced fail-closed
3. implementation would require broad pipeline redesign
4. required context data is unavailable and activation would be unsafe
5. package activation would require hardcoded clinical thresholds
6. validators fail
7. architecture gate fails
8. rollback path cannot be defined
```

---

## Success criteria

This sprint is complete only if:

```text
1. reusable runtime context evaluation model exists
2. runtime context evaluator exists or the sprint formally proves why it cannot yet be implemented
3. context-dependent packages fail closed when required context is missing
4. tests protect reusable context-gating behaviour
5. FT3 low has a final safe state
6. androgen panel has a final safe state
7. no clinical wording or thresholds change
8. no unrelated runtime behaviour changes
9. validators pass
10. architecture gate passes
11. future context-heavy biomarkers can reuse the pattern
```

```
```
