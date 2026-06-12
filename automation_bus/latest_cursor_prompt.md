---
work_id: BATCH2-CONTEXT-COMPLETION-1_runtime_semantics_and_stop_gated_activation
branch: work/BATCH2-CONTEXT-COMPLETION-1-runtime-semantics-and-stop-gated-activation
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# BATCH2-CONTEXT-COMPLETION-1 — Runtime Semantics and STOP-Gated Activation

## Purpose

Complete the remaining Batch 2 context-dependent package stream in one governed, outcome-based sprint.

This sprint exists because `CONTEXT-CLEARANCE-1` created the governed semantic model and clearance register, but did not implement runtime support for the new semantics or activate any packages.

The outcome of this sprint is:

```text
Implement governed context semantics in runtime and package metadata, validate behaviour, then activate only packages that pass an internal STOP gate and explicit human approval.
```

This sprint must not be split into smaller sprints unless a STOP condition is triggered.

---

## Strategic position

HealthIQ AI is no longer in early architecture rescue mode. The remaining Batch 2 context work should now be delivered as an outcome, not fragmented into avoidable micro-sprints.

However, this is still HIGH-risk work because it may affect signal emission behaviour.

The governing principle is:

```text
One outcome.
Internal phases.
Explicit STOP gate.
No activation unless evidence proves safety.
```

---

## Non-negotiable architecture constraints

The target architecture remains:

```text
canonical research authority
→ deterministic governed compile / translation
→ governed runtime artefacts
→ thin runtime loaders
→ structured DTOs
→ frontend render-only
```

This sprint must preserve:

```text
- no raw Pass 3 / investigation-spec runtime reads
- no frontend medical inference
- no fallback or dummy parsers
- no invented clinical sign-off
- no speculative endocrine or thyroid interpretation
- no unauthorised package activation
- no global/default reference range substitution where lab ranges exist
```

---

## Governance classification

This sprint is classified as:

```yaml
risk_level: HIGH
change_type: BEHAVIOUR
execution_model: TWO_PHASE_START_FINISH
```

Rationale:

```text
- runtime context semantics affect signal emission
- package metadata may be remediated
- package activation may occur after STOP-gated approval
- affected files may include backend/core/analytics/
```

Required route:

```text
Cursor implementation
Claude audit
GPT architectural review
Human merge approval
```

No merge is permitted without GPT architectural review.

---

## Required branch

Work only on:

```text
work/BATCH2-CONTEXT-COMPLETION-1-runtime-semantics-and-stop-gated-activation
```

Do not work on `main`.

Do not merge.

---

## Authoritative inputs

Before implementation, read:

```text
docs/sprints/launch_core_carry_forward_register.md
docs/audit-papers/CONTEXT-RUNTIME-1_reusable_runtime_context_evaluation_layer.md
docs/audit-papers/CONTEXT-THREADING-1_runtime_context_orchestrator_threading.md
docs/audit-papers/CONTEXT-CLEARANCE-1_context_semantics_and_batch2_clearance.md

knowledge_bus/governance/runtime_context_requirements_model_v1.yaml
knowledge_bus/governance/runtime_context_semantics_model_v1.yaml
knowledge_bus/governance/context_runtime_execution_register_v1.yaml
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
knowledge_bus/governance/batch2_context_clearance_register_v1.yaml
knowledge_bus/governance/batch2_remaining_blockers_execution_register_v1.yaml
knowledge_bus/governance/batch2_remainder_resolution_register_v1.yaml
knowledge_bus/governance/batch2_androgen_panel_medical_review_v1.yaml
knowledge_bus/governance/batch2_androgen_context_modifier_binding_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml

docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL.md
```

Also inspect:

```text
backend/core/analytics/runtime_context_evaluator.py
backend/core/analytics/signal_evaluator.py
backend/core/pipeline/orchestrator.py
backend/core/pipeline/orchestrator_phases_v1.py
```

Inspect all remaining context-dependent Batch 2 package files listed in:

```text
knowledge_bus/governance/batch2_context_clearance_register_v1.yaml
```

---

## Current known position

From CONTEXT-CLEARANCE-1:

```text
- all 8 androgen packages remain inactive
- FT3 low remains inactive
- zero packages are activation-eligible
- runtime_context_semantics_model_v1.yaml is clearance/classification authority only
- runtime_context_requirements_model_v1.yaml remains the runtime execution companion
- current runtime evaluator does not yet support disclosed-context semantics
- androgen clinical sign-off remains unresolved in CF-BATCH2-010
- FT3 low remains blocked pending context semantics
```

This sprint may change that position only if repository evidence supports it.

