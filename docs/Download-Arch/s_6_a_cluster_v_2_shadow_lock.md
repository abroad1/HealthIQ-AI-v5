---
work_id: "S6A-CLUSTER-V2-SHADOW-LOCK"
branch: "feature/sprint6a-cluster-v2-shadow-lock"
risk_level: "HIGH"
execution_model: "TWO_PHASE_START_FINISH"
---

# Sprint 6A — Cluster Engine v2 Shadow Determinism Lock

## Classification

Control-plane + analytical determinism enforcement.
No schema refactor permitted.
No migration permitted.

---

# Objective

Lock deterministic parity between:

- Legacy `ClusteringEngine` (runtime)
- `cluster_engine_v2` (shadow execution)

This sprint does **not** modify cluster logic.
This sprint enforces determinism and parity only.

---

# Scope (Allowed)

1. Implement shadow execution pathway:
   - Execute legacy clustering engine
   - Execute cluster_engine_v2

2. Produce structured outputs for both engines

3. Compare deterministically:
   - Cluster IDs
   - Cluster scores
   - Confidence values
   - Cluster ordering

4. Enforce:
   - Sorted JSON keys
   - Stable cluster ordering
   - No duplicate cluster IDs
   - No missing cluster keys

5. Add deterministic double-run validation:
   - Same input executed twice
   - Byte-identical JSON output required

6. Wire shadow parity enforcement into:
   `backend/scripts/golden_gate_local.py`

Gate must fail on any mismatch.

---

# Explicitly Out of Scope

The following are strictly prohibited:

- No cluster schema modifications
- No renaming of systems
- No refactor of scoring engine
- No changes to cluster definitions
- No changes to ssot files
- No migration to cluster_engine_v2 as runtime engine
- No logic changes in legacy engine
- No performance optimisation work
- No InsightGraph changes

If any of the above are required → STOP and FAIL.

---

# STOP Conditions (Hard Fail)

Kernel must treat as FAILED if any of the following occur:

- Any file under `backend/ssot/` modified
- Any cluster definition logic modified
- Any scoring logic modified
- Any renaming of cluster/system identifiers
- Any mutation of gate evidence
- Any non-deterministic ordering detected
- Any use of randomness
- Any UUID generation
- Any timestamp injection into cluster comparison
- Any bypass of golden gate

---

# Determinism Requirements

All cluster comparison JSON must:

- Use sorted keys
- Use stable indentation
- Use ISO UTC only where required
- Contain no volatile fields
- Be byte-identical across double-run execution

---

# Gate Requirements

Golden gate must:

1. Execute shadow parity comparison
2. Fail if mismatch detected
3. Fail if duplicate cluster IDs
4. Fail if cluster order unstable
5. Fail if output differs across two consecutive executions

Gate must not mutate evidence.

---

# Completion Criteria

Kernel `finish` may mark COMPLETE only if:

- Gate exit_code == 0
- Evidence.overall.status == PASS
- Shadow comparison PASS
- Determinism double-run PASS
- work_id matches

Otherwise status = FAILED.

---

# Deliverables

- Shadow comparison implementation
- Golden gate integration
- Determinism double-run validation
- Tests covering parity enforcement

No additional feature work permitted.

---

# Architectural Rationale

Before cluster schema refactor (Sprint 6B) or migration (Sprint 9),
cluster determinism must be frozen.

This sprint establishes invariant behaviour.

Refactor without invariants is prohibited.

---

# Post-Sprint Condition

Upon COMPLETE:

Cluster behaviour is frozen under deterministic parity.

Only then may schema refactor begin.

---

Version: v1.2 compliant
Status: READY_FOR_HARDENING

