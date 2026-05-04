# Q-2 — Questionnaire Visual Redesign: Background & Design Specification

## Why Q-1 was not enough

Q-1 delivered correct UX architecture: section-by-section flow, intent screen, conditional logic, payload parity. It is functionally solid. Visually it is unacceptable because the prompt did not contain design direction — it said "use existing project tokens / visual language" which gave Cursor no basis to produce anything except shadcn defaults.

The hardening spec should have flagged this as insufficient. It did not. This document corrects that.

Q-2 is a visual redesign. The UX structure from Q-1 is kept entirely. The functional logic is kept entirely. Only the visual layer changes.

---

## What is visually broken right now

**1. The intent screen text is invisible in dark mode.**
The intent screen outer wrapper uses `bg-gray-50` (from the upload page). In dark mode, `text-foreground` resolves to near-white. Near-white text on a light-gray background = unreadable. This is a dark/light context collision.

**2. The form lives inside an outer Card on the upload page.**
`upload/page.tsx` wraps `<QuestionnaireForm />` inside a `<Card>` with a `<CardHeader>` that says "Health questionnaire." This creates a card-within-a-card layout and removes the form's ability to control its own framing. The outer Card must be stripped.

**3. Question cards are indistinguishable from each other.**
Every question renders as an identical flat rectangle. No visual hierarchy, no question numbering, no sense of flow within a section.

**4. Pill tile selected state is invisible.**
`bg-primary/10 text-primary` (a 10% opacity tint) does not communicate "selected" clearly. A user can easily mistake an unselected option for a selected one.

**5. No typographic personality.**
Everything uses default font weight and sizing. The intent screen headline has no presence. Nothing says HealthIQ — it looks like a generic form.

**6. The sidebar is invisible.**
`bg-muted/20` creates a near-transparent panel. It reads as a grey blur, not a navigation element.

**7. The CTA has no visual weight.**
"Begin" and "Unlock my analysis" use the same standard Button component as every other button. The most important moments in the flow are visually identical to cancel links.

---

## Design direction

HealthIQ is a precision diagnostic instrument. The questionnaire should feel like calibrating something important — not filling in an admin form.

**Tone:** Dark, controlled, intelligent. Think a premium clinical device display, not a wellness app.

**Not:** Soft gradients, pastel colours, rounded-everything, emoji-led, conversational/chatty.

**Yes:** High contrast, deliberate typography, purposeful use of the forest green accent, visible structure.

---

## Files in scope

| File | Change |
|---|---|
| `frontend/app/components/forms/QuestionnaireForm.tsx` | Visual redesign — full replacement of all styling, new font import, animation, structural improvements |
| `frontend/app/(app)/upload/page.tsx` | Remove outer `<Card>` / `<CardHeader>` / `<CardDescription>` wrapper around `<QuestionnaireForm />`. Render the component directly. |

No backend changes. No schema changes. No props interface changes. No analytics event changes.

---

## Typography

### Display font for intent screen headline
Load `DM_Serif_Display` via `next/font/google`. This is part of Next.js core — no `npm install` required.

```typescript
import { DM_Serif_Display } from 'next/font/google';
const dmSerif = DM_Serif_Display({ weight: '400', subsets: ['latin'], display: 'swap' });
```

Apply only to the intent screen `<h1>`. All other text uses the existing body font.

Intent screen h1 class: `text-4xl sm:text-5xl lg:text-6xl font-normal leading-tight tracking-tight`

Everything else: existing font stack.

### Question labels within sections
Change from `text-base font-medium` → `text-lg font-semibold text-foreground`

### Help text
Keep `text-sm text-muted-foreground`. Add `mt-1.5` for cleaner spacing.

### Section header in form view
Section label: `text-2xl font-semibold text-foreground`
Estimate: `text-sm font-mono text-primary` (green monospace)

---

## Intent screen

### Background
The intent screen must own its background. Use `bg-background` as the outer wrapper (NOT `bg-gray-50` from a parent). This resolves the dark/light collision.

Add a radial gradient overlay using an inline style for the ambient green glow:
```
style={{ background: 'radial-gradient(ellipse 70% 50% at 100% 0%, hsl(142 76% 36% / 0.07) 0%, transparent 65%)' }}
```
In dark mode this creates a subtle green breath in the top-right corner that reads as precision/health without being garish.

### Headline
```
<h1 className={`${dmSerif.className} text-4xl sm:text-5xl lg:text-6xl font-normal tracking-tight text-foreground`}>
  Let's calibrate<br />your analysis.
```
The line break is intentional — two short powerful lines, not one long one.

### Subtext
`text-lg text-muted-foreground max-w-xl leading-relaxed`

### Time/section count line
`text-sm font-mono text-primary` — the green monospace makes it feel like a diagnostic readout, not a disclaimer.

