# Governance helper scripts

Read-only helpers that generate or validate **governance artefacts** only.

## Policy (PASS3-FRAME-INDEX-2 / CF-GOVHELPER-001)

- **Preferred location:** `knowledge_bus/tools/`
- **Allowed:** read-only scans of packages/research; YAML output under `knowledge_bus/governance/`
- **Forbidden:** imports from SignalEvaluator, SignalRegistry, pipeline, frontend; modification of `knowledge_bus/packages/*`

## Existing helpers

| Script | Location | Purpose |
|--------|----------|---------|
| `build_pass3_frame_coverage_audit.py` | `backend/scripts/` | Generate `pass3_frame_coverage_audit_v1.yaml` from KB-MAP-1 register |
| `build_biomarker_medical_frame_tree.py` | `knowledge_bus/tools/` | Generate `docs/architecture/biomarker_medical_frame_tree.md` from frame index + modifier catalogue (regenerate after index expansion) |

Legacy path under `backend/scripts/` is retained where aligned with validator tooling convention.
