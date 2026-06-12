---
work_id: CONTEXT-THREADING-1_runtime_context_orchestrator_threading
branch: work/CONTEXT-THREADING-1-runtime-context-orchestrator-threading
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# CONTEXT-THREADING-1 — Runtime Context Orchestrator Threading

## Purpose

Wire the reusable runtime context evaluator into the live analysis pipeline.

CONTEXT-RUNTIME-1 created the reusable context evaluation capability, including:

* `backend/core/analytics/runtime_context_evaluator.py`
* `build_runtime_context_snapshot()`
* package-declared `runtime_context_requirements`
* `SignalEvaluator.evaluate_all(..., runtime_context=None)`
* fail-closed runtime context gating

However, the pre-sprint architecture audit found that the live orchestrator does not yet pass questionnaire, demographic, medication, supplement, symptom, illness, or known-condition context into signal evaluation.

This sprint must complete the missing runtime threading step.

This is not a package activation sprint.

Do not activate:

* FT3 low
* androgen packages
* any other currently inactive package

Do not change androgen context semantics in this sprint.

---

## Strategic architecture alignment note

This sprint is an interim runtime-threading bridge, not the final orchestrator architecture.

The accepted ADR target remains:

```text
canonical research authority
→ governed compile
→ compiled runtime artefacts
→ thin runtime loaders
→ presentation-safe DTOs
→ frontend render-only
```

The current pipeline is structurally imperfect because signal evaluation currently runs before full `AnalysisContext` creation. `CONTEXT-THREADING-1` must not attempt a broad orchestrator refactor. It may use raw `questionnaire_data` because that is the only context source available before Step 1.6.

This tactical bridge is acceptable because it makes the reusable context evaluator live without activating blocked packages and without widening the runtime rewrite.

However, this sprint must not be represented as completing the final “thin runtime loader” target architecture.

The sprint must record a carry-forward that the day-one architecture / launch-gate work must address orchestrator phase ordering and context assembly so that, in the final architecture, runtime loaders receive already-assembled governed inputs rather than reaching backwards into raw questionnaire payloads.

Success criteria are limited to:

```text
- safe live threading of runtime_context into SignalEvaluator
- no package activation
- no behavioural drift for currently active signals
- explicit carry-forward for final orchestrator restructuring
```

Required carry-forward entry:

```text
ARCH-ORCH-RESTRUCTURE-1

The current orchestrator still performs signal evaluation before full AnalysisContext creation. CONTEXT-THREADING-1 uses raw questionnaire_data as an interim bridge only. Before final day-one architecture acceptance, the runtime pipeline must be reviewed/restructured so context assembly occurs before context-dependent evaluation, consistent with the ADR target of thin runtime loaders receiving governed, assembled inputs.
```

---

## Authoritative inputs

Read before implementation:

```text
docs/audit-papers/CONTEXT-RUNTIME-1_reusable_runtime_context_evaluation_layer.md
knowledge_bus/governance/runtime_context_requirements_model_v1.yaml
knowledge_bus/governance/context_runtime_execution_register_v1.yaml
docs/sprints/launch_core_carry_forward_register.md
CONTEXT-THREADING-1_pre_sprint_architecture_audit.md
docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL.md
```

Also inspect:

```text
backend/core/analytics/runtime_context_evaluator.py
backend/core/analytics/signal_evaluator.py
backend/core/pipeline/orchestrator.py
backend/core/pipeline/orchestrator_phases_v1.py
backend/core/pipeline/context_factory.py
backend/core/pipeline/questionnaire_mapper.py
backend/app/routes/analysis.py
```

---

## Architectural context

The pre-sprint architecture audit found:

```text
- orchestrator segmentation has only been partially completed
- backend/core/pipeline/orchestrator.py remains the main execution thread
- backend/core/pipeline/orchestrator_phases_v1.py contains evaluate_signal_evaluation_phase()
- signal evaluation occurs at Step 1.6
- create_analysis_context() runs later at Step 2
- therefore runtime context threading must use raw questionnaire_data, not mapped lifestyle_factors or medical_history
- build_runtime_context_snapshot() already accepts raw questionnaire_responses
- no new context builder module is required for this sprint
```

The intended threading path is:

```text
raw questionnaire_data
→ build_runtime_context_snapshot(questionnaire_responses=questionnaire_data)
→ evaluate_signal_evaluation_phase(..., runtime_context=runtime_ctx)
→ SignalEvaluator.evaluate_all(..., runtime_context=runtime_ctx)
→ package-declared runtime_context_requirements enforced fail-closed
```

---

