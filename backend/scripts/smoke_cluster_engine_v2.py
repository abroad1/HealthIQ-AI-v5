"""
Smoke test for Cluster Engine v2.

Loads SSOT biomarkers and cluster_rules.yaml, creates synthetic input,
runs score_clusters, and prints JSON result.
"""

import sys
import json
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from core.clustering.cluster_engine_v2 import score_clusters


def main():
    """Run smoke test."""
    # Create synthetic input (4-6 biomarkers + 1 derived metric)
    biomarkers = [
        {
            "name": "alt",
            "value": 45.0,
            "unit": "U/L",
            "flag": "high"
        },
        {
            "name": "ast",
            "value": 38.0,
            "unit": "U/L",
            "flag": "normal"
        },
        {
            "name": "glucose",
            "value": 105.0,
            "unit": "mg/dL",
            "flag": "high"
        },
        {
            "name": "hba1c",
            "value": 5.8,
            "unit": "%",
            "flag": "normal"
        },
        {
            "name": "total_cholesterol",
            "value": 220.0,
            "unit": "mg/dL",
            "flag": "high"
        },
        {
            "name": "ldl_cholesterol",
            "value": 140.0,
            "unit": "mg/dL",
            "flag": "high"
        }
    ]
    
    derived = [
        {
            "id": "tg_hdl",
            "value": 3.2,
            "band": "high"
        }
    ]
    
    # Run score_clusters
    try:
        results = score_clusters(biomarkers, derived)
        
        # Print JSON result
        print(json.dumps(results, indent=2))
        
        # Verify we got 8 clusters
        if len(results) != 8:
            print(f"ERROR: Expected 8 clusters, got {len(results)}", file=sys.stderr)
            sys.exit(1)
        
        # Verify all have required fields
        required_fields = {"id", "score", "band", "drivers", "confidence", "tags"}
        for result in results:
            missing = required_fields - set(result.keys())
            if missing:
                print(f"ERROR: Missing fields in result: {missing}", file=sys.stderr)
                sys.exit(1)
        
        sys.exit(0)
    
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
