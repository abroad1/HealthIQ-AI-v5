"""
Upload API routes - handles file uploads and parsing operations.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Dict, Any, Optional
from pydantic import BaseModel
import json
import yaml
from pathlib import Path
from datetime import datetime
from services.parsing.llm_parser import LLMParser
from services.parsing.deterministic_parser import try_deterministic_parse
from core.canonical.resolver import resolve_to_canonical
from core.lab.detector import detect_lab_origin

router = APIRouter()


def _load_ssot_metadata() -> Dict[str, Any]:
    """Load SSOT metadata for biomarkers. Cached per request."""
    ssot_path = Path(__file__).parent.parent.parent / "ssot" / "biomarkers.yaml"
    if not ssot_path.exists():
        return {}
    
    with open(ssot_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    return data.get("biomarkers", {})


class ParseResponse(BaseModel):
    """Response model for upload parsing."""
    success: bool
    message: str
    parsed_data: Optional[Dict[str, Any]] = None
    analysis_id: Optional[str] = None
    timestamp: str
    lab_origin: Optional[Dict[str, Any]] = None


@router.post("/parse")
async def parse_upload(
    file: Optional[UploadFile] = File(None),
    text_content: Optional[str] = Form(None)
) -> ParseResponse:
    """
    Parse uploaded file or text content using LLM-powered biomarker extraction.
    
    Uses Gemini LLM to extract quantitative biomarkers from lab reports and medical documents.
    Supports PDF, TXT, CSV, and JSON file formats.
    
    Args:
        file: Optional uploaded file
        text_content: Optional text content from form data
        
    Returns:
        Parsed biomarker data with confidence scores and metadata
    """
    try:
        # Generate analysis ID
        analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Initialize LLM parser
        parser = LLMParser()
        
        # Determine input source and process
        extracted_text: Optional[str] = None
        if file:
            # Read file bytes
            file_bytes = await file.read()
            filename = file.filename or "unknown"
            content_type = file.content_type

            # Extract biomarkers using LLM (may also yield text for lab detection)
            result = await parser.extract_biomarkers(file_bytes, filename, content_type)
            extracted_text = result.get("metadata", {}).get("extracted_text")

            input_source = "file_upload"
            content_info = f" (filename: {filename}, content_type: {content_type})"
            
        elif text_content:
            input_source = "text_input"
            content_info = f" (text length: {len(text_content)} characters)"
            filename = "text_input"

            # Try deterministic parser first for canonical CSV-ish format (marker,value,unit lines)
            deterministic_biomarkers = try_deterministic_parse(text_content)
            if deterministic_biomarkers is not None:
                result = {
                    "biomarkers": deterministic_biomarkers,
                    "metadata": {
                        "source": filename,
                        "method": "deterministic_csv",
                        "mime_type": "text/plain",
                    },
                }
            else:
                # Fall back to LLM for complex/unstructured content
                file_bytes = text_content.encode('utf-8')
                result = await parser.extract_biomarkers(file_bytes, filename, "text/plain")
            extracted_text = text_content

        else:
            raise HTTPException(
                status_code=400,
                detail="Either file or text_content must be provided"
            )
        
        # Check for parsing errors
        if result.get("metadata", {}).get("error"):
            return ParseResponse(
                success=False,
                message=f"Parsing failed for {input_source}{content_info}: {result['metadata']['error']}",
                parsed_data=None,
                analysis_id=analysis_id,
                timestamp=datetime.now().isoformat(),
                lab_origin=None,
            )

        # Sprint 2: Deterministic lab origin detection
        lab_origin = detect_lab_origin(text=extracted_text, filename=filename)
        
        # Enrich biomarkers with SSOT metadata
        enriched_biomarkers = []
        ssot_data = _load_ssot_metadata()
        
        for biomarker in result.get("biomarkers", []):
            # Resolve to canonical name
            canonical_id = resolve_to_canonical(biomarker.get("id", ""))
            
            # Get SSOT metadata if available
            ssot_metadata = {}
            if canonical_id and canonical_id in ssot_data:
                ssot_def = ssot_data[canonical_id]
                ssot_metadata = {
                    "system": ssot_def.get("system", ""),
                    "clusters": ssot_def.get("clusters", []),
                    "roles": ssot_def.get("roles", []),
                    "clinical_weight": ssot_def.get("clinical_weight", 0.0),
                }
            
            # Add SSOT block (empty if not found, but still include it)
            enriched_biomarker = {**biomarker, "ssot": ssot_metadata}
            enriched_biomarkers.append(enriched_biomarker)
        
        # Format response data
        parsing_method = result.get("metadata", {}).get("method", "gemini_llm")
        parsed_data = {
            "biomarkers": enriched_biomarkers,
            "metadata": {
                "parsing_method": parsing_method,
                "source_type": input_source,
                "parsed_at": datetime.now().isoformat(),
                "unit_validated": False,
                "unit_normalised": False,
                **result.get("metadata", {})
            }
        }
        
        # Calculate overall confidence
        biomarkers = result.get("biomarkers", [])
        if biomarkers:
            avg_confidence = sum(b.get("confidence", 0) for b in biomarkers) / len(biomarkers)
            parsed_data["metadata"]["overall_confidence"] = round(avg_confidence, 3)
        else:
            parsed_data["metadata"]["overall_confidence"] = 0.0
        
        parse_desc = "Deterministic parsing" if parsing_method == "deterministic_csv" else "LLM parsing"
        return ParseResponse(
            success=True,
            message=f"{parse_desc} completed for {input_source}{content_info}. "
                   f"Extracted {len(biomarkers)} biomarkers.",
            parsed_data=parsed_data,
            analysis_id=analysis_id,
            timestamp=datetime.now().isoformat(),
            lab_origin=lab_origin.to_dict(),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse upload: {str(e)}"
        )


@router.post("/validate")
async def validate_upload_format(
    file: Optional[UploadFile] = File(None),
    text_content: Optional[str] = Form(None)
) -> Dict[str, Any]:
    """
    Validate upload format and content (placeholder implementation).
    
    Args:
        file: Optional uploaded file
        text_content: Optional text content from form data
        
    Returns:
        Validation results
    """
    try:
        validation_results = {
            "valid": True,
            "supported_formats": ["pdf", "txt", "json", "csv"],
            "max_file_size_mb": 10,
            "detected_format": None,
            "file_size_bytes": None,
            "warnings": [],
            "errors": []
        }
        
        if file:
            validation_results["detected_format"] = file.content_type
            # Mock file size (would be actual file.size in real implementation)
            validation_results["file_size_bytes"] = 1024 * 1024  # 1MB mock
            
            if file.content_type not in ["application/pdf", "text/plain", "application/json", "text/csv"]:
                validation_results["warnings"].append(
                    f"File type {file.content_type} may not be supported"
                )
        
        elif text_content:
            validation_results["detected_format"] = "text/plain"
            validation_results["file_size_bytes"] = len(text_content.encode('utf-8'))
            
            if len(text_content) < 10:
                validation_results["errors"].append("Text content too short")
                validation_results["valid"] = False
        
        else:
            validation_results["errors"].append("No file or text content provided")
            validation_results["valid"] = False
        
        return validation_results
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to validate upload: {str(e)}"
        )
