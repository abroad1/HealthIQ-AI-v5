# HealthIQ AI — Definitive Beta Readiness Strategy

**Version:** v1.0 synthesis draft  
**Date:** 18 June 2026  
**Audience:** HealthIQ AI leadership, architecture, product, engineering, research, safety and validation reviewers  
**Status:** Definitive consolidated strategy for team ratification  
**Source basis:** Consolidated from the three 18 June 2026 strategy papers: Programme Reset and Layer Strategy v0.2, Programme Reset and Delivery Plan v0.1, and Programme Brief v0.1.  
**Intended repository path:** `docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_2026-06-18.md`

---

## 1. Executive summary

HealthIQ AI is not a prototype and should not be treated as a blank canvas.

The platform already has a functioning deterministic medical intelligence architecture, governed Knowledge Bus controls, Pass 3 research assets, Knowledge Bus packages, runtime DTOs, clinician and narrative report structures, replay/versioning concepts, Sentinel validation material, UAT evidence, and a now-corrected Layer A / Layer B / Layer C architecture model.

The strategic conclusion from the three reviewed papers is clear:

**HealthIQ AI should proceed through a structured internal beta-readiness completion programme, not a restart and not a rushed external beta.**

The product is materially advanced, but it is not ready for external or controlled beta exposure. It remains in internal validation until the missing launch-core domains, Layer B explanation substrate, safety/provenance controls, auditability, phenotype validation, UX trust and CEO approval gates are complete.

The product strategy is not to create “an LLM that writes blood reports”. HealthIQ AI is a deterministic medical intelligence platform that converts uploaded blood results and user context into governed, traceable, non-diagnostic, clinically cautious interpretation. A presentation layer may later translate that governed intelligence into a compelling consumer experience, but it must not become the reasoning engine.

The locked architecture is:

```text
Layer A = ingestion, parsing, canonical facts and lab-range preservation
Layer B = all deterministic medical intelligence, WHY, hierarchy, safety and provenance
Layer C = presentation, wording and translation only
Gemini = optional constrained Layer C component, not the analytical engine
```

The immediate next move is not direct implementation. The first work package must be:

```text
P1-1 — Launch-core domain build-materials map
```

This must map the existing packages, Pass 3 / investigation specs, signals, biomarkers, subsystem candidates, prose assets and test fixtures for the three missing launch-core domains:

- blood / iron / oxygen;
- thyroid / energy regulation;
- kidney function.

Only once that mapping is complete should the first missing launch-core domain implementation package be selected.

---

## 2. Current strategic position

### 2.1 What has been proven

Recent strategy, architecture, audit and UAT work has established that:

- the HealthIQ AI estate is richer and more coherent than first assumed;
- the platform has enough architecture and assets to justify completion, not reinvention;
- the Layer A / Layer B / Layer C boundary is now clear enough to govern future roadmap planning;
- Layer B must remain the source of medical truth;
- Layer C, Gemini and the frontend must not reason medically;
- recent UAT hardening has improved the product, but does not justify external beta exposure;
- the next phase should begin with mapping and consolidation, not direct code.

### 2.2 What already exists

The current estate includes:

- deterministic analytical engine components;
- signal evaluators, domain assembler logic and root-cause compiler foundations;
- Knowledge Bus governance and Pass 3 promotion controls;
- approximately 186–187 Knowledge Bus packages, with the exact count to be verified by P1-1;
- Pass 3 / investigation-spec research material;
- three visible launch-core domain/card areas, currently understood as metabolic, cardiovascular and inflammation;
- `ClinicianReportV1`, `NarrativePayloadV1` and `InterpretationDisplayLayerV1` style Layer B / report surfaces;
- result versioning and replay policy concepts;
- Sentinel packs, AB/VR panels, phenotype fixtures and UAT evidence;
- User Health to Systems Map as the systems taxonomy authority;
- scoring policy, primary concern policy, domain narrative contracts and retail explainer boundaries;
- retail explainer and pathway explainer assets, though coverage is incomplete.

### 2.3 What remains incomplete

The current launch-blocking gaps are:

- three missing launch-core domain cards / system outputs:
  - blood / iron / oxygen;
  - thyroid / energy regulation;
  - kidney function;
