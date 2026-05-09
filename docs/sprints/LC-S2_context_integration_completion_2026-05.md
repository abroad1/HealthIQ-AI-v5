# LC-S2 — Launch-core context integration (completion note)

**Work ID:** `LC-S2-CONTEXT-INTEGRATION`  
**Branch:** `feature/lc-s2-context-integration`  
**Date:** 2026-05-09  

## Summary

Wired governed statin questionnaire capture → `user_intervention_document` → `build_intervention_annotations_v1()` → production orchestrator path → `AnalysisDTO.intervention_annotations_v1`, deterministic narrative appendix (`compile_narrative_report_v1`), Wave‑1 cardiovascular consumer consequence suffix, and clinician report page‑1 `intervention_annotation_context`. Annotation is Layer B framing only; signal evaluation and scoring inputs are unchanged.

## Gate checks (bounded tests)

| Check | Evidence |
|-------|----------|
| S-1 | `test_s1_questionnaire_ssot_includes_statin_option` |
| S-2 | `test_s2_mapper_emits_valid_user_intervention_document` |
| S-3 | `test_s3_annotation_compiler_resolves_statin` |
| S-4 | `test_s4_analysis_dto_field_contract_roundtrip` |
| S-5 | `test_s5_visible_narrative_and_consumer_suffix_difference_when_annotation_present` |
| S-6 | `test_s6_annotation_helpers_do_not_import_signal_pipeline_modules` (+ architectural separation: annotations built post–Step 2 context, not fed into signal evaluator) |

Full golden-panel statin-on/off identity proofs for signals/bands remain deferred to broader regression if needed.

## Follow-ups

- Optional: golden orchestrator replay asserting identical `signal_results` / domain rails with vs without statin checkbox for a fixed panel fixture.
- Frontend shell: schema loaded from API picks up SSOT automatically; local mocks under `frontend/app/lib/mock/` were not updated in this core-engine pass.
