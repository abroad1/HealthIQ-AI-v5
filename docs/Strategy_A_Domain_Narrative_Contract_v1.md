# Strategy A — Domain narrative contract (first-wave domains)

**Status:** Repo-grounded specification (research only).  
**Depends on:** `docs/Strategy_A_Launch_Domains_Implementation_Blueprint.md` (factual base).  
**Scope:** Three launch-first domains only — Cardiovascular health, Blood sugar control, Liver health.  
**Out of scope:** Thyroid, kidney, blood/iron/oxygen, silent inflammation, hormone balance; code changes.

**Architecture rule (non-negotiable):** Consumer dashboard copy is a **deterministic translation layer** assembled from existing engine outputs and governed assets. It does **not** replace clinical handout labels (`clinician_report_v1` / clinician PDF pipeline) or internal phenotype/system authority. **Consumer labels must not appear in the clinical layer.**

---

## Shared definitions

### Domain → engine anchors (deterministic)

| Domain (consumer) | Clinical label (handout / strategy doc) | Primary scoring system key (`scoring_policy.yaml` `systems`) | ClusterEngineV2 cluster id prefix (`clusters.yaml` → `cluster_id`) | Burden / capacity system id (`system_burden_registry.yaml` → `system`) |
|-------------------|----------------------------------------|---------------------------------------------------------------|----------------------------------------------------------------------|--------------------------------------------------------------------------|
| Cardiovascular health | Cardiometabolic / Vascular Risk Status | `cardiovascular` | `cardiovascular` | `cardiovascular` |
| Blood sugar control | Glycaemic Regulation / Insulin Resistance Status | `metabolic` | `metabolic` | `metabolic` |
| Liver health | Hepatic-Metabolic Strain Status | `liver` | `hepatic` | **`hepatic`** (not `liver`) |

**Important:** Scoring uses the key `liver` (ALT/AST only); burden/capacity use **`hepatic`** for the same biology in SSOT. Any narrative that references “capacity headroom” for liver must read `system_capacity_scores["hepatic"]` when present, not `liver`.

### Interpretation Display Layer (IDL) phenotype rows used per domain

Governed static copy and dynamic severity live in `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml`. Publisher: `backend/core/analytics/interpretation_display_layer_publish_v1.py`. Contract: `backend/core/contracts/interpretation_display_layer_v1.py`.

| Domain | IDL `internal_id` values | Notes |
|--------|--------------------------|--------|
| Cardiovascular | `ph_vascular_hcy_inflammation_v1`, `ph_lipid_residual_ldl_favourable_transport_v1` | Vascular/homocysteine–inflammation and LDL-in-context patterns. |
| Blood sugar | `ph_metabolic_early_ir_v1`, `ph_hba1c_metabolic_stress_v1` | IR phenotype + HbA1c stress state. |
| Liver | `ph_hepatic_alt_inflammatory_v1` | Hepatic / liver stress pattern. |

**Cross-domain honesty:** `ph_metabolic_early_ir_v1` is metabolically led but involves lipid signals; it may be relevant to **both** Blood sugar and Cardiovascular cards. The contract should **either** attach it to a single primary domain via explicit SSOT mapping (recommended follow-up) **or** allow both cards to reference the **same** IDL row without inventing second interpretations (duplicate reference, not duplicate logic).

### Cluster and scoring signals on the wire

- **Clusters:** `AnalysisDTO.clusters` → `ClusterHit`: `cluster_id` (e.g. `cardiovascular_4_biomarkers`), `severity`, `confidence`, `biomarkers`, `description`. Built by `ClusterEngineV2` from **scored** biomarkers only (`backend/core/clustering/cluster_engine_v2.py`).
- **Per-marker scores:** `AnalysisDTO.biomarkers` → `BiomarkerScore` (`backend/core/models/results.py`): `biomarker_name`, `score` (normalised 0–1 in this model), `status`, `reference_range`, `interpretation`, optional explainers.
- **System-level scoring confidence:** `ScoringEngine` uses `ConfidenceLevel` = `high` | `medium` | `low` (`backend/core/scoring/engine.py`). **Not** exposed as first-class fields on `AnalysisDTO`; infer from cluster confidence, marker coverage, and unscored reasons, or add a contract field (see §Summary C).
- **Capacity / burden:** `AnalysisDTO.system_capacity_scores`, `meta.burden_vector` (canonical vectors + `derived_components`), `insight_graph` dump in `meta.insight_graph` (`orchestrator.py` assembly).
- **Narrative (global, not domain-scoped):** `AnalysisDTO.narrative_report_v1` → `NarrativeReportV1` (`backend/core/contracts/narrative_report_v1.py`): includes `retail_summary`, `next_steps_narrative`, `longitudinal_narrative`, `clinician_synthesis`, etc. Compiled in `narrative_report_compiler_v1.py`. **Retail summary** today only pulls IDL rows with `frontend_allowed_term == phenotype_allowed` and non–`not_observed` severity — so it is **not** a substitute for domain cards. **Next steps** are gated on benchmark lead/secondary signal sets (homocysteine/MCV vs lipid hints) and functional YAML — **not** aligned to the three product domains by default.

