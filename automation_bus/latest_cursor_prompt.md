---
work_id: ARCH-RT-5C_hypothesis_runtime_promotion
branch: work/ARCH-RT-5C-hypothesis-runtime-promotion
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-RT-5C — Hypothesis Runtime Promotion

## Purpose

Promote the compiled hypothesis architecture from shadow-only pilot into a governed runtime path for one carefully selected root-cause pathway, while preserving legacy YAML fallback and proving presentation-safe summary behaviour.

This sprint must resolve the key ARCH-RT-4 / ARCH-RT-5 carry-forward:

```text
compiled hypothesis artefact
→ compiled hypothesis loader
→ governed presentation mapping
→ root-cause runtime output
→ shadow comparison / regression evidence
````

This sprint must not migrate the full root-cause estate.

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
```

Before creating or switching to the sprint branch, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 12
git rev-parse HEAD
git rev-parse origin/main
```

STOP if:

* current branch is not `main`
* local `main` does not equal `origin/main`
* working tree is not clean
* ARCH-RT-5B is not merged
* untracked or uncommitted files are present

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint may touch root-cause compiler/runtime WHY output, compiled hypothesis loaders, contracts, DTO-adjacent output, tests and audit artefacts. It affects user-facing interpretation and is therefore HIGH risk.

HIGH-risk controls apply:

* Claude hardening required before kernel start
* Cursor implementation only after kernel start
* Claude audit after implementation
* GPT architectural review before merge
* dual approval before merge

## Authoritative inputs

Read these files before making changes:

```text
docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md
docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/architecture/ADR-RT-002_signal_spec_identity_and_registry_policy.md
docs/architecture/ADR-RT-003_hypothesis_artefact_and_root_cause_transition.md
docs/architecture/ADR-RT-004_compile_manifest_and_package_provenance_policy.md
docs/architecture/compiled_hypothesis_contract.md
docs/architecture/compiled_hypothesis_presentation_mapping.md
docs/architecture/ARCH-RT-4_compiled_hypothesis_root_cause_slice_report.md
docs/architecture/ARCH-RT-4_root_cause_divergence_report.md
docs/audit-papers/ARCH-RT-5_M3_hypothesis_root_cause_estate_audit.md
docs/audit-papers/day_one_architecture_launch_readiness_audit.md
docs/audit-papers/active_intelligence_authority_manifest.md
docs/architecture/ARCH-RT-5_full_regeneration_and_launch_gate_report.md
docs/architecture/ARCH-RT-5_split_recommendation.md
knowledge_bus/schema/compiled_hypothesis_schema_v1.yaml
knowledge_bus/compiled/hypotheses/signal_vitamin_d_low.yaml
knowledge_bus/compiled/manifests/arch_rt4_vitamin_d_hypothesis.yaml
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
```

STOP if any required authority file is missing.

If the updated sprint plan has a different path, locate it and report the path before proceeding.

## Mandatory inherited decisions and carry-forwards

The following are binding:

```text
ADR-008 is accepted.
PSI remains signal-layer semantics only.
Hypothesis graphs must not be placed into PSI.
ADR-RT-002 selected MULTI_FRAME_PER_DIRECTION.
activation_key is required.
signal_id remains signal-family identity.
Root-cause compiler is not fully multi-frame aware.
```

Carry-forward from ARCH-RT-4 / ARCH-RT-5:

```text
Compiled hypotheses are currently shadow-only.
compile_root_cause_v1() has not yet been wired to consume compiled hypothesis artefacts.
ARCH-RT-5C must decide when and how compiled hypotheses begin influencing runtime RootCauseV1 output.
physiological_claim must not be treated as direct retail/runtime summary text.
summary_template remains the presentation/runtime wording field unless superseded by explicit mapping policy.
Before runtime promotion, compiled hypothesis → RootCauseHypothesisV1 presentation mapping must be enforced.
The compiled hypothesis artefact must carry a presentation-safe summary_template or emit a root-cause-compatible view that preserves runtime summary semantics.
Root-cause compiler remains not fully multi-frame aware.
Multi-frame root-cause selection must be explicitly governed before any multi-frame hypothesis path is promoted.
Strong direct cross-load / fail-closed boundary tests should be added if legacy and compiled loaders remain side-by-side.
compile_manifest_ref must resolve to a real manifest file or governed estate index entry for promoted artefacts.
source_spec_provenance: source_document_derived is acceptable for pilot only and is not canonical explicit provenance.
```

Carry-forward from ARCH-RT-5 GPT review:

```text
runtime_summary_for_hypothesis() fail-safe must fail closed before any compiled hypothesis is promoted.
If summary_template is missing, do not silently degrade to physiological_claim.
physiological_claim must not be used as fallback runtime summary text in promoted output.
```

Do not reopen these decisions.

If repository evidence contradicts any inherited decision, STOP and report.

## Pilot selection

Preferred pilot:

```text
signal_vitamin_d_low
```

Reason:

* compiled hypothesis artefact already exists
* compile manifest exists
* divergence report exists
* single-frame pathway
* legacy YAML remains available
* avoids unresolved multi-frame root-cause selection risk

This sprint should use `signal_vitamin_d_low` unless preflight proves it is unsafe.

STOP if a different pilot appears necessary and report the reason before implementation.

## Authority preflight

Before implementation, verify and report:

1. Current compiled hypothesis schema.
2. Current compiled vitamin D hypothesis artefact.
3. Current compile manifest for vitamin D hypothesis.
4. Current compiled hypothesis loader.
5. Current compiled hypothesis shadow registry.
6. Current root_cause_registry_v1 production registry.
7. Current load_root_cause_hypotheses legacy loader.
8. Current root_cause_compiler_v1 implementation.
9. Current RootCauseHypothesisV1 / RootCauseFindingV1 contracts.
10. Current report/result path consuming root-cause output.
11. Current tests for compiled hypothesis pilot.
12. Current tests for legacy root-cause YAML loader.
13. Current behaviour when summary_template is missing.
14. Current behaviour for root-cause compiler signal_id matching.
15. Whether vitamin D remains single-frame and safe to promote.

If any authority path cannot be verified, STOP and report.

## Mandatory internal checkpoint

Before runtime promotion:

1. Confirm selected pilot artefact validates.
2. Confirm selected pilot compile manifest resolves.
3. Confirm selected pilot has `summary_template`.
4. Confirm runtime mapping uses `summary_template`, not `physiological_claim`.
5. Confirm missing `summary_template` fails closed.
6. Confirm legacy YAML remains available.
7. Confirm divergence is acceptable and already documented.
8. Confirm pilot is single-frame or has explicit frame-selection policy.

If any checkpoint fails, STOP before modifying runtime compiler behaviour.

## Scope

Allowed scope:

1. Harden compiled hypothesis presentation mapping.
2. Make `summary_template` mandatory for promoted runtime use.
3. Ensure `runtime_summary_for_hypothesis()` fails closed if `summary_template` is absent in promoted path.
4. Add or update compiled hypothesis loader / helper functions as needed.
5. Wire exactly one pilot signal into root-cause runtime output through a governed compiled path.
6. Preserve legacy YAML fallback or comparison path.
7. Ensure production registry is not broadly replaced.
8. Add shadow comparison / regression tests.
9. Add direct cross-load / fail-closed boundary tests between legacy and compiled loaders.
10. Produce runtime promotion report and audit evidence.

## Required deliverables

Create or update:

```text
docs/audit-papers/ARCH-RT-5C_hypothesis_runtime_promotion_audit.md
docs/architecture/ARCH-RT-5C_hypothesis_runtime_promotion_report.md
```

Implementation files may be updated only as required for:

```text
compiled hypothesis presentation mapping
compiled hypothesis runtime loader/helper
root-cause compiler pilot routing
root-cause registry pilot selection
targeted tests
```

## Runtime promotion requirements

If the pilot is promoted:

* promotion must be limited to `signal_vitamin_d_low`
* compiled artefact must validate
* compile manifest must resolve
* `summary_template` must exist
* runtime summary must use `summary_template`
* `physiological_claim` must not be emitted as runtime summary text
* missing `summary_template` must fail closed
* legacy YAML must remain available
* non-pilot root-cause pathways must remain unchanged
* no multi-frame signal may be promoted unless explicit frame policy exists

## Root-cause compiler requirements

If `root_cause_compiler_v1.py` is modified:

* change must be pilot-gated
* non-pilot behaviour must remain unchanged
* existing root-cause output contract must remain stable unless explicitly justified
* no global switch from YAML to compiled hypotheses
* no signal-family first-match multi-frame promotion
* no raw investigation spec runtime reads
* no PSI dependency

## Schema requirements

If `compiled_hypothesis_schema_v1.yaml` is updated:

* do not make breaking changes to existing valid pilot artefact unless updated consistently
* mark `summary_template` as required for runtime-promoted hypotheses, or introduce an explicit `promotion_requirements` / `runtime_promotion` rule
* preserve distinction between:

  * physiological_claim
  * summary_template
  * evidence fields
  * provenance fields

## Out of scope

Do not:

* migrate full root-cause estate
* delete or rewrite existing root-cause YAML
* promote multi-frame root-cause pathways
* modify SignalRegistry
* modify SignalEvaluator
* modify PSI artefacts
* implement PSI runtime wiring
* modify card evidence artefacts
* modify card evidence loader
* modify frontend
* modify package files
* modify investigation specs
* modify biomarker SSOT
* change clinical thresholds
* change scoring rails
* change unit conversion
* expose physiological_claim as retail summary text
* introduce fallback parsers
* commit helper scripts

## Required tests

At minimum:

1. Compiled hypothesis artefact still validates.
2. Compile manifest resolves.
3. Runtime promotion path uses `summary_template`.
4. Missing `summary_template` fails closed for promoted runtime use.
5. `physiological_claim` is not emitted as runtime summary.
6. Legacy YAML loader still works.
7. Compiled loader rejects legacy YAML directly.
8. Legacy loader rejects compiled YAML directly or fails closed.
9. Pilot root-cause runtime output matches expected safe summary.
10. Non-pilot root-cause pathways remain unchanged.
11. Multi-frame root-cause promotion is blocked or not in scope.
12. No raw investigation spec runtime reads.

Run narrow tests first. Run broader root-cause/report tests if touched contracts require them.

## STOP conditions

STOP and report if:

1. Required authority files are missing.
2. Vitamin D pilot artefact no longer validates.
3. Vitamin D compile manifest does not resolve.
4. `summary_template` is missing and cannot be safely added from governed/presentation-safe source.
5. Runtime mapping would use `physiological_claim` as summary text.
6. Missing summary_template would silently fall back to physiological_claim.
7. Runtime promotion requires broad root-cause compiler redesign.
8. Runtime promotion requires multi-frame root-cause policy.
9. Runtime promotion requires package/spec/PSI/card/frontend changes.
10. Legacy YAML would no longer be available.
11. Tests cannot prove non-pilot root-cause stability.
12. Scope expands into full root-cause estate migration.

## Required report

Create:

```text
docs/architecture/ARCH-RT-5C_hypothesis_runtime_promotion_report.md
```

The report must include:

* pilot selected and rationale
* artefact path
* manifest path
* runtime mapping decision
* summary_template policy
* physiological_claim boundary
* compiler/registry changes
* legacy YAML preservation evidence
* tests added/updated
* test commands and results
* non-pilot stability evidence
* remaining risks and carry-forwards

Create:

```text
docs/audit-papers/ARCH-RT-5C_hypothesis_runtime_promotion_audit.md
```

The audit must classify:

* pilot promoted or not promoted
* runtime behaviour changed or unchanged
* legacy YAML retained
* summary_template enforced
* physiological_claim blocked from runtime summary
* multi-frame promotion status
* remaining root-cause estate status

## Evidence required from Cursor

Cursor must report:

1. Baseline branch/status/HEAD evidence.
2. Authority preflight findings.
3. Internal checkpoint result.
4. Files changed.
5. Exact runtime promotion mechanism.
6. Exact summary_template enforcement behaviour.
7. Tests added/updated.
8. Test commands run.
9. Test results.
10. Confirmation that legacy YAML remains available.
11. Confirmation that non-pilot root-cause pathways are unchanged.
12. Confirmation that physiological_claim is not runtime summary text.
13. Confirmation that no package/spec/PSI/card/frontend work was included.
14. Confirmation that no helper scripts were committed.

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

* current branch matches `work/ARCH-RT-5C-hypothesis-runtime-promotion`
* all changed files are tied to this sprint
* no package/spec/PSI/card/frontend/SignalRegistry/SignalEvaluator files are changed
* no helper scripts are included
* no ambiguous stash exists
* latest commit contains only in-scope work

## Success criteria

This sprint is complete only if:

1. One compiled hypothesis path is promoted or explicitly classified as not ready.
2. If promoted, runtime output uses `summary_template`.
3. Missing `summary_template` fails closed for promoted output.
4. `physiological_claim` is not used as runtime summary text.
5. Legacy YAML remains available.
6. Non-pilot root-cause pathways remain unchanged.
7. Multi-frame root-cause promotion is not introduced without explicit policy.
8. Tests prove pilot runtime behaviour and legacy preservation.
9. No package/spec/PSI/card/frontend scope is included.
10. Automation Bus gate passes.

```
```
