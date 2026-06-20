# HealthIQ AI — Beta Readiness Definitive Strategy and Delivery Plan

**Version:** v1.0 definitive team review baseline  
**Date:** 18 June 2026  
**Audience:** HealthIQ AI leadership, architecture, product, engineering, research, safety and validation reviewers  
**Status:** Definitive strategy consolidation for team review and ratification  
**Intended repository path:** `docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_2026-06-18_v1.0.md`  

---

## 1. Purpose of this document

This document is the definitive beta-readiness strategy reset for HealthIQ AI.

It consolidates the strongest material from three preceding strategy drafts:

1. the long-form **Beta Readiness Programme Reset and Delivery Plan**;
2. the shorter **Beta Readiness Programme Reset and Layer Strategy**;
3. the concise **Beta Readiness Programme Brief**.

Its purpose is to preserve the full body of work completed across the recent Cursor, Claude, GPT and human review cycle so that the programme can continue safely even when ChatGPT, Cursor, Claude Code or other tool windows lose context.

This document should enable any reviewer joining the programme to understand:

- where HealthIQ AI stands now;
- what has been audited and decided;
- why the product is not yet beta-ready;
- what is already built and must not be reinvented;
- the canonical Layer A / Layer B / Layer C architecture;
- the eight beta-readiness blocks;
- the current maturity of each block;
- the reusable asset estate;
- the delivery principles for the next phase;
- the recommended 6-phase programme;
- the provisional expanded 30-sprint delivery map;
- the first three recommended work packages;
- the beta-readiness gates;
- the risks, dependencies and STOP gates;
- what the team needs to review, challenge and ratify.

This is not an implementation prompt. It does not authorise code changes. It does not replace the formal ADRs, audit papers, Knowledge Bus SOPs, Automation Bus SOPs or runtime source files. It is the strategic consolidation layer that explains how those materials fit together.

---

## 2. Executive summary

### 2.1 Where we are now

HealthIQ AI is materially beyond a prototype concept.

The product has a functioning deterministic medical intelligence platform, a governed analytical engine, a Knowledge Bus with approximately 187 packages, a Pass 3 research corpus, runtime DTOs, clinician and narrative report structures, result versioning, replay policy, Sentinel guards, UAT evidence, and an agreed layer architecture.

It is not a blank canvas and must not be treated as one.

Recent audits show that the estate is richer and more coherent than a first-glance assessment suggested. The correct strategy is to consolidate and complete the existing architecture, not rebuild the product from memory and not ask an LLM to invent a new plan in isolation.

### 2.2 What has been proven

The recent Cursor and Claude estate audits, late-document addendum, layer authority index, layer-boundary reconciliation ADR, UAT R1/R2 evidence, and multi-agent programme recommendation paper have collectively established the following:

- the product has strong structural foundations;
- the estate contains reusable research, package, runtime, report, prose, replay and validation assets;
- the product does not need to be restarted;
- the Layer A / B / C model is now clear enough to govern future sprint scoping;
- the internal UAT HIGH issue count moved from six to zero following trust-hardening work, although residual MEDIUM and LOW issues remain;
- the product is improving through disciplined completion;
- the next phase should begin with mapping and evidence consolidation, not immediate implementation;
- the product should remain in internal validation until beta-readiness gates are passed and the CEO explicitly approves external or controlled beta exposure.

### 2.3 The central strategic correction

HealthIQ AI is not “an LLM writing a blood report”.

It is a deterministic medical intelligence platform that uses governed research, lab-derived reference ranges, evidence-based signal logic, controlled medical interpretation, clinician-grade reporting, traceable provenance and reusable explanation assets. A downstream presentation layer may then translate that governed output into a compelling consumer experience.

This distinction is now foundational.

### 2.4 Why the product is not beta-ready yet

HealthIQ AI is not ready for external or controlled beta exposure because:

- only three of the six intended launch-core consumer domains are currently implemented and visible on the results page;
- the missing launch-core domains are blood / iron / oxygen, thyroid / energy regulation, and kidney function;
- those missing domains have research material in the Knowledge Bus but are not yet assembled as complete domain cards;
- subsystem depth remains uneven and deliberately constrained in places;
- Layer B prose, explainer and boilerplate coverage is partial;
- the retail explainer registry appears to cover approximately 17 of 79 key biomarkers;
- Gemini narrative synthesis is inactive and not validated;
- Layer C presentation/Gemini cannot yet be trusted as a downstream translator;
- UX trust issues remain even after UAT hardening;
- phenotype and edge-case validation is not broad enough;
- there is not yet a single consolidated beta-readiness gate artefact;
- prior security hygiene blockers, including secrets/environment concerns, have not been confirmed fully resolved.

### 2.5 What must be built before controlled beta

Before controlled beta, the product must complete or materially harden:

- missing launch-core domain coverage;
- minimum subsystem depth;
- Layer B WHY, prose, explainer and clinician-report substrate;
- safety, provenance and governance controls;
- replay, auditability and result-versioning coverage;
- phenotype, edge-case and suppression validation;
- UX trust and results-page clarity;
- constrained Layer C/Gemini design and validation, only after Layer B substrate is ready;
- explicit beta-readiness gates and CEO/human approval.

The programme objective is therefore not “ship something quickly”.

The objective is:

> Complete the platform in the right order so that controlled beta, when it happens, rests on deterministic medical truth, provenance, auditability, safety and a coherent product surface rather than on UX polish or LLM improvisation.

---

## 3. Document hierarchy and current authority position

This document consolidates three strategy drafts into a single v1.0 baseline.

### 3.1 Superseded strategy drafts

The following drafts are now treated as source inputs, not competing authority documents:

- `HEALTHIQ_AI_BETA_READINESS_PROGRAMME_RESET_2026-06-18 (1).md`
- `HEALTHIQ_AI_BETA_READINESS_PROGRAMME_RESET_2026-06-18_v0.2.md`
- `HEALTHIQ_AI_BETA_READINESS_PROGRAMME_BRIEF_2026-06-18.md`

Their strongest content has been absorbed here.

### 3.2 Governing architecture documents

The formal architectural and programme authority remains in the repository documents created and merged through the governed workflow:

| Document | Role |
|---|---|
| `docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md` | Governing layer-boundary vocabulary for future roadmap planning |
| `docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_COMPARISON_AND_PROGRAMME_RECOMMENDATION_2026-06-18.md` | Canonical Cursor/Claude comparison and multi-sprint beta-readiness programme paper |
| `docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md` | Layer authority ranking after late-document discovery |
| `docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_LATE_DOCUMENT_ADDENDUM_2026-06-17.md` | Records impact of late-discovered documents |
| `docs/strategy/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` | Strategic north star for the product and layer model |
| `docs/AUTHORITY_MAP.md` | Repository authority map |

### 3.3 Control-plane authority

Automation and Knowledge Bus governance remain controlled by:

| Document | Role |
|---|---|
| `AUTOMATION_BUS_SOP_v1.3.1.md` | Governs work package execution, hardening, audit and merge discipline |
| `KNOWLEDGE_BUS_SOP_v1.3.1.md` | Governs package-layer knowledge validation, package readiness and package lifecycle |
| `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md` | Governs upstream Pass 3 / investigation-spec promotion into package and intelligence artefacts |

Important process rule learned during this cycle:

> Documentation-only Automation Bus work uses `change_type: CONTENT`, not `DOCS`.

---

## 4. What has just happened

The programme has completed a major architecture and strategy consolidation sequence:

1. Cursor produced an eight-block beta-readiness estate audit.
2. Claude produced a parallel eight-block beta-readiness estate audit.
3. Late-discovered strategic and frontend policy documents were incorporated.
4. A Layer Architecture Authority Index was created and revised.
5. A Layer Boundary Reconciliation ADR was created, reviewed, accepted as a governed exception after a prompt classification issue, then merged.
6. A Cursor/Claude comparison and multi-sprint programme recommendation paper was created and merged.
7. UAT R2 evidence corrected stale UAT R1 high-severity findings.
8. The repository was cleaned.
9. The programme baseline was merged to `main`.
10. GPT ratified `ADR-LAYER-BOUNDARY-RECONCILIATION-1` for roadmap-planning purposes alongside the programme recommendation paper.

