# Medical Research Activation Review — Deferred Wave 1 Items

## Executive conclusion

This review assesses the deferred Wave 1 medical-intelligence items for HealthIQ AI. It is a medical activation-authority review only. It does not implement runtime logic, author Knowledge Bus package files, or change activation status.

The main conclusion is:

- Several deferred items are medically valid for cautious, non-diagnostic runtime interpretation, but only with strict companion-marker and context gates.
- No item should be activated as a loose standalone consumer-facing signal.
- Several items remain blocked by Core Engine / SSOT / formula-governance issues rather than by medical invalidity.
- Thyroid antibody interpretation is medically defensible but should not become launch-visible until package scoping, PSI/promoted intelligence status, and wording boundaries are completed.
- TSAT calculated mode is medically meaningful, but the implementation blocker is formula/provenance governance, not medical validity.

### Cleared in principle for activation with strict gates

- FT3 low — only with TSH, FT4, illness/recovery, thyroid medication and energy-availability context.
- Iron low / absolute iron deficiency frame — only with ferritin and TSAT, plus CRP/inflammation context.
- Iron low / functional iron restriction-inflammation frame — only with CRP/inflammation context, ferritin and TSAT.
- Iron high / iron overload context — only with TSAT and ferritin support, plus liver/acute iron exposure caveats.
- Homocysteine high / B-vitamin-related methylation impairment — only with B12/active B12 and folate context, preferably MCV and MMA where available.
- Homocysteine high / renal clearance reduction — only with renal-function support and B-vitamin contradiction handling.
- TPO antibody high / autoimmune hypothyroid context — only with TSH and FT4 context, non-diagnostic wording and no treatment implication.

### Remain deferred

- Iron high / hepatocellular or haemolytic release frame — medically plausible, but current companion set is insufficient without stronger haemolysis/liver-injury confirmation logic.
- Leukocyte PSI cohort — medically plausible but should not activate until SSOT identity and system-mapping blockers are resolved; neutrophil percentage high should not activate without absolute neutrophil count.
- TPO antibody high / euthyroid autoimmune risk — medically defensible but better as post-launch / advanced-mode due risk of anxiety and low immediate actionability.
- TgAb packages — defer post-launch pending package scoping and full source review.
- TSAT calculated mode — defer to Core Engine policy for formula, unit normalisation and provenance labelling.

---

## Decision matrix

| Group | Candidate | Decision | Rationale | Required gates | Owner for next step |
| ----- | --------- | -------- | --------- | -------------- | ------------------- |
| FT3-low activation control | FT3 low / low T3 syndrome context | ACTIVATE_WITH_STRICT_GATES | Medically coherent but highly context-dependent; unsafe as isolated thyroid signal. | FT3 low by lab range; TSH present; FT4 present; thyroid medication status; illness/recovery status; calorie restriction/fasting/low energy context; pregnancy/postpartum route. | Medical Review + Knowledge Bus activation-control sprint |
| Iron Batch C | Iron low / absolute iron deficiency | ACTIVATE_WITH_STRICT_GATES | Low serum iron alone is weak; low ferritin + low TSAT makes deficiency frame medically defensible. | Serum iron low; ferritin low; TSAT low; CRP available or inflammation caveat; FBC indices strongly recommended; supplement/infusion context. | Medical Review then Knowledge Bus |
| Iron Batch C | Iron low / functional iron restriction-inflammation | ACTIVATE_WITH_STRICT_GATES | Plausible when low iron/TSAT occurs with inflammation and non-low ferritin. | Serum iron low; TSAT low; CRP/inflammatory marker high or declared inflammatory illness; ferritin normal/high; contradiction if ferritin low. | Medical Review then Knowledge Bus |
| Iron Batch C | Iron high / iron overload context | ACTIVATE_WITH_STRICT_GATES | High serum iron only becomes meaningful with high TSAT and ferritin support. | Serum iron high; TSAT high; ferritin high or supportive; liver markers; recent iron ingestion/infusion exclusion; haemolysis/liver-injury contradiction handling. | Medical Review then Knowledge Bus |
| Iron Batch C | Iron high / hepatocellular or haemolytic release | DEFER_MEDICAL_REVIEW | Plausible but current frame is under-gated; ALT/bilirubin alone does not safely distinguish liver injury, haemolysis and overload. | Requires stronger haemolysis markers such as LDH, haptoglobin, reticulocytes, blood film where available; AST/ALT/bilirubin/GGT; TSAT contradiction. | Medical Review |
| TSAT calculated mode | Calculated TSAT | DEFER_CORE_ENGINE_POLICY | Formula is medically established, but activation use depends on governed formula, unit normalisation and provenance. | Serum iron and TIBC from same sample; compatible units; provenance label `calculated`; direct lab TSAT preferred where present. | Core Engine |
| Homocysteine | High homocysteine / B-vitamin-related methylation impairment | ACTIVATE_WITH_STRICT_GATES | Medically plausible with B12/folate support; unsafe as broad “methylation” or CVD claim. | Homocysteine high; B12/active B12 and folate present; MCV recommended; MMA recommended where B12 ambiguity exists; renal contradiction gate. | Medical Review then Knowledge Bus |
| Homocysteine | High homocysteine / renal clearance reduction | ACTIVATE_WITH_STRICT_GATES | Renal impairment can raise homocysteine; safe only as context, not renal diagnosis. | Homocysteine high; creatinine/eGFR present and abnormal by lab/risk frame; B12/folate contradiction handling; thyroid optional. | Medical Review then Knowledge Bus |
| Leukocyte PSI | WBC high / reactive leukocytosis | DEFER_CORE_ENGINE_POLICY | Medically plausible with differential and CRP, but SSOT identity and system-map blockers remain. | Canonical WBC identity; absolute neutrophils; CRP; symptoms/infection/steroid/smoking/stress context; red-flag suppression. | Core Engine + Medical Review |
| Leukocyte PSI | Lymphocyte low / stress or immunosuppression | DEFER_CORE_ENGINE_POLICY | Medically plausible but non-specific; SSOT identity blocker and context requirements remain. | Canonical lymphocyte absolute count; WBC total; neutrophils; medication/steroid/immunosuppression/infection context; repeat-test wording. | Core Engine + Medical Review |
| Leukocyte PSI | Neutrophil percentage high | DEFER_MEDICAL_REVIEW | Percentage alone can be misleading; absolute neutrophil count is mandatory. | Absolute neutrophils required; WBC total; lymphocyte count; CRP/infection context; pregnancy/steroid/stress modifiers. | Medical Review |
| Thyroid antibodies | TPOAb high / autoimmune hypothyroid pattern | ACTIVATE_WITH_STRICT_GATES | NICE supports TPOAb use when TSH is above range; safe as autoimmune thyroid context when thyroid biochemistry supports it. | TPOAb high; TSH present and above lab range; FT4 present; thyroid medication/pregnancy context; no diagnosis wording. | Knowledge Bus package/PSI scoping |
| Thyroid antibodies | TPOAb high / euthyroid autoimmune risk | DEFER_POST_LAUNCH | Medically defensible but low immediate actionability; risk of anxiety and overdiagnosis. | TPOAb high; TSH and FT4 not outside lab range; no current disease wording; longitudinal monitoring frame only. | Product/Medical Review later |
| Thyroid antibodies | TgAb high / autoimmune hypothyroid pattern | DEFER_POST_LAUNCH | TgAb can support thyroid autoimmunity but is less central than TPOAb; source extraction incomplete. | TgAb high; TPOAb/TSH/FT4 context; no diagnosis wording. | Medical Review + package scoping |
| Thyroid antibodies | TgAb high / euthyroid autoimmune risk | DEFER_POST_LAUNCH | Plausible as autoimmune context but not launch-critical and less actionable. | TgAb high; TSH/FT4/TPOAb context; no diagnosis wording. | Medical Review later |

