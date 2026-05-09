# HealthIQ AI — Pre-Sprint 2 Statin Gate Pack

**Date:** 2026-05-09  
**Purpose:** Define and close the statin prerequisite gate before Sprint 2 can be authored or started.  
**Status:** Decisions recorded 2026-05-09 — ready for Anthony sign-off.

---

## How to use this pack

This pack exists because the programme already decided:

- statins are the chosen medication category for proving
- statin prerequisites were explicitly deferred out of Sprint 1
- Sprint 2 cannot begin until the statin path is real, governed, and production-grade

This is a gate pack, not a sprint prompt.

Anthony reviews the populated pack, makes the binding decisions, and closes the gate.

---

## 1. Gate objective

Before Sprint 2 can begin, HealthIQ must have a real statin-aware modifier path that is:

- governed
- deterministic
- user-visible where appropriate
- reusable in the production product
- not a sprint-only shortcut

This gate must answer:

1. how statin use is captured
2. where statin-effect truth lives
3. what engine applies that truth
4. what outputs are allowed to change
5. how success is proved

---

## 2. Decision authority

| Item | Entry |
|---|---|
| Named decision authority | Anthony Broad |
| Operating model | Anthony decides. GPT pressure-tests strategy. Claude Code populates/hardens. Cursor implements. |

---

## 3. Ownership model

| Area | Owner | Notes |
|---|---|---|
| Core engine / modifier architecture | GPT (architecture authority) + Claude Code (hardening/audit) | The annotation architecture already exists; Sprint 2 wires it. |
| Questionnaire / intake capture | Cursor (implementation), with GPT/Claude Code on schema design | Minimal new question or option addition. |
| Frontend / report surface impact | Cursor (implementation) | Clinician surface + all consumer-visible fields naturally affected by statin context. |
| QA/UAT / proving checks | Anthony Broad (per §2.2 of closed Pre-Sprint 1 gate) | As assigned at Pre-Sprint 1 gate closure. |
| Programme/docs coordination | Anthony Broad (or delegate) | Gate record and sign-off. |

---

## 4. Decision register

---

### 4.1 Minimal statin questionnaire capture

**Question:** What is the minimum questionnaire/input capture needed to support a real statin modifier path?

| Field | Entry |
|---|---|
| Owner | Cursor (implementation) |
| **Current state** | `questionnaire.json` `long_term_medications` question (line 146–153) has three options: Corticosteroids, Atypical antipsychotics, HIV/AIDS treatments. **Statins are absent.** `questionnaire_mapper.py` maps `long_term_medications` to `MappedMedicalHistory.long_term_medication_classes` (line 161–165) but this path does not build a `user_intervention_document`. No statin capture exists anywhere in the current questionnaire or mapper. Confirmed by direct file inspection 2026-05-09. |
| **Evidence reviewed** | `backend/ssot/questionnaire.json:146–153`, `backend/core/pipeline/questionnaire_mapper.py:161–165`, `backend/tests/unit/test_questionnaire_mapper.py`. The `user_intervention_document` used by the annotation compiler has a structured schema (`schema_version`, `intervention_records` array with `canonical_class.link_status`, `canonical_class.intervention_class_id`). See `backend/tests/fixtures/user_intervention_exposure/valid_record_set.yaml` for the format. |
| **Alternative considered** | Free-text named drug field with alias map resolution — more powerful (user enters "atorvastatin"), uses the existing alias map at `knowledge_bus/interventions/intervention_class_alias_map_v1.yaml`. But requires more questionnaire real-estate and more mapper complexity. Overkill for proving. |
| **Final decision** | **CLOSED — 2026-05-09.** Add **"Statins (cholesterol medication)"** as a new option to the existing `long_term_medications` checkbox. No standalone statin question. The questionnaire mapper must produce a `user_intervention_document` record with `link_status: mapped`, `intervention_class_id: lipid_lowering_statin` when this option is selected. Named-drug capture with alias resolution is deferred to Phase 1.1. |
| Notes | This reuses the established QRISK-adjacent pattern with zero new questionnaire sections. The mapper bridge from checkbox selection → structured `user_intervention_document` is the key new implementation task — see §7. |

---

### 4.2 Governed statin truth location

**Question:** Where does the governed statin-effect truth live?

