---
work_id: ARCH-RT-6_day_one_architecture_guardrails_and_acceptance_gate
branch: work/ARCH-RT-6-day-one-architecture-guardrails-and-acceptance-gate
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-RT-6 — Day-One Architecture Guardrails and Acceptance Gate

## Purpose

Finalise the HealthIQ day-one architecture rework by implementing programmatic guardrails and producing final acceptance evidence.

This sprint must prove that the architecture is not just documented, but mechanically enforced.

The target is:

```text
canonical research authority
→ deterministic compile / translation
→ governed runtime artefacts
→ runtime loaders
→ structured DTOs
→ frontend render-only
→ programmatic guardrails preventing drift
````

This sprint must not add new product features.
It must enforce the architecture already delivered by the ARCH-RT programme.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
WAVE1-EQUIV1_total_bilirubin_false_missing_fix — merged
ARCH-RT-0_inventory_and_identity_decisions — merged
ARCH-RT-1_contracts_and_compile_foundation — merged
ARCH-RT-2_identity_runtime_pilot — merged
ARCH-RT-3_card_evidence_vertical_slice — merged
ARCH-RT-4_compiled_hypothesis_root_cause_slice — merged
ARCH-RT-5_full_regeneration_and_launch_gate — merged
ARCH-RT-5B_card_evidence_estate_and_required_provenance — merged
ARCH-RT-5C_hypothesis_runtime_promotion — merged
ARCH-RT-5D_package_provenance_backfill — merged
ARCH-RT-5E_psi_runtime_wiring_decision — merged
```

