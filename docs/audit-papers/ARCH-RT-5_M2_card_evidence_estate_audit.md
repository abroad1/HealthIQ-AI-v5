# ARCH-RT-5 M2 — Card Evidence Estate Audit

**Generated:** 2026-05-30

## Wave 1 subsystem authority

| subsystem_id | domain | Active authority | Launch classification |
|--------------|--------|------------------|------------------------|
| `wave1_met_glycaemic_control` | blood_sugar | **compiled_card_evidence** | launch_included_compiled |
| `wave1_cv_lipid_transport` | cardiovascular | hard_coded_python | legacy_retained_with_justification |
| `wave1_cv_homocysteine_pathway` | cardiovascular | hard_coded_python | legacy_retained_with_justification |
| `wave1_cv_vascular_strain` | cardiovascular | hard_coded_python | legacy_retained_with_justification |
| `wave1_met_insulin_metabolic` | blood_sugar | hard_coded_python | legacy_retained_with_justification |
| `wave1_liv_enzyme_pattern` | liver | hard_coded_python | legacy_retained_with_justification |
| `wave1_liv_processing_context` | liver | hard_coded_python | legacy_retained_with_justification |

## Checks

| Requirement | Status |
|-------------|--------|
| No unclassified hard-coded authority | **PASS** — 6/7 explicitly `legacy_retained_with_justification` |
| Bilirubin / total_bilirubin fix | **PASS** — `wave1_liv_processing_context` expects `bilirubin` only |
| `compile_manifest_ref` real for compiled pilot | **PASS** — links to `arch_rt3_glycaemic_card_evidence.yaml` |
| Raw `source_trace` not consumer-visible | **PASS** — frontend filters internal traces (ARCH-RT-3) |

## M2 outcome

**Complete for launch gate.** Full card estate regeneration for remaining 6 subsystems: **deferred_non_launch_blocker** (follow-on `ARCH-RT-5B` recommended in split doc).
