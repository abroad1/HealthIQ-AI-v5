"""P1-24 — Bio-oxygen compiled subsystem card signal depth tests."""

from __future__ import annotations

from core.analytics.wave1_subsystem_evidence import assemble_wave1_subsystem_evidence
from core.knowledge.health_system_card_evidence import get_card_evidence_artefact


def test_bio_oxygen_card_includes_p1_24_source_spec_ids():
    artefact = get_card_evidence_artefact("wave1_bio_oxygen_carrying_capacity")
    assert artefact.compile_manifest_ref.endswith("p1_26_iron_homocysteine_card_evidence.yaml")
    assert {
        "inv_ferritin_high_inflammatory_hyperferritinemia",
        "inv_ferritin_high_iron_overload_context",
        "inv_transferrin_high_iron_deficiency_transport_upregulation",
    } <= set(artefact.source_spec_ids)
    assert "inv_hgb_low_normocytic_underproduction_context" in artefact.source_spec_ids
    assert "inv_ferritin_low_iron_store_depletion" in artefact.source_spec_ids


def test_bio_oxygen_card_includes_transferrin_contextual_marker():
    artefact = get_card_evidence_artefact("wave1_bio_oxygen_carrying_capacity")
    by_id = {m.marker_id: m for m in artefact.markers}
    assert "transferrin" in by_id
    transferrin = by_id["transferrin"]
    assert transferrin.marker_role == "contextual_marker"
    assert transferrin.relationship_kind == "contextual_support"
    assert transferrin.presence_policy == "optional_on_panel"
    ferritin = by_id["ferritin"]
    assert "inflammatory hyperferritinemia" in ferritin.rationale_short.lower()
    assert "iron overload" in ferritin.rationale_short.lower()


def test_bio_oxygen_subsystem_evidence_emits_enriched_card_with_transferrin():
    panel = {"hemoglobin", "hematocrit", "ferritin", "transferrin"}
    rows = assemble_wave1_subsystem_evidence(
        domain_id="wave1_blood_iron_oxygen",
        panel_biomarker_ids=panel,
        rail_biomarker_scores=[
            {"biomarker_name": "hemoglobin"},
            {"biomarker_name": "hematocrit"},
        ],
    )
    assert len(rows) == 1
    row = rows[0]
    assert row.subsystem_id == "wave1_bio_oxygen_carrying_capacity"
    assert "transferrin" in row.included_marker_ids
    assert "p1_26_iron_homocysteine_card_evidence.yaml" in row.compile_manifest_ref