| Field | Entry |
|---|---|
| Owner | Knowledge Bus (asset already exists — no new authoring needed) |
| **Current state** | **ALREADY EXISTS, LOCKED, PRODUCTION-GRADE.** `knowledge_bus/interventions/intervention_effects_registry_v1.yaml` contains a complete `lipid_lowering_statin` entry (line 9–35): LDL/non-HDL/ApoB lowering (expected_biomarker_effect), ALT/AST/CK monitoring relevance (monitoring_relevance), HDL caveat (caveat_only). Evidence strength: strong. Citation: ACC/AHA and ESC/EAS guideline class guidance. Physiological rationale present. `knowledge_bus/interventions/intervention_class_alias_map_v1.yaml` is also complete with 11 statin brand-name aliases (atorvastatin, rosuvastatin, simvastatin, lipitor, crestor, etc.). Registry status: `LOCKED`. Confirmed by direct file inspection 2026-05-09. |
| **Evidence reviewed** | `knowledge_bus/interventions/intervention_effects_registry_v1.yaml:9–35`, `knowledge_bus/interventions/intervention_class_alias_map_v1.yaml:22–43`, `knowledge_bus/interventions/SAFETY_CONTRACT_v1.md`, `backend/scripts/validate_intervention_effects_registry.py` (validator confirms all 8 class IDs required including `lipid_lowering_statin`). |
| **Final decision** | **CLOSED — 2026-05-09.** Use the existing governed asset as-is. No new content authoring required. The `lipid_lowering_statin` registry entry is already production-grade. The Pre-Sprint 1 gate assessment that "no governed statin-effect YAML exists" was based on inspection of the caveat assembler path only — the intervention registry was not inspected at that time. |
| Notes | The existing asset is consistent with the Layer B / Layer C boundary — it is deterministic, governed, and annotation-only (no signal threshold mutation). It is already validated by `validate_intervention_effects_registry.py`. |

---

### 4.3 Modifier engine architecture

**Question:** What engine applies statin context?

| Field | Entry |
|---|---|
| Owner | GPT (architecture authority); Cursor (wiring implementation) |
| **Current state** | **ENGINE EXISTS, WIRING MISSING.** `backend/core/analytics/intervention_annotation_compiler_v1.py` is a complete, tested deterministic annotation compiler that: (1) accepts a `user_intervention_document`, (2) loads the intervention effects registry, (3) resolves each record to its canonical class, (4) emits `InterventionAnnotationsV1` with typed effect lists. `lipid_lowering_statin` is in `_APPROVED_INTERVENTION_CLASS_IDS` (line 22). The compiler is proven by unit tests (`test_intervention_annotation_compiler_v1.py`). The `ReportV1` contract already has `intervention_annotations_v1: Optional[InterventionAnnotationsV1]`. The legacy `compile_report_v1()` function already wires the compiler (line 774). However: `compile_narrative_report_v1()` (the orchestrator-called function) does NOT accept `user_intervention_document`. The main orchestrator (`orchestrator.py:2201`) does NOT pass medication context to the compiler. `AnalysisDTO` does NOT carry `intervention_annotations_v1`. The annotations never reach the frontend in the current pipeline. |
| **Evidence reviewed** | `backend/core/analytics/intervention_annotation_compiler_v1.py:20–30` (approved class IDs), `backend/core/analytics/report_compiler_v1.py:32,774,783` (compiler wired in legacy path), `backend/core/analytics/narrative_report_compiler_v1.py:522–528` (no user_intervention_document parameter), `backend/core/pipeline/orchestrator.py:2201–2206` (compile_narrative_report_v1 call — no intervention_document), `backend/core/models/results.py:245–298` (AnalysisDTO — no intervention_annotations_v1 field). |
| **Final decision** | **CLOSED — 2026-05-09.** Wire the existing engine into the production pipeline. Do not build a new engine. Three changes required: (1) pass `user_intervention_document` through the orchestrator to the annotation compiler; (2) expose `intervention_annotations_v1` on `AnalysisDTO` so downstream surfaces can read it; (3) make consumer and clinician surfaces read from the annotation and change content when statin context is active. The engine itself (compiler, registry, alias map, contracts) requires no changes — it is production-grade and governed. |
| Notes | The architecture is annotation-parallel, not a signal modifier. Statin context produces an `InterventionAnnotationsV1` object alongside the existing analysis — it does not change biomarker bands, signal firing, or domain scores. This is consistent with the Layer B / Layer C boundary. The annotation is Layer B truth; Layer C synthesises from it. |

