# HealthIQ AI
## Architecture Strategy Paper
### Signal Architecture Completion

**Version:** 1.0
**Status:** Active
**Classification:** Architecture Strategy
**Date:** 2026-03-09
**Author:** Product / Architecture
**Related Documents:** Master PRD v5.2, Delivery Sprint Plan v5.2 (Phase 5), Master Roadmap v5.2→v5.3, Automation Bus SOP v1.2

---

# 1. Executive Summary

HealthIQ AI is completing a transition from an early analytical system based primarily on
biomarker scoring into a deterministic biological intelligence platform.

This paper describes the completion of the signal architecture layer — the final major
component required to deliver that platform. It is not a pivot. The signal architecture was
designed into the platform from the beginning. The infrastructure required to support it has
been systematically built across Sprints 1–12 and the KB sprint series. What remains is
implementing the signal evaluation engine and wiring it into the runtime pipeline.

**Signals are the primary analytical unit of the HealthIQ platform.** Rather than
interpreting biomarkers independently, the system detects biological conditions such as:

- Insulin resistance
- Hepatic stress
- Chronic inflammation
- Methylation stress
- Atherogenic lipoprotein burden

These signals become the deterministic intelligence layer of the system.

The signal library is the central intellectual property of the HealthIQ platform.

---

# 2. Current Platform State

## 2.1 What Has Been Built

The existing platform is not a simple scoring system. It is a deterministic analytical
substrate built specifically to support signal-level reasoning. The runtime pipeline is:

```
API → Layer A (Canonicalisation + Unit Normalisation + Lab-Origin Detection)
    → Layer B (Scoring + Derived Ratios + Cluster Scoring + InsightGraph Assembly)
    → Layer C (Narrative Translation)
```

**Layer A is complete:**

- Hard-typed unit registry with base-unit normalisation
- Lab-origin detection and metadata capture
- Biomarker criticality and confidence degradation
- Canonical alias resolution (1,600 aliases mapped)
- 15 derived metrics computed deterministically via RatioRegistry, including:
  `remnant_cholesterol`, `homa_ir`, `fib_4`, `tyg_index`, `nlr`, `sii`, and others
- Age injection from `questionnaire_data.date_of_birth` for fib_4 computation
- SSOT registration of all computed derived metrics

**Layer B is substantially complete:**

- Deterministic scoring engine
- Criticality-weighted confidence
- Schema-driven cluster scoring (ClusterEngineV2)
- InsightGraph contract (`extra="forbid"` — strict boundary between Layer B and Layer C)
- Relationship registry (pairwise biomarker pattern detection)
- BiomarkerContext (code-only explanatory context per marker)
- Replay manifest with version stamping

**Layer C is complete:**

- Pure narrative translation consuming InsightGraph structured payload only
- LLM receives no raw biomarker values, units, or ranges (enforced by integration tests)

**Knowledge Bus is active:**

- 12 signals defined across 6 validated knowledge packages
- Full signal schema contract enforced by validator (`validate_signal_library.py`)
- Signal libraries reference-only at present — not yet evaluated at runtime

## 2.2 The Remaining Gap

One component is missing: the **signal evaluation engine**.

`backend/core/analytics/signal_evaluator.py` exists as a placeholder. ADR-005 defines the
complete implementation specification. The signal libraries are ready. The derived metrics
that feed them are computed. The InsightGraph boundary that will carry their output is frozen.

The gap is execution, not design.

---

# 3. Signals as the Core Analytical Primitive

Traditional blood analysis software treats biomarkers as the primary analytical objects.

HealthIQ treats **biological signals** as the core analytical primitive.

A signal represents a physiologically meaningful state detected through deterministic
biomarker patterns. It is not a score or a weighted heuristic. It is a traceable conclusion
derived from research-backed threshold logic applied to canonical biomarker values.

**Example — signal_insulin_resistance:**

```
Primary metric:   tyg_index
Supporting:       tg_hdl_ratio, homa_ir

Thresholds:
  tyg_index < 8.30   → optimal    (Navarro-González 2016, AUC 0.75)
  tyg_index 8.30–8.49 → suboptimal
  tyg_index ≥ 8.50   → at_risk    (Irace 2022, AUROC 0.837)

Override:
  hba1c ≥ 5.7 OR glucose ≥ 5.6 → escalate to at_risk regardless of tyg_index
```

