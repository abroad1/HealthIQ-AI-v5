# N-7 — Benchmark interpretation entities (implementation note)

## Preflight — what existed vs gap

| Asset family | Limitation for benchmark |
|--------------|---------------------------|
| `ph_vascular_hcy_inflammation_v1` | **Requires systemic inflammation**; not the lead “one-carbon / macrocytosis” object without that gate |
| `ph_metabolic_early_ir_v1` | **Dyslipidaemia dysfunction** (TG↑, HDL↓); opposite of “residual LDL in favourable transport context” |
| IDL + pathway + functional packs (N-5/N-6) | **No single compiler-stable object** binding phenotype ↔ display ↔ explainer ↔ functional read |

## Governed locations chosen

1. **`knowledge_bus/phenotypes/phenotype_map_v1.yaml`** — two new **materialization** phenotypes:
   - `ph_one_carbon_homocysteine_macrocytosis_v1`
   - `ph_lipid_residual_ldl_favourable_transport_v1`  
   Chain expectations **`pending`** (edges not yet on `interaction_map_v1` beyond exploratory LDL–HDL note).

2. **`knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml`** — display authority rows keyed to the same `internal_id` as phenotype id (IDL pattern used elsewhere).

3. **`knowledge_bus/interpretation_entities_v1/benchmark_interpretation_entities_v1.yaml`** — **compiler binding layer**: `interpretation_entity_id` → `phenotype_id`, `idl_internal_id`, `pathway_explainer_id` (N-5), `functional_interpretation_domain_id` (N-6).

## Cross-system vascular synthesis

**Deferred** in pack with rationale (see YAML). Existing vascular–inflammatory phenotype + N-4/N-5/N-6 stack covers that lane; a separate umbrella would duplicate authority.

## Fixtures & regression

- `backend/tests/fixtures/panels/phenotypes/ph_one_carbon_homocysteine_macrocytosis_v1.json`
- `backend/tests/fixtures/panels/phenotypes/ph_lipid_residual_ldl_favourable_transport_v1.json`
- `phenotype_expectations_v1.yaml` extended; `test_interpretation_entities_benchmark_v1.py` validates cross-refs.

## N-8

Compiler can resolve `interpretation_entity_id` → governed content slices without merging pathway, functional, and phenotype authorities.
