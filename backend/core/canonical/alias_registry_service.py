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
from typing import Dict, List, Optional, Any, Set
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

    def normalize_key(self, raw: str) -> str:
        """
        Normalize an input key for matching while preserving the raw key for output.
        """
        if raw is None:
            return ""
        key = str(raw).strip().lower()
        key = re.sub(r"[-/]", "_", key)
        key = re.sub(r"\s+", "_", key)
        key = re.sub(r"_+", "_", key)

        specimen_suffixes = [
            "venous",
            "serum",
            "plasma",
            "urine",
            "blood",
            "whole_blood",
            "capillary",
            "arterial",
        ]
        for suffix in specimen_suffixes:
            paren_suffix = f"_({suffix})"
            bare_suffix = f"_{suffix}"
            if key.endswith(paren_suffix):
                key = key[: -len(paren_suffix)]
                break
            if key.endswith(bare_suffix):
                key = key[: -len(bare_suffix)]
                break

        key = re.sub(r"_+", "_", key).strip("_")
        return key

    def analyte_tokens(self, name: str) -> Set[str]:
        if not name:
            return set()

        key = str(name).strip().lower()
        key = re.sub(r"[-/]", "_", key)
        key = re.sub(r"\s+", "_", key)
        key = re.sub(r"_+", "_", key).strip("_")

        remove_tokens = {
            "calculation",
            "calc",
            "ratio",
            "total",
            "free",
            "venous",
            "serum",
            "plasma",
            "urine",
            "blood",
            "whole",
            "whole_blood",
            "capillary",
            "arterial",
        }
        return {token for token in key.split("_") if token and token not in remove_tokens}
    
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

        raw_name = name
        normalized_input = self.normalize_key(name)
        if not normalized_input:
            print(f"[TRACE] [AliasRegistryService] Empty normalized input for: '{raw_name}'")
            return f"unmapped_{raw_name}"
        
        # Direct lookup (case-insensitive) on normalized input
        canonical = self._alias_to_canonical.get(normalized_input.lower())
        if canonical:
            print(f"[TRACE] [AliasRegistryService] Direct lookup found: '{canonical}'")
            return canonical
        
        print(f"[TRACE] [AliasRegistryService] Direct lookup failed for: '{normalized_input.lower()}'")

        # Exact match against canonical ids (if applicable)
        for canonical_id in set(self._alias_to_canonical.values()):
            if canonical_id.lower() == normalized_input.lower():
                print(f"[TRACE] [AliasRegistryService] Canonical id match found: '{canonical_id}'")
                return canonical_id
        
        # Fuzzy matching for close matches
        all_aliases = list({alias for alias in self._alias_to_canonical.keys() if alias == alias.lower()})
        input_tokens = self.analyte_tokens(normalized_input)
        if not input_tokens:
            print(f"[TRACE] [AliasRegistryService] Empty analyte tokens for: '{normalized_input}'")
            return f"unmapped_{raw_name}"

        close_matches = get_close_matches(
            normalized_input.lower(),
            all_aliases, 
            n=1, 
            cutoff=0.9
        )
        
        if close_matches:
            candidate = close_matches[0]
            candidate_tokens = self.analyte_tokens(candidate)
            if input_tokens.isdisjoint(candidate_tokens):
                print(f"[TRACE] [AliasRegistryService] Token gate blocked fuzzy match: '{normalized_input}' -> '{candidate}'")
                return f"unmapped_{raw_name}"

            result = self._alias_to_canonical[candidate]
            print(f"[TRACE] [AliasRegistryService] Fuzzy match found: '{candidate}' -> '{result}'")
            return result

        # Allow slightly lower cutoff only with strong analyte overlap
        strong_tokens = {
            "albumin",
            "creatine",
            "kinase",
            "glucose",
            "cholesterol",
            "triglycerides",
            "calcium",
            "sodium",
            "potassium",
            "hemoglobin",
            "thyroid",
        }
        relaxed_matches = get_close_matches(
            normalized_input.lower(),
            all_aliases,
            n=1,
            cutoff=0.85
        )
        if relaxed_matches:
            candidate = relaxed_matches[0]
            candidate_tokens = self.analyte_tokens(candidate)
            overlap = input_tokens.intersection(candidate_tokens)
            strong_overlap = overlap.intersection(strong_tokens)
            if not overlap:
                print(f"[TRACE] [AliasRegistryService] Token gate blocked relaxed fuzzy match: '{normalized_input}' -> '{candidate}'")
                return f"unmapped_{raw_name}"
            if not strong_overlap:
                print(f"[TRACE] [AliasRegistryService] Strong token gate blocked relaxed fuzzy match: '{normalized_input}' -> '{candidate}'")
                return f"unmapped_{raw_name}"

            result = self._alias_to_canonical[candidate]
            print(f"[TRACE] [AliasRegistryService] Relaxed fuzzy match found: '{candidate}' -> '{result}'")
            return result
        
        print(f"[TRACE] [AliasRegistryService] No match found, returning: 'unmapped_{raw_name}'")
        # Return unmapped key
        return f"unmapped_{raw_name}"
    
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
