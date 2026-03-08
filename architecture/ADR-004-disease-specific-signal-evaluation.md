# ADR-004 — Disease-Specific Signal Evaluation Architecture

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Date** | 2026-03-08 |
| **Authority** | Knowledge Bus translation programme; KBP-0005 threshold correction |
| **Supersedes** | — |
| **Superseded by** | — |
| **Implements** | ADR-002 (Layer B), ADR-003 (Knowledge Bus) |

---

## Context

During the Knowledge Bus translation programme (KBP-0002 through KBP-0005), a critical
architectural gap was identified: the platform's current pipeline evaluates each
biomarker once against a single lab reference range and propagates that single
pass/fail status to all downstream analysis. This is called **threshold amalgamation**.

Threshold amalgamation destroys clinical value because:

- The same biomarker carries different thresholds for different diseases
- A lab-normal result can simultaneously represent at-risk status for a specific
  condition when evaluated against a disease-targeted research threshold
- Once collapsed to a single `normal/elevated` status, the disease-specific signal
  is permanently lost

The specific incident that prompted this ADR: during KBP-0005 translation, the
translation engine defaulted to 3.0 mg/L for the hs-CRP at-risk boundary (the
traditional ACC/AHA general three-tier classification) rather than the 2.0 mg/L
threshold explicitly stated in the research conclusions (JUPITER trial; ACC/AHA 2025
Scientific Statement). The error was caught in review and corrected. The architectural
rules in this ADR exist to prevent the same class of error at the code level.

Additionally, the current `insight_graph_builder.py` contains hardcoded threshold
logic (e.g., `if crp > 1.0`) with no evidence anchor and no disease context — a
second form of the same problem inside the codebase itself.

---

## Decision

The platform must implement a Signal Evaluation Engine that:
1. Receives raw biomarker values (never pre-classified statuses)
2. Evaluates each signal independently against its disease-specific thresholds
3. Produces independent signal states that coexist without merging
4. Allows the same biomarker to be simultaneously optimal in one signal and at-risk
   in another

This is the architectural foundation of the HealthIQ intelligence moat.

---

## The HealthIQ Intelligence Model

The platform produces three simultaneous, independent verdicts for every biomarker:

### Layer 1 — Lab Context
> "Your CRP is 2.5 mg/L. The lab reference range is 0–10 mg/L. This is within the
> normal range."

*Source: lab reference range from the uploaded blood test report*

### Layer 2 — Disease-Signal Context
> "However, for chronic metabolic inflammation, research (JUPITER trial; ACC/AHA 2025)
> identifies 2.0 mg/L as the threshold for residual inflammatory risk. Your result
> places you in the at-risk category for this signal."

*Source: `signal_library.yaml` threshold, evaluated independently per signal*

### Layer 3 — Compound Intelligence
> "This finding is supported by your NLR of 2.1 (above the metabolic syndrome cutoff
> of 1.67) and your TyG index of 8.6 (suboptimal range). Together these markers suggest
> early metabolic inflammatory burden — a pattern associated with increased
> cardiovascular and metabolic risk in prospective cohort research, often years before
> standard screening would identify a problem."

*Source: supporting marker correlation within the same signal*

**Layer 3 is the HealthIQ moat.** Identifying early disease in lab-normal results,
corroborated by supporting markers, anchored to named research, is the capability
that distinguishes this platform from all existing consumer biomarker applications.

---

## Target Architecture

```
Layer A: Biomarker ingestion
  → raw values + lab reference ranges preserved
        ↓
Layer B: Derived metric computation (ratio_registry.py)
  → raw values + derived metric values available
        ↓
[NEW] Signal Evaluation Engine (signal_evaluator.py)
  → loads all active signal_library.yaml packages
  → evaluates each signal independently against raw values
  → applies override rules (escalation only)
  → produces: signal_id → {state, value, supporting_marker_states, evidence_anchor}
  → flags lab-normal-but-signal-flagged cases explicitly
        ↓
Layer C: Insight graph + bundle consumption
  → consumes signal states (not biomarker statuses) for clinical interpretation
  → consumes lab reference range statuses for display context only
  → both coexist — neither replaces the other
```

---

## Architectural Invariants

1. **Raw values must reach the signal evaluator.** The raw biomarker value (e.g.,
   CRP = 2.5 mg/L) must be passed to the Signal Evaluation Engine before any status
   classification occurs. A pre-classified status (`normal`, `elevated`) must never
   be used as input to signal threshold evaluation.

2. **Signals evaluate independently.** Each signal (`signal_systemic_inflammation`,
   `signal_vascular_inflammatory_stress`, etc.) evaluates the same biomarker value
   independently against its own thresholds. Signal states never merge. A biomarker
   may be simultaneously optimal in one signal and at-risk in another — both are correct.

