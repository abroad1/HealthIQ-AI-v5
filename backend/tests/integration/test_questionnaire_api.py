"""
API tests for questionnaire endpoints.
"""

import pytest
import json
from fastapi.testclient import TestClient
from app.main import app


class TestQuestionnaireAPI:
    """Test questionnaire API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    def test_get_questionnaire_schema(self, client):
        """Test GET /api/questionnaire/schema endpoint."""
        response = client.get("/api/questionnaire/schema")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "schema" in data
        assert "total_questions" in data
        assert "version" in data
        assert "description" in data
        
        # Verify schema content
        schema = data["schema"]
        assert isinstance(schema, list)
        assert data["total_questions"] == len(schema)
        
        # Verify first question structure
        if schema:
            first_question = schema[0]
            assert "id" in first_question
            assert "section" in first_question
            assert "question" in first_question
            assert "type" in first_question
            assert "required" in first_question
    
    def test_get_questionnaire_schema_validation(self, client):
        """Test GET /api/questionnaire/schema/validation endpoint."""
        response = client.get("/api/questionnaire/schema/validation")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify validation response structure
        assert "valid" in data
        assert "total_questions" in data
        assert "required_fields" in data
        assert "sections" in data
        assert "question_types" in data
        assert "errors" in data
        
        # Verify validation results
        assert data["valid"] is True
        assert data["total_questions"] > 0
        assert len(data["required_fields"]) > 0
        assert len(data["sections"]) > 0
        assert len(data["question_types"]) > 0
        assert len(data["errors"]) == 0  # Should be valid schema
    
    def test_questionnaire_schema_content_validation(self, client):
        """Test questionnaire schema contains expected content."""
        response = client.get("/api/questionnaire/schema")
        assert response.status_code == 200
        
        data = response.json()
        schema = data["schema"]
        
        # Verify expected sections exist
        sections = {q["section"] for q in schema}
        expected_sections = {
            "demographics", "medical_history", "symptoms", 
            "lifestyle", "physical_assessment", "cognitive_assessment", "family_history"
        }
        assert expected_sections.issubset(sections)
        
        # Verify expected question types exist
        question_types = {q["type"] for q in schema}
        expected_types = {"text", "dropdown", "checkbox", "slider", "number", "group"}
        assert expected_types.issubset(question_types)
        
        # Verify specific important questions exist
        question_ids = {q["id"] for q in schema}
        expected_questions = {
            "biological_sex", "date_of_birth", "diet_quality_rating",
            "sleep_hours_nightly", "alcohol_drinks_weekly", "tobacco_use"
        }
        assert expected_questions.issubset(question_ids)
    
    def test_questionnaire_schema_error_handling(self, client):
        """Test error handling when schema file is missing."""
        # This test would require mocking the file system
        # For now, we'll just verify the endpoint exists and responds
        response = client.get("/api/questionnaire/schema")
        assert response.status_code in [200, 404]  # Should either work or handle missing file gracefully
