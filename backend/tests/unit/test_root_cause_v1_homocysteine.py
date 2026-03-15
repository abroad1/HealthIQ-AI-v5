import json
from pathlib import Path

import pytest
import yaml

from tools.run_golden_panel import run_golden_panel


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "fixture_name",
    [
        "ab_full_panel_with_ranges.json",
        "vr_full_panel_with_ranges.json",
    ],
)
def test_root_cause_v1_present_for_homocysteine_and_non_regression(tmp_path, fixture_name):
    fixture = Path(__file__).parent.parent / "fixtures" / "panels" / fixture_name
    run_a, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path / "a",
        run_id=f"unit-root-cause-{fixture.stem}-a",
        write_narrative=False,
    )
    run_b, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path / "b",
        run_id=f"unit-root-cause-{fixture.stem}-b",
        write_narrative=False,
    )

    insight_a = _load_json(run_a / "insight_graph.json") or {}
    insight_b = _load_json(run_b / "insight_graph.json") or {}
    report_a = insight_a.get("report_v1") or {}
    report_b = insight_b.get("report_v1") or {}
    root_a = report_a.get("root_cause_v1")
    root_b = report_b.get("root_cause_v1")

    assert isinstance(root_a, dict)
    assert isinstance(root_b, dict)
    assert root_a.get("version") == "v1"
    assert root_b.get("version") == "v1"
    findings = root_a.get("findings", [])
    assert len(findings) == 1
    finding = findings[0]
    assert finding.get("signal_id") == "signal_homocysteine_elevation_context"
    hypotheses = finding.get("hypotheses", [])
    assert len(hypotheses) >= 3
    assert any(float(h.get("hypothesis_confidence", 0.0)) >= 0.40 for h in hypotheses if isinstance(h, dict))

    # Non-regression guards: signal and intervention outputs remain deterministic and unchanged.
    assert insight_a.get("signal_results", []) == insight_b.get("signal_results", [])
    assert report_a.get("actions", {}).get("interventions", []) == report_b.get("actions", {}).get("interventions", [])


def test_root_cause_v1_omitted_when_homocysteine_context_absent(tmp_path):
    fixture = Path(__file__).parent.parent / "fixtures" / "golden_panel_160.json"
    run_dir, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path / "absent",
        run_id="unit-root-cause-absent",
        write_narrative=False,
    )
    report = (_load_json(run_dir / "insight_graph.json") or {}).get("report_v1", {})
    root_cause = report.get("root_cause_v1", None)
    assert root_cause is None


def test_root_cause_v1_text_fields_respect_safety_denylist(tmp_path):
    fixture = Path(__file__).parent.parent / "fixtures" / "panels" / "ab_full_panel_with_ranges.json"
    run_dir, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path / "denylist",
        run_id="unit-root-cause-denylist",
        write_narrative=False,
    )
    insight = _load_json(run_dir / "insight_graph.json") or {}
    root_cause = ((insight.get("report_v1") or {}).get("root_cause_v1") or {})
    findings = root_cause.get("findings", [])
    assert findings

    rules_path = Path(__file__).resolve().parents[3] / "knowledge_bus" / "interventions" / "safety_rules_v1.yaml"
    rules = yaml.safe_load(rules_path.read_text(encoding="utf-8")) or {}
    denylist = [str(x).lower() for x in rules.get("denylist_phrases", [])]

    text_fields = []
    for finding in findings:
        for hypothesis in finding.get("hypotheses", []):
            text_fields.append(str(hypothesis.get("title", "")))
            text_fields.append(str(hypothesis.get("summary", "")))
            for item in hypothesis.get("evidence_for", []):
                text_fields.append(str(item.get("item", "")))
            for item in hypothesis.get("evidence_against", []):
                text_fields.append(str(item.get("item", "")))
            for item in hypothesis.get("missing_data", []):
                text_fields.append(str(item.get("reason", "")))
            for item in hypothesis.get("confirmatory_tests", []):
                text_fields.append(str(item.get("rationale", "")))
    lowered = "\n".join(text_fields).lower()
    for phrase in denylist:
        assert phrase not in lowered
