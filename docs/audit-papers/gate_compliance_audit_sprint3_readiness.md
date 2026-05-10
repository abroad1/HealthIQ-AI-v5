# Gate Compliance Audit — Sprint 3 Readiness
Date: 2026-05-10

---

## 1. Executive Answer

**Are we clear to author Sprint 3?** No — not yet. Sprint 3 authoring can proceed only after bounded closure tasks covering (a) the §3.9 Layer B payload completeness gap, (b) the IDL `clinical_only` consumer-surface gate, and (c) the `validate_llm_output_v2` review scope. These are genuine gate obligations from the closed authority documents, not discretionary items.

### Top 5 Findings

1. **Layer B payload richness is partially built but incomplete (§3.9 PARTIALLY SATISFIED).** `AnalysisDTO` exposes `consumer_domain_scores`, `interpretation_display_layer_v1`, `narrative_report_v1`, and `intervention_annotations_v1` as first-class fields. However `top_findings`, `root_cause_v1`, and `clinician_report_v1` are NOT first-class AnalysisDTO fields — they live inside `meta.insight_graph.report_v1` (a nested opaque dict) and are assembled at the DTO-builder stage via `compile_clinician_report_v1()`. The §3.9 contract requires these as explicit Layer B handoff fields. Narrative intent fields (per-section intent codes) and wording/claim boundary fields (allowed consumer wording, prohibited claims, allowed claim strength) do not exist anywhere in the payload — these are fully absent.

2. **The `validate_llm_output_v2` review obligation remains open and is not merely a Sprint 3 authoring note (§3.9 OUTSTANDING).** The guard exists (`backend/core/llm/validator_v2.py`) but its validation contract was explicitly flagged in §3.9 notes as requiring review "before Sprint 3 authors the Layer C payload." No recorded review against the full §3.9 boundary list has occurred. The validator checks numeric invention and red-flag referencing but does not verify ranked finding preservation, confidence/banding preservation, hypothesis set integrity, or wording boundary compliance — the material risks in the §3.9 boundary.

3. **IDL `clinical_only` consumer gate is not enforced on the consumer rendering path (§3.8 PARTIALLY SATISFIED).** The `idl_records_v1.yaml` registry has 7 records with `frontend_allowed_term: clinical_only` and `enabled_for_frontend: true`. The consumer component `selectVisibleIdlRecords()` filters only on `enabled_for_frontend === true` — it does NOT check `frontend_allowed_term !== 'clinical_only'`. The §3.8 gate explicitly states "`clinical_only` records must be gated from consumer surfaces." This verification is still a Sprint 4 carriage task per §3.8, but it was framed as a pre-expose verification that must happen before IDL records are exposed to users. This gap is PRESENT in production-path code today.

4. **Proving harness CHECK S-3/S-5/S-6 are PASS; full proving suite (CHECKs 1, 2, 4, 5, 6) has not been run against the binary criteria definitions.** The proving harness output confirms statin-on/off invariance (CHECK S-6 analog), CV consequence_sentence difference statin-on vs off (CHECK S-5 PASS), and lifestyle/context narrative payoff (CHECK 1 directional PASS). However CHECK 2 (alcohol bridge in human language in lead_narrative), CHECK 4 (no legacy_v1 insights visible), and CHECK 5 (no band-headline contradiction) have not been explicitly verified against their binary criteria. The `manifest_id` default in `InsightResult` is still `"legacy_v1"` (results.py:155) and the frontend still renders `analysis_result.insights` at results/page.tsx:141.

5. **Mock-mode honesty wording (§3.7) has not been implemented.** The approved wording "Your report is built from governed clinical rules applied to your lab data. AI-personalised narrative is not active in this view." appears in zero frontend files. This is a Sprint 4 carriage task (DEFERRED BY DESIGN), but it represents a live honesty gap in the current product for paying users.

---

## 2. Pre-Sprint 1 Compliance Table

