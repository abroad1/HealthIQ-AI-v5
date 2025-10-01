"""
Analysis repository for database operations.
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from sqlalchemy.exc import SQLAlchemyError
import logging

from core.models.database import Analysis, AnalysisResult, BiomarkerScore, Cluster, Insight
from repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class AnalysisRepository(BaseRepository[Analysis]):
    """Repository for Analysis entities."""
    
    def __init__(self, db_session: Session):
        super().__init__(Analysis, db_session)
    
    def get_by_analysis_id(self, analysis_id: str) -> Optional[Analysis]:
        """
        Get analysis by analysis_id (string identifier).
        
        Args:
            analysis_id: Analysis identifier string
            
        Returns:
            Analysis instance or None if not found
        """
        try:
            return self.db_session.query(Analysis).filter(Analysis.id == UUID(analysis_id)).first()
        except (ValueError, SQLAlchemyError) as e:
            logger.error(f"Failed to get analysis by analysis_id {analysis_id}: {str(e)}")
            return None
    
    def list_by_user_id(self, user_id: UUID, limit: int = 100, offset: int = 0) -> List[Analysis]:
        """
        List analyses for a specific user.
        
        Args:
            user_id: User ID
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of analysis instances
        """
        return self.list_by_field("user_id", user_id, limit, offset)
    
    def list_by_status(self, status: str, limit: int = 100, offset: int = 0) -> List[Analysis]:
        """
        List analyses by status.
        
        Args:
            status: Analysis status
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of analysis instances
        """
        return self.list_by_field("status", status, limit, offset)
    
    def get_recent_analyses(self, user_id: UUID, limit: int = 10) -> List[Analysis]:
        """
        Get recent analyses for a user.
        
        Args:
            user_id: User ID
            limit: Maximum number of records to return
            
        Returns:
            List of recent analysis instances
        """
        try:
            return (
                self.db_session.query(Analysis)
                .filter(Analysis.user_id == user_id)
                .order_by(desc(Analysis.created_at))
                .limit(limit)
                .all()
            )
        except Exception as e:
            logger.error(f"Failed to get recent analyses for user {user_id}: {str(e)}")
            raise
    
    def upsert_by_analysis_id(self, analysis_id: str, **kwargs) -> Optional[Analysis]:
        """
        Upsert analysis by analysis_id.
        
        Args:
            analysis_id: Analysis identifier string
            **kwargs: Fields to set/update
            
        Returns:
            Analysis instance or None if invalid analysis_id
        """
        try:
            analysis_uuid = UUID(analysis_id)
            return self.upsert({"id": analysis_uuid}, **kwargs)
        except ValueError:
            logger.error(f"Invalid analysis_id format: {analysis_id}")
            return None
    
    def get_result_dto(self, analysis_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get analysis result DTO for export.
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            Result DTO dict or None if not found
        """
        try:
            # Get analysis
            analysis = self.db_session.query(Analysis).filter(Analysis.id == analysis_id).first()
            if not analysis:
                return None
            
            # Get result
            result = self.db_session.query(AnalysisResult).filter(AnalysisResult.analysis_id == analysis_id).first()
            if not result:
                return None
            
            # Get biomarker scores
            biomarker_scores = self.db_session.query(BiomarkerScore).filter(BiomarkerScore.analysis_id == analysis_id).all()
            
            # Get clusters
            clusters = self.db_session.query(Cluster).filter(Cluster.analysis_id == analysis_id).all()
            
            # Get insights
            insights = self.db_session.query(Insight).filter(Insight.analysis_id == analysis_id).all()
            
            # Build DTO
            return {
                "analysis_id": str(analysis_id),
                "user_id": str(analysis.user_id),
                "result_version": result.result_version,
                "biomarkers": [
                    {
                        "biomarker_name": bs.biomarker_name,
                        "value": bs.value,
                        "unit": bs.unit,
                        "score": bs.score,
                        "percentile": bs.percentile,
                        "status": bs.status,
                        "reference_range": bs.reference_range,
                        "interpretation": bs.interpretation,
                        "confidence": bs.confidence,
                        "health_system": bs.health_system,
                        "critical_flag": bs.critical_flag
                    }
                    for bs in biomarker_scores
                ],
                "clusters": [
                    {
                        "id": str(c.id),
                        "name": c.cluster_name,
                        "biomarkers": c.biomarkers,
                        "description": c.description,
                        "severity": c.severity,
                        "confidence": c.confidence
                    }
                    for c in clusters
                ],
                "insights": [
                    {
                        "id": str(i.id),
                        "title": i.title,
                        "content": i.content,
                        "category": i.category,
                        "confidence": i.confidence,
                        "severity": i.severity,
                        "biomarkers_involved": i.biomarkers_involved,
                        "recommendations": i.recommendations
                    }
                    for i in insights
                ],
                "recommendations": result.recommendations or [],
                "overall_score": result.overall_score,
                "meta": {
                    "result_version": result.result_version,
                    "confidence_score": result.confidence_score,
                    "processing_metadata": result.processing_metadata or {}
                },
                "created_at": result.created_at.isoformat() if result.created_at else None
            }
        except Exception as e:
            logger.error(f"Failed to get result DTO for analysis {analysis_id}: {str(e)}")
            return None
    
    def get_user_id_for_analysis(self, analysis_id: UUID) -> Optional[UUID]:
        """
        Get user ID for an analysis.
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            User ID or None if not found
        """
        try:
            analysis = self.db_session.query(Analysis).filter(Analysis.id == analysis_id).first()
            return analysis.user_id if analysis else None
        except Exception as e:
            logger.error(f"Failed to get user ID for analysis {analysis_id}: {str(e)}")
            return None


