# Results — Why layer, hero “close call”, and narrative runtime (bounded investigation)

**Date:** 2026-04-12  
**Scope:** Runtime truth only (no code changes, no copy redesign).  
**Question:** For the current results experience, what data exists in stored analysis payloads vs what is rendered for hero, Why/root-cause, and “Narrative summaries”, and why UAT still sees missing runner-up context, shallow Why, and template-like narratives.

---

## Executive summary

1. **Competing secondary finding**  
   - **Yes — in the stored payload:** the full ranked signal list lives under **`meta.insight_graph.report_v1.top_findings`** (each row has `signal_id`, `priority_rank`, `why_it_matters`, `supporting_markers`, etc.).  
   - **Hero does not read that path.** The default hero (`InsightPanel`) consumes only **`clinician_report_v1.sections.page1`**, which is produced by **`compile_clinician_report_v1`** from the same `report_v1` slice — but **runner-up identity for “technical tie-break” mode is only surfaced when `co_primary_signal_ids` is non-empty.** When the compiler resolves `primary_concern_mode == technical_tiebreak_lead` **without** at least two IDs in the tie bucket, **`co_primary_signal_ids` is `[]`** while the policy line still describes a tie. The UI then shows the **“Close call between top findings”** badge but **no “Also closely reviewed” row** (that row is gated on `coPrimaries.length > 0`).  
   - So the issue is **not** that `top_findings[1]` is absent from storage; it is that **the hero contract does not map runner-up from `top_findings` when `co_primary_signal_ids` is empty**, and the **frontend does not consult `meta.insight_graph.report_v1`** for the hero.

2. **Richer “Why” narrative**  
   - **No — there is no separate long-form “Why narrative” field** in the runtime contract comparable to a clinical essay. **`root_cause_v1`** under `report_v1` (and mirrored in **`clinician_report_v1.sections.root_cause`**) is built by a **deterministic root-cause compiler** with **hypotheses**, **`evidence_for` / `evidence_against` / `missing_data` bullets**, and **ranking_rationale** strings — not a free-running personalised narrative layer.  
   - Anything rendered as “deep walkthrough” would require **new emitted content** or **surfacing additional existing fields** (e.g. fuller use of `explainability_report` in `meta`), not merely toggling a hidden flag.

3. **“Narrative summaries” (`insights[]`)**  
   - Provenance is **governed by `core.insights.narrative_runtime_policy`** and **`InsightSynthesizer`** (`backend/core/insights/synthesis.py`). Unless **`HEALTHIQ_NARRATIVE_LLM`**, **`HEALTHIQ_ENABLE_LLM`**, **`LLM_ENABLED`**, and mode allow it, the client resolves to **`MockLLMClient`**, and **`meta.narrative_runtime.runtime_mode`** is typically **`deterministic_mock`** (not live Gemini).  
   - Mock path returns **category-shaped, deterministic summaries** — so **similar depth across categories** is expected when the mock is active.

4. **Wrong layer surfaced?**  
   - The results page **intentionally** treats **`clinician_report_v1`** as the primary structured hero and **`insights[]`** as complementary short narratives under Advanced. **`meta.insight_graph`** carries the richest graph + **`report_v1`** but is **not** used to drive the default hero in the current UI. So **richer structured data exists in `meta` while the hero reads a narrower compiled slice** — behaviour is consistent with code paths, not a random bug.

---

## Files inspected (evidence)

| Area | Path |
|------|------|
| API DTO shape | `backend/core/dto/builders.py` — `build_analysis_result_dto` |
| Orchestrator meta assembly | `backend/core/pipeline/orchestrator.py` — `meta["insight_graph"] = insight_graph.model_dump()`, `meta["narrative_runtime"]` from synthesis summary |
| Insight graph + report_v1 | `backend/core/analytics/insight_graph_builder.py` — `compile_report_v1` → `InsightGraphV1.report_v1` |
| Clinician report / page1 | `backend/core/analytics/report_compiler_v1.py` — `compile_clinician_report_v1`, `_resolve_page1_concern_mode`, `co_primary_signal_ids` |
| Report contract | `backend/core/contracts/report_v1.py` — `ReportTopFindingV1` |
| Narrative LLM gates | `backend/core/insights/narrative_runtime_policy.py` |
| Insight synthesis + mock | `backend/core/insights/synthesis.py` — `MockLLMClient`, `synthesis_summary["narrative_runtime"]` |
| Hero UI | `frontend/app/components/insights/InsightPanel.tsx` |
| Narrative tab UI | `frontend/app/components/insights/InsightsPanel.tsx` |
| Narrative meta presentation | `frontend/app/lib/narrativeRuntimePresentation.ts` |
| Results page wiring | `frontend/app/(app)/results/page.tsx` |
| Representative stored shape | `backend/tests/fixtures/reports/clinician_report_v1_ab.json` (post–Wave 2 compiler) |

