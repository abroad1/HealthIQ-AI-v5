---
document_id: HEALTHIQ-CROSS-DOMAIN-PRIORITY-VALIDATION-001
title: HealthIQ Cross-Domain Clinical Prioritisation Validation Specification
version: "0.1"
status: READY_FOR_INDEPENDENT_MEDICAL_VALIDATION
owner: HealthIQ Head of Medical Research
product_authority: Anthony
governing_contract: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.3
implementation_status: NOT_AUTHORISED
supersedes_domain_sequence: HEPATIC_FIRST_DETAILED_RULE_AUTHORING
---

# HealthIQ Cross-Domain Clinical Prioritisation Validation Specification v0.1

## 1. Purpose

This specification tests whether the ratified HealthIQ Clinical Finding Prioritisation Contract v0.3 works safely and coherently across the full priority biomarker landscape before further detailed domain rulesets are authored.

It is a breadth-first validation exercise.

It must determine:

- which prioritisation principles are genuinely universal;
- which principles require domain-specific interpretation;
- where the current contract is incomplete or unsafe;
- whether the four-tier concern model works across unlike clinical domains;
- whether one orienting lead can be selected safely across domains;
- which detailed rulesets should be authored first;
- which domains require additional specialist input before specification.

This exercise must not define production thresholds for every marker.

## 2. Governing clinical model

The validation must apply the following ratified principles:

1. The unit of prioritisation is a consolidated clinical finding or pattern.
2. Urgency, severity, clinical significance, actionability, confidence, reliability and trend remain separate.
3. Urgency and severity establish the tier floor.
4. Confidence affects explanation, not prominence.
5. Supporting-marker count, frame count and panel completeness do not determine priority.
6. Multiple frames consolidate before prioritisation.
7. Contextual findings cannot displace a direct Tier 0 or Tier 1 finding.
8. The lead is selected from the highest non-empty concern tier.
9. Presentation and IDL priority cannot reorder clinical priority.
10. No-concern and insufficient-data outputs must remain distinct.
11. Domain-specific severity methods are expected; no universal biomarker score is authorised.
12. Governed overrides are the only route for multi-tier promotion.

## 3. Scope

The validation must cover the following domains:

1. hepatic;
2. electrolytes and acute metabolic disturbance;
3. renal;
4. haematology;
5. iron status;
6. thyroid and endocrine;
7. cardiometabolic and lipid risk;
8. inflammatory and immune-context markers;
9. nutritional and deficiency markers;
10. cross-domain findings and lead contests.

The hepatic ruleset already produced is retained as source material for the hepatic domain only. It is not the template for the other domains.

## 4. Out of scope

This specification does not authorise:

- production implementation;
- frontend design;
- final numerical thresholds for every biomarker;
- complete aetiological diagnosis;
- disease-specific treatment recommendations;
- medication cessation advice;
- paediatric, neonatal or pregnancy interpretation unless explicitly considered as an exclusion or safety boundary;
- architecture or sprint implementation;
- automatic conversion of every abnormal marker into a concern.

## 5. Validation method

For each domain, the reviewer must answer the same ten questions.

### 5.1 Clinician first-look hierarchy

Identify:

- the small set of markers a clinician typically inspects first;
- markers commonly deferred until the first-pass pattern is known;
- markers that are low-yield in isolation;
- markers that become important only conditionally.

This is not permission to ignore secondary markers permanently. It defines staged clinical attention.

### 5.2 Canonical consolidated findings

Define only the major finding classes a clinician would recognise at first pass.

Examples include:

- an electrolyte disturbance;
- an acute renal-function change;
- a cytopenia pattern;
- an iron-deficiency pattern;
- a thyroid-axis pattern;
- a long-term cardiometabolic-risk finding.

Do not create one finding per signal frame.

### 5.3 Urgency drivers

Identify what makes a finding time-sensitive, including whether urgency is driven by:

- absolute concentration;
- rate of change;
- organ dysfunction;
- symptoms or context;
- analytical artefact risk;
- a recognised combination;
- a critical threshold;
- inability to exclude a serious state.

### 5.4 Severity drivers

Identify the clinically appropriate severity method:

- absolute concentration;
- multiples of ULN or LRL;
- absolute cell count;
- percentage or absolute change from baseline;
- disease-stage bands;
- synthetic or organ function;
- combination pattern;
- long-term calculated risk.

State explicitly where magnitude is not a reliable proxy for significance.

### 5.5 Trend dependence

Classify the domain as:

- trend-essential;
- trend-important;
- trend-modifying;
- largely cross-sectional.

