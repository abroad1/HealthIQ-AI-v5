# LAUNCH-CORE-1 — Results Page Card Coherence and Consumer Copy Report

**Work package:** `LAUNCH-CORE-1_results_page_card_coherence_and_consumer_copy`  
**Generated:** 2026-05-30  
**UAT reference:** `docs/audit-papers/LAUNCH-CORE-0_results_page_human_uat_investigation.md`

## UAT issues addressed

| Issue | Fix |
|-------|-----|
| Blood sugar card summary vs subsystem marker count mismatch | Backend derives completeness from compiled subsystem union |
| High score with limited evidence misleading | Score qualification line when coverage/confidence limited |
| Raw marker-role enum chips | Consumer-safe role label map |
| “Homocysteine Elevation Context” in hero/narrative | Interim scrub → “Raised homocysteine pattern” |
| `Mcv` marker ref formatting | Reuse `formatBiomarkerDisplayName` in PrimaryFindingAndWhy |
| Narrative mojibake (`â` sequences) | `scrubMojibakeArtifacts` in retail narrative pipeline |
| HbA1c upload-fidelity “not scored separately” contradiction | Wording aligned to panel-fidelity note |

## Root cause — completeness mismatch

Card summary used `_evidence_completeness_for_rail()` (rail scored count + domain missing list). Expanded detail used compiled subsystem partition (glycaemic + insulin metabolic). **Fix:** `_evidence_completeness_from_subsystems()` when Wave 1 subsystem rows exist.

## Before / after — Blood sugar completeness

| | Before | After |
|---|--------|-------|
| Summary line | `1 of 3 expected markers included` | `2 of 4 expected markers included` |
| Subsystems (unchanged) | HbA1c + Triglycerides included; Glucose + Insulin missing | Same |

## Before / after — role chip labels

| Enum | Before | After |
|------|--------|-------|
| `score_contributor` | `score contributor` | `Used in this score` |
| `confidence_contributor` | `confidence contributor` | `Supports confidence` |
| `contextual_marker` | `contextual marker` | `Context marker` |

## Before / after — internal prose label

| Before | After |
|--------|-------|
| `Homocysteine Elevation Context: warrants attention…` | `Raised homocysteine pattern: warrants attention…` |

## Before / after — MCV formatting

| Before | After |
|--------|-------|
| `Mcv` | `MCV` |

## Encoding / mojibake

Display-boundary sanitisation in `scrubMojibakeArtifacts` + full `scrubConsumerRetailNarrative` pipeline. Historical persisted records may still contain artefacts until recompiled; sanitisation applies at render time.

## Files changed

| Layer | Path |
|-------|------|
| Backend | `backend/core/analytics/domain_score_assembler.py` |
| Backend tests | `backend/tests/unit/test_launch_core1_card_coherence.py` |
| Frontend lib | `cardEvidenceConsumerCopy.ts`, `retailNarrativeSanitize.ts`, `wave1HealthSystemCardDisplay.ts`, `uploadPanelFidelity.ts`, `clinicianPage1Placeholders.ts` |
| Frontend components | `Wave1SubsystemEvidenceSection.tsx`, `Wave1DomainCards.tsx`, `PrimaryFindingAndWhy.tsx` |
| Frontend tests | `cardEvidenceConsumerCopy.test.ts`, `retailNarrativeSanitize.test.ts`, `Wave1SubsystemEvidenceSection.test.tsx` |

## ARCH-RT-6 guardrails

`python backend/scripts/validate_day_one_architecture.py` — **PASS** (no PSI/root-cause/SignalRegistry changes).

## Tests run

```text
python -m pytest backend/tests/unit/test_launch_core1_card_coherence.py -q
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
npm test -- --testPathPattern="cardEvidenceConsumerCopy|retailNarrativeSanitize|Wave1Subsystem|uploadPanelFidelity" --passWithNoTests
```

## Manual browser validation

Target analysis `18e14232-9f93-45e6-820c-004ab5a16235` — **recommended post-merge** (requires local backend + auth). Automated tests cover DTO assembly and render paths; full browser re-run documented in LAUNCH-CORE-0 method.

## Remaining risks

| Risk | Mitigation |
|------|------------|
| Compiler still emits internal display names | Interim scrub list; follow-on narrative compiler sprint (LAUNCH-CORE-0 R2) |
| Persisted historical mojibake | Render-time sanitisation only |
| Score/evidence coupling policy | Qualification copy only; thresholds unchanged |

## Confirmations

- No PSI / root-cause / SignalRegistry / SignalEvaluator changes
- No raw internal IDs/traces exposed
- Frontend does not infer clinical meaning (enum map only)
- ARCH-RT-6 validator passes
