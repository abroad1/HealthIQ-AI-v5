---
work_id: BATCH2-MINIMUM-COVERAGE-1_androgen_ft3_low_clinical_and_runtime_completion
branch: work/BATCH2-MINIMUM-COVERAGE-1-androgen-ft3-low-clinical-and-runtime-completion
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# BATCH2-MINIMUM-COVERAGE-1 — Androgen and FT3 Low Clinical / Runtime Completion

## Purpose

Complete the remaining Batch 2 minimum-coverage decision for the context-dependent packages that were previously blocked or deferred:

```text
- 8 androgen packages
- FT3 low package
```

This sprint must determine, for each remaining package, whether it should be:

```text
ACTIVATE_WITH_GATES
EXCLUDE_FROM_MINIMUM_COVERAGE
DEFER_PENDING_EXTERNAL_CLINICAL_AUTHORITY
DO_NOT_ACTIVATE
```

The objective is to stop leaving the Batch 2 remainder in an ambiguous “later” state.

This sprint must either complete activation safely or produce a formal exclusion/defer decision with evidence.

---

## Strategic context

`ARCH-COMPLETION-1` has now corrected the orchestrator phase-order defect.

Signal evaluation now receives runtime context derived from the assembled `AnalysisContext`, not the former raw `questionnaire_data` bridge.

This removes the architectural blocker that previously prevented serious consideration of context-dependent package activation.

However, activation still requires clinical and governance authority.

The most recent readiness checks confirmed:

```text
- all 8 androgen packages remain inactive
- FT3 low remains inactive
- activated_package_count remains 0 for context-dependent Batch 2 packages
- approval_received remains false
- CF-BATCH2-010 remains open unless valid clinical sign-off now exists
```

This sprint must not assume those blockers are resolved. It must verify them.

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
- context-dependent clinical packages may be activated or formally excluded
- androgen interpretation is clinically sensitive
- FT3 low has known activation-layer blockers
- package activation state may change
- runtime signal behaviour may change
- clinical safety and wording boundaries are in scope
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
work/BATCH2-MINIMUM-COVERAGE-1-androgen-ft3-low-clinical-and-runtime-completion
```

Do not work on `main`.

Do not merge.

---

## Non-negotiable constraints

This sprint must not:

```text
- invent clinical sign-off
- activate androgen packages without valid clinical authority
- activate FT3 low without resolving both activation blockers
- activate any package without explicit STOP-gate evidence
- change clinical thresholds without explicit reviewed authority
- change signal IDs
- change activation keys unless a STOP gate explicitly approves it
- use global/default reference ranges where lab ranges are available
- change SSOT biomarker definitions unless explicitly required and separately justified
- change frontend code
- introduce frontend medical inference
- introduce fallback or dummy parsers
- introduce raw Pass 3 / investigation-spec runtime reads
- introduce LLM clinical reasoning into deterministic signal evaluation
```

If activation cannot be justified, the correct outcome is not to force activation. The correct outcome is a formal `DEFER_PENDING_EXTERNAL_CLINICAL_AUTHORITY`, `EXCLUDE_FROM_MINIMUM_COVERAGE`, or `DO_NOT_ACTIVATE` decision.

---

## Authoritative inputs

Read before implementation:

```text
docs/audit-papers/ARCH-COMPLETION-1_final_runtime_context_and_orchestrator_restructure.md
docs/audit-papers/BATCH2-CONTEXT-COMPLETION-1_runtime_semantics_and_stop_gated_activation.md
docs/audit-papers/CONTEXT-CLEARANCE-1_context_semantics_and_batch2_clearance.md
docs/audit-papers/DAY-ONE-ARCHITECTURE-CLOSURE-REVIEW.md
docs/sprints/launch_core_carry_forward_register.md

knowledge_bus/governance/batch2_context_clearance_register_v1.yaml
knowledge_bus/governance/batch2_remaining_blockers_execution_register_v1.yaml
knowledge_bus/governance/batch2_remainder_resolution_register_v1.yaml
knowledge_bus/governance/batch2_androgen_panel_medical_review_v1.yaml
knowledge_bus/governance/batch2_androgen_context_modifier_binding_v1.yaml
knowledge_bus/governance/context_runtime_execution_register_v1.yaml
knowledge_bus/governance/runtime_context_requirements_model_v1.yaml
knowledge_bus/governance/runtime_context_semantics_model_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

Inspect all package folders for the 9 remaining packages:

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

Also inspect:

