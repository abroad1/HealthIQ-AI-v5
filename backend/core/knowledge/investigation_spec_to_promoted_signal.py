"""
Deterministic translation: investigation spec v3.0.0 → promoted signal intelligence v1.

Hypotheses, hypothesis_ranking, and narrative are intentionally excluded (KB-S47d).
Adjacent hypothesis assets must reference owning signal_id.

Authority: ADR-008, promoted_signal_intelligence_schema_v1.yaml
"""

from __future__ import annotations

import copy
from typing import Any


INV_CONTRACT = "3.0.0"
PROMOTED_CONTRACT = "1.0.0"


def translate_investigation_spec_v3_to_promoted_signals(
    investigation_spec: dict[str, Any],
    *,
    package_id: str,
) -> dict[str, Any]:
    """
    Reduce one investigation-spec document (v3) to a promoted_signal_intelligence root map.

    One investigation spec yields exactly one entry in ``signals``.
    """
    if not isinstance(investigation_spec, dict):
        raise TypeError("investigation_spec must be a mapping")
    ver = investigation_spec.get("investigation_spec_contract_version")
    if ver != INV_CONTRACT:
        raise ValueError(
            f"investigation_spec_contract_version must be '{INV_CONTRACT}' (got {ver!r})"
        )

    signal = _translate_single_spec_to_signal(investigation_spec)

    return {
        "promoted_signal_intelligence_contract_version": PROMOTED_CONTRACT,
        "schema_version": PROMOTED_CONTRACT,
        "package_id": package_id,
        "translation": {
            "source": "investigation_spec_v3",
            "investigation_spec_contract_version": INV_CONTRACT,
            "investigation_spec_id": investigation_spec.get("spec_id"),
            "signal_id": investigation_spec.get("signal_id"),
        },
        "signals": [signal],
    }


def _translate_single_spec_to_signal(inv: dict[str, Any]) -> dict[str, Any]:
    primary = inv.get("primary_marker")
    if not isinstance(primary, dict):
        raise ValueError("primary_marker must be a map")

    biomarker_id = primary.get("biomarker_id")
    if not isinstance(biomarker_id, str) or not biomarker_id.strip():
        raise ValueError("primary_marker.biomarker_id required")

    rationale = primary.get("rationale")
    if not isinstance(rationale, str):
        raise ValueError("primary_marker.rationale required")

    signal_system = primary.get("signal_system")
    if not isinstance(signal_system, str) or not signal_system.strip():
        signal_system = "other"

    hypotheses = inv.get("hypotheses")
    if not isinstance(hypotheses, list) or len(hypotheses) < 1:
        raise ValueError("hypotheses must be a non-empty list")

    ranked = sorted(
        [h for h in hypotheses if isinstance(h, dict)],
        key=lambda h: int(h.get("rank", 0)),
    )

    contradiction_markers: list[dict[str, Any]] = []
    seen_ctr: set[str] = set()
    for hyp in ranked:
        cms = hyp.get("contradiction_markers")
        if not isinstance(cms, list):
            continue
        for cm in cms:
            if not isinstance(cm, dict):
                continue
            cid = cm.get("contradiction_id")
            if not isinstance(cid, str) or cid in seen_ctr:
                continue
            seen_ctr.add(cid)
            contradiction_markers.append(copy.deepcopy(cm))

    policies_set: set[str] = set()
    for hyp in ranked:
        md = hyp.get("missing_data")
        if isinstance(md, dict):
            pol = md.get("policy")
            if isinstance(pol, str) and pol.strip():
                policies_set.add(pol.strip())
    policies = sorted(policies_set)
    if not policies:
        policies = ["explicit_unknown_allowed"]

    supporting = inv.get("supporting_markers")
    if not isinstance(supporting, list) or not supporting:
        raise ValueError("supporting_markers must be a non-empty list")
    supporting_markers = copy.deepcopy(supporting)

    evidence = inv.get("evidence")
    if not isinstance(evidence, dict):
        raise ValueError("evidence must be a map")
    evidence_strength = evidence.get("evidence_strength")
    if evidence_strength is None:
        raise ValueError("evidence.evidence_strength required")

    evidence_out = {
        "evidence_strength": evidence_strength,
        "physiological_claim": evidence.get("physiological_claim"),
        "threshold_notes": evidence.get("threshold_notes", ""),
    }
    if "sources" in evidence:
        evidence_out["sources"] = copy.deepcopy(evidence["sources"])

    ct = inv.get("confirmatory_tests")
    if not isinstance(ct, list) or not ct:
        raise ValueError("confirmatory_tests must be a non-empty list")
    confirmatory_test_refs = []
    for item in ct:
        if not isinstance(item, dict):
            continue
        confirmatory_test_refs.append(
            {
                "test_id": item.get("test_id"),
                "rationale": item.get("rationale"),
            }
        )
    if not confirmatory_test_refs:
        raise ValueError("confirmatory_tests contained no valid entries")

    orules = inv.get("override_rules")
    if not isinstance(orules, list) or not orules:
        raise ValueError("override_rules must be a non-empty list")

    sig_id = inv.get("signal_id")
    if not isinstance(sig_id, str) or not sig_id.strip():
        raise ValueError("signal_id required")

    rd = inv.get("research_domain")
    if not isinstance(rd, str) or not rd.strip():
        raise ValueError("research_domain required")

    td = inv.get("trigger_direction")
    if td not in ("high", "low", "both"):
        raise ValueError("trigger_direction must be high, low, or both")

    return {
        "signal_id": sig_id,
        "research_domain": rd,
        "signal_system": signal_system,
        "primary_metric": {
            "biomarker_id": biomarker_id.strip(),
            "rationale": rationale,
        },
        "trigger_direction": td,
        "activation": copy.deepcopy(inv.get("activation")),
        "states": copy.deepcopy(inv.get("states")),
        "supporting_markers": supporting_markers,
        "contradiction_markers": contradiction_markers,
        "missing_data": {"policies": policies},
        "confidence": {"evidence_strength": evidence_strength},
        "override_rules": copy.deepcopy(orules),
        "evidence": evidence_out,
        "confirmatory_test_refs": confirmatory_test_refs,
    }
