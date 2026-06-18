# Layer Architecture Authority Index

**Date:** 2026-06-17  
**Mode:** Read-only documentation discovery  
**Purpose:** Index authoritative documents defining Layer A, Layer B, and Layer C purpose and boundaries for HealthIQ AI roadmap planning.

---

## 1. Strongest authoritative document (ranking)

| Rank | Document | Why it ranks highest |
|------|----------|-------------------|
| **1** | `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md` §3.9 | **CLOSED 2026-05-09** as *permanent written authority* for product Layer B → Layer C boundary; explicitly lists what Layer B hands off, what Layer C may/must not do; cited as governing Sprint 3+ readiness by `healthiq_pre_sprint3_closure_pack_FINAL.md` |
| **2** | `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md` | **Accepted ADR** — formalises `NarrativePayloadV1` handoff, `ReportV1` as Layer B source, and `NarrativeReportV1` compiler path |
| **3** | `architecture/ADR-002-deterministic-analysis-engine.md` | **Accepted constitutional ADR** — defines canonical three-layer pipeline (A/B/C) and inviolable layer boundaries |
| **4** | `backend/core/contracts/narrative_payload_v1.py` | **Runtime contract** — encodes translate-only LLM role, prohibited actions, evidence boundaries, score hierarchy |
| **5** | `architecture/Master_PRD_v5.2.md` §2.4, §3, §4 | **PRD authority** cited by ADR-002; foundational but older Layer C = LLM framing |

**Recommendation for future roadmap planning:** Govern layer-boundary work from **`healthiq_pre_sprint1_decision_pack_FINAL.md` §3.9** (product boundary), **`ADR_WP2_layer_b_layer_c_contract_path_b.md`** (typed handoff), and **`narrative_payload_v1.py`** (runtime enforcement). Use **`ADR-002`** for ingestion vs deterministic-compute vs narrative separation. Resolve naming collisions with **`ADR-005`** (signal-pipeline stages) before citing “Layer C” in new docs.

---

## 2. Layer responsibility map (evidence-based)

### Which document defines Layer A?

| Document | Evidence |
|----------|----------|
| **Primary:** `architecture/ADR-002-deterministic-analysis-engine.md` | > "Layer A — Canonicalisation and Normalisation" — alias resolution, unit conversion, lab range preservation; **must not** interpret or score |
| **Supporting:** `architecture/Master_PRD_v5.2.md` §3 | > "Layer A is responsible for converting unstructured or semi-structured lab data into canonical analytical inputs." |
| **Partial alternate:** `architecture/ADR-005-disease-specific-signal-evaluation-v2.md` | Uses "Stage 1 — Layer A: Biomarker Ingestion" in a **four-stage signal pipeline** (different taxonomy — see §11) |

### Which document defines Layer B?

| Document | Evidence |
|----------|----------|
| **Constitutional:** `architecture/ADR-002-deterministic-analysis-engine.md` | > "Layer B — Deterministic Intelligence Engine" — ratios, signal evaluation, clusters, signal states; **must not** LLM-narrate |
| **Product boundary:** `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md` §3.9 | > "**Layer B** produces `AnalysisDTO` with all structured analytical fields: `top_findings`, `consumer_domain_scores`, `insight_graph`, `root_cause_v1`, `clinician_report_v1.sections.page1`, `interpretation_display_layer_v1.records`, `actions`, `meta`" |
| **WHY / ranking:** `docs/intelligence/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` | Governs primary concern philosophy; `compile_report_v1` / `compile_clinician_report_v1` ordering |
| **WHY runtime:** `architecture/ADR-009-KB-S46-root-cause-why-insulin-inflammation.md` | Root-cause hypothesis assets and `compile_root_cause_v1` registration |
| **Clinician report:** `architecture/ADR-007-clinician-summary-report.md` | > "CSR / `ClinicianReportV1` assembly belongs to the backend runtime path" — deterministic compiler, no new clinical reasoning |
| **Domain prose assembly:** `docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` | Contract for Wave 1 domain card sentence assembly from engine fields (marked *not implementation authority*) |
| **Brief maturity:** `docs/audit-papers/LAYER-B-1_narrative_brief_maturity_report.md` | `NarrativePayloadV1` v1.1 section intents, evidence boundaries, LLM constraints |

