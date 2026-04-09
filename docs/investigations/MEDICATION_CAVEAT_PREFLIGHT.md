# Medication / Supplement Caveat Preflight (MEDICATION-CAVEAT-PREFLIGHT)

**work_id:** MEDICATION-CAVEAT-PREFLIGHT  
**mode:** Read-only investigation (no implementation)  
**date:** 2026-04-09  

---

## 1. Executive summary

**What already exists**

- **Strategy (v1.5 adopted plan):** Phase 1 medication handling is explicitly **bounded**. HealthIQ is **not** building a drug library. **Class-level intervention-effects registry** is the intended canonical knowledge shape; **user exposure state** stays separate. Medication context may surface **caveats and interpretation warnings** but **must not** silently alter analytical thresholds or invent medication-specific reasoning unless later governance authorises it (§6.7, §8.4). Wave 5 **BE-S0b** names **medication caveats** alongside subjective behavioural context (§13).
- **SSOT questionnaire (`backend/ssot/questionnaire.json`):**  
  - `current_medications` — **dropdown** (banded count: None / 1–2 / 3–5 / 6+ / prefer not to say).  
  - `long_term_medications` — **checkbox** (None, Corticosteroids, Atypical antipsychotics, HIV/AIDS treatments).  
  - `supplements` — **checkbox** (Multivitamin, Vitamin D, etc., Other, None), `allowOther: true`, **not required**.  
- **Mapping (`backend/core/pipeline/questionnaire_mapper.py`):** `map_submission` → `MappedMedicalHistory` with **distinct** `medications: List[str]` and `supplements: List[str]`, plus conditions, family_history, sleep_disorders, allergies, and **QRISK-style booleans** (atrial fibrillation, RA, SLE, corticosteroids, atypical antipsychotics, HIV treatments, migraines) derived from `medical_conditions`, `long_term_medications`, `regular_migraines`.  
- **Pipeline context:** `create_analysis_context` builds `medical_history` **dict** (subset of mapped fields) and attaches it to **`core.models.context.AnalysisContext`**; **`User.medical_history`** is updated on `user_data`; raw **`questionnaire`** is stored on `User`.  
- **Validation-layer `UserContext` (`backend/core/context/models.py`):** `medications: List[str]` on the **API** user shape — **independent** of the nested `medical_history.medications` from questionnaire mapping unless the route copies them (no dedicated medication merge like waist in current read).  
- **Persistence:** `Analysis.questionnaire_data` JSON stores raw submission; caveat interpretation is not separately persisted as a first-class field in the paths reviewed.  
- **Knowledge asset:** `knowledge_bus/interventions/intervention_effects_registry_v1.yaml` + loaders/validators (aligns with roadmap “class-level registry”); **not** wired from questionnaire free-text in the main orchestrator path reviewed.

**What is missing or weak**

- **No governed medication/supplement caveat** in **`ClinicianReportV1`** (`backend/core/contracts/clinician_report_v1.py`): `confidence_caveat` is **lab/data-quality** scoped only; no structured medication or supplement caveat field.  
- **Insight graph / scoring:** No references to `medical_history`, `medications`, or `supplements` under `backend/core/insight_graph` or `backend/core/scoring` in grep — context is **not** a first-class input to deterministic scoring or IG construction.  
- **Mapper ↔ SSOT mismatch:** `current_medications` is a **dropdown string** in SSOT; mapper uses **`_parse_checkbox_response`**, which wraps a string in a **one-element list** (e.g. `["3-5 medications"]`) — **coarse bands**, not drug identities. Unit tests sometimes use **lists of drug names**, which does **not** match the live SSOT dropdown contract.  
- **QRISK / long-term flags:** `MappedMedicalHistory` includes boolean QRISK-related fields, but **`orchestrator.py`** builds `medical_history` for `AnalysisContext` **without** those fields — they are **mapped then dropped** from the context dict.  
- **Frontend:** `QuestionnaireForm.tsx` mocks align to SSOT-style medication questions; still **mock-driven**, not SSOT-loaded.  

**Is a medication/supplement caveat sprint justified now?**

**Yes — as a deliberately bounded lane**, but **not** as a drug-knowledge expansion. Context-hardening A–C improved contract and behavioural usage; **medication remains the documented next context dimension** (§6.6–6.7, Wave 5 BE-S0b). Repo reality shows **capture + partial mapping + persistence** but **no truthful caveat output path** and **contract gaps** between mapper, context dict, and SSOT types. A sprint is justified only if scoped as **caveat / representation**, not clinical advice or interaction engines.