The latest known programme baseline from the merge reports is:

- `ADR-LAYER-BOUNDARY-RECONCILIATION-1` merged and ratified for roadmap planning;
- `EIGHT_BLOCK_BETA_READINESS_COMPARISON_AND_PROGRAMME_RECOMMENDATION_2026-06-18.md` merged;
- main published at `16eee6b` after programme merge;
- working tree reported clean;
- no runtime code changed during the ADR and programme planning sprints;
- next recommended package: `P1-1 — Launch-core domain build-materials map`.

---

## 5. Evidence base audited

This reset is based on audited evidence, not general intuition.

### 5.1 Cursor eight-block estate audit

Path:

`docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_ESTATE_AUDIT_CURSOR_2026-06-17.md`

Role:

- filesystem-grounded inventory of assets, implementation status and gaps;
- strong on current codebase maturity, implementation reality and practical reuse opportunities.

Key findings:

- overall maturity: medium for internal deterministic analysis, low–medium for controlled external beta;
- 186 `pkg_*` packages identified at audit time;
- 153 Pass 3 investigation specs;
- three of six launch-core consumer domains implemented;
- production Gemini narrative synthesis not wired;
- retail UX trust issues documented;
- beta gate not ready due to security hygiene blockers;
- strong reuse assets exist and should not be reinvented.

### 5.2 Claude eight-block estate audit

Path:

`docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_ESTATE_AUDIT_CLAUDE_2026-06-17.md`

Role:

- parallel independent qualitative architecture audit;
- strongest on Layer B, narrative payloads, Gemini risk, replay/auditability and test estate implications.

Key findings:

- overall maturity: medium;
- Layer B is the strongest block;
- `ClinicianReportV1`, `NarrativePayloadV1` and `InterpretationDisplayLayerBundleV1` are important deterministic artefacts;
- approximately 187 Knowledge Bus packages;
- 11 phenotype fixtures and 16 Sentinel-guarded defect classes;
- only three of six launch-core domains implemented;
- Gemini Layer C inactive;
- retail explainer registry around 17 of 79 biomarkers;
- no formal beta-readiness gate / checklist document;
- `NarrativePayloadV1` should be consumed and extended, not reinvented.

### 5.3 Late-discovered documents

Path:

`docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_LATE_DOCUMENT_ADDENDUM_2026-06-17.md`

Role:

- incorporated late-discovered strategic and product documents;
- strengthened Layer B/C framing;
- avoided the need for a full re-audit.

Key impact:

- Strategic Vision v1.5 became the strategic north star;
- late frontend/product materials supported the need for a coherent UX surface but did not override the Layer B/C boundary;
- layer responsibility interpretation became more stable.

### 5.4 Layer Architecture Authority Index r2

Path:

`docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md`

Role:

- ranked which documents govern Layer A/B/C interpretation;
- prevented stale or narrower documents from overriding current architecture.

### 5.5 Layer Boundary Reconciliation ADR

Path:

`docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md`

Role:

- locks the canonical Layer A/B/C vocabulary;
- resolves naming drift;
- confirms that Layer B owns medical intelligence and Layer C is presentation/translation only.

### 5.6 UAT R1 and UAT R2

Paths:

- `docs/testing/INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_6bcbf1de_2026-06-16.md`
- `docs/testing/INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_6bcbf1de_2026-06-17_r2.md`

Role:

- UAT R1 identified serious results-page trust issues;
- UAT R2 superseded the stale unresolved-HIGH view after trust-hardening work.

Key position:

- HIGH UAT issues reduced from six to zero;
- residual MEDIUM/LOW work remains;
- this supports continued internal validation, not external beta exposure.

