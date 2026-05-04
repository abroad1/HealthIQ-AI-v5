---
work_id: FE-VISUALISATION-B-PREFLIGHT
execution_model: READ_ONLY_INVESTIGATION
risk_level: STANDARD
date: 2026-04-05
---

# FE-VISUALISATION-B Preflight — Enriched Explanatory Content

## 1. Executive summary

| Area | Repo reality today |
|------|-------------------|
| **Biomarker “interpretation” on the wire** | Field **exists** on `BiomarkerResult` / DTOs and is **populated** in normal runs, but content is **scoring and lab-range mechanics** (e.g. “Scored using lab reference range”, “Not scored - no reference range available”), **not** retail plain-language physiology explainer text. |
| **Curated biomarker explainers (SSOT / dictionary)** | **No** first-class, user-facing biomarker explainer dictionary surfaced to the results API was found in this audit. SSOT biomarker metadata exists for IDs/units; **knowledge_bus** holds rich **signal-level** `explanation` blocks in package YAML that are **not** mapped 1:1 to per-biomarker retail strings on the analysis result. |
| **BiomarkerContext_v1** | Present in contracts as **code-only** nodes (`reason_codes`, `missing_codes`, `relationship_codes`) — **usable for governance/prompting**, **not** as off-the-shelf consumer prose. |
| **Body-system educational layer** | **No** dedicated “Understanding this system” content asset set wired to the FE. Cluster **names** are template-based and legible; **descriptions** are **auto-generated** from severity + biomarker ID lists — helpful as **supporting** copy, **not** vetted educational articles. |
| **Biomarker → system contribution narrative** | **Structural** link exists: each cluster lists `biomarkers`. There is **no** separate authored field explaining *how* a marker “drives” a pattern in consumer language without **new** content or inference text. |
| **Symptom relevance** | **Reserved** in UI only (dormant slot). **No** symptom-to-marker relevance implementation in results path; questionnaire may collect symptoms elsewhere — **out of scope** for Phase B as defined in Phase A policy intent. |
| **Mandatory policy docs on disk** | Paths cited in the investigation charter (`docs/architecture/HealthIQ_FE_VISUALISATION_Surface_Policy_Final.md`, `docs/investigations/FE_VISUALISATION_PREFLIGHT.md`) were **not found** in the repo at investigation time. Grounding below uses the **charter text**, **FE-VISUALISATION-A** implementation, `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` (FE-VISUALISATION line), and **code evidence**. **Recommendation:** restore or commit those policy artefacts so Phase B prompts stay governable. |

**Is Phase B “ready” as a single FE-only sprint?**  
**No.** Meaningful enriched **explanatory** content for standard users requires **authored or derived retail-safe strings** (or explicit surfacing of existing KB narratives through a **new or extended contract**). The FE can **render**; it cannot **invent** (per Phase A rules).  

**Recommendation (final):** **`SPLIT_INTO_CONTENT_FOUNDATION_AND_FRONTEND_RENDERING`** — see §6.

---

## 2. Policy-to-repo translation

### 2.1 What Phase B is supposed to add (per charter + strategic doc)

From the **FE-VISUALISATION-B preflight charter** and the **Wave 4** definition in `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`:

- Move beyond **structured interpretation only** toward **enriched explanatory** layers that Phase A **deferred**, including (examples from charter):
  - **Biomarker plain-language explainers** (educational / interpretive, not just status labels).
  - **Body-system educational explainer** layer (clearly **educational**, separable from personalised proof).
  - Optional **biomarker → system contribution** explanation (how markers relate to wider patterns).
- **Strategic doc** still frames FE-VISUALISATION as “core reusable product visualisation surfaces” with data contracts from the results pipeline — Phase B extends **content depth**, not just layout.

### 2.2 What Phase A delivered (evidence)

Implemented on `main` (post FE-VISUALISATION-A):

- **Hero** `InsightPanel` from `clinician_report_v1.sections.page1` (primary concern, ambiguity-aware).
- **Trust** layer from `data_quality` + confirmatory list.
- **Clusters** as secondary biological surface; **biomarkers** as supporting layer; **BiomarkerDials** can show `interpretation` only when **`showDetails`** and payload non-empty.
- **Dormant** symptom-relevance placeholder; **no** educational body-system article block.

### 2.3 What remains deferred after Phase B (even if B ships)

- **True symptom relevance** (policy-reserved; not authorised by Phase B charter).
- **Personalised “because you said X”** narrative tied to symptoms unless a future governed context sprint lands.
- **LLM-generated** retail prose without deterministic SSOT — out of alignment with current substrate unless explicitly scoped.

---

## 3. Biomarker explainer audit

### 3.1 Field existence

