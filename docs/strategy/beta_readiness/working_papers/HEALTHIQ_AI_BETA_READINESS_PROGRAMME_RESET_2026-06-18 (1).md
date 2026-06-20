# HealthIQ AI — Beta Readiness Programme Reset and Delivery Plan

Version: v0.1 team review draft  
Date: 18 June 2026  
Audience: HealthIQ AI leadership, architecture, product, engineering, research, safety and validation reviewers  
Status: Draft for team review  
Repository target path: `docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_PROGRAMME_RESET_2026-06-18.md`

---

## 1. Purpose of this document

This document is the programme reset point for HealthIQ AI.

It captures where the platform now stands after the recent architecture audits, what has been discovered, what has been decided, and what needs to happen next to move the product from internal validation towards future controlled beta readiness.

It is deliberately written as a durable team-facing reference. The intention is that, even if ChatGPT, Cursor, Claude Code or other tool windows lose context, the team can return to this document and understand:

- the current architecture position;
- the evidence base that has been audited;
- the eight-block beta-readiness framework;
- the corrected Layer A / Layer B / Layer C model;
- what assets already exist and must be reused;
- what gaps remain;
- why the product is not yet externally beta-ready;
- the recommended delivery sequence over the next 20–40 sprints;
- what the team needs to review, challenge, improve or ratify.

This document is not an implementation prompt. It is not a replacement for the existing ADRs, audits, programme paper or technical source files. It is a strategic consolidation document that points the team back to the authoritative materials and explains how they fit together.

---

## 2. Executive summary

HealthIQ AI is now materially beyond a prototype concept. The product has an emerging deterministic intelligence architecture, a governed Knowledge Bus, research-to-runtime promotion controls, runtime contracts, evidence assets, result versioning, UAT evidence, and an agreed direction for how medical intelligence should flow into a user-facing experience.

However, it is not yet externally beta-ready.

The strongest conclusion from the recent audits is that we should not start again. We have discovered a richer estate than was initially visible, and the right strategy is to consolidate and complete the existing architecture, not rebuild it from memory or ask an LLM to generate a new product plan in isolation.

The key strategic correction is this:

HealthIQ AI is not “an LLM writing a blood report”. It is a deterministic medical intelligence platform that uses governed research, lab-derived reference ranges, evidence-based signal logic, controlled medical interpretation, clinician-grade reporting, traceable provenance, and reusable explanation assets. A presentation layer may then translate that governed output into a compelling consumer experience.

The core architecture is now locked as follows:

- Layer A handles ingestion, parsing, canonicalisation and factual normalisation.
- Layer B owns all medical intelligence, including WHY/root-cause reasoning, signal activation, hierarchy, surfacing, suppression, clinician report content, evidence/counter-evidence, boilerplate selection, safety and provenance.
- Layer C is presentation and translation only. It may improve wording and user-facing composition, but it must not reason medically, rank findings, activate signals, inspect raw biomarkers or create new claims.
- Gemini, if used, is an optional constrained Layer C presentation component. It is not the analytical engine and must not become the product brain.

The recent Cursor and Claude audits both concluded that HealthIQ AI has substantial assets but is not yet ready for external beta exposure. The product has strong architecture in places, but the launch-core domain estate is incomplete, subsystem depth is still light, prose and explainer coverage is partial, Layer C/Gemini activation is not ready, UX trust issues remain, and the validation estate must be expanded.

The current delivery objective is therefore:

Move from a partially implemented internal validation platform to a controlled, traceable, medically safe beta-ready product by completing the eight beta-readiness blocks in the right order.

The recommended programme starts with documentation and mapping, not immediate code:

1. Map the build materials for the missing launch-core domains.
2. Map the Layer B prose/explainer and clinician-report substrate.
3. Then implement missing domains and Layer B substrate using existing assets, not memory.
4. Only after that should Layer C/Gemini and UX redesign work proceed.
5. Controlled beta readiness should be gated by domain coverage, safety, provenance, replayability, phenotype validation, UX trust and explicit CEO approval.

---

## 3. Current position

### 3.1 What has just happened

The team has completed a sequence of architecture and programme governance steps:

1. Cursor produced an eight-block beta-readiness estate audit.
2. Claude produced a parallel eight-block estate audit.
3. Late-discovered documents were incorporated, including the adopted Strategic Vision v1.5 and frontend visualisation policy material.
4. A Layer Architecture Authority Index was created and revised.
5. A Layer Boundary Reconciliation ADR was created, ratified for roadmap planning and merged.
6. A Cursor/Claude comparison and multi-sprint programme recommendation paper was created and merged.
7. UAT R2 evidence corrected stale high-severity findings from earlier UAT evidence.
8. The repository was cleaned and the programme baseline was merged to `main`.

The latest merged baseline is:

- `ADR-LAYER-BOUNDARY-RECONCILIATION-1` is merged and ratified for roadmap planning.
- `EIGHT_BLOCK_BETA_READINESS_COMPARISON_AND_PROGRAMME_RECOMMENDATION_2026-06-18.md` is merged.
- The working tree was reported clean after merge.
- No runtime code was changed during these planning and ADR sprints.
- The next recommended package is P1-1: Launch-core domain build-materials map.

### 3.2 What has been clarified

The main clarifications are:

- The current estate is more advanced than a first glance suggests.
- The product is not beta-ready, but it has enough architecture and assets to justify a structured completion programme.
- The eight-block framework is the right organising model.
- The User Health to Systems Map is the systems taxonomy authority.
- Strategic Vision v1.5 §2.3 is the strategic north star for layer responsibilities.
- The new Layer Boundary Reconciliation ADR governs future layer vocabulary.
- Layer B must remain the source of medical truth.
- Layer C and Gemini must remain presentation/translation only.
- UAT R2 supersedes the stale view that six high UAT issues remain unresolved.
- No full estate re-audit is required before proceeding.
- The immediate next step should be build-material mapping for missing launch-core domains, not direct implementation.

