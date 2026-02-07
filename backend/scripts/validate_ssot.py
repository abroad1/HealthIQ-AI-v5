"""
Helper script to validate SSOT and write JSON summary.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.ssot.validate import validate_ssot

def main():
    ssot_path = Path(__file__).parent.parent / "ssot" / "biomarkers.yaml"
    
    is_valid, errors, summary = validate_ssot(ssot_path)
    
    # Create artifacts directory if needed
    artifacts_dir = Path(__file__).parent.parent / ".artifacts"
    artifacts_dir.mkdir(exist_ok=True)
    
    # Write JSON summary
    output_path = artifacts_dir / "ssot_validate.json"
    output_data = {
        "valid": is_valid,
        "summary": summary,
        "errors": errors,
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Validation summary written to: {output_path}")
    
    if not is_valid:
        print(f"Validation failed with {len(errors)} errors", file=sys.stderr)
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main()

