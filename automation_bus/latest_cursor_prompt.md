---
work_id: D-3
branch: feature/wave1-domain-cards
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# D-3 — Wave 1 domain-specific next-step routing + frontend domain cards

## Cursor agent

Use `healthiq-core-engine`.

This is mandatory.

---

## Objective

Complete the Wave 1 customer-domain card path for:

1. Cardiovascular health
2. Blood sugar control
3. Liver health

This sprint has two tightly linked parts:

### Part A — backend cleanup
Fix the known D-2 limitation so each Wave 1 domain has its own deterministic `next_step_sentence`.

### Part B — frontend implementation
Implement the Wave 1 frontend domain cards using the completed backend contract.

The backend fix must happen first inside this sprint.

---

## Branch requirement

Before doing anything else:

1. create and switch to this branch:
   `feature/wave1-domain-cards`
2. confirm the branch name before implementation begins

If the branch already exists locally, check it out and confirm.

---

## Precondition

D-1 and D-2 must already exist on the current branch history or be cleanly available for this branch to build on.

Before implementation, restate:

- where D-1 output is being read from
- where D-2 output is being read from
- what exact D-2 limitation is being corrected in Part A
- which frontend surfaces will consume the completed contract in Part B

If D-1 or D-2 output is missing or inconsistent, STOP and report.

---

## In scope

### Wave 1 only
- Cardiovascular health
- Blood sugar control
- Liver health

### Part A — backend
1. Replace the current shared `next_step_sentence` behaviour with domain-specific deterministic routing.
2. Keep all next-step routing grounded in approved existing deterministic sources.
3. Do not invent new prose unless explicitly required by a minimal governed content fix and clearly reported.

### Part B — frontend
1. Build the Wave 1 domain card UI.
2. Consume the completed backend contract.
3. Show:
   - consumer label
   - short explainer
   - score
   - band label
   - confidence
   - one-line summary
4. Expanded state should show:
   - why this score
   - confidence explanation
   - what this may mean over time
   - what to do next
   - what would improve confidence

---

## Out of scope

- clinician PDF changes
- 6-domain expansion
- thyroid scoring
- kidney implementation
- blood/iron/oxygen implementation
- second-wave domains
- broad redesign of the whole results page
- replacing existing clinician or narrative surfaces wholesale

Do not widen scope.

---

## Architectural constraints

### 1. Backend first inside this sprint
Do not begin frontend wiring until domain-specific `next_step_sentence` is fixed and verified.

### 2. Deterministic sources only
Domain-specific next steps must come from approved deterministic sources only.

### 3. No clinician/consumer leakage
Consumer card labels and copy must remain consumer-layer only.
Do not alter clinician-facing labels or clinician report surfaces.

### 4. Additive implementation only
The Wave 1 cards are an additive product layer.
Do not break or replace existing results structures beyond what is necessary to insert the new domain cards cleanly.

### 5. No fake next-step specificity
Do not make domain-specific next steps by slicing generic prose heuristically if repo-grounded evidence does not support it.
If a true domain-specific source is unavailable for one domain, STOP and report rather than inventing.

---

## Part A — required backend fix

### Current limitation from D-2
`next_step_sentence` is currently shared across all three domains rather than truly domain-specific.

### Required outcome
Each of the three domains must emit its own deterministic `next_step_sentence`.

### Approved source types
Use only repo-grounded deterministic sources such as:
- per-domain insight outputs, if available and appropriate
- domain-mapped governed content
- domain-scoped existing backend structures already identified in the narrative-contract research

### Not allowed
- generic shared fallback copied into all domains unless explicitly documented as last-resort behaviour and approved in the report
- LLM-generated wording
- hidden heuristics that are not traceable to existing domain evidence

### Acceptance for Part A
For each Wave 1 domain:
- `next_step_sentence` must be populated
- it must be domain-specific
- it must be deterministic
- the report must state the exact source path used

---

## Part B — required frontend implementation

### Wave 1 card UX
Implement frontend cards for the three Wave 1 domains.

