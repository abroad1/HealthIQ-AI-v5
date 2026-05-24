---
work_id: LC-S18A
branch: kb-wave/lc-s18a-package-estate-inventory-refresh
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# LC-S18A — Knowledge Bus Package Estate Inventory Refresh

## Classification

This is a HIGH-risk CONTENT governance sprint.

Reason: this sprint may touch Knowledge Bus package inventory, package lifecycle classification, validation/reporting scripts, regression tests, Sentinel packs and documentation. It must not change analytical runtime behaviour or introduce new medical interpretation content.

This sprint is a KB-WAVE preflight. It exists to make the Knowledge Bus estate trustworthy before KB-WAVE-1 begins.

This is not a WHY expansion sprint.  
This is not a new signal authoring sprint.  
This is not a frontend sprint.  
This is not a scoring sprint.  
This is not a unit-governance sprint.  
This is not a Gemini/LLM sprint.  
This is not a launch-readiness sprint.

## Purpose

Refresh and reconcile the Knowledge Bus package estate inventory so future KB-WAVE work is built against a governed, visible and auditable asset estate.

The scaffold closeout review identified approximately 109 package directories on disk that are not aligned with `package_estate_KB-S49_v1.yaml`. That drift must be assessed before expanding LDL / ApoB / lipid WHY coverage.

The business purpose is:

```text
Turn the Knowledge Bus from a folder estate into a governed asset estate that can be trusted, validated and safely expanded.
````

## Non-negotiable rule

Do not auto-load orphan packages.

Do not promote, validate, approve, deprecate or surface any package silently.

This sprint may classify and inventory package estate state. It must not make orphan packages runtime-active unless explicitly approved.

## Controlling authority

Read before doing anything:

```text
docs/audit-papers/LC_SCAFFOLD_CLOSEOUT_transition_review.md
docs/audit-papers/LC-S18_root_cause_why_registration_generalisation_notes.md
docs/audit-papers/LC-S17_knowledge_bus_lifecycle_framework.md
docs/audit-papers/LC-S16_17_19_kb_surface_payload_contract_notes.md
docs/planning-papers/HealthIQ_AI_core_scaffold_completion_definition_v1.md
docs/developer-guides/how_to_add_signal_package_v1.md
docs/developer-guides/how_to_add_why_coverage_v1.md
docs/developer-guides/healthiq_scaffold_guardrails_v1.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
```

If any of the first three files are missing, STOP.

## Required output documentation

Create:

```text
docs/audit-papers/LC-S18A_package_estate_inventory_refresh_notes.md
```

If useful, also create:

```text
docs/audit-papers/LC-S18A_package_estate_inventory_delta_report.md
```

The notes must include:

1. preflight results
2. current package estate inventory location
3. package directory count on disk
4. package count in inventory
5. orphan package count
6. missing-on-disk inventory entries
7. duplicate package IDs, if any
8. classification of package types found
9. which packages appear WHY-enabled
10. which packages appear signal-only
11. which packages appear draft/incomplete
12. inventory update strategy
13. files changed
14. tests/validators added or updated
15. Sentinel updates
16. residual risks
17. recommendation for KB-WAVE-1

## Mandatory preflight

Run and record:

```powershell
git branch --show-current
git status --short
git log --oneline -n 12
git stash list
```

Verify work-package token:

```powershell
Test-Path automation_bus/state/work_package_active.json
```

Read `automation_bus/state/work_package_active.json` and confirm:

* `work_id` is `LC-S18A`
* branch is `kb-wave/lc-s18a-package-estate-inventory-refresh`

If token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

## Cross-sprint guard preflight

Run the current scaffold smoke pack before implementation.

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
python -m pytest backend/tests/regression/test_lc_s18_root_cause_why_registration.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
python -m pytest backend/tests/regression/test_lc_s21_23_23b_orchestrator_docs_ssot.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

If a prior guard fails, STOP unless GPT/human authority explicitly authorises continuation.

## Phase 1 — Current-state estate assessment

Identify and record:

1. location of package estate inventory
2. all package directories on disk
3. all packages listed in the estate inventory
4. packages on disk but not in inventory
5. packages in inventory but missing from disk
6. duplicate package IDs
7. malformed package folders
8. packages with `signal_library.yaml`
9. packages with WHY / promoted signal intelligence files
10. packages with research briefs
11. packages that appear draft/incomplete
12. packages that appear deprecated/archived
13. packages relevant to LDL / ApoB / lipid transport

Known likely files/paths:

```text
knowledge_bus/package_estate_KB-S49_v1.yaml
knowledge_bus/packages/**/*
backend/core/knowledge/kb_lifecycle_contract_v1.py
backend/scripts/validate_kb_package_estate_orphans_v1.py
```

## Phase 2 — Inventory refresh strategy

Before editing inventory, define the refresh strategy.

Acceptable outcomes:

### Option A — Report-only

If the estate is too messy or package classification cannot be safely inferred, create a report only and do not update inventory.

### Option B — Inventory refresh

If package identity and lifecycle state can be safely inferred, update the estate inventory to match disk state.

### Option C — Partial controlled refresh

Update only packages that can be classified safely and leave unresolved packages in a clearly documented review queue.

Preferred if uncertainty exists:

```text
Option C — Partial controlled refresh.
```

## STOP conditions

STOP before modifying the inventory if:

* package identity cannot be determined safely
* package lifecycle state cannot be inferred or represented
* orphan packages contain medical content that appears unvalidated
* inventory schema is unclear
* updating the inventory would make draft packages appear approved
* runtime loaders would begin loading packages differently as a consequence
* LDL/ApoB package state is unclear and would affect KB-WAVE-1 planning

Do not invent lifecycle status to make the report look complete.

## Phase 3 — Implementation scope

Depending on the selected strategy, do only the minimum safe work.

Allowed implementation types:

* update package estate inventory
* add deterministic estate validation tests
* improve orphan reporter output
* create inventory delta report
* classify packages into review queues
* add Sentinel guard for estate drift
* document package statuses clearly

Not allowed:

* new medical Knowledge Bus content
* new WHY hypothesis content
* signal threshold changes
* runtime package auto-discovery
* root-cause registry expansion
* frontend changes
* DTO changes
* scoring/unit changes

## Required classification fields

Use existing inventory schema where possible.

If schema supports it, classify packages by:

* package ID
* directory path
* lifecycle state
* package type
* has signal library
* has WHY asset
* has research brief
* has tests
* runtime loaded yes/no
* frontend surfaced yes/no
* requires review yes/no
* relevance to KB-WAVE-1 lipid transport yes/no

If these fields do not exist, do not add a large schema expansion without stopping for GPT review. Prefer report-only or minimal schema extension.

## Required tests

Add or update deterministic tests for:

* package estate inventory parses
* package directories are discoverable
* orphan package count is reported deterministically
* inventory entries point to existing directories, unless explicitly marked missing/deprecated
* no draft/unvalidated orphan package is treated as runtime-approved
* WHY-enabled packages have required files, or are clearly flagged
* LDL/ApoB/lipid-relevant packages are identifiable or explicitly absent
* orphan reporter output is stable
* package estate drift is visible in CI/Sentinel

## Required Sentinel / test harness obligations

Sentinel update is required if the sprint changes validators or creates a durable guard.

Add or update defect classes such as:

```text
kb_package_estate_inventory_stale
kb_orphan_package_unreviewed
kb_inventory_entry_missing_on_disk
kb_draft_package_marked_runtime_valid
kb_why_enabled_package_missing_required_files
```

Each must point to an active deterministic test or validator.

Do not add placeholder Sentinel entries.

## Potentially allowed files

```text
knowledge_bus/package_estate_KB-S49_v1.yaml
backend/core/knowledge/kb_lifecycle_contract_v1.py
backend/scripts/validate_kb_package_estate_orphans_v1.py
backend/tests/regression/**/*
backend/tests/unit/**/*
sentinel/packs/**/*
docs/audit-papers/LC-S18A_package_estate_inventory_refresh_notes.md
docs/audit-papers/LC-S18A_package_estate_inventory_delta_report.md
```

## Forbidden unless GPT explicitly approves

```text
backend/core/scoring/**/*
backend/core/units/**/*
backend/core/pipeline/**/*
backend/core/analytics/root_cause_compiler_v1.py
backend/core/knowledge/root_cause_registry_v1.py
backend/ssot/**/*
frontend/**/*
knowledge_bus/packages/**/*   # do not edit medical package content in this sprint
automation_bus/state/*
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
```

Do not edit medical package contents.

If `knowledge_bus/packages/**/*` files require changes, STOP and ask for GPT/human approval.

## Required validation commands

Run prior scaffold guards and new tests.

At minimum:

```powershell
python -m pytest backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py -q
python -m pytest backend/tests/regression/test_lc_s18_root_cause_why_registration.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
python -m pytest backend/tests/regression/test_lc_s21_23_23b_orchestrator_docs_ssot.py -q
```

Run the package estate validator:

```powershell
python backend/scripts/validate_kb_package_estate_orphans_v1.py
```

Run the new LC-S18A tests, for example:

```powershell
python -m pytest backend/tests/regression/test_lc_s18a_package_estate_inventory.py -q
```

If the orphan reporter exits non-zero because unresolved packages remain, that is acceptable only if the sprint has documented the unresolved packages and the test expectations reflect the chosen strategy.

## Acceptance criteria

This sprint is complete only if:

* package estate drift is measured and documented
* package inventory is either safely refreshed or explicitly left report-only with rationale
* orphan packages are not silently auto-loaded
* LDL/ApoB/lipid package readiness is clearly stated
* inventory validation is deterministic
* Sentinel or regression coverage exists for future drift
* no medical package content is changed
* no runtime analytical behaviour changes
* prior scaffold guards still pass
* KB-WAVE-1 can be scoped using a trustworthy estate view

## Closure requirements

Before finish, run:

```powershell
git branch --show-current
git status --short
git diff --name-only
git log --oneline -n 8
git stash list
```

Then run:

```powershell
python backend/scripts/run_work_package.py finish
```

After finish, follow SOP v1.3.1:

* if `automation_bus/latest_cursor_status.json` is the only dirty file and shows kernel-generated COMPLETE status for `LC-S18A`, commit it automatically as:
  `chore(bus): LC-S18A kernel COMPLETE status`
* if any other Automation Bus artefact is dirty, STOP and escalate

Do not merge.

Do not claim KB-WAVE-1 readiness. This sprint informs the decision.

## Cursor completion statement

Cursor implements estate governance only.

Cursor may not self-certify medical correctness, architecture correctness, KB-WAVE readiness, merge readiness, or permission to begin KB-WAVE-1.

```
```
