---
work_id: LAUNCH-CORE-1_results_page_card_coherence_and_consumer_copy
branch: work/LAUNCH-CORE-1-results-page-card-coherence-and-consumer-copy
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# LAUNCH-CORE-1 — Results Page Card Coherence and Consumer Copy

## Purpose

Fix the human UAT issues found on the results page after the ARCH-RT programme.

This sprint must improve the consumer-facing results page by resolving:

```text
1. Health Systems Card completeness mismatch
2. misleading score/coverage presentation
3. internal/generated names surfacing in prose
4. raw engineering marker-role labels appearing in chips
5. poor biomarker display labels such as Mcv instead of MCV
6. narrative encoding/mojibake artefacts
7. upload-fidelity wording inconsistencies
````

This sprint must preserve the ARCH-RT architecture guardrails. It must not weaken compiled evidence, provenance, PSI isolation, root-cause promotion safety, or frontend render-only principles.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
ARCH-RT programme fully merged through ARCH-RT-6
ARCH-RT-6 guardrails active
ARCH-RT-5E PSI classified deferred_non_launch_blocker
```

Before creating or switching to the sprint branch, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 16
git rev-parse HEAD
git rev-parse origin/main
```

STOP if:

* current branch is not `main`
* local `main` does not equal `origin/main`
* working tree is not clean
* ARCH-RT-6 is not merged
* untracked or uncommitted files are present

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint may touch backend domain-card assembly, DTO fields, frontend results rendering, narrative sanitisation, and tests. It affects user-facing health interpretation, even if the intention is clarity rather than clinical logic change.

## Standard rules

This work remains governed by the standard Knowledge Bus and Automation Bus SOPs already active in the repository.

Do not re-read SOPs unless the applicable governance requirement cannot be located.

## Authoritative inputs

Read these sprint-specific files before making changes:

```text
docs/audit-papers/LAUNCH-CORE-0_results_page_human_uat_investigation.md
docs/audit-papers/ARCH-RT-6_day_one_architecture_acceptance_audit.md
docs/architecture/ARCH-RT-6_day_one_architecture_guardrails_report.md
docs/audit-papers/active_intelligence_authority_manifest.md
docs/audit-papers/day_one_architecture_launch_readiness_audit.md
docs/architecture/card_evidence_role_translation_policy.md
docs/architecture/card_visibility_tier_policy.md
backend/scripts/validate_day_one_architecture.py
```

Also inspect as implementation authority:

```text
backend/core/analytics/domain_score_assembler.py
backend/core/knowledge/health_system_card_evidence.py
backend/core/models/results.py
frontend/app/components/results/Wave1DomainCards.tsx
frontend/app/components/results/Wave1SubsystemEvidenceSection.tsx
frontend/app/components/results/ResultsHeroBlocks.tsx
frontend/app/components/results/DeterministicNarrativeSurface.tsx
frontend/app/components/results/ResultsBodyOverview.tsx
frontend/app/components/results/PrimaryFindingAndWhy.tsx
frontend/app/lib/retailNarrativeSanitize.ts
frontend/app/lib/resultsPageLayout.ts
frontend/app/lib/wave1HealthSystemCardDisplay.ts
frontend/app/types/analysis.ts
```

STOP if the UAT investigation file is missing.

## UAT findings to fix

The investigation confirmed that marker presence itself is backend-correct for analysis `18e14232-9f93-45e6-820c-004ab5a16235`, but several user-facing issues remain. The key architectural UX defect is that card summary completeness uses legacy rail counting while expanded subsystem evidence uses the new compiled subsystem model, causing the Blood sugar card to show “1 of 3 expected markers included” while the expanded detail shows 2 included and 2 missing. 

The investigation also confirmed internal/generated prose leaks, raw enum role labels, poor marker display formatting, score/coverage dissonance, and mojibake artefacts. 

## Mandatory inherited guardrails

The following must remain true:

```text
1. No raw investigation spec runtime reads.
2. No frontend medical inference.
3. Frontend renders backend-provided evidence fields only.
4. PSI remains deferred and must not be used as card/root-cause/hypothesis authority.
5. All Wave 1 card subsystems remain on compiled card evidence.
6. total_bilirubin must not be reintroduced as an independent required marker.
7. signal_vitamin_d_low remains compiled-promoted with summary_template enforcement.
8. No raw internal source_trace strings are rendered to consumers.
9. Day-one architecture validator must still pass.
```

Do not weaken these.

## Scope

Allowed scope:

1. Change Health Systems Card evidence completeness so summary counts align with compiled subsystem evidence.
2. Improve score/completeness presentation so high scores with limited evidence are not misleading.
3. Add consumer-safe marker-role labels for card chips.
4. Stop rendering raw marker-role enum vocabulary such as `score_contributor` as “score contributor” unless explicitly approved as consumer copy.
5. Fix biomarker display formatting such as `mcv` → `MCV`.
6. Add an interim consumer-safe replacement for known generated/internal names, especially “Homocysteine Elevation Context”.
7. Fix narrative mojibake/encoding artefacts if the source is traceable and bounded.
8. Align upload-fidelity wording where a marker is scored in one context but described as “not scored separately”.
9. Add targeted regression tests.
10. Produce a launch defect resolution report.

## Primary backend fix required

The Health Systems Card summary evidence completeness must be reconciled with compiled subsystem evidence.

Current defect:

```text
Blood sugar summary:
1 of 3 expected markers included

