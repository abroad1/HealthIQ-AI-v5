# HealthIQ Architecture Guardrails

**Status:** Canonical — enforceable rules derived from the ADR registry
**Date:** 2026-03-08
**Derived from:** ADR-001, ADR-002, ADR-003, ADR-005
**Pipeline reference:** `architecture/HEALTHIQ_REASONING_PIPELINE.md`

---

## Purpose

This document defines the rules that must never be violated in the HealthIQ codebase.
They are derived from the accepted ADRs and the canonical reasoning pipeline.

Each guardrail is stated as a rule, explains why it exists, shows a forbidden example,
and names the ADR that establishes it. These rules are candidates for automated
enforcement in the golden gate check.

---

## Rule 1 — No Clinical Thresholds in Runtime Code

**Rule:**
Disease-specific clinical threshold values must only appear in `signal_library.yaml`
packages. Runtime modules must contain no numeric clinical threshold constants.

**Why:**
Hardcoded thresholds in runtime code create a duplicate SSOT authority source.
They drift independently of the evidence-anchored Knowledge Bus packages.
They have no research citation. They are invisible to the clinical sign-off process.
A hardcoded threshold and a KB threshold for the same biomarker will eventually
diverge — silently producing different classifications for the same user input.

**Forbidden — will be rejected at audit:**
```python
# insight_graph_builder.py — ILLEGAL
if crp > 1.0:
    inflammation_flags.append("elevated_crp")

# orchestrator.py — ILLEGAL
if tyg_index >= 8.5:
    insulin_resistance = "at_risk"

# any runtime module — ILLEGAL
RISK_THRESHOLD = 3.0
if value > RISK_THRESHOLD:
    ...
```

**Permitted:**
```python
# signal_evaluator.py — CORRECT
# Thresholds are loaded from signal_library.yaml at runtime via SignalRegistry.
# No threshold constants appear in this file.
state = self._evaluate_thresholds(signal["thresholds"], value)
```

**ADR reference:** ADR-005 Invariant 4; ADR-001 Invariant 7 (no duplicate SSOT)
**Violation classification:** ARCHITECTURAL — escalate to GPT; do not retry

---

## Rule 2 — Signals Must Evaluate Raw Biomarker Values

**Rule:**
The Signal Evaluation Engine must receive raw numeric biomarker and derived metric
values. It must never receive pre-classified statuses, traffic-light flags,
or frontend biomarker classifications.

**Why:**
Pre-classification collapses a continuous biomarker value into a binary status
(normal / elevated) using the lab's population reference range. Once collapsed,
the raw value is gone. Disease-specific thresholds — which may flag a value as
at-risk even within the lab's normal range — can no longer be applied.
This is threshold amalgamation: it permanently destroys the platform's intelligence moat.

**Forbidden — will be rejected at audit:**
```python
# ILLEGAL — passing pre-classified status
signal_evaluator.evaluate(
    biomarker_status={"crp": "normal"},   # ← collapsed; raw value lost
)

# ILLEGAL — passing frontend flags
signal_evaluator.evaluate(
    flags={"crp_elevated": False},        # ← lab-derived flag; not raw value
)

# ILLEGAL — passing traffic light objects
signal_evaluator.evaluate(
    biomarker_nodes=insight_graph.nodes,  # ← already classified; unusable
)
```

**Permitted:**
```python
# CORRECT — raw numeric values only
signal_evaluator.evaluate_all(
    biomarkers={"crp": 2.5, "triglycerides": 1.8},     # ← raw floats
    derived_metrics={"derived.nlr": 2.1, "derived.tyg_index": 8.6},  # ← raw floats
    lab_ranges={"crp": {"min": 0.0, "max": 10.0}},      # ← for display only
)
```

**ADR reference:** ADR-005 Invariant 1
**Violation classification:** ARCHITECTURAL — escalate to GPT; do not retry

---

## Rule 3 — Signals Must Be Independent

**Rule:**
Signals must read only raw biomarker values and derived metrics.
Signals must never read another signal's output, state, or result.

**Why:**
If signal A reads signal B's output, the two signals become coupled. Signal B's
classification error propagates into signal A silently. Testing signal A in isolation
becomes impossible — its output depends on signal B's evaluation. At scale, chains of
signal dependencies create an untestable recursive reasoning system. The Insight Graph
combines signal states. Signals do not.

**Forbidden — will be rejected at audit:**
```python
# ILLEGAL — signal reading another signal's state
def evaluate_vascular_risk(signal, biomarkers, derived, signal_results):
    inflammation_state = signal_results["signal_systemic_inflammation"].state
    if inflammation_state == "at_risk":   # ← reading another signal; forbidden
        ...

# ILLEGAL — passing signal results into evaluator
evaluator.evaluate(
    signal_def=vascular_signal,
    prior_signals={"signal_systemic_inflammation": "at_risk"},  # ← forbidden
)
```

**Permitted:**
```python
# CORRECT — signal reads only biomarkers and derived metrics
def evaluate_vascular_risk(signal, biomarkers: Dict[str, float],
                           derived: Dict[str, float]):
    crp = biomarkers.get("crp")          # ← raw value; permitted
    nlr = derived.get("derived.nlr")    # ← raw computed value; permitted
    ...
```

