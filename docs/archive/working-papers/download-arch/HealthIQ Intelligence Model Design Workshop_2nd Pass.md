# HealthIQ Intelligence Model Design — Second Pass Review Pack

## Purpose

This document is the second-pass design pack for the HealthIQ intelligence model.

Its purpose is not to brainstorm broadly.  
Its purpose is to force the architectural decisions that must be made before target-schema design begins.

This is the final design checkpoint before a period of stable bulk ingestion.

The goal is not to produce a schema that never changes.  
The goal is to produce a schema with the right structural shape so future growth can happen additively rather than through destructive redesign.

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

## Section 1 — Contradiction marker decision

### Why this matters

Contradiction markers are currently recognised as important, but not yet well-defined enough to place into schema.

Until we define what they do in reasoning terms, we cannot model them correctly.

### Questions to answer

1. What is a contradiction marker?
2. Does a contradiction marker:
   - reduce confidence only?
   - suppress a specific hypothesis?
   - redirect toward an alternative explanation?
   - do more than one of the above?
3. Is contradiction attached to:
   - a signal
   - a hypothesis
   - a supporting marker
   - a rule
   - another object
4. Can one contradiction marker apply to multiple possible explanations?
5. What is the minimum viable structure needed in v1?

### Working table

| Question | Decision | Why |
|---|---|---|
| What is a contradiction marker? | | |
| What does it do to reasoning? | | |
| What object does it attach to? | | |
| Is it single-hypothesis or multi-hypothesis? | | |
| What is the minimum viable v1 structure? | | |

### Output required

A short decision statement:

> “A contradiction marker is defined as…  
> In v1 it will…  
> It will attach to…  
> It will affect reasoning by…”

---

## Section 2 — Longitudinal primitive decision

### Why this matters

Longitudinal reasoning is strategically important, but a full longitudinal intelligence model is too large to design inside the first target-schema sprint.

We therefore need to decide the minimum viable longitudinal primitives that must exist now.

### Questions to answer

1. What is the minimum longitudinal structure required now?
2. Do we agree that v1 only needs:
   - stable identity key
   - snapshot timestamp
   - signal-state snapshot
3. What additional longitudinal concepts are explicitly out of scope for v1?
4. Which later longitudinal capabilities should the schema be able to grow into without redesign?

### Working table

| Longitudinal concept | Needed now? | Needs schema home now? | Can defer fully? | Why |
|---|---|---|---|---|
| Stable identity key | | | | |
| Snapshot timestamp | | | | |
| Signal-state snapshot | | | | |
| Trend / trajectory | | | | |
| Delta significance | | | | |
| Intervention linkage | | | | |
| Phenotype movement over time | | | | |
| Time-aware confidence adjustment | | | | |

### Output required

A short decision statement:

> “The minimum longitudinal primitives for v1 are…  
> These are sufficient because…  
> The following longitudinal capabilities are deferred…”

---

## Section 3 — Upstream knowledge primitive triage

### Why this matters

The first-pass exercise surfaced a large number of upstream knowledge primitives.  
That list is too large to move straight into schema design without triage.

We now need to force every primitive into one of three buckets:

1. required for correct reasoning now
2. required for correct reasoning later, but the schema must have a home for it now
3. genuinely deferrable

### Triage rule

Use the following definitions:

- **Required for correct reasoning now**  
  The platform cannot produce acceptable intelligence in early production without this primitive.

- **Required for correct reasoning later, but schema must have a home for it now**  
  It does not need to be populated or fully used in v1, but if we do not define its place in the model now, future implementation will force structural redesign under pressure.

- **Genuinely deferrable**  
  The primitive can be omitted from both population and schema v1 without causing architectural dishonesty or likely redesign pain.

### Working table

| Primitive | Short definition | Triage bucket | Why |
|---|---|---|---|
| Primary biomarker | | | |
| Trigger direction | | | |
| Supporting biomarker object | | | |
| Supporting biomarker role | | | |
| Supporting biomarker directionality | | | |
| Supporting biomarker rationale | | | |
| Supporting biomarker availability | | | |
| Mechanism relationships | | | |
| Corroboration relationships | | | |
| Severity relationships | | | |
| Differential relationships | | | |
| Contradiction markers | | | |
| Confirmatory tests | | | |
| Evidence source list | | | |
| Rule-level provenance | | | |
| Evidence strength | | | |
| Physiological claim | | | |
| Threshold notes | | | |
| Caveats / confounders | | | |
| Medication effects | | | |
| Context input interpretation rules | | | |
| Missing-data primitives | | | |
| Hypothesis objects | | | |
| Ranked differential explanations | | | |
| Pathway / system membership | | | |
| Phenotype relationships | | | |
| Longitudinal identity | | | |
| Signal-state snapshot | | | |
| Intervention tracking | | | |
| Provenance / authorship metadata | | | |

