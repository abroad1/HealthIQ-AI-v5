---
work_id: PASS3-FRAME-INDEX-2_high_risk_signal_family_index_expansion
branch: work/PASS3-FRAME-INDEX-2-high-risk-signal-family-index-expansion
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# PASS3-FRAME-INDEX-2 — High-Risk Signal Family Index Expansion

## Purpose

Expand the governed medical frame identity index beyond creatinine, using the estate-wide frame coverage audit to identify the highest-risk signal families for frame collapse.

This sprint must not let Cursor decide clinical truth.

Cursor may propose the highest-risk families from audit evidence, but selection must be based on objective criteria from `PASS3-FRAME-COVERAGE-1`, not preference, convenience, or instinct.

The goal is to prevent future package promotion from collapsing medically distinct frames into flat signals.

---

## Strategic framing

`PASS3-FRAME-COVERAGE-1` found that package promotion cannot safely continue as a naive ROUTE_A / ROUTE_C exercise.

The key estate-level finding was:

```text
0 packages are safe for naive ROUTE_A promotion.
Many packages require frame adjudication or Pass_3 enrichment before promotion.
````

The next architecture step is to expand the medical frame identity index for the highest-risk signal families, so future promotion work knows what frames must be preserved.

Creatinine was the pattern.

This sprint applies that pattern to the wider estate.

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
PASS3-FRAME-COVERAGE-1 merged
KB-UTIL-2-CREATININE-AUTHORITY-ADJUDICATION merged
MED-FRAME-2 merged
CONTEXT-MOD-1 merged
KNOWLEDGE_BUS_SOP_v1.3.1 committed
KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1 committed
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
- PASS3-FRAME-COVERAGE-1 artefacts are missing
- medical_frame_identity_index_v1.yaml is missing
- medical_frame_identity_index validator is missing
```

---

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint expands governed medical frame identity infrastructure. It must not change runtime behaviour, but it affects future medical-intelligence promotion authority.

---

## Required inputs

Read before work:

```text
docs/audit-papers/PASS3-FRAME-COVERAGE-1_estate_wide_multiframe_research_coverage_audit.md
knowledge_bus/governance/pass3_frame_coverage_audit_v1.yaml
knowledge_bus/governance/medical_frame_identity_expansion_candidates_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/schema/medical_frame_identity_index_schema_v1.yaml
backend/scripts/validate_medical_frame_identity_index.py
docs/architecture/MED-FRAME-1_signal_family_contextual_frame_architecture.md
docs/audit-papers/MED-FRAME-2_medical_frame_identity_index_report.md
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
docs/sprints/launch_core_carry_forward_register.md
```

Also inspect relevant packages and Pass_3 files for shortlisted families:

```text
knowledge_bus/packages/**
knowledge_bus/research/investigation_specs/multi_llm_research/**/*Pass_3*.json
knowledge_bus/governance/pass3_legacy_package_mapping_plan_v1.yaml
```

---

## High-risk family selection

Cursor must not choose families clinically.

Cursor must rank candidate signal families using objective audit fields from `pass3_frame_coverage_audit_v1.yaml` and `medical_frame_identity_expansion_candidates_v1.yaml`.

Ranking criteria:

```text
1. edge_case_loss_risk = high
2. promotion_safety_status = blocked_pending_frame_adjudication
3. promotion_safety_status = blocked_pending_pass3_enrichment
4. multiple Pass_3 frames for the same primary biomarker
5. legacy override/escalation logic exists
6. clinically important system area
7. risk of losing valid legacy context during promotion
8. appears in PASS3-FRAME-COVERAGE-1 worked examples
```

Required first step:

```text
Produce a ranked shortlist of the top candidate signal families before editing the frame index.
```

The shortlist must include:

```yaml
signal_family_id:
primary_biomarker_id:
packages_involved:
risk_evidence:
edge_case_loss_risk:
promotion_safety_status:
pass3_frame_count:
legacy_frame_summary:
reason_for_selection:
medical_review_required:
```

Cursor may proceed to index expansion only for the families that the prompt explicitly allows:

```text
Expand the index for the top 2–3 highest-risk families, based on audit evidence.
```

Likely candidates may include ALT, CRP and ferritin, but Cursor must verify this from the audit artefacts rather than assume.

---

## Required scope

Expand:

```text
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

for the selected high-risk families.

Minimum expected expansion:

```text
- at least 2 signal families beyond creatinine
- ideally no more than 3 signal families in this sprint
```

Do not attempt to index the entire 55-package estate.

---

## Required frame entries

For each selected signal family, create frame entries that preserve distinct medical contexts.

Each frame must include all fields already required by the medical frame identity index schema, including:

```yaml
signal_family_id:
primary_biomarker_id:
medical_frame_id:
frame_label:
frame_role:
research_spec_id:
source_package_id:
source_package_path:
activation_key:
signal_id:
promotion_state:
runtime_authority_status:
clinical_adjudication_status:
context_inputs_supported:
  biomarker_evidence:
  questionnaire_modifiers:
  medication_modifiers:
collision_group_id:
collision_status:
supersedes:
superseded_by:
notes:
```

Do not create duplicate active authority for the same activation key.

Do not mark unadjudicated legacy frames as resolved.

Do not mark draft/non-runtime entries as runtime active.

---

## Required family decision logic

For each selected family, document:

```text
- which package is currently runtime active, if any
- which Pass_3 frames exist
- which legacy frames exist
- which frames overlap
- which frames are distinct
- which frames require medical review
- which frames require Pass_3 enrichment
- which frames are compiled_not_promoted or deferred
- whether any collision exists
```

---

## Governance helper script policy

`PASS3-FRAME-COVERAGE-1` created a read-only governance helper script outside the declared docs/governance scope.

This sprint must handle governance helper scripts explicitly.

Allowed:

```text
- read-only helper scripts may be created or updated only if needed to generate or validate governance artefacts
- helper scripts must not import runtime/evaluator/pipeline modules
- helper scripts must not modify runtime/package/frontend files
- helper scripts must write only declared governance outputs
```

Preferred location for new governance helper scripts:

```text
knowledge_bus/tools/
```

Do not create new helper scripts under `backend/scripts/` unless justified by existing validator/tooling convention.

If the existing helper script is reused, classify it in the report as:

```text
read_only_governance_helper_non_runtime
```

Do not change runtime code.

---

## Required artefacts

Update:

```text
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

Create:

```text
docs/audit-papers/PASS3-FRAME-INDEX-2_high_risk_signal_family_index_expansion_report.md
```

Create or update:

```text
knowledge_bus/governance/medical_frame_identity_expansion_candidates_v1.yaml
```

Optional, only if justified:

```text
knowledge_bus/tools/build_medical_frame_identity_expansion.py
```

If a helper script is created or moved, document why.

---

## Required report content

The report must include:

```text
- executive verdict
- artefacts inspected
- ranked high-risk family shortlist
- objective selection criteria used
- selected families and rationale
- frame entries added
- collision checks
- clinical adjudication statuses
- Pass_3 enrichment needs
- context modifier relevance
- governance helper script disposition
- validation output pasted in full
- carry-forward updates
- remaining blockers
- recommended next sprint
```

---

## Carry-forward register

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Expected handling:

```text
CF-PASS3FRAME-001
Should be marked resolved only if the high-risk frame identity index expansion is completed for the selected families.

CF-PASS3FRAME-002
Remains open unless Pass_3 enrichment is actually completed, which is out of scope.

CF-PASS3FRAME-003
Remains open unless promotion pause list is fully converted into explicit next actions.

CF-GOVHELPER-001
Add or resolve depending on whether helper script policy/location is documented sufficiently.
```

If CF-GOVHELPER-001 does not yet exist, add it:

```markdown
| CF-GOVHELPER-001 | PASS3-FRAME-COVERAGE-1 | Governance helper script classification | PASS3-FRAME-COVERAGE-1 created a read-only helper script under backend/scripts to generate governance audit YAML. Future work packages must explicitly classify governance helper scripts, define allowed locations, and decide whether such scripts belong under backend/scripts or knowledge_bus/tools. | No | GOV-HELPER-1_governance_helper_script_policy |
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

## Required validations

Run and paste actual output:

```powershell
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
python -m pytest backend/tests/regression/test_med_frame_identity_index.py -q
python -m pytest backend/tests/regression/test_context_modifier_catalogue.py -q
```

Do not write only “see implementation evidence”.

---

## Medical boundary

Cursor must not decide clinical truth.

Cursor may:

```text
- identify frame candidates from artefacts
- classify existing package/research relationships
- mark medical review required
- mark Pass_3 enrichment required
- preserve medically distinct frames
```

Cursor must not:

```text
- decide a legacy edge case is obsolete
- retire packages
- activate packages
- invent new clinical thresholds
- mark clinical divergence accepted unless already approved in governance
- collapse multiple frames into one flat signal
```

---

## Out of scope

Do not:

```text
- enrich Pass_3 specs
- create new package artefacts
- promote packages
- activate packages
- retire packages
- modify runtime package files
- implement Layer B frame assembly
- implement context modifier evaluation
- change frontend
- adjudicate medical truth
- index all 55 packages
```

---

## STOP conditions

STOP and report if:

```text
1. candidate family ranking cannot be derived from audit artefacts
2. selected family cannot be mapped to package and Pass_3 evidence
3. frame entries would require clinical invention
4. duplicate active activation keys would be introduced
5. validators fail
6. any runtime/package/frontend change appears necessary
```

---

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. files inspected
3. ranked shortlist
4. selected families and rationale
5. frame entries added/updated
6. helper script disposition
7. carry-forward updates
8. validation commands run
9. actual validation output
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
- current branch matches work/PASS3-FRAME-INDEX-2-high-risk-signal-family-index-expansion
- only in-scope docs/governance/schema/tooling files changed
- no runtime package files changed
- no frontend/runtime evaluator files changed
- no ambiguous stash exists
- validators pass
```

---

## Success criteria

This sprint is complete only if:

```text
1. high-risk family shortlist is derived from PASS3-FRAME-COVERAGE-1 evidence
2. 2–3 high-risk signal families beyond creatinine are added to the medical frame identity index
3. all new frames validate
4. no duplicate active activation keys are introduced
5. unadjudicated frames remain clearly marked
6. context modifier relevance is noted but not wired
7. helper script governance is addressed
8. carry-forward register is updated
9. no runtime/package/frontend changes occur
10. actual validator outputs are pasted
```

```
```
