# HealthIQ Intelligence Model Design — Second Pass Filled Decision Document

## Purpose

This document is the second-pass design decision pack for the HealthIQ intelligence model.

Its purpose is not to brainstorm broadly.  
Its purpose is to force the architectural decisions that must be made before target-schema design begins.

This is the final design checkpoint before a period of stable bulk ingestion.

The goal is not to produce a schema that never changes.  
The goal is to produce a schema with the right structural shape so future growth can happen additively rather than through destructive redesign.

This second pass is grounded in the platform direction set out in HealthIQ AI — Strategic Vision and 12-Month Sprint Plan v1.3 and aligned with KNOWLEDGE_BUS_SOP_v1.3. It also reflects the current operating principle that intelligence must remain deterministic, auditable, and structurally governed rather than inferred loosely in narrative.

---

## Core framing

We are not asking:

- what fields do we currently have?
- what fits most easily into the current files?
- what is the smallest schema we can get away with?

We are asking:

- what intelligence must the platform support downstream?
- what upstream knowledge must exist to make that intelligence possible?
- which knowledge primitives must be shaped correctly now to avoid future rewrite pain?

The schema must serve the intelligence model.  
The intelligence model must not be squeezed into a convenient file format.

---

## What this pack must decide

By the end of this review we want clear decisions on:

1. what a contradiction marker actually is in the reasoning model
2. what the minimum viable longitudinal primitives are
3. how every upstream knowledge primitive should be triaged
4. what belongs in the first target schema version
5. what must have a schema home now even if it is not populated yet
6. what can genuinely be deferred
7. which structural choices would create future rewrite traps if we get them wrong now

---

# Section 1 — Contradiction marker decision

## Why this matters

Contradiction markers are currently recognised as important, but not yet well-defined enough to place into schema.

Until we define what they do in reasoning terms, we cannot model them correctly.

## Working table

| Question | Decision | Why |
|---|---|---|
| What is a contradiction marker? | A contradiction marker is a structured evidence item that weakens, challenges, or opposes a specific explanation or interpretive path. | It must be more than “negative evidence in prose.” It is a reasoning primitive. |
| What does it do to reasoning? | In v1 it reduces confidence in a hypothesis and may elevate alternative hypotheses, but it does not hard-suppress reasoning on its own unless explicitly paired with a rule-level exclusion. | This gives immediate practical value without forcing an over-complex suppression engine into v1. |
| What object does it attach to? | It attaches primarily to a hypothesis object, not to the signal globally. | Contradiction is explanation-specific. The same marker can weaken one hypothesis while strengthening another. |
| Is it single-hypothesis or multi-hypothesis? | The marker instance should be referenceable by multiple hypotheses, but its contradiction effect should be expressed per hypothesis. | The same real-world marker can play different roles depending on the explanation being evaluated. |
| What is the minimum viable v1 structure? | Hypothesis-level contradiction objects with marker reference, contradiction rationale, and contradiction strength/type. | This is the smallest useful shape that avoids future redesign. |

## Output required

**Decision statement**

> A contradiction marker is defined as a structured evidence item that weakens or challenges a specific explanation.  
> In v1 it will reduce confidence in a hypothesis and help differential ranking, but will not act as a global hard-stop unless an explicit rule later authorises that behaviour.  
> It will attach to hypothesis objects.  
> It will affect reasoning by recording explanation-specific counter-evidence in a first-class, structured way.

## Additional design note

Contradiction must not be hidden inside generic narrative such as “however…” or “despite…”.  
If it affects ranking, confidence, or defensibility, it is part of the reasoning model and needs structured representation.

---

# Section 2 — Longitudinal primitive decision

## Why this matters

Longitudinal reasoning is strategically important, but a full longitudinal intelligence model is too large to design inside the first target-schema sprint.

We therefore need to decide the minimum viable longitudinal primitives that must exist now.

