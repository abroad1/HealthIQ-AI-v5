# LC-S23 — Scaffold Documentation and Developer Onboarding Notes

## Objective

Provide standing architecture and contributor guides describing the **actual** runtime implementation.

## Files created

| Path | Purpose |
|------|---------|
| `docs/architecture/HealthIQ_AI_runtime_architecture_map_v1.md` | End-to-end runtime map |
| `docs/developer-guides/how_to_add_signal_package_v1.md` | Signal package lifecycle |
| `docs/developer-guides/how_to_add_why_coverage_v1.md` | WHY / root-cause registration |
| `docs/developer-guides/how_to_add_lifestyle_modifier_v1.md` | Lifestyle modifier path |
| `docs/developer-guides/how_to_test_intelligence_asset_v1.md` | Testing and Sentinel |
| `docs/developer-guides/healthiq_scaffold_guardrails_v1.md` | Non-negotiable guardrails |
| `docs/developer-guides/scaffold_defect_vs_missing_content_classification_v1.md` | Defect taxonomy |

## Validation

- Existence and required headings enforced by `test_lc_s21_23_23b_orchestrator_docs_ssot.py`
- Each guide includes a standing-maintenance obligation for future KB-WAVE / scaffold sprints

## Standing maintenance

Future KB-WAVE or scaffold sprints must update these documents if they introduce or change the relevant architectural pattern.
