---
work_id: D-5
branch: feature/wave1-runtime-diagnosis
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# D-5 — Wave 1 runtime verification and stale-path diagnosis

## Cursor agent

Use `healthiq-core-engine`.

This is mandatory.

---

## Objective

Diagnose why the live Wave 1 UAT recheck still appears to show pre-D-4 behaviour.

This sprint is diagnosis only.

The purpose is to determine, for the specific live analysis under review, whether the mismatch is caused by:

- stale persisted analysis payload
- stale frontend build/runtime
- wrong frontend field wiring
- D-4 logic not being exercised for this analysis
- or a genuine failure in D-4 backend/frontend refinement logic

Do not implement fixes in this sprint unless a tiny, fully obvious mechanical mistake is discovered and explicitly reported first.
Primary goal is repo/runtime truth.

---

## Branch requirement

Before doing anything else:

1. create and switch to this branch:
   `feature/wave1-runtime-diagnosis`
2. confirm the branch name before investigation begins

If the branch already exists locally, check it out and confirm.

---

## Problem statement

The post–D-4 live UAT still reported:

- cardiovascular and blood sugar showing “broadly stable”
- liver still leaking internal caveat slugs
- no visible evidence-anchor improvement
- overall behaviour looking closer to pre-D-4 than post-D-4

That may mean:
1. the wrong build is running
2. the wrong analysis payload is being viewed
3. D-4 only affects newly generated results
4. the frontend is not rendering the new fields
5. the D-4 logic is present but not firing for this payload
6. or D-4 did not actually solve the runtime path

This sprint must determine which is true.

---

## Specific target to investigate

Login:
- `test-user3@example.com`
- `Subaru@555`

Analysis result:
- `http://localhost:3000/results?analysis_id=c1c061ab-4691-4a47-80b8-2938ae1460e4`

---

## In scope

### Investigation only
1. Inspect the exact stored/backend response for analysis id:
   `c1c061ab-4691-4a47-80b8-2938ae1460e4`
2. Verify whether the API response for that analysis currently contains D-4 fields/values such as:
   - refined `headline_sentence`
   - refined `confidence_sentence`
   - user-facing liver caveat strings
   - `evidence_anchor_sentence`
3. Verify whether the frontend is actually reading/rendering those fields.
4. Verify whether the running frontend and backend processes are serving the expected code.
5. Determine whether this analysis would need recomputation/regeneration to pick up D-4 changes.

---

## Out of scope

- broad product refinement
- Phase 2 work
- unrelated frontend redesign
- clinician PDF work
- new domain logic
- speculative fixes not grounded in the diagnosis

Do not widen scope.

---

## Required investigation tasks

## A. Backend truth check

For the target analysis id:

1. identify where the persisted result is stored and how it is served
2. inspect the exact backend/API payload for `consumer_domain_scores`
3. verify for each Wave 1 domain whether the returned payload currently contains:
   - `headline_sentence`
   - `confidence_sentence`
   - `caveat_flags`
   - `evidence_anchor_sentence`
4. record the actual values seen for:
   - cardiovascular
   - blood sugar
   - liver

Goal:
prove whether the backend payload is already correct, incorrect, or stale.

---

## B. Frontend rendering check

1. inspect the current `Wave1DomainCards` rendering path
2. verify exactly which fields it reads for:
   - collapsed title/summary/headline
   - confidence
   - caveat display
   - evidence anchor
3. determine whether the live UI could still show old text even if backend payload is correct
4. identify any mismatch between:
   - fields D-4 produces
   - fields the component actually renders

Goal:
prove whether the frontend wiring is correct or stale.

---

## C. Persistence / recomputation check

Determine whether `analysis_id=c1c061ab-4691-4a47-80b8-2938ae1460e4` is:
- a stored analysis result generated before D-4
- an object that would need regeneration to pick up D-4-computed strings
- or a dynamically rebuilt response that should already reflect D-4

Be explicit:
- are domain narrative fields computed live on fetch?
- or persisted at analysis-completion time?

This is critical.

---

## D. Runtime/build check

Verify:
1. whether the running frontend is using the latest built code for D-4
2. whether the running backend is using the latest D-4 logic
3. whether there is any stale dev-server/build/cache issue that could explain the mismatch

Do not guess.
Ground this in what you can actually observe.

---

## E. Live browser verification

Using the same login and analysis id:
1. log in
2. wait for the session to settle
3. open the result URL
4. inspect the visible Wave 1 cards
5. compare what is on-screen against:
   - the backend payload
   - the frontend field mapping
   - the intended D-4 logic

Goal:
state exactly where the divergence occurs.

---

## Acceptance criteria

This sprint is successful only if it answers, explicitly:

1. Is the backend payload for this analysis already showing D-4-refined fields or not?
2. If yes, is the frontend rendering the wrong fields?
3. If no, is the analysis result stale/persisted and therefore needs regeneration?
4. Is the running frontend/backend code actually on the expected D-4 implementation?
5. What is the smallest correct next step:
   - rerun analysis
   - regenerate stored result
   - fix frontend field wiring
   - fix backend runtime path
   - or do a true D-4 follow-up refinement

---

## Testing / validation discipline

Do not run the full repository test suite.

Run only what is necessary to prove runtime truth, for example:
- targeted inspection commands
- direct API retrieval for the analysis id
- minimal backend/frontend checks
- bounded browser verification

Before running anything, state:
- what you will inspect
- why it is relevant
- what broader suites you are deliberately excluding

---

## Reporting requirements

When finished, report back in these sections:

### 1. Branch
- confirm branch name

### 2. Preflight restatement
- objective
- files inspected
- whether any files were modified
- what was deliberately not changed

### 3. Backend payload truth
- exact payload status for each Wave 1 domain
- whether D-4-refined fields are present
- actual values relevant to the mismatch

### 4. Frontend rendering truth
- exact fields read by `Wave1DomainCards`
- whether the UI wiring matches the payload

### 5. Persistence / recomputation finding
- are these fields persisted or rebuilt live?
- does this analysis id need recomputation to pick up D-4?

### 6. Runtime/build finding
- is the running frontend/backend actually on D-4 code?
- any stale-cache/build issue found?

### 7. Browser comparison
- what the user actually sees
- what the payload says
- where they diverge

### 8. Root cause
Choose one primary cause:
- stale persisted result
- stale runtime/build
- frontend wiring mismatch
- backend logic not firing
- true D-4 logic failure
- other

### 9. Smallest safe next step
State the minimum correct remediation path.

### 10. Uncommitted / not merged
- confirm diagnosis work is not merged to `main`

---

## STOP conditions

STOP and report if:
1. the diagnosis would require broad unrelated implementation to continue
2. the target analysis id cannot be retrieved/accessed
3. the environment is too inconsistent to establish repo/runtime truth
4. you discover the real issue is outside Wave 1 scope entirely

If blocked, report:
- exact blocker
- affected files or runtime surface
- smallest safe remediation path