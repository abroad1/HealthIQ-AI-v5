---
document_id: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001
title: HealthIQ Clinical Finding Prioritisation Contract
version: "0.2"
status: DRAFT_FOR_CONFIRMATORY_INDEPENDENT_MEDICAL_VALIDATION
owner: HealthIQ Head of Medical Research
product_authority: Anthony
scope: Clinical prioritisation, concern-set construction, lead selection, and presentation authority
implementation_status: NOT_AUTHORISED
regulatory_status: OPEN_SPECIALIST_REVIEW_REQUIRED
supersedes: "0.1"
---

# HealthIQ Clinical Finding Prioritisation Contract v0.2

## 1. Purpose

This contract defines the clinical policy HealthIQ must use to transform blood-panel data into a clinically prioritised concern set.

It replaces the concept of ranking raw markers or signal frames by a single universal score.

The contract governs:

- the unit that may be prioritised;
- the clinical dimensions that must remain separate;
- how urgency, severity and tiers are assigned;
- how supporting markers may affect interpretation;
- how multiple frames are consolidated;
- how findings enter the concern set;
- how one orienting lead is surfaced;
- how contextual findings are prevented from displacing direct concerns;
- how confidence affects explanation without controlling prominence;
- how phenotype and IDL outputs relate to direct findings;
- how no-concern outputs avoid false reassurance;
- how urgent findings require an operational escalation pathway;
- what remains subject to domain-specific, regulatory and product ratification.

This document is a clinical-policy draft. It does not authorise implementation or release.

## 2. Governing principle

HealthIQ must prioritise the clinical problem that matters most, not the marker with the greatest amount of supporting information.

The system must distinguish:

1. clinical consequence;
2. urgency;
3. severity;
4. actionability;
5. interpretive confidence;
6. analytical reliability;
7. persistence and trend;
8. whether a finding is direct, combination-derived, explanatory, contextual, phenotype-level or system-level.

These dimensions must not be collapsed into one undifferentiated ranking score.

## 3. Unit of prioritisation

### 3.1 Canonical unit

The canonical unit of prioritisation is a:

> **consolidated clinical finding or pattern**

It is not:

- a raw biomarker;
- a signal row;
- an investigation frame;
- a WHY hypothesis;
- a phenotype label;
- an IDL record;
- a narrative section.

A consolidated clinical finding may arise from:

- one abnormal marker;
- one in-range marker that is clinically abnormal in context;
- several markers forming a recognised pattern;
- a clinically meaningful combination;
- a change over time;
- one marker with several alternative interpretations;
- a direct abnormality plus explanatory context.

Reference-range exceedance is neither necessary nor sufficient for finding creation. Governed rules may create findings from in-range values where a recognised combination, demographic rule or trend criterion is met.

### 3.2 Examples

- ALT and ALP may form a hepatocellular, cholestatic or mixed liver-pattern finding.
- Ferritin and transferrin saturation may form an iron-overload or inflammatory-ferritin finding.
- Macrocytosis with anaemia or another cytopenia is different from isolated mild macrocytosis.
- Creatinine may form an acute-change finding only when a valid prior result exists.
- A platelet count within range may still generate a trend finding if it has fallen materially from baseline.
- Multiple MCV interpretation frames normally consolidate into one macrocytosis concern.

## 4. Mandatory clinical dimensions

Every consolidated finding must carry the following dimensions as separate properties.

### 4.1 Urgency

The time sensitivity of required action.

Urgency answers:

> How soon might this need clinical attention?

Urgency must be assigned through explicit, clinically governed rules.

### 4.2 Severity

The degree of abnormality or dysfunction using the metric appropriate to the finding.

Severity may depend on:

- multiples of ULN;
- absolute concentration;
- absolute cell count;
- percentage or absolute change from baseline;
- recognised disease-stage bands;
- synthetic-function impairment;
- combination patterns;
- direction-specific rules.

No universal severity formula is authorised.

### 4.3 Clinical significance

Clinical significance means:

> Given that this finding is present as characterised, how consequential is this class of finding?

Clinical significance is a property of the finding itself, not of HealthIQ’s certainty in explaining it.

Absence, unavailability or ambiguity of supporting data must not reduce clinical significance. Such factors act only on interpretive confidence.

### 4.4 Actionability

Whether a useful action follows, such as:

- prompt review;
- further investigation;
- repeat or confirmation;
- medication review;
- exposure modification;
- monitoring;
- reassurance.

### 4.5 Interpretive confidence

How certain HealthIQ is about the explanation of the finding.

Interpretive confidence may be affected by:

- missing markers;
- contradictory markers;
- unresolved alternative causes;
- incomplete context;
- absent history;
- weak pattern specificity.

Interpretive confidence must affect explanation specificity and uncertainty wording.

It must not determine clinical prominence, tier or lead selection.

### 4.6 Analytical reliability

Whether the measured result may be affected by:

- haemolysis;
- platelet clumping;
- delayed processing;
- assay limitation;
- inappropriate reference range;
- sample contamination;
- other recognised pre-analytical or analytical artefact.

Analytical reliability is an annotation. It must not be used to reduce urgency or suppress a finding.

### 4.7 Persistence and trend

Whether the finding is:

- new;
- persistent;
- improving;
- worsening;
- recurrent;
- stable;
- impossible to assess because no valid prior result exists.

### 4.8 Contextual role

Whether the finding is:

- direct;
- combination-derived;
- explanatory;
- contextual;
- phenotype-level;
- system-level.

A finding that independently meets Tier 0 or Tier 1 criteria may not be assigned contextual role.

Contextual role is available only to findings that would otherwise sit in Tier 2 or Tier 3.

## 5. Clinical processing order

HealthIQ must apply the following sequence:

```text
raw markers and valid prior results
→ signal/frame evaluation
→ clinical finding consolidation
→ urgency classification
→ domain-specific severity classification
→ recognised combination and override rules
→ clinical-significance and actionability assessment
→ concern-tier assignment
→ interpretive-confidence assessment
→ analytical-reliability annotation
→ lead selection
→ phenotype/IDL coordination
→ presentation
```

The sequence is mandatory because:

- consolidation must happen before ranking;
- urgency must not depend on confidence or reliability;
- severity must not depend on supporting-marker count;
- reliability modifies framing and confirmation advice, not priority;
- presentation must not reorder clinical priority.

## 6. Concern-tier assignment

HealthIQ will use one orienting lead over a clinically tiered concern set.

### 6.1 Tier-assignment algebra

Each finding receives:

- an urgency-derived tier;
- a severity-derived tier.

The initial tier is the higher-priority of those two tiers.

Clinical significance and actionability may promote a finding by at most one tier where an explicit governed rule permits it.

Clinical significance and actionability may not lower a finding below the floor set by urgency or severity.

Interpretive confidence, supporting-marker count, frame count, panel completeness and analytical reliability may not alter the assigned tier.

### 6.2 Tier 0 — Prompt clinical review

Reserved for findings meeting explicit, clinically ratified urgency criteria.

Tier 0 membership is determined solely by ratified clinical rules. Its observed firing rate is an empirical safety metric, not a design target.

A Tier 0 finding must:

- be foregrounded;
- control the lead or co-lead set;
- use action-and-timeframe language;
- avoid unsupported diagnostic claims;
- include confirmation advice where artefact is plausible;
- follow a defined operational escalation pathway.

### 6.3 Tier 1 — Discuss or investigate

Findings that warrant active clinical review or further investigation but do not meet Tier 0 criteria.

### 6.4 Tier 2 — Monitor or recheck

Findings that are real and potentially useful but usually lower consequence.

### 6.5 Tier 3 — Contextual

Findings whose main value is to explain, refine or contextualise another concern.

Tier 3 findings:

- may not lead;
- may not compete independently with Tier 0–2 findings;
- should attach to the finding they help explain;
- must remain reconcilable with the raw result.

