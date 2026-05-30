# LAUNCH-CORE-3 — Result Versioning, Replay and Regeneration Audit

**Generated:** 2026-05-30  
**Work package:** `LAUNCH-CORE-3_result_versioning_replay_and_regeneration_policy`

## Final launch recommendation

**Proceed** with immutable-snapshot policy enforced in documentation and stale detection. Display **stale warning (behaviour B)**; plan **versioned regeneration (behaviour C)** without implementing regeneration job in this sprint.

## Current persistence paths

| Store | Location | Content |
|-------|----------|---------|
| Analysis session | `analyses` table | `raw_biomarkers`, `questionnaire_data`, `analysis_version`, `pipeline_version`, status |
| Client result snapshot | `analysis_results.processing_metadata['client_result_shape_v1']` | Full frontend DTO shape (immutable blob) |
| Replay | `analysis_results.replay_manifest` | ReplayManifestV1 JSON |
| In-process cache | `_analysis_results` dict | Same shape when DB unavailable |

Authority: `PersistenceService.save_live_analysis_after_run`, `AnalysisRepository`, `AnalysisResultRepository`.

## API retrieval paths

| Endpoint | Behaviour |
|----------|-----------|
| `GET /api/analysis/result` | Load snapshot → `build_analysis_result_dto` → attach `result_versioning` metadata |
| `POST /api/analysis/start` | New run; stamp policy meta; persist new snapshot |

## Are old results immutable today?

**Yes in practice** — no code path updates `client_result_shape_v1` in place after save. LAUNCH-CORE-3 makes this explicit and adds stale classification.

## Is raw source input available for regeneration?

**Yes** — `analyses.raw_biomarkers` and `questionnaire_data` are persisted on live runs. A future regeneration job can re-invoke the orchestrator without mutating the old snapshot.

## Is deterministic regeneration possible today?

| Mode | Feasible? |
|------|-----------|
| Re-render stored DTO only | Yes (current GET path) |
| Full pipeline replay from raw input | Yes (data present) |
| Same-analysis in-place refresh | **No** — forbidden by policy |

## Version/hash fields today

| Field | Present |
|-------|---------|
| `result_version` | Yes (`1.0.0` default) |
| `replay_manifest.manifest_version` | Yes on new runs |
| Registry hashes in manifest | Yes (orchestrator-stamped) |
| `meta.completeness_policy_id` | Yes **after LAUNCH-CORE-3** on new runs only |
| Lineage / supersession IDs | **No** |

## Stale analysis examples (LAUNCH-CORE-2)

| Analysis ID | Classification | Reasons |
|-------------|----------------|---------|
| `18e14232-9f93-45e6-820c-004ab5a16235` | **stale** | Pre-LC-1 completeness (1/3 vs 2/4); policy meta missing |
| `bb695d3c-453e-4e49-abff-ae80587b4248` | **stale** | Legacy subsystem traces; `total_bilirubin` false-missing |
| `746f2b0a-b470-4d87-8ed8-e2c3d1e68c02` | **current** (post-LC-1 run) | Aligns with LC-1 presentation when policy stamped on future re-save N/A |

## Implementation performed

| Item | Path |
|------|------|
| Stale detection + metadata | `backend/core/dto/result_versioning_policy_v1.py` |
| API attachment | `backend/app/routes/analysis.py` |
| Policy stamp on new runs | `stamp_current_policy_meta` in start flow |
| Frontend banner | `frontend/app/components/results/StaleResultBanner.tsx` |
| Policy doc | `docs/architecture/LAUNCH-CORE-3_result_versioning_replay_and_regeneration_policy.md` |

**Not implemented:** regeneration job, DB lineage migration, destructive refresh.

## Tests run

```text
python -m pytest backend/tests/unit/test_launch_core3_result_versioning.py -q
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
cd frontend && npm test -- tests/components/StaleResultBanner.test.tsx
```

## Remaining risks

| Risk | Mitigation |
|------|------------|
| Heuristic false positive/negative on stale | Extend reasons; add analysis_id allowlist only for audit |
| Users confused by stale banner | Copy + future regenerate CTA |
| History lists stale analyses | Future filter or regen workflow |

## ARCH-RT-6

Guardrails **unchanged** — validator PASS; no clinical logic modified.
