# Full results experience — end-to-end narrative contract inventory

**Date:** 2026-04-12  
**Type:** Bounded runtime and contract investigation (no code changes, no copy redesign).  
**Goal:** Map every explanation-bearing layer from storage → backend producer → frontend renderer; trace Gemini handoff; assess bottlenecks.

---

## Executive summary

1. **The results API carries a deep structured stack** in `meta` (especially `insight_graph`, `explainability_report`, `burden_vector`, `narrative_runtime`) plus a **compiled** `clinician_report_v1` and **`insights[]`** for Layer C narrative cards.

2. **The default product surface uses only a subset.** The primary layout (`frontend/app/(app)/results/page.tsx`) leads with **`clinician_report_v1`** (hero, trust strip, Why) and **`clusters` / `biomarkers`**, and tucks **narrative summaries** and **full clinician report** behind **Advanced analysis** (collapsed by default). **`meta.explainability_report` is not referenced by any frontend module** (repository search: no matches in `frontend/` for `explainability`)—so a large, arbitration-rich structure is **stored on the result object** but **not rendered** in the shipped UI.

3. **Gemini in the analysis→results path** is used by **`InsightSynthesizer`** via **`core.llm.gemini_client.GeminiClient`** only when the **LLM client is live** (not `MockLLMClient`). The HTTP API constructs **`AnalysisOrchestrator()`** with default **`allow_llm=None`**, which flows into **`resolve_narrative_llm_allow_llm`** (`backend/core/insights/narrative_runtime_policy.py`): **live Gemini for insights requires explicit double opt-in** (`HEALTHIQ_NARRATIVE_LLM` and `HEALTHIQ_ENABLE_LLM`, plus `LLM_ENABLED`, non-test mode). Otherwise the synthesizer uses **`MockLLMClient`**, and for the **InsightGraph path** the mock returns **thin “translation” cards** (fixed title/body pattern) when the prompt contains the governed graph markers—**not** rich prose.

4. **Input to the narrative LLM (when live):** Per **`_generate_category_insights_from_graph`** (`backend/core/insights/synthesis.py`), each category call passes **`insight_graph_json`** (full serialized InsightGraph) and **`explainability_report_json`** (full serialized explainability) into **`llm_client.generate_insights`**. So the **contract is information-rich at the prompt boundary**; **shallowness in production UX** is therefore **not** primarily “Gemini only sees three numbers”—it is **gating (mock path)** plus **validator + UI surfacing**, not raw lack of structured inputs.

5. **Orchestrator insight DTO shaping:** When building final insights, the orchestrator maps **`insight.get('summary')`** to **both** `title` and `description` on **`InsightResult`** (`backend/core/pipeline/orchestrator.py`, insight DTO construction). That **collapses** distinct headline vs body even when upstream could differ.

6. **Bottleneck assessment:**
   - **Frontend:** **Partial** — Advanced section is optional/collapsed; **`explainability_report` unused**; many **`meta` fields** never bound to components.
   - **Stored/generated contract:** **Partial** — **Deterministic/clinician layers can be strong**; **`insights[]` is intentionally thin** under mock/translation path; **live Gemini path** could produce richer validated cards **if** env gates are on and validation passes.
   - **Separate Gemini use:** **Document upload / parsing** uses Gemini in **`backend/app/routes/upload.py`** — **not** the same handoff as results **`insights[]`** (called out for disambiguation only).

---

## 1. Files inspected (primary)

