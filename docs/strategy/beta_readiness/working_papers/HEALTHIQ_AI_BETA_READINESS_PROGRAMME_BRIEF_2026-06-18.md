# HealthIQ AI — Beta Readiness Programme Brief

Version: v0.1 team review draft
Date: 18 June 2026
Audience: HealthIQ AI leadership, architecture, product, engineering, research, safety and validation reviewers
Status: Draft for team review and decision

---

## 1. Executive summary

### Where we are now

HealthIQ AI has a functioning deterministic medical intelligence platform. It is not a prototype. It has a governed analytical engine, a Knowledge Bus with approximately 187 packages, a Pass 3 research corpus, runtime DTOs, clinician and narrative report structures, result versioning, a replay policy, Sentinel guards, UAT evidence, and an agreed layer architecture.

Three of the six intended launch-core consumer domains are implemented and visible on the results page. The other three — blood/iron/oxygen, thyroid/energy regulation, and kidney function — have research material in the Knowledge Bus but are not yet assembled as domain cards. Gemini is not active for runtime narrative. The retail explainer registry covers approximately 17 of the 79 key biomarkers. Subsystem depth is deliberately constrained (MED-REV-1). There is no single consolidated beta-readiness gate artefact.

### What has been proven

Recent Cursor and Claude estate audits, a late-document addendum, a layer architecture authority index, a layer-boundary reconciliation ADR, two rounds of UAT, and a multi-agent comparison and programme recommendation paper have collectively established:

- The estate is richer and more coherent than a first-glance assessment suggests.
- The product has strong structural foundations and does not need to be rebuilt.
- The internal UAT HIGH issue count has moved from six to zero following trust-hardening work.
- The layer model is now locked: Layer A ingests facts, Layer B owns all medical intelligence, Layer C presents governed output.

### Why we are not beta-ready yet

The product is not ready for external or controlled beta exposure because:

- Three launch-core domains are missing.
- Layer B prose, explainer, and boilerplate coverage is partial.
- Gemini narrative synthesis is not activated or validated.
- The phenotype and edge-case test estate is not sufficient.
- There is no single beta-readiness gate document.
- Security hygiene blockers from prior recheck have not been confirmed resolved.

### What must be built before controlled beta

Domain coverage must be complete. Layer B must provide governed WHY, prose, and clinician report material for all launch-core domains. Safety, provenance, and auditability must be hardened. Only then should Layer C presentation and Gemini be designed and activated under constraint. UX redesign should follow stable architecture, not precede it. Beta readiness must be gated explicitly, not assumed from feature completion.

---

## 2. What we audited

The following evidence was reviewed in reaching the conclusions in this document.

**Cursor eight-block estate audit** (`docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_ESTATE_AUDIT_CURSOR_2026-06-17.md`) — filesystem-grounded inventory of assets, maturity, and gaps across all eight blocks. Identified 186 KB packages, Wave 1 domain assembler patterns, and reuse priorities.

**Claude eight-block estate audit** (`docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_ESTATE_AUDIT_CLAUDE_2026-06-17.md`) — parallel qualitative audit with stronger focus on Layer B architecture, narrative payloads, Gemini risk, replay depth, and auditability. Identified 187 packages and proposed a sprint series.

**Late-discovered documents** (`docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_LATE_DOCUMENT_ADDENDUM_2026-06-17.md`) — addendum incorporating the Strategic Vision v1.5 and frontend policy material discovered after the initial audits. Strengthened the Layer B/C framing without requiring a full re-audit.

**Layer architecture authority index r2** (`docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md`) — ranked the authority stack for layer boundary interpretation following late-document discovery. Supersedes r1 for ranking purposes.

**Layer-boundary reconciliation ADR** (`docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md`) — the authoritative architectural decision record. Locks the Layer A/B/C vocabulary, resolves naming drift (including legacy compiler labels), and governs all future sprint scoping.

**UAT R1 and R2** (`docs/testing/INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_6bcbf1de_2026-06-16.md` and `..._2026-06-17_r2.md`) — UAT R1 identified six HIGH issues on the results page. UAT R2 supersedes R1: HIGH issues reduced to zero following trust-hardening work. Residual work is MEDIUM and LOW.

