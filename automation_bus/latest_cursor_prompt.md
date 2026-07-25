---
work_id: ARCH-GOV-BASELINE-1
branch: feature/arch-gov-baseline-1-programme-baseline-governance-reset
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-GOV-BASELINE-1 — Programme Baseline and Governance Reset

## 1. Purpose

Create one trustworthy, mechanically usable programme baseline from which all later HealthIQ AI sprint planning can proceed.

This work package must reconcile the current governance authority stack, publish the verified codebase maturity baseline, repair stale audit/test expectations, close narrow CI-enforcement gaps, and record recent governance exceptions honestly.

This is not a product-feature sprint.

This sprint must not:

- introduce new medical reasoning;
- alter clinical thresholds;
- activate PSI;
- change signal firing;
- change root-cause selection;
- change card-evidence medical content;
- change prose selection;
- change Gemini authority;
- select or author the next implementation sprint.

The intended outcome is:

> Future agents can identify the authoritative governance documents, understand the actual current build maturity, and rely on green tests and CI signals without inheriting stale programme claims.

---

## 2. Mandatory governance model

This work package is governed by the full Automation Bus lifecycle.

Required sequence:

1. Confirm branch alignment and clean repository state.
2. Complete authority and reality preflight.
3. Harden this prompt through Claude Code.
4. Run kernel start.
5. Implement only the authorised scope.
6. Complete post-implementation closure protocol.
7. Run kernel finish and deterministic gate.
8. Produce independent audit evidence.
9. Do not merge without explicit human authority.

The standard hardening invocation is:

> **harden work_id: ARCH-GOV-BASELINE-1 — verify source content and produce evidence checklist**

---

## 3. Authoritative audit inputs

Read every file listed below in full before changing anything.

### Independent repository audits

```text
docs/audit-papers/CURSOR_sprint_governance_and_codebase_maturity_audit.md
docs/audit-papers/CLAUDE_CODE_sprint_governance_and_codebase_maturity_audit.md
docs/audit-papers/CURSOR_executable_codebase_and_runtime_reality_audit.md
docs/audit-papers/CLAUDE_CODE_independent_executable_architecture_assurance_audit.md
```

### Current governance and continuity documents

```text
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md
docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
docs/governance/healthiq_pre_sop_prompt_scoping_workflow_v0_6.2.md
docs/AUTHORITY_MAP.md
docs/SPRINT_STATUS.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
```

### MR-BATCH-001B continuity documents

```text
docs/sprints/beta_readiness/MR-BATCH-001B_test_import_completion.md
docs/sprints/beta_readiness/MR-BATCH-001B_candidate_prose_test_output.md
docs/sprints/beta_readiness/MR-BATCH-001B_candidate_prose_assets.yaml
```

### Current test and CI evidence

Locate and read the current repository versions of:

```text
backend/tests/unit/test_arch_rt5d_package_provenance.py
backend/tests/unit/test_golden_panel_runner.py
backend/tests/unit/test_wave1_liver_marker_mapping_fix.py
.github/workflows/architecture-gate.yml
.github/workflows/ci.yml
.github/workflows/golden_gate.yml
backend/scripts/run_architecture_validation_gate.py
backend/scripts/validate_day_one_architecture.py
backend/scripts/validate_day_one_launch_estate_gate.py
backend/scripts/golden_gate_local.py
```

Do not assume paths from this prompt are correct if the repository has moved them. Resolve actual paths and record any path correction in the implementation report.

---

## 4. Stage 1A — Authority preflight

Before modifying files, verify and report:

1. The authoritative current Automation Bus SOP path.
2. The authoritative current Knowledge Bus SOP path.
3. The status and authority level of the Pass 3 promotion protocol.
4. The authoritative pre-SOP scoping workflow path and version.
5. The current programme continuity register.
6. The current day-one architecture carry-forward document.
7. Whether `docs/AUTHORITY_MAP.md` contains:
   - an obsolete Knowledge Bus SOP reference;
   - a stale or non-existent pre-SOP workflow reference;
   - missing Pass 3 promotion protocol entries;
   - duplicate or conflicting current/superseded documents.
8. Whether `docs/SPRINT_STATUS.md` still presents itself as current despite being superseded by later continuity records.
9. Whether both day-one FINAL variants exist and which one is current.
10. Whether any other file outside the proposed scope duplicates the same authority function.

Produce a pre-change authority table in the sprint implementation report.

### Authority rule

This sprint may correct references and classifications.

It must not create a new parallel authority document where an existing document can be corrected or explicitly superseded.

---

## 5. Stage 1B — Reality check

Confirm that the defects still exist on the current branch before implementation.

At minimum verify:

- `docs/AUTHORITY_MAP.md` remains stale or internally conflicting;
- the Pass 3 protocol remains marked DRAFT;
- `docs/SPRINT_STATUS.md` remains stale;
- MR-BATCH-001B completion/output papers still conflict with the latest benchmark-only classification;
- `automation_bus/latest_*` remains stale relative to HEAD;
- `knowledge_bus/current/latest_knowledge_status.json` is absent or otherwise inconsistent with documented expectations;
- RT-5D provenance tests still contain stale inventory expectations;
- golden-panel tests still contain obsolete mock signatures or equivalent stale assumptions;
- `golden_gate.yml` does not provide the intended `main`/`develop` push coverage;
- bilirubin/`total_bilirubin` regression protection still passes on the current baseline;
- architecture and launch-estate gates pass before changes.

If a claimed defect no longer exists, do not recreate it. Re-scope that item out and record the evidence.

If the authority structure differs materially from the audit baseline, STOP and escalate before editing.

---

## 6. Required deliverables

### Deliverable A — Authoritative current-state baseline

Create:

```text
docs/architecture/HEALTHIQ_AI_CURRENT_STATE_BASELINE_2026-07-25.md
```

The baseline must state verified current reality, not historical aspiration.

It must include:

1. Repository baseline:
   - branch;
   - HEAD used for verification;
   - audit date;
   - source audits.
2. Authoritative governance stack.
3. Current programme continuity stack.
4. Current production authorities.
5. Current maturity by the eight beta-readiness blocks.
6. Verified delivered capabilities.
7. Documented-but-undelivered capabilities.
8. Built-but-unwired capabilities.
9. Test-only and candidate-only assets.
10. Active blockers before controlled beta.
11. Explicit supersession notes for stale maturity claims.
12. A statement that this document is the authoritative maturity baseline for future Stage 0 planning until superseded by a later approved baseline.

It must explicitly record:

- six Wave 1 domains are built and wired;
- compiled card evidence is active authority;
- hard-coded card evidence is not active;
- activation-key identity is active;
- end-to-end multi-frame preservation is incomplete;
- package manifests have zero explicit `source_spec_id` across the scanned estate at the audited baseline;
- PSI is built but intentionally unwired;
- WHY authority is dual;
- production prose exists but frame routing and modifier binding are not delivered;
- MR-BATCH-001B is benchmark/test-only and not medically approved or promotable;
- Gemini is non-authoritative;
- controlled beta is not yet authorised.

Do not invent completion percentages.

### Deliverable B — Governance authority reconciliation

Update `docs/AUTHORITY_MAP.md` so it accurately identifies:

- Automation Bus SOP v1.3.1;
- Knowledge Bus SOP v1.3.1;
- Pass 3 promotion protocol v1.1 with its true current status;
- pre-SOP workflow v0.6.2;
- BUILD_DELIVERABLE_REGISTER as lightweight continuity only;
- the new current-state baseline;
- the updated day-one plan;
- audit papers as evidence, not ongoing authority;
- legacy and superseded governance locations.

Remove or correct dangling and obsolete references.

Do not silently change the Pass 3 protocol from DRAFT to APPROVED.

If formal approval authority is not evidenced, retain DRAFT and state that it is an operative companion pending governance ratification.

### Deliverable C — Stale continuity-document handling

Handle `docs/SPRINT_STATUS.md` without deleting history.

Preferred approach:

- add a clear superseded/stale banner at the top;
- identify the current continuity register and current-state baseline;
- preserve historical content below the banner.

Do not rewrite historical sprint records as though they were authored today.

### Deliverable D — MR-BATCH-001B authority correction

Update:

```text
docs/sprints/beta_readiness/MR-BATCH-001B_test_import_completion.md
docs/sprints/beta_readiness/MR-BATCH-001B_candidate_prose_test_output.md
```

Add clear supersession/continuity notes stating:

- Round 1 benchmark/test fixture only;
- not medically approved;
- not for promotion;
- not for production runtime;
- must not proceed to medical review as a promotion route;
- useful only as evidence for future Round 2 prose pipeline design.

Do not alter the candidate prose assets themselves.

### Deliverable E — Historical governance-exception record

Create:

```text
docs/audit-papers/ARCH-GOV-BASELINE-1_historical_governance_exception_record.md
```

Record, without fabricating retrospective hardening:

- P3-PROSE-DEPTH-1A lacks a demonstrated full Automation Bus lifecycle trail;
- MR-BATCH-001B lacks a demonstrated full Automation Bus lifecycle trail;
- MR-BATCH-001B touched `backend/tests/`, so the `/docs/`-only bypass does not clearly apply;
- the content-level risk was limited by isolation from production paths;
- the work remains accepted as historical repository state unless a specific defect is found;
- future work must not use this exception as precedent for bypassing governance.

