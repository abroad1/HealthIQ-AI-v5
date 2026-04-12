---
work_id: BE-W1-PR5
branch: feature/reference-type-modelling-and-review-ux-completion
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# BE-W1-PR5 — Reference-type modelling and review UX completion

## Objective

Deliver the next Wave 1 remediation pass for the upload → parse → review → analysis-input journey.

This sprint must complete the review-stage modelling of different lab reference logic types so the user no longer has to fight the UI to represent what the lab actually said.

The required outcome is:

- parsed biomarkers are explicitly classified into the correct review-stage reference type
- labelled interpretation bands are handled correctly
- applicability-dependent reference bands are handled correctly
- comparator-based one-sided thresholds can be edited faithfully
- genuine “no lab range supplied” cases are handled as valid lab outputs
- downstream analysis still receives the same singular `reference_range` contract where applicable
- no scoring-policy or fallback-range behaviour is changed

This sprint is not a scoring-policy sprint.
This sprint is not a fallback-range sprint.
This sprint is not a results/narrative sprint.

---

## Stage 1A — Authority Preflight (MANDATORY)

### Runtime truth already established

Repo/runtime validation has established that:

- PR4 correctly introduced contextual/applicability band extraction and user selection
- the remaining gap is broader: the review seam still lacks first-class modelling of different reference logic types
- current frontend attention and edit behaviour is still driven too much by data presence/absence rather than explicit reference semantics
- the existing review/edit seam already contains:
  - raw reference text display
  - min/max/unit edit fields
  - PR4 applicability-band selection flow
  - existing `reference_range` payload handoff
- scoring policy and fallback policy must remain unchanged

This sprint must not guess a different truth.

### Authoritative backend files for this sprint

At minimum, inspect and use the actual current versions of:

- `backend/core/llm/prompts/parsing_prompt_pdf.txt`
- `backend/services/parsing/llm_parser.py`
- `backend/app/routes/upload.py`
- any parser models / response models touched by the PDF extraction path

### Authoritative frontend files for this sprint

At minimum, inspect and use the actual current versions of:

- `frontend/app/types/parsed.ts`
- `frontend/app/lib/uploadReferenceRange.ts`
- `frontend/app/(app)/upload/page.tsx`
- `frontend/app/components/preview/ParsedTable.tsx`
- `frontend/app/components/preview/EditDialog.tsx`

If hardening finds the active paths differ, Claude must cite the exact actual files in evidence and hardening may narrow or correct touched-file scope. Cursor must not improvise beyond those verified files.

---

## Stage 1B — Reality Check

This sprint addresses a real remaining product gap and is not a no-op.

Confirmed remaining issues include:

- labelled interpretation bands (for example folate-style “Deficient / Intermediate / Normal”) are not yet treated as a first-class reference mode
- comparator-based thresholds cannot yet be faithfully entered in manual edit
- genuine no-range-supplied cases are still conflated with missing/incomplete parsing
- different range semantics are still being forced through the same incomplete/missing logic
- the product needs an explicit review-stage reference model, not further patching by special case

---

## Stage 1C — Intelligence Preflight

This sprint changes the governed parse/review behaviour for user-supplied lab data before analysis submission.

It therefore affects:

- PDF parse extraction contract
- parsed biomarker review-state contract
- review/edit user interaction before analysis
- quality and semantics of user-confirmed `reference_range` entering analysis

This is STANDARD risk. It does not touch the listed HIGH-risk directories or analytical reasoning boundaries, but it does affect governed input before analysis and must remain tightly bounded.

No risk downgrade or scope widening is permitted.

---

## Architectural Decisions Locked For This Sprint

Cursor must implement these decisions exactly.

### 1. Reference type becomes first-class

The product must no longer infer review behaviour indirectly from missing min/max alone.

Introduce an explicit review-stage `referenceType` model with the following supported values:

- `bounded_range`
- `one_sided_threshold`
- `applicability_band_selection`
- `labelled_bands`
- `no_lab_range_supplied`
- `incomplete_or_ambiguous`

This is a review-stage contract improvement, not a second scoring authority.

### 2. Classification authority is explicitly split

The following `referenceType` values must be **LLM-originated parse outputs** from the PDF prompt/schema:

- `labelled_bands`
- `applicability_band_selection`
- `no_lab_range_supplied`
- `incomplete_or_ambiguous`

The following may remain **frontend-derived or helper-derived** from resolved numeric range structure:

- `bounded_range`
- `one_sided_threshold`

Do not leave this ambiguous.

### 3. Labelled bands auto-resolve from measured value

For markers with labelled interpretation bands, such as:

- Deficient
- Intermediate
- Normal
- Optimal
- Borderline
- equivalent lab-defined labels

