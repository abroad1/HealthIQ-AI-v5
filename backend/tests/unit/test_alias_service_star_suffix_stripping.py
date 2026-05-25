"""
MAP-R1A — star-suffix abnormal lab marker stripping in alias resolution.
"""

from __future__ import annotations

import pytest

from core.canonical.alias_registry_service import (
    AliasRegistryService,
    get_alias_registry_service,
)


@pytest.fixture(scope="module")
def resolver() -> AliasRegistryService:
    get_alias_registry_service.cache_clear()
    svc = get_alias_registry_service()
    yield svc
    get_alias_registry_service.cache_clear()


MAP_R1A_STAR_AFFECTED = [
    ("Homocysteine (venous)*", "homocysteine"),
    ("Creatinine (venous)*", "creatinine"),
    ("TSH (venous)*", "tsh"),
    ("Vitamin B12 (venous)*", "vitamin_b12"),
    ("Active Vitamin B12 (venous)*", "active_b12"),
    ("Apolipoprotein A1 (venous)*", "apoa1"),
    ("Apolipoprotein B (venous)*", "apob"),
    ("Apolipoprotein Ratio (venous)*", "apob_apoa1_ratio"),
    ("Lipoprotein (a) (venous)*", "lipoprotein_a"),
    ("Corrected Calcium (venous)*", "corrected_calcium"),
    ("Vitamin D (venous)*", "vitamin_d"),
    ("Zinc (venous)*", "zinc"),
    ("Non HDL Cholesterol Calculation (venous)*", "non_hdl_cholesterol"),
    ("Total Cholesterol/HDL Ratio Calculation (venous)*", "tc_hdl_ratio"),
]


@pytest.mark.parametrize("label,canonical_id", MAP_R1A_STAR_AFFECTED)
def test_star_suffix_resolves_to_canonical(resolver: AliasRegistryService, label: str, canonical_id: str) -> None:
    assert resolver.resolve(label) == canonical_id
    assert not resolver.resolve(label).startswith("unmapped_")


@pytest.mark.parametrize("label,canonical_id", MAP_R1A_STAR_AFFECTED)
def test_clean_label_still_resolves(resolver: AliasRegistryService, label: str, canonical_id: str) -> None:
    clean = label.replace("*", "")
    assert resolver.resolve(clean) == canonical_id


def test_homocysteine_star_does_not_truncate_key(resolver: AliasRegistryService) -> None:
    result = resolver.resolve("Homocysteine (venous)*")
    assert result == "homocysteine"
    assert "homocysteine_(venous" not in result


def test_unknown_starred_label_remains_unmapped(resolver: AliasRegistryService) -> None:
    result = resolver.resolve("Totally Unknown Biomarker XYZ (venous)*")
    assert result.startswith("unmapped_")


def test_strip_abnormal_suffix_static() -> None:
    assert AliasRegistryService._strip_abnormal_lab_marker_suffix("Homocysteine (venous)*") == "Homocysteine (venous)"
    assert AliasRegistryService._strip_abnormal_lab_marker_suffix("TSH (venous)†") == "TSH (venous)"
    assert AliasRegistryService._strip_abnormal_lab_marker_suffix("Creatinine (venous) H") == "Creatinine (venous)"


def test_non_hdl_name_preserves_internal_h(resolver: AliasRegistryService) -> None:
    assert resolver.resolve("Non HDL Cholesterol Calculation (venous)*") == "non_hdl_cholesterol"