**Programme recommendation paper** (`docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_COMPARISON_AND_PROGRAMME_RECOMMENDATION_2026-06-18.md`) — compares the Cursor and Claude audits, reconciles differences, identifies settled and stale findings, and sets out the multi-sprint beta-readiness programme.

---

## 3. The architectural decision now locked

The following model is locked by `ADR-LAYER-BOUNDARY-RECONCILIATION-1` and must govern all future sprint scoping, prompt authoring, audit, and implementation.

**Layer A — Ingestion and canonical facts**

Layer A parses source material, canonicalises biomarkers, normalises units, preserves lab-provided reference ranges, and prepares structured factual inputs for deterministic analysis. Layer A does not interpret medical meaning, score biomarkers, activate signals, rank findings, or create health conclusions.

**Layer B — All medical intelligence, WHY, hierarchy, surfacing, clinician report, boilerplate selection, safety and provenance**

Layer B owns biomarker interpretation, signal activation and suppression, system and subsystem reasoning, phenotype mapping, WHY and root-cause reasoning, evidence and counter-evidence, missing-marker handling, primary concern ranking, surfacing hierarchy, deterministic prose and boilerplate asset selection, clinician report content, safety boundaries, and medical provenance. Layer B is the source of truth for what matters, why it matters, what is safe to say, and what may be shown to the user or clinician.

**Layer C — Presentation and translation only**

Layer C presents and translates governed Layer B output. It may improve wording, tone, and composition. It may use deterministic templates and render selected boilerplate modules. It must not decide findings, rank findings, activate signals, inspect raw biomarkers outside the governed brief, add medical claims, change confidence or severity, or override Layer B.

**Gemini — Optional constrained presentation component, not the analytical engine**

Gemini is inactive for runtime narrative. If activated later, it must operate as a constrained Layer C translation component working from a governed Layer B brief. It must not invent medical claims, rank findings, reason about biomarkers, or become the product brain. Activation requires a sufficient Layer B prose/brief substrate, prohibited-action controls, an anti-hallucination validator, and explicit CEO approval.

---

## 4. The eight beta-readiness blocks

| Block | Description | Current maturity | Beta relevance |
|---|---|---|---|
| 1 — Core health systems model | Coherent launch-core domain coverage | Medium | Essential |
| 2 — Subsystems and depth model | Meaningful subsystem reasoning within domains | Medium | Essential for differentiation |
| 3 — Layer B intelligence, WHY, clinician report, boilerplate prose | Governed explanation, evidence, prose assets | Medium–High | Essential |
| 4 — Layer C presentation and constrained Gemini | Presentation/translation of governed output | Low (runtime inactive) | Later-stage |
| 5 — Results page and UX product layer | Trustworthy consumer experience | Medium | Essential before beta |
| 6 — Medical safety, research provenance and governance | Clinical credibility and safe inference | Medium–High | Essential |
| 7 — Auditability, reproducibility and regulatory-grade traceability | Reproducible and governable outputs | Medium | Essential |
| 8 — Phenotype panels, edge-case estate and beta validation gates | Proven behaviour across user contexts | Low–Medium | Essential |

The Layer C/Gemini block is a later-stage dependency. It cannot proceed safely until Block 3 is sufficiently complete.

---

## 5. Current estate summary

### What already exists

- Deterministic analytical engine with signal evaluators, root-cause compilers, and domain assembler logic
- Wave 1 health system cards for three launch-core domains (metabolic, cardiovascular, inflammation)
- Knowledge Bus with approximately 187 packages and 153 Pass 3 investigation specs
- Triple Layer B DTO surface: `ClinicianReportV1`, `NarrativePayloadV1`, and `InterpretationDisplayLayerV1`
- Root-cause compiler, consumer prose safety guards, output authority provenance builder
- Retail explainer registry (approximately 17 of 79 key biomarkers)
- Pathway explainer content
- Result versioning policy and stale/incompatible banner logic (LAUNCH-CORE-3)
- `ReplayManifestV1` and golden runner test harness
- AB/VR test panels, phenotype fixtures, Sentinel defect-class guards
- UAT R1 and R2 results-page evidence
- User Health to Systems Map (systems taxonomy authority)
- Scoring policy, domain narrative contracts, primary concern policy, retail explainer boundaries
- Layer boundary ADR and layer architecture authority index

### What is partial

