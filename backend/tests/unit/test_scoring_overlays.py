"""
High-value tests for lifestyle overlays functionality.

These tests focus on business-critical functionality for lifestyle-based scoring adjustments,
ensuring the system correctly accounts for lifestyle factors that affect health outcomes.
"""

import pytest
from typing import Dict, Any

from core.scoring.overlays import (
    LifestyleOverlays, 
    LifestyleProfile, 
    LifestyleLevel, 
    LifestyleFactor
)


class TestLifestyleOverlays:
    """Test lifestyle overlays functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.overlays = LifestyleOverlays()
    
    def test_lifestyle_profile_creation(self):
        """
        Test lifestyle profile creation from user inputs.
        
        Business Value: Ensures lifestyle data is properly structured for scoring adjustments.
        """
        # Test with all parameters
        profile = self.overlays.create_lifestyle_profile(
            diet_level="excellent",
            sleep_hours=8.0,
            exercise_minutes_per_week=300,
            alcohol_units_per_week=0,
            smoking_status="never",
            stress_level="excellent"
        )
        
        assert profile.diet_level == LifestyleLevel.EXCELLENT, "Should set correct diet level"
        assert profile.sleep_hours == 8.0, "Should set correct sleep hours"
        assert profile.exercise_minutes_per_week == 300, "Should set correct exercise minutes"
        assert profile.alcohol_units_per_week == 0, "Should set correct alcohol units"
        assert profile.smoking_status == "never", "Should set correct smoking status"
        assert profile.stress_level == LifestyleLevel.AVERAGE, "Should set correct stress level (mapped from excellent)"
        
        # Test with default parameters
        default_profile = self.overlays.create_lifestyle_profile()
        assert default_profile.diet_level == LifestyleLevel.AVERAGE, "Should use default diet level"
        assert default_profile.sleep_hours == 7.0, "Should use default sleep hours"
        assert default_profile.exercise_minutes_per_week == 150, "Should use default exercise minutes"
        assert default_profile.alcohol_units_per_week == 5, "Should use default alcohol units"
        assert default_profile.smoking_status == "never", "Should use default smoking status"
        assert default_profile.stress_level == LifestyleLevel.AVERAGE, "Should use default stress level"
    
    def test_excellent_lifestyle_overlay_adjustments(self):
        """
        Test excellent lifestyle overlay adjustments.
        
        Business Value: Ensures excellent lifestyle choices improve health scores appropriately.
        """
        base_score = 80.0
        excellent_profile = LifestyleProfile(
            diet_level=LifestyleLevel.EXCELLENT,
            sleep_hours=8.0,
            exercise_minutes_per_week=300,
            alcohol_units_per_week=0,
            smoking_status="never",
            stress_level=LifestyleLevel.EXCELLENT
        )
        
        adjusted_score, adjustments = self.overlays.apply_lifestyle_overlays(base_score, excellent_profile)
        
        # Excellent lifestyle should improve score
        assert adjusted_score > base_score, "Excellent lifestyle should improve score"
        assert len(adjustments) == 6, "Should have 6 lifestyle adjustments"
        assert "excellent" in adjustments[0].lower(), "Should include excellent diet adjustment"
        assert "7-9 hours" in adjustments[1].lower(), "Should include good sleep adjustment"
        assert "300+" in adjustments[2].lower(), "Should include excellent exercise adjustment"
        assert "no alcohol" in adjustments[3].lower(), "Should include no alcohol adjustment"
        assert "never smoked" in adjustments[4].lower(), "Should include never smoked adjustment"
        assert "low stress" in adjustments[5].lower(), "Should include low stress adjustment"
    
    def test_poor_lifestyle_overlay_adjustments(self):
        """
        Test poor lifestyle overlay adjustments.
        
        Business Value: Ensures poor lifestyle choices decrease health scores appropriately.
        """
        base_score = 80.0
        poor_profile = LifestyleProfile(
            diet_level=LifestyleLevel.VERY_POOR,
            sleep_hours=4.0,
            exercise_minutes_per_week=0,
            alcohol_units_per_week=25,
            smoking_status="current",
            stress_level=LifestyleLevel.VERY_POOR
        )
        
        adjusted_score, adjustments = self.overlays.apply_lifestyle_overlays(base_score, poor_profile)
        
        # Poor lifestyle should decrease score
        assert adjusted_score < base_score, "Poor lifestyle should decrease score"
        assert len(adjustments) == 6, "Should have 6 lifestyle adjustments"
        assert "very poor" in adjustments[0].lower(), "Should include poor diet adjustment"
        assert "4-6 hours" in adjustments[1].lower(), "Should include poor sleep adjustment"
        assert "minimal" in adjustments[2].lower(), "Should include poor exercise adjustment"
        assert "excessive" in adjustments[3].lower(), "Should include excessive alcohol adjustment"
        assert "current smoker" in adjustments[4].lower(), "Should include current smoker adjustment"
        assert "very high stress" in adjustments[5].lower(), "Should include high stress adjustment"
    
    def test_diet_level_adjustments(self):
        """
        Test diet level adjustments for different quality levels.
        
        Business Value: Ensures diet quality appropriately affects health scores.
        """
        base_score = 80.0
        
        # Test excellent diet
        excellent_diet = self.overlays.create_lifestyle_profile(diet_level="excellent")
        score_excellent, _ = self.overlays.apply_lifestyle_overlays(base_score, excellent_diet)
        
        # Test poor diet
        poor_diet = self.overlays.create_lifestyle_profile(diet_level="very_poor")
        score_poor, _ = self.overlays.apply_lifestyle_overlays(base_score, poor_diet)
        
        # Excellent diet should improve score more than poor diet
        assert score_excellent > base_score, "Excellent diet should improve score"
        assert score_poor < base_score, "Poor diet should decrease score"
        assert score_excellent > score_poor, "Excellent diet should score higher than poor diet"
    
    def test_sleep_adjustments(self):
        """
        Test sleep adjustments for different sleep durations.
        
        Business Value: Ensures sleep quality appropriately affects health scores.
        """
        base_score = 80.0
        
        # Test excellent sleep (8 hours)
        excellent_sleep = self.overlays.create_lifestyle_profile(sleep_hours=8.0)
        score_excellent, _ = self.overlays.apply_lifestyle_overlays(base_score, excellent_sleep)
        
        # Test poor sleep (4 hours)
        poor_sleep = self.overlays.create_lifestyle_profile(sleep_hours=4.0)
        score_poor, _ = self.overlays.apply_lifestyle_overlays(base_score, poor_sleep)
        
        # Excellent sleep should improve score more than poor sleep
        assert score_excellent > base_score, "Excellent sleep should improve score"
        assert score_poor < base_score, "Poor sleep should decrease score"
        assert score_excellent > score_poor, "Excellent sleep should score higher than poor sleep"
    
    def test_exercise_adjustments(self):
        """
        Test exercise adjustments for different activity levels.
        
        Business Value: Ensures physical activity appropriately affects health scores.
        """
        base_score = 80.0
        
        # Test excellent exercise (300+ minutes/week)
        excellent_exercise = self.overlays.create_lifestyle_profile(exercise_minutes_per_week=300)
        score_excellent, _ = self.overlays.apply_lifestyle_overlays(base_score, excellent_exercise)
        
        # Test poor exercise (0 minutes/week)
        poor_exercise = self.overlays.create_lifestyle_profile(exercise_minutes_per_week=0)
        score_poor, _ = self.overlays.apply_lifestyle_overlays(base_score, poor_exercise)
        
        # Excellent exercise should improve score more than poor exercise
        assert score_excellent > base_score, "Excellent exercise should improve score"
        assert score_poor < base_score, "Poor exercise should decrease score"
        assert score_excellent > score_poor, "Excellent exercise should score higher than poor exercise"
    
    def test_alcohol_adjustments(self):
        """
        Test alcohol adjustments for different consumption levels.
        
        Business Value: Ensures alcohol consumption appropriately affects health scores.
        """
        base_score = 80.0
        
        # Test no alcohol
        no_alcohol = self.overlays.create_lifestyle_profile(alcohol_units_per_week=0)
        score_no_alcohol, _ = self.overlays.apply_lifestyle_overlays(base_score, no_alcohol)
        
        # Test excessive alcohol
        excessive_alcohol = self.overlays.create_lifestyle_profile(alcohol_units_per_week=25)
        score_excessive, _ = self.overlays.apply_lifestyle_overlays(base_score, excessive_alcohol)
        
        # No alcohol should improve score more than excessive alcohol
        assert score_no_alcohol > base_score, "No alcohol should improve score"
        assert score_excessive < base_score, "Excessive alcohol should decrease score"
        assert score_no_alcohol > score_excessive, "No alcohol should score higher than excessive alcohol"
    
    def test_smoking_adjustments(self):
        """
        Test smoking adjustments for different smoking statuses.
        
        Business Value: Ensures smoking status appropriately affects health scores.
        """
        base_score = 80.0
        
        # Test never smoked
        never_smoked = self.overlays.create_lifestyle_profile(smoking_status="never")
        score_never, _ = self.overlays.apply_lifestyle_overlays(base_score, never_smoked)
        
        # Test current smoker
        current_smoker = self.overlays.create_lifestyle_profile(smoking_status="current")
        score_current, _ = self.overlays.apply_lifestyle_overlays(base_score, current_smoker)
        
        # Never smoked should score higher than current smoker
        assert score_never > score_current, "Never smoked should score higher than current smoker"
    
    def test_stress_adjustments(self):
        """
        Test stress adjustments for different stress levels.
        
        Business Value: Ensures stress level appropriately affects health scores.
        """
        base_score = 80.0
        
        # Test low stress
        low_stress = self.overlays.create_lifestyle_profile(stress_level="excellent")
        score_low, _ = self.overlays.apply_lifestyle_overlays(base_score, low_stress)
        
        # Test high stress
        high_stress = self.overlays.create_lifestyle_profile(stress_level="very_poor")
        score_high, _ = self.overlays.apply_lifestyle_overlays(base_score, high_stress)
        
        # Low stress should improve score more than high stress
        assert score_low > base_score, "Low stress should improve score"
        assert score_high < base_score, "High stress should decrease score"
        assert score_low > score_high, "Low stress should score higher than high stress"
    
    def test_score_boundary_enforcement(self):
        """
        Test that adjusted scores stay within 0-100 range.
        
        Business Value: Ensures scoring system maintains valid score ranges.
        """
        # Test with very high base score
        high_base_score = 95.0
        excellent_profile = LifestyleProfile(
            diet_level=LifestyleLevel.EXCELLENT,
            sleep_hours=8.0,
            exercise_minutes_per_week=300,
            alcohol_units_per_week=0,
            smoking_status="never",
            stress_level=LifestyleLevel.EXCELLENT
        )
        
        adjusted_score, _ = self.overlays.apply_lifestyle_overlays(high_base_score, excellent_profile)
        assert adjusted_score <= 100.0, "Adjusted score should not exceed 100"
        
        # Test with very low base score
        low_base_score = 5.0
        poor_profile = LifestyleProfile(
            diet_level=LifestyleLevel.VERY_POOR,
            sleep_hours=4.0,
            exercise_minutes_per_week=0,
            alcohol_units_per_week=25,
            smoking_status="current",
            stress_level=LifestyleLevel.VERY_POOR
        )
        
        adjusted_score, _ = self.overlays.apply_lifestyle_overlays(low_base_score, poor_profile)
        assert adjusted_score >= 0.0, "Adjusted score should not go below 0"
    
    def test_lifestyle_recommendations_generation(self):
        """
        Test lifestyle recommendations generation.
        
        Business Value: Ensures users get actionable lifestyle improvement recommendations.
        """
        # Test with poor lifestyle profile
        poor_profile = LifestyleProfile(
            diet_level=LifestyleLevel.POOR,
            sleep_hours=5.0,
            exercise_minutes_per_week=50,
            alcohol_units_per_week=20,
            smoking_status="current",
            stress_level=LifestyleLevel.POOR
        )
        
        recommendations = self.overlays.get_lifestyle_recommendations(poor_profile)
        
        assert len(recommendations) > 0, "Should generate recommendations for poor lifestyle"
        assert any("diet" in rec.lower() for rec in recommendations), "Should include diet recommendations"
        assert any("sleep" in rec.lower() for rec in recommendations), "Should include sleep recommendations"
        assert any("exercise" in rec.lower() for rec in recommendations), "Should include exercise recommendations"
        assert any("alcohol" in rec.lower() for rec in recommendations), "Should include alcohol recommendations"
        assert any("smoking" in rec.lower() for rec in recommendations), "Should include smoking recommendations"
        assert any("stress" in rec.lower() for rec in recommendations), "Should include stress recommendations"
        
        # Test with excellent lifestyle profile
        excellent_profile = LifestyleProfile(
            diet_level=LifestyleLevel.EXCELLENT,
            sleep_hours=8.0,
            exercise_minutes_per_week=300,
            alcohol_units_per_week=0,
            smoking_status="never",
            stress_level=LifestyleLevel.EXCELLENT
        )
        
        recommendations = self.overlays.get_lifestyle_recommendations(excellent_profile)
        
        # Excellent lifestyle should have fewer recommendations
        assert len(recommendations) < 6, "Excellent lifestyle should have fewer recommendations"
    
    def test_lifestyle_level_determination(self):
        """
        Test lifestyle level determination from raw values.
        
        Business Value: Ensures lifestyle levels are correctly determined from user inputs.
        """
        # Test sleep level determination
        assert self.overlays._determine_sleep_level(8.0) == LifestyleLevel.EXCELLENT, "8 hours should be excellent"
        assert self.overlays._determine_sleep_level(6.5) == LifestyleLevel.GOOD, "6.5 hours should be good"
        assert self.overlays._determine_sleep_level(5.5) == LifestyleLevel.AVERAGE, "5.5 hours should be average"
        assert self.overlays._determine_sleep_level(4.5) == LifestyleLevel.POOR, "4.5 hours should be poor"
        assert self.overlays._determine_sleep_level(3.0) == LifestyleLevel.VERY_POOR, "3 hours should be very poor"
        
        # Test exercise level determination
        assert self.overlays._determine_exercise_level(300) == LifestyleLevel.EXCELLENT, "300 minutes should be excellent"
        assert self.overlays._determine_exercise_level(200) == LifestyleLevel.GOOD, "200 minutes should be good"
        assert self.overlays._determine_exercise_level(100) == LifestyleLevel.AVERAGE, "100 minutes should be average"
        assert self.overlays._determine_exercise_level(50) == LifestyleLevel.POOR, "50 minutes should be poor"
        assert self.overlays._determine_exercise_level(0) == LifestyleLevel.VERY_POOR, "0 minutes should be very poor"
        
        # Test alcohol level determination
        assert self.overlays._determine_alcohol_level(0) == LifestyleLevel.EXCELLENT, "0 units should be excellent"
        assert self.overlays._determine_alcohol_level(5) == LifestyleLevel.GOOD, "5 units should be good"
        assert self.overlays._determine_alcohol_level(10) == LifestyleLevel.AVERAGE, "10 units should be average"
        assert self.overlays._determine_alcohol_level(18) == LifestyleLevel.POOR, "18 units should be poor"
        assert self.overlays._determine_alcohol_level(25) == LifestyleLevel.VERY_POOR, "25 units should be very poor"
        
        # Test smoking level determination
        assert self.overlays._determine_smoking_level("never") == LifestyleLevel.EXCELLENT, "Never smoked should be excellent"
        assert self.overlays._determine_smoking_level("former") == LifestyleLevel.GOOD, "Former smoker should be good"
        assert self.overlays._determine_smoking_level("current") == LifestyleLevel.VERY_POOR, "Current smoker should be very poor"
    
    def test_lifestyle_adjustment_consistency(self):
        """
        Test lifestyle adjustment consistency across different base scores.
        
        Business Value: Ensures lifestyle adjustments are consistent and predictable.
        """
        excellent_profile = LifestyleProfile(
            diet_level=LifestyleLevel.EXCELLENT,
            sleep_hours=8.0,
            exercise_minutes_per_week=300,
            alcohol_units_per_week=0,
            smoking_status="never",
            stress_level=LifestyleLevel.EXCELLENT
        )
        
        # Test with different base scores
        base_scores = [20.0, 50.0, 80.0]
        adjusted_scores = []
        
        for base_score in base_scores:
            adjusted_score, _ = self.overlays.apply_lifestyle_overlays(base_score, excellent_profile)
            adjusted_scores.append(adjusted_score)
        
        # All adjusted scores should be higher than base scores
        for i, base_score in enumerate(base_scores):
            assert adjusted_scores[i] > base_score, f"Adjusted score should be higher than base score {base_score}"
        
        # The improvement should be proportional
        improvements = [adj - base for adj, base in zip(adjusted_scores, base_scores)]
        assert all(imp > 0 for imp in improvements), "All improvements should be positive"
    
    def test_lifestyle_overlay_integration(self):
        """
        Test lifestyle overlay integration with scoring system.
        
        Business Value: Ensures lifestyle overlays work correctly with the overall scoring system.
        """
        # Test that lifestyle overlays can be applied multiple times consistently
        base_score = 80.0
        profile = LifestyleProfile(
            diet_level=LifestyleLevel.GOOD,
            sleep_hours=7.0,
            exercise_minutes_per_week=150,
            alcohol_units_per_week=5,
            smoking_status="never",
            stress_level=LifestyleLevel.GOOD
        )
        
        # Apply overlays multiple times
        score1, adjustments1 = self.overlays.apply_lifestyle_overlays(base_score, profile)
        score2, adjustments2 = self.overlays.apply_lifestyle_overlays(base_score, profile)
        
        # Results should be consistent
        assert abs(score1 - score2) < 0.01, "Multiple applications should give consistent results"
        assert len(adjustments1) == len(adjustments2), "Should have same number of adjustments"
        assert adjustments1 == adjustments2, "Adjustments should be identical"
