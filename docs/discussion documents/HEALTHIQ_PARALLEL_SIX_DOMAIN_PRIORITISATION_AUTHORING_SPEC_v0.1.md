---
document_id: HEALTHIQ-PARALLEL-DOMAIN-PRIORITY-AUTHORING-001
title: HealthIQ Parallel Six-Domain Clinical Prioritisation Authoring Specification
version: "0.1"
status: READY_FOR_PARALLEL_MEDICAL_AUTHORING
owner: HealthIQ Head of Medical Research
product_authority: Anthony
governing_contract: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.5
implementation_status: NOT_AUTHORISED
---

# HealthIQ Parallel Six-Domain Clinical Prioritisation Authoring Specification v0.1

## 1. Purpose

This specification commissions six clinical-prioritisation domain workstreams in parallel.

The objective is to produce a complete cross-domain medical ruleset without creating a serial domain-by-domain bottleneck.

The six workstreams are:

1. haematology;
2. hepatic;
3. renal and electrolytes;
4. iron and inflammatory;
5. thyroid and endocrine;
6. cardiometabolic and nutritional.

All six workstreams must use the same governing contract, evidence standards, output structure and reconciliation rules.

No workstream may treat its own domain conventions as universal.

## 2. Governing policy

All workstreams must apply:

`HEALTHIQ_CLINICAL_FINDING_PRIORITISATION_CONTRACT_v0.5.md`

The governing principles include:

- consolidated clinical findings rather than raw markers or signal frames;
- urgency and severity as separate dimensions;
- common urgency time bands:
  - same day;
  - within days;
  - within weeks;
  - routine;
- domain-specific severity methods;
- confidence separated from prominence;
- no use of supporting-marker count, frame count or panel completeness as priority inputs;
- cross-domain severity values must not be compared directly;
- missing data must not silently suppress findings;
- indeterminate-severity rules must be defined by each domain;
- marker–modifier pairs must be explicitly governed;
- contextual findings cannot hide independently important findings;
- same-day findings may form an uncapped co-equal group;
- no-concern and insufficient-data outputs remain distinct;
- domain-specific rules must not be universalised without explicit cross-domain approval.

## 3. Parallel workstreams

### 3.1 Workstream A — Haematology

Must cover:

- haemoglobin;
- MCV;
- platelets;
- total white-cell count;
- absolute neutrophil count;
- lymphocytes, monocytes and eosinophils where clinically relevant;
- reticulocytes where available;
- red-cell indices as conditional or contextual markers;
- isolated and multi-lineage cytopenias;
- thrombocytosis;
- neutropenia;
- leucocytosis;
- macrocytosis;
- microcytosis;
- anaemia patterns;
- pseudothrombocytopenia and analytical caveats.

Must define:

- clinician first-look hierarchy;
- absolute-count severity bands;
- urgency time bands;
- multi-lineage consolidation;
- contextual-versus-independent boundaries;
- indeterminate-severity rules where differential or MCV data are missing;
- specification-only versus release-authorised Tier 0 rules.

### 3.2 Workstream B — Hepatic

Must use the existing hepatic ruleset as source material but reconcile it against contract v0.5.

Must cover:

- ALT;
- AST;
- ALP;
- GGT;
- bilirubin;
- albumin;
- INR where available;
- platelets where used in hepatic context;
- hepatic pattern classification;
- synthetic dysfunction;
- fibrosis-related context;
- trend;
- missing markers;
- medication, alcohol and metabolic context where available.

Must:

- label the hepatic Tier 1 floor as domain-specific;
- remove temporary haematology thresholds;
- preserve explicit haematology dependencies;
- distinguish specification-only Tier 0 rules;
- avoid universalising R-value, multiples of ULN or hepatic investigation rules.

### 3.3 Workstream C — Renal and electrolytes

Must cover:

- creatinine;
- eGFR;
- urea;
- potassium;
- sodium;
- calcium;
- albumin-adjusted calcium;
- bicarbonate;
- magnesium;
- phosphate where available;
- change from baseline;
- acute versus chronic renal dysfunction;
- analytical artefact and repeat-confirmation rules;
- renal–electrolyte combinations.

