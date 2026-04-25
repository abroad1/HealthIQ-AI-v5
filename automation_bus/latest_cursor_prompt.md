---
work_id: R-8
branch: feature/why-coverage-expansion-wave-1
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# R-8 — WHY coverage expansion, Wave 1

## Objective

Expand governed WHY reasoning for the genuinely ungoverned high-value Wave 1 findings only:

1. `signal_total_cholesterol_high`
2. `signal_vitamin_d_low`

This is a HIGH-risk Intelligence Core sprint.

Do not widen scope beyond these two canonical signal IDs.

## Expected Cursor role

Operate as `healthiq-core-engine` for this work package.

If the required implementation extends beyond that role’s allowed scope, stop and escalate rather than widening the sprint.

---

## Stage 0 prerequisite

Before doing anything else, create and switch to this branch:

`feature/why-coverage-expansion-wave-1`

Confirm branch creation before implementation begins.

---

## Strategic context

This sprint comes after the reset plan’s product-shell sequence.

Important scope correction:
The following are already governed and are **not** new work in this sprint:
- `signal_ldl_cholesterol_high`
- `signal_hdl_cholesterol_low`
- `signal_triglycerides_high`

Wave 1 new work is restricted to:
- `signal_total_cholesterol_high`
- `signal_vitamin_d_low`

---

## Required inputs

Treat the following as required inputs:

1. Reset plan
- `docs/RESET_SPRINT_PLAN_2026-04.md`

2. Relevant current runtime and governed files at minimum:
- `backend/core/analytics/root_cause_compiler_v1.py`
- `knowledge_bus/root_cause/hypotheses/`
- `knowledge_bus/registries/confirmatory_tests_v1.yaml`
- current governed WHY hypothesis files for existing supported domains
- relevant fixtures and tests for root-cause output

3. Standing operating docs:
- `AGENTS.md`
- `.cursor/rules/healthiq-core-engine.mdc`

---

## Locked Wave 1 scope

### Group A — Total cholesterol WHY
Required:
- `signal_total_cholesterol_high`

### Group B — Vitamin D WHY
Required:
- `signal_vitamin_d_low`

No other lipid, thyroid, inflammatory, renal, or iron WHY work is in scope.

---

## Core problem

Fallback WHY prevents silence, but these two high-value/common findings still lack governed WHY output.

This sprint must move them from fallback WHY to governed WHY.

---

## Required outcome

Deliver a bounded governed WHY expansion that:

1. adds governed root-cause hypotheses for:
   - `signal_total_cholesterol_high`
   - `signal_vitamin_d_low`
2. wires those hypotheses into `root_cause_compiler_v1.py`
3. ensures panels dominated by those findings produce governed WHY rather than fallback
4. preserves all existing WHY behaviour
5. preserves fallback for still-uncovered signals

---

## Scope

### In scope

1. Governed hypothesis authoring for:
- `signal_total_cholesterol_high`
- `signal_vitamin_d_low`

2. Root-cause compiler wiring:
- update `root_cause_compiler_v1.py` so these signal IDs map to governed WHY output

3. Confirmatory test registry support:
- because the loader validates confirmatory test IDs at load time, this sprint may add the **minimal** new entries needed to:
  - `knowledge_bus/registries/confirmatory_tests_v1.yaml`
- if no specific confirmatory tests are ready, you may use `confirmatory_tests: []` only if that is the smallest safe governed choice and you explain why

4. Tests / fixtures / regression:
- add or update the minimum fixtures/tests needed to prove governed WHY now appears for these two signals
- preserve regression coverage for existing WHY-covered domains
- preserve fallback behaviour for signals still outside governed WHY

5. Minimal implementation note:
- what signal IDs were added
- what files were touched
- what remains for Wave 2

---

## Out of scope

- `signal_ldl_cholesterol_high`
- `signal_hdl_cholesterol_low`
- `signal_triglycerides_high`
- iron WHY
- broader inflammatory WHY
- renal WHY
- expanded thyroid WHY
- frontend presentation
- broad root-cause architecture redesign

---

## Design rules

### Rule 1 — canonical IDs only
Use the canonical runtime signal IDs exactly as named above.

### Rule 2 — Wave 1 only
Do not silently expand scope beyond these two signals.

### Rule 3 — governed WHY, not ad hoc prose
Use the current governed hypothesis pattern.

### Rule 4 — preserve current architecture
Extend the current governed root-cause system.
Do not redesign it.

### Rule 5 — fallback must remain correct
Signals still outside governed WHY must continue to use fallback.

### Rule 6 — confirmatory registry must load cleanly
Do not introduce hypothesis YAML that fails loader validation because of missing confirmatory test IDs.

---

## Test execution scope

Run tests in this order only:

1. new or updated regression tests for this sprint
2. directly related existing unit/integration tests for touched root-cause/compiler paths
3. explicitly required golden/regression tests relevant to WHY output

Do not run the full repository test suite unless:
- this prompt explicitly requires it, or
- a targeted failure gives concrete evidence of wider regression risk

Before running tests, state:
- which tests you will run
- why they are relevant
- which broader suites you are deliberately not running

Do not run unrelated legacy or archived tests by default.

---

## Expected implementation shape

1. inspect existing governed WHY pattern and loader rules
2. author the minimum correct hypothesis files for:
   - `signal_total_cholesterol_high`
   - `signal_vitamin_d_low`
3. add minimal confirmatory-test registry support if needed
4. wire the signal IDs into `root_cause_compiler_v1.py`
5. add/update bounded tests and fixtures
6. verify governed WHY replaces fallback for these two signals
7. verify fallback still works elsewhere
8. report exact files touched and any Wave 2 recommendations not implemented

---

## STOP conditions

STOP immediately and report if any of the following are true:

1. these two signals cannot be completed without broader root-cause architecture redesign
2. adding the hypotheses would force broader governed asset redesign beyond this sprint
3. touched-file scope expands materially beyond root-cause hypotheses, confirmatory registry support, compiler wiring, and bounded tests
4. any additional signal group is tempting but not explicitly approved

If blocked, report:
- exact blocker
- affected files
- smallest safe remediation path

---

## Success criteria

This sprint is successful only if:

1. `signal_total_cholesterol_high` now produces governed WHY rather than fallback
2. `signal_vitamin_d_low` now produces governed WHY rather than fallback
3. existing WHY-covered domains continue to work
4. fallback still works for uncovered domains
5. relevant regression tests pass
6. no scope widening beyond the two locked Wave 1 signals occurred

---

## Deliverables

At finish, the sprint should leave behind:

- governed hypothesis YAML(s) for:
  - `signal_total_cholesterol_high`
  - `signal_vitamin_d_low`
- minimal confirmatory registry additions if required
- bounded `root_cause_compiler_v1.py` updates
- regression tests / fixture updates
- a short implementation note stating:
  - what was added
  - what remains for later Wave 2
  - any optional follow-up not implemented

Report back with:
- requested changes made
- incidental changes made
- optional extra changes not implemented

---

## Evidence requirements

You must show, with exact file paths and grounded evidence:

- where the new governed hypotheses now live
- where the compiler wiring was added
- what test/fixture proves total cholesterol WHY now exists
- what test/fixture proves vitamin D WHY now exists
- that fallback still applies correctly outside the governed set

Do not claim completion merely because new YAML files were added.
Show that Wave 1 WHY coverage is actually active in runtime behaviour.