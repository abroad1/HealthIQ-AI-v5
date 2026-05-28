# Package Generation Inventory

**Work package:** ARCH-RT-0  
**Generated:** 2026-05-28  
**Method:** Read-only scan of `knowledge_bus/packages/pkg_*/package_manifest.yaml` (186 manifests). Command:

```powershell
python -c "<inventory script — see ARCH-RT-0 evidence report>"
```

## Summary

| Metric | Count |
|--------|------:|
| `pkg_*` directories with `package_manifest.yaml` | 186 |
| Includes `pkg_example` | yes (1) |
| Excludes `pkg_example` from runtime load | yes (`SignalRegistry` skips `pkg_example`) |
| Additional non-`pkg_*` package folder | `knowledge_bus/packages/KBP-0001/` (legacy; 7 signals; not in manifest corpus below) |

## Counts by generation / prefix

| Generation / prefix | Package count | Notes |
|---------------------|--------------:|-------|
| `pkg_kb52c_` | 67 | Pass 3 batch (`Batch_*_Pass_3.json`); LC-S18A `post_kb_s49_unreviewed_batch` |
| `pkg_s24_` | 31 | Sprint-24; individual `inv_*.yaml` `source_document` |
| `pkg_kb58_` | 22 | CBC / haematology Pass 3 |
| `pkg_kb47_` | 20 | KB-S47 ingest; **all 20** have PSI on disk + manifest opt-in |
| `pkg_kb45_` | 10 | `investigation-spec-collection-batch1-10.json` |
| `pkg_kb60_` | 7 | Lipid-derived Pass 3 |
| `pkg_kb56_` | 5 | Pass 3 |
| `pkg_kb52d_` | 4 | Pass 3 |
| `pkg_kb59_` | 4 | Thyroid antibodies Pass 3 |
| `pkg_kb61_` | 3 | Transferrin Pass 3 |
| `pkg_kb52_` (no c/d suffix) | 0 | No packages on disk |
| Legacy / context (no sprint prefix) | 13 | See list below |
| **Total** | **186** | |

**Legacy / context packages (13):** `pkg_b12_deficiency_context`, `pkg_chronic_inflammation`, `pkg_glucose_dysregulation_hba1c_context`, `pkg_hepatic_alt_context`, `pkg_hepatic_metabolic_stress`, `pkg_homocysteine_elevation_context`, `pkg_inflammation_crp_context`, `pkg_insulin_resistance`, `pkg_iron_deficiency_context`, `pkg_iron_overload_context`, `pkg_lipid_transport`, `pkg_thyroid_tsh_context`, `pkg_example`.

## Provenance by `source_document` pattern

| Pattern class | Count | Detection rule |
|---------------|------:|----------------|
| Batch JSON (`*.json`, `multi_llm_research/`) | 142 | `source_document` ends with `.json` or contains `multi_llm_research` |
| Individual investigation spec (`inv_*.yaml`) | 31 | All `pkg_s24_*` |
| Architecture doc | 8 | `HealthIQ_Investigation_Layer.md` |
| Study markdown | 3 | `knowledge_bus/research/study_*.md` |
| Missing `source_document` | 2 | `pkg_lipid_transport`, `pkg_example` |
| **`source_spec_id` on manifest** | **0** | Field absent on all 186 manifests |

## Per-generation detail (required columns)

| Generation | Count | Typical `source_document` | `schema_version` (manifest) | PSI on disk | PSI manifest opt-in | `source_spec_id` | Batch JSON | Individual spec | Unknown source |
|------------|------:|---------------------------|----------------------------|------------:|--------------------:|-----------------:|-----------:|----------------:|---------------:|
| `pkg_kb52c` | 67 | `multi_llm_research/Batch_*_Pass_3.json` | Usually absent; signal lib `2.0.0` | 0 | 0 | 0 | 67 | 0 | 0 |
| `pkg_s24` | 31 | `knowledge_bus/research/investigation_specs/inv_*.yaml` | Absent; signal lib `1.0.0` | 0 | 0 | 0 | 0 | 31 | 0 |
| `pkg_kb58` | 22 | `cbc_hematology_pass_3.json` etc. | Absent; signal lib `2.0.0` | 0 | 0 | 0 | 22 | 0 | 0 |
| `pkg_kb47` | 20 | `Batch_2_Pass_3_Rev1.json` etc. | PSI file `schema_version: 1.0.0` | 20 | 20 | 0 | 20 | 0 | 0 |
| `pkg_kb45` | 10 | `investigation-spec-collection-batch1-10.json` | Signal lib `2.0.0` | 0 | 0 | 0 | 10 | 0 | 0 |
| `pkg_kb60` | 7 | Batch JSON | Signal lib `2.0.0` | 0 | 0 | 0 | 7 | 0 | 0 |
| `pkg_kb56` | 5 | Batch JSON | Signal lib `2.0.0` | 0 | 0 | 0 | 5 | 0 | 0 |
| `pkg_kb52d` | 4 | Batch JSON | Signal lib `2.0.0` | 0 | 0 | 0 | 4 | 0 | 0 |
| `pkg_kb59` | 4 | Batch JSON | Signal lib `2.0.0` | 0 | 0 | 0 | 4 | 0 | 0 |
| `pkg_kb61` | 3 | Batch JSON | Signal lib `2.0.0` | 0 | 0 | 0 | 3 | 0 | 0 |
| Legacy / context | 13 | Mixed (8 arch doc, 3 study, 2 missing) | Signal lib `1.0.0` typical | 0 | 0 | 0 | 0 | 0 | 2 |

## Schema reference

- Package manifest schema: `knowledge_bus/schema/package_manifest_schema.yaml` (`schema_version: "1.0.0"`).
- Signal library versions observed: `1.0.0` (legacy/s24), `2.0.0` (ingested Pass 3 / kb45+).

## LC-S18A cross-reference

Per `docs/audit-papers/LC-S18A_package_estate_inventory_delta_report.md`, **112** post–KB-S49 packages are inventory-registered with `runtime_loaded: false` and `requires_review: true`. Prefixes: kb52c (67), kb58 (22), kb60 (7), kb56 (5), kb52d (4), kb59 (4), kb61 (3).

## Uncertainty

- Per-package `schema_version` on manifest is often absent; signal library `version` field used where present.
- Frame-level `spec_id` inside batch JSON is not surfaced on manifests (see `activation_compile_gap_report.md`).
