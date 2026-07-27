# ARCH-CONV — Residual Runtime Inventory

**Work ID:** `ARCH-CONV-RESIDUAL-AUDIT-1`  
**Date (UTC):** 2026-07-27  
**Purpose:** Estate-wide inventory of active or potentially active pathways that influence medical output.  
**Method:** Static call-chain analysis from product entry points + registry/loader inspection + prior CORRECT-1 / PKG1–3 evidence.  
**Runtime change:** NONE  

---

## 1. Decision question context

This inventory supports:

> Can the active v5 runtime estate be brought fully onto the accepted Day-One architecture through a bounded completion programme, or do remaining dependencies justify freezing v5 and moving to v6?

Accepted target:

```text
canonical research authority
→ deterministic compile / translation
→ governed runtime artefacts
→ runtime loaders
→ structured Layer B DTOs
→ frontend render / translation only
```

---

## 2. Estate snapshot (disk vs runtime)

| Measure | Count | Evidence |
|---|---:|---|
| Packages with `signal_library.yaml` | 192 | `knowledge_bus/packages/*/signal_library.yaml` |
| Unique `signal_id`s in libraries | 140 | YAML parse of `signals[].signal_id` |
| Package manifests classified for eligibility | 191 | `package_runtime_eligibility_v1` |
| kb47 `production_reachable` | 6 | PKG2 INCLUDE thyroid/egfr |
| kb47 `non_reachable` | 14 | PKG2 androgen/CK/eos suppression |
| Non–launch-critical (`out_of_launch_critical_cohort`, still loadable) | 171 | Eligibility classifier scope |
| Legacy WHY YAML assets | 40 | `knowledge_bus/root_cause/hypotheses/*_hypotheses_v1.yaml` |
| `ROOT_CAUSE_TARGET_SPECS` | 41 | `backend/core/knowledge/root_cause_registry_v1.py` |
| Compiled WHY artefacts | 9 | `knowledge_bus/compiled/hypotheses/*.yaml` |
| WHY authority register frames | 10 (9 `COMPILED_ACTIVE` + 1 `REJECTED`) | `compiled_why_authority_register_v1.yaml` |
| WHY pilot signal families | 5 | `why_authority_v1._PILOT_SIGNAL_IDS` |

**Classification rule used:** file presence alone never implies runtime authority. Items below cite callers.

---

## 3. Product entry points (traced)

| Entry point | Route / trigger | Orchestrates medical core? | Classification |
|---|---|---|---|
| Analysis start | `POST /api/analysis/start` → `AnalysisOrchestrator.run` | Yes | **A. ACTIVE AUTHORITATIVE** pathway |
| Result regeneration | `POST /api/analysis/{id}/regenerate` → same orchestrator | Yes | **A** |
| Result retrieval | `GET /api/analysis/result` → `build_analysis_result_dto` | Assembles clinician report from stored InsightGraph | **A** (assembly) / **B** (pass-through of stored Layer B) |
| PDF export | `GET /api/analysis/export/pdf` | Reuses assembled DTO | **B. ACTIVE SUPPORTING** |
| History list | `GET /api/analysis/history` | No medical recompute | **B** |
| Fixture fetch | `GET /api/analysis/fixture` | Dev/fixture | **F. TEST / FIXTURE ONLY** |
| Scheduled / background analysis workers | — | **None found** | N/A |
| SSE analysis events | `/events` returns 410 Gone | Dead product path | **E. RUNTIME-UNREACHABLE** |
| Offline replay scripts | `backend/scripts/replay_arch_conv_*` | Harness only | **F** |

Primary call chain:

```text
frontend upload
→ POST /api/analysis/start (backend/app/routes/analysis.py::start_analysis)
→ normalize biomarkers / units / questionnaire waist
→ AnalysisOrchestrator.run (backend/core/pipeline/orchestrator.py)
   → SignalRegistry + SignalEvaluator
   → score / cluster / criticality
   → build_insight_graph_v1 → compile_report_v1 → compile_root_cause_v1
   → engines + optional InsightSynthesizer
   → attach_retail_explainers_v1
   → publish_interpretation_display_layer_v1
   → compile_narrative_report_v1
   → assemble_consumer_domain_scores_v1
→ persist client_result_shape_v1
→ GET /api/analysis/result
   → build_analysis_result_dto
   → compile_clinician_report_v1 (+ balanced_systems_v1)
→ frontend/app/(app)/results/page.tsx
```

