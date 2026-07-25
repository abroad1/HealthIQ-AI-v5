#!/usr/bin/env python3
"""
P3-LAYERB-INTEL-1 — Layer B integrity gate.

Detects:
- wrong-frame prose attachment
- unsupported modifier combinations (contradiction fail-safe probe)
- missing provenance on routing decisions
- false production status / candidate imports
- frame-specific WHY bound to family-level-only authority mismatch probes
- non-deterministic routing
- MR-BATCH production isolation breach
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO = Path(__file__).resolve().parents[2]
BACKEND = REPO / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from core.knowledge.layer_b_asset_authority_v1 import (  # noqa: E402
    FORBIDDEN_PRODUCTION,
    assert_production_allowed,
    load_layer_b_asset_authority,
    mr_batch_isolated,
)
from core.knowledge.layer_b_frame_routing_v1 import (  # noqa: E402
    ProseAssetCandidate,
    select_frame_prose_asset,
)
from core.knowledge.layer_b_modifier_binder_v1 import bind_modifiers_v1  # noqa: E402


def _scan_production_imports_for_mr_batch() -> List[str]:
    """
    Fail if production code imports the candidate-prose test harness module.
    Docstring / YAML governance mentions of the batch id are allowed.
    """
    errors: List[str] = []
    banned_import_needles = (
        "mr_candidate_prose_test_v1",
        "MR_BATCH_001B_candidate_prose_assets",
        "from tests.support.mr_candidate",
        "import mr_candidate_prose",
    )
    roots = [REPO / "backend" / "core", REPO / "backend" / "app", REPO / "frontend" / "app"]
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.suffix.lower() not in {".py", ".ts", ".tsx", ".js", ".jsx"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            for needle in banned_import_needles:
                if needle in text:
                    errors.append(f"production_import:{path.relative_to(REPO)} contains {needle}")
    return errors


def main() -> int:
    errors: List[str] = []
    warnings: List[str] = []

    reg = load_layer_b_asset_authority()
    if not mr_batch_isolated(reg):
        errors.append("MR-BATCH-001B not isolated as test_only in layer_b_asset_authority_v1")
    errors.extend(_scan_production_imports_for_mr_batch())

    for row in reg.get("assets") or []:
        if not isinstance(row, dict):
            continue
        aid = str(row.get("asset_id") or "").strip()
        auth = str(row.get("production_authority") or "").strip().lower()
        if auth in FORBIDDEN_PRODUCTION and row.get("production_import_allowed") is True:
            errors.append(f"false_production_status:{aid} forbidden authority but import allowed")
        if auth in {"pending_medical_review", "candidate", "test_only"}:
            try:
                assert_production_allowed(aid, reg)
                errors.append(f"assert_production_allowed unexpectedly passed for {aid}")
            except PermissionError:
                pass

    # Wrong-frame probe
    frame_a = "signal_alt_high::frame_a"
    frame_b = "signal_alt_high::frame_b"
    cands = [
        ProseAssetCandidate(
            asset_id="prose_frame_a",
            signal_id="signal_alt_high",
            activation_keys=(frame_a,),
            production_authority="approved",
        ),
        ProseAssetCandidate(
            asset_id="prose_frame_b",
            signal_id="signal_alt_high",
            activation_keys=(frame_b,),
            production_authority="approved",
        ),
    ]
    d_a = select_frame_prose_asset(
        candidates=cands, signal_id="signal_alt_high", activation_key=frame_a
    )
    d_b = select_frame_prose_asset(
        candidates=cands, signal_id="signal_alt_high", activation_key=frame_b
    )
    if d_a.selected_asset_id != "prose_frame_a":
        errors.append(f"wrong_frame_probe: expected prose_frame_a got {d_a.selected_asset_id}")
    if d_b.selected_asset_id != "prose_frame_b":
        errors.append(f"wrong_frame_probe: expected prose_frame_b got {d_b.selected_asset_id}")
    if d_a.selected_asset_id == d_b.selected_asset_id:
        errors.append("wrong_frame_probe: distinct frames collapsed to same prose")

    # Candidate rejection probe
    cand_only = [
        ProseAssetCandidate(
            asset_id="mr_batch_like",
            signal_id="signal_alt_high",
            production_authority="candidate",
        )
    ]
    d_c = select_frame_prose_asset(
        candidates=cand_only, signal_id="signal_alt_high", activation_key=frame_a
    )
    if d_c.selected_asset_id is not None:
        errors.append("candidate_asset_loaded_in_production_probe")

    # Missing provenance probe
    if not d_a.routing_policy_version or not d_a.fallback_authority:
        errors.append("missing_routing_provenance")

    # Modifier contradiction fail-safe
    rows = [
        {
            "modifier_id": "mod_x",
            "runtime_active": True,
            "production_authority": "approved",
            "exclusive_group": "g1",
        },
        {
            "modifier_id": "mod_y",
            "runtime_active": True,
            "production_authority": "approved",
            "exclusive_group": "g1",
        },
    ]
    bound = bind_modifiers_v1(catalogue_rows=rows, eligible_modifier_ids=["mod_x", "mod_y"])
    if bound.selected_modifier_ids:
        errors.append(f"contradiction_fail_safe_failed:{bound.selected_modifier_ids}")

    # Non-determinism probe
    for _ in range(5):
        again = select_frame_prose_asset(
            candidates=cands, signal_id="signal_alt_high", activation_key=frame_a
        )
        if again.as_dict() != d_a.as_dict():
            errors.append("non_deterministic_routing")
            break

    # Family-level WHY honesty probe: family asset must be labelled LEGACY_FAMILY_LEVEL
    family = [
        ProseAssetCandidate(
            asset_id="family_why",
            signal_id="signal_alt_high",
            production_authority="legacy_unreviewed",
        )
    ]
    d_f = select_frame_prose_asset(
        candidates=family,
        signal_id="signal_alt_high",
        activation_key="signal_alt_high::frame_a",
    )
    if d_f.fallback_authority != "LEGACY_FAMILY_LEVEL":
        errors.append(f"family_fallback_not_labelled:{d_f.fallback_authority}")

    payload: Dict[str, Any] = {
        "errors": errors,
        "warnings": warnings,
        "registry_assets": len(reg.get("assets") or []),
    }
    print(json.dumps(payload, indent=2))
    if errors:
        print("layer_b_integrity_gate: FAIL", file=sys.stderr)
        for e in errors:
            print(f"  error: {e}", file=sys.stderr)
        return 1
    print("layer_b_integrity_gate: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
