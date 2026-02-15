"""
Biomarker normalization - maps aliases to canonical names and builds BiomarkerPanel.
"""

from typing import Dict, Any, List, Optional, Tuple
from core.canonical.resolver import CanonicalResolver
from core.canonical.alias_registry_service import AliasRegistryService, get_alias_registry_service
from core.models.biomarker import BiomarkerPanel, BiomarkerValue


class BiomarkerNormalizer:
    """Normalizes biomarker data by mapping aliases to canonical names."""
    
    def __init__(self, resolver: Optional[CanonicalResolver] = None, alias_service: Optional[AliasRegistryService] = None):
        """
        Initialize the normalizer.
        
        Args:
            resolver: CanonicalResolver instance, creates new one if None
            alias_service: AliasRegistryService instance, creates new one if None
        """
        self.resolver = resolver or CanonicalResolver()
        self.alias_service = alias_service or get_alias_registry_service()
        self._alias_to_canonical: Optional[Dict[str, str]] = None
    
    def _build_alias_mapping(self) -> Dict[str, str]:
        """
        Build mapping from aliases to canonical names using v4 alias service.
        
        Returns:
            Dict mapping aliases to canonical biomarker names
        """
        if self._alias_to_canonical is not None:
            return self._alias_to_canonical
        
        # Use v4 alias service for comprehensive alias mapping
        self._alias_to_canonical = self.alias_service._build_alias_mapping()
        return self._alias_to_canonical
    
    def normalize_biomarkers(self, raw_biomarkers: Dict[str, Any]) -> Tuple[BiomarkerPanel, List[str]]:
        """
        Normalize raw biomarker data to canonical form using v4 alias service.
        
        Args:
            raw_biomarkers: Raw biomarker data with potential aliases
            
        Returns:
            Tuple of (normalized BiomarkerPanel, list of unmapped keys)
        """
        normalized_values = {}
        unmapped_keys = []
        
        for key, value in raw_biomarkers.items():
            # Skip re-normalizing already flagged biomarkers
            if key.startswith("unmapped_"):
                print(f"[WARN] Skipping already-flagged unmapped key: '{key}'")
                normalized_values[key] = BiomarkerValue(
                    name=key,
                    value=value,
                    unit=""
                )
                unmapped_keys.append(key)
                continue
            
            # Use v4 alias service for comprehensive resolution
            canonical_key = self.alias_service.resolve(key)
            if canonical_key.startswith("unmapped_"):
                # Keep unmapped biomarkers but tag them as "unmapped"
                unmapped_keys.append(key)
                # Still include them in the panel for downstream processing
                normalized_values[canonical_key] = BiomarkerValue(
                    name=key,
                    value=value,
                    unit=""
                )
            else:
                # Extract numeric value and unit from the biomarker data
                numeric_value = value
                unit = self._get_unit_for_biomarker(canonical_key)
                reference_range = None
                
                # Handle dict format like {"value": 95, "unit": "mg/dL", "reference_range": {...}}
                if isinstance(value, dict) and "value" in value:
                    numeric_value = value["value"]
                    if "unit" in value:
                        unit = value["unit"]
                    # Preserve reference_range if present
                    if "reference_range" in value:
                        ref_range = value["reference_range"]
                        if isinstance(ref_range, dict) and ref_range.get("min") is not None and ref_range.get("max") is not None:
                            reference_range = {
                                "min": float(ref_range.get("min")),
                                "max": float(ref_range.get("max")),
                                "unit": ref_range.get("unit", unit),
                                "source": ref_range.get("source", "lab")
                            }
                    # Also check for camelCase variant
                    elif "referenceRange" in value:
                        ref_range = value["referenceRange"]
                        if isinstance(ref_range, dict) and ref_range.get("min") is not None and ref_range.get("max") is not None:
                            reference_range = {
                                "min": float(ref_range.get("min")),
                                "max": float(ref_range.get("max")),
                                "unit": ref_range.get("unit", unit),
                                "source": ref_range.get("source", "lab")
                            }
                
                # Build BiomarkerValue; pass unit audit fields if present (from apply_unit_normalisation)
                extra = {}
                if isinstance(value, dict):
                    for k in ("original_unit", "original_value", "unit_normalised", "unit_source",
                              "confidence_downgrade_unit_assumed", "reference_unit_assumed"):
                        if k in value:
                            extra[k] = value[k]

                if canonical_key in normalized_values and key != canonical_key:
                    unmapped_key = f"unmapped_{key}"
                    unmapped_keys.append(key)
                    print(
                        f"[WARN] Collision detected for '{canonical_key}' from raw key '{key}'. "
                        f"Preserving existing value and storing '{unmapped_key}' to protect data integrity."
                    )
                    normalized_values[unmapped_key] = BiomarkerValue(
                        name=key,
                        value=numeric_value,
                        unit=unit,
                        reference_range=reference_range,
                        **extra
                    )
                else:
                    normalized_values[canonical_key] = BiomarkerValue(
                        name=canonical_key,
                        value=numeric_value,
                        unit=unit,
                        reference_range=reference_range,
                        **extra
                    )
        
        # Create BiomarkerPanel with normalized values
        panel = BiomarkerPanel(
            biomarkers=normalized_values,
            source="normalized",
            version="1.0"
        )
        
        return panel, unmapped_keys
    
    def _get_unit_for_biomarker(self, canonical_name: str) -> str:
        """
        Get the unit for a canonical biomarker name.
        
        Args:
            canonical_name: Canonical biomarker name
            
        Returns:
            Unit string for the biomarker
        """
        definition = self.resolver.get_biomarker_definition(canonical_name)
        return definition.unit if definition else ""
    
    def validate_canonical_only(self, biomarkers: Dict[str, Any]) -> List[str]:
        """
        Validate that all biomarker keys are canonical (no aliases).
        
        Args:
            biomarkers: Biomarker data to validate
            
        Returns:
            List of non-canonical keys found
        """
        alias_mapping = self._build_alias_mapping()
        non_canonical = []
        
        for key in biomarkers.keys():
            canonical_key = alias_mapping.get(key.lower())
            if canonical_key != key:  # Key is not canonical
                non_canonical.append(key)
        
        return non_canonical
    
    def get_canonical_biomarkers(self) -> List[str]:
        """
        Get list of all canonical biomarker names using v4 alias service.
        
        Returns:
            List of canonical biomarker names
        """
        return self.alias_service.get_canonical_biomarkers()


