# HealthIQ AI — Pre-Sprint 3 Closure Pack

**Date:** 2026-05-10  
**Status:** Final — all items classified from direct file evidence  
**Branch authored on:** `docs/pre-sprint3-closure-pack`  
**Authority:** Pre-Sprint 1 §3.9 (Layer B → Layer C boundary) is the governing Sprint 3 readiness authority  

---

## 1. Executive Decision

### Sprint 3 may not yet be authored.

Three blocking items must be resolved first. They are bounded and actionable, not speculative:

| # | Blocker | Nature | WP-2 or pre-WP-2 |
|---|---------|--------|------------------|
| B-1 | **Architecture decision on Layer B payload delivery path** (`top_findings`, `root_cause_v1`) | ADR — no code change required | Pre-WP-2 decision only |
| B-2 | **Formal review of `validate_llm_output_v2`** against the §3.9 boundary, with recorded outcome | Review — code extension decision | WP-2 if extension chosen |
| B-3 | **Investigation of blank clinician `primary_concern`** across all proving runs | Investigation + fix | WP-2 |

Two additional items are NOT Sprint 3 blockers but must not be deferred to Sprint 4 without explicit note:

| # | Item | Classification |
|---|------|----------------|
| N-1 | Narrative intent and wording/claim boundary schema | Sprint 3 implements these — not a prerequisite, but a design decision must be made before Sprint 3 is authored |
| N-2 | Minimum proving questionnaire | Not a Sprint 3 blocker; must be addressed before Sprint 5 human proving |

One item is an **immediate hotfix** outside WP-1 and WP-2:

| # | Item |
|---|------|
| H-1 | IDL `clinical_only` consumer gate (`selectVisibleIdlRecords()` — one-line fix) |

---

## 2. Authority Basis

The following documents govern this closure pack, in descending authority order:

1. **Pre-Sprint 1 Decision Pack** (`docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md`) — §3.9 (Layer B → Layer C boundary) is the primary Sprint 3 readiness authority. All five field groups in the approved boundary list are treated as contractual.

2. **Pre-Sprint 2 Statin Gate Pack** (`docs/planning-papers/healthiq_pre_sprint2_statin_gate_pack_FINAL.md`) — gate closed 2026-05-09. All statin checks S-1 through S-6 confirmed passed. This pack's obligations are treated as satisfied.

3. **Launch-Core Transformation Plan** (`docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md`) — Sprint 3 purpose stated as: *"Formalise and implement the governed payload sent from analytical truth to narrative generation."* This means Sprint 3 is expected to implement the payload schema, including fields that do not yet exist. Pre-Sprint 3 obligations are architectural prerequisites and decision clarity, not full implementation.

4. **Gate Compliance Audit** (`docs/audit-papers/gate_compliance_audit_sprint3_readiness.md`, dated 2026-05-10) — used as a starting finding set, but every classification in this pack is independently verified from direct file inspection.

**Principle applied:** Decisions recorded in the Pre-Sprint 1 pack are permanent written authority. Items classified there as "Sprint 4 carriage" are treated as DEFERRED BY DESIGN. Items left without an explicit deferral are treated as OUTSTANDING if the evidence does not show completion.

---

## 3. Compliance Table

### Pre-Sprint 1 items

