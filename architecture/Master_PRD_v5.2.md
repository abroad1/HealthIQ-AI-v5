**Master Architecture & Analytical Core PRD v5.2**.

This document pair (Master_PRD_v5.2 + Delivery_Sprint_Plan_v5.2) forms the authoritative architectural baseline for HealthIQ v5.2.
All future sprint execution and implementation must reference these documents explicitly.

This is written to be shareable with engineering, product, and external technical advisors.

This is the constitutional document. It does not contain sprint detail. It defines what we are building.

*Amendment v5.0 → v5.1: Architectural Refinement Pass. This is an amendment to v5.0, not a rewrite.*  
*Amendment v5.1 → v5.2: Documentation Hardening Pass. Structural clarifications only; no runtime changes.*

**Version:** 5.2  
**Status:** Active  
**Type:** Architecture Baseline Freeze  
**Scope:** Documentation Hardening Only (No Runtime Changes)

**Owner:** Product / Systems Architecture

Previous versions should be stored under /docs/archive/.

---

# Health IQ AI

# Analytical Core Master PRD

---

# 1. Executive Vision

Health IQ AI v5.1 is not a blood report generator.

It is a **Deterministic Biological Intelligence Engine** that:

* Normalises heterogeneous laboratory data
* Applies clinically defensible analytical logic
* Detects systemic biological patterns
* Generates structured insight graphs
* Delegates human-readable translation to an LLM

The system must:

* Be auditable
* Be versionable
* Be reproducible
* Be regulator-ready
* Be longitudinally extensible

The architecture must allow Health IQ AI to become the **reference platform for personal blood analytics**.

---

# 2. Architectural Philosophy

## 2.1 Deterministic Sovereignty

All clinical interpretation, scoring, clustering, and ratio logic must be deterministic.

The LLM:

* Does not calculate
* Does not classify
* Does not score
* Does not infer

The LLM translates only.

---

## 2.2 Lab-Range Sovereignty

For individual biomarkers:

* The lab-provided reference range is the authoritative source.
* Global “static” ranges are not used for interpretation of primary markers.

Exception:

* Derived ratios (see §6)

---

## 2.3 Snapshot Immutability

Each analysis produces an immutable `AnalysisSnapshot`.

An insight must be reproducible by replaying:

* Raw inputs
* Derived markers
* Reference ranges
* Scoring rules
* Versioned cluster definitions
* Versioned ratio registry

---

## 2.4 Layer Separation

### Layer A — Canonicalisation & Normalisation

### Layer B — Deterministic Intelligence Engine

### Layer C — Narrative Translation (LLM)

Layer C consumes structured outputs only.

---

# 3. Layer A — Canonicalisation & Data Normalisation

Layer A is responsible for converting unstructured or semi-structured lab data into canonical analytical inputs.

---

## 3.1 Biomarker Canonicalisation

Inputs:

* Alias name
* Value
* Unit
* Lab reference range

Outputs:

* Canonical biomarker ID
* Canonical unit
* Standardised numeric value
* Position within lab range
* Confidence of alias match

Alias resolution must be deterministic and versioned.

No fuzzy matching.

---

## 3.2 Hard-Typed Unit Registry — Two-Step Base Unit Model (Mandatory)

All biomarker values must be converted using a two-step deterministic process.

**Step 1 — Internal Base Unit Standardisation**

All incoming lab values are converted into a single canonical internal base unit (SI preferred).

Example:

* mg/dL → mmol/L
* g/L → mmol/L
* U/L → U/L (if already canonical)

Layer B performs all mathematical operations exclusively on base units.

**Step 2 — Presentation Conversion**

At the presentation layer only, values may be converted to:

* US customary units
* Metric preference

This prevents:

* Mixed-unit calculations
* Decimal drift
* Ratio distortion

**Mandatory Requirements**

* UnitEnum enforced
* ConversionMatrix versioned
* Conversion logged in snapshot metadata
* Unknown units rejected deterministically

No string-based unit interpretation.

---

## 3.3 Lab Origin Metadata Layer (P0 Safety Infrastructure)

Lab origin detection is now classified as **P0 Safety Infrastructure**.

Each snapshot must include:

```
lab_provider_id
lab_reference_profile_hash
lab_detection_confidence_score
```

If a previous snapshot exists and `lab_provider_id` differs:

Trigger:

```
ContextualVarianceFlag
```

**This flag must appear in InsightGraph.**

This prevents false biological interpretation caused by laboratory methodology variance.

---

## 3.4 Derived Biomarker Registry (Centralised Computation)

All derived biomarkers must be computed centrally.

* All derived ratios (TG/HDL, TC/HDL, LDL/HDL, ApoB/ApoA1, NLR, AST/ALT, etc.)
* Must be computed in a single deterministic pipeline step.
* Insights must not compute ratios locally.
* Ratios must be stored in the AnalysisSnapshot.
* **Lab-supplied ratios are never overwritten; RatioRegistry is a missing-value filler with provenance tagging.**
* **Derived markers are exposed as a first-class `derived_markers` field in the API result (registry_version + derived dict with provenance).**

