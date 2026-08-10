# Thyroid Deferred Signal Medical Review

**Work type:** Medical research / medical-governance review only  
**Scope:** `signal_tgab_high` Frame A, `signal_tgab_high` Frame B, and `signal_tpo_ab_high::inv_tpo_ab_high_euthyroid_autoimmune_risk`  
**Product context:** HealthIQ AI secondary consumer interpretation of blood-test results, with clinically useful, non-diagnostic explanation and appropriate follow-up guidance  
**Runtime / implementation status:** Not assessed as authority  
**Production decision status:** Not made here; requires Anthony ratification after GPT Head of Medical Research review

---

# Executive Recommendation

| Frame | Recommendation | Confidence | One-line rationale |
|---|---|---:|---|
| TgAb high — autoimmune hypothyroid-context concept | REFRAME | MODERATE | TgAb can support autoimmune thyroid context, but is weaker than TPOAb and should not generate a standalone HealthIQ finding; use as contextual evidence attached to TSH/FT4/TPOAb interpretation. |
| TgAb high — euthyroid autoimmune-risk concept | REFRAME | MODERATE | TgAb positivity alone is clinically real but lower-value and more anxiety-prone than TPOAb; use as contextual/follow-up evidence, not a standalone consumer finding. |
| TPOAb high — euthyroid autoimmune-risk frame | PROMOTE | MODERATE-HIGH | Euthyroid TPOAb positivity is medically meaningful as future thyroid-dysfunction risk context when TSH and FT4 are currently within range, provided wording is cautious and non-diagnostic. |

## Critical source-authority note

The prompt required the exact existing TgAb frames to be identified from canonical HealthIQ research artefacts before evaluation. The available HealthIQ materials did **not** expose a validated investigation-spec v3 or accepted canonical Pass_3 source for `signal_tgab_high`. Instead, available governance material identifies `signal_tgab_high` as a research gap / legacy-only item, with no Wave 1 TgAb frame compiled or ratified.

Therefore, this report does **not** treat any named TgAb frame as already canonical. It reviews the two medically plausible TgAb concepts that appear to be under dispute:

1. TgAb high as autoimmune context supporting hypothyroid biochemistry.
2. TgAb high as euthyroid autoimmune-risk context.

The disposition for both is `REFRAME`, not `PROMOTE`, because the underlying information is useful but should not be represented as independent standalone HealthIQ findings without a stronger canonical source and product justification.

---

# Frame 1 — TgAb high [autoimmune hypothyroid-context concept]

## Canonical HealthIQ source reviewed

### Existing HealthIQ evidence

- `signal_tgab_high` is listed in the thyroid-axis completion wave but explicitly as a research/specification gap rather than a confirmed spec-ready target.
- ARCH-CONV-A Wave 1 materials state that `signal_tgab_high` remained blocked / not submitted because of research gaps.
- The available frame tree does not provide a confirmed TgAb canonical investigation-spec frame in the material reviewed.
- No validated `inv_tgab_high_*` source was available in the supplied/searchable material.

### Source-status conclusion

Existing HealthIQ evidence is **insufficient to identify an exact canonical TgAb Frame A**.

For medical review purposes only, the likely frame is interpreted as:

> Raised TgAb as thyroid-autoimmune context that may support an autoimmune explanation when thyroid biochemistry already suggests hypothyroid physiology.

This is not treated as an approved HealthIQ frame.

## Exact medical interpretation

Thyroglobulin antibodies are thyroid autoantibodies directed against thyroglobulin, a thyroid protein involved in thyroid hormone production. TgAb can be present in autoimmune thyroid disease, especially Hashimoto-pattern autoimmune thyroiditis, but it is generally less clinically central than TPOAb for routine hypothyroid evaluation.

The medically safe inference is:

> Raised TgAb may support an autoimmune thyroid context, particularly if TSH and FT4 already show a hypothyroid or subclinical hypothyroid biochemical pattern.

The result must not be interpreted as:

- a diagnosis of Hashimoto's disease;
- evidence of Graves' disease;
- evidence of current thyroid dysfunction;
- a treatment indication;
- a reason to monitor TgAb serially.

## Required context

Minimum context for meaningful interpretation:

- TSH — required.
- FT4 — required.
- TPOAb — strongly recommended.
- TgAb — primary reviewed marker.
- Known thyroid disease — required if declared.
- Thyroid treatment — required if declared.
- Symptoms — optional explanatory context only; not required for antibody interpretation.
- Pregnancy / fertility context — important modifier; should route to clinician-discussion wording rather than a routine consumer frame.
- TRAb / TSI — not required unless the clinical question is Graves-pattern hyperthyroidism or current thyrotoxicosis.

## Clinical usefulness for HealthIQ

TgAb has some explanatory value, but mainly as a **context marker**.

It may help explain:

- why raised TSH / low or borderline FT4 may be autoimmune in origin;
- why TPOAb-negative but TgAb-positive users may still have evidence of thyroid autoimmunity;
- why clinician review may consider autoimmune thyroid disease if thyroid function markers are also altered.

However, as a standalone HealthIQ finding it has limited consumer value because:

- TgAb alone does not establish disease;
- repeat TgAb levels rarely change management;
- TPOAb usually provides the stronger autoimmune-thyroid signal;
- a standalone TgAb finding risks over-labelling and anxiety.

## Follow-up value

Reasonable non-diagnostic follow-up wording:

- If TSH is above range or FT4 is below range: “This may be worth discussing with a clinician as part of thyroid-function review.”
- If TPOAb has not been measured: “TPO antibodies are often used alongside thyroid function markers to clarify autoimmune thyroid context.”
- If hyperthyroid biochemistry is present: “TRAb/TSI may be relevant if Graves-pattern thyroid overactivity is suspected.”

Routine repeat TgAb testing should not be recommended.

## Disease-naming boundary

| Wording | Boundary |
|---|---|
| “thyroid autoimmunity” | Safe only as qualified context: “may support thyroid-autoimmune context.” |
| “autoimmune thyroid disease may be possible” | Safe only with TSH/FT4 context and clinician-review wording. |
| “Hashimoto's disease” | Unsafe as a standalone TgAb inference. May be mentioned only as an example clinicians may consider when hypothyroid biochemistry is present. |
| “Graves' disease” | Unsafe from TgAb. TRAb/TSI is the relevant antibody context for Graves-pattern disease. |
| “risk of future thyroid dysfunction” | Weak from TgAb alone; stronger for TPOAb. Use cautiously, if at all. |

## Contradictions / suppressors

Suppress or redirect this frame if:

- TSH and FT4 are clearly euthyroid and TPOAb is negative or unavailable: no standalone hypothyroid-autoimmune frame.
- TSH is suppressed with raised FT4/FT3: redirect to hyperthyroid / thyrotoxicosis-context review; TgAb is not Graves-specific.
- TRAb/TSI positive: Graves-pattern antibody context takes precedence.
- Current thyroid treatment is declared: interpretation becomes treatment/monitoring context and should not infer untreated disease.
- Pregnancy / fertility context is present: clinician review wording only; do not offer routine consumer conclusion.
- TgAb is measured because of thyroid-cancer surveillance: suppress this consumer autoimmune frame; TgAb has a distinct role as an interference/monitoring issue for thyroglobulin surveillance.

## Overlap / duplication assessment

This concept substantially overlaps with:

- TPOAb high with hypothyroid biochemistry;
- TSH high / FT4 low primary hypothyroid biochemistry;
- TPOAb euthyroid autoimmune-risk context.

TgAb adds some value when TPOAb is absent, negative or discordant, but not enough to justify an independent standalone finding.

## Evidence strengths / limitations

### Existing HealthIQ evidence

Insufficient to identify a canonical Frame A.

### External evidence

- NICE evidence review states that thyroid autoantibodies, including TPOAb and TgAb, may be useful to confirm autoimmunity as the cause in a patient with hypothyroidism; it also states that there was uncertainty about which antibodies should be tested and when testing should be repeated.
- British Thyroid Foundation states that TgAb is sometimes raised in Hashimoto's thyroiditis; TPOAb is raised in Hashimoto's/autoimmune thyroiditis and sometimes Graves' disease; TRAb is raised in Graves' disease.
- American Thyroid Association states that positive TPO and/or Tg antibodies in a patient with hypothyroidism can support diagnosis of Hashimoto's thyroiditis, but TSH and FT4 are what tell us about actual thyroid function.

