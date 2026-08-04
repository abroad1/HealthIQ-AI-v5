---
work_id: CLIN-PRIORITY-CORE-1
branch: feature/clin-priority-core-1
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
status: PACKAGE_DEFINITION_ONLY — NOT AN AUTOMATION BUS PROMPT
---

# CLIN-PRIORITY-CORE-1 — Cross-Domain Clinical Findings and Prioritisation

**This is a bounded package definition for later Automation Bus Stage 1/Stage D prompt authoring. It is not `automation_bus/latest_cursor_prompt.md` and does not authorise implementation, Cursor prompt authoring, or execution.**

## 1. Product outcome

HealthIQ surfaces current and longitudinal blood-test findings in the already-ratified clinical priority order: consolidated clinical findings, correctly tiered and time-banded, with a governed lead/co-lead/no-forced-lead presentation, full provenance, and correct fail-closed handling of Tier 0, quarantined capabilities, and incomplete questionnaire context.

## 2. In-scope runtime behaviour

```text
governed current and historical biomarker results
→ governed clinical findings                      [new: ClinicalFinding model + concern-construction service]
→ consolidation and relationship resolution        [new: same-domain + cross-domain combination logic]
→ current-severity, urgency and trend-aware prioritisation  [new tier/urgency assignment + governed trend integration]
→ lead / co-lead / no-forced-lead decision          [new: replaces technical_tiebreak_lead logic]
→ visible ordered concern set                       [new]
→ supporting and contextual relationships            [new: Tier 3 nesting, orphan handling]
→ structured provenance-rich DTO                     [extend: InsightGraphV1, AnalysisDTO — additive field]
→ frontend render-only                                [extend: consume new field; retire tiebreak-specific UI logic]
```

## 3. Governed source artefacts

Medical/product authority (do not reopen): contract v0.6.3; cross-domain ruleset v0.5; HMR adjudication register v0.4; six-domain closure report v0.4; acceptance-scenario medical adjudication v0.1; acceptance-scenario approval pack v1.2 (109 scenarios — the governing acceptance specification, §7); clinician-first product ratification v1.0, including the approved no-forced-lead rule.

Architecture authority: `CLIN-PRIORITY-ARCH-HARDEN-1` (approved) §6-§11; ADR-RT-001 through ADR-RT-004; this package's own repository inspection (`CLIN-PRIORITY-IMPLEMENTATION-RESET-1_repository_inspection.md`).

Six domain rulesets are subordinate evidence, compiled only where incorporated/preserved/adjudicated by the documents above (architecture-hardening report §8 source-precedence rule — applies unchanged).

## 4. Exact repository paths (verified during inspection)

**Reused, unmodified:**
- `backend/core/analytics/signal_evaluator.py` (`SignalRegistry`, activation-key input)
- `backend/core/analytics/longitudinal_numeric_v1.py` (`comparable_lab_delta`)
- `backend/core/analytics/snapshot_linker.py` (`link_prior_snapshot_insight_graphs`)
- `backend/core/analytics/runtime_context_evaluator.py` (questionnaire disclosure-state pattern)

**Extended, additively:**
- `backend/core/contracts/insight_graph_v1.py` (`InsightGraphV1` — add `clinical_concern_set` field)
- `backend/core/analytics/insight_graph_builder.py` (add one call to the new concern-construction service)
- `backend/core/models/results.py` (`AnalysisDTO` — surface the new field)
- `frontend/app/components/results/WhyThisLeadWonSection.tsx`, `PrimaryFindingAndWhy.tsx` (consume new lead/no-forced-lead state; retire `technical_tiebreak_lead`-specific branches)

**New:**
- New model module (e.g. `backend/core/models/clinical_finding.py`) — `ClinicalFinding`, `ConsolidatedConcernSet`
- New service module (e.g. `backend/core/analytics/concern_constructor.py`)
- New compiled prioritisation artefact schema/compiler/loader, hepatic-domain scope first (Checkpoint 1), estate-wide by Checkpoint 2
- New scenario-runner harness, modelled on `backend/tools/run_arbitration_scenarios.py` and `backend/tests/unit/test_arbitration_scenario_runner.py`

