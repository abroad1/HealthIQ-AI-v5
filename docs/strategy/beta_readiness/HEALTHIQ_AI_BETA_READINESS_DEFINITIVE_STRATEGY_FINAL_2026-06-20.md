# HealthIQ AI — Definitive Beta Readiness Strategy and Delivery Plan

**Version:** FINAL v1.0  
**Date:** 20 June 2026  
**Programme context:** HealthIQ AI internal validation → controlled beta readiness  
**Audience:** HealthIQ AI leadership, architecture, product, engineering, research, safety, clinical review and validation contributors  
**Status:** Final consolidated strategy baseline for team review, ratification and use as the basis of the eight-block beta-readiness build strategy  
**Intended repository path:** `docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md`  
**Supersedes:** all separate 18 June 2026 beta-readiness strategy drafts and synthesis drafts listed in Appendix A  

---

## 1. Purpose of this document

This document is the definitive strategy reset for the HealthIQ AI beta-readiness build programme.

It consolidates the best governance, architecture, delivery strategy and review material from the recent strategy papers, audits, ADRs, UAT evidence and independent synthesis review. It is intended to be the team’s shared reference point for the next phase of work so that the programme can continue safely even when ChatGPT, Cursor, Claude Code or other tool windows lose context.

This document is deliberately not a short chat summary. It is a durable strategy baseline that explains:

- where HealthIQ AI stands now;
- what has been audited and decided;
- why the product is not yet beta-ready;
- what already exists and must not be reinvented;
- the canonical Layer A / Layer B / Layer C architecture;
- the eight beta-readiness blocks;
- the current maturity of each block;
- the reusable asset estate;
- the governance and delivery rules for future sprints;
- the six-phase delivery programme;
- the expanded planning map for downstream sprints;
- the first three recommended work packages;
- the beta-readiness gates;
- the major risks and controls;
- the decisions the team needs to make before proceeding.

This document does not authorise implementation by itself. It does not replace the formal ADRs, source code, Knowledge Bus SOP, Automation Bus SOP, runtime contracts, audit papers or package-level evidence. It is the strategic consolidation layer that explains how those materials fit together and how they should guide the next 20–40 sprints.

---

## 2. Executive summary

### 2.1 HealthIQ AI is not starting again

HealthIQ AI is materially beyond a prototype concept.

The platform already has a functioning deterministic medical intelligence architecture, governed Knowledge Bus controls, Pass 3 research assets, Knowledge Bus packages, runtime DTOs, clinician and narrative report structures, replay/versioning concepts, Sentinel validation material, UAT evidence, and a now-corrected Layer A / Layer B / Layer C architecture model.

The recent estate audits showed that the product is richer and more coherent than it first appeared. The correct strategy is therefore not to restart, not to rebuild from memory, and not to ask an LLM to invent a new application plan in isolation.

The correct strategy is structured completion.

### 2.2 HealthIQ AI is not beta-ready yet

The product remains in internal validation. It is not ready for external or controlled beta exposure.

The main launch-blocking gaps are:

- only three of the six intended launch-core consumer domains are currently implemented and visible on the results page;
- the missing launch-core domains are blood / iron / oxygen, thyroid / energy regulation, and kidney function;
- those missing domains have research material in the Knowledge Bus but are not yet assembled as complete governed domain cards and output surfaces;
- subsystem depth remains uneven and deliberately constrained in places;
- Layer B prose, explainer and boilerplate coverage is incomplete;
- the retail explainer registry appears to cover materially fewer biomarkers than the full launch-relevant biomarker estate;
- Gemini narrative synthesis is inactive and not validated;
- Layer C presentation/Gemini cannot yet be trusted as a downstream translator;
- UX trust issues remain even after UAT hardening;
- phenotype, edge-case, incomplete-panel and suppression validation is not broad enough;
- there is not yet a single executed beta-readiness gate artefact;
- prior security hygiene blockers, including secrets/environment concerns, have not been confirmed fully resolved.

### 2.3 The central strategic correction

HealthIQ AI is not “an LLM writing a blood report”.

It is a deterministic medical intelligence platform that uses governed research, lab-derived reference ranges, evidence-based signal logic, controlled medical interpretation, clinician-grade reporting, traceable provenance and reusable explanation assets. A downstream presentation layer may later translate that governed output into a compelling consumer experience, but it must not become the reasoning engine.

The user should ultimately feel:

> “I had no idea that is how my body worked, and now I understand why this marker matters.”

That experience must come primarily from governed Layer B intelligence and explanation assets, not from uncontrolled LLM prose.

### 2.4 The locked architecture

The layer model is now locked for roadmap planning:

```text
Layer A = ingestion, parsing, canonical facts and lab-range preservation
Layer B = all deterministic medical intelligence, WHY, hierarchy, surfacing, safety and provenance
Layer C = presentation, wording, arrangement and translation only
Gemini = optional constrained Layer C component, not the analytical engine
Frontend = render-only, no medical inference
```

This is the main architectural guardrail for every future sprint.

### 2.5 The immediate next move

The next move is not direct implementation.

The first work package must be:

```text
P1-1 — Launch-core domain build-materials map
```

P1-1 must map the existing packages, Pass 3 / investigation specs, signals, biomarkers, subsystem candidates, prose assets, clinician-report assets and test fixtures for the three missing launch-core domains:

- blood / iron / oxygen;
- thyroid / energy regulation;
- kidney function.

Only after that mapping is complete should the first missing launch-core domain implementation package be selected.

---

## 3. Source basis and document hierarchy

### 3.1 Source papers consolidated

This final document consolidates the strongest material from:

1. `HEALTHIQ_AI_BETA_READINESS_PROGRAMME_RESET_2026-06-18_v0.2.md`  
   Used for the strategic spine, architecture framing, eight-block structure, delivery principles and immediate sequencing.

2. `HEALTHIQ_AI_BETA_READINESS_PROGRAMME_RESET_2026-06-18 (1).md`  
   Used for the durable long-form programme context, detailed evidence base, reusable asset inventory, expanded delivery map, risks and team review framing.

3. `HEALTHIQ_AI_BETA_READINESS_PROGRAMME_BRIEF_2026-06-18.md`  
   Used for the sharper factual baseline, beta blockers, missing-domain specifics, security/secrets gate, concise sprint framing and decision structure.

4. `HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_2026-06-18_v1.0.md`  
   Used as the first GPT-led consolidation, especially for the long-form governance and strategy integration.