---

## 4. Evidence base

The following documents form the current evidence base.

### 4.1 Core governance and programme documents

| Document | Role | Why it matters |
|---|---|---|
| `docs/strategy/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` | Strategic authority | Defines the adopted product and architecture direction, including the Layer A/B/C model and HealthIQ’s ambition as a systems-level blood-test interpretation platform. |
| `docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md` | Architecture authority | Reconciles naming drift and locks the canonical layer model for all future roadmap and sprint work. |
| `docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_COMPARISON_AND_PROGRAMME_RECOMMENDATION_2026-06-18.md` | Programme authority | Compares Cursor and Claude audits and sets out the multi-sprint beta-readiness programme. |
| `docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md` | Authority index | Identifies which documents govern layer interpretation after late-document discovery. |
| `docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_LATE_DOCUMENT_ADDENDUM_2026-06-17.md` | Late-evidence addendum | Records how late-discovered documents changed or strengthened the interpretation of the architecture. |
| `docs/AUTHORITY_MAP.md` | Repository authority map | Records authoritative and supporting documents. Updated minimally to include the layer-boundary ADR. |

### 4.2 Audit documents

| Document | Role | Why it matters |
|---|---|---|
| `docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_ESTATE_AUDIT_CURSOR_2026-06-17.md` | Cursor estate audit | Provides repo-grounded view of assets, maturity and gaps. Strong on filesystem inventory and current implementation. |
| `docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_ESTATE_AUDIT_CLAUDE_2026-06-17.md` | Claude estate audit | Provides stronger qualitative architecture review, particularly around Layer B, narrative payloads, Gemini risk, replay and auditability. |
| `docs/audit-papers/LAYER-BOUNDARY-RECONCILIATION-1_layer_boundary_reconciliation.md` | Closure and exception record | Records the governed exception where an invalid prompt `change_type: DOCS` was accepted retroactively because the output was docs-only and content-valid. Establishes future rule: documentation-only bus work uses `CONTENT`. |
| `docs/audit-papers/EIGHT-BLOCK-PROGRAMME-1_comparison_and_programme_recommendation.md` | Closure record | Records merge and GPT acceptance of the programme paper. |

### 4.3 Architecture and runtime contract documents

| Document | Role | Why it matters |
|---|---|---|
| `docs/architecture/User Health to Systems Map_FINAL.md` | Systems taxonomy authority | Defines the user-facing health systems model. This should not be rebuilt from scratch. |
| `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md` | Layer B/C contract | Defines the handoff between deterministic intelligence and presentation/narrative layers. |
| `backend/core/contracts/narrative_payload_v1.py` | Runtime contract | Defines the governed payload used to hand Layer B outputs to downstream presentation/narrative components. |
| `architecture/ADR-002-deterministic-analysis-engine.md` | Architecture ADR | Establishes the deterministic analysis engine concept. |
| `architecture/ADR-005-disease-specific-signal-evaluation-v2.md` | Signal evaluation ADR | Defines disease/signal evaluation staging, but its A/B/C/D labels are local pipeline stages and must not override product Layer A/B/C vocabulary. |
| `architecture/ADR-007-clinician-summary-report.md` | Clinician report ADR | Supports the clinician report as a governed output surface. |
| `docs/intelligence/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` | Intelligence policy | Governs primary concern, ranking and ambiguity. Important for Layer B hierarchy. |
| `docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` | Narrative/domain contract | Supports domain narrative behaviour and prevents uncontrolled presentation drift. |
| `docs/architecture/RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md` | Consumer wording boundary | Supports safe consumer-facing explanatory content. |

### 4.4 UAT, replay and validation documents

| Document | Role | Why it matters |
|---|---|---|
| `docs/testing/INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_6bcbf1de_2026-06-16.md` | UAT R1 | Identified results-page trust issues, including six high issues. |
| `docs/testing/INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_6bcbf1de_2026-06-17_r2.md` | UAT R2 | Supersedes the stale unresolved-high finding; high issues reduced from six to zero, with residual medium/low work. |
| `docs/architecture/LAUNCH-CORE-3_result_versioning_replay_and_regeneration_policy.md` | Replay/versioning policy | Governs stale/incompatible result handling and reproducibility. |
| `knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml` | Launch gate | Provides governance for what can be considered in the launch estate. |
| Sentinel and AB/VR/golden panel materials | Test estate | Provide the basis for phenotype, edge-case, suppression, replay and validation gates. |

---

## 5. Key architectural decision now locked

### 5.1 Layer A

Layer A owns ingestion, parsing, canonicalisation and factual normalisation.

Layer A may:

- parse source material;
- identify source facts;
- canonicalise biomarkers;
- preserve lab-provided reference ranges;
- normalise units;
- preserve raw factual inputs;
- prepare structured inputs for deterministic analysis.

Layer A must not:

- interpret medical meaning;
- score biomarkers;
- activate signals;
- rank findings;
- decide what to surface;
- generate user-facing health conclusions;
- infer causality or explanation.

### 5.2 Layer B

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

This is the most important architectural decision in the programme. If future work moves any of these responsibilities into Layer C, Gemini, frontend code or presentation templates, it is an architectural regression.

### 5.3 Layer C

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

### 5.4 Gemini

Gemini is not the analytical engine.

If Gemini is used later, it must be an optional constrained presentation component inside Layer C. It should translate, polish and compose governed Layer B material. It must not decide what matters, why it matters, what is safe to say, or what should be shown to the user.

Gemini should not be activated until:

- Layer B brief/prose substrate is ready;
- NarrativePayloadV1 or equivalent governed payload is sufficient;
- prohibited-action controls exist;
- output schema exists;
- anti-hallucination validation exists;
- safety and provenance checks are in place;
- CEO/human approval is given.

---

## 6. The eight beta-readiness blocks

The current delivery programme is organised around eight blocks.

### Block 1 — Core health systems model

