# ARCH-CONV — Dual Authority Findings

**Work ID:** `ARCH-CONV-RESIDUAL-AUDIT-1`  
**Date (UTC):** 2026-07-27  
**Rule:** Unresolved dual authority is a material architectural defect.  
**Runtime change:** NONE  

---

## 1. Dual-authority detection method

Overlaps were accepted only where **two systems can answer the same medical question** for the same (or overlapping) signal/frame on a live path.

Evidence types used:

- static call-chain analysis (`compile_root_cause_v1`, IDL, cards, FE)
- authority register + WHY resolver behaviour
- CORRECT-1 exclusivity gates for the pilot cohort
- loader/registry inspection

---

## 2. Findings table

### DUAL-01 — Compiled hcy frames vs elevation-context legacy WHY

| Field | Assessment |
|---|---|
| Overlap | Compiled `signal_homocysteine_high::*` WHY **and** legacy `signal_homocysteine_elevation_context` WHY from shared `hcy_hypotheses_v1.yaml` |
| Which wins? | Both can emit on the same analysis when both signals fire — **not mutually exclusive** |
| Where enforced? | No cross-signal exclusivity gate today; only per-activation_key selection inside each signal |
| Fail mode | Fail-open coexistence |
| Order sensitivity | Ranking/intervention citation order can change which explanation dominates UX |
| Tests prove exclusivity? | **No** estate exclusivity test for this pair |
| Config reactivation risk | N/A — already live |
| Defect class | **Material unresolved dual authority** |

### DUAL-02 — Pilot compiled WHY vs residual legacy YAML registration

| Field | Assessment |
|---|---|
| Overlap | Same activation_keys have compiled artefacts and still-registered legacy loaders |
| Which wins? | Compiled for `COMPILED_ACTIVE`; legacy skipped |
| Where enforced? | `why_authority_v1.resolve_frame_why_authority` + compiler branch |
| Fail mode | Fail-closed for unknown pilot keys / REJECTED |
| Order sensitivity | No (mode selected before load) |
| Tests prove exclusivity? | **Yes** for pilot (`validate_compiled_why_authority_gate.py`, PKG3/CORRECT-1 tests) |
| Config reactivation risk | Low unless register state changed |
| Defect class | **Controlled compatibility dual registration** — not an active emit dual |

### DUAL-03 — MCV morphology vs specific-frame causal WHY

| Field | Assessment |
|---|---|
| Overlap | Three MCV frames can fire; causal WHY could compete |
| Which wins? | Co-service policy: anchor `morphology_context`; specifics causal only behind evidence gates |
| Where enforced? | `frame_co_service_v1` + `root_cause_compiler_v1` |
| Fail mode | Fail-closed suppression of unauthorised causal siblings |
| Order sensitivity | Policy-driven, not load-order |
| Tests prove exclusivity? | **Yes** (CORRECT-1 gate + MCV inventory coexistence test) |
| Config reactivation risk | Policy YAML change could reintroduce dual causal emit |
| Defect class | **Resolved dual** (governed) for WHY; signal inventory coexistence intentional |

### DUAL-04 — Rejected metabolic frame vs compiled/specific hcy frames

| Field | Assessment |
|---|---|
| Overlap | Historical catch-all vs specific frames |
| Which wins? | Rejected frame does not fire / rank / intervene / WHY |
| Where enforced? | Authority register + `frame_runtime_authority_v1` at load/evaluate/graph |
| Fail mode | Fail-closed |
| Tests prove exclusivity? | **Yes** (CORRECT-1) |
| Config reactivation risk | Would require register + code policy change |
| Defect class | **Resolved** for runtime |

### DUAL-05 — IDL / compiled WHY summaries / `_why_template`

| Field | Assessment |
|---|---|
| Overlap | Multiple “why it matters” / pattern explanation producers |
| Which wins? | Surface-dependent (IDL for retail patterns; root_cause for causal WHY; template for generic clinician fill) |
| Where enforced? | No single selector across all three |
| Fail mode | Soft coexistence |
| Tests prove exclusivity? | **No** unified exclusivity |
| Defect class | **Material layered presentation dual** (lower than causal dual, still architectural debt) |

### DUAL-06 — PSI vs signal_library vs compiled cards

| Field | Assessment |
|---|---|
| Overlap | Conceptual duplicate intelligence depth |
| Which wins? | signal_library + compiled cards; PSI unwired |
| Where enforced? | ARCH-RT-5E non-wiring + import guards |
| Fail mode | Fail-closed (not called) |
| Config reactivation risk | **Yes** if future wiring bypasses Day-One compile path |
| Defect class | **Dormant dual** — treat reactivation as STOP-gated |

### DUAL-07 — New activation-key registry vs residual family `signal_id` maps

| Field | Assessment |
|---|---|
| Overlap | Frame identity vs family aggregation |
| Which wins? | Frame identity for signal rows/WHY pilot; family grain for phenotype/interaction joins |
| Where enforced? | Mixed — PKG1 improved auditability; family joins remain |
| Fail mode | Intentional aggregation vs silent collapse must be distinguished |
| Tests prove exclusivity? | Partial (launch-path identity gate) |
| Defect class | **Partial / conditional** — material if treated as silent collapse; acceptable if explicit family policy |

### DUAL-08 — Governed narrative DTO vs frontend copy

| Field | Assessment |
|---|---|
| Overlap | Educational/product copy around medical tokens |
| Which wins? | Backend DTOs for medical claims; FE static copy for chrome |
| Where enforced? | CORRECT-1 Layer C boundary closure + FE tests |
| Fail mode | Fail-safe omission preferred over invention |
| Tests prove exclusivity? | **Yes** for audited BOUNDARY_LEAK inventory |
| Defect class | **Resolved for audited leaks**; watch for new FE medical invention |

---

## 3. Material unresolved duals (must drive completion programme)

1. **DUAL-01** — homocysteine elevation-context legacy WHY beside compiled hcy frames.  
2. **DUAL-05** — layered why-it-matters producers without a single authority selector.  
3. **DUAL-07** — residual family-level aggregation wherever still silent rather than explicit.

Controlled or dormant duals (DUAL-02/03/04/06/08) are **not** kill-criteria triggers by themselves, but DUAL-06 reactivation must remain STOP-gated.

---

## 4. Pilot exclusivity proof (positive control)

For the reviewed 5/10 cohort after CORRECT-1:

- compiled vs legacy emit exclusivity holds for `COMPILED_ACTIVE` keys;
- REJECTED metabolic frame is runtime-inert;
- MCV causal co-service is governed.

This proves the **target exclusivity model**, not estate-wide absence of duals.
