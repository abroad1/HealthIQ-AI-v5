# P1-17 — Remaining PSI Blocker Resolution Pack

**Work ID:** P1-17  
**Branch:** `sprint/P1-17-remaining-psi-blocker-resolution`  
**Date:** 2026-06-21  
**Status:** IMPLEMENTATION_COMPLETE  
**Agent:** healthiq-knowledge-bus-medical-intelligence

---

## 1. Start-state candidate list

| Cohort | Count | Source |
|--------|-------|--------|
| Package-identity unresolved (P1-16 carry-forward) | 4 | `P1-16_identity_adjudication_manifest.yaml` |
| Derived-marker / transferrin_saturation (P1-14 carry-forward) | 7 | `P1-14_activation_readiness_cohort_manifest.yaml:211-269` |
| **Total adjudicated** | **11** | |

Medical-review blocked PSI (3 homocysteine + leukocyte cohort) were out of scope per prompt.

---

## 2. Package-identity adjudication results (4 candidates)

All four candidates share the same unresolved KB-S52c vs KB-S58 provenance pattern carried forward from P1-16.

| Staged package ID | Staged PSI `package_id` | Production home | STOP gate | Adjudication |
|-------------------|-------------------------|-----------------|-----------|--------------|
| `pkg_kb52c_rbc_high_erythrocytosis_pattern` | `pkg_kb52c_*` | `pkg_kb58_rbc_high_erythrocytosis_pattern` only | 1 | **BLOCKED_PACKAGE_IDENTITY_UNRESOLVED** |
| `pkg_kb52c_rbc_low_iron_restricted_anemia_pattern` | `pkg_kb52c_*` | `pkg_kb58_rbc_low_iron_restricted_anemia_pattern` only | 1 | **BLOCKED_PACKAGE_IDENTITY_UNRESOLVED** |
| `pkg_kb52c_rdw_cv_high_iron_deficiency_anisocytosis` | `pkg_kb52c_*` | `pkg_kb58_rdw_cv_high_iron_deficiency_anisocytosis` only | 1 | **BLOCKED_PACKAGE_IDENTITY_UNRESOLVED** |
| `pkg_kb52c_rdw_cv_high_mixed_red_cell_population_pattern` | `pkg_kb52c_*` | `pkg_kb58_rdw_cv_high_mixed_red_cell_population_pattern` only | 1 | **BLOCKED_PACKAGE_IDENTITY_UNRESOLVED** |

**Evidence inspected:**

- Staged PSI internal `package_id` is `pkg_kb52c_*` (e.g. `knowledge_bus/generated_pilot/p1_11_batch_b/pkg_kb52c_rbc_high_erythrocytosis_pattern/promoted_signal_intelligence.yaml:3`).
- Matching `pkg_kb58_*` production packages exist but contain no PSI (e.g. `knowledge_bus/packages/pkg_kb58_rbc_high_erythrocytosis_pattern/package_manifest.yaml:1`).
- No `pkg_kb52c_rbc_*` or `pkg_kb52c_rdw_cv_*` production packages exist (`Glob` returns empty).
- Cross-ID placement was rejected in P1-15 (GPT Option B).
- No deterministic identity-normalisation tooling exists (P1-16 sprint report §2).

**Resolution path:** Governed re-staging under `pkg_kb58_*` identity or explicit architectural approval to create `pkg_kb52c_*` production packages — not cross-ID opt-in.

---

## 3. Derived-marker adjudication results (7 candidates)

| Candidate | Derived dependency | SSOT status | Validator status | Host package | Compound blockers | Adjudication |
|-----------|-------------------|-------------|------------------|--------------|-------------------|--------------|
| `pkg_kb52c_ferritin_high_inflammatory_hyperferritinemia` | `transferrin_saturation` | Canonical (`biomarkers.yaml:1865`) | Hardcoded derived (`validate_staged_psi_activation_readiness.py:32`) | Missing | — | **BLOCKED_REQUIRES_CORE_BACKEND_AGENT** |
| `pkg_kb52c_ferritin_high_iron_overload_context` | `transferrin_saturation` | Canonical | Hardcoded derived | Missing | — | **BLOCKED_REQUIRES_CORE_BACKEND_AGENT** |
| `pkg_kb61_transferrin_high_iron_deficiency_transport_upregulation` | `transferrin_saturation` | Canonical | Hardcoded derived | Exists, no PSI | — | **BLOCKED_REQUIRES_CORE_BACKEND_AGENT** |
| `pkg_kb52c_iron_high_hepatocellular_or_hemolytic_release` | `transferrin_saturation` | Canonical | Hardcoded derived | Missing | Medical review + frame authority | **BLOCKED_REQUIRES_CORE_BACKEND_AGENT** |
| `pkg_kb52c_iron_high_iron_overload_context` | `transferrin_saturation` | Canonical | Hardcoded derived | Missing | Medical review + frame authority | **BLOCKED_REQUIRES_CORE_BACKEND_AGENT** |
| `pkg_kb52c_iron_low_absolute_iron_deficiency` | `transferrin_saturation` | Canonical | Hardcoded derived | Missing | Medical review + frame authority | **BLOCKED_REQUIRES_CORE_BACKEND_AGENT** |
| `pkg_kb52c_iron_low_functional_iron_restriction_inflammation` | `transferrin_saturation` | Canonical | Hardcoded derived | Missing | Medical review + frame authority | **BLOCKED_REQUIRES_CORE_BACKEND_AGENT** |

