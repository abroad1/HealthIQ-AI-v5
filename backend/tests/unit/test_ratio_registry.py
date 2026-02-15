"""
Unit tests for RatioRegistry (Sprint 4/5).

- RatioRegistry.compute returns structured output with correct values
- Lab-supplied ratios: compute treats them as source=lab (Sprint 4.1)
- Guard: insight modules do not contain direct division for RatioRegistry ratios
"""

import pytest
from core.analytics.ratio_registry import RatioRegistry, compute, DERIVED_IDS


def _get_val(out: dict, rid: str):
    """Extract value from structured compute output."""
    entry = out.get("derived", {}).get(rid)
    return entry.get("value") if isinstance(entry, dict) else None


class TestRatioRegistryCompute:
    """Tests for RatioRegistry.compute (structured output)."""

    def test_tc_hdl_ratio(self):
        panel = {"total_cholesterol": 200.0, "hdl_cholesterol": 50.0}
        out = compute(panel)
        assert _get_val(out, "tc_hdl_ratio") == pytest.approx(4.0, abs=0.001)
        assert out["derived"]["tc_hdl_ratio"]["source"] == "computed"

    def test_tg_hdl_ratio(self):
        panel = {"triglycerides": 100.0, "hdl_cholesterol": 50.0}
        out = compute(panel)
        assert _get_val(out, "tg_hdl_ratio") == pytest.approx(2.0, abs=0.001)

    def test_ldl_hdl_ratio(self):
        panel = {"ldl_cholesterol": 105.0, "hdl_cholesterol": 35.0}
        out = compute(panel)
        assert _get_val(out, "ldl_hdl_ratio") == pytest.approx(3.0, abs=0.001)

    def test_non_hdl_cholesterol(self):
        panel = {"total_cholesterol": 200.0, "hdl_cholesterol": 50.0}
        out = compute(panel)
        assert _get_val(out, "non_hdl_cholesterol") == pytest.approx(150.0, abs=0.01)

    def test_apoB_apoA1_when_both_present(self):
        panel = {"apob": 100.0, "apoa1": 125.0}
        out = compute(panel)
        assert _get_val(out, "apoB_apoA1_ratio") == pytest.approx(0.8, abs=0.001)

    def test_apoB_apoA1_missing_omitted(self):
        panel = {"apob": 100.0}
        out = compute(panel)
        assert "apoB_apoA1_ratio" not in out.get("derived", {})

    def test_missing_inputs_omitted(self):
        panel = {}
        out = compute(panel)
        assert "derived" in out
        assert "tc_hdl_ratio" not in out.get("derived", {})
        assert "tg_hdl_ratio" not in out.get("derived", {})
        assert "registry_version" in out

    def test_zero_hdl_returns_none_for_ratios(self):
        panel = {"total_cholesterol": 200.0, "hdl_cholesterol": 0}
        out = compute(panel)
        assert "tc_hdl_ratio" not in out.get("derived", {})
        assert _get_val(out, "non_hdl_cholesterol") == pytest.approx(200.0, abs=0.01)

    def test_version_is_string(self):
        assert isinstance(RatioRegistry.version, str)
        assert len(RatioRegistry.version) > 0

    def test_lab_supplied_ldl_hdl_ratio_wins(self):
        """When panel already includes ldl_hdl_ratio, compute returns source=lab, lab value."""
        panel = {
            "ldl_cholesterol": 105.0,
            "hdl_cholesterol": 35.0,
            "ldl_hdl_ratio": 4.5,
        }
        out = compute(panel)
        entry = out.get("derived", {}).get("ldl_hdl_ratio")
        assert entry is not None
        assert entry["source"] == "lab"
        assert entry["value"] == pytest.approx(4.5, abs=0.001)
        assert "tc_hdl_ratio" not in out.get("derived", {})  # no lipid inputs to compute tc

    def test_nlr_computed(self):
        """NLR = neutrophils / lymphocytes when both present."""
        panel = {"neutrophils": 8.0, "lymphocytes": 2.5}
        out = compute(panel)
        assert _get_val(out, "nlr") == pytest.approx(3.2, abs=0.001)
        assert out["derived"]["nlr"]["source"] == "computed"

    def test_bun_creatinine_ratio_computed(self):
        """bun_creatinine_ratio computed when bun and creatinine present."""
        panel = {"bun": 20.0, "creatinine": 1.0}
        out = compute(panel)
        assert _get_val(out, "bun_creatinine_ratio") == pytest.approx(20.0, abs=0.001)

    def test_ast_alt_ratio_computed(self):
        """ast_alt_ratio computed when ast and alt present."""
        panel = {"ast": 40.0, "alt": 20.0}
        out = compute(panel)
        assert _get_val(out, "ast_alt_ratio") == pytest.approx(2.0, abs=0.001)

    def test_nlr_lab_supplied_wins(self):
        """When panel has nlr, use lab value (source=lab)."""
        panel = {"neutrophils": 8.0, "lymphocytes": 2.5, "nlr": 5.0}
        out = compute(panel)
        entry = out.get("derived", {}).get("nlr")
        assert entry["source"] == "lab"
        assert entry["value"] == pytest.approx(5.0, abs=0.001)