> **All derived ratio calculations occur after full unit normalisation into internal base SI units.**  
> **RatioRegistry logic must never operate on presentation-layer units.**

Unit normalisation is Layer A responsibility. RatioRegistry is Layer B deterministic computation only.

> **Duplicate ratio calculations in insight modules are prohibited.**

Examples:

* TG/HDL
* TC/HDL
* LDL/HDL
* ApoB/ApoA1
* AST/ALT
* NLR
* Non-HDL
* Urea/Creatinine

Each derived marker must define:

```
id
formula
required_inputs
unit_requirements
calculation_precision
interpretation_bounds (see §6)
```

No insight file may compute ratios locally.

### Canonical Computation Boundary (Non-Negotiable)

Insight modules in **Layer C** are presentation/narrative translators and must not perform deterministic medical computation.

The following are prohibited inside insight modules:

* Computing derived biomarkers or ratios (including ratio-like arithmetic over biomarker values)
* Applying hard-coded normal/ideal/critical thresholds to biomarker-derived values

All computation authority belongs only to:

* **Layer A**: unit canonicalisation / ingestion normalisation
* **Layer B**: deterministic registries and engines

Any Layer C computation breach is an **architectural defect** and must be treated as a blocking governance violation.

### Enforcement Rollout Phases

* **Phase 1 — Detection (Report-Only, Current):** AST enforcement scanner reports deterministic violations without hard-failing CI.
* **Phase 2 — Migration:** Refactor violating insight modules in controlled batches until residual violations are reduced to zero.
* **Phase 3 — Hard Enforcement:** Zero-violation policy; enforcement test hard-fails on any detected violation.

---

# 4. Layer B — Deterministic Intelligence Engine

Layer B transforms canonical markers into systemic insight.

---

## 4.1 Biomarker Scoring Engine

Each biomarker receives:

* Position in lab range
* Status (low/normal/high)
* Normalised score
* Confidence score

Scoring must use:

* position_in_range()
* map_position_to_status()
* calculate_confidence()

All scoring logic must live in one engine.

No duplication across clusters or insights.

---

## 4.2 Health System Clusters — Canonical Clustering Engine Declaration

> **cluster_engine_v2 is the canonical clustering architecture going forward.**  
> **Legacy ClusteringEngine is deprecated and must not be extended.**

If cluster_engine_v2 is not yet production-ready:

> cluster_engine_v2 will replace legacy clustering in Sprint 9 (or designated migration sprint).  
> No new logic may be added to the legacy engine.

> **cluster_engine_v2 accepts canonical biomarker IDs only.**  
> **Alias resolution must be completed prior to clustering.**  
> **Name-based grouping is prohibited.**

Clusters define systemic groupings:

Initial systems:

* Metabolic
* Cardiovascular
* Inflammatory
* Hormonal
* Nutritional
* Kidney
* Liver
* CBC

Each cluster definition must include:

```
cluster_id
canonical_biomarkers
derived_biomarkers
weights
criticality_weights
confidence_penalties
```

Cluster logic must be schema-driven (YAML or registry).

---

## 4.3 Biomarker Criticality Model

Each biomarker must define:

```
cluster_weight
confidence_weight
criticality_level
required_for_cluster (boolean)
```

**Criticality Policy (Sprint 3):** `backend/ssot/criticality.yaml` defines required/important/optional biomarkers per health system. Analysis result meta includes:

* `criticality_version` — policy version
* `system_confidence` — per-system confidence (0–100)
* `overall_confidence` — weighted aggregate
* `missing_markers` — `{system: [biomarker, ...]}`
* `confidence_downgrades` — `[{system, tier, biomarker, penalty, reason}, ...]`

Example:

* Missing ApoB → 40% cardiovascular confidence penalty
* Missing Vitamin D → 5% nutritional penalty

**Missing markers must:**

* Reduce confidence proportionally
* Be explicitly listed in InsightGraph
* Never be silently ignored

Confidence is a deterministic mathematical output.

---

## 4.4 Missing Data Handling

Cluster scoring must:

* Compute score from available markers
* Apply weighted confidence degradation
* Expose missing marker list

System must never silently ignore missing critical markers.

---

## 4.5 Derived Ratio Interpretation (Exception Model) — Demographic Partitioning

Because labs do not supply ranges for ratios:

A Standardised Ratio Registry must define:

```
ratio_id
default_bounds
optional_sex_overrides
optional_age_overrides
literature_reference
```

The RatioRegistry must support optional demographic override fields:

* `overrides_by_sex`
* `overrides_by_age_range`
* `overrides_by_population`

**However:**

* Demographic overrides will **not be activated** in v5.1
* All overrides must be literature-backed
* All overrides must be versioned
* No probabilistic or heuristic population modelling permitted

This preserves architectural extensibility without introducing premature medical risk.

These are the only ranges permitted to be system-standardised.

All others must use lab-provided bounds.

---

## 4.6 InsightGraph Contract (Core Output)

Layer B must produce a structured object. The formal contract is defined in §4.7.

---

