---
work_id: MED-REV-2_wave1_domain_card_copy_alignment_and_result_regeneration_ux
branch: work/MED-REV-2-wave1-domain-card-copy-alignment-and-result-regeneration-ux
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# MED-REV-2 — Wave 1 Domain Card Copy Alignment and Result Regeneration UX

## Purpose

Resolve the post-MED-REV-1 mismatch between the visible Wave 1 subsystem model and the domain-card prose, while adding a safe regeneration UX so stale/incompatible test results can be regenerated using the latest engine without re-uploading the panel.

This sprint has two tracks:

```text
Track A — Wave 1 domain card copy alignment
Track B — Versioned result regeneration UX
````

Both tracks must preserve HealthIQ’s deterministic and auditable result model.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
ARCH-RT programme fully merged through ARCH-RT-6
LAUNCH-CORE-5 merged
MED-REV-1 merged
LAUNCH-CORE-3 result versioning policy merged
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

* current branch is not `main`
* local `main` does not equal `origin/main`
* working tree is not clean
* MED-REV-1 is not merged
* LAUNCH-CORE-3 is not merged
* untracked or uncommitted files are present

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint may touch user-facing medical prose, domain-card DTO assembly, result-versioning API behaviour, frontend stale/incompatible result UX, and tests. It affects product trust, auditability and user-facing interpretation.

## Standard rules

This work remains governed by the standard Knowledge Bus and Automation Bus SOPs already active in the repository.

Do not re-read SOPs unless the applicable governance requirement cannot be located.

## Authoritative inputs

Read these sprint-specific files before making changes:

```text
docs/audit-papers/MED-REV-1_wave1_subsystem_visibility_and_label_alignment_report.md
docs/audit-papers/healthiq_wave1_health_systems_subsystem_medical_review.md
docs/audit-papers/PROGRAMME-STATUS-1_healthiq_launch_workstream_consolidation_audit.md
docs/architecture/LAUNCH-CORE-3_result_versioning_replay_and_regeneration_policy.md
docs/audit-papers/LAUNCH-CORE-3_result_versioning_replay_and_regeneration_audit.md
docs/audit-papers/LAUNCH-CORE-5_results_page_narrative_hierarchy_and_score_rationalisation_report.md
docs/audit-papers/ARCH-RT-6_day_one_architecture_acceptance_audit.md
backend/scripts/validate_day_one_architecture.py
```

Also inspect as implementation authority:

```text
backend/app/routes/analysis.py
backend/core/dto/result_versioning_policy_v1.py
backend/core/analytics/domain_score_assembler.py
backend/core/analytics/domain_narrative_wave1.py
backend/core/analytics/report_compiler_v1.py
backend/core/pipeline/orchestrator.py
backend/services/storage/persistence_service.py
backend/core/contracts/replay_manifest_v1.py
backend/core/dto/persisted_replay_contract_v1.py
frontend/app/(app)/results/page.tsx
frontend/app/components/results/StaleResultBanner.tsx
frontend/app/components/results/Wave1DomainCards.tsx
frontend/app/lib/wave1HealthSystemCardDisplay.ts
frontend/app/types/analysis.ts
```

If actual paths differ, locate and report them.

---

# Track A — Wave 1 Domain Card Copy Alignment

## Problem statement

MED-REV-1 correctly hid or downgraded thin/support subsystems from the visible subsystem evidence rows. However, domain-card prose still references hidden or downgraded evidence.

Observed issue examples from manual UAT:

```text
Cardiovascular:
- Based mainly on: Vascular Inflammation Risk
- Why this score references inflammation and homocysteine signals
- But visible subsystem evidence is now only Atherogenic lipid pattern

Blood sugar:
- Card still says “Sugar and insulin balance”
- Copy still implies broader metabolic/insulin context
- But visible subsystem is now Long-term blood sugar only

Liver:
- Card evidence completeness and confidence prose no longer align cleanly with the flattened liver model
- Copy references marker availability in ways that may contradict actual available markers
```

This means MED-REV-1 fixed the subsystem visibility layer, but the domain-card narrative layer now needs alignment.

## Track A goal

Make domain-card anchors, labels, “why this score”, confidence, consequence and next-step text align with the MED-REV-1 visible medical model.

## Required Track A behaviour

### Cardiovascular

Required direction:

```text
Visible scored basis:
- Atherogenic lipid pattern

