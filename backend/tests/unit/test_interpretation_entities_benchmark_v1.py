"""N-7 — benchmark interpretation entities pack (governed bindings for N-8 compiler)."""

from __future__ import annotations

from pathlib import Path

import yaml

_ENTITIES = (
    Path(__file__).resolve().parents[3]
    / "knowledge_bus"
    / "interpretation_entities_v1"
    / "benchmark_interpretation_entities_v1.yaml"
)
_PATHWAYS = (
    Path(__file__).resolve().parents[3]
    / "knowledge_bus"
    / "pathway_explainers_v1"
    / "pathway_explainers_v1.yaml"
)
_FUNCTIONAL = (
    Path(__file__).resolve().parents[3]
    / "knowledge_bus"
    / "functional_interpretation_v1"
    / "functional_interpretation_v1.yaml"
)


def _load(path: Path) -> dict:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(raw, dict)
    return raw


def test_pack_metadata_and_deferred_vascular():
    data = _load(_ENTITIES)
    assert data.get("schema_version") == "1.0.0"
    assert data.get("pack_version") == "1.0.0"
    xs = data.get("cross_system_vascular_synthesis") or {}
    assert xs.get("decision") == "deferred"
    assert isinstance(xs.get("rationale", ""), str) and len(xs["rationale"].strip()) > 50


def test_four_interpretation_entities_with_bindings():
    data = _load(_ENTITIES)
    rows = data.get("interpretation_entities")
    assert isinstance(rows, list) and len(rows) == 4
    ids = {r.get("interpretation_entity_id") for r in rows}
    assert ids == {
        "int_benchmark_blood_iron_oxygen_lead_v1",
        "int_benchmark_thyroid_hormone_antibody_lead_v1",
        "int_benchmark_one_carbon_homocysteine_macrocytosis_v1",
        "int_benchmark_lipid_residual_ldl_favourable_transport_v1",
    }
    pathway = _load(_PATHWAYS)
    pathway_ids = {p.get("pathway_id") for p in pathway.get("pathways", [])}
    functional = _load(_FUNCTIONAL)
    domain_ids = {d.get("domain_id") for d in functional.get("domains", [])}
    for r in rows:
        assert r.get("pathway_explainer_id") in pathway_ids
        assert r.get("functional_interpretation_domain_id") in domain_ids
        assert r.get("phenotype_id")
        assert r.get("idl_internal_id") == r.get("phenotype_id")