---

## 4. Pathway inventory by medical concern

Every row is classified into exactly one of:

`A ACTIVE AUTHORITATIVE` · `B ACTIVE SUPPORTING` · `C COMPATIBILITY-ONLY` · `D SHADOW / DUAL-SERVICE` · `E RUNTIME-UNREACHABLE` · `F TEST / FIXTURE ONLY` · `G UNKNOWN`

### 4.1 Signal activation / frame identity

| Item | Caller | Class | Notes |
|---|---|---|---|
| `signal_library.yaml` (192 pkgs) | `SignalRegistry._load` / `SignalEvaluator` | **A** | Estate-wide activation authority |
| Package eligibility / provenance | `classify_package_runtime_eligibility` | **B** | Gates kb47 reachability |
| `frame_runtime_authority_v1` | Registry load + InsightGraph filter | **A** | Rejected-frame inactivation |
| `signal_authority_collision_model_v1` | `SignalEvaluator.evaluate_all` | **A** | Anti-double-count for configured axes |
| Rejected metabolic package on disk | — | **E** for fire/rank/WHY; asset retained | Proven excluded by CORRECT-1 gates |
| PSI YAML (57 opt-in packages) | Loader exists; no Intelligence Core consumer | **E** | ARCH-RT-5E decision; guard tests lock |

### 4.2 Investigation selection / WHY / causal interpretation

| Item | Caller | Class | Notes |
|---|---|---|---|
| Compiled WHY artefacts (9 pilot keys) | `compile_root_cause_v1` via `resolve_frame_why_authority` mode=`compiled` | **A** | Day-One target for pilot |
| Legacy WHY YAML via `ROOT_CAUSE_TARGET_SPECS` (36 non-pilot, verified exact count) | same compiler, mode=`legacy` | **A** | **Dominant estate WHY authority** |
| Pilot legacy YAML still registered | loaders present; skipped when mode=`compiled` | **C** | Dual registration, not dual emit for COMPILED_ACTIVE |
| `signal_homocysteine_elevation_context` + shared `hcy_hypotheses_v1.yaml` | legacy WHY path | **D** | Overlaps medical narrative space with compiled hcy frames |
| `why_engine_fallback_v1` | `compile_root_cause_v1` when lead lacks finding | **A** (fallback) | Fail-open placeholder for missing governed WHY |
| Investigation specs (`inv_*.yaml`) | Not read by evaluators | **E** as runtime engine; **canonical** upstream | Compile/promotion only |
| Co-service policy (`frame_co_service_policy_v1`) | `root_cause_compiler_v1` | **A** | MCV family only today |

### 4.3 InsightGraph / top findings / drivers / ranking

| Item | Caller | Class | Notes |
|---|---|---|---|
| `build_insight_graph_v1` | Orchestrator | **A** | Graph + report assembly |
| `compile_report_v1` / ranking | InsightGraph builder | **A** | `top_findings` |
| `primary_driver_v1` | InsightGraph builder | **A** | Layer B → Layer C projection (CORRECT-1) |
| Interaction map (`interaction_map_v1.yaml`) | `signal_interaction_builder` | **A** | Family-level (`signal_id`) nodes |
| Phenotype map | IDL / narrative consumers | **A** | Family-level required signals |

### 4.4 Interventions / confidence / provenance

| Item | Caller | Class | Notes |
|---|---|---|---|
| Intervention library YAML | `intervention_selector_v1` | **A** | Text + activation_key refs |
| Confidence engines / burden / state | Orchestrator engines | **A**/`B` | Deterministic engines |
| Output-authority provenance builder | DTO / report path | **B** | Known fixture key debt for bare `inv_homocysteine_high` |
| Replay manifest | Orchestrator | **B** | Lineage metadata |

