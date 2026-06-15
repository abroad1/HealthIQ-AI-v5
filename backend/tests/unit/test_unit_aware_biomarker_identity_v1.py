"""Unit tests for unit-aware DHEA / DHEA-S biomarker identity resolution."""

from __future__ import annotations

from core.canonical.unit_aware_biomarker_identity_v1 import (
    CONFIDENCE_FAIL_CLOSED,
    CONFIDENCE_HIGH_UNIT_RANGE,
    resolve_unit_aware_biomarker_identity,
)


def _dhea_s_range():
    return {"min": 0.94, "max": 15.44, "unit": "umol/L", "source": "lab"}


def test_dhea_venous_umol_l_range_resolves_to_dhea_s():
    result = resolve_unit_aware_biomarker_identity(
        raw_label="DHEA (Venous)",
        unit="umol/L",
        reference_range=_dhea_s_range(),
    )
    assert result is not None
    assert result.canonical_id == "dhea_s"
    assert result.confidence == CONFIDENCE_HIGH_UNIT_RANGE
    assert result.raw_label == "DHEA (Venous)"


def test_dhea_umol_l_range_resolves_to_dhea_s():
    result = resolve_unit_aware_biomarker_identity(
        raw_label="DHEA",
        unit="µmol/L",
        reference_range=_dhea_s_range(),
        label_canonical_hint="dhea",
    )
    assert result is not None
    assert result.canonical_id == "dhea_s"
    assert result.confidence == CONFIDENCE_HIGH_UNIT_RANGE


def test_dheas_label_resolves_to_dhea_s():
    result = resolve_unit_aware_biomarker_identity(raw_label="DHEAS")
    assert result is not None
    assert result.canonical_id == "dhea_s"


def test_dhea_s_label_resolves_to_dhea_s():
    result = resolve_unit_aware_biomarker_identity(raw_label="DHEA-S")
    assert result is not None
    assert result.canonical_id == "dhea_s"


def test_ambiguous_dhea_without_unit_or_range_fails_closed():
    result = resolve_unit_aware_biomarker_identity(
        raw_label="DHEA",
        label_canonical_hint="dhea",
    )
    assert result is not None
    assert result.fail_closed is True
    assert result.confidence == CONFIDENCE_FAIL_CLOSED
    assert result.canonical_id.startswith("unmapped_")


def test_unit_range_conflict_fails_closed():
    result = resolve_unit_aware_biomarker_identity(
        raw_label="DHEA",
        unit="umol/L",
        reference_range={"min": 0.0, "max": 100.0, "unit": "umol/L"},
        label_canonical_hint="dhea",
    )
    assert result is not None
    assert result.fail_closed is True
