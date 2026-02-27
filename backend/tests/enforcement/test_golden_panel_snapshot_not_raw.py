"""
v5.3 Sprint 6 - Enforcement for golden snapshot pack purity.
"""

import json
from pathlib import Path

from tools.run_golden_panel import run_golden_panel


def test_golden_panel_snapshot_pack_no_prompt_payload_raw_leak(tmp_path):
    fixture = Path(__file__).parent.parent / "fixtures" / "golden_panel_160.json"
    run_dir, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="enforcement-golden",
        write_narrative=True,
    )

    # Snapshot pack should not persist any prompt payload artifact.
    assert not (run_dir / "prompt_payload.json").exists()

    insight_graph = json.loads((run_dir / "insight_graph.json").read_text(encoding="utf-8"))
    text = json.dumps(insight_graph, sort_keys=True).lower()
    forbidden = [
        "\"biomarker_panel\"",
        "\"raw_biomarkers\"",
        "\"prompt_payload\"",
        "\"reference_range\"",
        "\"lab_range\"",
    ]
    for token in forbidden:
        assert token not in text, f"Forbidden raw token in insight_graph artifact: {token}"
