"""
Response parsing and validation for Gemini LLM integration.

This module provides utilities for parsing and validating responses from
the Gemini API, including JSON extraction and error handling.
"""

import json
import logging
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
from enum import Enum

from .client import GeminiResponse


class ParseError(Exception):
    """Exception raised when parsing fails."""
    pass


class ValidationError(Exception):
    """Exception raised when validation fails."""
    pass


@dataclass
class ParsedResponse:
    """Parsed response from Gemini API."""
    data: Dict[str, Any]
    success: bool
    error: Optional[str] = None
    confidence: float = 0.0


class ResponseParser:
    """Parser for Gemini API responses with validation."""
    
    def __init__(self):
        """Initialize the response parser."""
        self.logger = logging.getLogger(__name__)
    
    def parse_json_response(self, response: GeminiResponse) -> ParsedResponse:
        """
        Parse a JSON response from Gemini API.
        
        Args:
            response: GeminiResponse object
            
        Returns:
            ParsedResponse object
        """
        if not response.success:
            return ParsedResponse(
                data={},
                success=False,
                error=response.error or "Response failed"
            )
        
        try:
            # Extract JSON from response content
            content = response.content.strip()
            
            # Remove any markdown code blocks if present
            if content.startswith("```json"):
                content = content[7:]  # Remove ```json
            if content.startswith("```"):
                content = content[3:]   # Remove ```
            if content.endswith("```"):
                content = content[:-3]  # Remove trailing ```
            
            content = content.strip()
            
            # Parse JSON
            data = json.loads(content)
            
            return ParsedResponse(
                data=data,
                success=True,
                confidence=0.9  # High confidence for successful JSON parsing
            )
            
        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse JSON: {str(e)}"
            self.logger.error(error_msg)
            return ParsedResponse(
                data={},
                success=False,
                error=error_msg
            )
        except Exception as e:
            error_msg = f"Unexpected parsing error: {str(e)}"
            self.logger.error(error_msg)
            return ParsedResponse(
                data={},
                success=False,
                error=error_msg
            )
    
    def validate_biomarker_parsing_response(self, parsed_data: Dict[str, Any]) -> bool:
        """
        Validate biomarker parsing response structure.
        
        Args:
            parsed_data: Parsed response data
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["biomarkers", "extraction_notes", "confidence_score"]
        
        for field in required_fields:
            if field not in parsed_data:
                self.logger.error(f"Missing required field: {field}")
                return False
        
        # Validate biomarkers structure
        biomarkers = parsed_data.get("biomarkers", {})
        if not isinstance(biomarkers, dict):
            self.logger.error("Biomarkers must be a dictionary")
            return False
        
        # Validate each biomarker entry
        for biomarker_name, biomarker_data in biomarkers.items():
            if not isinstance(biomarker_data, dict):
                self.logger.error(f"Biomarker data for {biomarker_name} must be a dictionary")
                return False
            
            required_biomarker_fields = ["value", "unit", "confidence"]
            for field in required_biomarker_fields:
                if field not in biomarker_data:
                    self.logger.error(f"Missing biomarker field {field} for {biomarker_name}")
                    return False
            
            # Validate value is numeric
            if not isinstance(biomarker_data["value"], (int, float)):
                self.logger.error(f"Biomarker value for {biomarker_name} must be numeric")
                return False
            
            # Validate confidence is between 0 and 1
            confidence = biomarker_data["confidence"]
            if not isinstance(confidence, (int, float)) or not (0 <= confidence <= 1):
                self.logger.error(f"Biomarker confidence for {biomarker_name} must be between 0 and 1")
                return False
        
        return True
    
    def validate_insight_synthesis_response(self, parsed_data: Dict[str, Any]) -> bool:
        """
        Validate insight synthesis response structure.
        
        Args:
            parsed_data: Parsed response data
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["insights", "overall_assessment", "key_findings", "next_steps"]
        
        for field in required_fields:
            if field not in parsed_data:
                self.logger.error(f"Missing required field: {field}")
                return False
        
        # Validate insights array
        insights = parsed_data.get("insights", [])
        if not isinstance(insights, list):
            self.logger.error("Insights must be a list")
            return False
        
        # Validate each insight
        for i, insight in enumerate(insights):
            if not isinstance(insight, dict):
                self.logger.error(f"Insight {i} must be a dictionary")
                return False
            
            required_insight_fields = ["category", "title", "description", "severity", "confidence", "evidence", "recommendations"]
            for field in required_insight_fields:
                if field not in insight:
                    self.logger.error(f"Missing insight field {field} for insight {i}")
                    return False
            
            # Validate severity
            valid_severities = ["low", "moderate", "high", "critical"]
            if insight["severity"] not in valid_severities:
                self.logger.error(f"Invalid severity for insight {i}: {insight['severity']}")
                return False
            
            # Validate confidence
            confidence = insight["confidence"]
            if not isinstance(confidence, (int, float)) or not (0 <= confidence <= 1):
                self.logger.error(f"Insight confidence for insight {i} must be between 0 and 1")
                return False
        
        return True
    
    def validate_narrative_response(self, parsed_data: Dict[str, Any]) -> bool:
        """
        Validate narrative generation response structure.
        
        Args:
            parsed_data: Parsed response data
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["executive_summary", "detailed_analysis", "key_recommendations", 
                          "positive_findings", "areas_for_improvement", "next_steps"]
        
        for field in required_fields:
            if field not in parsed_data:
                self.logger.error(f"Missing required field: {field}")
                return False
        
        # Validate string fields
        string_fields = ["executive_summary", "detailed_analysis"]
        for field in string_fields:
            if not isinstance(parsed_data[field], str):
                self.logger.error(f"Field {field} must be a string")
                return False
        
        # Validate array fields
        array_fields = ["key_recommendations", "positive_findings", "areas_for_improvement", "next_steps"]
        for field in array_fields:
            if not isinstance(parsed_data[field], list):
                self.logger.error(f"Field {field} must be a list")
                return False
            
            # Check that all items are strings
            for i, item in enumerate(parsed_data[field]):
                if not isinstance(item, str):
                    self.logger.error(f"Item {i} in {field} must be a string")
                    return False
        
        return True
    
    def validate_recommendation_response(self, parsed_data: Dict[str, Any]) -> bool:
        """
        Validate recommendation generation response structure.
        
        Args:
            parsed_data: Parsed response data
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["nutrition_recommendations", "exercise_recommendations", 
                          "lifestyle_recommendations", "supplement_recommendations",
                          "monitoring_recommendations", "priority_actions", "timeline"]
        
        for field in required_fields:
            if field not in parsed_data:
                self.logger.error(f"Missing required field: {field}")
                return False
        
        # Validate recommendation arrays
        recommendation_fields = ["nutrition_recommendations", "exercise_recommendations",
                               "lifestyle_recommendations", "supplement_recommendations",
                               "monitoring_recommendations", "priority_actions"]
        
        for field in recommendation_fields:
            if not isinstance(parsed_data[field], list):
                self.logger.error(f"Field {field} must be a list")
                return False
            
            # Check that all items are strings
            for i, item in enumerate(parsed_data[field]):
                if not isinstance(item, str):
                    self.logger.error(f"Item {i} in {field} must be a string")
                    return False
        
        # Validate timeline structure
        timeline = parsed_data.get("timeline", {})
        if not isinstance(timeline, dict):
            self.logger.error("Timeline must be a dictionary")
            return False
        
        timeline_fields = ["immediate", "short_term", "long_term"]
        for field in timeline_fields:
            if field not in timeline:
                self.logger.error(f"Missing timeline field: {field}")
                return False
            
            if not isinstance(timeline[field], list):
                self.logger.error(f"Timeline field {field} must be a list")
                return False
            
            # Check that all items are strings
            for i, item in enumerate(timeline[field]):
                if not isinstance(item, str):
                    self.logger.error(f"Item {i} in timeline {field} must be a string")
                    return False
        
        return True
    
    def parse_and_validate(self, response: GeminiResponse, response_type: str) -> ParsedResponse:
        """
        Parse and validate a Gemini response based on type.
        
        Args:
            response: GeminiResponse object
            response_type: Type of response to validate
            
        Returns:
            ParsedResponse object
        """
        # Parse JSON response
        parsed = self.parse_json_response(response)
        
        if not parsed.success:
            return parsed
        
        # Validate based on response type
        validation_methods = {
            "biomarker_parsing": self.validate_biomarker_parsing_response,
            "insight_synthesis": self.validate_insight_synthesis_response,
            "narrative_generation": self.validate_narrative_response,
            "recommendation_generation": self.validate_recommendation_response
        }
        
        if response_type in validation_methods:
            is_valid = validation_methods[response_type](parsed.data)
            if not is_valid:
                return ParsedResponse(
                    data=parsed.data,
                    success=False,
                    error=f"Validation failed for {response_type}",
                    confidence=0.0
                )
        
        return parsed