Do not present hidden support signals as the basis of the card score:
- homocysteine pathway
- vascular strain / CRP
```

Fixes required:

```text
- Replace “Based mainly on: Vascular Inflammation Risk” with a lipid-aligned consumer label.
- Do not say the cardiovascular score is based on inflammation/homocysteine if those are hidden support contexts.
- If homocysteine remains relevant elsewhere, it must be clearly framed as separate primary finding/root-cause context, not as the visible cardiovascular subsystem score basis.
```

### Blood sugar

Required direction:

```text
Visible scored basis:
- Long-term blood sugar

Do not imply insulin resistance or broad insulin/metabolic context from thin evidence.
```

Fixes required:

```text
- Rename/adjust card copy away from “Sugar and insulin balance” if insulin context is hidden.
- Ensure “why this score” and “what this may mean” describe long-term blood sugar exposure, not insulin resistance unless supported.
- Keep completeness/reliability wording aligned with HbA1c/glucose evidence.
```

### Liver

Required direction:

```text
Visible model:
- Flat/simplified liver card
- Evidence preserved, but not split into misleading scored subsystem rows
```

Fixes required:

```text
- Ensure liver confidence copy reflects the actual available liver markers.
- Do not say GGT, ALP or albumin are needed if they are already present.
- Avoid over-claiming MASLD/fibrosis risk from a thin/partial liver score line.
- Preserve useful caveats around alcohol, medications, liver history and follow-up.
```

## Track A constraints

Do not:

```text
- change clinical scoring thresholds
- change rail score calculations
- change marker values
- change SignalEvaluator or SignalRegistry
- change root-cause compiler logic
- change PSI status
- reintroduce hidden subsystems as visible scored evidence
- use frontend logic to decide medical meaning
```

Layer B must own meaning. Layer C must render.

---

# Track B — Versioned Result Regeneration UX

## Problem statement

UAT requires repeatedly uploading a fresh panel to see how the current engine renders a result. LAUNCH-CORE-3 added stale/incompatible result metadata and a banner, but did not add regeneration.

We need a safe way to regenerate an existing analysis using the latest engine without overwriting the old result.

## Non-negotiable regeneration rule

Do not overwrite generated results.

Required model:

```text
old result remains immutable
regenerated result is a new version or new analysis/result record
old and new are linked or traceable where possible
```

No destructive refresh. No silent mutation.

## Track B goal

Add a safe “Regenerate with latest engine” user flow only if the stored input required for deterministic regeneration is available.

If required inputs are missing, show a clear “Regeneration unavailable” explanation and do not fake it.

## Required Track B preflight

Before implementation, verify and report:

```text
1. Where raw uploaded/pasted biomarker input is stored.
2. Where parsed biomarker payload is stored.
3. Where lifestyle/questionnaire answers are stored.
4. Whether the existing orchestrator can be invoked safely from stored input.
5. Whether regenerating from stored input would create a new result row or overwrite the existing row.
6. Whether existing DB schema supports linking old/new result versions.
7. Whether LAUNCH-CORE-3 result_versioning metadata can identify stale/incompatible records.
8. Whether regeneration is safe for:
   - 746f2b0a-b470-4d87-8ed8-e2c3d1e68c02
   - 18e14232-9f93-45e6-820c-004ab5a16235
   - bb695d3c-453e-4e49-abff-ae80587b4248
```

STOP if safe regeneration cannot be proven.

## Track B permitted implementation

Allowed if safe and bounded:

```text
- Add a backend endpoint such as POST /api/analysis/{analysis_id}/regenerate
- Endpoint reads preserved stored input/questionnaire
- Endpoint runs current engine deterministically
- Endpoint creates a new result/version record
- Endpoint does not overwrite old result
- Endpoint returns the new analysis/result ID
- Frontend stale/incompatible banner shows a “Regenerate with latest engine” button only when regeneration_available is true
- If regeneration_available is false, frontend shows clear reason / “upload again” guidance
```

If full regeneration endpoint is too broad:

```text
- Implement only regeneration availability detection and UI messaging.
- Do not add a button that cannot work.
```

## Track B constraints

Do not:

```text
- overwrite existing result payloads
- mutate old analysis records
- fake regenerated output
- bypass existing pipeline/orchestrator rules
- use fallback parsers
- regenerate from incomplete stored input
- silently change result history
- create broad DB migrations unless explicitly approved by hardening
```

---

# Shared architectural requirements

## Layer A / B / C separation

```text
Layer A = governed medical intelligence and stored inputs
Layer B = interpretation, result assembly, narrative, regeneration policy, DTO shaping
Layer C = presentation/rendering only
```

Frontend must not infer clinical meaning, stale logic, or regeneration safety from raw fields. Backend must provide safe metadata.

## Content preservation

Do not remove clinically meaningful evidence. If evidence is not suitable for default display, keep it available in governed detail or hidden Layer A artefacts.

## Auditability

Any regenerated result must be traceable to:

```text
- source analysis/input
- generation time
- current engine/result version metadata
- stale/incompatible reason of old result where applicable
```

If full lineage IDs are not yet available, document the gap and avoid over-claiming auditability.

---

# Required tests

Add or update tests for Track A:

```text
1. Cardiovascular card anchor/prose no longer uses hidden vascular inflammation/homocysteine context as score basis.
2. Cardiovascular visible subsystem remains Atherogenic lipid pattern.
3. Blood sugar card copy aligns with Long-term blood sugar and does not imply insulin resistance from hidden context.
4. Liver copy does not claim missing GGT/ALP/albumin when present.
5. Hidden subsystems remain hidden.
6. total_bilirubin protection remains intact.
```

Add or update tests for Track B, if implementation occurs:

```text
1. Regeneration availability is true only when stored input is sufficient.
2. Regeneration availability is false when required input is missing.
3. Regenerate endpoint creates a new result/version, not overwrite.
4. Old result remains accessible.
5. New result includes current result_versioning metadata.
6. Frontend button appears only when regeneration_available is true.
7. No regenerate button appears when unavailable.
8. Incompatible/stale banner remains visible.
```

Always run:

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
```