---

## Detailed review

## Section A — FT3-low activation control

### Medical rationale

Low FT3 is medically coherent as a biochemical direction, but it is not a safe standalone thyroid-disease signal. Low FT3 may occur in non-thyroidal illness syndrome, acute or chronic systemic illness, recovery from illness, calorie restriction, low energy availability, severe stress, liver disease and medication effects. It can also appear in broader hypothyroid physiology, but interpretation requires TSH and FT4.

NICE thyroid guidance does not support interpreting FT3 in isolation for routine hypothyroidism assessment. Endotext describes low T3 as characteristic of non-thyroidal illness, especially in systemic illness contexts.

### Evidence summary

| Source | Year | Relevance | Strength | Limitation |
|---|---:|---|---|---|
| NICE NG145, Thyroid disease: assessment and management | 2019, updated | UK thyroid testing and assessment framework | High | Does not provide consumer-app runtime logic |
| Endotext, Non-Thyroidal Illness Syndrome | Updated clinical reference | Low T3 in systemic illness and non-thyroidal illness | High | Specialist reference, not screening guidance |
| NICE exceptional surveillance on biotin interference | 2023 | Supports assay-interference caveat | Moderate | Focused on biotin, not all assay interferences |

### Activation logic

Low FT3 may be activated only as a contextual endocrine/metabolic stress signal, not as a thyroid-disease signal.

### Required companion markers

- REQUIRED: TSH
- REQUIRED: FT4
- STRONGLY RECOMMENDED: CRP or declared acute inflammatory illness
- OPTIONAL: albumin/protein status, liver markers, renal markers, nutritional markers

### Contradiction logic

- TSH high + FT4 low shifts interpretation toward possible primary hypothyroid physiology rather than low-T3 syndrome.
- TSH suppressed + FT4 high or FT3 high pattern belongs to thyrotoxicosis logic, not low FT3.
- Normal TSH/FT4 with low FT3 and illness/energy restriction context supports a low-T3 / non-thyroidal frame.
- Pregnancy/postpartum requires suppression unless pregnancy-specific logic exists.

### Red-line exclusions

- Missing TSH or FT4.
- Missing thyroid medication status.
- Missing illness/recovery and energy-availability context.
- Pregnancy/postpartum without specialist logic.
- Known thyroid medication use without medication-specific interpretation path.
- Suspected biotin interference or discordant thyroid panel.

### Safe user-facing wording constraints

HealthIQ may say:

- “This pattern may be consistent with reduced peripheral T3 availability, which can sometimes be seen during illness, recovery, calorie restriction or low energy availability.”
- “This is not diagnostic of thyroid disease on its own and should be interpreted with TSH, FT4, recent illness, medication and nutrition context.”

HealthIQ must not say:

- “You have low T3 syndrome.”
- “You have hypothyroidism.”
- “Your thyroid is underactive.”
- “You need thyroid treatment.”

### Recommended HealthIQ AI runtime status

ACTIVATE_WITH_STRICT_GATES.

---

## Section B — Iron Batch C PSI / iron-pattern frame authority

### Cohort-level medical rationale

Serum iron is biologically variable and should not be interpreted alone. Iron patterns require ferritin, transferrin saturation, TIBC/transferrin, FBC indices and inflammation context. Ferritin is the most useful marker for iron deficiency in many settings, but it is an acute-phase reactant and can be raised by inflammation, liver disease, malignancy, CKD and alcohol use. TSAT is central to both iron deficiency and iron overload framing.

