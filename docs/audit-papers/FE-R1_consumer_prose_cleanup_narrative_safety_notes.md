# FE-R1 — Consumer Prose Cleanup and Narrative Safety Notes

**work_id:** FE-R1  
**branch:** `frontend/fe-r1-consumer-prose-cleanup`  
**SOP:** AUTOMATION_BUS v1.3.1  
**controlling audit:** `docs/audit-papers/FE_R0_results_page_prose_source_trace_audit.md`

## 1. Preflight results

| Check | Result |
|-------|--------|
| Branch | `frontend/fe-r1-consumer-prose-cleanup` |
| Stash | empty (no convenience stash) |
| FE-R0 audit on `main` | present (`4bb5d49` lineage) |
| Kernel token | `FE-R1`, IN_PROGRESS after start |
| Work tree at start | implementation in progress; `results-page-full.png` moved outside repo for clean kernel start |

## 2. FE-R0 findings addressed

| FE-R0 issue | Disposition |
|-------------|-------------|
| Internal compiler text in retail summary / lead narrative | Fixed at source via `consumer_prose_safety_v1` + LC-S3 assembly + narrative/report compilers |
| Raw confidence `0.90 vs 0.90` | Fixed in `report_compiler_v1` consumer formatters |
| IDL template suffix on labels | `sanitize_retail_display_label` at publish + narrative build |
| Unbounded KB dumps in lead/secondary | Bounded builders + paragraph filtering |
| `Prioritised follow-up (governed assets)` / `Functional read —` headers | Next-steps header rewrite; functional-read titles excluded from body theme list |
| Empty `balanced_systems_v1` with high domain scores | Fallback from `consumer_domain_scores` when insight_graph has no `system_stable_normal` |
| ALP at lab floor shown as Critical | `frontend_status_from_lab_reference(..., biomarker_name=)` in orchestrator (both call sites) |
| Blood sugar headline vs stable glucose wording | `domain_narrative_wave1` conflict guard extended |
| Frontend “Clinician-structured why” heading | Renamed to consumer-safe heading on results page |

## 3. Source fields changed

- `narrative_report_v1`: `retail_summary`, `lead_narrative`, `secondary_narratives`, `next_steps_narrative`, `body_overview` (via LC-S3 assembly + `narrative_report_compiler_v1`)
- `clinician_report_v1.sections.page1`: `runner_up_why_not_lead_line`, `runner_up_topic_line`, `confidence_and_missing_data`
- `interpretation_display_layer_v1.records[].retail_display_label`
- `balanced_systems_v1` (compile path + DTO builder meta injection)
- `biomarkers[].status` (direction-aware lab reference mapping)

## 4. Before / after examples (representative)

| Surface | Before (class) | After (class) |
|---------|----------------|---------------|
| Retail summary | “The ranked lead pattern is … lab anchor …” | Concise homocysteine-led consumer summary without ranking mechanics |
| Confidence line | “0.90 vs 0.90” | “Several findings were close in priority…” / missing-marker caveat |
| IDL label | `Homocysteine High: is outside the optimal range on this panel` | `Homocysteine High` (suffix stripped) |
| Next steps header | `Prioritised follow-up (governed assets)` | `Suggested follow-up themes` |
| Results UI section | `Clinician-structured "why" and evidence` | `Primary finding — clinical detail` |
| ALP dial (46 U/L at min) | `critical` | Non-critical direction-aware status |

## 5. Backend vs frontend fixes

**Backend/compiler (primary):** narrative assembly, report compiler, IDL publish sanitization, balanced systems fallback, orchestrator status mapping, domain narrative wave1 guard.

**Frontend (limited):** results page section heading only; no new narrative logic invented in UI.

## 6. Omitted from UX

- Raw hypothesis lists with confidence weights in lead narrative (stripped by sanitization / not emitted in consumer builders)
- Long duplicate confirmatory-test blocks when already shown in structured sections (bounded copy)

## 7. Deferred

- Full hero vs cardiovascular domain-card sentence deduplication (requires assembler-level contributor suppression; not fully deduped in FE-R1)
- Page journey restructure (FE-R2 scope per journey paper v6)
- Knowledge Bus content edits (out of scope)

## 8. Balanced systems investigation

`compile_balanced_systems_v1` only populated from `insight_graph.system_states` with `system_stable_normal`. AB baseline had high `consumer_domain_scores` but no matching stable-normal rows → empty block. **Fix:** `_fallback_from_consumer_domain_scores` when stable rows absent and domain scores ≥ 80 (excluding primary cardiovascular driver when applicable). `build_analysis_result_dto` injects `consumer_domain_scores` into meta for compile.

## 9. ALP critical-status investigation

Retail status used lab position without LC-S14 direction override. ALP at reference minimum mapped to critical/high-critical. **Fix:** pass `biomarker_name` into `frontend_status_from_lab_reference` at both orchestrator biomarker DTO sites.

## 10. Tests added/updated

- `backend/tests/regression/test_fe_r1_consumer_prose_cleanup.py` (new)
- Existing scaffold smoke pack unchanged in intent; run in CI with FE-R1 branch

## 11. Sentinel updates

Added to `sentinel/packs/escaped_defects_v1.json`:

- `consumer_prose_internal_compiler_leakage`
- `consumer_prose_unbounded_kb_dump`
- `consumer_retail_label_template_suffix`
- `consumer_confidence_raw_numeric_leakage`
- `consumer_balanced_systems_empty_when_domains_stable`
- `consumer_biomarker_status_direction_mismatch`

## 12. Residual risks

- Narrative fingerprint drift on LC-S5/LC-S21 proving checks if baseline copy shifts materially
- Partial domain-card duplication may remain until FE-R2 assembler work
- Sanitization-by-substring may need tuning if new internal tokens appear

## 13. Recommendation for FE-R2

Proceed with results journey restructure only after FE-R1 merge: consumer prose is bounded and internal-token guarded; FE-R2 should focus on section order, progressive disclosure, and deduplicated domain/hero presentation without reintroducing compiler dumps.

## GPT retrospective boundary approval

GPT Architecture has reviewed the FE-R1 boundary deviations identified by Claude audit and retrospectively approves them as bounded, necessary, and architecturally appropriate for FE-R1.

Approved boundary change 1:
backend/core/pipeline/orchestrator.py
- Approved only for the two call-site changes passing biomarker_name=biomarker_name into frontend_status_from_lab_reference().
- Rationale: this is the minimal bridge needed for the ALP direction-aware frontend status correction. It does not alter orchestration order, pipeline phase ownership, DTO shape, or analytical routing.

Approved boundary change 2:
backend/core/analytics/consumer_prose_safety_v1.py
- Approved as the central consumer prose safety module.
- Rationale: centralised safety and sanitisation is preferable to scattered string handling across compilers.

Approved boundary change 3:
backend/core/analytics/narrative_compiler_lc_s3_assembly_v1.py
- Approved only for wiring bounded consumer-safe narrative builders into the LC-S3 narrative assembly path.

Approved boundary change 4:
backend/core/analytics/primitives.py
- Approved only for extending frontend_status_from_lab_reference() with biomarker-aware directionality correction using existing LC-S14 scoring directionality policy.

Approved boundary change 5:
backend/core/dto/builders.py
- Approved only for passing consumer_domain_scores into balanced_systems compilation so the false empty-state behaviour can be corrected.

This approval does not authorise any further pipeline, DTO, scoring, or compiler expansion beyond the changes already present in the FE-R1 branch.
