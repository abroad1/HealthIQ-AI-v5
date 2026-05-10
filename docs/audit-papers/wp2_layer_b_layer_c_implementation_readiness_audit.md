# WP-2 Layer B → Layer C Implementation Readiness Audit

**Date:** 2026-05-10  
**Branch:** `docs/pre-sprint3-closure-pack`  
**Auditor:** Claude Code (investigation/audit mode — no implementation files modified)  
**Evidence standard:** Every claim in this report is backed by a file path and line number (or explicit function/class name). If something does not exist, it is stated explicitly.

---

## 1. Executive Summary

This audit is a direct-inspection implementation readiness assessment for WP-2 (Pre-Sprint 3 Technical Closure: Layer B → Layer C Contract Readiness). It answers ten concrete questions about the current codebase state and produces findings that govern whether Sprint 3 can be authored.

**Overall verdict:** Sprint 3 cannot be authored yet. The five blockers identified in the Pre-Sprint 3 Closure Pack (C-1 through C-5) remain open. This audit deepens the evidence base for all five and adds a material finding not previously diagnosed: the `primary_concern` blank is a proving harness architecture gap, not a compiler bug — the harness extracts results from `AnalysisDTO.model_dump()` which does not contain `clinician_report_v1`, whereas the unit test suite correctly builds `clinician_report_v1` from `report_v1` and finds it populated.

**Recommended path:** Path B (formalise `meta.insight_graph.report_v1` as the approved Layer B delivery mechanism) with bounded contractualisation — for the short term. Path A (promote `top_findings` and `root_cause_v1` to first-class `AnalysisDTO` fields) is the correct long-term shape. The proving harness gap for `clinician_report_v1` must be fixed independently of this architecture decision.

---

## 2. Sprint 3 Readiness Verdict

| Check | Status | Evidence |
|-------|--------|----------|
| C-1 — Architecture decision (Path A or B) recorded | OPEN | No ADR file found. The Pre-Sprint 3 Closure Pack names this as a decision only — no code required. |
| C-2 — Schema decision for groups 4 and 5 recorded | OPEN | `narrative_intent`, `section_intent`, `intent_code`, `allowed_consumer_wording`, `prohibited_claims`, `wording_constraint` — all return zero grep hits across `backend/` and `knowledge_bus/`. |
| C-3 — `validate_llm_output_v2` review completed | OPEN | `backend/core/llm/validator_v2.py:110-178` — validator exists; review against §3.9 boundary not recorded. Gaps confirmed: ranked finding preservation, banding/confidence preservation, hypothesis set integrity, prohibited claim detection — all unprotected. |
| C-4 — Clinician `primary_concern` investigation complete | OPEN — ROOT CAUSE FOUND (see §8) | Root cause is a proving harness architecture gap, not a compiler bug. The compiler works correctly. Fix is bounded. |
| C-5 — IDL `clinical_only` consumer gate hotfix delivered | OPEN | `frontend/app/components/results/InterpretationPatternsSection.tsx:16` — filter still does not check `frontend_allowed_term !== 'clinical_only'`. Confirmed by direct inspection. |
| C-6 — Pre-Sprint 2 statin gate confirmed | CLOSED | All 6 checks S-1 through S-6 confirmed PASS per Pre-Sprint 2 gate closure. |
| C-7 — Sprint 1 WHY assets confirmed | CLOSED | WHY packs confirmed in pipeline per LC-S1 completion note. |
| C-8 — Layer B first-class fields confirmed | CLOSED | `results.py:287-302` — `consumer_domain_scores`, `interpretation_display_layer_v1`, `narrative_report_v1`, `intervention_annotations_v1` all present as typed first-class `AnalysisDTO` fields. |
| C-9 — Mock-mode honesty deferral recorded | CLOSED | Pre-Sprint 1 §3.7 explicitly deferred to Sprint 4. |
| C-10 — `insights[]` retirement decision recorded | CLOSED | Pre-Sprint 1 §3.6 recorded. |

**C-1 through C-5 must all be closed before Sprint 3 is authored.**

---

## 3. Files Inspected

### Authority documents
- `docs/planning-papers/healthiq_pre_sprint3_closure_pack_FINAL.md` — full read
- `docs/audit-papers/gate_compliance_audit_sprint3_readiness.md` — full read
- `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md` — §3.9 section and full decision register

### Backend contracts
- `backend/core/models/results.py` — full read (AnalysisDTO: lines 246-303; InsightResult: 138-162)
- `backend/core/contracts/report_v1.py` — full read (ReportV1: lines 77-86; ReportTopFindingV1: lines 15-27)
- `backend/core/contracts/root_cause_v1.py` — full read (RootCauseV1, RootCauseFindingV1, RootCauseHypothesisV1)
- `backend/core/contracts/clinician_report_v1.py` — full read (ClinicianReportV1, Page1SummaryBlockV1: lines 82-103)
- `backend/core/contracts/narrative_report_v1.py` — full read (NarrativeReportV1: lines 16-33)
- `backend/core/contracts/insight_graph_v1.py` — partial (report_v1 field at line 201)

