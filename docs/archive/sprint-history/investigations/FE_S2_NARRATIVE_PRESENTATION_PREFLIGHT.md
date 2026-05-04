# FE-S2 Narrative Presentation Layer — Preflight (READ-ONLY)

**work_id:** FE-S2-PREFLIGHT  
**Date:** 2026-04-09  
**Scope:** Investigation only — no implementation, no sprint start.

---

## 1. Executive summary

**What already exists on the frontend**

- A **deterministic hero** is implemented as `InsightPanel`, which renders **`clinician_report_v1.sections.page1`** (headline, single interpretation paragraph, confidence line, next-step cue). It is explicitly *not* driven by `insights[]`.
- **`insights[]`** is rendered only inside **Advanced analysis → “All insights”**, via `InsightsPanel` / `InsightCard`, with secondary visibility (overview tab shows a short alert pointing users to that tab when insights exist).
- **Clinician report** full contract is rendered in **Advanced analysis → “Clinician report”** via `ClinicianReportRenderer`.
- **Trust / data-quality** copy comes from **`clinician_report_v1.data_quality`** and related fields through `PipelineStatus` (Trust strip).
- **Educational explainers** (biomarker + system group) and **contribution context** are already wired on the retail path (`BiomarkerDials`, `ClusterSummary`) per prior visualisation work.
- The analysis API client **persists `meta`** on the result object (`AnalysisService.getAnalysisResult`), and the store type allows `meta`, but **no results UI reads `meta` today** (so runtime narrative metadata is effectively invisible to users).

**What is missing**

- **Explicit “narrative layer” framing**: the UI still labels `insights[]` as **“Health Insights”** and copy elsewhere says **“engine insights”**, which does not communicate translation-only / Layer C narrative (and can read like primary analytical truth).
- **Runtime-aware presentation**: backend attaches **`meta.narrative_runtime`** (from orchestrator + synthesis), including `synthesizer_allow_llm_resolved`, `runtime_mode`, `policy_reason`, and optional `outcome` when live Gemini returns no validated insights. The frontend **never consumes** this, so users cannot distinguish “narrative disabled”, “ran but produced no accepted narratives”, and “none returned for other reasons” except by inference from an empty list.
- **Typed FE contract for narrative metadata**: `AnalysisResult` in `frontend/app/types/analysis.ts` does not declare `narrative_runtime`; today it is an opaque `meta` bag if present.
- **Wireframe gap**: the locked wireframe’s Advanced Analysis third tab is **“Technical Detail”**; the app implements **“Overview” | “All insights” | “Clinician report”**. FE-S2 authors should decide whether “Technical Detail” was renamed intentionally or is still a design delta (out of scope for this preflight to resolve product-wise, but it is a **labelling/hierarchy** input).

**Is FE-S2 justified now?**

**Yes.** Backend narrative enablement (BE-S1A/B-style governance) assumes a governed **presentation** boundary so Layer C prose is not mistaken for deterministic reporting. The repo already separates hero (clinician page1) from `insights[]`, but **labelling, hierarchy, and runtime truthfulness** are not yet aligned with the narrative story. FE-S2 is the right follow-on, scoped to presentation and coexistence—not new reasoning.

---

## 2. Strategy interpretation (adopted roadmap)

**Source:** `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` (Wave 6).

**What FE-S2 is stated to deliver**

- **“Purpose: render the narrative cleanly in the frontend.”** It sits in Wave 6 with **BE-S1 — LLM Narrative Production Enablement** and before **FE-LAUNCH-INTEGRATION**.
- Wave 6 intent: **“translate structured truth into readable outputs”** while narrative remains **last**, after deterministic truth and context hardening.

**What “Narrative Presentation Layer” means in roadmap context**

- Presentation of **Layer C narrative** (readable translation) **on top of** governed structured outputs, **without** moving reasoning into the LLM.
- In current architecture, the primary user-visible narrative artifact from the LLM path is **`insights[]`** (validator-backed synthesis), while the **clinician report** remains the structured deterministic surface compiled for reporting.

**Relationship to other tracks**