the system must auto-resolve the matching band from the measured value.

This is not a user-choice workflow.

The matched band may populate the active review-stage `referenceRange` where appropriate, while raw band text remains visible.

### 4. Applicability bands require user confirmation

For markers whose applicable reference band depends on a condition such as:

- patient context
- pregnancy/menopausal status
- sex
- collection time
- fasting / non-fasting
- other lab-defined applicability condition

the user must confirm the applicable band when multiple valid options exist.

Do not silently choose one.

This is the generalised PR4 flow and must remain non-regressed.

### 5. Comparator-aware manual editing must be supported

The edit dialog must support faithful one-sided threshold entry.

At minimum, in one-sided edit mode, users must be able to enter:

- comparator
- numeric value
- unit

Do not force one-sided lab logic through bare numeric-only entry.

This must remain narrowly scoped and must not change the downstream payload shape.

### 6. No-lab-range-supplied is a valid state

`no_lab_range_supplied` must be treated as a legitimate lab-output state, not as a parsing defect.

This state must be emitted conservatively:
- only when the PDF genuinely provides no usable reference interval for that marker
- not when the parser is uncertain or failed to classify a supplied reference block

Uncertain or conflicting cases must remain `incomplete_or_ambiguous`.

### 7. Active analytical range remains singular

Even with richer review-state modelling, analysis submission must still use a singular active `reference_range` where applicable.

Do not introduce multiple downstream range authorities.

### 8. Raw lab text must remain visible

Even when structured bands or thresholds are extracted successfully, the original lab reference text must remain visible in review/edit for transparency.

### 9. Manual override remains available

If structured extraction is incomplete or wrong, manual edit remains available.

### 10. No scoring-policy or fallback-range changes

This sprint must not change:
- scoring rules
- lab-range sovereignty
- fallback policy
- analytical reasoning logic

### 11. PR4 behaviour must not regress

Existing applicability-band extraction and selection from PR4 must continue to work.
PR5 generalises and formalises the model; it must not break the current working flow.

### 12. Value-level inequality parsing remains out of scope

This sprint does not address the separate defect family where biomarker result values themselves may be expressed as inequalities (for example `<0.05` values).

Do not widen into that problem.

---

## Scope

## Required Changes

### A. PDF prompt/schema extension for reference type

Update the PDF parsing prompt/schema so the parser can explicitly emit `referenceType` for the supported LLM-originated classes:

- `labelled_bands`
- `applicability_band_selection`
- `no_lab_range_supplied`
- `incomplete_or_ambiguous`

The prompt must include conservative instructions for `no_lab_range_supplied`:
- emit this only when no lab interval is genuinely present
- if reference text exists but cannot be confidently structured, emit `incomplete_or_ambiguous`

### B. Parser/model support

Update parser-side models and parse response shaping so the live PDF parse path can return and preserve:

- `referenceType`
- raw reference text
- structured labelled bands where present
- structured applicability bands where present
- existing numeric `ref_low` / `ref_high` where safely extractable

### C. Parsed biomarker review-state contract

Update the frontend parsed biomarker contract to support:

- `referenceType`
- labelled bands
- applicability bands
- active `referenceRange`
- raw `referenceText`

Avoid conflicting multiple sources of truth.

The precedence rule must be clear:

- parser-provided structured band data populates review options
- labelled bands auto-resolve to matched active range where appropriate
- applicability bands require selection when multiple exist
- manual edit may override
- active `referenceRange` is what goes to analysis

### D. Labelled-band support in review

For markers like folate, the review/edit experience must:

- show the raw lab text
- show the structured labelled bands where available
- determine the applicable band from the measured value automatically
- surface the matched band clearly
- avoid turning labelled bands into a user-selection workflow

### E. Applicability-band support in review

For markers like prolactin or cortisol, the review/edit experience must:

- show the raw lab text
- show the structured applicability bands where available
- require user selection when multiple valid bands exist
- populate min/max/unit from the selected band
- show a distinct “selection required” attention state until resolved

### F. Comparator-aware editing

Extend the edit workflow so comparator-aware one-sided thresholds can be entered and preserved in the review state.

Scope this narrowly:
- comparator selector appears only in one-sided edit mode or equivalent bounded condition
- do not broadly redesign the edit form
- keep `referenceRangeToPayload()` shape unchanged

### G. No-range-supplied state in review

Add a distinct valid review state for `no_lab_range_supplied`.

This must:

- render as a neutral valid state, not a failure state
- allow optional manual entry if the user wishes
- keep analysis payload shape unchanged (`reference_range: null` when no active range exists)

### H. Review attention and badges by type

Update review attention logic so it can distinguish at minimum:

- bounded range resolved
- one-sided threshold resolved
- applicability band selection required
- labelled bands resolved
- no lab range supplied
- incomplete or ambiguous

Do not continue using one generic missing/incomplete path for these different states.

### I. Payload handoff unchanged

Ensure the selected or auto-resolved active range continues to flow through the existing `reference_range` contract to analysis start.

---

## Explicit Non-Goals

- no scoring-policy changes
- no fallback-range implementation for ordinary biomarkers
- no results-page/narrative/Gemini-output work
- no broad parser rewrite beyond the upload/review seam
- no profile-based or silent auto-selection when multiple applicability bands exist
- no second authority source for ranges
- no value-level inequality parsing work

---

## STOP Conditions (MANDATORY)

Cursor must STOP immediately if any of the following become true:

1. Supporting the required reference types would require changing scoring policy rather than the parse/review seam
2. The parser cannot emit stable `referenceType` and structured band data without a broad parser rewrite beyond this bounded sprint
3. The design would introduce a second range authority instead of a review-stage assistive contract
4. The system cannot preserve a singular active `reference_range` without conflicting sources of truth
5. The only way to resolve applicability bands would be silent medical-context inference without user confirmation
6. `no_lab_range_supplied` cannot be emitted conservatively and would hide genuine parse defects
7. The sprint would widen into value-level inequality parsing
8. The sprint would require broad redesign of the upload-review flow beyond bounded reference-type handling

If any STOP condition triggers, do not improvise. Report the blocker.

---

## Phase Execution Model

### Phase 1 — Reference-type modelling and review completion

Implement the bounded changes required so that:

- parsed biomarkers can carry explicit reference type
- labelled bands are supported and auto-resolved
- applicability bands are supported and user-selectable
- comparator-aware one-sided editing is supported
- genuine no-range-supplied cases are modelled correctly
- raw text remains visible
- active range payload shape remains unchanged
- no scoring-policy changes occur

### Phase 2 — Validation

Verify with targeted tests and browser checks that:

- folate-style labelled bands are parsed and matched correctly
- prolactin-style applicability bands still work and do not regress
- cortisol-style condition-dependent applicability bands still work and do not regress
- comparator-aware manual editing works in one-sided mode
- no-lab-range-supplied markers display correctly
- ordinary simple-range markers still behave normally

---

## Regression Targets

Must verify all of the following.

### Parse extraction

- parser preserves raw reference text
- parser emits `referenceType` correctly for LLM-originated classes
- parser returns structured labelled bands when clearly present
- parser returns structured applicability bands when clearly present
- parser emits `no_lab_range_supplied` conservatively only where appropriate

### Review/edit behaviour

- review behaviour is driven by `referenceType`
- labelled-band markers auto-resolve to the matching band
- applicability-band markers require user confirmation when multiple exist
- comparator-aware editing works for one-sided thresholds
- no-range-supplied markers show a distinct valid state
- incomplete/ambiguous markers remain distinct from legitimate no-range cases

### Analysis handoff

- active selected or auto-resolved `referenceRange` still serializes through the existing payload contract
- no regressions to successful analysis submission for ordinary markers
- no scoring-policy changes are introduced

### Safety / determinism

- no fallback ranges introduced
- no second authority source introduced
- same parsed output + same user choices produce the same active payload
- no silent applicability-band auto-selection when multiple options exist

### PR4 non-regression

- previously working contextual/applicability-band selection cases still work after the generalisation to `referenceType`

---

## Test Requirements

Minimum required tests must cover:

1. parser extraction of `referenceType` for a labelled-band marker
2. parser extraction of `referenceType` for an applicability-band marker
3. conservative `no_lab_range_supplied` emission vs `incomplete_or_ambiguous`
4. labelled-band auto-resolution from measured value
5. applicability-band user-selection flow
6. comparator-aware one-sided edit handling
7. distinct no-range-supplied review attention state
8. no regression to ordinary simple min/max markers
9. no regression to PR4 applicability-band workflow

Use the smallest relevant test scope.
Do not expand into broad unrelated suite creation.

---

## Execution Rules

- follow this prompt exactly
- do not change scoring policy
- do not introduce fallback ranges
- do not invent a second authority source
- do not widen into results/questionnaire/narrative work
- do not widen into value-level inequality parsing
- do not perform broad parser redesign beyond the bounded reference-type seam
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
   - reference types are now modelled explicitly
   - labelled bands are parsed and auto-resolved correctly
   - applicability bands are parsed and user-selectable correctly
   - comparator-aware editing works
   - no-range-supplied markers are handled as valid states
   - PR4 behaviour remains intact
7. any blockers encountered

---

## Governance

This is STANDARD-risk governed input-contract work.

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