### Which document defines Layer C?

| Document | Evidence |
|----------|----------|
| **Constitutional (LLM):** `architecture/ADR-002-deterministic-analysis-engine.md` | > "Layer C — Narrative Translation" — LLM translates structured Layer B outputs; **must not** compute thresholds or modify signal states |
| **Product boundary:** `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md` §3.9 | Two Layer C modes: **deterministic_mock** (`narrative_report_compiler_v1.py`) and **Gemini/LLM** (`synthesis.py` + `validate_llm_output_v2`); may polish **`narrative_report_v1` fields only** |
| **Handoff ADR:** `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md` | > "`NarrativeReportV1` remains the **Layer C deterministic prose output** of `compile_narrative_report_v1()`" |
| **Implementation note:** `docs/sprints/LC-S3_layer_c_payload_implementation_completion_2026-05.md` | Payload-driven deterministic Layer C assembly via `narrative_compiler_lc_s3_assembly_v1.py` |
| **NOT runtime Layer C:** `docs/frontend/CLAUDE_TRANSLATION_SPEC_v1.md` | Governs **Knowledge Bus research translation** (Phase B), not user-facing Layer C |

### Which document defines the Layer B → Layer C handoff?

| Document | Evidence |
|----------|----------|
| **Primary:** `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md` §3.9 | Five handoff groups (verdicts, medical reasoning, modifiers, narrative intent, wording boundaries) |
| **ADR:** `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md` | > "`NarrativePayloadV1` is the formal **Layer B → Layer C handoff object**" |
| **Runtime schema:** `backend/core/contracts/narrative_payload_v1.py` | `NarrativePayloadV1` bundles `report_v1`, `top_findings`, `root_cause_v1`, `section_intents`, `claim_boundaries`, `future_llm_translation_constraints` |
| **Builder:** `backend/core/analytics/narrative_payload_builder_v1.py` | Constructs payload from insight graph / report |
| **Frontend DTO lock:** `backend/core/dto/frontend_contract_v1.py` + `docs/audit-papers/LC-S19_payload_contract_hardening_notes.md` | Classifies which DTO fields are Layer B outputs vs user-facing surfaces |

### Which document confirms Layer B owns WHY / root-cause / surfacing?

| Document | Evidence |
|----------|----------|
| `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md` §3.9 | Group 2: "hypothesis / WHY set", "evidence-for", "evidence-against", "pathway/system interpretation" are **Layer B handoff**; `root_cause_v1` and `clinician_report_v1` are Layer B outputs |
| `architecture/ADR-007-clinician-summary-report.md` | > "The CSR will **not add new clinical reasoning**. It will compile and present governed outputs." |
| `docs/intelligence/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` | Primary concern / ranking philosophy for `compile_report_v1` and `compile_clinician_report_v1` |
| `architecture/ADR-009-KB-S46-root-cause-why-insulin-inflammation.md` | Governed hypothesis YAML + `compile_root_cause_v1` runtime |
| `backend/core/contracts/narrative_payload_v1.py` | `DEFAULT_LLM_PROHIBITED_ACTIONS` includes `"decide_findings_or_hierarchy"` |

### Which document confirms Layer C / frontend is render-only / presentation-only?

| Document | Evidence |
|----------|----------|
| `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md` §3.9 | > "**Layer C may do only this:** translate structured truth into natural prose … improve readability, flow, tone" |
| `architecture/ADR-007-clinician-summary-report.md` | > "The frontend is **renderer-only** … Frontend must not own selection logic, suppression logic, section assembly logic" |
| `docs/frontend/Interpretation_Display_Layer_Design_Lock.md` | > "The IDL is the **sole authority** the Section 5 UI reads from" — backend contract; FE blocked until BE-IDL-1 |
| `docs/architecture/RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md` | > "FE-VISUALISATION-B2 **renders** these keys; it **must not** merge them into `interpretation` or `clinician_report_v1` blocks" |
| `docs/governance/healthiq-frontend-shell.md` | > "treat backend as source of truth" / "Never do: invent narrative logic" |
| `AGENTS.md` | `healthiq-frontend-shell` agent: "Do not recreate narrative logic in the frontend" |
| `knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml` L40–41 | `required_frontend_render_only_conditions: frontend consumes DTO only; no package or Pass 3 reads` |
| `docs/audit-papers/LAYER-B-1_narrative_brief_maturity_report.md` | > "**Layer C changes: None.** Frontend remains render-only" |

