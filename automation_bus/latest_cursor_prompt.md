---
work_id: BE-W1-PR2
branch: feature/parse-inequalities-and-rich-reference-text
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# BE-W1-PR2 — Parse inequality handling, rich reference-text preservation, and review usability

## Objective

Deliver the Wave 1 follow-on remediation pass for the upload → parse → review → edit journey.

This sprint must resolve the remaining defects around:

- one-sided ranges not being handled gracefully in the actual review UX
- `<`, `>`, `≤`, `≥` style values/ranges still being mishandled
- raw parsed values with inequality symbols being visible but not meaningfully usable
- rich multi-line lab reference text still not being surfaced for markers like prolactin

This sprint is not a scoring-policy sprint.
This sprint is not a fallback-range sprint.
This sprint is not a broad parser rewrite.

The required outcome is:

- one-sided ranges are supported end to end in real UX, not just internal payload shape
- inequality symbols are treated as first-class supported cases in parse/review/edit/display
- raw parsed values are usable to help the user correct parsing issues
- rich lab reference text is preserved and surfaced where already captured
- the user can clearly understand and intervene when the lab’s range structure is more complex than a simple min/max pair

---

## Stage 1A — Authority Preflight (MANDATORY)

### Runtime truth already established

Repo/runtime investigations and UAT have established that:

- one-sided bounds may now survive in internal payloads, but the UX still appears not to handle them gracefully
- the system still appears to mishandle `<` / `>` style values or ranges in the live review experience
- the edit dialog shows raw parsed values including inequality symbols, but the field is not meaningfully usable
- rich multi-line reference text for biomarkers such as prolactin still does not appear clearly in the review flow
- this is a follow-on Wave 1 defect cluster inside the same upload-review seam, not a scoring-policy issue

This sprint must not guess a different runtime truth.

### Authoritative backend files for this sprint

At minimum, inspect and use the actual current versions of:

- parser models and parser output definitions used in upload parse
- `backend/app/routes/upload.py`
- any parser helpers that capture `reference`, `ref_low`, `ref_high`, raw value text, or equivalent
- any backend-normalisation files read by this seam if needed for contract confirmation

### Authoritative frontend files for this sprint

At minimum, inspect and use the actual current versions of:

- `frontend/app/(app)/upload/page.tsx`
- `frontend/app/components/preview/ParsedTable.tsx`
- `frontend/app/components/preview/EditDialog.tsx`
- `frontend/app/lib/uploadReferenceRange.ts`
- `frontend/app/types/parsed.ts`

If hardening finds the active component or helper paths differ, Claude must cite the exact actual files in evidence and hardening may narrow or correct touched-file scope. Cursor must not improvise beyond those verified files.

---

## Stage 1B — Reality Check

This sprint addresses real UAT findings and is not a no-op.

Confirmed remaining issues include:

- one-sided ranges still appear awkward or unsupported in the visible review UX
- `<`, `>`, `≤`, `≥` handling is still not trustworthy in the full user path
- the UI still appears to imply that both min and max are required when that is not always true
- raw parsed value visibility is not yet usefully actionable
- rich multi-line reference text is still not meaningfully surfaced in review

---

## Stage 1C — Intelligence Preflight

This sprint changes user-visible parsed biomarker state and user-editable review behaviour before analysis submission.

It therefore affects:

- parse fidelity presentation
- user correction behaviour
- upload-review UX
- analysis input quality through corrected review state

This is HIGH risk because it changes governed user-supplied input behaviour entering analysis, even though it must not change scoring policy or introduce fallback ranges.

No downgrade is permitted.

---

## Architectural Decisions Locked For This Sprint

Cursor must implement these decisions exactly.

### 1. One-sided ranges are valid first-class cases

The system must not assume both lower and upper bounds are required for every biomarker reference range.

The following are valid supported cases in this sprint:

- lower-bound only
- upper-bound only
- inequality-style raw values / raw range text using `<`, `>`, `≤`, `≥`

### 2. No broad fallback behaviour

Do not introduce hard-coded fallback ranges for ordinary biomarkers.

The approved recovery path remains:

- preserve the lab’s range/value detail where possible
- make the parsing limitation visible
- let the user correct the data manually where needed

### 3. Rich reference text must be preserved where captured

If the parser already captures rich raw reference text, the review experience must preserve and surface that text in a bounded, user-usable way.

Do not silently flatten it away if the contract can already carry it.

### 4. Raw parsed values must be usable

If a raw parsed value containing an inequality symbol is shown to the user, it must be meaningfully usable for correction support.

At minimum, it must be selectable/copyable or otherwise clearly presented as a read-only assistive field.

