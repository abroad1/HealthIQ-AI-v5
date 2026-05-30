# LAUNCH-CORE-3 — Result Versioning, Replay and Regeneration Policy

**Status:** LOCKED (launch policy)  
**Work package:** `LAUNCH-CORE-3_result_versioning_replay_and_regeneration_policy`  
**Generated:** 2026-05-30

## Immutable result principle

Generated client-result payloads (`client_result_shape_v1` in `AnalysisResult.processing_metadata`) are **immutable snapshots**. The system must **never** silently overwrite, mutate, or refresh a stored result in place when engine, estate, or presentation policy changes.

## Deterministic replay principle

Given identical inputs and identical engine/estate/schema versions, the pipeline must reproduce the same analytical outcome. `replay_manifest` (ReplayManifestV1) captures registry hashes and policy versions for this purpose on **new** runs.

## Versioned regeneration model

Regeneration is **not** destructive refresh:

```text
same raw input + same questionnaire + same engine/estate versions
  → reproducible original snapshot (read-only)

same raw input + same questionnaire + newer engine/estate versions
  → NEW analysis_id / NEW result_version lineage (future)
```

Required lineage fields (target contract — partial today):

| Field | Today |
|-------|--------|
| `analysis_id` | Yes (`analyses.id`) |
| `result_version` (DTO schema) | Yes (`analysis_results.result_version`, default `1.0.0`) |
| `replay_manifest` | Yes (JSON column + DTO) |
| `raw_biomarkers` | Yes (`analyses.raw_biomarkers`) |
| `questionnaire_data` | Yes (`analyses.questionnaire_data`) |
| `engine_version` / `pipeline_version` | Partial (`analyses.analysis_version`, `pipeline_version`) |
| `result_version_id` / parent linkage | **No** — single snapshot per analysis |
| `supersedes_*` / `superseded_by_*` | **No** |
| `raw_input_hash` / payload hashes | **No** (not persisted on analysis row) |
| `knowledge_estate_index_hash` | Partial (inside replay manifest components when stamped) |
| `active_authority_manifest_hash` | **No** |

## Current repository support

| Path | Role |
|------|------|
| `POST /api/analysis/start` | Runs pipeline; stores `client_result_shape_v1` snapshot |
| `GET /api/analysis/result` | Returns `build_analysis_result_dto` + `result_versioning` metadata (LAUNCH-CORE-3) |
| `PersistenceService.save_live_analysis_after_run` | Writes immutable snapshot to `processing_metadata` |
| `core/dto/persisted_replay_contract_v1.py` | LC-S20 compatibility + stale version checks |
| `core/dto/result_versioning_policy_v1.py` | LAUNCH-CORE-3 stale heuristics + API metadata |

**Deterministic full replay from stored snapshot alone:** not implemented (LC-S20 tests document gap).  
**Deterministic re-run from raw input:** feasible — `raw_biomarkers` + `questionnaire_data` retained on `analyses` row.

## Stale-result detection rule

A persisted result is **stale** when any of:

1. `result_version` ≠ current (`1.0.0`)
2. `replay_manifest` missing or manifest version mismatch
3. `meta.completeness_policy_id` missing or ≠ `launch_core_1_subsystem_union_v1` (LAUNCH-CORE-1)
4. Card `evidence_completeness_*` disagrees with union of subsystem included/missing markers
5. Legacy subsystem `source_trace` prefix `wave1_subsystem_evidence_v1:`
6. Legacy `total_bilirubin` in subsystem `missing_marker_ids`

Implementation: `assess_result_versioning()` / `build_result_versioning_metadata()`.

## UI behaviour (launch)

**Selected:** **B** — display stale warning banner (`StaleResultBanner`) when `result_versioning.result_status === 'stale'`.

**Planned:** **C** — “Regenerate with latest engine” creates **new** analysis/version; `regeneration_available: false` until job implemented.

**Rejected for launch:** **D** automatic regeneration on access (audit risk without lineage table).

## API behaviour

`GET /api/analysis/result` adds read-only `result_versioning` object (does not modify stored snapshot).

New runs stamp `meta.completeness_policy_id` and `meta.result_versioning_policy_id` at save time.

## Database / migration implications

Full versioning requires a follow-on migration tranche:

- `result_versions` table or `analysis_results` lineage columns
- `parent_analysis_id` / `supersedes_result_version_id`
- content-addressed payload hashes

**Out of scope for LAUNCH-CORE-3 implementation** — policy + detection only.

## Dev/test data handling

| Record | Handling |
|--------|----------|
| `746f2b0a…` | **Current** after LC-1 (post-fix run) |
| `18e14232…`, `bb695d3c…` | **Stale** — show banner; do not mutate |
| Future re-runs | New `analysis_id`; new snapshot with policy stamps |

## Production data handling

Same as dev: warn, never overwrite. Regeneration job gated on lineage schema.

## Recommended implementation sequence

1. LAUNCH-CORE-3 — policy + stale detection + UI banner (**this sprint**)
2. Lineage schema + `regeneration_available: true`
3. Regeneration API (`POST …/regenerate`) creating new analysis linked to parent
4. Optional: hide stale dev analyses from history for non-admin users

## Launch decision

**Proceed** with Wave 1 launch using stale warnings. Stale persisted records are a **known hygiene** issue, not a current-engine regression.