---

## Authority preflight

Before editing, verify and report:

```text
1. Current branch.
2. Working tree status.
3. Current HEAD SHA.
4. `automation_bus/state/work_package_active.json` exists.
5. Active token work_id matches this work_id.
6. Active token branch matches this branch.
7. The authoritative runtime semantics model exists.
8. The runtime execution companion exists.
9. The runtime evaluator path exists.
10. The clearance register exists.
11. The carry-forward register exists.
12. No duplicate runtime context semantics authority exists.
13. No active package currently declares unresolved disclosed-context semantics.
14. All 9 context-dependent Batch 2 packages can be identified from governance files.
```

STOP if any authority source is missing or ambiguous.

---

## Reality check

Before editing, verify whether this sprint is still required.

Confirm:

```text
- CF-CONTEXT-SEMANTICS-1 is Resolved at governance/classification level
- CF-BATCH2-010 remains Open unless clinical sign-off evidence now exists
- ARCH-ORCH-RESTRUCTURE-1 remains Open
- CF-CONTEXT-MOD-3 remains Resolved at capability/threading level
- all 8 androgen packages remain inactive
- FT3 low remains inactive
- runtime evaluator does not yet implement disclosed-context semantics
```

If runtime disclosed-context semantics already exist and package metadata is already correct, STOP and report. Do not create a no-op sprint.

---

## In-scope outcome

This sprint may perform the following, subject to STOP gates:

```text
1. Implement runtime support for governed disclosed-context semantics.
2. Update package runtime_context_requirements metadata where required.
3. Add or update governance registers to record implementation outcome.
4. Add regression tests for hard gates, disclosed context, interpretation modifiers, and companion biomarker requirements.
5. Validate all affected packages.
6. Produce evidence for an internal activation STOP gate.
7. If, and only if, explicit approval is given, activate cleared packages in the same sprint.
8. If approval is not given, leave packages inactive and complete the implementation evidence only.
```

---

## Explicit non-goals

This sprint must not:

```text
- redesign the full orchestrator
- resolve ARCH-ORCH-RESTRUCTURE-1
- change clinical thresholds
- change reference range policy
- change scoring
- change frontend
- change report compiler
- change SSOT biomarker definitions
- change signal IDs
- change activation keys
- add new medical hypotheses
- invent clinical sign-off
- introduce LLM reasoning into signal evaluation
- read raw investigation specs at runtime
- modify unrelated packages
- activate packages before STOP-gated approval
```

---

## Required semantic implementation

The runtime must distinguish these concepts:

### 1. Hard prerequisite gate

Meaning:

```text
Signal must not emit unless the required prerequisite is present.
```

Examples:

```text
- age available
- biological sex available where required
- SHBG available where required
- TSH and FT4 available where required for FT3 low
```

Runtime behaviour:

```text
missing prerequisite → suppress signal fail-closed
present prerequisite → allow evaluation to continue
```

### 2. Disclosed context requirement

Meaning:

```text
The user has disclosed whether a context applies.
```

This is not the same as the condition being positive.

For example:

```text
hormone therapy status disclosed = yes
```

must allow either:

```text
hormone_therapy = true
hormone_therapy = false
```

but should fail closed where the status is:

```text
unknown / unanswered / missing
```

Runtime behaviour:

```text
field missing or unknown → suppress if disclosure is required
field answered yes/no → allow evaluation to continue
```

### 3. Interpretation modifier

Meaning:

```text
Context that may affect wording, confidence, or caution in later layers but should not automatically suppress emission unless promoted to a hard prerequisite or disclosure requirement.
```

This sprint must not introduce new narrative wording. It may record modifier availability for future use if already supported by the runtime context snapshot.

### 4. Companion biomarker requirement

Meaning:

```text
A biomarker or derived value required to interpret a signal safely.
```

Runtime behaviour:

```text
companion missing → suppress signal fail-closed
companion present → allow evaluation to continue
```

---

## Phase 1 — Read-only implementation design

Before code changes, produce and report a short implementation design covering:

```text
1. Current runtime_context_requirements schema shape.
2. Current evaluator behaviour for `present`.
3. Proposed minimal representation for disclosed-context semantics.
4. Exact package metadata fields that need to change.
5. Exact evaluator logic that needs to change.
6. Exact tests that will prove the behaviour.
7. Whether activation can be considered in this sprint.
```

STOP if the design requires a schema fork or duplicate authority.

---

## Phase 2 — Runtime evaluator implementation

Implement the minimum deterministic runtime support needed for disclosed-context semantics.

Likely touched file:

```text
backend/core/analytics/runtime_context_evaluator.py
```

