"""
Integration test for upload pipeline with SSOT metadata.
"""

import pytest
from fastapi.testclient import TestClient
import importlib


def load_app():
    """Load FastAPI app."""
    for mod in ("backend.app.main", "app.main"):
        try:
            return getattr(importlib.import_module(mod), "app")
        except Exception:
            continue
    raise SystemExit("FastAPI app not found")


def test_upload_parse_includes_ssot_metadata():
    """Test that upload parse response includes SSOT metadata in biomarkers."""
    app = load_app()
    client = TestClient(app)
    
    # Use the two-line sample
    response = client.post(
        "/api/upload/parse",
        data={"text_content": "ALT,42,U/L\nHDL,1.0,mmol/L"}
    )
    
    assert response.status_code == 200
    body = response.json()
    
    assert "parsed_data" in body
    assert "biomarkers" in body["parsed_data"]
    assert len(body["parsed_data"]["biomarkers"]) >= 1
    
    # Check first biomarker has SSOT metadata
    first_biomarker = body["parsed_data"]["biomarkers"][0]
    assert "ssot" in first_biomarker
    
    ssot = first_biomarker["ssot"]
    assert "system" in ssot
    assert "clusters" in ssot
    assert "roles" in ssot
    assert "clinical_weight" in ssot
    
    # Validate types
    assert isinstance(ssot["system"], str)
    assert isinstance(ssot["clusters"], list)
    assert isinstance(ssot["roles"], list)
    assert isinstance(ssot["clinical_weight"], (int, float))

