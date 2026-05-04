# HealthIQ AI — GPT Handover Note
## Signal Contract Architecture: Recent Discussion Summary + Workshop Brief
**Date:** 2026-03-25
**From:** Claude (Adversarial Reviewer)
**To:** GPT (Architecture Authority)
**Purpose:** Bring GPT fully up to date on a recent architectural conversation and propose a workshop brief for team agreement before further signal contract work begins.

---

## Part 1 — What we discussed and what Claude assessed

### 1.1 The hardening blocker on KB-S48e

The KB-S48e sprint prompt was submitted for hardening. Claude Code returned a NOT_HARDENED verdict with two blockers.

**Blocker B-1:** The sprint described connecting intervention-aware reasoning through hypothesis-level intervention references. Repo inspection confirmed those references do not exist in any runtime hypothesis YAML file. The gold investigation spec schema carries them. The intelligence model schema v1 has a home for them. But no hypothesis YAML has been populated with `intervention_references`. The registry-level path — reading directly from `intervention_effects_registry_v1.yaml` — is the only viable runtime data source.

**Blocker B-2:** `RootCauseHypothesisV1` has `extra='forbid'`. Adding caveat text fields requires an explicit contract decision. Claude Code assessed three implementation paths and recommended Path B — a new separate `InterventionAnnotationV1` contract alongside the existing output, injected as a parallel field — because it avoids touching boundary files while enabling full caveat surfacing.

These were genuine architectural blockers, not procedural technicalities.

### 1.2 GPT's response — parallel annotation layer

GPT responded by proposing a parallel intervention annotation layer as a strategic architectural move. He framed this as the "world-class" path — additive, parallel output, no root-cause contract contamination, its own output contract.

### 1.3 Claude's assessment of GPT's response

Claude's assessment was: GPT is correct and not drifting. His parallel annotation layer proposal is Path B from the hardening document. GPT arrived at the same architectural conclusion as Claude Code through strategic reasoning. The language was perhaps more elaborate than necessary but the architectural position was sound and grounded in actual repo reality.

The hardening model worked exactly as designed. The governance caught a real integration path problem before Cursor wrote a single line of code.

**Action required from this blocker:** GPT should amend the KB-S48e prompt to declare Path B explicitly, confirm the registry-level data source, and re-submit for hardening.

---

### 1.4 The broader architectural problem that emerged from this

The hardening blocker exposed something more important than the sprint-level issue. The conversation that followed identified a structural contract asymmetry in the platform.

The gold biomarker investigation spec — `investigation_spec_contract_version_20_gold_final.yaml` — is the richest clinical intelligence object in the system. It carries signal definitions, activation conditions, supporting marker relationships, structured hypotheses, hypothesis ranking, confirmatory tests, override rules, evidence references, and narrative framing.

The promoted signal package contract — centred on `signal_library.yaml` — is thinner. It carries signal identity, activation logic, supporting metrics, thresholds, and dependencies. It is enough to define a signal for runtime evaluation. It is not enough to carry the full WHY reasoning structure.

The WHY layer currently lives in separate root-cause hypothesis YAML files, not inside the promoted signal package. The intervention and context layers live in separate registries and overlays. The runtime compiler stitches these together.

This is an acceptable interim maturity state. It is not acceptable as a final architecture because as the signal estate grows, the implicit coordination between adjacent artefacts becomes increasingly fragile. The runtime compiler risks becoming the hidden place where contract gaps are bridged informally, which is exactly how architectural debt accumulates invisibly.

The KB SOP v1.3 section 4 already anticipates the solution. The intelligence model is defined as an opt-in contract layer on top of the three-file package structure. What is missing is the deliberate commitment to that path with proper translation rules and validator enforcement.

---

### 1.5 The research and schema discussion

The conversation then covered several important strategic points that are now part of the shared context.

**On drug libraries and the intervention registry:** The team correctly identified that the platform should not become a drug library. The solution is a small class-level intervention-effects registry governing the drug classes that materially affect the biomarkers the platform interprets. Seven to ten classes cover the vast majority of metabolic panel confounding. The KB-S48a work has already established the foundation for this.

**On pharmaceutical phenotype targets:** An important insight emerged. Most pharmaceutical drug classes are targeting a small number of metabolic phenotypes — the same phenotypes HealthIQ is already modelling. Statins target lipid transport dysfunction. Metformin targets insulin resistance. Thyroid hormone replacement targets thyroid-driven metabolic disturbance. This means the intervention-effects registry stays compact because the phenotype targets are compact. The drugs are many but the biology they address is a small set of interconnected pathways already modelled in the interaction map.

