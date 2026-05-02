---
work_id: Q-1
branch: feature/questionnaire-ux-redesign
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# Q-1 — Questionnaire UX redesign

## Cursor agent

Use `healthiq-frontend`.

This is mandatory.

Claude already understands the design intent and prior research for this questionnaire redesign.
You should use that design intent directly when implementing.
Do not reduce this to a superficial restyle.

---

## Objective

Redesign the questionnaire experience in `QuestionnaireForm.tsx` so it feels like a guided precision-health calibration flow rather than a long admin form.

This sprint must:
- replace the current all-sections-at-once wall-of-form experience
- move to a section-by-section guided flow
- preserve backend/schema contracts
- preserve submission payload shape
- preserve conditional logic
- preserve the existing integration with the upload page

This is a real UX rebuild of the questionnaire component, not a cosmetic tidy-up.

---

## Problem being fixed

The current questionnaire is functionally working but poor UX:

- all 56 questions across 7 sections are rendered at once
- the progress bar is not semantically tied to the section structure
- dropdowns are overused where direct choice controls would be better
- the component renders all sections via one path but validates via another step-slice path, causing inconsistent required-field enforcement
- the overall feel is tedious and administrative rather than purposeful

The questionnaire is the first analytical act the user performs.
It should feel like calibrating a precision instrument, not filling in a long form.

---

## Design intent

Adopt the design direction already researched:

- precision diagnostic tone
- intent screen before questions
- section-by-section flow
- one section active at a time
- sidebar section map on desktop
- focused card-based question presentation
- pill/tile selectors for small categorical choices
- clear section progress
- calm, premium, clinically trustworthy feel

Claude’s prior questionnaire UX research should be treated as the intended design direction for this sprint.

---

## In scope

### File in scope
- `frontend/app/components/forms/QuestionnaireForm.tsx`

### Same props interface must be preserved
```ts
interface QuestionnaireFormProps {
  onSubmit: (responses: Record<string, unknown>) => void;
  onCancel?: () => void;
  initialData?: Record<string, unknown>;
  isLoading?: boolean;
}
````

Do not require caller changes.

### Required UX structure

#### Screen 0 — intent screen

Before any question is shown, present:

* headline
* short explanatory subtext
* section map with section names and time estimates
* primary “Begin” CTA
* low-prominence “Not now” / cancel path

#### Screen 1–7 — one section at a time

* one active section at a time
* desktop: sidebar left, questions right
* mobile: single-column
* completed sections visually marked
* active section clearly highlighted
* progress shown as section completion, not arbitrary question slice

### Required section display names / estimates

Use this order and naming:

* `demographics` → About you → 👤 → ~2 min
* `medical_history` → Health history → 🏥 → ~3 min
* `symptoms` → How you feel → 💬 → ~1 min
* `lifestyle` → Daily habits → 🌿 → ~3 min
* `physical_assessment` → Physical ability → 💪 → ~2 min
* `cognitive_assessment` → Mental sharpness → 🧠 → ~1 min
* `family_history` → Family story → 🧬 → ~1 min

Total visible estimate on intent screen:

* ~13 minutes

---

## Input behaviour requirements

### Small categorical sets

For dropdowns with 6 or fewer options:

* use pill/tile selectors instead of dropdowns

### Larger option sets

For dropdowns with more than 6 options:

* keep/select an appropriate searchable select pattern using current stack primitives

### Checkboxes

* use pill/tile multi-select treatment where appropriate

### Sliders

* keep slider pattern but make current value clear/prominent

### Grouped physical inputs

* render grouped inputs cleanly side by side where appropriate

### Basic text/date/number fields

* keep existing functional input types
* improve presentation to match the new UX

---

## Conditional logic

Preserve schema-driven conditional logic.

Questions with `dependsOn` logic must still hide/show correctly based on responses.

Do not break conditional display.

---

## Validation

Validation must happen on **section advance**, not on every keystroke.

Current mismatch to eliminate:

* rendering all sections while validating an arbitrary 5-question slice

Refactor validation so it validates:

* the actual active section’s visible required questions

Do not allow silent skipping of required questions in the active section.

Inline errors only.
Do not dump validation at the top of the page.

---

## State / behaviour constraints

* keep response state local
* keep payload structure passed to `onSubmit` unchanged
* preserve `?autofill=true`
* preserve existing wedge questionnaire submit behaviour
* preserve loading/error states before render

The component should track section-based flow, not arbitrary question-step slicing.

---

## Tech / design constraints

* use the approved frontend stack already in force for HealthIQ
* Tailwind only, no new CSS files
* use existing project tokens / visual language
* keep motion restrained and premium
* do not introduce new state libraries
* do not touch backend, schema, or upload page integration

---

## Out of scope

* backend schema/API changes
* upload page rewrites
* analytics event redesign
* profile integration
* PDF/export
* broader results-page work
* any non-questionnaire feature work

Do not widen scope.

---

## Acceptance criteria

1. Intent screen appears before any question is shown.
2. All 7 sections are displayed on the intent screen with names and time estimates.
3. Questionnaire advances one section at a time.
4. Active section is clearly shown; completed sections visibly marked.
5. Small categorical choices use pill/tile selectors instead of dropdowns.
6. Required validation fires on section advance against the actual active section.
7. `onSubmit` payload structure remains unchanged.
8. `onCancel` is reachable from the intent screen.
9. `?autofill=true` still works.
10. Conditional `dependsOn` logic still works.
11. No TypeScript errors introduced.
12. Upload page should not require modification to continue using this component.

---

## Testing discipline

Do not run the full repository suite.

Run only targeted checks relevant to:

* component behaviour
* section flow
* validation behaviour
* payload parity
* autofill behaviour
* conditional question logic
* type safety

Before running tests, state:

* what you will run
* why
* what broader suites you are excluding

---

## Reporting requirements

When finished, report back in these sections:

### 1. Branch

* confirm branch name

### 2. Preflight restatement

* objective
* file(s) touched
* what integration surfaces were intentionally left unchanged

### 3. UX implementation

* how the intent screen works
* how section-by-section navigation works
* how sidebar/mobile behaviour works
* how input patterns changed

### 4. Validation and logic

* how section validation now works
* how payload parity was preserved
* how `dependsOn` logic was preserved
* how `?autofill=true` was preserved

### 5. Tests run

* exact tests/checks
* results

### 6. Known limits intentionally deferred

* anything intentionally left out of scope

### 7. Uncommitted / not merged

* confirm work is not merged to `main`

---

## STOP conditions

STOP and report if:

1. preserving payload parity requires changing backend/schema contracts
2. upload page integration breaks and cannot be preserved cleanly
3. conditional question logic cannot be preserved inside the redesign
4. the redesign would require broader frontend architecture changes outside this component
5. scope starts drifting into unrelated frontend work

If blocked, report:

* exact blocker
* affected file/surface
* smallest safe remediation path

```
```
