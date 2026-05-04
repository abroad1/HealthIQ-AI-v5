# HealthIQ Signal Contract Design Workshop
## Boundary and Target Shape Review Pack

**Status:** Draft for team workshop  
**Owner:** GPT (Architecture Authority)  
**Purpose:** Force the architectural decisions required before any signal-contract decision sprint is authored.

---

## Purpose

This document is the workshop pack for deciding the target shape and boundary of the promoted signal-intelligence contract.

Its purpose is not to brainstorm broadly.  
Its purpose is to force the decisions that must be made before we lock further signal authoring, WHY expansion, or contract translation into the wrong structural shape.

This is the signal-layer equivalent of the earlier intelligence-model second-pass workshop. That workshop deliberately worked backwards from downstream intelligence needs to upstream knowledge requirements before schema design began. We should use the same discipline here. fileciteturn10file0

---

## Core framing

We are not asking:

- what fields do we currently have in `signal_library.yaml`?
- what fits most easily into the current package shape?
- what is the smallest promoted signal contract that still passes the current validator?
- what is the quickest way to unblock KB-S46?

We are asking:

- what signal-level intelligence must the platform support downstream?
- what upstream knowledge must exist in governed promoted artefacts to make that intelligence possible?
- what belongs in the signal contract versus adjacent governed artefacts?
- which signal primitives must be shaped correctly now to avoid future rewrite pain?
- what translation from the gold investigation spec must be deterministic and validator-enforced?

The strategic goal is not to collapse every concept into one file.  
The strategic goal is to ensure there is one unambiguous promoted contract authority for signal intelligence, with explicit boundaries to adjacent artefacts, so the runtime compiler is never forced to bridge contract gaps informally.

---

## Why this workshop exists

The current upstream and downstream contract layers are asymmetric.

### Upstream gold investigation authoring contract

The current investigation-spec schema already models a rich clinical object. The required top-level fields include:

- `investigation_spec_contract_version`
- `spec_id`
- `signal_id`
- `research_domain`
- `primary_marker`
- `trigger_direction`
- `activation`
- `states`
- `supporting_markers`
- `hypotheses`
- `hypothesis_ranking`
- `confirmatory_tests`
- `override_rules`
- `evidence`
- `narrative` fileciteturn10file2L13-L31

The gold investigation examples show those concepts populated in practice, including structured supporting markers, ranked hypotheses, contradiction markers, confirmatory tests, override rules, evidence strength, source references, and narrative interpretation. fileciteturn10file6 fileciteturn10file13 fileciteturn10file16

### Current promoted signal-package contract

The current Knowledge Bus machine-readable signal architecture is `signal_library.yaml`, and each signal currently needs only:

- `signal_id`
- `name`
- `description`
- `system`
- `primary_metric`
- `supporting_metrics`
- `dependencies`
- `thresholds`
- `activation_logic` fileciteturn10file1L60-L76

This is enough to define a signal for activation/evaluation. It is not enough to carry the full WHY, context, intervention, and phenotype-adjacent intelligence shape already implied by the upstream authoring layer.

### Current architectural consequence

The platform therefore currently spreads signal-domain intelligence across adjacent artefacts:

- signal activation and thresholds in promoted `signal_library.yaml`
- WHY reasoning in separate root-cause hypothesis assets
- intervention effects in separate registries/overlays
- future context and phenotype intelligence in adjacent layers

That is an acceptable interim state. It is not a stable end-state for a platform intended to become the deterministic operating system for metabolic interpretation, with narrative layered on top of governed structured intelligence. fileciteturn10file7L1-L18

This workshop exists to decide the proper target contract boundary before more work is authored into an interim shape.

---

## What this workshop is not

This is not:

- a YAML field-definition exercise
- a schema-writing session
- a debate about current validator convenience
- a local unblock for one sprint
- an attempt to collapse the whole intelligence stack into one monolithic file

This is a first-principles contract-boundary exercise.

---

## Workshop outputs required

By the end of this workshop we want clear decisions on:

1. what questions the promoted signal contract must support
2. what a strong signal-level answer looks like
3. which upstream knowledge primitives are required for correct signal reasoning now
4. which primitives need a schema home now even if lightly populated
5. which primitives are genuinely deferrable
6. what belongs in the signal contract versus hypotheses, registries, and overlays
7. what translation from the gold investigation spec must be deterministic
8. which structural choices would create future rewrite traps if we get them wrong now
9. the non-negotiable guardrails for the later signal-contract decision sprint
10. whether we are ready to author that architecture decision sprint

---