### Limitation

Most practical guidance centres TPOAb and thyroid function markers. TgAb is generally adjunctive, not primary.

## Disposition

```text
REFRAME
```

## Rationale

The medical information is valid but should be reframed as **contextual evidence attached to TSH/FT4/TPOAb thyroid-function interpretation**, not as a standalone HealthIQ finding.

Recommended reframe:

> TgAb high should be represented as contextual thyroid-autoimmune evidence when thyroid biochemistry is already outside the lab reference range or when TPOAb is unavailable/discordant. It should not fire as an independent finding.

---

# Frame 2 — TgAb high [euthyroid autoimmune-risk concept]

## Canonical HealthIQ source reviewed

### Existing HealthIQ evidence

No exact canonical HealthIQ TgAb euthyroid-risk frame was identified in the accessible material. Available architecture sources identify `signal_tgab_high` as legacy-only / no confirmed investigation-spec authority, and Wave 1 thyroid materials explicitly note TgAb research gaps.

### Source-status conclusion

Existing HealthIQ evidence is **insufficient to identify an exact canonical TgAb Frame B**.

For medical review purposes only, the likely frame is interpreted as:

> Raised TgAb in a person whose available TSH and thyroid hormone markers are otherwise euthyroid, considered as possible autoimmune thyroid context or future-risk context.

This is not treated as an approved HealthIQ frame.

## Exact medical interpretation

Raised TgAb in a euthyroid person may indicate thyroid autoimmunity, but the finding has weaker standalone interpretive value than TPOAb. It does not establish Hashimoto's disease, Graves' disease, current hypothyroidism or future progression.

The strongest medically safe inference is:

> Raised TgAb may represent thyroid-autoimmune activity, but if TSH and FT4 are currently within range, this does not establish current thyroid dysfunction.

## Required context

Minimum context:

- TSH — required.
- FT4 — required.
- TPOAb — strongly recommended.
- TgAb — primary reviewed marker.
- FT3 — optional; useful if thyrotoxicosis context exists.
- Known thyroid disease and treatment — required if declared.
- Pregnancy/fertility context — important modifier.
- TRAb/TSI — only relevant if TSH is low and FT4/FT3 suggest Graves-pattern hyperthyroidism.

## Clinical usefulness for HealthIQ

Standalone consumer usefulness is low to moderate.

Potential value:

- explains why thyroid antibody positivity can exist before thyroid-function change;
- encourages interpretation with TSH/FT4 rather than antibody level alone;
- may support a monitoring discussion if there are symptoms, family history, pregnancy planning or prior borderline thyroid function.

Risks:

- overdiagnosis of Hashimoto's;
- unnecessary anxiety;
- duplicate information when TPOAb is already high;
- little actionable value if TSH/FT4 are currently within range and no pregnancy/fertility/symptom context exists.

## Follow-up value

Safe follow-up wording:

- “If this is a new finding, it may be worth discussing with a clinician, especially if you have thyroid symptoms, a family history of thyroid disease, are pregnant or planning pregnancy, or if TSH/FT4 are borderline.”
- “Routine repeat TgAb testing is usually not useful; TSH and FT4 are more useful for monitoring thyroid function over time.”

No routine recommendation for TRAb/TSI unless thyroid function suggests hyperthyroidism or Graves-pattern disease.

## Disease-naming boundary

| Wording | Boundary |
|---|---|
| “thyroid autoimmunity” | Safe only as a qualified context phrase. |
| “autoimmune thyroid disease may be possible” | Safe only with careful caveat that thyroid function is currently not showing overt dysfunction. |
| “Hashimoto's disease” | Unsafe from TgAb alone in a euthyroid person. |
| “Graves' disease” | Unsafe from TgAb; TRAb/TSI and thyroid-function context are required. |
| “risk of future thyroid dysfunction” | Too strong from TgAb alone; use only as “may be worth monitoring thyroid function over time,” especially if TPOAb or TSH risk context also exists. |

## Contradictions / suppressors

Suppress standalone TgAb euthyroid-risk framing if:

- TPOAb is also high: prefer the TPOAb euthyroid autoimmune-risk frame, with TgAb as supporting context.
- TSH is above range or FT4 is below range: redirect to hypothyroid-biochemistry context.
- TSH is suppressed or FT4/FT3 high: redirect to hyperthyroid/thyrotoxicosis context; consider TRAb/TSI if clinically appropriate.
- The test was ordered for thyroid-cancer follow-up: TgAb has a different meaning and may interfere with thyroglobulin interpretation.
- Pregnancy/fertility context is present: use clinician-discussion wording; do not generate an independent consumer finding.
- Known thyroid disease/treatment is declared: avoid implying new disease.

## Overlap / duplication assessment

This frame overlaps heavily with TPOAb euthyroid autoimmune-risk. It adds insufficient value as a separate consumer-visible finding if TPOAb is present.

If TPOAb is absent and TgAb alone is high, the result may still be worth contextualising, but safest representation is a **low-prominence antibody-context note**, not a standalone finding.

## Evidence strengths / limitations

### Existing HealthIQ evidence

Insufficient to identify a canonical Frame B.

### External evidence

- ATA notes that TSH and FT4 tell us about actual thyroid function and that antibody levels over time are not helpful for detecting hypothyroidism development or treatment response.
- ATA Hashimoto material states that high thyroid antibodies with normal thyroid function tests do not require thyroid hormone treatment, but TSH monitoring over time is relevant.
- BTF states TgAb is sometimes raised in Hashimoto's thyroiditis but does not position TgAb as a strong standalone consumer-risk marker.

## Disposition

```text
REFRAME
```

## Rationale

The underlying medical information is useful but the current representation should become **contextual evidence / follow-up guidance**, not a separate standalone finding.

Recommended reframe:

> TgAb high with euthyroid TSH/FT4 should not generate a standalone HealthIQ finding. It may appear as a low-prominence antibody-context note, especially when TPOAb is absent or discordant, with wording focused on monitoring thyroid function rather than naming disease.

---

# Frame 3 — TPOAb euthyroid autoimmune-risk

## Canonical HealthIQ source reviewed

### Existing HealthIQ evidence

The available HealthIQ review pack identifies:

- activation key: `signal_tpo_ab_high::inv_tpo_ab_high_euthyroid_autoimmune_risk`;
- source package: `pkg_kb59_tpo_ab_high_euthyroid_autoimmune_risk`;
- investigation-spec hypotheses:
  - `hyp_euthyroid_autoimmune_thyroid_risk`;
  - `hyp_future_primary_hypothyroid_progression_risk`;
- current status at that time: pending GPT / Anthony medical review, not approved.

Available frame-tree governance also identifies the frame as:

- `frame_kb59_tpo_ab_high_euthyroid_autoimmune_risk`;
- `pass3_frame_indexed_pending_why_review`;
- promotion state `deferred`;
- clinical adjudication `blocked_pending_medical_review`;
- not diagnostic / not Anthony-ratified.

### Source-status conclusion

Unlike TgAb, this frame has identifiable HealthIQ canonical/package-level research context and a named activation key. It is suitable for medical-governance review.

## Exact medical interpretation

TPOAb positivity indicates immune recognition of thyroid peroxidase and is a common marker of autoimmune thyroid disease. In a person whose TSH and FT4 are currently within the lab reference range, high TPOAb may indicate autoimmune thyroid activity before overt thyroid dysfunction is present.

The medically safe inference is:

> High TPOAb with currently euthyroid thyroid function may support autoimmune thyroid context and may be associated with increased risk of future thyroid dysfunction, but it does not establish current hypothyroidism, Hashimoto's disease or a need for treatment.

## Required context

Minimum safe context:

- TPOAb high — required.
- TSH present and not above the lab reference range — required for this euthyroid frame.
- FT4 present and not below the lab reference range — required.
- FT3 — optional; useful if thyrotoxicosis/hyperthyroid context exists.
- TgAb — optional supporting context, not required.
- Known thyroid disease — required if declared.
- Thyroid medication — required if declared.
- Pregnancy / fertility context — must modify wording and encourage clinician discussion.
- Symptoms — optional explanatory context, not sufficient for diagnosis.
- TRAb/TSI — not required unless thyroid function suggests Graves-pattern overactivity.

