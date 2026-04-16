---
work_id: FE-R7-RESULTS-JOURNEY-V6
branch: feature/results-journey-v6-r7-pattern-layer-existence-check
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# Sprint: R-7 — Pattern Layer Existence Check and Specification Gate

## Objective

Complete the formal gate for **Section 5 — Patterns across your body**.

This is **not** a frontend implementation sprint.

This sprint must determine, in a disciplined and evidence-based way:

1. what the current system / cluster / interpretation layer actually provides
2. whether the current frontend-accessible assets are sufficient to build Section 5 now
3. whether a governed interpretation-display layer already exists
4. whether additional contract/content work is required before frontend implementation
5. how the future pattern layer should align with the approved taxonomy direction:
   - phenotype
   - risk construct
   - syndrome/state
   - organ-pattern

The output of this sprint must be a **written decision artifact**, not code-first implementation.

---

## Scope

### In scope

- Formal existence check of the current Section 5 source assets
- Verification of current cluster/system/interpretation layer on the frontend path
- Verification of available naming/display fields
- Verification of whether current assets can support a user-facing pattern layer
- Alignment check against current interpretation taxonomy and commercial screening direction
- Written recommendation for one of two outcomes:
  - Section 5 can be implemented as a frontend surfacing sprint
  - Section 5 requires backend/content/contract work first

### Out of scope

- Frontend implementation of Section 5
- New backend logic
- New DTO fields
- Renaming internal contracts during this sprint
- Large refactors
- Gemini narrative work
- UI polish or prototype building

---

## Key principles (must be followed)

1. **This is a gate, not a build sprint**
   - Do not drift into implementation

2. **Do not assume “phenotype layer” exists**
   - Verify what exists
   - Do not infer missing structure

3. **Taxonomy must remain medically disciplined**
   - not everything should be called a phenotype
   - Section 5 must support multiple governed interpretation classes where appropriate

4. **Commercial alignment matters**
   - the future pattern layer must be compatible with the commercial screening direction already established

5. **Naming quality is first-class**
   - weak generic labels are not acceptable
   - if the contract cannot support good naming, that must be called out explicitly

---

## Required inputs

This sprint must use the following as governing context:

### A. Results Journey v6
Use the current v6 paper as authority for:
- Section 5 purpose
- Phase 2 classification
- existence-check requirement
- three-layer naming goal
- fallback expectations

### B. Interpretation taxonomy direction
Use the current agreed taxonomy direction:
- not every entity is a phenotype
- supported classes may include:
  - phenotype
  - risk construct
  - syndrome/state
  - organ-pattern

### C. Commercial screening priority direction
Use the current strategic direction that future interpretation expansion should align to commercially valuable preventive/screening domains:
- dysglycaemia / insulin resistance
- atherogenic cardiometabolic risk
- CKD / kidney risk
- MASLD / liver fibrosis risk
- integrated metabolic clustering
- iron deficiency as a secondary high-volume lane

This does **not** mean Section 5 must fully implement those domains now.
It means the existence check must assess whether the future pattern layer can evolve in that direction without taxonomy or contract chaos.

---

## Required investigation tasks

### 1. Verify current frontend-accessible interpretation sources

Determine exactly what currently exists on the frontend results path for Section 5 candidates, including:

- `clusters[]`
- cluster labels / names
- severity / status
- cluster summaries
- supporting biomarker groupings
- system explainers
- any current system-topic naming
- any already-surfaced interpretation classification fields

For each, determine:
- whether it exists
- whether it is already on the frontend path
- whether it is user-safe
- whether it is strong enough for direct use

---

### 2. Verify current contract support for naming

Determine whether the current layer supports the following naming/display model:

- internal id
- scientific classification
  - phenotype / risk / syndrome-state / organ-pattern
- clinical display name
- plain-English subtitle
- why-it-matters explainer

For each field, determine:
- exists now
- partially exists
- missing entirely

Do not infer fields that are not actually present.

---

### 3. Assess current naming quality

Assess whether the current user-facing naming is good enough for Section 5.

This must explicitly answer:
- are current labels too generic?
- are they medically weak?
- are they commercially weak?
- would the current naming collapse the value of the middle interpretation layer?

Be blunt and specific.

---

### 4. Assess whether Section 5 is currently a surfacing sprint or a contract/content sprint

You must end with one clear decision:

### Option A — Surfacing sprint
Choose this only if current assets are strong enough that frontend implementation can proceed without creating misleading UX.

### Option B — Contract/content sprint first
Choose this if:
- naming fields are missing
- taxonomy classification is missing
- interpretation summaries are too weak
- the current cluster/system layer cannot support a strong user-facing middle layer

No hedging. Pick one.

---

### 5. Produce the implementation consequences

Depending on the decision:

#### If Option A
Specify what R-8 should implement using the current assets.

#### If Option B
Specify what must be built before R-8 can exist, for example:
- naming contract
- classification field
- plain-English subtitle layer
- why-it-matters copy
- interpretation-display DTO work

---

## Explicit questions this sprint must answer

1. What exactly is the current Section 5 source layer?
2. Is there already a governed interpretation-display layer?
3. Can current assets support user-facing pattern cards without weak/generic naming?
4. Do current assets support the approved taxonomy direction?
5. Can the future pattern layer evolve toward commercially valuable screening constructs cleanly?
6. Is R-8 a frontend sprint next, or a backend/content contract sprint first?

---

## Output format

Produce a short written decision artifact with these sections:

1. Executive conclusion
2. Current Section 5 asset inventory
3. Naming/display contract assessment
4. Taxonomy alignment assessment
5. Commercial alignment assessment
6. Decision:
   - Surfacing sprint now
   - or contract/content sprint first
7. Consequences for R-8
8. Risks if we proceed incorrectly

---

## Acceptance criteria

1. The sprint ends with a clear yes/no decision on whether Section 5 is implementation-ready
2. The decision is grounded in actual existing assets, not assumptions
3. Naming quality is explicitly assessed
4. Taxonomy alignment is explicitly assessed
5. Commercial-screening alignment is explicitly assessed
6. The output clearly states what R-8 must be next

---

## Completion criteria

- Decision artifact completed
- No implementation drift
- No speculative contract assumptions
- Clear recommendation for the next sprint

---

## Notes

This sprint is strategically important.

If done well, it will prevent:
- weak middle-layer UX
- taxonomy confusion
- phenotype overreach
- misalignment between product UX and future commercial strategy

The goal is to answer:

**“What are the named health constructs we can truthfully and usefully show users next — and are we actually ready to show them?”**