```text
backend/core/pipeline/orchestrator.py
backend/core/analytics/runtime_context_evaluator.py
backend/core/analytics/signal_evaluator.py
backend/tests/regression/test_runtime_context_evaluation.py
backend/tests/regression/test_context_threading.py
```

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
4. AnalysisContext now precedes signal evaluation.
5. Runtime context is derived from AnalysisContext or governed post-context object.
6. All 8 androgen packages are currently inactive.
7. FT3 low is currently inactive.
8. No activation approval currently exists.
9. Repository secret-file gate failure remains remediated.
```

STOP if the baseline is unclear.

---

# Phase 1 — Read-only Batch 2 remainder classification

Before changing package or runtime state, produce a read-only classification table for all 9 packages.

For each package, report:

```text
- package path
- biomarker / signal
- current activation state
- current blocker status
- required companion biomarkers
- required runtime context
- current lower/upper bound settings
- clinical authority present? YES / NO / INCONCLUSIVE
- activation-layer blockers
- runtime blockers
- governance blockers
- recommendation
```

Allowed recommendations:

```text
ACTIVATE_WITH_GATES
EXCLUDE_FROM_MINIMUM_COVERAGE
DEFER_PENDING_EXTERNAL_CLINICAL_AUTHORITY
DO_NOT_ACTIVATE
```

STOP if the package list cannot be reconciled with the governance registers.

---

# Phase 2 — Clinical authority check

## Androgen packages

The 8 androgen packages must not be activated unless valid clinical authority exists.

Valid authority must be a repo artefact that clearly supports cautious educational interpretation of the specific androgen pattern.

For each androgen package, determine whether the existing files provide enough authority to activate:

```text
knowledge_bus/governance/batch2_androgen_panel_medical_review_v1.yaml
knowledge_bus/governance/batch2_androgen_context_modifier_binding_v1.yaml
package research_brief.yaml
package signal_library.yaml
package package_manifest.yaml
any linked medical review artefacts
```

The required question is not:

```text
Can this be medically true?
```

The required question is:

```text
Is there enough governed clinical authority to activate this pattern safely in HealthIQ’s deterministic runtime?
```

If the answer is no, do not activate.

## FT3 low

FT3 low must not be activated unless all known blockers are resolved.

Known blockers include:

```text
- enable_lower_bound: false
- missing or incomplete thyroid medication disclosed context
- illness/recovery context requirements
- risk of over-interpreting low T3 syndrome / non-thyroidal illness
```

FT3 low must be assessed as a cautious interpretation pattern only, not a diagnosis.

---

# Phase 3 — Minimum coverage decision

For each package, decide whether it belongs in the minimum pre-beta biomarker coverage set.

Use this decision logic:

## Include / activate candidate

Only if:

```text
- clinical authority is sufficient
- runtime context requirements are deterministic and available
- companion biomarker requirements are explicit
- activation can fail closed safely
- package metadata is internally coherent
- no threshold/reference-range changes are needed without authority
- no frontend/report compiler changes are required
```

## Exclude from minimum coverage

Allowed if:

```text
- the biomarker/pattern is not required for minimum credible pre-beta coverage
- activation would require specialist clinical review not yet available
- the interpretation is too context-sensitive for deterministic runtime today
- safer active coverage already exists
```

## Defer pending external clinical authority

Required if:

```text
- the package may be valuable
- but the current repo does not contain sufficient clinical sign-off
```

## Do not activate

Required if:

```text
- package metadata is unsafe
- clinical interpretation is not sufficiently coherent
- activation would create misleading output
- required context cannot be captured deterministically
```

---

# Phase 4 — Internal STOP gate before any activation

Before any package activation, produce a STOP-gate table.

Columns:

```text
Package
Current state
Clinical authority
Runtime context complete?
Companion biomarkers complete?
Lower/upper bound settings correct?
Known blockers resolved?
Recommended action
Evidence
```

No package may receive `ACTIVATE_WITH_GATES` unless all relevant fields are positive.

If any androgen package is recommended for activation, the audit must explicitly explain how CF-BATCH2-010 is resolved.

If CF-BATCH2-010 is not resolved, all androgen packages must remain inactive.

If FT3 low is recommended for activation, the audit must explicitly explain how:

```text
enable_lower_bound: false
thyroid_medication_disclosed
illness_or_recovery_status_disclosed
```

have been resolved.

Activation requires explicit human approval phrase:

```text
APPROVE BATCH2 MINIMUM COVERAGE ACTIVATION
```

If that exact approval phrase is not present, do not activate packages.

---

# Phase 5 — Conditional implementation

Only proceed to implementation if the STOP gate supports action.

Allowed implementation actions:

```text
- update activation/governance registers
- activate package(s) that passed the STOP gate and received explicit approval
- update runtime context requirements only where clearly governed
- update package metadata only if required for a package that passed clinical authority review
- add tests for activation/fail-closed behaviour
- update carry-forward register
```

Forbidden implementation actions:

```text
- broad runtime redesign
- frontend changes
- report compiler changes
- scoring changes
- SSOT changes
- unreviewed threshold changes
- unreviewed clinical wording changes
- raw research runtime reads
- LLM reasoning inside signal evaluation
```

If no package passes the STOP gate, implementation should be limited to governance documentation and carry-forward clarification.

---

# Phase 6 — Required tests

If any package is activated, add or update tests proving:

```text
1. activated package fires only when biomarker direction and context requirements are met
2. activated package fails closed when required context is missing
3. positive and negative disclosed-context answers behave correctly
4. companion biomarker gates work
5. unrelated active signals are unchanged
6. androgen packages remain inactive unless specifically approved
7. FT3 low remains inactive unless specifically approved
8. no duplicate/conflicting signals are introduced
9. no active signal output format changes unexpectedly
```

If no package is activated, add or update tests only if needed to preserve the inactive/fail-closed state.

---

# Phase 7 — Required validation

Run and paste full output.

## Architecture / governance validators

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_day_one_architecture.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

## Context safety regressions

```powershell
python -m pytest backend/tests/regression/test_runtime_context_evaluation.py -q
python -m pytest backend/tests/regression/test_context_threading.py -q
```

## Signal / package tests

Run all relevant signal evaluator, package activation, governance and context package tests.

If package validators exist, run them for all 9 package directories.

If no validator exists, report that as an evidence gap.

## Secret-file guardrail

Run:

```powershell
python scripts/check_no_secret_files.py
```

if present.

---

# Phase 8 — Required audit paper

Create:

```text
docs/audit-papers/BATCH2-MINIMUM-COVERAGE-1_androgen_ft3_low_clinical_and_runtime_completion.md
```

The audit paper must include:

```text
- executive verdict
- files inspected
- files changed
- full 9-package classification table
- androgen clinical authority assessment
- FT3 low blocker assessment
- minimum coverage decision
- STOP-gate table
- activation decision for every package
- confirmation whether exact approval phrase was present
- confirmation no unauthorised activation occurred
- confirmation no package metadata changed unless authorised
- confirmation no SSOT changed
- confirmation no scoring changed
- confirmation no report compiler changed
- confirmation no frontend changed
- confirmation no raw research runtime reads introduced
- validator output in full
- test output in full
- rollback path
- carry-forward impact
- recommended next action
```

Validation and test output must be pasted in full, not summarised.

---

# Phase 9 — Carry-forward handling

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

only if justified.

Expected possible outcomes:

```text
CF-BATCH2-010 remains Open
CF-BATCH2-010 resolved
FT3 low deferred with explicit minimum-coverage exclusion
FT3 low activated with gates
Androgen packages deferred pending external authority
Androgen packages activated with gates
```

Do not close `CF-BATCH2-010` unless clinical authority is genuinely sufficient and documented.

Do not close FT3 low blockers unless the lower-bound and context issues are genuinely resolved.

---

## Expected changed files

Expected changed files may include:

```text
knowledge_bus/governance/batch2_context_clearance_register_v1.yaml
knowledge_bus/governance/context_runtime_execution_register_v1.yaml
docs/sprints/launch_core_carry_forward_register.md
docs/audit-papers/BATCH2-MINIMUM-COVERAGE-1_androgen_ft3_low_clinical_and_runtime_completion.md
backend/tests/regression/test_runtime_context_evaluation.py
backend/tests/regression/test_context_threading.py
backend/tests/governance/*
automation_bus/latest_cursor_status.json
```

Package files may change only if a package passes the STOP gate and exact human approval phrase is present.

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
- androgen packages without CF-BATCH2-010 resolution
- FT3 low without lower-bound/context blocker resolution
- any package without exact human approval phrase
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
1. the 9-package remainder cannot be reconciled with governance registers
2. androgen clinical authority is missing or inconclusive
3. FT3 low lower-bound blocker remains unresolved
4. FT3 low medication/illness context remains unresolved
5. activation would require threshold changes without authority
6. activation would require frontend/report compiler changes
7. activation would require scoring changes
8. activation would require SSOT changes
9. package metadata changes are needed but approval phrase is absent
10. exact approval phrase is absent and activation would otherwise occur
11. context gates cannot fail closed
12. validators fail
13. tests fail
14. secret-file guardrail fails
15. rollback path cannot be defined
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
docs(governance): classify Batch 2 minimum coverage remainder
```

If activation is approved and performed, use:

```text
feat(signals): activate approved Batch 2 minimum coverage packages
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
- all 9 remaining packages are classified
- androgen clinical authority is assessed
- FT3 low blockers are assessed
- each package has a final minimum-coverage decision
- no unauthorised activation occurs
- no vague “later” state remains
- validators pass
- tests pass
- audit paper contains full evidence
- carry-forwards are updated only where justified
```

A successful outcome does not require activation.

A successful outcome does require a clear governed decision for every remaining package.

Expected next action after success:

```text
If packages are activated:
  proceed to ARCH-COMPLETION-2 compiled card/root-cause authority completion.

If packages are excluded/deferred:
  proceed to ARCH-COMPLETION-2 with the minimum biomarker estate explicitly defined.

If clinical authority is missing:
  run a focused external medical authority/sign-off workflow before activation.
```
