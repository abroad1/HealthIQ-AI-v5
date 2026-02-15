# Sprint 8 Delivery Report — Confidence & Missing Data Model Hardening

**Version:** v5.2 Phase 2  
**Sprint:** 8  
**Authority:** Master_PRD_v5.2.md §4.3, §4.4; Delivery_Sprint_Plan_v5.2.md  

---

## Phase A — Evidence: Current Confidence Logic

### 1. Where confidence is computed

| Location | Logic | Deterministic? | Versioned? |
|----------|-------|----------------|------------|
| `backend/core/analytics/criticality.py` L64–159 | `evaluate_criticality`: system_confidence, overall_confidence, missing_markers from ssot/criticality.yaml | Yes | Yes (criticality_version) |
| `backend/core/clustering/cluster_engine_v2.py` L193–205 | cluster confidence = present_count / total_members | Yes | Schema-driven |
| `backend/core/clustering/rules.py` L136–158 | `_calculate_cluster_confidence`: variance-based | No (heuristic) | No |
| `backend/core/clustering/engine.py` L231–253 | `_calculate_cluster_confidence`: variance-based | No | No |
| `backend/core/insights/synthesis.py` L590–605 | `_calculate_overall_confidence`: avg of insight confidences | Yes | Post-LLM only |
| `backend/core/insights/modules/*.py` | Per-insight `_calculate_confidence` (biomarker count) | Heuristic | No |

### 2. Duplication / implicit logic

| File | Logic | Centralise? |
|------|-------|-------------|
| `criticality.py` | system_confidence, missing_markers | Keep; used by ConfidenceModel |
| `cluster_engine_v2.py` | cluster confidence (present/total) | Centralised in confidence_builder |
| `rules.py` / `engine.py` | Variance-based cluster confidence | Legacy; not used by InsightGraph path |
| `synthesis.py` | overall_confidence from insights | Different concern (post-LLM) |
| `insight modules` | Per-insight confidence | Out of scope (no redesign) |

---

## Phase B — Deliverables

### Files created

| File | Purpose |
|------|---------|
| `backend/core/contracts/confidence_model_v1.py` | ConfidenceModelV1 contract (system, cluster, biomarker confidence; missing lists; version refs) |
| `backend/core/analytics/confidence_builder.py` | Deterministic builder from cluster schema + available biomarkers |

### Files modified

| File | Change |
|------|--------|
| `backend/core/contracts/insight_graph_v1.py` | Added `confidence: Optional[ConfidenceModelV1]` |
| `backend/core/analytics/insight_graph_builder.py` | Build ConfidenceModel, inject into InsightGraph |
| `backend/core/insights/prompts.py` | Added `{confidence_context}` placeholder; format from InsightGraph confidence |
| `backend/core/contracts/__init__.py` | Export ConfidenceModelV1, CONFIDENCE_MODEL_V1_VERSION |

---

## Phase C — LLM Boundary

- InsightGraph includes `confidence` (ConfidenceModelV1).
- Prompt `format_template_from_insight_graph` uses only: cluster summary, status, confidence, missing_required.
- No raw biomarkers in prompt.
- Isolation test: `backend/tests/integration/test_confidence_model_isolation.py` (3 tests).

---

## Phase D — Tests

### Unit tests

| Test | File |
|------|------|
| test_confidence_builder_basic | test_confidence_builder.py |
| test_missing_required_marker_reduces_cluster_confidence | test_confidence_builder.py |
| test_all_required_markers_present_cluster_confidence_1 | test_confidence_builder.py |
| test_confidence_model_version_stamp | test_confidence_builder.py |
| test_deterministic_output_ordering | test_confidence_builder.py |

### Enforcement tests

| Test | File |
|------|------|
| test_build_confidence_model_only_in_confidence_builder | test_confidence_model_centralised.py |
| test_synthesis_does_not_compute_confidence_model | test_confidence_model_centralised.py |
| test_confidence_builder_is_sole_source | test_confidence_model_centralised.py |

---

## Regression Gate Results

| Suite | Pass | Fail | Skip |
|-------|------|------|-----|
| `pytest backend/tests/unit` | 574 | 0 | 0 |
| `pytest backend/tests/integration -k "analysis_result or insight_pipeline or scoring_orchestrator or upload_api or persistence_flow or ratio_registry"` | 37 | 0 | 0 |
| `pytest backend/tests/integration -k "llm_insight_graph_isolation or confidence_model_isolation"` | 5 | 0 | 0 |

---

## Constraints Met

- No insight redesign  
- No new medical scoring heuristics  
- No fuzzy logic  
- No LLM computation  
- Confidence deterministic and replay-safe  
- Minimal, auditable changes  