## Section 1 — Downstream questions the signal contract must support

### Why this matters

Contract shape should be designed from downstream intelligence needs, not from current file contents.

### Instruction

For each user or system type below, list the questions they will want answered that require **signal-level** knowledge specifically.

Not biomarker-level only.  
Not pure hypothesis-level only.  
Signal-level knowledge about what metabolic state is active, why it matters, how it interacts, how reliable it is, and what changes its meaning.

### User and system types

- Consumer user wanting to understand their metabolic pattern
- Advanced user / biohacker wanting mechanisms and cross-system links
- Clinician wanting rapid synthesis and ranked priorities
- Internal reasoning engine connecting signals into WHY, phenotype, and interaction layers
- Future longitudinal layer tracking signal-state change over time
- Future B2B buyer wanting cohort / phenotype intelligence
- Future clinical-audit layer needing traceability and defensibility

### Working table

| User / system type | Signal-level questions they need answered |
|---|---|
| Consumer user | |
| Advanced user / biohacker | |
| Clinician | |
| Internal reasoning engine | |
| Longitudinal layer | |
| B2B / cohort intelligence | |
| Clinical audit layer | |

### Output required

A consolidated list of downstream questions that the promoted signal contract must support directly or by enabling downstream governed layers.

---

## Section 2 — What a strong signal-level answer looks like

### Why this matters

If we do not define what a genuinely intelligent signal-level answer looks like, we will design a contract that still behaves like a traffic-light engine.

### Weak signal-level answers

- This signal is active.
- This marker is high.
- There is a metabolic concern.

### Strong signal-level answers should be able to do some or all of the following

- state what metabolic state the signal represents with clinical specificity
- show which markers support activation and which argue against it
- show how signal state was determined
- indicate whether the signal is weak / moderate / strong / ambiguous in context
- connect the signal to plausible upstream drivers and downstream consequences
- show what additional data would strengthen or weaken interpretation
- show what context materially changes the signal’s meaning
- show which interventions or exposures may confound or explain the signal
- show how this signal relates to other active signals and phenotype states
- preserve evidence traceability and auditability

### Working table

| Question from Section 1 | What would make the answer genuinely intelligent rather than thin? |
|---|---|
| | |
| | |
| | |

### Output required

A short definition of what constitutes a strong signal-level answer in HealthIQ AI.

---

## Section 3 — Upstream knowledge primitive triage for signal intelligence

### Why this matters

We cannot move straight from the current asymmetry to a contract decision without triaging the knowledge primitives involved.

We therefore need to force every candidate signal-level primitive into one of three buckets:

1. required for correct reasoning now
2. required for correct reasoning later, but the schema must have a home now
3. genuinely deferrable

This follows the same discipline as the earlier second-pass workshop. fileciteturn10file12

### Triage rule

- **Required for correct reasoning now**  
  The platform cannot produce honest, acceptable signal intelligence in early production without this primitive.

- **Required for correct reasoning later, but schema must have a home now**  
  It may be lightly populated or unused in v1, but if it has no defined home now, later implementation will force structural redesign.

- **Genuinely deferrable**  
  It can be omitted from both v1 population and v1 schema without likely architectural dishonesty or redesign pain.

### Candidate primitive list

Use this as the minimum starting list and add rows as needed:

| Primitive | Short definition | Triage bucket | Why |
|---|---|---|---|
| Signal identity | Canonical signal identity and meaning | | |
| Signal class / canonical classification | Stable classification for reasoning and grouping | | |
| Signal system membership | Metabolic / inflammatory / hepatic etc. | | |
| Primary metric object | Main marker for signal activation | | |
| Trigger direction | High / low / both | | |
| Activation logic | Deterministic activation rule | | |
| Activation config | Thresholding / state trigger details | | |
| Signal states | Baseline / escalation / risk-state model | | |
| Supporting marker objects | Marker objects rather than flat names | | |
| Supporting marker relationship kind | Mechanism / corroboration / differential / severity etc. | | |
| Supporting marker directionality | Expected direction and meaning | | |
| Supporting marker rationale | Why the marker matters | | |
| Marker availability | Common / uncommon / specialty | | |
| Contradiction / suppression markers | Evidence that weakens or redirects signal interpretation | | |
| Missing-data primitives | What cannot be concluded when data is absent | | |
| Confidence determinants | What makes this signal more or less reliable | | |
| Confirmatory test references | Structured next-step test objects or pointers | | |
| Override / escalation rules | Governed state escalation or suppression rules | | |
| Evidence strength | Strength of clinical evidence | | |
| Evidence source traceability | Source references and provenance | | |
| Physiological claim | Core claim the signal represents | | |
| Threshold notes | Threshold interpretation traceability | | |
| Narrative interpretation | Human-readable interpretation text | | |
| Upstream driver references | Links to plausible upstream causes / domains | | |
| Downstream consequence references | Links to consequences / affected systems | | |
| Cross-signal interaction references | Explicit relationships to other signals | | |
| Phenotype membership / contribution | Belongs to or contributes to phenotype state | | |
| Context sensitivity references | Which user/context inputs materially alter meaning | | |
| Intervention sensitivity references | Which intervention classes confound/explain the signal | | |
| Longitudinal identity key | Stable identity across time | | |
| Longitudinal snapshot primitive | What changed over time | | |
| Provenance / authorship metadata | Governance traceability | | |