| Item | Status | Evidence | Judgement |
|------|--------|----------|-----------|
| **§3.1 — Biology slice decided** | SATISFIED | `healthiq_pre_sprint1_decision_pack_FINAL.md §3.1` — CLOSED 2026-05-09; LC-S1 completion note confirms WHY assets added for the named signals | Slice confirmed and implemented. |
| **§3.1 — WHY assets for proving slice** | SATISFIED | `docs/sprints/LC-S1_analytical_hardening_completion_2026-05.md §1-2`; WHY packs added for `hcy_hypotheses_v1`, `mcv_high_hypotheses_v1`, `apoa1_cardio_risk_hypotheses_v1`, `hypercortisolism_hypotheses_v1` | Targeted WHY completion for the proving slice is done per §3.5 decision. |
| **§3.2 — Full proving surface decided** | SATISFIED | Pre-Sprint 1 §3.2 CLOSED; surface includes `narrative_report_v1`, `consumer_domain_scores`, `clinician_report_v1`, IDL | Decision is recorded; surface proven by harness runs. |
| **§3.3 — Medication category decided** | SATISFIED | Pre-Sprint 1 §3.3 CLOSED 2026-05-09; Statins confirmed | Closed. |
| **§3.4 — Statin prerequisites (Option B)** | SATISFIED | Pre-Sprint 2 gate closed 2026-05-09; all six statin checks S-1 through S-6 confirmed passed by harness | Statin gate closed as required. Sprint 2 complete. |
| **§3.4 — Questionnaire minimum proving set** | OUTSTANDING | `backend/ssot/questionnaire.json` contains 55+ required fields across demographics, medical history, symptoms, lifestyle, physical assessment, cognitive assessment, and family history. No reduction has been applied. Pre-Sprint 1 §3.4 explicitly required: *"the questionnaire must be reduced to the minimum proving set so human testing remains practical during this phase."* The proving harness uses fixture data and bypasses the full questionnaire, but human proving (Sprint 5) faces the full 55+ field form. | The proving harness solves automated proving but not human proving. The §3.4 requirement was about human testing practicality. This is not a Sprint 3 blocker, but it must be closed before Sprint 5. See §8 (Non-blockers / deferred). |
| **§3.5 — Silent-WHY policy** | SATISFIED | Pre-Sprint 1 §3.5 CLOSED; LC-S1 delivered targeted WHY assets; fallback suppression policy implemented for out-of-slice signals | Satisfied. |
| **§3.6 — `insights[]` retirement decision** | SATISFIED WITH EXPLICIT DEFERRAL | Pre-Sprint 1 §3.6 CLOSED; retirement decision recorded. `InsightResult.manifest_id` defaults to `"legacy_v1"` at `backend/core/models/results.py:155`; frontend still consumes `analysis_result.insights` at `frontend/app/(app)/results/page.tsx:141`, `actions/page.tsx:62`, `clusterStore.ts:467`. No flag or removal has been applied. | Decision to retire is permanent authority. Implementation explicitly assigned to Sprint 4 carriage. §3.6 said "start the removal process now" — this has not started — but this item does not block Sprint 3 (see §8). |
| **§3.7 — Mock-mode honesty decision** | SATISFIED WITH EXPLICIT DEFERRAL | Pre-Sprint 1 §3.7 CLOSED; Option B wording approved. No implementation exists in frontend. `frontend/app/lib/narrativeRuntimePresentation.ts` uses different copy. | Decision recorded. Implementation is Sprint 4 carriage per §3.7 notes. Not a Sprint 3 blocker. |
| **§3.8 — IDL consumer-surfacing decision** | SATISFIED | Pre-Sprint 1 §3.8 CLOSED; IDL included in proving surface | Decision closed. IDL is live. |
| **§3.8 — IDL `clinical_only` consumer gate** | PARTIALLY SATISFIED | `frontend/app/components/results/InterpretationPatternsSection.tsx:16` — `selectVisibleIdlRecords()` filters only on `r.enabled_for_frontend === true`. No check for `r.frontend_allowed_term !== 'clinical_only'`. The IDL record YAML contains records with `frontend_allowed_term: clinical_only` and `enabled_for_frontend: true`. §3.8 states: *"The `clinical_only` gate must be verified as correctly enforced in the consumer rendering path before IDL records are exposed."* IDL is live today. | **Immediate hotfix.** The gate is not enforced. See §6. |
| **§3.9 — Layer B → Layer C boundary decided** | SATISFIED | Pre-Sprint 1 §3.9 CLOSED 2026-05-09; governing rule and full five-group boundary list recorded as permanent written authority | The decision is closed and authoritative. |
| **§3.9 — Layer B payload richness (groups 1–3)** | PARTIALLY SATISFIED | `backend/core/models/results.py:246-303` confirms: `consumer_domain_scores` (group 1 — domain banding), `interpretation_display_layer_v1` (groups 1–2), `narrative_report_v1` (groups 1–3 assembled), `intervention_annotations_v1` (group 3 — medication), `lifestyle` (group 3 — lifestyle) are first-class `AnalysisDTO` fields. `top_findings`, `root_cause_v1`, and `clinician_report_v1` are NOT first-class fields — they live inside `meta.insight_graph.report_v1` (a nested `Dict[str, Any]`). `compile_narrative_report_v1()` receives `insight_graph: Optional[Mapping[str, Any]]`, not typed objects (`backend/core/analytics/narrative_report_compiler_v1.py:526-533`). | Group 1–3 data exists in the pipeline but its delivery path has an architectural ambiguity. See §4 (full Layer B audit). Architecture decision required before Sprint 3. |
| **§3.9 — Layer B payload richness (group 4 — narrative intent)** | OUTSTANDING | Zero grep hits for `narrative_intent`, `section_intent`, `intent_code` across `backend/` and `knowledge_bus/`. No per-section intent fields exist in any contract, YAML, or pipeline output. | Does not exist. Sprint 3 must implement or explicitly defer. Schema decision required before Sprint 3 is authored. |
| **§3.9 — Layer B payload richness (group 5 — wording/claim boundaries)** | OUTSTANDING | Zero grep hits for `allowed_consumer_wording`, `clinician_only_wording`, `prohibited_claims`, `allowed_claim_strength`, `wording_constraint` across the entire repo. | Does not exist. Sprint 3 must implement or explicitly defer. Schema decision required before Sprint 3 is authored. |
| **§3.9 — `validate_llm_output_v2` pre-Sprint-3 review** | OUTSTANDING | `backend/core/llm/validator_v2.py:110-178` — guard exists. It checks: (a) schema validation (`LLMResultV2`), (b) numeric invention in evidence/actions fields, (c) red-flag ID referencing. It does NOT check: ranked finding preservation, confidence/banding preservation, hypothesis set integrity, or wording boundary compliance. §3.9 notes explicitly: *"The guard's validation contract must be reviewed before Sprint 3 authors the Layer C payload."* No such review has been recorded. | **Sprint 3 blocker.** The review is a named pre-Sprint-3 requirement from the closed authority document. |
| **§3.10 — Binary proving checks defined** | SATISFIED | Pre-Sprint 1 §3.10 CLOSED; 6 checks approved | Checks 1–6 defined as written. |
| **§3.10 — CHECK 3 (statin modifier visible)** | SATISFIED | Proving harness: CHECK S-5 confirmed PASS — AB and VR both show `CV consequence_sentence_head` differs statin-on vs statin-off | Pre-Sprint 2 gate delivered this. CHECK 3 is satisfied. |
| **§3.10 — CHECKs 1, 2, 4, 5, 6 explicitly encoded** | PARTIALLY SATISFIED | Proving harness covers statin invariants and lifestyle payoff (CHECK 1 direction). CHECKs 2, 4, 5, 6 have not been structured as explicit binary pass/fail harness checks. `manifest_id: "legacy_v1"` still present at `results.py:155` means CHECK 4 ("no legacy_v1 manifest entries visible") would fail if run. | Pre-Sprint 5 prep work, not a Sprint 3 blocker. |

