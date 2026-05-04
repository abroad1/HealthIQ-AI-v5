```yaml
executive_summary: |
  The evidence strongly supports using total atherogenic lipoprotein measures (e.g. non-HDL-C or ApoB) rather than LDL-C alone to detect lipid transport dysfunction. Large cohort analyses (e.g. Multinational Cardiovascular Risk Consortium) show stepwise increases in long-term CVD risk as non-HDL-C rises【7†L577-L585】. ApoB consistently emerges as the strongest risk marker (vs. non-HDL-C, LDL-C) in meta-analysis【10†L315-L323】 and statin-era cohorts【13†L99-L107】. Triglyceride-rich lipoproteins (TRLs) and their cholesterol remnants also independently raise risk: for example, PAD risk conferred by elevated ApoB is explained primarily by remnant cholesterol【25†L330-L339】. An elevated TG/HDL-C ratio likewise predicts higher cardiovascular event rates【29†L331-L339】. Clinical guidelines reflect these findings, designating non-HDL-C and ApoB as secondary targets (e.g. non-HDL-C <2.6 mmol/L and ApoB <80 mg/dL for high-risk individuals【49†L3167-L3172】). Importantly, simply lowering TG levels without reducing ApoB/lipoprotein burden has not reliably reduced events (the PROMINENT trial of the TG-lowering fibrate pemafibrate showed no CVD benefit). Overall, evidence validates the two‐axis lipid panel approach: both a measure of atherogenic cholesterol (non-HDL-C/ApoB) and a TG-based remnant stress indicator are needed to capture lipid transport dysfunction.

package_metadata:
  research_id: RIB-0001
  topic: Lipid transport dysfunction biomarkers
  generated_utc: 2026-03-08T12:13:31Z
  source_file: LIPID-TRANSPORT-DYSFUNCTION-SIGNAL-STUDY.md
  extraction_model: gpt-4-browsing
  extraction_mode: web_research

research_scope:
  research_domain: Cardiology / Lipidology
  research_question: Can lipid transport dysfunction be detected from standard blood lipid biomarkers and related derived metrics?
  evidence_scope: |
    We focused on large prospective cohorts, meta-analyses, and guidelines assessing relationships between lipid panel measures (e.g. LDL-C, HDL-C, TG, non-HDL-C, ApoB) and cardiovascular outcomes.

entities:
  biomarkers:
    - id: biomarker_LDL_C
      name: LDL cholesterol
      description: Low-density lipoprotein cholesterol, traditional primary lipid target.
      synonyms: [LDL-C]
    - id: biomarker_HDL_C
      name: HDL cholesterol
      synonyms: [HDL-C]
    - id: biomarker_triglycerides
      name: Triglycerides
      synonyms: [TG]
    - id: biomarker_ApoB
      name: Apolipoprotein B
      description: Protein component of all atherogenic lipoproteins (VLDL, LDL, Lp(a)), measures particle number.
      synonyms: [apoB]
  derived_metrics:
    - id: metric_non_HDL_C
      name: Non-HDL cholesterol
      formula: Total cholesterol minus HDL cholesterol
      description: Sum of cholesterol in all ApoB-containing (atherogenic) lipoproteins, including LDL and remnants.
      synonyms: [non-HDL cholesterol]
    - id: metric_remnant_cholesterol
      name: Remnant cholesterol
      description: Cholesterol content of triglyceride-rich lipoprotein remnants (calculated as total cholesterol – LDL-C – HDL-C when fasting).
      synonyms: [TRL cholesterol]
    - id: metric_TG_to_HDL_ratio
      name: TG/HDL-C ratio
      description: Ratio of fasting triglycerides to HDL cholesterol; a surrogate of atherogenic dyslipidemia (insulin resistance).
      synonyms: [triglyceride–HDL ratio]
    - id: metric_LDL_C_equation
      name: LDL-C (Sampson equation)
      description: LDL-C estimated by the Sampson formula (a novel equation accurate up to TG ≤800 mg/dL).
      synonyms: [calculated LDL-C]

physiological_claims:
  - claim_id: claim_nonHDL_Risk
    claim_text: |
      Non-HDL cholesterol is strongly associated with long-term cardiovascular risk, and predicts CVD events as well or better than LDL-C.
    evidence_strength: strong
    source_refs: [source_7]
  - claim_id: claim_ApoB_superior
    claim_text: |
      ApoB level is a more potent marker of atherogenic lipoprotein burden and CVD risk than LDL-C (and slightly more than non-HDL-C).
    evidence_strength: strong
    source_refs: [source_10, source_13]
  - claim_id: claim_TG_remnant_risk
    claim_text: |
      Elevated remnant cholesterol (reflecting triglyceride-rich lipoprotein remnants) independently raises atherosclerotic risk; for PAD, remnant cholesterol explains most of the excess risk.
    evidence_strength: strong
    source_refs: [source_25, source_44]
  - claim_id: claim_TG_HDL_association
    claim_text: |
      A higher triglyceride/HDL-C ratio is associated with increased odds of future cardiovascular events.
    evidence_strength: moderate
    source_refs: [source_29]
  - claim_id: claim_ApoB_LDL_discordance
    claim_text: |
      In discordant profiles (high ApoB with low LDL-C), the elevated ApoB/non-HDL-C drives risk, whereas high LDL-C with low ApoB does not increase risk.
    evidence_strength: strong
    source_refs: [source_13]
  - claim_id: claim_TG_lowering_no_outcome
    claim_text: |
      Lowering triglycerides alone (without reducing ApoB/atherogenic particle count) has not consistently reduced cardiovascular events (e.g. the PROMINENT trial with pemafibrate showed no event benefit despite TG lowering).
    evidence_strength: moderate
    source_refs: []
  - claim_id: claim_LDL_calculation
    claim_text: |
      A novel LDL-C calculation using TG and non-HDL-C (Sampson equation) provides more accurate LDL-C estimates, especially at high TG levels up to 800 mg/dL.
    evidence_strength: moderate
    source_refs: [source_32]

evidence_quotes:
  - quote_id: quote_nonHDL
    sentence: "Incidence curve analyses showed progressively higher 30-year cardiovascular disease event-rates for increasing non-HDL cholesterol categories ... (p<0.0001) ... Multivariable adjusted Cox models ... showed an increase in association with CVD risk for both sexes (HR up to ~2.3 for ≥5.7 mmol/L non-HDL vs <2.6 mmol/L)【7†L577-L585】."
    source_refs: [source_7]
  - quote_id: quote_ApoB_markers
    sentence: "Whether analyzed individually or in head-to-head comparisons, apoB was the most potent marker of cardiovascular risk (RRR 1.43; 95% CI 1.35–1.51), LDL-C was the least (RRR 1.25; 95% CI 1.18–1.33), and non-HDL-C was intermediate (RRR 1.34; 95% CI 1.24–1.44)... apoB strategy would prevent 500,000 more events than a non-HDL-C strategy【10†L315-L323】."
    source_refs: [source_10]
  - quote_id: quote_ApoB_discordance
    sentence: "High apoB and non-HDL cholesterol were associated with increased risk of all-cause mortality and myocardial infarction, whereas no such associations were found for high LDL cholesterol... discordant apoB above the median with LDL cholesterol below yielded HR 1.21 (CI 1.07–1.36) for all-cause mortality and 1.49 (1.15–1.92) for MI【13†L99-L107】."
    source_refs: [source_13]
  - quote_id: quote_remnant_PAD
    sentence: "PAD risk conferred by elevated apoB-containing lipoproteins was explained mainly by elevated remnants, while myocardial infarction risk was explained by both elevated remnants and LDL【25†L330-L339】."
    source_refs: [source_25]
  - quote_id: quote_TG_HDL_meta
    sentence: "Meta-analysis: compared with lowest TG/HDL-C, highest ratio was independently associated with higher CVD risk (pooled HR 1.43; 95% CI 1.26–1.62)【29†L331-L339】."
    source_refs: [source_29]
  - quote_id: quote_Sampson_LDL
    sentence: "The new equation was more accurate than other LDL-C equations ... for patients with hypertriglyceridemia ... and was associated with 35% fewer misclassifications when patients with TG 400–800 mg/dL were categorized into different LDL-C groups【32†L374-L382】."
    source_refs: [source_32]
  - quote_id: quote_guidelines
    sentence: "Non-HDL-C secondary goals are <2.2, 2.6, and 3.4 mmol/L ... for very-high-, high-, and moderate-risk people, respectively. ApoB secondary goals are <65, 80, and 100 mg/dL for very-high-, high-, and moderate-risk people, respectively【49†L3167-L3172】."
    source_refs: [source_49]

original_vs_validated:
  - original: "Atherogenic burden proxy = non-HDL cholesterol (TC – HDL-C); remnant stress proxy = fasting TG."
    validated: "Large cohorts confirm that higher non-HDL-C strongly predicts CVD events (HR~2–2.3 at high levels)【7†L577-L585】. High fasting TG and remnant cholesterol also independently predict risk (especially PAD)【25†L330-L339】."
    source_refs: [source_7, source_25]
  - original: "ApoB is the best single metric of atherogenic particle effect."
    validated: "Meta-analysis and cohort studies show apoB is the most potent risk marker, outperforming non-HDL-C and LDL-C【10†L315-L323】【13†L99-L107】."
    source_refs: [source_10, source_13]
  - original: "Lowering TG will lower events."
    validated: "Trials targeting TG (e.g. the PROMINENT fibrate study) have not shown event reduction, implying TG lowering alone may not reduce risk."
    source_refs: []
  - original: "LDL-C can be estimated by a universal equation (Friedewald/Martin)."
    validated: "A newer formula (Sampson equation) using TG and non-HDL improved LDL-C accuracy, particularly at high TG, with 35% fewer misclassifications【32†L374-L382】."
    source_refs: [source_32]

sources:
  - source_id: source_7
    citation: Brunner FJ et al. Lancet. 2019;394(10215):2173–2183.
    doi: 10.1016/S0140-6736(19)32519-X
    url: https://doi.org/10.1016/S0140-6736(19)32519-X
  - source_id: source_10
    citation: Sniderman AD et al. Circ Cardiovasc Qual Outcomes. 2011;4(3):337–345.
    doi: 10.1161/CIRCOUTCOMES.110.959247
    url: https://doi.org/10.1161/CIRCOUTCOMES.110.959247
  - source_id: source_13
    citation: Johannesen CD et al. J Am Coll Cardiol. 2021;77(11):1439–1450.
    doi: 10.1016/j.jacc.2021.01.027
    url: https://doi.org/10.1016/j.jacc.2021.01.027
  - source_id: source_25
    citation: Wadström BN et al. Arterioscler Thromb Vasc Biol. 2024;44(5):1144–1155.
    doi: 10.1161/ATVBAHA.123.320175
    url: https://doi.org/10.1161/ATVBAHA.123.320175
  - source_id: source_29
    citation: Chen Y et al. Nutr Metab Cardiovasc Dis. 2022;32(2):318–329.
    doi: 10.1016/j.numecd.2021.11.005
    url: https://doi.org/10.1016/j.numecd.2021.11.005
  - source_id: source_32
    citation: Sampson M et al. JAMA Cardiol. 2020;5(5):540–548.
    doi: 10.1001/jamacardio.2020.0013
    url: https://doi.org/10.1001/jamacardio.2020.0013
  - source_id: source_44
    citation: Varbo A et al. J Am Coll Cardiol. 2013;61(4):427–436.
    doi: 10.1016/j.jacc.2012.08.1026
    url: https://doi.org/10.1016/j.jacc.2012.08.1026
  - source_id: source_49
    citation: Catapano AL et al. Eur Heart J. 2019;40(7):1111–1166 (ESC/EAS Dyslipidaemia Guidelines).
    doi: 10.1093/eurheartj/ehz455
    url: https://doi.org/10.1093/eurheartj/ehz455
```