---
work_id: FE-R6-RESULTS-JOURNEY-V6
branch: feature/results-journey-v6-r6-layer-c-insight-features
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# Sprint: R-6 — Layer C Insight Features

## Objective

Implement Section 7 of the V6 Results Journey:

**Key body-level insights**

This sprint must surface only the most robust, explainable, deterministic Layer C features so that the user sees a higher-order “body insight” layer after the core story is already understood.

The user should be able to understand:

1. what broader body-level insight has been identified
2. why it matters
3. how it relates to their wider interpretation
4. that these insights are selective and grounded, not gimmicky

This sprint must not depend on Gemini.

---

## Scope

### In scope

- Section 7: Key body-level insights
- Surfacing deterministic Layer C features already available on the frontend results path
- A strict render gate so only robust, populated features appear
- A small number of insight cards only
- Clean omission when no feature is sufficiently robust

### Primary allowed assets

Use only data already available on the frontend results path, specifically:

- `layer_c_features`
- any already-exposed frontend DTO/store fields containing deterministic Layer C feature outputs
- existing results context already visible on the page, only where needed for framing

### Out of scope

- New backend logic
- New DTO fields
- Gemini / LLM narrative generation
- Use of `insights[]` narrative prose as authority
- New clinical scoring logic
- Section 5 pattern layer work
- Section 8 action layer changes
- Any feature that is not already deterministically computed and surfaced

---

## Key principles (must be followed)

1. **Selective, not exhaustive**
   - Show only features that are robust enough to deserve space
   - Do not render thin or placeholder cards

2. **Deterministic authority only**
   - Use surfaced Layer C features
   - Do not depend on Gemini summary prose

3. **No gimmick layer**
   - This section must feel credible and grounded
   - Not futuristic for its own sake

4. **Optional by panel**
   - If no robust features exist, the section must omit cleanly

5. **Concise interpretation**
   - Each card must be short, high-signal, and readable
   - No essay-style feature descriptions

---

## Confirmed data authority for this sprint

This sprint must be built only from data already available on the frontend results path.

### Primary section assets

- `layer_c_features`
- existing frontend DTO/store fields already carrying deterministic feature values

### Explicit non-authority

Do not use or depend on:

- `insights[]` prose as the authoritative source
- Gemini-generated narrative
- unsurfaced InsightGraph internals
- new DTO additions
- new feature computation

If a feature is not already deterministically available on the frontend path, it is out of scope for this sprint.

---

## Target UX structure

### Section 7 — Key body-level insights

**Purpose:**
Show a small set of robust higher-order body insights once the user already understands the core interpretation.

**This section must answer:**
- what broader body-level feature was detected
- what that suggests in plain language
- why it is worth noticing

---

## Required section structure

### A. Section render gate

This section must render only if at least one feature passes the robustness gate.

If no qualifying feature exists:
- omit the entire section cleanly
- do not show placeholder headings or empty cards

---

### B. Insight cards

Each rendered feature must appear as a compact card containing:

1. **Feature name**
2. **Primary value / status**
3. **Short explanation**
4. **Why it matters** (short, single-block phrasing)

Cards must be concise and visually calm.

---

## Feature eligibility rule

Only surface features that are both:

1. **present**
2. **credible enough to show**

At minimum, the implementation must verify that each feature:
- exists in the surfaced frontend data
- has the minimum data needed to render meaningfully
- is not null / partial / placeholder

If robustness is ambiguous:
- omit the feature

---

## Feature scope for this sprint

Features in scope only if already surfaced and populated on the frontend path:

- metabolic age
- heart resilience score
- inflammation burden
- fatigue root causes
- detox capacity

Do not assume all five will be available.
Do not force all five to render.

---

## Required card behaviour

For each feature card:

### 1. Feature name
Must use a user-readable label.
Do not expose internal type/class names.

### 2. Primary value / status
Must present the actual surfaced deterministic output clearly.
Do not invent labels if none exist.

### 3. Short explanation
Must explain what the feature means in plain language using already available deterministic content or carefully shaped UI copy tied directly to the surfaced value.

### 4. Why it matters
Must be short and specific.
Do not drift into lifestyle advice.
Do not imply diagnosis.

---

## Render policy

### Case 1 — Multiple strong features available
Show only the strongest small set.
Maximum:
- 3 cards

Do not create a dashboard wall.

### Case 2 — One strong feature available
Show one card only.
That is acceptable.

### Case 3 — Feature data present but weak / partial
Do not render that feature.

### Case 4 — No robust features
Omit the section entirely.

---

## Component / architecture rules

Before creating new components:
- check whether an existing card/panel layout can be reused

If a new component is required:
- create one dedicated Section 7 component
- keep feature mapping logic isolated and simple
- use a small helper/lib only if needed for deterministic feature filtering or shaping

Do not:
- introduce new shared framework
- duplicate card logic across many files
- move business logic into styling components

---

## Files likely impacted

- `frontend/app/(app)/results/page.tsx`
- new Section 7 component (or equivalent)
- small helper/lib for feature gating/shaping only if necessary
- existing frontend results types only if already present and needing local narrowing without backend change

No backend files.

---

## Content shaping rules

1. Keep each card tight:
   - one title
   - one primary value/status
   - one short explanation block
   - one short “why it matters” block

2. Do not repeat:
   - Section 1 body overview language
   - Section 3 lead explanation
   - Section 4 trust language

3. Do not make these cards sound like:
   - marketing copy
   - wellness fluff
   - futuristic inventions

4. If a feature is thin:
   - omit it
   - do not stretch weak content into a card

---

## Acceptance criteria

1. Section 7 renders only when at least one robust deterministic feature is available

2. No more than 3 cards render

3. Each card contains:
   - readable feature name
   - surfaced value/status
   - short explanation
   - short why-it-matters framing

4. No feature card renders from weak / null / partial data

5. No section shell appears when no feature qualifies

6. No new backend or DTO dependency is introduced

7. No references to:
   - phenotype
   - internal IDs
   - raw class names
   - Gemini narrative
   - unsurfaced backend data

---

## Test instructions

- Run `/upload → /results`

Test with:
- case with multiple Layer C features available
- case with one available feature
- case with partial/weak feature coverage
- case with no qualifying feature

Validate:
- section appears only when appropriate
- max 3 cards
- no empty cards
- no repeated explanation text
- section feels credible and concise
- omission works cleanly when no features qualify

Confirm no regression in:
- Sections 1–5
- biomarker expansion
- navigation / loading
- advanced tabs

---

## Completion criteria

- Code compiles cleanly
- No console errors
- Manual UX validation passes
- Section 7 adds real value without gimmickry
- Weak feature output is omitted rather than surfaced
- Ready for gate validation via kernel

---

## Notes

This sprint is about **earned insight**, not novelty.

If done correctly, the user should feel:

**“That’s interesting — and it feels grounded in my results.”**

If done poorly, it will feel:
- thin
- showy
- or untrustworthy

Keep it selective.
Keep it deterministic.
Keep it credible.