## Clinical usefulness for HealthIQ

This frame has meaningful consumer value because it can explain a common situation:

- “my antibodies are high but TSH/FT4 are currently within range.”

It can help prevent both overreaction and dismissal:

- not a diagnosis;
- not a treatment instruction;
- not “nothing”;
- useful as a thyroid-function monitoring context.

This provides value beyond TSH/FT4 alone because TPOAb positivity can explain why periodic thyroid-function monitoring may be reasonable even when current thyroid function is preserved.

## Follow-up value

Safe follow-up guidance:

- Discuss with a clinician if new, unexpected, symptomatic, pregnant/planning pregnancy, or if TSH/FT4 are borderline.
- Future monitoring should focus on thyroid function markers, especially TSH and FT4, not repeated antibody titres.
- TRAb/TSI is not routine for this euthyroid TPOAb frame; it becomes relevant if TSH is low and FT4/FT3 suggest Graves-pattern thyroid overactivity.

## Disease-naming boundary

| Wording | Boundary |
|---|---|
| “thyroid autoimmunity” | Safe with qualification: “may support thyroid-autoimmune context.” |
| “autoimmune thyroid disease may be possible” | Safe if paired with “thyroid function is currently not showing overt dysfunction.” |
| “Hashimoto's disease” | Too strong for antibody positivity alone in HealthIQ consumer wording. |
| “Graves' disease” | Unsafe from TPOAb euthyroid positivity; TRAb/TSI and hyperthyroid biochemistry are relevant. |
| “risk of future thyroid dysfunction” | Safe with qualification: “may be associated with increased risk” / “may be worth monitoring thyroid function over time.” |

## Contradictions / suppressors

Suppress or redirect this frame if:

- TSH is above the lab reference range: redirect to hypothyroid / subclinical hypothyroid biochemistry context; TPOAb may support autoimmune explanation.
- FT4 is below range: redirect to overt hypothyroid biochemistry context.
- TSH is suppressed or FT4/FT3 high: redirect to hyperthyroid/thyrotoxicosis context; TPOAb is not Graves-specific.
- Known thyroid treatment is present: avoid interpreting as untreated natural-history risk.
- Pregnancy/fertility context is present: do not offer generic monitoring only; advise clinician/midwife/GP discussion.
- Biotin use or assay interference is declared: add assay caveat or suppress if discordant.

## Overlap / duplication assessment

This frame is distinct from:

- TPOAb high supporting hypothyroid biochemistry, where TSH is above range and/or FT4 is low;
- TSH high hypothyroid biochemistry;
- FT4 low thyroid hormone deficiency;
- TgAb-only contextual evidence.

It should remain separate because the consumer question and wording are different:

- TPOAb + hypothyroid biochemistry: “autoimmune context may help explain reduced thyroid output.”
- TPOAb + euthyroid function: “immune marker present, but current thyroid function appears preserved; monitoring context.”

## Evidence strengths / limitations

### Existing HealthIQ evidence

Sufficient to identify the frame and its intended hypotheses, but not sufficient alone for final medical promotion. External guideline/literature review was required.

### External evidence

- NICE NG145 recommends considering TPOAb measurement for adults with TSH above the reference range and does not recommend repeat TPOAb testing.
- NICE evidence review states that TPOAb, in particular, is associated with increased risk of progression to overt hypothyroidism in subclinical hypothyroidism.
- ATA states that TSH and FT4 tell us actual thyroid function and that following antibody levels over time is not helpful for detecting development of hypothyroidism or response to therapy.
- ATA Hashimoto material states that high thyroid antibodies with normal thyroid function do not require thyroid hormone treatment, but TSH monitoring is appropriate because thyroid hormone levels may fall over time.
- More recent cohort evidence in initially euthyroid antibody-positive patients identifies TPOAb level, baseline TSH, FT4 and age as independent risk factors for progression to hypothyroidism, supporting a risk-context rather than diagnosis frame.

## Disposition

```text
PROMOTE
```

## Rationale

This is medically valid and useful for HealthIQ’s purpose if the frame is tightly constrained to euthyroid thyroid-function context and non-diagnostic wording.

Promotion should be bounded by these medical conditions:

1. TPOAb above the lab-provided reference range.
2. TSH present and not above the lab-provided reference range.
3. FT4 present and not below the lab-provided reference range.
4. No current thyroid medication context that would make natural-history risk wording misleading.
5. Pregnancy/fertility context routes to clinician-discussion wording.
6. No disease label, no treatment advice, no repeat-antibody recommendation.

---

# Cross-Frame Assessment

## 1. Should TgAb generate one, two or zero standalone HealthIQ findings?

TgAb should generate **zero standalone HealthIQ findings** at this stage.

It should be represented as:

- contextual evidence attached to hypothyroid-biochemistry interpretation;
- low-prominence autoimmune-thyroid context when TPOAb is unavailable/negative but TgAb is high;
- follow-up guidance only where TSH/FT4, symptoms, family history or pregnancy/fertility context make it useful.

## 2. Does TgAb add sufficient value beyond TPOAb to justify independent surfacing?

No, not as a standalone finding.

TgAb adds value mainly when:

- TPOAb is unavailable;
- TPOAb is negative but TgAb is high;
- thyroid biochemistry already suggests hypothyroid physiology;
- a clinician may be considering autoimmune thyroid disease despite discordant antibodies.

When TPOAb is high, TgAb is usually supporting context, not a separate finding.

## 3. Should euthyroid TPOAb positivity be a standalone finding, contextual information, follow-up guidance, or not surfaced?

It should be a **standalone low-intensity HealthIQ finding**, provided it is framed as:

- autoimmune-thyroid context;
- preserved current thyroid function;
- possible future monitoring relevance;
- not Hashimoto's disease;
- not treatment advice.

This is more than contextual information because it directly answers a common consumer question: “My antibody is high but my thyroid function is currently normal — what does that mean?”

## 4. What is the medically safest way for HealthIQ to discuss autoimmune thyroid disease without diagnosing Hashimoto's or Graves' from insufficient evidence?

Recommended safest general wording:

> “Your thyroid antibody result may support an autoimmune thyroid context. Antibodies can be present before thyroid hormone levels change, and thyroid function is best assessed using TSH and FT4. This result does not diagnose Hashimoto's disease or Graves' disease on its own. If this is a new finding, if you have symptoms, or if you are pregnant or planning pregnancy, it is worth discussing with a clinician.”

Specific disease-name rules:

- Hashimoto's: do not use as a direct HealthIQ conclusion from antibodies alone.
- Graves': do not use unless TRAb/TSI and hyperthyroid biochemical context support clinician-style differential discussion.
- Autoimmune thyroid disease: use only as qualified possibility/context, not diagnosis.
- Future dysfunction risk: strongest for TPOAb, not TgAb alone.

## 5. Are any of these frames suitable for governed promotion immediately?

Only one:

```text
signal_tpo_ab_high::inv_tpo_ab_high_euthyroid_autoimmune_risk
```

Recommended status:

```text
PROMOTE, with strict medical wording and context gates
```

TgAb frames are not suitable for governed promotion as standalone findings. They should be reframed as contextual evidence/follow-up modifiers.

---

# Evidence Gaps

| Evidence gap | Existing HealthIQ research sufficient? | Targeted external research required? | Further dedicated HealthIQ research required? |
|---|---:|---:|---:|
| Exact canonical identity of TgAb Frame A | NO | YES | YES — identify or author canonical research/spec if any TgAb context is to be retained. |
| Exact canonical identity of TgAb Frame B | NO | YES | YES — same as above. |
| Whether TgAb-only positivity has sufficient future-risk value for consumer surfacing | NO | YES | YES if HealthIQ wants a TgAb-only follow-up note. |
| Whether euthyroid TPOAb positivity is safe/useful for consumer interpretation | PARTLY | YES | NO further broad research required; proceed to adjudication/ratification. |
| Graves-vs-Hashimoto follow-up antibody handling | PARTLY | YES | NO for this decision; TRAb/TSI should remain conditional on hyperthyroid clinical question. |
| Pregnancy/fertility handling for antibody-positive euthyroid users | PARTLY | YES | YES if HealthIQ wants pregnancy-specific logic; otherwise suppress/clinician-discussion wording. |

---

# Ratification Recommendation

