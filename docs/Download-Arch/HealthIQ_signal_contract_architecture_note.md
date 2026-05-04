# HealthIQ AI — Signal Contract Architecture Note

## Purpose

This note sets out:

1. the contract and knowledge assets we have today
2. the architectural problem we have just exposed
3. why the problem matters to the end-to-end intelligence stack
4. the proposed strategic direction for consensus before further contract hardening or runtime expansion

This is not a sprint prompt.
This is an architectural decision paper.

---

## 1. Current asset landscape

HealthIQ currently has multiple contract layers across the intelligence stack. They are individually useful, but they are not yet unified into one gold end-to-end signal contract.

### 1.1 Upstream gold authoring contract: investigation spec

The strongest and richest contract currently in the stack is the gold-standard pre-ingestion biomarker investigation spec:

- `investigation_spec_contract_version_20_gold_final.yaml`

This is effectively the most expressive authored clinical/research representation we currently have before downstream promotion.

At a high level, the gold investigation schema carries materially richer structure than the promoted signal package schema. In practical terms, it can express:

- biomarker identity and metadata
- clinical context and interpretation framing
- signal definitions
- activation conditions
- signal states / tiering
- supporting markers
- structured hypotheses
- hypothesis ranking
- confirmatory tests
- override rules
- evidence references
- narrative / explanation framing

This matters because it is already much closer to the kind of structured intelligence object we ultimately want the system to reason from.

### 1.2 Knowledge Bus promoted package contract

The current downstream promoted signal/package layer is governed through the Knowledge Bus. In practice, package validation is centred around:

- `research_brief.yaml`
- `signal_library.yaml`
- `package_manifest.yaml`
- package-level validation via `validate_knowledge_package.py`

This is a real governed contract, but it is narrower than the gold investigation authoring schema.

The current promoted signal-library contract focuses on signal-level runtime essentials such as:

- `signal_id`
- name / description
- system
- primary metric
- supporting metrics
- dependencies
- thresholds
- activation logic

That is enough to define a governed signal package for activation and threshold behaviour.
It is not enough, on its own, to represent the full WHY layer we want for root-cause reasoning.

### 1.3 Root-cause / WHY assets

The WHY layer is currently not embedded directly inside the promoted signal package contract.
Instead, it is represented separately via root-cause hypothesis assets and compiler wiring.

In practical terms, that means:

- signal package contract defines the signal
- separate root-cause hypothesis YAML defines WHY competition / evidence structure
- runtime compiler consumes those hypothesis assets
- intervention/context overlays remain separate again

So the platform currently uses a **layered contract model**, not a single unified promoted intelligence object.

### 1.4 Intervention and user-state contracts

We have recently strengthened the intervention side materially:

- class-level intervention-effects registry
- deterministic alias resolution
- separate user intervention/exposure schema
- additive runtime annotation layer
- explicit boundary: no threshold mutation, no signal-state override, no hypothesis mutation

This area is now better governed than the signal/WHY contract relationship in one important sense:
its boundaries are explicit.

### 1.5 Runtime consumption layer

The runtime consumes these layers through distinct paths rather than a single canonical signal intelligence object.

In simplified terms:

- signal activation/state logic comes from signal package assets
- WHY / root-cause competition comes from separate hypothesis assets
- intervention caveat/confounder annotations come from a separate overlay path
- compiler/runtime logic stitches these together

This works, but it also exposes where authority is fragmented.

---

## 2. The architectural problem we have just exposed

### 2.1 Problem statement

We do **not** currently have one gold-standard, locked, runtime-authoritative signal package schema equivalent in richness and authority to the gold pre-ingestion biomarker investigation schema.

That is the core problem.

Put bluntly:

- upstream gold authoring is rich
- downstream promotion is governed but thinner
- WHY reasoning lives partly outside the signal package contract
- runtime understanding therefore depends on multiple adjacent contracts rather than one canonical promoted signal intelligence object

### 2.2 Why this surfaced now

This surfaced during KB-S46 readiness analysis.

The insulin resistance and systemic inflammation signal packages were in good enough shape structurally:

- validator-passing
- stable IDs
- threshold governance now settled
- bounded runtime integration path identified

But the WHY layer for those same domains did not exist yet in governed root-cause hypothesis assets.

That exposed an important truth:

**a valid promoted signal package is not the same thing as a complete promoted reasoning object**.

In other words, the current signal package schema can say:

- this signal exists
- this is how it activates
- these are the thresholds
- these are the supporting metrics

But it cannot, by itself, fully say:

- these are the competing hypotheses
- this is the evidence-for model
- this is the evidence-against model
- this is the confirmatory pathway
- this is the ranked WHY reasoning structure

That intelligence is currently split across contracts.

### 2.3 What makes this strategically important

This is not just a documentation issue.
This is an intelligence-stack architecture issue.

If not addressed deliberately, the platform risks:

- duplicated concepts across authoring and promoted layers
- semantic loss during promotion
- unclear authority boundaries
- runtime stitching logic becoming the de facto integrator of meaning
- difficulty knowing which layer is the true source of truth for a signal’s full intelligence model
- future drift between upstream authored richness and downstream runtime truth

For a deterministic platform, that is dangerous.

The system must not rely on “soft understanding” of how separate files are meant to line up.
It needs explicit, governed, validator-enforced contract boundaries and translation rules.

---

## 3. Current contract asymmetry

The simplest way to describe the asymmetry is this:

| Layer | Current strength | Current weakness |
|---|---|---|
| Gold investigation spec | Rich, expressive, clinically meaningful authoring object | Not the direct runtime/promoted contract |
| Signal package (`signal_library.yaml`) | Governed, validator-backed, promotion-ready | Too thin to carry full WHY intelligence |
| Root-cause hypothesis YAML | Supports WHY reasoning explicitly | Separate from signal package, so authority is split |
| Runtime compiler | Deterministic consumption path exists | Risk that code becomes the place where contract gaps are compensated |

This is why the question arose at all.

If a true gold promoted signal contract existed, it would be obvious where signal intelligence lived.
At present, it is distributed.

---

## 4. What the gold investigation spec is already telling us

The existing gold biomarker investigation schema is useful not just as an ingestion artefact, but as a design signal for end-state contract shape.

It already demonstrates that a serious intelligence object for a biomarker/signal domain needs structured support for at least:

### 4.1 Core identity and classification

- biomarker / domain identity
- canonical IDs
- related signal IDs
- system/domain placement
- dependencies / supporting marker relationships

### 4.2 Detection and state logic

- activation conditions
- state definitions / tiers
- threshold framing
- override rules
- supporting markers and contextual markers

### 4.3 WHY reasoning

- competing hypotheses
- structured evidence for each hypothesis
- structured evidence against each hypothesis
- confirmatory tests
- hypothesis ordering / ranking logic
- missing-data awareness

### 4.4 Explanation and communication

- evidence references
- narrative framing
- clinical interpretation language
- explanation structure that can be consumed consistently

### 4.5 Governance implications

That means the gold investigation spec is already richer than the current promoted signal package contract in exactly the areas that matter for world-class WHY reasoning.

So the design question is not whether richer structure is needed.
That is already answered.

The real design question is:

**how should that richness be represented downstream in the promoted runtime intelligence model?**

---

## 5. Why the current state is acceptable temporarily, but not as the end-state

### 5.1 Why it is acceptable for now

The current layered model is acceptable as an interim maturity state because:

- it allows bounded progress
- signal activation and threshold logic can be governed independently
- WHY reasoning can be added incrementally
- intervention/context can remain isolated from core signal truth
- additive architecture has prevented premature contamination of older contracts

That was the correct move during the maturity detour.

### 5.2 Why it is not acceptable as the final contract model

As the platform scales, the current split becomes increasingly costly.

The more signals we add, the more painful it becomes if:

- upstream authored intelligence is richer than promoted runtime truth
- the mapping between them is implicit rather than explicit
- signal package meaning requires multiple adjacent assets to reconstruct
- different teams form different mental models of where “the real signal definition” lives

