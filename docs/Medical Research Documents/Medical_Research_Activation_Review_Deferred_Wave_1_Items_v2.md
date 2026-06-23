# Medical Research Activation Review — Deferred Wave 1 Items — Revision 2

**Document status:** Revision 2 medical activation-authority review  
**Revision basis:** Pass 1 HealthIQ medical review, Pass 2 Medical Research Activation Pathway Report, and GPT adjudication after additional evidence review  
**Date:** 2026-06-23  
**Scope:** Medical activation safety only. This document does not implement runtime logic, author Knowledge Bus package files, modify activation state, or override Automation Bus / Knowledge Bus governance.

---

## Executive conclusion

This revision updates the original Pass 1 medical activation review after considering the Pass 2 Medical Research Activation Pathway Report and subsequent adjudication. Pass 2 usefully distinguishes between **medical validity**, **runtime activation readiness**, and **non-medical Core Engine blockers**. That distinction does unlock several previously deferred items, but not every Pass 2 recommendation is accepted unchanged.

The revised conclusion is:

- FT3 low can now be treated as **medically cleared for activation with strict gates**, because the original blocker was not permanent rejection but the need for TSH, FT4, illness/recovery, thyroid medication and energy-availability context.
- Iron low absolute deficiency, iron low functional/inflammatory restriction, and iron high overload context remain **cleared with strict gates**.
- Iron high hepatocellular/haemolytic release is **not cleared as a full standalone runtime signal**. It is medically plausible, but should be used as a caveat / suppressor / redirect frame unless stronger liver-injury or haemolysis evidence is available.
- Calculated TSAT remains a **Core Engine formula/provenance governance item**, not a medical blocker.
- Homocysteine high B-vitamin and renal frames are **cleared with strict gates**, but broad cardiovascular-risk and consumer-facing “methylation impairment” claims must remain prohibited.
- WBC high and lymphocyte low are **medically cleared in principle**, but remain blocked by SSOT identity and system-mapping governance before implementation.
- Neutrophil percentage high is **not cleared as a percentage-only primary signal**. It may activate only when absolute neutrophil count is available and confirms the frame; otherwise it may only act as a cautious modifier/caveat.
- TPOAb high with hypothyroid biochemistry is **cleared with strict gates**.
- TPOAb high with euthyroid thyroid function is **medically defensible**, but should be treated as **post-launch / advanced cautious context**, not a launch-core signal.
- TgAb packages remain **deferred / corroborator-only** pending fuller package scoping and source review.

### Items medically cleared for governed implementation planning

1. FT3 low / reduced peripheral T3 availability context — **ACTIVATE_WITH_STRICT_GATES**
2. Iron low / absolute iron deficiency pattern — **ACTIVATE_WITH_STRICT_GATES**
3. Iron low / functional iron restriction-inflammation — **ACTIVATE_WITH_STRICT_GATES**
4. Iron high / iron overload context — **ACTIVATE_WITH_STRICT_GATES**
5. Homocysteine high / B-vitamin-related processing context — **ACTIVATE_WITH_STRICT_GATES**
6. Homocysteine high / renal clearance context — **ACTIVATE_WITH_STRICT_GATES**
7. TPOAb high / autoimmune thyroid context supporting hypothyroid biochemistry — **ACTIVATE_WITH_STRICT_GATES**

### Items medically plausible but not yet implementable because of non-medical blockers

1. WBC high / reactive leukocytosis — **medical cleared, Core Engine SSOT/system-mapping blocked**
2. Lymphocyte low / stress or immunosuppression context — **medical cleared, Core Engine SSOT/system-mapping blocked**
3. Calculated TSAT — **medical formula accepted in principle, Core Engine formula/provenance blocked**

### Items narrowed or deferred after Pass 2 adjudication

1. Iron high / hepatocellular or haemolytic release — **DEFER_MEDICAL_REVIEW as standalone signal; allow as caveat/suppressor frame**
2. Neutrophil percentage high — **ACTIVATE_ONLY_WITH_ANC_CONFIRMATION; otherwise modifier only**
3. TPOAb high / euthyroid autoimmune risk — **DEFER_POST_LAUNCH / advanced cautious context**
4. TgAb high packages — **DEFER_POST_LAUNCH / corroborator-only**

---

## Decision matrix

