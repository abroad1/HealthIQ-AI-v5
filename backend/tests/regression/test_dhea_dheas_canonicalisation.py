"""Regression tests for DHEA / DHEA-S unit-aware canonicalisation."""

from __future__ import annotations

import json
from pathlib import Path

from core.canonical.alias_registry_service import get_alias_registry_service
from core.canonical.normalize import BiomarkerNormalizer, normalize_biomarkers_with_metadata

REPO_ROOT = Path(__file__).resolve().parents[3]
AB_PANEL = REPO_ROOT / "backend/tests/fixtures/panels/ab_full_panel_with_ranges.json"


def _reset_alias_cache():
    get_alias_registry_service.cache_clear()


def test_ab_panel_dhea_key_canonicalises_to_dhea_s_with_metadata():
    _reset_alias_cache()
    payload = json.loads(AB_PANEL.read_text(encoding="utf-8"))
    biomarkers = payload["biomarkers"]
    result = normalize_biomarkers_with_metadata({"DHEA (Venous)": biomarkers["dhea"]})
    assert "dhea_s" in result
    assert result["dhea_s"]["value"] == biomarkers["dhea"]["value"]
    assert result["dhea_s"]["unit"] == biomarkers["dhea"]["unit"]
    assert result["dhea_s"]["reference_range"]["max"] == 15.44
    assert result["dhea_s"]["raw_label"] == "DHEA (Venous)"
    assert result["dhea_s"]["identity_confidence"] == "HIGH_CONFIDENCE_UNIT_RANGE_MATCH"
    _reset_alias_cache()


def test_ambiguous_dhea_label_only_does_not_map_to_dhea_s():
    _reset_alias_cache()
    normalizer = BiomarkerNormalizer()
    panel, unmapped = normalizer.normalize_biomarkers({"DHEA": {"value": 5.0}})
    assert unmapped == ["DHEA"]
    assert "dhea_s" not in panel.biomarkers
    assert any(k.startswith("unmapped_") for k in panel.biomarkers)
    _reset_alias_cache()


def test_preserves_raw_label_unit_and_reference_range():
    _reset_alias_cache()
    entry = {
        "value": 12.0,
        "unit": "umol/L",
        "reference_range": {"min": 0.94, "max": 15.44, "unit": "umol/L", "source": "lab"},
    }
    result = normalize_biomarkers_with_metadata({"DHEA": entry})
    assert result["dhea_s"]["raw_label"] == "DHEA"
    assert result["dhea_s"]["unit"] == "umol/L"
    assert result["dhea_s"]["reference_range"]["max"] == 15.44
    assert result["dhea_s"]["identity_resolution_reason"]
    _reset_alias_cache()
