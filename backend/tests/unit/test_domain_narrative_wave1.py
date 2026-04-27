"""D-2 Wave 1 domain narrative: lipid-dominant CV consequence from governed idl registry."""

from __future__ import annotations

from types import SimpleNamespace

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


def test_d4_headline_cv_avoids_broadly_stable_when_story_implies_strain():
    from core.analytics.domain_narrative_wave1 import headline_cv_coherent, headline_cv

    contrib = "Homocysteine is elevated, adding a vascular-stress context alongside the lipid picture."
    cons = "Elevated atherogenic risk in context of transport markers."
    h = headline_cv_coherent("stable", contrib, cons)
    assert "broadly stable" not in h.lower()
    assert headline_cv("stable") != h


def test_d4_headline_met_avoids_broadly_stable_when_metabolic_strain():
    from core.analytics.domain_narrative_wave1 import headline_met_coherent, headline_met

    c = "The triglyceride–glucose pattern suggests early insulin-resistance stress."
    q = "Sustained glycaemic load matters for long-term risk."
    h = headline_met_coherent("stable", c, q)
    assert "broadly stable" not in h.lower()
    assert headline_met("stable") != h


def test_headline_cv_coherent_strong_band_blocked_when_primary_rec_is_risk_led():
    """D-6: strong band must not emit reassuring headline_cv('strong') when primary IDL is risk-led."""
    from core.analytics.domain_narrative_wave1 import headline_cv, headline_cv_coherent

    reassuring_strong = headline_cv("strong")
    primary_rec = SimpleNamespace(severity_state="watch")
    out = headline_cv_coherent(
        "strong",
        "Lipids look favourable on paper.",
        "Residual transport risk still warrants structured review.",
        primary_rec=primary_rec,
    )
    assert out != reassuring_strong
    assert "looks strong" not in out.lower()


def test_d4_confidence_cv_bridges_homocysteine_when_tier_not_high():
    from core.analytics.domain_narrative_wave1 import confidence_sentence_cv_coherent, confidence_sentence_for

    contrib = "Homocysteine is elevated, adding vascular-stress context."
    s = confidence_sentence_cv_coherent("medium", contrib)
    assert "homocysteine" in s.lower()
    assert s != confidence_sentence_for("medium", "cv")