5. `HEALTHIQ_AI_BETA_READINESS_SYNTHESIS_CONFIRMED_v1.0_2026-06-18.md`  
   Used for independent synthesis improvements: clearer executive structure, sharper next-step framing, cleaner beta gates, and stronger decision-required section.

### 3.2 What this document supersedes

This document supersedes the separate strategy drafts and synthesis drafts as the single team-facing strategy baseline.

The superseded drafts should be retained as source history, but they should not be treated as competing strategy authorities after this document is ratified.

### 3.3 Governing repository authorities

The formal architecture and programme authority remains in the governed repository documents created and merged through the Automation Bus / review process:

| Document | Role |
|---|---|
| `docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md` | Governing layer-boundary vocabulary for future roadmap planning |
| `docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_COMPARISON_AND_PROGRAMME_RECOMMENDATION_2026-06-18.md` | Canonical Cursor/Claude comparison and multi-sprint beta-readiness programme paper |
| `docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md` | Layer authority ranking after late-document discovery |
| `docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_LATE_DOCUMENT_ADDENDUM_2026-06-17.md` | Records impact of late-discovered documents |
| `docs/strategy/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` | Strategic north star for product and layer model |
| `docs/AUTHORITY_MAP.md` | Repository authority map |

### 3.4 Control-plane authorities

Automation and Knowledge Bus governance remain controlled by:

| Document | Role |
|---|---|
| `AUTOMATION_BUS_SOP_v1.3.1.md` | Governs work package execution, hardening, audit and merge discipline |
| `KNOWLEDGE_BUS_SOP_v1.3.1.md` | Governs package-layer knowledge validation, package readiness and package lifecycle |
| `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md` | Governs upstream Pass 3 / investigation-spec promotion into package and intelligence artefacts |

Important process rule learned during the recent cycle:

```text
Documentation-only Automation Bus work uses change_type: CONTENT, not DOCS.
```

---

## 4. Current strategic position

### 4.1 What has just happened

The programme has completed a major architecture and strategy consolidation sequence:

1. Cursor produced an eight-block beta-readiness estate audit.
2. Claude produced a parallel eight-block beta-readiness estate audit.
3. Late-discovered strategic and frontend policy documents were incorporated.
4. A Layer Architecture Authority Index was created and revised.
5. A Layer Boundary Reconciliation ADR was created, reviewed, accepted through a governed exception after a prompt classification issue, then merged.
6. A Cursor/Claude comparison and multi-sprint programme recommendation paper was created and merged.
7. UAT R2 evidence corrected stale UAT R1 high-severity findings.
8. The repository was cleaned.
9. The programme baseline was merged to `main`.
10. GPT ratified `ADR-LAYER-BOUNDARY-RECONCILIATION-1` for roadmap-planning purposes alongside the programme recommendation paper.
11. Three strategy documents and an independent synthesis were reviewed and consolidated into this final strategy baseline.

The latest known programme baseline from the merge reports is:

- `ADR-LAYER-BOUNDARY-RECONCILIATION-1` merged and ratified for roadmap planning;
- `EIGHT_BLOCK_BETA_READINESS_COMPARISON_AND_PROGRAMME_RECOMMENDATION_2026-06-18.md` merged;
- `main` published at `16eee6b` after programme merge;
- working tree reported clean;
- no runtime code changed during ADR and programme planning sprints;
- next recommended package: `P1-1 — Launch-core domain build-materials map`.

### 4.2 What has been proven

The recent strategy, architecture, audit and UAT work has established that:

- the HealthIQ AI estate is richer and more coherent than first assumed;
- the platform has enough architecture and assets to justify completion, not reinvention;
- the Layer A / Layer B / Layer C boundary is now clear enough to govern roadmap planning;
- Layer B must remain the source of medical truth;
- Layer C, Gemini and frontend code must not reason medically;
- recent UAT hardening improved the product, but does not justify external beta exposure;
- the next phase should begin with mapping and consolidation, not direct implementation.

### 4.3 What already exists

The current estate includes:

- deterministic analytical engine components;
- signal evaluators, domain assembler logic and root-cause compiler foundations;
- Knowledge Bus governance and Pass 3 promotion controls;
- approximately 186–187 Knowledge Bus packages, with the exact count to be verified by P1-1;
- approximately 153 Pass 3 / investigation-spec research materials;
- three visible launch-core domain/card areas, currently understood as metabolic, cardiovascular and inflammation;
- `ClinicianReportV1`, `NarrativePayloadV1` and `InterpretationDisplayLayerV1` style Layer B / report surfaces;
- result versioning and replay policy concepts;
- Sentinel packs, AB/VR panels, phenotype fixtures and UAT evidence;
- User Health to Systems Map as the systems taxonomy authority;
- scoring policy, primary concern policy, domain narrative contracts and retail explainer boundaries;
- retail explainer and pathway explainer assets, though coverage is incomplete.

### 4.4 What remains incomplete

The current launch-blocking gaps are:

- three missing launch-core domain cards / system outputs:
  - blood / iron / oxygen;
  - thyroid / energy regulation;
  - kidney function;
- uneven subsystem depth;
- partial Layer B prose, explainer and boilerplate coverage;
- partial clinician-report completeness across launch-core domains;
- retail explainer coverage materially below the full biomarker estate;
- Gemini narrative synthesis not active, not validated and not ready for runtime use;
- insufficient phenotype and edge-case validation breadth;
- replay/auditability coverage needing strengthening before beta;
- remaining UX trust, hierarchy, marker-count and journey clarity work;
- no single consolidated beta-readiness gate artefact;
- unresolved or unconfirmed security/secrets/environment blockers from prior checks.

### 4.5 What must not be reinvented

The next phase must preserve and reuse, not recreate:

- User Health to Systems Map;
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
- Layer Boundary Reconciliation ADR and related authority index.

---

## 5. Strategic objective

The objective is not to ship quickly.

The objective is:

> Complete HealthIQ AI in the right order so that controlled beta, when explicitly approved, rests on deterministic medical truth, provenance, auditability, safe explanation, complete launch-core coverage and a coherent product surface.

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

## 6. Canonical architecture now locked

The Layer A/B/C boundary is no longer open for casual reinterpretation.

### 6.1 Layer A — ingestion and canonical facts

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

### 6.2 Layer B — deterministic medical intelligence

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

### 6.3 Layer C — presentation and translation only

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

### 6.4 Gemini — optional constrained presentation component

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

### 6.5 Frontend — render only

