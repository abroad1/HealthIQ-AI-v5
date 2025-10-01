"""
Unit tests for insight synthesis engine.
"""

import pytest
from datetime import datetime, UTC
from typing import Dict, Any, List

from core.insights.synthesis import InsightSynthesizer, MockLLMClient, LLMClient
from core.insights.prompts import InsightPromptTemplates
from core.models.context import AnalysisContext
from core.models.user import User
from core.models.biomarker import BiomarkerPanel, BiomarkerValue
from core.models.insight import Insight, InsightSynthesisResult, InsightGenerationRequest


class TestMockLLMClient:
    """Test the mock LLM client."""
    
    def test_mock_llm_client_initialization(self):
        """Test mock LLM client initializes correctly."""
        client = MockLLMClient()
        # MockLLMClient no longer tracks call count for determinism
    
    def test_mock_llm_client_generate_insights(self):
        """Test mock LLM client generates insights."""
        client = MockLLMClient()
        
        # Test generate_insights method
        response = client.generate_insights(
            system_prompt="Test system prompt",
            user_prompt="Test user prompt metabolic",
            category="metabolic"
        )
        
        assert "text" in response
        assert "candidates" in response
        assert "model" in response
        assert response["model"] == "mock-llm-client"
    
    def test_mock_llm_client_generate_method(self):
        """Test mock LLM client generate method."""
        client = MockLLMClient()
        
        # Test generate method
        response = client.generate(
            prompt="Test system prompt\n\nTest user prompt metabolic"
        )
        
        assert "text" in response
        assert "candidates" in response
        assert "model" in response
        assert response["model"] == "mock-llm-client"
    
    def test_mock_llm_client_deterministic_responses(self):
        """Test mock LLM client returns deterministic responses."""
        client = MockLLMClient()
        
        # Generate same category multiple times
        response1 = client.generate("cardiovascular test prompt")
        response2 = client.generate("cardiovascular test prompt")
        
        # Should have same structure and deterministic responses
        assert response1["model"] == response2["model"]
        assert response1["text"] == response2["text"]
        # Responses should be identical since they use the same prompt
    
    def test_mock_llm_client_unsupported_category(self):
        """Test mock LLM client handles unsupported categories."""
        client = MockLLMClient()
        
        response = client.generate("unsupported_category test prompt")
        assert "text" in response
        assert "candidates" in response
        assert "model" in response


class TestInsightPromptTemplates:
    """Test insight prompt templates."""
    
    def test_get_supported_categories(self):
        """Test getting supported categories."""
        categories = InsightPromptTemplates.get_supported_categories()
        expected_categories = ["metabolic", "cardiovascular", "inflammatory", "organ", "nutritional", "hormonal"]
        
        assert set(categories) == set(expected_categories)
    
    def test_get_template_valid_category(self):
        """Test getting template for valid category."""
        template = InsightPromptTemplates.get_template("metabolic")
        assert "metabolic" in template.lower()
        assert "biomarker" in template.lower()
        assert "lifestyle" in template.lower()
    
    def test_get_template_invalid_category(self):
        """Test getting template for invalid category raises error."""
        with pytest.raises(ValueError, match="Unsupported insight category"):
            InsightPromptTemplates.get_template("invalid_category")
    
    def test_get_system_prompt(self):
        """Test getting system prompt."""
        system_prompt = InsightPromptTemplates.get_system_prompt()
        assert "clinical biomarker analysis expert" in system_prompt
        assert "insights" in system_prompt
    
    def test_format_template(self):
        """Test formatting template with data."""
        biomarker_scores = {"glucose": 0.75, "hba1c": 0.68}
        lifestyle_profile = {"diet_level": "good", "exercise_minutes_per_week": 180}
        clustering_results = {"clusters": []}
        
        formatted = InsightPromptTemplates.format_template(
            category="metabolic",
            biomarker_scores=biomarker_scores,
            lifestyle_profile=lifestyle_profile,
            clustering_results=clustering_results
        )
        
        assert "good" in formatted
        assert "180" in formatted
        assert "0.75" in formatted