The system therefore detects the signal "insulin resistance" rather than reporting individual
marker deviations. This allows the platform to reason about physiology rather than laboratory
numbers.

---

# 4. Strategic Benefits

## 4.1 System-Level Reasoning

Signals enable the platform to reason about biological systems rather than isolated markers.

Multiple signals can interact to produce higher-order physiological interpretations.

Example:

```
insulin_resistance + hepatic_stress → metabolic syndrome precursor state
```

## 4.2 Research Integration

Signals provide a structured mechanism for incorporating biomedical research.

New research findings are converted into new signals or refinements of existing signals via
the Knowledge Bus pipeline. The platform evolves continuously as new research emerges.

The Knowledge Bus validator enforces schema integrity, threshold provenance, and canonical
identifier compliance on every new package before it enters the runtime.

## 4.3 Intellectual Property

A large curated library of physiological signal definitions is a defensible intellectual
asset. Competitors can replicate biomarker explanations. Replicating a comprehensive signal
detection library built from primary research, with traceable threshold provenance and a
validated schema contract, is materially more difficult.

## 4.4 The lab_normal_but_flagged Differentiator

A critical platform capability enabled by signal architecture: a biomarker can be within
the laboratory reference range yet still trigger a signal.

Example: a patient's TyG index may fall within a generic lab reference range but still meet
the research-derived threshold for insulin resistance onset. The platform surfaces this
explicitly as `lab_normal_but_flagged`.

This capability — deterministically exposing the gap between lab-normal and research-normal —
is a core platform differentiator. It cannot be replicated by systems that treat lab
reference ranges as the only classification authority.

---

# 5. Signal Architecture Contract

Signals follow a deterministic contract. Every signal defines:

| Field | Description |
|-------|-------------|
| `signal_id` | Canonical identifier (`^signal_[a-z0-9_]+$`) |
| `primary_metric` | Single derived or raw metric driving the signal |
| `supporting_metrics` | Metrics providing corroborating evidence |
| `dependencies` | Required biomarkers and derived metrics |
| `thresholds` | Research-backed severity classifications (optimal / suboptimal / at_risk) |
| `activation_logic` | Always `deterministic_threshold` — no probabilistic logic |
| `override_rules` | Conditions that escalate severity; never downgrade |
| `research_sources` | Citation-level provenance per threshold |
| `bundle_consumers` | Downstream systems consuming this signal |

**Signals never rely on probabilistic reasoning or weighted heuristics. Activation is always
traceable to deterministic threshold logic backed by research citations.**

---

# 6. Multi-Layer Signal Architecture

The platform supports three signal layers, implemented progressively.

## Layer 1 — Primary Physiological Signals

Detect direct physiological states from biomarker patterns.

Current knowledge bus signals:

- `signal_insulin_resistance` — tyg_index primary, homa_ir supporting
- `signal_atherogenic_lipoprotein_burden` — non_hdl_cholesterol primary
- `signal_hepatic_metabolic_stress` — ast_alt_ratio primary, fib_4 supporting
- `signal_chronic_low_grade_inflammation` — crp primary, nlr supporting
- Plus 8 additional signals across metabolic, vascular, and hepatic systems

## Layer 2 — Composite Signals

Detect higher-order patterns from multiple primary signals.

Example:

```
cardiometabolic_acceleration
  ← insulin_resistance
  ← vascular_inflammation
```

## Layer 3 — System Burden Signals

Represent cumulative stress on major biological systems by integrating composite and
primary signal outputs.

Examples: `metabolic_system_burden`, `cardiovascular_system_burden`

---

# 7. Alignment with Three-Layer Architecture

The signal detection engine is the core component of Layer B.

```
Layer A   Canonical data ingestion
          (canonicalisation, unit normalisation, lab-origin detection, derived ratios)

Layer B   Deterministic biological intelligence
          (scoring, clustering, SIGNAL EVALUATION, InsightGraph assembly)

Layer C   Narrative translation
          (LLM consumes InsightGraph only — no raw biomarkers, no signal logic)
```

Signal evaluation slots into Layer B between derived ratio computation and InsightGraph
assembly. This placement is architecturally clean: signals consume derived metrics already
computed by the RatioRegistry, and their outputs feed into the InsightGraph as a
version-stamped, structured field.

The LLM operates purely as a narrative translation layer. It receives signal states as
structured data. It does not perform signal reasoning.

---