class AnalysisResultRepository(BaseRepository[AnalysisResult]):
    """Repository for AnalysisResult entities."""
    
    def __init__(self, db_session: Session):
        super().__init__(AnalysisResult, db_session)
    
    def get_by_analysis_id(self, analysis_id: UUID) -> Optional[AnalysisResult]:
        """
        Get analysis result by analysis ID.
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            AnalysisResult instance or None if not found
        """
        return self.get_by_field("analysis_id", analysis_id)
    
    def upsert_by_analysis_id(self, analysis_id: UUID, **kwargs) -> AnalysisResult:
        """
        Upsert analysis result by analysis ID.
        
        Args:
            analysis_id: Analysis ID
            **kwargs: Fields to set/update
            
        Returns:
            AnalysisResult instance
        """
        return self.upsert({"analysis_id": analysis_id}, **kwargs)


class BiomarkerScoreRepository(BaseRepository[BiomarkerScore]):
    """Repository for BiomarkerScore entities."""
    
    def __init__(self, db_session: Session):
        super().__init__(BiomarkerScore, db_session)
    
    def list_by_analysis_id(self, analysis_id: UUID) -> List[BiomarkerScore]:
        """
        List biomarker scores for an analysis.
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            List of biomarker score instances
        """
        return self.list_by_field("analysis_id", analysis_id)
    
    def get_by_analysis_and_biomarker(self, analysis_id: UUID, biomarker_name: str) -> Optional[BiomarkerScore]:
        """
        Get biomarker score by analysis ID and biomarker name.
        
        Args:
            analysis_id: Analysis ID
            biomarker_name: Biomarker name
            
        Returns:
            BiomarkerScore instance or None if not found
        """
        try:
            return (
                self.db_session.query(BiomarkerScore)
                .filter(
                    and_(
                        BiomarkerScore.analysis_id == analysis_id,
                        BiomarkerScore.biomarker_name == biomarker_name
                    )
                )
                .first()
            )
        except Exception as e:
            logger.error(f"Failed to get biomarker score for analysis {analysis_id}, biomarker {biomarker_name}: {str(e)}")
            raise
    
    def upsert_by_analysis_and_biomarker(self, analysis_id: UUID, biomarker_name: str, **kwargs) -> BiomarkerScore:
        """
        Upsert biomarker score by analysis ID and biomarker name.
        
        Args:
            analysis_id: Analysis ID
            biomarker_name: Biomarker name
            **kwargs: Fields to set/update
            
        Returns:
            BiomarkerScore instance
        """
        return self.upsert(
            {"analysis_id": analysis_id, "biomarker_name": biomarker_name},
            **kwargs
        )
    
    def delete_by_analysis_id(self, analysis_id: UUID) -> int:
        """
        Delete all biomarker scores for an analysis.
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            Number of deleted records
        """
        try:
            count = self.db_session.query(BiomarkerScore).filter(BiomarkerScore.analysis_id == analysis_id).count()
            self.db_session.query(BiomarkerScore).filter(BiomarkerScore.analysis_id == analysis_id).delete()
            self.db_session.commit()
            logger.info(f"Deleted {count} biomarker scores for analysis {analysis_id}")
            return count
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Failed to delete biomarker scores for analysis {analysis_id}: {str(e)}")
            raise