| Area | Path |
|------|------|
| API DTO | `backend/core/dto/builders.py` (`build_analysis_result_dto`) |
| Orchestrator run + meta assembly | `backend/core/pipeline/orchestrator.py` |
| Insight synthesis + Gemini/mock | `backend/core/insights/synthesis.py` |
| Narrative LLM policy | `backend/core/insights/narrative_runtime_policy.py` |
| Clinician report compile | `backend/core/analytics/report_compiler_v1.py`, `backend/core/contracts/clinician_report_v1.py` |
| Explainability build | `backend/core/analytics/explainability_builder.py` (referenced from orchestrator) |
| Retail explainers | `backend/core/analytics/retail_explainer_assembly_v1.py` (`attach_retail_explainers_v1` per orchestrator) |
| HTTP analysis route | `backend/app/routes/analysis.py` (`AnalysisOrchestrator()`) |
| Results page | `frontend/app/(app)/results/page.tsx` |
| Components | `InsightPanel.tsx`, `RootCauseEvidenceSummary.tsx`, `PipelineStatus.tsx`, `ClusterSummary.tsx`, `BiomarkerDials.tsx`, `InsightsPanel.tsx`, `InsightCard.tsx`, `ClinicianReportRenderer.tsx` |
| Narrative presentation | `frontend/app/lib/narrativeRuntimePresentation.ts` |

---

## 2. Payload / storage paths inspected

| Path | Role |
|------|------|
| **`clinician_report_v1`** | Top-level DTO field; produced in **`build_analysis_result_dto`** via **`compile_clinician_report_v1`** from **`meta.insight_graph.report_v1`** (+ biomarkers / medical snapshot). |
| **`meta.insight_graph`** | Large graph: **`signal_results`**, **`report_v1`** (top_findings, top_chains, root_cause_v1, …), **cluster_summary**, **interaction_***, **biomarker_context**, etc. |
| **`meta.explainability_report`** | Set in orchestrator: **`meta["explainability_report"] = exp_dump`** (`orchestrator.py`). |
| **`meta.narrative_runtime`** | Copied from **`synthesis_summary["narrative_runtime"]`** when present. |
| **`meta.burden_vector`** | System burden vectors + diagnostics. |
| **`insights[]`** | Top-level; from orchestrator insight DTOs after synthesis. |
| **`biomarkers[]`**, **`clusters[]`** | Enriched with optional **`biomarker_educational_explainer`**, **`contribution_context`**, **`system_educational_explainer`** via **`attach_retail_explainers_v1`**. |

---

## 3. Explanation-bearing layers — full table

| Layer | Payload path | Backend producer | Frontend renderer | Character (rich / shallow / template / technical / unrendered) |
|-------|----------------|------------------|-------------------|----------------------------------------------------------------|
| **Hero / page1** | `clinician_report_v1.sections.page1` | `compile_clinician_report_v1` (`report_compiler_v1.py`) from `report_v1` + ranking helpers | `InsightPanel` | **Structured, deterministic** — bounded strings; improved runner-up fields (Wave 2). Consultant-like depth is **contract-limited** (compiler templates), not FE-only. |
| **Trust strip** | `clinician_report_v1.data_quality`, `sections.confirmatory_tests`, + page-derived `missingChapterLine` | Compiler + `page.tsx` heuristic | `PipelineStatus` | **Consumer-safe** completeness/caveat copy; **not** full technical burden. |
| **Why / lead hypothesis** | `clinician_report_v1.sections.root_cause` | `compile_clinician_report_v1` / root cause selection from graph | `RootCauseEvidenceSummary` | **Structured** hypotheses, evidence lists, ranking rationale — **medium depth** when present. |
| **System groups** | `clusters[]` (name, description/summary, severity, biomarkers, optional `system_educational_explainer`) | Cluster pipeline + retail explainer attach | `ClusterSummary` | **Variable** — retail explainer **optional**; cluster text often **short**. |
| **Biomarker evidence** | `biomarkers[]` (`interpretation`, `biomarker_educational_explainer`, `contribution_context`) | Pipeline + `attach_retail_explainers_v1` | `BiomarkerDials` | **Optional B1A** explainers — **rich when present**, absent when not assembled. |
| **Overall / risk (Advanced overview)** | `overall_score`, `risk_assessment` | Scoring / engine | `page.tsx` Advanced → Overview tab | **Summary metrics** — not a full narrative layer. |
| **Overflow key findings** | `clinician_report_v1.sections.page1.key_findings[1..]` | Compiler | Listed on Advanced Overview | **Structured bullets** — supports hero, not standalone story. |
| **Narrative summaries** | `insights[]`, `meta.narrative_runtime` | `InsightSynthesizer.synthesize_insights` → `GeminiClient` **or** `MockLLMClient` | `InsightsPanel`, `InsightCard` | **Template / thin** under mock graph translation; **potentially richer** under live Gemini + `validate_llm_output_v2` **if** gates on and validation passes. |
| **Clinician report (full)** | `clinician_report_v1` | Same compiler | `ClinicianReportRenderer` | **Deepest deterministic** retail-safe report in one place. |
| **Raw graph: signals / chains** | `meta.insight_graph.signal_results`, `report_v1.top_chains`, `interaction_summary` | Insight graph + report compiler | **Partially** reflected in compiler → page1 chains; **not** a separate “story” block on main page | **Rich structured** — **surfacing** is via compiler, not direct JSON dump. |
| **Explainability v1** | `meta.explainability_report` | `build_explainability_report_v1` | **None** (no `frontend` references found) | **Rich arbitration/dominance** — **technical / clinical-adjacent** — **stored but not rendered** in current UI. |
| **Burden vector** | `meta.burden_vector` | Orchestrator from insight graph | **Not** on main retail sections | **Technical** replay / diagnostics. |
| **Replay manifest** | `replay_manifest` | Orchestrator | Not user-facing narrative | **Provenance / technical**. |

