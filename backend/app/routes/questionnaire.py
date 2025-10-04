"""
Questionnaire API routes - handles questionnaire schema and related operations.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import json
import os
from pathlib import Path

router = APIRouter()


@router.get("/schema")
async def get_questionnaire_schema() -> Dict[str, Any]:
    """
    Get the canonical questionnaire schema.
    
    Returns:
        The 58-question questionnaire schema from SSOT
    """
    try:
        # Load questionnaire schema from SSOT
        schema_path = Path(__file__).parent.parent.parent / "ssot" / "questionnaire.json"
        
        if not schema_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Questionnaire schema not found"
            )
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        return {
            "schema": schema,
            "total_questions": len(schema),
            "version": "1.0",
            "description": "Canonical 58-question HealthIQ questionnaire schema"
        }
        
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid questionnaire schema format: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load questionnaire schema: {str(e)}"
        )


@router.get("/schema/validation")
async def validate_questionnaire_schema() -> Dict[str, Any]:
    """
    Validate the questionnaire schema structure.
    
    Returns:
        Validation results for the questionnaire schema
    """
    try:
        # Load and validate schema
        schema_path = Path(__file__).parent.parent.parent / "ssot" / "questionnaire.json"
        
        if not schema_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Questionnaire schema not found"
            )
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        # Basic validation
        validation_results = {
            "valid": True,
            "total_questions": len(schema),
            "required_fields": ["id", "section", "question", "type", "required"],
            "sections": [],
            "question_types": [],
            "errors": []
        }
        
        # Extract unique sections and question types
        sections = set()
        question_types = set()
        
        for i, question in enumerate(schema):
            # Check required fields
            for field in validation_results["required_fields"]:
                if field not in question:
                    validation_results["errors"].append(
                        f"Question {i+1}: Missing required field '{field}'"
                    )
                    validation_results["valid"] = False
            
            # Extract sections and types
            if "section" in question:
                sections.add(question["section"])
            if "type" in question:
                question_types.add(question["type"])
        
        validation_results["sections"] = sorted(list(sections))
        validation_results["question_types"] = sorted(list(question_types))
        
        return validation_results
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to validate questionnaire schema: {str(e)}"
        )
