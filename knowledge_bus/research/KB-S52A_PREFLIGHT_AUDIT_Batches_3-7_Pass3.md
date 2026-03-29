# KB-S52A — Preflight audit: Batches 3–7 Pass 3 (investigation specs v3.0.0)

**work_id:** KB-S52A  
**Audit date:** 2026-03-29  
**Classification:** Read-only CONTENT audit (no repository mutations for this deliverable).

---

## 1. Authority checks (required)

| Item | Authoritative path | Notes |
|------|-------------------|--------|
| Upstream research tranche | `knowledge_bus/research/investigation_specs/multi_llm_research/Batch_3_Pass_3.json` … `Batch_7_Pass_3.json` | Five JSON files, each a **top-level array** of specs. |
| Biomarker / panel SSOT | `backend/ssot/biomarker_alias_registry.yaml`, `backend/ssot/biomarkers.yaml` | Resolution behaviour in this audit uses **`AliasRegistryService.resolve()`** (`backend/core/canonical/alias_registry_service.py`) as the runtime-aligned resolver. |
| Investigation contract | `knowledge_bus/research/investigation_specs/investigation_spec_schema_v3.0.0.yaml` | v3.0.0 locked schema. |
| Investigation validator | `backend/scripts/validate_investigation_spec.py` | See **translation-boundary** note: CLI expects a **single root object**, not an array batch file. |
| KB package contracts | `knowledge_bus/schema/research_brief_schema.yaml`, `signal_library_schema.yaml`, `package_manifest_schema.yaml`; optional `intelligence_model_schema_v1.yaml`, `promoted_signal_intelligence_schema_v1.yaml`; ADR `architecture/ADR-008-promoted-signal-intelligence-contract-v1.md` | Govern downstream package shape and opt-in intelligence layers. |
| Package validator | `backend/scripts/validate_knowledge_package.py` | Promotion gate per Knowledge Bus SOP v1.3. |

**Parallel authority:** This audit does not introduce a second SSOT; it cross-checks upstream `biomarker_id` / `metric_id` / `marker_reference` strings against the existing resolver.

---

## 2. Tranche inventory