The frontend may render, filter, arrange and display governed outputs.

The frontend must not:

- calculate medical meaning;
- infer missing markers;
- rank concerns;
- determine severity;
- reinterpret biomarkers;
- generate new claims.

---

## 7. Product identity and differentiation

HealthIQ AI’s differentiator is not that it can produce a long report with an LLM.

Its differentiator is that it can produce a fascinating, personalised, systems-level explanation of the human body from blood results while remaining grounded in deterministic medical logic, provenance and safety constraints.

The product should help users understand:

- what their blood results show;
- how biomarkers relate to wider body systems;
- why a marker may matter;
- what evidence supports or complicates the interpretation;
- what is missing or uncertain;
- what questions may be worth discussing with a clinician;
- how the body works as an interconnected system.

The “wow” experience should come primarily from governed Layer B assets:

- biomarker explainers;
- system explainers;
- subsystem explainers;
- pathway explainers;
- lifestyle-context explainers;
- missing-marker explainers;
- counter-evidence explainers;
- clinician report sections;
- safe consumer wording;
- hierarchy and WHY reasoning.

Gemini can improve presentation later, but it must not invent the medical story.

---

## 8. The eight beta-readiness blocks

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

### 8.1 Block 1 — Core health systems model

Purpose:

Ensure HealthIQ has a coherent user-facing systems model, not a loose set of biomarker observations.

Current position:

- Strategic systems taxonomy exists.
- User Health to Systems Map is the taxonomy authority.
- Three of six launch-core domains are implemented and visible on the results page.
- Blood/iron/oxygen, thyroid/energy regulation and kidney function are missing from complete domain-card implementation.

Target:

- all launch-core domains mapped, assembled and validated;
- each domain has biomarker coverage, scoring logic, evidence inputs, card/output behaviour and tests;
- domains are coherent to the user and traceable to Layer B.

### 8.2 Block 2 — Subsystems and depth model

Purpose:

Move beyond shallow top-level system summaries into meaningful subsystem reasoning.

Current position:

- subsystem concepts exist;
- depth is uneven;
- MED-REV-1 deliberately constrains subsystem visibility in places;
- some runtime/card outputs do not yet express the richness of the underlying research estate.

Target:

- each core system has a minimum viable subsystem model;
- subsystem outputs remain governed by Layer B;
- subsystems inform explanation, hierarchy, missing-marker and counter-evidence logic;
- subsystem behaviour is tested across representative panels.

### 8.3 Block 3 — Layer B intelligence, WHY, clinician report and boilerplate prose estate

Purpose:

Build the true HealthIQ intelligence substrate.

Current position:

- strong foundations exist in `ClinicianReportV1`, `NarrativePayloadV1`, interpretation display records, root-cause assets, primary concern policy and domain narrative contracts;
- prose/explainer coverage is incomplete;
- retail explainer registry appears to cover materially fewer biomarkers than the full launch-relevant biomarker estate;
- the product cannot rely on Gemini to create medical explanation improvisationally.

Target:

- Layer B can produce governed explanation material for biomarker, pathway, system, subsystem and phenotype-level interpretation;
- clinician and consumer explanation assets are selected deterministically;
- missing markers and counter-evidence are explained safely;
- output is educational, engaging, traceable, non-diagnostic and non-alarmist.

### 8.4 Block 4 — Layer C presentation and constrained Gemini

Purpose:

Present governed Layer B intelligence beautifully without introducing new medical reasoning.

Current position:

- narrative payload and presentation concepts exist;
- Gemini is not active for runtime narrative synthesis;
- older prompt/spec material may be stale or misleading;
- Layer C/Gemini test coverage is underdeveloped.

Target:

- Layer C presents governed Layer B outputs;
- Gemini, if activated, operates only within strict constraints;
- Layer C output is schema-bound and validator-gated;
- no medical reasoning is delegated to Layer C.

### 8.5 Block 5 — Results page and UX product layer

Purpose:

Build a trustworthy, coherent user experience around stable architecture.

Current position:

- results page has improved after UAT hardening;
- R2 UAT shows high issues resolved/downgraded;
- residual MEDIUM/LOW issues remain;
- marker count clarity, hierarchy, trust language and domain completeness still need work.

Target:

- results page reflects complete Layer B outputs;
- no frontend inference;
- user understands marker count, missing data, hierarchy, confidence and why findings matter;
- report feels polished but remains faithful to governed Layer B outputs.

### 8.6 Block 6 — Medical safety, research provenance and governance

Purpose:

Preserve clinical credibility and prevent unsafe inference.

Current position:

- Knowledge Bus SOP, Pass 3 promotion, launch gate, package provenance and research-to-runtime traceability provide strong foundations;
- some context-dependent packages remain blocked or gated;
- thyroid, androgen and DHEA-S work shows the importance of cautious activation decisions.

Target:

- every activated runtime signal has provenance;
- research material is promoted through controlled pathways;
- medical claims are traceable;
- lab-provided ranges remain the interpretation authority where present;
- safety rules prevent speculative, diagnostic or alarmist output.

### 8.7 Block 7 — Auditability, reproducibility and regulatory-grade traceability

Purpose:

Make outputs reproducible, explainable and governable.

Current position:

- `ReplayManifestV1`, result versioning, stale/incompatible banner logic and launch-core replay policies exist;
- earlier false incompatible/stale issues were resolved;
- broader replay and Sentinel coverage is still required before beta.

Target:

- every result can be reproduced against versioned inputs, packages, policies and output components;
- compatibility/versioning accurately distinguishes current from stale/incompatible outputs;
- changes in intelligence or presentation can be regression-tested;
- audit artefacts support clinical, product and regulatory review.

### 8.8 Block 8 — Phenotype panels, edge-case estate and beta validation gates

Purpose:

Prove behaviour across the range of users and panels the product may see.

Current position:

- some phenotype fixtures, AB/VR panels and Sentinel packs exist;
- more contexts, incomplete panels and edge cases are needed;
- product validation should remain internal.

Target:

- representative phenotype panels exist across age, sex, metabolic, endocrine, renal, iron, inflammation and lifestyle contexts;
- suppression and counter-evidence tests exist;
- beta readiness is gated by evidence, not optimism;
- CEO/human approval is required before external exposure.

---

## 9. Current maturity assessment

