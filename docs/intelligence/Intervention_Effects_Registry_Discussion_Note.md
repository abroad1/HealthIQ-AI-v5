# HealthIQ Discussion Note — Intervention-Effects Registry

## Purpose

This note sets out a proposed approach for how HealthIQ should model intervention effects without turning the platform into a drug library.

The aim is to agree:
- where intervention knowledge should live in the architecture
- what the minimum v1 intervention-effects registry should contain
- how that registry should relate to user intervention records
- how it should be governed
- how it should connect to longitudinal interpretation

This is a discussion document for review and agreement by the team.

It is not yet a final schema specification.

---

## The problem we are trying to solve

HealthIQ needs to reason about interventions because they materially affect biomarker interpretation.

Examples:
- a statin may lower LDL
- corticosteroids may raise glucose
- creatine may raise creatinine without renal disease
- stopping alcohol may lower GGT over time
- reducing weight may improve HbA1c over time
- stopping a medication may allow a biomarker to drift back in the opposite direction

Without a governed intervention model, the platform will struggle to answer questions such as:
- is this abnormality disease-driven or intervention-driven?
- what changed between this panel and the previous one?
- is the observed movement directionally consistent with a prescribed intervention?
- should the leading hypothesis be weakened because of a known confounding exposure?
- does stopping an intervention explain a worsening biomarker trend?

---

## The key boundary

HealthIQ should not become a drug library.

We do not need:
- a full pharmaceutical database
- every brand name drug
- every dosing formulation
- exhaustive pharmacology

That is not the product and it would be a major distraction.

What we do need is:
- a small, governed set of intervention-effect knowledge relevant to the biomarkers and hypotheses the platform interprets

This means:
- class-level knowledge
- not drug-library-level knowledge

Examples:
- statin class
- corticosteroid class
- thyroid hormone replacement
- metformin class
- oral contraceptive / hormone therapy class
- creatine supplementation
- alcohol reduction
- exercise increase
- major dietary change

The platform only needs intervention-effect knowledge where it materially changes biomarker interpretation.

---

## The first major architecture decision

### Option A — Put intervention knowledge inside hypothesis caveat objects
In this model, intervention effects are attached directly to biomarker hypotheses or caveat lists.

#### Advantages
- reasoning links are very local
- easy to understand at first glance

#### Problems
- duplicates the same intervention logic across many hypotheses
- hard to maintain
- difficult to update globally
- risks drift and inconsistency
- becomes bloated as more biomarkers and hypotheses are added

### Option B — Create a separate intervention-effects registry
In this model, intervention-effect knowledge is stored centrally in a governed registry and linked into reasoning when needed.

#### Advantages
- reusable across many biomarkers and hypotheses
- easier to maintain
- avoids duplication
- cleaner separation of concepts
- easier to govern
- easier to extend later

#### Problems
- requires a linking model
- slightly more abstract than embedding everything directly in hypotheses

### Recommendation
Option B is preferred.

HealthIQ should use a separate intervention-effects registry.

---

## The second major architecture decision

If we create a separate intervention-effects registry, where should it live?

### Option A — Outside the Knowledge Bus as a separate governed asset
#### Advantages
- lighter operational footprint
- easier to change independently

#### Problems
- risks becoming a side-table with weaker governance
- needs a separate governance model
- easier for drift to emerge between intervention logic and KB reasoning

### Option B — Inside the Knowledge Bus as a governed registry asset
#### Advantages
- strong governance
- versioned and reviewable
- aligns with existing registry-style architecture patterns
- easier to keep consistent with signal and hypothesis reasoning
- fits the broader deterministic knowledge model

#### Problems
- adds governance overhead
- requires clear rules for how registry changes are promoted

### Recommendation
Option B is preferred.

The intervention-effects registry should live inside the Knowledge Bus as a governed registry asset.

This does not mean it should be embedded inside every signal package.  
It means it should be governed within the KB architecture, with its own schema, validator, and promotion discipline.

---

## Proposed high-level architecture

### Layer 1 — Knowledge Bus intervention-effects registry
This holds canonical knowledge about intervention classes and biomarker effects.

Example knowledge:
- statin class lowers LDL
- statin cessation may allow LDL to rise over time
- corticosteroids may raise glucose
- creatine supplementation may raise creatinine without kidney injury
- alcohol reduction may lower GGT over time

This is class-level and governed.

### Layer 2 — User intervention / exposure records
This holds the user’s actual live state and timeline.

Examples:
- atorvastatin started 3 months ago
- creatine supplement started 2 weeks ago
- alcohol use reduced from daily to weekends only
- metformin dose doubled 6 weeks ago
- new exercise programme started 1 month ago

This is user-specific and time-dependent.

### Layer 3 — Reasoning / linking logic
This combines:
- canonical intervention-effect knowledge
- the user’s actual intervention history
- the biomarker and hypothesis layer

to answer:
- is this likely confounded?
- is this direction of change expected?
- is the timing plausible?
- should disease confidence be reduced?
- should monitoring be suggested?

---

## What the intervention-effects registry is not

It is not:
- a drug library
- a medication lookup service
- a complete formulary
- a complete supplement encyclopedia
- a general-purpose pharmacology dataset

It is a small class-level reasoning registry for biomarker interpretation.

That boundary must remain explicit.

