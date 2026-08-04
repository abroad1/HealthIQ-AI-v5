---
document_id: HEALTHIQ-HMR-CROSS-DOMAIN-RECONCILIATION-001
title: HealthIQ Head of Medical Research Reconciliation — Six-Domain Clinical Prioritisation Rulesets
version: "0.1"
status: HMR_RECONCILIATION_COMPLETE_WITH_REQUIRED_CLOSURES
governing_contract: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.5
reviews:
  - HEALTHIQ-HAEM-RULESET-001 v0.1
  - HEALTHIQ-HEPATIC-RULESET-001 v0.2
  - HEALTHIQ-RENAL-ELEC-RULESET-001 v0.1
  - HEALTHIQ-IRON-INFLAM-RULESET-001 v0.1
  - HEALTHIQ-THYROID-ENDO-RULESET-001 v0.1
  - HEALTHIQ-CARDIO-NUTRI-RULESET-001 v0.1
  - HEALTHIQ-CROSS-DOMAIN-RULESET-001 v0.1
implementation_status: NOT_AUTHORISED
---

# HMR Reconciliation — Six-Domain Clinical Prioritisation Rulesets v0.1

## 1. Executive verdict

The six-domain authoring exercise has validated the operating model and produced a coherent cross-domain structure.

The package is **not yet clinically ratifiable as a production ruleset** because:

1. the renal/electrolyte workstream has three missing evidence-based severity band sets;
2. Tier 0 release remains unresolved operationally and regulatorily;
3. pregnancy handling is inconsistent and unsafe across the landscape;
4. several product-scope decisions remain open;
5. the workstreams were authored against v0.4 plus a v0.5 summary and require clause-level conformance against the actual v0.5 contract;
6. some proposed cross-domain rules exceed what has yet been medically or product-ratified.

HMR disposition:

`RECONCILIATION_COMPLETE_WITH_REQUIRED_CLOSURES`

No redesign is required.

## 2. What is approved in principle

The following are accepted as the governing clinical structure:

- consolidated clinical findings are the unit of prioritisation;
- urgency and severity remain separate;
- cross-domain ordering uses common time-to-action bands;
- severity is domain-specific and cannot be compared directly across unlike domains;
- confidence, supporting-marker count, frame count and panel completeness cannot control prominence;
- missing discriminators must not silently suppress findings;
- uninterpretable-without-modifier and indeterminate-severity are distinct states;
- no trend-based downgrade is authorised as a universal mechanism;
- contextual findings cannot absorb independently important Tier 0 or Tier 1 findings;
- same-day findings form a co-equal group where no governed clinical distinction exists;
- no-concern output must state what normal results do not exclude;
- an empty Tier 0 register is a legitimate domain outcome;
- domain-specific conventions may not be exported universally.

## 3. Domain dispositions

### 3.1 Haematology

Disposition:

`ACCEPT_STRUCTURE_WITH_REQUIRED_ADJUDICATIONS`

Accepted:

- clinician first-look hierarchy;
- absolute counts rather than percentages;
- one anaemia finding with MCV subtype;
- multi-lineage cytopenia as one consolidated finding;
- platelet urgency bands;
- isolated mild macrocytosis as Tier 2;
- haematology ownership of Hb, MCV and platelet severity bands;
- Tier 0 rules remain specification-only.

Required closures:

- severe-anaemia same-day threshold;
- benign ethnic neutropenia handling without reliable ancestry;
- leucocytosis escalation threshold;
- pregnancy policy;
- unsourced baseline-validity windows.

Rejected or amended:

- sex-unknown behaviour must not silently apply the female haemoglobin threshold as a universal default. It requires an explicit demographic policy and must remain indeterminate until ratified.

### 3.2 Hepatic

Disposition:

`ACCEPT_STRUCTURE_WITH_POLICY_DECISIONS`

Accepted:

- one consolidated hepatic pattern;
- domain-bound use of multiples of ULN;
- R-value as an internal hepatic pattern classifier only;
- synthetic function outranking injury;
- missing AST/ALP/albumin/INR affecting assessability or confidence, not significance;
- haematology-derived contextual boundaries;
- specification-only Tier 0 register;
- explicit non-export of the hepatic Tier 1 floor.

Required closures:

- HEP-U1: literal BSG Tier 1 floor versus governed modified approach;
- bilirubin urgency threshold;
- isolated GGT disposition;
- pregnancy policy;
- FIB-4 regulatory decision;
- rules unsafe without medication, alcohol and metabolic context.

HMR position:

The hepatic Tier 1 floor remains domain-specific and must not be ratified until HEP-U1 is decided. It must not enter the consolidated ruleset as settled policy.

### 3.3 Renal and electrolytes

Disposition:

`NOT READY — BOUNDED ADDITIONAL RESEARCH REQUIRED`

Accepted:

- renal and electrolytes authored together;
- AKI as change-defined;
- CKD chronicity rules;
- potassium, hyponatraemia and hypercalcaemia structure;
- uncorrected calcium requiring albumin;
- artefact-safe urgent wording;
- renal–electrolyte combinations;
- Tier 0 specification-only treatment.

Blocking research:

- evidence-based hypokalaemia severity and urgency bands;
- evidence-based hypernatraemia severity and urgency bands;
- evidence-based hypocalcaemia severity and urgency bands.

Required decisions:

- potassium urgent threshold;
- renal/electrolyte release without Tier 0 capability;
- eGFR staging without ACR;
- dialysis/transplant exclusions;
- pregnancy;
- baseline validity.

HMR position:

Renal/electrolytes must not be incorporated into a final clinical ruleset until the three missing band sets are supplied and reviewed.

### 3.4 Iron and inflammatory

Disposition:

`ACCEPT_STRUCTURE_WITH_BOUNDED GAPS`

Accepted:

- TSAT, not ferritin magnitude, governs overload concern;
- iron deficiency anaemia consolidates with haematology;
- in-range ferritin may conceal deficiency under inflammation;
- TSAT must be derived when inputs permit;
- CRP is usually contextual;
- empty Tier 0 register;
- iron/inflammatory outputs should rarely lead.

Required closures:

- low-TSAT deficiency threshold;
- CRP escalation policy;
- ancestry handling;
- sex-specific threshold behaviour where sex is unavailable;
- ESR scope;
- communication policy for naming haemochromatosis.

HMR position:

Do not invent universal CRP severity bands. CRP should remain primarily contextual unless an evidence-supported persistent or marked pattern is defined.

### 3.5 Thyroid and endocrine

Disposition:

`THYROID ACCEPTED; ENDOCRINE SCOPE INCOMPLETE`

Accepted:

- TSH and free T4 as one finding;
- pattern-based severity;
- THY-F5 indeterminate thyroid-axis finding;
- TSH ≥10 mIU/L as a governed subclinical threshold;
- discordant patterns require specialist interpretation;
- empty Tier 0 register;
- thyroid as a secondary-cause context for lipids and macrocytosis.

Required closures:

- subclinical hyperthyroidism bands;
- marked thyrotoxicosis urgency;
- pregnancy policy;
- communication policy for disease labels;
- scope decision for non-thyroid endocrine axes.

HMR position:

This workstream currently validates thyroid only. It must not be represented as complete endocrine coverage.

Known pregnancy must not produce silent suppression. It must produce an explicit out-of-scope/special-rules-required output until a pregnancy-specific ruleset exists.

### 3.6 Cardiometabolic and nutritional

Disposition:

`ACCEPT STRUCTURE WITH REGULATORY AND EVIDENCE CLOSURES`

Accepted:

- long-term risk as a severity method;
- low urgency must not imply low importance;
- triglycerides >20 mmol/L as a same-day specification-only rule;
- one consolidated lipid finding;
- secondary-cause reframing without downgrade;
- B12 consequence-based severity;
- functional deficiency with an in-range value;
- nutritional consolidation with haematology.

Required closures:

- regulatory decision on individual risk calculation;
- vitamin D evidence bands or formal exclusion;
- HbA1c invalidity policy;
- symptom self-report dependency for neurological B12 concern;
- homocysteine/MMA governance;
- naming familial hypercholesterolaemia;
- dysglycaemia same-day scope;
- pregnancy policy.

HMR position:

Do not compute or display individual cardiovascular risk until the regulatory workstream has explicitly approved the intended purpose and method.

## 4. Cross-domain rules accepted

The following central rules are accepted:

1. Shared markers have domain-declared roles.
2. Haemoglobin severity is owned by haematology.
3. MCV severity is owned by haematology.
4. Platelet severity is owned by haematology.
5. Ferritin and TSAT interpretation is owned by iron.
6. Albumin has domain-conditional roles.
7. Potassium is owned by renal/electrolytes.
8. Thyroid findings may also appear as explanatory context without becoming a second concern.
9. Derived modifiers must be calculated when validated inputs permit.
10. Unevaluable combination criteria are reported as not assessable, not not-met.
11. Anaemia must never appear twice.
12. Same-day cross-domain findings may form an uncapped co-equal group.
13. Normal-result outputs require domain-specific limitation statements.

## 5. Cross-domain rules requiring amendment before ratification

### 5.1 A7 — Two missing-modifier consequences

Approve for inclusion in the next contract revision:

- insufficient data where the marker is not interpretable without the modifier;
- indeterminate severity where the marker is valid but cannot distinguish material clinical states.

### 5.2 A8 — Derivation obligation

Approve in principle, subject to a validated formula and unit contract for every derived value.

No value may be derived merely because a mathematical formula exists. The formula, units, assay assumptions, provenance and version must be governed.