---

## 2. Strategy interpretation

**What medication/supplement caveat hardening is supposed to do (per adopted roadmap)**

| Intent | Meaning in practice |
|--------|---------------------|
| **Role of medication/supplement context** | Part of the **minimum high-impact context set** for Phase 1 (§6.6); supports interpretation **without** replacing biomarker physics. |
| **Bounded interpretive caveat** | **Primary allowed mechanism:** surface **warnings / interpretation caveats**; align with §6.7 and §8.4. |
| **Not a drug library** | No general drug database, interaction matrix, or dosing logic as product truth in Phase 1. |
| **Class-level registry** | Canonical knowledge = **intervention class** metadata (existing YAML direction), separate from user state. |
| **User state** | Questionnaire / profile exposure — **not** merged silently into thresholds without governance. |
| **Explicitly excluded (unless later authorised)** | Silent threshold changes; medication-specific reasoning chains; unconstrained LLM inference in Layer B. |

**Versus “clinician-only note” / “narrative”**  
Roadmap positions **caveats** in the **deterministic, governable** layer; Layer C narrative is **downstream**. Clinician report contract is a natural **bounded emitter** for caveat text once representation is truthful.

---

## 3. Current audit (evidence-based)

### 3.1 Capture

| Surface | Medication | Supplement | Notes |
|---------|------------|------------|--------|
| `backend/ssot/questionnaire.json` | ✅ Dropdown + long-term checkbox | ✅ Checkbox + Other | Structured / semi-structured; supplements optional |
| `frontend/app/components/forms/QuestionnaireForm.tsx` | ✅ Mock fields aligned to SSOT | ✅ | Not SSOT-driven fetch in reviewed file |
| `frontend/app/lib/mock/questionnaire.ts` | ✅ | ✅ | Defaults e.g. `current_medications: "None"` |
| Analysis API (`AnalysisStartRequest`) | Via `questionnaire_data` / alias | Same | CONTEXT-HARDENING-A transport |
| `core.context.UserContext` | `medications: List[str]` on **user** payload | ❌ No dedicated supplements field on `UserContext` | Supplements live under mapped `medical_history` only on pipeline side |

**E2E status:** **Partial** — raw questionnaire can reach backend and persist; **validation UserContext** does not automatically mirror nested questionnaire `medical_history.supplements` into a top-level supplements field.

### 3.2 Mapping / contract

| Item | Status |
|------|--------|
| `medications` vs `supplements` in mapper | **Distinguished** in `MappedMedicalHistory` and in `medical_history` dict |
| `current_medications` semantics | **Coarse band** (dropdown), not molecule-level |
| QRISK booleans in runtime context | **Partial — computed, not passed** in `orchestrator` `medical_history` dict |
| Canonical registry-like structure | **Intervention-effects registry** exists under `knowledge_bus/`; **not** proven consumed from questionnaire meds in orchestrator `run` |
| Governed enough for next sprint | **Foundation incomplete** — type/field alignment and context completeness must be fixed before caveat **output** can claim truth |

### 3.3 Persistence

| Path | Behaviour |
|------|-----------|
| `PersistenceService.save_live_analysis_after_run` | Stores `questionnaire_data` on `Analysis` |
| `User` / `AnalysisContext` in pipeline | `medical_history` + `questionnaire` on in-memory context |
| Dedicated “caveat” column | **Not identified** in this audit |

### 3.4 Runtime / output usage

| Surface | Uses medication/supplement context? |
|---------|-------------------------------------|
| `AnalysisOrchestrator.create_analysis_context` | **Stores** mapped `medical_history` on context |
| Scoring / clustering / insight graph (grepped subtrees) | **No operational consumption** located |
| `ClinicianReportV1` | **No** medication/supplement caveat fields |
| `confidence_caveat` | **Reference-range / panel** quality only (fixtures + contract) |
| Lifestyle modifier engine | **No** medication inputs in `lifestyle_registry.yaml` reviewed earlier in programme |
| FE results (not exhaustively scraped) | No first-class “medication caveat” panel inferred |

**Verdict:** **Captured and mapped (partially); not consumed** for deterministic analytics or clinician contract caveat lines in the reviewed paths.

---

## 4. Gap ranking