### Backend pipeline
- `backend/core/dto/builders.py` — full read (build_analysis_result_dto: lines 29-86; clinician_report compilation: lines 48-53)
- `backend/core/analytics/report_compiler_v1.py` — extensive read (compile_clinician_report_v1: lines 494-668; primary_concern construction: lines 563-567)
- `backend/core/analytics/narrative_report_compiler_v1.py` — partial (compile_narrative_report_v1 signature: lines 526-533; body assembly: lines 615-665)
- `backend/core/pipeline/orchestrator.py` — partial (AnalysisDTO assembly: lines 2245-2265; insight_graph.model_dump: line 2142; compile_narrative_report_v1 call: lines 2214-2220)
- `backend/core/llm/validator_v2.py` — full read (validate_llm_output_v2: lines 110-178)

### Backend tools / harness
- `backend/tools/run_golden_panel.py` — extensive read (run_golden_panel: lines 302-421; return path: line 421)
- `backend/tools/launch_core_proving_harness.py` — extensive read (fingerprint_analysis_result: lines 168-184; _clinician_heads: lines 104-124)
- `backend/tests/unit/test_launch_core_proving_harness.py` — full read
- `backend/tests/unit/test_clinician_report_runtime_alignment.py` — partial (lines 1-60)

### Frontend
- `frontend/app/components/results/InterpretationPatternsSection.tsx` — partial (selectVisibleIdlRecords: lines 11-18)
- `frontend/app/types/analysis.ts` — partial (InterpretationDisplayRecordV1: lines 225-241; InterpretationFrontendAllowedTermV1: line 217)
- `frontend/tests/components/InterpretationPatternsSection.test.tsx` — full read

### Proving artefacts
- `docs/audit-papers/launch-core-proving/latest_fingerprints.json` — partial (AB__baseline run entry, confirming blank clinician fields)

---

## 4. Current Data Flow: `top_findings`, `root_cause_v1`, `clinician_report_v1`, `narrative_report_v1`

### 4.1 `top_findings` source and flow

**Where created:** `backend/core/analytics/report_compiler_v1.py` — the report compiler assembles `top_findings` from `signal_results` inside the insight graph. The typed contract is `ReportTopFindingV1` (`backend/core/contracts/report_v1.py:15-27`) with fields: `priority_rank`, `signal_id`, `system`, `signal_state`, `confidence`, `confidence_reasons`, `primary_metric`, `supporting_markers`, `why_it_matters`.

**Where stored:** `InsightGraphV1.report_v1: Optional[ReportV1]` (`backend/core/contracts/insight_graph_v1.py:201`). `ReportV1` carries `top_findings: List[ReportTopFindingV1]` (`backend/core/contracts/report_v1.py:81`).

**How it reaches the pipeline output:** The orchestrator calls `insight_graph.model_dump()` at line 2142 and stores the result as `meta["insight_graph"]`. This dumps the entire `InsightGraphV1` including its `report_v1` (with `top_findings`) as a nested dict. The `AnalysisDTO` field `meta: Optional[Dict[str, Any]]` (`backend/core/models/results.py:278`) carries this as an opaque dict.

**Is there a typed model that can be reused:** Yes. `ReportTopFindingV1` (`report_v1.py:15-27`) is the existing typed contract. It is already used inside `ReportV1`.

**What code changes would expose it as first-class `AnalysisDTO.top_findings`:** A new field `top_findings: Optional[List[ReportTopFindingV1]] = None` added to `AnalysisDTO` (`results.py`), plus orchestrator code to extract and populate it at assembly time (lines 2245-2264 in orchestrator). This is a BEHAVIOUR-class change requiring a full governed work package.

**What tests currently protect them:** `backend/tests/unit/test_report_compiler_v1.py` and `backend/tests/unit/test_clinician_report_runtime_alignment.py` protect the compiler contract. No tests directly assert that `top_findings` is accessible as a first-class `AnalysisDTO` field (because it is not one).

### 4.2 `root_cause_v1` source and flow

**Where created:** `backend/core/analytics/root_cause_compiler_v1.py` (imported by `report_compiler_v1.py` at line 40: `from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1`). The typed contract is `RootCauseV1` (`backend/core/contracts/root_cause_v1.py:58-63`) with `findings: List[RootCauseFindingV1]`.

**Typed contract:** `RootCauseFindingV1` (`root_cause_v1.py:48-56`) contains `signal_id`, `primary_metric`, `signal_state`, `signal_confidence`, `hypotheses: List[RootCauseHypothesisV1]`. Each `RootCauseHypothesisV1` (`root_cause_v1.py:34-46`) contains `hypothesis_id`, `title`, `summary`, `hypothesis_confidence`, `evidence_for: List[RootCauseEvidenceItemV1]`, `evidence_against: List[RootCauseEvidenceItemV1]`, `missing_data: List[RootCauseMissingItemV1]`, `confirmatory_tests: List[RootCauseConfirmatoryTestV1]`, `safety_class`.

