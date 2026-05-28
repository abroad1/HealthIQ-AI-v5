# ADR-RT-002 — Signal Spec Identity and Registry Policy

| Field | Value |
|-------|-------|
| **Status** | ACCEPTED |
| **Date** | 2026-05-28 |
| **Work package** | ARCH-RT-0 |
| **Decisive** | Yes — one-frame vs multi-frame resolved below |

## Context

Repo evidence (ARCH-RT-0):

- **45** duplicate `signal_id` families across **96** package rows.  
- Pass 3 intentionally emits **multiple medical frames per biomarker direction** (e.g. **4** packages for `signal_alt_high`).  
- Current `SignalRegistry` keeps **one** definition via lexicographic path overwrite — **discarding medically distinct frames**.  
- Transition Plan v3 and ARCH-R1 require preserving Pass 3 frame fidelity for launch-grade differential intelligence.

## Decision 1 — Frame policy (mandatory)

### **MULTI_FRAME_PER_DIRECTION**

HealthIQ **will** support multiple governed activation frames per biomarker direction at runtime.

**ONE_FRAME_PER_DIRECTION is rejected** as the target policy. It may describe today's accidental overwrite behaviour but is **not** acceptable for day-one architecture.

**Rationale:**

1. **67** `pkg_kb52c_*` packages encode Pass 3 multi-frame hypotheses.  
2. ALT collision proves **intentional** frame split with shared `signal_id`.  
3. Collapsing frames via lexicographic overwrite loses clinical content without audit trail.  
4. Transition Plan v3 §5 explicitly recommends multi-frame for medical fidelity.

## Decision 2 — Registry keying

| Element | Policy |
|---------|--------|
| Primary registry key | **`activation_key`** (required) |
| Format | `signal_id::spec_id` where `spec_id` is the investigation-spec frame identifier |
| Fallback during migration | `package_id` may be recorded as provenance but **must not** be the long-term key |
| `signal_id` alone | **Insufficient** for registry storage when multi-frame is active |

`spec_id` is sourced from investigation spec v3 (`spec_id` field in batch JSON / `inv_*.yaml`).

## Decision 3 — Is `activation_key` required?

**YES.** Required on:

- Compiled `signal_library` entries (or sidecar index)  
- `SignalResult` at runtime  
- Compile manifest rows  

## Decision 4 — `signal_id + spec_id` sufficiency

**YES**, when `spec_id` is unique per frame within the estate. Collision detection becomes **duplicate `activation_key`** (hard error at compile time), not duplicate `signal_id`.

## Decision 5 — SignalResult provenance requirements

`SignalResult` (and downstream DTO copies) **must** carry:

| Field | Required |
|-------|----------|
| `signal_id` | Yes |
| `spec_id` | Yes |
| `activation_key` | Yes (`signal_id::spec_id`) |
| `package_id` | Yes (compile provenance) |
| `source_document` / `source_spec_hash` | Yes (manifest or compile manifest) |
| `frame_label` / `direction` | Recommended (presentation) |

Implementation owner: **ARCH-RT-2** (identity runtime pilot).

## Decision 6 — Interaction map / phenotype map / root-cause registry

| Asset | Policy |
|-------|--------|
| **Interaction map** | Keys **elevated to `activation_key`** where a frame-specific interaction exists; family-level keys retained only for true family-wide rules |
| **Phenotype map** | Same as interaction map |
| **Root-cause registry** | Register **`activation_key`**, not `signal_id` alone; multiple frames may share one hypothesis YAML with distinct activation contexts |

## Decision 7 — Sprint 3 (ARCH-RT-2) implications

ARCH-RT-2 must:

1. Replace `SignalRegistry` dict keyed by `signal_id` with **`activation_key`**.  
2. Emit **multiple** `SignalResult` rows per direction when frames fire.  
3. Fail compile on duplicate `activation_key`.  
4. Provide parity harness comparing legacy overwrite vs multi-frame for ALT + homocysteine pilots.

## Consequences

- Silent lexicographic overwrite **must be removed** before estate regeneration.  
- Presentation layer must handle **multiple active frames** safely (IDL gates).  
- Larger behavioural change than one-frame; accepted for clinical correctness.

## Rejected alternatives

| Alternative | Reason rejected |
|-------------|-----------------|
| ONE_FRAME_PER_DIRECTION | Destroys Pass 3 frame inventory; already fails on ALT |
| `signal_id` only + governed arbitration | Arbitration undocumented; still loses simultaneous frames |
| `package_id` as primary key | Not stable across regeneration; not spec-identity |

## Evidence

- `docs/architecture/signal_id_collision_inventory.md`  
- `backend/core/analytics/signal_evaluator.py` (current overwrite policy)  
- `docs/planning-papers/HealthIQ_As-Is_to_Day-One_Architecture_Transition_Plan_v3.md` §5
