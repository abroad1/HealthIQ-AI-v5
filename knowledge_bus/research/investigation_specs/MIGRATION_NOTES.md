# Investigation Spec Schema Migration Notes

## Scope

These notes apply to investigation spec authoring under:
`knowledge_bus/research/investigation_specs/`.

## Versioning Policy (KB-S47c)

| Contract file | Status | Use |
|---------------|--------|-----|
| `investigation_spec_schema_v1.yaml` | Legacy | Existing v1 specs only; do not use for new work. |
| `investigation_spec_schema_v2.yaml` | Legacy | Existing `inv_*.yaml` inventory (S24 and historical). No contract field required. |
| `investigation_spec_schema_v3.0.0.yaml` | Current for **new** LLM output | All **new** biomarker investigation specs from research generation MUST set `investigation_spec_contract_version: "3.0.0"` and satisfy v3. |

### Backward compatibility

- **v2 lineage** (no `investigation_spec_contract_version`, or value `2.0.0`) remains valid. Do not bulk-rewrite existing `inv_*.yaml` solely for migration.
- **v3** is a **versioned successor** (separate schema file). It aligns upstream authoring with the locked package intelligence model (`intelligence_model_schema_v1.yaml`): multi-hypothesis structure, explicit `relationship_kind` on supporting markers, hypothesis-level `contradiction_markers`, and required `confirmatory_tests`.

### Validation

- Run: `python backend/scripts/validate_investigation_spec.py --spec <path>`
- Emits `contract_mode: v2` or `v3` and writes `backend/artifacts/investigation_spec_audit.md`.

## Narrative Contract Authority (v2 and v3)

- `narrative.supporting_marker_roles` (string) remains the single runtime-authoritative prose field for package translation of `explanation.supporting_marker_roles`.
- Optional `narrative.supporting_marker_roles_map` is documentation-only and non-runtime authoritative in both v2 and v3.

## v3 authoring highlights (intelligence-aligned)

- Every `supporting_markers[]` entry MUST include **`relationship_kind`**: `mechanism` | `corroboration` | `severity` | `differential` | `exclusion`, aligned with **`role`** (see schema `relationship_kind_role_alignment`).
- At least one supporting marker MUST use **`relationship_kind: differential`** (reduces under-labelled batch-style outputs).
- **`hypotheses`**: minimum **two** structured hypotheses; each lists **`supporting_marker_refs`** that MUST match `supporting_markers[].biomarker_id` values.
- **`contradiction_markers`** live **under each hypothesis** (hypothesis-level counter-evidence), not at signal root.
- **`confirmatory_tests`**: at least one structured next-step test with `ct_*` ids.
- **`hypothesis_ranking.ordered_hypothesis_ids`** must enumerate exactly the declared hypotheses.

## Operational guidance

- Preserve v2 for historical inventory and in-flight translation.
- Require **v3** for all **new** research LLM outputs after KB-S47c.
- Do not mutate `investigation_spec_schema_v2.yaml` in place for v3 features; extend via `investigation_spec_schema_v3.0.0.yaml` only.
