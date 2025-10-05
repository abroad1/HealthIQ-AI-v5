"""
Integration tests for multimodal LLM-powered biomarker parsing service.

Tests the complete pipeline from file upload to biomarker extraction using mocked Gemini responses
with support for PDF, images, text, CSV, and JSON files.
"""

import pytest
import json
from unittest.mock import Mock, patch, AsyncMock
from services.parsing.llm_parser import LLMParser, ParsedBiomarker, ParsedResult


class TestLLMParserMultimodalIntegration:
    """Integration tests for multimodal LLM parser service."""
    
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
    def sample_pdf_bytes(self):
        """Sample PDF file bytes for testing."""
        return b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Glucose: 95 mg/dL) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF"
    
    @pytest.fixture
    def sample_image_bytes(self):
        """Sample image file bytes for testing."""
        return b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.' \",#\x1c\x1c(7),01444\x1f'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9"
    
    @pytest.fixture
    def sample_text_content(self):
        """Sample text content for testing."""
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
    async def test_extract_biomarkers_from_pdf_multimodal(self, parser, mock_gemini_response, sample_pdf_bytes):
        """
        Test successful biomarker extraction from PDF using multimodal processing.
        
        Business Value: Core functionality for PDF lab reports
        User Scenario: User uploads PDF lab report and gets structured biomarker data
        """
        # Mock the Gemini client
        with patch.object(parser.gemini_client, 'generate', return_value=mock_gemini_response):
            # Test PDF content
            filename = "lab_report.pdf"
            
            # Extract biomarkers
            result = await parser.extract_biomarkers(sample_pdf_bytes, filename, "application/pdf")
            
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
            
            # Check metadata
            metadata = result["metadata"]
            assert metadata["source"] == filename
            assert metadata["method"] == "gemini_llm_multimodal"
            assert metadata["mime_type"] == "application/pdf"
            assert metadata["total_biomarkers"] == 2
            assert metadata["gemini_tokens_used"] == 150
            assert metadata["gemini_latency_ms"] == 1200
    
    @pytest.mark.asyncio
    async def test_extract_biomarkers_from_image_multimodal(self, parser, mock_gemini_response, sample_image_bytes):
        """
        Test successful biomarker extraction from image using multimodal processing.
        
        Business Value: Support for image-based lab reports
        User Scenario: User uploads image of lab report and gets structured biomarker data
        """
        # Mock the Gemini client
        with patch.object(parser.gemini_client, 'generate', return_value=mock_gemini_response):
            # Test image content
            filename = "lab_report.jpg"
            
            # Extract biomarkers
            result = await parser.extract_biomarkers(sample_image_bytes, filename, "image/jpeg")
            
            # Assertions
            assert result["biomarkers"] is not None
            assert len(result["biomarkers"]) == 2
            assert result["metadata"]["mime_type"] == "image/jpeg"
            assert result["metadata"]["source"] == filename
            assert result["metadata"]["method"] == "gemini_llm_multimodal"
    
    @pytest.mark.asyncio
    async def test_extract_biomarkers_from_text_multimodal(self, parser, mock_gemini_response, sample_text_content):
        """
        Test successful biomarker extraction from text using text-based processing.
        
        Business Value: Support for text-based lab data
        User Scenario: User uploads text file with lab data and gets structured biomarker data
        """
        # Mock the Gemini client
        with patch.object(parser.gemini_client, 'generate', return_value=mock_gemini_response):
            # Test text content
            file_bytes = sample_text_content.encode('utf-8')
            filename = "lab_report.txt"
            
            # Extract biomarkers
            result = await parser.extract_biomarkers(file_bytes, filename, "text/plain")
            
            # Assertions
            assert result["biomarkers"] is not None
            assert len(result["biomarkers"]) == 2
            assert result["metadata"]["mime_type"] == "text/plain"
            assert result["metadata"]["source"] == filename
            assert result["metadata"]["method"] == "gemini_llm_multimodal"
    
    @pytest.mark.asyncio
    async def test_extract_biomarkers_from_csv_multimodal(self, parser, mock_gemini_response):
        """
        Test successful biomarker extraction from CSV using text-based processing.
        
        Business Value: Support for CSV lab data exports
        User Scenario: User uploads CSV file with lab data and gets structured biomarker data
        """
        # Mock the Gemini client
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
            assert result["metadata"]["method"] == "gemini_llm_multimodal"
    
    @pytest.mark.asyncio
    async def test_extract_biomarkers_from_json_multimodal(self, parser, mock_gemini_response):
        """
        Test successful biomarker extraction from JSON using text-based processing.
        
        Business Value: Support for JSON lab data exports
        User Scenario: User uploads JSON file with lab data and gets structured biomarker data
        """
        # Mock the Gemini client
        with patch.object(parser.gemini_client, 'generate', return_value=mock_gemini_response):
            # Test JSON content
            json_content = json.dumps({
                "patient": "John Doe",
                "results": {
                    "glucose": {"value": 95, "unit": "mg/dL", "reference": "70-100"},
                    "cholesterol": {"value": 180, "unit": "mg/dL", "reference": "<200"}
                }
            })
            file_bytes = json_content.encode('utf-8')
            filename = "lab_data.json"
            
            # Extract biomarkers
            result = await parser.extract_biomarkers(file_bytes, filename, "application/json")
            
            # Assertions
            assert result["biomarkers"] is not None
            assert len(result["biomarkers"]) == 2
            assert result["metadata"]["mime_type"] == "application/json"
            assert result["metadata"]["source"] == filename
            assert result["metadata"]["method"] == "gemini_llm_multimodal"
    
    @pytest.mark.asyncio
    async def test_extract_biomarkers_unknown_file_type(self, parser, mock_gemini_response):
        """
        Test handling of unknown file types with fallback prompt.
        
        Business Value: Graceful handling of unsupported file formats
        User Scenario: User uploads unknown file type, should use fallback prompt
        """
        # Mock the Gemini client
        with patch.object(parser.gemini_client, 'generate', return_value=mock_gemini_response):
            # Test unknown file type
            file_bytes = b"some unknown content"
            filename = "unknown_file.xyz"
            
            # Extract biomarkers
            result = await parser.extract_biomarkers(file_bytes, filename, "application/octet-stream")
            
            # Assertions
            assert result["biomarkers"] is not None
            assert len(result["biomarkers"]) == 2
            assert result["metadata"]["mime_type"] == "application/octet-stream"
            assert result["metadata"]["source"] == filename
            assert result["metadata"]["method"] == "gemini_llm_multimodal"
    
    @pytest.mark.asyncio
    async def test_extract_biomarkers_mime_type_detection(self, parser, mock_gemini_response):
        """
        Test automatic MIME type detection from filename.
        
        Business Value: Automatic file type detection
        User Scenario: User uploads file without content-type, should auto-detect
        """
        # Mock the Gemini client
        with patch.object(parser.gemini_client, 'generate', return_value=mock_gemini_response):
            # Test PNG file without content-type
            file_bytes = b"fake png content"
            filename = "lab_report.png"
            
            # Extract biomarkers
            result = await parser.extract_biomarkers(file_bytes, filename)
            
            # Assertions
            assert result["biomarkers"] is not None
            assert result["metadata"]["mime_type"] == "image/png"
            assert result["metadata"]["source"] == filename
    
    @pytest.mark.asyncio
    async def test_extract_biomarkers_gemini_error_multimodal(self, parser):
        """
        Test handling of Gemini API errors in multimodal processing.
        
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
            # Test PDF content
            file_bytes = b"fake pdf content"
            filename = "lab_report.pdf"
            
            # Extract biomarkers
            result = await parser.extract_biomarkers(file_bytes, filename, "application/pdf")
            
            # Assertions
            assert result["biomarkers"] == []
            assert "error" in result["metadata"]
            assert "API rate limit exceeded" in result["metadata"]["error"]
    
    @pytest.mark.asyncio
    async def test_extract_biomarkers_invalid_json_response_multimodal(self, parser):
        """
        Test handling of invalid JSON response from Gemini in multimodal processing.
        
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
            # Test image content
            file_bytes = b"fake image content"
            filename = "lab_report.jpg"
            
            # Extract biomarkers
            result = await parser.extract_biomarkers(file_bytes, filename, "image/jpeg")
            
            # Assertions
            assert result["biomarkers"] == []
            assert "error" in result["metadata"]
            assert "Failed to parse response" in result["metadata"]["error"]
    
    def test_prompt_template_selection(self, parser):
        """
        Test prompt template selection based on MIME type.
        
        Business Value: Correct prompt routing for different file types
        User Scenario: Ensure appropriate prompts are used for different file formats
        """
        # Test PDF prompt selection
        pdf_prompt = parser._load_prompt_template('application/pdf')
        assert 'PDF-Specific Extraction Rules' in pdf_prompt
        
        # Test image prompt selection
        image_prompt = parser._load_prompt_template('image/jpeg')
        assert 'Image-Specific Extraction Rules' in image_prompt
        
        # Test text prompt selection
        text_prompt = parser._load_prompt_template('text/plain')
        assert 'Text-Specific Extraction Rules' in text_prompt
        
        # Test fallback prompt selection
        fallback_prompt = parser._load_prompt_template('application/octet-stream')
        assert 'Generic Extraction Rules' in fallback_prompt
    
    def test_mime_type_detection(self, parser):
        """
        Test MIME type detection from filename and content type.
        
        Business Value: Accurate file type detection
        User Scenario: Ensure correct MIME types are detected for various file formats
        """
        # Test with content type
        assert parser._detect_mime_type("test.pdf", "application/pdf") == "application/pdf"
        
        # Test with filename only
        assert parser._detect_mime_type("test.pdf") == "application/pdf"
        assert parser._detect_mime_type("test.jpg") == "image/jpeg"
        assert parser._detect_mime_type("test.png") == "image/png"
        assert parser._detect_mime_type("test.txt") == "text/plain"
        # Note: mimetypes.guess_type() returns 'application/vnd.ms-excel' for CSV files
        assert parser._detect_mime_type("test.csv") == "application/vnd.ms-excel"
        assert parser._detect_mime_type("test.json") == "application/json"
        
        # Test unknown file type
        assert parser._detect_mime_type("test.xyz") == "application/octet-stream"
        
        # Test no filename
        assert parser._detect_mime_type("") == "application/octet-stream"
