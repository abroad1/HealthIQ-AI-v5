---
work_id: BE-W1-PR3
branch: feature/pdf-parse-one-sided-ranges-and-rich-reference-text
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# BE-W1-PR3 — PDF parse extraction, one-sided range classification, and rich reference-text preservation

## Objective

Deliver the next Wave 1 remediation pass for the live PDF upload path.

This sprint must fix the upstream extraction seam so that the actual PDF parse flow preserves and returns enough truth for the review UI to behave correctly.

This sprint exists because BE-W1-PR1 and BE-W1-PR2 improved the upload-review frontend seam, but did not change the PDF extraction path itself. Post-sprint investigation established that the remaining defects are primarily upstream in the live PDF parse path.

The required outcome is:

- live PDF parsing preserves strict comparator semantics where present (`<`, `>`, `≤`, `≥`)
- live PDF parsing preserves richer multi-line lab reference text where available
- contextual lab reference text such as sex / pregnancy / life-stage blocks is preserved when present in the source panel
- the parse response gives the frontend enough structured truth to distinguish:
  - fully bounded range
  - valid one-sided threshold
  - rich contextual reference text
  - genuinely incomplete range
- frontend attention-state logic no longer treats valid one-sided thresholds as equivalent to incomplete ranges

This sprint is not a scoring-policy sprint.
This sprint is not a fallback-range sprint.
This sprint is not a broad results/narrative sprint.

---

## Stage 1A — Authority Preflight (MANDATORY)

### Runtime truth already established

Repo/runtime investigation has established that:

- BE-W1-PR2 changed the upload-review frontend seam only
- it did not change:
  - `LLMParser`
  - the PDF parsing prompt
  - `/api/upload/parse`
- on the live PDF path, rich reference text and strict comparator semantics depend on what the parser/model returns in the parsed `reference` field
- if the model returns shortened or symbol-free text, the frontend cannot reconstruct richer comparator/reference meaning later
- screenshot evidence shows comparator display can now work, but one-sided ranges are still being classified as incomplete in the review attention logic

This sprint must not guess a different truth.

### Authoritative backend files for this sprint

At minimum, inspect and use the actual current versions of:

- the parser models used by PDF parsing
- `LLMParser` implementation
- the PDF parsing prompt file(s), including any schema/prompt assets used for PDF extraction
- `backend/app/routes/upload.py`
- any parser response models and helpers that shape `reference`, `ref_low`, `ref_high`, raw value text, or related fields

### Authoritative frontend files for this sprint

At minimum, inspect and use the actual current versions of:

- `frontend/app/(app)/upload/page.tsx`
- `frontend/app/lib/uploadReferenceRange.ts`
- `frontend/app/components/preview/ParsedTable.tsx`
- `frontend/app/components/preview/EditDialog.tsx`
- `frontend/app/types/parsed.ts`

If hardening finds the active paths differ, Claude must cite the exact actual files in evidence and hardening may narrow or correct touched-file scope. Cursor must not improvise beyond those verified files.

---

## Stage 1B — Reality Check

This sprint addresses real UAT and investigation findings and is not a no-op.

Confirmed remaining issues include:

- the live PDF parse path does not reliably preserve richer reference text
- the live PDF parse path does not reliably preserve strict comparator semantics in a recoverable way
- pregnancy / sex / life-stage contextual range text is not being surfaced in review even when present in lab output
- valid one-sided thresholds are still being flagged as incomplete by the review UX
- previous frontend seam fixes cannot recover truth that was never extracted upstream

---

## Stage 1C — Intelligence Preflight

This sprint changes the governed parse extraction and review classification behaviour for user-supplied lab data before analysis submission.

It therefore affects:

- PDF parse extraction truth
- parser response shape / semantics
- upload-review attention classification
- user confidence in parsed lab data before analysis

This is HIGH risk because it changes user-input interpretation upstream of analysis, even though it must not change scoring policy or introduce fallback ranges.

No downgrade is permitted.

---

## Architectural Decisions Locked For This Sprint

Cursor must implement these decisions exactly.

### 1. One-sided thresholds are valid, not inherently incomplete

A lab reference such as:

- `> 1.55 mmol/L`
- `< 39`
- `≤ 5.7`
- `≥ 48`

is a valid one-sided threshold and must not automatically be treated as incomplete.

The system must distinguish between:
- valid one-sided threshold
- rich contextual reference text requiring review
- genuinely incomplete or malformed range data

### 2. Rich raw reference text is first-class evidence

If the lab provides richer reference text, including multi-line or contextual blocks such as:
- pregnancy
- sex-specific ranges
- menopausal status
- age/life-stage distinctions
that text must be preserved where possible and surfaced to the user in review.

Do not flatten it away if the parser can capture it.

### 3. Preserve raw truth before simplification

