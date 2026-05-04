# HealthIQ Signal Contract Design — Filled Decision Document

## Purpose

This document completes the signal-contract workshop pack and sets out the proposed target shape and contract boundary for promoted signal intelligence.

Its purpose is not to optimise for current validator convenience or to unblock one sprint.
Its purpose is to ensure the promoted signal layer is shaped for the platform HealthIQ is actually building:

a deterministic metabolic intelligence platform with explicit, auditable biological reasoning, governed context consumption, longitudinal growth potential, and eventual strategic buyer fit. fileciteturn13file0 fileciteturn13file14

The core strategic question is:

> what signal-level contract shape best supports HealthIQ’s long-term value as the metabolic reasoning layer between raw biomarker data and high-value regulated workflows?

That matters because a signal contract that remains too thin will force the runtime compiler to compensate informally, while a signal contract that becomes too broad will collapse into an ungovernable monolith. fileciteturn13file11

---

## Core framing

We are not designing the signal contract for the current `signal_library.yaml` alone.
We are designing it for:

- downstream clinician-grade synthesis
- cross-signal metabolic interpretation
- context-aware interpretation
- longitudinal signal tracking
- phenotype / cohort intelligence
- traceability and auditability
- eventual buyer value in insurer, clinic, and enterprise settings

The promoted signal contract therefore needs to be materially richer than a simple activation object, but it must still stop short of absorbing every adjacent concept into one file. The correct outcome is one unambiguous promoted signal-intelligence authority with explicit boundaries to adjacent governed artefacts. fileciteturn13file2

---

# Section 1 — Downstream questions the promoted signal contract must support

## Working table

| User / system type | Signal-level questions they need answered |
|---|---|
| Consumer user | What metabolic state is active? How important is it? Is it weak, moderate, or strong? Why does it matter beyond one abnormal marker? What other signals does it relate to? |
| Advanced user / biohacker | What exact physiological state does this signal represent? What markers support it? What markers weaken it? What upstream drivers are plausible? What downstream consequences are linked? What other signals commonly co-occur? |
| Clinician | Which active signals matter most? Which are robust versus ambiguous? What evidence drove activation? What context materially changes meaning? What confounders or intervention caveats apply? What next tests would clarify the picture? |
| Internal reasoning engine | What is the canonical signal identity? What state is active? What supporting and contradiction evidence exists? What confidence determinants apply? What cross-signal links, context sensitivities, intervention sensitivities, and phenotype links are available in governed form? |
| Longitudinal layer | What signal existed at time A vs time B? Did the signal strengthen, weaken, resolve, or remain stable? Did confidence change? Did context or interventions change interpretation? |
| B2B / cohort intelligence | Which members express this signal? Which phenotypes does it contribute to? Which signal combinations define a cohort? Which signals are stable enough for stratification? |
| Clinical audit layer | What exactly was the signal claim? What governed logic activated it? What supporting evidence existed? What caveats, overrides, and source traceability were present at the time? |

## Consolidated downstream question set

The promoted signal contract must support or enable answers to the following:

1. What metabolic state does this signal represent?
2. Why is this signal active?
3. How strong, reliable, or ambiguous is the signal in context?
4. What evidence supports the signal, and what weakens it?
5. What context or intervention materially changes its meaning?
6. What other signals does it connect to?
7. What phenotype or cohort logic does it contribute to?
8. What changed over time?
9. What audit trail exists for why the signal was emitted?

## Decision statement

The promoted signal contract is not only an activation contract.
It is the canonical governed representation of a metabolic state that must be intelligible to downstream reasoning, longitudinal tracking, clinician synthesis, and future cohort logic.

---

# Section 2 — What a strong signal-level answer looks like

## Working table

