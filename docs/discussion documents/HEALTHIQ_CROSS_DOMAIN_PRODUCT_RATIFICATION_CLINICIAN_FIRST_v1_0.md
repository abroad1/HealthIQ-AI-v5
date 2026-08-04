---
document_id: HEALTHIQ_CROSS_DOMAIN_PRODUCT_RATIFICATION_CLINICIAN_FIRST
version: "1.0"
status: PRODUCT_RATIFIED
ratifier: Anthony
ratification_date: "2026-08-03"
ratification_method: EXPLICIT_HUMAN_RATIFICATION
programme: HealthIQ AI v5
scope: Cross-Domain Clinical Prioritisation
supersedes:
  - Cross-Domain Clinical Prioritisation product-ratification draft 1
  - Cross-Domain Clinical Prioritisation product-ratification draft 2
related_authority:
  - HEALTHIQ_CLINICAL_FINDING_PRIORITISATION_CONTRACT_v0_6_3.md
  - HEALTHIQ_CROSS_DOMAIN_CLINICAL_PRIORITISATION_RULESET_v0_5.md
  - HEALTHIQ_CROSS_DOMAIN_HMR_ADJUDICATION_REGISTER_v0_4.md
  - HEALTHIQ_SIX_DOMAIN_CLINICAL_CLOSURE_REPORT_v0_4.md
  - CLIN-PRIORITY-ARCH-HARDEN-1_cross_domain_prioritisation_architecture_hardening.md
implementation_authorised: false
cursor_prompt_authorised: false
tier_0_activation_authorised: false
questionnaire_context_reliance_authorised: false
release_authorised: false
---

# HealthIQ AI — Cross-Domain Clinical Prioritisation
## Product Ratification — Clinician-First Model

## 1. Status and authority

This document records Anthony’s formal product ratification of the clinician-first product model for Cross-Domain Clinical Prioritisation.

**Ratification status:** `PRODUCT_RATIFIED`

**Ratifier:** Anthony  
**Ratification date:** 3 August 2026  
**Ratification statement used:** “I ratify Draft 3.”

This document records product authority only.

It does not:

- create, amend or replace clinical prioritisation rules;
- change medical thresholds;
- close regulatory or legal dependencies;
- authorise Tier 0 activation;
- authorise runtime reliance on incomplete questionnaire context;
- authorise a Cursor implementation prompt;
- authorise implementation execution;
- authorise release.

## 2. Clinical-authority boundary

Clinical priority is determined by the ratified domain and cross-domain clinical rulesets.

Those rulesets establish:

- the clinically meaningful finding or pattern;
- domain-specific severity;
- urgency and time-to-action;
- interpretability requirements;
- consolidation rules;
- combination rules;
- modifiers;
- overrides;
- insufficient-data states;
- indeterminate-severity states;
- the resulting Tier 0–3 concern classification.

This product ratification governs only:

- selection of the lead concern or clinically justified co-leads;
- prominence and ordering of the visible concern set;
- presentation of supporting and contextual information;
- communication of uncertainty and limitations;
- user-facing product behaviour.

The product layer must not:

- recalculate clinical severity;
- reinterpret urgency;
- change a clinically assigned tier;
- downgrade or suppress a finding for presentation convenience;
- create a competing clinical-prioritisation authority;
- substitute interface logic for the governed clinical rulesets.

## 3. Governing clinician-first premise

Where a product or presentation decision remains open, the governing test is:

> **What would a competent clinician reasonably identify as the principal clinical concern, what action would they take next, and what information would they treat as supporting or contextual rather than as a competing concern?**

The product must represent the outcome of that clinical reasoning.

It must not prioritise according to:

- interface neatness;
- technical confidence alone;
- number of supporting markers;
- number of active signal frames;
- panel completeness;
- amount of available narrative;
- editorial prominence;
- frontend grouping;
- ease of implementation.

## 4. Clinician-style decision sequence

HealthIQ should present the result of the following clinically governed sequence:

1. Establish whether the available results are interpretable.
2. Identify findings requiring immediate or time-sensitive attention.
3. Construct clinically meaningful findings from the available markers, signals and context.
4. Consolidate related abnormalities before prioritisation.
5. Apply domain-specific severity and urgency rules.
6. Apply cross-domain combinations, modifiers and overrides.
7. Assign the clinically governed concern tier.
8. Determine which finding a clinician would focus on first.
9. Identify any genuinely co-equal concerns.
10. Keep clinically important secondary concerns visible.
11. Attach supporting and contextual information to the concern it explains.
12. Communicate uncertainty, missing information and limitations explicitly.

