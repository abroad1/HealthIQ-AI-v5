"""
Signal Evaluation Engine — HealthIQ AI v5

Architecture reference: ADR-005 Disease-Specific Signal Evaluation Architecture (v2)
See: architecture/ADR-005-disease-specific-signal-evaluation-v2.md

Pipeline position:
    Evidence → Signal → Insight
               ^^^^^^
               This module implements the Signal stage of the HealthIQ reasoning
               pipeline. See architecture/HEALTHIQ_REASONING_PIPELINE.md for the
               full pipeline definition.

    Evidence is stored in Knowledge Bus packages (knowledge_bus/packages/).
    This engine evaluates biomarker values against that evidence.
    InsightGraph (insight_graph_builder.py) converts signal outputs into insights.

Architectural invariants (from ADR-005 — all are non-negotiable):

    Invariant 1 — Raw values only
        This engine accepts Dict[str, float] biomarker and derived metric values.
        It must NEVER receive pre-classified statuses, traffic-light flags, or
        frontend biomarker classifications. Violation silently reintroduces
        threshold amalgamation and destroys the platform's intelligence moat.

    Invariant 2 — Signals are independent evaluators
        Each signal evaluates biomarker values independently against its own
        disease-specific thresholds. Signal states never merge. A biomarker may
        be simultaneously optimal in one signal and at_risk in another.

    Invariant 3 — No signal reads another signal
        Signals read only biomarkers and derived_metrics. No signal may consume
        another signal's state or result. Signal combination happens in the
        InsightGraph layer, not here.

    Invariant 4 — Zero clinical thresholds in this file
        All clinical threshold values are loaded from signal_library.yaml packages
        via SignalRegistry. This file contains no numeric threshold constants.

    Invariant 5 — Override rules escalate only; primary metric is immutable
        Override rules may escalate severity. They may not downgrade it.
        Override rules may not change the primary metric.

    Invariant 6 — lab_normal_but_flagged must surface
        When a biomarker is within its lab reference range but a signal classifies
        it as suboptimal or at_risk, this must be explicitly flagged. These cases
        are the highest-value outputs the platform produces.

Implementation status:
    NOT YET IMPLEMENTED — placeholder module only.
    Implementation is scheduled for KB-S10.
    See architecture/HEALTHIQ_REASONING_PIPELINE.md Stage 5 for design specification.
    See architecture/ADR-005-disease-specific-signal-evaluation-v2.md for the
    full reference implementation.
"""

# KB-S10: Implement SignalRegistry and SignalEvaluator here.
# Do not implement until KB-S9 (derived metrics) is complete and all KB packages
# have passed clinical sign-off.
#
# Required classes:
#   SignalRegistry   — loads all signal_library.yaml packages at startup
#   SignalEvaluator  — evaluates all registered signals against raw biomarker values
#   SignalResult     — output dataclass per signal evaluation
#
# Required inputs to SignalEvaluator.evaluate_all():
#   biomarkers:      Dict[str, float]   raw biomarker values only
#   derived_metrics: Dict[str, float]   raw derived metric values only
#   lab_ranges:      Dict[str, dict]    for lab_normal_but_flagged detection only
#
# See ADR-005 for the complete reference implementation.

raise NotImplementedError(
    "signal_evaluator.py is a placeholder. "
    "Implementation is scheduled for KB-S10. "
    "See architecture/ADR-005-disease-specific-signal-evaluation-v2.md."
)
