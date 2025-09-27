"""
Integration tests for clustering orchestrator.

Tests the full clustering pipeline integration with the orchestrator.
"""

import pytest
from unittest.mock import Mock, patch
from core.pipeline.orchestrator import AnalysisOrchestrator
from core.models.context import AnalysisContext
from core.models.biomarker import BiomarkerPanel, BiomarkerValue
from core.models.user import User


@pytest.fixture
def mock_analysis_context():
    """Create a mock analysis context for testing."""
    user = User(
        user_id="test_user",
        age=35,
        gender="male",
        weight=75.0,
        height=175.0
    )
    
    biomarker_panel = BiomarkerPanel(
        biomarkers={
            "glucose": BiomarkerValue(name="glucose", value=95.0, unit="mg/dL"),
            "hba1c": BiomarkerValue(name="hba1c", value=5.2, unit="%"),
            "total_cholesterol": BiomarkerValue(name="total_cholesterol", value=220.0, unit="mg/dL"),
            "ldl_cholesterol": BiomarkerValue(name="ldl_cholesterol", value=140.0, unit="mg/dL"),
            "hdl_cholesterol": BiomarkerValue(name="hdl_cholesterol", value=45.0, unit="mg/dL"),
            "triglycerides": BiomarkerValue(name="triglycerides", value=180.0, unit="mg/dL"),
            "crp": BiomarkerValue(name="crp", value=2.5, unit="mg/L"),
            "creatinine": BiomarkerValue(name="creatinine", value=1.2, unit="mg/dL"),
            "alt": BiomarkerValue(name="alt", value=35.0, unit="U/L"),
            "vitamin_d": BiomarkerValue(name="vitamin_d", value=25.0, unit="ng/mL")
        },
        source="test_source",
        version="1.0"
    )
    
    return AnalysisContext(
        analysis_id="test_analysis",
        user=user,
        biomarker_panel=biomarker_panel,
        created_at="2024-01-01T00:00:00Z"
    )


@pytest.fixture
def mock_scoring_result():
    """Create a mock scoring result."""
    return {
        "overall_score": 52.0,
        "confidence": "medium",
        "health_system_scores": {
            "metabolic": {
                "overall_score": 77.5,
                "confidence": "high",
                "missing_biomarkers": [],
                "recommendations": ["Monitor blood glucose regularly"],
                "biomarker_scores": [
                    {
                        "biomarker_name": "glucose",
                        "value": 95.0,
                        "score": 75.0,
                        "score_range": "normal",
                        "confidence": "high"
                    },
                    {
                        "biomarker_name": "hba1c",
                        "value": 5.2,
                        "score": 80.0,
                        "score_range": "normal",
                        "confidence": "high"
                    }
                ]
            },
            "cardiovascular": {
                "overall_score": 42.5,
                "confidence": "medium",
                "missing_biomarkers": [],
                "recommendations": ["Address cholesterol levels"],
                "biomarker_scores": [
                    {
                        "biomarker_name": "total_cholesterol",
                        "value": 220.0,
                        "score": 45.0,
                        "score_range": "high",
                        "confidence": "medium"
                    },
                    {
                        "biomarker_name": "ldl_cholesterol",
                        "value": 140.0,
                        "score": 40.0,
                        "score_range": "high",
                        "confidence": "medium"
                    },
                    {
                        "biomarker_name": "hdl_cholesterol",
                        "value": 45.0,
                        "score": 55.0,
                        "score_range": "normal",
                        "confidence": "medium"
                    },
                    {
                        "biomarker_name": "triglycerides",
                        "value": 180.0,
                        "score": 35.0,
                        "score_range": "high",
                        "confidence": "medium"
                    }
                ]
            },
            "inflammatory": {
                "overall_score": 35.0,
                "confidence": "high",
                "missing_biomarkers": [],
                "recommendations": ["Address inflammation"],
                "biomarker_scores": [
                    {
                        "biomarker_name": "crp",
                        "value": 2.5,
                        "score": 35.0,
                        "score_range": "high",
                        "confidence": "high"
                    }
                ]
            },
            "kidney": {
                "overall_score": 60.0,
                "confidence": "medium",
                "missing_biomarkers": [],
                "recommendations": ["Monitor kidney function"],
                "biomarker_scores": [
                    {
                        "biomarker_name": "creatinine",
                        "value": 1.2,
                        "score": 60.0,
                        "score_range": "normal",
                        "confidence": "medium"
                    }
                ]
            },
            "liver": {
                "overall_score": 80.0,
                "confidence": "high",
                "missing_biomarkers": [],
                "recommendations": ["Liver function looks good"],
                "biomarker_scores": [
                    {
                        "biomarker_name": "alt",
                        "value": 35.0,
                        "score": 80.0,
                        "score_range": "normal",
                        "confidence": "high"
                    }
                ]
            },
            "nutritional": {
                "overall_score": 40.0,
                "confidence": "medium",
                "missing_biomarkers": ["b12", "folate"],
                "recommendations": ["Address vitamin D deficiency"],
                "biomarker_scores": [
                    {
                        "biomarker_name": "vitamin_d",
                        "value": 25.0,
                        "score": 40.0,
                        "score_range": "low",
                        "confidence": "medium"
                    }
                ]
            }
        },
        "missing_biomarkers": ["b12", "folate"],
        "recommendations": ["Address cholesterol levels", "Address inflammation", "Address vitamin D deficiency"],
        "lifestyle_adjustments": ["Consider dietary changes", "Increase physical activity"]
    }