**How it reaches the pipeline output:** Same path as `top_findings`. `root_cause_v1` is a field on `ReportV1` (`report_v1.py:85`). When the insight graph is dumped at orchestrator line 2142, `root_cause_v1` becomes a nested dict at `meta.insight_graph.report_v1.root_cause_v1`.

**Can it be exposed as first-class `AnalysisDTO.root_cause_v1`:** Yes — by adding `root_cause_v1: Optional[RootCauseV1] = None` to `AnalysisDTO` and populating it in the orchestrator. This is BEHAVIOUR-class / HIGH-risk.

**What file changes required (do not implement):**
- `backend/core/models/results.py` — add import for `RootCauseV1` from `core.contracts.root_cause_v1`; add field to `AnalysisDTO`
- `backend/core/pipeline/orchestrator.py` — extract `root_cause_v1` from `insight_graph` and pass to `AnalysisDTO()` constructor
- `backend/tests/unit/test_report_compiler_v1.py` — add assertion that `AnalysisDTO.root_cause_v1` is populated and non-null for AB/VR panels

### 4.3 `AnalysisDTO` assembly path

**Current `AnalysisDTO` fields** (`backend/core/models/results.py:246-303`):

```
analysis_id, biomarkers, clusters, insights, status, created_at, overall_score,
primary_driver_system_id, system_capacity_scores, burden_hash, unmapped_biomarkers,
derived_markers, meta, replay_manifest, lifestyle,
interpretation_display_layer_v1, narrative_report_v1,
consumer_domain_scores, intervention_annotations_v1
```

**`clinician_report_v1` is NOT a field on `AnalysisDTO`.** It is assembled separately by `build_analysis_result_dto()` in `backend/core/dto/builders.py:48-53` which calls `compile_clinician_report_v1()` using `report_v1` extracted from `meta["insight_graph"]`.

**The `build_analysis_result_dto()` function** (`builders.py:29-86`) returns a plain `Dict[str, Any]` (not an `AnalysisDTO`) that adds `clinician_report_v1`, `balanced_systems_v1`, and several other fields on top of `AnalysisDTO` content. This dict is what the HTTP API route serves to the frontend.

**Where new first-class fields should be added:** `backend/core/models/results.py` in the `AnalysisDTO` class, and correspondingly populated in `backend/core/pipeline/orchestrator.py` at the `AnalysisDTO(...)` constructor call (~lines 2245-2265).

**Would adding them break existing consumers:** Adding new `Optional` fields with `None` defaults to `AnalysisDTO` is non-breaking for existing consumers. The `model_config = ConfigDict(frozen=True, extra="forbid")` means field additions are safe but extra keys are forbidden — so new fields must be added to the model, not passed as extras.

**Frontend types:** `frontend/app/types/analysis.ts` would need updating to expose new fields. Currently `top_findings` and `root_cause_v1` are not typed in the frontend types (they are accessible only through nested `meta` traversal).

**Persistence/replay fixtures:** The orchestrator calls `dto.model_dump()` and the golden panel runner stores this as `analysis_result.json`. If new fields are added to `AnalysisDTO`, the artifact shape changes. Existing fixture comparison tests that do exact-match on `analysis_result.json` would need updating. The `VOLATILE_FIELD_ALLOWLIST` in `run_golden_panel.py:29-33` strips time-volatile fields — it does not need changing.

**Tests that would fail:** Any test doing exact `analysis_result.json` snapshot comparison would need fixture updates. `test_clinician_report_runtime_alignment.py` would continue to work as it directly calls `compile_clinician_report_v1()`.

### 4.4 `narrative_report_v1` compiler path

**Compiler function:** `compile_narrative_report_v1()` in `backend/core/analytics/narrative_report_compiler_v1.py:526-533`.

**Current signature:**
```python
def compile_narrative_report_v1(
    *,
    analysis_id: str,
    meta: Optional[Mapping[str, Any]] = None,
    insight_graph: Optional[Mapping[str, Any]] = None,
    idl_bundle: Any = None,
    intervention_annotations_v1: Optional[InterventionAnnotationsV1] = None,
) -> NarrativeReportV1:
```

**What it currently receives:** The compiler receives `insight_graph` as `Optional[Mapping[str, Any]]` — the raw dict produced by `insight_graph.model_dump()`. It does NOT receive typed objects for `top_findings` or `root_cause_v1`. It navigates the dict by key (`insight_graph.get("primary_driver_system_id", ...)` at line 612-613; `_fired_suboptimal_signal_ids(insight_graph)` at line 568).

