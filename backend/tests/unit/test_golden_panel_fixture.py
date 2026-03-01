"""
v5.3 Sprint 6 - Golden panel fixture sanity tests.
"""

import json
from pathlib import Path

from core.canonical.normalize import normalize_biomarkers_with_metadata


def test_golden_panel_fixture_contains_expected_size_and_shape():
    path = Path(__file__).parent.parent / "fixtures" / "golden_panel_160.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    assert isinstance(payload.get("biomarkers"), dict)
    assert len(payload["biomarkers"]) == 63
    normalize_biomarkers_with_metadata(payload["biomarkers"])
    sample_key = sorted(payload["biomarkers"].keys())[0]
    sample = payload["biomarkers"][sample_key]
    assert "value" in sample
    assert "unit" in sample
    assert "reference_range" in sample
