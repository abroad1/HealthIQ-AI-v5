"""
Integration tests for LLM-powered biomarker parsing service.

Tests the complete pipeline from file upload to biomarker extraction using mocked Gemini responses.
"""

import pytest
import json
from unittest.mock import Mock, patch, AsyncMock
from services.parsing.llm_parser import LLMParser, ParsedBiomarker, ParsedResult


class TestLLMParserIntegration:
    """Integration tests for LLM parser service."""
    
    @pytest.fixture
    def parser(self):
        """Create LLM parser instance for testing."""
        return LLMParser()
    
    @pytest.fixture
    def mock_gemini_response(self):
        """Mock Gemini response with valid biomarker data."""
        return {
            "text": json.dumps({
                "biomarkers": [
                    {
                        "id": "glucose",
                        "name": "Glucose",
                        "value": 95.0,
                        "unit": "mg/dL",
                        "reference": "70-100 mg/dL",
                        "confidence": 0.95
                    },
                    {
                        "id": "total_cholesterol",
                        "name": "Total Cholesterol",
                        "value": 180.0,
                        "unit": "mg/dL",
                        "reference": "< 200 mg/dL",
                        "confidence": 0.90
                    }
                ]
            }),
            "tokens_used": 150,
            "latency_ms": 1200,
            "model": "models/gemini-flash-latest"
        }
    
    @pytest.fixture
    def sample_lab_text(self):
        """Sample lab report text for testing."""
        return """
        LABORATORY RESULTS
        
        Patient: John Doe
        Date: 2024-01-15
        
        Glucose: 95 mg/dL (Reference: 70-100 mg/dL)
        Total Cholesterol: 180 mg/dL (Reference: < 200 mg/dL)
        HDL Cholesterol: 45 mg/dL (Reference: > 40 mg/dL)
        LDL Cholesterol: 120 mg/dL (Reference: < 100 mg/dL)
        Triglycerides: 150 mg/dL (Reference: < 150 mg/dL)
        
        These results are within normal limits.
        """
    
    @pytest.mark.asyncio
    async def test_extract_biomarkers_from_text_success(self, parser, mock_gemini_response, sample_lab_text):
        """
        Test successful biomarker extraction from text content.
        
        Business Value: Core functionality for parsing lab reports
        User Scenario: User uploads lab report text and gets structured biomarker data
        """
        # Mock the Gemini client
        with patch.object(parser.gemini_client, 'generate', return_value=mock_gemini_response):
            # Test text content
            file_bytes = sample_lab_text.encode('utf-8')
            filename = "lab_report.txt"
            
            # Extract biomarkers
            result = await parser.extract_biomarkers(file_bytes, filename, "text/plain")
            
            # Assertions
            assert result["biomarkers"] is not None
            assert len(result["biomarkers"]) == 2
            
            # Check first biomarker
            glucose = result["biomarkers"][0]
            assert glucose["id"] == "glucose"
            assert glucose["name"] == "Glucose"
            assert glucose["value"] == 95.0
            assert glucose["unit"] == "mg/dL"
            assert glucose["reference"] == "70-100 mg/dL"
            assert glucose["confidence"] == 0.95
            
            # Check second biomarker
            cholesterol = result["biomarkers"][1]
            assert cholesterol["id"] == "total_cholesterol"
            assert cholesterol["name"] == "Total Cholesterol"
            assert cholesterol["value"] == 180.0
            assert cholesterol["unit"] == "mg/dL"
            assert cholesterol["reference"] == "< 200 mg/dL"
            assert cholesterol["confidence"] == 0.90
            
            # Check metadata
            metadata = result["metadata"]
            assert metadata["source"] == filename
            assert metadata["method"] == "gemini_llm_multimodal"
            assert metadata["mime_type"] == "text/plain"
            assert metadata["total_biomarkers"] == 2
            assert metadata["gemini_tokens_used"] == 150
            assert metadata["gemini_latency_ms"] == 1200
    
    @pytest.mark.asyncio
    async def test_extract_biomarkers_from_pdf_success(self, parser, mock_gemini_response):
        """
        Test successful biomarker extraction from PDF content.
        
        Business Value: Support for PDF lab reports (common format)
        User Scenario: User uploads PDF lab report and gets structured biomarker data
        """
        # Mock PDF text extraction
        sample_pdf_text = "Glucose: 95 mg/dL, Total Cholesterol: 180 mg/dL"
        
        with patch('services.parsing.llm_parser.PyPDF2.PdfReader') as mock_pdf_reader:
            # Mock PDF reader
            mock_page = Mock()
            mock_page.extract_text.return_value = sample_pdf_text
            mock_pdf_reader.return_value.pages = [mock_page]
            
            # Mock Gemini client
            with patch.object(parser.gemini_client, 'generate', return_value=mock_gemini_response):
                # Test PDF content
                file_bytes = b"fake_pdf_content"
                filename = "lab_report.pdf"
                
                # Extract biomarkers
                result = await parser.extract_biomarkers(file_bytes, filename, "application/pdf")
                
                # Assertions
                assert result["biomarkers"] is not None
                assert len(result["biomarkers"]) == 2
                assert result["metadata"]["mime_type"] == "application/pdf"
                assert result["metadata"]["source"] == filename
    
    @pytest.mark.asyncio
    async def test_extract_biomarkers_from_csv_success(self, parser, mock_gemini_response):
        """
        Test successful biomarker extraction from CSV content.
        
        Business Value: Support for CSV lab data exports
        User Scenario: User uploads CSV file with lab data and gets structured biomarker data
        """
        # Mock Gemini client
        with patch.object(parser.gemini_client, 'generate', return_value=mock_gemini_response):
            # Test CSV content
            csv_content = "Biomarker,Value,Unit,Reference\nGlucose,95,mg/dL,70-100\nCholesterol,180,mg/dL,<200"
            file_bytes = csv_content.encode('utf-8')
            filename = "lab_data.csv"
            
            # Extract biomarkers
            result = await parser.extract_biomarkers(file_bytes, filename, "text/csv")
            
            # Assertions
            assert result["biomarkers"] is not None
            assert len(result["biomarkers"]) == 2
            assert result["metadata"]["mime_type"] == "text/csv"
            assert result["metadata"]["source"] == filename
    
    @pytest.mark.asyncio
    async def test_extract_biomarkers_gemini_error(self, parser, sample_lab_text):
        """
        Test handling of Gemini API errors.
        
        Business Value: Graceful error handling for API failures
        User Scenario: User uploads file but Gemini API is down, should get error response
        """
        # Mock Gemini error response
        error_response = {
            "text": None,
            "error": "API rate limit exceeded",
            "tokens_used": 0,
            "latency_ms": 0
        }
        
        with patch.object(parser.gemini_client, 'generate', return_value=error_response):
            # Test text content
            file_bytes = sample_lab_text.encode('utf-8')
            filename = "lab_report.txt"
            
            # Extract biomarkers
            result = await parser.extract_biomarkers(file_bytes, filename, "text/plain")
            
            # Assertions
            assert result["biomarkers"] == []
            assert "error" in result["metadata"]
            assert "API rate limit exceeded" in result["metadata"]["error"]
    
    @pytest.mark.asyncio
    async def test_extract_biomarkers_invalid_json_response(self, parser, sample_lab_text):
        """
        Test handling of invalid JSON response from Gemini.
        
        Business Value: Robust parsing of malformed LLM responses
        User Scenario: Gemini returns invalid JSON, should handle gracefully
        """
        # Mock invalid JSON response
        invalid_response = {
            "text": "This is not valid JSON",
            "tokens_used": 50,
            "latency_ms": 800
        }
        
        with patch.object(parser.gemini_client, 'generate', return_value=invalid_response):
            # Test text content
            file_bytes = sample_lab_text.encode('utf-8')
            filename = "lab_report.txt"
            
            # Extract biomarkers
            result = await parser.extract_biomarkers(file_bytes, filename, "text/plain")
            
            # Assertions
            assert result["biomarkers"] == []
            assert "error" in result["metadata"]
            assert "Failed to parse response" in result["metadata"]["error"]
    
    @pytest.mark.asyncio
    async def test_extract_biomarkers_empty_file(self, parser):
        """
        Test handling of empty file content.
        
        Business Value: Handle edge cases gracefully
        User Scenario: User uploads empty file, should get appropriate error
        """
        # Test empty content
        file_bytes = b""
        filename = "empty.txt"
        
        # Extract biomarkers
        result = await parser.extract_biomarkers(file_bytes, filename, "text/plain")
        
        # Assertions
        assert result["biomarkers"] == []
        assert "error" in result["metadata"]
        assert "No text content extracted" in result["metadata"]["error"]
    
    @pytest.mark.asyncio
    async def test_extract_biomarkers_unknown_file_type(self, parser, mock_gemini_response, sample_lab_text):
        """
        Test handling of unknown file types.
        
        Business Value: Support for various file formats
        User Scenario: User uploads file with unknown extension, should still attempt parsing
        """
        # Mock Gemini client
        with patch.object(parser.gemini_client, 'generate', return_value=mock_gemini_response):
            # Test unknown file type
            file_bytes = sample_lab_text.encode('utf-8')
            filename = "lab_report.unknown"
            
            # Extract biomarkers
            result = await parser.extract_biomarkers(file_bytes, filename, "application/octet-stream")
            
            # Assertions
            assert result["biomarkers"] is not None
            assert len(result["biomarkers"]) == 2
            assert result["metadata"]["mime_type"] == "application/octet-stream"
    
    def test_parsed_biomarker_validation(self):
        """
        Test Pydantic validation of parsed biomarker data.
        
        Business Value: Data integrity and type safety
        User Scenario: Ensure biomarker data follows expected schema
        """
        # Valid biomarker data
        valid_data = {
            "id": "glucose",
            "name": "Glucose",
            "value": 95.0,
            "unit": "mg/dL",
            "reference": "70-100 mg/dL",
            "confidence": 0.95
        }
        
        biomarker = ParsedBiomarker(**valid_data)
        assert biomarker.id == "glucose"
        assert biomarker.value == 95.0
        assert biomarker.confidence == 0.95
        
        # Invalid confidence score
        invalid_data = valid_data.copy()
        invalid_data["confidence"] = 1.5  # > 1.0
        
        with pytest.raises(ValueError):
            ParsedBiomarker(**invalid_data)
    
    def test_parsed_result_validation(self):
        """
        Test Pydantic validation of parsed result data.
        
        Business Value: Data integrity for complete parsing results
        User Scenario: Ensure parsing results follow expected schema
        """
        # Valid result data
        biomarkers = [
            ParsedBiomarker(
                id="glucose",
                name="Glucose",
                value=95.0,
                unit="mg/dL",
                reference="70-100 mg/dL",
                confidence=0.95
            )
        ]
        
        result = ParsedResult(
            biomarkers=biomarkers,
            metadata={"source": "test", "method": "gemini_llm"}
        )
        
        assert len(result.biomarkers) == 1
        assert result.biomarkers[0].id == "glucose"
        assert result.metadata["source"] == "test"
