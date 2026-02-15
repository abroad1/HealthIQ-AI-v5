"""
Sprint 8 - Unit tests for Confidence Model builder.
"""

import pytest
from core.contracts.confidence_model_v1 import ConfidenceModelV1, CONFIDENCE_MODEL_V1_VERSION
from core.analytics.confidence_builder import build_confidence_model_v1


def test_confidence_builder_basic():
    """Builder produces valid ConfidenceModel_v1."""
    m = build_confidence_model_v1(available_biomarkers={"glucose", "hba1c"})
    assert isinstance(m, ConfidenceModelV1)
    assert 0 <= m.system_confidence <= 1.0
    assert isinstance(m.cluster_confidence, dict)
    assert isinstance(m.biomarker_confidence, dict)
    assert isinstance(m.missing_required_biomarkers, list)
    assert isinstance(m.missing_required_clusters, list)


def test_missing_required_marker_reduces_cluster_confidence():
    """Missing required biomarker reduces cluster confidence."""
    full = build_confidence_model_v1(available_biomarkers={"glucose", "hba1c"})
    partial = build_confidence_model_v1(available_biomarkers={"glucose"})
    assert full.cluster_confidence.get("metabolic", 0) > partial.cluster_confidence.get("metabolic", 0)


def test_all_required_markers_present_cluster_confidence_1():
    """When all required markers present, cluster confidence is 1.0."""
    m = build_confidence_model_v1(available_biomarkers={"glucose", "hba1c"})
    assert m.cluster_confidence.get("metabolic") == 1.0


def test_confidence_model_version_stamp():
    """Model includes version stamp."""
    m = build_confidence_model_v1(available_biomarkers=set())
    assert m.model_version == CONFIDENCE_MODEL_V1_VERSION
    assert m.cluster_schema_version
    assert m.cluster_schema_hash


def test_deterministic_output_ordering():
    """missing_required_biomarkers and cluster_confidence keys are deterministically ordered."""
    m = build_confidence_model_v1(available_biomarkers={"glucose"})
    # missing_required_biomarkers should be sorted
    missing = m.missing_required_biomarkers
    assert missing == sorted(missing)
    # missing_required_clusters should be sorted
    clusters = m.missing_required_clusters
    assert clusters == sorted(clusters)