---

## Proposed minimum v1 registry scope

The v1 intervention-effects registry should only cover classes that materially affect the biomarkers in the panels the product actually interprets.

Likely examples for v1:
- statin class
- metformin class
- corticosteroid class
- thyroid hormone replacement
- oral contraceptive / hormone therapy class
- diuretic class
- antihypertensive classes where materially relevant
- creatine supplementation
- alcohol reduction / increase
- major exercise change
- major dietary change
- smoking change where directly relevant

The final list should be driven by biomarker relevance, not drug-catalog completeness.

---

## Proposed minimum v1 fields for the intervention-effects registry

Each registry entry should have at least:

### Identity and governance
- intervention class ID
- intervention class name
- intervention type  
  (medication / supplement / lifestyle / behavioural / clinical)

### Interpretation relevance
- biomarkers affected
- expected direction of effect
- broad effect type  
  (confounder / therapeutic effect / monitoring implication / adverse-effect relevance)

### Timing
- expected onset / lag to effect
- expected cessation / reversal effect
- approximate persistence if known

### Evidence / confidence
- evidence strength
- physiological rationale
- source / provenance references

### Monitoring / reasoning relevance
- monitoring significance if applicable
- caveat notes if applicable
- hypotheses or systems likely to be affected

---

## Important addition: cessation effects

Cessation effects should be part of v1.

This is important because many interventions influence biomarkers in two ways:
- when started
- when stopped

Examples:
- stopping statins may allow LDL to rise again
- stopping corticosteroids may alter glucose and inflammatory patterns
- stopping thyroid replacement may shift thyroid markers over time
- stopping alcohol may improve GGT and related liver markers over time

Without cessation effects, longitudinal reasoning will miss a clinically important class of explanations.

---

## Relationship to the user intervention / exposure schema

The intervention-effects registry does not replace the user intervention model.

The registry holds canonical class-level knowledge.  
The user intervention schema holds actual user-level records.

### User intervention record examples
- atorvastatin 20 mg daily started 2026-01-01
- creatine supplement started 2026-02-10
- alcohol intake reduced on 2026-03-01
- metformin dose increased on 2026-04-15

Those user records should then map to intervention classes in the registry:
- atorvastatin -> statin class
- creatine -> creatine supplementation
- reduced alcohol -> alcohol reduction
- metformin -> metformin class

This is how the platform stays useful without becoming a drug database.

---

## Relationship to the KB hypothesis layer

The hypothesis layer should not duplicate full intervention knowledge.

Instead:
- hypotheses should be able to reference or consume intervention registry knowledge
- intervention classes can weaken, caveat, or contextualise hypotheses
- the registry should remain the canonical source for intervention effects

This preserves reuse and avoids duplication.

---

## Relationship to BE-S0 lifestyle/context work

There is a potential overlap between:
- lifestyle/context inputs
- intervention / exposure records

This must be handled deliberately.

### Proposed principle
BE-S0-style lifestyle/context inputs and intervention records should be treated as related but not identical.

#### Example
- “Typical alcohol intake” may be a context input
- “Alcohol intake reduced significantly 6 weeks ago” is an intervention event

So:
- static or baseline lifestyle descriptors may remain in context
- discrete changes with longitudinal relevance should be represented as intervention/exposure records

This prevents duplication while still supporting longitudinal reasoning.

---

## Key questions for team agreement

1. Do we agree that intervention effects should live in a separate registry rather than inside hypothesis caveat objects?
2. Do we agree that the registry should live inside the Knowledge Bus as a governed registry asset?
3. Do we agree that the registry should remain class-level rather than drug-library-level?
4. Do we agree that cessation effects belong in the minimum v1 model?
5. What intervention classes are in scope for v1?
6. What minimum fields must each registry entry contain?
7. How should intervention classes link back into biomarker/hypothesis reasoning?
8. Where do we draw the boundary between lifestyle context and lifestyle intervention events?
9. What mapping approach should be used from user-entered intervention names to registry classes?
10. What parts of intervention modelling belong in v1 versus later enrichment?

---

## Risks if we get this wrong

If we model this badly, likely failure modes include:
- HealthIQ drifting toward a drug library
- duplicated intervention logic across many hypotheses
- poor longitudinal explanation of biomarker movement
- inability to distinguish confounding from disease progression
- schema contamination between canonical knowledge and live user state
- future redesign when intervention-aware reasoning becomes unavoidable

---

## Provisional recommendation

The current recommendation for team review is:

1. create a separate intervention-effects registry
2. govern it inside the Knowledge Bus
3. keep it class-level, not drug-library-level
4. include cessation effects in v1
5. keep user intervention/exposure records in a separate user-state schema
6. link the two through reasoning logic rather than embedding intervention data directly inside biomarker packages

---

## Proposed next step

If the team broadly agrees with this direction, the next step should be:

define the minimum v1 intervention-effects registry contract, including:
- entry identity
- class-level scope
- effect directions
- onset / lag
- cessation effects
- evidence fields
- linking model to hypotheses and user intervention records

---

## Summary in one sentence

The recommended model is a small class-level intervention-effects registry governed inside the Knowledge Bus, linked to separate user intervention/exposure records, so HealthIQ can reason about medications, supplements, and lifestyle changes without becoming a drug library.