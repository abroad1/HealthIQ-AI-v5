# Metabolic Pathway Coverage Audit — HealthIQ AI v5
**Date:** 2026-03-20 | **Auditor:** Claude Code (Sonnet 4.6) | **Basis:** Live codebase read-only

---

## Coverage Matrix

| Pathway | Signal Count | Hypothesis Assets | Phenotype Fixture | Interaction Map Edges | Phenotype Map Coverage | Overall Status |
|---|---|---|---|---|---|---|
| Insulin resistance / primary metabolic cascade | 2 (`signal_insulin_resistance`, `signal_hba1c_high`) | YES — `hba1c_hypotheses_v1.yaml` | YES — `ph_hba1c_metabolic_stress_v1.json` | 6 | YES — `ph_metabolic_early_ir_v1` | **PARTIAL** |
| Lipid transport dysfunction | 4 (`signal_lipid_transport_dysfunction`, `signal_ldl_cholesterol_high`, `signal_hdl_cholesterol_low`, `signal_triglycerides_high`) | NO — none registered to lipid signals directly | YES — `ph_metabolic_early_ir_v1.json`, `ph_thyroid_lipid_disturbance_v1.json` | 7 | YES — `ph_metabolic_early_ir_v1`, `ph_thyroid_lipid_disturbance_v1` | **PARTIAL** |
| Hepatic metabolic stress | 4 (`signal_hepatic_metabolic_stress`, `signal_hepatic_alt_context`, `signal_alt_high`, `signal_ggt_high`) | YES — `alt_hypotheses_v1.yaml` (`signal_hepatic_alt_context` only; `signal_ggt_high` uncovered) | YES — `ph_hepatic_alt_inflammatory_v1.json`, `ph_hba1c_metabolic_stress_v1.json` | 7 | YES — `ph_hepatic_alt_inflammatory_v1`, `ph_hba1c_metabolic_stress_v1` | **PARTIAL** |
| Systemic inflammation | 5 (`signal_systemic_inflammation`, `signal_crp_high`, `signal_inflammation_crp_context`, `signal_neutrophils_high`, `signal_wbc_high`) | NO — no standalone hypothesis file; coupled indirectly inside `alt_hypotheses_v1.yaml` | YES — `ph_vascular_hcy_inflammation_v1.json`, `ph_hepatic_alt_inflammatory_v1.json`, `ph_iron_deficiency_inflammation_v1.json` | 9 | YES — `ph_vascular_hcy_inflammation_v1`, `ph_hepatic_alt_inflammatory_v1`, `ph_iron_deficiency_inflammation_v1` | **PARTIAL** |
| Thyroid-driven metabolic disturbance | 4 (`signal_thyroid_tsh_context`, `signal_tsh_high`, `signal_tsh_low`, `signal_ldl_cholesterol_high`) | YES — `tsh_hypotheses_v1.yaml` (`signal_thyroid_tsh_context` only; `signal_tsh_high`, `signal_tsh_low` uncovered) | YES — `ph_thyroid_lipid_disturbance_v1.json`, `ph_tsh_axis_metabolic_v1.json` | 5 | YES — `ph_thyroid_lipid_disturbance_v1`, `ph_tsh_axis_metabolic_v1` | **PARTIAL** |
| Iron and oxygen transport | 6 (`signal_iron_deficiency_context`, `signal_iron_overload_context`, `signal_ferritin_low`, `signal_ferritin_high`, `signal_hemoglobin_low`, `signal_oxygen_transport_capacity`) | NO — none registered; ferritin referenced as supporting marker in `hcy_hypotheses_v1.yaml` only | YES — `ph_iron_deficiency_inflammation_v1.json` | 5 | YES — `ph_iron_deficiency_inflammation_v1` | **PARTIAL** |
| Renal metabolic stress | 4 (`signal_creatinine_high`, `signal_urea_high`, `signal_urate_high`, `signal_renal_metabolic_stress`) | NO — none registered | YES — `ph_renal_stress_v1.json` | **0** (pending research promotion) | YES — `ph_renal_stress_v1` (chain enforcement: pending) | **MISSING** |

