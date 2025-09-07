"""
Canonical biomarker resolver - loads from Single Source of Truth (SSOT).
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional

from core.models.biomarker import BiomarkerDefinition


class CanonicalResolver:
    """Resolves canonical biomarker definitions from SSOT."""
    
    def __init__(self, ssot_path: Optional[Path] = None):
        """
        Initialize the resolver with SSOT path.
        
        Args:
            ssot_path: Path to SSOT directory, defaults to backend/ssot/
        """
        if ssot_path is None:
            ssot_path = Path(__file__).parent.parent.parent / "ssot"
        
        self.ssot_path = ssot_path
        self._biomarkers_cache: Optional[Dict[str, BiomarkerDefinition]] = None
        self._ranges_cache: Optional[Dict[str, Any]] = None
        self._units_cache: Optional[Dict[str, Any]] = None
    
    def load_biomarkers(self) -> Dict[str, BiomarkerDefinition]:
        """
        Load canonical biomarker definitions from SSOT.
        
        Returns:
            Dict mapping canonical biomarker names to definitions
        """
        if self._biomarkers_cache is not None:
            return self._biomarkers_cache
        
        biomarkers_file = self.ssot_path / "biomarkers.yaml"
        if not biomarkers_file.exists():
            raise FileNotFoundError(f"Biomarkers SSOT file not found: {biomarkers_file}")
        
        with open(biomarkers_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        biomarkers = {}
        for name, definition in data.get("biomarkers", {}).items():
            biomarkers[name] = BiomarkerDefinition(
                name=name,
                aliases=definition.get("aliases", []),
                unit=definition.get("unit", ""),
                description=definition.get("description", ""),
                category=definition.get("category", ""),
                data_type=definition.get("data_type", "numeric")
            )
        
        self._biomarkers_cache = biomarkers
        return biomarkers
    
    def load_ranges(self) -> Dict[str, Any]:
        """
        Load reference ranges from SSOT.
        
        Returns:
            Dict mapping biomarker names to reference ranges
        """
        if self._ranges_cache is not None:
            return self._ranges_cache
        
        ranges_file = self.ssot_path / "ranges.yaml"
        if not ranges_file.exists():
            raise FileNotFoundError(f"Ranges SSOT file not found: {ranges_file}")
        
        with open(ranges_file, 'r', encoding='utf-8') as f:
            self._ranges_cache = yaml.safe_load(f)
        
        return self._ranges_cache
    
    def load_units(self) -> Dict[str, Any]:
        """
        Load unit definitions from SSOT.
        
        Returns:
            Dict mapping unit names to definitions
        """
        if self._units_cache is not None:
            return self._units_cache
        
        units_file = self.ssot_path / "units.yaml"
        if not units_file.exists():
            raise FileNotFoundError(f"Units SSOT file not found: {units_file}")
        
        with open(units_file, 'r', encoding='utf-8') as f:
            self._units_cache = yaml.safe_load(f)
        
        return self._units_cache
    
    def get_biomarker_definition(self, name: str) -> Optional[BiomarkerDefinition]:
        """
        Get a specific biomarker definition by canonical name.
        
        Args:
            name: Canonical biomarker name
            
        Returns:
            BiomarkerDefinition or None if not found
        """
        biomarkers = self.load_biomarkers()
        return biomarkers.get(name)
    
    def clear_cache(self):
        """Clear all cached data."""
        self._biomarkers_cache = None
        self._ranges_cache = None
        self._units_cache = None