### 5.3 A9 — Empty Tier 0

Approve.

A domain with no evidence-supported same-day biochemical rule should have an empty Tier 0 register.

### 5.4 Proposed cross-domain lead distinguishers

Do not yet ratify the proposed universal tie-breakers:

- organ dysfunction over marker abnormality;
- irreversible harm over reversible harm;
- direct measurement over derived interpretation.

They are clinically plausible but not yet sufficiently bounded across all domains. Until separately validated, equal time-band cross-domain findings remain co-leads.

## 6. Rules rejected or prohibited

The following must not enter the consolidated governed ruleset:

- a universal Tier 1 floor for any out-of-range marker;
- direct comparison of domain severity bands;
- unsourced electrolyte thresholds;
- unsourced vitamin D bands;
- a universal CRP severity scale;
- automatic sex or ancestry assumptions;
- silent pregnancy suppression;
- individual cardiovascular risk calculation before regulatory approval;
- FIB-4 before regulatory approval;
- demotion of Tier 0 findings where the operational pathway is unavailable;
- presenting a finding with no governed severity or indeterminate disposition;
- temporary thresholds carried forward as precedent.

## 7. Pregnancy policy

Current state is unacceptable:

- most domains exclude pregnancy;
- thyroid proposes suppression where pregnancy is known;
- pregnancy status is often unavailable;
- no common output behaviour exists.

Interim HMR policy:

1. No pregnancy-adjusted interpretation is authorised.
2. Where pregnancy is known, affected findings must produce an explicit out-of-scope/specialist-rules-required output.
3. Findings must not be silently suppressed.
4. Where pregnancy status is unknown, the product must state that interpretation assumes non-pregnant adult reference rules where that assumption materially affects the domain.
5. A future pregnancy-specific ruleset is separate work and is not required to complete the non-pregnant adult ruleset.

## 8. Tier 0 policy

Tier 0 medical rules may be specified, but no Tier 0 output may be released without the contract §17 operational pathway and regulatory/legal approval.

HMR judgement:

- renal/electrolytes should not be released if they can identify life-threatening abnormalities but cannot provide governed same-day guidance;
- Tier 0 findings must not be demoted;
- withholding must be explicit and auditable;
- domains with empty Tier 0 registers may proceed independently, subject to their other dependencies;
- this is a product-release decision, not a reason to weaken the clinical rules.

## 9. Context-free operation

Every workstream identified rules whose source guidance assumes clinical history, symptoms, medications or examination.

Interim HMR policy:

- missing context normally limits specificity and confidence;
- it does not normally lower prominence;
- a rule is unsafe without context only where the missing item changes whether the measured value is interpretable, changes the applicable reference framework, or changes the action category materially;
- each domain must enumerate these unsafe-without-context cases;
- pregnancy, treatment status for some thyroid patterns, anticoagulation for INR, calcium without albumin, and absent baseline for AKI are reference examples.

## 10. Required closures before final consolidated ruleset

### Clinical evidence

1. Hypokalaemia bands.
2. Hypernatraemia bands.
3. Hypocalcaemia bands.
4. Severe-anaemia threshold.
5. Subclinical hyperthyroidism handling.
6. Low-TSAT deficiency threshold.
7. Vitamin D inclusion and bands.
8. Bilirubin urgent threshold.

### HMR policy

1. Hepatic Tier 1 floor.
2. Potassium urgent threshold.
3. Pregnancy policy adoption.
4. Context-free unsafe-rule register.
5. Sex and ancestry handling.
6. Baseline-validity framework.
7. Endocrine scope beyond thyroid.
8. CRP role and escalation policy.

### Product authority

1. Same-day group presentation.
2. Tier 1 volume control.
3. Dual-role presentation.
4. Disease-name communication policy.
5. No-concern limitation presentation.
6. Release sequencing for domains with and without Tier 0.

### Regulatory/legal

1. Tier 0 action guidance.
2. Individual cardiovascular risk.
3. FIB-4.
4. Consumer disease-name outputs.
5. Domain exclusions and intended-purpose wording.

## 11. Next action

Do not send the seven documents to architecture or implementation.

The next medical action is a single bounded closure package containing:

1. supplemental research for the three missing electrolyte band sets;
2. a concise HMR adjudication register for the policy decisions above;
3. contract v0.6 incorporating A7–A9 and the pregnancy/output policy;
4. a corrected cross-domain consolidated ruleset v0.2;
5. one independent cross-domain consistency review.

No six separate review cycles are required.

## 12. Final verdict

`HMR_RECONCILIATION_COMPLETE_WITH_REQUIRED_CLOSURES`

The broad model is clinically coherent.

The six-domain parallel approach succeeded.

The package now requires bounded closure of evidence, policy and regulatory gaps before it can become a ratified clinical ruleset.