---

## 1. Completed analysis payload — field map

What the client typically receives from **`GET /api/analysis/result`** (via `build_analysis_result_dto`) includes at least:

| Concern | Top-level / path | Role |
|--------|------------------|------|
| Hero (default) | **`clinician_report_v1`** (compiled from `meta.insight_graph.report_v1` + biomarker rows) | **`sections.page1`**: `primary_concern`, `key_findings[]`, `primary_concern_mode`, **`co_primary_signal_ids`**, `confidence_and_missing_data`, `top_hypothesis_line`, `ranking_policy_version`, etc. |
| Full ranked findings | **`meta.insight_graph.report_v1.top_findings`** | Ordered **`ReportTopFindingV1`** list: **`priority_rank`**, **`signal_id`**, **`why_it_matters`**, **`supporting_markers`**, etc. |
| Root cause / Why (structured) | **`clinician_report_v1.sections.root_cause`** and **`meta.insight_graph.report_v1.root_cause_v1`** | Hypotheses, evidence items, missing data — **not** a single narrative field |
| Narrative summaries | **`insights[]`** | Short category insights from synthesis |
| Narrative provenance | **`meta.narrative_runtime`** | **`runtime_mode`**, **`policy_reason`**, **`client_kind`**, etc. |
| Extra explainability | **`meta.explainability_report`** | Present on orchestrator path; **not** wired as default hero body in current results page |

**`build_analysis_result_dto`** passes **`meta` through unchanged** and sets **`insights`**, **`clinician_report_v1`** (recompiled from `report_v1` + biomarkers). See `backend/core/dto/builders.py` lines 24–56.

---

## 2. Competing secondary finding — exists in payload?

**Yes (as data).**  
Path: **`meta.insight_graph.report_v1.top_findings`** — index **`1`** (and beyond) holds the second and lower-ranked findings when multiple signals exist.

**Why the hero does not show it**

- **UI source:** `InsightPanel` only uses **`clinician_report_v1.sections.page1`** (`frontend/app/components/insights/InsightPanel.tsx`). It does **not** read **`meta.insight_graph.report_v1.top_findings`**.
- **Runner-up row gating:** The “Also closely reviewed” line renders only when **`page1.co_primary_signal_ids`** is non-empty **and** mode is tie/ambiguity (`showCoPrimaryRow`).
- **Compiler behaviour:** For **`technical_tiebreak_lead`**, **`co_primary_signal_ids`** is filled only when the **tie bucket** from **`_technical_tie_bucket_signal_ids(top_findings)`** has **≥ 2** signal IDs. Otherwise it is **`[]`**. Example from governed fixture **`clinician_report_v1_ab.json`**: **`primary_concern_mode`: `technical_tiebreak_lead`**, **`co_primary_signal_ids`: `[]`** — so the badge can read “close call” while **no IDs** are passed for the secondary row.

**Conclusion:** The **secondary finding is not “dropped from storage”** in the general case; it is **addressable from `top_findings[1]`** in **`meta`**. It **is** omitted from the **hero-specific** fields when **`co_primary_signal_ids`** is empty, and the **frontend never falls back** to **`top_findings`**.

---

## 3. Richer Why narrative — exists in payload?

**No — not as a dedicated deep narrative channel.**

- **`root_cause_v1` / `clinician_report_v1.sections.root_cause`** are **structured**: hypotheses with **`title`**, **`summary`**, **`evidence_for` / `evidence_against` / `missing_data`**, **`ranking_rationale`**, etc. (`backend/core/analytics/root_cause_compiler_v1.py` and contracts under `core/contracts/root_cause_v1.py`).
- There is **no** separate field meaning “personalised explanatory walkthrough paragraph” in the same sense as a long LLM essay; depth is **by design** bounded compiler output.

**Richer material elsewhere:** **`meta.explainability_report`** is attached on the orchestrator path (`orchestrator.py` ~2065–2068). The **default results page does not render it** as the main Why layer today.

---

## 4. “Narrative summaries” — source for a typical run

