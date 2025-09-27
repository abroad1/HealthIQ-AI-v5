"""
Modular weighting system for scoring engines in clustering analysis.

This module provides a flexible weighting system that allows clinical priorities
to be adjusted while maintaining equal weights as the default configuration.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class EngineType(Enum):
    """Types of scoring engines."""
    METABOLIC = "metabolic"
    CARDIOVASCULAR = "cardiovascular"
    INFLAMMATORY = "inflammatory"
    HORMONAL = "hormonal"
    NUTRITIONAL = "nutritional"
    KIDNEY = "kidney"
    LIVER = "liver"
    CBC = "cbc"


@dataclass
class EngineWeight:
    """Weight configuration for a scoring engine."""
    engine_type: EngineType
    weight: float
    priority: int  # Lower number = higher priority
    description: str
    clinical_rationale: str


class EngineWeightingSystem:
    """Modular weighting system for scoring engines."""
    
    def __init__(self):
        """Initialize with default equal weights."""
        self.weights: Dict[EngineType, EngineWeight] = {}
        self._initialize_default_weights()
    
    def _initialize_default_weights(self) -> None:
        """Initialize with equal weights for all engines."""
        default_weight = 1.0 / len(EngineType)
        
        weight_configs = [
            (EngineType.METABOLIC, "Metabolic health and glucose regulation"),
            (EngineType.CARDIOVASCULAR, "Heart and blood vessel health"),
            (EngineType.INFLAMMATORY, "Systemic inflammation markers"),
            (EngineType.HORMONAL, "Endocrine system function"),
            (EngineType.NUTRITIONAL, "Nutrient levels and deficiencies"),
            (EngineType.KIDNEY, "Kidney function and filtration"),
            (EngineType.LIVER, "Liver function and detoxification"),
            (EngineType.CBC, "Blood cell counts and hematology")
        ]
        
        for i, (engine_type, rationale) in enumerate(weight_configs):
            self.weights[engine_type] = EngineWeight(
                engine_type=engine_type,
                weight=default_weight,
                priority=i + 1,
                description=f"{engine_type.value.title()} health scoring",
                clinical_rationale=rationale
            )
    
    def get_engine_weight(self, engine_type: EngineType) -> float:
        """
        Get weight for a specific engine.
        
        Args:
            engine_type: Type of scoring engine
            
        Returns:
            Weight value for the engine
        """
        return self.weights.get(engine_type, EngineWeight(
            engine_type=engine_type,
            weight=0.0,
            priority=999,
            description="Unknown engine",
            clinical_rationale="No rationale available"
        )).weight
    
    def set_engine_weight(self, engine_type: EngineType, weight: float, 
                         priority: Optional[int] = None,
                         clinical_rationale: Optional[str] = None) -> None:
        """
        Set weight for a specific engine.
        
        Args:
            engine_type: Type of scoring engine
            weight: New weight value (should sum to 1.0 across all engines)
            priority: Optional priority level (lower = higher priority)
            clinical_rationale: Optional clinical justification
        """
        if engine_type not in self.weights:
            self.weights[engine_type] = EngineWeight(
                engine_type=engine_type,
                weight=weight,
                priority=priority or 999,
                description=f"{engine_type.value.title()} health scoring",
                clinical_rationale=clinical_rationale or "Custom weight configuration"
            )
        else:
            current = self.weights[engine_type]
            self.weights[engine_type] = EngineWeight(
                engine_type=engine_type,
                weight=weight,
                priority=priority or current.priority,
                description=current.description,
                clinical_rationale=clinical_rationale or current.clinical_rationale
            )
    
    def normalize_weights(self) -> None:
        """Normalize weights to sum to 1.0."""
        total_weight = sum(weight.weight for weight in self.weights.values())
        if total_weight > 0:
            for weight in self.weights.values():
                weight.weight = weight.weight / total_weight
    
    def apply_clinical_priority(self, priority_engines: List[EngineType], 
                              boost_factor: float = 1.5) -> None:
        """
        Apply clinical priority boost to specified engines.
        
        Args:
            priority_engines: List of engines to boost
            boost_factor: Factor to multiply priority engine weights
        """
        # First, reduce non-priority engines
        non_priority_engines = [e for e in EngineType if e not in priority_engines]
        reduction_factor = 0.8
        
        for engine_type in non_priority_engines:
            if engine_type in self.weights:
                self.weights[engine_type].weight *= reduction_factor
        
        # Then boost priority engines
        for engine_type in priority_engines:
            if engine_type in self.weights:
                self.weights[engine_type].weight *= boost_factor
        
        # Normalize to ensure weights sum to 1.0
        self.normalize_weights()
    
    def get_weighted_scores(self, engine_scores: Dict[str, float]) -> Dict[str, float]:
        """
        Apply weights to engine scores.
        
        Args:
            engine_scores: Dictionary of engine names to scores
            
        Returns:
            Dictionary of weighted scores
        """
        weighted_scores = {}
        
        for engine_name, score in engine_scores.items():
            # Convert engine name to EngineType
            try:
                engine_type = EngineType(engine_name)
                weight = self.get_engine_weight(engine_type)
                weighted_scores[engine_name] = score * weight
            except ValueError:
                # Unknown engine type, use default weight
                weighted_scores[engine_name] = score * (1.0 / len(EngineType))
        
        return weighted_scores
    
    def get_weight_summary(self) -> Dict[str, Any]:
        """
        Get summary of current weight configuration.
        
        Returns:
            Dictionary with weight summary information
        """
        total_weight = sum(weight.weight for weight in self.weights.values())
        
        return {
            "total_weight": total_weight,
            "normalized": abs(total_weight - 1.0) < 0.001,
            "engine_weights": [
                {
                    "engine": weight.engine_type.value,
                    "weight": weight.weight,
                    "priority": weight.priority,
                    "description": weight.description,
                    "clinical_rationale": weight.clinical_rationale
                }
                for weight in sorted(self.weights.values(), key=lambda w: w.priority)
            ],
            "weight_distribution": {
                weight.engine_type.value: weight.weight 
                for weight in self.weights.values()
            }
        }
    
    def reset_to_default(self) -> None:
        """Reset weights to default equal configuration."""
        self._initialize_default_weights()
    
    def validate_weights(self) -> List[str]:
        """
        Validate weight configuration.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check if weights sum to 1.0
        total_weight = sum(weight.weight for weight in self.weights.values())
        if abs(total_weight - 1.0) > 0.001:
            errors.append(f"Weights sum to {total_weight:.3f}, should be 1.0")
        
        # Check for negative weights
        negative_weights = [
            weight.engine_type.value 
            for weight in self.weights.values() 
            if weight.weight < 0
        ]
        if negative_weights:
            errors.append(f"Negative weights found for: {', '.join(negative_weights)}")
        
        # Check for missing engines
        missing_engines = [
            engine.value 
            for engine in EngineType 
            if engine not in self.weights
        ]
        if missing_engines:
            errors.append(f"Missing weight configuration for: {', '.join(missing_engines)}")
        
        return errors