| Item | Status | Evidence | Explanation |
|------|--------|----------|-------------|
| Biology slice decided and bounded | SATISFIED | `LC-S1_analytical_hardening_completion_2026-05.md §1`; `backend/core/knowledge/load_root_cause_hypotheses.py` loaders confirmed; `root_cause_compiler_v1.py` targets all seven signals | All seven slice signals have WHY assets: `hcy_hypotheses_v1`, `mcv_high_hypotheses_v1`, `apoa1_cardio_risk_hypotheses_v1`, `hypercortisolism_hypotheses_v1`, plus pre-existing `alp_low`, `ldl_cholesterol_high`, `hcy_hypotheses_v1` loaders |
| Silent-WHY policy — targeted WHY completion | SATISFIED | LC-S1 completion note §2; regression test `test_lc_s1_root_cause_slice_signals.py` exists | Three new WHY packs added; A-1 correction applied to `apoa1_cardio_risk_hypotheses_v1.yaml` confirmatory tests per GPT ruling recorded in completion note §5 |
| `insights[]` retirement decision recorded | SATISFIED | Pre-Sprint 1 §3.6 Final decision; `results.py:155` `manifest_id: "legacy_v1"` still default | Decision to retire is recorded. Implementation is Sprint 4 carriage. Frontend still renders legacy_v1 insights at results/page.tsx:141. Not a gate failure for Sprint 1 but relevant to CHECK 4. |
| `insights[]` retirement STARTED (flag or removal) | OUTSTANDING | `frontend/app/(app)/results/page.tsx:141` still consumes `analysis_result.insights`; `clusterStore.ts:467` still wires it; no feature flag present | Decision recorded but removal NOT started. §3.6 says "Start the removal process now." No removal or feature-flag gating has been initiated. |
| Mock-mode honesty wording decided | SATISFIED | Pre-Sprint 1 §3.7 Final decision: Option B wording approved as written | Decision is closed. |
| Mock-mode honesty implementation | DEFERRED BY DESIGN | §3.7 notes: "Sprint 4 carriage task"; no frontend implementation found | Correctly deferred. Approved wording absent from frontend (`narrativeRuntimePresentation.ts` uses different copy). |
| IDL consumer-surfacing decision | SATISFIED | Pre-Sprint 1 §3.8 Final decision: IDL included in proving surface | Decision closed 2026-05-09. |
| IDL `clinical_only` gate verification | PARTIALLY SATISFIED | `interpretation_display_layer_publish_v1.py:165-179`; `InterpretationPatternsSection.tsx:11-17`; `idl_records_v1.yaml` lines 24-56 (7 `clinical_only` records with `enabled_for_frontend: true`) | The backend publishes `clinical_only` records with `enabled_for_frontend: true`; the consumer component `selectVisibleIdlRecords()` only filters on `enabled_for_frontend` — does NOT exclude `clinical_only` records. §3.8 says this verification is a "Sprint 4 carriage task" but must happen "before IDL records are exposed." IDL is currently live in the consumer path. |
| Layer B → Layer C boundary decided | SATISFIED | Pre-Sprint 1 §3.9 Final decision and full boundary list recorded | Decision is closed permanent authority. |
| Layer B payload richness (§3.9) | PARTIALLY SATISFIED | See Section 4 (dedicated Layer B audit) | First-class fields partly present; critical fields absent from AnalysisDTO; narrative intent and wording boundary fields not built. |
| `validate_llm_output_v2` pre-Sprint-3 review | OUTSTANDING | `backend/core/llm/validator_v2.py` exists; §3.9 notes explicitly: "The guard's validation contract must be reviewed before Sprint 3 authors the Layer C payload." | Guard exists but review against §3.9 boundary list not completed. Validator does not check ranked finding preservation, confidence/banding, hypothesis set integrity, or wording boundaries — the material Sprint 3 risks. |
| Human proving acceptance criteria defined | SATISFIED | Pre-Sprint 1 §3.10: 6 checks approved as written | All 6 binary criteria defined and recorded. |
| Questionnaire minimum proving set | SATISFIED | LC-S2 added statin option; `questionnaire.json` includes `"Statins (cholesterol medication)"` in `long_term_medications` options | Confirmed by `grep` of questionnaire.json. |
| CHECKs 1, 2, 4, 5, 6 (non-gated, Sprint 5) | PARTIALLY SATISFIED | Proving harness run stamp `proving-main-2026-05-10`; lifestyle payoff verified (CHECK 1 directional pass); CHECK 2 (alcohol bridge) not explicitly verified; CHECK 4 (no legacy_v1 visible) not verified; CHECK 5, 6 not verified | Proving harness covers statin and lifestyle invariants but was not structured to test the six §3.10 binary criteria explicitly |
| CHECK 3 (medication modifier visible) | SATISFIED | Proving harness: AB/VR both show `CV consequence_sentence_head` differs statin-on vs statin-off (PASS); `intervention_annotations_v1` absent on statin-off, present on statin-on | Pre-Sprint 2 gate closed; statin wiring confirmed in production path |

