"""KB-HBA1C-GOV1 — HbA1c mmol/mol normalisation and Layer B arbitration."""

import copy

import pytest

from core.canonical.hba1c_layer_b_arbitration import arbitrate_hba1c_layer_b_input
from core.canonical.normalize import normalize_biomarkers_with_metadata
from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
from core.units.registry import UNIT_REGISTRY_VERSION, apply_unit_normalisation, convert_value
from core.canonical.alias_registry_service import AliasRegistryService, get_alias_registry_service


@pytest.fixture(autouse=True)
def _disable_common_alias_injection(monkeypatch):
    get_alias_registry_service.cache_clear()
    monkeypatch.setattr(
        AliasRegistryService,
        "_add_common_aliases",
        lambda self, alias_mapping, insert_alias: None,
    )
    yield
    get_alias_registry_service.cache_clear()


def _prepare_layer_b_payload(biomarkers: dict) -> dict:
    normalized = normalize_biomarkers_with_metadata(biomarkers)
    normalized = arbitrate_hba1c_layer_b_input(normalized)
    normalized = apply_unit_normalisation(normalized)
    normalized[UNIT_NORMALISATION_META_KEY] = {
        "unit_normalised": True,
        "unit_registry_version": UNIT_REGISTRY_VERSION,
    }
    return normalized


class TestHbA1cMmolMolToPercent:
    def test_hba1c_mmol_mol_converts_to_percent_diabetes_threshold(self):
        """48 mmol/mol aligns ~6.5% NGSP (paired criteria)."""
        val, unit = convert_value("hba1c", 48.0, "mmol/mol")
        assert unit == "%"
        assert abs(val - 6.54304) < 0.02

    def test_hba1c_percent_identity(self):
        val, unit = convert_value("hba1c", 5.5, "%")
        assert unit == "%"
        assert val == 5.5


class TestHbA1cArbitration:
    def test_both_ids_only_hba1c_remains(self):
        raw = {
            "hba1c": {"value": 48.0, "unit": "mmol/mol"},
            "hba1c_pct": {"value": 6.5, "unit": "%"},
        }
        normalized = normalize_biomarkers_with_metadata(raw)
        out = arbitrate_hba1c_layer_b_input(normalized)
        assert "hba1c" in out
        assert "hba1c_pct" not in out
        assert out["hba1c"]["value"] == 48.0
        assert out["hba1c"]["unit"] == "mmol/mol"

    def test_only_hba1c_pct_promoted_to_hba1c(self):
        raw = {"hba1c_pct": {"value": 6.2, "unit": "%"}}
        normalized = normalize_biomarkers_with_metadata(raw)
        out = arbitrate_hba1c_layer_b_input(normalized)
        assert "hba1c" in out
        assert "hba1c_pct" not in out
        assert out["hba1c"]["value"] == 6.2
        assert out["hba1c"]["unit"] == "%"

    def test_input_not_mutated(self):
        raw = {
            "hba1c": {"value": 40.0, "unit": "mmol/mol"},
            "hba1c_pct": {"value": 5.0, "unit": "%"},
        }
        normalized = normalize_biomarkers_with_metadata(raw)
        snapshot = copy.deepcopy(normalized)
        arbitrate_hba1c_layer_b_input(normalized)
        assert normalized == snapshot


class TestHbA1cLayerBBoundPath:
    def test_orchestrator_input_excludes_hba1c_pct_when_both_present(self):
        user = {"user_id": "t", "age": 40, "gender": "male"}
        raw = {
            "glucose": {"value": 5.0, "unit": "mmol/L"},
            "hba1c": {"value": 48.0, "unit": "mmol/mol"},
            "hba1c_pct": {"value": 6.5, "unit": "%"},
        }
        prepared = _prepare_layer_b_payload(raw)
        assert "hba1c_pct" not in prepared
        assert "hba1c" in prepared
        orch = AnalysisOrchestrator()
        dto = orch.run(prepared, user, assume_canonical=True)
        names = [b.biomarker_name for b in dto.biomarkers if hasattr(b, "biomarker_name")]
        assert "hba1c_pct" not in names
        assert "hba1c" in names

    def test_no_duplicate_hba1c_metrics_in_signal_path_keys(self):
        """Layer B-bound dict has at most one HbA1c analytical key (hba1c)."""
        raw = {
            "hba1c": {"value": 42.0, "unit": "mmol/mol"},
            "hba1c_pct": {"value": 6.0, "unit": "%"},
        }
        prepared = _prepare_layer_b_payload(raw)
        keys = [k for k in prepared.keys() if k != UNIT_NORMALISATION_META_KEY]
        hb_keys = [k for k in keys if "hba1c" in k]
        assert hb_keys == ["hba1c"]