@pytest.fixture
def mock_lifestyle_data():
    """Create mock lifestyle data."""
    return {
        "diet_level": "average",
        "sleep_hours": 7.0,
        "exercise_minutes_per_week": 150,
        "alcohol_units_per_week": 5,
        "smoking_status": "never",
        "stress_level": "moderate"
    }


class TestClusteringOrchestratorIntegration:
    """Integration tests for clustering with orchestrator."""
    
    def test_orchestrator_has_clustering_engine(self):
        """Test that orchestrator has clustering engine."""
        orchestrator = AnalysisOrchestrator()
        
        assert hasattr(orchestrator, 'clustering_engine')
        assert orchestrator.clustering_engine is not None
    
    def test_cluster_biomarkers_with_precomputed_scoring(self, mock_analysis_context, mock_scoring_result):
        """Test clustering with pre-computed scoring results."""
        orchestrator = AnalysisOrchestrator()
        
        result = orchestrator.cluster_biomarkers(
            context=mock_analysis_context,
            scoring_result=mock_scoring_result
        )
        
        assert "clusters" in result
        assert "clustering_summary" in result
        assert isinstance(result["clusters"], list)
        assert isinstance(result["clustering_summary"], dict)
        
        # Check clustering summary structure
        summary = result["clustering_summary"]
        assert "total_clusters" in summary
        assert "algorithm_used" in summary
        assert "confidence_score" in summary
        assert "processing_time_ms" in summary
        assert "validation_summary" in summary
        
        # Check cluster structure
        for cluster in result["clusters"]:
            assert "cluster_id" in cluster
            assert "name" in cluster
            assert "biomarkers" in cluster
            assert "description" in cluster
            assert "severity" in cluster
            assert "confidence" in cluster
            assert isinstance(cluster["biomarkers"], list)
            assert 0.0 <= cluster["confidence"] <= 1.0
    
    def test_cluster_biomarkers_without_scoring_result(self, mock_analysis_context, mock_lifestyle_data):
        """Test clustering without pre-computed scoring results."""
        orchestrator = AnalysisOrchestrator()
        
        # Mock the scoring engine to return a known result
        with patch.object(orchestrator.scoring_engine, 'score_biomarkers') as mock_score:
            mock_scoring_result = {
                "overall_score": 52.0,
                "confidence": "medium",
                "health_system_scores": {
                    "metabolic": {
                        "overall_score": 77.5,
                        "confidence": "high",
                        "missing_biomarkers": [],
                        "recommendations": ["Monitor blood glucose regularly"],
                        "biomarker_scores": [
                            {
                                "biomarker_name": "glucose",
                                "value": 95.0,
                                "score": 75.0,
                                "score_range": "normal",
                                "confidence": "high"
                            }
                        ]
                    }
                },
                "missing_biomarkers": [],
                "recommendations": [],
                "lifestyle_adjustments": []
            }
            mock_score.return_value = mock_scoring_result
            
            result = orchestrator.cluster_biomarkers(
                context=mock_analysis_context,
                lifestyle_data=mock_lifestyle_data
            )
            
            assert "clusters" in result
            assert "clustering_summary" in result
            assert isinstance(result["clusters"], list)
            assert isinstance(result["clustering_summary"], dict)
    
    def test_cluster_biomarkers_with_lifestyle_data(self, mock_analysis_context, mock_lifestyle_data):
        """Test clustering with lifestyle data."""
        orchestrator = AnalysisOrchestrator()
        
        with patch.object(orchestrator.scoring_engine, 'score_biomarkers') as mock_score:
            mock_score.return_value = {
                "overall_score": 52.0,
                "confidence": "medium",
                "health_system_scores": {},
                "missing_biomarkers": [],
                "recommendations": [],
                "lifestyle_adjustments": []
            }
            
            result = orchestrator.cluster_biomarkers(
                context=mock_analysis_context,
                lifestyle_data=mock_lifestyle_data
            )
            
            # Verify that scoring was called with lifestyle data
            mock_score.assert_called_once()
            call_args = mock_score.call_args
            
            # Check that lifestyle profile was created (passed as 4th positional argument)
            assert len(call_args[0]) == 4  # biomarkers, age, gender, lifestyle_profile
            lifestyle_profile = call_args[0][3]
            assert lifestyle_profile is not None
    
    def test_clustering_result_structure(self, mock_analysis_context, mock_scoring_result):
        """Test that clustering results have the expected structure."""
        orchestrator = AnalysisOrchestrator()
        
        result = orchestrator.cluster_biomarkers(
            context=mock_analysis_context,
            scoring_result=mock_scoring_result
        )
        
        # Test clusters structure
        for cluster in result["clusters"]:
            assert isinstance(cluster["cluster_id"], str)
            assert isinstance(cluster["name"], str)
            assert isinstance(cluster["biomarkers"], list)
            assert isinstance(cluster["description"], str)
            assert cluster["severity"] in ["normal", "mild", "moderate", "high", "critical"]
            assert isinstance(cluster["confidence"], float)
            assert 0.0 <= cluster["confidence"] <= 1.0
            
            # Check that biomarkers are valid
            for biomarker in cluster["biomarkers"]:
                assert isinstance(biomarker, str)
                assert len(biomarker) > 0
        
        # Test clustering summary structure
        summary = result["clustering_summary"]
        assert isinstance(summary["total_clusters"], int)
        assert summary["total_clusters"] >= 0
        assert isinstance(summary["algorithm_used"], str)
        assert summary["algorithm_used"] in ["rule_based", "weighted_correlation", "health_system_grouping"]
        assert isinstance(summary["confidence_score"], float)
        assert 0.0 <= summary["confidence_score"] <= 1.0
        assert isinstance(summary["processing_time_ms"], float)
        assert summary["processing_time_ms"] >= 0.0
        assert isinstance(summary["validation_summary"], dict)
    
    def test_clustering_with_different_algorithms(self, mock_analysis_context, mock_scoring_result):
        """Test clustering with different algorithms."""
        orchestrator = AnalysisOrchestrator()
        
        algorithms = ["rule_based", "weighted_correlation", "health_system_grouping"]
        
        for algorithm in algorithms:
            # Set algorithm
            orchestrator.clustering_engine.set_clustering_algorithm(algorithm)
            
            result = orchestrator.cluster_biomarkers(
                context=mock_analysis_context,
                scoring_result=mock_scoring_result
            )
            
            assert result["clustering_summary"]["algorithm_used"] == algorithm
            assert "clusters" in result
            assert "clustering_summary" in result
    
    def test_clustering_performance(self, mock_analysis_context, mock_scoring_result):
        """Test clustering performance requirements."""
        orchestrator = AnalysisOrchestrator()
        
        result = orchestrator.cluster_biomarkers(
            context=mock_analysis_context,
            scoring_result=mock_scoring_result
        )
        
        # Check that processing time is reasonable (< 1 second)
        processing_time = result["clustering_summary"]["processing_time_ms"]
        assert processing_time < 1000.0  # Less than 1 second in milliseconds
        
        # Check that we got results
        assert len(result["clusters"]) >= 0
    
    def test_clustering_validation_integration(self, mock_analysis_context, mock_scoring_result):
        """Test that clustering includes validation."""
        orchestrator = AnalysisOrchestrator()
        
        result = orchestrator.cluster_biomarkers(
            context=mock_analysis_context,
            scoring_result=mock_scoring_result
        )
        
        # Check that validation summary is included
        validation_summary = result["clustering_summary"]["validation_summary"]
        assert isinstance(validation_summary, dict)
        assert "total_clusters" in validation_summary
        assert "valid_clusters" in validation_summary
        assert "is_valid" in validation_summary
        
        # Check that validation results are reasonable
        assert validation_summary["total_clusters"] >= 0
        assert validation_summary["valid_clusters"] >= 0
        assert validation_summary["valid_clusters"] <= validation_summary["total_clusters"]
    
    def test_clustering_with_minimal_biomarkers(self):
        """Test clustering with minimal biomarker data."""
        orchestrator = AnalysisOrchestrator()
        
        # Create context with minimal biomarkers
        user = User(user_id="test_user", age=30, gender="female")
        biomarker_panel = BiomarkerPanel(
            biomarkers={
                "glucose": BiomarkerValue(name="glucose", value=90.0, unit="mg/dL"),
                "crp": BiomarkerValue(name="crp", value=1.0, unit="mg/L")
            },
            source="test_source"
        )
        context = AnalysisContext(
            analysis_id="minimal_test",
            user=user,
            biomarker_panel=biomarker_panel,
            created_at="2024-01-01T00:00:00Z"
        )
        
        minimal_scoring = {
            "overall_score": 75.0,
            "confidence": "medium",
            "health_system_scores": {
                "metabolic": {
                    "overall_score": 85.0,
                    "confidence": "high",
                    "missing_biomarkers": ["hba1c"],
                    "recommendations": [],
                    "biomarker_scores": [
                        {
                            "biomarker_name": "glucose",
                            "value": 90.0,
                            "score": 85.0,
                            "score_range": "normal",
                            "confidence": "high"
                        }
                    ]
                },
                "inflammatory": {
                    "overall_score": 80.0,
                    "confidence": "high",
                    "missing_biomarkers": [],
                    "recommendations": [],
                    "biomarker_scores": [
                        {
                            "biomarker_name": "crp",
                            "value": 1.0,
                            "score": 80.0,
                            "score_range": "normal",
                            "confidence": "high"
                        }
                    ]
                }
            },
            "missing_biomarkers": ["hba1c"],
            "recommendations": [],
            "lifestyle_adjustments": []
        }
        
        result = orchestrator.cluster_biomarkers(
            context=context,
            scoring_result=minimal_scoring
        )
        
        assert "clusters" in result
        assert "clustering_summary" in result
        assert isinstance(result["clusters"], list)
        
        # Should still produce valid results even with minimal data
        assert result["clustering_summary"]["total_clusters"] >= 0
        assert result["clustering_summary"]["confidence_score"] >= 0.0
    
    def test_clustering_error_handling(self, mock_analysis_context):
        """Test clustering error handling."""
        orchestrator = AnalysisOrchestrator()
        
        # Test with invalid scoring result
        invalid_scoring = {
            "invalid": "data"
        }
        
        # Should not raise an exception, but handle gracefully
        result = orchestrator.cluster_biomarkers(
            context=mock_analysis_context,
            scoring_result=invalid_scoring
        )
        
        assert "clusters" in result
        assert "clustering_summary" in result
        assert isinstance(result["clusters"], list)