- **Backend model:** `BiomarkerScoreDTO` / pipeline assembly sets `interpretation` in `orchestrator.py` when building biomarker rows (see excerpt references below).
- **DTO builder:** `build_biomarker_score_dto` passes `interpretation` through (`backend/core/dto/builders.py`).
- **Persistence / API paths** map `interpretation` on load/save (e.g. `persistence_service.py`, `analysis_repository.py`, `analysis.py` route shaping).
- **Frontend:** `BiomarkerResult.interpretation` in `frontend/app/types/analysis.ts`; **BiomarkerDials** displays it in detail mode.

### 3.2 Actual population (representative logic)

In `backend/core/pipeline/orchestrator.py`, populated strings include:

- `Scored {score}/100` for scored markers in one branch.
- `Not scored - no reference range available`, `Not scored - insufficient numeric bounds for scoring`, `Scored using lab reference range`, `Scored using HealthIQ fallback bounds (lab range not provided)`, etc.

These strings are **deterministic** and **useful for transparency**, but they are **not** plain-language explanations of *what the biomarker measures* or *what it means biologically* for a lay user.

### 3.3 Other biomarker-level “explainer” sources

| Source | Nature | Retail-ready? |
|--------|--------|----------------|
| **`BiomarkerContextNode`** (`backend/core/contracts/biomarker_context_v1.py`) | Codes + status + optional score | **No** — not prose. |
| **Signal package `explanation.*` in knowledge_bus** (e.g. `pkg_homocysteine_elevation_context/signal_library.yaml`) | Rich structured text tied to **signals**, not each biomarker row | **Partial** — high quality for **signal** education if **surfaced** through a governed mapping; **not** currently on standard `biomarkers[]` JSON for arbitrary markers. |
| **Fixture / tests** | Placeholder e.g. “Within normal range” | Test data only. |

### 3.4 Assessment

- **Type exists:** yes.  
- **Field populated:** yes, routinely.  
- **Production-usable as “enriched explanatory content” for Phase B goals:** **no** — wrong **content class** (mechanistic/scoring, not curated explainer prose).

---

## 4. System / body-system educational content audit

### 4.1 SSOT / schema

- **`ClusterDefinition`** in `cluster_schema_loader.py` includes a **`description`** field from `clusters.yaml` **at schema level**.
- **Runtime clusters** from `ClusterEngineV2._build_clusters` set:
  - `name`: `f"{system_name.title()} Health Pattern"` — **product-legible** pattern label.
  - `description`: **template** combining severity, system key, and **raw biomarker IDs** (comma-separated). Legible to engineers; **borderline** for **polished** consumer education (IDs like `hdl_cholesterol` appear in prose unless post-processed).

### 4.2 Frontend

- **No** `insight_graph` / `biomarker_context` usage in TS/TSX (`grep` over `frontend/` returned no matches). Educational depth in **meta** is **not** driving a retail explainer block today.

### 4.3 Separation from personalised interpretation

- **Clinician report** and **InsightPanel** carry **personalised** synthesis.  
- A future **educational** block must be **visually and contractually** distinct (policy: educational must not read as personalised proof). **No** dedicated component or content source enforces that separation yet for body-system education.

---

## 5. Cluster / system translation audit

| Question | Finding |
|----------|---------|
| Typical `cluster.name` in practice? | **`{System_title} Health Pattern`** where `system_name` is the **cluster schema key** (e.g. metabolic → “Metabolic Health Pattern”). |
| Good enough for educational header? | **Yes** as a **short label**; not sufficient alone for **depth**. |
| `cluster.description` quality? | **Auto-generated**; includes **raw biomarker tokens** — acceptable for **supporting** text with light formatting, **not** final edu copy without cleanup or replacement. |
| Translation layer still required? | **Yes** if Phase B promises **polished** educational prose — either **curated strings per system** or **deterministic prettification** of marker lists + separate static paragraphs. |

---

## 6. Biomarker-to-system contribution audit

| Question | Finding |
|----------|---------|
| Linkage in payload? | **Yes:** `clusters[].biomarkers` (and `cluster_id`, `name`, `description`). |
| Safe derivation for “this marker contributes to this pattern”? | **Membership-only** truth is safe. **Narrative** (“materially drives”) requires **authored** rules or **approved** templates — **not** present as a dedicated field. |
| New backend contract? | **Optional:** a sprint could add e.g. `contributions: { biomarker_id, cluster_id, relation_type }` or attach **pre-authored** blurbs — otherwise FE can only list membership. |
| Belongs in FE-VISUALISATION-B alone? | **Not** if “contribution” copy must be **clinically meaningful** — that is **content + governance**, likely **B1**. |

---

## 7. Symptom-relevance boundary

