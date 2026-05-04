# HealthIQ AI — Front-End UX Asset Surfacing Proposal

## Purpose

This document proposes a concrete front-end results experience and specifies exactly which existing text assets should be surfaced in each section.

This is not a technical audit.
This is not a generic vision note.
This is a build-oriented content architecture proposal grounded in the audited assets already available in the codebase.

---

## 1. Core principle

HealthIQ is showing users a level of systems-based interpretation most people have never experienced before.

So each major section should do three things:

1. introduce what the user is about to see  
2. show the user their result in that frame  
3. summarise what it means for them

That means the UX should not jump straight into scores, clusters, or biomarker cards.
It should teach the frame first, then show the user’s result, then interpret it.

---

## 2. Design direction

The results page should feel:

- premium
- restrained
- clinically credible
- future-facing but not flashy
- educational without being patronising
- transparent about uncertainty

Avoid:

- sci-fi dashboard gimmicks
- excessive glow / pulse metaphors
- horizontal scrolling for key content
- raw debug / engine-log presentation
- dense table-first layouts at the top of the page

Recommended direction:

**Premium restrained clinical-futurist**

---

## 3. Recommended page architecture

1. How to read your body map  
2. Your body overview  
3. What’s working well  
4. Primary finding and why  
5. Key body-level insights  
6. Why this lead won / uncertainty  
7. Patterns across your body  
8. Marker-level evidence  
9. What to do next  
10. Clinician summary

---

## 4. Exact text assets to surface by section

## Section 1 — How to read your body map

### Purpose
Introduce the idea that HealthIQ groups blood markers into interacting body systems and patterns.

### Text assets to surface
These do not need to come from existing clinical contracts. This is product framing copy and should be authored deliberately.

Recommended content:
- short boilerplate explainer introducing body systems / marker groups / pattern reasoning
- one sentence explaining that a full blood panel lets us assess how multiple systems are functioning together
- one sentence explaining the journey: big picture → strongest systems → lead finding → evidence → next steps

### Why this section matters
Without this framing, users are dropped into an unfamiliar interpretation model without being taught how to read it.

---

## Section 2 — Your body overview

### Purpose
Give the user a whole-body orientation before detail.

### Primary text assets to surface
- `clinician_report_v1.sections.page1.primary_concern`
- selected body-level summary copy derived from:
  - `arbitration_result`
  - `system_capacity_scores`
  - `primary_driver_system_id`

### Supporting text assets
- a short, compiler-shaped summary line synthesising:
  - how many systems are stable
  - which system is the lead concern
  - whether the lead was obvious or a close call

### What should not be surfaced here
- biomarker values
- dense system cards
- full hypothesis blocks
- long educational explainers

### Recommendation
This section should use **short deterministic summary text**, not Gemini-led prose.

---

## Section 3 — What’s working well

### Purpose
Create reassurance early and show that the engine can identify strengths, not only strain.

### Primary text assets to surface
- `balanced_systems_v1.intro_line`
- `balanced_systems_v1.system_topic`
- `balanced_systems_v1.evidence_line`
- `balanced_systems_v1.capacity_note`

### Supporting text assets
- relevant cluster/system explainer snippets where available
- selected evidence statements tied to stable systems

### Why this is important
This is one of the highest-value existing deterministic assets and should become a first-class section, not a lower-page afterthought.

### Recommendation
Surface `balanced_systems_v1` prominently and early.
Do not bury it below biomarker evidence.

---

## Section 4 — Primary finding and why

### Purpose
Deliver the lead interpretation with actual reasoning depth.

### Primary text assets to surface
- `clinician_report_v1.sections.page1.primary_concern`
- `clinician_report_v1.sections.page1.top_hypothesis_line`
- `clinician_report_v1.sections.page1.key_findings[]` (selected, not necessarily all)
- `clinician_report_v1.sections.page1.chains[]`
- `root_cause_v1.hypotheses[].summary`
- `root_cause_v1.hypotheses[].evidence_for[].item`
- `root_cause_v1.hypotheses[].evidence_against[].item`
- `root_cause_v1.hypotheses[].missing_data[].reason`
- `root_cause_v1.confirmatory_tests[].rationale`

### What this section should answer
- what the lead pattern is
- why it matters
- what supports it
- what complicates it
- what data would clarify it

### Recommendation
This is one of the most underused high-value text layers in the product.
It should become a primary visible interpretation block, not secondary advanced content.

---

## Section 5 — Key body-level insights

### Purpose
Deliver the “wow” moments, but only where the insights are robust.

### Primary text assets to surface
Where available and mature enough:
- compiler-shaped summaries for `layer_c_features`
  - metabolic age
  - heart resilience
  - inflammation burden
  - fatigue-related feature
  - detox / clearance feature

### Supporting text assets
- deterministic explanation snippets describing what the feature means
- short contextual interpretation explaining why the feature matters for this user

### Important note
This section should only surface features that are:
- genuinely computed
- explainable
- clinically defensible

### Recommendation
This section should be present, but it should not become the emotional centre of the page until those features are fully trusted.

---

## Section 6 — Why this lead won / uncertainty

### Purpose
Build trust by showing the reasoning and uncertainty, not just the outcome.

