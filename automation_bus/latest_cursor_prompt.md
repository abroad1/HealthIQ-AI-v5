---
work_id: FE-R3-RESULTS-JOURNEY-V6
branch: feature/results-journey-v6-r3-uncertainty-and-why-this-lead-won
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# Sprint: R-3 — Why This Lead Won / Uncertainty

## Objective

Implement Section 4 of the V6 Results Journey:

**Why This Lead Won / Uncertainty**

This sprint must make the reasoning process visible to the user immediately after the primary finding.

The user should be able to understand:

1. what nearly became the lead finding
2. why it did not
3. how certain HealthIQ is about the lead interpretation
4. what data is missing
5. what would change the conclusion

This sprint must increase trust without exposing raw engine traces or technical internals.

---

## Scope

### In scope

- Section 4: Why This Lead Won / Uncertainty
- Surfacing the strongest currently available deterministic confidence / runner-up / missing-data assets
- Clear trust-building presentation of uncertainty
- Repositioning or adapting existing components if appropriate
- Wiring only to **currently available frontend DTO/store data**

### Primary allowed assets

Use only assets already available on the frontend results path, specifically:

- `clinician_report_v1.sections.page1.runner_up_topic_line`
- `clinician_report_v1.sections.page1.runner_up_why_not_lead_line`
- `clinician_report_v1.sections.page1.confidence_and_missing_data`
- `clinician_report_v1.data_quality.confidence_caveat`
- `clinician_report_v1.sections.page1.primary_concern_mode`
- `clinician_report_v1.sections.page1.co_primary_signal_ids`
- `clinician_report_v1.sections.page1.ranking_policy_version`
- existing missing-data / confirmatory context already surfaced in `clinician_report_v1`
- existing frontend DTO/store fields already exposed in `analysis.ts`

### Out of scope

- New backend logic
- New DTO fields
- Raw `ExplainabilityReportV1`
- `arbitration_result`
- Gemini / LLM narrative generation
- Section 5+ work
- Biomarker-level evidence changes
- Pattern / phenotype display work

---

## Key principles (must be followed)

1. **Transparency without technical leakage**
   - user should understand why the lead won
   - do not expose raw arbitration traces, engine logs, or debugging language

2. **Confidence must feel honest, not defensive**
   - uncertainty should build trust
   - do not make the engine sound weak or confused if the deterministic conclusion is valid

3. **Runner-up must clarify, not distract**
   - this section is about why the main lead stands
   - not about listing every alternative interpretation

4. **No false precision**
   - if missing-data explanation is limited, keep it limited
   - do not invent detailed uncertainty narratives

5. **No duplication with Section 3**
   - Section 3 explains the lead and its evidence
   - Section 4 explains why this lead won and what uncertainty remains
   - keep these roles distinct

---

## Confirmed data authority for this sprint

This sprint must be built only from data already available on the frontend results path.

### Primary section assets

- `clinician_report_v1.sections.page1.runner_up_topic_line`
- `clinician_report_v1.sections.page1.runner_up_why_not_lead_line`
- `clinician_report_v1.sections.page1.confidence_and_missing_data`
- `clinician_report_v1.data_quality.confidence_caveat`
- `clinician_report_v1.sections.page1.primary_concern_mode`
- `clinician_report_v1.sections.page1.co_primary_signal_ids`
- `clinician_report_v1.sections.page1.ranking_policy_version`

### Explicit non-authority for this sprint

Do not use or depend on:

- raw `ExplainabilityReportV1`
- backend-only arbitration objects
- raw `arbitration_result`
- new DTO additions
- internal trace structures

If richer uncertainty logic requires new compiler work, that is a later sprint.

---

## Target UX structure

### Section 4 — Why This Lead Won / Uncertainty

**Purpose:**
Give the user a clear and calm explanation of why the current lead finding was chosen, what nearly competed with it, and how much uncertainty remains.

**This section must answer:**
- what nearly became the lead
- why it did not
- whether the lead was obvious or closely contested
- what missing information limits certainty
- what would make the conclusion stronger or weaker

---

### Required subsection structure

#### A. Why this lead won

Must display:
- a short explanation of why the lead finding was chosen
- primarily derived from:
  - `runner_up_why_not_lead_line`
  - `primary_concern_mode`

Rules:
- this must not read like an engine trace
- it must be short and readable
- if there is no meaningful runner-up explanation, omit cleanly

---

#### B. Competing finding

Must display:
- the runner-up / close competing finding only if present
- from `runner_up_topic_line`

Rules:
- max 1 competing finding
- this is not a ranked alternatives list
- if no runner-up exists, omit this block

---

#### C. How confident we are

Must display:
- confidence framing from:
  - `confidence_and_missing_data`
  - `data_quality.confidence_caveat`

