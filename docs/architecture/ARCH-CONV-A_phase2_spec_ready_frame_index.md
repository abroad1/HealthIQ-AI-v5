# ARCH-CONV-A — Phase 2 Spec-Ready Frame Index (17)

**Work ID:** `ARCH-CONV-A`  
**Date (UTC):** 2026-07-27  
**Purpose:** Index of specification-ready Package A frames authorised for medical-review pack preparation after STOP A.  
**Cursor role:** assemble packs only — **no medical decisions**.

| # | wave | signal_id | source_spec_id | activation_key (proposed) | inv path | STOP B status |
|---:|---|---|---|---|---|---|
| 1 | 1 | signal_tsh_high | inv_tsh_high_hypothyroidism | signal_tsh_high::inv_tsh_high_hypothyroidism | knowledge_bus/research/investigation_specs/inv_tsh_high_hypothyroidism_v1.yaml | **RATIFIED (Wave 1 STOP C)** |
| 2 | 1 | signal_tsh_low | inv_tsh_low_hyperthyroidism | signal_tsh_low::inv_tsh_low_hyperthyroidism | knowledge_bus/research/investigation_specs/inv_tsh_low_hyperthyroidism_v1.yaml | **RATIFIED (Wave 1 STOP C)** |
| 3 | 1 | signal_free_t3_high | inv_free_t3_high_t3_predominant_thyrotoxicosis | signal_free_t3_high::inv_free_t3_high_t3_predominant_thyrotoxicosis | knowledge_bus/research/investigation_specs/inv_free_t3_high_t3_predominant_thyrotoxicosis.yaml | **RATIFIED (Wave 1 STOP C)** |
| 4 | 1 | signal_free_t4_high | inv_free_t4_high_thyrotoxicosis_context | signal_free_t4_high::inv_free_t4_high_thyrotoxicosis_context | knowledge_bus/research/investigation_specs/inv_free_t4_high_thyrotoxicosis_context.yaml | **RATIFIED (Wave 1 STOP C)** |
| 5 | 1 | signal_free_t4_low | inv_free_t4_low_thyroid_hormone_deficiency | signal_free_t4_low::inv_free_t4_low_thyroid_hormone_deficiency | knowledge_bus/research/investigation_specs/inv_free_t4_low_thyroid_hormone_deficiency.yaml | **RATIFIED (Wave 1 STOP C)** |
| 6 | 2 | signal_ldl_cholesterol_high | inv_ldl_high_dyslipidaemia | signal_ldl_cholesterol_high::inv_ldl_high_dyslipidaemia | knowledge_bus/research/investigation_specs/inv_ldl_high_dyslipidaemia_v1.yaml | **RATIFIED (Wave 2 Gate 1/2)** |
| 7 | 2 | signal_hdl_cholesterol_low | inv_hdl_low_cardiovascular | signal_hdl_cholesterol_low::inv_hdl_low_cardiovascular | knowledge_bus/research/investigation_specs/inv_hdl_low_cardiovascular.yaml | **RATIFIED (Wave 2 Gate 1/2)** |
| 8 | 2 | signal_triglycerides_high | inv_triglycerides_high_metabolic | signal_triglycerides_high::inv_triglycerides_high_metabolic | knowledge_bus/research/investigation_specs/inv_triglycerides_high_metabolic_v1.yaml | **RATIFIED (Wave 2 Gate 1/2)** |
| 9 | 3 | signal_creatinine_high | inv_creatinine_high_renal_v1 | signal_creatinine_high::inv_creatinine_high_renal_v1 | knowledge_bus/research/investigation_specs/inv_creatinine_high_renal_v1.yaml | prepared index only |
| 10 | 3 | signal_urea_high | inv_urea_high_renal | signal_urea_high::inv_urea_high_renal | knowledge_bus/research/investigation_specs/inv_urea_high_renal.yaml | prepared index only |
| 11 | 3 | signal_urate_high | inv_uric_acid_high_metabolic | signal_urate_high::inv_uric_acid_high_metabolic | knowledge_bus/research/investigation_specs/inv_uric_acid_high_metabolic.yaml | prepared index only |
| 12 | 4 | signal_ggt_high | inv_ggt_high_hepatic | signal_ggt_high::inv_ggt_high_hepatic | knowledge_bus/research/investigation_specs/inv_ggt_high_hepatic.yaml | prepared index only |
| 13 | 4 | signal_alp_high | inv_alp_high_bone_biliary | signal_alp_high::inv_alp_high_bone_biliary | knowledge_bus/research/investigation_specs/inv_alp_high_bone_biliary.yaml | prepared index only |
| 14 | 5 | signal_ferritin_low | inv_ferritin_low_iron_deficiency | signal_ferritin_low::inv_ferritin_low_iron_deficiency | knowledge_bus/research/investigation_specs/inv_ferritin_spec_v1.yaml | prepared index only |
| 15 | 5 | signal_ferritin_high | inv_ferritin_high_overload_v1 | signal_ferritin_high::inv_ferritin_high_overload_v1 | knowledge_bus/research/investigation_specs/inv_ferritin_high_overload_v1.yaml | prepared index only |
| 16 | 5 | signal_hemoglobin_low | inv_hgb_low_anemia | signal_hemoglobin_low::inv_hgb_low_anemia | knowledge_bus/research/investigation_specs/inv_hgb_low_anemia.yaml | prepared index only |
| 17 | 6 | signal_hba1c_high | inv_hba1c_high_glycaemia_v1 | signal_hba1c_high::inv_hba1c_high_glycaemia_v1 | knowledge_bus/research/investigation_specs/inv_hba1c_high_glycaemia_v1.yaml | prepared index only |

**Not in the 17:** Wave 1 blocked (`signal_thyroid_tsh_context`, `signal_tgab_high`); bilirubin provisional frames (separate research pack, not medically approved); Wave 0 suppressed; Wave 2 blocked (`signal_total_cholesterol_high`, `signal_apoa1_cardio_risk`, `signal_lipid_transport_dysfunction`).

**Identity note (Wave 2):** rows 6 and 8 use embedded canonical `spec_id` values (`inv_ldl_high_dyslipidaemia`, `inv_triglycerides_high_metabolic`). Filename `_v1` suffixes are not activation-key material.

Wave 1 STOP B / STOP C = rows 1–5 complete.  
Wave 2 Gate 1 / Gate 2 = rows 6–8 ratified — see `docs/architecture/ARCH-CONV-A_wave2_lipid_gate1_gate2_decision.md`.
