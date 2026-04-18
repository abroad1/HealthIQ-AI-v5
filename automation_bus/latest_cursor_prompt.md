---
work_id: FE-R8B
branch: feature/fe-r8b-results-journey-coherence
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# FE-R8B — Results journey coherence and narrative composition refinement

## Objective

Improve the results journey so it reads as one coherent, premium, body-wide investigation rather than several deterministic engines stacked vertically.

This is a bounded frontend composition and narrative-shaping sprint.

It exists because:
- FE-R8 and FE-R8A successfully surfaced the intended governed assets
- the page is now richer
- but the live experience still feels mechanically stitched, repetitive, and insufficiently world-class

This sprint must improve coherence, hierarchy, and narrative flow without widening into a rebuild.

It must not introduce LLM/Gemini dependency.
It must not redesign backend intelligence.
It must not reopen taxonomy or IDL strategy.

---

## Strategic context already settled

The following are already decided and are not open for reinterpretation in this sprint:

- The results page is a guided reasoning journey, not a better lab report.
- Deterministic assets remain the narrative spine.
- BE-IDL-1, FE-R8, and FE-R8A are complete and approved.
- The current “wow” gap is now primarily a composition/narrative-shaping problem, not a missing-data-flow problem.
- The page already has substantial backend intelligence on screen:
  - `clinician_report_v1`
  - `balanced_systems_v1`
  - `interpretation_display_layer_v1`
  - Layer C feature cards
  - clusters/system groups
  - biomarker evidence
- The current live problem is that these appear as several adjacent systems rather than one guided investigation.

Your job is to improve how the existing assets are composed, introduced, and connected.

---

## Required outcome

Deliver a bounded refinement that:

1. gives the page a clearer above-the-fold investigation spine
2. reduces the sense that multiple engines are speaking independently
3. improves narrative continuity between:
   - Body overview
   - What’s working well
   - Primary finding
   - Why this lead won
   - Patterns across your body
4. reduces obvious repetition and mechanically stitched phrasing where the frontend can do so safely through composition/presentation choices
5. resolves or softens conflicting “center of gravity” cues so the user feels one coherent body-wide story
6. improves access to deeper narrative where high-value content already exists

---

## Primary problems this sprint is intended to address

The live page now has more real content, but still feels off because of:

- static, generic onboarding/hero framing
- a body overview lead that reads as mechanically concatenated
- repeated tokens and duplicated concepts across adjacent sections
- competing “primary” framings:
  - lead hypothesis / homocysteine-B12 story
  - IDL pattern story
  - “primary driver system group” language
- strong deterministic assets presented as separate cards rather than one investigation path
- deeper narrative content hidden behind progressive disclosure that is too easy to ignore

This sprint should address those issues through composition and frontend shaping, not new backend logic.

---

## Authority and preflight checks

Before modifying files, verify and cite:

1. the current results-page structure and actual section order
2. the components currently responsible for:
   - Body overview
   - What’s working well
   - Primary finding and why
   - Why this lead won
   - Patterns across your body
   - Clinical interpretation detail / trust strip / advanced analysis entry
3. which visible phrases are:
   - backend-authored strings that should not be rewritten in frontend
   - frontend-authored intro/bridge/headline copy that may be refined
4. where the “primary driver system group” line is currently surfaced
5. whether a minimal composition layer can unify the visible story without altering backend contracts

If repo reality shows that the main issue is backend-authored text that cannot be improved safely in frontend, stop and report that clearly rather than widening scope silently.

---

## In scope

### 1. Improve above-the-fold investigation spine
Create a stronger opening flow so the user quickly understands:
- what the main body-wide story is
- what appears stable
- what the main line of inquiry is
- where they should look next

This may include:
- a better introductory bridge between Body overview and the next sections
- a short deterministic “what we’re investigating” framing block composed from already-visible assets
- improved ordering or emphasis of existing sub-elements within the opening journey

Do not invent new clinical claims.

### 2. Reduce stitched / repetitive experience
Reduce the sense that adjacent sections repeat the same idea mechanically.

Possible mechanisms:
- tighter section intros
- better transitions between sections
- de-emphasis or removal of redundant bridge copy
- presentational consolidation where multiple nearby blocks say nearly the same thing

Do not rewrite backend clinical strings unless the source is clearly frontend-authored presentation text.

### 3. Resolve “multiple center of gravity” problem
Where the user currently sees competing interpretations of what the page is “about,” improve composition so one main thread leads and secondary frames read as supporting context.