| Batch file | Wave (default) | Spec count | `spec_id` list |
|------------|----------------|------------|----------------|
| `Batch_3_Pass_3.json` | Wave 1 (3–5) | 26 | `inv_fsh_high_primary_gonadal_failure`, `inv_fsh_low_hypogonadotropic_suppression`, `inv_globulin_high_polyclonal_inflammatory_hypergammaglobulinemia`, `inv_globulin_high_monoclonal_gammopathy_signal`, `inv_globulin_low_hypogammaglobulinemia_or_protein_loss`, `inv_hba1c_pct_high_chronic_hyperglycemia_diabetes`, `inv_hba1c_pct_high_red_cell_turnover_bias_or_iron_deficiency`, `inv_hba1c_pct_low_shortened_red_cell_survival_or_low_glycemia`, `inv_hematocrit_high_absolute_erythrocytosis`, `inv_hematocrit_high_relative_hemoconcentration`, `inv_hematocrit_low_anemia_or_hemodilution`, `inv_iron_low_absolute_iron_deficiency`, `inv_iron_low_functional_iron_restriction_inflammation`, `inv_iron_high_iron_overload_context`, `inv_iron_high_hepatocellular_or_hemolytic_release`, `inv_lh_high_primary_gonadal_feedback_loss`, `inv_lh_low_central_hypogonadotropic_pattern`, `inv_lipoprotein_a_high_atherosclerotic_cardiovascular_risk`, `inv_lipoprotein_a_high_calcific_aortic_valve_risk`, `inv_lymphocyte_pct_high_relative_reactive_lymphocytosis`, `inv_lymphocyte_pct_low_relative_lymphopenic_shift`, `inv_lymphocytes_abs_high_reactive_lymphocytosis`, `inv_lymphocytes_abs_low_true_lymphopenia`, `inv_magnesium_low_total_body_magnesium_deficiency`, `inv_magnesium_low_renal_magnesium_wasting`, `inv_magnesium_high_reduced_excretion_or_excess_load` |
| `Batch_4_Pass_3.json` | Wave 1 | 23 | `inv_albumin_low_inflammatory_hypoalbuminemia`, `inv_albumin_low_protein_loss_or_reduced_synthesis`, `inv_creatinine_high_reduced_glomerular_filtration`, `inv_creatinine_low_low_muscle_mass_or_low_generation`, `inv_crp_high_active_inflammatory_or_infective_state`, `inv_crp_high_residual_cardiometabolic_inflammatory_risk`, `inv_ferritin_low_iron_store_depletion`, `inv_ferritin_high_iron_overload_context`, `inv_ferritin_high_inflammatory_hyperferritinemia`, `inv_hdl_low_atherogenic_dyslipidemia`, `inv_hdl_low_hypertriglyceridemic_insulin_resistance_pattern`, `inv_ldl_high_atherogenic_ldl_burden`, `inv_ldl_high_familial_hypercholesterolemia_context`, `inv_triglycerides_high_insulin_resistant_hypertriglyceridemia`, `inv_triglycerides_high_severe_hypertriglyceridemia_context`, `inv_tsh_high_primary_hypothyroid_pattern`, `inv_tsh_low_thyrotoxic_pattern`, `inv_vitamin_b12_low_b12_deficiency_context`, `inv_vitamin_b12_high_supplementation_or_secondary_elevation`, `inv_vitamin_d_low_vitamin_d_deficiency`, `inv_vitamin_d_high_vitamin_d_excess_context`, `inv_magnesium_low_hypomagnesemia`, `inv_magnesium_high_hypermagnesemia_context` |
| `Batch_5_Pass_3.json` | Wave 1 | 28 | `inv_active_b12_low_b12_depletion`, `inv_alp_high_cholestatic_pattern`, `inv_alp_high_high_bone_turnover_pattern`, `inv_alp_low_hypophosphatasia_pattern`, `inv_alp_low_nutrient_or_cofactor_deficiency`, `inv_alt_high_hepatocellular_injury_pattern`, `inv_alt_high_metabolic_steatotic_liver_pattern`, `inv_alt_high_muscle_source_or_exertional_pattern`, `inv_apoa1_low_atherogenic_hdl_deficiency`, `inv_apoa1_low_severe_primary_hdl_deficiency_pattern`, `inv_apob_high_atherogenic_particle_excess`, `inv_apob_high_familial_combined_hyperlipidemia_pattern`, `inv_apob_low_hypobetalipoproteinemia_or_malabsorption_pattern`, `inv_apob_apoa1_ratio_high_atherogenic_particle_imbalance`, `inv_apob_apoa1_ratio_high_insulin_resistance_atherogenic_dyslipidemia`, `inv_basophil_pct_high_type2_hypersensitivity_inflammation`, `inv_basophil_pct_high_myeloproliferative_signal`, `inv_basophil_pct_low_glucocorticoid_or_acute_stress_pattern`, `inv_basophils_abs_high_type2_hypersensitivity_inflammation`, `inv_basophils_abs_high_myeloproliferative_signal`, `inv_basophils_abs_low_glucocorticoid_or_acute_stress_pattern`, `inv_bilirubin_high_gilbert_pattern`, `inv_bilirubin_high_hemolytic_turnover_pattern`, `inv_bilirubin_high_hepatobiliary_excretion_impairment`, `inv_calcium_high_primary_hyperparathyroid_pattern`, `inv_calcium_high_pth_independent_hypercalcemia`, `inv_calcium_low_vitamin_d_or_magnesium_related_hypocalcemia`, `inv_calcium_low_hypoparathyroid_pattern` |
| `Batch_6_Pass_3.json` | Wave 2 (6–7) | 24 | `inv_chloride_high_hyperchloremic_metabolic_acidosis`, `inv_chloride_low_chloride_depletion_metabolic_alkalosis`, `inv_corrected_calcium_high_pth_mediated_hypercalcemia`, `inv_corrected_calcium_high_malignancy_mediated_hypercalcemia`, `inv_corrected_calcium_low_hypoparathyroid_state`, `inv_corrected_calcium_low_secondary_hyperparathyroid_context`, `inv_cortisol_low_adrenal_insufficiency`, `inv_cortisol_high_hypercortisolism`, `inv_folate_low_folate_deficiency`, `inv_folate_high_supplementation_or_excess_exposure`, `inv_ggt_high_hepatobiliary_cholestatic_context`, `inv_ggt_high_alcohol_or_enzyme_induction_context`, `inv_hba1c_high_diabetes_range_hyperglycemia`, `inv_hba1c_low_shortened_erythrocyte_lifespan_context`, `inv_hgb_low_iron_deficiency_or_blood_loss_anemia`, `inv_hgb_low_normocytic_underproduction_context`, `inv_hgb_high_erythrocytosis_or_hypoxic_drive`, `inv_homocysteine_high_b_vitamin_related_methylation_impairment`, `inv_homocysteine_high_renal_clearance_reduction`, `inv_lym_low_lymphopenia_stress_or_immunosuppression`, `inv_lym_high_reactive_or_lymphoproliferative_lymphocytosis`, `inv_mcv_high_megaloblastic_macrocytosis`, `inv_mcv_high_nonmegaloblastic_macrocytosis`, `inv_mcv_low_microcytosis_iron_deficiency` |
| `Batch_7_Pass_3.json` | Wave 2 | 16 | `inv_neutrophils_high_acute_bacterial_inflammatory_response`, `inv_neutrophils_low_marrow_suppression_or_drug_effect`, `inv_non_hdl_high_atherogenic_lipoprotein_burden`, `inv_non_hdl_low_reduced_atherogenic_lipoprotein_pool`, `inv_plt_high_reactive_thrombocytosis`, `inv_plt_high_clonal_myeloproliferative_thrombocytosis`, `inv_plt_low_peripheral_consumption_or_immune_destruction`, `inv_plt_low_marrow_suppression_pattern`, `inv_tyg_index_high_insulin_resistance_pattern`, `inv_urate_high_gout_crystal_deposition_risk`, `inv_urate_low_reduced_urate_pool_or_renal_loss`, `inv_urea_high_prerenal_volume_depletion_or_catabolic_load`, `inv_urea_low_low_protein_or_reduced_urea_cycle_input`, `inv_wbc_high_reactive_leukocytosis`, `inv_wbc_low_global_leukopenic_suppression`, `inv_wbc_high_possible_clonal_leukocyte_proliferation` |

