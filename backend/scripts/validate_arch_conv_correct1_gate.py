#!/usr/bin/env python3
"""
ARCH-CONV-CORRECT-1 — programme correction gate.

Fails if any of the four workstream closures regress:

WS1 — rejected-frame total inactivation
  - the REJECTED activation key is registered as runtime-ineligible;
  - it is absent from the signal registry;
  - it never survives ``SignalEvaluator.evaluate_all``;
  - an injected rejected row is dropped before the insight graph / report / interventions.

WS2 — legacy "methylation capacity" wording retirement
  - retired phrases are absent from runtime signal results, root-cause findings, compiled
    reports, frontend-facing IDL records, governed YAML hypothesis sources and Layer C source.

WS3 — MCV frame co-service control
  - anchor serves morphology context only and never carries causal hypotheses;
  - a specific frame serves causally only when its governed evidence gate is satisfied;
  - mutually ambiguous specific frames fall back to anchor context.

WS4 — Layer C medical-boundary closure
  - the frontend files named in the leakage inventory no longer contain the medical decision
    logic they were flagged for.

Exit code 0 = PASS, 1 = FAIL.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND = REPO_ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

REJECTED_KEY = "signal_homocysteine_high::inv_homocysteine_high_metabolic"

MCV_ANCHOR = "signal_mcv_high::inv_mcv_high_macrocytosis"
MCV_MEGALOBLASTIC = "signal_mcv_high::inv_mcv_high_megaloblastic_macrocytosis"
MCV_NONMEGALOBLASTIC = "signal_mcv_high::inv_mcv_high_nonmegaloblastic_macrocytosis"

#: Retired wording. Governed replacement lives in the ratified medical review pack.
RETIRED_PHRASES = (
    "methylation capacity",
    "methylation pathway pattern",
)

FAILURES: List[str] = []

# --- shared panel fixtures ------------------------------------------------------------

LAB_RANGES: Dict[str, Dict[str, float]] = {
    "homocysteine": {"min": 5.0, "max": 15.0},
    "mcv": {"min": 80.0, "max": 96.0},
    "folate": {"min": 3.9, "max": 26.8},
    "vitamin_b12": {"min": 197.0, "max": 771.0},
    "active_b12": {"min": 37.5, "max": 188.0},
    "ggt": {"min": 10.0, "max": 71.0},
    "alt": {"min": 0.0, "max": 41.0},
    "egfr": {"min": 90.0, "max": 120.0},
    "creatinine": {"min": 59.0, "max": 104.0},
}

#: The live UAT panel for analysis e34aaedf-b09f-42f0-8cc8-4653a00b4c10.
UAT_PANEL: Dict[str, float] = {
    "homocysteine": 16.2,
    "mcv": 99.5,
    "folate": 7.7,
    "vitamin_b12": 336.0,
    "active_b12": 139.2,
    "ggt": 30.0,
    "alt": 22.0,
    "egfr": 84.0,
    "creatinine": 90.0,
}


def _fail(workstream: str, msg: str) -> None:
    FAILURES.append(f"{workstream}: {msg}")


def _evaluate(panel: Dict[str, float]) -> List[Dict[str, Any]]:
    from core.analytics.signal_evaluator import SignalEvaluator, SignalRegistry

    registry = SignalRegistry()
    rows = SignalEvaluator(registry).evaluate_all(panel, {}, lab_ranges=LAB_RANGES)
    return [r.model_dump() for r in rows]


def _compile_root_cause(panel: Dict[str, float], rows: Sequence[Dict[str, Any]]):
    from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1

    return compile_root_cause_v1(
        signal_results=list(rows),
        biomarker_context={k: {"value": v} for k, v in panel.items()},
        input_reference_ranges=LAB_RANGES,
    )


# --- WS1 ----------------------------------------------------------------------------


def check_ws1_rejected_frame_inactivation() -> None:
    from core.analytics.signal_evaluator import SignalRegistry
    from core.knowledge.frame_runtime_authority_v1 import (
        clear_frame_runtime_authority_cache,
        is_frame_runtime_eligible,
        rejected_activation_keys,
    )

    clear_frame_runtime_authority_cache()

    if REJECTED_KEY not in rejected_activation_keys():
        _fail("WS1", f"{REJECTED_KEY} is not registered as a rejected activation key")
    if is_frame_runtime_eligible(REJECTED_KEY):
        _fail("WS1", f"{REJECTED_KEY} is still runtime-eligible")

    registry = SignalRegistry()
    if REJECTED_KEY in set(registry._signals_by_activation_key):
        _fail("WS1", f"{REJECTED_KEY} is present in the signal registry")
    if REJECTED_KEY not in {row["activation_key"] for row in registry.excluded_rejected_frames}:
        _fail("WS1", "registry did not record the rejected frame as excluded")

    rows = _evaluate({**UAT_PANEL, "homocysteine": 30.0})
    if REJECTED_KEY in {str(r.get("activation_key") or "") for r in rows}:
        _fail("WS1", "rejected frame survived evaluate_all")
    if not rows:
        _fail("WS1", "evaluation returned no signals; the probe panel is no longer meaningful")

    # Fail-closed re-assertion: a replayed / fixture row must not reach report assembly.
    injected = list(rows) + [
        {
            "signal_id": "signal_homocysteine_high",
            "activation_key": REJECTED_KEY,
            "source_spec_id": "inv_homocysteine_high_metabolic",
            "signal_state": "suboptimal",
            "confidence": 0.9,
            "primary_metric": "homocysteine",
            "system": "metabolic",
        }
    ]
    graph = _build_insight_graph(injected)
    if graph is None:
        _fail("WS1", "insight graph could not be built for the injected-row assertion")
        return

    blob = graph.model_dump_json() if hasattr(graph, "model_dump_json") else str(graph)
    if REJECTED_KEY in blob or "inv_homocysteine_high_metabolic" in blob:
        _fail("WS1", "rejected frame reached the insight graph payload")

    root = _compile_root_cause({**UAT_PANEL, "homocysteine": 30.0}, injected)
    if root is not None:
        keys = {f.activation_key for f in root.findings}
        if REJECTED_KEY in keys:
            _fail("WS1", "rejected frame produced a root-cause finding")


def _build_insight_graph(rows: Sequence[Dict[str, Any]]):
    from core.analytics.insight_graph_builder import build_insight_graph_v1

    return build_insight_graph_v1(
        analysis_id="arch-conv-correct-1-gate",
        scoring_result={},
        clustering_result={"clusters": []},
        input_reference_ranges=LAB_RANGES,
        filtered_biomarkers={k: {"value": v} for k, v in UAT_PANEL.items()},
        signal_results=list(rows),
    )


# --- WS2 ----------------------------------------------------------------------------

WS2_SOURCE_GLOBS = (
    ("knowledge_bus/root_cause/hypotheses", "*.yaml"),
    ("knowledge_bus/compiled/hypotheses", "*.yaml"),
    ("knowledge_bus/interpretation_display_layer_v1", "*.yaml"),
    ("knowledge_bus/packages", "signal_library.yaml"),
)

#: The rejected frame's own package and research spec keep their historical text on disk as
#: the audit record of what was rejected. WS1 proves that content is unreachable at runtime,
#: so the fingerprint scan excludes those two governed-history paths and instead asserts
#: absence from live runtime output.
WS2_EXCLUDED_PATHS = (
    REPO_ROOT / "knowledge_bus/packages/pkg_s24_homocysteine_high_metabolic",
    REPO_ROOT / "knowledge_bus/research/investigation_specs/inv_homocysteine_high_metabolic.yaml",
)


def check_ws2_retired_wording() -> None:
    rows = _evaluate({**UAT_PANEL, "homocysteine": 30.0})
    runtime_text = " ".join(str(r) for r in rows).lower()
    for phrase in RETIRED_PHRASES:
        if phrase in runtime_text:
            _fail("WS2", f"retired phrase {phrase!r} present in runtime signal results")

    root = _compile_root_cause({**UAT_PANEL, "homocysteine": 30.0}, rows)
    if root is not None:
        findings_text = " ".join(
            f"{h.hypothesis_id} {h.title} {h.summary}"
            for finding in root.findings
            for h in finding.hypotheses
        ).lower()
        for phrase in RETIRED_PHRASES:
            if phrase in findings_text:
                _fail("WS2", f"retired phrase {phrase!r} present in root-cause findings")

    for rel, pattern in WS2_SOURCE_GLOBS:
        base = REPO_ROOT / rel
        if not base.is_dir():
            continue
        for path in base.rglob(pattern):
            if any(str(path).startswith(str(excluded)) for excluded in WS2_EXCLUDED_PATHS):
                continue
            # Comments are non-runtime: a governance note may name a retired phrase in order
            # to record its retirement, so only YAML content lines are scanned.
            content = " ".join(
                line
                for line in path.read_text(encoding="utf-8", errors="ignore").lower().splitlines()
                if not line.strip().startswith("#")
            )
            for phrase in RETIRED_PHRASES:
                if phrase in content:
                    _fail("WS2", f"retired phrase {phrase!r} in {path.relative_to(REPO_ROOT)}")

    frontend = REPO_ROOT / "frontend" / "app"
    if frontend.is_dir():
        for path in list(frontend.rglob("*.ts")) + list(frontend.rglob("*.tsx")):
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
            for phrase in RETIRED_PHRASES:
                if phrase in text:
                    _fail("WS2", f"retired phrase {phrase!r} in {path.relative_to(REPO_ROOT)}")


# --- WS3 ----------------------------------------------------------------------------


def _mcv_roles(panel: Dict[str, float]) -> Dict[str, str]:
    rows = _evaluate(panel)
    root = _compile_root_cause(panel, rows)
    if root is None:
        return {}
    return {
        f.activation_key: f.why_role
        for f in root.findings
        if f.activation_key.startswith("signal_mcv_high::")
    }


def check_ws3_mcv_co_service() -> None:
    from core.knowledge.frame_co_service_v1 import (
        WHY_ROLE_CAUSAL,
        WHY_ROLE_MORPHOLOGY_CONTEXT,
        clear_frame_co_service_cache,
        load_frame_co_service_policy,
    )

    clear_frame_co_service_cache()
    load_frame_co_service_policy()

    # (a) no specific evidence — anchor context only, no causal MCV frame.
    roles = _mcv_roles(UAT_PANEL)
    if roles.get(MCV_ANCHOR) != WHY_ROLE_MORPHOLOGY_CONTEXT:
        _fail("WS3", f"unsupported panel: anchor role was {roles.get(MCV_ANCHOR)!r}")
    causal = [k for k, role in roles.items() if role == WHY_ROLE_CAUSAL]
    if causal:
        _fail("WS3", f"unsupported panel emitted causal MCV frames: {sorted(causal)}")

    # (b) megaloblastic supported by low folate.
    roles = _mcv_roles({**UAT_PANEL, "folate": 2.1})
    if roles.get(MCV_MEGALOBLASTIC) != WHY_ROLE_CAUSAL:
        _fail("WS3", f"low folate did not make megaloblastic causal: {roles}")
    if roles.get(MCV_ANCHOR) != WHY_ROLE_MORPHOLOGY_CONTEXT:
        _fail("WS3", "anchor must stay morphology context when a specific frame serves")
    if roles.get(MCV_NONMEGALOBLASTIC) == WHY_ROLE_CAUSAL:
        _fail("WS3", "non-megaloblastic served causally without its evidence gate")

    # (c) non-megaloblastic supported by raised GGT.
    roles = _mcv_roles({**UAT_PANEL, "ggt": 120.0})
    if roles.get(MCV_NONMEGALOBLASTIC) != WHY_ROLE_CAUSAL:
        _fail("WS3", f"raised GGT did not make non-megaloblastic causal: {roles}")
    if roles.get(MCV_MEGALOBLASTIC) == WHY_ROLE_CAUSAL:
        _fail("WS3", "megaloblastic served causally without its evidence gate")

    # (d) both supported — no ratified combined pattern, so anchor context only.
    roles = _mcv_roles({**UAT_PANEL, "folate": 2.1, "ggt": 120.0})
    causal = [k for k, role in roles.items() if role == WHY_ROLE_CAUSAL]
    if causal:
        _fail("WS3", f"ambiguous panel emitted causal MCV frames: {sorted(causal)}")
    if roles.get(MCV_ANCHOR) != WHY_ROLE_MORPHOLOGY_CONTEXT:
        _fail("WS3", "ambiguous panel must fall back to anchor morphology context")


# --- WS4 ----------------------------------------------------------------------------

FRONTEND = REPO_ROOT / "frontend"


def _read_frontend(rel: str) -> str:
    path = FRONTEND / rel
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def check_ws4_layer_c_boundary() -> None:
    results_page = _read_frontend("app/(app)/results/page.tsx")
    if not results_page:
        _fail("WS4", "results page not found")
        return

    if "pickHeroAlignedPrimaryDriver" in results_page or "pickSeverityPrimaryDriverCluster" in results_page:
        _fail("WS4", "results page still arbitrates its own primary driver")
    if "selectGovernedPrimaryDriver" not in results_page:
        _fail("WS4", "results page does not consume the governed primary driver")
    if "primary_driver_v1" not in results_page:
        _fail("WS4", "results page does not read meta.insight_graph.primary_driver_v1")
    if "0.85" in results_page:
        _fail("WS4", "results page still invents a confidence value")
    if "derivePatternRelevanceLine" in results_page:
        _fail("WS4", "results page still derives frontend pattern-relevance prose")

    layout = _read_frontend("app/lib/resultsPageLayout.ts")
    for symbol in ("evidenceLevelFromCluster", "evidenceFromInsight", "pickSeverityPrimaryDriverCluster"):
        if symbol in layout:
            _fail("WS4", f"resultsPageLayout still defines {symbol}")

    if (FRONTEND / "app/lib/biomarkerPatternRelevance.ts").exists():
        _fail("WS4", "biomarkerPatternRelevance.ts still present")
    if (FRONTEND / "app/components/clusters/ClusterInsightPanel.tsx").exists():
        _fail("WS4", "ClusterInsightPanel.tsx still present")
    if "ClusterInsightPanel" in _read_frontend("app/components/clusters/index.ts"):
        _fail("WS4", "ClusterInsightPanel still exported from the clusters barrel")

    dials = _read_frontend("app/components/biomarkers/BiomarkerDials.tsx")
    if re.search(r"value\s*<\s*\d+\s*\|\|\s*value\s*>\s*\d+", dials):
        _fail("WS4", "BiomarkerDials still colours by numeric dial position")
    if "patternRelevanceLine" in dials:
        _fail("WS4", "BiomarkerDials still renders a frontend pattern-relevance line")

    insights = _read_frontend("app/components/insights/InsightsPanel.tsx")
    if "severityOrder" in insights:
        _fail("WS4", "InsightsPanel still re-ranks insights by severity")

    layer_c = _read_frontend("app/components/results/LayerCInsightSection.tsx")
    if "b.confidence - a.confidence" in layer_c or "b.confidence !== a.confidence" in layer_c:
        _fail("WS4", "LayerCInsightSection still re-ranks features by confidence")
    if "LAYER_C_INSIGHT_COPY" not in layer_c:
        _fail("WS4", "LayerCInsightSection does not use the governed copy module")

    cluster_summary = _read_frontend("app/components/clusters/ClusterSummary.tsx")
    if "getScoreColor" in cluster_summary or "getScoreBarColor" in cluster_summary:
        _fail("WS4", "ClusterSummary still applies frontend clinical colour thresholds")

    system_understanding = _read_frontend("app/components/results/SystemUnderstandingSection.tsx")
    if "systemUnderstandingCopy" not in system_understanding:
        _fail("WS4", "SystemUnderstandingSection does not use the governed copy module")


def main() -> int:
    check_ws1_rejected_frame_inactivation()
    check_ws2_retired_wording()
    check_ws3_mcv_co_service()
    check_ws4_layer_c_boundary()

    if FAILURES:
        print("arch_conv_correct1_gate: FAIL", file=sys.stderr)
        for failure in FAILURES:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    print("arch_conv_correct1_gate: PASS")
    print("WS1 rejected-frame inactivation, WS2 retired wording, WS3 MCV co-service, WS4 Layer C boundary")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
