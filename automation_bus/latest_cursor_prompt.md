---
work_id: BATCH2-FULL-COVERAGE-BUILD-1_reusable_context_layer_research_authority_and_activation_readiness
branch: work/BATCH2-FULL-COVERAGE-BUILD-1-reusable-context-layer-research-authority-and-activation-readiness
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
----------------------

# BATCH2-FULL-COVERAGE-BUILD-1 — Reusable Context Layer, Research Authority and Activation Readiness

## Purpose

Build the reusable context capability required to safely interpret the remaining Batch 2 context-dependent markers, while preparing the system for a future activation sprint once the medical research authority is complete.

This is not another decision-only classification sprint.

This sprint must build the missing reusable context infrastructure that FT3 low and androgen patterns require, and make that capability reusable for future biomarkers and signal inputs.

The immediate use cases are:

```text
- FT3 low / low T3 syndrome / non-thyroidal illness context
- DHEA high
- DHEA low
- FAI high
- FAI low
- free testosterone high
- free testosterone low
- free testosterone percentage high
- free testosterone percentage low
```

But the architecture must not be thyroid-and-androgen-specific.

The strategic goal is:

```text
Build context once.
Bind it to many signals.
Keep signal evaluation deterministic.
Avoid marker-specific questionnaire hacks.
```

---

## Strategic context

HealthIQ AI is not currently being released to beta users.

The human owner has decided that the backend intelligence foundation and full intended biomarker coverage must be completed before frontend polish or beta exposure.

`ARCH-COMPLETION-1` corrected the orchestrator architecture so that `AnalysisContext` now precedes signal evaluation.

`BATCH2-MINIMUM-COVERAGE-1` formally classified the remaining Batch 2 context-dependent packages but did not activate them.

That classification is no longer enough. This sprint must start building what is missing.

The desired end state is:

```text
A reusable context layer that supports FT3 low, androgen patterns and future context-sensitive biomarkers.
```

---

## Governance classification

This sprint is classified as:

```yaml
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
```

Rationale:

```text
- reusable clinical/context primitives are being introduced or expanded
- runtime context mapping may change
- questionnaire/context contract may change
- signal activation readiness is being prepared
- future package activation depends on the output
```

Required route:

```text
Cursor implementation
Claude hardening / audit
GPT architectural review
Human approval before merge
```

Do not merge without explicit human approval.

---

## Required branch

Work only on:

```text
work/BATCH2-FULL-COVERAGE-BUILD-1-reusable-context-layer-research-authority-and-activation-readiness
```

Do not work on `main`.

Do not merge.

---

## Non-negotiable constraints

This sprint must not:

```text
- activate androgen packages
- activate FT3 low
- activate any inactive package
- change signal IDs
- change activation keys
- change clinical thresholds
- change biomarker reference range policy
- change SSOT biomarker definitions
- change scoring
- change report compiler logic
- change frontend result rendering
- introduce frontend medical inference
- introduce fallback or dummy parsers
- introduce raw Pass 3 / investigation-spec runtime reads
- introduce LLM clinical reasoning into runtime signal evaluation
- hardcode context logic only for FT3 low or androgen
```

This sprint may prepare activation readiness.

It must not perform activation.

---

## Core design rule

Any context capability built for FT3 low or androgen must be reusable for other future context-sensitive signals unless there is a specific clinical reason it cannot be.

Examples of future reusable use cases include:

```text
- inflammation interpretation
- liver marker interpretation
- kidney marker interpretation
- iron studies
- glucose / insulin patterns
- cortisol / stress patterns
- nutrient deficiency patterns
- medication-influenced results
- training-load-influenced results
- acute illness / recovery interpretation
```

Do not build marker-specific questionnaire hacks.

Build reusable primitives, then bind them to marker-specific requirements.

---

## Authoritative inputs

Read before implementation:

