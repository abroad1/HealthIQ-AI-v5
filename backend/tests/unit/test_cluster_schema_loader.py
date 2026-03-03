"""
Unit tests for clustering cluster schema loader migration.
"""

from pathlib import Path

import pytest

import core.clustering.cluster_schema_loader as cluster_schema_loader


EXPECTED_CLUSTER_IDS = {
    "metabolic",
    "cardiovascular",
    "hepatic",
    "renal",
    "inflammatory",
    "hematological",
    "hormonal",
    "nutritional",
}


def test_loader_determinism_with_cache_reset():
    cluster_schema_loader._schema_cache = None
    schema_a = cluster_schema_loader.load_cluster_schema()
    hash_a = schema_a.schema_hash
    cluster_schema_loader._schema_cache = None
    schema_b = cluster_schema_loader.load_cluster_schema()
    hash_b = schema_b.schema_hash
    assert hash_a == hash_b


def test_schema_hash_present_and_stable():
    cluster_schema_loader._schema_cache = None
    schema = cluster_schema_loader.load_cluster_schema()
    assert isinstance(schema.schema_hash, str)
    assert len(schema.schema_hash) == 16
    assert all(ch in "0123456789abcdef" for ch in schema.schema_hash)

    cluster_schema_loader._schema_cache = None
    schema_2 = cluster_schema_loader.load_cluster_schema()
    assert schema.schema_hash == schema_2.schema_hash


def test_expected_cluster_ids_stable():
    cluster_schema_loader._schema_cache = None
    schema = cluster_schema_loader.load_cluster_schema()
    assert set(schema.clusters.keys()) == EXPECTED_CLUSTER_IDS


def test_validation_cluster_id_mismatch_raises_value_error(monkeypatch: pytest.MonkeyPatch):
    cluster_schema_loader._schema_cache = None
    monkeypatch.setattr(
        cluster_schema_loader.yaml,
        "safe_load",
        lambda _: {
            "version": "1.0.0",
            "schema_version": "1.0",
            "clusters": {
                "metabolic": {
                    "cluster_id": "renal",
                    "description": "Bad",
                    "biomarker_membership": {"required": ["glucose"], "important": [], "optional": []},
                }
            },
        },
    )
    with pytest.raises(ValueError) as exc_info:
        cluster_schema_loader.load_cluster_schema()
    assert str(exc_info.value).strip()


def test_validation_unknown_biomarker_raises_value_error():
    canonical = {"glucose", "hba1c"}
    with pytest.raises(ValueError) as exc_info:
        cluster_schema_loader._validate_cluster(
            "metabolic",
            {
                "cluster_id": "metabolic",
                "description": "Bad",
                "biomarker_membership": {"required": ["unknown_xyz"], "important": [], "optional": []},
            },
            canonical,
        )
    assert str(exc_info.value).strip()


def test_validation_duplicate_biomarker_raises_value_error():
    canonical = {"glucose", "hba1c"}
    with pytest.raises(ValueError) as exc_info:
        cluster_schema_loader._validate_cluster(
            "metabolic",
            {
                "cluster_id": "metabolic",
                "description": "Bad",
                "biomarker_membership": {"required": ["glucose"], "important": [], "optional": ["glucose"]},
            },
            canonical,
        )
    assert str(exc_info.value).strip()


def test_validation_non_dict_cluster_entry_raises_value_error(monkeypatch: pytest.MonkeyPatch):
    cluster_schema_loader._schema_cache = None
    monkeypatch.setattr(
        cluster_schema_loader.yaml,
        "safe_load",
        lambda _: {
            "version": "1.0.0",
            "schema_version": "1.0",
            "clusters": {"metabolic": "not-a-dict"},
        },
    )
    with pytest.raises(ValueError) as exc_info:
        cluster_schema_loader.load_cluster_schema()
    assert str(exc_info.value).strip()


def test_clustering_runtime_has_no_analytics_cluster_schema_import():
    repo_backend_root = Path(__file__).resolve().parents[2]
    clustering_dir = repo_backend_root / "core" / "clustering"
    for py_file in clustering_dir.rglob("*.py"):
        if "__pycache__" in py_file.parts:
            continue
        text = py_file.read_text(encoding="utf-8")
        assert "core.analytics.cluster_schema" not in text
