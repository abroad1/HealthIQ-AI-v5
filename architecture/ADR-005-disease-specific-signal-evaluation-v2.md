# ADR-005 — Disease-Specific Signal Evaluation Architecture (v2)

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Date** | 2026-03-08 |
| **Authority** | Product Architecture Review — Strategic Architecture Assessment |
| **Supersedes** | ADR-004 |
| **Superseded by** | — |
| **Implements** | ADR-002 (layer architecture), ADR-003 (Knowledge Bus) |

---

## Context

ADR-004 correctly identified the threshold amalgamation problem and the HealthIQ
intelligence moat. A product architecture review confirmed the strategic direction but
identified three errors requiring correction before implementation:

1. **Compound intelligence was framed as a separate architectural layer.** It is not.
   Compound intelligence (supporting marker corroboration) belongs inside the Signal
   Evaluation Engine, not in a separate output layer. Implementing it as a separate layer
   would create duplicated logic and a second signal evaluation pass.

2. **The SignalRegistry startup-load pattern was absent.** Loading signal definitions
   dynamically per execution becomes inefficient and brittle at scale (200+ signals).
   Signals must be compiled into a registry at startup.

3. **Signal independence was not stated as a hard invariant.** Signals must never read
   each other's outputs. If signals can consume other signal states, the system becomes
   recursively coupled and untestable. This must be a hard architectural constraint.

Additionally, two rules on override behaviour and the supporting metrics schema were
incomplete and are corrected here.

---

## Decision

The platform must implement a Signal Evaluation Engine governed by the invariants in
this document. The engine is the biological reasoning core of the platform. Its design
directly determines whether HealthIQ's clinical intelligence moat can be maintained as
the system scales.

---

## The HealthIQ Intelligence Model

The platform's intelligence value is produced by this specific combination:

```
biomarker value
  + disease-specific research threshold       → signal state
  + supporting biomarker corroboration        → compound finding
  + evidence citation                         → clinical credibility
```

Most platforms produce:
```
value → reference range → normal / abnormal
```

HealthIQ produces:
```
value → disease evidence graph → signal state with supporting marker context
```

The key differentiation is the **lab-normal-but-signal-flagged case**: a biomarker
within its lab reference range that nonetheless meets the research threshold for a
specific disease, corroborated by supporting markers in the same signal. This is
finding early disease before the lab would flag anything. It is the platform moat.

---

## Corrected Pipeline Architecture

The correct pipeline is four stages, not three:

```
Stage 1 — Layer A: Biomarker Ingestion
  Input:  raw lab data (values + lab reference ranges)
  Output: canonical biomarker values (Dict[str, float])
          lab reference ranges preserved as display metadata only
  Rule:   no clinical interpretation; no threshold evaluation

Stage 2 — Layer B: Derived Metric Computation
  Input:  canonical biomarker values
  Output: canonical biomarkers + derived metrics (Dict[str, float])
  Rule:   ratio_registry.py only; no threshold evaluation

Stage 3 — Layer C: Signal Evaluation Engine (NEW)
  Input:  biomarkers: Dict[str, float]
          derived_metrics: Dict[str, float]
  Output: signal results (one per active signal)
          each result contains: state, primary value, supporting marker states,
          evidence anchor, lab_normal_but_flagged flag
  Rule:   evaluates each signal independently; reads only biomarkers and
          derived_metrics; never reads another signal's output

Stage 4 — Layer D: Insight and Narrative Construction
  Input:  signal results from Stage 3
          lab reference range statuses from Stage 1 (for display context)
  Output: user-facing insights with evidence-anchored narrative
  Rule:   consumes signal states; performs no clinical computation
```

**Key correction from ADR-004:** What was previously called "Layer 3 — Compound
Intelligence" is not a separate architectural stage. It is the supporting metric
evaluation that occurs inside Stage 3 (the Signal Evaluation Engine) for every signal.
The compound finding is part of the signal result, not a subsequent pass.

---

## Signal Evaluation Engine Design

### SignalRegistry — load once at startup

Signal definitions are loaded and compiled once when the service starts. The evaluator
receives compiled signal objects, not raw YAML.

```python
"""
Architecture reference: ADR-005 Disease-Specific Signal Evaluation Architecture v2
See: architecture/ADR-005-disease-specific-signal-evaluation-v2.md
"""

class SignalRegistry:
    """
    Loads all active signal_library.yaml packages at service startup.
    Compiled signal objects are passed to SignalEvaluator at runtime.

    Benefits: fast runtime; validates all signals at startup; deterministic;
    scales to 200+ signals without per-execution I/O.
    """
    def __init__(self, packages_dir: str):
        self._signals: Dict[str, dict] = {}
        self._load_all(packages_dir)

    def _load_all(self, packages_dir: str) -> None:
        for package_path in Path(packages_dir).glob("*/signal_library.yaml"):
            library = yaml.safe_load(package_path.read_text())
            for signal in library.get("signals", []):
                self._signals[signal["signal_id"]] = signal

    def get_all(self) -> List[dict]:
        return list(self._signals.values())
```

