# P1-16 — PSI Identity & Blocker Remediation Pack

**Work ID:** P1-16  
**Branch:** `sprint/P1-16-psi-identity-blocker-remediation`  
**Date:** 2026-06-21  
**Status:** IMPLEMENTATION_COMPLETE

---

## 1. Start-state blocker summary

| Cohort | Count at start | P1-16 outcome |
|--------|----------------|---------------|
| P1-15 `BLOCKED_AMBIGUOUS_PACKAGE_MAPPING` | 4 | 4 remain blocked (`BLOCKED_PACKAGE_IDENTITY_UNRESOLVED`) |
| P1-14/P1-15 biomarker-identity blocked | 9 | 4 opted in; 3 blocked identity; 2 out of scope (medical review) |
| Derived-marker blocked | 7 | Not in scope — unchanged |
| Medical-review blocked | 3 | Not in scope — unchanged |

Baseline after P1-15: 18 production PSI opt-ins complete; 4 package-identity deferrals; 9 biomarker-identity blocks.

---

## 2. Package identity adjudication (4 deferred candidates)

All four candidates share the same unresolved pattern:

| Staged package ID | Staged PSI `package_id` | Production home exists as | Adjudication |
|-------------------|-------------------------|---------------------------|--------------|
| `pkg_kb52c_rbc_high_erythrocytosis_pattern` | `pkg_kb52c_*` | `pkg_kb58_rbc_high_erythrocytosis_pattern` only | **BLOCKED** — STOP gate 1 |
| `pkg_kb52c_rbc_low_iron_restricted_anemia_pattern` | `pkg_kb52c_*` | `pkg_kb58_rbc_low_iron_restricted_anemia_pattern` only | **BLOCKED** — STOP gate 1 |
| `pkg_kb52c_rdw_cv_high_iron_deficiency_anisocytosis` | `pkg_kb52c_*` | `pkg_kb58_rdw_cv_high_iron_deficiency_anisocytosis` only | **BLOCKED** — STOP gate 1 |
| `pkg_kb52c_rdw_cv_high_mixed_red_cell_population_pattern` | `pkg_kb52c_*` | `pkg_kb58_rdw_cv_high_mixed_red_cell_population_pattern` only | **BLOCKED** — STOP gate 1 |

**Evidence:** Staged PSI internal `package_id` matches `pkg_kb52c_*` (e.g. `knowledge_bus/generated_pilot/p1_11_batch_b/pkg_kb52c_rbc_high_erythrocytosis_pattern/promoted_signal_intelligence.yaml:3`). Production packages exist only under `pkg_kb58_*` with KB-S58 compile provenance (`cbc_hematology_pass_3.json`). Cross-ID placement was rejected in P1-15 (GPT Option B). No deterministic identity-normalisation tooling exists in the repository. Creating new `pkg_kb52c_*` production packages was not authorised.

**Resolution path required:** Dedicated package provenance / re-staging sprint (recompile under `pkg_kb58_*` identity or create governed `pkg_kb52c_*` production packages with explicit architectural approval).

---

## 3. Biomarker identity adjudication (9 candidates)

### Newly cleared and opted in (4)

| Candidate | Identity change | SSOT evidence | Medical meaning |
|-----------|-----------------|---------------|-----------------|
| `pkg_kb52c_urea_high_prerenal_*` | `hgb` → `hemoglobin` (supporting + contradiction ref) | `hemoglobin` aliases include `hgb` (`biomarkers.yaml:734`) | Unchanged |
| `pkg_kb52d_non_hdl_cholesterol_high_*` | `non_hdl` → `non_hdl_cholesterol` (primary) | Canonical key `non_hdl_cholesterol` (`biomarkers.yaml:149`) | Unchanged |
| `pkg_kb52c_plt_high_reactive_*` | `plt` → `platelets`; `wbc` → `white_blood_cells` | Aliases under `platelets` / `white_blood_cells` | Unchanged |
| `pkg_kb52c_plt_low_peripheral_*` | `plt` → `platelets`; `wbc` → `white_blood_cells`; `hgb` → `hemoglobin` (override + contradiction) | Same alias mappings | Unchanged |

