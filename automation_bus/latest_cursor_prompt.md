---
work_id: P1-14
branch: work/P1-14-staged-psi-hash-repair-and-activation-cohort-lock
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# P1-14 — Staged PSI Hash Repair, Gate Re-run and Activation Cohort Lock

## Objective

Repair staged PSI compile-manifest hash integrity, rerun the activation-readiness gate, and produce the clean activation-readiness cohort map for future production opt-in planning.

This is not a validation-only sprint.

This is an outcome-based remediation sprint with internal STOP gates.

It must:

1. repair the universal staged PSI compile-manifest hash mismatch discovered in P1-13;
2. rerun the P1-13 activation-readiness validator;
3. confirm the true post-hash activation-readiness split;
4. lock the clean staged PSI cohort map;
5. produce next workpacks for activation-ready PSI, biomarker identity blockers, derived-marker blockers, and medical-review blockers.

Promotion is not activation.

This sprint must not make any PSI runtime-active.

## Strategic purpose

P1-10, P1-11 and P1-12 created staged PSI artefacts from Pass 3 research.

P1-13 created the activation-readiness gate and discovered that all 41 staged compile manifests had stale hash values, blocking reliable readiness classification.

P1-14 must remove that mechanical blocker and convert the P1-13 gate into actionable programme sequencing.

Do not split this into a hash-only micro-sprint.

Do not use this sprint to make medical identity decisions.

Do not use this sprint to activate staged PSI.

## Branch and state checks

Start from `main`.

```powershell
git switch main
git pull origin main
git status --short
git rev-parse main
git rev-parse origin/main
```

Confirm:

```text
- current branch is main
- local main == origin/main
- working tree is clean
```

Then create:

```powershell
git switch -c work/P1-14-staged-psi-hash-repair-and-activation-cohort-lock
```

Do not proceed if the working tree is dirty.

Confirm the Automation Bus active work package/state file if required by SOP.

## Required prerequisites on main

