# MED-RESEARCH-REVIEW-1 — Pass 3 Primary Biomarker Cross-Validation Addendum

**Work ID:** `MED-RESEARCH-REVIEW-1_non_pass3_package_revalidation`
**Date:** 2026-05-31
**Scope:** All Pass 3 JSON under `knowledge_bus/research/investigation_specs/multi_llm_research`
**Match rule:** `primary_marker.biomarker_id` only (not supporting/contradiction/confirmatory markers)

---

## Executive summary

Pass 3 files scanned: **10**

| Metric | Count |
|---|---:|
| Packages in cohort | 55 |
| Primary biomarker match in Pass 3 (any signal primary) | 55 |
| No primary biomarker Pass 3 match (derivable primaries) | 0 |
| No derivable primary biomarker in signal_library | 0 |
| Appears to have Pass 3 primary research but older package authority | 27 |
| Genuinely need new Pass 3 frame (signal construct; biomarker may exist) | 1 |
| Provenance recovery (not medical rewrite) | 1 |

### Pass 3 files included

- `knowledge_bus/research/investigation_specs/multi_llm_research/archived_ingested_batches/Batch_2_Pass_3_Rev1.json`
- `knowledge_bus/research/investigation_specs/multi_llm_research/Batch_3_Pass_3.json`
- `knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json`
- `knowledge_bus/research/investigation_specs/multi_llm_research/Batch_5_Pass_3.json`
- `knowledge_bus/research/investigation_specs/multi_llm_research/Batch_6_Pass_3.json`
- `knowledge_bus/research/investigation_specs/multi_llm_research/Batch_7_Pass_3.json`
- `knowledge_bus/research/investigation_specs/multi_llm_research/cbc_hematology_pass_3.json`
- `knowledge_bus/research/investigation_specs/multi_llm_research/lipid_derived_pass_3.json`
- `knowledge_bus/research/investigation_specs/multi_llm_research/thyroid_antibodies_pass_3.json`
- `knowledge_bus/research/investigation_specs/multi_llm_research/transferrin_pass_3.json`

---

## Answers

1. **Packages with a primary biomarker present in Pass 3 primary_marker:** 55 of 55.
2. **Packages with no primary biomarker Pass 3 match:** 0 of 55 (0 additional packages lack derivable primary biomarkers in signal_library).

3. **Likely newer Pass 3 research available but older package authority still active:**

