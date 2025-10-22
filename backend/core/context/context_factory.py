"""
Context Factory Service

This module provides the ContextFactory class for creating validated AnalysisContext objects
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

from typing import Dict, List, Optional, Union, Any, Tuple
from decimal import Decimal
import decimal
from datetime import datetime, date
import logging
import uuid
import os

from pydantic import ValidationError as PydanticValidationError

from .models import AnalysisContext, UserContext, BiomarkerContext, BiomarkerPanel, ScoringMetrics, Sex


# Configure logging
logger = logging.getLogger(__name__)


class ContextFactoryError(Exception):
    """Base exception for ContextFactory errors."""
    pass


class ValidationError(ContextFactoryError):
    """Exception raised when data validation fails."""
    pass


class ContextFactory:
    """
    Factory for creating validated AnalysisContext objects from raw data.
    
    This class provides the single entry point for converting raw biomarker panel data
    and user information into validated AnalysisContext objects. It handles all validation,
    data conversion, and error handling to ensure data integrity.
    
    The factory supports:
    - Raw data validation and sanitization
    - Biomarker panel creation with proper validation
    - User context creation with demographic and lifestyle data
    - Analysis context assembly with optional questionnaire data
    - Backward compatibility for legacy data formats
    - Comprehensive error handling and logging
    """
    
    def __init__(self, enable_logging: bool = True, strict_validation: Optional[bool] = None):
        """
        Initialize the ContextFactory.
        
        Args:
            enable_logging: Whether to enable logging for factory operations
            strict_validation: If True, raises on first invalid biomarker instead of skipping.
                              If None, uses STRICT_VALIDATION environment variable.
        """
        self.enable_logging = enable_logging
        
        if strict_validation is None:
            strict_validation = os.getenv("STRICT_VALIDATION", "false").lower() == "true"
        
        self.strict_validation = strict_validation
        
        if self.strict_validation:
            self._log("Strict validation mode enabled - will fail on first invalid biomarker", "INFO")
        
        self._log("ContextFactory initialized")
    
    def _log(self, message: str, level: str = "INFO") -> None:
        """Log a message if logging is enabled."""
        if self.enable_logging:
            if level == "ERROR":
                logger.error(message)
            elif level == "WARNING":
                logger.warning(message)
            else:
                logger.info(message)
    
    def create_context(
        self,
        payload: Dict[str, Any],
        analysis_id: Optional[str] = None,
        scoring_metrics: Optional[Dict[str, Any]] = None,
        validate_requirements: Optional[Dict[str, Any]] = None
    ) -> AnalysisContext:
        """
        Create a validated AnalysisContext from raw payload data.
        
        This is the main entry point for creating analysis contexts. It validates
        and converts raw data into properly structured AnalysisContext objects.
        
        Args:
            payload: Raw payload data containing biomarkers and user data
            analysis_id: Optional analysis identifier (generated if not provided)
            scoring_metrics: Optional scoring metrics data
            validate_requirements: Optional requirements to validate against
            
        Returns:
            Validated AnalysisContext object
            
        Raises:
            ValidationError: If data validation fails
            ContextFactoryError: If context creation fails
        """
        try:
            self._log(f"[TRACE] Validating payload with ContextFactory")
            
            # Extract required sections from payload
            raw_biomarkers = payload.get('biomarkers', {})
            raw_user_data = payload.get('user', {})
            questionnaire_data = payload.get('questionnaire')
            
            # Check if this is a panel-based payload
            is_panel_payload = 'panel' in payload or 'panel_name' in payload or 'panel_type' in payload
            
            # Validate required sections
            if not raw_biomarkers and not is_panel_payload:
                raise ValidationError("Payload must contain 'biomarkers' section")
            if not raw_user_data:
                raise ValidationError("Payload must contain 'user' section")
            
            # Generate analysis ID if not provided
            if analysis_id is None:
                analysis_id = self._generate_analysis_id()
            
            # Create validated user context
            user_context = self._create_user_context(raw_user_data)
            self._log(f"[TRACE] Created user context for user_id: {user_context.user_id}")
            
            # Handle panel-based payload
            biomarker_panel = None
            biomarker_contexts = None
            
            if is_panel_payload:
                # Create biomarker panel with metadata
                if 'panel' in payload:
                    panel_data = payload['panel']
                else:
                    # Use entire payload if panel data is at root level
                    panel_data = payload
                biomarker_panel = self._create_biomarker_panel(panel_data)
                self._log(f"[TRACE] Created biomarker panel with {len(biomarker_panel.biomarkers)} biomarkers")
            else:
                # Create individual biomarker contexts (legacy mode)
                biomarker_contexts = {}
                for name, raw_biomarker in raw_biomarkers.items():
                    try:
                        biomarker_context = self._create_biomarker_context(name, raw_biomarker)
                        biomarker_contexts[name.lower()] = biomarker_context
                    except Exception as e:
                        if self.strict_validation:
                            # In strict mode, re-raise the exception to fail context creation
                            self._log(f"Strict validation: failing on invalid biomarker '{name}': {str(e)}", "ERROR")
                            raise ValidationError(f"Strict validation failed for biomarker '{name}': {str(e)}") from e
                        else:
                            # In normal mode, log warning and continue
                            self._log(f"Failed to create biomarker '{name}': {str(e)}", "WARNING")
                            continue
                
                if not biomarker_contexts:
                    raise ValidationError("No valid biomarkers found in payload")
                
                self._log(f"[TRACE] Created {len(biomarker_contexts)} individual biomarkers")
            
            # Create scoring metrics if provided
            scoring_metrics_obj = None
            if scoring_metrics:
                scoring_metrics_obj = self._create_scoring_metrics(scoring_metrics)
                self._log("[TRACE] Created scoring metrics")
            
            # Create analysis context
            analysis_context = AnalysisContext(
                biomarkers=biomarker_contexts,
                biomarker_panel=biomarker_panel,
                user=user_context,
                questionnaire=questionnaire_data,
                scoring_metrics=scoring_metrics_obj,
                analysis_id=analysis_id
            )
            
            # Validate against requirements if provided
            if validate_requirements:
                validation_result = analysis_context.validate_analysis_requirements(validate_requirements)
                if not validation_result['valid']:
                    error_msg = f"Analysis context validation failed: {', '.join(validation_result['errors'])}"
                    self._log(error_msg, "ERROR")
                    raise ValidationError(error_msg)
                
                if validation_result['warnings']:
                    self._log(f"Analysis context validation warnings: {', '.join(validation_result['warnings'])}", "WARNING")
            
            biomarker_count = len(biomarker_panel.biomarkers) if biomarker_panel else len(biomarker_contexts or {})
            self._log(f"[OK] AnalysisContext validated successfully with {biomarker_count} biomarkers, user={user_context.user_id}")
            return analysis_context
            
        except PydanticValidationError as e:
            error_msg = f"Data validation failed: {str(e)}"
            self._log(f"[ERROR] ContextFactory validation failed: {error_msg}", "ERROR")
            raise ValidationError(error_msg) from e
        except Exception as e:
            error_msg = f"Failed to create analysis context: {str(e)}"
            self._log(f"[ERROR] ContextFactory validation failed: {error_msg}", "ERROR")
            raise ContextFactoryError(error_msg) from e
    
    def _create_biomarker_context(self, name: str, raw_biomarker: Dict[str, Any]) -> BiomarkerContext:
        """
        Create a validated BiomarkerContext from raw biomarker data.
        
        Args:
            name: Biomarker name
            raw_biomarker: Raw biomarker data dictionary
            
        Returns:
            Validated BiomarkerContext object
            
        Raises:
            ValidationError: If biomarker data validation fails
        """
        try:
            # Handle different input formats
            if isinstance(raw_biomarker, (int, float, str)):
                # Simple value format
                value = raw_biomarker
                unit = "unknown"
                measured_at = None
                reference_range = None
                notes = None
            elif isinstance(raw_biomarker, dict):
                # Complex format with metadata
                value = raw_biomarker.get('value')
                unit = raw_biomarker.get('unit', 'unknown')
                measured_at = self._parse_datetime(raw_biomarker.get('measured_at'))
                reference_range = raw_biomarker.get('reference_range')
                notes = raw_biomarker.get('notes')
            else:
                raise ValidationError(f"Invalid biomarker data format for '{name}': {type(raw_biomarker)}")
            
            # Validate value is present and numeric
            if value is None:
                raise ValidationError(f"Biomarker '{name}' must have a value")
            
            # Convert value to numeric using strict parsing
            try:
                value = self._parse_decimal(value)
            except ValueError as e:
                raise ValidationError(f"Biomarker '{name}' value must be numeric: {str(e)}") from e
            
            # Validate reference range if provided
            if reference_range:
                try:
                    reference_range = self._validate_reference_range(reference_range)
                except ValidationError as e:
                    self._log(f"[WARN] Invalid reference range for biomarker '{name}': {str(e)}", "WARNING")
                    reference_range = None
            
            return BiomarkerContext(
                name=name,
                value=value,
                unit=unit,
                measured_at=measured_at,
                reference_range=reference_range,
                notes=notes
            )
            
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Failed to create biomarker '{name}': {str(e)}") from e
    
    def _create_user_context(self, raw_user_data: Dict[str, Any]) -> UserContext:
        """
        Create a validated UserContext from raw user data.
        
        Args:
            raw_user_data: Raw user data dictionary
            
        Returns:
            Validated UserContext object
            
        Raises:
            ValidationError: If user data validation fails
        """
        try:
            # Extract required fields with defaults
            user_id = raw_user_data.get('user_id', str(uuid.uuid4()))
            sex = self._parse_sex(raw_user_data.get('sex', 'other'))
            chronological_age = int(raw_user_data.get('chronological_age', 0))
            height_cm = self._parse_decimal(raw_user_data.get('height_cm', 0))
            weight_kg = self._parse_decimal(raw_user_data.get('weight_kg', 0))
            
            # Extract optional fields with defaults
            waist_cm = raw_user_data.get('waist_cm')
            if waist_cm is not None:
                waist_cm = self._parse_decimal(waist_cm)
            
            stress_level = int(raw_user_data.get('stress_level', 5))
            sleep_hours = self._parse_decimal(raw_user_data.get('sleep_hours', 8.0))
            physical_activity_minutes = int(raw_user_data.get('physical_activity_minutes', 0))
            fluid_intake_frequency = raw_user_data.get('fluid_intake_frequency', 'moderate')
            alcohol_units_per_week = int(raw_user_data.get('alcohol_units_per_week', 0))
            exercise_days_per_week = int(raw_user_data.get('exercise_days_per_week', 0))
            smoking_status = raw_user_data.get('smoking_status', 'never')
            
            # Extract optional fields
            medical_conditions = raw_user_data.get('medical_conditions', [])
            medications = raw_user_data.get('medications', [])
            family_history = raw_user_data.get('family_history', {})
            
            # Parse timestamps
            created_at = self._parse_datetime(raw_user_data.get('created_at'))
            updated_at = self._parse_datetime(raw_user_data.get('updated_at'))
            
            return UserContext(
                user_id=user_id,
                sex=sex,
                chronological_age=chronological_age,
                height_cm=height_cm,
                weight_kg=weight_kg,
                waist_cm=waist_cm,
                stress_level=stress_level,
                sleep_hours=sleep_hours,
                physical_activity_minutes=physical_activity_minutes,
                fluid_intake_frequency=fluid_intake_frequency,
                alcohol_units_per_week=alcohol_units_per_week,
                exercise_days_per_week=exercise_days_per_week,
                smoking_status=smoking_status,
                medical_conditions=medical_conditions,
                medications=medications,
                family_history=family_history,
                created_at=created_at,
                updated_at=updated_at
            )
            
        except Exception as e:
            raise ValidationError(f"Failed to create user context: {str(e)}") from e
    
    def _parse_decimal(self, value: Any) -> float:
        """
        Convert input to float with strict numeric validation.
        Raises ValueError if value is not numeric or cannot be parsed.
        """
        logger.debug(f"Parsing biomarker value: {value} ({type(value).__name__})")
        
        if isinstance(value, (int, float, Decimal)):
            return float(value)
        try:
            return float(Decimal(str(value)))
        except (decimal.InvalidOperation, TypeError, ValueError):
            raise ValueError(f"Invalid numeric value for biomarker: {value!r}")
    
    def _parse_datetime(self, value: Any) -> Optional[datetime]:
        """
        Parse a value to datetime with proper error handling.
        
        Args:
            value: Value to parse
            
        Returns:
            datetime value or None
        """
        if value is None:
            return None
        
        try:
            if isinstance(value, datetime):
                return value
            elif isinstance(value, date):
                return datetime.combine(value, datetime.min.time())
            elif isinstance(value, str):
                # Try ISO format first
                try:
                    return datetime.fromisoformat(value.replace('Z', '+00:00'))
                except ValueError:
                    # Try other common formats
                    for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y']:
                        try:
                            return datetime.strptime(value, fmt)
                        except ValueError:
                            continue
                    raise ValueError(f"Unable to parse datetime string: {value}")
            else:
                raise ValueError(f"Cannot convert {type(value)} to datetime")
        except Exception as e:
            raise ValidationError(f"Cannot convert '{value}' to datetime: {str(e)}") from e
    
    def _parse_sex(self, value: Any) -> Sex:
        """
        Parse a value to Sex enum with proper error handling.
        
        Args:
            value: Value to parse
            
        Returns:
            Sex enum value
            
        Raises:
            ValidationError: If value cannot be parsed to Sex
        """
        if value is None:
            return Sex.OTHER
        
        try:
            if isinstance(value, Sex):
                return value
            elif isinstance(value, str):
                return Sex(value.lower().strip())
            else:
                raise ValueError(f"Cannot convert {type(value)} to Sex")
        except (ValueError, TypeError) as e:
            raise ValidationError(f"Cannot convert '{value}' to Sex: {str(e)}") from e
    
    def _create_scoring_metrics(self, raw_scoring_data: Dict[str, Any]) -> ScoringMetrics:
        """
        Create a validated ScoringMetrics from raw scoring data.
        
        Args:
            raw_scoring_data: Raw scoring data dictionary
            
        Returns:
            Validated ScoringMetrics object
            
        Raises:
            ValidationError: If scoring data validation fails
        """
        try:
            # Extract scores with proper numeric conversion
            raw_scores = {
                k: self._parse_decimal(v) 
                for k, v in raw_scoring_data.get('raw_scores', {}).items()
            }
            
            weighted_scores = {
                k: self._parse_decimal(v) 
                for k, v in raw_scoring_data.get('weighted_scores', {}).items()
            }
            
            cluster_scores = {
                k: self._parse_decimal(v) 
                for k, v in raw_scoring_data.get('cluster_scores', {}).items()
            }
            
            confidence_scores = {
                k: self._parse_decimal(v) 
                for k, v in raw_scoring_data.get('confidence_scores', {}).items()
            }
            
            # Extract other fields
            risk_factors = raw_scoring_data.get('risk_factors', [])
            metadata = raw_scoring_data.get('metadata', {})
            computed_at = self._parse_datetime(raw_scoring_data.get('computed_at', datetime.now()))
            
            return ScoringMetrics(
                raw_scores=raw_scores,
                weighted_scores=weighted_scores,
                cluster_scores=cluster_scores,
                risk_factors=risk_factors,
                confidence_scores=confidence_scores,
                metadata=metadata,
                computed_at=computed_at
            )
            
        except Exception as e:
            raise ValidationError(f"Failed to create scoring metrics: {str(e)}") from e

    def _create_biomarker_panel(self, raw_panel_data: Dict[str, Any]) -> BiomarkerPanel:
        """
        Create a validated BiomarkerPanel from raw panel data.
        
        Args:
            raw_panel_data: Raw panel data dictionary
            
        Returns:
            Validated BiomarkerPanel object
            
        Raises:
            ValidationError: If panel data validation fails
        """
        try:
            # Extract panel metadata
            panel_name = raw_panel_data.get('name') or raw_panel_data.get('panel_name', 'Unknown Panel')
            panel_type = raw_panel_data.get('panel_type', 'custom')
            collected_at = self._parse_datetime(raw_panel_data.get('collected_at', datetime.now()))
            laboratory = raw_panel_data.get('laboratory')
            notes = raw_panel_data.get('notes')
            
            # Extract and validate biomarkers
            raw_biomarkers = raw_panel_data.get('biomarkers', {})
            if not raw_biomarkers:
                raise ValidationError("Panel must contain at least one biomarker")
            
            biomarkers = {}
            for name, raw_biomarker in raw_biomarkers.items():
                try:
                    biomarker = self._create_biomarker_context(name, raw_biomarker)
                    biomarkers[name.lower()] = biomarker
                except Exception as e:
                    if self.strict_validation:
                        # In strict mode, re-raise the exception to fail panel creation
                        self._log(f"Strict validation: failing on invalid biomarker '{name}': {str(e)}", "ERROR")
                        raise ValidationError(f"Strict validation failed for biomarker '{name}': {str(e)}") from e
                    else:
                        # In normal mode, log warning and continue
                        self._log(f"Failed to create biomarker '{name}': {str(e)}", "WARNING")
                        continue
            
            if not biomarkers:
                raise ValidationError("No valid biomarkers found in panel data")
            
            panel = BiomarkerPanel(
                name=panel_name,
                biomarkers=biomarkers,
                collected_at=collected_at,
                laboratory=laboratory,
                panel_type=panel_type,
                notes=notes
            )
            
            self._log(f"[TRACE] Created biomarker panel: {panel_name}")
            return panel
            
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Failed to create biomarker panel: {str(e)}") from e

    def _validate_reference_range(self, reference_range: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and normalize reference range data.
        
        Args:
            reference_range: Raw reference range data
            
        Returns:
            Validated reference range data
            
        Raises:
            ValidationError: If reference range validation fails
        """
        if not isinstance(reference_range, dict):
            raise ValidationError("Reference range must be a dictionary")
        
        required_keys = {'min', 'max', 'interpretation'}
        if not all(key in reference_range for key in required_keys):
            raise ValidationError("Reference range must contain 'min', 'max', and 'interpretation' keys")
        
        try:
            min_val = self._parse_decimal(reference_range['min'])
            max_val = self._parse_decimal(reference_range['max'])
            
            if min_val >= max_val:
                raise ValidationError("Reference range min must be less than max")
            
            return {
                'min': min_val,
                'max': max_val,
                'interpretation': str(reference_range['interpretation'])
            }
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Invalid reference range: {str(e)}") from e


    def _generate_analysis_id(self) -> str:
        """
        Generate a unique analysis ID.
        
        Returns:
            Unique analysis identifier
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        return f"analysis_{timestamp}_{unique_id}"
    
    def validate_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate payload without creating objects.
        
        This method performs validation on raw data to check for issues
        before attempting to create AnalysisContext objects.
        
        Args:
            payload: Raw payload data
            
        Returns:
            Dictionary with validation results and any issues found
        """
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'biomarker_issues': [],
            'user_issues': []
        }
        
        try:
            # Validate payload structure
            if not isinstance(payload, dict):
                validation_result['valid'] = False
                validation_result['errors'].append("Payload must be a dictionary")
                return validation_result
            
            # Validate biomarkers section
            raw_biomarkers = payload.get('biomarkers', {})
            if not raw_biomarkers:
                validation_result['valid'] = False
                validation_result['errors'].append("Payload must contain 'biomarkers' section")
            else:
                for name, biomarker_data in raw_biomarkers.items():
                    try:
                        self._create_biomarker_context(name, biomarker_data)
                    except Exception as e:
                        validation_result['biomarker_issues'].append(f"Biomarker '{name}': {str(e)}")
            
            # Validate user section
            raw_user_data = payload.get('user', {})
            if not raw_user_data:
                validation_result['valid'] = False
                validation_result['errors'].append("Payload must contain 'user' section")
            else:
                try:
                    self._create_user_context(raw_user_data)
                except Exception as e:
                    validation_result['user_issues'].append(str(e))
            
            # Check for critical issues
            if validation_result['biomarker_issues'] or validation_result['user_issues']:
                validation_result['valid'] = False
                validation_result['errors'].extend(validation_result['biomarker_issues'])
                validation_result['errors'].extend(validation_result['user_issues'])
            
        except Exception as e:
            validation_result['valid'] = False
            validation_result['errors'].append(f"Validation failed: {str(e)}")
        
        return validation_result