| Question | What would make the answer genuinely intelligent rather than thin? |
|---|---|
| What metabolic state is active? | A clinically specific state claim, not just “marker high”. |
| Why is it active? | Explicit activation basis: primary metric, supporting markers, trigger direction, state logic. |
| How reliable is it? | Confidence / ambiguity determinants, missing-data limits, and contradiction or suppression signals. |
| What changes its meaning? | Structured context sensitivity and intervention sensitivity, not prose-only caveats. |
| How does it connect? | Upstream-driver references, downstream-consequence references, and cross-signal links. |
| What next? | Clear confirmatory-test references and escalation / override relevance where appropriate. |
| Can this be defended later? | Source traceability, threshold notes, and deterministic activation rationale. |

## Definition of a strong signal-level answer

A strong signal-level answer in HealthIQ AI is one that:

- names the metabolic state with clinical specificity
- shows how activation was determined
- distinguishes support from contradiction and ambiguity
- expresses confidence limits honestly
- makes context and intervention sensitivity explicit
- connects the signal to broader system meaning
- supports auditability and later automation

A thin answer says a signal is present.
A strong answer says what state is present, why it is believed, how robust that belief is, and what materially changes its interpretation.

---

# Section 3 — Upstream knowledge primitive triage for signal intelligence

## Triage table

| Primitive | Short definition | Triage bucket | Why |
|---|---|---|---|
| Signal identity | Canonical signal identity and meaning | Required now | Without stable identity, no downstream reasoning or audit is reliable. |
| Signal class / canonical classification | Stable classification for grouping and reasoning | Required later, schema home now | Important for cohorting and system grouping; not strictly needed for immediate activation. |
| Signal system membership | Metabolic / hepatic / inflammatory etc. | Required now | Clinician synthesis and cross-system reasoning need it. |
| Primary metric object | Main marker for signal activation | Required now | Core activation anchor. |
| Trigger direction | High / low / both | Required now | Essential to deterministic activation. |
| Activation logic | Deterministic activation rule | Required now | Core runtime truth. |
| Activation config | Threshold / state trigger details | Required now | Needed for deterministic evaluation and audit. |
| Signal states | Baseline / escalation / risk-state model | Required now | A signal without structured state remains traffic-light thin. |
| Supporting marker objects | Marker objects rather than flat names | Required now | Flat lists are architecturally dishonest. |
| Supporting marker relationship kind | Mechanism / corroboration / differential / severity etc. | Required now | Relationship semantics affect reasoning quality. |
| Supporting marker directionality | Expected direction and meaning | Required now | Needed for precise logic. |
| Supporting marker rationale | Why the marker matters | Required later, schema home now | Valuable for transparency and future enrichment. |
| Marker availability | Common / uncommon / specialty | Genuinely deferrable | Useful later, but not a core signal-intelligence requirement. |
| Contradiction / suppression markers | Evidence that weakens or redirects interpretation | Required now | Critical to honest confidence handling. |
| Missing-data primitives | What cannot be concluded when data is absent | Required now | Prevents false certainty. |
| Confidence determinants | What makes the signal more or less reliable | Required now | Strong signal answers require this. |
| Confirmatory test references | Structured next-step test objects or pointers | Required now | Needed for clinician utility and downstream actionability. |
| Override / escalation rules | Governed escalation or suppression rules | Required now | Necessary where state or interpretation can be modified deterministically. |
| Evidence strength | Strength of clinical evidence | Required now | Important for defensibility and ranking. |
| Evidence source traceability | Source references and provenance | Required later, schema home now | Should not be homeless, even if lightly populated at first. |
| Physiological claim | Core claim the signal represents | Required now | Semantic centre of the signal. |
| Threshold notes | Threshold interpretation traceability | Required later, schema home now | Useful for nuance and audit. |
| Narrative interpretation | Human-readable interpretation text | Required later, schema home now | Important for translation layer, but must not drive reasoning. |
| Upstream driver references | Links to plausible upstream causes / domains | Required later, schema home now | Important for WHY, phenotype, and buyer value. |
| Downstream consequence references | Links to consequences / affected systems | Required later, schema home now | Important for richer synthesis and future cohort logic. |
| Cross-signal interaction references | Explicit relationships to other signals | Required later, schema home now | Needed for systems-level reasoning; schema home required now. |
| Phenotype membership / contribution | Belongs to or contributes to phenotype state | Required later, schema home now | Future-important for platform moat and buyer value. |
| Context sensitivity references | Which user/context inputs materially alter meaning | Required later, schema home now | Context is now strategically central. fileciteturn13file17 |
| Intervention sensitivity references | Which intervention classes confound/explain the signal | Required later, schema home now | Registry foundation exists; signal contract must be able to consume it. fileciteturn13file13 |
| Longitudinal identity key | Stable identity across time | Required later, schema home now | Needed for trajectory growth without redesign. |
| Longitudinal snapshot primitive | What changed over time | Required later, schema home now | Same reason. |
| Provenance / authorship metadata | Governance traceability | Genuinely deferrable beyond minimal versioning | Useful, but can remain minimal if higher-level package governance already tracks it. |

