# Layer Architecture Authority Index (Revision 2)

**Date:** 2026-06-17  
**Supersedes ranking in:** `docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17.md` (r1 retained unchanged)  
**Trigger:** Post-audit late-document discovery — see `docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_LATE_DOCUMENT_ADDENDUM_2026-06-17.md`  
**Mode:** Documentation addendum only — no code changes, no estate re-audit

---

## 1. Revised authority ranking

| Rank | Document | Role |
|------|----------|------|
| **1** | `docs/strategy/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` **§2.3** | **Strategic north star** — master Phase 1 record; defines Layer A/B/C purpose at strategy level |
| **2** | `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md` **§3.9** | **Product boundary** — CLOSED 2026-05-09; "Layer B decides. Layer C synthesises."; field-level handoff and prohibitions |
| **3** | `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md` | **Formal handoff ADR** — `NarrativePayloadV1`, `ReportV1`, `NarrativeReportV1` compiler path |
| **4** | `backend/core/contracts/narrative_payload_v1.py` | **Runtime enforcement** — evidence boundaries, claim boundaries, `translate_governed_brief_only`, prohibited actions |
| **5** | `architecture/ADR-002-deterministic-analysis-engine.md` | **Constitutional separation** — ingestion vs deterministic computation vs narrative/presentation |
| **6** | `architecture/ADR-007-clinician-summary-report.md` + `docs/intelligence/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` | **Clinician report, WHY, ranking, lead-finding ownership** |

**r1 change:** Pre-Sprint §3.9 was ranked **1** in r1; v1.5 §2.3 is now **1** because `docs/AUTHORITY_MAP.md` marks v1.5 FINAL as **AUTHORITATIVE** master strategic record and §2.3 states the corrected Layer B/C model at the highest strategic level. §3.9 remains the **operational product boundary** immediately below.

---

## 2. Strategic Vision v1.5 §2.3 — exact excerpts

**Source:** `docs/strategy/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`  
**AUTHORITY_MAP status:** **AUTHORITATIVE** — "Master strategic record."

### Layer A — Canonicalisation and governed inputs

> This layer receives raw lab data and converts it into governed analytical input.
>
> It covers:
> - biomarker values and lab ranges from the uploaded panel
> - canonicalisation and normalisation of those values into the platform's governed input form
> - over time, governed non-biomarker context inputs such as anthropometrics, blood pressure, smoking, alcohol, medications, exercise, sleep, and stress
>
> Layer A is the input and normalisation layer.
> It must not become the place where clinical reasoning is improvised.

### Layer B — Deterministic analytical engine

> This is the biological reasoning core of HealthIQ.
> It is where governed inputs are transformed into structured metabolic intelligence.
>
> Inside Layer B, the platform builds through several connected internal components:
> - signal activation and signal-state evaluation
> - interaction and system-level reasoning
> - phenotype mapping, phenotype fixture truth, and phenotype coherence
> - WHY / root-cause reasoning
> - structured output generation including clinician-grade reporting
>
> … HealthIQ's strategic ambition inside Layer B is not merely to accumulate more signals.
> It is to connect signals into pathway-level, phenotype-aware, root-cause-capable metabolic reasoning.

### Layer C — Narrative translation and presentation

> Only after Layers A and B are coherent should the platform translate structured truth into human-readable language.
>
> Layer C covers:
> - user-facing narrative translation
> - presentation of governed outputs
> - readable explanation of structured truth
>
> Layer C must never become the analytical engine.
> It translates governed truth; it does not invent or replace it.

### Why the model matters (§2.3 closing)

> This distinction is strategically important because it keeps the product honest.
> It prevents HealthIQ from drifting into a narrative-first product, a frontend-led interpretation product, or a weak blood-report application that sounds intelligent while compensating for incomplete deterministic truth.

---

## 3. Confirmations against corrected architecture

| Question | Answer | Evidence |
|----------|--------|----------|
| Does Layer B own **signals**? | **Yes** | v1.5 §2.3: "signal activation and signal-state evaluation" inside Layer B |
| Does Layer B own **WHY / root-cause**? | **Yes** | v1.5 §2.3: "WHY / root-cause reasoning" inside Layer B |
| Does Layer B own **clinician reporting**? | **Yes** | v1.5 §2.3: "structured output generation including clinician-grade reporting" inside Layer B |
| Does Layer B own **surfacing / medical decisioning**? | **Yes (strategic)** | v1.5 §2.3 + §3.9: Layer B produces structured analytical outputs; §3.9 lists `top_findings`, `root_cause_v1`, `clinician_report_v1`, domain scores, IDL as Layer B handoff |
| Is Layer C **presentation / translation only**? | **Yes (strategic)** | v1.5 §2.3: "narrative translation and presentation"; "must never become the analytical engine" |
| Does Gemini / LLM sit in Layer C only? | **Yes (when active)** | ADR-002, §3.9 Gemini path, v1.5 strategic framing — translation after Layer B coherence |

**Caveat (unchanged from r1):** Repo implementation still labels `compile_narrative_report_v1()` as "Layer C deterministic prose" per ADR_WP2 and §3.9 — see §6.

---

## 4. How v1.5 §2.3 relates to other authorities

