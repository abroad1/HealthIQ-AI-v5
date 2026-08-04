# HealthIQ AI — Day-One Architecture Rework Sprint Plan vNEXT.1

**Supersedes (sequencing only):** `healthiq_day_one_architecture_rework_sprint_plan_vNEXT.md`
**Historical provenance:** `healthiq_day_one_architecture_rework_sprint_plan_FINAL.md`
**Does not reopen:** any ratified clinical, product, or approved architecture decision. The 109-scenario approval estate, the clinician-first product ratification, and the no-forced-lead rule stand unchanged.
**Status:** Provisional — presented for Anthony/GPT review alongside `CLIN-PRIORITY-CORE-1_v1_1`
**Prepared by:** Claude Code, Stage 0 architecture and package-definition review

## 1. Why this revision

vNEXT correctly re-sequenced the programme around the ratified Cross-Domain Clinical Findings and Prioritisation objective, but carried forward two framing errors corrected here:

1. It treated several genuinely optional or explicitly out-of-scope capabilities (comprehensive Tier 0 escalation, emergency routing, FIB-4/CV-risk activation, specialist pregnancy interpretation, broad questionnaire redesign) as `ESSENTIAL_BEFORE_RELEASE`, which overstates HealthIQ's product boundary as a **secondary, consumer-facing interpretation application** — it does not operate an emergency service, does not receive results as the primary clinical recipient, and does not monitor user follow-through.
2. It implied the core package was building toward a future HealthIQ-operated Tier 0 operational escalation pathway. It is not. Serious findings must remain fully visible, correctly tiered, and never downgraded — but "Tier 0" in this programme is a **clinical severity/urgency classification carried in the data model**, not a service HealthIQ will one day operate.

No clinical rule, threshold, or the ratified prioritisation model is touched by this revision.

## 2. Governing product boundary (restated)

HealthIQ is a secondary, consumer-facing blood-test interpretation application. Users upload results produced elsewhere. HealthIQ interprets, consolidates, prioritises, explains, and supports informed discussion with a healthcare professional. It does not provide testing, does not replace the original lab or requesting clinician, does not diagnose autonomously, does not prescribe or manage treatment, does not operate an emergency escalation service, and does not monitor whether a user acts on advice.

## 3. Preserved: architecture work already completed

Unchanged from vNEXT §2: Sprint 0 (bilirubin fix), Sprint 1 (`ARCH-RT-0` inventory/identity), and the `activation_key` multi-frame registry (repository-confirmed live in `SignalRegistry`, `signal_evaluator.py:26-202`) — re-verify at Phase 0, do not re-implement.

## 4. Next implementation outcome

> Construct, consolidate, prioritise and surface current and supported longitudinal clinical findings in the already-approved clinical priority order.

Delivered by one bounded package: **`CLIN-PRIORITY-CORE-1`** (revised definition: `CLIN-PRIORITY-CORE-1_cross_domain_clinical_findings_and_prioritisation_v1_1.md`).

## 5. Minimum safe sprint count and anti-micro-sprint position

**One implementation package, unchanged from vNEXT §5.** No new sub-sprint is created by this revision — the corrections below narrow what is *in* the follow-on register, not the shape of the core package. Internal checkpoints (§6) are unchanged in structure; checkpoint 3's content is narrowed per §7 of this document and of the revised package definition.

## 6. Internal checkpoints (within `CLIN-PRIORITY-CORE-1`)

1. **Phase 0 verification** — `SignalRegistry` re-verification; resolve whether a live FIB-4/CV-risk computation path exists (informs quarantine posture, not activation).
2. **Hepatic pilot** — canonical model, identity, concern-construction service, serious-result state gate (§7 below), DTO extension, hepatic compiled artefact, hepatic acceptance scenarios.
3. **Estate rollout** — remaining five domains; full 109-scenario estate passing.
4. **Longitudinal integration** — bounded per §8 below: specimen provenance, comparable-unit validation, prior-linking, numeric delta, the specific governed change-defined findings with an explicit authoritative window, persistence/worsening as within-tier ordering, absent-history-is-not-stability. No trend-tier-promotion, no generic band-movement-as-finding.
5. **Frontend and closure** — DTO consumption, `technical_tiebreak_lead` retirement, full regression, closure documentation.

## 7. Corrected serious-result scope (replaces vNEXT's Tier 0 framing)

The core package does **not** build toward a future HealthIQ-operated Tier 0 escalation service. It must:

- preserve the governed severity, urgency, and priority of serious findings exactly as the ratified contract and ruleset assign them;
- never silently downgrade, suppress, or convert a serious finding to a no-concern output;
- expose a **bounded serious-result state** to the presentation layer (a data classification, not a workflow);
- support consumer-safe wording directing the user to seek appropriate professional medical advice;
- make clear in that wording that HealthIQ cannot determine whether the result has already been reviewed by the originating provider;
- not route users to any service;
- not manage escalation of any kind;
- not monitor whether the user responds;
- not create territory-specific emergency workflows.

Internal "Tier 0" terminology may remain in code and data models where the approved clinical contract itself uses it (contract §6.2, §17) — that is the contract's own severity/urgency vocabulary, not a commitment to build an escalation service. No document produced by this package may describe the implementation as preparing for, or a precursor to, a future comprehensive Tier 0 operational pathway.