- `pkg_b12_deficiency_context` — primary(s) `vitamin_b12`; Pass 3 signals: `signal_active_b12_low, signal_vitamin_b12_high, signal_vitamin_b12_low`
- `pkg_glucose_dysregulation_hba1c_context` — primary(s) `hba1c`; Pass 3 signals: `signal_hba1c_high, signal_hba1c_low, signal_hba1c_pct_high, signal_hba1c_pct_low`
- `pkg_hepatic_alt_context` — primary(s) `alt`; Pass 3 signals: `signal_alt_high`
- `pkg_hepatic_metabolic_stress` — primary(s) `tyg_index`; Pass 3 signals: `signal_tyg_index_high`
- `pkg_homocysteine_elevation_context` — primary(s) `homocysteine`; Pass 3 signals: `signal_homocysteine_high`
- `pkg_inflammation_crp_context` — primary(s) `crp`; Pass 3 signals: `signal_crp_high`
- `pkg_insulin_resistance` — primary(s) `tyg_index`; Pass 3 signals: `signal_tyg_index_high`
- `pkg_iron_deficiency_context` — primary(s) `ferritin`; Pass 3 signals: `signal_ferritin_high, signal_ferritin_low`
- `pkg_iron_overload_context` — primary(s) `ferritin`; Pass 3 signals: `signal_ferritin_high, signal_ferritin_low`
- `pkg_kb45_active_b12_low_deficiency` — primary(s) `active_b12`; Pass 3 signals: `signal_active_b12_low`
- `pkg_kb45_apoa1_low_cardio_risk` — primary(s) `apoa1`; Pass 3 signals: `signal_apoa1_low`
- `pkg_kb45_apob_apoa1_ratio_high_imbalance` — primary(s) `apob_apoa1_ratio`; Pass 3 signals: `signal_apob_apoa1_ratio_high`
- `pkg_kb45_apob_high_atherogenic` — primary(s) `apob`; Pass 3 signals: `signal_apob_high, signal_apob_low`
- `pkg_kb45_basophil_pct_high_basophilia` — primary(s) `basophil_pct`; Pass 3 signals: `signal_basophil_pct_high, signal_basophil_pct_low`
- `pkg_kb45_basophils_abs_high_basophilia` — primary(s) `basophils_abs`; Pass 3 signals: `signal_basophils_abs_high, signal_basophils_abs_low`
- `pkg_kb45_bilirubin_high_hyperbilirubinemia` — primary(s) `bilirubin`; Pass 3 signals: `signal_bilirubin_high`
- `pkg_kb45_chloride_high_hyperchloremia` — primary(s) `chloride`; Pass 3 signals: `signal_chloride_high, signal_chloride_low`
- `pkg_kb45_corrected_calcium_high_hypercalcemia` — primary(s) `corrected_calcium`; Pass 3 signals: `signal_corrected_calcium_high, signal_corrected_calcium_low`
- `pkg_kb45_cortisol_high_hypercortisolism` — primary(s) `cortisol`; Pass 3 signals: `signal_cortisol_high, signal_cortisol_low`
- `pkg_s24_hdl_high_cardiovascular` — primary(s) `hdl_cholesterol`; Pass 3 signals: `signal_hdl_low`
- `pkg_s24_hdl_low_cardiovascular` — primary(s) `hdl_cholesterol`; Pass 3 signals: `signal_hdl_low`
- `pkg_s24_hgb_low_anemia` — primary(s) `hemoglobin`; Pass 3 signals: `signal_hgb_high, signal_hgb_low`
- `pkg_s24_ldl_high_dyslipidaemia` — primary(s) `ldl_cholesterol`; Pass 3 signals: `signal_ldl_high`
- `pkg_s24_lym_high_lymphocytosis` — primary(s) `lymphocytes`; Pass 3 signals: `signal_lym_high, signal_lym_low, signal_lymphocytes_abs_high, signal_lymphocytes_abs_low`
- `pkg_s24_plt_high_thrombocytosis` — primary(s) `platelets`; Pass 3 signals: `signal_plt_high, signal_plt_low`
- `pkg_s24_plt_low_thrombocytopenia` — primary(s) `platelets`; Pass 3 signals: `signal_plt_high, signal_plt_low`
- `pkg_thyroid_tsh_context` — primary(s) `tsh`; Pass 3 signals: `signal_tsh_high, signal_tsh_low`

4. **Genuinely need new Pass 3 research/spec creation:**

All 55 packages have at least one **primary biomarker** present as a Pass 3 `primary_marker.biomarker_id` (after grounded ID normalization: e.g. `hemoglobin`↔`hgb`, `platelets`↔`plt`, `white_blood_cells`↔`wbc`, `hdl_cholesterol`↔`hdl`).

Packages that still need **new Pass 3 frames** (distinct signal construct, not merely compile/mapping):

- **`pkg_chronic_inflammation`** — primary `crp` matches Pass 3 CRP specs (`signal_crp_high`), but runtime authority is `signal_systemic_inflammation` (study-derived chronic construct). **CF-CHRONICINFL-001** / `author_new_pass3_frame` remains required; do not treat CRP-primary Pass 3 specs as substitutes.

Study-derived packages with **biomarker overlap but signal_id mismatch** (prefer Pass 3 mapping/re-run, not net-new biomarker research):

- **`pkg_insulin_resistance`** — primary `tyg_index` ↔ Pass 3 `signal_tyg_index_high`; package signal `signal_insulin_resistance`.
- **`pkg_hepatic_metabolic_stress`** — primary `tyg_index` ↔ Pass 3 `signal_tyg_index_high`; package signal `signal_hepatic_metabolic_stress`.

5. **Provenance recovery rather than medical rewrite:**

