# KB-S56 Preflight — Renal Research Promotion + Renal WHY Completion

**work_id:** KB-S56-PREFLIGHT  
**mode:** READ_ONLY investigation (no implementation)  
**date:** 2026-04-06  
**evidence:** Repository files cited inline below.

---

## 1. Executive summary

### What renal capability already exists

- **Runtime signal evaluation:** Renal-associated signals `signal_creatinine_high`, `signal_urea_high`, and `signal_urate_high` are exercised in unit tests against `SignalRegistry` (e.g. `backend/tests/unit/test_signal_evaluator.py` fixtures at lines 1422–1427, 1548–1558).
- **Promoted Knowledge Bus packages** (signal libraries + manifests) exist for creatinine, urea, and urate high patterns, including KB-S52C-era packages and older `pkg_s24_*` packages, e.g.:
  - `knowledge_bus/packages/pkg_kb52c_creatinine_high_reduced_glomerular_filtration/signal_library.yaml` (`signal_creatinine_high`, `system: renal`, `explanation` block with mechanism/pathway/interpretation at lines 83–95).
  - `knowledge_bus/packages/pkg_kb52c_urea_high_prerenal_volume_depletion_or_catabolic_load/signal_library.yaml` (`signal_urea_high`).
  - `knowledge_bus/packages/pkg_kb52c_urate_high_gout_crystal_deposition_risk/signal_library.yaml` (`signal_urate_high`).
- **Research investigation specs** on disk, e.g. `knowledge_bus/research/investigation_specs/inv_creatinine_high_renal_v1.yaml`, `inv_urea_high_renal.yaml` (legacy naming `inv_urea_high_renal` / creatinine spec content).
- **Phenotype scaffolding:** `ph_renal_stress_v1` in `knowledge_bus/phenotypes/phenotype_map_v1.yaml` (lines 61–85) declares required signals and a **single** `required_edges` entry (creatinine_high → urea_high) with `requires_research_promotion: true` and `chain_expectations.status: "pending"`.
- **Fixture:** `backend/tests/fixtures/panels/phenotypes/ph_renal_stress_v1.json` — synthetic panel for the phenotype id.
- **Clinician AB/VR fixtures** mention renal *clearance context* only in a **homocysteine** hypothesis pathway (`hcy_renal_clearance_context_v1` in `backend/tests/fixtures/reports/clinician_report_v1_ab.json` / `_vr.json`), not a dedicated creatinine/urea/urate root-cause stack.

### What is missing

- **Runtime interaction map (`interaction_map_v1.yaml`):** No renal `nodes` and no renal `edges` (verified by grep across `knowledge_bus/interaction_maps/interaction_map_v1.yaml`; file begins with metabolic/hepatic/inflammatory/vascular/hormonal/lipid nodes only — lines 5–45). This matches the adopted strategy baseline: “**Renal interaction-map status | Structurally incomplete; zero active renal interaction edges**” (`docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`, table at lines 233–241).
- **Root-cause / clinician WHY (hypothesis loaders):** `backend/core/analytics/root_cause_compiler_v1.py` `_ROOT_CAUSE_TARGETS` (lines 61–94) **does not** register `signal_creatinine_high`, `signal_urea_high`, or `signal_urate_high`. No matching `load_*_hypotheses_v1` imports exist for renal signals in that module. **Grep** over `backend/core/knowledge/*.py` finds **no** creatinine/urea/urate renal hypothesis loaders.
- **Phenotype edge evidence:** `knowledge_bus/phenotypes/rationales/ph_renal_stress_edge_creatinine_to_urea.md` is explicitly a **placeholder** (“requires research promotion”, lines 8–9).
- **Naming collision risk:** Roadmap label **KB-S56** (renal wave) must **not** be confused with existing Knowledge Bus package ids **`pkg_kb56_*`**, which are **Wave C globulin / ALP** packages under the same numeric prefix (e.g. `knowledge_bus/packages/pkg_kb56_globulin_low_hypogammaglobulinemia_or_protein_loss/package_manifest.yaml` line 7: “HealthIQ Knowledge Bus — KB-S56”). Those are **unrelated** to the roadmap’s renal pathway sprint naming.

### Whether KB-S56 is justified now

**Yes.** The adopted roadmap explicitly calls out renal structural incompleteness and defines a KB-S56 lineage for renal promotion + WHY completion (`docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`, lines 688–690, cross-cutting lines 240–241, 277, 782). Repo evidence aligns: **signals and packages exist**, but **interaction map and root-cause WHY plumbing for renal signals do not**.

---

## 2. Strategy interpretation (roadmap KB-S56)

**Source:** `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`.

