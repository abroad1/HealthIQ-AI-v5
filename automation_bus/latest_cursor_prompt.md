---
work_id: KB-UTIL-2-CREATININE-AUTHORITY-ADJUDICATION_creatinine_multiframe_model_decision
branch: work/KB-UTIL-2-CREATININE-AUTHORITY-ADJUDICATION-creatinine-multiframe-model-decision
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# KB-UTIL-2-CREATININE-AUTHORITY-ADJUDICATION — Creatinine Multi-Frame Model Decision

## Purpose

Decide how HealthIQ should represent the medically valid interpretive layers under `signal_creatinine_high` without collapsing them into one flat signal and without creating duplicate runtime authority.

This sprint must not activate, retire, overwrite, or modify runtime packages.

The goal is to produce a governed adjudication decision for the creatinine-high signal family so future implementation work knows whether to:

```text
- retain legacy s24 eGFR/potassium logic as distinct frames
- enrich the Pass_3 creatinine model to preserve those contexts
- retire part of the legacy package
- defer activation pending further medical research
````

## Strategic framing

HealthIQ must support:

```text
one biomarker signal family
→ multiple medically credible interpretive frames
→ clear activation identities
→ governed context modifiers
→ Layer B personalised analysis
→ frontend render-only output
```

`creatinine_high` is not one flat medical meaning.

It may support several valid frames, including:

```text
- reduced glomerular filtration / kidney-function severity
- albuminuric kidney damage / UACR context
- acute electrolyte-risk context / potassium
- creatinine distortion or context modifiers / muscle mass, exercise, supplements, hydration
- medication-associated renal strain
```

The task is not to ask developers to choose which medical interpretation is “true”.

The task is to decide how medically valid layers should be represented in the architecture.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
KB-UTIL-2-PROMOTE-WIRE-1 merged
MED-FRAME-1 merged
MED-FRAME-2 merged
CONTEXT-MOD-1 merged
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
- medical frame identity index is missing
- context modifier catalogue is missing
- creatinine WIRE-1 audit report is missing
```

## Governance classification

```yaml
risk_level: HIGH
change_type: CONTENT
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint adjudicates medical-intelligence structure for a live biomarker signal family. It must not change runtime behaviour, but its output will govern future package promotion and activation.

## Required inputs

Read before work:

```text
docs/architecture/MED-FRAME-1_signal_family_contextual_frame_architecture.md
docs/audit-papers/MED-FRAME-2_medical_frame_identity_index_report.md
docs/architecture/CONTEXT-MOD-1_questionnaire_and_medication_modifier_governance.md
docs/audit-papers/CONTEXT-MOD-1_questionnaire_and_medication_modifier_governance_report.md
docs/audit-papers/KB-UTIL-2-PROMOTE-WIRE-1_creatinine_runtime_authority_switch_report.md
docs/audit-papers/KB-UTIL-2-ACTIVATION-READINESS_creatinine_candidate_divergence_and_collision_resolution_report.md
docs/sprints/launch_core_carry_forward_register.md
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
knowledge_bus/governance/pass3_promotion_decision_register_v1.yaml
```

Inspect the relevant package assets:

```text
knowledge_bus/packages/pkg_s24_creatinine_high_renal/
knowledge_bus/packages/pkg_kb52c_creatinine_high_reduced_glomerular_filtration/
knowledge_bus/generated_pilot/kb_util_2_pilot/promoted_candidates/pkg_creatinine_high_renal_pass3_v1/
knowledge_bus/research/investigation_specs/multi_llm_research/**/*Pass_3*.json
```

If paths differ, locate and report actual paths.

## Required medical/architecture boundary

Cursor must not make independent clinical judgements.

Cursor may:

```text
- compare artefacts
- identify divergence
- classify frame relationships
- identify where medical review is required
- update governance documentation
```

Cursor must not:

```text
- decide that eGFR/potassium context is medically obsolete
- decide that UACR replaces all other creatinine contexts
- invent hybrid clinical rules
- delete valid legacy medical context
- promote or activate a package
```

## Known medical framing to preserve

The adjudication must begin from this architectural assumption:

```text
Creatinine high can support multiple medically valid contexts.
These contexts may coexist and are not automatically contradictory.
```

At minimum, distinguish:

```text
creatinine high + low eGFR
= filtration severity / corroborating kidney-function context