The medical problem is not that the proposed frames are implausible. The problem is that the same serum iron direction can sit within competing frames: absolute deficiency, functional restriction, liver injury, haemolysis, supplementation, recent infusion or iron overload.

### Evidence summary

| Source | Year | Relevance | Strength | Limitation |
|---|---:|---|---|---|
| British Society of Gastroenterology guideline for iron deficiency anaemia | 2021 | Ferritin/TSAT and iron-deficiency investigation | High | Adult IDA-focused, not consumer-screening logic |
| EASL haemochromatosis guideline | 2022 | Iron overload characterised by elevated TSAT and progressive iron loading | High | Haemochromatosis-specific |
| NHS / RLBUHT Iron Studies guidance | Current lab guidance | TSAT calculated from serum iron/TIBC; ferritin better indicator of deficiency | Moderate to high | Local laboratory guidance |
| NHS ferritin interpretation guide | 2025 | Ferritin raised by inflammation, CKD, liver disease, alcohol etc.; TSAT can help avoid missed deficiency | Moderate | Local guideline, not national guideline |

### Candidate-level table

| Candidate / pattern | Medically valid? | Activation allowed? | Required companions | Contradictions | Red-line exclusions | Final decision |
|---|---|---|---|---|---|---|
| Iron low / absolute iron deficiency | Yes | Yes, strict gates only | Ferritin low; TSAT low; FBC indices; CRP/inflammation context | CRP high with non-low ferritin; normal/high ferritin without inflammation explanation | Recent iron infusion, supplement loading, acute inflammation without ferritin/CRP context | ACTIVATE_WITH_STRICT_GATES |
| Iron low / functional iron restriction-inflammation | Yes | Yes, strict gates only | CRP/inflammation high; ferritin normal/high; TSAT low; FBC indices | Ferritin low argues for absolute deficiency; CRP normal weakens inflammatory frame | Missing ferritin/TSAT/CRP; recent infusion/supplement confounding | ACTIVATE_WITH_STRICT_GATES |
| Iron high / iron overload context | Yes | Yes, strict gates only | TSAT high; ferritin high/supportive; liver markers | ALT/bilirubin/haemolysis markers suggest release state; ferritin normal weakens overload frame | Recent iron ingestion/infusion; haemolysis; acute liver injury without follow-up frame | ACTIVATE_WITH_STRICT_GATES |
| Iron high / hepatocellular or haemolytic release | Plausible | Not yet | ALT/AST, bilirubin, GGT; LDH/haptoglobin/reticulocytes if haemolysis frame; TSAT/ferritin | Persistently high TSAT and ferritin supports overload instead | Missing haemolysis markers; isolated ALT/bilirubin only; acute symptoms/red flags | DEFER_MEDICAL_REVIEW |

### Safe wording constraints

Allowed:

- “This pattern may be consistent with reduced circulating iron availability when interpreted with ferritin, transferrin saturation and inflammation markers.”
- “Serum iron should not be interpreted on its own because it varies and can be affected by inflammation, supplements, liver injury and recent iron exposure.”

Prohibited:

- “You have iron deficiency.”
- “You have iron overload.”
- “You have haemochromatosis.”
- “You have anaemia of chronic disease.”
- “Your liver is releasing iron.”

### Recommended HealthIQ AI runtime status

- Low iron absolute deficiency: ACTIVATE_WITH_STRICT_GATES.
- Low iron functional restriction/inflammation: ACTIVATE_WITH_STRICT_GATES.
- High iron overload context: ACTIVATE_WITH_STRICT_GATES.
- High iron hepatocellular/haemolytic release: DEFER_MEDICAL_REVIEW.

---

## Section C — TSAT calculated mode: medical boundary only

### Medical rationale

Calculated TSAT is medically meaningful if serum iron and TIBC are available from the same report/sample and units are correctly normalised. The common formula is:

```text
TSAT (%) = serum iron / TIBC × 100
```

However, HealthIQ should distinguish a directly reported laboratory TSAT from a HealthIQ-calculated TSAT. Direct lab TSAT should remain preferred where present. Calculated TSAT can support interpretation, but should not silently behave as if it were a directly reported lab value unless Core Engine governance explicitly approves derived-metric equivalence.

### Evidence summary

| Source | Year | Relevance | Strength | Limitation |
|---|---:|---|---|---|
| NHS / RLBUHT Iron Studies | Current | Gives TSAT formula and interpretation boundary | High for formula | Local lab document |
| Synnovis transferrin saturation test page | 2023 | States lab equation for TSAT | Moderate | Local lab guidance |
| StatPearls Iron-Binding Capacity | 2024 | States formula and iron-binding physiology | Moderate | Secondary reference |
| Lab Tests Online UK iron tests | Current | Iron tests interpreted together | Moderate | Public laboratory information |

### Boundary decision

Calculated TSAT should be allowed to support or qualify signals only until Core Engine formally governs:

- formula;
- accepted input markers;
- unit normalisation;
- same-sample/report requirements;
- provenance label;
- precedence when direct TSAT is present;
- rounding/precision;
- fail-closed behaviour.

### Required input markers

- Serum iron.
- TIBC or iron-binding capacity.
- Same compatible unit family after normalisation.
- Same report/sample context preferred.

### Unit-normalisation risks

- Serum iron and TIBC may be reported in different unit families.
- Transferrin-derived approximations are not identical to direct TIBC unless a governed conversion exists.
- Direct TSAT and calculated TSAT may differ due to lab method/rounding.