### Primary text assets to surface
- `clinician_report_v1.sections.page1.runner_up_topic_line`
- `clinician_report_v1.sections.page1.runner_up_why_not_lead_line`
- `clinician_report_v1.sections.page1.confidence_and_missing_data`
- `clinician_report_v1.data_quality.confidence_caveat`
- selected `root_cause_v1.missing_data[]`

### Why this section matters
This is one of the best trust-building surfaces in the whole system.
Users should understand:
- what nearly led
- why it did not
- what is missing
- what would change the conclusion

### Recommendation
Surface these fields explicitly in a consumer-readable transparency section.
Do not leave them buried in the clinician report only.

---

## Section 7 — Patterns across your body

### Purpose
Show pattern-level reasoning beneath the lead story.

### Primary text assets to surface
- governed phenotype display names and subtitles (to be authored)
- phenotype-level “why it matters” explainers (to be authored)
- `clusters[]`
- `system_educational_explainer`
- pattern/group-level supporting evidence copy

### Important naming recommendation
Do not use generic labels like:
- Metabolic Health
- Cardiovascular Health
- Inflammatory Health
- Organ Health
- Nutritional Health
- Hormonal Health

Use medically meaningful pattern names plus plain-English subtitles, for example:
- Early Insulin Resistance Pattern  
  Early blood sugar regulation strain
- Vascular Inflammation and Homocysteine Pattern  
  Blood vessel stress and inflammatory strain
- Renal Stress Pattern  
  Kidney filtration and clearance strain

### Recommendation
This section should become the true middle layer between body overview and biomarker rows.

---

## Section 8 — Marker-level evidence

### Purpose
Show the underlying data for users who want depth.

### Primary text assets to surface
- `biomarkers[].contribution_context`
- `biomarkers[].biomarker_educational_explainer`
- `biomarkers[].system_educational_explainer` where relevant
- selected reference-range interpretation copy

### Supporting text assets
- signal contribution context
- cluster membership context
- biomarker education on demand

### Important note
This section is important, but it should come after the user has already been oriented and interpreted.

### Recommendation
Keep this as evidence depth, not as the first thing the user sees.

---

## Section 9 — What to do next

### Purpose
Move from interpretation to action.

### Primary text assets to surface
- `root_cause_v1.confirmatory_tests[].rationale`
- `report_v1.actions`
- `insights[].next_steps[]`
- clinician report action / follow-up fields where present

### What this should answer
- what to discuss with a clinician
- what further tests would clarify things
- what should happen next
- what matters most now

### Recommendation
This section should feel like a prioritised roadmap, not a generic advice box.

---

## Section 10 — Clinician summary

### Purpose
Provide a separate formal handoff.

### Primary text assets to surface
- full `ClinicianReportV1`

### Recommendation
Keep this clearly separate from the consumer journey.
Do not try to make the whole page switch live into “professional mode.”

---

## 5. Most valuable existing text assets to promote now

These are the highest-value existing assets that appear underused and should be surfaced more prominently:

1. `top_hypothesis_line`
2. `chains[]`
3. `runner_up_topic_line`
4. `runner_up_why_not_lead_line`
5. `confidence_and_missing_data`
6. `balanced_systems_v1`
7. `root_cause_v1` evidence-for / evidence-against / missing-data / confirmatory rationale
8. retail explainers (on-demand, not default)
9. signal-library explanation content — but only via compiler-mediated surfacing
10. explainability/arbitration-derived rationales — transformed, not raw

---

## 6. What should remain internal or transformed before surfacing

Do not surface directly to users:

- raw `meta.insight_graph`
- raw `ExplainabilityReportV1`
- raw burden vectors
- raw arbitration traces
- raw signal-library YAML prose without transformation
- policy/debug identifiers

These should only appear if:
- transformed into consumer-safe explanation
- or placed in clinician/technical export contexts

---

## 7. Deterministic vs Gemini recommendation

### Deterministic / compiler-shaped should power the main UX
Primary spine should come from:
- `clinician_report_v1`
- `root_cause_v1`
- `balanced_systems_v1`
- phenotype/pattern outputs
- retail explainers
- selected explainability-derived rationales

### Gemini should be supplementary
Gemini should later be used for:
- smoothing body-level summaries
- polishing category summaries
- improving readability of selected narrative sections

Gemini should **not** be the main explanation authority.
It should polish governed structured truth, not replace it.

---

## 8. Concrete next deliverables

The team should now produce these concrete follow-ons:

### Deliverable 1 — Results page section spec
For each section define:
- purpose
- intro copy goal
- show layer
- summary layer
- primary source assets
- secondary source assets
- hidden / expandable content

### Deliverable 2 — Phenotype display naming framework
For each governed phenotype define:
- internal id
- clinical display name
- plain-English subtitle
- why-it-matters explainer
- likely supporting biomarkers/signals

### Deliverable 3 — Deterministic narrative spine spec
Define exactly which backend fields power:
- body overview
- what’s working well
- primary finding and why
- why this lead won / uncertainty
- next steps

---

## 9. Final recommendation

The next build phase should focus on:

1. results-page architecture
2. phenotype/pattern naming
3. surfacing existing deterministic assets better
4. making balanced systems first-class
5. introducing a transparent “why this lead won” layer
6. delaying Gemini-led polish until the deterministic spine is right

That is the clearest route from a technically strong product to a world-class interpretation experience.
