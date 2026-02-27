import json

import pytest

from core.canonical.normalize import normalize_biomarkers_with_metadata, detect_canonical_collisions
from tools.run_golden_panel import _default_fixture_path


def test_default_golden_fixture_is_collision_free():
    """Default golden fixture must have no canonical collisions (same detector as golden runner)."""
    fixture_path = _default_fixture_path()
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    biomarkers = payload.get("biomarkers", {})

    collisions = detect_canonical_collisions(biomarkers)
    assert collisions == [], f"Default fixture has canonical collisions: {collisions}"

    normalized = normalize_biomarkers_with_metadata(biomarkers)
    assert isinstance(normalized, dict)
    assert len(normalized) > 0
