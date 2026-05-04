**Health IQ AI v5 Delivery & Sprint Plan v5.2**.

This document pair (Master_PRD_v5.2 + Delivery_Sprint_Plan_v5.2) forms the authoritative architectural baseline for HealthIQ v5.2.
All future sprint execution and implementation must reference these documents explicitly.

This document is designed to be:

* Referencable across chat windows
* Executable by Cursor
* Traceable against the Master PRD
* Structured enough for engineering discipline
* Clear enough for new team members
* **Safety-first** — P0 infrastructure sequenced first

*Amendment v5.0 → v5.1: Sequencing Refinement. Sprint order adjusted based on safety-first architecture.*  
*Amendment v5.1 → v5.2: Documentation Hardening. Structural clarifications; no runtime changes.*

**Version:** 5.2  
**Status:** Active  
**Type:** Architecture Baseline Freeze  
**Scope:** Documentation Hardening Only (No Runtime Changes)

**Linked To:** Master_PRD_v5.2.md  
**Owner:** Product / Architecture

Previous versions should be stored under /docs/archive/.

---

# Health IQ AI

# Delivery & Sprint Plan

---

# 1. Execution Philosophy

This roadmap converts the Master PRD into:

* Sequential, isolated build phases
* **Safety-first sequencing** — P0 infrastructure before clinical depth
* Test-gated architectural milestones
* Stable integration points
* No cross-layer contamination

Each sprint must:

* Deliver deterministic, test-covered functionality
* Not introduce LLM logic into Layer B
* Maintain snapshot immutability
* Pass full regression suite

v4 codebase files are reference-only and must never be imported into the v5 runtime.

---

# 1.1 Execution Status (Current Baseline)

Status update to align documentation with delivered runtime state.

| Sprint | Scope (short) | Status |
|--------|----------------|--------|
| 1 | Hard-typed unit registry | Complete |
| 2 | Lab-origin metadata and variance flag | Complete |
| 3 | Criticality and missing-data confidence | Complete |
| 4 | Derived ratio registry (static bounds) | Complete |
| 5 | Ratio centralisation | Complete |
| 6 | Cluster schema refactor | Complete |
| 7 | InsightGraph contract implementation | Complete |
| 8 | Confidence model + boundary hardening | Complete |
| 9 | Replay/stamping foundation | Complete |
| 10 | RelationshipRegistry_v1 + replay stamping | Complete |
| 11 | BiomarkerContext_v1 + replay stamping | Complete |

Remaining v5.2 execution is re-ordered below to be depth-enabling and deterministic.

## 1.2 Remaining v5.2 — Depth-Enabling Order

1. **SSOT scoring policy migration**  
   Migrate remaining hardcoded scoring thresholds/weights into versioned SSOT policy artifacts. This reduces policy drift and improves replay/audit traceability.

2. **Runtime convergence (single clustering path)**  
   Converge production clustering to one deterministic runtime path and quarantine inactive engines from production execution to remove architectural ambiguity.

3. **Deterministic failure envelope** *(Added to support depth)*  
   Define deterministic failure artifacts for replay compatibility, replacing non-deterministic fallback characteristics in failure outputs.

4. **Runtime purity governance invariants** *(Added to support depth)*  
   Add enforcement-level governance to prevent legacy/non-authoritative runtime paths from re-entering production flows.

---

# 2. Phase Overview

V5.1 delivery is divided into four macro phases, with **Phase 1 containing all safety-critical systems**:

---

## Phase 1 — Deterministic Safety Infrastructure (P0)

This phase now contains all safety-critical systems.

**Sprints:**

1. Hard-Typed Unit Registry (Two-Step Model)
2. Lab Header Detection & Lab-Origin Metadata
3. Biomarker Criticality & Missing Data Logic

---

## Phase 2 — Clinical Depth (Core v5)

**Sprints:**

