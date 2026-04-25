---
work_id: R-1B
branch: fix/unscored-marker-trust-gaps
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# R-1B — Unscored marker trust gaps

## Objective

Fix the bounded backend trust gaps surfaced in live-panel diagnosis around unscored biomarker output.

This is a HIGH-risk Intelligence Core sprint.

This sprint exists to restore trust in the biomarker layer by ensuring:
1. the true unscored reason is preserved through the scoring → DTO path
2. markers with valid one-sided lab ranges that should score do in fact score
3. HbA1c unit mismatch is handled truthfully rather than being mislabeled as a bounds problem

Do not widen this sprint beyond those three defects.

## Expected Cursor role

Operate as `healthiq-core-engine` for this work package.

If the required implementation extends beyond that role’s allowed scope, stop and escalate rather than widening the sprint.

---

## Strategic context

This sprint is a direct follow-on trust-fix sprint after Sprint 1 and Sprint 2.

The live-panel diagnosis established three distinct backend trust issues:

1. `unscored_reason` is attached internally but dropped before DTO interpretation text is built
2. several live biomarkers with valid one-sided lab ranges still surface as unscored despite the one-sided scoring fix
3. HbA1c can reach the user as “insufficient numeric bounds” when the real problem is unit mismatch (`%` vs `mmol/mol`)

This sprint fixes those backend truthfulness/correctness issues only.

---

## Required inputs

Treat the following as required inputs:

1. Live-panel diagnosis and evidence
- the latest QA diagnosis covering live analysis `6f702428-ec3e-4e00-9416-280904e9d4b3`

2. Relevant runtime files at minimum:
- `backend/core/pipeline/orchestrator.py`
- `backend/core/scoring/rules.py`
- `backend/core/analytics/primitives.py`
- any biomarker score dataclass / score serialization path
- any DTO/result-building path directly involved in biomarker interpretation text

3. Standing operating docs:
- `AGENTS.md`
- `.cursor/rules/healthiq-core-engine.mdc`

---

## Core problem

The biomarker surface is currently mixing together:
- real unscorable markers
- markers that should score but do not
- unit mismatch cases
- generic heuristic fallback wording

This produces avoidable trust damage in the results page.

The sprint must make the backend truthful and correct for the bounded defects identified.

---

## Scope

This sprint is limited to the three defects below.

### Defect 1 — `unscored_reason` is dropped before DTO interpretation

### Problem
The scoring path attaches `unscored_reason` internally, but the orchestrator dict built for biomarker score rows drops it before the DTO/user-facing interpretation logic reads it.

As a result, live biomarker interpretation text can fall back to weaker bounds/status heuristics and fail to state the true reason.

### Required behaviour
- preserve `unscored_reason` through the scoring → orchestrator/DTO path wherever biomarker interpretation text is constructed
- do not invent a new broad contract family unless strictly required
- ensure biomarker interpretation text can distinguish the real cause rather than relying on generic heuristics when the score already knows why it is unscored

### Regression target
A marker with a known non-empty `unscored_reason` must preserve that cause into the biomarker output path used for interpretation text.

---

### Defect 2 — valid one-sided live markers still surface as unscored

### Problem
The live diagnosis indicates these markers appear unscored despite valid one-sided lab ranges and matching units:
- `hdl_cholesterol`
- `triglycerides`
- `active_b12`
- `egfr`
- `folate`

This suggests the one-sided range fix from R-1 is not being fully honored somewhere in the live scoring/DTO path.

### Required behaviour
- trace the exact live scoring path for these markers
- identify where the one-sided-range handling still fails or is discarded
- fix the smallest safe backend path so valid one-sided ranges score end-to-end
- do not widen into a broad redesign of biomarker scoring

### Regression target
A bounded regression fixture covering representative min-only and max-only live-style markers must produce scored output rather than an unscored interpretation when units and ranges are valid.

---

### Defect 3 — HbA1c unit mismatch is misclassified as bounds failure