### IDL dynamic fields (for narrative)

For each record, the publisher fills at minimum:

- `severity_state`: `not_observed` | `watch` | `attention` | `strong_signal`
- `supporting_biomarkers_summary`: short deterministic list from fired required signals’ metrics

Static governed fields usable verbatim in consumer copy (retail lane): `retail_display_label`, `subtitle`, `why_it_matters`. **Do not** surface `clinical_display_label` on the consumer dashboard; reserve it for clinician-facing artifacts.

### Frontend pattern section behaviour (reference)

`frontend/app/components/results/InterpretationPatternsSection.tsx` renders IDL rows where `enabled_for_frontend === true` (publisher sets false when severity is `not_observed`). It does **not** filter by `frontend_allowed_term`; that filter applies only to `narrative_report_v1.retail_summary` in the compiler.

---

## 1. Cardiovascular health

### 1.1 Consumer label

Cardiovascular health

### 1.2 Clinical label

Cardiometabolic / Vascular Risk Status (strategy document; clinician handout — not for dashboard primary title).

### 1.3 Narrative components (UX slots)

| Component | Purpose | Example shape (illustrative; final wording via templates + governed text) |
|-----------|---------|-----------------------------------------------------------------------------|
| **Headline sentence** | Calm band summary for the domain | e.g. “This area looks broadly stable on your lipids” / “This area shows strain in your lipid pattern” |
| **Why this score** | One sentence on main contributors | e.g. “Mainly driven by your LDL, HDL, and triglyceride pattern versus your lab ranges.” |
| **Confidence sentence** | Why the model trusts the read | e.g. “Confidence is high because several lipid markers were scored with lab reference ranges.” |
| **What this may mean over time** | Non-diagnostic, persistence framing | Prefer **governed** `why_it_matters` from relevant IDL rows, or neutral cardiometabolic framing aligned to those strings. |
| **What to do next** | Single actionable line | Prefer closing guidance implied by IDL `why_it_matters` (“review”, “lifestyle action”) **or** category-matched `insights[].recommendations` **or** neutral clinician discussion line — no new prescriptive medical instructions. |

### 1.4 Source-of-truth mapping (per component)

| Component | Direct sources today | Assemble deterministically from | New contract work |
|-----------|---------------------|----------------------------------|-------------------|
| **Headline** | — | `clusters` entry whose `cluster_id` starts with `cardiovascular_` → map `severity` (`normal` / `mild` / `moderate` / `high` / `critical`) to a fixed headline template **or** derive band from mean of member biomarker `score` in `AnalysisDTO.biomarkers` for `cluster.biomarkers`. | Optional: precomputed domain band enum on DTO. |
| **Why this score** | `ClusterHit.biomarkers`, `ClusterHit.description` | Names of scored markers in cluster; optionally worst N contributors by distance from mid-range using `biomarkers[].status` / `score`. | Optional: explicit `contributor_reason_codes[]` from backend. |
| **Confidence** | `ClusterHit.confidence` (0–1) | Count of cardiovascular cluster members present vs `scoring_policy` `cardiovascular.min_biomarkers_required` (3); presence of `unscored_reason` / missing lab range on lipid markers if exposed on biomarker rows. | Expose `health_system_scores.cardiovascular.confidence` (`high`/`medium`/`low`) on API for fidelity to `ScoringEngine`. |
| **Over time** | IDL `why_it_matters` for `ph_vascular_hcy_inflammation_v1`, `ph_lipid_residual_ldl_favourable_transport_v1` when `severity_state !== not_observed` | `narrative_report_v1.longitudinal_narrative` only if marker-level transitions concern lipids (not domain-scoped). | Domain-tagged longitudinal snippets. |
| **Next step** | IDL `why_it_matters` (last clause often action-oriented) | `insights[]` where `category === "cardiovascular"` (e.g. heart insight); `narrative_report_v1.next_steps_narrative` is **global** — use only if product explicitly accepts benchmark-gated text. | Per-domain `next_step_governed_line` in SSOT or DTO. |