This also needs to stay aligned with the roadmap direction that repeated panels, intervention tracking, and trajectories are part of the dataset moat, while the first platform year remains focused on building a strong deterministic engine first, as stated in HealthIQ AI — Strategic Vision and 12-Month Sprint Plan v1.3.

## Working table

| Longitudinal concept | Needed now? | Needs schema home now? | Can defer fully? | Why |
|---|---|---|---|---|
| Stable identity key | Yes | Yes | No | Without identity continuity, repeat-panel interpretation cannot exist coherently. |
| Snapshot timestamp | Yes | Yes | No | Required for sequencing panels in time. |
| Signal-state snapshot | Yes | Yes | No | This is the minimum meaningful longitudinal unit for structured comparison. |
| Trend / trajectory | No | Yes | No | Not required to populate in v1, but schema must be able to grow into it without redesign. |
| Delta significance | No | Yes | No | Later-important for meaningful change detection; omission of a schema home now would create future pain. |
| Intervention linkage | No | Yes | No | Not needed for initial population, but strategically important enough that it should have a defined home now. |
| Phenotype movement over time | No | Yes | No | Future-important for the metabolic platform vision. |
| Time-aware confidence adjustment | No | No | Yes | Valuable later, but not essential to shape now. |

## Output required

**Decision statement**

> The minimum longitudinal primitives for v1 are: stable identity key, snapshot timestamp, and signal-state snapshot.  
> These are sufficient because they allow the platform to recognise the same person across time, place observations in sequence, and compare structured signal states between panels.  
> The following longitudinal capabilities are deferred from active population in v1 but must have schema homes now: trend / trajectory, delta significance, intervention linkage, and phenotype movement over time.  
> Time-aware confidence adjustment is deferred fully.

## Additional design note

The minimum viable longitudinal model is not “full progress intelligence.”  
It is just enough continuity to avoid having to rebuild the object model later when repeated panels become central.

---

# Section 3 — Upstream knowledge primitive triage

## Why this matters

The first-pass exercise surfaced a large number of upstream knowledge primitives.  
That list is too large to move straight into schema design without triage.

We now need to force every primitive into one of three buckets:

1. required for correct reasoning now
2. required for correct reasoning later, but the schema must have a home for it now
3. genuinely deferrable

## Complete triage table