- Launch-core domain coverage: three of six domains implemented
- Retail explainer registry: approximately 17 of 79 key biomarkers covered
- Subsystem depth: deliberately collapsed for MED-REV-1 medical review constraints; assembly patterns not yet wired for missing domains
- Layer B boilerplate and prose asset coverage: foundations present, gaps significant
- Replay manifest: stale/incompatible banner complete; raw input hash and lineage table deferred
- Phenotype and edge-case test estate: AB/VR panels exist; full phenotype matrix not yet executed
- Security/secrets gate: prior recheck flagged blockers; status not confirmed resolved

### What is missing

- Blood/iron/oxygen domain card and subsystem wiring
- Thyroid/energy regulation domain card and subsystem wiring
- Kidney function domain card and subsystem wiring
- A consolidated beta-readiness gate artefact
- Full boilerplate/prose coverage matrix (gap analysis not yet formally documented)
- Gemini activation design, prompt constraints, and validator tests
- Controlled Gemini narrative pilot (behind feature flag)
- Progressive disclosure and journey IA redesign (Journey v6 alignment)
- Full phenotype panel validation matrix

### What must not be reinvented

- The User Health to Systems Map systems taxonomy
- The Wave 1 domain assembler patterns (reuse for missing domains)
- The Layer B DTO contracts (`NarrativePayloadV1`, `ClinicianReportV1`, `InterpretationDisplayLayerV1`)
- The Knowledge Bus packages and Pass 3 research corpus for missing domains
- The layer boundary model (ADR-LAYER-BOUNDARY-RECONCILIATION-1)
- The Pass 3 promotion protocol
- The LAUNCH-CORE-3 replay and versioning policy

---

## 6. Key reusable assets

| Asset | Path | Gives us |
|---|---|---|
| User Health to Systems Map | `docs/architecture/User Health to Systems Map_FINAL.md` | Systems taxonomy authority; do not rebuild |
| Domain assembler | `backend/core/analytics/domain_score_assembler.py` | Wave 1 pattern for implementing missing domains |
| Wave 1 subsystem evidence | `backend/core/analytics/wave1_subsystem_evidence.py` | Subsystem wiring pattern |
| Scoring policy | `backend/ssot/scoring_policy.yaml` | Eight engine systems and biomarker scoring rails |
| Compiled health system cards | `knowledge_bus/compiled/health_system_cards/` | Card evidence YAML for existing domains |
| KB packages for missing domains | `pkg_thyroid_tsh_context`, `pkg_iron_deficiency_context`, renal packages | Raw material for domain implementation |
| ClinicianReportV1 | `backend/core/analytics/report_compiler_v1.py` | Clinician summary report assembly |
| NarrativePayloadV1 | `backend/core/contracts/narrative_payload_v1.py` | Governed Layer B to Layer C handoff contract |
| Root cause compiler | `backend/core/analytics/root_cause_compiler_v1.py` | WHY hypothesis selection logic |
| IDL bundle | `interpretation_display_layer_v1` on DTO | Pattern cards for results display |
| Retail explainer registry | `backend/ssot/retail_explainer_v1/registry.yaml` | Consumer biomarker explainer assets |
| Pathway explainers | `knowledge_bus/pathway_explainers_v1/` | Mechanistic pathway explanation copy |
| Domain narrative contract | `docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` | Wave 1 copy constraints |
| Primary concern policy | `docs/intelligence/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` | Layer B ranking philosophy |
| ReplayManifestV1 | `backend/core/contracts/replay_manifest_v1.py` | Component hash and reproducibility |
| Result versioning policy | `result_versioning_policy_v1.py` + LAUNCH-CORE-3 | Stale/incompatible result lifecycle |
| Sentinel packs | `sentinel/packs/` | Defect-class regression guards |
| AB/VR panels and phenotype fixtures | `backend/tests/fixtures/` | Acceptance and edge-case test profiles |

---

## 7. Strategic delivery principles

1. **No Gemini before Layer B is ready.** Gemini must not be used to compensate for incomplete Layer B prose or explanation assets. Activation requires a sufficient brief/prose substrate, validator, anti-hallucination tests, and CEO approval.

2. **No frontend inference.** The frontend renders governed DTO output. It must not calculate medical meaning, rank concerns, reinterpret biomarkers, or generate new claims.

3. **No fallback parser.** The deterministic parser is authoritative. Fallback or dummy parsing behaviour is prohibited. False reassurance from fallback parsing is unacceptable.

