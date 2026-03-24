#!/usr/bin/env python3
"""
Validate Knowledge Bus intelligence_model.yaml (target schema v1).

Deterministic structural checks only — no heuristics.
Authority: docs/architecture/HealthIQ_Intelligence_Model_Design_Second_Pass.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCHEMA_PATH = ROOT / "knowledge_bus" / "schema" / "intelligence_model_schema_v1.yaml"
DEFAULT_AUDIT_PATH = ROOT / "backend" / "artifacts" / "intelligence_model_audit.md"

SCHEMA_VERSION = "1.0.0"

_FORBIDDEN_SIGNAL_KEYS = frozenset(
    {"rendering", "presentation", "display", "report_layout", "ui_hints"}
)

_TRIGGER_DIRECTIONS = frozenset({"high", "low", "bidirectional", "context_dependent"})
_ROLES = frozenset(
    {"mechanism_marker", "severity_marker", "contextual_marker", "corroborator", "differential_marker"}
)
_REL_KINDS = frozenset({"mechanism", "corroboration", "severity", "differential"})
_REL_TO_ROLE = {
    "mechanism": frozenset({"mechanism_marker", "contextual_marker"}),
    "corroboration": frozenset({"corroborator"}),
    "severity": frozenset({"severity_marker"}),
    "differential": frozenset({"differential_marker"}),
}
_EXPECTED_DIRECTIONS = frozenset({"high", "low", "any"})
_AVAILABILITY = frozenset({"common", "specialist", "optional"})
_EVIDENCE_STRENGTH = frozenset({"exploratory", "moderate", "strong", "consensus"})
_CONTRA_STRENGTH = frozenset({"weak", "moderate", "strong"})

_FALLBACK_INTERVENTION_CLASS_IDS = frozenset(
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
_FALLBACK_INTERVENTION_RELATION_TYPES = frozenset(
    {
        "interpretation_confounder",
        "expected_biomarker_effect",
        "monitoring_relevance",
        "caveat_only",
    }
)
_FALLBACK_INTERVENTION_REF_KEY_FRAGMENTS = (
    "threshold",
    "override_signal",
    "signal_state_mutation",
    "activation_override",
    "lab_range_modify",
    "firing_rule",
    "deterministic_threshold_change",
)


def _intervention_class_ids(schema_doc: dict[str, Any]) -> frozenset[str]:
    raw = schema_doc.get("intervention_class_id_allowed")
    if isinstance(raw, list) and raw:
        return frozenset(str(x) for x in raw)
    return _FALLBACK_INTERVENTION_CLASS_IDS


def _intervention_relation_types(schema_doc: dict[str, Any]) -> frozenset[str]:
    raw = schema_doc.get("intervention_relation_type_allowed")
    if isinstance(raw, list) and raw:
        return frozenset(str(x) for x in raw)
    return _FALLBACK_INTERVENTION_RELATION_TYPES


def _intervention_ref_allowed_keyset(schema_doc: dict[str, Any]) -> frozenset[str]:
    raw = schema_doc.get("intervention_reference_allowed_keys")
    if isinstance(raw, list) and raw:
        return frozenset(str(x) for x in raw)
    return frozenset({"intervention_class_id", "relation_type"})


def _intervention_ref_forbidden_frags(schema_doc: dict[str, Any]) -> tuple[str, ...]:
    raw = schema_doc.get("forbidden_intervention_reference_key_fragments")
    if isinstance(raw, list) and raw:
        return tuple(str(x) for x in raw)
    return _FALLBACK_INTERVENTION_REF_KEY_FRAGMENTS


def _validate_hypothesis_intervention_references(
    hyp: dict[str, Any],
    hp: str,
    *,
    schema_doc: dict[str, Any],
    errors: list[str],
) -> None:
    refs = hyp.get("intervention_references")
    if refs is None:
        return
    if not isinstance(refs, list):
        errors.append(f"{hp}.intervention_references must be a list when present")
        return
    if len(refs) < 1:
        errors.append(
            f"{hp}.intervention_references must contain at least one entry when present "
            "(omit the field if there are no links)"
        )
        return

    allowed_keys = _intervention_ref_allowed_keyset(schema_doc)
    class_ids = _intervention_class_ids(schema_doc)
    rel_types = _intervention_relation_types(schema_doc)
    frags = _intervention_ref_forbidden_frags(schema_doc)

    for ri, item in enumerate(refs):
        rp = f"{hp}.intervention_references[{ri}]"
        if not isinstance(item, dict):
            errors.append(f"{rp} must be a map")
            continue
        got_keys = frozenset(item.keys())
        if got_keys != allowed_keys:
            errors.append(
                f"{rp} must contain exactly keys {sorted(allowed_keys)} (found {sorted(got_keys)})"
            )
            continue
        for key in item:
            low = key.lower()
            for frag in frags:
                if frag in low:
                    errors.append(
                        f"{rp}: key '{key}' contains forbidden fragment '{frag}' "
                        "(intervention link must not encode threshold/signal mutation)"
                    )
        cid = item.get("intervention_class_id")
        if not isinstance(cid, str) or cid not in class_ids:
            errors.append(
                f"{rp}.intervention_class_id must be one of {sorted(class_ids)}"
            )
        rt = item.get("relation_type")
        if not isinstance(rt, str) or rt not in rel_types:
            errors.append(
                f"{rp}.relation_type must be one of {sorted(rel_types)}"
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
        "# Intelligence Model Audit",
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


def _bucket2_keys_from_schema(schema: dict[str, Any]) -> list[str]:
    raw = schema.get("future_bucket2_homes_required_keys")
    if isinstance(raw, list):
        return [str(x) for x in raw]
    return []


def validate_intelligence_model(
    doc: dict[str, Any],
    *,
    schema_doc: dict[str, Any],
    source_path: Path,
    errors: list[str],
) -> None:
    if not isinstance(doc, dict):
        errors.append("Root must be a map")
        return

    for key in schema_doc.get("forbidden_root_keys") or []:
        if key in doc:
            errors.append(f"Forbidden root key (reasoning/rendering separation): {key}")

    ver = doc.get("schema_version")
    if ver != SCHEMA_VERSION:
        errors.append(
            f"schema_version must be '{SCHEMA_VERSION}' for target schema v1 (got {ver!r})"
        )

    pid = doc.get("package_id")
    if not isinstance(pid, str) or not pid.strip():
        errors.append("package_id must be a non-empty string")

    signals = doc.get("signals")
    if not isinstance(signals, list) or not signals:
        errors.append("signals must be a non-empty list")
        return

    bucket2_keys = _bucket2_keys_from_schema(schema_doc)

    for si, sig in enumerate(signals):
        prefix = f"signals[{si}]"
        if not isinstance(sig, dict):
            errors.append(f"{prefix} must be a map")
            continue

        for fk in _FORBIDDEN_SIGNAL_KEYS:
            if fk in sig:
                errors.append(f"{prefix} must not contain rendering key '{fk}'")

        sid = sig.get("signal_id")
        if not isinstance(sid, str) or not sid.strip():
            errors.append(f"{prefix}.signal_id must be a non-empty string")

        td = sig.get("trigger_direction")
        if td not in _TRIGGER_DIRECTIONS:
            errors.append(
                f"{prefix}.trigger_direction must be one of {sorted(_TRIGGER_DIRECTIONS)}"
            )

        pb = sig.get("primary_biomarker")
        if not isinstance(pb, str) or not pb.strip():
            errors.append(f"{prefix}.primary_biomarker must be a non-empty string")

        hyp_list = sig.get("hypotheses")
        if not isinstance(hyp_list, list):
            errors.append(f"{prefix}.hypotheses must be a list")
            continue
        if len(hyp_list) < 2:
            errors.append(
                f"{prefix}.hypotheses must contain at least 2 structured hypotheses "
                "(single-explanation blobs are not valid for target schema v1)"
            )

        hypo_ids: list[str] = []
        has_differential_support = False

        for hi, hyp in enumerate(hyp_list):
            hp = f"{prefix}.hypotheses[{hi}]"
            if not isinstance(hyp, dict):
                errors.append(f"{hp} must be a map")
                continue

            hid = hyp.get("hypothesis_id")
            if not isinstance(hid, str) or not hid.strip():
                errors.append(f"{hp}.hypothesis_id must be a non-empty string")
            else:
                hypo_ids.append(hid.strip())

            rank = hyp.get("rank")
            if not isinstance(rank, int) or rank < 1:
                errors.append(f"{hp}.rank must be a positive integer")

            claim = hyp.get("physiological_claim")
            if not isinstance(claim, str) or len(claim.strip()) < 10:
                errors.append(f"{hp}.physiological_claim must be a string with min_length 10")

            evs = hyp.get("evidence_strength")
            if evs not in _EVIDENCE_STRENGTH:
                errors.append(
                    f"{hp}.evidence_strength must be one of {sorted(_EVIDENCE_STRENGTH)}"
                )

            cav = hyp.get("caveats")
            if not isinstance(cav, list):
                errors.append(f"{hp}.caveats must be a list")
            else:
                for ci, c in enumerate(cav):
                    if not isinstance(c, str) or not c.strip():
                        errors.append(f"{hp}.caveats[{ci}] must be a non-empty string")

            md = hyp.get("missing_data")
            if not isinstance(md, dict):
                errors.append(f"{hp}.missing_data must be a map (structured home)")
            else:
                if "policy" not in md:
                    errors.append(f"{hp}.missing_data.policy is required")

            sms = hyp.get("supporting_markers")
            if not isinstance(sms, list) or not sms:
                errors.append(f"{hp}.supporting_markers must be a non-empty list of objects")
            else:
                for j, row in enumerate(sms):
                    sml = f"{hp}.supporting_markers[{j}]"
                    if isinstance(row, str):
                        errors.append(
                            f"{sml} must be an object, not a string (flat lists are forbidden)"
                        )
                        continue
                    if not isinstance(row, dict):
                        errors.append(f"{sml} must be a map")
                        continue

                    bid = row.get("biomarker_id")
                    if not isinstance(bid, str) or not bid.strip():
                        errors.append(f"{sml}.biomarker_id must be a non-empty string")

                    ed = row.get("expected_direction")
                    if ed not in _EXPECTED_DIRECTIONS:
                        errors.append(
                            f"{sml}.expected_direction must be one of {sorted(_EXPECTED_DIRECTIONS)}"
                        )

                    role = row.get("role")
                    if role not in _ROLES:
                        errors.append(f"{sml}.role must be one of {sorted(_ROLES)}")

                    rk = row.get("relationship_kind")
                    if rk not in _REL_KINDS:
                        errors.append(
                            f"{sml}.relationship_kind must be one of {sorted(_REL_KINDS)}"
                        )
                    elif role in _ROLES and rk in _REL_TO_ROLE:
                        if role not in _REL_TO_ROLE[rk]:
                            errors.append(
                                f"{sml}.role '{role}' is incompatible with "
                                f"relationship_kind '{rk}' for target schema v1"
                            )
                    if rk == "differential":
                        has_differential_support = True

                    av = row.get("availability")
                    if av not in _AVAILABILITY:
                        errors.append(
                            f"{sml}.availability must be one of {sorted(_AVAILABILITY)}"
                        )

                    rat = row.get("rationale")
                    if rat is not None and (not isinstance(rat, str)):
                        errors.append(f"{sml}.rationale must be a string when present")

            cms = hyp.get("contradiction_markers")
            if not isinstance(cms, list):
                errors.append(f"{hp}.contradiction_markers must be a list (may be empty)")
            else:
                for ci, cm in enumerate(cms):
                    cml = f"{hp}.contradiction_markers[{ci}]"
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
                            errors.append(f"{cml}.{fld} is required")
                    cr = cm.get("contradiction_rationale")
                    if isinstance(cr, str) and len(cr.strip()) < 10:
                        errors.append(f"{cml}.contradiction_rationale min_length 10")
                    cs = cm.get("contradiction_strength")
                    if cs not in _CONTRA_STRENGTH:
                        errors.append(
                            f"{cml}.contradiction_strength must be one of {sorted(_CONTRA_STRENGTH)}"
                        )

            _validate_hypothesis_intervention_references(
                hyp, hp, schema_doc=schema_doc, errors=errors
            )

        if hypo_ids and len(hypo_ids) != len(set(hypo_ids)):
            errors.append(f"{prefix}: duplicate hypothesis_id values")

        if not has_differential_support:
            errors.append(
                f"{prefix}: at least one supporting_markers[].relationship_kind must be "
                "'differential' (differential reasoning must be first-class in v1)"
            )

        hr = sig.get("hypothesis_ranking")
        if hr is not None:
            if not isinstance(hr, dict):
                errors.append(f"{prefix}.hypothesis_ranking must be a map when present")
            else:
                oids = hr.get("ordered_hypothesis_ids")
                if not isinstance(oids, list) or [x for x in oids if not isinstance(x, str)]:
                    errors.append(
                        f"{prefix}.hypothesis_ranking.ordered_hypothesis_ids must be a list of strings"
                    )
                elif sorted(oids) != sorted(hypo_ids):
                    errors.append(
                        f"{prefix}.hypothesis_ranking.ordered_hypothesis_ids must match hypotheses"
                    )

        prov = sig.get("provenance")
        if not isinstance(prov, dict):
            errors.append(f"{prefix}.provenance must be a map")
        else:
            es = prov.get("evidence_source_ids")
            if not isinstance(es, list) or [x for x in es if not isinstance(x, str)]:
                errors.append(
                    f"{prefix}.provenance.evidence_source_ids must be a list of strings"
                )
            rpr = prov.get("rule_provenance_refs")
            if not isinstance(rpr, list) or [x for x in rpr if not isinstance(x, str)]:
                errors.append(
                    f"{prefix}.provenance.rule_provenance_refs must be a list of strings"
                )

        lmin = sig.get("longitudinal_minimum")
        if not isinstance(lmin, dict):
            errors.append(f"{prefix}.longitudinal_minimum must be a map")
        else:
            for fld in ("stable_identity_key", "snapshot_timestamp", "signal_state_snapshot"):
                if fld not in lmin:
                    errors.append(f"{prefix}.longitudinal_minimum.{fld} key is required (nullable allowed)")

        fb2 = sig.get("future_bucket2_homes")
        if not isinstance(fb2, dict):
            errors.append(f"{prefix}.future_bucket2_homes must be a map")
        elif bucket2_keys:
            for k in bucket2_keys:
                if k not in fb2:
                    errors.append(f"{prefix}.future_bucket2_homes missing key '{k}'")

        ct = sig.get("confirmatory_tests")
        if ct is not None:
            if not isinstance(ct, list):
                errors.append(f"{prefix}.confirmatory_tests must be a list when present")
            else:
                for ti, t in enumerate(ct):
                    if not isinstance(t, dict):
                        errors.append(f"{prefix}.confirmatory_tests[{ti}] must be a map")
                        continue
                    if not isinstance(t.get("test_id"), str) or not str(t.get("test_id")).strip():
                        errors.append(f"{prefix}.confirmatory_tests[{ti}].test_id required")
                    rat = t.get("rationale")
                    if not isinstance(rat, str) or len(rat.strip()) < 5:
                        errors.append(
                            f"{prefix}.confirmatory_tests[{ti}].rationale must be a substantive string"
                        )

        if "contradiction_markers" in sig:
            errors.append(
                f"{prefix}: contradiction_markers must not appear at signal level "
                "(hypothesis-level attachment only)"
            )

    # unused but documents intent
    _ = source_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate intelligence_model.yaml (target schema v1).")
    parser.add_argument("--model", required=True, help="Path to intelligence_model.yaml")
    parser.add_argument(
        "--schema",
        default=str(DEFAULT_SCHEMA_PATH),
        help="Path to intelligence_model_schema_v1.yaml",
    )
    parser.add_argument(
        "--audit-path",
        default=str(DEFAULT_AUDIT_PATH),
        help="Audit markdown output path.",
    )
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    model_path = Path(args.model).resolve()
    schema_path = Path(args.schema).resolve()
    audit_path = Path(args.audit_path).resolve()

    errors: list[str] = []
    doc, e1 = _load_yaml(model_path)
    errors.extend(e1)
    schema_doc, e2 = _load_yaml(schema_path)
    errors.extend(e2)

    if not errors and isinstance(doc, dict) and isinstance(schema_doc, dict):
        validate_intelligence_model(doc, schema_doc=schema_doc, source_path=model_path, errors=errors)

    status = "FAIL" if errors else "PASS"
    _write_audit(audit_path, status, errors)

    print(f"validation_status: {status}")
    print(f"errors: {len(errors)}")
    print(f"audit_path: {audit_path}")
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
