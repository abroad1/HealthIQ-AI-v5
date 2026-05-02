---
work_id: Q-2
branch: feature/questionnaire-visual-redesign
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# Q-2 — Questionnaire visual redesign

## Cursor agent

Use `healthiq-frontend`.

This is mandatory.

Claude already understands the design intent and prior research for this redesign.
Use that design intent directly.
Do not reduce this to a superficial restyle.

---

## Objective

Keep the Q-1 questionnaire UX architecture intact, but redesign the visual layer so the questionnaire feels like a premium diagnostic calibration flow rather than a generic form.

This sprint must:
- preserve the Q-1 functional behaviour
- preserve props and payload parity
- preserve conditional logic
- preserve schema-driven flow
- materially improve the visual design

This is a visual redesign sprint, not a backend or schema sprint.

---

## Why Q-1 was not enough

Q-1 fixed the questionnaire flow and logic, but the visual result was still poor because the prompt did not give a strong enough design direction.

The outcome was too generic:
- default-looking component styling
- weak hierarchy
- indistinct question cards
- weak selected states
- visually invisible sidebar
- no premium launch moment
- dark/light collisions on the intent screen
- card-within-a-card framing caused by the upload page wrapper

Q-2 exists to fix that.

---

## Design direction

HealthIQ is a precision diagnostic instrument.

The questionnaire should feel like calibrating something important.

### Tone
- dark
- controlled
- intelligent
- premium
- clinically trustworthy

### Not
- pastel
- soft wellness-app styling
- rounded-everything
- chatty or playful
- generic shadcn defaults

### Yes
- high contrast
- deliberate typography
- purposeful use of green accent
- visible structure
- restrained but premium motion

---

## In scope

### Files in scope
- `frontend/app/components/forms/QuestionnaireForm.tsx`
- `frontend/app/(app)/upload/page.tsx`

No backend changes.
No schema changes.
No props interface changes.
No analytics event changes.

---

## Functional rules from Q-1 that must remain intact

Do not break any of the following:

- props interface
- flat `Record<string, unknown>` submission payload
- `conditionalDisplay` / `dependsOn` logic
- section order, names, and estimates
- `?autofill=true`
- schema loading path
- loading/error states
- validation behaviour
- section-by-section flow
- intent screen flow
- upload-page integration

All Q-1 behavioural acceptance criteria remain in force.

---

## Required visual redesign

## A. Intent screen

### Root background
The intent screen must own its background.

Use:
- `bg-background`

Do not inherit or rely on a light upload-page card background.
This must eliminate the dark/light unreadable-text collision.

Add subtle ambient green radial glow in the background.

### Headline font
Load `DM_Serif_Display` via `next/font/google`.

Use it **only** for the intent-screen headline.

Do not spread the display font across the rest of the form.

### Headline treatment
Large, high-presence, two-line headline.
It should feel intentional and premium, not generic.

### Supporting copy
Use calmer, readable body copy with clear hierarchy.

### Section map
The 7 section cards on the intent screen should feel like a diagnostic map, not generic cards.

Required qualities:
- clear border
- visible hover treatment
- subtle accent
- visible structure
- readable time estimates

### Time/readout styling
Section estimates and total-time line should use the green accent and monospace styling so they feel like diagnostic readouts.

### Begin CTA
The Begin button must feel like a launch moment.
It should have clearly more visual weight than a normal secondary button.

### Cancel path
“Not now” remains low prominence.

---

## B. Upload page wrapper

The questionnaire must own its own framing.

Remove the outer upload-page Card wrapper around `<QuestionnaireForm />` so the questionnaire is rendered directly.

Keep the green “markers confirmed” confirmation card above it unchanged.

This is necessary to eliminate the card-within-a-card problem.

---

## C. Questionnaire shell

### Outer layout
Do not wrap the whole questionnaire flow in another card-like shell.
Use the page background and internal structure to define containment.

### Sidebar
The desktop sidebar must be clearly visible, with:
- proper card/background presence
- border separation
- clear active state
- clear completed state
- dimmed future state
- visible progress footer

The current near-transparent muted panel look is not acceptable.

### Active section state
Use the brand green tint/primary treatment, not a generic neutral ring state.

### Mobile section strip
Use the same semantic treatment as desktop:
- active
- done
- pending
must read clearly and consistently.

---

## D. Section content area

### Section header
Increase hierarchy and clarity.
The active section should feel like the user is entering a defined stage of calibration.

