# BATCH2-CONTEXT-MOD-1 — Androgen-Panel Context Modifier Binding

**Work ID:** `BATCH2-CONTEXT-MOD-1_androgen_panel_context_modifier_binding`  
**Date:** 2026-06-06  
**SOP:** AUTOMATION_BUS_SOP_v1.3.1

---

## Executive verdict

**PASS (governance binding only).** All **8/8** androgen-panel frames have `context_modifier_dependency: true` in the promotion-readiness register. **8/8** frames documented in `batch2_androgen_context_modifier_binding_v1.yaml` with catalogue modifier links. **4** new governance placeholder modifiers added; **10** existing modifiers linked to androgen `medical_frame_ids`. Frame index `context_inputs_supported` flags updated for all 8 frames. **Zero** package/runtime/frontend changes. Androgen promotion **remains blocked** pending CF-BATCH2-010 clinical signoff and CF-CONTEXT-MOD-3 runtime evaluation. Architecture gate **PASS**.

---

## Artefacts inspected

| Artefact | Purpose |
|----------|---------|
| `knowledge_bus/governance/batch2_androgen_panel_medical_review_v1.yaml` | Medical review outcomes and context dependencies |
| `knowledge_bus/governance/batch2_promotion_readiness_register_v1.yaml` | Corrected `context_modifier_dependency` flags |
| `knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml` | Modifier links and new placeholders |
| `knowledge_bus/governance/medical_frame_identity_index_v1.yaml` | Context input flags |
| `docs/audit-papers/BATCH2-MEDREVIEW-1_androgen_panel_medical_review.md` | Prior review baseline |
| `knowledge_bus/packages/pkg_kb47_dhea_*`, `fai_*`, `free_testosterone_*`, `free_testosterone_pct_*` | Read-only package inspection |

**Created:** `knowledge_bus/governance/batch2_androgen_context_modifier_binding_v1.yaml`

---

## 8-frame context dependency table

| frame_id | medical review outcome | catalogue links | remains blocked |
|----------|------------------------|-----------------|-----------------|
| frame_batch2_dhea_high_androgen_excess_context | MEDICALLY_COHERENT_BUT_CONTEXT_DEPENDENT | 8 modifiers | yes |
| frame_batch2_dhea_low_adrenal_androgen_reduction | MEDICALLY_COHERENT_BUT_CONTEXT_DEPENDENT | 6 modifiers | yes |
| frame_batch2_fai_high_biochemical_hyperandrogenism | BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING | 9 modifiers | yes |
| frame_batch2_fai_low_reduced_free_androgen_availability | BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING | 8 modifiers | yes |
| frame_batch2_free_testosterone_high_androgen_excess_context | MEDICALLY_COHERENT_BUT_CONTEXT_DEPENDENT | 8 modifiers | yes |
| frame_batch2_free_testosterone_low_androgen_deficiency_context | MEDICALLY_COHERENT_BUT_CONTEXT_DEPENDENT | 7 modifiers | yes |
| frame_batch2_free_testosterone_pct_high_elevated_free_androgen_fraction | BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING | 6 modifiers | yes |
| frame_batch2_free_testosterone_pct_low_reduced_free_androgen_fraction | BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING | 5 modifiers | yes |

Full per-frame fields: `knowledge_bus/governance/batch2_androgen_context_modifier_binding_v1.yaml`.

---

## Promotion-readiness register correction

For all 8 androgen-panel packages:

- `context_modifier_dependency: true` (was `false`)
- `medical_review_required: false` (CF-BATCH2-005 resolved)
- Summary counts updated: `BLOCKED_PENDING_MEDICAL_REVIEW: 0`, `BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING: 4`, `READY_WITH_DOCUMENTED_CAUTION: 14`

Per-frame status (promotion still blocked):

| Frames | promotion_readiness_status |
|--------|----------------------------|
| dhea (2), free_testosterone (2) | READY_WITH_DOCUMENTED_CAUTION (caution-gated; not promotion-authorised) |
| fai (2), free_testosterone_pct (2) | BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING (runtime Layer B evaluation still pending) |

---

## Context modifier catalogue changes

### Existing modifiers linked to androgen frames