Purpose: Ensure HealthIQ has a coherent user-facing systems model, not a loose collection of biomarker observations.

Current position:

- Strong strategic asset exists in the User Health to Systems Map.
- Only part of the launch-core systems estate appears fully implemented in the runtime/results page.
- Missing or incomplete launch-core domains include blood/iron/oxygen, thyroid/energy regulation and kidney function.
- The system model should not be recreated from scratch.

Target:

- All launch-core domains mapped, assembled and validated.
- Each domain has biomarker coverage, scoring logic, evidence inputs, card/output behaviour and test coverage.
- Domains are visibly coherent to a user and traceable to Layer B.

### Block 2 — Subsystems and depth model

Purpose: Move beyond shallow top-level system summaries into meaningful subsystem reasoning.

Current position:

- Subsystem concepts exist, but depth is uneven and in some places collapsed.
- Domain/system cards appear to exist for some areas but are not consistently rich.
- The “wow” experience requires the user to understand not only that a marker is abnormal, but how it fits into a broader body system.

Target:

- Each core system has a defined minimum subsystem model.
- Subsystem outputs remain governed by Layer B.
- Subsystems inform explanation, hierarchy and missing-marker logic.
- The subsystem estate is tested across representative panels.

### Block 3 — Layer B deterministic intelligence, WHY, clinician report and boilerplate prose estate

Purpose: Build the true HealthIQ intelligence layer.

Current position:

- Strong foundations exist: ClinicianReportV1, NarrativePayloadV1, interpretation display records, root-cause assets, primary concern policy and domain narrative contracts.
- However, boilerplate/prose assets and explainer coverage are partial.
- Retail explainer coverage appears incomplete relative to the full biomarker estate.
- The product cannot rely on Gemini to create medical explanation improvisationally.

Target:

- Layer B can produce governed explanation material for biomarker, pathway, system and phenotype-level interpretation.
- Clinician and consumer explanation assets are selected deterministically.
- Missing markers and counter-evidence are explained safely.
- The output is educational and engaging but not speculative or alarmist.

### Block 4 — Layer C presentation / translation, including constrained Gemini

Purpose: Present governed Layer B intelligence beautifully without introducing new medical reasoning.

Current position:

- Narrative payload and presentation concepts exist.
- Gemini is not yet active for runtime narrative synthesis.
- Older prompt/spec material may be stale or misleading.
- Layer C testing is underdeveloped.

Target:

- Layer C presents governed Layer B outputs in a user-friendly way.
- Gemini, if activated, operates only within strict constraints.
- Layer C output is schema-bound and validator-gated.
- No medical reasoning is delegated to Layer C.

### Block 5 — Results page / UX product layer

Purpose: Build a trustworthy, coherent user experience around stable architecture.

Current position:

- Results page has improved after UAT hardening.
- R2 UAT shows high issues resolved/downgraded.
- UX trust issues remain, including residual hierarchy/wording and marker count clarity.
- Only some launch-core domains are represented.

Target:

- Results page reflects complete Layer B outputs.
- No frontend inference.
- No confusing mismatch between marker counts, key markers and domain findings.
- Wording is polished but faithful to governed Layer B outputs.
- User can understand “why this matters” without being alarmed.

### Block 6 — Medical safety, research provenance and governance

Purpose: Preserve clinical credibility and prevent unsafe inference.

Current position:

- Knowledge Bus SOP, Pass 3 promotion, launch gate, package provenance and research-to-runtime traceability provide strong foundations.
- Some context-dependent packages remain blocked or gated.
- DHEA-S, thyroid and androgen work shows the importance of cautious activation decisions.

Target:

- Every activated runtime signal has provenance.
- Research material is promoted through controlled pathways.
- Medical claims are traceable.
- Lab-provided ranges remain the interpretation authority unless a derived ratio must be calculated.
- Safety rules prevent speculative, diagnostic or alarmist output.

### Block 7 — Auditability, reproducibility and regulatory-grade traceability

Purpose: Make outputs reproducible, explainable and governable.

Current position:

- ReplayManifestV1, result versioning, stale/incompatible banner logic and launch-core replay policies exist.
- Earlier false incompatible/stale issues were resolved.
- More replay/sentinel coverage will be required before beta.

Target:

- Every result can be reproduced against versioned inputs, packages, policies and output components.
- Result versioning accurately distinguishes compatible/current from stale/incompatible outputs.
- Changes in intelligence or presentation can be regression-tested.
- Audit artefacts support clinical, product and regulatory review.

### Block 8 — Phenotype panels, edge-case estate and beta validation gates

Purpose: Prove behaviour across the range of users and panels the product may see.

Current position:

- Some phenotype fixtures and Sentinel packs exist.
- More panels, contexts and edge cases are needed.
- Current product validation should remain internal.

Target:

- Representative phenotype panels exist across age, sex, metabolic, endocrine, renal, iron, inflammation and lifestyle contexts.
- Suppression and counter-evidence tests exist.
- Beta readiness is gated by evidence, not optimism.
- CEO/human approval is required before any external exposure.

---

## 7. Current maturity assessment

| Block | Current maturity | Evidence confidence | Main gap | Beta relevance |
|---|---:|---:|---|---|
| 1. Core health systems model | Medium | High | Missing/incomplete launch-core domains | Essential |
| 2. Subsystems and depth model | Low–Medium | Medium | Subsystem depth uneven/collapsed | Essential for “wow” |
| 3. Layer B intelligence/prose/clinician substrate | Medium | High | WHY/prose/explainer coverage partial | Essential |
| 4. Layer C/Gemini presentation | Low | Medium | Gemini inactive, constraints/tests not ready | Later-stage |
| 5. Results page/UX | Medium | High | UX trust and coverage gaps remain | Essential before beta |
| 6. Safety/provenance/governance | Medium–High | High | Some packages/context-dependent signals still gated | Essential |
| 7. Auditability/replay | Medium | Medium–High | More end-to-end replay and regression coverage needed | Essential |
| 8. Phenotype/beta validation | Low–Medium | Medium | Edge-case and phenotype estate not yet sufficient | Essential |

