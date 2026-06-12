---
work_id: CONTEXT-CLEARANCE-1_context_semantics_and_batch2_clearance
branch: work/CONTEXT-CLEARANCE-1-context-semantics-and-batch2-clearance
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# CONTEXT-CLEARANCE-1 — Context Semantics and Batch 2 Clearance

## Purpose

Define the reusable runtime context semantics required before any remaining context-dependent Batch 2 package can be safely activated.

This sprint must answer one question:

```text
For context-dependent Batch 2 packages, what must be true before runtime activation is safe?
```

This sprint must produce a governed clearance decision for:

```text
- 8 androgen packages
- FT3 low
```

This is not a package activation sprint.

Do not activate:

```text
- androgen packages
- FT3 low
- any other currently inactive package
```

---

## Strategic architecture note

CONTEXT-RUNTIME-1 created fail-closed runtime context evaluation.

CONTEXT-THREADING-1 made that context capability live in the orchestrator via raw `questionnaire_data`.

However, androgen activation remains blocked because the current context requirement semantics may incorrectly treat fields such as:

```text
medication.hormone_therapy: present
clinical_context.aas_exposure: present
```

as meaning:

```text
the patient is on hormone therapy / has AAS exposure
```

rather than:

```text
the patient has disclosed whether hormone therapy / AAS exposure applies
```

That is a false-negative risk and must be resolved before activation.

The target model must distinguish:

```text
1. hard prerequisite gates
2. disclosed context requirements
3. optional interpretation modifiers
4. companion biomarker requirements
5. activation eligibility decisions
```

These concepts must not be collapsed into one boolean gate.

---

## Governance classification

This sprint is HIGH risk / MIXED because it affects governed runtime package eligibility and context semantics for Intelligence Core signal emission.

Required route:

```text
Cursor implementation
Claude hardening / audit
GPT architectural review
Human approval before merge
```

No merge is permitted without GPT architectural review.

---

## Authoritative inputs

Read before implementation:

```text
docs/sprints/launch_core_carry_forward_register.md
docs/audit-papers/CONTEXT-RUNTIME-1_reusable_runtime_context_evaluation_layer.md
docs/audit-papers/CONTEXT-THREADING-1_runtime_context_orchestrator_threading.md
CONTEXT-THREADING-1_pre_sprint_architecture_audit.md

knowledge_bus/governance/runtime_context_requirements_model_v1.yaml
knowledge_bus/governance/context_runtime_execution_register_v1.yaml
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
knowledge_bus/governance/batch2_remaining_blockers_execution_register_v1.yaml
knowledge_bus/governance/batch2_remainder_resolution_register_v1.yaml
knowledge_bus/governance/batch2_androgen_panel_medical_review_v1.yaml
knowledge_bus/governance/batch2_androgen_context_modifier_binding_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml

docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL.md
```

Also inspect all 9 context-dependent Batch 2 packages:

```text
FT3 low package
8 androgen packages
```

Confirm their exact paths from the repo before editing.

---

## Authority preflight

Before making changes, verify and report:

```text
1. The authoritative runtime context semantics source file.
2. The runtime evaluator that consumes package-declared runtime_context_requirements.
3. The package files that currently declare runtime_context_requirements.
4. The current activation status of FT3 low.
5. The current activation status of all 8 androgen packages.
6. That no duplicate context semantics authority exists.
7. That any proposed new semantics file does not create a second competing authority.
8. That any tests reference the same authority source as runtime/governance.
```

STOP if the authoritative context semantics location cannot be identified.

---

## Reality check

Before editing, verify whether the problem still exists.

Confirm:

```text
- CF-CONTEXT-SEMANTICS-1 is still Open.
- CF-BATCH2-010 is still Open.
- FT3 low remains inactive.
- all 8 androgen packages remain inactive.
- hormone_therapy / AAS exposure semantics are still ambiguous or unsafe for activation.
```

If the problem no longer exists, STOP and report instead of proceeding.

---

## Scope

This sprint must produce:

```text
1. A reusable context requirement semantics model.
2. A hard gate vs disclosed context vs modifier distinction.
3. An androgen clearance matrix covering all 8 androgen packages.
4. An FT3 low clearance decision.
5. A package-level activation eligibility list.
6. A deferred / non-launch-critical list if required.
7. Updated carry-forward register entries.
8. Tests / validators proving the semantics model is structurally valid.
9. An audit paper explaining decisions and remaining blockers.
```

