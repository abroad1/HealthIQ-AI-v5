# V5 Canonical Activation Gate Stage 2 — Pre-change Launch-Critical Inventory

**Work ID:** `V5-CANONICAL-ACTIVATION-GATE-2`  
**Branch:** `refactor/v5-canonical-activation-gate-2`  
**Captured before mutation from live `SignalRegistry` + `package_runtime_eligibility_v1`**

## Cohort size

| Bucket | Count |
|---|---:|
| `pkg_kb47_*` package directories | 20 |
| `CURRENTLY_ELIGIBLE_AND_ACTIVE` | 6 |
| `CURRENTLY_BLOCKED_OR_INELIGIBLE` | 14 |
| `AMBIGUOUS_STOP` | 0 |

Cross-check vs ARCH-CONV-PKG2 BDR / Stage 1 hardening: **exact match** (6 Wave 1 INCLUDE with explicit lineage; 14 androgen/CK/eos non-reachable).

## CURRENTLY_ELIGIBLE_AND_ACTIVE

All have `provenance_status: EXPLICIT_SPEC`, runtime-loaded today, **zero** canonical register membership pre-change.

| package_id | activation_key | signal_id |
|---|---|---|
| `pkg_kb47_egfr_low_chronic_kidney_function_reduction` | `signal_egfr_low::inv_egfr_low_chronic_kidney_function_reduction` | `signal_egfr_low` |
| `pkg_kb47_egfr_low_hemodynamic_filtration_drop` | `signal_egfr_low::inv_egfr_low_hemodynamic_filtration_drop` | `signal_egfr_low` |
| `pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis` | `signal_free_t3_high::inv_free_t3_high_t3_predominant_thyrotoxicosis` | `signal_free_t3_high` |
| `pkg_kb47_free_t3_low_low_t3_syndrome` | `signal_free_t3_low::inv_free_t3_low_low_t3_syndrome` | `signal_free_t3_low` |
| `pkg_kb47_free_t4_high_thyrotoxicosis_context` | `signal_free_t4_high::inv_free_t4_high_thyrotoxicosis_context` | `signal_free_t4_high` |
| `pkg_kb47_free_t4_low_thyroid_hormone_deficiency` | `signal_free_t4_low::inv_free_t4_low_thyroid_hormone_deficiency` | `signal_free_t4_low` |

Authority to migrate: existing ARCH-CONV-PKG2 Wave 1 INCLUDE + recovered Pass 3 lineage (not inferred from disk presence alone).

## CURRENTLY_BLOCKED_OR_INELIGIBLE

All `eligibility: non_reachable`, `provenance_status: BLOCKED`. **Do not** create canonical activation entries.

1. `pkg_kb47_creatine_kinase_high_exertional_muscle_injury`
2. `pkg_kb47_creatine_kinase_high_persistent_nonexertional_muscle_injury`
3. `pkg_kb47_dhea_high_androgen_excess_context`
4. `pkg_kb47_dhea_low_adrenal_androgen_reduction`
5. `pkg_kb47_eosinophil_pct_high_reactive_atopic_eosinophilia`
6. `pkg_kb47_eosinophil_pct_high_secondary_or_systemic_eosinophilia`
7. `pkg_kb47_eosinophils_abs_high_hypereosinophilic_or_secondary_eosinophilia`
8. `pkg_kb47_eosinophils_abs_high_reactive_eosinophilic_inflammation`
9. `pkg_kb47_fai_high_biochemical_hyperandrogenism`
10. `pkg_kb47_fai_low_reduced_free_androgen_availability`
11. `pkg_kb47_free_testosterone_high_androgen_excess_context`
12. `pkg_kb47_free_testosterone_low_androgen_deficiency_context`
13. `pkg_kb47_free_testosterone_pct_high_elevated_free_androgen_fraction`
14. `pkg_kb47_free_testosterone_pct_low_reduced_free_androgen_fraction`

## Pre-change grant path (to retire)

`SignalRegistry._load` skips the canonical register gate when `is_launch_critical_package_id` is true (`signal_evaluator.py`), so lineage eligibility in `package_runtime_eligibility_v1` independently grants activation for the 6 active packages.

## AMBIGUOUS_STOP

None. Migration may proceed for the 6 active frames only.