Overall assessment:

HealthIQ AI is architecturally viable and strategically coherent, but not yet ready for external beta use. It is ready for a structured internal beta-readiness programme.

---

## 8. What we must not lose

The following discoveries are strategically important and must not be lost across chat-window resets or tool-memory loss.

### 8.1 The product is not starting again

The estate includes:

- strategic vision;
- systems taxonomy;
- Knowledge Bus governance;
- Pass 3 research;
- promoted packages;
- runtime DTOs/contracts;
- clinician report structures;
- NarrativePayloadV1;
- interpretation display layer concepts;
- scoring policy;
- result versioning;
- replay manifest concepts;
- Sentinel tests;
- UAT evidence;
- frontend journey recommendations;
- results page hardening evidence.

The next phase is consolidation and completion, not reinvention.

### 8.2 The “wow” experience comes from governed intelligence, not uncontrolled LLM prose

The user should feel:

“I had no idea that is how my body worked, and now I understand why this marker matters.”

That experience should be built from Layer B assets:

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

### 8.3 Layer C must not become a back door for medical reasoning

This is the main architecture risk. Any future prompt or implementation that says “Layer C should decide what to say” must be challenged.

Layer C can decide how to present a governed message. It cannot decide the medical message.

### 8.4 Frontend remains render-only

The frontend may render, filter, arrange and display governed outputs. It must not calculate medical meaning, infer missing markers, rank concerns, determine severity, reinterpret biomarkers or generate new claims.

### 8.5 Lab-provided reference ranges remain the interpretation authority

HealthIQ must use lab-provided reference ranges for biomarker interpretation where they are available. Global/default ranges must not override lab ranges. Derived ratios may be calculated where the lab has not provided them, but that logic must be governed and traceable.

### 8.6 No fallback parser

The product must not introduce fallback/dummy parser behaviour. Parsing should use the deterministic parser, or the explicitly enabled LLM-backed parser when authorised. False reassurance from fallback parsing is unacceptable.

---

## 9. Reusable asset inventory

This inventory should be treated as a starting point for P1-1 and subsequent mapping sprints. It is not exhaustive; each future sprint should verify paths and content in the repository.

### 9.1 Systems and subsystem assets

| Asset | What it gives us | Future use |
|---|---|---|
| `docs/architecture/User Health to Systems Map_FINAL.md` | User-facing system taxonomy | Authority for system/domain completion |
| `backend/ssot/scoring_policy.yaml` | Scoring policy | Domain and card scoring alignment |
| Wave 1 assembler/card assets | Existing implemented systems/cards | Reuse patterns for missing launch-core domains |
| Compiled health system cards | Existing card structures | Extend/standardise missing domains |
| Knowledge Bus packages for thyroid, iron, renal etc. | Research-backed intelligence packages | Inputs for missing domains |

### 9.2 Layer B intelligence and prose assets

| Asset | What it gives us | Future use |
|---|---|---|
| `ClinicianReportV1` | Clinician-oriented structured report | Layer B clinician report expansion |
| `NarrativePayloadV1` | Governed Layer B-to-Layer C handoff | Constrained narrative/presentation pipeline |
| Root-cause assets | WHY reasoning | Layer B explanation hierarchy |
| Interpretation Display Layer records | Structured display outputs | Results page and report rendering |
| Retail explainer registry | Consumer explanation assets | Boilerplate/prose expansion |
| Pathway explainers | Mechanistic explanation | “Wow” user education |
| Domain narrative contracts | Domain-specific narrative constraints | Safe user-facing communication |

### 9.3 Layer C and presentation assets

| Asset | What it gives us | Future use |
|---|---|---|
| `ADR-LAYER-BOUNDARY-RECONCILIATION-1.md` | Layer C boundary | Prevents presentation layer drift |
| Existing narrative presentation components | Existing report/display structures | Presentation layer refinement |
| Gemini validator/prohibited action concepts | Constraints for future LLM presentation | Later Gemini activation gate |
| Results page components | Current user interface | UX redesign after Layer B completion |

### 9.4 Safety and provenance assets

| Asset | What it gives us | Future use |
|---|---|---|
| Knowledge Bus SOP | Promotion governance | Research-to-runtime safety |
| Pass 3 promotion protocol | Investigation-to-package controls | Research provenance |
| Package provenance | Traceability | Claim audit |
| Output authority provenance | Evidence chain | Medical safety |
| Lab-range tests | Range correctness | Prevent unsafe interpretation |
| Consumer prose safety boundaries | Safe wording | Prose asset expansion |

### 9.5 Auditability assets

| Asset | What it gives us | Future use |
|---|---|---|
| ReplayManifestV1 | Component/version traceability | Reproducible outputs |
| Result versioning policy | Stale/incompatible control | Trustworthy result lifecycle |
| LAUNCH-CORE-3 | Replay/regeneration policy | Launch-core validation |
| Replay sentinel packs | Regression evidence | Pre-beta gate |

### 9.6 Testing and beta validation assets

| Asset | What it gives us | Future use |
|---|---|---|
| AB/VR/golden panels | Known test inputs | Regression tests |
| Phenotype fixtures | User/panel diversity | Beta validation |
| Sentinel packs | Defect-class coverage | Regression and suppression |
| Suppression tests | Safety validation | Prevent overclaiming |
| UAT R1/R2 | Product trust evidence | UX gate |

---

## 10. Delivery principles

The next 20–40 sprints should follow these principles.

### 10.1 Use existing authority before creating new content

Every implementation sprint should begin by identifying the authoritative documents and existing runtime assets. New logic should not be invented if an existing package, policy, ADR or contract already governs the area.

### 10.2 Complete Layer B before activating Gemini

Gemini should not be used to compensate for incomplete intelligence. If Layer B cannot provide the governed brief, the answer is not to ask Gemini to fill the gap.

