"""
Analysis service - handles biomarker analysis operations.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from core.models.biomarker import BiomarkerPanel, BiomarkerValue
from core.models.user import User
from core.models.context import AnalysisContext
from core.models.results import AnalysisResult, AnalysisDTO
from core.pipeline.orchestrator import AnalysisOrchestrator
from core.canonical.resolver import CanonicalResolver


class AnalysisService:
    """Service for handling biomarker analysis operations."""
    
    def __init__(self):
        """Initialize the analysis service."""
        self.orchestrator = AnalysisOrchestrator()
        self.resolver = CanonicalResolver()
        # In-memory storage for demo purposes - replace with database in production
        self._analysis_results: Dict[str, AnalysisResult] = {}
        self._analysis_status: Dict[str, Dict[str, Any]] = {}
    
    async def start_analysis(
        self,
        biomarkers: Dict[str, Any], 
        user_data: Dict[str, Any]
    ) -> str:
        """
        Start a new biomarker analysis.
        
        Args:
            biomarkers: Raw biomarker data (may contain aliases)
            user_data: User information for context
            
        Returns:
            Analysis ID for tracking the analysis
        """
        # Generate unique analysis ID
        analysis_id = str(uuid.uuid4())
        
        # Validate and normalize biomarkers
        try:
            biomarker_panel, unmapped_keys = self.orchestrator.normalizer.normalize_biomarkers(biomarkers)
            
            # Log unmapped biomarkers
            if unmapped_keys:
                print(f"Warning: Unmapped biomarker keys in analysis {analysis_id}: {unmapped_keys}")
            
            # Create user object
            user = User(
                user_id=user_data.get("user_id", "anonymous"),
                email=user_data.get("email"),
                age=user_data.get("age"),
                gender=user_data.get("gender"),
                height=user_data.get("height"),
                weight=user_data.get("weight"),
                ethnicity=user_data.get("ethnicity"),
                medical_history=user_data.get("medical_history", {}),
                medications=user_data.get("medications", []),
                lifestyle_factors=user_data.get("lifestyle_factors", {}),
                created_at=datetime.now(timezone.utc).isoformat()
            )
            
            # Create analysis context
            context = self.orchestrator.create_analysis_context(
                analysis_id=analysis_id,
                raw_biomarkers=biomarkers,
                user_data=user_data,
                assume_canonical=False
            )
            
            # Initialize analysis status
            self._analysis_status[analysis_id] = {
                "status": "processing",
                "progress": 0,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "user_id": user.user_id,
                "biomarker_count": len(biomarker_panel.biomarkers),
                "unmapped_biomarkers": unmapped_keys
            }
            
            # Run analysis (this would typically be queued as a background job)
            await self._process_analysis(analysis_id, context)
            
            return analysis_id
            
        except Exception as e:
            # Update status to error
            self._analysis_status[analysis_id] = {
                "status": "error",
                "error": str(e),
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            raise
    
    async def get_analysis_result(self, analysis_id: str) -> Optional[AnalysisResult]:
        """
        Get analysis result by ID.
        
        Args:
            analysis_id: Analysis identifier
            
        Returns:
            AnalysisResult or None if not found
        """
        return self._analysis_results.get(analysis_id)
    
    async def get_analysis_status(self, analysis_id: str) -> Dict[str, Any]:
        """
        Get analysis status and progress.
        
        Args:
            analysis_id: Analysis identifier
            
        Returns:
            Dictionary with status and progress information
        """
        return self._analysis_status.get(analysis_id, {"status": "not_found"})
    
    async def get_user_analysis_history(self, user_id: str) -> List[AnalysisResult]:
        """
        Get analysis history for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of AnalysisResult objects for the user
        """
        user_results = []
        for result in self._analysis_results.values():
            if result.user_id == user_id:
                user_results.append(result)
        
        # Sort by creation date (newest first)
        user_results.sort(key=lambda x: x.created_at, reverse=True)
        return user_results
    
    async def _process_analysis(self, analysis_id: str, context: AnalysisContext) -> None:
        """
        Process the analysis using the orchestrator.
        
        Args:
            analysis_id: Analysis identifier
            context: Analysis context with normalized biomarkers
        """
        try:
            # Update status to processing
            self._analysis_status[analysis_id]["status"] = "processing"
            self._analysis_status[analysis_id]["progress"] = 25
            
            # Run the analysis pipeline
            result_dto = self.orchestrator.run(
                biomarkers=context.biomarker_panel.biomarkers,
                user=context.user.__dict__,
                assume_canonical=True
            )
            
            # Update status to processing
            self._analysis_status[analysis_id]["progress"] = 75
            
            # Create analysis result
            analysis_result = AnalysisResult(
                analysis_id=analysis_id,
                user_id=context.user.user_id,
                biomarkers=context.biomarker_panel.biomarkers,
                clusters=result_dto.clusters,
                insights=result_dto.insights,
                status="completed",
                created_at=datetime.now(timezone.utc).isoformat(),
                completed_at=datetime.now(timezone.utc).isoformat(),
                confidence_score=self._calculate_confidence_score(context.biomarker_panel)
            )
            
            # Store result
            self._analysis_results[analysis_id] = analysis_result
            
            # Update status to completed
            self._analysis_status[analysis_id]["status"] = "completed"
            self._analysis_status[analysis_id]["progress"] = 100
            self._analysis_status[analysis_id]["completed_at"] = datetime.now(timezone.utc).isoformat()
            
        except Exception as e:
            # Update status to error
            self._analysis_status[analysis_id]["status"] = "error"
            self._analysis_status[analysis_id]["error"] = str(e)
            self._analysis_status[analysis_id]["failed_at"] = datetime.now(timezone.utc).isoformat()
            raise
    
    def _calculate_confidence_score(self, biomarker_panel: BiomarkerPanel) -> float:
        """
        Calculate confidence score based on biomarker completeness and quality.
        
        Args:
            biomarker_panel: Normalized biomarker panel
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        # Get all available biomarkers
        all_biomarkers = self.resolver.load_biomarkers()
        total_available = len(all_biomarkers)
        
        # Count biomarkers in panel
        panel_count = len(biomarker_panel.biomarkers)
        
        # Calculate completeness score
        completeness_score = panel_count / total_available if total_available > 0 else 0.0
        
        # Calculate quality score based on data validation
        quality_score = 1.0
        for biomarker_name, biomarker_value in biomarker_panel.biomarkers.items():
            # Validate each biomarker value
            validation_result = self.resolver.validate_biomarker_value(
                biomarker_name=biomarker_name,
                value=float(biomarker_value.value) if isinstance(biomarker_value.value, (int, float)) else 0.0,
                unit=biomarker_value.unit
            )
            
            # Reduce quality score for invalid values
            if validation_result["status"] == "conversion_error":
                quality_score -= 0.1
            elif validation_result["status"] == "unknown":
                quality_score -= 0.05
        
        # Ensure quality score doesn't go below 0
        quality_score = max(0.0, quality_score)
        
        # Combine scores (70% completeness, 30% quality)
        confidence_score = (completeness_score * 0.7) + (quality_score * 0.3)
        
        return round(confidence_score, 3)
    
    async def validate_biomarker_panel(self, biomarkers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a biomarker panel before analysis.
        
        Args:
            biomarkers: Raw biomarker data
            
        Returns:
            Validation results with recommendations
        """
        try:
            # Normalize biomarkers
            biomarker_panel, unmapped_keys = self.orchestrator.normalizer.normalize_biomarkers(biomarkers)
            
            # Validate each biomarker
            validation_results = {}
            for biomarker_name, biomarker_value in biomarker_panel.biomarkers.items():
                validation_result = self.resolver.validate_biomarker_value(
                    biomarker_name=biomarker_name,
                    value=float(biomarker_value.value) if isinstance(biomarker_value.value, (int, float)) else 0.0,
                    unit=biomarker_value.unit
                )
                validation_results[biomarker_name] = validation_result
            
            # Calculate overall validation score
            total_biomarkers = len(validation_results)
            valid_biomarkers = sum(1 for result in validation_results.values() if result["status"] == "normal")
            validation_score = valid_biomarkers / total_biomarkers if total_biomarkers > 0 else 0.0
            
            return {
                "valid": validation_score >= 0.8,  # 80% threshold
                "score": validation_score,
                "total_biomarkers": total_biomarkers,
                "valid_biomarkers": valid_biomarkers,
                "unmapped_biomarkers": unmapped_keys,
                "validation_results": validation_results,
                "recommendations": self._generate_validation_recommendations(validation_results, unmapped_keys)
            }
            
        except Exception as e:
            return {
                "valid": False,
                "score": 0.0,
                "error": str(e),
                "total_biomarkers": 0,
                "valid_biomarkers": 0,
                "unmapped_biomarkers": [],
                "validation_results": {},
                "recommendations": ["Analysis validation failed due to technical error"]
            }
    
    def _generate_validation_recommendations(
        self, 
        validation_results: Dict[str, Any], 
        unmapped_keys: List[str]
    ) -> List[str]:
        """
        Generate recommendations based on validation results.
        
        Args:
            validation_results: Validation results for each biomarker
            unmapped_keys: List of unmapped biomarker keys
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Check for unmapped biomarkers
        if unmapped_keys:
            recommendations.append(f"Consider adding definitions for unmapped biomarkers: {', '.join(unmapped_keys[:5])}")
        
        # Check for abnormal values
        abnormal_biomarkers = [
            name for name, result in validation_results.items() 
            if result["status"] in ["low", "high"]
        ]
        if abnormal_biomarkers:
            recommendations.append(f"Review abnormal values for: {', '.join(abnormal_biomarkers[:5])}")
        
        # Check for conversion errors
        conversion_errors = [
            name for name, result in validation_results.items() 
            if result["status"] == "conversion_error"
        ]
        if conversion_errors:
            recommendations.append(f"Verify units for: {', '.join(conversion_errors[:5])}")
        
        # Check for missing reference ranges
        unknown_ranges = [
            name for name, result in validation_results.items() 
            if result["status"] == "unknown"
        ]
        if unknown_ranges:
            recommendations.append(f"Reference ranges not available for: {', '.join(unknown_ranges[:5])}")
        
        return recommendations