### Recommended HealthIQ AI runtime status

DEFER_CORE_ENGINE_POLICY.

Medical boundary: calculated TSAT is clinically meaningful, but should not independently activate launch signals until governed as a derived metric. It may be displayed or used as supporting context only with provenance.

---

## Section D — Homocysteine PSI cohort

### Cohort-level medical rationale

High homocysteine is suitable for cautious educational interpretation when framed narrowly. It can support B-vitamin/one-carbon metabolism context and renal-clearance context. It should not be used as a broad cardiovascular-risk signal in HealthIQ launch logic because routine homocysteine testing for cardiovascular risk remains controversial, and lowering homocysteine has not consistently improved major cardiovascular outcomes in trials.

### Evidence summary

| Source | Year | Relevance | Strength | Limitation |
|---|---:|---|---|---|
| NICE NG239 Vitamin B12 deficiency | 2024 | B12 deficiency diagnosis/management and further testing context | High | Does not position homocysteine as broad screening test |
| NICE CKS B12/folate anaemia | Current | Homocysteine/MMA as further testing in selected cases | High | Clinical pathway, not consumer platform |
| ADLM Optimal Testing Guide: Homocysteine | 2023 | Homocysteine not recommended for routine population CVD screening | High | US laboratory medicine context |
| NEJM HOPE-2 homocysteine lowering trial | 2006 | B vitamins lowered homocysteine but did not reduce major CV events | High | Older but landmark outcome trial |
| CKD/B12 review literature | 2024 | CKD/ESKD associated with elevated homocysteine | Moderate | Specialist populations |

### Candidate 1 — Homocysteine high / B-vitamin-related methylation impairment

#### Activation logic

Allowed only when high homocysteine is paired with B12/active B12 and/or folate support.

#### Required companion markers

- REQUIRED: B12 or active B12.
- REQUIRED: folate.
- STRONGLY RECOMMENDED: MCV.
- STRONGLY RECOMMENDED: MMA where B12 deficiency ambiguity exists.
- REQUIRED CONTRADICTION: creatinine/eGFR to check renal contribution where available.

#### Contradiction logic

- Normal B12 and normal folate weaken B-vitamin frame.
- Reduced eGFR/high creatinine shifts toward renal-clearance frame.
- Normal MCV does not exclude B-vitamin-related elevation but lowers haematological confidence.
- Supplement use can obscure interpretation.

#### Red-line exclusions

- Missing B12/folate.
- Missing renal-function context if renal frame might explain elevation.
- Use of homocysteine as a cardiovascular-risk diagnosis.
- Treatment or supplement advice.

#### Safe wording

- “A high homocysteine result can sometimes be seen when folate or vitamin B12-dependent metabolism is impaired, but it is not diagnostic on its own.”
- “This should be interpreted with B12, folate, red-cell indices and kidney function.”

#### Recommended status

ACTIVATE_WITH_STRICT_GATES.

### Candidate 2 — Homocysteine high / renal clearance reduction

#### Activation logic

Allowed only when high homocysteine is accompanied by renal-function evidence.

#### Required companion markers

- REQUIRED: creatinine and/or eGFR.
- STRONGLY RECOMMENDED: B12/active B12 and folate.
- OPTIONAL: thyroid markers, liver markers, inflammatory markers.

#### Contradiction logic

- Normal creatinine/eGFR weakens renal frame.
- Low B12 or folate shifts toward B-vitamin frame.
- Thyroid dysfunction may be a modifier but should not be primary without thyroid-panel logic.

#### Red-line exclusions

- Missing renal markers.
- Cardiovascular-risk wording as the main frame.
- “Methylation impairment” claims without B-vitamin evidence.

#### Safe wording

- “A high homocysteine result can sometimes be seen when kidney clearance or metabolism is reduced, but it is not a kidney-disease diagnosis.”
- “Interpretation should consider kidney markers and B-vitamin markers together.”

#### Recommended status

ACTIVATE_WITH_STRICT_GATES.

---

## Section E — Leukocyte PSI cohort

### Cohort-level medical rationale

Leukocyte patterns are medically meaningful but highly non-specific. High WBC, low lymphocytes and neutrophil-predominant shifts can be seen with infection, inflammation, medication effects, corticosteroids, smoking, stress, pregnancy, exercise and haematological disease. They are suitable only as cautious inflammatory/immune context signals, not disease diagnoses.

The current cohort also has non-medical blockers: WBC and lymphocyte canonical marker identity issues and system-mapping review. These must be cleared before activation, regardless of medical plausibility.

### Evidence summary

| Source | Year | Relevance | Strength | Limitation |
|---|---:|---|---|---|
| AAFP Evaluation of Patients with Leukocytosis | 2015 | Reactive leukocytosis, stressors, differential and repeat/smear evaluation | Moderate-high | US primary care review, older but widely cited |
| StatPearls Leukocytosis | 2024 | Leukocytosis differential by WBC subtype | Moderate | Secondary reference |
| Merck Manual Professional, Lymphocytopenia | 2025/2026 update | Lymphopenia transient with infection, stress and corticosteroids | Moderate-high | Clinical reference, not UK guideline |
| NHS low WBC page | Current public NHS | Low WBC can increase infection risk | Moderate | Public-level source |

### Candidate 1 — WBC high / reactive leukocytosis

#### Medical validity

Medically plausible, but not as a standalone signal.

#### Activation logic

Would be acceptable only after Core Engine identity resolution and with differential-count support.

#### Required companions