- uneven subsystem depth;
- partial Layer B prose, explainer and boilerplate coverage;
- partial clinician-report completeness across launch-core domains;
- retail explainer coverage that is materially below the full biomarker estate;
- Gemini narrative synthesis not active, not validated and not ready for runtime use;
- insufficient phenotype and edge-case validation breadth;
- replay/auditability coverage that needs strengthening before beta;
- remaining UX trust, hierarchy, marker-count and journey clarity work;
- no single consolidated beta-readiness gate artefact;
- unresolved or unconfirmed security/secrets/environment blockers from prior checks.

### 2.4 What must not be reinvented

The next programme phase must preserve and reuse, not recreate:

- the User Health to Systems Map;
- Wave 1 domain assembler and card patterns;
- Knowledge Bus packages;
- Pass 3 / investigation-spec research assets;
- `NarrativePayloadV1` and `ClinicianReportV1` contracts;
- interpretation display layer concepts;
- root-cause and pathway explainer assets;
- scoring policy;
- lab-range authority policy;
- result versioning and replay policy;
- Sentinel packs and existing validation fixtures;
- the Layer Boundary Reconciliation ADR and related authority index.

---

## 3. Strategic objective

The objective is not to ship quickly.

The objective is:

**Complete HealthIQ AI in the right order so that controlled beta, when explicitly approved, rests on deterministic medical truth, provenance, auditability, safe explanation, complete launch-core coverage and a coherent product surface.**

This means:

- no Gemini shortcut;
- no UX-first shortcut;
- no fallback parser;
- no frontend medical inference;
- no global/default ranges where lab ranges exist;
- no uncontrolled medical prose;
- no beta framing until the CEO explicitly approves external or controlled beta exposure.

Near-term work must remain framed as internal validation and architecture completion.

---

## 4. Locked architecture model

### 4.1 Layer A — ingestion and canonical facts

Layer A owns:

- file upload / input handling;
- parsing;
- factual extraction;
- biomarker canonicalisation;
- unit normalisation;
- preservation of lab-provided reference ranges;
- preservation of raw factual inputs;
- preparation of structured factual inputs for deterministic analysis.

Layer A must not:

- interpret medical meaning;
- score biomarkers or domains;
- activate signals;
- infer causality;
- rank findings;
- decide what to surface;
- create user-facing health conclusions.

### 4.2 Layer B — deterministic medical intelligence

Layer B is the source of medical truth.

Layer B owns:

- biomarker interpretation;
- signal activation and suppression;
- system and subsystem reasoning;
- phenotype mapping;
- WHY and root-cause reasoning;
- evidence and counter-evidence;
- missing-marker handling;
- confidence, completeness and reliability assessment;
- hierarchy and primary concern logic;
- surfacing and suppression decisions;
- clinician report content;
- interpretation display records;
- deterministic boilerplate and explainer selection;
- safety boundaries and prohibited claims;
- provenance and traceability for clinically meaningful claims.

Layer B decides:

- what matters;
- why it matters;
- how strongly it is supported;
- what complicates the interpretation;
- what is safe to say;
- what the user and clinician should see.

Any future sprint that moves these responsibilities into Layer C, Gemini, frontend code or uncontrolled templates is an architectural regression.

### 4.3 Layer C — presentation and translation only

Layer C owns:

- wording;
- arrangement;
- formatting;
- report composition;
- user-facing readability;
- deterministic presentation templates;
- constrained translation of governed Layer B outputs.

Layer C may make governed output clearer.

Layer C must not:

- reason medically;
- activate or suppress signals;
- rank findings;
- inspect raw biomarkers outside the governed Layer B payload;
- add new medical claims;
- change confidence or severity;
- override Layer B;
- read raw Pass 3 material or Knowledge Bus packages at runtime;
- perform frontend medical inference.

### 4.4 Gemini

Gemini is optional and later-stage.

If used, Gemini may only operate as a constrained Layer C presentation component working from a governed Layer B brief.

Gemini must not:

- become the analytical engine;
- decide what matters;
- rank findings;
- reason about biomarkers;
- invent explanations;
- create medical claims;
- change safety framing;
- compensate for missing Layer B prose or logic.

