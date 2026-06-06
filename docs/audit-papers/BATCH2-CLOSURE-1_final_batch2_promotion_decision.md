# BATCH2-CLOSURE-1 — Final Batch 2 Promotion Decision

**Work ID:** `BATCH2-CLOSURE-1_final_batch2_promotion_decision`  
**Date:** 2026-06-06  
**SOP:** AUTOMATION_BUS_SOP_v1.3.1

---

## Executive verdict

**PASS (governance consolidation only).** All **20/20** Batch 2 packages reconciled with per-package final promotion classification. **20/20** package validators PASS. **20/20** provenance canonical. **16/16** signal families indexed. **20/20** frames visible in biomarker tree.

**Final decision:** `PROCEED_TO_PROMOTION_WITH_CLEARED_SUBSET`

**BATCH2-PROMOTE-1 scope:** **10 cleared**, **10 excluded**. Architecture gate **PASS**. **No runtime, package, frontend, or activation changes.**

---

## Batch 2 work completed (consolidated)

| Sprint | Outcome |
|--------|---------|
| PASS3-BATCH2-INGEST-1 | 20 specs registered |
| PASS3-BATCH2-PROVENANCE-1 | 20/20 manifests realigned to canonical Batch_2_Pass_3.json |
| PASS3-BATCH2-FRAME-INDEX-1/2 | 16 families / 20 frames indexed |
| BATCH2-PROMOTION-READINESS-1 | Per-package readiness classification |
| BATCH2-MEDREVIEW-1 | 8 androgen frames medically reviewed |
| BATCH2-CONTEXT-MOD-1 | Androgen context modifier governance binding |

---

## Consolidation answers

| # | Question | Answer |
|---|----------|--------|
| 1 | All 20 packages validated? | **Yes** — 20/20 PASS |
| 2 | All manifests provenance-corrected? | **Yes** — source_document = Batch_2_Pass_3.json |
| 3 | All 16 signal families indexed? | **Yes** |
| 4 | All frames in biomarker tree? | **Yes** — verified in `biomarker_medical_frame_tree.md` |
| 5 | Cleared for BATCH2-PROMOTE-1? | **10 packages** (see below) |
| 6 | Excluded and why? | **10 packages** — androgen (8), eGFR (2) |
| 7 | Androgen still blocked? | **Yes** — CF-BATCH2-010, CF-CONTEXT-MOD-3 |
| 8 | Thyroid in cautious wave? | **Yes — cleared** for BATCH2-PROMOTE-1 with documented caution; activation still requires clinical sign-off |
| 9 | eGFR excluded? | **Yes** — CF-BATCH2-007 creatinine/eGFR adjudication unresolved |
| 10 | Further review before cleared subset promotion? | Thyroid clinical sign-off before **activation**; promotion sprint may proceed for cleared compile/promote scope |

---

## 20-package final decision table