- REQUIRED: canonical WBC total.
- REQUIRED: absolute neutrophils and/or differential.
- STRONGLY RECOMMENDED: CRP.
- STRONGLY RECOMMENDED: platelets and haemoglobin for broader FBC context.
- OPTIONAL: liver markers, medication/steroid context, infection/symptom context.

#### Contradiction logic

- Lymphocyte-predominant pattern redirects away from neutrophil-reactive frame.
- Normal CRP weakens inflammation frame but does not exclude stress/steroid/reactive causes.
- Very high WBC, immature cells, cytopenias or red flags should suppress routine wording.

#### Red-line exclusions

- WBC not resolved to canonical SSOT ID.
- No differential count.
- Red flags: very high WBC, blasts/immature granulocytes if reported, unexplained bruising, weight loss, fever, severe infection symptoms.
- Pregnancy without pregnancy-specific interpretation.

#### Recommended status

DEFER_CORE_ENGINE_POLICY, with future ACTIVATE_WITH_STRICT_GATES after SSOT/system-map clearance.

### Candidate 2 — Lymphocyte low / stress or immunosuppression

#### Medical validity

Medically plausible but highly non-specific.

#### Activation logic

Should not activate until absolute lymphocyte identity is resolved and medication/infection/steroid/immunosuppression context is captured.

#### Required companions

- REQUIRED: canonical absolute lymphocyte count, not percentage alone.
- REQUIRED: WBC total.
- STRONGLY RECOMMENDED: neutrophils.
- STRONGLY RECOMMENDED: CRP/infection context.
- OPTIONAL: medication/steroid context, albumin/nutritional context.

#### Contradiction logic

- Low WBC total shifts toward broader leukopenia/marrow/viral/medication context.
- High neutrophils with low lymphocytes supports stress/steroid/inflammatory redistribution.
- Normal WBC total weakens broad immune-suppression wording.

#### Red-line exclusions

- Lymphocyte marker not resolved to canonical SSOT ID.
- Missing WBC total.
- Missing medication/steroid/immunosuppression context.
- Severe/recurrent infection symptoms or very low lymphocyte count requiring clinician-review wording.

#### Recommended status

DEFER_CORE_ENGINE_POLICY, with future ACTIVATE_WITH_STRICT_GATES only after SSOT and context gates.

### Candidate 3 — Neutrophil percentage high / neutrophil-predominant leukocyte shift

#### Medical validity

Medically plausible as a differential-count pattern, but percentage alone is insufficient. Absolute neutrophil count is essential because relative percentages can shift due to changes in other leukocyte fractions.

#### Activation logic

Not cleared as currently framed. It may become a supporting modifier if absolute neutrophils and WBC total are present.

#### Required companions

- REQUIRED: absolute neutrophil count.
- REQUIRED: WBC total.
- STRONGLY RECOMMENDED: lymphocyte absolute count.
- STRONGLY RECOMMENDED: CRP or infection/inflammation context.

#### Contradiction logic

- High percentage with normal absolute neutrophils should not be framed as neutrophilia.
- Lymphopenia can raise neutrophil percentage without true neutrophil excess.
- Steroid/stress/pregnancy context can explain pattern.

#### Recommended status

DEFER_MEDICAL_REVIEW.

---

## Section F — kb59 thyroid antibody packages

### Group-level medical rationale

Thyroid antibodies are medically suitable for cautious HealthIQ interpretation, but only as context. They should not be used to diagnose autoimmune thyroid disease in isolation, and they should not be treated as proof of current thyroid dysfunction.

The strongest launch candidate is TPOAb high in the presence of thyroid biochemistry consistent with primary hypothyroid physiology. TPOAb high with euthyroid biochemistry is a future-risk/context signal, not a current-disease signal. TgAb can support autoimmune thyroid context but is less central than TPOAb in routine hypothyroidism assessment and should be deferred until package scoping is complete.

### Evidence summary

| Source | Year | Relevance | Strength | Limitation |
|---|---:|---|---|---|
| NICE NG145 | 2019, updated | Consider TPOAbs in adults with TSH above reference range; do not repeat TPOAbs | High | Does not define consumer-app wording |
| NICE CKS Hypothyroidism | Current | Positive TPOAb can predict progression to overt hypothyroidism | High | Primary care framing |
| British Thyroid Foundation thyroid antibodies explainer | 2024 | TPOAb helps establish autoimmune cause when TSH high | Moderate | Patient-facing charity source, not guideline |
| RACGP hypothyroidism review | 2012 | TPOAb positivity occurs in general population and is not treatment indication if thyroid function normal | Moderate | Non-UK but clinically useful |

### Candidate 1 — TPOAb high / autoimmune hypothyroid pattern

#### Activation logic

Cleared only when TPOAb high is accompanied by TSH above lab range and FT4 context. The frame must be “autoimmune thyroid context supporting the pattern”, not diagnosis.

#### Required companions

- REQUIRED: TSH.
- REQUIRED: FT4.
- OPTIONAL: FT3.
- STRONGLY RECOMMENDED: TgAb if available.

#### Contradiction logic

- TPOAb high with TSH/FT4 not outside lab range shifts to euthyroid autoimmune-risk context.
- FT4 high or suppressed TSH redirects to hyperthyroid/destructive/stimulatory frames, not autoimmune hypothyroid frame.

#### Safe wording

- “Raised TPO antibodies can support an autoimmune thyroid context when thyroid function markers also point towards reduced thyroid output.”
- “This is not diagnostic on its own and should be interpreted with TSH, FT4, symptoms, medication and pregnancy context.”

#### Recommended status

ACTIVATE_WITH_STRICT_GATES.