## Triage summary

### Required for correct reasoning now
- signal identity
- signal system membership
- primary metric object
- trigger direction
- activation logic
- activation config
- signal states
- supporting marker objects
- supporting marker relationship kind
- supporting marker directionality
- contradiction / suppression markers
- missing-data primitives
- confidence determinants
- confirmatory test references
- override / escalation rules
- evidence strength
- physiological claim

### Required later, but schema must have a home now
- signal class / canonical classification
- supporting marker rationale
- evidence source traceability
- threshold notes
- narrative interpretation
- upstream driver references
- downstream consequence references
- cross-signal interaction references
- phenotype membership / contribution
- context sensitivity references
- intervention sensitivity references
- longitudinal identity key
- longitudinal snapshot primitive

### Genuinely deferrable
- marker availability
- full authorship/provenance metadata beyond minimal governance metadata

---

# Section 4 — Structured vs narrative vs reference

## Classification table

| Primitive | Structured / Narrative / Reference | Why |
|---|---|---|
| Signal identity | Structured | Core contract identity. |
| Signal class / canonical classification | Structured | Used for grouping and downstream logic. |
| Signal system membership | Structured | Used in reasoning and synthesis. |
| Primary metric object | Structured | Core activation object. |
| Trigger direction | Structured | Determines logic. |
| Activation logic | Structured | Deterministic runtime truth. |
| Activation config | Structured | Thresholding and state rules must be machine-readable. |
| Signal states | Structured | State must not be prose-only. |
| Supporting marker objects | Structured | Reasoning-relevant structure. |
| Supporting marker relationship kind | Structured | Affects interpretation. |
| Supporting marker directionality | Structured | Affects interpretation. |
| Supporting marker rationale | Structured | Better as governed data than prose. |
| Contradiction / suppression markers | Structured | Affects confidence and ambiguity. |
| Missing-data primitives | Structured | Affects what may be concluded. |
| Confidence determinants | Structured | Should not be hidden in narrative. |
| Confirmatory test references | Reference | Better as pointers to governed confirmatory-test artefacts than embedded copies. |
| Override / escalation rules | Structured | Affect runtime behaviour. |
| Evidence strength | Structured | Affects ranking and trust. |
| Evidence source traceability | Reference | Better as governed references than duplicated blobs. |
| Physiological claim | Structured | Core semantic claim. |
| Threshold notes | Structured | Needs governed machine-readable home even if human-readable text is included. |
| Narrative interpretation | Narrative | Helpful for humans, but must not drive reasoning. |
| Upstream driver references | Reference | Better linked to adjacent governed assets. |
| Downstream consequence references | Reference | Same reason. |
| Cross-signal interaction references | Reference | Should point to governed interaction maps rather than duplicate them. |
| Phenotype membership / contribution | Reference | Better linked to phenotype assets. |
| Context sensitivity references | Reference | Should point to governed context rules / mappings. |
| Intervention sensitivity references | Reference | Should point to intervention-effects registry entries. |
| Longitudinal identity key | Structured | Runtime-relevant identifier. |
| Longitudinal snapshot primitive | Structured | Machine-readable for future tracking. |

## Decision statement

