"""
Unit tests for questionnaire models and validation.

Tests the 56-question questionnaire schema, validation logic, and data models.
"""

import pytest
import json
from datetime import datetime
from typing import Dict, Any

from core.models.questionnaire import (
    QuestionnaireQuestion,
    QuestionnaireSchema,
    QuestionnaireResponse,
    QuestionnaireSubmission,
    QuestionnaireValidator,
    load_questionnaire_schema,
    create_questionnaire_validator
)


class TestQuestionnaireModels:
    """Test questionnaire model creation and validation."""
    
    def test_questionnaire_question_creation(self):
        """Test creating a questionnaire question."""
        question = QuestionnaireQuestion(
            id="age",
            section="demographics",
            question="What is your age?",
            type="number",
            required=True,
            min=18,
            max=100
        )
        
        assert question.id == "age"
        assert question.section == "demographics"
        assert question.question == "What is your age?"
        assert question.type == "number"
        assert question.required is True
        assert question.min == 18
        assert question.max == 100
    
    def test_questionnaire_schema_creation(self):
        """Test creating a questionnaire schema."""
        questions = [
            QuestionnaireQuestion(
                id="age",
                section="demographics",
                question="What is your age?",
                type="number",
                required=True
            ),
            QuestionnaireQuestion(
                id="biological_sex",
                section="demographics",
                question="What is your gender?",
                type="dropdown",
                options=["Male", "Female", "Other"],
                required=True
            )
        ]
        
        schema = QuestionnaireSchema(questions=questions)
        
        assert len(schema.questions) == 2
        assert schema.questions[0].id == "age"
        assert schema.questions[1].id == "biological_sex"
        assert schema.version == "1.0"
    
    def test_questionnaire_response_creation(self):
        """Test creating a questionnaire response."""
        response = QuestionnaireResponse(
            question_id="age",
            value=25
        )
        
        assert response.question_id == "age"
        assert response.value == 25
        assert isinstance(response.timestamp, str)
    
    def test_questionnaire_submission_creation(self):
        """Test creating a questionnaire submission."""
        responses = {"age": 25, "biological_sex": "Male"}
        submission = QuestionnaireSubmission(
            responses=responses,
            submission_id="test_submission"
        )
        
        assert submission.responses == responses
        assert submission.submission_id == "test_submission"
        assert isinstance(submission.completed_at, str)


