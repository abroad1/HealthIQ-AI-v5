"""
Unit tests for clustering engine.

Tests the core clustering functionality including multi-engine orchestration,
rule-based clustering, and cluster validation.
"""

import pytest
from unittest.mock import Mock, patch
from core.clustering.engine import ClusteringEngine, ClusteringAlgorithm, ClusteringResult
from core.clustering.weights import EngineWeightingSystem, EngineType
from core.clustering.rules import ClusteringRuleEngine
from core.clustering.validation import ClusterValidator
from core.models.context import AnalysisContext
from core.models.biomarker import BiomarkerCluster, BiomarkerPanel, BiomarkerValue
from core.models.user import User
from core.scoring.engine import ScoringResult, HealthSystemScore, BiomarkerScore, ConfidenceLevel, ScoreRange


@pytest.fixture
def mock_context():
    """Create a mock analysis context."""
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
            "crp": BiomarkerValue(name="crp", value=2.5, unit="mg/L")
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
    biomarker_scores = [
        BiomarkerScore(
            biomarker_name="glucose",
            value=95.0,
            score=75.0,
            score_range=ScoreRange.NORMAL,
            confidence=ConfidenceLevel.HIGH
        ),
        BiomarkerScore(
            biomarker_name="hba1c",
            value=5.2,
            score=80.0,
            score_range=ScoreRange.NORMAL,
            confidence=ConfidenceLevel.HIGH
        ),
        BiomarkerScore(
            biomarker_name="total_cholesterol",
            value=220.0,
            score=45.0,
            score_range=ScoreRange.HIGH,
            confidence=ConfidenceLevel.MEDIUM
        ),
        BiomarkerScore(
            biomarker_name="ldl_cholesterol",
            value=140.0,
            score=40.0,
            score_range=ScoreRange.HIGH,
            confidence=ConfidenceLevel.MEDIUM
        ),
        BiomarkerScore(
            biomarker_name="crp",
            value=2.5,
            score=35.0,
            score_range=ScoreRange.HIGH,
            confidence=ConfidenceLevel.HIGH
        )
    ]
    
    health_system_scores = {
        "metabolic": HealthSystemScore(
            system_name="metabolic",
            overall_score=77.5,
            confidence=ConfidenceLevel.HIGH,
            biomarker_scores=[biomarker_scores[0], biomarker_scores[1]],
            missing_biomarkers=[],
            recommendations=["Monitor blood glucose regularly"]
        ),
        "cardiovascular": HealthSystemScore(
            system_name="cardiovascular",
            overall_score=42.5,
            confidence=ConfidenceLevel.MEDIUM,
            biomarker_scores=[biomarker_scores[2], biomarker_scores[3]],
            missing_biomarkers=["hdl_cholesterol"],
            recommendations=["Address cholesterol levels"]
        ),
        "inflammatory": HealthSystemScore(
            system_name="inflammatory",
            overall_score=35.0,
            confidence=ConfidenceLevel.HIGH,
            biomarker_scores=[biomarker_scores[4]],
            missing_biomarkers=[],
            recommendations=["Address inflammation"]
        )
    }
    
    return ScoringResult(
        overall_score=52.0,
        confidence=ConfidenceLevel.MEDIUM,
        health_system_scores=health_system_scores,
        missing_biomarkers=["hdl_cholesterol"],
        recommendations=["Address cholesterol levels", "Address inflammation"],
        lifestyle_adjustments=["Consider dietary changes"]
    )


@pytest.fixture
def clustering_engine():
    """Create a clustering engine instance."""
    return ClusteringEngine()


