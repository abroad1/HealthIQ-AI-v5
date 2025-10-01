"""
Versioned insight registry for modular insights engine.
"""

from typing import Dict, List, Type, Optional
from core.insights.base import BaseInsight


class InsightRegistry:
    """Registry for versioned insight modules with duplicate prevention."""
    
    def __init__(self):
        self._registry: Dict[str, Dict[str, Type[BaseInsight]]] = {}
        self._instances: Dict[str, Dict[str, BaseInsight]] = {}
    
    def register(self, insight_id: str, version: str, insight_class: Type[BaseInsight]) -> None:
        """
        Register an insight class with version.
        
        Args:
            insight_id: Unique insight identifier (lowercase snake_case)
            version: SemVer version string
            insight_class: Insight class to register
            
        Raises:
            ValueError: If (insight_id, version) already registered
        """
        if insight_id not in self._registry:
            self._registry[insight_id] = {}
            self._instances[insight_id] = {}
        
        if version in self._registry[insight_id]:
            raise ValueError(f"Insight {insight_id} version {version} already registered")
        
        self._registry[insight_id][version] = insight_class
    
    def get(self, insight_id: str, version: str) -> BaseInsight:
        """
        Get insight instance by ID and version.
        
        Args:
            insight_id: Insight identifier
            version: Version string
            
        Returns:
            Insight instance
            
        Raises:
            KeyError: If insight not found
        """
        if insight_id not in self._registry:
            raise KeyError(f"Insight {insight_id} not registered")
        
        if version not in self._registry[insight_id]:
            raise KeyError(f"Insight {insight_id} version {version} not registered")
        
        # Return cached instance or create new one
        if version not in self._instances[insight_id]:
            insight_class = self._registry[insight_id][version]
            self._instances[insight_id][version] = insight_class()
        
        return self._instances[insight_id][version]
    
    def get_all(self) -> List[BaseInsight]:
        """Get all registered insight instances."""
        instances = []
        for insight_id in self._registry:
            for version in self._registry[insight_id]:
                instances.append(self.get(insight_id, version))
        return instances
    
    def list_versions(self, insight_id: str) -> List[str]:
        """List all versions for an insight ID."""
        if insight_id not in self._registry:
            return []
        return list(self._registry[insight_id].keys())
    
    def is_registered(self, insight_id: str, version: str) -> bool:
        """Check if insight is registered."""
        return (insight_id in self._registry and 
                version in self._registry[insight_id])
    
    def ensure_insights_registered(self) -> None:
        """Explicit import trigger to ensure all insights are registered."""
        # This will be called after importing all insight modules
        pass
    
    def assert_registered(self, insight_id: str, version: str) -> None:
        """
        Assert that insight is registered, fail fast if not.
        
        Args:
            insight_id: Insight identifier
            version: Version string
            
        Raises:
            KeyError: If insight not registered
        """
        if not self.is_registered(insight_id, version):
            raise KeyError(f"Insight {insight_id} version {version} not registered")


# Global registry instance
insight_registry = InsightRegistry()


def ensure_insights_registered():
    """
    Ensure all insight modules are imported so their decorators register them
    into the global registry. Safe to call multiple times.
    """
    import importlib
    import pkgutil
    import core.insights.modules as modules

    # Import every submodule in core/insights/modules
    for _, name, _ in pkgutil.iter_modules(modules.__path__):
        importlib.import_module(f"{modules.__name__}.{name}")

    return insight_registry


def get_insight(insight_id: str, version: str) -> BaseInsight:
    """
    Get insight instance by ID and version.
    
    Args:
        insight_id: Insight identifier
        version: Version string
        
    Returns:
        Insight instance
        
    Raises:
        KeyError: If insight not found
    """
    return insight_registry.get(insight_id, version)


def register_insight(insight_id: str, version: str):
    """
    Decorator to register insight classes.
    
    Args:
        insight_id: Unique insight identifier
        version: SemVer version string
        
    Returns:
        Decorator function
    """
    def decorator(cls: Type[BaseInsight]) -> Type[BaseInsight]:
        insight_registry.register(insight_id, version, cls)
        return cls
    return decorator


# Make sure ensure_insights_registered is included in __all__:
__all__ = ["register_insight", "get_insight", "insight_registry", "ensure_insights_registered"]