| Group | Candidate | Decision | Rationale | Required gates | Owner for next step |
| ----- | --------- | -------- | --------- | -------------- | ------------------- |
| FT3-low activation control | FT3 low / reduced peripheral T3 availability context | ACTIVATE_WITH_STRICT_GATES | Pass 2 confirms that the original ADR blocker is satisfied if TSH, FT4, illness/recovery, medication and energy-availability gates are enforced. Safe only as non-diagnostic low-T3 / non-thyroidal context, not hypothyroidism. | FT3 below lab range; TSH present; FT4 present; TSH not elevated with FT4 low for this frame; thyroid medication status; illness/recovery status; calorie restriction/fasting/low-energy context; pregnancy/postpartum route; biotin/interference caveat. | Medical Review + Knowledge Bus activation-control sprint |
| Iron Batch C | Iron low / absolute iron deficiency | ACTIVATE_WITH_STRICT_GATES | Confirmed by Pass 2. Low serum iron alone is weak; low ferritin + low TSAT supports iron-deficiency pattern. | Serum iron low; ferritin low; TSAT low; FBC indices strongly recommended; CRP/inflammation context; iron supplement/infusion context. | Knowledge Bus |
| Iron Batch C | Iron low / functional iron restriction-inflammation | ACTIVATE_WITH_STRICT_GATES | Confirmed by Pass 2. Inflammation-mediated iron sequestration is medically coherent when low iron/TSAT occurs with inflammatory context and non-low ferritin. | Serum iron low; TSAT low; CRP/inflammation high or declared inflammatory illness; ferritin normal/high; contradiction if ferritin low; supplement/infusion context. | Knowledge Bus |
| Iron Batch C | Iron high / iron overload context | ACTIVATE_WITH_STRICT_GATES | Confirmed, with stricter ferritin gate. High serum iron requires TSAT and ferritin support. | Serum iron high; TSAT high; ferritin above lab range; liver markers checked; recent iron ingestion/infusion exclusion; ALT/AST/bilirubin contradiction handling. | Knowledge Bus |
| Iron Batch C | Iron high / hepatocellular or haemolytic release | DEFER_MEDICAL_REVIEW | Pass 2 makes plausible case, but ALT/bilirubin alone are insufficient to safely distinguish liver injury, haemolysis, overload and acute illness. Use as caveat/suppressor where liver/haemolysis contradiction exists, not full standalone frame. | For future activation: ALT/AST/GGT/bilirubin plus haemolysis markers where available; LDH/haptoglobin/reticulocytes/blood film if haemolysis frame; TSAT/ferritin contradiction logic. | Medical Review |
| TSAT calculated mode | Calculated transferrin saturation | DEFER_CORE_ENGINE_POLICY | Medical formula is accepted in principle, but implementation depends on governed derived-metric formula, unit normalisation, same-sample requirement, precedence and provenance. | Serum iron + TIBC from same sample/report; compatible units; provenance label `calculated`; direct lab TSAT preferred; fail-closed if inputs incompatible. | Core Engine |
| Homocysteine | High homocysteine / B-vitamin-related processing context | ACTIVATE_WITH_STRICT_GATES | Confirmed by Pass 2. High homocysteine with B12/active B12 and folate support is medically coherent. Avoid broad cardiovascular and “methylation impairment” language. | Homocysteine high; B12/active B12 present; folate present; renal markers present for contradiction; MCV recommended; supplement context. | Knowledge Bus |
| Homocysteine | High homocysteine / renal clearance context | ACTIVATE_WITH_STRICT_GATES | Confirmed by Pass 2. Renal impairment can elevate homocysteine; safe only as context, not kidney disease diagnosis. | Homocysteine high; creatinine/eGFR present and supportive; B12/folate contradiction handling; thyroid optional. | Knowledge Bus |
| Leukocyte PSI | WBC high / reactive leukocytosis | DEFER_CORE_ENGINE_POLICY | Pass 2 unlocks medical case, but SSOT WBC identity and system-mapping remain binding constraints. | Canonical WBC total; absolute neutrophils/differential if available; CRP optional but useful; medication/steroid/smoking/stress/infection context; critical-high suppression. | Core Engine + Medical Review |
| Leukocyte PSI | Lymphocyte low / stress or immunosuppression | DEFER_CORE_ENGINE_POLICY | Pass 2 unlocks medical case, but lymphocyte and WBC identity blockers remain. | Canonical absolute lymphocyte count; WBC total; neutrophils; medication/steroid/immunosuppression/recent illness context; very-low / persistent pattern escalation. | Core Engine + Medical Review |
| Leukocyte PSI | Neutrophil percentage high | ACTIVATE_WITH_STRICT_GATES only if ANC present; otherwise modifier-only | Pass 2 is right that percentage can be gated, but percentage-only activation remains unsafe. Absolute neutrophil count must confirm true neutrophilia for primary activation. | Neutrophil % high; absolute neutrophils present and high for full activation; WBC total; lymphocyte count; CRP/infection/steroid/stress context; if ANC normal or absent, render only caveat/modifier. | Medical Review + Core Engine |
| Thyroid antibodies | TPOAb high / autoimmune thyroid context supporting hypothyroid biochemistry | ACTIVATE_WITH_STRICT_GATES | Confirmed. TPOAb is useful when TSH is above reference range and FT4 context supports hypothyroid biochemistry. Must avoid disease-label diagnosis. | TPOAb high; TSH present and above lab range; FT4 present; thyroid medication context; pregnancy/postpartum context; no Hashimoto’s diagnosis wording. | Knowledge Bus package/PSI scoping |
| Thyroid antibodies | TPOAb high / euthyroid autoimmune risk | DEFER_POST_LAUNCH | Pass 2 makes medical case, but product-safety/adoption risk remains. Suitable for advanced/post-launch cautious longitudinal context, not launch-core. | TPOAb high; TSH and FT4 within lab range; no current thyroid dysfunction wording; longitudinal monitoring frame only. | Product + Medical Review later |
| Thyroid antibodies | TgAb high / autoimmune hypothyroid pattern | DEFER_POST_LAUNCH | TgAb can support autoimmunity but is less central than TPOAb and package extraction/source review is incomplete. | TgAb high; TPOAb/TSH/FT4 context; no standalone diagnosis; use as corroborator where possible. | Medical Review + Knowledge Bus |
| Thyroid antibodies | TgAb high / euthyroid autoimmune risk | DEFER_POST_LAUNCH | Plausible as autoimmune thyroid context but lower actionability and less launch relevance. | TgAb high; TSH/FT4/TPOAb context; longitudinal/context wording only. | Medical Review later |

---

## Detailed review

## Section A — FT3-low activation control

### Revision 2 decision

**ACTIVATE_WITH_STRICT_GATES**

### Medical rationale

Pass 2 correctly reframes the FT3-low issue. The existing HealthIQ ADR did not permanently reject FT3 low; it deferred the signal until TSH, FT4, illness/recovery and medication context were available. Those are now explicit activation gates.

Low FT3 is medically coherent as a pattern of reduced peripheral T3 availability and is well described in non-thyroidal illness, recovery states, starvation/calorie restriction, low energy availability and systemic stress. It is also relevant in people using thyroid medication, but that requires a separate medication-context frame.

The key safety boundary is that low FT3 must not be interpreted as hypothyroidism by itself. If TSH is high with FT4 low, the FT3-low frame should suppress and the primary hypothyroid-pattern logic should govern. If TSH is normal/low-normal and FT4 is normal, a cautious low-T3 / reduced-conversion context is defensible.

### Evidence summary

| Source | Year | Relevance | Strength | Limitations |
|---|---:|---|---|---|
| NICE NG145, Thyroid disease: assessment and management | 2019, updated | UK thyroid testing framework; TSH/FT4-centred interpretation | High | Does not define consumer runtime gates |
| Endotext, Non-Thyroidal Illness Syndrome | Current clinical reference | Describes low T3 pattern in systemic illness/starvation and non-thyroidal illness | High | Specialist reference, not wellness-platform guidance |
| Endotext, Thyroid hormone assay interpretation | Current clinical reference | Assay limitations and interference | High | Not specific to HealthIQ context |
| NICE exceptional surveillance on biotin interference | 2023 | Supports biotin/interference caveat | Moderate | Focused on one assay interference source |

