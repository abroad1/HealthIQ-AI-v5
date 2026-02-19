"""
Sprint 9 - Unit tests for Replay Manifest.
"""

import json
import pytest
from core.contracts.replay_manifest_v1 import ReplayManifestV1, REPLAY_MANIFEST_V1_VERSION
from core.contracts.insight_graph_v1 import InsightGraphV1, BiomarkerNode
from core.contracts.confidence_model_v1 import ConfidenceModelV1
from core.analytics.replay_manifest_builder import build_replay_manifest_v1, _canonical_json_hash

_FORBIDDEN_KEYS = {"timestamp", "date", "uuid", "env", "created_at", "updated_at"}


def test_build_twice_yields_identical_json():
    """Given fixed fixture, building manifest twice yields identical manifest JSON."""
    ig = InsightGraphV1(
        graph_version="1.0.0",
        analysis_id="t",
        biomarker_nodes=[BiomarkerNode(biomarker_id="x", status="normal")],
        edges=[],
    )
    conf = ConfidenceModelV1(
        model_version="1.0.0",
        system_confidence=0.5,
        cluster_confidence={"a": 1.0},
        biomarker_confidence={"x": 1.0},
        missing_required_biomarkers=[],
        missing_required_clusters=[],
    )
    m1 = build_replay_manifest_v1(
        unit_registry_version="1.0",
        ratio_registry_version="1.1.0",
        cluster_schema_version="1.0.0",
        cluster_schema_hash="abc123",
        insight_graph=ig,
        confidence_model=conf,
    )
    m2 = build_replay_manifest_v1(
        unit_registry_version="1.0",
        ratio_registry_version="1.1.0",
        cluster_schema_version="1.0.0",
        cluster_schema_hash="abc123",
        insight_graph=ig,
        confidence_model=conf,
    )
    j1 = json.dumps(m1.model_dump(), sort_keys=True, default=str)
    j2 = json.dumps(m2.model_dump(), sort_keys=True, default=str)
    assert j1 == j2


def test_hashes_are_stable():
    """Hashes are deterministic for same input."""
    ig = InsightGraphV1(
        graph_version="1.0.0",
        analysis_id="t",
        biomarker_nodes=[BiomarkerNode(biomarker_id="x", status="normal")],
        edges=[],
    )
    m = build_replay_manifest_v1(
        unit_registry_version="1.0",
        ratio_registry_version="1.1.0",
        cluster_schema_version="1.0.0",
        cluster_schema_hash="abc",
        insight_graph=ig,
        confidence_model=None,
    )
    assert "insight_graph_hash" in m.schema_hashes
    h = m.schema_hashes["insight_graph_hash"]
    assert len(h) == 64  # SHA-256 hex
    assert all(c in "0123456789abcdef" for c in h)


