---
work_id: CLIN-PRIORITY-CORE-1
branch: feature/clin-priority-core-1
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
status: PACKAGE_DEFINITION_ONLY — NOT AN AUTOMATION BUS PROMPT
supersedes: CLIN-PRIORITY-CORE-1_cross_domain_clinical_findings_and_prioritisation.md
---

# CLIN-PRIORITY-CORE-1 v1.1 — Cross-Domain Clinical Findings and Prioritisation

**This is a bounded package definition for later Automation Bus Stage 1/Stage D prompt authoring. It is not `automation_bus/latest_cursor_prompt.md` and does not authorise implementation, Cursor prompt authoring, or execution.**

## 1. Product outcome

Construct, consolidate, prioritise and surface current and supported longitudinal clinical findings in the already-approved clinical priority order, within HealthIQ's product boundary as a secondary, consumer-facing blood-test interpretation application.

## 2. Product boundary (governs every decision in this package)

HealthIQ interprets clinically meaningful findings, combines related biomarkers, identifies cross-domain and longitudinal patterns, prioritises what deserves attention, explains results in consumer-safe language, and supports informed discussion with a healthcare professional. HealthIQ does not provide testing, does not replace the originating lab or clinician, does not diagnose autonomously, does not prescribe or manage treatment, does not operate an emergency escalation service, and does not monitor whether a user acts on advice.

## 3. In-scope runtime behaviour

```text
governed current and historical biomarker results
→ governed clinical findings                                [new: ClinicalFinding model + concern-construction service]
→ consolidation and relationship resolution                  [new: same-domain + cross-domain combination logic]
→ current-severity, urgency and bounded trend-aware priority  [new tier/urgency assignment + narrowly governed trend integration, §9]
→ lead / co-lead / no-forced-lead decision                    [new: replaces technical_tiebreak_lead logic]
→ visible ordered concern set, with bounded serious-result state [new — see §8]
→ supporting and contextual relationships                      [new: Tier 3 nesting, orphan handling]
→ structured provenance-rich DTO                               [extend: InsightGraphV1, AnalysisDTO — additive field]
→ frontend render-only                                          [extend: consume new field; retire tiebreak-specific UI logic]
```

## 4. Governed source artefacts

Unchanged from the prior version: contract v0.6.3; cross-domain ruleset v0.5; HMR adjudication register v0.4; six-domain closure report v0.4; acceptance-scenario medical adjudication v0.1; acceptance-scenario approval pack v1.2 (109 scenarios, unchanged, not reopened); clinician-first product ratification v1.0, including the approved no-forced-lead rule; `CLIN-PRIORITY-ARCH-HARDEN-1` (approved); ADR-RT-001 through ADR-RT-004; `CLIN-PRIORITY-IMPLEMENTATION-RESET-1_repository_inspection.md`.

## 5. Exact repository paths

Unchanged from the prior version (§4 of that document): reused unmodified — `signal_evaluator.py` (`SignalRegistry`), `longitudinal_numeric_v1.py`, `snapshot_linker.py`, `runtime_context_evaluator.py`. Extended additively — `insight_graph_v1.py`, `insight_graph_builder.py`, `results.py`, `WhyThisLeadWonSection.tsx`, `PrimaryFindingAndWhy.tsx`. New — `clinical_finding.py` (models), `concern_constructor.py` (service), new compiled prioritisation artefact, new scenario-runner harness modelled on `run_arbitration_scenarios.py`. **Not touched** unless repository evidence later proves a strictly necessary integration point — `precedence_engine.py`, `state_engine.py`, `arbitration_engine.py`.

## 6. DTO contract

Unchanged: additive `InsightGraphV1.clinical_concern_set: Optional[ConsolidatedConcernSet]`, propagated into `AnalysisDTO`. No existing field renamed, removed, or restructured.

## 7. Frontend render-only boundary

Unchanged: frontend renders tier, ordering, lead/co-lead/no-forced-lead state, serious-result state (§8), withheld status, and provenance labels exactly as supplied. `technical_tiebreak_lead` branch in `WhyThisLeadWonSection.tsx` retired and replaced with `no_forced_lead` per `XD-AS-32`.

## 8. Serious-result scope (corrected — replaces prior version's Tier 0-pathway framing)

This package does not build toward a future HealthIQ-operated emergency escalation service. It must:

- preserve governed severity, urgency, and priority for serious findings exactly as assigned by the ratified contract and ruleset;
- never silently downgrade, suppress, or convert a serious finding to no-concern;
- expose a bounded `serious_result_state` field on `ClinicalFinding` (a data classification consumed by presentation, not a workflow trigger);
- support consumer-safe wording directing the user to seek appropriate professional medical advice;
- state clearly, in that wording, that HealthIQ cannot determine whether the result has already been reviewed by the originating provider;
- not route the user to any service, not manage escalation, not monitor response, not create territory-specific emergency workflows.

