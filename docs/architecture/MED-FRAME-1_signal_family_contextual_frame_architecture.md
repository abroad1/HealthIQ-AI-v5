# MED-FRAME-1 — Signal Family and Contextual Medical Frame Architecture

**Work ID:** `MED-FRAME-1_signal_family_contextual_frame_architecture`  
**Date:** 2026-06-02  
**Status:** Architecture / governance design (non-runtime)  
**Companion draft:** `knowledge_bus/governance/medical_frame_identity_model_draft_v1.yaml` (draft, non-runtime)

---

## Executive summary

HealthIQ must interpret biomarkers through **medically distinct interpretive frames**, not a single flat “marker high/low” meaning. A **signal family** groups all governed frames that share a primary biomarker and clinical domain (for example `signal_creatinine_high`). Each **medical frame** is a bounded, auditable interpretation pathway tied to a canonical research spec and a unique **activation identity**. **Questionnaire** and **medication / drug-category** inputs are structured medical-context modifiers applied in **Layer B** assembly—not optional UX fields and not frontend inference.

This sprint defines the architecture only. No runtime, package, frontend, or evaluator changes were made.

---

## Problem statement

Current promotion work correctly separates Pass_3 research authority from package activation logic, but the product risk is architectural collapse:

- Multiple Pass_3 investigation specs can share one `signal_id` (for example creatinine high with reduced filtration vs albuminuric damage vs electrolyte risk).
- Legacy packages and Pass_3-derived packages can coexist with different override rules and supporting-marker roles.
- Questionnaire and medication context already exist in the codebase (`UserContext`, `backend/ssot/questionnaire.json`, intervention-effects registry) but are not yet formally bound to a **frame + modifier** model that prevents flat-signal interpretation.

Without an explicit frame architecture, future sprints will either:

- collapse distinct medical meanings into one runtime signal, or
- create uncontrolled duplicate authorities for the same activation identity.

---

## Why flat signal modelling is insufficient

A flat model treats `signal_creatinine_high` as one disease claim. Clinically, high creatinine supports **multiple non-equivalent interpretive frames**:

| Frame (illustrative) | Distinct medical question |
|---|---|
| Reduced glomerular filtration | Is filtration reduced? |
| Albuminuric kidney damage | Is there meaningful albuminuria with filtration abnormality? |
| Acute electrolyte risk | Is there dangerous potassium or acute imbalance context? |
| Creatinine distortion | Is creatinine misleading (muscle mass, supplements, hydration)? |
| Medication-associated renal strain | Are nephrotoxic or renal-active drug classes relevant? |

These frames share a biomarker trigger but must not share one co-equal runtime authority or one undifferentiated narrative claim.

---

## Definitions

### Signal family

A **signal family** is the governed grouping of all medical frames that:

- share a `signal_id` (for example `signal_creatinine_high`),
- share a `primary_biomarker_id` (for example `creatinine`),
- belong to one clinical domain / system (for example `renal`).

The family is **not** a runtime evaluator object. It is an architecture index used for collision checks, promotion planning, and Layer B presentation grouping.

### Interpretive medical frame

A **medical frame** is one governed interpretation pathway derived from canonical research (Pass_3 / investigation spec v3) and compiled into package-layer activation artefacts. Each frame has:

- exactly one `research_spec_id` (for example `inv_creatinine_high_reduced_glomerular_filtration`),
- exactly one `activation_key` (`signal_id::research_spec_id`),
- optional package authority (`package_id`) when promoted to runtime,
- biomarker evidence roles (supporting / contradicting / mechanism),
- optional ranked hypotheses (future ROOT_CAUSE layer),
- governed context-modifier hooks (questionnaire + intervention class).

### Frame vs `signal_id`

| Concept | Granularity | Role |
|---|---|---|
| `signal_id` | Coarse | Biomarker-direction trigger label shared across frames |
| Medical frame | Fine | One research-backed interpretation pathway |
| `activation_key` | Runtime identity | Prevents duplicate authority for the same frame |

### Frame vs hypothesis

| Concept | Layer | Purpose |
|---|---|---|
| Medical frame | Package / activation + PSI | Defines activation, supporting markers, override rules, evidence |
| Hypothesis | ROOT_CAUSE / WHY (adjacent) | Ranked explanatory claims *within* or *across* frames |

A frame answers “what clinical pattern is being evaluated?” A hypothesis answers “which explanatory story ranks highest given evidence?” Hypotheses must not replace frame identity or activation keys.

---

## Identity model

Proposed governed identifiers (see draft YAML for machine-readable sketch):