class ClusterRepository(BaseRepository[Cluster]):
    """Repository for Cluster entities."""
    
    def __init__(self, db_session: Session):
        super().__init__(Cluster, db_session)
    
    def list_by_analysis_id(self, analysis_id: UUID) -> List[Cluster]:
        """
        List clusters for an analysis.
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            List of cluster instances
        """
        return self.list_by_field("analysis_id", analysis_id)
    
    def list_by_analysis_and_type(self, analysis_id: UUID, cluster_type: str) -> List[Cluster]:
        """
        List clusters for an analysis by type.
        
        Args:
            analysis_id: Analysis ID
            cluster_type: Cluster type
            
        Returns:
            List of cluster instances
        """
        try:
            return (
                self.db_session.query(Cluster)
                .filter(
                    and_(
                        Cluster.analysis_id == analysis_id,
                        Cluster.cluster_type == cluster_type
                    )
                )
                .order_by(desc(Cluster.created_at))
                .all()
            )
        except Exception as e:
            logger.error(f"Failed to list clusters for analysis {analysis_id}, type {cluster_type}: {str(e)}")
            raise
    
    def delete_by_analysis_id(self, analysis_id: UUID) -> int:
        """
        Delete all clusters for an analysis.
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            Number of deleted records
        """
        try:
            count = self.db_session.query(Cluster).filter(Cluster.analysis_id == analysis_id).count()
            self.db_session.query(Cluster).filter(Cluster.analysis_id == analysis_id).delete()
            self.db_session.commit()
            logger.info(f"Deleted {count} clusters for analysis {analysis_id}")
            return count
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Failed to delete clusters for analysis {analysis_id}: {str(e)}")
            raise


class InsightRepository(BaseRepository[Insight]):
    """Repository for Insight entities."""
    
    def __init__(self, db_session: Session):
        super().__init__(Insight, db_session)
    
    def list_by_analysis_id(self, analysis_id: UUID) -> List[Insight]:
        """
        List insights for an analysis.
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            List of insight instances
        """
        return self.list_by_field("analysis_id", analysis_id)
    
    def list_by_analysis_and_category(self, analysis_id: UUID, category: str) -> List[Insight]:
        """
        List insights for an analysis by category.
        
        Args:
            analysis_id: Analysis ID
            category: Insight category
            
        Returns:
            List of insight instances
        """
        try:
            return (
                self.db_session.query(Insight)
                .filter(
                    and_(
                        Insight.analysis_id == analysis_id,
                        Insight.category == category
                    )
                )
                .order_by(desc(Insight.created_at))
                .all()
            )
        except Exception as e:
            logger.error(f"Failed to list insights for analysis {analysis_id}, category {category}: {str(e)}")
            raise
    
    def list_by_priority(self, analysis_id: UUID, priority: str) -> List[Insight]:
        """
        List insights for an analysis by priority.
        
        Args:
            analysis_id: Analysis ID
            priority: Insight priority
            
        Returns:
            List of insight instances
        """
        try:
            return (
                self.db_session.query(Insight)
                .filter(
                    and_(
                        Insight.analysis_id == analysis_id,
                        Insight.priority == priority
                    )
                )
                .order_by(desc(Insight.created_at))
                .all()
            )
        except Exception as e:
            logger.error(f"Failed to list insights for analysis {analysis_id}, priority {priority}: {str(e)}")
            raise
    
    def delete_by_analysis_id(self, analysis_id: UUID) -> int:
        """
        Delete all insights for an analysis.
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            Number of deleted records
        """
        try:
            count = self.db_session.query(Insight).filter(Insight.analysis_id == analysis_id).count()
            self.db_session.query(Insight).filter(Insight.analysis_id == analysis_id).delete()
            self.db_session.commit()
            logger.info(f"Deleted {count} insights for analysis {analysis_id}")
            return count
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Failed to delete insights for analysis {analysis_id}: {str(e)}")
            raise
