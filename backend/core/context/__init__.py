"""
Context Factory Package

This package provides the ContextFactory class for creating validated AnalysisContext objects
from raw data. It serves as the single entry point for data validation and context creation,
ensuring all data is properly structured before being passed to the orchestrator.

The factory handles:
- Raw data validation and conversion
- Biomarker panel creation
- User context creation
- Analysis context assembly
- Error handling and validation
- Backward compatibility during migration
"""

from .context_factory import ContextFactory, ContextFactoryError, ValidationError
from .models import AnalysisContext, UserContext, BiomarkerContext, BiomarkerPanel, ScoringMetrics, Sex

__all__ = [
    "ContextFactory",
    "ContextFactoryError", 
    "ValidationError",
    "AnalysisContext",
    "UserContext",
    "BiomarkerContext",
    "BiomarkerPanel",
    "ScoringMetrics",
    "Sex"
]
