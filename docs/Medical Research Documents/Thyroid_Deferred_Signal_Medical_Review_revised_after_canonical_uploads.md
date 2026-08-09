# Thyroid Deferred Signal Medical Review — Revised After Canonical TgAb/TPOAb Uploads

**Work type:** Medical research / medical-governance review only  
**Scope:** three disputed thyroid antibody frames  
**Date:** 2026-08-09  
**Product context:** HealthIQ AI secondary consumer interpretation of blood-test results, with clinically useful, non-diagnostic explanation and appropriate follow-up guidance  
**Runtime / implementation status:** Not used as medical authority  
**Production decision status:** Not made here; requires Anthony ratification for this review context  

---

# Executive Recommendation

| Frame | Recommendation | Confidence | One-line rationale |
|---|---|---:|---|
| Frame 1 — TgAb high / `inv_tgab_high_autoimmune_hypothyroid_pattern` | REFRAME | MODERATE-HIGH | Medically valid as supportive autoimmune context when hypothyroid biochemistry is present, but not sufficiently useful or distinct as a standalone consumer finding. |
| Frame 2 — TgAb high / `inv_tgab_high_euthyroid_autoimmune_risk` | REFRAME | MODERATE | Medically plausible but weaker and more anxiety-prone than TPOAb; should become low-prominence context/follow-up guidance, not an independent finding. |
| Frame 3 — TPOAb high / `inv_tpo_ab_high_euthyroid_autoimmune_risk` | PROMOTE | HIGH | Existing canonical source and prior ratified review support cautious surfacing as preserved-function autoimmune-thyroid risk/context, with strict non-diagnostic wording and TSH/FT4 gates. |

## Change from previous review

The earlier review concluded that the TgAb frames could not be exactly identified from available canonical artefacts. The new upload changes that. The `thyroid_antibodies_pass_3.json` file contains two explicit TgAb investigation specs:

1. `inv_tgab_high_autoimmune_hypothyroid_pattern`
2. `inv_tgab_high_euthyroid_autoimmune_risk`

The new evidence therefore removes the previous source-identification gap. It does **not** fully remove the product-safety concern: TgAb is medically real, but its best role in HealthIQ is contextual/corroborative rather than standalone consumer surfacing.

---

# Frame 1 — TgAb high [`inv_tgab_high_autoimmune_hypothyroid_pattern`]

## Canonical HealthIQ source reviewed

### Identified canonical frame

```text
spec_id: inv_tgab_high_autoimmune_hypothyroid_pattern
signal_id: signal_tgab_high
primary_marker: tgab
trigger_direction: high
research_domain: endocrine
```

### HealthIQ source summary

The uploaded Pass 3 antibody research defines this frame as TgAb-high autoimmune hypothyroid context. It states that TgAb is a thyroid autoantibody that can support autoimmune thyroid interpretation when corroborated by thyroid-function changes or other thyroid antibodies.

The frame includes:

- `tpo_ab` high as a corroborator;
- `tsh` high as a corroborator;
- `free_t4` low as a severity marker;
- `free_t3` high as a differential marker redirecting away from hypothyroid interpretation;
- two hypotheses:
  - `hyp_tgab_autoimmune_thyroiditis_with_failure`;
  - `hyp_tgab_supportive_autoimmune_cause_of_primary_hypothyroidism`.

The override rule escalates when high TgAb coexists with raised TSH and low FT4.

## Exact medical interpretation

Raised TgAb indicates antibodies against thyroglobulin. It can support autoimmune thyroid disease context, particularly Hashimoto-pattern thyroiditis, but it is not as central as TPOAb for routine autoimmune-hypothyroid assessment.

This frame is medically valid **only as a contextual autoimmune-cause support frame** when thyroid biochemistry already indicates hypothyroid physiology.

The strongest safe inference is:

> High TgAb may support an autoimmune thyroid context when TSH and FT4 already suggest primary hypothyroid physiology, especially if TPOAb is also positive or unavailable.

What must not be inferred:

- Hashimoto’s disease diagnosis from TgAb alone;
- Graves’ disease from TgAb;
- current hypothyroidism from TgAb alone;
- thyroid-failure severity from antibody titre;
- need for treatment;
- need to repeat TgAb routinely.

## Required context

Minimum safe context:

