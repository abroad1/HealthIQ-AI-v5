# ARCH-RT-5D — Unresolved Provenance Register

**Generated:** 2026-05-30

## Launch-critical compiled artefacts (resolved hashes)

| Item id | Artefact | Classification | Reason | Future action | Launch blocker |
|---------|----------|----------------|--------|---------------|----------------|
| RT5D-MAN-001 | 8 launch compile manifests | hashes refreshed | Were `pending_inventory_refresh` | Re-run on artefact change | No |

## Batch JSON packages (142)

| Item id | Package/artefact | Classification | Reason | Future action | Launch blocker |
|---------|------------------|----------------|--------|---------------|----------------|
| RT5D-BATCH-* | `pkg_kb52c_*` (67) + other batch cohorts (75) | `batch_json_blocked_pending_spec_extraction` | Frame `spec_id` only inside JSON | Bounded batch extraction compiler (ARCH-RT-5D out of scope) | No for current Wave 1 launch slices |

## Architecture / study sourced packages (11)

| Item id | Package | Classification | Reason | Future action | Launch blocker |
|---------|---------|----------------|--------|---------------|----------------|
| RT5D-ARCH-001 | Legacy context packages (8) | `architecture_doc_source_blocked` | `HealthIQ_Investigation_Layer.md` source | Map to investigation specs or retire | No |
| RT5D-STUDY-001 | `pkg_insulin_resistance` etc. (3) | `architecture_doc_source_blocked` | `study_*.md` source | Spec extraction or retirement | No |

## Provenance gaps

| Item id | Package/marker | Classification | Reason | Future action | Launch blocker |
|---------|----------------|----------------|--------|---------------|----------------|
| RT5D-GAP-001 | `pkg_lipid_transport` | `provenance_gap` | No `source_document` on manifest | Add governed source or retire; do not use as card provenance | No (card uses s24 packages) |
| RT5D-GAP-002 | `pkg_example` | `retire_candidate` | Example package | Remove from estate when approved | No |

## Five inferred card markers

| Item id | Marker | Classification | Reason | Future action | Launch blocker |
|---------|--------|----------------|--------|---------------|----------------|
| RT5D-CARD-001 | `total_cholesterol` | `package_manifest_inferred` | No `inv_*` spec | ARCH-RT-5D follow-on spec authoring | No |
| RT5D-CARD-002 | `tc_hdl_ratio` | `package_manifest_inferred` | No `inv_*` spec | Same | No |
| RT5D-CARD-003 | `insulin` | `package_manifest_inferred` | No `inv_*` spec | Same | No |
| RT5D-CARD-004 | `ast` | `package_manifest_inferred` | No `inv_*` spec | Same | No |
| RT5D-CARD-005 | `bilirubin` | `package_manifest_inferred` | No `inv_*` spec; canonical id `bilirubin` | Same; never `total_bilirubin` | No |

## Explicit provenance estate-wide

| Item id | Scope | Classification | Reason | Future action | Launch blocker |
|---------|-------|----------------|--------|---------------|----------------|
| RT5D-EXP-001 | All 186 manifests | No explicit `source_spec_id` field | Field absent by design until backfill | Add only with verified explicit provenance | No for current pilots |
