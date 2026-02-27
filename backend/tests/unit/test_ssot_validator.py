"""
Unit tests for SSOT validator.
"""

import pytest
import yaml
import tempfile
from pathlib import Path

from core.analytics.system_burden_engine import ALLOWED_BURDEN_SYSTEM_IDS
from core.ssot.validate import ALLOWED_SYSTEMS, validate_biomarker, validate_ssot


def test_validate_biomarker_happy_path():
    """Test validation of a valid biomarker."""
    biomarker = {
        "system": "cardiovascular",
        "clusters": ["heart_health"],
        "roles": ["cholesterol_marker"],
        "key_risks_when_high": ["cardiovascular_disease"],
        "key_risks_when_low": [],
        "known_modifiers": ["fasting_state"],
        "clinical_weight": 0.8,
    }
    
    errors = validate_biomarker("test_biomarker", biomarker)
    assert len(errors) == 0


def test_validate_biomarker_missing_field():
    """Test validation fails when required field is missing."""
    biomarker = {
        "system": "cardiovascular",
        "clusters": [],
        # Missing: roles, key_risks_when_high, etc.
    }
    
    errors = validate_biomarker("test_biomarker", biomarker)
    assert len(errors) > 0
    assert any("missing required field" in e for e in errors)


def test_validate_biomarker_invalid_system():
    """Test validation fails for invalid system value."""
    biomarker = {
        "system": "invalid_system",
        "clusters": [],
        "roles": [],
        "key_risks_when_high": [],
        "key_risks_when_low": [],
        "known_modifiers": [],
        "clinical_weight": 0.8,
    }
    
    errors = validate_biomarker("test_biomarker", biomarker)
    assert len(errors) > 0
    assert any("system" in e and "must be one of" in e for e in errors)


def test_validate_biomarker_invalid_clinical_weight():
    """Test validation fails for clinical_weight outside [0, 1]."""
    biomarker = {
        "system": "cardiovascular",
        "clusters": [],
        "roles": [],
        "key_risks_when_high": [],
        "key_risks_when_low": [],
        "known_modifiers": [],
        "clinical_weight": 1.5,  # Invalid: > 1.0
    }
    
    errors = validate_biomarker("test_biomarker", biomarker)
    assert len(errors) > 0
    assert any("clinical_weight" in e and "[0, 1]" in e for e in errors)


def test_validate_ssot_happy_path():
    """Test validation of real SSOT file."""
    is_valid, errors, summary = validate_ssot()
    
    assert is_valid
    assert len(errors) == 0
    assert summary["total_biomarkers"] > 0
    assert summary["validated"] == summary["total_biomarkers"]


def test_validate_ssot_failing_fixture():
    """Test validation fails with incomplete fixture."""
    # Create a temporary YAML file with missing field
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump({
            "biomarkers": {
                "test_bio": {
                    "system": "cardiovascular",
                    "clusters": [],
                    # Missing required fields
                }
            }
        }, f)
        temp_path = Path(f.name)
    
    try:
        is_valid, errors, summary = validate_ssot(temp_path)
        
        assert not is_valid
        assert len(errors) > 0
    finally:
        temp_path.unlink()


def test_lifestyle_and_burden_system_namespaces_match():
    """
    SSOT integrity: lifestyle_registry system_caps must match system_burden allowlist.
    Ensures single consistent system namespace across lifestyle and burden registries.
    """
    ssot_root = Path(__file__).resolve().parent.parent.parent / "ssot"
    lifestyle_path = ssot_root / "lifestyle_registry.yaml"
    if not lifestyle_path.exists():
        pytest.skip("lifestyle_registry.yaml not found")
    lifestyle_data = yaml.safe_load(lifestyle_path.read_text(encoding="utf-8"))
    lifestyle_systems = set((lifestyle_data.get("system_caps") or {}).keys())
    burden_systems = set(ALLOWED_BURDEN_SYSTEM_IDS)
    assert lifestyle_systems == burden_systems, (
        f"System namespace mismatch: lifestyle has {sorted(lifestyle_systems - burden_systems)} not in burden; "
        f"burden has {sorted(burden_systems - lifestyle_systems)} not in lifestyle"
    )