**Total:** 117 specs.

---

## 3. Resolver summary (canonical mapping)

**Method:** Every `biomarker_id`, `marker_reference`, and override-rule `metric_id` in each spec was collected recursively and passed through `AliasRegistryService.resolve()`. Any result starting with `unmapped_` is treated as **not currently in the authoritative alias/biomarker estate** for pipeline resolution.

**Counts:**

- **117** total specs.
- **67** specs: **no** unmapped touchpoints (**ingestible as-is** from an SSOT-resolution perspective).
- **50** specs: **at least one** unmapped touchpoint.
- **4** specs: **unmapped primary** `biomarker_id` — both `inv_non_hdl_*` (`non_hdl` vs SSOT `non_hdl_cholesterol`), and both `inv_lym_*` (`lym` vs no SSOT key; nearest concepts are e.g. `lymphocyte_pct`, `lymphocytes_abs`).

**Distinct unmapped upstream IDs (28):**

`amylase`, `anion_gap`, `bicarbonate`, `erythropoietin`, `fasting_glucose`, `fractional_excretion_magnesium`, `igg`, `jak2_v617f`, `lym`, `mma`, `non_hdl`, `parathyroid_hormone`, `phosphate`, `procalcitonin`, `pth`, `pth_related_peptide`, `rbc_count`, `repeat_bilirubin`, `reticulocyte_count`, `reticulocytes`, `serum_protein_electrophoresis`, `smudge_cells`, `total_b12`, `transferrin_saturation`, `urine_magnesium_24h`, `urine_protein_creatinine_ratio`, `vitamin_b6`, `wbc_total`

**Obvious governed remaps (not applied in data — require explicit governance):**

- `non_hdl` → `non_hdl_cholesterol` (registry key / aliases use `non_hdl_cholesterol`).
- `fasting_glucose` → `glucose` (no separate fasting glucose canonical; `glucose` is the analyte SSOT).
- `wbc_total` → `white_blood_cells` (same concept as WBC common alias).
- `parathyroid_hormone` / `pth` → single canonical PTH key once added to SSOT (both currently missing).
- `lym` → choose `lymphocyte_pct` vs `lymphocytes_abs` vs new canonical (abbreviation not valid today).

**Derived / composite / non-analyte constructs:**

- `tyg_index` **resolves** (present in `biomarkers.yaml` and registered via SSOT load).
- `transferrin_saturation`, `anion_gap`, `fractional_excretion_magnesium`, `urine_protein_creatinine_ratio`: treated as **missing** unless explicitly added as biomarkers or `derived_metrics` with engine support.
- `repeat_bilirubin`, `serum_protein_electrophoresis`, `jak2_v617f`, `smudge_cells`: **clinical artefacts / tests / morphologic flags**, not standard chemistry CBC keys — translation to `signal_library` **primary_metric** / **supporting_metrics** requires a **governed decision** (omit, map to narrative-only, or extend SSOT).

---

## 4. Per-spec outcomes (compact)

**Legend:** `OK` = all touchpoints resolve. `BLOCKED` = ≥1 unmapped ID in primary, supporting, hypotheses, contradictions, or override conditions.