| Roadmap phrase | Meaning in context |
|----------------|------------------|
| **“Renal research promotion”** | Elevating governed evidence for the renal pathway from research/placeholder artefacts (e.g. phenotype edge `requires_research_promotion: true`, placeholder rationale MD) to **promoted, reviewable** evidence suitable for **interaction map** and phenotype **chain** maturity — not merely having `signal_library` YAML on disk. |
| **“Renal WHY completion”** | Closing the gap where **breadth** (signals) is not matched by **governed explanatory depth** at the **clinician/root-cause** layer — i.e. wiring renal signals into the same class of **deterministic hypothesis** infrastructure used for other targets in `root_cause_compiler_v1.py`. Strategy baseline states most live signals still lack WHY at runtime (lines 235–239); renal fits that pattern in code (no `_ROOT_CAUSE_TARGETS` entries). |
| **Capability unlocked** | End-to-end **renal-aware reasoning chains** in structured output: renal nodes/edges in `interaction_map_v1.yaml` feeding `signal_interaction_builder` / insight graph, plus **hypothesis lists** for renal primary signals in `clinician_report_v1` / root-cause compilation — subject to existing report compiler contracts (`backend/core/analytics/report_compiler_v1.py` loads interaction map at line 180). |
| **Parallel prep vs immediate runtime** | Roadmap positions KB-S56 as **Wave 4** lineage work (lines 668–690) alongside product surfaces; wording **“after its prerequisite research promotion”** implies **ordered dependency**: research promotion **before** declaring WHY/path complete, not speculative runtime-only patches without evidence assets. |

**Note:** Roadmap does **not** spell out file-level tasks; this document derives them from repo diffs above.

---

## 3. Renal asset audit

### 3.1 Research assets

| Asset | Path | State |
|-------|------|--------|
| Creatinine investigation spec | `knowledge_bus/research/investigation_specs/inv_creatinine_high_renal_v1.yaml` | **Present** — full v1-style spec (`spec_id`, supporting markers, overrides, evidence). |
| Urea investigation spec | `knowledge_bus/research/investigation_specs/inv_urea_high_renal.yaml` | **Present** — renal domain, narrative mechanism block. |
| Phenotype placeholder rationale | `knowledge_bus/phenotypes/rationales/ph_renal_stress_edge_creatinine_to_urea.md` | **Present but placeholder only** (lines 1–9). |
| Phenotype map entry | `knowledge_bus/phenotypes/phenotype_map_v1.yaml` (`ph_renal_stress_v1`) | **Partial** — definition exists; `chain_expectations.status: "pending"`; edge `requires_research_promotion: true` (lines 72–85). |

### 3.2 Promoted / runtime-usable (Knowledge Bus packages)

| Signal | Example package paths | State |
|--------|----------------------|--------|
| `signal_creatinine_high` | `knowledge_bus/packages/pkg_kb52c_creatinine_high_reduced_glomerular_filtration/`, `knowledge_bus/packages/pkg_s24_creatinine_high_renal/` | **Present** — promoted libraries with thresholds, `explanation` blocks, governance manifests. |
| `signal_urea_high` | `knowledge_bus/packages/pkg_kb52c_urea_high_prerenal_volume_depletion_or_catabolic_load/` | **Present**. |
| `signal_urate_high` | `knowledge_bus/packages/pkg_kb52c_urate_high_gout_crystal_deposition_risk/`, `knowledge_bus/packages/pkg_s24_urate_high_metabolic/` | **Present**. |

### 3.3 Runtime map / chain assets

| Asset | State |
|-------|--------|
| `knowledge_bus/interaction_maps/interaction_map_v1.yaml` | **Missing renal** nodes/edges (no matches for creatinine/urea/urate/renal). |
| Root-cause hypothesis YAML loaders for renal | **Missing** under `backend/core/knowledge/` (no renal-specific loaders found). |

### 3.4 SSOT / biomarkers

- `backend/ssot/biomarkers.yaml` marks multiple markers with `system: renal` — **present** (engine taxonomy supports renal grouping). This is **not** the same as interaction-map or hypothesis completeness.

---

## 4. Runtime / WHY audit

### 4.1 Current renal runtime behaviour

- **Signal firing:** Evaluator + registry support renal signals (see test fixtures cited above).
- **Package `explanation`:** Ingested signal libraries carry narrative `explanation` fields (e.g. creatinine package lines 83–95). **Not verified in this preflight:** whether every downstream consumer surfaces `explanation` in `clinician_report_v1` without root-cause hypotheses — **grep** in `report_compiler_v1.py` for `mechanism` returned no matches in that file; clinician narrative is primarily **`compile_root_cause_v1`**-driven for hypothesis structure (`report_compiler_v1.py` calls `compile_root_cause_v1` around lines 657–670).
- **Interaction chaining:** `backend/core/analytics/signal_interaction_builder.py` builds chains solely from **`interaction_map_v1.yaml`** (path at line 42). With **no renal nodes**, **no deterministic renal chains** are produced at this layer.