| Identifier | Definition | Example |
|---|---|---|
| `signal_id` | Coarse biomarker-direction signal | `signal_creatinine_high` |
| `signal_family_id` | Family index (typically equals `signal_id` until split needed) | `signal_creatinine_high` |
| `primary_biomarker_id` | Canonical trigger biomarker | `creatinine` |
| `research_spec_id` | Upstream Pass_3 / investigation spec | `inv_creatinine_high_reduced_glomerular_filtration` |
| `activation_key` | Runtime uniqueness: `signal_id::research_spec_id` | `signal_creatinine_high::inv_creatinine_high_reduced_glomerular_filtration` |
| `medical_frame_id` | Stable frame slug (1:1 with research spec in v1) | `frame_creatinine_reduced_glomerular_filtration` |
| `hypothesis_id` | ROOT_CAUSE registry target | `hyp_creatinine_high_ckd` (future) |
| `context_modifier_id` | Governed modifier rule reference | `mod_hydration_low`, `mod_nsaid_exposure` |
| `evidence_role` | Marker role in frame | `corroborator`, `mechanism_marker`, `differential_marker`, `contradiction` |
| `visibility_tier` | Presentation policy | `scored_subsystem`, `hidden_v1`, `detail_only` |
| `presentation_safety_status` | Consumer-safe emission gate | `consumer_safe`, `clinician_only`, `withheld` |

**Relationship rules (v1):**

1. `activation_key` = `signal_id` + `::` + `research_spec_id` (already implemented in `signal_activation_identity_v1.py`).
2. `medical_frame_id` MUST map 1:1 to `research_spec_id` unless an explicit multi-frame package split is approved.
3. Only one runtime package authority per `activation_key`.
4. Multiple frames may share `signal_id` only when `activation_key` differs.

---

## Context modifier model

Context modifiers adjust **interpretation, confidence, explanation, and escalation posture** within a frame. They do not replace frame identity and do not create new activation keys.

### Modifier classes

| Class | Source artefacts (current repo) | Governed by |
|---|---|---|
| Questionnaire context | `backend/ssot/questionnaire.json`, `UserContext`, `questionnaire_mapper.py` | SSOT + Layer B mapping |
| Medication / drug-category | `medications` bands in questionnaire, `intervention_effects_registry` | KB-S48 intervention class registry |
| Biomarker evidence | Package `signal_library` + PSI | Knowledge Bus compile |
| Presentation safety | `visibility_tier`, narrative payload compilers | Architecture policies + Layer B |

### Where modifiers live

```text
Pass_3 canonical research
  → compile → package activation + PSI (frame definition)
  → Layer B assembly applies context_modifier_id rules
  → InsightGraph / NarrativePayload (structured, deterministic)
  → frontend render-only
```

Modifiers MUST NOT be encoded as ad hoc frontend branches or silent evaluator heuristics.

### Questionnaire role

Questionnaire inputs are **structured medical context**, including: age, sex, symptoms (when collected), lifestyle (alcohol, smoking, exercise, hydration, diet, sleep, stress), known conditions, family history, supplements.

Current codebase anchors:

- `backend/core/context/models.py` — `UserContext`
- `backend/core/models/context.py` — `AnalysisContext.questionnaire_responses`
- `backend/core/pipeline/questionnaire_mapper.py` — lifestyle / medical history mapping
- `backend/ssot/questionnaire.json` — governed field definitions

### Medication / drug-category role

Medication context uses **intervention classes**, not brand-level prescribing inference:

- `knowledge_bus/registries/intervention_effects_registry_v1.yaml` (schema: `intervention_effects_registry_schema_v1.yaml`)
- `backend/core/contracts/intervention_annotation_v1.py` — Layer B annotations
- `NarrativePayloadV1` includes `InterventionAnnotationsV1`

Phase-1 boundary (locked): interpretive relevance and caveats only—no threshold mutation or signal firing overrides without a governed HIGH-risk sprint.

---

## Required design questions — explicit answers

1. **What is a signal family?** — Governed grouping of frames sharing `signal_id` + primary biomarker + domain.
2. **What is an interpretive medical frame?** — One research-spec-backed activation pathway with unique `activation_key`.
3. **How does a frame differ from `signal_id`?** — `signal_id` is coarse trigger; frame is spec-scoped medical meaning.
4. **How does a frame differ from a hypothesis?** — Frame defines activation pattern; hypothesis ranks explanatory stories.
5. **How should activation_key / spec_id / hypothesis_id relate?** — `activation_key` binds signal+spec; hypotheses reference frame via `signal_id` / frame index, never replace activation identity.
6. **How do questionnaire inputs modify a frame?** — Via governed `context_modifier_id` rules in Layer B (confidence, caveat, narrative intent, visibility)—not package YAML edits per user.
7. **How do medication inputs modify a frame?** — Via intervention class registry + annotation compiler; caveats and interpretive confounders only in phase 1.
8. **Where should context modifiers live?** — Layer B + governed registries; not frontend; not raw Pass_3 runtime reads.
9. **What should be compiled from Pass_3?** — Package activation, PSI, preservation audit, compile manifest; hypotheses extracted to ROOT_CAUSE when promoted.
10. **What should remain Layer B runtime assembly?** — Personalised weighting of frames, modifier application, conflict/precedence, narrative payload compilation.
11. **What must never be inferred by the frontend?** — Clinical meaning, frame selection, hypothesis ranking, medication effects, or escalation decisions.

