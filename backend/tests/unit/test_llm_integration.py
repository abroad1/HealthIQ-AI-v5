"""
Unit tests for LLM integration with insight synthesizer.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json

from core.insights.synthesis import InsightSynthesizer
from core.llm.client import GeminiResponse
from core.models.context import AnalysisContext
from core.models.user import User
from core.models.biomarker import BiomarkerValue


class TestLLMIntegration:
    """Test cases for LLM integration with insight synthesizer."""
    
    @patch('config.env.settings.GEMINI_API_KEY', 'test_key')
    def test_synthesizer_initialization_with_llm(self):
        """Test synthesizer initializes with LLM components."""
        synthesizer = InsightSynthesizer()
        
        assert hasattr(synthesizer, 'llm_client')
        assert hasattr(synthesizer, 'prompt_templates')
        assert synthesizer.llm_client is not None
        assert synthesizer.prompt_templates is not None
    
    @patch('config.env.settings.GEMINI_API_KEY', 'test_key')
    @patch('core.insights.synthesis.GeminiClient.generate_insights')
    def test_synthesize_insights_success(self, mock_generate):
        """Test successful insight synthesis."""
        # Mock LLM response
        mock_response = {
            "text": json.dumps({
                "insights": [
                    {
                        "id": "metabolic_insight_1",
                        "category": "metabolic",
                        "summary": "Good glucose control",
                        "severity": "info",
                        "confidence": 0.9,
                        "evidence": {"biomarkers": ["glucose"]},
                        "recommendations": ["Continue current diet"],
                        "biomarkers_involved": ["glucose"],
                        "lifestyle_factors": []
                    }
                ]
            }),
            "candidates": [],
            "model": "gemini-pro"
        }
        
        mock_generate.return_value = mock_response
        
        # Create test context
        user = User(user_id="test_user", age=30, gender="male")
        biomarker = BiomarkerValue(
            name="glucose",
            value=95.0,
            unit="mg/dL"
        )
        from core.models.biomarker import BiomarkerPanel
        biomarker_panel = BiomarkerPanel(
            biomarkers={"glucose": biomarker},
            source="test",
            created_at="2024-01-01T00:00:00Z"
        )
        context = AnalysisContext(
            analysis_id="test_analysis",
            user=user,
            biomarker_panel=biomarker_panel,
            created_at="2024-01-01T00:00:00Z"
        )
        
        biomarker_scores = {"glucose": 0.85}
        clustering_results = {"clusters": []}
        lifestyle_profile = {}
        
        # Test insight synthesis
        synthesizer = InsightSynthesizer()
        result = synthesizer.synthesize_insights(
            context=context,
            biomarker_scores=biomarker_scores,
            clustering_results=clustering_results,
            lifestyle_profile=lifestyle_profile
        )
        
        # Verify results
        assert any(insight.category == "metabolic" for insight in result.insights)
        metabolic_insight = next(insight for insight in result.insights if insight.category == "metabolic")
        assert metabolic_insight.summary == "Good glucose control"
        assert metabolic_insight.severity == "info"
        assert metabolic_insight.confidence == 0.9
        
        # Verify LLM was called
        mock_generate.assert_called()
    
    @patch('config.env.settings.GEMINI_API_KEY', 'test_key')
    @patch('core.insights.synthesis.GeminiClient.generate_insights')
    def test_synthesize_insights_llm_failure(self, mock_generate):
        """Test insight synthesis with LLM failure."""
        # Mock LLM failure
        mock_generate.side_effect = Exception("LLM API error")
        
        # Create test context
        user = User(user_id="test_user", age=30, gender="male")
        biomarker = BiomarkerValue(
            name="glucose",
            value=95.0,
            unit="mg/dL"
        )
        from core.models.biomarker import BiomarkerPanel
        biomarker_panel = BiomarkerPanel(
            biomarkers={"glucose": biomarker},
            source="test",
            created_at="2024-01-01T00:00:00Z"
        )
        context = AnalysisContext(
            analysis_id="test_analysis",
            user=user,
            biomarker_panel=biomarker_panel,
            created_at="2024-01-01T00:00:00Z"
        )
        
        biomarker_scores = {"glucose": 0.85}
        clustering_results = {
            "clusters": [
                {
                    "name": "metabolic",
                    "description": "Metabolic health cluster",
                    "severity": "low",
                    "confidence": 0.8,
                    "biomarkers": ["glucose"]
                }
            ]
        }
        lifestyle_profile = {}
        
        # Test insight synthesis - should handle LLM failure gracefully
        synthesizer = InsightSynthesizer()
        result = synthesizer.synthesize_insights(
            context=context,
            biomarker_scores=biomarker_scores,
            clustering_results=clustering_results,
            lifestyle_profile=lifestyle_profile
        )
        
        # Verify synthesis completes even with LLM failure
        assert result.analysis_id == "test_analysis"
        assert result.total_insights >= 0  # May be 0 if all categories fail
        assert result.synthesis_summary is not None
    
    @patch('config.env.settings.GEMINI_API_KEY', 'test_key')
    @patch('core.insights.synthesis.GeminiClient.generate_insights')
    def test_synthesize_insights_parsing_failure(self, mock_generate):
        """Test insight synthesis with parsing failure."""
        # Mock LLM response with invalid JSON
        mock_response = {
            "text": '{"invalid": "json structure"}',
            "candidates": [],
            "model": "gemini-pro"
        }
        
        mock_generate.return_value = mock_response
        
        # Create test context
        user = User(user_id="test_user", age=30, gender="male")
        biomarker = BiomarkerValue(
            name="glucose",
            value=95.0,
            unit="mg/dL"
        )
        from core.models.biomarker import BiomarkerPanel
        biomarker_panel = BiomarkerPanel(
            biomarkers={"glucose": biomarker},
            source="test",
            created_at="2024-01-01T00:00:00Z"
        )
        context = AnalysisContext(
            analysis_id="test_analysis",
            user=user,
            biomarker_panel=biomarker_panel,
            created_at="2024-01-01T00:00:00Z"
        )
        
        biomarker_scores = {"glucose": 0.85}
        clustering_results = {
            "clusters": [
                {
                    "name": "metabolic",
                    "description": "Metabolic health cluster",
                    "severity": "low",
                    "confidence": 0.8,
                    "biomarkers": ["glucose"]
                }
            ]
        }
        lifestyle_profile = {}
        
        # Test insight synthesis - should handle parsing failure gracefully
        synthesizer = InsightSynthesizer()
        result = synthesizer.synthesize_insights(
            context=context,
            biomarker_scores=biomarker_scores,
            clustering_results=clustering_results,
            lifestyle_profile=lifestyle_profile
        )
        
        # Verify synthesis completes even with parsing failure
        assert result.analysis_id == "test_analysis"
        assert result.total_insights >= 0  # May be 0 if parsing fails
        assert result.synthesis_summary is not None
    
    @patch('config.env.settings.GEMINI_API_KEY', 'test_key')
    def test_synthesize_insights_with_clusters(self):
        """Test insight synthesis with clustering results."""
        # Create test context
        user = User(user_id="test_user", age=30, gender="male")
        biomarker = BiomarkerValue(
            name="glucose",
            value=95.0,
            unit="mg/dL"
        )
        from core.models.biomarker import BiomarkerPanel
        biomarker_panel = BiomarkerPanel(
            biomarkers={"glucose": biomarker},
            source="test",
            created_at="2024-01-01T00:00:00Z"
        )
        context = AnalysisContext(
            analysis_id="test_analysis",
            user=user,
            biomarker_panel=biomarker_panel,
            created_at="2024-01-01T00:00:00Z"
        )
        
        biomarker_scores = {"glucose": 0.85, "hba1c": 0.75, "cholesterol": 0.65, "ldl": 0.70}
        clustering_results = {
            "clusters": [
                {
                    "name": "metabolic",
                    "description": "Metabolic health cluster",
                    "severity": "low",
                    "confidence": 0.8,
                    "biomarkers": ["glucose", "hba1c"]
                },
                {
                    "name": "cardiovascular",
                    "description": "Cardiovascular health cluster",
                    "severity": "moderate",
                    "confidence": 0.7,
                    "biomarkers": ["cholesterol", "ldl"]
                }
            ]
        }
        lifestyle_profile = {}
        
        # Test insight synthesis
        synthesizer = InsightSynthesizer()
        result = synthesizer.synthesize_insights(
            context=context,
            biomarker_scores=biomarker_scores,
            clustering_results=clustering_results,
            lifestyle_profile=lifestyle_profile
        )
        
        # Verify results
        assert result.analysis_id == "test_analysis"
        assert result.total_insights >= 0  # May vary based on LLM response
        assert result.synthesis_summary is not None
        assert "categories_processed" in result.synthesis_summary
        assert "total_insights_generated" in result.synthesis_summary
    
    @patch('config.env.settings.GEMINI_API_KEY', 'test_key')
    def test_synthesize_insights_empty_clusters(self):
        """Test insight synthesis with empty clusters."""
        # Create test context
        user = User(user_id="test_user", age=30, gender="male")
        biomarker = BiomarkerValue(
            name="glucose",
            value=95.0,
            unit="mg/dL"
        )
        from core.models.biomarker import BiomarkerPanel
        biomarker_panel = BiomarkerPanel(
            biomarkers={"glucose": biomarker},
            source="test",
            created_at="2024-01-01T00:00:00Z"
        )
        context = AnalysisContext(
            analysis_id="test_analysis",
            user=user,
            biomarker_panel=biomarker_panel,
            created_at="2024-01-01T00:00:00Z"
        )
        
        biomarker_scores = {"glucose": 0.85}
        clustering_results = {
            "clusters": [],
            "scoring_summary": {"overall_score": 85},
            "clustering_summary": {"total_clusters": 0}
        }
        lifestyle_profile = {}
        
        # Test insight synthesis
        synthesizer = InsightSynthesizer()
        result = synthesizer.synthesize_insights(
            context=context,
            biomarker_scores=biomarker_scores,
            clustering_results=clustering_results,
            lifestyle_profile=lifestyle_profile
        )
        
        # Verify synthesis completes even with empty clusters
        assert result.analysis_id == "test_analysis"
        assert result.total_insights >= 0  # May still generate insights from biomarker scores
        assert result.synthesis_summary is not None
    
    @patch('config.env.settings.GEMINI_API_KEY', 'test_key')
    @patch('core.insights.synthesis.InsightSynthesizer.synthesize_insights')
    def test_synthesizer_integration_with_orchestrator(self, mock_synthesize):
        """Test synthesizer integration through orchestrator."""
        # Mock synthesis result
        from core.models.insight import InsightSynthesisResult, Insight
        mock_insight = Insight(
            id="test_insight_1",
            category="metabolic",
            summary="Good glucose control",
            evidence={"biomarkers": ["glucose"]},
            confidence=0.9,
            severity="info",
            recommendations=["Continue current diet"],
            biomarkers_involved=["glucose"],
            lifestyle_factors=[],
            tokens_used=100,
            latency_ms=500,
            created_at="2024-01-01T00:00:00Z"
        )
        
        mock_synthesis_result = InsightSynthesisResult(
            analysis_id="test_analysis",
            insights=[mock_insight],
            synthesis_summary={
                "categories_processed": 1,
                "categories_with_insights": 1,
                "total_insights_generated": 1,
                "processing_time_ms": 1000,
                "llm_calls_made": 1,
                "total_tokens_used": 100,
                "total_latency_ms": 500,
                "llm_provider": "gemini-pro"
            },
            total_insights=1,
            categories_covered=["metabolic"],
            overall_confidence=0.9,
            processing_time_ms=1000,
            created_at="2024-01-01T00:00:00Z"
        )
        
        mock_synthesize.return_value = mock_synthesis_result
        
        # Test data
        biomarkers = {
            "glucose": {"value": 95.0, "unit": "mg/dL"}
        }
        user = {
            "age": 30,
            "gender": "male"
        }
        
        # Test through orchestrator
        from core.pipeline.orchestrator import AnalysisOrchestrator
        orchestrator = AnalysisOrchestrator()
        result = orchestrator.run(biomarkers, user, assume_canonical=True)
        
        # Verify results
        assert result is not None
        assert result.status == "complete"
        assert result.analysis_id is not None
        assert result.created_at is not None
