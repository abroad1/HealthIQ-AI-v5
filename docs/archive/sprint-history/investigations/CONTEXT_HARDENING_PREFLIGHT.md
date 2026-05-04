# Context hardening preflight — governed non-biomarker inputs

**work_id:** CONTEXT-HARDENING-PREFLIGHT  
**mode:** Read-only repo audit (no implementation)  
**date:** 2026-04-09  

---

## 1. Executive summary

**What already exists**

- **Strategic intent** is explicit: Wave 5 (“Context Hardening Before Narrative”) splits into **BE-S0a** (objective context: waist, BP, height/weight/BMI-related, age/sex gaps) and **BE-S0b** (subjective/behavioural: smoking, alcohol, exercise, sleep, stress, medication caveats). Narrative (Wave 6) is explicitly downstream; context must be governable first (roadmap §12, §13.0, §6.6–6.7, §8.4).
- **Backend data models** already encode a wide “wish list” of non-biomarker fields. `UserContext` in the validation-layer factory includes waist, lifestyle numerics, smoking, medications, family history, etc. (`backend/core/context/models.py`). The **pipeline** `User` model carries age, gender, height, weight, lifestyle_factors, questionnaire, medications (`backend/core/pipeline/context_factory.py` + `backend/core/models/user.py`).
- **SSOT questionnaire** (`backend/ssot/questionnaire.json`) includes demographics, **waist circumference**, **blood pressure** (group field `blood_pressure_reading`), symptoms, conditions, medications, diet/sleep/exercise/smoking/alcohol/stress style coverage, and more.
- **QuestionnaireMapper** can turn validated submissions into structured `MappedLifestyleFactors` and `MappedMedicalHistory` (`backend/core/pipeline/questionnaire_mapper.py`).
- **LifestyleModifierEngine** implements deterministic UK-canonical inputs including `height_cm`, `weight_kg`, `waist_circumference_cm`, `systolic_bp`, `diastolic_bp`, sleep, alcohol, etc. (`backend/core/analytics/lifestyle_modifier_engine.py`).
- **Persistence** stores per-analysis `questionnaire_data` JSON on `Analysis` and optional `demographics` JSON on `Profile` (`backend/core/models/database.py`).

**What is weak or missing (repo-truth)**

- **End-to-end governance is not intact on the live upload/API path.** The frontend sends `questionnaire`; the FastAPI request model only declares `questionnaire_data`. There is no alias — the captured questionnaire is dropped at the API boundary unless clients send the backend field name (`backend/app/routes/analysis.py`).
- **Two different validation contexts exist:** the route uses `core.context.ContextFactory` with `chronological_age` / `height_cm` / `weight_kg`, while the frontend sends `age` / `height` / `weight` (`backend/core/context/context_factory.py`, `frontend/app/upload/page.tsx`). That yields **silent wrong zeros** in the route-level `AnalysisContext` validation object for demographics.
- **Scoring uses the raw `user` dict before questionnaire mapping:** `score_biomarkers` is called with `age=user.get('age')`, `sex=user.get('gender')`, `lifestyle_data=user.get('lifestyle_factors', {})` *before* `create_analysis_context` merges questionnaire-derived `lifestyle_factors` and demographics (`backend/core/pipeline/orchestrator.py`). So even if questionnaire data were present, **lifestyle overlays in the scoring engine would not see mapped questionnaire lifestyle on this path**, and **sex is not read** (`gender` vs `sex`).
- **Layer-2 lifestyle modifiers** in burden propagation only run when `lifestyle_inputs` is passed or `user["lifestyle_inputs"]` is set (`orchestrator.run`); the standard FE payload path does not populate UK-canonical `systolic_bp` / `waist_circumference_cm` etc. from questionnaire responses (and **QuestionnaireMapper does not reference blood pressure or waist** at all).
- **Frontend questionnaire UX** is still largely **mock-driven** (“would fetch from backend”) rather than SSOT-driven (`frontend/app/components/forms/QuestionnaireForm.tsx`).
- **Account/profile product surface** is **identity read-only**; it does not capture or reconcile metabolic context (`frontend/app/(app)/profile/page.tsx`).
- **Results/history UI** does not surface persisted user context as a first-class product view (no matches for rendering stored demographics/questionnaire on results pages in this audit).

