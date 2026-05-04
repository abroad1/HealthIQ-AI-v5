# BE-S1 Narrative Preflight (BE-S1-PREFLIGHT)

**work_id:** BE-S1-PREFLIGHT  
**mode:** Read-only investigation (no implementation)  
**date:** 2026-04-09  
**authority:** `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` + repository inspection  

---

## 1. Executive summary

### What narrative capability already exists

- **Deterministic “narrative-shaped” output (non-LLM):** `ClinicianReportV1` is compiled deterministically from `report_v1` + biomarkers (`backend/core/analytics/report_compiler_v1.py`, `backend/core/contracts/clinician_report_v1.py`). It includes lab/data-quality caveats and, after recent work, a bounded **medication/supplement interpretation caveat** field driven only by `medical_history_snapshot` in analysis `meta` (`backend/core/dto/builders.py`, `backend/core/pipeline/orchestrator.py`).
- **Layer C LLM path (exists, gated):** `InsightSynthesizer` (`backend/core/insights/synthesis.py`) is wired from `AnalysisOrchestrator.run()` Step 5 via `_synthesize_from_insight_graph`, with **Sprint 7 purity rules**: production synthesis requires `insight_graph` + `explainability_report`; the LLM prompt path uses `format_template_from_insight_graph` in `backend/core/insights/prompts.py`, which injects InsightGraph JSON and derived **status/score-only** biomarker views (comment PRD §4.7).
- **LLM client stack:** `GeminiClient` / `MockLLMClient`, env gates `HEALTHIQ_ENABLE_LLM`, constructor `allow_llm` on `AnalysisOrchestrator` / `InsightSynthesizer` (`synthesis.py` lines 259–275).
- **Offline validation scaffold:** `validate_llm_output_v2` and `LLMResultV2` (`backend/core/llm/validator_v2.py`, `schemas_v2.py`) with fixtures and unit tests — **not invoked** from `InsightSynthesizer._parse_llm_response` (grep shows usage only in `smoke_prompt_v2.py` and tests).
- **Frontend hooks:** Results UI already consumes **`insights`** and optionally **`clinician_report_v1`** (`frontend/app/results/page.tsx`); “narrative” in the product sense is partially **insights list**, partially **clinician report**, not a single dedicated narrative field yet.

### What is missing

- **Production-hard narrative boundary:** LLM outputs are parsed into `Insight` models with normalization, but **no prompt-aligned JSON validation** (numeric invention, unknown fields, evidence reference rules) on the live synthesis path.
- **Prompt doctrine vs roadmap:** `InsightPromptTemplates.SYSTEM_PROMPT` still frames the model as a “clinical biomarker analysis expert” generating “clinically meaningful insights” (`backend/core/insights/prompts.py`), which is **not aligned verbatim** with adopted doctrine “LLM as translation layer only” (`v1.5` §7.2) — behavioural risk of **reasoning leakage via prompt wording**.
- **Verified production path:** Golden runner defaults to **no network LLM** (`run_golden_panel.py`: `enable_llm: bool = False`; `AnalysisOrchestrator(..., allow_llm=bool(enable_llm))`). There is **no requirement** in the default gate that narrative is exercised with real Gemini output.
- **Persistence vs GET `/result` shape:** `/start` persists a **client-shaped** payload that omits `clinician_report_v1`; `GET /analysis/result` recomputes DTO via `build_analysis_result_dto(raw)` (`backend/app/routes/analysis.py`). Narrative/LLM **insights** are stored in `stored.insights`; **clinician_report_v1** is derived on read — acceptable for replay of structured meta, but **operators must understand** which fields are materialised when.
- **Roadmap honesty on “context complete”:** Adopted plan §6.4 still lists context consumption as not fully governed and narrative “should still not be treated as a priority layer until these conditions are stronger”; §14 reiterates context not fully governed. **Repo has advanced** (objective/behavioural context hardening, medication caveat lineage), but **WHY depth, renal map, phenotype unevenness** remain strategic gaps — narrative quality and safety are still bounded by **upstream structured truth strength**.

### Whether BE-S1 is justified now

