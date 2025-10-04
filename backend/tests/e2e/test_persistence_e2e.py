"""
End-to-end tests for persistence flow.
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


class TestPersistenceE2E:
    """End-to-end test cases for persistence flow."""
    
    @pytest.fixture
    def mock_db_session(self):
        """Mock database session."""
        return Mock()
    
    @pytest.fixture
    def persistence_service(self, mock_db_session):
        """PersistenceService instance with mocked session."""
        return PersistenceService(mock_db_session)
    
    def test_full_analysis_persistence_flow(self, persistence_service, mock_db_session):
        """Test complete analysis persistence flow from start to finish."""
        # Arrange
        user_id = uuid4()
        analysis_id = uuid4()
        
        analysis_dto = {
            "analysis_id": str(analysis_id),
            "status": "completed",
            "raw_biomarkers": {
                "glucose": 95.0,
                "cholesterol": 180.0
            },
            "questionnaire_data": {
                "age": 30,
                "gender": "male"
            },
            "processing_time_seconds": 5.0,
            "analysis_version": "1.0.0",
            "pipeline_version": "1.0.0"
        }
        
        results_dto = {
            "biomarkers": [
                {
                    "biomarker_name": "glucose",
                    "value": 95.0,
                    "unit": "mg/dL",
                    "score": 0.75,
                    "percentile": 65.0,
                    "status": "normal",
                    "reference_range": {"min": 70, "max": 100},
                    "interpretation": "Within normal range",
                    "confidence": 0.9,
                    "health_system": "metabolic",
                    "critical_flag": False
                },
                {
                    "biomarker_name": "cholesterol",
                    "value": 180.0,
                    "unit": "mg/dL",
                    "score": 0.85,
                    "percentile": 75.0,
                    "status": "normal",
                    "reference_range": {"min": 120, "max": 200},
                    "interpretation": "Good cholesterol levels",
                    "confidence": 0.9,
                    "health_system": "cardiovascular",
                    "critical_flag": False
                }
            ],
            "clusters": [
                {
                    "cluster_name": "metabolic",
                    "cluster_type": "health_system",
                    "score": 0.8,
                    "confidence": 0.9,
                    "biomarkers": ["glucose"],
                    "insights": ["Good glucose control"],
                    "severity": "normal",
                    "description": "Metabolic health cluster",
                    "health_system": "metabolic",
                    "algorithm_used": "kmeans"
                },
                {
                    "cluster_name": "cardiovascular",
                    "cluster_type": "health_system",
                    "score": 0.85,
                    "confidence": 0.9,
                    "biomarkers": ["cholesterol"],
                    "insights": ["Good cholesterol levels"],
                    "severity": "normal",
                    "description": "Cardiovascular health cluster",
                    "health_system": "cardiovascular",
                    "algorithm_used": "kmeans"
                }
            ],
            "insights": [
                {
                    "insight_type": "health_insight",
                    "category": "metabolic",
                    "title": "Good glucose control",
                    "content": "Your glucose levels are well controlled and within normal range",
                    "confidence": 0.9,
                    "priority": "medium",
                    "actionable": True,
                    "severity": "normal",
                    "biomarkers_involved": ["glucose"],
                    "health_system": "metabolic",
                    "evidence": {"glucose": 95.0},
                    "recommendations": ["Continue current diet and exercise routine"]
                },
                {
                    "insight_type": "health_insight",
                    "category": "cardiovascular",
                    "title": "Good cholesterol levels",
                    "content": "Your cholesterol levels are within healthy range",
                    "confidence": 0.9,
                    "priority": "medium",
                    "actionable": True,
                    "severity": "normal",
                    "biomarkers_involved": ["cholesterol"],
                    "health_system": "cardiovascular",
                    "evidence": {"cholesterol": 180.0},
                    "recommendations": ["Maintain current lifestyle habits"]
                }
            ],
            "overall_score": 0.85,
            "result_version": "1.0.0",
            "confidence_score": 0.9,
            "processing_metadata": {
                "pipeline_version": "1.0.0",
                "processing_time": 5.0
            }
        }
        
        # Mock repository methods
        with patch.object(persistence_service.analysis_repo, 'upsert_by_analysis_id') as mock_upsert_analysis, \
             patch.object(persistence_service.analysis_result_repo, 'upsert_by_analysis_id') as mock_upsert_result, \
             patch.object(persistence_service.biomarker_score_repo, 'delete_by_analysis_id') as mock_delete_biomarkers, \
             patch.object(persistence_service.biomarker_score_repo, 'upsert_by_analysis_and_biomarker') as mock_upsert_biomarker, \
             patch.object(persistence_service.cluster_repo, 'delete_by_analysis_id') as mock_delete_clusters, \
             patch.object(persistence_service.cluster_repo, 'create') as mock_create_cluster, \
             patch.object(persistence_service.insight_repo, 'delete_by_analysis_id') as mock_delete_insights, \
             patch.object(persistence_service.insight_repo, 'create') as mock_create_insight, \
             patch.object(persistence_service.audit_log_repo, 'log_action') as mock_create_audit_log:
            
            # Mock analysis creation
            mock_analysis = Mock()
            mock_analysis.id = analysis_id
            mock_upsert_analysis.return_value = mock_analysis
            
            # Mock result creation
            mock_result = Mock()
            mock_upsert_result.return_value = mock_result
            
            # Mock biomarker scores creation
            mock_biomarker1 = Mock()
            mock_biomarker2 = Mock()
            mock_upsert_biomarker.side_effect = [mock_biomarker1, mock_biomarker2]
            
            # Mock clusters creation
            mock_cluster1 = Mock()
            mock_cluster2 = Mock()
            mock_create_cluster.side_effect = [mock_cluster1, mock_cluster2]
            
            # Mock insights creation
            mock_insight1 = Mock()
            mock_insight2 = Mock()
            mock_create_insight.side_effect = [mock_insight1, mock_insight2]
            
            # Mock audit log creation
            mock_audit_log = Mock()
            mock_create_audit_log.return_value = mock_audit_log
            
            # Act - Step 1: Save analysis
            analysis_result = persistence_service.save_analysis(analysis_dto, user_id)
            
            # Act - Step 2: Save results
            results_result = persistence_service.save_results(results_dto, analysis_id)
            
            # Assert - Analysis was saved
            assert analysis_result == analysis_id
            mock_upsert_analysis.assert_called_once()
            
            # Assert - Results were saved
            assert results_result is True
            mock_upsert_result.assert_called_once()
            mock_delete_biomarkers.assert_called_once_with(analysis_id)
            assert mock_upsert_biomarker.call_count == 2  # Two biomarkers
            mock_delete_clusters.assert_called_once_with(analysis_id)
            assert mock_create_cluster.call_count == 2  # Two clusters
            mock_delete_insights.assert_called_once_with(analysis_id)
            assert mock_create_insight.call_count == 2  # Two insights
            
            # Assert - Audit logs were created
            assert mock_create_audit_log.call_count >= 2  # At least one for analysis, one for results
    
    def test_analysis_history_retrieval_flow(self, persistence_service, mock_db_session):
        """Test analysis history retrieval flow."""
        # Arrange
        user_id = uuid4()
        analysis_id1 = uuid4()
        analysis_id2 = uuid4()
        
        mock_analyses = [
            Mock(
                id=analysis_id1,
                created_at=datetime.now(),
                status="completed",
                processing_time_seconds=5.0
            ),
            Mock(
                id=analysis_id2,
                created_at=datetime.now(),
                status="completed",
                processing_time_seconds=3.0
            )
        ]
        
        mock_results = [
            Mock(overall_score=0.85, confidence_score=0.9),
            Mock(overall_score=0.92, confidence_score=0.95)
        ]
        
        # Mock repository methods
        with patch.object(persistence_service.analysis_repo, 'get_recent_analyses') as mock_get_analyses, \
             patch.object(persistence_service.analysis_result_repo, 'get_by_analysis_id') as mock_get_result:
            
            mock_get_analyses.return_value = mock_analyses
            mock_get_result.side_effect = mock_results
            
            # Act
            history = persistence_service.get_analysis_history(user_id, limit=10, offset=0)
            
            # Assert
            assert len(history) == 2
            assert history[0]["analysis_id"] == str(analysis_id1)
            assert history[0]["overall_score"] == 0.85
            assert history[1]["analysis_id"] == str(analysis_id2)
            assert history[1]["overall_score"] == 0.92
            mock_get_analyses.assert_called_once_with(user_id, 10)
            assert mock_get_result.call_count == 2
    
    def test_analysis_result_retrieval_flow(self, persistence_service, mock_db_session):
        """Test analysis result retrieval flow."""
        # Arrange
        analysis_id = uuid4()
        
        mock_analysis = Mock(
            id=analysis_id,
            created_at=datetime.now(),
            status="completed",
            processing_time_seconds=5.0
        )
        
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
                interpretation="Within normal range",
                confidence=0.9,
                health_system="metabolic",
                critical_flag=False
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
    
    def test_export_creation_flow(self, persistence_service, mock_db_session):
        """Test export creation flow."""
        # Arrange
        user_id = uuid4()
        analysis_id = uuid4()
        
        export_dto = {
            "analysis_id": analysis_id,
            "export_type": "pdf",
            "status": "pending"
        }
        
        # Mock repository methods
        with patch.object(persistence_service.export_repo, 'create') as mock_create_export, \
             patch.object(persistence_service.audit_log_repo, 'log_action') as mock_create_audit_log:
            
            mock_export = Mock()
            mock_export.id = uuid4()
            mock_create_export.return_value = mock_export
            
            mock_audit_log = Mock()
            mock_create_audit_log.return_value = mock_audit_log
            
            # Act
            export_id = persistence_service.save_export(export_dto, user_id)
            
            # Assert
            assert export_id == mock_export.id
            mock_create_export.assert_called_once()
            mock_create_audit_log.assert_called_once()
