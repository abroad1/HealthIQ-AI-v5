---
work_id: INTERNAL-UAT-RESULTS-TRUST-HARDENING-1_high_trust_results_page_coherence
branch: work/INTERNAL-UAT-RESULTS-TRUST-HARDENING-1-high-trust-results-page-coherence
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# INTERNAL-UAT-RESULTS-TRUST-HARDENING-1 — High-Trust Results Page Coherence

## Purpose

Fix the six HIGH trust/coherence defects found during internal UAT of the working HealthIQ results page.

This sprint follows the successful result-versioning fix. The page now loads correctly, the API returns `compatible: true`, `clinician_report_v1` is present, and the stale/incompatible banner is absent.

The purpose of this sprint is therefore not structural compatibility.

The purpose is:

```text id="6dbhzp"
Make the working results page more coherent, trustworthy, clinically cautious and understandable by fixing the HIGH issues identified in the internal UAT audit.
```

This is an internal validation hardening sprint only.

Do not frame this as beta readiness, external launch readiness, or consumer release readiness.

---

## Strategic framing

The current result page is structurally working but not yet retail-quality.

The UAT audit found:

```text id="ve3ux2"
BLOCKER: 0
HIGH: 6
MEDIUM: 6
LOW: 3
```

This sprint must fix the six HIGH items only.

Do not chase MEDIUM/LOW polish unless it is directly necessary to fix one of the HIGH items safely.

---

## Governance classification

This work is:

```yaml id="jtwmlb"
risk_level: HIGH
change_type: BEHAVIOUR
execution_model: TWO_PHASE_START_FINISH
```

Rationale:

```text id="9x8jgd"
- may touch backend output-generation / report compiler semantics
- may touch frontend result rendering copy
- affects user-facing interpretation hierarchy
- affects trust, clinical caution and apparent meaning of results
- must preserve frontend render-only boundaries
```

Required route:

```text id="9yxgmd"
Cursor implementation
Claude audit
GPT architectural review
Human approval before merge
```

Do not merge.

---

## Required branch

Work only on:

```text id="wtockn"
work/INTERNAL-UAT-RESULTS-TRUST-HARDENING-1-high-trust-results-page-coherence
```

Do not work on `main`.

Do not merge.

---

## Authoritative inputs

Read before editing:

```text id="q8t384"
docs/testing/INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_6bcbf1de_2026-06-16.md
automation_bus/_uat_6bcbf1de_result_api.json
docs/testing/screenshots/uat_6bcbf1de_results_page/
```

Also inspect, but do not treat as new authority unless needed for regression context:

```text id="b76v1p"
docs/testing/INVESTIGATION_fdf9bc74_result_versioning_false_incompatible_2026-06-16.md
docs/audit-papers/INTERNAL-UAT-RESULT-VERSIONING-1_dto_render_contract_compatibility_fix.md
```

The standard Automation Bus and Knowledge Bus SOPs already apply. Do not add unnecessary SOP files to the read-list unless required by a validator.

---

## Baseline evidence

The audit result to preserve:

```text id="w8ibvq"
analysis_id: 6bcbf1de-d97f-4a1c-9556-e3a6e0625fd1
GET /api/analysis/result: HTTP 200
result_versioning.compatible: true
result_status: current
render_blockers: []
stale_reasons: []
clinician_report_v1: present and populated
narrative_report_v1: present
interpretation_display_layer_v1: present
consumer_domain_scores: present
clusters: 3
biomarkers: 79
stale/incompatible banner: absent
regenerate CTA: absent
```

This must remain true after the sprint.

---

## HIGH issues in scope

Fix only these six HIGH issues.

### IUAT-001 — B12-associated heading mismatch

Problem:

```text id="uvz4a0"
The Primary Finding and Why section displays “B12-associated pattern”, but the evidence says B12 is in range and pulls against a B12-driven explanation.
```

Required outcome:

```text id="9aw3xw"
The heading must not imply B12 causality or abnormality when B12 is in range and counter-evidence is present.
```

Acceptable fix direction:

```text id="93m3d8"
Use a more neutral title such as:
- “Raised homocysteine context”
- “Homocysteine-related pattern”
- “One-carbon / homocysteine context”
```

Do not hardcode this only in the frontend if the API/compiler is producing an over-assertive hypothesis title. Prefer fixing the producer if the title comes from `clinician_report_v1`.