4. Derived Ratio Registry (Static Bounds Only)
5. Derived Ratio Centralisation *(explicit refactor)*
6. Cluster Definition Schema Refactor
7. InsightGraph Contract Implementation
8. InsightGraph Contract Freeze *(before any narrative layer work)*
9. cluster_engine_v2 Migration

---

## Phase 3 — Deterministic Stabilisation

**Sprint:**

10. Snapshot Hardening & Replay Validation

---

## Phase 4 — Strategic Moat (P2 Evolution)

**Sprints:**

11. Snapshot Linking & Delta Engine
12. Velocity & Stability Metrics
13. Demographic Partition Activation (Literature-Gated)

---

# 3. Detailed Sprint Definitions

---

# Phase 1 — Deterministic Safety Infrastructure (P0)

---

## Sprint 1 — Hard-Typed Unit Registry (Two-Step Model)

**PRD Reference:** §3.2

### Includes:

* Base unit standardisation
* ConversionMatrix
* Snapshot conversion logging
* UnitEnum enforcement
* Full unit regression tests

### Deliverables:

* unit_registry.py
* conversion_matrix.py
* UnitEnum
* Conversion tests (full coverage)

### Definition of Done:

* All scoring math uses base units only
* No string-based unit logic remains
* Full unit regression suite passes

---

## Sprint 2 — Lab Header Detection & Lab-Origin Metadata

**PRD Reference:** §3.3 (P0 Safety Infrastructure)

### Includes:

* Lab provider detection logic
* Metadata extraction
* `lab_reference_profile_hash` generation
* ContextualVarianceFlag
* InsightGraph integration

### Deliverables:

* Lab detection module
* Metadata capture in snapshot
* ContextualVarianceFlag surfaced in InsightGraph

### Definition of Done:

* Lab-origin differences detectable
* Flag surfaced in InsightGraph

---

## Sprint 3 — Biomarker Criticality & Missing Data Logic

**PRD Reference:** §4.3 & §4.4

### Includes:

* Criticality registry
* Confidence degradation engine
* `required_for_cluster` enforcement
* Missing marker exposure

### Deliverables:

* Criticality registry
* Confidence calculation module
* Snapshot confidence integration

### Definition of Done:

* Confidence mathematically derived
* Missing markers surfaced deterministically

### Implemented (Sprint 3):

* `backend/ssot/criticality.yaml` — system-aware required/important/optional per health system
* `backend/core/analytics/criticality.py` — `load_criticality_policy()`, `evaluate_criticality()`
* Orchestrator wires criticality into result meta; `/api/analysis/result` returns meta with criticality fields

---

# Phase 2 — Clinical Depth (Core v5)

---

## Sprint 4 — Derived Ratio Registry (Static Bounds Only)

**PRD Reference:** §3.4 & §4.5

### Includes:

* v5 ratio schema
* Centralised ratio engine
* Removal of local ratio logic
* Default static interpretation bounds
* Snapshot version stamping
* Demographic overrides architected but **inactive**

### Deliverables:

* Ratio registry loader
* Deterministic ratio engine
* Validation tests

### Definition of Done:

* All ratios computed centrally
* No duplicate local ratio calculations exist
* Snapshot includes derived markers

### Implemented (Sprint 4):

* `backend/core/analytics/ratio_registry.py` — RatioRegistry, compute()
* Orchestrator wires ratio computation after simple_biomarkers, before score_biomarkers
* tc_hdl_ratio, tg_hdl_ratio, ldl_hdl_ratio, non_hdl_cholesterol, apoB_apoA1_ratio (when apob+apoa1 present)
* Static bounds for tc/tg/ldl HDL applied via input_reference_ranges; meta["derived_ratios"] persists
* metabolic_age.py and heart_insight.py read lipid ratios from panel; no local computation
* Deferred: nlr, bun_creatinine_ratio, urea_creatinine_ratio, ast_alt_ratio

---

## Sprint 5 — Derived Ratio Centralisation

**PRD Reference:** §3.4 Derived Ratio Registry (Centralised Computation)

### Includes:

* Create RatioRegistry
* Compute all derived ratios in Layer B (single deterministic pipeline step)
* Remove local ratio calculations from insight modules
* Store all ratios in AnalysisSnapshot

### Deliverables:

* RatioRegistry implementation
* Layer B ratio computation pipeline
* Removal of duplicate ratio logic from insight modules
* Snapshot schema extension for derived ratios

### Definition of Done:

* All derived ratios (TG/HDL, TC/HDL, LDL/HDL, ApoB/ApoA1, NLR, AST/ALT, etc.) computed centrally
* No insight module performs ratio calculation locally
* Duplicate ratio calculations prohibited and enforced

---

## Sprint 6 — Cluster Definition Schema Refactor

**PRD Reference:** §4.2 & §6

### Includes:

* Schema-driven cluster definitions
* Removal of hardcoded cluster logic
* Validation layer
* Version stamping

### Deliverables:

* Cluster schema loader
* Validation layer
* Test coverage for all clusters

### Definition of Done:

* Clusters fully schema-driven
* No cluster logic duplicated in scoring engine

---

## Sprint 7 — InsightGraph Contract Implementation

**PRD Reference:** §4.6 & §4.7

### Includes:

* Strict output object
* Removal of direct scoring from narrative layer
* Structured interface enforcement
* Version stamping

### Deliverables:

* InsightGraph builder
* Contract validation

### Definition of Done:

* No scoring logic outside InsightGraph builder
* LLM consumes structured payload only
* No narrative layer performs independent scoring or ratio calculation

---

## Sprint 8 — InsightGraph Contract Freeze

**PRD Reference:** §4.7 InsightGraph v1 Contract

*Must complete before any narrative layer work.*

### Includes:

* Final InsightGraph_v1 schema lock
* Snapshot replay validation
* LLM isolation enforcement test

### Deliverables:

* Final InsightGraph_v1 schema
* Snapshot replay validation suite
* LLM isolation enforcement test (LLM never receives raw biomarker values)

### Definition of Done:

* InsightGraph_v1 schema frozen and version-stamped
* Replay produces identical structured output
* Test proves LLM receives only InsightGraph_v1, never raw biomarkers

---

## Sprint 9 — cluster_engine_v2 Migration

**PRD Reference:** §4.2 Canonical Clustering Engine Declaration

### Includes:

* Port all cluster logic to cluster_engine_v2
* Remove legacy ClusteringEngine
* Add regression tests for cluster parity

### Deliverables:

* cluster_engine_v2 production-ready
* Legacy engine removed
* Regression tests proving cluster output parity

### Definition of Done:

* All clustering uses cluster_engine_v2
* Legacy engine code removed
* No new logic in legacy engine; migration complete

---

### Regression Gate — Deterministic Integrity Check

*Must complete after Sprint 9 before proceeding to Phase 3.*

Must validate:

* Ratio centralisation integrity
* Canonical ID enforcement
* Cluster engine parity
* Snapshot replay determinism
* InsightGraph version validation

This is a testing milestone, not a new feature.

---

# Phase 3 — Deterministic Stabilisation

---

## Sprint 10 — Snapshot Hardening & Replay Validation

**PRD Reference:** §5

### Includes:

* Immutable snapshot enforcement
* Replay reproducibility test suite
* Cross-version validation detection

### Definition of Done:

* Snapshot replay reproduces identical output
* Version mismatches detectable

---

# Phase 4 — Strategic Moat (P2 Evolution)

---

## Sprint 11 — Snapshot Linking & Delta Engine

* Link Snapshot_n to Snapshot_n-1
* Implement delta calculations
* Store deltas in structured format

---

## Sprint 12 — Velocity & Stability Metrics

* Implement:

  * percent delta
  * rate-of-change
  * stability index
* Integrate temporal flags into InsightGraph

---

## Sprint 13 — Demographic Partition Activation (Literature-Gated)

**PRD Reference:** §4.5

