# CONTEXT-MOD-1 — Questionnaire and Medication Modifier Governance

**Work ID:** `CONTEXT-MOD-1_questionnaire_and_medication_modifier_governance`  
**Date:** 2026-06-02  
**Status:** Architecture / governance design (non-runtime)  
**Companion catalogue:** `knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml` (`runtime_consumed: false`)

---

## Executive summary

HealthIQ interpretation depends on biomarker evidence plus structured questionnaire and medication context applied in **Layer B** medical frame assembly—not frontend inference or developer shortcuts. This sprint defines the **modifier governance model** and an initial class-level catalogue. No runtime behaviour, evaluators, or frontend logic were changed.

---

## Strategic context

MED-FRAME-1 defined signal families and contextual frames. MED-FRAME-2 created the governed `medical_frame_identity_index_v1.yaml`. CONTEXT-MOD-1 defines how questionnaire answers, supplements, and medication / drug-category inputs attach to frames as **governed modifiers** with explicit effect types and allowed layers.

```text
biomarker evidence
+ questionnaire context
+ medication / drug-category context
→ medical frames (Layer B)
→ personalised interpretation
→ frontend render-only output
```

---

## Architectural distinctions

| Input class | May influence medical interpretation? | Where allowed |
|---|---|---|
| Biomarker evidence | Yes | Package activation, frame evidence, Layer B assembly |
| Questionnaire lifestyle | Yes (governed) | Layer A normalisation; Layer B when catalogue-bound |
| Questionnaire symptom | Yes (safety/differential) | Layer B brief / safety context |
| Questionnaire known condition | Yes | Layer B frame assembly (medical review often required) |
| Questionnaire family history | Yes (differential only) | Layer B narrative brief; not diagnosis |
| Supplement | Yes (confounder / distortion) | Layer B when catalogue-bound |
| Medication / drug category | Yes | Layer B via intervention registry alignment |
| Demographic (age, sex) | Stratification only | Layer A reference stratification |
| Presentation-only user preference | No | `Not_allowed_for_medical_inference` |

**Presentation-only** inputs (for example health goals, general stress/sleep without clinical linkage) must not select or strengthen medical frames.

---

## Modifier model

Each catalogue row implements the governed modifier record:

| Field | Purpose |
|---|---|
| `modifier_id` | Stable catalogue identifier |
| `modifier_type` | Questionnaire, supplement, medication, demographic class |
| `source_input` | Canonical input path (questionnaire field or registry class) |
| `source_schema_path` | Authority file for the input definition |
| `normalised_value` | Normalised token consumed by future Layer B binder |
| `applies_to` | `signal_family_ids`, `medical_frame_ids`, `biomarker_ids` |
| `modifier_effect` | strengthen, weaken, explain, confidence, safety, suppress overclaiming, etc. |
| `evidence_role` | Role in evidence assembly |
| `direction` | Directional hint for binder |
| `strength` | low / medium / high |
| `clinical_scope` | Clinical domain tag |
| `requires_medical_review` | Whether activation needs medical sign-off |
| `allowed_layer` | Highest layer permitted to consume the modifier |
| `presentation_safety_status` | Safety / wording governance tag |
| `source_authority` | SSOT or registry authority |
| `runtime_active` | Must remain `false` until a promotion sprint |
| `notes` | Governance rationale |

### Allowed `modifier_type` values

`questionnaire_lifestyle`, `questionnaire_symptom`, `questionnaire_known_condition`, `questionnaire_family_history`, `supplement`, `medication_category`, `drug_category`, `demographic`

### Allowed `modifier_effect` values

`strengthens_frame`, `weakens_frame`, `explains_possible_cause`, `increases_confidence`, `decreases_confidence`, `adds_safety_escalation_context`, `adds_differential_context`, `suppresses_overclaiming`, `requires_missing_data_caveat`, `no_interpretive_effect`

### Allowed `allowed_layer` values

`Layer_A_input_normalisation`, `Layer_B_frame_assembly`, `Layer_B_narrative_brief`, `Presentation_safety_only`, `Not_allowed_for_medical_inference`

---

## Creatinine worked example (`signal_creatinine_high`)

Using MED-FRAME-2 indexed frames and MED-FRAME-1 conceptual frames:

### Frame: reduced glomerular filtration

**Governed frame:** `frame_creatinine_reduced_glomerular_filtration`

| Modifier (catalogue) | Effect |
|---|---|
| `mod_creatinine_ctx_known_ckd` | strengthens_frame |
| `mod_creatinine_ctx_diabetes_htn` | strengthens_frame (comorbidity; albuminuric frame not yet indexed) |
| `mod_med_ace_arb`, `mod_med_diuretic` | adds_differential_context |
| `mod_med_nsaid`, `mod_med_nephrotoxic_class` | adds_safety_escalation_context |

### Frame: albuminuric kidney damage (conceptual)

No `medical_frame_id` in the identity index yet. Catalogue rows use **empty** `medical_frame_ids` and document binding in CONTEXT-MOD-2. Relevant modifiers: diabetes/hypertension, UACR availability (`mod_creatinine_ctx_uacr_available`).

### Frame: acute electrolyte risk

**Closest indexed frame:** `frame_creatinine_legacy_s24_potassium_escalation` (inactive runtime authority; adjudication pending per CF-MEDFRAME1-003).

| Modifier | Effect |
|---|---|
| `mod_creatinine_ctx_potassium_high` | adds_safety_escalation_context |
| `mod_med_ace_arb` | adds_differential_context (ACE/ARB + potassium) |
| `mod_creatinine_ctx_known_ckd` | strengthens_frame |

### Frame: creatinine distortion / muscle-supplement context (conceptual)

No indexed `medical_frame_id`. Modifiers: `mod_sup_creatine`, `mod_q_lifestyle_exercise`, `mod_q_hydration`, `mod_creatinine_ctx_high_muscle_mass`, `mod_creatinine_ctx_cystatin_c_available` — effects include `explains_possible_cause`, `suppresses_overclaiming`, `increases_confidence`.

---

## Runtime boundary

- Catalogue: `runtime_consumed: false`, `status: draft_governance_non_runtime`
- Every modifier: `runtime_active: false`
- Validator is standalone; not imported by pipeline
- Identity index `context_inputs_supported.questionnaire_modifiers` / `medication_modifiers` remain `false` until CONTEXT-MOD-2

---

## Related artefacts

| Artefact | Path |
|---|---|
| Catalogue | `knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml` |
| Schema | `knowledge_bus/schema/context_modifier_catalogue_schema_v1.yaml` |
| Validator | `backend/scripts/validate_context_modifier_catalogue.py` |
| Regression tests | `backend/tests/regression/test_context_modifier_catalogue.py` |
| Audit report | `docs/audit-papers/CONTEXT-MOD-1_questionnaire_and_medication_modifier_governance_report.md` |

---

## Next sprint

**CONTEXT-MOD-2** — bind governed context modifiers into Layer B frame assembly and update the medical frame identity index `context_inputs_supported` flags when medically approved.
