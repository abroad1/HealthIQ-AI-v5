#!/usr/bin/env python3
"""
Validate intervention-effects registry and optional alias map (KB-S48a).

Phase-1 boundary (deterministic): registry documents must not encode threshold/signal
mutation logic — enforced via forbidden key-fragment scan on all mapping keys.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY = ROOT / "knowledge_bus" / "interventions" / "intervention_effects_registry_v1.yaml"
DEFAULT_ALIASES = ROOT / "knowledge_bus" / "interventions" / "intervention_class_alias_map_v1.yaml"
DEFAULT_AUDIT = ROOT / "backend" / "artifacts" / "intervention_effects_registry_audit.md"

REGISTRY_SCHEMA_VERSION = "1.0.0"
ALIAS_SCHEMA_VERSION = "1.0.0"

APPROVED_CLASS_IDS = frozenset(
    {
        "lipid_lowering_statin",
        "systemic_glucocorticoid",
        "thyroid_hormone_replacement",
        "raas_inhibitor",
        "thiazide_or_loop_diuretic",
        "biguanide_metformin",
        "ppi_long_term_high_dose",
        "sex_hormone_therapy",
    }
)

INTERVENTION_TYPES = frozenset({"medication_class", "hormone_therapy_class", "other_class"})
EFFECT_TYPES = frozenset(
    {
        "interpretation_confounder",
        "expected_biomarker_effect",
        "monitoring_relevance",
        "caveat_only",
    }
)
EXPECTED_DIRECTIONS = frozenset(
    {"lower", "raise", "variable", "mixed", "context_dependent"}
)
EVIDENCE_STRENGTH = frozenset({"exploratory", "moderate", "strong", "consensus"})
CITATION_TYPES = frozenset({"guideline", "review", "primary_literature", "internal_summary"})

FORBIDDEN_KEY_FRAGMENTS = (
    "threshold",
    "override_signal",
    "signal_state_mutation",
    "activation_override",
    "lab_range_modify",
    "firing_rule",
    "deterministic_threshold_change",
)


def _collect_key_paths(obj: Any, prefix: str = "") -> list[str]:
    paths: list[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not isinstance(k, str):
                paths.append(f"{prefix}<non-string-key>")
                continue
            p = f"{prefix}.{k}" if prefix else k
            paths.append(p)
            paths.extend(_collect_key_paths(v, p))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            paths.extend(_collect_key_paths(v, f"{prefix}[{i}]"))
    return paths


def _forbidden_key_errors(obj: dict[str, Any], errors: list[str]) -> None:
    paths = _collect_key_paths(obj)
    for path in paths:
        # last segment only
        seg = path.split(".")[-1].split("[")[0]
        low = seg.lower()
        for frag in FORBIDDEN_KEY_FRAGMENTS:
            if frag in low:
                errors.append(
                    f"Phase-1 boundary: key '{seg}' contains forbidden fragment '{frag}' "
                    f"(path: {path})"
                )


def _validate_registry(doc: dict[str, Any], errors: list[str]) -> None:
    if doc.get("registry_schema_version") != REGISTRY_SCHEMA_VERSION:
        errors.append(f"registry_schema_version must be '{REGISTRY_SCHEMA_VERSION}'")
    if doc.get("registry_id") != "intervention_effects_registry_v1":
        errors.append("registry_id must be 'intervention_effects_registry_v1'")

    classes = doc.get("intervention_classes")
    if not isinstance(classes, list):
        errors.append("intervention_classes must be a list")
        return

    seen: set[str] = set()
    for i, row in enumerate(classes):
        lab = f"intervention_classes[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{lab} must be a map")
            continue
        _forbidden_key_errors(row, errors)

        cid = row.get("intervention_class_id")
        if not isinstance(cid, str) or cid not in APPROVED_CLASS_IDS:
            errors.append(f"{lab}.intervention_class_id must be one of {sorted(APPROVED_CLASS_IDS)}")
        else:
            if cid in seen:
                errors.append(f"duplicate intervention_class_id: {cid}")
            seen.add(cid)

        for req in (
            "class_display_name",
            "intervention_type",
            "interpretation_effects",
            "onset_lag",
            "cessation_effect",
            "evidence_strength",
            "physiological_rationale",
            "evidence_sources",
        ):
            if req not in row:
                errors.append(f"{lab}.{req} is required")

        it = row.get("intervention_type")
        if it not in INTERVENTION_TYPES:
            errors.append(f"{lab}.intervention_type must be one of {sorted(INTERVENTION_TYPES)}")

        es = row.get("evidence_strength")
        if es not in EVIDENCE_STRENGTH:
            errors.append(f"{lab}.evidence_strength invalid")

        ie = row.get("interpretation_effects")
        if not isinstance(ie, list) or not ie:
            errors.append(f"{lab}.interpretation_effects must be a non-empty list")
        else:
            for j, eff in enumerate(ie):
                el = f"{lab}.interpretation_effects[{j}]"
                if not isinstance(eff, dict):
                    errors.append(f"{el} must be a map")
                    continue
                et = eff.get("effect_type")
                if et not in EFFECT_TYPES:
                    errors.append(f"{el}.effect_type must be one of {sorted(EFFECT_TYPES)}")
                bids = eff.get("biomarker_ids")
                if not isinstance(bids, list) or not bids or not all(isinstance(x, str) and x for x in bids):
                    errors.append(f"{el}.biomarker_ids must be a non-empty list of strings")
                ed = eff.get("expected_direction")
                if ed not in EXPECTED_DIRECTIONS:
                    errors.append(f"{el}.expected_direction must be one of {sorted(EXPECTED_DIRECTIONS)}")

        ce = row.get("cessation_effect")
        if not isinstance(ce, dict):
            errors.append(f"{lab}.cessation_effect must be a map")
        else:
            if not isinstance(ce.get("description"), str) or len(ce.get("description", "").strip()) < 10:
                errors.append(f"{lab}.cessation_effect.description required (min 10 chars)")
            if not isinstance(ce.get("reversible"), bool):
                errors.append(f"{lab}.cessation_effect.reversible must be boolean")

        srcs = row.get("evidence_sources")
        if not isinstance(srcs, list) or not srcs:
            errors.append(f"{lab}.evidence_sources must be a non-empty list")
        else:
            for j, s in enumerate(srcs):
                sl = f"{lab}.evidence_sources[{j}]"
                if not isinstance(s, dict):
                    errors.append(f"{sl} must be a map")
                    continue
                ct = s.get("citation_type")
                if ct not in CITATION_TYPES:
                    errors.append(f"{sl}.citation_type must be one of {sorted(CITATION_TYPES)}")
                if not isinstance(s.get("citation"), str) or len(s.get("citation", "").strip()) < 5:
                    errors.append(f"{sl}.citation required")

    if seen != APPROVED_CLASS_IDS:
        missing = APPROVED_CLASS_IDS - seen
        extra = seen - APPROVED_CLASS_IDS
        if missing:
            errors.append(f"missing approved class ids: {sorted(missing)}")
        if extra:
            errors.append(f"unexpected class ids: {sorted(extra)}")


def _validate_aliases(doc: dict[str, Any], errors: list[str]) -> None:
    if doc.get("alias_map_schema_version") != ALIAS_SCHEMA_VERSION:
        errors.append(f"alias_map_schema_version must be '{ALIAS_SCHEMA_VERSION}'")
    if doc.get("registry_id") != "intervention_effects_registry_v1":
        errors.append("alias map registry_id must match intervention_effects_registry_v1")

    allowed = doc.get("allowed_target_class_ids")
    if not isinstance(allowed, list) or set(allowed) != APPROVED_CLASS_IDS:
        errors.append("allowed_target_class_ids must list exactly the 8 approved class IDs")

    aliases = doc.get("aliases")
    if not isinstance(aliases, list) or not aliases:
        errors.append("aliases must be a non-empty list")
        return

    seen_alias: set[str] = set()
    for i, row in enumerate(aliases):
        lab = f"aliases[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{lab} must be a map")
            continue
        _forbidden_key_errors(row, errors)
        al = row.get("alias_normalized")
        if not isinstance(al, str) or not al.strip():
            errors.append(f"{lab}.alias_normalized required")
        else:
            a = al.strip().lower()
            if a in seen_alias:
                errors.append(f"duplicate alias_normalized: {a}")
            seen_alias.add(a)

        tid = row.get("intervention_class_id")
        if not isinstance(tid, str) or tid not in APPROVED_CLASS_IDS:
            errors.append(f"{lab}.intervention_class_id must be one of {sorted(APPROVED_CLASS_IDS)}")


def _write_audit(path: Path, status: str, errors: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Intervention-Effects Registry Audit", "", f"validation_status: {status}", "", "errors:"]
    if errors:
        lines.extend(f"- {e}" for e in errors)
    else:
        lines.append("- None")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Validate intervention-effects registry and optional alias map.")
    p.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY, help="Path to intervention_effects_registry_v1.yaml")
    p.add_argument("--aliases", type=Path, default=DEFAULT_ALIASES, help="Path to intervention_class_alias_map_v1.yaml")
    p.add_argument("--skip-aliases", action="store_true", help="Validate registry only.")
    p.add_argument("--audit-path", type=Path, default=DEFAULT_AUDIT)
    args = p.parse_args(argv if argv is not None else sys.argv[1:])

    errors: list[str] = []
    try:
        reg_text = args.registry.resolve().read_text(encoding="utf-8")
        reg_doc = yaml.safe_load(reg_text)
    except (OSError, yaml.YAMLError) as exc:
        errors.append(f"registry load error: {exc}")
        reg_doc = None

    if isinstance(reg_doc, dict):
        _forbidden_key_errors(reg_doc, errors)
        _validate_registry(reg_doc, errors)

    if not args.skip_aliases:
        try:
            alias_text = args.aliases.resolve().read_text(encoding="utf-8")
            alias_doc = yaml.safe_load(alias_text)
        except (OSError, yaml.YAMLError) as exc:
            errors.append(f"alias map load error: {exc}")
            alias_doc = None

        if isinstance(alias_doc, dict):
            _forbidden_key_errors(alias_doc, errors)
            _validate_aliases(alias_doc, errors)

    status = "FAIL" if errors else "PASS"
    _write_audit(args.audit_path.resolve(), status, errors)

    print(f"validation_status: {status}")
    print(f"errors: {len(errors)}")
    print(f"audit_path: {args.audit_path.resolve()}")
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