| Context | Requirement |
|---|---|
| TgAb | Required as primary marker. |
| TSH | Required to assess primary thyroid stress/failure. |
| FT4 | Required to distinguish overt biochemical hypothyroidism from subclinical/evolving physiology. |
| TPOAb | Strongly recommended; if positive, it becomes the stronger autoimmune-thyroid marker. |
| FT3 | Useful suppressor/redirect when high or when hyperthyroid physiology exists. |
| Symptoms | Supportive context only; not diagnostic. |
| Known thyroid disease | Must be considered because antibody positivity may reflect known disease. |
| Thyroid treatment | Suppresses untreated natural-history wording. |
| Pregnancy/fertility | Requires clinician-discussion wording and should not use generic consumer monitoring logic. |
| TRAb/TSI | Not required unless hyperthyroid biochemistry suggests a Graves-pattern question. |

## Clinical usefulness

Clinically useful, but not as a separate consumer headline.

Usefulness exists where:

- TgAb is high and TSH/FT4 indicate hypothyroid physiology;
- TPOAb is unavailable or negative;
- HealthIQ needs to explain why an abnormal thyroid-function pattern may have autoimmune context.

Usefulness is weaker where:

- TPOAb is also high, because TPOAb is already the more established marker;
- TSH and FT4 are preserved;
- the user has known thyroid disease or is already being treated;
- the result was obtained in thyroid-cancer surveillance, where TgAb has a different role.

## Follow-up value

Reasonable follow-up context:

- repeat TSH and FT4 if thyroid dysfunction is new, borderline or discordant;
- TPOAb if not already measured and autoimmune cause is clinically relevant;
- clinician discussion if symptomatic, pregnant/planning pregnancy, known thyroid disease, or discordant results.

Do not recommend routine repeat TgAb testing.

## Disease-naming boundary

| Phrase | Decision |
|---|---|
| “thyroid autoimmunity” | Permitted as qualified context. |
| “autoimmune thyroid disease may be possible” | Permitted only with TSH/FT4 context. |
| “Hashimoto’s disease” | Not as a HealthIQ conclusion; may be mentioned only as a clinician-considered example in hypothyroid biochemical context. |
| “Graves’ disease” | Not supported by TgAb; use TRAb/TSI and hyperthyroid biochemistry if relevant. |
| “risk of future thyroid dysfunction” | Weak from TgAb alone; if used, keep lower-prominence and longitudinal. |

## Contradictions / suppressors

Suppress or redirect if:

- TSH and FT4 do not support hypothyroid physiology;
- TPOAb is positive and already explains autoimmune context — TgAb should become supporting context, not duplicate finding;
- FT3 is high or TSH is suppressed with raised FT4/FT3 — redirect to hyperthyroid / thyrotoxic context;
- known thyroid-cancer follow-up is present — TgAb belongs to thyroglobulin-monitoring interference context;
- current thyroid treatment is declared;
- pregnancy/fertility context is present and no pregnancy-specific logic exists.

## Overlap / duplication assessment

This frame overlaps strongly with:

- TPOAb high autoimmune hypothyroid pattern;
- primary hypothyroid biochemical interpretation from TSH/FT4;
- subclinical hypothyroid TSH-axis frames.

TgAb adds value mostly as **corroboration** or as an alternative autoimmune clue where TPOAb is absent/unavailable. It should not compete with TPOAb or TSH/FT4 as a standalone signal.

## Evidence strengths / limitations

### Existing HealthIQ evidence

Now sufficient to identify the frame and its intended hypotheses. Evidence strength in the spec is `moderate`.

### External evidence

- NICE evidence review says thyroid autoantibodies including TPOAb and TgAb may be useful to confirm autoimmunity as the cause in a patient with hypothyroidism, while noting TPOAb in particular is associated with progression in subclinical hypothyroidism.
- BTF says TgAb can be raised in Hashimoto’s thyroiditis but generally does not add anything to TPOAb results in assessment of people with raised TSH.
- ATA states Hashimoto’s diagnosis may involve thyroid-function evidence plus elevated thyroid antibodies, but antibody positivity with normal thyroid function does not require thyroid hormone treatment and antibody monitoring is not needed.

### Limitations

- TgAb is less central than TPOAb in most routine hypothyroid guidance.
- TgAb has a separate thyroid-cancer surveillance/interference role that HealthIQ must not conflate with autoimmune-thyroid interpretation.

## Disposition