### Pre-Sprint 2 items

| Item | Status | Evidence | Judgement |
|------|--------|----------|-----------|
| CHECK S-1 — Questionnaire statin option | SATISFIED | `backend/ssot/questionnaire.json:150` — `"Statins (cholesterol medication)"` present in `long_term_medications` options | Confirmed by direct file inspection. |
| CHECK S-2 — Mapper produces `user_intervention_document` | SATISFIED | `LC-S2_context_integration_completion_2026-05.md` + unit test `test_s2_mapper_emits_valid_user_intervention_document` referenced; `questionnaire_mapper.py` `build_user_intervention_document_for_statin()` exists | Confirmed by sprint completion note. |
| CHECK S-3 — Annotation compiler resolves statin | SATISFIED | `intervention_annotation_compiler_v1.py:22` — `lipid_lowering_statin` in `_APPROVED_INTERVENTION_CLASS_IDS`; unit tests passing | Confirmed. |
| CHECK S-4 — Pipeline wiring passes annotation through | SATISFIED | `AnalysisDTO.intervention_annotations_v1` field present at `results.py:299`; orchestrator wiring confirmed in LC-S2 completion note | Confirmed. |
| CHECK S-5 — User-visible field differs statin-on vs statin-off | SATISFIED | Proving harness PASS: AB and VR `CV consequence_sentence_head` differs between statin-off and statin-on | Confirmed by harness output. |
| CHECK S-6 — No signal state change from statin annotation | SATISFIED | Proving harness: top-finding order, signal states, consumer band labels identical statin-off vs statin-on (PASS) | Confirmed. |
| Governed statin truth location | SATISFIED | `knowledge_bus/interventions/intervention_effects_registry_v1.yaml:9-35` `lipid_lowering_statin` entry; status LOCKED | Confirmed. |
| Statin alias map | SATISFIED | `knowledge_bus/interventions/intervention_class_alias_map_v1.yaml:22-43`; LOCKED | Confirmed. |
| Annotation-parallel modifier (no signal mutation) | SATISFIED | Registry validator `validate_intervention_effects_registry.py` enforces forbidden keys; `SAFETY_CONTRACT_v1.md` exists; no signal threshold mutation in annotation path | Confirmed. |
| Layer B / Layer C boundary preserved for statin | SATISFIED | Statin annotation is built in Layer B (orchestrator pre-narrative compile); annotation translated to prose by `narrative_report_compiler_v1.py` only | Confirmed. |
| Production-grade asset rule | SATISFIED | Real `user_intervention_document` schema, real `InterventionAnnotationsV1` contract, real `AnalysisDTO` extension | Confirmed. |
| Statin gate signed off | SATISFIED | Pre-Sprint 2 §8: closed 2026-05-09 | Confirmed. |

