"""
Questionnaire models - immutable Pydantic v2 models for questionnaire data.

This module defines the 58-question questionnaire schema and validation logic
based on the canonical questionnaire.json file.
"""

from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, validator
from datetime import datetime, date
import json
import os


class QuestionnaireField(BaseModel):
    """Individual field within a questionnaire question."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    label: str = Field(..., description="Field label")
    type: str = Field(..., description="Field type (number, text, etc.)")
    min: Optional[Union[int, float]] = Field(default=None, description="Minimum value")
    max: Optional[Union[int, float]] = Field(default=None, description="Maximum value")


class AlternativeUnit(BaseModel):
    """Alternative unit specification for a question."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    label: str = Field(..., description="Alternative unit label")
    type: str = Field(..., description="Alternative unit type")
    min: Optional[Union[int, float]] = Field(default=None, description="Minimum value")
    max: Optional[Union[int, float]] = Field(default=None, description="Maximum value")


class QuestionnaireQuestion(BaseModel):
    """Immutable questionnaire question definition."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    id: str = Field(..., description="Unique question identifier (semantic ID)")
    section: str = Field(..., description="Question section for grouping")
    question: str = Field(..., description="Question text")
    type: str = Field(..., description="Question type (text, dropdown, number, etc.)")
    required: bool = Field(default=False, description="Whether question is required")
    options: Optional[List[str]] = Field(default=None, description="Options for dropdown questions")
    fields: Optional[List[QuestionnaireField]] = Field(default=None, description="Fields for group questions")
    alternativeUnit: Optional[AlternativeUnit] = Field(default=None, description="Alternative unit specification")
    label: Optional[str] = Field(default=None, description="Question label")
    min: Optional[Union[int, float]] = Field(default=None, description="Minimum value for number questions")
    max: Optional[Union[int, float]] = Field(default=None, description="Maximum value for number questions")
    helpText: Optional[str] = Field(default=None, description="Help text for the question")
    allowOther: Optional[bool] = Field(default=None, description="Whether to allow 'Other' option")
    labels: Optional[Dict[str, str]] = Field(default=None, description="Labels for slider questions")
    conditionalDisplay: Optional[Dict[str, Any]] = Field(default=None, description="Conditional display logic")


class QuestionnaireSchema(BaseModel):
    """Immutable questionnaire schema containing all questions."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    questions: List[QuestionnaireQuestion] = Field(..., description="List of questionnaire questions")
    version: str = Field(default="1.0", description="Schema version")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Schema creation timestamp")


class QuestionnaireResponse(BaseModel):
    """Immutable questionnaire response for a single question."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    question_id: str = Field(..., description="Question identifier")
    value: Any = Field(..., description="Response value")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Response timestamp")


class QuestionnaireSubmission(BaseModel):
    """Immutable complete questionnaire submission."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    responses: Dict[str, Any] = Field(..., description="Map of question_id to response value")
    user_id: Optional[str] = Field(default=None, description="User identifier")
    submission_id: str = Field(..., description="Unique submission identifier")
    completed_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Submission completion timestamp")
    version: str = Field(default="1.0", description="Questionnaire version used")