**Is context-hardening justified now?**

**Yes.** The roadmap explicitly lists incomplete **governed context consumption** as a current constraint (§6.3–6.4, §6.6, §14). The repo shows substantial **backend affordances** (mapper, modifier engine, SSOT questionnaire) but **fractured contracts and ordering** between capture, validation, scoring, burden modification, and persistence. That is exactly the class of problem Wave 5 / §8.4 describes (formalise first-class inputs, verify mapping, prevent silent drift).

---

## 2. Strategy interpretation

**What “context-hardening” means on the roadmap**

- Non-biomarker inputs are **Layer A substrate**, not “questionnaire decoration” (§2.3, §7.7).
- Minimum Phase 1 context set includes **waist / waist–height relationship**, **blood pressure**, **height/weight/BMI-related inputs**, **medications**, **smoking**, **alcohol**, **exercise**, **sleep**, **stress** (§6.6).
- **Medication** remains **caveat / bounded interpretation**, not a drug library (§6.7).
- **Wave 5** is deliberately **before narrative**: consume context in governed, auditable ways; shrink the gap between collected data and analytical use (§13 “Wave 5 — Context Hardening Before Narrative”).
- Delivery is **already split at strategy level** into **BE-S0a** (objective) and **BE-S0b** (subjective/behavioural) rather than one monolithic “questionnaire tweak.”

**Capability it is meant to unlock**

- Deterministic interpretation that can use **the same context** the user supplied, with **no silent loss** between UI → API → validation → scoring → burden/clinical artefacts → persistence → replay.
- Safer eventual **Layer C** (narrative) because narrative can track structured truth that actually includes context.

**One broad wave vs multiple lanes**

- The roadmap defines **two named backend lanes** (BE-S0a / BE-S0b) plus explicit **product-foundation** work that is now largely advanced per user notes.
- **Repo reality** adds a **prerequisite lane**: **request contract + ordering** must be fixed before “anthropometric” or “BP” lanes can honestly change runtime behaviour.

---

## 3. Current context audit

Legend: **E2E** = captured in FE, sent on analysis request, persisted where applicable, available to pipeline paths that matter; **Partial** = some stages only.

| Category | SSOT / BE models | FE capture | API / validation | Persisted | Runtime use |
|----------|------------------|------------|------------------|-----------|---------------|
| Age | Questionnaire DOB; `User.age`; derived marker injection from DOB in orchestrator | Upload questionnaire | Route `user.age` works for orchestrator; `ContextFactory` expects `chronological_age` (Partial) | `questionnaire_data` if saved | DOB → `simple_biomarkers["age"]` for derived ratios; scoring uses `user.age` |
| Sex / gender | Questionnaire `biological_sex`; pipeline `User.gender` | Upload flow sets `sex` | FE sends `sex`; scoring reads `gender` (**gap**) | If questionnaire saved | Scoring sex overlay **misses** FE `sex` unless questionnaire maps to `gender` later |
| Height / weight | `User.height`/`weight`; `UserContext.height_cm`/`weight_kg` | Questionnaire + payload | Name mismatch for `ContextFactory`; orchestrator `User` uses `height`/`weight` | If questionnaire saved | Used indirectly via user dict for lifestyle engine only if wired; scoring overlays use age/sex/lifestyle_profile |
| BMI / body composition | Lifestyle engine derives BMI / waist-to-height from canonical keys | Not explicit field on FE types | UK-canonical keys not fed from questionnaire mapper | — | Engine capable; **not fed** on main FE path |
| Waist | SSOT `waist_circumference`; `UserContext.waist_cm` | In SSOT; FE mock may omit | Not mapped in `QuestionnaireMapper` | Raw questionnaire only if persisted | **Not mapped** to `waist_circumference_cm` for modifier engine |
| Blood pressure | SSOT `blood_pressure_reading`; engine expects `systolic_bp`/`diastolic_bp` | In SSOT; mapper FE incomplete | No mapper to engine inputs | Raw questionnaire only if persisted | **No mapper**; engine unused for BP from questionnaire |
| Smoking / alcohol / sleep / exercise / stress | Mapper + `UserContext` defaults; LifestyleModifierEngine ranges | Partial in FE mock | Lost if questionnaire not on API | Raw JSON if persisted | **Scoring** uses `lifestyle_factors` **before** questionnaire merge — **not operational** for mapped questionnaire on live path |
| Medications / supplements | Mapper → `MappedMedicalHistory`; `UserContext.medications` | SSOT + mock | Same transport issues | If persisted | Primarily stored on context user; not surfaced as governed caveats in this audit |
| Symptoms | SSOT sections | Mock / partial | Same | Raw JSON | No deterministic “symptom inference” path audited |
| Family history | Mapper + `UserContext.family_history` | SSOT | Same | Raw / mapped in context only if questionnaire runs | Limited downstream use in this audit |
| Goals / interventions | Not a first-class governed field in core DTOs reviewed | Not prominent | — | — | Out of scope for hardened runtime unless tied to intervention registry (§6.7) |