### Section estimate
Use green monospace styling, consistent with the intent screen.

### Top marker
Add a visible top-border/accent treatment for the active section content area.

---

## E. Question cards

Question cards must no longer feel identical and flat.

Required improvements:
- clearer separation
- better hierarchy
- stronger question label styling
- visible question numbering within each section

Each visible question in a section must show a sequential `Q{n}` identifier above the label in a subtle diagnostic/readout style.

---

## F. Inputs

### Pill/tile selectors — critical
The selected state must be unambiguous.

Do not use a faint tinted selected state.

Selected options must use a strong, obvious selected treatment.
Unselected options must still look interactive and premium.

### Sliders
Upgrade the slider presentation so the current value is prominent and feels intentional.
Do not leave it as a generic boxed control.

### General controls
Text inputs, grouped inputs, and large-option selectors should all visually belong to the same premium diagnostic system.

---

## G. Motion

Use only restrained motion already compatible with the current stack and existing Tailwind/keyframe setup.

Required motion moments:
- intent-screen content entrance
- staggered section-card entrance on intent screen
- section-content entrance on section advance
- smooth selected-state transitions for pill tiles
- premium CTA hover/transition behaviour

Do not over-animate.

---

## Specific implementation notes to follow

### Typography
- `DM_Serif_Display` only for the intent-screen headline
- section header stronger than Q-1
- question labels upgraded from generic medium body styling
- help text kept subtle and readable

### Question numbering
Add `Q{n}` numbering per visible question within the active section.

### Selected pill state
Use a strong solid selected treatment, not a weak translucent tint.

### CTA treatment
- Begin CTA: premium launch styling
- final “Unlock my analysis” CTA: same family of premium styling
- regular Next button: improved but not as strong as the final CTA

### Sidebar active state
Use HealthIQ green-tinted active state, not generic grey/neutral emphasis.

---

## Out of scope

- backend/schema changes
- questionnaire logic redesign
- broader frontend design-system overhaul
- global typography system work
- global colour-system overhaul
- results-page redesign
- any non-questionnaire feature work

Do not widen scope.

---

## Acceptance criteria

### Q-1 behaviour must still pass
All Q-1 behavioural acceptance criteria must remain true.

### Additional visual acceptance criteria
13. Intent-screen headline uses `DM_Serif_Display`.
14. Intent-screen root uses `bg-background`, avoiding dark/light collision.
15. Intent-screen headline remains readable in dark mode.
16. Section estimates and total-time line use green/monospace diagnostic styling.
17. Selected pill tiles use a strong, unambiguous selected state.
18. Slider value display is visually upgraded and prominent.
19. Question cards show sequential `Q{n}` identifiers.
20. Active desktop sidebar section uses a visible HealthIQ-specific active treatment.
21. Begin CTA has visibly stronger launch styling.
22. Final “Unlock my analysis” CTA has matching premium launch styling.
23. Upload page renders `<QuestionnaireForm />` directly, without the outer Card wrapper.
24. Section content animates in on section advance.

---

## Testing discipline

Do not run the full repository suite.

Run only targeted checks relevant to:
- questionnaire behaviour regression
- visual implementation sanity
- conditional logic preservation
- payload parity
- autofill behaviour
- type safety

Before running tests, state:
- what you will run
- why
- what broader suites you are excluding

---

## Reporting requirements

When finished, report back in these sections:

### 1. Branch
- confirm branch name

### 2. Preflight restatement
- objective
- files touched
- behavioural surfaces intentionally preserved

### 3. Visual redesign implementation
- intent-screen treatment
- typography choices
- sidebar treatment
- question-card treatment
- input/pill/slider treatment
- CTA treatment
- upload-page framing change

### 4. Behaviour preservation
- how Q-1 behaviour was kept intact
- how payload parity was preserved
- how `conditionalDisplay` was preserved
- how `?autofill=true` was preserved

### 5. Tests run
- exact tests/checks
- results

### 6. Known limits intentionally deferred
- anything intentionally left out of scope

### 7. Uncommitted / not merged
- confirm work is not merged to `main`

---

## STOP conditions

STOP and report if:

1. removing the outer upload-page wrapper causes wider layout breakage
2. `DM_Serif_Display` import causes build issues
3. intended premium CTA styling causes Tailwind/build issues
4. any Q-1 behavioural acceptance criterion regresses
5. scope starts drifting into global frontend redesign work

If blocked, report:
- exact blocker
- affected file/surface
- smallest safe remediation path