| modifier_id | frames linked |
|-------------|---------------|
| mod_demo_age | all 8 |
| mod_demo_sex | all 8 |
| mod_q_symptoms | all 8 |
| mod_q_known_conditions | all 8 |
| mod_sup_testosterone | all 8 |
| mod_med_testosterone_hormone | all 8 |
| mod_med_steroid | all 8 |
| mod_med_thyroid | SHBG-related + free_testosterone frames |
| mod_med_hepatotoxic_class | SHBG-related frames |
| mod_q_stress | dhea_low adrenal frame |

### New governance placeholders (runtime_active: false)

| modifier_id | purpose |
|-------------|---------|
| mod_androgen_ctx_shbg_governance | SHBG-dependent fraction interpretation context |
| mod_androgen_ctx_lh_governance | LH gonadal-axis context |
| mod_androgen_ctx_adrenal_stress | Adrenal/stress context for DHEA-low |
| mod_androgen_ctx_aas_exposure | Anabolic-androgenic supplement exposure placeholder |

All modifiers remain `runtime_active: false`. Catalogue remains `runtime_consumed: false`.

---

## Medical frame index changes

For all 8 androgen-panel frames:

```yaml
context_inputs_supported:
  biomarker_evidence: true  # unchanged
  questionnaire_modifiers: true  # was false
  medication_modifiers: true  # was false
```

`promotion_state`, `runtime_authority_status`, and `clinical_adjudication_status` unchanged.

---

## Missing modifier governance

Tracked per frame in binding register:

| Gap | Frames affected |
|-----|-----------------|
| fsh_governance | all 8 (FSH not in catalogue) |
| runtime_layer_b_evaluation | all 8 (CF-CONTEXT-MOD-3) |
| cortisol_acth_runtime_binding | dhea_low |
| overlap_adjudication | free_testosterone_pct high/low vs free_testosterone frames |

---

## Remaining medical sign-off requirements

**CF-BATCH2-010 remains Open.** All 8 frames retain:

- `clinical_adjudication_status: required_before_activation`
- `promotion_state: compiled_not_promoted`
- `runtime_authority_status: inactive`

No androgen package promotion authorised.

---

## Carry-forward updates

| ID | Action |
|----|--------|
| CF-BATCH2-009 | **Resolved** — governance binding complete |
| CF-BATCH2-010 | **Open** — clinical signoff before activation |
| CF-CONTEXT-MOD-3 | **Open (new)** — runtime Layer B modifier evaluation |
| CF-BATCH2-006 | Remains Open |
| CF-BATCH2-008 | Remains Open |

---

## Validation output (full)

### Architecture gate

```powershell
python backend/scripts/run_architecture_validation_gate.py
```

```text
[architecture-gate] validate_medical_frame_identity_index
[architecture-gate] validate_context_modifier_catalogue
[architecture-gate] validate_day_one_architecture
[architecture-gate] validate_medical_intelligence_architecture
[architecture-gate] pytest_architecture_guardrails
[architecture-gate] pytest_governance_regression
architecture_validation_gate: PASS
day_one_architecture_validation: PASS
medical_intelligence_architecture_validation: PASS
.......s..                                                               [100%]
SKIPPED [1] backend\tests\architecture\test_medical_intelligence_architecture_sentinels.py:67
.....................                                                    [100%]
```

### Medical frame identity index

```powershell
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

```text
validation_status: PASS
errors: 0
```

### Context modifier catalogue

```powershell
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

```text
validation_status: PASS
errors: 0
```

### Regression tests

```powershell
python -m pytest backend/tests/regression/test_context_modifier_catalogue.py -q
python -m pytest backend/tests/regression/test_med_frame_identity_index.py -q
```

```text
..........                                                               [100%]
...........                                                              [100%]
```

---

## Runtime boundary confirmation

**Confirmed:** No changes to SignalEvaluator, SignalRegistry, runtime loaders, domain_score_assembler, report_compiler, frontend, SSOT, scoring thresholds, unit conversion, `knowledge_bus/packages/*`, or `knowledge_bus/current/latest_knowledge_status.json`.

Governance-only deliverables: binding register, catalogue links, promotion register correction, frame index flags, audit report, carry-forward update.
