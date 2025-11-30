"""
Smoke test for Prompt Builder v2 and LLM Output Validator v2.

Loads canonical_small.json, builds prompt, loads valid_llm_result_v2.json,
runs validate_llm_output_v2, and prints "OK" if successful.
"""

import sys
import json
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from core.prompt_builder.v2 import build_prompt_v2
from core.llm.validator_v2 import validate_llm_output_v2
from core.models.context import AnalysisContext
from core.models.user import User
from core.models.biomarker import BiomarkerPanel, BiomarkerValue
from datetime import datetime, UTC


def main():
    """Run smoke test."""
    # Load canonical_small.json
    panel_path = backend_dir / "tests" / "fixtures" / "panels" / "canonical_small.json"
    with open(panel_path, 'r', encoding='utf-8') as f:
        panel_data = json.load(f)
    
    # Create AnalysisContext
    user = User(
        user_id="smoke_test_user",
        age=35,
        gender="male"
    )
    
    biomarkers = {}
    for bm_data in panel_data["biomarkers"]:
        biomarkers[bm_data["name"]] = BiomarkerValue(
            name=bm_data["name"],
            value=bm_data["value"],
            unit=bm_data["unit"],
            reference_range=bm_data.get("reference_range")
        )
    
    biomarker_panel = BiomarkerPanel(
        biomarkers=biomarkers,
        source="smoke_test",
        version="1.0"
    )
    
    context = AnalysisContext(
        analysis_id="smoke_test_analysis",
        user=user,
        biomarker_panel=biomarker_panel,
        created_at=datetime.now(UTC).isoformat()
    )
    
    # Build prompt
    prompt_json = build_prompt_v2(context)
    
    # Load valid_llm_result_v2.json
    result_path = backend_dir / "tests" / "fixtures" / "llm" / "valid_llm_result_v2.json"
    with open(result_path, 'r', encoding='utf-8') as f:
        llm_result_json = json.load(f)
    
    # Validate
    try:
        result = validate_llm_output_v2(prompt_json, llm_result_json)
        print("OK")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

