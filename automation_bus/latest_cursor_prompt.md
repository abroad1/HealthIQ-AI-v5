---
work_id: MED-FRAME-TREE-1_generated_human_readable_biomarker_frame_tree
branch: work/MED-FRAME-TREE-1-generated-human-readable-biomarker-frame-tree
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# MED-FRAME-TREE-1 — Generated Human-Readable Biomarker Frame Tree

## Purpose

Create a generated, human-readable medical frame tree showing how HealthIQ’s biomarker signal families break down into medically distinct frames, evidence roles, context modifiers, package authority and promotion status.

The tree must be generated from governed source artefacts.

It must not become a manually maintained second source of truth.

Core principle:

```text
The tree is an output, not an authority.
````

Authority remains with:

```text
Pass_3 / investigation specs
→ medical_frame_identity_index_v1.yaml
→ context_modifier_catalogue_draft_v1.yaml
→ package / promotion governance
→ generated tree
```

---

## Strategic framing

HealthIQ now has:

```text
- medical frame identity index
- context modifier catalogue
- Pass_3 frame coverage audit
- architecture sentinel gate
- CI architecture gate
```

The next need is human visibility.

We need a clear tree-style document that allows product, architecture, medical review and future developers to see:

```text
biomarker signal family
├── medical frame
│   ├── evidence markers
│   ├── context modifiers
│   ├── package authority
│   ├── Pass_3 / legacy source
│   └── promotion / adjudication status
```

This should help prevent future agents from flattening edge cases or losing valid medical reasoning during package promotion.

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
ARCH-SENTINEL-1 merged
CI-ARCH-GATE-1 merged
CI-ARCH-GATE-1A merged
MED-FRAME-2 merged
CONTEXT-MOD-1 merged
PASS3-FRAME-COVERAGE-1 merged
PASS3-FRAME-INDEX-2 merged
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
- medical_frame_identity_index_v1.yaml is missing
- context_modifier_catalogue_draft_v1.yaml is missing
- pass3_frame_coverage_audit_v1.yaml is missing
- architecture gate script is missing
```

---

## Governance classification

```yaml
risk_level: STANDARD
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint creates generated documentation and non-runtime tooling. It must not change runtime behaviour.

---

## Required inputs

Read before implementation:

```text
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
knowledge_bus/governance/pass3_frame_coverage_audit_v1.yaml
knowledge_bus/governance/medical_frame_identity_expansion_candidates_v1.yaml
knowledge_bus/governance/pass3_promotion_decision_register_v1.yaml
docs/architecture/MED-FRAME-1_signal_family_contextual_frame_architecture.md
docs/architecture/CONTEXT-MOD-1_questionnaire_and_medication_modifier_governance.md
docs/audit-papers/PASS3-FRAME-COVERAGE-1_estate_wide_multiframe_research_coverage_audit.md
docs/audit-papers/PASS3-FRAME-INDEX-2_high_risk_signal_family_index_expansion_report.md
docs/sprints/launch_core_carry_forward_register.md
knowledge_bus/tools/README_governance_helpers.md
```

Also inspect:

```text
backend/scripts/run_architecture_validation_gate.py
backend/scripts/validate_medical_intelligence_architecture.py
backend/tests/architecture/test_medical_intelligence_architecture_sentinels.py
```

---

## Required implementation

Create a deterministic tree generator.

Preferred path:

```text
knowledge_bus/tools/build_biomarker_medical_frame_tree.py
```

The generator must:

```text
- read governed source artefacts
- generate Markdown output
- not read raw Pass_3 as its primary source
- not infer clinical meaning
- not modify runtime/package/frontend files
- sort output deterministically
- include generation metadata
- clearly state the tree is generated and non-authoritative
```

Do not place this tool under `backend/scripts/` unless hardening explicitly approves.

---

## Required generated output

Create:

```text
docs/architecture/biomarker_medical_frame_tree.md
```

Optional focused companion if helpful:

```text
docs/architecture/biomarker_medical_frame_tree_indexed_families.md
```

The generated Markdown must include at least the indexed families currently in:

```text
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

Expected current families include:

```text
- creatinine high
- ALT high
- CRP high
- ferritin high
```

Do not hardcode these names. Read them from the index.

---

## Required tree content

For each signal family, the tree must show:

```text
- signal_family_id
- primary_biomarker_id
- each medical_frame_id
- frame_label
- frame_role
- signal_id
- activation_key
- source package
- source package path
- research_spec_id
- promotion_state
- runtime_authority_status
- clinical_adjudication_status
- collision_status
- context inputs supported
- linked context modifiers where catalogue references the frame
- notes / unresolved status
```

The output must make it visually clear where frames are:

```text
- runtime_active_canonical
- runtime_active_legacy_unadjudicated
- compiled_not_promoted
- deferred
- superseded
- retired
```

---

