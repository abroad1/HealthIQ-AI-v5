# P1-21 — Ferritin-High Signal Authority Reconciliation and PSI Promotion

**Work ID:** P1-21  
**Branch:** `sprint/P1-21-ferritin-high-authority-reconciliation`  
**Date:** 2026-06-22  
**Status:** IMPLEMENTATION_COMPLETE  
**pipeline_advisory_trigger:** Stage 0 pipeline advisory post P1-19 — ferritin-high authority collision  
**pipeline_advisory_reason:** Option A selected — retire pkg_s24 active authority; promote Pass 3 ferritin-high PSI to modern pkg_kb52c hosts

---

## 1. Start state

P1-19 blocked 2 ferritin-high candidates (`BLOCKED_DUPLICATE_AUTHORITY_RISK`) due to `signal_ferritin_high` collision with `pkg_s24_ferritin_high_overload`. Production opt-ins **47**.

## 2. Authority decision

`ADR-FERRITIN-HIGH-SIGNAL-AUTHORITY-RECONCILIATION-1` — Option A: in-place deprecation of pkg_s24; two modern `pkg_kb52c_*` production packages; retain `signal_ferritin_high`; no new signal IDs; no runtime changes.

## 3. Legacy retirement

`pkg_s24_ferritin_high_overload` — manifest-level `deprecated: true` with `deprecated_by` pointing to new packages. Directory and `signal_library.yaml` unchanged (non-regression test compatibility).

## 4. Production packages created

| Package | Signal ID | PSI source |
|---------|-----------|------------|
| `pkg_kb52c_ferritin_high_inflammatory_hyperferritinemia` | `signal_ferritin_high` | Byte-copy staged pilot |
| `pkg_kb52c_ferritin_high_iron_overload_context` | `signal_ferritin_high` | Byte-copy staged pilot |

## 5. Validation

```text
validate_promoted_signal_intelligence.py — 2/2 PASS
validate_knowledge_package.py — 2/2 PASS (ready_for_implementation: True)
pkg_s24 post-deprecation package validation — PASS
validate_staged_psi_activation_readiness.py — exit 0
  production_opt_ins_found: 49 (+2)
test_signal_authority_collision_enforcement.py — 13 passed
```

## 6. Carry-forwards

None from P1-21 ferritin-high scope.

## 7. Scope confirmations

No generated-pilot edits, no ferritin-low changes, no backend/runtime/validator/test edits (except none required).

## 8. Recommended next sprint

Iron Batch C medical-review clearance or bio-oxygen subsystem signal enrichment per P1-18 carry-forward.