class TestInsightSynthesizer:
    """Test the insight synthesizer."""
    
    @pytest.fixture
    def mock_context(self):
        """Create a mock analysis context."""
        user = User(
            user_id="test_user",
            age=35,
            gender="male",
            lifestyle_factors={"diet_level": "good", "exercise_minutes_per_week": 150}
        )
        
        biomarker_panel = BiomarkerPanel(
            biomarkers={
                "glucose": BiomarkerValue(name="glucose", value=95, unit="mg/dL"),
                "hba1c": BiomarkerValue(name="hba1c", value=5.2, unit="%")
            }
        )
        
        return AnalysisContext(
            analysis_id="test_analysis",
            user=user,
            biomarker_panel=biomarker_panel,
            created_at=datetime.now(UTC).isoformat()
        )
    
    @pytest.fixture
    def synthesizer(self):
        """Create insight synthesizer with mock client."""
        return InsightSynthesizer()
    
    def test_synthesizer_initialization(self, synthesizer):
        """Test synthesizer initializes correctly."""
        assert synthesizer.llm_client is not None
        # Should be either GeminiClient or MockLLMClient depending on configuration
        from core.llm.gemini_client import GeminiClient
        from core.insights.synthesis import MockLLMClient
        assert isinstance(synthesizer.llm_client, (GeminiClient, MockLLMClient))
        assert synthesizer.prompt_templates is not None
    
    def test_synthesize_insights_basic(self, synthesizer, mock_context):
        """Test basic insight synthesis."""
        biomarker_scores = {
            "overall_score": 0.75,
            "health_system_scores": {
                "metabolic": {"overall_score": 0.70, "biomarker_scores": []}
            }
        }
        
        clustering_results = {"clusters": []}
        lifestyle_profile = {"diet_level": "good", "exercise_minutes_per_week": 150}
        
        result = synthesizer.synthesize_insights(
            context=mock_context,
            biomarker_scores=biomarker_scores,
            clustering_results=clustering_results,
            lifestyle_profile=lifestyle_profile,
            requested_categories=["metabolic"],
            max_insights_per_category=2
        )
        
        assert isinstance(result, InsightSynthesisResult)
        assert result.analysis_id == "test_analysis"
        assert result.total_insights > 0
        assert "metabolic" in result.categories_covered
        assert result.overall_confidence > 0
    
    def test_synthesize_insights_multiple_categories(self, synthesizer, mock_context):
        """Test insight synthesis for multiple categories."""
        biomarker_scores = {"overall_score": 0.75, "health_system_scores": {}}
        clustering_results = {"clusters": []}
        lifestyle_profile = {"diet_level": "good"}
        
        result = synthesizer.synthesize_insights(
            context=mock_context,
            biomarker_scores=biomarker_scores,
            clustering_results=clustering_results,
            lifestyle_profile=lifestyle_profile,
            requested_categories=["metabolic", "cardiovascular"],
            max_insights_per_category=1
        )
        
        assert result.total_insights >= 2
        assert len(result.categories_covered) >= 2
    
    def test_synthesize_insights_no_categories(self, synthesizer, mock_context):
        """Test insight synthesis with no specific categories."""
        biomarker_scores = {"overall_score": 0.75, "health_system_scores": {}}
        clustering_results = {"clusters": []}
        lifestyle_profile = {"diet_level": "good"}
        
        result = synthesizer.synthesize_insights(
            context=mock_context,
            biomarker_scores=biomarker_scores,
            clustering_results=clustering_results,
            lifestyle_profile=lifestyle_profile
        )
        
        assert result.total_insights > 0
        assert len(result.categories_covered) > 0
    
    def test_synthesize_insights_error_handling(self, synthesizer, mock_context):
        """Test insight synthesis error handling."""
        # Test with invalid data
        result = synthesizer.synthesize_insights(
            context=mock_context,
            biomarker_scores={},
            clustering_results={},
            lifestyle_profile={},
            requested_categories=["invalid_category"]
        )
        
        # Should still return a result, but with no insights
        assert isinstance(result, InsightSynthesisResult)
        assert result.total_insights == 0
    
    def test_get_supported_categories(self, synthesizer):
        """Test getting supported categories."""
        categories = synthesizer.get_supported_categories()
        assert len(categories) > 0
        assert "metabolic" in categories
        assert "cardiovascular" in categories
    
    def test_validate_insight_request(self, synthesizer):
        """Test insight request validation."""
        # Valid request
        valid_request = InsightGenerationRequest(
            analysis_id="test",
            context_data={"user": "test"},
            requested_categories=["metabolic"]
        )
        assert synthesizer.validate_insight_request(valid_request) is True
        
        # Invalid request - missing analysis_id
        invalid_request = InsightGenerationRequest(
            analysis_id="",
            context_data={"user": "test"},
            requested_categories=["metabolic"]
        )
        assert synthesizer.validate_insight_request(invalid_request) is False
        
        # Invalid request - missing context_data
        invalid_request2 = InsightGenerationRequest(
            analysis_id="test",
            context_data={},
            requested_categories=["metabolic"]
        )
        assert synthesizer.validate_insight_request(invalid_request2) is False


class TestInsightModels:
    """Test insight models."""
    
    def test_insight_model_creation(self):
        """Test creating insight model."""
        insight = Insight(
            id="test_insight",
            category="metabolic",
            summary="Test insight summary",
            evidence={"biomarkers": ["glucose"]},
            confidence=0.85,
            severity="warning",
            recommendations=["Test recommendation"],
            biomarkers_involved=["glucose"],
            lifestyle_factors=["diet"],
            tokens_used=150,
            latency_ms=250,
            created_at=datetime.now(UTC).isoformat()
        )
        
        assert insight.id == "test_insight"
        assert insight.category == "metabolic"
        assert insight.confidence == 0.85
        assert insight.severity == "warning"
        assert insight.tokens_used == 150
        assert insight.latency_ms == 250
    
    def test_insight_model_default_values(self):
        """Test insight model with default values."""
        insight = Insight(
            id="test_insight",
            category="metabolic",
            summary="Test insight summary",
            created_at=datetime.now(UTC).isoformat()
        )
        
        assert insight.tokens_used == 0
        assert insight.latency_ms == 0
        assert insight.confidence == 0.0
        assert insight.severity == "info"
    
    def test_insight_synthesis_result_creation(self):
        """Test creating insight synthesis result."""
        insights = [
            Insight(
                id="insight1",
                category="metabolic",
                summary="Test insight",
                evidence={},
                confidence=0.8,
                created_at=datetime.now(UTC).isoformat()
            )
        ]
        
        result = InsightSynthesisResult(
            analysis_id="test_analysis",
            insights=insights,
            synthesis_summary={"total_processed": 1},
            total_insights=1,
            categories_covered=["metabolic"],
            overall_confidence=0.8,
            processing_time_ms=100,
            created_at=datetime.now(UTC).isoformat()
        )
        
        assert result.analysis_id == "test_analysis"
        assert result.total_insights == 1
        assert result.overall_confidence == 0.8
        assert "metabolic" in result.categories_covered


if __name__ == "__main__":
    pytest.main([__file__])