# Predefined weight configurations for common clinical scenarios
class ClinicalWeightProfiles:
    """Predefined weight profiles for different clinical scenarios."""
    
    @staticmethod
    def metabolic_focus() -> EngineWeightingSystem:
        """Weight profile focusing on metabolic health."""
        system = EngineWeightingSystem()
        system.apply_clinical_priority([EngineType.METABOLIC, EngineType.INFLAMMATORY])
        return system
    
    @staticmethod
    def cardiovascular_focus() -> EngineWeightingSystem:
        """Weight profile focusing on cardiovascular health."""
        system = EngineWeightingSystem()
        system.apply_clinical_priority([EngineType.CARDIOVASCULAR, EngineType.INFLAMMATORY])
        return system
    
    @staticmethod
    def comprehensive_health() -> EngineWeightingSystem:
        """Weight profile for comprehensive health assessment."""
        system = EngineWeightingSystem()
        # Slight boost to metabolic and cardiovascular as primary health indicators
        priority_engines = [EngineType.METABOLIC, EngineType.CARDIOVASCULAR]
        system.apply_clinical_priority(priority_engines, boost_factor=1.2)
        return system
    
    @staticmethod
    def organ_function_focus() -> EngineWeightingSystem:
        """Weight profile focusing on organ function."""
        system = EngineWeightingSystem()
        system.apply_clinical_priority([
            EngineType.KIDNEY, 
            EngineType.LIVER, 
            EngineType.CBC
        ])
        return system
    
    @staticmethod
    def wellness_optimization() -> EngineWeightingSystem:
        """Weight profile for wellness optimization."""
        system = EngineWeightingSystem()
        system.apply_clinical_priority([
            EngineType.NUTRITIONAL, 
            EngineType.HORMONAL, 
            EngineType.INFLAMMATORY
        ])
        return system
