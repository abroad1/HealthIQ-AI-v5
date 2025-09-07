"""
Insight registry - manages available insight generators.
"""

from typing import List, Dict, Type

from core.insights.base import BaseInsight


class InsightRegistry:
    """Registry for managing insight generators."""
    
    def __init__(self):
        """Initialize the insight registry."""
        self._insights: Dict[str, Type[BaseInsight]] = {}
        self._instances: Dict[str, BaseInsight] = {}
    
    def register(self, insight_class: Type[BaseInsight]) -> None:
        """
        Register an insight generator class.
        
        Args:
            insight_class: Insight generator class to register
        """
        name = insight_class.__name__
        self._insights[name] = insight_class
    
    def get_insight(self, name: str) -> BaseInsight:
        """
        Get an insight generator instance by name.
        
        Args:
            name: Name of the insight generator
            
        Returns:
            Insight generator instance
            
        Raises:
            KeyError: If insight generator not found
        """
        if name not in self._instances:
            if name not in self._insights:
                raise KeyError(f"Insight generator '{name}' not registered")
            
            # Create instance
            self._instances[name] = self._insights[name]()
        
        return self._instances[name]
    
    def get_all_insights(self) -> List[BaseInsight]:
        """
        Get all registered insight generator instances.
        
        Returns:
            List of all insight generator instances
        """
        return [self.get_insight(name) for name in self._insights.keys()]
    
    def get_insight_names(self) -> List[str]:
        """
        Get names of all registered insight generators.
        
        Returns:
            List of insight generator names
        """
        return list(self._insights.keys())
    
    def clear(self) -> None:
        """Clear all registered insights."""
        self._insights.clear()
        self._instances.clear()


# Global insight registry instance
insight_registry = InsightRegistry()
