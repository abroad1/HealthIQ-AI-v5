---
work_id: LC-S12B
branch: scaffold/lc-s12b-core-scaffold-definition
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# LC-S12B — Core Scaffold Definition, Gates and Execution Governance

## Classification

This is a STANDARD-risk CONTENT work package.

Reason: this sprint should create the controlling planning document and supporting governance notes only. It must not modify runtime code, backend logic, frontend logic, tests, Sentinel packs, Knowledge Bus assets, Automation Bus scripts, or application contracts.

If any runtime, test, Sentinel, DTO, frontend, backend, Knowledge Bus, pipeline, scoring, signal, unit, or control-plane file appears necessary, STOP and escalate. Do not reclassify yourself.

The `scaffold/` branch prefix is intentional for the scaffold-completion programme. If repo branch naming policy rejects this prefix, STOP and request human/GPT branch-name approval rather than choosing a replacement.

## Purpose

Create the controlling scaffold-definition document for the next HealthIQ AI build phase.

This sprint defines what “core scaffold complete” means before HealthIQ AI moves from architecture-building mode into governed intelligence-ingestion mode.

This is not a launch-readiness sprint.

This is not a commercial-readiness sprint.

This is not a frontend redesign sprint.

This is not an implementation sprint.

The goal is to turn the approved scaffold roadmap into a clear, governed, usable reference that future LC-S13 to LC-S23B prompts can cite as controlling authority.

## Authoritative input

Use this saved final plan as the primary source:

```text
docs/planning-papers/HealthIQ_AI_Core_Scaffold_Completion_Sprint_Plan_FINAL.md
````

Also inspect these documents if present:

```text
docs/audit-papers/LC-S12A_forensic_architecture_audit.md
docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md
docs/audit-papers/LC-S11_forensic_human_uat_audit.md
docs/audit-papers/LC-S11A_trust_blocker_correction_notes.md
automation_bus/latest_audit_summary.md
automation_bus/latest_cursor_status.json
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md
```

If any of these are missing, record that in the output notes, but do not fail the sprint unless the final scaffold plan itself is missing.

## Required output

Create:

```text
docs/planning-papers/HealthIQ_AI_core_scaffold_completion_definition_v1.md
```

Also create a concise implementation note:

```text
docs/audit-papers/LC-S12B_core_scaffold_definition_notes.md
```

Do not create additional planning documents unless required.

## Mandatory preflight

Before creating or editing files, run and record:

```powershell
git branch --show-current
git status --short
git log --oneline -n 8
```

Then verify:

```powershell
Test-Path automation_bus/state/work_package_active.json
```

Read `automation_bus/state/work_package_active.json` and confirm:

* `work_id` is `LC-S12B`
* branch is `scaffold/lc-s12b-core-scaffold-definition`

If the token is missing or mismatched, STOP with:

```text
Kernel start not executed or work package mismatch.
```

Then verify the authoritative final scaffold plan exists:

```powershell
Test-Path docs/planning-papers/HealthIQ_AI_Core_Scaffold_Completion_Sprint_Plan_FINAL.md
```

If this file is missing, STOP.

## Duplicate authority check

Before writing the new scaffold-definition document, search for competing final scaffold plans.

Check at minimum:

```powershell
Get-ChildItem docs/planning-papers -Recurse | Where-Object { $_.Name -match "Scaffold|scaffold|Sprint|sprint|Completion|completion" } | Select-Object FullName
```

Also search for likely duplicate references:

```powershell
Select-String -Path docs/planning-papers/* -Pattern "Core Scaffold Completion", "LC-S12B", "LC-S23B", "scaffold complete" -ErrorAction SilentlyContinue
```

If duplicate or competing “final” scaffold plans exist, do not choose silently. Record the candidates and STOP for GPT/human authority.

If older drafts exist but the saved final plan is clearly the latest authority, record them as non-authoritative and proceed.

## Scope

Create a scaffold-definition document that defines:

1. What “core scaffold complete” means.
2. What is in scope for the scaffold phase.
3. What is deliberately not in scope.
4. How to distinguish:

   * scaffold defect
   * missing knowledge asset
   * frontend presentation issue
   * clinical content backlog
5. The seven compressed scaffold sprints.
6. The gates that must be enforced across the scaffold phase.
7. Risk classifications and STOP conditions that must be preserved in later prompts.
8. Cross-sprint regression expectations.
9. Sentinel/test-harness expectations.
10. Knowledge Bus lifecycle expectations.
11. DTO/payload contract expectations.
12. Documentation maintenance expectations.
13. The transition criteria from scaffold-completion mode into KB-WAVE intelligence-ingestion mode.

## Required content for scaffold-definition document

The document must include the following sections.

### 1. Executive statement

State clearly:

* HealthIQ AI is not currently trying to launch.
* The next phase is scaffold completion.
* The goal is to complete the machinery so future work becomes governed intelligence ingestion rather than scaffold repair.
* The saved final roadmap is the controlling strategic plan.
* This document is the controlling execution definition for LC-S13 to LC-S23B.

### 2. Definition of scaffold complete

Define scaffold complete as the point where HealthIQ AI has:

* deterministic Layer B analytical engine
* governed signal ingestion pathway
* governed root-cause / WHY ingestion pathway
* safe biomarker canonicalisation
* governed unit handling
* lab-derived reference range preservation
* direction-aware biomarker scoring
* questionnaire/lifestyle propagation pathway
* structured Layer B → Layer C DTO contract
* coherent frontend surfacing of governed assets
* persisted-result replay compatibility
* stale-result strategy
* Sentinel protection for escaped defects and scaffold-defining behaviours
* scalable Knowledge Bus registration process
* maintainable orchestration phases
* SSOT metadata completion for active signal biomarkers
* standing architecture and contributor documentation

### 3. What scaffold complete does not mean

State clearly that scaffold complete does not mean:

* full WHY coverage for all signals
* all biomarkers fully interpreted
* all drug interactions complete
* every disease-context permutation complete
* final frontend design complete
* Gemini activated
* commercial launch ready
* first-user ready
* clinician-grade comprehensive coverage
* all KB-WAVE work complete

### 4. Defect classification model

Create a practical classification table.

Required categories:

| Category                    | Meaning                                                        | Example                                       | Correct response                 |
| --------------------------- | -------------------------------------------------------------- | --------------------------------------------- | -------------------------------- |
| Scaffold defect             | Platform machinery fails or cannot carry governed intelligence | lifestyle modifiers compute but never surface | architecture/scaffold sprint     |
| Missing knowledge asset     | Machinery works but content does not yet exist                 | LDL lacks governed WHY                        | KB-WAVE sprint                   |
| Frontend presentation issue | Governed content exists but is poorly ordered/visualised       | lead WHY buried below generic card            | product/UI sprint after scaffold |
| Clinical content backlog    | Needed medical interpretation not yet authored                 | ferritin + CRP interaction missing            | Knowledge Bus/content sprint     |
| Escaped defect              | Known failure that reached UAT or audit                        | ApoA1 elevated treated as risk                | regression + Sentinel guard      |
| Governance gap              | Missing rule/approval/contract                                 | no persisted replay strategy                  | scaffold governance sprint       |

### 5. Seven compressed scaffold sprints

Summarise the final sequence exactly:

```text
Sprint 1 — LC-S12B       — Core Scaffold Definition, Gates and Execution Governance
Sprint 2 — LC-S13        — Lifestyle Propagation, Coherence Guard and Narrative Language Audit [HIGH]
Sprint 3 — LC-S14        — Direction-Aware Scoring Framework [HIGH]
Sprint 4 — LC-S16/17/19  — Knowledge Asset Frontend Surface, KB Framework and Payload Contract [HIGH]
Sprint 5 — LC-S18        — Root Cause / WHY Registration Generalisation [HIGH]
Sprint 6 — LC-S20/22     — Persisted Replay, Stale-Result Strategy and Sentinel Phase 2 Scaffold
Sprint 7 — LC-S21/23/23B — Orchestrator Decomposition, Scaffold Documentation and SSOT Metadata [HIGH / MIXED]
```

For each sprint, include:

* purpose
* why it matters
* risk classification
* key STOP conditions
* key output
* Sentinel/test expectation
* dependency/gate if applicable

Do not expand into full implementation prompts. This document is the scaffold definition, not the sprint-by-sprint Cursor prompt library.

### 6. Gate model

Document these gates.

#### Gate A — LC-S12B approval gate

LC-S13 may not start until this LC-S12B scaffold-definition document is reviewed and approved by:

* GPT Head of Product Architecture
* Claude Code audit
* Human product owner

Record that approval status must be captured before LC-S13 begins.

#### Gate B — Sprint 4 internal audit-before-implementation gate

Sprint 4 must complete and review the Knowledge Asset Frontend-Surface Audit before implementing or finalising the Knowledge Bus framework and payload-contract hardening elements.

If the audit materially changes the understanding of what is visible, governed, fallback-backed or unsupported, Sprint 4 must STOP and return to GPT/human authority for amended scope.

#### Gate C — Sprint 6 persisted replay fixture gate

Sprint 6 must establish a concrete persisted replay fixture strategy before finalising Sentinel Phase 2 render-level checks.

If Sprint 6 cannot establish a fixture contract, Sentinel Phase 2 scope must be revised by GPT/human authority before implementation continues.

#### Gate D — Cross-sprint guard gate

Every scaffold sprint after LC-S12B must begin by running the current scaffold smoke/regression pack.

If prior scaffold guards fail, the sprint must STOP unless GPT explicitly classifies the failure as unrelated and authorises continuation.

### 7. Global STOP conditions

Define global STOP conditions for all scaffold sprints.

Include:

* work package token missing/mismatch
* wrong branch
* dirty branch ambiguity
* duplicate authority source
* runtime code required in a CONTENT-only sprint
* risk level needs escalation
* required source document missing
* frontend contract change discovered but not authorised
* DTO field rename/removal required but not scoped
* Sentinel requirement identified but not added
* material rescoping required
* prior scaffold regression failing
* scope begins to include launch/commercial/product redesign work

### 8. Cross-sprint regression policy

State:

Every scaffold sprint must begin by running prior scaffold regression/Sentinel guards before implementation.

The smoke pack should grow as each scaffold sprint adds new protections.

Initial categories:

* LC-S8F / LC-S8G unit and display fidelity
* LC-S10B launch-core protection
* LC-S11A trust blocker correction
* LC-S13 lifestyle/coherence guards once created
* LC-S14 direction-aware scoring guards once created
* LC-S16/17/19 DTO/KB surfacing guards once created
* LC-S18 WHY registration guards once created
* LC-S20/22 persisted replay/render guards once created
* LC-S21/23/23B orchestrator/documentation/SSOT guards once created

### 9. Sentinel/test-harness policy

State:

Every scaffold sprint must include a section titled:

```text
Sentinel / test harness obligations
```

It must explicitly state either:

```text
Sentinel update required
```

or:

```text
Sentinel update not required because...
```

Sentinel is required when a defect class is:

* user-facing
* previously escaped
* likely to recur
* cross-layer
* clinically trust-sensitive
* related to unit/display/reference-range safety
* related to internal token or placeholder leakage
* related to DTO compatibility or persisted replay
* related to Knowledge Bus asset surfacing

A known escaped-defect class must not be fixed without a regression/Sentinel guard.

### 10. Risk classification model

Create a scaffold risk table.

At minimum:

| Sprint        |                                             Default risk | Reason                                       |
| ------------- | -------------------------------------------------------: | -------------------------------------------- |
| LC-S12B       |                                                 STANDARD | CONTENT planning document only               |
| LC-S13        |                                                     HIGH | lifestyle, DTO/frontend surfacing, Sentinel  |
| LC-S14        |                                                     HIGH | scoring policy/engine behaviour              |
| LC-S16/17/19  |                                                     HIGH | DTO/frontend/KB contract                     |
| LC-S18        |                                                     HIGH | root-cause WHY registration mechanism        |
| LC-S20/22     | HIGH if API/frontend/Sentinel/persisted DTO work touched | persisted replay and render-level protection |
| LC-S21/23/23B |                                             HIGH / MIXED | pipeline decomposition plus content/doc work |

State that if a sprint touches `backend/core/analytics/`, `backend/core/pipeline/`, `backend/core/scoring/`, `backend/core/dto/`, `backend/ssot/`, Sentinel packs, or frontend result rendering, the prompt must apply SOP HIGH-risk controls unless explicitly justified.

### 11. Knowledge Bus lifecycle expectations

Define required lifecycle states:

* draft
* validated
* runtime-loaded
* signal-only
* WHY-enabled
* frontend-surfaced
* Sentinel-protected

Define that later LC-S16/17/19 must distinguish:

* machine-enforced now
* documented now, machine-enforced later
* advisory only

For:

* orphaned package detection
* package lifecycle state validity
* required file presence for WHY-enabled packages
* signal library schema validity
* root-cause hypothesis metadata validity
* asset coverage reporting for active signals

### 12. DTO / Layer B → Layer C contract principles

State:

* frontend must remain renderer, not analyst
* Layer B must carry structured truth
* Layer C may present/polish but must not invent unsupported interpretation
* DTO field classification is governance work
* DTO field renaming/restructuring/removal must not occur casually
* any DTO shape change must include frontend consumer search, TypeScript update, runtime rendering validation, regression test and stale-result compatibility assessment

### 13. Documentation standing obligation

State:

The documentation created during scaffold completion becomes standing documentation.

Every future KB-WAVE sprint must update documentation if it introduces or changes:

* combination-case pattern
* modifier class
* medication overlay pattern
* WHY registration pattern
* DTO field category
* Sentinel requirement
* Knowledge Bus lifecycle pattern
* frontend surfacing pattern

### 14. Transition criteria into KB-WAVE phase

Define what must be true before systematic KB-WAVE intelligence expansion begins:

* LC-S12B approved
* LC-S13 completed or split/closed
* LC-S14 direction-aware scoring complete
* LC-S16/17/19 frontend-surface and KB/DTO contract complete
* LC-S18 WHY registration generalisation complete or explicitly deferred with mitigation
* LC-S20/22 persisted replay and Sentinel Phase 2 scaffold complete
* LC-S21/23/23B complete or explicitly split/closed
* Tier 1 SSOT metadata complete for active signal biomarkers
* scaffold smoke pack green
* standing docs available

### 15. Expected grade after scaffold completion

State:

```text
Scaffold architecture grade target: A−
Medical application grade target: B+
```

Clarify:

* this is strategic shorthand, not pass/fail
* sprint acceptance is governed by tests, gates, audits and evidence
* medical application grade becomes A-grade only through later KB-WAVE population

## Required implementation note

Create:

```text
docs/audit-papers/LC-S12B_core_scaffold_definition_notes.md
```

It must include:

1. branch and git state
2. source documents inspected
3. duplicate authority check result
4. files created/changed
5. confirmation no runtime code changed
6. unresolved issues
7. recommended approval route for Gate A
8. whether LC-S13 can be drafted next, subject to approval

## Allowed files

Allowed:

```text
docs/planning-papers/HealthIQ_AI_core_scaffold_completion_definition_v1.md
docs/audit-papers/LC-S12B_core_scaffold_definition_notes.md
```

Read-only:

```text
docs/planning-papers/HealthIQ_AI_Core_Scaffold_Completion_Sprint_Plan_FINAL.md
docs/audit-papers/LC-S12A_forensic_architecture_audit.md
docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md
docs/audit-papers/LC-S11_forensic_human_uat_audit.md
docs/audit-papers/LC-S11A_trust_blocker_correction_notes.md
automation_bus/latest_audit_summary.md
automation_bus/latest_cursor_status.json
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md
```

Forbidden:

```text
backend/**/*
frontend/**/*
knowledge_bus/**/*
sentinel/**/*
automation_bus/state/*
automation_bus/latest_gate_evidence.json
automation_bus/latest_gate_output.txt
automation_bus/latest_cursor_status.json
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
```

Do not edit Automation Bus files except through the normal finish command.

## Validation

Because this is a CONTENT-only sprint, validation is mostly file and governance validation.

Run:

```powershell
git diff --name-only
git status --short
```

Confirm only the two allowed output files are changed.

If any other file is modified, STOP.

Check the new scaffold-definition document includes:

* scaffold complete definition
* not-in-scope definition
* defect classification model
* seven compressed sprints
* gates A-D
* global STOP conditions
* cross-sprint regression policy
* Sentinel/test-harness policy
* risk classification model
* Knowledge Bus lifecycle expectations
* DTO contract principles
* documentation standing obligation
* transition criteria to KB-WAVE phase
* grade statement

## Closure requirements

When complete:

1. Run:

```powershell
git branch --show-current
git status --short
git diff --name-only
git log --oneline -n 8
git stash list
```

2. Confirm:

   * only allowed files changed
   * no runtime files changed
   * no Automation Bus files manually edited
   * no untracked unexpected files
   * no stash ambiguity

3. Run finish:

```powershell
python backend/scripts/run_work_package.py finish
```

4. Report whether finish completed or failed.

5. Do not merge.

6. Do not create `automation_bus/latest_audit_summary.md`.

7. Do not claim final approval.

## Cursor completion statement

Cursor implements the documentation artefacts only.

Cursor may not self-certify scaffold approval, architecture approval, merge readiness, launch readiness, or permission to begin LC-S13.

The output of this sprint must go to Claude Code audit, GPT architectural review, and human approval under Gate A before LC-S13 starts.

```
```