| File | spec_id | Primary resolution | Supporting / other unmapped | Status |
|------|---------|--------------------|-----------------------------|--------|
| Batch_3_Pass_3.json | inv_fsh_high_primary_gonadal_failure | fsh→fsh | — | OK |
| Batch_3_Pass_3.json | inv_fsh_low_hypogonadotropic_suppression | fsh→fsh | — | OK |
| Batch_3_Pass_3.json | inv_globulin_high_polyclonal_inflammatory_hypergammaglobulinemia | globulin→globulin | serum_protein_electrophoresis | BLOCKED |
| Batch_3_Pass_3.json | inv_globulin_high_monoclonal_gammopathy_signal | globulin→globulin | serum_protein_electrophoresis | BLOCKED |
| Batch_3_Pass_3.json | inv_globulin_low_hypogammaglobulinemia_or_protein_loss | globulin→globulin | igg, urine_protein_creatinine_ratio | BLOCKED |
| Batch_3_Pass_3.json | inv_hba1c_pct_high_chronic_hyperglycemia_diabetes | hba1c_pct→hba1c_pct | fasting_glucose | BLOCKED |
| Batch_3_Pass_3.json | inv_hba1c_pct_high_red_cell_turnover_bias_or_iron_deficiency | hba1c_pct→hba1c_pct | fasting_glucose | BLOCKED |
| Batch_3_Pass_3.json | inv_hba1c_pct_low_shortened_red_cell_survival_or_low_glycemia | hba1c_pct→hba1c_pct | fasting_glucose, reticulocyte_count | BLOCKED |
| Batch_3_Pass_3.json | inv_hematocrit_high_absolute_erythrocytosis | hematocrit→hematocrit | erythropoietin, jak2_v617f | BLOCKED |
| Batch_3_Pass_3.json | inv_hematocrit_high_relative_hemoconcentration | hematocrit→hematocrit | erythropoietin | BLOCKED |
| Batch_3_Pass_3.json | inv_hematocrit_low_anemia_or_hemodilution | hematocrit→hematocrit | — | OK |
| Batch_3_Pass_3.json | inv_iron_low_absolute_iron_deficiency | iron→iron | transferrin_saturation | BLOCKED |
| Batch_3_Pass_3.json | inv_iron_low_functional_iron_restriction_inflammation | iron→iron | transferrin_saturation | BLOCKED |
| Batch_3_Pass_3.json | inv_iron_high_iron_overload_context | iron→iron | transferrin_saturation | BLOCKED |
| Batch_3_Pass_3.json | inv_iron_high_hepatocellular_or_hemolytic_release | iron→iron | transferrin_saturation | BLOCKED |
| Batch_3_Pass_3.json | inv_lh_high_primary_gonadal_feedback_loss | lh→lh | — | OK |
| Batch_3_Pass_3.json | inv_lh_low_central_hypogonadotropic_pattern | lh→lh | — | OK |
| Batch_3_Pass_3.json | inv_lipoprotein_a_high_atherosclerotic_cardiovascular_risk | lipoprotein_a→lipoprotein_a | — | OK |
| Batch_3_Pass_3.json | inv_lipoprotein_a_high_calcific_aortic_valve_risk | lipoprotein_a→lipoprotein_a | — | OK |
| Batch_3_Pass_3.json | inv_lymphocyte_pct_high_relative_reactive_lymphocytosis | lymphocyte_pct→lymphocyte_pct | — | OK |
| Batch_3_Pass_3.json | inv_lymphocyte_pct_low_relative_lymphopenic_shift | lymphocyte_pct→lymphocyte_pct | — | OK |
| Batch_3_Pass_3.json | inv_lymphocytes_abs_high_reactive_lymphocytosis | lymphocytes_abs→lymphocytes_abs | smudge_cells | BLOCKED |
| Batch_3_Pass_3.json | inv_lymphocytes_abs_low_true_lymphopenia | lymphocytes_abs→lymphocytes_abs | igg | BLOCKED |
| Batch_3_Pass_3.json | inv_magnesium_low_total_body_magnesium_deficiency | magnesium→magnesium | fractional_excretion_magnesium | BLOCKED |
| Batch_3_Pass_3.json | inv_magnesium_low_renal_magnesium_wasting | magnesium→magnesium | fractional_excretion_magnesium, urine_magnesium_24h | BLOCKED |
| Batch_3_Pass_3.json | inv_magnesium_high_reduced_excretion_or_excess_load | magnesium→magnesium | — | OK |
| Batch_4_Pass_3.json | inv_albumin_low_inflammatory_hypoalbuminemia | albumin→albumin | — | OK |
| Batch_4_Pass_3.json | inv_albumin_low_protein_loss_or_reduced_synthesis | albumin→albumin | — | OK |
| Batch_4_Pass_3.json | inv_creatinine_high_reduced_glomerular_filtration | creatinine→creatinine | — | OK |
| Batch_4_Pass_3.json | inv_creatinine_low_low_muscle_mass_or_low_generation | creatinine→creatinine | — | OK |
| Batch_4_Pass_3.json | inv_crp_high_active_inflammatory_or_infective_state | crp→crp | procalcitonin | BLOCKED |
| Batch_4_Pass_3.json | inv_crp_high_residual_cardiometabolic_inflammatory_risk | crp→crp | procalcitonin | BLOCKED |
| Batch_4_Pass_3.json | inv_ferritin_low_iron_store_depletion | ferritin→ferritin | — | OK |
| Batch_4_Pass_3.json | inv_ferritin_high_iron_overload_context | ferritin→ferritin | transferrin_saturation | BLOCKED |
| Batch_4_Pass_3.json | inv_ferritin_high_inflammatory_hyperferritinemia | ferritin→ferritin | transferrin_saturation | BLOCKED |
| Batch_4_Pass_3.json | inv_hdl_low_atherogenic_dyslipidemia | hdl→hdl_cholesterol | — | OK |
| Batch_4_Pass_3.json | inv_hdl_low_hypertriglyceridemic_insulin_resistance_pattern | hdl→hdl_cholesterol | — | OK |
| Batch_4_Pass_3.json | inv_ldl_high_atherogenic_ldl_burden | ldl→ldl_cholesterol | — | OK |
| Batch_4_Pass_3.json | inv_ldl_high_familial_hypercholesterolemia_context | ldl→ldl_cholesterol | — | OK |
| Batch_4_Pass_3.json | inv_triglycerides_high_insulin_resistant_hypertriglyceridemia | triglycerides→triglycerides | — | OK |
| Batch_4_Pass_3.json | inv_triglycerides_high_severe_hypertriglyceridemia_context | triglycerides→triglycerides | amylase | BLOCKED |
| Batch_4_Pass_3.json | inv_tsh_high_primary_hypothyroid_pattern | tsh→tsh | — | OK |
| Batch_4_Pass_3.json | inv_tsh_low_thyrotoxic_pattern | tsh→tsh | — | OK |
| Batch_4_Pass_3.json | inv_vitamin_b12_low_b12_deficiency_context | vitamin_b12→vitamin_b12 | — | OK |
| Batch_4_Pass_3.json | inv_vitamin_b12_high_supplementation_or_secondary_elevation | vitamin_b12→vitamin_b12 | — | OK |
| Batch_4_Pass_3.json | inv_vitamin_d_low_vitamin_d_deficiency | vitamin_d→vitamin_d | parathyroid_hormone | BLOCKED |
| Batch_4_Pass_3.json | inv_vitamin_d_high_vitamin_d_excess_context | vitamin_d→vitamin_d | parathyroid_hormone | BLOCKED |
| Batch_4_Pass_3.json | inv_magnesium_low_hypomagnesemia | magnesium→magnesium | — | OK |
| Batch_4_Pass_3.json | inv_magnesium_high_hypermagnesemia_context | magnesium→magnesium | — | OK |
| Batch_5_Pass_3.json | inv_active_b12_low_b12_depletion | active_b12→active_b12 | mma | BLOCKED |
| Batch_5_Pass_3.json | inv_alp_high_cholestatic_pattern | alp→alp | — | OK |
| Batch_5_Pass_3.json | inv_alp_high_high_bone_turnover_pattern | alp→alp | phosphate | BLOCKED |
| Batch_5_Pass_3.json | inv_alp_low_hypophosphatasia_pattern | alp→alp | phosphate, vitamin_b6 | BLOCKED |
| Batch_5_Pass_3.json | inv_alp_low_nutrient_or_cofactor_deficiency | alp→alp | vitamin_b6 | BLOCKED |
| Batch_5_Pass_3.json | inv_alt_high_hepatocellular_injury_pattern | alt→alt | — | OK |
| Batch_5_Pass_3.json | inv_alt_high_metabolic_steatotic_liver_pattern | alt→alt | — | OK |
| Batch_5_Pass_3.json | inv_alt_high_muscle_source_or_exertional_pattern | alt→alt | — | OK |
| Batch_5_Pass_3.json | inv_apoa1_low_atherogenic_hdl_deficiency | apoa1→apoa1 | — | OK |
| Batch_5_Pass_3.json | inv_apoa1_low_severe_primary_hdl_deficiency_pattern | apoa1→apoa1 | — | OK |
| Batch_5_Pass_3.json | inv_apob_high_atherogenic_particle_excess | apob→apob | — | OK |
| Batch_5_Pass_3.json | inv_apob_high_familial_combined_hyperlipidemia_pattern | apob→apob | — | OK |
| Batch_5_Pass_3.json | inv_apob_low_hypobetalipoproteinemia_or_malabsorption_pattern | apob→apob | — | OK |
| Batch_5_Pass_3.json | inv_apob_apoa1_ratio_high_atherogenic_particle_imbalance | apob_apoa1_ratio→apob_apoa1_ratio | — | OK |
| Batch_5_Pass_3.json | inv_apob_apoa1_ratio_high_insulin_resistance_atherogenic_dyslipidemia | apob_apoa1_ratio→apob_apoa1_ratio | — | OK |
| Batch_5_Pass_3.json | inv_basophil_pct_high_type2_hypersensitivity_inflammation | basophil_pct→basophil_pct | — | OK |
| Batch_5_Pass_3.json | inv_basophil_pct_high_myeloproliferative_signal | basophil_pct→basophil_pct | — | OK |
| Batch_5_Pass_3.json | inv_basophil_pct_low_glucocorticoid_or_acute_stress_pattern | basophil_pct→basophil_pct | — | OK |
| Batch_5_Pass_3.json | inv_basophils_abs_high_type2_hypersensitivity_inflammation | basophils_abs→basophils_abs | — | OK |
| Batch_5_Pass_3.json | inv_basophils_abs_high_myeloproliferative_signal | basophils_abs→basophils_abs | — | OK |
| Batch_5_Pass_3.json | inv_basophils_abs_low_glucocorticoid_or_acute_stress_pattern | basophils_abs→basophils_abs | — | OK |
| Batch_5_Pass_3.json | inv_bilirubin_high_gilbert_pattern | bilirubin→bilirubin | repeat_bilirubin (contradiction) | BLOCKED |
| Batch_5_Pass_3.json | inv_bilirubin_high_hemolytic_turnover_pattern | bilirubin→bilirubin | reticulocytes | BLOCKED |
| Batch_5_Pass_3.json | inv_bilirubin_high_hepatobiliary_excretion_impairment | bilirubin→bilirubin | — | OK |
| Batch_5_Pass_3.json | inv_calcium_high_primary_hyperparathyroid_pattern | calcium→calcium | parathyroid_hormone, phosphate, pth_related_peptide | BLOCKED |
| Batch_5_Pass_3.json | inv_calcium_high_pth_independent_hypercalcemia | calcium→calcium | parathyroid_hormone, pth_related_peptide | BLOCKED |
| Batch_5_Pass_3.json | inv_calcium_low_vitamin_d_or_magnesium_related_hypocalcemia | calcium→calcium | parathyroid_hormone | BLOCKED |
| Batch_5_Pass_3.json | inv_calcium_low_hypoparathyroid_pattern | calcium→calcium | parathyroid_hormone, phosphate | BLOCKED |
| Batch_6_Pass_3.json | inv_chloride_high_hyperchloremic_metabolic_acidosis | chloride→chloride | bicarbonate, anion_gap | BLOCKED |
| Batch_6_Pass_3.json | inv_chloride_low_chloride_depletion_metabolic_alkalosis | chloride→chloride | bicarbonate | BLOCKED |
| Batch_6_Pass_3.json | inv_corrected_calcium_high_pth_mediated_hypercalcemia | corrected_calcium→corrected_calcium | pth, phosphate | BLOCKED |
| Batch_6_Pass_3.json | inv_corrected_calcium_high_malignancy_mediated_hypercalcemia | corrected_calcium→corrected_calcium | pth, phosphate | BLOCKED |
| Batch_6_Pass_3.json | inv_corrected_calcium_low_hypoparathyroid_state | corrected_calcium→corrected_calcium | pth, phosphate | BLOCKED |
| Batch_6_Pass_3.json | inv_corrected_calcium_low_secondary_hyperparathyroid_context | corrected_calcium→corrected_calcium | pth, phosphate | BLOCKED |
| Batch_6_Pass_3.json | inv_cortisol_low_adrenal_insufficiency | cortisol→cortisol | — | OK |
| Batch_6_Pass_3.json | inv_cortisol_high_hypercortisolism | cortisol→cortisol | — | OK |
| Batch_6_Pass_3.json | inv_folate_low_folate_deficiency | folate→folate | — | OK |
| Batch_6_Pass_3.json | inv_folate_high_supplementation_or_excess_exposure | folate→folate | — | OK |
| Batch_6_Pass_3.json | inv_ggt_high_hepatobiliary_cholestatic_context | ggt→ggt | — | OK |
| Batch_6_Pass_3.json | inv_ggt_high_alcohol_or_enzyme_induction_context | ggt→ggt | — | OK |
| Batch_6_Pass_3.json | inv_hba1c_high_diabetes_range_hyperglycemia | hba1c→hba1c | — | OK |
| Batch_6_Pass_3.json | inv_hba1c_low_shortened_erythrocyte_lifespan_context | hba1c→hba1c | — | OK |
| Batch_6_Pass_3.json | inv_hgb_low_iron_deficiency_or_blood_loss_anemia | hgb→hemoglobin | reticulocytes | BLOCKED |
| Batch_6_Pass_3.json | inv_hgb_low_normocytic_underproduction_context | hgb→hemoglobin | — | OK |
| Batch_6_Pass_3.json | inv_hgb_high_erythrocytosis_or_hypoxic_drive | hgb→hemoglobin | erythropoietin | BLOCKED |
| Batch_6_Pass_3.json | inv_homocysteine_high_b_vitamin_related_methylation_impairment | homocysteine→homocysteine | — | OK |
| Batch_6_Pass_3.json | inv_homocysteine_high_renal_clearance_reduction | homocysteine→homocysteine | — | OK |
| Batch_6_Pass_3.json | inv_lym_low_lymphopenia_stress_or_immunosuppression | lym→**UNMAPPED** | wbc_total | BLOCKED |
| Batch_6_Pass_3.json | inv_lym_high_reactive_or_lymphoproliferative_lymphocytosis | lym→**UNMAPPED** | wbc_total | BLOCKED |
| Batch_6_Pass_3.json | inv_mcv_high_megaloblastic_macrocytosis | mcv→mcv | — | OK |
| Batch_6_Pass_3.json | inv_mcv_high_nonmegaloblastic_macrocytosis | mcv→mcv | — | OK |
| Batch_6_Pass_3.json | inv_mcv_low_microcytosis_iron_deficiency | mcv→mcv | rbc_count | BLOCKED |
| Batch_7_Pass_3.json | inv_neutrophils_high_acute_bacterial_inflammatory_response | neutrophils→neutrophils | lym | BLOCKED |
| Batch_7_Pass_3.json | inv_neutrophils_low_marrow_suppression_or_drug_effect | neutrophils→neutrophils | lym | BLOCKED |
| Batch_7_Pass_3.json | inv_non_hdl_high_atherogenic_lipoprotein_burden | non_hdl→**UNMAPPED** | — | BLOCKED |
| Batch_7_Pass_3.json | inv_non_hdl_low_reduced_atherogenic_lipoprotein_pool | non_hdl→**UNMAPPED** | — | BLOCKED |
| Batch_7_Pass_3.json | inv_plt_high_reactive_thrombocytosis | plt→platelets | — | OK |
| Batch_7_Pass_3.json | inv_plt_high_clonal_myeloproliferative_thrombocytosis | plt→platelets | — | OK |
| Batch_7_Pass_3.json | inv_plt_low_peripheral_consumption_or_immune_destruction | plt→platelets | — | OK |
| Batch_7_Pass_3.json | inv_plt_low_marrow_suppression_pattern | plt→platelets | — | OK |
| Batch_7_Pass_3.json | inv_tyg_index_high_insulin_resistance_pattern | tyg_index→tyg_index | — | OK |
| Batch_7_Pass_3.json | inv_urate_high_gout_crystal_deposition_risk | urate→urate | — | OK |
| Batch_7_Pass_3.json | inv_urate_low_reduced_urate_pool_or_renal_loss | urate→urate | — | OK |
| Batch_7_Pass_3.json | inv_urea_high_prerenal_volume_depletion_or_catabolic_load | urea→urea | — | OK |
| Batch_7_Pass_3.json | inv_urea_low_low_protein_or_reduced_urea_cycle_input | urea→urea | — | OK |
| Batch_7_Pass_3.json | inv_wbc_high_reactive_leukocytosis | wbc→white_blood_cells | lym | BLOCKED |
| Batch_7_Pass_3.json | inv_wbc_low_global_leukopenic_suppression | wbc→white_blood_cells | lym | BLOCKED |
| Batch_7_Pass_3.json | inv_wbc_high_possible_clonal_leukocyte_proliferation | wbc→white_blood_cells | — | OK |

