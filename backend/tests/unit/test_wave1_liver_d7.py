"""D-7 — liver consequence coherence (neutral vs strain) and governed YAML gate."""

from __future__ import annotations

from core.analytics.domain_narrative_wave1 import (
    headline_liv,
    idl_records_index,
    liv_consequence_primary,
)
from core.contracts.interpretation_display_layer_v1 import (
    InterpretationDisplayLayerBundleV1,
    InterpretationDisplayRecordV1,
)


def _hepatic_record(*, severity_state: str) -> InterpretationDisplayRecordV1:
    return InterpretationDisplayRecordV1(
        internal_id="ph_hepatic_alt_inflammatory_v1",
        scientific_class="organ_pattern",
        clinical_display_label="Hepatic inflammatory pattern",
        retail_display_label="Liver Stress Pattern",
        subtitle="A pattern suggesting metabolic or inflammatory strain in the liver",
        why_it_matters="Early liver-strain patterns are a key lane toward MASLD/fibrosis risk if ignored.",
        severity_state=severity_state,
        supporting_biomarkers_summary="ALT context",
        frontend_allowed_term="clinical_only",
        display_order_priority=4,
        enabled_for_frontend=True,
    )


def test_d7_liver_consequence_neutral_when_stable_surface_and_no_risk_led_evidence():
    """
    Stable/in-range contributor + strong headline + no active liver signals + no IDL bundle:
    must not emit static MASLD/fibrosis copy from YAML alone.
    """
    out = liv_consequence_primary(
        {},
        None,
        contributor_sentence="Your liver enzyme markers are within their reference ranges.",
        headline_sentence=headline_liv("strong"),
        active_liver_signal_ids=[],
    )
    assert "MASLD" not in out
    assert "enzyme snapshot" in out.lower()


def test_d7_liver_consequence_retains_strain_copy_when_hepatic_idl_is_risk_led():
    """Risk-led hepatic IDL with non-reassuring headline path still surfaces governed strain consequence."""
    rec = _hepatic_record(severity_state="watch")
    bundle = InterpretationDisplayLayerBundleV1(records=[rec])
    by_id = idl_records_index(bundle)
    out = liv_consequence_primary(
        by_id,
        "ph_hepatic_alt_inflammatory_v1",
        contributor_sentence="ALT is above the expected range, indicating hepatocellular strain in context.",
        headline_sentence=headline_liv("watch"),
        active_liver_signal_ids=["signal_alt_high"],
    )
    assert "MASLD" in out
