# HealthIQ AI — Strategic Architectural Review
## Narrative asset inventory, UX surfacing strategy, and target user experience

You are conducting a strategic architectural review of the HealthIQ AI codebase and governed data assets.

This is not an implementation sprint.
This is not a repo-wide bug hunt.
This is not a prompt to change code.

Your job is to produce a clear architectural review that answers two questions:

1. What explanation, interpretation, and narrative assets already exist in the system that could be surfaced to create a rich, differentiated user experience?
2. What should HealthIQ AI actually present to the user, and where in the UX should each type of information live, so the product feels like a world-class metabolic reasoning engine rather than a fragmented reporting tool?

The required output is a strategy document, not code.

---

## Background

Recent work has materially improved the upload → parse → review journey.

We now have enough stability in the pre-analysis flow to stop treating parsing as the main blocker and move to the more important product question:

**What explanatory assets do we already have, and how should they be used to create a truly strong user experience?**

We already suspect that the codebase contains a large amount of governed explanatory material that is either:
- not surfaced at all
- surfaced in the wrong place
- surfaced too thinly
- compiled into weaker text than the source assets would allow

Examples likely include:
- signal-library explanation fields
- report compiler outputs
- clinician report structures
- root-cause structures
- explainability report structures
- insight graph content
- system/group explanatory content
- biomarker educational text
- contribution-context text
- narrative prompt inputs for Gemini / Layer C
- any other explanation-bearing content embedded in the governed data model or runtime contracts

At the same time, the product still does not feel like:
- a world-class metabolic reasoning engine
- a body-level interpretation experience
- a “wow, I now understand my body” product

This review exists to define the target explanatory architecture.

---

## What this review must do

Produce a strategic architecture document that covers:

1. **Narrative / explanation asset inventory**
2. **Current UX surfacing map**
3. **Gap analysis**
4. **Target user experience**
5. **Target layered explanation architecture**
6. **Deterministic vs Gemini boundary**
7. **Recommended asset-to-UX mapping**
8. **Sequenced next-step roadmap**

---

## Required review tasks

### 1. Inventory the explanation-bearing assets in the codebase

Identify all significant explanation-bearing assets currently available across the codebase and governed contracts.

At minimum, inspect and catalogue assets in these categories where they exist:

- signal-library explanation fields
  - mechanism
  - biological_pathway
  - interpretation
  - implications
  - supporting_marker_roles
- `meta.insight_graph`
- `report_v1`
- `root_cause_v1`
- `clinician_report_v1`
- `meta.explainability_report`
- `meta.burden_vector`
- `insights[]`
- system/group explainers
- biomarker educational explainers
- contribution-context fields
- any stable/reassuring system evidence already present
- any narrative-bearing data passed to Gemini
- any other governed text assets that materially contribute to explanation or interpretation

For each asset class, determine:

- where it lives
- how it is generated
- whether it is deterministic, compiler-shaped, or LLM-dependent
- whether it is currently surfaced anywhere
- whether it is rich, shallow, technical, or consumer-safe
- whether it is already good enough for direct or transformed user-facing use

---

### 2. Map what the current UX is actually surfacing

Map the current results experience section by section.

For each major visible section, identify:

- what the user currently sees
- which source field(s) it uses
- which component renders it
- whether richer data exists elsewhere but is not used
- whether the current weakness is caused by:
  - frontend surfacing
  - report/compiler contract
  - runtime narrative mode
  - or shallow source material

Sections to consider include, at minimum:

- hero interpretation
- trust strip / quality signals
- Why / lead hypothesis explanation
- stable / reassuring systems
- competing findings
- system groups
- biomarker evidence
- contribution context
- advanced analysis
- clinician report
- narrative summaries
- any current technical/meta surfaces

---

### 3. Identify what is genuinely underused

Make a grounded determination of which assets are currently underused.

Distinguish between:
- assets that are rich and governable but not surfaced
- assets that are surfaced but weakly transformed
- assets that are currently too shallow to support a premium UX even if surfaced
- assets that should remain internal/technical only

Be specific.
Do not say merely “there is more text in the system.”
State exactly which assets appear most valuable and underused.

---

### 4. Define the target user experience

This is the most important part.

Define what the user should walk away with after viewing a HealthIQ AI analysis.

Do not answer vaguely.