### 10.3 Keep medical reasoning deterministic and traceable

All medical interpretation must remain in governed Layer B logic. LLMs can support research workflows or presentation, but runtime reasoning must be traceable and controlled.

### 10.4 UX follows architecture

The user experience should be compelling, but it must sit on stable outputs. UX polish before domain completion and hierarchy stability risks making a beautiful interface that misrepresents the intelligence.

### 10.5 Avoid unnecessary micro-sprints

The programme should use outcome-based sprint packages. Split work only when safety, clinical review, architectural boundaries or STOP gates genuinely require it.

### 10.6 Preserve internal-validation framing

The product should not be framed as ready for external users until the CEO explicitly approves that move. Near-term testing should be described as internal validation.

### 10.7 No frontend inference

Frontend code must not become a medical reasoning layer.

### 10.8 No fallback parser

Do not introduce fallback/dummy parsing behaviour.

### 10.9 Use lab-provided ranges

Lab-specific reference ranges are the interpretation authority where present.

### 10.10 Gate beta readiness explicitly

Beta readiness should be granted by gates, not assumed from feature completion.

---

## 11. Programme phases

### Phase 0 — Governance and evidence consolidation

Goal: Make sure the team is using the correct authorities before building.

Status: Largely complete.

Completed or near-complete:

- Layer Boundary Reconciliation ADR.
- Eight-block programme recommendation paper.
- Audit closure records.
- UAT R2 correction.
- Programme reset document.

Remaining:

- Team review and ratification of this reset document.
- Agreement that P1-1 is the next work package.
- Confirmation that no further major authority documents are missing.

### Phase 1 — Systems and subsystem completion

Goal: Complete missing launch-core domains and minimum subsystem depth.

Primary domains:

- blood / iron / oxygen;
- thyroid / energy regulation;
- kidney function.

Expected outputs:

- build-materials map;
- domain asset matrix;
- biomarker-domain mapping;
- package/spec mapping;
- subsystem candidates;
- scoring/card requirements;
- implementation-ready sprint definitions.

### Phase 2 — Layer B substrate expansion

Goal: Complete the WHY/prose/clinician substrate that makes HealthIQ educational and trusted.

Expected outputs:

- prose/explainer gap matrix;
- retail explainer expansion plan;
- clinician report expansion plan;
- boilerplate selection rules;
- missing-marker explanation rules;
- counter-evidence explanation rules;
- pathway/system explainer coverage;
- safety review gates.

### Phase 3 — Safety, provenance and auditability hardening

Goal: Ensure medical credibility and reproducibility.

Expected outputs:

- provenance checks;
- package-to-output traceability;
- replay coverage;
- result versioning checks;
- suppression/counter-evidence validation;
- lab-range protection;
- audit manifests.

### Phase 4 — Layer C presentation and constrained Gemini

Goal: Implement or prepare presentation/translation only after Layer B is ready.

Expected outputs:

- Layer C schema;
- Gemini prompt constraints;
- prohibited-action validator;
- anti-hallucination tests;
- narrative presentation templates;
- CEO approval gate for activation.

### Phase 5 — Results page and UX redesign

Goal: Build the consumer experience around stable Layer B outputs.

Expected outputs:

- updated result journey;
- card hierarchy;
- marker count clarity;
- domain/system presentation;
- trust language;
- user education modules;
- mobile-responsive UX;
- no frontend inference.

### Phase 6 — Beta validation and release gates

Goal: Prove behaviour across panels, phenotypes, edge cases and user contexts.

Expected outputs:

- beta validation protocol;
- phenotype panels;
- edge-case matrix;
- regression tests;
- security/secrets gate;
- CEO/human beta approval gate.

---

## 12. Recommended 30-sprint delivery programme

This section expands the programme into a long-form delivery map. Some of these may be combined if the team confirms dependencies are straightforward. They should not be split further unless a safety or STOP gate requires it.

### Phase 0 — Reset and authority consolidation

#### Sprint 0.1 — Programme reset document

Objective: Produce this team-facing reset document.

Type: CONTENT  
Layer touched: none directly  
Status: current document

Expected output:

- durable reset paper;
- team review baseline;
- decision record for next sprint.

#### Sprint 0.2 — Team review and ratification

Objective: Gather team feedback on the reset document and programme sequence.

Type: CONTENT  
Layer touched: none directly

Outputs:

- team comments;
- accepted amendments;
- final v1.0 reset document;
- decision to start P1-1.

#### Sprint 0.3 — Authority pack index

Objective: Create a compact index of all authority documents needed for future sprints.

Type: CONTENT  
Layer touched: governance

Outputs:

- one-page authority index;
- “read before sprint” map;
- stale/superseded document warnings.

### Phase 1 — Systems and subsystem completion

#### Sprint 1.1 — Launch-core domain build-materials map

Objective: Identify all existing build materials for missing launch-core domains.

Type: CONTENT  
Layers touched: A/B mapping only, no runtime change

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
- implementation recommendations.

This should be the next sprint.

#### Sprint 1.2 — Blood / iron / oxygen implementation package

Objective: Implement or complete the blood/iron/oxygen domain using mapped assets.

Type: likely MIXED  
Layer touched: Layer B and runtime display contract

Outputs:

- completed domain assembler/card logic if missing;
- biomarker coverage;
- scoring alignment;
- test coverage;
- provenance map.

STOP gates:

- medical safety review if new signal activation is required;
- no global ranges where lab ranges exist.

#### Sprint 1.3 — Thyroid / energy regulation implementation package

Objective: Complete thyroid/energy domain using existing thyroid research and runtime assets.

Type: likely MIXED  
Layer touched: Layer B

Outputs:

- domain logic;
- thyroid biomarker handling;
- low/high thyroid pattern handling consistent with medical review;
- missing-marker/counter-evidence handling;
- tests.

STOP gates:

- FT3 low and context-dependent thyroid concerns must remain governed by prior clinical review outcomes.