Gemini activation requires:

- sufficient Layer B prose / brief substrate;
- `NarrativePayloadV1` or equivalent governed payload readiness;
- explicit allowed-action and prohibited-action contract;
- anti-hallucination validation;
- output schema and validator;
- safety and provenance checks;
- internal-only sandbox evaluation;
- explicit CEO approval before controlled use.

---

## 5. The eight beta-readiness blocks

The programme is organised around eight blocks. These are not optional workstreams; they define the conditions for credible controlled beta readiness.

| Block | Purpose | Current maturity | Strategic action |
|---|---|---:|---|
| 1. Core health systems model | Complete coherent launch-core domain coverage | Medium | Map and complete missing domains |
| 2. Subsystems and depth | Provide meaningful system-level and subsystem-level reasoning | Low–Medium / Medium | Define minimum viable depth and wire missing domains |
| 3. Layer B intelligence, WHY, clinician report and prose | Build the real HealthIQ intelligence and explanation layer | Medium | Expand governed prose, WHY, report and explainer substrate |
| 4. Layer C / Gemini | Present governed output without adding reasoning | Low | Design later; do not activate early |
| 5. Results page / UX | Make outputs trustworthy and understandable | Medium | Redesign after Layer B stabilises |
| 6. Safety, provenance and governance | Preserve clinical credibility and traceability | Medium–High | Harden promotion, lab-range and claim provenance controls |
| 7. Auditability and replay | Make outputs reproducible and governable | Medium | Expand replay, versioning and regression evidence |
| 8. Phenotype and beta validation | Prove behaviour across representative cases | Low–Medium | Expand panels, edge cases and beta gates |

The most important sequencing rule is:

```text
Domain coverage + Layer B substrate before Layer C/Gemini and UX redesign.
```

---

## 6. Delivery principles

### 6.1 Use existing authority before creating new content

Every sprint must begin by identifying the governing documents, policies, packages, specs and contracts. New logic must not be invented where existing governed assets already exist.

### 6.2 Complete Layer B before activating Gemini

Gemini must not fill gaps in medical reasoning or prose. If Layer B cannot provide a governed brief, the answer is to complete Layer B, not to ask Gemini to improvise.

### 6.3 Keep medical reasoning deterministic and traceable

All runtime medical interpretation must be governed, deterministic and traceable. LLMs may support research workflows or presentation experiments, but runtime reasoning must remain controlled.

### 6.4 Frontend remains render-only

The frontend may render, filter, arrange and display governed outputs. It must not calculate medical meaning, infer missing markers, rank concerns, determine severity, reinterpret biomarkers or generate new claims.

### 6.5 Use lab-provided ranges where available

Lab-provided reference ranges are the interpretation authority where present. Global/default ranges must not override lab ranges. Derived ratios may be calculated only where the lab has not provided them, and only through governed and traceable logic.

### 6.6 No fallback parser

The product must not introduce fallback or dummy parsing behaviour. Parsing must use the deterministic parser, or an explicitly enabled and governed LLM-backed parser when authorised.

### 6.7 UX follows architecture

UX should be compelling, but it must sit on stable Layer B outputs. UX polish before domain completion and hierarchy stability risks creating a polished interface that misrepresents the intelligence.

### 6.8 Outcome-based sprints, not micro-sprints

The programme should use meaningful outcome-based sprint packages. Work should only be split where safety, clinical review, architectural boundaries, STOP gates or governance genuinely require it.

### 6.9 Internal-validation framing

The product remains in internal validation. External or controlled beta exposure requires explicit CEO approval after beta-readiness gates are passed.

---

## 7. Programme phases

The delivery programme is organised into six phases plus reset/ratification. The sprint list below is a working delivery map, not a rigid commitment to a fixed number of sprints. Sprints may be combined where dependencies are simple and governance permits. They must be split where safety or STOP gates require it.

### Phase 0 — Governance and evidence consolidation

Goal: ensure the team is using the correct authorities before building.

Outputs:

- definitive strategy document;
- team review and ratification;
- compact authority pack index;
- consolidated beta-readiness gate artefact.

