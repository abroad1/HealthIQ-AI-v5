"""
Unit tests for LLM response parsing.
"""

import pytest
import json
from unittest.mock import Mock

from core.llm.parsing import ResponseParser, ParsedResponse, ParseError, ValidationError
from core.llm.client import GeminiResponse


class TestResponseParser:
    """Test cases for ResponseParser."""
    
    def test_init(self):
        """Test parser initialization."""
        parser = ResponseParser()
        assert parser is not None
    
    def test_parse_json_response_success(self):
        """Test successful JSON parsing."""
        response = GeminiResponse(
            content='{"result": "success", "data": [1, 2, 3]}',
            model="gemini-pro",
            usage={"promptTokenCount": 10, "candidatesTokenCount": 5},
            success=True
        )
        
        parser = ResponseParser()
        result = parser.parse_json_response(response)
        
        assert result.success is True
        assert result.data == {"result": "success", "data": [1, 2, 3]}
        assert result.confidence == 0.9
        assert result.error is None
    
    def test_parse_json_response_with_markdown(self):
        """Test JSON parsing with markdown code blocks."""
        response = GeminiResponse(
            content='```json\n{"result": "success"}\n```',
            model="gemini-pro",
            usage={"promptTokenCount": 10, "candidatesTokenCount": 5},
            success=True
        )
        
        parser = ResponseParser()
        result = parser.parse_json_response(response)
        
        assert result.success is True
        assert result.data == {"result": "success"}
    
    def test_parse_json_response_failed_response(self):
        """Test parsing failed response."""
        response = GeminiResponse(
            content="",
            model="gemini-pro",
            usage={},
            success=False,
            error="API error"
        )
        
        parser = ResponseParser()
        result = parser.parse_json_response(response)
        
        assert result.success is False
        assert result.error == "API error"
        assert result.data == {}
    
    def test_parse_json_response_invalid_json(self):
        """Test parsing invalid JSON."""
        response = GeminiResponse(
            content="invalid json content",
            model="gemini-pro",
            usage={"promptTokenCount": 10, "candidatesTokenCount": 5},
            success=True
        )
        
        parser = ResponseParser()
        result = parser.parse_json_response(response)
        
        assert result.success is False
        assert "Failed to parse JSON" in result.error
        assert result.data == {}
    
    def test_validate_biomarker_parsing_response_valid(self):
        """Test valid biomarker parsing response."""
        valid_data = {
            "biomarkers": {
                "glucose": {
                    "value": 95.0,
                    "unit": "mg/dL",
                    "confidence": 0.9
                },
                "cholesterol": {
                    "value": 180.0,
                    "unit": "mg/dL",
                    "confidence": 0.8
                }
            },
            "extraction_notes": "Successfully extracted biomarkers",
            "confidence_score": 0.85
        }
        
        parser = ResponseParser()
        result = parser.validate_biomarker_parsing_response(valid_data)
        
        assert result is True
    
    def test_validate_biomarker_parsing_response_missing_fields(self):
        """Test biomarker parsing response with missing fields."""
        invalid_data = {
            "biomarkers": {
                "glucose": {
                    "value": 95.0,
                    "unit": "mg/dL"
                    # Missing confidence
                }
            },
            "extraction_notes": "Test notes"
            # Missing confidence_score
        }
        
        parser = ResponseParser()
        result = parser.validate_biomarker_parsing_response(invalid_data)
        
        assert result is False
    
    def test_validate_biomarker_parsing_response_invalid_biomarker_data(self):
        """Test biomarker parsing response with invalid biomarker data."""
        invalid_data = {
            "biomarkers": {
                "glucose": "invalid_data"  # Should be dict
            },
            "extraction_notes": "Test notes",
            "confidence_score": 0.85
        }
        
        parser = ResponseParser()
        result = parser.validate_biomarker_parsing_response(invalid_data)
        
        assert result is False
    
    def test_validate_biomarker_parsing_response_invalid_confidence(self):
        """Test biomarker parsing response with invalid confidence."""
        invalid_data = {
            "biomarkers": {
                "glucose": {
                    "value": 95.0,
                    "unit": "mg/dL",
                    "confidence": 1.5  # Invalid confidence > 1
                }
            },
            "extraction_notes": "Test notes",
            "confidence_score": 0.85
        }
        
        parser = ResponseParser()
        result = parser.validate_biomarker_parsing_response(invalid_data)
        
        assert result is False
    
    def test_validate_insight_synthesis_response_valid(self):
        """Test valid insight synthesis response."""
        valid_data = {
            "insights": [
                {
                    "category": "metabolic",
                    "title": "Glucose Control",
                    "description": "Good glucose control",
                    "severity": "low",
                    "confidence": 0.9,
                    "evidence": ["Normal glucose levels"],
                    "recommendations": ["Continue current diet"]
                }
            ],
            "overall_assessment": "Good overall health",
            "key_findings": ["Normal biomarkers"],
            "next_steps": ["Continue monitoring"]
        }
        
        parser = ResponseParser()
        result = parser.validate_insight_synthesis_response(valid_data)
        
        assert result is True
    
    def test_validate_insight_synthesis_response_invalid_severity(self):
        """Test insight synthesis response with invalid severity."""
        invalid_data = {
            "insights": [
                {
                    "category": "metabolic",
                    "title": "Glucose Control",
                    "description": "Good glucose control",
                    "severity": "invalid",  # Invalid severity
                    "confidence": 0.9,
                    "evidence": ["Normal glucose levels"],
                    "recommendations": ["Continue current diet"]
                }
            ],
            "overall_assessment": "Good overall health",
            "key_findings": ["Normal biomarkers"],
            "next_steps": ["Continue monitoring"]
        }
        
        parser = ResponseParser()
        result = parser.validate_insight_synthesis_response(invalid_data)
        
        assert result is False
    
    def test_validate_narrative_response_valid(self):
        """Test valid narrative response."""
        valid_data = {
            "executive_summary": "Good health overall",
            "detailed_analysis": "Detailed analysis here",
            "key_recommendations": ["Eat well", "Exercise"],
            "positive_findings": ["Normal glucose"],
            "areas_for_improvement": ["Cholesterol"],
            "next_steps": ["Monitor progress"]
        }
        
        parser = ResponseParser()
        result = parser.validate_narrative_response(valid_data)
        
        assert result is True
    
    def test_validate_narrative_response_invalid_types(self):
        """Test narrative response with invalid types."""
        invalid_data = {
            "executive_summary": "Good health overall",
            "detailed_analysis": "Detailed analysis here",
            "key_recommendations": "Not a list",  # Should be list
            "positive_findings": ["Normal glucose"],
            "areas_for_improvement": ["Cholesterol"],
            "next_steps": ["Monitor progress"]
        }
        
        parser = ResponseParser()
        result = parser.validate_narrative_response(invalid_data)
        
        assert result is False
    
    def test_validate_recommendation_response_valid(self):
        """Test valid recommendation response."""
        valid_data = {
            "nutrition_recommendations": ["Eat more vegetables"],
            "exercise_recommendations": ["Walk daily"],
            "lifestyle_recommendations": ["Get more sleep"],
            "supplement_recommendations": ["Vitamin D"],
            "monitoring_recommendations": ["Check glucose"],
            "priority_actions": ["Start exercise"],
            "timeline": {
                "immediate": ["Start today"],
                "short_term": ["This week"],
                "long_term": ["This month"]
            }
        }
        
        parser = ResponseParser()
        result = parser.validate_recommendation_response(valid_data)
        
        assert result is True
    
    def test_validate_recommendation_response_invalid_timeline(self):
        """Test recommendation response with invalid timeline."""
        invalid_data = {
            "nutrition_recommendations": ["Eat more vegetables"],
            "exercise_recommendations": ["Walk daily"],
            "lifestyle_recommendations": ["Get more sleep"],
            "supplement_recommendations": ["Vitamin D"],
            "monitoring_recommendations": ["Check glucose"],
            "priority_actions": ["Start exercise"],
            "timeline": {
                "immediate": "Not a list",  # Should be list
                "short_term": ["This week"],
                "long_term": ["This month"]
            }
        }
        
        parser = ResponseParser()
        result = parser.validate_recommendation_response(invalid_data)
        
        assert result is False
    
    def test_parse_and_validate_biomarker_parsing_success(self):
        """Test successful parse and validate for biomarker parsing."""
        response = GeminiResponse(
            content=json.dumps({
                "biomarkers": {
                    "glucose": {
                        "value": 95.0,
                        "unit": "mg/dL",
                        "confidence": 0.9
                    }
                },
                "extraction_notes": "Successfully extracted",
                "confidence_score": 0.85
            }),
            model="gemini-pro",
            usage={"promptTokenCount": 10, "candidatesTokenCount": 5},
            success=True
        )
        
        parser = ResponseParser()
        result = parser.parse_and_validate(response, "biomarker_parsing")
        
        assert result.success is True
        assert "biomarkers" in result.data
        assert result.confidence == 0.9
    
    def test_parse_and_validate_biomarker_parsing_validation_failure(self):
        """Test parse and validate with validation failure."""
        response = GeminiResponse(
            content=json.dumps({
                "biomarkers": {
                    "glucose": {
                        "value": 95.0,
                        "unit": "mg/dL"
                        # Missing confidence
                    }
                },
                "extraction_notes": "Successfully extracted",
                "confidence_score": 0.85
            }),
            model="gemini-pro",
            usage={"promptTokenCount": 10, "candidatesTokenCount": 5},
            success=True
        )
        
        parser = ResponseParser()
        result = parser.parse_and_validate(response, "biomarker_parsing")
        
        assert result.success is False
        assert "Validation failed" in result.error
        assert result.confidence == 0.0
    
    def test_parse_and_validate_unknown_type(self):
        """Test parse and validate with unknown response type."""
        response = GeminiResponse(
            content='{"result": "success"}',
            model="gemini-pro",
            usage={"promptTokenCount": 10, "candidatesTokenCount": 5},
            success=True
        )
        
        parser = ResponseParser()
        result = parser.parse_and_validate(response, "unknown_type")
        
        # Should succeed since no validation is performed for unknown types
        assert result.success is True
        assert result.data == {"result": "success"}
