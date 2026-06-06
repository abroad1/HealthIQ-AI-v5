---
work_id: PASS3-BATCH2-INGEST-1_batch2_pass3_research_asset_registration
branch: work/PASS3-BATCH2-INGEST-1-batch2-pass3-research-asset-registration
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# PASS3-BATCH2-INGEST-1 — Batch 2 Pass_3 Research Asset Registration

## Purpose

Register and audit `Batch_2_Pass_3.json` as a governed Pass_3 research asset before it is used for frame indexing, package promotion, or runtime-facing work.

This sprint must determine what Batch 2 contains, whether it is schema-valid, what biomarkers/signals it covers, whether it overlaps with existing Pass_3 batches, and whether it introduces new frame-index or enrichment candidates.

This is a research asset registration/audit sprint only.

Do not create packages.
Do not promote packages.
Do not update runtime.
Do not update SignalEvaluator, SignalRegistry, frontend, scoring, SSOT, or package files.

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
PASS3-FRAME-INDEX-3 merged
Batch_2_Pass_3.json present on main
ARCH-SENTINEL-1 merged
CI-ARCH-GATE-1 / CI-ARCH-GATE-1A merged
MED-FRAME-TREE-1 merged
````

Before starting, run and report:

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
- Batch_2_Pass_3.json cannot be found
- investigation spec schema cannot be found
```

---

## Governance classification

```yaml
risk_level: HIGH
change_type: CONTENT
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint registers a newly discovered medical research asset. It does not alter runtime, but it affects future research coverage, frame indexing, package generation and promotion decisions.

---

## Required inputs

Locate and inspect:

```text
knowledge_bus/research/investigation_specs/multi_llm_research/Batch_2_Pass_3.json
knowledge_bus/research/investigation_specs/multi_llm_research/**/*Pass_3*.json
knowledge_bus/schema/investigation_spec_schema_v3.0.0.yaml
backend/scripts/validate_investigation_spec.py
knowledge_bus/governance/pass3_frame_coverage_audit_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/medical_frame_identity_expansion_candidates_v1.yaml
knowledge_bus/governance/pass3_legacy_package_mapping_plan_v1.yaml
docs/architecture/biomarker_medical_frame_tree.md
docs/sprints/launch_core_carry_forward_register.md
```

If paths differ, locate and report the actual paths.

---

## Required investigation

For `Batch_2_Pass_3.json`, report:

```text
1. file path
2. file size
3. number of specs
4. schema / contract version
5. all spec_ids
6. all signal_ids
7. all primary_marker.biomarker_id values
8. trigger directions
9. supporting markers
10. contradiction markers if present
11. confirmatory tests if present
12. evidence/source fields
13. any invalid or incomplete specs
```

Then compare Batch 2 against the existing Pass_3 estate:

```text
1. spec_ids already present elsewhere
2. signal_ids already present elsewhere
3. primary biomarkers already present elsewhere
4. new biomarkers not seen in other Pass_3 batches
5. new signal_ids not seen in other Pass_3 batches
6. overlapping but distinct frames
7. possible duplicate frames
8. likely new medical-frame-index candidates
9. likely package-promotion / enrichment implications
```

---

## Required validation

Validate every spec in Batch 2.

If the existing validator can validate the whole batch directly, use it.

If the validator requires one spec at a time, split Batch 2 into temporary per-spec files under a clearly temporary ignored/generated validation folder, then validate each one.

Use the project’s existing validation style where possible.

Do not commit temporary split files unless hardening explicitly approves.

---

## Required classifications

For every Batch 2 spec, classify:

```yaml
spec_id:
signal_id:
primary_biomarker_id:
trigger_direction:
schema_valid:
already_indexed_in_medical_frame_index:
existing_pass3_overlap:
overlap_type:
new_marker_to_pass3_estate:
new_signal_to_pass3_estate:
likely_frame_identity_action:
likely_package_action:
medical_review_required:
notes:
```

Allowed `overlap_type` values:

```text
none_new_spec
same_signal_same_frame_possible_duplicate
same_signal_distinct_frame
same_biomarker_distinct_signal
supporting_marker_overlap_only
unclear_manual_review
```

Allowed `likely_frame_identity_action` values:

```text
no_action_already_indexed
add_to_existing_signal_family
create_new_signal_family_entry
defer_pending_medical_review
defer_pending_source_validation
possible_duplicate_review
```

