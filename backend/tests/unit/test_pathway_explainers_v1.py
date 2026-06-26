"""N-5 — pathway explainer pack v1 structure (governed YAML, compiler-ready fields)."""

from __future__ import annotations

from pathlib import Path

import yaml

_PACK = (
    Path(__file__).resolve().parents[3]
    / "knowledge_bus"
    / "pathway_explainers_v1"
    / "pathway_explainers_v1.yaml"
)


def _load_pack() -> dict:
    raw = yaml.safe_load(_PACK.read_text(encoding="utf-8"))
    assert isinstance(raw, dict)
    return raw


def test_pack_version_and_authority():
    data = _load_pack()
    assert data.get("schema_version") == "1.0.0"
    assert data.get("pack_version") == "1.0.0"
    assert "pathway_explainers_v1" in str(data.get("authority", ""))


def test_four_benchmark_pathways_present():
    data = _load_pack()
    pathways = data.get("pathways")
    assert isinstance(pathways, list) and len(pathways) == 4
    ids = {p.get("pathway_id") for p in pathways}
    assert ids == {
        "one_carbon_methylation_homocysteine_v1",
        "lipid_transport_cholesterol_handling_v1",
        "blood_iron_oxygen_handling_v1",
        "thyroid_hormone_antibody_context_v1",
    }


def test_one_carbon_fields_non_empty():
    data = _load_pack()
    p = next(x for x in data["pathways"] if x["pathway_id"] == "one_carbon_methylation_homocysteine_v1")
    for key in (
        "homocysteine_in_this_pathway",
        "remethylation_and_transsulfuration",
        "red_blood_cell_maturation_link",
        "interpretive_friction_when_serum_b12_folate_improve",
        "pathway_role",
        "system_in_action",
        "markers_belong_together",
        "why_matters_beyond_a_single_marker_reading",
        "interpretive_caution",
    ):
        assert isinstance(p.get(key), str) and len(p[key].strip()) > 40


def test_lipid_fields_non_empty():
    data = _load_pack()
    p = next(x for x in data["pathways"] if x["pathway_id"] == "lipid_transport_cholesterol_handling_v1")
    for key in (
        "lipid_particles_as_transport_architecture",
        "apob_triglycerides_hdl_ldl_together",
        "beyond_a_single_ldl_value",
        "protective_and_atherogenic_can_coexist",
        "pathway_role",
        "system_in_action",
        "why_matters_beyond_simple_high_cholesterol_framing",
        "interpretive_caution",
    ):
        assert isinstance(p.get(key), str) and len(p[key].strip()) > 40


def test_no_giant_unstructured_only_blob():
    """Each pathway uses multiple compiler-addressable fields (not a single body key)."""
    data = _load_pack()
    for p in data["pathways"]:
        text_fields = [k for k, v in p.items() if isinstance(v, str) and k != "display_title"]
        assert len(text_fields) >= 8