class QuestionnaireValidator:
    """Validator for questionnaire responses."""
    
    def __init__(self, schema: QuestionnaireSchema):
        """
        Initialize validator with questionnaire schema.
        
        Args:
            schema: Questionnaire schema to validate against
        """
        self.schema = schema
        self._question_map = {q.id: q for q in schema.questions}
    
    def validate_response(self, question_id: str, value: Any) -> tuple[bool, Optional[str]]:
        """
        Validate a single response.
        
        Args:
            question_id: Question identifier
            value: Response value to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if question_id not in self._question_map:
            return False, f"Unknown question ID: {question_id}"
        
        question = self._question_map[question_id]
        
        # Check required fields
        if question.required and (value is None or value == ""):
            return False, f"Required question {question_id} is missing"
        
        # Skip validation for empty optional fields
        if not question.required and (value is None or value == ""):
            return True, None
        
        # Type-specific validation
        if question.type == "number":
            if not isinstance(value, (int, float)):
                return False, f"Question {question_id} expects a number"
            if question.min is not None and value < question.min:
                return False, f"Question {question_id} value {value} is below minimum {question.min}"
            if question.max is not None and value > question.max:
                return False, f"Question {question_id} value {value} is above maximum {question.max}"
        
        elif question.type == "dropdown":
            if question.options and value not in question.options:
                return False, f"Question {question_id} value {value} is not in options {question.options}"
        
        elif question.type == "email":
            if not isinstance(value, str) or "@" not in value:
                return False, f"Question {question_id} expects a valid email address"
        
        elif question.type == "date":
            if not isinstance(value, str):
                return False, f"Question {question_id} expects a date string"
            try:
                datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError:
                return False, f"Question {question_id} expects a valid date format"
        
        elif question.type == "group":
            if not isinstance(value, dict):
                return False, f"Question {question_id} expects a dictionary for group type"
            if question.fields:
                for field in question.fields:
                    if field.label in value:
                        field_value = value[field.label]
                        if field.type == "number":
                            if not isinstance(field_value, (int, float)):
                                return False, f"Field {field.label} expects a number"
                            if field.min is not None and field_value < field.min:
                                return False, f"Field {field.label} value {field_value} is below minimum {field.min}"
                            if field.max is not None and field_value > field.max:
                                return False, f"Field {field.label} value {field_value} is above maximum {field.max}"
        
        return True, None
    
    def validate_submission(self, submission: QuestionnaireSubmission) -> tuple[bool, List[str]]:
        """
        Validate a complete questionnaire submission.
        
        Args:
            submission: Questionnaire submission to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check all required questions are answered
        for question in self.schema.questions:
            if question.required and question.id not in submission.responses:
                errors.append(f"Required question {question.id} is missing")
        
        # Validate all responses
        for question_id, value in submission.responses.items():
            is_valid, error = self.validate_response(question_id, value)
            if not is_valid:
                errors.append(error)
        
        return len(errors) == 0, errors


def load_questionnaire_schema() -> QuestionnaireSchema:
    """
    Load questionnaire schema from canonical JSON file.
    
    Returns:
        QuestionnaireSchema object
    """
    # Get the path to the questionnaire.json file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    questionnaire_path = os.path.join(current_dir, "..", "..", "ssot", "questionnaire.json")
    
    with open(questionnaire_path, 'r', encoding='utf-8') as f:
        questions_data = json.load(f)
    
    # Convert to QuestionnaireQuestion objects
    questions = []
    for q_data in questions_data:
        # Handle fields
        fields = None
        if "fields" in q_data:
            fields = [QuestionnaireField(**field) for field in q_data["fields"]]
        
        # Handle alternativeUnit
        alternative_unit = None
        if "alternativeUnit" in q_data:
            alternative_unit = AlternativeUnit(**q_data["alternativeUnit"])
        
        question = QuestionnaireQuestion(
            id=q_data["id"],
            section=q_data["section"],
            question=q_data["question"],
            type=q_data["type"],
            required=q_data.get("required", False),
            options=q_data.get("options"),
            fields=fields,
            alternativeUnit=alternative_unit,
            label=q_data.get("label"),
            min=q_data.get("min"),
            max=q_data.get("max"),
            helpText=q_data.get("helpText"),
            allowOther=q_data.get("allowOther"),
            labels=q_data.get("labels"),
            conditionalDisplay=q_data.get("conditionalDisplay")
        )
        questions.append(question)
    
    return QuestionnaireSchema(questions=questions)


def create_questionnaire_validator() -> QuestionnaireValidator:
    """
    Create a questionnaire validator with the canonical schema.
    
    Returns:
        QuestionnaireValidator instance
    """
    schema = load_questionnaire_schema()
    return QuestionnaireValidator(schema)