---

## 3. Pre-Sprint 2 Compliance Table

| Item | Status | Evidence | Explanation |
|------|--------|----------|-------------|
| Minimal statin questionnaire capture | SATISFIED | `backend/ssot/questionnaire.json` `long_term_medications` options include `"Statins (cholesterol medication)"` | Verified by repo inspection (2026-05-10). Matches `STATINS_LONG_TERM_MEDICATION_LABEL` in `questionnaire_mapper.py:15-16`. |
| CHECK S-1 (questionnaire capture exists) | SATISFIED | `questionnaire.json` option confirmed; unit test `test_s1_questionnaire_ssot_includes_statin_option` referenced in LC-S2 completion | |
| Mapper → `user_intervention_document` (CHECK S-2) | SATISFIED | `questionnaire_mapper.py:71-94` `build_user_intervention_document_for_statin()` method exists; produces `intervention_class_id: lipid_lowering_statin`, `link_status: mapped`; unit test `test_s2_mapper_emits_valid_user_intervention_document` | |
| Annotation compiler resolves statin (CHECK S-3) | SATISFIED | `intervention_annotation_compiler_v1.py:22` `lipid_lowering_statin` in `_APPROVED_INTERVENTION_CLASS_IDS`; test `test_s3_annotation_compiler_resolves_statin` | |
| Pipeline wiring passes annotation through (CHECK S-4) | SATISFIED | `orchestrator.py:1295-1300` passes `user_intervention_document` through to `build_intervention_annotations_v1()`; `AnalysisDTO.intervention_annotations_v1` field present at `results.py:299`; test `test_s4_analysis_dto_field_contract_roundtrip` | |
| User-visible field differs statin-on vs statin-off (CHECK S-5) | SATISFIED | Proving harness output: AB and VR both show `CV consequence_sentence_head` differs between statin-off and statin-on (PASS flag `True` in PROVING_REPORT.md) | |
| No signal state change from statin annotation (CHECK S-6) | SATISFIED | Proving harness: AB and VR top-finding order, signal states, consumer band labels identical statin-off vs statin-on (PASS); test `test_s6_annotation_helpers_do_not_import_signal_pipeline_modules` | |
| Governed statin truth location | SATISFIED | `knowledge_bus/interventions/intervention_effects_registry_v1.yaml:9-35` `lipid_lowering_statin` entry; status LOCKED; cited in Pre-Sprint 2 §4.2 | |
| Statin alias map | SATISFIED | `knowledge_bus/interventions/intervention_class_alias_map_v1.yaml:22-43`; LOCKED | |
| Modifier engine (annotation-parallel, no signal mutation) | SATISFIED | `intervention_annotation_compiler_v1.py` confirmed annotation-parallel; `builders.py:47-53` wires clinician_report with `intervention_annotations_v1`; `domain_score_assembler.py` confirms bands NOT affected | |
| Affected outputs (clinician + consumer) | SATISFIED | `clinician_report_v1.py:99-103` `intervention_annotation_context` field; `consumer_domain_scores` CV `consequence_sentence` carries statin suffix via `format_intervention_annotation_consumer_cv_suffix_v1()` at orchestrator:2240-2242 | |
| Allowed effect type (annotation framing only) | SATISFIED | Registry validator `validate_intervention_effects_registry.py` enforces forbidden keys; SAFETY_CONTRACT_v1.md present; no signal threshold mutation in annotation path | |
| Layer B / Layer C boundary preserved | SATISFIED | Annotation built in Layer B (orchestrator pre-narrative compile); `narrative_report_compiler_v1.py` accepts `intervention_annotations_v1` as parameter and translates to prose appendix only | |
| Production-grade asset rule (no sprint-only stubs) | SATISFIED | Real `user_intervention_document` schema used; real `InterventionAnnotationsV1` contract; real `AnalysisDTO` extension | |
| Statin gate sign-off | SATISFIED | Pre-Sprint 2 §8: "Date closed: 2026-05-09; Gate outcome: closed" | |