### 4.2 Current renal WHY behaviour (root-cause / clinician)

- **`root_cause_compiler_v1.py`:** **No renal signal targets** in `_ROOT_CAUSE_TARGETS` (lines 61–94). Therefore **no governed hypothesis lists** keyed to creatinine/urea/urate high as primary drivers in that compiler path.
- **Contrast:** Other domains (e.g. HbA1c, lipids, iron, hepatic, thyroid) have explicit `load_*_hypotheses_v1` registrations in the same list.

### 4.3 Identified gaps (research vs runtime)

| Gap | Type | Evidence |
|-----|------|----------|
| No renal edges in interaction map | **Runtime / structural** | `interaction_map_v1.yaml` lacks renal signals; strategy table confirms “zero active renal interaction edges”. |
| No renal root-cause targets | **Runtime WHY** | `root_cause_compiler_v1.py` `_ROOT_CAUSE_TARGETS` omission. |
| Phenotype edge not promoted | **Promotion / content** | `ph_renal_stress_edge_creatinine_to_urea.md` placeholder; phenotype `requires_research_promotion: true`. |
| Phenotype chain not enforced | **Contract / governance** | `chain_expectations.status: "pending"` in `phenotype_map_v1.yaml` lines 83–84. |
| Fixture biomarker naming | **Possible contract gap** | `ph_renal_stress_v1.json` uses `uric_acid` key; tests for `signal_urate_high` use `urate` in evaluator fixture (`test_signal_evaluator.py` line 1555). **Requires** careful cross-check against canonical SSOT ids during implementation (not resolved here). |

---

## 5. Promotion-gap audit (research → product)

| Gap | Domain | Category | Fits KB-S56? |
|-----|--------|----------|--------------|
| Placeholder rationale → promoted evidence | `knowledge_bus/phenotypes/rationales/` | **Promotion + content** | **Yes** |
| Add renal nodes/edges to interaction map | `knowledge_bus/interaction_maps/interaction_map_v1.yaml` | **Runtime structural** | **Yes** |
| Register renal signals in root-cause compiler + add hypothesis assets | `backend/core/analytics/root_cause_compiler_v1.py`, `backend/core/knowledge/` | **Runtime WHY** | **Yes** |
| Advance phenotype chain status when evidence allows | `knowledge_bus/phenotypes/phenotype_map_v1.yaml` | **Contract / governance** | **Yes** (when evidence gates are met) |
| DB persistence of explainer-adjacent fields | Persistence layer | **Out of scope** for renal-specific KB-S56 unless sprint explicitly includes it | **Later** (not renal-specific in this preflight) |

---

## 6. WHAT “renal WHY completion” requires (grounded)

From repo evidence, completion is **not** “write more research JSON” alone. It requires **at minimum**:

1. **Governed promotion** replacing the **placeholder** renal phenotype edge rationale (`ph_renal_stress_edge_creatinine_to_urea.md`) and satisfying `requires_research_promotion: true` in `phenotype_map_v1.yaml`.
2. **Interaction map promotion:** new **nodes** (at least `signal_creatinine_high`, `signal_urea_high`, `signal_urate_high`) and **edges** with rationales meeting `signal_interaction_builder` validation (minimum rationale length per `load_interaction_map_v1` in `signal_interaction_builder.py` lines 85+).
3. **Root-cause wiring:** new hypothesis YAML loaders (patterned like existing `load_hba1c_hypotheses_v1` etc.) + **registration** in `_ROOT_CAUSE_TARGETS` in `root_cause_compiler_v1.py`.
4. **Regression / fixtures:** extend AB/VR or golden expectations if clinician report shape gains renal hypotheses; align `ph_renal_stress_v1` fixture keys with SSOT (`ph_renal_stress_v1.json` vs `urate` naming).
5. **Optional later split:** if promotion and map edits must pass **separate** governance review, gate **interaction map revision** separately from **hypothesis loader** merges (same programme, two reviewable artefacts).

**Combination:** **Package promotion is largely done** for basic signal definitions; **missing work is predominantly runtime structure (interaction map + root cause) and evidence promotion for the phenotype edge**, not greenfield signal invention.

---

## 7. Seeding recommendation

### Chosen recommendation

**`SPLIT_INTO_PROMOTION_AND_WHY_PHASES`**

### Rationale