### 1.5 Confidence logic inputs (repo-evidence)

- **Coverage:** At least `scoring_policy` cardiovascular `min_biomarkers_required` (3) **scored** lipid markers; cluster appears only if `ClusterEngineV2` policy `min_members_per_cluster` satisfied.
- **Supporting context:** Extended markers (e.g. homocysteine, ApoB) may appear in **burden** (`system_burden_registry`) but are **not** on the cardiovascular **scoring** list — treat as **context** or “extended panel” in confidence copy, not as part of the core 0–100 lipid rail unless policy is extended.
- **IDL / phenotype:** Fired signals for `ph_vascular_hcy_inflammation_v1` imply **additional** interpretive context (homocysteine/inflammation); `severity_state` informs strength of pattern language **without** replacing lipid cluster severity.
- **Coherence:** Conflicting cluster vs IDL states should be resolved by precedence rules (documented): e.g. cluster severity for headline, IDL for pattern subtitle.

### 1.6 Safe claims only (today)

- Lipid-focused summaries relative to **lab reference ranges** and scored markers.
- When IDL rows are enabled, reuse **retail** `subtitle` / `why_it_matters` / `supporting_biomarkers_summary` — no new disease claims.
- Do **not** claim “full cardiovascular risk” or imaging/blood-pressure findings not in the panel.
- Do **not** merge CRP into the lipid **score** without a governed merge rule; CRP remains a separate **inflammatory** scoring system in `scoring_policy`.

### 1.7 Gaps (biology present, contract thin)

- No first-class **domain DTO**; FE must derive domain story from `clusters` + `biomarkers` + IDL + optional burden.
- Homocysteine / ApoB / Lp(a) biology in burden **not** reflected in cardiovascular **scoring** list — narrative must say what was **not** in the score if those markers matter to the user story.

---

## 2. Blood sugar control

### 2.1 Consumer label

Blood sugar control

### 2.2 Clinical label

Glycaemic Regulation / Insulin Resistance Status

### 2.3 Narrative components

| Component | Example shape |
|-----------|----------------|
| **Headline** | e.g. “Blood sugar markers look broadly stable” / “This area shows glycaemic strain” |
| **Why this score** | e.g. “Driven mainly by glucose and HbA1c versus your lab ranges.” |
| **Confidence** | e.g. “Confidence is moderate because insulin was not on the panel.” (only if true) |
| **Over time** | Prefer IDL `why_it_matters` for `ph_metabolic_early_ir_v1` / `ph_hba1c_metabolic_stress_v1`. |
| **Next step** | Governed IDL / neutral clinician follow-up; optional `insights[]` for metabolic category if present. |

### 2.4 Source-of-truth mapping

| Component | Direct | Assemble | New work |
|-----------|--------|----------|----------|
| **Headline** | — | `cluster_id` prefix `metabolic_` → `severity`; same band mapping as §1. | Optional domain band on DTO. |
| **Why this score** | `ClusterHit.biomarkers` for metabolic cluster | Glucose, HbA1c, insulin from biomarker list; flag insulin missing via absence in `biomarkers` / cluster membership. | Explicit `missing_for_domain[]`. |
| **Confidence** | `ClusterHit.confidence` | vs `metabolic.min_biomarkers_required` (2) + optional insulin “nice-to-have” flag from policy table. | Expose system-level scoring confidence for `metabolic`. |
| **Over time** | IDL `why_it_matters` (both internal_ids) | `lifestyle` bridges in `meta` (`fasting_dietary_glycaemic`) may append context in **global** narrative compiler — domain card should not duplicate unless mapped. | Domain-specific bridge slot. |
| **Next step** | IDL strings; `insights[].recommendations` if metabolic | Same caveats as §1 for `next_steps_narrative`. | Per-domain governed next-step line. |

