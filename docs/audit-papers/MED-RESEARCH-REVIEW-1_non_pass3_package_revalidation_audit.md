# MED-RESEARCH-REVIEW-1 — Non-Pass 3 Package Revalidation Audit

**Work ID:** `MED-RESEARCH-REVIEW-1_non_pass3_package_revalidation`
**Date:** 2026-05-31
**Sprint type:** Audit / classification only (no runtime changes)
**Governance register:** `knowledge_bus/governance/non_pass3_package_revalidation_register_v1.yaml`

---

## Executive verdict

All **55** non–Pass 3 / unclear-provenance packages from the CRP-PASS3-MIGRATION cohort are classified.
**54** are runtime-loaded; **1** (`pkg_example`) is not.
**0** packages are **launch_visible** under current Wave 1 compiled card evidence policy.

**No launch blocker** was identified. Non–Pass 3 runtime packages require Knowledge Bus re-review before being treated as Pass 3–mature launch intelligence.
This does not imply clinical invalidity and does not require user-facing disclosure.

**KBP-0001** is accepted with rationale. **pkg_lipid_transport** requires provenance recovery (CF-MRIMPROVE-004).
**pkg_chronic_inflammation** requires a dedicated Pass 3 frame (CF-CHRONICINFL-001).
**pkg_s24_crp_high_inflammation** remains deferred per CRP authority (CF-CRPPASS3-001).

### Pass 3 primary-biomarker cross-validation (closure)

Repo-grounded scan of all Pass 3 files under `knowledge_bus/research/investigation_specs/multi_llm_research` (`primary_marker.biomarker_id` only). Detail: `docs/audit-papers/MED-RESEARCH-REVIEW-1_pass3_primary_biomarker_cross_validation_addendum.md`.

| Finding | Result |
|---|---:|
| Non–Pass 3 packages with primary biomarker present in Pass 3 | **55 / 55** |
| Packages missing Pass 3 primary biomarker coverage | **0 / 55** |

**Conclusion:** The estate gap is **mostly mapping, compilation, and promotion** — not missing Pass 3 medical research at the primary-biomarker level. KB-UTIL-2 and related workstreams should prioritize governed compile/map from existing Pass 3 specs rather than net-new biomarker research for this cohort.

**Exceptions (unchanged):**

- **`pkg_chronic_inflammation`** — manual-review exception: primary `crp` matches Pass 3 CRP-primary frames (`signal_crp_high`), but those frames are **not equivalent** to runtime authority `signal_systemic_inflammation`. A dedicated Pass 3 frame remains required (CF-CHRONICINFL-001).
- **`pkg_lipid_transport`** — **provenance recovery and mapping** (CF-MRIMPROVE-004): manifest gap; primary `non_hdl_cholesterol` already matches Pass 3 `non_hdl` specs — hygiene and promotion, not greenfield research.

---

## Package cohort summary

| Cohort (`source_type`) | Count |
|---|---:|
| architecture_doc_blocked | 8 |
| investigation_spec_v1_yaml | 31 |
| legacy_retained_with_justification | 1 |
| provenance_gap | 1 |
| research_study_markdown | 3 |
| retire_candidate | 1 |
| unknown_ambiguous | 10 |

---

## CRP / inflammation distinction (confirmed)

Cross-reference: `knowledge_bus/governance/crp_runtime_authority_v1.yaml`.

| Signal | Runtime package(s) | Pass 3? |
|---|---|---|
| `signal_crp_high` | `pkg_s24_crp_high_inflammation` | No — defer CF-CRPPASS3-001 |
| `signal_systemic_inflammation` | `pkg_chronic_inflammation`, KBP-0001 | No — CF-CHRONICINFL-001 |
| `signal_inflammation_crp_context` | `pkg_inflammation_crp_context` | No — internal context |

---

## Launch-relevant findings

No package in this cohort is `launch_visible`. Visible Wave 1 subsystems use Pass 3–compiled card evidence.

---

## Carry-forward register updates