#### Sprint 1.4 — Kidney function implementation package

Objective: Complete kidney function domain using existing renal/Kidney Bus assets.

Type: likely MIXED  
Layer touched: Layer B

Outputs:

- renal domain logic;
- eGFR/creatinine/urea/electrolyte mappings as applicable;
- lab-range and age-context handling;
- tests.

STOP gates:

- avoid diagnostic claims;
- preserve educational framing.

#### Sprint 1.5 — Subsystem minimum viable depth

Objective: Define and implement minimum subsystem depth across launch-core domains.

Type: likely MIXED  
Layer touched: Layer B

Outputs:

- subsystem taxonomy;
- system-to-subsystem mapping;
- display requirements;
- tests.

#### Sprint 1.6 — Cross-domain system coherence pass

Objective: Ensure domains do not produce contradictory or disconnected interpretations.

Type: MIXED  
Layer touched: Layer B

Outputs:

- cross-domain consistency checks;
- domain interaction rules;
- missing-marker/counter-evidence interactions;
- regression tests.

### Phase 2 — Layer B WHY, prose and clinician substrate

#### Sprint 2.1 — Layer B prose/explainer gap matrix

Objective: Identify what prose/explainer assets exist and what is missing.

Type: CONTENT  
Layer touched: Layer B planning

Outputs:

- biomarker explainer gap matrix;
- system explainer gap matrix;
- pathway explainer gap matrix;
- clinician report gap matrix;
- missing-marker/counter-evidence prose requirements.

This is likely the second sprint after P1-1.

#### Sprint 2.2 — Retail explainer registry expansion

Objective: Expand retail/consumer explainer coverage for launch-core biomarkers.

Type: CONTENT or MIXED depending repository structure  
Layer touched: Layer B asset selection

Outputs:

- new/expanded explainer entries;
- safety wording review;
- coverage tests if runtime loaded.

#### Sprint 2.3 — WHY and root-cause explanation substrate

Objective: Strengthen WHY/root-cause explanation assets.

Type: MIXED  
Layer touched: Layer B

Outputs:

- deterministic root-cause explanation selection;
- pathway explanation support;
- evidence/counter-evidence handling;
- tests.

#### Sprint 2.4 — ClinicianReportV1 launch-core expansion

Objective: Ensure clinician report surfaces all launch-core domains and evidence correctly.

Type: MIXED  
Layer touched: Layer B

Outputs:

- clinician report sections;
- evidence traceability;
- missing-marker handling;
- report tests.

#### Sprint 2.5 — Consumer boilerplate selection rules

Objective: Define deterministic rules for selecting user-facing explanation modules.

Type: MIXED  
Layer touched: Layer B

Outputs:

- selection rules;
- severity/uncertainty wording constraints;
- no speculative claims;
- tests.

#### Sprint 2.6 — Missing-marker and counter-evidence explanation sprint

Objective: Make absence and uncertainty understandable without alarmism.

Type: MIXED  
Layer touched: Layer B

Outputs:

- missing-marker explainer rules;
- counter-evidence wording;
- suppression rules;
- tests.

### Phase 3 — Safety, provenance and auditability

#### Sprint 3.1 — Research-to-runtime provenance trace

Objective: Verify activated outputs can be traced to packages and research authority.

Type: CONTENT or MIXED  
Layer touched: governance/Layer B

Outputs:

- provenance matrix;
- gap list;
- remediation plan.

#### Sprint 3.2 — Lab-range protection audit

Objective: Ensure all biomarker interpretation uses lab-provided reference ranges where available.

Type: MIXED  
Layer touched: Layer A/B boundary

Outputs:

- lab-range compliance tests;
- no-default-range checks;
- exception map for derived ratios.

#### Sprint 3.3 — Signal activation safety gate

Objective: Review all active, inactive and blocked signals for beta-readiness safety.

Type: CONTENT/MIXED  
Layer touched: Layer B

Outputs:

- signal activation matrix;
- blocked/context-dependent signal list;
- STOP gates for unresolved signals.

#### Sprint 3.4 — Replay and result versioning hardening

Objective: Ensure outputs are reproducible and versioned correctly.

Type: MIXED  
Layer touched: auditability

Outputs:

- replay tests;
- compatibility checks;
- stale/incompatible banner regression tests.

#### Sprint 3.5 — Output authority provenance

Objective: Ensure user-visible and clinician-visible claims carry appropriate authority.

Type: MIXED  
Layer touched: Layer B/Layer C handoff

Outputs:

- output provenance manifest;
- claim-to-source tracing;
- tests.

### Phase 4 — Layer C presentation and constrained Gemini

#### Sprint 4.1 — Layer C schema and allowed-action contract

Objective: Define exactly what Layer C may receive and output.

Type: CONTENT  
Layer touched: Layer C contract only

Outputs:

- schema;
- allowed actions;
- prohibited actions;
- validation approach.

#### Sprint 4.2 — Gemini prompt and validator design

Objective: Design constrained Gemini use without activation.

Type: CONTENT  
Layer touched: Layer C planning

Outputs:

- prompt template;
- prohibited action list;
- validator requirements;
- test plan.

No runtime activation.

#### Sprint 4.3 — Layer C deterministic presentation templates

Objective: Improve presentation without LLM dependency.

Type: MIXED  
Layer touched: Layer C presentation

Outputs:

- report templates;
- section ordering;
- wording polish;
- no new medical claims.

#### Sprint 4.4 — Gemini sandbox/offline evaluation

Objective: Test Gemini output against governed payloads without production activation.

Type: MIXED or CONTENT depending approach  
Layer touched: Layer C test harness

Outputs:

- sandbox test outputs;
- hallucination/fidelity assessment;
- CEO decision evidence.

#### Sprint 4.5 — Gemini activation decision gate

Objective: Decide whether Gemini should be activated and under what constraints.

Type: CONTENT  
Layer touched: governance

Outputs:

- activation decision paper;
- safety sign-off;
- CEO approval requirement.

### Phase 5 — Results page and UX product layer

#### Sprint 5.1 — Results-page information architecture redesign

Objective: Redesign around completed Layer B outputs.

Type: CONTENT  
Layer touched: UX only

Outputs:

- UX structure;
- hierarchy model;
- no inference rules.

#### Sprint 5.2 — Domain/system card UX implementation

Objective: Render complete domain cards cleanly.

Type: MIXED  
Layer touched: frontend render only

Outputs:

- domain card UI;
- subsystem display;
- no frontend medical logic.

#### Sprint 5.3 — Primary finding and hierarchy UX

Objective: Make lead findings, caveats and context clear.

Type: MIXED  
Layer touched: frontend render only

Outputs:

- primary finding UI;
- uncertainty/counter-evidence display;
- trust wording.

#### Sprint 5.4 — Marker count and uploaded-data clarity

Objective: Avoid confusion over uploaded markers, key markers and scored markers.

Type: MIXED  
Layer touched: frontend render only

Outputs:

- marker count model;
- “not uploaded” handling;
- clearer UI labels.

#### Sprint 5.5 — Full report journey polish

Objective: Build the end-to-end consumer journey.

Type: MIXED  
Layer touched: Layer C/frontend presentation only

Outputs:

- report sections;
- narrative flow;
- callouts;
- safe education.

#### Sprint 5.6 — Internal UAT rerun

Objective: Re-test the full results journey with current architecture.

Type: CONTENT/testing  
Layer touched: validation

Outputs:

- UAT report;
- defect list;
- go/no-go for beta validation phase.

### Phase 6 — Beta validation and release gates

#### Sprint 6.1 — Phenotype panel expansion

Objective: Expand representative panels and user contexts.

Type: CONTENT/MIXED  
Layer touched: testing

Outputs:

- panel matrix;
- fixtures;
- expected behaviours.

#### Sprint 6.2 — Edge-case and suppression testing

Objective: Validate safe behaviour in ambiguous, conflicting or incomplete cases.

Type: MIXED  
Layer touched: Layer B/testing

Outputs:

- suppression tests;
- counter-evidence tests;
- missing-marker tests.

#### Sprint 6.3 — End-to-end replay regression pack

Objective: Ensure outputs remain stable and reproducible across versioned changes.

Type: MIXED  
Layer touched: auditability/testing

Outputs:

- replay pack;
- regression reports;
- gate evidence.

#### Sprint 6.4 — Safety and provenance beta gate

Objective: Confirm claims, provenance and safety constraints are beta-ready.

Type: CONTENT/testing  
Layer touched: governance

Outputs:

- safety gate report;
- provenance sign-off;
- unresolved risk list.

#### Sprint 6.5 — Security/secrets/environment gate

Objective: Confirm no committed secrets, unsafe config or environment readiness gaps.

Type: MIXED/testing  
Layer touched: infrastructure/governance

Outputs:

- security gate;
- secrets audit;
- environment checklist.

#### Sprint 6.6 — CEO controlled beta decision paper

Objective: Present final go/no-go evidence for controlled beta.

Type: CONTENT  
Layer touched: governance

Outputs:

- beta readiness decision paper;
- unresolved risks;
- recommendation;
- CEO approval record.

---

## 13. Recommended first three work packages

### 13.1 First: P1-1 — Launch-core domain build-materials map

Why first:

We cannot safely implement missing domains until we know what already exists. The audits found that the estate is rich but uneven. Direct implementation risks duplicating or contradicting existing packages, specs, signal logic or tests.

What it should produce:

- map of existing KB packages;
- map of Pass 3 / investigation specs;
- biomarker-to-domain map;
- signal activation/block status;
- subsystem candidate map;
- prose/explainer asset map;
- test/fixture map;
- implementation recommendations.

What it must not do:

- no runtime code;
- no signal activation;
- no new domain logic;
- no Gemini;
- no frontend changes.

### 13.2 Second: P2-1 — Layer B prose/explainer gap matrix

Why second:

The HealthIQ “wow” experience depends on rich, governed explanation. We need to know what prose assets already exist and what is missing before trying to improve reports or activate Gemini.

What it should produce:

- biomarker explainer gap matrix;
- system explainer gap matrix;
- pathway explainer gap matrix;
- clinician report gap matrix;
- missing-marker/counter-evidence prose requirements;
- priority list for prose asset expansion.

What it must not do:

- no LLM runtime activation;
- no frontend polish;
- no uncontrolled prose generation;
- no change to medical logic.

### 13.3 Third: P1-2 — First missing launch-core domain implementation package

Why third:

Only after P1-1 maps the missing domain materials should implementation begin. The first domain should be selected based on readiness, safety, available assets and testability, not preference.

Likely candidates:

- blood / iron / oxygen;
- thyroid / energy regulation;
- kidney function.

Decision should be made after P1-1.

What it should produce:

- completed domain implementation plan or runtime implementation depending readiness;
- tests;
- provenance links;
- output/card behaviour;
- safety review.

What it must not do:

- do not implement all missing domains at once unless P1-1 shows this is safe;
- do not bypass medical review for context-dependent signals;
- do not use Layer C to compensate for incomplete Layer B.

---

## 14. Beta-readiness gates

Controlled beta should not proceed until the following gates are passed.

### Gate 1 — Domain coverage

All launch-core domains must be implemented, mapped, tested and visible in a coherent way.

### Gate 2 — Layer B evidence/prose

Layer B must provide sufficient WHY, hierarchy, evidence, counter-evidence and prose selection to support a compelling user experience.

### Gate 3 — Layer C/Gemini

Layer C must be constrained to presentation/translation only. Gemini must not be active unless explicitly approved and validator-gated.

### Gate 4 — Medical safety/provenance

All medical claims must be traceable and non-diagnostic. Context-dependent or blocked signals must remain controlled.

### Gate 5 — Auditability/replay

