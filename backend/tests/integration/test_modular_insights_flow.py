"""
Integration tests for modular insights flow through orchestrator.
"""

import pytest
from unittest.mock import Mock, patch
from uuid import uuid4
from datetime import datetime, UTC

from core.pipeline.orchestrator import AnalysisOrchestrator
from core.pipeline.context_factory import AnalysisContextFactory
from core.models.context import AnalysisContext
from core.models.user import User
from core.models.biomarker import BiomarkerPanel, BiomarkerValue
from core.dto.builders import build_analysis_result_dto


class TestModularInsightsFlow:
    """Test the complete modular insights flow through orchestrator."""
    
    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator instance."""
        return AnalysisOrchestrator()
    
    @pytest.fixture
    def context_factory(self):
        """Create context factory instance."""
        return AnalysisContextFactory()
    
    @pytest.fixture
    def mock_biomarkers(self):
        """Create realistic mock biomarkers for all five insight engines."""
        return {
            # Metabolic Age Insight
            "glucose": 95.0,
            "hba1c": 5.4,
            "insulin": 8.5,
            "age": 35,
            
            # Heart Insight
            "total_cholesterol": 220.0,
            "hdl_cholesterol": 45.0,
            "ldl_cholesterol": 140.0,
            "triglycerides": 150.0,
            
            # Inflammation Insight
            "crp": 2.5,
            "white_blood_cells": 7.2,
            "neutrophils": 4.5,
            "lymphocytes": 2.1,
            "ferritin": 180.0,
            
            # Fatigue Root Cause Insight
            "transferrin_saturation": 25.0,
            "b12": 350.0,
            "folate": 8.5,
            "tsh": 2.8,
            "ft4": 1.2,
            "ft3": 3.1,
            "cortisol": 15.0,
            
            # Detox Filtration Insight
            "creatinine": 1.0,
            "alt": 35.0,
            "ast": 28.0,
            "ggt": 45.0,
            "alp": 85.0,
            "bilirubin": 0.8,
            "egfr": 95.0,
            "bun": 18.0,
            "albumin": 4.2
        }
    
    @pytest.fixture
    def mock_user_data(self):
        """Create mock user data."""
        return {
            "user_id": str(uuid4()),
            "age": 35,
            "gender": "male",
            "height": 180.0,
            "weight": 75.0,
            "ethnicity": "caucasian",
            "medical_history": {},
            "medications": [],
            "lifestyle_factors": {
                "diet_level": "good",
                "exercise_minutes_per_week": 180,
                "sleep_hours": 7.5,
                "stress_level": "moderate",
                "smoking_status": "never",
                "alcohol_units_per_week": 3
            }
        }
    
    @pytest.fixture
    def analysis_context(self, context_factory, mock_biomarkers, mock_user_data):
        """Create analysis context with mock data."""
        # Create biomarker values
        biomarker_values = {}
        for name, value in mock_biomarkers.items():
            biomarker_values[name] = BiomarkerValue(
                name=name,
                value=value,
                unit="mg/dL"
            )
        
        # Create biomarker panel
        biomarker_panel = BiomarkerPanel(
            biomarkers=biomarker_values,
            source="test",
            version="1.0",
            created_at=datetime.now(UTC).isoformat()
        )
        
        # Create user
        user = User(
            user_id=mock_user_data["user_id"],
            age=mock_user_data["age"],
            gender=mock_user_data["gender"],
            height=mock_user_data["height"],
            weight=mock_user_data["weight"],
            ethnicity=mock_user_data["ethnicity"],
            medical_history=mock_user_data["medical_history"],
            medications=mock_user_data["medications"],
            lifestyle_factors=mock_user_data["lifestyle_factors"]
        )
        
        # Create analysis context
        context = AnalysisContext(
            analysis_id=str(uuid4()),
            user=user,
            biomarker_panel=biomarker_panel,
            created_at=datetime.now(UTC).isoformat()
        )
        
        return context
    
    def test_modular_insights_execution(self, orchestrator, analysis_context):
        """Test that all modular insight engines execute successfully."""
        # Mock the LLM synthesis to avoid external dependencies
        with patch.object(orchestrator.insight_synthesizer, 'synthesize_insights') as mock_synthesize:
            mock_synthesize.return_value = Mock(
                analysis_id=analysis_context.analysis_id,
                insights=[],
                synthesis_summary={},
                total_insights=0,
                categories_covered=[],
                overall_confidence=0.0,
                processing_time_ms=100,
                created_at=datetime.now(UTC).isoformat()
            )
            
            # Execute orchestrator
            result = orchestrator.synthesize_insights(
                context=analysis_context,
                biomarker_scores={},
                clustering_results={},
                lifestyle_data=analysis_context.user.lifestyle_factors
            )
            
            # Assertions
            assert result is not None
            assert "analysis_id" in result
            assert "insights" in result
            assert "total_insights" in result
            assert "modular_insights_count" in result
            assert "llm_insights_count" in result
            
            # Should have modular insights
            assert result["modular_insights_count"] >= 5
            assert result["total_insights"] >= 5
            
            # Print insight IDs for debug visibility
            insight_ids = [insight["id"] for insight in result["insights"]]
            print(f"[DEBUG] Generated insight IDs: {', '.join(insight_ids)}")
            
            # Verify all expected insight engines produced results
            expected_insights = [
                "metabolic_age", "heart_insight", "inflammation", 
                "fatigue_root_cause", "detox_filtration"
            ]
            
            for expected in expected_insights:
                assert any(insight["id"] == expected for insight in result["insights"]), \
                    f"Expected insight '{expected}' not found in results"
            
            print(f"[OK] All {len(expected_insights)} expected insights generated successfully")
    
    def test_insight_data_structure(self, orchestrator, analysis_context):
        """Test that insight data has correct structure."""
        # Mock the LLM synthesis
        with patch.object(orchestrator.insight_synthesizer, 'synthesize_insights') as mock_synthesize:
            mock_synthesize.return_value = Mock(
                analysis_id=analysis_context.analysis_id,
                insights=[],
                synthesis_summary={},
                total_insights=0,
                categories_covered=[],
                overall_confidence=0.0,
                processing_time_ms=100,
                created_at=datetime.now(UTC).isoformat()
            )
            
            # Execute orchestrator
            result = orchestrator.synthesize_insights(
                context=analysis_context,
                biomarker_scores={},
                clustering_results={},
                lifestyle_data=analysis_context.user.lifestyle_factors
            )
            
            # Check insight structure
            for insight in result["insights"]:
                # Required fields
                assert "id" in insight
                assert "category" in insight
                assert "confidence" in insight
                assert "severity" in insight
                assert "recommendations" in insight
                assert "biomarkers_involved" in insight
                assert "source" in insight
                
                # Data types
                assert isinstance(insight["id"], str)
                assert isinstance(insight["confidence"], (int, float))
                assert isinstance(insight["recommendations"], list)
                assert isinstance(insight["biomarkers_involved"], list)
                assert insight["source"] in ["modular", "llm"]
                
                # Confidence should be between 0 and 1
                assert 0.0 <= insight["confidence"] <= 1.0
                
                # Severity should be valid
                assert insight["severity"] in ["info", "mild", "moderate", "high", "critical", "normal"]
    
    def test_dto_builder_integration(self, orchestrator, analysis_context):
        """Test that DTO builder correctly processes modular insights."""
        # Mock the LLM synthesis
        with patch.object(orchestrator.insight_synthesizer, 'synthesize_insights') as mock_synthesize:
            mock_synthesize.return_value = Mock(
                analysis_id=analysis_context.analysis_id,
                insights=[],
                synthesis_summary={},
                total_insights=0,
                categories_covered=[],
                overall_confidence=0.0,
                processing_time_ms=100,
                created_at=datetime.now(UTC).isoformat()
            )
            
            # Execute orchestrator
            result = orchestrator.synthesize_insights(
                context=analysis_context,
                biomarker_scores={},
                clustering_results={},
                lifestyle_data=analysis_context.user.lifestyle_factors
            )
            
            # Build DTO
            dto = build_analysis_result_dto(result)
            
            # Assertions
            assert dto is not None
            assert "analysis_id" in dto
            assert "insights" in dto
            assert "meta" in dto
            
            # Check meta information
            meta = dto["meta"]
            assert "total_insights" in meta
            assert "modular_insights_count" in meta
            assert "llm_insights_count" in meta
            assert "processing_time_ms" in meta
            assert "modular_processing_time_ms" in meta
            
            # Should have modular insights
            assert meta["modular_insights_count"] >= 5
            assert meta["total_insights"] >= 5
            
            print(f"[DEBUG] DTO meta: {meta}")
    
    def test_persistence_compatibility(self, orchestrator, analysis_context):
        """Test that insights are compatible with persistence service."""
        # Mock the LLM synthesis
        with patch.object(orchestrator.insight_synthesizer, 'synthesize_insights') as mock_synthesize:
            mock_synthesize.return_value = Mock(
                analysis_id=analysis_context.analysis_id,
                insights=[],
                synthesis_summary={},
                total_insights=0,
                categories_covered=[],
                overall_confidence=0.0,
                processing_time_ms=100,
                created_at=datetime.now(UTC).isoformat()
            )
            
            # Execute orchestrator
            result = orchestrator.synthesize_insights(
                context=analysis_context,
                biomarker_scores={},
                clustering_results={},
                lifestyle_data=analysis_context.user.lifestyle_factors
            )
            
            # Check that insights have fields required by persistence service
            for insight in result["insights"]:
                # Required fields for persistence
                assert "id" in insight
                assert "category" in insight
                assert "confidence" in insight
                assert "severity" in insight
                assert "recommendations" in insight
                assert "biomarkers_involved" in insight
                
                # Optional fields that should be present
                assert "evidence" in insight
                assert "source" in insight
                
                # Ensure data types are correct for persistence
                assert isinstance(insight["confidence"], (int, float))
                assert isinstance(insight["recommendations"], list)
                assert isinstance(insight["biomarkers_involved"], list)
                assert isinstance(insight["evidence"], dict)
    
    def test_error_handling(self, orchestrator, analysis_context):
        """Test error handling when insight engines fail."""
        # Mock the LLM synthesis
        with patch.object(orchestrator.insight_synthesizer, 'synthesize_insights') as mock_synthesize:
            mock_synthesize.return_value = Mock(
                analysis_id=analysis_context.analysis_id,
                insights=[],
                synthesis_summary={},
                total_insights=0,
                categories_covered=[],
                overall_confidence=0.0,
                processing_time_ms=100,
                created_at=datetime.now(UTC).isoformat()
            )
            
            # Mock one insight engine to fail
            with patch('core.insights.modules.metabolic_age.MetabolicAgeInsight.analyze') as mock_analyze:
                mock_analyze.side_effect = Exception("Test error")
                
                # Execute orchestrator - should not fail completely
                result = orchestrator.synthesize_insights(
                    context=analysis_context,
                    biomarker_scores={},
                    clustering_results={},
                    lifestyle_data=analysis_context.user.lifestyle_factors
                )
                
                # Should still have results from other engines
                assert result is not None
                assert result["modular_insights_count"] >= 4  # At least 4 other engines should work
                assert result["total_insights"] >= 4
    
    def test_performance_metrics(self, orchestrator, analysis_context):
        """Test that performance metrics are captured."""
        # Mock the LLM synthesis
        with patch.object(orchestrator.insight_synthesizer, 'synthesize_insights') as mock_synthesize:
            mock_synthesize.return_value = Mock(
                analysis_id=analysis_context.analysis_id,
                insights=[],
                synthesis_summary={},
                total_insights=0,
                categories_covered=[],
                overall_confidence=0.0,
                processing_time_ms=100,
                created_at=datetime.now(UTC).isoformat()
            )
            
            # Execute orchestrator
            result = orchestrator.synthesize_insights(
                context=analysis_context,
                biomarker_scores={},
                clustering_results={},
                lifestyle_data=analysis_context.user.lifestyle_factors
            )
            
            # Check performance metrics
            assert "processing_time_ms" in result
            assert "modular_processing_time_ms" in result
            
            # Modular processing should be fast (under 1 second)
            assert result["modular_processing_time_ms"] < 1000
            
            print(f"[DEBUG] Modular processing time: {result['modular_processing_time_ms']}ms")
            print(f"[DEBUG] Total processing time: {result['processing_time_ms']}ms")
