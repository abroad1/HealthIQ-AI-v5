---
name: pipeline-advisory
description: Pre-SOP Stage 0 pipeline advisory. Writes a prioritised sprint sequence plan to automation_bus/latest_pipeline_advisory.md. NEVER writes advisory content to chat. Use when GPT requests a pipeline advisory at a batch boundary.
---

# Pre-SOP Stage 0 — Pipeline Advisory

## HARD RULE — NO EXCEPTIONS

When this skill is invoked, ALL advisory output MUST be written to files.

**NEVER write advisory content, sprint sequences, carry-forward analysis, or product outcome summaries to the chat window.**

The only permitted chat output is a one-sentence confirmation that the files were written, e.g.:
> "Pipeline advisory written to `automation_bus/latest_pipeline_advisory.md`."

Any violation of this rule is a governance failure.

---

## What this skill does

Executes pre-SOP Stage 0 as defined in `docs/discussion documents/healthiq_pre_sop_prompt_scoping_workflow_v0_5.md` §4 and §6.

Stage 0 is a batch-level sprint sequencing review. It reads all open carry-forward state once and produces a prioritised sprint plan for the next 3–5 sprints, including agent assignment and inter-sprint dependencies.

**This is advisory only.**
- Do NOT write `automation_bus/latest_prompt_hardening.json`
- Do NOT start Automation Bus stages
- Do NOT modify the repository or any governed assets

---

## Files to write (mandatory — both files must be written)

### File 1 — Pipeline Advisory
**Path:** `automation_bus/latest_pipeline_advisory.md`

Use the exact template from §6 of the pre-SOP workflow:

```
PIPELINE ADVISORY — [date]

Carry-forward state:
* [count and headline summary]

Current build position:
* [production opt-in count]
* [internally unblocked items]
* [externally blocked items]
* [remaining launch/beta-critical gaps]

PRODUCT OUTCOMES:
* [What domains/capabilities land at the end of this sequence]
* [Expected production opt-in delta]

MINIMUM SPRINT COUNT: [n]
[One sentence: why this is the minimum. If sequence has more sprints, one sentence per surplus sprint explaining why bundling is not safe.]

RECOMMENDED SPRINT SEQUENCE:
Sprint 1: [theme] | Agent: [x] | Scope: [one line] | Dependency: [none or prior sprint] | Product output: [one line]
Sprint 2: [theme] | Agent: [x] | Scope: [one line] | Dependency: [x] | Product output: [one line]
...

PARALLEL OPPORTUNITIES:
* [what can run concurrently across agent domains]

BLOCKED UNTIL:
* [what requires external resolution before it can proceed]

FIRST SPRINT TO AUTHOR:
* [which sprint GPT should write first]
* [why it is the highest-value next package]
* [whether Stage B Mode 1 is still needed before formal prompt writing]
```

### File 2 — Scope Advisory index entry
**Path:** `automation_bus/latest_scope_advisory.md`

Write a brief header-only entry confirming Stage 0 ran (Stage B per-sprint advisory is superseded when a pipeline advisory is active):

```
STAGE 0 PIPELINE ADVISORY ACTIVE — [date]

Per-sprint Stage B dropped to Mode 1 or skipped for next sprint batch.
See automation_bus/latest_pipeline_advisory.md for sequencing authority.
```

---

## Mandatory derivation sequence (§6 — must appear in File 1)

Complete these three steps IN ORDER before writing the sprint list. Each step's output must appear in the advisory file.

**Step 1 — Identify product outcomes.**
State what domains, capabilities, or production signals become available at the end of the proposed sequence. Use capability language ("thyroid domain card active", "49 → 53 production opt-ins"), NOT carry-forward language ("cf_007 resolved").

**Step 2 — Derive minimum sprint count.**
Working backwards from Step 1 outcomes, state the minimum number of sprints required. Any sequence with more sprints than this minimum requires one sentence of justification per surplus sprint explaining why bundling is not safe.

**Step 3 — Apply the anti-micro-sprint gate to each proposed sprint.**
For every sprint: *"Does this sprint deliver standalone runtime or product output?"*
A sprint that produces only a governance document, ADR, report, or config entry with no accompanying runtime implementation FAILS and must be absorbed into the adjacent implementation sprint unless execution-safety requires separation.

---

## Mandatory repo reads before writing

Read the following before producing the advisory:

1. `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md` — current carry-forward state and build position
2. `automation_bus/latest_audit_summary.md` — last audit close state and `pipeline_advisory_trigger` reason
3. Any carry-forward manifests or handoff files referenced in the audit summary
4. Current candidate package files if relevant to sequencing

---

## Anti-micro-sprint gate — pass criteria

A sprint PASSES if it delivers at least one of:
- A new domain active at runtime
- New signals firing in the production pipeline
- One or more new production PSI opted in
- Scoring behaviour changed or new scoring rail activated
- A user-facing capability activated or meaningfully changed
- A sprint that creates a necessary runtime precondition AND bundles the immediately unlocked capability

A sprint FAILS (micro-sprint) if it produces ONLY:
- A governance document, ADR, or authority record with no accompanying implementation
- A configuration entry or YAML population with no associated runtime activation
- A blocker classification or readiness report
- A single surgical file change that could be a register carry-forward
- Administrative artefacts with no product delta

Failed sprints must be absorbed into the adjacent implementation sprint.

---

## Trigger conditions (when Stage 0 runs)

Claude sets `pipeline_advisory_trigger: true` in `latest_audit_summary.md` at Stage 5 close when ANY of:
- Sprint closed with 4 or more carry-forward items
- Activation-ready validator count is 5 or more
- The sprint's recommended next sprint is itself a candidate-set sprint
- Three or more consecutive sprints produced no new runtime activations or production opt-ins
- The sprint resolved a blocker that unlocks a cohort of downstream candidates
- The logical next steps require more than one agent domain

---

## Completion

After writing both files, confirm in ONE sentence in chat:

> "Pipeline advisory written to `automation_bus/latest_pipeline_advisory.md` and stage index updated in `automation_bus/latest_scope_advisory.md`."

Nothing else in chat.