```text
docs/audit-papers/ARCH-COMPLETION-1_final_runtime_context_and_orchestrator_restructure.md
docs/audit-papers/BATCH2-MINIMUM-COVERAGE-1_androgen_ft3_low_clinical_and_runtime_completion.md
docs/audit-papers/BATCH2-CONTEXT-COMPLETION-1_runtime_semantics_and_stop_gated_activation.md
docs/audit-papers/CONTEXT-CLEARANCE-1_context_semantics_and_batch2_clearance.md
docs/audit-papers/DAY-ONE-ARCHITECTURE-CLOSURE-REVIEW.md
docs/sprints/launch_core_carry_forward_register.md

knowledge_bus/governance/batch2_minimum_coverage_decision_register_v1.yaml
knowledge_bus/governance/batch2_context_clearance_register_v1.yaml
knowledge_bus/governance/context_runtime_execution_register_v1.yaml
knowledge_bus/governance/runtime_context_requirements_model_v1.yaml
knowledge_bus/governance/runtime_context_semantics_model_v1.yaml
knowledge_bus/governance/batch2_remaining_blockers_execution_register_v1.yaml
knowledge_bus/governance/batch2_androgen_panel_medical_review_v1.yaml
knowledge_bus/governance/batch2_androgen_context_modifier_binding_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

Inspect:

```text
backend/core/pipeline/orchestrator.py
backend/core/analytics/runtime_context_evaluator.py
backend/core/analytics/signal_evaluator.py
backend/tests/regression/test_runtime_context_evaluation.py
backend/tests/regression/test_context_threading.py
```

Inspect the 9 relevant package directories:

```text
knowledge_bus/packages/pkg_kb47_dhea_high_androgen_excess_context/
knowledge_bus/packages/pkg_kb47_dhea_low_adrenal_androgen_reduction/
knowledge_bus/packages/pkg_kb47_fai_high_biochemical_hyperandrogenism/
knowledge_bus/packages/pkg_kb47_fai_low_reduced_free_androgen_availability/
knowledge_bus/packages/pkg_kb47_free_testosterone_high_androgen_excess_context/
knowledge_bus/packages/pkg_kb47_free_testosterone_low_androgen_deficiency_context/
knowledge_bus/packages/pkg_kb47_free_testosterone_pct_high_elevated_free_androgen_fraction/
knowledge_bus/packages/pkg_kb47_free_testosterone_pct_low_reduced_free_androgen_fraction/
knowledge_bus/packages/pkg_kb47_free_t3_low_low_t3_syndrome/
```

If any expected file is missing, report it and classify whether it blocks the sprint.

---

## Authority preflight

Before editing, verify and report:

```powershell
git branch --show-current
git status --short
git rev-parse HEAD
git log --oneline -n 10
```

Confirm:

```text
1. Current branch matches this work package branch.
2. Working tree is clean.
3. ARCH-COMPLETION-1 is merged.
4. BATCH2-MINIMUM-COVERAGE-1 is merged.
5. `AnalysisContext` precedes signal evaluation.
6. Runtime context is derived from `AnalysisContext` or a governed post-context object.
7. All 8 androgen packages remain inactive.
8. FT3 low remains inactive.
9. No activation approval currently exists.
10. Repository secret-file gate failure remains remediated.
```

STOP if the baseline is unclear.

---

# Phase 1 — Read-only architecture and context gap audit

Before changing code or governance files, produce a short design note answering:

```text
1. What context primitives already exist?
2. Which context primitives are missing for FT3 low?
3. Which context primitives are missing for androgen signals?
4. Which missing primitives are likely reusable across future biomarkers?
5. Where is questionnaire/context data currently represented?
6. Where is runtime context currently built?
7. Which context keys are currently disclosed-only?
8. Which context keys represent positive exposure?
9. Which context keys represent modifier intensity, duration, recency or severity?
10. What is the minimal reusable model needed before activation readiness can be claimed?
```

STOP if the sprint would require a broad unrelated questionnaire/frontend redesign.

---

# Phase 2 — Define reusable context primitives

Create or update a governed context primitive model.

Preferred artefact:

```text
knowledge_bus/governance/reusable_runtime_context_primitive_model_v1.yaml
```

If a better existing authority file already exists, use that and explain why.

The model must define reusable primitives for at least:

```text
- disclosure state
- positive / negative exposure state
- unknown / unanswered state
- medication exposure
- medication class exposure
- thyroid medication exposure
- hormone therapy exposure
- HRT exposure
- prescribed steroid exposure
- anabolic steroid / AAS exposure
- supplement exposure
- acute illness status
- recent infection status
- recovery status
- calorie restriction / dieting / fasting
- under-eating / low energy availability
- weight loss phase
- heavy training load
- overtraining / recovery pressure
- relevant thyroid symptoms
- relevant androgen symptoms
- sex / biological sex
- age
- life-stage where applicable
- companion biomarker availability
```

For each primitive, define:

```text
- canonical context key
- type
- allowed values
- whether it is required / optional / disclosed-only / modifier
- whether it can gate signal activation
- whether it can only modify interpretation
- whether missing value must fail closed
- example source questionnaire field
- likely reusable biomarker domains
```

Required value semantics:

```text
answered_yes
answered_no
not_answered
unknown
not_applicable
```

Do not collapse `answered_no` into missing.

Do not treat a default empty frontend list as genuine disclosure unless the source contract proves the user actively answered the field.

---

# Phase 3 — Define questionnaire/context contract

Create or update a governed questionnaire/context contract.

Preferred artefact:

```text
knowledge_bus/governance/context_questionnaire_contract_v1.yaml
```

The contract must define the backend context fields needed to support the primitives.

This does not require frontend implementation in this sprint.

The contract should describe the structured data the frontend or upload flow must eventually provide.

Include:

```text
- field name
- user-facing intent
- internal context primitive mapped
- allowed values
- required for which signal families
- whether required before activation
- whether optional modifier
- whether unanswered must fail closed
- safe default behaviour
```

For FT3 low, include at least:

```text
- thyroid medication status
- recent illness / infection
- recovery from illness
- calorie restriction / fasting / under-eating
- recent significant weight loss
- heavy training / overtraining
- relevant thyroid symptoms
- TSH availability
- FT4 availability
```

For androgen, include at least:

```text
- biological sex
- age
- hormone therapy / HRT
- anabolic steroid / AAS exposure
- prescribed steroid use
- relevant medication classes
- supplement use
- relevant androgen symptoms
- companion androgen biomarker availability
```

Design the contract so that future biomarkers can bind to the same primitives.

---

# Phase 4 — Build runtime context mapping capability

Update runtime context mapping so that the reusable primitives can be represented deterministically in runtime context.

Likely file:

```text
backend/core/analytics/runtime_context_evaluator.py
```

Allowed work:

```text
- add reusable primitive mapping helpers
- add `answered_yes` / `answered_no` / `not_answered` distinction where missing
- add deterministic mapping from AnalysisContext fields to primitive keys
- preserve existing disclosed-context semantics
- preserve existing positive-exposure semantics
- preserve fail-closed behaviour when required context is missing
```

Do not weaken existing gates.

Do not make context inference speculative.

Do not infer AAS, HRT, steroid use, thyroid medication, illness, dieting or overtraining from biomarkers alone.

Context must come from user-declared/questionnaire/context fields or explicit structured inputs.

---

# Phase 5 — Bind primitives to Batch 2 activation-readiness register

Create or update an activation-readiness register.

Preferred artefact:

```text
knowledge_bus/governance/batch2_full_coverage_activation_readiness_register_v1.yaml
```

For each of the 9 packages, document:

```text
- package path
- current activation state
- current minimum coverage decision
- required context primitives
- required companion biomarkers
- missing research authority
- missing context fields
- runtime readiness status
- package metadata readiness status
- activation blocker status
- next activation prerequisite
```

Allowed readiness statuses:

```text
RUNTIME_CONTEXT_READY_RESEARCH_PENDING
RESEARCH_READY_CONTEXT_PENDING
ACTIVATION_READY_PENDING_APPROVAL
BLOCKED_PENDING_EXTERNAL_CLINICAL_AUTHORITY
BLOCKED_PENDING_CONTEXT_CONTRACT
BLOCKED_PENDING_PACKAGE_METADATA_REMEDIATION
DO_NOT_ACTIVATE
```

This register must be governance-only:

```yaml
runtime_consumed: false
```

Do not activate any package.

---

# Phase 6 — Medical research handoff contract

Prepare the repository to receive the parallel medical research output.

Create a medical research intake specification.

Preferred artefact:

```text
knowledge_bus/governance/batch2_medical_research_intake_contract_v1.yaml
```

It must define the expected structure of the medical research output for:

```text
- FT3 low
- 8 androgen packages
```

For each marker/pattern, the research output must answer:

```text
- clinically valid cautious interpretation?
- required companion biomarkers
- required context fields
- exclusion conditions
- fail-closed conditions
- safe wording boundaries
- unsafe wording to avoid
- activation recommendation
- confidence level
- research citations / evidence basis
- whether external clinician review is still required
```

This sprint should not invent the medical conclusions.

It should create the structured contract so the medical research LLM output can be validated and used in the next activation sprint.

---

# Phase 7 — Tests

Add or update tests proving:

```text
1. context primitives preserve answered_yes / answered_no / not_answered distinctions
2. disclosed context still passes for answered_yes and answered_no
3. disclosed context fails for not_answered
4. positive exposure is not confused with disclosure
5. AAS answered_no is not treated as missing
6. HRT / hormone therapy answered_no is not treated as missing
7. thyroid medication answered_no is not treated as missing
8. illness/recovery unanswered fails closed where required
9. reusable primitives can be generated from AnalysisContext-derived runtime context
10. no context-dependent packages become active
11. androgen packages remain inactive
12. FT3 low remains inactive
```

If existing tests already cover some of these, extend only where needed.

Do not rely only on governance-file tests. There must be runtime mapping tests.

---

# Phase 8 — Required validation

Run and paste full output.

## Architecture / governance validators

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_day_one_architecture.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

## Context regressions

```powershell
python -m pytest backend/tests/regression/test_runtime_context_evaluation.py -q
python -m pytest backend/tests/regression/test_context_threading.py -q
```

## Governance tests

Run existing governance tests for:

```text
batch2 minimum coverage
batch2 context clearance
runtime context semantics
```

Add and run new tests for new governance artefacts.

## Secret-file guardrail

Run:

```powershell
python scripts/check_no_secret_files.py
```

if present.

---

# Phase 9 — Required audit paper

Create:

```text
docs/audit-papers/BATCH2-FULL-COVERAGE-BUILD-1_reusable_context_layer_research_authority_and_activation_readiness.md
```

The audit paper must include:

```text
- executive verdict
- files inspected
- files changed
- existing context primitives found
- new reusable context primitives added
- questionnaire/context contract summary
- runtime context mapping changes
- FT3 low readiness assessment
- androgen readiness assessment
- activation-readiness register summary
- medical research intake contract summary
- confirmation no packages activated
- confirmation androgen packages remain inactive
- confirmation FT3 low remains inactive
- confirmation no package metadata changed unless explicitly justified
- confirmation no SSOT changed
- confirmation no scoring changed
- confirmation no report compiler changed
- confirmation no frontend changed
- confirmation no raw research runtime reads introduced
- full validator output
- full test output
- rollback path
- carry-forward impact
- recommended next action
```

Validation and test output must be pasted in full, not summarised.

---

# Phase 10 — Carry-forward handling

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

only if justified.

Expected handling:

```text
CF-BATCH2-010 remains Open unless external clinical authority is actually present.
FT3 low blocker remains Open unless the context contract and lower-bound readiness are truly resolved.
Context capability carry-forward may be added or updated only if this sprint leaves a precise residual.
```

Do not close CF-BATCH2-010.

Do not claim activation readiness if medical research authority is not yet available.

---

## Expected changed files

Expected changed files may include:

```text
knowledge_bus/governance/reusable_runtime_context_primitive_model_v1.yaml
knowledge_bus/governance/context_questionnaire_contract_v1.yaml
knowledge_bus/governance/batch2_full_coverage_activation_readiness_register_v1.yaml
knowledge_bus/governance/batch2_medical_research_intake_contract_v1.yaml
backend/core/analytics/runtime_context_evaluator.py
backend/tests/regression/test_runtime_context_evaluation.py
backend/tests/regression/test_context_threading.py
backend/tests/governance/*
docs/sprints/launch_core_carry_forward_register.md
docs/audit-papers/BATCH2-FULL-COVERAGE-BUILD-1_reusable_context_layer_research_authority_and_activation_readiness.md
automation_bus/latest_cursor_status.json
```

No package files are expected to change unless a strictly necessary metadata-readiness annotation is proposed and STOP-gated.

No frontend files are expected to change.

No SSOT files are expected to change.

No scoring or report compiler files are expected to change.

---

## Forbidden changes

Do not change:

```text
frontend/**
backend/ssot/**
backend/core/reporting/**
backend/core/scoring/**
```

Do not activate:

```text
- androgen packages
- FT3 low
- any inactive package
```

Do not introduce:

```text
- fallback parsers
- dummy parsers
- raw research runtime reads
- frontend clinical inference
- LLM clinical reasoning
```

---

## STOP conditions

STOP and report if:

```text
1. reusable context primitives cannot be introduced without broad frontend redesign
2. runtime context mapping cannot preserve answered_yes / answered_no / not_answered distinctions
3. positive exposure and disclosure cannot be separated deterministically
4. AnalysisContext does not contain enough structured fields to support a reusable context adapter
5. the sprint would require package activation
6. the sprint would require clinical threshold changes
7. the sprint would require SSOT changes
8. the sprint would require report compiler changes
9. the sprint would require frontend changes
10. validators fail
11. context runtime tests fail
12. secret-file guardrail fails
13. rollback path cannot be defined
```

If a STOP condition is triggered, do not perform ad hoc remediation beyond scope.

---

## Git evidence requirements

Before commit, report:

```powershell
git branch --show-current
git status --short
git diff --name-only
git diff --cached --name-only
```

Commit message:

```text
feat(context): add reusable runtime context primitives for Batch 2 readiness
```

After commit, report:

```powershell
git status --short
git log --oneline -n 5
git diff --name-only main...HEAD
```

Do not merge.

Return evidence for Claude audit and GPT architectural review.

---

## Success criteria

This sprint succeeds only if:

```text
- reusable context primitives are defined
- questionnaire/context contract is defined
- runtime context mapping supports the new primitives deterministically
- answered_yes / answered_no / not_answered are preserved
- disclosure is not confused with positive exposure
- Batch 2 full-coverage activation-readiness register exists
- medical research intake contract exists
- all 9 remaining packages have activation-readiness status
- no packages are activated
- androgen packages remain inactive
- FT3 low remains inactive
- no package metadata changes occur unless explicitly justified
- no SSOT changes occur
- no scoring changes occur
- no report compiler changes occur
- no frontend changes occur
- validators pass
- context runtime tests pass
- audit paper contains full evidence
```

Expected next action after success:

```text
Run the parallel medical research LLM review using the intake contract, then proceed to the activation build only once research authority and runtime readiness are both present.
```