| package_id | panel | group | decision |
|------------|-------|-------|----------|
| pkg_kb47_creatine_kinase_high_exertional_muscle_injury | muscle_injury | CLEARED_FOR_BATCH2_PROMOTE_1 | CLEARED |
| pkg_kb47_creatine_kinase_high_persistent_nonexertional_muscle_injury | muscle_injury | CLEARED_FOR_BATCH2_PROMOTE_1 | CLEARED |
| pkg_kb47_eosinophil_pct_high_reactive_atopic_eosinophilia | eosinophil | CLEARED_FOR_BATCH2_PROMOTE_1 | CLEARED |
| pkg_kb47_eosinophil_pct_high_secondary_or_systemic_eosinophilia | eosinophil | CLEARED_FOR_BATCH2_PROMOTE_1 | CLEARED |
| pkg_kb47_eosinophils_abs_high_hypereosinophilic_or_secondary_eosinophilia | eosinophil | CLEARED_FOR_BATCH2_PROMOTE_1 | CLEARED |
| pkg_kb47_eosinophils_abs_high_reactive_eosinophilic_inflammation | eosinophil | CLEARED_FOR_BATCH2_PROMOTE_1 | CLEARED |
| pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis | thyroid | CLEARED_FOR_BATCH2_PROMOTE_1 | CLEARED |
| pkg_kb47_free_t3_low_low_t3_syndrome | thyroid | CLEARED_FOR_BATCH2_PROMOTE_1 | CLEARED |
| pkg_kb47_free_t4_high_thyrotoxicosis_context | thyroid | CLEARED_FOR_BATCH2_PROMOTE_1 | CLEARED |
| pkg_kb47_free_t4_low_thyroid_hormone_deficiency | thyroid | CLEARED_FOR_BATCH2_PROMOTE_1 | CLEARED |
| pkg_kb47_dhea_high_androgen_excess_context | androgen | EXCLUDE_ANDROGEN_PENDING_CLINICAL_SIGNOFF | EXCLUDED |
| pkg_kb47_dhea_low_adrenal_androgen_reduction | androgen | EXCLUDE_ANDROGEN_PENDING_CLINICAL_SIGNOFF | EXCLUDED |
| pkg_kb47_fai_high_biochemical_hyperandrogenism | androgen | EXCLUDE_ANDROGEN_PENDING_CLINICAL_SIGNOFF | EXCLUDED |
| pkg_kb47_fai_low_reduced_free_androgen_availability | androgen | EXCLUDE_ANDROGEN_PENDING_CLINICAL_SIGNOFF | EXCLUDED |
| pkg_kb47_free_testosterone_high_androgen_excess_context | androgen | EXCLUDE_ANDROGEN_PENDING_CLINICAL_SIGNOFF | EXCLUDED |
| pkg_kb47_free_testosterone_low_androgen_deficiency_context | androgen | EXCLUDE_ANDROGEN_PENDING_CLINICAL_SIGNOFF | EXCLUDED |
| pkg_kb47_free_testosterone_pct_high_elevated_free_androgen_fraction | androgen | EXCLUDE_ANDROGEN_PENDING_CLINICAL_SIGNOFF | EXCLUDED |
| pkg_kb47_free_testosterone_pct_low_reduced_free_androgen_fraction | androgen | EXCLUDE_ANDROGEN_PENDING_CLINICAL_SIGNOFF | EXCLUDED |
| pkg_kb47_egfr_low_chronic_kidney_function_reduction | egfr | EXCLUDE_EGFR_PENDING_CREATININE_EGFR_ADJUDICATION | EXCLUDED |
| pkg_kb47_egfr_low_hemodynamic_filtration_drop | egfr | EXCLUDE_EGFR_PENDING_CREATININE_EGFR_ADJUDICATION | EXCLUDED |

Full register: `knowledge_bus/governance/batch2_final_promotion_decision_register_v1.yaml`

---

## Panel decisions

### Androgen (8 packages) — EXCLUDED

All androgen-panel frames remain blocked. No clinical sign-off evidence in repo (CF-BATCH2-010 Open). FAI and free testosterone pct frames additionally note runtime Layer B evaluation pending (CF-CONTEXT-MOD-3).

### Thyroid (4 packages) — CLEARED with caution

Included in BATCH2-PROMOTE-1 cleared subset. `READY_WITH_DOCUMENTED_CAUTION` from promotion readiness register. Clinical adjudication sign-off still required before **activation**, not before controlled promotion compile work.

### eGFR (2 packages) — EXCLUDED

Blocked pending creatinine/eGFR multi-frame adjudication (CF-BATCH2-007). Overlap with legacy creatinine eGFR override not resolved.

---

## BATCH2-PROMOTE-1 scope

**Include (10):** creatine_kinase (2), eosinophil_pct (2), eosinophils_abs (2), free_t3 (2), free_t4 (2)

**Exclude (10):** all androgen (8), all egfr (2)

**Authorization:** Proceed to BATCH2-PROMOTE-1 for cleared subset only. Do not promote androgen or eGFR packages in that sprint.

---

## Package validation

**Method:** `python backend/scripts/validate_knowledge_package.py --package-dir <pkg>` for all 20 packages during register generation.

**Result:** 20/20 PASS (exit code 0).

Representative output:

```text
manifest_validation: PASS
research_validation: PASS
signal_validation: PASS
promoted_signal_intelligence_validation: PASS
ready_for_implementation: True
```

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

### Frame index and catalogue

```text
validation_status: PASS
errors: 0
```

(both validators)

---

## Carry-forward updates

| ID | Action |
|----|--------|
| CF-BATCH2-006 | **Resolved** — cleared promotion wave defined (10 packages) |
| CF-BATCH2-008 | **Resolved** — thyroid classified cleared for cautious BATCH2-PROMOTE-1 |
| CF-BATCH2-011 | **Open (new)** — execute BATCH2-PROMOTE-1 for cleared subset |
| CF-BATCH2-007 | Remains Open |
| CF-BATCH2-010 | Remains Open |
| CF-CONTEXT-MOD-3 | Remains Open |

---

## Runtime boundary confirmation

**Confirmed:** No changes to packages, SignalEvaluator, SignalRegistry, runtime loaders, frontend, SSOT, or activation state. Governance-only decision register and audit report.
