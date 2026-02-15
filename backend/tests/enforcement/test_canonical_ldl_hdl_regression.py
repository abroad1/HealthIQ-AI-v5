"""
Regression test: LDL/HDL canonical IDs aligned end-to-end.

Ensures lipid panel with LDL/HDL produces canonical keys ldl_cholesterol, hdl_cholesterol
so clustering and insights can form.
"""

import pytest
from core.canonical.normalize import BiomarkerNormalizer
from core.pipeline.orchestrator import AnalysisOrchestrator


class TestCanonicalLDLHDLRegression:
    """Regression: LDL/HDL resolve to ldl_cholesterol, hdl_cholesterol."""

    def test_ldl_aliases_resolve_to_ldl_cholesterol(self):
        """LDL, ldl, LDL Cholesterol all resolve to ldl_cholesterol."""
        normalizer = BiomarkerNormalizer()
        for alias in ["LDL", "ldl", "LDL Cholesterol", "ldl_chol", "bad_cholesterol"]:
            panel, unmapped = normalizer.normalize_biomarkers({alias: 100.0})
            assert "ldl_cholesterol" in panel.biomarkers, f"{alias} should map to ldl_cholesterol"
            assert panel.biomarkers["ldl_cholesterol"].value == 100.0

    def test_hdl_aliases_resolve_to_hdl_cholesterol(self):
        """HDL, hdl, HDL Cholesterol all resolve to hdl_cholesterol."""
        normalizer = BiomarkerNormalizer()
        for alias in ["HDL", "hdl", "HDL Cholesterol", "hdl_chol", "good_cholesterol"]:
            panel, unmapped = normalizer.normalize_biomarkers({alias: 55.0})
            assert "hdl_cholesterol" in panel.biomarkers, f"{alias} should map to hdl_cholesterol"
            assert panel.biomarkers["hdl_cholesterol"].value == 55.0

    def test_lipid_panel_produces_canonical_keys_only(self):
        """Lipid panel with LDL/HDL produces no duplicate entries."""
        normalizer = BiomarkerNormalizer()
        raw = {
            "LDL": 100.0,
            "HDL": 50.0,
            "total_cholesterol": 180.0,
            "triglycerides": 120.0,
        }
        panel, unmapped = normalizer.normalize_biomarkers(raw)
        assert "ldl_cholesterol" in panel.biomarkers
        assert "hdl_cholesterol" in panel.biomarkers
        assert "ldl" not in panel.biomarkers
        assert "hdl" not in panel.biomarkers
        assert len([k for k in panel.biomarkers if "ldl" in k or "hdl" in k]) == 2
