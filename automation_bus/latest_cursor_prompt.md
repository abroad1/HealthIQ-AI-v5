---
work_id: LC-S20-22
branch: scaffold/lc-s20-22-persisted-replay-sentinel-phase2
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# LC-S20/22 — Persisted Replay, Stale-Result Strategy and Sentinel Phase 2 Scaffold

## Classification

This is a HIGH-risk MIXED scaffold sprint.

Reason: this sprint may touch persisted result compatibility, replay DTO handling, API/result rendering smoke checks, Sentinel structure, escaped-defect guard organisation, regression tests, and documentation.

This sprint is part of the approved HealthIQ AI core scaffold completion programme.

This is not an analytical logic sprint.  
This is not a scoring sprint.  
This is not a unit-governance sprint.  
This is not a Knowledge Bus content expansion sprint.  
This is not a frontend redesign sprint.  
This is not a Gemini/LLM sprint.  
This is not a launch-readiness sprint.

## Purpose

Ensure stored reports remain compatible and trustworthy after code changes, then extend Sentinel from backend escaped-defect checks into product-level and render-level protection.

This sprint combines:

```text
LC-S20 — Persisted Replay Scaffold and Stale-Result Strategy
LC-S22 — Sentinel Phase 2 Scaffold
````

The sequence is mandatory:

```text
1. Establish persisted-result replay fixture strategy.
2. Define stale-result handling policy.
3. Only then build Sentinel Phase 2 render/API-to-render guards around that strategy.
```

If a concrete persisted replay fixture strategy cannot be established, STOP before implementing Sentinel Phase 2 render-level checks.

## Controlling authority

Read before doing anything:

```text
docs/planning-papers/HealthIQ_AI_core_scaffold_completion_definition_v1.md
docs/planning-papers/HealthIQ_AI_Core_Scaffold_Completion_Sprint_Plan_FINAL.md
docs/audit-papers/LC-S16_knowledge_asset_frontend_surface_audit.md
docs/audit-papers/LC-S17_knowledge_bus_lifecycle_framework.md
docs/audit-papers/LC-S19_payload_contract_hardening_notes.md
docs/audit-papers/LC-S16_17_19_kb_surface_payload_contract_notes.md
docs/audit-papers/LC-S18_root_cause_why_registration_generalisation_notes.md
```

Also inspect if present:

```text
docs/audit-papers/LC-S12A_forensic_architecture_audit.md
docs/audit-papers/LC-S13_lifestyle_coherence_narrative_notes.md
docs/audit-papers/LC-S14_direction_aware_scoring_notes.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md
```

If the scaffold definition document is missing, STOP.

## Required output documentation

Create:

```text
docs/audit-papers/LC-S20_persisted_replay_stale_result_strategy.md
docs/audit-papers/LC-S22_sentinel_phase2_scaffold_notes.md
```

Also create one combined implementation note:

```text
docs/audit-papers/LC-S20_22_persisted_replay_sentinel_phase2_notes.md
```

The combined implementation note must include:

1. preflight results
2. prior scaffold guard results
3. persisted replay current-state assessment
4. stale-result policy decision
5. Sentinel Phase 2 structure decision
6. Sentinel pack rationalisation decision
7. files changed
8. tests added/updated
9. render/API smoke coverage added
10. residual risks
11. recommendation for LC-S21/23/23B

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

* `work_id` is `LC-S20-22`
* branch is `scaffold/lc-s20-22-persisted-replay-sentinel-phase2`

If token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

Confirm controlling docs exist:

```powershell
Test-Path docs/planning-papers/HealthIQ_AI_core_scaffold_completion_definition_v1.md
Test-Path docs/audit-papers/LC-S19_payload_contract_hardening_notes.md
Test-Path docs/audit-papers/LC-S18_root_cause_why_registration_generalisation_notes.md
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
python -m pytest backend/tests/regression/test_lc_s18_root_cause_why_registration.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

If one of these files has a different current name, find the current equivalent and record the substitution.

If a prior scaffold/launch-core guard fails, STOP unless the failure is already documented as unrelated and GPT/human authority explicitly permits continuation.

