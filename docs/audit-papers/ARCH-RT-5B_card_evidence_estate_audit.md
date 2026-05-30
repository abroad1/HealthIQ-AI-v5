# ARCH-RT-5B — Card Evidence Estate Audit

**Generated:** 2026-05-30  
**Work package:** ARCH-RT-5B_card_evidence_estate_and_required_provenance

## Wave 1 subsystem classification

| subsystem_id | domain | Classification | Active authority | Launch classification |
|--------------|--------|----------------|------------------|------------------------|
| `wave1_met_glycaemic_control` | blood_sugar | compiled_card_evidence | compiled YAML + loader | launch_included_compiled |
| `wave1_cv_lipid_transport` | cardiovascular | compiled_card_evidence | compiled YAML + loader | launch_included_compiled |
| `wave1_cv_homocysteine_pathway` | cardiovascular | compiled_card_evidence | compiled YAML + loader | launch_included_compiled |
| `wave1_cv_vascular_strain` | cardiovascular | compiled_card_evidence | compiled YAML + loader | launch_included_compiled |
| `wave1_met_insulin_metabolic` | blood_sugar | compiled_card_evidence | compiled YAML + loader | launch_included_compiled |
| `wave1_liv_enzyme_pattern` | liver | compiled_card_evidence | compiled YAML + loader | launch_included_compiled |
| `wave1_liv_processing_context` | liver | compiled_card_evidence | compiled YAML + loader | launch_included_compiled |

## Estate checks

| Requirement | Status |
|-------------|--------|
| All 7 Wave 1 subsystems classified | **PASS** |
| No unclassified hard-coded authority | **PASS** — `wave1_subsystems_legacy_hard_coded.subsystem_ids` empty |
| Bilirubin / total_bilirubin fix | **PASS** — `wave1_liv_processing_context` uses `bilirubin` only; validator rejects `total_bilirubin` |
| `compile_manifest_ref` resolves for all compiled | **PASS** — 7 manifests under `knowledge_bus/compiled/manifests/` |
| Raw `source_trace` not consumer-visible | **PASS** — frontend render-only; no source_trace display |
| PSI / root-cause / SignalRegistry untouched | **PASS** — no changes in forbidden paths |

## Visibility tier notes

| subsystem_id | visibility_tier | Notes |
|--------------|-----------------|-------|
| `wave1_cv_vascular_strain` | contextual_evidence | Retained contextual tier from legacy classification |

## Outcome

**Complete.** All Wave 1 card evidence subsystems promoted to compiled governed path or explicitly classified. No legacy hard-coded card authority remains active at runtime.