### 2.5 Confidence logic inputs

- **Coverage:** `metabolic.min_biomarkers_required` = 2 (`glucose`, `hba1c`, `insulin` list — insulin optional for cluster membership but strengthens interpretability).
- **Phenotype:** `ph_metabolic_early_ir_v1` / `ph_hba1c_metabolic_stress_v1` severity states strengthen “pattern” language; `ph_metabolic_early_ir_v1` is `phenotype_allowed` in IDL — usable in retail-adjacent summaries per policy.
- **Cross-rail:** Triglycerides/HDL may support IR narrative via **cardiovascular** cluster and phenotype map; if referenced, label them as **related lipid signals**, not as separate diagnoses.

### 2.6 Safe claims only

- Glycaemic / insulin-resistance **pattern** language grounded in scored glucose/HbA1c (and insulin when present) plus governed IDL.
- Do not imply continuous glucose monitoring or medication titration advice.

### 2.7 Gaps

- `narrative_report_v1.retail_summary` may omit `ph_hba1c_metabolic_stress_v1` (clinical_only) even when clinically important — domain card should still use IDL row fields under governed FE rules, consistent with `InterpretationPatternsSection` (which shows enabled records regardless of `frontend_allowed_term`).

---

## 3. Liver health

### 3.1 Consumer label

Liver health

### 3.2 Clinical label

Hepatic-Metabolic Strain Status

### 3.3 Narrative components

| Component | Example shape |
|-----------|----------------|
| **Headline** | e.g. “Liver enzyme markers look broadly stable” / “This area shows enzyme elevation versus your ranges” |
| **Why this score** | e.g. “Based on ALT and AST versus your lab reference ranges.” |
| **Confidence** | e.g. “Confidence is limited because other liver markers on your report were not included in this score.” (when GGT/ALP present but unscored on rail) |
| **Over time** | IDL `why_it_matters` for `ph_hepatic_alt_inflammatory_v1` when active; otherwise neutral strain framing **without** fibrosis/MASLD diagnostic labels unless from governed text. |
| **Next step** | IDL `why_it_matters` / neutral clinician discussion. |

### 3.4 Source-of-truth mapping

| Component | Direct | Assemble | New work |
|-----------|--------|----------|----------|
| **Headline** | — | `cluster_id` prefix `hepatic_` + `severity` **or** biomarker-level ALT/AST statuses. | Domain band enum. |
| **Why this score** | Cluster members (ALT, AST) | Explicitly name only markers on **scoring** rail unless product extends policy. | List `extended_hepatic_markers_present` from panel normalisation for honesty. |
| **Confidence** | `ClusterHit.confidence`; `system_capacity_scores["hepatic"]` if key present | Compare panel presence of `ggt`, `alp`, etc. from `biomarkers` / burden against scoring inclusion. | Single `domain_confidence_caveat` string from backend rules. |
| **Over time** | IDL for `ph_hepatic_alt_inflammatory_v1` | `ph_hba1c_metabolic_stress_v1` touches hepatic pathways internally — only mention if IDL enabled and product maps that row to liver card (otherwise omit to avoid scope creep). | SSOT map: phenotype → primary domain. |
| **Next step** | IDL; insights with hepatic/liver category if any | — | Governed liver next-step asset. |

### 3.5 Confidence logic inputs

- **Coverage:** `liver` scoring system `min_biomarkers_required` = 1; cluster `hepatic` requires ALT + importance of AST in `clusters.yaml`.
- **Extended markers:** Burden registry lists `ggt`, `alp`, `bilirubin`, `albumin` under **`hepatic`** — if measured but not on scoring rail, confidence copy should acknowledge **partial view**.
- **Capacity:** `system_capacity_scores["hepatic"]` can support “headroom” language **if** product copy is approved to mirror `balanced_systems_presentation_v1`-style evidence (today used in clinician-oriented assembly via `compile_balanced_systems_v1`, not as domain cards).

### 3.6 Safe claims only

- Enzyme-centric framing (ALT/AST) for the **numeric** domain score; broader “liver health” only when IDL/burden context is explicitly included and labelled as additional context.
- Reuse IDL retail strings when the row is enabled; no new pathology names.

