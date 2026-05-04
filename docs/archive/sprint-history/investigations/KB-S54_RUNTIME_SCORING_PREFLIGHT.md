# KB-S54 Preflight — Cluster Runtime Wiring + System-Level Scoring Completion

**work_id:** `KB-S54-PREFLIGHT`  
**Mode:** READ-ONLY investigation (no implementation).  
**Date:** 2026-04-04  

---

## 1. Executive summary

| Question | Answer |
|----------|--------|
| **Is KB-S54 justified now?** | **Yes** — at least one **verified** runtime coherence gap exists on the **AB acceptance harness** (reproducible local run). |
| **Named verified gap(s)** | **G1 — System burden key fragmentation:** `insight_graph.raw_system_burden_vector` (and related vectors) mixes **canonical** system IDs (`cardiovascular`, `renal`, …) with **cluster-suffixed** bucket IDs (`cardiovascular_4_biomarkers`, `renal_2_biomarkers`, …). Propagation/validation operate on this **combined** namespace, while the **exported** `meta["burden_vector"]` artifact **filters** to canonical keys and pushes cluster buckets to `derived_components`. |
| **Should the sprint proceed?** | **Yes**, if authored to close **G1** (and optionally **G2** below) with explicit acceptance criteria on AB/VR harness runs — not as a vague “improve scoring” effort. |

**Final recommendation (see §6):** **`PROCEED_AS_PURE_RUNTIME_COMPLETION`** — scoped to orchestrator/burden wiring and contract clarity; **no** SSOT/signal-package change required for the verified gap unless the chosen fix deliberately rolls burden up using registry semantics (still runtime-side).

---

## 2. Strategy interpretation (v1.5 adopted plan)

**Source:** `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` (Wave 3 — KB-S54 lineage).

KB-S54 is defined as:

- **Purpose:** Complete **trustworthy runtime / system-level output behaviour** (not “prove clustering exists”).
- **Strategic note:** Emphasis shifts to **coherence, correctness, and trusted semantics** of system-level interpretation.
- **Preflight gate:** Read `cluster_engine_v2.py`, `system_burden_engine.py`, `scoring_policy_registry.py`; identify **specific** coherence/correctness gaps vs **AB and VR** acceptance panels; **if no named gap → no-op sprint.**

**Capability KB-S54 is meant to unlock (interpretation):**

- After KB-S53 (AB/VR formalised acceptance floors), Wave 3 expects **structured outputs that do not contradict themselves** at the **system / burden / cluster** layer when read alongside signals and reports.
- KB-S54 is **backend runtime coherence**, not FE, not ingestion batching, and not (by itself) primary-concern **philosophy**.

---

## 3. Runtime / scoring file assessment (mandatory files)

### 3.1 `backend/core/clustering/cluster_engine_v2.py`

| Aspect | Assessment |
|--------|------------|
| **Role** | Two subsystems in one module: (A) legacy **`score_clusters()`** — flag/derived-based deterministic cluster DTOs + YAML rules; (B) **`ClusterEngineV2`** — **runtime** engine: groups biomarkers by **cluster schema**, severity from **numeric biomarker scores** from the scoring engine. |
| **Runtime** | **`ClusterEngineV2` is active:** imported and instantiated in `AnalysisOrchestrator` (`backend/core/pipeline/orchestrator.py`); `cluster_biomarkers()` calls `clustering_engine.cluster_biomarkers(context, scoring_result)`. |
| **Legacy / partial** | **`score_clusters()` is not orchestrator-wired.** Module docstring still states “Sprint 16: Engine-only implementation (not wired to runtime)” for that path; **tests** (`test_cluster_engine_v2.py`) and **`smoke_cluster_engine_v2.py`** exercise it. This is **parallel surface area**, not driving AB/VR pipeline output. |

**Verdict:** **Active (class `ClusterEngineV2`) + stale/parallel (`score_clusters`)** in the same file.

### 3.2 `backend/core/analytics/system_burden_engine.py`

| Aspect | Assessment |
|--------|------------|
| **Role** | Loads `backend/ssot/system_burden_registry.yaml`; audits risk directions; **`build_raw_system_burden_v1`** sums **direction-aware** weighted z-style components per **caller-supplied** system bucket key. |
| **Runtime** | **Active:** orchestrator Step 4.73 calls `load_burden_registry`, `audit_*`, `build_raw_system_burden_v1`, then propagation/capacity/validation. |
| **Partial / TODO** | `CALIBRATION_FACTOR = 1.0` with TODO for tier-aware calibration — **design debt**, not shown as AB/VR failure in this preflight. |

