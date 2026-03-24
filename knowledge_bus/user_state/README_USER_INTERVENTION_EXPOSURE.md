# User intervention / exposure (v1)

**What this is:** Governed **user-state** for what a person is taking, doing, or was exposed to, with timeline and provenance. It is **not** the intervention-effects registry (KB-S48a) and **not** package knowledge.

**Contract:** `knowledge_bus/schema/user_intervention_exposure_schema_v1.yaml`

**Validation**

```bash
python backend/scripts/validate_user_intervention_exposure.py --document path/to/record_set.yaml
```

**Canonical class linkage**

- `canonical_class.link_status: mapped` requires `intervention_class_id` to be one of the eight KB-S48a class IDs.
- `canonical_class.link_status: unmapped` requires `intervention_class_id: null` — no guessing; resolve later via alias map / review.

**Timeline**

Use ISO **YYYY-MM-DD** for `effective_from_date` and optional `effective_to_date`. If `is_ongoing` is true, `effective_to_date` must be null.