These files must exist on `main`:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/sprints/beta_readiness/P1-10_pass3_launch_core_signal_intelligence_batch_a.md
docs/sprints/beta_readiness/P1-10_signal_intelligence_batch_a_manifest.yaml
docs/sprints/beta_readiness/P1-11_pass3_cbc_iron_oxygen_signal_intelligence_batch_b.md
docs/sprints/beta_readiness/P1-11_signal_intelligence_batch_b_manifest.yaml
docs/sprints/beta_readiness/P1-12_pass3_deferred_cbc_iron_hematology_batch_c.md
docs/sprints/beta_readiness/P1-12_signal_intelligence_batch_c_manifest.yaml
docs/sprints/beta_readiness/P1-13_staged_psi_activation_readiness_gate.md
docs/sprints/beta_readiness/P1-13_staged_psi_activation_readiness_manifest.yaml
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
backend/scripts/validate_staged_psi_activation_readiness.py
docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
```

These staged PSI directories must also exist:

```text
knowledge_bus/generated_pilot/p1_10_batch_a/
knowledge_bus/generated_pilot/p1_11_batch_b/
knowledge_bus/generated_pilot/p1_12_batch_c/
```

If any are missing, stop and report:

```text
P1-14 prerequisite staged PSI or activation-readiness evidence is not present on main. P1-14 must not proceed.
```

## First authority documents

Read these first, in this order:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/sprints/beta_readiness/P1-13_staged_psi_activation_readiness_gate.md
docs/sprints/beta_readiness/P1-13_staged_psi_activation_readiness_manifest.yaml
docs/sprints/beta_readiness/P1-10_pass3_launch_core_signal_intelligence_batch_a.md
docs/sprints/beta_readiness/P1-11_pass3_cbc_iron_oxygen_signal_intelligence_batch_b.md
docs/sprints/beta_readiness/P1-12_pass3_deferred_cbc_iron_hematology_batch_c.md
docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md
docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Use the `healthiq-knowledge-bus-medical-intelligence` agent rule if available.

If the agent rule is missing, continue under the approved sprint prompt, but record that the specialist rule was not available.

## Scope

This sprint has four phases.

## Phase 0 — Compile-manifest hash repair

Recompute the SHA-256 hash for every staged `promoted_signal_intelligence.yaml` file under:

```text
knowledge_bus/generated_pilot/p1_10_batch_a/
knowledge_bus/generated_pilot/p1_11_batch_b/
knowledge_bus/generated_pilot/p1_12_batch_c/
```

Update only the corresponding hash values in the matching staged `compile_manifest.yaml` files.

If batch-level compile manifest indexes also contain PSI output hashes, update those hash values only where required.

Do not edit PSI medical content.

Do not edit production package manifests.

Do not edit source packages.

Do not edit Pass 3 source files.

Do not edit validators.

STOP if:

```text
- a PSI file has no matching compile manifest;
- a compile manifest has no matching PSI file;
- the hash field structure is unclear;
- a hash mismatch appears to be caused by missing or corrupted PSI content rather than stale manifest values;
- repairing hashes would require editing PSI content;
- repairing hashes would require production package changes.
```

## Phase 1 — Gate re-run

Run the P1-13 activation-readiness validator against all staged batches.

Expected command shape, adjust only if the script help requires a different syntax:

```powershell
python backend/scripts/validate_staged_psi_activation_readiness.py --staged-root knowledge_bus/generated_pilot --batches p1_10_batch_a p1_11_batch_b p1_12_batch_c
```

If the script uses different arguments, inspect the script help and run the correct equivalent.

STOP if:

```text
- hash mismatches remain after repair;
- validator fails structurally;
- validator reports any staged PSI as runtime-active;
- validator reports production manifest opt-in;
- validator reports unexpected backend/runtime coupling;
- validator output is missing or cannot be trusted.
```

## Phase 2 — Activation-readiness cohort lock

Using the clean validator output, classify the staged PSI estate into programme cohorts:

```text
ACTIVATION_READY_CANDIDATE
BLOCKED_BIOMARKER_IDENTITY
BLOCKED_DERIVED_MARKER_DEPENDENCY
BLOCKED_MEDICAL_REVIEW_REQUIRED
BLOCKED_FRAME_AUTHORITY
BLOCKED_SOURCE_SUPPORT
BLOCKED_SYSTEM_MAPPING
BLOCKED_SCHEMA_OR_VALIDATOR
BLOCKED_MANIFEST_OR_HASH
NOT_ELIGIBLE_FOR_ACTIVATION
```

Expected post-hash baseline from P1-13:

```text
22 activation-ready
9 biomarker-identity blocked
7 derived-marker blocked
3 medical-review blocked
```

Do not force this result. Verify it from the validator output.

If the actual result differs, report the difference and explain why.

## Phase 3 — Next-workpack definition

Create clear follow-on workpacks from the clean cohort map.

At minimum, define:

```text
- first production PSI opt-in pilot candidate cohort;
- SSOT / biomarker identity adjudication cohort;
- derived-marker support cohort;
- medical-review cohort;
- source-support / research-authoring cohort if still needed;
- system-mapping / frame-authority cohort if still needed.
```

Do not implement these workpacks in this sprint.

Do not make production opt-ins.

Do not edit SSOT biomarker keys.

Do not make medical-review decisions.

Do not activate anything.

## Permitted changes

Expected product changes may include:

```text
knowledge_bus/generated_pilot/p1_10_batch_a/**/compile_manifest.yaml
knowledge_bus/generated_pilot/p1_11_batch_b/**/compile_manifest.yaml
knowledge_bus/generated_pilot/p1_12_batch_c/**/compile_manifest.yaml
knowledge_bus/generated_pilot/p1_10_batch_a/*compile_manifest_index*.yaml
knowledge_bus/generated_pilot/p1_11_batch_b/*compile_manifest_index*.yaml
knowledge_bus/generated_pilot/p1_12_batch_c/*compile_manifest_index*.yaml
docs/sprints/beta_readiness/P1-14_staged_psi_hash_repair_and_activation_cohort_lock.md
docs/sprints/beta_readiness/P1-14_activation_readiness_cohort_manifest.yaml
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
automation_bus/
```

Only update index files if they contain hash values requiring synchronisation.

## Prohibited changes

Do not modify:

```text
frontend/
Gemini paths
fallback parser paths
backend/core/
backend/scripts/
backend/tests/
backend/ssot/scoring_policy.yaml
backend/ssot/biomarkers.yaml
runtime DTO contracts
domain assemblers
narrative assemblers
compiled runtime cards
production package manifests
Pass 3 source files
investigation-spec source files
Knowledge Bus source package files
staged promoted_signal_intelligence.yaml files
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/AUTHORITY_MAP.md
```

Do not change PSI content.

Do not change medical wording.

Do not change signal identifiers.

Do not change biomarker IDs.

Do not change lifecycle status.

Do not change runtime flags except where a stale staged compile manifest hash field is being corrected.

## Required deliverable 1 — Sprint report

Create:

```text
docs/sprints/beta_readiness/P1-14_staged_psi_hash_repair_and_activation_cohort_lock.md
```

Use this structure:

```markdown
# P1-14 — Staged PSI Hash Repair, Gate Re-run and Activation Cohort Lock

## 1. Executive summary
- why this sprint was run
- hash repair outcome
- validator rerun outcome
- final activation-readiness split
- recommended next sprint

## 2. Programme context
- relationship to eight-block beta-readiness
- relationship to P1-10
- relationship to P1-11
- relationship to P1-12
- relationship to P1-13
- why this is not a validation-only micro-sprint
- why this is not runtime activation

## 3. Phase 0 — Hash repair
- staged batches inspected
- PSI files counted
- compile manifests counted
- hash fields repaired
- index files repaired, if any
- STOP conditions checked
- limitations

## 4. Phase 1 — Gate re-run
- validator command run
- validator output summary
- remaining hash issues, if any
- unexpected structural issues, if any
- runtime activation check

## 5. Phase 2 — Activation-readiness cohort lock
Create a table:

| Cohort | Count | Representative PSI files | Blocker / readiness basis | Recommended action |
|---|---:|---|---|---|

Include:
- ACTIVATION_READY_CANDIDATE
- BLOCKED_BIOMARKER_IDENTITY
- BLOCKED_DERIVED_MARKER_DEPENDENCY
- BLOCKED_MEDICAL_REVIEW_REQUIRED
- any other actual class returned by the validator

## 6. Phase 3 — Follow-on workpacks
Define:
- production PSI opt-in pilot workpack
- SSOT / biomarker identity workpack
- derived-marker workpack
- medical-review workpack
- source-support / research-authoring workpack, if needed
- frame-authority / system-mapping workpack, if needed

## 7. Runtime non-activation confirmation
Confirm:
- no staged PSI content changed
- no production package manifests changed
- no runtime activation occurred
- no scoring_policy change
- no biomarkers.yaml change
- no backend/core change
- no frontend/Gemini/parser change
- no DTO/domain assembler change
- no compiled card change
- no Pass 3 source change

## 8. Validation
- YAML parse checks
- validator commands and outputs
- hash verification output
- git diff checks
- limitations

## 9. Business value delivered
Explain:
- why repairing hash integrity matters
- how this turns staged PSI into actionable activation cohorts
- how it avoids micro-sprinting
- how it supports parallel medical/SSOT/codebase planning

## 10. Carry-forwards
Group carry-forwards into:
- activation-ready pilot candidates
- SSOT / biomarker identity decisions
- derived-marker decisions
- medical-review decisions
- source-support / research-authoring decisions
- frame-authority / system-mapping decisions

## 11. Recommended next sprint
Recommend the next sprint with:
- title
- risk_level
- change_type
- scope
- STOP gates
- rationale
```

## Required deliverable 2 — Activation cohort manifest

Create:

```text
docs/sprints/beta_readiness/P1-14_activation_readiness_cohort_manifest.yaml
```

Use this structure:

```yaml
work_id: P1-14
classification_date: <YYYY-MM-DD>
source_authorities:
  - path: <path>
    role: <role>
staged_estate:
  batches_inspected:
    - p1_10_batch_a
    - p1_11_batch_b
    - p1_12_batch_c
  psi_files_found: <number>
  compile_manifests_found: <number>
  hashes_repaired: <number>
  production_opt_ins_found: <number>
summary:
  activation_ready_candidate_count: <number>
  blocked_count: <number>
  blocker_counts:
    biomarker_identity: <number>
    derived_marker_dependency: <number>
    medical_review_required: <number>
    frame_authority: <number>
    source_support: <number>
    system_mapping: <number>
    schema_or_validator: <number>
    manifest_or_hash: <number>
cohorts:
  - cohort: ACTIVATION_READY_CANDIDATE
    count: <number>
    items:
      - psi_path: <path>
        compile_manifest_path: <path>
        primary_metric_biomarker_id: <id>
        recommended_next_action: <short action>
  - cohort: BLOCKED_BIOMARKER_IDENTITY
    count: <number>
    items:
      - psi_path: <path>
        blocker: <blocker>
        recommended_next_action: <short action>
  - cohort: BLOCKED_DERIVED_MARKER_DEPENDENCY
    count: <number>
    items:
      - psi_path: <path>
        blocker: <blocker>
        recommended_next_action: <short action>
  - cohort: BLOCKED_MEDICAL_REVIEW_REQUIRED
    count: <number>
    items:
      - psi_path: <path>
        blocker: <blocker>
        recommended_next_action: <short action>
validation:
  manifest_yaml_parse: pass | fail | not_run
  activation_readiness_validator: pass | fail | partial | not_run
  hash_integrity_after_repair: pass | fail | partial | not_run
  runtime_activation_check: pass | fail | not_run
```

The manifest is a planning and audit artefact.

It must not be consumed by runtime.

## Required deliverable 3 — Build deliverable register update

At closure, update:

```text
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Append a short entry:

```markdown
## P1-14 — Staged PSI hash repair and activation cohort lock

**Status:** Complete / Partial / Blocked  
**Date closed:** <YYYY-MM-DD>  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance; Block 7 Auditability, reproducibility and traceability  

### Delivered / ticked off
- <what this sprint completed against the beta-readiness programme>
- <major hash repair / cohort lock outcome>

### Carry-forwards
- <what still needs to be done later>
- <known gaps exposed by this sprint>

### Blockers / risks
- <only material blockers or risks that affect future work>

### Recommended next sprint
- <next work package recommendation>
```

Keep the entry short.

Do not list every file touched.

Do not duplicate the sprint report.

## Validation

Run:

```powershell
git diff --stat
git diff --name-only
git status --short
```

Validate the P1-14 cohort manifest YAML:

```powershell
python -c "import yaml; from pathlib import Path; p=Path('docs/sprints/beta_readiness/P1-14_activation_readiness_cohort_manifest.yaml'); data=yaml.safe_load(p.read_text(encoding='utf-8')); assert data['work_id']=='P1-14'; assert 'cohorts' in data; print('P1-14 activation cohort manifest YAML parsed successfully')"
```

Run the staged PSI activation-readiness validator after hash repair.

Capture exact command and output.

If the validator supports a machine-readable output file, use it only under `docs/sprints/beta_readiness/` or a clearly non-runtime temporary/report path.

Do not write validator output into runtime paths.

## Runtime non-activation validation

Confirm:

```text
- no staged promoted_signal_intelligence.yaml files changed
- no production package manifests changed
- no backend/core files changed
- no backend/scripts files changed
- no backend/tests files changed
- no backend/ssot/scoring_policy.yaml changed
- no backend/ssot/biomarkers.yaml changed
- no frontend files changed
- no Gemini or fallback parser files changed
- no runtime DTO or assembler files changed
- no compiled cards changed
- no Pass 3 source files changed
- no runtime activation flags changed to true
```

If compile manifests include `runtime_active`, confirm all remain `false`.

## Required final report

Return:

```text
- branch name
- main SHA baseline
- specialist agent availability
- staged batches inspected
- PSI files found
- compile manifests found
- hashes repaired
- validator command and output
- final activation-ready candidate count
- final blocked counts by blocker type
- files changed
- whether any staged PSI content changed
- whether any production package manifests changed
- whether scoring_policy.yaml or biomarkers.yaml changed
- whether backend/core/frontend/runtime files changed
- whether Pass 3 source files changed
- recommended next sprint
- git diff --stat
- git diff --name-only
- git status --short
```

Do not merge until Claude audit, GPT architectural review and human approval.

## Acceptance criteria

This sprint is complete only if:

```text
1. All staged PSI compile-manifest hash mismatches from P1-13 are repaired or explicitly blocked with evidence.

2. No staged PSI content files are modified.

3. No medical content is changed.

4. No biomarker IDs are changed.

5. No production package manifests are changed.

6. No runtime activation occurs.

7. The P1-13 activation-readiness validator is rerun after hash repair.

8. Hash integrity passes after repair, or remaining failures are explicitly explained.

9. The true post-hash activation-readiness cohort split is reported.

10. Activation-ready candidates are listed.

11. Blocked cohorts are grouped by blocker type.

12. Follow-on workpacks are defined without implementing them.

13. No scoring policy or SSOT biomarker file is changed.

14. No backend/core, backend/scripts, backend/tests, frontend, Gemini, parser, DTO, assembler or compiled-card files are changed.

15. No Pass 3 or investigation-spec source file is changed.

16. P1-14 report exists at:
    docs/sprints/beta_readiness/P1-14_staged_psi_hash_repair_and_activation_cohort_lock.md

17. P1-14 cohort manifest exists at:
    docs/sprints/beta_readiness/P1-14_activation_readiness_cohort_manifest.yaml

18. Build deliverable register is updated with a short P1-14 entry.

19. Manifest YAML validation passes.

20. Final report includes validator output, hash-repair result and clean git status.
```
