# ARCH-RT-5B — Card Evidence Provenance Audit

**Generated:** 2026-05-30  
**Work package:** ARCH-RT-5B_card_evidence_estate_and_required_provenance

## Provenance classification by promoted artefact

### wave1_cv_lipid_transport

| Marker | Provenance class | Notes |
|--------|------------------|-------|
| ldl_cholesterol | source_document_derived | `inv_ldl_high_dyslipidaemia_v1` via `pkg_s24_ldl_high_dyslipidaemia` |
| hdl_cholesterol | source_document_derived | `inv_hdl_high/low_cardiovascular` via s24 packages |
| triglycerides | source_document_derived | `inv_triglycerides_high_metabolic_v1` |
| total_cholesterol | package_manifest_inferred | No investigation spec — explicitly inferred |
| tc_hdl_ratio | package_manifest_inferred | No investigation spec — explicitly inferred |

**Excluded:** `pkg_lipid_transport` (provenance_gap — not used)

### wave1_cv_homocysteine_pathway

| Marker | Provenance class | Notes |
|--------|------------------|-------|
| homocysteine | source_document_derived | `inv_homocysteine_high_metabolic` via `pkg_s24_homocysteine_high_metabolic`; declared inferred at artefact level |

### wave1_cv_vascular_strain

| Marker | Provenance class | Notes |
|--------|------------------|-------|
| crp | source_document_derived | `inv_crp_high_inflammation_v1` via `pkg_s24_crp_high_inflammation` |

### wave1_met_insulin_metabolic

| Marker | Provenance class | Notes |
|--------|------------------|-------|
| insulin | package_manifest_inferred | No investigation spec — explicitly inferred |
| triglycerides | source_document_derived | `inv_triglycerides_high_metabolic_v1` |

### wave1_liv_enzyme_pattern

| Marker | Provenance class | Notes |
|--------|------------------|-------|
| alt | source_document_derived | `inv_alt_high_hepatocellular_injury_v1` |
| ggt | source_document_derived | `inv_ggt_high_hepatic` |
| ast | package_manifest_inferred | No investigation spec — explicitly inferred |

### wave1_liv_processing_context

| Marker | Provenance class | Notes |
|--------|------------------|-------|
| alp | source_document_derived | `inv_alp_high_bone_biliary` |
| albumin | source_document_derived | `inv_albumin_low_nutritional` |
| bilirubin | package_manifest_inferred | No investigation spec — canonical `bilirubin` id (WAVE1-EQUIV1) |

## Inferred provenance policy compliance

| Check | Status |
|-------|--------|
| Inferred markers declared in artefact `provenance.notes` | **PASS** |
| `source_spec_provenance: inferred_from_package_manifest` on all promoted artefacts | **PASS** |
| No explicit `source_spec_id` claimed for inferred-only markers | **PASS** |
| No PSI runtime dependency | **PASS** |
| No root-cause/hypothesis text as card authority | **PASS** |

## Carry-forwards

- Full 186-package provenance backfill remains deferred to `ARCH-RT-5D`.
- Markers without investigation specs remain on inferred provenance until spec extraction completes.
