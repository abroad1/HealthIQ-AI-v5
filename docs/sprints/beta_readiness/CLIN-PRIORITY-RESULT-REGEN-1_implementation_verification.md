# CLIN-PRIORITY-RESULT-REGEN-1 — Implementation & Verification Report

**Work ID:** CLIN-PRIORITY-RESULT-REGEN-1  
**Branch:** `feature/clin-priority-result-regen-1`  
**Change type:** BEHAVIOUR  
**Risk:** HIGH  
**Date:** 2026-08-05

## Objective delivered

Governed result-regeneration architecture with:

- single user-entered clinical chronology field `result_date`
- analysis-policy version as the broad personalised-output stale trigger
- regeneration lineage / supersession without mutating historic records
- canonical backend trend selection
- frontend migration off client-side trend authority

## Stage 1A / 1B

Confirmed against hardening citations:

| Authority | Path | Status |
|---|---|---|
| Versioning | `backend/core/dto/result_versioning_policy_v1.py` | Single authority extended |
| Compatibility | `backend/core/dto/persisted_replay_contract_v1.py` | Unchanged rules |
| Regeneration | `analysis_regeneration_v1.py` + `analysis_regeneration.py` + route | Extended lineage |
| Retention | LAUNCH-CORE-3 policy | Historic rows untouched |
| Persistence | `database.py` Analysis model | `result_date` + lineage columns |
| Trend (pre) | FE-only `useTrendData` / `trendComparison` | Replaced by backend path |
| Banner | `StaleResultBanner.tsx` | Unchanged; still server-status gated |
| Parallel authorities | None found | Confirmed |

Stage 1B baseline confirmed: pre-stamp results classified `current` without `clinical_concern_set`; no supersession exclusion in trends; no general analysis-policy version. All addressed.

## Outcomes A–G

| Outcome | Implementation |
|---|---|
| A `result_date` | Column + provenance on `analyses`; API optional `result_date`; meta stamp; backfill `legacy_created_at_fallback` |
| B analysis-policy version | `CURRENT_ANALYSIS_POLICY_VERSION = analysis_policy_v1_clin_priority_core`; stamped via `stamp_current_policy_meta` |
| C current stamping | `/start` and regen stamp policy + result_date |
| D historic classification | Missing/mismatched policy → `stale` (not `incompatible`); covers missing `clinical_concern_set` estate |
| E regeneration | New row; copies `result_date`; sets `supersedes_analysis_id` + `lineage_root_analysis_id`; source immutable |
| F backend trend | `GET /api/analysis/trend-eligible` + `trend_selection_v1.select_trend_eligible` |
| G frontend | `useTrendData` uses trend-eligible endpoint; banner unchanged |

## Before / after (pre-CLIN-PRIORITY result)

**Before:** Persisted payload without `analysis_policy_version` / without `clinical_concern_set` → `result_status=current`; no refresh surface from policy; trends include all completed by `created_at`.

**After:** Same payload → `result_status=stale` with `analysis_policy_version_missing`; `regeneration_available=true` when raw biomarkers present; after refresh, tip only appears in trend-eligible set at original `result_date`.

## Regression evidence

```
pytest tests/unit/test_clin_priority_result_regen_1.py tests/unit/test_launch_core3_result_versioning.py -q
→ 15 passed
```

Canonical coverage added/extended for required scenarios 1–13 (policy current/stale, regen availability, trend tip-once, same-date distinct lineages, incompatible unchanged).

Note: `test_internal_uat_result_versioning_dto_contract.py` two cases fail on pre-existing `missing_wave1_domain_cards` render blocker unrelated to analysis-policy / result_date changes (builders/compatibility path not modified for domain-card assembly).

## Clinical / signal confirmation

No changes to:

- signal activation / thresholds
- concern construction / prioritisation / tiering
- longitudinal medical rules
- WHY / root-cause authority

Touched surfaces are versioning classifier, persistence, regeneration lineage, trend selection, and FE trend data loading.

## Changed-file classification

| Class | Files |
|---|---|
| Policy / DTO | `analysis_policy_version_v1.py`, `trend_selection_v1.py`, `result_versioning_policy_v1.py` |
| Schema / migration | `database.py`, `clin_priority_result_regen_1.py` |
| Persistence / routes | `persistence_service.py`, `analysis_regeneration.py`, `routes/analysis.py` |
| Frontend | `types/analysis.ts`, `services/analysis.ts`, `hooks/useTrendData.ts`, `lib/trendComparison.ts` |
| Tests | `test_clin_priority_result_regen_1.py`, `test_launch_core3_result_versioning.py` |
| Evidence | this report; audit paper (preflight) |

## Migration

Idempotent Alembic revision `clin_priority_result_regen_1`:

- adds nullable columns
- backfills `result_date` from `created_at` with provenance `legacy_created_at_fallback`
- sets `lineage_root_analysis_id = id` for existing rows
- never deletes or rewrites analysis payloads