---

## 4. Layer B → Layer C Readiness Audit

This section is a dedicated audit of §3.9. It is the primary gate for Sprint 3 authoring.

### 4.1 What §3.9 actually required

The closed §3.9 contract records the governing rule as: **"Layer B decides. Layer C synthesises."**

Layer B must hand off the richest deterministic narrative contract possible, across five field groups:

**Group 1 — Core analytical verdicts:** lead finding, runner-up, ranked findings, domain scores/banding, confidence state, missing-data state, contradiction state.  
**Group 2 — Governed medical reasoning:** hypothesis/WHY set, evidence-for, evidence-against/limiting factors, missing confirmatory markers, pathway/system interpretation, why it matters medically.  
**Group 3 — Personalisation/context outputs that actually fired:** lifestyle modifiers, medication/drug modifiers, body-composition/age/sex context if used, longitudinal context if available, explicit statement of what changed because of those modifiers.  
**Group 4 — Narrative intent:** per-section indication of what prose is trying to do (reassure, prioritise, explain mechanism, express uncertainty, frame next steps, support clinician fast-read).  
**Group 5 — Wording and claim boundaries:** allowed consumer wording, clinician-only wording, prohibited claims, allowed claim strength ("suggests", "may reflect", "is consistent with").

### 4.2 What current mainline Layer B actually emits

`AnalysisDTO` (`backend/core/models/results.py:246-303`) is the Layer B output contract as of the current `main` state.

**First-class `AnalysisDTO` fields confirmed by direct file inspection:**

| Field | Status | Group coverage |
|-------|--------|----------------|
| `consumer_domain_scores: Optional[List[ConsumerDomainScoreV1]]` | Present (line 295) | Group 1 — domain banding, band_label, headline, confidence_tier |
| `interpretation_display_layer_v1: Optional[InterpretationDisplayLayerBundleV1]` | Present (line 287) | Groups 1–2 — pattern-level cross-biomarker interpretation with severity state and why_it_matters |
| `narrative_report_v1: Optional[NarrativeReportV1]` | Present (line 291) | Groups 1–3 — assembled narrative sections |
| `intervention_annotations_v1: Optional[InterventionAnnotationsV1]` | Present (line 299) | Group 3 — medication/drug modifiers |
| `lifestyle: Optional[Dict[str, Any]]` | Present (line 283) | Group 3 — lifestyle modifier context |
| `meta: Optional[Dict[str, Any]]` | Present (line 278) | Contains `insight_graph.report_v1` which holds `top_findings`, `root_cause_v1`, `clinician_report_v1` as nested dicts |

**Fields that are NOT first-class `AnalysisDTO` fields:**

| §3.9 Requirement | AnalysisDTO field? | Where it lives |
|---|---|---|
| `top_findings` (group 1 — ranked findings, lead, runner-up) | NO | `meta.insight_graph.report_v1.top_findings` (nested dict) |
| `root_cause_v1` (group 2 — hypothesis/WHY set, evidence) | NO | `meta.insight_graph.report_v1.root_cause_v1` (nested dict) |
| `clinician_report_v1` (group 1 — primary concern, confidence, chains) | NO | Assembled at DTO-build time from `meta.insight_graph.report_v1` by `backend/core/dto/builders.py:48-53`; not a Layer B output field |
| Narrative intent codes (group 4) | NO | Absent from codebase entirely |
| Wording / claim boundaries (group 5) | NO | Absent from codebase entirely |

**Layer C compiler function signature** (`backend/core/analytics/narrative_report_compiler_v1.py:526-533`):

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

The compiler receives `insight_graph` as a `Mapping[str, Any]` — an opaque dict. It accesses `top_findings` and `root_cause_v1` by key navigation through this dict, not through typed objects.

### 4.3 What is satisfied