**Yes, with a split delivery shape —** not because narrative is “missing code,” but because **enabling** the existing LLM path **safely** requires hardening the **translation boundary** (validation, prompts, acceptance, env policy) before treating Layer C as production-complete. Proceeding **without** wiring `validator_v2` (or equivalent) into synthesis would contradict Wave 6’s “final gate” intent.

---

## 2. Strategy interpretation (BE-S1 in roadmap context)

**Source:** `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` Wave 6 (§735–770), core principles §7–§11.

### What BE-S1 is intended to deliver (exact roadmap text)

> **BE-S1 — LLM Narrative Production Enablement**  
> **Purpose:** enable narrative translation on top of governed structured intelligence.  
> **Strategic note:** this governs and activates the existing narrative direction on top of deterministic truth; **it is not a licence to move reasoning into Layer C**.

### What “LLM Narrative Production Enablement” means here

- Turning the **existing** Layer C synthesis path into a **governed, production-trustworthy translation** from **InsightGraph_v1 + ExplainabilityReport_v1** (already built in `orchestrator.run`) into **user-facing narrative artefacts** (today: `Insight` list; roadmap: fuller presentation in FE-S2).
- **Unlocks:** Wave 6 product claim progression — “structured truth → readable outputs” — without relocating metabolic reasoning into the LLM.

### What the roadmap explicitly allows

- Narrative as **translation on top of** deterministic / contracted outputs (§7.2; Wave 6 purpose).
- Wave ordering: **narrative last** after context hardening waves (§13 Wave 5 → Wave 6).
- **FE-S2** after BE-S1: “render the narrative cleanly in the frontend” (§756–757).
- **FE-LAUNCH-INTEGRATION** as the coherent integration pass (auth, persistence, dashboard, narrative) — separate sprint ID (§759–762).

### What the roadmap explicitly forbids

- **No LLM reasoning in the analytical core** (§7.1).
- **Narrative must never become the source of metabolic reasoning** (§7.2).
- **Narrative-first drift** is an anti-pattern (§11.3).
- **Medication boundary:** no silent threshold changes or unconstrained medication-specific reasoning unless later governance authorises (§6.7) — relevant because narrative must not **invent** coaching beyond structured outputs.

### Relationship to FE-S2 and FE-LAUNCH-INTEGRATION

- **BE-S1:** backend enablement + governance of narrative **production**.
- **FE-S2:** presentation of that narrative.
- **FE-LAUNCH-INTEGRATION:** ensures shell, auth, persistence, and narrative **work as one product**.

This preflight **does not** scope FE-S2 or launch integration; it notes **dependencies** (e.g. which API fields carry narrative).

---

## 3. Current architecture audit

| Surface | Status | Evidence / notes |
|---------|--------|------------------|
| InsightGraph build (deterministic) | **Present** | `build_insight_graph_v1` in `insight_graph_builder.py`; consumed by explainability, replay manifest, DTO meta. |
| ExplainabilityReport_v1 | **Present** | Built before synthesis in `orchestrator.run` (~Step 4.72). |
| InsightSynthesizer + graph path | **Present** | `_synthesize_from_insight_graph`; requires `explainability_report` in production (`synthesis.py` 337–340). |
| LLM gating | **Present** | `allow_llm`, `HEALTHIQ_ENABLE_LLM`, `HEALTHIQ_MODE=test`, `LLM_ENABLED` → `MockLLMClient` (`synthesis.py` 259–275). |
| Prompt templates (graph) | **Partial** | `format_template_from_insight_graph` builds prompt from IG + explainability + lifestyle; **system prompt** still “expert / generate insights” not “translate only” (`prompts.py` 12–22, 400+). |
| LLM output validation (v2) | **Partial / scaffold** | `validator_v2.py` tested; **not called** from synthesis parse path. |
| Legacy synthesis path | **Scaffold / gated** | Biomarker/cluster templates exist; **disabled outside fixture/test** (`synthesis.py` 503–505, 382–385). |
| Clinician report (deterministic) | **Present** | `compile_clinician_report_v1`; extended with medication caveat field. |
| DTO clinician_report exposure | **Present** | `build_analysis_result_dto` → `clinician_report_v1` (GET `/result`). |
| Analysis `/start` stored payload | **Partial** | No `clinician_report_v1` at write time; recomputed on GET (`analysis.py` 180–226 vs 337–339). |
| Golden panel narrative artefact | **Partial** | `narrative.txt` = concatenation of **insight** summaries when `write_narrative=True` (`run_golden_panel.py` 408–417); **not** a governed narrative contract. |
| Frontend results | **Partial** | Renders insights + clinician report object; dedicated “narrative” UX is **FE-S2** scope. |
| Retail / Layer3 | **Present / parallel** | `attach_retail_explainers_v1`, `assemble_layer3_insights` in golden runner — separate from InsightSynthesizer LLM path; do not conflate in BE-S1 without preflight. |

