# CTRL-01 — Pre-SOP Prompt Scoping Workflow Adoption

**work_id:** CTRL-01  
**change_type:** CONTENT (docs/control-plane only)

## Files changed

- `docs/discussion documents/healthiq_pre_sop_prompt_scoping_workflow_v0_4.md` — preserved (committed pre-kernel as discussion lineage)
- `docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md` — audit YAML header: `pipeline_advisory_trigger`, `pipeline_advisory_reason`; Stage 5 close requirement
- `.claude/CLAUDE.md` — §14 Pre-SOP advisory mode (Stage 0 / Stage B)
- `docs/AUTHORITY_MAP.md` — references to v0.4 workflow and advisory cache files

## Intentionally not changed

- Automation Bus stages D/E execution rules
- Runtime, product, Knowledge Bus, tests, validators
- Full pre-SOP workflow merged into Automation Bus SOP

## Next expected use

P1-19 audit close should likely set `pipeline_advisory_trigger: true` if multi-domain carry-forwards remain.