### Activation logic

Activate only when low FT3 is interpreted as a **contextual reduced peripheral T3 availability pattern**, not thyroid failure.

### Required companion markers

- REQUIRED: TSH
- REQUIRED: FT4
- STRONGLY RECOMMENDED: CRP or declared illness/inflammatory context
- OPTIONAL: albumin/protein status, liver markers, renal markers, nutritional markers

### Contradiction logic

- TSH high + FT4 low: suppress FT3-low context frame; route to hypothyroid biochemistry frame.
- TSH suppressed: suppress FT3-low context frame; route to hyperthyroid/destructive thyroid logic if other markers support it.
- FT4 low with FT3 low: higher concern; clinician-review wording rather than low-energy-only explanation.
- Biotin/interference disclosed: add caveat or suppress if discordant.

### Red-line exclusions

- Missing TSH.
- Missing FT4.
- Missing thyroid medication status.
- Missing illness/recovery and energy-availability context.
- Pregnancy/postpartum without specialist logic.
- Thyroid medication use without medication-context wording.

### Safe user-facing wording constraints

HealthIQ may say:

- “Your free T3 result is below the reference range provided by your lab. When TSH and FT4 do not show a clear primary thyroid pattern, low free T3 can sometimes be seen during or after illness, physical stress, calorie restriction or low energy availability.”
- “This is not diagnostic of thyroid disease and should be interpreted alongside TSH, FT4, medication use and recent health context.”

HealthIQ must not say:

- “You have low T3 syndrome.”
- “You have hypothyroidism.”
- “Your thyroid is not converting properly.”
- “You need treatment.”

### Recommended HealthIQ AI runtime status

**ACTIVATE_WITH_STRICT_GATES** through a dedicated FT3-low activation-control sprint.

---

## Section B — Iron Batch C PSI / iron-pattern frame authority

### Revision 2 cohort decision

Iron low and iron overload frames can be activated with strict gates. The hepatocellular/haemolytic high-iron frame should remain deferred as a standalone signal but can be used as a suppressor or cautionary redirect when liver/haemolysis markers conflict with iron-overload interpretation.

### Cohort-level medical rationale

Serum iron is highly variable and should not be interpreted alone. Ferritin, transferrin saturation, transferrin/TIBC, FBC indices, CRP/inflammation, liver markers and supplement/infusion context are all important for safe frame selection.

The strongest iron frames are:

- low serum iron + low ferritin + low TSAT → iron deficiency pattern context;
- low serum iron + low TSAT + inflammation/CRP + normal/high ferritin → functional/inflammatory restriction context;
- high serum iron + high TSAT + ferritin above range → iron overload pattern context.

### Evidence summary

| Source | Year | Relevance | Strength | Limitation |
|---|---:|---|---|---|
| British Society of Gastroenterology guideline for iron deficiency anaemia | 2021 | Ferritin and TSAT interpretation in iron deficiency | High | Adult IDA-focused |
| EASL haemochromatosis guideline | 2022 | Elevated TSAT and ferritin in iron overload / haemochromatosis work-up | High | Haemochromatosis-specific |
| NHS / hospital iron-studies guidance | Current | TSAT calculation and interpretation of iron studies together | Moderate-high | Local lab guidance |
| Raised ferritin guidance / liver disease literature | 2024-current | Ferritin and liver/inflammation caveats | Moderate-high | Ferritin-focused rather than serum iron frame-specific |

### Candidate-level table

| Candidate / pattern | Medically valid? | Activation allowed? | Required companions | Contradictions | Red-line exclusions | Final decision |
|---|---|---|---|---|---|---|
| Iron low / absolute iron deficiency | Yes | Yes, strict gates only | Ferritin low; TSAT low; FBC indices; CRP/inflammation context | CRP high with non-low ferritin; ferritin normal/high without explanation | Recent iron infusion/supplement loading; missing ferritin/TSAT | ACTIVATE_WITH_STRICT_GATES |
| Iron low / functional iron restriction-inflammation | Yes | Yes, strict gates only | CRP/inflammation high; ferritin normal/high; TSAT low; FBC indices | Ferritin low argues against pure inflammatory restriction; CRP normal weakens frame | Missing ferritin/TSAT/CRP; recent iron infusion/supplement confounding | ACTIVATE_WITH_STRICT_GATES |
| Iron high / iron overload context | Yes | Yes, strict gates only | TSAT high; ferritin above lab range; liver markers | ALT/AST/bilirubin/haemolysis markers suggest release/injury; ferritin not high weakens overload frame | Recent iron ingestion/infusion; missing TSAT; missing ferritin | ACTIVATE_WITH_STRICT_GATES |
| Iron high / hepatocellular or haemolytic release | Plausible | Not as standalone launch signal | ALT/AST/GGT/bilirubin; haemolysis markers where available; TSAT/ferritin | TSAT + ferritin high supports overload; normal liver/haemolysis markers weakens frame | Missing haemolysis markers for haemolysis claim; isolated high iron only | DEFER_MEDICAL_REVIEW; ALLOW_AS_SUPPRESSOR_OR_CAVEAT |

### Safe wording constraints

Allowed:

- “This pattern may be consistent with reduced circulating iron availability when interpreted with ferritin, transferrin saturation and inflammation markers.”
- “Your iron result is above the lab reference range and is supported by transferrin saturation and ferritin, which can sometimes be seen when the body has accumulated more iron than usual.”
- “Serum iron can be affected by inflammation, liver stress, haemolysis, recent supplements and biological variation, so it should not be interpreted alone.”

Prohibited:

- “You have iron deficiency.”
- “You have iron overload.”
- “You have haemochromatosis.”
- “You have anaemia of chronic disease.”
- “Your liver is releasing iron.”

### Recommended HealthIQ AI runtime status

