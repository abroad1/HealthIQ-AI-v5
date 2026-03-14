# Interaction Map Governance

This document governs changes to interaction map assets under `knowledge_bus/interaction_maps/`.

## Versioning

- `map_version` is the major contract family (`v1`) used by runtime loaders.
- `map_revision` tracks non-breaking map updates within a contract family.
  - Patch bump (x.y.Z): rationale/evidence text refinements, ordering-safe metadata updates.
  - Minor bump (x.Y.0): additive node/edge expansions within already approved pathways.
- Breaking changes require a new map contract version and architecture approval.

## Pathway Authority

- No new pathways without architecture approval.
- Allowed pathways for `v1`:
  - metabolic -> hepatic -> inflammatory -> vascular
  - iron -> hematologic (plus one direct inflammatory modulation edge if in-chain)
  - thyroid -> lipid -> metabolic

## PR Review Expectations

- Every PR touching interaction maps must include:
  - completed `INTERACTION_MAP_REVIEW_CHECKLIST.md` validation
  - updated governance notes when omissions are discovered
  - passing deterministic interaction tests

## Missing Signal Handling

- If a planned edge references a non-existent signal ID:
  - omit the edge
  - record the omission in change notes or coverage/governance report
  - do not invent placeholder IDs
