---
work_id: ARCH-COMPLETION-1_final_runtime_context_and_orchestrator_restructure
branch: work/ARCH-COMPLETION-1-final-runtime-context-and-orchestrator-restructure
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# ARCH-COMPLETION-1 — Final Runtime Context and Orchestrator Restructure

## Purpose

Complete the orchestrator phase-order correction required by `ARCH-ORCH-RESTRUCTURE-1`.

The current orchestrator still uses an interim bridge in which context-dependent signal evaluation receives runtime context derived directly from raw `questionnaire_data` before the fully assembled `AnalysisContext` exists.

That bridge was acceptable only while all context-dependent packages remained inactive.

This sprint must replace that bridge with the recommended target architecture:

```text
normalise input
→ assemble governed AnalysisContext
→ derive runtime context from AnalysisContext
→ run signal evaluation
→ run downstream analytics / cards / narratives / DTO assembly
```

The goal is not to rewrite the whole product.

The goal is to fix the orchestrator phase order once properly, so the orchestrator becomes a clean pipeline coordinator rather than a source of hidden context behaviour.

---

## Strategic rationale

HealthIQ AI is not currently being released to beta users.

The human owner has decided that the correct priority is to complete the backend intelligence foundation before frontend polish or beta preparation.

This sprint therefore reclassifies `ARCH-ORCH-RESTRUCTURE-1` from an acceptable Wave 1 residual into pre-beta foundation work.

