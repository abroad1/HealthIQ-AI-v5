"""
Manifest service for managing insight configurations.
"""

import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

from core.insights.registry import insight_registry


@dataclass
class InsightConfig:
    """Configuration for a single insight in a manifest."""
    insight_id: str
    version: str
    enabled: bool
    weight: float = 1.0


@dataclass
class InsightManifest:
    """Complete insight manifest with metadata and configurations."""
    schema_version: str
    manifest_id: str
    name: str
    description: str
    created_by: str
    updated_by: str
    insights: List[InsightConfig]
    overrides: Optional[Dict[str, any]] = None


class ManifestService:
    """Service for loading and validating insight manifests."""
    
    def __init__(self, manifest_dir: str = "backend/data/insight_manifests"):
        self.manifest_dir = Path(manifest_dir)
        self._active_manifest: Optional[InsightManifest] = None
    
    def get_active_manifest(self) -> InsightManifest:
        """Get the currently active manifest."""
        if self._active_manifest is None:
            self._active_manifest = self._load_default_manifest()
        return self._active_manifest
    
    def get_enabled_insights(self) -> List[InsightConfig]:
        """Get all enabled insights from the active manifest."""
        manifest = self.get_active_manifest()
        return [config for config in manifest.insights if config.enabled]
    
    def validate_manifest(self, manifest: Dict) -> bool:
        """
        Validate manifest against JSON schema.
        
        Args:
            manifest: Manifest dictionary to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Basic structure validation
            required_fields = ["schema_version", "manifest_id", "name", "insights"]
            for field in required_fields:
                if field not in manifest:
                    return False
            
            # Validate insights array
            if not isinstance(manifest["insights"], list):
                return False
            
            for insight in manifest["insights"]:
                if not isinstance(insight, dict):
                    return False
                required_insight_fields = ["insight_id", "version", "enabled"]
                for field in required_insight_fields:
                    if field not in insight:
                        return False
            
            return True
        except Exception:
            return False
    
    def validate_insight_registry(self) -> None:
        """
        Validate that all insights in manifest are registered.
        Fails fast if any (id, version) missing.
        
        Raises:
            KeyError: If any insight not registered
        """
        manifest = self.get_active_manifest()
        for config in manifest.insights:
            insight_registry.assert_registered(config.insight_id, config.version)
    
    def load_manifest(self, manifest_id: str) -> InsightManifest:
        """
        Load a specific manifest by ID.
        
        Args:
            manifest_id: Manifest identifier
            
        Returns:
            Loaded manifest
        """
        manifest_path = self.manifest_dir / f"{manifest_id}.json"
        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest {manifest_id} not found")
        
        with open(manifest_path, 'r') as f:
            manifest_data = json.load(f)
        
        if not self.validate_manifest(manifest_data):
            raise ValueError(f"Invalid manifest format: {manifest_id}")
        
        return self._dict_to_manifest(manifest_data)
    
    def save_manifest(self, manifest: InsightManifest) -> None:
        """
        Save a manifest to disk.
        
        Args:
            manifest: Manifest to save
        """
        manifest_path = self.manifest_dir / f"{manifest.manifest_id}.json"
        manifest_data = self._manifest_to_dict(manifest)
        
        with open(manifest_path, 'w') as f:
            json.dump(manifest_data, f, indent=2)
    
    def _load_default_manifest(self) -> InsightManifest:
        """Load the default manifest."""
        return self.load_manifest("default")
    
    def _dict_to_manifest(self, data: Dict) -> InsightManifest:
        """Convert dictionary to InsightManifest."""
        insights = [
            InsightConfig(
                insight_id=insight["insight_id"],
                version=insight["version"],
                enabled=insight["enabled"],
                weight=insight.get("weight", 1.0)
            )
            for insight in data["insights"]
        ]
        
        return InsightManifest(
            schema_version=data["schema_version"],
            manifest_id=data["manifest_id"],
            name=data["name"],
            description=data["description"],
            created_by=data["created_by"],
            updated_by=data["updated_by"],
            insights=insights,
            overrides=data.get("overrides")
        )
    
    def _manifest_to_dict(self, manifest: InsightManifest) -> Dict:
        """Convert InsightManifest to dictionary."""
        return {
            "schema_version": manifest.schema_version,
            "manifest_id": manifest.manifest_id,
            "name": manifest.name,
            "description": manifest.description,
            "created_by": manifest.created_by,
            "updated_by": manifest.updated_by,
            "insights": [
                {
                    "insight_id": insight.insight_id,
                    "version": insight.version,
                    "enabled": insight.enabled,
                    "weight": insight.weight
                }
                for insight in manifest.insights
            ],
            "overrides": manifest.overrides
        }
