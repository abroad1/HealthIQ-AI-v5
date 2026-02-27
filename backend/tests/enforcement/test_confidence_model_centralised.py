"""
Sprint 8 - Enforcement: ConfidenceModel must be built only in confidence_builder.

No direct computation of system_confidence, cluster_confidence, missing_required
outside confidence_builder. Synthesis layer must not compute these.
"""

import pytest
from pathlib import Path


def test_build_confidence_model_only_in_confidence_builder():
    """build_confidence_model_v1 must only be defined in confidence_builder."""
    root = Path(__file__).parent.parent.parent
    builder_path = root / "core" / "analytics" / "confidence_builder.py"
    assert builder_path.exists()
    text = builder_path.read_text()
    assert "def build_confidence_model_v1" in text


def test_synthesis_does_not_compute_confidence_model():
    """Synthesis layer must not compute cluster_confidence or missing_required from schema."""
    path = Path(__file__).parent.parent.parent / "core" / "insights" / "synthesis.py"
    text = path.read_text()
    assert "compute_cluster_status" not in text, (
        "Sprint 8: Synthesis must not compute confidence from cluster schema"
    )


def test_confidence_builder_is_sole_source():
    """Only confidence_builder defines build_confidence_model_v1."""
    root = Path(__file__).parent.parent.parent / "core"
    builder_name = "confidence_builder.py"
    for py_path in root.rglob("*.py"):
        if py_path.name == builder_name:
            continue
        if "test" in str(py_path) or "conftest" in str(py_path):
            continue
        text = py_path.read_text(errors="ignore")
        if "def build_confidence_model_v1" in text:
            pytest.fail(
                f"Sprint 8: build_confidence_model_v1 must only exist in confidence_builder, found in {py_path}"
            )
