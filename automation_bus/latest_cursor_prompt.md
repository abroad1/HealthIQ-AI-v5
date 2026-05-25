---
work_id: MAP-R1A
branch: mapping/map-r1a-star-suffix-canonical-fix
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# MAP-R1A — Star-Suffix Canonical Mapping Fix

## Classification

This is a HIGH-risk BEHAVIOUR sprint.

Reason: this sprint changes canonical biomarker mapping behaviour in the upload/analysis path. It affects whether uploaded markers enter the scored biomarker set, signal evaluation, root-cause selection, narrative generation and frontend results.

This is not a frontend UX sprint.  
This is not KB-WAVE-1.  
This is not PATTERN-C1.  
This is not a Knowledge Bus content sprint.  
This is not a scoring policy sprint.  
This is not a unit conversion sprint.  
This is not a Gemini/LLM sprint.

## Purpose

Fix the proven canonical marker mapping failure caused by trailing lab abnormal markers such as `*` in extracted biomarker names.

The MAP-R1 investigation proved that labels such as:

```text
Homocysteine (venous)*
Apolipoprotein B (venous)*
Lipoprotein (a) (venous)*
````

fall through as `unmapped_*` because the trailing `*` prevents specimen suffix stripping. This caused the d8 fresh UAT run to score 63 biomarkers instead of 77 and changed the lead finding from Homocysteine-led to Total Cholesterol-led.

The goal is:

```text
Known biomarkers with trailing abnormal markers must resolve to their canonical IDs before scoring and signal evaluation.
```

## Controlling authority

Read before doing anything:

```text
docs/audit-papers/MAP-R1_fresh_upload_canonical_mapping_regression_investigation.md
docs/audit-papers/Post-FE-R6A_Fresh_UAT_Investigation_d8cfe1a8.md
docs/audit-papers/FE-R6A_fresh_uat_defect_cleanup_notes.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
```

Also inspect if present:

```text
docs/audit-papers/LC-S8G_uploaded_unit_display_fidelity_notes.md
docs/audit-papers/LC-S16_knowledge_asset_frontend_surface_audit.md
docs/audit-papers/LC-S20_22_persisted_replay_sentinel_phase2_notes.md
```

If the MAP-R1 investigation report is missing, STOP.

## Required output documentation

Create:

```text
docs/audit-papers/MAP-R1A_star_suffix_canonical_mapping_fix_notes.md
```

This document must include:

1. preflight results
2. MAP-R1 root-cause summary
3. exact mapping fix implemented
4. frontend defence-in-depth implemented, if any
5. affected markers tested
6. before/after alias examples
7. whether scored biomarker count is restored for the d8 fixture/input
8. signal/arbitration impact
9. tests added/updated
10. Sentinel updates
11. residual risks
12. explicit recommendation on KB-WAVE-1 readiness

## Mandatory preflight

Run and record:

```powershell
git branch --show-current
git status --short
git log --oneline -n 12
git stash list
```

Verify work-package token:

```powershell
Test-Path automation_bus/state/work_package_active.json
```

Read `automation_bus/state/work_package_active.json` and confirm:

* `work_id` is `MAP-R1A`
* branch is `mapping/map-r1a-star-suffix-canonical-fix`

If token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

## Cross-sprint guard preflight

Run current relevant guards before implementation:

```powershell
python -m pytest backend/tests/regression/test_fe_r1_consumer_prose_cleanup.py -q
python -m pytest backend/tests/regression/test_fe_r6a_fresh_uat_defect_cleanup.py -q
python -m pytest backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py -q
python -m pytest backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

If a guard fails, STOP unless GPT/human explicitly authorises continuation.

## Proven root cause

The MAP-R1 investigation proved:

```text
Homocysteine (venous)* → homocysteine_(venous)* → unmapped_homocysteine_(venous)*
```

Correct behaviour should be:

```text
Homocysteine (venous)* → Homocysteine (venous) → homocysteine
```

