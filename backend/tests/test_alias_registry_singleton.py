"""
Regression test: AliasRegistryService must build the registry at most once per request flow.

This test ensures that within a single request-like flow, the registry is built/loaded
at most once. Multiple resolves must be pure lookups.
"""

import pytest
from unittest.mock import patch

from core.canonical.alias_registry_service import (
    AliasRegistryService,
    get_alias_registry_service,
)
from core.canonical.normalize import BiomarkerNormalizer, normalize_biomarkers_with_metadata


# Force fresh singleton state for each test by clearing lru_cache
def _clear_singleton_cache():
    get_alias_registry_service.cache_clear()


@pytest.fixture(autouse=True)
def clear_cache_between_tests():
    """Ensure each test starts with a fresh cache."""
    _clear_singleton_cache()
    yield
    _clear_singleton_cache()


def test_registry_load_at_most_once_per_request_flow():
    """
    Simulate route flow: normalize_biomarkers_with_metadata + multiple normalizers
    (as would happen with orchestrator + scoring engine + completeness + gaps).
    Patch _load_alias_registry; assert it is called at most once.
    """
    with patch(
        "core.canonical.alias_registry_service.AliasRegistryService._load_alias_registry"
    ) as mock_load:
        mock_load.return_value = {
            "hdl": {"aliases": ["HDL", "hdl_cholesterol"], "canonical_id": "hdl"},
            "ldl": {"aliases": ["LDL", "ldl_cholesterol"], "canonical_id": "ldl"},
            "total_cholesterol": {
                "aliases": ["TC", "Total Cholesterol"],
                "canonical_id": "total_cholesterol",
            },
            "triglycerides": {
                "aliases": ["TG", "Trigs"],
                "canonical_id": "triglycerides",
            },
        }

        biomarkers = {
            "hdl": {"value": 45.0, "unit": "mg/dL", "reference_range": {"min": 40, "max": 60, "unit": "mg/dL", "source": "lab"}},
            "ldl": {"value": 120.0, "unit": "mg/dL", "reference_range": {"min": 0, "max": 100, "unit": "mg/dL", "source": "lab"}},
            "total_cholesterol": {"value": 200.0, "unit": "mg/dL", "reference_range": {"min": 0, "max": 200, "unit": "mg/dL", "source": "lab"}},
            "triglycerides": {"value": 150.0, "unit": "mg/dL", "reference_range": {"min": 0, "max": 150, "unit": "mg/dL", "source": "lab"}},
        }

        # Step 1: Route-style normalization (creates normalizer, uses singleton)
        normalized = normalize_biomarkers_with_metadata(biomarkers)

        # Step 2: Additional normalizers (as orchestrator + scoring + completeness create)
        # All should share the same alias service singleton
        n2 = BiomarkerNormalizer()
        n2.normalize_biomarkers({k: v.get("value", v) for k, v in normalized.items()})

        n3 = BiomarkerNormalizer()
        n3.get_canonical_biomarkers()

        # _load_alias_registry should be called at most once for the entire flow
        assert mock_load.call_count <= 1, (
            f"Alias registry loaded {mock_load.call_count} times; expected at most 1. "
            "Registry must be built once and reused for all resolves."
        )


def test_multiple_resolves_use_cached_registry():
    """
    Resolve many biomarkers in sequence; _build_alias_mapping / load should run once.
    """
    _clear_singleton_cache()
    with patch(
        "core.canonical.alias_registry_service.AliasRegistryService._load_alias_registry"
    ) as mock_load:
        mock_load.return_value = {
            "hdl": {"aliases": ["HDL"], "canonical_id": "hdl"},
            "ldl": {"aliases": ["LDL"], "canonical_id": "ldl"},
            "glucose": {"aliases": ["blood_sugar"], "canonical_id": "glucose"},
        }

        service = get_alias_registry_service()
        biomarkers = ["hdl", "ldl", "glucose", "HDL", "LDL", "blood_sugar"]
        for name in biomarkers:
            service.resolve(name)

        assert mock_load.call_count == 1, (
            f"_load_alias_registry called {mock_load.call_count} times for {len(biomarkers)} resolves; expected 1."
        )


def test_get_alias_registry_service_returns_same_instance():
    """get_alias_registry_service(True) returns the same instance on repeated calls."""
    _clear_singleton_cache()
    s1 = get_alias_registry_service()
    s2 = get_alias_registry_service()
    assert s1 is s2
