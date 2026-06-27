"""P2-2+P2-3 — retail explainer and pathway/missing-marker expansion."""

from __future__ import annotations

from pathlib import Path

import yaml

from core.ssot.retail_explainer_registry_v1 import load_retail_explainer_registry_v1

_REPO = Path(__file__).resolve().parents[3]
_REGISTRY = _REPO / "backend" / "ssot" / "retail_explainer_v1" / "registry.yaml"
_PATHWAYS = _REPO / "knowledge_bus" / "pathway_explainers_v1" / "pathway_explainers_v1.yaml"
_MISSING = _REPO / "knowledge_bus" / "missing_marker_explainers_v1" / "missing_marker_explainers_v1.yaml"

_PROHIBITED = (
    "you have iron deficiency",
    "you have hypothyroidism",
    "you need iron",
    "order this test",
    "you should take",
    "diagnosis of",
    "treatment recommendation",
)

_DIRECTIVE_MISSING = (
    "you must order",
    "you should order",
    "request this test",
)


def test_retail_explainer_coverage_at_least_forty_biomarkers() -> None:
    reg = load_retail_explainer_registry_v1()
    assert len(reg.biomarkers) >= 40


def test_retail_explainer_wave1_priority_markers_present() -> None:
    reg = load_retail_explainer_registry_v1()
    required = {
        "iron",
        "ferritin",
        "transferrin",
        "transferrin_saturation",
        "crp",
        "hemoglobin",
        "mcv",
        "vitamin_b12",
        "active_b12",
        "folate",
        "homocysteine",
        "creatinine",
        "egfr",
        "alt",
        "ast",
        "bilirubin",
        "tsh",
        "free_t3",
        "free_t4",
        "tpo_ab",
    }
    assert required.issubset(set(reg.biomarkers.keys()))


def test_retail_explainer_no_prohibited_wording() -> None:
    reg = load_retail_explainer_registry_v1()
    blob = yaml.safe_dump({"biomarkers": reg.biomarkers}).lower()
    for phrase in _PROHIBITED:
        assert phrase not in blob, phrase


def test_pathway_pack_includes_renal_and_wave1_domains() -> None:
    data = yaml.safe_load(_PATHWAYS.read_text(encoding="utf-8"))
    ids = {p.get("pathway_id") for p in data.get("pathways", []) if isinstance(p, dict)}
    assert "renal_filtration_handling_v1" in ids
    assert "blood_iron_oxygen_handling_v1" in ids
    assert "thyroid_hormone_antibody_context_v1" in ids
    assert "one_carbon_methylation_homocysteine_v1" in ids


def test_missing_marker_explainers_schema_and_cautionary_tone() -> None:
    data = yaml.safe_load(_MISSING.read_text(encoding="utf-8"))
    rows = data.get("missing_markers")
    assert isinstance(rows, list) and len(rows) >= 5
    for row in rows:
        assert row.get("missing_marker_id")
        assert row.get("biomarker_id")
        assert row.get("caution_when_absent", "").strip()
        assert row.get("interpretive_caution", "").strip()
        low = yaml.safe_dump(row).lower()
        for phrase in _DIRECTIVE_MISSING:
            assert phrase not in low
        assert (
            "less specific" in low
            or "incomplete" in low
            or "bounded" in low
            or "specificity" in low
        )


def test_p1_26_m1_iron_signal_library_package_ids_corrected() -> None:
    paths = (
        _REPO
        / "knowledge_bus/packages/pkg_kb52c_iron_low_absolute_iron_deficiency/signal_library.yaml",
        _REPO
        / "knowledge_bus/packages/pkg_kb52c_iron_low_functional_iron_restriction_inflammation/signal_library.yaml",
        _REPO
        / "knowledge_bus/packages/pkg_kb52c_iron_high_iron_overload_context/signal_library.yaml",
    )
    expected = (
        "pkg_kb52c_iron_low_absolute_iron_deficiency",
        "pkg_kb52c_iron_low_functional_iron_restriction_inflammation",
        "pkg_kb52c_iron_high_iron_overload_context",
    )
    for path, pkg_id in zip(paths, expected):
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert raw["library"]["package_id"] == pkg_id
