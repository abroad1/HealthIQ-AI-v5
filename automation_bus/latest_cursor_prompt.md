---
work_id: BE-W1-PR6
branch: feature/review-cleanup-comparator-unit-no-range-state
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# BE-W1-PR6 — Review cleanup: comparator display, duplicate unit UI, and no-range-supplied classification

## Objective

Deliver a small, bounded cleanup pass for the upload/review experience.

This sprint must fix the remaining review-layer anomalies without reopening the broader parsing programme.

The required outcome is:

- matched one-sided/labelled-band thresholds display the correct comparator symbol instead of a dash
- the edit UI does not redundantly show the range unit twice in a confusing way
- markers for which the lab genuinely supplied no range are classified and shown as `no_lab_range_supplied`, not `Range needed`

This sprint is not a new parsing architecture sprint.
This sprint is not a scoring-policy sprint.
This sprint is not a fallback-range sprint.
This sprint is not a results/narrative sprint.

---

## Stage 1A — Authority Preflight (MANDATORY)

### Runtime truth already established

Recent UAT after PR5 shows the main parsing/review workflow is largely working, but three narrow issues remain:

1. comparator display anomaly
   - a dash is shown where a `<` comparator should be shown for a matched labelled band / one-sided threshold

2. duplicate unit presentation
   - the range unit is shown again beneath the comparator area in a way that feels redundant/confusing

3. no-range-supplied misclassification
   - markers such as Free Testosterone % and Testosterone:Free Testosterone Ratio are still being flagged as `Range needed` even though the lab did not provide a range

This sprint must stay tightly focused on those issues.

### Authoritative frontend files for this sprint

At minimum, inspect and use the actual current versions of:

- `frontend/app/lib/uploadReferenceRange.ts`
- `frontend/app/components/preview/ParsedTable.tsx`
- `frontend/app/components/preview/EditDialog.tsx`
- `frontend/app/(app)/upload/page.tsx`
- `frontend/app/types/parsed.ts`

### Authoritative backend files for this sprint

Inspect backend only if needed to confirm whether `referenceType` / no-range state is or is not being emitted correctly for the affected markers. If a backend touch is required, keep it minimal and bounded to the parse/review seam.

If hardening finds the active paths differ, Claude must cite the exact actual files in evidence and hardening may narrow or correct touched-file scope. Cursor must not improvise beyond those verified files.

---

## Stage 1B — Reality Check

This sprint addresses real user-visible defects and is not a no-op.

However, it is deliberately small.

It must not widen into:
- broader parser redesign
- new reference-type expansion
- scoring changes
- narrative/results work

---

## Architectural Decisions Locked For This Sprint

Cursor must implement these decisions exactly.

### 1. Comparator display must reflect actual resolved threshold semantics

Where the system has already resolved a one-sided threshold or matched labelled band such as:
- Normal: `< 39`
the displayed active range must show the actual comparator, not a placeholder dash.

### 2. Unit presentation must be simplified, not duplicated

The edit form should show the unit once in the most useful place for the user.
Do not show redundant unit presentation that adds confusion without adding information.

### 3. No-lab-range-supplied is a valid neutral state

If the lab genuinely did not provide a range for a marker, the review layer must show that as a valid neutral state, not as `Range needed`.

This is especially important for calculated / derived markers.

### 4. No scoring-policy or fallback changes

This sprint must not change:
- scoring
- fallback behaviour
- payload shape
- results logic

### 5. Keep this a cleanup pass

Do not introduce new ambitious parsing behaviour in this sprint.
Fix only the three enumerated issues.

---

## Scope

## Required Changes

### A. Comparator display cleanup
Fix the review/edit rendering path so resolved one-sided thresholds display the correct comparator symbol instead of `—` or other placeholder output.

### B. Duplicate unit cleanup
Refine the edit UI so the range unit is presented clearly once, without redundant repetition.

### C. No-range-supplied classification cleanup
Fix the review-state classification/rendering so markers with genuinely absent lab ranges surface as:
- `No lab range supplied`
or equivalent neutral state,
not:
- `Range needed`

If the root cause is frontend classification only, keep the fix frontend-only.
If the root cause is parser emission for these markers, make the smallest bounded parse/review seam correction necessary.

---

## Explicit Non-Goals

- no broad parser improvements
- no new reference-type classes
- no scoring-policy changes
- no fallback-range changes
- no results-page/narrative work
- no broad UX redesign
- no value-level inequality work

---

## STOP Conditions (MANDATORY)

Cursor must STOP immediately if any of the following become true:

1. fixing the no-range-supplied state would require broader parser redesign rather than a bounded classification fix
2. comparator display correction would require changing payload shape or scoring semantics
3. the unit presentation cleanup would require broad edit-form redesign
4. the sprint begins to widen into general parsing-quality work beyond the three enumerated issues

If any STOP condition triggers, do not improvise. Report the blocker.

---

## Phase Execution Model

### Phase 1 — Cleanup implementation
Implement the smallest safe changes required to resolve the three review-layer issues.

### Phase 2 — Validation
Verify with targeted tests and browser checks that:

- `<` / `>` style resolved ranges display correctly
- duplicate unit presentation is gone
- genuinely no-range-supplied markers no longer show `Range needed`
- existing PR4/PR5 behaviour is not regressed

---

## Regression Targets

Must verify all of the following.

### Review display
- resolved one-sided thresholds show the correct comparator
- labelled-band matched thresholds display correctly
- unit presentation is clear and non-duplicative

### Review state
- no-range-supplied markers render as a valid neutral state
- incomplete/ambiguous markers remain distinct from true no-range-supplied cases

### Non-regression
- PR4 applicability-band selection still works
- PR5 labelled-band handling still works
- ordinary bounded ranges still work
- analysis payload shape remains unchanged

---

## Test Requirements

Minimum required tests must cover:

1. comparator display for a resolved one-sided / labelled-band threshold
2. no-range-supplied classification for a representative derived/calculated marker
3. non-regression for labelled-band and applicability-band review behaviour

Use the smallest relevant test scope.
Do not expand into broad unrelated suite creation.

---

## Execution Rules

- follow this prompt exactly
- keep scope tiny
- do not widen into general parsing work
- do not change scoring or fallback behaviour
- do not modify unrelated files

---

## Deliverables

Cursor must return:

1. files changed
2. concise implementation summary
3. tests run and results
4. before/after evidence for:
   - comparator display
   - unit cleanup
   - no-range-supplied state
5. any blockers encountered

---

## Governance

This is STANDARD-risk governed review-layer cleanup work.

Requires:

- Claude hardening
- kernel start
- controlled execution
- kernel finish
- gate evidence
- Claude audit summary
- GPT architectural review
- dual approval before merge

No shortcuts permitted.