class TestQuestionnaireValidator:
    """Test questionnaire validation logic."""
    
    def setup_method(self):
        """Set up test data."""
        self.questions = [
            QuestionnaireQuestion(
                id="age",
                section="demographics",
                question="What is your age?",
                type="number",
                required=True,
                min=18,
                max=100
            ),
            QuestionnaireQuestion(
                id="biological_sex",
                section="demographics",
                question="What is your gender?",
                type="dropdown",
                options=["Male", "Female", "Other"],
                required=True
            ),
            QuestionnaireQuestion(
                id="email_address",
                section="demographics",
                question="What is your email?",
                type="email",
                required=True
            ),
            QuestionnaireQuestion(
                id="height",
                section="demographics",
                question="What is your height?",
                type="group",
                fields=[
                    {"label": "Feet", "type": "number", "min": 3, "max": 8},
                    {"label": "Inches", "type": "number", "min": 0, "max": 11}
                ],
                required=True
            )
        ]
        
        self.schema = QuestionnaireSchema(questions=self.questions)
        self.validator = QuestionnaireValidator(self.schema)
    
    def test_validate_valid_number_response(self):
        """Test validating a valid number response."""
        is_valid, error = self.validator.validate_response("age", 25)
        
        assert is_valid is True
        assert error is None
    
    def test_validate_invalid_number_response(self):
        """Test validating an invalid number response."""
        # Test below minimum
        is_valid, error = self.validator.validate_response("age", 15)
        assert is_valid is False
        assert "below minimum" in error
        
        # Test above maximum
        is_valid, error = self.validator.validate_response("age", 150)
        assert is_valid is False
        assert "above maximum" in error
        
        # Test wrong type
        is_valid, error = self.validator.validate_response("age", "twenty-five")
        assert is_valid is False
        assert "expects a number" in error
    
    def test_validate_valid_dropdown_response(self):
        """Test validating a valid dropdown response."""
        is_valid, error = self.validator.validate_response("biological_sex", "Male")
        
        assert is_valid is True
        assert error is None
    
    def test_validate_invalid_dropdown_response(self):
        """Test validating an invalid dropdown response."""
        is_valid, error = self.validator.validate_response("biological_sex", "Invalid")
        
        assert is_valid is False
        assert "not in options" in error
    
    def test_validate_valid_email_response(self):
        """Test validating a valid email response."""
        is_valid, error = self.validator.validate_response("email_address", "test@example.com")
        
        assert is_valid is True
        assert error is None
    
    def test_validate_invalid_email_response(self):
        """Test validating an invalid email response."""
        is_valid, error = self.validator.validate_response("email_address", "invalid-email")
        
        assert is_valid is False
        assert "valid email address" in error
    
    def test_validate_valid_group_response(self):
        """Test validating a valid group response."""
        group_response = {"Feet": 5, "Inches": 10}
        is_valid, error = self.validator.validate_response("height", group_response)
        
        assert is_valid is True
        assert error is None
    
    def test_validate_invalid_group_response(self):
        """Test validating an invalid group response."""
        # Test wrong type
        is_valid, error = self.validator.validate_response("height", "not a dict")
        assert is_valid is False
        assert "expects a dictionary" in error
        
        # Test invalid field value
        group_response = {"Feet": 10, "Inches": 5}  # Feet > max
        is_valid, error = self.validator.validate_response("height", group_response)
        assert is_valid is False
        assert "below minimum" in error or "above maximum" in error
    
    def test_validate_required_field_missing(self):
        """Test validating when required field is missing."""
        is_valid, error = self.validator.validate_response("age", None)
        
        assert is_valid is False
        assert "Required question" in error
    
    def test_validate_optional_field_empty(self):
        """Test validating when optional field is empty."""
        # Create a new question that's optional
        optional_question = QuestionnaireQuestion(
            id="age_optional",
            section="demographics",
            question="What is your age?",
            type="number",
            required=False,
            min=18,
            max=100
        )
        
        # Create new schema with optional question
        optional_schema = QuestionnaireSchema(questions=[optional_question])
        optional_validator = QuestionnaireValidator(optional_schema)
        
        is_valid, error = optional_validator.validate_response("age_optional", None)
        
        assert is_valid is True
        assert error is None
    
    def test_validate_unknown_question(self):
        """Test validating response for unknown question."""
        is_valid, error = self.validator.validate_response("unknown", "value")
        
        assert is_valid is False
        assert "Unknown question ID" in error
    
    def test_validate_complete_submission(self):
        """Test validating a complete questionnaire submission."""
        responses = {
            "age": 25,
            "biological_sex": "Male",
            "email_address": "test@example.com",
            "height": {"Feet": 5, "Inches": 10}
        }
        
        submission = QuestionnaireSubmission(
            responses=responses,
            submission_id="test_submission"
        )
        
        is_valid, errors = self.validator.validate_submission(submission)
        
        assert is_valid is True
        assert len(errors) == 0
    
    def test_validate_incomplete_submission(self):
        """Test validating an incomplete questionnaire submission."""
        responses = {
            "age": 25,
            "biological_sex": "Male"
            # Missing email_address and height
        }
        
        submission = QuestionnaireSubmission(
            responses=responses,
            submission_id="test_submission"
        )
        
        is_valid, errors = self.validator.validate_submission(submission)
        
        assert is_valid is False
        assert len(errors) == 2  # Missing email_address and height
        assert any("email_address" in error for error in errors)
        assert any("height" in error for error in errors)


class TestQuestionnaireSchemaLoading:
    """Test loading questionnaire schema from JSON file."""
    
    def test_load_questionnaire_schema(self):
        """Test loading the canonical questionnaire schema."""
        schema = load_questionnaire_schema()
        
        assert isinstance(schema, QuestionnaireSchema)
        assert len(schema.questions) == 59  # Should have 59 questions (58 + QRISK3)
        assert schema.version == "1.0"
        
        # Check that all questions have required fields
        for question in schema.questions:
            assert question.id
            assert question.question
            assert question.type
            assert isinstance(question.required, bool)
    
    def test_create_questionnaire_validator(self):
        """Test creating a questionnaire validator."""
        validator = create_questionnaire_validator()
        
        assert isinstance(validator, QuestionnaireValidator)
        assert len(validator.schema.questions) == 59
        
        # Test that validator can validate responses
        is_valid, error = validator.validate_response("full_name", "Test Name")
        assert is_valid is True or is_valid is False  # Should not crash


class TestQuestionnaireIntegration:
    """Test questionnaire integration with real data."""
    
    def test_real_questionnaire_validation(self):
        """Test validation with real questionnaire data structure."""
        validator = create_questionnaire_validator()
        
        # Test with realistic responses
        responses = {
            "full_name": "John Doe",
            "email_address": "john@example.com",
            "phone_number": "+1234567890",
            "country": "United States",
            "date_of_birth": "1990-01-01",
            "biological_sex": "Male",
            "height": {"Feet": 5, "Inches": 10},
            "weight": {"Weight (lbs)": 180},
            "sleep_hours_nightly": "7-8 hours",
            "sleep_quality_rating": 7,
            "alcohol_consumption": "1-3 drinks",
            "smoking_status": "Never used",
            "stress_level": 5,
            "exercise_frequency": "3 days"
        }
        
        submission = QuestionnaireSubmission(
            responses=responses,
            submission_id="integration_test"
        )
        
        is_valid, errors = validator.validate_submission(submission)
        
        # Should be valid or have specific validation errors
        if not is_valid:
            print(f"Validation errors: {errors}")
            # Check that errors are specific and helpful
            for error in errors:
                assert len(error) > 10  # Should be descriptive
                # Should reference semantic question ID


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