---

## 4. Structured truth readiness audit

### Already present and stable enough to **support** translation (with caveats)

| Input | Readiness | Caveat |
|-------|-----------|--------|
| InsightGraph_v1 (serialised) | **High** for shape | Size/completeness varies by panel; must stay **within validated subgraph** for prompts. |
| ExplainabilityReport_v1 | **High** | Required for production synthesis. |
| Report_v1 + root_cause_v1 | **High** | Feeds clinician compiler; deterministic. |
| DataQuality + confidence caveat (clinician) | **High** | Lab-scope; separate from LLM insights. |
| Medication/supplement caveat (clinician) | **High** | Deterministic from `medical_history_snapshot`; must not be contradicted by LLM prose without explicit product rules. |
| Context-hardening outputs (lifestyle_inputs, questionnaire merge) | **Medium–High** | Consumed in Layer B paths; **not automatically duplicated** inside InsightGraph JSON passed to LLM unless explicitly included — check prompt builder for what lifestyle fields are forwarded (`prompts.py` lifestyle_profile). |
| Persistence / replay | **Medium** | `meta.insight_graph`, `replay_manifest`, biomarkers, insights stored; `medical_history_snapshot` on meta for caveat replay. LLM **narrative is not** a separate versioned artifact today — **insights list** is the de facto narrative store. |

### Gaps / weaknesses

- **WHY / signal depth uneven** (roadmap §6.4, §14): LLM can only translate what IG encodes; weak WHY → thin or generic narrative **without inventing** — product expectation must be managed.
- **No enforced alignment** between **LLM insight text** and **clinician deterministic caveat** lines — risk of **tone or implied clinical claims** unless prompts forbid contradiction and validator enforces evidence refs.
- **Validator not wired:** highest-risk gap for “safe translation.”

### Critical structured input “too weak for safe narrative”?

**Not globally false** — the **contract stack is strong enough to start BE-S1**, but **safe** production narrative requires the **validation + prompt boundary** before scaling to real users. Otherwise the bottleneck is **process**, not absence of InsightGraph.

---

## 5. Runtime boundary audit

### Where reasoning currently happens (Layer B / deterministic)

- Signal evaluation, scoring, clustering, InsightGraph construction, explainability, calibration, arbitration, clinician report compilation — **`backend/core/analytics/**`, **`backend/core/pipeline/orchestrator.py`**, **`report_compiler_v1.py`**.

### Where narrative translation may safely begin

- **After** `insight_graph` + `explainability_report` are finalised for the run, in `InsightSynthesizer.synthesize_insights` — **already the designed boundary.**

### Risk of reasoning leakage into prompts

- **High** if prompts ask the model to “generate clinically meaningful insights” and “actionable recommendations” without strict **translation** instructions and **schema validation**.
- **Fallback path** in `_parse_llm_response` creates synthetic insights from raw text on JSON failure (`synthesis.py` 601–614) — **unsafe for production** without guardrails.

### What must remain deterministic

- All of Layer B above; clinician report fields except any future **explicit** LLM companion (none today); ranking policy; signal states; numeric biomarker interpretation policies.

### What may be translated into prose

- Structured IG + explainability + **bounded** lifestyle context snippets that are already in the prompt — as **summaries**, not new facts.

### What must not be delegated to the LLM

- New biomarker values, ranges, diagnoses, drug advice, threshold changes, signal re-ranking, “why” not present in structured inputs.

---

## 6. Candidate output-surface audit

