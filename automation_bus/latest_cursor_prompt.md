---
work_id: KB-MAP-1_pass3_to_legacy_package_mapping_and_promotion_plan
branch: work/KB-MAP-1-pass3-to-legacy-package-mapping-and-promotion-plan
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# KB-MAP-1 — Pass_3 to Legacy Package Mapping and Promotion Plan

## Purpose

Turn the 55 non-Pass_3 / unclear-provenance package audit into a practical promotion plan.

This sprint must not promote, rewrite, delete, or change any runtime package.

The aim is to map each legacy/runtime package to its best available Pass_3 / investigation-spec source and classify the safest future promotion route.

The output should tell us:

```text
- which packages are easy promotion candidates
- which need compiler/promotion pilot testing
- which need manual clinical/architecture review
- which are provenance hygiene issues
- which should be retired
- which must remain deferred
````

This is a planning and classification sprint only.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
CRP-PASS3-MIGRATION merged
MED-RESEARCH-REVIEW-1 merged
KNOWLEDGE_BUS_SOP_v1.3.1 committed
KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1 committed
docs/sprints/launch_core_carry_forward_register.md present and updated
knowledge_bus/governance/non_pass3_package_revalidation_register_v1.yaml present
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
- MED-RESEARCH-REVIEW-1 is not merged
- Knowledge Bus SOP v1.3.1 is missing
- Pass3 Promotion Protocol v1.1 is missing
- non_pass3_package_revalidation_register_v1.yaml is missing
```

## Governance classification

