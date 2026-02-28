"""
Deterministic 3-layer pipeline verification script.

Runs golden runner (no lifestyle, LLM disabled), then asserts:
- status == completed
- Required artifacts exist
- layer3 schema_version == 1.0.0
- 11 cards with required fields
- All cards have system_burdens evidence, none have lifestyle evidence
- No timestamps in layer3_insights.json

Fails hard with AssertionError on any invariant break.

Usage:
  python backend/scripts/verify_three_layer_pipeline.py
  (run from repo root; or from backend with: python scripts/verify_three_layer_pipeline.py)
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Ensure backend is on path when run from repo root
_backend = Path(__file__).resolve().parents[1]
if str(_backend) not in sys.path:
    sys.path.insert(0, str(_backend))

# Must set before importing run_golden_panel (reads env at import/call time)
os.environ["HEALTHIQ_ENABLE_LLM"] = "0"

from tools.run_golden_panel import run_golden_panel, _default_fixture_path, _default_output_root


def _collect_timestamp_keys(obj: object, path: str = "") -> list[str]:
    """Recursively find any timestamp-like keys in obj. Returns list of paths."""
    found: list[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            key_lower = str(k).lower()
            if any(ts in key_lower for ts in ("created_at", "timestamp", "elapsed", "latency", "processing_time", "updated_at", "run_id")):
                found.append(f"{path}.{k}" if path else str(k))
            found.extend(_collect_timestamp_keys(v, f"{path}.{k}" if path else str(k)))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            found.extend(_collect_timestamp_keys(item, f"{path}[{i}]"))
    return found


def verify_three_layer_pipeline() -> None:
    """Run golden panel (no lifestyle) and verify 3-layer pipeline invariants."""
    fixture = _default_fixture_path()
    output_root = _default_output_root() / "three_layer_verify"
    output_root.mkdir(parents=True, exist_ok=True)

    run_dir, result = run_golden_panel(
        fixture_path=fixture,
        output_root=output_root,
        run_id=None,  # Use default timestamp
        write_narrative=False,
        enable_llm=False,
        lifestyle_fixture_path=None,
    )

    status = result.get("status")
    if status != "completed":
        raise AssertionError(
            f"3-LAYER PIPELINE VERIFICATION FAILED: expected status=='completed', got status=='{status}'"
        )

    required_files = [
        "analysis_result.json",
        "burden_vector.json",
        "insight_graph.json",
        "layer3_insights.json",
    ]
    missing = [f for f in required_files if not (run_dir / f).exists()]
    if missing:
        raise AssertionError(
            f"3-LAYER PIPELINE VERIFICATION FAILED: missing artifacts: {missing} in {run_dir}"
        )

    # Load and validate all 4 artifacts (ensures valid JSON)
    json.loads((run_dir / "analysis_result.json").read_text(encoding="utf-8"))
    burden_vector = json.loads((run_dir / "burden_vector.json").read_text(encoding="utf-8"))
    json.loads((run_dir / "insight_graph.json").read_text(encoding="utf-8"))
    layer3 = json.loads((run_dir / "layer3_insights.json").read_text(encoding="utf-8"))

    schema_version = layer3.get("schema_version")
    if schema_version != "1.0.0":
        raise AssertionError(
            f"3-LAYER PIPELINE VERIFICATION FAILED: layer3.schema_version must be '1.0.0', got '{schema_version}'"
        )

    insights = layer3.get("insights", [])
    if len(insights) < 1:
        raise AssertionError(
            f"3-LAYER PIPELINE VERIFICATION FAILED: expected at least 1 card, got {len(insights)}"
        )

    supported_system_ids = frozenset(
        burden_vector.get("adjusted_system_burden_vector") or {}
    )

    required_card_fields = {"insight_id", "system_id", "severity", "confidence"}
    for i, card in enumerate(insights):
        if not isinstance(card, dict):
            raise AssertionError(
                f"3-LAYER PIPELINE VERIFICATION FAILED: card[{i}] is not a dict"
            )
        missing_fields = required_card_fields - set(card.keys())
        if missing_fields:
            raise AssertionError(
                f"3-LAYER PIPELINE VERIFICATION FAILED: card[{i}] missing fields: {missing_fields}"
            )
        evidence = card.get("evidence")
        if not isinstance(evidence, dict):
            raise AssertionError(
                f"3-LAYER PIPELINE VERIFICATION FAILED: card[{i}].evidence must be a dict"
            )
        if "system_burdens" not in evidence:
            raise AssertionError(
                f"3-LAYER PIPELINE VERIFICATION FAILED: card[{i}] missing evidence.system_burdens"
            )
        if "lifestyle" in evidence:
            raise AssertionError(
                f"3-LAYER PIPELINE VERIFICATION FAILED: card[{i}] must not have evidence.lifestyle (no-lifestyle mode)"
            )
        card_system_id = card.get("system_id")
        if card_system_id not in supported_system_ids:
            raise AssertionError(
                f"3-LAYER PIPELINE VERIFICATION FAILED: card[{i}].system_id='{card_system_id}' not in burden vectors"
            )

    timestamp_paths = _collect_timestamp_keys(layer3)
    if timestamp_paths:
        raise AssertionError(
            f"3-LAYER PIPELINE VERIFICATION FAILED: layer3_insights.json must not contain timestamps, found: {timestamp_paths}"
        )

    print(f"RUN_DIR: {os.path.abspath(run_dir)}")
    print("3-LAYER PIPELINE VERIFIED: PASS")


if __name__ == "__main__":
    verify_three_layer_pipeline()