The failure occurs because:

* frontend `analysisBiomarkerKey()` does not strip trailing `*`
* backend alias resolver does not strip trailing abnormal markers before suffix stripping
* `_strip_surrounding_punctuation()` can strip `*` and then strip `)`, producing a truncated key such as `homocysteine_(venous`
* `_strip_specimen_suffix()` cannot match `_(venous)` when the key ends in `*`

## Required implementation

### A. Backend canonical alias fix

Implement a small, deterministic fix in:

```text
backend/core/canonical/alias_registry_service.py
```

Expected behaviour:

* strip trailing lab abnormal markers before alias lookup and specimen suffix stripping
* at minimum support trailing `*`
* preferably support common abnormal-marker suffixes such as `†`
* be careful with `H` / `L`: only strip if clearly appended as a lab abnormal marker, not if part of the biomarker name

Safe examples that must resolve:

```text
Homocysteine (venous)*
Apolipoprotein B (venous)*
Apolipoprotein A1 (venous)*
Lipoprotein (a) (venous)*
Corrected Calcium (venous)*
TSH (venous)*
```

Do not weaken alias matching in a way that creates false positives.

### B. Frontend defence-in-depth

Implement defence-in-depth in:

```text
frontend/app/lib/uploadReferenceRange.ts
```

Specifically, update `analysisBiomarkerKey()` so trailing lab abnormal markers are stripped before lowercasing / underscore conversion.

This does not replace the backend fix. Backend must remain authoritative.

### C. Do not modify scoring policy

Do not change scoring thresholds, severity labels, unit conversion, clinical interpretation, Knowledge Bus assets, or root-cause rules.

This sprint is mapping only.

## Affected markers that must be tested

At minimum, tests must cover:

```text
Homocysteine (venous)*
Creatinine (venous)*
TSH (venous)*
Vitamin B12 (venous)*
Active Vitamin B12 (venous)*
Apolipoprotein A1 (venous)*
Apolipoprotein B (venous)*
Apolipoprotein Ratio (venous)*
Lipoprotein (a) (venous)*
Corrected Calcium (venous)*
Vitamin D (venous)*
Zinc (venous)*
Non HDL Cholesterol Calculation (venous)*
Total Cholesterol/HDL Ratio Calculation (venous)*
```

Expected canonical IDs:

```text
homocysteine
creatinine
tsh
vitamin_b12
active_b12
apoa1
apob
apob_apoa1_ratio
lipoprotein_a
corrected_calcium
vitamin_d
zinc
non_hdl_cholesterol
tc_hdl_ratio
```

Also test clean labels without `*` still resolve exactly as before.

## Required tests

Add or update deterministic tests for:

### Backend alias resolution

* `resolve("Homocysteine (venous)*") == "homocysteine"`
* all affected marker examples above resolve to expected canonical IDs
* same labels without `*` still resolve
* specimen suffix stripping still works
* `*` stripping does not produce truncated keys such as `homocysteine_(venous`
* unknown markers with `*` remain unmapped safely

### Frontend key generation

* `analysisBiomarkerKey("Homocysteine (venous)*") == "homocysteine_(venous)"`
* same for representative ApoB/ApoA1/Lp(a)/Corrected Calcium examples
* clean labels still generate unchanged keys

### Integration / regression fixture

Create a deterministic fixture or test from the d8-style input keys proving:

* Group A affected markers no longer become `unmapped_*`
* Homocysteine enters the canonical/scored biomarker path
* ApoB, ApoA1 and Lipoprotein(a) resolve
* Creatinine resolves so dependent derived ratio logic can run where applicable
* existing f2 clean-label path still passes

If full end-to-end scored biomarker count restoration is too large for this sprint, document why and prove alias/canonical resolution at the lowest deterministic layer.

### Regression preservation