**What it does with `top_findings` and `root_cause_v1`:** It does NOT directly use `top_findings` or `root_cause_v1` from `insight_graph`. The current v1 implementation uses `signal_results` to determine which signals fired (`_fired_suboptimal_signal_ids`), then assembles prose from YAML assets keyed by `compiler_role` and `pathway_explainer_id`. `top_findings` are not used by the narrative compiler — they are used by the clinician report compiler.

**Where the five sections are assembled:**
- `retail_summary` — `_build_retail_summary(idl_bundle, compiler_meta)` (line 637)
- `lead_narrative` — `lead_text` assembled from pathway/functional YAML assets (lines 580-603)
- `body_overview` — `_build_body_overview(...)` (line 615-623)
- `next_steps_narrative` — `_collect_next_steps(...)` (line 639-645)
- `clinician_synthesis` — `_build_clinician_synthesis(...)` (line 646-654)

**How a governed prose-contract scaffold should be inserted:** The compiler's `insight_graph` parameter should be replaced (or supplemented) by a typed `NarrativePayloadV1` object that carries the subset of fields the compiler actually needs. This would be the Layer B → Layer C contract object. Currently the compiler reads `insight_graph.get("primary_driver_system_id")` and `_fired_suboptimal_signal_ids(insight_graph)` — both of which could be typed fields on such an object.

---

## 5. Recommended Layer B Payload Implementation Path

### Decision needed: Path A vs Path B

**Path A — Promote `top_findings` and `root_cause_v1` to first-class `AnalysisDTO` fields**

Risk: HIGH (BEHAVIOUR class — modifies pipeline assembly, orchestrator, AnalysisDTO contract).  
Benefit: Clean typed Layer B → Layer C contract. Sprint 3 implementors work against typed objects.  
Scope: 3 file changes minimum (`results.py`, `orchestrator.py`, tests). One full governed work package required.

**Path B — Formalise `meta.insight_graph.report_v1` as the approved Layer B delivery path**

Risk: LOW (docs/decision record only; no production code change required for the architecture decision itself).  
Benefit: Avoids HIGH-risk pipeline change. The data is already present and proven in the existing clinician report unit tests. Sprint 3 can be authored against a contractualised `insight_graph.report_v1` shape.  
Additional code required: Update `compile_narrative_report_v1()` to accept a typed wrapper for the fields it needs from `insight_graph` (its current usage of `insight_graph` is already narrow). This is STANDARD risk.

**Audit recommendation: Path B as the binding short-term decision, Path A as named Sprint 6 work.**

Justification:
1. The clinician report unit test (`test_clinician_report_runtime_alignment.py:39-59`) proves that `compile_clinician_report_v1()` correctly produces a non-empty `primary_concern` when called directly from `meta.insight_graph.report_v1` — confirming the existing delivery path works.
2. The `ReportV1` type (`report_v1.py:77-86`) is already a typed Pydantic model. Contractualising it is a documentation decision, not a schema invention.
3. Sprint 3's purpose (Transformation Plan) is to formalise the governed payload sent from analytical truth to narrative generation. A contractualised `insight_graph.report_v1` with an explicit Layer C compiler signature is achievable in Sprint 3 scope without requiring a preceding HIGH-risk pipeline restructure.
4. Path A should be named as a Sprint 6 architectural cleanup task in the ADR.

**If Path B is chosen, the following compiler signature change is the bounded code deliverable for WP-2 (STANDARD risk):**

Update `compile_narrative_report_v1()` to accept a typed `ReportV1` object (or a minimal typed wrapper) rather than a raw `Mapping[str, Any]` for the `insight_graph` parameter. This makes the Layer B → Layer C interface typed without requiring structural `AnalysisDTO` changes.

---

## 6. Recommended Governed Prose-Contract Scaffold

### Q5 — Governed prose-contract scaffold design

**Current state:** Groups 4 (narrative intent) and 5 (wording/claim boundaries) from §3.9 do not exist anywhere in the codebase. Zero grep hits for all relevant field names across `backend/` and `knowledge_bus/`.

**Where it should live:** A new `NarrativePayloadV1` Pydantic model, placed in `backend/core/contracts/narrative_payload_v1.py`. This is the formal Layer B → Layer C handoff object. It is separate from `NarrativeReportV1` (which is the Layer C output, not the Layer B input).

**Minimal v1 schema recommendation:**

```python
class NarrativeSectionIntentV1(BaseModel):
    section_id: str  # "retail_summary" | "lead_narrative" | "body_overview" | "next_steps_narrative" | "clinician_synthesis"
    intent_code: str  # "prioritise" | "explain_mechanism" | "express_uncertainty" | "frame_next_steps" | "support_clinician_fast_read" | "reassure"
    
class NarrativeClaimBoundaryV1(BaseModel):
    allowed_consumer_wording: List[str]  # e.g. ["suggests", "may reflect", "is consistent with"]
    prohibited_claims: List[str]  # e.g. ["diagnoses", "confirms", "rules out"]
    allowed_claim_strength: str  # "suggestive" | "associative" | "correlative"

class NarrativePayloadV1(BaseModel):
    analysis_id: str
    top_findings: List[ReportTopFindingV1]
    root_cause_v1: Optional[RootCauseV1]
    clinician_report_source: ReportV1
    section_intents: List[NarrativeSectionIntentV1]
    claim_boundaries: NarrativeClaimBoundaryV1
    intervention_annotations_v1: Optional[InterventionAnnotationsV1]
```

