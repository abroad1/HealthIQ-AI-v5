# LC-S19 — Structured Payload Contract Hardening

**Work package:** LC-S16-17-19  
**Date:** 2026-05-23

## 1. Executive verdict

**PASS** — Root DTO keys machine-locked to frontend `AnalysisResult` without renaming or removing consumed fields. No breaking serialisation changes in this sprint.

## 2. DTO sources inspected

| Authority | Path |
|-----------|------|
| DTO builder | `backend/core/dto/builders.py` — `build_analysis_result_dto` |
| Contract constants | `backend/core/dto/frontend_contract_v1.py` |
| Contracts | `backend/core/contracts/report_v1.py`, `clinician_report_v1.py`, `narrative_report_v1.py`, `interpretation_display_layer_v1.py` |
| Route storage | `backend/app/routes/analysis.py` — `CLIENT_RESULT_SHAPE_V1` |
| Frontend types | `frontend/app/types/analysis.ts` |

## 3. Frontend consumers inspected

- `frontend/app/(app)/results/page.tsx`
- `frontend/app/services/analysis.ts` — `normalizeAnalysisResultPayload`
- `frontend/app/types/analysis.ts` — `AnalysisResult` interface

## 4. Field classification table

| Field / section | Producer | Consumer(s) | Classification | Consumer-safe? | Stability requirement | Notes |
|---|---|---|---|---|---|---|
| `analysis_id` | Orchestrator | Results page, PDF | Display metadata | Yes | Stable | |
| `biomarkers[]` | Scoring + enrichment | Dials, driving markers | Analytical truth | Yes | Stable | LC-S8G display fields |
| `clusters[]` | Clustering | Hero, actions, advanced | Analytical truth | Yes | Stable | |
| `insights[]` | Insight modules | Advanced (filtered) | Explanatory evidence | Partial | Stable | Legacy rows hidden |
| `overall_score` | Scoring | Advanced card | Analytical truth | Yes | Stable | |
| `status`, `created_at` | Orchestrator | Page chrome | Display metadata | Yes | Stable | |
| `risk_assessment` | Orchestrator meta | Advanced | Analytical truth | Yes | Stable | |
| `recommendations[]` | Orchestrator | Action cards | Explanatory evidence | Yes | Stable | |
| `meta` | Orchestrator | Many sections | Mixed | Partial | Stable | Contains internal graph |
| `meta.insight_graph` | `insight_graph_builder` | Advanced / compile-on-read | **Internal-only** | No (retail) | Stable | Full Layer B exposure |
| `meta.wave1_aligned_drivers` | Orchestrator | Driving markers | Display metadata | Yes | Stable | |
| `meta.upload_panel_observations` | LC-S8G | Upload fidelity | Display metadata | Yes | Stable | |
| `meta.narrative_runtime` | Orchestrator | Mock disclosure | Display metadata | Yes | Stable | |
| `clinician_report_v1` | `compile_clinician_report_v1` (read) | Hero, WHY, trust, advanced | Governed DTO | Yes | Stable | Not stored at POST |
| `balanced_systems_v1` | `compile_balanced_systems_v1` | Balanced systems card | Governed DTO | Yes | Stable | Compile-on-read |
| `interpretation_display_layer_v1` | IDL publish | Pattern cards | Governed asset-backed | Yes | Stable | |
| `narrative_report_v1` | Narrative compilers | Hero, body, WHY, next steps | Governed DTO | Yes | Stable | |
| `consumer_domain_scores[]` | Domain assembly | Wave 1 cards | Governed DTO | Yes | Stable | |
| `intervention_annotations_v1` | Intervention selector | Limited | Explanatory evidence | Partial | Stable | |
| `replay_manifest` | Orchestrator | Replay tooling | Internal-only | No | Stable | Compatibility |
| `primary_driver_system_id` | Arbitration | Layout helpers | Analytical truth | Yes | Stable | |
| `system_capacity_scores`, `burden_hash` | Burden engine | Debug/advanced | Internal-only | No | Stable | |
| `derived_markers` | Derived registry | Optional advanced | Analytical truth | Partial | Stable | |
| `report_v1.top_findings` (nested) | `compile_report_v1` | Indirect via clinician | Analytical truth | Indirect | Stable | Not API root |
| `report_v1.root_cause_v1` (nested) | `compile_root_cause_v1` | Clinician WHY sections | Governed KB-backed | Indirect | Stable | |

## 5. Analytical truth fields

`biomarkers`, `clusters`, `overall_score`, `meta.insight_graph.signal_results`, nested `report_v1.top_findings`, `primary_driver_system_id`, `system_capacity_scores`.

## 6. Explanatory evidence fields

`insights`, `recommendations`, `narrative_report_v1.*`, `clinician_report_v1.sections.root_cause`, `intervention_annotations_v1`.

## 7. Display metadata fields

`meta.wave1_aligned_drivers`, `meta.upload_panel_observations`, `meta.display_unit_policy`, `meta.narrative_runtime`, biomarker display_* fields.

## 8. Caveat fields

`clinician_report_v1.data_quality`, `consumer_domain_scores[].caveat_flags`, IDL `display_caveat`.

## 9. Polishable prose fields

`narrative_report_v1.retail_summary`, domain `headline_sentence` / `consequence_sentence` (deterministic today; Gemini-polishable later).

## 10. Internal-only fields

`meta.insight_graph` (full), `burden_hash`, `system_capacity_scores`, `replay_manifest`, ranking policy strings in advanced view.

## 11. Legacy / compatibility-only fields

`insights[]` with `manifest_id: legacy_v1` (hidden by frontend filter). `questionnaire` alias on request (deprecated).

## 12. Unknown / follow-up fields

`meta.insight_graph.layer_c_features` — surfaced in advanced; Gemini-safe subset TBD (LC-S18).

## 13. Consumer payload risks

- Full analytical graph on wire increases leakage surface (`signal_id`, internal meta).
- Compile-on-read clinician report must stay deterministic for stale persisted results.

## 14. DTO stability risks

- Accidental rename in `build_analysis_result_dto` breaks frontend — mitigated by `FRONTEND_CONSUMED_ROOT_KEYS` regression.
- Adding keys without TypeScript update — mitigated by `test_lc_s19_analysis_ts_declares_consumed_roots`.

## 15. Gemini-readiness implications

Future consumer-safe payload should emit a filtered view: retail sections only, no raw `signal_results`, prose fields marked `polishable_prose` in classification.

## 16. Recommended contract rules

1. No rename/remove of `FRONTEND_CONSUMED_ROOT_KEYS` without frontend + regression in same work package.
2. New root keys require `AnalysisResult` TypeScript update and OpenAPI regeneration.
3. `meta.insight_graph` must not become a retail dependency (hero already uses compile-on-read paths).
4. Internal-only fields documented before any API versioning.
