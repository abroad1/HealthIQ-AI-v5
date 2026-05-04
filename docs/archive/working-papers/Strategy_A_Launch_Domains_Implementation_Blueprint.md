# Strategy A — Launch Domains Implementation Blueprint

Repo-grounded implementation research for HealthIQ AI (HealthIQ-AI-v5).  
Source context: `User Health to Systems Map_v4.md` (customer-facing score model) and current codebase.

**Scope:** Six launch-core domains only. Silent inflammation and hormone balance remain second-wave unless explicitly promoted with repo evidence.

---

## 1. Cardiovascular health

**Consumer label:** Cardiovascular health  
**Clinical label (Strategy A doc):** Cardiometabolic / Vascular Risk Status  

### Internal engine mapping

- **Scoring (0–100 rail):** `cardiovascular` system in `backend/ssot/scoring_policy.yaml` — lipids + `tc_hdl_ratio`; weighted in overall score.
- **Clusters (runtime):** `cardiovascular` membership in `backend/ssot/clusters.yaml` (lipid core).
- **Burden SSOT:** Many markers mapped to `cardiovascular` (e.g. `homocysteine`, `lipoprotein_a`, `apob`, ratios) in `backend/ssot/system_burden_registry.yaml`.
- **Governed phenotypes / IDL:** `ph_vascular_hcy_inflammation_v1`, `ph_lipid_residual_ldl_favourable_transport_v1` in `knowledge_bus/phenotypes/phenotype_map_v1.yaml` and matching rows in `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml` (vascular / LDL-in-context patterns).
- **Cross-domain:** `ph_metabolic_early_ir_v1` and `ph_thyroid_lipid_disturbance_v1` also touch `cardiovascular` in the phenotype map — many-to-many is real in-repo.
- **Insight module:** `backend/core/insights/modules/heart_insight.py` documents ratio-based CV framing (execution depends on `insight_graph` / layer C features).

### Current codebase support

- **Strong:** Deterministic lipid system score + cluster + burden alignment for core lipids; multiple governed phenotype + IDL constructs for vascular / lipid nuance.
- **Partial:** “Vascular inflammation” and homocysteine are supported as **phenotype/signal/IDL** paths, not as a single merged numeric “cardiovascular” bucket in `scoring_policy` (CRP is a separate **inflammatory** scoring system; homocysteine is in burden registry as cardiovascular but **not** in the cardiovascular scoring biomarker list).
- **Confidence:** `ScoringEngine` exposes per-system `ConfidenceLevel` from scored biomarkers + `min_biomarkers_required`; biomarkers without lab ranges stay unscored per `ScoringRules` contract.

### Missing / weak for launch

- No **single product DTO** that rolls lipids + optional CRP/homocysteine context into one “Cardiovascular health” score with governed weights.
- Extended markers (ApoB, Lp(a), homocysteine) are in **burden** but not in the **cardiovascular scoring system** list — a domain score either ignores them on the 0–100 rail or must pull from burden / signals explicitly.

### Launch readiness rating

**Launchable with light assembly** — compose from existing `health_system_scores.cardiovascular`, optionally blend or gate with `inflammatory` for narrative only (careful double-counting), and surface IDL/phenotype rows when fired.

### Implementation notes

- **Truthful expanded card today:** “Based on your lipids (and ratios) relative to your lab’s reference ranges…”; if IDL shows vascular/homocysteine or LDL-in-context patterns, use **governed** `clinical_display_label` / `retail_display_label` from IDL, not new copy.
- **Likely code paths:** `backend/core/scoring/engine.py`, `backend/ssot/scoring_policy.yaml` (only if extending biomarkers on the rail), `backend/core/pipeline/orchestrator.py` (`score_biomarkers` / result assembly), `backend/core/dto/builders.py`, `publish_interpretation_display_layer_v1` + `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml`, `frontend` results/types.

---

## 2. Blood sugar control

**Consumer label:** Blood sugar control  
**Clinical label:** Glycaemic Regulation / Insulin Resistance Status  

### Internal engine mapping

