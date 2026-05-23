# HealthIQ Scaffold Guardrails v1

## Forbidden patterns

- **No fallback parser** for biomarker aliases outside canonical resolver
- **No global/default ranges** where lab-derived ranges exist on the panel
- **No frontend clinical logic** — rendering only
- **No hidden Gemini interpretation** in deterministic analytical path
- **No silent mutation** of historical persisted reports
- **No raw signal/governance/internal IDs** in user-facing text
- **No DTO restructuring** without frontend consumer tracing (LC-S19)
- **No unvalidated orphan package auto-loading**
- **No hardcoded biomarker exceptions** where SSOT policy should govern

## Required practices

- Run cross-sprint guard suite before and after scaffold changes
- Automation Bus SOP for core/scoring/ssot/knowledge_bus work
- Behaviour-preserving refactors must prove fingerprint stability

## Standing maintenance

Future KB-WAVE or scaffold sprints must update this document if they introduce or change the relevant architectural pattern.