* uploaded unit display fidelity still passes
* FE-R6A fresh UAT retail guards still pass
* LC-S16/17/19 DTO surface guards still pass
* LC-S20/22 persisted replay guards still pass

## Required Sentinel obligations

Add or update Sentinel defect class:

```text
canonical_mapping_star_suffix_failure
```

It must point to an active deterministic test.

If more specific classes are useful, allowed examples:

```text
canonical_mapping_abnormal_marker_suffix_failure
canonical_mapping_specimen_suffix_truncation
canonical_mapping_known_marker_unmapped_after_star_suffix
```

No placeholder Sentinel entries.

## Potentially allowed files

```text
backend/core/canonical/alias_registry_service.py
frontend/app/lib/uploadReferenceRange.ts
backend/tests/unit/**/*
backend/tests/regression/**/*
frontend/tests/**/*
sentinel/packs/**/*
docs/audit-papers/MAP-R1A_star_suffix_canonical_mapping_fix_notes.md
```

If existing alias tests live elsewhere, update the correct existing test file.

## Forbidden unless GPT explicitly approves

```text
backend/core/scoring/**/*
backend/core/units/**/*
backend/core/pipeline/**/*
backend/core/analytics/**/*
backend/core/dto/**/*
backend/ssot/**/*
knowledge_bus/**/*
Gemini / LLM activation
KB-WAVE-1 content expansion
PATTERN-C1 backend/content contract work
frontend results-page UX changes
automation_bus/state/*
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
```

Do not edit Knowledge Bus medical content.

Do not alter root-cause, arbitration, signal ranking, or clinical scoring.

If implementation requires touching forbidden paths, STOP and report.

## Required validation commands

Run:

```powershell
python -m pytest backend/tests/unit/test_alias_service_star_suffix_stripping.py -q
python -m pytest backend/tests/regression/test_canonical_mapping_star_suffix_failure.py -q
python -m pytest backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py -q
python -m pytest backend/tests/regression/test_fe_r6a_fresh_uat_defect_cleanup.py -q
python -m pytest backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

If frontend file changed:

```powershell
npm run type-check
```

If frontend tests exist for `uploadReferenceRange.ts`, run/update them.

## Optional manual verification

If practical, run the same d8-style upload input through the analysis path and confirm:

* Homocysteine is mapped/scored
* ApoB/ApoA1/Lp(a) are mapped/scored
* scored biomarker count increases compared with the broken d8 result
* homocysteine signals can fire again when the value is present
* lead finding becomes analytically plausible for the full marker set

Do not claim this verification if not actually run.

## Acceptance criteria

Complete only if:

* backend alias resolver strips trailing abnormal markers before specimen suffix resolution
* frontend `analysisBiomarkerKey()` strips trailing abnormal markers as defence-in-depth
* all listed affected markers resolve to expected canonical IDs
* clean labels without `*` still resolve
* unknown starred labels remain safely unmapped
* no scoring/unit/root-cause/Knowledge Bus logic is changed
* uploaded display fidelity remains intact
* Sentinel guard is active and deterministic
* MAP-R1A notes document whether KB-WAVE-1 remains blocked or can proceed after merge

## Closure requirements

Before finish, run:

```powershell
git branch --show-current
git status --short
git diff --name-only
git log --oneline -n 8
git stash list
```

Then run:

```powershell
python backend/scripts/run_work_package.py finish
```

After finish, follow SOP v1.3.1:

* if `automation_bus/latest_cursor_status.json` is the only dirty file and shows kernel-generated COMPLETE status for `MAP-R1A`, commit it automatically as:
  `chore(bus): MAP-R1A kernel COMPLETE status`
* if any other Automation Bus artefact is dirty, STOP and escalate

Do not merge.

Do not claim KB-WAVE-1 authorisation.

## Cursor completion statement

Cursor implements canonical mapping fix only.

Cursor may not self-certify clinical correctness, KB-WAVE-1 readiness, merge readiness, or permission to begin the next sprint.

```
```