- Iron low absolute deficiency: **ACTIVATE_WITH_STRICT_GATES**.
- Iron low functional restriction/inflammation: **ACTIVATE_WITH_STRICT_GATES**.
- Iron high overload context: **ACTIVATE_WITH_STRICT_GATES**.
- Iron high hepatocellular/haemolytic release: **defer as standalone; allow as suppressor/caveat frame where liver/haemolysis markers conflict with overload framing**.

---

## Section C — TSAT calculated mode: medical boundary only

### Revision 2 decision

**DEFER_CORE_ENGINE_POLICY**

### Medical rationale

Pass 2 is correct that calculated transferrin saturation is not medically controversial if serum iron and TIBC are known and units are compatible:

```text
TSAT (%) = serum iron / TIBC × 100
```

However, this remains a Core Engine / SSOT governance issue. HealthIQ must decide how to govern:

- accepted input markers;
- unit normalisation;
- same-sample/report requirement;
- direct vs calculated precedence;
- provenance label;
- rounding;
- whether calculated TSAT can activate signals or only support them.

### Medical boundary decision

Calculated TSAT is medically meaningful and may support interpretation once governed. Until formula/provenance governance exists, it should not silently behave as a directly reported lab value.

### Required input markers

- Serum iron.
- TIBC, or a governed equivalent if transferrin-derived calculation is approved separately.
- Same report/sample context.
- Compatible units after deterministic normalisation.

### Recommended HealthIQ AI runtime status

**DEFER_CORE_ENGINE_POLICY**. No additional medical review is required for the basic serum iron / TIBC formula, but implementation must be governed by Core Engine.

---

## Section D — Homocysteine PSI cohort

### Revision 2 cohort decision

Both homocysteine frames are medically cleared with strict gates. Pass 2 strengthens the wording boundary: consumer-facing output must avoid “methylation impairment” and must not make broad cardiovascular-risk claims.

### Cohort-level medical rationale

High homocysteine can be interpreted cautiously in two clinically meaningful contexts:

1. B-vitamin-dependent processing context, especially when B12/active B12 and/or folate are low or borderline.
2. Renal clearance context, especially where creatinine/eGFR suggests reduced kidney function.

HealthIQ must not use homocysteine as a broad cardiovascular-event prediction signal. Although homocysteine is epidemiologically associated with vascular risk, routine use for cardiovascular screening is not supported by major laboratory medicine guidance and interventional trials have not consistently shown outcome improvement from homocysteine lowering.

### Evidence summary

| Source | Year | Relevance | Strength | Limitation |
|---|---:|---|---|---|
| NICE NG239 Vitamin B12 deficiency | 2024 | B12 deficiency investigation context | High | Does not endorse broad homocysteine screening |
| NICE CKS B12/folate anaemia | Current | Homocysteine/MMA supplementary testing context | High | Clinical pathway, not consumer product logic |
| ADLM Homocysteine optimal testing guide | 2023 | Advises against routine population CVD screening | High | US lab-medicine context |
| Major homocysteine-lowering trials | 2000s onward | Shows caution around cardiovascular outcome claims | High | Older but still relevant |
| Renal impairment literature | Current | Supports renal contribution to homocysteine elevation | Moderate-high | Population-specific |

### Candidate 1 — Homocysteine high / B-vitamin-related processing context

#### Activation logic

Activate only when high homocysteine is paired with B12/active B12 and folate context.

#### Required companion markers

- REQUIRED: B12 or active B12.
- REQUIRED: folate.
- STRONGLY RECOMMENDED: MCV.
- STRONGLY RECOMMENDED: MMA where B12 ambiguity exists.
- REQUIRED CONTRADICTION: creatinine/eGFR if available.

#### Contradiction logic

- Normal B12 and normal folate weaken the B-vitamin frame.
- Reduced eGFR/high creatinine shifts toward renal-clearance frame.
- Supplement use can mask or modify interpretation.

#### Safe wording

- “Your homocysteine result is above the reference range provided by your lab. Homocysteine can rise when the body has less vitamin B12 or folate available for related metabolic processes. This should be interpreted alongside your B12, folate, red-cell indices and kidney function.”

#### Prohibited wording

- “Methylation impairment” in consumer output.
- “You have a methylation problem.”
- “You have cardiovascular risk because homocysteine is high.”
- Supplement or treatment advice.

#### Recommended status

**ACTIVATE_WITH_STRICT_GATES**.

### Candidate 2 — Homocysteine high / renal clearance context

#### Activation logic

Activate only when renal markers support the frame.

#### Required companion markers

- REQUIRED: creatinine and/or eGFR.
- STRONGLY RECOMMENDED: B12/active B12 and folate.
- OPTIONAL: thyroid markers, liver markers, inflammatory markers.

#### Safe wording

- “Your homocysteine result is above the reference range provided by your lab. When kidney function is lower, homocysteine can accumulate in the blood because the kidneys are involved in its clearance and metabolism. This is not a kidney disease diagnosis on its own and should be interpreted with your kidney markers and B-vitamin results.”

#### Recommended status

**ACTIVATE_WITH_STRICT_GATES**.

---

## Section E — Leukocyte PSI cohort

### Revision 2 cohort decision

Pass 2 makes a credible medical case that WBC high and lymphocyte low can be useful non-diagnostic educational signals, but these remain blocked by non-medical SSOT/system-mapping issues. Neutrophil percentage high can only activate as a primary signal when absolute neutrophil count confirms the pattern.

### Cohort-level medical rationale

Leukocyte changes are common and often reactive. High WBC may reflect infection, inflammation, physical stress, exercise, smoking, pregnancy, medications such as corticosteroids, or haematological disease. Low lymphocytes may be transient after illness or stress, or related to medication, undernutrition, immunosuppression or systemic disease. Neutrophil predominance may reflect bacterial infection, inflammation, stress, steroids or smoking.

Because these patterns are non-specific, they are suitable only as cautious immune/inflammatory context signals, not disease diagnoses.

### Evidence summary

