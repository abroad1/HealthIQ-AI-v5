---
work_id: FE-R4-RESULTS-JOURNEY-V6
branch: feature/results-journey-v6-r4-biomarker-expansion-depth
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# Sprint: R-4 — Biomarker Expansion Depth

## Objective

Implement the biomarker expansion model from the V6 Results Journey so that the marker-level experience becomes a second-order differentiator rather than a conventional blood-report appendix.

This sprint must make each expanded biomarker card answer three questions:

1. what this result means now
2. why this marker matters
3. how it connects to the wider body story

The goal is not to redesign the whole biomarker table.
The goal is to make biomarker expansion feel materially richer, more relevant, and more connected to the user’s broader interpretation.

---

## Scope

### In scope

- Expansion experience for biomarker cards in the main results page
- Three-layer biomarker expansion model
- Stronger surfacing of already-available educational / contribution assets
- Rendering-layer derivation of pattern relevance using existing frontend data
- Safe fallback behaviour when deeper layers are absent
- Wiring only to **currently available frontend DTO/store data**

### Primary allowed assets

Use only assets already available on the frontend results path, specifically:

- `biomarkers[]`
- `biomarker_educational_explainer`
- `contribution_context`
- value / unit / reference range / score / interpretation fields already exposed in `analysis.ts`
- `clusters[]`
- the already-identified lead interpretation context visible on the page (Section 3 output / associated frontend-available source data)

### Out of scope

- New backend logic
- New DTO fields
- New biomarker science generation
- New system/pattern taxonomy contract
- Pattern layer / phenotype display work
- Gemini / LLM narrative generation
- Changes to analysis pipeline
- Reworking the entire biomarker list UI beyond the expansion experience

---

## Key principles (must be followed)

1. **Point of parity + point of differentiation**
   - users must still see familiar biomarker facts clearly
   - but expansion must go beyond conventional blood-report UX

2. **Expansion must be relevant, not generic**
   - do not dump educational text without tying it back to the user’s broader interpretation

3. **No fabricated depth**
   - if richer content is absent, keep the card simpler
   - do not invent “why this matters” prose

4. **Use existing assets more effectively**
   - this sprint is about surfacing and structuring, not generating new knowledge

5. **Pattern relevance must remain a rendering-layer derivation**
   - do not introduce a new backend contract field in this sprint

---

## Confirmed data authority for this sprint

This sprint must be built only from data already available on the frontend results path.

### Primary section assets

- `biomarkers[]`
- `biomarker_educational_explainer`
- `contribution_context`
- biomarker value / reference range / score / interpretation data already present in frontend DTOs
- `clusters[]`
- current lead interpretation context already surfaced in the results experience

### Explicit non-authority for this sprint

Do not use or depend on:

- new backend-derived “pattern relevance” field
- raw Knowledge Bus package data
- raw signal-library explanation content
- new DTO additions
- Gemini-generated explanation text

If richer biomarker explanatory content requires new compiler or DTO work, that is a later sprint.

---

## Target UX structure

## Biomarker expansion rule

Every biomarker expansion must be structured as:

### Layer 1 — What this result means now

Must display:
- current result
- reference range
- status / interpretation
- a short interpretation tied to this user’s actual result

Rules:
- this is the minimum layer and must always render
- must remain clean and fast to scan
- do not bury the biomarker’s actual value beneath explanation

---

### Layer 2 — Why this marker matters

Must display:
- `biomarker_educational_explainer` where present

Rules:
- this should explain the marker’s biological or clinical significance
- it must feel educational, not generic filler
- if absent, omit cleanly
- do not create substitute prose

---

### Layer 3 — How it connects to your wider pattern

Must display:
- `contribution_context`
- plus a rendering-layer “pattern relevance” line derived from:
  - `contribution_context`
  - the biomarker’s cluster membership
  - the primary pattern / lead interpretation already visible in the current results flow

Rules:
- this is not a new backend field
- it must be derived only from existing frontend data
- it should help the user understand:
  - whether this marker contributed to the main pattern
  - or whether it sits in another meaningful group