---

## 3. Supporting documents (full list)

### Constitutional / architecture

| Path | Status (per `docs/AUTHORITY_MAP.md`) | Layer relevance |
|------|--------------------------------------|-----------------|
| `architecture/ARCHITECTURE_INDEX.md` | AUTHORITATIVE | ADR registry |
| `architecture/ADR-001-platform-non-negotiables.md` | AUTHORITATIVE | Platform invariants |
| `architecture/ADR-002-deterministic-analysis-engine.md` | AUTHORITATIVE | **Layer A/B/C definitions** |
| `architecture/ADR-003-knowledge-bus-architecture.md` | AUTHORITATIVE | Research → packages → Layer B |
| `architecture/ADR-005-disease-specific-signal-evaluation-v2.md` | AUTHORITATIVE | Signal eval (alternate A/B/C/D staging) |
| `architecture/ADR-007-clinician-summary-report.md` | AUTHORITATIVE | Clinician report = Layer B compile |
| `architecture/ADR-009-KB-S46-root-cause-why-insulin-inflammation.md` | AUTHORITATIVE | WHY hypotheses |
| `architecture/ARCHITECTURE_GUARDRAILS.md` | AUTHORITATIVE | Enforceable rules |
| `architecture/HEALTHIQ_REASONING_PIPELINE.md` | AUTHORITATIVE | Research → signal → narrative pipeline |
| `architecture/Master_PRD_v5.2.md` | SUPPORTING (PRD) | Layer A/B/C in §2.4–§4 |

### Product boundary / sprint authority

| Path | Layer relevance |
|------|-----------------|
| `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md` | **§3.9 — primary Layer B/C boundary** |
| `docs/planning-papers/healthiq_pre_sprint3_closure_pack_FINAL.md` | Sprint 3 readiness audit against §3.9 |
| `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md` | **Accepted B→C contract ADR** |
| `docs/audit-papers/wp2_layer_b_layer_c_implementation_readiness_audit.md` | Readiness evidence |
| `docs/audit-papers/LAYER-B-1_narrative_brief_maturity_report.md` | NarrativePayload v1.1 maturity |
| `docs/sprints/LC-S3_layer_c_payload_implementation_completion_2026-05.md` | Deterministic Layer C assembly |

### Intelligence / narrative contracts

| Path | Layer relevance |
|------|-----------------|
| `docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` | AUTHORITATIVE (per AUTHORITY_MAP) — Wave 1 domain copy assembly |
| `docs/intelligence/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` | AUTHORITATIVE — lead finding / ranking |
| `docs/intelligence/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` | AUTHORITATIVE — code-grounded pipeline reality |
| `docs/architecture/RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md` | Content-class boundaries; FE render-only |
| `docs/frontend/Interpretation_Display_Layer_Design_Lock.md` | AUTHORITATIVE — IDL backend contract |
| `docs/frontend/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md` | AUTHORITATIVE — results UX hierarchy |

### Runtime contracts / code authority comments

| Path | Layer relevance |
|------|-----------------|
| `backend/core/contracts/narrative_payload_v1.py` | **Layer B → Layer C handoff schema** |
| `backend/core/analytics/narrative_report_compiler_v1.py` | Docstring: "Consumes governed knowledge_bus assets … **no LLM**" |
| `backend/core/analytics/report_compiler_v1.py` | `compile_clinician_report_v1`, `compile_report_v1` |
| `backend/core/llm/validator_v2.py` | Anti-hallucination / boundary enforcement for LLM path |
| `backend/core/insights/narrative_runtime_policy.py` | Double opt-in for narrative LLM |
| `backend/core/dto/frontend_contract_v1.py` | Frontend-consumed DTO keys |

### Governance / estate gates

