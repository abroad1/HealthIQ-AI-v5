"""
Unit tests for LLM integration with orchestrator.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json

from core.pipeline.orchestrator import AnalysisOrchestrator
from core.llm.client import GeminiResponse
from core.models.context import AnalysisContext
from core.models.user import User
from core.models.biomarker import BiomarkerValue


class TestLLMIntegration:
    """Test cases for LLM integration with orchestrator."""
    
    @patch('config.env.settings.GEMINI_API_KEY', 'test_key')
    def test_orchestrator_initialization_with_llm(self):
        """Test orchestrator initializes with LLM components."""
        orchestrator = AnalysisOrchestrator()
        
        assert hasattr(orchestrator, 'llm_client')
        assert hasattr(orchestrator, 'response_parser')
        assert orchestrator.llm_client is not None
        assert orchestrator.response_parser is not None
    
    @patch('config.env.settings.GEMINI_API_KEY', 'test_key')
    @patch('core.llm.client.GeminiClient.generate_structured_output')
    @patch('core.llm.parsing.ResponseParser.parse_and_validate')
    def test_generate_insights_success(self, mock_parse, mock_generate):
        """Test successful insight generation."""
        # Mock LLM response
        mock_response = GeminiResponse(
            content=json.dumps({
                "insights": [
                    {
                        "category": "metabolic",
                        "title": "Glucose Control",
                        "description": "Good glucose control",
                        "severity": "low",
                        "confidence": 0.9,
                        "evidence": ["Normal glucose levels"],
                        "recommendations": ["Continue current diet"]
                    }
                ],
                "overall_assessment": "Good overall health",
                "key_findings": ["Normal biomarkers"],
                "next_steps": ["Continue monitoring"]
            }),
            model="gemini-pro",
            usage={"promptTokenCount": 100, "candidatesTokenCount": 50},
            success=True
        )
        
        # Mock parsing response
        mock_parsed = Mock()
        mock_parsed.success = True
        mock_parsed.data = {
            "insights": [
                {
                    "category": "metabolic",
                    "title": "Glucose Control",
                    "description": "Good glucose control",
                    "severity": "low",
                    "confidence": 0.9,
                    "evidence": ["Normal glucose levels"],
                    "recommendations": ["Continue current diet"]
                }
            ]
        }
        
        mock_generate.return_value = mock_response
        mock_parse.return_value = mock_parsed
        
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
        
        analysis_result = {
            "clusters": [],
            "scoring_summary": {"overall_score": 85},
            "clustering_summary": {"total_clusters": 2}
        }
        
        # Test insight generation
        orchestrator = AnalysisOrchestrator()
        insights = orchestrator._generate_insights(context, analysis_result)
        
        # Verify results
        assert len(insights) == 1
        assert insights[0]["category"] == "metabolic"
        assert insights[0]["title"] == "Glucose Control"
        assert insights[0]["severity"] == "low"
        assert insights[0]["confidence"] == 0.9
        
        # Verify LLM was called
        mock_generate.assert_called_once()
        mock_parse.assert_called_once()
    
    @patch('config.env.settings.GEMINI_API_KEY', 'test_key')
    @patch('core.llm.client.GeminiClient.generate_structured_output')
    def test_generate_insights_llm_failure(self, mock_generate):
        """Test insight generation with LLM failure."""
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
        
        analysis_result = {
            "clusters": [
                {
                    "name": "metabolic",
                    "description": "Metabolic health cluster",
                    "severity": "low",
                    "confidence": 0.8,
                    "biomarkers": ["glucose"]
                }
            ],
            "scoring_summary": {"overall_score": 85},
            "clustering_summary": {"total_clusters": 1}
        }
        
        # Test insight generation
        orchestrator = AnalysisOrchestrator()
        insights = orchestrator._generate_insights(context, analysis_result)
        
        # Verify fallback insights were generated
        assert len(insights) == 1
        assert insights[0]["category"] == "metabolic"
        assert insights[0]["title"] == "metabolic Analysis"
        assert insights[0]["severity"] == "low"
        assert insights[0]["confidence"] == 0.8
    
    @patch('config.env.settings.GEMINI_API_KEY', 'test_key')
    @patch('core.llm.client.GeminiClient.generate_structured_output')
    @patch('core.llm.parsing.ResponseParser.parse_and_validate')
    def test_generate_insights_parsing_failure(self, mock_parse, mock_generate):
        """Test insight generation with parsing failure."""
        # Mock LLM response
        mock_response = GeminiResponse(
            content='{"invalid": "json"}',
            model="gemini-pro",
            usage={"promptTokenCount": 100, "candidatesTokenCount": 50},
            success=True
        )
        
        # Mock parsing failure
        mock_parsed = Mock()
        mock_parsed.success = False
        mock_parsed.data = {}
        
        mock_generate.return_value = mock_response
        mock_parse.return_value = mock_parsed
        
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
        
        analysis_result = {
            "clusters": [
                {
                    "name": "metabolic",
                    "description": "Metabolic health cluster",
                    "severity": "low",
                    "confidence": 0.8,
                    "biomarkers": ["glucose"]
                }
            ],
            "scoring_summary": {"overall_score": 85},
            "clustering_summary": {"total_clusters": 1}
        }
        
        # Test insight generation
        orchestrator = AnalysisOrchestrator()
        insights = orchestrator._generate_insights(context, analysis_result)
        
        # Verify fallback insights were generated
        assert len(insights) == 1
        assert insights[0]["category"] == "metabolic"
        assert insights[0]["title"] == "metabolic Analysis"
        assert insights[0]["severity"] == "low"
        assert insights[0]["confidence"] == 0.8
    
    @patch('config.env.settings.GEMINI_API_KEY', 'test_key')
    def test_generate_fallback_insights(self):
        """Test fallback insight generation."""
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
        
        analysis_result = {
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
            ],
            "scoring_summary": {"overall_score": 85},
            "clustering_summary": {"total_clusters": 2}
        }
        
        # Test fallback insight generation
        orchestrator = AnalysisOrchestrator()
        insights = orchestrator._generate_fallback_insights(context, analysis_result)
        
        # Verify results
        assert len(insights) == 2
        
        # Check first insight
        assert insights[0]["category"] == "metabolic"
        assert insights[0]["title"] == "metabolic Analysis"
        assert insights[0]["severity"] == "low"
        assert insights[0]["confidence"] == 0.8
        assert "glucose" in insights[0]["evidence"][0]
        assert "hba1c" in insights[0]["evidence"][0]
        
        # Check second insight
        assert insights[1]["category"] == "cardiovascular"
        assert insights[1]["title"] == "cardiovascular Analysis"
        assert insights[1]["severity"] == "moderate"
        assert insights[1]["confidence"] == 0.7
        assert "cholesterol" in insights[1]["evidence"][0]
        assert "ldl" in insights[1]["evidence"][0]
    
    @patch('config.env.settings.GEMINI_API_KEY', 'test_key')
    def test_generate_fallback_insights_empty_clusters(self):
        """Test fallback insight generation with empty clusters."""
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
        
        analysis_result = {
            "clusters": [],
            "scoring_summary": {"overall_score": 85},
            "clustering_summary": {"total_clusters": 0}
        }
        
        # Test fallback insight generation
        orchestrator = AnalysisOrchestrator()
        insights = orchestrator._generate_fallback_insights(context, analysis_result)
        
        # Verify no insights generated
        assert len(insights) == 0
    
    @patch('config.env.settings.GEMINI_API_KEY', 'test_key')
    @patch('core.pipeline.orchestrator.AnalysisOrchestrator._generate_insights')
    def test_run_with_llm_integration(self, mock_generate_insights):
        """Test full run method with LLM integration."""
        # Mock insight generation
        mock_generate_insights.return_value = [
            {
                "category": "metabolic",
                "title": "Glucose Control",
                "description": "Good glucose control",
                "severity": "low",
                "confidence": 0.9,
                "evidence": ["Normal glucose levels"],
                "recommendations": ["Continue current diet"]
            }
        ]
        
        # Test data
        biomarkers = {
            "glucose": {"value": 95.0, "unit": "mg/dL"}
        }
        user = {
            "age": 30,
            "gender": "male"
        }
        
        # Test run method
        orchestrator = AnalysisOrchestrator()
        result = orchestrator.run(biomarkers, user, assume_canonical=True)
        
        # Verify results
        assert result.analysis_id is not None
        assert result.status == "complete"
        assert result.created_at is not None
        
        # Verify methods were called
        mock_generate_insights.assert_called_once()