- **Scoring:** `metabolic` system — `glucose`, `hba1c`, `insulin` in `scoring_policy.yaml`.
- **Clusters:** `metabolic` in `clusters.yaml`.
- **Phenotypes:** `ph_metabolic_early_ir_v1`, `ph_hba1c_metabolic_stress_v1` (and edges into hepatic signals in the map).
- **IDL:** First-class records with retail/clinical labels for insulin resistance and “blood sugar stress” (`idl_records_v1.yaml`).

### Current codebase support

- **Strong:** End-to-end numeric scoring, clustering, governed phenotypes, IDL cards, interaction-map signals for `signal_hba1c_high`, etc.

### Missing / weak

- Domain score is still **assembly**: product must map “Blood sugar control” → `metabolic` **plus** optional phenotype severity from IDL (not duplicated as a second score without rules).
- Triglyceride/HDL coupling for IR lives partly under **cardiovascular** scoring and **ph_metabolic_early_ir** — consumer domain should acknowledge contributors from those rails when present (many-to-many).

### Launch readiness rating

**Launch-ready now** (with a thin translation layer), or **light assembly** if you require one canonical 0–100 + explicit confidence copy.

### Implementation notes

- **Score bands:** Can mirror `health_system_scores.metabolic.overall_score` (already 0–100). Map bands to Strategy A’s 80/65/45 placeholders only after clinical sign-off.
- **Expanded card:** Metabolic markers scored; IDL subtitles/why_it_matters; “insulin may be missing” from `missing_biomarkers` on that system.
- **Paths:** Same core scoring/orchestrator/DTO/FE as above; IDL publisher is already deterministic from `insight_graph`.

---

## 3. Liver health

**Consumer label:** Liver health  
**Clinical label:** Hepatic-Metabolic Strain Status  

### Internal engine mapping

- **Scoring:** `liver` system — **only** `alt`, `ast` in `scoring_policy.yaml`.
- **Clusters:** `hepatic` — ALT required, AST important (`clusters.yaml`).
- **Burden:** `hepatic` includes `ggt`, `alp`, `bilirubin`, `albumin`, etc. (`system_burden_registry.yaml`).
- **Phenotypes / IDL:** `ph_hepatic_alt_inflammatory_v1` (+ `ph_hba1c_metabolic_stress_v1` hepatic involvement; `ph_iron_overload_v1` lists hepatic).

### Current codebase support

- **Moderate:** Numeric score is **narrow** (enzymes only). Burden and phenotypes encode **richer** hepatic context than the consumer-facing 0–100 rail.

### Missing / weak

- **GGT and other hepatic markers** are not on the scoring rail; phenotype edges reference `signal_ggt_high` / hepatic context, but the **published domain score** cannot claim full “liver health” from scoring alone without burden/signal aggregation or policy extension.
- Risk of overstating “liver health” if the UI implies more than ALT/AST scoring supports.

### Launch readiness rating

**Launchable with light assembly** if positioned honestly as enzyme-centric **or** **medium governed work** to add GGT (and optionally ALP/bilirubin) to `scoring_policy` + `clusters.yaml` + weights.

### Implementation notes

- **Truthful card today:** ALT/AST vs lab range; if IDL “Liver Stress Pattern” enabled, cite governed text; optionally reference burden vector for GGT if product chooses to expose “strain” language consistent with burden docs.
- **Paths:** `system_burden_registry.yaml`, orchestrator burden step in `orchestrator.py`, `scoring_policy.yaml`, `clusters.yaml`, phenotype/IDL assets above.

---

## 4. Blood, iron & oxygen

**Consumer label:** Blood, iron & oxygen  
**Clinical label:** Iron-Erythropoietic / Oxygen-Carrying Status  

### Internal engine mapping

