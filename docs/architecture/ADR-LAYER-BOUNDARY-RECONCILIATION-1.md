# ADR-LAYER-BOUNDARY-RECONCILIATION-1 — Canonical Layer Boundary Vocabulary

## Status

Accepted — pending human ratification alongside beta-readiness roadmap planning.

## Date

2026-06-17

## Context

HealthIQ AI uses a canonical **Layer A / Layer B / Layer C** product vocabulary across strategy, architecture, contracts, and sprint governance. Recent estate audits (`docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17.md`, `docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md`, eight-block beta-readiness audits) confirm strong underlying architecture but **naming drift** that risks mis-scoping future sprints.

### Sources of drift

1. **Strategic Vision v1.5 §2.3** (`docs/strategy/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`) defines the intended product model: Layer A = governed inputs; Layer B = deterministic analytical engine including WHY, root-cause, and clinician-grade reporting; Layer C = narrative translation and presentation only.

2. **Pre-Sprint §3.9** (`docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md`) and **ADR_WP2** (`docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md`) define the Layer B → Layer C handoff via `NarrativePayloadV1`, with `NarrativeReportV1` as deterministic Layer C prose output.

3. **ADR-002** (`architecture/ADR-002-deterministic-analysis-engine.md`) establishes the constitutional three-layer separation (canonicalisation / deterministic intelligence / narrative translation).

4. **ADR-005** (`architecture/ADR-005-disease-specific-signal-evaluation-v2.md`) uses **Stage 1–4 labels** mapped to A/B/C/D inside the **signal-evaluation pipeline** — a local taxonomy that must not override product Layer A/B/C vocabulary.

5. **Historical compiler labelling** — deterministic narrative and report compilers (`compile_narrative_report_v1`, `narrative_report_compiler_v1`, LC-S3 assembly) have sometimes been described as “Layer C” work. That label correctly means **presentation/translation output**, not authority to add medical reasoning. The ambiguity has led some readers to treat compiler paths as places to introduce new analytical logic.

6. **`NarrativePayloadV1`** (`backend/core/contracts/narrative_payload_v1.py`) encodes translate-only LLM constraints and prohibited actions (e.g. deciding findings or hierarchy). It is the governed handoff object, not an analytical engine.

This ADR reconciles the above into one vocabulary for **roadmap and sprint planning**. It does not change runtime behaviour.

---

## Decision

Lock the canonical product vocabulary below. Future sprint prompts, ADRs, and architecture notes must use these definitions unless explicitly scoped as **local pipeline stages** (see ADR-005 handling).

### Layer A

Layer A owns ingestion, parsing, canonicalisation, and factual normalisation.

Layer A may:

- parse source material (uploads, structured lab extracts)
- canonicalise biomarker identities and aliases
- preserve lab-provided reference ranges
- normalise units and governed input forms
- preserve raw factual inputs and upload fidelity metadata

Layer A must not:

- interpret medical meaning
- score biomarkers
- activate or suppress signals
- rank findings or decide primary concern
- decide what to surface to users or clinicians
- generate user-facing health conclusions

### Layer B

Layer B owns all deterministic medical intelligence and explanation.

Layer B owns:

- biomarker interpretation
- signal activation and suppression
- system and subsystem reasoning
- phenotype mapping and coherence
- WHY / root-cause reasoning
- evidence-for and evidence-against
- counter-evidence
- missing-marker handling
- confidence, completeness, and reliability
- lead-finding hierarchy and primary concern ranking
- what should be surfaced and what should be suppressed
- clinician report output (`ClinicianReportV1`, CSR assembly)
- interpretation display records (`interpretation_display_layer_v1`)
- deterministic boilerplate and prose **asset selection** (which governed module to use)
- safety boundaries and prohibited claims
- provenance and traceability for medical claims

Layer B is the source of truth for:

- what matters
- why it matters
- how strongly it is supported
- what evidence complicates the interpretation
- what the user or clinician is allowed to see

Layer B may produce deterministic prose assets, report sections, explainer selections, structured narrative briefs (`NarrativePayloadV1`), and DTO fields consumed by the frontend.

Layer B must not delegate medical reasoning, finding selection, hierarchy, signal activation, WHY, or surfacing decisions to Layer C, Gemini, frontend code, or any presentation renderer.

### Layer C

Layer C owns presentation and translation of governed Layer B output.

Layer C may:

- present Layer B outputs in a clear user-facing format
- improve wording, flow, tone, and readability within claim boundaries
- arrange governed sections into a polished report experience
- use deterministic presentation templates and compilers (`NarrativeReportV1`, LC-S3 assembly)
- use a constrained LLM (e.g. Gemini) only to translate or polish the governed brief
- render boilerplate modules **selected by Layer B**
- render clinician and user-facing sections according to the DTO contract
- apply frontend retail scrubbing and layout (render-only)

Layer C must not:

- decide findings or rank findings
- activate or suppress signals
- infer medical meaning from raw biomarkers
- inspect raw biomarkers or Pass 3 packages outside the governed Layer B brief
- add new medical claims
- change confidence or severity
- change what is surfaced or suppressed
- create new evidence
- override Layer B
- read raw Pass 3 material or packages at runtime
- perform frontend medical inference