| Source | Year | Relevance | Strength | Limitation |
|---|---:|---|---|---|
| AAFP Evaluation of Patients with Leukocytosis | 2015 | Reactive leukocytosis and differential diagnosis | Moderate-high | US primary care review |
| Merck Manual Professional, Lymphocytopenia | Current | Common causes and clinical context for low lymphocytes | Moderate-high | Clinical reference, not UK guideline |
| StatPearls / clinical haematology references | Current | Leukocytosis and differential interpretation | Moderate | Secondary references |
| CBC/differential literature | Current | Percentage vs absolute count limitations | Moderate | Often acute-care context |

### Candidate 1 — WBC high / reactive leukocytosis

#### Medical validity

Medically cleared in principle, but not implementable until SSOT identity and system-mapping blockers are resolved.

#### Required companions

- REQUIRED: canonical WBC total.
- STRONGLY RECOMMENDED: absolute neutrophils and/or differential count.
- OPTIONAL: CRP.
- OPTIONAL: platelets and haemoglobin for broader FBC context.
- REQUIRED CONTEXT WHERE AVAILABLE: corticosteroid/immunosuppressant medication, smoking, exercise/stress, recent infection/inflammation, pregnancy.

#### Red-line exclusions

- WBC not resolved to canonical SSOT ID.
- Critical/highly elevated WBC or lab critical flag.
- Immature cells/blasts if reported.
- Concurrent cytopenias or red-flag symptoms requiring clinician-review wording.

#### Safe wording

- “Your white blood cell count is above the reference range provided by your lab. White blood cells are part of the immune system, and counts above the reference range are commonly seen with infection, inflammation, physical stress, recent exercise, smoking or certain medicines. This is not diagnostic of any specific condition.”

#### Recommended status

**DEFER_CORE_ENGINE_POLICY** with medical clearance recorded.

### Candidate 2 — Lymphocyte low / stress or immunosuppression context

#### Medical validity

Medically cleared in principle, but not implementable until lymphocyte and WBC identity blockers are resolved.

#### Required companions

- REQUIRED: canonical absolute lymphocyte count.
- REQUIRED: WBC total.
- STRONGLY RECOMMENDED: neutrophils.
- OPTIONAL: CRP/infection context.
- REQUIRED CONTEXT WHERE AVAILABLE: corticosteroid/immunosuppressant medication, recent illness, recurrent infections, severe stress, undernutrition.

#### Red-line exclusions

- Lymphocyte marker not resolved to canonical SSOT ID.
- Missing WBC total.
- Very low lymphocyte count or lab critical flag.
- Persistent pattern without repeat-test context.
- Severe/recurrent infection symptoms.

#### Safe wording

- “Your lymphocyte count is below the reference range provided by your lab. Lymphocytes are white blood cells involved in immune defence and immune memory. A mildly low result can sometimes be seen after illness, during periods of physical stress, or with certain medicines such as corticosteroids. This is not diagnostic on its own.”

#### Recommended status

**DEFER_CORE_ENGINE_POLICY** with medical clearance recorded.

### Candidate 3 — Neutrophil percentage high / neutrophil-predominant shift

#### Medical validity

Medically plausible, but unsafe as a percentage-only primary signal. Pass 2 is right that the issue can be handled by gates, but the strict requirement is that absolute neutrophil count must be available and supportive for full activation.

#### Activation paths

**Path A — full activation:**

- neutrophil percentage high; and
- absolute neutrophil count above lab range; and
- WBC/differential context present.

**Path B — modifier/caveat only:**

- neutrophil percentage high but ANC absent; or
- neutrophil percentage high with normal ANC.

Path B must not render a primary “neutrophilia” or “neutrophil-predominant inflammatory response” signal. It may say that the proportion is shifted and that an absolute count is needed for interpretation.

#### Required companions

- REQUIRED FOR FULL ACTIVATION: absolute neutrophil count.
- REQUIRED: WBC total.
- STRONGLY RECOMMENDED: lymphocyte absolute count.
- OPTIONAL: CRP or infection/inflammation context.
- CONTEXT: corticosteroids, smoking, stress/exercise, pregnancy, recent infection.

#### Recommended status

**ACTIVATE_WITH_STRICT_GATES only when ANC confirms; otherwise modifier-only.**

---

## Section F — kb59 thyroid antibody packages

### Revision 2 cohort decision

TPOAb high with hypothyroid biochemistry is cleared. TPOAb high with euthyroid thyroid function is medically defensible but should not be launch-core. TgAb packages remain deferred and should be considered corroborators before primary signals.

### Group-level medical rationale

Thyroid antibodies can support autoimmune thyroid context, but must not diagnose autoimmune thyroid disease or imply that thyroid function is currently impaired unless TSH and FT4 support that pattern. TPOAb is more clinically central than TgAb for routine hypothyroid-context interpretation.

### Evidence summary

| Source | Year | Relevance | Strength | Limitation |
|---|---:|---|---|---|
| NICE NG145 | 2019, updated | Consider TPOAbs in adults with TSH above reference range; do not repeat TPOAbs | High | Does not define consumer wording |
| NICE CKS Hypothyroidism | Current | TPOAb positivity predicts progression risk | High | Primary-care pathway |
| Thyroid autoimmunity cohort literature | Current/older longitudinal data | Euthyroid antibody positivity can predict future thyroid dysfunction | Moderate-high | Population-specific; not always direct product actionability |
| Thyroid antibody reviews | Current | TgAb is supportive but less central than TPOAb | Moderate | Heterogeneous evidence |

### Candidate 1 — TPOAb high / autoimmune thyroid context supporting hypothyroid biochemistry

#### Activation logic

Cleared only when TPOAb high is accompanied by TSH above lab range and FT4 context.

#### Required companions

- REQUIRED: TPOAb high.
- REQUIRED: TSH present and above lab range.
- REQUIRED: FT4 present.
- OPTIONAL: FT3.
- OPTIONAL: TgAb as corroborator.

#### Contradiction logic

- TPOAb high with TSH/FT4 within range routes to euthyroid antibody context, not hypothyroid frame.
- Suppressed TSH or high FT4 redirects to thyrotoxic/destructive/stimulatory thyroid logic.

#### Safe wording

- “Your TPO antibody result is raised. When this is seen alongside thyroid function markers that suggest reduced thyroid output, it can support an autoimmune thyroid context. This is not a diagnosis on its own and should be interpreted with your TSH, FT4, medication and clinical context.”