## 5. Principal clinical concern

HealthIQ should present one principal clinical concern where the governed clinical findings show that one issue clearly matters most.

The principal concern should represent:

> **The issue a competent clinician would reasonably focus on first.**

Selection must be based on the clinically governed outputs, including:

- concern tier;
- urgency;
- severity;
- actionability;
- trend;
- risk of delay;
- clinically relevant combinations and overrides;
- the role of the finding in organising the wider clinical picture.

The product must not independently recalculate these factors.

## 6. Co-equal clinical concerns

More than one lead concern should be presented only where the clinically governed findings are genuinely co-equal.

Co-equality may exist where:

- two independent findings require the same urgent response;
- two findings have materially equivalent clinical importance, urgency and actionability;
- a recognised combined pattern would be misrepresented if one component were subordinated;
- the governing rules specify that findings should be presented together.

Co-lead status must not be used merely to avoid making a difficult prioritisation decision.

Below the same-day band, the default maximum is two co-leads.

Additional clinically important findings remain visible in their assigned tier.

For clinically co-equal same-day findings:

- all qualifying findings remain visible;
- they are presented as one same-day concern group;
- no artificial internal ranking is imposed;
- no finding is hidden to maintain a visual cap.

## 7. Consolidation before presentation

The user-facing concern set must be based on consolidated clinical findings, not on raw system outputs.

A single clinical finding may be supported by:

- multiple biomarkers;
- multiple activation frames;
- multiple hypotheses;
- more than one clinical domain;
- trends;
- questionnaire context;
- supporting or contradictory evidence.

These inputs must not automatically become separate concerns.

The governing separation test is:

> **Would a clinician reasonably take a materially different next action depending on which finding or frame is correct?**

If not, the information should normally be consolidated.

If yes, it may remain as a separate finding.

The product must avoid:

- one concern per biomarker;
- one concern per signal;
- one concern per frame;
- duplicate concerns caused by cross-domain overlap;
- separate headline prominence for supporting markers that do not change clinical action.

## 8. Clinical roles within the concern set

Each item should have one primary clinical role.

### Principal concern

The issue the clinician would focus on first.

### Co-lead concern

A separate concern that is genuinely clinically co-equal with the principal concern.

### Independent secondary concern

A clinically meaningful issue requiring its own monitoring, investigation, discussion or action, but not the first priority.

### Supporting evidence

A marker, trend or related result that strengthens or explains a finding without creating a separate management issue.

### Modifier

Information that changes the interpretation, urgency, severity or action associated with another finding.

### Contextual information

Relevant information that helps explain the clinical picture but would not independently drive action.

### Insufficient-data state

The required information is absent and a clinically valid finding cannot be created.

### Indeterminate-severity state

The finding is valid, but the available information is insufficient to determine its full severity or urgency.

A fact may serve more than one role, but it must not appear as duplicate competing concerns. Any secondary role should be visibly linked to the primary finding.

## 9. Priority tiers

Priority tiers are assigned by the clinically governed domain and cross-domain rulesets.

They reflect the urgency, severity and likely next action that a competent clinician would reasonably recognise.

### Tier 0 — Immediate or same-day clinical attention

A finding requiring, or potentially requiring, urgent assessment, same-day escalation or another defined safety pathway.

Until the operational, clinical, regulatory and legal pathway is approved:

- Tier 0 rules remain specification-only;
- Tier 0 remains unreachable for release;
- withheld Tier 0 evaluation remains auditable;
- Tier 0 must never be silently downgraded to Tier 1 or Tier 2.

### Tier 1 — Clinically important follow-up

A clinically significant finding that reasonably warrants investigation, clinical discussion or active follow-up.

Tier 1 must reflect genuine clinical importance, not abnormality alone.

### Tier 2 — Monitoring or planned reassessment

A clinically relevant finding that would usually be monitored, repeated or reviewed over a longer timeframe.

### Tier 3 — Supporting or contextual information

Information that contributes to interpretation but would not ordinarily be treated as an independent management priority.

Tier 3 information should normally be attached to, or displayed beneath, the concern it supports.

The product may refine the consumer-facing wording of these tiers only with appropriate clinical, product and regulatory approval. It must not change their clinical meaning.