Rules:
- this should feel calm and specific
- do not show multiple overlapping confidence blocks if one is enough
- if both fields exist, shape them into a clean non-duplicative presentation

---

#### D. What limits certainty

Must display:
- short missing-data / uncertainty explanation
- derived from available page1 confidence/missing-data text and any related surfaced deterministic context

Rules:
- focus on what is absent and why it matters
- do not create a separate “limitations essay”
- maximum one short block

---

#### E. Special case — near tie / co-primary mode

If `primary_concern_mode` indicates:
- close call
- technical tiebreak
- co-primary context

then the section must reflect that clearly and calmly.

Rules:
- do not over-dramatise
- explain that more than one interpretation was close if that is true
- `co_primary_signal_ids` may be used only as an internal presence check that a co-primary situation exists
- do not render raw signal IDs to the user
- do not surface raw ranking logic or technical policy text as a main body block

---

## Fallback model (mandatory)

### Case 1 — Full runner-up + confidence data present
Show:
- why this lead won
- competing finding
- how confident we are
- what limits certainty

### Case 2 — Confidence present, runner-up absent
Show:
- how confident we are
- what limits certainty

Do not create a fake competing finding block.

### Case 3 — Minimal confidence signal only
Show:
- one calm confidence/limitation block

Do not overbuild the section.

### Case 4 — No meaningful uncertainty assets
Omit the section cleanly rather than rendering an empty shell.

---

## Component / architecture rules

Before creating new components:
- identify whether existing interpretation / panel / trust-related components can be reused or adapted

Likely existing candidates:
- `InsightPanel`
- `PipelineStatus`
- related results components already surfacing clinician report confidence context

Only create new components if:
- no suitable component exists
- or reuse would create duplication or conceptual confusion with other sections

Avoid duplicating confidence / ambiguity rendering logic across components.

---

## Files likely impacted

- `frontend/app/(app)/results/page.tsx`
- existing results components handling interpretation / trust / confidence
- new Section 4 wrapper component only if needed
- frontend helper/lib for shaping uncertainty text only if necessary

Do not create backend dependencies in this sprint.

---

## Content shaping rules

1. Do not repeat the same wording already shown in:
   - Section 1
   - Section 3
   - existing trust strip / pipeline status copy

2. Section 4 must feel like:
   - a trust layer
   - not a repeat of the lead interpretation

3. Keep visible text tight:
   - one short why-this-won explanation
   - one runner-up block max
   - one confidence/limitation block
   - one special-case tie/co-primary clarification only if needed

4. If the deterministic content is thin:
   - keep the section thinner
   - do not compensate with invented transparency prose

5. `ranking_policy_version` may be retained only as a subtle metadata/detail element if already present in current UX patterns
   - do not elevate it into the main explanatory text
   - do not make policy version feel like a user-facing headline

---

## Acceptance criteria

1. Section 4 appears after Section 3 and before later evidence-heavy layers

2. User can understand:
   - what nearly became the lead
   - why the current lead won
   - how confident the system is
   - what limits certainty

3. Section uses only currently available frontend DTO/store data

4. No raw arbitration traces or internal technical language

5. No fabricated runner-up / uncertainty explanations where data is absent

6. No references to:
   - phenotype
   - internal IDs
   - raw signal names
   - backend-only arbitration or explainability artifacts

7. Section renders safely with:
   - full runner-up + confidence data
   - confidence-only data
   - minimal uncertainty data
   - no useful uncertainty data (section omitted cleanly)

---

## Test instructions

- Run full analysis flow via `/upload → /results`
- Test with:
  - case with close/competing finding present
  - case with clear lead and minimal runner-up
  - case with strong confidence caveat / missing-data note
  - case where uncertainty assets are minimal or absent

Validate:
- Section 4 renders in the right position
- runner-up block only appears when real data exists
- confidence wording is calm and non-duplicative
- no empty shells / broken subsection headings
- no repeated wording with Section 3 or trust strip
- no raw policy / technical trace leakage

Confirm no regression in:
- Body Overview
- What’s Working Well
- Primary Finding and Why
- InsightPanel / clinical interpretation
- PipelineStatus
- navigation / loading / advanced tabs

---

## Completion criteria

- Code compiles cleanly
- No console errors
- Manual UX validation passes
- Section 4 materially improves trust and transparency without increasing confusion
- Ready for gate validation via kernel

---

## Notes

This sprint is sensitive because it introduces uncertainty handling.

Do not overreach.
Do not make the system sound uncertain when the deterministic conclusion is strong.
Do not expose internal mechanics as if they were user-facing explanation.

The goal is to make the user feel:

**“I can see why this conclusion was chosen, and I understand how certain the system is.”**