"""
Integration tests for PersistenceService.
"""

import pytest
from unittest.mock import Mock, patch
from uuid import uuid4, UUID
from datetime import datetime

from services.storage.persistence_service import PersistenceService
from repositories import (
    AnalysisRepository,
    AnalysisResultRepository,
    BiomarkerScoreRepository,
    ClusterRepository,
    InsightRepository,
    ExportRepository,
    ProfileRepository,
    AuditLogRepository
)


class TestPersistenceService:
    """Test cases for PersistenceService."""
    
    @pytest.fixture
    def mock_db_session(self):
        """Mock database session."""
        return Mock()
    
    @pytest.fixture
    def persistence_service(self, mock_db_session):
        """PersistenceService instance with mocked session."""
        return PersistenceService(mock_db_session)
    
    def test_save_analysis_success(self, persistence_service, mock_db_session):
        """Test successful analysis saving."""
        # Arrange
        analysis_dto = {
            "analysis_id": str(uuid4()),
            "status": "completed",
            "raw_biomarkers": {"glucose": 95.0},
            "questionnaire_data": {"age": 30},
            "processing_time_seconds": 5.0,
            "analysis_version": "1.0.0",
            "pipeline_version": "1.0.0"
        }
        user_id = uuid4()
        
        # Mock repository methods
        with patch.object(persistence_service.analysis_repo, 'upsert_by_analysis_id') as mock_upsert:
            mock_analysis = Mock()
            mock_analysis.id = UUID(analysis_dto["analysis_id"])
            mock_upsert.return_value = mock_analysis
            
            # Act
            result = persistence_service.save_analysis(analysis_dto, user_id)
            
            # Assert
            assert result == UUID(analysis_dto["analysis_id"])
            mock_upsert.assert_called_once()
    
    def test_save_analysis_failure(self, persistence_service, mock_db_session):
        """Test analysis saving failure."""
        # Arrange
        analysis_dto = {
            "analysis_id": "invalid-uuid",
            "status": "completed"
        }
        user_id = uuid4()
        
        # Act
        result = persistence_service.save_analysis(analysis_dto, user_id)
        
        # Assert
        assert result is None
    
    def test_save_results_success(self, persistence_service, mock_db_session):
        """Test successful results saving."""
        # Arrange
        analysis_id = uuid4()
        results_dto = {
            "biomarkers": [
                {
                    "biomarker_name": "glucose",
                    "value": 95.0,
                    "unit": "mg/dL",
                    "score": 0.75,
                    "status": "normal"
                }
            ],
            "clusters": [
                {
                    "cluster_name": "metabolic",
                    "cluster_type": "health_system",
                    "score": 0.8,
                    "confidence": 0.9
                }
            ],
            "insights": [
                {
                    "insight_type": "health_insight",
                    "category": "metabolic",
                    "title": "Good glucose control",
                    "content": "Your glucose levels are well controlled"
                }
            ],
            "overall_score": 0.85,
            "result_version": "1.0.0"
        }
        
        # Mock repository methods
        with patch.object(persistence_service.analysis_result_repo, 'upsert_by_analysis_id') as mock_upsert_result, \
             patch.object(persistence_service.biomarker_score_repo, 'delete_by_analysis_id') as mock_delete_biomarkers, \
             patch.object(persistence_service.biomarker_score_repo, 'upsert_by_analysis_and_biomarker') as mock_upsert_biomarker, \
             patch.object(persistence_service.cluster_repo, 'delete_by_analysis_id') as mock_delete_clusters, \
             patch.object(persistence_service.cluster_repo, 'create') as mock_create_cluster, \
             patch.object(persistence_service.insight_repo, 'delete_by_analysis_id') as mock_delete_insights, \
             patch.object(persistence_service.insight_repo, 'create') as mock_create_insight:
            
            mock_result = Mock()
            mock_upsert_result.return_value = mock_result
            
            # Act
            result = persistence_service.save_results(results_dto, analysis_id)
            
            # Assert
            assert result is True
            mock_upsert_result.assert_called_once()
            mock_delete_biomarkers.assert_called_once_with(analysis_id)
            mock_upsert_biomarker.assert_called_once()
            mock_delete_clusters.assert_called_once_with(analysis_id)
            mock_create_cluster.assert_called_once()
            mock_delete_insights.assert_called_once_with(analysis_id)
            mock_create_insight.assert_called_once()
    
    def test_save_export_success(self, persistence_service, mock_db_session):
        """Test successful export saving."""
        # Arrange
        user_id = uuid4()
        export_dto = {
            "analysis_id": uuid4(),
            "export_type": "pdf",
            "status": "pending"
        }
        
        # Mock repository methods
        with patch.object(persistence_service.export_repo, 'create') as mock_create:
            mock_export = Mock()
            mock_export.id = uuid4()
            mock_create.return_value = mock_export
            
            # Act
            result = persistence_service.save_export(export_dto, user_id)
            
            # Assert
            assert result == mock_export.id
            mock_create.assert_called_once()
    
    def test_get_analysis_history_success(self, persistence_service, mock_db_session):
        """Test successful analysis history retrieval."""
        # Arrange
        user_id = uuid4()
        mock_analyses = [
            Mock(id=uuid4(), created_at=datetime.now(), status="completed", processing_time_seconds=5.0),
            Mock(id=uuid4(), created_at=datetime.now(), status="completed", processing_time_seconds=3.0)
        ]
        
        # Mock repository methods
        with patch.object(persistence_service.analysis_repo, 'get_recent_analyses') as mock_get_analyses, \
             patch.object(persistence_service.analysis_result_repo, 'get_by_analysis_id') as mock_get_result:
            
            mock_get_analyses.return_value = mock_analyses
            mock_result1 = Mock(overall_score=0.85)
            mock_result2 = Mock(overall_score=0.92)
            mock_get_result.side_effect = [mock_result1, mock_result2]
            
            # Act
            result = persistence_service.get_analysis_history(user_id, limit=10, offset=0)
            
            # Assert
            assert len(result) == 2
            assert result[0]["overall_score"] == 0.85
            assert result[1]["overall_score"] == 0.92
            mock_get_analyses.assert_called_once_with(user_id, 10)
    
    def test_get_analysis_result_success(self, persistence_service, mock_db_session):
        """Test successful analysis result retrieval."""
        # Arrange
        analysis_id = uuid4()
        mock_analysis = Mock(id=analysis_id, created_at=datetime.now(), status="completed")
        mock_result = Mock(
            overall_score=0.85,
            result_version="1.0.0",
            confidence_score=0.9,
            processing_metadata={"test": "data"},
            created_at=datetime.now()
        )
        mock_biomarker_scores = [
            Mock(
                biomarker_name="glucose",
                value=95.0,
                unit="mg/dL",
                score=0.75,
                percentile=65.0,
                status="normal",
                reference_range={"min": 70, "max": 100},
                interpretation="Within normal range"
            )
        ]
        mock_clusters = [
            Mock(
                id=uuid4(),
                cluster_name="metabolic",
                biomarkers=["glucose"],
                description="Metabolic health cluster",
                severity="normal",
                confidence=0.9
            )
        ]
        mock_insights = [
            Mock(
                id=uuid4(),
                title="Good glucose control",
                content="Your glucose levels are well controlled",
                category="metabolic",
                confidence=0.9,
                severity="normal",
                biomarkers_involved=["glucose"],
                recommendations=["Continue current diet"]
            )
        ]
        
        # Mock repository methods
        with patch.object(persistence_service.analysis_repo, 'get_by_id') as mock_get_analysis, \
             patch.object(persistence_service.analysis_result_repo, 'get_by_analysis_id') as mock_get_result, \
             patch.object(persistence_service.biomarker_score_repo, 'list_by_analysis_id') as mock_get_biomarkers, \
             patch.object(persistence_service.cluster_repo, 'list_by_analysis_id') as mock_get_clusters, \
             patch.object(persistence_service.insight_repo, 'list_by_analysis_id') as mock_get_insights:
            
            mock_get_analysis.return_value = mock_analysis
            mock_get_result.return_value = mock_result
            mock_get_biomarkers.return_value = mock_biomarker_scores
            mock_get_clusters.return_value = mock_clusters
            mock_get_insights.return_value = mock_insights
            
            # Act
            result = persistence_service.get_analysis_result(analysis_id)
            
            # Assert
            assert result is not None
            assert result["analysis_id"] == str(analysis_id)
            assert result["overall_score"] == 0.85
            assert len(result["biomarkers"]) == 1
            assert len(result["clusters"]) == 1
            assert len(result["insights"]) == 1
            assert result["biomarkers"][0]["biomarker_name"] == "glucose"
            assert result["clusters"][0]["name"] == "metabolic"
            assert result["insights"][0]["title"] == "Good glucose control"
    
    def test_get_analysis_result_not_found(self, persistence_service, mock_db_session):
        """Test analysis result retrieval when not found."""
        # Arrange
        analysis_id = uuid4()
        
        # Mock repository methods
        with patch.object(persistence_service.analysis_repo, 'get_by_id') as mock_get_analysis:
            mock_get_analysis.return_value = None
            
            # Act
            result = persistence_service.get_analysis_result(analysis_id)
            
            # Assert
            assert result is None