- **Stored:** **`insights[]`** on the analysis result; **`meta.narrative_runtime`** records policy outcome.
- **Generation:** **`InsightSynthesizer.synthesize_insights`** (`backend/core/insights/synthesis.py`). Client selection uses **`MockLLMClient`** unless gates pass and **`GeminiClient`** is configured — see **`_create_llm_client`** and **`resolve_narrative_llm_allow_llm`** (`allow_llm=None` on HTTP path per `analysis.py` comments).
- **`meta.narrative_runtime`:** Built by **`narrative_runtime_meta_from_decision`** (`narrative_runtime_policy.py`). Typical values include **`runtime_mode`: `deterministic_mock`** when the client class is **`MockLLMClient`** (lines 141–171).
- **Why summaries feel uniformly shallow under mock:** **`MockLLMClient.generate`** returns **fixed template-style content** per category (`synthesis.py` ~91+), so **all categories** tend to **look similar in depth and tone**.

**Gemini:** Only when **`runtime_mode`** reflects **`live_gemini`** (and client kind **`gemini`**) — otherwise not the active path for narrative text.

---

## 5. Rendered UI → source fields

| UI region | Component | Primary data source |
|-----------|-----------|---------------------|
| Hero | `InsightPanel` | **`clinician_report_v1.sections.page1` only** |
| Lead hypothesis evidence (summary strip) | `RootCauseEvidenceSummary` | **`clinician_report_v1.sections.root_cause.hypotheses[0]`** evidence lists |
| Narrative summaries tab | `InsightsPanel` | **`insights[]`**, **`meta.narrative_runtime`** for empty states |
| Clinician report tab | `ClinicianReportRenderer` | **`clinician_report_v1`** |
| System groups | `ClusterSummary` | **`clusters[]`** from DTO |
| Biomarker cards | `BiomarkerDials` | **`biomarkers[]`** |

**Shallowest layer?** The **hero** is intentionally **narrow** (compiled page1). **`meta.insight_graph.report_v1.top_findings`** is **richer for ranking** but **not bound** to the hero component. **`insights[]`** may be **mock** and **shallower** than a future live narrative layer.

---

## 6. Direct answers (required)

| Question | Answer |
|----------|--------|
| Does the competing secondary finding exist in stored/runtime payload? | **Yes** — typically as **`meta.insight_graph.report_v1.top_findings[1]`** (when ≥ 2 findings). |
| Does a richer Why narrative already exist as a single field? | **No** — only **structured** root-cause and **bounded** compiler strings; optional **`explainability_report`** is separate. |
| Are narrative summaries Gemini / fallback / deterministic? | **Default path:** **`deterministic_mock`** unless env gates enable **live Gemini** — see **`meta.narrative_runtime.runtime_mode`**. |
| Is richer data hidden / not rendered? | **Partially yes:** **`top_findings`** and **`explainability_report`** are **not** used for the **default hero**; **`co_primary_signal_ids`** may be **empty** even in tie-break mode, so the UI **cannot** show runner-up without further wiring. |

---

## 7. Smallest safe next-fix scope (non-prescriptive)

1. **Hero runner-up:** When **`primary_concern_mode`** indicates tie/ambiguity, **derive display of runner-up** from **`top_findings[1]`** (or fix **`co_primary_signal_ids`** population when `len(top_findings) > 1`) **and/or** pass **`meta.insight_graph.report_v1.top_findings`** into a thin hero helper — **presentation-only** if data already exists.  
2. **Why depth:** Either **emit one bounded “walkthrough” paragraph** from existing structured evidence (compiler-only), or **surface a vetted slice of `explainability_report`** in results — **scope must stay governed**, not ad-hoc LLM.  
3. **Narratives:** Treat **`meta.narrative_runtime`** as the **truth label** for UAT; enable live Gemini only with **explicit env + product** approval.

---

## 8. Recommended sprint classification

- **P1 — Results contract / presentation:** Hero runner-up + `co_primary` consistency (**ties** UAT-027).  
- **P1 — Compiler / optional explainability surfacing:** Deeper **Why** without new reasoning engines (**ties** UAT-028).  
- **P2 — Narrative runtime:** Env + quality bar for **live** `insights[]` vs **mock** (ties narrative shallow-template UAT themes).

---

## 9. Ambiguity / limits

- This report **does not** reference a specific production **`analysis_id`** from UAT; conclusions are **code-path and fixture-backed**. To validate one real run, inspect that result’s JSON for **`meta.insight_graph.report_v1.top_findings`** and **`meta.narrative_runtime`**.  
- **Persistence layer:** If any storage path strips **`meta`**, behaviour could differ; the **API builder** assumes full **`meta`** on the in-memory result object.
