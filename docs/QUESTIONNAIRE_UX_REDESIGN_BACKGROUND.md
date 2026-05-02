# Questionnaire UX Redesign — Background & Coding Specification

## Background

The current `QuestionnaireForm.tsx` is a functional but poor-experience form. It renders all 56 questions across all 7 sections simultaneously in a single scrollable card, uses a progress bar that has no semantic connection to the section structure, and relies on dropdowns for categorical choices that would work far better as tap targets. The net effect is a wall-of-text form that signals tedium rather than purpose.

There is also a rendering bug: the component uses `getQuestionsBySection()` to render all sections at once, but validates using `getCurrentQuestions()` which only examines 5 questions at a time. The step counter and the visible content are disconnected — this is never surfaced to the user but produces inconsistent required-field enforcement.

The questionnaire is the first analytical act the user performs on the platform. It should feel like calibrating a precision instrument, not filling in an admin form.

A reference design was reviewed at `https://flow-quest-joy.lovable.app/`. That design demonstrates several strong UX patterns worth adopting. This document specifies what to take, what to improve on, and what is specific to HealthIQ.

---

## Design Direction

**Tone:** Precision diagnostic, not wellness check-in. The user is unlocking a personalised metabolic analysis — every question has a reason. The UI should communicate that.

**Core UX pattern:** Section-by-section flow. One section is active at a time. Within a section, questions are shown as individual focused cards rather than a collapsed list. A sidebar tracks section-level progress (not individual question progress).

**Key framing:** The questionnaire opens on an intent screen — not the first question. The intent screen shows the section map (names + time estimates + what each section contributes to the analysis) and a single "Begin" CTA. This gives the user a mental model before they start and removes the anxiety of not knowing how long this will take.

---

## Files to Change

| File | Change type |
|---|---|
| `frontend/app/components/forms/QuestionnaireForm.tsx` | Full redesign — same props interface, new render logic |

No backend changes. No SSOT changes. No schema changes. The component receives the same schema from `/api/questionnaire/schema` and calls the same `onSubmit` callback.

---

## Props Interface — Unchanged

```typescript
interface QuestionnaireFormProps {
  onSubmit: (responses: Record<string, unknown>) => void;
  onCancel?: () => void;
  initialData?: Record<string, unknown>;
  isLoading?: boolean;
}
```

This must not change. The upload page (`app/(app)/upload/page.tsx`) passes these props and must not need modification.

---

## Section Structure

The schema returns 7 sections in this order. Use these display names and estimates:

| Schema key | Display name | Icon | Estimate |
|---|---|---|---|
| `demographics` | About you | 👤 | ~2 min |
| `medical_history` | Health history | 🏥 | ~3 min |
| `symptoms` | How you feel | 💬 | ~1 min |
| `lifestyle` | Daily habits | 🌿 | ~3 min |
| `physical_assessment` | Physical ability | 💪 | ~2 min |
| `cognitive_assessment` | Mental sharpness | 🧠 | ~1 min |
| `family_history` | Family story | 🧬 | ~1 min |

Total visible time estimate on intent screen: ~13 minutes.

---

## Screen Flow

### Screen 0 — Intent screen
Shown before any questions. Contains:
- Headline: "Let's calibrate your analysis."
- Subtext: "These questions let us interpret your results as you — not as population averages. Answer honestly; precision improves your output."
- Section map: grid of 7 cards, each showing icon, display name, and time estimate
- Single CTA button: "Begin →"
- `onCancel` triggered by a low-prominence "Not now" link below the CTA

### Screen 1–7 — One section at a time
Layout: two-column on desktop (sidebar left, questions right). Single column on mobile.

**Left sidebar (desktop only):**
- HealthIQ wordmark or logo mark at top
- Section list: all 7 sections listed vertically
- Active section highlighted
- Completed sections shown with a checkmark
- Remaining sections shown as upcoming (dimmed)
- Progress fraction at bottom: "3 of 7 complete"