### 5.7 Programme recommendation paper

Path:

`docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_COMPARISON_AND_PROGRAMME_RECOMMENDATION_2026-06-18.md`

Role:

- compares Cursor and Claude audits;
- reconciles stale findings;
- establishes the six-phase multi-sprint beta-readiness programme;
- recommends P1-1 as the next sprint.

---

## 6. Canonical architecture now locked

The Layer A/B/C boundary is no longer open for casual reinterpretation.

### 6.1 Layer A — Ingestion and canonical facts

Layer A owns:

- ingestion;
- parsing;
- source fact extraction;
- canonicalisation;
- unit normalisation;
- preservation of lab-provided reference ranges;
- preservation of raw factual inputs;
- preparation of structured inputs for deterministic analysis.

Layer A must not:

- interpret medical meaning;
- score biomarkers;
- activate signals;
- rank findings;
- decide what to surface;
- infer causality;
- generate user-facing health conclusions.

### 6.2 Layer B — Deterministic medical intelligence and WHY

Layer B owns all deterministic medical intelligence and explanation.

Layer B owns:

- biomarker interpretation;
- signal activation and suppression;
- system and subsystem reasoning;
- phenotype mapping;
- WHY and root-cause reasoning;
- evidence-for and evidence-against;
- counter-evidence;
- missing-marker handling;
- confidence, completeness and reliability;
- lead-finding hierarchy;
- primary concern ranking;
- what should be surfaced;
- what should be suppressed;
- clinician report output;
- interpretation display records;
- deterministic boilerplate/prose asset selection;
- safety boundaries;
- prohibited claims;
- provenance and traceability for medical claims.

Layer B is the source of truth for:

- what matters;
- why it matters;
- how strongly it is supported;
- what evidence complicates the interpretation;
- what is safe to say;
- what the user or clinician is allowed to see.

This is the most important architectural decision in the programme.

Any future work that moves WHY, hierarchy, signal activation, surfacing, safety, clinician report content or boilerplate selection into Layer C, Gemini, frontend code or presentation templates is an architectural regression.

### 6.3 Layer C — Presentation and translation only

Layer C owns presentation and translation of governed Layer B output.

Layer C may:

- present Layer B outputs in a clear user-facing format;
- improve wording, flow, tone and readability;
- arrange governed sections into a polished report experience;
- use deterministic presentation templates;
- use a constrained LLM such as Gemini only to translate or polish a governed brief;
- render boilerplate modules selected by Layer B;
- render clinician/user-facing sections according to the DTO contract.

Layer C must not:

- decide findings;
- rank findings;
- activate or suppress signals;
- infer medical meaning;
- inspect raw biomarkers outside the governed Layer B brief;
- add new medical claims;
- change confidence or severity;
- change what is surfaced;
- create new evidence;
- override Layer B;
- read raw Pass 3 material or packages at runtime;
- perform frontend medical inference.

### 6.4 Gemini — optional constrained presentation component

Gemini is not the analytical engine.

Gemini is inactive for runtime narrative at the current point in the programme.

If Gemini is used later, it must be an optional constrained Layer C presentation component working from a governed Layer B brief. It may translate, polish and compose governed material. It must not decide what matters, why it matters, what is safe to say, or what should be shown to the user.

Gemini should not be activated until:

- Layer B brief/prose substrate is ready;
- `NarrativePayloadV1` or equivalent governed payload is sufficient;
- prohibited-action controls exist;
- output schema exists;
- anti-hallucination validation exists;
- safety and provenance checks are in place;
- CEO/human approval is given.

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

The user should feel:

> “I had no idea that is how my body worked, and now I understand why this marker matters.”

That “wow” experience should come primarily from governed Layer B assets:

- biomarker explainers;
- system explainers;
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

The programme is organised around eight blocks.

### Block 1 — Core health systems model

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

### Block 2 — Subsystems and depth model

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

### Block 3 — Layer B intelligence, WHY, clinician report and boilerplate prose estate