#### Prohibited wording

- “You have Hashimoto’s.”
- “You have autoimmune thyroid disease.”
- “Your immune system is attacking your thyroid.”
- “Your thyroid will fail.”

#### Recommended status

**ACTIVATE_WITH_STRICT_GATES**.

### Candidate 2 — TPOAb high / euthyroid autoimmune risk

#### Medical rationale

Pass 2 provides a stronger affirmative case than Pass 1 credited. Euthyroid TPOAb positivity has prognostic relevance and may identify people more likely to develop later thyroid dysfunction. However, from a product-safety perspective, this is a longer-horizon risk-context signal with anxiety potential and low immediate actionability.

#### Recommended status

**DEFER_POST_LAUNCH / advanced cautious context**, not launch-core activation.

#### Safe future wording

- “Your TPO antibody result is raised, while your TSH and thyroid hormone levels are currently within the reference range. This can sometimes indicate autoimmune thyroid activity that may be worth monitoring over time. It does not mean your thyroid is currently underactive, and many people with raised antibodies maintain thyroid function for years.”

### Candidate 3 — TgAb high / autoimmune hypothyroid pattern

#### Medical rationale

TgAb can support thyroid autoimmunity but is less central than TPOAb in routine hypothyroid interpretation. Source extraction/package scoping remains incomplete.

#### Recommended status

**DEFER_POST_LAUNCH / corroborator-only initially**.

### Candidate 4 — TgAb high / euthyroid autoimmune risk

#### Medical rationale

Plausible as autoimmune thyroid context, but lower actionability and weaker launch relevance.

#### Recommended status

**DEFER_POST_LAUNCH / corroborator-only initially**.

---

## Activation authority outputs

```yaml
cleared_candidates:
  - candidate_id: ft3_low_reduced_peripheral_t3_availability_context
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
      - biotin_or_assay_interference_context
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
      - tsh_high_with_free_t4_low_for_this_frame
    safe_runtime_frame: reduced_peripheral_t3_availability_context
    unsafe_runtime_frame: hypothyroidism_diagnosis
    medical_review_status: cleared_with_strict_gates_revision_2
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
      - recent_iron_infusion_without_specific_logic
    safe_runtime_frame: iron_deficiency_pattern_context
    unsafe_runtime_frame: iron_deficiency_diagnosis
    medical_review_status: cleared_with_strict_gates_revision_2
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
    unsafe_runtime_frame: anaemia_of_inflammation_diagnosis
    medical_review_status: cleared_with_strict_gates_revision_2
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
      - ferritin_not_above_lab_range
    safe_runtime_frame: iron_overload_pattern_context
    unsafe_runtime_frame: haemochromatosis_diagnosis
    medical_review_status: cleared_with_strict_gates_revision_2
    implementation_owner: Knowledge Bus

  - candidate_id: homocysteine_high_b_vitamin_related_processing_context
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
      - consumer_facing_methylation_impairment_label
    safe_runtime_frame: b_vitamin_dependent_metabolic_processing_context
    unsafe_runtime_frame: methylation_impairment_or_cardiovascular_event_prediction
    medical_review_status: cleared_with_strict_gates_revision_2
    implementation_owner: Knowledge Bus

  - candidate_id: homocysteine_high_renal_clearance_context
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
    medical_review_status: cleared_with_strict_gates_revision_2
    implementation_owner: Knowledge Bus

  - candidate_id: neutrophil_pct_high_with_anc_confirmed_neutrophil_shift
    signal_direction: high
    activation_status: ACTIVATE_WITH_STRICT_GATES_ONLY_IF_ANC_PRESENT_AND_HIGH
    required_primary_marker: neutrophil_pct
    required_companion_markers:
      - neutrophils_abs
      - wbc_total
      - lymphocytes_abs_if_available
    required_contradiction_markers:
      - normal_neutrophils_abs
      - low_lymphocytes_abs
      - crp_normal_if_available
    required_context_fields:
      - recent_infection_or_inflammation_context
      - corticosteroid_use
      - smoking_status_if_available
      - physical_stress_or_recent_heavy_exercise_if_available
      - pregnancy_status_if_relevant
    red_line_exclusions:
      - missing_absolute_neutrophil_count_for_full_activation
      - normal_absolute_neutrophil_count_for_neutrophilia_frame
      - lab_critical_flag
    safe_runtime_frame: neutrophil_predominant_shift_confirmed_by_absolute_count
    unsafe_runtime_frame: neutrophilia_from_percentage_only
    medical_review_status: cleared_only_with_anc_confirmation_revision_2
    implementation_owner: Knowledge Bus / Core Engine

  - candidate_id: tpo_ab_high_autoimmune_thyroid_context_supporting_hypothyroid_biochemistry
    signal_direction: high
    activation_status: ACTIVATE_WITH_STRICT_GATES
    required_primary_marker: tpo_ab
    required_companion_markers:
      - tsh
      - free_t4
    required_contradiction_markers:
      - tsh_not_above_range
      - free_t4_not_low_or_not_supportive
      - suppressed_tsh_or_high_ft4_pattern
    required_context_fields:
      - thyroid_medication_status
      - pregnancy_postpartum_status
    red_line_exclusions:
      - missing_tsh
      - missing_free_t4
      - euthyroid_biochemistry_for_hypothyroid_frame
      - hashimotos_diagnosis_wording
    safe_runtime_frame: autoimmune_thyroid_context_supporting_hypothyroid_biochemistry
    unsafe_runtime_frame: hashimotos_or_autoimmune_thyroid_disease_diagnosis
    medical_review_status: cleared_with_strict_gates_revision_2
    implementation_owner: Knowledge Bus
```

---

## Deferred / rejected outputs