---

## 4. Results page → source fields (major sections)

| Section | Component | Source field(s) | Richer unused data |
|---------|-----------|-------------------|---------------------|
| Hero interpretation | `InsightPanel` | `clinician_report_v1.sections.page1` | Raw `meta.insight_graph.report_v1.top_findings` (partially compiled into page1); full **`explainability_report`** unused in UI. |
| Trust strip | `PipelineStatus` | `data_quality`, `confirmatory_tests`, computed missing line | — |
| Lead hypothesis Why | `RootCauseEvidenceSummary` | `sections.root_cause` | Other hypotheses in same finding **not** expanded by default in this component (top hypothesis only). |
| System groups | `ClusterSummary` | `clusters[]` | Full **`meta.insight_graph.cluster_summary`** not exposed beyond cluster list as mapped. |
| Biomarker evidence | `BiomarkerDials` | `biomarkers[]` per-marker fields | Raw graph biomarker nodes in **`insight_graph`** not shown as JSON. |
| Advanced → Overview | inline | `overall_score`, `risk_assessment`, `key_findings` overflow | **`explainability_report`**, **burden_vector** still unused. |
| Advanced → Narrative | `InsightsPanel` | `insights[]`, `narrativeRuntime` from `meta` | Same as table above — **`insights`** thin when mock path. |
| Advanced → Clinician | `ClinicianReportRenderer` | `clinician_report_v1` | Same object as hero source — **consistent**. |

---

## 5. Gemini handoff path (analysis → results)

### 5.1 Where Gemini is invoked

- **Insight narrative path:** `InsightSynthesizer` → **`llm_client.generate_insights(system_prompt, user_prompt, category)`** (`synthesis.py`).
- **Implementation:** **`core.llm.gemini_client.GeminiClient`** (when selected) vs **`MockLLMClient`**.

### 5.2 When Gemini is **not** used (typical dev / gated prod)

- **`MockLLMClient`** is returned when **`allow_llm`** resolves false via **`resolve_narrative_llm_allow_llm`** (e.g. **`HEALTHIQ_NARRATIVE_LLM`** not set, or **`HEALTHIQ_ENABLE_LLM`** false, or **`LLM_ENABLED`** false, or test/fixture mode) — see **`narrative_runtime_policy.py`** and **`_create_llm_client`** in **`synthesis.py`**.
- For the **InsightGraph** user prompt, **`MockLLMClient.generate_insights`** detects graph markers and returns a **fixed “translation” JSON** (`{category}_translation_*`, generic title/actions) — **intentionally thin** validated-shaped output.