```text
REFRAME
```

## Rationale

The frame is medically valid, but the current representation as a primary `signal_tgab_high` finding risks duplication and over-surfacing. It should be reframed as:

```text
contextual evidence / modifier
```

Recommended reframe:

> High TgAb should contribute supportive autoimmune-thyroid context when TSH/FT4 already indicate hypothyroid or subclinical hypothyroid physiology, especially if TPOAb is absent, unavailable or discordant. It should not independently generate a consumer-facing HealthIQ finding where TPOAb and thyroid-function frames already cover the clinical interpretation.

---

# Frame 2 — TgAb high [`inv_tgab_high_euthyroid_autoimmune_risk`]

## Canonical HealthIQ source reviewed

### Identified canonical frame

```text
spec_id: inv_tgab_high_euthyroid_autoimmune_risk
signal_id: signal_tgab_high
primary_marker: tgab
trigger_direction: high
research_domain: endocrine
```

### HealthIQ source summary

The uploaded Pass 3 antibody research defines this as a preserved-thyroid-function TgAb frame. It states that TgAb is a marker of thyroid autoimmunity usually interpreted as supportive context, especially when current thyroid function is preserved.

The frame includes:

- `tpo_ab` high as a corroborator;
- `tsh` and `free_t4` as differential markers;
- hypotheses:
  - `hyp_tgab_euthyroid_autoimmune_context`;
  - `hyp_tgab_future_hypothyroid_risk_supportive`;
- contradictions:
  - TSH above max redirects to dysfunction;
  - FT4 below min redirects to overt biochemical dysfunction;
  - isolated TgAb without TPOAb reduces confidence.

## Exact medical interpretation

High TgAb with current euthyroid thyroid-function markers may indicate thyroid-autoimmune context, but the finding is less definitive than TPOAb and should be interpreted cautiously when isolated.

The strongest safe inference is:

> High TgAb may provide supportive autoimmune-thyroid context when thyroid function is currently preserved, especially if TPOAb is also positive. Isolated TgAb does not establish current thyroid disease or a reliable individual prognosis.

What must not be inferred:

- current hypothyroidism;
- Hashimoto’s disease as a diagnosis;
- Graves’ disease;
- need for treatment;
- specific risk percentage or timing of future hypothyroidism;
- need for routine repeat TgAb testing.

## Required context

Minimum safe context:

| Context | Requirement |
|---|---|
| TgAb | Required. |
| TSH | Required to confirm this is not active/evolving hypothyroid physiology. |
| FT4 | Required to confirm preserved current thyroid hormone status. |
| TPOAb | Strongly recommended; without it, confidence should be lower. |
| FT3 | Optional; useful if hyperthyroid physiology is possible. |
| Pregnancy/fertility | Suppress generic consumer frame; clinician-discussion wording only. |
| Thyroid treatment/known thyroid disease | Suppress untreated risk wording. |
| Thyroid-cancer follow-up | Suppress autoimmune-risk interpretation. |

## Clinical usefulness

This frame has lower standalone consumer value than the TPOAb euthyroid frame.

Potential value:

- explains that TgAb can indicate autoimmune context;
- prevents overinterpretation by stating thyroid function is currently preserved;
- supports monitoring TSH/FT4 over time where clinically relevant.

Risks:

- anxiety from “autoimmune risk” despite normal thyroid function;
- duplication where TPOAb is also positive;
- over-labelling Hashimoto’s from an isolated antibody;
- conflation with TgAb’s thyroid-cancer monitoring role.

## Follow-up value

Reasonable follow-up context:

- If isolated TgAb with normal TSH/FT4: no strong routine finding; consider low-prominence note only.
- If TPOAb is also positive: prefer the TPOAb euthyroid frame; TgAb can be supporting context.
- If symptoms, family history, borderline TSH, pregnancy/fertility context or prior abnormal thyroid tests exist: clinician discussion and future TSH/FT4 monitoring may be useful.

Do not recommend TRAb/TSI unless hyperthyroid biochemistry exists.

## Disease-naming boundary

| Phrase | Decision |
|---|---|
| “thyroid autoimmunity” | Permitted only as low-confidence/qualified context if isolated. |
| “autoimmune thyroid disease may be possible” | Use cautiously; avoid if isolated TgAb with no TPOAb and normal TSH/FT4. |
| “Hashimoto’s disease” | Not permitted as HealthIQ conclusion. |
| “Graves’ disease” | Not supported. |
| “risk of future thyroid dysfunction” | Weaker than TPOAb; use only as monitoring context, not prognosis. |

