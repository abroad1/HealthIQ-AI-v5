---
work_id: FE-R5-RESULTS-JOURNEY-V6
branch: feature/results-journey-v6-r5-system-understanding-layer
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# Sprint: R-5 — System Understanding Layer (“How to read your body”)

## Objective

Introduce a **tight, embedded explanation layer** that helps the user understand:

1. why their results are grouped into systems
2. how to interpret “stable vs strain”
3. how biomarkers connect to the broader picture

This sprint must create an **“Ah-ha” moment** without slowing the user down or introducing a long educational block.

---

## Scope

### In scope

- Section 5: System Understanding Layer
- Short, embedded explanation of:
  - system grouping logic
  - interpretation model (stable vs strain)
  - biomarker → system → finding relationship
- Light grounding in the user’s actual data
- Rendering using only **currently available frontend DTO/store data**

### Primary allowed assets

Use only data already available on the frontend results path:

- `balanced_systems_v1`
- `clusters[]`
- `biomarkers[]`
- Section 3 (Primary Finding) already-rendered context
- Section 4 (Why this lead won) already-rendered context
- existing system/cluster labels already present in the UI

### Out of scope

- New backend logic
- New DTO fields
- Pattern / phenotype naming layer (R-7 / R-8)
- Long-form educational content
- Standalone “learn” pages or modals
- Gemini / LLM generated education
- Rewriting earlier sections

---

## Key principles (must be followed)

1. **No long education block**
   - This must not feel like a tutorial
   - Maximum: short, scannable, embedded content

2. **Explain using the user’s data**
   - All explanation must be anchored to what the user has already seen
   - No abstract biology lecture

3. **Reinforce, not interrupt**
   - This section should make earlier sections clearer
   - Not introduce new complexity

4. **One concept per block**
   - Avoid dense paragraphs
   - Use short, clearly separated ideas

5. **No generic filler**
   - Every sentence must help the user interpret their results

---

## Confirmed data authority for this sprint

This sprint must be built only from data already available on the frontend results path.

### Primary section assets

- `balanced_systems_v1`
- `clusters[]`
- `biomarkers[]`
- already-rendered lead finding context (Section 3)
- already-rendered system labels

### Explicit non-authority

Do not use or depend on:

- new “system explanation” backend fields
- Knowledge Bus raw content
- unsurfaced phenotype definitions
- Gemini-generated educational content
- any new DTO additions

---

## Target UX structure

### Section 5 — How to understand your results

**Purpose:**
Help the user understand how to read the page they are currently viewing.

**This section must answer:**
- why results are grouped
- what systems represent
- how markers connect to findings

---

## Required structure

This section must be composed of **3 short blocks only**.

---

### Block A — Why your results are grouped

**Must explain:**
- that biomarkers are grouped into systems
- that this helps reveal how the body is functioning as a whole

**Must anchor to real data:**
- reference 1–2 system names visible on the page
- optionally reference the system highlighted in Section 3

Example shape (not hardcoded):
> “We’ve grouped your results into body systems so you can see how different markers work together. For example, your [system name] combines markers like [A/B/C] to help explain your main finding.”

Rules:
- do not list many markers
- do not show raw IDs
- keep to 1–2 examples max

---

### Block B — What “stable vs strain” means

**Must explain:**
- what it means for a system to be stable
- what it means for a system to show strain

**Must anchor to real data:**
- reference `balanced_systems_v1`
- optionally contrast with the system driving the primary finding

Example shape (not hardcoded):
> “Systems shown as stable are operating within expected ranges. Where we highlight strain, it means multiple markers are pointing in the same direction and may need closer attention.”

Rules:
- no medical overclaiming
- no diagnostic language
- keep it simple and grounded

---

### Block C — How markers connect to the bigger picture

**Must explain:**
- biomarkers are individual signals
- patterns emerge when they are interpreted together

**Must anchor to real data:**
- reference the existence of the lead finding
- optionally reference clusters or groups already shown

Example shape (not hardcoded):
> “Individual markers give useful signals, but the most important insights come from how they interact. That’s how we identified your main finding.”

Rules:
- do not introduce new concepts not already shown
- do not repeat Section 3 wording

---

## Fallback model (mandatory)

### Case 1 — Full system + cluster context available
Show all 3 blocks with light grounding in real data

### Case 2 — Limited system context
Show all 3 blocks but:
- reduce references to specific systems
- keep wording more general

### Case 3 — Minimal usable context
Show:
- simplified versions of the 3 blocks
- no forced references to missing data

Do not:
- create fake examples
- render broken placeholders

---

## Component / architecture rules

Before creating new components:
- check whether an existing section container or card layout can be reused

If new component is required:
- create a single dedicated component for Section 5
- keep logic minimal
- do not introduce new shared libraries

Avoid:
- duplicating system or biomarker rendering logic
- re-fetching or reprocessing data

---

## Files likely impacted

- `frontend/app/(app)/results/page.tsx`
- new component: SystemUnderstandingSection (or equivalent)
- minimal helper logic if required for selecting example systems/markers

No backend files.

---

## Content shaping rules

1. Maximum:
   - 3 blocks
   - 2–3 sentences per block

2. No repetition of:
   - Section 1 wording
   - Section 3 explanation
   - Section 4 trust language

3. No:
   - long paragraphs
   - bullet dumps
   - generic “health education” language

4. Tone:
   - clear
   - calm
   - intelligent
   - not patronising

---

## Placement rules

- Section 5 must appear:
  - after Section 4 (Why this lead won)
  - before biomarker-heavy sections

- It must feel like:
  - a natural continuation
  - not a separate learning module

---

## Acceptance criteria

1. Section 5 renders as exactly 3 short blocks

2. User can understand:
   - why systems exist
   - what stable vs strain means
   - how markers connect to findings

3. Content is anchored to real data where available

4. No generic or filler educational text

5. Section does not slow down page comprehension

6. No references to:
   - phenotype
   - internal IDs
   - raw signal names
   - unsurfaced backend data

---

## Test instructions

- Run `/upload → /results`

Test with:
- strong abnormal case
- mostly normal case
- mixed case

Validate:
- section appears in correct position
- content adapts to available data
- no broken examples
- no repeated wording from earlier sections
- section is quick to scan (<10 seconds)

Confirm no regression in:
- Sections 1–4
- biomarker expansion
- navigation / loading
- advanced tabs

---

## Completion criteria

- Code compiles cleanly
- No console errors
- Manual UX validation passes
- Section delivers a clear “Ah-ha” moment
- No overlong educational content introduced
- Ready for gate validation via kernel

---

## Notes

This sprint is about **clarity, not volume**.

If done correctly, the user should feel:

“I finally understand how to read this.”

If done poorly, it will feel like:
- a generic explainer
- or unnecessary friction

Keep it tight.
Keep it grounded.
Keep it useful.