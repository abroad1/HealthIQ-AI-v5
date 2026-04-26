"""D-2 Wave 1 domain narrative: lipid-dominant CV consequence from governed idl registry."""

from __future__ import annotations

from core.analytics.domain_narrative_wave1 import cv_consequence, governed_idl_field, idl_records_index
from core.contracts.interpretation_display_layer_v1 import InterpretationDisplayLayerBundleV1


def test_governed_lipid_why_it_matters_loads_from_idl_registry():
    t = governed_idl_field("ph_lipid_residual_ldl_favourable_transport_v1", "why_it_matters")
    assert t
    assert "atherogenic" in t.lower() or "ldl" in t.lower()


def test_cv_consequence_falls_back_to_governed_lipid_for_lipid_dominant():
    # Empty bundle: no active IDL rows
    bundle = InterpretationDisplayLayerBundleV1(records=[])
    by_id = idl_records_index(bundle)
    rows = [
        {
            "signal_id": "signal_ldl_cholesterol_high",
            "signal_state": "at_risk",
            "system": "lipid_transport",
            "primary_metric": "ldl_cholesterol",
        }
    ]
    out = cv_consequence(by_id, ["signal_ldl_cholesterol_high"], rows)
    assert out
    assert "transport" in out.lower() or "atherogenic" in out.lower()