Before creating or switching to the sprint branch, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 16
git rev-parse HEAD
git rev-parse origin/main
```

STOP if:

* current branch is not `main`
* local `main` does not equal `origin/main`
* working tree is not clean
* ARCH-RT-5E is not merged
* untracked or uncommitted files are present

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint may add permanent architecture tests, validators, Sentinel guard packs, launch-gate enforcement scripts and final authority manifests. These are control-plane / governance enforcement surfaces and must be treated as HIGH risk.

## Standard rules

This work remains governed by the standard Knowledge Bus and Automation Bus SOPs already active in the repository.

Do not re-read SOPs unless the applicable governance requirement cannot be located.

## Authoritative inputs

Read these sprint-specific files before making changes:

```text
docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md
docs/audit-papers/active_intelligence_authority_manifest.md
docs/audit-papers/day_one_architecture_launch_readiness_audit.md
docs/audit-papers/research_to_runtime_traceability_audit.md
docs/audit-papers/ARCH-RT-5B_card_evidence_estate_audit.md
docs/audit-papers/ARCH-RT-5C_hypothesis_runtime_promotion_audit.md
docs/audit-papers/ARCH-RT-5D_package_provenance_backfill_audit.md
docs/audit-papers/ARCH-RT-5E_psi_runtime_wiring_decision_audit.md
docs/audit-papers/ARCH-RT-5D_unresolved_provenance_register.md
docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/architecture/ADR-RT-002_signal_spec_identity_and_registry_policy.md
docs/architecture/compiled_hypothesis_presentation_mapping.md
docs/architecture/card_evidence_role_translation_policy.md
docs/architecture/card_visibility_tier_policy.md
knowledge_bus/compiled/estate_index_v1.yaml
knowledge_bus/schema/compile_manifest_schema_v1.yaml
```

Inspect as implementation authority:

```text
backend/core/knowledge/health_system_card_evidence.py
backend/core/knowledge/compiled_hypothesis.py
backend/core/analytics/root_cause_compiler_v1.py
backend/core/analytics/wave1_subsystem_evidence.py
backend/core/analytics/signal_evaluator.py
backend/scripts/validate_compile_manifest.py
backend/core/knowledge/package_provenance_scan_v1.py
```

STOP if any required authority file is missing.

## Mandatory architectural rules to enforce

This sprint must implement programmatic enforcement for the following rules.

### Card evidence rules

```text
1. All Wave 1 Health Systems Card subsystems must be classified.
2. All launch-active Wave 1 card subsystems must use compiled card evidence.
3. Hard-coded Wave 1 card evidence must not become active again for compiled subsystems.
4. Compiled card evidence artefacts must have resolving compile_manifest_ref values.
5. total_bilirubin must not be reintroduced as an independent required marker where bilirubin is canonical.
6. Frontend must not infer marker roles or clinical meaning.
7. Raw internal source_trace strings must not be rendered directly to consumers.
```

### Root-cause / hypothesis rules

```text
8. signal_vitamin_d_low must use the compiled promoted hypothesis path.
9. Promoted compiled hypotheses must require summary_template.
10. Promoted compiled hypotheses must not use physiological_claim as runtime summary text.
11. Root-cause YAML must not be used for signals classified as compiled-promoted.
12. Multi-frame root-cause promotion must remain blocked unless explicit frame-selection policy exists.
```

### Signal identity rules

```text
13. Duplicate signal_id must not silently collapse.
14. activation_key must remain available for runtime activation-frame identity.
15. Duplicate activation_key must fail closed.
```

### Provenance / manifest rules

```text
16. No package may be unclassified by provenance status.
17. Inferred source_spec_id must not be treated as explicit provenance.
18. kb52c / batch JSON packages must remain classified unless explicitly extracted.
19. compile_run_id must equal compile_id when both exist.
20. Launch-active compile manifests must resolve and must not contain pending_inventory_refresh hashes.
```

### PSI rules

```text
21. PSI remains signal-layer semantics only.
22. PSI must not be used as hypothesis/root-cause authority.
23. PSI must not be used as Health Systems Card evidence authority.
24. PSI must not be imported into launch-critical runtime paths unless explicitly reclassified.
```

### Runtime research-read rules

```text
25. Raw investigation specs must not be read at runtime.
26. Runtime must consume governed compiled artefacts/loaders, not raw research files.
```

## Scope

Allowed scope:

1. Add permanent architecture guardrail tests.
2. Add or update a permanent architecture validation script.
3. Add Sentinel guard pack or equivalent repository-level guard definitions if Sentinel structure exists.
4. Add launch acceptance audit.
5. Refresh active authority manifest if required.
6. Add fail-closed checks only where needed to prevent accidental legacy reuse.
7. Preserve all existing runtime behaviour unless a guard is enforcing already-approved architecture.
8. Add tests for architectural drift prevention.

## Required deliverables

Create or update:

```text
backend/tests/architecture/test_day_one_architecture_guardrails.py
backend/scripts/validate_day_one_architecture.py
docs/audit-papers/ARCH-RT-6_day_one_architecture_acceptance_audit.md
docs/architecture/ARCH-RT-6_day_one_architecture_guardrails_report.md
docs/audit-papers/active_intelligence_authority_manifest.md
docs/audit-papers/day_one_architecture_launch_readiness_audit.md
```

If the repository has an established Sentinel pack location, create or update:

```text
sentinel/packs/day_one_architecture_guardrails.yaml
```

If no Sentinel pack structure exists, STOP and report the correct guardrail integration point before creating a new convention.

## Guardrail implementation requirements

### `backend/scripts/validate_day_one_architecture.py`

Must provide a deterministic validation command that checks, at minimum:

* Wave 1 compiled card estate coverage
* card artefact manifest refs resolve
* no pending manifest hashes for launch-active artefacts
* no forbidden `total_bilirubin` marker in compiled card artefacts
* vitamin D compiled hypothesis runtime promotion status
* promoted compiled hypotheses have `summary_template`
* package provenance scan has no unclassified package
* PSI is not imported by launch-critical runtime modules
* frontend does not contain marker-role inference patterns
* raw investigation spec runtime reads are absent from launch-critical runtime modules
* active authority manifest exists and references current classifications

The script must fail non-zero on guardrail violation.

It must not mutate files.

### `backend/tests/architecture/test_day_one_architecture_guardrails.py`

Must test the validator and/or directly test the same guardrails.

Tests must be stable and not overly brittle.

### Sentinel guard pack

If Sentinel pack structure exists, the pack must reference or mirror the validator checks.

The intended rule is:

```text
If a future change violates the day-one architecture, Sentinel must fail before merge.
```

## Launch-critical runtime modules to inspect

At minimum, inspect:

```text
backend/core/knowledge/health_system_card_evidence.py
backend/core/knowledge/compiled_hypothesis.py
backend/core/knowledge/load_promoted_signal_intelligence.py
backend/core/analytics/root_cause_compiler_v1.py
backend/core/analytics/wave1_subsystem_evidence.py
backend/core/analytics/signal_evaluator.py
backend/core/analytics/report_compiler_v1.py
backend/core/pipeline/orchestrator.py
backend/core/pipeline/orchestrator_phases_v1.py
frontend/app/components/results/Wave1SubsystemEvidenceSection.tsx
frontend/app/types/analysis.ts
```

If paths differ, locate and report the actual paths.

## Out of scope

Do not:

* add new card evidence content
* change clinical thresholds
* change scoring rails
* change biomarker SSOT
* change unit conversion
* change package clinical content
* change investigation specs
* implement PSI runtime wiring
* promote additional root-cause pathways
* alter SignalRegistry identity policy
* alter SignalEvaluator behaviour
* alter frontend design beyond guard/test needs
* add fallback parsers
* make broad runtime behaviour changes not required for enforcement

## STOP conditions

STOP and report if:

1. required authority files are missing
2. Sentinel structure cannot be located and no approved integration point exists
3. guardrails require broad runtime refactoring
4. validator cannot detect key architecture drift programmatically
5. any launch-active authority remains ambiguous
6. tests would need to rely only on documentation rather than repo state
7. raw investigation spec runtime reads are found and cannot be resolved/classified
8. frontend inference patterns are found and cannot be safely resolved
9. package provenance classification is incomplete
10. any guard would produce unstable false positives without a better implementation path

## Required reports

Create:

```text
docs/architecture/ARCH-RT-6_day_one_architecture_guardrails_report.md
```

Must include:

* guardrails implemented
* files checked by validator
* Sentinel integration status
* tests added
* any guardrails deferred and why
* remaining launch risks
* final recommendation

Create:

```text
docs/audit-papers/ARCH-RT-6_day_one_architecture_acceptance_audit.md
```

Must classify final state as one of:

```text
accepted_for_wave1_launch
accepted_with_deferred_non_launch_blockers
launch_blocked
```

No ambiguous final status is allowed.

## Required tests

At minimum:

```text
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
python backend/scripts/validate_day_one_architecture.py
```

Also run targeted regression tests for prior protected behaviours:

```text
backend/tests/unit/test_health_system_card_evidence_arch_rt5b.py
backend/tests/unit/test_compiled_hypothesis_arch_rt5c.py
backend/tests/unit/test_arch_rt5d_package_provenance.py
backend/tests/unit/test_arch_rt5e_psi_runtime_wiring_decision.py
```

Run narrower equivalent paths if names differ.

## Evidence required from Cursor

Cursor must report:

1. baseline branch/status/HEAD evidence
2. authority preflight findings
3. Sentinel integration point found or not found
4. guardrails implemented
5. files changed
6. validator command output
7. tests run
8. test results
9. final acceptance classification
10. confirmation that guardrails are programmatic, not just documentation
11. confirmation no broad runtime/product behaviour change was introduced
12. confirmation prior ARCH-RT protections remain intact

## Closure requirements

Before `run_work_package.py finish`, complete the Automation Bus post-implementation closure protocol.

Run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
git diff --name-only
git diff --cached --name-only
git stash list
```

Classify:

* tracked modified files
* staged files
* untracked files
* tooling files
* out-of-scope files
* stash entries

Do not run finish unless:

* current branch matches `work/ARCH-RT-6-day-one-architecture-guardrails-and-acceptance-gate`
* all changed files are tied to guardrail/acceptance scope
* no ambiguous stash exists
* validator passes
* architecture guardrail tests pass
* final acceptance classification is explicit
* latest commit contains only in-scope work

## Success criteria

This sprint is complete only if:

1. day-one architecture guardrails are enforced programmatically
2. validator exists and fails on drift
3. architecture guardrail tests exist and pass
4. Sentinel integration exists or the correct integration gap is explicitly reported
5. final acceptance audit exists
6. active authority manifest and launch readiness audit are current
7. raw investigation spec runtime reads are guarded against
8. frontend clinical inference is guarded against
9. legacy authority reuse is guarded against
10. PSI misuse is guarded against
11. package provenance drift is guarded against
12. compile manifest drift is guarded against
13. prior ARCH-RT protections remain intact
14. Automation Bus gate passes

```
```