def test_no_forbidden_keys_in_manifest():
    """Manifest contains no timestamp, date, uuid, env."""
    m = build_replay_manifest_v1(
        unit_registry_version="1.0",
        ratio_registry_version="1.1.0",
        cluster_schema_version="1.0.0",
        cluster_schema_hash="x",
        insight_graph=None,
        confidence_model=None,
    )
    d = m.model_dump()
    keys_lower = [k.lower() for k in d.keys()]
    for forbidden in _FORBIDDEN_KEYS:
        assert forbidden not in keys_lower, f"Forbidden key {forbidden} found"
    # Recursively check schema_hashes and any nested dicts
    def check_no_forbidden(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k.lower() in _FORBIDDEN_KEYS:
                    pytest.fail(f"Forbidden key '{k}' at {path}")
                check_no_forbidden(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                check_no_forbidden(v, f"{path}[{i}]")
    check_no_forbidden(d)


def test_version_stamp_present():
    """Manifest includes manifest_version."""
    m = build_replay_manifest_v1(
        unit_registry_version="1.0",
        ratio_registry_version="1.1.0",
        cluster_schema_version="1.0.0",
        cluster_schema_hash="x",
    )
    assert m.manifest_version == REPLAY_MANIFEST_V1_VERSION


def test_relationship_registry_stamp_in_manifest():
    """Manifest carries relationship registry version/hash for replay stamping."""
    m = build_replay_manifest_v1(
        unit_registry_version="1.0",
        ratio_registry_version="1.1.0",
        cluster_schema_version="1.0.0",
        cluster_schema_hash="x",
        relationship_registry_version="1.0.0",
        relationship_registry_hash="abc123",
    )
    assert m.relationship_registry_version == "1.0.0"
    assert m.relationship_registry_hash == "abc123"


def test_biomarker_context_stamp_in_manifest():
    """Manifest carries biomarker context version/hash for replay stamping."""
    m = build_replay_manifest_v1(
        unit_registry_version="1.0",
        ratio_registry_version="1.1.0",
        cluster_schema_version="1.0.0",
        cluster_schema_hash="x",
        biomarker_context_version="1.0.0",
        biomarker_context_hash="ctxhash123",
    )
    assert m.biomarker_context_version == "1.0.0"
    assert m.biomarker_context_hash == "ctxhash123"


def test_scoring_policy_stamp_in_manifest():
    """Manifest carries scoring policy version/hash for replay stamping."""
    m = build_replay_manifest_v1(
        unit_registry_version="1.0",
        ratio_registry_version="1.1.0",
        cluster_schema_version="1.0.0",
        cluster_schema_hash="x",
        scoring_policy_version="1.0.0",
        scoring_policy_hash="policyhash123",
    )
    assert m.scoring_policy_version == "1.0.0"
    assert m.scoring_policy_hash == "policyhash123"


def test_evidence_registry_stamp_in_manifest():
    """Manifest carries evidence registry version/hash for replay stamping."""
    m = build_replay_manifest_v1(
        unit_registry_version="1.0",
        ratio_registry_version="1.1.0",
        cluster_schema_version="1.0.0",
        cluster_schema_hash="x",
        evidence_registry_version="1.0.0",
        evidence_registry_hash="evidencehash123",
    )
    assert m.evidence_registry_version == "1.0.0"
    assert m.evidence_registry_hash == "evidencehash123"


def test_state_transition_stamp_and_linked_snapshot_ids_in_manifest():
    """Manifest carries state transition stamp and linked snapshot IDs."""
    m = build_replay_manifest_v1(
        unit_registry_version="1.0",
        ratio_registry_version="1.1.0",
        cluster_schema_version="1.0.0",
        cluster_schema_hash="x",
        state_transition_version="1.0.0",
        state_transition_hash="statehash123",
        linked_snapshot_ids=["a-1", "a-2"],
    )
    assert m.state_transition_version == "1.0.0"
    assert m.state_transition_hash == "statehash123"
    assert m.linked_snapshot_ids == ["a-1", "a-2"]


def test_state_engine_stamp_in_manifest():
    """Manifest carries state engine version/hash for replay stamping."""
    m = build_replay_manifest_v1(
        unit_registry_version="1.0",
        ratio_registry_version="1.1.0",
        cluster_schema_version="1.0.0",
        cluster_schema_hash="x",
        state_engine_version="1.0.0",
        state_engine_hash="enginehash123",
    )
    assert m.state_engine_version == "1.0.0"
    assert m.state_engine_hash == "enginehash123"


def test_state_engine_stamp_deterministic_across_runs():
    """State engine fields remain deterministic across repeated builds."""
    kwargs = dict(
        unit_registry_version="1.0",
        ratio_registry_version="1.1.0",
        cluster_schema_version="1.0.0",
        cluster_schema_hash="x",
        state_engine_version="1.0.0",
        state_engine_hash="enginehash123",
    )
    m1 = build_replay_manifest_v1(**kwargs)
    m2 = build_replay_manifest_v1(**kwargs)
    assert m1.state_engine_version == m2.state_engine_version
    assert m1.state_engine_hash == m2.state_engine_hash


def test_replay_manifest_builder_fails_loud_on_unserialisable_insight_graph(monkeypatch):
    """Production mode: replay stamp assembly must fail loudly."""
    monkeypatch.delenv("HEALTHIQ_MODE", raising=False)

    class BadInsightGraph:
        def model_dump(self):
            raise RuntimeError("boom")

    with pytest.raises(ValueError, match="Replay manifest build failed for insight_graph"):
        build_replay_manifest_v1(
            unit_registry_version="1.0",
            ratio_registry_version="1.1.0",
            cluster_schema_version="1.0.0",
            cluster_schema_hash="x",
            insight_graph=BadInsightGraph(),
        )


def test_replay_manifest_builder_fixture_mode_allows_soft_fail(monkeypatch):
    """Fixture mode: allow replay stamp soft-fail for fixture generation paths."""
    monkeypatch.setenv("HEALTHIQ_MODE", "fixture")

    class BadConfidenceModel:
        def model_dump(self):
            raise RuntimeError("boom")

    m = build_replay_manifest_v1(
        unit_registry_version="1.0",
        ratio_registry_version="1.1.0",
        cluster_schema_version="1.0.0",
        cluster_schema_hash="x",
        confidence_model=BadConfidenceModel(),
    )
    assert m.confidence_model_version == ""