* Activate demographic overrides only when literature-backed
* Enable `overrides_by_sex`, `overrides_by_age_range`, `overrides_by_population` per ratio
* Version all overrides
* No probabilistic or heuristic population modelling

---

# 4. Updated Priority Matrix

| Priority | Component | Classification |
|----------|-----------|----------------|
| **P0** | Unit Registry (Base Unit Model) | Safety |
| **P0** | Lab Header Detection | Safety |
| **P0** | Biomarker Criticality | Scientific Integrity |
| **P1** | Derived Ratio Registry | Clinical Depth |
| **P1** | Cluster Schema Refactor | Structural Integrity |
| **P1** | InsightGraph Contract | Architectural Boundary |
| **P2** | Velocity Engine | Competitive Moat |
| **P2** | Demographic Partitioning | Personalisation |

---

# 5. Execution Governance

Each sprint must:

* Pass full regression suite
* Maintain deterministic isolation
* Avoid importing v4 artifacts
* Avoid introducing fallback parsers
* Avoid introducing LLM inference logic

Each sprint must produce:

* Schema validation tests
* Deterministic tests
* Integration tests

---

# 6. Cross-Chat Referencing Protocol

When opening a new chat:

Always specify:

```
We are executing Delivery Plan v5.2
Current Phase: X
Current Sprint: Y
PRD Reference: Section Z
```

This prevents drift.

---

# 7. Success Definition for v5.1 Completion

v5.1 is complete when:

* Unit handling uses two-step base-unit model
* Lab-origin detection exists and flag is in InsightGraph
* Biomarker criticality is mathematically enforced
* Derived ratios are registry-driven
* Clusters are schema-driven
* InsightGraph is the sole narrative input
* Snapshot is immutable and replayable

---

# 8. Final Structural Reality

With v5.1:

**You now have:**

**Layer A:**

* Canonicalisation
* Base-unit normalisation
* Lab-origin awareness
* Derived biomarker registry

**Layer B:**

* Deterministic scoring
* Criticality-weighted confidence
* Schema-driven clusters
* InsightGraph generation

**Layer C:**

* Pure translation

**This is no longer a feature roadmap.**

**It is a systems architecture roadmap.**

---

# Phase 5 — Signal Intelligence Layer (KB Sprint Series)

*Amendment: added to reflect the Knowledge Bus sprint series executed under Automation Bus SOP v1.2. This phase completes the biological intelligence infrastructure and delivers a testable end-to-end blood panel assessment. Sprints are executed via the Automation Bus and audited by Claude before GPT architectural review and merge.*

---

## KB Sprint Series — Execution Status

| Sprint | Scope | Status |
|--------|-------|--------|
| KB-S10 | Derived ratio registry expansion (remnant_cholesterol, homa_ir, fib_4) + namespace validator | Complete |
| KB-S11 | Age injection from questionnaire date_of_birth to enable fib_4 computation | Complete |
| KB-S12 | SSOT biomarker registration (remnant_cholesterol, homa_ir, fib_4) | Complete |
| KB-S13 | Insight module wiring | Pending |
| KB-S14 | Signal evaluator implementation | Pending |
| KB-S15 | Signal evaluator runtime integration | Pending |
| KB-S16 | End-to-end blood panel assessment test suite | Pending |

---

## KB-S13 — Insight Module Wiring

**PRD Reference:** §4.2 (Cluster schema), §4.6 (InsightGraph)

**Context:**

KB-S10 through KB-S12 established three new derived metrics (remnant_cholesterol, homa_ir,
fib_4) in the ratio registry and SSOT. Post-KB-S12, two unmapped biomarker warnings remain
in the pipeline (`tyg_index`, `age`). KB-S13 resolves the remaining unmapped metric warnings
and wires all computed derived metrics into the appropriate insight modules so that the
pipeline produces insight output — not just computation output — for these markers.

### Includes:

* Register `tyg_index` in `backend/ssot/biomarkers.yaml`
* Wire `homa_ir`, `remnant_cholesterol`, `tyg_index` to their respective insight modules or cluster scoring paths
* Confirm `fib_4` wiring path is ready for when age is supplied
* Resolve `unmapped_age` pipeline warning

