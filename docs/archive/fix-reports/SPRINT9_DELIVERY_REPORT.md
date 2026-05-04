# Sprint 9 Delivery Report — ReplayManifest_v1 Determinism Lock

**Version:** v5.2 Phase 2  
**Sprint:** 9  
**Authority:** Master_PRD_v5.2.md; Delivery_Sprint_Plan_v5.2.md  

---

## Phase A — Evidence: Version Stamps & Persistence

### Version stamps currently produced

| Item | Location | Persisted? |
|------|----------|------------|
| Unit registry version | `core/units/registry.py` L23 `UNIT_REGISTRY_VERSION` | In unit_meta; not first-class in result |
| Ratio registry version | `core/analytics/ratio_registry.py` L18 `RatioRegistry.version` | In derived_markers.registry_version |
| Cluster schema version/hash | `core/analytics/cluster_schema.py` L170 `get_cluster_schema_version_stamp()` | In meta |
| InsightGraph version | `core/contracts/insight_graph_v1.py` L52 `graph_version` | In meta.insight_graph |
| ConfidenceModel version | `core/contracts/confidence_model_v1.py` L26 `model_version` | In insight_graph.confidence |
| Result version | `core/models/database.py` L163 `result_version` | Yes (column) |

### Persistence

| Location | Fields |
|----------|--------|
| `core/models/database.py` AnalysisResult | biomarkers, clusters, insights, overall_score, derived_markers, result_version, confidence_score, processing_metadata |
| Meta (processing_metadata) | insight_graph, derived_ratios, cluster_schema_version, cluster_schema_hash |
| API return | build_analysis_result_dto → meta, derived_markers |

---

## Phase B — Deliverables

### Files created

| File | Purpose |
|------|---------|
| `backend/core/contracts/replay_manifest_v1.py` | ReplayManifestV1 contract (version stamps, schema_hashes) |
| `backend/core/analytics/replay_manifest_builder.py` | build_replay_manifest_v1, _canonical_json_hash |

### Files modified

| File | Change |
|------|--------|
| `backend/core/models/results.py` | replay_manifest on AnalysisDTO and AnalysisResult |
| `backend/core/pipeline/orchestrator.py` | Build ReplayManifest after InsightGraph; add to AnalysisDTO |
| `backend/app/routes/analysis.py` | Store replay_manifest in _analysis_results |
| `backend/core/dto/builders.py` | Include replay_manifest in build_analysis_result_dto |
| `backend/core/models/database.py` | replay_manifest JSON column on AnalysisResult |
| `backend/services/storage/persistence_service.py` | Write/read replay_manifest |
| `backend/core/contracts/__init__.py` | Export ReplayManifestV1 |

---

## Phase C — Wiring Evidence

### Manifest builder call in orchestrator

- **File:** `backend/core/pipeline/orchestrator.py`
- **Lines:** After Step 4.6 (InsightGraph build), Step 4.7 added
- **Flow:** build_replay_manifest_v1(unit_registry_version, ratio_registry_version, cluster_schema_version, cluster_schema_hash, insight_graph, confidence_model, …) → replay_manifest.model_dump() in AnalysisDTO

### Persistence

- **Column:** `analysis_results.replay_manifest` (JSON, nullable)
- **Write:** `persistence_service.create_analysis_result` → result_data["replay_manifest"]; `save_results` → result_data["replay_manifest"]
- **Read:** `get_analysis_result` → `"replay_manifest": getattr(result, "replay_manifest", None)`
- **Backward compat:** Old rows return None for replay_manifest

### Migration

- **File:** `backend/migrations/versions/add_replay_manifest_column.py`
- **Revision:** add_replay_manifest_column
- **Down revision:** add_derived_markers_column

---

## Phase D — Tests

### Unit tests

| Test | File |
|------|------|
| test_build_twice_yields_identical_json | test_replay_manifest.py |
| test_hashes_are_stable | test_replay_manifest.py |
| test_no_forbidden_keys_in_manifest | test_replay_manifest.py |
| test_version_stamp_present | test_replay_manifest.py |

### Integration

- `test_persistence_flow`: replay_manifest in DTO, persisted, returned with required version fields and non-empty hashes.

---

## Regression Gate Results

| Suite | Pass | Fail | Skip |
|-------|------|------|-----|
| `pytest backend/tests/unit` | 578 | 0 | 0 |
| `pytest backend/tests/integration -k "..."` | 37 | 0 | 0 |

---

## Constraints Met

- No insight redesign  
- No new medical logic  
- No fuzzy logic  
- No fallback parser  
- Layer B computes; Layer C translates  
- Deterministic: no timestamps, no random, no env-dependent fields  
