"""
Persistence service for orchestration-level database operations.
"""

from typing import Dict, Any, Optional, List
from uuid import UUID, uuid4
from datetime import datetime, UTC
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from core.models.results import AnalysisResult as AnalysisResultDTO
from core.models.context import AnalysisContext
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

logger = logging.getLogger(__name__)


class PersistenceService:
    """Service for orchestration-level persistence operations."""
    
    def __init__(self, db_session: Session):
        """
        Initialize the persistence service.
        
        Args:
            db_session: Database session
        """
        self.db_session = db_session
        self.analysis_repo = AnalysisRepository(db_session)
        self.analysis_result_repo = AnalysisResultRepository(db_session)
        self.biomarker_score_repo = BiomarkerScoreRepository(db_session)
        self.cluster_repo = ClusterRepository(db_session)
        self.insight_repo = InsightRepository(db_session)
        self.export_repo = ExportRepository(db_session)
        self.profile_repo = ProfileRepository(db_session)
        self.audit_log_repo = AuditLogRepository(db_session)
    
    def save_analysis(self, analysis_dto: Dict[str, Any], user_id: UUID) -> Optional[UUID]:
        """
        Save analysis data to database.
        
        Args:
            analysis_dto: Analysis data transfer object
            user_id: User ID
            
        Returns:
            Analysis ID if successful, None if failed
        """
        try:
            analysis_id = analysis_dto.get("analysis_id")
            if not analysis_id:
                logger.error("Analysis ID is required for persistence")
                return None
            
            # Convert string analysis_id to UUID if needed
            if isinstance(analysis_id, str):
                analysis_id = UUID(analysis_id)
            
            # Create or update analysis record
            analysis_data = {
                "id": analysis_id,
                "user_id": user_id,
                "status": analysis_dto.get("status", "completed"),
                "raw_biomarkers": analysis_dto.get("raw_biomarkers"),
                "questionnaire_data": analysis_dto.get("questionnaire_data"),
                "processing_time_seconds": analysis_dto.get("processing_time_seconds"),
                "analysis_version": analysis_dto.get("analysis_version", "1.0.0"),
                "pipeline_version": analysis_dto.get("pipeline_version", "1.0.0"),
                "completed_at": datetime.now(UTC) if analysis_dto.get("status") == "completed" else None
            }
            
            analysis = self.analysis_repo.upsert_by_analysis_id(str(analysis_id), **analysis_data)
            
            if analysis:
                logger.info(f"Successfully saved analysis {analysis_id}")
                self._log_audit_action(
                    action="analysis_saved",
                    resource_type="analysis",
                    resource_id=analysis_id,
                    user_id=user_id,
                    details={"status": analysis_dto.get("status")}
                )
                return analysis_id
            else:
                logger.error(f"Failed to save analysis {analysis_id}")
                return None
                
        except Exception as e:
            logger.error(f"Error saving analysis: {str(e)}")
            self._log_audit_action(
                action="analysis_save_failed",
                resource_type="analysis",
                user_id=user_id,
                details={"error": str(e)},
                severity="error",
                outcome="failure"
            )
            return None
    
    def save_results(self, results_dto: Dict[str, Any], analysis_id: UUID) -> bool:
        """
        Save analysis results to database.
        
        Args:
            results_dto: Results data transfer object
            analysis_id: Analysis ID
            
        Returns:
            True if successful, False if failed
        """
        try:
            # Save main analysis result
            result_data = {
                "biomarkers": results_dto.get("biomarkers"),
                "clusters": results_dto.get("clusters"),
                "insights": results_dto.get("insights"),
                "overall_score": results_dto.get("overall_score"),
                "risk_assessment": results_dto.get("risk_assessment"),
                "recommendations": results_dto.get("recommendations"),
                "result_version": results_dto.get("result_version", "1.0.0"),
                "confidence_score": results_dto.get("confidence_score"),
                "processing_metadata": results_dto.get("processing_metadata")
            }
            
            analysis_result = self.analysis_result_repo.upsert_by_analysis_id(analysis_id, **result_data)
            
            if not analysis_result:
                logger.error(f"Failed to save analysis result for {analysis_id}")
                return False
            
            # Save individual biomarker scores
            biomarkers = results_dto.get("biomarkers", [])
            if biomarkers:
                # Clear existing biomarker scores
                self.biomarker_score_repo.delete_by_analysis_id(analysis_id)
                
                for biomarker in biomarkers:
                    biomarker_data = {
                        "biomarker_name": biomarker.get("biomarker_name"),
                        "value": biomarker.get("value"),
                        "unit": biomarker.get("unit"),
                        "score": biomarker.get("score"),
                        "percentile": biomarker.get("percentile"),
                        "status": biomarker.get("status"),
                        "reference_range": biomarker.get("reference_range"),
                        "interpretation": biomarker.get("interpretation"),
                        "confidence": biomarker.get("confidence"),
                        "health_system": biomarker.get("health_system"),
                        "critical_flag": biomarker.get("critical_flag", False)
                    }
                    self.biomarker_score_repo.upsert_by_analysis_and_biomarker(
                        analysis_id, biomarker_data["biomarker_name"], **biomarker_data
                    )
            
            # Save clusters
            clusters = results_dto.get("clusters", [])
            if clusters:
                # Clear existing clusters
                self.cluster_repo.delete_by_analysis_id(analysis_id)
                
                for cluster in clusters:
                    cluster_data = {
                        "cluster_name": cluster.get("cluster_name"),
                        "cluster_type": cluster.get("cluster_type"),
                        "score": cluster.get("score"),
                        "confidence": cluster.get("confidence"),
                        "biomarkers": cluster.get("biomarkers"),
                        "insights": cluster.get("insights"),
                        "severity": cluster.get("severity"),
                        "description": cluster.get("description"),
                        "health_system": cluster.get("health_system"),
                        "algorithm_used": cluster.get("algorithm_used")
                    }
                    self.cluster_repo.create(**cluster_data)
            
            # Save insights
            insights = results_dto.get("insights", [])
            if insights:
                # Clear existing insights
                self.insight_repo.delete_by_analysis_id(analysis_id)
                
                for insight in insights:
                    # Handle both old and new insight formats
                    insight_data = {
                        "insight_type": insight.get("insight_type", insight.get("id", "unknown")),
                        "category": insight.get("category", "unknown"),
                        "title": insight.get("title", insight.get("summary", "")),
                        "content": insight.get("content", insight.get("description", "")),
                        "confidence": insight.get("confidence", 0.0),
                        "priority": insight.get("priority", "medium"),
                        "actionable": insight.get("actionable", True),
                        "severity": insight.get("severity", "info"),
                        "biomarkers_involved": insight.get("biomarkers_involved", []),
                        "health_system": insight.get("health_system", "general"),
                        "evidence": insight.get("evidence", {}),
                        "recommendations": insight.get("recommendations", []),
                        "source": insight.get("source", "unknown"),
                        "version": insight.get("version", "v1.0.0")
                    }
                    self.insight_repo.create(**insight_data)
            
            logger.info(f"Successfully saved results for analysis {analysis_id}")
            self._log_audit_action(
                action="results_saved",
                resource_type="analysis_result",
                resource_id=analysis_id,
                details={
                    "biomarkers_count": len(biomarkers),
                    "clusters_count": len(clusters),
                    "insights_count": len(insights)
                }
            )
            return True
            
        except Exception as e:
            logger.error(f"Error saving results for analysis {analysis_id}: {str(e)}")
            self._log_audit_action(
                action="results_save_failed",
                resource_type="analysis_result",
                resource_id=analysis_id,
                details={"error": str(e)},
                severity="error",
                outcome="failure"
            )
            return False
    
    def save_insights(self, insights_dto: Dict[str, Any], analysis_id: UUID) -> bool:
        """
        Save insights data to database.
        
        Args:
            insights_dto: Insights data transfer object
            analysis_id: Analysis ID
            
        Returns:
            True if successful, False if failed
        """
        try:
            insights = insights_dto.get("insights", [])
            if not insights:
                logger.warning(f"No insights to save for analysis {analysis_id}")
                return True
            
            # Clear existing insights
            self.insight_repo.delete_by_analysis_id(analysis_id)
            
            for insight in insights:
                insight_data = {
                    "insight_type": insight.get("insight_type"),
                    "category": insight.get("category"),
                    "title": insight.get("title"),
                    "content": insight.get("content"),
                    "confidence": insight.get("confidence"),
                    "priority": insight.get("priority"),
                    "actionable": insight.get("actionable", True),
                    "severity": insight.get("severity"),
                    "biomarkers_involved": insight.get("biomarkers_involved"),
                    "health_system": insight.get("health_system"),
                    "evidence": insight.get("evidence"),
                    "recommendations": insight.get("recommendations")
                }
                self.insight_repo.create(**insight_data)
            
            logger.info(f"Successfully saved {len(insights)} insights for analysis {analysis_id}")
            self._log_audit_action(
                action="insights_saved",
                resource_type="insight",
                resource_id=analysis_id,
                details={"insights_count": len(insights)}
            )
            return True
            
        except Exception as e:
            logger.error(f"Error saving insights for analysis {analysis_id}: {str(e)}")
            self._log_audit_action(
                action="insights_save_failed",
                resource_type="insight",
                resource_id=analysis_id,
                details={"error": str(e)},
                severity="error",
                outcome="failure"
            )
            return False
    
    def save_export(self, export_dto: Dict[str, Any], user_id: UUID) -> Optional[UUID]:
        """
        Save export data to database.
        
        Args:
            export_dto: Export data transfer object
            user_id: User ID
            
        Returns:
            Export ID if successful, None if failed
        """
        try:
            export_data = {
                "user_id": user_id,
                "analysis_id": export_dto.get("analysis_id"),
                "export_type": export_dto.get("export_type"),
                "status": export_dto.get("status", "pending"),
                "file_path": export_dto.get("file_path"),
                "file_size_bytes": export_dto.get("file_size_bytes"),
                "download_url": export_dto.get("download_url"),
                "expires_at": export_dto.get("expires_at"),
                "error_message": export_dto.get("error_message"),
                "processing_metadata": export_dto.get("processing_metadata")
            }
            
            export = self.export_repo.create(**export_data)
            
            if export:
                logger.info(f"Successfully saved export {export.id}")
                self._log_audit_action(
                    action="export_saved",
                    resource_type="export",
                    resource_id=export.id,
                    user_id=user_id,
                    details={"export_type": export_dto.get("export_type")}
                )
                return export.id
            else:
                logger.error("Failed to save export")
                return None
                
        except Exception as e:
            logger.error(f"Error saving export: {str(e)}")
            self._log_audit_action(
                action="export_save_failed",
                resource_type="export",
                user_id=user_id,
                details={"error": str(e)},
                severity="error",
                outcome="failure"
            )
            return None
    
    def get_analysis_history(self, user_id: UUID, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get analysis history for a user.
        
        Args:
            user_id: User ID
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of analysis summary dictionaries
        """
        try:
            analyses = self.analysis_repo.get_recent_analyses(user_id, limit)
            
            history = []
            for analysis in analyses:
                # Get overall score from analysis result
                result = self.analysis_result_repo.get_by_analysis_id(analysis.id)
                overall_score = result.overall_score if result else None
                
                history.append({
                    "analysis_id": str(analysis.id),
                    "created_at": analysis.created_at.isoformat(),
                    "status": analysis.status,
                    "overall_score": overall_score,
                    "processing_time_seconds": analysis.processing_time_seconds
                })
            
            return history
            
        except Exception as e:
            logger.error(f"Error getting analysis history for user {user_id}: {str(e)}")
            return []
    
    def get_analysis_result(self, analysis_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get analysis result from database.
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            Analysis result dictionary or None if not found
        """
        try:
            analysis = self.analysis_repo.get_by_id(analysis_id)
            if not analysis:
                return None
            
            result = self.analysis_result_repo.get_by_analysis_id(analysis_id)
            if not result:
                return None
            
            # Get biomarker scores
            biomarker_scores = self.biomarker_score_repo.list_by_analysis_id(analysis_id)
            biomarkers = []
            for score in biomarker_scores:
                biomarkers.append({
                    "biomarker_name": score.biomarker_name,
                    "value": score.value,
                    "unit": score.unit,
                    "score": score.score,
                    "percentile": score.percentile,
                    "status": score.status,
                    "reference_range": score.reference_range,
                    "interpretation": score.interpretation
                })
            
            # Get clusters
            clusters = self.cluster_repo.list_by_analysis_id(analysis_id)
            cluster_list = []
            for cluster in clusters:
                cluster_list.append({
                    "cluster_id": str(cluster.id),
                    "name": cluster.cluster_name,
                    "biomarkers": cluster.biomarkers or [],
                    "description": cluster.description,
                    "severity": cluster.severity,
                    "confidence": cluster.confidence
                })
            
            # Get insights
            insights = self.insight_repo.list_by_analysis_id(analysis_id)
            insight_list = []
            for insight in insights:
                insight_list.append({
                    "insight_id": str(insight.id),
                    "title": insight.title,
                    "description": insight.content,
                    "category": insight.category,
                    "confidence": insight.confidence,
                    "severity": insight.severity,
                    "biomarkers": insight.biomarkers_involved or [],
                    "recommendations": insight.recommendations or []
                })
            
            return {
                "analysis_id": str(analysis_id),
                "result_version": result.result_version,
                "biomarkers": biomarkers,
                "clusters": cluster_list,
                "insights": insight_list,
                "recommendations": result.recommendations or [],
                "overall_score": result.overall_score,
                "meta": {
                    "confidence_score": result.confidence_score,
                    "processing_metadata": result.processing_metadata
                },
                "created_at": result.created_at.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting analysis result for {analysis_id}: {str(e)}")
            return None
    
    def _log_audit_action(self, action: str, resource_type: str, user_id: UUID = None, 
                         resource_id: UUID = None, details: Dict[str, Any] = None,
                         severity: str = "info", outcome: str = "success"):
        """
        Log an action to the audit trail.
        
        Args:
            action: Action name
            resource_type: Resource type
            user_id: User ID (optional)
            resource_id: Resource ID (optional)
            details: Additional details (optional)
            severity: Severity level (optional)
            outcome: Outcome (optional)
        """
        try:
            self.audit_log_repo.log_action(
                action=action,
                resource_type=resource_type,
                user_id=user_id,
                resource_id=resource_id,
                details=details,
                severity=severity,
                outcome=outcome
            )
        except Exception as e:
            logger.error(f"Failed to log audit action {action}: {str(e)}")
            # Don't raise here to avoid breaking the main operation
