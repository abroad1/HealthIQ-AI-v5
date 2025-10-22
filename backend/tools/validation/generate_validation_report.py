"""
Validation Report Generator

This module combines validation results into comprehensive JSON and HTML reports.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from .validate_aliases_and_ranges import validate_alias_registry
from .validate_biomarker_schema import validate_biomarker_schema


def generate_validation_report(
    alias_yaml: str = "backend/ssot/biomarker_alias_registry.yaml",
    biomarkers_yaml: str = "backend/ssot/biomarkers.yaml",
    output_dir: str = "tests/reports"
) -> Dict[str, Any]:
    """
    Generate comprehensive validation report combining all validation results.
    
    Args:
        alias_yaml: Path to alias registry YAML
        biomarkers_yaml: Path to biomarkers YAML
        output_dir: Directory to save reports
        
    Returns:
        Combined validation results
    """
    print("🚀 Generating comprehensive validation report...")
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Run all validations
    print("\n1️⃣ Running alias and range validation...")
    alias_results = validate_alias_registry(alias_yaml, biomarkers_yaml)
    
    print("\n2️⃣ Running biomarker schema validation...")
    schema_results = validate_biomarker_schema(biomarkers_yaml)
    
    # Combine results
    combined_results = {
        "timestamp": datetime.now().isoformat() + "Z",
        "alias_validation": alias_results,
        "schema_validation": schema_results,
        "status": "PASS" if not (alias_results["errors"] or schema_results["errors"]) else "FAIL"
    }
    
    # Generate JSON report
    json_path = os.path.join(output_dir, "validation_report.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(combined_results, f, indent=2, ensure_ascii=False)
    
    print(f"📄 JSON report saved to: {json_path}")
    
    # Generate HTML report
    html_path = os.path.join(output_dir, "validation_report.html")
    generate_html_report(combined_results, html_path)
    print(f"🌐 HTML report saved to: {html_path}")
    
    # Print summary
    print(f"\n📊 Validation Summary:")
    print(f"   Status: {'✅ PASS' if combined_results['status'] == 'PASS' else '❌ FAIL'}")
    print(f"   Alias errors: {len(alias_results['errors'])}")
    print(f"   Schema errors: {len(schema_results['errors'])}")
    print(f"   Total errors: {len(alias_results['errors']) + len(schema_results['errors'])}")
    
    return combined_results


def generate_html_report(results: Dict[str, Any], output_path: str) -> None:
    """
    Generate HTML validation report.
    
    Args:
        results: Combined validation results
        output_path: Path to save HTML file
    """
    status_icon = "✅" if results["status"] == "PASS" else "❌"
    status_color = "#28a745" if results["status"] == "PASS" else "#dc3545"
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HealthIQ Validation Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: {status_color};
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2em;
        }}
        .status {{
            font-size: 1.2em;
            margin-top: 10px;
        }}
        .content {{
            padding: 20px;
        }}
        .section {{
            margin-bottom: 30px;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            overflow: hidden;
        }}
        .section-header {{
            background: #f8f9fa;
            padding: 15px 20px;
            border-bottom: 1px solid #e9ecef;
            font-weight: bold;
            font-size: 1.1em;
        }}
        .section-content {{
            padding: 20px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .summary-item {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            text-align: center;
        }}
        .summary-item h3 {{
            margin: 0 0 10px 0;
            color: #495057;
        }}
        .summary-item .value {{
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
        }}
        .error {{
            background: #f8d7da;
            color: #721c24;
            padding: 10px;
            margin: 5px 0;
            border-radius: 4px;
            border-left: 4px solid #dc3545;
        }}
        .warning {{
            background: #fff3cd;
            color: #856404;
            padding: 10px;
            margin: 5px 0;
            border-radius: 4px;
            border-left: 4px solid #ffc107;
        }}
        .timestamp {{
            color: #6c757d;
            font-size: 0.9em;
            text-align: center;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>HealthIQ Validation Report</h1>
            <div class="status">{status_icon} {results["status"]}</div>
        </div>
        
        <div class="content">
            <div class="section">
                <div class="section-header">📊 Overall Summary</div>
                <div class="section-content">
                    <div class="summary">
                        <div class="summary-item">
                            <h3>Alias Validation</h3>
                            <div class="value">{results["alias_validation"]["summary"]["valid_aliases"]}/{results["alias_validation"]["summary"]["total_aliases"]}</div>
                            <div>Valid Aliases</div>
                        </div>
                        <div class="summary-item">
                            <h3>Range Validation</h3>
                            <div class="value">{results["alias_validation"]["summary"]["valid_ranges"]}/{results["alias_validation"]["summary"]["total_biomarkers"]}</div>
                            <div>Valid Ranges</div>
                        </div>
                        <div class="summary-item">
                            <h3>Schema Validation</h3>
                            <div class="value">{results["schema_validation"]["summary"]["valid_biomarkers"]}/{results["schema_validation"]["summary"]["total_biomarkers"]}</div>
                            <div>Valid Biomarkers</div>
                        </div>
                        <div class="summary-item">
                            <h3>Total Errors</h3>
                            <div class="value">{len(results["alias_validation"]["errors"]) + len(results["schema_validation"]["errors"])}</div>
                            <div>Errors Found</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <div class="section-header">🔗 Alias & Range Validation</div>
                <div class="section-content">
                    <h4>Summary</h4>
                    <ul>
                        <li>Total aliases: {results["alias_validation"]["summary"]["total_aliases"]}</li>
                        <li>Valid aliases: {results["alias_validation"]["summary"]["valid_aliases"]}</li>
                        <li>Total biomarkers: {results["alias_validation"]["summary"]["total_biomarkers"]}</li>
                        <li>Valid ranges: {results["alias_validation"]["summary"]["valid_ranges"]}</li>
                    </ul>
                    
                    {_generate_errors_html(results["alias_validation"]["errors"], "Alias Errors")}
                    {_generate_warnings_html(results["alias_validation"]["warnings"], "Alias Warnings")}
                </div>
            </div>
            
            <div class="section">
                <div class="section-header">📋 Schema Validation</div>
                <div class="section-content">
                    <h4>Summary</h4>
                    <ul>
                        <li>Total biomarkers: {results["schema_validation"]["summary"]["total_biomarkers"]}</li>
                        <li>Valid biomarkers: {results["schema_validation"]["summary"]["valid_biomarkers"]}</li>
                        <li>Duplicate names: {results["schema_validation"]["summary"]["duplicate_names"]}</li>
                        <li>Invalid categories: {results["schema_validation"]["summary"]["invalid_categories"]}</li>
                    </ul>
                    
                    {_generate_errors_html(results["schema_validation"]["errors"], "Schema Errors")}
                    {_generate_warnings_html(results["schema_validation"]["warnings"], "Schema Warnings")}
                </div>
            </div>
        </div>
        
        <div class="timestamp">
            Generated on {results["timestamp"]}
        </div>
    </div>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


def _generate_errors_html(errors: list, title: str) -> str:
    """Generate HTML for errors section."""
    if not errors:
        return f"<h4>{title}</h4><p>✅ No errors found</p>"
    
    html = f"<h4>{title}</h4>"
    for error in errors[:10]:  # Show first 10 errors
        html += f'<div class="error">{error}</div>'
    
    if len(errors) > 10:
        html += f'<div class="error">... and {len(errors) - 10} more errors</div>'
    
    return html


def _generate_warnings_html(warnings: list, title: str) -> str:
    """Generate HTML for warnings section."""
    if not warnings:
        return f"<h4>{title}</h4><p>✅ No warnings found</p>"
    
    html = f"<h4>{title}</h4>"
    for warning in warnings[:5]:  # Show first 5 warnings
        html += f'<div class="warning">{warning}</div>'
    
    if len(warnings) > 5:
        html += f'<div class="warning">... and {len(warnings) - 5} more warnings</div>'
    
    return html


def generate_validation_report_cli():
    """
    CLI entry point for validation report generation.
    """
    import sys
    
    # Default paths
    alias_yaml = "backend/ssot/biomarker_alias_registry.yaml"
    biomarkers_yaml = "backend/ssot/biomarkers.yaml"
    output_dir = "tests/reports"
    
    # Allow override via command line args
    if len(sys.argv) > 1:
        alias_yaml = sys.argv[1]
    if len(sys.argv) > 2:
        biomarkers_yaml = sys.argv[2]
    if len(sys.argv) > 3:
        output_dir = sys.argv[3]
    
    result = generate_validation_report(alias_yaml, biomarkers_yaml, output_dir)
    
    # Exit with error code if validation failed
    if result["status"] == "FAIL":
        sys.exit(1)
    
    print("✅ Validation report generation completed successfully!")


if __name__ == "__main__":
    generate_validation_report_cli()
