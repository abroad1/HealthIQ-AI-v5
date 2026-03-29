"""KB-S52B: regression proof for translation_remap_contract_KB-S52B_v1.yaml."""

from __future__ import annotations

from pathlib import Path

import yaml

from core.canonical.alias_registry_service import get_alias_registry_service

ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = ROOT.parent
REMAP_PATH = (
    REPO_ROOT / "knowledge_bus" / "governance" / "translation_remap_contract_KB-S52B_v1.yaml"
)
READINESS_PATH = (
    REPO_ROOT
    / "knowledge_bus"
    / "governance"
    / "translation_contract_v3_to_package_KB-S52B_v1.yaml"
)
SSOT_REGISTRY_PATH = ROOT / "ssot" / "biomarker_alias_registry.yaml"


def _load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict)
    return data


def _canonical_ids_from_registry(registry: dict) -> set[str]:
    ids: set[str] = set()
    for key, definition in registry.items():
        if isinstance(definition, dict) and definition.get("canonical_id"):
            ids.add(str(definition["canonical_id"]))
        else:
            ids.add(str(key))
    return ids


def test_kb_s52b_remap_contract_authority_file_exists() -> None:
    assert REMAP_PATH.is_file(), f"Missing governance artifact: {REMAP_PATH}"


def test_kb_s52b_approved_remaps_resolve_consistently() -> None:
    doc = _load_yaml(REMAP_PATH)
    resolver = get_alias_registry_service()
    approved = [r for r in doc["remaps"] if r["status"] == "APPROVED"]
    assert len(approved) == 3

    with SSOT_REGISTRY_PATH.open(encoding="utf-8") as f:
        registry = yaml.safe_load(f)
    canonical_ids = _canonical_ids_from_registry(registry)

    approved_upstream: set[str] = set()
    for row in approved:
        up = row["upstream_token"]
        down = row["downstream_canonical"]
        approved_upstream.add(up)

        res_up = resolver.resolve(up)
        assert res_up.startswith("unmapped_"), (
            f"Approved remap upstream {up!r} must be unmapped today; got {res_up!r}"
        )

        res_down = resolver.resolve(down)
        assert not res_down.startswith("unmapped_"), (
            f"Downstream {down!r} must resolve; got {res_down!r}"
        )
        assert res_down == down, f"Resolver must return canonical key {down!r}, got {res_down!r}"
        assert down in canonical_ids, f"{down!r} must appear in biomarker_alias_registry"


def test_kb_s52b_deferred_tokens_not_in_approved_list() -> None:
    doc = _load_yaml(REMAP_PATH)
    approved = {r["upstream_token"] for r in doc["remaps"] if r["status"] == "APPROVED"}
    assert approved == {"non_hdl", "fasting_glucose", "wbc_total"}

    deferred_tokens: set[str] = set()
    for block in doc["remaps_deferred"]:
        for t in block["upstream_tokens"]:
            deferred_tokens.add(t)

    assert "lym" in deferred_tokens
    assert "pth" in deferred_tokens
    assert "parathyroid_hormone" in deferred_tokens
    assert not deferred_tokens & approved

    resolver = get_alias_registry_service()
    for token in deferred_tokens:
        assert resolver.resolve(token).startswith("unmapped_")


def test_kb_s52b_readiness_waves_partition_tranche() -> None:
    doc = _load_yaml(READINESS_PATH)
    waves = doc["readiness_waves_spec_ids"]
    a = set(waves["wave_a_resolver_clean_no_remap_needed"]["spec_ids"])
    b = {e["spec_id"] for e in waves["wave_b_remap_only_subset_of_kb_s52b_approved_tokens"]["entries"]}
    c = set(waves["wave_c_blocked_prerequisite"]["spec_ids"])

    assert len(a) == 67
    assert len(b) == 4
    assert len(c) == 46
    assert a | b | c == a.union(b).union(c)
    assert len(a & b) == 0
    assert len(a & c) == 0
    assert len(b & c) == 0
    assert len(a) + len(b) + len(c) == 117