| Track | Relationship to FE-S2 |
|--------|------------------------|
| **BE-S1A / BE-S1B** | Backend provides validated `insights[]`, runtime policy metadata in `meta.narrative_runtime`, and unchanged deterministic report compilation. FE-S2 **consumes and frames** these artifacts; it does not redefine contracts except optionally for **typing / display-only** fields already on the wire. |
| **Clinician report rendering** | Already a **separate** surface (`ClinicianReportRenderer`). FE-S2 should **preserve** visual and cognitive separation: narrative must not visually replace or subsume the report. |
| **Results page UX already implemented** | Retail stack (Hero → Trust → System groups → Biomarker evidence → Advanced) matches the locked wireframe package structurally; narrative belongs as a **companion** layer, not a second hero. |
| **FE-LAUNCH-INTEGRATION** | Shell integration (auth, history, dashboard, account) is **orthogonal**; narrative presentation should not be blocked on shell work, but launch polish may later **reuse** the same narrative section patterns. |

**What the roadmap does *not* imply FE-S2 should do**

- Replace or rewrite **backend** narrative generation, validation, or orchestration.
- Build the **full product shell** or dashboard/history (that is FE-LAUNCH-INTEGRATION / FE-PAGES).
- Make **unbounded LLM prose** the primary “truth” surface or merge it into the deterministic clinician report blocks.
- Introduce **new analytical ranking** in the frontend (sorting inside `InsightsPanel` is presentation-only today; any change that re-orders narrative as “clinical priority” would be out of scope without explicit governance).

---

## 3. Current frontend audit

### 3.1 `insights[]` — where, how prominent, how framed

| Aspect | State |
|--------|--------|
| **Location** | **Present:** Only under **Advanced analysis** → tab **“All insights”** (`frontend/app/results/page.tsx`). |
| **Prominence** | **Partial:** Hidden behind expand + tab; overview tab shows an **Alert** when `insights.length > 0` nudging users to open “All insights”. Not on the main retail scroll path. |
| **Framing** | **Partial / risky:** `InsightsPanel` title is **“Health Insights”**; overview copy says **“engine insight(s)”**. Neither says **narrative**, **translation**, or **non-diagnostic** Layer C. |
| **Treated as narrative?** | **No** — treated as generic “insights”. |

**Evidence (results page structure):**

- `insights` from `currentAnalysis?.insights`; `InsightPanel` consumes **`clinician_report_v1`** only for the hero; `InsightsPanel` consumes **`insights`**.

### 3.2 Clinician report vs narrative vs explainers

| Surface | Content type | Coexistence today |
|---------|----------------|-------------------|
| **Hero (`InsightPanel`)** | Deterministic **page1** strings from `clinician_report_v1` | **Clearly separated** from `insights[]`. |
| **Trust strip (`PipelineStatus`)** | Deterministic **data quality** + confirmatory tests | Separated. |
| **System groups / biomarkers** | Deterministic scores + **governed educational** text | Explainer layers are distinct from `insights[]`. |
| **Advanced → Clinician report** | Full **ClinicianReportV1** | Separated tab from **All insights**. |

**Confusion risk (real but manageable):**

- **Naming:** `InsightPanel` is the **hero** (clinician), while **`InsightsPanel`** is **`insights[]`**. The word “insight” appears in both paths with different meanings — **present naming debt**, not yet user-facing catastrophic overlap because the hero title is **“Hero interpretation”**.
- **Copy:** “Health Insights” / “engine insights” can imply **primary analytical output**, which conflicts with the governance story (deterministic report + translation).

### 3.3 Scaffolding already useful for FE-S2

- **Present:** Tabbed Advanced analysis, `InsightsPanel` grouping/filtering, `InsightCard` for card-level narrative fields (`summary`/`title`, evidence, recommendations).
- **Partial:** Empty state for no insights is generic (“No insights available yet”) with **no** narrative-runtime explanation.
- **Missing:** Dedicated **narrative section header** (e.g. translation / Layer C), **microcopy** tying insights to structured report, and **runtime** footnotes or badges from `meta.narrative_runtime`.

### 3.4 Other surfaces (secondary)

- **`frontend/app/demo/page.tsx`:** Uses `InsightsPanel` with mock data — not production results flow; note for regression only.
- **`ClusterInsightPanel` / `clusterStore`:** Separate “cluster insights” concept; not the main `insights[]` narrative path for results v2.

---

## 4. Contract / payload audit (frontend ↔ backend)

### 4.1 What the frontend already receives

From `frontend/app/services/analysis.ts` mapping of `GET /analysis/result`:

- **`insights`** — array (passed through).
- **`clinician_report_v1`** — compiled on backend via DTO builder.
- **`meta`** — **passed through via `meta: result.meta || {}`** (so **`meta.narrative_runtime`** is on the wire when backend populates it).
- **`result_version`, `replay_manifest`** — returned by backend DTO (`build_analysis_result_dto`); **not referenced** in results UI at time of audit.

