import json

import pytest

from core.canonical import normalize as normalize_mod
from core.canonical.normalize import normalize_biomarkers_with_metadata
from tools.run_golden_panel import _default_fixture_path


def test_default_golden_fixture_is_collision_free():
    fixture_path = _default_fixture_path()
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    biomarkers = payload.get("biomarkers", {})

    collision_exc = getattr(normalize_mod, "CanonicalCollisionError", None)
    try:
        normalized = normalize_biomarkers_with_metadata(biomarkers)
    except Exception as exc:  # pragma: no cover - explicit assertion branch
        if collision_exc is not None and isinstance(exc, collision_exc):
            pytest.fail(f"Default fixture has canonical collisions: {exc}")
        raise

    assert isinstance(normalized, dict)
    assert len(normalized) > 0
