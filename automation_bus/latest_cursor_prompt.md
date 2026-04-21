---
work_id: N-7
branch: feature/n-7-governed-interpretation-assets-ab-benchmark
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# N-7 — New governed interpretation assets for the benchmark AB case

## Objective

Create the missing governed interpretation entities needed to support the benchmark AB narrative deterministically, using the new narrative-support stack already built in N-3 through N-6.

This is a CONTENT sprint.
It is not a frontend sprint.
It is not a compiler implementation sprint.
Do not modify backend analytical logic unless a tiny validation/registry touch is strictly required and justified.
Do not widen into narrative assembly.

The purpose of N-7 is to create the governed interpretation entities that later compiler work will compose into benchmark-grade narrative output.

---

## Strategic context already settled

The following are already decided and are not open for reinterpretation in this sprint:

- The benchmark narrative is locked.
- The merged reverse-engineering matrix is locked.
- The narrative compiler architecture is locked.
- N-3 has closed the longitudinal raw-value contract gap.
- N-4 has created the first lifestyle interpretation bridge assets.
- N-5 has created pathway-grade explainer assets.
- N-6 has created governed functional interpretation / confidence assets.
- One of the major remaining deterministic gaps is that the benchmark still depends on governed interpretation entities that do not yet exist in the right form.
- N-7 exists to create those missing governed entities before N-8 compiler implementation.

Your job is to create the minimum correct governed interpretation set required for the benchmark narrative and near-term deterministic narrative work.

---

## Required inputs

Treat the following as required inputs:

1. Benchmark target lock  
`docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_TARGET_LOCK.md`

2. Merged reverse-engineering matrix  
`docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REVERSE_ENGINEERING_MERGED.md`

3. Final sprint strategy  
`docs/golden-narrative/HealthIQ_Deterministic_Narrative_Sprint_Strategy_FINAL.md`

4. Narrative compiler architecture  
`docs/golden-narrative/HealthIQ_Deterministic_Narrative_Compiler_Architecture_v1.md`

5. Relevant current authority files, at minimum:
- `knowledge_bus/phenotypes/phenotype_map_v1.yaml`
- `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml`
- `knowledge_bus/pathway_explainers_v1/pathway_explainers_v1.yaml`
- `knowledge_bus/functional_interpretation_v1/functional_interpretation_v1.yaml`
- relevant homocysteine / macrocytosis / lipid transport packages and hypotheses
- any interaction-map or related governed files you determine are relevant

---

## Core problem this sprint must solve

HealthIQ now has:
- pathway explainers
- functional interpretation assets
- confidence / clarification / monitoring assets
- lifestyle bridges
- longitudinal support

But the benchmark narrative still depends on governed interpretation entities that express the right interpretation objects themselves.

In particular, the current governed interpretation layer does not yet cleanly encode the benchmark’s priority entities such as:
- a methylation / homocysteine / macrocytosis interpretation object
- a protective lipid transport interpretation object
- any truly necessary cross-system vascular synthesis object, if the benchmark still requires one after the new asset work

This sprint must create those entities in the right governed location(s), without overbuilding.

---

## Required outcome

Deliver a bounded CONTENT implementation that:

1. defines which governed interpretation entities are actually required for the benchmark and near-term deterministic narrative work
2. creates those entities in the correct governed authority layer(s)
3. aligns them cleanly with existing pathway explainers and functional interpretation assets
4. avoids duplicative or speculative entity creation
5. leaves the interpretation layer ready for N-8 compiler implementation

---

## In scope

### 1. Preflight authority verification
Before creating any new entities, verify and cite:

- what current phenotype/interpretation entities already exist
- what current IDL records already exist
- which current entities are too weak, too broad, or misframed for the benchmark narrative
- whether the benchmark still truly requires:
  - a methylation / homocysteine / macrocytosis entity
  - a protective lipid transport entity
  - a cross-system vascular synthesis entity
- which governed layer should own each required entity:
  - phenotype map
  - IDL records
  - functional interpretation pack linkage
  - another bounded layer if clearly justified

You must not create new entities casually.
First prove which are actually needed.

### 2. Methylation / homocysteine / macrocytosis interpretation entity
Create the governed interpretation entity required for the benchmark’s lead domain.

This should be the entity that allows later compiler work to refer to the lead interpretation coherently and repeatedly without relying on improvised composition.

You must decide and justify:
- whether this belongs as a new phenotype map entry
- whether it requires a new IDL record
- whether it should link to the pathway explainer and functional interpretation assets already created

Do not force the term phenotype if repo/medical logic indicates another governed interpretation framing is more correct.
But the resulting governed object must be usable as the lead benchmark interpretation entity.

### 3. Protective lipid transport interpretation entity
Create the governed interpretation entity required for the benchmark’s secondary domain.