- **Group 1 — Domain-level verdicts:** `consumer_domain_scores` with `band_label`, `score`, `confidence_tier`, `headline_sentence`, `consequence_sentence` is a properly typed first-class `AnalysisDTO` field. The domain-level verdict is a first-class Layer B output. ✓
- **Group 1–2 — Pattern-level cross-biomarker interpretation:** `interpretation_display_layer_v1` is a properly typed first-class field carrying `frontend_allowed_term`, `severity_state`, `why_it_matters`, and `supporting_biomarkers_summary`. ✓
- **Group 3 — Medication modifiers:** `intervention_annotations_v1` is a properly typed first-class field. ✓
- **Group 3 — Lifestyle modifiers:** `lifestyle` is present. ✓
- **Narrative sections assembled:** `NarrativeReportV1` fields are populated from governed assets in `deterministic_mock` mode. The five sections (`retail_summary`, `lead_narrative`, `body_overview`, `next_steps_narrative`, `clinician_synthesis`) are assembled and available. ✓

### 4.4 What is partial

- **Groups 1–2 — Finding-level verdicts and medical reasoning:** The data exists (`top_findings`, `root_cause_v1`, `clinician_report_v1` content), but it is delivered inside `meta.insight_graph.report_v1` — a nested opaque dict — rather than as first-class typed `AnalysisDTO` fields. The §3.9 contract's spirit is that Layer B hands off "the richest deterministic narrative contract possible." An opaque dict is a weaker delivery mechanism than typed first-class fields. However, the data itself is present and accessible.

- **Group 3 — Explicit change statement:** Statin annotation produces an `intervention_annotation_context` string in the clinician surface and a `consequence_sentence` suffix in cardiovascular consumer domain scores. These communicate what changed. But the structure is prose-level rather than a machine-readable "modifier_applied / modifier_not_applied" field that Layer C can query deterministically by modifier ID.

### 4.5 What is missing

- **Groups 1–2 delivery path architectural gap:** `top_findings` and `root_cause_v1` are not first-class `AnalysisDTO` fields. Whether this matters depends on the architectural path chosen (see §4.7). An architecture decision is required before Sprint 3 is authored.

- **Group 4 — Narrative intent:** No per-section intent codes exist anywhere in the codebase (`narrative_intent`, `section_intent`, `intent_code` return zero grep results). Layer C (Gemini path) receives no structured signal about what each narrative section is trying to achieve.

- **Group 5 — Wording and claim boundaries:** No `allowed_consumer_wording`, `clinician_only_wording`, `prohibited_claims`, or `allowed_claim_strength` fields exist anywhere in the codebase. This is the primary structural guard against Layer C over-claiming. It does not exist as a Layer B output.

- **`validate_llm_output_v2` gap — wording and ranking:** `validator_v2.py:110-178` validates schema, numeric invention, and red-flag referencing. It does NOT validate: (a) lead finding ID preservation, (b) ranking/runner-up preservation, (c) banding/confidence preservation, (d) hypothesis set integrity (no invented hypotheses), (e) prohibited claim detection. These are the most material risks when Gemini generates prose from a Layer B payload. §3.9 notes named the review of this guard as a mandatory pre-Sprint-3 step.

### 4.6 Clinician `primary_concern` blank in all proving runs

All 8 proving harness runs show `primary_concern_head: ""`. Source: `docs/audit-papers/launch-core-proving/latest_fingerprints.json` (all 8 run entries).

This matters for Sprint 3 because:
- §3.2 confirmed that `clinician_report_v1.sections.page1.primary_concern` is part of the proving surface
- §3.9 CHECK 6 requires `clinician_report_v1.sections.page1.primary_concern` and `narrative_report_v1.retail_summary` to reference the same lead pattern
- Sprint 3 will design and implement the Layer B payload — if `primary_concern` is blank in the current pipeline, the Layer C payload Sprint 3 authors cannot be validated against it
- The root cause must be investigated before Sprint 3 can proceed

### 4.7 Whether Sprint 3 can start from current state

**No.** Before Sprint 3 is authored, the following must be resolved:

1. **Architectural path decision** on `top_findings` / `root_cause_v1` delivery (Path A or Path B, see §5). Sprint 3's implementation scope depends on this decision.
2. **Schema decision** on whether groups 4 and 5 are implemented in Sprint 3 (recommended) or explicitly deferred with compensating controls recorded.
3. **`validate_llm_output_v2` review** formally completed and gaps recorded or closed.
4. **Clinician `primary_concern` investigation** completed, so Sprint 3 is not authoring payload for a surface that is visibly broken.

These are decisions and investigations, not large implementation tasks. Once made, Sprint 3 can be authored with a clear scope.

---

## 5. Architectural Decision Section

### 5.1 The decision required

§3.9 requires Layer B to hand off the richest deterministic narrative contract. Currently `top_findings` and `root_cause_v1` — the ranked finding list and the hypothesis/WHY set — are not first-class `AnalysisDTO` fields. They are accessible through `meta.insight_graph.report_v1`, which is an opaque `Dict[str, Any]`.