---

## Pass_3 / package / compiled artefact relationship

Aligned with `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1`:

```text
Pass_3 canonical research (authority)
  ↓ deterministic compile
package files + promoted_signal_intelligence + compile manifest
  ↓ optional runtime promotion (one activation_key → one package)
SignalRegistry loads packages (activation_key identity)
  ↓
SignalEvaluator (activation + overrides only; no questionnaire logic)
  ↓
Layer B (frames + modifiers + narrative)
  ↓
frontend (render-only)
```

Promotion routes (from KB-MAP-1) remain valid: ROUTE_A single-frame, ROUTE_C multi-frame adjudication, etc. MED-FRAME-1 requires ROUTE_C frames to be explicitly indexed under a signal family before promotion.

---

## Layer B role

Layer B is the **personalisation and contextualisation layer**. It consumes:

- `InsightGraphV1` (deterministic analytical graph),
- signal results (with `activation_key`, `source_spec_id`, `package_id`),
- questionnaire-mapped context,
- intervention annotations,

and produces structured outputs such as `NarrativePayloadV1` for Layer C / frontend.

Layer B may:

- select which **visible** frames to surface,
- apply context modifiers to confidence and narrative intent,
- arbitrate conflicts between frames in the same family.

Layer B must not:

- invent new medical frames,
- merge frames without governed precedence rules,
- read raw Pass_3 JSON at runtime.

---

## Frontend boundary

Frontend components consume compiled DTOs only (`InsightGraph`, report sections, narrative payload views). Existing guardrails (`validate_day_one_architecture.py`) prohibit package/Pass_3 reads and clinical inference in UI code.

Frontend MUST remain **render-only** for frame meaning, modifier effects, and hypothesis ordering.

---

## Worked example: `signal_creatinine_high`

### Signal family

```yaml
signal_family_id: signal_creatinine_high
primary_biomarker_id: creatinine
system: renal
```

### Frames (research-backed; not collapsed)

| medical_frame_id | research_spec_id | activation_key | Current package authority (2026-06-02) |
|---|---|---|---|
| frame_reduced_gfr | inv_creatinine_high_reduced_glomerular_filtration | signal_creatinine_high::inv_creatinine_high_reduced_glomerular_filtration | pkg_kb52c_creatinine_high_reduced_glomerular_filtration |
| frame_legacy_renal_v1 | inv_creatinine_high_renal | signal_creatinine_high::inv_creatinine_high_renal | pkg_s24_creatinine_high_renal |
| frame_albuminuric_damage | inv_creatinine_high_albuminuric_kidney_damage | (future compile) | not yet promoted |
| frame_electrolyte_risk | inv_creatinine_high_acute_electrolyte_risk | (future compile) | not yet promoted |
| frame_creatinine_distortion | inv_creatinine_high_muscle_mass_distortion | (future compile) | not yet promoted |
| frame_medication_renal_strain | inv_creatinine_high_medication_associated_strain | (future compile) | not yet promoted |

Note: Only frames with distinct `research_spec_id` may coexist at runtime. KB-UTIL-2-PROMOTE-WIRE-1 correctly refused activating a Pass_3 candidate duplicate of the kb52c frame.

### Biomarker evidence roles (frame: reduced GFR)

| biomarker | evidence_role | expected_direction |
|---|---|---|
| egfr | corroborator | low |
| uacr | mechanism_marker | high |
| potassium | differential / escalation | context-dependent |
| cystatin_c | differential_marker | high |

### Questionnaire modifiers (examples)

| context_modifier_id | source field | effect on frame |
|---|---|---|
| mod_hydration_low | fluid_intake / hydration | increases uncertainty; flags distortion differential |
| mod_exercise_high | exercise_days_per_week | supports creatinine distortion frame weighting |
| mod_creatine_supplement | supplements | supports distortion frame; not a disease claim |
| mod_known_ckd | medical_conditions | increases confidence in chronic kidney frames |
| mod_diabetes_hypertension | medical_conditions | contextualises cardiorenal risk narrative |

