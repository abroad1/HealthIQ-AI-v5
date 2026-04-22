---
work_id: N-9
branch: feature/n-9-ab-benchmark-runtime-validation
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# N-9 — AB benchmark runtime validation

## Objective

Validate the real deterministic runtime output for the AB benchmark case against the locked benchmark narrative and determine, with repo-grounded evidence, what is now strong enough, what is still materially weaker, and what remains missing before frontend re-entry.

This is a validation sprint.
It is not a frontend redesign sprint.
It is not a new compiler-build sprint.
Do not widen into general product strategy.
Do not introduce Gemini or any other LLM dependency.

The purpose of N-9 is to pressure-test the newly built deterministic narrative stack end to end and produce a clear verdict on whether the current runtime output is good enough for controlled surfacing, or whether a bounded refinement sprint is still required first.

---

## Strategic context already settled

The following are already decided and are not open for reinterpretation in this sprint:

- The benchmark narrative is locked.
- The merged reverse-engineering matrix is locked.
- The narrative compiler architecture is locked.
- N-3 through N-8 have now built:
  - longitudinal numeric support
  - lifestyle interpretation bridges
  - pathway explainer assets
  - functional interpretation / confidence assets
  - governed benchmark interpretation entities
  - deterministic narrative compiler v1
- N-9 exists to test the real runtime output against the benchmark standard before major frontend re-entry.

Your job is to validate the actual generated output, not to speculate about what the system might produce.

---

## Required inputs

Treat the following as required inputs:

1. Benchmark target lock  
`docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_TARGET_LOCK.md`

2. Locked benchmark narrative  
`docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REPORT_CHAT_2_FINAL.md`

3. Merged reverse-engineering matrix  
`docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REVERSE_ENGINEERING_MERGED.md`

4. Final sprint strategy  
`docs/golden-narrative/HealthIQ_Deterministic_Narrative_Sprint_Strategy_FINAL.md`

5. Narrative compiler architecture  
`docs/golden-narrative/HealthIQ_Deterministic_Narrative_Compiler_Architecture_v1.md`

6. The real AB input fixture and any required paired context
At minimum:
- the authoritative AB panel fixture with ranges
- the questionnaire/lifestyle context actually used for this benchmark run
- any prior snapshot/panel 0 support used in runtime comparison

7. Current runtime/compiler paths relevant to N-8 output
At minimum:
- `backend/core/analytics/narrative_report_compiler_v1.py`
- `backend/core/contracts/narrative_report_v1.py`
- `backend/core/pipeline/orchestrator.py`
- `backend/core/models/results.py`
- any runtime output artifact or API result path used to inspect the generated narrative

---

## Core problem this sprint must solve

HealthIQ now has a deterministic narrative compiler, but it is not yet known whether the actual runtime output is:

- close enough to the benchmark to justify frontend re-entry
- still materially weaker due to compiler assembly limits
- still materially weaker due to governed asset quality
- or still blocked by some missing runtime support

This sprint must answer that precisely using the real output, not aspiration.

---

## Required outcome

Deliver a validation package that:

1. runs or inspects the real AB runtime narrative output produced by N-8
2. compares that output against the locked benchmark narrative
3. evaluates each major benchmark narrative move
4. classifies the remaining gap for each weak area
5. states clearly whether a bounded refinement sprint is required before frontend re-entry
6. leaves behind a planning-ready recommendation for what comes after N-9

---

## In scope

### 1. Runtime output acquisition
Obtain the actual deterministic runtime output for the AB benchmark case.

This may be via:
- a generated backend artifact
- a JSON/API result
- a golden-run artifact
- another grounded runtime output path

Do not evaluate a hypothetical or hand-assembled output.
Use the real runtime output from the current stack.

### 2. Benchmark comparison
Compare the generated runtime output against the locked benchmark narrative at the level of narrative moves, not just section titles.

At minimum assess:
- patient-summary quality
- body overview quality
- lead domain narrative quality
- secondary domain narrative quality
- longitudinal section quality
- next-steps quality
- clinician synthesis quality

### 3. Strength / weakness classification
For each major narrative area, classify it as:
- strong enough
- partially there
- materially weaker than benchmark
- absent / still unsupported