Do not proceed while prior protected behaviours are broken.

---

# Phase 1 — Current-state inventory

Before changing anything, identify and record current authority paths for:

1. persisted analysis storage / retrieval
2. saved analysis DTO shape
3. replay manifest generation
4. result version handling
5. API route that serves stored results
6. frontend result-page render path
7. existing Playwright/e2e framework, if any
8. Sentinel runner / pack structure
9. current escaped-defects pack usage
10. DTO root-key contract from LC-S16/17/19
11. existing launch-core proving harness
12. any current stale-result or migration logic

Known likely files to inspect:

```text
backend/app/routes/analysis.py
backend/core/dto/**/*
backend/core/analytics/**/*
backend/core/pipeline/**/*
backend/tests/regression/**/*
backend/tools/launch_core_proving_harness.py
frontend/app/(app)/results/page.tsx
frontend/app/types/analysis.ts
frontend/e2e/**/*
frontend/tests/**/*
sentinel/**/*
sentinel/packs/**/*
docs/audit-papers/launch-core-proving/latest_fingerprints.json
docs/audit-papers/launch-core-proving/PROVING_REPORT.md
```

STOP if there are multiple competing persisted replay authorities and the correct one cannot be established.

---

# Phase 2 — LC-S20 persisted replay and stale-result strategy

## Objective

Upgrade persisted-result replay from a weak placeholder/schema check into a real scaffold compatibility contract.

A report generated today should either:

```text
1. remain renderable and interpretable after future code changes, or
2. be clearly marked stale / requiring regeneration.
```

## Required current-state questions

Answer explicitly:

1. Where are analysis results persisted?
2. What exact DTO is persisted?
3. What fields are required for result-page rendering?
4. Is `result_version` meaningful?
5. Is `replay_manifest` meaningful?
6. Is there an engine/version stamp?
7. Can an older result be identified as stale?
8. Is there a migration path?
9. Does the frontend distinguish fresh vs stale results?
10. Is stored JSON immutable historical output or regeneratable analysis?

## Required stale-result policy decision

Define and document one of these policies:

### Option A — Immutable historical report

Stored reports are preserved as generated. New code does not reinterpret old reports unless the user explicitly regenerates.

Required implication:

* old report must continue to render
* engine version must be visible internally
* stale warning may be needed if old report predates major scaffold fixes

### Option B — Regeneratable report

Stored raw input is replayed through the current engine to produce updated output.

Required implication:

* raw input and questionnaire context must be preserved
* regenerated output may differ
* user-facing distinction between original and regenerated report may be needed

### Option C — Hybrid

Stored reports render as historical artefacts, with optional regeneration if raw input is available.

Required implication:

* persisted report compatibility is still required
* regeneration capability is explicit and not silent

Preferred unless repo evidence says otherwise:

```text
Hybrid: persisted report renders as historical output; regeneration is explicit when raw inputs are available.
```

Do not silently mutate historical reports.

## Required persisted replay fixture strategy

Create or identify at least one fixture that represents a stored analysis DTO.

The fixture must include, at minimum:

* analysis_id
* biomarkers
* consumer_domain_scores
* clinician_report_v1
* narrative_report_v1
* interpretation_display_layer_v1
* replay_manifest
* meta
* result_version

If no existing fixture is suitable, create a minimal deterministic fixture from a current known-good analysis.

## Required compatibility checks

Add deterministic tests proving:

* persisted DTO has required root keys
* persisted DTO can be loaded by current backend compatibility path
* persisted DTO has enough fields for frontend rendering
* missing critical fields fail clearly or mark stale
* stale/legacy version is detectable
* current DTO root-key contract remains compatible with persisted fixture

## Required output

Create:

```text
docs/audit-papers/LC-S20_persisted_replay_stale_result_strategy.md
```

Use this structure:

```md
# LC-S20 — Persisted Replay and Stale-Result Strategy

## 1. Executive verdict

## 2. Current persisted-result architecture

## 3. Stored DTO fields

## 4. Replay manifest assessment

## 5. Result/versioning assessment

## 6. Stale-result policy decision

## 7. Persisted replay fixture strategy

## 8. Compatibility checks added

## 9. Failure behaviour

## 10. Residual risks

## 11. Implications for Sentinel Phase 2
```

## STOP condition

STOP before Sentinel Phase 2 implementation if:

* no persisted replay fixture can be established
* current persisted outputs cannot be loaded deterministically
* result-version/stale-state cannot be detected at all
* frontend render requirements cannot be mapped to stored DTO fields
* establishing replay compatibility requires broad DTO restructuring

If STOP triggers, Cursor may not self-rescope. Report findings for GPT/human decision.

---

# Phase 3 — LC-S22 Sentinel Phase 2 scaffold

Proceed only after Phase 2 establishes a concrete persisted replay fixture strategy.

## Objective

Extend Sentinel from backend escaped-defect tracking into product-level, DTO-level and render-level protection.

## Required Sentinel structure decision

The Sentinel estate is growing.

Current known issue:

```text
escaped_defects_v1.json is becoming a broad catch-all pack.
```

Decide and document one of these structures:

### Option A — Keep single escaped-defects pack

Continue adding escaped and scaffold-defining defects to `escaped_defects_v1.json`.

Must include grouping metadata by sprint/domain.

### Option B — Introduce scaffold-phase packs

Create separate packs such as:

```text
sentinel/packs/scaffold_lc_s20_22_replay_render_v1.json
sentinel/packs/scaffold_payload_contract_v1.json
sentinel/packs/scaffold_why_registry_v1.json
```

### Option C — Hybrid

Keep `escaped_defects_v1.json` for escaped defects and create new scaffold packs for planned scaffold guards.

Preferred:

```text
Hybrid: keep escaped_defects_v1.json for escaped defects; create scaffold-specific packs for planned scaffold behaviours.
```

Do not reorganise existing Sentinel packs destructively unless fully tested.

## Required Sentinel Phase 2 coverage

Add or prepare deterministic guards for:

* persisted result schema compatibility
* persisted result render/API smoke
* stale analysis unmarked
* results page missing primary finding
* results page placeholder text visible
* results page internal token visible
* results page unit display regression
* results page missing domain cards
* DTO root-key drift
* Knowledge Bus asset surfacing regression

## Required render/API smoke path

Add at least one smoke path that starts with a persisted or fixture DTO and proves it can support result-page rendering.

Acceptable forms:

1. backend API-to-DTO smoke test if frontend render tools are not available
2. frontend type/render smoke test if existing frontend test harness supports it
3. Playwright route smoke if existing Playwright setup is reliable
4. minimal TypeScript/component render check if frontend test infra exists

Do not build a large brittle UI automation suite.

The minimum acceptable Phase 2 guard is:

```text
A stored/persisted DTO fixture can be loaded and provides all fields required by the result-page contract, with no placeholder/internal-token leakage in user-facing sections.
```

## Required output

Create:

```text
docs/audit-papers/LC-S22_sentinel_phase2_scaffold_notes.md
```

Use this structure:

```md
# LC-S22 — Sentinel Phase 2 Scaffold

## 1. Executive verdict

## 2. Existing Sentinel pack assessment

## 3. Chosen Sentinel Phase 2 structure

## 4. Persisted replay fixture dependency

## 5. New/updated defect classes

## 6. Render/API smoke path

## 7. DTO/schema compatibility guards

## 8. Placeholder/internal-token guards

## 9. Unit/display fidelity guards

## 10. Knowledge Bus surfacing guards

## 11. What remains deferred

## 12. Recommended next Sentinel work
```

---

# Potentially allowed files

Only edit what is necessary.

Potentially allowed backend:

```text
backend/core/dto/**/*
backend/core/analytics/**/*
backend/app/routes/analysis.py
backend/tests/unit/**/*
backend/tests/regression/**/*
backend/tests/fixtures/**/*
backend/tools/**/*
```

Potentially allowed frontend tests only:

```text
frontend/tests/**/*
frontend/e2e/**/*
frontend/app/types/**/*
```