Immediate actions:

- ratify this document as the programme baseline;
- confirm whether any major authority documents are missing;
- author P1-1.

### Phase 1 — Systems and subsystem completion

Goal: complete missing launch-core domains and minimum subsystem depth.

Primary missing domains:

- blood / iron / oxygen;
- thyroid / energy regulation;
- kidney function.

Expected outputs:

- launch-core domain build-materials map;
- package/spec/signal map;
- biomarker-to-domain map;
- subsystem candidate map;
- prose/explainer asset map;
- test/fixture map;
- domain implementation recommendations;
- selected first implementation package;
- completed domain card and subsystem wiring for each missing domain;
- cross-domain coherence tests.

### Phase 2 — Layer B WHY, prose and clinician substrate

Goal: complete the deterministic explanation estate that makes HealthIQ educational, clinically credible and differentiated.

Expected outputs:

- Layer B prose/explainer gap matrix;
- biomarker, system and pathway explainer coverage map;
- retail explainer expansion plan;
- clinician report expansion plan;
- missing-marker explanation rules;
- counter-evidence explanation rules;
- boilerplate selection rules;
- NarrativePayload brief hardening for future constrained presentation.

### Phase 3 — Safety, provenance and auditability

Goal: harden traceability, replayability, versioning, safety and research-to-output credibility.

Expected outputs:

- research-to-runtime provenance matrix;
- package-to-output traceability checks;
- lab-range protection audit;
- active/blocked/context-dependent signal safety matrix;
- replay coverage extension;
- result versioning regression pack;
- output authority provenance manifest;
- security/secrets/environment recheck.

### Phase 4 — Layer C presentation and constrained Gemini

Goal: define and test constrained presentation behaviour only after Layer B is sufficient.

Expected outputs:

- Layer C allowed-action contract;
- Layer C schema;
- Gemini prompt and validator design;
- prohibited-action list;
- anti-hallucination tests;
- internal-only sandbox evaluation;
- CEO decision evidence before activation.

No production Gemini activation should occur in this phase unless all agreed gates pass.

### Phase 5 — Results page and UX redesign

Goal: build a trustworthy consumer experience around stable Layer B outputs.

Expected outputs:

- results-page information architecture redesign;
- Journey v6 alignment where still applicable;
- progressive disclosure model;
- domain/system card UX;
- subsystem display policy;
- primary finding and hierarchy UX;
- marker count and uploaded-data clarity;
- trust wording;
- full internal UAT rerun.

Frontend remains render-only throughout.

### Phase 6 — Beta validation and release gates

Goal: prove behaviour across panels, phenotypes, edge cases and user contexts before any controlled external exposure.

Expected outputs:

- phenotype validation matrix;
- expanded panel fixtures;
- edge-case and suppression testing;
- end-to-end replay regression pack;
- beta-readiness gate report;
- unresolved risk list;
- security/secrets/environment gate evidence;
- CEO controlled beta decision paper.

---

## 8. First recommended work packages

### P1-1 — Launch-core domain build-materials map

This is the first work package.

Purpose:

Map exactly what already exists for the missing launch-core domains before any implementation begins.

Domains:

- blood / iron / oxygen;
- thyroid / energy regulation;
- kidney function.

Required outputs:

- Knowledge Bus package map;
- Pass 3 / investigation spec map;
- biomarker-to-domain map;
- signal activation and block-status map;
- subsystem candidate map;
- prose/explainer asset map;
- clinician report asset map;
- tests and fixtures map;
- implementation readiness assessment;
- recommended sequencing for P1-2 onwards.

Classification:

```yaml
risk_level: STANDARD
change_type: CONTENT
execution_model: TWO_PHASE_START_FINISH
```

Must not do:

- no runtime code;
- no signal activation;
- no new domain logic;
- no frontend changes;
- no Gemini;
- no implementation.

### P2-1 — Layer B prose/explainer gap matrix

This is the second strategic work package. It may be prepared in parallel with P1-1 if capacity allows, but it must not overtake P1-1 for domain implementation decisions.

Purpose:

Identify what Layer B prose, boilerplate and explainer assets already exist and what is missing.

Required outputs:

- biomarker explainer gap matrix;
- system explainer gap matrix;
- pathway explainer gap matrix;
- clinician report gap matrix;
- consumer education gap matrix;
- missing-marker explanation requirements;
- counter-evidence explanation requirements;
- priority list for deterministic prose expansion.

Classification:

```yaml
risk_level: STANDARD
change_type: CONTENT
execution_model: TWO_PHASE_START_FINISH
```

Must not do:

- no runtime LLM activation;
- no frontend polish;
- no uncontrolled prose generation;
- no medical logic changes.

### P1-2 — First missing launch-core domain implementation package

This must happen after P1-1.

Purpose:

Implement the first selected missing launch-core domain using mapped existing assets, not memory.

Likely candidate:

- blood / iron / oxygen, if P1-1 confirms strongest readiness and lowest clinical risk.

Selection criteria:

- existing package/spec support;
- biomarker scope clarity;
- safety and clinical complexity;
- available tests and fixtures;
- prose/explainer readiness;
- scoring/card integration readiness.

Classification:

```yaml
risk_level: HIGH
change_type: BEHAVIOUR or MIXED, depending final scope
execution_model: TWO_PHASE_START_FINISH
```

Must not do:

- do not implement all missing domains at once unless P1-1 proves it is safe and governable;
- do not bypass medical review for context-dependent signals;
- do not use Layer C to compensate for incomplete Layer B;
- do not introduce frontend inference;
- do not use global/default ranges where lab ranges exist.

---

## 9. Beta-readiness gates

Controlled beta must not proceed until the following gates pass.

### Gate 1 — Launch-core domain coverage

All intended launch-core domains must be mapped, implemented, tested and visible in a coherent user-facing way.

### Gate 2 — Subsystem depth and coherence

Each launch-core domain must have sufficient subsystem depth to support meaningful explanation, hierarchy and missing-marker handling.

### Gate 3 — Layer B evidence, WHY and prose substrate

Layer B must provide sufficient governed WHY, hierarchy, evidence, counter-evidence, clinician report content and prose selection to support a compelling and safe user experience.

### Gate 4 — Layer C / Gemini constraint

Layer C must be presentation-only. Gemini must remain inactive unless explicitly approved, validator-gated and constrained to governed Layer B briefs.

### Gate 5 — Medical safety and provenance

All clinically meaningful claims must be non-diagnostic, traceable, safe and governed. Context-dependent or blocked signals must remain controlled.

### Gate 6 — Lab-range and parser integrity

Lab-provided reference ranges must remain authoritative where available. No fallback parser or dummy parser behaviour may be introduced.

### Gate 7 — Auditability and replay

Results must be reproducible, versioned, regression-testable and auditable across package, policy, runtime and output changes.

### Gate 8 — UX trust

The results page must not confuse users about marker count, severity, hierarchy, missing data, confidence or what has and has not been interpreted.

### Gate 9 — Phenotype and edge-case validation

The product must be tested against representative panels, incomplete panels, conflicting evidence, suppression cases, age/sex/lifestyle contexts and relevant edge cases.

### Gate 10 — Security, secrets and environment

No unresolved high-severity security, secrets, unsafe configuration or environment-readiness blockers may remain.

### Gate 11 — CEO / human approval

External or controlled beta exposure requires explicit CEO approval based on a written evidence pack and unresolved-risk register.

---

## 10. Key risks and controls

| Risk | Why it matters | Control |
|---|---|---|
| Rebuilding from memory | Wastes the existing estate and may create contradictory logic | Start each sprint with authority and asset mapping |
| Gemini overreach | Could turn presentation into uncontrolled medical reasoning | No Gemini before Layer B substrate and validators are ready |
| Layer C drift | Presentation layer may begin deciding what to say medically | Enforce Layer Boundary Reconciliation ADR in every relevant sprint |
| Frontend inference | Undermines auditability and safety | Frontend render-only rule |
| UX-first shortcut | Polished surface may hide incomplete intelligence | UX implementation after Layer B outputs stabilise |
| Unsafe domain bundling | Too much medical/runtime behaviour may be changed at once | Outcome-based sprints with STOP gates and HIGH-risk routing |
| Over-fragmentation | Excessive governance drag slows delivery | Combine work where safe; split only where risk requires |
| Lab-range regression | Default ranges could override lab-specific interpretation | Lab-range protection audit and regression tests |
| Parser fallback regression | Could create false reassurance and unsafe parsing | No fallback parser policy |
| Security/secrets blockers | Could prevent safe beta regardless of intelligence maturity | Dedicated security/secrets/environment gate |
| Stale authority documents | Old prompts/specs could override current architecture | Authority pack index and stale-document warnings |
| Incomplete phenotype validation | Product may fail on realistic cases | Expanded phenotype, edge-case and suppression test estate |

