# How to Add WHY Coverage v1

## Root-cause registry

- Authority: `backend/core/knowledge/root_cause_registry_v1.py`
- Each target: `RootCauseTargetSpec(signal_id, loader_fn, asset_filename, registration_source="manual_v1")`
- Validation: `validate_root_cause_registry()` — duplicate IDs and malformed entries fail loudly

## LC-S18 hybrid registry state

- 41 governed targets discovered via `get_root_cause_targets()`
- Adding a target requires one registry row + hypothesis YAML asset — **not** compiler loop edits
- Fingerprints: `fingerprint_root_cause_targets()`

## Hypothesis asset requirements

- Governed YAML under `knowledge_bus/packages/`
- Must load without silent skip
- Asset fingerprint tracked in audit papers

## Governed vs fallback WHY

- Registered + fired signal → governed hypotheses from asset
- Unregistered lead → explicit `why_engine_fallback_v1` finding (never silent)

## Fingerprint expectations

- Before/after migration fingerprints must match unless asset content intentionally changes
- See `docs/audit-papers/LC-S18_root_cause_why_registration_generalisation_notes.md`

## Duplicate/malformed metadata failure

- Duplicate `signal_id` → `RootCauseRegistryValidationError`
- Empty signal_id → validation error

## Avoid backend-code coupling

Prefer registry spec + asset over hardcoded compiler tables.

## Standing maintenance

Future KB-WAVE or scaffold sprints must update this document if they introduce or change the relevant architectural pattern.