**Contract / persistence**

- **Transient:** Corrected demographics in FE payload `user` object are visible to orchestrator `user` dict, but **questionnaire responses are not** unless `questionnaire_data` is populated at the API.
- **Persisted:** `Analysis.questionnaire_data` and `Analysis.raw_biomarkers` when `save_live_analysis_after_run` succeeds; `Profile.demographics` is a bucket for future use — not populated by this audit’s upload flow review.
- **Validation:** Biomarkers heavily validated; **user/questionnaire consistency across layers is not validated as one contract** (multiple parallel shapes).

**Runtime usage — crisp list**

- **Actually used on main path today (with caveats):** biomarker panel; age from `user.age` for scoring; optional `simple_biomarkers["age"]` from questionnaire DOB for derived ratios **if** `questionnaire_data` is non-null; signal evaluation; clustering; insight graph; clinician report assembly from engine outputs.
- **Captured but not operational for intended behaviour:** full questionnaire-driven lifestyle and medical mapping for **scoring overlays** (ordering gap); **LifestyleModifierEngine** inputs from real user/questionnaire (no UK-canonical bridging from SSOT responses on main path).
- **Planned in SSOT / engine but not wired:** BP and waist (and other objective fields) from questionnaire → modifier engine.

---

## 4. Gap ranking (candidate lanes)

| Lane | Repo maturity | User/product value | Dependency / risk | Ready as *next* bounded sprint? |
|------|----------------|--------------------|-------------------|--------------------------------|
| **A. Analysis request contract + ordering** (FE field names, `questionnaire` vs `questionnaire_data`, `sex` vs `gender`, ContextFactory vs pipeline `User`, score **after** questionnaire merge or dual-pass) | **Low** (active mismatches) | **High** — unblocks all other context work | Touches API + orchestrator + FE; governance risk if analytics touched carelessly | **Yes — highest priority** |
| **B. Anthropometrics / body-composition context** (waist, BMI, waist-to-height; align `UserContext` and engine keys) | Medium (models + engine exist; mapper gaps) | High (roadmap §6.6) | Requires **A** first | After **A** |
| **C. Blood pressure / CV risk context** | Low (SSOT + engine; **no mapper**) | High | Requires **A** + explicit mapping spec | After **A** |
| **D. Lifestyle / smoking / alcohol** (mapper exists; scoring order broken) | Medium | High | Mostly orchestration + validation; beware §8.4 HIGH if analytics core touched | After **A** |
| **E. Medication / supplement caveat layer** | Medium content; bounded policy in §6.7 | Medium–high | Legal/clinical copy + deterministic rules | After **A**; keep class-level registry frame |
| **F. Symptom capture** | SSOT present; no governed inference | Medium | Risk of speculative inference — exclude per governance | Not next |
| **G. FE questionnaire from SSOT + account/profile sync** | Low (mock form) | High for product truth | FE + API; depends on **A** | Parallel after **A** contract frozen |

---

## 5. Recommendation

**Verdict:** `SPLIT_CONTEXT_HARDENING_INTO_FOUNDATION_AND_USAGE_PHASES`

**Rationale (repo-grounded):** There is a clear **transport and sequencing gap** that makes any single “context lane” sprint misleading: objective fields, subjective fields, and the modifier engine **cannot be governed** until the **analysis request contract** is single-sourced and questionnaire data reaches `orchestrator.run` *before* behaviours that should consume it. The roadmap’s BE-S0a / BE-S0b split remains valid, but **Phase 0 (“contract + ordering”)** is mandatory first based on current code paths.