---

### 4.4 Launch-core affected outputs

**Question:** Which launch-core outputs are allowed to change when statin context fires?

| Field | Entry |
|---|---|
| Owner | Cursor (implementation) |
| **Evidence reviewed** | The registry entry for `lipid_lowering_statin` has three effect types: `expected_biomarker_effect` on LDL/non-HDL/ApoB (lower), `monitoring_relevance` on ALT/AST/CK (variable), `caveat_only` on HDL. Both AB and VR panels fire `signal_ldl_cholesterol_high` (AB rank 7) and `signal_apoa1_cardio_risk` (AB rank 5) — where statin context is directly meaningful. Pre-Sprint 1 gate §3.10 CHECK 3: "at least one user-visible field in `consumer_domain_scores`, `lead_narrative`, or `clinician_report_v1.sections.page1` must differ between statin-on and statin-off." |
| **Final decision** | **CLOSED — 2026-05-09.** Clinician surface and all consumer-visible fields that are legitimately affected by statin context. Do not artificially constrain to a single consumer field. Concretely: (1) `clinician_report_v1.sections.page1` — medication context row present when statin annotation resolves, noting expected LDL effect. (2) All consumer surfaces where statin context is naturally relevant — including `consumer_domain_scores[lipid/cardiovascular]` fields and `narrative_report_v1.lead_narrative` when LDL is in the top findings. The annotation must narrate deterministic facts from the governed registry — it must not invent medical reasoning outside what the registry provides. |
| Notes | This decision removes the artificial "one consumer field only" constraint. Statin context should surface wherever it is genuinely meaningful on the launch-core consumer path — not be artificially suppressed to pass a minimal test. CHECK S-5 is satisfied if any one of the approved consumer surfaces differs; the broader carriage is the right production behaviour. |

---

### 4.5 Allowed effect type

**Question:** What kind of change is statin context allowed to make?

| Field | Entry |
|---|---|
| Owner | GPT (architecture authority) |
| **Final decision** | **CLOSED — 2026-05-09.** Statin context may: change interpretation framing on LDL/non-HDL/ApoB readings (noting expected medication-driven lowering), add monitoring context for ALT/AST/CK in the clinician surface, carry an HDL caveat where relevant. Statin context must not: alter biomarker bands, change signal firing thresholds, alter domain scores, alter the lead finding or ranking, add clinical recommendations outside the governed annotation registry. |
| Notes | This is consistent with the Phase-1 boundary in `knowledge_bus/interventions/SAFETY_CONTRACT_v1.md` and the `validate_intervention_effects_registry.py` forbidden-key enforcement (`threshold`, `override_signal`, `signal_state_mutation` etc. are all forbidden). |

---

### 4.6 Boundary with Layer B / Layer C

**Question:** How does statin context respect the Layer B / Layer C boundary?

| Field | Entry |
|---|---|
| Owner | GPT (architecture authority) |
| **Final decision** | **CLOSED — 2026-05-09.** Statin annotation is built entirely in Layer B — it is deterministic, from a governed registry, with no LLM reasoning. Layer C (narrative compiler) may translate the annotation into user-readable language following the wording constraints in the registry. Layer C must not generate statin-related medical reasoning outside what the annotation provides. |
| Notes | This is already consistent with the closed Pre-Sprint 1 §3.9 Layer B → Layer C boundary. The statin modifier outputs that Layer B must hand off are in the approved boundary list under "Personalisation/context outputs that actually fired" → "medication/drug modifiers". |

---

### 4.7 Production-grade asset rule

**Question:** What standard must new statin assets meet?

| Field | Entry |
|---|---|
| Owner | All roles (enforcement) |
| **Final decision** | **CLOSED — 2026-05-09.** No sprint-only stubs. The registry and alias map are already production-grade locked assets — they must not be modified for Sprint 2. New sprint work (questionnaire capture, mapper path, orchestrator wiring, surface changes) must use the real production shapes (real `user_intervention_document` schema, real `InterventionAnnotationsV1` contract, real `AnalysisDTO` extension if needed). No throwaway hardcoded statin flags. |
| Notes | The governed assets (`intervention_effects_registry_v1.yaml`, `intervention_class_alias_map_v1.yaml`, `intervention_annotation_compiler_v1.py`) are LOCKED and must not be changed for Sprint 2 purposes without a new governed sprint. |