| Document | Relationship to v1.5 §2.3 |
|----------|---------------------------|
| **Pre-Sprint §3.9** | **Operationalises** v1.5 at product-contract level: which DTO fields are Layer B vs what Layer C may polish; governing rule "Layer B decides. Layer C synthesises." Does not contradict v1.5; adds field-level detail |
| **ADR_WP2** | **Formalises handoff** between Layer B typed outputs (`ReportV1`) and Layer C assembly (`NarrativePayloadV1` → `NarrativeReportV1`). Narrower scope than v1.5; does not replace it |
| **NarrativePayloadV1** | **Runtime embodiment** of §3.9 groups 4–5 and v1.5 Layer C constraints (`translate_governed_brief_only`, prohibited actions) |
| **ADR-002** | **Constitutional** layer separation; Layer C = "Narrative Translation" with LLM framing — **partially stale** vs v1.5/§3.9 deterministic compiler path |
| **ADR-007 + Primary Concern policy** | **Specialises** v1.5 "clinician-grade reporting" and lead-finding ranking mechanics |

**Reading order for roadmap authors:** v1.5 §2.3 (why) → §3.9 (what fields) → ADR_WP2 + NarrativePayloadV1 (how) → ADR-002/007 (constitutional detail).

---

## 5. Late-discovered documents — classification

| Document | AUTHORITY_MAP | Classification | Use in layer planning |
|----------|---------------|----------------|----------------------|
| `HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` | **AUTHORITATIVE** | **Tier 1 strategic** | §2.3 is now rank 1 |
| `docs/archive/superseded/..._v1.4_amended.md` | **SUPERSEDED** | Historical | No §2.3 layer model; sprint roadmap only — **not relevant** for layer authority |
| `docs/archive/superseded/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan.md` (v1.3) | **SUPERSEDED** | Historical | Same — **not relevant** for layer authority |
| `docs/archive/working-papers/download-arch/HealthIQ_FE_VISUALISATION_Surface_Policy_Proposal_v1_fresh.md` | **NOT LISTED** | **Draft discussion paper** | **Supporting UX/design-policy only** — cannot override MED-REV-1, runtime assembler, or launch estate |
| `docs/archive/working-papers/download-arch/HealthIQ_FE_VISUALISATION_Surface_Policy_Final_v3.md` | **SUPPORTING** | Historical surface policy | Supporting context; Results Journey v6 is AUTHORITATIVE for results UX |

### CLAUDE_TRANSLATION_SPEC_v1 (unchanged from r1)

`docs/frontend/CLAUDE_TRANSLATION_SPEC_v1.md` governs **Knowledge Bus Phase B — research markdown → packages**. It is **not** runtime Layer C user narrative. Filename is misleading.

---

## 6. FE Visualisation Surface Policy — supporting only

**File:** `docs/archive/working-papers/download-arch/HealthIQ_FE_VISUALISATION_Surface_Policy_Proposal_v1_fresh.md`  
**Status:** Version 1.0 **draft** — team discussion paper; **not in AUTHORITY_MAP**

**Aligns with audits (supporting evidence):**
- Tiered disclosure (standard / advanced / internal)
- Lead with synthesis not charts
- Educational phenotype layer **separate from personalised interpretation**
- Backend artefacts must not leak un-translated

**Tensions (do not override runtime):**

| FE proposal | Current estate | Tension |
|-------------|----------------|---------|
| "Show systems, not just markers" | MED-REV-1 hid 5/7 subsystems (`hidden_v1`) | Proposal pushes **more** system legibility; medical review pushed **less** |
| BiomarkerChart "priority markers only" (standard mode) | UAT panel shows full 79-marker grid | Implementation **drifts** from proposal |
| ClusterCard as main systems surface | Wave1 domain cards + IDL are newer primary surfaces | **Evolution** — not contradiction, but proposal predates current journey |

**Governance rule:** FE proposal informs UX policy discussion only. **MED-REV-1**, `domain_score_assembler.py`, `day_one_launch_estate_gate_v1.yaml`, and **Results Journey v6** outrank it for implementation decisions.

---

## 7. Reconciling ADR — still required?

**Yes.** r2 elevates v1.5 §2.3 but does **not** resolve:

1. **ADR-002 / Master PRD** — Layer C = LLM narrative only  
2. **ADR_WP2 / §3.9** — deterministic `narrative_report_compiler_v1` labelled Layer C  
3. **ADR-005** — alternate A/B/C/D labels for signal-pipeline stages  
4. **Strategic correction** — Layer B owns full medical prose substrate vs consumer narrative compiler assigned to Layer C in §3.9

**Recommended next artefact:** Short **Layer-boundary reconciliation ADR** mapping:
- v1.5 §2.3 (strategic)
- §3.9 (product fields)
- Whether deterministic consumer prose compilation is Layer B "structured output" or Layer C "presentation"

---

## 8. Roadmap governance stack (r2)

1. `HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` §2.3  
2. `healthiq_pre_sprint1_decision_pack_FINAL.md` §3.9  
3. `ADR_WP2_layer_b_layer_c_contract_path_b.md`  
4. `backend/core/contracts/narrative_payload_v1.py`  
5. `ADR-002-deterministic-analysis-engine.md`  
6. `ADR-007` + `PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md`  

Then: **reconciling ADR** → multi-sprint programme.

---

## 9. r1 → r2 summary

| Item | r1 | r2 |
|------|----|----|
| Top authority | Pre-Sprint §3.9 | **v1.5 FINAL §2.3** |
| Strategic Vision v1.5 | Not included | **Rank 1** |
| FE Surface Policy Proposal v1 fresh | Not included | **Supporting only** |
| Superseded v1.3/v1.4 | Not included | **Not relevant** for layers |
| Core conclusions | Layer B real; C = presentation; reconciling ADR needed | **Unchanged** |
| Full estate re-audit | Not recommended | **Still not recommended** |

---

*End of r2 index — 2026-06-17.*
