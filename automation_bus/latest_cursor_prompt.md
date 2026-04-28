---
work_id: D-7
branch: feature/wave1-liver-cleanup
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# D-7 — Wave 1 liver coherence and missing-marker label cleanup

## Cursor agent

Use `healthiq-core-engine`.

This is mandatory.

---

## Objective

Implement a small, bounded follow-up to D-6.

This sprint must fix two remaining user-facing issues in the Wave 1 layer:

1. **Liver consequence coherence**
   - when the liver contributor/headline says enzymes are within range / broadly stable, the liver consequence must not jump to an active-strain / MASLD-fibrosis style message unless the resolved liver pattern genuinely supports that

2. **Missing-marker label rendering**
   - user-facing “What would improve confidence” labels must not expose internal ids or raw schema-style labels such as:
     - `total_bilirubin`
     - `ast`
     - `ggt`

This is a small cleanup sprint only.
Do not reopen the broader Wave 1 architecture work.

---

## Branch requirement

Before doing anything else:

1. create and switch to this branch:
   `feature/wave1-liver-cleanup`
2. confirm the branch name before implementation begins

If the branch already exists locally, check it out and confirm.

---

## Precondition

D-6 is complete and accepted as the Wave 1 architecture remediation.

Before implementation, restate briefly:

- the original Wave 1 contradiction issue is resolved
- cardiovascular and blood sugar are out of scope
- this sprint only fixes the remaining liver coherence and label-rendering issues

If repo reality differs, STOP and report.

---

## In scope

### A. Liver consequence coherence
1. Review the liver consequence selection path for the case where:
   - liver contributor says markers are within reference range
   - headline says broadly stable
   - no truly active liver-risk pattern is present
2. Ensure the liver consequence falls back to a neutral / proportionate explanation in that case
3. Do not emit a generic active-strain consequence when the resolved liver pattern does not support it

### B. Missing-marker label rendering
1. Replace raw/internal missing-marker ids with user-safe labels in the Wave 1 UI
2. This must cover at least the currently observed examples:
   - `total_bilirubin`
   - `ast`
   - `ggt`
3. Prefer a governed / deterministic label mapping rather than ad hoc string hacks
4. Keep the fix bounded to user-facing rendering for these confidence-improver labels

---

## Out of scope

- cardiovascular logic
- blood sugar logic
- backfill architecture
- D-6 primary-pattern selector
- “What’s driving this” architecture
- hemoglobin/unit issue
- broader results-page redesign
- Phase 2 domains

Do not widen scope.

---

## Architectural constraints

### 1. No re-opening D-6
Do not rework the Wave 1 authority architecture unless absolutely necessary for this small liver fix.

### 2. Keep the liver fix truthful
Do not make liver falsely reassuring.
The goal is coherence, not optimism.

### 3. User-safe labels only
Do not expose internal ids, snake_case labels, or implementation-shaped text in the confidence-improver section.

### 4. Deterministic only
No LLM text generation or ad hoc runtime inference.

---

## Required implementation details

## A. Liver consequence fallback
Implement a proportionate fallback when the resolved liver pattern does not support an active-strain consequence.

The corrected liver card should not produce:
- stable / in-range headline
and then
- active liver-strain / MASLD-fibrosis consequence
unless the resolved domain evidence truly supports that.

Be explicit in reporting:
- what condition now triggers the neutral fallback
- what condition still triggers the stronger consequence

## B. Missing-marker user label mapping
Implement a clean user-facing mapping for the missing/improver marker list.

At minimum ensure:
- `ast` is shown with an understandable user-facing label
- `ggt` is shown with an understandable user-facing label
- `total_bilirubin` / bilirubin-related missing labels are shown cleanly

If there is already a canonical/alias source in the repo that should drive this, use it.

---

## Files likely in scope

These are likely, not mandatory:

### Backend
- `backend/core/analytics/domain_narrative_wave1.py`
- `backend/core/analytics/domain_score_assembler.py`

### Frontend
- `frontend/app/components/results/Wave1DomainCards.tsx`
- any small helper used to render missing-marker labels safely

### Tests
- targeted backend tests
- targeted frontend/rendering tests if needed

---

## Files likely out of scope

Do not touch unless absolutely required and justified:

- `backend/core/pipeline/orchestrator.py`
- backfill runner
- pricing/billing
- upload flow
- clinician PDF/export paths
- Phase 2 domain logic
- broad KB/SSOT changes unless absolutely necessary for safe label mapping

---

## Testing discipline

Do not run the full repository test suite.

Run only:

### Backend
1. targeted test proving liver consequence is neutral/proportionate when no active liver-risk pattern is resolved
2. targeted test proving stronger liver consequence still appears when the resolved pattern genuinely supports it

### Frontend / rendering
3. targeted test proving missing/improver labels are rendered as user-safe labels, not raw ids
4. type-check for touched surfaces

Before running tests, state:
- what you will run
- why it is relevant
- what broader suites you are deliberately excluding

---

## Acceptance criteria

This sprint is successful only if:

1. Liver collapsed and expanded content no longer give a mixed stable-vs-strain story when no active liver-risk pattern is present.
2. A stronger liver consequence still appears when domain evidence genuinely supports it.
3. Missing-marker / confidence-improver labels no longer expose raw ids such as `total_bilirubin`.
4. User-facing labels for AST / GGT / bilirubin-related fields are readable and appropriate.
5. No broader Wave 1 architecture is disturbed.
6. Targeted tests pass.

---

## Reporting requirements

When finished, report back in these sections:

### 1. Branch
- confirm branch name

### 2. Preflight restatement
- objective
- files touched
- files not touched
- exact liver issue being fixed
- exact label-rendering issue being fixed

### 3. Requested changes made
- exact files changed
- how liver consequence fallback now works
- how missing-marker labels are now rendered safely

### 4. Tests run
- exact tests
- results

### 5. Browser/UAT note
- whether this should now be rechecked in live UAT on the same liver case

### 6. Known limits intentionally deferred
- anything still intentionally left out of scope

### 7. Uncommitted / not merged
- confirm work is not merged to `main`

---

## STOP conditions

STOP and report if:

1. fixing liver consequence coherence requires reopening the full Wave 1 authority architecture
2. safe label rendering requires a much broader schema/content change than expected
3. the liver issue turns out to be driven by the separate hemoglobin/unit/data problem
4. scope starts to drift back into D-6 areas

If blocked, report:
- exact blocker
- affected files/surfaces
- smallest safe remediation path