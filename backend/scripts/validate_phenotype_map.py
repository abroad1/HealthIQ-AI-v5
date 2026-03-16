#!/usr/bin/env python3
"""
Validate KB-S35 phenotype map registry against schema and repo assets.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import yaml


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MAP_PATH = ROOT / "knowledge_bus" / "phenotypes" / "phenotype_map_v1.yaml"
DEFAULT_SCHEMA_PATH = ROOT / "knowledge_bus" / "phenotypes" / "phenotype_map_schema_v1.yaml"
PACKAGES_ROOT = ROOT / "knowledge_bus" / "packages"
FIXTURES_ROOT = ROOT / "backend" / "tests" / "fixtures" / "panels" / "phenotypes"
RATIONALES_ROOT = ROOT / "knowledge_bus" / "phenotypes" / "rationales"
ERROR_PREFIX = "ERROR phenotype_map_v1:"


def _err(phenotype_id: str, reason: str, field_path: str) -> str:
    return f"{ERROR_PREFIX} [{phenotype_id}] {reason} (field_path={field_path})"


def _load_yaml(path: Path) -> Dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"YAML document must be a mapping: {path}")
    return payload


def _resolve_path(path_value: str, default_path: Path) -> Path:
    candidate = Path(path_value)
    return candidate if candidate.is_absolute() else (ROOT / candidate if path_value else default_path)


def _check_type(value: Any, type_name: str) -> bool:
    type_map = {
        "str": str,
        "list": list,
        "dict": dict,
        "bool": bool,
    }
    expected = type_map.get(type_name)
    if expected is None:
        return False
    return isinstance(value, expected)


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


def _validate_schema_contract(
    map_payload: Dict[str, Any],
    schema_payload: Dict[str, Any],
) -> Tuple[List[str], List[Dict[str, Any]]]:
    errors: List[str] = []
    required_top = schema_payload.get("top_level_required_keys", []) or []
    for key in required_top:
        if key not in map_payload:
            errors.append(_err("global", f"missing required top-level key '{key}'", f"$.{key}"))

    if map_payload.get("schema_version") != schema_payload.get("schema_version"):
        errors.append(
            _err(
                "global",
                f"schema_version mismatch: expected {schema_payload.get('schema_version')}",
                "$.schema_version",
            )
        )

    phenotypes = map_payload.get("phenotypes")
    if not isinstance(phenotypes, list):
        errors.append(_err("global", "phenotypes must be a list", "$.phenotypes"))
        return errors, []

    required_ph_keys = schema_payload.get("required_phenotype_keys", []) or []
    type_contract = schema_payload.get("type_contract", {}) or {}
    enum_cfg = schema_payload.get("allowed_enums", {}) or {}
    required_edge_keys = schema_payload.get("required_edge_keys", []) or []
    required_basis_keys = schema_payload.get("required_evidence_basis_keys", []) or []
    edge_type_contract = schema_payload.get("edge_type_contract", {}) or {}

    for i, phenotype in enumerate(phenotypes):
        field_base = f"$.phenotypes[{i}]"
        if not isinstance(phenotype, dict):
            errors.append(_err("unknown", "phenotype entry must be an object", field_base))
            continue
        pid = str(phenotype.get("phenotype_id", "")).strip() or "unknown"

        for key in required_ph_keys:
            if key not in phenotype:
                errors.append(_err(pid, f"missing required key '{key}'", f"{field_base}.{key}"))

        for key, type_name in type_contract.items():
            if key in phenotype and not _check_type(phenotype.get(key), type_name):
                errors.append(_err(pid, f"{key} must be type {type_name}", f"{field_base}.{key}"))

        chain_expectations = phenotype.get("chain_expectations", {})
        if isinstance(chain_expectations, dict):
            status = str(chain_expectations.get("status", "")).strip()
            allowed = set(enum_cfg.get("chain_expectations_status", []) or [])
            if status not in allowed:
                errors.append(
                    _err(
                        pid,
                        f"chain_expectations.status must be one of {sorted(allowed)}",
                        f"{field_base}.chain_expectations.status",
                    )
                )
        else:
            errors.append(_err(pid, "chain_expectations must be an object", f"{field_base}.chain_expectations"))

        for j, edge in enumerate(phenotype.get("required_edges", []) or []):
            edge_base = f"{field_base}.required_edges[{j}]"
            if not isinstance(edge, dict):
                errors.append(_err(pid, "required_edges entry must be an object", edge_base))
                continue
            for key in required_edge_keys:
                if key not in edge:
                    errors.append(_err(pid, f"missing edge key '{key}'", f"{edge_base}.{key}"))
            for key, type_name in edge_type_contract.items():
                if key in edge and not _check_type(edge.get(key), type_name):
                    errors.append(_err(pid, f"edge field {key} must be type {type_name}", f"{edge_base}.{key}"))
            relationship_type = str(edge.get("relationship_type", "")).strip()
            allowed_relationships = set(enum_cfg.get("relationship_type", []) or [])
            if relationship_type not in allowed_relationships:
                errors.append(
                    _err(
                        pid,
                        f"relationship_type must be one of {sorted(allowed_relationships)}",
                        f"{edge_base}.relationship_type",
                    )
                )
            evidence_strength = str(edge.get("evidence_strength", "")).strip()
            allowed_strength = set(enum_cfg.get("evidence_strength", []) or [])
            if evidence_strength not in allowed_strength:
                errors.append(
                    _err(
                        pid,
                        f"evidence_strength must be one of {sorted(allowed_strength)}",
                        f"{edge_base}.evidence_strength",
                    )
                )
            basis = edge.get("evidence_basis")
            if not isinstance(basis, dict):
                errors.append(_err(pid, "evidence_basis must be an object", f"{edge_base}.evidence_basis"))
                continue
            for key in required_basis_keys:
                if key not in basis:
                    errors.append(_err(pid, f"missing evidence_basis key '{key}'", f"{edge_base}.evidence_basis.{key}"))
            basis_type = str(basis.get("type", "")).strip()
            allowed_basis_types = set(enum_cfg.get("evidence_basis_type", []) or [])
            if basis_type not in allowed_basis_types:
                errors.append(
                    _err(
                        pid,
                        f"evidence_basis.type must be one of {sorted(allowed_basis_types)}",
                        f"{edge_base}.evidence_basis.type",
                    )
                )

    return errors, phenotypes


def validate_phenotype_map(
    map_path: Path | None = None,
    schema_path: Path | None = None,
) -> Tuple[bool, List[str]]:
    resolved_map = map_path or DEFAULT_MAP_PATH
    resolved_schema = schema_path or DEFAULT_SCHEMA_PATH
    errors: List[str] = []

    if not resolved_map.exists():
        return False, [_err("global", "phenotype map file not found", "$")]
    if not resolved_schema.exists():
        return False, [_err("global", "phenotype schema file not found", "$")]

    try:
        map_payload = _load_yaml(resolved_map)
    except Exception as exc:
        return False, [_err("global", f"failed to parse phenotype map: {exc}", "$")]
    try:
        schema_payload = _load_yaml(resolved_schema)
    except Exception as exc:
        return False, [_err("global", f"failed to parse phenotype schema: {exc}", "$")]

    schema_errors, phenotypes = _validate_schema_contract(map_payload, schema_payload)
    errors.extend(schema_errors)

    known_signal_ids = _collect_known_signal_ids(PACKAGES_ROOT)
    if not known_signal_ids:
        errors.append(_err("global", "no signal ids discovered from package libraries", "$"))

    for i, phenotype in enumerate(phenotypes):
        if not isinstance(phenotype, dict):
            continue
        pid = str(phenotype.get("phenotype_id", "")).strip() or "unknown"
        field_base = f"$.phenotypes[{i}]"

        for j, signal_id in enumerate(phenotype.get("required_signals", []) or []):
            sid = str(signal_id).strip()
            if sid and sid not in known_signal_ids:
                errors.append(_err(pid, f"orphan signal_id '{sid}'", f"{field_base}.required_signals[{j}]"))

        for j, signal_id in enumerate(phenotype.get("optional_signals", []) or []):
            sid = str(signal_id).strip()
            if sid and sid not in known_signal_ids:
                errors.append(_err(pid, f"orphan signal_id '{sid}'", f"{field_base}.optional_signals[{j}]"))

        for j, edge in enumerate(phenotype.get("required_edges", []) or []):
            if not isinstance(edge, dict):
                continue
            edge_base = f"{field_base}.required_edges[{j}]"
            from_id = str(edge.get("from_signal_id", "")).strip()
            to_id = str(edge.get("to_signal_id", "")).strip()
            if from_id and from_id not in known_signal_ids:
                errors.append(_err(pid, f"orphan signal_id '{from_id}'", f"{edge_base}.from_signal_id"))
            if to_id and to_id not in known_signal_ids:
                errors.append(_err(pid, f"orphan signal_id '{to_id}'", f"{edge_base}.to_signal_id"))
            if from_id and to_id and from_id == to_id:
                errors.append(_err(pid, "required edge cannot connect a signal to itself", edge_base))

            basis = edge.get("evidence_basis")
            promo = edge.get("requires_research_promotion")
            if isinstance(basis, dict):
                basis_type = str(basis.get("type", "")).strip()
                ref = str(basis.get("ref", "")).strip()
                if not ref:
                    errors.append(_err(pid, "evidence_basis.ref must be non-empty", f"{edge_base}.evidence_basis.ref"))
                if not isinstance(promo, bool):
                    errors.append(_err(pid, "requires_research_promotion must be boolean", f"{edge_base}.requires_research_promotion"))
                elif basis_type == "rationale_md":
                    if promo is not True:
                        errors.append(
                            _err(
                                pid,
                                "requires_research_promotion must be true when evidence_basis.type is rationale_md",
                                f"{edge_base}.requires_research_promotion",
                            )
                        )
                    rationale_path = _resolve_path(ref, RATIONALES_ROOT)
                    if not rationale_path.exists():
                        errors.append(_err(pid, f"rationale file not found: {ref}", f"{edge_base}.evidence_basis.ref"))
                    try:
                        rationale_path.relative_to(RATIONALES_ROOT)
                    except ValueError:
                        errors.append(
                            _err(
                                pid,
                                "rationale_md ref must point inside knowledge_bus/phenotypes/rationales/",
                                f"{edge_base}.evidence_basis.ref",
                            )
                        )
                elif isinstance(promo, bool) and promo is not False:
                    errors.append(
                        _err(
                            pid,
                            "requires_research_promotion must be false unless evidence_basis.type is rationale_md",
                            f"{edge_base}.requires_research_promotion",
                        )
                    )

        for j, fixture_ref in enumerate(phenotype.get("synthetic_fixture_refs", []) or []):
            fixture_name = str(fixture_ref).strip()
            fixture_path = FIXTURES_ROOT / fixture_name
            if not fixture_name or not fixture_path.exists():
                errors.append(
                    _err(
                        pid,
                        f"synthetic fixture ref not found: {fixture_name}",
                        f"{field_base}.synthetic_fixture_refs[{j}]",
                    )
                )

    return len(errors) == 0, errors


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate KB-S35 phenotype map registry.")
    parser.add_argument("--map", dest="map_path", default=str(DEFAULT_MAP_PATH))
    parser.add_argument("--schema", dest="schema_path", default=str(DEFAULT_SCHEMA_PATH))
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    map_path = _resolve_path(str(args.map_path), DEFAULT_MAP_PATH)
    schema_path = _resolve_path(str(args.schema_path), DEFAULT_SCHEMA_PATH)
    is_valid, errors = validate_phenotype_map(map_path=map_path, schema_path=schema_path)
    if not is_valid:
        for err in errors:
            print(err)
        return 1
    print("phenotype_map_v1: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
