# KB-MAP-1 — Pass 3 to Legacy Package Mapping and Promotion Plan

**Work ID:** `KB-MAP-1_pass3_to_legacy_package_mapping_and_promotion_plan`
**Date:** 2026-05-31
**Type:** Planning / classification only (no runtime changes)
**Machine plan:** `knowledge_bus/governance/pass3_legacy_package_mapping_plan_v1.yaml`

---

## Executive verdict

All **55** non–Pass 3 packages are mapped to Pass 3 primary-biomarker coverage (MED-RESEARCH-REVIEW-1). This sprint assigns **promotion routes** and **transition states** per `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md`.

The estate problem is **research present → not mapped → not compiled → not promoted**; not missing Pass 3 primary biomarker research.

- Pass 3 files scanned: **10**
- Exact single-signal Pass 3 `signal_id` match (compile-ready candidates): **24**
- Primary biomarker match without exact `signal_id` match: **31**
- Multiple Pass 3 frames requiring adjudication: **39**

**No launch blocker.** No runtime, package, or production code changes.

### Route classification counts

| Route | Count |
|---|---:|
| ROUTE_A_exact_signal_match_compile_candidate | 13 |
| ROUTE_B_primary_biomarker_match_signal_mapping_needed | 3 |
| ROUTE_C_multiple_pass3_frames_adjudication_needed | 35 |
| ROUTE_D_legacy_accepted_with_rationale | 1 |
| ROUTE_E_provenance_recovery_needed | 1 |
| ROUTE_F_retire_candidate | 1 |
| ROUTE_G_manual_medical_review_exception | 1 |

### Recommended pilot set (5–6 packages)

- `pkg_s24_creatinine_high_renal` — ROUTE_A (exact `signal_id` match; compile pilot)
- `pkg_s24_ferritin_low_iron_deficiency` — ROUTE_A (s24 legacy → Pass 3 compile)
- `pkg_kb45_apob_high_atherogenic` — ROUTE_C (kb45 batch lineage; multi-frame adjudication)
- `pkg_hepatic_alt_context` — ROUTE_C (architecture anchor; mapping/adjudication)
- `pkg_lipid_transport` — ROUTE_E (provenance recovery + Pass 3 `non_hdl` mapping)
- `pkg_chronic_inflammation` — ROUTE_G (manual comparator; not for promotion)

### Manual-review exceptions

- `pkg_chronic_inflammation` — CRP-primary Pass 3 ≠ `signal_systemic_inflammation` (ROUTE_G)
- `KBP-0001` — multi-signal legacy baseline (ROUTE_D)

### Provenance recovery

- `pkg_lipid_transport` — ROUTE_E; Pass 3 `non_hdl` exists; manifest hygiene first

### Retire

- `pkg_example` — ROUTE_F

### Recommended next sprint

**KB-UTIL-2-PILOT** (or equivalent): promotion pilot on ROUTE_A packages from pilot set; parallel provenance hygiene for `pkg_lipid_transport`.

---

## Full 55-package mapping table