Add rows if needed.

### Output required

A complete triage table with every primitive assigned and justified.

---

## Section 4 — Full intelligence target vs v1 target schema

### Why this matters

We need a clean separation between:
- what the platform should ultimately become
- what the first target schema version must support

Without this, the next sprint will either become too thin or too broad.

### Working table

| Primitive | Part of full intelligence target? | Must exist in v1 schema? | Must be populated in v1? | Why |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |

### Output required

A single reconciled view of:
- full target
- v1 schema commitment
- v1 population commitment

---

## Section 5 — Structural risk check

### Why this matters

Future schema pain is usually caused by wrong structural assumptions, not missing fields.

We need to identify where the current design thinking is still at risk of creating destructive rewrite traps.

### Questions to ask

1. Are we modelling any object too simply?
2. Are we still treating anything as a single value that should really be one-to-many?
3. Are we keeping important reasoning primitives in prose that should be structured?
4. Are we attaching knowledge to the wrong level of the model?
5. Are any future-important primitives still missing a defined home?

### Working table

| Potential structural risk | Why it is risky | Action needed now? |
|---|---|---|
| Supporting markers modelled too simply | | |
| Explanation object too thin | | |
| Differential reasoning not first-class | | |
| Contradiction markers not attached clearly | | |
| Provenance lacks a governed home | | |
| Missing-data logic has no home | | |
| Longitudinal identity not defined | | |

Add rows as needed.

### Output required

A shortlist of structural rewrite risks that must be eliminated before schema design begins.

---

## Section 6 — Guardrails for target schema design

### Why this matters

The next schema sprint needs hard design guardrails so that good intentions do not collapse into convenience modelling.

### Proposed guardrail questions

1. Must supporting markers always be objects rather than flat lists?
2. Must explanation support multiple hypotheses rather than one explanation blob?
3. Must provenance have a governed home?
4. Must contradiction and differential reasoning be first-class rather than hidden in prose?
5. Must every primitive in bucket 2 have an explicit schema home now?
6. Must rendering-oriented fields be separated from reasoning-oriented fields?

### Working table

| Guardrail | Decision | Why |
|---|---|---|
| Supporting markers must be objects | | |
| Multiple hypotheses must be supported | | |
| Provenance must have a governed home | | |
| Contradiction reasoning must be first-class | | |
| Bucket-2 primitives must have schema homes | | |
| Reasoning objects must be separate from rendering objects | | |

### Output required

A final list of non-negotiable schema design guardrails.

---

## Section 7 — Final decision summary

This section should be completed only after the rest of the pack is done.

### Required summary

1. Contradiction marker definition agreed?
2. Longitudinal minimum agreed?
3. Primitive triage complete?
4. Full target vs v1 reconciliation complete?
5. Structural rewrite risks identified?
6. Schema design guardrails agreed?
7. Are we ready to author the target-schema sprint?

### Working table

| Decision area | Status | Notes |
|---|---|---|
| Contradiction marker definition | | |
| Longitudinal minimum | | |
| Primitive triage | | |
| Full target vs v1 reconciliation | | |
| Structural risk check | | |
| Schema design guardrails | | |
| Ready for target-schema sprint | | |

---

## Suggested workshop sequence

1. Reconfirm the purpose of the second pass
2. Resolve contradiction marker definition
3. Resolve longitudinal minimum
4. Triage all knowledge primitives
5. Reconcile full target vs v1 schema
6. Review structural risks
7. Freeze schema design guardrails
8. Decide whether the schema sprint can now be authored

---

## Suggested success criteria

This second pass is successful only if:

- contradiction markers are defined in reasoning terms
- minimum longitudinal primitives are agreed
- every important primitive has been triaged
- there is a clear distinction between full target and v1 schema
- future rewrite traps have been identified and addressed
- the next schema sprint can be authored without broad ambiguity

---

## Final reminder

The purpose of this exercise is not to be exhaustive for its own sake.

The purpose is to ensure that the **shape** of the intelligence model is correct before the next stable ingestion era begins.

A missing field later is survivable.  
A wrongly shaped core object is expensive.

This review exists to prevent the second problem.