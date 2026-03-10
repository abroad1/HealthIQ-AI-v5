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


def test_cluster_scoring_policy_loads():
    cluster_schema_loader._cluster_scoring_policy_cache = None
    policy = cluster_schema_loader.load_cluster_scoring_policy()
    assert policy.policy_version
    assert policy.schema_version
    assert policy.min_members_per_cluster >= 1
    assert policy.severity_thresholds["critical_lt"] < policy.severity_thresholds["high_lt"]


def test_cluster_scoring_policy_validation_fails_on_invalid_thresholds(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    bad = tmp_path / "cluster_scoring_policy.yaml"
    bad.write_text(
        "policy_version: '1.0.0'\n"
        "schema_version: '1.0'\n"
        "cluster_membership: {min_members_per_cluster: 2}\n"
        "severity_thresholds: {critical_lt: 40, high_lt: 30, moderate_lt: 70, mild_lt: 85}\n"
        "confidence: {variance_divisor: 2500, size_boost_per_member: 0.05, max_size_boost: 0.2}\n"
        "overall_confidence: {invalid_cluster_penalty: 0.2, out_of_range_cluster_count_penalty: 0.1, optimal_cluster_count_min: 2, optimal_cluster_count_max: 6}\n",
        encoding="utf-8",
    )
    cluster_schema_loader._cluster_scoring_policy_cache = None
    monkeypatch.setattr(cluster_schema_loader, "_cluster_scoring_policy_path", lambda: bad)
    with pytest.raises(ValueError, match="strictly increasing"):
        cluster_schema_loader.load_cluster_scoring_policy()
