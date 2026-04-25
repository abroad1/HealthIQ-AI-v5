---
work_id: R-2A
branch: fix/integration-stability-backend
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# R-2A — Integration Layer Stabilisation (backend path)

## Objective

Stabilise the backend side of the integration layer by removing the fake SSE progress model and replacing it with an honest polling-compatible flow.

This sprint is limited to the backend/API path for Sprint 2.
It does not include the frontend type-generation work.
It does not include the `reports.ts` frontend cleanup.
Those will be handled separately under the light model.

This is a bounded backend integration sprint.
Do not widen into new analytical depth.
Do not introduce real live phase-streaming in this sprint.
Do not reopen the orchestrator architecture.

## Expected Cursor role

Operate as `healthiq-core-engine` for this work package.

If the required implementation extends beyond that role’s allowed scope, stop and escalate rather than widening the sprint.

---

## Strategic context

This sprint follows R-1 in the reset plan.

The decision is now made:

### Locked decision for Sprint 2B
Use **Option A**:
- remove fake SSE
- use an honest polling-compatible model
- do not build real phase-by-phase streaming in this sprint

Business rationale:
a truthful simple waiting experience is sufficient now, and engineering time should be preserved for higher-value product shell work.

---

## Required inputs

Treat the following as required inputs:

1. Reset plan
- `docs/RESET_SPRINT_PLAN_2026-04.md`

2. Relevant backend files at minimum:
- `backend/app/routes/analysis.py`
- any current analysis start/result/status endpoints
- any frontend-facing status contract path touched by backend response shape
- any tests directly covering `/api/analysis/start`, `/api/analysis/events`, or result polling paths

3. Standing operating docs:
- `AGENTS.md`
- `.cursor/rules/healthiq-core-engine.mdc`

---

## Core problem

The current SSE endpoint is fake:
- it sleeps
- emits a fabricated “completed” event
- closes

Meanwhile the real pipeline runs synchronously elsewhere.

This produces a misleading user experience and a brittle integration model.

This sprint must remove that fake mechanism and leave the backend in an honest, polling-compatible state.

---

## Scope

This sprint is limited to the backend half of Sprint 2B.

### In scope

1. Identify the current fake SSE path and remove or disable it safely.
2. Ensure the backend start/result flow supports a polling-compatible model.
3. If a lightweight status/read endpoint adjustment is needed for polling compatibility, make the smallest safe change.
4. Preserve current analytical behaviour.
5. Add/update bounded tests for the backend flow change.
6. Leave clear notes for the frontend light-model sprint that will consume this path.

### Out of scope

- frontend polling implementation
- frontend type generation
- removal of `reports.ts`
- real phase-by-phase streaming
- orchestrator redesign
- progress callback infrastructure
- new narrative or intelligence features
- unrelated API cleanup

---

## Required outcome

Deliver a bounded backend integration change that:

1. removes the fake SSE behaviour
2. leaves the backend with an honest result/status retrieval path suitable for polling
3. does not alter Intelligence Core analytical output
4. provides a stable backend contract for the frontend Sprint 2 follow-on

---

## Required implementation behaviour

### 1. Fake SSE removal
The fake `/events` behaviour must no longer present fabricated progress/completion.

Acceptable outcomes include:
- removing the endpoint entirely if it is unused after the new flow
- returning an explicit unsupported/not-used response if appropriate
- otherwise making it inert in a clearly non-misleading way

Do **not** leave a fake “completed” path in place.

### 2. Polling-compatible backend flow
The backend must support a truthful client flow of:

- start analysis
- wait for completion / retrieve result via polling-compatible endpoint(s)

Because the current pipeline runs synchronously, the simplest correct backend behaviour may be:
- start endpoint returns the created/completed analysis identifier and/or completion state
- result endpoint remains the truth source

Choose the smallest safe backend shape consistent with honesty.

### 3. No fake progress states
Do not fabricate intermediate phases or completion messages not backed by real runtime events.

---

## Design rules

### Rule 1 — honesty over sophistication
A simpler truthful backend flow is better than a more sophisticated fake one.

### Rule 2 — smallest safe backend change
Do not turn this into a broader async job-system sprint.

### Rule 3 — preserve analytical runtime
Do not modify analysis logic, pipeline ordering, or narrative generation.

### Rule 4 — no frontend invention
This sprint prepares the backend for polling.
It does not implement the frontend experience.

### Rule 5 — no adjacent improvements
If you identify a better long-term async architecture, report it separately.
Do not implement it in this sprint.

---

## Test execution scope

Run tests in this order only:

1. new or updated tests for this sprint
2. directly related existing unit/integration tests for touched backend/API paths
3. explicitly required regression/golden tests relevant to this sprint

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

1. inspect current `/events` and analysis start/result backend flow
2. identify the minimum backend changes needed for Option A
3. remove or neutralise fake SSE safely
4. ensure truthful polling-compatible backend behaviour
5. add/update bounded tests
6. report exact backend contract implications for the frontend follow-on sprint

---

## STOP conditions

STOP immediately and report if any of the following are true:

1. removing fake SSE safely would require a broader async job-system redesign
2. the backend does not currently expose a sufficient truthful retrieval path for polling and would require a larger contract redesign
3. touched-file scope expands materially beyond the expected route/backend integration layer
4. the proposed change would modify analytical runtime behaviour rather than integration behaviour
5. the frontend follow-on would require undocumented backend assumptions not safely addressed here

If blocked, report:
- exact blocker
- affected files
- smallest safe remediation path

---

## Success criteria

This sprint is successful only if:

1. fake SSE behaviour is gone
2. the backend exposes an honest polling-compatible analysis retrieval path
3. no analytical behaviour changes
4. relevant backend/API tests pass
5. the frontend follow-on can proceed on a stable backend basis

---

## Deliverables

At finish, the sprint should leave behind:

- bounded backend integration changes
- bounded backend/API tests
- a short implementation note stating:
  - what fake SSE behaviour was removed
  - what backend path frontend should now use
  - any follow-on frontend assumptions

Report back with:
- requested changes made
- incidental changes made
- optional extra changes not implemented

---

## Evidence requirements

You must show, with exact file paths and grounded evidence:

- where fake SSE existed
- how it was removed or neutralised
- what backend path now supports polling
- what tests prove the new backend behaviour
- what the frontend follow-on should consume

Do not claim completion merely because an endpoint changed.
Show that the misleading progress model is actually gone.