This document must not claim that hardening occurred retrospectively.

### Deliverable F — Test and inventory refresh

Update stale, deterministic test expectations to current repository reality.

At minimum address:

- current package/provenance row count;
- current compiled card count;
- current kb52c or equivalent package classification count;
- obsolete golden-panel mock signatures;
- any other directly related stale expectation exposed while fixing these failures.

Rules:

- derive expected inventory from the current authoritative inventory contract where possible;
- do not weaken tests merely to make them pass;
- do not replace exact invariant tests with vague assertions;
- do not modify production behaviour to satisfy stale tests;
- distinguish stable invariants from inherently changing estate counts;
- where exact counts are intentionally retained, document the authority source for those counts.

### Deliverable G — CI enforcement correction

Review `.github/workflows/golden_gate.yml`.

Ensure the intended golden/enforcement suite is triggered for the normal protected development flow, including `main` and `develop` where appropriate.

Do not duplicate an existing CI job unnecessarily.

If adding direct push coverage would create redundant or conflicting workflows, STOP and propose a single consolidated correction rather than layering another job.

Preserve NO-LLM enforcement for deterministic golden paths.

### Deliverable H — Narrow unresolved verification closure

Run and record:

- bilirubin/`total_bilirubin` regression test;
- relevant replay/auditability tests or validators already present;
- architecture validation gate;
- launch estate gate;
- refreshed provenance tests;
- refreshed golden-panel tests;
- MR-BATCH isolation tests;
- PSI isolation tests;
- relevant frontend tests if CI workflow changes affect them.

If replay/auditability cannot be fully verified using existing tests, record the exact remaining unknown in the baseline. Do not invent a new replay subsystem in this sprint.

### Deliverable I — Build-register continuity entry

Append one concise entry to:

```text
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

The entry must record:

- the work package outcome;
- the files changed;
- gates/tests run;
- unresolved carry-forwards;
- that no product capability or medical content was added;
- that future Stage 0 planning must start from the new current-state baseline.

The register remains lightweight continuity only.

---

## 7. Allowed implementation scope

Expected scope is limited to:

```text
docs/AUTHORITY_MAP.md
docs/SPRINT_STATUS.md
docs/architecture/HEALTHIQ_AI_CURRENT_STATE_BASELINE_2026-07-25.md
docs/audit-papers/ARCH-GOV-BASELINE-1_historical_governance_exception_record.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
docs/sprints/beta_readiness/MR-BATCH-001B_test_import_completion.md
docs/sprints/beta_readiness/MR-BATCH-001B_candidate_prose_test_output.md
backend/tests/unit/test_arch_rt5d_package_provenance.py
backend/tests/unit/test_golden_panel_runner.py
.github/workflows/golden_gate.yml
```

Additional directly related test or documentation files may be changed only if repository reality proves they are required to complete the stated outcome.

Any expansion beyond governance documentation, tests, and CI configuration requires STOP and escalation.

---

## 8. Forbidden scope

Do not modify:

```text
backend/core/
backend/ssot/
backend/app/
knowledge_bus/packages/
knowledge_bus/compiled/
knowledge_bus/root_cause/
knowledge_bus/pathway_explainers_v1/
knowledge_bus/functional_explainers_v1/
frontend/app/
```

Do not modify:

- signal activation logic;
- thresholds;
- scoring;
- card content;
- root-cause content;
- prose content;
- package manifests;
- compiled artefacts;
- Gemini runtime policy;
- PSI loader or consumers;
- Automation Bus execution scripts;
- Knowledge Bus validator behaviour;
- evidence artefacts produced by prior work packages.

Do not regenerate governed intelligence artefacts.

---

## 9. Required implementation method

### Phase 1 — Evidence capture

Before changes, capture:

```powershell
git branch --show-current
git status --short
git log --oneline -n 20
python backend/scripts/validate_day_one_architecture.py
python backend/scripts/validate_day_one_launch_estate_gate.py
python backend/scripts/run_architecture_validation_gate.py
```

Run the failing targeted tests and preserve their before-state output.

### Phase 2 — Authority and baseline update

Complete Deliverables A–E.

Do not change tests or CI until the authoritative baseline and document classifications are drafted from verified evidence.

### Phase 3 — Test and CI repair

Complete Deliverables F–H.

### Phase 4 — Continuity and final evidence

Complete Deliverable I, rerun all required validation, and prepare closure evidence.

---

## 10. Required test commands

Use repository-supported commands and environment conventions.

At minimum run the repository-equivalent of:

```powershell
$env:PYTHONPATH = "backend"
$env:HEALTHIQ_MODE = "test"