---

### 4.8 Proving checks

**Question:** What binary checks must pass before the statin gate is considered closed?

| Field | Entry |
|---|---|
| Owner | Anthony Broad (QA/UAT owner, as per Pre-Sprint 1 §2) |
| **Final decision** | **CLOSED — 2026-05-09. Checks S-1 through S-6 approved as written:** |
| | **CHECK S-1 — Questionnaire capture exists.** `questionnaire.json` `long_term_medications` options include a statin option. Verify by file inspection. → PASS / FAIL |
| | **CHECK S-2 — Mapper produces valid user_intervention_document.** Given a statin-on questionnaire response, the mapper produces a `user_intervention_document` with `intervention_class_id: lipid_lowering_statin` and `link_status: mapped`. Verify by unit test. → PASS / FAIL |
| | **CHECK S-3 — Annotation compiler resolves statin record.** Given the above document, `build_intervention_annotations_v1()` produces an `InterventionAnnotationsV1` with at least one resolved entry for `lipid_lowering_statin`. Verify by unit test. → PASS / FAIL |
| | **CHECK S-4 — Pipeline wiring passes annotation through.** Orchestrator produces a non-None `intervention_annotations_v1` on a statin-on panel run. Verify by integration test or golden-panel run inspection. → PASS / FAIL |
| | **CHECK S-5 — User-visible field differs statin-on vs statin-off.** Run AB panel with statin-on and statin-off profiles. At least one field in `consumer_domain_scores`, `lead_narrative`, or `clinician_report_v1.sections.page1` must differ. This is CHECK 3 from Pre-Sprint 1 §3.10 binary proving checks. → PASS / FAIL |
| | **CHECK S-6 — No signal state change from statin annotation alone.** `top_findings` rankings, `consumer_domain_scores.band_label`, and signal states must be identical between statin-on and statin-off profiles (annotation is parallel, not a signal modifier). Verify by comparison test. → PASS / FAIL |
| Notes | CHECK S-5 is the same as Pre-Sprint 1 CHECK 3, which was gated on this gate closing. Once these six checks pass, CHECK 3 is also unblocked for Sprint 5 proving. |

---

## 5. Verification section

| Item | Status | Notes |
|---|---|---|
| Statin capture path exists in questionnaire | **DOES NOT EXIST** | `questionnaire.json:146–153` — `long_term_medications` has no statin option. Confirmed 2026-05-09. |
| Governed statin truth asset exists | **EXISTS — LOCKED** | `knowledge_bus/interventions/intervention_effects_registry_v1.yaml:9–35` — `lipid_lowering_statin` complete with effects, evidence, rationale, cessation info. Status: LOCKED. |
| Statin alias map exists | **EXISTS — LOCKED** | `knowledge_bus/interventions/intervention_class_alias_map_v1.yaml:22–43` — 11 brand-name aliases. Status: LOCKED. |
| Intervention annotation compiler exists | **EXISTS — TESTED** | `backend/core/analytics/intervention_annotation_compiler_v1.py` — accepts user_intervention_document, resolves to registry, emits InterventionAnnotationsV1. lipid_lowering_statin in approved class IDs at line 22. Unit tests passing. |
| Annotation contract (ReportV1) exists | **EXISTS** | `backend/core/contracts/report_v1.py:86` — `intervention_annotations_v1: Optional[InterventionAnnotationsV1]`. |
| Modifier engine wired in production pipeline | **DOES NOT EXIST** | `orchestrator.py:2201` calls `compile_narrative_report_v1()` with no `user_intervention_document`. Annotations are never built in the production path. Confirmed 2026-05-09. |
| AnalysisDTO carries intervention_annotations_v1 | **DOES NOT EXIST** | `backend/core/models/results.py:245–298` — AnalysisDTO has no `intervention_annotations_v1` field. |
| Questionnaire mapper builds user_intervention_document | **DOES NOT EXIST** | `questionnaire_mapper.py` maps `long_term_medications` to a string list only. No path to user_intervention_document format. |
| Launch-core surface wiring exists | **DOES NOT EXIST** | No surface in `narrative_report_compiler_v1.py`, `consumer_domain_scores`, or any consumer path reads `intervention_annotations_v1` to change output. |
| Statin-on vs statin-off difference proven | **CANNOT BE RUN** | Pipeline wiring missing. |
| No contradiction introduced | **N/A — not testable yet** | Will be verified as part of CHECK S-6 once wiring exists. |
| Layer B / Layer C boundary preserved | **ARCHITECTURE COMPLIANT** | Annotation is a Layer B deterministic construct. Registry forbids threshold mutation, signal state mutation, and override keys. SAFETY_CONTRACT_v1.md exists. |
| LC-S1 gate status | **FAIL — A-1 correction pending** | `automation_bus/latest_audit_summary.md` — gate FAIL on `apoa1_cardio_risk_hypotheses_v1.yaml` (confirmatory test mismatch). Awaiting GPT decision on replacement test IDs, then Cursor correction and re-audit. Sprint 2 gate is independent; LC-S1 correction does not block gate pack population but should be tracked separately. |

