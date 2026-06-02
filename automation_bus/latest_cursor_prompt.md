---
work_id: PASS3-FRAME-COVERAGE-1_estate_wide_multiframe_research_coverage_audit
branch: work/PASS3-FRAME-COVERAGE-1-estate-wide-multiframe-research-coverage-audit
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# PASS3-FRAME-COVERAGE-1 — Estate-Wide Multi-Frame Research Coverage Audit

## Purpose

Audit the wider Pass_3 / package estate to determine where HealthIQ has multiple medically distinct interpretive frames under the same biomarker signal family, and whether those frames are correctly represented before package promotion continues.

This sprint must not become a one-biomarker creatinine fix.

Creatinine exposed the issue, but the architectural concern is estate-wide:

```text
A primary biomarker signal may support multiple medically valid frames.
Legacy packages may contain valid edge-case logic.
Pass_3 may contain some, all, or none of those frames.
Package promotion must not collapse valid medical frames or silently discard edge-case logic.
````

The goal is to produce an estate-level frame coverage and enrichment audit so future promotion work knows:

```text
- which packages can safely proceed to promotion
- which require multi-frame adjudication
- which require Pass_3 enrichment
- which legacy logic must be preserved
- which package candidates should remain blocked
```

This is a governance/audit sprint only.

Do not change runtime behaviour.

---

## Strategic framing

HealthIQ must support:

```text
one biomarker signal family
→ multiple medically credible frames
→ supporting / contradicting / contextual evidence
→ questionnaire and medication modifiers
→ Layer B personalised interpretation
→ frontend render-only output
```

The current promotion pipeline must not flatten this into:

```text
one biomarker = one signal = one meaning
```

The estate-level question is:

```text
Where does HealthIQ already have multiple valid medical frames, and are those frames properly represented in Pass_3, package artefacts, frame identity governance and future promotion plans?
```

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
KB-MAP-1 merged
KB-UTIL-2-PILOT merged
KB-UTIL-2-PROMOTE-PILOT merged
KB-UTIL-2-ACTIVATION-READINESS merged
KB-UTIL-2-PROMOTE-WIRE-1 merged
MED-FRAME-1 merged
MED-FRAME-2 merged
CONTEXT-MOD-1 merged
KB-UTIL-2-CREATININE-AUTHORITY-ADJUDICATION merged
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
- medical_frame_identity_index_v1.yaml is missing
- context_modifier_catalogue_draft_v1.yaml is missing
- pass3_legacy_package_mapping_plan_v1.yaml is missing
- creatinine authority adjudication report is missing
```

---

## Governance classification