### Output required

A complete triage table with every important signal-level primitive assigned and justified.

---

## Section 4 — Structured vs narrative vs reference

### Why this matters

Not everything should be embedded as a first-class field in the signal contract.

We need to distinguish between:

- **Structured** — must be machine-readable because it affects reasoning, ranking, confidence, auditability, or automation
- **Narrative** — explanatory prose that does not drive reasoning
- **Reference** — a governed pointer to another contract or registry rather than embedded payload

### Rule

If the item affects reasoning, ranking, cross-signal linkage, confidence, auditability, deterministic translation, or future automation, it should not be prose-only.

### Working table

| Primitive | Structured / Narrative / Reference | Why |
|---|---|---|
| | | |
| | | |
| | | |

### Output required

A classified view of every important signal intelligence primitive.

---

## Section 5 — Boundary decisions: what belongs where

### Why this matters

This is the core architectural boundary decision.

The question is not simply “what should the signal package contain?”  
The question is “what must be true in promoted signal intelligence so downstream reasoning does not depend on informal runtime compensation?”

### Candidate homes

For each structured primitive from Section 4, decide whether it belongs in:

- the promoted signal package contract directly
- adjacent WHY / hypothesis assets
- a separate governed registry (intervention, phenotype, interaction map, confirmatory-test registry, etc.)
- a runtime overlay / user-state layer that is deliberately outside promoted package scope

### Working table

| Primitive | Signal package | Hypothesis assets | Separate registry | Overlay / user state | Why |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |

### Output required

An explicit boundary decision set for the signal contract and adjacent artefacts.

---

## Section 6 — Full target vs v1 promoted signal contract

### Why this matters

We need a clean separation between:

- the full target signal-intelligence contract the platform will eventually need
- the minimum v1 promoted contract shape that must exist soon
- what must be populated immediately versus what merely needs a schema home now

Without this, the next sprint will either be too thin or too broad.

### Working table

| Primitive | Part of full target? | Must exist in v1 schema? | Must be populated in v1? | Why |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |

### Output required

A reconciled view of:

- full target signal-intelligence contract
- v1 contract commitment
- v1 population commitment

---

## Section 7 — Deterministic translation from gold investigation spec

### Why this matters

The gold investigation spec is already richer than the current promoted signal contract. It is therefore the natural reference source for what promoted signal intelligence may need to express. But this does **not** mean “copy everything across blindly”.

We need explicit translation rules.

### Questions to answer

1. Which investigation-spec concepts must translate directly into promoted signal intelligence?
2. Which investigation-spec concepts should remain in adjacent assets by design?
3. Which concepts should translate as references rather than embedded structures?
4. What concepts are upstream-authoring-only and should not appear in promoted runtime authority?
5. Which concepts require deterministic validators to prove semantic completeness?

### Working table

| Gold investigation concept | Translate directly | Translate by reference | Stay outside promoted signal contract | Why |
|---|---|---|---|---|
| Activation | | | | |
| States | | | | |
| Supporting markers | | | | |
| Hypotheses | | | | |
| Hypothesis ranking | | | | |
| Confirmatory tests | | | | |
| Override rules | | | | |
| Evidence | | | | |
| Narrative | | | | |
| | | | | |

### Output required

A deterministic translation stance from upstream gold investigation specs into downstream promoted signal intelligence.

---

## Section 8 — Structural risk check

### Why this matters

Future pain usually comes from wrong structural assumptions, not from missing fields.

We therefore need to identify the signal-contract design choices most likely to create destructive rewrite traps if we get them wrong now.

### Questions to ask

1. Are we modelling any object too simply?
2. Are we still treating anything one-to-one that is really one-to-many?
3. Are we leaving reasoning-important structure in prose?
4. Are we attaching knowledge at the wrong layer?
5. Are future-important primitives still missing a defined home?