If a Tier 3 finding has no valid parent, it must not disappear. It must either:

- be presented in a distinct low-prominence contextual group; or
- be promoted to Tier 2 where it independently warrants monitoring or recheck.

## 7. Lead-selection policy

### 7.1 Core rule

The lead is selected from the highest non-empty concern tier.

### 7.2 Within-tier ordering

Within the highest non-empty tier, findings are ordered by:

1. urgency;
2. severity;
3. clinical significance;
4. actionability;
5. persistence or worsening trend;
6. directness of evidence;
7. deterministic tie-breaker only when clinically equivalent.

### 7.3 Excluded inputs

The following must not determine lead selection:

- interpretive confidence;
- supporting-marker count;
- number of frames;
- panel completeness;
- analytical-reliability status;
- lexical signal identifiers;
- static IDL display priority;
- narrative prominence;
- editorial preference.

### 7.4 Co-leads

Co-leads may be used only when:

- two or more distinct Tier 0 or Tier 1 findings are clinically comparable;
- they represent materially different action pathways;
- forcing one winner would be arbitrary or misleading.

Anthony must ratify a maximum co-lead count.

The recommended maximum is two.

If more findings qualify than the cap permits, one lead or bounded co-lead set is shown and the remaining findings remain visible within their tier.

## 8. Supporting-marker policy

Supporting markers must not be counted as votes.

Their mere number must have no effect on priority.

Supporting markers may affect a finding only when they:

- establish a recognised pattern;
- trigger a clinically governed combination rule;
- identify organ dysfunction;
- materially increase or reduce the consequence of the characterised finding;
- reveal an artefact;
- resolve a clinically meaningful ambiguity;
- alter the recommended action.

Missing supporting markers may lower interpretive confidence.

They must not lower severity, clinical significance, tier or lead eligibility merely because they are absent.

## 9. Frame-consolidation policy

### 9.1 Default rule

One analyte contributes one concern slot by default.

Multiple frames over the same primary analyte must consolidate before concern-tier assignment and lead selection.

### 9.2 Consolidated content

A consolidated finding may contain:

- the leading interpretation;
- alternative interpretations;
- missing discriminating tests;
- contradictions;
- contextual markers;
- recommended next steps.

### 9.3 Separation exception

Frames may remain separate only when they imply materially different clinical action pathways.

The governing test is:

> Would a clinician reasonably take materially different next actions depending on which frame is correct?

### 9.4 Severity inheritance

A consolidated finding inherits the highest clinically justified urgency and severity among its constituent frames.

Frame count must not increase prominence.

## 10. Confidence policy

Interpretive confidence answers:

> How certain are we about what this finding means?

Clinical priority answers:

> How much does this finding matter if present as characterised?

The two must remain independent.

Confidence may control:

- strength of wording;
- presentation of alternatives;
- missing-test recommendations;
- whether interpretation is provisional;
- level of explanatory specificity.

Confidence may not control:

- whether the finding is shown;
- whether it enters Tier 0 or Tier 1;
- whether it becomes the lead;
- whether it receives urgent action language.

## 11. Analytical-reliability policy

Where a result may be artefactual:

- the finding remains visible;
- urgency remains based on potential consequence;
- confirmation advice is explicit;
- the system must not assert that the abnormality is genuine;
- the system must not silently demote the finding.

Analytical reliability must be represented as a separate annotation consumed by wording, confirmation and action guidance.

It must not be an input to urgency, severity or tier assignment.

## 12. Trend policy

HealthIQ must distinguish:

### 12.1 Change-defined findings

For some clinical rules, change over time is the finding.

Where a governed rule is change-defined:

- trend evaluation is mandatory;
- baseline-validity requirements must be defined by the domain rule;
- the age and comparability of the prior result must be checked;
- if no valid baseline exists, HealthIQ must state that the change-defined criterion could not be assessed.

### 12.2 Change-modified findings

For other findings, trend modifies the interpretation of an already-present single-timepoint abnormality.

Trend may then increase or decrease concern according to an explicit governed rule.