### SignalEvaluator — API contract

The evaluator API must accept **raw numeric values only**. Pre-classified statuses,
flags, or frontend classifications are forbidden inputs.

```python
class SignalEvaluator:
    """
    Evaluates all registered signals against raw biomarker and derived metric values.

    INVARIANT: inputs must be raw numeric values (Dict[str, float]).
    This engine must NEVER receive biomarker_status, biomarker_flags,
    frontend classifications, or any other pre-classified form.
    Violation silently reintroduces threshold amalgamation.

    INVARIANT: signals are evaluated independently.
    No signal result is passed as input to another signal.
    """

    def evaluate_all(
        self,
        biomarkers: Dict[str, float],       # raw values only
        derived_metrics: Dict[str, float],  # raw computed values only
        lab_ranges: Dict[str, dict],        # for lab_normal_but_flagged detection only
        signals: List[dict],
    ) -> List[SignalResult]:
        return [
            self._evaluate_one(signal, biomarkers, derived_metrics, lab_ranges)
            for signal in signals
        ]
```

### Signal evaluation — including supporting metrics

Supporting metrics are declared in `signal_library.yaml` with their own research
thresholds. The evaluator handles them generically — no ad-hoc logic per signal.

```python
    def _evaluate_one(
        self,
        signal: dict,
        biomarkers: Dict[str, float],
        derived_metrics: Dict[str, float],
        lab_ranges: Dict[str, dict],
    ) -> SignalResult:
        primary_metric = signal["primary_metric"]
        primary_value = self._get_value(primary_metric, biomarkers, derived_metrics)

        # Evaluate primary thresholds
        state = self._evaluate_thresholds(signal["thresholds"], primary_value)

        # Apply override rules — escalation only; primary metric never changes
        for rule in signal.get("override_rules", []):
            if self._conditions_met(rule["conditions"], biomarkers, derived_metrics):
                state = self._safe_escalate(state, rule["resulting_state"])

        # Evaluate supporting metrics (declarative, generic — not ad-hoc)
        supporting_states = {}
        for sm in signal.get("supporting_metrics_with_thresholds", []):
            sm_value = self._get_value(sm["metric"], biomarkers, derived_metrics)
            if sm_value is not None:
                supporting_states[sm["metric"]] = {
                    "value": sm_value,
                    "threshold": sm["threshold"],
                    "elevated": sm_value >= sm["threshold"],
                }

        # Detect lab-normal-but-signal-flagged (the highest-value output)
        lab_range = lab_ranges.get(primary_metric, {})
        lab_normal = self._is_within_lab_range(primary_value, lab_range)
        lab_normal_but_flagged = lab_normal and state in ("suboptimal", "at_risk")

        return SignalResult(
            signal_id=signal["signal_id"],
            state=state,
            primary_metric=primary_metric,
            primary_value=primary_value,
            supporting_states=supporting_states,
            lab_normal_but_flagged=lab_normal_but_flagged,
            evidence=signal.get("description", ""),
        )
```

### Override safety — escalation only, primary metric immutable

```python
    SEVERITY_RANK = {"optimal": 0, "suboptimal": 1, "at_risk": 2}

    def _safe_escalate(self, current: str, proposed: str) -> str:
        """
        Override rules may only escalate severity. Never downgrade.
        Override rules may never change the primary metric.
        (Primary metric immutability is enforced by the API — overrides
        receive state only, never the metric identifier.)
        """
        if self.SEVERITY_RANK.get(proposed, 0) > self.SEVERITY_RANK.get(current, 0):
            return proposed
        return current
```

---

## Supporting Metrics Schema Extension

The signal_library.yaml schema must be extended to declare supporting metric thresholds
explicitly. This keeps signal definitions fully declarative.

Current schema (supporting_metrics as name-list only):
```yaml
supporting_metrics:
  - "derived.nlr"
  - "derived.sii"
```

Required schema addition (`supporting_metrics_with_thresholds`):
```yaml
supporting_metrics_with_thresholds:
  - metric: "derived.nlr"
    threshold: 1.67
    evidence: "NHANES meta-analysis n=70,937 — MetS cutoff"
  - metric: "derived.sii"
    threshold: 626.51
    evidence: "Frontiers in Endocrinology 2025 meta-analysis n=85,796"
```

The existing `supporting_metrics` list is retained for backwards compatibility.
`supporting_metrics_with_thresholds` is the new field evaluated by the Signal
Evaluation Engine. **KB-S9 must add this field to all existing KB packages.**

---

## Architectural Invariants

The following invariants are binding on all implementation. They may not be overridden
by any sprint, work package, or individual engineering decision.

### Invariant 1 — Raw values only at the signal evaluator boundary

The Signal Evaluation Engine must accept:
```
biomarkers:       Dict[str, float]   ← raw numeric values
derived_metrics:  Dict[str, float]   ← raw computed values
```

