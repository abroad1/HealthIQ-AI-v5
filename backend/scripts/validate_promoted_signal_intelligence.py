#!/usr/bin/env python3
"""
Validate Knowledge Bus promoted_signal_intelligence.yaml (contract v1).

Deterministic structural checks — no heuristics.
Authority: KB-S47d / promoted_signal_intelligence_schema_v1.yaml
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCHEMA_PATH = ROOT / "knowledge_bus" / "schema" / "promoted_signal_intelligence_schema_v1.yaml"
DEFAULT_AUDIT_PATH = ROOT / "backend" / "artifacts" / "promoted_signal_intelligence_audit.md"

_CONTRACT_VER = "1.0.0"
_SCHEMA_VER = "1.0.0"

_FORBIDDEN_ROOT = frozenset(
    {
        "hypotheses",
        "hypothesis_ranking",
        "narrative",
        "rendering",
        "presentation",
        "display",
        "report_layout",
        "ui_hints",
    }
)
_FORBIDDEN_SIGNAL_KEYS = _FORBIDDEN_ROOT | frozenset({"hypotheses", "hypothesis_ranking", "narrative"})

# Aligned with investigation_spec v3.0.0 and promoted_signal_intelligence_schema_v1 (KB-S47d).
_TRIGGERS = frozenset({"high", "low", "bidirectional", "context_dependent"})
_SIGNAL_SYSTEMS = frozenset(
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
_ROLES = frozenset(
    {
        "mechanism_marker",
        "severity_marker",
        "contextual_marker",
        "corroborator",
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
_BOUNDARIES = frozenset(
    {
        "above_max",
        "below_min",
        "out_of_range",
        "not_above_max",
        "not_below_min",
    }
)


def _load_yaml(path: Path) -> tuple[Any | None, list[str]]:
    errors: list[str] = []
    try:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f), errors
    except OSError as exc:
        return None, [f"Could not read {path}: {exc}"]
    except yaml.YAMLError as exc:
        return None, [f"Invalid YAML in {path}: {exc}"]


def _write_audit(path: Path, status: str, errors: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Promoted Signal Intelligence Audit",
        "",
        f"validation_status: {status}",
        "",
        "errors:",
    ]
    if errors:
        lines.extend(f"- {e}" for e in errors)
    else:
        lines.append("- None")
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


def validate_promoted_signal_intelligence(
    doc: dict[str, Any],
    *,
    schema_doc: dict[str, Any],
    source_path: Path,
    errors: list[str],
) -> None:
    if not isinstance(doc, dict):
        errors.append("Root must be a map")
        return

    for fk in schema_doc.get("forbidden_root_keys") or []:
        if fk in doc:
            errors.append(f"Forbidden root key (boundary): {fk}")
    for fk in _FORBIDDEN_ROOT:
        if fk in doc:
            errors.append(f"Forbidden root key (boundary): {fk}")

    trans = doc.get("translation")
    if trans is not None and not isinstance(trans, dict):
        errors.append("translation must be a map when present")

    cver = doc.get("promoted_signal_intelligence_contract_version")
    if cver != _CONTRACT_VER:
        errors.append(f"promoted_signal_intelligence_contract_version must be '{_CONTRACT_VER}' (got {cver!r})")

    sver = doc.get("schema_version")
    if sver != _SCHEMA_VER:
        errors.append(f"schema_version must be '{_SCHEMA_VER}' (got {sver!r})")

    pid = doc.get("package_id")
    if not isinstance(pid, str) or not pid.strip():
        errors.append("package_id must be a non-empty string")

    signals = doc.get("signals")
    if not isinstance(signals, list) or not signals:
        errors.append("signals must be a non-empty list")
        return

    for si, sig in enumerate(signals):
        prefix = f"signals[{si}]"
        if not isinstance(sig, dict):
            errors.append(f"{prefix} must be a map")
            continue

        for fk in _FORBIDDEN_SIGNAL_KEYS:
            if fk in sig:
                errors.append(f"{prefix} must not contain forbidden key '{fk}'")

        sid = sig.get("signal_id")
        if not isinstance(sid, str) or not sid.strip():
            errors.append(f"{prefix}.signal_id must be a non-empty string")
        elif not sid.startswith("signal_"):
            errors.append(f"{prefix}.signal_id must start with 'signal_'")

        rd = sig.get("research_domain")
        if not isinstance(rd, str) or not rd.strip():
            errors.append(f"{prefix}.research_domain must be a non-empty string")

        ss = sig.get("signal_system")
        if ss not in _SIGNAL_SYSTEMS:
            errors.append(
                f"{prefix}.signal_system must be one of {sorted(_SIGNAL_SYSTEMS)}"
            )

        td = sig.get("trigger_direction")
        if td not in _TRIGGERS:
            errors.append(f"{prefix}.trigger_direction must be one of {sorted(_TRIGGERS)}")

        pm = sig.get("primary_metric")
        if not isinstance(pm, dict):
            errors.append(f"{prefix}.primary_metric must be a map")
        else:
            bid = pm.get("biomarker_id")
            if not isinstance(bid, str) or not bid.strip():
                errors.append(f"{prefix}.primary_metric.biomarker_id must be a non-empty string")
            rat = pm.get("rationale")
            if not isinstance(rat, str) or len(rat.strip()) < 10:
                errors.append(f"{prefix}.primary_metric.rationale min_length 10")

        act = sig.get("activation")
        if not isinstance(act, dict):
            errors.append(f"{prefix}.activation must be a map")
        else:
            al = act.get("activation_logic")
            if al not in ("lab_range_exceeded", "deterministic_threshold"):
                errors.append(f"{prefix}.activation.activation_logic invalid")
            ac = act.get("activation_config")
            if not isinstance(ac, dict):
                errors.append(f"{prefix}.activation.activation_config must be a map")
            else:
                for req in (
                    "enable_upper_bound",
                    "upper_bound_state",
                    "enable_lower_bound",
                    "lower_bound_state",
                ):
                    if req not in ac:
                        errors.append(f"{prefix}.activation.activation_config.{req} is required")
                for bool_key in ("enable_upper_bound", "enable_lower_bound"):
                    if not isinstance(ac.get(bool_key), bool):
                        errors.append(
                            f"{prefix}.activation.activation_config.{bool_key} must be a boolean"
                        )
                if ac.get("upper_bound_state") != "suboptimal":
                    errors.append(f"{prefix}.activation.activation_config.upper_bound_state must be 'suboptimal'")
                if ac.get("lower_bound_state") != "suboptimal":
                    errors.append(f"{prefix}.activation.activation_config.lower_bound_state must be 'suboptimal'")

        st = sig.get("states")
        if not isinstance(st, dict):
            errors.append(f"{prefix}.states must be a map")
        else:
            if st.get("baseline_state") != "suboptimal":
                errors.append(f"{prefix}.states.baseline_state must be 'suboptimal'")
            if st.get("escalation_state") != "at_risk":
                errors.append(f"{prefix}.states.escalation_state must be 'at_risk'")

        sm = sig.get("supporting_markers")
        biomarker_ids: set[str] = set()
        has_differential = False
        if not isinstance(sm, list) or not sm:
            errors.append(f"{prefix}.supporting_markers must be a non-empty list")
        else:
            if len(sm) > 15:
                errors.append(f"{prefix}.supporting_markers max 15 items")
            for ri, row in enumerate(sm):
                sl = f"{prefix}.supporting_markers[{ri}]"
                if not isinstance(row, dict):
                    errors.append(f"{sl} must be a map")
                    continue
                b = row.get("biomarker_id")
                if not isinstance(b, str) or not b.strip():
                    errors.append(f"{sl}.biomarker_id required")
                else:
                    biomarker_ids.add(b.strip())
                ed = row.get("expected_direction")
                if ed not in _EXPECTED:
                    errors.append(f"{sl}.expected_direction invalid")
                role = row.get("role")
                if role not in _ROLES:
                    errors.append(f"{sl}.role invalid")
                rk = row.get("relationship_kind")
                if rk not in _REL_KINDS:
                    errors.append(f"{sl}.relationship_kind invalid")
                elif role in _ROLES and rk in _REL_TO_ROLE and role not in _REL_TO_ROLE[rk]:
                    errors.append(f"{sl}.role '{role}' incompatible with relationship_kind '{rk}'")
                if rk == "differential":
                    has_differential = True
                av = row.get("availability")
                if av not in _AVAIL:
                    errors.append(f"{sl}.availability invalid")
                rationale = row.get("rationale")
                if not isinstance(rationale, str) or len(rationale.strip()) < 10:
                    errors.append(f"{sl}.rationale min_length 10")
            if not has_differential:
                errors.append(
                    f"{prefix}: at least one supporting_markers[].relationship_kind must be 'differential'"
                )

        cms = sig.get("contradiction_markers")
        if not isinstance(cms, list):
            errors.append(f"{prefix}.contradiction_markers must be a list")
        else:
            seen_ctr: set[str] = set()
            for ci, cm in enumerate(cms):
                cml = f"{prefix}.contradiction_markers[{ci}]"
                if not isinstance(cm, dict):
                    errors.append(f"{cml} must be a map")
                    continue
                for fld in (
                    "contradiction_id",
                    "marker_reference",
                    "contradiction_rationale",
                    "contradiction_strength",
                ):
                    if fld not in cm:
                        errors.append(f"{cml}.{fld} required")
                cid = cm.get("contradiction_id")
                if not isinstance(cid, str) or not cid.startswith("ctr_"):
                    errors.append(f"{cml}.contradiction_id must match ctr_*")
                if cid in seen_ctr:
                    errors.append(f"{cml}.contradiction_id duplicate '{cid}'")
                seen_ctr.add(str(cid))
                cr = cm.get("contradiction_rationale")
                if not isinstance(cr, str) or len(cr.strip()) < 10:
                    errors.append(f"{cml}.contradiction_rationale min_length 10")
                cs = cm.get("contradiction_strength")
                if cs not in _CONTRA_STRENGTH:
                    errors.append(f"{cml}.contradiction_strength invalid")

        md = sig.get("missing_data")
        if not isinstance(md, dict):
            errors.append(f"{prefix}.missing_data must be a map")
        else:
            pol = md.get("policies")
            if not isinstance(pol, list) or not pol:
                errors.append(f"{prefix}.missing_data.policies must be a non-empty list")
            elif not all(isinstance(x, str) and x.strip() for x in pol):
                errors.append(f"{prefix}.missing_data.policies must be non-empty strings")

        conf = sig.get("confidence")
        conf_es: Any = None
        if not isinstance(conf, dict):
            errors.append(f"{prefix}.confidence must be a map")
        else:
            conf_es = conf.get("evidence_strength")
            if conf_es not in _EVIDENCE:
                errors.append(f"{prefix}.confidence.evidence_strength invalid")

        ev = sig.get("evidence")
        if not isinstance(ev, dict):
            errors.append(f"{prefix}.evidence must be a map")
        else:
            evs = ev.get("evidence_strength")
            if evs not in _EVIDENCE:
                errors.append(f"{prefix}.evidence.evidence_strength invalid")
            pc = ev.get("physiological_claim")
            if not isinstance(pc, str) or len(pc.strip()) < 10:
                errors.append(f"{prefix}.evidence.physiological_claim min_length 10")
            tn = ev.get("threshold_notes")
            if not isinstance(tn, str):
                errors.append(f"{prefix}.evidence.threshold_notes must be a string")
            if "sources" in ev and ev.get("sources") is not None and not isinstance(
                ev.get("sources"), list
            ):
                errors.append(f"{prefix}.evidence.sources must be a list when present")
            if (
                isinstance(conf, dict)
                and conf_es in _EVIDENCE
                and evs in _EVIDENCE
                and conf_es != evs
            ):
                errors.append(
                    f"{prefix}.confidence.evidence_strength must match evidence.evidence_strength"
                )

        ctr = sig.get("confirmatory_test_refs")
        if not isinstance(ctr, list) or not ctr:
            errors.append(f"{prefix}.confirmatory_test_refs must be a non-empty list")
        else:
            for ti, t in enumerate(ctr):
                tl = f"{prefix}.confirmatory_test_refs[{ti}]"
                if not isinstance(t, dict):
                    errors.append(f"{tl} must be a map")
                    continue
                tid = t.get("test_id")
                if not isinstance(tid, str) or not tid.startswith("ct_"):
                    errors.append(f"{tl}.test_id must match ct_*")
                tr = t.get("rationale")
                if not isinstance(tr, str) or len(tr.strip()) < 10:
                    errors.append(f"{tl}.rationale min_length 10")

        orules = sig.get("override_rules")
        if not isinstance(orules, list) or not orules:
            errors.append(f"{prefix}.override_rules must be a non-empty list")
        else:
            for oi, rule in enumerate(orules):
                ol = f"{prefix}.override_rules[{oi}]"
                if not isinstance(rule, dict):
                    errors.append(f"{ol} must be a map")
                    continue
                for req in ("rule_id", "resulting_state", "description", "conditions", "source_refs"):
                    if req not in rule:
                        errors.append(f"{ol}.{req} required")
                rid = rule.get("rule_id")
                if not isinstance(rid, str) or not rid.startswith("or_"):
                    errors.append(f"{ol}.rule_id must match or_*")
                if rule.get("resulting_state") != "at_risk":
                    errors.append(f"{ol}.resulting_state must be 'at_risk'")
                desc = rule.get("description")
                if not isinstance(desc, str) or len(desc.strip()) < 10:
                    errors.append(f"{ol}.description min_length 10")
                srs = rule.get("source_refs")
                if not isinstance(srs, list) or not srs:
                    errors.append(f"{ol}.source_refs must be a non-empty list")
                else:
                    for si2, s in enumerate(srs):
                        if not isinstance(s, str) or not s.startswith("source_"):
                            errors.append(f"{ol}.source_refs[{si2}] must match source_*")
                _validate_override_conditions(rule.get("conditions"), ol, errors)

        b2 = sig.get("bucket2_homes")
        if b2 is not None and not isinstance(b2, dict):
            errors.append(f"{prefix}.bucket2_homes must be a map when present")

    _ = source_path  # reserved for future path-relative diagnostics


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Validate promoted_signal_intelligence.yaml (contract v1).")
    p.add_argument("--model", required=True, help="Path to promoted_signal_intelligence.yaml")
    p.add_argument(
        "--schema",
        default=str(DEFAULT_SCHEMA_PATH),
        help="Path to promoted_signal_intelligence_schema_v1.yaml",
    )
    p.add_argument("--audit-path", default=str(DEFAULT_AUDIT_PATH))
    args = p.parse_args(argv if argv is not None else sys.argv[1:])

    model_path = Path(args.model).resolve()
    schema_path = Path(args.schema).resolve()
    audit_path = Path(args.audit_path).resolve()

    errors: list[str] = []
    doc, e1 = _load_yaml(model_path)
    errors.extend(e1)
    schema_doc, e2 = _load_yaml(schema_path)
    errors.extend(e2)

    if doc is not None and isinstance(doc, dict) and isinstance(schema_doc, dict):
        validate_promoted_signal_intelligence(doc, schema_doc=schema_doc, source_path=model_path, errors=errors)

    status = "FAIL" if errors else "PASS"
    _write_audit(audit_path, status, errors)
    print(f"validation_status: {status}")
    print(f"audit_path: {audit_path}")
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