---

## 4. Layer B → Layer C Readiness Audit

### What §3.9 actually required

The closed §3.9 contract defines Layer B as providing "the richest deterministic narrative contract possible" across five categories:

1. **Core analytical verdicts** — lead finding, runner-up, ranked findings, domain scores/banding, confidence state, missing-data state, contradiction state
2. **Governed medical reasoning** — hypothesis/WHY set, evidence-for, evidence-against/limiting factors, missing confirmatory markers, pathway/system interpretation, why it matters medically
3. **Personalisation/context outputs that actually fired** — lifestyle modifiers, medication/drug modifiers, body-composition/age/sex context if used, longitudinal context if available, explicit statement of what changed because of those modifiers
4. **Narrative intent** — per-section indication of what prose is trying to do (reassure, prioritise, explain mechanism, express uncertainty, frame next steps, support clinician fast-read)
5. **Wording and claim boundaries** — allowed consumer wording, clinician-only wording, prohibited claims, allowed claim strength ("suggests", "may reflect", "is consistent with")

### What current mainline Layer B actually emits

`AnalysisDTO` (the Layer B output contract, `backend/core/models/results.py:246-302`) carries these first-class fields as of `d9be528`:

| §3.9 Field Group | AnalysisDTO First-Class Fields |
|---|---|
| Core analytical verdicts — domain scores/banding | `consumer_domain_scores: Optional[List[ConsumerDomainScoreV1]]` — includes `band_label`, `score`, `confidence_tier` |
| Governed medical reasoning (hypothesis/WHY sets) | NOT a first-class field. Lives at `meta.insight_graph.report_v1.root_cause_v1` (nested opaque dict) |
| Core analytical verdicts — top findings, rankings, confidence | NOT a first-class field. Lives at `meta.insight_graph.report_v1.top_findings` (nested opaque dict) |
| Clinician surface fields (primary concern, runner-up, chains) | NOT a first-class field on AnalysisDTO. `clinician_report_v1` is assembled in `builders.py:48-53` from `meta.insight_graph.report_v1` at DTO-build time — it is computed post-AnalysisDTO, not a payload field |
| IDL records (pattern-level cross-biomarker interpretation) | `interpretation_display_layer_v1: Optional[InterpretationDisplayLayerBundleV1]` — first-class ✓ |
| Narrative report sections (Layer C assembly product) | `narrative_report_v1: Optional[NarrativeReportV1]` — first-class ✓ |
| Personalisation — medication/drug modifiers | `intervention_annotations_v1: Optional[InterventionAnnotationsV1]` — first-class ✓ (LC-S2) |
| Personalisation — lifestyle modifiers | `lifestyle: Optional[Dict[str, Any]]` — first-class ✓ |
| Personalisation — explicit statement of what changed | Present in `narrative_report_v1` text assembled by compiler; not a structured Layer B field |
| Narrative intent per section | NOT PRESENT anywhere in payload |
| Wording and claim boundaries | NOT PRESENT anywhere in payload |

### What is satisfied

- `consumer_domain_scores` with `band_label`, `score`, `confidence_tier`, and consumer/clinician labels is a proper Layer B first-class field — covers the domain score portion of group 1.
- `interpretation_display_layer_v1` is a proper Layer B first-class field carrying `frontend_allowed_term` (consumer vs clinician routing), severity state, and cross-biomarker interpretation — partially covers groups 1 and 2 at the IDL level.
- `intervention_annotations_v1` is a proper Layer B first-class field — covers group 3 medication modifiers.
- `lifestyle` is present for lifestyle modifier context — covers group 3 lifestyle portion.
- `NarrativeReportV1` sections exist and are populated from governed assets in deterministic_mock mode — the five narrative sections are assembled and available.

