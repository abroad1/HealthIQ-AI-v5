"""
Canonical signal-library validation tests for KB-S45a dual-mode override conditions.

Regression target: backend/scripts/validate_signal_library.py + knowledge_bus/schema/signal_library_schema.yaml
"""

from __future__ import annotations

import importlib.util
import sys
import textwrap
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[3]
_SCHEMA_PATH = _REPO_ROOT / "knowledge_bus" / "schema" / "signal_library_schema.yaml"


def _load_validator():
    path = _REPO_ROOT / "backend" / "scripts" / "validate_signal_library.py"
    name = "validate_signal_library_kb_s45a_tests"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    # Required for dataclasses / forward refs when loading via importlib
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _run_validate(library_text: str, tmp_path: Path) -> int:
    mod = _load_validator()
    lib_path = tmp_path / "signal_library.yaml"
    lib_path.write_text(library_text, encoding="utf-8")
    out_dir = tmp_path / "out"
    return mod.validate_signal_library(
        schema_path=_SCHEMA_PATH,
        library_path=lib_path,
        output_dir=out_dir,
    )


def _minimal_signal_block(
    *,
    override_yaml: str,
    primary_metric: str = "glucose",
    signal_id: str = "signal_test",
    dependency_biomarkers: list[str] | None = None,
) -> str:
    # Two-space indent matches sibling fields under the signal list item (see canonical packages).
    override_block = textwrap.indent(textwrap.dedent(override_yaml).strip(), "  ")
    deps = [primary_metric] if dependency_biomarkers is None else list(dependency_biomarkers)
    biomarker_lines = "\n".join(f"            - {b}" for b in deps)
    head = textwrap.dedent(
        f"""
        library:
          schema_version: 1.0.0
          package_id: KBP-9999
          library_name: Test Library
          description: KB-S45a validation harness.
        signals:
        - signal_id: {signal_id}
          name: Test
          description: Test signal for override validation.
          system: metabolic
          primary_metric: {primary_metric}
          supporting_metrics: []
          dependencies:
            biomarkers:
{biomarker_lines}
            derived_metrics: []
            signals: []
          optional_dependencies:
            biomarkers: []
            derived_metrics: []
            signals: []
          thresholds:
          - threshold_id: t1
            metric_id: {primary_metric}
            operator: ">="
            value: 0.0
            severity: suboptimal
          activation_logic: deterministic_threshold
        """
    ).strip()
    tail = (
        f"  output:\n"
        f"    signal_value: {primary_metric}\n"
        f"    signal_state: suboptimal\n"
        f"    confidence: confidence_model_v1\n"
    )
    return f"{head}\n{override_block}\n{tail}"


def test_kb_s45a_validator_accepts_valid_lab_range_boundary_condition(tmp_path):
    body = _minimal_signal_block(
        override_yaml=textwrap.dedent(
            """
          override_rules:
          - rule_id: r_lab
            description: Lab boundary override.
            conditions:
            - metric_id: free_t4
              condition_type: all_of
              comparator_type: lab_range_boundary
              boundary: lower
            resulting_state: at_risk
            """
        ),
        primary_metric="tsh",
        signal_id="signal_val_lab",
        dependency_biomarkers=["tsh", "free_t4"],
    )
    assert _run_validate(body, tmp_path) == 0


def test_kb_s45a_validator_rejects_lab_range_boundary_without_boundary(tmp_path):
    body = _minimal_signal_block(
        override_yaml=textwrap.dedent(
            """
          override_rules:
          - rule_id: r_bad
            description: Missing boundary.
            conditions:
            - metric_id: glucose
              operator: "<"
              condition_type: all_of
              comparator_type: lab_range_boundary
            resulting_state: at_risk
            """
        ),
    )
    assert _run_validate(body, tmp_path) != 0


def test_kb_s45a_validator_rejects_lab_range_boundary_with_value(tmp_path):
    body = _minimal_signal_block(
        override_yaml=textwrap.dedent(
            """
          override_rules:
          - rule_id: r_bad
            description: Value forbidden for lab boundary.
            conditions:
            - metric_id: glucose
              condition_type: all_of
              comparator_type: lab_range_boundary
              boundary: lower
              value: 5.0
            resulting_state: at_risk
            """
        ),
    )
    assert _run_validate(body, tmp_path) != 0


def test_kb_s45a_validator_rejects_numeric_condition_without_value(tmp_path):
    body = _minimal_signal_block(
        override_yaml=textwrap.dedent(
            """
          override_rules:
          - rule_id: r_bad
            description: Numeric requires value.
            conditions:
            - metric_id: glucose
              operator: ">="
              condition_type: any_of
            resulting_state: at_risk
            """
        ),
    )
    assert _run_validate(body, tmp_path) != 0


@pytest.mark.parametrize(
    "boundary",
    ["lower", "upper", "out_of_range", "below_min", "above_max"],
)
def test_kb_s45a_validator_accepts_all_governed_boundary_tokens(tmp_path, boundary: str):
    body = _minimal_signal_block(
        override_yaml=textwrap.dedent(
            f"""
          override_rules:
          - rule_id: r_{boundary}
            description: Boundary token test.
            conditions:
            - metric_id: glucose
              condition_type: any_of
              comparator_type: lab_range_boundary
              boundary: {boundary}
            resulting_state: at_risk
            """
        ),
    )
    assert _run_validate(body, tmp_path) == 0
