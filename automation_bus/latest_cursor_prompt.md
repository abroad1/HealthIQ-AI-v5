---
work_id: LAYER-B-1_narrative_brief_maturity
branch: work/LAYER-B-1-narrative-brief-maturity
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# LAYER-B-1 — Narrative Brief Maturity

## Purpose

Build the governed Layer B narrative brief needed to turn HealthIQ’s deterministic analysis into a coherent, ordered, auditable health report.

MED-REV-1, MED-REV-2 and KB-UTIL-1 have stabilised the visible Wave 1 medical model and enriched the card evidence. The remaining report problem is that the application still does not consistently produce a single coherent narrative plan across:

```text
- primary finding
- why it matters
- confidence
- supporting evidence
- missing evidence
- health system context
- next steps
````

This sprint must mature the Layer B narrative brief. It must not wire LLM narrative generation yet.

The goal is to create a governed structured brief that a deterministic renderer or future LLM translation layer can safely consume.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
ARCH-RT programme fully merged through ARCH-RT-6
LAUNCH-CORE-5 merged
MED-REV-1 merged
MED-REV-2 merged
KB-UTIL-1 merged
docs/sprints/launch_core_carry_forward_register.md present and updated
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
* KB-UTIL-1 is not merged
* `docs/sprints/launch_core_carry_forward_register.md` is missing
* untracked or uncommitted files are present

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint may touch Layer B narrative payload contracts, narrative payload builders, report assembly, deterministic narrative surfaces, validation rules and tests. It affects user-facing health interpretation and future LLM readiness.

## Standard rules

This work remains governed by the standard Knowledge Bus and Automation Bus SOPs already active in the repository.

Do not re-read SOPs unless the applicable governance requirement cannot be located.

## Carry-forward register handling

Before implementation, read:

```text
docs/sprints/launch_core_carry_forward_register.md
```

If this sprint resolves any carry-forward, update the register.

If this sprint creates new carry-forwards, add them to the register.

Pay particular attention to:

```text
CF-KBUTIL1-002 — Hypothesis, contradiction marker and confirmatory test surfacing
```

This sprint may prepare the narrative brief structure needed for that future surfacing, but it must not expose unsafe hypothesis/contradiction/confirmatory-test content unless explicitly governed and tested.

## Authoritative inputs

Read these sprint-specific files before making changes:

```text
docs/sprints/launch_core_carry_forward_register.md
docs/audit-papers/PROGRAMME-STATUS-1_healthiq_launch_workstream_consolidation_audit.md
docs/audit-papers/KB-UTIL-1_pass3_card_evidence_compile_and_consume_report.md
docs/audit-papers/MED-REV-2_wave1_domain_card_copy_alignment_and_result_regeneration_ux_report.md
docs/audit-papers/MED-REV-1_wave1_subsystem_visibility_and_label_alignment_report.md
docs/audit-papers/LAUNCH-CORE-4_results_page_narrative_hierarchy_and_score_rationalisation_audit.md
docs/audit-papers/LAUNCH-CORE-5_results_page_narrative_hierarchy_and_score_rationalisation_report.md
docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md
docs/planning-papers/healthiq_pre_sprint3_closure_pack_FINAL.md
docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md
docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md
backend/scripts/validate_day_one_architecture.py
```

Also inspect as implementation authority:

```text
backend/core/contracts/narrative_payload_v1.py
backend/core/analytics/narrative_payload_builder_v1.py
backend/core/analytics/domain_narrative_wave1.py
backend/core/analytics/report_compiler_v1.py
backend/core/analytics/domain_score_assembler.py
backend/core/llm/validator_v2.py
backend/core/models/results.py
frontend/app/(app)/results/page.tsx
frontend/app/components/results/*
frontend/app/types/analysis.ts
```

If paths differ, locate and report the actual paths.

## Problem statement

The current system has many useful deterministic outputs, but the report-level narrative is still not sufficiently governed.

Known issues:

```text
1. Multiple surfaces can still compete to explain the same lead finding.
2. The page can expose too many score families without a clear precedence model.
3. Primary finding, health system cards, patterns and marker evidence are not always governed by one shared narrative plan.
4. Layer B does not yet produce a complete narrative brief with section-specific intent, evidence boundaries and wording constraints.
5. LLM translation cannot safely proceed until this brief exists.
```

This sprint should not try to make the final consumer prose perfect. It should build the structured narrative plan underneath it.

## Architectural principle

Preserve the HealthIQ layer architecture:

```text
Layer A = governed medical intelligence inputs and compiled artefacts
Layer B = interpretation, prioritisation, narrative planning, DTO shaping
Layer C = presentation/rendering only
```

Layer B must own:

```text
- report story ordering
- primary finding hierarchy
- section intent
- evidence selection boundaries
- confidence / limitation framing
- what should be visible by default vs detail
- what should never be said
- what future LLM translation may and may not do
```

Layer C must not infer clinical meaning or decide narrative priority.

## LLM boundary

Do not wire LLM narrative generation in this sprint.

The future LLM role remains:

```text
LLM translates a governed Layer B brief.
LLM does not reason.
LLM does not inspect raw biomarkers independently.
LLM does not decide findings, hierarchy, confidence or next steps.
Layer C does not call the LLM.
```

This sprint may update `validator_v2` or narrative validation scaffolds if needed, but it must not enable production LLM narrative generation.

## Scope

Allowed scope:

1. Audit current `NarrativePayloadV1` and builder coverage against the desired Layer B brief.
2. Extend the narrative payload contract if necessary.
3. Add section-specific narrative intent fields.
4. Add evidence-boundary fields that define what each section may cite.
5. Add confidence/limitation framing fields.
6. Add forbidden-claim / must-not-say constraints where appropriate.
7. Add report-level priority ordering metadata.
8. Add fields needed for future LLM translation safety.
9. Wire deterministic report assembly to consume the improved brief where safe.
10. Add validation/tests for narrative brief integrity.
11. Update carry-forward register.
12. Produce sprint report.

## Out of scope

Do not:

```text
- wire Gemini or any LLM into the report
- implement LLM translation
- change clinical scoring thresholds
- change signal activation
- change biomarker SSOT
- change unit conversion
- change SignalEvaluator or SignalRegistry
- change PSI runtime status
- modify root-cause compiler promotion policy
- expose raw Pass 3 hypotheses directly to users
- expose contradiction markers directly to users unless governed and tested
- expose confirmatory tests directly unless governed and tested
- perform broad UX redesign
- implement regeneration lineage hardening
- introduce frontend clinical inference
- introduce fallback parsers
```

## Required preflight

Before implementation, verify and report:

```text
1. Current NarrativePayloadV1 fields.
2. Current NarrativePayload builder logic.
3. Which result-page sections currently consume narrative payload fields.
4. Which sections still use separate narrative sources instead of the shared payload.
5. Whether primary finding, body overview, health systems, patterns and next steps have explicit section intent.
6. Whether evidence boundaries exist per section.
7. Whether forbidden-claim constraints exist.
8. Whether current LLM validator can validate against the narrative payload.
9. Which gaps map directly to the §3.9 Layer B/Layer C contract.
10. Whether implementation can be bounded without rewriting the report compiler.
```

STOP if the brief cannot be matured safely without broad report compiler redesign.

## Target narrative brief model

The exact schema should follow repo conventions, but the target concept is:

```text
NarrativeBriefV1 / improved NarrativePayloadV1:
- report_story_priority
- primary_finding
- primary_finding_reason
- confidence_summary
- evidence_for
- evidence_against
- missing_or_limiting_evidence
- system_context
- marker_context
- next_step_intent
- section_intents
- section_visibility
- allowed_claims
- forbidden_claims
- required_caveats
- evidence_boundaries
- future_llm_translation_constraints
```

Do not add fields blindly.

Only add fields that are:

```text
- useful to Layer B
- testable
- grounded in existing outputs
- safe for deterministic renderer or future LLM translator
- not duplicating existing DTO fields unnecessarily
```

## Required narrative sections

At minimum, the brief should be able to govern these sections:

```text
1. Hero / main finding
2. Primary finding and why
3. What’s working well
4. Health systems context
5. Patterns across your body
6. Marker evidence
7. Missing evidence / confidence limitations
8. What to do next
9. Technical / clinician detail
```

For each section, define:

```text
- purpose
- allowed evidence sources
- default visibility
- claim boundaries
- caveats
- whether future LLM translation may rewrite it
```

## Score hierarchy requirement

The brief should define score hierarchy guidance.

At minimum:

```text
- system scores are domain-level summaries
- marker scores should not dominate the main narrative
- evidence completeness qualifies score confidence
- limited coverage must be surfaced when relevant
- hidden/support evidence must not be presented as score basis
- overall score, if present, must not compete with primary finding
```

Do not change the score calculations in this sprint.

## Relationship to KB-UTIL-1 carry-forward

This sprint may prepare structured locations for:

```text
- hypotheses
- contradiction markers
- confirmatory test rationale
```

But it must not surface those directly unless:

```text
- Layer B has a governed field
- wording boundaries are defined
- tests prove no unsafe exposure
- frontend remains render-only
```

It is acceptable to leave CF-KBUTIL1-002 open if safe surfacing requires a future sprint.

## Required tests

Add or update tests proving:

```text
1. Narrative brief has section-specific intent for required sections.
2. Primary finding and health systems context have distinct purposes.
3. Evidence boundaries prevent hidden/support subsystems being described as score basis.
4. Missing evidence / confidence limitations are represented.
5. Score hierarchy guidance exists in Layer B, not frontend.
6. Future LLM translation constraints exist and prohibit reasoning.
7. Frontend does not infer narrative priority.
8. No raw Pass 3 runtime reads are introduced.
9. No internal IDs/source traces are exposed.
10. ARCH-RT-6 validator still passes.
```

Always run:

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
```

Also run targeted tests for:

```text
narrative_payload_v1
narrative_payload_builder_v1
domain_narrative_wave1
report_compiler_v1
validator_v2 if touched
frontend result components if touched
```

## Manual validation target

After implementation, inspect a latest-engine regenerated result.

Use either the latest regenerated analysis or regenerate from:

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
- the page still renders
- no internal IDs/traces visible
- no stale snapshot is mistaken for latest output
- primary finding and health system cards no longer feel like independent competing narratives
- any changed narrative fields improve coherence without deleting useful analysis
```

If this sprint is mostly contract/brief scaffolding and not intended to visibly change the UI, state that clearly in the report.

## STOP conditions

STOP and report if:

```text
1. Narrative brief maturity requires broad report compiler redesign.
2. Current payload contracts are too unstable to extend safely.
3. Implementation would require frontend clinical inference.
4. Implementation would wire LLM translation.
5. Implementation would expose raw Pass 3 hypotheses/contradictions unsafely.
6. Score hierarchy requires changing clinical score calculations.
7. Hidden/support subsystems would be reintroduced as score basis.
8. ARCH-RT-6 validator fails.
9. Sprint drifts into full UX redesign.
```

## Required deliverable

Create:

```text
docs/audit-papers/LAYER-B-1_narrative_brief_maturity_report.md
```

The report must include:

```text
- preflight findings
- current narrative payload gaps
- fields added or deferred
- Layer B changes
- Layer C changes, if any
- LLM boundary confirmation
- score hierarchy handling
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
3. narrative payload preflight findings
4. schema/contract changes
5. builder changes
6. validation changes
7. frontend changes, if any
8. tests added/updated
9. test commands run
10. test results
11. manual browser validation result
12. confirmation no LLM translation was wired
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
- current branch matches work/LAYER-B-1-narrative-brief-maturity
- all changed files are tied to this sprint
- carry-forward register has been updated if required
- no LLM translation is wired
- no frontend clinical inference is introduced
- no raw Pass 3 runtime reads are introduced
- no scoring rails or thresholds are changed
- no ambiguous stash exists
- latest commit contains only in-scope work
```

## Success criteria

This sprint is complete only if:

```text
1. Narrative brief maturity is materially improved or explicitly bounded/deferred.
2. Section-specific intent and evidence boundaries are represented in Layer B.
3. Future LLM translation constraints are clearer.
4. Frontend remains render-only.
5. Hidden/support evidence is not misrepresented as score basis.
6. Score hierarchy is clarified at the brief/contract level.
7. Carry-forward register is updated.
8. ARCH-RT-6 validator passes.
9. Tests prove the narrative brief contract.
10. Automation Bus gate passes.
```

```
```