Before Sprint 3 can be authored, the programme must choose one of two paths:

---

**Path A — Promote `top_findings` and `root_cause_v1` to first-class `AnalysisDTO` fields**

What this requires:
- Add `top_findings: Optional[List[TopFinding]]` to `AnalysisDTO` (typed)
- Add `root_cause_v1: Optional[RootCauseV1]` to `AnalysisDTO` (typed)
- Update the orchestrator / DTO builder to populate these fields from `insight_graph.report_v1` at assembly time
- Update `compile_narrative_report_v1()` signature to accept typed objects alongside or instead of raw `insight_graph`

What this delivers:
- Explicit, typed Layer B → Layer C contract matching the spirit of §3.9
- Sprint 3 implementors know exactly what typed objects they receive
- Layer C cannot accidentally access internal graph structures beyond the contracted fields
- Consistent with the programme principle: *"The payload must be the real long-term Layer B → Layer C handoff shape"* (Transformation Plan Sprint 3 Architectural rule)

Cost: moderate — orchestrator and DTO builder changes are required. These are BEHAVIOUR class changes (HIGH risk) and require full work-package governance.

---

**Path B — Formally contract `meta.insight_graph.report_v1` as the approved Layer B delivery path**

What this requires:
- Record as a binding architecture decision that `insight_graph` (specifically `insight_graph.report_v1`) is the contractual Layer B source for `top_findings`, `root_cause_v1`, and `clinician_report_v1` content
- Explicitly define the `insight_graph` dict shape as a first-class contract (not an opaque blob)
- Update `compile_narrative_report_v1()` to accept a typed wrapper for the insight_graph fields it needs, rather than a raw `Mapping[str, Any]`
- Record this as the permanent approved delivery mechanism

What this delivers:
- Avoids structural AnalysisDTO changes and the associated HIGH risk sprint
- The data is already present and working — this path formalises what exists
- Lighter scope for WP-2

Cost: lower — requires documentation and type contractualisation, not structural pipeline changes.

---

### 5.2 Recommended path

**Recommendation: Path A for the long term; Path B as a valid short-term option if bounded correctly.**

The transformation plan is explicit: *"The payload must be the real long-term Layer B → Layer C handoff shape, even if only a bounded subset of content is populated initially."* Path A is the architecturally correct answer — it creates explicit, typed Layer B contracts that Sprint 3 implementors can work against without navigating opaque dicts.

However, Path A requires BEHAVIOUR-class pipeline changes that need a full work package. If the programme needs to author Sprint 3 promptly, Path B is acceptable **only if**:
- The `insight_graph.report_v1` structure is explicitly contractualised (not just accessed as a dict)
- The `compile_narrative_report_v1()` signature is updated to accept typed objects extracted from `insight_graph`
- This decision is recorded in a bounded architecture decision record as the approved short-term path, with a named follow-on task to promote to Path A in Sprint 6

**The programme must choose. This is a binding decision that must be recorded before Sprint 3 is authored.**

---

## 6. Immediate Hotfix Section

### H-1 — IDL `clinical_only` consumer gate (immediate — do not defer to Sprint 4)

**Why it is immediate:**

Pre-Sprint 1 §3.8 states: *"The `clinical_only` gate must be verified as correctly enforced in the consumer rendering path before IDL records are exposed."* IDL records are live in the consumer product today.

**Current gap confirmed:**

`frontend/app/components/results/InterpretationPatternsSection.tsx:11-17`:

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

The filter checks only `enabled_for_frontend === true`. It does NOT filter on `frontend_allowed_term !== 'clinical_only'`. IDL records can carry both `enabled_for_frontend: true` AND `frontend_allowed_term: clinical_only`, which means clinical-only records would be rendered on consumer-facing surfaces today if their signals fire.

**Required fix:** Add `.filter((r) => r.frontend_allowed_term !== 'clinical_only')` to `selectVisibleIdlRecords()`. This is a single-line addition.

**Why it should not wait for Sprint 4:**

Sprint 4 is the "launch-core report carriage" sprint — it is commercial-readiness work. Allowing clinical-only content to reach consumer surfaces before that sprint is a live product risk, not just a pending sprint task. §3.8 named the verification as a prerequisite to IDL exposure, which has already happened. This is a pre-existing live gap, not Sprint 4 scope.

**This fix should be delivered as a standalone bounded hotfix outside WP-1/WP-2.** It does not require a proving harness run and does not affect Layer B output — it is a consumer filter correction.