class TestClusteringEngine:
    """Test cases for ClusteringEngine."""
    
    def test_initialization(self):
        """Test clustering engine initialization."""
        engine = ClusteringEngine()
        
        assert isinstance(engine.weighting_system, EngineWeightingSystem)
        assert isinstance(engine.rule_engine, ClusteringRuleEngine)
        assert isinstance(engine.validator, ClusterValidator)
        assert engine.algorithm == ClusteringAlgorithm.RULE_BASED
    
    def test_extract_biomarker_values(self, clustering_engine, mock_context):
        """Test biomarker value extraction."""
        values = clustering_engine._extract_biomarker_values(mock_context)
        
        assert isinstance(values, dict)
        assert "glucose" in values
        assert "hba1c" in values
        assert "total_cholesterol" in values
        assert values["glucose"] == 95.0
        assert values["hba1c"] == 5.2
    
    def test_extract_biomarker_scores_from_scoring_result(self, clustering_engine, mock_scoring_result):
        """Test biomarker score extraction from ScoringResult object."""
        scores = clustering_engine._extract_biomarker_scores(mock_scoring_result)
        
        assert isinstance(scores, dict)
        assert "glucose" in scores
        assert "hba1c" in scores
        assert "total_cholesterol" in scores
        assert scores["glucose"] == 75.0
        assert scores["hba1c"] == 80.0
        assert scores["total_cholesterol"] == 45.0
    
    def test_extract_biomarker_scores_from_dict(self, clustering_engine):
        """Test biomarker score extraction from dictionary format."""
        dict_result = {
            "health_system_scores": {
                "metabolic": {
                    "biomarker_scores": [
                        {"biomarker_name": "glucose", "score": 75.0},
                        {"biomarker_name": "hba1c", "score": 80.0}
                    ]
                },
                "cardiovascular": {
                    "biomarker_scores": [
                        {"biomarker_name": "total_cholesterol", "score": 45.0}
                    ]
                }
            }
        }
        
        scores = clustering_engine._extract_biomarker_scores(dict_result)
        
        assert isinstance(scores, dict)
        assert "glucose" in scores
        assert "hba1c" in scores
        assert "total_cholesterol" in scores
        assert scores["glucose"] == 75.0
        assert scores["hba1c"] == 80.0
        assert scores["total_cholesterol"] == 45.0
    
    def test_group_biomarkers_by_health_system(self, clustering_engine):
        """Test biomarker grouping by health system."""
        biomarker_values = {
            "glucose": 95.0,
            "hba1c": 5.2,
            "total_cholesterol": 220.0,
            "ldl_cholesterol": 140.0,
            "crp": 2.5,
            "nonexistent": 100.0
        }
        
        groups = clustering_engine._group_biomarkers_by_health_system(biomarker_values)
        
        assert "metabolic" in groups
        assert "cardiovascular" in groups
        assert "inflammatory" in groups
        assert "glucose" in groups["metabolic"]
        assert "hba1c" in groups["metabolic"]
        assert "total_cholesterol" in groups["cardiovascular"]
        assert "ldl_cholesterol" in groups["cardiovascular"]
        assert "crp" in groups["inflammatory"]
        assert "nonexistent" not in groups["metabolic"]
    
    def test_calculate_cluster_confidence(self, clustering_engine):
        """Test cluster confidence calculation."""
        biomarkers = ["glucose", "hba1c", "total_cholesterol"]
        scores = {
            "glucose": 75.0,
            "hba1c": 80.0,
            "total_cholesterol": 45.0
        }
        
        confidence = clustering_engine._calculate_cluster_confidence(biomarkers, scores)
        
        assert 0.0 <= confidence <= 1.0
        assert confidence > 0  # Should have some confidence
    
    def test_calculate_cluster_confidence_empty(self, clustering_engine):
        """Test cluster confidence calculation with empty biomarkers."""
        confidence = clustering_engine._calculate_cluster_confidence([], {})
        assert confidence == 0.0
    
    def test_create_health_system_cluster(self, clustering_engine):
        """Test health system cluster creation."""
        biomarkers = ["glucose", "hba1c"]
        scores = {"glucose": 75.0, "hba1c": 80.0}
        
        cluster = clustering_engine._create_health_system_cluster("metabolic", biomarkers, scores)
        
        assert cluster is not None
        assert cluster.cluster_id == "metabolic_2_biomarkers"
        assert cluster.name == "Metabolic Health Pattern"
        assert cluster.biomarkers == biomarkers
        assert cluster.severity in ["normal", "mild", "moderate", "high", "critical"]
        assert 0.0 <= cluster.confidence <= 1.0
    
    def test_create_health_system_cluster_insufficient_biomarkers(self, clustering_engine):
        """Test health system cluster creation with insufficient biomarkers."""
        biomarkers = ["glucose"]
        scores = {"glucose": 75.0}
        
        cluster = clustering_engine._create_health_system_cluster("metabolic", biomarkers, scores)
        
        assert cluster is None
    
    def test_validate_clusters_empty(self, clustering_engine):
        """Test cluster validation with empty clusters."""
        validation_summary = clustering_engine._validate_clusters([])
        
        assert validation_summary["total_clusters"] == 0
        assert validation_summary["valid_clusters"] == 0
        assert validation_summary["is_valid"] is True
    
    def test_validate_clusters_with_data(self, clustering_engine):
        """Test cluster validation with cluster data."""
        clusters = [
            BiomarkerCluster(
                cluster_id="test_cluster_1",
                name="Test Cluster 1",
                biomarkers=["glucose", "hba1c"],
                description="Test description",
                severity="moderate",
                confidence=0.8
            ),
            BiomarkerCluster(
                cluster_id="test_cluster_2",
                name="Test Cluster 2",
                biomarkers=["total_cholesterol", "ldl_cholesterol"],
                description="Test description 2",
                severity="high",
                confidence=0.7
            )
        ]
        
        validation_summary = clustering_engine._validate_clusters(clusters)
        
        assert validation_summary["total_clusters"] == 2
        assert validation_summary["valid_clusters"] >= 0
        assert "is_valid" in validation_summary
    
    def test_calculate_overall_confidence(self, clustering_engine):
        """Test overall confidence calculation."""
        clusters = [
            BiomarkerCluster(
                cluster_id="test_cluster_1",
                name="Test Cluster 1",
                biomarkers=["glucose", "hba1c"],
                description="Test description",
                severity="moderate",
                confidence=0.8
            ),
            BiomarkerCluster(
                cluster_id="test_cluster_2",
                name="Test Cluster 2",
                biomarkers=["total_cholesterol"],
                description="Test description 2",
                severity="high",
                confidence=0.7
            )
        ]
        
        validation_summary = {"is_valid": True}
        
        confidence = clustering_engine._calculate_overall_confidence(clusters, validation_summary)
        
        assert 0.0 <= confidence <= 1.0
        assert confidence > 0
    
    def test_set_clustering_algorithm(self, clustering_engine):
        """Test setting clustering algorithm."""
        clustering_engine.set_clustering_algorithm(ClusteringAlgorithm.HEALTH_SYSTEM_GROUPING)
        assert clustering_engine.algorithm == ClusteringAlgorithm.HEALTH_SYSTEM_GROUPING
    
    def test_get_clustering_parameters(self, clustering_engine):
        """Test getting clustering parameters."""
        params = clustering_engine.get_clustering_parameters()
        
        assert "algorithm" in params
        assert "weighting_system" in params
        assert "rule_count" in params
        assert "validation_thresholds" in params
        assert params["algorithm"] == ClusteringAlgorithm.RULE_BASED.value
    
    def test_set_clustering_parameters(self, clustering_engine):
        """Test setting clustering parameters."""
        params = {
            "algorithm": "health_system_grouping",
            "validation_thresholds": {
                "min_cluster_size": 3,
                "min_coherence_threshold": 0.7
            }
        }
        
        clustering_engine.set_clustering_parameters(params)
        
        assert clustering_engine.algorithm == ClusteringAlgorithm.HEALTH_SYSTEM_GROUPING
        assert clustering_engine.validator.min_cluster_size == 3
        assert clustering_engine.validator.min_coherence_threshold == 0.7
    
    def test_apply_clinical_priority(self, clustering_engine):
        """Test applying clinical priority to engines."""
        priority_engines = ["metabolic", "cardiovascular"]
        
        clustering_engine.apply_clinical_priority(priority_engines)
        
        # Verify that priority was applied (weighting system should be modified)
        weight_summary = clustering_engine.weighting_system.get_weight_summary()
        assert "metabolic" in [ew["engine"] for ew in weight_summary["engine_weights"]]
        assert "cardiovascular" in [ew["engine"] for ew in weight_summary["engine_weights"]]
    
    def test_get_clustering_summary(self, clustering_engine):
        """Test getting clustering summary."""
        clusters = [
            BiomarkerCluster(
                cluster_id="test_cluster_1",
                name="Test Cluster 1",
                biomarkers=["glucose", "hba1c"],
                description="Test description",
                severity="moderate",
                confidence=0.8
            )
        ]
        
        result = ClusteringResult(
            clusters=clusters,
            algorithm_used=ClusteringAlgorithm.RULE_BASED,
            confidence_score=0.8,
            validation_summary={"is_valid": True},
            processing_time_ms=50.0
        )
        
        summary = clustering_engine.get_clustering_summary(result)
        
        assert summary["total_clusters"] == 1
        assert summary["algorithm_used"] == ClusteringAlgorithm.RULE_BASED.value
        assert summary["confidence_score"] == 0.8
        assert summary["processing_time_ms"] == 50.0
        assert len(summary["cluster_summary"]) == 1
    
    @patch('time.time')
    def test_cluster_biomarkers_rule_based(self, mock_time, clustering_engine, mock_context, mock_scoring_result):
        """Test rule-based clustering."""
        mock_time.side_effect = [0.0, 0.05]  # Start and end times
        
        # Mock the rule engine to return test clusters
        with patch.object(clustering_engine.rule_engine, 'apply_rules') as mock_apply_rules:
            test_clusters = [
                BiomarkerCluster(
                    cluster_id="metabolic_cluster",
                    name="Metabolic Dysfunction",
                    biomarkers=["glucose", "hba1c"],
                    description="Moderate metabolic dysfunction",
                    severity="moderate",
                    confidence=0.8
                )
            ]
            mock_apply_rules.return_value = test_clusters
            
            result = clustering_engine.cluster_biomarkers(mock_context, mock_scoring_result)
            
            assert isinstance(result, ClusteringResult)
            assert len(result.clusters) == 1
            assert result.algorithm_used == ClusteringAlgorithm.RULE_BASED
            assert result.confidence_score > 0
            assert result.processing_time_ms == 50.0
            assert isinstance(result.validation_summary, dict)
    
    def test_cluster_biomarkers_health_system_grouping(self, clustering_engine, mock_context, mock_scoring_result):
        """Test health system grouping clustering."""
        clustering_engine.set_clustering_algorithm(ClusteringAlgorithm.HEALTH_SYSTEM_GROUPING)
        
        result = clustering_engine.cluster_biomarkers(mock_context, mock_scoring_result)
        
        assert isinstance(result, ClusteringResult)
        assert result.algorithm_used == ClusteringAlgorithm.HEALTH_SYSTEM_GROUPING
        assert len(result.clusters) > 0  # Should create clusters from health systems
    
    def test_cluster_biomarkers_weighted_correlation(self, clustering_engine, mock_context, mock_scoring_result):
        """Test weighted correlation clustering."""
        clustering_engine.set_clustering_algorithm(ClusteringAlgorithm.WEIGHTED_CORRELATION)
        
        result = clustering_engine.cluster_biomarkers(mock_context, mock_scoring_result)
        
        assert isinstance(result, ClusteringResult)
        assert result.algorithm_used == ClusteringAlgorithm.WEIGHTED_CORRELATION
        assert len(result.clusters) > 0  # Should create clusters from health systems