class TestInsightNoLocalRatioDivision:
    """Guard: insight modules must not compute RatioRegistry ratios locally."""

    def test_metabolic_age_no_direct_division_for_tc_tg_hdl(self):
        """metabolic_age must not contain (total_chol / hdl_chol) or (triglycerides / hdl_chol)."""
        from pathlib import Path
        path = Path(__file__).parent.parent.parent / "core" / "insights" / "modules" / "metabolic_age.py"
        text = path.read_text(encoding="utf-8")
        assert "total_chol / hdl_chol" not in text, "metabolic_age must not compute tc_hdl_ratio locally"
        assert "triglycerides / hdl_chol" not in text, "metabolic_age must not compute tg_hdl_ratio locally"

    def test_heart_insight_no_direct_division_for_lipid_ratios(self):
        """heart_insight must not contain (ldl_chol / hdl_chol), (total_chol / hdl_chol), (triglycerides / hdl_chol)."""
        from pathlib import Path
        path = Path(__file__).parent.parent.parent / "core" / "insights" / "modules" / "heart_insight.py"
        text = path.read_text(encoding="utf-8")
        assert "ldl_chol / hdl_chol" not in text, "heart_insight must not compute ldl_hdl_ratio locally"
        assert "total_chol / hdl_chol" not in text, "heart_insight must not compute tc_hdl_ratio locally"
        assert "triglycerides / hdl_chol" not in text, "heart_insight must not compute tg_hdl_ratio locally"

    def test_inflammation_no_division_for_nlr(self):
        """inflammation must not compute nlr via neutrophils / lymphocytes."""
        from pathlib import Path
        path = Path(__file__).parent.parent.parent / "core" / "insights" / "modules" / "inflammation.py"
        text = path.read_text(encoding="utf-8")
        assert "neutrophils / lymphocytes" not in text
        assert "lymphocytes / neutrophils" not in text

    def test_detox_filtration_no_division_for_bun_creatinine(self):
        """detox_filtration must not compute bun_creatinine_ratio via bun / creatinine."""
        from pathlib import Path
        path = Path(__file__).parent.parent.parent / "core" / "insights" / "modules" / "detox_filtration.py"
        text = path.read_text(encoding="utf-8")
        assert "bun / creatinine" not in text
        assert "bun / creat" not in text


class TestUnitNormalisationInvariant:
    """Orchestrator requires unit-normalised input; RatioRegistry uses base SI units."""

    def test_unnormalised_mg_dl_lipids_yield_wrong_non_hdl(self):
        """Un-normalised mg/dL lipids produce wrong non_hdl_cholesterol (TC-HDL requires mmol/L)."""
        from core.analytics.ratio_registry import compute
        from core.units.registry import apply_unit_normalisation

        # Raw mg/dL (un-normalised)
        raw = {
            "total_cholesterol": {"value": 200.0, "unit": "mg/dL", "reference_range": None},
            "hdl_cholesterol": {"value": 50.0, "unit": "mg/dL", "reference_range": None},
        }
        # Normalise first (production path)
        normalised = apply_unit_normalisation({k: v for k, v in raw.items()})
        panel_raw = {"total_cholesterol": 200.0, "hdl_cholesterol": 50.0}
        panel_norm = {
            "total_cholesterol": normalised["total_cholesterol"]["value"],
            "hdl_cholesterol": normalised["hdl_cholesterol"]["value"],
        }

        out_raw = compute(panel_raw)
        out_norm = compute(panel_norm)
        non_hdl_raw = out_raw.get("derived", {}).get("non_hdl_cholesterol", {}).get("value")
        non_hdl_norm = out_norm.get("derived", {}).get("non_hdl_cholesterol", {}).get("value")

        assert non_hdl_raw == pytest.approx(150.0, abs=0.01)  # 200 - 50 in mg/dL (wrong unit)
        assert non_hdl_norm == pytest.approx(3.885, abs=0.01)  # Correct in mmol/L
        assert non_hdl_raw != pytest.approx(non_hdl_norm, abs=0.1)  # Must differ
