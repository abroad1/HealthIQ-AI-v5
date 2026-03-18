import subprocess
import sys
from pathlib import Path
from typing import Set, Tuple

import yaml

from scripts.validate_interaction_map_v1 import validate_interaction_map_v1


ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = ROOT / "backend" / "scripts" / "validate_interaction_map_v1.py"
REAL_PHENOTYPE_MAP_PATH = ROOT / "knowledge_bus" / "phenotypes" / "phenotype_map_v1.yaml"


def _collect_known_signal_ids(packages_root: Path) -> Set[str]:
    known: Set[str] = set()
    for signal_path in sorted(packages_root.rglob("signal_library.yaml")):
        payload = yaml.safe_load(signal_path.read_text(encoding="utf-8")) or {}
        if not isinstance(payload, dict):
            continue
        for row in payload.get("signals", []) or []:
            if not isinstance(row, dict):
                continue
            signal_id = str(row.get("signal_id", "")).strip()
            if signal_id:
                known.add(signal_id)
    return known


def _required_edge_set(phenotype_map_path: Path) -> Set[Tuple[str, str]]:
    edges: Set[Tuple[str, str]] = set()
    payload = yaml.safe_load(phenotype_map_path.read_text(encoding="utf-8")) or {}
    for phenotype in payload.get("phenotypes", []) or []:
        if not isinstance(phenotype, dict):
            continue
        for edge in phenotype.get("required_edges", []) or []:
            if not isinstance(edge, dict):
                continue
            from_signal = str(edge.get("from_signal_id", "")).strip()
            to_signal = str(edge.get("to_signal_id", "")).strip()
            if from_signal and to_signal:
                edges.add((from_signal, to_signal))
    return edges