Purpose:

Build the true HealthIQ intelligence substrate.

Current position:

- strong foundations exist in `ClinicianReportV1`, `NarrativePayloadV1`, interpretation display records, root-cause assets, primary concern policy and domain narrative contracts;
- prose/explainer coverage is incomplete;
- retail explainer registry appears to cover approximately 17 of 79 key biomarkers;
- the product cannot rely on Gemini to create medical explanation improvisationally.

Target:

- Layer B can produce governed explanation material for biomarker, pathway, system, subsystem and phenotype-level interpretation;
- clinician and consumer explanation assets are selected deterministically;
- missing markers and counter-evidence are explained safely;
- output is educational, engaging, traceable, non-diagnostic and non-alarmist.

### Block 4 — Layer C presentation and constrained Gemini

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

### Block 5 — Results page and UX product layer

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

### Block 6 — Medical safety, research provenance and governance

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

### Block 7 — Auditability, reproducibility and regulatory-grade traceability

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

### Block 8 — Phenotype panels, edge-case estate and beta validation gates

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
- approximately 187 Knowledge Bus packages;
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

## 11. Strategic delivery principles

### 11.1 Use existing authority before creating new content

Every implementation sprint must begin by identifying the authoritative documents, packages, ADRs, contracts and runtime assets that govern the area. New logic must not be invented where existing assets already govern it.

### 11.2 No Gemini before Layer B is ready

Gemini must not be used to compensate for incomplete intelligence. If Layer B cannot provide the governed brief, the solution is to complete Layer B, not ask Gemini to fill the gap.

### 11.3 No frontend inference

Frontend code must remain render-only. It may display governed DTO outputs. It must not calculate, infer, rank, reinterpret or generate medical meaning.

### 11.4 No fallback parser

Fallback or dummy parsing behaviour is prohibited. Parsing should use the deterministic parser, or an explicitly enabled and governed LLM-backed parser when authorised. False reassurance from fallback parsing is unacceptable.

### 11.5 Use lab-provided reference ranges

Lab-specific reference ranges are the interpretation authority where present. Global/default ranges must not override lab ranges. Derived ratios may be calculated where the lab has not provided them, but only through governed and traceable logic.

### 11.6 Preserve provenance

Every clinically meaningful claim should remain traceable from research, package, policy and runtime component to emitted output. Raw Pass 3 material must not be read at runtime.

### 11.7 UX follows architecture

The user experience should become compelling after the architecture is stable enough to deserve it. UX polish before domain completion and hierarchy stability risks creating a beautiful interface that misrepresents incomplete intelligence.

### 11.8 Outcome-based sprints, not fragmented micro-sprints

The programme should use meaningful, outcome-based sprint packages. Split work only when safety, clinical review, architectural boundaries, signal activation or STOP gates require it.

### 11.9 Internal-validation framing until CEO approval

The product should remain framed as internal validation until the CEO explicitly approves controlled beta exposure. Beta readiness must be granted by evidence and gates, not assumed from feature completion.

### 11.10 Beta readiness must be gated explicitly

Domain completion, Layer B prose, safety, provenance, replay, UX trust, phenotype validation, security and CEO approval are all required gates.

---

## 12. Programme structure

The programme should be understood at two levels.

### 12.1 Formal programme baseline

The formal baseline is a six-phase programme with approximately sixteen primary sprint packages.

This is the baseline established by the merged programme recommendation paper.

### 12.2 Expanded planning decomposition

The expanded 30-sprint map in this document is a planning decomposition showing likely downstream work packages. It is not a fixed delivery commitment.

The detailed map should be refined after P1-1 and P2-1 because those mapping sprints will reveal which assets are genuinely implementation-ready and which require additional research, safety review or governance work.

---

## 13. Six-phase programme baseline

### Phase 0 — Governance and evidence consolidation

Goal:

Make sure the team is using the correct authorities before building.

Status:

Largely complete.

Completed or near-complete:

- Layer Boundary Reconciliation ADR;
- Cursor/Claude programme recommendation paper;
- audit closure records;
- UAT R2 correction;
- programme reset / definitive strategy document.

Remaining:

- team review and ratification of this document;
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

## 14. Expanded 30-sprint delivery map

This section provides a longer-range decomposition. Some of these sprints may later be combined if P1-1 and P2-1 show the dependencies are simple. They should not be split further unless safety, clinical review, signal activation, parser/range logic, runtime contracts or STOP gates require it.

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
- no global ranges where lab ranges exist.

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
- preserve educational framing.

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

## 15. Recommended first three work packages

### 15.1 First: P1-1 — Launch-core domain build-materials map

Why first:

Three of six launch-core domains are missing, but the Knowledge Bus likely already holds the packages, Pass 3 specs and signal logic needed to build them. Implementing domains before mapping risks duplicating or contradicting existing assets.

Purpose:

Map exactly what already exists for:

- blood / iron / oxygen;
- thyroid / energy regulation;
- kidney function.

Outputs:

- existing KB package map;
- Pass 3 / investigation spec map;
- biomarker-to-domain map;
- signal activation and blocked-status map;
- subsystem candidate map;
- prose/explainer asset map;
- test and fixture map;
- readiness and dependency assessment;
- implementation recommendations;
- recommended first domain for implementation.

Classification:

`change_type: CONTENT`

Must not do:

- no runtime code;
- no tests;
- no signal activation;
- no new domain logic;
- no Gemini;
- no frontend changes;
- no implementation.

### 15.2 Second: P2-1 — Layer B prose/explainer gap matrix

Why second:

The HealthIQ “wow” experience depends on governed explanation. Before improving results pages or activating Gemini, the team must know which prose/explainer assets already exist and what gaps remain.

Outputs:

- biomarker explainer gap matrix;
- system explainer gap matrix;
- pathway explainer gap matrix;
- clinician report gap matrix;
- consumer education gap matrix;
- missing-marker/counter-evidence prose requirements;
- priority list for deterministic prose expansion.

Classification:

`change_type: CONTENT`

Must not do:

- no LLM runtime activation;
- no frontend polish;
- no uncontrolled prose generation;
- no medical logic changes.

### 15.3 Third: P1-2 — First missing launch-core domain implementation package

Why third:

Only after P1-1 maps the build materials should implementation begin. The domain selected should be based on readiness, safety, available assets and testability, not preference. Blood/iron/oxygen is a likely candidate but must be confirmed by P1-1.

Outputs:

- completed domain assembler entry or implementation plan, depending readiness;
- subsystem wiring;
- scoring alignment;
- test coverage;
- provenance links;
- output/card behaviour;
- safety review.

Classification:

Likely `change_type: BEHAVIOUR` or `MIXED`, depending on whether runtime-loaded governed content assets are changed.

Must not do:

- do not implement all missing domains at once unless P1-1 proves this is safe;
- do not bypass medical review for context-dependent signals;
- do not use Layer C to compensate for incomplete Layer B;
- do not activate blocked signals casually.

---

## 16. Beta-readiness gates

Controlled beta should not proceed until the following gates are passed.

### Gate 1 — Domain coverage

All launch-core domains must be implemented, mapped, tested and visible in a coherent way.

### Gate 2 — Subsystem depth

Minimum viable subsystem depth must be defined, implemented and validated across launch-core domains.

### Gate 3 — Layer B evidence/prose

Layer B must provide sufficient WHY, hierarchy, evidence, counter-evidence and prose selection to support a compelling and safe user experience.

### Gate 4 — Layer C/Gemini

Layer C must be constrained to presentation/translation only. Gemini must not be active unless explicitly approved and validator-gated.

### Gate 5 — Medical safety/provenance

All medical claims must be traceable, non-diagnostic and non-alarmist. Context-dependent or blocked signals must remain controlled.

### Gate 6 — Auditability/replay

Results must be reproducible, versioned and regression-testable.

### Gate 7 — UX trust

The results page must not confuse users about marker count, severity, hierarchy, missing data, confidence or uncertainty.

