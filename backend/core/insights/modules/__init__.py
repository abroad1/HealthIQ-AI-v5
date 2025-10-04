"""
Insight modules package - auto-import all modules for registry.
"""

# Import all insight modules to trigger registration
from . import metabolic_age
from . import heart_insight
from . import inflammation
from . import fatigue_root_cause
from . import detox_filtration

__all__ = [
    "metabolic_age",
    "heart_insight",
    "inflammation",
    "fatigue_root_cause",
    "detox_filtration",
]