| Block | Current maturity | Evidence confidence | Main gap | Beta relevance |
|---|---:|---:|---|---|
| 1. Core health systems model | Medium | High | Three missing launch-core domains | Essential |
| 2. Subsystems and depth model | Low–Medium | Medium | Depth uneven and constrained | Essential for differentiation |
| 3. Layer B intelligence/prose/clinician substrate | Medium | High | WHY/prose/explainer coverage partial | Essential |
| 4. Layer C/Gemini presentation | Low | Medium | Gemini inactive; constraints/tests not ready | Later-stage dependency |
| 5. Results page/UX | Medium | High | Residual trust and coverage gaps | Essential before beta |
| 6. Safety/provenance/governance | Medium–High | High | Some packages/signals remain gated | Essential |
| 7. Auditability/replay | Medium | Medium–High | More end-to-end replay and regression coverage needed | Essential |
| 8. Phenotype/beta validation | Low–Medium | Medium | Edge-case and phenotype estate insufficient | Essential |

Overall assessment:

HealthIQ AI is architecturally viable and strategically coherent, but not yet ready for external beta use. It is ready for a structured internal beta-readiness programme.

---

## 10. Current estate summary

### 10.1 What already exists

The product already has:

- strategic vision;
- corrected Layer A/B/C architecture boundary;
- systems taxonomy authority;
- Knowledge Bus governance;
- Pass 3 research corpus;
- approximately 186–187 Knowledge Bus packages, exact count to be verified;
- approximately 153 Pass 3 investigation specs;
- runtime DTOs and contracts;
- `NarrativePayloadV1`;
- `ClinicianReportV1`;
- interpretation display layer concepts;
- root-cause compiler assets;
- primary concern policy;
- domain narrative contracts;
- scoring policy;
- Wave 1 domain assembler patterns;
- health system card assets;
- retail explainer registry;
- pathway explainers;
- result versioning and stale/incompatible banner logic;
- replay policy / replay manifest concepts;
- Sentinel packs;
- AB/VR/golden panels;
- phenotype fixtures;
- internal UAT R1/R2 evidence;
- frontend journey recommendations;
- results-page hardening evidence.

### 10.2 What is partial

The following are real but incomplete:

- launch-core domain coverage;
- subsystem depth;
- Layer B prose/explainer substrate;
- clinician-report completeness;
- consumer education assets;
- Layer C/Gemini readiness;
- results-page trust and clarity;
- phenotype/edge-case validation;
- replay/auditability breadth;
- security/secrets gate confirmation.

### 10.3 What is missing or insufficient for beta

Still missing or insufficient:

- blood/iron/oxygen domain card and subsystem wiring;
- thyroid/energy regulation domain card and subsystem wiring;
- kidney function domain card and subsystem wiring;
- mapped build materials for all missing launch-core domains;
- sufficiently rich Layer B boilerplate/explainer estate;
- full prose/explainer coverage matrix;
- Gemini activation design, prompt constraints and validator tests;
- controlled Gemini narrative pilot, if later approved;
- progressive disclosure and journey IA redesign;
- complete beta-readiness gate artefact;
- enough validation across representative cases;
- confirmed resolution of prior security/secrets blockers.

### 10.4 What must not be reinvented

Do not recreate the following unless mapping proves they are unusable:

- User Health to Systems Map;
- Wave 1 domain assembler patterns;
- scoring policy;
- Knowledge Bus packages;
- Pass 3 research;
- `NarrativePayloadV1`;
- `ClinicianReportV1`;
- interpretation display layer concepts;
- retail explainer registry;
- pathway explainers;
- phenotype fixtures;
- replay/versioning logic;
- Sentinel packs;
- Pass 3 promotion protocol;
- Layer Boundary Reconciliation ADR.

---

## 11. Reusable asset inventory

This inventory is a strategic starting point for P1-1 and subsequent mapping sprints. It must be verified against the repository during each work package.

### 11.1 Authority assets

| Asset | What it gives us | Future use |
|---|---|---|
| Strategic Vision v1.5 | Product and architecture north star | Strategic alignment for all future sprints |
| Layer Boundary Reconciliation ADR | Canonical Layer A/B/C vocabulary | Prevents Layer C/Gemini/frontend drift |
| User Health to Systems Map | User-facing system taxonomy | Authority for domain completion |
| Knowledge Bus SOP | Package governance | Research-to-runtime safety |
| Pass 3 Promotion Protocol | Upstream research promotion controls | Prevents raw research/runtime confusion |
| Scoring policy | Domain/card scoring rails | Aligns domain implementation |
| Domain narrative contracts | Safe domain-specific output behaviour | Governs report/presentation constraints |
| Primary concern policy | Hierarchy/ranking philosophy | Layer B surfacing and ambiguity handling |
| Retail explainer boundaries | Consumer wording safety | Prose/boilerplate expansion controls |

### 11.2 Runtime and Layer B assets

| Asset | What it gives us | Future use |
|---|---|---|
| Wave 1 domain assembler patterns | Existing domain/card assembly approach | Reuse for missing launch-core domains |
| Knowledge Bus packages | Research-backed intelligence material | Inputs for missing domains |
| Pass 3 investigation specs | Rich research source estate | Promotion and package validation |
| `ClinicianReportV1` | Clinician-oriented structured report | Clinician report expansion |
| `NarrativePayloadV1` | Governed Layer B-to-Layer C handoff | Future presentation/Gemini substrate |
| Interpretation Display Layer concepts | Structured display outputs | Results page and report rendering |
| Root-cause compiler assets | WHY reasoning foundations | Layer B explanation hierarchy |
| Retail explainer registry | Consumer explanation assets | Boilerplate/prose expansion |
| Pathway explainers | Mechanistic explanation copy | “Wow” educational content |

### 11.3 Safety, provenance and auditability assets

| Asset | What it gives us | Future use |
|---|---|---|
| Package provenance | Traceability | Claim audit and promotion checks |
| Output authority provenance | Claim/source links | Safety and review gates |
| Lab-range tests/policies | Range correctness | Prevent unsafe interpretation |
| ReplayManifestV1 | Component/version traceability | Reproducible outputs |
| Result versioning policy | Stale/incompatible result lifecycle | Trustworthy result handling |
| LAUNCH-CORE-3 | Replay/regeneration policy | Launch-core validation |
| Sentinel packs | Defect-class regression guards | Regression and suppression testing |

### 11.4 Testing and validation assets

| Asset | What it gives us | Future use |
|---|---|---|
| AB/VR/golden panels | Known test inputs | Regression coverage |
| Phenotype fixtures | User/panel diversity | Beta validation |
| Suppression tests | Safety validation | Prevent overclaiming |
| UAT R1/R2 evidence | Product trust evidence | UX gate and regression evidence |
| Internal UAT scripts/reports | User-facing validation | Internal validation reruns |

