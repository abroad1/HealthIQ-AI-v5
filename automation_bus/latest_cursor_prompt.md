---
work_id: LC-S18
branch: scaffold/lc-s18-root-cause-why-registration
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# LC-S18 — Root Cause / WHY Registration Generalisation

## Classification

This is a HIGH-risk BEHAVIOUR scaffold sprint.

Reason: this sprint may touch root-cause / WHY registration machinery, Knowledge Bus package loading, hypothesis discovery, runtime validation, regression tests, Sentinel packs, package inventory reporting and scaffold documentation.

This sprint is part of the approved HealthIQ AI core scaffold completion programme.

This is not a Knowledge Bus content expansion sprint.  
This is not a new medical signal authoring sprint.  
This is not a frontend redesign sprint.  
This is not a DTO restructuring sprint.  
This is not a Gemini/LLM sprint.  
This is not a launch-readiness sprint.

## Purpose

Generalise the root-cause / WHY registration mechanism so future WHY-enabled signals can be added primarily as governed asset work rather than backend code work.

The existing root-cause compiler is a strong part of the application. This sprint must preserve that strength while reducing manual registration bottlenecks.

The goal is not to rewrite the WHY engine. The goal is to make registration scalable, deterministic, validated and safe.

## Core rule

Do not change existing WHY output unless explicitly required, tested and approved.

The required outcome is:

```text
Every currently registered root-cause / WHY target that works before this sprint must still load and produce equivalent WHY output after this sprint.
````

No silent skipping of WHY assets is allowed.

Malformed or incomplete metadata must fail loudly.

## Controlling authority

Read before doing anything:

```text
docs/planning-papers/HealthIQ_AI_core_scaffold_completion_definition_v1.md
docs/planning-papers/HealthIQ_AI_Core_Scaffold_Completion_Sprint_Plan_FINAL.md
docs/audit-papers/LC-S16_knowledge_asset_frontend_surface_audit.md
docs/audit-papers/LC-S17_knowledge_bus_lifecycle_framework.md
docs/audit-papers/LC-S19_payload_contract_hardening_notes.md
docs/audit-papers/LC-S16_17_19_kb_surface_payload_contract_notes.md
```

Also inspect if present:

```text
docs/audit-papers/LC-S12A_forensic_architecture_audit.md
docs/audit-papers/LC-S13_lifestyle_coherence_narrative_notes.md
docs/audit-papers/LC-S14_direction_aware_scoring_notes.md
docs/audit-papers/LC-S11_forensic_human_uat_audit.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md
```

If the scaffold definition document or LC-S17 lifecycle framework is missing, STOP.

## Required output documentation

Create or update:

```text
docs/audit-papers/LC-S18_root_cause_why_registration_generalisation_notes.md
```

This document must include:

1. preflight results
2. current root-cause / WHY registration map
3. current registered target count discovered at sprint start
4. fingerprint of current WHY outputs before change
5. package estate drift findings
6. proposed registration mechanism
7. GPT/Claude review checkpoint result before implementation
8. implementation summary
9. validation and failure-mode behaviour
10. tests added/updated
11. Sentinel updates
12. residual risks
13. recommendation for LC-S20/22

## Mandatory preflight

Run and record:

```powershell
git branch --show-current
git status --short
git log --oneline -n 8
git stash list
```

Verify work-package token:

```powershell
Test-Path automation_bus/state/work_package_active.json
```

Read `automation_bus/state/work_package_active.json` and confirm:

* `work_id` is `LC-S18`
* branch is `scaffold/lc-s18-root-cause-why-registration`

If token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

Confirm controlling docs exist:

```powershell
Test-Path docs/planning-papers/HealthIQ_AI_core_scaffold_completion_definition_v1.md
Test-Path docs/audit-papers/LC-S17_knowledge_bus_lifecycle_framework.md
Test-Path docs/audit-papers/LC-S19_payload_contract_hardening_notes.md
```

If any are missing, STOP.

## Cross-sprint guard preflight

Before implementation, run prior scaffold / launch-core protections.

At minimum run the current equivalents of:

```powershell
python -m pytest backend/tests/regression/test_lc_s8f_phase_b_true_conversions.py -q
python -m pytest backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py -q
python -m pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q
python -m pytest backend/tests/regression/test_lc_s10b_launch_core_protection.py -q
python -m pytest backend/tests/regression/test_lc_s11a_trust_blocker_correction.py -q
python -m pytest backend/tests/regression/test_lc_s13_lifestyle_coherence_narrative.py -q
python -m pytest backend/tests/regression/test_lc_s14_direction_aware_scoring.py -q
python -m pytest backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

