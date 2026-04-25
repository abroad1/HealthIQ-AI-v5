---
work_id: R-1
branch: fix/engine-trust-bugs
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# R-1 — Engine trust bugs

## Objective

Fix the three engine correctness failures that directly undermine HealthIQ’s deterministic trust claim:

1. contradictory signal activation
2. one-sided lab range scoring failure
3. missing WHY fallback for non-covered lead signals

This is a HIGH-risk Intelligence Core sprint.

Do not widen scope.
Do not introduce new analytical depth beyond the explicit fallback behaviour required here.
Do not perform unrelated cleanup or opportunistic refactors.

## Expected Cursor role

Operate as `healthiq-core-engine` for this work package.

If the required implementation extends beyond that role’s allowed scope, stop and escalate rather than widening the sprint.

---

## Strategic context

This sprint is Sprint 1 in the reset plan.
Order is non-negotiable:
- engine trust bugs first
- integration stability next
- product shell after that

This sprint exists because these failures directly damage user trust in the moat and must be resolved before further product-shell work proceeds.

---

## Required inputs

Treat the following as required inputs:

1. Reset plan
- `docs/RESET_SPRINT_PLAN_2026-04.md`

2. Relevant runtime files at minimum:
- `backend/core/analytics/signal_evaluator.py`
- `backend/core/pipeline/orchestrator.py`
- `backend/core/analytics/root_cause_compiler_v1.py`
- relevant contracts / DTO builders / clinician summary paths
- relevant existing tests and golden-panel tests

3. Current standing operating docs:
- `AGENTS.md`
- `.cursor/rules/healthiq-core-engine.mdc`

---

## Scope

This sprint is limited to the three trust bugs below.

### Bug 1 — Contradictory signal activation

**File:** `backend/core/analytics/signal_evaluator.py`  
**Target:** `_evaluate_lab_range_activation_state` or equivalent activation path

### Problem
`enable_upper_bound` / `enable_lower_bound` flags are not being honoured, allowing contradictory high and low activation on the same value.

### Required behaviour
- respect `enable_upper_bound`
- respect `enable_lower_bound`
- do not activate upper-bound logic when upper-bound is disabled
- do not activate lower-bound logic when lower-bound is disabled
- if a signal definition would still allow contradictory activation after this fix, treat that as a configuration warning/problem, not a runtime result

### Regression target
A mid-range cholesterol test value must not produce both `signal_total_cholesterol_high` and `signal_total_cholesterol_low` as active simultaneously.

---

### Bug 2 — One-sided lab range scoring failure

**File:** `backend/core/pipeline/orchestrator.py`  
**Target:** `_has_valid_numeric_bounds` or equivalent scoring eligibility logic

### Problem
Scoring currently requires both `min` and `max` numeric bounds, which breaks common commercial panels with one-sided ranges.

### Required behaviour
- a range is valid if either `min` or `max` is numeric
- max-only: above max = high, below max = in-range
- min-only: below min = low, above min = in-range
- do not produce “insufficient numeric bounds” for valid one-sided commercial ranges

### Regression target
A panel with LDL max-only and HDL min-only ranges must produce scored output, not the “insufficient bounds” message.

---

### Bug 3 — WHY fallback for non-covered lead signals

**Files:** 
- `backend/core/analytics/root_cause_compiler_v1.py`
- any directly related contracts / DTO / clinician summary path required to surface fallback cleanly

### Problem
WHY reasoning exists for only a narrow governed set. When the lead signal falls outside that set, the summary can silently omit WHY content.

### Required behaviour
- return a structured fallback object instead of null/empty when no governed hypothesis exists
- fallback must include:
  - signal name
  - activation state
  - lab range classification
  - a standard phrase stating that deep hypothesis analysis is not yet available for this marker
- fallback must be surfaced visibly in the results DTO / clinician path
- clinician summary must degrade gracefully and not assume `top_findings[0]` always has governed WHY content

### Regression target
A panel whose lead signal is outside the governed WHY set must still produce a visible, non-empty WHY section via fallback.

---

## In scope

- bounded fixes for the three bugs above
- regression tests proving each fix
- minimal DTO/summary/contract adaptation only if required to surface the WHY fallback cleanly
- preservation of existing output contracts wherever possible

---

## Out of scope

- expanding governed WHY coverage beyond the fallback mechanism
- new phenotype/IDL/narrative work
- frontend changes
- product-shell changes
- broad orchestrator refactoring
- repo cleanup
- documentation rationalisation beyond a short sprint note if needed

---

## Design rules

### Rule 1 — no scope drift
Implement only the three trust fixes.

### Rule 2 — smallest safe behavioural change
Fix the trust bug without broad redesign.

### Rule 3 — preserve existing contracts where possible
Fallback should fit the existing WHY surface rather than triggering an unnecessary new contract family.

### Rule 4 — no silent omissions
If WHY is unavailable, the user-visible/report-visible output must say so explicitly via fallback.

### Rule 5 — no adjacent helpful changes
If you discover a worthwhile related improvement, report it separately and do not implement it.

---

## Expected implementation shape

1. inspect current bug path for each of the three issues
2. implement the smallest safe fix for each
3. add or update regression tests
4. run relevant targeted tests and golden-panel tests
5. report back with exact files touched and how each bug is now prevented

---

## STOP conditions

STOP immediately and report if any of the following are true:

1. fixing one-sided ranges requires broader scoring-policy redesign than expected
2. WHY fallback cannot be surfaced cleanly without a broader contract change
3. contradictory activation is caused by upstream signal-definition corruption rather than runtime logic alone
4. touched-file scope expands materially beyond the three named runtime paths plus minimal necessary supporting files
5. any additional Intelligence Core path appears necessary but was not explicitly approved

If blocked, report:
- exact blocker
- affected files
- smallest safe remediation path

---

## Success criteria

This sprint is successful only if:

1. contradictory high/low activation is prevented by test
2. one-sided commercial ranges score correctly by test
3. non-covered lead signals produce visible WHY fallback by test
4. existing golden-panel tests continue to pass
5. no unnecessary contract or runtime widening occurred

---

## Deliverables

At finish, the sprint should leave behind:

- bounded code changes for the three trust bugs
- regression tests
- a short implementation note stating:
  - files touched
  - how each bug was fixed
  - any follow-up issue discovered but not implemented

Report back with:
- requested changes made
- incidental changes made
- optional extra changes not implemented

---

## Evidence requirements

You must show, with exact file paths and grounded evidence:

- where contradictory activation was prevented
- where one-sided ranges are now treated as valid
- where WHY fallback is now returned and surfaced
- what tests prove the new behaviour
- that existing golden-panel tests still pass

Do not claim completion without showing each of the three trust failures is now directly addressed.