**Question area (right / full width on mobile):**
- Section header: icon + display name + time estimate
- Each question rendered as its own card with clear vertical spacing
- Question text as the primary label (medium weight, legible size)
- Optional `helpText` rendered below question text in a smaller muted style
- Input appropriate to question type (see Input Patterns below)
- No red asterisks — required fields get a subtle "(required)" suffix in muted text, or nothing at all if the section is known to be mandatory
- Validation errors shown inline below the field, not at the top of the page

**Navigation:**
- "← Back" (previous section or back to intent screen if on section 1)
- "Next section →" (advances to next section, validates current section first)
- On final section: "Unlock my analysis →" instead of "Next section →"

---

## Input Patterns

Replace dropdowns with pill/tile selectors wherever the option count is ≤ 6:

| Question type | Render as |
|---|---|
| `dropdown` with ≤ 6 options | Pill button grid (multi-select if `allowMultiple`) |
| `dropdown` with > 6 options | Searchable select (keep current Radix Select) |
| `checkbox` | Pill button grid, multi-select |
| `slider` | Keep existing Radix Slider, but show current value prominently |
| `group` (height, weight, body composition) | Inline paired inputs side by side |
| `text`, `email`, `phone`, `date`, `number` | Keep existing Input, but underline-style not box |
| `textarea` | Keep existing Textarea |

Pill tile spec: rounded-full or rounded-lg border, neutral default state, teal/brand-coloured selected state with check icon, hover state with subtle background.

---

## Conditional Logic

Preserve the existing dependency logic from the schema. Questions with a `dependsOn` field that references another question's value should be hidden when the condition is not met — this already exists in the schema definition and the component needs to respect it (e.g. menstrual status only for females, testosterone symptoms only for males).

---

## Validation

Validate on section advance (not on every keystroke). If required fields in the current section are empty, show inline errors and prevent advance. Do not allow silent skip of required fields.

The existing `validateStep()` logic can be re-used but should be refactored to validate the current section's questions rather than an arbitrary 5-question slice.

---

## State

All response state remains local (`useState`). No changes to how data is passed to `onSubmit`. The `?autofill=true` dev shortcut must be preserved.

The component should track which section is active (`currentSection: number`, 0 = intent screen, 1–7 = sections) rather than the current arbitrary step count.

---

## Loading & Error States

Keep existing loading spinner and schema load error states. These are shown before the intent screen renders — no change to that behaviour.

---

## Design Tokens / Styling

Use Tailwind utility classes throughout (consistent with the rest of the frontend). Do not introduce new CSS files.

Colour palette: use existing design tokens. For the brand accent on selected pills and the "Unlock my analysis" CTA, use the existing green/teal primary button style (`bg-green-600 hover:bg-green-700` or the project's established primary colour).

Typography: use the project's existing font stack. Headline on the intent screen should be large (text-3xl or text-4xl), the section header within each section should be text-xl, question text should be text-base font-medium.

Background: a subtle warm-neutral gradient on the outer wrapper (consistent with the existing upload page card styling) is acceptable but not required — match the surrounding page context.

---

## Out of Scope

- No changes to the backend schema or API
- No changes to the upload page or any calling component
- No new state management libraries
- No changes to the analytics events (`wedge_questionnaire_submitted` must still fire)
- No PDF or export functionality
- No profile page integration

---

## Acceptance Criteria

1. Intent screen displays all 7 sections with names and time estimates before any question is shown.
2. Sections advance one at a time; the active section is visually highlighted in the sidebar.
3. Completed sections show a checkmark in the sidebar.
4. Categorical questions with ≤ 6 options render as pill tiles, not dropdowns.
5. Required field validation fires on section advance, not before.
6. `onSubmit` is called with the same `Record<string, unknown>` payload structure as the current component.
7. `onCancel` is reachable from the intent screen.
8. `?autofill=true` still populates responses correctly.
9. Conditional question display (dependsOn) works correctly.
10. No TypeScript errors introduced.