If one of these files has a different current name, find the current equivalent and record the substitution.

If a prior scaffold/launch-core guard fails, STOP unless the failure is already documented as unrelated and GPT/human authority explicitly permits continuation.

Do not proceed while prior protected behaviours are broken.

---

# Phase 1 — Current-state authority and target discovery

Before making changes, identify and record current authority paths for:

1. root-cause compiler
2. manually registered WHY targets
3. hypothesis YAML loading
4. Knowledge Bus package estate inventory
5. signal library package loading
6. promoted signal intelligence files
7. package lifecycle contract created in LC-S16/17/19
8. orphan package reporter created in LC-S16/17/19
9. Sentinel packs covering escaped defects
10. tests covering root-cause / WHY output

Known likely files to inspect:

```text
backend/core/analytics/root_cause_compiler_v1.py
backend/core/analytics/**/*
backend/core/knowledge/kb_lifecycle_contract_v1.py
backend/scripts/validate_kb_package_estate_orphans_v1.py
knowledge_bus/packages/**/*
knowledge_bus/package_estate_KB-S49_v1.yaml
backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py
sentinel/packs/escaped_defects_v1.json
```

STOP if multiple competing root-cause / WHY registration authorities exist and the correct one cannot be established.

## Required current-state findings

Record:

* current registered root-cause target count discovered at sprint start
* list of current registered targets
* source file / line range of current registration table
* current hypothesis YAML paths used by registered targets
* which targets have governed WHY output
* which targets rely on fallback
* which packages are on disk but not in the estate inventory
* whether the 109-package drift from LC-S16/17/19 still exists
* whether estate drift affects WHY registration safety
* whether LC-S18 can safely proceed without regenerating the estate inventory

Do not hardcode an expected target count. Discover it at sprint start.

---

# Phase 2 — Fingerprint existing WHY behaviour

Before changing registration logic, create a deterministic fingerprint of existing WHY behaviour.

The fingerprint must include, for every currently registered root-cause target:

* target ID / signal ID
* expected hypothesis asset path, if any
* whether asset loads
* whether output is governed or fallback
* concise WHY output fingerprint
* error state, if any

Store the fingerprint in an audit-safe location, for example:

```text
docs/audit-papers/LC-S18_root_cause_why_registration_before_fingerprint.json
```

If no suitable JSON output format exists, create a deterministic markdown/table fingerprint in the LC-S18 notes.

After implementation, produce the matching after-fingerprint:

```text
docs/audit-papers/LC-S18_root_cause_why_registration_after_fingerprint.json
```

The after-fingerprint must prove equivalent output for all targets present at sprint start.

STOP if you cannot fingerprint current WHY output deterministically.

---

# Phase 3 — Package estate drift assessment

LC-S16/17/19 found that many packages on disk are not represented in the package estate inventory.

Before implementing WHY registration changes, assess the package estate drift.

Run or use:

```powershell
python backend/scripts/validate_kb_package_estate_orphans_v1.py
```

Record:

* number of packages on disk
* number of packages in estate inventory
* orphan count
* whether orphan packages contain WHY-relevant files
* whether orphan packages contain promoted signal intelligence
* whether orphan packages should be ignored, inventoried, or blocked from auto-discovery

## STOP condition — estate drift unsafe for auto-discovery

STOP before implementation if:

* auto-discovery would load orphan packages that are not validated
* orphan packages contain WHY assets that could alter runtime output
* package lifecycle state cannot distinguish validated vs draft assets
* estate inventory is too stale to safely support metadata-driven discovery

If STOP triggers, report whether the correct next step is:

```text
LC-S18A — Package estate inventory refresh and validation
```

rather than root-cause registration generalisation.

Do not silently auto-load unvalidated orphan packages.

---

# Phase 4 — Proposed mechanism and review checkpoint

Before implementation, write a proposed mechanism in the LC-S18 notes.

The proposal must answer:

1. Will the new registration be metadata-driven, hybrid, or manual-table-plus-validation?
2. What metadata is required for a WHY-enabled asset?
3. How are draft/unvalidated packages excluded?
4. How are orphan packages handled?
5. How are malformed assets handled?
6. How are duplicate target IDs handled?
7. How are missing hypothesis files handled?
8. How is deterministic ordering guaranteed?
9. How does this preserve all current registered targets?
10. How can a future WHY-enabled signal be added without bespoke backend code?

## Mandatory review checkpoint

After writing the proposed mechanism but before changing runtime registration behaviour, STOP for GPT/human review unless the implementation is purely documentation/test-only.

Report:

```text
LC-S18 proposed WHY registration mechanism ready for architectural review.
```

Cursor may not self-authorise the migration mechanism.

If GPT/human approval is already explicitly provided in the same conversation after reviewing the proposal, proceed.

If not, stop.

---

# Phase 5 — Implementation requirements

Proceed only after the review checkpoint is approved.

## Required behaviour

The final mechanism must:

* preserve every currently registered target
* preserve current WHY output for all currently registered targets
* fail loudly on malformed metadata
* fail loudly on duplicate target IDs
* fail loudly on missing required files for WHY-enabled assets
* exclude draft/unvalidated/orphan packages unless explicitly permitted
* use deterministic ordering
* support future asset-first registration
* keep fallback behaviour explicit and detectable
* avoid silent skip behaviour

## Allowed implementation patterns

Acceptable patterns include:

1. Hybrid manual table plus metadata validation.
2. Metadata-driven discovery limited to validated/inventory-listed packages only.
3. Manual table retained for now, with validator proving it matches metadata.
4. New registry builder that produces the same target map as the old table.

Do not remove the old manual path until the new path proves equivalence.

A transitional dual-path mechanism is acceptable if it is deterministic and tested.

## Required package metadata expectation

If metadata-driven registration is introduced, a WHY-enabled package must declare enough information to identify:

* package ID
* lifecycle state
* signal ID / target ID
* hypothesis asset path
* supported biomarker/system context
* runtime eligibility
* validation status
* display/IDL link where applicable

If current packages do not yet have this metadata, do not invent broad metadata content. Implement validation/reporting and defer migration where appropriate.

---

# Potentially allowed files

Only edit what is necessary.

Potentially allowed backend:

```text
backend/core/analytics/root_cause_compiler_v1.py
backend/core/analytics/**/*
backend/core/knowledge/**/*
backend/scripts/validate_kb_package_estate_orphans_v1.py
backend/tests/unit/**/*
backend/tests/regression/**/*
```

Potentially allowed docs:

```text
docs/audit-papers/LC-S18_root_cause_why_registration_generalisation_notes.md
docs/audit-papers/LC-S18_root_cause_why_registration_before_fingerprint.json
docs/audit-papers/LC-S18_root_cause_why_registration_after_fingerprint.json
```

Potentially allowed Sentinel:

```text
sentinel/packs/**/*
sentinel/**/*
```

Potentially allowed Knowledge Bus files only if metadata validation absolutely requires minimal non-medical metadata additions and GPT has explicitly approved after the review checkpoint:

```text
knowledge_bus/package_estate_KB-S49_v1.yaml
knowledge_bus/packages/**/*
```

## Forbidden unless GPT explicitly approves

```text
backend/core/scoring/**/*
backend/core/units/**/*
backend/ssot/units.yaml
backend/ssot/scoring_policy.yaml
backend/ssot/biomarkers.yaml
frontend/**/*
automation_bus/state/*
automation_bus/latest_gate_evidence.json
automation_bus/latest_gate_output.txt
automation_bus/latest_cursor_status.json
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
```

Do not modify scoring, unit governance, frontend rendering, SSOT biomarker metadata, or Automation Bus scripts in this sprint.

Do not add new medical Knowledge Bus content.

If those appear necessary, STOP.

---

# Required tests

Add or update deterministic tests for:

## Existing WHY preservation

* every pre-existing registered target still loads
* every pre-existing registered target produces equivalent WHY output
* homocysteine / AB baseline governed WHY remains present
* no registered target silently drops out
* fallback targets remain explicitly detectable

## Metadata / registry safety

