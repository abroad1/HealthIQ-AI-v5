# Renal edge rationale: signal_creatinine_high → signal_urea_high (co-occurrence)

**Status:** Governed promoted rationale (KB-S56A).  
**Authoritative promotion record:** `knowledge_bus/phenotypes/research_refs/ref_edge_renal_creatinine_to_urea_v1.yaml` (cited from `phenotype_map_v1.yaml` for `ph_renal_stress_v1`).

## Relationship

- **From:** `signal_creatinine_high`
- **To:** `signal_urea_high`
- **Type:** Co-occurrence (same renal clearance / azotaemia interpretation frame).
- **Strength:** Strong (governance: investigation specs + promoted KB-S52C packages).

## Evidence basis

1. **Creatinine spec (`inv_creatinine_high_renal_v1.yaml`):** Urea is a **corroborator** with expected direction **high** when interpreting elevated creatinine; both rise in intrinsic renal impairment; urea is also more sensitive to hydration and protein load, so pairing matters clinically.
2. **Urea spec (`inv_urea_high_renal.yaml`):** Creatinine is a **corroborator** with expected direction **high**; when **both** are high, intrinsic renal disease is more likely than isolated prerenal urea elevation; explicit override `or_urea_intrinsic_renal` encodes creatinine-above-range as an escalation path.
3. **Promoted packages:** `pkg_kb52c_creatinine_high_reduced_glomerular_filtration` and `pkg_kb52c_urea_high_prerenal_volume_depletion_or_catabolic_load` provide runtime signal definitions and explanation blocks consistent with the above physiology.

## Interpretation guardrails

- Co-occurrence here **does not** assert acute kidney injury vs CKD; it records that **joint elevation** is a **governed renal stress pattern** for phenotype assembly, distinct from volume-only urea shifts when creatinine is not corroborating.
- Hydration, muscle mass, and catabolic state remain confounders as documented in the investigation specs; phenotype consumers must not overclaim mechanism from blood chemistry alone.

## Out of scope for this artefact

- Interaction-map runtime edges (KB-S56B).
- Root-cause / clinician hypothesis loaders (KB-S56B).
