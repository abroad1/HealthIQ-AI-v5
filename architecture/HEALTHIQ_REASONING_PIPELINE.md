# HealthIQ Canonical Reasoning Pipeline

**Status:** Canonical — all platform development must align with this document
**Date:** 2026-03-08
**References:** ADR-003, ADR-005

---

## Purpose

This document defines the canonical reasoning model of the HealthIQ platform.
It is the single authoritative explanation of how the platform moves from published
biomedical research to a user-facing health insight.

Every engineer, sprint, AI agent, and architectural decision working on this platform
must be able to place their work within this pipeline. If work cannot be placed within
it, that is a signal that the work either violates the architecture or that the pipeline
requires a formal amendment (via a new ADR).

---

## The Reasoning Model

```
Research Evidence
      ↓
Knowledge Bus Packages
      ↓
Signal Library
      ↓
Signal Registry
      ↓
Signal Evaluation Engine
      ↓
Insight Graph
      ↓
User Narrative Output
```

The pipeline has one direction. Data flows forward. No stage reads backward.
Each stage has a single, exclusive responsibility.

The pipeline embodies three architectural invariants that must never be violated:

> **Invariant A — Evidence produces Signals**
> Every signal threshold must originate from a Knowledge Bus package backed by
> published research. No threshold may exist without an evidence anchor.

> **Invariant B — Signals produce Insights**
> Insights are constructed from signal states. They are never constructed directly
> from raw biomarker values or from lab reference ranges.

> **Invariant C — Signals evaluate raw biomarker values only**
> The Signal Evaluation Engine receives raw numeric values. It never receives
> pre-classified statuses, traffic-light flags, or frontend classifications.
> Pre-classification destroys disease-specific intelligence before it can be computed.

---

## Stage-by-Stage Definition

---

### Stage 1 — Research Evidence

**What it is:**
Published biomedical research — prospective cohort studies, meta-analyses, RCTs,
and clinical guidelines — that establishes which biomarker values are associated
with specific disease outcomes, at what thresholds, in what populations.

**What it produces:**
Structured research reports (`.md` format) translated by the Claude Translation
Engine into Knowledge Bus packages.

**Governing rule:**
Research conclusions are followed to the letter. Thresholds are used exactly as
stated for the disease being studied. No substitution from a different condition's
classification is permitted. (ADR-003)

**Key files:**
- `knowledge_bus/research/study_0N_*.md` — source research reports
- `knowledge_bus/research/RESEARCH_PROMPT_TEMPLATE.md` — LLM research prompt
- `knowledge_bus/research/study_topics_metabolic_core.md` — study programme

---

### Stage 2 — Knowledge Bus Packages

**What it is:**
The structured, validated representation of research evidence in machine-readable form.
Each KB package contains three components:

- `research_brief.yaml` — evidence sources, biomarkers, physiological claim
- `signal_library.yaml` — signal definitions, disease-specific thresholds, override rules
- `clinical_signoff.md` — pending decisions and human clinical reviewer sign-off

**What it produces:**
Validated, signed-off signal definitions ready for runtime use.

**Governing rule:**
No KB package may proceed to runtime implementation without passing the KB validator
and receiving a completed clinical sign-off. (ADR-003)

**Key files:**
- `knowledge_bus/packages/KBP-XXXX/` — individual packages
- `backend/scripts/validate_knowledge_package.py` — validator

---

### Stage 3 — Signal Library

**What it is:**
The complete set of active, validated `signal_library.yaml` definitions across all
accepted Knowledge Bus packages. Each signal library entry defines:

- A biological question the signal answers
- The primary metric and its disease-specific threshold tiers
- Supporting metrics with evidence-anchored thresholds
- Override rules (escalation only)
- The bundle consumers downstream

**What it produces:**
The authoritative reference for all disease-specific thresholds in the platform.

**Governing rule:**
`signal_library.yaml` is the single source of truth for all clinical thresholds.
No threshold value may exist anywhere else in the codebase. (ADR-005, Invariant 4)

**Supporting metrics schema:**
Two fields coexist in the signal library:
- `supporting_metrics` — contextual markers (name-list only; no research threshold declared)
- `supporting_metrics_with_thresholds` — evidence-anchored supporting markers with
  explicit thresholds for deterministic evaluation by the Signal Evaluation Engine

Both fields are valid. They serve different purposes and must not be merged.

---

### Stage 4 — Signal Registry

**What it is:**
The in-process compiled representation of all active signal library definitions,
loaded once at service startup. The `SignalRegistry` class reads all
`signal_library.yaml` packages from the Knowledge Bus directory and compiles
them into runtime objects.

**What it produces:**
A compiled, validated set of signal objects passed to the Signal Evaluation Engine
at runtime.

**Governing rule:**
Signals are loaded once at startup, not per execution. This ensures deterministic
behaviour and correct performance at scale (200+ signals). (ADR-005)

**Key file (to be created in KB-S10):**
- `backend/core/analytics/signal_registry.py`

---

### Stage 5 — Signal Evaluation Engine