## Contradictions / suppressors

Suppress or redirect if:

- TSH is above reference range — redirect to hypothyroid/subclinical hypothyroid context.
- FT4 is below reference range — redirect to overt thyroid hormone deficiency context.
- TPOAb is positive — use TPOAb euthyroid frame as primary; TgAb becomes corroborator.
- TRAb/TSI positive or TSH suppressed with high FT4/FT3 — redirect to hyperthyroid/Graves-pattern review.
- Thyroid-cancer surveillance context exists — do not use autoimmune-risk frame.
- Pregnancy/fertility context exists — use clinician-discussion wording and avoid generic risk framing.
- Known thyroid disease or treatment exists — do not present as a new risk state.

## Overlap / duplication assessment

This frame overlaps heavily with TPOAb euthyroid autoimmune-risk.

It is not sufficiently distinct as a standalone finding unless HealthIQ wants a deliberately low-prominence “isolated TgAb context” note. Even then, it should not be a main signal.

## Evidence strengths / limitations

### Existing HealthIQ evidence

Sufficient to identify the frame, but the frame’s own caveats state that isolated TgAb is less definitive than TPOAb and should be interpreted cautiously.

### External evidence

- BTF states TgAb can be raised in Hashimoto’s thyroiditis, is found in about 10% of the general population, and generally does not add anything to TPOAb results when assessing raised TSH.
- BTF also states positive antibodies can exist without thyroid disease.
- Review evidence supports that TPOAb and TgAb can identify thyroid autoimmunity and future-risk context, but the clinical signal is stronger and more commonly used for TPOAb.

## Disposition

```text
REFRAME
```

## Rationale

The underlying information is medically true but should not be a standalone consumer finding. It should be reframed as:

```text
low-prominence contextual evidence / follow-up guidance
```

Recommended reframe:

> High TgAb with preserved thyroid function should be surfaced only as cautious context, preferably when TPOAb is unavailable/discordant or when dual-antibody positivity supports the TPOAb euthyroid frame. It should not generate an independent headline finding.

---

# Frame 3 — TPOAb euthyroid autoimmune-risk [`inv_tpo_ab_high_euthyroid_autoimmune_risk`]

## Canonical HealthIQ source reviewed

### Identified canonical frame

```text
spec_id: inv_tpo_ab_high_euthyroid_autoimmune_risk
signal_id: signal_tpo_ab_high
activation_key: signal_tpo_ab_high::inv_tpo_ab_high_euthyroid_autoimmune_risk
primary_marker: tpo_ab
trigger_direction: high
research_domain: endocrine
```

### HealthIQ source summary

The uploaded YAML and Pass 3 JSON define this frame as high TPOAb with currently preserved thyroid function. It includes:

- TgAb as a corroborator;
- TSH and FT4 as differential markers;
- hypotheses:
  - `hyp_euthyroid_autoimmune_thyroid_risk`;
  - `hyp_future_primary_hypothyroid_progression_risk`;
- strong contradictions:
  - raised TSH redirects away from euthyroid risk to active/evolving hypothyroid physiology;
  - low FT4 redirects to overt biochemical dysfunction;
- missing-data policy:
  - if TSH and FT4 are unavailable, interpret antibody positivity as autoimmune context only and avoid assuming preserved or failed thyroid function.

The consolidated WHY pilot review previously recorded the same frame as `APPROVE_WITH_REVISIONS` and Anthony ratified that disposition, with requirements to preserve current euthyroid status, avoid personalised probability, avoid repeated antibody testing, and avoid treatment advice.

## Exact medical interpretation

High TPOAb indicates thyroid autoimmunity. When TSH and FT4 are currently within their governed/lab reference ranges, it can be interpreted as autoimmune-thyroid context with preserved current thyroid function.

The safe inference is:

> Raised TPOAb can indicate autoimmune thyroid context even when current thyroid function appears preserved, and may be associated with increased future risk of thyroid underactivity. It does not diagnose current hypothyroidism, Hashimoto’s disease or Graves’ disease.

What must not be inferred:

- current thyroid failure;
- Hashimoto’s disease diagnosis from antibody positivity alone;
- Graves’ disease;
- need for treatment;
- personalised probability/timing of progression;
- need for repeat TPOAb titres;
- antibody titre as disease-severity measure.

## Required context

Minimum safe context:

| Context | Requirement |
|---|---|
| TPOAb | Required. |
| TSH | Required and not above range for this frame. |
| FT4 | Required and not below range for this frame. |
| TgAb | Optional corroborator; strengthens autoimmune context but not required. |
| FT3 | Optional; useful if hyperthyroid physiology or low-TSH state exists. |
| Symptoms | Contextual only; not diagnostic. |
| Known thyroid disease | Must suppress “new risk” wording. |
| Thyroid treatment | Suppress untreated natural-history wording. |
| Pregnancy/fertility | Must route to clinician-discussion/pregnancy-specific wording. |
| TRAb/TSI | Not required unless hyperthyroid biochemistry suggests Graves-pattern overactivity. |

## Clinical usefulness

This is clinically useful for HealthIQ because it answers a common consumer interpretation gap:

> “My thyroid antibodies are high, but TSH and FT4 are currently normal — what does that mean?”

It adds value because:

- it prevents overdiagnosis by explicitly saying current function appears preserved;
- it prevents under-explanation by recognising autoimmune context;
- it provides safe monitoring-oriented follow-up without treatment advice;
- it distinguishes preserved-function antibody positivity from subclinical/overt hypothyroid frames.

## Follow-up value

Safe follow-up context:

- TSH and FT4 monitoring over time may be clinically relevant.
- Clinician discussion is appropriate if new/unexpected, symptomatic, borderline TSH, pregnant/planning pregnancy, or family/personal history suggests thyroid disease.
- Repeat TPOAb testing should not be recommended routinely.
- TgAb can be contextual but should not drive the frame.
- TRAb/TSI should not be suggested routinely; only if hyperthyroid biochemistry/clinical suspicion exists.

## Disease-naming boundary

| Phrase | Decision |
|---|---|
| “thyroid autoimmunity” | Permitted with caveat. |
| “autoimmune thyroid disease may be possible” | Permitted if paired with preserved thyroid-function statement. |
| “Hashimoto’s disease” | Do not use as HealthIQ conclusion. May be mentioned only as a clinician-considered autoimmune-thyroid condition. |
| “Graves’ disease” | Not supported by this frame. |
| “risk of future thyroid dysfunction” | Permitted as “may be associated with increased risk”; no probability or timeframe. |

## Contradictions / suppressors

Suppress or redirect if:

- TSH is above range — use subclinical/overt hypothyroid context depending on FT4.
- FT4 is below range — use overt thyroid hormone deficiency context.
- TSH is suppressed or FT4/FT3 high — redirect to hyperthyroid/thyrotoxic context; consider TRAb/TSI if clinically indicated.
- Known thyroid treatment exists — do not present untreated natural-history risk.
- Pregnancy/fertility context exists — route to clinician discussion/pregnancy-specific logic.
- Assay interference/biotin context is declared and results are discordant.

## Overlap / duplication assessment

This frame is distinct from:

- TPOAb high with hypothyroid biochemistry;
- TgAb supportive autoimmune context;
- TSH/FT4 hypothyroid frames.

It should be standalone but low-intensity, because it represents preserved-function antibody positivity, which is a different consumer question from active hypothyroid biochemistry.

## Evidence strengths / limitations

### Existing HealthIQ evidence

Strong. The YAML and Pass 3 JSON define the frame clearly, and the consolidated medical review pack previously approved it with revisions and Anthony ratification.

### External evidence

- NICE NG145 recommends considering TPOAb measurement when TSH is above range and not repeating TPOAbs in adults.
- NICE evidence review states thyroid autoantibodies including TPOAb and TgAb may confirm autoimmunity in hypothyroidism and that TPOAb in particular is associated with increased progression risk in subclinical hypothyroidism.
- BTF states TPOAb is raised in Hashimoto’s/autoimmune thyroiditis and sometimes Graves’, may indicate future thyroid disease in subclinical cases, can be positive without current thyroid disease, and is rarely useful to repeat.
- ATA says high thyroid antibodies with normal TSH and FT4 do not require thyroid hormone treatment, but TSH monitoring is appropriate because low thyroid hormone may develop over time.

## Disposition

```text
PROMOTE
```

## Rationale