| Primitive | Short definition | Triage bucket | Why |
|---|---|---|---|
| Primary biomarker | The main marker anchoring the signal or explanation | Required now | Core reasoning cannot work without it. |
| Trigger direction | Whether the marker matters when high, low, rising, etc. | Required now | Necessary for deterministic rule evaluation. |
| Supporting biomarker object | Structured representation of an additional evidentiary marker | Required now | Flat lists are too weak for future reasoning. |
| Supporting biomarker role | Role such as support, corroboration, severity, differential, contradiction | Required now | Reasoning quality depends on role separation. |
| Supporting biomarker directionality | Direction in which the supporting marker supports the interpretation | Required now | Needed for precise rule logic. |
| Supporting biomarker rationale | Why that marker supports the interpretation | Required later, schema home now | Important for transparency and auditability, but not every v1 object must be fully populated. |
| Supporting biomarker availability | Whether a marker is present, absent, missing, or unavailable | Required now | Missing-data handling requires this. |
| Mechanism relationships | Links explaining physiological mechanism | Required later, schema home now | Important for future depth and pathway reasoning. |
| Corroboration relationships | Links that strengthen an interpretation without being primary | Required now | Needed for strong explanation quality. |
| Severity relationships | Markers that help distinguish magnitude or seriousness | Required now | Severity is part of a strong answer, not a later luxury. |
| Differential relationships | Markers that distinguish between competing explanations | Required now | Differential reasoning is part of real intelligence. |
| Contradiction markers | Structured counter-evidence against a hypothesis | Required now | Must be first-class from the start. |
| Confirmatory tests | Suggested next tests that would clarify interpretation | Required now | Strong downstream answers need next-step value. |
| Evidence source list | Source references supporting a rule or interpretation | Required later, schema home now | Important for defensibility and future audit. |
| Rule-level provenance | Structured provenance tied to a specific rule or explanation primitive | Required later, schema home now | Must have a governed home even if lightly populated initially. |
| Evidence strength | Strength of support for a claim or hypothesis | Required now | Needed for defensible ranking and communication. |
| Physiological claim | The core biological claim being made | Required now | Without it, the model has no semantic centre. |
| Threshold notes | Notes on threshold interpretation or nuance | Required later, schema home now | Needed for future nuance but can start lightly. |
| Caveats / confounders | Factors that may weaken or distort interpretation | Required now | Clinically important and central to trust. |
| Medication effects | Medication-related interpretation caveats or confounding effects | Required later, schema home now | The roadmap already treats medication as governed context; schema should not force redesign later. |
| Context input interpretation rules | Rules linking structured context inputs to interpretation | Required later, schema home now | Core to the governed context direction, but can mature in staged fashion. |
| Missing-data primitives | Structured representation of missingness and its consequences | Required now | Intelligence without missing-data logic is brittle and misleading. |
| Hypothesis objects | Structured candidate explanations | Required now | Explanation cannot remain a blob. |
| Ranked differential explanations | Ordered competing hypotheses | Required now | Strong answers require ranking, not just one narrative. |
| Pathway / system membership | Membership of a signal / marker / explanation in a pathway or system | Required later, schema home now | Important for future systems-level reasoning. |
| Phenotype relationships | Links between explanations/signals and phenotype states | Required later, schema home now | Important for later platform and buyer value. |
| Longitudinal identity | Stable identity reference across time | Required later, schema home now | Needed for future longitudinal intelligence; can be defined now and populated later. |
| Signal-state snapshot | Structured signal state at a moment in time | Required later, schema home now | Needed to support longitudinal growth without redesign. |
| Intervention tracking | Structured actions taken between panels | Required later, schema home now | Strategically critical later; not required for first reasoning release. |
| Provenance / authorship metadata | Metadata about origin, authorship, versioning, review | Required later, schema home now | Not required for correct reasoning in v1, but a governed schema home should exist now so future provenance, authorship, and audit metadata can be added without structural redesign. |

## Triage summary

### Bucket 1 — Required for correct reasoning now
- primary biomarker
- trigger direction
- supporting biomarker object
- supporting biomarker role
- supporting biomarker directionality
- supporting biomarker availability
- corroboration relationships
- severity relationships
- differential relationships
- contradiction markers
- confirmatory tests
- evidence strength
- physiological claim
- caveats / confounders
- missing-data primitives
- hypothesis objects
- ranked differential explanations

### Bucket 2 — Required later, but schema must have a home now
- supporting biomarker rationale
- mechanism relationships
- evidence source list
- rule-level provenance
- threshold notes
- medication effects
- context input interpretation rules
- pathway / system membership
- phenotype relationships
- longitudinal identity
- signal-state snapshot
- intervention tracking
- trend / trajectory
- delta significance
- phenotype movement over time

### Bucket 3 — Genuinely deferrable
- time-aware confidence adjustment
- richer provenance / authorship metadata beyond minimal versioning requirements

---

# Section 4 — Full intelligence target vs v1 target schema

## Why this matters

We need a clean separation between:
- what the platform should ultimately become
- what the first target schema version must support

Without this, the next sprint will either become too thin or too broad.

## Reconciled table