### Candidate 2 — TPOAb high / euthyroid autoimmune risk

#### Medical rationale

Medically defensible as future-risk context, but low immediate actionability and high anxiety risk. It is not a launch-priority signal.

#### Recommended status

DEFER_POST_LAUNCH.

### Candidate 3 — TgAb high / autoimmune hypothyroid pattern

#### Medical rationale

TgAb can support autoimmune thyroid context, but it is less central than TPOAb in routine hypothyroidism assessment. The source context pack also notes incomplete extraction for some TgAb signal libraries.

#### Recommended status

DEFER_POST_LAUNCH.

### Candidate 4 — TgAb high / euthyroid autoimmune risk

#### Medical rationale

Plausible but not sufficiently launch-critical and less actionable.

#### Recommended status

DEFER_POST_LAUNCH.

---

## Activation authority outputs

```yaml
cleared_candidates:
  - candidate_id: ft3_low_low_t3_context
    signal_direction: low
    activation_status: ACTIVATE_WITH_STRICT_GATES
    required_primary_marker: free_t3
    required_companion_markers:
      - tsh
      - free_t4
    required_contradiction_markers:
      - tsh
      - free_t4
      - pregnancy_postpartum_context
      - thyroid_medication_context
    required_context_fields:
      - thyroid_medication_status
      - illness_or_recovery_status
      - calorie_restriction_status
      - fasting_or_low_energy_availability_status
      - pregnancy_or_postpartum_status
      - biotin_or_assay_interference_disclosure
    red_line_exclusions:
      - missing_tsh
      - missing_free_t4
      - missing_required_context
      - pregnancy_without_specific_logic
      - thyroid_medication_without_specific_logic
    safe_runtime_frame: reduced_peripheral_t3_availability_context
    unsafe_runtime_frame: hypothyroidism_diagnosis
    medical_review_status: cleared_with_strict_gates
    implementation_owner: Knowledge Bus / Core Engine

  - candidate_id: iron_low_absolute_iron_deficiency
    signal_direction: low
    activation_status: ACTIVATE_WITH_STRICT_GATES
    required_primary_marker: serum_iron
    required_companion_markers:
      - ferritin
      - transferrin_saturation
      - crp_or_inflammation_context
      - fbc_indices
    required_contradiction_markers:
      - crp
      - ferritin
      - transferrin_saturation
    required_context_fields:
      - iron_supplement_use
      - recent_iron_infusion
      - menstruation_or_recent_blood_loss_if_available
      - inflammation_or_infection_context
    red_line_exclusions:
      - isolated_low_serum_iron_only
      - missing_ferritin
      - missing_tsat
      - acute_inflammation_without_caveat
    safe_runtime_frame: iron_deficiency_pattern_context
    unsafe_runtime_frame: iron_deficiency_diagnosis
    medical_review_status: cleared_with_strict_gates
    implementation_owner: Knowledge Bus

  - candidate_id: iron_low_functional_iron_restriction_inflammation
    signal_direction: low
    activation_status: ACTIVATE_WITH_STRICT_GATES
    required_primary_marker: serum_iron
    required_companion_markers:
      - transferrin_saturation
      - ferritin
      - crp_or_declared_inflammation
    required_contradiction_markers:
      - ferritin_low
      - crp_normal
    required_context_fields:
      - inflammation_or_infection_context
      - iron_supplement_or_infusion_context
    red_line_exclusions:
      - missing_ferritin
      - missing_tsat
      - missing_inflammation_context
    safe_runtime_frame: inflammatory_iron_restriction_context
    unsafe_runtime_frame: anaemia_of_chronic_disease_diagnosis
    medical_review_status: cleared_with_strict_gates
    implementation_owner: Knowledge Bus

  - candidate_id: iron_high_iron_overload_context
    signal_direction: high
    activation_status: ACTIVATE_WITH_STRICT_GATES
    required_primary_marker: serum_iron
    required_companion_markers:
      - transferrin_saturation
      - ferritin
      - liver_markers
    required_contradiction_markers:
      - alt
      - ast
      - bilirubin
      - haemolysis_markers_if_available
    required_context_fields:
      - recent_iron_supplement_or_infusion
      - known_haemochromatosis_or_iron_overload
      - liver_disease_context
    red_line_exclusions:
      - isolated_high_serum_iron_only
      - recent_iron_exposure_without_caveat
      - missing_tsat
    safe_runtime_frame: iron_overload_pattern_context
    unsafe_runtime_frame: haemochromatosis_diagnosis
    medical_review_status: cleared_with_strict_gates
    implementation_owner: Knowledge Bus

  - candidate_id: homocysteine_high_b_vitamin_related_methylation_impairment
    signal_direction: high
    activation_status: ACTIVATE_WITH_STRICT_GATES
    required_primary_marker: homocysteine
    required_companion_markers:
      - b12_or_active_b12
      - folate
      - renal_function
    required_contradiction_markers:
      - creatinine_or_egfr
      - normal_b12_and_folate
    required_context_fields:
      - b_vitamin_supplement_use
      - nitrous_oxide_exposure_if_available
      - renal_disease_context
    red_line_exclusions:
      - missing_b12_or_folate
      - cardiovascular_risk_claim_as_primary_frame
    safe_runtime_frame: b_vitamin_one_carbon_metabolism_context
    unsafe_runtime_frame: cardiovascular_event_risk_prediction
    medical_review_status: cleared_with_strict_gates
    implementation_owner: Knowledge Bus

  - candidate_id: homocysteine_high_renal_clearance_reduction
    signal_direction: high
    activation_status: ACTIVATE_WITH_STRICT_GATES
    required_primary_marker: homocysteine
    required_companion_markers:
      - creatinine_or_egfr
      - b12_or_active_b12
      - folate
    required_contradiction_markers:
      - normal_creatinine_or_egfr
      - low_b12
      - low_folate
    required_context_fields:
      - known_renal_condition_if_available
      - b_vitamin_supplement_use
    red_line_exclusions:
      - missing_renal_markers
      - renal_disease_diagnosis_wording
    safe_runtime_frame: renal_clearance_context
    unsafe_runtime_frame: kidney_disease_diagnosis
    medical_review_status: cleared_with_strict_gates
    implementation_owner: Knowledge Bus

  - candidate_id: tpo_ab_high_autoimmune_hypothyroid_pattern
    signal_direction: high
    activation_status: ACTIVATE_WITH_STRICT_GATES
    required_primary_marker: tpo_ab
    required_companion_markers:
      - tsh
      - free_t4
    required_contradiction_markers:
      - tsh_not_above_range
      - free_t4_not_low
      - suppressed_tsh_or_high_ft4_pattern
    required_context_fields:
      - thyroid_medication_status
      - pregnancy_postpartum_status
    red_line_exclusions:
      - missing_tsh
      - missing_free_t4
      - euthyroid_biochemistry_for_hypothyroid_frame
    safe_runtime_frame: autoimmune_thyroid_context_supporting_hypothyroid_biochemistry
    unsafe_runtime_frame: hashimotos_diagnosis
    medical_review_status: cleared_with_strict_gates
    implementation_owner: Knowledge Bus
```