### Medication / drug-category modifiers (examples)

| context_modifier_id | intervention_class | effect |
|---|---|---|
| mod_nsaid_exposure | NSAIDs | caveat + monitoring relevance |
| mod_ace_arb | ACE inhibitors / ARBs | interpretation confounder for creatinine trend |
| mod_diuretic | diuretics | volume/electrolyte context |

### Preventing duplicate co-equal disease claims

Rules:

1. Surface **at most one primary frame** per family in consumer hero narrative unless governed multi-frame policy applies.
2. Secondary frames appear as **context** or **differential**, not parallel disease diagnoses.
3. Activation keys prevent duplicate runtime authorities.
4. Layer B precedence registry resolves same-family conflicts deterministically.

---

## Implications for current creatinine promotion work

| Prior sprint | Implication under MED-FRAME-1 |
|---|---|
| KB-UTIL-2-PROMOTE-PILOT | Correct: promoted candidate as separate package path, not overwrite |
| KB-UTIL-2-ACTIVATION-READINESS | Correct: divergence = behavioural difference, not richness-only |
| KB-UTIL-2-PROMOTE-WIRE-1 | Correct: refused duplicate Pass_3 frame activation; kb52c remains canonical for GFR frame |
| Future promotion | Must index frame in family manifest before activation; legacy s24 retirement requires explicit adjudication sprint |

Creatinine is the reference case for **ROUTE_C multi-frame** planning: compile multiple specs under one family without collapsing activation identity.

---

## Recommended next sprints

| Sprint | Scope |
|---|---|
| **MED-FRAME-2** | Implement medical frame identity index (family → frames → activation keys); wire into promotion and audit tooling |
| **CONTEXT-MOD-1** | Govern questionnaire + intervention-class modifier catalogues; bind modifiers to frame IDs |
| **KB-UTIL-2-CREATININE-AUTHORITY-ADJUDICATION** | Clinical adjudication for legacy s24 vs Pass_3 override divergence (carry-forward from WIRE-1) |

---

## Risks if ignored

- **Flat-signal collapse** — all creatinine findings merge into one misleading diagnosis narrative.
- **Duplicate authority** — multiple packages fight for the same activation key (SignalRegistry collision).
- **Context as UX-only** — questionnaire and medications treated as display text, not medical inputs.
- **Frontend inference drift** — UI starts selecting “what the result means.”
- **Unbounded edge cases** — thousands of future frames added without family index or modifier governance.

---

## Architectural principles preserved

- Do not collapse medically distinct frames into one flat signal.
- Do not create uncontrolled duplicate runtime authority.
- Do not let developers resolve medical truth ad hoc.
- Do not let frontend infer clinical meaning.
- Do not treat questionnaire/drug context as UX-only data.
- Do not manually invent context rules without governance.
- Do preserve medically valid edge cases as structured frames or modifiers.
- Do allow thousands of future edge cases without making runtime chaotic.

---

## Files inspected (evidence)

| Path | Finding |
|---|---|
| `docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md` | Package vs canonical research hierarchy |
| `docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md` | Promotion chain + no raw runtime reads |
| `docs/audit-papers/KB-MAP-1_pass3_to_legacy_package_mapping_and_promotion_plan.md` | ROUTE_A/C promotion routes |
| `docs/audit-papers/KB-UTIL-2-PILOT_pass3_to_runtime_artifact_compiler_pilot_report.md` | Pilot compile boundaries |
| `docs/audit-papers/KB-UTIL-2-PROMOTE-WIRE-1_creatinine_runtime_authority_switch_report.md` | Activation-key collision outcome |
| `knowledge_bus/governance/pass3_legacy_package_mapping_plan_v1.yaml` | Legacy mapping states |
| `knowledge_bus/governance/pass3_promotion_decision_register_v1.yaml` | Promotion decisions |
| `backend/core/knowledge/signal_activation_identity_v1.py` | `activation_key` implementation |
| `backend/core/analytics/signal_evaluator.py` | Package scan + activation evaluation |
| `backend/core/contracts/insight_graph_v1.py` | Layer B → C contract |
| `backend/core/contracts/narrative_payload_v1.py` | Narrative + intervention annotations |
| `backend/ssot/questionnaire.json` | Questionnaire SSOT |
| `knowledge_bus/schema/intervention_effects_registry_schema_v1.yaml` | Medication class registry schema |
| `backend/core/context/models.py` | UserContext fields |

---

## Confirmation

This sprint made **documentation and draft governance artefacts only**. No changes to runtime code, packages, SignalEvaluator, SignalRegistry, frontend, or SSOT behavioural files.