## Required worked tree shape

The generated Markdown should use a clear tree-like structure, for example:

```text
## signal_creatinine_high — creatinine

├── Reduced glomerular filtration
│   ├── Frame ID: frame_creatinine_reduced_glomerular_filtration
│   ├── Source package: pkg_kb52c...
│   ├── Status: runtime_active_canonical
│   ├── Evidence/modifier links: known CKD, NSAID, ACE/ARB, diuretic
│   └── Notes: current Pass_3 authority
│
├── Legacy eGFR escalation
│   ├── Source package: pkg_s24...
│   ├── Status: runtime_active_legacy_unadjudicated
│   └── Notes: preserved pending Pass_3 enrichment
```

Exact formatting can differ, but it must be readable by humans.

---

## Source-of-truth rule

The generated tree must include a header stating:

```text
This document is generated from governed HealthIQ architecture artefacts.
Do not edit this file manually.
Update the underlying governance files and regenerate.
```

The generator must include enough metadata to show:

```text
- generated timestamp
- source files used
- source file hashes if practical
- generator version
```

---

## Regression tests

Create:

```text
backend/tests/regression/test_biomarker_medical_frame_tree_generation.py
```

Tests must prove:

```text
1. generator runs successfully
2. generated tree contains every signal_family_id from medical_frame_identity_index_v1.yaml
3. generated tree contains every medical_frame_id from medical_frame_identity_index_v1.yaml
4. generated tree contains linked context modifiers for frames where modifier catalogue references exist
5. generated tree declares itself generated / do-not-edit
6. generator is deterministic
7. generator does not modify governance source files
8. generator does not write outside docs/architecture/
```

---

## Governance helper boundary

This sprint may create a governance helper script because it is explicitly declared.

Rules:

```text
- helper script must live under knowledge_bus/tools/
- helper script must be read-only against governance inputs
- helper script must write only declared tree documentation outputs
- helper script must not import runtime/evaluator/frontend modules
- helper script must not modify package files
```

The existing medical-intelligence sentinel should pass after adding the helper.

---

## Required validations

Run and paste actual output:

```powershell
python knowledge_bus/tools/build_biomarker_medical_frame_tree.py
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_intelligence_architecture.py
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/regression/test_biomarker_medical_frame_tree_generation.py -q
```

Also run:

```powershell
python -m pytest backend/tests/architecture/test_medical_intelligence_architecture_sentinels.py -q
```

Do not write only “all tests passed”.

---

## Required report

Create:

```text
docs/audit-papers/MED-FRAME-TREE-1_generated_human_readable_biomarker_frame_tree_report.md
```

Report must include:

```text
- executive verdict
- source artefacts read
- generator path
- generated tree path
- indexed families included
- number of frames included
- context modifier links included
- determinism evidence
- validation output pasted in full
- runtime boundary confirmation
- carry-forward updates
- remaining limitations
- recommended next sprint
```

---

## Carry-forward register

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

only if needed.

Expected handling:

```text
CF-PASS3FRAME-003
May remain open. The tree supports promotion safety visibility but does not itself complete package promotion gating.

CF-CONTEXT-MOD-2
Remains open. The tree may show modifier links, but it does not bind modifiers into Layer B.

Possible new carry-forward:
CF-MEDTREE-001 — wire generated tree refresh into architecture gate or docs generation workflow if not completed in this sprint.
```

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

## Out of scope

Do not:

```text
- implement Layer B frame evaluation
- implement context modifier evaluation
- promote packages
- activate packages
- enrich Pass_3 specs
- manually rewrite medical trees
- create a second authority source
- change frontend
- change runtime behaviour
```

---

## STOP conditions

STOP and report if:

```text
1. tree generation would require manual clinical interpretation
2. generator cannot read the frame index cleanly
3. generated tree omits indexed frames
4. generated tree would need to become authoritative
5. generator would need runtime imports
6. generator would write outside declared docs paths
7. architecture gate fails
```

---

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. source files inspected
3. generator created
4. generated tree created
5. frame/family counts
6. tests created
7. validation commands run
8. actual validation output
9. confirmation no runtime/package/frontend changes
10. carry-forward updates
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
- current branch matches work/MED-FRAME-TREE-1-generated-human-readable-biomarker-frame-tree
- only in-scope docs/tooling/test/register files changed
- no runtime package files changed
- no frontend/runtime evaluator files changed
- no ambiguous stash exists
- architecture gate passes
```

---

## Success criteria

This sprint is complete only if:

```text
1. deterministic tree generator exists
2. human-readable biomarker frame tree exists
3. tree includes every indexed signal family
4. tree includes every indexed medical frame
5. tree links context modifiers where available
6. tree clearly states it is generated and non-authoritative
7. regression tests pass
8. architecture gate passes
9. no runtime/package/frontend changes occur
10. future update process is clear
```

```
```