This should support the benchmark’s more precise reading:
- not “high cholesterol”
- not broad lipid dysfunction
- but residual LDL-related exposure within a more favourable transport context

Again, you must decide and justify:
- whether this is a new phenotype/entity
- whether it requires a new IDL record
- how it links to the new pathway explainer and functional interpretation assets

### 4. Cross-system vascular synthesis entity — only if truly needed
Assess whether the benchmark still requires a distinct cross-system vascular synthesis entity, now that:
- pathway explainers exist
- functional interpretation assets exist
- lifestyle bridges exist

If a separate governed cross-system entity is still genuinely needed, create it carefully.
If not, document why it should be deferred or omitted.

Do not build this merely because it appeared in earlier reverse-engineering documents.
Only create it if repo-grounded reasoning and benchmark needs still justify it.

### 5. Cross-asset linkage
Where new interpretation entities are created, ensure they are cleanly linkable to:
- pathway explainers
- functional interpretation assets
- confidence/clarification/monitoring assets
- IDL/display surfaces where appropriate

The later compiler must be able to consume these relationships clearly.

### 6. Validation / structural checks if needed
If the chosen governed layer(s) already have validation or structural tests, add the minimum appropriate coverage.

If no runtime validation is required beyond structural/content checks, say so clearly.

### 7. Short sprint note
Add a concise implementation note documenting:
- what entities were created
- where they live
- why they were needed
- what N-8 is now unblocked to consume

---

## Out of scope

The following are explicitly out of scope:

- narrative compiler implementation
- frontend changes
- broad new system/entity expansion outside benchmark needs
- new lifestyle bridge work
- new longitudinal contract work
- broad report compiler redesign
- Gemini / LLM work

---

## Design rules

### Rule 1 — create only what is needed
Do not create a larger interpretation taxonomy than the benchmark and near-term deterministic roadmap require.

### Rule 2 — governed entity clarity
Make it unambiguous what each new interpretation object is for and where it lives.

### Rule 3 — no taxonomy inflation
Do not create multiple overlapping entities that later compiler work will have to arbitrate unnecessarily.

### Rule 4 — benchmark-aligned but reusable
These entities should support the benchmark case first, but they must not be so bespoke that they only work for AB.

### Rule 5 — preserve authority separation
Do not blur:
- interpretation entity
- pathway explainer
- functional interpretation asset
- display-layer copy

### Rule 6 — compiler-ready linkage
Later N-8 compiler work must be able to consume these entities and their linked asset families cleanly.

---

## Expected implementation shape

The expected shape is:

1. inspect current phenotype/IDL/entity state
2. determine what new governed interpretation objects are actually required
3. create them in the correct layer(s)
4. wire or document the cross-asset linkage expectations
5. add minimal validation if needed
6. write a short sprint note

This must remain a targeted governed-asset sprint, not a narrative-assembly or taxonomy-expansion sprint.

---

## STOP conditions

STOP immediately and report if any of the following are true:

1. the correct governed home for the new entities is ambiguous and needs architectural adjudication
2. creating the needed benchmark entities would force a broader redesign of the phenotype/IDL model
3. the benchmark no longer truly requires one of the originally expected entities and the strategy needs a small correction
4. validation/schema work needed is much larger than expected
5. touched-file scope expands materially beyond the intended governed-content layers

If blocked, report:
- the exact blocker
- the affected files
- the smallest safe remediation path
- whether N-7 should be split before continuing

---

## Success criteria

This sprint is successful only if:

1. the benchmark-required governed interpretation entities are clearly defined
2. the methylation / homocysteine / macrocytosis entity exists in the correct governed form
3. the protective lipid transport entity exists in the correct governed form
4. any cross-system vascular synthesis entity is either created with justification or explicitly deferred with justification
5. cross-asset linkage for later compiler work is clear
6. the sprint remains bounded and avoids unnecessary taxonomy expansion

---

## Deliverables

At finish, the sprint should leave behind:

- the new or updated governed interpretation entity file(s)
- any minimal validation needed
- a short sprint note explaining:
  - what entities were added or changed
  - where they live
  - what future sprint they unblock

Report back with:
- files touched
- governed entity location(s) chosen
- how each benchmark domain is now represented
- whether a cross-system vascular synthesis entity was created or deferred
- any remaining limitation later sprints must respect

---

## Evidence requirements

You must show, with exact file paths and grounded repo evidence:

- what current entities were insufficient
- where the new governed interpretation entities now live
- how they link to pathway explainers / functional interpretation assets
- why that structure is suitable for later compiler consumption
- how this specifically unblocks N-8

Do not claim success merely because some YAML rows were added.
Show that the benchmark’s missing interpretation objects now exist in governed form.