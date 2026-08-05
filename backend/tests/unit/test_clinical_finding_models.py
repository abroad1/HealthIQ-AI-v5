"""
CLIN-PRIORITY-CORE-1 — Unit tests for clinical finding models.
"""

import pytest
from pydantic import ValidationError

from core.models.clinical_finding import (
    ClinicalFinding,
    ConsolidatedConcernSet,
    FindingProvenance,
    make_finding_id,
)


def test_finding_id_deterministic_and_order_independent():
    a = make_finding_id("hepatic", "HEP-F1", ["b::x", "a::y"])
    b = make_finding_id("hepatic", "HEP-F1", ["a::y", "b::x"])
    c = make_finding_id("hepatic", "HEP-F1", ["a::y", "b::x", "a::y"])
    assert a == b == c
    assert a.startswith("hepatic:HEP-F1:")


def test_clinical_finding_requires_activation_keys_and_matching_id():
    keys = ["signal_alt_high::inv_alt_high_r_value_hepatocellular_biochemical_pattern"]
    fid = make_finding_id("hepatic", "HEP-F1", keys)
    finding = ClinicalFinding(
        finding_id=fid,
        domain="hepatic",
        finding_type="HEP-F1",
        label="consolidated_hepatocellular_enzyme_elevation",
        constituent_activation_keys=keys,
        urgency_time_band="within_days",
        severity_band="marked",
        concern_tier=1,
        role="principal_concern",
        provenance=FindingProvenance(clinical_rule_ids=["HEP-CONS-1"]),
    )
    assert finding.constituent_activation_keys == keys

    with pytest.raises(ValidationError):
        ClinicalFinding(
            finding_id="wrong",
            domain="hepatic",
            finding_type="HEP-F1",
            label="x",
            constituent_activation_keys=keys,
            urgency_time_band="within_days",
            concern_tier=1,
            role="principal_concern",
        )

    with pytest.raises(ValidationError):
        ClinicalFinding(
            finding_id=make_finding_id("hepatic", "HEP-F1", ["k"]),
            domain="hepatic",
            finding_type="HEP-F1",
            label="x",
            constituent_activation_keys=[],
            urgency_time_band="within_days",
            concern_tier=1,
            role="principal_concern",
        )


def test_consolidated_concern_set_frozen_and_quarantine_defaults():
    concern = ConsolidatedConcernSet(no_concern=True, no_concern_notes=["note"])
    assert concern.fib_4_computed is False
    assert concern.fib_4_displayed is False
    assert concern.presentation_mode == "principal"
    with pytest.raises(ValidationError):
        concern.no_concern = False  # type: ignore[misc]