```yaml
deferred_candidates:
  - candidate_id: iron_high_hepatocellular_or_hemolytic_release
    deferred_status: DEFER_MEDICAL_REVIEW_AS_STANDALONE_SIGNAL
    reason: Pass 2 medical plausibility accepted, but routine ALT/bilirubin gates are insufficient to distinguish liver injury, haemolysis, overload and acute illness safely.
    what_evidence_is_missing:
      - explicit haemolysis marker requirements
      - stronger liver injury frame rules
      - clear contradiction handling against iron overload frame
      - safe suppressor_or_redirect implementation design
    permitted_interim_use:
      - caveat_when_liver_markers_conflict_with_overload_frame
      - suppressor_when_b3_overload_and_liver_release_frames_conflict
      - clinician_review_message_when_high_iron_plus_liver_markers_are_discordant
    who_must_clear: Medical Review
    recommended_future_review: hepatocellular_haemolytic_iron_release_frame_review

  - candidate_id: transferrin_saturation_calculated_mode
    deferred_status: DEFER_CORE_ENGINE_POLICY
    reason: Medically meaningful but requires governed derived-metric formula, unit normalisation, same-sample rule and provenance labelling.
    what_evidence_is_missing:
      - no_medical_evidence_missing_for_serum_iron_tibc_formula
      - core_engine_ssot_formula_governance_missing
      - provenance_and_precedence_policy_missing
    who_must_clear: Core Engine
    recommended_future_review: P1-TRANSFERRIN-SAT-CALC-POLICY-1

  - candidate_id: wbc_high_reactive_leukocytosis
    deferred_status: DEFER_CORE_ENGINE_POLICY_MEDICALLY_CLEARED_IN_PRINCIPLE
    reason: Medical case accepted, but WBC SSOT identity and system-mapping blockers remain.
    what_evidence_is_missing:
      - canonical_wbc_identity_resolution
      - differential_count_gate_mapping
      - critical_high_suppression_policy
      - symptom_context_safety_gates
    who_must_clear: Core Engine plus Medical Review
    recommended_future_review: leukocyte_identity_and_activation_gate_review

  - candidate_id: lym_low_lymphopenia_stress_or_immunosuppression
    deferred_status: DEFER_CORE_ENGINE_POLICY_MEDICALLY_CLEARED_IN_PRINCIPLE
    reason: Medical case accepted, but lymphocyte SSOT identity blocker and context requirements remain.
    what_evidence_is_missing:
      - canonical_absolute_lymphocyte_identity
      - wbc_total_identity
      - medication_steroid_immunosuppression_context_gates
      - repeat_test_and_persistence_wording_policy
    who_must_clear: Core Engine plus Medical Review
    recommended_future_review: lymphocyte_identity_and_context_gate_review

  - candidate_id: neutrophil_pct_high_without_anc_confirmation
    deferred_status: MODIFIER_ONLY_NOT_PRIMARY_SIGNAL
    reason: Neutrophil percentage can be misleading without absolute neutrophil count because relative percentages can shift when other leukocyte fractions change.
    what_evidence_is_missing:
      - absolute_neutrophil_count
      - wbc_total_confirmation
    who_must_clear: Medical Review if future percentage-only signal is proposed
    recommended_future_review: neutrophil_absolute_vs_percentage_policy

  - candidate_id: tpo_ab_high_euthyroid_autoimmune_risk
    deferred_status: DEFER_POST_LAUNCH_ADVANCED_CONTEXT
    reason: Medically defensible and stronger than Pass 1 credited, but better as longitudinal risk-context after launch due anxiety/actionability considerations.
    what_evidence_is_missing:
      - product_level_decision_on_risk_context_surfacing
      - longitudinal_monitoring_wording
      - package_psi_activation_plan
    who_must_clear: Product plus Medical Review
    recommended_future_review: thyroid_antibody_euthyroid_context_review

  - candidate_id: tgab_high_autoimmune_hypothyroid_pattern
    deferred_status: DEFER_POST_LAUNCH_CORROBORATOR_ONLY
    reason: TgAb is less central than TPOAb and source extraction/package scoping is incomplete.
    what_evidence_is_missing:
      - full_signal_library_review
      - package_scoping
      - tpoab_tsh_ft4_companion_policy
    who_must_clear: Medical Review plus Knowledge Bus
    recommended_future_review: tgab_activation_scoping_review

  - candidate_id: tgab_high_euthyroid_autoimmune_risk
    deferred_status: DEFER_POST_LAUNCH_CORROBORATOR_ONLY
    reason: Plausible as autoimmune thyroid context but not launch-critical and less actionable.
    what_evidence_is_missing:
      - full_source_review
      - safe_longitudinal_context_wording
      - package_psi_plan
    who_must_clear: Medical Review plus Product
    recommended_future_review: tgab_euthyroid_context_review
```

---

## Cross-validation checklist for Pass 2 / Pass 3 Medical LLM

A future Medical Research reviewer should specifically validate the following.

### 1. Highest-risk medical decisions in this revision

- FT3 low is now medically cleared with strict gates; confirm suppression when TSH/FT4 indicates primary thyroid disease.
- Iron high overload remains cleared, but only with ferritin above lab range and high TSAT.
- Hepatocellular/haemolytic high-iron frame is not accepted as standalone despite Pass 2’s stronger position.
- Neutrophil percentage high is allowed only with ANC confirmation.
- TPOAb euthyroid risk is medically valid but deferred for product-safety/actionability reasons.

### 2. Evidence weak or conflicting

- Homocysteine cardiovascular interpretation remains controversial and should not become a launch frame.
- Hepatocellular/haemolytic iron release is plausible but under-supported by routine panels without haemolysis markers.
- TgAb interpretation is less central than TPOAb and should be corroborator-first.
- Euthyroid TPOAb positivity has prognostic value but uncertain consumer actionability.
- Neutrophil percentage without absolute count is weak.

### 3. Decisions that depend on companion markers

- FT3 low requires TSH and FT4.
- Iron low absolute deficiency requires ferritin and TSAT.
- Functional iron restriction requires ferritin, TSAT and inflammatory context.
- Iron overload requires TSAT and ferritin above lab range.
- Homocysteine B-vitamin frame requires B12/active B12 and folate.
- Homocysteine renal frame requires creatinine/eGFR.
- TPOAb hypothyroid-context frame requires TSH and FT4.
- Neutrophil percentage high requires absolute neutrophil count for full activation.

### 4. Diagnostic-overreach risks