| ID | Update |
|---|---|
| CF-MRIMPROVE-001 | **Resolved** — 55-package classification complete |
| CF-MRIMPROVE-002 | **Deferred** — kb45 cohort classified; KB-UTIL-2 mapping |
| CF-MRIMPROVE-003 | **Deferred** — architecture cohort classified; KB-UTIL-2 extraction |
| CF-MRIMPROVE-004 | **Open** — `pkg_lipid_transport` provenance recovery |
| CF-CHRONICINFL-001 | **Open** — `author_new_pass3_frame` confirmed |
| CF-CRPPASS3-001 | **Open** — CRP s24 deferral confirmed |

---

## Recommended next sprints

1. **KB-UTIL-2** — Pass 3 compile/mapping/promotion for s24, kb45, and architecture cohorts (primary biomarker coverage already exists in Pass 3).
2. **KB hygiene** — `pkg_lipid_transport` provenance recovery + mapping to Pass 3 `non_hdl` frames; `pkg_example` retirement.
3. **Medical research** — dedicated Pass 3 frame for `signal_systemic_inflammation` (not satisfied by CRP-primary Pass 3 specs).

---

## Full 55-package classification table

| package_id | signal_id(s) | source_type | runtime_loaded | launch_relevance | maturity_classification | recommended_action |
|---|---|---|---|---|---|---|
| KBP-0001 | signal_insulin_resistance, signal_lipid_transport_dysfunction, signal_hepatic_metabolic_stress, signal_systemic_inflammation, signal_vascular_inflammatory_stress, signal_renal_metabolic_stress, signal_oxygen_transport_capacity | legacy_retained_with_justification | True | runtime_active_not_visible | accepted_with_rationale | accept_as_currently_valid_with_rationale |
| pkg_b12_deficiency_context | signal_b12_deficiency_context | architecture_doc_blocked | True | internal_only | architecture_anchor_review_required | map_to_existing_pass3_frame |
| pkg_chronic_inflammation | signal_systemic_inflammation | research_study_markdown | True | runtime_active_not_visible | study_derived_revalidation_required | author_new_pass3_frame |
| pkg_example | signal_example_metabolic | retire_candidate | False | not_runtime_loaded | retire_candidate | retire_package |
| pkg_glucose_dysregulation_hba1c_context | signal_glucose_dysregulation_hba1c_context | architecture_doc_blocked | True | internal_only | architecture_anchor_review_required | map_to_existing_pass3_frame |
| pkg_hepatic_alt_context | signal_hepatic_alt_context | architecture_doc_blocked | True | internal_only | architecture_anchor_review_required | map_to_existing_pass3_frame |
| pkg_hepatic_metabolic_stress | signal_hepatic_metabolic_stress | research_study_markdown | True | runtime_active_not_visible | study_derived_revalidation_required | re_run_through_pass3 |
| pkg_homocysteine_elevation_context | signal_homocysteine_elevation_context | architecture_doc_blocked | True | internal_only | architecture_anchor_review_required | map_to_existing_pass3_frame |
| pkg_inflammation_crp_context | signal_inflammation_crp_context | architecture_doc_blocked | True | internal_only | architecture_anchor_review_required | map_to_existing_pass3_frame |
| pkg_insulin_resistance | signal_insulin_resistance | research_study_markdown | True | runtime_active_not_visible | study_derived_revalidation_required | re_run_through_pass3 |
| pkg_iron_deficiency_context | signal_iron_deficiency_context | architecture_doc_blocked | True | internal_only | architecture_anchor_review_required | map_to_existing_pass3_frame |
| pkg_iron_overload_context | signal_iron_overload_context | architecture_doc_blocked | True | internal_only | architecture_anchor_review_required | map_to_existing_pass3_frame |
| pkg_kb45_active_b12_low_deficiency | signal_active_b12_deficiency | unknown_ambiguous | True | runtime_active_not_visible | batch_json_lineage_review_required | map_to_existing_pass3_frame |
| pkg_kb45_apoa1_low_cardio_risk | signal_apoa1_cardio_risk | unknown_ambiguous | True | runtime_active_not_visible | batch_json_lineage_review_required | map_to_existing_pass3_frame |
| pkg_kb45_apob_apoa1_ratio_high_imbalance | signal_lipid_imbalance | unknown_ambiguous | True | runtime_active_not_visible | batch_json_lineage_review_required | map_to_existing_pass3_frame |
| pkg_kb45_apob_high_atherogenic | signal_apob_atherogenic | unknown_ambiguous | True | runtime_active_not_visible | batch_json_lineage_review_required | map_to_existing_pass3_frame |
| pkg_kb45_basophil_pct_high_basophilia | signal_basophilia_pct | unknown_ambiguous | True | runtime_active_not_visible | batch_json_lineage_review_required | map_to_existing_pass3_frame |
| pkg_kb45_basophils_abs_high_basophilia | signal_basophilia_abs | unknown_ambiguous | True | runtime_active_not_visible | batch_json_lineage_review_required | map_to_existing_pass3_frame |
| pkg_kb45_bilirubin_high_hyperbilirubinemia | signal_hyperbilirubinemia | unknown_ambiguous | True | runtime_active_not_visible | batch_json_lineage_review_required | map_to_existing_pass3_frame |
| pkg_kb45_chloride_high_hyperchloremia | signal_hyperchloremia | unknown_ambiguous | True | runtime_active_not_visible | batch_json_lineage_review_required | map_to_existing_pass3_frame |
| pkg_kb45_corrected_calcium_high_hypercalcemia | signal_hypercalcemia | unknown_ambiguous | True | runtime_active_not_visible | batch_json_lineage_review_required | map_to_existing_pass3_frame |
| pkg_kb45_cortisol_high_hypercortisolism | signal_hypercortisolism | unknown_ambiguous | True | runtime_active_not_visible | batch_json_lineage_review_required | map_to_existing_pass3_frame |
| pkg_lipid_transport | signal_lipid_transport_dysfunction | provenance_gap | True | runtime_active_not_visible | provenance_gap | recover_provenance |
| pkg_s24_albumin_low_nutritional | signal_albumin_low | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_alp_high_bone_biliary | signal_alp_high | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_alt_high_hepatocellular_injury | signal_alt_high | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_calcium_high_endocrine | signal_calcium_high | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_creatinine_high_renal | signal_creatinine_high | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_crp_high_inflammation | signal_crp_high | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | defer_with_reason |
| pkg_s24_ferritin_high_overload | signal_ferritin_high | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_ferritin_low_iron_deficiency | signal_ferritin_low | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_folate_low_deficiency | signal_folate_low | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_ggt_high_hepatic | signal_ggt_high | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_hba1c_high_glycaemia | signal_hba1c_high | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_hdl_high_cardiovascular | signal_hdl_cholesterol_high | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_hdl_low_cardiovascular | signal_hdl_cholesterol_low | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_hgb_low_anemia | signal_hemoglobin_low | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_homocysteine_high_metabolic | signal_homocysteine_high | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_ldl_high_dyslipidaemia | signal_ldl_cholesterol_high | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_lym_high_lymphocytosis | signal_lymphocytes_high | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_mcv_high_macrocytosis | signal_mcv_high | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_neutrophils_high_neutrophilia | signal_neutrophils_high | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_neutrophils_low_neutropenia | signal_neutrophils_low | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_plt_high_thrombocytosis | signal_platelets_high | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_plt_low_thrombocytopenia | signal_platelets_low | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_triglycerides_high_metabolic | signal_triglycerides_high | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_tsh_high_hypothyroidism | signal_tsh_high | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_tsh_low_hyperthyroidism | signal_tsh_low | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_urate_high_metabolic | signal_urate_high | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_urea_high_renal | signal_urea_high | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_vitamin_b12_low_deficiency | signal_vitamin_b12_low | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_vitamin_d_low_deficiency | signal_vitamin_d_low | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_wbc_high_leukocytosis | signal_wbc_high | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_s24_wbc_low_leukopenia | signal_wbc_low | investigation_spec_v1_yaml | True | runtime_active_not_visible | non_pass3_runtime_revalidation_required | re_run_through_pass3 |
| pkg_thyroid_tsh_context | signal_thyroid_tsh_context | architecture_doc_blocked | True | internal_only | architecture_anchor_review_required | map_to_existing_pass3_frame |

---

## Confirmation

Audit documentation and governance classification only. No production code, packages, or runtime behaviour changed.
