"""
LLM-powered biomarker parsing service using Gemini.

This module provides intelligent parsing of lab reports and medical documents
using Google's Gemini LLM with multimodal support for various file formats.
"""

import json
import io
import csv
import math
import mimetypes
import re
from typing import Dict, Any, List, Optional
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError

from core.llm.gemini_client import GeminiClient
from core.models.biomarker import BiomarkerValue


class ContextRangeOption(BaseModel):
    """Single sex/pregnancy/life-stage (etc.) band extracted for review-stage selection."""

    model_config = {"extra": "ignore"}

    context_label: str = Field(default="", description="Lab-defined label for this band")
    min: Optional[float] = Field(None, description="Lower bound if applicable")
    max: Optional[float] = Field(None, description="Upper bound if applicable")
    unit: str = Field(default="", description="Unit for this interval row")
    source_snippet: Optional[str] = Field(None, description="Short verbatim quote from the PDF")


class ParsedBiomarker(BaseModel):
    """Parsed biomarker data structure."""
    id: str = Field(..., description="Canonical biomarker ID")
    name: str = Field(..., description="Biomarker name")
    value: float = Field(..., description="Numeric value")
    unit: str = Field(..., description="Unit of measurement")
    reference: str = Field(..., description="Reference range (may combine primary line + contextual text)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    ref_low: Optional[float] = Field(None, description="Lower reference limit")
    ref_high: Optional[float] = Field(None, description="Upper reference limit")
    status: Optional[str] = Field(None, description="Health status: Low/Normal/High")
    raw_reference_text: Optional[str] = Field(
        None,
        description="Optional multi-line footnotes / sex or pregnancy context from the PDF",
    )
    context_range_options: List[ContextRangeOption] = Field(
        default_factory=list,
        description="Structured contextual intervals when the lab lists multiple bands",
    )


class ParsedResult(BaseModel):
    """Complete parsing result structure."""
    biomarkers: List[ParsedBiomarker] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LLMParser:
    """LLM-powered biomarker parser with multimodal support."""
    
    def __init__(self):
        """Initialize the LLM parser."""
        self.gemini_client = GeminiClient()
        
        # Prompt template mapping by MIME type
        self.prompt_templates = {
            'application/pdf': 'parsing_prompt_pdf.txt',
            'image/jpeg': 'parsing_prompt_image.txt',
            'image/png': 'parsing_prompt_image.txt',
            'image/jpg': 'parsing_prompt_image.txt',
            'text/plain': 'parsing_prompt_text.txt',
            'text/csv': 'parsing_prompt_text.txt',
            'application/vnd.ms-excel': 'parsing_prompt_text.txt',
            'application/json': 'parsing_prompt_text.txt',
        }
        self.fallback_prompt = 'parsing_prompt_generic.txt'
    
    def _load_prompt_template(self, mime_type: str) -> str:
        """Load the appropriate prompt template for the MIME type."""
        prompt_filename = self.prompt_templates.get(mime_type, self.fallback_prompt)
        prompt_path = Path(__file__).parent.parent.parent / "core" / "llm" / "prompts" / prompt_filename
        
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            return self._load_fallback_prompt()
    
    def _load_fallback_prompt(self) -> str:
        """Load the fallback prompt template."""
        return """
        You are a biomedical data parser.
        Extract all quantitative biomarkers and return valid JSON matching this schema:
        {
          "biomarkers": [
            {
              "id": "string (canonical biomarker ID)",
              "name": "string (biomarker name)",
              "value": float (numeric value),
              "unit": "string (unit of measurement)",
              "reference": "string (reference range)",
              "confidence": float (confidence score 0.0-1.0),
              "ref_low": float (lower reference limit, optional),
              "ref_high": float (upper reference limit, optional)
            }
          ]
        }
        Only output JSON. No explanations.
        """
    
    def _detect_mime_type(self, filename: str, content_type: Optional[str] = None) -> str:
        """Detect MIME type from filename and content type."""
        if content_type:
            return content_type
        
        if filename:
            guessed_type, _ = mimetypes.guess_type(filename)
            if guessed_type:
                return guessed_type
        
        # Fallback based on file extension
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
        
        return 'application/octet-stream'
    
    def _convert_to_text(self, file_bytes: bytes, mime_type: str, filename: str) -> str:
        """Convert file bytes to text based on MIME type."""
        try:
            if mime_type == 'text/plain':
                return file_bytes.decode('utf-8')
            elif mime_type in ['text/csv', 'application/vnd.ms-excel']:
                return self._extract_csv_text(file_bytes)
            elif mime_type == 'application/json':
                return self._extract_json_text(file_bytes)
            else:
                return file_bytes.decode('utf-8', errors='ignore')
        except Exception as e:
            raise ValueError(f"Failed to convert {mime_type} file to text: {str(e)}")
    
    def _extract_csv_text(self, file_bytes: bytes) -> str:
        """Extract text from CSV file."""
        try:
            text = file_bytes.decode('utf-8')
            # Convert CSV to readable format
            csv_reader = csv.reader(io.StringIO(text))
            rows = list(csv_reader)
            
            # Format as readable text
            formatted_text = ""
            for row in rows:
                formatted_text += " | ".join(row) + "\n"
            
            return formatted_text.strip()
        except Exception as e:
            raise ValueError(f"Failed to extract CSV text: {str(e)}")
    
    def _extract_json_text(self, file_bytes: bytes) -> str:
        """Extract text from JSON file."""
        try:
            data = json.loads(file_bytes.decode('utf-8'))
            # Convert JSON to readable format
            return json.dumps(data, indent=2)
        except Exception as e:
            raise ValueError(f"Failed to extract JSON text: {str(e)}")
    
    @staticmethod
    def _coerce_optional_ref_bound(value: Any) -> Optional[float]:
        """Coerce LLM JSON ref_low/ref_high to float or None."""
        if value is None:
            return None
        try:
            f = float(value)
        except (TypeError, ValueError):
            return None
        return f if math.isfinite(f) else None

    @staticmethod
    def _has_any_bound(ref_low: Optional[float], ref_high: Optional[float]) -> bool:
        return ref_low is not None or ref_high is not None

    def _parse_context_range_options(self, raw: Any) -> List[ContextRangeOption]:
        if not isinstance(raw, list) or len(raw) == 0:
            return []
        out: List[ContextRangeOption] = []
        for item in raw:
            if not isinstance(item, dict):
                continue
            label = str(item.get("context_label") or item.get("contextLabel") or "").strip() or "Reference"
            try:
                out.append(
                    ContextRangeOption(
                        context_label=label,
                        min=self._coerce_optional_ref_bound(item.get("min")),
                        max=self._coerce_optional_ref_bound(item.get("max")),
                        unit=str(item.get("unit") or "").strip(),
                        source_snippet=(
                            str(item["source_snippet"]).strip()
                            if item.get("source_snippet") or item.get("sourceSnippet")
                            else None
                        ),
                    )
                )
            except (TypeError, ValueError):
                continue
        return out

    def _parse_reference_range(self, reference: str) -> tuple[Optional[float], Optional[float]]:
        """Parse reference range string to extract numeric limits."""
        if not reference:
            return None, None
        
        # Common patterns for reference ranges
        patterns = [
            r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)',  # "70-100"
            r'(\d+(?:\.\d+)?)\s*to\s*(\d+(?:\.\d+)?)',  # "70 to 100"
            r'(\d+(?:\.\d+)?)\s*–\s*(\d+(?:\.\d+)?)',   # "70–100" (en dash)
            r'(\d+(?:\.\d+)?)\s*–\s*(\d+(?:\.\d+)?)',   # "70–100" (em dash)
            r'<\s*(\d+(?:\.\d+)?)',                     # "< 200"
            r'>\s*(\d+(?:\.\d+)?)',                     # "> 40"
            r'≤\s*(\d+(?:\.\d+)?)',                     # "≤ 200"
            r'≥\s*(\d+(?:\.\d+)?)',                     # "≥ 40"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, reference, re.IGNORECASE)
            if match:
                if '<' in pattern or '≤' in pattern:
                    return None, float(match.group(1))
                elif '>' in pattern or '≥' in pattern:
                    return float(match.group(1)), None
                else:
                    return float(match.group(1)), float(match.group(2))
        
        return None, None
    
    def _compute_health_status(self, value: float, ref_low: Optional[float], ref_high: Optional[float]) -> str:
        """Compute health status based on value and reference limits."""
        if ref_low is not None and value < ref_low:
            return "Low"
        elif ref_high is not None and value > ref_high:
            return "High"
        else:
            return "Normal"
    
    def _parse_gemini_response(self, response_text: str) -> ParsedResult:
        """Parse Gemini response into structured data."""
        try:
            # Clean response text
            text = response_text.strip()
            
            # Remove markdown code blocks if present
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            
            text = text.strip()
            
            # Parse JSON
            data = json.loads(text)
            
            # Extract biomarkers
            biomarkers = []
            for biomarker_data in data.get("biomarkers", []):
                try:
                    context_opts = self._parse_context_range_options(
                        biomarker_data.get("context_range_options")
                        or biomarker_data.get("contextRangeOptions")
                    )
                    main_ref = str(biomarker_data.get("reference") or "").strip()
                    raw_extra = str(biomarker_data.get("raw_reference_text") or "").strip()
                    if raw_extra and main_ref:
                        combined_ref = f"{raw_extra}\n\n{main_ref}"
                    elif raw_extra:
                        combined_ref = raw_extra
                    else:
                        combined_ref = main_ref

                    if len(context_opts) > 1:
                        # Multiple contextual bands: require user selection; do not guess ref bounds.
                        ref_low, ref_high = None, None
                        status = "Unknown"
                    elif len(context_opts) == 1:
                        o0 = context_opts[0]
                        ref_low, ref_high = o0.min, o0.max
                        if not self._has_any_bound(ref_low, ref_high):
                            ref_low, ref_high = self._parse_reference_range(main_ref)
                        if not self._has_any_bound(ref_low, ref_high):
                            ref_low = self._coerce_optional_ref_bound(biomarker_data.get("ref_low"))
                            ref_high = self._coerce_optional_ref_bound(biomarker_data.get("ref_high"))
                        if not self._has_any_bound(ref_low, ref_high):
                            ref_low, ref_high = self._parse_reference_range(combined_ref)
                        status = self._compute_health_status(
                            biomarker_data["value"],
                            ref_low,
                            ref_high,
                        )
                    else:
                        # Bound extraction: primary line first; LLM numeric helpers second; combined scan last only
                        # if needed — avoids footnote/pregnancy tables overriding the main threshold.
                        ref_low, ref_high = self._parse_reference_range(main_ref)
                        if not self._has_any_bound(ref_low, ref_high):
                            ref_low = self._coerce_optional_ref_bound(biomarker_data.get("ref_low"))
                            ref_high = self._coerce_optional_ref_bound(biomarker_data.get("ref_high"))
                        if not self._has_any_bound(ref_low, ref_high):
                            ref_low, ref_high = self._parse_reference_range(combined_ref)

                        status = self._compute_health_status(
                            biomarker_data["value"],
                            ref_low,
                            ref_high,
                        )

                    biomarker = ParsedBiomarker(
                        id=biomarker_data["id"],
                        name=biomarker_data["name"],
                        value=biomarker_data["value"],
                        unit=biomarker_data["unit"],
                        reference=combined_ref if combined_ref else main_ref,
                        confidence=biomarker_data["confidence"],
                        ref_low=ref_low,
                        ref_high=ref_high,
                        status=status,
                        raw_reference_text=raw_extra or None,
                        context_range_options=context_opts,
                    )
                    biomarkers.append(biomarker)
                except (KeyError, ValueError, TypeError) as e:
                    # Skip invalid biomarker entries
                    continue
            
            return ParsedResult(
                biomarkers=biomarkers,
                metadata=data.get("metadata", {})
            )
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to parse response: {str(e)}")
    
    async def extract_biomarkers(self, file_bytes: bytes, filename: str, content_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Extract biomarkers from file using LLM.
        
        Args:
            file_bytes: File content as bytes
            filename: Name of the file
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
            
            # Convert to expected format and add deterministic classification
            biomarkers_list = []
            for biomarker in parsed_result.biomarkers:
                # Add deterministic classification based on value and reference ranges
                try:
                    value = float(biomarker.value)
                    ref_low = float(biomarker.ref_low) if biomarker.ref_low is not None else None
                    ref_high = float(biomarker.ref_high) if biomarker.ref_high is not None else None
                    
                    if ref_low is not None and value < ref_low:
                        health_status = "Low"
                    elif ref_high is not None and value > ref_high:
                        health_status = "High"
                    else:
                        health_status = "Normal"
                except (TypeError, ValueError):
                    health_status = "Unknown"
                
                row: Dict[str, Any] = {
                    "id": biomarker.id,
                    "name": biomarker.name,
                    "value": biomarker.value,
                    "unit": biomarker.unit,
                    "referenceRange": biomarker.reference,
                    "confidence": biomarker.confidence,
                    "ref_low": biomarker.ref_low,
                    "ref_high": biomarker.ref_high,
                    "healthStatus": health_status,
                }
                if biomarker.raw_reference_text:
                    row["rawReferenceText"] = biomarker.raw_reference_text
                if biomarker.context_range_options:
                    row["contextRangeOptions"] = [
                        {
                            "contextLabel": opt.context_label,
                            "min": opt.min,
                            "max": opt.max,
                            "unit": opt.unit,
                            "sourceSnippet": opt.source_snippet,
                        }
                        for opt in biomarker.context_range_options
                    ]
                biomarkers_list.append(row)
            
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
            metadata["source"] = filename  # Ensure filename takes precedence
            
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