## 10. Visibility and prominence

HealthIQ must not hide clinically meaningful findings merely to simplify the interface.

The product should display:

- the principal concern;
- any genuine co-lead;
- all clinically distinct Tier 0, Tier 1 and Tier 2 findings;
- relevant Tier 3 context attached to its parent concern;
- insufficient-data states;
- indeterminate-severity states;
- withheld or quarantined states where required.

The product may control visual prominence, but it must not:

- suppress an independent concern because another finding ranks higher;
- downgrade a concern to reduce visible volume;
- hide findings because the display becomes crowded;
- allow a phenotype or system-level output to displace a more important direct clinical finding;
- promote a contextual output above the direct finding it explains.

## 11. Action and timeframe

Each concern should communicate the clinically governed type and timeframe of action.

Possible action classes may include:

- immediate assessment;
- same-day clinical contact;
- prompt clinical review;
- further investigation;
- repeat testing;
- medication or treatment review by an appropriate clinician;
- monitoring;
- planned reassessment;
- specialist interpretation required;
- insufficient information to advise safely.

The product must not invent urgency or action wording independently.

User-facing wording must remain within the approved intended purpose and must not become an unauthorised medical instruction.

## 12. Missing information and uncertainty

Clinically material uncertainty must remain visible.

Where information is missing:

- use **insufficient data** where a finding cannot validly be constructed;
- use **indeterminate severity** where a finding exists but its full severity or urgency cannot be resolved;
- state any interim assumption used to permit interpretation;
- preserve the provenance of missing, unanswered or defaulted information.

Missing information must not:

- silently remove a concern;
- cause an automatic downgrade;
- be represented as normal;
- be replaced by an undocumented default.

Pregnancy- and sex-dependent behaviour must not be treated as operationally complete until the questionnaire and server-side enforcement gaps are resolved.

## 13. No-concern outcome

Where the governed analysis identifies no clinically meaningful concern, HealthIQ should present one clear overall conclusion.

Accessible limitations should explain that:

- the analysis is bounded by the biomarkers and clinical context available;
- absence of a detected concern does not exclude all disease;
- some conditions require symptoms, examination, imaging or other investigations;
- missing data may limit interpretation.

The main conclusion should remain concise.

Limitations must remain visible and accessible but should not be repeated as multiple competing warnings.

## 14. Diagnostic and disease-name language

At initial release, HealthIQ should not present a consumer-facing disease diagnosis unless this is separately authorised through clinical and regulatory governance.

Preferred wording includes:

- finding;
- biochemical pattern;
- clinical concern;
- possible explanation;
- warrants investigation;
- consistent with;
- may be associated with.

Disease names may remain in:

- internal provenance;
- clinical source material;
- rule identifiers;
- approved clinician-facing material.

The product must not imply diagnostic certainty where the governed evidence supports only a finding, pattern or differential consideration.

## 15. Domain and release sequencing

Domains may proceed independently where their clinical, architecture and governance dependencies are satisfied.

However:

- Tier 0 findings must not be demoted to enable release;
- Tier 0 rules must not be silently removed;
- quarantined capabilities must remain visibly classified and auditable;
- capability-specific regulatory blockers must remain effective;
- unresolved questionnaire dependencies block release or runtime reliance on the affected context;
- engineering convenience must not determine clinical release sequencing.

## 16. Governance authority

### Head of Medical Research

Owns:

- clinical meaning;
- clinical thresholds;
- severity;
- urgency;
- clinical combinations;
- modifiers;
- overrides;
- evidence interpretation;
- medical safety.

### Anthony

Owns:

- product ratification;
- user-facing prominence and visibility;
- presentation of the lead and concern set;
- product release sequencing;
- final human approval.

### Regulatory and legal workstream

Owns:

- intended-purpose constraints;
- diagnostic and disease-name language;
- population exclusions;
- Tier 0 operational and escalation requirements;
- regulatory release restrictions.

### Architecture

Owns:

- canonical models;
- system boundaries;
- identity and provenance;
- deterministic compilation;
- fail-closed behaviour;
- runtime ownership;
- frontend non-authority.

### Engineering

Implements ratified decisions.

Engineering must not reinterpret:

- clinical rules;
- product decisions;
- regulatory constraints;
- release authority.

## 17. Auditability and change control

Every prioritisation and presentation decision must be reproducible and traceable.