**Key finding:** The blocker is not SSOT absence. `transferrin_saturation` is a canonical top-level SSOT key. The activation-readiness validator hardcodes it in `DERIVED_MARKER_IDS` and flags all seven PSI regardless of SSOT presence. Removing or replacing that policy requires editing `backend/scripts/validate_staged_psi_activation_readiness.py` — outside Medical Intelligence agent boundary (STOP gate 2).

---

## 4. Candidates opted in

**None.** All 11 candidates hit STOP gates 1 or 2. No production PSI artefacts were created or modified.

---

## 5. Candidates blocked

| Adjudication class | Count |
|--------------------|-------|
| `BLOCKED_PACKAGE_IDENTITY_UNRESOLVED` | 4 |
| `BLOCKED_REQUIRES_CORE_BACKEND_AGENT` | 7 |

Full per-candidate records: `P1-17_blocker_resolution_manifest.yaml`.

---

## 6. Core backend handoff

Seven derived-marker candidates require core backend ownership. Handoff manifest: `P1-17_core_backend_handoff_manifest.yaml`.

Primary handoff action: adjudicate `DERIVED_MARKER_IDS` policy for `transferrin_saturation` given SSOT canonical presence at `biomarkers.yaml:1865`.

Package-identity candidates require a separate source-research / package-provenance sprint — not classified as core-backend handoff in this sprint.

---

## 7. Validation commands and results

No new PSI opt-ins — per-candidate PSI and package validation not applicable.

Full estate activation-readiness rerun (mandatory Phase 5):

```powershell
python backend/scripts/validate_staged_psi_activation_readiness.py
```

**Result:** exit 0 — no regression from P1-16 baseline.

Expected counts unchanged:

- `psi_files_found`: 41
- `production_opt_ins_found`: 42
- `activation_ready_count`: 4
- `blocked_count`: 37

---

## 8. Scope confirmations

| Check | Status |
|-------|--------|
| No `backend/ssot/` edits | Confirmed |
| No `backend/core/` edits | Confirmed |
| No `backend/scripts/` edits | Confirmed |
| No `backend/tests/` edits | Confirmed |
| No `frontend/` edits | Confirmed |
| No DTO / scoring / Gemini / parser / runtime loader edits | Confirmed |
| No staged `generated_pilot/` edits | Confirmed |
| No medical-review blocked PSI promoted | Confirmed |
| No cross-ID PSI placement | Confirmed |
| No runtime / user-facing activation | Confirmed |
| No medical meaning altered | Confirmed (no PSI content changed) |

---

## 9. Recommended next outcome-based package

**P1-DERIVED-METRIC-TRANSFERRIN-SAT-1** (core-engine agent)

Resolve `DERIVED_MARKER_IDS` policy for SSOT-canonical `transferrin_saturation` in `validate_staged_psi_activation_readiness.py`. After validator policy is resolved:

1. Opt-in `pkg_kb61_transferrin_high_iron_deficiency_transport_upregulation` PSI (ID-matched host package already exists).
2. Create production host packages for ferritin-high patterns.
3. Defer iron Batch C PSI until medical-review blockers cleared.

**Parallel track:** Package provenance sprint for 4 KB-S52c vs KB-S58 CBC candidates (re-staging or governed production package creation).

---

## Artefacts produced

| File | Purpose |
|------|---------|
| `P1-17_blocker_resolution_manifest.yaml` | Full 11-candidate adjudication ledger |
| `P1-17_core_backend_handoff_manifest.yaml` | Core-engine handoff for 7 derived-marker candidates |
| `P1-17_remaining_psi_blocker_resolution.md` | This sprint report |
| `BUILD_DELIVERABLE_REGISTER.md` | Updated P1-17 entry |