Anthony should ratify the following medical-governance decisions.

## Frame 1 — TgAb high autoimmune hypothyroid-context concept

```text
Recommendation: REFRAME
Ratification wording:
TgAb high must not generate a standalone HealthIQ finding. It may be used as contextual thyroid-autoimmune evidence attached to TSH/FT4/TPOAb interpretation, especially where hypothyroid biochemistry is present or TPOAb is unavailable/discordant. It must not diagnose Hashimoto's disease, Graves' disease or current thyroid dysfunction.
```

## Frame 2 — TgAb high euthyroid autoimmune-risk concept

```text
Recommendation: REFRAME
Ratification wording:
TgAb high with euthyroid thyroid-function markers must not generate a standalone HealthIQ finding. It may be surfaced only as low-prominence contextual/follow-up information if clinically useful, with wording focused on thyroid-function monitoring rather than disease naming. If TPOAb is also high, the TPOAb euthyroid frame takes precedence and TgAb becomes supporting context only.
```

## Frame 3 — TPOAb high euthyroid autoimmune-risk frame

```text
Recommendation: PROMOTE
Ratification wording:
TPOAb high with TSH and FT4 currently within lab-provided reference ranges is medically suitable for governed HealthIQ promotion as a low-intensity, non-diagnostic autoimmune-thyroid risk/context finding. It must state that current thyroid function appears preserved, must not diagnose Hashimoto's disease or Graves' disease, must not recommend treatment, and should recommend clinician discussion where new, symptomatic, borderline, pregnant/planning pregnancy, or otherwise clinically relevant.
```

---

# References

## HealthIQ / project sources reviewed

1. `THYROID_DEFERRED_SIGNAL_MEDICAL_REVIEW_PROMPT(1).md` — task authority for this medical review.
2. `ARCH-CONV-A_medical_review_wave_plan.md` — identifies Wave 1 thyroid completion and classifies `signal_tgab_high` as no confirmed spec / research gap.
3. `ARCH-CONV-A_wave1_thyroid_medical_review_pack.md` — states Wave 1 blocked/not submitted for `signal_tgab_high` because of research gaps.
4. `biomarker_medical_frame_tree.md` — generated frame tree, not source of truth; identifies TPOAb euthyroid frame as deferred/pending WHY review and TPOAb hypothyroid frame as accepted with TSH gate.
5. `HEALTHIQ_AI_V5_WHY_PILOT_CONSOLIDATED_MEDICAL_REVIEW.md` — identifies `signal_tpo_ab_high::inv_tpo_ab_high_euthyroid_autoimmune_risk` and its hypotheses.

## External medical sources

1. NICE. **Thyroid disease: assessment and management**. NICE Guideline NG145. Recommendations and evidence review D. 2019, updated.  
   https://www.nice.org.uk/guidance/ng145  
   https://www.ncbi.nlm.nih.gov/books/NBK577225/

2. British Thyroid Foundation. **Thyroid function tests**. Endorsed by the British Thyroid Association.  
   https://www.btf-thyroid.org/thyroid-function-tests

3. American Thyroid Association. **Thyroid Function Tests**.  
   https://www.thyroid.org/thyroid-function-tests/

4. American Thyroid Association. **Hashimoto’s Thyroiditis**.  
   https://www.thyroid.org/hashimotos-thyroiditis/

5. Mayo Clinic Laboratories. **Thyroglobulin Antibody, Serum**.  
   https://prd1.mayocliniclabs.com/test-catalog/overview/84382

6. Frontiers in Endocrinology / PubMed. **Analysis of risk factors for hypothyroidism in initially euthyroid patients with positive thyroid autoantibodies: a multicenter retrospective cohort study**. 2026. PMID: 42232752.  
   https://pubmed.ncbi.nlm.nih.gov/42232752/

---

# Final medical-governance position

```text
TgAb high should not be promoted as one or two standalone consumer findings.
TgAb high should be reframed as contextual autoimmune-thyroid evidence / follow-up guidance.
TPOAb high euthyroid autoimmune-risk should be promoted with strict wording and context gates.
```

This report does not authorise implementation. The next step is Anthony ratification of the above dispositions, followed by any architecture/runtime work through the governed HealthIQ process.
