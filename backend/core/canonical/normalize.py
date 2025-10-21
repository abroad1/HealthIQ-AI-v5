"""
Biomarker normalization - maps aliases to canonical names and builds BiomarkerPanel.
"""

from typing import Dict, Any, List, Optional, Tuple
from core.canonical.resolver import CanonicalResolver
from core.canonical.alias_registry_service import AliasRegistryService
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
        self.alias_service = alias_service or AliasRegistryService()
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
                
                # Handle dict format like {"value": 95, "unit": "mg/dL"}
                if isinstance(value, dict) and "value" in value:
                    numeric_value = value["value"]
                    if "unit" in value:
                        unit = value["unit"]
                
                # Create BiomarkerValue with canonical name
                normalized_values[canonical_key] = BiomarkerValue(
                    name=canonical_key,
                    value=numeric_value,
                    unit=unit
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
    
    Args:
        raw_biomarkers: Raw biomarker data with potential aliases
        
    Returns:
        Dict with canonical biomarker names as keys
    """
    # Skip re-normalizing already flagged biomarkers
    if any(key.startswith("unmapped_") for key in raw_biomarkers.keys()):
        return raw_biomarkers
    
    normalizer = BiomarkerNormalizer()
    panel, _ = normalizer.normalize_biomarkers(raw_biomarkers)
    return {name: value.value for name, value in panel.biomarkers.items()}
