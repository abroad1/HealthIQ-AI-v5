import json

from core.analytics.balanced_systems_presentation_v1 import compile_balanced_systems_v1
from core.dto.builders import build_analysis_result_dto


def test_compile_surfaces_stable_systems_deterministically():
    meta = {
        "insight_graph": {
            "system_states": [
                {
                    "system_id": "cardiovascular_1_biomarkers",
                    "state_codes": ["system_stable_normal"],
                    "rationale_codes": [],
                    "transition_summary_codes": [],
                    "confidence_bucket": "high",
                },
                {
                    "system_id": "metabolic_1_biomarkers",
                    "state_codes": ["system_multi_marker_derangement"],
                    "rationale_codes": [],
                    "transition_summary_codes": [],
                    "confidence_bucket": "moderate",
                },
            ],
        },
        "explainability_report": {
            "dominance_resolution": {
                "influence_ordering": {
                    "supporting_systems": ["cardiovascular_1_biomarkers"],
                }
            },
            "system_burden": {"system_capacity_scores": {"cardiovascular_1_biomarkers": 88}},
        },
    }
    out = compile_balanced_systems_v1(meta=meta, primary_driver_system_id="metabolic")
    assert out is not None
    assert out["intro_line"]
    assert len(out["items"]) == 1
    assert out["items"][0]["system_topic"] == "Cardiovascular"
    assert "broadly within expected ranges" in out["items"][0]["evidence_line"]
    assert "88" in out["items"][0]["capacity_note"]
    assert "supporting" in out["items"][0]["evidence_line"].lower() or "model" in out["items"][0]["evidence_line"].lower()
    # Determinism: same payload → same JSON
    out2 = compile_balanced_systems_v1(meta=meta, primary_driver_system_id="metabolic")
    assert json.dumps(out, sort_keys=True) == json.dumps(out2, sort_keys=True)


def test_compile_excludes_primary_driver_system_from_stable_list():
    meta = {
        "insight_graph": {
            "system_states": [
                {
                    "system_id": "metabolic_1_biomarkers",
                    "state_codes": ["system_stable_normal"],
                    "rationale_codes": [],
                    "transition_summary_codes": [],
                    "confidence_bucket": "high",
                },
            ],
        },
    }
    out = compile_balanced_systems_v1(meta=meta, primary_driver_system_id="metabolic")
    assert out is None


def test_build_analysis_result_dto_includes_narrative_report_v1():
    raw = {
        "analysis_id": "a-narrative",
        "biomarkers": [],
        "clusters": [],
        "insights": [],
        "status": "completed",
        "primary_driver_system_id": "",
        "meta": {"insight_graph": {"report_v1": {}}},
        "narrative_report_v1": {
            "narrative_report_version": "1.0.0",
            "retail_summary": "Lay summary line.",
            "body_overview": "Body overview line.",
            "lead_narrative": "Lead block.",
            "secondary_narratives": "",
            "longitudinal_narrative": "",
            "secondary_systems": "",
            "next_steps_narrative": "",
            "clinician_synthesis": "",
            "meta": {},
        },
    }
    dto = build_analysis_result_dto(raw)
    nr = dto.get("narrative_report_v1")
    assert isinstance(nr, dict)
    assert nr.get("retail_summary") == "Lay summary line."
    assert nr.get("lead_narrative") == "Lead block."


def test_build_analysis_result_dto_includes_balanced_systems():
    raw = {
        "analysis_id": "a1",
        "biomarkers": [],
        "clusters": [],
        "insights": [],
        "status": "completed",
        "primary_driver_system_id": "metabolic",
        "meta": {
            "insight_graph": {
                "report_v1": {},
                "system_states": [
                    {
                        "system_id": "z_system_1_biomarkers",
                        "state_codes": ["system_stable_normal"],
                        "rationale_codes": [],
                        "transition_summary_codes": [],
                        "confidence_bucket": "moderate",
                    },
                    {
                        "system_id": "a_system_1_biomarkers",
                        "state_codes": ["system_stable_normal"],
                        "rationale_codes": [],
                        "transition_summary_codes": [],
                        "confidence_bucket": "moderate",
                    },
                ],
            }
        },
    }
    dto = build_analysis_result_dto(raw)
    assert "balanced_systems_v1" in dto
    bs = dto["balanced_systems_v1"]
    assert bs is not None
    # Sorted by system_id → a_system before z_system
    topics = [x["system_topic"] for x in bs["items"]]
    assert topics == sorted(topics)