4. **No default/global ranges where lab ranges exist.** Lab-provided reference ranges are the interpretation authority. Global defaults must not override lab ranges. Derived ratios may be calculated where the lab has not provided them, under governed and traceable logic only.

5. **Preserve provenance.** Every activated runtime signal must be traceable to a Knowledge Bus package and a research authority. Raw Pass 3 material must not be read at runtime.

6. **UX polish after architecture is stable.** Results page redesign and consumer experience work should follow domain completion and Layer B prose stability, not precede it.

7. **Outcome-based sprints, not fragmented micro-sprints.** Sprint packages should be sized to produce a meaningful outcome. Work should not be split into one-marker or one-file micro-sprints unless a safety STOP gate specifically requires it.

8. **Use existing authority before creating new content.** Every implementation sprint must begin by identifying the authoritative documents, packages, ADRs, and contracts that govern the area. New logic must not be invented if existing assets already govern it.

9. **Beta framing remains internal until CEO explicitly approves.** The product should continue to be described as internal validation until the CEO makes an explicit decision to proceed with external or controlled beta exposure.

---

## 8. The multi-sprint programme

The programme runs across six phases and approximately sixteen sprints. Phases are ordered by dependency: domain and prose substrate before Layer C, architecture before UX, validation before external exposure.

**Phase 0 — Governance and evidence consolidation**

Publish the programme reset document and this brief. Draft a consolidated beta-readiness gate checklist. Confirm programme baseline with the team.

**Phase 1 — Systems and subsystem completion**

Map existing build materials for the three missing launch-core domains. Then implement each domain card using existing Knowledge Bus packages, Wave 1 assembler patterns, and governed signal logic.

Sprints: P1-1 domain build-materials map; P1-2 blood/iron domain card; P1-3 thyroid domain card; P1-4 kidney domain card.

**Phase 2 — Layer B WHY/prose/clinician substrate**

Formally document the boilerplate and prose coverage gap. Expand the retail explainer registry toward meaningful biomarker coverage. Expand pathway and missing-marker explainers for new domains. Harden the `NarrativePayloadV1` brief for future constrained Gemini use.

Sprints: P2-1 prose/boilerplate coverage matrix; P2-2 retail explainer expansion; P2-3 pathway and missing-marker explainer pack; P2-4 NarrativePayload brief hardening.

**Phase 3 — Safety, provenance and auditability**

Expand the Pass 3 promotion pipeline for high-value research frames. Extend the ReplayManifestV1 with compiler and package hashes. Confirm provenance and lineage coverage.

Sprints: P3-1 Pass 3 promotion pilot expansion; P3-2 replay manifest and lineage extension.

**Phase 4 — Layer C presentation and constrained Gemini**

Design the constrained Gemini activation path (prompt template, validator, prohibited actions) without production activation. Run an internal-only sandbox evaluation. CEO approval gate before any activation.

Sprints: P4-1 Gemini activation design and test harness; P4-2 controlled Gemini narrative pilot (feature flag, internal only, CEO approval required).

**Phase 5 — Results page and UX redesign**

Resolve the remaining MEDIUM UAT backlog. Align the results page with Journey v6. Implement progressive disclosure, domain card hierarchy, and subsystem visibility policy. No frontend medical inference.

Sprints: P5-1 MEDIUM UAT and retail polish backlog; P5-2 progressive disclosure and journey IA.

**Phase 6 — Beta validation and release gates**

Execute the full phenotype and panel validation matrix. Run the consolidated beta-readiness gate checklist. Clear security and secrets blockers. Produce the CEO controlled beta decision paper.

Sprints: P6-1 phenotype and panel validation matrix; P6-2 internal beta gate execution.

---

## 9. First recommended work packages

### P1-1 — Launch-core domain build-materials map

**Why first:** Three of six launch-core domains are missing, but the Knowledge Bus likely already holds the packages, Pass 3 specs, and signal logic needed to build them. Implementing domains before mapping risks duplicating or contradicting existing assets.

**What it produces:** An authoritative map for each missing domain (blood/iron/oxygen, thyroid/energy regulation, kidney function) covering: existing KB packages; Pass 3 investigation specs; biomarker-to-domain mapping; signal activation and block status; subsystem candidate list; prose and explainer asset coverage; test fixture status; implementation readiness and dependency sequencing.

