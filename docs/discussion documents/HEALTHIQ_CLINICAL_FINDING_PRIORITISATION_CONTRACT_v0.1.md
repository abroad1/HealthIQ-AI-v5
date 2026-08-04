---
document_id: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001
title: HealthIQ Clinical Finding Prioritisation Contract
version: "0.1"
status: DRAFT_FOR_INDEPENDENT_MEDICAL_VALIDATION
owner: HealthIQ Head of Medical Research
product_authority: Anthony
scope: Clinical prioritisation, concern-set construction, lead selection, and presentation authority
implementation_status: NOT_AUTHORISED
---

# HealthIQ Clinical Finding Prioritisation Contract v0.1

## 1. Purpose

This contract defines the clinical policy HealthIQ must use to transform blood-panel abnormalities into a clinically prioritised concern set.

It replaces the concept of ranking raw markers or signal frames by a single universal score.

The contract governs:

- the unit that may be prioritised;
- the clinical dimensions that must remain separate;
- how urgency and severity are assigned;
- how supporting markers may affect interpretation;
- how multiple frames are consolidated;
- how findings enter the concern set;
- how one orienting lead is surfaced;
- how contextual findings are prevented from displacing direct concerns;
- how confidence affects explanation without controlling prominence;
- how the phenotype/IDL layer must relate to direct findings;
- what remains subject to domain-specific research and ratification.

This document is a clinical-policy draft. It does not authorise implementation.

## 2. Governing principle

HealthIQ must prioritise the clinical problem that matters most, not the marker with the greatest amount of supporting information.

The system must therefore distinguish:

1. how clinically important a finding is;
2. how urgently it may require action;
3. how certain HealthIQ is about the interpretation;
4. how reliable the underlying result is;
5. what action the finding warrants;
6. whether the finding is direct, explanatory, contextual, or derivative.

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

A consolidated clinical finding may be derived from:

- one markedly abnormal marker;
- several related markers forming a recognised pattern;
- a change over time;
- a clinically meaningful combination;
- one marker with several alternative interpretations;
- a direct abnormality plus explanatory context.

### 3.2 Examples

- ALT and ALP may form a hepatocellular, cholestatic, or mixed liver-pattern finding.
- Ferritin and transferrin saturation may form an iron-overload or inflammatory-ferritin finding.
- Macrocytosis with anaemia or another cytopenia is a different finding from isolated mild macrocytosis.
- Creatinine may form an acute-change finding only when a prior result is available.
- Multiple MCV interpretation frames must normally consolidate into one macrocytosis concern.

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

The likelihood that the finding represents a clinically meaningful problem rather than an incidental or biologically minor variation.

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

It must not determine clinical prominence.

### 4.6 Analytical reliability

Whether the measured result may be affected by:

- haemolysis;
- platelet clumping;
- delayed processing;
- assay limitation;
- inappropriate reference range;
- sample contamination;
- other recognised pre-analytical or analytical artefact.

Analytical uncertainty must trigger confirmation language where appropriate.

It must not silently suppress the finding.

### 4.7 Persistence and trend

Whether the finding is:

- new;
- persistent;
- improving;
- worsening;
- recurrent;
- stable;
- impossible to assess because no prior result exists.

### 4.8 Contextual role

Whether the finding is:

- direct;
- combination-derived;
- explanatory;
- contextual;
- phenotype-level;
- system-level.

This role determines whether the finding may compete for the lead.

## 5. Clinical processing order

HealthIQ must apply the following sequence:

```text
raw markers and prior results
→ signal/frame evaluation
→ clinical finding consolidation
→ analytical reliability checks
→ urgency rules
→ domain-specific severity classification
→ recognised combination and override rules
→ clinical significance and actionability assessment
→ concern-tier assignment
→ interpretive confidence assessment
→ lead selection
→ phenotype/IDL coordination
→ presentation
```

The sequence is mandatory because:

- frame consolidation must happen before ranking;
- urgency must not depend on confidence;
- severity must not depend on supporting-marker count;
- presentation must not reorder clinical priority.

## 6. Concern-set model

HealthIQ will use one orienting lead over a clinically tiered concern set.

### 6.1 Tier 0 — Prompt clinical review

Reserved for findings meeting explicit, clinically ratified urgency criteria.

Tier 0 is normally empty.

