---
work_id: CTRL-01
branch: control/pre-sop-scoping-workflow-adoption
risk_level: LOW
execution_model: TWO_PHASE_START_FINISH
change_type: DOCS
---

# CTRL-01 — Adopt Pre-SOP Prompt Scoping Workflow v0.4 and Pipeline Advisory Fields

You are Cursor, acting as the documentation/control-plane implementation agent.

Implement this tightly bounded documentation package before any further HealthIQ AI product sprint work.

This is not a product sprint.
This is not a runtime sprint.
This is not a prompt-hardening sprint.
This is a control-plane documentation consolidation package to preserve the agreed GPT ↔ Claude pre-SOP scoping workflow.

## Purpose

Bake the agreed pre-SOP prompt-scoping workflow into repository documentation so the intent is not lost.

The key agreement is:

1. Pre-SOP scoping remains separate from the Automation Bus SOP.
2. Stage 0 Pipeline Advisory is adopted at sprint batch boundaries.
3. Stage A/B/C sit before formal Automation Bus hardening.
4. Stage D formal hardening remains unchanged.
5. Stage E Cursor implementation remains unchanged.
6. Stage B is advisory only and must not write hardening JSON or start Automation Bus stages.
7. Automation Bus SOP changes are limited to two audit schema fields:
   - `pipeline_advisory_trigger`
   - `pipeline_advisory_reason`
8. GPT must check audit summaries for `pipeline_advisory_trigger` before authoring the next sprint prompt.
9. If `pipeline_advisory_trigger: true`, GPT must request Claude pipeline advisory before writing the next Stage A concept.
10. `automation_bus/latest_pipeline_advisory.md` becomes the advisory frame for the next sprint batch.
11. Small targeted fixes should not automatically trigger Stage B; they require only a bundling check.
12. Candidate-set/carry-forward sprints require at least Mode 1 scope advisory.
13. Sprint batch boundaries use Stage 0 Pipeline Advisory to sequence the next 3–5 sprints.
14. Full SOP cycles must not be used for tiny product deltas unless urgent safety-critical.

## Mandatory read list

Read before editing:

- docs/discussion documents/healthiq_pre_sop_prompt_scoping_workflow_v0_4.md
- docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
- any existing CLAUDE.md / agent instruction file that governs Claude Code behaviour
- any existing docs index or governance index that lists process documents

Use `rg` to locate if exact paths differ:

- `rg "pipeline_advisory_trigger|pipeline_advisory_reason|latest_pipeline_advisory|latest_scope_advisory" .`
- `rg "Automation Bus SOP|audit output schema|latest_audit_summary" docs automation_bus .`
- `rg "CLAUDE.md|Claude Code|scope-advisory|pre-SOP" .`

## Files in scope

Allowed:

- docs/discussion documents/healthiq_pre_sop_prompt_scoping_workflow_v0_4.md
- docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
- CLAUDE.md or equivalent Claude Code instruction file, if present and appropriate
- docs/process/ or docs/governance/ index files, if present
- docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md only if the repository convention requires recording control-plane documentation packages

If the existing repository has a better canonical process-doc location, use it and record the reason.

## Files out of scope

Do not modify:

- backend/
- frontend/
- knowledge_bus package content
- generated pilot PSI
- raw Pass 3 research
- validators
- tests
- runtime loaders
- DTO/report/Gemini/scoring files
- package manifests
- signal libraries
- promoted signal intelligence files
- any product/runtime implementation file

## Required changes

### 1. Preserve the v0.4 workflow document

Ensure the v0.4 pre-SOP prompt-scoping workflow document exists in the repository.

If it currently sits under `docs/discussion documents/`, leave it there unless the repository has a clear process-doc location.

Do not expand it into a long SOP.

It should remain a concise working convention.

It must preserve these concepts:

- Stage 0 Pipeline Advisory;
- Stage A GPT draft sprint concept;
- Stage B Claude scope advisory;
- Stage C GPT formal SOP prompt;
- Stage D Claude formal hardening unchanged;
- Stage E Cursor implementation unchanged;
- Stage B invocation template;
- Stage D hardening preamble;
- throughput rules;
- documentation discipline;
- evidence cache files:
  - `automation_bus/latest_scope_advisory.md`
  - `automation_bus/latest_pipeline_advisory.md`

### 2. Update Automation Bus SOP audit schema only

In `AUTOMATION_BUS_SOP_v1.3.1.md`, update only the audit output schema section.

Add exactly these two fields:

```yaml
pipeline_advisory_trigger: true | false
pipeline_advisory_reason: "<one-line reason, or omitted if false>"

Do not merge the full pre-SOP workflow into the Automation Bus SOP.

Do not rewrite Automation Bus stages.

Do not alter Stage D/E execution rules.

Do not make pipeline advisory an Automation Bus execution stage.

The Automation Bus SOP should state only that the audit summary must include these fields at Stage 5 close.

3. Update Claude Code guidance if appropriate

If a CLAUDE.md or equivalent Claude Code guidance file exists, add a concise section explaining:

recognise scope-advisory: ... — pre-SOP only, no hardening;
recognise pipeline advisory requests;
do not write latest_prompt_hardening.json during Stage B/Stage 0 advisory;
do not start Automation Bus stages during Stage B/Stage 0 advisory;
write automation_bus/latest_scope_advisory.md for Stage B where practical;
write automation_bus/latest_pipeline_advisory.md for Stage 0;
set pipeline_advisory_trigger and pipeline_advisory_reason in audit summaries when trigger criteria are met.

Keep this concise. Do not duplicate the full v0.4 document.

4. Add or update index/reference if present

If the repository has a governance/process index, add a lightweight reference to:

Pre-SOP Prompt Scoping Workflow v0.4;
Automation Bus SOP v1.3.1 audit schema update;
advisory files:
automation_bus/latest_scope_advisory.md
automation_bus/latest_pipeline_advisory.md

Do not create a large new index if none exists.

5. Keep documentation minimal

This package must not create long sprint reports.

Create only a concise implementation note if required by repository convention.

Maximum content:

files changed;
what was added;
what was intentionally not changed;
next expected use: P1-19 audit should likely set pipeline_advisory_trigger: true.
Acceptance criteria

This package passes only if:

v0.4 pre-SOP scoping workflow is present and preserved.
Automation Bus SOP is updated only with:
pipeline_advisory_trigger
pipeline_advisory_reason
The pre-SOP workflow is not collapsed into Automation Bus SOP.
Stage D and Stage E remain unchanged.
Claude guidance recognises Stage 0/Stage B advisory mode if a Claude guidance file exists.
Advisory files are documented as advisory only, not execution-authorising state.
No runtime/product files are modified.
No Knowledge Bus package/intelligence content is modified.
No raw Pass 3 research is modified.
No tests, validators, backend, frontend, DTO, Gemini, scoring, parser, or runtime files are modified.
Documentation remains concise.
P1-19 closure expectation is recorded: if P1-19 creates multi-domain carry-forwards, audit should set pipeline_advisory_trigger: true.
Validation

Run appropriate repository documentation checks if available.

At minimum run:

git diff --name-only
git diff --check
any markdown lint/check command already used by the repository, if available

Do not invent new tooling.

Closure

Before finish, report:

files changed;
confirmation no product/runtime files changed;
confirmation Automation Bus SOP change was limited to the two audit fields;
confirmation v0.4 workflow remains separate from Automation Bus SOP;
confirmation whether Claude guidance was updated or not present.

Then run the normal completion/closure protocol required for a documentation/control-plane package.

Do not merge without human approval.