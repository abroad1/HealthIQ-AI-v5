"""
Biomarker Alias Registry - v4 compatibility layer for v5 normalizer.
Ports v4's comprehensive alias resolution logic into v5 architecture.
"""

import os
import yaml
from typing import Dict, List, Optional, Tuple


class BiomarkerAliasResolver:
    """
    Biomarker alias resolver with SSOT alias mapping.
    Provides case-insensitive matching capabilities.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the alias resolver.
        
        Args:
            config_path: Path to biomarkers config YAML file
        """
        if config_path is None:
            # Default to SSOT alias registry
            config_path = os.path.join(
                os.path.dirname(__file__), 
                "..", "..", "ssot", "biomarker_alias_registry.yaml"
            )
        
        self.config_path = config_path
        self._alias_to_canonical: Optional[Dict[str, str]] = None
        self._canonical_biomarkers: Optional[List[str]] = None
        self._loaded = False
    
    def _load_alias_registry(self) -> Dict[str, any]:
        """Load SSOT alias registry from YAML file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Warning: SSOT alias registry not found at {self.config_path}")
            return {}
        except yaml.YAMLError as e:
            print(f"Error parsing SSOT alias registry: {e}")
            return {}
    
    def _build_alias_mapping(self) -> Dict[str, str]:
        """
        Build comprehensive alias mapping using v4 alias registry as primary source.
        Falls back to biomarkers config if v4 registry is not available.
        """
        if self._alias_to_canonical is not None:
            return self._alias_to_canonical
        
        alias_mapping = {}
        
        ssot_registry = self._load_alias_registry()
        if ssot_registry:
            print("Using SSOT alias registry for comprehensive alias mapping")
            for canonical_id, definition in ssot_registry.items():
                if isinstance(definition, dict) and 'aliases' in definition:
                    # Map canonical name to itself
                    alias_mapping[canonical_id.lower()] = canonical_id
                    alias_mapping[canonical_id.upper()] = canonical_id
                    
                    # Map all aliases to canonical name
                    for alias in definition['aliases']:
                        alias_mapping[alias.lower()] = canonical_id
                        alias_mapping[alias.upper()] = canonical_id
                        # Handle variations with spaces, hyphens, underscores
                        normalized = alias.lower().replace(' ', '_').replace('-', '_')
                        alias_mapping[normalized] = canonical_id
        
        # Add common medical abbreviations and variations
        self._add_common_aliases(alias_mapping)
        
        self._alias_to_canonical = alias_mapping
        self._loaded = True
        return alias_mapping
    
    def _generate_variations(self, canonical_name: str, display_name: str) -> List[str]:
        """Generate common variations of biomarker names."""
        variations = []
        
        # Add canonical name variations
        variations.append(canonical_name)
        variations.append(canonical_name.replace('_', ''))
        variations.append(canonical_name.replace('_', ' '))
        variations.append(canonical_name.replace('_', '-'))
        
        # Add display name variations
        if display_name:
            variations.append(display_name)
            variations.append(display_name.replace(' ', ''))
            variations.append(display_name.replace(' ', '_'))
            variations.append(display_name.replace(' ', '-'))
            variations.append(display_name.replace('-', '_'))
            variations.append(display_name.replace('-', ' '))
        
        return variations
    
    def _add_common_aliases(self, alias_mapping: Dict[str, str]):
        """Add common medical abbreviations and aliases."""
        common_aliases = {
            # Cardiovascular - canonical: ldl_cholesterol, hdl_cholesterol (aligns with clustering, insights, SSOT)
            'hdl': 'hdl_cholesterol',
            'hdl_chol': 'hdl_cholesterol',
            'hdl_cholesterol': 'hdl_cholesterol',
            'good_cholesterol': 'hdl_cholesterol',
            'ldl': 'ldl_cholesterol',
            'ldl_chol': 'ldl_cholesterol',
            'ldl_cholesterol': 'ldl_cholesterol',
            'bad_cholesterol': 'ldl_cholesterol',
            'total_chol': 'total_cholesterol',
            'cholesterol': 'total_cholesterol',
            'trig': 'triglycerides',
            'triglyceride': 'triglycerides',
            
            # Metabolic
            'glucose': 'glucose',
            'blood_sugar': 'glucose',
            'blood_glucose': 'glucose',
            'sugar': 'glucose',
            'hba1c': 'hba1c',
            'a1c': 'hba1c',
            'hemoglobin_a1c': 'hba1c',
            'glycated_hemoglobin': 'hba1c',
            'insulin': 'insulin',
            'insulin_level': 'insulin',
            'serum_insulin': 'insulin',
            
            # Kidney
            'creat': 'creatinine',
            'creatinine': 'creatinine',
            'serum_creatinine': 'creatinine',
            'bun': 'bun',
            'blood_urea_nitrogen': 'bun',
            'urea_nitrogen': 'bun',
            
            # Liver
            'alt': 'alt',
            'alanine_aminotransferase': 'alt',
            'sgot': 'alt',
            'ast': 'ast',
            'aspartate_aminotransferase': 'ast',
            'sgpt': 'ast',
            
            # Inflammatory
            'crp': 'crp',
            'c_reactive_protein': 'crp',
            'hs_crp': 'crp',
            'high_sensitivity_crp': 'crp',
            
            # CBC
            'hgb': 'hemoglobin',
            'hb': 'hemoglobin',
            'hemoglobin': 'hemoglobin',
            'hct': 'hematocrit',
            'pcv': 'hematocrit',
            'hematocrit': 'hematocrit',
            'wbc': 'white_blood_cells',
            'leukocytes': 'white_blood_cells',
            'white_blood_cells': 'white_blood_cells',
            'plt': 'platelets',
            'platelet_count': 'platelets',
            'platelets': 'platelets',
        }
        
        for alias, canonical in common_aliases.items():
            alias_mapping[alias.lower()] = canonical
            alias_mapping[alias.upper()] = canonical
    
    def resolve_to_canonical(self, alias: str) -> Optional[str]:
        """
        Resolve an alias to its canonical name with deterministic matching.
        
        Args:
            alias: Alias to resolve
            
        Returns:
            Canonical name if found, None otherwise
        """
        if not self._loaded:
            self._build_alias_mapping()
        
        # Direct lookup (case-insensitive)
        canonical = self._alias_to_canonical.get(alias.lower())
        if canonical:
            return canonical
        
        return None
    
    def get_canonical_biomarkers(self) -> List[str]:
        """Get list of all canonical biomarker names."""
        if not self._loaded:
            self._build_alias_mapping()
        
        if self._canonical_biomarkers is None:
            # Extract unique canonical names from alias mapping
            canonical_set = set(self._alias_to_canonical.values())
            self._canonical_biomarkers = sorted(list(canonical_set))
        
        return self._canonical_biomarkers
    
    def get_aliases_for_canonical(self, canonical_name: str) -> List[str]:
        """Get all aliases for a canonical biomarker name."""
        if not self._loaded:
            self._build_alias_mapping()
        
        aliases = []
        for alias, canonical in self._alias_to_canonical.items():
            if canonical == canonical_name:
                aliases.append(alias)
        
        return aliases
    
    def is_canonical(self, name: str) -> bool:
        """Check if a name is a canonical biomarker name."""
        if not self._loaded:
            self._build_alias_mapping()
        
        return name in self.get_canonical_biomarkers()
    
    def get_alias_count(self) -> int:
        """Get total number of aliases loaded."""
        if not self._loaded:
            self._build_alias_mapping()
        
        return len(self._alias_to_canonical)
    
    def get_canonical_count(self) -> int:
        """Get total number of canonical biomarkers."""
        return len(self.get_canonical_biomarkers())


# Convenience function for backward compatibility
def resolve_biomarker_alias(alias: str) -> Optional[str]:
    """Resolve a biomarker alias to its canonical name."""
    resolver = BiomarkerAliasResolver()
    return resolver.resolve_to_canonical(alias)
