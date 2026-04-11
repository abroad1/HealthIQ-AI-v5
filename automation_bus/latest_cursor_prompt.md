---
work_id: KB-SQ1
branch: feature/questionnaire-schema-wiring
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# KB-SQ1 — Questionnaire Schema Wiring (Upload Flow)

## Objective

Replace mock-backed questionnaire loading in the upload flow with the governed questionnaire schema from the backend, ensuring all runtime questionnaire inputs align with SSOT and are correctly fed into downstream analysis.

This is a governed-input wiring correction, not a UI redesign.

## Stage 1A — Authority Preflight (MANDATORY)

### Canonical Authority

- File:
  `backend/ssot/questionnaire.json`

This is the single source of truth for questionnaire structure and content.

### Runtime Loader

- Endpoint:
  `GET /api/questionnaire/schema`

- Defined in:
  `backend/app/routes/questionnaire.py`

- Expected response shape:
  - top-level object containing `schema`
  - `schema` is the questionnaire array loaded from `backend/ssot/questionnaire.json`

### Frontend Consumer

- Component:
  `frontend/app/components/forms/QuestionnaireForm.tsx`

- Render path:
  `frontend/app/(app)/upload/page.tsx`

### Duplicate Authority Check

The following are non-authoritative and must not be used in production runtime:

- inline `mockQuestions` in `QuestionnaireForm.tsx`
- `@/lib/mock/questionnaire`

No second authority source may be introduced.

## Stage 1B — Reality Check

Confirmed runtime defect:

- questionnaire renders successfully
- no request is made to `/api/questionnaire/schema`
- form is populated from hardcoded `mockQuestions`
- governed fields such as `blood_pressure_reading` are absent

This sprint addresses a real defect and is not a no-op.

## Stage 1C — Intelligence Preflight

This change affects:

- `questionnaire_data` passed into analysis
- contextual interpretation inputs reaching downstream runtime behaviour

Therefore this work is:

- `change_type: MIXED`
- HIGH risk under SOP rules

## Scope

### Primary Change

Update:

- `frontend/app/components/forms/QuestionnaireForm.tsx`

Replace:

- hardcoded question loading via `mockQuestions`

With:

- runtime fetch to `GET /api/questionnaire/schema`
- question source set from `response.schema`

### Requirements

- use the existing frontend API base resolution pattern already used elsewhere in the app
- include loading state
- include explicit error state
- do not silently degrade to mock questions in the normal production runtime path

### Mock Handling

- `mockQuestions` must not be used in the production questionnaire path
- if retained for test/dev purposes, it must be clearly isolated from the normal runtime path

### Rendering

- preserve existing question rendering logic where compatible
- do not redesign questionnaire UX
- do not invent new question content
- do not introduce new question types unless required by the authoritative schema and already supported

## Non-Goals

- no modification of `backend/ssot/questionnaire.json`
- no questionnaire content rewrite
- no backend route redesign if the current endpoint works
- no results, narrative, clinician report, or broader analysis-pipeline changes
- no duplicate authority source

## STOP Conditions (MANDATORY)

Cursor must STOP immediately if:

1. `/api/questionnaire/schema` does not return the expected structure
2. the authoritative schema contains field types unsupported by the current renderer
3. any backend modification appears necessary to complete the wiring
4. any production fallback to mock questions becomes necessary
5. a second authority source would be introduced
6. questionnaire submission becomes incompatible with the current analysis-start contract

## Phase Execution Model

### Phase 1 — Wiring

- implement schema fetch in `QuestionnaireForm`
- replace production use of `mockQuestions`
- ensure questionnaire renders from API-backed schema

### Phase 2 — Validation

- verify network request to `/api/questionnaire/schema`
- verify blood pressure reading fields are rendered
- verify questionnaire submission still progresses into analysis start

## Regression Targets

### Upload Flow

- upload → parse → review → questionnaire still works

### Questionnaire

- `GET /api/questionnaire/schema` is called
- `blood_pressure_reading` is present in rendered form
- production runtime no longer depends on `mockQuestions`

### Submission

- `POST /api/analysis/start` still succeeds after questionnaire completion
- questionnaire data remains compatible with the existing analysis flow

### Determinism

- same schema input produces the same rendered questionnaire
- no randomness, hidden fallback, or duplicate authority logic introduced

## Test Requirements

Minimum required:

- narrow test coverage proving questionnaire questions are sourced from API schema
- bounded assertion that `blood_pressure_reading` is surfaced in the rendered questionnaire
- smallest relevant test scope only

## Execution Rules

- follow this prompt exactly
- do not widen scope
- do not modify unrelated files
- do not introduce speculative refactors

## Deliverables

Cursor must return:

1. files changed
2. implementation summary
3. tests run and results
4. browser verification evidence showing:
   - `/api/questionnaire/schema` request observed
   - blood pressure reading fields present
5. confirmation that production runtime no longer uses `mockQuestions`
6. any blocker encountered

## Governance

This is HIGH-risk work.

Requires:

- Claude hardening
- kernel start
- controlled execution
- kernel finish
- gate evidence
- Claude audit summary
- GPT architectural review
- dual approval before merge

No shortcuts are permitted.