**What it must not do:** No runtime code. No signal activation. No new domain logic. No Gemini. No frontend changes.

**Classification:** `change_type: CONTENT` — documentation and discovery only.

### P2-1 — Layer B prose/explainer gap matrix

**Why second:** The HealthIQ "wow" experience depends on governed explanation. Before attempting to improve the results page or activate Gemini, the team must know what prose and explainer assets already exist and what gaps remain. This is parallel-safe with domain planning.

**What it produces:** A coverage matrix and prioritised gap list across biomarker explainers, system explainers, pathway explainers, clinician report sections, missing-marker explanation, and counter-evidence explanation.

**What it must not do:** No LLM runtime activation. No frontend polish. No uncontrolled prose generation. No medical logic changes.

**Classification:** `change_type: CONTENT`.

### P1-2 — First missing launch-core domain implementation package

**Why third:** Only after P1-1 has mapped the build materials should implementation begin. The domain selected should be the one with the strongest existing package coverage, clearest biomarker scope, and lowest clinical risk. Blood/iron/oxygen is the likely first candidate but this must be confirmed by P1-1 findings.

**What it produces:** Completed domain assembler entry, subsystem wiring, scoring alignment, test coverage, and provenance links for the selected domain.

**What it must not do:** Do not implement all missing domains at once. Do not bypass medical review for context-dependent signals. Do not use Layer C to compensate for incomplete Layer B.

**Classification:** `change_type: BEHAVIOUR` — Layer B only. Full HIGH-risk route: Cursor build, Claude audit, GPT architectural review, human approval.

---

## 10. What the team needs to review

The following questions are open for team challenge, improvement, or confirmation.

**Does the architecture feel right?**

- Is everyone aligned that Layer B owns WHY, hierarchy, surfacing, clinician report, and boilerplate selection?
- Is everyone aligned that Layer C and Gemini must not reason medically?
- Are there any documents in the repository that contradict this and need explicit handling?

**Are the sprint phases correctly ordered?**

- Should P2-1 (prose gap matrix) happen before or after the first domain implementation?
- Which missing launch-core domain should be implemented first after P1-1?
- Are any phases too broad to be safe, or unnecessarily fragmented?
- Are any STOP gates missing?

**Are any known assets missing?**

- Are any authority documents absent from the evidence base listed in §2?
- Are any assets overstated in the estate summary?
- Are any file paths listed in the asset inventory wrong or stale?

**Are any dependencies wrong?**

- Is P1-1 the correct prerequisite for all Phase 1 domain sprints?
- Are there dependencies between Phase 2 and Phase 1 that change the sequencing?
- Does P2-4 (NarrativePayload hardening) correctly gate Phase 4 Gemini design?

**Are any risks understated?**

- Is Gemini architectural risk adequately captured?
- Is the clinical risk around thyroid and androgen activation adequately surfaced?
- Are the security/secrets blockers from prior beta recheck adequately flagged?
- Is the subsystem MED-REV-1 constraint adequately represented in Phase 1 scope?

**Does this give enough clarity to proceed?**

- Is P1-1 sufficiently well defined to author a work package prompt?
- Is the beta-readiness gate list complete?
- What evidence would the CEO need before approving a controlled external beta cohort?

---

## 11. Decision required

The team is asked to make the following decisions.

**Agree this as the working beta-readiness programme baseline.** The eight-block framework, reconciled layer model, phase sequencing, and sprint list in this document and the accompanying programme reset should become the shared working baseline. Any team member who believes the evidence does not support a section must state that directly.

**Agree the first sprint package.** P1-1 (Launch-core domain build-materials map, `change_type: CONTENT`) should be the next work package authored and executed. It produces the mapping foundation for all Phase 1 domain implementation sprints.

**Agree no Gemini/UX-first shortcut.** The product must not jump to Gemini narrative activation or UX redesign before domain coverage and Layer B prose substrate are complete. This is the highest architectural risk and the most likely source of quality regression.

**Agree Layer B remains the source of analytical truth.** No future sprint, prompt, or implementation should assign Layer B responsibilities — WHY reasoning, signal activation, clinician report content, boilerplate selection, or safety boundaries — to Layer C, Gemini, the frontend, or any LLM runtime path.

---

*Programme Brief — HealthIQ AI Beta Readiness — 2026-06-18 — v0.1 team review draft.*
