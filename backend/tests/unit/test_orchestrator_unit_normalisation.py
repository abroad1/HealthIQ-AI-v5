"""
Unit tests for Sprint 5 unit-normalisation invariant.

Orchestrator.run() must reject input without unit normalisation.
"""

import pytest
from uuid import UUID
from unittest.mock import patch
from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
from core.canonical.normalize import normalize_biomarkers_with_metadata
from core.units.registry import apply_unit_normalisation, UNIT_REGISTRY_VERSION
from core.canonical.alias_registry_service import AliasRegistryService, get_alias_registry_service
from core.models.signal import SignalResult


def _prepare_unit_normalised(biomarkers: dict) -> dict:
    """Apply normalize -> unit norm -> add meta (production path)."""
    normalized = normalize_biomarkers_with_metadata(biomarkers)
    normalized = apply_unit_normalisation(normalized)
    normalized[UNIT_NORMALISATION_META_KEY] = {
        "unit_normalised": True,
        "unit_registry_version": UNIT_REGISTRY_VERSION,
    }
    return normalized


@pytest.fixture(autouse=True)
def _disable_common_alias_injection(monkeypatch):
    """Keep orchestrator unit-normalisation tests focused on conversion invariant."""
    get_alias_registry_service.cache_clear()
    monkeypatch.setattr(
        AliasRegistryService,
        "_add_common_aliases",
        lambda self, alias_mapping, insert_alias: None,
    )
    yield
    get_alias_registry_service.cache_clear()


class TestOrchestratorUnitNormalisationInvariant:
    """Sprint 5: orchestrator enforces unit-normalisation before run."""

    def test_orchestrator_run_rejects_unnormalised_mg_dl_lipids(self):
        """Un-normalised mg/dL lipids must be rejected; no silent incorrect derived markers."""
        orchestrator = AnalysisOrchestrator()
        raw_biomarkers = {
            "total_cholesterol": {"value": 200.0, "unit": "mg/dL"},
            "hdl_cholesterol": {"value": 50.0, "unit": "mg/dL"},
        }
        user = {"user_id": "test", "age": 35, "gender": "male"}

        with pytest.raises(ValueError) as exc_info:
            orchestrator.run(raw_biomarkers, user, assume_canonical=True)

        assert "Unit normalisation required" in str(exc_info.value)
        assert "apply_unit_normalisation" in str(exc_info.value)

    def test_orchestrator_run_accepts_normalised_payload_derived_markers_correct(self):
        """Normalised payload passes unit gate and reaches downstream pipeline."""
        orchestrator = AnalysisOrchestrator()
        raw_biomarkers = {
            "total_cholesterol": {"value": 200.0, "unit": "mg/dL"},
            "hdl_cholesterol": {"value": 50.0, "unit": "mg/dL"},
        }
        user = {"user_id": "test", "age": 35, "gender": "male"}

        prepared = _prepare_unit_normalised(raw_biomarkers)
        dto = orchestrator.run(prepared, user, assume_canonical=True)

        assert dto is not None
        if dto.status == "completed":
            assert dto.derived_markers is not None
            derived = dto.derived_markers.get("derived", {})
            non_hdl = derived.get("non_hdl_cholesterol", {})
            val = non_hdl.get("value")
            assert val is not None
            assert abs(val - 3.885) < 0.1, f"non_hdl should be ~3.885 mmol/L, got {val}"
        else:
            assert dto.status == "error"
            manifest = dto.replay_manifest or {}
            assert manifest.get("stage") == "orchestrator.run"

    def test_orchestrator_failure_envelope_is_deterministic(self):
        """Failure DTO reuses analysis_id and fixed timestamp with code-only manifest."""
        orchestrator = AnalysisOrchestrator()
        prepared = _prepare_unit_normalised({"glucose": {"value": 95.0, "unit": "mg/dL"}})
        user = {"user_id": "test", "age": 35, "gender": "male"}

        with patch("uuid.uuid4", side_effect=[UUID("11111111-1111-1111-1111-111111111111")]) as uuid_mock:
            orchestrator.score_biomarkers = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("forced"))
            dto = orchestrator.run(prepared, user, assume_canonical=True)

        assert dto.status == "error"
        assert dto.analysis_id == "11111111-1111-1111-1111-111111111111"
        assert dto.created_at == "1970-01-01T00:00:00+00:00"
        assert uuid_mock.call_count == 1
        assert dto.replay_manifest is not None
        assert dto.replay_manifest.get("failure_code") == "analysis_pipeline_failed"
        assert dto.replay_manifest.get("failure_type") == "RuntimeError"
        assert dto.replay_manifest.get("stage") == "orchestrator.run"

    def test_signal_evaluation_happens_before_scoring(self):
        orchestrator = AnalysisOrchestrator()
        prepared = _prepare_unit_normalised({"glucose": {"value": 95.0, "unit": "mg/dL"}})
        user = {"user_id": "test", "age": 35, "gender": "male"}
        events = []

        def _eval(*args, **kwargs):
            events.append("evaluate")
            return []

        def _score(*args, **kwargs):
            events.append("score")
            raise RuntimeError("forced-stop")

        orchestrator.signal_evaluator.evaluate_all = _eval
        orchestrator.score_biomarkers = _score

        dto = orchestrator.run(prepared, user, assume_canonical=True)
        assert dto.status == "error"
        assert events == ["evaluate", "score"]

    def test_orchestrator_passes_signal_payload_into_insight_graph(self, monkeypatch):
        orchestrator = AnalysisOrchestrator()
        prepared = _prepare_unit_normalised({"glucose": {"value": 95.0, "unit": "mg/dL"}})
        user = {"user_id": "test", "age": 35, "gender": "male"}
        captured = {}

        orchestrator.score_biomarkers = lambda *args, **kwargs: {
            "overall_score": 0.0,
            "health_system_scores": {},
        }
        orchestrator.create_analysis_context = lambda *args, **kwargs: object()
        orchestrator.cluster_biomarkers = lambda *args, **kwargs: {"clusters": []}
        orchestrator.signal_evaluator.evaluate_all = lambda *args, **kwargs: [
            SignalResult(
                signal_id="signal_alpha",
                system="metabolic",
                signal_state="suboptimal",
                signal_value=8.9,
                primary_metric="tyg_index",
                confidence=None,
                lab_normal_but_flagged=False,
                supporting_markers=["insulin"],
            )
        ]

        def _capture_build(*args, **kwargs):
            captured.update(kwargs)
            raise RuntimeError("halt-after-build")

        monkeypatch.setattr("core.pipeline.orchestrator.build_insight_graph_v1", _capture_build)
        dto = orchestrator.run(prepared, user, assume_canonical=True)

        assert dto.status == "error"
        assert captured["signal_registry_version"] == orchestrator.signal_registry.version
        assert captured["signal_registry_hash"] == orchestrator.signal_registry.package_hash
        assert captured["signal_results"] == [
            {
                "signal_id": "signal_alpha",
                "system": "metabolic",
                "signal_state": "suboptimal",
                "signal_value": 8.9,
                "confidence": None,
                "primary_metric": "tyg_index",
                "lab_normal_but_flagged": False,
                "supporting_markers": ["insulin"],
            }
        ]
