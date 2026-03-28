#!/usr/bin/env python3
"""
Validate a single investigation spec (YAML or JSON) against v2 or v3 contract rules.

Version selection (deterministic):
- investigation_spec_contract_version == "3.0.0" → full v3 rules
- absent, "2.0.0", or legacy → v2 structural rules (legacy inventory)

Does not touch package or signal-library validators.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_AUDIT_PATH = ROOT / "backend" / "artifacts" / "investigation_spec_audit.md"

_V3_CONTRACT = "3.0.0"
_V2_CONTRACT = "2.0.0"

# Investigation v3 trigger vocabulary — aligned with signal_library 2.0.0 (not legacy "both").
_V3_TRIGGER_DIRECTION = frozenset({"high", "low", "bidirectional", "context_dependent"})
# Aligned with investigation_spec_schema_v3.0.0 + signal_library + promoted_signal_intelligence (KB-S50).
_V3_SIGNAL_SYSTEMS = frozenset(
    {
        "metabolic",
        "lipid_transport",
        "hepatic",
        "inflammatory",
        "renal",
        "vascular",
        "hematologic",
        "hormonal",
        "mitochondrial",
        "endocrine",
        "bone",
        "mineral",
        "nutritional",
        "other",
    }
)
_EXPECTED = frozenset({"high", "low", "either", "any"})
_ROLES_V3 = frozenset(
    {
        "corroborator",
        "mechanism_marker",
        "contextual_marker",
        "severity_marker",
        "differential_marker",
        "exclusion_marker",
    }
)
_REL_KINDS = frozenset({"mechanism", "corroboration", "severity", "differential", "exclusion"})
_REL_TO_ROLE = {
    "mechanism": frozenset({"mechanism_marker", "contextual_marker"}),
    "corroboration": frozenset({"corroborator"}),
    "severity": frozenset({"severity_marker"}),
    "differential": frozenset({"differential_marker"}),
    "exclusion": frozenset({"exclusion_marker"}),
}
_AVAIL = frozenset({"common", "specialist", "optional"})
_EVIDENCE = frozenset({"exploratory", "moderate", "strong", "consensus"})
_CONTRA_STRENGTH = frozenset({"weak", "moderate", "strong"})
_OPERATORS = frozenset({">", ">=", "<", "<=", "=="})
_CONDITION_TYPE = frozenset({"any_of", "all_of"})
_COMPARATOR = frozenset({"lab_range_boundary", "numeric_value", "presence"})
_BOUNDARIES = frozenset({"above_max", "below_min", "out_of_range"})

_V2_REQUIRED_ROOT = frozenset(
    {
        "spec_id",
        "signal_id",
        "research_domain",
        "primary_marker",
        "trigger_direction",
        "activation",
        "states",
        "supporting_markers",
        "override_rules",
        "evidence",
        "narrative",
    }
)

_V3_REQUIRED_ROOT = _V2_REQUIRED_ROOT | {
    "investigation_spec_contract_version",
    "hypotheses",
    "hypothesis_ranking",
    "confirmatory_tests",
}


def _load(path: Path) -> tuple[Any | None, list[str]]:
    err: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [f"Cannot read {path}: {exc}"]
    try:
        if path.suffix.lower() in {".yaml", ".yml"}:
            return yaml.safe_load(text), err
        if path.suffix.lower() == ".json":
            return json.loads(text), err
        # best-effort YAML
        return yaml.safe_load(text), err
    except (yaml.YAMLError, json.JSONDecodeError) as exc:
        return None, [f"Parse error in {path}: {exc}"]


def _write_audit(path: Path, status: str, errors: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Investigation Spec Audit", "", f"validation_status: {status}", "", "errors:"]
    lines.extend(f"- {e}" for e in errors) if errors else lines.append("- None")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def _validate_override_conditions(conditions: Any, label: str, errors: list[str]) -> None:
    if not isinstance(conditions, list) or not conditions:
        errors.append(f"{label}.conditions must be a non-empty list")
        return
    for ci, cond in enumerate(conditions):
        cl = f"{label}.conditions[{ci}]"
        if not isinstance(cond, dict):
            errors.append(f"{cl} must be a map")
            continue
        for req in ("metric_id", "operator", "condition_type", "comparator_type"):
            if req not in cond:
                errors.append(f"{cl}.{req} is required")
        mid = cond.get("metric_id")
        if not isinstance(mid, str) or not mid.strip():
            errors.append(f"{cl}.metric_id must be a non-empty string")
        op = cond.get("operator")
        if op not in _OPERATORS:
            errors.append(f"{cl}.operator must be one of {sorted(_OPERATORS)}")
        ct = cond.get("condition_type")
        if ct not in _CONDITION_TYPE:
            errors.append(f"{cl}.condition_type must be one of {sorted(_CONDITION_TYPE)}")
        comp = cond.get("comparator_type")
        if comp not in _COMPARATOR:
            errors.append(f"{cl}.comparator_type must be one of {sorted(_COMPARATOR)}")
            continue
        if comp == "lab_range_boundary":
            b = cond.get("boundary")
            if b is None:
                b = cond.get("lab_range_boundary")
            if b not in _BOUNDARIES:
                errors.append(
                    f"{cl}.boundary (or legacy lab_range_boundary) must be one of {sorted(_BOUNDARIES)}"
                )
        elif comp == "numeric_value":
            if cond.get("numeric_value") is None and cond.get("value") is None:
                errors.append(f"{cl}.numeric_value (or legacy value) required for numeric_value mode")
        elif comp == "presence":
            pv = cond.get("presence_value")
            if pv != "present":
                errors.append(f"{cl}.presence_value must be 'present' for presence mode")


def _validate_v2(doc: dict[str, Any], errors: list[str]) -> None:
    missing = _V2_REQUIRED_ROOT - doc.keys()
    if missing:
        errors.append(f"v2: missing required root keys: {sorted(missing)}")
    sm = doc.get("supporting_markers")
    if not isinstance(sm, list) or not sm:
        errors.append("v2: supporting_markers must be a non-empty list")
    else:
        for i, row in enumerate(sm):
            if not isinstance(row, dict):
                errors.append(f"v2: supporting_markers[{i}] must be a map")
                continue
            if not isinstance(row.get("biomarker_id"), str) or not row["biomarker_id"].strip():
                errors.append(f"v2: supporting_markers[{i}].biomarker_id required")
    orules = doc.get("override_rules")
    if isinstance(orules, list):
        for ri, rule in enumerate(orules):
            if not isinstance(rule, dict):
                continue
            _validate_override_conditions(rule.get("conditions"), f"v2.override_rules[{ri}]", errors)


def _validate_v3(doc: dict[str, Any], errors: list[str]) -> None:
    ver = doc.get("investigation_spec_contract_version")
    if ver != _V3_CONTRACT:
        errors.append(f"v3: investigation_spec_contract_version must be '{_V3_CONTRACT}'")

    missing = _V3_REQUIRED_ROOT - doc.keys()
    if missing:
        errors.append(f"v3: missing required root keys: {sorted(missing)}")

    td_root = doc.get("trigger_direction")
    if td_root not in _V3_TRIGGER_DIRECTION:
        errors.append(
            f"v3: trigger_direction must be one of {sorted(_V3_TRIGGER_DIRECTION)}"
        )

    pm_root = doc.get("primary_marker")
    if not isinstance(pm_root, dict):
        errors.append("v3: primary_marker must be a map")
    else:
        ss = pm_root.get("signal_system")
        if not isinstance(ss, str) or not ss.strip():
            errors.append("v3: primary_marker.signal_system is required (non-empty string)")
        elif ss.strip() not in _V3_SIGNAL_SYSTEMS:
            errors.append(
                "v3: primary_marker.signal_system must be one of "
                f"{sorted(_V3_SIGNAL_SYSTEMS)}"
            )

    sm = doc.get("supporting_markers")
    biomarker_ids: set[str] = set()
    has_differential = False
    if not isinstance(sm, list) or not sm:
        errors.append("v3: supporting_markers must be a non-empty list")
    else:
        for i, row in enumerate(sm):
            sl = f"v3.supporting_markers[{i}]"
            if not isinstance(row, dict):
                errors.append(f"{sl} must be a map")
                continue
            bid = row.get("biomarker_id")
            if not isinstance(bid, str) or not bid.strip():
                errors.append(f"{sl}.biomarker_id required")
            else:
                biomarker_ids.add(bid.strip())

            ed = row.get("expected_direction")
            if ed not in _EXPECTED:
                errors.append(f"{sl}.expected_direction must be one of {sorted(_EXPECTED)}")

            role = row.get("role")
            if role not in _ROLES_V3:
                errors.append(f"{sl}.role must be one of {sorted(_ROLES_V3)}")

            rk = row.get("relationship_kind")
            if rk not in _REL_KINDS:
                errors.append(f"{sl}.relationship_kind must be one of {sorted(_REL_KINDS)}")
            elif role in _ROLES_V3 and rk in _REL_TO_ROLE and role not in _REL_TO_ROLE[rk]:
                errors.append(f"{sl}.role '{role}' incompatible with relationship_kind '{rk}'")

            if rk == "differential":
                has_differential = True

            av = row.get("availability")
            if av not in _AVAIL:
                errors.append(f"{sl}.availability must be one of {sorted(_AVAIL)}")

            rat = row.get("rationale")
            if not isinstance(rat, str) or len(rat.strip()) < 10:
                errors.append(f"{sl}.rationale min_length 10")

    if not has_differential:
        errors.append(
            "v3: at least one supporting_markers[].relationship_kind must be 'differential'"
        )

    hyp = doc.get("hypotheses")
    hypo_ids: list[str] = []
    if not isinstance(hyp, list) or len(hyp) < 2:
        errors.append("v3: hypotheses must be a list with at least 2 items")
    else:
        for hi, h in enumerate(hyp):
            hl = f"v3.hypotheses[{hi}]"
            if not isinstance(h, dict):
                errors.append(f"{hl} must be a map")
                continue
            hid = h.get("hypothesis_id")
            if not isinstance(hid, str) or not hid.startswith("hyp_"):
                errors.append(f"{hl}.hypothesis_id must match hyp_*")
            else:
                hypo_ids.append(hid)

            rank = h.get("rank")
            if not isinstance(rank, int) or rank < 1:
                errors.append(f"{hl}.rank must be a positive integer")

            pc = h.get("physiological_claim")
            if not isinstance(pc, str) or len(pc.strip()) < 10:
                errors.append(f"{hl}.physiological_claim min_length 10")

            es = h.get("evidence_strength")
            if es not in _EVIDENCE:
                errors.append(f"{hl}.evidence_strength invalid")

            cav = h.get("caveats")
            if not isinstance(cav, list) or not cav or not all(isinstance(x, str) and x.strip() for x in cav):
                errors.append(f"{hl}.caveats must be a non-empty list of strings")

            md = h.get("missing_data")
            if not isinstance(md, dict) or not isinstance(md.get("policy"), str) or not md["policy"].strip():
                errors.append(f"{hl}.missing_data.policy required")

            refs = h.get("supporting_marker_refs")
            if not isinstance(refs, list) or not refs:
                errors.append(f"{hl}.supporting_marker_refs must be a non-empty list")
            else:
                for ri, ref in enumerate(refs):
                    if not isinstance(ref, str) or ref not in biomarker_ids:
                        errors.append(
                            f"{hl}.supporting_marker_refs[{ri}] '{ref}' must match a supporting_markers.biomarker_id"
                        )

            cms = h.get("contradiction_markers")
            if not isinstance(cms, list):
                errors.append(f"{hl}.contradiction_markers must be a list")
            else:
                for ci, cm in enumerate(cms):
                    cml = f"{hl}.contradiction_markers[{ci}]"
                    if not isinstance(cm, dict):
                        errors.append(f"{cml} must be a map")
                        continue
                    for fld in ("contradiction_id", "marker_reference", "contradiction_rationale", "contradiction_strength"):
                        if fld not in cm:
                            errors.append(f"{cml}.{fld} required")
                    cid = cm.get("contradiction_id")
                    if not isinstance(cid, str) or not cid.startswith("ctr_"):
                        errors.append(f"{cml}.contradiction_id must match ctr_*")
                    cr = cm.get("contradiction_rationale")
                    if not isinstance(cr, str) or len(cr.strip()) < 10:
                        errors.append(f"{cml}.contradiction_rationale min_length 10")
                    cs = cm.get("contradiction_strength")
                    if cs not in _CONTRA_STRENGTH:
                        errors.append(f"{cml}.contradiction_strength invalid")

    if len(hypo_ids) != len(set(hypo_ids)):
        errors.append("v3: duplicate hypothesis_id values")

    hr = doc.get("hypothesis_ranking")
    if not isinstance(hr, dict):
        errors.append("v3: hypothesis_ranking must be a map")
    else:
        oids = hr.get("ordered_hypothesis_ids")
        if not isinstance(oids, list):
            errors.append("v3: hypothesis_ranking.ordered_hypothesis_ids must be a list")
        elif sorted(oids) != sorted(hypo_ids):
            errors.append("v3: hypothesis_ranking.ordered_hypothesis_ids must match hypotheses")

    ct = doc.get("confirmatory_tests")
    if not isinstance(ct, list) or not ct:
        errors.append("v3: confirmatory_tests must be a non-empty list")
    else:
        for ti, t in enumerate(ct):
            tl = f"v3.confirmatory_tests[{ti}]"
            if not isinstance(t, dict):
                errors.append(f"{tl} must be a map")
                continue
            tid = t.get("test_id")
            if not isinstance(tid, str) or not tid.startswith("ct_"):
                errors.append(f"{tl}.test_id must match ct_*")
            tr = t.get("rationale")
            if not isinstance(tr, str) or len(tr.strip()) < 10:
                errors.append(f"{tl}.rationale min_length 10")

    orules = doc.get("override_rules")
    if isinstance(orules, list):
        for ri, rule in enumerate(orules):
            if not isinstance(rule, dict):
                continue
            lbl = f"v3.override_rules[{ri}]"
            for req in ("rule_id", "resulting_state", "description", "conditions", "source_refs"):
                if req not in rule:
                    errors.append(f"{lbl}.{req} required")
            srs = rule.get("source_refs")
            if isinstance(srs, list) and srs:
                for si, s in enumerate(srs):
                    if not isinstance(s, str) or not s.strip():
                        errors.append(f"{lbl}.source_refs[{si}] must be a non-empty string")
            _validate_override_conditions(rule.get("conditions"), lbl, errors)

    # narrative min lengths
    nar = doc.get("narrative")
    if isinstance(nar, dict):
        for fld in ("mechanism", "biological_pathway", "interpretation", "implications", "supporting_marker_roles"):
            v = nar.get(fld)
            if not isinstance(v, str) or len(v.strip()) < 20:
                errors.append(f"v3.narrative.{fld} min_length 20")


def validate_document(doc: Any, errors: list[str]) -> str:
    if not isinstance(doc, dict):
        errors.append("Root must be a map")
        return "unknown"

    ver = doc.get("investigation_spec_contract_version")
    if ver == _V3_CONTRACT:
        _validate_v3(doc, errors)
        return "v3"
    if ver in (None, "", _V2_CONTRACT):
        _validate_v2(doc, errors)
        return "v2"
    errors.append(
        f"Unknown investigation_spec_contract_version {ver!r}; use '{_V3_CONTRACT}' for new specs or omit for v2 legacy"
    )
    return "unknown"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Validate investigation spec YAML/JSON (v2 legacy or v3).")
    p.add_argument("--spec", required=True, type=Path, help="Path to investigation spec file")
    p.add_argument("--audit-path", type=Path, default=DEFAULT_AUDIT_PATH)
    args = p.parse_args(argv if argv is not None else sys.argv[1:])

    spec_path = args.spec.resolve()
    audit_path = args.audit_path.resolve()
    errors: list[str] = []
    doc, load_err = _load(spec_path)
    errors.extend(load_err)
    mode = "unknown"
    if not errors and doc is not None:
        mode = validate_document(doc, errors)

    status = "FAIL" if errors else "PASS"
    _write_audit(audit_path, status, errors)

    print(f"validation_status: {status}")
    print(f"contract_mode: {mode}")
    print(f"errors: {len(errors)}")
    print(f"audit_path: {audit_path}")
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