**Files that would need changing (do not implement):**
- New file: `backend/core/contracts/narrative_payload_v1.py`
- `backend/core/analytics/narrative_report_compiler_v1.py` — update `compile_narrative_report_v1()` to accept `NarrativePayloadV1` instead of raw `Mapping[str, Any]`
- `backend/core/pipeline/orchestrator.py` — construct `NarrativePayloadV1` from the insight graph at assembly time and pass it to the compiler

**Decision required before authoring Sprint 3:** Whether groups 4 and 5 are Sprint 3 scope (recommended) or deferred. If deferred, a compensating control must be named (e.g., extended `validate_llm_output_v2` guard as the only protection).

---

## 7. `validate_llm_output_v2` Gap Assessment

**File:** `backend/core/llm/validator_v2.py:110-178`

**What is currently protected:**

| Protection category | Status | Evidence |
|--------------------|--------|----------|
| Schema validation (LLMResultV2) | PROTECTED | `validator_v2.py:126-130` — `LLMResultV2.model_validate(llm_json)` raises `ValidationError` on schema failure |
| Numeric invention guard (evidence and actions fields) | PROTECTED | `validator_v2.py:143-154` — extracts numerics from `evidence` and `actions`, checks against prompt numerics |
| Red-flag ID referencing | PROTECTED | `validator_v2.py:170-176` — checks red_flags list against `prompt_red_flags` and `prompt_ids` |

**What is NOT protected:**

| Protection category | Status | Gap description |
|--------------------|--------|-----------------|
| Lead finding preservation | NOT PROTECTED | No check that the lead finding ID in the LLM output matches the lead finding passed in the prompt. Gemini can produce prose that centres a different finding without failing validation. |
| Ranking / runner-up preservation | NOT PROTECTED | No check that the ranked order of findings in LLM output matches `top_findings` order from the prompt. |
| Confidence and banding preservation | NOT PROTECTED | No check that band labels (strong/stable/watch/review) or confidence tier claims in generated prose match the Layer B `consumer_domain_scores`. |
| Hypothesis set integrity | NOT PROTECTED | No check that hypotheses mentioned in LLM narrative are a subset of `root_cause_v1.findings[*].hypotheses`. Gemini can invent hypotheses without failing validation. |
| Prohibited claim detection | NOT PROTECTED | No check for prohibited claim strength wording (e.g., "diagnoses", "confirms", "rules out"). Groups 4 and 5 from §3.9 have no enforcement point. |
| Evidence text ID referencing (lenient) | PARTIALLY PROTECTED | `validator_v2.py:156-167` — the check exists but has a `pass` branch that allows free text that references no known ID. The comment says "allow free text that might reference concepts." This is functionally not a guard. |

**What validator changes are needed:**

For Sprint 3 to be safe to author (given the Gemini path will be activated in Sprint 3 or Sprint 4):
1. Add `_check_lead_finding_preserved(prompt_json, result)` — verify the narrative's primary topic signal ID matches `prompt_json["top_findings"][0]["signal_id"]` if that field is present in the prompt.
2. Add `_check_no_invented_hypotheses(prompt_json, result)` — verify any hypothesis ID mentioned in narrative text matches a known `hypothesis_id` from `root_cause_v1.findings[*].hypotheses[*]`.
3. Add `_check_no_prohibited_claims(result)` — regex check for prohibited wording patterns in `insight.evidence` and `insight.description`.

**What tests should be added:**
- `test_validate_llm_output_v2_rejects_invented_lead_finding()`
- `test_validate_llm_output_v2_rejects_invented_hypothesis()`
- `test_validate_llm_output_v2_rejects_prohibited_claim_language()`

These can be LOW-risk additions (no pipeline change, pure validation layer extension).

---

## 8. Clinician `primary_concern` Root-Cause Investigation

### Finding: this is a proving harness architecture gap, not a compiler bug.

**Observed symptom:** All 8 proving harness runs in `latest_fingerprints.json` show `primary_concern_head: ""`, `key_findings_head: ""`, `top_hypothesis_line_head: ""`.

**Root cause, traced through the code:**

**Step 1 — What `run_golden_panel()` returns.**  
`backend/tools/run_golden_panel.py:354`: `dto_dump = dto.model_dump() if hasattr(dto, "model_dump") else dict(dto)`. This dumps `AnalysisDTO`. The function returns `analysis_result` which is this dump.

