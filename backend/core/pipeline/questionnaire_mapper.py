"""
Questionnaire mapper - maps questionnaire responses to lifestyle factors and medical history.

This module converts questionnaire responses into structured data that can be used
by the scoring engine and analysis pipeline.
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from core.models.questionnaire import QuestionnaireSubmission, load_questionnaire_schema


class LifestyleLevel(Enum):
    """Lifestyle factor levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    POOR = "poor"
    VERY_POOR = "very_poor"


@dataclass
class MappedLifestyleFactors:
    """Mapped lifestyle factors from questionnaire responses."""
    diet_level: LifestyleLevel
    sleep_hours: float
    exercise_minutes_per_week: int
    alcohol_units_per_week: int
    smoking_status: str
    stress_level: LifestyleLevel
    sedentary_hours_per_day: float
    caffeine_consumption: int
    fluid_intake_liters: float


@dataclass
class MappedMedicalHistory:
    """Mapped medical history from questionnaire responses."""
    conditions: List[str]
    medications: List[str]
    family_history: List[str]
    supplements: List[str]
    sleep_disorders: List[str]
    allergies: List[str]
    # QRISK®3 cardiovascular risk factors
    atrial_fibrillation: bool
    rheumatoid_arthritis: bool
    systemic_lupus: bool
    corticosteroids: bool
    atypical_antipsychotics: bool
    hiv_treatments: bool
    migraines: bool