**Note:** `validate_staged_psi_activation_readiness.py` uses canonical SSOT keys only (`load_ssot_keys()` returns top-level keys). Alias additions to `biomarkers.yaml` would be a no-op for staged validation. Resolution used production PSI canonical ID substitution only — no SSOT file changes.

### Remaining blocked (3)

| Candidate | Blocker |
|-----------|---------|
| `pkg_kb52c_hematocrit_high_absolute_erythrocytosis` | `erythropoietin`, `jak2_v617f` absent from SSOT; no production host package |
| `pkg_kb52c_hematocrit_high_relative_hemoconcentration` | `erythropoietin` absent from SSOT; no production host package |
| `pkg_kb52c_mcv_low_microcytosis_iron_deficiency` | Staged `rbc_count` → canonical `rbc` mappable, but no production host package |

### Out of scope — medical review carry-forward (2)

| Candidate | Reason |
|-----------|--------|
| `pkg_kb52c_lym_low_lymphopenia_stress_or_immunosuppression` | P1-12 medical-review + system-mapping carry-forward; ambiguous `lym` identity |
| `pkg_kb52c_wbc_high_reactive_leukocytosis` | P1-12 medical-review + system-mapping carry-forward |

---

## 4. SSOT changes

**None.** All cleared candidates resolved via production PSI canonical ID normalisation only.

---

## 5. Production PSI artefacts created / opted in

| Production package | PSI path | Manifest opt-in |
|--------------------|----------|-----------------|
| `pkg_kb52c_urea_high_prerenal_volume_depletion_or_catabolic_load` | `promoted_signal_intelligence.yaml` | Added |
| `pkg_kb52d_non_hdl_cholesterol_high_atherogenic_lipoprotein_burden` | `promoted_signal_intelligence.yaml` | Added |
| `pkg_kb52c_plt_high_reactive_thrombocytosis` | `promoted_signal_intelligence.yaml` | Added |
| `pkg_kb52c_plt_low_peripheral_consumption_or_immune_destruction` | `promoted_signal_intelligence.yaml` | Added |

No staged `generated_pilot/` files were modified.

---

## 6. Validation results

```text
validate_knowledge_package.py — 4/4 PASS (ready_for_implementation: True)
validate_promoted_signal_intelligence.py — 4/4 PASS
validate_staged_psi_activation_readiness.py — exit 0
  psi_files_found: 41
  production_opt_ins_found: 42 (was 38 after P1-15; +4 this sprint)
  activation_ready_count: 4
  blocked_count: 37
```

---

## 7. Confirmations

- No derived-marker blocked PSI promoted  
- No medical-review blocked PSI promoted  
- No cross-ID PSI placement  
- No runtime / user-facing activation introduced  
- No `backend/core/`, `backend/scripts/`, `backend/tests/`, `frontend/`, scoring, Gemini, or DTO changes  
- No medical meaning changed — identity metadata only  

---

## 8. Recommended next work package

**P1-17 — Package provenance adjudication for KB-S52c vs KB-S58 CBC cohort**

Resolve the 4 `BLOCKED_PACKAGE_IDENTITY_UNRESOLVED` candidates via governed re-staging or explicit production package creation — not cross-ID opt-in.

Secondary parallel track: **derived-marker authority sprint** for 7 `transferrin_saturation`-blocked iron-panel PSI (unchanged from P1-14 register).

---

## Artefacts

- `docs/sprints/beta_readiness/P1-16_identity_adjudication_manifest.yaml`
- `docs/sprints/beta_readiness/P1-16_psi_identity_blocker_remediation.md` (this file)
- `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md` (updated)