| package_id | signals | primary biomarker(s) | transition_state | route | exact signal match | multiple frames | pilot |
|---|---|---|---|---|:---:|:---:|:---:|
| KBP-0001 | signal_hepatic_metabolic_stress, signal_insulin_resistance… | ast_alt_ratio, crp, hemoglobin, non_hdl_cholesterol, tyg_index, urea_creatinine_ratio | accepted_with_rationale | ROUTE_D_legacy_accepted_with_rationale | no | yes | no |
| pkg_b12_deficiency_context | signal_b12_deficiency_context | vitamin_b12 | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_chronic_inflammation | signal_systemic_inflammation | crp | runtime_active_legacy | ROUTE_G_manual_medical_review_exception | no | yes | yes |
| pkg_example | signal_example_metabolic | triglycerides | retired | ROUTE_F_retire_candidate | no | yes | no |
| pkg_glucose_dysregulation_hba1c_context | signal_glucose_dysregulation_hba1c_context | hba1c | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_hepatic_alt_context | signal_hepatic_alt_context | alt | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_hepatic_metabolic_stress | signal_hepatic_metabolic_stress | tyg_index | research_present_unmapped | ROUTE_B_primary_biomarker_match_signal_mapping_needed | no | no | yes |
| pkg_homocysteine_elevation_context | signal_homocysteine_elevation_context | homocysteine | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_inflammation_crp_context | signal_inflammation_crp_context | crp | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_insulin_resistance | signal_insulin_resistance | tyg_index | research_present_unmapped | ROUTE_B_primary_biomarker_match_signal_mapping_needed | no | no | yes |
| pkg_iron_deficiency_context | signal_iron_deficiency_context | ferritin | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_iron_overload_context | signal_iron_overload_context | ferritin | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_kb45_active_b12_low_deficiency | signal_active_b12_deficiency | active_b12 | research_present_unmapped | ROUTE_B_primary_biomarker_match_signal_mapping_needed | no | no | yes |
| pkg_kb45_apoa1_low_cardio_risk | signal_apoa1_cardio_risk | apoa1 | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_kb45_apob_apoa1_ratio_high_imbalance | signal_lipid_imbalance | apob_apoa1_ratio | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_kb45_apob_high_atherogenic | signal_apob_atherogenic | apob | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_kb45_basophil_pct_high_basophilia | signal_basophilia_pct | basophil_pct | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_kb45_basophils_abs_high_basophilia | signal_basophilia_abs | basophils_abs | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_kb45_bilirubin_high_hyperbilirubinemia | signal_hyperbilirubinemia | bilirubin | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_kb45_chloride_high_hyperchloremia | signal_hyperchloremia | chloride | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_kb45_corrected_calcium_high_hypercalcemia | signal_hypercalcemia | corrected_calcium | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_kb45_cortisol_high_hypercortisolism | signal_hypercortisolism | cortisol | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_lipid_transport | signal_lipid_transport_dysfunction | non_hdl_cholesterol | runtime_active_legacy | ROUTE_E_provenance_recovery_needed | no | yes | yes |
| pkg_s24_albumin_low_nutritional | signal_albumin_low | albumin | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | yes | yes | no |
| pkg_s24_alp_high_bone_biliary | signal_alp_high | alp | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | yes | yes | no |
| pkg_s24_alt_high_hepatocellular_injury | signal_alt_high | alt | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | yes | yes | no |
| pkg_s24_calcium_high_endocrine | signal_calcium_high | calcium | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | yes | yes | no |
| pkg_s24_creatinine_high_renal | signal_creatinine_high | creatinine | research_present_uncompiled | ROUTE_A_exact_signal_match_compile_candidate | yes | no | yes |
| pkg_s24_crp_high_inflammation | signal_crp_high | crp | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | yes | yes | yes |
| pkg_s24_ferritin_high_overload | signal_ferritin_high | ferritin | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | yes | yes | no |
| pkg_s24_ferritin_low_iron_deficiency | signal_ferritin_low | ferritin | research_present_uncompiled | ROUTE_A_exact_signal_match_compile_candidate | yes | no | yes |
| pkg_s24_folate_low_deficiency | signal_folate_low | folate | research_present_uncompiled | ROUTE_A_exact_signal_match_compile_candidate | yes | no | yes |
| pkg_s24_ggt_high_hepatic | signal_ggt_high | ggt | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | yes | yes | no |
| pkg_s24_hba1c_high_glycaemia | signal_hba1c_high | hba1c | research_present_uncompiled | ROUTE_A_exact_signal_match_compile_candidate | yes | no | yes |
| pkg_s24_hdl_high_cardiovascular | signal_hdl_cholesterol_high | hdl_cholesterol | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_s24_hdl_low_cardiovascular | signal_hdl_cholesterol_low | hdl_cholesterol | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_s24_hgb_low_anemia | signal_hemoglobin_low | hemoglobin | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_s24_homocysteine_high_metabolic | signal_homocysteine_high | homocysteine | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | yes | yes | no |
| pkg_s24_ldl_high_dyslipidaemia | signal_ldl_cholesterol_high | ldl_cholesterol | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_s24_lym_high_lymphocytosis | signal_lymphocytes_high | lymphocytes | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_s24_mcv_high_macrocytosis | signal_mcv_high | mcv | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | yes | yes | no |
| pkg_s24_neutrophils_high_neutrophilia | signal_neutrophils_high | neutrophils | research_present_uncompiled | ROUTE_A_exact_signal_match_compile_candidate | yes | no | yes |
| pkg_s24_neutrophils_low_neutropenia | signal_neutrophils_low | neutrophils | research_present_uncompiled | ROUTE_A_exact_signal_match_compile_candidate | yes | no | yes |
| pkg_s24_plt_high_thrombocytosis | signal_platelets_high | platelets | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_s24_plt_low_thrombocytopenia | signal_platelets_low | platelets | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |
| pkg_s24_triglycerides_high_metabolic | signal_triglycerides_high | triglycerides | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | yes | yes | no |
| pkg_s24_tsh_high_hypothyroidism | signal_tsh_high | tsh | research_present_uncompiled | ROUTE_A_exact_signal_match_compile_candidate | yes | no | yes |
| pkg_s24_tsh_low_hyperthyroidism | signal_tsh_low | tsh | research_present_uncompiled | ROUTE_A_exact_signal_match_compile_candidate | yes | no | yes |
| pkg_s24_urate_high_metabolic | signal_urate_high | urate | research_present_uncompiled | ROUTE_A_exact_signal_match_compile_candidate | yes | no | yes |
| pkg_s24_urea_high_renal | signal_urea_high | urea | research_present_uncompiled | ROUTE_A_exact_signal_match_compile_candidate | yes | no | yes |
| pkg_s24_vitamin_b12_low_deficiency | signal_vitamin_b12_low | vitamin_b12 | research_present_uncompiled | ROUTE_A_exact_signal_match_compile_candidate | yes | no | yes |
| pkg_s24_vitamin_d_low_deficiency | signal_vitamin_d_low | vitamin_d | research_present_uncompiled | ROUTE_A_exact_signal_match_compile_candidate | yes | no | yes |
| pkg_s24_wbc_high_leukocytosis | signal_wbc_high | white_blood_cells | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | yes | yes | no |
| pkg_s24_wbc_low_leukopenia | signal_wbc_low | white_blood_cells | research_present_uncompiled | ROUTE_A_exact_signal_match_compile_candidate | yes | no | yes |
| pkg_thyroid_tsh_context | signal_thyroid_tsh_context | tsh | runtime_active_legacy | ROUTE_C_multiple_pass3_frames_adjudication_needed | no | yes | no |

---

## Confirmation

Docs and governance classification only.