The parser and parse route must preserve the richest truthful reference representation available before any frontend simplification into numeric bounds.

Numeric `ref_low` / `ref_high` remain useful, but they are not the only truth source.

### 4. Frontend classification must use better semantics

Once richer parser truth is available, frontend attention-state logic must distinguish:
- complete bounded range
- valid one-sided threshold
- rich contextual reference text present
- no usable range/reference truth

Do not continue using a rule that effectively means:
- both min and max = complete
- everything else = incomplete

### 5. No broad fallback behaviour

Do not introduce hard-coded fallback ranges for ordinary biomarkers.

### 6. Stay within the PDF parse → review seam

This sprint must stay within:
- PDF parse extraction
- parse response contract
- upload-review classification/rendering
- review/edit usability as needed to support the improved parse truth

Do not widen into scoring-policy changes or results-page work.

---

## Scope

## Required Changes

### A. PDF parse extraction improvement

Improve the live PDF parse path so that it more faithfully captures:

- strict inequality symbols
- one-sided thresholds
- richer multi-line reference text
- contextual reference blocks such as pregnancy / sex / life-stage text

This includes prompt/schema/extraction handling in the actual PDF parse path, not just helper functions downstream.

### B. Parse response contract quality

Ensure the parse route returns enough structure for the frontend to preserve:

- raw reference text
- numeric lower/upper bounds where safely extracted
- one-sided threshold meaning where applicable
- raw parsed value text when useful

### C. Review classification improvement

Update the upload-review seam so valid one-sided thresholds are not automatically flagged as incomplete.

A richer classification model is required, grounded in the parser truth returned.

### D. Rich reference-text surfacing

Ensure rich reference text, where captured, is actually visible and usable in review for markers such as prolactin and similar complex cases.

### E. Maintain editability and payload correctness

Any improvements must remain compatible with the existing edit flow and analysis payload handoff.
Do not break the already-approved min/max/unit edit path.

---

## Explicit Non-Goals

- no scoring-policy changes
- no broad fallback-range behaviour
- no broad parser redesign beyond the bounded PDF extraction seam
- no results-page/narrative work
- no questionnaire work
- no second authority source for ranges
- no broad UX redesign outside review/edit classification and display

---

## STOP Conditions (MANDATORY)

Cursor must STOP immediately if any of the following become true:

1. Fixing the issue would require changing scoring policy rather than the parse/review seam
2. Rich reference preservation would require an open-ended parser rewrite rather than a bounded PDF extraction improvement
3. Supporting contextual reference text would require inventing a second authority source
4. Valid one-sided threshold handling cannot be distinguished cleanly from genuinely incomplete data within the current parse/review seam
5. The sprint would require broad redesign of the upload-review flow
6. The only way to preserve richer reference truth would be a non-governed free-form parser output with no stable contract

If any STOP condition triggers, do not improvise. Report the blocker.

---

## Phase Execution Model

### Phase 1 — Parser and review classification correction

Implement the bounded changes required so that:

- live PDF parsing preserves richer reference truth
- one-sided thresholds are preserved as valid semantics
- contextual reference text is retained
- review classification distinguishes valid one-sided cases from incomplete cases
- rich reference text is visible in the review experience

### Phase 2 — Validation

Verify with targeted tests and browser checks that:

- a representative PDF with one-sided thresholds now preserves them correctly
- a representative PDF with rich contextual reference text now surfaces that text
- valid one-sided thresholds are no longer flagged as incomplete
- genuinely incomplete cases are still flagged
- existing min/max edit flow still works

---

## Regression Targets

Must verify all of the following.

### PDF parse extraction

- parser captures strict comparator semantics where present
- parser preserves richer raw reference text where present
- parser preserves contextual reference blocks where present

### Review classification and display

- valid one-sided thresholds are displayed as valid one-sided thresholds
- valid one-sided thresholds are not mislabeled as incomplete
- rich reference text is visible where captured
- truly missing or malformed range data is still flagged for attention

### Edit and payload handoff

- edit flow remains functional for min/max/unit correction
- improved parsed truth does not break payload serialization
- corrected/parsed values still hand off correctly to analysis start

### Safety / determinism

- no fallback ranges introduced
- no second authority source introduced
- same PDF input produces the same parsed reference output
- no hidden repair logic or silent invented values

---

## Test Requirements

Minimum required tests must cover:

1. representative parser extraction for one-sided thresholds
2. representative parser extraction for multi-line contextual reference text
3. review classification that distinguishes valid one-sided threshold vs incomplete range
4. rich reference-text display in review
5. no regression to existing valid min/max edit behaviour

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
   - live PDF one-sided thresholds are preserved and classified correctly
   - rich contextual reference text is surfaced where available
   - valid one-sided thresholds are no longer mislabeled as incomplete
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