**Step 2 — What `AnalysisDTO` contains.**  
`backend/core/models/results.py:246-303` — `AnalysisDTO` has NO `clinician_report_v1` field. The `clinician_report_v1` is assembled by `build_analysis_result_dto()` in `builders.py:48-53` and is NOT part of `AnalysisDTO`. Therefore `dto.model_dump()` does not contain `clinician_report_v1`.

**Step 3 — What the proving harness extracts.**  
`backend/tools/launch_core_proving_harness.py:104-124`, function `_clinician_heads(analysis_result)`:
```python
cr = analysis_result.get("clinician_report_v1") or {}
```
Since `analysis_result` is `dto.model_dump()` (an `AnalysisDTO` dump without `clinician_report_v1`), `cr` is always `{}`. All three extracted fields (`primary_concern_head`, `key_findings_head`, `top_hypothesis_line_head`) will always be `""`.

**Step 4 — Confirmation that the compiler works correctly.**  
`backend/tests/unit/test_clinician_report_runtime_alignment.py:39-60` — this test calls `run_golden_panel()` to get `analysis_result`, then manually extracts `meta.insight_graph.report_v1` and calls `compile_clinician_report_v1()` directly. The assertion at line 49 `assert contract.sections.page1.primary_concern` passes — meaning `primary_concern` is non-empty when the compiler is called correctly. This test is passing (it is in the unit test suite).

**Conclusion:** The clinician report compiler produces correct output. The proving harness `_clinician_heads()` function reads `analysis_result.get("clinician_report_v1")` from a dict that never contains that key (because it is an `AnalysisDTO` dump, not a `build_analysis_result_dto()` dict). The harness is reading from the wrong source.

**Fix required (bounded — STANDARD or LOW risk):**  
Update `launch_core_proving_harness.py:_clinician_heads()` to extract `clinician_report_v1` by calling `compile_clinician_report_v1()` directly from `meta.insight_graph.report_v1`, following the pattern used in `test_clinician_report_runtime_alignment.py:23-36`. Alternatively, call `build_analysis_result_dto()` on the raw analysis dict to get the full DTO dict. The fix is isolated to `backend/tools/launch_core_proving_harness.py` — it does not touch any governed pipeline files.

**This is NOT a BEHAVIOUR-class change.** It is a harness correction that ensures the proving surface matches what users see via the HTTP API path (which does call `build_analysis_result_dto()`).

**Important implication for Sprint 3:** Sprint 3 will design the Layer B payload. The proving surface must be fixed to correctly reflect `clinician_report_v1` before Sprint 3's Layer C compiler is proven against it. This fix (C-4) is a WP-2 task.

---

## 9. IDL `clinical_only` Gate Assessment

**File:** `frontend/app/components/results/InterpretationPatternsSection.tsx:11-18`

**Current filter function:**
```typescript
export function selectVisibleIdlRecords(
  bundle: InterpretationDisplayLayerBundleV1 | null | undefined
): InterpretationDisplayRecordV1[] {
  if (!bundle?.records?.length) return [];
  return [...bundle.records]
    .filter((r) => r.enabled_for_frontend === true)
    .sort((a, b) => a.display_order_priority - b.display_order_priority);
}
```

**Gap confirmed:** The filter checks only `enabled_for_frontend === true`. It does NOT check `r.frontend_allowed_term !== 'clinical_only'`. Per `frontend/app/types/analysis.ts:217`, `InterpretationFrontendAllowedTermV1 = 'phenotype_allowed' | 'clinical_only'`. Records with both `enabled_for_frontend: true` and `frontend_allowed_term: 'clinical_only'` would pass this filter and be rendered on consumer-facing surfaces.

**Can `clinical_only` records currently render on consumer surfaces:** YES. If a `clinical_only` IDL record has `enabled_for_frontend: true` and its signal fires, it will be returned by `selectVisibleIdlRecords()` and rendered. The gate is absent.

**Is the proposed fix simply filtering `frontend_allowed_term !== 'clinical_only'`:** YES. Adding `.filter((r) => r.frontend_allowed_term !== 'clinical_only')` to the chain is the complete fix. Single-line addition.

**What test changes are required:** The existing test in `frontend/tests/components/InterpretationPatternsSection.test.tsx` uses `baseRecord` with `frontend_allowed_term: 'clinical_only'` (line 34) and `enabled_for_frontend: true`. The test at line 76-82 currently passes because the `baseRecord` has `display_order_priority: 2` and `enabled_for_frontend: true`, but `ph_second_v1` has `enabled_for_frontend: false`. Adding the `clinical_only` filter would cause `ph_first_v1` (display_order_priority 1, `frontend_allowed_term: 'clinical_only'`) and `ph_third_v1` (display_order_priority 3, `frontend_allowed_term: 'clinical_only'`) to be filtered out. The existing test would need updating to:
- Add a record with `frontend_allowed_term: 'phenotype_allowed'` to represent the visible case
- Assert that `clinical_only` records are excluded even when `enabled_for_frontend: true`
- Add explicit test case: `it('filters out clinical_only records even when enabled_for_frontend', ...)`