Must define:

- trend-essential renal findings;
- baseline validity rules;
- absolute-concentration electrolyte severity;
- marker–modifier pairs;
- same-day escalation criteria;
- artefact-safe urgent wording;
- insufficient-data rules where correction or baseline is unavailable.

Renal and electrolyte outputs must be authored as one coordinated workstream.

### 3.4 Workstream D — Iron and inflammatory

Must cover:

- ferritin;
- transferrin saturation;
- serum iron;
- transferrin or TIBC;
- CRP;
- ESR where available;
- haemoglobin and MCV dependencies;
- iron-deficiency patterns;
- iron-deficiency anaemia;
- possible iron overload;
- inflammatory or dysmetabolic hyperferritinaemia;
- functional iron deficiency;
- in-range ferritin under inflammatory conditions;
- absent TSAT where calculation is possible from available inputs.

Must define:

- ferritin direction asymmetry;
- when CRP is contextual versus independently important;
- TSAT calculation policy;
- iron–haematology consolidation;
- inflammatory-marker persistence rules;
- missing-modifier and insufficient-data handling.

### 3.5 Workstream E — Thyroid and endocrine

Must cover:

- TSH;
- free T4;
- free T3 where relevant;
- thyroid antibodies as contextual or prognostic markers;
- overt and subclinical hypo- and hyperthyroid patterns;
- indeterminate thyroid-axis findings;
- discordant results;
- treatment-status limitations;
- pregnancy exclusion or special-handling requirements;
- other endocrine markers already within the HealthIQ priority landscape where sufficient evidence exists.

Must define:

- pattern-based severity;
- domain-specific indeterminate-severity rules;
- missing free-hormone handling;
- urgency limitations where clinical symptoms are unavailable;
- context required before interpretation;
- findings that should remain out of scope.

### 3.6 Workstream F — Cardiometabolic and nutritional

Must cover:

- total cholesterol;
- non-HDL cholesterol;
- LDL cholesterol;
- HDL cholesterol;
- triglycerides;
- HbA1c;
- fasting glucose where available;
- aggregate cardiovascular risk where valid;
- possible familial hypercholesterolaemia patterns;
- B12;
- folate;
- vitamin D;
- homocysteine where governed;
- functional deficiency patterns;
- deficiency-related haematology dependencies;
- binding-protein and inflammatory caveats.

Must define:

- long-term calculated risk as a severity method;
- low urgency but high clinical importance;
- severe triglyceride urgency;
- named referral thresholds;
- context dependencies for risk calculation;
- nutritional urgency driven by neurological or haematological consequence;
- in-range functional-deficiency findings;
- findings that cannot safely be produced without additional context.

## 4. Common required questions

Each workstream must answer:

1. What does a clinician inspect first?
2. Which markers are reviewed only conditionally?
3. What are the canonical consolidated findings?
4. What creates urgency?
5. What creates severity?
6. What role does trend play?
7. Which combinations create a new finding?
8. Which markers are contextual?
9. Which factors affect confidence only?
10. Which marker–modifier pairs are uninterpretable when incomplete?
11. What creates indeterminate severity?
12. How are findings mapped to Tier 0–3?
13. Which Tier 0 rules are specification-only?
14. Which findings require same-day, days, weeks or routine action?
15. Which findings can consolidate across domains?
16. Which domain rules must not be universalised?
17. Which unresolved questions require HMR adjudication?
18. Which rules are unsafe without clinical context?

## 5. Common evidence standard

Use UK-first evidence:

- NICE;
- NHS pathways;
- Royal Colleges;
- British specialist societies;
- MHRA where relevant;
- recognised international guidance only where UK guidance is absent.

Every rule must be labelled:

- `[E]` evidence-supported;
- `[C]` accepted clinical convention;
- `[J]` HealthIQ clinical judgement;
- `[U]` unresolved.

Every threshold, override, combination and action-timeframe rule must include:

- source;
- scope;
- rationale;
- limitations;
- review date or version.

## 6. Common output structure