- `pkg_lipid_transport` — manifest/source_document gap

---

## Per-package table (55)

| package_id | signal_id(s) | package primary biomarker(s) | source_type | maturity | Pass_3 primary match | Pass_3 file(s) | Pass_3 spec_id(s) | Pass_3 signal_id(s) | interpretation |
|---|---|---|---|---|:---:|---|---|---|---|
| KBP-0001 | signal_insulin_resistance, signal_lipid_transport_dysfunction, signal_hepatic_metabolic_stress, signal_systemic_inflammation, signal_vascular_inflammatory_stress, signal_renal_metabolic_stress, signal_oxygen_transport_capacity | ast_alt_ratio, crp, hemoglobin, non_hdl_cholesterol, tyg_index, urea_creatinine_ratio | legacy_retained_with_justification | accepted_with_rationale | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json; knowledge_bus/research/investigation_specs/multi_llm_research/Batch_6_Pass_3.json (+1) | inv_crp_high_active_inflammatory_or_infective_state; inv_crp_high_residual_cardiometabolic_inflammatory_risk (+6) | signal_crp_high; signal_hgb_high (+4) | needs_manual_review |
| pkg_b12_deficiency_context | signal_b12_deficiency_context | vitamin_b12 | architecture_doc_blocked | architecture_anchor_review_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json; knowledge_bus/research/investigation_specs/multi_llm_research/Batch_5_Pass_3.json | inv_active_b12_low_b12_depletion; inv_vitamin_b12_high_supplementation_or_secondary_elevation (+1) | signal_active_b12_low; signal_vitamin_b12_high (+1) | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_chronic_inflammation | signal_systemic_inflammation | crp | research_study_markdown | study_derived_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json | inv_crp_high_active_inflammatory_or_infective_state; inv_crp_high_residual_cardiometabolic_inflammatory_risk | signal_crp_high | needs_manual_review |
| pkg_example | signal_example_metabolic | triglycerides | retire_candidate | retire_candidate | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json | inv_triglycerides_high_insulin_resistant_hypertriglyceridemia; inv_triglycerides_high_severe_hypertriglyceridemia_context | signal_triglycerides_high | retire_candidate |
| pkg_glucose_dysregulation_hba1c_context | signal_glucose_dysregulation_hba1c_context | hba1c | architecture_doc_blocked | architecture_anchor_review_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_3_Pass_3.json; knowledge_bus/research/investigation_specs/multi_llm_research/Batch_6_Pass_3.json | inv_hba1c_high_diabetes_range_hyperglycemia; inv_hba1c_low_shortened_erythrocyte_lifespan_context (+3) | signal_hba1c_high; signal_hba1c_low (+2) | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_hepatic_alt_context | signal_hepatic_alt_context | alt | architecture_doc_blocked | architecture_anchor_review_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_5_Pass_3.json | inv_alt_high_hepatocellular_injury_pattern; inv_alt_high_metabolic_steatotic_liver_pattern (+1) | signal_alt_high | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_hepatic_metabolic_stress | signal_hepatic_metabolic_stress | tyg_index | research_study_markdown | study_derived_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_7_Pass_3.json | inv_tyg_index_high_insulin_resistance_pattern | signal_tyg_index_high | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_homocysteine_elevation_context | signal_homocysteine_elevation_context | homocysteine | architecture_doc_blocked | architecture_anchor_review_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_6_Pass_3.json | inv_homocysteine_high_b_vitamin_related_methylation_impairment; inv_homocysteine_high_renal_clearance_reduction | signal_homocysteine_high | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_inflammation_crp_context | signal_inflammation_crp_context | crp | architecture_doc_blocked | architecture_anchor_review_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json | inv_crp_high_active_inflammatory_or_infective_state; inv_crp_high_residual_cardiometabolic_inflammatory_risk | signal_crp_high | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_insulin_resistance | signal_insulin_resistance | tyg_index | research_study_markdown | study_derived_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_7_Pass_3.json | inv_tyg_index_high_insulin_resistance_pattern | signal_tyg_index_high | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_iron_deficiency_context | signal_iron_deficiency_context | ferritin | architecture_doc_blocked | architecture_anchor_review_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json | inv_ferritin_high_inflammatory_hyperferritinemia; inv_ferritin_high_iron_overload_context (+1) | signal_ferritin_high; signal_ferritin_low | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_iron_overload_context | signal_iron_overload_context | ferritin | architecture_doc_blocked | architecture_anchor_review_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json | inv_ferritin_high_inflammatory_hyperferritinemia; inv_ferritin_high_iron_overload_context (+1) | signal_ferritin_high; signal_ferritin_low | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_kb45_active_b12_low_deficiency | signal_active_b12_deficiency | active_b12 | unknown_ambiguous | batch_json_lineage_review_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_5_Pass_3.json | inv_active_b12_low_b12_depletion | signal_active_b12_low | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_kb45_apoa1_low_cardio_risk | signal_apoa1_cardio_risk | apoa1 | unknown_ambiguous | batch_json_lineage_review_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_5_Pass_3.json | inv_apoa1_low_atherogenic_hdl_deficiency; inv_apoa1_low_severe_primary_hdl_deficiency_pattern | signal_apoa1_low | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_kb45_apob_apoa1_ratio_high_imbalance | signal_lipid_imbalance | apob_apoa1_ratio | unknown_ambiguous | batch_json_lineage_review_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_5_Pass_3.json | inv_apob_apoa1_ratio_high_atherogenic_particle_imbalance; inv_apob_apoa1_ratio_high_insulin_resistance_atherogenic_dyslipidemia | signal_apob_apoa1_ratio_high | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_kb45_apob_high_atherogenic | signal_apob_atherogenic | apob | unknown_ambiguous | batch_json_lineage_review_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_5_Pass_3.json | inv_apob_high_atherogenic_particle_excess; inv_apob_high_familial_combined_hyperlipidemia_pattern (+1) | signal_apob_high; signal_apob_low | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_kb45_basophil_pct_high_basophilia | signal_basophilia_pct | basophil_pct | unknown_ambiguous | batch_json_lineage_review_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_5_Pass_3.json | inv_basophil_pct_high_myeloproliferative_signal; inv_basophil_pct_high_type2_hypersensitivity_inflammation (+1) | signal_basophil_pct_high; signal_basophil_pct_low | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_kb45_basophils_abs_high_basophilia | signal_basophilia_abs | basophils_abs | unknown_ambiguous | batch_json_lineage_review_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_5_Pass_3.json | inv_basophils_abs_high_myeloproliferative_signal; inv_basophils_abs_high_type2_hypersensitivity_inflammation (+1) | signal_basophils_abs_high; signal_basophils_abs_low | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_kb45_bilirubin_high_hyperbilirubinemia | signal_hyperbilirubinemia | bilirubin | unknown_ambiguous | batch_json_lineage_review_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_5_Pass_3.json | inv_bilirubin_high_gilbert_pattern; inv_bilirubin_high_hemolytic_turnover_pattern (+1) | signal_bilirubin_high | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_kb45_chloride_high_hyperchloremia | signal_hyperchloremia | chloride | unknown_ambiguous | batch_json_lineage_review_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_6_Pass_3.json | inv_chloride_high_hyperchloremic_metabolic_acidosis; inv_chloride_low_chloride_depletion_metabolic_alkalosis | signal_chloride_high; signal_chloride_low | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_kb45_corrected_calcium_high_hypercalcemia | signal_hypercalcemia | corrected_calcium | unknown_ambiguous | batch_json_lineage_review_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_6_Pass_3.json | inv_corrected_calcium_high_malignancy_mediated_hypercalcemia; inv_corrected_calcium_high_pth_mediated_hypercalcemia (+2) | signal_corrected_calcium_high; signal_corrected_calcium_low | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_kb45_cortisol_high_hypercortisolism | signal_hypercortisolism | cortisol | unknown_ambiguous | batch_json_lineage_review_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_6_Pass_3.json | inv_cortisol_high_hypercortisolism; inv_cortisol_low_adrenal_insufficiency | signal_cortisol_high; signal_cortisol_low | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_lipid_transport | signal_lipid_transport_dysfunction | non_hdl_cholesterol | provenance_gap | provenance_gap | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_7_Pass_3.json | inv_non_hdl_high_atherogenic_lipoprotein_burden; inv_non_hdl_low_reduced_atherogenic_lipoprotein_pool | signal_non_hdl_high; signal_non_hdl_low | provenance_recovery_needed |
| pkg_s24_albumin_low_nutritional | signal_albumin_low | albumin | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json | inv_albumin_low_inflammatory_hypoalbuminemia; inv_albumin_low_protein_loss_or_reduced_synthesis | signal_albumin_low | needs_manual_review |
| pkg_s24_alp_high_bone_biliary | signal_alp_high | alp | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_5_Pass_3.json | inv_alp_high_cholestatic_pattern; inv_alp_high_high_bone_turnover_pattern (+2) | signal_alp_high; signal_alp_low | needs_manual_review |
| pkg_s24_alt_high_hepatocellular_injury | signal_alt_high | alt | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_5_Pass_3.json | inv_alt_high_hepatocellular_injury_pattern; inv_alt_high_metabolic_steatotic_liver_pattern (+1) | signal_alt_high | needs_manual_review |
| pkg_s24_calcium_high_endocrine | signal_calcium_high | calcium | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_5_Pass_3.json | inv_calcium_high_primary_hyperparathyroid_pattern; inv_calcium_high_pth_independent_hypercalcemia (+2) | signal_calcium_high; signal_calcium_low | needs_manual_review |
| pkg_s24_creatinine_high_renal | signal_creatinine_high | creatinine | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json | inv_creatinine_high_reduced_glomerular_filtration; inv_creatinine_low_low_muscle_mass_or_low_generation | signal_creatinine_high; signal_creatinine_low | needs_manual_review |
| pkg_s24_crp_high_inflammation | signal_crp_high | crp | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json | inv_crp_high_active_inflammatory_or_infective_state; inv_crp_high_residual_cardiometabolic_inflammatory_risk | signal_crp_high | needs_manual_review |
| pkg_s24_ferritin_high_overload | signal_ferritin_high | ferritin | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json | inv_ferritin_high_inflammatory_hyperferritinemia; inv_ferritin_high_iron_overload_context (+1) | signal_ferritin_high; signal_ferritin_low | needs_manual_review |
| pkg_s24_ferritin_low_iron_deficiency | signal_ferritin_low | ferritin | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json | inv_ferritin_high_inflammatory_hyperferritinemia; inv_ferritin_high_iron_overload_context (+1) | signal_ferritin_high; signal_ferritin_low | needs_manual_review |
| pkg_s24_folate_low_deficiency | signal_folate_low | folate | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_6_Pass_3.json | inv_folate_high_supplementation_or_excess_exposure; inv_folate_low_folate_deficiency | signal_folate_high; signal_folate_low | needs_manual_review |
| pkg_s24_ggt_high_hepatic | signal_ggt_high | ggt | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_6_Pass_3.json | inv_ggt_high_alcohol_or_enzyme_induction_context; inv_ggt_high_hepatobiliary_cholestatic_context | signal_ggt_high | needs_manual_review |
| pkg_s24_hba1c_high_glycaemia | signal_hba1c_high | hba1c | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_3_Pass_3.json; knowledge_bus/research/investigation_specs/multi_llm_research/Batch_6_Pass_3.json | inv_hba1c_high_diabetes_range_hyperglycemia; inv_hba1c_low_shortened_erythrocyte_lifespan_context (+3) | signal_hba1c_high; signal_hba1c_low (+2) | needs_manual_review |
| pkg_s24_hdl_high_cardiovascular | signal_hdl_cholesterol_high | hdl_cholesterol | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json | inv_hdl_low_atherogenic_dyslipidemia; inv_hdl_low_hypertriglyceridemic_insulin_resistance_pattern | signal_hdl_low | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_s24_hdl_low_cardiovascular | signal_hdl_cholesterol_low | hdl_cholesterol | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json | inv_hdl_low_atherogenic_dyslipidemia; inv_hdl_low_hypertriglyceridemic_insulin_resistance_pattern | signal_hdl_low | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_s24_hgb_low_anemia | signal_hemoglobin_low | hemoglobin | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_6_Pass_3.json | inv_hgb_high_erythrocytosis_or_hypoxic_drive; inv_hgb_low_iron_deficiency_or_blood_loss_anemia (+1) | signal_hgb_high; signal_hgb_low | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_s24_homocysteine_high_metabolic | signal_homocysteine_high | homocysteine | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_6_Pass_3.json | inv_homocysteine_high_b_vitamin_related_methylation_impairment; inv_homocysteine_high_renal_clearance_reduction | signal_homocysteine_high | needs_manual_review |
| pkg_s24_ldl_high_dyslipidaemia | signal_ldl_cholesterol_high | ldl_cholesterol | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json | inv_ldl_high_atherogenic_ldl_burden; inv_ldl_high_familial_hypercholesterolemia_context | signal_ldl_high | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_s24_lym_high_lymphocytosis | signal_lymphocytes_high | lymphocytes | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_3_Pass_3.json; knowledge_bus/research/investigation_specs/multi_llm_research/Batch_6_Pass_3.json | inv_lym_high_reactive_or_lymphoproliferative_lymphocytosis; inv_lym_low_lymphopenia_stress_or_immunosuppression (+2) | signal_lym_high; signal_lym_low (+2) | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_s24_mcv_high_macrocytosis | signal_mcv_high | mcv | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_6_Pass_3.json | inv_mcv_high_megaloblastic_macrocytosis; inv_mcv_high_nonmegaloblastic_macrocytosis (+1) | signal_mcv_high; signal_mcv_low | needs_manual_review |
| pkg_s24_neutrophils_high_neutrophilia | signal_neutrophils_high | neutrophils | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_7_Pass_3.json | inv_neutrophils_high_acute_bacterial_inflammatory_response; inv_neutrophils_low_marrow_suppression_or_drug_effect | signal_neutrophils_high; signal_neutrophils_low | needs_manual_review |
| pkg_s24_neutrophils_low_neutropenia | signal_neutrophils_low | neutrophils | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_7_Pass_3.json | inv_neutrophils_high_acute_bacterial_inflammatory_response; inv_neutrophils_low_marrow_suppression_or_drug_effect | signal_neutrophils_high; signal_neutrophils_low | needs_manual_review |
| pkg_s24_plt_high_thrombocytosis | signal_platelets_high | platelets | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_7_Pass_3.json | inv_plt_high_clonal_myeloproliferative_thrombocytosis; inv_plt_high_reactive_thrombocytosis (+2) | signal_plt_high; signal_plt_low | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_s24_plt_low_thrombocytopenia | signal_platelets_low | platelets | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_7_Pass_3.json | inv_plt_high_clonal_myeloproliferative_thrombocytosis; inv_plt_high_reactive_thrombocytosis (+2) | signal_plt_high; signal_plt_low | primary_biomarker_exists_in_pass3_not_mapped |
| pkg_s24_triglycerides_high_metabolic | signal_triglycerides_high | triglycerides | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json | inv_triglycerides_high_insulin_resistant_hypertriglyceridemia; inv_triglycerides_high_severe_hypertriglyceridemia_context | signal_triglycerides_high | needs_manual_review |
| pkg_s24_tsh_high_hypothyroidism | signal_tsh_high | tsh | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json | inv_tsh_high_primary_hypothyroid_pattern; inv_tsh_low_thyrotoxic_pattern | signal_tsh_high; signal_tsh_low | needs_manual_review |
| pkg_s24_tsh_low_hyperthyroidism | signal_tsh_low | tsh | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json | inv_tsh_high_primary_hypothyroid_pattern; inv_tsh_low_thyrotoxic_pattern | signal_tsh_high; signal_tsh_low | needs_manual_review |
| pkg_s24_urate_high_metabolic | signal_urate_high | urate | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_7_Pass_3.json | inv_urate_high_gout_crystal_deposition_risk; inv_urate_low_reduced_urate_pool_or_renal_loss | signal_urate_high; signal_urate_low | needs_manual_review |
| pkg_s24_urea_high_renal | signal_urea_high | urea | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_7_Pass_3.json | inv_urea_high_prerenal_volume_depletion_or_catabolic_load; inv_urea_low_low_protein_or_reduced_urea_cycle_input | signal_urea_high; signal_urea_low | needs_manual_review |
| pkg_s24_vitamin_b12_low_deficiency | signal_vitamin_b12_low | vitamin_b12 | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json; knowledge_bus/research/investigation_specs/multi_llm_research/Batch_5_Pass_3.json | inv_active_b12_low_b12_depletion; inv_vitamin_b12_high_supplementation_or_secondary_elevation (+1) | signal_active_b12_low; signal_vitamin_b12_high (+1) | needs_manual_review |
| pkg_s24_vitamin_d_low_deficiency | signal_vitamin_d_low | vitamin_d | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json | inv_vitamin_d_high_vitamin_d_excess_context; inv_vitamin_d_low_vitamin_d_deficiency | signal_vitamin_d_high; signal_vitamin_d_low | needs_manual_review |
| pkg_s24_wbc_high_leukocytosis | signal_wbc_high | white_blood_cells | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_7_Pass_3.json | inv_wbc_high_possible_clonal_leukocyte_proliferation; inv_wbc_high_reactive_leukocytosis (+1) | signal_wbc_high; signal_wbc_low | needs_manual_review |
| pkg_s24_wbc_low_leukopenia | signal_wbc_low | white_blood_cells | investigation_spec_v1_yaml | non_pass3_runtime_revalidation_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_7_Pass_3.json | inv_wbc_high_possible_clonal_leukocyte_proliferation; inv_wbc_high_reactive_leukocytosis (+1) | signal_wbc_high; signal_wbc_low | needs_manual_review |
| pkg_thyroid_tsh_context | signal_thyroid_tsh_context | tsh | architecture_doc_blocked | architecture_anchor_review_required | yes | knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json | inv_tsh_high_primary_hypothyroid_pattern; inv_tsh_low_thyrotoxic_pattern | signal_tsh_high; signal_tsh_low | primary_biomarker_exists_in_pass3_not_mapped |

