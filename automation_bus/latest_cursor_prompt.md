---
work_id: PASS3-BATCH2-PROVENANCE-1_kb47_manifest_canonical_source_realign
branch: work/PASS3-BATCH2-PROVENANCE-1-kb47-manifest-canonical-source-realign
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# PASS3-BATCH2-PROVENANCE-1 — kb47 Manifest Canonical Source Realignment

## Purpose

Realign the `pkg_kb47_*` compiled package manifests so their provenance points to the canonical Batch 2 Pass_3 research asset:

```text
knowledge_bus/research/investigation_specs/multi_llm_research/Batch_2_Pass_3.json
````

rather than the archived / older:

```text
Batch_2_Pass_3_Rev1.json
```

This sprint addresses:

```text
CF-BATCH2-002 — Realign pkg_kb47_* manifest provenance to canonical Batch_2_Pass_3.json
```

This is a provenance hygiene sprint only.

Do not change signal logic, thresholds, activation keys, frame identity, runtime status, package activation, frontend behaviour, or medical interpretation.

---

## Strategic framing

`PASS3-BATCH2-INGEST-1` registered `Batch_2_Pass_3.json` as the canonical Batch 2 research asset.

It also found that existing compiled `pkg_kb47_*` packages already exist on disk, but their manifests cite the archived `Batch_2_Pass_3_Rev1.json`.

Before Batch 2 package promotion or activation readiness can proceed, package provenance must be aligned to the canonical research source.

This sprint must ensure package metadata is accurate without changing package behaviour.

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
PASS3-BATCH2-INGEST-1 merged
PASS3-BATCH2-FRAME-INDEX-1 merged
PASS3-FRAME-INDEX-3 merged
MED-FRAME-TREE-1 merged
ARCH-SENTINEL-1 merged
CI-ARCH-GATE-1 / CI-ARCH-GATE-1A merged
```

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
- Batch_2_Pass_3.json is missing
- pass3_batch2_research_asset_register_v1.yaml is missing
- pkg_kb47_* packages cannot be located
```

---

## Governance classification

```yaml
risk_level: HIGH
change_type: CONTENT
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint modifies package manifests for existing compiled packages. It must be metadata/provenance-only and must not alter runtime behaviour.

---

## Required inputs

Read before work:

```text
knowledge_bus/research/investigation_specs/multi_llm_research/Batch_2_Pass_3.json
knowledge_bus/governance/pass3_batch2_research_asset_register_v1.yaml
docs/audit-papers/PASS3-BATCH2-INGEST-1_batch2_pass3_research_asset_registration_report.md
docs/audit-papers/PASS3-BATCH2-FRAME-INDEX-1_batch2_multiframe_identity_index_expansion_report.md
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
docs/sprints/launch_core_carry_forward_register.md
```

Inspect all relevant packages:

```text
knowledge_bus/packages/pkg_kb47_*
```

Also inspect package validation tooling:

```text
backend/scripts/validate_knowledge_package.py
backend/scripts/run_architecture_validation_gate.py
```

If paths differ, locate and report actual paths.

---

## Required preflight

Before editing any manifest, report:

```text
1. total pkg_kb47_* package count
2. each package path
3. current manifest source_document / source path fields
4. current source spec_id if present
5. matching Batch_2_Pass_3 spec_id
6. whether the package signal_id matches the Batch 2 spec signal_id
7. whether package activation logic appears unchanged by this sprint
8. whether any package cannot be confidently mapped to canonical Batch_2_Pass_3.json
```

STOP if any `pkg_kb47_*` package cannot be mapped to a Batch 2 spec with confidence.

---

## Required changes

For every confirmed `pkg_kb47_*` package, update manifest provenance only.

Expected target:

```text
source_document: knowledge_bus/research/investigation_specs/multi_llm_research/Batch_2_Pass_3.json
```

or the repo-equivalent manifest field if naming differs.

If manifests also carry related source path/hash/revision fields, update them consistently to reflect canonical `Batch_2_Pass_3.json`.

Do not edit:

```text
signal_library.yaml
research_brief.yaml
thresholds
activation logic
override rules
signal_id
activation_key
runtime status
```

unless hardening explicitly identifies a metadata-only field that must be updated and proves no behavioural change.

---

## Source hash handling

If package manifests currently include source hash fields:

```text
- recalculate hash for Batch_2_Pass_3.json if repo convention requires
- update only provenance hash fields
- document the old and new values
```