Internal "Tier 0" data-model terminology is retained where the ratified contract itself uses it (contract §6.2, §17) — it names a severity/urgency classification the contract defines, not a commitment this package makes to build an escalation service. No artefact produced under this package may describe the work as preparing for a future comprehensive Tier 0 operational pathway (R1, retired as a framing for this package per the revised sprint plan §7; R1 remains a genuinely open regulatory/legal question, but this package neither depends on nor anticipates its resolution).

## 9. Longitudinal scope (corrected — narrowed to explicit authority)

**In scope, on existing authority only:**

- Specimen dates and source provenance.
- Comparable-unit validation (`comparable_lab_delta`'s existing unit-match enforcement).
- Prior-result linking (`link_prior_snapshot_insight_graphs`).
- Current-versus-prior numeric change.
- The following governed change-defined findings, each with an explicit, authoritative criterion and time window already present in the ratified domain rulesets — no new threshold is created; the count below is definitional, not a claim of current implementation:
  1. **Acute kidney injury** (renal ruleset `RE-T1`) — NICE NG148: creatinine rise ≥26 µmol/L within 48 hours, or ≥50% within 7 days. `[E]`.
  2. **CKD chronicity** (renal ruleset `RE-S-2`) — sustained abnormality ≥3 months required before CKD is established. `[E]`.
  3. **Statin-monitoring change** (hepatic ruleset `HEP-T1`) — stop-consideration only if enzymes double within 3 months of statin start. `[E]`.
  4. **Cytopenia chronicity/rate-of-change** (haematology ruleset `HAEM-T5`) — 12-month chronicity window, 3-month rate-of-change window. `[J]` — HealthIQ judgement, no cited UK source; implementable as already-adjudicated authority, consistent with how every other `[J]`-labelled item in the ratified package has been treated throughout this engagement, with the lower evidence grade preserved in provenance.
  5. **Subclinical thyroid two-occasion confirmation** (thyroid ruleset `THY-T1`) — NICE NG145 requires two results ≥3 months apart before a subclinical treatment consideration. `[E]`.
  6. **HbA1c/diabetes confirmation spacing** (cardiometabolic ruleset `CN-T2`/`CN-T3`) — HbA1c reflects ~3 months of glycaemia; two values <3 months apart are not independent timepoints; diabetes diagnosis on a single result requires confirmation. `[C]`.
- Persistence or worsening trend as a **within-tier ordering consideration only** (contract §7.2 point 5) — never a tier-promotion mechanism.
- The absent-history-is-not-stability invariant (contract §12.2, §18.9) as a hard, testable rule.
- Transparent trend evidence surfaced in the DTO, whether or not it changes a finding's classification.

**Out of scope for this package:**

- Invented trend thresholds of any kind.
- Trend-triggered tier promotion — no domain ruleset or the cross-domain ruleset enumerates a governed override for this; not implemented, not approximated.
- Treating generic score-band movement (`state_transition_engine.py`'s `low_band`/`mid_band`/`high_band` transitions) as itself a clinical finding — that engine's output may inform presentation-layer framing (e.g. "improving"/"worsening" language) only where a governed rule above already licenses a trend effect; it is never a substitute for one.
- Comprehensive trend interpretation for every biomarker merely because historical values exist.
- Any new medical adjudication cycle.

Where a domain has no explicit, authoritative trend rule for a given finding, the package retains the historical data and evidence in the DTO but does not change that finding's priority, tier, or urgency.

## 10. Scenario-based acceptance strategy (corrected — two separate coverage statements)

The 109-scenario approval-pack-v1.2 estate remains the governing current-state and constrained-state acceptance specification, unchanged and not reopened. It is **not** claimed to independently prove all longitudinal behaviour — only two of the 109 scenarios contain both an explicit historical value and an expected trend-dependent outcome:

- `RE-AS-3` (creatinine 145, prior 70 six days ago → AKI, same day) — proves governed rule 1 above.
- `RE-AS-5` (eGFR 52, prior 54 four months ago → stable CKD G3a) — proves governed rule 2 above.

**Two coverage statements are maintained separately, and neither substitutes for the other:**

1. **`APPROVED_SCENARIO_ESTATE_COVERAGE`: 109/109.** Every scenario in approval pack v1.2 §7-§9 becomes one fixture in the new scenario-runner harness (modelled on `run_arbitration_scenarios.py`), asserting the full field set recorded there. This is the current-state and constrained-state acceptance gate for Checkpoints 2-3.
2. **`GOVERNED_LONGITUDINAL_RULE_COVERAGE`: 6 governed rules identified in §9 above; 2 of 6 already have a scenario in the approved estate (`RE-AS-3`, `RE-AS-5`); the remaining 4 require new test fixtures authored during Checkpoint 4 against already-governed authority — not invented, not new medical adjudication, and not created by this documentation task. This statement is the longitudinal-specific acceptance gate for Checkpoint 4 and is reported separately from item 1 at closure.**

No new longitudinal scenario is authored by this task, per the governing instruction.

Scenario classification (unchanged from the prior version, §8 of that document): direct end-to-end (all 109); parametric families (same-day co-equal grouping, vitamin D band family, Tier 0 specification-only family); quarantine/constrained-state assertions (`XD-AS-17`/`-18`/`-36`, `XD-AS-35`); ordering/consolidation/role proofs (`XD-AS-25`, `XD-AS-32`, `HEP-AS-14`/`RE-AS-13`); missing-data/indeterminate proofs (`XD-AS-33`/`-34`, `HAEM-AS-6`, `RE-AS-7`); trend proofs (`RE-AS-3`, `RE-AS-5`, plus the 4 new fixtures at Checkpoint 4).

## 11. Exclusions

Comprehensive Tier 0 operational escalation pathway (retired as this package's framing, §8); emergency-service routing; user follow-up monitoring; FIB-4 activation (quarantine preserved, activation excluded); cardiovascular-risk calculation activation (quarantine preserved, activation excluded); consumer-facing autonomous disease diagnosis; specialist pregnancy interpretation engine; broad questionnaire redesign (individual proven-necessary fields excepted per the revised sprint plan §9); laboratory-provider integrations; final regulatory release approval; trend-triggered tier promotion (§9); comprehensive trend interpretation beyond the six governed rules in §9.

## 12. Risk classification

`HIGH` — unchanged; touches Intelligence Core.

## 13. Change type

`MIXED` — unchanged.

## 14. Execution model

`TWO_PHASE_START_FINISH` — unchanged. START through Checkpoint 3 (109/109 scenarios passing), independent STOP review, FINISH covering Checkpoints 4-5 (longitudinal integration, frontend, closure).

## 15. Internal checkpoints

1. **Phase 0 verification** — `SignalRegistry` re-verification; resolve whether a live FIB-4/CV-risk computation path exists (informs quarantine posture only — quarantine is retained either way, per §11).
2. **Hepatic pilot** — model, identity, concern-construction service, serious-result state (§8), DTO extension, hepatic compiled artefact, hepatic acceptance scenarios.
3. **Estate rollout** — remaining five domains; `APPROVED_SCENARIO_ESTATE_COVERAGE` 109/109.
4. **Longitudinal integration** — the six governed rules in §9; `GOVERNED_LONGITUDINAL_RULE_COVERAGE` 6/6 implemented, with the 2 already-scenario-proven plus 4 new fixtures built against existing authority.
5. **Frontend and closure** — DTO consumption, `technical_tiebreak_lead` retirement, full regression, closure documentation, Build Deliverables Register update, both coverage statements reported at closure.

## 16. STOP conditions

- Any scenario in the 109-scenario estate, or any of the six §9 longitudinal rules, cannot be implemented without inventing a new threshold, tier, urgency band, override, or product rule — stop, do not invent.
- Phase 0 finds a live, user-facing FIB-4/CV-risk computation path — stop before Checkpoint 2, escalate for explicit quarantine-implementation scope; this does not reopen the release-blocker status of R2/R3, which remain `RETAIN_QUARANTINED` per the revised sprint plan.
- Any change would require modifying `precedence_engine.py`, `arbitration_engine.py`, or the questionnaire schema beyond an individually-proven-necessary field — stop, out of scope.
- A domain's serious-result classification cannot be represented without implying an operational escalation commitment — stop, do not approximate a service HealthIQ does not operate.
- Checkpoint 3 reveals a domain ruleset genuinely irreconcilable with the ratified cross-domain package — stop and escalate, do not adjudicate.

## 17. Success criteria

Unchanged in substance from the prior version, with §8/§9's corrected scope: `ClinicalFinding`/`ConsolidatedConcernSet` additive and provenance-traceable; concern-construction service reproduces all 109 approval-pack-v1.2 scenarios; serious findings preserved, never downgraded, bounded `serious_result_state` exposed without implying an escalation service; no-forced-lead behaviour matches `XD-AS-32`; the six §9 governed longitudinal rules implemented and reported separately from scenario-estate coverage; DTO extension additive; frontend render-only; quarantines (R1-R6 framing corrected per §8; R2/R3 retained quarantined) intact.

## 18. Follow-on items

Per the revised sprint plan §9: `REQUIRES_DEEPER_INSPECTION` — trend-tier-promotion override, individually-proven-necessary questionnaire fields; `RETAIN_QUARANTINED` — CV-risk activation, FIB-4 activation, existing cluster-level arbitration engine; `OPTIONAL_FUTURE_CAPABILITY` — broad questionnaire redesign, Health Systems Card slice, compiled hypothesis/root-cause slice, laboratory-provider integrations; `ESSENTIAL_BEFORE_RELEASE` — narrow disease-terminology wording, intended-purpose/claims/population wording; `OUT_OF_SCOPE_DISCARD` — comprehensive Tier 0 escalation pathway, emergency-service routing, user-response monitoring, autonomous disease diagnosis, specialist pregnancy interpretation engine.