Example shape (not hardcoded):
> “This marker contributed to the [pattern/system] finding and helps explain why that pattern was highlighted.”

If the derivation is weak or ambiguous:
- show `contribution_context` only
- do not force a synthetic “pattern relevance” sentence

---

## Pattern relevance derivation rule

Pattern relevance must remain a **frontend rendering-layer derivation** only.

### Allowed derivation inputs

- `contribution_context`
- cluster membership from `clusters[]`
- the lead interpretation context already surfaced in the results page

### Not allowed

- new backend fields
- guessed relationships not supported by surfaced data
- hidden signal-level reasoning not available on the frontend

### Behaviour rule

- if a credible relevance link to the current lead interpretation can be made using existing surfaced data, render it
- if not, omit that derived sentence and fall back to contribution-context only

---

## Fallback model (mandatory)

### Case 1 — Full biomarker support present
Show:
- Layer 1
- Layer 2
- Layer 3

### Case 2 — Educational explainer absent, contribution context present
Show:
- Layer 1
- Layer 3

### Case 3 — Educational explainer present, contribution context absent
Show:
- Layer 1
- Layer 2

### Case 4 — Only base biomarker data present
Show:
- Layer 1 only

Do not render empty shells for missing layers.

---

## Component / architecture rules

Before creating new components:
- identify whether existing biomarker card / dial / expansion components can be reused or adapted

Likely existing candidates:
- biomarker rendering components currently used in the results page
- existing educational explainer UI
- existing contribution-context rendering

Only create new components if:
- no suitable component exists
- or reuse would create excessive coupling or confusion

Avoid duplicating biomarker rendering logic across components.

---

## Files likely impacted

- `frontend/app/(app)/results/page.tsx`
- biomarker-related results components
- biomarker card / dial expansion components
- small frontend helper/lib for pattern relevance derivation only if necessary
- `frontend/app/types/analysis.ts` only if existing frontend type usage requires local tightening without backend change

Do not create backend dependencies in this sprint.

---

## Content shaping rules

1. Do not allow educational content to appear without relevance framing when contribution context exists
2. Do not repeat the same explanatory sentence across multiple biomarkers
3. Keep expansion readable:
   - one result layer
   - one educational layer
   - one connection layer
4. If deeper content is absent:
   - the card must still feel clean and complete
   - not broken or incomplete
5. Biomarker expansion must remain evidence-led, not narrative-led

---

## Acceptance criteria

1. Expanded biomarker cards follow the three-layer model where data supports it

2. Every biomarker expansion shows at minimum:
   - value
   - range
   - status / interpretation

3. Educational explainer appears only when real data exists

4. Contribution context is clearly surfaced where present

5. Pattern relevance is derived only from existing frontend data and omitted when not credible

6. No fabricated explanation appears where deeper data is absent

7. No new backend or DTO dependency is introduced

8. No references to:
   - phenotype
   - internal IDs
   - raw signal names
   - unsurfaced KB package content

---

## Test instructions

- Run full analysis flow via `/upload → /results`
- Test with:
  - biomarker having educational explainer + contribution context
  - biomarker having educational explainer only
  - biomarker having contribution context only
  - biomarker with only basic data

Validate:
- all three layers render correctly when available
- fallback behaviour is clean
- no empty expansion sections
- no repeated generic text
- pattern relevance only appears when supportable
- base biomarker usability remains strong

Confirm no regression in:
- results page loading
- biomarker list rendering
- expand/collapse behaviour
- Section 1–4 content already implemented
- advanced tabs / navigation

---

## Completion criteria

- Code compiles cleanly
- No console errors
- Manual UX validation passes
- Biomarker expansion feels materially richer than the previous version
- No fabricated “deep explanation” where supporting data is absent
- Ready for gate validation via kernel

---

## Notes

This sprint is important because biomarkers are the point of parity with conventional blood reports.

Do not make them secondary or weak.
Do not turn them into generic explainer cards.

The goal is:

**users should feel that HealthIQ both respects the familiar biomarker layer and makes it much more meaningful than a normal blood report.**