- **Scoring:** `cbc` system — `hemoglobin`, `hematocrit`, `white_blood_cells`, `platelets` only (no `mcv`, `rdw`, `iron`, `ferritin` in `scoring_policy`).
- **Burden:** `hematological` + `nutritional` include `iron`, `ferritin`, `transferrin`, indices, B12, folate, etc.
- **Phenotypes / IDL:** `ph_iron_deficiency_inflammation_v1`, `ph_iron_overload_v1`, `ph_one_carbon_homocysteine_macrocytosis_v1` with IDL rows (iron, methylation pattern).
- **Clusters:** `hematological` cluster requires Hb + WBC (platelets important) — **iron studies not in cluster schema**.

### Current codebase support

- **Strong** at **interpretation/phenotype/IDL** layer for iron and macrocytic/one-carbon patterns.
- **Weak** at **single 0–100 domain score**: iron/ferritin/transferrin are **not** scored in `ScoringEngine`; `ClusterEngineV2` only sees biomarkers that received scores from `scoring_result` (`cluster_engine_v2._extract_biomarker_scores`).

### Missing / weak

- No dedicated **customer domain score** wired to iron + RBC indices without **policy extension** or a **burden-derived** score with explicit governance.
- WBC/platelets in `cbc` scoring conflate **infection/inflammation** with **oxygen carriage** — product semantics need care.

### Launch readiness rating

**Launchable only with medium backend/governed work** (extend scoring + clusters + weighting rules), **or** launch as **pattern/IDL-first** domain with limited numeric score (honest “partial panel”).

### Implementation notes

- **Truthful card today:** Hb/Hct (and CBC components) where scored; iron studies explained via burden/flags if exposed; IDL when iron/methylation phenotypes fire.
- **Paths:** `scoring_policy.yaml`, `clusters.yaml`, `system_burden_registry.yaml`, phenotype map, IDL YAML, orchestrator burden + scoring merge logic, new domain aggregator.

---

## 5. Thyroid & energy regulation

**Consumer label:** Thyroid & energy regulation  
**Clinical label:** Thyroid Axis Status  

### Internal engine mapping

- **Burden registry:** `tsh`, `free_t3`, `free_t4`, `tgab`, `tpo_ab` → `thyroid` system.
- **Scoring:** `hormonal` system has **zero weight and no biomarkers** in `scoring_policy`.
- **Clusters:** `hormonal` cluster is effectively empty for thyroid (only optional `calcium` in `clusters.yaml`).
- **Phenotypes / IDL:** `ph_thyroid_lipid_disturbance_v1`, `ph_tsh_axis_metabolic_v1` + IDL rows; `knowledge_bus/interaction_maps/interaction_map_v1.yaml` includes `signal_thyroid_tsh_context`.
- **Root cause:** `tsh_hypotheses_v1.yaml` loaded from `root_cause_compiler_v1.py`.

### Current codebase support

- **Strong** in **knowledge bus + phenotypes + IDL + burden**.
- **Absent** on the **same 0–100 scoring + cluster rail** as metabolic/cardiovascular.

### Missing / weak

- No `HealthSystemScore` for thyroid today → no symmetric “score out of 100” from `ScoringEngine` without new policy.
- “Energy regulation” copy must not outrun **TSH/thyroid hormone** evidence actually on the panel.

### Launch readiness rating

**Medium backend/governed work** (add thyroid biomarkers to `scoring_policy`, fix `clusters.yaml` hormonal membership, calibrate weights, clinical review).

### Implementation notes

- **Truthful card today (limited):** If thyroid markers present, describe burden direction and any fired thyroid-related IDL/phenotype; avoid a numeric domain score unless derived from an approved formula.
- **Paths:** `scoring_policy.yaml`, `clusters.yaml`, `system_burden_registry.yaml`, `interpretation_display_layer_publish_v1.py`, `phenotype_map_v1.yaml`, orchestrator.

---

## 6. Kidney function

**Consumer label:** Kidney function  
**Clinical label:** Renal Filtration / Renal Strain Status  

### Internal engine mapping

- **Scoring:** `kidney` — `creatinine`, `urea`.
- **Clusters:** `renal` — creatinine required, urea important.
- **Burden:** `egfr`, `urate`, `urea_creatinine_ratio` on `renal`.
- **Phenotype:** `ph_renal_stress_v1` requires **creatinine, urea, and urate** high signals together — strict vs typical panels (`phenotype_map_v1.yaml`).