### What is partial

- **Core analytical verdicts (group 1):** `top_findings` and `root_cause_v1` are structurally present in `insight_graph.report_v1` (within `meta`) and are accessible to the DTO builder. They are NOT first-class AnalysisDTO fields. `clinician_report_v1` is assembled at the DTO-build layer from `report_v1`, not emitted directly from the analytical pipeline as a Layer B output. This is a boundary ambiguity: the data exists but is not carried as an explicit Layer B contract.
- **Governed medical reasoning (group 2):** `RootCauseV1` with `hypotheses`, `evidence_for`, `evidence_against`, `missing_data`, `confirmatory_tests` is fully populated per `root_cause_v1.py` contract and proven by tests. However it is not a first-class AnalysisDTO field — it requires navigation through `meta.insight_graph.report_v1.root_cause_v1`.
- **Personalisation — explicit change statement (group 3):** The statin annotation produces an `intervention_annotation_context` string in the clinician page1 and a `consequence_sentence` suffix in the cardiovascular consumer domain. These communicate what changed. However the structure is prose-level, not a structured "modifier applied / not applied" field that Layer C can query deterministically by modifier ID.

### What is missing

- **Narrative intent fields (group 4):** No per-section narrative intent coding exists anywhere in the pipeline. `NarrativeReportV1` carries assembled prose fields but no machine-readable intent code (`reassure`, `prioritise`, `explain_mechanism`, `express_uncertainty`, `frame_next_steps`, `support_clinician_fast_read`). Layer C (Gemini path) receives no guidance on what each section is trying to achieve.
- **Wording and claim boundary fields (group 5):** No `allowed_consumer_wording`, `clinician_only_wording`, `prohibited_claims`, or `allowed_claim_strength` fields exist in any contract, YAML, or pipeline output. This is the primary guard against Layer C (Gemini) over-claiming — and it does not exist as a Layer B output.
- **`top_findings`, `root_cause_v1` as explicit Layer B contract fields:** These are required by §3.9 group 1 and group 2 but are not first-class `AnalysisDTO` fields. The Layer C compiler (`narrative_report_compiler_v1.py`) receives `insight_graph` (a Mapping) and `idl_bundle` — it does not receive a typed `top_findings` list or `root_cause_v1` object. This makes the Layer B → Layer C handoff structurally weaker than the §3.9 contract specified.
- **`validate_llm_output_v2` contract review:** The validator (`core/llm/validator_v2.py`) checks numeric invention and red-flag referencing but does NOT verify: (a) ranked finding preservation, (b) confidence/banding preservation, (c) hypothesis set integrity (no new hypotheses invented), (d) wording boundary compliance. These are the four material risks identified in §3.9. The §3.9 notes explicitly required this review before Sprint 3 authors the Layer C payload.

### Whether Sprint 3 can start from current state

**No.** Sprint 3 is the Layer C payload sprint. The §3.9 contract defines what Layer B must provide before Sprint 3 can be authored. The following gaps must be resolved first:

1. `top_findings` and `root_cause_v1` must be promoted to first-class Layer B output fields (or a design decision must be made and recorded that the current `meta.insight_graph.report_v1` path is the approved delivery mechanism, with explicit Layer C compiler signature changes to receive typed objects).
2. Narrative intent codes and wording/claim boundary fields either need to be built or explicitly deferred with a recorded governance decision on how Layer C will be constrained without them.
3. `validate_llm_output_v2` must be reviewed against the §3.9 boundary and its gaps recorded or fixed.

These are pre-Sprint 3 requirements from the signed authority document. They are not new asks.

---

## 5. Genuine Outstanding Items

The following items are genuinely open or partial — not deferred-by-design items presented as failures.

### 5.1 Layer B payload — `top_findings` and `root_cause_v1` not first-class AnalysisDTO fields (OUTSTANDING)