Also run targeted tests for touched backend/frontend files.

## Manual validation

After implementation, manually inspect:

```text
http://localhost:3000/results?analysis_id=746f2b0a-b470-4d87-8ed8-e2c3d1e68c02
```

Login:

```text
test-user3@example.com
Subaru@555
```

Confirm:

```text
- Cardiovascular card no longer anchors on Vascular Inflammation Risk as the card score basis.
- Cardiovascular prose aligns with Atherogenic lipid pattern.
- Blood sugar card no longer implies insulin context if hidden.
- Liver card prose aligns with flattened model and actual available markers.
- Hidden subsystems do not appear as scored subsystem rows.
- Regenerate button appears only if backend says regeneration is available.
- If regeneration is used, old result remains accessible and new result loads.
- No internal IDs/traces are visible.
```

---

# STOP conditions

STOP and report if:

```text
1. Track A requires changing scoring thresholds or clinical interpretation logic.
2. Track A requires frontend medical inference.
3. Track A requires broad narrative compiler rewrite.
4. Track B cannot locate stored input needed for deterministic regeneration.
5. Track B would overwrite old results.
6. Track B requires broad DB lineage migration.
7. Regeneration cannot be made auditable enough for this sprint.
8. ARCH-RT-6 validator fails.
9. Scope drifts into Pass 3 richness utilisation or LLM narrative translation.
```

---

# Required deliverable

Create:

```text
docs/audit-papers/MED-REV-2_wave1_domain_card_copy_alignment_and_result_regeneration_ux_report.md
```

Report must include:

```text
- Track A changes
- Track B preflight findings
- regeneration implemented or deferred decision
- files changed
- before/after card copy examples
- Layer A/B/C responsibility split
- evidence preservation confirmation
- result immutability confirmation
- tests run
- manual validation result
- remaining risks / carry-forwards
```

---

# Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. Track A root-cause findings
3. Track B regeneration preflight findings
4. exact card copy / DTO changes
5. exact regeneration API/UI changes, if any
6. files changed
7. tests added/updated
8. test commands run
9. test results
10. manual browser validation result
11. confirmation old results are not overwritten
12. confirmation frontend did not infer clinical meaning
13. confirmation ARCH-RT-6 validator still passes
```

---

# Closure requirements

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
- current branch matches work/MED-REV-2-wave1-domain-card-copy-alignment-and-result-regeneration-ux
- all changed files are tied to this sprint
- no destructive refresh logic is included
- no clinical thresholds or scoring rails are changed
- no frontend clinical inference is introduced
- no ambiguous stash exists
- latest commit contains only in-scope work
```

---

# Success criteria

This sprint is complete only if:

```text
1. Domain-card prose aligns with the MED-REV-1 visible model.
2. Hidden/support subsystems are not referenced as the visible score basis.
3. Liver prose aligns with the flattened v1 model and available markers.
4. Useful evidence remains preserved.
5. Regeneration is either safely implemented or explicitly deferred with reason.
6. No old result is overwritten.
7. Frontend remains render-only.
8. ARCH-RT-6 validator passes.
9. Tests prove the card alignment and regeneration behaviour.
10. Automation Bus gate passes.
```

```
```