---

## 12. Strategic delivery principles

### 12.1 Use existing authority before creating new content

Every sprint must begin by identifying the governing documents, policies, packages, specs and contracts. New logic must not be invented where existing governed assets already exist.

### 12.2 Complete Layer B before activating Gemini

Gemini must not fill gaps in medical reasoning or prose. If Layer B cannot provide a governed brief, the answer is to complete Layer B, not to ask Gemini to improvise.

### 12.3 Keep medical reasoning deterministic and traceable

All runtime medical interpretation must be governed, deterministic and traceable. LLMs may support research workflows or presentation experiments, but runtime reasoning must remain controlled.

### 12.4 Frontend remains render-only

The frontend may render, filter, arrange and display governed outputs. It must not calculate medical meaning, infer missing markers, rank concerns, determine severity, reinterpret biomarkers or generate new claims.

### 12.5 Use lab-provided ranges where available

Lab-provided reference ranges are the interpretation authority where present. Global/default ranges must not override lab ranges. Derived ratios may be calculated only where the lab has not provided them, and only through governed and traceable logic.

### 12.6 No fallback parser

The product must not introduce fallback or dummy parsing behaviour. Parsing must use the deterministic parser, or an explicitly enabled and governed LLM-backed parser when authorised.

### 12.7 UX follows architecture

UX should be compelling, but it must sit on stable Layer B outputs. UX polish before domain completion and hierarchy stability risks creating a polished interface that misrepresents incomplete intelligence.

### 12.8 Outcome-based sprints, not micro-sprints

The programme should use meaningful outcome-based sprint packages. Work should only be split where safety, clinical review, architectural boundaries, STOP gates or governance genuinely require it.

### 12.9 Internal-validation framing

The product remains in internal validation. External or controlled beta exposure requires explicit CEO approval after beta-readiness gates are passed.

### 12.10 Beta readiness must be gated explicitly

Domain completion, subsystem depth, Layer B prose, safety, provenance, replay, UX trust, phenotype validation, security and CEO approval are all required gates.

---

## 13. Programme structure

The programme should be understood at two levels.

### 13.1 Formal programme baseline

The formal baseline is a six-phase programme with approximately sixteen primary sprint packages.

This is the baseline established by the merged programme recommendation paper and reinforced by the independent synthesis.

### 13.2 Expanded planning decomposition

The expanded 30-sprint map in this document is a planning decomposition showing likely downstream work packages. It is not a fixed delivery commitment.

The detailed map should be refined after P1-1 and P2-1 because those mapping sprints will reveal which assets are genuinely implementation-ready and which require additional research, safety review or governance work.

---

## 14. Six-phase programme baseline

### Phase 0 — Governance and evidence consolidation

Goal:

Ensure the team is using the correct authorities before building.

Completed or near-complete:

- Layer Boundary Reconciliation ADR;
- Cursor/Claude programme recommendation paper;
- audit closure records;
- UAT R2 correction;
- definitive strategy document.

Remaining:

- team review and ratification of this document;
- compact authority pack index if needed;
- consolidated beta-readiness gate artefact;
- agreement that P1-1 is the next package;
- confirmation no major authority documents are missing.

### Phase 1 — Systems and subsystem completion

Goal:

Complete missing launch-core domains and minimum subsystem depth.

Primary domains:

- blood / iron / oxygen;
- thyroid / energy regulation;
- kidney function.

Primary sprint sequence:

- P1-1: Launch-core domain build-materials map;
- P1-2: blood/iron/oxygen implementation package;
- P1-3: thyroid/energy regulation implementation package;
- P1-4: kidney function implementation package;
- P1-5: subsystem minimum viable depth;
- P1-6: cross-domain system coherence pass.

### Phase 2 — Layer B WHY, prose and clinician substrate

Goal:

Complete the deterministic explanation estate that makes HealthIQ educational, clinically credible and differentiated.

Primary sprint sequence:

- P2-1: Layer B prose/explainer gap matrix;
- P2-2: retail explainer registry expansion;
- P2-3: pathway and missing-marker explainer pack;
- P2-4: NarrativePayload brief hardening;
- P2-5: clinician-report launch-core expansion;
- P2-6: consumer boilerplate selection rules;
- P2-7: counter-evidence and uncertainty explanation sprint.

### Phase 3 — Safety, provenance and auditability

Goal:

Harden traceability, replayability, versioning, safety and research-to-output credibility.

Primary sprint sequence:

- P3-1: research-to-runtime provenance trace;
- P3-2: lab-range protection audit;
- P3-3: signal activation safety gate;
- P3-4: replay and result-versioning hardening;
- P3-5: output authority provenance;
- P3-6: security/secrets/environment gate.

### Phase 4 — Layer C presentation and constrained Gemini

Goal:

Design and test presentation/translation only after Layer B substrate is ready.

Primary sprint sequence:

- P4-1: Layer C schema and allowed-action contract;
- P4-2: Gemini prompt and validator design;
- P4-3: deterministic presentation templates;
- P4-4: Gemini sandbox/offline evaluation;
- P4-5: Gemini activation decision gate.

### Phase 5 — Results page and UX product layer

Goal:

Build the consumer experience around stable Layer B outputs and user trust.

Primary sprint sequence:

- P5-1: results-page information architecture redesign;
- P5-2: domain/system card UX implementation;
- P5-3: primary finding and hierarchy UX;
- P5-4: marker count and uploaded-data clarity;
- P5-5: full report journey polish;
- P5-6: internal UAT rerun.

### Phase 6 — Beta validation and release gates

Goal:

Prove behaviour across panels, phenotypes, edge cases and user contexts before controlled beta.

Primary sprint sequence:

- P6-1: phenotype panel expansion;
- P6-2: edge-case and suppression testing;
- P6-3: end-to-end replay regression pack;
- P6-4: safety and provenance beta gate;
- P6-5: internal beta gate execution;
- P6-6: CEO controlled beta decision paper.

---

## 15. First recommended work packages

### 15.1 First: P1-1 — Launch-core domain build-materials map

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
- recommended sequencing for P1-2 onwards;
- exact package count verification.

Recommended classification:

```yaml
risk_level: HIGH
change_type: CONTENT
execution_model: TWO_PHASE_START_FINISH
```

Rationale for HIGH:

P1-1 is documentation/mapping only, but it is architecture-critical. It maps the build materials for missing launch-core medical domains and will determine the safe sequencing of later implementation. A wrong map could misdirect multiple downstream HIGH-risk domain sprints. Therefore, it should follow HIGH-governance discipline even though it must not change runtime behaviour.

Must not do:

- no runtime code;
- no signal activation;
- no new domain logic;
- no frontend changes;
- no Gemini;
- no implementation.

### 15.2 Second: P2-1 — Layer B prose/explainer gap matrix

This is the second strategic work package. It may be prepared in parallel with P1-1 if capacity allows, but it must not overtake P1-1 for domain implementation decisions.

Purpose:

Identify what Layer B prose, boilerplate and explainer assets already exist and what is missing.

Required outputs:

- biomarker explainer gap matrix;
- system explainer gap matrix;
- subsystem explainer gap matrix;
- pathway explainer gap matrix;
- clinician report gap matrix;
- consumer education gap matrix;
- missing-marker explanation requirements;
- counter-evidence explanation requirements;
- priority list for deterministic prose expansion.

Recommended classification:

```yaml
risk_level: HIGH
change_type: CONTENT
execution_model: TWO_PHASE_START_FINISH
```

Rationale for HIGH:

P2-1 is documentation/mapping only, but it defines the Layer B explanatory substrate. If this mapping is wrong, the programme may either underbuild the “wow” experience or incorrectly push explanation responsibility into Gemini/Layer C. It should therefore follow HIGH-governance discipline even without code changes.

Must not do:

- no runtime LLM activation;
- no frontend polish;
- no uncontrolled prose generation;
- no medical logic changes.

### 15.3 Third: P1-2 — First missing launch-core domain implementation package

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
- scoring/card integration readiness;
- absence of unresolved signal-activation blockers.

Recommended classification:

```yaml
risk_level: HIGH
change_type: BEHAVIOUR or MIXED, depending final scope
execution_model: TWO_PHASE_START_FINISH
```

Must not do:

- do not implement all missing domains at once unless P1-1 proves this is safe and governable;
- do not bypass medical review for context-dependent signals;
- do not use Layer C to compensate for incomplete Layer B;
- do not introduce frontend inference;
- do not use global/default ranges where lab ranges exist;
- do not activate blocked signals casually.

---

## 16. Expanded planning decomposition

This section provides a longer-range decomposition. Some work packages may later be combined if P1-1 and P2-1 show the dependencies are simple. They should not be split further unless safety, clinical review, signal activation, parser/range logic, runtime contracts or STOP gates require it.

### Phase 0 — Reset and authority consolidation

#### Sprint 0.1 — Programme reset and definitive strategy document

Objective:

Produce the durable team-facing strategy document.

Type:

`CONTENT`

Outputs:

- definitive strategy paper;
- team review baseline;
- decision record for next sprint.

#### Sprint 0.2 — Team review and ratification

Objective:

Gather team feedback and ratify or amend the programme baseline.

Type:

`CONTENT`

Outputs:

- comments and challenge log;
- accepted amendments;
- final ratified v1.0 or v1.1;
- decision to start P1-1.

#### Sprint 0.3 — Authority pack index

Objective:

Create a compact index of all authority documents needed for future sprints.

Type:

`CONTENT`

Outputs:

- one-page authority index;
- “read before sprint” map;
- stale/superseded warning list.

#### Sprint 0.4 — Consolidated beta-readiness gate artefact

Objective:

Turn the beta-readiness gates in this strategy into an executable review checklist.

Type:

`CONTENT`

Outputs:

- beta-readiness gate checklist;
- evidence requirements;
- owner/approver fields;
- pass/fail/blocked status model.

### Phase 1 — Systems and subsystem completion

#### Sprint 1.1 — Launch-core domain build-materials map

Objective:

Identify all existing build materials for missing launch-core domains.

Type:

`CONTENT`

Layers touched:

Mapping only. No runtime change.

Domains:

- blood / iron / oxygen;
- thyroid / energy regulation;
- kidney function.

Outputs:

- package/spec map;
- biomarker map;
- signal status map;
- subsystem candidate map;
- prose/explainer asset map;
- tests/fixtures map;
- implementation readiness assessment;
- recommended first implementation domain.

This is the next sprint.

#### Sprint 1.2 — Blood / iron / oxygen implementation package

Objective:

Implement or complete the blood/iron/oxygen domain using mapped assets.

Type:

Likely `BEHAVIOUR` or `MIXED`, depending whether new governed content assets are loaded by runtime.

Layers touched:

Layer B and runtime display contract.

Outputs:

- completed domain assembler/card logic if missing;
- biomarker coverage;
- scoring alignment;
- subsystem wiring;
- test coverage;
- provenance map.

STOP gates:

- medical safety review if new signal activation is required;
- no global ranges where lab ranges exist;
- no activation of unreviewed ambiguous patterns.

#### Sprint 1.3 — Thyroid / energy regulation implementation package

Objective:

Complete thyroid/energy domain using existing thyroid research and runtime assets.

Type:

Likely `BEHAVIOUR` or `MIXED`.

Layers touched:

Layer B.

Outputs:

- domain logic;
- thyroid biomarker handling;
- low/high thyroid pattern handling consistent with medical review;
- missing-marker/counter-evidence handling;
- tests.

STOP gates:

- FT3 low and context-dependent thyroid concerns must remain governed by prior clinical review outcomes;
- no unsafe activation of context-dependent signals.

#### Sprint 1.4 — Kidney function implementation package

Objective:

Complete kidney function domain using existing renal/Kidney Bus assets.

Type:

Likely `BEHAVIOUR` or `MIXED`.

Layers touched:

Layer B.

Outputs:

- renal domain logic;
- eGFR/creatinine/urea/electrolyte mappings as applicable;
- lab-range and age-context handling;
- tests.

STOP gates:

- avoid diagnostic claims;
- preserve educational framing;
- maintain lab-range authority.

#### Sprint 1.5 — Subsystem minimum viable depth

Objective:

Define and implement minimum subsystem depth across launch-core domains.

Type:

Likely `MIXED`.

Layers touched:

Layer B.

Outputs:

- subsystem taxonomy;
- system-to-subsystem mapping;
- display requirements;
- tests.

#### Sprint 1.6 — Cross-domain system coherence pass

Objective:

Ensure domains do not produce contradictory or disconnected interpretations.

Type:

Likely `MIXED`.

Layers touched:

Layer B.

Outputs:

- cross-domain consistency checks;
- domain interaction rules;
- missing-marker/counter-evidence interactions;
- regression tests.

### Phase 2 — Layer B WHY, prose and clinician substrate

#### Sprint 2.1 — Layer B prose/explainer gap matrix

Objective:

Identify what prose/explainer assets already exist and what is missing.

Type:

`CONTENT`

Layer touched:

Layer B planning.

Outputs:

- biomarker explainer gap matrix;
- system explainer gap matrix;
- pathway explainer gap matrix;
- clinician report gap matrix;
- missing-marker/counter-evidence prose requirements;
- prioritised prose substrate roadmap.

#### Sprint 2.2 — Retail explainer registry expansion

Objective:

Expand consumer explainer coverage for launch-core biomarkers.

Type:

`CONTENT` or `MIXED`, depending whether runtime-loaded assets are modified.

Layer touched:

Layer B asset selection.

Outputs:

- new or expanded explainer entries;
- safety wording review;
- coverage tests if runtime-loaded.

#### Sprint 2.3 — WHY and root-cause explanation substrate

Objective:

Strengthen WHY/root-cause explanation assets.

Type:

Likely `MIXED`.

Layer touched:

Layer B.

Outputs:

- deterministic root-cause explanation selection;
- pathway explanation support;
- evidence/counter-evidence handling;
- tests.

#### Sprint 2.4 — NarrativePayload brief hardening

Objective:

Ensure the governed Layer B-to-Layer C brief is sufficient for future deterministic presentation and any constrained Gemini use.

Type:

Likely `BEHAVIOUR` or `MIXED`.

Layer touched:

Layer B/C contract.

Outputs:

- payload adequacy assessment;
- missing fields if any;
- validator implications;
- no Gemini activation.

#### Sprint 2.5 — ClinicianReportV1 launch-core expansion

Objective:

Ensure clinician report surfaces all launch-core domains and evidence correctly.

Type:

Likely `MIXED`.

Layer touched:

Layer B.

Outputs:

- clinician report sections;
- evidence traceability;
- missing-marker handling;
- report tests.

#### Sprint 2.6 — Consumer boilerplate selection rules

Objective:

Define deterministic rules for selecting user-facing explanation modules.

Type:

Likely `MIXED`.

Layer touched:

Layer B.

Outputs:

- selection rules;
- severity/uncertainty wording constraints;
- no speculative claims;
- tests.

#### Sprint 2.7 — Missing-marker and counter-evidence explanation sprint

Objective:

Make absence, uncertainty and conflicting evidence understandable without alarmism.

Type:

Likely `MIXED`.

Layer touched:

Layer B.

Outputs:

- missing-marker explainer rules;
- counter-evidence wording;
- suppression rules;
- tests.

### Phase 3 — Safety, provenance and auditability

#### Sprint 3.1 — Research-to-runtime provenance trace

Objective:

Verify activated outputs can be traced to packages and research authority.

Type:

`CONTENT` or `MIXED`.

Layer touched:

Governance / Layer B.

Outputs:

- provenance matrix;
- gap list;
- remediation plan.

#### Sprint 3.2 — Lab-range protection audit

Objective:

Ensure biomarker interpretation uses lab-provided reference ranges where available.

Type:

Likely `MIXED`.

Layer touched:

Layer A/B boundary.

Outputs:

- lab-range compliance tests;
- no-default-range checks;
- exception map for derived ratios.

#### Sprint 3.3 — Signal activation safety gate

Objective:

Review active, inactive and blocked signals for beta-readiness safety.

Type:

`CONTENT` or `MIXED`.

Layer touched:

Layer B.

Outputs:

- signal activation matrix;
- blocked/context-dependent signal list;
- STOP gates for unresolved signals.

#### Sprint 3.4 — Replay and result-versioning hardening

Objective:

Ensure outputs are reproducible and versioned correctly.

Type:

Likely `MIXED`.

Layer touched:

Auditability.

Outputs:

- replay tests;
- compatibility checks;
- stale/incompatible banner regression tests.

#### Sprint 3.5 — Output authority provenance

Objective:

Ensure user-visible and clinician-visible claims carry appropriate authority.

Type:

Likely `MIXED`.

Layer touched:

Layer B / Layer C handoff.

Outputs:

- output provenance manifest;
- claim-to-source tracing;
- tests.

#### Sprint 3.6 — Security/secrets/environment gate

Objective:

Confirm no committed secrets, unsafe config, environment leakage or deployment-readiness gaps.

Type:

Likely `MIXED` or testing/governance.

Layer touched:

Infrastructure/governance.

Outputs:

- secrets audit;
- environment checklist;
- remediation actions if needed;
- pre-beta security gate status.

### Phase 4 — Layer C presentation and constrained Gemini

#### Sprint 4.1 — Layer C schema and allowed-action contract

Objective:

Define exactly what Layer C may receive and output.

Type:

`CONTENT`

Layer touched:

Layer C contract only.

Outputs:

- schema;
- allowed actions;
- prohibited actions;
- validation approach.

#### Sprint 4.2 — Gemini prompt and validator design

Objective:

Design constrained Gemini use without activation.

Type:

`CONTENT`

Layer touched:

Layer C planning.

Outputs:

- prompt template;
- prohibited action list;
- validator requirements;
- anti-hallucination test plan.

No runtime activation.

#### Sprint 4.3 — Layer C deterministic presentation templates

Objective:

Improve presentation without LLM dependency.

Type:

Likely `MIXED`.

Layer touched:

Layer C presentation.

Outputs:

- report templates;
- section ordering;
- wording polish;
- no new medical claims.

#### Sprint 4.4 — Gemini sandbox/offline evaluation

Objective:

Test Gemini output against governed payloads without production activation.

Type:

`CONTENT` or `MIXED`, depending harness design.

Layer touched:

Layer C test harness.

Outputs:

- sandbox test outputs;
- hallucination/fidelity assessment;
- validator results;
- CEO decision evidence.

#### Sprint 4.5 — Gemini activation decision gate

Objective:

Decide whether Gemini should be activated and under what constraints.

Type:

`CONTENT`

Layer touched:

Governance.

Outputs:

- activation decision paper;
- safety sign-off;
- CEO approval requirement.

### Phase 5 — Results page and UX product layer

#### Sprint 5.1 — Results-page information architecture redesign

Objective:

Redesign around completed Layer B outputs.

Type:

`CONTENT`

Layer touched:

UX only.

Outputs:

- UX structure;
- hierarchy model;
- no-inference rules.