**Are backend changes needed:** No. The `clinical_only` term is already set at the backend (`backend/core/contracts/interpretation_display_layer_v1.py:71`) and passed through the `InterpretationDisplayRecordV1` contract. The frontend is the enforcement point and the only thing requiring a change.

---

## 10. Test Impact / Required Tests

| WP-2 Task | Test changes needed | Risk class |
|-----------|---------------------|------------|
| C-4: Proving harness fix (`_clinician_heads`) | Update `test_launch_core_proving_harness.py` to assert non-empty `primary_concern_head` after fix | LOW |
| C-3: Validator extension | New: `test_validate_llm_output_v2_rejects_invented_lead_finding()`, `test_validate_llm_output_v2_rejects_invented_hypothesis()`, `test_validate_llm_output_v2_rejects_prohibited_claim_language()` | LOW |
| C-5: IDL clinical_only gate | Update `InterpretationPatternsSection.test.tsx` — add phenotype_allowed record to visible test, add clinical_only exclusion assertion | LOW |
| Path B contractualisation (if chosen) | Update `test_clinician_report_runtime_alignment.py` to cover new compiler signature if changed | STANDARD |
| Groups 4 and 5 schema (if Sprint 3 scope) | New: `test_narrative_payload_v1_schema.py` — validate NarrativePayloadV1 construction and schema contract | LOW |

**Tests that currently pass and must not break:**
- `backend/tests/unit/test_clinician_report_runtime_alignment.py` — must continue passing (it directly calls compiler, not affected by harness fix)
- `backend/tests/unit/test_report_compiler_v1.py` — must continue passing
- `backend/tests/regression/test_obs2_questionnaire_exercise_unknown_regression.py` — must continue passing (unrelated to Layer B changes)
- `frontend/tests/components/InterpretationPatternsSection.test.tsx` — will need updating (as described in §9)

---

## 11. Risk Classification

| WP-2 Sub-task | Risk Class | Justification |
|---------------|------------|---------------|
| C-1 — Architecture decision (Path A or B) | NONE (docs only) | No code change. ADR document only. |
| C-2 — Groups 4 and 5 schema decision | NONE (docs only) for decision; LOW/STANDARD for implementation | Decision is docs only. If Sprint 3 implements, new contract file (`narrative_payload_v1.py`) is additive and does not touch existing engine logic. |
| C-3 — Validator gap review and extension | LOW | Pure validation layer additions in `validator_v2.py`. Does not touch pipeline, SSOT, or analytical engine. |
| C-4 — Proving harness `_clinician_heads` fix | LOW | Isolated to `backend/tools/launch_core_proving_harness.py`. Does not modify pipeline, models, or contracts. Tooling file only. |
| C-5 — IDL `clinical_only` consumer gate | LOW | Single-line filter addition in `InterpretationPatternsSection.tsx`. Frontend consumer filter only — no backend change. |
| Path B contractualisation (compiler signature) | STANDARD | Updates `narrative_report_compiler_v1.py` signature. Touches the analytics layer but is a signature-only change if the compiler's internal logic is not altered. Needs STANDARD-risk governed work package. |
| Path A AnalysisDTO promotion | HIGH | Structural `AnalysisDTO` change + orchestrator pipeline change. BEHAVIOUR class — requires full HIGH-risk work package with Claude audit + GPT architectural review. |
| Groups 4 and 5 Sprint 3 implementation | STANDARD | New contract file + compiler signature change. If claim boundary enforcement is added to the validator, that is LOW. If it touches orchestrator wiring, STANDARD. |

---

## 12. Recommended WP-2 Implementation Scope

WP-2 consists of five tasks (matching C-1 through C-5). Below is what each task should contain.

### WP-2-T1 — Architecture decision record (docs only, no code)
- GPT records: Path A or Path B for `top_findings` / `root_cause_v1`
- If Path B: explicitly state that `ReportV1` (typed Pydantic model at `backend/core/contracts/report_v1.py`) is the contractual Layer B source for these fields; state that `compile_clinician_report_v1()` accessing `report_v1` via `meta.insight_graph` is the approved delivery mechanism
- If Path B: name Path A as a Sprint 6 follow-on
- Deliverable: ADR document in `/docs/architecture/` (new file)

### WP-2-T2 — Narrative intent and wording boundary schema decision (docs only, no code)
- GPT records: whether groups 4 and 5 are Sprint 3 scope or deferred
- If Sprint 3 scope: define minimum field names (matching the schema sketch in §6 above)
- If deferred: name the compensating control (e.g., the validator extension from T3 alone, plus explicit statement that Gemini is not activated until groups 4/5 are implemented)
- Deliverable: decision recorded in the Sprint 3 prompt front matter or a standalone schema sketch document