Allowed only if required:

```text
backend/core/analytics/signal_evaluator.py
```

Do not change `signal_evaluator.py` unless absolutely required. If it must change, explain why before making the change.

Runtime implementation must be:

```text
- deterministic
- fail-closed
- backward compatible for existing `present` requirements
- non-inferential
- free of clinical thresholds
- free of LLM calls
```

It must not alter existing active signal behaviour.

---

## Phase 3 — Package metadata remediation

Update only the package metadata needed to align the 9 context-dependent Batch 2 packages with the governed semantics model.

Likely affected package files:

```text
signal_library.yaml files for:
- FT3 low
- 8 androgen packages
```

For each touched package, report:

```text
- package_id
- file path
- old runtime_context_requirements
- new runtime_context_requirements
- reason for change
- proof activation status did not change unless STOP-gated activation phase is reached
```

Do not change:

```text
- signal_id
- activation_key
- thresholds
- clinical wording
- evidence text
- reference range logic
- scoring
```

---

## Phase 4 — Governance register updates

Update governance artefacts to reflect implementation status.

Expected updates may include:

```text
knowledge_bus/governance/batch2_context_clearance_register_v1.yaml
knowledge_bus/governance/context_runtime_execution_register_v1.yaml
docs/sprints/launch_core_carry_forward_register.md
```

Do not mark androgen clinical sign-off resolved unless an explicit sign-off artefact exists in the repository.

Do not mark ARCH-ORCH-RESTRUCTURE-1 resolved.

---

## Phase 5 — Regression and validation

Add or update tests proving:

```text
1. Existing `present` semantics still work.
2. New `disclosed` semantics distinguish answered yes/no from missing/unknown.
3. `hormone_therapy = false` satisfies a disclosure requirement.
4. `hormone_therapy = true` satisfies a disclosure requirement.
5. missing hormone therapy status fails closed where disclosure is required.
6. AAS exposure yes/no satisfies disclosure where required.
7. missing AAS exposure fails closed where disclosure is required.
8. hard prerequisite gates still fail closed.
9. companion biomarker gates still fail closed.
10. active packages without runtime_context_requirements are unchanged.
11. FT3 low remains inactive unless STOP-gated activation is approved.
12. all 8 androgen packages remain inactive unless STOP-gated activation is approved.
```

Expected test areas:

```text
backend/tests/regression/test_runtime_context_evaluation.py
backend/tests/governance/test_runtime_context_semantics_model.py
backend/tests/governance/test_batch2_context_clearance_register.py
new tests if needed
```

---

## Phase 6 — Required validations before STOP gate

Run and paste actual output:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
python -m pytest backend/tests/regression/test_runtime_context_evaluation.py -q
python -m pytest backend/tests/governance/test_runtime_context_semantics_model.py -q
python -m pytest backend/tests/governance/test_batch2_context_clearance_register.py -q
```

Also run any new or affected tests.

If any package files are touched, run:

```powershell
python backend/scripts/validate_knowledge_package.py --package-dir <each_touched_package_dir>
```

If a validator fails, STOP.

---

## Phase 7 — Internal activation STOP gate

After implementation, package remediation, and validation, prepare an activation evidence table.

For each of the 9 packages, state:

```text
- package_id
- signal_id
- activation_key
- current status
- runtime_context_requirements status
- clinical sign-off status
- test coverage status
- package validation status
- activation recommendation
```

Allowed activation recommendations:

```text
ACTIVATE_NOW
KEEP_INACTIVE_PENDING_CLINICAL_SIGNOFF
KEEP_INACTIVE_PENDING_CONTEXT_EVIDENCE
KEEP_INACTIVE_NON_LAUNCH_CRITICAL
DO_NOT_ACTIVATE
```

STOP before activation and request explicit human approval.

Required approval phrase:

```text
APPROVE BATCH2 CONTEXT RUNTIME ACTIVATION
```

No activation may occur without this exact phrase.

If approval is not given:

```text
- do not activate packages
- commit implementation and governance evidence only if otherwise complete
- document that activation remains pending
```

---

## Phase 8 — Conditional activation

Only if the exact approval phrase is received:

```text
APPROVE BATCH2 CONTEXT RUNTIME ACTIVATION
```

then activate only packages with:

```text
activation recommendation = ACTIVATE_NOW
```

Do not activate packages blocked by:

```text
- missing clinical sign-off
- missing companion biomarker support
- failed tests
- unresolved context evidence
- non-launch-critical classification
```

For each activated package, update only the required governance / package activation metadata.

After activation, rerun:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python -m pytest backend/tests/regression/test_runtime_context_evaluation.py -q
```

