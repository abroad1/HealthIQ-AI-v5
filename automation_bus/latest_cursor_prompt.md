---
work_id: LC-S13
branch: scaffold/lc-s13-lifestyle-coherence-narrative
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# LC-S13 — Lifestyle Propagation, Coherence Guard and Narrative Language Audit

## Classification

This is a HIGH-risk MIXED scaffold sprint.

Reason: this sprint may touch backend lifestyle/questionnaire logic, analytics, DTO payloads, frontend results rendering, deterministic narrative surfaces, regression tests, Sentinel packs and documentation.

This sprint is part of the approved HealthIQ AI core scaffold completion programme.

This is not a launch-readiness sprint.  
This is not a frontend redesign sprint.  
This is not a Gemini/LLM sprint.  
This is not a broad questionnaire redesign sprint.  
This is not a medication-modifier sprint.

## Purpose

Prove that questionnaire-derived intelligence can travel from structured input to governed user-visible output, while protecting the rendered report from contradictory or misleading deterministic/mock-mode language.

This sprint has three bounded scopes:

1. Lifestyle and questionnaire propagation pathway
2. Report coherence guard
3. Narrative language audit

The goal is to complete and protect a scaffold pathway, not to add broad lifestyle content.

## Controlling authority

Read before doing anything:

```text
docs/planning-papers/HealthIQ_AI_core_scaffold_completion_definition_v1.md
docs/planning-papers/HealthIQ_AI_Core_Scaffold_Completion_Sprint_Plan_FINAL.md
docs/audit-papers/LC-S12B_core_scaffold_definition_notes.md
````

Also inspect if present:

```text
docs/audit-papers/LC-S12A_forensic_architecture_audit.md
docs/audit-papers/LC-S11_forensic_human_uat_audit.md
docs/audit-papers/LC-S11A_trust_blocker_correction_notes.md
docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md
```

If the scaffold definition document is missing, STOP.

## Required output documentation

Create or update:

```text
docs/audit-papers/LC-S13_lifestyle_coherence_narrative_notes.md
```

This document must include:

1. preflight results
2. lifestyle computation trace
3. whether `confidence_adjustments` compute meaningful non-zero output
4. whether lifestyle bridges fire correctly
5. whether this sprint proceeded normally or required split/STOP
6. files changed
7. coherence guards added
8. narrative language findings
9. Sentinel updates
10. tests run
11. residual risks
12. recommendation for next sprint

## Mandatory preflight

Run and record:

```powershell
git branch --show-current
git status --short
git log --oneline -n 8
git stash list
```

Verify work-package token:

```powershell
Test-Path automation_bus/state/work_package_active.json
```

Read `automation_bus/state/work_package_active.json` and confirm:

* `work_id` is `LC-S13`
* branch is `scaffold/lc-s13-lifestyle-coherence-narrative`

If token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

Confirm controlling docs exist:

```powershell
Test-Path docs/planning-papers/HealthIQ_AI_core_scaffold_completion_definition_v1.md
Test-Path docs/planning-papers/HealthIQ_AI_Core_Scaffold_Completion_Sprint_Plan_FINAL.md
```

If either is missing, STOP.

## Cross-sprint guard preflight

Before implementation, run prior scaffold / launch-core protections.

At minimum run the currently available equivalents of:

```powershell
python -m pytest backend/tests/regression/test_lc_s8f_phase_b_true_conversions.py -q
python -m pytest backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py -q
python -m pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q
python -m pytest backend/tests/regression/test_lc_s10b_launch_core_protection.py -q
python -m pytest backend/tests/regression/test_lc_s11a_trust_blocker_correction.py -q
```

If one of these files has a different current name, find the current equivalent and record the substitution.

If a prior scaffold/launch-core guard fails, STOP unless the failure is already documented as unrelated and GPT/human authority explicitly permits continuation.

Do not proceed while prior protected behaviours are broken.

## Q-1 / Q-2 questionnaire dependency check

Before touching questionnaire/lifestyle code, check whether Q-1/Q-2 questionnaire redesign work is active.

Search branch names, docs and recent logs for questionnaire redesign references.

If questionnaire input shape, field names, mapping, or frontend collection flow are actively changing, STOP and report.

Possible outcomes:

1. Q-1/Q-2 is already merged and stable — proceed.
2. Q-1/Q-2 is active but unrelated to backend mapped DTOs — proceed only using stable backend mapped inputs.
3. Q-1/Q-2 changes questionnaire shape/mapping — STOP for GPT/human decision.

Do not create parallel incompatible questionnaire assumptions.

---

# Scope A — Lifestyle propagation pathway

## Problem

The lifestyle/questionnaire layer appears to compute internally but produces little visible user payoff.

Previous audit work also found `lifestyle.confidence_adjustments` was uniformly `0.0` across contrasting lifestyle profiles. That means this may not be only an unwired-output problem; it may also be a dormant or broken computation path.

## Mandatory lifestyle computation preflight

Before wiring anything to user-facing output, trace the current lifestyle pathway:

```text
questionnaire input
→ mapped lifestyle factors
→ lifestyle modifier engine
→ confidence adjustments
→ lifestyle bridges
→ DTO/meta
→ user-visible surfaces
```

Answer explicitly:

1. Are questionnaire inputs received?
2. Are they mapped into stable lifestyle factors?
3. Are lifestyle modifiers computed?
4. Are `confidence_adjustments` ever non-zero?
5. Are lifestyle bridges firing?
6. Is alcohol / one-carbon / methylation bridge firing when expected?
7. Are outputs present in DTO/meta?
8. Which outputs are currently visible to the user?
9. Which outputs are computed but not surfaced?
10. Which outputs are absent because computation did not happen?

## STOP / split condition

If lifestyle modifiers and confidence adjustments are not computing meaningful internal outputs, Scope A must STOP.

Do not wire broken or meaningless values to the frontend.

If Scope A stops, report whether the work should split into:

```text
LC-S13A — Lifestyle computation repair
LC-S13B — Lifestyle surface propagation
```

Scopes B and C may only proceed if they are independent of the failed lifestyle computation path and GPT/human authority approves the split.

Cursor may not self-authorise this split.

## Required lifestyle behaviour

Same blood panel + different questionnaire profile must produce at least one governed, visible, explainable difference in the output.

Allowed user-visible effects:

* caveat
* confidence modifier
* explanation modifier
* lifestyle-context paragraph
* next-step priority
* supporting-context note

Not allowed:

* changing measured biomarker values
* overriding lab-derived ranges
* changing biomarker truth
* claiming causality without governed support
* generic wellness filler
* raw internal bridge code
* lifestyle advice unrelated to the panel

## Minimum fixture expectation

Use or create contrasting profiles for the same panel, for example:

```text
Profile A: low alcohol, no smoking, normal BMI, good sleep/activity
Profile B: moderate/high alcohol, smoking, high BMI, poor sleep/stress
```

Expected result:

At least one governed user-visible field differs in a clinically bounded way.

The sprint must prove:

```text
Lifestyle intelligence is computed.
Lifestyle intelligence is surfaced.
```

---

# Scope B — Coherence guard

## Problem

The rendered report has previously shown contradictions such as a domain card labelled stable/high confidence while the headline says “not a simple all-clear”.

This is a scaffold integrity issue, not product polish.

## Required coherence protections

Add deterministic tests and Sentinel entries protecting against:

* hero finding contradicting body overview
* domain band contradicting headline/consequence text
* stable card carrying warning copy without clear context
* strong / needs-review card lacking supporting evidence
* domain claiming active signals when none exist
* active concern copy without active signal
* raw signal IDs or governance tokens leaking into user-facing prose
* generic placeholder copy appearing in consumer report

Known defect class to protect:

```text
Card says Stable / High confidence while headline says “not a simple all-clear”.
```

## Required Sentinel defect classes

Add or update Sentinel entries for:

```text
domain_band_headline_polarity_contradiction
domain_active_signal_false_claim
governance_label_user_visible_leakage
```

These must point to deterministic regression tests, not status notes.

---

# Scope C — Narrative language audit

## Problem

Deterministic/mock-mode narrative may use first-person possessive language that implies AI-personalised interpretation beyond what the current deterministic scaffold actually provides.

## Required audit

Search static source strings and generated/runtime prose for:

```text
"your measured"
"your cardiovascular"
"your results"
"your report"
"your blood"
"your panel"
"AI-personalised"
"personalised narrative"
"personalized narrative"
```

Classify each hit as:

1. acceptable user-addressed explanatory language
2. deterministic template language that overclaims personalisation
3. internal governance/runtime label leaking to users
4. test/documentation-only usage

## Required behaviour

Remove or reframe deterministic template language that overclaims personalisation.

Do not remove useful patient-facing clarity merely because the word “your” appears. The issue is not second-person language by itself; the issue is implying personalised AI interpretation when the output is deterministic template prose.

Acceptable:

```text
Your uploaded panel includes...
```

Potentially unacceptable:

```text
Your measured homocysteine is the main lab anchor...
```

if presented as personalised AI-style reasoning without clear governance framing.

## Required Sentinel defect classes

Add or update Sentinel entries for:

```text
mock_mode_personalisation_overclaim
governance_label_user_visible_leakage
```

If no runtime user-facing defect remains, still add regression coverage proving the audited class stays clean.

---

# Potentially allowed files

Only edit what is necessary.

Potentially allowed backend:

```text
backend/core/analytics/**/*
backend/core/pipeline/**/*
backend/core/dto/**/*
backend/core/lifestyle/**/*
backend/core/questionnaire/**/*
backend/app/routes/analysis.py
backend/tests/unit/**/*
backend/tests/regression/**/*
```

Potentially allowed frontend:

```text
frontend/app/(app)/results/**/*
frontend/app/components/**/*
frontend/app/lib/**/*
frontend/app/types/**/*
frontend/tests/**/*
```

Potentially allowed Sentinel/docs:

```text
sentinel/packs/**/*
sentinel/**/*
docs/audit-papers/LC-S13_lifestyle_coherence_narrative_notes.md
```

## Forbidden unless GPT explicitly approves

```text
backend/ssot/biomarkers.yaml
backend/ssot/units.yaml
backend/ssot/scoring_policy.yaml
backend/core/units/registry.py
backend/core/scoring/rules.py
knowledge_bus/**/*
automation_bus/state/*
automation_bus/latest_gate_evidence.json
automation_bus/latest_gate_output.txt
automation_bus/latest_cursor_status.json
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
```

Do not modify unit conversion, scoring directionality, Knowledge Bus content, SSOT metadata, or Automation Bus scripts in this sprint.

If those appear necessary, STOP.

---

# Required tests

Add or update deterministic tests for:

## Lifestyle propagation

* contrasting questionnaire profiles produce a visible governed difference
* alcohol / one-carbon bridge appears in plain English when expected
* raw bridge rationale codes do not appear in user-facing prose
* lifestyle modifiers do not change measured biomarker values
* lifestyle modifiers do not override lab-derived reference ranges
* if confidence adjustment is expected, non-zero adjustment is visible and explainable
* if confidence adjustment is not expected, absence is explicitly justified

## Coherence

* stable domain card does not carry warning headline copy unless clearly contextualised
* no active concern text appears without active signal
* no domain claims active signals when none exist
* hero/body/domain sections agree on lead finding polarity
* no generic placeholder consumer copy appears

## Narrative language

* no mock-mode personalisation overclaim appears in user-facing text
* no internal governance labels appear in rendered consumer prose
* no raw signal IDs appear in user-facing sections

## Regression preservation

* LC-S8F/G unit and display fidelity still passes
* LC-S11A trust blockers remain fixed
* homocysteine lead finding remains intact
* uploaded-panel fidelity remains intact
* no frontend conversion maths introduced

---

# Required Sentinel / test harness obligations

Sentinel update is required.

At minimum add/update defect classes:

```text
lifestyle_visible_payoff_missing
lifestyle_bridge_internal_code_leakage
domain_band_headline_polarity_contradiction
domain_active_signal_false_claim
mock_mode_personalisation_overclaim
governance_label_user_visible_leakage
```

Each must point to an active deterministic regression test.

Do not add placeholder Sentinel entries.

If a defect class cannot yet be fully guarded, document why and add the strongest available deterministic guard.

---

# Required validation commands

Run relevant targeted tests.

At minimum:

```powershell
python -m pytest backend/tests/regression/test_lc_s8f_phase_b_true_conversions.py -q
python -m pytest backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py -q
python -m pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q
python -m pytest backend/tests/regression/test_lc_s10b_launch_core_protection.py -q
python -m pytest backend/tests/regression/test_lc_s11a_trust_blocker_correction.py -q
```

Run the new LC-S13 regression test explicitly, for example:

```powershell
python -m pytest backend/tests/regression/test_lc_s13_lifestyle_coherence_narrative.py -q
```

If frontend files changed:

```powershell
npm run type-check
npm run test
```

If Playwright/e2e files are added or changed, run the relevant Playwright command and record exact output.

If any required existing test file name differs, find and run the current equivalent, then record the substitution.

---

# Human/UAT check

If implementation reaches frontend-visible output, generate or reuse two equivalent analyses:

1. Same blood panel with low-risk lifestyle profile
2. Same blood panel with higher-risk lifestyle profile

Check rendered output:

* at least one user-visible governed lifestyle difference appears
* no raw internal bridge code appears
* homocysteine lead remains coherent where applicable
* no stable/warning contradiction appears
* no mock-mode overclaim appears
* no internal governance label appears
* no unit/display regression appears

If browser-based UAT cannot be completed, document that and provide the exact API/DTO evidence instead. Do not claim frontend UAT passed unless it was actually inspected.

---

# Acceptance criteria

This sprint is complete only if:

* lifestyle computation path is proven or the sprint correctly STOPs/splits
* lifestyle surface propagation is implemented only if internal computation is meaningful
* same panel + different lifestyle profile produces a governed visible difference
* raw lifestyle bridge codes do not appear in consumer prose
* report coherence defects are regression/Sentinel guarded
* deterministic/mock-mode narrative overclaim is audited and corrected/protected
* prior scaffold/launch-core guards still pass
* new Sentinel entries are active and deterministic
* documentation note clearly records findings and residual risks
* no forbidden files are touched
* no unit/scoring/Knowledge Bus work is smuggled into this sprint

---

# Closure requirements

When complete:

1. Run:

```powershell
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

```powershell
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
