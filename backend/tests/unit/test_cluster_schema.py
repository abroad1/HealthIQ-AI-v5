"""
Sprint 6 - Unit tests for cluster schema loader and validator.

Schema validation: load success, invalid schema failures, cluster behaviour coverage.
"""

import pytest
from pathlib import Path

from core.analytics.cluster_schema import (
    load_cluster_schema,
    compute_cluster_status,
    get_cluster_schema_version_stamp,
    ClusterSchema,
)


class TestClusterSchemaLoad:
    """Tests for cluster schema loading."""

    def test_clusters_yaml_loads_successfully(self):
        """clusters.yaml loads successfully."""
        schema = load_cluster_schema()
        assert schema is not None
        assert isinstance(schema, ClusterSchema)
        assert schema.version
        assert schema.schema_version
        assert schema.schema_hash
        assert len(schema.clusters) >= 6

    def test_cluster_schema_version_stamp(self):
        """get_cluster_schema_version_stamp returns version and hash."""
        stamp = get_cluster_schema_version_stamp()
        assert "cluster_schema_version" in stamp
        assert "cluster_schema_hash" in stamp
        assert isinstance(stamp["cluster_schema_version"], str)
        assert isinstance(stamp["cluster_schema_hash"], str)


class TestClusterSchemaValidation:
    """Tests for schema validation (invalid schema must fail)."""

    def test_validate_unknown_biomarker_via_direct_call(self):
        """_validate_cluster with unknown biomarker ID raises ValueError."""
        from core.analytics.cluster_schema import _validate_cluster
        canonical = {"glucose", "hba1c"}
        raw = {
            "cluster_id": "test",
            "description": "Test",
            "biomarker_membership": {
                "required": ["glucose", "nonexistent_xyz"],
                "important": [],
                "optional": [],
            },
        }
        with pytest.raises(ValueError, match="unknown biomarker"):
            _validate_cluster("test", raw, canonical)

    def test_validate_duplicate_biomarker_raises(self):
        """Duplicate biomarker across required/important/optional raises ValueError."""
        from core.analytics.cluster_schema import _validate_cluster
        canonical = {"glucose", "hba1c"}
        raw = {
            "cluster_id": "test",
            "description": "Test",
            "biomarker_membership": {
                "required": ["glucose"],
                "important": ["glucose"],  # duplicate
                "optional": [],
            },
        }
        with pytest.raises(ValueError, match="duplicate"):
            _validate_cluster("test", raw, canonical)

    def test_validate_empty_cluster_raises(self):
        """Empty cluster (no biomarkers) raises ValueError."""
        from core.analytics.cluster_schema import _validate_cluster
        canonical = {"glucose"}
        raw = {
            "cluster_id": "empty",
            "description": "Empty",
            "biomarker_membership": {"required": [], "important": [], "optional": []},
        }
        with pytest.raises(ValueError, match="empty cluster"):
            _validate_cluster("empty", raw, canonical)


class TestClusterBehaviour:
    """Tests for cluster status behaviour (required missing vs complete)."""

    def test_metabolic_required_missing_reflects_incomplete(self):
        """Metabolic cluster: missing required glucose -> incomplete."""
        schema = load_cluster_schema()
        metabolic = schema.clusters.get("metabolic")
        if not metabolic:
            pytest.skip("No metabolic cluster in schema")
        # Only hba1c present, glucose missing
        status = compute_cluster_status(metabolic, {"hba1c"})
        assert not status["complete"]
        assert "glucose" in status["required_missing"]

    def test_metabolic_all_required_present_complete(self):
        """Metabolic cluster: glucose + hba1c present -> complete."""
        schema = load_cluster_schema()
        metabolic = schema.clusters.get("metabolic")
        if not metabolic:
            pytest.skip("No metabolic cluster in schema")
        status = compute_cluster_status(metabolic, {"glucose", "hba1c"})
        assert status["complete"]
        assert len(status["required_missing"]) == 0

    def test_cardiovascular_required_missing(self):
        """Cardiovascular: missing ldl_cholesterol -> incomplete."""
        schema = load_cluster_schema()
        cardio = schema.clusters.get("cardiovascular")
        if not cardio:
            pytest.skip("No cardiovascular cluster in schema")
        status = compute_cluster_status(cardio, {"total_cholesterol"})
        assert not status["complete"]
        assert "ldl_cholesterol" in status["required_missing"]

    def test_inflammatory_single_required_complete(self):
        """Inflammatory: crp alone -> complete."""
        schema = load_cluster_schema()
        infl = schema.clusters.get("inflammatory")
        if not infl:
            pytest.skip("No inflammatory cluster in schema")
        status = compute_cluster_status(infl, {"crp"})
        assert status["complete"]
