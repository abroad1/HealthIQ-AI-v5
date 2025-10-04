#!/usr/bin/env python3
"""
Validate insight registry and manifest consistency.
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from core.insights.registry import insight_registry
from services.insights.manifest_service import ManifestService


def validate_insights():
    """Ensure all insights are properly registered."""
    print("Validating insight registry...")
    
    # Import all modules to trigger registration
    from core.insights.modules import (
        metabolic_age, heart_insight, inflammation, 
        fatigue_root_cause, detox_filtration
    )
    
    insight_registry.ensure_insights_registered()
    registered = insight_registry.get_all()
    
    print(f"SUCCESS: {len(registered)} insights registered")
    
    for insight in registered:
        print(f"  - {insight.metadata.insight_id} v{insight.metadata.version}")
    
    return len(registered) >= 5


def validate_manifest():
    """Validate manifest against registry."""
    print("\nValidating manifest consistency...")
    
    try:
        service = ManifestService("data/insight_manifests")
        manifest = service.get_active_manifest()
        
        print(f"SUCCESS: Manifest loaded: {manifest.manifest_id}")
        print(f"  - {len(manifest.insights)} insights configured")
        
        # Validate each insight in manifest
        missing_insights = []
        for config in manifest.insights:
            try:
                insight_registry.assert_registered(config.insight_id, config.version)
                print(f"  SUCCESS: {config.insight_id} v{config.version} registered")
            except KeyError:
                print(f"  ERROR: {config.insight_id} v{config.version} NOT registered")
                missing_insights.append((config.insight_id, config.version))
        
        if missing_insights:
            print(f"\nERROR: {len(missing_insights)} insights missing from registry:")
            for insight_id, version in missing_insights:
                print(f"  - {insight_id} v{version}")
            return False
        
        print("SUCCESS: All manifest insights are registered")
        return True
        
    except Exception as e:
        print(f"ERROR: Manifest validation failed: {e}")
        return False


def main():
    """Main validation function."""
    print("HealthIQ-AI v5 - Insight Validation")
    print("=" * 50)
    
    # Validate insights
    insights_valid = validate_insights()
    
    # Validate manifest
    manifest_valid = validate_manifest()
    
    print("\n" + "=" * 50)
    if insights_valid and manifest_valid:
        print("SUCCESS: All validations passed!")
        sys.exit(0)
    else:
        print("ERROR: Validation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
