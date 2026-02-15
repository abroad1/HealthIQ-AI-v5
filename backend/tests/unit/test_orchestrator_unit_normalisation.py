"""
Unit tests for Sprint 5 unit-normalisation invariant.

Orchestrator.run() must reject input without unit normalisation.
"""

import pytest
from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
from core.canonical.normalize import normalize_biomarkers_with_metadata
from core.units.registry import apply_unit_normalisation, UNIT_REGISTRY_VERSION


def _prepare_unit_normalised(biomarkers: dict) -> dict:
    """Apply normalize -> unit norm -> add meta (production path)."""
    normalized = normalize_biomarkers_with_metadata(biomarkers)
    normalized = apply_unit_normalisation(normalized)
    normalized[UNIT_NORMALISATION_META_KEY] = {
        "unit_normalised": True,
        "unit_registry_version": UNIT_REGISTRY_VERSION,
    }
    return normalized


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
        """Normalised payload produces correct derived markers (non_hdl in mmol/L)."""
        orchestrator = AnalysisOrchestrator()
        raw_biomarkers = {
            "total_cholesterol": {"value": 200.0, "unit": "mg/dL"},
            "hdl_cholesterol": {"value": 50.0, "unit": "mg/dL"},
        }
        user = {"user_id": "test", "age": 35, "gender": "male"}

        prepared = _prepare_unit_normalised(raw_biomarkers)
        dto = orchestrator.run(prepared, user, assume_canonical=True)

        assert dto is not None
        assert dto.derived_markers is not None
        derived = dto.derived_markers.get("derived", {})
        non_hdl = derived.get("non_hdl_cholesterol", {})
        val = non_hdl.get("value")
        assert val is not None
        assert abs(val - 3.885) < 0.1, f"non_hdl should be ~3.885 mmol/L, got {val}"
