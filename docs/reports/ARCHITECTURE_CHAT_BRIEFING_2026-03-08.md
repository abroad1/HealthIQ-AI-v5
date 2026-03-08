# Architecture Chat Briefing — 2026-03-08
## HealthIQ AI v5 — Knowledge Bus Programme Status

**Branch:** `feature/research-ingestion-bus-contract`
**Prepared for:** Product Architecture Review
**Prepared by:** Claude Code

---

## What exists today

### 1. Architecture Decision Registry — NEW

A formal ADR registry has been established at `architecture/` in the repository.

| ADR | Title | Status |
|-----|-------|--------|
| ADR-001 | Platform Non-Negotiables and Governance Invariants | Accepted |
| ADR-002 | Deterministic Three-Layer Analysis Architecture | Accepted |
| ADR-003 | Knowledge Bus Evidence Architecture | Accepted |
| ADR-004 | Disease-Specific Signal Evaluation Architecture | Superseded |
| ADR-005 | Disease-Specific Signal Evaluation Architecture (v2) | Accepted |

ADR-004 was superseded on the same day it was created following your architecture
review. The three corrections — compound intelligence inside the signal evaluator,
SignalRegistry startup pattern, and signal independence as a hard invariant — are
incorporated in ADR-005. The full decision history is preserved.

**Key file:** `architecture/ARCHITECTURE_INDEX.md`

---

### 2. Knowledge Bus Packages — Research Translation

Four KB packages have been translated from research reports and validated. All pass
the KB validator (`ready_for_implementation: True`). All are pending clinical sign-off
before Layer B implementation.

| Package | Signal | Mode | Primary metric | At-risk threshold | Evidence |
|---------|--------|------|---------------|-------------------|----------|
| KBP-0002 | `signal_insulin_resistance` | Confirmation | `derived.tyg_index` | ≥ 8.50 | Navarro-González meta-analysis |
| KBP-0003 | `signal_lipid_transport_dysfunction` | Creation | `derived.non_hdl_cholesterol` | ≥ 5.7 mmol/L | Lancet 2019, n=398,846 |
| KBP-0004 | `signal_hepatic_metabolic_stress` | Creation | `derived.tyg_index` | ≥ 8.97 (hepatic) | Zhang/Zheng meta-analysis, n=105,365 |
| KBP-0005 | `signal_systemic_inflammation` | Creation | `crp` | ≥ 2.0 mg/L | JUPITER trial; ACC/AHA 2025 |

Note: KBP-0002 and KBP-0004 both use `derived.tyg_index` but with different
thresholds (8.50 vs 8.97) because they target different diseases. This validates
the "threshold belongs to the signal not the biomarker" principle.

**Key directory:** `knowledge_bus/packages/`

---

### 3. Research Pipeline Infrastructure

**Research prompt template** (`knowledge_bus/research/RESEARCH_PROMPT_TEMPLATE.md`):
A generic prompt for the deep research LLM that produces structured evidence reports
in a consistent format. Includes the Platform Data Availability Reference (lifestyle
registry, questionnaire inputs) and the new disease-specific threshold rule.

**Research study library** (`knowledge_bus/research/`):
- `study_topics_metabolic_core.md` — 10 prioritised study topics
- `study_01` through `study_04` — completed research reports
- Studies 5–10 are pending research report delivery

**Governance rule confirmed this session:**
> Follow research conclusions to the letter. The threshold belongs to the signal,
> not the biomarker. Do not substitute a general-purpose classification for a
> disease-specific research threshold.

This rule was triggered by KBP-0005: the translation engine initially used 3.0 mg/L
for hs-CRP (the traditional ACC/AHA three-tier boundary) instead of 2.0 mg/L (the
explicit RIR threshold stated in the research conclusions). Caught in review, corrected,
and formalised as ADR-003 Invariant.

---

### 4. Supporting Design Documents

| Document | Purpose |
|----------|---------|
| `docs/DISEASE_SPECIFIC_THRESHOLD_ARCHITECTURE.md` | Full design record for the intelligence moat concept |
| `docs/CLAUDE_TRANSLATION_SPEC_v1.md` | KB translation specification |
| `docs/KNOWLEDGE_BUS_SOP_v1.2.md` | KB governance SOP |
| `docs/AUTOMATION_BUS_SOP_v1.2.md` | Execution governance SOP |

---

## Open engineering items for your input

### KB-S9 — Derived metrics (must precede KB-S10)

| Metric | Required by | Status |
|--------|-------------|--------|
| `derived.tyg_index` | KBP-0002, KBP-0004 | Not in `ratio_registry.py` |
| `derived.tyg_bmi_index` | KBP-0004 (pending Decision 1) | Not in `ratio_registry.py` |
| `derived.sii` | KBP-0005 | Not in `ratio_registry.py` |
| HOMA-IR divisor confirmation | KBP-0002 | 405 (mg/dL) vs 22.5 (mmol/L) — unresolved |

**Also flagged for KB-S9:** the `supporting_metrics_with_thresholds` field (per ADR-005)
needs to be added to all existing KB package signal libraries. This makes supporting
metric evaluation fully declarative.

### KB-S10 — Signal Evaluation Engine (the intelligence layer)

Per ADR-005, the following must be built:

1. `SignalRegistry` — loads and compiles all KB packages at startup
2. `SignalEvaluator` — evaluates signals against raw `Dict[str, float]` values only;
   never accepts pre-classified statuses
3. Remove hardcoded CRP threshold in `insight_graph_builder.py` (lines 97–117)
4. Wire signal evaluator into `orchestrator.py` before status classification
5. `lab_normal_but_flagged` flag in signal output DTO — preserves the intelligence moat

### Clinical sign-off — 4 packages pending

All four KB packages require a named clinical reviewer to complete `clinical_signoff.md`
before any package is promoted to Layer B. Key open decisions:

- **KBP-0004 Decision 1:** TyG vs TyG-BMI as primary metric (TyG-BMI now confirmed
  available via `lifestyle_registry.yaml` — not blocked)
- **KBP-0001 delta:** `signal_systemic_inflammation` in KBP-0001 uses 3.0/10.0 mg/L;
  KBP-0005 uses 1.0/2.0 mg/L. Both cannot be active simultaneously.

### Studies 5–10 — pending research report delivery

| # | Topic | Key signals |
|---|-------|-------------|
| 5 | Metabolic Syndrome Pattern Detection | TG, HDL, glucose, BP, waist circumference |
| 6 | Mitochondrial Energy Efficiency | lactate, glucose, metabolic ratios |
| 7 | Cardiovascular Metabolic Risk | QRISK/Framingham models |
| 8 | Kidney Metabolic Stress | creatinine, eGFR, urea |
| 9 | Biological Age / Metabolic Age | composite of all prior signals |
| 10 | Brain Metabolic Health | insulin resistance, inflammation, vascular, lipids |

---

## One architectural question for your review

ADR-005 introduces `supporting_metrics_with_thresholds` as a new field in the
`signal_library.yaml` schema — making supporting metric thresholds fully declarative
and generically evaluated by the Signal Evaluation Engine.

**Question:** Should the existing `supporting_metrics` list (name-only) be deprecated
in favour of `supporting_metrics_with_thresholds`, or retained for signals where a
supporting metric is contextual only (no research threshold to declare)?

The current KB packages use `supporting_metrics` as a name list. KB-S9 would need
to add `supporting_metrics_with_thresholds` to each where evidence-anchored thresholds
exist. Your call on whether both fields coexist or whether we deprecate the name-only
version entirely.

---

*End of briefing. All assets are committed to `feature/research-ingestion-bus-contract`.*