**On research evidence standards:** The platform's evidence standards were made explicit. The accepted evidence hierarchy in priority order is: systematic reviews and meta-analyses first, large prospective cohort studies second (minimum n=1,000, minimum three years follow-up, peer-reviewed), randomised controlled trials third (peer-reviewed, hard endpoints), and major clinical guidelines fourth (NICE, ADA, ESC, AHA, WHO only). Cross-sectional studies, case series, expert opinion without underlying RCT or cohort evidence, and single small observational studies below n=500 are not accepted as primary evidence. Evidence strength classifications must be justified against this hierarchy, not assigned by convention.

**On open-source drug name APIs:** The team discussed using RxNorm and dm+d as research and enrichment tools for populating the alias registry, not as runtime dependencies. External API data must enter the platform through the governance model — reviewed, committed to the repo, and promoted through the normal KB process. It must never enter the reasoning layer unreviewed at runtime. Unknown drug names resolve to `caveat_only` and are queued for human review.

---

### 1.6 The strategic architectural decision now required

The architecture note (`HealthIQ_signal_contract_architecture_note.md`) correctly diagnosed the problem and proposed the right direction. The proposed direction is a controlled contract-unification programme that defines a gold promoted signal-intelligence contract as the authoritative runtime-level representation of signal intelligence.

That contract should be rich enough that the system can understand a signal domain from governed promoted data, not from loosely coordinated adjacent artefacts.

The proposed end-state uses multiple physical artefacts but with unified contract authority — formal validator-enforced boundaries, deterministic translation from the gold investigation spec, unambiguous runtime authority.

Five decisions require explicit team agreement before the architecture decision sprint is authored:

1. Confirm that the intelligence model opt-in contract in KB SOP v1.3 section 4 is the correct architectural mechanism and that new packages must include it.
2. Confirm that existing promoted packages are grandfathered under the three-file legacy contract and do not require immediate migration.
3. Confirm that the gold investigation spec schema is the authoritative source for what the intelligence model contract should eventually contain, and that translation rules must be deterministic and validated.
4. Confirm that the signal contract shape workshop runs before the architecture decision sprint, and that the architecture decision sprint runs before KB-S46.
5. Confirm that the runtime compiler must never be the place where contract gaps are bridged informally. If a signal domain cannot be fully reasoned about from governed promoted artefacts, incompleteness must surface explicitly.

---

## Part 2 — The critical question Claude raised

After reviewing the architecture note, the CEO correctly asked: have we actually agreed what the signal contract shape looks like, or is the shape assumed to be obvious?

The answer is: we have not agreed the shape and it is not obvious.

The second-pass intelligence model design workshop produced the hypothesis object structure, the contradiction marker definition, the supporting marker object requirements, and the longitudinal primitive homes. That work was done from the perspective of what the WHY layer needs to answer. It was the right exercise for hypothesis objects.

We have not done the equivalent exercise specifically for the signal contract — the promoted package that defines signal identity, activation, state logic, supporting marker relationships, and how those connect to the WHY layer below and the intervention and phenotype layers around it.

The current signal library schema was designed around activation and threshold logic. If the promoted signal intelligence contract must now carry WHY reasoning structure, intervention relevance links, phenotype relationships, and longitudinal primitives, we need to know explicitly what questions that contract must support before designing its shape.

Without that exercise we risk either building a contract that is still too thin and repeats the asymmetry problem in a different form, or building one that is overcomplete and collapses too many concerns into one ungovernable object.

---

## Part 3 — Proposed workshop brief: Signal Contract Intelligence Design

This workshop follows the same methodology as the second-pass intelligence model design exercise. We work backwards from downstream questions to upstream knowledge requirements, and only then design the contract shape.

---

### Workshop purpose

Answer one strategic question:

**What questions must the signal contract be able to support — directly or by enabling downstream layers — and what upstream knowledge must be structured in the promoted signal package for those questions to be answerable without informal runtime compensation?**

---

### What this workshop is not

This is not a schema design session.
This is not a YAML field definition exercise.
This is not a discussion of current file formats.

It is a first-principles design exercise that works from downstream intelligence needs to upstream contract requirements.

---

### Rules

Do not start from what the current signal library schema contains.
Do not start from what is convenient to author.
Do not start from what currently passes the validator.

Start from the questions the platform must answer and work backwards.

---

### Part A — User and system perspective

For each user or system type below, list the questions they will want to ask that require signal-level knowledge specifically. Not biomarker-level knowledge. Not hypothesis-level knowledge. Signal-level knowledge about what a metabolic state means, how confident we are in it, and how it connects to other states.

User and system types:
- Consumer user wanting to understand their metabolic pattern
- Advanced user or biohacker wanting mechanism and cross-system connections
- Clinician wanting rapid synthesis and ranked priorities
- Internal reasoning engine connecting signals into chains, phenotypes, and WHY reasoning
- Future longitudinal layer tracking signal state change over time
- Future B2B buyer — pharma, insurer, health system — wanting phenotype and cohort intelligence
- Future clinical audit layer verifying that interpretation was traceable and defensible

For each: what questions do they ask that the signal contract must support?

---

### Part B — What a strong signal-level answer looks like

