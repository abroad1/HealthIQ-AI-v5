"""FE-VISUALISATION-B1B — SSOT alignment and contract checks for retail explainer registry."""

from __future__ import annotations

from pathlib import Path

import yaml

from core.contracts.retail_explainer_v1 import (
    BiomarkerEducationalExplainerV1,
    SystemEducationalExplainerV1,
)
from core.ssot.retail_explainer_registry_v1 import (
    cached_retail_explainer_registry_v1,
    load_retail_explainer_registry_v1,
)


def _backend_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _canonical_biomarker_ids() -> set[str]:
    path = _backend_root() / "ssot" / "biomarkers.yaml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(raw, dict) and isinstance(raw.get("biomarkers"), dict)
    return {str(k) for k in raw["biomarkers"].keys()}


def _canonical_system_keys() -> set[str]:
    path = _backend_root() / "ssot" / "biomarkers.yaml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(raw, dict) and isinstance(raw.get("biomarkers"), dict)
    systems: set[str] = set()
    for spec in raw["biomarkers"].values():
        if isinstance(spec, dict):
            s = spec.get("system")
            if isinstance(s, str) and s.strip():
                systems.add(s.strip())
    return systems


def test_retail_explainer_registry_b1b_loads_with_content():
    cached_retail_explainer_registry_v1.cache_clear()
    reg = load_retail_explainer_registry_v1()
    assert reg.biomarkers
    assert reg.systems
    assert reg.registry_version


def test_retail_explainer_registry_b1b_keys_match_ssot():
    cached_retail_explainer_registry_v1.cache_clear()
    reg = load_retail_explainer_registry_v1()
    biomarkers = _canonical_biomarker_ids()
    systems = _canonical_system_keys()
    for bid in reg.biomarkers:
        assert bid in biomarkers, f"registry biomarker_id not in biomarkers.yaml: {bid}"
    for sid in reg.systems:
        assert sid in systems, f"registry system_key not in biomarkers.yaml system field: {sid}"


def test_retail_explainer_registry_b1b_nonempty_educational_text():
    cached_retail_explainer_registry_v1.cache_clear()
    reg = load_retail_explainer_registry_v1()
    for bid, row in reg.biomarkers.items():
        assert row["title"].strip(), f"empty title for biomarker {bid}"
        body = row["body"].strip()
        assert body, f"empty body for biomarker {bid}"
        lowered = body.lower()
        assert "general education" in lowered or "educational" in lowered, bid


def test_retail_explainer_registry_b1b_contract_round_trip():
    cached_retail_explainer_registry_v1.cache_clear()
    reg = load_retail_explainer_registry_v1()
    for bid, row in reg.biomarkers.items():
        BiomarkerEducationalExplainerV1(biomarker_id=bid, title=row["title"], body=row["body"])
    for sid, row in reg.systems.items():
        SystemEducationalExplainerV1(system_key=sid, title=row["title"], body=row["body"])