---

## Deferred / rejected outputs

```yaml
deferred_candidates:
  - candidate_id: iron_high_hepatocellular_or_hemolytic_release
    deferred_status: DEFER_MEDICAL_REVIEW
    reason: Current companion marker set is insufficient to distinguish liver injury, haemolysis and iron overload safely.
    what_evidence_is_missing:
      - haemolysis marker requirements
      - stronger liver-injury pattern rules
      - contradiction handling against iron overload frame
    who_must_clear: Medical Review
    recommended_future_review: hepatocellular_haemolytic_iron_release_frame_review

  - candidate_id: transferrin_saturation_calculated_mode
    deferred_status: DEFER_CORE_ENGINE_POLICY
    reason: Medically meaningful but requires governed derived-metric formula, unit normalisation and provenance labelling.
    what_evidence_is_missing:
      - no medical evidence missing for formula
      - Core Engine SSOT formula governance missing
      - provenance policy missing
    who_must_clear: Core Engine
    recommended_future_review: P1-TRANSFERRIN-SAT-CALC-POLICY-1

  - candidate_id: wbc_high_reactive_leukocytosis
    deferred_status: DEFER_CORE_ENGINE_POLICY
    reason: Medically plausible but WBC SSOT identity and system-mapping blockers remain.
    what_evidence_is_missing:
      - canonical WBC identity resolution
      - differential-count gate mapping
      - symptom/context safety gates
    who_must_clear: Core Engine plus Medical Review
    recommended_future_review: leukocyte_identity_and_activation_gate_review

  - candidate_id: lym_low_lymphopenia_stress_or_immunosuppression
    deferred_status: DEFER_CORE_ENGINE_POLICY
    reason: Medically plausible but lymphocyte SSOT identity blocker and context requirements remain.
    what_evidence_is_missing:
      - canonical absolute lymphocyte identity
      - medication/steroid/immunosuppression context gates
      - repeat-test wording policy
    who_must_clear: Core Engine plus Medical Review
    recommended_future_review: lymphocyte_identity_and_context_gate_review

  - candidate_id: neutrophil_pct_high_neutrophil_predominant_shift
    deferred_status: DEFER_MEDICAL_REVIEW
    reason: Percentage-only neutrophil signal is unsafe without absolute neutrophil count.
    what_evidence_is_missing:
      - absolute_neutrophil_requirement
      - revised_companion_marker_design
      - removal_or_downgrading_of_weak_correlates
    who_must_clear: Medical Review
    recommended_future_review: neutrophil_absolute_vs_percentage_policy

  - candidate_id: tpo_ab_high_euthyroid_autoimmune_risk
    deferred_status: DEFER_POST_LAUNCH
    reason: Medically defensible but low immediate actionability and risk of consumer anxiety.
    what_evidence_is_missing:
      - product_level_decision_on_risk_context_surfacing
      - longitudinal_monitoring_wording
      - package_psi_activation_plan
    who_must_clear: Product plus Medical Review
    recommended_future_review: thyroid_antibody_euthyroid_context_review

  - candidate_id: tgab_high_autoimmune_hypothyroid_pattern
    deferred_status: DEFER_POST_LAUNCH
    reason: TgAb is less central than TPOAb and source extraction/package scoping is incomplete.
    what_evidence_is_missing:
      - full_signal_library_review
      - package_scoping
      - tpoab_tsh_ft4_companion_policy
    who_must_clear: Medical Review plus Knowledge Bus
    recommended_future_review: tgab_activation_scoping_review

  - candidate_id: tgab_high_euthyroid_autoimmune_risk
    deferred_status: DEFER_POST_LAUNCH
    reason: Plausible as autoimmune context but not launch-critical and less actionable.
    what_evidence_is_missing:
      - full_source_review
      - safe_longitudinal_context_wording
      - package_psi_plan
    who_must_clear: Medical Review plus Product
    recommended_future_review: tgab_euthyroid_context_review
```

---

## Cross-validation checklist for Pass 2 Medical LLM

The second Medical Research LLM should specifically validate the following.

### 1. Highest-risk medical decisions

