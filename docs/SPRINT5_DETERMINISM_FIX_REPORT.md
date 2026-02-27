# Sprint 5 Determinism Hardening — Fix Report

**Authority:** docs/README_V5.2_BASELINE.md, Master_PRD_v5.2.md, Delivery_Sprint_Plan_v5.2.md Sprint 5 DoD

---

## Summary

Implemented two Sprint 5 blockers:

**A) Unit normalisation invariant** — Orchestrator.run() rejects input that has not been through apply_unit_normalisation.

**B) derived_markers first-class** — Persisted to dedicated column on AnalysisResult; fallback to processing_metadata for legacy rows.

---

## Files Changed

### Part A — Unit normalisation invariant

| File | Change |
|------|--------|
| `backend/core/units/registry.py` | Added `UNIT_REGISTRY_VERSION = "1.0"` |
| `backend/core/units/__init__.py` | Exported `UNIT_REGISTRY_VERSION` |
| `backend/core/pipeline/orchestrator.py` | Added `UNIT_NORMALISATION_META_KEY`; guard at start of `run()` that raises if `__unit_normalisation_meta__` absent or `unit_normalised != True` |
| `backend/app/routes/analysis.py` | After `apply_unit_normalisation`, set `normalized[UNIT_NORMALISATION_META_KEY]` with `unit_normalised: True` and `unit_registry_version` before `orchestrator.run()` |
| `backend/tests/unit/test_orchestrator_unit_normalisation.py` | **New** — rejects un-normalised mg/dL lipids; accepts normalised payload and asserts derived markers correct |
| `backend/tests/unit/test_llm_integration.py` | Apply normalize → unit norm → add meta before `orchestrator.run()` |
| `backend/tests/integration/test_orchestrator_unmapped_quarantine.py` | Added `_prepare_unit_normalised()`; use it before both `orchestrator.run()` calls |
| `backend/tests/integration/test_venous_aliases_orchestrator_integration.py` | Added `_prepare_unit_normalised()`; use it before all 4 `orchestrator.run()` calls |

### Part B — derived_markers first-class

| File | Change |
|------|--------|
| `backend/core/models/database.py` | Added `derived_markers = Column(JSON, nullable=True)` to AnalysisResult |
| `backend/migrations/versions/add_derived_markers_column.py` | **New** — Migration adding `derived_markers` JSON column to `analysis_results` |
| `backend/services/storage/persistence_service.py` | `create_analysis_result`: persist `derived_markers` to column (removed from processing_metadata). `get_analysis_result`: prefer `result.derived_markers`, fallback to `processing_metadata["derived_markers"]` |
| `backend/tests/integration/test_persistence_flow.py` | Assert `result.derived_markers` is populated on DB model; verify round-trip via first-class column |

---

## Migration

| Name | Path |
|------|------|
| `add_derived_markers_column` | `backend/migrations/versions/add_derived_markers_column.py` |

**To run:**  
`cd backend && alembic upgrade head`  
(or `python -m alembic upgrade head` if using system Python)

Ensure `DATABASE_URL` points to the target database. For persistence tests, use the test DB URL (e.g. `DATABASE_URL_TEST`).

---

## Tests Added / Updated

| Test | Change |
|------|--------|
| `test_orchestrator_run_rejects_unnormalised_mg_dl_lipids` | **New** — Unit test: orchestrator raises ValueError for un-normalised input |
| `test_orchestrator_run_accepts_normalised_payload_derived_markers_correct` | **New** — Unit test: normalised input yields correct non_hdl_cholesterol |
| `test_automatic_analysis_result_creation` | Assert `result.derived_markers` column populated |
| `test_llm_integration` (unit) | Prepares unit-normalised payload before run |
| `test_orchestrator_unmapped_quarantine` (2 tests) | Use `_prepare_unit_normalised()` |
| `test_venous_aliases_orchestrator_integration` (4 tests) | Use `_prepare_unit_normalised()` |

---

## Regression Gate Results

### Unit tests
```
pytest tests/unit -q --tb=short
```
**Result:** 319 passed (includes 2 new unit tests for orchestrator unit normalisation).

### Integration tests
```
pytest tests/integration -k "analysis_result or insight_pipeline or scoring_orchestrator or upload_api or persistence_flow or ratio_registry" -q --tb=short
```

**Result without migration:** 31 passed, 3 failed (persistence tests fail with `column analysis_results.derived_markers does not exist`).

**Result with migration applied:** Run `alembic upgrade head` against the test database, then re-run integration tests. All tests are expected to pass.

**Note:** Migration must be run before persistence integration tests. If Alembic is not installed or the database is unavailable, those 3 tests will fail until the migration is applied.

---

## Invariant Behaviour

1. **Unit normalisation:** Callers must pass biomarkers through `apply_unit_normalisation` and set `__unit_normalisation_meta__` before `orchestrator.run()`. Otherwise `run()` raises `ValueError`.

2. **derived_markers:** Written to `analysis_results.derived_markers`. Read from that column when present; otherwise from `processing_metadata["derived_markers"]` for legacy rows.