### Section cards
Replace `border-border/80 bg-card` with:
```
border border-border bg-card rounded-xl p-5 
hover:border-primary/40 hover:bg-primary/5 
transition-all duration-200 cursor-default
```
Add a left accent bar that becomes visible on hover:
```
relative overflow-hidden
before:absolute before:left-0 before:top-0 before:bottom-0 before:w-0.5 
before:bg-primary before:opacity-0 hover:before:opacity-100 
before:transition-opacity before:duration-200
```

Section icon: `text-3xl leading-none` (unchanged, already works)
Section label: `text-base font-semibold text-foreground`
Time estimate: `text-sm font-mono text-primary` (green, same as headline time line)

Add `animate-fade-up` with staggered `animation-delay` to each card (using inline style `animationDelay: \`${idx * 60}ms\``). The `animate-fade-up` keyframe already exists in `tailwind.config.ts`.

### Begin CTA
Replace the standard `Button` with:
```
h-14 px-10 text-base font-semibold rounded-xl
bg-primary text-primary-foreground 
shadow-[0_0_24px_hsl(142_76%_36%/0.35)]
hover:shadow-[0_0_32px_hsl(142_76%_36%/0.50)]
hover:bg-primary-glow
transition-all duration-300
```
The green glow (`shadow-[...]`) is the visual signal that this is the launch moment. Use `hsl(var(--primary) / 0.35)` syntax.

### "Not now" link
`text-sm text-muted-foreground/60 hover:text-muted-foreground underline-offset-4 hover:underline transition-colors`

---

## Section form

### Outer container
Replace `lg:bg-card` with `bg-background` so the form matches the page background rather than adding a card layer on top of it. The internal sidebar and question area provide the visual containment — the outer shell doesn't need to be a card itself.

Full class: `mx-auto flex min-h-screen max-w-6xl flex-col lg:flex-row`

Remove the `lg:border lg:rounded-2xl lg:shadow-sm` — these look fine in isolation but inside the upload page they create a card-within-a-card with a double border. The form's internal structure provides enough visual separation.

### Sidebar
Replace `bg-muted/20` with `bg-card border-r border-border`:
```
hidden w-[240px] shrink-0 flex-col bg-card border-r border-border lg:flex
```

HealthIQ label area:
```
border-b border-border px-5 py-5
```
HealthIQ text: `text-sm font-bold uppercase tracking-[0.2em] text-foreground` (more prominent than current)
"Calibration map" subtitle: `text-xs text-muted-foreground mt-0.5`

Active section item:
```
bg-primary/10 border border-primary/20 text-primary
```
(Replace `bg-background shadow-sm ring-1 ring-border` — the green tint is HealthIQ-specific, the current ring-border is generic.)

Done section item: `text-muted-foreground` with `text-primary` check icon (already correct, keep)

Pending section items: `text-muted-foreground/50` (slightly more muted than done)

Progress footer:
```
border-t border-border px-5 py-4
```
Text: `text-xs font-mono text-primary` — make it read as a diagnostic value, not a label.

### Section header bar
Add a thin `3px` border-top using the primary colour on the header div:
```
border-t-[3px] border-primary
```
This creates a visible "active marker" at the top of the content area.

Section estimate: change from `text-muted-foreground` → `text-sm font-mono text-primary`

### Question cards
Current: `border-border/80 shadow-sm`
Replace with: `border border-border bg-card shadow-none hover:border-border/80 hover:shadow-sm transition-all duration-200`

Add question numbering — a sequential counter above each question label within the section:
```
<span className="block text-xs font-mono text-primary/70 mb-2 uppercase tracking-wider">
  Q{questionIndex + 1}
</span>
```
where `questionIndex` is the 0-based index of the question within its section's visible questions array.

Question label: `text-lg font-semibold text-foreground leading-snug` (upgrade from `text-base font-medium`)

Add entrance animation on section transition: when `activeSectionIdx` changes, the question area should animate in. Wrap the question list `div` with `key={activeSectionIdx}` so React remounts it, and give it `className="animate-fade-up"`. The existing keyframe handles this.

### Pill tiles — CRITICAL FIX

**Unselected:**
```
border border-border bg-background text-foreground 
hover:border-primary/50 hover:bg-primary/5 hover:text-primary
transition-all duration-150
```

**Selected:**
```
border border-primary bg-primary text-primary-foreground 
shadow-sm
```
Solid fill, white (or dark) text. This is the most important change. The 10% tint selected state from Q-1 was not visually distinct enough. Solid primary fill makes selection unambiguous.

Remove the `ring-1 ring-primary/25` — the solid fill makes the ring redundant.

Keep the `<Check />` icon for selected pills — it adds further confirmation.

### Slider — visual upgrade
Remove the `rounded-xl border bg-muted/40 px-4 py-4` wrapper box.
Replace with a cleaner layout:
```
<div className="space-y-4">
  <div className="flex items-baseline gap-3">
    <span className="text-5xl font-bold tabular-nums text-primary leading-none">{sliderValue}</span>
    {/* if labels exist, show the matching label next to the number */}
    {question.labels?.[String(sliderValue)] && (
      <span className="text-sm text-muted-foreground">{question.labels[String(sliderValue)]}</span>
    )}
  </div>
  <Slider ... className="w-full" />
  <div className="flex justify-between text-xs font-mono text-muted-foreground">
    {/* min and max labels */}
  </div>
</div>
```
Big green number, no box. Shows the per-value label inline next to the number.