**What it is:**
The biological reasoning core of the platform. The Signal Evaluation Engine receives
raw biomarker values and derived metric values and evaluates each registered signal
independently against its disease-specific thresholds.

**What it produces:**
One `SignalResult` per active signal, each containing:
- `signal_id` — which signal was evaluated
- `state` — `optimal` / `suboptimal` / `at_risk`
- `primary_metric` and `primary_value` — what was evaluated
- `supporting_states` — supporting metric values and whether they are elevated
- `lab_normal_but_flagged` — `true` when the biomarker is within lab normal range
  but the signal classifies it as suboptimal or at_risk (the intelligence moat)
- `evidence` — the research anchor for the classification

**Governing rule:**
Governed by ADR-005 in full. The engine accepts `Dict[str, float]` only. Signals
evaluate independently. No signal reads another signal's output.

**Key file (to be created in KB-S10):**
- `backend/core/analytics/signal_evaluator.py`

---

### Stage 6 — Insight Graph

**What it is:**
The Layer D component that receives signal results and constructs a structured
representation of the user's health state. The Insight Graph organises signal
outputs into clinically coherent clusters and prepares them for narrative generation.

**What it produces:**
A structured `InsightGraph` object — signal states organised by physiological system,
with supporting context, confidence, and evidence references — ready for LLM narrative
generation.

**Governing rule:**
The Insight Graph reads signal states from the Signal Evaluation Engine. It does not
perform clinical threshold evaluation. It does not consume raw biomarker values for
clinical interpretation. Lab reference range statuses are consumed for display context
only (Layer 1 output), separate from signal state interpretation (Layer 2 output).
(ADR-002, ADR-005)

**Key file:**
- `backend/core/analytics/insight_graph_builder.py`

---

### Stage 7 — User Narrative Output

**What it is:**
The LLM-assisted translation of structured Insight Graph outputs into personalised,
human-readable health narratives. This is the only stage where non-deterministic
inference is permitted.

**What it produces:**
The user-facing output: health insights, risk explanations, supporting marker context,
and evidence citations.

**Governing rule:**
Layer D performs no clinical computation. It receives structured signal states and
translates them into language. It does not re-evaluate, re-classify, or override any
signal state it receives. Any computation in this layer that belongs in Stage 5 is an
architectural defect. (ADR-002)

---

## The Intelligence Moat — Where the Platform Differentiates

The highest-value output the platform produces occurs at the intersection of Stage 5
and Stage 6: the **lab-normal-but-signal-flagged case**.

```
Biomarker:   hs-CRP = 2.5 mg/L
Lab range:   0–10 mg/L  →  Lab verdict: NORMAL

Signal:      signal_systemic_inflammation
Threshold:   ≥ 2.0 mg/L (JUPITER trial; ACC/AHA 2025)
Signal verdict: AT RISK

Supporting:  NLR = 2.1 (above 1.67 MetS cutoff)
             TyG = 8.6  (suboptimal IR range)

Output:      "Your CRP is within the lab's normal range. However, at 2.5 mg/L it
              exceeds the residual inflammatory risk threshold from clinical trial
              evidence. This is corroborated by an elevated NLR and suboptimal TyG
              index — a pattern associated with early metabolic inflammatory burden."
```

This output is only possible if:
1. The raw CRP value reaches the Signal Evaluation Engine uncollapsed (Stage 5)
2. The signal threshold is evidence-anchored in the signal library (Stage 3)
3. Supporting metric thresholds are declared and evaluated (Stage 5)
4. The `lab_normal_but_flagged` flag is preserved to the Insight Graph (Stage 6)
5. The narrative layer cites the evidence anchor (Stage 7)

Breaking the pipeline at any point between Stages 3 and 6 destroys this output.

---

## Current Implementation Status

| Stage | Component | Status |
|-------|-----------|--------|
| 1 — Research Evidence | Studies 1–4 complete; 5–10 pending | Partial |
| 2 — Knowledge Bus Packages | KBP-0002 through KBP-0005 validated | Pending clinical sign-off |
| 3 — Signal Library | 4 packages ready | Pending sign-off |
| 4 — Signal Registry | Not yet built | KB-S10 |
| 5 — Signal Evaluation Engine | Not yet built | KB-S10 |
| 6 — Insight Graph | Built; contains hardcoded thresholds to remove | KB-S10 refactor |
| 7 — User Narrative Output | Built | Active |

---

## References

- `architecture/ADR-003-knowledge-bus-architecture.md` — governs Stages 1–3
- `architecture/ADR-005-disease-specific-signal-evaluation-v2.md` — governs Stages 4–5
- `architecture/ADR-002-deterministic-analysis-engine.md` — governs layer boundaries
- `architecture/ARCHITECTURE_GUARDRAILS.md` — enforceable rules derived from this pipeline
- `docs/RESEARCH_KNOWLEDGE_PIPELINE_v1.md` — earlier pipeline design document
- `docs/DISEASE_SPECIFIC_THRESHOLD_ARCHITECTURE.md` — design record for Stage 5
