"""
LLM-powered biomarker parsing service using Gemini with multimodal support.
"""

import json
import io
import csv
import mimetypes
from typing import Dict, Any, List, Optional
from pathlib import Path
import PyPDF2
from pydantic import BaseModel, Field, ValidationError

from core.llm.gemini_client import GeminiClient
from core.models.biomarker import BiomarkerValue


class ParsedBiomarker(BaseModel):
    """Parsed biomarker data from LLM extraction."""
    
    id: str = Field(..., description="Canonical biomarker ID")
    name: str = Field(..., description="Biomarker name")
    value: float = Field(..., description="Numeric value")
    unit: str = Field(..., description="Unit of measurement")
    reference: str = Field(..., description="Reference range")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")


class ParsedResult(BaseModel):
    """Complete parsing result from LLM."""
    
    biomarkers: List[ParsedBiomarker] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LLMParser:
    """
    LLM-powered biomarker parser using Gemini with multimodal support.
    
    Extracts biomarkers from various file formats (PDF, images, TXT, CSV, JSON)
    and returns structured biomarker data with confidence scores.
    Automatically routes files to appropriate prompt templates based on MIME type.
    """
    
    def __init__(self):
        """Initialize the LLM parser with Gemini client and prompt templates."""
        self.gemini_client = GeminiClient()
        
        # Prompt template lookup based on MIME type
        self.prompt_templates = {
            'application/pdf': 'parsing_prompt_pdf.txt',
            'image/jpeg': 'parsing_prompt_image.txt',
            'image/png': 'parsing_prompt_image.txt',
            'image/jpg': 'parsing_prompt_image.txt',
            'text/plain': 'parsing_prompt_text.txt',
            'text/csv': 'parsing_prompt_text.txt',
            'application/vnd.ms-excel': 'parsing_prompt_text.txt',  # CSV files
            'application/json': 'parsing_prompt_text.txt',
        }
        
        # Fallback prompt for unknown types
        self.fallback_prompt = 'parsing_prompt_generic.txt'
    
    def _load_prompt_template(self, mime_type: str) -> str:
        """Load the appropriate prompt template based on MIME type."""
        # Get prompt filename from lookup
        prompt_filename = self.prompt_templates.get(mime_type, self.fallback_prompt)
        
        # Load prompt from file
        prompt_path = Path(__file__).parent.parent.parent / "core" / "llm" / "prompts" / prompt_filename
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            # Fallback to generic prompt if specific file doesn't exist
            return self._load_fallback_prompt()
    
    def _load_fallback_prompt(self) -> str:
        """Load the fallback prompt template."""
        fallback_path = Path(__file__).parent.parent.parent / "core" / "llm" / "prompts" / self.fallback_prompt
        try:
            with open(fallback_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            # Ultimate fallback if no prompt files exist
            return """You are a biomedical data parser specialized in extracting quantitative biomarkers from lab reports.

Extract all quantitative biomarkers and return valid JSON matching this exact schema:
{
  "biomarkers": [
    {
      "id": "string (canonical biomarker ID)",
      "name": "string (biomarker name)",
      "value": float (numeric value),
      "unit": "string (unit of measurement)",
      "reference": "string (reference range)",
      "confidence": float (confidence score 0.0-1.0)
    }
  ]
}

Rules:
- Only extract quantitative biomarkers with numeric values
- Use canonical biomarker IDs from the standard list
- Include confidence scores based on clarity of extraction
- Only output valid JSON, no explanations or additional text
- If no biomarkers found, return empty biomarkers array"""
    
    def _detect_mime_type(self, filename: str, content_type: Optional[str] = None) -> str:
        """Detect MIME type from filename and content type."""
        # First try content_type if provided
        if content_type:
            return content_type
        
        # Use mimetypes library to guess from filename
        if filename:
            guessed_type, _ = mimetypes.guess_type(filename)
            if guessed_type:
                return guessed_type
        
        # Fallback to extension-based detection
        if filename:
            ext = Path(filename).suffix.lower()
            if ext == '.pdf':
                return 'application/pdf'
            elif ext in ['.txt', '.text']:
                return 'text/plain'
            elif ext == '.csv':
                return 'text/csv'
            elif ext == '.json':
                return 'application/json'
            elif ext in ['.jpg', '.jpeg']:
                return 'image/jpeg'
            elif ext == '.png':
                return 'image/png'
        
        # Ultimate fallback
        return 'application/octet-stream'
    
    def _convert_to_text(self, file_bytes: bytes, mime_type: str, filename: str) -> str:
        """Convert file bytes to plain text based on MIME type."""
        try:
            if mime_type == 'application/pdf':
                return self._extract_pdf_text(file_bytes)
            elif mime_type == 'text/plain':
                return file_bytes.decode('utf-8')
            elif mime_type in ['text/csv', 'application/vnd.ms-excel']:
                return self._extract_csv_text(file_bytes)
            elif mime_type == 'application/json':
                return self._extract_json_text(file_bytes)
            else:
                # Try to decode as text for unknown types
                return file_bytes.decode('utf-8', errors='ignore')
        except Exception as e:
            raise ValueError(f"Failed to convert {mime_type} file to text: {str(e)}")
    
    def _extract_pdf_text(self, file_bytes: bytes) -> str:
        """Extract text from PDF bytes."""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise ValueError(f"Failed to extract PDF text: {str(e)}")
    
    def _extract_csv_text(self, file_bytes: bytes) -> str:
        """Extract text from CSV bytes."""
        try:
            csv_text = file_bytes.decode('utf-8')
            # Convert CSV to readable text format
            csv_reader = csv.reader(io.StringIO(csv_text))
            lines = []
            for row in csv_reader:
                lines.append(" | ".join(row))
            return "\n".join(lines)
        except Exception as e:
            raise ValueError(f"Failed to extract CSV text: {str(e)}")
    
    def _extract_json_text(self, file_bytes: bytes) -> str:
        """Extract text from JSON bytes."""
        try:
            json_data = json.loads(file_bytes.decode('utf-8'))
            # Convert JSON to readable text format
            return json.dumps(json_data, indent=2)
        except Exception as e:
            raise ValueError(f"Failed to extract JSON text: {str(e)}")
    
    def _parse_gemini_response(self, response_text: str) -> ParsedResult:
        """Parse Gemini response into structured biomarker data."""
        try:
            # Clean response text
            response_text = response_text.strip()
            
            # Try to extract JSON from response
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            # Parse JSON
            response_data = json.loads(response_text)
            
            # Validate and convert to Pydantic models
            biomarkers = []
            for biomarker_data in response_data.get('biomarkers', []):
                try:
                    biomarker = ParsedBiomarker(**biomarker_data)
                    biomarkers.append(biomarker)
                except ValidationError as e:
                    # Skip invalid biomarkers but continue processing
                    continue
            
            return ParsedResult(
                biomarkers=biomarkers,
                metadata={
                    "source": "gemini_llm",
                    "extraction_method": "llm_parsing",
                    "total_biomarkers": len(biomarkers)
                }
            )
            
        except (json.JSONDecodeError, ValidationError) as e:
            # Return empty result if parsing fails
            return ParsedResult(
                biomarkers=[],
                metadata={
                    "source": "gemini_llm",
                    "extraction_method": "llm_parsing",
                    "error": f"Failed to parse response: {str(e)}",
                    "total_biomarkers": 0
                }
            )
    
    async def extract_biomarkers(self, file_bytes: bytes, filename: str, content_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Extract biomarkers from uploaded file using multimodal LLM.
        
        Args:
            file_bytes: Raw file bytes
            filename: Original filename
            content_type: MIME content type (optional)
            
        Returns:
            Dictionary with extracted biomarkers and metadata
        """
        try:
            # Detect MIME type
            mime_type = self._detect_mime_type(filename, content_type)
            
            # Load appropriate prompt template
            prompt_template = self._load_prompt_template(mime_type)
            
            # Determine if we should send raw file or convert to text
            if mime_type in ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg']:
                # Send raw file for multimodal processing
                input_files = [(mime_type, file_bytes)]
                response = self.gemini_client.generate(prompt_template, input_files=input_files)
            else:
                # Convert to text for text-based processing
                text_content = self._convert_to_text(file_bytes, mime_type, filename)
                
                if not text_content.strip():
                    return {
                        "biomarkers": [],
                        "metadata": {
                            "source": filename,
                            "method": "gemini_llm_multimodal",
                            "error": "No text content extracted from file",
                            "mime_type": mime_type
                        }
                    }
                
                # Create prompt with text content
                full_prompt = f"{prompt_template}\n\nFile content to parse:\n{text_content}"
                response = self.gemini_client.generate(full_prompt)
            
            if response.get('error'):
                return {
                    "biomarkers": [],
                    "metadata": {
                        "source": filename,
                        "method": "gemini_llm_multimodal",
                        "error": f"Gemini API error: {response['error']}",
                        "mime_type": mime_type
                    }
                }
            
            # Parse response
            parsed_result = self._parse_gemini_response(response['text'])
            
            # Convert to expected format
            biomarkers_list = []
            for biomarker in parsed_result.biomarkers:
                biomarkers_list.append({
                    "id": biomarker.id,
                    "name": biomarker.name,
                    "value": biomarker.value,
                    "unit": biomarker.unit,
                    "reference": biomarker.reference,
                    "confidence": biomarker.confidence
                })
            
            # Merge metadata, ensuring filename takes precedence
            metadata = {
                "source": filename,
                "method": "gemini_llm_multimodal",
                "mime_type": mime_type,
                "total_biomarkers": len(biomarkers_list),
                "gemini_tokens_used": response.get('tokens_used', 0),
                "gemini_latency_ms": response.get('latency_ms', 0),
                **parsed_result.metadata
            }
            # Ensure source is always the filename
            metadata["source"] = filename
            
            return {
                "biomarkers": biomarkers_list,
                "metadata": metadata
            }
            
        except Exception as e:
            return {
                "biomarkers": [],
                "metadata": {
                    "source": filename,
                    "method": "gemini_llm_multimodal",
                    "error": f"Parsing failed: {str(e)}",
                    "mime_type": mime_type if 'mime_type' in locals() else "unknown"
                }
            }