### WP-2-T3 — `validate_llm_output_v2` gap review and optional extension (code — LOW risk)
- Read `backend/core/llm/validator_v2.py` (already done in this audit)
- Record decision on each of the six gaps (lead finding preservation, ranking, confidence/banding, hypothesis integrity, prohibited claims, numeric invention — last one already done)
- Implement the three new checks listed in §7 if mandatory-before-Sprint-3
- Add three new unit tests
- Deliverable: updated `validator_v2.py` + new tests + decision record

### WP-2-T4 — Proving harness `_clinician_heads` fix (code — LOW risk)
- Fix `backend/tools/launch_core_proving_harness.py:_clinician_heads()` to compile `clinician_report_v1` from `meta.insight_graph.report_v1` following the pattern in `test_clinician_report_runtime_alignment.py:23-36`
- Run the proving harness after fix and confirm `primary_concern_head` is non-empty across all 8 runs
- Update `latest_fingerprints.json` and `PROVING_REPORT.md` with corrected output
- Add assertion to `test_launch_core_proving_harness.py` that `primary_concern_head` is non-empty
- Deliverable: fixed harness + updated proving artefacts + new test assertion

### WP-2-T5 — IDL `clinical_only` consumer gate (code — LOW risk)
- Fix `frontend/app/components/results/InterpretationPatternsSection.tsx:16` — add `.filter((r) => r.frontend_allowed_term !== 'clinical_only')` to `selectVisibleIdlRecords()`
- Update `frontend/tests/components/InterpretationPatternsSection.test.tsx` — add phenotype_allowed test record, add explicit `clinical_only` exclusion assertion
- Branch: `fix/idl-clinical-only-consumer-gate`
- Deliverable: merged fix before Sprint 3 is authored

---

## 13. Open Questions / Blockers

### OQ-1 — Path A vs Path B decision (BLOCKER — C-1)

The programme must make a binding written decision. This audit recommends Path B for the short term, but the decision must come from GPT (architecture authority). Sprint 3 cannot be scoped without knowing which shape the Layer C compiler will receive.

### OQ-2 — Groups 4 and 5 Sprint 3 vs deferred decision (BLOCKER — C-2)

If deferred, a compensating control must be explicitly named in the Sprint 3 prompt. If Sprint 3 scope, the minimum schema must be defined (the sketch in §6 is a starting point, not a final authority). This is a GPT decision.

### OQ-3 — Validator extension mandatory-before-Sprint-3 classification (BLOCKER — C-3)

The audit confirms the validator gaps. Whether each gap is mandatory-before-Sprint-3 or accepted as bounded risk (given the Gemini path is not yet live) is a programme decision, not a technical finding. The audit recommends the three checks in §7 be implemented before Sprint 3 because Sprint 3 will author the Layer C payload that will eventually be fed to Gemini — starting with the correct guard scope now avoids a HIGH-risk retrofit later.

### OQ-4 — Proving harness root cause confirmed (NOT a blocker — actionable immediately)

The `primary_concern` blank is a proven harness gap, not an engine defect. This is the most actionable finding in this audit. WP-2-T4 can begin immediately — no architectural decision is required first. It is a tooling fix only.

### OQ-5 — `insights[]` removal start (ADVISORY — not Sprint 3 blocker)

Pre-Sprint 1 §3.6 said "start the removal process now." `InsightResult.manifest_id` defaults to `"legacy_v1"` at `results.py:155`. Frontend still renders `analysis_result.insights` at `results/page.tsx:141`. No feature flag has been applied. This should be noted in the Sprint 4 prompt as a standing obligation.

### OQ-6 — Questionnaire minimum proving set (ADVISORY — pre-Sprint 5 requirement, not Sprint 3)

The questionnaire has 55+ required fields (`backend/ssot/questionnaire.json`). Pre-Sprint 1 §3.4 required reduction for human testing practicality. Not a Sprint 3 concern.

---

## 14. Non-Document Files Modified

**NONE.** This audit read the following code files but did not modify any of them:

`backend/core/models/results.py`, `backend/core/contracts/report_v1.py`, `backend/core/contracts/root_cause_v1.py`, `backend/core/contracts/clinician_report_v1.py`, `backend/core/contracts/narrative_report_v1.py`, `backend/core/contracts/insight_graph_v1.py`, `backend/core/dto/builders.py`, `backend/core/analytics/report_compiler_v1.py`, `backend/core/analytics/narrative_report_compiler_v1.py`, `backend/core/pipeline/orchestrator.py`, `backend/core/llm/validator_v2.py`, `backend/tools/run_golden_panel.py`, `backend/tools/launch_core_proving_harness.py`, `backend/tests/unit/test_launch_core_proving_harness.py`, `backend/tests/unit/test_clinician_report_runtime_alignment.py`, `frontend/app/components/results/InterpretationPatternsSection.tsx`, `frontend/app/types/analysis.ts`, `frontend/tests/components/InterpretationPatternsSection.test.tsx`, `docs/audit-papers/launch-core-proving/latest_fingerprints.json`.