**Verdict:** **Active**; correctness of **inputs** (system key namespace) is orchestrator-owned, not this module’s.

### 3.3 `backend/core/analytics/scoring_policy_registry.py`

| Aspect | Assessment |
|--------|------------|
| **Role** | Loads and validates `backend/ssot/scoring_policy.yaml`; exposes **version/hash stamp** for replay manifests. |
| **Runtime** | **Active:** `ScoringRules` / `core/scoring/rules.py` uses `load_scoring_policy()`; orchestrator stamps replay manifest with policy version/hash. |
| **Bypassed** | **No** — policy load is on the hot path for scoring rules construction. |

**Verdict:** **Active** (loader/validator/stamp). KB-S54 does **not** require changing this file **unless** the sprint explicitly extends policy schema (out of scope for the **verified** G1 gap).

---

## 4. AB/VR gap analysis (evidence-bound)

### 4.1 Harness context

- **Authoritative AB/VR fixtures:** `panel_acceptance_profiles_v1.yaml` → `ab_full_panel_with_ranges.json`, `vr_full_panel_with_ranges.json` (KB-S53).
- **Investigation doc:** `KB-S53_AB_VR_ACCEPTANCE_HARNESS.md` (harness intent: deterministic regression floors — does not assert burden semantics).

### 4.2 G1 — Verified: fragmented system burden namespace on `InsightGraph`

**Behaviour:** For a normal AB acceptance run, clustering produces clusters whose `cluster_id` values follow `ClusterEngineV2`’s pattern `{system_name}_{count}_biomarkers` (e.g. `cardiovascular_4_biomarkers`). The orchestrator builds `system_to_biomarkers` using **`cluster_id` as the map key** (`_system_biomarker_map`). Burden is then computed **per key**. **Canonical** system IDs still appear for biomarkers routed via the “not covered by cluster membership” path (registry `system` field).

**Evidence (reproduced 2026-04-04, local):**

- `insight_graph.json` from `run_golden_panel` on `ab_full_panel_with_ranges.json` reported **3** clusters (`cardiovascular_4_biomarkers`, `hematological_4_biomarkers`, `renal_2_biomarkers`).
- **`insight_graph.raw_system_burden_vector`** contained **12 keys**: canonical systems **plus** the three `*_biomarkers` suffix keys (e.g. `cardiovascular` **and** `cardiovascular_4_biomarkers`).
- **`burden_vector.json`** (artifact) **`raw_system_burden_vector`** contained **only 9 canonical** keys; non-canonical keys appeared under **`derived_components`**.

**Owning components:**

- Key choice for burden grouping: `AnalysisOrchestrator._system_biomarker_map` (`orchestrator.py` ~760–776).
- Split for export: `AnalysisOrchestrator.run` meta assembly (`orchestrator.py` ~1884–1911) — comment states base vectors should be canonical-only; **`insight_graph` assignment** (~1486–1490) still holds the **pre-split** combined namespace.

**Classification:** **Verified coherence / trusted-semantics gap** — a consumer reading **`insight_graph` alone** sees **duplicate system semantics** (canonical row vs cluster-scoped row for related biomarker sets). The artifact writer partially mitigates for **replay JSON**, but **Layer C / LLM / any code using `insight_graph` vectors** does not get the same shape as `burden_vector.json`.

### 4.3 G2 — Verified: dual cluster scoring models in one module (documentation / drift)

**Behaviour:** `score_clusters()` implements a **different** scoring model (flags + `cluster_rules.yaml`) than **`ClusterEngineV2`** (schema + numeric scores). Only the latter feeds the orchestrator.

**Classification:** **Verified structural drift**, not an AB/VR functional bug by itself. KB-S54 **may** include bounded cleanup (deprecate/rename/document) to reduce false confidence that “cluster score” in tests equals runtime clusters.

### 4.4 Suspicions not elevated to verified gaps (this preflight)

- **Calibration TODO** in `system_burden_engine.py` — no AB/VR contradiction demonstrated here.
- **Primary concern / `top_findings` ordering** (e.g. `signal_id` tie-break) — **explicitly ranking-policy / reporting philosophy**, not KB-S54 per strategy boundary; see `VR_PRIMARY_CONCERN_RANKING_INVESTIGATION.md`.

---

## 5. Current scoring / coherence surface map (AB/VR path)

**Abbreviated trace (signal → report):**