| Path | Layer relevance |
|------|-----------------|
| `knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml` | Frontend render-only; Layer C quarantine |
| `docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md` | Explicitly excludes LLM narrative generation from promotion scope |
| `docs/STATE_OF_TRUTH_REVIEW_2026-05.md` | Documentation hierarchy problems; points to authoritative audits |

### Misleading filename (not runtime Layer C)

| Path | Actual scope |
|------|--------------|
| `docs/frontend/CLAUDE_TRANSLATION_SPEC_v1.md` | **Knowledge Bus Phase B** — research markdown → packages; not Gemini user narrative |

---

## 4. Key quoted excerpts

### Governing rule (Pre-Sprint 1 §3.9)

> **Governing rule: Layer B decides. Layer C synthesises.**

Source: `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md` (§3.9, approved 2026-05-09)

### Layer C prohibitions (Pre-Sprint 1 §3.9)

> **Layer C must not do this**
> - invent new medical reasoning
> - change lead finding or ranking
> - alter confidence or banding
> - add causal claims
> - introduce new evidence

### ADR-002 Layer C invariant

> **Invariant:** Any computation performed in Layer C that belongs in Layer B is an **architectural defect** and must be treated as a blocking governance violation.

Source: `architecture/ADR-002-deterministic-analysis-engine.md`

### ADR_WP2 handoff

> **`NarrativePayloadV1`** is the formal **Layer B → Layer C handoff object** for Sprint 3 readiness: structured section intents, claim boundaries, and references to the same typed Layer B models (no duplicate medical definitions).

Source: `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md`

### LLM translate-only constraint (runtime)

> `llm_role: Literal["translate_governed_brief_only"] = "translate_governed_brief_only"`

> `DEFAULT_LLM_PROHIBITED_ACTIONS` includes `"decide_findings_or_hierarchy"`

Source: `backend/core/contracts/narrative_payload_v1.py`

### Clinician report ownership

> CSR / `ClinicianReportV1` assembly belongs to the backend runtime path. The frontend is **renderer-only** and consumes governed contract output.

Source: `architecture/ADR-007-clinician-summary-report.md`

### Frontend render-only gate

> `required_frontend_render_only_conditions: frontend consumes DTO only; no package or Pass 3 reads`

Source: `knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml`

---

## 5. Contradictions and stale naming

| Issue | Evidence | Classification |
|-------|----------|----------------|
| **Two different Layer A/B/C taxonomies** | `ADR-002`: A=canonicalise, B=deterministic engine, C=LLM narrative. `ADR-005`: A=ingestion, B=derived metrics, **C=Signal Evaluation Engine**, D=insight/narrative | **CONFIRMED contradiction** — same labels, different meanings |
| **Deterministic compilers labelled "Layer C"** | `ADR_WP2`: `NarrativeReportV1` = "Layer C deterministic prose output". `narrative_report_compiler_v1.py` has no LLM. Pre-Sprint §3.9 calls compiler "Layer C (deterministic_mock)" | **CONFIRMED naming drift** — conflicts with ADR-002 where Layer C = LLM only |
| **ADR-007 root-cause line** | Lists "root cause hypotheses (Layer C compilation)" while body assigns CSR assembly to backend deterministic path | **PARTIAL contradiction** — header taxonomy vs body ownership |
| **Strategic correction vs §3.9** | User correction places clinician report + boilerplate in Layer B; §3.9 places `narrative_report_v1` **assembly** in Layer C (deterministic compiler) while keeping `clinician_report_v1` in Layer B | **UNRESOLVED** — repo authority splits deterministic consumer prose compiler from analytical truth |
| **CLAUDE_TRANSLATION_SPEC_v1 name** | Filename suggests Layer C; document governs KB package translation only | **CONFIRMED misnomer risk** |
| **DOMAIN_NARRATIVE_CONTRACT status** | Header: "not implementation authority" vs AUTHORITY_MAP: AUTHORITATIVE | **PARTIAL** — authoritative for Wave 1 contract spec, not binding implementation |
| **Master PRD Layer C** | §2.4: "Layer C — Narrative Translation (LLM)" only | **STALE relative to** WP2/§3.9 deterministic Layer C compiler path |