Each collapsed card must show:
- consumer label
- short explainer
- numeric score
- band label
- confidence tier
- a concise summary line

Expanded content must show:
- contributor / why-this-score content
- confidence sentence
- consequence sentence
- next-step sentence
- missing markers / what would improve confidence

### Frontend behaviour requirements
- do not expose domains beyond the Wave 1 three
- gracefully handle absence/null if contract is not present
- do not duplicate clinician-report copy blocks unnecessarily
- keep presentation calm, readable, and consistent with the intended domain-score layer

---

## Files likely in scope

These are likely, not mandatory:

### Backend
- `backend/core/analytics/domain_narrative_wave1.py`
- `backend/core/analytics/domain_score_assembler.py`
- `backend/core/models/results.py`
- `backend/core/pipeline/orchestrator.py`
- any directly relevant domain narrative / insight wiring path needed for domain-specific next-step sourcing

### Frontend
- `frontend/app/(app)/results/page.tsx`
- new or existing Wave 1 domain card component(s)
- `frontend/app/types/analysis.ts`
- any directly relevant results component files
- targeted frontend tests

---

## Files likely out of scope

Do not touch unless absolutely required and justified:

- clinician PDF/export paths
- broad scoring policy files
- thyroid/kidney/blood-iron domain logic
- second-wave domain assets
- unrelated frontend layout systems
- pricing, trends, actions, upload flows

---

## Testing discipline

Do not run the full repository test suite.

Run only:

### Backend
1. targeted tests for domain-specific next-step routing
2. directly relevant existing D-1 / D-2 backend tests for the Wave 1 domain contract

### Frontend
3. targeted tests for the new Wave 1 card components / results integration
4. type-check for touched frontend/backend contract surfaces
5. bounded browser/UAT check for the three Wave 1 domains on a completed analysis

Before running tests, state:
- what you will run
- why it is relevant
- what broader suites you are deliberately excluding

---

## Acceptance criteria

This sprint is successful only if:

1. Wave 1 backend contract now emits domain-specific `next_step_sentence` values for:
   - cardiovascular health
   - blood sugar control
   - liver health

2. The exact deterministic source for each domain-specific next step is identified and reported.

3. Wave 1 frontend cards are implemented and consume the backend contract correctly.

4. The frontend shows the three domains only.

5. No clinician-facing surfaces are altered.

6. No fake or non-deterministic prose is introduced.

7. Targeted backend and frontend tests pass.

8. Browser/UAT confirms the cards render coherently on a real completed analysis.

---

## Reporting requirements

When finished, report back in these sections:

### 1. Branch
- confirm branch name

### 2. Preflight restatement
- objective
- files touched
- files not touched
- D-1/D-2 dependency check
- exact D-2 limitation being fixed first

### 3. Part A — backend next-step routing fix
- exact files changed
- exact source used for each domain’s next-step sentence
- how determinism was preserved
- any fallback behaviour

### 4. Part B — frontend Wave 1 cards
- exact files changed
- where cards were inserted
- what each card shows collapsed and expanded
- how missing/null contract states are handled

### 5. Tests run
- exact tests
- results

### 6. Browser/UAT
- what was checked
- result

### 7. Known limits intentionally deferred
- anything left for later phases
- any remaining contract or UX caveats

### 8. Uncommitted / not merged
- confirm work is not merged to `main`

---

## STOP conditions

STOP and report instead of widening scope if any of the following occurs:

1. Domain-specific next-step routing cannot be implemented from approved deterministic sources.
2. Frontend implementation depends on additional backend contract redesign beyond Wave 1 scope.
3. A fourth domain starts to creep into scope.
4. Clinician-facing outputs would need to change to complete the sprint.
5. The results page would need a broader redesign beyond inserting the Wave 1 cards.
6. Browser/UAT reveals a major contract mismatch that cannot be fixed safely inside this sprint.

If blocked, report:
- exact blocker
- affected files
- smallest safe remediation path