State concretely what a great user outcome looks like, for example:

- what they understand about their body overall
- what they understand about their strongest / most resilient systems
- what they understand about their most strained systems
- what they understand about how markers connect to each other
- what they understand about uncertainty and missing information
- what feels reassuring
- what feels important
- what feels surprising
- what feels educational
- what feels actionable
- what creates the “wow” factor

This section should answer:

**What should a user genuinely feel and understand after using HealthIQ AI?**

---

### 5. Propose the target layered explanation architecture

Define the target architecture for explanation and interpretation.

At minimum, describe the intended roles of:

#### Layer A — Analytical truth
The governed deterministic reasoning engine.

#### Layer B — Structured explanation contract
The report/compiler/explainability layer that translates analytical truth into structured explanation objects.

#### Layer C — Narrative shaping
What should remain deterministic, what should be compiler-shaped, and what — if anything — should be Gemini-polished.

#### Layer D — UX surfacing
Which sections should exist on the results page and what each should communicate.

For each proposed user-facing section, state:

- purpose
- source authority
- expected depth/tone
- what belongs there
- what does not belong there

---

### 6. Make the deterministic vs Gemini boundary explicit

Do not assume that more Gemini equals better UX.

Make an explicit recommendation for what should be:

- fully deterministic
- compiler-generated from deterministic assets
- Gemini-polished using governed structured inputs
- never delegated to Gemini

You must comment specifically on whether Gemini is currently being used in the right place and with the right inputs.

Also assess whether the current Gemini/narrative layer is:
- inactive
- underused
- poorly aimed
- or fundamentally fed the wrong material

---

### 7. Define the balanced narrative strategy

HealthIQ AI should not only tell users what is suboptimal.

It should also tell them what looks strong, stable, reassuring, or well-regulated where evidence supports that.

Your review must explicitly address:

- whether positive/reassuring system interpretation should become a first-class product layer
- which assets could support it
- how to avoid false reassurance
- how stronger systems should contextualise weaker ones
- how this contributes to trust and wow factor

---

### 8. Assess signal-library explanation strategy

Determine whether signal-library explanation fields should become a first-class narrative source.

Assess:

- whether they are suitable for direct use
- whether they should instead be compiler-fed
- whether they belong in:
  - hero
  - Why
  - system-group explanations
  - biomarker explainers
  - clinician report
  - Gemini prompt context
- which specific fields are most valuable
- what transformations are needed before surfacing them

---

### 9. Produce a gap analysis

Classify the main reasons the current UX falls short.

Use categories such as:

- surfacing gap
- contract gap
- compiler/report gap
- runtime narrative gap
- asset-governance gap
- product-definition gap

Be explicit about which problems are:
- “we already have the right data but do not use it”
- “we use the wrong layer”
- “we lack the right intermediate contract”
- “we do not yet have the right target experience definition”

---

### 10. End with a strategic recommendation and roadmap

Finish with a clear strategic recommendation that states:

- what the target explanatory UX should be
- which asset classes should power which layers
- what should be surfaced first
- what should remain hidden/internal
- what the recommended deterministic vs Gemini split is
- what sequence of architectural/product work should happen next

This must end in a practical next-step roadmap, not just themes.

---

## Important constraints

- Do not change code
- Do not write a sprint prompt
- Do not assume Gemini is the answer to everything
- Do not collapse all explanation into one generic “narrative” layer
- Do not speculate loosely without grounding your conclusions in actual repo/runtime structures
- Do not ignore governed assets just because the current frontend is weak
- Do not recommend surfacing raw technical/debug material directly to users without transformation

---

## Output format

Write the review as a structured architecture document with these sections:

1. Executive summary
2. Problem statement
3. Narrative / explanation asset inventory
4. Current UX surfacing map
5. Gap analysis
6. Target user experience definition
7. Proposed layered explanation architecture
8. Deterministic vs Gemini boundary
9. Balanced narrative strategy
10. Signal-library explanation strategy
11. Strategic recommendation
12. Sequenced roadmap / priority next steps

---

## Final standard

This review should help answer:

- what assets we already have
- which are valuable
- what the user should actually see
- what belongs in each UX layer
- and how HealthIQ AI becomes an experience that leaves the user thinking:

**“I understand my body in a far deeper way now.”**