If a primitive affects reasoning, ranking, confidence, traceability, or future automation, it must be structured or reference-governed.
Narrative is for explanation only.

---

# Section 5 — Boundary decisions: what belongs where

## Boundary table

| Primitive | Signal package | Hypothesis assets | Separate registry | Overlay / user state | Why |
|---|---|---|---|---|---|
| Signal identity | Yes | No | No | No | Core promoted signal authority. |
| Signal class / canonical classification | Yes | No | No | No | Stable grouping should live with the signal. |
| Signal system membership | Yes | No | No | No | Core signal attribute. |
| Primary metric object | Yes | No | No | No | Core activation definition. |
| Trigger direction | Yes | No | No | No | Core activation definition. |
| Activation logic | Yes | No | No | No | Core promoted runtime truth. |
| Activation config | Yes | No | No | No | Core promoted runtime truth. |
| Signal states | Yes | No | No | No | State belongs to signal semantics. |
| Supporting marker objects | Yes | No | No | No | Signal activation/support shape must not be fragmented. |
| Supporting marker relationship kind | Yes | No | No | No | Same reason. |
| Supporting marker directionality | Yes | No | No | No | Same reason. |
| Supporting marker rationale | Yes | No | No | No | Best kept close to signal support semantics. |
| Contradiction / suppression markers | Yes | Partly | No | No | Signal-level contradiction belongs in promoted contract; hypothesis-specific contradiction remains in hypothesis assets. |
| Missing-data primitives | Yes | Partly | No | No | Signal-level limitations belong in signal package; explanation-specific missingness can remain in hypotheses. |
| Confidence determinants | Yes | Partly | No | No | Signal-level confidence belongs in contract; explanation-specific confidence belongs in hypotheses. |
| Confirmatory test references | By reference | By reference | Yes | No | Best handled through governed test registry. |
| Override / escalation rules | Yes | Partly | No | No | Signal-state overrides belong with signal; explanation-level caveat logic can remain adjacent. |
| Evidence strength | Yes | Partly | No | No | Signal-level evidence strength belongs in contract; hypothesis evidence remains adjacent. |
| Evidence source traceability | By reference | By reference | Yes | No | Centralised references avoid duplication. |
| Physiological claim | Yes | No | No | No | Core signal meaning. |
| Threshold notes | Yes | No | No | No | Interpretation-critical and tied to signal thresholds. |
| Narrative interpretation | No | No | No | Downstream translation layer | Must remain separate from reasoning objects. |
| Upstream driver references | No | Yes | Possibly | No | Better handled in WHY / hypothesis layer. |
| Downstream consequence references | No | Yes | Possibly | No | Same reason. |
| Cross-signal interaction references | By reference | No | Yes | No | Govern in dedicated interaction maps. |
| Phenotype membership / contribution | By reference | No | Yes | No | Govern in phenotype contract, not embedded. |
| Context sensitivity references | By reference | No | Yes | Partly | Signal package should point to governed context rules; live context values are user-state/overlay. |
| Intervention sensitivity references | By reference | No | Yes | Partly | Signal package should point to intervention-effects registry; live interventions are user-state. |
| Longitudinal identity key | No | No | No | Yes | Belongs to user-state / longitudinal layer, not package. |
| Longitudinal snapshot primitive | No | No | No | Yes | Same reason. |

## Boundary decision summary

### Belongs directly in promoted signal package
- signal identity
- signal class / canonical classification
- signal system membership
- primary metric object
- trigger direction
- activation logic
- activation config
- signal states
- supporting marker objects
- supporting marker relationship kind
- supporting marker directionality
- supporting marker rationale
- signal-level contradiction / suppression primitives
- signal-level missing-data primitives
- signal-level confidence determinants
- signal-level override / escalation rules
- signal-level evidence strength
- physiological claim
- threshold notes

### Belongs in adjacent hypothesis assets
- ranked hypotheses
- explanation-specific contradiction
- explanation-specific confidence and caveats
- upstream driver reasoning
- downstream consequence reasoning
- differential reasoning