- **Phase B** should **remain separate** from symptom relevance **implementation**.  
- **No** results-path symptom association logic was found in FE/BE audit scope beyond **questionnaire** test references.  
- The **reserved slot** should **stay unpopulated** after Phase B unless a **future governed sprint** authorises symptom relevance.  
- **Overlap risk:** personalised **clinician_report** and **insights** must **not** be relabelled as “symptom explanation” without explicit product governance.

---

## 8. Delivery-shape recommendation

### Final recommendation: **`SPLIT_INTO_CONTENT_FOUNDATION_AND_FRONTEND_RENDERING`**

| Phase | Suggested ID | Scope (high level) |
|-------|----------------|-------------------|
| **B1 — Content / contract foundation** | `FE-VISUALISATION-B1` (or KB + BE if governance prefers) | Define **retail-safe** explainer sources: optional biomarker dictionary SSOT, optional system-level educational blurbs, mapping from **signal**/`knowledge_bus` explanations where appropriate, **or** explicit new fields on analysis DTO; ensure **determinism** and **separation** from personalised interpretation; optionally improve cluster description generation **in backend** (prettier names, no raw IDs in user string). |
| **B2 — Frontend rendering** | `FE-VISUALISATION-B2` | **Consume** B1 fields only: biomarker explainer blocks, “Understanding this system” panel, contribution callouts **without** inventing text; integrate with results hierarchy **below** hero interpretation per policy. |

**Why not one sprint:** Phase B **goals** are **content-class** changes. Current `interpretation` **cannot** stand in for authored explainers; **meta** insight graph is **unused** in FE; **signal** YAML prose is **not** wired to biomarker rows. Shipping “enrichment” in one bounded FE-only sprint would either **fake** depth or **silently** narrow scope to trivial formatting.

**`DO_NOT_PROCEED_YET`** applies only if **B1 is not authorised at all** — then Phase B2 has nothing truthful to render. The repo **does** have partial assets (KB signal explanations, cluster membership, scoring transparency strings), so the correct gate is **split**, not **hard stop**.

---

## 9. Likely touched surfaces (future sprints — no work implied)

| Layer | Likely files / areas |
|-------|----------------------|
| **Frontend** | `frontend/app/results/page.tsx`, `frontend/app/components/biomarkers/*`, `frontend/app/components/clusters/*`, new small **educational** components, `frontend/app/types/analysis.ts` |
| **Backend DTO / assembly** | `backend/core/pipeline/orchestrator.py`, `backend/core/dto/builders.py`, `core/models/results.py`, optional new compiler for “retail explainer” bundle |
| **SSOT / content** | `backend/ssot/*`, `knowledge_bus/packages/**/signal_library.yaml` (read-only consumer or curated export), possible new `knowledge_bus` or `docs` content packs |
| **Cluster** | `cluster_engine_v2.py` description formatting; optional `clusters.yaml` descriptions surfaced to FE |
| **Clinician / policy** | Ensure educational copy does **not** duplicate or contradict `clinician_report_v1` — coordination in `report_compiler_v1` / product review |

---

## 10. Evidence index (non-exhaustive)

- `backend/core/pipeline/orchestrator.py` — biomarker `interpretation` assignment (scoring/lab messages).
- `backend/core/dto/builders.py` — `interpretation` on biomarker DTO.
- `backend/core/clustering/cluster_engine_v2.py` — `name` / `description` templates.
- `backend/core/contracts/biomarker_context_v1.py` — code-only context nodes.
- `knowledge_bus/packages/**/signal_library.yaml` — structured `explanation` payloads (signal-scoped).
- `frontend/app/components/biomarkers/BiomarkerDials.tsx` — conditional interpretation display.
- `frontend/app/components/insights/InsightPanel.tsx` — Phase A hero (personalised, not educational encyclopaedia).
- `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` — FE-VISUALISATION purpose statement.
- **Missing from repo at audit:** `docs/architecture/HealthIQ_FE_VISUALISATION_Surface_Policy_Final.md`, `docs/investigations/FE_VISUALISATION_PREFLIGHT.md`.

---

## 11. Charter checklist — required output mapping

| Required section | Location |
|------------------|----------|
| Executive summary | §1 |
| Policy-to-repo | §2 |
| Biomarker explainer audit | §3 |
| System explainer audit | §4 |
| Cluster translation audit | §5 |
| Recommendation | §6 (symptom §7), §8 (delivery shape) |

**Declared recommendation:** **`SPLIT_INTO_CONTENT_FOUNDATION_AND_FRONTEND_RENDERING`** — phases **`FE-VISUALISATION-B1`** (content/contract/backend enrichment foundation) and **`FE-VISUALISATION-B2`** (frontend rendering of enriched content only).
