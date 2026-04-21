"""N-6 — functional interpretation & confidence pack v1 (governed YAML)."""

from __future__ import annotations

from pathlib import Path

import yaml

_PACK = (
    Path(__file__).resolve().parents[3]
    / "knowledge_bus"
    / "functional_interpretation_v1"
    / "functional_interpretation_v1.yaml"
)

_REQUIRED_DOMAIN_KEYS = (
    "domain_id",
    "benchmark_domain",
    "display_title",
    "functional_reading",
    "why_beyond_itself",
    "confidence_grade_label",
    "confidence_supports_reading",
    "confidence_limits",
    "clarification_paths",
    "monitoring_improvement_signals",
    "monitoring_persistence_signals",
)


def _load_pack() -> dict:
    raw = yaml.safe_load(_PACK.read_text(encoding="utf-8"))
    assert isinstance(raw, dict)
    return raw


def test_pack_metadata():
    data = _load_pack()
    assert data.get("schema_version") == "1.0.0"
    assert data.get("pack_version") == "1.0.0"
    assert "functional_interpretation_v1" in str(data.get("authority", ""))


def test_two_benchmark_domains():
    data = _load_pack()
    domains = data.get("domains")
    assert isinstance(domains, list) and len(domains) == 2
    ids = {d.get("domain_id") for d in domains}
    assert ids == {
        "one_carbon_methylation_functional_v1",
        "lipid_transport_functional_v1",
    }


def test_compiler_fields_present_and_substantive():
    data = _load_pack()
    for d in data["domains"]:
        for key in _REQUIRED_DOMAIN_KEYS:
            assert key in d, f"missing {key} in {d.get('domain_id')}"
        assert isinstance(d["clarification_paths"], list)
        assert len(d["clarification_paths"]) >= 2
        for path in d["clarification_paths"]:
            assert isinstance(path, str) and len(path.strip()) > 10
        for prose_key in (
            "functional_reading",
            "why_beyond_itself",
            "confidence_supports_reading",
            "confidence_limits",
            "monitoring_improvement_signals",
            "monitoring_persistence_signals",
        ):
            assert len(str(d[prose_key]).strip()) > 80


def test_pathway_cross_refs():
    data = _load_pack()
    oc = next(x for x in data["domains"] if x["domain_id"] == "one_carbon_methylation_functional_v1")
    lip = next(x for x in data["domains"] if x["domain_id"] == "lipid_transport_functional_v1")
    assert oc.get("related_pathway_explainer_id") == "one_carbon_methylation_homocysteine_v1"
    assert lip.get("related_pathway_explainer_id") == "lipid_transport_cholesterol_handling_v1"
