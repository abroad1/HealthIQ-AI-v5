# Intervention-Effects Registry (v1)

**Purpose:** Class-level reference for how broad intervention categories plausibly affect biomarker interpretation.  
**Not:** A drug dictionary, dosing guide, or runtime threshold/signal rule store.

**Artifacts**

- `intervention_effects_registry_v1.yaml` — canonical registry (8 approved class IDs).
- `intervention_class_alias_map_v1.yaml` — governed normalized alias → class map (KB-S48c populated).

**Unknown user-entered names (KB-S48c)**

The alias map includes `unknown_name_handling.resolution: unmapped`. Strings not listed under `aliases` must resolve to **no** canonical class ID at preprocessing time — no fuzzy or heuristic mapping into the eight classes. Use `core.knowledge.intervention_alias_resolution` for deterministic lookup.

**Validation**

```bash
python backend/scripts/validate_intervention_effects_registry.py
```

Phase-1 boundary: documents must not contain keys encoding threshold/signal mutation semantics (see schema `forbidden_key_fragments`).