### Belongs in separate governed registries / contracts
- confirmatory tests
- evidence source references
- cross-signal interaction maps
- phenotype definitions / memberships
- context rule registries
- intervention-effects registry

### Belongs in overlay / user-state layer
- user context values
- user intervention / exposure records
- longitudinal identity
- longitudinal snapshots and trajectory data

---

# Section 6 — Full target vs v1 promoted signal contract

## Reconciled table

| Primitive | Part of full target? | Must exist in v1 schema? | Must be populated in v1? | Why |
|---|---|---|---|---|
| Signal identity | Yes | Yes | Yes | Core contract. |
| Signal class / canonical classification | Yes | Yes | Yes | Stable grouping should be locked now. |
| Signal system membership | Yes | Yes | Yes | Core synthesis primitive. |
| Primary metric object | Yes | Yes | Yes | Core contract. |
| Trigger direction | Yes | Yes | Yes | Core contract. |
| Activation logic | Yes | Yes | Yes | Core contract. |
| Activation config | Yes | Yes | Yes | Core contract. |
| Signal states | Yes | Yes | Yes | Signal must support richer than binary activation. |
| Supporting marker objects | Yes | Yes | Yes | Non-negotiable. |
| Supporting marker relationship kind | Yes | Yes | Yes | Non-negotiable. |
| Supporting marker directionality | Yes | Yes | Yes | Non-negotiable. |
| Supporting marker rationale | Yes | Yes | No | Schema home now; fill over time. |
| Contradiction / suppression markers | Yes | Yes | Yes | Must be first-class in v1. |
| Missing-data primitives | Yes | Yes | Yes | Must be first-class in v1. |
| Confidence determinants | Yes | Yes | Yes | Must be first-class in v1. |
| Confirmatory test references | Yes | Yes | No | Reference home now; population can expand later. |
| Override / escalation rules | Yes | Yes | Yes | Important for governed behaviour. |
| Evidence strength | Yes | Yes | Yes | Immediate reasoning value. |
| Evidence source traceability | Yes | Yes | No | Schema home now to avoid later surgery. |
| Physiological claim | Yes | Yes | Yes | Core meaning. |
| Threshold notes | Yes | Yes | No | Schema home now. |
| Upstream driver references | Yes | No in signal package | No | Belongs in adjacent hypotheses, not signal package. |
| Downstream consequence references | Yes | No in signal package | No | Same reason. |
| Cross-signal interaction references | Yes | Yes by reference | No | Reference home now. |
| Phenotype membership / contribution | Yes | Yes by reference | No | Reference home now. |
| Context sensitivity references | Yes | Yes by reference | No | Reference home now. |
| Intervention sensitivity references | Yes | Yes by reference | No | Reference home now. |
| Narrative interpretation | Yes | No in promoted reasoning contract | No | Narrative should remain separate. |
| Longitudinal identity key | Yes | No in signal package | No | Overlay/user-state concern. |
| Longitudinal snapshot primitive | Yes | No in signal package | No | Overlay/user-state concern. |

## Reconciled decision

The v1 promoted signal schema must be broader than the current minimal activation contract.
But it must not absorb hypotheses, phenotype contracts, intervention registries, or longitudinal user state into a single object.

The correct v1 stance is:

- enrich the promoted signal contract where the primitive is signal-semantic and reasoning-critical
- use references where adjacent governed artefacts are the right authority
- keep user-state and longitudinal data outside the promoted package

---

# Section 7 — Deterministic translation from gold investigation spec

## Translation table

| Gold investigation concept | Translate directly | Translate by reference | Stay outside promoted signal contract | Why |
|---|---|---|---|---|
| Activation | Yes | No | No | Core promoted signal logic. |
| States | Yes | No | No | Core signal semantics. |
| Supporting markers | Yes | No | No | Must not be flattened away. |
| Hypotheses | No | No | Yes | Belongs in adjacent WHY assets. |
| Hypothesis ranking | No | No | Yes | Same reason. |
| Confirmatory tests | No | Yes | No | Best as references to governed test artefacts. |
| Override rules | Yes | Partly | No | Signal-state override logic belongs in signal package; explanation-specific overrides may remain adjacent. |
| Evidence | Partly | Yes | No | Evidence strength direct; detailed source traceability by reference. |
| Narrative | No | No | Yes | Narrative should remain out of promoted reasoning authority. |
| Research domain | Yes | No | No | Useful signal classification input. |
| Primary marker | Yes | No | No | Core promoted logic. |
| Trigger direction | Yes | No | No | Core promoted logic. |