### 4.5 Clinician / consumer / cards / IDL

| Item | Caller | Class | Notes |
|---|---|---|---|
| `compile_clinician_report_v1` | GET `/result` DTO builder | **A** | Assembled at read time |
| `compile_narrative_report_v1` | Orchestrator | **A** | Consumer narrative |
| IDL records YAML | `publish_interpretation_display_layer_v1` | **A** | Retail/clinical labels |
| Retail explainer SSOT | `attach_retail_explainers_v1` | **B** | Biomarker/cluster explainers |
| Compiled Health Systems Card evidence | `assemble_consumer_domain_scores_v1` / wave1 assemblers | **A** | Compiled YAML evidence |
| Hard-coded card marker lists | — | **E** | Retired (ARCH-RT-5B / estate index) |
| Domain label constants / IDL order tuples | `domain_score_assembler.py` | **B** | Presentation/policy assembly |
| Confirmatory-test registry | WHY compilers | **A** | Shared IDs + rationale |

### 4.6 Frontend medical presentation

| Item | Consumer | Class | Notes |
|---|---|---|---|
| Results page DTO renderers | `results/page.tsx` + clinician/IDL/narrative/cards | **B** | Post-CORRECT-1: render/translate |
| `layerCInsightCopy.ts` / `systemUnderstandingCopy.ts` | Layer C sections | **B** | Governed static product copy |
| Deleted FE medical inventers | — | **E** | `ClusterInsightPanel`, `biomarkerPatternRelevance` removed |
| Display-name maps / humanizers | various FE helpers | **B** | Presentation risk if overused; not Layer B authority |

### 4.7 Analysis regeneration / replay

| Item | Class | Notes |
|---|---|---|
| Product regenerate route | **A** | Full re-run of orchestrator |
| Persisted snapshot replay on GET | **C** | Historic payload under versioning contract |
| Historic bare waist analyses | **C** + data debt | Impact audited; remediation not authorised here |

---

## 5. Migrated cohort vs residual estate

### Migrated WHY cohort (proven)

5 signals / 10 frames under `compiled_why_authority_register_v1.yaml` (9 compiled + 1 rejected inactive).

### Residual active estate (not Day-One WHY-converged)

- ~135 non-pilot `signal_id` families still fire from `signal_library`.
- 36 of 41 `ROOT_CAUSE_TARGET_SPECS` resolve unconditionally to `"legacy"` via `why_authority_v1.resolve_frame_why_authority`.
- Co-service / reject machinery is register-scoped (MCV + REJECTED keys), not estate-wide.

---

## 6. Summary counts by classification

| Class | Material pathways (approx.) | Dominant risk |
|---|---:|---|
| **A ACTIVE AUTHORITATIVE** | High (signal libraries + legacy WHY + compiled pilot + IDL + cards + interventions + ranking) | Estate medical meaning still multi-source |
| **B ACTIVE SUPPORTING** | Moderate | Assembly/policy/presentation |
| **C COMPATIBILITY-ONLY** | Moderate | Historic payloads; retired-but-registered loaders |
| **D SHADOW / DUAL-SERVICE** | Low count, high medical risk | Hcy elevation-context vs compiled hcy; layered “why it matters” |
| **E RUNTIME-UNREACHABLE** | Material on disk | PSI; rejected metabolic fire path; retired hard-coded cards |
| **F TEST / FIXTURE ONLY** | Harnesses / fixtures | Must not be treated as product |
| **G UNKNOWN** | Few | No scheduled workers found; residual config toggles (e.g. LLM allow flags, blocked-pkg env opt-in) need continued monitoring |

---

## 7. Evidence gaps (explicit)

1. Full dynamic coverage/tracing of every one of 140 signal families in production traffic was **not** executed in this audit (static reachability of loaders is proven; per-signal product traffic share is unverified).
2. LLM narrative path reachability depends on runtime policy flags — default deny is evidenced historically; live production flag state should be confirmed at ops time (**G** until environment-confirmed).
3. `compiled/estate_index_v1.yaml` is **stale** relative to PKG3 compiled WHY set — do not use as authoritative inventory.