The sprint must establish the best recommended orchestrator architecture for the current product stage.

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
- backend/core/pipeline/orchestrator.py may be changed
- backend/core/pipeline/orchestrator_phases_v1.py may be changed
- runtime phase ordering may change
- signal evaluation input source may change
- context-dependent package safety depends on the result
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
work/ARCH-COMPLETION-1-final-runtime-context-and-orchestrator-restructure
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
- change package signal_library.yaml files
- change signal IDs
- change activation keys
- change clinical thresholds
- change biomarker reference range policy
- change SSOT biomarker definitions
- change scoring
- change report compiler logic
- change frontend code
- introduce frontend medical inference
- introduce fallback or dummy parsers
- introduce raw Pass 3 / investigation-spec runtime reads
- add LLM-based clinical reasoning
- change clinical wording unless forced by existing tests and explicitly justified
```

The output of currently active signals must remain behaviourally stable unless a test proves the current behaviour is wrong and the change is explicitly documented.

---

## Authoritative inputs

Read before implementation:

```text
docs/audit-papers/DAY-ONE-ARCHITECTURE-CLOSURE-REVIEW.md
docs/audit-papers/BETA-READINESS-RECHECK-1_post_launch_fixes_readiness_gate.md
docs/audit-papers/CONTEXT-RUNTIME-1_reusable_runtime_context_evaluation_layer.md
docs/audit-papers/CONTEXT-THREADING-1_runtime_context_orchestrator_threading.md
docs/audit-papers/CONTEXT-CLEARANCE-1_context_semantics_and_batch2_clearance.md
docs/audit-papers/BATCH2-CONTEXT-COMPLETION-1_runtime_semantics_and_stop_gated_activation.md
docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/sprints/launch_core_carry_forward_register.md
```

Also inspect:

```text
backend/core/pipeline/orchestrator.py
backend/core/pipeline/orchestrator_phases_v1.py
backend/core/analytics/runtime_context_evaluator.py
backend/core/analytics/signal_evaluator.py
backend/core/context.py
backend/core/models.py
backend/core/data/validation.py
knowledge_bus/governance/context_runtime_execution_register_v1.yaml
knowledge_bus/governance/batch2_context_clearance_register_v1.yaml
knowledge_bus/governance/runtime_context_requirements_model_v1.yaml
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
3. Repository secret-file gate failure is no longer present in tracked files.
4. BETA-READINESS-RECHECK-1 exists and records beta readiness as not claimed.
5. Context-dependent Batch 2 packages are currently inactive.
6. FT3 low is currently inactive.
7. All 8 androgen packages are currently inactive.
8. No explicit activation approval exists.
```

STOP if baseline state is unclear.

---

## Current known architectural defect

The current architecture contains this known defect:

```text
Signal evaluation receives runtime context before the fully assembled AnalysisContext exists.
```

The current interim bridge:

```text
build_runtime_context_snapshot(questionnaire_responses=questionnaire_data)
```

or equivalent logic reads raw questionnaire payload before the governed `AnalysisContext` has been created.

This was previously accepted only because:

```text
- context-dependent packages were inactive
- no active package relied on those gates
- the bridge was deterministic and fail-closed
```

It is not the final target architecture.

---

## Target architecture

After this sprint, the orchestrator should follow this high-level phase order:

```text
1. Receive raw request / input DTO
2. Validate and normalise biomarkers
3. Prepare demographic and questionnaire inputs
4. Create governed AnalysisContext
5. Build RuntimeContextSnapshot from AnalysisContext or equivalent governed context object
6. Run SignalEvaluator.evaluate_all(..., runtime_context=runtime_context)
7. Run downstream analytics, scoring, card evidence, root-cause, narrative and DTO assembly
```

The orchestrator should coordinate phases.

It should not perform medical reasoning itself.

It should not inspect raw research.

It should not become a parallel intelligence authority.

---

## Required design principle

The runtime context used by signal evaluation must be derived from governed assembled context, not raw questionnaire payload.

Preferred implementation:

```text
AnalysisContext
→ RuntimeContextSnapshot
→ SignalEvaluator.evaluate_all(runtime_context=...)
```

Acceptable implementation:

```text
a clearly named governed context object produced after AnalysisContext assembly
→ RuntimeContextSnapshot
→ SignalEvaluator.evaluate_all(runtime_context=...)
```

Unacceptable implementation:

```text
raw questionnaire_data
→ RuntimeContextSnapshot
→ SignalEvaluator before AnalysisContext
```

---

## In scope

This sprint may modify:

```text
backend/core/pipeline/orchestrator.py
backend/core/pipeline/orchestrator_phases_v1.py
backend/core/analytics/runtime_context_evaluator.py
backend/tests/regression/test_context_threading.py
backend/tests/regression/test_runtime_context_evaluation.py
backend/tests/architecture/*
docs/audit-papers/*
docs/sprints/launch_core_carry_forward_register.md
```

Only modify `runtime_context_evaluator.py` if needed to create a clean `AnalysisContext` → `RuntimeContextSnapshot` adapter.

Only modify `signal_evaluator.py` if absolutely necessary, and explain why the existing `runtime_context` parameter is insufficient.

---

## Out of scope

Do not modify:

```text
knowledge_bus/packages/**
backend/ssot/**
backend/core/reporting/**
backend/core/scoring/**
frontend/**
```

Do not modify package activation registers except to confirm that inactive packages remain inactive.

Do not change package metadata.

Do not change clinical content.

Do not change thresholds.

Do not change report output wording unless unavoidable and explicitly justified.

---

# Phase 1 — Read-only design audit

Before changing code, produce a short implementation design note in the sprint audit paper or Cursor status.

Answer:

```text
1. Where is AnalysisContext currently created?
2. Where is signal evaluation currently invoked?
3. Where is runtime context currently built?
4. Which exact line/order causes the current inversion?
5. What is the minimal safe phase reordering?
6. Can SignalEvaluator already receive runtime_context without interface changes?
7. Can RuntimeContextSnapshot be built from AnalysisContext without weakening semantics?
8. Which tests currently protect context threading?
9. Which active outputs must remain unchanged?
```

STOP if the required change requires a broad orchestrator rewrite rather than a phase-order correction.

---

# Phase 2 — Implement final context phase ordering

Restructure the orchestrator so that:

```text
AnalysisContext is created before context-dependent signal evaluation.
```

Then ensure signal evaluation receives runtime context derived from that assembled context.

Expected pattern:

```text
context = create_analysis_context(...)
runtime_context = build_runtime_context_snapshot_from_context(context)
signals = signal_evaluator.evaluate_all(..., runtime_context=runtime_context)
```

or equivalent.

The exact function names may differ, but the architectural flow must be clear.

If the current `build_runtime_context_snapshot()` only accepts raw questionnaire input, extend it safely rather than keeping the raw bridge.

Any new helper must be deterministic and test-covered.

---

# Phase 3 — Remove or neutralise the raw questionnaire bridge

Remove the old interim behaviour where signal evaluation relies on:

```text
questionnaire_data
```

before `AnalysisContext` exists.

It is acceptable for raw questionnaire data to be used in constructing `AnalysisContext`.

It is not acceptable for context-dependent signal evaluation to bypass `AnalysisContext` once this sprint is complete.

Search for and inspect:

```text
build_runtime_context_snapshot(questionnaire_responses=questionnaire_data)
runtime_context_snapshot(questionnaire_data)
evaluate_all(... questionnaire_data ...)
```

The final implementation must make it clear that signal evaluation is downstream of context assembly.

---

# Phase 4 — Preserve inactive package safety

Confirm no activation changes.

Required checks:

```text
- all 8 androgen packages remain inactive
- FT3 low remains inactive
- activated_package_count remains 0 for context-dependent Batch 2 packages
- approval_received remains false unless explicit approval evidence exists
- no package signal_library.yaml files changed
```

Add or update tests if necessary.

This sprint must not be used as a back door to activate context-dependent packages.

---

# Phase 5 — Regression tests

Add or update tests proving:

```text
1. AnalysisContext is created before signal evaluation.
2. Runtime context passed to SignalEvaluator is derived from AnalysisContext or a governed post-context object.
3. SignalEvaluator no longer receives context derived directly from raw questionnaire_data before AnalysisContext creation.
4. Existing disclosed-context semantics still pass.
5. Missing context still fails closed.
6. Positive and negative disclosure answers still satisfy disclosed requirements.
7. Active signal output is unchanged for representative panels.
8. Context-dependent inactive packages remain inactive.
```

If direct phase-order testing is difficult, add the narrowest robust test using mocks/spies/instrumentation around orchestrator phase calls.

Do not rely only on implementation comments.

---

# Phase 6 — Required validation

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

## Orchestrator / pipeline regressions

Run existing orchestrator and pipeline tests.

If there is no direct orchestrator test coverage, add targeted tests and run them.

Suggested search:

```powershell
python -m pytest backend/tests -q -k "orchestrator or pipeline or context"
```

Do not rely on broad passing tests only. There must be at least one direct test proving the new phase ordering.

## Safety checks

Run:

```powershell
python scripts/check_no_secret_files.py
```

if present.

Run grep/search evidence proving forbidden package files were not modified.

---

# Phase 7 — Required audit paper

Create:

```text
docs/audit-papers/ARCH-COMPLETION-1_final_runtime_context_and_orchestrator_restructure.md
```

The audit paper must include:

```text
- executive verdict
- files inspected
- files changed
- previous orchestrator phase order
- new orchestrator phase order
- explanation of how AnalysisContext now precedes signal evaluation
- explanation of how RuntimeContextSnapshot is derived
- confirmation raw questionnaire bridge removed or neutralised
- confirmation SignalEvaluator interface remains stable or explanation if changed
- confirmation all context-dependent packages remain inactive
- confirmation no package metadata changed
- confirmation no clinical thresholds changed
- confirmation no scoring changed
- confirmation no report compiler changed
- confirmation no SSOT changed
- confirmation no frontend changed
- full validator output
- full test output
- rollback path
- carry-forward impact
```

Validation and test output must be pasted in full, not summarised.

---

# Phase 8 — Carry-forward handling

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

only if the implementation genuinely closes `ARCH-ORCH-RESTRUCTURE-1`.

Do not close unrelated carry-forwards.

If closed, record:

```text
ARCH-ORCH-RESTRUCTURE-1: Resolved by ARCH-COMPLETION-1. Signal evaluation now receives runtime context derived from AnalysisContext / governed post-context object rather than raw questionnaire_data bridge.
```

If not fully closed, leave it open and explain the remaining gap.

---

## Expected changed files

Expected changed files may include:

```text
backend/core/pipeline/orchestrator.py
backend/core/pipeline/orchestrator_phases_v1.py
backend/core/analytics/runtime_context_evaluator.py
backend/tests/regression/test_context_threading.py
backend/tests/regression/test_runtime_context_evaluation.py
backend/tests/architecture/*
docs/audit-papers/ARCH-COMPLETION-1_final_runtime_context_and_orchestrator_restructure.md
docs/sprints/launch_core_carry_forward_register.md
automation_bus/latest_cursor_status.json
```

No package files are expected to change.

No SSOT files are expected to change.

No frontend files are expected to change.

---

## Forbidden changes

Do not change:

```text
knowledge_bus/packages/**
backend/ssot/**
backend/core/reporting/**
backend/core/scoring/**
frontend/**
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
1. AnalysisContext creation cannot be moved before signal evaluation without broad pipeline rewrite.
2. RuntimeContextSnapshot cannot be derived from AnalysisContext or governed post-context object.
3. SignalEvaluator interface must be redesigned broadly.
4. Active signal outputs change unexpectedly.
5. Any context-dependent package would become active.
6. Any package metadata change is required.
7. Any clinical threshold or reference range change is required.
8. Any frontend change is required.
9. Any report compiler or scoring change is required.
10. Architecture validators fail.
11. Context runtime tests fail.
12. Orchestrator phase-order tests cannot be written.
13. Secret-file guardrail fails.
14. Working tree contains untracked local secret files.
15. Rollback path cannot be defined.
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
refactor(orchestrator): derive signal runtime context after analysis context assembly
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
- AnalysisContext is assembled before signal evaluation
- runtime context passed to SignalEvaluator is derived from AnalysisContext or governed post-context object
- interim raw questionnaire_data bridge is removed or neutralised
- active outputs remain stable
- context-dependent packages remain inactive
- androgen packages remain inactive
- FT3 low remains inactive
- no package metadata changes
- no SSOT changes
- no scoring changes
- no report compiler changes
- no frontend changes
- architecture validators pass
- context runtime tests pass
- direct orchestrator phase-order test passes
- audit paper contains full evidence
- ARCH-ORCH-RESTRUCTURE-1 is either closed with evidence or remains open with a precise residual
```

Expected next action after success:

```text
Proceed to BATCH2-MINIMUM-COVERAGE-1_androgen_ft3_low_clinical_and_runtime_completion.
```

Do not proceed to Batch 2 completion until this orchestrator foundation is complete and approved.
