"""
Biomarker normalization - maps aliases to canonical names and builds BiomarkerPanel.
"""

from typing import Dict, Any, List, Optional, Tuple
from core.canonical.resolver import CanonicalResolver
from core.models.biomarker import BiomarkerPanel, BiomarkerValue


class BiomarkerNormalizer:
    """Normalizes biomarker data by mapping aliases to canonical names."""
    
    def __init__(self, resolver: Optional[CanonicalResolver] = None):
        """
        Initialize the normalizer.
        
        Args:
            resolver: CanonicalResolver instance, creates new one if None
        """
        self.resolver = resolver or CanonicalResolver()
        self._alias_to_canonical: Optional[Dict[str, str]] = None
    
    def _build_alias_mapping(self) -> Dict[str, str]:
        """
        Build mapping from aliases to canonical names.
        
        Returns:
            Dict mapping aliases to canonical biomarker names
        """
        if self._alias_to_canonical is not None:
            return self._alias_to_canonical
        
        biomarkers = self.resolver.load_biomarkers()
        alias_mapping = {}
        
        for canonical_name, definition in biomarkers.items():
            # Map canonical name to itself
            alias_mapping[canonical_name.lower()] = canonical_name
            
            # Map all aliases to canonical name
            for alias in definition.aliases:
                alias_mapping[alias.lower()] = canonical_name
        
        self._alias_to_canonical = alias_mapping
        return alias_mapping
    
    def normalize_biomarkers(self, raw_biomarkers: Dict[str, Any]) -> Tuple[BiomarkerPanel, List[str]]:
        """
        Normalize raw biomarker data to canonical form.
        
        Args:
            raw_biomarkers: Raw biomarker data with potential aliases
            
        Returns:
            Tuple of (normalized BiomarkerPanel, list of unmapped keys)
        """
        alias_mapping = self._build_alias_mapping()
        normalized_values = {}
        unmapped_keys = []
        
        for key, value in raw_biomarkers.items():
            canonical_key = alias_mapping.get(key.lower())
            
            if canonical_key:
                # Create BiomarkerValue with canonical name
                normalized_values[canonical_key] = BiomarkerValue(
                    name=canonical_key,
                    value=value,
                    unit=self._get_unit_for_biomarker(canonical_key)
                )
            else:
                unmapped_keys.append(key)
        
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
        Get list of all canonical biomarker names.
        
        Returns:
            List of canonical biomarker names
        """
        biomarkers = self.resolver.load_biomarkers()
        return list(biomarkers.keys())


def normalize_panel(raw_biomarkers: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize raw biomarker data to canonical form.
    
    Args:
        raw_biomarkers: Raw biomarker data with potential aliases
        
    Returns:
        Dict with canonical biomarker names as keys
    """
    normalizer = BiomarkerNormalizer()
    panel, _ = normalizer.normalize_biomarkers(raw_biomarkers)
    return {name: value.value for name, value in panel.biomarkers.items()}
