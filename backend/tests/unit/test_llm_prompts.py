"""
Unit tests for LLM prompt templates.
"""

import pytest
from core.llm.prompts import PromptTemplates, PromptType, PromptTemplate


class TestPromptTemplates:
    """Test cases for PromptTemplates."""
    
    def test_get_biomarker_parsing_prompt(self):
        """Test biomarker parsing prompt template."""
        template = PromptTemplates.get_biomarker_parsing_prompt()
        
        assert isinstance(template, PromptTemplate)
        assert template.name == "biomarker_parsing"
        assert "biomarker" in template.template.lower()
        assert "text_content" in template.variables
        assert "canonical_biomarkers" in template.variables
        assert "biomarkers" in template.output_schema["properties"]
    
    def test_get_insight_synthesis_prompt(self):
        """Test insight synthesis prompt template."""
        template = PromptTemplates.get_insight_synthesis_prompt()
        
        assert isinstance(template, PromptTemplate)
        assert template.name == "insight_synthesis"
        assert "insight" in template.template.lower()
        assert "biomarker_data" in template.variables
        assert "scoring_results" in template.variables
        assert "insights" in template.output_schema["properties"]
    
    def test_get_narrative_generation_prompt(self):
        """Test narrative generation prompt template."""
        template = PromptTemplates.get_narrative_generation_prompt()
        
        assert isinstance(template, PromptTemplate)
        assert template.name == "narrative_generation"
        assert "narrative" in template.template.lower()
        assert "analysis_results" in template.variables
        assert "user_profile" in template.variables
        assert "executive_summary" in template.output_schema["properties"]
    
    def test_get_recommendation_generation_prompt(self):
        """Test recommendation generation prompt template."""
        template = PromptTemplates.get_recommendation_generation_prompt()
        
        assert isinstance(template, PromptTemplate)
        assert template.name == "recommendation_generation"
        assert "recommendation" in template.template.lower()
        assert "biomarker_analysis" in template.variables
        assert "lifestyle_factors" in template.variables
        assert "nutrition_recommendations" in template.output_schema["properties"]
    
    def test_get_template_by_type(self):
        """Test getting template by type."""
        # Test biomarker parsing
        template = PromptTemplates.get_template(PromptType.BIOMARKER_PARSING)
        assert template.name == "biomarker_parsing"
        
        # Test insight synthesis
        template = PromptTemplates.get_template(PromptType.INSIGHT_SYNTHESIS)
        assert template.name == "insight_synthesis"
        
        # Test narrative generation
        template = PromptTemplates.get_template(PromptType.NARRATIVE_GENERATION)
        assert template.name == "narrative_generation"
        
        # Test recommendation generation
        template = PromptTemplates.get_template(PromptType.RECOMMENDATION_GENERATION)
        assert template.name == "recommendation_generation"
    
    def test_get_template_invalid_type(self):
        """Test getting template with invalid type raises error."""
        with pytest.raises(ValueError, match="Unknown prompt type"):
            PromptTemplates.get_template("invalid_type")
    
    def test_format_prompt_biomarker_parsing(self):
        """Test formatting biomarker parsing prompt."""
        prompt = PromptTemplates.format_prompt(
            PromptType.BIOMARKER_PARSING,
            text_content="Test text",
            canonical_biomarkers="glucose, cholesterol"
        )
        
        assert "Test text" in prompt
        assert "glucose, cholesterol" in prompt
        assert "biomarker" in prompt.lower()
    
    def test_format_prompt_insight_synthesis(self):
        """Test formatting insight synthesis prompt."""
        prompt = PromptTemplates.format_prompt(
            PromptType.INSIGHT_SYNTHESIS,
            biomarker_data="Test data",
            scoring_results="Test results",
            clustering_results="Test clusters",
            user_profile="Test profile"
        )
        
        assert "Test data" in prompt
        assert "Test results" in prompt
        assert "Test clusters" in prompt
        assert "Test profile" in prompt
        assert "insight" in prompt.lower()
    
    def test_format_prompt_narrative_generation(self):
        """Test formatting narrative generation prompt."""
        prompt = PromptTemplates.format_prompt(
            PromptType.NARRATIVE_GENERATION,
            analysis_results="Test results",
            user_profile="Test profile"
        )
        
        assert "Test results" in prompt
        assert "Test profile" in prompt
        assert "narrative" in prompt.lower()
    
    def test_format_prompt_recommendation_generation(self):
        """Test formatting recommendation generation prompt."""
        prompt = PromptTemplates.format_prompt(
            PromptType.RECOMMENDATION_GENERATION,
            biomarker_analysis="Test analysis",
            user_profile="Test profile",
            lifestyle_factors="Test factors"
        )
        
        assert "Test analysis" in prompt
        assert "Test profile" in prompt
        assert "Test factors" in prompt
        assert "recommendation" in prompt.lower()
    
    def test_format_prompt_missing_variables(self):
        """Test formatting prompt with missing variables raises error."""
        with pytest.raises(KeyError):
            PromptTemplates.format_prompt(
                PromptType.BIOMARKER_PARSING,
                text_content="Test text"
                # Missing canonical_biomarkers
            )
    
    def test_biomarker_parsing_output_schema(self):
        """Test biomarker parsing output schema structure."""
        template = PromptTemplates.get_biomarker_parsing_prompt()
        schema = template.output_schema
        
        # Check required fields
        assert "biomarkers" in schema["properties"]
        assert "extraction_notes" in schema["properties"]
        assert "confidence_score" in schema["properties"]
        
        # Check biomarkers structure
        biomarkers_schema = schema["properties"]["biomarkers"]
        assert biomarkers_schema["type"] == "object"
        assert "additionalProperties" in biomarkers_schema
        
        # Check biomarker entry structure
        biomarker_entry = biomarkers_schema["additionalProperties"]
        assert "value" in biomarker_entry["properties"]
        assert "unit" in biomarker_entry["properties"]
        assert "confidence" in biomarker_entry["properties"]
    
    def test_insight_synthesis_output_schema(self):
        """Test insight synthesis output schema structure."""
        template = PromptTemplates.get_insight_synthesis_prompt()
        schema = template.output_schema
        
        # Check required fields
        assert "insights" in schema["properties"]
        assert "overall_assessment" in schema["properties"]
        assert "key_findings" in schema["properties"]
        assert "next_steps" in schema["properties"]
        
        # Check insights array structure
        insights_schema = schema["properties"]["insights"]
        assert insights_schema["type"] == "array"
        
        # Check insight item structure
        insight_item = insights_schema["items"]
        assert "category" in insight_item["properties"]
        assert "title" in insight_item["properties"]
        assert "description" in insight_item["properties"]
        assert "severity" in insight_item["properties"]
        assert "confidence" in insight_item["properties"]
        assert "evidence" in insight_item["properties"]
        assert "recommendations" in insight_item["properties"]
        
        # Check severity enum
        severity_enum = insight_item["properties"]["severity"]["enum"]
        assert "low" in severity_enum
        assert "moderate" in severity_enum
        assert "high" in severity_enum
        assert "critical" in severity_enum
    
    def test_narrative_generation_output_schema(self):
        """Test narrative generation output schema structure."""
        template = PromptTemplates.get_narrative_generation_prompt()
        schema = template.output_schema
        
        # Check required fields
        assert "executive_summary" in schema["properties"]
        assert "detailed_analysis" in schema["properties"]
        assert "key_recommendations" in schema["properties"]
        assert "positive_findings" in schema["properties"]
        assert "areas_for_improvement" in schema["properties"]
        assert "next_steps" in schema["properties"]
        
        # Check array fields
        array_fields = ["key_recommendations", "positive_findings", "areas_for_improvement", "next_steps"]
        for field in array_fields:
            assert schema["properties"][field]["type"] == "array"
            assert schema["properties"][field]["items"]["type"] == "string"
    
    def test_recommendation_generation_output_schema(self):
        """Test recommendation generation output schema structure."""
        template = PromptTemplates.get_recommendation_generation_prompt()
        schema = template.output_schema
        
        # Check required fields
        assert "nutrition_recommendations" in schema["properties"]
        assert "exercise_recommendations" in schema["properties"]
        assert "lifestyle_recommendations" in schema["properties"]
        assert "supplement_recommendations" in schema["properties"]
        assert "monitoring_recommendations" in schema["properties"]
        assert "priority_actions" in schema["properties"]
        assert "timeline" in schema["properties"]
        
        # Check timeline structure
        timeline_schema = schema["properties"]["timeline"]
        assert "immediate" in timeline_schema["properties"]
        assert "short_term" in timeline_schema["properties"]
        assert "long_term" in timeline_schema["properties"]
        
        # Check timeline array types
        for period in ["immediate", "short_term", "long_term"]:
            assert timeline_schema["properties"][period]["type"] == "array"
            assert timeline_schema["properties"][period]["items"]["type"] == "string"
