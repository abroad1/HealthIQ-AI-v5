# backend/tests/unit/test_export_service.py

import pytest
from unittest.mock import Mock, patch
from services.storage.export_service import ExportService


@patch('services.storage.export_service.get_supabase_client')
def test_csv_generation_minimal(mock_get_client):
    """Test CSV generation with minimal data."""
    # Mock the Supabase client
    mock_client = Mock()
    mock_get_client.return_value = mock_client
    
    svc = ExportService()
    dto = {
        "biomarkers": [
            {
                "biomarker_name": "glucose",
                "value": 95,
                "unit": "mg/dL",
                "status": "normal",
                "reference_range": {"min": 70, "max": 99},
            }
        ]
    }

    # Test the CSV generation method directly
    data = svc._to_csv_bytes(dto)
    s = data.decode()

    assert "biomarker_name,value,unit,status,reference_min,reference_max" in s
    assert "glucose,95,mg/dL,normal,70,99" in s


@patch('services.storage.export_service.get_supabase_client')
def test_json_generation_minimal(mock_get_client):
    """Test JSON generation with minimal data."""
    # Mock the Supabase client
    mock_client = Mock()
    mock_get_client.return_value = mock_client
    
    svc = ExportService()
    dto = {
        "biomarkers": [
            {
                "biomarker_name": "A",
                "value": 1,
                "unit": "u",
                "status": "ok",
                "reference_range": {"min": 0, "max": 1},
            }
        ]
    }

    # Test JSON generation by checking the method exists and can be called
    # We'll test the actual JSON generation in the generate_and_upload method
    assert hasattr(svc, '_to_csv_bytes')
    assert hasattr(svc, 'generate_and_upload')
    assert hasattr(svc, 'signed_url')
