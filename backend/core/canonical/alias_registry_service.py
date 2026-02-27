"""
Alias Registry Service - v4 integration for v5 canonicalization.

This service provides a clean interface to the v4 alias registry system,
integrating it seamlessly into the v5 architecture while maintaining
backward compatibility and performance.

Process-level singleton via get_alias_registry_service() ensures the registry
is built once and reused for all resolves within the process.
"""

import os
import re
import string
import threading
import yaml
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Any

# Lock for thread-safe first load
_load_lock = threading.Lock()


@lru_cache(maxsize=2)
def get_alias_registry_service(use_v4_registry: bool = True) -> "AliasRegistryService":
    """
    Get the process-level AliasRegistryService singleton.
    Registry is built once lazily on first use.
    """
    return AliasRegistryService(use_v4_registry=use_v4_registry)


class AliasCollisionError(ValueError):
    """Raised when a normalized alias key maps to multiple canonical IDs."""


class AliasRegistryService:
    """
    Service for resolving biomarker aliases to canonical names using v4 registry.
    
    Provides case-insensitive lookups and comprehensive
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
        
        # Paths to SSOT registry files
        self.ssot_alias_registry_path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "ssot", "biomarker_alias_registry.yaml"
        )
    
    def _load_alias_registry(self) -> Dict[str, Any]:
        """Load the SSOT alias registry from YAML file (called once per process)."""
        try:
            with open(self.ssot_alias_registry_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"[WARN] SSOT alias registry not found at {self.ssot_alias_registry_path}")
            return {}
        except yaml.YAMLError as e:
            print(f"[ERROR] Error parsing SSOT alias registry: {e}")
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
        Thread-safe; builds once per instance.
        
        Returns:
            Dict mapping aliases to canonical biomarker names
        """
        if self._alias_to_canonical is not None:
            return self._alias_to_canonical

        with _load_lock:
            if self._alias_to_canonical is not None:
                return self._alias_to_canonical
            alias_mapping = self._build_alias_mapping_impl()
            self._alias_to_canonical = alias_mapping
            self._loaded = True
            # Log once per process when registry is first built
            print(f"[TRACE] [AliasRegistryService] Registry built: {len(alias_mapping)} aliases mapped")
            return alias_mapping

    def _build_alias_mapping_impl(self) -> Dict[str, str]:
        """Internal implementation of alias mapping build (called under lock)."""
        alias_mapping: Dict[str, str] = {}
        alias_sources: Dict[str, set[str]] = {}

        def _insert_alias(alias_key: str, canonical_id: str, source_alias: Optional[str] = None) -> None:
            key = str(alias_key)
            source = str(source_alias if source_alias is not None else alias_key)
            existing = alias_mapping.get(key)
            if existing is None:
                alias_mapping[key] = canonical_id
                alias_sources[key] = {source}
                return
            alias_sources.setdefault(key, set()).add(source)
            if existing == canonical_id:
                return
            encountered = sorted({existing, canonical_id})
            sources = sorted(alias_sources.get(key, set()))
            raise AliasCollisionError(
                f"Alias collision for key '{key}': "
                f"canonical_ids={encountered}; source_aliases={sources}"
            )

        ssot_alias_registry = self._load_alias_registry()
        if ssot_alias_registry:
            for key, definition in ssot_alias_registry.items():
                if isinstance(definition, dict) and 'aliases' in definition:
                    # Use canonical_id if specified, otherwise use the key
                    canonical_id = definition.get('canonical_id', key)
                    
                    # Map canonical name to itself
                    _insert_alias(canonical_id.lower(), canonical_id, canonical_id)
                    _insert_alias(canonical_id.upper(), canonical_id, canonical_id)
                    
                    # Map all aliases to canonical name
                    for alias in definition['aliases']:
                        _insert_alias(alias.lower(), canonical_id, alias)
                        _insert_alias(alias.upper(), canonical_id, alias)
                        # Handle variations with spaces, hyphens, underscores
                        normalized = alias.lower().replace(' ', '_').replace('-', '_')
                        _insert_alias(normalized, canonical_id, alias)
                        # Handle parentheses variations: create both (a) and _(a) versions
                        if '(' in normalized and ')' in normalized:
                            # Create version with underscore before parentheses: (a) -> _(a)
                            parens_with_underscore = normalized.replace('(', '_(').replace(')', '_)')
                            if parens_with_underscore != normalized:
                                _insert_alias(parens_with_underscore, canonical_id, alias)
                            # Also ensure we have the version without underscore: _(a) -> (a) if needed
                            # (This handles cases where alias already has _(a) format)
                            if '_(' in normalized:
                                parens_without_underscore = normalized.replace('_(', '(').replace('_)', ')')
                                if parens_without_underscore != normalized:
                                    _insert_alias(parens_without_underscore, canonical_id, alias)
        
        # Load SSOT aliases to supplement v4 registry (or as primary source if v4 unavailable)
        ssot_biomarkers = self._load_ssot_biomarkers()
        if ssot_biomarkers:
            for canonical_name, definition in ssot_biomarkers.items():
                if isinstance(definition, dict) and 'aliases' in definition:
                    # Map canonical name to itself
                    _insert_alias(canonical_name.lower(), canonical_name, canonical_name)
                    _insert_alias(canonical_name.upper(), canonical_name, canonical_name)
                    
                    # Map all aliases to canonical name
                    for alias in definition.get('aliases', []):
                        # Direct lowercase/uppercase mappings
                        _insert_alias(alias.lower(), canonical_name, alias)
                        _insert_alias(alias.upper(), canonical_name, alias)
                        # Handle variations with spaces, hyphens, underscores (but preserve parentheses)
                        normalized = alias.lower().replace(' ', '_').replace('-', '_')
                        _insert_alias(normalized, canonical_name, alias)
                        # Handle parentheses variations: create both (a) and _(a) versions
                        if '(' in normalized and ')' in normalized:
                            # Create version with underscore before parentheses: (a) -> _(a)
                            parens_with_underscore = normalized.replace('(', '_(').replace(')', '_)')
                            if parens_with_underscore != normalized:
                                _insert_alias(parens_with_underscore, canonical_name, alias)
                            # Also ensure we have the version without underscore: _(a) -> (a) if needed
                            if '_(' in normalized:
                                parens_without_underscore = normalized.replace('_(', '(').replace('_)', ')')
                                if parens_without_underscore != normalized:
                                    _insert_alias(parens_without_underscore, canonical_name, alias)
        
        # Add common medical abbreviations and variations
        self._add_common_aliases(alias_mapping, _insert_alias)
        return alias_mapping
    
    def _add_common_aliases(self, alias_mapping: Dict[str, str], insert_alias):
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
            
            # Liver
            'alt': 'alt',
            'alanine_aminotransferase': 'alt',
            'sgpt': 'alt',
            'ast': 'ast',
            'aspartate_aminotransferase': 'ast',
            'sgot': 'ast',
            
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
            insert_alias(alias.lower(), canonical, alias)
            insert_alias(alias.upper(), canonical, alias)
    
    @staticmethod
    def _strip_surrounding_punctuation(value: str) -> str:
        strip_chars = string.punctuation.replace("_", "")
        return value.strip(strip_chars)

    @staticmethod
    def _normalize_key(raw: str) -> str:
        normalized = (raw or "").strip().lower()
        normalized = re.sub(r"[-/\s]+", "_", normalized)
        normalized = re.sub(r"_+", "_", normalized)
        return normalized

    @staticmethod
    def _normalize_special_patterns(normalized: str) -> str:
        if normalized.endswith("_(a)"):
            return normalized[:-4] + "_a"
        return normalized

    @staticmethod
    def _strip_specimen_suffix(normalized: str) -> str:
        specimen_suffixes = [
            "venous",
            "serum",
            "plasma",
            "whole_blood",
            "urine",
            "csf",
        ]
        for suffix in specimen_suffixes:
            paren_suffix = f"_({suffix})"
            bare_suffix = f"_{suffix}"
            if normalized.endswith(paren_suffix):
                return normalized[: -len(paren_suffix)]
            if normalized.endswith(bare_suffix):
                return normalized[: -len(bare_suffix)]
        return normalized

    def resolve(self, name: str) -> str:
        """
        Resolve an alias to its canonical name with deterministic matching.
        
        Args:
            name: Alias to resolve
            
        Returns:
            Canonical name if found, "unmapped_{name}" if not found
        """
        if not self._loaded:
            self._build_alias_mapping()
        
        raw = name or ""
        base = self._normalize_special_patterns(self._normalize_key(raw))
        norm = self._strip_surrounding_punctuation(base)
        norm_stripped = self._strip_surrounding_punctuation(self._strip_specimen_suffix(base))

        # Direct lookup (case-insensitive)
        canonical = self._alias_to_canonical.get(raw.lower())
        if canonical:
            return canonical

        if norm:
            canonical = self._alias_to_canonical.get(norm)
            if canonical:
                return canonical

        if norm_stripped and norm_stripped != norm:
            canonical = self._alias_to_canonical.get(norm_stripped)
            if canonical:
                return canonical

        # Return unmapped key
        return f"unmapped_{raw}"
    
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