### Current codebase support

- **Moderate:** Core filtration markers on scoring rail; cluster support; renal burden broader than scoring.

### Missing / weak

- **eGFR** not in `scoring_policy` — many users expect eGFR in “kidney function”.
- Renal **phenotype** may rarely fire if urate missing — domain narrative should not imply phenotype always available.

### Launch readiness rating

**Launchable with light assembly** for an MVP score from `kidney` system; **medium** if eGFR must be first-class on the same rail with governed bands.

### Implementation notes

- **Truthful card today:** Creatinine/urea scores + cluster severity; mention eGFR only if measured and interpreted via burden/reference logic you already trust.
- **Paths:** `scoring_policy.yaml` (eGFR addition), `clusters.yaml`, `system_burden_registry.yaml`, phenotype/IDL, orchestrator.

---

## Final summary

### A. Strongest 2–3 domains to implement first (least risk)

1. **Blood sugar control** — full scoring + cluster + phenotype + IDL alignment.
2. **Cardiovascular health** — strong lipid scoring + clusters + multiple governed phenotypes/IDL; plan explicitly for CRP/homocysteine as cross-system context.
3. **Kidney function** — scoring rail for creatinine/urea is already real; burden adds eGFR when present.

### B. Domains most likely to need new governed work

- **Blood, iron & oxygen** — iron/RBC indices off the scoring rail; cluster schema gap; semantic risk if CBC score is sold as “iron”.
- **Thyroid & energy regulation** — scoring policy and cluster schema must be built; copy must stay tied to measured thyroid markers.
- **Liver health** — if the launch promise exceeds ALT/AST, GGT (+ friends) need scoring/cluster governance.

### C. First implementation shape: flat 6 vs phased

**Recommendation: Phased 3-score then 6-score** (or **4+2**):

- **Phase 1:** Blood sugar control, Cardiovascular health, Kidney function — all have non-zero `system_weight` and concrete biomarker lists in `scoring_policy.yaml`.
- **Phase 2:** Liver (after scope clarity), Blood/iron/oxygen (after policy/burden merge design), Thyroid (after hormonal scoring exists).

A **flat 6** is only safe if the UI allows **“limited / pattern-only”** states for domains without a governed 0–100 aggregate (especially thyroid and iron).

### D. Realistic sprint sequence (from current repo)

1. **SSOT:** Add `customer_health_domains_v1` (or equivalent) mapping: domain → `{ scoring_systems[], burden_systems[], phenotype_ids[], idl_internal_ids[] }` under `knowledge_bus/` + validation.
2. **Core:** Implement deterministic **domain aggregator** (read `scoring_result`, `insight_graph` burden/capacity, IDL severity) — likely `backend/core/analytics/` + call site in `orchestrator.py`.
3. **Contracts/DTO:** Extend analysis result model + `backend/core/dto/builders.py` to emit `customer_domain_scores_v1` (scores, confidence, contributors, caveats).
4. **Governance:** Clinical review of band thresholds; extend `scoring_policy.yaml` / `clusters.yaml` for agreed gaps (eGFR, GGT, thyroid panel, iron panel) in priority order.
5. **Frontend:** New results/dashboard components; **do not** replace `clinician_report_v1` strings — keep consumer vs clinical separation per `build_analysis_result_dto`.
6. **QA:** Golden panels per domain; enforce “no score without evidence” using existing unscored reasons and missing-marker lists.

---

### Note on second-wave domains (Strategy A)

**Silent inflammation** and **Hormone balance** are out of launch-core per strategy; **CRP** is already a scored `inflammatory` system, while **hormonal** scoring is empty today — promoting those to top-level scores would repeat the thyroid/iron governance problem unless intentionally designed.

---

*This blueprint follows what is **implemented** (scoring policy, clusters, phenotype map, IDL, burden registry, orchestrator paths) and labels **aggregation of existing rails** as the main “light assembly” work rather than assuming a finished six-domain product layer already exists in code.*