### Working table

| Potential structural risk | Why it is risky | Action needed now? |
|---|---|---|
| Signal states modelled too simply | | |
| Supporting markers reduced to flat lists | | |
| Confidence model too thin / implicit | | |
| Cross-signal relationships left implicit | | |
| Context sensitivity buried in prose | | |
| Intervention relevance buried in prose | | |
| Hypothesis / signal boundary still ambiguous | | |
| Phenotype membership has no governed home | | |
| Longitudinal identity not defined | | |
| Runtime compiler still expected to bridge gaps | | |

Add rows as needed.

### Output required

A shortlist of structural rewrite risks that must be eliminated before the architecture decision sprint is authored.

---

## Section 9 — Guardrails for the signal-contract decision sprint

### Why this matters

The later architecture decision sprint will need hard guardrails so that good intentions do not collapse into convenience modelling.

### Proposed guardrail questions

1. Must supporting markers always be objects rather than flat lists?
2. Must signal state be a structured object rather than a single label?
3. Must contradiction / suppression / ambiguity have a governed structured home?
4. Must all reasoning-relevant cross-signal relationships be explicit rather than inferred ad hoc?
5. Must any future-important primitive in “schema home now” have an explicit field or reference home?
6. Must narrative remain separated from reasoning objects?
7. Must the runtime compiler refuse to infer knowledge that should exist in governed promoted artefacts?
8. Must translation from investigation spec to promoted signal intelligence be deterministic and validator-enforced?
9. Must legacy packages be grandfathered rather than forced into immediate migration?
10. Must v1 avoid collapsing hypotheses, intervention, phenotype, and context into one ungovernable object?

### Working table

| Guardrail | Decision | Why |
|---|---|---|
| Supporting markers must be objects | | |
| Signal state must be structured | | |
| Contradiction / suppression must have a governed home | | |
| Cross-signal relationships must be explicit | | |
| Bucket-2 primitives must have schema homes | | |
| Narrative must stay separate from reasoning objects | | |
| Runtime must not compensate for missing contract structure | | |
| Translation rules must be deterministic | | |
| Legacy packages may be grandfathered | | |
| Contract scope must stay governable | | |

### Output required

A final closed list of non-negotiable structural guardrails.

---

## Section 10 — Final decision summary

This section should be completed only after the rest of the pack is done.

### Required summary

1. Downstream signal-intelligence questions agreed?
2. Strong signal-level answer definition agreed?
3. Primitive triage complete?
4. Structured / narrative / reference classification complete?
5. Boundary decisions complete?
6. Full target vs v1 reconciliation complete?
7. Translation stance from gold investigation spec agreed?
8. Structural risks identified?
9. Guardrails agreed?
10. Are we ready to author the signal-contract architecture decision sprint?

### Working table

| Decision area | Status | Notes |
|---|---|---|
| Downstream questions | | |
| Strong signal-level answer definition | | |
| Primitive triage | | |
| Structured / narrative / reference classification | | |
| Boundary decisions | | |
| Full target vs v1 reconciliation | | |
| Translation stance | | |
| Structural risk check | | |
| Guardrails | | |
| Ready for architecture decision sprint | | |

---

## Suggested workshop sequence

1. Reconfirm the purpose of the exercise
2. Define the downstream questions the signal contract must support
3. Define what a strong signal-level answer looks like
4. Triage all signal intelligence primitives
5. Classify each as structured, narrative, or reference
6. Make explicit boundary decisions
7. Reconcile full target vs v1
8. Define deterministic translation stance from gold investigation spec
9. Review structural risks
10. Freeze guardrails
11. Decide whether the architecture decision sprint can now be authored

---

## Suggested success criteria

This workshop is successful only if:

- the team agrees what the promoted signal contract is for
- the signal contract boundary versus adjacent artefacts is explicit
- every important signal primitive has been triaged
- there is a clean distinction between full target and v1 contract shape
- translation expectations from the gold investigation spec are explicit
- structural rewrite traps have been identified and addressed
- the next architecture decision sprint can be authored without broad ambiguity

---

## Final reminder

The purpose of this exercise is not to be exhaustive for its own sake.

The purpose is to ensure that the **shape** of promoted signal intelligence is correct before the next stable authoring era begins.

A missing field later is survivable.  
A wrongly shaped core object is expensive.

If the signal contract remains too thin, the runtime compiler will be pressured to compensate.  
If the signal contract becomes too broad, the model will become ungovernable.

This workshop exists to avoid both failures.
