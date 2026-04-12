---
work_id: BE-W1-PR4
branch: feature/contextual-lab-range-extraction-and-selection
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# BE-W1-PR4 — Contextual lab-range extraction and user selection workflow

## Objective

Deliver the next Wave 1 remediation pass for the PDF upload → parse → review → analysis-input journey.

This sprint must resolve the real remaining product gap for markers whose lab reports contain multiple context-dependent reference ranges, such as:

- male
- female
- female non-pregnant
- female pregnant
- female postmenopausal
- other equivalent lab-defined contextual variants

The required outcome is:

- the parser preserves rich contextual lab reference text
- the parser attempts structured extraction of context-specific range options at parse time
- the review/edit UI shows those detected contextual options clearly
- the user can choose the applicable context when multiple valid options exist
- selecting a context auto-populates the active min/max/unit used for analysis
- raw lab text remains visible for transparency
- manual override remains available when extraction is incomplete or wrong

This sprint is not a scoring-policy sprint.
This sprint is not a fallback-range sprint.
This sprint is not a broad results/narrative sprint.

---

## Stage 1A — Authority Preflight (MANDATORY)

### Runtime truth already established

Repo/runtime investigation has established that:

- raw contextual lab reference text now survives further through the parse/review seam than before
- the unresolved product failure is not just text preservation, but lack of a workflow to resolve which contextual range applies
- the existing review/edit seam already contains:
  - raw reference text display
  - min/max/unit edit fields
  - attention badges
  - existing `reference_range` payload handoff
- the missing step is structured context-option extraction plus explicit user selection
- this work must remain outside scoring-policy changes

This sprint must not guess a different runtime truth.

### Authoritative backend files for this sprint

At minimum, inspect and use the actual current versions of:

- `backend/core/llm/prompts/parsing_prompt_pdf.txt`
- `backend/services/parsing/llm_parser.py`
- `backend/app/routes/upload.py`
- any parser models / response models touched by the PDF extraction path

### Authoritative frontend files for this sprint

At minimum, inspect and use the actual current versions of:

- `frontend/app/(app)/upload/page.tsx`
- `frontend/app/components/preview/ParsedTable.tsx`
- `frontend/app/components/preview/EditDialog.tsx`
- `frontend/app/lib/uploadReferenceRange.ts`
- `frontend/app/types/parsed.ts`

If hardening finds the active paths differ, Claude must cite the exact actual files in evidence and hardening may narrow or correct touched-file scope. Cursor must not improvise beyond those verified files.

---

## Stage 1B — Reality Check

This sprint addresses a real remaining user problem and is not a no-op.

Confirmed current gaps include:

- the system can preserve contextual lab text but does not help the user resolve which range applies
- rich text alone is not sufficient for prolactin-style markers and similar multi-context lab ranges
- users still have to manually interpret and transcribe the correct range from the contextual text
- this prevents the review flow from feeling reliable or intelligent in context-dependent cases

---

## Stage 1C — Intelligence Preflight

This sprint changes the governed parse/review behaviour for user-supplied lab data before analysis submission.

It therefore affects:

- PDF parse extraction contract
- parsed biomarker review-state contract
- review/edit user interaction before analysis
- quality of user-confirmed `reference_range` entering analysis

This is STANDARD risk. It does not touch the listed HIGH-risk directories or analytical reasoning boundaries, but it does affect governed user input before analysis and must remain tightly bounded.

No risk downgrade or scope widening is permitted.

---

## Architectural Decisions Locked For This Sprint

Cursor must implement these decisions exactly.

### 1. Structured context options are a review-stage assistive contract

The parser may extract structured context-specific range options from lab text, but these options are assistive review-stage data only.

They do not become a new SSOT or second range authority.
The authoritative user-submitted range remains the final selected or manually edited `reference_range`.

### 2. User confirmation is required when multiple context-specific ranges exist

If multiple valid contextual options are detected, the system must not silently choose one.

The user must confirm the applicable context before the range is considered resolved.

The only acceptable no-click case is:
- one single unambiguous extracted option
- or no extracted options at all

### 3. Selecting a context auto-populates the active analytical range

When the user selects a contextual option, the active min/max/unit fields used for analysis must populate automatically from that selection.

This must feed the same existing `reference_range` contract already used downstream.

### 4. Raw lab text must remain visible

Even when structured context options are extracted successfully, the original lab reference text must remain visible in review/edit for transparency.

### 5. Manual override remains available

If structured extraction is incomplete, wrong, or not trusted, the user must still be able to manually set min/max/unit.

### 6. Approach A is mandated

Use prompt-level/schema-level structured extraction in the PDF parsing path.

That means:
- extend the PDF parsing prompt/schema to request structured contextual range options directly from Gemini when present
- allow omission/null when the model cannot extract them confidently

Do not choose a regex-only post-processing strategy as the primary approach for this sprint.

### 7. Distinct review attention state required

Markers with multiple detected context options but no confirmed selection must have a distinct attention state, such as:

- context selection required

This must not be conflated with:
- valid one-sided threshold
- text-only partial range
- genuinely incomplete range