Blood sugar expanded subsystems:
HbA1c included
Triglycerides included
Glucose missing
Insulin missing
= 2 of 4 subsystem-expected markers included
```

Required direction:

```text
Derive domain/card evidence completeness from the union of compiled subsystem included/missing markers, or from one backend-owned field derived from that union.
```

Expected result for the observed analysis, subject to implementation details:

```text
Blood sugar evidence completeness should read 2 of 4 expected markers included
```

Do not let the frontend independently recompute clinical completeness. Backend should remain authoritative.

## Score/coverage presentation rule

If a card has a very high score but low confidence or low evidence completeness, the UI must avoid implying “perfect health certainty”.

Acceptable approaches include:

```text
- qualify the score visually/copy-wise when evidence coverage is limited
- show “Score based on available markers” wording
- ensure reliability/completeness text is visually close to the score
- avoid unqualified celebratory interpretation when confidence_tier is low
```

Do not change clinical scoring thresholds unless specifically justified and approved by hardening.

## Consumer copy fixes

### Marker role chips

Replace raw role enum display with consumer-safe labels.

Examples:

```text
score_contributor       → Used in this score
confidence_contributor  → Supports confidence
contextual_marker       → Context marker
mechanism_marker        → Helps explain mechanism
differential_marker     → Helps distinguish causes
exclusion_marker        → Helps rule out alternatives
missing_for_confidence  → Missing for confidence
optional_deeper_marker  → Optional deeper marker
```

Final wording can differ, but must be intentionally consumer-facing.

### Internal/generated names

At minimum, prevent this consumer-facing phrase:

```text
Homocysteine Elevation Context
```

from appearing as the hero/prose label.

Use a safer consumer-facing replacement, for example:

```text
Raised homocysteine pattern
```

or an equivalent governed wording.

This may be an interim scrub if the deeper narrative compiler fix is too broad.

### Marker display labels

Use governed display-name mapping where available.

Known defect:

```text
Mcv → MCV
```

Do not use naive title-casing where a biomarker label map exists.

### Mojibake

Fix visible narrative mojibake such as:

```text
â
```

where this can be corrected safely at compile/render/persist boundary.

If the source is persisted historical data and cannot be safely corrected for existing records, add frontend/backend display sanitisation and document the limitation.

## Out of scope

Do not:

* change clinical thresholds
* change scoring rail calculations unless needed only for completeness display alignment
* change biomarker SSOT
* change unit conversion
* change package clinical content
* change investigation specs
* change PSI runtime status
* modify SignalRegistry or SignalEvaluator
* promote additional root-cause pathways
* alter compiled card evidence clinical meaning
* weaken ARCH-RT-6 guardrails
* expose source_trace, compile_manifest_ref, artefact_id, package_id, source_spec_id or activation_key to consumers
* introduce fallback parsers

## Required tests

Add or update targeted tests for:

1. Blood sugar completeness aligns with compiled subsystem evidence.
2. Domain/card summary completeness no longer disagrees with expanded subsystem chips.
3. Role chips use consumer-safe labels, not raw enum strings.
4. `Homocysteine Elevation Context` does not render to the consumer page.
5. `mcv` formats as `MCV`.
6. Mojibake is removed or sanitised from consumer-visible narrative.
7. Upload-fidelity wording does not contradict scored-marker status for HbA1c, if fixed.
8. Raw internal IDs/traces are not rendered.
9. ARCH-RT-6 validator still passes.
10. Existing card evidence and root-cause tests still pass.

At minimum run:

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
```

