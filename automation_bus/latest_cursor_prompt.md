---
work_id: KB-UTIL-2-PROMOTE-PILOT_route_a_single_package_promotion
branch: work/KB-UTIL-2-PROMOTE-PILOT-route-a-single-package-promotion
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# KB-UTIL-2-PROMOTE-PILOT — ROUTE_A Single Package Promotion Pilot

## Purpose

Promote one validated ROUTE_A package from the KB-UTIL-2-PILOT generated artefacts into governed package authority.

This sprint is the first controlled promotion sprint after the deterministic Pass_3 compiler pilot.

The goal is to prove the full governed path for one low-risk exact-match package:

```text
Pass_3 source
→ deterministic compiler output
→ divergence review
→ validator pass
→ package promotion decision
→ legacy package retirement/classification decision
→ no runtime behavioural surprise
````

This is not a bulk migration sprint.

## Non-negotiable architecture rule

Do not bulk promote.

Do not promote more than one package unless explicitly approved during hardening.

The purpose is to prove the controlled promotion harness and divergence policy before scaling to the remaining ROUTE_A cohort.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
KB-MAP-1 merged
KB-UTIL-2-PILOT merged
KNOWLEDGE_BUS_SOP_v1.3.1 committed
KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1 committed
docs/sprints/launch_core_carry_forward_register.md present and updated
knowledge_bus/governance/pass3_legacy_package_mapping_plan_v1.yaml present
knowledge_bus/generated_pilot/kb_util_2_pilot/ present
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
- KB-UTIL-2-PILOT is not merged
- generated pilot artefacts are missing
- carry-forward register is missing
- Pass3 Promotion Protocol v1.1 is missing
```

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint may promote a generated Knowledge Bus package into package authority and may classify or retire one legacy package authority. Even with a low-risk ROUTE_A package, this is medical intelligence promotion work.

## Required governance inputs

Read before implementation:

```text
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md
docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
docs/sprints/launch_core_carry_forward_register.md
docs/audit-papers/KB-UTIL-2-PILOT_pass3_to_runtime_artifact_compiler_pilot_report.md
docs/audit-papers/KB-MAP-1_pass3_to_legacy_package_mapping_and_promotion_plan.md
knowledge_bus/governance/pass3_legacy_package_mapping_plan_v1.yaml
knowledge_bus/governance/pass3_pilot_compile_manifest_index_v1.yaml
knowledge_bus/generated_pilot/kb_util_2_pilot/
```

Also inspect:

```text
backend/scripts/compile_pass3_pilot_artifacts.py
backend/tests/regression/test_kb_util2_pass3_pilot_compiler.py
backend/scripts/validate_knowledge_package.py
backend/scripts/validate_promoted_signal_intelligence.py
knowledge_bus/current/latest_knowledge_status.json
knowledge_bus/packages/
```

If paths differ, locate and report actual paths.

## Advisory points from KB-UTIL-2-PILOT

This sprint must address or formally carry forward both advisory points from KB-UTIL-2-PILOT:

### Advisory 1 — preservation audit path discrepancy

KB-UTIL-2-PILOT found that:

```text
source_field_preservation_audit.yaml recorded:
investigation_spec_contract_version → compile_manifest.yaml#source_contract_version

but compile_manifest.yaml did not contain source_contract_version.
```

Required action:

```text
- Correct the compiler/audit template so the target path is accurate.
- Either add source_contract_version to compile_manifest.yaml,
  or update the audit pointer to the actual preservation location.
- Add/adjust regression test so this cannot recur.
```

### Advisory 2 — generated signal_library schema version

KB-UTIL-2-PILOT generated:

```yaml
schema_version: "2.0.0"
```

while current runtime packages generally use:

```yaml
schema_version: "1.0.0"
```

Required action:

```text
- Determine whether "2.0.0" is intentional and governed.
- If not formally governed, use "1.0.0" for promoted package artefacts until schema advancement is explicitly approved.
- Document the decision in the sprint report.
- Add/adjust regression test so the chosen schema version is deliberate.
```

STOP if promoting with `schema_version: "2.0.0"` would create an unapproved schema migration.

## Package selection