```yaml
risk_level: STANDARD
change_type: CONTENT
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This is a mapping and planning sprint only. It must not change runtime behaviour.

## Required governance inputs

Read before investigation:

```text
KNOWLEDGE_BUS_SOP_v1.3.1.md
KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
docs/sprints/launch_core_carry_forward_register.md
knowledge_bus/governance/non_pass3_package_revalidation_register_v1.yaml
docs/audit-papers/MED-RESEARCH-REVIEW-1_non_pass3_package_revalidation_audit.md
docs/audit-papers/MED-RESEARCH-REVIEW-1_pass3_primary_biomarker_cross_validation_addendum.md
docs/audit-papers/CRP-PASS3-MIGRATION_crp_legacy_s24_package_and_signal_naming_alignment_report.md
docs/audit-papers/CRP-PASS3-MIGRATION_package_provenance_non_pass3_table.md
```

Also inspect:

```text
knowledge_bus/packages/**
knowledge_bus/research/investigation_specs/multi_llm_research/**/*Pass_3*.json
knowledge_bus/research/investigation_specs/**/*.yaml
knowledge_bus/compiled/**
knowledge_bus/governance/**
backend/scripts/validate_day_one_architecture.py
```

If paths differ, locate and report the actual paths.

## Strategic framing

Do not treat the problem as “missing research”.

MED-RESEARCH-REVIEW-1 found that:

```text
55 / 55 non-Pass_3 packages have primary biomarker coverage in Pass_3 files.
0 / 55 lacked Pass_3 primary biomarker coverage.
```

Therefore the main problem is likely:

```text
research present
→ not mapped
→ not compiled
→ not promoted
→ legacy runtime package remains active
```

This sprint must classify that state accurately for each package.

## Required classification states

Use the transition-state model from `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md`:

```text
research_missing
research_present_unmapped
research_present_uncompiled
compiled_not_promoted
runtime_active_legacy
accepted_with_rationale
retired
```

Do not invent a new classification model unless absolutely required.

## Package cohort

The sprint must cover the full 55-package cohort from:

```text
knowledge_bus/governance/non_pass3_package_revalidation_register_v1.yaml
```

For each package, identify:

```text
- package_id
- package source_type
- package signal_id(s)
- package primary metric / biomarker
- runtime_loaded status
- launch_relevance
- current maturity classification
- matching Pass_3 primary biomarker spec(s)
- exact Pass_3 signal_id match, if any
- biomarker-only match, if signal_id differs
- whether multiple Pass_3 frames exist for the same biomarker
- whether the current package can be mapped to one or more Pass_3 specs
- whether the current package should be regenerated, accepted, retired, deferred or manually reviewed
```

## Promotion route classification

For each package, assign one future route:

```text
ROUTE_A_exact_signal_match_compile_candidate
ROUTE_B_primary_biomarker_match_signal_mapping_needed
ROUTE_C_multiple_pass3_frames_adjudication_needed
ROUTE_D_legacy_accepted_with_rationale
ROUTE_E_provenance_recovery_needed
ROUTE_F_retire_candidate
ROUTE_G_manual_medical_review_exception
```

Definitions:

### ROUTE_A_exact_signal_match_compile_candidate

Use where Pass_3 contains the same signal_id and same primary biomarker.

Likely low-risk candidate for compiler/promotion pilot.

### ROUTE_B_primary_biomarker_match_signal_mapping_needed

Use where Pass_3 contains the same primary biomarker, but signal_id differs.

Requires mapping decision before compile/promotion.

### ROUTE_C_multiple_pass3_frames_adjudication_needed

Use where several Pass_3 frames exist for the same primary biomarker and cannot safely collapse into one runtime signal without an identity decision.

### ROUTE_D_legacy_accepted_with_rationale

Use where legacy runtime package should remain active for now with explicit rationale.

### ROUTE_E_provenance_recovery_needed

Use where the package needs source/provenance recovery before promotion planning.

### ROUTE_F_retire_candidate

Use where the package appears unnecessary or scaffold-only.

### ROUTE_G_manual_medical_review_exception

Use where Pass_3 biomarker coverage exists but the package signal represents a different construct.

Known likely example:

```text
pkg_chronic_inflammation / signal_systemic_inflammation
```

## Pilot selection

Recommend a small pilot set for the next sprint.

The pilot set should contain 5–6 packages representing:

```text
- one clean exact signal match
- one s24 legacy package with Pass_3 equivalent
- one kb45 batch lineage package
- one architecture-anchor package
- one provenance gap or hygiene item, if safe
- one manual-review exception only as comparator, not for promotion
```

Do not choose only easy packages. The pilot must prove the promotion process across representative risk classes.

## Required outputs

Create:

```text
docs/audit-papers/KB-MAP-1_pass3_to_legacy_package_mapping_and_promotion_plan.md
```

Create or update:

```text
knowledge_bus/governance/pass3_legacy_package_mapping_plan_v1.yaml
```

Do not make this YAML runtime-consumed.

## Required report content

The report must include:

```text
- executive verdict
- summary of 55-package cohort
- route classification counts
- full 55-package mapping table
- exact signal_id match count
- primary biomarker-only match count
- multiple-frame adjudication count
- manual-review exceptions
- provenance recovery items
- retire candidates
- recommended pilot set
- recommended bulk-promotion wave
- explicit items not suitable for bulk promotion
- carry-forward register updates
- recommended next sprint
```

## Required YAML fields

For each package in `pass3_legacy_package_mapping_plan_v1.yaml`, include:

```yaml
package_id:
current_signal_ids:
current_primary_biomarkers:
runtime_loaded:
launch_relevance:
current_source_type:
current_maturity_classification:
pass3_primary_biomarker_match:
pass3_primary_biomarker_match_spec_ids:
pass3_primary_biomarker_match_signal_ids:
exact_pass3_signal_id_match:
exact_pass3_signal_id_match_spec_ids:
multiple_pass3_frames:
promotion_route:
recommended_action:
recommended_pilot_candidate:
manual_review_required:
notes:
```

## Carry-forward register

Before finish, update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Only update carry-forwards if this sprint materially changes their meaning.

Expected updates may include:

```text
CF-MRIMPROVE-001
CF-MRIMPROVE-002
CF-MRIMPROVE-003
CF-MRIMPROVE-004
CF-CRPPASS3-001
CF-CHRONICINFL-001
```

Do not mark an item resolved unless this sprint actually resolves it. Mapping/classification alone may reframe an item but does not necessarily complete the future promotion work.

## Out of scope

Do not:

```text
- promote packages
- regenerate packages
- edit signal_library.yaml
- edit package manifests
- change thresholds
- change activation logic
- change SignalEvaluator or SignalRegistry
- change scoring
- change frontend
- compile new artefacts
- retire packages
- alter runtime loading
- add user-facing warnings
```

## Required checks

Run:

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
```

If they fail, STOP and report.

## STOP conditions

STOP and report if:

```text
1. The 55-package register is missing or inconsistent.
2. Pass_3 files cannot be located.
3. Package signal IDs cannot be derived.
4. Mapping cannot distinguish exact signal match from biomarker-only match.
5. Any package appears launch-visible and risky.
6. Any proposed route would require runtime change in this sprint.
7. Validator fails.
```

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. governance documents read
3. carry-forward register read/update evidence
4. 55-package cohort count
5. Pass_3 file count scanned
6. route classification counts
7. pilot set recommendation
8. files changed
9. validators/tests run
10. test results
11. confirmation no runtime/package/code/frontend changes were made
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
- current branch matches work/KB-MAP-1-pass3-to-legacy-package-mapping-and-promotion-plan
- only docs/governance classification files are changed
- no runtime package files are changed
- no production code is changed
- no helper scripts are committed
- no ambiguous stash exists
- latest commit contains only in-scope mapping/planning work
```

## Success criteria

This sprint is complete only if:

```text
1. all 55 packages are mapped to Pass_3 coverage
2. each package has a promotion route classification
3. exact signal matches are separated from biomarker-only matches
4. multi-frame/adjudication cases are identified
5. a representative pilot set is recommended
6. no runtime behaviour is changed
7. carry-forward register is updated if needed
8. validator passes
9. Automation Bus gate passes
```

```
```
