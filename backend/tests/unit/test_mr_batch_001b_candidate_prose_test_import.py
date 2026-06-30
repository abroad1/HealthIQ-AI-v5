"""MR-BATCH-001B candidate prose test import — governance and output generation tests."""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from core.analytics import retail_explainer_assembly_v1
from core.insights.narrative_runtime_policy import resolve_narrative_llm_allow_llm
from core.pipeline import orchestrator
from tests.support.mr_candidate_prose_test_v1 import (
    compose_marker_state_prose,
    default_mr_batch_001b_pack_path,
    load_mr_batch_001b_candidate_pack,
    validate_pack_governance,
)

_REPO = Path(__file__).resolve().parents[3]
_OUTPUT_PATH = (
    _REPO
    / "docs"
    / "sprints"
    / "beta_readiness"
    / "MR-BATCH-001B_candidate_prose_test_output.md"
)


@pytest.fixture
def candidate_pack():
    return load_mr_batch_001b_candidate_pack(candidate_test_mode=True)


def test_mr_batch_001b_yaml_parses(candidate_pack) -> None:
    assert candidate_pack.batch_id == "MR-BATCH-001B"
    assert len(candidate_pack.assets) == 69


def test_mr_batch_001b_all_assets_remain_candidate(candidate_pack) -> None:
    statuses = {a.review_status for a in candidate_pack.assets}
    assert statuses == {"CANDIDATE"}


def test_mr_batch_001b_no_asset_marked_approved(candidate_pack) -> None:
    for asset in candidate_pack.assets:
        assert asset.review_status != "APPROVED"


def test_mr_batch_001b_no_prohibited_generic_wording(candidate_pack) -> None:
    violations = validate_pack_governance(candidate_pack)
    phrase_violations = [v for v in violations if "prohibited phrase" in v]
    assert phrase_violations == []


def test_mr_batch_001b_marker_state_assets_have_required_fields(candidate_pack) -> None:
    violations = [
        v
        for v in validate_pack_governance(candidate_pack)
        if any(
            token in v
            for token in (
                "missing context_dependencies",
                "missing interpretive_limitations",
                "invalid range_state",
            )
        )
    ]
    assert violations == []


def test_mr_batch_001b_loader_requires_candidate_test_mode() -> None:
    with pytest.raises(RuntimeError, match="candidate_test_mode=True"):
        load_mr_batch_001b_candidate_pack(candidate_test_mode=False)


def test_mr_batch_001b_not_imported_by_production_runtime_modules() -> None:
    production_modules = (
        retail_explainer_assembly_v1,
        orchestrator,
    )
    for module in production_modules:
        source = inspect.getsource(module)
        assert "mr_candidate_prose_test_v1" not in source
        assert "MR-BATCH-001B" not in source


def test_gemini_remains_inactive_for_narrative_path() -> None:
    decision = resolve_narrative_llm_allow_llm(orchestrator_explicit_allow_llm=False)
    assert decision.synthesizer_allow_llm is False


def test_mr_batch_001b_compose_representative_cases(candidate_pack) -> None:
    cases = [
        compose_marker_state_prose(
            candidate_pack, biomarker_id="cystatin_c", range_state="in_range"
        ),
        compose_marker_state_prose(
            candidate_pack, biomarker_id="cystatin_c", range_state="high"
        ),
        compose_marker_state_prose(
            candidate_pack, biomarker_id="cystatin_c", range_state="low"
        ),
        compose_marker_state_prose(
            candidate_pack, biomarker_id="uacr", range_state="in_range"
        ),
        compose_marker_state_prose(
            candidate_pack, biomarker_id="uacr", range_state="high"
        ),
        compose_marker_state_prose(
            candidate_pack, biomarker_id="white_blood_cells", range_state="high"
        ),
        compose_marker_state_prose(
            candidate_pack, biomarker_id="white_blood_cells", range_state="low"
        ),
        compose_marker_state_prose(
            candidate_pack,
            biomarker_id="creatine_kinase",
            range_state="high",
            modifier_asset_ids=[
                "lifestyle_exercise_creatinine_ck_fragment_v1_b",
                "medication_statin_lipid_context_fragment_v1_b",
            ],
        ),
        compose_marker_state_prose(
            candidate_pack, biomarker_id="calcium", range_state="high"
        ),
        compose_marker_state_prose(
            candidate_pack, biomarker_id="calcium", range_state="low"
        ),
        compose_marker_state_prose(
            candidate_pack, biomarker_id="cortisol", range_state="high"
        ),
        compose_marker_state_prose(
            candidate_pack, biomarker_id="cortisol", range_state="low"
        ),
        compose_marker_state_prose(
            candidate_pack, biomarker_id="shbg", range_state="high"
        ),
        compose_marker_state_prose(
            candidate_pack,
            biomarker_id="free_testosterone",
            range_state="in_range",
        ),
        compose_marker_state_prose(
            candidate_pack,
            missing_marker_asset_ids=["missing_hba1c_metabolic_context_v1_b"],
            include_base=False,
            include_marker_state=False,
        ),
        compose_marker_state_prose(
            candidate_pack,
            missing_marker_asset_ids=["missing_cystatin_c_renal_context_v1_b"],
            include_base=False,
            include_marker_state=False,
        ),
        compose_marker_state_prose(
            candidate_pack,
            biomarker_id="cystatin_c",
            range_state="in_range",
            resilience_asset_id="resilience_renal_stable_panel_qualifier_v1_b",
        ),
    ]
    for composed in cases:
        assert composed.asset_ids, f"no assets selected for {composed.biomarker_id}/{composed.range_state}"
        assert composed.rendered
        assert "General education only" not in composed.rendered


