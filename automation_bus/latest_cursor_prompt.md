---
work_id: FE-R2-RESULTS-JOURNEY-V6
branch: feature/results-journey-v6-r2-primary-finding-why
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# Sprint: R-2 — Primary Finding and Why

## Objective

Implement Section 3 of the V6 Results Journey:

**Primary finding and why**

This sprint must turn the lead interpretation into a genuine reasoning layer rather than a short headline or a buried clinical block.

The user should be able to understand:

1. what the main finding is
2. what it means
3. what evidence supports it
4. what complicates it
5. what data would strengthen or weaken confidence

This sprint must deepen understanding without introducing speculative narrative.

---

## Scope

### In scope

- Section 3: Primary Finding and Why
- Surfacing the best currently available deterministic explanation assets for the lead finding
- Clear fallbacks when richer hypothesis assets are absent
- Repositioning or adapting existing components if appropriate
- Wiring only to **currently available frontend DTO/store data**

### Primary allowed assets

Use only assets already available on the frontend results path, specifically:

- `clinician_report_v1.sections.page1.primary_concern`
- `clinician_report_v1.sections.page1.top_hypothesis_line`
- `clinician_report_v1.sections.page1.key_findings`
- `clinician_report_v1.sections.page1.chains`
- `clinician_report_v1.sections.root_cause`
- `clinician_report_v1.sections.confirmatory_tests`
- existing fields already exposed in `analysis.ts` / store and currently consumed by results components

### Out of scope

- Section 4+ (uncertainty, pattern layer, biomarkers, etc.)
- New backend logic
- New DTO fields
- New compiler work
- Gemini / LLM narrative generation
- Pattern / phenotype display layer
- Any use of internal explainability artifacts not already surfaced to the frontend DTO
- Any raw use of `ExplainabilityReportV1`

---

## Key principles (must be followed)

1. **Explain, do not dump**
   - The section must feel like a guided interpretation
   - Do not paste raw clinician-report blocks into the page

2. **Deterministic assets only**
   - Use currently available frontend-facing deterministic text
   - Do not fabricate reasoning

3. **Lead first, evidence second**
   - The user must first understand the main interpretation
   - Then see what supports it and what complicates it

4. **No false completeness**
   - If root-cause coverage is absent or partial, say less
   - Do not imply a full hypothesis model exists where it does not

5. **Keep tone calm and serious**
   - No alarmism
   - No consumer-wellness fluff
   - No clinical jargon without framing

---

## Confirmed data authority for this sprint

This sprint must be built only from data already available on the frontend results path.

### Primary section assets

- `clinician_report_v1.sections.page1.primary_concern`
- `clinician_report_v1.sections.page1.top_hypothesis_line`
- `clinician_report_v1.sections.page1.key_findings`
- `clinician_report_v1.sections.page1.chains`
- `clinician_report_v1.sections.root_cause`
- `clinician_report_v1.sections.confirmatory_tests`

### Explicit non-authority for this sprint

Do not use or depend on:

- raw `ExplainabilityReportV1`
- `arbitration_result`
- any backend-only signal-library source not already surfaced to the current frontend DTO
- new backend / DTO additions

If richer reasoning requires new contract work, that is a later sprint.

---

## Target UX structure

### Section 3 — Primary Finding and Why

**Purpose:**
Give the user a clear explanation of the lead interpretation and the strongest current reasoning behind it.

**This section must answer:**
- what the main finding is
- what HealthIQ currently thinks is the leading explanation
- what supports that interpretation
- what complicates or weakens it
- what follow-up data or test would help

---

### Required subsection structure

#### A. Lead finding statement

Must display:
- a short lead interpretation statement
- derived from `primary_concern`
- optionally supported by `top_hypothesis_line`

Rules:
- must be concise
- must not be a raw field dump
- must not repeat the exact Section 1 wording
- must feel like the start of a deeper explanation, not another hero banner

---

#### B. What this means

Must display:
- a short explanatory paragraph or block
- primarily derived from `top_hypothesis_line`
- may use the strongest available `key_findings[0]` support if needed

Rules:
- should explain what the lead pattern means in human terms
- do not introduce new claims beyond surfaced deterministic content
- do not over-expand if the underlying text is thin

---

#### C. How the evidence connects

Must display:
- 1–2 chain narratives from `chains`
- if available

