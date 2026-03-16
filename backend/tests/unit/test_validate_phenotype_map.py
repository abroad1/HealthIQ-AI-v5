import subprocess
import sys
from pathlib import Path

import yaml

from scripts.validate_phenotype_map import DEFAULT_SCHEMA_PATH, validate_phenotype_map


def test_validate_phenotype_map_repo_map_passes():
    is_valid, errors = validate_phenotype_map()
    assert is_valid
    assert errors == []


def test_validate_phenotype_map_detects_orphan_signal(tmp_path):
    map_payload = {
        "schema_version": "v1",
        "phenotypes": [
            {
                "phenotype_id": "ph_invalid_orphan_signal_v1",
                "name": "Invalid orphan phenotype",
                "description": "Temporary invalid map used to assert orphan detection.",
                "systems_involved": ["metabolic"],
                "required_signals": ["signal_this_does_not_exist_v1"],
                "optional_signals": [],
                "required_edges": [],
                "synthetic_fixture_refs": ["ph_renal_stress_v1.json"],
                "chain_expectations": {"status": "pending"},
                "evidence_notes": "Test-only payload",
            }
        ],
    }
    map_path = tmp_path / "invalid_map.yaml"
    map_path.write_text(yaml.safe_dump(map_payload, sort_keys=False), encoding="utf-8")

    cmd = [
        sys.executable,
        str(Path(__file__).resolve().parents[2] / "scripts" / "validate_phenotype_map.py"),
        "--map",
        str(map_path),
        "--schema",
        str(DEFAULT_SCHEMA_PATH),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    assert proc.returncode == 1
    assert "ERROR phenotype_map_v1: [ph_invalid_orphan_signal_v1] orphan signal_id" in proc.stdout
