"""
SSOT validator - validates biomarker metadata structure.

Validates that all shipped biomarkers have required SSOT metadata fields.
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, Any, List

ALLOWED_SYSTEMS = {
    "metabolic",
    "cardiovascular",
    "hepatic",
    "renal",
    "immune",
    "hematological",
    "hormonal",
    "nutritional",
}

REQUIRED_FIELDS = {
    "system": str,
    "clusters": list,
    "roles": list,
    "key_risks_when_high": list,
    "key_risks_when_low": list,
    "known_modifiers": list,
    "clinical_weight": (int, float),
}

KNOWN_MODIFIERS = {
    "alcohol",
    "training_load",
    "stress",
    "fasting_state",
    "menstrual_phase",
    "meds",
}


def load_ssot(ssot_path: Path = None) -> Dict[str, Any]:
    """Load SSOT biomarkers YAML file."""
    if ssot_path is None:
        ssot_path = Path(__file__).parent.parent.parent / "ssot" / "biomarkers.yaml"
    
    if not ssot_path.exists():
        print(f"ERROR: SSOT file not found: {ssot_path}", file=sys.stderr)
        sys.exit(1)
    
    with open(ssot_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    return data.get("biomarkers", {})


def validate_biomarker(biomarker_id: str, definition: Dict[str, Any]) -> List[str]:
    """Validate a single biomarker definition. Returns list of errors."""
    errors = []
    
    # Check required fields exist
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in definition:
            errors.append(f"{biomarker_id}: missing required field '{field}'")
            continue
        
        value = definition[field]
        
        # Type checking
        if field == "system":
            if not isinstance(value, str):
                errors.append(f"{biomarker_id}: 'system' must be a string, got {type(value).__name__}")
            elif value not in ALLOWED_SYSTEMS:
                errors.append(f"{biomarker_id}: 'system' must be one of {ALLOWED_SYSTEMS}, got '{value}'")
        
        elif field in ("clusters", "roles", "key_risks_when_high", "key_risks_when_low", "known_modifiers"):
            if not isinstance(value, list):
                errors.append(f"{biomarker_id}: '{field}' must be a list, got {type(value).__name__}")
            else:
                # Check list items are strings
                for i, item in enumerate(value):
                    if not isinstance(item, str):
                        errors.append(f"{biomarker_id}: '{field}[{i}]' must be a string, got {type(item).__name__}")
                
                # Validate known_modifiers values
                if field == "known_modifiers":
                    for modifier in value:
                        if modifier not in KNOWN_MODIFIERS:
                            errors.append(f"{biomarker_id}: 'known_modifiers' contains invalid value '{modifier}', must be one of {KNOWN_MODIFIERS}")
        
        elif field == "clinical_weight":
            if not isinstance(value, (int, float)):
                errors.append(f"{biomarker_id}: 'clinical_weight' must be a number, got {type(value).__name__}")
            elif not (0.0 <= float(value) <= 1.0):
                errors.append(f"{biomarker_id}: 'clinical_weight' must be in [0, 1], got {value}")
    
    return errors


def validate_ssot(ssot_path: Path = None) -> tuple[bool, List[str], Dict[str, Any]]:
    """
    Validate SSOT biomarkers file.
    
    Returns:
        (is_valid, errors, summary)
    """
    biomarkers = load_ssot(ssot_path)
    
    all_errors = []
    validated_count = 0
    
    for biomarker_id, definition in biomarkers.items():
        errors = validate_biomarker(biomarker_id, definition)
        if errors:
            all_errors.extend(errors)
        else:
            validated_count += 1
    
    summary = {
        "total_biomarkers": len(biomarkers),
        "validated": validated_count,
        "errors": len(all_errors),
        "first_5_ids": list(biomarkers.keys())[:5],
    }
    
    return len(all_errors) == 0, all_errors, summary


def main():
    """CLI entry point."""
    ssot_path = Path(__file__).parent.parent.parent / "ssot" / "biomarkers.yaml"
    
    is_valid, errors, summary = validate_ssot(ssot_path)
    
    # Print summary
    print(f"SSOT Validation Summary:")
    print(f"  Total biomarkers: {summary['total_biomarkers']}")
    print(f"  Validated: {summary['validated']}")
    print(f"  Errors: {summary['errors']}")
    print(f"  First 5 IDs: {', '.join(summary['first_5_ids'])}")
    
    if errors:
        print("\nErrors found:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("\n✓ All biomarkers validated successfully")
        sys.exit(0)


if __name__ == "__main__":
    main()