Absent baseline data must never be treated as evidence of stability.

## 13. Override policy

Overrides may move findings across tiers only when individually governed.

Every override must be:

- explicitly enumerated;
- attributable to a named clinical rule;
- supported by a cited source or documented clinical adjudication;
- versioned;
- auditable;
- directionally constrained.

No override may downgrade a finding below the floor set by urgency or severity.

An override without a citable clinical basis or documented clinical adjudication is editorial preference and is prohibited.

## 14. Phenotype and IDL policy

Phenotype and IDL records are interpretive layers over direct findings.

They must not operate as an independent cross-severity ranking system.

Rules:

- direct findings and phenotypes must map to the same concern-tier framework;
- static display priority may operate only as a tie-breaker within the same tier and comparable severity;
- phenotype severity must derive from constituent findings;
- a broad phenotype may not outrank a more severe direct abnormality;
- system summaries are contextual by construction;
- where a phenotype explains the lead, it should be presented as context around the lead rather than as a competing concern.

## 15. Presentation policy

The interface must preserve the clinical concern structure.

### 15.1 Default presentation

- Highest-tier lead or bounded co-leads.
- Other Tier 0 findings visible without interaction.
- Tier 1 findings visible, subject to a ratified presentation-density rule.
- Tier 2 findings visible but visually de-emphasised.
- Tier 3 findings nested beneath their parent or placed in a distinct contextual group.
- Missing-data and analytical limitations shown explicitly.

### 15.2 Tier 1 volume control

Anthony must ratify:

- the number of Tier 1 findings shown fully expanded;
- the compact grouping behaviour above that number;
- the maximum presentation density.

Compression may alter presentation density only.

It may not:

- reorder findings;
- remove findings;
- lower tiers;
- conceal that additional Tier 1 findings exist.

### 15.3 Language

Language must:

- distinguish urgency from diagnosis;
- state action and timeframe where needed;
- communicate uncertainty;
- avoid false reassurance;
- avoid unnecessary alarm;
- explain why a finding is prominent;
- avoid implying completeness where the panel was incomplete.

## 16. No-concern and all-normal output policy

HealthIQ must define a governed output for panels containing:

- no Tier 0 or Tier 1 findings;
- only Tier 2 findings;
- only Tier 3 findings;
- no out-of-range values;
- incomplete data that prevents meaningful assessment.

The output must not state or imply:

- that no disease is present;
- that the user is medically well;
- that symptoms are explained or excluded;
- that conditions not tested by the panel have been ruled out.

The output must state, in appropriate user-facing language:

1. what was and was not identified from the supplied results;
2. that normal or low-concern results do not exclude conditions the panel did not test for;
3. that missing markers or missing history may limit assessment;
4. that ongoing, severe or concerning symptoms warrant clinical review irrespective of the result summary;
5. what, if anything, is worth monitoring or discussing routinely.

The no-concern language requires the same clinical governance and versioning as Tier 0 language.

## 17. Tier 0 operational pathway

Tier 0 is not merely a wording class.

Before Tier 0 can be implemented, HealthIQ must define and ratify:

- the exact action the user is instructed to take;
- the required timeframe;
- confirmation advice for common artefact-prone results;
- whether acknowledgement is requested or recorded;
- whether any follow-up mechanism exists;
- whether any circumstance permits contact with another party;
- what is recorded for audit;
- what happens if later information shows the result was artefactual;
- legal, duty-of-care and support implications.

The Tier 0 pathway requires joint clinical, product, regulatory and legal review.

No Tier 0 production release is authorised without this pathway.

## 18. Prohibited behaviours

The following are prohibited:

1. Ranking by supporting-marker count.
2. Using interpretive confidence as a prominence multiplier.
3. Allowing missing supporting data to reduce clinical significance.
4. Applying multiples of ULN universally across domains.
5. Allowing lexical ordering before clinical differentiators are exhausted.
6. Allowing static IDL priority to select the lead across severity levels.
7. Allowing multiple frames of one analyte to occupy multiple concern slots by default.
8. Suppressing a finding because confidence is low.
9. Treating absent baseline data as evidence of stability.
10. Treating panel completeness as clinical importance.
11. Letting presentation logic reorder clinically prioritised findings.
12. Treating tier thresholds as ordinary product configuration.
13. Using unsupported diagnostic language.
14. Presenting no foreground concern as proof that no clinically important issue exists.
15. Escalating common artefact-prone results without confirmation guidance.
16. Allowing contextual or system-level findings to outrank direct higher-severity abnormalities.
17. Assigning contextual status to a finding that independently meets Tier 0 or Tier 1.
18. Using an ungoverned or unsourced override.
19. Allowing an override to lower a finding below its urgency or severity floor.
20. Silently dropping an orphan Tier 3 finding.
21. Treating an in-range value as incapable of forming a clinical finding.
22. Presenting a change-defined condition as assessed when no valid baseline exists.

## 19. Initial hepatic regression fixture

The following case is a regression fixture.

It is not the source from which hepatic thresholds may be reverse-engineered.

### 19.1 Inputs

- ALT: 250 U/L
- ALT ULN: 49 U/L
- ALP: 46 U/L
- ALP ULN: 116 U/L
- R-value: approximately 12.9
- Bilirubin: normal
- GGT: normal
- AST: absent
- MCV: 99.5 fL
- MCV ULN: 96 fL
- Transferrin: mildly low

### 19.2 Required non-regression behaviour

- Consolidated lead finding: marked hepatocellular enzyme elevation.
- Expected concern tier: Tier 1 — discuss/investigate, subject to independent hepatic rule derivation and adjudication.
- Interpretive confidence: reduced for precise aetiological characterisation because AST is absent.
- Clinical significance and priority: not reduced merely because AST is absent.
- MCV: does not occupy multiple concern slots.
- Mild macrocytosis: contextual unless other blood-count abnormalities create a separate clinically meaningful pattern.
- Mildly low transferrin: contextual unless an independent iron, protein or liver pattern justifies separate concern status.
- IDL phenotype: may contextualise but may not displace the direct hepatic finding.
- No urgent diagnostic claim is authorised from these results alone.

### 19.3 Evidence discipline

The hepatic pilot must derive thresholds independently from cited evidence.

After derivation, the rules must be tested against this fixture.

If independently derived rules do not produce the expected Tier 1 result, the discrepancy requires clinical adjudication. Thresholds must not be adjusted merely to force the expected answer.

## 20. Domain-research requirements

This contract does not define numerical thresholds.

The following governed domain work is required before production implementation:

1. Hepatic severity, urgency, R-value and synthetic-function rules.
2. Electrolyte absolute thresholds and artefact rules.
3. Renal change-defined and single-timepoint rules.
4. Haematology and cytopenia severity rules.
5. Iron, ferritin, transferrin saturation and inflammatory-context rules.
6. Endocrine direction-specific rules.
7. Cardiometabolic and lipid risk-trigger rules.
8. Inflammatory-marker significance rules.
9. Nutritional-marker severity and actionability rules.
10. Cross-domain tier mapping.
11. Phenotype severity derivation.
12. Demographic and contextual modifiers.
13. Baseline-validity rules by domain.
14. Trend and persistence policy.
15. Tier 0 and no-concern language templates.
16. Clinical review and versioning cadence.
17. Tier 0 operational escalation pathway.

## 21. Pilot sequence

### 21.1 First pilot — hepatic

The hepatic pilot remains first because:

- it contains the observed UAT failure;
- the architecture already computes R-value;
- it supports pattern classification;
- it demonstrates confidence-versus-priority separation;
- it provides a direct test of contextual MCV and transferrin handling.

The hepatic pilot must define:

- ALT and AST severity bands;
- R-value classification;
- bilirubin, albumin, INR and platelet modifiers;
- urgent and non-urgent escalation conditions;
- missing-AST handling;
- analytical and clinical caveats;
- action-tier mapping;
- contextual-marker attachment;
- acceptance scenarios.