---

## 5. Translation-boundary findings

| Category | Description | Risk |
|----------|-------------|------|
| Batch file shape vs validator | `validate_investigation_spec.py` requires root **object**; batch files are **arrays**. Mechanical per-spec validation needs splitting or a batch mode. | **Cautionary** — process/tooling gap, not content quality. |
| Multi-hypothesis + contradictions | v3 `hypotheses`, `contradiction_markers`, `supporting_marker_refs` exceed flat signal_library narrative; promoted-signal-intelligence / intelligence-model contracts must carry or deliberately drop reasoning depth per ADR-008. | **Cautionary / blocked** until mapping rules are explicit. |
| Non-lab `marker_reference` | e.g. `repeat_bilirubin` encodes repeat testing semantics, not a canonical analyte. | **Blocked** for strict metric-level package unless governed as narrative-only or new construct. |
| Specialist / composite IDs | MMA, PTH variants, EPO, JAK2, SPEP, UPCR, FeSat, anion gap — some are analytes, some derived, some tests. | Mix of **governed remap** vs **SSOT expansion** vs **prerequisite sprint**. |
| Primary ID mismatch | `non_hdl`, `lym` do not match resolver/SSOT keys. | **blocked pending remap** or SSOT + upstream editorial pass. |

---

## 6. Recommended ingestion split