1. **Context contract gap:** QRISK / long-term medication **flags** computed in mapper but **omitted** from `medical_history` passed to `AnalysisContext` — breaks single-source truth for downstream if ever needed.  
2. **SSOT vs mapper gap:** `current_medications` is a **dropdown band**; tests and some assumptions treat **drug-name lists** — **drift risk**.  
3. **Consumer gap:** **No** governed caveat emission in clinician report or IG; medication context is **inert** for user-visible deterministic outputs.  
4. **Split representation:** Pipeline `User.medical_history` holds supplements; validation `UserContext` has **medications** only — **easy desynchronisation** across layers.  
5. **Registry linkage gap:** **Intervention-effects registry** exists but **no** verified E2E path from questionnaire **→** class ID **→** caveat text in this audit.

**Readiness:** **Foundation fixes** should precede or wrap the first **caveat-output** slice; doing output alone would bake in misaligned semantics.

---

## 5. Recommendation

### **SPLIT_INTO_FOUNDATION_AND_CAVEAT_OUTPUT_PHASES**

**Rationale:** Repo reality is **not** “no data”; it is **partial mapping + no consumer + contract holes**. A single combined sprint risks shipping caveat text on top of **dropped QRISK fields** and **dropdown/list ambiguity**. Splitting matches roadmap **§6.7** (bounded caveat, class registry) and **§8.4** (governed context-hardening).

**Phase 1 — Foundation / representation (bounded)**  
- Align `medical_history` dict with **full** governed mapper output (including **long-term / QRISK booleans** if they remain product truth) **or** explicitly document exclusions.  
- Normalize **`current_medications`** handling to SSOT **dropdown** semantics (typed representation, not ambiguous list).  
- Clarify **supplements** on validation `UserContext` vs pipeline-only (minimal change, explicit contract).  
- Optional: thin **intervention-class** bridge from `long_term_medications` **checkbox** labels to registry IDs (**no** free-text inference).  

**Likely touched surfaces:** `questionnaire_mapper.py`, `orchestrator.py` (context assembly), `context` models, `analysis_payload` / route only if contract requires FE/API parity tests — **narrow**.  

**Phase 2 — Caveat output (bounded)**  
- Add **deterministic** caveat strings (or structured caveat DTO) to **`ClinicianReportV1`** or adjacent compiler path, driven only by **Phase-1-normalised** inputs.  
- Regression: compiler + contract tests; **no** LLM in analytical path.  

**If Phase 1 discovers unfixable ambiguity:** escalate to **DO_NOT_PROCEED** for caveat **output** until representation is stable.

---

## 6. Boundary (next sprint must exclude)

Per strategy and this audit, the next medication/supplement workpackage should **not** include:

- Drug interaction engine or proprietary drug knowledge base  
- Speculative medical advice or dosing  
- Symptom inference from medications  
- Broad Layer C narrative generation as the carrier of **primary** medication truth  
- Full supplement ontology or unconstrained free-text reasoning  
- Clinician workspace redesign as the main deliverable  
- Silent changes to scoring thresholds or biomarker cut-offs based on medication alone  

---

## 7. Evidence index (non-exhaustive)

| Topic | Path(s) |
|-------|---------|
| Strategy §6.6–6.7, §8.4, Wave 5 BE-S0b | `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` |
| Question IDs & types | `backend/ssot/questionnaire.json` |
| Mapper + `MappedMedicalHistory` | `backend/core/pipeline/questionnaire_mapper.py` |
| Context assembly | `backend/core/pipeline/orchestrator.py` |
| Pipeline `User` | `backend/core/models/user.py`, `backend/core/pipeline/context_factory.py` |
| Analysis context | `backend/core/models/context.py` |
| API user shape | `backend/core/context/models.py` |
| Clinician contract | `backend/core/contracts/clinician_report_v1.py` |
| Intervention registry | `knowledge_bus/interventions/intervention_effects_registry_v1.yaml`, `backend/core/knowledge/load_intervention_effects_registry_v1.py` |
| FE mock | `frontend/app/components/forms/QuestionnaireForm.tsx`, `frontend/app/lib/mock/questionnaire.ts` |
| Prior context audit | `docs/investigations/CONTEXT_HARDENING_PREFLIGHT.md` |
| Tests | `backend/tests/unit/test_questionnaire_mapper.py`, `backend/tests/integration/test_questionnaire_pipeline_integration.py`, `backend/tests/unit/test_analysis_context_enhancement.py` |

---

## 8. Required closing line

**Final recommendation token:** `SPLIT_INTO_FOUNDATION_AND_CAVEAT_OUTPUT_PHASES`  

**Best-next shape:** **Phase 1** — medication/supplement **representation and context completeness** (mapper + orchestrator + contract alignment); **Phase 2** — **bounded caveat emission** on a deterministic report/compiler path, using Phase-1 outputs only.