1. **Scoring:** `ScoringEngine` + `ScoringRules` (`scoring_policy.yaml` via `scoring_policy_registry` / `rules.py`) → `health_system_scores` / per-biomarker scores in orchestrator.
2. **Clustering:** `ClusterEngineV2.cluster_biomarkers` → cluster list → `build_insight_graph_v1` embeds **`cluster_summary.clusters`** with `cluster_id` as above (`insight_graph_builder.py` ~342–361).
3. **Signals / report_v1:** `compile_report_v1` in `insight_graph_builder.py` — **does not** consume burden vectors for ranking (grep: no `burden`/`cluster` in `report_compiler_v1.py` for this path).
4. **System burden:** Orchestrator Step 4.73: registry-backed **bio stats** + **`build_raw_system_burden_v1`** → **propagate** → **capacity** → **validation** → fields on **`InsightGraphV1`**; explainability report rebuilt with burden stamps.
5. **Export split:** `meta["burden_vector"]` canonicalises + `derived_components` for non-canonical keys (`orchestrator.py` ~1884–1911).

**Policy application:** Biomarker scoring — **active** via SSOT policy. **Cluster severity** — **active** via cluster schema + score thresholds. **Burden** — **active** but **fed with mixed bucket keys** (G1).

---

## 6. Scope boundary

| In KB-S54 | Out of KB-S54 |
|-----------|----------------|
| Unifying or explicitly contracting **system burden bucket IDs** vs **cluster IDs**; making **`insight_graph` burden vectors** align with **replay-safe canonical semantics** (or documenting a single authoritative consumer rule). | **Ranking policy** (“which signal is primary concern”), `compile_report_v1` tie-break philosophy. |
| Optional: **retire or fence** `score_clusters()` vs `ClusterEngineV2` naming/docs to remove false dual-runtime impression. | **KB-S58** phenotype/fixture expansion; broad SSOT ingestion. |
| Orchestrator + (if needed) **contract/tests** for burden shape; possibly **`insight_graph_v1` field documentation**. | **FE** surfaces; **root-cause hypothesis asset** content changes. |
| Regression: **AB/VR harness** `run_golden_panel` / existing golden tests still **PASS**; add **targeted assertions** on burden key policy if sprint defines one. | General unfocused bugfixing without a named gap. |

**Structural integrity:** The **verified** G1 gap can likely be closed **without** changing signal packages, root-cause YAML content, or FE — **unless** the chosen design requires new SSOT fields (not necessary for “rollup to canonical system IDs only” at orchestrator level).

---

## 7. Recommendation

### **PROCEED_AS_PURE_RUNTIME_COMPLETION**

**Named gap(s) to close in sprint authoring:**

1. **G1 (required):** **System burden / cluster bucket coherence** — eliminate or formally unify the **canonical vs `{system}_{n}_biomarkers`**** dual namespace** on **`insight_graph` burden fields** (and any downstream consumer assumptions), consistent with the stated intent in `orchestrator.py` that **base system vectors are canonical**.

**Likely touched files (indicative, not prescriptive):**

- `backend/core/pipeline/orchestrator.py` (`_system_biomarker_map`, Step 4.73 assembly, `insight_graph` mutation vs `meta["burden_vector"]`).
- Possibly `backend/core/contracts/insight_graph_v1.py` (field descriptions / optional structured sub-object for cluster-scoped diagnostics).
- Tests: `backend/tests/unit/test_golden_panel_runner.py` or new unit tests asserting **burden key policy** on AB (and VR) acceptance fixtures.

**Optional (bounded):**

2. **G2:** Documentation or deprecation path for **`score_clusters()`** vs **`ClusterEngineV2`** in `cluster_engine_v2.py` + smoke script alignment.

**Sprint shape:** **PURE_RUNTIME_COMPLETION** — no bounded external prerequisite identified **beyond** defining the **exact burden key contract** in the sprint prompt (product/engineering decision: rollup-only vs explicit dual fields with documented merge rule).

---

## 8. References (repo)

- Strategy: `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` (KB-S54 lineage ~641–645).
- AB/VR harness: `docs/investigations/KB-S53_AB_VR_ACCEPTANCE_HARNESS.md`, `backend/tests/fixtures/panels/panel_acceptance_profiles_v1.yaml`.
- Orchestrator burden split: `backend/core/pipeline/orchestrator.py` ~760–776, ~1288–1510, ~1884–1911.
- Cluster runtime: `backend/core/clustering/cluster_engine_v2.py` (`ClusterEngineV2._build_clusters` cluster_id pattern ~328–329).
- Ranking (out of scope for KB-S54): `docs/investigations/VR_PRIMARY_CONCERN_RANKING_INVESTIGATION.md`.