class TestClusteringEngineIntegration:
    """Integration tests for clustering engine."""
    
    def test_full_clustering_pipeline(self, mock_context, mock_scoring_result):
        """Test the full clustering pipeline."""
        engine = ClusteringEngine()
        
        result = engine.cluster_biomarkers(mock_context, mock_scoring_result)
        
        assert isinstance(result, ClusteringResult)
        assert result.algorithm_used == ClusteringAlgorithm.RULE_BASED
        assert result.confidence_score >= 0.0
        assert result.processing_time_ms >= 0.0
        assert isinstance(result.validation_summary, dict)
        
        # Check that clusters have required fields
        for cluster in result.clusters:
            assert hasattr(cluster, 'cluster_id')
            assert hasattr(cluster, 'name')
            assert hasattr(cluster, 'biomarkers')
            assert hasattr(cluster, 'description')
            assert hasattr(cluster, 'severity')
            assert hasattr(cluster, 'confidence')
    
    def test_clustering_with_different_algorithms(self, mock_context, mock_scoring_result):
        """Test clustering with different algorithms."""
        engine = ClusteringEngine()
        
        algorithms = [
            ClusteringAlgorithm.RULE_BASED,
            ClusteringAlgorithm.HEALTH_SYSTEM_GROUPING,
            ClusteringAlgorithm.WEIGHTED_CORRELATION
        ]
        
        for algorithm in algorithms:
            engine.set_clustering_algorithm(algorithm)
            result = engine.cluster_biomarkers(mock_context, mock_scoring_result)
            
            assert result.algorithm_used == algorithm
            assert isinstance(result.clusters, list)
            assert result.confidence_score >= 0.0
    
    def test_extract_biomarker_values_non_numeric(self, clustering_engine):
        """Test biomarker value extraction with non-numeric values."""
        # Create context with non-numeric biomarker values
        user = User(user_id="test_user", age=35, gender="male")
        biomarker_panel = BiomarkerPanel(
            biomarkers={
                "glucose": BiomarkerValue(name="glucose", value="invalid", unit="mg/dL"),
                "hba1c": BiomarkerValue(name="hba1c", value=None, unit="%"),
                "total_cholesterol": BiomarkerValue(name="total_cholesterol", value=220.0, unit="mg/dL")
            },
            source="test_source"
        )
        context = AnalysisContext(
            analysis_id="test_analysis",
            user=user,
            biomarker_panel=biomarker_panel,
            created_at="2024-01-01T00:00:00Z"
        )
        
        values = clustering_engine._extract_biomarker_values(context)
        
        # Should only include numeric values
        assert "total_cholesterol" in values
        assert values["total_cholesterol"] == 220.0
        assert "glucose" not in values
        assert "hba1c" not in values
    
    def test_extract_biomarker_values_direct_numeric(self, clustering_engine):
        """Test biomarker value extraction with direct numeric values."""
        # Create context with BiomarkerValue objects containing non-numeric values
        user = User(user_id="test_user", age=35, gender="male")
        biomarker_panel = BiomarkerPanel(
            biomarkers={
                "glucose": BiomarkerValue(name="glucose", value=95.0, unit="mg/dL"),
                "hba1c": BiomarkerValue(name="hba1c", value="invalid", unit="%"),
                "total_cholesterol": BiomarkerValue(name="total_cholesterol", value=220.0, unit="mg/dL")
            },
            source="test_source"
        )
        context = AnalysisContext(
            analysis_id="test_analysis",
            user=user,
            biomarker_panel=biomarker_panel,
            created_at="2024-01-01T00:00:00Z"
        )
        
        values = clustering_engine._extract_biomarker_values(context)
        
        # Should only include numeric values
        assert "glucose" in values
        assert values["glucose"] == 95.0
        assert "total_cholesterol" in values
        assert values["total_cholesterol"] == 220.0
        assert "hba1c" not in values
    
    def test_extract_biomarker_scores_empty_result(self, clustering_engine):
        """Test biomarker score extraction with empty scoring result."""
        empty_result = {}
        scores = clustering_engine._extract_biomarker_scores(empty_result)
        
        assert isinstance(scores, dict)
        assert len(scores) == 0
    
    def test_extract_biomarker_scores_malformed_result(self, clustering_engine):
        """Test biomarker score extraction with malformed scoring result."""
        malformed_result = {
            "health_system_scores": {
                "metabolic": {
                    # Missing biomarker_scores key
                    "overall_score": 75.0
                }
            }
        }
        scores = clustering_engine._extract_biomarker_scores(malformed_result)
        
        assert isinstance(scores, dict)
        assert len(scores) == 0
    
    def test_set_clustering_parameters_invalid_algorithm(self, clustering_engine):
        """Test setting clustering parameters with invalid algorithm."""
        original_algorithm = clustering_engine.algorithm
        
        params = {
            "algorithm": "invalid_algorithm",
            "validation_thresholds": {
                "min_cluster_size": 3
            }
        }
        
        clustering_engine.set_clustering_parameters(params)
        
        # Should keep original algorithm when invalid algorithm is provided
        assert clustering_engine.algorithm == original_algorithm
        # But validation thresholds should still be updated
        assert clustering_engine.validator.min_cluster_size == 3
    
    def test_apply_clinical_priority_invalid_engines(self, clustering_engine):
        """Test applying clinical priority with invalid engine names."""
        priority_engines = ["metabolic", "invalid_engine", "cardiovascular", "another_invalid"]
        
        clustering_engine.apply_clinical_priority(priority_engines)
        
        # Should not raise an exception and should handle invalid engines gracefully
        # The method should still work with valid engines
        weight_summary = clustering_engine.weighting_system.get_weight_summary()
        assert "metabolic" in [ew["engine"] for ew in weight_summary["engine_weights"]]
        assert "cardiovascular" in [ew["engine"] for ew in weight_summary["engine_weights"]]
    
    def test_apply_clinical_priority_empty_list(self, clustering_engine):
        """Test applying clinical priority with empty engine list."""
        clustering_engine.apply_clinical_priority([])
        
        # Should not raise an exception
        weight_summary = clustering_engine.weighting_system.get_weight_summary()
        assert isinstance(weight_summary, dict)
    
    def test_create_health_system_cluster_severity_boundaries(self, clustering_engine):
        """Test health system cluster creation with severity boundary values."""
        biomarkers = ["glucose", "hba1c"]
        
        # Test exact boundary values
        test_cases = [
            (29.0, "critical"),  # Just below 30
            (30.0, "high"),      # Exactly 30
            (49.0, "high"),      # Just below 50
            (50.0, "moderate"),  # Exactly 50
            (69.0, "moderate"),  # Just below 70
            (70.0, "mild"),      # Exactly 70
            (84.0, "mild"),      # Just below 85
            (85.0, "normal"),    # Exactly 85
            (90.0, "normal")     # Above 85
        ]
        
        for avg_score, expected_severity in test_cases:
            scores = {"glucose": avg_score, "hba1c": avg_score}
            cluster = clustering_engine._create_health_system_cluster("metabolic", biomarkers, scores)
            
            assert cluster is not None
            assert cluster.severity == expected_severity