That is exactly how architectural ambiguity turns into platform drag.

---

## 6. Strategic decision now required

We need consensus on the intended end-state contract strategy.

### Decision question

Should HealthIQ continue with a deliberately layered model where:

- signal package contract remains relatively lean
- WHY reasoning remains in separate root-cause hypothesis assets
- other overlays remain separate

with better translation/governance between them,

**or**

should HealthIQ move toward a richer unified promoted signal-intelligence contract that absorbs more of the gold investigation-spec structure into one runtime-authoritative governed object?

That is the real architectural decision.

---

## 7. My proposed solution

My recommendation is **not** to do a reckless big-bang schema merger.

The correct strategic move is a controlled contract-unification programme.

### 7.1 Proposed end-state principle

HealthIQ should define a **gold promoted signal intelligence contract** that becomes the authoritative runtime-level representation of signal intelligence.

That contract should clearly define, for each signal domain:

- identity and metadata
- activation/state logic
- supporting/dependent markers
- WHY reasoning structure
- confirmatory pathways
- evidence requirements
- allowed narrative/explanation structure
- boundaries with intervention/context overlays

In other words:

the promoted contract should eventually be rich enough that the system can understand a signal domain from governed data, not from loosely coordinated adjacent artefacts.

### 7.2 Important boundary: do not collapse everything into one giant file

The end-state does **not** have to mean one monolithic YAML file.

What matters is not physical file count.
What matters is **contract authority**.

A good end-state could still use multiple physical artefacts, provided that:

- they are all part of one explicit promoted contract family
- their boundaries are formal and validator-enforced
- translation from gold investigation spec is deterministic
- runtime authority is unambiguous
- semantic loss is controlled and auditable

So the real objective is:

**unified contract authority, not necessarily single-file storage**.

### 7.3 Short-term recommendation

Do not block KB-S46 on this strategic issue.

For now:

- proceed with KB-S46 using the current additive architecture
- require high-quality governed hypothesis assets
- do not compensate in runtime for content thinness
- keep signal thresholds / state logic / intervention boundaries untouched

That is still the right local decision.

### 7.4 Medium-term recommendation

Run a dedicated architecture hardening/design sprint to define:

1. the target promoted signal-intelligence contract shape
2. the boundary between signal package, WHY hypothesis, and intervention/context layers
3. deterministic translation rules from gold investigation spec to promoted runtime artefacts
4. which concepts remain separated by design and why
5. validator responsibilities at each layer
6. the migration path from current layered reality to the agreed end-state

This should be a design/governance sprint first, not an implementation scramble.

---

## 8. Proposed decision statement for team discussion

Suggested framing for consensus discussion:

> HealthIQ currently has a rich upstream gold investigation authoring contract and a governed downstream signal package contract, but not yet a unified gold promoted signal-intelligence contract at equivalent richness. This creates a contract asymmetry where full signal intelligence is distributed across signal packages, root-cause hypothesis assets, and other overlays. The proposed strategic direction is to define the target end-state promoted signal-intelligence contract and its deterministic translation path from upstream gold investigation specs, while continuing near-term delivery through the current additive architecture.

---

## 9. Recommended next actions

1. Align the team on whether the end-state should be:
   - lean layered contract family, or
   - richer unified promoted signal-intelligence contract
2. Agree that current state is an interim maturity state, not final architecture
3. Preserve KB-S46 as a bounded WHY sprint under current architecture
4. Schedule a dedicated architecture decision sprint for signal contract unification / authority design
5. Do not allow runtime code to become the hidden place where upstream/downstream contract gaps are bridged informally

---

## 10. Bottom line

We have not discovered that the platform is broken.

We have discovered that the platform’s signal intelligence contract is **not yet fully unified**.

That is a strategic architecture issue, not a tactical bug.

The correct response is:

- recognise the current layered model for what it is
- prevent code from papering over contract asymmetry
- deliberately design the end-state promoted signal-intelligence contract
- then harden toward that end-state in a governed way

That is how we protect determinism while scaling toward a world-class intelligence stack.