A Tier 0 finding must:

- be foregrounded;
- control the lead;
- use action-and-timeframe language;
- avoid unsupported diagnostic claims;
- include confirmation advice where artefact is plausible.

### 6.2 Tier 1 — Discuss or investigate

Findings that warrant active clinical review or further investigation but do not meet Tier 0 urgency.

### 6.3 Tier 2 — Monitor or recheck

Findings that are real and potentially useful but usually lower consequence.

### 6.4 Tier 3 — Contextual

Findings whose main value is to explain, refine, or contextualise another concern.

Tier 3 findings:

- may not lead;
- may not compete independently with Tier 0–2 findings;
- should be attached to the finding they help explain;
- should remain visible for transparency where clinically useful.

## 7. Lead-selection policy

### 7.1 Core rule

The lead is selected from the highest non-empty concern tier.

### 7.2 Within-tier ordering

Within the highest non-empty tier, findings are ordered by:

1. urgency;
2. severity;
3. likely clinical significance;
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
- lexical signal identifiers;
- static IDL display priority;
- narrative prominence;
- editorial preference.

### 7.4 Co-leads

Co-leads may be used only when:

- two or more distinct Tier 0 or Tier 1 findings are clinically comparable;
- they represent materially different action pathways;
- forcing one winner would be arbitrary or misleading.

Co-leads must remain exceptional and bounded.

## 8. Supporting-marker policy

Supporting markers must not be counted as votes.

Their mere number must have no effect on priority.

Supporting markers may affect a finding only when they:

- establish a recognised pattern;
- trigger a clinically governed combination rule;
- identify organ dysfunction;
- materially increase or reduce the likelihood of a serious interpretation;
- reveal an artefact;
- resolve a clinically meaningful ambiguity;
- alter the recommended action.

Missing supporting markers may lower interpretive confidence.

They must not automatically lower clinical priority.

## 9. Frame-consolidation policy

### 9.1 Default rule

One analyte contributes one concern slot by default.

Multiple frames over the same primary analyte must consolidate before concern-tier assignment and lead selection.

### 9.2 Separation exception

Frames may remain separate only when they imply materially different clinical action pathways.

### 9.3 Severity inheritance

A consolidated finding inherits the highest clinically justified urgency and severity among its constituent frames.

Frame count must not increase prominence.

## 10. Confidence policy

Interpretive confidence answers:

> How certain are we about what this finding means?

Clinical priority answers:

> How much does this finding matter?

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
- urgency remains based on the potential consequence;
- confirmation advice is explicit;
- the system must not assert that the abnormality is genuine;
- the system must not silently demote the finding.

## 12. Trend policy

Trend may modify priority when sufficient prior data exists.

HealthIQ must distinguish:

- single-timepoint interpretation;
- current result versus baseline;
- acute change;
- chronic stable abnormality;
- improving or worsening trend.

Where a clinical rule requires change over time and no baseline exists, HealthIQ must state that the relevant criterion could not be assessed.

## 13. Phenotype and IDL policy

Phenotype and IDL records are interpretive layers over direct findings.

They must not operate as an independent cross-severity ranking system.

Rules:

- direct findings and phenotypes must map to the same concern-tier framework;
- static display priority may operate only as a tie-breaker within the same tier and comparable severity;
- phenotype severity must derive from constituent findings;
- a broad phenotype may not outrank a more severe direct abnormality;
- system summaries are contextual by construction;
- where a phenotype explains the lead, it should be presented as context around the lead rather than as a competing concern.

## 14. Presentation policy

The interface must preserve the clinical concern structure.

Default presentation:

- highest-tier lead or co-leads;
- other Tier 0 and Tier 1 concerns visible without interaction;
- Tier 2 concerns visible but visually de-emphasised;
- Tier 3 findings nested beneath the concern they explain;
- missing-data and analytical limitations shown explicitly.

## 15. Prohibited behaviours

The following are prohibited:

1. Ranking by supporting-marker count.
2. Using interpretive confidence as a prominence multiplier.
3. Applying multiples of ULN universally across domains.
4. Allowing lexical ordering before clinical differentiators are exhausted.
5. Allowing static IDL priority to select the lead across severity levels.
6. Allowing multiple frames of one analyte to occupy multiple concern slots by default.
7. Suppressing a finding because confidence is low.
8. Treating absent baseline data as evidence of stability.
9. Treating panel completeness as clinical importance.
10. Letting presentation logic reorder clinically prioritised findings.
11. Treating tier thresholds as ordinary product configuration.
12. Using unsupported diagnostic language.
13. Presenting no foreground concern as proof that no clinically important issue exists.
14. Escalating common artefact-prone results without confirmation guidance.
15. Allowing contextual or system-level findings to outrank direct higher-severity abnormalities.

## 16. Initial clinical acceptance case

### Inputs

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

### Required clinical interpretation

- Consolidated lead finding: marked hepatocellular enzyme elevation.
- Concern tier: Tier 1 — discuss/investigate.
- Interpretive confidence: reduced for precise aetiological characterisation because AST is absent.
- Priority: remains high despite missing AST.
- MCV: does not occupy multiple concern slots.
- Mild macrocytosis: Tier 3 contextual unless other blood-count abnormalities create a separate clinically meaningful pattern.
- Mildly low transferrin: contextual unless an independent iron/protein/liver pattern justifies separate concern status.
- IDL phenotype: may contextualise but may not displace the direct hepatic finding.
- No urgent diagnostic claim is authorised from these results alone.

## 17. Domain-research requirements

This contract does not define numerical thresholds.

The following governed domain work is required before production implementation:

1. Hepatic severity, urgency, R-value, and synthetic-function rules.
2. Electrolyte absolute thresholds and artefact rules.
3. Renal change-based and single-timepoint rules.
4. Haematology and cytopenia severity rules.
5. Iron, ferritin, transferrin saturation, and inflammatory-context rules.
6. Endocrine direction-specific rules.
7. Cardiometabolic and lipid risk-trigger rules.
8. Inflammatory-marker significance rules.
9. Nutritional-marker severity and actionability rules.
10. Cross-domain tier mapping.
11. Phenotype severity derivation.
12. Demographic and contextual modifiers.
13. Trend and persistence policy.
14. Urgency-language templates.
15. Clinical review and versioning cadence.

## 18. First pilot domain

The first policy pilot should be hepatic because:

- it contains the observed UAT failure;
- the current architecture already computes a liver-pattern R-value;
- the domain supports clear pattern classification;
- it demonstrates confidence-versus-priority separation;
- it provides an immediate test of contextual MCV and transferrin handling.

The hepatic pilot must define:

- ALT and AST severity bands;
- R-value classification;
- bilirubin, albumin, INR, and platelet modifiers;
- urgent and non-urgent escalation conditions;
- missing-AST handling;
- analytical and clinical caveats;
- action-tier mapping;
- contextual-marker attachment;
- acceptance scenarios.

## 19. Governance and authority

### 19.1 Clinical authorship

The HealthIQ Head of Medical Research owns this policy and any clinical threshold assets derived from it.

### 19.2 Independent medical validation

An independent medical reviewer must:

- challenge the clinical assumptions;
- verify evidence use;
- identify unsafe generalisation;
- test challenge cases;
- review false-reassurance and over-escalation risks.

### 19.3 Product ratification

Anthony must ratify:

- the lead-plus-tiered-concern-set product model;
- co-lead policy;
- tier visibility;
- user-facing tier names;
- missing-data transparency;
- governance authority;
- threshold versioning and auditability.

### 19.4 Architecture hardening

Claude Code must validate:

- repository compatibility;
- contract impact;
- data-flow boundaries;
- consolidation location;
- versioning requirements;
- IDL and frontend dependencies;
- migration and regression risk.

Claude Code does not validate clinical truth.

### 19.5 Implementation authority

No Cursor implementation prompt may be issued until:

1. independent medical validation is complete;
2. Head of Medical Research reconciliation is complete;
3. Anthony has ratified the product decisions;
4. architecture hardening is complete;
5. the hepatic pilot has a clinically governed specification;
6. acceptance scenarios are approved.

## 20. Status and next action

Current status:

`DRAFT_FOR_INDEPENDENT_MEDICAL_VALIDATION`

Next action:

Send this contract to an independent medical reviewer for a structured red-team review.

The reviewer must conclude with one of:

- `VALIDATE`
- `VALIDATE_WITH_REQUIRED_REVISIONS`
- `REJECT_AND_REDESIGN`