### 8. One-sided thresholds remain valid

A contextual option may itself be one-sided.
Examples:
- Male: `> 1.55`
- Adult: `< 25`

Those must remain valid selectable options.

### 9. No scoring-policy changes

This sprint must not change:
- scoring rules
- lab-range sovereignty
- fallback-range policy
- any analytical interpretation logic

### 10. Value-level inequality parsing is explicitly out of scope

This sprint does not address the separate defect family where biomarker result values themselves may be expressed as inequalities (for example `<0.05` values).

Do not widen into that problem in this sprint.

---

## Scope

## Required Changes

### A. PDF prompt/schema extension for contextual options

Update the PDF parsing prompt/schema so the parser can return structured contextual range options when the lab text clearly contains multiple context-specific reference ranges.

Each option should include, where available:
- context label
- min
- max
- unit
- optional source snippet / source line text

Confidence should be omission/null-based:
- if the model cannot structure options confidently, it may omit them and preserve only raw text

### B. Parser/model support

Update parser-side models and parse response shaping so contextual options can survive the live PDF parse path into the frontend review state.

This must preserve:
- raw reference text
- numeric `ref_low` / `ref_high` where safely extractable
- structured context options where available

### C. Frontend review-state support

Update the parsed biomarker review contract to support:
- contextual range options
- selected context id / selection state
- active `referenceRange`
- raw `referenceText`

Avoid conflicting multiple sources of truth. The precedence rule must be clear:
- selected context option populates active range
- manual edit may then override
- active `referenceRange` is what goes to analysis

### D. Review/edit UI for contextual selection

Update the review/edit experience so that for biomarkers with contextual range options:

- the user sees that multiple context-specific ranges were detected
- the raw lab text remains visible
- the selectable options are shown clearly
- selecting an option populates min/max/unit
- if no option is selected yet, the attention state reflects that
- manual override remains possible

### E. Payload handoff

Ensure the selected or manually corrected active range continues to flow through the existing `reference_range` contract to analysis start.

---

## Explicit Non-Goals

- no scoring-policy changes
- no fallback-range implementation for ordinary biomarkers
- no results-page/narrative/Gemini-output work beyond PDF parse-time extraction
- no broad parser redesign beyond this bounded contextual-range seam
- no profile-based or silent auto-selection of pregnancy/sex/life-stage context
- no second authority source for ranges
- no value-level inequality parsing work

---

## STOP Conditions (MANDATORY)

Cursor must STOP immediately if any of the following become true:

1. Supporting contextual range selection would require changing scoring policy rather than the parse/review seam
2. Prompt-level structured extraction proves too unstable and would require broad parser redesign beyond the bounded sprint
3. The design would introduce a second range authority instead of a review-stage assistive contract
4. The system cannot preserve a single active `reference_range` without conflicting sources of truth
5. The sprint would require silent medical-context inference without user confirmation
6. The sprint would widen into value-level inequality parsing
7. The sprint would require broad redesign of the upload-review flow beyond bounded contextual-range handling

If any STOP condition triggers, do not improvise. Report the blocker.

---

## Phase Execution Model

### Phase 1 — Contextual extraction and selection workflow

Implement the bounded changes required so that:

- contextual lab text is preserved
- structured context options are extracted where possible
- the user can choose the applicable context
- the active analytical range is populated from that choice
- manual override remains available
- no scoring-policy changes occur

### Phase 2 — Validation

Verify with targeted tests and browser checks that:

- a representative contextual marker such as prolactin now surfaces structured options
- selecting an option populates min/max/unit
- raw text remains visible
- context selection required state appears when appropriate
- ordinary simple-range markers still behave normally
- no regression to existing one-sided threshold support

---

## Regression Targets

Must verify all of the following.

### PDF parse extraction

- parser preserves raw contextual lab text
- parser returns structured context options when clearly present in the source
- one-sided thresholds inside context options are preserved where applicable

### Review/edit behaviour

- contextual-range markers show a clear context selection workflow
- user selection populates the active min/max/unit
- raw lab text remains visible
- manual override remains possible
- markers with options but no confirmed choice show a distinct attention state

### Analysis handoff

- active selected/manual `reference_range` still serializes through the existing payload contract
- no regressions to successful analysis submission for simple markers
- no scoring-policy changes are introduced

### Safety / determinism

- no fallback ranges introduced
- no second authority source introduced
- same parsed contextual option set + same user choice produces the same active range payload
- no silent context assumption when multiple choices exist

---

## Test Requirements

Minimum required tests must cover:

1. representative parser extraction of contextual options from a multi-range marker such as prolactin
2. one-sided contextual option support
3. review-state handling of contextual options + selected option
4. context selection required attention state
5. selected option populates active `referenceRange`
6. no regression to ordinary simple min/max markers
7. no regression to existing one-sided threshold handling for non-contextual markers

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
- do not perform broad parser redesign beyond the bounded contextual-range seam
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
   - contextual options are extracted and surfaced for representative markers
   - user selection populates active range fields
   - context selection required state appears when relevant
   - raw text remains visible
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