def test_validate_interaction_map_v1_controlled_maps_pass(tmp_path):
    phenotype_payload = {
        "schema_version": "v1",
        "phenotypes": [
            {
                "phenotype_id": "ph_controlled_pass_v1",
                "name": "Controlled pass phenotype",
                "description": "Temporary deterministic PASS fixture.",
                "systems_involved": ["inflammatory"],
                "required_signals": ["signal_crp_high", "signal_mcv_high"],
                "optional_signals": [],
                "required_edges": [
                    {
                        "from_signal_id": "signal_crp_high",
                        "to_signal_id": "signal_mcv_high",
                        "relationship_type": "co_occurrence",
                        "evidence_strength": "exploratory",
                        "evidence_basis": {
                            "type": "guideline",
                            "ref": "KB-S40-controlled-pass",
                        },
                        "requires_research_promotion": False,
                    }
                ],
                "synthetic_fixture_refs": [],
                "chain_expectations": {"status": "pending"},
                "evidence_notes": "test",
            }
        ],
    }
    interaction_payload = {
        "map_version": "v1",
        "edges": [
            {
                "from_signal": "signal_crp_high",
                "to_signal": "signal_mcv_high",
                "relationship_type": "co_occurrence",
                "evidence_strength": "exploratory",
            }
        ],
    }
    phenotype_path = tmp_path / "phenotype_map_controlled_pass.yaml"
    interaction_path = tmp_path / "interaction_map_controlled_pass.yaml"
    phenotype_path.write_text(yaml.safe_dump(phenotype_payload, sort_keys=False), encoding="utf-8")
    interaction_path.write_text(yaml.safe_dump(interaction_payload, sort_keys=False), encoding="utf-8")

    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--interaction-map",
            str(interaction_path),
            "--phenotype-map",
            str(phenotype_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert proc.stdout == "interaction_map_v1: PASS\n"


def test_validate_interaction_map_v1_stops_when_allowed_edge_set_empty(tmp_path):
    phenotype_payload = {
        "schema_version": "v1",
        "phenotypes": [
            {
                "phenotype_id": "ph_empty_required_edges_v1",
                "name": "Empty required edges phenotype",
                "description": "Temporary stop-condition test payload.",
                "systems_involved": ["metabolic"],
                "required_signals": ["signal_crp_high"],
                "optional_signals": [],
                "required_edges": [],
                "synthetic_fixture_refs": [],
                "chain_expectations": {"status": "pending"},
                "evidence_notes": "test",
            }
        ],
    }
    interaction_payload = {
        "map_version": "v1",
        "edges": [
            {
                "from_signal": "signal_crp_high",
                "to_signal": "signal_mcv_high",
                "relationship_type": "co_occurrence",
                "evidence_strength": "exploratory",
            }
        ],
    }
    phenotype_path = tmp_path / "phenotype_map_empty_edges.yaml"
    interaction_path = tmp_path / "interaction_map_for_stop.yaml"
    phenotype_path.write_text(yaml.safe_dump(phenotype_payload, sort_keys=False), encoding="utf-8")
    interaction_path.write_text(yaml.safe_dump(interaction_payload, sort_keys=False), encoding="utf-8")

    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--interaction-map",
            str(interaction_path),
            "--phenotype-map",
            str(phenotype_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 1
    assert (
        "STOP validate_interaction_map_v1: phenotype_map contains no required_edges entries. "
        "Cannot evaluate phenotype coverage with empty allowed set. Verify KB-S35 phenotype map is "
        "populated before running this validator."
    ) in proc.stdout


def test_validate_interaction_map_v1_fails_orphaned_edge(tmp_path):
    interaction_payload = {
        "map_version": "v1",
        "edges": [
            {
                "from_signal": "signal_does_not_exist",
                "to_signal": "signal_crp_high",
                "relationship_type": "co_occurrence",
                "evidence_strength": "exploratory",
            }
        ],
    }
    interaction_path = tmp_path / "interaction_map_invalid.yaml"
    interaction_path.write_text(yaml.safe_dump(interaction_payload, sort_keys=False), encoding="utf-8")

    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--interaction-map",
            str(interaction_path),
            "--phenotype-map",
            str(REAL_PHENOTYPE_MAP_PATH),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 1
    assert (
        "ERROR interaction_map_v1: orphaned_edge signal_id=signal_does_not_exist "
        "edge=signal_does_not_exist->signal_crp_high"
    ) in proc.stdout


def test_validate_interaction_map_v1_fails_when_edge_not_covered_by_any_phenotype(tmp_path):
    packages_root = ROOT / "knowledge_bus" / "packages"
    known_signal_ids = _collect_known_signal_ids(packages_root)
    assert "signal_crp_high" in known_signal_ids, "STOP: signal_crp_high missing in live signal libraries."
    assert "signal_mcv_high" in known_signal_ids, "STOP: signal_mcv_high missing in live signal libraries."

    required_edges = _required_edge_set(REAL_PHENOTYPE_MAP_PATH)
    assert (
        "signal_crp_high",
        "signal_mcv_high",
    ) not in required_edges, "STOP: signal_crp_high->signal_mcv_high already covered by phenotype required_edges."

    phenotype_payload = {
        "schema_version": "v1",
        "phenotypes": [
            {
                "phenotype_id": "ph_uncovered_edge_fixture_v1",
                "name": "Uncovered edge fixture phenotype",
                "description": "Keeps allowed-edge set non-empty while excluding test edge.",
                "systems_involved": ["inflammatory"],
                "required_signals": ["signal_crp_high", "signal_homocysteine_high"],
                "optional_signals": [],
                "required_edges": [
                    {
                        "from_signal_id": "signal_crp_high",
                        "to_signal_id": "signal_homocysteine_high",
                        "relationship_type": "co_occurrence",
                        "evidence_strength": "exploratory",
                        "evidence_basis": {
                            "type": "guideline",
                            "ref": "KB-S40-uncovered-edge-fixture",
                        },
                        "requires_research_promotion": False,
                    }
                ],
                "synthetic_fixture_refs": [],
                "chain_expectations": {"status": "pending"},
                "evidence_notes": "test",
            }
        ],
    }
    interaction_payload = {
        "map_version": "v1",
        "edges": [
            {
                "from_signal": "signal_crp_high",
                "to_signal": "signal_mcv_high",
                "relationship_type": "co_occurrence",
                "evidence_strength": "exploratory",
            }
        ],
    }
    phenotype_path = tmp_path / "phenotype_map_uncovered_edge.yaml"
    interaction_path = tmp_path / "interaction_map_uncovered_edge.yaml"
    phenotype_path.write_text(yaml.safe_dump(phenotype_payload, sort_keys=False), encoding="utf-8")
    interaction_path.write_text(yaml.safe_dump(interaction_payload, sort_keys=False), encoding="utf-8")

    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--interaction-map",
            str(interaction_path),
            "--phenotype-map",
            str(phenotype_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 1
    assert proc.stdout == (
        "interaction_map_v1: FAIL\n"
        "edge_not_covered_by_any_phenotype: 1 edges\n"
        "edge=signal_crp_high->signal_mcv_high\n"
    )


def test_validate_interaction_map_v1_warns_for_rationale_backed_edge(tmp_path):
    phenotype_payload = {
        "schema_version": "v1",
        "phenotypes": [
            {
                "phenotype_id": "ph_temp_rationale_warn_v1",
                "name": "Temp rationale phenotype",
                "description": "Temporary test map for rationale warning behavior.",
                "systems_involved": ["inflammatory"],
                "required_signals": ["signal_crp_high", "signal_mcv_high"],
                "optional_signals": [],
                "required_edges": [
                    {
                        "from_signal_id": "signal_crp_high",
                        "to_signal_id": "signal_mcv_high",
                        "relationship_type": "co_occurrence",
                        "evidence_strength": "exploratory",
                        "evidence_basis": {
                            "type": "rationale_md",
                            "ref": "knowledge_bus/phenotypes/rationales/temp.md",
                        },
                        "requires_research_promotion": True,
                    }
                ],
                "synthetic_fixture_refs": [],
                "chain_expectations": {"status": "pending"},
                "evidence_notes": "test",
            }
        ],
    }
    interaction_payload = {
        "map_version": "v1",
        "edges": [
            {
                "from_signal": "signal_crp_high",
                "to_signal": "signal_mcv_high",
                "relationship_type": "co_occurrence",
                "evidence_strength": "exploratory",
            }
        ],
    }
    phenotype_path = tmp_path / "phenotype_map_rationale.yaml"
    interaction_path = tmp_path / "interaction_map_rationale.yaml"
    phenotype_path.write_text(yaml.safe_dump(phenotype_payload, sort_keys=False), encoding="utf-8")
    interaction_path.write_text(yaml.safe_dump(interaction_payload, sort_keys=False), encoding="utf-8")

    is_valid, errors, warnings, stopped, uncovered_edges = validate_interaction_map_v1(
        interaction_map_path=interaction_path,
        phenotype_map_path=phenotype_path,
    )
    assert is_valid
    assert errors == []
    assert not stopped
    assert uncovered_edges == []
    assert (
        "WARN interaction_map_v1: edge_requires_research_promotion "
        "edge=signal_crp_high->signal_mcv_high "
        "phenotype_id=ph_temp_rationale_warn_v1 ref=knowledge_bus/phenotypes/rationales/temp.md"
    ) in warnings
