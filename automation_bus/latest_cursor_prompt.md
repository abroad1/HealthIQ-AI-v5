---
work_id: KB-UTIL-1_pass3_card_evidence_compile_and_consume
branch: work/KB-UTIL-1-pass3-card-evidence-compile-and-consume
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# KB-UTIL-1 — Pass 3 Card Evidence Compile and Consume

## Purpose

Now that MED-REV-1 and MED-REV-2 have stabilised the visible Wave 1 subsystem model, begin using the richer Pass 3 / package medical intelligence properly in the Health Systems Card evidence layer.

The consolidation audits concluded that Pass 3 and package intelligence is only partially utilised. Signal activation uses governed packages, but much of the richer medical intelligence remains stranded:

```text
- hypotheses
- contradiction markers
- relationship_kind
- marker role/rationale detail
- mechanism prose
- missing-data policy
- confirmatory test rationale
- explanation.* fields
````

This sprint must compile and consume relevant Pass 3 / package richness into governed Layer B card/subsystem DTO fields.

It must not introduce raw Pass 3 runtime reads.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
ARCH-RT programme fully merged through ARCH-RT-6
MED-REV-1 merged
MED-REV-2 merged
LAUNCH-CORE carry-forward register created
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
* MED-REV-2 is not merged
* `docs/sprints/launch_core_carry_forward_register.md` is missing
* untracked or uncommitted files are present

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint may touch Knowledge Bus compiled card artefacts, package-to-card evidence compilation, Layer B card evidence DTOs, health system card assembly, validators and tests. It affects user-facing medical explanation and must remain strictly governed.

## Standard rules

This work remains governed by the standard Knowledge Bus and Automation Bus SOPs already active in the repository.

Do not re-read SOPs unless the applicable governance requirement cannot be located.

## Required carry-forward register handling

Before implementation, read:

```text
docs/sprints/launch_core_carry_forward_register.md
```

If this sprint resolves any carry-forward, update the register.

If this sprint creates new carry-forwards, add them to the register.

Do not let sprint-level carry-forwards remain only in chat, reports, or audit summaries.

## Authoritative inputs

Read these sprint-specific files before making changes:

```text
docs/sprints/launch_core_carry_forward_register.md
docs/audit-papers/PROGRAMME-STATUS-1_healthiq_launch_workstream_consolidation_audit.md
docs/audit-papers/PASS3_research_asset_utilisation_investigation_cursor.md
docs/architecture/ARCH-R1_research_asset_to_runtime_intelligence_architecture_review_cursor.md
docs/audit-papers/healthiq_wave1_health_systems_subsystem_medical_review.md
docs/audit-papers/MED-REV-1_wave1_subsystem_visibility_and_label_alignment_report.md
docs/audit-papers/MED-REV-2_wave1_domain_card_copy_alignment_and_result_regeneration_ux_report.md
docs/audit-papers/ARCH-RT-6_day_one_architecture_acceptance_audit.md
docs/audit-papers/active_intelligence_authority_manifest.md
backend/scripts/validate_day_one_architecture.py
```

Also inspect as implementation authority:

```text
knowledge_bus/research/investigation_specs/multi_llm_research/*_Pass_3.json
knowledge_bus/packages/**
knowledge_bus/compiled/health_system_cards/*.yaml
knowledge_bus/compiled/estate_index_v1.yaml
backend/core/knowledge/health_system_card_evidence.py
backend/core/analytics/wave1_subsystem_evidence.py
backend/core/analytics/domain_score_assembler.py
frontend/app/components/results/Wave1DomainCards.tsx
frontend/app/components/results/Wave1SubsystemEvidenceSection.tsx
frontend/app/types/analysis.ts
```

If paths differ, locate and report the actual paths.

## Problem statement

Programme consolidation found:

```text
Pass 3 → packages:
- moderate utilisation for signal activation
- limited utilisation for rich explanatory intelligence

Packages → runtime:
- activation and overrides are used
- explanation.* is stored but largely not consumed by cards/reports
- relationship_kind is not consumed
- contradiction markers and hypothesis ranking are not surfaced
- SubsystemEvidenceV1.evidence_role is usually null
```

The Health Systems Cards now have a medically safer visible subsystem model after MED-REV-1 / MED-REV-2. The next step is to enrich those visible cards and evidence groups using governed research/package intelligence.

## Architectural principle

Preserve the HealthIQ architecture:

```text
Layer A = governed medical intelligence inputs and compiled artefacts
Layer B = interpretation, prioritisation, card evidence DTO shaping
Layer C = presentation/rendering only
```

This sprint must compile or consume richer evidence into Layer A/B governed artefacts and DTOs.

Frontend must not mine packages, Pass 3 JSON, signal IDs, or marker IDs to infer meaning.

## Non-negotiable rule: no raw Pass 3 runtime reads

Runtime must not read raw `*_Pass_3.json` files.

Allowed:

```text
Pass 3 / packages → governed compile artefact → Layer B loader/assembler → DTO → frontend render
```

Forbidden:

```text
runtime orchestrator / API / frontend → raw Pass 3 JSON
runtime orchestrator / API / frontend → package file scraping for prose
frontend → marker-ID inference
```

## Scope

Allowed scope:

1. Audit which Pass 3/package richness is available for the current visible Wave 1 card model.
2. Define the minimal governed enrichment fields needed for card/subsystem DTOs.
3. Extend compiled card evidence artefacts or create a bounded compiled enrichment artefact if needed.
4. Populate only medically reviewed, consumer-safe evidence fields for visible Wave 1 card surfaces.
5. Wire Layer B card evidence assembly to consume those compiled/governed fields.
6. Add tests proving enriched evidence is compiled/governed and consumed without raw runtime reads.
7. Update validator/guardrails if needed.
8. Update carry-forward register.
9. Produce sprint report.

## Out of scope

Do not:

```text
- read raw Pass 3 JSON at runtime
- implement full estate Pass 3 compiler
- wire all 153 specs
- change signal activation thresholds
- change scoring rails
- change biomarker SSOT
- change unit conversion
- modify SignalEvaluator
- modify SignalRegistry
- change PSI runtime status
- implement LLM narrative translation
- implement regeneration lineage hardening
- implement frontend clinical inference
- re-surface hidden MED-REV-1 support subsystems as scored findings
- reverse MED-REV-1 visibility decisions
- introduce fallback parsers
```

## Required preflight

Before implementation, verify and report:

```text
1. Which visible Wave 1 card/subsystem surfaces remain after MED-REV-1:
   - Atherogenic lipid pattern
   - Long-term blood sugar
   - flattened liver card / evidence model

2. Which Pass 3/package assets correspond to those visible surfaces.

3. Which useful fields already exist in packages:
   - explanation.*
   - supporting_metrics roles/rationales
   - mechanism/pathway/implications text
   - contradiction markers
   - missing data policy
   - confirmatory tests
   - relationship_kind

4. Which of those fields are already present in compiled card artefacts.

5. Which of those fields are already present in DTOs.

6. Which fields are safe for consumer-facing use without LLM rewriting.

7. Which fields should remain internal until Layer B narrative brief maturity work.

8. Whether the implementation can be bounded to Wave 1 launch surfaces.
```

STOP if the available evidence is too broad or ambiguous to compile safely in one sprint.

## Target enrichment model

Prefer a minimal, explicit model.

Candidate fields to consider, subject to current schema and medical safety:

```text
marker_role
relationship_kind
consumer_rationale
mechanism_summary
why_this_marker_matters
missing_marker_reason
confidence_contribution
contradiction_note
confirmatory_follow_up
evidence_limitations
```

Do not add all fields blindly.

Only add fields that:

```text
- are grounded in existing Pass 3/package content
- can be validated
- are suitable for Layer B DTO output
- do not require frontend interpretation
- do not contradict MED-REV-1 visibility decisions
```

## Visible surface rules

### Atherogenic lipid pattern

Allowed enrichment direction:

```text
- explain why LDL, HDL, triglycerides, total cholesterol and TC/HDL ratio matter together
- use role/rationale from packages where available
- avoid claiming CRP/homocysteine are the card score basis
- do not reintroduce vascular strain as visible scored subsystem
```

### Long-term blood sugar

Allowed enrichment direction:

```text
- explain HbA1c as long-term glycaemic exposure
- explain glucose as useful when present but optional/missing for confidence
- avoid implying insulin resistance when insulin context is hidden
- keep insulin/TG support context internal unless medically reviewed for display
```

### Liver flat model

Allowed enrichment direction:

```text
- explain available liver markers without re-splitting into scored subsystems
- avoid over-claiming MASLD/fibrosis risk from thin evidence
- use missing-marker logic accurately
- preserve alcohol/medication/liver-history caveats
```

## Schema / artefact rules

If compiled card YAML is extended:

```text
- update schema if required
- update validator if required
- update compile manifest hashes if repository policy requires
- preserve existing marker IDs and clinical thresholds
- preserve `total_bilirubin` prohibition
- do not alter visibility tiers unless medical review requires it
```

If creating a new compiled enrichment artefact:

```text
- add it to estate index / authority manifest if required
- add validation tests
- ensure Layer B consumes it, not frontend
```

## Layer B consumption rules

Layer B may:

```text
- attach enriched evidence text to card/subsystem DTO fields
- expose consumer-safe rationales
- expose evidence limitations
- expose confidence contribution notes
```

Layer B must not:

```text
- expose raw package prose without review
- expose internal IDs
- expose raw source traces
- expose unreviewed Pass 3 hypotheses directly
- turn hidden support subsystems back into primary card findings
```

## Layer C rendering rules

Frontend may:

```text
- render backend-provided enriched fields
- collapse detail by default if needed
- display approved labels
```

Frontend must not:

```text
- read packages
- read Pass 3 files
- infer marker roles
- infer clinical hierarchy
- map hidden subsystem meaning from IDs
```

## Required tests

Add or update tests proving:

```text
1. No raw Pass 3 JSON runtime reads are introduced.
2. Enriched card evidence is loaded from governed compiled artefacts or packages through an approved Layer B path.
3. Visible Wave 1 card surfaces receive enriched evidence where implemented.
4. Hidden MED-REV-1 subsystems remain hidden.
5. Atherogenic lipid pattern does not use homocysteine/CRP as card score basis.
6. Long-term blood sugar does not imply insulin resistance from hidden context.
7. Liver enrichment does not re-split liver into scored subsystems.
8. Frontend remains render-only.
9. Internal IDs/source traces/package IDs are not exposed.
10. `total_bilirubin` protection remains intact.
11. ARCH-RT-6 validator still passes.
```

Always run:

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
```

Also run targeted tests for:

```text
health_system_card_evidence
wave1_subsystem_evidence
domain_score_assembler
MED-REV-1
MED-REV-2
relevant frontend card components if touched
```

## Manual validation target

After implementation, inspect a regenerated latest-engine result, not an immutable stale snapshot.

Use either the most recent regenerated analysis or regenerate from:

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
- enriched evidence appears only where medically safe
- hidden support subsystems remain hidden
- card text feels more clinically informative without becoming noisy
- frontend is not exposing internal IDs/traces
- no old stale snapshot is mistaken for current engine output
```

## STOP conditions

STOP and report if:

```text
1. Pass 3/package evidence cannot be mapped safely to visible Wave 1 surfaces.
2. Implementation would require raw Pass 3 runtime reads.
3. Implementation would require a broad full-estate compiler.
4. Implementation would re-open MED-REV-1 hidden subsystems as scored findings.
5. Implementation would require frontend clinical inference.
6. Evidence fields are not consumer-safe without LLM narrative translation.
7. Schema extension is too broad for one sprint.
8. Compile manifest / estate index updates cannot be safely performed.
9. ARCH-RT-6 validator fails.
10. Sprint drifts into LLM translation or UX redesign.
```

## Required deliverable

Create:

```text
docs/audit-papers/KB-UTIL-1_pass3_card_evidence_compile_and_consume_report.md
```

The report must include:

```text
- preflight findings
- Pass 3/package fields assessed
- fields selected for consumption
- fields deferred and why
- artefacts changed or created
- Layer B consumption changes
- Layer C rendering changes, if any
- evidence preservation confirmation
- hidden subsystem protection confirmation
- carry-forward register updates
- tests run
- manual validation result
- remaining risks / carry-forwards
```

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. carry-forward register read/update evidence
3. Pass 3/package asset mapping
4. selected enrichment model
5. exact artefact changes
6. exact Layer B changes
7. exact frontend changes, if any
8. tests added/updated
9. test commands run
10. test results
11. manual browser validation result
12. confirmation no raw Pass 3 runtime reads were introduced
13. confirmation frontend did not infer clinical meaning
14. confirmation ARCH-RT-6 validator still passes
```

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
- current branch matches work/KB-UTIL-1-pass3-card-evidence-compile-and-consume
- all changed files are tied to this sprint
- carry-forward register has been updated if required
- no raw Pass 3 runtime reads are introduced
- no frontend clinical inference is introduced
- no clinical thresholds or scoring rails are changed
- no hidden subsystem is reintroduced as a visible scored finding
- no ambiguous stash exists
- latest commit contains only in-scope work
```

## Success criteria

This sprint is complete only if:

```text
1. Pass 3/package richness utilisation for visible Wave 1 cards is materially improved or explicitly bounded/deferred.
2. Enrichment is governed through Layer A/B, not frontend inference.
3. No raw Pass 3 runtime reads are introduced.
4. MED-REV-1/2 visible subsystem model remains intact.
5. Hidden support subsystems remain hidden.
6. Useful evidence is preserved.
7. Carry-forward register is updated.
8. ARCH-RT-6 validator passes.
9. Tests prove the new evidence consumption path.
10. Automation Bus gate passes.
```

```
```