### "← Back" button
Keep `variant="outline"` — this is correctly subdued.

### "Next section" / "Unlock my analysis" button
**Next section:**
```
h-12 px-8 font-semibold
```
(Slightly larger than default, but not the glow treatment — that's reserved for the final CTA.)

**"Unlock my analysis" (final section only):**
```
h-12 px-8 font-semibold
bg-primary text-primary-foreground
shadow-[0_0_20px_hsl(142_76%_36%/0.30)]
hover:shadow-[0_0_28px_hsl(142_76%_36%/0.45)]
hover:bg-primary-glow
transition-all duration-300
```
Same green glow as the Begin CTA. The visual language of "this is the launch moment" should be consistent.

---

## Upload page change

Remove the outer Card wrapper. The relevant section in `upload/page.tsx` currently reads:

```tsx
<Card>
  <CardHeader>
    <CardTitle className="flex items-center gap-2">
      <FileText className="h-5 w-5" />
      Health questionnaire
    </CardTitle>
    <CardDescription>
      Context for interpretation...
    </CardDescription>
  </CardHeader>
  <CardContent>
    <QuestionnaireForm
      onSubmit={handleQuestionnaireFromUpload}
      isLoading={isAnalyzing}
    />
  </CardContent>
</Card>
```

Replace with:

```tsx
<QuestionnaireForm
  onSubmit={handleQuestionnaireFromUpload}
  isLoading={isAnalyzing}
/>
```

The green "markers confirmed" Card directly above it (lines 460-472) should be kept exactly as-is — it's a confirmation banner, not a form wrapper.

The `CardHeader`, `CardTitle`, `CardDescription`, `CardContent` imports on the upload page can be removed if no longer used elsewhere on that page.

---

## Mobile section strip

The current mobile horizontal scroll strip uses plain outlined pills. Apply the same active/done treatment as the sidebar:

Active: `border-primary bg-primary/10 text-primary font-medium`
Done: `border-border bg-muted/50 text-muted-foreground`
Pending: `border-border/50 bg-transparent text-muted-foreground/60`

---

## Animations summary

Use only the keyframes that already exist in `tailwind.config.ts`:

| Moment | Class |
|---|---|
| Intent screen entrance | `animate-fade-up` on the header block |
| Section cards on intent screen | `animate-fade-up` with staggered `animation-delay` (0ms, 60ms, 120ms…) |
| Section content on advance | `animate-fade-up` via `key={activeSectionIdx}` remount |
| Pill tile selection | `transition-all duration-150` (CSS only, no keyframe needed) |
| CTA glow | `transition-all duration-300` on box-shadow |

No new keyframes needed.

---

## What does NOT change

- Props interface (`onSubmit`, `onCancel`, `initialData`, `isLoading`)
- Submission payload shape (flat `Record<string, unknown>`)
- `conditionalDisplay` / `dependsOn` logic
- Section order, section names, section estimates
- `?autofill=true` dev shortcut
- `fetchQuestionnaireSchema()` loading path
- Loading and error state rendering
- Validation logic
- All 12 acceptance criteria from Q-1 remain valid and must still pass

---

## Acceptance criteria (visual, in addition to all Q-1 AC)

13. The intent screen headline uses DM Serif Display and renders at `text-5xl` minimum on `sm:` breakpoint.
14. The intent screen uses `bg-background` as its root background — no inherited `bg-gray-50` collision.
15. In dark mode: the intent screen headline text is clearly readable (high contrast against `bg-background`).
16. Section card estimates and the time-line on the intent screen render in `text-primary font-mono`.
17. Selected pill tiles use solid `bg-primary text-primary-foreground` fill — not a tint.
18. Slider value displays at `text-5xl font-bold text-primary` with the per-value label inline.
19. Question cards show a sequential `Q{n}` identifier in `text-xs font-mono text-primary/70` above each question.
20. Active sidebar section uses `bg-primary/10 border-primary/20 text-primary` (green tint, not grey ring).
21. "Begin" CTA renders with green glow shadow.
22. "Unlock my analysis" CTA renders with green glow shadow (matching Begin).
23. The upload page renders `<QuestionnaireForm />` directly — no outer Card wrapper.
24. Section content animates in on section advance via `animate-fade-up`.

---

## STOP conditions

STOP and report if:

1. Removing the outer Card wrapper on the upload page causes any layout breakage outside the questionnaire step.
2. `next/font/google` for `DM_Serif_Display` causes any build error (report font name and error — do not substitute a random alternative).
3. The `shadow-[...]` arbitrary Tailwind values cause a build error (report and use a standard shadow utility instead).
4. Any of the Q-1 acceptance criteria (1–12) regress.
5. Scope drifts into any surface outside `QuestionnaireForm.tsx` and `upload/page.tsx`.