**Not touched (verify, do not modify):**
- `backend/core/analytics/precedence_engine.py`, `state_engine.py`, `arbitration_engine.py` — existing cluster-level arbitration, left running for its own purpose
- `backend/core/contracts/clinician_report_v1.py`'s `RootCauseFindingV1`/WHY layer — separate concern, not this package's scope

## 5. DTO contract

Additive only. `InsightGraphV1.clinical_concern_set: Optional[ConsolidatedConcernSet]`, propagated into `AnalysisDTO`. No existing field renamed, removed, or restructured. Version-stamped (`clinical_prioritisation_contract_version`) per the architecture-hardening report §12 migration design.

## 6. Frontend render-only boundary

Frontend consumes `clinical_concern_set` and renders tier, ordering, lead/co-lead/no-forced-lead state, withheld status, and provenance labels exactly as supplied. No frontend component computes tier, ordering, or lead selection. `WhyThisLeadWonSection.tsx`'s `technical_tiebreak_lead` branch is retired and replaced with a `no_forced_lead` rendering path per `XD-AS-32`.

## 7. Current and longitudinal input handling

Current-result path: signals → concern-construction service → findings, as above. Longitudinal path: `link_prior_snapshot_insight_graphs` supplies up to 3 prior snapshots; `comparable_lab_delta` supplies numeric deltas; the concern-construction service applies the governed trend rules recorded in §8 of the inspection report (change-defined criteria and baseline-validity windows already authored in the ratified domain rulesets; absent-baseline-not-stability invariant; persistence/worsening as a within-tier ordering criterion). Trend-triggered tier promotion is explicitly **not** implemented in this package (no governed override exists — inspection report §7) and is recorded as follow-on item `TREND-TIER-PROMOTION-1`.

## 8. Scenario-based acceptance strategy

Governing specification: approval pack v1.2, 109 scenarios (§7-§9 of that document). Not 109 bespoke implementations — classified as follows:

| Class | Scenario examples | Approach |
|---|---|---|
| Direct end-to-end scenario tests | All 109 — each scenario becomes one fixture in the new scenario-runner harness (modelled on `arbitration_scenarios_v2.json`/`run_arbitration_scenarios.py`), asserting the full field set recorded in approval pack v1.2 | One harness, 109 fixtures, not 109 separate test implementations |
| Parametric coverage | Same-day co-equal grouping (`XD-AS-1`/`-7`/`-12`, `RE-AS-12`, `CN-AS-12`); vitamin D concentration-band family (`XD-AS-26`-`-30`); Tier 0 specification-only family (all Tier 0 scenarios) | One parametrised test per family, panel as parameter, rather than duplicated test logic |
| Quarantine / constrained-state assertions | `XD-AS-17`/`-18`/`-36` (CV-risk, FIB-4, disease-name); `XD-AS-35` (Tier 0 withheld) | Assert the constrained/withheld state and the corresponding prohibited-behaviour negative assertion, not a full activation path |
| Ordering/consolidation/role proofs | `XD-AS-25` (4-constituent nesting), `XD-AS-32` (no-forced-lead), `HEP-AS-14`/`RE-AS-13` (cross-domain boundary) | Direct assertions on the `ConsolidatedConcernSet` structure |
| Missing-data/indeterminate proofs | `XD-AS-33`/`-34`, `HAEM-AS-6`, `RE-AS-7` | Direct assertions on the missing-data/indeterminate state field |
| Trend proofs | Change-defined/baseline-window scenarios where present in the domain rulesets | Direct assertions using `comparable_lab_delta` fixtures with prior/current pairs |