class QuestionnaireMapper:
    """Maps questionnaire responses to structured lifestyle and medical data."""
    
    def __init__(self):
        """Initialize the questionnaire mapper."""
        self.schema = load_questionnaire_schema()
        self._question_map = {q.id: q for q in self.schema.questions}
    
    def map_submission(self, submission: QuestionnaireSubmission) -> Tuple[MappedLifestyleFactors, MappedMedicalHistory]:
        """
        Map questionnaire submission to lifestyle factors and medical history.
        
        Args:
            submission: Questionnaire submission to map
            
        Returns:
            Tuple of (lifestyle_factors, medical_history)
        """
        responses = submission.responses
        
        # Map lifestyle factors
        lifestyle_factors = self._map_lifestyle_factors(responses)
        
        # Map medical history
        medical_history = self._map_medical_history(responses)
        
        return lifestyle_factors, medical_history
    
    def _map_lifestyle_factors(self, responses: Dict[str, Any]) -> MappedLifestyleFactors:
        """Map questionnaire responses to lifestyle factors."""
        
        # Diet level mapping
        diet_level = self._map_diet_level(responses)
        
        # Sleep hours mapping
        sleep_hours = self._map_sleep_hours(responses)
        
        # Exercise mapping
        exercise_minutes = self._map_exercise_minutes(responses)
        
        # Alcohol consumption mapping
        alcohol_units = self._map_alcohol_consumption(responses)
        
        # Smoking status mapping
        smoking_status = self._map_smoking_status(responses)
        
        # Stress level mapping
        stress_level = self._map_stress_level(responses)
        
        # Sedentary hours mapping
        sedentary_hours = self._map_sedentary_hours(responses)
        
        # Caffeine consumption mapping
        caffeine_consumption = self._map_caffeine_consumption(responses)
        
        # Fluid intake mapping
        fluid_intake = self._map_fluid_intake(responses)
        
        return MappedLifestyleFactors(
            diet_level=diet_level,
            sleep_hours=sleep_hours,
            exercise_minutes_per_week=exercise_minutes,
            alcohol_units_per_week=alcohol_units,
            smoking_status=smoking_status,
            stress_level=stress_level,
            sedentary_hours_per_day=sedentary_hours,
            caffeine_consumption=caffeine_consumption,
            fluid_intake_liters=fluid_intake
        )
    
    def _map_medical_history(self, responses: Dict[str, Any]) -> MappedMedicalHistory:
        """Map questionnaire responses to medical history."""
        
        conditions = []
        medications = []
        family_history = []
        supplements = []
        sleep_disorders = []
        allergies = []
        
        # Map conditions (chronic_conditions - Medical conditions)
        if "chronic_conditions" in responses:
            conditions = self._parse_checkbox_response(responses["chronic_conditions"])
        
        # Map medications (current_medications - Current medications)
        if "current_medications" in responses:
            medications = self._parse_checkbox_response(responses["current_medications"])
        
        # Map family history (family_* - Family history)
        if "family_cardiovascular_disease" in responses:
            family_history.extend(self._parse_checkbox_response(responses["family_cardiovascular_disease"]))
        if "family_diabetes_metabolic" in responses:
            family_history.extend(self._parse_checkbox_response(responses["family_diabetes_metabolic"]))
        if "family_cancer_history" in responses:
            family_history.extend(self._parse_checkbox_response(responses["family_cancer_history"]))
        if "family_lifespan" in responses:
            family_history.extend(self._parse_checkbox_response(responses["family_lifespan"]))
        
        # Map supplements (supplements - Supplements)
        if "supplements" in responses:
            supplements = self._parse_checkbox_response(responses["supplements"])
        
        # Map sleep disorders (sleep_disorders - Sleep disorders)
        if "sleep_disorders" in responses:
            sleep_disorders = self._parse_checkbox_response(responses["sleep_disorders"])
        
        # Map allergies (food_sensitivities - Food sensitivities/allergies)
        if "food_sensitivities" in responses:
            allergies = self._parse_checkbox_response(responses["food_sensitivities"])
        
        # Map QRISK®3 cardiovascular risk factors
        atrial_fibrillation = self._check_qrisk_condition(responses, "medical_conditions", "Atrial fibrillation")
        rheumatoid_arthritis = self._check_qrisk_condition(responses, "medical_conditions", "Rheumatoid arthritis")
        systemic_lupus = self._check_qrisk_condition(responses, "medical_conditions", "Systemic lupus erythematosus (SLE)")
        corticosteroids = self._check_qrisk_condition(responses, "long_term_medications", "Corticosteroids")
        atypical_antipsychotics = self._check_qrisk_condition(responses, "long_term_medications", "Atypical antipsychotics")
        hiv_treatments = self._check_qrisk_condition(responses, "long_term_medications", "HIV/AIDS treatments")
        migraines = self._check_qrisk_condition(responses, "regular_migraines", "Yes")
        
        return MappedMedicalHistory(
            conditions=conditions,
            medications=medications,
            family_history=family_history,
            supplements=supplements,
            sleep_disorders=sleep_disorders,
            allergies=allergies,
            atrial_fibrillation=atrial_fibrillation,
            rheumatoid_arthritis=rheumatoid_arthritis,
            systemic_lupus=systemic_lupus,
            corticosteroids=corticosteroids,
            atypical_antipsychotics=atypical_antipsychotics,
            hiv_treatments=hiv_treatments,
            migraines=migraines
        )
    
    def _map_diet_level(self, responses: Dict[str, Any]) -> LifestyleLevel:
        """Map diet-related responses to diet level."""
        diet_score = 0
        
        # Dietary pattern (dietary_pattern)
        if "dietary_pattern" in responses:
            pattern = responses["dietary_pattern"]
            if pattern == "Mediterranean":
                diet_score += 2
            elif pattern == "Plant-based":
                diet_score += 2
            elif pattern == "Low-carb/Keto":
                diet_score += 1
            elif pattern == "Intermittent fasting":
                diet_score += 1
            elif pattern == "None":
                diet_score += 0
        
        # Fruit and vegetable servings (fruit_vegetable_servings)
        if "fruit_vegetable_servings" in responses:
            servings = responses["fruit_vegetable_servings"]
            if servings == "6+ servings":
                diet_score += 2
            elif servings == "4-5 servings":
                diet_score += 1
            elif servings == "2-3 servings":
                diet_score += 0
            elif servings == "0-1 servings":
                diet_score -= 1
        
        # Sugar-sweetened beverages (sugar_beverages_weekly)
        if "sugar_beverages_weekly" in responses:
            beverages = responses["sugar_beverages_weekly"]
            if beverages == "None":
                diet_score += 1
            elif beverages == "1-3 drinks":
                diet_score += 0
            elif beverages == "4-7 drinks":
                diet_score -= 1
            elif beverages in ["8-14 drinks", "15+ drinks"]:
                diet_score -= 2
        
        # Convert score to lifestyle level
        if diet_score >= 4:
            return LifestyleLevel.EXCELLENT
        elif diet_score >= 2:
            return LifestyleLevel.GOOD
        elif diet_score >= 0:
            return LifestyleLevel.AVERAGE
        elif diet_score >= -2:
            return LifestyleLevel.POOR
        else:
            return LifestyleLevel.VERY_POOR
    
    def _map_sleep_hours(self, responses: Dict[str, Any]) -> float:
        """Map sleep hours from questionnaire responses."""
        if "sleep_hours_nightly" in responses:
            sleep_range = responses["sleep_hours_nightly"]
            if sleep_range == "Less than 5 hours":
                return 4.5
            elif sleep_range == "5-6 hours":
                return 5.5
            elif sleep_range == "7-8 hours":
                return 7.5
            elif sleep_range == "9+ hours":
                return 9.0
        return 7.0  # Default
    
    def _map_exercise_minutes(self, responses: Dict[str, Any]) -> int:
        """Map exercise minutes per week from questionnaire responses."""
        total_minutes = 0
        
        # Vigorous exercise (vigorous_exercise_days)
        if "vigorous_exercise_days" in responses:
            vigorous_days = responses["vigorous_exercise_days"]
            if vigorous_days == "4+ days":
                total_minutes += 120  # 4 days * 30 min
            elif vigorous_days == "3 days":
                total_minutes += 90
            elif vigorous_days == "2 days":
                total_minutes += 60
            elif vigorous_days == "1 day":
                total_minutes += 30
        
        # Resistance training (resistance_training_days)
        if "resistance_training_days" in responses:
            resistance_days = responses["resistance_training_days"]
            if resistance_days == "3+ days":
                total_minutes += 90  # 3 days * 30 min
            elif resistance_days == "2 days":
                total_minutes += 60
            elif resistance_days == "1 day":
                total_minutes += 30
        
        return total_minutes
    
    def _map_alcohol_consumption(self, responses: Dict[str, Any]) -> int:
        """Map alcohol consumption to units per week."""
        # Check both possible field names for backward compatibility
        consumption = None
        if "alcohol_drinks_weekly" in responses:
            consumption = responses["alcohol_drinks_weekly"]
        elif "alcohol_consumption" in responses:
            consumption = responses["alcohol_consumption"]
        
        if consumption:
            if consumption == "None":
                return 0
            elif consumption == "1-3 drinks":
                return 2
            elif consumption == "4-7 drinks":
                return 5
            elif consumption == "8-14 drinks":
                return 11
            elif consumption == "15+ drinks":
                return 20
        return 5  # Default moderate
    
    def _map_smoking_status(self, responses: Dict[str, Any]) -> str:
        """Map smoking status from questionnaire responses."""
        # Check both possible field names for backward compatibility
        status = None
        if "tobacco_use" in responses:
            status = responses["tobacco_use"]
        elif "smoking_status" in responses:
            status = responses["smoking_status"]
        
        if status:
            # Handle case-insensitive matching
            status_lower = status.lower()
            if status_lower in ["never used", "never"]:
                return "never"
            elif status_lower in ["former user quit >1 year", "former user quit <1 year", "former"]:
                return "former"
            elif status_lower in ["occasional use", "daily use", "current"]:
                return "current"
        return "never"  # Default
    
    def _map_stress_level(self, responses: Dict[str, Any]) -> LifestyleLevel:
        """Map stress level from questionnaire responses."""
        stress_score = 0
        
        # Average stress level (stress_level_rating)
        if "stress_level_rating" in responses:
            stress_level = responses["stress_level_rating"]
            if isinstance(stress_level, (int, float)):
                if stress_level <= 3:
                    stress_score += 2
                elif stress_level <= 5:
                    stress_score += 1
                elif stress_level <= 7:
                    stress_score += 0
                elif stress_level <= 9:
                    stress_score -= 1
                else:
                    stress_score -= 2
        
        # Control over important things (stress_control_frequency)
        if "stress_control_frequency" in responses:
            control = responses["stress_control_frequency"]
            if control == "Never":
                stress_score += 1
            elif control == "Almost never":
                stress_score += 0
            elif control == "Sometimes":
                stress_score -= 1
            elif control in ["Fairly often", "Very often"]:
                stress_score -= 2
        
        # Major life stressors (major_life_stressors)
        if "major_life_stressors" in responses:
            stressors = responses["major_life_stressors"]
            if stressors == "No major stressors":
                stress_score += 1
            elif stressors == "1 major stressor":
                stress_score += 0
            elif stressors == "2-3 major stressors":
                stress_score -= 1
            elif stressors == "4+ major stressors":
                stress_score -= 2
        
        # Convert score to lifestyle level
        if stress_score >= 3:
            return LifestyleLevel.EXCELLENT
        elif stress_score >= 1:
            return LifestyleLevel.GOOD
        elif stress_score >= -1:
            return LifestyleLevel.AVERAGE
        elif stress_score >= -3:
            return LifestyleLevel.POOR
        else:
            return LifestyleLevel.VERY_POOR
    
    def _map_sedentary_hours(self, responses: Dict[str, Any]) -> float:
        """Map sedentary hours per day from questionnaire responses."""
        if "sitting_hours_daily" in responses:
            sitting_time = responses["sitting_hours_daily"]
            if sitting_time == "Less than 4 hours":
                return 3.0
            elif sitting_time == "4-6 hours":
                return 5.0
            elif sitting_time == "7-9 hours":
                return 8.0
            elif sitting_time == "10-12 hours":
                return 11.0
            elif sitting_time == "13+ hours":
                return 14.0
        return 8.0  # Default
    
    def _map_caffeine_consumption(self, responses: Dict[str, Any]) -> int:
        """Map caffeine consumption from questionnaire responses."""
        if "caffeine_beverages_daily" in responses:
            consumption = responses["caffeine_beverages_daily"]
            if consumption == "None":
                return 0
            elif consumption == "1-2":
                return 1
            elif consumption == "3-4":
                return 3
            elif consumption == "5-6":
                return 5
            elif consumption == "7+":
                return 8
        return 2  # Default moderate
    
    def _map_fluid_intake(self, responses: Dict[str, Any]) -> float:
        """Map fluid intake from questionnaire responses."""
        if "daily_fluid_intake" in responses:
            intake = responses["daily_fluid_intake"]
            if intake == "Less than 1 litre":
                return 0.5
            elif intake == "1-2 litres":
                return 1.5
            elif intake == "2-3 litres":
                return 2.5
            elif intake == "More than 3 litres":
                return 3.5
        return 2.0  # Default
    
    def _parse_checkbox_response(self, response: Any) -> List[str]:
        """Parse checkbox response into list of strings."""
        if isinstance(response, list):
            return response
        elif isinstance(response, str):
            return [response]
        else:
            return []
    
    def get_demographic_data(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract demographic data from questionnaire responses.
        
        Args:
            responses: Questionnaire responses
            
        Returns:
            Dictionary of demographic data
        """
        demographics = {}
        
        # Age calculation from date of birth (date_of_birth)
        if "date_of_birth" in responses:
            # This would need proper date parsing in a real implementation
            demographics["age"] = 35  # Placeholder
        
        # Gender (biological_sex)
        if "biological_sex" in responses:
            demographics["gender"] = responses["biological_sex"].lower()
        
        # Height (height)
        if "height" in responses:
            height_data = responses["height"]
            if isinstance(height_data, dict):
                if "Feet" in height_data and "Inches" in height_data:
                    # Convert to cm
                    feet = height_data.get("Feet", 0)
                    inches = height_data.get("Inches", 0)
                    height_cm = (feet * 12 + inches) * 2.54
                    demographics["height"] = height_cm
                elif "Height (cm)" in height_data:
                    demographics["height"] = height_data["Height (cm)"]
        
        # Weight (weight)
        if "weight" in responses:
            weight_data = responses["weight"]
            if isinstance(weight_data, dict):
                if "Weight (kg)" in weight_data:
                    demographics["weight"] = weight_data["Weight (kg)"]
                elif "Weight (lbs)" in weight_data:
                    # Convert to kg
                    weight_kg = weight_data["Weight (lbs)"] * 0.453592
                    demographics["weight"] = weight_kg
        
        # Ethnicity (ethnicity)
        if "ethnicity" in responses:
            demographics["ethnicity"] = responses["ethnicity"]
        
        return demographics
    
    def _check_qrisk_condition(self, responses: Dict[str, Any], question_id: str, condition: str) -> bool:
        """Check if a specific QRISK®3 condition is present in the responses."""
        if question_id not in responses:
            return False
        
        response = responses[question_id]
        
        # Handle checkbox responses (list of selected options)
        if isinstance(response, list):
            return condition in response
        
        # Handle single value responses
        if isinstance(response, str):
            return response == condition
        
        return False
