"""
Unit tests for insight prompt templates.
"""

import pytest
from core.insights.prompts import InsightPromptTemplates, create_insight_templates
from core.models.insight import InsightTemplate


class TestInsightPromptTemplates:
    """Test insight prompt templates functionality."""
    
    def test_get_supported_categories(self):
        """Test getting all supported categories."""
        categories = InsightPromptTemplates.get_supported_categories()
        
        expected_categories = [
            "metabolic", "cardiovascular", "inflammatory", 
            "organ", "nutritional", "hormonal"
        ]
        
        assert set(categories) == set(expected_categories)
        assert len(categories) == 6
    
    def test_get_system_prompt(self):
        """Test getting system prompt."""
        system_prompt = InsightPromptTemplates.get_system_prompt()
        
        assert isinstance(system_prompt, str)
        assert len(system_prompt) > 0
        assert "clinical biomarker analysis expert" in system_prompt
        assert "insights" in system_prompt
        assert "structured" in system_prompt
    
    def test_get_template_metabolic(self):
        """Test getting metabolic template."""
        template = InsightPromptTemplates.get_template("metabolic")
        
        assert isinstance(template, str)
        assert len(template) > 0
        assert "metabolic" in template.lower()
        assert "biomarker" in template.lower()
        assert "lifestyle" in template.lower()
        assert "insulin resistance" in template.lower()
        assert "json" in template.lower()
    
    def test_get_template_cardiovascular(self):
        """Test getting cardiovascular template."""
        template = InsightPromptTemplates.get_template("cardiovascular")
        
        assert isinstance(template, str)
        assert len(template) > 0
        assert "cardiovascular" in template.lower()
        assert "cholesterol" in template.lower()
        assert "heart" in template.lower()
        assert "smoking" in template.lower()
    
    def test_get_template_inflammatory(self):
        """Test getting inflammatory template."""
        template = InsightPromptTemplates.get_template("inflammatory")
        
        assert isinstance(template, str)
        assert len(template) > 0
        assert "inflammatory" in template.lower()
        assert "inflammation" in template.lower()
        assert "crp" in template.lower()
        assert "stress" in template.lower()
    
    def test_get_template_organ(self):
        """Test getting organ template."""
        template = InsightPromptTemplates.get_template("organ")
        
        assert isinstance(template, str)
        assert len(template) > 0
        assert "organ" in template.lower()
        assert "liver" in template.lower()
        assert "kidney" in template.lower()
        assert "alcohol" in template.lower()
    
    def test_get_template_nutritional(self):
        """Test getting nutritional template."""
        template = InsightPromptTemplates.get_template("nutritional")
        
        assert isinstance(template, str)
        assert len(template) > 0
        assert "nutritional" in template.lower()
        assert "vitamin" in template.lower()
        assert "mineral" in template.lower()
        assert "deficiency" in template.lower()
    
    def test_get_template_hormonal(self):
        """Test getting hormonal template."""
        template = InsightPromptTemplates.get_template("hormonal")
        
        assert isinstance(template, str)
        assert len(template) > 0
        assert "hormonal" in template.lower()
        assert "hormone" in template.lower()
        assert "cortisol" in template.lower()
        assert "stress" in template.lower()
    
    def test_get_template_invalid_category(self):
        """Test getting template for invalid category raises error."""
        with pytest.raises(ValueError, match="Unsupported insight category"):
            InsightPromptTemplates.get_template("invalid_category")
    
    def test_format_template_basic(self):
        """Test basic template formatting."""
        biomarker_scores = {
            "glucose": 0.75,
            "hba1c": 0.68,
            "insulin": 0.82
        }
        
        lifestyle_profile = {
            "diet_level": "good",
            "exercise_minutes_per_week": 180,
            "sleep_hours": 7.5,
            "stress_level": "low",
            "smoking_status": "never",
            "alcohol_units_per_week": 3
        }
        
        clustering_results = {
            "clusters": [
                {"name": "metabolic_cluster", "biomarkers": ["glucose", "hba1c"]}
            ]
        }
        
        formatted = InsightPromptTemplates.format_template(
            category="metabolic",
            biomarker_scores=biomarker_scores,
            lifestyle_profile=lifestyle_profile,
            clustering_results=clustering_results
        )
        
        assert isinstance(formatted, str)
        assert len(formatted) > 0
        
        # Check that data was inserted
        assert "0.75" in formatted
        assert "0.68" in formatted
        assert "0.82" in formatted
        assert "good" in formatted
        assert "180" in formatted
        assert "7.5" in formatted
        assert "low" in formatted
        assert "never" in formatted
        assert "3" in formatted
        assert "metabolic_cluster" in formatted
    
    def test_format_template_missing_data(self):
        """Test template formatting with missing data uses defaults."""
        biomarker_scores = {}
        lifestyle_profile = {}
        clustering_results = {}
        
        formatted = InsightPromptTemplates.format_template(
            category="cardiovascular",
            biomarker_scores=biomarker_scores,
            lifestyle_profile=lifestyle_profile,
            clustering_results=clustering_results
        )
        
        assert isinstance(formatted, str)
        assert len(formatted) > 0
        
        # Check that defaults were used
        assert "average" in formatted  # diet_level default
        assert "150" in formatted      # exercise_minutes_per_week default
        assert "7.0" in formatted      # sleep_hours default
        assert "average" in formatted  # stress_level default
        assert "never" in formatted    # smoking_status default
        assert "5" in formatted        # alcohol_units_per_week default
    
    def test_format_template_partial_data(self):
        """Test template formatting with partial data."""
        biomarker_scores = {"glucose": 0.75}
        lifestyle_profile = {"diet_level": "excellent", "exercise_minutes_per_week": 300}
        clustering_results = {"clusters": []}
        
        formatted = InsightPromptTemplates.format_template(
            category="inflammatory",
            biomarker_scores=biomarker_scores,
            lifestyle_profile=lifestyle_profile,
            clustering_results=clustering_results
        )
        
        assert isinstance(formatted, str)
        assert len(formatted) > 0
        
        # Check that provided data was used
        assert "0.75" in formatted
        assert "excellent" in formatted
        assert "300" in formatted
        
        # Check that defaults were used for missing data
        assert "7.0" in formatted      # sleep_hours default
        assert "average" in formatted  # stress_level default
    
    def test_all_templates_have_required_structure(self):
        """Test that all templates have required structure."""
        categories = InsightPromptTemplates.get_supported_categories()
        
        for category in categories:
            template = InsightPromptTemplates.get_template(category)
            
            # Check for required placeholders
            assert "{biomarker_scores}" in template
            assert "{diet_level}" in template
            assert "{exercise_minutes_per_week}" in template
            assert "{sleep_hours}" in template
            assert "{stress_level}" in template
            assert "{clustering_results}" in template
            
            # Check for JSON structure
            assert "json" in template.lower()
            assert "insights" in template.lower()
            assert "category" in template.lower()
            assert "summary" in template.lower()
            assert "confidence" in template.lower()
            assert "severity" in template.lower()
            assert "recommendations" in template.lower()
    
    def test_template_consistency(self):
        """Test that all templates have consistent structure."""
        categories = InsightPromptTemplates.get_supported_categories()
        templates = [InsightPromptTemplates.get_template(cat) for cat in categories]
        
        # All templates should have similar length (not too different)
        lengths = [len(template) for template in templates]
        min_length = min(lengths)
        max_length = max(lengths)
        
        # Templates should be reasonably similar in length
        assert max_length - min_length < 1000  # Allow some variation
    
    def test_template_category_specific_content(self):
        """Test that templates have category-specific content."""
        # Metabolic template should mention metabolic-specific terms
        metabolic_template = InsightPromptTemplates.get_template("metabolic")
        assert "insulin" in metabolic_template.lower()
        assert "glucose" in metabolic_template.lower()
        assert "metabolic" in metabolic_template.lower()
        
        # Cardiovascular template should mention cardiovascular-specific terms
        cardio_template = InsightPromptTemplates.get_template("cardiovascular")
        assert "cholesterol" in cardio_template.lower()
        assert "heart" in cardio_template.lower()
        assert "cardiovascular" in cardio_template.lower()
        
        # Inflammatory template should mention inflammatory-specific terms
        inflammatory_template = InsightPromptTemplates.get_template("inflammatory")
        assert "inflammation" in inflammatory_template.lower()
        assert "crp" in inflammatory_template.lower()
        assert "inflammatory" in inflammatory_template.lower()