Do not make new medical claims.

Do not suppress the B12 counter-evidence. The counter-evidence is useful and should remain visible.

---

### IUAT-002 — Pattern-groups placeholder copy

Problem:

```text id="cf3yjy"
The UI says “Pattern groups are not available for this result yet…” even though the API contains 3 clusters.
```

Required outcome:

```text id="ee6etr"
The page must not say pattern groups are unavailable when clusters exist.
```

Acceptable fix direction:

```text id="vt7v25"
If detailed pattern buckets are intentionally hidden by default, say that clearly.

Example:
“Detailed pattern groups are hidden in this view. The main pattern summary is shown above.”

or:
“Pattern summaries are available in the result narrative. Detailed buckets can be shown in technical detail.”
```

Do not expose technical buckets by default unless that is already intended.

Do not create fake pattern groups.

Do not calculate new pattern groups in the frontend.

---

### IUAT-003 — 79 markers vs 9/9 expected markers wording

Problem:

```text id="mlfy1t"
The toolbar says 79 markers, while data quality says “We received 9 of 9 expected markers for this interpretation”. To a normal user, this looks contradictory.
```

Required outcome:

```text id="907hfw"
The page must clearly distinguish:
- total uploaded/result biomarkers
- key markers used for this interpretation or headline completeness
```

Acceptable fix direction:

```text id="d3h7ma"
Toolbar:
“79 uploaded markers”

Data quality:
“9 of 9 key markers available for this headline interpretation”

or:
“Your panel contains 79 uploaded markers. For this specific interpretation, all 9 key markers were available.”
```

Do not change completeness calculation unless a defect proves the existing numerator/denominator are wrong.

Do not calculate clinical completeness in the frontend.

Frontend may render clearer labels using existing DTO fields.

---

### IUAT-004 — Markdown/internal system wording leakage in body overview

Problem:

```text id="7o0izx"
Body overview displays raw markdown/internal wording such as:
**Cardiovascular 4 Biomarkers**
and phrases like “analytical model”.
```

Required outcome:

```text id="g92t2v"
Consumer-facing prose must not expose markdown syntax, internal system names, engineering language, slugs, or model vocabulary.
```

Acceptable fix direction:

```text id="ii8dgi"
- Strip markdown markers before rendering, if markdown is not intentionally supported.
- Map internal system labels to consumer-safe labels.
- Replace “analytical model” with user-facing wording such as “interpretation” or “health summary”.
```

Prefer fixing this at the output/compiler/scrubber layer if the API is producing the text.

Frontend sanitisation is acceptable only for display-format markdown cleanup, not for changing medical meaning.

Do not introduce markdown rendering if that would create XSS/security risk.

---

### IUAT-005 — Homocysteine hierarchy vs vascular inflammation framing

Problem:

```text id="di7snj"
Hero correctly leads with raised homocysteine, but the subline says “Most relevant area: Vascular Inflammation Risk”. The page then moves between homocysteine, B12, methylation and vascular language without a clear hierarchy.
```

Required outcome:

```text id="3j1yuj"
The page must make the hierarchy clear:
primary finding = raised homocysteine pattern
broader system context = cardiovascular/vascular risk context
possible explanatory context = methylation / one-carbon / B-vitamin context, expressed cautiously
```

Acceptable fix direction:

```text id="qrgwgh"
Adjust hero/subline wording so it explains the relationship.

Example:
“Primary finding: raised homocysteine pattern”
“Relevant system context: cardiovascular / vascular risk context”

or:
“Raised homocysteine is the lead finding; the broader affected system is cardiovascular risk.”
```

Do not change scoring, signal activation or domain ranking.

Do not relabel the medical signal unless the current output is demonstrably wrong.

This is hierarchy/copy alignment, not a clinical scoring sprint.

---

### IUAT-006 — Transferrin “Critical” presentation

Problem:

```text id="9yk5mh"
Transferrin 2.0 g/L is below the lab range 2.15–3.65 and is therefore lab-grounded as low, but the retail label “Critical” appears too alarmist in the driver band, especially with ferritin in range.
```

Required outcome:

```text id="klw1ib"
The page must not present a mildly low lab-grounded value in a disproportionately alarming way unless the backend status/severity model explicitly justifies it.
```

Required investigation before fixing:

```text id="zstr51"
Determine whether “critical” comes from:
- lab status mapping
- backend biomarker DTO severity
- frontend badge mapping
- driver-band display logic
- generic abnormality tier naming
```

Acceptable fix direction:

```text id="5x5sji"
If the value is simply below range, use a less alarmist consumer label such as:
- Low
- Below range
- Needs review
```

Important boundary:

```text id="vgkt4t"
The frontend may render a consumer-safe label from an existing backend status, but must not independently infer clinical severity.
```

If changing the backend severity mapping is required, STOP and report before implementation unless the mapping defect is local, obvious and fully covered by tests.

Do not alter lab ranges.

Do not suppress transferrin if it is legitimately part of the driver set.

---

## Non-goals

Do not fix these in this sprint unless directly required by the HIGH issues:

```text id="r9003f"
- raw marker display names such as dhea s, Apob Apoa1 Ratio, (venous)
- governance strip wording
- page length / information architecture
- next-step grammar polish
- blood sugar 100/100 with limited reliability wording
- free testosterone % score edge
- minor layout or duplicate heading polish
```

Create or preserve carry-forward entries for these where appropriate.

---

## Non-negotiable constraints

Do not:

```text id="07rr0l"
- change parser behaviour
- introduce fallback or dummy parser logic
- change biomarker intelligence
- change signal activation or deactivation
- change active signal context gates
- change scoring logic unless explicitly approved
- change lab reference range handling
- introduce global/default reference ranges where lab ranges exist
- change result versioning / compatibility logic
- hide stale/incompatible warnings
- introduce dummy clinician_report_v1 content
- introduce raw Pass 3 or investigation-spec runtime reads
- let frontend infer clinical meaning
- let frontend calculate abnormality
- let frontend determine clinical severity independently
- remove uncertainty/caution language
- introduce diagnosis or treatment recommendations
- make alarmist claims
```

Frontend remains render-only.

Backend/output compiler remains the source of clinical wording and hierarchy.

---

## Authority preflight

Before editing, run and report:

```powershell id="d8mvjg"
git branch --show-current
git status --short
git rev-parse HEAD
git log --oneline -n 10
```

Confirm:

```text id="l2d1vw"
1. Current branch is work/INTERNAL-UAT-RESULTS-TRUST-HARDENING-1-high-trust-results-page-coherence.
2. Working tree is clean.
3. INTERNAL-UAT-RESULT-VERSIONING-1 is merged into main.
4. Fresh result compatibility is currently passing.
5. The UAT audit file exists.
6. The API snapshot exists.
7. The six HIGH issues can be reproduced from current API/UI evidence.
```

STOP if the baseline cannot be reproduced.

---

## Phase 1 — Source tracing

Before implementing, trace each HIGH issue to its likely producer.

For each IUAT issue, document:

```text id="7t6wky"
- visible UI text
- API field
- frontend component
- backend producer, if applicable
- whether the defect is frontend copy, frontend mapping, backend compiler output, scrubber gap, DTO issue, or severity/status mapping
- proposed smallest safe fix
```

Likely files to inspect:

```text id="qhmoyn"
frontend/app/(app)/results/page.tsx
frontend/components/results/**
frontend/components/**
backend/core/dto/builders.py
backend/core/analytics/report_compiler_v1.py
backend/core/analytics/**
backend/core/dto/frontend_contract_v1.py
backend/app/routes/analysis.py
```

Search for strings:

```text id="1puznr"
"B12-associated"
"Pattern groups are not available"
"expected markers"
"Cardiovascular 4 Biomarkers"
"analytical model"
"Vascular Inflammation Risk"
"Critical"
"transferrin"
```

STOP if a HIGH issue requires clinical scoring changes or signal activation changes.

---

## Phase 2 — Implement targeted fixes

Implement the smallest safe fixes for IUAT-001 to IUAT-006.

Preferred fix strategy:

```text id="f6dqv5"
- Fix backend/compiler text where the API produces misleading clinical wording.
- Fix frontend copy where the frontend is merely labelling or explaining existing DTO fields.
- Keep frontend render-only.
- Keep DTO contract stable unless a small additive non-breaking field is needed.
```

Do not implement broad refactors.

Do not redesign the page.

Do not fix MEDIUM/LOW issues unless they are touched naturally by the HIGH fix.

---

## Phase 3 — Tests