---

## 6. Gate closure checklist

| Item | Status | Notes |
|---|---|---|
| Owners assigned | **CLOSED** | Role owners confirmed 2026-05-09. |
| Minimal statin capture decided | **CLOSED — 2026-05-09** | "Statins (cholesterol medication)" added to `long_term_medications`. No standalone question. See §4.1. |
| Governed truth location decided | **CLOSED — 2026-05-09** | Existing `intervention_effects_registry_v1.yaml` — production-grade, no new authoring needed. See §4.2. |
| Modifier engine approach decided | **CLOSED — 2026-05-09** | Wire existing engine — not build a new one. See §4.3. |
| Affected outputs decided | **CLOSED — 2026-05-09** | Clinician surface + all consumer-visible fields naturally affected by statin context. See §4.4. |
| Allowed effect type decided | **CLOSED — 2026-05-09** | Annotation framing only, no signal mutation. See §4.5. |
| Boundary with Layer B / Layer C confirmed | **CLOSED — 2026-05-09** | Annotation is Layer B deterministic by design. Consistent with Pre-Sprint 1 §3.9 authority. See §4.6. |
| Proving checks approved | **CLOSED — 2026-05-09** | Checks S-1 through S-6 approved as written. See §4.8. |
| Verification complete | **CLOSED — current state** | All "does it exist" questions answered from live repo. Outstanding items are Sprint 2 build work. |
| Gate signed off | **READY FOR ANTHONY SIGN-OFF** | All decisions recorded. Anthony signs §8 to close the gate. |

---

## 7. What Sprint 2 actually needs to build

Based on verified current state (2026-05-09):

| Component | State | Sprint 2 Work |
|---|---|---|
| `questionnaire.json` statin option | MISSING | Add option to `long_term_medications` |
| Questionnaire mapper → user_intervention_document | MISSING | Extend mapper to build structured document from statin response |
| Orchestrator pipeline wiring | MISSING | Pass user_intervention_document through to annotation compiler |
| AnalysisDTO.intervention_annotations_v1 | MISSING | Add field (or alternative propagation path) |
| User-visible surface change | MISSING | Wire at least one consumer + clinician surface to read annotation |
| Governed statin truth asset | **EXISTS — LOCKED** | None |
| Statin alias map | **EXISTS — LOCKED** | None |
| Intervention annotation compiler | **EXISTS — TESTED** | None |
| Annotation contracts | **EXISTS** | None |

---

## 8. Final sign-off

| Field | Entry |
|---|---|
| Decision authority | Anthony Broad |
| Sign-off | **All decisions recorded 2026-05-09. Gate is ready for Anthony sign-off.** |
| Date closed |**2026-05-09** |
| Gate outcome |**closed** |
| Notes for Sprint 2 authoring | Once signed: Sprint 2 prompt must reference this gate as prerequisite, cite the five build items in §7 as implementation scope, confirm CHECK S-5 as the minimum proving bar, and treat the existing governed assets (registry, alias map, compiler) as the authoritative starting point — not to be rebuilt. |

---

## 9. Immediate next step after closure

Once this gate is closed, the next artefact is the Sprint 2 work package for launch-core context integration.

Sprint 2 must not be authored until this statin gate is closed.

Sprint 2 prompt must reference:
- this gate as the prerequisite
- the five build items in §7 as the implementation scope
- CHECK S-5 as the minimum proving bar
- the existing governed assets (registry, alias map, compiler) as the authoritative starting point — not to be rebuilt
