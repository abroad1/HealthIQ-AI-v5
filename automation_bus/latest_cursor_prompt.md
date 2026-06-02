---
work_id: MED-FRAME-2_medical_frame_identity_index
branch: work/MED-FRAME-2-medical-frame-identity-index
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# MED-FRAME-2 — Medical Frame Identity Index

## Purpose

Implement the first machine-enforced medical frame identity index for HealthIQ.

This sprint turns the MED-FRAME-1 architecture into a governed, non-runtime identity register that can represent:

```text
one biomarker signal family
→ many medically distinct frames
→ clear activation identities
→ package/spec provenance
→ promotion state
→ collision prevention
````

The purpose is not to activate packages or change runtime behaviour.

The purpose is to prevent HealthIQ from collapsing medically distinct edge cases into one flat signal, while also preventing uncontrolled duplicate runtime authority.

## Strategic context

MED-FRAME-1 established that HealthIQ must support:

```text
biomarker evidence
+ questionnaire context
+ medication/drug-category context
→ medical frames
→ Layer B personalised interpretation
→ frontend render-only
```

This sprint implements the identity/index foundation for the first part of that model:

```text
signal family
medical frame
activation key
research spec
package authority
promotion state
```

Questionnaire and medication/drug-category modifiers are not implemented in this sprint. They are handled by `CONTEXT-MOD-1`.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
MED-FRAME-1 merged
KB-UTIL-2-PROMOTE-WIRE-1 merged or activation-refusal outcome available
KB-UTIL-2-ACTIVATION-READINESS merged
KB-UTIL-2-PROMOTE-PILOT merged
KB-UTIL-2-PILOT merged
KB-MAP-1 merged
KNOWLEDGE_BUS_SOP_v1.3.1 committed
KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1 committed
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
- MED-FRAME-1 architecture paper is missing
- medical_frame_identity_model_draft_v1.yaml is missing
- carry-forward register is missing
```

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint creates governed identity infrastructure for future medical-frame runtime authority. It must not alter runtime behaviour, but it defines controls that future runtime promotion work will depend on.

## Required inputs

Read before implementation:

```text
docs/architecture/MED-FRAME-1_signal_family_contextual_frame_architecture.md
knowledge_bus/governance/medical_frame_identity_model_draft_v1.yaml
docs/sprints/launch_core_carry_forward_register.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md
docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
docs/audit-papers/KB-UTIL-2-PROMOTE-WIRE-1_creatinine_runtime_authority_switch_report.md
docs/audit-papers/KB-UTIL-2-ACTIVATION-READINESS_creatinine_candidate_divergence_and_collision_resolution_report.md
knowledge_bus/governance/pass3_promotion_decision_register_v1.yaml
knowledge_bus/governance/pass3_legacy_package_mapping_plan_v1.yaml
```

Also inspect:

```text
knowledge_bus/packages/pkg_s24_creatinine_high_renal/
knowledge_bus/packages/pkg_kb52c_creatinine_high_reduced_glomerular_filtration/
knowledge_bus/generated_pilot/kb_util_2_pilot/promoted_candidates/pkg_creatinine_high_renal_pass3_v1/
backend/scripts/validate_day_one_architecture.py
backend/tests/architecture/test_day_one_architecture_guardrails.py
```

If paths differ, locate and report actual paths.

## Required outcome

Create a governed medical frame identity index and validator.

The index must be machine-readable, explicitly non-runtime for now, and must model at least the creatinine-high frame family from MED-FRAME-1.

The validator must prove:

```text
- no duplicate active runtime authority for the same activation_key
- compiled_not_promoted entries may share an activation_key only if explicitly collision-classified
- each frame has signal_family_id, medical_frame_id, activation_key, research_spec_id, package reference and promotion_state
- frame identity is not collapsed into signal_id alone
```

## Required artefacts

Create:

```text
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/schema/medical_frame_identity_index_schema_v1.yaml
backend/scripts/validate_medical_frame_identity_index.py
backend/tests/regression/test_med_frame_identity_index.py
docs/audit-papers/MED-FRAME-2_medical_frame_identity_index_report.md
```

The index must be marked:

```yaml
runtime_consumed: false
status: governed_non_runtime_index
```

Do not wire it into runtime.

## Required index scope

Minimum required signal family:

```text
signal_creatinine_high
```

The creatinine family must include frames for:

```text
1. reduced glomerular filtration / Pass_3 kb52c frame
2. legacy s24 renal severity / eGFR context
3. legacy s24 potassium acute complication context
4. promoted candidate duplicate of kb52c, marked compiled_not_promoted
```

The index must clearly show that:

```text
- pkg_kb52c is the current canonical Pass_3 runtime package for the reduced-glomerular-filtration frame
- promoted candidate pkg_creatinine_high_renal_pass3_v1 is compiled_not_promoted because it collides with pkg_kb52c
- pkg_s24_creatinine_high_renal contains medically valid legacy context that is not yet adjudicated into the Pass_3 frame model
- eGFR/potassium logic must not be silently collapsed or discarded
```

## Required identity fields

Each frame entry must include at minimum:

```yaml
signal_family_id:
primary_biomarker_id:
medical_frame_id:
frame_label:
frame_role:
research_spec_id:
source_package_id:
source_package_path:
activation_key:
signal_id:
promotion_state:
runtime_authority_status:
clinical_adjudication_status:
context_inputs_supported:
  biomarker_evidence:
  questionnaire_modifiers:
  medication_modifiers:
collision_group_id:
collision_status:
supersedes:
superseded_by:
notes:
```

Allowed `promotion_state` values:

```text
runtime_active_canonical
runtime_active_legacy_unadjudicated
compiled_not_promoted
superseded
retired
deferred
```

Allowed `clinical_adjudication_status` values:

```text
not_required
required_before_activation
accepted_with_rationale
blocked_pending_medical_review
```

Allowed `collision_status` values:

```text
none
real_collision_active_blocker
allowed_non_runtime_collision
resolved_by_supersession
requires_adjudication
```

## Validator requirements

The validator must:

```text
1. Load the medical frame identity index.
2. Validate required top-level fields.
3. Validate required fields for each frame.
4. Reject duplicate `medical_frame_id`.
5. Reject duplicate active `activation_key` where more than one frame has `runtime_authority_status: active`.
6. Allow duplicate activation keys only where non-active entries are explicitly marked `compiled_not_promoted` or equivalent.
7. Reject any frame with `promotion_state: runtime_active_canonical` and `collision_status: real_collision_active_blocker`.
8. Reject unknown enum values.
9. Confirm `runtime_consumed: false`.
10. Confirm every referenced package path exists, unless explicitly marked future/deferred with reason.
```

Do not make the validator a runtime dependency.

## Regression tests

Add tests proving:

```text
1. valid creatinine frame index passes
2. duplicate active activation_key fails
3. duplicate non-runtime compiled_not_promoted activation_key passes when collision is classified
4. missing required field fails
5. unknown promotion_state fails
6. unknown collision_status fails
7. runtime_consumed must be false
8. referenced package paths exist or are explicitly deferred
```

## Creatinine worked example requirements

The report must explain in business and architecture terms:

```text
- why creatinine_high is not one flat medical meaning
- why eGFR, potassium, UACR and cystatin C represent different evidence roles
- why the Pass_3 candidate was not activated
- why pkg_kb52c remains current canonical Pass_3 runtime authority for its frame
- why legacy s24 logic remains unadjudicated rather than deleted
- how the identity index prevents both collapse and duplicate authority
```

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
knowledge_bus/current/latest_knowledge_status.json
knowledge_bus/packages/*/signal_library.yaml
knowledge_bus/packages/*/package_manifest.yaml
knowledge_bus/packages/*/research_brief.yaml
```

If any runtime change appears necessary, STOP and report.

## Required validation

Run:

```powershell
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
python -m pytest backend/tests/regression/test_med_frame_identity_index.py -q
```

If existing project conventions require a different CLI style, use that style and document it.

## Carry-forward register

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Expected updates:

```text
CF-MEDFRAME1-001 — should be marked resolved only if the identity index and validator are created and passing.
CF-MEDFRAME1-002 — remains open for CONTEXT-MOD-1.
CF-MEDFRAME1-003 — remains open for creatinine authority adjudication.
```

Do not mark creatinine adjudication resolved in this sprint.

## Required report content

Create:

```text
docs/audit-papers/MED-FRAME-2_medical_frame_identity_index_report.md
```

Report must include:

```text
- executive verdict
- files created/changed
- identity model implemented
- creatinine family/frame entries
- validator behaviour
- regression test coverage
- runtime boundary confirmation
- carry-forward updates
- remaining limitations
- recommended next sprint
```

## Out of scope

Do not:

```text
- adjudicate creatinine eGFR/potassium vs UACR logic
- activate or retire packages
- modify package contents
- modify runtime loading
- modify SignalRegistry
- modify frontend
- implement questionnaire modifier rules
- implement medication modifier rules
- implement Layer B frame evaluation
- bulk-index all biomarkers
```

## STOP conditions

STOP and report if:

```text
1. MED-FRAME-1 architecture paper cannot be found
2. current creatinine package state cannot be reconstructed
3. pkg_kb52c cannot be found
4. promoted creatinine candidate cannot be found
5. validator would require runtime imports
6. index cannot distinguish active authority from compiled_not_promoted candidate
7. tests fail
8. any runtime/package/frontend change appears necessary
```

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. governance inputs read
3. package/frame state reconstructed
4. index path created
5. schema path created
6. validator path created
7. tests created
8. validation commands run
9. validation results
10. carry-forward updates
11. confirmation no runtime/package/frontend changes
```

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
- current branch matches work/MED-FRAME-2-medical-frame-identity-index
- only in-scope docs/governance/schema/validator/test files changed
- no runtime package files changed
- no frontend/runtime evaluator files changed
- no ambiguous stash exists
- validator and tests pass
```

## Success criteria

This sprint is complete only if:

```text
1. medical_frame_identity_index_v1.yaml exists
2. schema exists
3. validator exists
4. regression tests exist and pass
5. creatinine high family is modelled with multiple frames
6. duplicate active activation_key is blocked
7. compiled_not_promoted collision is allowed only when classified
8. pkg_kb52c and promoted candidate collision is represented accurately
9. legacy s24 eGFR/potassium context is preserved as unadjudicated, not deleted
10. no runtime behaviour changes occur
```

```
```