creatinine high + high potassium
= acute complication / safety-risk context

creatinine high + high UACR
= kidney-damage / albuminuria context

creatinine high + cystatin C
= supporting or differential filtration marker

creatinine high + muscle/exercise/creatine/hydration context
= possible creatinine distortion or contextual explanation
```

Do not collapse these into one generic consequence.

## Core questions to answer

Answer explicitly:

```text
1. Is `pkg_kb52c` the correct current Pass_3 canonical package for the reduced-glomerular-filtration frame?
2. Does the promoted candidate add anything beyond `pkg_kb52c`, or is it a duplicate candidate?
3. What distinct medical frames are currently represented by `pkg_s24_creatinine_high_renal`?
4. Which parts of s24 are already covered by Pass_3 / kb52c?
5. Which parts of s24 are not yet covered by Pass_3 / kb52c?
6. Should eGFR and potassium be treated as:
   - separate frames,
   - supporting evidence roles,
   - override/escalation rules,
   - context modifiers,
   - or deferred pending medical review?
7. What should happen before any package is activated, superseded, or retired?
8. What Pass_3 enrichment, package regeneration, or frame-index update is needed?
```

## Required comparison table

Produce a comparison table covering:

```text
pkg_s24_creatinine_high_renal
pkg_kb52c_creatinine_high_reduced_glomerular_filtration
pkg_creatinine_high_renal_pass3_v1 promoted candidate
```

For each, capture:

```text
- package path
- signal_id
- activation_key
- source spec / source document
- primary biomarker
- supporting markers
- override rules
- thresholds
- evidence roles
- frame(s) represented
- runtime status
- promotion state
- clinical adjudication status
- whether it should be retained, enriched, superseded, or deferred
```

## Required frame-decision output

For the creatinine signal family, define proposed frame decisions for:

```text
1. reduced_glomerular_filtration
2. albuminuric_kidney_damage
3. acute_electrolyte_risk
4. creatinine_distortion_context
5. medication_associated_renal_strain
6. legacy_s24_renal_context
```

For each frame, specify:

```yaml
frame_id:
frame_label:
current_source_package:
current_status:
recommended_status:
required_source_research:
required_package_action:
required_context_modifiers:
requires_medical_review:
notes:
```

## Expected decision style

Preferred outcome is likely not “delete s24” or “activate new candidate”.

Preferred outcome is likely a governed route such as:

```text
- keep pkg_kb52c as current canonical Pass_3 authority for reduced-glomerular-filtration frame
- treat promoted candidate as duplicate compiled_not_promoted candidate
- preserve s24 eGFR and potassium as medically valid unadjudicated legacy frames
- require Pass_3 enrichment or explicit medical adjudication before retiring s24 logic
- ensure future Layer B can distinguish severity, albuminuria, acute electrolyte risk and distortion contexts
```

But Cursor must base final wording on repo evidence.

## Required artefacts

Create:

```text
docs/audit-papers/KB-UTIL-2-CREATININE-AUTHORITY-ADJUDICATION_creatinine_multiframe_model_decision_report.md
```

Create or update:

```text
knowledge_bus/governance/creatinine_multiframe_authority_decision_v1.yaml
```

Update if needed:

```text
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/pass3_promotion_decision_register_v1.yaml
docs/sprints/launch_core_carry_forward_register.md
```

Do not update runtime package files.

## YAML requirements

`creatinine_multiframe_authority_decision_v1.yaml` must include:

```yaml
schema_version:
runtime_consumed: false
status:
work_id:
decision_scope:
signal_family_id:
primary_biomarker_id:
current_runtime_authorities:
compiled_not_promoted_candidates:
legacy_unadjudicated_frames:
frame_decisions:
activation_decision:
runtime_activation_allowed:
required_before_activation:
recommended_next_sprint:
```

`runtime_activation_allowed` should be `false` unless all medical/architecture blockers are cleared.

## Medical frame identity index handling

If updating `medical_frame_identity_index_v1.yaml`, only make documentation/governance updates that reflect adjudication status.

Allowed:

```text
- update notes
- update clinical_adjudication_status
- update references to the decision file
```

Forbidden:

```text
- mark unadjudicated frames as resolved without evidence
- remove eGFR or potassium frames
- mark duplicate runtime authority as acceptable
- make the index runtime-consumed
```

Run the identity index validator after any update.

## Context modifier handling

Use `context_modifier_catalogue_draft_v1.yaml` to identify relevant modifiers, but do not wire them into runtime.

The report must mention how future creatinine frames should eventually use:

```text
- known CKD
- diabetes / hypertension
- NSAIDs
- ACE inhibitors / ARBs
- diuretics
- nephrotoxic medication categories
- hydration
- exercise / muscle mass
- creatine supplementation
```

Do not implement modifier evaluation.

## Required validations

Run:

```powershell
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
python -m pytest backend/tests/regression/test_med_frame_identity_index.py -q
python -m pytest backend/tests/regression/test_context_modifier_catalogue.py -q
```

If a new YAML validator is created for the creatinine decision file, run it too. It is optional unless hardening requires it.

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

If any of those appear necessary, STOP and report.

## Required report content

The report must include:

```text
- executive verdict
- artefacts inspected
- package comparison table
- current runtime authority assessment
- promoted candidate assessment
- s24 legacy frame assessment
- eGFR/potassium/UACR/cystatin-C frame interpretation
- context modifier relevance
- medical/architecture decision
- what must not be collapsed
- what must not be activated yet
- updates made
- validation results
- remaining blockers
- recommended next sprint
```

## Carry-forward register

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Expected updates:

```text
CF-MEDFRAME1-003 — should only be marked resolved if this sprint produces a clear creatinine multi-frame decision.
CF-CONTEXT-MOD-2 — remains open unless Layer B modifier binding is implemented, which is out of scope.
```

Likely new carry-forward if needed:

```text
CF-CREATININE-001 — Pass_3 enrichment or package regeneration for eGFR/potassium creatinine frames.
```

Do not mark runtime activation complete.

## Out of scope

Do not:

```text
- activate any package
- retire any package
- change package files
- change runtime loading
- change SignalRegistry
- change SignalEvaluator
- implement modifier evaluation
- implement Layer B frame assembly
- change frontend
- write user-facing wording
- invent clinical rules
```

## STOP conditions

STOP and report if:

```text
1. current creatinine package state cannot be reconstructed
2. pkg_kb52c cannot be found
3. s24 package cannot be found
4. promoted candidate cannot be found
5. eGFR/potassium/UACR divergence cannot be classified without medical review
6. any runtime/package/frontend change appears necessary
7. validators fail
```

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. files inspected
3. package comparison findings
4. frame decision summary
5. medical-review boundary statement
6. governance files created/updated
7. carry-forward updates
8. validation commands run
9. validation results
10. confirmation no runtime/package/frontend changes
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
- current branch matches work/KB-UTIL-2-CREATININE-AUTHORITY-ADJUDICATION-creatinine-multiframe-model-decision
- only in-scope docs/governance files changed
- no runtime package files changed
- no frontend/runtime evaluator files changed
- no ambiguous stash exists
- validators pass
```

## Success criteria

This sprint is complete only if:

```text
1. creatinine high is represented as a multi-frame signal family
2. pkg_kb52c canonical Pass_3 role is clear
3. promoted candidate duplicate status is clear
4. s24 eGFR and potassium contexts are preserved, not deleted
5. UACR/eGFR/potassium/cystatin-C roles are distinguished
6. no developer-led clinical rule choice is made
7. no runtime activation occurs
8. required future work is clear
9. carry-forward register is accurate
10. validators pass
```

```
```
