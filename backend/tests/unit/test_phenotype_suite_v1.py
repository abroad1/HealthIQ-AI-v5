import json
from pathlib import Path
from typing import Any

import yaml

from tools.run_golden_panel import run_golden_panel


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_expectations() -> dict:
    expectations_path = (
        Path(__file__).parent.parent
        / "fixtures"
        / "panels"
        / "phenotypes"
        / "phenotype_expectations_v1.yaml"
    )
    payload = yaml.safe_load(expectations_path.read_text(encoding="utf-8")) or {}
    assert isinstance(payload, dict)
    return payload


def _signal_ids(signal_results: list[dict[str, Any]]) -> list[str]:
    ids: list[str] = []
    for row in signal_results:
        if not isinstance(row, dict):
            continue
        signal_id = str(row.get("signal_id", "")).strip()
        if signal_id and str(row.get("signal_state", "")).strip() in {"suboptimal", "at_risk"}:
            ids.append(signal_id)
    return sorted(ids)


def _normalized_signal_results(signal_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [row for row in signal_results if isinstance(row, dict)]
    return sorted(rows, key=lambda row: str(row.get("signal_id", "")))


def _strip_volatile(obj: Any) -> Any:
    if isinstance(obj, dict):
        out = {}
        for key, value in obj.items():
            if key in {"generated_at", "created_at", "updated_at", "timestamp", "timestamp_utc"}:
                continue
            out[key] = _strip_volatile(value)
        return out
    if isinstance(obj, list):
        return [_strip_volatile(item) for item in obj]
    return obj


def _max_chain_confidence(interaction_summary: list[dict[str, Any]]) -> float:
    max_conf = 0.0
    for row in interaction_summary:
        if not isinstance(row, dict):
            continue
        try:
            max_conf = max(max_conf, float(row.get("confidence", 0.0)))
        except (TypeError, ValueError):
            continue
    return max_conf


def test_phenotype_suite_v1_regression_harness(tmp_path):
    expectations = _load_expectations()
    phenotypes = expectations.get("phenotypes", [])
    assert isinstance(phenotypes, list) and phenotypes

    fixtures_dir = Path(__file__).parent.parent / "fixtures" / "panels" / "phenotypes"

    for phenotype in phenotypes:
        phenotype_id = str(phenotype.get("phenotype_id", "")).strip()
        fixture_filename = str(phenotype.get("fixture_filename", "")).strip()
        fixture_path = fixtures_dir / fixture_filename
        assert fixture_path.exists(), f"[{phenotype_id}] missing fixture: {fixture_filename}"

        run_a, _ = run_golden_panel(
            fixture_path=fixture_path,
            output_root=tmp_path / phenotype_id / "a",
            run_id=f"unit-phenotype-{phenotype_id}-a",
            write_narrative=False,
        )
        run_b, _ = run_golden_panel(
            fixture_path=fixture_path,
            output_root=tmp_path / phenotype_id / "b",
            run_id=f"unit-phenotype-{phenotype_id}-b",
            write_narrative=False,
        )

        insight_a = _load_json(run_a / "insight_graph.json") or {}
        insight_b = _load_json(run_b / "insight_graph.json") or {}
        signals_a = insight_a.get("signal_results", []) or []
        signals_b = insight_b.get("signal_results", []) or []
        signal_ids = _signal_ids(signals_a)

        assert _normalized_signal_results(signals_a) == _normalized_signal_results(
            signals_b
        ), f"[{phenotype_id}] signal_results not deterministic; observed_signals={signal_ids}"

        chains_a = _strip_volatile(insight_a.get("interaction_chains", []) or [])
        chains_b = _strip_volatile(insight_b.get("interaction_chains", []) or [])
        assert chains_a == chains_b, (
            f"[{phenotype_id}] interaction_chains not deterministic; observed_signals={signal_ids}"
        )

        root_a = _strip_volatile(((insight_a.get("report_v1") or {}).get("root_cause_v1")))
        root_b = _strip_volatile(((insight_b.get("report_v1") or {}).get("root_cause_v1")))
        assert root_a == root_b, (
            f"[{phenotype_id}] root_cause_v1 not deterministic; observed_signals={signal_ids}"
        )

        expected_signals = phenotype.get("expected_signals", {}) or {}
        must_fire = expected_signals.get("must_fire", []) or []
        must_not_fire = expected_signals.get("must_not_fire", []) or []

        for signal_id in must_fire:
            assert signal_id in signal_ids, (
                f"[{phenotype_id}] must_fire missing: {signal_id}; observed_signals={signal_ids}"
            )
        for signal_id in must_not_fire:
            assert signal_id not in signal_ids, (
                f"[{phenotype_id}] must_not_fire present: {signal_id}; observed_signals={signal_ids}"
            )

        chain_status = str(phenotype.get("chain_coverage_status", "")).strip().lower()
        expected_chains = phenotype.get("expected_chains", {}) or {}
        observed_chains = insight_a.get("interaction_chains", []) or []
        observed_summary = insight_a.get("interaction_summary", []) or []
        max_chain_conf = _max_chain_confidence(observed_summary)

        if chain_status == "enforced":
            must_exist = bool(expected_chains.get("must_exist", False))
            min_count = int(expected_chains.get("min_count", 0))
            min_conf = float(expected_chains.get("min_chain_confidence", 0.0))
            must_include_any_signal = expected_chains.get("must_include_any_signal", []) or []

            if must_exist:
                assert observed_chains, (
                    f"[{phenotype_id}] expected chains to exist; observed_signals={signal_ids}"
                )
            assert len(observed_chains) >= min_count, (
                f"[{phenotype_id}] chain count below min_count={min_count}; "
                f"observed_count={len(observed_chains)}; observed_signals={signal_ids}"
            )
            assert max_chain_conf >= min_conf, (
                f"[{phenotype_id}] chain confidence below min_chain_confidence={min_conf}; "
                f"observed_max_confidence={max_chain_conf:.3f}; observed_signals={signal_ids}"
            )
            if must_include_any_signal:
                assert any(
                    any(required in chain for required in must_include_any_signal)
                    for chain in observed_chains
                    if isinstance(chain, list)
                ), (
                    f"[{phenotype_id}] no chain includes required signals={must_include_any_signal}; "
                    f"observed_chains={observed_chains}; observed_signals={signal_ids}"
                )

        expected_root = phenotype.get("expected_root_cause", {}) or {}
        if bool(expected_root.get("must_exist", False)):
            report = insight_a.get("report_v1", {}) or {}
            root = report.get("root_cause_v1")
            assert isinstance(root, dict), (
                f"[{phenotype_id}] expected root_cause_v1 to exist; observed_signals={signal_ids}"
            )
            findings = root.get("findings", []) or []
            applies_to = str(expected_root.get("applies_to_signal_id", "")).strip()
            matching = [
                finding
                for finding in findings
                if isinstance(finding, dict) and str(finding.get("signal_id", "")).strip() == applies_to
            ]
            assert matching, (
                f"[{phenotype_id}] expected root_cause finding for {applies_to}; "
                f"observed_findings={findings}; observed_signals={signal_ids}"
            )
            min_hypothesis_count = int(expected_root.get("min_hypothesis_count", 0))
            hypothesis_count = len(matching[0].get("hypotheses", []) or [])
            assert hypothesis_count >= min_hypothesis_count, (
                f"[{phenotype_id}] root_cause hypothesis count below minimum={min_hypothesis_count}; "
                f"observed_hypothesis_count={hypothesis_count}; observed_signals={signal_ids}"
            )