**Default (from prompt):** Wave 1 = Batch 3–5 Pass 3; Wave 2 = Batch 6–7 Pass 3.

**Audit adjustment:** Resolver-clean specs are **distributed across both waves** (not only Wave 1). Recommendation:

1. **Ingestion Wave A (lowest risk):** All **67** specs with `OK` in §4, in any batch — **subject to** separate acceptance of where v3 reasoning is truncated for package form.
2. **Wave B (remap-only):** Specs blocked only by **obvious token remaps** (`non_hdl`, `fasting_glucose`, `wbc_total`, possibly `parathyroid_hormone`/`pth` once canonical exists) — after a **single governed alias table** is approved for translation (no silent fixes).
3. **Wave C (prerequisite SSOT / derived-metrics sprint):** Remaining BLOCKED specs depending on new biomarkers, derived metrics, or non-analyte handling.

**Rationale:** Proceeding with “Wave 1 files only” without per-spec filtering would still **mix ingestible and blocked** specs in the same file (e.g. Batch_3 has both OK and BLOCKED entries).

---

## 7. Package-level lineage contract (minimum)

For each future package produced from this tranche, preserve:

1. Source batch filename (e.g. `Batch_5_Pass_3.json`).
2. Source `spec_id` and `signal_id`.
3. `investigation_spec_contract_version`.
4. Primary `biomarker_id` → resolver canonical outcome (or `UNMAPPED:<id>`).
5. Supporting / condition / contradiction marker inventory → canonical or `UNMAPPED`.
6. Explicit list of **governed remap decisions** (upstream token, downstream canonical, authority: e.g. architecture note or SSOT version).
7. Omitted or blocked elements with **reason** (SSOT gap, narrative-only, deferred hypothesis layer).
8. Package production status: **full** / **partial (scoped signal only)** / **not produced**.

