# KB-S58B — Promotion summary (bounded)

**date:** 2026-04-08  
**work_id:** KB-S58B  

## Enforced chain coverage (4 total in suite)

| `phenotype_id` | Notes |
|----------------|--------|
| `ph_vascular_hcy_inflammation_v1` | unchanged (legacy enforced) |
| `ph_renal_stress_v1` | unchanged (KB-S56B enforced) |
| `ph_hba1c_metabolic_stress_v1` | **promoted** — `signal_hba1c_high`→`signal_alt_high` in `interaction_map_v1.yaml` (moderate); fixture chains observed with confidence 0.9 |
| `ph_thyroid_lipid_disturbance_v1` | **promoted** — `signal_thyroid_tsh_context`→`signal_ldl_cholesterol_high` and `signal_tsh_high`→`signal_ldl_cholesterol_high` in map; observed max summary confidence ~0.375 → `min_chain_confidence: 0.35` in map/expectations |

## Still pending (and why)

| `phenotype_id` | Reason |
|----------------|--------|
| `ph_metabolic_early_ir_v1` | Primary TG→lipid-transport edge in phenotype map still `requires_research_promotion: true` |
| `ph_iron_deficiency_inflammation_v1` | Primary CRP→iron-deficiency edge still `requires_research_promotion: true` (runtime can chain; SSOT flag not cleared this sprint) |
| `ph_iron_overload_v1` | No `required_edges` / chain path |
| `ph_hepatic_alt_inflammatory_v1` | Phenotype requires `signal_alt_high`→`signal_systemic_inflammation`; map has `signal_alt_high`→`signal_crp_high` only |
| `ph_tsh_axis_metabolic_v1` | Phenotype requires `signal_tsh_high`→`signal_thyroid_tsh_context`; edge absent from interaction map |

## Files touched

- `knowledge_bus/phenotypes/phenotype_map_v1.yaml`
- `backend/tests/fixtures/panels/phenotypes/phenotype_expectations_v1.yaml`
- This note

No fixture JSON changes; `test_phenotype_suite_v1.py` unchanged.
