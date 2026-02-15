"""
Sprint 6 - Prohibition test: no hardcoded cluster definitions in scoring/clustering.

Fails if legacy cluster hardcode patterns are found (required_biomarkers = [...],
health_system_mapping = {...}, cluster_ids = [...] with literal lists).
"""

import pytest
from pathlib import Path


def test_no_hardcoded_cluster_rules_in_rules_py():
    """rules.py must not contain hardcoded required_biomarkers lists from legacy."""
    path = Path(__file__).parent.parent.parent / "core" / "clustering" / "rules.py"
    text = path.read_text()
    # Legacy pattern: rule.required_biomarkers = ["glucose", "hba1c"]
    assert 'rule.required_biomarkers = ["glucose"' not in text, (
        "Sprint 6: Cluster definitions must come from ssot/clusters.yaml, not hardcoded rules"
    )


def test_no_hardcoded_health_system_mapping_in_engine_py():
    """engine.py must not contain hardcoded health_system_mapping dict."""
    path = Path(__file__).parent.parent.parent / "core" / "clustering" / "engine.py"
    text = path.read_text()
    assert '"metabolic": ["glucose"' not in text, (
        "Sprint 6: _group_biomarkers_by_health_system must use cluster schema, not hardcoded mapping"
    )


def test_no_hardcoded_cluster_ids_in_cluster_engine_v2():
    """cluster_engine_v2.py must not contain hardcoded cluster_ids list."""
    path = Path(__file__).parent.parent.parent / "core" / "clustering" / "cluster_engine_v2.py"
    text = path.read_text()
    # Legacy: cluster_ids = ["metabolic", "cardiovascular", "hepatic", ...]
    assert 'cluster_ids = [\n        "metabolic"' not in text, (
        "Sprint 6: cluster_ids must come from cluster schema, not hardcoded list"
    )