### Gate 8 — Phenotype/edge-case validation

The product must be tested against representative panels, incomplete panels, conflicting evidence and edge cases.

### Gate 9 — Security/secrets/environment

There must be no committed secrets, unsafe test data, environment leakage or deployment-readiness blockers.

### Gate 10 — CEO/human approval

External or controlled beta exposure requires explicit CEO approval. The product should remain in internal validation until that decision is made.

---

## 17. Risks and mitigations

### 17.1 Rebuilding from memory

Risk:

The team forgets the discovered estate and recreates logic or strategy from scratch.

Mitigation:

Start every sprint from the authority index, programme paper, this strategy document and relevant source files.

### 17.2 Layer C drift

Risk:

Gemini or presentation logic starts making medical decisions.

Mitigation:

Enforce `ADR-LAYER-BOUNDARY-RECONCILIATION-1` in every sprint touching narrative, reports, Gemini, frontend or prose output.

### 17.3 UX-first shortcut

Risk:

The team polishes the results page before Layer B outputs are complete.

Mitigation:

Complete launch-core domains and Layer B prose substrate before full UX redesign.

### 17.4 Gemini overreach

Risk:

Gemini becomes positioned as the product brain.

Mitigation:

Delay Gemini until Layer B substrate, schemas, validators, tests and CEO approval are ready.

### 17.5 Over-fragmentation

Risk:

Work is split into too many small governance sprints, slowing delivery.

Mitigation:

Use outcome-based sprint packages with internal STOP gates.

### 17.6 Unsafe bundling

Risk:

Too much runtime logic is bundled into a single sprint without adequate review.

Mitigation:

Split when clinical safety, signal activation, parser/range logic, runtime contracts or output-emission behaviour are affected.

### 17.7 Stale documents

Risk:

Older Layer C or prompt documents are treated as current authority.

Mitigation:

Use `AUTHORITY_MAP`, Layer Authority Index r2 and the Layer Boundary Reconciliation ADR.

### 17.8 Security/secrets blockers

Risk:

Prior security hygiene blockers remain unresolved and are forgotten during product work.

Mitigation:

Elevate the security/secrets/environment gate into the beta-readiness gate set and run it before any controlled beta decision.

### 17.9 Lab range regression

Risk:

Default/global ranges accidentally override lab-provided ranges.

Mitigation:

Enforce lab-range tests and no-default interpretation policy.

### 17.10 Parser fallback regression

Risk:

A fallback parser is introduced to make demos appear to work.

Mitigation:

Preserve the non-negotiable no-fallback-parser policy.

### 17.11 Clinical review gaps

Risk:

Context-dependent signals such as FT3 low, androgen patterns or DHEA-S high are activated without sufficient context gating.

Mitigation:

Maintain STOP gates for context-dependent or clinically ambiguous signals and require medical research review before activation.

---

## 18. What the team needs to review

The team should review this document as a proposed definitive baseline and actively challenge it. Passive agreement is not the goal.

### 18.1 Architecture

Questions:

- Is the Layer A/B/C split now clear enough?
- Is everyone aligned that Layer B owns WHY, hierarchy, surfacing, clinician report and boilerplate selection?
- Is everyone aligned that Layer C and Gemini must not reason medically?
- Are there any repository documents that contradict this and need explicit handling?

### 18.2 Evidence base

Questions:

- Are any major authority documents missing?
- Are any listed documents superseded?
- Are any assets overstated or understated?
- Are any file paths wrong or stale?

### 18.3 Eight-block model

Questions:

- Are these the right eight blocks?
- Are any blocks missing?
- Is the maturity assessment fair?
- Which block creates the most risk if delayed?

### 18.4 Sprint sequencing

Questions:

- Is P1-1 the right next work package?
- Should P2-1 happen before or after the first domain implementation?
- Which missing launch-core domain should be implemented first after P1-1?
- Are any STOP gates missing?
- Are any proposed sprints unnecessarily fragmented?
- Are any proposed sprints too broad to be safe?