| Primitive | Part of full intelligence target? | Must exist in v1 schema? | Must be populated in v1? | Why |
|---|---|---|---|---|
| Primary biomarker | Yes | Yes | Yes | Core anchor of interpretation. |
| Trigger direction | Yes | Yes | Yes | Needed for rule logic. |
| Supporting biomarker object | Yes | Yes | Yes | Prevents flat-list modelling trap. |
| Supporting biomarker role | Yes | Yes | Yes | Needed for explanation quality. |
| Supporting biomarker directionality | Yes | Yes | Yes | Needed for precise interpretation. |
| Supporting biomarker rationale | Yes | Yes | No | Schema should support it early; population can grow over time. |
| Corroboration relationships | Yes | Yes | Yes | Core to defensible support. |
| Severity relationships | Yes | Yes | Yes | Needed for strong answer quality. |
| Differential relationships | Yes | Yes | Yes | Must be first-class in v1. |
| Contradiction markers | Yes | Yes | Yes | Core reasoning primitive. |
| Confirmatory tests | Yes | Yes | Yes | Immediate clinical/business value. |
| Evidence strength | Yes | Yes | Yes | Needed for ranking and confidence communication. |
| Physiological claim | Yes | Yes | Yes | Semantic core of reasoning. |
| Caveats / confounders | Yes | Yes | Yes | Critical for trust and defensibility. |
| Missing-data primitives | Yes | Yes | Yes | Prevents false certainty. |
| Hypothesis objects | Yes | Yes | Yes | Explanation must be structured. |
| Ranked differential explanations | Yes | Yes | Yes | Single-explanation blob is not acceptable. |
| Evidence source list | Yes | Yes | No | Home needed now for future defensibility. |
| Rule-level provenance | Yes | Yes | No | Home needed now to avoid later surgery. |
| Threshold notes | Yes | Yes | No | Needed later, not always v1-populated. |
| Medication effects | Yes | Yes | No | Home needed because governed context workstream is already in the roadmap. |
| Context input interpretation rules | Yes | Yes | No | Same reason as above. |
| Pathway / system membership | Yes | Yes | No | Home needed for future systems biology layer. |
| Phenotype relationships | Yes | Yes | No | Important later for platform-scale intelligence. |
| Longitudinal identity | Yes | Yes | No | Home needed now. |
| Signal-state snapshot | Yes | Yes | No | Home needed now. |
| Intervention tracking | Yes | Yes | No | Home needed now. |
| Provenance / authorship metadata | Yes | Yes | No | Not required for immediate reasoning output, but the schema should reserve a governed home now for future provenance and authorship metadata. |

## Reconciled decision

The v1 target schema must be **structurally broader** than v1 population.  
That is not overengineering. That is avoiding predictable rewrite traps.

The correct rule is:

- if a primitive is part of the believable full intelligence target
- and omission of a schema home now would likely force destructive redesign later

then it must have a schema home in v1 even if it is initially empty or lightly populated.

---

# Section 5 — Structural risk check

## Why this matters

Future schema pain is usually caused by wrong structural assumptions, not missing fields.

We need to identify where the current design thinking is still at risk of creating destructive rewrite traps.

## Working table

| Potential structural risk | Why it is risky | Action needed now? |
|---|---|---|
| Supporting markers modelled too simply | Flat lists cannot represent role, directionality, contradiction, or severity cleanly. | Yes — supporting markers must be objects. |
| Explanation object too thin | A single explanation blob will collapse mechanism, evidence, severity, and differential into prose. | Yes — explanation must support structured hypotheses. |
| Differential reasoning not first-class | Without first-class differential structure, ranking logic ends up hidden in narrative. | Yes — must be explicit in schema. |
| Contradiction markers not attached clearly | Ambiguous attachment level causes brittle future logic and poor auditability. | Yes — attach to hypotheses in v1. |
| Provenance lacks a governed home | Future defensibility and audit become messy retrofits. | Yes — provide a schema home now. |
| Missing-data logic has no home | Missingness will be handled informally and inconsistently. | Yes — must be modelled explicitly. |
| Longitudinal identity not defined | Repeat-panel intelligence later will force cross-cutting redesign. | Yes — define a schema home now. |
| Context inputs treated as loose narrative | This would conflict with the roadmap’s governed context direction and create later overlay redesign. | Yes — define a schema home and interpretation-rule home now. |
| Reasoning and rendering fields mixed together | UI/reporting needs will distort the reasoning model. | Yes — separate reasoning objects from presentation objects. |
| Single-value fields used where one-to-many is inevitable | Future growth would require object breakage and data migration. | Yes — design for one-to-many where structurally obvious. |