3. **No hardcoded clinical thresholds in runtime code.** No numeric threshold constant
   (e.g., `if crp > 1.0`, `if tyg > 8.5`) may appear in `insight_graph_builder.py`,
   `orchestrator.py`, or any Layer C or bundle file. All thresholds are loaded from
   `signal_library.yaml` packages at runtime.

4. **Override rules escalate only.** Signal override rules may only increase severity
   (force `at_risk`). They may never decrease severity (e.g., override `at_risk` to
   `suboptimal`). The Signal Evaluation Engine must enforce this with the severity
   rank constraint: `optimal (0) < suboptimal (1) < at_risk (2)`.

5. **Lab-normal-but-signal-flagged cases must surface.** When a biomarker is within
   its lab reference range but a signal classifies it as `suboptimal` or `at_risk`,
   this combination must be explicitly flagged in the signal output and must not be
   suppressed by any downstream scoring, normalisation, or aggregation step.

6. **Evidence anchors must be preserved to output.** Each signal state output must
   carry the evidence reference (study name, threshold value, population) that produced
   it. This reference must reach the Layer C narrative layer so it can be cited in user
   output.

7. **Thresholds belong to signals, not biomarkers.** The same biomarker may have
   different thresholds in different signals because each signal targets a specific
   disease. A threshold appropriate for vascular inflammatory stress may differ from
   one targeting metabolic meta-inflammation — both are simultaneously valid. The
   threshold must be stored with the signal definition, never with the biomarker
   definition.

---

## Implementation Requirements (KB-S10)

| Requirement | Component | Priority |
|------------|-----------|----------|
| Create Signal Evaluation Engine | `backend/core/analytics/signal_evaluator.py` | Critical |
| Pass raw values to signal evaluator before status classification | `orchestrator.py` | Critical |
| Remove all hardcoded CRP threshold logic | `insight_graph_builder.py` lines 97-117 | Critical |
| Layer C reads signal states, not biomarker statuses, for clinical logic | `insight_graph_builder.py` + bundles | Critical |
| Flag lab-normal-but-signal-flagged cases in signal output | `signal_evaluator.py` | High |
| Preserve evidence anchor in signal output DTO | `signal_evaluator.py` → output | High |
| Enforce override escalation-only constraint | `signal_evaluator.py` | High |
| Implement `derived.tyg_index` (blocks KBP-0002, KBP-0004) | `ratio_registry.py` | High |
| Implement `derived.sii` (blocks KBP-0005) | `ratio_registry.py` | Standard |

---

## Signal Evaluation Engine — Reference Implementation

```python
"""
Signal Evaluation Engine

Architecture reference: ADR-004 Disease-Specific Signal Evaluation Architecture
See: architecture/ADR-004-disease-specific-signal-evaluation.md

INVARIANT: This engine receives raw biomarker values only.
It must never receive pre-classified biomarker statuses as input.
"""

SEVERITY_RANK = {"optimal": 0, "suboptimal": 1, "at_risk": 2}


def evaluate_signal(signal_def: dict, biomarkers: dict, derived: dict) -> dict:
    primary_metric = signal_def["primary_metric"]
    value = _get_value(primary_metric, biomarkers, derived)

    # Evaluate primary thresholds against raw value
    state = _evaluate_thresholds(signal_def["thresholds"], value)

    # Apply override rules — escalation only, never downgrade
    for rule in signal_def.get("override_rules", []):
        if _evaluate_conditions(rule["conditions"], biomarkers, derived):
            state = _resolve_override(state, rule["resulting_state"])

    return {
        "signal_id": signal_def["signal_id"],
        "state": state,
        "primary_metric": primary_metric,
        "value": value,
        "evidence": signal_def.get("description", ""),
    }


def _resolve_override(current: str, proposed: str) -> str:
    """Override rules may only escalate severity. Never downgrade."""
    if SEVERITY_RANK.get(proposed, 0) > SEVERITY_RANK.get(current, 0):
        return proposed
    return current  # silently ignore downgrade attempts
```

---

## Consequences

- The existing hardcoded threshold logic in `insight_graph_builder.py` must be removed
  in KB-S10 — it is a direct violation of invariant 3
- Any future sprint that adds clinical threshold constants to Layer B or C code must
  be rejected at audit (future golden gate check)
- The output DTO for signal evaluation must carry `lab_normal_but_flagged: bool` to
  support the Layer 3 compound intelligence output
- This architecture enables the platform's core differentiation: finding early disease
  in lab-normal results, corroborated by supporting markers, cited to published research

---

## Source Documents

- `docs/DISEASE_SPECIFIC_THRESHOLD_ARCHITECTURE.md` — detailed design record
- `knowledge_bus/packages/pkg_chronic_inflammation/clinical_signoff.md` — KBP-0005
  threshold correction that prompted this ADR
- `docs/KNOWLEDGE_BUS_SOP_v1.2.md` — KB governance
- `docs/Master_PRD_v5.2.md` §4 — Layer B specification