The system must retain:

- clinical rule identity;
- source specification identity;
- signal identity;
- activation identity;
- contract version;
- ruleset version;
- adjudication identity where applicable;
- compile identity and hashes;
- contributing findings and markers;
- applied combinations and overrides;
- missing-data state;
- assigned tier;
- lead or co-lead decision;
- supporting or contextual relationships;
- withheld or quarantined status;
- product-presentation policy version.

No threshold, tiering rule, lead-selection rule or presentation policy may change silently.

Material changes require:

- explicit authority;
- versioning;
- validation;
- regression testing;
- governed promotion.

## 18. Ratified product decisions

Anthony ratifies the following product principles:

1. Clinical findings, severity, urgency, consolidation, overrides and tiers are determined by the governed clinical rulesets, not by the product layer.
2. The governing product test is what a competent clinician would reasonably prioritise and do next.
3. HealthIQ presents one principal concern unless findings are genuinely clinically co-equal.
4. Co-lead status is determined by clinical co-equality, not display preference.
5. Clinically distinct important findings remain visible even when they are not the lead.
6. Related biomarkers, signals, frames and contextual outputs are consolidated before presentation.
7. Supporting evidence and modifiers do not become competing concerns unless they independently change clinical action.
8. Product prominence and ordering must remain faithful to the clinically governed tier and time-to-action.
9. Missing data and uncertainty remain visible and must not silently suppress or downgrade findings.
10. Tier 0 content remains specification-only and fail-closed until its operational pathway is authorised.
11. Consumer-facing disease diagnoses remain quarantined unless separately approved.
12. No-concern results use one concise conclusion with accessible limitations.
13. Product presentation must not recalculate, reinterpret, downgrade or override a clinically governed finding or tier.
14. All prioritisation and presentation decisions must be deterministic, versioned and auditable.
15. Engineering has no authority to reinterpret clinical, product, regulatory or release decisions.

## 19. Formal ratification statement

> I ratify this clinician-first product model as the governing product interpretation of the Cross-Domain Clinical Prioritisation Contract.
>
> I confirm that the clinically governed domain and cross-domain rulesets determine the findings, severity, urgency, consolidation, overrides and resulting concern tiers.
>
> The product layer must faithfully present those governed outputs according to what a competent clinician would reasonably identify as the principal concern, what action they would take next, and what information they would treat as supporting or contextual.
>
> This ratification does not amend clinical rules, close regulatory or legal dependencies, authorise Tier 0 activation, authorise reliance on incomplete questionnaire context, authorise a Cursor implementation prompt, or authorise release.

## 20. Ratification record

```yaml
ratified_by: Anthony
ratification_date: 2026-08-03
ratification_statement: "I ratify Draft 3."
ratification_status: PRODUCT_RATIFIED
architecture_effect: SATISFIES_PRODUCT_RATIFICATION_RECORD_ONLY
cursor_prompt_effect: NO_AUTHORISATION
implementation_effect: NO_AUTHORISATION
tier_0_effect: NO_ACTIVATION
questionnaire_context_effect: NO_RUNTIME_RELIANCE_AUTHORISATION
release_effect: NO_RELEASE_AUTHORISATION
```

## 21. Required downstream references

The following governing records should cite this artefact:

1. `HEALTHIQ_CROSS_DOMAIN_HMR_ADJUDICATION_REGISTER_v0_4.md`
   - Mark the applicable product items as product-ratified.
   - Preserve regulatory and legal items as open.

2. `HEALTHIQ_SIX_DOMAIN_CLINICAL_CLOSURE_REPORT_v0_4.md`
   - Record the product-ratification artefact as subsequent authority.
   - Do not alter the clinical closure status.

3. `CLIN-PRIORITY-ARCH-HARDEN-1_cross_domain_prioritisation_architecture_hardening.md`
   - Update contract §23.6 condition 3 to `SATISFIED`.
   - Cite this document as the authority record.
   - Preserve the Cursor authoring gate as prohibited until the remaining conditions close.

4. `docs/sprints/launch_core_carry_forward_register.md`
   - Record product ratification as complete.
   - Carry forward regulatory, Tier 0, acceptance-scenario and questionnaire dependencies.

---

**Document status:** `PRODUCT_RATIFIED`  
**Version:** `1.0`  
**Ratifier:** Anthony  
**Ratified:** 3 August 2026
