"""
Alias Registry Service - v4 integration for v5 canonicalization.

This service provides a clean interface to the v4 alias registry system,
integrating it seamlessly into the v5 architecture while maintaining
backward compatibility and performance.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from difflib import get_close_matches


class AliasRegistryService:
    """
    Service for resolving biomarker aliases to canonical names using v4 registry.
    
    Provides case-insensitive lookups, fuzzy matching, and comprehensive
    alias resolution identical to v4 behaviour.
    """
    
    def __init__(self, use_v4_registry: bool = True):
        """
        Initialize the alias registry service.
        
        Args:
            use_v4_registry: Whether to use v4 registry (True) or fallback to v5 config
        """
        self.use_v4_registry = use_v4_registry
        self._alias_to_canonical: Optional[Dict[str, str]] = None
        self._canonical_to_aliases: Optional[Dict[str, List[str]]] = None
        self._loaded = False
        
        # Paths to registry files
        self.v4_registry_path = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "v4_reference", "biomarker_alias_registry.yaml"
        )
        self.v5_config_path = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "v4_reference", "biomarkers_config.yaml"
        )
    
    def _load_v4_registry(self) -> Dict[str, Any]:
        """Load the v4 alias registry from YAML file."""
        print(f"[TRACE] [AliasRegistryService] Loading v4 registry from: {self.v4_registry_path}")
        try:
            with open(self.v4_registry_path, 'r', encoding='utf-8') as f:
                registry = yaml.safe_load(f)
                print(f"[TRACE] [AliasRegistryService] Loaded {len(registry)} entries from v4 registry")
                return registry
        except FileNotFoundError:
            print(f"[WARN] v4 alias registry not found at {self.v4_registry_path}")
            return {}
        except yaml.YAMLError as e:
            print(f"[ERROR] Error parsing v4 alias registry: {e}")
            return {}
    
    def _load_v5_config(self) -> Dict[str, Any]:
        """Load the v5 biomarkers config as fallback."""
        try:
            with open(self.v5_config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Warning: v5 biomarkers config not found at {self.v5_config_path}")
            return {}
        except yaml.YAMLError as e:
            print(f"Error parsing v5 biomarkers config: {e}")
            return {}
    
    def _load_ssot_biomarkers(self) -> Dict[str, Any]:
        """Load biomarkers from SSOT (Single Source of Truth)."""
        ssot_path = Path(__file__).parent.parent.parent / "ssot" / "biomarkers.yaml"
        try:
            with open(ssot_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                return data.get('biomarkers', {})
        except FileNotFoundError:
            print(f"[WARN] SSOT biomarkers file not found at {ssot_path}")
            return {}
        except yaml.YAMLError as e:
            print(f"[ERROR] Error parsing SSOT biomarkers: {e}")
            return {}
    
    def _build_alias_mapping(self) -> Dict[str, str]:
        """
        Build comprehensive alias mapping using v4 registry as primary source.
        
        Returns:
            Dict mapping aliases to canonical biomarker names
        """
        if self._alias_to_canonical is not None:
            return self._alias_to_canonical
        
        alias_mapping = {}
        
        if self.use_v4_registry:
            # Load v4 alias registry (most comprehensive)
            v4_registry = self._load_v4_registry()
            if v4_registry:
                print("[TRACE] Using v4 alias registry for comprehensive alias mapping")
                for key, definition in v4_registry.items():
                    if isinstance(definition, dict) and 'aliases' in definition:
                        # Use canonical_id if specified, otherwise use the key
                        canonical_id = definition.get('canonical_id', key)
                        
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
                            # Handle parentheses variations: create both (a) and _(a) versions
                            if '(' in normalized and ')' in normalized:
                                # Create version with underscore before parentheses: (a) -> _(a)
                                parens_with_underscore = normalized.replace('(', '_(').replace(')', '_)')
                                if parens_with_underscore != normalized:
                                    alias_mapping[parens_with_underscore] = canonical_id
                                # Also ensure we have the version without underscore: _(a) -> (a) if needed
                                # (This handles cases where alias already has _(a) format)
                                if '_(' in normalized:
                                    parens_without_underscore = normalized.replace('_(', '(').replace('_)', ')')
                                    if parens_without_underscore != normalized:
                                        alias_mapping[parens_without_underscore] = canonical_id
                            # Handle common medical abbreviations
                            if ' ' in alias:
                                abbrev = ''.join(word[0] for word in alias.split() if word)
                                alias_mapping[abbrev.lower()] = canonical_id
                                alias_mapping[abbrev.upper()] = canonical_id
            else:
                print("[WARN] v4 registry not available, falling back to v5 config")
                self.use_v4_registry = False
        
        # Load SSOT aliases to supplement v4 registry (or as primary source if v4 unavailable)
        ssot_biomarkers = self._load_ssot_biomarkers()
        if ssot_biomarkers:
            print("[TRACE] Loading aliases from SSOT biomarkers.yaml")
            for canonical_name, definition in ssot_biomarkers.items():
                if isinstance(definition, dict) and 'aliases' in definition:
                    # Map canonical name to itself
                    alias_mapping[canonical_name.lower()] = canonical_name
                    alias_mapping[canonical_name.upper()] = canonical_name
                    
                    # Map all aliases to canonical name
                    for alias in definition.get('aliases', []):
                        # Direct lowercase/uppercase mappings
                        alias_mapping[alias.lower()] = canonical_name
                        alias_mapping[alias.upper()] = canonical_name
                        # Handle variations with spaces, hyphens, underscores (but preserve parentheses)
                        normalized = alias.lower().replace(' ', '_').replace('-', '_')
                        alias_mapping[normalized] = canonical_name
                        # Handle parentheses variations: create both (a) and _(a) versions
                        if '(' in normalized and ')' in normalized:
                            # Create version with underscore before parentheses: (a) -> _(a)
                            parens_with_underscore = normalized.replace('(', '_(').replace(')', '_)')
                            if parens_with_underscore != normalized:
                                alias_mapping[parens_with_underscore] = canonical_name
                            # Also ensure we have the version without underscore: _(a) -> (a) if needed
                            if '_(' in normalized:
                                parens_without_underscore = normalized.replace('_(', '(').replace('_)', ')')
                                if parens_without_underscore != normalized:
                                    alias_mapping[parens_without_underscore] = canonical_name
        
        if not self.use_v4_registry:
            # Fallback to v5 config
            print("[TRACE] Using v5 biomarkers config as fallback for alias mapping")
            config = self._load_v5_config()
            raw_biomarkers = config.get('raw_biomarkers', {})
            derived_biomarkers = config.get('derived_biomarkers', {})
            
            # Process raw biomarkers
            for biomarker_id, definition in raw_biomarkers.items():
                canonical_name = biomarker_id
                alias_mapping[canonical_name.lower()] = canonical_name
                alias_mapping[canonical_name.upper()] = canonical_name
                
                # Map display name variations
                display_name = definition.get('display_name', '')
                if display_name:
                    alias_mapping[display_name.lower()] = canonical_name
                    alias_mapping[display_name.upper()] = canonical_name
                    normalized_display = display_name.lower().replace(' ', '_').replace('-', '_')
                    alias_mapping[normalized_display] = canonical_name
            
            # Process derived biomarkers
            for biomarker_id, definition in derived_biomarkers.items():
                canonical_name = biomarker_id
                alias_mapping[canonical_name.lower()] = canonical_name
                alias_mapping[canonical_name.upper()] = canonical_name
                
                display_name = definition.get('name', '')
                if display_name:
                    alias_mapping[display_name.lower()] = canonical_name
                    alias_mapping[display_name.upper()] = canonical_name
        
        # Add common medical abbreviations and variations
        self._add_common_aliases(alias_mapping)
        
        self._alias_to_canonical = alias_mapping
        self._loaded = True
        
        print(f"[TRACE] [AliasRegistryService] Registry building complete: {len(alias_mapping)} aliases mapped")
        # Show sample of mappings for debugging
        sample_keys = list(alias_mapping.keys())[:10]
        print(f"[TRACE] [AliasRegistryService] Sample mappings: {sample_keys}")
        return alias_mapping
    
    def _add_common_aliases(self, alias_mapping: Dict[str, str]):
        """Add common medical abbreviations and aliases."""
        common_aliases = {
            # Cardiovascular
            'hdl': 'hdl',
            'hdl_chol': 'hdl',
            'hdl_cholesterol': 'hdl',
            'good_cholesterol': 'hdl',
            'ldl': 'ldl',
            'ldl_chol': 'ldl',
            'ldl_cholesterol': 'ldl',
            'bad_cholesterol': 'ldl',
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

    def _strip_specimen_suffix(self, name: str) -> str:
        """Strip trailing specimen suffixes like _(venous), _(serum), etc."""
        return re.sub(r"(?:_?\(?(venous|serum|plasma|urine|blood)\)?)$", "", name)

    def _normalize_input_name(self, name: str) -> str:
        """Normalize input name for matching without altering core analyte tokens."""
        normalized = (name or "").strip().lower()
        normalized = re.sub(r"[-/\\s]+", "_", normalized)
        normalized = re.sub(r"_+", "_", normalized).strip("_")
        normalized = self._strip_specimen_suffix(normalized).strip("_")
        return normalized

    def _tokenize_analyte(self, name: str) -> set:
        """Tokenize analyte name for fuzzy-match guardrails."""
        stopwords = {
            "calculation", "calc", "ratio", "total", "free",
            "venous", "serum", "plasma", "urine", "blood"
        }
        cleaned = re.sub(r"[()]", "", name.lower())
        tokens = {t for t in cleaned.split("_") if t}
        return {t for t in tokens if t not in stopwords}
    
    def resolve(self, name: str) -> str:
        """
        Resolve an alias to its canonical name with fuzzy matching.
        
        Args:
            name: Alias to resolve
            
        Returns:
            Canonical name if found, "unmapped_{name}" if not found
        """
        # === BEGIN DEBUG LOGGING FOR ALIAS RESOLVER ===
        print(f"[TRACE] [AliasRegistryService] Resolving: '{name}'")
        # === END DEBUG LOGGING ===
        
        if not self._loaded:
            self._build_alias_mapping()

        original_raw = name or ""
        input_norm = self._normalize_input_name(original_raw)
        alias_lookup = {alias.lower(): canonical for alias, canonical in self._alias_to_canonical.items()}

        # Direct lookup (case-insensitive) using normalized form first
        canonical = alias_lookup.get(input_norm)
        if canonical:
            print(f"[TRACE] [AliasRegistryService] Direct lookup found: '{canonical}'")
            return canonical

        # Fall back to raw lowercase lookup
        canonical = alias_lookup.get(original_raw.lower())
        if canonical:
            print(f"[TRACE] [AliasRegistryService] Direct lookup found: '{canonical}'")
            return canonical
        
        print(f"[TRACE] [AliasRegistryService] Direct lookup failed for: '{input_norm}'")
        
        # Fuzzy matching for close matches (guarded by analyte token overlap)
        all_aliases = list(alias_lookup.keys())
        input_tokens = self._tokenize_analyte(input_norm)
        close_matches = get_close_matches(
            input_norm,
            all_aliases, 
            n=2,
            cutoff=0.9
        )
        
        if close_matches:
            if len(close_matches) > 1 and close_matches[0] != close_matches[1]:
                print(f"[TRACE] [AliasRegistryService] Fuzzy match ambiguous: {close_matches}")
                return f"unmapped_{original_raw}"

            candidate = close_matches[0]
            candidate_tokens = self._tokenize_analyte(candidate)
            if input_tokens and candidate_tokens and input_tokens.isdisjoint(candidate_tokens):
                print(f"[TRACE] [AliasRegistryService] Fuzzy match blocked by token mismatch: '{candidate}'")
                return f"unmapped_{original_raw}"

            result = alias_lookup.get(candidate)
            if result:
                print(f"[TRACE] [AliasRegistryService] Fuzzy match found: '{candidate}' -> '{result}'")
                return result
        
        print(f"[TRACE] [AliasRegistryService] No match found, returning: 'unmapped_{original_raw}'")
        # Return unmapped key
        return f"unmapped_{original_raw}"
    
    def normalize_panel(self, panel: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize a biomarker panel to use canonical names.
        
        Args:
            panel: Raw biomarker panel with potential aliases
            
        Returns:
            Normalized panel with canonical names as keys
        """
        if not self._loaded:
            self._build_alias_mapping()
        
        normalized_panel = {}
        mapped_count = 0
        unmapped_count = 0
        
        for key, value in panel.items():
            canonical_key = self.resolve(key)
            
            if canonical_key.startswith("unmapped_"):
                unmapped_count += 1
                print(f"[WARN] Unmapped biomarker: {key} -> {canonical_key}")
            else:
                mapped_count += 1
            
            normalized_panel[canonical_key] = value
        
        print(f"[TRACE] Alias normalization used v4 registry: {mapped_count} mapped, {unmapped_count} unmapped")
        return normalized_panel
    
    def get_all_aliases(self) -> Dict[str, List[str]]:
        """
        Get all aliases grouped by canonical name.
        
        Returns:
            Dict mapping canonical names to lists of aliases
        """
        if not self._loaded:
            self._build_alias_mapping()
        
        if self._canonical_to_aliases is None:
            self._canonical_to_aliases = {}
            for alias, canonical in self._alias_to_canonical.items():
                if canonical not in self._canonical_to_aliases:
                    self._canonical_to_aliases[canonical] = []
                self._canonical_to_aliases[canonical].append(alias)
        
        return self._canonical_to_aliases
    
    def get_canonical_biomarkers(self) -> List[str]:
        """
        Get list of all canonical biomarker names.
        
        Returns:
            List of canonical biomarker names
        """
        if not self._loaded:
            self._build_alias_mapping()
        
        canonical_set = set(self._alias_to_canonical.values())
        return sorted(list(canonical_set))
    
    def is_canonical(self, name: str) -> bool:
        """
        Check if a name is a canonical biomarker name.
        
        Args:
            name: Name to check
            
        Returns:
            True if canonical, False otherwise
        """
        if not self._loaded:
            self._build_alias_mapping()
        
        return name in self.get_canonical_biomarkers()
    
    def get_alias_count(self) -> int:
        """
        Get total number of aliases loaded.
        
        Returns:
            Number of aliases
        """
        if not self._loaded:
            self._build_alias_mapping()
        
        return len(self._alias_to_canonical)
    
    def get_canonical_count(self) -> int:
        """
        Get total number of canonical biomarkers.
        
        Returns:
            Number of canonical biomarkers
        """
        return len(self.get_canonical_biomarkers())