---

## 7. Non-Blockers / Deferred Items

These items are explicitly NOT Sprint 3 blockers. They are listed here so they are not silently ignored.

| Item | Classification | Rationale |
|------|----------------|-----------|
| `insights[]` retirement implementation | DEFERRED BY DESIGN — Sprint 4 carriage | Pre-Sprint 1 §3.6 explicitly assigned implementation to Sprint 4 carriage. The retirement decision is recorded and permanent. It does not affect the Layer B → Layer C payload that Sprint 3 authors. |
| Mock-mode honesty implementation | DEFERRED BY DESIGN — Sprint 4 carriage | Pre-Sprint 1 §3.7 explicitly assigned Sprint 4 carriage. Wording approved. Not a Sprint 3 payload concern. |
| `insights[]` removal process started | OUTSTANDING | §3.6 said "start the removal process now" and this has not started (`manifest_id` defaults to `"legacy_v1"` at `results.py:155`). However this is not a Sprint 3 blocker. It should be noted in the Sprint 4 prompt as a standing obligation. |
| CHECKs 2, 4, 5, 6 explicitly encoded in harness | PARTIALLY SATISFIED — pre-Sprint 5 prep | The proving harness does not yet explicitly test the §3.10 binary criteria for CHECK 2 (alcohol bridge in human language), CHECK 4 (no legacy_v1 visible), CHECK 5 (no band-headline contradiction), CHECK 6 (cross-section lead coherence). These are Sprint 5 proving requirements, not Sprint 3 concerns. |
| Questionnaire minimum proving set reduction | OUTSTANDING — pre-Sprint 5 requirement | The questionnaire contains 55+ required fields. Pre-Sprint 1 §3.4 required reduction to a minimum proving set for human testing practicality. The proving harness uses fixture data, bypassing the questionnaire for automated proving. But Sprint 5 (human proving) requires Anthony to fill out the form. This must be resolved before Sprint 5 is authored. Not a Sprint 3 blocker. |
| Named-drug capture with alias resolution | DEFERRED BY DESIGN | Pre-Sprint 2 §4.1 explicitly deferred alias-resolution capture to Phase 1.1. Not a Sprint 3 concern. |
| Mock-mode honesty wording | SATISFIED WITH EXPLICIT DEFERRAL | Wording approved at Pre-Sprint 1. Implementation Sprint 4. |

---

## 8. Final Go / No-Go Checklist for Sprint 3 Authoring

This is a binary checklist. Sprint 3 may not be authored until every item is checked.

| # | Check | Status |
|---|-------|--------|
| C-1 | Architecture decision recorded: Path A or Path B for `top_findings` / `root_cause_v1` Layer B delivery | ☐ OPEN |
| C-2 | Schema decision recorded: whether groups 4 and 5 (narrative intent, wording/claim boundaries) are Sprint 3 scope or explicitly deferred with compensating controls named | ☐ OPEN |
| C-3 | `validate_llm_output_v2` review completed: all six §3.9 boundary checks reviewed, gaps recorded, and decision made on whether to extend before Sprint 3 | ☐ OPEN |
| C-4 | Clinician `primary_concern` investigation complete: root cause diagnosed, fix confirmed or documented as a known limitation | ☐ OPEN |
| C-5 | IDL `clinical_only` consumer gate hotfix delivered (H-1) | ☐ OPEN |
| C-6 | Pre-Sprint 2 statin gate confirmed closed (all 6 checks S-1 through S-6 PASS) | ✓ CLOSED |
| C-7 | All Sprint 1 WHY assets for proving slice confirmed in pipeline | ✓ CLOSED |
| C-8 | Layer B `consumer_domain_scores`, `interpretation_display_layer_v1`, `narrative_report_v1`, `intervention_annotations_v1` confirmed first-class fields | ✓ CLOSED |
| C-9 | Mock-mode honesty deferral formally recorded | ✓ CLOSED |
| C-10 | `insights[]` retirement decision recorded | ✓ CLOSED |

**Sprint 3 authoring requires C-1 through C-5 to be checked closed.**

---

## 9. WP-2 Implementation Scope

WP-2 is the bounded pre-Sprint 3 closure work package. It is defined here for scoping purposes only. The Sprint 3 prompt must not be authored until WP-2 is complete and this checklist C-1 through C-5 is closed.

### WP-2 task list (minimum bounded scope)

