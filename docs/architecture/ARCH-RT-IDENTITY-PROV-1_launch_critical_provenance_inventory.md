# ARCH-RT-IDENTITY-PROV-1 — Launch-critical provenance inventory

Generated deterministically by `backend/scripts/validate_identity_provenance_gate.py`.

| package_id | signal_id | source_spec_id | activation_key | provenance_status | beta_eligible_explicit | unresolved_action |
|---|---|---|---|---|---|---|
| pkg_kb47_creatine_kinase_high_exertional_muscle_injury | signal_creatine_kinase_high | inv_creatine_kinase_high_exertional_muscle_injury | signal_creatine_kinase_high::inv_creatine_kinase_high_exertional_muscle_injury | BLOCKED | False | Extract investigation-spec frame from batch JSON or attach inv_ YAML before beta claim |
| pkg_kb47_creatine_kinase_high_persistent_nonexertional_muscle_injury | signal_creatine_kinase_high | inv_creatine_kinase_high_persistent_nonexertional_muscle_injury | signal_creatine_kinase_high::inv_creatine_kinase_high_persistent_nonexertional_muscle_injury | BLOCKED | False | Extract investigation-spec frame from batch JSON or attach inv_ YAML before beta claim |
| pkg_kb47_dhea_high_androgen_excess_context | signal_dhea_high | inv_dhea_high_androgen_excess_context | signal_dhea_high::inv_dhea_high_androgen_excess_context | BLOCKED | False | Extract investigation-spec frame from batch JSON or attach inv_ YAML before beta claim |
| pkg_kb47_egfr_low_chronic_kidney_function_reduction | signal_egfr_low | inv_egfr_low_chronic_kidney_function_reduction | signal_egfr_low::inv_egfr_low_chronic_kidney_function_reduction | BLOCKED | False | Extract investigation-spec frame from batch JSON or attach inv_ YAML before beta claim |
| pkg_kb47_egfr_low_hemodynamic_filtration_drop | signal_egfr_low | inv_egfr_low_hemodynamic_filtration_drop | signal_egfr_low::inv_egfr_low_hemodynamic_filtration_drop | BLOCKED | False | Extract investigation-spec frame from batch JSON or attach inv_ YAML before beta claim |
| pkg_kb47_eosinophil_pct_high_reactive_atopic_eosinophilia | signal_eosinophil_pct_high | inv_eosinophil_pct_high_reactive_atopic_eosinophilia | signal_eosinophil_pct_high::inv_eosinophil_pct_high_reactive_atopic_eosinophilia | BLOCKED | False | Extract investigation-spec frame from batch JSON or attach inv_ YAML before beta claim |
| pkg_kb47_eosinophil_pct_high_secondary_or_systemic_eosinophilia | signal_eosinophil_pct_high | inv_eosinophil_pct_high_secondary_or_systemic_eosinophilia | signal_eosinophil_pct_high::inv_eosinophil_pct_high_secondary_or_systemic_eosinophilia | BLOCKED | False | Extract investigation-spec frame from batch JSON or attach inv_ YAML before beta claim |
| pkg_kb47_eosinophils_abs_high_hypereosinophilic_or_secondary_eosinophilia | signal_eosinophils_abs_high | inv_eosinophils_abs_high_hypereosinophilic_or_secondary_eosinophilia | signal_eosinophils_abs_high::inv_eosinophils_abs_high_hypereosinophilic_or_secondary_eosinophilia | BLOCKED | False | Extract investigation-spec frame from batch JSON or attach inv_ YAML before beta claim |
| pkg_kb47_eosinophils_abs_high_reactive_eosinophilic_inflammation | signal_eosinophils_abs_high | inv_eosinophils_abs_high_reactive_eosinophilic_inflammation | signal_eosinophils_abs_high::inv_eosinophils_abs_high_reactive_eosinophilic_inflammation | BLOCKED | False | Extract investigation-spec frame from batch JSON or attach inv_ YAML before beta claim |
| pkg_kb47_fai_high_biochemical_hyperandrogenism | signal_fai_high | inv_fai_high_biochemical_hyperandrogenism | signal_fai_high::inv_fai_high_biochemical_hyperandrogenism | BLOCKED | False | Extract investigation-spec frame from batch JSON or attach inv_ YAML before beta claim |
| pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis | signal_free_t3_high | inv_free_t3_high_t3_predominant_thyrotoxicosis | signal_free_t3_high::inv_free_t3_high_t3_predominant_thyrotoxicosis | BLOCKED | False | Extract investigation-spec frame from batch JSON or attach inv_ YAML before beta claim |
| pkg_kb47_free_t3_low_low_t3_syndrome | signal_free_t3_low | inv_free_t3_low_low_t3_syndrome | signal_free_t3_low::inv_free_t3_low_low_t3_syndrome | BLOCKED | False | Extract investigation-spec frame from batch JSON or attach inv_ YAML before beta claim |
| pkg_kb47_free_t4_high_thyrotoxicosis_context | signal_free_t4_high | inv_free_t4_high_thyrotoxicosis_context | signal_free_t4_high::inv_free_t4_high_thyrotoxicosis_context | BLOCKED | False | Extract investigation-spec frame from batch JSON or attach inv_ YAML before beta claim |
| pkg_kb47_free_t4_low_thyroid_hormone_deficiency | signal_free_t4_low | inv_free_t4_low_thyroid_hormone_deficiency | signal_free_t4_low::inv_free_t4_low_thyroid_hormone_deficiency | BLOCKED | False | Extract investigation-spec frame from batch JSON or attach inv_ YAML before beta claim |
| pkg_kb47_free_testosterone_high_androgen_excess_context | signal_free_testosterone_high | inv_free_testosterone_high_androgen_excess_context | signal_free_testosterone_high::inv_free_testosterone_high_androgen_excess_context | BLOCKED | False | Extract investigation-spec frame from batch JSON or attach inv_ YAML before beta claim |
| pkg_kb47_free_testosterone_low_androgen_deficiency_context | signal_free_testosterone_low | inv_free_testosterone_low_androgen_deficiency_context | signal_free_testosterone_low::inv_free_testosterone_low_androgen_deficiency_context | BLOCKED | False | Extract investigation-spec frame from batch JSON or attach inv_ YAML before beta claim |
| — | signal_vitamin_d_low | — | — | COMPILED_MANIFEST | True | — |

## Naming authority

- `compile_manifest_ref` — canonical logical reference on compiled artefacts.
- `compile_manifest_path` — estate-index internal path field (same files; not a competing authority).

## Scanner roles

- `package_provenance_scan_v1.scan_all_package_provenance` — estate-wide classification inventory.
- `launch_estate_v1.scan_package_provenance` — launch-estate focused row set.
- Shared overlapping facts must use consistent terminology; this gate is the beta-readiness view for the launch-critical cohort.

