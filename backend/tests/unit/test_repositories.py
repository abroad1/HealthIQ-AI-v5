"""
Unit tests for repository classes.
"""

import pytest
from unittest.mock import Mock, MagicMock
from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy.orm import Session

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
from core.models.database import Analysis, AnalysisResult, BiomarkerScore, Cluster, Insight, Export, Profile, AuditLog


class TestAnalysisRepository:
    """Test cases for AnalysisRepository."""
    
    @pytest.fixture
    def mock_db_session(self):
        """Mock database session."""
        return Mock(spec=Session)
    
    @pytest.fixture
    def analysis_repo(self, mock_db_session):
        """AnalysisRepository instance with mocked session."""
        return AnalysisRepository(mock_db_session)
    
    def test_create_analysis(self, analysis_repo, mock_db_session):
        """Test creating an analysis."""
        # Arrange
        analysis_data = {
            "id": uuid4(),
            "user_id": uuid4(),
            "status": "pending",
            "raw_biomarkers": {"glucose": 95.0},
            "analysis_version": "1.0.0",
            "pipeline_version": "1.0.0"
        }
        mock_analysis = Mock(spec=Analysis)
        mock_analysis.id = analysis_data["id"]
        mock_db_session.add.return_value = None
        mock_db_session.commit.return_value = None
        mock_db_session.refresh.return_value = None
        
        # Act
        result = analysis_repo.create(**analysis_data)
        
        # Assert
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()
        assert result is not None
    
    def test_get_by_id(self, analysis_repo, mock_db_session):
        """Test getting analysis by ID."""
        # Arrange
        analysis_id = uuid4()
        mock_analysis = Mock(spec=Analysis)
        mock_analysis.id = analysis_id
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_analysis
        mock_db_session.query.return_value = mock_query
        
        # Act
        result = analysis_repo.get_by_id(analysis_id)
        
        # Assert
        assert result == mock_analysis
        mock_db_session.query.assert_called_once_with(Analysis)
    
    def test_list_by_user_id(self, analysis_repo, mock_db_session):
        """Test listing analyses by user ID."""
        # Arrange
        user_id = uuid4()
        mock_analyses = [Mock(spec=Analysis), Mock(spec=Analysis)]
        mock_query = Mock()
        mock_query.filter.return_value.order_by.return_value.limit.return_value.offset.return_value.all.return_value = mock_analyses
        mock_db_session.query.return_value = mock_query
        
        # Act
        result = analysis_repo.list_by_user_id(user_id, limit=10, offset=0)
        
        # Assert
        assert result == mock_analyses
        mock_db_session.query.assert_called_once_with(Analysis)