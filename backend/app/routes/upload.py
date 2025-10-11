"""
Upload API routes - handles file uploads and parsing operations.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Dict, Any, Optional
from pydantic import BaseModel
import json
from datetime import datetime
from services.parsing.llm_parser import LLMParser

router = APIRouter()


class ParseResponse(BaseModel):
    """Response model for upload parsing."""
    success: bool
    message: str
    parsed_data: Optional[Dict[str, Any]] = None
    analysis_id: Optional[str] = None
    timestamp: str


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
        if file:
            # Read file bytes
            file_bytes = await file.read()
            filename = file.filename or "unknown"
            content_type = file.content_type
            
            # Extract biomarkers using LLM
            result = await parser.extract_biomarkers(file_bytes, filename, content_type)
            
            input_source = "file_upload"
            content_info = f" (filename: {filename}, content_type: {content_type})"
            
        elif text_content:
            # Convert text content to bytes for processing
            file_bytes = text_content.encode('utf-8')
            filename = "text_input"
            
            # Extract biomarkers using LLM
            result = await parser.extract_biomarkers(file_bytes, filename, "text/plain")
            
            input_source = "text_input"
            content_info = f" (text length: {len(text_content)} characters)"
            
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
                timestamp=datetime.now().isoformat()
            )
        
        # Format response data
        parsed_data = {
            "biomarkers": result.get("biomarkers", []),
            "metadata": {
                "parsing_method": "gemini_llm",
                "source_type": input_source,
                "parsed_at": datetime.now().isoformat(),
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
        
        return ParseResponse(
            success=True,
            message=f"LLM parsing completed for {input_source}{content_info}. "
                   f"Extracted {len(biomarkers)} biomarkers.",
            parsed_data=parsed_data,
            analysis_id=analysis_id,
            timestamp=datetime.now().isoformat()
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