This frame is medically sound, clinically useful and safe for HealthIQ if tightly governed.

Promotion conditions:

1. TPOAb above lab-provided reference range.
2. TSH present and not above lab-provided reference range.
3. FT4 present and not below lab-provided reference range.
4. No current thyroid treatment context that would make natural-history wording misleading.
5. Pregnancy/fertility context routes to clinician-discussion wording.
6. No treatment advice.
7. No Hashimoto’s/Graves’ diagnosis.
8. No repeat-antibody recommendation.
9. No personalised progression probability.

---

# Cross-Frame Assessment

## 1. Should TgAb generate one, two or zero standalone HealthIQ findings?

TgAb should generate **zero standalone primary HealthIQ findings** at launch.

The two TgAb frames are medically real but should be reframed as:

- contextual evidence attached to hypothyroid-biochemistry interpretation;
- corroborating autoimmune evidence within the TPOAb euthyroid frame;
- low-prominence follow-up guidance when isolated TgAb is high and TPOAb is unavailable/discordant.

## 2. Does TgAb add sufficient value beyond TPOAb to justify independent surfacing?

Usually no.

TgAb adds value when:

- TPOAb is absent/unavailable/discordant;
- thyroid biochemistry already suggests hypothyroid physiology;
- dual-antibody positivity strengthens autoimmune context;
- a clinician may be considering autoimmune thyroiditis and needs corroborative context.

TgAb does not add enough value to justify a separate consumer headline when:

- TPOAb is positive;
- TSH/FT4 are preserved;
- no thyroid-function abnormality exists;
- known thyroid disease/treatment already explains antibodies.

## 3. Should euthyroid TPOAb positivity be standalone, contextual information, follow-up guidance, or not surfaced?

It should be a **standalone low-intensity finding**, because it is clinically meaningful, source-supported, consumer-relevant and can be worded safely.

It should not be high-prominence unless TSH/FT4 become abnormal or pregnancy/fertility context changes the clinical pathway.

## 4. Safest autoimmune-thyroid wording

Recommended wording:

> “Your thyroid antibody result may support an autoimmune thyroid context. Your current thyroid function is best understood from TSH and FT4. Antibody positivity alone does not diagnose Hashimoto’s disease or Graves’ disease, and it does not show that treatment is needed. If this is new, if symptoms are present, or if pregnancy/fertility is relevant, it is worth discussing with a clinician.”

For TPOAb euthyroid frame:

> “Raised TPO antibodies can indicate an autoimmune thyroid context even when thyroid hormone levels are currently preserved. This can be associated with a higher future risk of thyroid underactivity, but progression is not certain.”

For TgAb context:

> “Raised TgAb can support thyroid-autoimmune context, especially when other thyroid markers also point that way. On its own, it is usually not enough to explain current thyroid function or diagnose a thyroid condition.”

## 5. Are any of these frames suitable for governed promotion immediately?

Yes:

```text
signal_tpo_ab_high::inv_tpo_ab_high_euthyroid_autoimmune_risk
```

Recommended:

```text
PROMOTE
```

Not as treatment or diagnosis, but as a preserved-function autoimmune-thyroid risk/context finding.

The two TgAb frames should not be promoted as standalone findings. They should be reframed as contextual/corroborative logic.

---

# Evidence Gaps

| Evidence gap | Existing HealthIQ research sufficient? | Targeted external research required? | Further dedicated HealthIQ research required? |
|---|---:|---:|---:|
| Exact identity of TgAb Frame A | YES | NO for identity; YES for external clinical value | NO broad research required, but a product representation decision is required. |
| Exact identity of TgAb Frame B | YES | NO for identity; YES for external clinical value | NO broad research required, but a product representation decision is required. |
| Whether TgAb should be standalone | PARTLY | YES | No further medical research required; this is now a product-safety/adjudication decision. |
| Whether TPOAb euthyroid risk is valid | YES | YES, already supported by guideline/review evidence | NO. Evidence is sufficient for ratification. |
| Pregnancy/fertility handling | PARTLY | YES | YES only if HealthIQ wants pregnancy-specific logic; otherwise suppress/clinician-discussion wording. |
| Graves/Hashimoto naming | YES | YES | NO; boundaries are clear enough. |

---

# Ratification Recommendation

Anthony should ratify the following medical-governance decisions.