**Gate reference:** Pre-Sprint 1 §3.9 group 1 and group 2.  
**Current state:** Both structures exist in the pipeline but live in `meta.insight_graph.report_v1` (a nested dict). `AnalysisDTO` has no `top_findings` or `root_cause_v1` field. The `narrative_report_compiler_v1.compile_narrative_report_v1()` function signature (`analysis_id, meta, insight_graph, idl_bundle, intervention_annotations_v1`) receives raw dicts, not typed objects for these fields.  
**Evidence:** `backend/core/models/results.py:246-302` (no `top_findings`/`root_cause_v1` field); `backend/core/analytics/narrative_report_compiler_v1.py:526-533` (function signature); `backend/core/dto/builders.py:44` (report_v1 extracted from meta.insight_graph).

### 5.2 Layer B payload — narrative intent and wording boundary fields absent (OUTSTANDING)

**Gate reference:** Pre-Sprint 1 §3.9 groups 4 and 5.  
**Current state:** No `narrative_intent`, `allowed_consumer_wording`, `clinician_only_wording`, `prohibited_claims`, or `allowed_claim_strength` fields exist in any contract or YAML asset.  
**Evidence:** `grep` across `backend/` and `knowledge_bus/` for these terms returns zero results.

### 5.3 `validate_llm_output_v2` contract review not completed (OUTSTANDING)

**Gate reference:** Pre-Sprint 1 §3.9 notes: "The guard's validation contract must be reviewed before Sprint 3 authors the Layer C payload."  
**Current state:** `backend/core/llm/validator_v2.py` checks numeric invention and red-flag referencing. It does NOT check: ranked finding preservation, confidence/banding preservation, hypothesis set integrity, wording boundary compliance.  
**Evidence:** `backend/core/llm/validator_v2.py:110-178`.

### 5.4 IDL `clinical_only` consumer gate not enforced (PARTIALLY SATISFIED)

**Gate reference:** Pre-Sprint 1 §3.8: "`clinical_only` records must be gated from consumer surfaces — this is already defined in the IDL contract."  
**Current state:** `selectVisibleIdlRecords()` in `InterpretationPatternsSection.tsx:11-17` filters only on `enabled_for_frontend === true`. Seven IDL records in `idl_records_v1.yaml` carry `frontend_allowed_term: clinical_only` AND `enabled_for_frontend: true` — these would be rendered to consumer-facing surfaces if their signals fire.  
**Evidence:** `frontend/app/components/results/InterpretationPatternsSection.tsx:16`; `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml:24-56`. §3.8 calls this a "Sprint 4 carriage task" but specifies it must be verified "before IDL records are exposed." IDL records are live in production today.

### 5.5 `insights[]` retirement not started (PARTIALLY SATISFIED)

**Gate reference:** Pre-Sprint 1 §3.6: "Start the removal process now."  
**Current state:** `InsightResult.manifest_id` defaults to `"legacy_v1"` (`results.py:155`). Frontend still consumes `analysis_result.insights` at `results/page.tsx:141`, `actions/page.tsx:62`, `clusterStore.ts:467`. No feature flag gating has been applied.  
**Evidence:** `backend/core/models/results.py:155`; `frontend/app/(app)/results/page.tsx:141`; `frontend/app/state/clusterStore.ts:467`. §3.6 assigned implementation to "Sprint 4 carriage" but said "start the removal process now." No removal or flag has been applied.

### 5.6 CHECK 2 (alcohol bridge in human language), CHECK 4 (no legacy_v1 visible), CHECK 5 (band-headline coherence), CHECK 6 (cross-section lead coherence) not explicitly verified (OUTSTANDING for Sprint 5)

**Gate reference:** Pre-Sprint 1 §3.10.  
**Current state:** The proving harness covers statin invariants and lifestyle payoff. The four remaining binary checks have not been structured into the proving harness output or verified against the binary pass/fail criteria in §3.10. These are Sprint 5 proving items, but the harness should be extended to cover them before Sprint 5.

### 5.7 Clinician `primary_concern` blank in all proving harness runs (OUTSTANDING — OBS-3)