Types: `frontend/app/types/analysis.ts` defines **`Insight`**, **`ClinicianReportV1`**, **`AnalysisResult.meta?: Record<string, any>`** — **no** explicit `narrative_runtime` typing.

### 4.2 What the backend attaches (relevant to narrative)

From `backend/core/dto/builders.py` and `backend/core/pipeline/orchestrator.py`:

- **`build_analysis_result_dto`** returns full **`meta`** and **`clinician_report_v1`**.
- Orchestrator merges **`insights_result.synthesis_summary.narrative_runtime`** into **`meta["narrative_runtime"]`** when present.

Shape (conceptual): policy version, `runtime_mode`, `client_kind`, boolean gates, `policy_reason`, optional **`outcome`** (e.g. no validated insights after live call — see `core/insights/synthesis.py`).

### 4.3 Does FE-S2 need backend contract changes?

**Not strictly required** for a first **presentation-only** slice: `insights[]` and `clinician_report_v1` are sufficient to **relabel and reposition** narrative.

**Recommended for a second phase** (runtime truthfulness): **optional FE typing** (and possibly a **display-only** normalization helper) for `meta.narrative_runtime` — **no backend change** if the shape is already stable.

---

## 5. UX boundary assessment (locked results UX + repo reality)

**Sources:** `docs/architecture/Frontend/HealthIQ_Results_Page_UX_Design_Package.md`; implemented `frontend/app/results/page.tsx`.

### 5.1 Where narrative should sit

- **Should remain** primarily a **companion** layer inside **Advanced analysis**, at least initially — consistent with wireframe (“Clinician report / insights / … progressive disclosure”).
- **Must not** be promoted to **hero** without explicit product/governance approval — the hero is locked to **four page1 blocks** from clinician report, not Layer C.

### 5.2 Hero / Trust / system groups / biomarkers

- **Hero interpretation:** Deterministic **page1** only (already).
- **Trust strip:** Deterministic **data quality** narrative — already distinct from `insights[]`.
- **System groups & biomarkers:** Structured + educational layers — keep **separate** from LLM narrative cards.

### 5.3 What must not happen

- **Narrative replacing** deterministic report sections or hero content.
- **Clinician report** visually merged into **Layer C cards** (single prose stream).
- **Unbounded prose** presented as the **main analytical truth** (no single “wall of text” summary driven only by `insights[]`).
- **Implicit clinical claims** in microcopy (e.g. “diagnosis”, “proves”) — narrative must remain **translation / education / orientation**.

---

## 6. Runtime-state / degraded-mode audit

### 6.1 Information available today on the client

- **`insights.length === 0`:** Observable.
- **`meta.narrative_runtime`:** **Present on API payload** when backend sets it; **not read** by any audited FE code path for results.

### 6.2 Can FE distinguish “why no narrative” today?

| Scenario | FE capability today |
|----------|---------------------|
| Narrative LLM **disabled** by policy | **Cannot** distinguish — empty `insights[]` only. |
| Live call ran, **validator rejected** / no validated insights | **Partial** on backend (`outcome` on `narrative_runtime` in some paths); **missing on FE** (meta unused). |
| Feature “unavailable” vs “ran, nothing qualifying” | **No** — same empty state copy. |

### 6.3 Recommendation for FE-S2

- **Phase 1 (presentation):** Safe **silent omission** or **generic** empty state remains acceptable if copy avoids implying a bug.
- **Phase 2 (runtime):** Surface **non-alarmist** status from **`meta.narrative_runtime`** (e.g. “Narrative summary unavailable in this environment” or “No short summaries passed quality checks for this run”) — exact strings must be governance-reviewed.

---

## 7. Candidate implementation shape (safest first target)

**Safest first target (Phase A — presentation boundary)**

1. **Reframe the “All insights” experience** as the **Narrative / translation** layer (labels, intro copy, optional footnote linking to deterministic hero/report).
2. **Tighten overview-tab alert copy** so “engine insights” language does not contradict governance (or replace with “short narrative summaries”).
3. **Optional:** Light visual distinction (badge, section subtitle) — **not** a new layout pillar.

**Explicitly out of scope for Phase A**

- Moving narrative to hero or above Trust strip.
- Changing clinician report structure or ranking policy display.
- Backend narrative logic changes.
- **FE-LAUNCH-INTEGRATION** shell work.