## 4.7 The InsightGraph Contract — The System Handshake

The InsightGraph is the **formal interface boundary** between:

* **Layer B** (Deterministic Intelligence Engine)
* **Layer C** (Narrative Translation Engine)

This contract is immutable and versioned.

### The Golden Rule

**The LLM must never receive:**

* Raw biomarker values
* Raw lab reference ranges
* Unit information
* Alias resolution metadata
* Snapshot internals

**The LLM may only receive the structured InsightGraph object.**

### InsightGraph v1 Structure

```
InsightGraph:
  analysis_id
  system_scores
  biomarker_contributions
  derived_ratios
  detected_clusters
  missing_markers
  lab_variance_flags
  temporal_flags (reserved)
  confidence_model
  processing_version
```

### InsightGraph v1 Contract (Deterministic → Narrative Boundary)

Define the JSON schema shape explicitly:

```
InsightGraph_v1 = {
  "insight_graph_version": "1.0.0",
  "analysis_id": str,
  "snapshot_version": str,
  "scoring_engine_version": str,
  "system_scores": {
      "<system_name>": {
          "overall_score": float,
          "confidence": float
      }
  },
  "biomarker_contributions": [
      {
          "biomarker_id": str,
          "impact_percentage": float,
          "direction": "positive" | "negative"
      }
  ],
  "detected_clusters": [
      {
          "cluster_id": str,
          "confidence": float
      }
  ],
  "variance_flags": [
      {
          "type": "lab_origin_change" | "velocity_alert" | "unit_normalisation",
          "severity": "info" | "warning" | "critical"
      }
  ],
  "confidence_score": float
}
```

* The `insight_graph_version` field is mandatory.
* It must be stored inside AnalysisSnapshot.
* Snapshot replay must validate graph version compatibility.
* Any schema evolution requires version increment and migration note.

> **The LLM must never receive raw biomarker values.**  
> **The LLM only receives InsightGraph_v1.**

### Required Properties

* Fully deterministic
* Fully reproducible from snapshot
* Contains no unprocessed data
* Contains no interpretive gaps
* Version stamped

This object is the "ranking algorithm" equivalent of Health IQ AI.

**No narrative logic may bypass this contract.**

Layer C consumes this object only.

---

# 5. Snapshot & Versioning Model

Each AnalysisSnapshot must contain:

```
raw_inputs
canonicalised_markers
derived_markers
reference_ranges
cluster_definitions_version
ratio_registry_version
scoring_engine_version
unit_registry_version
lab_origin_metadata
confidence_metrics
timestamp
```

No insight may be generated without snapshot creation.

---

# 6. Derived Ratio & Cluster Schema (Foundational DNA)

The Derived Biomarker & Cluster Schema is the mathematical DNA of the system.

It must define:

* Ratio definitions
* Cluster definitions
* Evaluation thresholds
* Weighting model
* Confidence degradation rules
* Missing-data penalties

This schema must be:

* Versioned
* Validated
* Test-covered
* Independent from insight narrative files

---

# 7. Temporal Intelligence (Phase 2 Architecture)

Velocity & Trend Engine must be architected but not necessarily implemented in v5.0.

It must support:

* Delta absolute
* Delta percent
* Delta position-in-range
* Stability index
* Acceleration detection

Temporal flags must integrate into InsightGraph.

---

# 8. Performance & Scalability Requirements

* Deterministic scoring must complete in < 1 second
* Snapshot generation must be atomic
* Ratio calculation must be isolated
* Unit conversion must be precompiled and not dynamic
* Cluster evaluation must not scale quadratically

---

# 9. Explicitly Out of Scope for v5.1

* Full correlation network modelling
* Machine learning clustering
* Adaptive scoring based on population datasets
* Real-time wearable ingestion
* Predictive mortality modelling

This prevents scope creep.

v4 codebase files are reference-only and must never be imported into the v5 runtime.

---

# 10. Non-Goals (v5.1)

* LLM performing medical inference
* Free-text risk scoring
* Unbounded fuzzy parsing
* Non-versioned logic
* Static global biomarker ranges (except ratios)

---

# 11. Regulatory Readiness

The architecture must support:

* Deterministic replay
* Version traceability
* Confidence transparency
* Rule explainability
* Audit logging

The system must be capable of CE/FDA alignment without structural redesign.

---

# 12. Success Criteria

Health IQ AI v5.1 is considered architecturally complete when:

* All biomarker logic is centralised
* All derived ratios are registry-driven
* All clusters are schema-driven
* Unit handling is type-safe
* Lab-origin detection exists
* Confidence is mathematically defined
* InsightGraph is immutable and structured
* LLM is fully decoupled from logic
* **InsightGraph is the sole narrative input object**
* **All insights derive exclusively from InsightGraph**
* **No insight file performs independent scoring or ratio calculation**

---

# 13. Strategic Positioning

This architecture positions Health IQ AI as:

* Deterministic
* Transparent
* Extensible
* Longitudinally intelligent
* Clinically defensible
* Platform-ready

Not a report tool.

A biological intelligence system.