### Problem
HbA1c can surface as:
- value in `%`
- lab range in `mmol/mol`
and currently reach the user as `Not scored - insufficient numeric bounds for scoring`

That is not truthful. The issue is unit mismatch / harmonisation, not missing numeric bounds.

### Required behaviour
- detect this case truthfully in the backend path
- either:
  - harmonise units safely before scoring if already supported by current architecture, or
  - classify it explicitly as a unit mismatch / incompatible units case rather than a bounds failure
- do not fake scoring if the units cannot be meaningfully reconciled
- do not widen this into a broad HbA1c architecture redesign

### Regression target
A fixture/path with HbA1c value/range unit mismatch must not surface as “insufficient numeric bounds.” It must either score correctly after valid conversion or report a truthful unit mismatch-style reason.

---

## In scope

- bounded fixes for the three defects above
- regression tests proving each fix
- minimal supporting runtime/serialization changes required to preserve true unscored reasons
- minimal interpretation text correction needed so the backend no longer misstates the cause

---

## Out of scope

- adding policy bounds for `remnant_cholesterol`
- changing policy for markers with no lab range such as `free_testosterone_pct`
- broad UI/wording redesign across all biomarker states
- SSOT fallback scoring for lab-sovereign markers
- new frontend work
- broad scoring-engine redesign
- broad unit-system redesign beyond what is required for truthful HbA1c handling

---

## Design rules

### Rule 1 — truthfulness first
If a marker is unscored, the backend must preserve and surface the real reason where available.

### Rule 2 — smallest safe fix
Do not redesign the whole biomarker scoring layer.

### Rule 3 — no policy creep
Do not turn this sprint into a policy decision about which derived or no-range markers should be scored.

### Rule 4 — preserve existing contracts where possible
Prefer bounded extension/preservation of existing fields over broad new structures unless strictly necessary.

### Rule 5 — no adjacent helpful changes
If additional unscored-marker improvements are discovered, report them separately and do not implement them in this sprint.

---

## Test execution scope

Run tests in this order only:

1. new or updated regression tests for this sprint
2. directly related existing unit/integration tests for touched scoring/orchestrator/DTO paths
3. explicitly required golden/regression tests relevant to this sprint

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

1. inspect the scoring → orchestrator → biomarker DTO interpretation path
2. preserve `unscored_reason` through that path
3. reproduce and fix the one-sided live-marker scoring failure
4. reproduce and fix truthful HbA1c unit-mismatch handling
5. add/update regression tests
6. report exact files touched and how each defect is now prevented

---

## STOP conditions

STOP immediately and report if any of the following are true:

1. preserving `unscored_reason` requires a broader contract redesign than expected
2. the one-sided marker failure is caused by upstream data corruption rather than scoring/runtime logic
3. truthful HbA1c handling requires a larger unit-normalisation redesign than can safely fit here
4. touched-file scope expands materially beyond the expected scoring/orchestrator/DTO path
5. any additional policy decision is required to complete the sprint safely

If blocked, report:
- exact blocker
- affected files
- smallest safe remediation path

---

## Success criteria

This sprint is successful only if:

1. `unscored_reason` is preserved into the biomarker interpretation path
2. representative live-style one-sided markers now score correctly end-to-end
3. HbA1c unit mismatch is no longer mislabeled as a bounds failure
4. relevant regression tests pass
5. no policy-widening or frontend changes were introduced

---

## Deliverables

At finish, the sprint should leave behind:

- bounded backend changes for the three defects
- regression tests
- a short implementation note stating:
  - files touched
  - how each defect was fixed
  - any follow-up issue discovered but not implemented

Report back with:
- requested changes made
- incidental changes made
- optional extra changes not implemented

---

## Evidence requirements

You must show, with exact file paths and grounded evidence:

- where `unscored_reason` was previously dropped and is now preserved
- where the one-sided-range live-marker path was failing and is now fixed
- where HbA1c mismatch is now handled truthfully
- what tests prove the corrected behaviour

Do not claim completion merely because some marker text changed.
Show that the backend scoring/truth path is now correct.