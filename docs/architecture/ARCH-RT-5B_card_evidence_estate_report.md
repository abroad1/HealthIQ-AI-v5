# ARCH-RT-5B — Card Evidence Estate Report

**Generated:** 2026-05-30  
**Work package:** ARCH-RT-5B_card_evidence_estate_and_required_provenance  
**Authority:** ADR-RT-001, ADR-RT-004, ARCH-RT-3, ARCH-RT-5

## Summary

ARCH-RT-5B promoted all six remaining Wave 1 hard-coded card evidence subsystems to the compiled governed path established by ARCH-RT-3. Every Wave 1 subsystem is now classified and powered by compiled card evidence artefacts with resolving compile manifests.

## Subsystems promoted

| subsystem_id | artefact | manifest |
|--------------|----------|----------|
| wave1_cv_lipid_transport | `wave1_cv_lipid_transport.yaml` | `arch_rt5b_lipid_transport_card_evidence.yaml` |
| wave1_cv_homocysteine_pathway | `wave1_cv_homocysteine_pathway.yaml` | `arch_rt5b_homocysteine_pathway_card_evidence.yaml` |
| wave1_cv_vascular_strain | `wave1_cv_vascular_strain.yaml` | `arch_rt5b_vascular_strain_card_evidence.yaml` |
| wave1_met_insulin_metabolic | `wave1_met_insulin_metabolic.yaml` | `arch_rt5b_insulin_metabolic_card_evidence.yaml` |
| wave1_liv_enzyme_pattern | `wave1_liv_enzyme_pattern.yaml` | `arch_rt5b_enzyme_pattern_card_evidence.yaml` |
| wave1_liv_processing_context | `wave1_liv_processing_context.yaml` | `arch_rt5b_processing_context_card_evidence.yaml` |

## Subsystems retained / classified

| subsystem_id | Classification |
|--------------|----------------|
| wave1_met_glycaemic_control | compiled_card_evidence (ARCH-RT-3 pilot — unchanged) |

No subsystems remain on legacy hard-coded card authority.

## Backend changes

- `backend/core/knowledge/health_system_card_evidence.py` — expanded `WAVE1_COMPILED_SUBSYSTEM_IDS` / `PILOT_COMPILED_SUBSYSTEM_IDS` to all seven Wave 1 subsystems.

## DTO / frontend changes

None required. Existing ARCH-RT-3 DTO v2 fields and render-only frontend components handle multi-subsystem compiled evidence without modification.

## Estate index changes

- `knowledge_bus/compiled/estate_index_v1.yaml` — six new `card_evidence_artefacts` entries; `wave1_subsystems_legacy_hard_coded.subsystem_ids` emptied.

## Tests

| Module | Coverage |
|--------|----------|
| `test_health_system_card_evidence_arch_rt5b.py` | Schema validation, manifest resolution, estate index, loader, assembler, bilirubin regression, provenance boundary |
| `test_health_system_card_evidence_arch_rt3.py` | Updated compiled-path assertions |
| `test_arch_rt5_launch_gate.py` | Updated estate index counts |

## Remaining risks

- Inferred provenance for markers without investigation specs (total_cholesterol, tc_hdl_ratio, insulin, ast, bilirubin) — deferred to ARCH-RT-5D.
- Manifest output hashes marked `pending_inventory_refresh` — inventory refresh sprint follow-on.

## Carry-forwards

- ARCH-RT-5C: hypothesis runtime promotion
- ARCH-RT-5D: package provenance backfill
- ARCH-RT-5E: PSI runtime wiring (only if product mandates)