---

## Specific Gaps

### 1. Signals without hypothesis assets

These signals are registered in the signal evaluator and will fire at runtime — but `compile_root_cause_v1()` returns `None` for all of them. No WHY reasoning is produced.

| Pathway | Signals with no hypothesis coverage |
|---|---|
| Insulin resistance | `signal_insulin_resistance` (only `signal_hba1c_high` is covered) |
| Lipid transport dysfunction | `signal_lipid_transport_dysfunction`, `signal_ldl_cholesterol_high`, `signal_hdl_cholesterol_low`, `signal_triglycerides_high` — all four uncovered |
| Hepatic metabolic stress | `signal_hepatic_metabolic_stress`, `signal_ggt_high` — uncovered; `signal_alt_high` uncovered separately from `signal_hepatic_alt_context` |
| Systemic inflammation | `signal_systemic_inflammation`, `signal_crp_high`, `signal_inflammation_crp_context`, `signal_neutrophils_high`, `signal_wbc_high` — all five uncovered |
| Thyroid disturbance | `signal_tsh_high`, `signal_tsh_low` — individual signals uncovered; only `signal_thyroid_tsh_context` has hypotheses |
| Iron / oxygen transport | `signal_iron_deficiency_context`, `signal_iron_overload_context`, `signal_ferritin_low`, `signal_ferritin_high`, `signal_hemoglobin_low`, `signal_oxygen_transport_capacity` — all six uncovered |
| Renal metabolic stress | `signal_creatinine_high`, `signal_urea_high`, `signal_urate_high`, `signal_renal_metabolic_stress` — all four uncovered |

**Total: approximately 30 of ~33 non-hcy signals have no hypothesis asset.**

---

### 2. Pathways with no interaction map edges

| Pathway | Edge count | Gap detail |
|---|---|---|
| Renal metabolic stress | **0** | `signal_creatinine_high → signal_urea_high` is documented in `phenotype_map_v1.yaml` as requiring research promotion before it can be added. No edges are active in `interaction_map_v1.yaml`. |

All other pathways have at least 5 active edges.

---

### 3. Phenotype coverage gaps

All seven pathways have at least one phenotype fixture and one `phenotype_map_v1.yaml` entry. However:

| Pathway | Gap |
|---|---|
| Iron / oxygen transport | Only one phenotype (`ph_iron_deficiency_inflammation_v1`) — covers the iron-deficiency + inflammation pattern only. Iron overload pattern has no phenotype fixture. |
| Renal metabolic stress | `ph_renal_stress_v1` exists but chain enforcement is marked **pending** — the fixture cannot be fully validated until renal interaction map edges are promoted. |
| Insulin resistance | `ph_metabolic_early_ir_v1` requires `signal_lipid_transport_dysfunction` as a required signal — which itself has no hypothesis coverage. The phenotype can fire without WHY for its own required signal. |

---

## Priority Order for Next Sprints

Based on gaps alone, the highest-value additions in order:

1. **Systemic inflammation hypotheses** — 5 signals, 9 interaction edges already wired, 3 phenotype fixtures already in place. Hypothesis authoring alone unlocks WHY across the most-connected pathway in the interaction map.

2. **Lipid transport hypotheses** — 4 signals, 7 edges wired, 2 phenotype fixtures ready. The full lipid WHY chain is structurally in place; only the hypothesis asset is missing.

3. **Iron / oxygen transport hypotheses** — 6 signals, 5 edges wired, 1 phenotype fixture. High biomarker frequency in real panels; iron overload phenotype also missing.

4. **Renal interaction map edges + hypotheses** — the only pathway with zero active edges. Requires research promotion step before edges can be added; edge work and hypothesis work must be sequenced (edges first, then hypotheses).