---

## Interpretation key

| Code | Meaning |
|---|---|
| `primary_biomarker_exists_in_pass3_not_mapped` | At least one package primary biomarker is a Pass 3 primary_marker elsewhere; package/signal mapping not aligned |
| `no_primary_biomarker_pass3_match` | No Pass 3 primary_marker match for package primary biomarker(s) |
| `provenance_recovery_needed` | Manifest/provenance gap; not primarily a Pass 3 rewrite |
| `retire_candidate` | Non-runtime example scaffold |
| `needs_manual_review` | Multi-signal legacy, signal-id overlap, or ambiguous cohort |

## Notes

- CRP as **supporting** marker in Pass 3 does not count; only `primary_marker.biomarker_id`.
- Biomarker ID normalization (package `primary_metric` ↔ Pass 3 `biomarker_id`): `hemoglobin`↔`hgb`, `platelets`↔`plt`, `white_blood_cells`↔`wbc`, `hdl_cholesterol`↔`hdl`, `ldl_cholesterol`↔`ldl`, `non_hdl_cholesterol`↔`non_hdl`, `vitamin_b12`↔`active_b12`, `hba1c`↔`hba1c_pct`, `lymphocytes`↔`lym`/`lymphocytes_abs`, `uric_acid`↔`urate`.
- `pkg_chronic_inflammation` primary `crp` may match Pass 3 CRP-primary specs while `signal_systemic_inflammation` remains study-derived — manual review / new frame still required.
- Register updated: `knowledge_bus/governance/non_pass3_package_revalidation_register_v1.yaml`.
- No runtime, package, or production code changes.
