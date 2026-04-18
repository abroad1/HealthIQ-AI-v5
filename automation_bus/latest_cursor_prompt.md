---
work_id: FE-R8C
branch: feature/fe-r8c-results-dedup-and-example-binding
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# FE-R8C — Results journey de-duplication and example binding

## Objective

Refine the results journey so it stops repeating the same lead story in multiple adjacent shells and makes the explanatory sections track the actual live investigation thread on the page.

This is a bounded frontend composition/editing sprint.

It exists because:
- FE-R8A restored the missing payload fields
- FE-R8B improved the page structure and coherence
- but the live page still repeats the same lead idea too many times and still uses generic educational examples that do not track the active story

This sprint must improve narrative economy and example alignment without widening into a redesign or backend rewrite.

It must not introduce Gemini/LLM dependency.
It must not change backend contracts.
It must not reopen IDL strategy or naming.

---

## Strategic context already settled

The following are already decided and are not open for reinterpretation in this sprint:

- The page is a guided reasoning journey, not a better lab report.
- Deterministic assets remain the narrative spine.
- BE-IDL-1, FE-R8, FE-R8A, and FE-R8B are complete and approved.
- The current live page now surfaces the intended core assets, including:
  - `clinician_report_v1`
  - `balanced_systems_v1`
  - `interpretation_display_layer_v1`
  - Layer C feature cards
  - clusters/system groups
  - biomarker evidence
  - Advanced/Narrative when present
- The main remaining gap is now repetition, generic example binding, and editorial composition — not missing core backend intelligence.

Your job is to tighten the page so it feels more curated and less mechanically repetitive.

---

## Required outcome

Deliver a bounded refinement that:

1. reduces repetition of the same lead story across the upper page
2. makes the investigation spine orient the user without duplicating nearby sections
3. makes “How to understand your results” use examples grounded in the actual live page context rather than a fixed generic cardiovascular script
4. preserves the governed backend meaning while improving editorial flow
5. keeps the page feeling like one investigation rather than multiple repeated summaries

---

## Primary problems this sprint is intended to address

The live page is materially improved, but still feels off because of:

- the lead thread being told multiple times across:
  - investigation spine
  - body overview
  - primary finding
- IDL being previewed in the spine and then repeated again immediately in full
- “How to understand your results” using stock examples that do not track the active lead/IDL context
- stacked cards still reading like adjacent outputs rather than a curated single narrative

This sprint should solve those issues through bounded frontend composition and copy binding only.

---

## Authority and preflight checks

Before modifying files, verify and cite:

1. the current components responsible for:
   - `ResultsInvestigationSpine`
   - `ResultsBodyOverview`
   - `PrimaryFindingAndWhy`
   - `SystemUnderstandingSection`
   - `InterpretationPatternsSection`
2. which visible strings in those components are:
   - backend-authored and must remain verbatim
   - frontend-authored and may be tightened or rebound
3. whether the current duplication comes from:
   - frontend-authored wrappers/labels
   - repeated surfacing of the same backend field
   - or both
4. what live deterministic values are already available in the page/component tree that can be safely used for example binding, such as:
   - first visible IDL retail label
   - primary driver system group name
   - lead topic / lead concern label
   - visible balanced-system names

If the duplication problem turns out to be mainly backend-authored copy that cannot be improved safely in frontend, stop and report that clearly.

---

## In scope

### 1. Investigation spine de-duplication
Refine the upper-page flow so the spine or body-overview layer does not restate the same lead thread in near-identical form.

This may include:
- shortening the investigation spine
- making the spine more of a directional bridge and less of a second summary card
- reducing or removing duplicated phrases where the next section already says the same thing better

Do not remove clinically meaningful content without justification.

### 2. Body overview / spine editorial economy
Tighten the relationship between:
- spine
- body overview
- primary finding

The user should feel:
- “I understand the thread”
not
- “I just read the same thing again”

### 3. Example binding in “How to understand your results”
Replace fixed generic examples with deterministic examples derived from already-visible page context when available.

The section should use the actual live investigation thread more intelligently.

Possible sources include:
- first visible IDL `retail_display_label`
- primary driver system group name
- lead pattern / lead topic already on screen

This must be deterministic substitution from existing loaded props/data.
Do not create new inference logic.
Do not invent new clinical claims.

### 4. Section relationship tightening
Where two nearby sections are conceptually valid but too close in substance, improve the transitions and emphasis so they feel complementary instead of repetitive.

### 5. Bounded tests / validation
Add tests or validation as appropriate for:
- example binding behaviour
- de-duplication logic / conditional display choices
- protection against regression into fixed generic examples

---

## Out of scope

The following are explicitly out of scope:

- backend analytical changes
- backend DTO changes
- IDL content/classification changes
- Gemini / LLM narrative enablement
- full redesign of the results page
- broad rewrite of backend-authored clinical strings
- changes to biomarker evidence architecture
- new interpretation entities
- launch/trust/compliance work

---

## Implementation rules

### Rule 1 — no change to clinical meaning
Frontend may improve wrappers, transitions, and example selection, but must not alter the meaning of backend-authored reasoning.

### Rule 2 — use existing deterministic context only
Any smarter example binding must come from already-loaded deterministic fields already present on the page.

### Rule 3 — reduce repetition, do not strip substance
The goal is editorial economy, not content loss.

### Rule 4 — one thread, not one more card
Prefer strengthening the single investigation thread over adding new presentational blocks.

### Rule 5 — no hidden frontend intelligence
Do not let example binding become implicit interpretation logic.
It must remain simple, visible, and deterministic.

---

## Expected implementation shape

The expected shape is:

1. inspect the upper-page components and repeated strings
2. identify the smallest set of edits with the highest de-duplication value
3. bind educational/example copy to live deterministic context where safe
4. validate in browser against the same analysis result
5. confirm whether repetition is materially reduced

This should remain a bounded editorial/frontend refinement sprint.

---

## STOP conditions

STOP immediately and report if any of the following are true:

1. the repetition problem is mainly caused by backend-authored strings that cannot be safely improved in frontend
2. binding “How to understand” to live context would require new inference logic rather than deterministic substitution
3. meaningful improvement would require backend contract changes
4. the sprint starts to widen into a redesign of multiple sections
5. repo reality contradicts the assumption that this is a bounded frontend de-duplication sprint

If blocked, report the exact blocker, affected files, and the smallest safe next sprint.

---

## Success criteria

This sprint is successful only if:

1. the upper-page journey repeats the lead story less obviously
2. the investigation spine orients rather than duplicates
3. “How to understand your results” reflects the actual live story more credibly
4. the page feels more edited and less mechanically stitched
5. no backend or Gemini dependency is introduced
6. FE-R8 / FE-R8A / FE-R8B data-flow and coherence gains remain intact

---

## Deliverables

At finish, the sprint should leave behind:

- bounded frontend de-duplication refinements
- deterministic example-binding improvement in the explanatory section
- tests/validation for changed behaviours
- browser-verified notes showing how repetition was reduced

---

## Evidence requirements

You must show, with file citations and browser evidence:

- what repeated content was reduced
- which deterministic fields now drive the example binding
- what changed in the upper-page reading experience
- that no governed backend authority was bypassed
- that the result is more coherent without becoming thinner or vaguer

Do not claim the issue is solved unless the browser-visible result materially supports that claim.

---

## After this sprint

After FE-R8C, report clearly which of these is true:

1. **The deterministic journey now feels strong enough without Gemini**
2. **The journey is substantially better, but a later optional polish sprint may still help**
3. **The remaining problem is now clearly upstream/backend-authored narrative quality, not frontend composition**