**Gate reference:** Pre-Sprint 1 §3.2 (full proving surface includes `clinician_report_v1`); Pre-Sprint 2 §4.4.  
**Current state:** All 8 proving harness runs show `primary_concern_head: ""`. `clinician_report_v1.sections.page1.primary_concern` is empty across AB and VR panels in the fixture-driven proving runs.  
**Evidence:** `docs/audit-papers/launch-core-proving/latest_fingerprints.json` (all 8 runs `primary_concern_head: ""`); `automation_bus/latest_audit_summary.md OBS-3`. The clinician report compiler is called at DTO-build time from `report_v1` in `meta.insight_graph`; if `report_v1.top_findings` is empty or the compiler logic does not emit `primary_concern` for these fixture runs, the clinician surface is not proving correctly.

---

## 6. Recommended Closure Plan

Minimum bounded tasks before Sprint 3, ordered by priority:

### Task 1 — Layer B contract decision record (Pre-Sprint 3 gate, 1 day)
**Scope:** Architecture decision only, no implementation.  
GPT must make a binding recorded decision on one of two paths:
- **Path A:** Promote `top_findings` and `root_cause_v1` to first-class `AnalysisDTO` fields and update `compile_narrative_report_v1()` signature to accept typed objects.
- **Path B:** Record as a permanent authority decision that `meta.insight_graph.report_v1` is the approved Layer B → Layer C delivery mechanism for these fields, with `compile_narrative_report_v1()` reading them from `insight_graph` as typed dicts. This requires the `insight_graph` parameter shape to be explicitly contractualised.

Either path closes the ambiguity. Sprint 3 cannot be authored without knowing which shape the Layer C compiler will receive.

### Task 2 — Narrative intent and wording boundary decision record (Pre-Sprint 3 gate, 1 day)
**Scope:** Decision only.  
GPT must record whether narrative intent codes and wording boundary fields will be (a) built before Sprint 3 as a minimal schema extension, or (b) explicitly deferred to Phase 1.1 with a recorded acceptance that Sprint 3's Gemini path will be governed by the `validate_llm_output_v2` guard alone (no structural intent/boundary fields). If deferred, this must be a named explicit deferral, not a silent absence.

### Task 3 — `validate_llm_output_v2` gap audit and extension decision (Pre-Sprint 3 gate, 1 day)
**Scope:** Read the validator, document the gaps against §3.9 boundary, decide whether to extend before Sprint 3 or accept as bounded risk.  
Required checks to add or explicitly decline: (a) ranked finding preservation (top finding ID unchanged in output vs prompt), (b) confidence/banding preservation (no invented band shifts in prose), (c) hypothesis set integrity (no hypotheses invented that are not in root_cause_v1), (d) wording boundary compliance (prohibited claims absent from narrative output). At minimum, a recorded decision on each gap.

### Task 4 — IDL `clinical_only` consumer gate (Sprint 4 carriage but immediate risk)
**Scope:** Single-line fix to `selectVisibleIdlRecords()` in `InterpretationPatternsSection.tsx` — add filter `r.frontend_allowed_term !== 'clinical_only'`.  
This is a one-line guard. §3.8 explicitly stated it must be verified before IDL records are exposed to consumers. IDL is live today. This should be treated as a bounded bugfix, not a Sprint 4 carriage item.

### Task 5 — Clinician `primary_concern` investigation (Pre-Sprint 3, bounded)
**Scope:** Diagnose why `clinician_report_v1.sections.page1.primary_concern` is empty in all proving harness runs. This is the clinician surface that Sprint 3 will reference. Sprint 3 cannot author a payload layer that is visibly empty.

### Task 6 — Proving harness extension (Pre-Sprint 5, advisory)
**Scope:** Extend `launch_core_proving_harness.py` to explicitly evaluate CHECKs 2, 4, 5, 6 from §3.10 and report PASS/FAIL. Not a Sprint 3 blocker, but required before Sprint 5 proving.

---

## 7. Files Inspected