def test_mr_batch_001b_write_test_output_report(candidate_pack) -> None:
    """Generate human-readable candidate/test output artefact (not medically approved)."""
    cases = [
        ("Cystatin C in-range", "cystatin_c", "in_range", {}),
        ("Cystatin C high", "cystatin_c", "high", {}),
        ("Cystatin C low", "cystatin_c", "low", {}),
        ("UACR in-range", "uacr", "in_range", {}),
        ("UACR high", "uacr", "high", {}),
        ("WBC high", "white_blood_cells", "high", {}),
        ("WBC low", "white_blood_cells", "low", {}),
        (
            "Creatine kinase high + exercise/statin modifiers",
            "creatine_kinase",
            "high",
            {
                "modifier_asset_ids": [
                    "lifestyle_exercise_creatinine_ck_fragment_v1_b",
                    "medication_statin_lipid_context_fragment_v1_b",
                ]
            },
        ),
        ("Calcium high", "calcium", "high", {}),
        ("Calcium low", "calcium", "low", {}),
        ("Cortisol high (sampling-time limits in asset)", "cortisol", "high", {}),
        ("Cortisol low", "cortisol", "low", {}),
        ("SHBG high", "shbg", "high", {}),
        ("Free testosterone in-range", "free_testosterone", "in_range", {}),
        (
            "Missing HbA1c metabolic caveat",
            "",
            "",
            {
                "include_base": False,
                "include_marker_state": False,
                "missing_marker_asset_ids": ["missing_hba1c_metabolic_context_v1_b"],
            },
        ),
        (
            "Missing cystatin C renal caveat",
            "",
            "",
            {
                "include_base": False,
                "include_marker_state": False,
                "missing_marker_asset_ids": ["missing_cystatin_c_renal_context_v1_b"],
            },
        ),
        (
            "Positive resilience qualifier (renal stable panel) with cystatin C in-range",
            "cystatin_c",
            "in_range",
            {"resilience_asset_id": "resilience_renal_stable_panel_qualifier_v1_b"},
        ),
    ]

    lines = [
        "# MR-BATCH-001B — Candidate Prose Test Output",
        "",
        "**Status:** CANDIDATE / TEST-ONLY — not medically approved",
        f"**Source pack:** `docs/sprints/beta_readiness/MR-BATCH-001B_candidate_prose_assets.yaml`",
        "**Isolation:** Loaded only via `candidate_test_mode=True` test loader",
        "",
        "## Test cases run",
        "",
    ]

    unreachable: list[str] = []

    for title, biomarker_id, range_state, extras in cases:
        composed = compose_marker_state_prose(
            candidate_pack,
            biomarker_id=biomarker_id,
            range_state=range_state,
            **extras,
        )
        lines.append(f"### {title}")
        lines.append("")
        if not composed.asset_ids:
            unreachable.append(title)
            lines.append("_No assets reachable for this case with current scope mapping._")
            lines.append("")
            continue
        lines.append(f"- **Selected asset IDs:** {', '.join(composed.asset_ids)}")
        lines.append("")
        snippet = composed.rendered
        if len(snippet) > 1200:
            snippet = snippet[:1197] + "..."
        lines.append("```text")
        lines.append(snippet)
        lines.append("```")
        lines.append("")

    lines.extend(
        [
            "## Assets not reachable in this test pass",
            "",
        ]
    )
    if unreachable:
        for item in unreachable:
            lines.append(f"- {item}")
    else:
        lines.append("- None — all representative cases produced output.")

    lines.extend(
        [
            "",
            "## Loader / architecture limitations",
            "",
            "- Candidate pack remains in `docs/sprints/beta_readiness/`; production retail/pathway registries unchanged.",
            "- Test loader lives under `backend/tests/support/` and is not wired into orchestrator or `attach_retail_explainers_v1`.",
            "- Hybrid composition is test-side only; narrative compiler does not yet select MR candidate assets.",
            "- WBC scope uses `white_blood_cells` biomarker id; directional assets use `wbc_*` asset ids.",
            "- Glucose marker-state assets are not in MR-BATCH-001B; missing HbA1c caveat is composed standalone.",
            "",
            "## Candidate/test-only confirmation",
            "",
            "- All assets remain `review_status: CANDIDATE`.",
            "- No production runtime consumption without explicit `candidate_test_mode=True`.",
            "- Gemini narrative path remains inactive by default policy gates.",
            "",
            "## Recommended next engineering step",
            "",
            "Run medical review on MR-BATCH-001B, then design a promotion/import sprint that maps approved assets into governed packs with runtime selection behind an explicit candidate flag.",
            "",
        ]
    )

    _OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert _OUTPUT_PATH.exists()