python backend/scripts/validate_day_one_architecture.py
python backend/scripts/validate_day_one_launch_estate_gate.py
python backend/scripts/run_architecture_validation_gate.py

pytest backend/tests/unit/test_arch_rt5d_package_provenance.py -q
pytest backend/tests/unit/test_golden_panel_runner.py -q
pytest backend/tests/unit/test_wave1_liver_marker_mapping_fix.py -q
pytest backend/tests -k "mr_batch_001b or arch_rt5e" -q
```

Also run any workflow-specific tests needed to prove the CI change is syntactically valid and non-duplicative.

Do not update snapshots or governed artefacts to manufacture a pass.

---

## 11. Acceptance criteria

The sprint is complete only when all applicable criteria pass.

### Governance authority

- [ ] `docs/AUTHORITY_MAP.md` points to the correct current governance documents.
- [ ] No non-existent pre-SOP file is presented as authoritative.
- [ ] Knowledge Bus SOP v1.3.1 is correctly classified.
- [ ] Pass 3 protocol v1.1 retains an honest status.
- [ ] `docs/SPRINT_STATUS.md` is clearly marked superseded/stale.
- [ ] Historical audit papers are classified as evidence, not authority.

### Current-state baseline

- [ ] The new baseline exists.
- [ ] Every major maturity claim is supported by the independent audits or current execution evidence.
- [ ] Stale strategy claims are explicitly superseded.
- [ ] No unsupported percentage is used.
- [ ] Future Stage 0 planning is directed to the baseline.

### MR-BATCH-001B

- [ ] Completion/output documents cannot reasonably be read as authorising medical review or promotion.
- [ ] Candidate assets remain unchanged.
- [ ] Isolation tests pass.

### Governance exception

- [ ] Missing historical lifecycle evidence is recorded honestly.
- [ ] No retrospective hardening is fabricated.
- [ ] The exception is explicitly non-precedential.

### Tests and CI

- [ ] RT-5D provenance tests pass against current authorised inventory.
- [ ] Golden-panel tests pass with current production signatures.
- [ ] Bilirubin regression test passes.
- [ ] PSI isolation tests pass.
- [ ] Architecture validation gate passes.
- [ ] Launch-estate gate passes.
- [ ] Golden/enforcement workflow covers the intended protected development flow without unnecessary duplication.
- [ ] NO-LLM deterministic enforcement remains intact.

### Scope integrity

- [ ] No product runtime code changed.
- [ ] No medical content changed.
- [ ] No governed package or compiled artefact changed.
- [ ] No PSI or Gemini activation occurred.
- [ ] No next sprint was selected or authored.

---

## 12. STOP conditions

STOP immediately and report evidence if:

1. Current repository authority differs materially from the two independent audits.
2. Fixing stale tests requires changing production runtime behaviour.
3. Correcting provenance tests requires modifying package manifests or compiled artefacts.
4. Golden-panel failures expose a real production defect rather than stale test mocks.
5. Bilirubin regression protection fails.
6. Architecture or launch-estate gates fail before implementation for a reason unrelated to known stale tests.
7. CI correction would duplicate or conflict with an existing protected-branch workflow.
8. Any required change touches Intelligence Core or medical-content paths.
9. Pass 3 protocol status cannot be represented honestly without a human governance decision.
10. A governance document appears legally or clinically authoritative beyond the evidence available.
11. Any unrelated working-tree changes or tooling-file leakage are present.
12. The sprint would need to select or implement one of the later architecture packages.

---

## 13. Required implementation report

Create:

```text
docs/audit-papers/ARCH-GOV-BASELINE-1_implementation_and_verification_report.md
```

Include:

1. Executive outcome.
2. Pre-change authority table.
3. Reality-check results.
4. Files changed.
5. Exact changes by deliverable.
6. Before/after failing-test evidence.
7. CI trigger comparison.
8. Commands executed and exit codes.
9. Acceptance-criteria table.
10. STOP-condition assessment.
11. Remaining unknowns.
12. Carry-forwards for later Stage 0 planning.
13. Confirmation that no product runtime or medical content changed.

---

## 14. Closure requirements

Before `finish`, execute the mandatory Post-Implementation Closure Protocol from the Automation Bus SOP.

At minimum report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
git diff --name-only
git diff --cached --name-only
git stash list
```

Classify all modified, staged, untracked, tooling, and out-of-scope files.

Do not use stash as routine closure convenience.

Do not run `finish` until:

- the current branch matches the prompt;
- all changes are in scope;
- all required tests pass;
- the working tree is closure-ready;
- no tooling files are leaking into scope;
- no unrelated audit files remain unclassified.

After successful `finish`, handle the kernel-generated COMPLETE status exactly as required by the SOP and confirm the branch is clean.

Do not merge without explicit human authority.