| Candidate | Assessment |
|-----------|------------|
| **Insight list (`dto.insights`)** | **Strongest current hook** — already produced by synthesis; FE already displays. BE-S1 naturally **hardens this path** first. |
| **ClinicianReportV1** | **Deterministic today**; BE-S1 should **not** silently add LLM-generated clinician fields without a **new governed contract** decision. Translation can **reference** clinician structured text, not replace it. |
| **New narrative companion field** (e.g. `narrative_summary_v1` on DTO) | **Possible later**; increases contract + persistence work — better as **phase 2** if Phase 1 focuses on insight quality + validation. |
| **Retail explainer / Layer3** | **Separate assembly**; include only if BE-S1 scope explicitly covers it — default **out of scope** for first BE-S1 phase. |

**Recommendation — safest first narrative target:** **Harden and production-enable the existing `InsightSynthesizer` → `insights[]` path** (translation-only prompts + `validator_v2` + acceptance tests). **FE-S2** presents it; **do not** merge FE work into BE-S1.

**Out of scope for first phase:** wholesale clinician report LLM rewrite; unconstrained `narrative.txt` as product truth; retail narrative unless explicitly scoped.

---

## 7. Dependency / blocker audit

| Blocker | Severity | Notes |
|---------|----------|-------|
| `validator_v2` not wired to synthesis | **High** | Must fix for production honesty. |
| Prompt wording vs §7.2 | **Medium–High** | Rewrite system + category instructions for **translation**. |
| Default LLM off in golden path | **Medium** | Need **opt-in** narrative acceptance test job (CI policy decision). |
| Strategy §6.4 / §14 “context not fully governed” | **Medium (interpretation)** | Repo ahead of doc in places; still true for **WHY depth / renal / phenotype**. |
| FE-S2 not done | **Not a BE-S1 code blocker** | Presentation can follow; API must expose stable narrative fields. |
| OPS/compliance | **Out of scope** per roadmap note on OPS-S1 cold start. |

---

## 8. Delivery-shape recommendation

### Chosen recommendation label

**SPLIT_INTO_CONTRACT_AND_RUNTIME_NARRATIVE_PHASES**

### Rationale

- **Phase 1 — Translation contract & boundary:** Rewire prompts; integrate `validate_llm_output_v2` (or merge schemas with `Insight`); eliminate or strictly gate JSON-failure text fallback; add deterministic fixtures for **approved** narrative outputs when LLM is mock/disabled; define denylist / numeric invention rules at synthesis boundary.
- **Phase 2 — Production enablement & verification:** Policy for `AnalysisOrchestrator(allow_llm=...)` on `analysis` route vs env; optional CI job with `HEALTHIQ_ENABLE_LLM=1` (secrets policy); document persistence of insights; handoff checklist for **FE-S2**.

This respects roadmap §7.4 (split when testability/governance requires) without unnecessary fragmentation: **two clear governable slices**, not many micro-sprints.

### If compressed to one sprint

Possible only if the **single sprint prompt** explicitly lists both **validator wiring + acceptance + env policy** as mandatory exit criteria — otherwise risk **partial enablement**.

---

## 9. Boundary check — out of scope for BE-S1

- **FE narrative presentation** → **FE-S2**
- **Launch integration** → **FE-LAUNCH-INTEGRATION**
- **OPS/compliance** → **OPS-S1** (blocked on market/compliance inputs per roadmap §770)
- **Moving reasoning into Layer C**
- **Unguided narrative from raw biomarkers** (legacy path already disabled in production)
- **Speculative lifestyle/medication coaching** beyond governed structured outputs and existing deterministic caveats

---

## 10. Recommendation (summary table)

| Question | Answer |
|----------|--------|
| Proceed now? | **Yes — backend narrative enablement is justified** if scoped as **governed activation** of existing synthesis, not new reasoning. |
| One sprint vs split? | **SPLIT_INTO_CONTRACT_AND_RUNTIME_NARRATIVE_PHASES** (validator/prompt/acceptance vs prod policy/CI/operator docs). |
| First output surface | **`insights[]` from InsightSynthesizer**; keep clinician report deterministic unless a separate contract sprint authorises LLM there. |

---

**Document status:** Complete (read-only).  
**Next step:** Author **BE-S1** implementation prompt(s) from this file — **not** done in this preflight.