Potentially allowed Sentinel/docs:

```text
sentinel/packs/**/*
sentinel/**/*
docs/audit-papers/LC-S20_persisted_replay_stale_result_strategy.md
docs/audit-papers/LC-S22_sentinel_phase2_scaffold_notes.md
docs/audit-papers/LC-S20_22_persisted_replay_sentinel_phase2_notes.md
```

## Forbidden unless GPT explicitly approves

```text
backend/core/scoring/**/*
backend/core/units/**/*
backend/ssot/units.yaml
backend/ssot/scoring_policy.yaml
backend/ssot/biomarkers.yaml
knowledge_bus/**/*
frontend/app/(app)/results/page.tsx
frontend/app/components/**/*
frontend/app/lib/**/*
automation_bus/state/*
automation_bus/latest_gate_evidence.json
automation_bus/latest_gate_output.txt
automation_bus/latest_cursor_status.json
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
```

Do not modify scoring, unit governance, Knowledge Bus content, production frontend rendering, SSOT biomarker metadata, or Automation Bus scripts in this sprint.

If those appear necessary, STOP.

---

# Required tests

Add or update deterministic tests for:

## Persisted replay

* persisted DTO fixture loads
* required root keys present
* replay manifest present and parseable
* result_version present
* stale/legacy version detectable
* missing critical fields fail clearly or mark stale
* DTO fixture satisfies frontend-consumed root-key contract
* persisted fixture does not leak internal-only fields into user-facing text checks

## Sentinel Phase 2

* Sentinel pack structure validates
* new defect classes are present and active
* each new defect class points to an active deterministic test
* escaped-defects pack is not allowed to silently become unstructured catch-all if new structure is chosen
* render/API smoke path passes

## Regression preservation

* LC-S8F/G unit and display fidelity still passes
* LC-S11A trust blockers remain fixed
* LC-S13 lifestyle/coherence/narrative protections still pass
* LC-S14 direction-aware scoring protections still pass
* LC-S16/17/19 DTO/KB surfacing protections still pass
* LC-S18 WHY registration protections still pass
* homocysteine lead finding remains intact

---

# Required Sentinel / test harness obligations

Sentinel update is required.

At minimum add/update defect classes:

```text
persisted_result_schema_incompatible
persisted_result_render_failure
stale_analysis_unmarked
results_page_missing_primary_finding
results_page_placeholder_text_visible
results_page_internal_token_visible
results_page_unit_display_regression
results_page_missing_domain_cards
```

Each must point to an active deterministic regression test, or the strongest available deterministic guard with documented limitation.

Do not add placeholder Sentinel entries.

If the chosen Sentinel Phase 2 structure creates new packs, tests must validate those packs.

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
python -m pytest backend/tests/regression/test_lc_s18_root_cause_why_registration.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

Run new LC-S20/22 tests explicitly, for example:

```powershell
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
```

If frontend test files are changed:

```powershell
npm run type-check
npm run test
```

If Playwright/e2e files are added or changed, run the relevant Playwright command and record exact output.

If any required existing test file name differs, find and run the current equivalent, then record the substitution.

---

# Optional proving harness check

If replay fixtures or result payload compatibility changes could affect launch-core proving output, run:

```powershell
python backend/tools/launch_core_proving_harness.py
```

If only metadata/stamp changes occur, revert or do not commit metadata-only proving artefacts.

If payload fingerprints change, STOP and report before committing unless the change is expected and approved.

---

# Acceptance criteria

This sprint is complete only if:

* persisted replay fixture strategy is established
* stale-result handling policy is documented
* persisted DTO compatibility is deterministically tested
* Sentinel Phase 2 structure decision is documented
* at least one API/render smoke path is guarded
* all required Sentinel defect classes are active or limitations documented
* escaped-defects pack growth is addressed structurally
* prior scaffold/launch-core guards still pass
* no production frontend redesign occurs
* no scoring/unit/Knowledge Bus content work is smuggled into this sprint
* residual risks are documented for LC-S21/23/23B or KB-WAVE phase

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