**Note:** The Insight Graph layer (Stage 6) is the correct place to combine multiple
signal states into compound interpretations. Signal combination happens after
evaluation, not during it.

**ADR reference:** ADR-005 Invariant 3
**Violation classification:** ARCHITECTURAL — escalate to GPT; do not retry

---

## Rule 4 — Override Rules May Only Escalate

**Rule:**
Signal override rules may escalate severity (`optimal` → `suboptimal` → `at_risk`).
They may not downgrade severity. They may not change the primary metric.

**Why:**
A downgrading override would silently suppress a clinically significant finding.
A user at `at_risk` from the primary threshold evaluation could be reclassified to
`suboptimal` without the user knowing that the original threshold was met.
This is a patient safety concern, not an engineering preference.

**Forbidden:**
```yaml
# ILLEGAL in signal_library.yaml — downgrade override
- rule_id: "normalise_if_low_bmi"
  conditions:
    - metric_id: "bmi"
      operator: "<"
      value: 22.0
  resulting_state: "optimal"   # ← would downgrade an at_risk result; forbidden
```

**Permitted:**
```yaml
# CORRECT — escalation-only override
- rule_id: "tg_pancreatitis_override"
  conditions:
    - metric_id: "triglycerides"
      operator: ">="
      value: 5.6
  resulting_state: "at_risk"   # ← always an escalation; permitted
```

**ADR reference:** ADR-005 Invariant 5
**Violation classification:** MECHANICAL for schema; ARCHITECTURAL if in runtime code

---

## Rule 5 — Lab Reference Ranges Are Display Metadata Only

**Rule:**
Lab reference ranges (from the uploaded blood test report) are preserved for
display context — to show the user what the lab considers normal. They must never
be used as disease-specific clinical thresholds in signal evaluation.

**Why:**
Lab reference ranges are population normality ranges. They are not disease-specific.
A CRP within 0–10 mg/L is "lab normal" but may simultaneously represent residual
inflammatory risk at the 2.0 mg/L disease threshold. Using the lab range as a
clinical threshold collapses these two separate verdicts into one, destroying the
intelligence moat.

**Forbidden:**
```python
# ILLEGAL — using lab range as a clinical threshold
lab_max = input_reference_ranges["crp"]["max"]   # e.g., 10.0
if crp_value > lab_max:
    state = "at_risk"    # ← lab range used as clinical threshold; forbidden
```

**Permitted:**
```python
# CORRECT — lab range used only for display flag
lab_range = lab_ranges.get("crp", {})
lab_normal = _is_within_lab_range(crp_value, lab_range)  # display context only
lab_normal_but_flagged = lab_normal and signal_state in ("suboptimal", "at_risk")
```

**ADR reference:** ADR-002 Invariant 3; ADR-005 Invariant 1
**Violation classification:** ARCHITECTURAL — escalate to GPT; do not retry

---

## Rule 6 — Knowledge Bus Is the Only Route for Signal Thresholds

**Rule:**
No signal threshold may be introduced into the platform by any route other than
a validated and signed-off Knowledge Bus package.

**Why:**
This is the governance guarantee of the evidence pipeline. Any threshold introduced
outside the KB process bypasses clinical review, has no evidence anchor, and creates
an untraceable SSOT violation. The KB validator and clinical sign-off process exist
precisely to prevent unreviewed thresholds from entering the platform.

**Forbidden:**
```python
# ILLEGAL — threshold introduced without KB package
# (in ratio_registry.py, orchestrator.py, or any runtime module)
INSULIN_RESISTANCE_THRESHOLD = 8.5   # Where did this come from? No evidence. Forbidden.
```

**Permitted:**
```
New threshold → research report → KB translation → KB package
→ validator PASS → clinical sign-off → Layer B implementation
```

**ADR reference:** ADR-003 Invariant 1; ADR-001 Invariant 7
**Violation classification:** ARCHITECTURAL — escalate to GPT; do not retry

---

## Enforcement Status

| Rule | Currently enforced | Target enforcement |
|------|-------------------|-------------------|
| Rule 1 — No thresholds in runtime | Manual audit only | Golden gate regex check (future) |
| Rule 2 — Raw values at evaluator | Not yet (evaluator not built) | SignalEvaluator API contract (KB-S10) |
| Rule 3 — Signal independence | Not yet (evaluator not built) | SignalEvaluator API contract (KB-S10) |
| Rule 4 — Override escalation only | KB validator (partial) | SignalEvaluator `_safe_escalate()` (KB-S10) |
| Rule 5 — Lab ranges are display only | Manual audit only | Code review gate |
| Rule 6 — KB only route | KB validator + sign-off process | KB validator (active) |

---

## References

- `architecture/HEALTHIQ_REASONING_PIPELINE.md` — canonical pipeline
- `architecture/ADR-001-platform-non-negotiables.md`
- `architecture/ADR-002-deterministic-analysis-engine.md`
- `architecture/ADR-003-knowledge-bus-architecture.md`
- `architecture/ADR-005-disease-specific-signal-evaluation-v2.md`