### 5. Stay inside the upload-review seam

This sprint must stay within:

- parser output handling
- parsed biomarker state
- review table display
- edit dialog usability
- analysis payload preparation

Do not widen into scoring-policy, results-page, or narrative-layer work.

---

## Scope

## Required Changes

### A. One-sided range UX completion

Complete the one-sided range support so the actual review UX handles and displays these cases cleanly.

This includes:

- review table display
- edit dialog initialization
- saved edit state
- analysis payload serialization

### B. Inequality symbol support

Fix `<`, `>`, `≤`, `≥` handling across the full visible user seam:

- parse capture
- parsed review state
- table display
- edit dialog
- corrected submission payload

### C. Raw parsed value usability

Make raw parsed values with inequality symbols meaningfully usable in the edit flow.

This is a bounded usability requirement, not a broad redesign.

### D. Rich reference-text surfacing

Preserve and surface rich multi-line lab reference text, where already captured, for markers such as prolactin and similar complex lab reference patterns.

This must help the user understand that the lab provided more nuanced range context than a simple numeric min/max pair.

### E. Maintain review-stage attention UX

Ensure that biomarkers with complex, partial, or ambiguous reference structures remain clearly flagged for user attention where appropriate.

---

## Explicit Non-Goals

- no scoring-policy changes
- no broad fallback-range behaviour
- no broad parser rewrite
- no results-page/narrative/Gemini work
- no questionnaire work
- no new second authority source for biomarker ranges
- no broad UX redesign beyond this bounded review/edit seam

---

## STOP Conditions (MANDATORY)

Cursor must STOP immediately if any of the following become true:

1. Fixing one-sided or inequality handling would require changing scoring policy rather than the upload-review seam
2. Rich reference text cannot be surfaced without a broad parser rewrite rather than bounded preservation/display work
3. Supporting these cases would require introducing a second range/value authority source
4. The only way to resolve the issue would be a broad redesign of the upload-review flow
5. Raw parsed value usability cannot be improved without widening outside the edit/review seam
6. The sprint would require broad fallback behaviour contrary to the locked Wave 1 policy

If any STOP condition triggers, do not improvise. Report the blocker.

---

## Phase Execution Model

### Phase 1 — Upload-review defect correction

Implement the bounded changes required so that:

- one-sided ranges are visible and usable
- inequality symbols are preserved and handled properly
- raw parsed values are useful to the user
- rich reference text is surfaced where available
- missing/complex range states remain clearly flagged

### Phase 2 — Validation

Verify with targeted tests and browser checks that:

- one-sided ranges no longer feel broken in the live review UX
- inequality-style values/ranges are handled cleanly
- raw parsed values are usable
- rich reference text is visible for supported examples
- no scoring-policy or fallback-policy changes were introduced

---

## Regression Targets

Must verify all of the following.

### Parse / review fidelity

- one-sided bounds survive parse → review → edit → payload
- `<`, `>`, `≤`, `≥` cases are not silently broken or flattened in UX
- rich reference text is preserved where captured

### Edit usability

- raw parsed value is meaningfully usable in the edit dialog
- edited one-sided or inequality-based entries persist correctly
- no regression to normal min/max range editing

### Analysis handoff

- corrected values/ranges still flow through the existing payload contract
- no regressions to successful analysis submission from valid reviewed biomarkers

### Safety / determinism

- no fallback ranges introduced
- no second authority source introduced
- same reviewed input produces the same payload
- no hidden repair logic or silent data invention

---

## Test Requirements

Minimum required tests must cover:

1. one-sided bounds through review/edit/payload
2. inequality-symbol handling in the visible review/edit seam
3. raw parsed value usability / rendering behaviour
4. rich reference-text preservation and display for a representative marker such as prolactin
5. no regression to existing valid range-edit behaviour

Use the smallest relevant test scope.
Do not expand into broad unrelated suite creation.

---

## Execution Rules

- follow this prompt exactly
- do not turn this into a fallback-range sprint
- do not change scoring policy
- do not invent a second authority source
- do not widen into results/questionnaire/narrative work
- do not perform broad parser redesign beyond the bounded seam improvement
- do not modify unrelated files

---

## Deliverables

Cursor must return:

1. files changed
2. exact backend files touched
3. exact frontend files touched
4. implementation summary
5. tests run and results
6. before/after evidence that:
   - one-sided ranges are now handled gracefully in the review UX
   - inequality symbols are supported end to end in this seam
   - raw parsed values are usable
   - rich reference text is surfaced where available
7. any blockers encountered

---

## Governance

This is HIGH-risk governed input-contract work.

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