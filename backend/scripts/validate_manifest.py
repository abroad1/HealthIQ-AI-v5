#!/usr/bin/env python3
"""
Validate insight manifest format and consistency.
"""

import sys
import json
import os
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from services.insights.manifest_service import ManifestService


def validate_manifest_format():
    """Validate manifest JSON format."""
    print("Validating manifest format...")
    
    try:
        service = ManifestService("data/insight_manifests")
        manifest = service.get_active_manifest()
        
        print(f"SUCCESS: Manifest format valid: {manifest.manifest_id}")
        print(f"  - Schema version: {manifest.schema_version}")
        print(f"  - Name: {manifest.name}")
        print(f"  - Insights: {len(manifest.insights)}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Manifest format validation failed: {e}")
        return False


def validate_manifest_schema():
    """Validate manifest against JSON schema."""
    print("\nValidating manifest against JSON schema...")
    
    try:
        service = ManifestService("data/insight_manifests")
        manifest = service.get_active_manifest()
        
        # Convert to dict for validation
        manifest_dict = {
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
            ]
        }
        
        # Validate using service method
        if service.validate_manifest(manifest_dict):
            print("SUCCESS: Manifest schema validation passed")
            return True
        else:
            print("ERROR: Manifest schema validation failed")
            return False
            
    except Exception as e:
        print(f"ERROR: Schema validation failed: {e}")
        return False


def validate_insight_ids():
    """Validate insight IDs follow naming convention."""
    print("\nValidating insight ID naming convention...")
    
    try:
        service = ManifestService("data/insight_manifests")
        manifest = service.get_active_manifest()
        
        invalid_ids = []
        for insight in manifest.insights:
            insight_id = insight.insight_id
            # Check lowercase snake_case format
            if not insight_id.replace('_', '').islower() or ' ' in insight_id:
                invalid_ids.append(insight_id)
        
        if invalid_ids:
            print(f"ERROR: Invalid insight IDs found: {invalid_ids}")
            print("  Insight IDs must be lowercase snake_case (e.g., 'metabolic_age')")
            return False
        
        print("SUCCESS: All insight IDs follow naming convention")
        return True
        
    except Exception as e:
        print(f"ERROR: Insight ID validation failed: {e}")
        return False


def validate_version_format():
    """Validate version strings follow SemVer format."""
    print("\nValidating version format...")
    
    try:
        service = ManifestService("data/insight_manifests")
        manifest = service.get_active_manifest()
        
        invalid_versions = []
        for insight in manifest.insights:
            version = insight.version
            # Check SemVer format (v1.2.3)
            if not version.startswith('v') or len(version.split('.')) != 3:
                invalid_versions.append(f"{insight.insight_id}: {version}")
        
        if invalid_versions:
            print(f"ERROR: Invalid version formats found:")
            for invalid in invalid_versions:
                print(f"  - {invalid}")
            print("  Versions must follow SemVer format (e.g., 'v1.0.0')")
            return False
        
        print("SUCCESS: All versions follow SemVer format")
        return True
        
    except Exception as e:
        print(f"ERROR: Version validation failed: {e}")
        return False


def main():
    """Main validation function."""
    print("HealthIQ-AI v5 - Manifest Validation")
    print("=" * 50)
    
    # Run all validations
    format_valid = validate_manifest_format()
    schema_valid = validate_manifest_schema()
    ids_valid = validate_insight_ids()
    versions_valid = validate_version_format()
    
    print("\n" + "=" * 50)
    if all([format_valid, schema_valid, ids_valid, versions_valid]):
        print("SUCCESS: All manifest validations passed!")
        sys.exit(0)
    else:
        print("ERROR: Manifest validation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