- **Evidence ordering:** Roadmap says completion comes **after** prerequisite research promotion; the phenotype map already **flags** promotion on the critical edge (`requires_research_promotion: true`, `phenotype_map_v1.yaml` line 80).
- **Different blast radii:** `interaction_map_v1.yaml` changes affect **all panels**’ chain ranking (`insight_graph_builder.py` integration at lines 407–415); root-cause additions affect **clinician JSON** shape and ranking. **Splitting** reduces the risk of a single mixed PR that is hard to audit.
- **Suggested bounded shape:**
  - **Phase A — Promotion:** Finalise renal phenotype edge evidence; replace placeholder rationale MD; update `phenotype_map_v1.yaml` flags/status **only as evidence becomes non-placeholder**.
  - **Phase B — Runtime structure:** Add renal nodes/edges to `interaction_map_v1.yaml` (with `map_revision` bump per existing convention); run/extend interaction-map validation tests.
  - **Phase C — WHY / clinician:** Add `backend/core/knowledge/*renal*_hypotheses_v1.yaml` (exact naming TBD by sprint author), register targets in `root_cause_compiler_v1.py`; extend clinician fixtures (AB/VR) if required.

**Alternative considered:** `PROCEED_AS_ONE_BOUNDED_SPRINT` — acceptable **only** if Automation Bus / programme office explicitly treats KB-S56 as **one work_id** with **sequential internal checkpoints** (promotion sign-off before map merge, etc.). Repo complexity still favours **phase labels** in the sprint prompt.

**Not chosen:** `DO_NOT_PROCEED_NO_CLEAR_RENAL_GAP` — **rejected**; gap is explicit in strategy and code.

---

## 8. Boundary check (out of scope for KB-S56)

Unless explicitly re-scoped by programme governance:

- **Frontend:** FE results surfaces, FE-VISUALISATION, retail explainer (`RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md` renal **educational** copy is separate from clinical WHY).
- **Non-renal phenotype expansion** beyond what is required to **close renal** coherence (e.g. do not expand unrelated phenotypes in the same sprint).
- **Broad reporting-policy changes** (e.g. primary concern policy) — renal work should use **existing** ranking/compiler contracts.
- **Unrelated package ingestion** (e.g. new biomarker batches).
- **Symptom relevance** — explicitly deferred elsewhere; not part of renal WHY.
- **Renaming collision:** Do **not** repurpose `pkg_kb56_*` packages; roadmap KB-S56 is **programme nomenclature**, not `package_id`.

---

## 9. File evidence index (quick reference)

| Path | Relevance |
|------|-----------|
| `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` | KB-S56 lineage; renal incompleteness baseline |
| `knowledge_bus/interaction_maps/interaction_map_v1.yaml` | No renal nodes/edges |
| `knowledge_bus/phenotypes/phenotype_map_v1.yaml` | `ph_renal_stress_v1`, pending chain, promotion flag |
| `knowledge_bus/phenotypes/rationales/ph_renal_stress_edge_creatinine_to_urea.md` | Placeholder |
| `knowledge_bus/packages/pkg_kb52c_*_creatinine_high_*/signal_library.yaml` | Promoted creatinine signal + explanation |
| `knowledge_bus/packages/pkg_kb52c_urea_high_*/signal_library.yaml` | Promoted urea signal |
| `knowledge_bus/packages/pkg_kb52c_urate_high_*/signal_library.yaml` | Promoted urate signal |
| `knowledge_bus/research/investigation_specs/inv_creatinine_high_renal_v1.yaml` | Research spec |
| `backend/core/analytics/root_cause_compiler_v1.py` | No renal `_ROOT_CAUSE_TARGETS` |
| `backend/core/analytics/signal_interaction_builder.py` | Interaction map loader |
| `backend/tests/unit/test_signal_evaluator.py` | Renal signal fixtures |
| `backend/tests/fixtures/panels/phenotypes/ph_renal_stress_v1.json` | Phenotype fixture |
| `knowledge_bus/packages/pkg_kb56_*/` | **Different** KB numeric — globulin tranche; not roadmap renal KB-S56 |

---

## 10. Required output — recommendation line

**`SPLIT_INTO_PROMOTION_AND_WHY_PHASES`**

**Named gaps:** (1) renal interaction map nodes/edges absent; (2) renal root-cause / hypothesis loaders absent; (3) phenotype renal edge still placeholder / promotion-flagged; (4) phenotype chain enforcement pending.

**Likely touched surfaces:** `knowledge_bus/phenotypes/`, `knowledge_bus/interaction_maps/interaction_map_v1.yaml`, `backend/core/analytics/root_cause_compiler_v1.py`, new/extended `backend/core/knowledge/` hypothesis YAML, `backend/tests/fixtures/reports/` and/or golden panel expectations.