## Structural rewrite risks that must be eliminated before schema design begins

1. Supporting markers must not be modelled as flat strings or flat IDs.
2. Explanation must not be modelled as one prose blob.
3. Differential reasoning must not be implicit.
4. Contradiction must not be hidden in narrative.
5. Provenance must not be left homeless.
6. Missing-data logic must not be informal.
7. Longitudinal continuity must not be bolted on later.
8. Context interpretation must not remain a free-text side-channel.
9. Rendering concerns must not distort reasoning structure.

---

# Section 6 — Guardrails for target schema design

## Why this matters

The next schema sprint needs hard design guardrails so that good intentions do not collapse into convenience modelling.

## Working table

| Guardrail | Decision | Why |
|---|---|---|
| Supporting markers must be objects | Yes | Flat lists are structurally dishonest for the intelligence target. |
| Multiple hypotheses must be supported | Yes | Real reasoning requires alternatives, not one explanation blob. |
| Provenance must have a governed home | Yes | Future defensibility and audit require it. |
| Contradiction reasoning must be first-class | Yes | It materially affects confidence and ranking. |
| Bucket-2 primitives must have schema homes | Yes | This is the main protection against rewrite pain. |
| Reasoning objects must be separate from rendering objects | Yes | The intelligence model must not be shaped by report formatting needs. |

## Final non-negotiable schema design guardrails

1. Supporting markers are always objects, never just flat lists.
2. Explanations must support multiple hypotheses.
3. Differential reasoning is first-class.
4. Contradiction is first-class.
5. Missing-data logic has a structured home.
6. Provenance has a governed home.
7. Bucket-2 primitives must have schema homes in v1.
8. Longitudinal continuity primitives must have schema homes in v1.
9. Context interpretation primitives must have schema homes in v1.
10. Reasoning objects and rendering objects must remain separate.

---

# Section 7 — Final decision summary

## Working table

| Decision area | Status | Notes |
|---|---|---|
| Contradiction marker definition | Agreed | Hypothesis-level, confidence-reducing counter-evidence object. |
| Longitudinal minimum | Agreed | Stable identity key, snapshot timestamp, signal-state snapshot. |
| Primitive triage | Agreed | All major primitives assigned across the three buckets. |
| Full target vs v1 reconciliation | Agreed | v1 schema broader than v1 population. |
| Structural risk check | Agreed | Main rewrite traps identified and addressed. |
| Schema design guardrails | Agreed | Non-negotiable guardrails listed. |
| Ready for target-schema sprint | Yes, with discipline | The next sprint can be authored if it honours these decisions. |

## Final decision statement

This second pass concludes that the target schema must be shaped around structured reasoning objects rather than around current file convenience or renderer needs. Contradiction, differential reasoning, missing-data logic, and multi-hypothesis explanation are not optional enrichments; they are part of the minimum honest shape of the intelligence model. Longitudinal and governed-context primitives do not need full population immediately, but they do need explicit schema homes now because the strategic direction of the platform already commits to those capabilities, as set out in HealthIQ AI — Strategic Vision and 12-Month Sprint Plan v1.3.

The team is therefore ready to author the target-schema sprint, provided the sprint is explicitly constrained by the decisions and guardrails in this document.

---

## Suggested next-step instruction for the schema sprint

The next sprint should not attempt to populate every future primitive fully.

The sprint must treat validator enforcement as a first-class deliverable alongside schema design, so the new structural rules are governed rather than advisory.

It should do four things well:

1. define the core reasoning object model correctly
2. provide explicit homes for bucket-2 primitives
3. keep rendering concerns separate from reasoning concerns
4. avoid structural shortcuts that create future rewrite pressure

---

## Final reminder

The purpose of this exercise is not to be exhaustive for its own sake.

The purpose is to ensure that the **shape** of the intelligence model is correct before the next stable ingestion era begins.

A missing field later is survivable.  
A wrongly shaped core object is expensive.