### 3.7 Gaps

- **Semantic gap:** User says “liver”; engine scoring key is `liver`; clusters/burden use `hepatic` — narrative contract must **normalize** this in documentation and DTO keys to avoid wrong capacity lookup.
- GGT and other hepatic markers **not** in `scoring_policy` `liver` biomarker list — largest honesty gap for launch copy.

---

## Summary

### A. Proposed shared narrative assembly template (all three domains)

Deterministic order for the expanded card:

1. **Score band statement (headline)** — from `ClusterHit.severity` for the domain’s cluster prefix, with explicit **no-cluster** / **insufficient members** branch (panel too thin).
2. **Contributor sentence** — from cluster biomarker membership + top deviations from `AnalysisDTO.biomarkers` (or future `contributor_reason_codes`).
3. **Confidence sentence** — from `ClusterHit.confidence`, scoring min-threshold coverage, optional extended-marker caveat lists, and (if exposed) system-level `ConfidenceLevel`.
4. **Consequence sentence (over time)** — prefer **verbatim** `InterpretationDisplayRecordV1.why_it_matters` for domain-mapped IDL rows with `severity_state !== not_observed`; otherwise omit or use neutral governed fallback from SSOT (not free text).
5. **Next-step sentence** — prefer IDL closing guidance, then category-matched `insights[].recommendations`, then neutral “discuss with your clinician” boilerplate from product/legal.

### B. Domain-specific deviations

| Domain | Special handling |
|--------|------------------|
| **Cardiovascular** | Do not silently fold **CRP** into the lipid domain score; optional **second sentence** referencing inflammatory IDL/`inflammatory` cluster only with explicit “separate system” wording. Homocysteine-aware copy only when `ph_vascular_hcy_inflammation_v1` is active. |
| **Blood sugar** | `ph_metabolic_early_ir_v1` may overlap cardiovascular narrative — enforce **one primary domain** per IDL row in SSOT or accept duplicate reference with identical text. Insulin absence is a standard confidence downgrade. |
| **Liver** | **Always** disambiguate `liver` (scoring) vs `hepatic` (burden/capacity). Headline must not imply full hepatic workup if only ALT/AST scored. |

### C. Contract implications (DTO / backend)

Concise list for work packages:

1. **`customer_domain_scores_v1` (or equivalent)** on `AnalysisDTO` / `build_analysis_result_dto` output: per domain `{ domain_id, band, score_0_100?, confidence_tier, headline_key, contributor_codes[], idl_internal_ids[], caveats[] }` — all **deterministic**, no LLM.
2. **Expose or duplicate `health_system_scores[*].confidence` and `missing_biomarkers`** from `ScoringEngine` on the API payload (today not on `AnalysisDTO`).
3. **`future_commercial_domain` (optional)** in `idl_records_v1.yaml` rows to bind IDL → domain without hardcoding in FE (field exists on `InterpretationDisplayRecordV1` but is not populated in current YAML).
4. **SSOT mapping file:** `internal_id` → primary `domain_id` (+ optional secondary) to resolve `ph_metabolic_early_ir_v1` overlap.
5. **Per-domain `next_step_governed`** optional strings in `knowledge_bus` if IDL `why_it_matters` is insufficient for a single action line.

### D. Implementation readiness (narrative only)

| Domain | Classification | Rationale |
|--------|----------------|-----------|
| **Cardiovascular health** | **Narrative-ready with light assembly** | Cluster + biomarkers + IDL + burden context sufficient; headline/band mapping and CRP/homocysteine honesty rules are the main work. |
| **Blood sugar control** | **Narrative-ready with light assembly** | Strongest rail; insulin-missing confidence and IR/lipid cross-reference discipline. |
| **Liver health** | **Narrative-ready with light assembly** (honesty-heavy) | Numeric story is narrow; requires explicit caveats for unscored hepatic markers and `liver` vs `hepatic` naming in implementation — **or** **narrative-ready only after contract cleanup** if marketing insists on “full liver health” without those caveats. |

---

*This document is intentionally limited to narrative contracts for the first three Strategy A domains. Analytical behaviour is defined by existing engine and SSOT; this spec only binds how consumer-facing text may be filled from those outputs.*
