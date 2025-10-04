"""
API tests for upload endpoints.
"""

import pytest
import json
from fastapi.testclient import TestClient
from app.main import app


class TestUploadAPI:
    """Test upload API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    def test_parse_upload_with_text(self, client):
        """Test POST /api/upload/parse with text content."""
        response = client.post(
            "/api/upload/parse",
            data={"text_content": "Sample lab report text content"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "success" in data
        assert "message" in data
        assert "parsed_data" in data
        assert "analysis_id" in data
        assert "timestamp" in data
        
        # Verify response content
        assert data["success"] is True
        assert "Mock parsing completed" in data["message"]
        assert "placeholder implementation" in data["message"]
        assert data["analysis_id"] is not None
        assert data["timestamp"] is not None
        
        # Verify parsed data structure
        parsed_data = data["parsed_data"]
        assert "biomarkers" in parsed_data
        assert "demographics" in parsed_data
        assert "questionnaire_responses" in parsed_data
        assert "metadata" in parsed_data
        
        # Verify biomarkers structure
        biomarkers = parsed_data["biomarkers"]
        assert "total_cholesterol" in biomarkers
        assert "hdl_cholesterol" in biomarkers
        assert "glucose" in biomarkers
        
        # Verify metadata
        metadata = parsed_data["metadata"]
        assert metadata["parsing_method"] == "mock_placeholder"
        assert metadata["confidence_score"] == 0.95
        assert metadata["source_type"] == "text_input"
    
    def test_parse_upload_with_file(self, client):
        """Test POST /api/upload/parse with file upload."""
        # Create a mock file
        files = {"file": ("test_report.pdf", b"mock pdf content", "application/pdf")}
        
        response = client.post("/api/upload/parse", files=files)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert data["success"] is True
        assert "Mock parsing completed" in data["message"]
        assert "file_upload" in data["message"]
        
        # Verify parsed data metadata indicates file source
        parsed_data = data["parsed_data"]
        metadata = parsed_data["metadata"]
        assert metadata["source_type"] == "lab_report"
    
    def test_parse_upload_without_input(self, client):
        """Test POST /api/upload/parse without any input."""
        response = client.post("/api/upload/parse")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should still return mock data even without input
        assert data["success"] is True
        assert data["parsed_data"] is not None
    
    def test_validate_upload_format_with_text(self, client):
        """Test POST /api/upload/validate with text content."""
        response = client.post(
            "/api/upload/validate",
            data={"text_content": "Sample text content for validation"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify validation response structure
        assert "valid" in data
        assert "supported_formats" in data
        assert "max_file_size_mb" in data
        assert "detected_format" in data
        assert "file_size_bytes" in data
        assert "warnings" in data
        assert "errors" in data
        
        # Verify validation results
        assert data["valid"] is True
        assert data["detected_format"] == "text/plain"
        assert data["file_size_bytes"] > 0
        assert len(data["errors"]) == 0
    
    def test_validate_upload_format_with_file(self, client):
        """Test POST /api/upload/validate with file upload."""
        files = {"file": ("test_report.pdf", b"mock pdf content", "application/pdf")}
        
        response = client.post("/api/upload/validate", files=files)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify validation results
        assert data["valid"] is True
        assert data["detected_format"] == "application/pdf"
        assert data["file_size_bytes"] > 0
        assert "pdf" in data["supported_formats"]
    
    def test_validate_upload_format_with_unsupported_file(self, client):
        """Test POST /api/upload/validate with unsupported file type."""
        files = {"file": ("test_file.exe", b"mock executable content", "application/x-executable")}
        
        response = client.post("/api/upload/validate", files=files)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should still be valid but with warnings
        assert data["valid"] is True
        assert len(data["warnings"]) > 0
        assert "may not be supported" in data["warnings"][0]
    
    def test_validate_upload_format_without_input(self, client):
        """Test POST /api/upload/validate without any input."""
        response = client.post("/api/upload/validate")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should be invalid without input
        assert data["valid"] is False
        assert len(data["errors"]) > 0
        assert "No file or text content provided" in data["errors"]
    
    def test_validate_upload_format_with_short_text(self, client):
        """Test POST /api/upload/validate with very short text."""
        response = client.post(
            "/api/upload/validate",
            data={"text_content": "Hi"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Should be invalid due to short text
        assert data["valid"] is False
        assert len(data["errors"]) > 0
        assert "Text content too short" in data["errors"]
    
    def test_upload_endpoints_error_handling(self, client):
        """Test error handling in upload endpoints."""
        # Test with malformed request
        response = client.post(
            "/api/upload/parse",
            data={"invalid_field": "invalid_value"}
        )
        
        # Should still work (mock implementation handles missing inputs gracefully)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