Each workstream must produce:

1. scope and exclusions;
2. clinician first-look hierarchy;
3. canonical finding taxonomy;
4. urgency rules and time bands;
5. severity rules;
6. indeterminate-severity rules;
7. trend and baseline rules;
8. modifier and interpretability rules;
9. combination and override register;
10. contextual-marker rules;
11. confidence-only factors;
12. concern-tier mapping;
13. lead-selection examples;
14. no-concern outputs;
15. insufficient-data outputs;
16. acceptance scenarios;
17. prohibited behaviours;
18. unresolved questions;
19. evidence table;
20. clinical sign-off fields.

## 7. Cross-stream coordination rules

The six workstreams are parallel, but not independent silos.

The following shared-marker boundaries must be reconciled explicitly:

- platelets: haematology and hepatic;
- MCV: haematology, hepatic and nutritional;
- haemoglobin: haematology, iron, inflammatory and nutritional;
- albumin: hepatic, calcium interpretation and inflammatory context;
- ferritin: iron, inflammatory and hepatic;
- CRP: inflammatory, iron and nutritional;
- potassium: renal and electrolyte;
- creatinine/eGFR: renal and cardiometabolic context;
- thyroid function: endocrine and cardiometabolic secondary-cause interpretation;
- B12/folate: nutritional and haematology.

No workstream may finalise a shared-marker rule without recording:

- the marker’s role in its own domain;
- the boundary at which another domain becomes primary;
- whether the result consolidates, attaches contextually or remains separate;
- the applicable urgency time band;
- any conflict requiring central adjudication.

## 8. Central reconciliation deliverable

After all six workstreams complete, produce one consolidated document:

`HEALTHIQ_CROSS_DOMAIN_CLINICAL_PRIORITISATION_RULESET_v0.1.md`

The consolidated ruleset must include:

1. universal rules;
2. six domain rule sections;
3. shared-marker boundary register;
4. cross-domain combination register;
5. urgency time-band register;
6. indeterminate-severity register;
7. marker–modifier register;
8. Tier 0 specification-only register;
9. same-day co-equal group rules;
10. cross-domain lead-selection rules;
11. prohibited universalisation register;
12. unresolved product, clinical and regulatory questions;
13. evidence and provenance register;
14. acceptance-test matrix.

## 9. Parallel authoring discipline

The six workstreams may be researched simultaneously.

They must not be ratified independently before central reconciliation.

A workstream may finish earlier, but early completion does not make it the precedent for other domains.

Temporary thresholds, placeholders or assumptions must be clearly labelled and may not enter the consolidated ruleset without adjudication.

## 10. Required individual deliverables

Produce:

1. `HEALTHIQ_HAEMATOLOGY_PRIORITISATION_RULESET_v0.1.md`
2. `HEALTHIQ_HEPATIC_PRIORITISATION_RULESET_v0.2.md`
3. `HEALTHIQ_RENAL_ELECTROLYTE_PRIORITISATION_RULESET_v0.1.md`
4. `HEALTHIQ_IRON_INFLAMMATORY_PRIORITISATION_RULESET_v0.1.md`
5. `HEALTHIQ_THYROID_ENDOCRINE_PRIORITISATION_RULESET_v0.1.md`
6. `HEALTHIQ_CARDIOMETABOLIC_NUTRITIONAL_PRIORITISATION_RULESET_v0.1.md`

Each must conclude with exactly one of:

- `READY_FOR_CENTRAL_RECONCILIATION`
- `REQUIRES_ADDITIONAL_DOMAIN_RESEARCH`
- `UNSAFE_TO_SPECIFY`

## 11. Governance sequence

1. Six parallel medical-authoring workstreams.
2. Head of Medical Research central reconciliation.
3. Independent cross-domain consistency review.
4. Anthony ratification of any product or scope decisions.
5. Specialist regulatory constraints applied.
6. Claude Code architecture hardening.
7. GPT approval of policy-to-architecture mapping.
8. Cursor implementation only after formal authorisation.

## 12. Status

`READY_FOR_PARALLEL_MEDICAL_AUTHORING`