def normalize_panel(raw_biomarkers: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize raw biomarker data to canonical form.
    
    WARNING: This function returns only {name: value} pairs, losing metadata.
    For routes that need reference_range, use normalize_biomarkers() directly.
    
    Args:
        raw_biomarkers: Raw biomarker data with potential aliases
        
    Returns:
        Dict with canonical biomarker names as keys and numeric values only
    """
    # Skip re-normalizing already flagged biomarkers
    if any(key.startswith("unmapped_") for key in raw_biomarkers.keys()):
        return raw_biomarkers
    
    normalizer = BiomarkerNormalizer()
    panel, _ = normalizer.normalize_biomarkers(raw_biomarkers)
    return {name: value.value for name, value in panel.biomarkers.items()}


def normalize_biomarkers_with_metadata(raw_biomarkers: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize raw biomarker data to canonical form, preserving all metadata including reference_range.
    
    Args:
        raw_biomarkers: Raw biomarker data with potential aliases
        
    Returns:
        Dict with canonical biomarker names as keys, containing value, unit, and reference_range
    """
    normalizer = BiomarkerNormalizer()
    panel, _ = normalizer.normalize_biomarkers(raw_biomarkers)
    
    # Convert BiomarkerPanel to dict format preserving all metadata
    result = {}
    for name, biomarker_value in panel.biomarkers.items():
        result[name] = {
            "value": biomarker_value.value,
            "unit": biomarker_value.unit,
            "reference_range": biomarker_value.reference_range
        }
        if biomarker_value.timestamp:
            result[name]["timestamp"] = biomarker_value.timestamp
    
    return result