## 8. Corrected longitudinal scope

**In scope**, on existing authority only: specimen dates and source provenance; comparable-unit validation; prior-result linking (`link_prior_snapshot_insight_graphs`); current-vs-prior numeric change (`comparable_lab_delta`); the specific governed change-defined findings whose criterion and valid time window are already authoritative in the ratified domain rulesets — identified in §9 of the revised package definition; persistence/worsening as a within-tier ordering consideration (contract §7.2 point 5); the absent-history-is-not-stability invariant (contract §12.2, §18.9); transparent trend evidence surfaced in the DTO.

**Out of scope for this package:** invented trend thresholds; trend-triggered tier promotion (no governed override exists for any domain — confirmed by inspection, not re-litigated here); treating generic score-band movement (`state_transition_engine.py`'s `low_band`/`mid_band`/`high_band` transitions) as itself a clinical finding; comprehensive trend interpretation for every biomarker merely because historical values exist; any new medical adjudication cycle. Where a domain has no explicit, authoritative trend rule for a given finding, the package retains the historical data and evidence but does not change that finding's priority or classification.

## 9. Revised follow-on register

| Item | Classification | Note |
|---|---|---|
| Comprehensive Tier 0 operational escalation pathway | `OUT_OF_SCOPE_DISCARD` | Not a HealthIQ product function; see §7 |
| Emergency-service routing | `OUT_OF_SCOPE_DISCARD` | Outside product boundary entirely |
| Monitoring whether users act on advice | `OUT_OF_SCOPE_DISCARD` | Outside product boundary entirely |
| Consumer-facing autonomous disease diagnosis | `OUT_OF_SCOPE_DISCARD` | Contract §22, clinician-first §14 already prohibit this permanently, not just pending R4 |
| Cardiovascular-risk calculation activation | `RETAIN_QUARANTINED` | Capability may exist in future; quarantine (R2) preserved by this package, not a release blocker for the rest of HealthIQ |
| FIB-4 calculation activation | `RETAIN_QUARANTINED` | Same treatment as CV-risk (R3) |
| Narrow consumer disease-terminology policy | `ESSENTIAL_BEFORE_RELEASE` | Distinct from full disease-*diagnosis* (which is discarded, not deferred) — this is the bounded wording-set decision clinician-first §14 already substantially specifies |
| Intended-purpose, claims and population wording | `ESSENTIAL_BEFORE_RELEASE` | R5 |
| Broad questionnaire redesign | `OPTIONAL_FUTURE_CAPABILITY` | Downgraded from essential; see next row for the bounded exception |
| Specific questionnaire fields proven necessary for active governed rules | `REQUIRES_DEEPER_INSPECTION` | Promote individual fields to essential only where repository evidence proves a specific in-scope rule cannot run without them — not a blanket questionnaire programme |
| Specialist pregnancy interpretation engine | `OUT_OF_SCOPE_DISCARD` | For the current product; not a future release gate |
| Pregnancy-aware limitation or withholding | Retained, scoped | Only where an active in-scope rule currently requires the contract §26 interim behaviour (explicit out-of-scope/withheld output) — not a broader pregnancy programme |
| R6 (renal/electrolyte release requiring a future Tier 0 operational pathway) | **Retired as obsolete** | The premise (a future HealthIQ-operated Tier 0 pathway) no longer applies under the reset product boundary (§7); renal/electrolyte findings are represented with correct severity/urgency and the bounded serious-result state like every other domain |
| Laboratory-provider integrations | `OPTIONAL_FUTURE_CAPABILITY` | Not part of this programme |
| Trend-triggered tier-promotion override rule | `REQUIRES_DEEPER_INSPECTION` | No governed override exists in any domain ruleset; needs a future bounded medical adjudication if pursued |
| Health Systems Card evidence vertical slice | `OPTIONAL_FUTURE_CAPABILITY` | Unchanged from vNEXT |
| Compiled hypothesis / root-cause slice | `OPTIONAL_FUTURE_CAPABILITY` | Unchanged from vNEXT |
| Frontend UI built around `technical_tiebreak_lead` | `ESSENTIAL_TO_CORE_FUNCTION` | Must be retired within this package's Checkpoint 5, not deferred |
| Existing cluster-level arbitration engine (`precedence_engine.py`, `arbitration_engine.py`) | `RETAIN_QUARANTINED` from this programme | Left running for its existing purpose; not modified unless repository evidence later proves a strictly necessary integration point |
| Final regulatory release approval | `ESSENTIAL_BEFORE_RELEASE` | Umbrella item; the specific capability-level items above (R2/R3 quarantine, R4 wording, R5 intended-purpose) are its actual content |

**No optional or quarantined capability in this table blocks release of the rest of HealthIQ.** Only the narrow, bounded items marked `ESSENTIAL_BEFORE_RELEASE` do, and each is a specific wording/documentation decision, not an open-ended programme.

## 10. Dependencies that block implementation versus release only

**Block implementation:** none outstanding, unchanged from vNEXT.

**Block release only:** narrow disease-terminology wording (R4-scoped, not full diagnosis policy); intended-purpose/claims/population wording (R5); the specific questionnaire fields individually proven necessary (not a redesign programme). CV-risk and FIB-4 activation are explicitly **not** release blockers for the rest of HealthIQ — they are independently quarantined, optional capabilities.