This may include:
- reframing or repositioning the “primary driver system group” line
- reducing the prominence of secondary competing labels
- making it clearer how the IDL pattern relates to the lead finding rather than appearing as a separate story

### 4. Improve access to deeper narrative
If deeper narrative content already exists and is valuable, improve the user’s chance of encountering it.

This may include a bounded progressive-disclosure refinement such as:
- default-opening the most relevant narrative surface when content exists
- clearer invitation into advanced narrative
- a stronger “deep dive” affordance

Do not redesign Advanced analysis wholesale.

### 5. Preserve governed data usage
All improvements must continue to rely on existing governed deterministic assets.
No frontend invention of clinical meaning.

### 6. Add bounded tests / validation
Add tests or UI validation where appropriate to protect:
- new composition logic
- conditional rendering
- section order / visibility assumptions where changed
- absence of regressions to FE-R8/FE-R8A behaviour

---

## Out of scope

The following are explicitly out of scope:

- backend analytical changes
- IDL content or classification changes
- new backend DTO fields
- Gemini / LLM narrative enablement
- full redesign of biomarker evidence
- full redesign of Advanced analysis
- rewriting backend-generated clinical reasoning text at source
- new interpretation entities
- broader launch/trust/compliance work

---

## Implementation rules

### Rule 1 — composition over reinvention
Use better composition of existing assets before inventing new UI complexity.

### Rule 2 — one story, not many panels
The page should feel like one investigation path.
Avoid adding more disconnected cards that increase fragmentation.

### Rule 3 — frontend must not alter clinical meaning
Do not paraphrase or soften backend-authored reasoning in ways that change its meaning.

### Rule 4 — reduce duplication, do not hide truth
If two blocks repeat the same concept, prefer cleaner composition.
Do not solve repetition by removing clinically important context without justification.

### Rule 5 — bounded progressive disclosure only
Any changes to default-open/default-closed behaviour must remain narrow and justified by user comprehension.

### Rule 6 — preserve existing governed authority
No taxonomy, naming, or interpretation logic may move into frontend composition code.

---

## Expected implementation shape

The expected shape is:

1. inspect the live page and current section/component structure
2. identify the smallest set of composition changes with highest coherence value
3. implement bounded layout/heading/bridge/progressive-disclosure refinements
4. preserve existing governed content sources
5. validate in browser against the same live analysis result

This should remain a coherence sprint, not a broad redesign.

---

## STOP conditions

STOP immediately and report if any of the following are true:

1. the main quality problem is clearly backend-authored copy that cannot be improved safely in frontend
2. meaningful coherence improvement would require backend contract changes
3. fixing the “multiple center of gravity” issue requires changing deterministic reasoning outputs rather than frontend composition
4. the proposed solution starts to become a broad redesign of the results page
5. the sprint would need to introduce new generated narrative rather than improving composition of existing assets
6. repo reality contradicts the assumption that this is a bounded frontend coherence sprint

If blocked, report the exact blocker, affected files, and the smallest safe next sprint.

---

## Success criteria

This sprint is successful only if:

1. the page feels more like one guided investigation and less like stacked engines
2. the opening journey is clearer and more compelling above the fold
3. stable systems, lead finding, and IDL pattern feel connected rather than competing
4. obvious repetition/mechanical stitching is reduced
5. deeper narrative is easier to encounter where valuable content already exists
6. no new backend or Gemini dependency is introduced
7. FE-R8 and FE-R8A governed data-flow behaviour remains intact

---

## Deliverables

At finish, the sprint should leave behind:

- bounded frontend composition refinements
- clearer investigation-spine presentation
- any justified progressive-disclosure adjustment
- tests/validation for the changed behaviours
- browser-verified notes on how the user experience improved

---

## Evidence requirements

You must show, with file citations and browser evidence:

- what specific sections/components were changed
- what composition problem each change was intended to solve
- how the live page now reads more coherently
- that no governed backend authority was bypassed
- that the page still renders from the same deterministic assets

Do not claim the page is “world class” unless the browser-visible result materially supports that claim.

---

## After this sprint

After FE-R8B, report clearly which of these is true:

1. **The deterministic journey is now strong enough without Gemini**
2. **The deterministic journey is much stronger, but selective narrative-polish work may still be justified later**
3. **The remaining problem is now clearly upstream/backend-authored content quality, not frontend composition**

That report will determine whether anything like R-9 is actually needed.
```
