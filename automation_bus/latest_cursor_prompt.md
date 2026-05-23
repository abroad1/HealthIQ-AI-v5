---
work_id: LC-S14
branch: scaffold/lc-s14-direction-aware-scoring
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# LC-S14 — Direction-Aware Scoring Framework

## Classification

This is a HIGH-risk BEHAVIOUR scaffold sprint.

Reason: this sprint may touch biomarker scoring behaviour, scoring policy, analytical interpretation of below-range versus above-range deviations, regression tests and Sentinel protections.

This sprint is part of the approved HealthIQ AI core scaffold completion programme.

This is not a scoring redesign sprint.  
This is not a reference-range rewrite sprint.  
This is not a unit-governance sprint.  
This is not a Knowledge Bus expansion sprint.  
This is not a frontend redesign sprint.  
This is not a Gemini/LLM sprint.

## Purpose

Replace one-off biomarker scoring exceptions with a governed direction-aware scoring framework.

The goal is to allow HealthIQ AI to safely score biomarkers where high and low deviations have different clinical meaning, without adding bespoke hardcoded exceptions for each biomarker.

This sprint directly addresses the scaffold weakness identified in the LC-S12A architecture audit and carried forward into the approved scaffold plan.

## Core rule

Preserve this non-negotiable policy:

```text
Use lab-derived reference ranges for biomarker interpretation wherever the lab provides them.
Do not substitute global/default ranges.
Do not change measured biomarker values.
Do not change units.
Do not change signal firing unless explicitly required and approved.
````

Direction-aware scoring is about how to interpret position relative to the lab range, not about replacing the lab range.

## Controlling authority

Read before doing anything:

```text
docs/planning-papers/HealthIQ_AI_core_scaffold_completion_definition_v1.md
docs/planning-papers/HealthIQ_AI_Core_Scaffold_Completion_Sprint_Plan_FINAL.md
docs/audit-papers/LC-S12B_core_scaffold_definition_notes.md
docs/audit-papers/LC-S13_lifestyle_coherence_narrative_notes.md
```

Also inspect if present:

```text id="un4rwh"
docs/audit-papers/LC-S12A_forensic_architecture_audit.md
docs/audit-papers/LC-S11A_trust_blocker_correction_notes.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md
```

If the scaffold definition document is missing, STOP.

## Required output documentation

Create or update:

```text id="2o2p0e"
docs/audit-papers/LC-S14_direction_aware_scoring_notes.md
```

This document must include:

1. preflight results
2. current scoring architecture summary
3. location and behaviour of the current ALT bypass
4. directionality policy design
5. biomarkers covered in this sprint
6. files changed
7. tests added/updated
8. Sentinel updates
9. proof that lab-derived ranges remain authoritative
10. proof that units/display fidelity are unaffected
11. residual risks
12. recommendation for LC-S15/Sprint 4

## Mandatory preflight

Run and record:

```powershell id="eim0c0"
git branch --show-current
git status --short
git log --oneline -n 8
git stash list
```

Verify work-package token:

```powershell id="evfod5"
Test-Path automation_bus/state/work_package_active.json
```

Read `automation_bus/state/work_package_active.json` and confirm:

* `work_id` is `LC-S14`
* branch is `scaffold/lc-s14-direction-aware-scoring`

If token is missing or mismatched, STOP:

```text id="b0ftdf"
Kernel start not executed or work package mismatch.
```

Confirm controlling docs exist:

```powershell id="7ofccl"
Test-Path docs/planning-papers/HealthIQ_AI_core_scaffold_completion_definition_v1.md
Test-Path docs/planning-papers/HealthIQ_AI_Core_Scaffold_Completion_Sprint_Plan_FINAL.md
```

If either is missing, STOP.

## Cross-sprint guard preflight

Before implementation, run prior scaffold / launch-core protections.

At minimum run the current equivalents of:

```powershell id="rqm96f"
python -m pytest backend/tests/regression/test_lc_s8f_phase_b_true_conversions.py -q
python -m pytest backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py -q
python -m pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q
python -m pytest backend/tests/regression/test_lc_s10b_launch_core_protection.py -q
python -m pytest backend/tests/regression/test_lc_s11a_trust_blocker_correction.py -q
python -m pytest backend/tests/regression/test_lc_s13_lifestyle_coherence_narrative.py -q
```

If one of these files has a different current name, find the current equivalent and record the substitution.

If a prior scaffold/launch-core guard fails, STOP unless the failure is already documented as unrelated and GPT/human authority explicitly permits continuation.

Do not proceed while prior protected behaviours are broken.

---

# Phase 1 — Authority and current-state investigation

Before making any changes, identify and record the current authority paths for:

1. biomarker scoring rules
2. lab-derived reference range scoring
3. current ALT low-value bypass
4. score-to-status mapping
5. domain/system score aggregation if affected
6. biomarker SSOT metadata
7. scoring policy YAML or equivalent
8. signal activation logic
9. Sentinel packs protecting scoring and launch-core output
10. tests currently covering ALT, HDL, ApoA1, liver enzymes and lipid markers

Known likely files to inspect:

```text id="u3k8ms"
backend/core/scoring/rules.py
backend/core/scoring/engine.py
backend/core/scoring/primitives.py
backend/core/analytics/bio_stats_engine.py
backend/core/analytics/domain_score_assembler.py
backend/ssot/scoring_policy.yaml
backend/ssot/biomarkers.yaml
backend/tests/unit/test_scoring_rules.py
backend/tests/regression/test_lc_s11a_trust_blocker_correction.py
sentinel/packs/lc_s10b_launch_core_protection_v1.json
```

STOP if there are multiple competing scoring authorities and the correct one cannot be established.

## Required current-state findings

Record in `LC-S14_direction_aware_scoring_notes.md`:

* how standard biomarkers are currently scored against lab-derived ranges
* where derived ratio policy scoring is handled
* whether scoring is currently symmetric around the lab range
* exact current ALT bypass behaviour
* whether bio_stats/system burden calculations are affected by the same asymmetry problem
* whether high/low direction is currently represented anywhere in SSOT or scoring policy
* whether signal activation already has directionality controls separate from scoring

---

# Phase 2 — Design the smallest safe policy mechanism

## Required design

Implement the smallest governed directionality mechanism that replaces hardcoded biomarker-specific exceptions.

The framework must support these direction classes:

```text id="rp58cd"
bidirectional_concern
high_only_concern
low_only_concern
protective_high
protective_low
informational_low
informational_high
```

You may choose the exact enum names if they are consistent and documented.

The policy must be stored in a governed configuration/SSOT/policy location, not hardcoded inside scoring logic.

Preferred location, if appropriate:

```text id="ovmejv"
backend/ssot/scoring_policy.yaml
```

or an equivalent existing scoring policy authority if discovered.

## Required initial coverage

At minimum, cover representative biomarkers:

```text id="j5ybxg"
ALT
AST
GGT
ALP
HDL cholesterol
ApoA1
```

Also investigate and document whether these should be included now or deferred:

```text id="s3f0n2"
ferritin
transferrin
CRP
TSH
Free T4
```

If clinical directionality for a biomarker is uncertain or context-dependent, do not invent policy. Mark it as deferred with reason.

## Required behaviour by marker class

### High-only concern

Example class:

```text
ALT, AST, GGT, ALP where low values are not treated as an alarming clinical concern
```

Behaviour:

* above upper lab range may reduce score / trigger concern according to existing scoring rules
* below lower lab range should not produce critical/alarming score unless explicitly governed
* below lower lab range may be informational, neutral, or low-severity depending on policy
* high behaviour must remain intact

### Protective-high

Example class:

```text
HDL, ApoA1
```

Behaviour:

* high value should not be penalised as negative risk solely because above upper lab range
* low value may remain concerning if governed
* borderline high protective values should not create low scores
* ApoB/ApoA1 ratio logic must remain separate and unaffected

### Bidirectional concern

Behaviour:

* both low and high deviations may be scored as concerning
* current symmetric behaviour may remain where clinically appropriate

### Informational-only deviation

Behaviour:

* out-of-range value may be visible but should not create alarming score
* may affect caveat/explanation if governed
* should not drive domain “Needs review” alone

---

# Phase 3 — Implementation constraints

## Preserve lab-derived range policy

Do not change the rule that lab-provided ranges are authoritative for standard biomarkers.

Do not introduce default/global ranges.

Do not change range parsing.

Do not change units.

Do not change uploaded-unit display fidelity.

## Preserve signal activation separation

Signal activation and biomarker score directionality are related but distinct.

Do not change signal libraries or Knowledge Bus assets in this sprint.

Do not change signal firing unless a test proves scoring policy cannot be separated from signal policy. If that happens, STOP for GPT review.

## Preserve existing domain/signal behaviour unless intentionally protected

This sprint may change biomarker score/status for direction-sensitive cases such as low ALT or high ApoA1.

It must not unexpectedly change:

* homocysteine lead finding
* LC-S13 lifestyle visibility
* LC-S11A blood sugar correction
* LC-S8F/G units/display fidelity
* ApoB/ApoA1 ratio interpretation
* unrelated biomarker scores

If broader domain score shifts occur, document and justify them.

STOP if domain/system aggregation depends on symmetric z-scores in a way that cannot be safely adjusted within this sprint.

---

# Potentially allowed files

Only edit what is necessary.

Potentially allowed backend:

```text id="8mx1hg"
backend/core/scoring/**/*
backend/core/analytics/bio_stats_engine.py
backend/core/analytics/domain_score_assembler.py
backend/core/dto/**/* only if needed for score/status visibility
backend/ssot/scoring_policy.yaml
backend/ssot/biomarkers.yaml only if adding directionality metadata is clearly the selected governed policy location
backend/tests/unit/**/*
backend/tests/regression/**/*
```

Potentially allowed Sentinel/docs:

```text id="kp47a7"
sentinel/packs/**/*
sentinel/**/*
docs/audit-papers/LC-S14_direction_aware_scoring_notes.md
```

## Forbidden unless GPT explicitly approves

```text id="drj09k"
backend/ssot/units.yaml
backend/core/units/registry.py
backend/core/analytics/narrative_report_compiler_v1.py
backend/core/analytics/report_compiler_v1.py
backend/core/analytics/lifestyle_consumer_surface_v1.py
knowledge_bus/**/*
frontend/**/*
automation_bus/state/*
automation_bus/latest_gate_evidence.json
automation_bus/latest_gate_output.txt
automation_bus/latest_cursor_status.json
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
```

Do not modify unit conversion, lifestyle propagation, Knowledge Bus content, frontend rendering, or Automation Bus scripts in this sprint.

If those appear necessary, STOP.

---

# Required tests

Add or update deterministic tests for:

## Direction-aware scoring

* low ALT does not produce critical/alarming score
* high ALT remains concerning
* low AST/GGT/ALP behaviour follows policy
* high AST/GGT/ALP behaviour remains concerning where appropriate
* high HDL is not penalised as negative solely because high
* low HDL remains concerning if governed
* high ApoA1 is not penalised as negative solely because high
* low ApoA1 remains concerning if governed
* bidirectional markers retain current behaviour where policy says bidirectional
* unknown/unconfigured biomarkers retain safe existing behaviour

## Regression preservation

* lab-derived ranges remain authoritative
* no global/default ranges are introduced
* units unchanged
* LC-S8F/G unit and display fidelity still passes
* LC-S11A trust blockers remain fixed
* LC-S13 lifestyle/coherence/narrative protections still pass
* ApoB/ApoA1 ratio remains coherent
* homocysteine lead finding remains intact

## Policy safety

* no hardcoded `biomarker_name == "alt"` bypass remains as the directionality mechanism
* policy file/schema rejects invalid directionality class
* missing directionality policy uses safe default behaviour
* directionality policy is documented and test-covered

---

# Required Sentinel / test harness obligations

Sentinel update is required.

At minimum add/update defect classes:

```text id="9f8bpv"
direction_sensitive_marker_false_alarm
low_enzyme_false_alarm
protective_high_marker_penalised
hardcoded_biomarker_scoring_exception
scoring_signal_directionality_conflation
```

Each must point to an active deterministic regression test.

Do not add placeholder Sentinel entries.

If a defect class cannot yet be fully guarded, document why and add the strongest available deterministic guard.

---

# Required validation commands

Run relevant targeted tests.

At minimum:

```powershell id="5kiw47"
python -m pytest backend/tests/unit/test_scoring_rules.py -q
python -m pytest backend/tests/regression/test_lc_s14_direction_aware_scoring.py -q
python -m pytest backend/tests/regression/test_lc_s8f_phase_b_true_conversions.py -q
python -m pytest backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py -q
python -m pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q
python -m pytest backend/tests/regression/test_lc_s10b_launch_core_protection.py -q
python -m pytest backend/tests/regression/test_lc_s11a_trust_blocker_correction.py -q
python -m pytest backend/tests/regression/test_lc_s13_lifestyle_coherence_narrative.py -q
```

If a listed test file has a different current name, find and run the current equivalent, then record the substitution.

If scoring changes affect broader tests, run the relevant broader backend suite and record why.

Do not skip LC-S8F/G or LC-S13 regressions.

---

# Optional API/DTO smoke check

If easy and already supported by existing tools, run one smoke check of a panel containing:

```text id="0g9hyf"
low ALT
high ALT
high ApoA1
high HDL
```

Confirm:

* low ALT not alarming
* high ALT concerning
* high ApoA1 not penalised solely for being high
* high HDL not penalised solely for being high
* values/ranges/units unchanged

Do not create frontend UAT work unless required.

---

# Acceptance criteria

This sprint is complete only if:

* the current ALT hardcoded bypass is replaced or rendered unnecessary by governed directionality policy
* directionality policy is data/policy-driven, not hardcoded per marker in scoring logic
* high-only, protective-high and bidirectional classes are supported
* representative markers are covered
* low ALT / low enzyme false alarms are prevented
* high enzyme concern remains intact
* high HDL/ApoA1 are not penalised solely because high
* lab-derived range policy remains intact
* units/display fidelity remain intact
* signal activation remains separate unless explicitly escalated
* prior scaffold/launch-core guards still pass
* Sentinel defect classes are active and deterministic
* notes clearly document residual risks and deferred biomarkers
* no forbidden files are touched

---

# Closure requirements

When complete:

1. Run:

```powershell id="roau96"
git branch --show-current
git status --short
git diff --name-only
git log --oneline -n 8
git stash list
```

2. Classify:

   * tracked modified files
   * staged files
   * untracked files
   * tooling files
   * out-of-scope files
   * stash entries

3. STOP if unrelated files, tooling leakage, dirty branch ambiguity, or stash ambiguity exists.

4. Run finish:

```powershell id="t4s651"
python backend/scripts/run_work_package.py finish
```

5. Report whether finish completed or failed.

6. Do not merge.

7. Do not create `automation_bus/latest_audit_summary.md`.

8. Do not claim final approval.

## Cursor completion statement

Cursor implements and reports only.

Cursor may not self-certify clinical correctness, architecture correctness, scaffold completion, merge readiness, launch readiness, or permission to begin the next sprint.

```
```