### Deliverables:

* `tyg_index` entry in `backend/ssot/biomarkers.yaml`
* Insight module or cluster mapping for homa_ir, remnant_cholesterol, tyg_index
* Zero unmapped biomarker warnings in golden pipeline run (excluding age when date_of_birth absent)

### Definition of Done:

* Pipeline verification PASS with no unexpected unmapped biomarker warnings
* homa_ir, remnant_cholesterol, tyg_index producing insight-level output
* Baseline tests PASS
* Kernel finish exit code 0

---

## KB-S14 — Signal Evaluator Implementation

**PRD Reference:** §4.6 (InsightGraph Layer B), Master Roadmap v5.3 §3.1 (Multi-Marker State Engine)

**Context:**

`backend/core/analytics/signal_evaluator.py` exists as a placeholder raising `NotImplementedError`.
ADR-005 defines the complete implementation specification. The knowledge bus packages (KBP-0001
through KBP-0005) contain validated `signal_library.yaml` files with 12 signals ready for
evaluation. This sprint implements the signal evaluation engine exactly as specified in ADR-005.

### Includes:

* `SignalRegistry` class — loads all `knowledge_bus/packages/*/signal_library.yaml` at service
  startup; validates schema; indexes by `signal_id`
* `SignalEvaluator` class — evaluates all registered signals independently against
  `Dict[str, float]` biomarker values and derived metric values; applies thresholds and
  override_rules deterministically
* `SignalResult` dataclass — output per evaluated signal:
  `signal_id`, `signal_state`, `signal_value`, `supporting_marker_states`, `confidence`,
  `lab_normal_but_flagged`
* Unit tests covering threshold evaluation, override escalation, missing-metric graceful
  degradation, and `lab_normal_but_flagged` detection

### Architectural Invariants (non-negotiable, from ADR-005):

* Raw values only — accepts `Dict[str, float]`; never pre-classified statuses
* Signals are independent evaluators — each signal evaluates independently; no signal reads
  another signal's output
* Zero clinical thresholds in code — all thresholds loaded from `signal_library.yaml` via
  `SignalRegistry`
* Override rules escalate only — may escalate severity, never downgrade
* `lab_normal_but_flagged` must surface — when a biomarker is within lab reference range but
  signal threshold fires, this must be explicitly flagged (platform differentiator)

### Deliverables:

* `SignalRegistry` — production implementation
* `SignalEvaluator` — production implementation
* `SignalResult` — dataclass
* Unit tests for all ADR-005 invariants
* `signal_evaluator.py` `NotImplementedError` removed

### Definition of Done:

* All 12 signals in current knowledge bus packages evaluate without error against the golden
  biomarker panel
* All ADR-005 architectural invariants enforced by tests
* Baseline tests PASS
* Kernel finish exit code 0

---

## KB-S15 — Signal Evaluator Runtime Integration

**PRD Reference:** §4.6 (InsightGraph), §4.7 (InsightGraph Contract Freeze)

**Context:**

KB-S14 delivers a standalone signal evaluation engine. KB-S15 wires it into the orchestrator
pipeline between derived ratio computation (Layer B) and InsightGraph assembly (Layer C).
Signal states become structured inputs to the InsightGraph, maintaining the `extra="forbid"`
contract boundary.

### Includes:

* Wire `SignalEvaluator.evaluate_all()` into `orchestrator.run()` after `compute(simple_biomarkers)`
  and before InsightGraph assembly
* Pass derived metric output from `ratio_registry.compute()` as `derived_metrics` input to
  signal evaluator
* Add `signal_results: List[SignalResult]` to InsightGraph structured output (version-stamped)
* Ensure existing InsightGraph consumers remain unaffected (additive-only change)
* Integration test: golden panel in → signal states present in InsightGraph output

### Deliverables:

* Signal evaluation wired into orchestrator runtime
* `signal_results` field in InsightGraph output
* Integration test confirming signal states present in pipeline output
* No regression to existing InsightGraph fields

### Definition of Done:

* At least one signal evaluates to a non-null state on the golden biomarker panel
* InsightGraph output contains `signal_results` field
* All existing InsightGraph fields unchanged (`extra="forbid"` maintained)
* Pipeline verification PASS
* Baseline tests PASS
* Kernel finish exit code 0

---

## KB-S16 — End-to-End Blood Panel Assessment Test Suite

**PRD Reference:** §5 (Snapshot Hardening), §4.7 (Replay Validation)

**Context:**

KB-S16 is the validation milestone for the full signal intelligence layer. It defines and
executes a comprehensive end-to-end test covering the complete pipeline from raw blood panel
input to signal-enriched InsightGraph output, with deterministic replay verification. This
sprint produces the golden fixture for the signal-era baseline and confirms the platform
delivers a testable end-to-end blood panel assessment.

### Includes:

* Golden blood panel fixture extended with `questionnaire_data` (date_of_birth) to enable
  fib_4 computation in the test harness
* End-to-end test: raw biomarkers in → Layer A (canonicalisation + normalisation) → Layer B
  (scoring + derived metrics + signal evaluation) → InsightGraph out
* Signal state assertions: confirm expected signal states for the golden panel (e.g.,
  `signal_insulin_resistance` state matches known panel values)
* Replay determinism test: run pipeline twice against same input, assert identical
  InsightGraph output including signal_results
* `fib_4` computation confirmed when date_of_birth present
* Regression guard: all prior golden fixture outputs unchanged

### Deliverables:

* Extended golden panel fixture with questionnaire_data
* End-to-end test script covering full pipeline
* Signal state assertions for all evaluable signals on golden panel
* Replay determinism assertion
* Confirmed pipeline output biomarker count and signal count

### Definition of Done:

* End-to-end test PASS from raw input to InsightGraph with signal states
* All signal states deterministic across two consecutive runs (replay test)
* fib_4 computes when date_of_birth supplied in golden fixture
* No regression to existing pipeline output
* Baseline tests PASS
* Pipeline verification PASS
* Kernel finish exit code 0

---

# 9. Success Definition for Phase 5 Completion

Phase 5 is complete when:

* All derived metrics (remnant_cholesterol, homa_ir, fib_4, tyg_index) produce insight-level
  output in the pipeline
* Signal evaluation engine loads all knowledge bus signal libraries at runtime
* Signal states are produced deterministically for every evaluated signal
* Signal states are present in InsightGraph output as a versioned, structured field
* `lab_normal_but_flagged` surfaces when signal threshold fires within lab-normal range
* End-to-end test passes from raw blood panel to signal-enriched InsightGraph
* Pipeline replay produces identical output including signal states
* Zero unmapped biomarker warnings for registered metrics
* All ADR-005 architectural invariants enforced by tests

**At Phase 5 completion, HealthIQ AI delivers a testable end-to-end deterministic blood
panel assessment with biological signal detection. This is the entry point to v5.3
biological intelligence expansion.**

---

# 10. Updated Execution State (Post KB-S12)

**Layer A — Complete:**

* Canonicalisation
* Base-unit normalisation
* Lab-origin awareness
* Derived biomarker registry (15 derived metrics including remnant_cholesterol, homa_ir, fib_4)
* Age injection from questionnaire date_of_birth (KB-S11)
* SSOT registration of all computed derived metrics (KB-S12)

**Layer B — Partially complete:**

* Deterministic scoring
* Criticality-weighted confidence
* Schema-driven clusters
* InsightGraph generation
* Signal evaluation engine — placeholder only; implementation scheduled KB-S14

**Layer C — Complete:**

* Pure narrative translation

**Knowledge Bus — Active:**

* 12 signals defined across 6 validated packages
* Signal validator enforcing schema contract
* Signal libraries ready for runtime evaluation pending KB-S14