If no source hash convention exists, do not invent one in this sprint. Record that provenance path was realigned without hash update.

---

## Validation requirements

After manifest updates, validate every modified package:

```powershell
python backend/scripts/validate_knowledge_package.py --package-dir <package_dir>
```

If the validator supports batch validation, use the repo-standard method and document it.

Also run:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

Do not write only “all tests passed”. Paste actual output.

---

## Required artefacts

Create:

```text
docs/audit-papers/PASS3-BATCH2-PROVENANCE-1_kb47_manifest_canonical_source_realign_report.md
```

Create or update:

```text
knowledge_bus/governance/pass3_batch2_kb47_manifest_realign_register_v1.yaml
docs/sprints/launch_core_carry_forward_register.md
```

Do not update the medical frame identity index unless a purely documentary note is needed and hardening approves it.

Do not regenerate the biomarker tree unless the frame index changes, which is not expected.

---

## Required register content

`pass3_batch2_kb47_manifest_realign_register_v1.yaml` must include:

```yaml
schema_version:
runtime_consumed: false
status:
work_id:
canonical_source:
package_count:
packages:
  - package_id:
    package_path:
    old_source_document:
    new_source_document:
    matched_spec_id:
    matched_signal_id:
    manifest_updated:
    package_validator_status:
    behaviour_change_expected:
    notes:
```

---

## Required report content

The report must include:

```text
- executive verdict
- package count
- package list
- old provenance pattern
- new canonical provenance path
- mapping method to Batch_2_Pass_3 specs
- any packages not updated and why
- package validation output pasted in full
- architecture gate output pasted in full
- confirmation signal_library/research_brief/activation logic unchanged
- confirmation no runtime/frontend/SSOT/evaluator changes
- carry-forward updates
- remaining limitations
- recommended next sprint
```

---

## Carry-forward handling

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Expected handling:

```text
CF-BATCH2-002
Mark Resolved only if all pkg_kb47_* package manifests are realigned to canonical Batch_2_Pass_3.json and validate.

CF-BATCH2-001
Should remain partially open if remaining single-frame Batch 2 families are not indexed.

CF-BATCH2-003
Should remain open. Promotion readiness review happens after indexing and provenance alignment.

CF-BATCH2-004
Should remain open unless remaining single-frame families are indexed, which is out of scope.
```

Do not mark Batch 2 promotion readiness complete.

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
knowledge_bus/current/latest_knowledge_status.json
```

Package manifest metadata updates are allowed only for `pkg_kb47_*` provenance fields.

STOP if any change would alter runtime activation or clinical interpretation.

---

## Out of scope

Do not:

```text
- index remaining Batch 2 single-frame families
- change signal_library.yaml
- change research_brief.yaml
- change thresholds
- change activation logic
- create packages
- promote packages
- activate packages
- retire packages
- update runtime loaders
- change frontend
- adjudicate medical truth
```

---

## STOP conditions

STOP and report if:

```text
1. any pkg_kb47 package cannot be matched to Batch_2_Pass_3.json
2. manifest field structure differs in a way that makes provenance update ambiguous
3. package validation fails after metadata update
4. architecture gate fails
5. any runtime/package logic/frontend change appears necessary
6. source hash convention cannot be preserved safely
```

---

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. pkg_kb47 package count
3. package-to-spec mapping table
4. manifest fields changed
5. package validation commands run
6. actual validation output
7. architecture gate output
8. carry-forward updates
9. confirmation no signal_library/research_brief/runtime/frontend changes
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
- current branch matches work/PASS3-BATCH2-PROVENANCE-1-kb47-manifest-canonical-source-realign
- only in-scope manifest/governance/docs/register files changed
- no signal_library.yaml files changed
- no research_brief.yaml files changed
- no runtime/frontend/evaluator files changed
- no ambiguous stash exists
- package validators pass
- architecture gate passes
```

---

## Success criteria

This sprint is complete only if:

```text
1. all pkg_kb47_* packages are identified
2. all pkg_kb47_* manifests are mapped to canonical Batch_2_Pass_3.json specs
3. provenance fields are realigned without changing signal logic
4. every modified package validates
5. architecture gate passes
6. CF-BATCH2-002 is updated accurately
7. no runtime/frontend/evaluator changes occur
8. no signal_library or research_brief logic changes occur
9. actual validation output is pasted
10. remaining Batch 2 work is clearly scoped
```

```
```