### Authority documents
- `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md` — full read
- `docs/planning-papers/healthiq_pre_sprint2_statin_gate_pack_FINAL.md` — full read
- `docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md` — partial (executive summary and principles)

### Sprint completion notes
- `docs/sprints/LC-S1_analytical_hardening_completion_2026-05.md` — full read
- `docs/sprints/LC-S2_context_integration_completion_2026-05.md` — full read
- `docs/sprints/LC-PROVING-HARNESS-AUTOMATION_completion_2026-05.md` — full read
- `docs/sprints/LC-OBS2_completion_2026-05.md` — full read

### Proving outputs
- `docs/audit-papers/launch-core-proving/PROVING_REPORT.md` — full read
- `docs/audit-papers/launch-core-proving/latest_fingerprints.json` — partial read (all 8 run entries)
- `automation_bus/latest_audit_summary.md` — full read (LC-PROVING-HARNESS-AUTOMATION)

### Backend contracts and models
- `backend/core/models/results.py` — full read (AnalysisDTO at lines 246-302; InsightResult at 140-162)
- `backend/core/contracts/narrative_report_v1.py` — full read
- `backend/core/contracts/report_v1.py` — full read (ReportV1, top_findings at line 81, root_cause_v1 at line 85)
- `backend/core/contracts/clinician_report_v1.py` — full read
- `backend/core/contracts/root_cause_v1.py` — full read
- `backend/core/contracts/insight_graph_v1.py` — partial (report_v1 field at line 201)

### Backend pipeline
- `backend/core/pipeline/orchestrator.py` — partial (AnalysisDTO assembly at lines 2245-2265; intervention wiring at 1295-1300)
- `backend/core/dto/builders.py` — full read (build_analysis_result_dto shape; clinician_report compilation at lines 48-53)
- `backend/core/analytics/narrative_report_compiler_v1.py` — partial (compile_narrative_report_v1 signature at lines 526-533; bridge_lines logic at 503-523; wording/intent fields absent)
- `backend/core/analytics/interpretation_display_layer_publish_v1.py` — partial (enabled_for_frontend logic at lines 165-179)
- `backend/core/analytics/interpretation_display_layer_governance_v1.py` — full read (clinical_only at line 71)
- `backend/core/llm/validator_v2.py` — full read (validate_llm_output_v2 at lines 110-178)
- `backend/core/insights/synthesis.py` — partial (validate_llm_output_v2 import confirmed; prompt_json build)
- `backend/core/pipeline/questionnaire_mapper.py` — partial (statin document builder at line 71; medication mapping at 204-223)

### SSOT and knowledge bus
- `backend/ssot/questionnaire.json` — partial (long_term_medications options verified)
- `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml` — partial (frontend_allowed_term and enabled_for_frontend values for all records, lines 8-118)

### Frontend
- `frontend/app/components/results/InterpretationPatternsSection.tsx` — full read (selectVisibleIdlRecords filter logic at lines 11-17)
- `frontend/app/(app)/results/page.tsx` — partial (insights consumption at line 141; IDL usage at lines 155-174)
- `frontend/app/state/clusterStore.ts` — partial (insights wiring at lines 466-467)
- `frontend/app/lib/narrativeRuntimePresentation.ts` — full read (§3.7 wording absent)
- `frontend/app/types/analysis.ts` — partial (frontend_allowed_term type at line 217)
- `frontend/tests/components/InterpretationPatternsSection.test.tsx` — partial (clinical_only test at line 34; confirms filter uses enabled_for_frontend only)

---

## 8. Working Tree Status

**Current branch:** `main`

**Working tree:** Two modified (unstaged) files:
- `docs/audit-papers/launch-core-proving/PROVING_REPORT.md` — M (modified)
- `docs/audit-papers/launch-core-proving/latest_fingerprints.json` — M (modified)
- `frontend/.env.local.example` — M (modified)

No staged changes. Latest commit: `d9be528` — Merge `chore/obs2-sentinel-promotion` into main (2026-05-10).

The two proving files are modified because the harness was likely re-run at the point of audit. This does not affect any of the audit findings — all findings are based on source code and committed documentation, not on re-run artefact content.
