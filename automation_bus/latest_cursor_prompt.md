---
work_id: CONTEXT-MOD-1_questionnaire_and_medication_modifier_governance
branch: work/CONTEXT-MOD-1-questionnaire-and-medication-modifier-governance
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# CONTEXT-MOD-1 — Questionnaire and Medication Modifier Governance

## Purpose

Define the governed architecture for using questionnaire answers and medication / drug-category context as structured medical modifiers in HealthIQ analysis.

This sprint must ensure HealthIQ does not become a biomarker-only interpretation system.

It must define how contextual inputs attach to medical frames without allowing frontend inference, developer judgement, or uncontrolled ad hoc rules.

This is a governance/design sprint only.

Do not change runtime behaviour.

## Strategic context

MED-FRAME-1 established that HealthIQ interpretation depends on:

```text
biomarker evidence
+ questionnaire context
+ medication / drug-category context
→ medical frames
→ Layer B personalised interpretation
→ frontend render-only output
````

MED-FRAME-2 created the first governed medical frame identity index.

This sprint defines the modifier governance model that will later allow questionnaire and medication context to strengthen, weaken, explain, suppress, redirect, or escalate medical frames.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
MED-FRAME-1 merged
MED-FRAME-2 merged
KNOWLEDGE_BUS_SOP_v1.3.1 committed
KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1 committed
docs/sprints/launch_core_carry_forward_register.md present and updated
knowledge_bus/governance/medical_frame_identity_index_v1.yaml present
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
- MED-FRAME-2 is not merged
- medical_frame_identity_index_v1.yaml is missing
- carry-forward register is missing
```

## Governance classification

```yaml
risk_level: HIGH
change_type: CONTENT
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint defines future clinical-context modifier governance. It must not change runtime behaviour, but it will shape how personal questionnaire and medication data influence medical interpretation.

## Required inputs

Read before implementation:

```text
docs/architecture/MED-FRAME-1_signal_family_contextual_frame_architecture.md
docs/audit-papers/MED-FRAME-2_medical_frame_identity_index_report.md
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/schema/medical_frame_identity_index_schema_v1.yaml
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md
docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
docs/sprints/launch_core_carry_forward_register.md
```

Also inspect and report any existing artefacts related to:

```text
questionnaire schema
lifestyle input DTOs
medication input DTOs
drug category / intervention registries
supplement fields
known condition fields
analysis input contracts
Layer B / report input models
intervention_effects_registry_v1.yaml
intervention_annotation_v1.py
medication_caveat_assembler_v1.py
```

If paths differ, locate and report actual paths.

## Core problem

Questionnaire and medication context must affect analysis, but not through uncontrolled logic.

For example, creatinine high may be interpreted differently depending on:

```text
- hydration
- recent intense exercise
- high muscle mass
- creatine supplementation
- known CKD
- diabetes / hypertension
- NSAID use
- ACE inhibitor / ARB use
- diuretic use
- abnormal potassium
- abnormal UACR
- cystatin C availability
```

These must not become frontend assumptions or developer-authored clinical shortcuts.

They need a governed modifier model.

## Required architectural distinctions

Define the difference between:

```text
biomarker evidence
questionnaire modifier
medication/drug-category modifier
supplement modifier
known-condition modifier
symptom modifier
family-history modifier
presentation-only user preference
```

The architecture must state which of these can influence medical interpretation and where that influence is allowed.

## Required modifier model

Propose a governed modifier model with at least these fields:

```yaml
modifier_id:
modifier_type:
source_input:
source_schema_path:
normalised_value:
applies_to:
  signal_family_ids:
  medical_frame_ids:
  biomarker_ids:
modifier_effect:
evidence_role:
direction:
strength:
clinical_scope:
requires_medical_review:
allowed_layer:
presentation_safety_status:
source_authority:
notes:
```

Allowed `modifier_type` values should include at least:

```text
questionnaire_lifestyle
questionnaire_symptom
questionnaire_known_condition
questionnaire_family_history
supplement
medication_category
drug_category
demographic
```

Allowed `modifier_effect` values should include at least:

```text
strengthens_frame
weakens_frame
explains_possible_cause
increases_confidence
decreases_confidence
adds_safety_escalation_context
adds_differential_context
suppresses_overclaiming
requires_missing_data_caveat
no_interpretive_effect
```

Allowed `allowed_layer` values should include at least:

```text
Layer_A_input_normalisation
Layer_B_frame_assembly
Layer_B_narrative_brief
Presentation_safety_only
Not_allowed_for_medical_inference
```

## Required first catalogue

Create an initial governance catalogue for modifier classes.

This is not exhaustive, but must include at least:

### Questionnaire / lifestyle

```text
age
sex
alcohol
smoking
exercise
hydration
diet
sleep
stress
known_conditions
family_history
symptoms if collected
health_goals if used
```

### Supplements

```text
creatine
iron
vitamin D
B12
folate
protein supplements
testosterone / hormone-related supplements if captured
```

### Medication / drug categories

```text
NSAIDs
ACE inhibitors / ARBs
diuretics
statins
metformin
thyroid medication
steroids
testosterone / hormones if declared
nephrotoxic medication categories
liver-impacting medication categories
glucose-impacting medication categories
lipid-impacting medication categories
```

Do not invent detailed clinical rules for every item. Classify where the rule would belong, what it can modify, and whether medical review is required.

## Required worked example

Use `signal_creatinine_high` and the MED-FRAME-2 creatinine frames.

Show how context modifiers attach to frames:

```text
Frame: reduced glomerular filtration
Relevant modifiers:
- known CKD
- diabetes / hypertension
- ACE inhibitor / ARB
- diuretics
- NSAIDs