Rules:
- show only the strongest 1–2
- do not dump a long list
- must read as “how these findings connect”
- if `chains` absent, omit cleanly

---

#### D. Supports this interpretation

Must display:
- strongest evidence-for items from `root_cause`
- only if `root_cause` exists for the lead finding

Rules:
- keep concise
- max 3 evidence-for items
- if absent, do not fabricate a “supports” block

---

#### E. Pulls against or complicates it

Must display:
- strongest evidence-against / complicating items from `root_cause`
- only if available

Rules:
- max 2–3 items
- this is important for trust
- if absent, omit cleanly

---

#### F. What would clarify the picture

Must display:
- missing-data item(s) and/or confirmatory test rationale
- from `root_cause` and `confirmatory_tests` where available

Rules:
- keep this short
- this is not the full action section
- it should answer:
  - what extra data would make this interpretation stronger or weaker?

---

## Fallback model (mandatory)

This sprint must handle partial or absent hypothesis coverage honestly.

### Case 1 — Full useful root-cause data present
Show:
- lead finding
- what this means
- 1–2 chain narratives
- supports
- complicates
- what would clarify

### Case 2 — `top_hypothesis_line` present, but root-cause weak/absent
Show:
- lead finding
- what this means
- 1–2 chain narratives if available
- short “what would clarify” only if confirmatory test data exists

Do **not** fabricate supports/complicates sections.

### Case 3 — minimal page1 only
Show:
- lead finding
- short explanatory fallback from available `key_findings[0]` or equivalent page1 content

Do not create fake hypothesis structure.

---

## Component / architecture rules

Before creating new components:
- identify whether existing interpretation / root-cause components can be reused or adapted

Likely existing candidates:
- `InsightPanel`
- `RootCauseEvidenceSummary`
- related results components already consuming clinician report content

Only create new components if:
- no suitable component exists
- or reuse would create confusing coupling with later sections

Avoid duplicating reasoning-rendering logic across components.

---

## Files likely impacted

- `frontend/app/(app)/results/page.tsx`
- existing interpretation / root-cause related result components
- new Section 3 wrapper component only if needed
- frontend helper/lib for shaping lead explanation text only if necessary

Do not create backend dependencies in this sprint.

---

## Content shaping rules

1. Do not repeat the same sentence in:
   - Section 1
   - Section 3
   - existing clinical interpretation block

2. Section 3 must feel like:
   - deeper explanation
   - not another summary header

3. Keep visible text tight:
   - lead statement
   - one short explanatory block
   - a few evidence bullets/rows
   - a short clarify-the-picture block

4. If the surfaced deterministic content is thin:
   - keep the section thinner
   - do not compensate with invented prose

---

## Acceptance criteria

1. Section 3 appears after Section 2 and before later evidence-heavy layers

2. User can understand:
   - what the lead finding is
   - what it means
   - what supports it
   - what complicates it
   - what would help clarify it

3. Section uses only currently available frontend DTO/store data

4. No raw clinician-report dumps

5. No fabricated reasoning where root-cause coverage is absent

6. No references to:
   - phenotype
   - internal IDs
   - raw signal names
   - backend-only explainability artifacts

7. Section renders safely with:
   - full root-cause data
   - partial data
   - minimal page1 data only

---

## Test instructions

- Run full analysis flow via `/upload → /results`
- Test with:
  - case with good root-cause coverage
  - case with weak/partial root-cause coverage
  - case with only minimal page1 narrative available

Validate:
- Section 3 renders in the right position
- lead finding is clear
- chain narratives show only when meaningful
- supports/complicates only show when real data exists
- clarify-the-picture is concise and grounded
- no empty shells / broken subsection headings
- no repeated wording with Section 1

Confirm no regression in:
- Body Overview
- What’s Working Well
- InsightPanel / clinical interpretation
- RootCauseEvidenceSummary if reused elsewhere
- navigation / loading / advanced tabs

---

## Completion criteria

- Code compiles cleanly
- No console errors
- Manual UX validation passes
- Section 3 is visibly more explanatory than the current interpretation block
- Ready for gate validation via kernel

---

## Notes

This sprint is the first one that materially affects **narrative integrity**.

Do not overreach.
Do not write beyond the deterministic evidence.
Do not expand into Section 4 uncertainty logic yet.

The goal is to make the user feel:

**“I understand what the main finding is, and I can see why the system is saying this.”**