Results must be reproducible, versioned and regression-testable.

### Gate 6 — UX trust

The results page must not confuse users about marker count, severity, hierarchy, missing data or confidence.

### Gate 7 — Phenotype/edge-case validation

The product must be tested against representative panels, incomplete panels, conflicting evidence and edge cases.

### Gate 8 — Security/secrets/environment

No committed secrets, unsafe test data, environment leakage or deployment-readiness risks.

### Gate 9 — CEO/human approval

External or controlled beta exposure requires explicit CEO approval. The product should remain in internal validation until that decision is made.

---

## 15. Risks

### 15.1 Rebuilding from memory

Risk: The team forgets the discovered estate and recreates logic or strategy from scratch.

Mitigation: Use this reset document, the programme paper and authority index as the starting point for every sprint.

### 15.2 Layer C drift

Risk: Gemini or presentation logic starts making medical decisions.

Mitigation: Enforce ADR-LAYER-BOUNDARY-RECONCILIATION-1 in every sprint touching narrative, reports, Gemini or frontend.

### 15.3 UX-first shortcut

Risk: The team polishes the results page before Layer B outputs are complete.

Mitigation: Complete domain and prose substrate first.

### 15.4 Over-fragmentation

Risk: Work is split into too many small governance sprints, slowing delivery.

Mitigation: Use outcome-based sprint packages with internal STOP gates.

### 15.5 Unsafe bundling

Risk: Too much runtime logic is bundled into a sprint without adequate review.

Mitigation: Split when clinical safety, signal activation, parser/range logic or runtime contracts are affected.

### 15.6 Stale documents

Risk: Older Layer C or prompt documents are treated as current authority.

Mitigation: Use AUTHORITY_MAP, layer authority index r2 and the layer-boundary ADR.

### 15.7 Gemini overreach

Risk: Gemini is positioned as the product brain.

Mitigation: Delay Gemini until Layer B substrate is mature and keep it presentation-only.

### 15.8 Lab range regression

Risk: Default/global ranges accidentally override lab ranges.

Mitigation: Enforce lab-range tests and no-default interpretation policy.

### 15.9 Parser fallback regression

Risk: A fallback parser is introduced to make demos appear to work.

Mitigation: Preserve the non-negotiable no-fallback-parser policy.

---

## 16. What the team needs to review

The team should review this document and provide challenge or improvement in the following areas.

### 16.1 Architecture

Questions:

- Does the Layer A/B/C model now feel clear?
- Is everyone aligned that Layer B owns WHY, hierarchy and surfacing?
- Is everyone aligned that Layer C/Gemini must not reason medically?
- Are there any documents that contradict this and need explicit handling?

### 16.2 Evidence base

Questions:

- Are any major authority documents missing from the evidence base?
- Are any listed documents superseded?
- Are any assets overstated or understated?
- Are any paths wrong?

### 16.3 Eight-block model

Questions:

- Are these the right eight blocks?
- Are any blocks missing?
- Is the maturity assessment fair?
- Which block creates the most risk if delayed?

### 16.4 Sprint sequencing

Questions:

- Is P1-1 the right next work package?
- Should P2-1 happen before or after the first domain implementation?
- Which missing launch-core domain should be implemented first after P1-1?
- Are any STOP gates missing?
- Are any proposed sprints unnecessarily fragmented?
- Are any proposed sprints too broad to be safe?

### 16.5 Product experience

Questions:

- Does the plan sufficiently protect the “wow” user experience?
- Does it make the product too governance-heavy?
- Are we giving enough weight to clinician report quality?
- Are we giving enough weight to consumer education and trust?

### 16.6 Beta-readiness

Questions:

- Are the beta gates sufficient?
- Is anything missing before external exposure?
- What evidence would the CEO need before approving controlled beta?
- What should remain internal-only?

---

## 17. Immediate next decision

The immediate decision is whether to accept this reset document as the shared programme baseline for team review.

If accepted, the next work package should be:

`P1-1 — Launch-core domain build-materials map`

Recommended classification:

- `change_type: CONTENT`
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
- which implementation sprints should follow.

---

## 18. Team review request

Please review this reset document as the proposed baseline for the next phase of HealthIQ AI delivery.

The specific review request is:

1. Confirm whether the architectural interpretation is correct.
2. Confirm whether the eight-block model is the right delivery framework.
3. Identify any missing authority documents or assets.
4. Challenge the proposed sprint sequence.
5. Identify any safety, clinical, UX or engineering risks that are understated.
6. Confirm whether P1-1 should be the next work package.
7. Suggest amendments before the document is ratified as v1.0.

The intended outcome is not passive agreement. The team should either agree the plan, improve it, or identify where the evidence does not support it.

---

## 19. Final recommendation

HealthIQ AI should proceed with the beta-readiness programme, but not by jumping directly into code.

The correct next move is to preserve the current architecture baseline, share this reset document with the team, gather feedback, and then begin P1-1: Launch-core domain build-materials map.

The programme should continue to use the eight-block framework and the reconciled layer model:

- Layer A: facts and canonicalisation;
- Layer B: deterministic medical intelligence and WHY;
- Layer C: presentation and translation only.

This is the safest path to building a product that is not merely visually impressive, but medically credible, traceable, scalable and genuinely differentiated.

---

## 20. One-page summary for the team

HealthIQ AI is not starting again.

Recent Cursor and Claude audits found that the product has a stronger architecture and richer asset base than was initially visible, but it is not yet externally beta-ready. The right path is a structured beta-readiness programme that completes missing launch-core domains, strengthens Layer B intelligence and prose, hardens safety/provenance/replay, and only then moves into Layer C/Gemini and UX polish.

The key decision now locked is:

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

The next recommended sprint is P1-1: Launch-core domain build-materials map. It should identify exactly what already exists for blood/iron/oxygen, thyroid/energy and kidney function before any implementation begins.

The team is asked to review, challenge and improve this reset document before it becomes the v1.0 programme baseline.