## Frame 1 — `signal_tgab_high::inv_tgab_high_autoimmune_hypothyroid_pattern`

```text
Recommendation: REFRAME

Ratification wording:
TgAb high with hypothyroid-biochemistry support is medically valid as contextual autoimmune-thyroid evidence, but it must not generate a standalone HealthIQ finding. It may support TSH/FT4/TPOAb-based hypothyroid interpretation, especially where TPOAb is unavailable, negative or discordant. It must not diagnose Hashimoto’s disease, Graves’ disease, current thyroid dysfunction or disease severity from TgAb alone.
```

## Frame 2 — `signal_tgab_high::inv_tgab_high_euthyroid_autoimmune_risk`

```text
Recommendation: REFRAME

Ratification wording:
TgAb high with preserved thyroid function must not generate a standalone HealthIQ finding. It may be surfaced only as low-prominence contextual/follow-up information where clinically useful, especially if TPOAb is unavailable or discordant. If TPOAb is high, the TPOAb euthyroid autoimmune-risk frame takes precedence and TgAb becomes corroborating context.
```

## Frame 3 — `signal_tpo_ab_high::inv_tpo_ab_high_euthyroid_autoimmune_risk`

```text
Recommendation: PROMOTE

Ratification wording:
TPOAb high with TSH and FT4 currently within lab-provided reference ranges is medically suitable for governed HealthIQ promotion as a low-intensity, non-diagnostic autoimmune-thyroid risk/context finding. It must state that current thyroid function appears preserved, must not diagnose Hashimoto’s disease or Graves’ disease, must not recommend treatment or repeat antibody testing, and should recommend clinician discussion where new, symptomatic, borderline, pregnant/planning pregnancy, or otherwise clinically relevant.
```

---

# Source Basis

## HealthIQ / uploaded sources

1. `THYROID_DEFERRED_SIGNAL_MEDICAL_REVIEW_PROMPT(1).md` — task authority and required structure.
2. `thyroid_antibodies_pass_3.json` — canonical Pass 3 antibody research containing:
   - `inv_tpo_ab_high_autoimmune_hypothyroid_pattern`;
   - `inv_tpo_ab_high_euthyroid_autoimmune_risk`;
   - `inv_tgab_high_autoimmune_hypothyroid_pattern`;
   - `inv_tgab_high_euthyroid_autoimmune_risk`.
3. `inv_tpo_ab_high_euthyroid_autoimmune_risk.yaml` — dedicated v3 investigation spec for the TPOAb euthyroid frame.
4. `HEALTHIQ_AI_V5_WHY_PILOT_CONSOLIDATED_MEDICAL_REVIEW(1).md` — prior Gate C consolidated medical review and Anthony ratification table.

## External medical sources used

1. NICE. **Thyroid disease: assessment and management**. NG145. Recommendations: TPOAb measurement for adults with TSH above reference range; do not repeat TPOAb in adults.
2. NICE / NCBI Bookshelf. **Tests for people with confirmed primary hypothyroidism — Evidence review D.** States that TPOAb and TgAb may help confirm autoimmunity as cause in hypothyroidism, and that TPOAb in particular is associated with increased progression risk in subclinical hypothyroidism.
3. British Thyroid Foundation. **Thyroid antibodies explained.** Updated 2025. Distinguishes TPOAb, TgAb, TRAb and TSI; notes TgAb’s limited added value beyond TPOAb in raised TSH assessment.
4. American Thyroid Association. **Hashimoto’s Thyroiditis.** Describes antibody positivity with normal TSH/FT4, monitoring TSH rather than antibodies, and no thyroid hormone treatment when thyroid function tests are normal.
5. Vargas-Uricoechea H. **The Usefulness of Thyroid Antibodies in the Diagnostic Approach to Autoimmune Thyroid Disease.** Diagnostics. 2023.
6. Gill S et al. **Evaluating the Progression to Hypothyroidism in Preconception Euthyroid Thyroid Peroxidase Antibody-Positive Women.** 2022.

---

# Final medical-governance position

```text
Frame 1 — TgAb autoimmune hypothyroid context: REFRAME
Frame 2 — TgAb euthyroid autoimmune risk: REFRAME
Frame 3 — TPOAb euthyroid autoimmune risk: PROMOTE
```

This report does not authorise implementation. The next step is Anthony ratification of these dispositions, followed by any architecture/runtime work through the governed HealthIQ process.
