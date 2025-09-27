"""
Lifestyle overlays for scoring adjustments.

This module provides lifestyle-based adjustments to biomarker scores,
accounting for diet, sleep, exercise, and alcohol consumption patterns.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class LifestyleFactor(Enum):
    """Lifestyle factors that can affect biomarker scores."""
    DIET = "diet"
    SLEEP = "sleep"
    EXERCISE = "exercise"
    ALCOHOL = "alcohol"
    SMOKING = "smoking"
    STRESS = "stress"


class LifestyleLevel(Enum):
    """Levels of lifestyle factor impact."""
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    POOR = "poor"
    VERY_POOR = "very_poor"


@dataclass
class LifestyleAdjustment:
    """Adjustment factor for a lifestyle factor."""
    factor: LifestyleFactor
    level: LifestyleLevel
    adjustment_factor: float  # Multiplier for score adjustment
    description: str


@dataclass
class LifestyleProfile:
    """Complete lifestyle profile for a user."""
    diet_level: LifestyleLevel
    sleep_hours: float
    exercise_minutes_per_week: int
    alcohol_units_per_week: int
    smoking_status: str  # "never", "former", "current"
    stress_level: LifestyleLevel


class LifestyleOverlays:
    """Lifestyle-based adjustments for biomarker scores."""
    
    def __init__(self):
        """Initialize lifestyle overlays."""
        self._adjustments = self._load_lifestyle_adjustments()
    
    def _load_lifestyle_adjustments(self) -> Dict[LifestyleFactor, Dict[LifestyleLevel, LifestyleAdjustment]]:
        """Load lifestyle adjustment factors."""
        adjustments = {}
        
        # Diet adjustments
        adjustments[LifestyleFactor.DIET] = {
            LifestyleLevel.EXCELLENT: LifestyleAdjustment(
                factor=LifestyleFactor.DIET,
                level=LifestyleLevel.EXCELLENT,
                adjustment_factor=1.1,
                description="Excellent diet (Mediterranean, whole foods, minimal processed)"
            ),
            LifestyleLevel.GOOD: LifestyleAdjustment(
                factor=LifestyleFactor.DIET,
                level=LifestyleLevel.GOOD,
                adjustment_factor=1.05,
                description="Good diet (mostly whole foods, limited processed)"
            ),
            LifestyleLevel.AVERAGE: LifestyleAdjustment(
                factor=LifestyleFactor.DIET,
                level=LifestyleLevel.AVERAGE,
                adjustment_factor=1.0,
                description="Average diet (mixed whole and processed foods)"
            ),
            LifestyleLevel.POOR: LifestyleAdjustment(
                factor=LifestyleFactor.DIET,
                level=LifestyleLevel.POOR,
                adjustment_factor=0.9,
                description="Poor diet (mostly processed foods, high sugar/fat)"
            ),
            LifestyleLevel.VERY_POOR: LifestyleAdjustment(
                factor=LifestyleFactor.DIET,
                level=LifestyleLevel.VERY_POOR,
                adjustment_factor=0.8,
                description="Very poor diet (fast food, high sugar, minimal nutrients)"
            )
        }
        
        # Sleep adjustments
        adjustments[LifestyleFactor.SLEEP] = {
            LifestyleLevel.EXCELLENT: LifestyleAdjustment(
                factor=LifestyleFactor.SLEEP,
                level=LifestyleLevel.EXCELLENT,
                adjustment_factor=1.1,
                description="7-9 hours quality sleep consistently"
            ),
            LifestyleLevel.GOOD: LifestyleAdjustment(
                factor=LifestyleFactor.SLEEP,
                level=LifestyleLevel.GOOD,
                adjustment_factor=1.05,
                description="6-8 hours sleep, mostly consistent"
            ),
            LifestyleLevel.AVERAGE: LifestyleAdjustment(
                factor=LifestyleFactor.SLEEP,
                level=LifestyleLevel.AVERAGE,
                adjustment_factor=1.0,
                description="5-7 hours sleep, somewhat inconsistent"
            ),
            LifestyleLevel.POOR: LifestyleAdjustment(
                factor=LifestyleFactor.SLEEP,
                level=LifestyleLevel.POOR,
                adjustment_factor=0.9,
                description="4-6 hours sleep, often inconsistent"
            ),
            LifestyleLevel.VERY_POOR: LifestyleAdjustment(
                factor=LifestyleFactor.SLEEP,
                level=LifestyleLevel.VERY_POOR,
                adjustment_factor=0.8,
                description="<4 hours sleep, very inconsistent"
            )
        }
        
        # Exercise adjustments
        adjustments[LifestyleFactor.EXERCISE] = {
            LifestyleLevel.EXCELLENT: LifestyleAdjustment(
                factor=LifestyleFactor.EXERCISE,
                level=LifestyleLevel.EXCELLENT,
                adjustment_factor=1.1,
                description="300+ minutes moderate exercise per week"
            ),
            LifestyleLevel.GOOD: LifestyleAdjustment(
                factor=LifestyleFactor.EXERCISE,
                level=LifestyleLevel.GOOD,
                adjustment_factor=1.05,
                description="150-300 minutes moderate exercise per week"
            ),
            LifestyleLevel.AVERAGE: LifestyleAdjustment(
                factor=LifestyleFactor.EXERCISE,
                level=LifestyleLevel.AVERAGE,
                adjustment_factor=1.0,
                description="75-150 minutes moderate exercise per week"
            ),
            LifestyleLevel.POOR: LifestyleAdjustment(
                factor=LifestyleFactor.EXERCISE,
                level=LifestyleLevel.POOR,
                adjustment_factor=0.9,
                description="<75 minutes moderate exercise per week"
            ),
            LifestyleLevel.VERY_POOR: LifestyleAdjustment(
                factor=LifestyleFactor.EXERCISE,
                level=LifestyleLevel.VERY_POOR,
                adjustment_factor=0.8,
                description="Minimal to no exercise"
            )
        }
        
        # Alcohol adjustments
        adjustments[LifestyleFactor.ALCOHOL] = {
            LifestyleLevel.EXCELLENT: LifestyleAdjustment(
                factor=LifestyleFactor.ALCOHOL,
                level=LifestyleLevel.EXCELLENT,
                adjustment_factor=1.05,
                description="No alcohol consumption"
            ),
            LifestyleLevel.GOOD: LifestyleAdjustment(
                factor=LifestyleFactor.ALCOHOL,
                level=LifestyleLevel.GOOD,
                adjustment_factor=1.0,
                description="1-7 units per week (moderate)"
            ),
            LifestyleLevel.AVERAGE: LifestyleAdjustment(
                factor=LifestyleFactor.ALCOHOL,
                level=LifestyleLevel.AVERAGE,
                adjustment_factor=0.95,
                description="8-14 units per week"
            ),
            LifestyleLevel.POOR: LifestyleAdjustment(
                factor=LifestyleFactor.ALCOHOL,
                level=LifestyleLevel.POOR,
                adjustment_factor=0.9,
                description="15-21 units per week (heavy)"
            ),
            LifestyleLevel.VERY_POOR: LifestyleAdjustment(
                factor=LifestyleFactor.ALCOHOL,
                level=LifestyleLevel.VERY_POOR,
                adjustment_factor=0.8,
                description="22+ units per week (excessive)"
            )
        }
        
        # Smoking adjustments
        adjustments[LifestyleFactor.SMOKING] = {
            LifestyleLevel.EXCELLENT: LifestyleAdjustment(
                factor=LifestyleFactor.SMOKING,
                level=LifestyleLevel.EXCELLENT,
                adjustment_factor=1.0,
                description="Never smoked"
            ),
            LifestyleLevel.GOOD: LifestyleAdjustment(
                factor=LifestyleFactor.SMOKING,
                level=LifestyleLevel.GOOD,
                adjustment_factor=0.95,
                description="Former smoker (>5 years ago)"
            ),
            LifestyleLevel.AVERAGE: LifestyleAdjustment(
                factor=LifestyleFactor.SMOKING,
                level=LifestyleLevel.AVERAGE,
                adjustment_factor=0.9,
                description="Former smoker (1-5 years ago)"
            ),
            LifestyleLevel.POOR: LifestyleAdjustment(
                factor=LifestyleFactor.SMOKING,
                level=LifestyleLevel.POOR,
                adjustment_factor=0.8,
                description="Former smoker (<1 year ago)"
            ),
            LifestyleLevel.VERY_POOR: LifestyleAdjustment(
                factor=LifestyleFactor.SMOKING,
                level=LifestyleLevel.VERY_POOR,
                adjustment_factor=0.7,
                description="Current smoker"
            )
        }
        
        # Stress adjustments
        adjustments[LifestyleFactor.STRESS] = {
            LifestyleLevel.EXCELLENT: LifestyleAdjustment(
                factor=LifestyleFactor.STRESS,
                level=LifestyleLevel.EXCELLENT,
                adjustment_factor=1.05,
                description="Low stress, good coping mechanisms"
            ),
            LifestyleLevel.GOOD: LifestyleAdjustment(
                factor=LifestyleFactor.STRESS,
                level=LifestyleLevel.GOOD,
                adjustment_factor=1.0,
                description="Moderate stress, adequate coping"
            ),
            LifestyleLevel.AVERAGE: LifestyleAdjustment(
                factor=LifestyleFactor.STRESS,
                level=LifestyleLevel.AVERAGE,
                adjustment_factor=0.95,
                description="Moderate-high stress, some coping"
            ),
            LifestyleLevel.POOR: LifestyleAdjustment(
                factor=LifestyleFactor.STRESS,
                level=LifestyleLevel.POOR,
                adjustment_factor=0.9,
                description="High stress, poor coping"
            ),
            LifestyleLevel.VERY_POOR: LifestyleAdjustment(
                factor=LifestyleFactor.STRESS,
                level=LifestyleLevel.VERY_POOR,
                adjustment_factor=0.8,
                description="Very high stress, minimal coping"
            )
        }
        
        return adjustments
    
    def create_lifestyle_profile(
        self,
        diet_level: str = "average",
        sleep_hours: float = 7.0,
        exercise_minutes_per_week: int = 150,
        alcohol_units_per_week: int = 5,
        smoking_status: str = "never",
        stress_level: str = "average"
    ) -> LifestyleProfile:
        """
        Create a lifestyle profile from user inputs.
        
        Args:
            diet_level: Diet quality level
            sleep_hours: Average hours of sleep per night
            exercise_minutes_per_week: Minutes of moderate exercise per week
            alcohol_units_per_week: Alcohol units consumed per week
            smoking_status: Smoking status
            stress_level: Stress level
            
        Returns:
            LifestyleProfile object
        """
        # Map stress level to correct enum value
        stress_mapping = {
            "low": LifestyleLevel.EXCELLENT,
            "good": LifestyleLevel.GOOD,
            "average": LifestyleLevel.AVERAGE,
            "poor": LifestyleLevel.POOR,
            "very_poor": LifestyleLevel.VERY_POOR
        }
        
        return LifestyleProfile(
            diet_level=LifestyleLevel(diet_level.lower()),
            sleep_hours=sleep_hours,
            exercise_minutes_per_week=exercise_minutes_per_week,
            alcohol_units_per_week=alcohol_units_per_week,
            smoking_status=smoking_status.lower(),
            stress_level=stress_mapping.get(stress_level.lower(), LifestyleLevel.AVERAGE)
        )
    
    def apply_lifestyle_overlays(
        self, 
        base_score: float, 
        lifestyle_profile: LifestyleProfile
    ) -> Tuple[float, List[str]]:
        """
        Apply lifestyle overlays to a base score.
        
        Args:
            base_score: Base biomarker score (0-100)
            lifestyle_profile: User's lifestyle profile
            
        Returns:
            Tuple of (adjusted_score, adjustment_descriptions)
        """
        adjusted_score = base_score
        adjustments = []
        
        # Apply diet adjustment
        diet_adj = self._adjustments[LifestyleFactor.DIET][lifestyle_profile.diet_level]
        adjusted_score *= diet_adj.adjustment_factor
        adjustments.append(f"Diet: {diet_adj.description}")
        
        # Apply sleep adjustment
        sleep_level = self._determine_sleep_level(lifestyle_profile.sleep_hours)
        sleep_adj = self._adjustments[LifestyleFactor.SLEEP][sleep_level]
        adjusted_score *= sleep_adj.adjustment_factor
        adjustments.append(f"Sleep: {sleep_adj.description}")
        
        # Apply exercise adjustment
        exercise_level = self._determine_exercise_level(lifestyle_profile.exercise_minutes_per_week)
        exercise_adj = self._adjustments[LifestyleFactor.EXERCISE][exercise_level]
        adjusted_score *= exercise_adj.adjustment_factor
        adjustments.append(f"Exercise: {exercise_adj.description}")
        
        # Apply alcohol adjustment
        alcohol_level = self._determine_alcohol_level(lifestyle_profile.alcohol_units_per_week)
        alcohol_adj = self._adjustments[LifestyleFactor.ALCOHOL][alcohol_level]
        adjusted_score *= alcohol_adj.adjustment_factor
        adjustments.append(f"Alcohol: {alcohol_adj.description}")
        
        # Apply smoking adjustment
        smoking_level = self._determine_smoking_level(lifestyle_profile.smoking_status)
        smoking_adj = self._adjustments[LifestyleFactor.SMOKING][smoking_level]
        adjusted_score *= smoking_adj.adjustment_factor
        adjustments.append(f"Smoking: {smoking_adj.description}")
        
        # Apply stress adjustment
        stress_adj = self._adjustments[LifestyleFactor.STRESS][lifestyle_profile.stress_level]
        adjusted_score *= stress_adj.adjustment_factor
        adjustments.append(f"Stress: {stress_adj.description}")
        
        # Ensure score stays within 0-100 range
        adjusted_score = max(0.0, min(100.0, adjusted_score))
        
        return adjusted_score, adjustments
    
    def _determine_sleep_level(self, sleep_hours: float) -> LifestyleLevel:
        """Determine sleep level based on hours."""
        if sleep_hours >= 7.0:
            return LifestyleLevel.EXCELLENT
        elif sleep_hours >= 6.0:
            return LifestyleLevel.GOOD
        elif sleep_hours >= 5.0:
            return LifestyleLevel.AVERAGE
        elif sleep_hours >= 4.0:
            return LifestyleLevel.POOR
        else:
            return LifestyleLevel.VERY_POOR
    
    def _determine_exercise_level(self, minutes_per_week: int) -> LifestyleLevel:
        """Determine exercise level based on minutes per week."""
        if minutes_per_week >= 300:
            return LifestyleLevel.EXCELLENT
        elif minutes_per_week >= 150:
            return LifestyleLevel.GOOD
        elif minutes_per_week >= 75:
            return LifestyleLevel.AVERAGE
        elif minutes_per_week > 0:
            return LifestyleLevel.POOR
        else:
            return LifestyleLevel.VERY_POOR
    
    def _determine_alcohol_level(self, units_per_week: int) -> LifestyleLevel:
        """Determine alcohol level based on units per week."""
        if units_per_week == 0:
            return LifestyleLevel.EXCELLENT
        elif units_per_week <= 7:
            return LifestyleLevel.GOOD
        elif units_per_week <= 14:
            return LifestyleLevel.AVERAGE
        elif units_per_week <= 21:
            return LifestyleLevel.POOR
        else:
            return LifestyleLevel.VERY_POOR
    
    def _determine_smoking_level(self, smoking_status: str) -> LifestyleLevel:
        """Determine smoking level based on status."""
        if smoking_status == "never":
            return LifestyleLevel.EXCELLENT
        elif smoking_status == "former":
            return LifestyleLevel.GOOD  # All former smokers get good rating
        else:  # current
            return LifestyleLevel.VERY_POOR
    
    def get_lifestyle_recommendations(self, lifestyle_profile: LifestyleProfile) -> List[str]:
        """
        Get lifestyle recommendations based on profile.
        
        Args:
            lifestyle_profile: User's lifestyle profile
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        # Diet recommendations
        if lifestyle_profile.diet_level in [LifestyleLevel.POOR, LifestyleLevel.VERY_POOR]:
            recommendations.append("Improve diet quality by reducing processed foods and increasing whole foods")
        
        # Sleep recommendations
        if lifestyle_profile.sleep_hours < 6.0:
            recommendations.append("Aim for 7-9 hours of quality sleep per night")
        
        # Exercise recommendations
        if lifestyle_profile.exercise_minutes_per_week < 150:
            recommendations.append("Increase physical activity to at least 150 minutes of moderate exercise per week")
        
        # Alcohol recommendations
        if lifestyle_profile.alcohol_units_per_week > 14:
            recommendations.append("Reduce alcohol consumption to moderate levels (1-7 units per week)")
        
        # Smoking recommendations
        if lifestyle_profile.smoking_status == "current":
            recommendations.append("Consider smoking cessation programs for significant health benefits")
        
        # Stress recommendations
        if lifestyle_profile.stress_level in [LifestyleLevel.POOR, LifestyleLevel.VERY_POOR]:
            recommendations.append("Develop stress management techniques like meditation, yoga, or counseling")
        
        return recommendations