class TestCreateInsightTemplates:
    """Test creating insight template objects."""
    
    def test_create_insight_templates(self):
        """Test creating insight template objects."""
        templates = create_insight_templates()
        
        assert isinstance(templates, list)
        assert len(templates) == 6  # Should have 6 categories
        
        # Check that all templates are InsightTemplate objects
        for template in templates:
            assert isinstance(template, InsightTemplate)
            assert template.template_id.endswith("_insight_template")
            assert template.category in InsightPromptTemplates.get_supported_categories()
            assert template.is_active is True
            assert template.version == "1.0"
    
    def test_template_required_fields(self):
        """Test that all templates have required fields."""
        templates = create_insight_templates()
        
        for template in templates:
            assert template.template_id
            assert template.name
            assert template.category
            assert template.prompt_template
            assert template.required_lifestyle_factors
            assert template.output_format
            assert template.version
            assert template.is_active is not None
    
    def test_template_lifestyle_factors(self):
        """Test that templates have required lifestyle factors."""
        templates = create_insight_templates()
        
        required_factors = [
            "diet_level", "exercise_minutes_per_week", 
            "sleep_hours", "stress_level"
        ]
        
        for template in templates:
            for factor in required_factors:
                assert factor in template.required_lifestyle_factors
    
    def test_template_output_format(self):
        """Test that templates have proper output format."""
        templates = create_insight_templates()
        
        for template in templates:
            output_format = template.output_format
            assert output_format["type"] == "json"
            assert output_format["structure"] == "insights_array"
            assert "required_fields" in output_format
            assert "id" in output_format["required_fields"]
            assert "category" in output_format["required_fields"]
            assert "summary" in output_format["required_fields"]


if __name__ == "__main__":
    pytest.main([__file__])