- FT3 low activation despite high context dependence.
- Iron high overload frame activation despite serum iron variability.
- Homocysteine activation without encouraging cardiovascular-risk overclaims.
- TPOAb activation without implying Hashimoto’s diagnosis.
- Leukocyte deferral despite plausible medical frames.

### 2. Weak or conflicting evidence

- Homocysteine cardiovascular relevance remains controversial.
- Functional iron deficiency terminology varies across disease states.
- TgAb utility is less central than TPOAb in routine hypothyroid interpretation.
- Neutrophil percentage interpretation is weak without absolute counts.
- Euthyroid antibody positivity has prognostic value but uncertain consumer actionability.

### 3. Activation decisions dependent on companion markers

- FT3 low requires TSH and FT4.
- Iron low requires ferritin and TSAT.
- Iron functional restriction requires CRP/inflammation context and ferritin.
- Iron overload requires TSAT and ferritin.
- Homocysteine B-vitamin frame requires B12/active B12 and folate.
- Homocysteine renal frame requires renal markers.
- TPOAb hypothyroid frame requires TSH and FT4.

### 4. Diagnostic-overreach risks

- “Hypothyroidism” from FT3 low.
- “Iron deficiency” from low serum iron alone.
- “Haemochromatosis” from high serum iron or TSAT alone.
- “B-vitamin deficiency” from high homocysteine alone.
- “Infection” from high WBC or neutrophil shift.
- “Hashimoto’s” from TPOAb positivity alone.

### 5. Core Engine policy blockers

- TSAT calculated mode.
- WBC canonical identity.
- Lymphocyte canonical identity.
- Leukocyte system mapping.
- Derived metric provenance and direct-vs-calculated TSAT precedence.

### 6. Sources to independently verify

- NICE NG145 thyroid antibody and thyroid testing recommendations.
- Endotext non-thyroidal illness syndrome.
- BSG 2021 iron deficiency anaemia guideline.
- EASL 2022 haemochromatosis guideline.
- NHS/RLBUHT and Synnovis TSAT formula sources.
- NICE NG239 and NICE CKS B12/folate guidance.
- ADLM homocysteine optimal testing guidance.
- AAFP/StatPearls/Merck leukocytosis and lymphopenia sources.

### 7. Wording that needs to be made safer

- “Autoimmune hypothyroid pattern” should render as “autoimmune thyroid context supporting hypothyroid biochemistry.”
- “Functional iron restriction” should explain inflammation-mediated reduced iron availability, not diagnose anaemia of inflammation.
- “Methylation impairment” should not appear as a strong user-facing disease-like label.
- “Reactive leukocytosis” should not imply infection unless symptoms/CRP support it.
- “Iron overload context” must not imply haemochromatosis.

---

## References

1. NICE NG145. Thyroid disease: assessment and management. https://www.nice.org.uk/guidance/ng145
2. Endotext. The Non-Thyroidal Illness Syndrome. https://www.endotext.org/wp-content/uploads/pdfs/the-non-thyroidal-illness-syndrome.pdf
3. NICE exceptional surveillance of thyroid disease guideline: biotin interference. https://www.nice.org.uk/guidance/ng145/resources/2023-exceptional-surveillance-of-thyroid-disease-assessment-and-management-nice-guideline-ng145-pdf-17094825912517
4. Snook J, et al. British Society of Gastroenterology guidelines for the management of iron deficiency anaemia in adults. Gut. 2021. https://gut.bmj.com/content/70/11/2030
5. EASL Clinical Practice Guidelines on haemochromatosis. Journal of Hepatology. 2022. https://pubmed.ncbi.nlm.nih.gov/35662478/
6. RLBUHT Pathology. Iron Studies. https://pathlabs.rlbuht.nhs.uk/iron_studies.pdf
7. Synnovis. Transferrin Saturation. https://www.synnovis.co.uk/our-tests/transferrin-saturation
8. NHS. Total iron-binding capacity and transferrin test. https://www.nhs.uk/tests-and-treatments/tibc-test/
9. Lab Tests Online UK. Iron tests. https://labtestsonline.org.uk/tests/iron-tests
10. NICE NG239. Vitamin B12 deficiency in over 16s: diagnosis and management. https://www.nice.org.uk/guidance/ng239
11. NICE CKS. Anaemia — B12 and folate deficiency. https://cks.nice.org.uk/topics/anaemia-b12-folate-deficiency/
12. ADLM. Homocysteine optimal testing guide. https://myadlm.org/advocacy-and-outreach/optimal-testing-guide-to-lab-test-utilization/g-s/homocysteine
13. Lonn E, et al. Homocysteine lowering with folic acid and B vitamins in vascular disease. NEJM. 2006. https://www.nejm.org/doi/full/10.1056/NEJMoa060900
14. Riley LK, Rupert J. Evaluation of Patients with Leukocytosis. American Family Physician. 2015. https://www.aafp.org/afp/2015/1201/p1004
15. StatPearls. Leukocytosis. https://www.ncbi.nlm.nih.gov/books/NBK560882/
16. Merck Manual Professional. Lymphocytopenia. https://www.merckmanuals.com/professional/hematology-and-oncology/leukopenias/lymphocytopenia
17. NICE CKS. Hypothyroidism assessment. https://cks.nice.org.uk/topics/hypothyroidism/diagnosis/assessment/
18. British Thyroid Foundation. Thyroid antibodies explained. https://www.btf-thyroid.org/thyroid-antibodies-explained
19. RACGP. Hypothyroidism — investigation and management. https://www.racgp.org.au/afp/2012/august/hypothyroidism