Use only one ROUTE_A package for promotion.

Recommended first candidate:

```text
pkg_s24_creatinine_high_renal
```

Rationale:

```text
- ROUTE_A exact signal match
- single Pass_3 frame
- renal signal with clear primary biomarker
- generated pilot artefacts already exist
- suitable for validating promotion mechanics
```

Alternative only if preflight identifies a blocker:

```text
pkg_s24_ferritin_low_iron_deficiency
```

Do not promote both.

## Required preflight

Before changing package authority, report:

```text
1. selected package_id
2. current legacy package path
3. generated pilot package path
4. source Pass_3 path
5. source spec_id
6. source signal_id
7. source primary biomarker
8. confirmation exact signal_id match
9. confirmation single Pass_3 frame
10. current legacy package schema_version
11. generated package schema_version
12. validator status for generated package
13. promoted_signal_intelligence validator status
14. compile manifest hash evidence
15. source-field preservation audit status
16. behavioural parity/divergence summary
```

STOP if:

```text
- selected package is not ROUTE_A
- selected package has multiple Pass_3 frames
- exact signal_id match is absent
- threshold/activation divergence is clinically meaningful
- generated artefacts fail validation
- source-field preservation audit has unresolved gaps
```

## Divergence policy

Before promotion, classify all differences between current legacy package and generated package.

Use:

```text
NO_DIFFERENCE
STRUCTURAL_ONLY
RICHNESS_GAIN_ONLY
BEHAVIOURAL_DIFFERENCE_LOW
BEHAVIOURAL_DIFFERENCE_HIGH
CLINICAL_ADJUDICATION_REQUIRED
```

Promotion is allowed only if all differences are:

```text
NO_DIFFERENCE
STRUCTURAL_ONLY
RICHNESS_GAIN_ONLY
```

or explicitly accepted with rationale.

STOP if any difference is:

```text
BEHAVIOURAL_DIFFERENCE_HIGH
CLINICAL_ADJUDICATION_REQUIRED
```

Do not resolve clinical divergence in this sprint.

## Promotion method

Preferred safe promotion method:

```text
1. Create a new package directory for the generated package rather than overwriting the legacy package.
2. Preserve the old package unchanged.
3. Use package naming that makes source/version clear.
4. Validate the new package.
5. Update package authority only if governance allows.
```

Suggested package naming:

```text
knowledge_bus/packages/pkg_creatinine_high_renal_pass3_v1/
```

or another repo-consistent name approved by hardening.

Do not overwrite:

```text
knowledge_bus/packages/pkg_s24_creatinine_high_renal/
```

unless hardening explicitly approves overwrite, which should normally be avoided because promoted packages are immutable.

## Required generated/promoted package contents

The promoted package must include:

```text
research_brief.yaml
signal_library.yaml
package_manifest.yaml
promoted_signal_intelligence.yaml
compile_manifest.yaml
source_field_preservation_audit.yaml
```

If existing package validator does not permit extra files, keep additional artefacts inside the package only if accepted by the validator. Otherwise place them in an adjacent governed artefact folder and reference them from the manifest/report.

Do not drop promoted signal intelligence.

Do not flatten Pass_3 richness into signal_library only.

## Runtime status

This sprint may update:

```text
knowledge_bus/current/latest_knowledge_status.json
```

only if the promoted package is intended to become the active package authority under the current Knowledge Bus SOP process.

If updating latest_knowledge_status.json, include validator evidence exactly as required by Knowledge Bus SOP v1.3.1.

If hardening decides runtime activation should wait for a later sprint, do not update latest_knowledge_status.json and instead classify the package as:

```text
compiled_not_promoted
```

## Legacy package treatment

Do not delete the legacy package.

Classify it as one of:

```text
retained_for_traceability
superseded_by_pass3_package
accepted_with_rationale
deferred
```

If the new package is promoted, the old package should be marked in governance/reporting as superseded, not edited in place.

## Validation requirements

Run package validation against the promoted/generated package:

```powershell
python backend/scripts/validate_knowledge_package.py --package-dir <new_package_dir>
```

Run promoted signal intelligence validation if not included automatically:

```powershell
python backend/scripts/validate_promoted_signal_intelligence.py --file <path_to_promoted_signal_intelligence.yaml>
```

Run:

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
python -m pytest backend/tests/regression/test_kb_util2_pass3_pilot_compiler.py -q
```

Add or update regression tests proving:

```text
1. advisory 1 is fixed
2. schema_version decision is deliberate
3. promoted package validates
4. promoted signal intelligence validates
5. legacy package is not overwritten
6. Pass_3 richness is preserved outside signal_library
7. no raw Pass_3 runtime read is introduced
8. no runtime evaluator/frontend code is changed
```

## Runtime boundary

Do not modify:

```text
SignalEvaluator
SignalRegistry
domain_score_assembler
report_compiler
runtime loaders
frontend
SSOT
scoring thresholds
unit conversion
```

If any of those appear necessary, STOP and report.

## Required deliverables

Create:

```text
docs/audit-papers/KB-UTIL-2-PROMOTE-PILOT_route_a_single_package_promotion_report.md
```

Update or create:

```text
knowledge_bus/governance/pass3_promotion_decision_register_v1.yaml
```

Update if needed:

```text
knowledge_bus/governance/pass3_pilot_compile_manifest_index_v1.yaml
docs/sprints/launch_core_carry_forward_register.md
```

## Required report content

The sprint report must include:

```text
- executive verdict
- selected package and rationale
- source Pass_3 spec used
- generated artefacts promoted
- validator results
- promoted signal intelligence validation
- advisory 1 resolution
- advisory 2 schema_version decision
- source-field preservation summary
- behavioural parity/divergence classification
- legacy package treatment
- whether latest_knowledge_status.json was updated
- confirmation no runtime evaluator/frontend changes occurred
- confirmation no manual LLM extraction occurred
- recommended next sprint
```

## Carry-forward register

Before finish, update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Only update items actually changed by this sprint.

Likely relevant items:

```text
CF-KBUTIL1-001
CF-MRIMPROVE-001
CF-CRPPASS3-001
CF-CHRONICINFL-001
```

Do not mark broad migration items resolved from a single-package pilot.

## Out of scope

Do not:

```text
- bulk promote ROUTE_A packages
- promote ROUTE_B/C packages
- promote CRP/systemic inflammation
- resolve multi-frame adjudication
- delete legacy packages
- alter thresholds manually
- change activation logic manually
- change SignalEvaluator or SignalRegistry
- change frontend
- implement root-cause replacement
- implement card evidence runtime consumption
- implement LLM narrative generation
- manually summarise Pass_3 into artefacts
```

## STOP conditions

STOP and report if:

```text
1. selected package has ambiguous mapping
2. selected package has multiple Pass_3 frames
3. package validation fails
4. promoted signal intelligence validation fails
5. advisory 1 cannot be cleanly resolved
6. schema_version choice is unclear
7. behavioural divergence is clinically meaningful
8. promotion would require runtime code changes
9. legacy package would need to be overwritten
10. ARCH-RT validator fails
```

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. governance inputs read
3. selected package and why
4. source Pass_3 spec
5. promoted package path
6. validation commands run
7. validation results
8. advisory 1 resolution
9. advisory 2 decision
10. divergence classification
11. legacy package treatment
12. files changed
13. confirmation no runtime/frontend/evaluator changes
14. confirmation no manual LLM extraction
15. confirmation whether latest_knowledge_status.json changed
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
- current branch matches work/KB-UTIL-2-PROMOTE-PILOT-route-a-single-package-promotion
- only in-scope package/governance/test/report files changed
- no existing legacy package was overwritten
- no runtime evaluator/frontend files changed
- no ambiguous stash exists
- validator evidence is recorded
- advisory points are resolved or explicitly carried forward
```

## Success criteria

This sprint is complete only if:

```text
1. one ROUTE_A package is selected and justified
2. advisory 1 is resolved
3. schema_version decision is made and tested
4. generated/promoted package validates
5. promoted signal intelligence validates
6. legacy package is preserved
7. divergence policy is applied
8. no runtime evaluator/frontend behaviour changes
9. no manual LLM extraction is used
10. next promotion wave can be planned from evidence
```

```
```