```yaml
risk_level: HIGH
change_type: CONTENT
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint reviews medical-intelligence coverage and will govern future package promotion. It must not change runtime behaviour, but it is high-impact architecture work.

---

## Required inputs

Read before work:

```text
docs/architecture/MED-FRAME-1_signal_family_contextual_frame_architecture.md
docs/audit-papers/MED-FRAME-2_medical_frame_identity_index_report.md
docs/architecture/CONTEXT-MOD-1_questionnaire_and_medication_modifier_governance.md
docs/audit-papers/CONTEXT-MOD-1_questionnaire_and_medication_modifier_governance_report.md
docs/audit-papers/KB-UTIL-2-CREATININE-AUTHORITY-ADJUDICATION_creatinine_multiframe_model_decision_report.md
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
knowledge_bus/governance/pass3_legacy_package_mapping_plan_v1.yaml
knowledge_bus/governance/pass3_promotion_decision_register_v1.yaml
knowledge_bus/governance/creatinine_multiframe_authority_decision_v1.yaml
docs/sprints/launch_core_carry_forward_register.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md
docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
```

Inspect:

```text
knowledge_bus/packages/**
knowledge_bus/research/investigation_specs/multi_llm_research/**/*Pass_3*.json
knowledge_bus/research/investigation_specs/**/*.yaml
knowledge_bus/generated_pilot/**
knowledge_bus/governance/**
```

If paths differ, locate and report actual paths.

---

## Core architectural issue

This sprint must answer the estate-level question:

```text
Where do we risk losing medically valid edge-case reasoning when promoting legacy packages into Pass_3-derived artefacts?
```

Use creatinine as the pattern, not the scope.

For each reviewed signal family, distinguish:

```text
- primary biomarker signal family
- Pass_3 research frames
- legacy package frames
- supporting markers
- contradiction markers
- override/escalation rules
- questionnaire modifiers
- medication/drug-category modifiers
- current package authority
- promotion route risk
```

---

## Required package cohort

Start from the 55-package cohort in:

```text
knowledge_bus/governance/pass3_legacy_package_mapping_plan_v1.yaml
```

Prioritise review in this order:

```text
1. ROUTE_C multiple Pass_3 frame adjudication cases
2. ROUTE_G manual medical-review exceptions
3. ROUTE_B primary biomarker match but signal mismatch
4. ROUTE_A exact signal matches where legacy package contains additional override/escalation logic
5. ROUTE_E provenance recovery items
```

Do not attempt full clinical adjudication of all 55.

This is a coverage and risk audit, not a package rewrite.

---

## Required frame coverage classification

For each package reviewed, classify:

```yaml
package_id:
signal_family_id:
primary_biomarker_id:
current_route:
current_package_authority:
pass3_frame_count:
pass3_frame_ids:
legacy_frame_count:
legacy_frame_summary:
frame_coverage_status:
edge_case_loss_risk:
promotion_safety_status:
recommended_next_action:
requires_medical_review:
notes:
```

Allowed `frame_coverage_status` values:

```text
pass3_complete_for_known_frames
pass3_partial_legacy_frames_not_fully_represented
pass3_multiple_frames_need_adjudication
legacy_contains_valid_unmapped_frame
legacy_likely_scaffold_or_retire_candidate
unclear_requires_manual_review
```

Allowed `edge_case_loss_risk` values:

```text
none_detected
low
medium
high
unknown
```

Allowed `promotion_safety_status` values:

```text
safe_for_route_a_promotion
safe_after_documented_divergence_acceptance
blocked_pending_frame_adjudication
blocked_pending_pass3_enrichment
blocked_pending_provenance_recovery
retire_candidate
```

---

## Required estate-level questions

Answer explicitly:

```text
1. How many of the 55 packages have multiple Pass_3 frames for the same primary biomarker?
2. How many have legacy override/escalation logic not clearly represented in Pass_3?
3. How many appear safe for ROUTE_A-style promotion without loss of edge-case reasoning?
4. How many require Pass_3 enrichment before package retirement or activation?
5. How many require medical review rather than architecture-only classification?
6. Which signal families look most at risk of frame collapse?
7. Which signal families should be prioritised after creatinine?
8. Does the medical frame identity index need to expand beyond creatinine before further promotion?
9. Does the context modifier catalogue need extra modifier classes before Layer B wiring?
10. What promotion work should be paused until frame coverage is improved?
```

---

## Required worked examples

Include at least three worked examples:

```text
1. Creatinine high
   Use as the known pattern:
   reduced filtration / UACR / eGFR / potassium / cystatin C / context modifiers.

2. One ROUTE_C multi-frame case
   Select from the actual KB-MAP-1 route table.

3. One apparent ROUTE_A case
   Check whether it is genuinely safe or whether legacy package logic contains hidden frame richness.
```

Do not choose examples only because they are easy.

---

## Required output artefacts

Create:

```text
docs/audit-papers/PASS3-FRAME-COVERAGE-1_estate_wide_multiframe_research_coverage_audit.md
knowledge_bus/governance/pass3_frame_coverage_audit_v1.yaml
```

Optional, only if useful:

```text
knowledge_bus/governance/medical_frame_identity_expansion_candidates_v1.yaml
```

All new governance YAML must include:

```yaml
runtime_consumed: false
status: governance_audit_non_runtime
```

---

## Required report content

The report must include:

```text
- executive verdict
- artefacts inspected
- estate-level methodology
- 55-package cohort summary
- route distribution summary
- multi-frame risk summary
- edge-case-loss risk summary
- packages safe for continued promotion
- packages blocked pending frame adjudication
- packages blocked pending Pass_3 enrichment
- packages needing medical review
- creatinine worked example
- second worked example from ROUTE_C
- third worked example from ROUTE_A or ROUTE_B
- implications for KB-UTIL package promotion
- implications for medical frame identity index expansion
- implications for context modifier governance
- carry-forward updates
- recommended next sprint
- validation output pasted in full
```

---

## Required YAML content

`pass3_frame_coverage_audit_v1.yaml` must include:

```yaml
schema_version:
runtime_consumed: false
status:
work_id:
source_register:
package_count:
summary_counts:
  pass3_complete_for_known_frames:
  pass3_partial_legacy_frames_not_fully_represented:
  pass3_multiple_frames_need_adjudication:
  legacy_contains_valid_unmapped_frame:
  legacy_likely_scaffold_or_retire_candidate:
  unclear_requires_manual_review:
packages:
  - package_id:
    signal_family_id:
    primary_biomarker_id:
    current_route:
    pass3_frame_count:
    pass3_frame_ids:
    legacy_frame_count:
    legacy_frame_summary:
    frame_coverage_status:
    edge_case_loss_risk:
    promotion_safety_status:
    recommended_next_action:
    requires_medical_review:
    notes:
```

---

## Medical boundary

Cursor must not decide clinical truth.

Cursor may:

```text
- identify where research frames exist
- compare package logic to Pass_3 frame coverage
- classify risk of edge-case loss
- recommend medical review or Pass_3 enrichment
```

Cursor must not:

```text
- decide a valid legacy edge case is obsolete
- delete or retire packages
- invent clinical rules
- mark clinical divergence accepted unless already accepted in source governance
- promote or activate packages
```

---

## Carry-forwards to consider

This sprint must review and update, if appropriate:

```text
CF-CREATININE-001
CF-MRIMPROVE-001
CF-MRIMPROVE-002
CF-MRIMPROVE-003
CF-CRPPASS3-001
CF-CHRONICINFL-001
CF-CONTEXT-MOD-2
```

Likely new carry-forwards:

```text
CF-PASS3FRAME-001 — expand medical frame identity index to top high-risk multi-frame signal families
CF-PASS3FRAME-002 — Pass_3 enrichment queue for packages with valid legacy frames not fully represented
CF-PASS3FRAME-003 — promotion pause list for packages at high risk of edge-case loss
```

Do not mark a carry-forward resolved unless this sprint genuinely resolves it.

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

If any runtime or package change appears necessary, STOP and report.

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
```

---

## STOP conditions

STOP and report if:

```text
1. the 55-package mapping register cannot be loaded
2. Pass_3 files cannot be located
3. package frame coverage cannot be assessed reliably
4. audit discovers a likely runtime safety issue requiring immediate escalation
5. validators fail
6. any package/runtime/frontend change appears necessary
```

---

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. files inspected
3. package cohort count
4. methodology used
5. summary classification counts
6. high-risk frame-collapse packages
7. examples analysed
8. governance files created
9. carry-forward updates
10. validation commands run
11. actual validation output
12. confirmation no runtime/package/frontend changes
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
- current branch matches work/PASS3-FRAME-COVERAGE-1-estate-wide-multiframe-research-coverage-audit
- only in-scope docs/governance files changed
- no runtime package files changed
- no frontend/runtime evaluator files changed
- no ambiguous stash exists
- validators pass
```

---

## Success criteria

This sprint is complete only if:

```text
1. estate-wide frame coverage audit exists
2. all 55 packages are classified for frame coverage risk
3. multi-frame / edge-case-loss risks are identified
4. creatinine is treated as an example, not the whole sprint
5. at least two additional worked examples are included
6. future promotion work is clearly gated by frame coverage safety
7. carry-forward register is updated
8. no package/runtime/frontend changes occur
9. actual validator outputs are pasted
10. validators pass
```

```
```
