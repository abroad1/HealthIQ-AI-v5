# Interaction Map Review Checklist

Use this checklist for all changes to `knowledge_bus/interaction_maps/interaction_map_v1.yaml`.

1) **Edge fields present and valid**
- Every edge includes `from_signal`, `to_signal`, `relationship_type`, `evidence_strength`, and `rationale`.
- `relationship_type` is one of: `driver`, `consequence`, `co_occurrence`, `bidirectional`.
- `evidence_strength` is one of: `exploratory`, `moderate`, `strong`, `consensus`.
- `rationale` is at least 20 characters.

2) **Scope rule**
- Edges remain inside approved pathways only:
  - metabolic -> hepatic -> inflammatory -> vascular
  - iron -> hematologic (plus at most one direct inflammatory modulation edge)
  - thyroid -> lipid -> metabolic
- No new pathways are introduced.

3) **Signal existence rule**
- Both edge endpoints exist as signal IDs in repository signal libraries.
- Missing endpoints are not added; edge is omitted and documented.

4) **Auditability rule**
- Every edge has explicit rationale and explicit evidence strength.
- Rationale explains why the directed relationship is clinically interpretable.

5) **Regression rule**
- Edge isolation test passes:
  - adding/removing edges for signals absent from a panel does not change that panel's interaction outputs.
