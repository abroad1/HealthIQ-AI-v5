# ARCH-CONV — Day-One Layer Completion Assessment

**Work ID:** `ARCH-CONV-RESIDUAL-AUDIT-1`  
**Date (UTC):** 2026-07-27  
**Statuses used:** `COMPLETE` · `SUBSTANTIALLY COMPLETE` · `PARTIAL` · `LEGACY-DOMINANT` · `UNKNOWN`  
**Rule:** No unsupported percentage-complete estimates.  
**Runtime change:** NONE  

---

## Layer A — Ingestion and canonical facts

**Status:** `SUBSTANTIALLY COMPLETE`

### What is in place

- Canonical biomarker normalisation and unit registry on analysis start.
- Explicit waist cm/inches integrity (CORRECT-1 closure stabilisation).
- Quarantine of unmapped biomarkers; derived ratio computation.
- Questionnaire/context assembly before signal evaluation (ARCH-COMPLETION-1).

### Missing / residual

| Gap | Active legacy dependency | Consequence | Bounded remediation |
|---|---|---|---|
| Historic bare-waist analyses | L-11 compatibility debt | Some historic results incorrect or dropped | Result-versioning + regenerate/remap package |
| Marker display-name polish (FE) | Retail label maps | Trust/UX, not Layer A facts | Separate polish (non-architecture critical) |

---

## Layer B — Medical reasoning and output authority

**Status:** `PARTIAL` (pilot `SUBSTANTIALLY COMPLETE`; estate `LEGACY-DOMINANT` for WHY)

### What is in place

- Activation-key identity on registry and launch-path PKG1 surfaces.
- Provenance/reachability honesty for launch-critical kb47 INCLUDE/EXCLUDE.
- Compiled WHY authority for 9 frames; rejected frame structurally inactive.
- MCV co-service policy; collision model for configured axes.
- Compiled Wave 1 Health Systems Card evidence.
- Clinician/narrative/IDL compilers producing structured DTOs.
- CORRECT-1 Layer B enforcement of primary driver projection.

### Missing / residual

| Gap | Active legacy dependency | Consequence | Bounded remediation |
|---|---|---|---|
| Estate WHY still legacy for 36 targets (verified exact count; frame count per target unresolved until Phase 1 identity closure) | L-01 | Day-One WHY incomplete | Wave-based compiled WHY completion |
| Elevation-context dual | L-02 / DUAL-01 | Competing hcy explanations | Migrate or bound elevation-context |
| Fallback WHY placeholder | L-04 | Soft fail-open | Policy: fail-closed or governed insufficient-evidence |
| Layer C feature thresholds in Python | L-07 | Hidden medical policy | Compile/govern feature policy |
| Family-level phenotype/interaction grain | L-06 | Frame collapse at those surfaces | Explicit aggregation policy or key migration |
| PSI unwired | Dormant dual | Not a current emit defect; reactivation risk | Keep STOP-gated |

---

## Layer C — Presentation / translation

**Status:** `SUBSTANTIALLY COMPLETE` (for audited boundary inventory)

### What is in place

- CORRECT-1 closed 12/12 Layer C `BOUNDARY_LEAK` inventory rows.
- FE consumes `primary_driver_v1`; dial/confidence/order governed by backend.
- Deleted FE-authored clinical recommendation / causal-ish relevance modules.
- Governed static copy modules for educational chrome.

### Missing / residual

| Gap | Active legacy dependency | Consequence | Bounded remediation |
|---|---|---|---|
| Residual humanization / fallback sentences | Display helpers | Low-grade invention risk if fields missing | Extend boundary tests; fail-safe copy only |
| Retail polish carry-forwards | Label normalisation etc. | UX trust | Non-blocking polish track |

---

## Knowledge Bus — Canonical research → compiled runtime artefacts

**Status:** `PARTIAL`

### What is in place

- Investigation specs + Pass 3 lineage recoverable for material cohorts.
- Package manifests, compile manifests, authority registers.
- Pilot compiled WHY artefacts + Wave 1 compiled cards.
- Governance validators / architecture gates.

### Missing / residual

| Gap | Active legacy dependency | Consequence | Bounded remediation |
|---|---|---|---|
| Most WHY content not compiled | Legacy YAML L-01 | Bus incomplete for Day-One WHY | Cohort compile waves |
| Stale estate index vs PKG3 | Inventory drift | Misleading ops view | Refresh index inside next compile package |
| Generated-pilot / candidate prose non-runtime | Candidate YAML | Safe if kept non-runtime | Continue authority blockers |
| Non-Pass-3 / deferred package dispositions | Multiple CF items | Provenance debt | Existing KB disposition track (not v6-forcing alone) |

---

## Automation / governance — Deterministic promotion and validation

**Status:** `SUBSTANTIALLY COMPLETE` for architecture gates; `PARTIAL` for estate promotion automation

### What is in place

- Architecture validation umbrella gate (identity, provenance, compiled WHY, Layer B integrity, etc.).
- CORRECT-1 gate + PKG1–3 gates.
- Day-one guardrails validator / sentinel pack.
- Promotion safety / frame-index validators.

### Missing / residual

| Gap | Active legacy dependency | Consequence | Bounded remediation |
|---|---|---|---|
| Estate-wide compile pipeline still partly manual | CF-KBUTIL1-001 class debt | Slow/error-prone expansion | Absorb into WHY completion waves |
| Medical-review throughput for remaining frames | Process, not code | Bounds programme speed | Wave sizing + Gate 2.5-style STOP gates |

---

## Replay / provenance — Reproducibility and lineage

**Status:** `PARTIAL`

### What is in place

- Replay manifest emission; regenerate route re-runs orchestrator.
- Result versioning metadata on GET assembly.
- Persisted client result shape for retrieval.
- Provenance elements on report authority model (partial).

### Missing / residual

| Gap | Active legacy dependency | Consequence | Bounded remediation |
|---|---|---|---|
| Historic waist impact | L-11 | Historic fidelity gaps | Stale/regenerate policy package |
| Output-authority provenance key debt | L-12 (`…::inv_homocysteine_high`) | Misleading lineage identity | Fix emitter/tests |
| Result-versioning after medical-authority changes | Policy incomplete | Users may see stale medical meaning without forced regen | Advance LAUNCH-CORE-3 policy |
| Full DB lineage table | CF-MEDREV2-002 | Long-term auditability | Later hardening (non-blocking for architecture GO if versioning advanced) |

---

## Cross-layer verdict

| Layer | Status |
|---|---|
| Layer A | SUBSTANTIALLY COMPLETE |
| Layer B | PARTIAL (estate WHY LEGACY-DOMINANT) |
| Layer C | SUBSTANTIALLY COMPLETE |
| Knowledge Bus | PARTIAL |
| Automation/governance | SUBSTANTIALLY COMPLETE (gates) / PARTIAL (estate compile automation) |
| Replay/provenance | PARTIAL |

**Estate-wide Day-One architecture is not COMPLETE.**  
**The migrated cohort demonstrates the target model is achievable without a platform rewrite.**
