# Investigation Spec Schema Migration Notes

## Scope

These notes apply to investigation spec authoring under:
`knowledge_bus/research/investigation_specs/`.

## Versioning Policy

- `investigation_spec_schema_v1.yaml` remains accepted for existing specs.
- Existing v1 specs should not be rewritten solely for schema migration.
- `investigation_spec_schema_v2.yaml` is required for all new specs going forward.

## Narrative Contract Authority

- In v2, `narrative.supporting_marker_roles` (string) is the single runtime-authoritative narrative field.
- Package translation must source `explanation.supporting_marker_roles` from this string field only.

### Documentation-only helper map

- v2 also allows optional `narrative.supporting_marker_roles_map`.
- This map is documentation-only and non-runtime authoritative.
- It must NOT be translated into package outputs.
- It must NOT be used to generate explanation payload fields.

## Deterministic Translation Improvements in v2

- Override-rule conditions are explicit and mode-specific (`lab_range_boundary`, `numeric_value`, `presence`).
- Activation enum alignment includes `lab_range_exceeded` and `deterministic_threshold`.
- `test_vectors` is optional but recommended for deterministic no-trigger / baseline / escalation test generation.

## Operational Guidance

- Continue accepting v1 for historical inventory and in-flight items.
- Require v2 for new research LLM outputs to reduce translation drift in coverage sprints.
