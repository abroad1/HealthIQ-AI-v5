"""
Sentinel / bounded regression — narrative compiler WHY reaches Layer C assembly.

Post-LC-S1 protection chore (not a sprint): migrated unchanged from
`tests/unit/test_narrative_report_compiler_v1.py` so Sentinel `--all` and
`-m regression` runs enforce:

  WHY signal inputs → `compile_narrative_report_v1` consumer-visible narratives.

Defect class key: narrative_compiler_why_surface
"""

from __future__ import annotations

import pytest

from core.analytics.narrative_report_compiler_v1 import compile_narrative_report_v1


@pytest.mark.regression
def test_compiler_emits_lead_when_homocysteine_signal_fires():
    ig = {
        "signal_results": [
            {"signal_id": "signal_homocysteine_high", "signal_state": "at_risk"},
        ],
        "primary_driver_system_id": "vascular",
    }
    rep = compile_narrative_report_v1(analysis_id="a1", meta={}, insight_graph=ig, idl_bundle=None)
    assert rep.lead_narrative
    assert "homocysteine" in rep.lead_narrative.lower() or "one-carbon" in rep.lead_narrative.lower()
    assert rep.body_overview
    assert "vascular" in rep.body_overview.lower()
    assert "Benchmark interpretation themes" in rep.body_overview


@pytest.mark.regression
def test_compiler_emits_secondary_when_ldl_signal_fires():
    ig = {
        "signal_results": [
            {"signal_id": "signal_ldl_cholesterol_high", "signal_state": "suboptimal"},
        ],
    }
    rep = compile_narrative_report_v1(analysis_id="a2", meta={}, insight_graph=ig, idl_bundle=None)
    assert rep.secondary_narratives
    assert "lipid" in rep.secondary_narratives.lower() or "ldl" in rep.secondary_narratives.lower()
