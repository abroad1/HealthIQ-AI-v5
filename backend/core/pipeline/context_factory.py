"""
Analysis context factory - creates immutable AnalysisContext objects.
"""

from datetime import datetime
from typing import Dict, Any, Optional

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
        analysis_parameters: Optional[Dict[str, Any]] = None
    ) -> AnalysisContext:
        """
        Create an immutable AnalysisContext.
        
        Args:
            analysis_id: Unique analysis identifier
            user: User information
            biomarker_panel: Normalized biomarker data
            analysis_parameters: Optional analysis configuration
            
        Returns:
            Immutable AnalysisContext
        """
        if analysis_parameters is None:
            analysis_parameters = {}
        
        return AnalysisContext(
            analysis_id=analysis_id,
            user=user,
            biomarker_panel=biomarker_panel,
            analysis_parameters=analysis_parameters,
            created_at=datetime.utcnow().isoformat(),
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
            created_at=user_data.get("created_at"),
            updated_at=user_data.get("updated_at")
        )