## Governance classification

This sprint is HIGH risk because it touches runtime pipeline files:

```text
backend/core/pipeline/orchestrator.py
backend/core/pipeline/orchestrator_phases_v1.py
```

Required route:

```text
Cursor implementation
Claude audit
GPT architectural review
Merge only after explicit approval
```

---

## Start conditions

Start from clean `main`.

Before creating the branch, run and report:

```powershell
git branch --show-current
git status --short
git rev-parse HEAD
git rev-parse origin/main
git log --oneline -n 8
```

Do not proceed unless:

```text
- current branch is main
- local main equals origin/main
- working tree is clean
- CONTEXT-RUNTIME-1 is already merged
- build_runtime_context_snapshot() exists
- SignalEvaluator.evaluate_all() already accepts runtime_context
```

Then create/switch to:

```text
work/CONTEXT-THREADING-1-runtime-context-orchestrator-threading
```

---

## Phase 1 — Read-only verification

Before making code changes, verify and report:

```text
1. Exact variable name and scope of raw questionnaire data inside AnalysisOrchestrator.run()
2. Exact call site of evaluate_signal_evaluation_phase()
3. Exact signature of evaluate_signal_evaluation_phase()
4. Exact signature of SignalEvaluator.evaluate_all()
5. Confirm build_runtime_context_snapshot() can be imported safely
6. Confirm create_analysis_context() runs after signal evaluation
7. Confirm raw questionnaire_data is available before signal evaluation
8. Confirm only the 9 inactive Batch 2 context-dependent packages currently declare runtime_context_requirements:
   - FT3 low
   - androgen ×8
9. Confirm no currently active package declares runtime_context_requirements
10. Confirm no package activation is required for this sprint
11. Confirm this sprint is only an interim bridge and not final orchestrator restructuring
```

STOP and report if:

```text
- raw questionnaire_data is not available before signal evaluation
- build_runtime_context_snapshot() cannot consume raw questionnaire_data
- any currently active package declares runtime_context_requirements
- implementation would require broad orchestrator refactor
- implementation would require modifying clinical wording, thresholds, reference ranges, scoring, frontend, SSOT, report compiler, package activation keys, or signal IDs
```

---

## Phase 2 — Minimal implementation

Allowed files:

```text
backend/core/pipeline/orchestrator.py
backend/core/pipeline/orchestrator_phases_v1.py
backend/tests/regression/test_context_threading.py
docs/audit-papers/CONTEXT-THREADING-1_runtime_context_orchestrator_threading.md
docs/sprints/launch_core_carry_forward_register.md
```

If a different test file is used, report the reason.

Do not modify:

```text
backend/core/analytics/signal_evaluator.py
backend/core/analytics/runtime_context_evaluator.py
backend/core/pipeline/questionnaire_mapper.py
backend/core/pipeline/context_factory.py
any package signal_library.yaml
any package package_manifest.yaml
knowledge_bus/governance/*.yaml
frontend
SSOT
scoring
report compiler
clinical wording
thresholds
reference ranges
signal IDs
activation keys
```

Exception:

```text
Only modify another file if a validator proves it is required. If so, STOP and report before continuing.
```

---

## Required implementation detail

In:

```text
backend/core/pipeline/orchestrator.py
```

Import:

```python
build_runtime_context_snapshot
```

from the existing runtime context evaluator module.

Immediately before the existing `evaluate_signal_evaluation_phase()` call, build:

```python
runtime_ctx = build_runtime_context_snapshot(
    questionnaire_responses=questionnaire_data,
)
```

Pass it into the phase call:

```python
runtime_context=runtime_ctx
```

Do not use mapped `lifestyle_factors` or `medical_history` in this sprint because they are created after signal evaluation.

In:

```text
backend/core/pipeline/orchestrator_phases_v1.py
```

Update `evaluate_signal_evaluation_phase()` to accept:

```python
runtime_context: Optional[Dict[str, Any]] = None
```

Then forward it into:

```python
signal_evaluator.evaluate_all(
    ...
    runtime_context=runtime_context,
)
```

Do not change the order of existing signal evaluation steps.

Do not alter:

```text
- threshold evaluation
- lab-range logic
- mandatory pre-emission gates
- confidence calculation
- authority collision resolution
- package registry behaviour
- signal activation state
```

---

## Required tests

Add regression coverage proving:

```text
1. evaluate_signal_evaluation_phase() remains backward compatible when runtime_context=None
2. runtime_context is forwarded into SignalEvaluator.evaluate_all()
3. build_runtime_context_snapshot() is called from orchestrator using raw questionnaire_data
4. active signals without runtime_context_requirements are unaffected by runtime_context
5. a signal with runtime_context_requirements suppresses when required context is missing
6. a signal with runtime_context_requirements can pass when required context is present
7. no currently active package is suppressed by the threading change
8. no package activation occurs
```

The critical integration test is:

```text
A representative active panel with questionnaire_data must produce the same active signal set as the same panel without questionnaire_data, because currently active packages must not depend on runtime_context_requirements.
```

---

## Required validations

Run and paste actual output:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
python -m pytest backend/tests/regression/test_runtime_context_evaluation.py -q
python -m pytest backend/tests/regression/test_context_threading.py -q
```

If the context threading tests are placed elsewhere, run the actual file and report the path.

Also run any existing signal evaluator regression tests if they exist.

---

## Required audit report

Create:

```text
docs/audit-papers/CONTEXT-THREADING-1_runtime_context_orchestrator_threading.md
```

The report must include:

```text
- executive verdict
- files inspected
- files changed
- confirmation of raw questionnaire_data source
- confirmation of signal evaluation call path
- confirmation create_analysis_context() still runs later and is not used for this sprint
- confirmation this is an interim bridge, not final orchestrator architecture
- implementation summary
- test evidence
- validation output pasted in full
- confirmation no package activation occurred
- confirmation FT3 low remains inactive
- confirmation androgen packages remain inactive
- confirmation no clinical wording / thresholds / reference ranges changed
- confirmation no frontend / SSOT / scoring / report compiler changed
- confirmation no package signal_library.yaml changed
- rollback path
- residual architectural observations
```

---

## Carry-forward handling

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Required logic:

```text
CF-CONTEXT-MOD-3:
- may be marked resolved only if reusable context capability is now live in the pipeline and tested
- note that package activation remains blocked separately

CF-BATCH2-010:
- must remain open
- androgen activation remains blocked pending androgen clinical sign-off and context semantics correction

ARCH-ORCH-RESTRUCTURE-1:
- must be added or updated
- record that CONTEXT-THREADING-1 uses raw questionnaire_data as an interim bridge only
- record that final day-one architecture still requires review/restructure of orchestrator phase ordering and context assembly
- record that final runtime loaders should receive already-assembled governed inputs rather than reaching backwards into raw questionnaire payloads

CF-CONTEXT-SEMANTICS-1:
- create if not already present
- resolve androgen gate semantics before activation
- distinguish hard gates from disclosed context and interpretation modifiers
```

Do not create one carry-forward per androgen marker.

---

## Explicit non-goals

This sprint must not:

```text
- activate FT3 low
- activate androgen packages
- change androgen runtime_context_requirements semantics
- change hormone_therapy or aas_exposure handling
- add new clinical logic
- add hardcoded clinical thresholds
- change clinical wording
- change signal thresholds
- change reference ranges
- change scoring
- change frontend
- change report compiler
- refactor the orchestrator beyond the minimum threading change
- redesign questionnaire mapping
- claim final day-one orchestrator architecture is complete
```

---

## STOP conditions

STOP and report if:

```text
1. any currently active package declares runtime_context_requirements
2. raw questionnaire_data is not available before signal evaluation
3. build_runtime_context_snapshot() cannot safely consume the raw questionnaire_data
4. threading requires modifying signal_evaluator.py or runtime_context_evaluator.py
5. threading requires changing package metadata
6. validators fail
7. architecture gate fails
8. tests show existing active signals are suppressed or changed
9. implementation requires broad orchestrator refactor
10. rollback path cannot be defined
11. the sprint cannot record ARCH-ORCH-RESTRUCTURE-1 as an explicit carry-forward
```

---

## Expected changed files

Expected changed files should be limited to:

```text
backend/core/pipeline/orchestrator.py
backend/core/pipeline/orchestrator_phases_v1.py
backend/tests/regression/test_context_threading.py
docs/audit-papers/CONTEXT-THREADING-1_runtime_context_orchestrator_threading.md
docs/sprints/launch_core_carry_forward_register.md
```

If any other file changes, explain why before commit.

---

## Commit requirements

Before commit, report:

```powershell
git diff --name-only
git status --short
```

Commit message:

```text
fix(pipeline): thread runtime context into signal evaluation
```

After commit, report:

```powershell
git status --short
git log --oneline -n 5
git diff --name-only main...HEAD
```

Do not merge.

Return evidence for Claude audit and GPT architectural review.

The strategic correction is now built into the sprint: this is a safe bridge, not a claim that the final orchestrator architecture is complete.