Frame: albuminuric kidney damage
Relevant modifiers:
- diabetes
- hypertension
- UACR availability
- ACE inhibitor / ARB

Frame: acute electrolyte risk
Relevant modifiers:
- potassium high
- ACE inhibitor / ARB
- spironolactone / potassium-sparing diuretic category if represented
- CKD context

Frame: creatinine distortion / muscle-supplement context
Relevant modifiers:
- high muscle mass
- recent intense exercise
- creatine supplementation
- dehydration
- cystatin C availability
```

Show what the modifier may do:

```text
- strengthen a frame
- add caution
- explain possible cause
- improve or reduce confidence
- add safety escalation context
- suppress overclaiming
```

Do not write retail user copy.

## Required artefacts

Create:

```text
docs/architecture/CONTEXT-MOD-1_questionnaire_and_medication_modifier_governance.md
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
knowledge_bus/schema/context_modifier_catalogue_schema_v1.yaml
backend/scripts/validate_context_modifier_catalogue.py
backend/tests/regression/test_context_modifier_catalogue.py
docs/audit-papers/CONTEXT-MOD-1_questionnaire_and_medication_modifier_governance_report.md
```

Mark the catalogue:

```yaml
runtime_consumed: false
status: draft_governance_non_runtime
```

Do not wire it into runtime.

## Validator requirements

The validator must:

```text
1. Load the context modifier catalogue.
2. Confirm runtime_consumed is false.
3. Confirm required top-level metadata exists.
4. Confirm every modifier has required fields.
5. Reject duplicate modifier_id.
6. Reject unknown modifier_type.
7. Reject unknown modifier_effect.
8. Reject unknown allowed_layer.
9. Confirm referenced medical_frame_ids exist in medical_frame_identity_index_v1.yaml where specified.
10. Confirm no modifier is marked runtime-active.
```

Do not make the validator a runtime dependency.

## Regression tests

Add tests proving:

```text
1. valid catalogue passes
2. duplicate modifier_id fails
3. unknown modifier_type fails
4. unknown modifier_effect fails
5. unknown allowed_layer fails
6. runtime_consumed true fails
7. referenced frame IDs must exist
8. modifier catalogue is non-runtime
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
questionnaire runtime schema
medication runtime schema
knowledge_bus/packages/*
knowledge_bus/current/latest_knowledge_status.json
```

If any runtime change appears necessary, STOP and report.

## Required validation

Run:

```powershell
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
python -m pytest backend/tests/regression/test_context_modifier_catalogue.py -q
```

## Carry-forward register

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Expected updates:

```text
CF-MEDFRAME1-002 — should be marked resolved only if questionnaire and medication modifier governance, catalogue, schema, validator and tests are created and passing.
```

Likely new carry-forward:

```text
CONTEXT-MOD-2 — bind governed context modifiers into Layer B frame assembly.
```

Do not mark runtime integration complete in this sprint.

## Required report content

Create:

```text
docs/audit-papers/CONTEXT-MOD-1_questionnaire_and_medication_modifier_governance_report.md
```

Report must include:

```text
- executive verdict
- files created/changed
- existing questionnaire artefacts found
- existing medication/drug-category artefacts found
- modifier model implemented
- catalogue summary
- creatinine worked example
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
- implement modifier evaluation
- alter questionnaire schema
- alter medication schema
- alter Layer B frame assembly
- change runtime analysis
- change frontend
- write user-facing prose
- add clinical rules directly to SignalEvaluator
- adjudicate creatinine authority
- bulk-index all biomarker frames
```

## STOP conditions

STOP and report if:

```text
1. existing questionnaire artefacts cannot be located
2. existing medication/drug-category artefacts cannot be located
3. modifier catalogue cannot reference the frame index cleanly
4. validator would require runtime imports
5. medical_frame_identity_index_v1.yaml validation fails
6. tests fail
7. any runtime/package/frontend change appears necessary
```

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. governance inputs read
3. questionnaire artefacts found
4. medication/drug-category artefacts found
5. catalogue path created
6. schema path created
7. validator path created
8. tests created
9. validation commands run
10. validation results
11. carry-forward updates
12. confirmation no runtime/package/frontend changes
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
- current branch matches work/CONTEXT-MOD-1-questionnaire-and-medication-modifier-governance
- only in-scope docs/governance/schema/validator/test files changed
- no runtime package files changed
- no frontend/runtime evaluator files changed
- no questionnaire/medication runtime schema changed
- no ambiguous stash exists
- validator and tests pass
```

## Success criteria

This sprint is complete only if:

```text
1. context modifier governance paper exists
2. context modifier catalogue exists
3. schema exists
4. validator exists
5. regression tests exist and pass
6. questionnaire context is represented as governed medical input
7. medication/drug-category context is represented as governed medical input
8. creatinine example shows modifier attachment to frames
9. catalogue remains non-runtime
10. no runtime behaviour changes occur
```

```
```
