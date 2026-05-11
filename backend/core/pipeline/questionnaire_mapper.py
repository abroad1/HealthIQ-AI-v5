"""
Questionnaire mapper - maps questionnaire responses to lifestyle factors and medical history.

This module converts questionnaire responses into structured data that can be used
by the scoring engine and analysis pipeline.
"""

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from core.models.questionnaire import QuestionnaireSubmission, load_questionnaire_schema

# LC-S2 — governed statin intake label (must match SSOT questionnaire.json option text).
STATINS_LONG_TERM_MEDICATION_LABEL = "Statins (cholesterol medication)"


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
    # None = dimension not answered / not applicable — overlays must not invent defaults (WP3).
    diet_level: Optional[LifestyleLevel]
    sleep_hours: Optional[float]
    # None = exercise questions not answered (unknown); do not coerce to 0 — avoids false VERY_POOR exercise overlay (OBS-2).
    exercise_minutes_per_week: Optional[int]
    alcohol_units_per_week: Optional[int]
    smoking_status: Optional[str]
    stress_level: Optional[LifestyleLevel]
    sedentary_hours_per_day: Optional[float]
    caffeine_consumption: Optional[int]
    fluid_intake_liters: Optional[float]


@dataclass
class MappedMedicalHistory:
    """Mapped medical history from questionnaire responses."""
    conditions: List[str]
    medications: List[str]
    family_history: List[str]
    supplements: List[str]
    long_term_medication_classes: List[str]
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
    
    def build_user_intervention_document_for_statin(self, responses: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        When the SSOT long_term_medications checkbox includes the governed statin label, emit a
        KB-S48d-compliant user_intervention_document (single mapped lipid_lowering_statin record).

        Deterministic defaults only — no wall-clock timestamps (replay-stable).
        """
        if not isinstance(responses, dict):
            return None
        raw = responses.get("long_term_medications")
        choices = self._parse_checkbox_response(raw)
        if STATINS_LONG_TERM_MEDICATION_LABEL not in choices:
            return None
        return {
            "schema_version": "1.0.0",
            "intervention_records": [
                {
                    "intervention_record_id": "rec_questionnaire_statin_001",
                    "intervention_type": "medication",
                    "entered_label": STATINS_LONG_TERM_MEDICATION_LABEL,
                    "canonical_class": {
                        "link_status": "mapped",
                        "intervention_class_id": "lipid_lowering_statin",
                    },
                    "timeline": {
                        "effective_from_date": None,
                        "effective_to_date": None,
                        "is_ongoing": True,
                        "change_event_type": "started",
                    },
                    "provenance": {
                        "source_type": "user_reported",
                        "confidence": "estimated",
                    },
                }
            ],
        }

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
        
        # Map family history (family_* - Family history)
        if "family_cardiovascular_disease" in responses:
            family_history.extend(self._parse_checkbox_response(responses["family_cardiovascular_disease"]))
        if "family_diabetes_metabolic" in responses:
            family_history.extend(self._parse_checkbox_response(responses["family_diabetes_metabolic"]))
        if "family_cancer_history" in responses:
            family_history.extend(self._parse_checkbox_response(responses["family_cancer_history"]))
        if "family_lifespan" in responses:
            family_history.extend(self._parse_checkbox_response(responses["family_lifespan"]))
        
        # Map supplements (supplements — SSOT checkbox, semi-structured; distinct from medications)
        if "supplements" in responses:
            supplements = self._parse_checkbox_response(responses["supplements"])

        long_term_medication_classes: List[str] = []
        if "long_term_medications" in responses:
            long_term_medication_classes = self._parse_checkbox_response(
                responses["long_term_medications"]
            )
        
        # Map sleep disorders (sleep_disorders - Sleep disorders)
        if "sleep_disorders" in responses:
            sleep_disorders = self._parse_checkbox_response(responses["sleep_disorders"])
        
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
            long_term_medication_classes=long_term_medication_classes,
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
    
    def _map_diet_level(self, responses: Dict[str, Any]) -> Optional[LifestyleLevel]:
        """Map diet-related responses to diet level (unknown when dietary_pattern not answered)."""
        if "dietary_pattern" not in responses:
            return None
        diet_score = 0

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

        if diet_score >= 4:
            return LifestyleLevel.EXCELLENT
        if diet_score >= 2:
            return LifestyleLevel.GOOD
        if diet_score >= 0:
            return LifestyleLevel.AVERAGE
        if diet_score >= -2:
            return LifestyleLevel.POOR
        return LifestyleLevel.VERY_POOR

    def _map_sleep_hours(self, responses: Dict[str, Any]) -> Optional[float]:
        """Map sleep hours from questionnaire responses (unknown when unanswered)."""
        if "sleep_hours_nightly" not in responses:
            return None
        sleep_range = responses["sleep_hours_nightly"]
        if sleep_range == "Less than 5 hours":
            return 4.5
        if sleep_range == "5-6 hours":
            return 5.5
        if sleep_range == "7-8 hours":
            return 7.5
        if sleep_range == "9+ hours":
            return 9.0
        return None
    
    def _map_exercise_minutes(self, responses: Dict[str, Any]) -> Optional[int]:
        """Map exercise minutes per week from questionnaire responses.

        When neither vigorous nor resistance exercise question is present, returns None (unknown).
        Present keys with recognised option values contribute minutes; explicit absence of both keys
        must not be treated as zero weekly exercise (OBS-2).
        """
        has_vigorous = "vigorous_exercise_days" in responses
        has_resistance = "resistance_training_days" in responses
        if not has_vigorous and not has_resistance:
            return None

        total_minutes = 0

        # Vigorous exercise (vigorous_exercise_days)
        if has_vigorous:
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
        if has_resistance:
            resistance_days = responses["resistance_training_days"]
            if resistance_days == "3+ days":
                total_minutes += 90  # 3 days * 30 min
            elif resistance_days == "2 days":
                total_minutes += 60
            elif resistance_days == "1 day":
                total_minutes += 30

        return total_minutes
    
    def _map_alcohol_consumption(self, responses: Dict[str, Any]) -> Optional[int]:
        """Map alcohol consumption to units per week (unknown when unanswered — WP3)."""
        consumption = None
        if "alcohol_drinks_weekly" in responses:
            consumption = responses["alcohol_drinks_weekly"]
        elif "alcohol_consumption" in responses:
            consumption = responses["alcohol_consumption"]
        if consumption is None or consumption == "":
            return None
        if consumption == "None":
            return 0
        if consumption == "1-3 drinks":
            return 2
        if consumption == "4-7 drinks":
            return 5
        if consumption == "8-14 drinks":
            return 11
        if consumption == "15+ drinks":
            return 20
        return None
    
    def _map_smoking_status(self, responses: Dict[str, Any]) -> Optional[str]:
        """Map smoking status from questionnaire responses."""
        status = None
        if "tobacco_use" in responses:
            status = responses["tobacco_use"]
        elif "smoking_status" in responses:
            status = responses["smoking_status"]

        if status is None or status == "":
            return None
        status_lower = str(status).lower()
        if status_lower in ["never used", "never"]:
            return "never"
        if status_lower in ["former user quit >1 year", "former user quit <1 year", "former"]:
            return "former"
        if status_lower in ["occasional use", "daily use", "current"]:
            return "current"
        return None

    def _map_stress_level(self, responses: Dict[str, Any]) -> Optional[LifestyleLevel]:
        """Map stress level from questionnaire responses (unknown when slider not answered)."""
        if "stress_level_rating" not in responses:
            return None
        stress_level = responses["stress_level_rating"]
        if not isinstance(stress_level, (int, float)):
            return None
        stress_score = 0
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

        if stress_score >= 3:
            return LifestyleLevel.EXCELLENT
        if stress_score >= 1:
            return LifestyleLevel.GOOD
        if stress_score >= -1:
            return LifestyleLevel.AVERAGE
        if stress_score >= -3:
            return LifestyleLevel.POOR
        return LifestyleLevel.VERY_POOR

    def _map_sedentary_hours(self, responses: Dict[str, Any]) -> Optional[float]:
        """Map sedentary hours per day from questionnaire responses."""
        if "sitting_hours_daily" not in responses:
            return None
        sitting_time = responses["sitting_hours_daily"]
        if sitting_time == "Less than 4 hours":
            return 3.0
        if sitting_time == "4-6 hours":
            return 5.0
        if sitting_time == "7-9 hours":
            return 8.0
        if sitting_time == "10-12 hours":
            return 11.0
        if sitting_time == "13+ hours":
            return 14.0
        return None

    def _map_caffeine_consumption(self, responses: Dict[str, Any]) -> Optional[int]:
        """Map caffeine consumption from questionnaire responses."""
        if "caffeine_beverages_daily" not in responses:
            return None
        consumption = responses["caffeine_beverages_daily"]
        if consumption == "None":
            return 0
        if consumption == "1-2":
            return 1
        if consumption == "3-4":
            return 3
        if consumption == "5-6":
            return 5
        if consumption == "7+":
            return 8
        return None

    def _map_fluid_intake(self, responses: Dict[str, Any]) -> Optional[float]:
        """Map fluid intake from questionnaire responses."""
        if "daily_fluid_intake" not in responses:
            return None
        intake = responses["daily_fluid_intake"]
        if intake == "Less than 1 litre":
            return 0.5
        if intake == "1-2 litres":
            return 1.5
        if intake == "2-3 litres":
            return 2.5
        if intake == "More than 3 litres":
            return 3.5
        return None
    
    def _parse_checkbox_response(self, response: Any) -> List[str]:
        """Parse checkbox response into list of strings."""
        if isinstance(response, list):
            return response
        elif isinstance(response, str):
            return [response]
        else:
            return []

    def extract_objective_lifestyle_inputs(self, responses: Dict[str, Any]) -> Dict[str, float]:
        """
        Map objective questionnaire fields to LifestyleModifierEngine canonical keys.

        CONTEXT-HARDENING-B — SSOT: ``waist_circumference`` primary unit is inches (numeric);
        alternative captures cm under dict key ``Waist circumference (cm)``.
        ``blood_pressure_reading`` uses group labels ``Systolic (mmHg)`` / ``Diastolic (mmHg)``.

        Omits BP keys when absent or non-positive (do not inject sentinel zeros).
        """
        out: Dict[str, float] = {}
        cm_key = "Waist circumference (cm)"

        if "waist_circumference" in responses:
            raw = responses["waist_circumference"]
            if isinstance(raw, (int, float)):
                # SSOT primary label: inches → centimetres
                inches = float(raw)
                if inches > 0:
                    out["waist_circumference_cm"] = round(inches * 2.54, 4)
            elif isinstance(raw, dict):
                if cm_key in raw and raw[cm_key] is not None:
                    try:
                        cm = float(raw[cm_key])
                        if cm > 0:
                            out["waist_circumference_cm"] = cm
                    except (TypeError, ValueError):
                        pass

        if "blood_pressure_reading" in responses:
            bp = responses["blood_pressure_reading"]
            if isinstance(bp, dict):
                sys_lbl = "Systolic (mmHg)"
                dia_lbl = "Diastolic (mmHg)"
                if sys_lbl in bp and bp[sys_lbl] is not None:
                    try:
                        s = float(bp[sys_lbl])
                        if s > 0:
                            out["systolic_bp"] = s
                    except (TypeError, ValueError):
                        pass
                if dia_lbl in bp and bp[dia_lbl] is not None:
                    try:
                        d = float(bp[dia_lbl])
                        if d > 0:
                            out["diastolic_bp"] = d
                    except (TypeError, ValueError):
                        pass

        return out

    def extract_behavioural_lifestyle_inputs(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """
        CONTEXT-HARDENING-C — Map behavioural questionnaire fields to ``lifestyle_registry.yaml`` engine keys.

        Emits only keys for SSOT fields that are present with a recognised value (no sentinel defaults).
        Canonical keys: ``sleep_hours``, ``alcohol_units_per_week``, ``smoking_status``.
        """
        out: Dict[str, Any] = {}

        shr = responses.get("sleep_hours_nightly")
        if shr is not None:
            if shr == "Less than 5 hours":
                out["sleep_hours"] = 4.5
            elif shr == "5-6 hours":
                out["sleep_hours"] = 5.5
            elif shr == "7-8 hours":
                out["sleep_hours"] = 7.5
            elif shr == "9+ hours":
                out["sleep_hours"] = 9.0

        consumption = responses.get("alcohol_drinks_weekly")
        if consumption is None:
            consumption = responses.get("alcohol_consumption")
        if consumption is not None:
            if consumption == "None":
                out["alcohol_units_per_week"] = 0.0
            elif consumption == "1-3 drinks":
                out["alcohol_units_per_week"] = 2.0
            elif consumption == "4-7 drinks":
                out["alcohol_units_per_week"] = 5.0
            elif consumption == "8-14 drinks":
                out["alcohol_units_per_week"] = 11.0
            elif consumption == "15+ drinks":
                out["alcohol_units_per_week"] = 20.0

        raw_tobacco = responses.get("tobacco_use")
        raw_smoking = responses.get("smoking_status")
        status_raw = raw_tobacco if raw_tobacco is not None else raw_smoking
        if status_raw is not None and str(status_raw).strip():
            sl = str(status_raw).strip().lower()
            if sl in ["never used", "never"]:
                out["smoking_status"] = "never"
            elif sl in ["former user quit >1 year", "former user quit <1 year", "former"]:
                out["smoking_status"] = "former"
            elif sl in ["occasional use", "daily use", "current"]:
                out["smoking_status"] = "current"

        return out

    def get_demographic_data(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract demographic data from questionnaire responses.
        
        Args:
            responses: Questionnaire responses
            
        Returns:
            Dictionary of demographic data
        """
        demographics = {}
        
        # Age from date_of_birth (ISO date or date string); skip if parsing fails
        if "date_of_birth" in responses:
            raw_dob = responses["date_of_birth"]
            try:
                if hasattr(raw_dob, "isoformat"):
                    dob = raw_dob if isinstance(raw_dob, date) else date.fromisoformat(str(raw_dob)[:10])
                else:
                    dob_str = str(raw_dob).replace("Z", "").split("T")[0].strip()
                    dob = date.fromisoformat(dob_str)
                today = date.today()
                demographics["age"] = today.year - dob.year - (
                    (today.month, today.day) < (dob.month, dob.day)
                )
            except (ValueError, TypeError, AttributeError):
                pass

        # Gender (biological_sex)
        if "biological_sex" in responses:
            g = str(responses["biological_sex"]).strip().lower()
            if g == "intersex":
                g = "other"
            demographics["gender"] = g
        
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
            elif isinstance(weight_data, (int, float)):
                demographics["weight"] = float(weight_data) * 0.453592

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