**Gemini**, if used, is not the analytical engine. It is an optional constrained presentation component inside Layer C, operating on `NarrativePayloadV1` (or equivalent governed brief) under `validate_llm_output_v2` and related guardrails.

---

## Canonical interpretation of existing naming drift

| Legacy reference | Canonical reading |
|------------------|-------------------|
| Deterministic narrative/report compilers labelled “Layer C” | **Presentation output path only** — compilers may assemble prose from Layer B selections; they must not introduce new medical logic. `NarrativeReportV1` is Layer C **output**, not Layer B **authority**. |
| `NarrativeReportV1` / `compile_narrative_report_v1()` | Governed Layer C deterministic prose output of Layer B brief + templates. Not a place to add scoring, signal activation, or hierarchy. |
| ADR-005 Stages 1–4 (A/B/C/D) | **Local signal-pipeline stages** inside Layer B’s evaluation architecture. Stage 4 (“Layer D: Insight and Narrative Construction”) builds structured Layer B artefacts; it does **not** redefine product Layer C. When citing ADR-005, prefix with “signal pipeline stage” to avoid collision. |
| `NarrativePayloadV1` | Formal **Layer B → Layer C handoff object** (per ADR_WP2). Carries section intents, claim boundaries, and references to typed Layer B models. |
| Strategic Vision v1.5 §2.3 | **Strategic north star** for layer responsibility in roadmap planning. |
| Pre-Sprint §3.9 + ADR_WP2 | Valid product boundary when read through this ADR. |
| `docs/frontend/CLAUDE_TRANSLATION_SPEC_v1.md` | **Knowledge Bus research translation** (Phase B), not runtime user-facing Layer C. |
| FE Visualisation Surface Policy (draft) | Supporting only unless registered in `docs/AUTHORITY_MAP.md`. |

---

## Consequences

Future sprint prompts must:

- explicitly state which layer (A, B, or C) is being touched
- keep all medical reasoning and surfacing decisions in Layer B
- keep frontend and Layer C render-only / translate-only
- avoid using “Layer C” to mean analytical reasoning or compiler-side medical invention
- avoid using Gemini for medical decisioning, signal activation, or hierarchy
- cite this ADR when working on narrative, reports, Gemini, results page, domain cards, clinician reports, or boilerplate prose
- **stop and escalate** if implementation would move Layer B responsibilities into Layer C

Governance validators (`day_one_launch_estate_gate_v1.yaml` render-only conditions), `RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1`, and `PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1` remain in force and are interpreted through this vocabulary.

---

## Non-goals

This ADR does not:

- implement Gemini or any LLM path
- change runtime code, tests, or frontend behaviour
- change report compilers, DTOs, or scoring
- alter existing medical logic or lab range handling
- create the beta-readiness roadmap or system/domain completion sequencing
- supersede ADR-002, ADR-005, ADR-007, or ADR_WP2 — it reconciles how to cite them

---

## Supporting documents

| Document | Role |
|----------|------|
| `docs/strategy/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` §2.3 | Strategic north star — Layer A/B/C definitions |
| `docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md` | Discovery index feeding this reconciliation |
| `docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17.md` | Prior discovery index |
| `docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_LATE_DOCUMENT_ADDENDUM_2026-06-17.md` | Beta estate context |
| Pre-Sprint §3.9 (`healthiq_pre_sprint1_decision_pack_FINAL.md`) | Closed product Layer B/C boundary |
| `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md` | Accepted B→C contract; `NarrativePayloadV1` handoff |
| `backend/core/contracts/narrative_payload_v1.py` | Runtime handoff schema and LLM prohibitions |
| `architecture/ADR-002-deterministic-analysis-engine.md` | Constitutional A/B/C separation |
| `architecture/ADR-005-disease-specific-signal-evaluation-v2.md` | Signal pipeline stages (local A/B/C/D — not product layers) |
| `architecture/ADR-007-clinician-summary-report.md` | Clinician report = Layer B compile; frontend render-only |
| `docs/intelligence/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` | Primary concern / ranking philosophy (Layer B) |
| `docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` | Wave 1 domain sentence assembly contract |
| `docs/architecture/RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md` | Retail explainer render boundaries |
| `knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml` | Launch estate render-only conditions |

---

## Decision record

**ADR-LAYER-BOUNDARY-RECONCILIATION-1** is the governing reconciliation document for **Layer A / Layer B / Layer C terminology** in HealthIQ AI roadmap and sprint planning from 2026-06-17 onward. Where older documents conflict on layer naming, this ADR defines the canonical reading unless a later accepted ADR explicitly supersedes it.

**Authority ranking used for this reconciliation:**

1. Strategic Vision v1.5 FINAL ADOPTED §2.3 (strategic north star)
2. Pre-Sprint §3.9 (closed product B/C boundary)
3. ADR_WP2 + `NarrativePayloadV1` (typed handoff)
4. ADR-002 (constitutional separation)
5. ADR-005, ADR-007, intelligence policies (scoped through this ADR)

---

## Compliance

Documentation-only. No runtime files modified by this ADR’s acceptance record.