---

## 11. Team ratification questions

The team should review this document and decide:

1. Is this now the correct definitive programme baseline?
2. Is the Layer A / Layer B / Layer C architecture stated clearly enough?
3. Does everyone agree Layer B owns medical truth, WHY, hierarchy, surfacing, clinician report, boilerplate selection, safety and provenance?
4. Does everyone agree Layer C, Gemini and frontend code must not reason medically?
5. Are any authority documents or material runtime assets missing from this strategy?
6. Is P1-1 the correct next sprint?
7. Can P2-1 safely run in parallel with P1-1, or should it wait?
8. Which missing launch-core domain is most likely to be safest for P1-2, subject to P1-1 evidence?
9. Are the beta-readiness gates complete?
10. What evidence would be required for the CEO to approve controlled beta exposure?

The intended outcome is not passive agreement. The team should either ratify the strategy, amend it, or identify where evidence does not support it.

---

## 12. Decision required

The team is asked to make four decisions.

### Decision 1 — Adopt this as the working strategy baseline

Adopt this document as the consolidated beta-readiness strategy baseline, replacing the three separate draft papers as the single working strategy for the next phase.

### Decision 2 — Author P1-1 next

Proceed to author:

```text
P1-1 — Launch-core domain build-materials map
```

This is a CONTENT sprint and must not include implementation.

### Decision 3 — Prohibit Gemini / UX-first shortcuts

Agree that no Gemini runtime activation or UX redesign implementation should precede launch-core domain mapping, domain completion, and sufficient Layer B prose/brief substrate.

### Decision 4 — Preserve Layer B as analytical truth

Agree that future sprint prompts, implementation work and audits must not move Layer B responsibilities into Layer C, Gemini, frontend code or uncontrolled runtime LLM paths.

---

## 13. Final recommendation

HealthIQ AI should proceed with a disciplined beta-readiness completion programme.

The platform is not starting again. It is not yet ready for beta. It is ready for structured internal completion.

The safest path is:

```text
1. Ratify the definitive strategy baseline.
2. Map missing launch-core domain build materials.
3. Map Layer B prose/explainer gaps.
4. Implement missing domains using existing governed assets.
5. Expand Layer B WHY/prose/clinician substrate.
6. Harden safety, provenance, replay and auditability.
7. Only then design constrained Layer C/Gemini behaviour.
8. Redesign UX around stable Layer B outputs.
9. Execute phenotype, edge-case, security and beta-readiness gates.
10. Seek CEO approval before any external or controlled beta exposure.
```

The product should not aim to be merely visually impressive. It must be medically credible, traceable, reproducible, safe, differentiated and genuinely useful.

That is the route to a HealthIQ AI product that can eventually support controlled beta with confidence rather than optimism.

---

## Appendix A — Source papers consolidated

This document consolidates:

1. `HEALTHIQ_AI_BETA_READINESS_PROGRAMME_RESET_2026-06-18_v0.2.md`  
   Used for the strategic spine, architecture framing, eight-block structure, delivery principles and immediate work-package sequencing.

2. `HEALTHIQ_AI_BETA_READINESS_PROGRAMME_RESET_2026-06-18 (1).md`  
   Used for the detailed evidence base, maturity framing, reusable asset inventory, programme phases, risks and longer-form delivery map.

3. `HEALTHIQ_AI_BETA_READINESS_PROGRAMME_BRIEF_2026-06-18.md`  
   Used for executive-level factual clarity, hard beta blockers, missing-domain specifics, security/secrets gate, concise sprint list and decision framing.