Also rerun package validators for activated packages.

---

## Required audit paper

Create:

```text
docs/audit-papers/BATCH2-CONTEXT-COMPLETION-1_runtime_semantics_and_stop_gated_activation.md
```

The audit paper must include:

```text
- executive verdict
- files inspected
- files changed
- authority preflight result
- reality check result
- runtime implementation summary
- package metadata remediation summary
- package-by-package clearance table
- activation STOP gate table
- whether approval phrase was received
- packages activated, if any
- packages left inactive, with reasons
- confirmation no unauthorised activation occurred
- confirmation no thresholds changed
- confirmation no reference range policy changed
- confirmation no signal IDs changed
- confirmation no activation keys changed
- confirmation no frontend changed
- confirmation no SSOT changed
- confirmation no scoring changed
- confirmation no report compiler changed
- full validator output
- full test output
- rollback path
- residual architectural observations
- recommended next action
```

Validation and test output must be pasted in full.

---

## Required Architecture Delta Report

Create:

```text
docs/audit-papers/BATCH2-CONTEXT-COMPLETION-1_architecture_delta_report.md
```

It must answer:

```text
1. What architectural debt was removed?
2. What new architectural debt was created?
3. Did the sprint move HealthIQ closer to or further from the target architecture?
4. Which carry-forwards were resolved, created, superseded, or left open?
5. Has the estimated Day-One Architecture maturity changed?
```

Use these headings exactly:

```text
# Architecture Delta Report — BATCH2-CONTEXT-COMPLETION-1

## 1. Architectural debt removed
## 2. New architectural debt created
## 3. Movement toward target architecture
## 4. Carry-forward impact
## 5. Day-One Architecture maturity assessment
## Overall verdict
```

---

## Carry-forward rules

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Rules:

```text
CF-CONTEXT-SEMANTICS-1:
- may remain Resolved if runtime semantics now implement the governed distinction
- if runtime implementation is incomplete, reopen or add a precise follow-forward item

CF-BATCH2-010:
- must remain Open unless androgen clinical sign-off evidence exists in the repo
- do not close based on assumption or intent

CF-CONTEXT-MOD-3:
- remains Resolved unless runtime context capability is broken

ARCH-ORCH-RESTRUCTURE-1:
- remains Open
- this sprint must not claim final orchestrator architecture is complete
```

If this sprint creates a new carry-forward, add one concise item. Do not create one item per androgen marker.

---

## Expected changed files

Expected files may include:

```text
backend/core/analytics/runtime_context_evaluator.py
backend/tests/regression/test_runtime_context_evaluation.py
backend/tests/governance/test_runtime_context_semantics_model.py
backend/tests/governance/test_batch2_context_clearance_register.py

knowledge_bus/governance/batch2_context_clearance_register_v1.yaml
knowledge_bus/governance/context_runtime_execution_register_v1.yaml

docs/audit-papers/BATCH2-CONTEXT-COMPLETION-1_runtime_semantics_and_stop_gated_activation.md
docs/audit-papers/BATCH2-CONTEXT-COMPLETION-1_architecture_delta_report.md
docs/sprints/launch_core_carry_forward_register.md
```

Package `signal_library.yaml` files may be touched only if required for runtime context metadata remediation.

Files not expected to change:

```text
frontend/**
backend/ssot/**
backend/core/pipeline/orchestrator.py
backend/core/pipeline/orchestrator_phases_v1.py
backend/core/reporting/**
backend/core/scoring/**
```

If an unexpected file must change, STOP and explain before continuing.

---

## Forbidden changes

Do not change:

```text
- clinical thresholds
- reference range policy
- lab range interpretation
- signal IDs
- activation keys
- scoring
- frontend rendering
- report compiler output
- SSOT biomarker definitions
- orchestrator phase ordering
- raw research runtime loading
```

Do not introduce:

```text
- fallback parsers
- dummy parsers
- hidden heuristics
- LLM-based signal evaluation
- duplicate context authority
```

---

## STOP conditions

STOP and report if:

```text
1. authoritative runtime semantics cannot be identified
2. duplicate context authority would be created
3. disclosed semantics cannot be implemented deterministically
4. runtime implementation would require broad evaluator redesign
5. orchestrator changes are required
6. package remediation would require threshold changes
7. package remediation would require signal_id or activation_key changes
8. androgen clinical sign-off is absent and activation would depend on it
9. FT3 low activation would require ungoverned illness/medication logic
10. any active package behaviour changes unexpectedly
11. validators fail
12. tests fail
13. package validators fail
14. activation approval phrase is not given
15. rollback path cannot be defined
```

