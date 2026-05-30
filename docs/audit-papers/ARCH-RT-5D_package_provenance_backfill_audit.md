# ARCH-RT-5D — Package Provenance Backfill Audit

**Generated:** 2026-05-30  
**Scan:** `package_provenance_scan_v1.scan_all_package_provenance()`

## Package estate summary

| Metric | Count |
|--------|------:|
| Total `package_manifest.yaml` files | **186** |
| Explicit `source_spec_id` on manifest | **0** |
| `activation_key` on manifest | **0** |
| Packages updated (manifest fields) | **0** |

Classification is recorded in this audit and the unresolved register. No package clinical content or signal thresholds were modified.

## Classification counts

| Classification | Count | Notes |
|----------------|------:|-------|
| `batch_json_blocked_pending_spec_extraction` | 142 | Batch JSON `source_document` (kb52c, kb52d, kb45, kb47, kb58, kb60, kb56, kb59, kb61) |
| `source_document_derived` | 31 | All `pkg_s24_*` → individual `inv_*.yaml` paths |
| `architecture_doc_source_blocked` | 11 | 8× `HealthIQ_Investigation_Layer.md` + 3× `study_*.md` |
| `provenance_gap` | 1 | `pkg_lipid_transport` (no `source_document`) |
| `retire_candidate` | 1 | `pkg_example` |
| **Total** | **186** | All packages classified |

## Explicit vs inferred

| Status | Count |
|--------|------:|
| Explicit `source_spec_id` on manifest | 0 |
| Inferred from `source_document` path (not written to manifest) | 31 |
| Batch JSON frame/spec in JSON only | 142 |

Inferred provenance is **not** upgraded to explicit manifest fields.

## kb52c / batch JSON

| Prefix | Count | Classification |
|--------|------:|----------------|
| `pkg_kb52c_*` | 67 | `batch_json_blocked_pending_spec_extraction` |
| `pkg_kb52d_*` | 4 | `batch_json_blocked_pending_spec_extraction` |
| Other batch cohorts | 71 | Same (kb45, kb47, kb58, kb60, kb56, kb59, kb61) |

Extraction of per-frame `spec_id` from batch JSON is **out of scope** for this sprint.

## Five inferred card markers (ARCH-RT-5B carry-forward)

| Marker | Classification | Launch blocker |
|--------|----------------|--------------|
| `total_cholesterol` | `package_manifest_inferred` | No — card artefact declares inferred |
| `tc_hdl_ratio` | `package_manifest_inferred` | No |
| `insulin` | `package_manifest_inferred` | No |
| `ast` | `package_manifest_inferred` | No |
| `bilirubin` | `package_manifest_inferred` | No (canonical `bilirubin`; WAVE1-EQUIV1) |

No investigation spec exists for these markers; classifications **confirmed**, not resolved to explicit.

## Packages not updated

All 186 packages retain existing manifest bodies. Provenance metadata additions were deferred where they would require fabricating `source_spec_id` or bulk-touching clinical packages without mechanical verification benefit beyond this audit.

## Runtime behaviour

**No runtime modules changed** except governed validator/schema (`validate_compile_manifest.py`, `compile_manifest_schema_v1.yaml`) and read-only scan helper (`package_provenance_scan_v1.py`).