* malformed metadata fails loudly
* duplicate target IDs fail loudly
* missing required WHY file fails loudly
* draft/unvalidated package is not auto-loaded
* orphan package is not auto-loaded unless explicitly allowed
* deterministic ordering is stable
* new compliant WHY asset can be discovered or validated without bespoke backend code, if migration proceeds

## Package estate drift

* orphan reporter still detects estate drift
* orphan count/report is deterministic
* package lifecycle state validity is enforced or clearly reported
* required WHY-enabled package files are checked

## Regression preservation

* LC-S8F/G unit and display fidelity still passes
* LC-S11A trust blockers remain fixed
* LC-S13 lifestyle/coherence/narrative protections still pass
* LC-S14 direction-aware scoring protections still pass
* LC-S16/17/19 DTO/KB surfacing protections still pass
* homocysteine lead finding remains intact

---

# Required Sentinel / test harness obligations

Sentinel update is required.

At minimum add/update defect classes:

```text
root_cause_target_not_loaded
why_asset_silent_skip
metadata_malformed_not_failed
why_output_changed_after_registration_migration
new_why_asset_requires_backend_code
orphan_why_asset_auto_loaded
duplicate_why_target_id_not_rejected
```

Each must point to an active deterministic regression test, or the strongest available deterministic guard with documented limitation.

Do not add placeholder Sentinel entries.

---

# Required validation commands

Run prior scaffold guards and new tests.

At minimum:

```powershell
python -m pytest backend/tests/regression/test_lc_s8f_phase_b_true_conversions.py -q
python -m pytest backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py -q
python -m pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q
python -m pytest backend/tests/regression/test_lc_s10b_launch_core_protection.py -q
python -m pytest backend/tests/regression/test_lc_s11a_trust_blocker_correction.py -q
python -m pytest backend/tests/regression/test_lc_s13_lifestyle_coherence_narrative.py -q
python -m pytest backend/tests/regression/test_lc_s14_direction_aware_scoring.py -q
python -m pytest backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

Run the new LC-S18 tests explicitly, for example:

```powershell
python -m pytest backend/tests/regression/test_lc_s18_root_cause_why_registration.py -q
```

Run the orphan reporter:

```powershell
python backend/scripts/validate_kb_package_estate_orphans_v1.py
```

If the orphan reporter exits non-zero due to known drift, record the output. Do not treat known pre-existing drift as a test failure unless the sprint changes the drift state or auto-loads unsafe packages.

If any required existing test file name differs, find and run the current equivalent, then record the substitution.

---

# Optional proving harness check

If runtime WHY output or root-cause payload output changes, run:

```powershell
python backend/tools/launch_core_proving_harness.py
```

If only metadata/stamp changes occur, revert or do not commit metadata-only proving artefacts.

If payload fingerprints change, STOP and report before committing unless the change is expected and approved.

---

# Acceptance criteria

This sprint is complete only if:

* current root-cause / WHY target set is discovered dynamically
* before/after WHY fingerprints are produced
* all pre-existing registered targets still load
* all pre-existing registered targets produce equivalent WHY output
* no silent skip behaviour exists
* malformed metadata fails loudly
* duplicate target IDs fail loudly
* orphan/unvalidated packages are not auto-loaded
* package estate drift is assessed and documented
* future WHY-enabled signal registration is more asset-driven or has a concrete validated migration path
* Sentinel defect classes are active and deterministic
* prior scaffold/launch-core guards still pass
* no new medical Knowledge Bus content is introduced
* no scoring/unit/frontend changes are smuggled into this sprint
* residual risks are documented for LC-S20/22 or KB-WAVE phase

---

# Closure requirements

When complete:

1. Run:

```powershell
git branch --show-current
git status --short
git diff --name-only
git log --oneline -n 8
git stash list
```

2. Classify:

   * tracked modified files
   * staged files
   * untracked files
   * tooling files
   * out-of-scope files
   * stash entries

3. STOP if unrelated files, tooling leakage, dirty branch ambiguity, or stash ambiguity exists.

4. Run finish:

```powershell
python backend/scripts/run_work_package.py finish
```

5. Report whether finish completed or failed.

6. Do not merge.

7. Do not create `automation_bus/latest_audit_summary.md`.

8. Do not claim final approval.

## Cursor completion statement

Cursor implements and reports only.

Cursor may not self-certify clinical correctness, architecture correctness, scaffold completion, merge readiness, launch readiness, or permission to begin the next sprint.

```
```