**WP-2-T1 — Architectural decision record** (docs only — no code)
- GPT records: Path A or Path B for `top_findings` / `root_cause_v1`
- If Path A: WP-2 includes the AnalysisDTO extension as a BEHAVIOUR sprint
- If Path B: WP-2 documents the `insight_graph.report_v1` contract explicitly; `compile_narrative_report_v1()` signature may be updated to accept typed wrapper objects
- Deliverable: ADR recorded in `/docs/architecture/` or equivalent

**WP-2-T2 — Narrative intent and wording boundary schema decision** (docs only — no code)
- GPT records: whether groups 4 and 5 are Sprint 3 scope (recommended) or deferred
- If Sprint 3 scope: define the minimum schema (field names, types, example values) so Sprint 3 can be authored with a complete picture
- If deferred: name the compensating control (e.g., the extended `validate_llm_output_v2` guard alone, plus an explicit statement that Gemini path is not enabled until Phase 1.1)
- Deliverable: schema sketch or deferral decision recorded

**WP-2-T3 — `validate_llm_output_v2` gap review and extension decision** (investigation + optional code)
- Review `backend/core/llm/validator_v2.py` against the §3.9 boundary
- The six checks to review: (a) lead finding ID preservation, (b) ranking/runner-up preservation, (c) banding/confidence preservation, (d) hypothesis set integrity, (e) prohibited claim detection, (f) numeric invention (already implemented)
- Record decision on each: mandatory-before-Sprint-3, or explicitly accepted as bounded risk with rationale
- If any checks are mandatory: implement them as a LOW-risk sprint
- Deliverable: review record + optional test additions

**WP-2-T4 — Clinician `primary_concern` investigation and fix** (investigation + code)
- Diagnose why `primary_concern` is blank across all 8 proving harness runs
- This requires reading `builders.py`, `clinician_report_v1.py`, and the `insight_graph.report_v1` structure as produced by the orchestrator for the AB/VR fixture panels
- Fix if the root cause is clear and bounded
- If the fix is BEHAVIOUR class: it requires a full HIGH-risk work package
- Deliverable: diagnosis note + fix or investigation record confirming the clinician surface works

**WP-2-T5 — IDL `clinical_only` consumer gate hotfix** (code — single-line)
- Deliver as a standalone bounded fix
- Branch: `fix/idl-clinical-only-consumer-gate`
- Change: `InterpretationPatternsSection.tsx:16` — add `&& r.frontend_allowed_term !== 'clinical_only'` to the filter
- Deliverable: merged fix before Sprint 3 is authored

### WP-2 scope boundary

WP-2 does NOT include:
- Sprint 4 carriage work (`insights[]` retirement, mock-mode honesty wording)
- Questionnaire reduction (pre-Sprint 5)
- Proving harness extensions for CHECKs 2, 4, 5, 6 (pre-Sprint 5)
- Any frontend redesign
- Wave 2 WHY expansion
- Any change to the analytics engine, SSOT, or Knowledge Bus outside the investigation scope

---

## 10. Files Inspected

### Authority documents (read in full)
- `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md`
- `docs/planning-papers/healthiq_pre_sprint2_statin_gate_pack_FINAL.md`
- `docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md`
- `docs/audit-papers/gate_compliance_audit_sprint3_readiness.md`

### Sprint completion notes (read in full)
- `docs/sprints/LC-PROVING-HARNESS-AUTOMATION_completion_2026-05.md`

### Core contracts and models (read directly)
- `backend/core/models/results.py` (lines 140–162, 246–303) — `InsightResult`, `AnalysisDTO`
- `backend/core/analytics/narrative_report_compiler_v1.py` (lines 520–533) — `compile_narrative_report_v1()` signature
- `backend/core/llm/validator_v2.py` (full — 180 lines) — `validate_llm_output_v2()` implementation
- `frontend/app/components/results/InterpretationPatternsSection.tsx` (lines 1–30) — `selectVisibleIdlRecords()`
- `backend/ssot/questionnaire.json` (full — 536 lines) — all question fields

---

## 11. Working Tree Status

**Branch at time of authoring:** `docs/pre-sprint3-closure-pack` (created from `main` at commit `d9be528`)

**Working tree status:**
- Two modified (unstaged) files present on `main` before branching: `docs/audit-papers/launch-core-proving/PROVING_REPORT.md`, `docs/audit-papers/launch-core-proving/latest_fingerprints.json` — these are proving-run artefacts and do not affect any audit finding in this pack
- `frontend/.env.local.example` — M (modified, pre-existing)
- This file (`healthiq_pre_sprint3_closure_pack_FINAL.md`) is a new addition under `/docs/` only

**No files outside `/docs/` were touched.**