## Deterministic translation stance

The promoted signal contract should be a deterministic reduction of the gold investigation spec, not a blind copy.

### Translate directly
Anything that is:
- signal-semantic
- activation-relevant
- confidence-relevant
- state-relevant
- needed for downstream signal intelligence

### Translate by reference
Anything that is:
- governed elsewhere more cleanly
- reusable across many signals
- liable to duplication if embedded repeatedly

### Stay outside promoted signal contract
Anything that is:
- explanation-specific rather than signal-semantic
- narrative-only
- fundamentally part of adjacent WHY assets or user-state overlays

### Validator expectation
The translation should be deterministic and validator-enforced.
The runtime compiler should not infer missing signal semantics that ought to have been carried across from the gold investigation artefact. This is directly aligned with the workshop’s anti-compensation principle. fileciteturn13file11

---

# Section 8 — Structural risk check

## Working table

| Potential structural risk | Why it is risky | Action needed now? |
|---|---|---|
| Signal states modelled too simply | Collapses meaningful metabolic state into flat labels and makes later progression logic brittle. | Yes — state must be structured. |
| Supporting markers reduced to flat lists | Loses relationship kind, directionality, rationale, contradiction, and severity meaning. | Yes — marker objects are non-negotiable. |
| Confidence model too thin / implicit | Forces narrative or runtime guesswork to explain ambiguity. | Yes — confidence determinants need structured homes. |
| Cross-signal relationships left implicit | Prevents governed systems-level reasoning and later phenotype logic. | Yes — create explicit reference homes now. |
| Context sensitivity buried in prose | Makes context-aware interpretation fragile and non-automatable. | Yes — reference-governed context sensitivity must exist. |
| Intervention relevance buried in prose | Prevents proper use of the intervention-effects registry. | Yes — reference-governed intervention sensitivity must exist. |
| Hypothesis / signal boundary still ambiguous | Risks monolithic ungovernable objects or duplication across artefacts. | Yes — freeze explicit boundary now. |
| Phenotype membership has no governed home | Blocks future cohort and buyer value logic. | Yes — define reference home now. |
| Longitudinal identity not defined | Later trajectory work will require cross-cutting redesign. | Yes — keep home in overlay/user-state architecture. |
| Runtime compiler still expected to bridge gaps | Encourages hidden intelligence outside governed contracts. | Yes — architecture must forbid this. |
| Narrative mixed into reasoning contract | Encourages prose to become de facto logic. | Yes — keep separate. |
| Everything collapsed into signal package | Makes the contract ungovernable and migration-heavy. | Yes — preserve explicit adjacent artefact boundaries. |

## Structural rewrite risks that must be eliminated now

1. Signal state must not remain a simple label.
2. Supporting markers must not remain flat lists.
3. Confidence and ambiguity must not stay implicit.
4. Context and intervention relevance must not live only in prose.
5. Cross-signal and phenotype links must not be left homeless.
6. Runtime must not compensate for missing contract structure.
7. Narrative must not contaminate governed reasoning authority.
8. Hypothesis and signal boundaries must remain explicit.

---

# Section 9 — Guardrails for the signal-contract decision sprint

## Guardrail table