---

## 8. Blocker register (prerequisite sprints)

| Blocker | Affected areas | Sprint type |
|---------|----------------|-------------|
| Missing SSOT / alias keys (list in §3) | Iron panels (FeSat), renal electrolytes (bicarb, anion gap, phosphate), PTH family, reticulocytes, IgG, amylase, EPO, genetic/morph flags, etc. | **SSOT expansion** (+ alias registry) |
| Derived / ratio metrics not as canonical keys | e.g. transferrin_saturation, fractional_excretion_magnesium, UPCR | **Derived-metric prerequisite** or explicit biomarker definitions |
| Abbreviation / token drift | `non_hdl`, `lym`, `fasting_glucose` vs estate | **Governed remap table** + optional upstream JSON normalisation |
| Non-analyte semantics in metric slots | `repeat_bilirubin`, SPEP | **KB governance** (narrative-only vs new metric class) |
| Batch validator ergonomics | Array JSON | **Tooling** (batch wrapper) — does not block manual per-spec validation |
| v3 reasoning ↓ package | hypotheses, contradictions, confirmatory_tests, narrative | **Translation contract** (intelligence model / promoted signal intelligence opt-in) |

---

## 9. STOP-condition assessment (prompt § “Hard STOP”)

| Condition | Triggered? | Notes |
|-----------|------------|-------|
| Translation ambiguity | **Partially** | Non-analyte IDs and reasoning depth require explicit downstream homes before full fidelity ingestion. |
| Authority ambiguity | **No** | Upstream paths and SSOT are explicit; resolver is the declared behavioural authority for names. |
| SSOT incompatibility | **Yes** | 50 specs touch unmapped IDs; 4 have unmapped primaries. |
| Derived-metric prerequisite gap | **Yes** | Several blocked items are classic derived/specialist measures absent from resolver output. |
| Hidden behaviour creep | **No** | This audit did not modify runtime, validators, schemas, or translators. |
| Tranche cannot be bounded | **No** | Tranche is finite and enumerable; split by resolver-clean vs blocked is clear. |

**Conclusion:** **Do not author a full-tranche ingestion sprint** until **Wave A/B/C** governance above is accepted. A **narrow** ingestion sprint restricted to the **67 resolver-clean** specs may still need architecture sign-off on **hypothesis/truncation** policy.

---

## 10. Acceptance criteria cross-check (prompt)

| # | Criterion | Met |
|---|-----------|-----|
| 1 | Every spec in Batch 3–7 Pass 3 inventoried | Yes (117). |
| 2 | Primary-marker mapping outcome per spec | Yes (§4). |
| 3 | Supporting-marker compatibility per spec | Yes (included in §4 via unmapped scan). |
| 4 | Alias/remap assessment per spec | Yes (implicit in resolver + §3). |
| 5 | Derived-metric/ratio assessment | Yes (§3, §8). |
| 6 | ingestible / governed / blocked distinguished | Yes (§4, §6). |
| 7 | No package assets created | Yes (audit only). |
| 8 | No runtime/validator/schema/translator edits in this task | Yes. |
| 9 | Recommended tranche split stated | Yes (§6). |
| 10 | Lineage contract stated | Yes (§7). |
| 11 | Ambiguities surfaced as blockers | Yes (§5, §8, §9). |

---

*End of KB-S52A preflight audit.*