**Phase B — runtime / empty-state**

1. Read and type **`meta.narrative_runtime`**.
2. Implement a small **explicit matrix** of empty/populated states + tests.
3. Optional: surface **replay / result_version** only if product asks (likely launch or ops, not FE-S2 core).

---

## 8. Dependency / blocker audit

| Item | Blocker? |
|------|----------|
| Missing backend fields for `insights[]` / `clinician_report_v1` | **No** — present. |
| `meta.narrative_runtime` | **Not a blocker** — present on DTO path; FE ignores it today. |
| Results hierarchy conflicts | **No hard conflict** — narrative is already **de-emphasised** vs hero; risk is **copy/naming**, not layout deadlock. |
| Narrative vs deterministic distinction | **Partial debt** — fixable in FE copy/structure. |
| Launch/product questions | **FE-LAUNCH-INTEGRATION** may later decide **where else** narrative appears (history, PDF) — out of scope for minimal FE-S2. |

**Honest gap:** Without Phase B, FE **cannot** truthfully explain all “empty narrative” cases.

---

## 9. Delivery-shape recommendation

### Verdict

**`SPLIT_INTO_PRESENTATION_AND_RUNTIME_STATE_PHASES`**

**Rationale**

1. **Presentation framing** (Phase A) can ship with **no new backend work** and immediately reduces user confusion — bounded and gateable alone.
2. **Runtime truthfulness** (Phase B) requires **disciplined consumption** of `meta.narrative_runtime`, **typing**, and a matrix of states — a **separate** regression and copy review surface, cleaner as its own governed slice.
3. Keeps **FE-S2** aligned with “narrative last”: deterministic surfaces stay stable while narrative presentation hardens in **two controlled steps**.

**If Phase A only were forced into one sprint:** still acceptable under strict scope — but the investigation recommends **not** folding runtime metadata into the same gate without explicit test/coverage expectation.

**Phase A — likely touched surfaces**

- `frontend/app/results/page.tsx` (overview alert copy, optional section intro)
- `frontend/app/components/insights/InsightsPanel.tsx` (title, descriptions)
- Possibly `frontend/app/components/insights/InsightCard.tsx` (footnote / badge only if needed)

**Phase B — likely touched surfaces**

- `frontend/app/types/analysis.ts` (narrow type for `narrative_runtime`)
- `frontend/app/results/page.tsx` or small child component (empty states)
- Tests under `frontend/tests/**` for state matrix

---

## 10. Boundary check — out of scope for FE-S2

FE-S2 presentation work should **exclude**, unless explicitly re-scoped:

- **Backend** narrative generation, validator, or orchestrator changes.
- **FE-LAUNCH-INTEGRATION** (auth shell, dashboard, history pages) except **reuse** of existing results components.
- **Clinician report redesign** beyond coexistence / clarity (no new report sections).
- Broad **marketing/landing** copy.
- **New narrative contracts** or new Layer C schemas.
- **New reasoning logic** or client-side re-ranking of clinical priority.
- Making narrative the **primary truth layer** (hero replacement, single narrative wall).

---

## 11. Evidence index (key files)

| File | Relevance |
|------|-----------|
| `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` | FE-S2 definition, Wave 6 sequencing |
| `docs/architecture/Frontend/HealthIQ_Results_Page_UX_Design_Package.md` | Locked hierarchy, Advanced analysis pattern |
| `frontend/app/results/page.tsx` | Wiring of hero, trust, `insights[]`, clinician report |
| `frontend/app/components/insights/InsightPanel.tsx` | Hero = `clinician_report_v1.page1` |
| `frontend/app/components/insights/InsightsPanel.tsx` | `insights[]` retail framing |
| `frontend/app/components/results/ClinicianReportRenderer.tsx` | Deterministic report tab |
| `frontend/app/services/analysis.ts` | API mapping including `meta` |
| `frontend/app/types/analysis.ts` | DTO types (`Insight`, `ClinicianReportV1`, `AnalysisResult`) |
| `backend/core/dto/builders.py` | `meta` passthrough, clinician compile |
| `backend/core/pipeline/orchestrator.py` | `meta["narrative_runtime"]` merge |
| `backend/core/insights/narrative_runtime_policy.py` | Runtime metadata semantics |
| `backend/core/insights/synthesis.py` | `synthesis_summary`, narrative_runtime, empty outcome |

---

*End of preflight.*