Also run targeted backend/frontend tests relevant to touched files.

If frontend tests exist, run the relevant test command. If no frontend tests exist for the touched components, document manual/browser validation steps.

## STOP conditions

STOP and report if:

1. Required investigation or architecture files are missing.
2. Fixing completeness requires broad clinical scoring redesign.
3. Fixing prose requires rewriting the narrative compiler broadly.
4. Any fix would weaken ARCH-RT-6 guardrails.
5. Frontend would need to infer clinical meaning.
6. Backend would need raw investigation spec runtime reads.
7. PSI/root-cause/card authority boundaries would be blurred.
8. Tests cannot prove the observed UAT defects are fixed.
9. The fix scope expands beyond results-page coherence and consumer copy.

## Required deliverables

Create:

```text
docs/audit-papers/LAUNCH-CORE-1_results_page_card_coherence_and_consumer_copy_report.md
```

The report must include:

* UAT issues addressed
* files changed
* backend changes
* frontend changes
* exact before/after for Blood sugar completeness
* exact before/after for role chip labels
* exact before/after for generated/internal prose labels
* exact before/after for MCV formatting
* encoding/mojibake outcome
* tests run
* results
* remaining risks or carry-forwards

## Evidence required from Cursor

Cursor must report:

1. Baseline branch/status/HEAD evidence.
2. Authority preflight findings.
3. Root cause confirmation for the completeness mismatch.
4. Exact completeness calculation change.
5. Exact consumer-copy changes.
6. Files changed.
7. Tests added/updated.
8. Test commands run.
9. Test results.
10. Manual browser validation result for the target analysis page.
11. Confirmation ARCH-RT-6 validator still passes.
12. Confirmation no raw internal IDs/traces are visible.
13. Confirmation no PSI/root-cause/SignalRegistry/SignalEvaluator changes were included.

## Closure requirements

Before `run_work_package.py finish`, complete the Automation Bus post-implementation closure protocol.

Run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
git diff --name-only
git diff --cached --name-only
git stash list
```

Classify:

* tracked modified files
* staged files
* untracked files
* tooling files
* out-of-scope files
* stash entries

Do not run finish unless:

* current branch matches `work/LAUNCH-CORE-1-results-page-card-coherence-and-consumer-copy`
* all changed files are tied to this sprint
* architecture validator passes
* targeted tests pass
* no ambiguous stash exists
* latest commit contains only in-scope work

## Success criteria

This sprint is complete only if:

1. Blood sugar summary completeness matches compiled subsystem evidence.
2. Health card summary and expanded detail no longer present contradictory marker counts.
3. Raw marker-role enums are not surfaced as consumer chip text.
4. Known internal/generated prose labels are not surfaced to consumers.
5. Biomarker labels use governed display names where available.
6. Mojibake is fixed or safely sanitised.
7. No internal source_trace / compile_manifest_ref / artefact_id / source_spec_id / activation_key is visible to consumers.
8. ARCH-RT-6 guardrails still pass.
9. Tests prove the fixes.
10. Automation Bus gate passes.

```
```
