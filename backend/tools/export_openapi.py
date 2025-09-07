#!/usr/bin/env python3
"""
Export OpenAPI specification from running HealthIQ-AI v5 backend.

This script hits the running app at http://localhost:8000/openapi.json
and writes the OpenAPI spec to docs/openapi.yaml.

Note: The backend server must be running for this script to work.
"""

import requests
import yaml
from pathlib import Path
import sys


def export_openapi_spec():
    """Export OpenAPI specification from running backend."""
    
    # Configuration
    backend_url = "http://localhost:8000"
    openapi_endpoint = f"{backend_url}/openapi.json"
    output_file = Path("docs/openapi.yaml")
    
    try:
        print(f"Fetching OpenAPI spec from {openapi_endpoint}...")
        
        # Make request to running backend
        response = requests.get(openapi_endpoint, timeout=10)
        response.raise_for_status()
        
        # Parse JSON response
        openapi_spec = response.json()
        
        # Create docs directory if it doesn't exist
        output_file.parent.mkdir(exist_ok=True)
        
        # Write YAML file
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(openapi_spec, f, default_flow_style=False, sort_keys=False)
        
        print(f"✅ OpenAPI spec exported to {output_file}")
        print(f"📊 API has {len(openapi_spec.get('paths', {}))} endpoints")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to backend server")
        print("💡 Make sure the backend is running: uvicorn app.main:app --reload")
        sys.exit(1)
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    export_openapi_spec()
