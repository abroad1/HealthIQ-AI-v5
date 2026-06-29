# P2-4 — NarrativePayload Brief Hardening

**Work ID:** P2-4  
**Date closed:** 2026-06-29

## 1. Start state

P2-2+P2-3 merged on `main`. `NarrativePayloadV1` v1.1 existed with section intents, evidence boundaries, claim boundaries, and LLM translation constraints. Gemini inactive. P2-4 required before P4-1/P4-2.

## 2. Authority reviewed

* `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md`
* `automation_bus/latest_pipeline_advisory.md`
* `docs/sprints/beta_readiness/P2-1_prose_substrate_wave1_wired_completion.md`
* `docs/sprints/beta_readiness/P2-2_P2-3_retail_pathway_explainer_completion.md`
* `backend/core/contracts/narrative_payload_v1.py` (pre-change)
* Read-only consumers: `narrative_payload_builder_v1.py`, `narrative_report_compiler_v1.py`, `narrative_brief_enforcement_v1.py`

## 3. Contract sufficiency assessment

Contract structure was largely sufficient for Wave 1 prose substrate and missing-marker caution representation via `permitted_source_fields` / `NarrativeEvidenceBoundaryV1`. Material gaps remained in LLM boundary defaults, deny-all semantics, no-new-findings explicit guard, `required_caveats` minimum when intents present, and `report_story_priority` validation. **Hardened** (not confirmed as-is).

## 4. Changes made

* `future_llm_may_rewrite` default changed to `False` (deny-by-default).
* `may_translate_section_ids` documented as deny-all when empty; section id validation added.
* `introduce_findings_not_in_governed_brief` added to `DEFAULT_LLM_PROHIBITED_ACTIONS`.
* `DEFAULT_REQUIRED_CAVEATS` constant added; validator requires non-empty `required_caveats` when `section_intents` present.
* `report_story_priority` validated against `NarrativeSectionIdV1`.
* Optional `missing_marker_caution_refs` field for P2-2+P2-3 caution passthrough.
* Clinician-reserved sections blocked from `may_translate_section_ids`.
* `GOVERNED_BRIEF_CORE_SECTION_INTENT_IDS` and `MISSING_MARKER_EVIDENCE_SOURCE_KEY` documented.

## 5. Validation result

P2-4 unit tests, existing NarrativePayload / Layer B-1 regression tests, and golden gate (via `run_work_package.py finish`) required at closure.

## 6. Gemini readiness impact

Contract now enforces B→C brief safety boundaries for future constrained Gemini translation. **No Gemini activation.** CEO approval still required before production narrative LLM.

## 7. Carry-forwards

See `P2-4_carry_forward.yaml`. Builder explicit `future_llm_may_rewrite=True` on consumer surfaces deferred. P2-FRAME-ROUTING-ARCHITECTURE-1 deferred.

## 8. Recommended next sprint

P4-1 Gemini activation design (CEO approval gate) or P2-FRAME-ROUTING-ARCHITECTURE-1 per programme priority.

**pipeline_advisory_trigger:** true  
**pipeline_advisory_reason:** P2-4 NarrativePayload hardening complete; P4-1 Gemini activation design is next blocked only by CEO approval gate.