### 18.5 Product experience

Questions:

- Does the plan sufficiently protect the “wow” user experience?
- Does it make the product too governance-heavy?
- Are we giving enough weight to clinician report quality?
- Are we giving enough weight to consumer education and trust?

### 18.6 Beta readiness

Questions:

- Are the beta gates sufficient?
- Is anything missing before external exposure?
- What evidence would the CEO need before approving a controlled external beta cohort?
- What should remain internal-only?

### 18.7 Security, clinical and governance risk

Questions:

- Are security/secrets blockers adequately captured?
- Are thyroid, androgen and DHEA-S context risks adequately represented?
- Are lab-range and parser policies sufficiently visible?
- Are Automation Bus and Knowledge Bus governance expectations clear enough?

---

## 19. Immediate decision required

The immediate decision is whether to accept this document as the definitive team-review baseline.

If accepted, the next work package should be:

`P1-1 — Launch-core domain build-materials map`

Recommended classification:

- `change_type: CONTENT`;
- documentation/mapping only;
- no runtime code;
- no tests;
- no frontend changes;
- no Gemini;
- no implementation.

P1-1 should answer:

- what existing build materials exist for blood/iron/oxygen;
- what existing build materials exist for thyroid/energy regulation;
- what existing build materials exist for kidney function;
- what packages/specs/signals/prose/tests already exist;
- what should be implemented first;
- which implementation sprints should follow;
- which STOP gates are required before implementation.

---

## 20. Final recommendation

HealthIQ AI should proceed with the beta-readiness programme, but not by jumping directly into code.

The platform is not starting again.

It is not ready for beta yet.

It is ready for a disciplined, evidence-led completion programme.

The correct next move is to preserve the current architecture baseline, share this definitive strategy document with the team, gather challenge and amendments, and then begin P1-1: Launch-core domain build-materials map.

The programme should continue to use the eight-block framework and the reconciled layer model:

- Layer A: facts and canonicalisation;
- Layer B: deterministic medical intelligence and WHY;
- Layer C: presentation and translation only.

This is the safest path to building a product that is not merely visually impressive, but medically credible, traceable, scalable and genuinely differentiated.

---

## 21. One-page summary for circulation

HealthIQ AI is not starting again.

Recent Cursor and Claude audits found that the product has a stronger architecture and richer asset base than was initially visible. It has a governed analytical engine, Knowledge Bus assets, Pass 3 research, runtime contracts, clinician/narrative/report structures, result versioning, replay policy, Sentinel guards and internal UAT evidence.

However, it is not externally beta-ready.

Three of six launch-core domains are implemented; the missing domains are blood/iron/oxygen, thyroid/energy regulation and kidney function. Layer B prose/explainer coverage is partial. Gemini is inactive and not validated. The phenotype and edge-case estate is insufficient. Security hygiene blockers from prior recheck have not yet been confirmed resolved. UX trust work remains.

The key architecture is now locked:

- Layer A ingests and canonicalises facts.
- Layer B owns medical intelligence, WHY, hierarchy, surfacing, clinician report, prose selection, safety and provenance.
- Layer C presents and translates governed Layer B output.
- Gemini, if used later, is constrained presentation only.

The eight programme blocks are:

1. Core health systems model
2. Subsystems and depth model
3. Layer B deterministic intelligence, WHY, clinician report and prose estate
4. Layer C presentation/Gemini
5. Results page/UX
6. Medical safety, research provenance and governance
7. Auditability, reproducibility and traceability
8. Phenotype panels, edge cases and beta validation gates

The formal programme baseline is six phases and approximately sixteen primary sprint packages. The expanded 30-sprint map is a planning decomposition, not a fixed commitment.

The next recommended sprint is P1-1: Launch-core domain build-materials map. It should identify exactly what already exists for blood/iron/oxygen, thyroid/energy and kidney function before any implementation begins.

The team is asked to review, challenge and improve this definitive strategy before it becomes the ratified v1.0 programme baseline.