Allowed `likely_package_action` values:

```text
none
future_pass3_compile_candidate
future_pass3_enrichment_candidate
blocks_legacy_retirement_until_indexed
possible_duplicate_do_not_compile
manual_review_required
```

---

## Required artefacts

Create:

```text
docs/audit-papers/PASS3-BATCH2-INGEST-1_batch2_pass3_research_asset_registration_report.md
knowledge_bus/governance/pass3_batch2_research_asset_register_v1.yaml
```

Update if needed:

```text
knowledge_bus/governance/medical_frame_identity_expansion_candidates_v1.yaml
docs/sprints/launch_core_carry_forward_register.md
```

Do not update:

```text
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
docs/architecture/biomarker_medical_frame_tree.md
```

unless hardening explicitly approves. This sprint is asset registration; indexing comes later.

---

## Required report content

The report must include:

```text
- executive verdict
- Batch 2 file path and metadata
- validation method
- validation results with actual output
- spec count
- signal_id list
- primary biomarker list
- new vs overlapping markers
- new vs overlapping signals
- duplicate / possible duplicate findings
- comparison against existing Pass_3 batches
- comparison against medical frame identity index
- implications for frame-index expansion
- implications for package promotion
- carry-forward updates
- recommended next sprint
- confirmation no runtime/package/frontend changes
```

---

## Carry-forward handling

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Expected possible carry-forwards:

```text
CF-BATCH2-001 — index newly registered Batch 2 frames into medical_frame_identity_index_v1.yaml
CF-BATCH2-002 — resolve possible duplicate Batch 2 specs
CF-BATCH2-003 — compile eligible Batch 2 Pass_3 specs after indexing
```

Only add carry-forwards that are actually supported by the audit.

Do not mark existing frame-index or promotion work resolved merely because Batch 2 is registered.

---

## Runtime boundary

Do not modify:

```text
SignalEvaluator
SignalRegistry
runtime loaders
domain_score_assembler
report_compiler
frontend
SSOT
scoring thresholds
unit conversion
knowledge_bus/packages/*
knowledge_bus/current/latest_knowledge_status.json
```

If any runtime/package/frontend change appears necessary, STOP and report.

---

## Required validations

Run and paste actual output:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_intelligence_architecture.py
python backend/scripts/validate_day_one_architecture.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

Also validate Batch 2 using the investigation spec validator, with actual output pasted.

Do not write only “all tests passed”.

---

## Out of scope

Do not:

```text
- index Batch 2 frames into medical_frame_identity_index_v1.yaml
- regenerate the biomarker tree
- create packages
- promote packages
- activate packages
- retire packages
- modify package files
- change runtime loading
- change frontend
- adjudicate clinical truth
- invent missing clinical fields
```

---

## STOP conditions

STOP and report if:

```text
1. Batch_2_Pass_3.json is missing
2. Batch 2 cannot be parsed as JSON
3. schema validation fails in a way that cannot be isolated per spec
4. duplicate spec_ids conflict with existing Pass_3 estate
5. the audit cannot distinguish new frames from possible duplicates
6. any runtime/package/frontend change appears necessary
7. architecture gate fails
```

---

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. Batch 2 path and metadata
3. validation method
4. actual validation output
5. spec/signal/biomarker counts
6. overlap findings
7. new marker/signal findings
8. governance files created/updated
9. carry-forward updates
10. confirmation no runtime/package/frontend changes
```

---

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
- current branch matches work/PASS3-BATCH2-INGEST-1-batch2-pass3-research-asset-registration
- only in-scope docs/governance files changed
- no runtime package files changed
- no frontend/runtime evaluator files changed
- no temporary split validation files are committed unless explicitly approved
- no ambiguous stash exists
- architecture gate passes
```

---

## Success criteria

This sprint is complete only if:

```text
1. Batch_2_Pass_3.json is located and registered
2. every Batch 2 spec is validated or validation failures are explicitly documented
3. all Batch 2 spec_ids, signal_ids and biomarkers are listed
4. overlap with existing Pass_3 estate is classified
5. new markers/signals are identified
6. future frame-index/package implications are documented
7. carry-forward register is updated if needed
8. no runtime/package/frontend changes occur
9. actual validation output is pasted
10. architecture gate passes
```

```
```
