"""
Biomarker Alias Resolution Utilities

This module provides functions to resolve biomarker aliases to their canonical IDs
using the central biomarker alias registry.
"""

import os
import yaml
from typing import Dict, List, Optional, Set, Any
from pathlib import Path


class BiomarkerAliasResolver:
    """
    Resolves biomarker aliases to canonical IDs using the central registry.
    """
    
    def __init__(self, registry_path: Optional[str] = None):
        """
        Initialize the resolver with the alias registry.
        
        Args:
            registry_path: Path to the biomarker alias registry YAML file.
                          If None, uses default location.
        """
        if registry_path is None:
            # Default to config directory
            config_dir = Path(__file__).parent.parent / "config"
            registry_path = config_dir / "biomarker_alias_registry.yaml"
        
        self.registry_path = Path(registry_path)
        self._registry = None
        self._alias_to_canonical = None
        self._canonical_ids = None
        
        # Performance enhancements
        self._resolution_cache = {}  # Memoization cache
        self._cache_hits = 0
        self._cache_misses = 0
        
        # Load the registry
        self._load_registry()
    
    def _load_registry(self):
        """Load the biomarker alias registry from YAML file."""
        try:
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                self._registry = yaml.safe_load(f)
            
            # Build reverse mapping from aliases to canonical IDs
            self._alias_to_canonical = {}
            self._canonical_ids = set()
            
            for canonical_id, entry in self._registry.items():
                if isinstance(entry, dict) and 'canonical_id' in entry:
                    # Use the canonical_id from the entry (in case it differs from the key)
                    actual_canonical_id = entry['canonical_id']
                    self._canonical_ids.add(actual_canonical_id)
                    
                    # Map the canonical ID to itself
                    self._alias_to_canonical[actual_canonical_id] = actual_canonical_id
                    
                    # Map all aliases to the canonical ID
                    aliases = entry.get('aliases', [])
                    for alias in aliases:
                        self._alias_to_canonical[alias.lower()] = actual_canonical_id
                        self._alias_to_canonical[alias] = actual_canonical_id
                        
        except FileNotFoundError:
            raise FileNotFoundError(f"Biomarker alias registry not found at {self.registry_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in biomarker alias registry: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading biomarker alias registry: {e}")
    
    def resolve_to_canonical(self, alias_name: str) -> str:
        """
        Resolve a biomarker alias to its canonical ID with caching.
        
        Args:
            alias_name: The alias name to resolve
            
        Returns:
            The canonical ID for the biomarker, or the original name if not found
        """
        if not alias_name:
            return alias_name
        
        # Check cache first
        if alias_name in self._resolution_cache:
            self._cache_hits += 1
            return self._resolution_cache[alias_name]
        
        self._cache_misses += 1
        
        # Try exact match first
        if alias_name in self._alias_to_canonical:
            result = self._alias_to_canonical[alias_name]
        else:
            # Try case-insensitive match
            alias_lower = alias_name.lower()
            if alias_lower in self._alias_to_canonical:
                result = self._alias_to_canonical[alias_lower]
            else:
                # If not found, return the original name
                result = alias_name
        
        # Cache the result
        self._resolution_cache[alias_name] = result
        return result
    
    def batch_resolve_to_canonical(self, alias_names: List[str]) -> Dict[str, str]:
        """
        Resolve multiple biomarker aliases to canonical IDs in batch.
        
        Args:
            alias_names: List of biomarker aliases to resolve
            
        Returns:
            Dictionary mapping original aliases to canonical IDs
        """
        results = {}
        for alias_name in alias_names:
            results[alias_name] = self.resolve_to_canonical(alias_name)
        return results
    
    def get_canonical_ids(self) -> Set[str]:
        """
        Get all canonical biomarker IDs.
        
        Returns:
            Set of all canonical biomarker IDs
        """
        return self._canonical_ids.copy()
    
    def get_all_canonical_ids(self) -> Set[str]:
        """
        Get all canonical biomarker IDs (alias for get_canonical_ids for consistency).
        
        Returns:
            Set of all canonical biomarker IDs
        """
        return self._canonical_ids.copy()
    
    def get_aliases_for_canonical(self, canonical_id: str) -> List[str]:
        """
        Get all aliases for a canonical biomarker ID.
        
        Args:
            canonical_id: The canonical biomarker ID
            
        Returns:
            List of aliases for the canonical ID
        """
        if canonical_id not in self._registry:
            return []
        
        entry = self._registry[canonical_id]
        if isinstance(entry, dict) and 'aliases' in entry:
            return entry['aliases']
        
        return []
    
    def is_canonical_id(self, biomarker_name: str) -> bool:
        """
        Check if a biomarker name is a canonical ID.
        
        Args:
            biomarker_name: The biomarker name to check
            
        Returns:
            True if the name is a canonical ID, False otherwise
        """
        return biomarker_name in self._canonical_ids
    
    def normalize_panel(self, panel: Dict[str, any]) -> Dict[str, any]:
        """
        Normalize a panel by resolving all biomarker keys to canonical IDs.
        
        Args:
            panel: Dictionary with biomarker names as keys
            
        Returns:
            New dictionary with canonical biomarker IDs as keys
        """
        normalized_panel = {}
        
        for alias_name, value in panel.items():
            canonical_id = self.resolve_to_canonical(alias_name)
            normalized_panel[canonical_id] = value
        
        return normalized_panel
    
    def validate_panel_aliases(self, panel: Dict[str, any]) -> Dict[str, List[str]]:
        """
        Validate a panel and return unknown aliases.
        
        Args:
            panel: Dictionary with biomarker names as keys
            
        Returns:
            Dictionary with 'unknown_aliases' and 'resolved_mappings' keys
        """
        unknown_aliases = []
        resolved_mappings = {}
        
        for alias_name in panel.keys():
            canonical_id = self.resolve_to_canonical(alias_name)
            resolved_mappings[alias_name] = canonical_id
            
            # If the resolved ID is the same as the original, it might be unknown
            if canonical_id == alias_name and not self.is_canonical_id(alias_name):
                unknown_aliases.append(alias_name)
        
        return {
            'unknown_aliases': unknown_aliases,
            'resolved_mappings': resolved_mappings
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get performance metrics for the resolver.
        
        Returns:
            Dictionary with cache hits, misses, and hit rate
        """
        total_requests = self._cache_hits + self._cache_misses
        hit_rate = (self._cache_hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'cache_hits': self._cache_hits,
            'cache_misses': self._cache_misses,
            'total_requests': total_requests,
            'hit_rate_percent': hit_rate,
            'cache_size': len(self._resolution_cache)
        }


# Global resolver instance
_resolver = None


def get_resolver() -> BiomarkerAliasResolver:
    """
    Get the global biomarker alias resolver instance.
    
    Returns:
        BiomarkerAliasResolver instance
    """
    global _resolver
    if _resolver is None:
        _resolver = BiomarkerAliasResolver()
    return _resolver


def resolve_to_canonical(alias_name: str) -> str:
    """
    Resolve a biomarker alias to its canonical ID.
    
    Args:
        alias_name: The alias name to resolve
        
    Returns:
        The canonical ID for the biomarker, or the original name if not found
    """
    return get_resolver().resolve_to_canonical(alias_name)


def normalize_panel(panel: Dict[str, any]) -> Dict[str, any]:
    """
    Normalize a panel by resolving all biomarker keys to canonical IDs.
    
    Args:
        panel: Dictionary with biomarker names as keys
        
    Returns:
        New dictionary with canonical biomarker IDs as keys
    """
    return get_resolver().normalize_panel(panel)


def validate_panel_aliases(panel: Dict[str, any]) -> Dict[str, List[str]]:
    """
    Validate a panel and return unknown aliases.
    
    Args:
        panel: Dictionary with biomarker names as keys
        
    Returns:
        Dictionary with 'unknown_aliases' and 'resolved_mappings' keys
    """
    return get_resolver().validate_panel_aliases(panel)


def is_canonical_id(biomarker_name: str) -> bool:
    """
    Check if a biomarker name is a canonical ID.
    
    Args:
        biomarker_name: The biomarker name to check
        
    Returns:
        True if the name is a canonical ID, False otherwise
    """
    return get_resolver().is_canonical_id(biomarker_name) 