**Best-next single lane (first bounded sprint after this preflight)**

**Lane name:** **Governed analysis-request contract and questionnaire transport (Layer A pre-req)** — objective *and* subjective **payload integrity**, not yet full clinical consumption depth.

**Exact named gaps to close in that sprint**

1. Frontend `questionnaire` ↔ backend `questionnaire_data` (or explicit Pydantic alias + tests).
2. `ContextFactory` user field names vs FE (`age`/`chronological_age`, `height`/`height_cm`, etc.) — one canonical contract.
3. `score_biomarkers` using `gender` while FE sends `sex` — one canonical field or explicit normalisation layer.
4. **Ordering:** map questionnaire → `lifestyle_factors` / demographics **before** scoring **or** re-score with merged context; document deterministic choice.
5. Persistence: ensure `questionnaire_data` is actually populated on real runs so history/replay is truthful.
6. **Defer** BP/waist→engine wiring until payload + mapper spec exists (or include as narrow sub-scope only if contract work stays in same sprint and HIGH risk is declared per §8.4).

**Likely touched surfaces**

- `frontend/app/upload/page.tsx`, `frontend/app/state/analysisStore.ts`, `frontend/app/types/analysis.ts`
- `backend/app/routes/analysis.py`
- `backend/core/context/context_factory.py` (or adapter in route only — minimal touch principle at sprint time)
- `backend/core/pipeline/orchestrator.py` (ordering / normalisation only with explicit risk classification)
- Tests: integration tests for analysis start with questionnaire payload

**Bounded sprint shape**

1. **Sprint 1 — Contract + transport + ordering** (this document’s “best next lane”).
2. **Sprint 2 — BE-S0a-style objective context:** mapper + canonical keys for waist/BP/BMI surfaces feeding `LifestyleModifierEngine` where appropriate.
3. **Sprint 3 — BE-S0b-style subjective/behavioural caveats** aligned to §6.7 and modifier/scoring policy.

---

## 6. Boundary (out of scope for next context-hardening sprint)

Per user constraint and repo state, **exclude unless explicitly re-scoped:**

- New FE shell / account page feature work beyond contract alignment (pages exist; profile remains read-only by design).
- Retail explainer / Layer C narrative production.
- Broad launch marketing copy.
- Clinician workspace as a product surface (clinician report DTO already exists — not the same as workspace).
- Enterprise batch features.
- Unguided full questionnaire UX redesign without SSOT-driven schema fetch.
- Speculative symptom inference or LLM reasoning in the analytical path (forbidden by strategy in any case).

---

## 7. Evidence pointers (non-exhaustive)

| Finding | File(s) |
|--------|---------|
| Wave 5 split BE-S0a / BE-S0b | `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` §13 |
| Request model `questionnaire_data` only | `backend/app/routes/analysis.py` |
| FE sends `questionnaire` | `frontend/app/upload/page.tsx` |
| ContextFactory user key mismatch | `backend/core/context/context_factory.py` (`chronological_age`, `height_cm`, `weight_kg`) vs FE `age`, `height`, `weight` |
| Scoring before questionnaire merge; `gender` vs lifestyle | `backend/core/pipeline/orchestrator.py` (~1161–1177) |
| LifestyleModifierEngine canonical inputs | `backend/core/analytics/lifestyle_modifier_engine.py` |
| Mapper has no BP/waist | `backend/core/pipeline/questionnaire_mapper.py` (no `blood`/`waist` matches) |
| SSOT includes BP, waist, symptoms | `backend/ssot/questionnaire.json` |
| FE questionnaire mock | `frontend/app/components/forms/QuestionnaireForm.tsx` |
| DB columns for questionnaire | `backend/core/models/database.py` (`Analysis.questionnaire_data`) |

---

## 8. Required closing line

**Final recommendation token:** `SPLIT_CONTEXT_HARDENING_INTO_FOUNDATION_AND_USAGE_PHASES`

**Best-next lane:** Governed **analysis request contract + questionnaire transport + orchestrator consumption ordering** (prerequisite to BE-S0a/BE-S0b as named in the roadmap).
