#!/usr/bin/env python3
"""
CLI utility for validating SSOT YAML files.

This script validates the Single Source of Truth YAML files including
biomarkers, reference ranges, and unit definitions.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

# Add the backend directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.validation.ssot.validator import SSOTValidator


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate SSOT YAML files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate all SSOT files in the default directory
  python validate_ssot.py
  
  # Validate specific directory
  python validate_ssot.py --ssot-dir /path/to/ssot
  
  # Validate specific file
  python validate_ssot.py --file biomarkers.yaml
  
  # Output results as JSON
  python validate_ssot.py --output-format json
  
  # Include consistency checks
  python validate_ssot.py --check-consistency
        """
    )
    
    parser.add_argument(
        "--ssot-dir",
        type=str,
        default="ssot",
        help="Directory containing SSOT YAML files (default: ssot)"
    )
    
    parser.add_argument(
        "--file",
        type=str,
        choices=["biomarkers.yaml", "ranges.yaml", "units.yaml"],
        help="Validate specific file only"
    )
    
    parser.add_argument(
        "--output-format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    
    parser.add_argument(
        "--check-consistency",
        action="store_true",
        help="Perform consistency checks between files"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Initialize validator
    validator = SSOTValidator()
    
    # Determine SSOT directory
    ssot_dir = Path(args.ssot_dir)
    if not ssot_dir.is_absolute():
        # Make relative to the backend directory
        backend_dir = Path(__file__).parent.parent
        ssot_dir = backend_dir / ssot_dir
    
    if not ssot_dir.exists():
        print(f"Error: SSOT directory not found: {ssot_dir}")
        sys.exit(1)
    
    # Validate files
    if args.file:
        # Validate specific file
        file_path = ssot_dir / args.file
        if not file_path.exists():
            print(f"Error: File not found: {file_path}")
            sys.exit(1)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if args.file == "biomarkers.yaml":
            result = validator.validate_biomarkers_yaml(content)
        elif args.file == "ranges.yaml":
            result = validator.validate_ranges_yaml(content)
        elif args.file == "units.yaml":
            result = validator.validate_units_yaml(content)
        else:
            print(f"Error: Unsupported file type: {args.file}")
            sys.exit(1)
        
        results = {
            "valid": result["valid"],
            "errors": result["errors"],
            "files_validated": 1,
            "file_results": {args.file: result}
        }
    else:
        # Validate all files
        results = validator.validate_all_ssot_files(ssot_dir)
    
    # Perform consistency checks if requested
    if args.check_consistency and results["valid"]:
        biomarker_consistency = validator.validate_biomarker_consistency(results)
        unit_consistency = validator.validate_unit_consistency(results)
        
        results["consistency_checks"] = {
            "biomarker_consistency": biomarker_consistency,
            "unit_consistency": unit_consistency
        }
        
        # Update overall validity
        if not biomarker_consistency["valid"] or not unit_consistency["valid"]:
            results["valid"] = False
            results["errors"].extend(biomarker_consistency["errors"])
            results["errors"].extend(unit_consistency["errors"])
    
    # Output results
    if args.output_format == "json":
        output_json(results)
    else:
        output_text(results, args.verbose)
    
    # Exit with appropriate code
    sys.exit(0 if results["valid"] else 1)


def output_json(results: dict):
    """Output results in JSON format."""
    print(json.dumps(results, indent=2))


def output_text(results: dict, verbose: bool):
    """Output results in human-readable text format."""
    print("=" * 60)
    print("SSOT YAML Validation Results")
    print("=" * 60)
    
    if results["valid"]:
        print("✅ All SSOT files are valid!")
    else:
        print("❌ Validation failed!")
    
    print(f"\nFiles validated: {results['files_validated']}")
    
    if results["errors"]:
        print(f"\nErrors ({len(results['errors'])}):")
        for error in results["errors"]:
            print(f"  • {error}")
    
    # File-specific results
    if "file_results" in results:
        print(f"\nFile Details:")
        for filename, file_result in results["file_results"].items():
            status = "✅ Valid" if file_result["valid"] else "❌ Invalid"
            print(f"  {filename}: {status}")
            
            if verbose and file_result["errors"]:
                for error in file_result["errors"]:
                    print(f"    • {error}")
            
            # Show counts for valid files
            if file_result["valid"]:
                if "biomarker_count" in file_result:
                    print(f"    • Biomarkers: {file_result['biomarker_count']}")
                if "range_count" in file_result:
                    print(f"    • Reference ranges: {file_result['range_count']}")
                if "unit_count" in file_result:
                    print(f"    • Units: {file_result['unit_count']}")
                if "conversion_count" in file_result:
                    print(f"    • Conversions: {file_result['conversion_count']}")
    
    # Consistency check results
    if "consistency_checks" in results:
        print(f"\nConsistency Checks:")
        
        biomarker_consistency = results["consistency_checks"]["biomarker_consistency"]
        unit_consistency = results["consistency_checks"]["unit_consistency"]
        
        status = "✅ Passed" if biomarker_consistency["valid"] else "❌ Failed"
        print(f"  Biomarker consistency: {status}")
        if not biomarker_consistency["valid"] and verbose:
            for error in biomarker_consistency["errors"]:
                print(f"    • {error}")
        
        status = "✅ Passed" if unit_consistency["valid"] else "❌ Failed"
        print(f"  Unit consistency: {status}")
        if not unit_consistency["valid"] and verbose:
            for error in unit_consistency["errors"]:
                print(f"    • {error}")
    
    # Summary
    if "consistency_checks" in results:
        from core.validation.ssot.validator import SSOTValidator
        validator = SSOTValidator()
        summary = validator.get_validation_summary(results)
        print(f"\nSummary:")
        print(f"  Total biomarkers: {summary['total_biomarkers']}")
        print(f"  Total reference ranges: {summary['total_ranges']}")
        print(f"  Total units: {summary['total_units']}")
        print(f"  Total conversions: {summary['total_conversions']}")
    
    print("=" * 60)


if __name__ == "__main__":
    main()