| Guardrail | Decision | Why |
|---|---|---|
| Supporting markers must be objects | Yes | Flat lists are architecturally dishonest. |
| Signal state must be structured | Yes | Required for non-trivial signal intelligence. |
| Contradiction / suppression must have a governed home | Yes | Required for honest confidence handling. |
| Cross-signal relationships must be explicit | Yes | Needed for systems-level reasoning and phenotype growth. |
| Bucket-2 primitives must have schema homes | Yes | Prevents later redesign. |
| Narrative must stay separate from reasoning objects | Yes | Preserves deterministic core. |
| Runtime must not compensate for missing contract structure | Yes | Missing knowledge must be treated as a contract failure, not silently inferred. |
| Translation rules must be deterministic | Yes | Required for governance and validator enforcement. |
| Legacy packages may be grandfathered | Yes | Avoids forcing immediate repo-wide migration if bounded compatibility is safe. |
| Contract scope must stay governable | Yes | Prevents a monolithic signal object swallowing adjacent layers. |

## Final closed guardrail list

1. Supporting markers are always objects.
2. Signal state is always structured.
3. Contradiction / suppression has a governed home.
4. Confidence determinants have a governed home.
5. Cross-signal relationships are explicit or reference-governed.
6. Bucket-2 primitives get schema homes now.
7. Narrative stays outside promoted reasoning authority.
8. Runtime must not infer absent governed signal semantics.
9. Translation from gold investigation spec is deterministic and validator-enforced.
10. Legacy packages may be grandfathered only under explicit compatibility rules.
11. The promoted signal contract must remain governable and must not absorb hypotheses, phenotype contracts, intervention registries, or user-state overlays into one object.

---

# Section 10 — Final decision summary

## Working table

| Decision area | Status | Notes |
|---|---|---|
| Downstream questions | Agreed | Promoted signal contract must support clinician, engine, cohort, and audit use cases, not just activation. |
| Strong signal-level answer definition | Agreed | Must express state, support, ambiguity, context, and governed traceability. |
| Primitive triage | Agreed | Important signal primitives are triaged across now / schema-home-now / deferrable buckets. |
| Structured / narrative / reference classification | Agreed | Reasoning-critical items are structured or reference-governed; narrative remains downstream. |
| Boundary decisions | Agreed | Signal package enriched, but hypotheses, registries, and overlays remain explicit neighbours. |
| Full target vs v1 reconciliation | Agreed | v1 contract broader than today, but not monolithic. |
| Translation stance | Agreed | Deterministic reduction from gold investigation spec, validator-enforced. |
| Structural risk check | Agreed | Main rewrite traps identified and addressed. |
| Guardrails | Agreed | Non-negotiable guardrails defined. |
| Ready for architecture decision sprint | Yes | The signal-contract architecture decision sprint can now be authored with bounded scope. |

## Final decision statement

The promoted signal contract should evolve from a thin activation object into a governed signal-intelligence contract.
It must become rich enough to support strong signal-level answers, clinician-grade synthesis, and future cohort value, but it must not absorb adjacent WHY, phenotype, intervention, context, and longitudinal layers into one ungovernable structure. fileciteturn13file5 fileciteturn13file12

The correct architectural stance is therefore:

- enrich the promoted signal contract where the primitive is signal-semantic and reasoning-critical
- keep explanation-specific reasoning in adjacent WHY assets
- use governed references for confirmatory tests, interactions, phenotype links, context sensitivity, intervention sensitivity, and evidence provenance
- keep user-state and longitudinal observations out of the promoted package
- enforce deterministic translation from gold investigation spec into promoted signal intelligence

This is the shape most aligned to HealthIQ’s strategic ambition to become the deterministic operating system for metabolic interpretation and, in time, a strategic infrastructure asset rather than a thin report product. fileciteturn13file14

---

## Suggested next-step instruction for the architecture decision sprint

The next sprint should:

1. define the v1 promoted signal-intelligence contract formally
2. lock explicit boundaries to hypothesis assets, registries, and overlays
3. define deterministic translation rules from investigation-spec v3
4. introduce validator rules for semantic completeness
5. specify bounded grandfathering rules for legacy signal packages

It should **not** attempt to fully populate every bucket-2 primitive in the same sprint.

---

## Final reminder

A missing enrichment field later is survivable.
A wrongly shaped promoted signal contract is expensive.
