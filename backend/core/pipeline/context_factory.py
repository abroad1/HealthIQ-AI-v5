"""
Analysis context factory - creates immutable AnalysisContext objects.
"""

from datetime import datetime, UTC
from typing import Dict, Any, Optional, List

from core.models.context import AnalysisContext
from core.models.user import User
from core.models.biomarker import BiomarkerPanel


class AnalysisContextFactory:
    """Factory for creating immutable AnalysisContext objects."""
    
    @staticmethod
    def create_context(
        analysis_id: str,
        user: User,
        biomarker_panel: BiomarkerPanel,
        analysis_parameters: Optional[Dict[str, Any]] = None,
        questionnaire_responses: Optional[Dict[str, Any]] = None,
        lifestyle_factors: Optional[Dict[str, Any]] = None,
        medical_history: Optional[Dict[str, Any]] = None
    ) -> AnalysisContext:
        """
        Create an immutable AnalysisContext.
        
        Args:
            analysis_id: Unique analysis identifier
            user: User information
            biomarker_panel: Normalized biomarker data
            analysis_parameters: Optional analysis configuration
            questionnaire_responses: Optional questionnaire responses
            lifestyle_factors: Optional mapped lifestyle factors
            medical_history: Optional mapped medical history
            
        Returns:
            Immutable AnalysisContext
        """
        if analysis_parameters is None:
            analysis_parameters = {}
        
        return AnalysisContext(
            analysis_id=analysis_id,
            user=user,
            biomarker_panel=biomarker_panel,
            questionnaire_responses=questionnaire_responses,
            lifestyle_factors=lifestyle_factors,
            medical_history=medical_history,
            analysis_parameters=analysis_parameters,
            created_at=datetime.now(UTC).isoformat(),
            version="1.0"
        )
    
    @staticmethod
    def create_user_from_dict(user_data: Dict[str, Any]) -> User:
        """
        Create a User object from dictionary data.
        
        Args:
            user_data: Raw user data dictionary
            
        Returns:
            Immutable User object
        """
        return User(
            user_id=user_data.get("user_id", ""),
            email=user_data.get("email"),
            age=user_data.get("age"),
            gender=user_data.get("gender"),
            height=user_data.get("height"),
            weight=user_data.get("weight"),
            ethnicity=user_data.get("ethnicity"),
            medical_history=user_data.get("medical_history", {}),
            medications=user_data.get("medications", []),
            lifestyle_factors=user_data.get("lifestyle_factors", {}),
            questionnaire=user_data.get("questionnaire", {}),
            created_at=user_data.get("created_at"),
            updated_at=user_data.get("updated_at")
        )
    
    @staticmethod
    def create_context_with_insights(
        analysis_id: str,
        user: User,
        biomarker_panel: BiomarkerPanel,
        analysis_parameters: Optional[Dict[str, Any]] = None,
        insights: Optional[List[Dict[str, Any]]] = None
    ) -> AnalysisContext:
        """
        Create an AnalysisContext with pre-computed insights.
        
        Args:
            analysis_id: Unique analysis identifier
            user: User information
            biomarker_panel: Normalized biomarker data
            analysis_parameters: Optional analysis configuration
            insights: Optional pre-computed insights
            
        Returns:
            AnalysisContext with insights included in parameters
        """
        if analysis_parameters is None:
            analysis_parameters = {}
        
        # Add insights to analysis parameters if provided
        if insights:
            analysis_parameters["insights"] = insights
        
        return AnalysisContext(
            analysis_id=analysis_id,
            user=user,
            biomarker_panel=biomarker_panel,
            analysis_parameters=analysis_parameters,
            created_at=datetime.now(UTC).isoformat(),
            version="1.0"
        )
    
    @staticmethod
    def extract_lifestyle_profile(context: AnalysisContext) -> Dict[str, Any]:
        """
        Extract lifestyle profile from analysis context for insight synthesis.
        
        Args:
            context: Analysis context
            
        Returns:
            Lifestyle profile dictionary
        """
        lifestyle_profile = {}
        
        # Extract from user lifestyle factors
        if hasattr(context.user, 'lifestyle_factors') and context.user.lifestyle_factors:
            lifestyle_profile.update(context.user.lifestyle_factors)
        
        # Extract from questionnaire if available
        if hasattr(context.user, 'questionnaire') and context.user.questionnaire:
            questionnaire = context.user.questionnaire
            
            # Map questionnaire responses to lifestyle factors
            if "diet_level" in questionnaire:
                lifestyle_profile["diet_level"] = questionnaire["diet_level"]
            if "sleep_hours" in questionnaire:
                lifestyle_profile["sleep_hours"] = questionnaire["sleep_hours"]
            if "exercise_minutes_per_week" in questionnaire:
                lifestyle_profile["exercise_minutes_per_week"] = questionnaire["exercise_minutes_per_week"]
            if "alcohol_units_per_week" in questionnaire:
                lifestyle_profile["alcohol_units_per_week"] = questionnaire["alcohol_units_per_week"]
            if "smoking_status" in questionnaire:
                lifestyle_profile["smoking_status"] = questionnaire["smoking_status"]
            if "stress_level" in questionnaire:
                lifestyle_profile["stress_level"] = questionnaire["stress_level"]
        
        return lifestyle_profile
    
    @staticmethod
    def extract_biomarker_scores(context: AnalysisContext) -> Dict[str, Any]:
        """
        Extract biomarker scores from analysis context for insight synthesis.
        
        Args:
            context: Analysis context
            
        Returns:
            Biomarker scores dictionary
        """
        biomarker_scores = {}
        
        # Extract from analysis parameters if available
        if "biomarker_scores" in context.analysis_parameters:
            biomarker_scores = context.analysis_parameters["biomarker_scores"]
        
        return biomarker_scores
    
    @staticmethod
    def extract_clustering_results(context: AnalysisContext) -> Dict[str, Any]:
        """
        Extract clustering results from analysis context for insight synthesis.
        
        Args:
            context: Analysis context
            
        Returns:
            Clustering results dictionary
        """
        clustering_results = {}
        
        # Extract from analysis parameters if available
        if "clustering_results" in context.analysis_parameters:
            clustering_results = context.analysis_parameters["clustering_results"]
        
        return clustering_results