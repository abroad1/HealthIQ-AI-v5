---
work_id: ARCH-LEGACY-1_pathway_retirement_audit
branch: work/ARCH-LEGACY-1-pathway-retirement-audit
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# ARCH-LEGACY-1 — Legacy Pathway Retirement Audit

## Purpose

Audit remaining legacy / dual-authority pathways now that the core Wave 1 architecture, medical subsystem visibility model, card evidence enrichment and Layer B narrative brief have been stabilised.

This is an audit-only sprint.

Do not modify production code, compiled artefacts, schemas, tests, packages, frontend components, backend logic, or medical content.

The goal is to classify which old architecture paths can be:

```text
- retired
- retained but unreachable
- retained and explicitly classified
- deferred
- migrated in a later sprint
- removed only after a dependency is complete
````

This sprint must not remove code yet.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
ARCH-RT programme fully merged through ARCH-RT-6
MED-REV-1 merged
MED-REV-2 merged
KB-UTIL-1 merged
LAYER-B-1 merged
docs/sprints/launch_core_carry_forward_register.md present and updated
```

Before creating or switching branch, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 12
git rev-parse HEAD
git rev-parse origin/main
```

STOP if:

```text
- current branch is not main
- local main does not equal origin/main
- working tree is not clean
- LAYER-B-1 is not merged
- docs/sprints/launch_core_carry_forward_register.md is missing
- untracked or uncommitted files are present
```

## Governance classification

```yaml
risk_level: STANDARD
change_type: CONTENT
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This is an audit-only sprint. It must not change production behaviour. It may produce recommendations for future HIGH-risk implementation work.

## Standard rules

This work remains governed by the standard Knowledge Bus and Automation Bus SOPs already active in the repository.

Do not re-read SOPs unless the applicable governance requirement cannot be located.

## Carry-forward register handling

Before investigation, read:

```text
docs/sprints/launch_core_carry_forward_register.md
```

If this audit resolves, reclassifies, or creates carry-forwards, update the register.

Do not leave carry-forwards only in chat, audit summaries, or sprint reports.

## Authoritative inputs

Read these sprint-specific files before investigation:

```text
docs/sprints/launch_core_carry_forward_register.md
docs/audit-papers/PROGRAMME-STATUS-1_healthiq_launch_workstream_consolidation_audit.md
docs/audit-papers/ARCH-RT-6_day_one_architecture_acceptance_audit.md
docs/architecture/ARCH-RT-6_day_one_architecture_guardrails_report.md
docs/audit-papers/active_intelligence_authority_manifest.md
docs/audit-papers/ARCH-RT-5D_unresolved_provenance_register.md
docs/audit-papers/MED-REV-1_wave1_subsystem_visibility_and_label_alignment_report.md
docs/audit-papers/MED-REV-2_wave1_domain_card_copy_alignment_and_result_regeneration_ux_report.md
docs/audit-papers/KB-UTIL-1_pass3_card_evidence_compile_and_consume_report.md
docs/audit-papers/LAYER-B-1_narrative_brief_maturity_report.md
backend/scripts/validate_day_one_architecture.py
```

Also inspect likely legacy / dual-authority implementation areas:

```text
backend/core/analytics/wave1_subsystem_evidence.py
backend/core/knowledge/health_system_card_evidence.py
backend/core/knowledge/domain_flat_card_evidence.py
backend/core/analytics/domain_score_assembler.py
backend/core/analytics/domain_narrative_wave1.py
backend/core/analytics/root_cause_compiler_v1.py
backend/core/knowledge/compiled_hypothesis.py
backend/core/knowledge/load_root_cause_hypotheses.py
backend/core/analytics/signal_evaluator.py
backend/core/analytics/report_compiler_v1.py
backend/core/analytics/narrative_payload_builder_v1.py
knowledge_bus/packages/**
knowledge_bus/compiled/**
sentinel/packs/day_one_architecture_guardrails_v1.json
```

If paths differ, locate and report the actual paths.

## Problem statement

The ARCH-RT programme added strong programmatic guardrails, but did not delete every old pathway.

Known or suspected legacy / dual-authority areas include:

```text
- legacy root-cause YAML path for non-promoted signals
- hard-coded fallback subsystem definitions in wave1_subsystem_evidence.py
- old CV contributor / homocysteine bridge helper paths
- legacy s24 CRP package route
- inferred provenance package/card markers
- batch JSON packages blocked pending extraction
- dead or semi-dead narrative/card helper functions
- old completeness / rail paths that may still exist but should not govern new visible surfaces
```

The audit must determine which of these are safe, guarded, still reachable, or risky.

## Required investigation questions

For each identified legacy or dual-authority path, answer:

```text
1. What is it?
2. Where is it located?
3. What originally used it?
4. Is it still reachable at runtime?
5. If reachable, under what conditions?
6. Is it launch-critical?
7. Is it guarded by ARCH-RT-6 validator / Sentinel / regression tests?
8. Does it conflict with MED-REV-1/2, KB-UTIL-1 or LAYER-B-1?
9. Should it be:
   - deleted
   - retained temporarily
   - retained indefinitely
   - migrated
   - hidden behind explicit classification
   - deferred
10. What future sprint should handle it?
```

## Classification model

Use this classification table:

```text
deleted
retained_unreachable_guarded
retained_reachable_classified
retained_reachable_unguarded
migration_required
retirement_candidate
deferred_non_launch_blocker
launch_blocker
```

No item may remain unclassified.

## Specific areas to audit

### 1. Wave 1 hard-coded subsystem fallback

Investigate:

```text
backend/core/analytics/wave1_subsystem_evidence.py
```

Questions:

```text
- Are hard-coded _Wave1SubsystemDef labels still stale?
- Are they reachable after compiled card evidence routing?
- Could they reintroduce old labels like “Lipid transport” or “Glycaemic control”?
- Are they guarded by validator or tests?
- Should they be removed, updated, or classified?
```

### 2. Legacy cardiovascular narrative helpers

Investigate old CV contributor / homocysteine bridge logic.

Questions:

```text
- Which functions are now dead or only edge-case reachable?
- Could they reintroduce inflammation/homocysteine as score basis?
- Are MED-REV-2 / KB-UTIL-1 tests sufficient?
- Should they be removed or retained for non-card surfaces?
```

### 3. Root-cause legacy YAML path

Investigate:

```text
load_root_cause_hypotheses.py
compiled_hypothesis.py
root_cause_compiler_v1.py
```

Questions:

```text
- Which signals still use legacy YAML root-cause?
- Which signals use compiled promoted hypothesis?
- Is the boundary explicit and guarded?
- What would be required to migrate more signals?
- Is multi-frame root-cause still blocked?
```

### 4. Legacy / inferred provenance packages

Investigate unresolved provenance items.

Questions:

```text
- Which package cohorts remain inferred-only?
- Which are batch JSON blocked?
- Which affect launch-visible Wave 1 surfaces?
- Which can stay deferred?
- Which should be elevated after KB-UTIL-1?
```

### 5. CRP / s24 legacy path

Investigate whether CRP still depends on legacy `pkg_s24_crp_high_inflammation`.

Questions:

```text
- Is CRP still active in SignalEvaluator?
- Is it visible to users after MED-REV-1/2?
- Does it affect hero/pattern surfaces?
- Is it safe to defer, or should a dedicated Pass 3 CRP spec migration be prioritised?
```

### 6. Old completeness / rail logic

Investigate whether old completeness methods can still contradict visible evidence.

Questions:

```text
- Are rail completeness paths still used anywhere user-facing?
- Are flat liver completeness and subsystem union completeness now protected?
- Could future domains reintroduce 1-of-3 vs 2-of-4 style mismatch?
```

### 7. Frontend legacy inference / rendering risks

Investigate frontend result components for old inferred clinical logic.

Questions:

```text
- Does frontend still infer marker role, clinical priority, score meaning or subsystem importance?
- Are new flat evidence components render-only?
- Are source traces/internal IDs protected?
```

## Required validator / Sentinel assessment

Assess whether current guardrails cover:

```text
- domain_flat_card_evidence.py
- hidden_v1 enforcement
- no raw Pass 3 runtime reads
- PSI isolation
- no frontend clinical inference
- no old card evidence reactivation
- total_bilirubin prohibition
- MED-REV-1 visibility partition
- KB-UTIL-1 manifest hash integrity
- LAYER-B-1 hidden/support evidence boundaries
```

Identify any missing guardrails.

Do not implement guardrails in this sprint unless explicitly approved later.

## Required output

Create:

```text
docs/audit-papers/ARCH-LEGACY-1_pathway_retirement_audit.md
```

The report must include:

```text
- executive verdict
- legacy pathway inventory
- classification table
- reachability assessment
- guardrail coverage assessment
- launch-risk assessment
- recommended retirement / migration order
- proposed future sprint list
- carry-forward register updates
```

## Recommended roadmap output

The report must recommend the next action after this audit.

Potential follow-on sprint types:

```text
ARCH-LEGACY-2_targeted_retirement_implementation
KB-UTIL-2_hypothesis_contradiction_confirmatory_surface_design
LLM-NAR-0_translation_design_audit
LAUNCH-UX-2_results_hierarchy_polish
REGEN-1_result_lineage_hardening
```

The audit must not assume all legacy paths should be deleted. It must justify each recommendation.

## Out of scope

Do not:

```text
- delete legacy files
- modify backend logic
- modify frontend components
- change compiled artefacts
- change packages
- change schemas
- change tests
- change validators
- change scoring
- change medical content
- implement migration
- implement LLM translation
- implement UX redesign
```

## Required checks

Run:

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
```

If they fail, STOP and report.

## Manual validation

No browser UAT is required unless the audit identifies a live runtime concern that needs confirmation.

## STOP conditions

STOP and report if:

```text
1. authoritative reports are missing
2. carry-forward register is missing
3. validator fails
4. working tree is not clean
5. investigation reveals a launch blocker
6. audit cannot determine reachability of a critical legacy path
```

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. carry-forward register read/update evidence
3. files inspected
4. legacy pathway classification table
5. reachability findings
6. guardrail coverage findings
7. launch-risk findings
8. recommended next sprint
9. tests/validators run
10. test results
11. confirmation no production code was changed
```

## Closure requirements

Before finish, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
git diff --name-only
git diff --cached --name-only
git stash list
```

Do not run finish unless:

```text
- current branch matches work/ARCH-LEGACY-1-pathway-retirement-audit
- only audit documentation and carry-forward register updates are changed
- no production code is changed
- no helper scripts are committed
- no ambiguous stash exists
- latest commit contains only in-scope audit work
```

## Success criteria

This sprint is complete only if:

```text
1. legacy / dual-authority pathways are inventoried
2. every identified item is classified
3. runtime reachability is assessed
4. guardrail coverage is assessed
5. launch blockers, if any, are identified
6. future retirement / migration order is recommended
7. carry-forward register is updated
8. ARCH-RT-6 validator passes
9. no production code is changed
10. Automation Bus gate passes
```

```
```