For each question identified in Part A, define what would make the answer feel genuinely intelligent rather than a traffic light.

Weak signal-level answers:
- This signal is active.
- This marker is high.
- There is a metabolic concern.

Strong signal-level answers would:
- State what metabolic state the signal represents with clinical specificity
- Show which markers support activation and which argue against it
- Connect the signal to upstream drivers and downstream consequences
- State what context inputs materially change the signal's meaning
- Show confidence level and what determines it
- Show what would strengthen or weaken the interpretation
- Indicate what the signal means alongside other co-active signals

---

### Part C — Upstream knowledge the signal contract must carry

For each downstream question, ask: what information must exist in the promoted signal package for this answer to be possible without the runtime compiler inventing it?

Consider at minimum:
- Signal identity and canonical classification
- Activation conditions and state logic
- Supporting marker objects with roles and directionality
- Contradiction or suppression markers
- Cross-signal interaction references
- Phenotype membership or contribution
- Context input sensitivity — which inputs materially change signal meaning
- Intervention class sensitivity — which drug or lifestyle classes confound or explain this signal
- Confidence determinants — what makes this signal more or less reliable
- Longitudinal comparison primitives — what this signal looked like before and what change means
- Evidence traceability — what clinical evidence justifies this signal definition

---

### Part D — Structured vs narrative vs reference

For each upstream knowledge item identified in Part C, classify it as:
- Structured — must be a machine-readable field in the signal contract
- Narrative — can live in explanation prose without affecting reasoning
- Reference — should be a pointer to another governed contract rather than embedded

Use this rule: if the item affects reasoning, ranking, cross-signal linkage, confidence, auditability, or future automation, it must be structured.

---

### Part E — Signal contract boundary decisions

This is the most important part of the exercise.

For each knowledge item classified as structured in Part D, decide:
- Does it belong in the signal package contract directly?
- Does it belong in the hypothesis assets alongside the signal package?
- Does it belong in a separate registry — intervention, phenotype, interaction map — referenced by the signal?
- Does it belong in a runtime overlay — context, user state — that is not part of the promoted package?

This exercise produces the explicit boundary definitions that the KB SOP and validator must enforce.

---

### Part F — Core now vs schema home now vs defer

Following the same discipline as the second-pass intelligence model design exercise, triage every structured knowledge item into:
- Required for correct signal reasoning now — must be populated in v1
- Required for correct reasoning later, but the schema must have a home now — defined but can be empty or lightly populated
- Genuinely deferrable — not needed in the promoted signal contract at this stage

---

### Part G — Structural risk check

Identify the structural decisions that would cause destructive redesign if made incorrectly now.

Examples to consider:
- If supporting markers are flat lists rather than objects with roles
- If signal state is a single field rather than a structured state object with determinants
- If cross-signal relationships are implicit rather than explicitly referenced
- If context sensitivity is buried in prose rather than a structured field
- If confidence is a single float rather than a structured object showing what drives it
- If phenotype membership is not a first-class concept in the signal contract

---

### Part H — Non-negotiable structural guardrails

Produce a closed list of structural guardrails for the signal contract design that will be treated as STOP conditions in the schema sprint. These should mirror the ten guardrails produced in the second-pass intelligence model design exercise but scoped specifically to the signal contract layer.

---

### Workshop output required

By the end of this exercise the team should have:

1. A consolidated list of downstream questions the signal contract must support at each user and system layer
2. A clear view of what strong versus weak signal-level answers look like
3. A triage of upstream knowledge items into structured, narrative, and reference
4. Explicit boundary decisions for what belongs in the signal package versus adjacent governed artefacts
5. A core-now versus schema-home-now versus defer triage
6. A structural risk check identifying rewrite traps
7. A closed list of non-negotiable structural guardrails

That output becomes the governing design document for the target signal intelligence schema sprint.

---

### What happens after this workshop

After the workshop produces the design document, the sequence is:

1. Agree the minimum v1 signal intelligence contract shape from the workshop output
2. Author the architecture decision sprint that implements that shape and its translation rules from the gold investigation spec
3. Update the KB SOP to reflect the new contract requirements
4. Then proceed with KB-S46 WHY expansion using packages that conform to the agreed contract

KB-S46 should not proceed before this workshop and the architecture decision sprint are complete. Packages authored without the agreed signal contract shape will need retroactive migration, which is avoidable at this stage but expensive later.

---

### Final reminder

The goal of this workshop is not to produce a schema.

The goal is to ensure the shape of the signal intelligence contract is correct before the next stable authoring era begins.

A missing field later is survivable.
A wrongly shaped core object is expensive.
A contract that requires the runtime compiler to compensate for its gaps is architecturally dishonest.

**Design the signal contract around the questions the platform must answer in three years, not around what is easiest to encode today.**

---
*This document was prepared by Claude (Adversarial Reviewer) for GPT (Architecture Authority) review and team consensus.*