#### Sprint 5.2 — Domain/system card UX implementation

Objective:

Render complete domain cards cleanly.

Type:

Likely `MIXED`.

Layer touched:

Frontend render only.

Outputs:

- domain card UI;
- subsystem display;
- no frontend medical logic.

#### Sprint 5.3 — Primary finding and hierarchy UX

Objective:

Make lead findings, caveats and context clear.

Type:

Likely `MIXED`.

Layer touched:

Frontend render only.

Outputs:

- primary finding UI;
- uncertainty/counter-evidence display;
- trust wording.

#### Sprint 5.4 — Marker count and uploaded-data clarity

Objective:

Avoid confusion over uploaded markers, key markers and scored/expected markers.

Type:

Likely `MIXED`.

Layer touched:

Frontend render only.

Outputs:

- marker count model;
- “not uploaded” handling;
- clearer UI labels.

#### Sprint 5.5 — Full report journey polish

Objective:

Build the end-to-end consumer journey.

Type:

Likely `MIXED`.

Layer touched:

Layer C/frontend presentation only.

Outputs:

- report sections;
- narrative flow;
- callouts;
- safe education.

#### Sprint 5.6 — Internal UAT rerun

Objective:

Re-test the full results journey with current architecture.

Type:

`CONTENT` / testing.

Layer touched:

Validation.

Outputs:

- UAT report;
- defect list;
- go/no-go for beta validation phase.

### Phase 6 — Beta validation and release gates

#### Sprint 6.1 — Phenotype panel expansion

Objective:

Expand representative panels and user contexts.

Type:

`CONTENT` or `MIXED`.

Layer touched:

Testing.

Outputs:

- panel matrix;
- fixtures;
- expected behaviours.

#### Sprint 6.2 — Edge-case and suppression testing

Objective:

Validate safe behaviour in ambiguous, conflicting or incomplete cases.

Type:

Likely `MIXED`.

Layer touched:

Layer B/testing.

Outputs:

- suppression tests;
- counter-evidence tests;
- missing-marker tests.

#### Sprint 6.3 — End-to-end replay regression pack

Objective:

Ensure outputs remain stable and reproducible across versioned changes.

Type:

Likely `MIXED`.

Layer touched:

Auditability/testing.

Outputs:

- replay pack;
- regression reports;
- gate evidence.

#### Sprint 6.4 — Safety and provenance beta gate

Objective:

Confirm claims, provenance and safety constraints are beta-ready.

Type:

`CONTENT` / testing.

Layer touched:

Governance.

Outputs:

- safety gate report;
- provenance sign-off;
- unresolved risk list.

#### Sprint 6.5 — Internal beta gate execution

Objective:

Execute all beta gates and identify residual blockers.

Type:

`CONTENT` / testing.

Layer touched:

Governance/testing.

Outputs:

- gate status;
- blocker list;
- remediation plan.

#### Sprint 6.6 — CEO controlled beta decision paper

Objective:

Present final go/no-go evidence for controlled beta.

Type:

`CONTENT`

Layer touched:

Governance.

Outputs:

- beta readiness decision paper;
- unresolved risks;
- recommendation;
- CEO approval record.

---

## 17. Beta-readiness gates

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

## 18. Risks and controls

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
| Clinical review gaps | Context-dependent signals could be activated too broadly | Maintain STOP gates and require medical research review before activation |

---

## 19. STOP gates for future implementation sprints

Future work must stop and escalate if any of the following conditions arise:

- a sprint would move medical reasoning into Layer C, Gemini or frontend code;
- a sprint would introduce or rely on fallback parser behaviour;
- a sprint would substitute global/default reference ranges where lab ranges are available;
- a sprint would activate a context-dependent or clinically ambiguous signal without explicit medical review;
- a sprint would read raw Pass 3 research or raw package material at runtime contrary to architecture;
- a sprint would create user-facing medical claims without provenance;
- a sprint would change runtime contracts without audit/replay implications being reviewed;
- a sprint would implement UX that infers or reinterprets clinical meaning in the frontend;
- a sprint would advance toward external beta without the beta gates being executed;
- a sprint would proceed on an Automation Bus prompt that is not HARDENED where hardening is required.

---

## 20. Team ratification questions

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

## 21. Decision required

The team is asked to make four decisions.

### Decision 1 — Adopt this as the working strategy baseline

Adopt this document as the consolidated beta-readiness strategy baseline, replacing the separate draft papers and synthesis drafts as the single working strategy for the next phase.

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

## 22. Final recommendation

HealthIQ AI should proceed with a disciplined beta-readiness completion programme.

The platform is not starting again.

It is not yet ready for beta.

It is ready for structured internal completion.

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

## 23. One-page circulation summary

HealthIQ AI is not starting again.

Recent Cursor and Claude audits found that the product has a stronger architecture and richer asset base than was initially visible. It has a governed analytical engine, Knowledge Bus assets, Pass 3 research, runtime contracts, clinician/narrative/report structures, result versioning, replay policy, Sentinel guards and internal UAT evidence.

However, it is not externally beta-ready.

Three of six launch-core domains are implemented; the missing domains are blood/iron/oxygen, thyroid/energy regulation and kidney function. Layer B prose/explainer coverage is partial. Gemini is inactive and not validated. The phenotype and edge-case estate is insufficient. Security hygiene blockers from prior recheck have not yet been confirmed resolved. UX trust work remains.

The key architecture is now locked:

- Layer A ingests and canonicalises facts.
- Layer B owns medical intelligence, WHY, hierarchy, surfacing, clinician report, prose selection, safety and provenance.
- Layer C presents and translates governed Layer B output.
- Gemini, if used later, is constrained presentation only.
- Frontend is render-only.

The eight programme blocks are:

1. Core health systems model
2. Subsystems and depth model
3. Layer B deterministic intelligence, WHY, clinician report and prose estate
4. Layer C presentation/Gemini
5. Results page/UX
6. Medical safety, research provenance and governance
7. Auditability, reproducibility and traceability
8. Phenotype panels, edge cases and beta validation gates

The formal programme baseline is six phases and approximately sixteen primary sprint packages. The expanded delivery map is a planning decomposition, not a fixed commitment.

The next recommended sprint is P1-1: Launch-core domain build-materials map. It should identify exactly what already exists for blood/iron/oxygen, thyroid/energy and kidney function before any implementation begins.

The team is asked to review, challenge and ratify this final strategy as the basis for the eight-block beta-readiness build programme.
