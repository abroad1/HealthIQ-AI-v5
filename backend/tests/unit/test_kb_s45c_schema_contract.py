"""
KB-S45c / KB-S45c1: signal_library 2.0.0 + research_brief fidelity contract enforcement;
supporting-metric role/availability enum extensions (corroborator, optional).
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import textwrap
from pathlib import Path

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[3]
_SIGNAL_SCHEMA = _REPO_ROOT / "knowledge_bus" / "schema" / "signal_library_schema.yaml"
_RESEARCH_SCHEMA = _REPO_ROOT / "knowledge_bus" / "schema" / "research_brief_schema.yaml"
_VALIDATE_SIGNAL = _REPO_ROOT / "backend" / "scripts" / "validate_signal_library.py"
_VALIDATE_RESEARCH = _REPO_ROOT / "backend" / "scripts" / "validate_research_brief.py"
_BIOMARKER_REGISTRY = _REPO_ROOT / "backend" / "ssot" / "biomarkers.yaml"


def _load_signal_validator():
    name = "validate_signal_library_kb_s45c"
    spec = importlib.util.spec_from_file_location(name, _VALIDATE_SIGNAL)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    # Register before exec_module so @dataclass can resolve __module__ in sys.modules.
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _run_signal_validate(
    tmp_path: Path,
    library_text: str,
    *,
    research_brief_path: Path | None = None,
) -> int:
    lib_path = tmp_path / "signal_library.yaml"
    lib_path.write_text(library_text, encoding="utf-8")
    out_dir = tmp_path / "out"
    mod = _load_signal_validator()
    return mod.validate_signal_library(
        schema_path=_SIGNAL_SCHEMA,
        library_path=lib_path,
        output_dir=out_dir,
        research_brief_path=research_brief_path,
    )


def _minimal_v2_brief() -> str:
    return textwrap.dedent(
        """
        research_domain: metabolic
        sources:
          - source_id: source_kb_s45c_fixture
            paper_title: Example metabolic study title for contract testing
            journal: JCEM
            year: 2020
        biomarkers:
          - glucose
          - hba1c
        physiological_claim: >-
          Elevated fasting glucose associates with sustained dysglycaemia and requires
          structured follow-up in clinical contexts.
        evidence_strength: moderate
        research_summary: Lab-range breach is the trigger; overrides use lab-range conditions.
        """
    ).strip()


def _minimal_v2_library() -> str:
    return textwrap.dedent(
        """
        library:
          package_id: KBP-2499
          schema_version: "2.0.0"
          package_version: 1.0.0
          library_name: KB-S45c harness
          description: Contract test fixture.
        signals:
          - signal_id: signal_kb_s45c_harness
            name: Harness
            description: Deterministic contract harness signal.
            system: metabolic
            primary_metric: glucose
            trigger_direction: high
            supporting_metrics:
              - biomarker_id: hba1c
                expected_direction: high
                role: severity_marker
                availability: common
                rationale: >-
                  Supporting rationale text for harness validation purposes only.
            dependencies:
              biomarkers:
                - glucose
                - hba1c
              derived_metrics: []
              signals: []
            optional_dependencies:
              biomarkers: []
              derived_metrics: []
              signals: []
            thresholds:
              - threshold_id: t_harness
                metric_id: glucose
                operator: ">="
                value: 9999.0
                severity: at_risk
            activation_logic: lab_range_exceeded
            activation_config:
              upper_bound_state: suboptimal
              enable_lower_bound: false
              lower_bound_state: suboptimal
            override_rules:
              - rule_id: or_harness
                description: Escalate when hba1c is above lab max.
                conditions:
                  - metric_id: hba1c
                    condition_type: all_of
                    comparator_type: lab_range_boundary
                    boundary: above_max
                resulting_state: at_risk
                source_refs:
                  - source_kb_s45c_fixture
            output:
              signal_value: glucose
              signal_state: at_risk
              confidence: confidence_model_v1
              primary_metric: glucose
              supporting_markers:
                - hba1c
        """
    ).strip()


def _v2_library_with_supporting_role_and_availability(role: str, availability: str) -> str:
    lib = yaml.safe_load(_minimal_v2_library())
    lib["signals"][0]["supporting_metrics"][0]["role"] = role
    lib["signals"][0]["supporting_metrics"][0]["availability"] = availability
    return yaml.dump(lib, default_flow_style=False, sort_keys=False, allow_unicode=True)


def test_kb_s45c_v2_minimal_fixture_passes(tmp_path: Path):
    brief_path = tmp_path / "research_brief.yaml"
    brief_path.write_text(_minimal_v2_brief(), encoding="utf-8")
    assert _run_signal_validate(tmp_path, _minimal_v2_library(), research_brief_path=brief_path) == 0


def test_kb_s45c_v2_requires_research_brief_path(tmp_path: Path):
    assert _run_signal_validate(tmp_path, _minimal_v2_library(), research_brief_path=None) != 0


def test_kb_s45c_v2_missing_trigger_direction_fails(tmp_path: Path):
    brief_path = tmp_path / "research_brief.yaml"
    brief_path.write_text(_minimal_v2_brief(), encoding="utf-8")
    lib = yaml.safe_load(_minimal_v2_library())
    del lib["signals"][0]["trigger_direction"]
    bad = yaml.dump(lib, default_flow_style=False, sort_keys=False, allow_unicode=True)
    assert _run_signal_validate(tmp_path, bad, research_brief_path=brief_path) != 0


def test_kb_s45c_v2_missing_supporting_expected_direction_fails(tmp_path: Path):
    brief_path = tmp_path / "research_brief.yaml"
    brief_path.write_text(_minimal_v2_brief(), encoding="utf-8")
    lib = yaml.safe_load(_minimal_v2_library())
    del lib["signals"][0]["supporting_metrics"][0]["expected_direction"]
    bad = yaml.dump(lib, default_flow_style=False, sort_keys=False, allow_unicode=True)
    assert _run_signal_validate(tmp_path, bad, research_brief_path=brief_path) != 0


def test_kb_s45c_v2_override_without_source_refs_fails(tmp_path: Path):
    brief_path = tmp_path / "research_brief.yaml"
    brief_path.write_text(_minimal_v2_brief(), encoding="utf-8")
    lib = yaml.safe_load(_minimal_v2_library())
    del lib["signals"][0]["override_rules"][0]["source_refs"]
    bad = yaml.dump(lib, default_flow_style=False, sort_keys=False, allow_unicode=True)
    assert _run_signal_validate(tmp_path, bad, research_brief_path=brief_path) != 0


def test_kb_s45c_v2_unresolved_source_ref_fails(tmp_path: Path):
    brief_path = tmp_path / "research_brief.yaml"
    brief_path.write_text(_minimal_v2_brief(), encoding="utf-8")
    lib = yaml.safe_load(_minimal_v2_library())
    lib["signals"][0]["override_rules"][0]["source_refs"] = ["source_does_not_exist"]
    bad = yaml.dump(lib, default_flow_style=False, sort_keys=False, allow_unicode=True)
    assert _run_signal_validate(tmp_path, bad, research_brief_path=brief_path) != 0


def test_kb_s45c_research_fidelity_rejects_placeholder_journal(tmp_path: Path):
    (tmp_path / "b.yaml").write_text(
        textwrap.dedent(
            """
            research_domain: metabolic
            sources:
              - source_id: source_bad
                paper_title: KB-S45b investigation signal brief — Fake
                journal: HealthIQ Knowledge Bus
                year: 2026
            biomarkers:
              - glucose
            physiological_claim: >-
              Elevated fasting glucose associates with sustained dysglycaemia and requires
              structured follow-up in clinical contexts.
            evidence_strength: moderate
            research_summary: Notes here.
            """
        ).strip(),
        encoding="utf-8",
    )
    proc = subprocess.run(
        [
            sys.executable,
            str(_VALIDATE_RESEARCH),
            "--brief",
            str(tmp_path / "b.yaml"),
            "--schema",
            str(_RESEARCH_SCHEMA),
            "--biomarkers-registry",
            str(_BIOMARKER_REGISTRY),
            "--audit-path",
            str(tmp_path / "audit.md"),
            "--research-fidelity",
        ],
        cwd=str(_REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode != 0


def test_kb_s45c_research_fidelity_rejects_process_claim(tmp_path: Path):
    (tmp_path / "b.yaml").write_text(
        textwrap.dedent(
            """
            research_domain: metabolic
            sources:
              - source_id: source_ok
                paper_title: Real paper title
                journal: JCEM
                year: 2020
            biomarkers:
              - glucose
            physiological_claim: >-
              Investigation signal for glucose high: activation uses lab-range breach semantics
              with governed override conditions consistent with the approved KB-S45 signal definition.
            evidence_strength: moderate
            research_summary: Notes here.
            """
        ).strip(),
        encoding="utf-8",
    )
    proc = subprocess.run(
        [
            sys.executable,
            str(_VALIDATE_RESEARCH),
            "--brief",
            str(tmp_path / "b.yaml"),
            "--schema",
            str(_RESEARCH_SCHEMA),
            "--biomarkers-registry",
            str(_BIOMARKER_REGISTRY),
            "--audit-path",
            str(tmp_path / "audit.md"),
            "--research-fidelity",
        ],
        cwd=str(_REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode != 0


def test_kb_s45c_research_fidelity_valid_brief_passes(tmp_path: Path):
    (tmp_path / "b.yaml").write_text(_minimal_v2_brief(), encoding="utf-8")
    proc = subprocess.run(
        [
            sys.executable,
            str(_VALIDATE_RESEARCH),
            "--brief",
            str(tmp_path / "b.yaml"),
            "--schema",
            str(_RESEARCH_SCHEMA),
            "--biomarkers-registry",
            str(_BIOMARKER_REGISTRY),
            "--audit-path",
            str(tmp_path / "audit.md"),
            "--research-fidelity",
        ],
        cwd=str(_REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0


def test_kb_s45c_existing_pkg_still_validates_v1(tmp_path: Path):
    pkg = _REPO_ROOT / "knowledge_bus" / "packages" / "pkg_s24_hba1c_high_glycaemia"
    proc = subprocess.run(
        [
            sys.executable,
            str(_REPO_ROOT / "backend" / "scripts" / "validate_knowledge_package.py"),
            "--package-dir",
            str(pkg),
        ],
        cwd=str(_REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_kb_s45c1_corroborator_and_optional_accepted(tmp_path: Path):
    brief_path = tmp_path / "research_brief.yaml"
    brief_path.write_text(_minimal_v2_brief(), encoding="utf-8")
    lib = _v2_library_with_supporting_role_and_availability("corroborator", "optional")
    assert _run_signal_validate(tmp_path, lib, research_brief_path=brief_path) == 0


def test_kb_s45c1_invalid_supporting_role_rejected(tmp_path: Path):
    brief_path = tmp_path / "research_brief.yaml"
    brief_path.write_text(_minimal_v2_brief(), encoding="utf-8")
    lib = _v2_library_with_supporting_role_and_availability("not_a_governed_role", "common")
    assert _run_signal_validate(tmp_path, lib, research_brief_path=brief_path) != 0


def test_kb_s45c1_invalid_supporting_availability_rejected(tmp_path: Path):
    brief_path = tmp_path / "research_brief.yaml"
    brief_path.write_text(_minimal_v2_brief(), encoding="utf-8")
    lib = _v2_library_with_supporting_role_and_availability("severity_marker", "not_an_availability")
    assert _run_signal_validate(tmp_path, lib, research_brief_path=brief_path) != 0


def test_kb_s45c1_contextual_marker_and_specialist_still_accepted(tmp_path: Path):
    brief_path = tmp_path / "research_brief.yaml"
    brief_path.write_text(_minimal_v2_brief(), encoding="utf-8")
    lib = _v2_library_with_supporting_role_and_availability("contextual_marker", "specialist")
    assert _run_signal_validate(tmp_path, lib, research_brief_path=brief_path) == 0