### 4. Gap-type classification
For each materially weak area, classify the remaining cause as one or more of:
- governed asset quality gap
- compiler assembly gap
- missing deterministic support
- runtime integration/surfacing gap
- wording polish only

Do not collapse all remaining issues into “needs polish.”

### 5. Frontend-readiness judgement
Make a direct recommendation on one of the following:

1. deterministic runtime is now strong enough for frontend re-entry
2. deterministic runtime is materially improved but still needs one bounded refinement sprint first
3. deterministic runtime is still too weak and needs more than one additional backend/content sprint before frontend re-entry

### 6. Recommended next move
If refinement is needed, state the smallest bounded next sprint that should happen.
If refinement is not needed, state that frontend re-entry may begin.

### 7. Concise validation note
Leave behind a concise validation note or report documenting:
- what runtime output was inspected
- what the outcome was
- what the next step should be

---

## Out of scope

The following are explicitly out of scope:

- implementing fixes during this sprint
- frontend redesign
- writing new narrative assets
- modifying compiler logic
- Gemini / LLM work
- broad strategy debate already settled

---

## Design rules

### Rule 1 — validate reality, not intention
Judge the actual runtime output only.

### Rule 2 — benchmark is the standard
Do not quietly lower the benchmark because the runtime is weaker.

### Rule 3 — distinguish true weakness from missing surfacing
If the output exists but is merely not surfaced well, say so clearly.

### Rule 4 — no vague “needs work”
Weaknesses must be classified precisely.

### Rule 5 — bounded recommendation
If another sprint is needed, recommend the smallest one that would materially improve the runtime.

---

## Expected implementation shape

The expected shape is:

1. identify the real AB runtime output artifact/path
2. inspect the generated deterministic narrative output
3. compare it against the benchmark
4. score/classify strengths and weaknesses
5. identify the true remaining gap types
6. produce a recommendation for what comes next

This must remain a validation sprint, not a fixing sprint.

---

## Required output files

Create the following file in:
`docs/golden-narrative/`

Suggested filename:
`AB_BENCHMARK_RUNTIME_VALIDATION_N9.md`

If repo reality strongly suggests a better naming pattern, justify it.

---

## Output structure requirements

The output file must include, at minimum:

### 1. Purpose
What was validated and why.

### 2. Source authorities used
List:
- benchmark narrative
- target lock
- merged matrix
- runtime artifact/output inspected
- relevant runtime files inspected

### 3. Runtime output inspected
State exactly what output was evaluated and how it was obtained.

### 4. Benchmark comparison table
Use a structured table with columns such as:
- benchmark narrative area
- runtime output status
- quality judgement
- remaining gap type
- notes

### 5. Strongest wins
State what parts of the deterministic runtime are now genuinely strong.

### 6. Remaining weaknesses
State what is still materially below benchmark and why.

### 7. Frontend-readiness recommendation
Choose one of the three frontend-readiness outcomes listed above.

### 8. Recommended next sprint or next phase
State the immediate next move.

---

## STOP conditions

STOP immediately and report if any of the following are true:

1. no reliable runtime output artifact can be obtained for the AB benchmark case
2. the runtime output inspected does not actually reflect the current N-8 compiler path
3. the benchmark comparison cannot be made reliably because the runtime case differs materially from the locked benchmark case
4. another upstream issue prevents fair validation

If blocked, report:
- the exact blocker
- the affected files or runtime path
- the smallest safe remediation path

---

## Success criteria

This sprint is successful only if:

1. the real deterministic AB runtime output was inspected
2. the output was compared against the benchmark in a structured way
3. remaining weaknesses were classified precisely
4. a clear frontend-readiness judgement was made
5. a clear next move was recommended
6. no implementation changes were made during validation

---

## Deliverables

At finish, the sprint should leave behind:

- `docs/golden-narrative/AB_BENCHMARK_RUNTIME_VALIDATION_N9.md`

plus a short completion note stating:
- what runtime output was inspected
- the frontend-readiness judgement
- the recommended next move

---

## Evidence requirements

You must show, with exact file paths and grounded runtime evidence:

- where the runtime output came from
- that it reflects the current N-8 compiler path
- how each benchmark area compares
- what the remaining weakness types actually are
- why the recommended next step follows from the evidence

Do not produce a vague review.
Produce a validation authority artifact.