### 5.3 When Gemini **is** used

- **`GeminiClient`** constructed when provider configured, **`LLM_ENABLED`**, mode not test, and **explicit allow + env** conditions satisfied (see **`_create_llm_client`**).
- **Input contract:** Full **`insight_graph`** JSON string + full **`explainability_report`** JSON string + lifestyle profile, per **`_generate_category_insights_from_graph`** — **large structured envelope**, not a one-line summary.
- **Post-processing:** **`validate_llm_output_v2`** against **`build_validator_prompt_json_from_insight_graph_dict`** — PRD notes **status/score-only** safe biomarker view in validator prompt (`synthesis.py` comments).

### 5.4 Other Gemini usage (out of scope for “results narrative”, but disambiguated)

- **`backend/app/routes/upload.py`** — document / lab extraction via LLM — **upstream of** analysis results, **different** contract than **`insights[]`**.

### 5.5 API default orchestrator

- **`backend/app/routes/analysis.py`** — **`AnalysisOrchestrator()`** with **`allow_llm=None`** — relies on **policy** for narrative, not an explicit `True`.

---

## 6. Is the narrative contract the limiting factor?

| Question | Finding |
|----------|---------|
| Rich data exists but not rendered? | **Yes (partial)** — especially **`meta.explainability_report`** and parts of **`insight_graph`** not bound to retail components. |
| Only shallow data exists everywhere? | **No** — **`clinician_report_v1`** and graph internals can be **substantial**; **`insights[]`** is **often shallow** due to **mock translation path** and **orchestrator title/description collapse**. |
| Gemini fed shallow summaries? | **Not at prompt construction** — full IG + explainability JSON strings are passed; **output** may be rejected by validator or thinned by mock. |
| Final narrative layer inactive? | **Often yes in default gated environments** — **`meta.narrative_runtime`** will show **mock/deterministic** modes when LLM not allowed. |

---

## 7. Frontend vs contract bottleneck (verdict)

| Question | Answer |
|----------|--------|
| Is the frontend the main bottleneck? | **Partial** — **Advanced** is secondary/collapsed; **`explainability_report`** unused; many **`meta`** fields never mapped. |
| Is the stored/generated contract the main bottleneck? | **Partial** — **Storage is deep**; **Layer C `insights[]`** is **shallow** under default mock path; **deterministic report** is the reliable “consultant-like” layer but **bounded by compiler design**. |

---

## 8. Smallest safe next fix scope (non-prescriptive)

1. **Operational truth:** For any environment, record **`meta.narrative_runtime`** and one **`insights[0]`** sample to classify **live vs mock** without code changes.  
2. **Product clarity:** Decide whether **`explainability_report`** should ever be **user-visible** (Advanced/Clinician) vs **audit-only** — today it is **audit/storage-only** in UI terms.  
3. **Env / governance:** Treat **double opt-in** for narrative LLM as a **deliberate** quality gate; “world-class” prose is **not** expected when gates are off.

---

## 9. Recommended sprint grouping (next remediation wave)

| Track | Focus |
|-------|--------|
| **Narrative runtime / ops** | Validate production env matrix; document expected **`insights[]** depth per mode. |
| **FE surfacing (governed)** | Optional Advanced panels for **sanitized** explainability excerpts (if product approves), without new authority sources. |
| **Contract / compiler** | Deeper deterministic copy is **compiler work**, not LLM — separate from Layer C. |

---

## Exact output path

**File written:** `docs/investigations/2026-04-12_full_results_narrative_contract_inventory.md`

---

*End of report.*
