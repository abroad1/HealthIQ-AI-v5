# Intervention-Effects Registry (v1)

**Purpose:** Class-level reference for how broad intervention categories plausibly affect biomarker interpretation.  
**Not:** A drug dictionary, dosing guide, or runtime threshold/signal rule store.

**Artifacts**

- `intervention_effects_registry_v1.yaml` — canonical registry (8 approved class IDs).
- `intervention_class_alias_map_v1.yaml` — optional normalized alias → class map (skeleton; expand later).

**Validation**

```bash
python backend/scripts/validate_intervention_effects_registry.py
```

Phase-1 boundary: documents must not contain keys encoding threshold/signal mutation semantics (see schema `forbidden_key_fragments`).