### 21.2 Second pilot — electrolytes

Electrolytes should be the second pilot because they stress-test the prohibition on universal ULN-based severity scoring and require explicit artefact and urgency handling.

## 22. Regulatory status and intended purpose

The regulatory status of this functionality is an open question requiring specialist advice in each intended launch market.

This contract assigns:

- patient-specific clinical concern tiers;
- urgency classes;
- action-and-timeframe guidance;
- prioritised interpretation of laboratory data.

Ratification of this clinical contract does not determine that HealthIQ falls outside medical-device or software-as-a-medical-device regulation.

Non-diagnostic or informational disclaimers do not by themselves settle regulatory status. The actual intended purpose, claims, outputs and user journey must be assessed together.

Before release, HealthIQ must:

1. obtain specialist regulatory advice;
2. document the intended-purpose statement;
3. reconcile that statement with the outputs authorised by this contract;
4. determine applicable clinical-evaluation, validation, quality, post-market and change-control obligations;
5. confirm whether Tier 0 functionality is permissible within the chosen product and regulatory model.

Regulatory review may constrain:

- tier naming;
- urgency wording;
- action recommendations;
- supported users;
- market scope;
- release sequence.

## 23. Governance and authority

### 23.1 Clinical authorship

The HealthIQ Head of Medical Research owns this policy and the clinical threshold assets derived from it.

Any individual providing clinical ratification must have appropriate qualifications, competence and scope for the decisions being ratified.

### 23.2 Independent medical validation

An independent medical reviewer must:

- challenge the clinical assumptions;
- verify evidence use;
- identify unsafe generalisation;
- test challenge cases;
- review false-reassurance and over-escalation risks.

### 23.3 Product ratification

Anthony must ratify:

- the lead-plus-tiered-concern-set product model;
- maximum co-lead count;
- tier visibility;
- Tier 1 volume-control behaviour;
- user-facing tier names;
- missing-data transparency;
- no-concern presentation;
- governance authority;
- threshold versioning and auditability.

### 23.4 Regulatory validation

A qualified regulatory adviser must assess intended purpose, market classification and release obligations.

### 23.5 Architecture hardening

Claude Code must validate:

- repository compatibility;
- contract impact;
- data-flow boundaries;
- consolidation location;
- versioning requirements;
- IDL and frontend dependencies;
- migration and regression risk.

Claude Code does not validate clinical truth or regulatory classification.

### 23.6 Implementation authority

No Cursor implementation prompt may be issued until:

1. independent medical validation is complete;
2. Head of Medical Research reconciliation is complete;
3. Anthony has ratified the product decisions;
4. the regulatory workstream has established any constraints material to design;
5. architecture hardening is complete;
6. the hepatic pilot has a clinically governed specification;
7. acceptance scenarios are approved;
8. the Tier 0 operational pathway is defined if Tier 0 is in implementation scope.

## 24. Monitoring and review

HealthIQ must monitor:

- Tier 0 firing rate;
- Tier 1 volume;
- no-concern output frequency;
- override firing;
- artefact-warning frequency;
- co-lead frequency;
- clinical-review escalations;
- false-positive and false-negative safety signals.

Observed firing rates are empirical safety indicators, not targets.

Unexpected over-firing or under-firing must trigger clinical review.

Thresholds, overrides, language and concern-set rules must be versioned and reviewable.

## 25. Status and next action

Current status:

`DRAFT_FOR_CONFIRMATORY_INDEPENDENT_MEDICAL_VALIDATION`

Next actions:

1. Send v0.2 to the independent medical reviewer for a short confirmatory review.
2. Open specialist regulatory review in parallel.
3. Do not author the hepatic pilot until the tier-assignment model is confirmed.
4. Do not author implementation work until the governance conditions in §23.6 are met.

The confirmatory reviewer must conclude with one of:

- `VALIDATE`
- `VALIDATE_WITH_REQUIRED_REVISIONS`
- `REJECT_AND_REDESIGN`