The Signal Evaluation Engine must NOT accept:
```
biomarker_status    ← pre-classified
biomarker_flags     ← pre-classified
frontend_status     ← pre-classified
```

Passing a pre-classified status silently reintroduces amalgamation. There is no valid
exception to this rule.

### Invariant 2 — Signals are independent evaluators

Each signal evaluates the same biomarker values independently against its own
disease-specific thresholds. Signal states never merge. A biomarker may be
simultaneously `optimal` in one signal and `at_risk` in another. Both are correct
because they answer different biological questions.

### Invariant 3 — No signal reads another signal

Signals may read only:
```
biomarkers        (Dict[str, float])
derived_metrics   (Dict[str, float])
```

Signals may NOT read:
```
other signal states
other signal results
```

If a signal consumes another signal's output, the system becomes recursively coupled
and untestable. Insights combine signal states. Signals do not.

### Invariant 4 — Zero clinical thresholds in runtime code

No numeric threshold constant may appear in `insight_graph_builder.py`,
`orchestrator.py`, or any Layer D file. The only permitted location for clinical
threshold values is `signal_library.yaml` packages. Hardcoded thresholds are an
illegal duplicate SSOT authority source (violates ADR-001 Invariant 7).

### Invariant 5 — Override rules escalate only; primary metric is immutable

Override rules may:
- Escalate severity (`optimal` → `suboptimal`; `suboptimal` → `at_risk`)
- Attach explanation metadata

Override rules may NOT:
- Downgrade severity
- Change the primary metric
- Bypass thresholds entirely

### Invariant 6 — Lab-normal-but-signal-flagged cases must surface

When a biomarker is within its lab reference range but a signal classifies it as
`suboptimal` or `at_risk`, the `lab_normal_but_flagged` flag in the signal result
must be `true`. This flag must not be suppressed by any downstream scoring,
normalisation, or aggregation step. These cases represent the highest-value clinical
outputs the platform produces.

### Invariant 7 — Evidence anchors must reach the output layer

Each `SignalResult` must carry the evidence anchor (study, threshold, population) that
produced the signal state. This reference must be preserved through Layer D so it can
be cited in user-facing narrative. An output without an evidence citation is incomplete.

### Invariant 8 — Thresholds belong to signals, not biomarkers

The same biomarker may carry different thresholds in different signals. The threshold
is a property of the signal definition (the disease being studied), never of the
biomarker itself. Biomarker definitions in `biomarkers.yaml` must never contain
clinical threshold values.

---

## Implementation Requirements (KB-S9 and KB-S10)

### KB-S9 (derived metrics + schema extension)

| Requirement | File | Priority |
|------------|------|----------|
| Implement `derived.tyg_index` | `ratio_registry.py` | Critical (blocks KBP-0002, KBP-0004) |
| Implement `derived.sii` | `ratio_registry.py` | High (blocks KBP-0005) |
| Add `supporting_metrics_with_thresholds` to all KB packages | `*/signal_library.yaml` | High |
| Confirm HOMA-IR divisor (405 vs 22.5) | `ratio_registry.py` | High |

### KB-S10 (Signal Evaluation Engine)

| Requirement | File | Priority |
|------------|------|----------|
| Implement `SignalRegistry` | `backend/core/analytics/signal_registry.py` | Critical |
| Implement `SignalEvaluator` with raw-values-only API | `backend/core/analytics/signal_evaluator.py` | Critical |
| Remove hardcoded CRP logic | `insight_graph_builder.py` lines 97–117 | Critical |
| Wire signal evaluator into orchestrator before status classification | `orchestrator.py` | Critical |
| Layer D reads signal states for clinical logic (not biomarker statuses) | `insight_graph_builder.py` + bundles | Critical |
| Preserve `lab_normal_but_flagged` through to output DTO | `signal_evaluator.py` → output | High |
| Preserve evidence anchor through to output DTO | `signal_evaluator.py` → output | High |

---

## Consequences

- ADR-004 is superseded. Its core insight was correct; the architectural details
  required the corrections documented here.
- The "compound intelligence" concept from ADR-004 is preserved but is now correctly
  located inside the Signal Evaluation Engine as supporting metric evaluation.
- `docs/DISEASE_SPECIFIC_THRESHOLD_ARCHITECTURE.md` remains as the design record
  that preceded and informed this ADR.
- All future sprint work packages implementing signal evaluation must reference
  this ADR and demonstrate compliance with all eight invariants.

---

## Source Documents

- `architecture/ADR-004-disease-specific-signal-evaluation.md` — superseded predecessor
- `docs/DISEASE_SPECIFIC_THRESHOLD_ARCHITECTURE.md` — design record
- Product Architecture Review — Strategic Architecture Assessment (2026-03-08)
- `docs/KNOWLEDGE_BUS_SOP_v1.2.md` — Knowledge Bus governance
- `docs/Master_PRD_v5.2.md` §4 — Layer B specification