- “Hypothyroidism” from FT3 low.
- “Iron deficiency” from low serum iron alone.
- “Iron overload” or “haemochromatosis” from high serum iron alone.
- “Liver iron release” from ALT/bilirubin alone.
- “Methylation impairment” from homocysteine.
- “Infection” from WBC or neutrophil changes.
- “Hashimoto’s” from TPOAb positivity.
- “Immune suppression” from low lymphocytes.

### 5. Core Engine policy blockers

- Calculated TSAT formula/provenance.
- WBC canonical identity.
- Lymphocyte canonical identity.
- WBC total naming / `wbc_total` vs canonical SSOT.
- Absolute neutrophil count availability and canonical ID.
- Leukocyte system mapping.
- Direct-vs-calculated TSAT precedence.

### 6. Sources to independently verify

- NICE NG145 thyroid testing and thyroid antibody recommendations.
- Endotext non-thyroidal illness syndrome.
- BSG 2021 iron deficiency anaemia guideline.
- EASL 2022 haemochromatosis guideline.
- NHS / hospital TSAT formula and iron studies pages.
- NICE NG239 B12 deficiency guidance.
- ADLM homocysteine optimal testing guidance.
- AAFP leukocytosis review.
- Merck lymphocytopenia reference.
- Thyroid antibody prognostic cohort evidence.

### 7. Wording that must be made safer

- “Low T3 syndrome” should not render as a user diagnosis.
- “Functional iron restriction” should explain inflammation-mediated reduced iron availability, not diagnose anaemia of inflammation.
- “Iron overload context” must not say haemochromatosis.
- “Methylation impairment” should not be user-facing.
- “Reactive leukocytosis” should not imply infection.
- “Autoimmune hypothyroid pattern” should render as “autoimmune thyroid context supporting hypothyroid biochemistry.”
- “Euthyroid autoimmune risk” should be framed as monitoring context, not predicted disease.

---

## References

1. NICE NG145. Thyroid disease: assessment and management. https://www.nice.org.uk/guidance/ng145
2. Endotext. The Non-Thyroidal Illness Syndrome. https://www.ncbi.nlm.nih.gov/books/NBK285570/
3. Endotext. Assay of Thyroid Hormone and Related Substances. https://www.ncbi.nlm.nih.gov/books/NBK279113/
4. NICE exceptional surveillance of thyroid disease guideline: biotin interference. https://www.nice.org.uk/guidance/ng145/resources/2023-exceptional-surveillance-of-thyroid-disease-assessment-and-management-nice-guideline-ng145-pdf-17094825912517
5. Snook J, et al. British Society of Gastroenterology guidelines for the management of iron deficiency anaemia in adults. Gut. 2021. https://gut.bmj.com/content/70/11/2030
6. EASL Clinical Practice Guidelines on haemochromatosis. Journal of Hepatology. 2022. https://easl.eu/wp-content/uploads/2022/06/PIIS01688278220021121.pdf
7. NHS. Total iron-binding capacity and transferrin test. https://www.nhs.uk/tests-and-treatments/tibc-test/
8. Lab Tests Online UK. Iron tests. https://labtestsonline.org.uk/tests/iron-tests
9. NICE NG239. Vitamin B12 deficiency in over 16s: diagnosis and management. https://www.nice.org.uk/guidance/ng239
10. NICE CKS. Anaemia — B12 and folate deficiency. https://cks.nice.org.uk/topics/anaemia-b12-folate-deficiency/
11. ADLM. Homocysteine optimal testing guide. https://myadlm.org/advocacy-and-outreach/optimal-testing-guide-to-lab-test-utilization/g-s/homocysteine
12. Lonn E, et al. Homocysteine lowering with folic acid and B vitamins in vascular disease. NEJM. 2006. https://www.nejm.org/doi/full/10.1056/NEJMoa060900
13. Riley LK, Rupert J. Evaluation of Patients with Leukocytosis. American Family Physician. 2015. https://www.aafp.org/pubs/afp/issues/2015/1201/p1004.html
14. Merck Manual Professional. Lymphocytopenia. https://www.merckmanuals.com/professional/hematology-and-oncology/leukopenias/lymphocytopenia
15. StatPearls. Hemolytic Anemia. https://www.ncbi.nlm.nih.gov/books/NBK558904/
16. NICE CKS. Hypothyroidism assessment. https://cks.nice.org.uk/topics/hypothyroidism/diagnosis/assessment/
17. British Thyroid Foundation. Thyroid antibodies explained. https://www.btf-thyroid.org/thyroid-antibodies-explained
18. Vanderpump MPJ. The epidemiology of thyroid disease. British Medical Bulletin. 2011 / Whickham-related longitudinal thyroid autoimmunity evidence.

---

## Revision 2 change log

| Item | Pass 1 position | Pass 2 input | Revision 2 adjudication |
|---|---|---|---|
| FT3 low | Cleared but cautious / previously deferred in ADR | Strong activation case | Cleared with strict gates |
| Iron low absolute | Cleared | Confirmed | Cleared with supplement/infusion caveat |
| Iron low functional | Cleared | Confirmed | Cleared with supplement/infusion caveat |
| Iron high overload | Cleared | Confirmed with stronger ferritin gate | Cleared; ferritin must be above lab range |
| Iron high hepatocellular/haemolytic | Deferred | Pass 2 argued unlock | Not accepted as standalone; allowed as caveat/suppressor |
| TSAT calculated | Core Engine | Core Engine only | unchanged |
| Homocysteine B-vitamin | Cleared | Confirmed | Cleared; prohibit “methylation impairment” wording |
| Homocysteine renal | Cleared | Confirmed | Cleared |
| WBC high | Deferred Core Engine | Medical cleared pending SSOT | Medical clearance recorded; Core Engine blocked |
| Lymphocyte low | Deferred Core Engine | Medical cleared pending SSOT | Medical clearance recorded; Core Engine blocked |
| Neutrophil % high | Deferred | Pass 2 argued gated unlock | Unlock only with ANC confirmation; modifier otherwise |
| TPOAb hypothyroid | Cleared | Confirmed | Cleared |
| TPOAb euthyroid | Deferred post-launch | Pass 2 argued unlock | Medically valid but post-launch/advanced cautious context |
| TgAb packages | Deferred | Deferred | unchanged |
