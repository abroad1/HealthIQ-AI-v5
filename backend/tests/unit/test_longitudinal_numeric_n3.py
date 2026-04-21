"""N-3 — longitudinal lab_value snapshot and numeric delta helpers."""

from core.analytics import snapshot_linker as snapshot_linker_mod
from core.analytics.longitudinal_numeric_v1 import comparable_lab_delta
from core.contracts.insight_graph_v1 import BiomarkerNode


def test_nodes_from_biomarkers_payload_preserves_lab_fields():
    rows = [
        {
            "biomarker_name": "creatinine",
            "status": "high",
            "score": 0.4,
            "value": 110.0,
            "unit": "µmol/L",
        }
    ]
    nodes = snapshot_linker_mod._nodes_from_biomarkers_payload(rows)
    assert len(nodes) == 1
    assert nodes[0].biomarker_id == "creatinine"
    assert nodes[0].lab_value == 110.0
    assert nodes[0].lab_unit == "µmol/L"


def test_comparable_lab_delta_requires_matching_units():
    assert comparable_lab_delta(110.0, "µmol/L", 87.0, "µmol/L") == {
        "prior": 110.0,
        "current": 87.0,
        "delta": -23.0,
        "unit": "µmol/L",
    }
    assert comparable_lab_delta(110.0, "µmol/L", 87.0, "mg/dL") is None


def test_comparable_lab_delta_both_missing_units():
    out = comparable_lab_delta(5.0, None, 4.5, "")
    assert out is not None
    assert out["delta"] == -0.5
    assert out["unit"] == ""


def test_biomarker_node_optional_lab_defaults():
    n = BiomarkerNode(biomarker_id="x", status="normal", score=70.0)
    assert n.lab_value is None
    assert n.lab_unit is None