# 8. Implementation Completion Path

The following sprints complete the signal architecture. Full sprint definitions are in
`Delivery_Sprint_Plan_v5.2.md` — Phase 5.

| Sprint | Scope | Outcome |
|--------|-------|---------|
| KB-S13 | Insight module wiring — homa_ir, remnant_cholesterol, tyg_index, fib_4 | Zero unmapped pipeline warnings; derived metrics produce insight output |
| KB-S14 | Signal evaluator implementation — SignalRegistry + SignalEvaluator + SignalResult | All 12 signals evaluate at runtime; ADR-005 invariants enforced by tests |
| KB-S15 | Signal evaluator runtime integration — wired into orchestrator, signal states in InsightGraph | Signal states present in every pipeline run |
| KB-S16 | End-to-end blood panel assessment test suite | Full deterministic test from raw panel to signal-enriched InsightGraph; replay verified |

**KB-S16 is the testable milestone.** At completion, HealthIQ AI delivers a deterministic
end-to-end blood panel assessment with biological signal detection, replay integrity, and
`lab_normal_but_flagged` surfacing.

---

# 9. Role of the Knowledge Bus

The Knowledge Bus is the research ingestion pipeline that feeds the signal library.

Scientific research papers are converted into structured knowledge packages via a defined
prompt template and research process. Each package produces a validated `signal_library.yaml`
that is loaded by the signal engine at runtime.

The platform therefore evolves through the continuous addition of new signals derived from
primary biomedical research — without touching computation code.

The Knowledge Bus validator enforces:

- Canonical identifier compliance (`^[a-z0-9_]+$`)
- Threshold provenance (each threshold must carry a research citation)
- Schema completeness (all required fields present)
- Cycle detection (no signal-to-signal dependencies at Layer 1)
- Activation logic constraint (`deterministic_threshold` only)

---

# 10. Strategic Outcome

Completing the signal architecture transforms HealthIQ from a deterministic analytical
substrate into a biological intelligence platform.

This architecture supports multiple product categories:

- Consumer health applications
- Clinical decision support tools
- Longevity medicine platforms
- Research analytics systems

The signal library is the core intellectual property. The architectural discipline surrounding
it — deterministic execution, research provenance, replay integrity, validated schema contract,
`lab_normal_but_flagged` surfacing — is what makes it defensible.

From the Master Roadmap v5.2→v5.3:

> *Proprietary inference behavior is defensible because it accumulates through structured
> rule interaction, conflict policy, longitudinal state logic, and calibrated outcome
> alignment. Replay determinism supports regulatory credibility by enabling exact
> reconstruction, auditability, and controlled evolution of inference assets.*

---

# 11. What Has Been Built vs What Remains

## Built and Locked

| Component | Location | Status |
|-----------|----------|--------|
| Signal schema contract | `knowledge_bus/packages/*/signal_library.yaml` | 12 signals, 6 packages |
| Signal validator | `backend/scripts/validate_signal_library.py` | Full schema enforcement |
| ADR-005 implementation spec | `architecture/ADR-005-*` | Complete design spec |
| RatioRegistry (15 derived metrics) | `backend/core/analytics/ratio_registry.py` | Production |
| Age injection for fib_4 | `backend/core/pipeline/orchestrator.py` | Production (KB-S11) |
| SSOT registration | `backend/ssot/biomarkers.yaml` | remnant_cholesterol, homa_ir, fib_4 (KB-S12) |
| InsightGraph contract | `backend/core/contracts/insight_graph_v1.py` | Frozen, `extra="forbid"` |
| ClusterEngineV2 | `backend/core/clustering/cluster_engine_v2.py` | Production |
| Layer 3 insight assembler | `backend/core/layer3/insight_assembler_v1.py` | Production |

## Remaining (KB-S13 → KB-S16)

| Component | Location | Status |
|-----------|----------|--------|
| Insight module wiring | orchestrator + insight modules | KB-S13 |
| SignalRegistry | `backend/core/analytics/signal_evaluator.py` | KB-S14 |
| SignalEvaluator | `backend/core/analytics/signal_evaluator.py` | KB-S14 |
| SignalResult | `backend/core/analytics/signal_evaluator.py` | KB-S14 |
| Runtime integration | `backend/core/pipeline/orchestrator.py` | KB-S15 |
| End-to-end test suite | `backend/tests/` | KB-S16 |
