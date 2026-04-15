---
work_id: FE-R1-RESULTS-JOURNEY-V6
branch: feature/results-journey-v6-r1-page-architecture
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# Sprint: R-1 — Results Page Architecture + Section 1 + Section 2 Reframe

## Objective

Restructure the `/results` page to implement the opening of the V6 Results Journey:

1. Introduce a **clear, guided entry point**
2. Present a **Body Overview (Section 1)** before any deep data
3. Reposition **“What’s Working Well” (Section 2)** immediately after
4. Embed a **lightweight “how to read this page” framing** without slowing the user down

This sprint must change the **shape of the experience**, not just styling.

---

## Scope

### In scope

- `/results` page layout restructuring
- Section 1: Body Overview (new)
- Section 2: What’s Working Well (reposition + refine)
- Lightweight intro framing (inline, not a full page)
- Wiring only to **currently available frontend DTO/store data**, specifically:
  - `clinician_report_v1`
  - `balanced_systems_v1`
  - `clusters`
  - existing top-level analysis metadata already present on the current frontend path

### Out of scope

- Section 3+ (Deep Discovery, Glass Box, etc.)
- Pattern / phenotype display layer (R-7 / R-8)
- New backend logic
- Changes to analysis pipeline
- New DTO fields
- Visual polish beyond functional clarity

---

## Key principles (must be followed)

1. **User came for results → show value immediately**
   - No long educational block before insight

2. **Introduce → show → reinforce**
   - micro framing → insight → reinforcement

3. **Reassurance before concern**
   - Section 2 must clearly show what is stable/working

4. **No generic summaries**
   - All text must be grounded in actual analysis outputs

5. **Do not expose raw structures**
   - no raw JSON
   - no internal naming

6. **Do not depend on unavailable fields**
   - do not use `arbitration_result`
   - do not use `system_capacity_scores`
   - do not use `adjusted_system_burden_vector`
   - do not require backend additions in this sprint

---

## Confirmed data authority for this sprint

This sprint must be built only from data already available on the frontend results path.

### Primary section assets

- `clinician_report_v1.sections.page1`
- `balanced_systems_v1`
- `clusters`
- existing analysis-level fields already present in `analysis.ts` / store

### Explicit non-authority for this sprint

The following are not currently available on the frontend DTO/store path and must not be referenced in implementation logic:

- `arbitration_result`
- `system_capacity_scores`
- `adjusted_system_burden_vector`

If any of these are needed, that is a separate backend/DTO sprint, not this one.

---

## Target UX structure

### Section 1 — Body Overview (NEW)

**Purpose:**
Give the user immediate orientation and a single, clear understanding of their body state.

**Must display:**

- One **primary sentence**
  - derived from `clinician_report_v1.sections.page1`
  - using the best available combination of:
    - `primary_concern`
    - `key_findings`
    - any existing page1 summary fields already present
  - must answer:
    - what stands out
    - whether there is a clear lead concern
    - that the page will guide the user through the bigger picture

**Primary sentence rule:**
- it must be derived from available `clinician_report_v1` content
- it must **not** be a raw dump of page1 fields
- it must be shaped into a single clear sentence
- do not render raw clinician-report blocks
- do not show multi-paragraph summaries in this section

Example shape (not hardcoded):
> “Your results suggest one main area that deserves closer attention, and we’ll show you how it fits into the wider picture of how your body is functioning.”

- A simple overview visual or structural summary
  - must be built only from currently available frontend data
  - may use:
    - `balanced_systems_v1`
    - `clusters`
    - sectioned labels such as “stable”, “needs attention”, “explore further”
  - must allow quick scan across the body-level picture
  - no heavy animation required

**Add inline micro-framing (1–2 lines max):**
- example intent:
  > “We’ve grouped your results into body systems and patterns so you can understand the bigger picture before looking at the individual markers.”

Do not expand beyond this.

---

### Section 2 — What’s Working Well (REPOSITION + REFINE)

**Purpose:**
Anchor the user in stability before introducing problems.

**Must display:**

- Systems with reassuring / stable interpretation
  - derived from `balanced_systems_v1`
  - if needed, supported by existing `clusters` context already on the frontend path

- Each item must:
  - name the system clearly
  - include a short, grounded explanation

Example shape:
> “Your liver and kidney systems are showing no clear signs of strain in this panel.”

**Rules:**

- No vague praise (“looks good”, “healthy”)
- Must be tied to actual system interpretation
- Limit to top 2–4 systems max (avoid overload)
- Each system explanation must be:
  - maximum 1 sentence
  - specific
  - non-repetitive across systems
- Do not repeat the same phrasing across multiple systems

---

## Data wiring requirements

You must verify:

- `clinician_report_v1.sections.page1` is available and mapped correctly
- `balanced_systems_v1` is available and filtered/rendered safely
- `clusters` are available if needed for light overview support
- fallback behaviour exists if any of the above are missing

Fallback rules:

- If `balanced_systems_v1` empty:
  - show minimal message:
    > “No clearly stable systems are highlighted in this panel — we’ll guide you through the key findings below.”

- If `clinician_report_v1.sections.page1` missing or incomplete:
  - do not fabricate
  - show safe fallback:
    > “We’ve analysed your results and will guide you through the key findings below.”

- If both are partial:
  - page must still render
  - do not show empty visual shells or broken section containers

---

## Component / architecture rules

Before creating new components:
- identify whether existing results, summary, or balanced-system components can be reused or adapted

Only create new components if:
- no suitable component exists
- or reuse would introduce complexity or inconsistency

Avoid duplicating rendering logic across components.

---

## Files likely impacted

- `frontend/app/(app)/results/page.tsx`
- `frontend/app/components/results/BalancedSystemsSummary.tsx`
- `frontend/app/types/analysis.ts`
- new or adapted results-page section components only where necessary

Do not create backend dependencies in this sprint.

---

## Acceptance criteria

1. Results page opens with:
   - Body Overview (Section 1)
   - followed immediately by What’s Working Well (Section 2)

2. User can understand within ~5 seconds:
   - that there is an overall body-level interpretation
   - whether anything stands out
   - that there are also stable/reassuring areas

3. No large text blocks before insight

4. All text grounded in real available frontend data (no placeholders)

5. Page does not crash with partial/missing data

6. No references to:
   - “phenotype”
   - internal IDs
   - raw signal names
   - unavailable fields such as `arbitration_result`, `system_capacity_scores`, or `adjusted_system_burden_vector`

---

## Test instructions

- Run full analysis flow via `/upload → /results`
- Test with:
  - strong abnormal case
  - mostly normal case
  - mixed case
- Validate:
  - Section 1 renders correctly
  - Section 2 shows correct stable systems where available
  - no duplication
  - no empty UI blocks
- Confirm no regression in:
  - navigation
  - analysis loading
  - existing components

---

## Completion criteria

- Code compiles cleanly
- No console errors
- Manual UX validation passes
- Ready for gate validation via kernel

---

## Notes

This sprint is foundational.

Do not over-engineer visuals.
Do not expand scope into later sections.
Do not introduce backend requests for missing fields in this sprint.

The goal is to **change how the user experiences the first 10 seconds** of the product using data the frontend already has.