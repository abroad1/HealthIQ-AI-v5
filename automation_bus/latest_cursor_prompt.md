---
work_id: KB-UTIL-2-PILOT_pass3_to_runtime_artifact_compiler_pilot
branch: work/KB-UTIL-2-PILOT-pass3-to-runtime-artifact-compiler-pilot
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# KB-UTIL-2-PILOT — Pass_3 to Runtime Artefact Compiler Pilot

## Purpose

Build the first deterministic pilot compiler pathway from Pass_3 / investigation-spec v3 research into governed runtime artefacts.

This sprint is the first controlled extraction sprint after KB-MAP-1.

The goal is not to manually rewrite package files. The goal is to prove that Pass_3 research can be parsed, mapped, compiled, validated and audited without losing medical richness.

## Non-negotiable architecture rule

Do not use LLM/manual extraction as the promotion mechanism.

Cursor may use LLM assistance to write code, inspect outputs, and summarise findings, but the actual extraction must be deterministic and schema-driven.

Forbidden:

```text
- manually reading Pass_3 and copy/pasting into package files
- asking an LLM to “extract the important bits”
- summarising Pass_3 into artefacts by judgement
- bulk prompt extraction
- best-effort field selection
````

Required:

```text
Pass_3 JSON in
→ deterministic parser
→ deterministic compiler mapping
→ generated artefacts
→ validation
→ source-field preservation audit
```

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
KB-MAP-1 merged
MED-RESEARCH-REVIEW-1 merged
CRP-PASS3-MIGRATION merged
KNOWLEDGE_BUS_SOP_v1.3.1 committed
KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1 committed
docs/sprints/launch_core_carry_forward_register.md present and updated
knowledge_bus/governance/pass3_legacy_package_mapping_plan_v1.yaml present
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
- KB-MAP-1 is not merged
- Pass3 Promotion Protocol v1.1 is missing
- pass3_legacy_package_mapping_plan_v1.yaml is missing
```

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint creates compiler logic and generated Knowledge Bus artefacts. It must not wire outputs into runtime yet, but it touches the future medical intelligence promotion path.

## Required governance inputs

Read before implementation:

```text
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md
docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
docs/sprints/launch_core_carry_forward_register.md
knowledge_bus/governance/pass3_legacy_package_mapping_plan_v1.yaml
knowledge_bus/governance/non_pass3_package_revalidation_register_v1.yaml
docs/audit-papers/KB-MAP-1_pass3_to_legacy_package_mapping_and_promotion_plan.md
docs/audit-papers/MED-RESEARCH-REVIEW-1_pass3_primary_biomarker_cross_validation_addendum.md
docs/audit-papers/MED-RESEARCH-REVIEW-1_non_pass3_package_revalidation_audit.md
```

Also inspect:

```text
knowledge_bus/research/investigation_specs/multi_llm_research/**/*Pass_3*.json
knowledge_bus/schema/investigation_spec_schema_v3.0.0.yaml
knowledge_bus/schema/signal_library_schema.yaml
knowledge_bus/schema/research_brief_schema.yaml
knowledge_bus/schema/package_manifest_schema.yaml
knowledge_bus/schema/promoted_signal_intelligence_schema_v1.yaml
backend/scripts/validate_investigation_spec.py
backend/scripts/validate_knowledge_package.py
backend/scripts/validate_promoted_signal_intelligence.py
```

If paths differ, locate and report actual paths.

## Pilot scope

Use a small pilot set only.

Primary pilot candidates from KB-MAP-1:

```text
pkg_s24_creatinine_high_renal
pkg_s24_ferritin_low_iron_deficiency
```

These should be ROUTE_A exact signal match / compile candidates.

Use comparison-only cases if helpful:

```text
pkg_lipid_transport
pkg_chronic_inflammation
```

But do not promote or regenerate comparison-only exceptions unless explicitly safe and approved within this sprint.

## Required preflight

Before writing compiler code, report:

```text
1. Exact package IDs selected for pilot.
2. Current legacy package paths.
3. Matching Pass_3 file paths.
4. Matching Pass_3 spec_ids.
5. Matching signal_ids.
6. Matching primary biomarkers.
7. Whether each pilot has one Pass_3 frame or multiple frames.
8. Whether current package thresholds/activation logic match Pass_3 activation logic.
9. Whether any behavioural difference would result from generated artefacts.
10. Whether pilot can proceed without runtime wiring.
```

STOP if the selected pilot package has multiple Pass_3 frames, signal ambiguity, or threshold/activation conflict that requires clinical adjudication.

## Artefacts to generate

For each approved pilot spec, generate into a clearly isolated pilot output area, not active runtime package directories unless hardening explicitly approves.

Preferred output root:

```text
knowledge_bus/generated_pilot/kb_util_2_pilot/<package_id>/
```

For each pilot, generate:

```text
research_brief.yaml
signal_library.yaml
package_manifest.yaml
promoted_signal_intelligence.yaml
compile_manifest.yaml
source_field_preservation_audit.yaml
```

Do not overwrite existing runtime packages.

Do not update `knowledge_bus/current/latest_knowledge_status.json`.

Do not make generated pilot packages active.

## Required extraction mapping

The compiler must account for these Pass_3 fields:

```text
investigation_spec_contract_version
spec_id
signal_id
research_domain
primary_marker
trigger_direction
activation
states
supporting_markers
hypotheses
hypothesis_ranking
confirmatory_tests
override_rules
evidence
narrative
```

Each field must be mapped to one of:

```text
PACKAGE_ACTIVATION
PROMOTED_SIGNAL_INTELLIGENCE
ROOT_CAUSE_FUTURE
CARD_EVIDENCE_FUTURE
PRESENTATION_SAFETY_FUTURE
COMPILE_MANIFEST
DEFERRED_WITH_REASON
NOT_APPLICABLE_WITH_REASON
```

No field may disappear without an explicit preservation-audit entry.

## Source-field preservation audit

For each pilot spec, generate:

```text
source_field_preservation_audit.yaml
```

It must include:

```yaml
source_spec_id:
source_path:
source_hash:
compiler_version:
fields:
  field_name:
    status:
    target_artifact:
    target_path:
    reason:
```

Allowed `status` values:

```text
preserved
partially_preserved
deferred
not_applicable
blocked
```

The audit must explicitly prove that the following rich research content was not silently lost:

```text
- supporting marker roles
- relationship_kind
- marker rationale
- ranked hypotheses
- physiological claims
- caveats
- contradiction markers
- missing_data.policy
- confirmatory tests
- override rules
- evidence strength
- evidence source references
- mechanism / pathway / interpretation / implications narrative
```

## Compiler implementation

Create a deterministic compiler script or module.

Suggested path:

```text
backend/scripts/compile_pass3_pilot_artifacts.py
```

or, if repo conventions prefer Knowledge Bus scripts:

```text
knowledge_bus/scripts/compile_pass3_pilot_artifacts.py
```

The compiler must:

```text
- load explicit source Pass_3 spec(s)
- validate source structure before compile
- generate deterministic YAML output
- sort keys / lists deterministically where appropriate
- emit source hashes
- emit output hashes
- emit compile manifest
- emit source-field preservation audit
```

Do not create a broad estate compiler in this sprint.

This is a pilot compiler only.

## Validation requirements

Add or update validators/tests proving:

```text
1. Pilot compiler is deterministic.
2. Same input produces same output hashes.
3. All required Pass_3 top-level fields are accounted for.
4. Generated signal_library.yaml validates structurally.
5. Generated research_brief.yaml validates structurally.
6. Generated package_manifest.yaml validates structurally.
7. Generated promoted_signal_intelligence.yaml validates if present.
8. No generated pilot artefact is runtime-active.
9. Existing runtime packages are not overwritten.
10. No raw Pass_3 runtime reads are introduced.
```

Add targeted tests, for example:

```text
backend/tests/regression/test_kb_util2_pass3_pilot_compiler.py
```

## Standard checks

Always run:

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
```

Also run:

```powershell
python -m pytest backend/tests/regression/test_kb_util2_pass3_pilot_compiler.py -q
```

Run package validators against generated pilot artefacts if supported by the validator.

## Runtime boundary

This sprint must not wire generated artefacts into runtime.

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
knowledge_bus/current/latest_knowledge_status.json
```

If any of those appear necessary, STOP and report.

## Behavioural parity / divergence report

For each pilot package, compare generated pilot artefacts against current legacy package.

Report:

```text
- signal_id match
- primary biomarker match
- activation logic match
- threshold match
- supporting marker differences
- override rule differences
- richer intelligence preserved
- any behavioural difference
- whether generated package would be safe for future promotion
```

Do not resolve behavioural differences in this sprint. Classify them.

## Required deliverables

Create:

```text
docs/audit-papers/KB-UTIL-2-PILOT_pass3_to_runtime_artifact_compiler_pilot_report.md
```

Create generated pilot outputs under:

```text
knowledge_bus/generated_pilot/kb_util_2_pilot/
```

Create or update:

```text
knowledge_bus/governance/pass3_pilot_compile_manifest_index_v1.yaml
```

Do not make this runtime-consumed.

## Required report content

The sprint report must include:

```text
- executive verdict
- pilot package selection rationale
- source Pass_3 specs used
- generated artefacts
- source-field preservation summary
- field-level deferred items
- validation results
- deterministic output/hash evidence
- behavioural parity/divergence findings
- confirmation no runtime wiring occurred
- confirmation no manual LLM extraction occurred
- recommended next sprint
- whether pilot proves enough for broader ROUTE_A compile wave
```

## Carry-forward register

Before finish, update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Only update if this sprint materially changes a carry-forward.

Likely items:

```text
CF-MRIMPROVE-001
CF-MRIMPROVE-002
CF-MRIMPROVE-003
CF-CRPPASS3-001
CF-CHRONICINFL-001
CF-KBUTIL1-001
```

Do not mark broad migration items resolved from this pilot alone.

## Out of scope

Do not:

```text
- bulk compile all 55 packages
- promote generated artefacts into runtime
- overwrite existing packages
- change active package status
- change thresholds
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
1. selected pilot has ambiguous Pass_3 mapping
2. selected pilot has multiple Pass_3 frames requiring adjudication
3. compiler would need manual LLM extraction
4. generated artefacts would require runtime wiring to validate
5. source-field preservation cannot be proven
6. package validator cannot validate generated pilot package structure
7. behavioural divergence appears clinically meaningful
8. any runtime package would need overwriting
9. ARCH-RT validator fails
```

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. governance inputs read
3. pilot package selection
4. source Pass_3 specs selected
5. compiler files created/changed
6. generated artefacts
7. source-field preservation audit output
8. validation commands run
9. test results
10. behavioural parity/divergence summary
11. confirmation no runtime wiring
12. confirmation no manual LLM extraction
13. confirmation generated outputs are not active runtime authority
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
- current branch matches work/KB-UTIL-2-PILOT-pass3-to-runtime-artifact-compiler-pilot
- changed files are tied to compiler pilot only
- no existing runtime packages were overwritten
- no active package status changed
- no production runtime logic changed
- no frontend changed
- source-field preservation audit exists
- generated artefacts are clearly marked pilot/non-runtime
- no ambiguous stash exists
```

## Success criteria

This sprint is complete only if:

```text
1. deterministic pilot compiler exists
2. at least one clean ROUTE_A package is compiled from Pass_3
3. generated package artefacts validate structurally
4. promoted signal intelligence artefact is generated where possible
5. source-field preservation audit accounts for all rich Pass_3 fields
6. no manual LLM extraction is used
7. no runtime behaviour changes
8. no generated artefact is promoted to runtime
9. parity/divergence report is produced
10. next promotion wave can be judged from evidence
```

```
```