**Full coverage demonstration:** the harness manifest (mirroring `run_arbitration_scenarios.py`'s existing manifest output) enumerates all 109 scenario IDs with pass/fail status; the package's Checkpoint 2 exit criterion is 109/109 passing with zero skips.

## 9. Exclusions

Per the governing prompt's exclusion list and inspection report §8: comprehensive Tier 0 operational escalation pathway; emergency-service routing; user follow-up monitoring; FIB-4 activation; cardiovascular-risk calculation activation; consumer-facing disease diagnosis; specialist pregnancy interpretation; broad questionnaire redesign; laboratory-provider integrations; final regulatory release approval. Trend-triggered tier promotion (no governed override exists — not invented here).

## 10. Risk classification

`HIGH` — touches Intelligence Core (finding construction, tiering, lead selection, output assembly) per Automation Bus SOP §3/§11.

## 11. Change type

`MIXED` — behavioural logic (concern-construction, tiering, lead selection) plus governed content (compiled prioritisation artefact). Governed under BEHAVIOUR controls per SOP §4.2.

## 12. Execution model

`TWO_PHASE_START_FINISH` — START through Checkpoint 2 (hepatic pilot + estate rollout, 109/109 scenarios passing), independent STOP review, then FINISH covering Checkpoints 3-4 (trend integration, frontend, closure) after authorised correction.

## 13. Internal checkpoints

1. **Phase 0 verification** — confirm `SignalRegistry` activation-key behaviour live; resolve the FIB-4/CV-risk live-path question (inspection report §10 risk 2) before any new code is written; confirm forbidden-path boundaries (no modification to `precedence_engine.py`/`arbitration_engine.py`, no questionnaire redesign, no Tier 0 pathway content).
2. **Hepatic pilot** — model, identity, concern-construction service, Tier 0 gate, DTO extension, hepatic compiled artefact, hepatic acceptance scenarios (approval pack v1.2 §9.1, plus `CONTRACT-FIX-1`/`HEP-AS-1`) passing.
3. **Estate rollout** — remaining five domains; full 109-scenario harness passing.
4. **Trend integration** — governed trend effects wired per §7 above; `TREND-TIER-PROMOTION-1` explicitly deferred, not implemented.
5. **Frontend and closure** — DTO consumption, `technical_tiebreak_lead` retirement, full regression, closure documentation, Build Deliverables Register update.

## 14. STOP conditions

- Any scenario in the 109-scenario estate cannot be made to pass without inventing a new threshold, tier, urgency band, override, or product rule — stop and return to GPT/HMR, do not invent.
- The Phase 0 FIB-4/CV-risk verification finds a live, user-facing computation path — stop before Checkpoint 1 and escalate for explicit quarantine-implementation scope, do not silently leave it running.
- Any change would require modifying `precedence_engine.py`, `arbitration_engine.py`, or the questionnaire schema — stop, these are explicitly out of scope.
- Tier 0 representation cannot be made unreachable by default without touching R1-governed operational content — stop, do not approximate an operational pathway.
- Six-domain rollout (Checkpoint 3) reveals a domain ruleset genuinely irreconcilable with the ratified cross-domain package in a way the architecture-hardening report's source-precedence rule cannot resolve — stop and escalate, do not adjudicate.

## 15. Success criteria

- `ClinicalFinding`/`ConsolidatedConcernSet` models exist, additive, fully provenance-traceable.
- Concern-construction service deterministically reproduces all 109 approval-pack-v1.2 scenarios.
- Tier 0 rules evaluated and provably withheld, never demoted, auditable.
- No-forced-lead behaviour matches `XD-AS-32` exactly; `technical_tiebreak_lead` retired.
- Governed trend effects implemented per §7; trend-tier-promotion explicitly absent, not approximated.
- DTO extension is additive; no existing consumer breaks.
- Frontend remains render-only; no client-side tier/order/lead computation.
- Full regression suite passes; quarantines (R1-R6) remain intact and unreachable.

## 16. Follow-on items

Per the revised sprint plan §7: `TREND-TIER-PROMOTION-1` (`REQUIRES_DEEPER_INSPECTION`); Tier 0 operational pathway, disease-name release, CV-risk/FIB-4 activation, population/intended-purpose wording, renal/electrolyte Tier 0-suppressed release, questionnaire remediation (all `ESSENTIAL_BEFORE_RELEASE`, none blocking this package); Health Systems Card and compiled hypothesis/root-cause work (`OPTIONAL_FUTURE_CAPABILITY`, unblocked but not sequenced here).
