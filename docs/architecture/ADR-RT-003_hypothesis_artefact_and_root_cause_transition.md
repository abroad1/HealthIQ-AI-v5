# ADR-RT-003 — Hypothesis Artefact and Root Cause Transition

| Field | Value |
|-------|-------|
| **Status** | ACCEPTED |
| **Date** | 2026-05-28 |
| **Work package** | ARCH-RT-0 |

## Context

- **40** hand-maintained hypothesis YAML files in `knowledge_bus/root_cause/hypotheses/`.  
- **41** manual tuples in `root_cause_registry_v1.py`.  
- Pass 3 investigation specs contain **hypothesis blocks** not compiled to YAML today.  
- ADR-008 defines PSI as **signal-layer only** (no hypotheses in PSI).

## Decision 1 — ADR-008

**ADR-008 is ACCEPTED** (`architecture/ADR-008-promoted-signal-intelligence-contract-v1.md`).

PSI remains **signal-layer intelligence only**. Hypotheses and narrative WHY content **must not** be added to PSI to bypass compile work.

## Decision 2 — PSI scope

PSI is **optional signal-semantics compile output**, not the hypothesis authority. Runtime may remain activation-only (`signal_library`) until PSI wiring is explicitly scheduled.

## Decision 3 — Hypothesis artefact boundary

| Layer | Authority |
|-------|-----------|
| Research | `investigation_spec.hypotheses` (and related blocks) |
| Compiled runtime | **New `compiled_hypothesis` artefact** (name TBD in ARCH-RT-1 schema) |
| Compatibility view | **Root-cause-compatible YAML or loader adapter** emitted from compile |

**Boundary rule:** Investigation-spec hypotheses **never** load directly at runtime.

## Decision 4 — Investigation spec vs root-cause YAML

| Phase | Policy |
|-------|--------|
| Now | Existing YAML + manual registry remain **runtime authority** |
| ARCH-RT-1 | Define hypothesis compile schema + provenance |
| ARCH-RT-3+ | Compile from spec; YAML becomes **generated** or read-only mirror |
| End state | Single compile path; hand-editing YAML **deprecated** |

## Decision 5 — Consumption model

The runtime **root_cause_compiler** will consume a **compiled hypothesis artefact** (or loader that presents root-cause-compatible structures).

**Direct consumption** of raw investigation spec: **prohibited**.

**Emit root-cause-compatible view:** **YES** — compiler may emit YAML or in-memory structures equivalent to today's loader output for parity testing.

## Decision 6 — root_cause_registry transition

| Stage | Mechanism |
|-------|-----------|
| **Sprint ARCH-RT-1** | Add provenance columns to registry tuples; no behaviour change |
| **Sprint ARCH-RT-2** | Key registry by `activation_key` (per ADR-RT-002) |
| **Sprint ARCH-RT-3** | **Manifest-backed registry** pointing to compiled hypothesis assets |
| **End state** | **Generated registry** from estate compile manifest index |

**Rejected for day-one:** Immediate deletion of manual YAML or registry.

## Consequences

- Hypothesis schema work proceeds **after** ADR-RT-001/002 alignment (per transition plan v3).  
- Homocysteine dual registry rows remain until `activation_key` migration maps both frames explicitly.  
- Package regeneration must include **hypothesis compile** as separate stage from activation compile.

## References

- `docs/architecture/root_cause_registry_inventory.md`  
- `docs/architecture/psi_coverage_and_manifest_opt_in_report.md`  
- `docs/planning-papers/HealthIQ_As-Is_to_Day-One_Architecture_Transition_Plan_v3.md`