---

## 6. Missing definitive documentation

| Gap | Why it matters |
|-----|----------------|
| **Single canonical Layer Architecture ADR** reconciling ADR-002, ADR-005, and Pre-Sprint §3.9 naming | Prevents roadmap authors citing conflicting "Layer C" meanings |
| **Authoritative doc matching strategic correction** (Layer B owns all medical prose substrate including deterministic consumer narrative; Layer C = presentation/Gemini translation only) | §3.9 and ADR_WP2 still assign `narrative_report_compiler_v1` to Layer C |
| **Ratified Gemini Layer C activation spec** consuming `NarrativePayloadV1` | LAYER-B-1 defers `LLM-NAR-0`; no production prompt template confirmed |
| **Unified clinician vs user-facing report boundary doc** beyond ADR-007 + RETAIL_EXPLAINER | Scattered across multiple contracts |
| **STATE_OF_TRUTH layer section** | `docs/STATE_OF_TRUTH_REVIEW_2026-05.md` inventories docs but does not define layers |

---

## 7. Unresolved ambiguity

1. **What counts as "Layer C" in 2026 launch architecture?** — LLM synthesis only (ADR-002), or also deterministic `narrative_report_compiler_v1` (ADR_WP2 / §3.9)?
2. **Is `interpretation_display_layer_v1` Layer B or presentation?** — Published by backend (`interpretation_display_layer_publish_v1.py`); IDL Design Lock treats it as backend contract for FE Section 5; §3.9 lists it as Layer B output.
3. **Is `layer_c_features` (insight modules) Layer C?** — Runtime modules in `backend/core/insights/modules/`; quarantined from governed consumer cards per launch estate gate; not defined in §3.9.
4. **ADR-005 four-stage vs ADR-002 three-layer** — Which taxonomy governs new engineering docs?

---

## 8. Recommendation: document to govern future roadmap planning

**Primary governance stack (in order):**

1. `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md` **§3.9** — product Layer B decides / Layer C synthesises boundary  
2. `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md` — typed `NarrativePayloadV1` handoff  
3. `backend/core/contracts/narrative_payload_v1.py` — runtime prohibited actions and translate-only LLM role  
4. `architecture/ADR-002-deterministic-analysis-engine.md` — constitutional separation of compute vs narrative  
5. `architecture/ADR-007-clinician-summary-report.md` + `docs/intelligence/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` — clinician report and lead-finding ownership  

**Before any new layer-architecture sprint:** Author a short reconciling ADR that maps ADR-005 stage labels to product Layer A/B/C vocabulary and clarifies whether deterministic narrative compilation is Layer B prose estate or Layer C presentation (aligning with the strategic correction in this index's brief).

---

## Appendix — Files searched

```
architecture/ADR-002-deterministic-analysis-engine.md
architecture/ADR-005-disease-specific-signal-evaluation-v2.md
architecture/ADR-007-clinician-summary-report.md
architecture/ADR-009-KB-S46-root-cause-why-insulin-inflammation.md
architecture/Master_PRD_v5.2.md
architecture/HEALTHIQ_REASONING_PIPELINE.md
docs/AUTHORITY_MAP.md
docs/STATE_OF_TRUTH_REVIEW_2026-05.md
docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md
docs/planning-papers/healthiq_pre_sprint3_closure_pack_FINAL.md
docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md
docs/architecture/RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md
docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md
docs/intelligence/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md
docs/frontend/CLAUDE_TRANSLATION_SPEC_v1.md
docs/frontend/Interpretation_Display_Layer_Design_Lock.md
docs/audit-papers/LAYER-B-1_narrative_brief_maturity_report.md
docs/audit-papers/wp2_layer_b_layer_c_implementation_readiness_audit.md
docs/audit-papers/LC-S19_payload_contract_hardening_notes.md
docs/sprints/LC-S3_layer_c_payload_implementation_completion_2026-05.md
backend/core/contracts/narrative_payload_v1.py
backend/core/dto/frontend_contract_v1.py
knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml
docs/governance/healthiq-frontend-shell.md
AGENTS.md
```

---

*End of index — Cursor read-only discovery, 2026-06-17.*