Identify which findings cannot be assessed safely without a valid baseline.

### 5.6 Combination and pattern dependence

Identify:

- combinations that create a new finding;
- combinations that change urgency;
- combinations that change severity;
- combinations that change confidence only;
- combinations that provide explanatory context only.

### 5.7 Contextual versus independent findings

Identify which markers are often contextual and the boundary at which they become independent concerns.

A marker may not be labelled contextual if it independently meets Tier 0 or Tier 1 criteria.

### 5.8 Confidence-only factors

Identify information that should alter certainty or wording but not prominence, including:

- missing corroborating markers;
- incomplete clinical history;
- possible alternative causes;
- absent baseline;
- analytical caveats;
- missing demographic context.

### 5.9 Provisional concern-tier behaviour

For each major finding class, describe its likely place within:

- Tier 0 — prompt clinical review;
- Tier 1 — discuss or investigate;
- Tier 2 — monitor, repeat or routine follow-up;
- Tier 3 — contextual.

Do not define detailed numerical boundaries unless a boundary is necessary to test the contract.

### 5.10 Contract stress test

State whether the domain:

- fits the contract without modification;
- fits only with domain-specific rules;
- exposes a contract ambiguity;
- exposes a cross-domain dependency;
- requires a contract amendment;
- is unsafe to specify without specialist review.

## 6. Required domain challenge cases

The validation must include at least the following representative cases.

### 6.1 Hepatic

- marked transaminase elevation with incomplete supporting markers;
- mild isolated abnormality;
- injury pattern with possible synthetic dysfunction;
- contextual MCV or ferritin;
- normal enzymes with unresolved fibrosis risk.

### 6.2 Electrolytes and acute metabolic disturbance

- marked potassium abnormality;
- possible haemolysis or analytical artefact;
- sodium abnormality with uncertain chronicity;
- calcium abnormality requiring albumin correction or ionised confirmation;
- abnormal result with symptoms unavailable.

### 6.3 Renal

- creatinine change from a valid baseline;
- reduced eGFR without baseline;
- stable chronic reduction;
- urea elevation as contextual rather than causal;
- renal abnormality with potassium disturbance.

### 6.4 Haematology

- isolated anaemia;
- low haemoglobin with low MCV;
- macrocytosis without anaemia;
- macrocytosis with another cytopenia;
- thrombocytopenia;
- neutropenia using absolute count rather than differential percentage;
- multi-lineage cytopenia.

The review must incorporate the clinician first-look principle: haemoglobin, MCV, platelets, total white count and absolute neutrophils are primary triage markers, while lower-yield indices enter conditionally.

### 6.5 Iron status

- low ferritin;
- raised ferritin with low or normal TSAT;
- raised ferritin with high TSAT;
- absent TSAT despite available iron and transferrin;
- iron findings with inflammation;
- iron findings with anaemia.

### 6.6 Thyroid and endocrine

- raised TSH with low free T4;
- raised TSH with normal free T4;
- suppressed TSH with raised free T4;
- isolated TSH abnormality with missing free hormone;
- abnormal result in a context where treatment or pregnancy status is unavailable.

### 6.7 Cardiometabolic and lipid risk

- severely raised triglycerides;
- markedly raised LDL cholesterol;
- moderate lipid abnormalities with high aggregate risk;
- apparently minor biomarker abnormality with major long-term consequence;
- discordance between immediate urgency and long-term actionability.

### 6.8 Inflammatory and immune-context markers

- isolated CRP elevation;
- persistent inflammatory pattern;
- CRP as explanation for ferritin;
- inflammatory markers with anaemia;
- non-specific marker abnormality without symptoms.

### 6.9 Nutritional and deficiency markers

- severe deficiency with neurological or haematological consequences;
- borderline deficiency without corroboration;
- functional deficiency pattern despite an in-range value;
- deficiency marker influenced by inflammation or binding proteins;
- multiple deficiencies competing with a more urgent direct finding.

### 6.10 Cross-domain lead contests

The reviewer must adjudicate, at principle level, cases such as:

- marked hepatic injury versus mild macrocytosis;
- thrombocytopenia versus suspected hepatic fibrosis;
- severe electrolyte abnormality versus high long-term cardiovascular risk;
- acute renal decline versus chronic lipid risk;
- possible iron overload versus inflammatory ferritin;
- multiple Tier 1 findings with genuinely different action pathways.

The exercise must identify where the shared tier model is sufficient and where cross-domain tie-break rules remain unresolved.

## 7. Required outputs for each domain

For every domain, produce a compact table with:

| Field | Required content |
|---|---|
| First-look markers | Primary clinician triage markers |
| Deferred/conditional markers | Markers reviewed after the first-pass pattern |
| Major consolidated findings | Bounded finding classes |
| Urgency drivers | What controls time sensitivity |
| Severity method | Appropriate domain-specific method |
| Trend role | Essential, important, modifying or limited |
| Combination rules | Pattern-forming or urgency-changing combinations |
| Contextual markers | Markers that usually refine rather than lead |
| Confidence-only factors | Factors that change certainty, not priority |
| Provisional tier behaviour | Tier 0–3 principles |
| Contract fit | Pass, conditional pass, amendment required or unsafe |
| Dependencies | Other domains, context, regulatory or operational needs |

## 8. Universal-rule extraction

After completing all domains, the reviewer must identify:

### 8.1 Confirmed universal rules

Rules that held safely across every tested domain.

### 8.2 Domain-specific rules

Rules that are valid only within a named domain.

### 8.3 Cross-domain rules

Rules required to compare unlike findings safely.

### 8.4 Contract amendments

Any wording or structural change required to contract v0.3.

### 8.5 Prohibited universalisation

Any rule that worked in one domain but would be unsafe if applied globally.

Examples to test include:

- multiples of ULN;
- reference-range abnormality as a Tier 1 floor;
- supporting-marker count;
- requirement for corroboration;
- trend-based downgrading;
- static domain priority;
- fixed ordering of marker classes.

## 9. Breadth gate

The broad model passes only if the review demonstrates that:

1. every priority domain can express findings using the same core clinical dimensions;
2. no domain requires confidence to control prominence;
3. no domain requires supporting-marker count to determine priority;
4. every domain can distinguish direct, contextual and pattern-level findings;
5. urgency and severity can be separated;
6. the tier model remains clinically intelligible across domains;
7. cross-domain lead contests can either be resolved or explicitly bounded;
8. no hepatic-specific concept has silently become a universal rule;
9. no major priority biomarker domain has been omitted;
10. the result supports a safe sequence for detailed domain authoring.

Failure of one item does not automatically invalidate the model, but it must produce an explicit amendment or bounded exception.

## 10. Detailed-rule sequencing decision

The reviewer must recommend the next detailed ruleset sequence based on:

- clinical safety value;
- cross-domain dependency value;
- ability to test the model;
- availability of authoritative guidance;
- regulatory implications;
- risk of temporary thresholds becoming precedent;
- reuse across other domains.

Do not recommend a number of sprints.

Do not assume hepatic remains first.

## 11. Evidence standard

Use UK-first clinical evidence:

- NICE;
- NHS pathways;
- Royal Colleges;
- recognised UK specialist societies;
- MHRA where relevant;
- recognised international guidance only where UK evidence is absent.

For each material conclusion, classify it as:

- evidence-supported rule;
- accepted clinical convention;
- HealthIQ clinical judgement;
- unresolved question.

The exercise is not a systematic review of every threshold. Evidence should be sufficient to validate the prioritisation structure and expose exceptions.

## 12. Required deliverable

Produce:

`HEALTHIQ_CROSS_DOMAIN_CLINICAL_PRIORITISATION_VALIDATION_REPORT_v0.1.md`

The report must contain:

1. executive conclusion;
2. domain-by-domain validation tables;
3. challenge-case results;
4. confirmed universal rules;
5. domain-specific exceptions;
6. cross-domain dependencies;
7. proposed contract amendments;
8. prohibited universalisation list;
9. unresolved clinical questions;
10. recommended sequence for detailed ruleset authoring;
11. evidence table;
12. reviewer verdict.

Conclude with exactly one of:

- `VALIDATE_BROAD_MODEL`
- `VALIDATE_WITH_CONTRACT_AMENDMENTS`
- `REQUIRES_ADDITIONAL_CROSS_DOMAIN_RESEARCH`
- `REJECT_AND_REDESIGN`

## 13. Governance sequence

1. Independent cross-domain medical validation.
2. Head of Medical Research reconciliation.
3. Anthony ratification of any product-model or contract changes.
4. Specialist regulatory constraints applied in parallel.
5. Selection of the first detailed domain ruleset.
6. Claude Code architecture hardening only after the clinical model and domain sequence are settled.
7. Cursor implementation only after formal authorisation.

## 14. Current status

`READY_FOR_INDEPENDENT_MEDICAL_VALIDATION`

The existing hepatic ruleset remains retained as domain evidence. It is not clinically ratified, not implementation-ready and must not control the cross-domain conclusions.
