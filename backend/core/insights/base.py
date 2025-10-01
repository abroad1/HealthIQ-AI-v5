"""
Base insight classes - abstract base for modular biomarker insights.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

from core.models.context import AnalysisContext
from core.insights.metadata import InsightMetadata, InsightResult


class BaseInsight(ABC):
    """Abstract base class for modular biomarker insights."""
    
    @property
    @abstractmethod
    def metadata(self) -> InsightMetadata:
        """Return insight metadata including ID, version, etc."""
        pass
    
    @abstractmethod
    def analyze(self, context: AnalysisContext) -> List[InsightResult]:
        """
        Analyze context and return structured results. Never raise exceptions.
        
        Args:
            context: Analysis context with user and biomarker data
            
        Returns:
            List of structured insight results
        """
        pass
    
    def can_analyze(self, context: AnalysisContext) -> bool:
        """
        Check if this insight can analyze the given context.
        
        Args:
            context: Analysis context to check
            
        Returns:
            True if analysis is possible, False otherwise
        """
        required = set(self.metadata.required_biomarkers)
        available = set(context.biomarker_panel.biomarkers.keys())
        return required.issubset(available)


# Contract Rule: All insights must consume only AnalysisContext. 
# Legacy ScoredContext is fully deprecated and unsupported.
