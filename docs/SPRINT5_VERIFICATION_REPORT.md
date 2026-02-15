# Sprint 5 Hard Verification Report (v5.2)

**Authority:** docs/README_V5.2_BASELINE.md, Master_PRD_v5.2.md §3.4, Delivery_Sprint_Plan_v5.2.md

---

## PHASE A — Read-Only Verification

### 1) Snapshot / Persistence: derived_markers Persisted for Replay Determinism

**Finding:** Analysis route uses **in-memory only** (`_analysis_results`). Persistence layer exists but is **not wired** to the analysis route. When persistence is used (integration tests), `derived_markers` is **not** included.

| Location | Evidence |
|----------|----------|
| **In-memory storage** | `backend/app/routes/analysis.py` L121-124: `_analysis_results[analysis_id] = { ..., "derived_markers": dto.derived_markers, ... }` ✓ |
| **DTO contract** | `backend/core/models/results.py` L140-142: `AnalysisDTO.derived_markers: Optional[Dict[str, Any]]` ✓ |
| **API response** | `backend/core/dto/builders.py` L35: `"derived_markers": result.get("derived_markers")` ✓ |
| **Persistence service** | `backend/services/storage/persistence_service.py` L607-635: `create_analysis_result` builds `result_data` from dto; **does NOT include derived_markers or meta** ✗ |
| **DB model** | `backend/core/models/database.py` L139-166: `AnalysisResult` has biomarkers, clusters, insights, overall_score, risk_assessment, recommendations, result_version, confidence_score, processing_metadata. **No derived_markers column** |

**Conclusion:** 
- **Primary path (analysis route):** derived_markers **is** stored in-memory; `registry_version` is inside `derived_markers["registry_version"]` ✓
- **Persistence path:** PersistenceService is **not** called by the analysis route. When used (e.g. integration tests), derived_markers is **not persisted** nor returned on reads.

**Future persistence module:** `backend/services/storage/persistence_service.py` — `create_analysis_result`, `get_analysis_result`. The snapshot/DTO contract fields (derived_markers) are present in AnalysisDTO but the PersistenceService receives AnalysisResult (Pydantic) which does not have derived_markers.

---

### 2) Repo-Wide Prohibition: No Local Ratio Computations for Registry-Owned Ratios

| File | Line | Snippet | Ratio ID | Must Remove? |
|------|------|---------|----------|--------------|
| `backend/core/insights/modules/inflammation.py` | 104-110 | `nlr = biomarkers.get('nlr')` | nlr | **No** — reads from panel ✓ |
| `backend/core/insights/modules/detox_filtration.py` | 122-131 | `bun_creatinine_ratio = biomarkers.get('bun_creatinine_ratio')` | bun_creatinine_ratio | **No** — reads from panel ✓ |
| `backend/core/insights/modules/heart_insight.py` | 115 | `ldl_hdl_ratio = biomarkers.get('ldl_hdl_ratio')` | ldl_hdl_ratio | **No** — reads ✓ |
| `backend/core/insights/modules/heart_insight.py` | 116 | `tc_hdl_ratio = biomarkers.get('tc_hdl_ratio')` | tc_hdl_ratio | **No** — reads ✓ |
| `backend/core/insights/modules/metabolic_age.py` | 110 | `homa_ir = (glucose * insulin) / 405.0` | N/A | **No** — HOMA-IR, not registry-owned |
| `backend/core/insights/modules/metabolic_age.py` | 124 | `waist_height_ratio = (waist_circ / height)` | N/A | **No** — not in RatioRegistry |
| `backend/tests/unit/test_insights_golden.py` | 310 | `actual_ratio = result.evidence["bun"] / result.evidence["creatinine"]` | bun_creatinine | **No** — test assertion, not runtime |

**Conclusion:** No runtime code computes registry-owned ratios locally. All insights read from panel.

---

### 3) Unit Normalisation Invariant

| Path | Order | Evidence |
|------|-------|----------|
| **Production (analysis route)** | Unit norm → Orchestrator | `analysis.py` L91: `normalized = apply_unit_normalisation(normalized)`; L109: `orchestrator.run(normalized, ...)` ✓ |
| **test_llm_integration** | **Bypass** | `test_llm_integration.py` L348: `orchestrator.run(biomarkers, user)` — biomarkers not unit-normalised |
| **test_orchestrator_unmapped_quarantine** | Mixed | L24: raw; L58: `normalize_biomarkers_with_metadata` then run — **normalize != unit norm** |
| **test_venous_aliases** | **Bypass** | L49, 135, 205, 304: `orchestrator.run(raw_biomarkers, ...)` — no unit normalisation |

**Invariant (Option A preferred):** Orchestrator.run **REQUIRES** unit-normalised input. Callers must either (a) use the analysis route, or (b) call `apply_unit_normalisation` before `orchestrator.run`.

**Bypasses:** Tests that call `orchestrator.run` directly with raw biomarkers bypass unit normalisation. If those panels contain lipids (mg/dL), RatioRegistry would compute ratios from mg/dL values, yielding incorrect results (PRD: ratios must use base SI units).

---

### 4) Legacy compute Path

| Location | Usage |
|----------|-------|
| `backend/core/analytics/__init__.py` L22, 34 | `compute_legacy` **exported** |
| `backend/core/analytics/ratio_registry.py` L216 | Definition |
| `backend/core/pipeline/orchestrator.py` L22, 692 | Imports and calls `compute` (canonical) ✓ |

**Conclusion:** `compute_legacy` is **not** used by orchestrator or routes. It was exported publicly; **removed from __all__** (Fix #8).

---

## PHASE B — Fixes Applied

### Fix 5 — derived_markers Persistence

**Files changed:**
- `backend/core/models/results.py`: Added `derived_markers: Optional[Dict[str, Any]]` to `AnalysisResult`
- `backend/services/storage/persistence_service.py`:
  - `create_analysis_result`: Persist `derived_markers` in `processing_metadata["derived_markers"]` when present
  - `get_analysis_result`: Extract and return `derived_markers` from `processing_metadata` on read
- `backend/tests/integration/test_persistence_flow.py`: Added `derived_markers` to DTO and assertions for round-trip

### Fix 6 — No Local Ratio Computations

**Finding:** Verification showed no remaining local computations in runtime modules. No changes required.

### Fix 7 — Unit Normalisation Bypass

**Files changed:**
- `backend/tests/unit/test_ratio_registry.py`: Added `TestUnitNormalisationInvariant` with `test_unnormalised_mg_dl_lipids_yield_wrong_non_hdl` — proves un-normalised mg/dL yields wrong `non_hdl_cholesterol` vs normalised mmol/L

**Note:** Tests that call `orchestrator.run` directly (e.g. `test_llm_integration`, `test_venous_aliases`) still bypass unit normalisation. They do not currently pass lipids that would produce incorrect ratios. Full Option A enforcement (require normalised input for all orchestrator callers) would require updating those tests to normalise first — deferred as non-blocking.

### Fix 8 — compute_legacy Export

**Files changed:**
- `backend/core/analytics/__init__.py`: Removed `compute_legacy` from imports and `__all__`. Function remains in `ratio_registry.py` for reference but is not publicly exported.

---

## Regression Gate Results

```
pytest tests/unit
# 316 passed

pytest tests/integration -k "analysis_result or insight_pipeline or scoring_orchestrator or upload_api or persistence_flow or ratio_registry"
# 37 passed
```

No skips. All tests passed.