If STOP condition 14 occurs, the sprint may still complete implementation without activation if all implementation tests and validators pass and the audit clearly records activation was withheld.

---

## Git evidence requirements

Before commit, report:

```powershell
git branch --show-current
git status --short
git diff --name-only
git diff --cached --name-only
```

Commit message for implementation without activation:

```text
feat(context): implement Batch 2 disclosed runtime semantics
```

Commit message if activation also occurs after approval:

```text
feat(context): implement and activate cleared Batch 2 context packages
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

This sprint succeeds if:

```text
- governed disclosed-context semantics are implemented deterministically
- package metadata is remediated where required
- tests prove yes/no disclosure is distinct from positive presence
- existing active package behaviour is unchanged
- all validators pass
- all affected package validators pass
- activation STOP gate evidence is produced
- activation occurs only if explicitly approved
- no unauthorised activation occurs
- carry-forward register is updated accurately
- audit paper and architecture delta report are produced
```

If no packages are activated because clinical sign-off is absent or approval is withheld, the sprint can still succeed as an implementation sprint, provided the blockers are clearly documented.

---

## Amendment 1 — Add to Current known position

Add this bullet to the `Current known position` section:

```text
- FT3 low also has a separate activation-layer blocker: its signal_library.yaml currently has enable_lower_bound: false. Even if disclosed-context semantics are implemented correctly, FT3 low must not receive ACTIVATE_NOW unless enable_lower_bound is explicitly reviewed and changed through the STOP-gated activation phase.
```

---

## Amendment 2 — Add to Phase 1 design requirements

Replace the existing Phase 1 item:

```text
5. Exact evaluator logic that needs to change.
```

with:

```text
5. Exact runtime_context_evaluator.py logic that needs to change, including both:
   - build_runtime_context_snapshot()
   - evaluate_runtime_context_requirements()
```

Add:

```text
The design must explicitly explain how disclosure will be represented in the runtime context snapshot. It is not sufficient to add a disclosed branch to requirement evaluation if the snapshot never records whether the relevant question was answered.
```

---

## Amendment 3 — Replace Phase 2 opening section

Replace the first paragraph of Phase 2 with:

```text
Implement the minimum deterministic runtime support needed for disclosed-context semantics.

This is expected to require two coordinated changes inside:

backend/core/analytics/runtime_context_evaluator.py

1. Snapshot-building change:
   build_runtime_context_snapshot() must record whether the relevant context question was disclosed/answered, independently from whether the exposure is positive.

   For example:
   - hormone therapy status disclosed: yes/no/unknown
   - AAS exposure status disclosed: yes/no/unknown

   A patient answering “no hormone therapy” must satisfy a disclosure requirement, even though hormone_therapy itself is false.

2. Requirement-evaluation change:
   evaluate_runtime_context_requirements() must support disclosed-context requirements separately from existing present requirements.

   `present` means the condition/value is present.
   `disclosed` means the question/status was answered, regardless of whether the answer is yes or no.
```

---

## Amendment 4 — Add to Phase 5 tests

Add these required tests:

```text
13. build_runtime_context_snapshot() records hormone therapy disclosure separately from positive hormone therapy exposure.
14. build_runtime_context_snapshot() records AAS exposure disclosure separately from positive AAS exposure.
15. disclosed requirement passes when hormone therapy answer is no.
16. disclosed requirement passes when AAS exposure answer is no.
17. disclosed requirement fails when the relevant question was not answered.
18. FT3 low cannot receive ACTIVATE_NOW while enable_lower_bound remains false.
```

---

## Amendment 5 — Add to Phase 7 activation STOP gate table

Add this field to the package-by-package STOP gate table:

```text
- activation-layer blockers, including enable_lower_bound where applicable
```

Add this rule:

```text
FT3 low must not receive ACTIVATE_NOW unless enable_lower_bound has been explicitly reviewed and, if changed, the change is made only during the STOP-gated activation phase with validator and regression evidence.
```

---

## Amendment 6 — Add STOP condition

Add:

```text
16. disclosed semantics are implemented in requirement evaluation but the runtime context snapshot does not record disclosure state
17. FT3 low is recommended for activation while enable_lower_bound remains false
```

---

## Expected next action after this sprint

If packages are activated successfully:

```text
Proceed to Day-One Architecture Closure Review.
```

If packages remain inactive because clinical sign-off is absent:

```text
Resolve clinical sign-off evidence before any further activation.
```

If runtime semantics cannot be implemented safely:

```text
Do not activate. Produce remediation plan and keep all packages inactive.
```