---

## Required semantic model

The sprint must define or update a governed semantics model that distinguishes:

### Hard prerequisite gate

A condition required before signal emission can safely occur.

Examples:

```text
- biological sex available where sex-specific interpretation is required
- age available where age-specific interpretation is required
- SHBG available where FAI/free testosterone interpretation requires SHBG
- TSH and FT4 available where FT3 low interpretation requires thyroid context
```

### Disclosed context requirement

A requirement that the user has answered or disclosed a context field, regardless of whether the answer is positive or negative.

Examples:

```text
- hormone therapy status disclosed: yes/no/unknown
- AAS exposure status disclosed: yes/no/unknown
- relevant medication status disclosed: yes/no/unknown
```

This must not mean the condition is present.

### Interpretation modifier

A context item that may alter interpretation wording, confidence, caution level, or explanatory framing, but should not automatically suppress signal emission unless explicitly promoted to a hard prerequisite.

Examples:

```text
- hormone therapy
- AAS exposure
- supplements
- endocrine history
- symptoms
- recent illness/recovery
```

### Companion biomarker requirement

A required biomarker dependency for specific frames.

Examples:

```text
- SHBG for FAI / free testosterone percentage contexts where clinically required
- FT4 and TSH for FT3 low context
```

---

## Batch 2 clearance requirements

### Androgen packages

For each of the 8 androgen packages, produce a row containing:

```text
- package_id
- signal_id
- activation_key
- source_spec_id
- current runtime authority status
- current runtime_context_requirements
- required hard gates
- required disclosed context
- optional modifiers
- companion biomarker requirements
- clinical sign-off status
- clearance decision
- reason
- activation eligibility
```

Allowed clearance decisions:

```text
CLEARED_FOR_STOP_GATED_ACTIVATION
BLOCKED_PENDING_CLINICAL_SIGNOFF
BLOCKED_PENDING_CONTEXT_SEMANTICS
BLOCKED_PENDING_COMPANION_BIOMARKER
DEFERRED_NON_LAUNCH_CRITICAL
REJECTED_DO_NOT_ACTIVATE
```

### FT3 low

Produce the same clearance assessment for FT3 low.

FT3 low must not be activated unless the sprint can prove that the required TSH + FT4 + illness/medication context model is safe and deterministic.

---

## Required outputs

Create or update appropriate governance artefacts.

Expected outputs may include:

```text
knowledge_bus/governance/runtime_context_semantics_model_v1.yaml
knowledge_bus/governance/batch2_context_clearance_register_v1.yaml
docs/audit-papers/CONTEXT-CLEARANCE-1_context_semantics_and_batch2_clearance.md
docs/sprints/launch_core_carry_forward_register.md
backend/tests/governance/test_runtime_context_semantics_model.py
backend/tests/governance/test_batch2_context_clearance_register.py
```

If different file paths are used, explain why.

Do not modify runtime pipeline code unless validation proves it is absolutely required. If runtime code changes appear necessary, STOP and report before continuing.

---

## Explicit non-goals

This sprint must not:

```text
- activate androgen packages
- activate FT3 low
- change runtime package activation metadata to active
- change clinical thresholds
- change lab reference range policy
- change scoring
- change frontend
- change report compiler
- change SSOT biomarker definitions
- change signal IDs
- change activation keys
- change orchestrator phase ordering
- refactor runtime pipeline
- alter existing active package behaviour
- introduce fallback or dummy parsers
- introduce raw Pass 3 runtime reads
- add LLM interpretation logic
```

---

## Package modification rules

Package metadata may only be changed if required to encode corrected, governed context semantics.

If any package `signal_library.yaml` is modified, Cursor must:

```text
1. list each modified package
2. explain the exact semantic correction
3. prove no activation status changed
4. run package validation for each touched package
5. prove the change does not alter thresholds, clinical wording, signal_id, activation_key, or reference ranges
```

If package changes are not necessary, do not touch package files.

---

## Required carry-forward handling

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Required logic:

```text
CF-CONTEXT-SEMANTICS-1:
- mark Resolved only if the sprint creates a governed semantics model distinguishing hard gates, disclosed context, modifiers, and companion biomarker requirements
- otherwise keep Open and explain remaining blocker

CF-BATCH2-010:
- must remain Open unless a clinical sign-off artefact is created or verified
- if androgen clinical sign-off remains incomplete, state that androgen activation remains blocked

ARCH-ORCH-RESTRUCTURE-1:
- must remain Open
- do not claim this sprint resolves final orchestrator phase ordering

CF-CONTEXT-MOD-3:
- must remain Resolved at capability/threading level
- note that package activation is still governed separately
```

Do not create one carry-forward per androgen marker.

---

## Required audit report

Create:

```text
docs/audit-papers/CONTEXT-CLEARANCE-1_context_semantics_and_batch2_clearance.md
```

The report must include:

```text
- executive verdict
- files inspected
- files changed
- authority preflight result
- reality check result
- semantic model summary
- androgen clearance matrix summary
- FT3 low decision summary
- activation eligibility list
- deferred / non-launch-critical list
- confirmation no activation occurred
- confirmation FT3 low remains inactive
- confirmation all androgen packages remain inactive
- confirmation no clinical thresholds changed
- confirmation no reference range policy changed
- confirmation no frontend / SSOT / scoring / report compiler changed
- validation output pasted in full
- test output pasted in full
- rollback path
- residual architectural observations
- recommended next sprint
```

Validation output must be pasted in full, not summarised.

---

## Required validations

Run and paste actual output:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
python -m pytest backend/tests/regression/test_runtime_context_evaluation.py -q
```

Also run any new tests created by this sprint, for example:

```powershell
python -m pytest backend/tests/governance/test_runtime_context_semantics_model.py -q
python -m pytest backend/tests/governance/test_batch2_context_clearance_register.py -q
```

If package files are modified, run:

```powershell
python backend/scripts/validate_knowledge_package.py --package-dir <each_touched_package_dir>
```

If a validator does not exist for a new governance artefact, either:

```text
- create a narrow validator/test for it, or
- STOP and explain why validation cannot be provided
```

---

## STOP conditions

STOP and report if:

```text
1. the authoritative context semantics source cannot be identified
2. the sprint would create a duplicate context semantics authority
3. any activation is required to complete the sprint
4. androgen clinical sign-off cannot be found and clearance would require inventing clinical approval
5. FT3 low clearance would require inventing illness/medication logic not present in governed artefacts
6. runtime pipeline changes are required
7. SignalEvaluator changes are required
8. package activation metadata would need to change
9. thresholds, clinical wording, reference ranges, scoring, SSOT, frontend, or report compiler would need to change
10. validators fail
11. tests fail
12. the clearance matrix cannot identify every one of the 8 androgen packages
13. the sprint cannot prove FT3 low and all androgen packages remain inactive
14. rollback path cannot be defined
```

---

## Expected changed files

Expected changed files should be limited to governance, tests, audit and carry-forward documentation, for example:

```text
knowledge_bus/governance/runtime_context_semantics_model_v1.yaml
knowledge_bus/governance/batch2_context_clearance_register_v1.yaml
backend/tests/governance/test_runtime_context_semantics_model.py
backend/tests/governance/test_batch2_context_clearance_register.py
docs/audit-papers/CONTEXT-CLEARANCE-1_context_semantics_and_batch2_clearance.md
docs/sprints/launch_core_carry_forward_register.md
```

Package files may only be touched if necessary to encode corrected context semantics and must be validated individually.

Runtime code files are not expected to change.

If any file outside expected scope changes, STOP and explain before commit.

---

## Commit requirements

Before commit, report:

```powershell
git diff --name-only
git status --short
```

Commit message:

```text
docs(governance): define context clearance for Batch 2 packages
```

If tests or validators are added, use:

```text
test(governance): validate Batch 2 context clearance model
```

or a single combined commit:

```text
chore(governance): define Batch 2 context clearance model
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
- reusable context semantics are defined
- hard gates, disclosed context, modifiers, and companion biomarker requirements are separated
- all 8 androgen packages have a clearance decision
- FT3 low has a clearance decision
- activation eligibility list exists
- deferred / non-launch-critical list exists if required
- no package activation occurred
- all validators and tests pass
- carry-forward register is updated correctly
- next activation sprint can be scoped without re-litigating semantics
```

The expected next sprint, if this passes, is:

```text
BATCH2-CONTEXT-ACTIVATION-1_stop_gated_context_package_activation
```

That next sprint must activate only packages explicitly cleared by this sprint and must not re-open semantic or clinical sign-off decisions.
