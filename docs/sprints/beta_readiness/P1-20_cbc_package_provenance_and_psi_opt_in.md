# P1-20 — CBC Package Provenance Resolution and PSI Opt-In

**Work ID:** P1-20  
**Branch:** `sprint/P1-20-cbc-package-provenance-and-psi-opt-in`  
**Date:** 2026-06-22  
**Status:** IMPLEMENTATION_COMPLETE  
**pipeline_advisory_trigger:** Stage 0 pipeline advisory post P1-19 audit close  
**pipeline_advisory_reason:** Sprint 3 CBC package provenance — resolve KB-S52c vs KB-S58 identity for cf_003–cf_006 with bundled opt-in

---

## 1. Start state

Post P1-19: 4 CBC candidates blocked `BLOCKED_PACKAGE_IDENTITY_UNRESOLVED`; production opt-ins **43**; activation-ready **6**.

## 2. Canonical candidate set

Four candidates from `P1-19_pass3_carry_forward.yaml` cf_003–cf_006. Stage 0 advisory fifth candidate recorded as duplication only — not implemented.

## 3. Provenance proof results

All four passed Phase 2 gate:

- Staged compile manifest `source_path` = `cbc_hematology_pass_3.json`
- Production manifest `source_document` = same path
- No prior `promoted_signal_intelligence` on any `pkg_kb58_*` host
- No medical-review or frame-authority blockers

## 4. Re-homing and opt-ins completed

| Staged `pkg_kb52c_*` | Production `pkg_kb58_*` | SHA256 verified |
|----------------------|-------------------------|-----------------|
| `rbc_high_erythrocytosis_pattern` | `pkg_kb58_rbc_high_erythrocytosis_pattern` | match |
| `rbc_low_iron_restricted_anemia_pattern` | `pkg_kb58_rbc_low_iron_restricted_anemia_pattern` | match |
| `rdw_cv_high_iron_deficiency_anisocytosis` | `pkg_kb58_rdw_cv_high_iron_deficiency_anisocytosis` | match |
| `rdw_cv_high_mixed_red_cell_population_pattern` | `pkg_kb58_rdw_cv_high_mixed_red_cell_population_pattern` | match |

Byte-copy only — staged PSI internal `package_id` remains `pkg_kb52c_*` (unchanged). Production manifests updated only to add `promoted_signal_intelligence: promoted_signal_intelligence.yaml`.

## 5. Validation results

```text
validate_promoted_signal_intelligence.py — 4/4 PASS
validate_knowledge_package.py — 4/4 PASS (ready_for_implementation: True)
validate_staged_psi_activation_readiness.py — exit 0
  production_opt_ins_found: 47 (+4)
  activation_ready_count: 6 (unchanged — expected)
  blocked_count: 35
```

**Expected staged-validator behaviour:** The four re-homed candidates continue to show `production_manifest_opt_in: false` under their `pkg_kb52c_*` staged directory names. Production opt-in is registered under `pkg_kb58_*`. Validator matches by staged directory name (`validate_staged_psi_activation_readiness.py:196`), not production host. This is expected — not a failure.

## 6. Carry-forwards

No remaining CBC package-provenance carry-forwards from this sprint.

## 7. Scope confirmations

No generated-pilot edits, no signal_library/research_brief changes, no backend/frontend/validator/test edits.

## 8. Recommended next sprint

**P1-FERRITIN-HIGH-AUTHORITY-RECONCILIATION-1** — resolve `signal_ferritin_high` duplicate authority (P1-19 carry-forward cf_001–cf_002).
