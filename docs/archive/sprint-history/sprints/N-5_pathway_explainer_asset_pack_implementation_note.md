# N-5 — Pathway explainer asset pack v1 (implementation note)

## Governed asset location

**`knowledge_bus/pathway_explainers_v1/pathway_explainers_v1.yaml`**

Rationale:

- **`backend/ssot/retail_explainer_v1/registry.yaml`** remains the authority for **short, per-biomarker / per-cluster retail education** (FE-VISUALISATION-B1B), not pathway-grade biology.
- **`knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml`** owns **phenotype display labels and “why it matters” one-liners** for UI gating—not long-form pathway narrative.
- A **dedicated pack** under `knowledge_bus/` keeps compiler-oriented pathway prose **separate from IDL and retail explainers**, avoiding authority blur while staying in the governed Knowledge Bus namespace.

## What was added

- **Pack metadata:** `schema_version`, `pack_version`, `authority` pointer.
- **Two pathways (v1):**
  - `one_carbon_methylation_homocysteine_v1` — methylation / one-carbon / homocysteine, remethylation/transsulfuration, RBC maturation link, bounded “serum B12/folate can look fine” friction, interpretive caution.
  - `lipid_transport_cholesterol_handling_v1` — lipoprotein transport architecture, ApoB/TG/HDL/LDL as one story, beyond single LDL, coexistence of protective and atherogenic features, caution.

Fields are **explicit strings** (e.g. `pathway_role`, `system_in_action`, domain-specific blocks) so a future **narrative compiler** can select slices without parsing one blob.

## Validation

- **`backend/tests/unit/test_pathway_explainers_v1.py`** — loads YAML, asserts both pathway IDs, required field presence and minimum substance.
- **Golden gate:** test included in `backend/scripts/run_baseline_tests.py`.

## What this unblocks

- **N-6 / N-8** and later **deterministic narrative compiler** work can load `pathway_explainers_v1.yaml` by `pathway_id` without coupling to retail or IDL records.

## Limits for later sprints

- No runtime wiring in this sprint; **consumption is file-based** until the compiler imports this pack.
- Content is **educational / interpretive framing**, not thresholds or treatment rules.
