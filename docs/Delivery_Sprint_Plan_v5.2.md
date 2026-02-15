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
We are executing Delivery Plan v5.1
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