Add or update tests to prevent recurrence.

Minimum required tests:

### For IUAT-001

Test that when B12 is in range and appears as counter-evidence, the rendered/API hypothesis title does not assert a B12-driven pattern.

Expected:

```text id="l0t2bz"
No “B12-associated pattern” title where B12 is counter-evidence.
Neutral homocysteine/one-carbon wording is used.
Counter-evidence remains visible.
```

### For IUAT-002

Test that when clusters exist but detailed pattern buckets are hidden, the UI/copy does not say pattern groups are unavailable.

Expected:

```text id="vqbff3"
clusters.length > 0
showPatternGroupBuckets = false
copy does not contain “not available”
copy honestly indicates hidden/summary mode
```

### For IUAT-003

Test marker-count wording distinguishes uploaded markers from key/headline markers.

Expected:

```text id="z1mjfm"
79 uploaded markers
9 of 9 key markers for this interpretation/headline completeness
No apparent contradiction
```

### For IUAT-004

Test body overview output/rendering does not expose:

```text id="lqxfuo"
**
Cardiovascular 4 Biomarkers
analytical model
mojibake replacement character
internal slugs
```

### For IUAT-005

Test hero/subline hierarchy makes the relationship clear:

```text id="wzut8q"
primary finding: raised homocysteine
broader system context: cardiovascular/vascular context
no contradictory or competing lead labels
```

### For IUAT-006

Test transferrin or below-range driver label is not displayed as “Critical” in consumer driver band unless backend status explicitly requires a critical consumer label.

Expected:

```text id="qnh8i0"
Low / Below range / Needs review is acceptable.
Critical is not acceptable for this lab-grounded mildly-low transferrin scenario unless justified by backend severity policy.
```

Test level:

```text id="zpntqg"
Use the smallest reliable combination of unit, regression and component tests.
Do not rely only on manual visual inspection.
```

---

## Phase 4 — Re-run internal UAT evidence

After implementation and tests, re-run the audit against:

```text id="q7sqbt"
1. existing analysis_id: 6bcbf1de-d97f-4a1c-9556-e3a6e0625fd1
2. one brand-new upload/result if practical
```

For both, confirm:

```text id="p2bqba"
result_versioning.compatible: true
result_status: current
render_blockers: []
stale_reasons: []
clinician_report_v1 present
stale/incompatible banner absent
regenerate CTA absent
```

Then check the six HIGH fixes.

---

## Phase 5 — Carry-forward register

Update the carry-forward register.

Close or mark resolved:

```text id="eekrda"
IUAT-001
IUAT-002
IUAT-003
IUAT-004
IUAT-005
IUAT-006
```

Open or preserve separate carry-forwards for deferred items:

```text id="91mse2"
- raw marker display-name normalisation
- governance strip retail wording
- page-length / progressive disclosure
- next-step grammar polish
- blood sugar score/reliability explanatory bridge
- free testosterone % score display edge
```

Do not silently drop deferred issues.

---

## Phase 6 — Required validation

Run and paste full output.

Architecture and governance:

```powershell id="0287xt"
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_day_one_architecture.py
python backend/scripts/validate_day_one_launch_estate_gate.py
python backend/scripts/validate_active_signal_context_gate_reachability.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

Backend tests:

```powershell id="8zuqrs"
python -m pytest backend/tests/regression/test_internal_uat_result_versioning_dto_contract.py -q
python -m pytest backend/tests/regression/test_active_signal_context_gate_reachability.py -q
python -m pytest backend/tests/regression/test_dhea_s_high_activation.py -q
```

Run any new or updated tests for:

```text id="gmot2e"
- report compiler hypothesis titles
- body overview scrubber
- result copy / marker count
- pattern groups placeholder
- driver severity label
- hero hierarchy
```

Frontend tests:

```powershell id="slbwza"
npm test -- --runInBand
npm run lint
npm run build
```

If the repo uses different frontend commands, discover and run the appropriate existing equivalents. Report the exact commands used.

Secret-file guardrail, if present:

```powershell id="ke3mvc"
python scripts/check_no_secret_files.py
```

---

## Phase 7 — Required audit paper

Create:

```text id="4ooxrl"
docs/audit-papers/INTERNAL-UAT-RESULTS-TRUST-HARDENING-1_high_trust_results_page_coherence.md
```

The audit paper must include:

```text id="tiwlpa"
- executive verdict
- baseline UAT summary
- files inspected
- files changed
- issue-by-issue source tracing for IUAT-001 to IUAT-006
- before/after screenshots or text evidence
- before/after API evidence where applicable
- explanation of why frontend remains render-only
- explanation of why parser/intelligence/signal/scoring/versioning were not changed
- confirmation lab-provided ranges remain authoritative
- confirmation no global/default ranges were introduced
- confirmation no dummy/fallback content was introduced
- confirmation no stale/incompatible warning was hidden or bypassed
- confirmation true result_versioning remains current for compatible result
- confirmation true render blockers would still surface
- full validator output
- full backend test output
- full frontend test/lint/build output
- carry-forward updates
- rollback path
- recommended next action
```

Do not summarise test output. Paste full relevant output.

---

## Phase 8 — Git evidence

Before commit, report:

```powershell id="9lccgj"
git branch --show-current
git status --short
git diff --name-only
git diff --stat
```

Expected commit message:

```text id="xslte7"
fix(results): harden high-trust result page copy and hierarchy
```

After commit, report:

```powershell id="d5561d"
git status --short
git log --oneline -n 5
git diff --name-only main...HEAD
```

Run:

```powershell id="qzblxt"
python backend/scripts/run_work_package.py finish
```

Return final gate evidence.

Do not merge.

---

## Expected changed files

Likely changed files include some of:

```text id="leessx"
backend/core/analytics/report_compiler_v1.py
backend/core/analytics/narrative_report_compiler_v1.py
backend/core/dto/builders.py

frontend/app/(app)/results/page.tsx
frontend/components/results/ResultsBodyOverview.tsx
frontend/components/results/PrimaryFindingAndWhy.tsx
frontend/components/results/PipelineStatus.tsx
frontend/components/results/*
```

Likely tests:

```text id="c7qyor"
backend/tests/regression/*
backend/tests/unit/*
frontend tests for results components, if present
```

Governance/audit files:

```text id="jr6w72"
docs/sprints/launch_core_carry_forward_register.md
docs/audit-papers/INTERNAL-UAT-RESULTS-TRUST-HARDENING-1_high_trust_results_page_coherence.md
```

Do not touch unless justified:

```text id="gu98r9"
parser files
signal library YAML
runtime context evaluator
signal evaluator
scoring core
result versioning compatibility logic
medical frame identity index
reference range logic
```

---

## STOP conditions

STOP and report if:

```text id="nqbpn6"
1. Any HIGH issue cannot be reproduced.
2. Fixing any issue requires changing signal activation/deactivation.
3. Fixing any issue requires changing clinical scoring logic.
4. Fixing any issue requires changing lab reference range interpretation.
5. Fixing any issue requires frontend clinical inference.
6. Fixing transferrin “Critical” requires a new medical severity policy decision.
7. Fixing B12 wording requires new medical authority beyond cautious title neutralisation.
8. Versioning compatibility regresses.
9. clinician_report_v1 disappears or becomes dummy/fallback content.
10. stale/incompatible warnings are hidden or bypassed.
11. parser behaviour changes.
12. raw Pass 3 or investigation-spec runtime reads are introduced.
13. frontend build/lint/tests fail.
14. backend tests or validators fail.
15. secret guardrail fails.
16. rollback path is unclear.
```

Do not perform ad hoc remediation outside scope.

---

## Success criteria

This sprint succeeds only if:

```text id="1g93gs"
- all six HIGH issues are fixed or explicitly STOP-gated with evidence
- no BLOCKER or new HIGH issue is introduced
- results page remains structurally working
- result_versioning remains compatible/current
- clinician_report_v1 remains present and real
- stale/incompatible banner remains absent for current compatible result
- true stale/incompatible protections are not weakened
- frontend remains render-only
- parser/intelligence/signal/scoring/versioning remain unchanged
- lab ranges remain authoritative
- no global/default ranges are introduced
- no dummy/fallback content is introduced
- validators pass
- backend tests pass
- frontend tests/lint/build pass
- audit paper contains before/after evidence
```

Expected next action after success:

```text id="tuqkiq"
Claude audit
GPT architectural review
Human approval
Merge

Then rerun the full internal UAT checklist on:
1. existing 6bcbf1de result
2. one new upload/result
```
