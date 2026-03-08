# ADR-002 — Deterministic Three-Layer Analysis Architecture

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Date** | 2026-03-08 |
| **Authority** | Master PRD v5.2 §2.4, §3, §4 |
| **Supersedes** | — |
| **Superseded by** | — |

---

## Context

HealthIQ AI v5 produces health insights from blood test data. The system must be
clinically credible, reproducible, and suitable for future regulatory alignment.
This requires a strict separation between:

- Deterministic analytical computation (which must produce identical outputs for
  identical inputs, always)
- Narrative generation (which uses LLM inference and is inherently non-deterministic)

Without this separation, clinical outputs become unreliable: the same blood test
uploaded twice could produce different risk classifications. This is unacceptable
for a health platform.

Additionally, the system must distinguish between:
- What a lab reports as normal/abnormal (population reference ranges)
- What clinical research says about risk at specific disease-targeted thresholds

Mixing these two concerns in the same computation layer destroys clinical value.

---

## Decision

The platform is built as a strict three-layer architecture. Each layer has an
exclusive responsibility and must not perform the work of another layer.

---

## The Three Layers

### Layer A — Canonicalisation and Normalisation

**Responsibility:** Convert raw lab input into canonical analytical form.

**What it does:**
- Resolves biomarker aliases to canonical SSOT names
  (`"hs_crp"` → `"crp"`, `"c-reactive_protein"` → `"crp"`)
- Converts units to canonical base units (mmol/L for lipids and glucose; IU/L for
  enzymes; g/L for proteins)
- Preserves the lab's own reference range as input metadata
- Rejects unresolvable inputs deterministically — no silent fallbacks

**What it must not do:**
- Perform any clinical interpretation
- Apply any threshold or scoring logic
- Make any determination about whether a value is "normal" or "abnormal"

**Key file:** `backend/ssot/biomarkers.yaml` (alias registry)

---

### Layer B — Deterministic Intelligence Engine

**Responsibility:** Transform canonical biomarker values into structured analytical
outputs through deterministic computation.

**What it does:**
- Computes derived metrics (ratios, indices) via `ratio_registry.py`
- Evaluates disease-specific signal thresholds from Knowledge Bus packages
- Applies override rules
- Produces confidence scores, cluster assignments, and signal states
- All computation is deterministic: identical inputs always produce identical outputs

**What it must not do:**
- Perform any LLM inference or narrative generation
- Apply lab reference ranges as clinical thresholds (lab ranges are Layer A metadata,
  not Layer B analytical inputs)
- Contain any hardcoded clinical threshold constants — all thresholds live in
  `signal_library.yaml` (see ADR-003 and ADR-004)

**Key files:**
- `backend/core/analytics/ratio_registry.py` — derived metric computation
- `backend/core/analytics/signal_evaluator.py` — signal threshold evaluation (KB-S10)
- `backend/core/analytics/insight_graph_builder.py` — graph construction
- `backend/core/pipeline/orchestrator.py` — pipeline coordination

---

### Layer C — Narrative Translation

**Responsibility:** Translate structured Layer B outputs into human-readable insights.

**What it does:**
- Receives structured signal states, cluster outputs, and confidence scores from Layer B
- Uses LLM inference to generate personalised narrative explanations
- Formats outputs for the frontend

**What it must not do:**
- Perform any deterministic clinical computation
- Apply any threshold values
- Modify or reinterpret the signal states it receives from Layer B
- Act as a fallback computation layer if Layer B outputs are incomplete

**Invariant:** Any computation performed in Layer C that belongs in Layer B is an
**architectural defect** and must be treated as a blocking governance violation.

---

## Architectural Invariants

1. **Layer boundaries are inviolable.** No layer may perform the responsibilities of
   another layer. Layer C must not compute. Layer B must not narrate.

2. **All clinical computation is deterministic.** Identical biomarker inputs must
   always produce identical signal states and scores. Non-determinism in clinical
   outputs is a platform defect.

3. **Lab reference ranges are metadata, not thresholds.** A lab reference range
   (e.g., CRP 0–10 mg/L) is preserved for display context only. It must not be used
   as a clinical threshold in Layer B signal evaluation. Layer B thresholds are defined
   in `signal_library.yaml` packages only.

4. **No hardcoded clinical constants in runtime code.** No numeric threshold value
   (e.g., `if crp > 1.0`) may appear in `insight_graph_builder.py`, bundle logic, or
   any Layer C file. All thresholds are loaded from the Knowledge Bus at runtime.

5. **Unit normalisation happens once, in Layer A.** Layer B operates exclusively on
   canonical base units. No unit conversion logic appears in Layer B or C.

---

## Consequences

- `insight_graph_builder.py` must be refactored in KB-S10 to remove all hardcoded
  threshold logic (e.g., `if crp > 1.0`)
- The Signal Evaluation Engine (`signal_evaluator.py`) must be introduced as the
  Layer B component that reads and evaluates KB packages
- Any future sprint that adds clinical logic to Layer C code must be rejected at audit
- The golden gate check should be extended to detect numeric threshold constants in
  Layer B/C code

---

## Source Documents

- `docs/Master_PRD_v5.2.md` §2.4 — layer separation
- `docs/Master_PRD_v5.2.md` §3 — Layer A specification
- `docs/Master_PRD_v5.2.md` §4 — Layer B specification
- `docs/DISEASE_SPECIFIC_THRESHOLD_ARCHITECTURE.md` — threshold architecture detail
