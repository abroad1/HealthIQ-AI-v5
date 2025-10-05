"""
Integration tests for LLM biomarker parsing with status classification.
"""

import pytest
import json
from unittest.mock import Mock, patch
from services.parsing.llm_parser import LLMParser


class TestLLMBiomarkerParsing:
    """Test cases for LLM biomarker parsing with status classification."""
    
    @pytest.fixture
    def parser(self):
        """Create LLM parser instance for testing."""
        return LLMParser()
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_biomarker_status_classification_low(self, parser):
        """Test biomarker status classification for low values."""
        # Mock Gemini response with low value
        mock_response = {
            'text': json.dumps({
                "biomarkers": [
                    {
                        "id": "glucose",
                        "name": "Glucose",
                        "value": 65.0,
                        "unit": "mg/dL",
                        "reference": "70-100 mg/dL",
                        "confidence": 0.9,
                        "ref_low": 70.0,
                        "ref_high": 100.0
                    }
                ]
            }),
            'tokens_used': 100,
            'latency_ms': 500
        }
        
        with patch.object(parser.gemini_client, 'generate', return_value=mock_response):
            result = await parser.extract_biomarkers(
                file_bytes=b"test content",
                filename="test.txt",
                content_type="text/plain"
            )
        
        assert result["biomarkers"][0]["healthStatus"] == "Low"
        assert result["biomarkers"][0]["value"] == 65.0
        assert result["biomarkers"][0]["ref_low"] == 70.0
        assert result["biomarkers"][0]["ref_high"] == 100.0
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_biomarker_status_classification_high(self, parser):
        """Test biomarker status classification for high values."""
        # Mock Gemini response with high value
        mock_response = {
            'text': json.dumps({
                "biomarkers": [
                    {
                        "id": "cholesterol",
                        "name": "Total Cholesterol",
                        "value": 250.0,
                        "unit": "mg/dL",
                        "reference": "< 200 mg/dL",
                        "confidence": 0.9,
                        "ref_low": None,
                        "ref_high": 200.0
                    }
                ]
            }),
            'tokens_used': 100,
            'latency_ms': 500
        }
        
        with patch.object(parser.gemini_client, 'generate', return_value=mock_response):
            result = await parser.extract_biomarkers(
                file_bytes=b"test content",
                filename="test.txt",
                content_type="text/plain"
            )
        
        assert result["biomarkers"][0]["healthStatus"] == "High"
        assert result["biomarkers"][0]["value"] == 250.0
        assert result["biomarkers"][0]["ref_high"] == 200.0
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_biomarker_status_classification_normal(self, parser):
        """Test biomarker status classification for normal values."""
        # Mock Gemini response with normal value
        mock_response = {
            'text': json.dumps({
                "biomarkers": [
                    {
                        "id": "glucose",
                        "name": "Glucose",
                        "value": 85.0,
                        "unit": "mg/dL",
                        "reference": "70-100 mg/dL",
                        "confidence": 0.9,
                        "ref_low": 70.0,
                        "ref_high": 100.0
                    }
                ]
            }),
            'tokens_used': 100,
            'latency_ms': 500
        }
        
        with patch.object(parser.gemini_client, 'generate', return_value=mock_response):
            result = await parser.extract_biomarkers(
                file_bytes=b"test content",
                filename="test.txt",
                content_type="text/plain"
            )
        
        assert result["biomarkers"][0]["healthStatus"] == "Normal"
        assert result["biomarkers"][0]["value"] == 85.0
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_biomarker_status_classification_unknown(self, parser):
        """Test biomarker status classification for missing reference ranges."""
        # Mock Gemini response with valid value but missing reference ranges
        mock_response = {
            'text': json.dumps({
                "biomarkers": [
                    {
                        "id": "glucose",
                        "name": "Glucose",
                        "value": 85.0,
                        "unit": "mg/dL",
                        "reference": "Normal range",
                        "confidence": 0.9,
                        "ref_low": None,
                        "ref_high": None
                    }
                ]
            }),
            'tokens_used': 100,
            'latency_ms': 500
        }
        
        with patch.object(parser.gemini_client, 'generate', return_value=mock_response):
            result = await parser.extract_biomarkers(
                file_bytes=b"test content",
                filename="test.txt",
                content_type="text/plain"
            )
        
        assert result["biomarkers"][0]["healthStatus"] == "Normal"
        assert result["biomarkers"][0]["value"] == 85.0
        assert result["biomarkers"][0]["ref_low"] is None
        assert result["biomarkers"][0]["ref_high"] is None
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_biomarker_status_classification_conversion_error(self, parser):
        """Test biomarker status classification when value conversion fails."""
        # Mock Gemini response with value that will cause conversion error
        mock_response = {
            'text': json.dumps({
                "biomarkers": [
                    {
                        "id": "glucose",
                        "name": "Glucose",
                        "value": "invalid_value",
                        "unit": "mg/dL",
                        "reference": "70-100 mg/dL",
                        "confidence": 0.9,
                        "ref_low": 70.0,
                        "ref_high": 100.0
                    }
                ]
            }),
            'tokens_used': 100,
            'latency_ms': 500
        }
        
        with patch.object(parser.gemini_client, 'generate', return_value=mock_response):
            result = await parser.extract_biomarkers(
                file_bytes=b"test content",
                filename="test.txt",
                content_type="text/plain"
            )
        
        # The biomarker should be filtered out due to invalid value
        assert len(result["biomarkers"]) == 0
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_biomarker_status_classification_missing_reference_ranges(self, parser):
        """Test biomarker status classification with missing reference ranges."""
        # Mock Gemini response with missing reference ranges
        mock_response = {
            'text': json.dumps({
                "biomarkers": [
                    {
                        "id": "glucose",
                        "name": "Glucose",
                        "value": 85.0,
                        "unit": "mg/dL",
                        "reference": "Normal range",
                        "confidence": 0.9,
                        "ref_low": None,
                        "ref_high": None
                    }
                ]
            }),
            'tokens_used': 100,
            'latency_ms': 500
        }
        
        with patch.object(parser.gemini_client, 'generate', return_value=mock_response):
            result = await parser.extract_biomarkers(
                file_bytes=b"test content",
                filename="test.txt",
                content_type="text/plain"
            )
        
        assert result["biomarkers"][0]["healthStatus"] == "Normal"
        assert result["biomarkers"][0]["value"] == 85.0
        assert result["biomarkers"][0]["ref_low"] is None
        assert result["biomarkers"][0]["ref_high"] is None
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_biomarker_status_classification_multiple_biomarkers(self, parser):
        """Test biomarker status classification with multiple biomarkers."""
        # Mock Gemini response with multiple biomarkers
        mock_response = {
            'text': json.dumps({
                "biomarkers": [
                    {
                        "id": "glucose",
                        "name": "Glucose",
                        "value": 65.0,
                        "unit": "mg/dL",
                        "reference": "70-100 mg/dL",
                        "confidence": 0.9,
                        "ref_low": 70.0,
                        "ref_high": 100.0
                    },
                    {
                        "id": "cholesterol",
                        "name": "Total Cholesterol",
                        "value": 250.0,
                        "unit": "mg/dL",
                        "reference": "< 200 mg/dL",
                        "confidence": 0.8,
                        "ref_low": None,
                        "ref_high": 200.0
                    },
                    {
                        "id": "hdl",
                        "name": "HDL Cholesterol",
                        "value": 55.0,
                        "unit": "mg/dL",
                        "reference": "> 40 mg/dL",
                        "confidence": 0.9,
                        "ref_low": 40.0,
                        "ref_high": None
                    }
                ]
            }),
            'tokens_used': 150,
            'latency_ms': 750
        }
        
        with patch.object(parser.gemini_client, 'generate', return_value=mock_response):
            result = await parser.extract_biomarkers(
                file_bytes=b"test content",
                filename="test.txt",
                content_type="text/plain"
            )
        
        # Verify all biomarkers have status classification
        assert len(result["biomarkers"]) == 3
        
        # Check individual status classifications
        glucose = next(b for b in result["biomarkers"] if b["id"] == "glucose")
        assert glucose["healthStatus"] == "Low"
        
        cholesterol = next(b for b in result["biomarkers"] if b["id"] == "cholesterol")
        assert cholesterol["healthStatus"] == "High"
        
        hdl = next(b for b in result["biomarkers"] if b["id"] == "hdl")
        assert hdl["healthStatus"] == "Normal"
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_biomarker_status_classification_edge_cases(self, parser):
        """Test biomarker status classification edge cases."""
        # Mock Gemini response with edge case values
        mock_response = {
            'text': json.dumps({
                "biomarkers": [
                    {
                        "id": "glucose",
                        "name": "Glucose",
                        "value": 70.0,  # Exactly at lower bound
                        "unit": "mg/dL",
                        "reference": "70-100 mg/dL",
                        "confidence": 0.9,
                        "ref_low": 70.0,
                        "ref_high": 100.0
                    },
                    {
                        "id": "cholesterol",
                        "name": "Total Cholesterol",
                        "value": 100.0,  # Exactly at upper bound
                        "unit": "mg/dL",
                        "reference": "70-100 mg/dL",
                        "confidence": 0.9,
                        "ref_low": 70.0,
                        "ref_high": 100.0
                    }
                ]
            }),
            'tokens_used': 100,
            'latency_ms': 500
        }
        
        with patch.object(parser.gemini_client, 'generate', return_value=mock_response):
            result = await parser.extract_biomarkers(
                file_bytes=b"test content",
                filename="test.txt",
                content_type="text/plain"
            )
        
        # At lower bound should be Normal (not Low)
        glucose = next(b for b in result["biomarkers"] if b["id"] == "glucose")
        assert glucose["healthStatus"] == "Normal"
        
        # At upper bound should be Normal (not High)
        cholesterol = next(b for b in result["biomarkers"] if b["id"] == "cholesterol")
        assert cholesterol["healthStatus"] == "Normal"
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_biomarker_status_classification_metadata_preserved(self, parser):
        """Test that existing metadata is preserved after status classification."""
        # Mock Gemini response
        mock_response = {
            'text': json.dumps({
                "biomarkers": [
                    {
                        "id": "glucose",
                        "name": "Glucose",
                        "value": 85.0,
                        "unit": "mg/dL",
                        "reference": "70-100 mg/dL",
                        "confidence": 0.9,
                        "ref_low": 70.0,
                        "ref_high": 100.0
                    }
                ],
                "metadata": {
                    "extraction_method": "gemini_llm",
                    "confidence_score": 0.9
                }
            }),
            'tokens_used': 100,
            'latency_ms': 500
        }
        
        with patch.object(parser.gemini_client, 'generate', return_value=mock_response):
            result = await parser.extract_biomarkers(
                file_bytes=b"test content",
                filename="test.txt",
                content_type="text/plain"
            )
        
        # Verify metadata is preserved
        assert result["metadata"]["method"] == "gemini_llm_multimodal"
        assert result["metadata"]["mime_type"] == "text/plain"
        assert result["metadata"]["source"] == "test.txt"
        assert result["metadata"]["total_biomarkers"] == 1
        assert result["metadata"]["gemini_tokens_used"] == 100
        assert result["metadata"]["gemini_latency_ms"] == 500
        assert result["metadata"]["extraction_method"] == "gemini_llm"
        assert result["metadata"]["confidence_score"] == 0.9
