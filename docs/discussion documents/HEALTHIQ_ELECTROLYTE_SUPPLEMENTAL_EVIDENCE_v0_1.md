---
document_id: HEALTHIQ-ELECTROLYTE-SUPPLEMENTAL-EVIDENCE-001
title: HealthIQ Supplemental Electrolyte Evidence — Hypokalaemia, Hypernatraemia, Hypocalcaemia
version: "0.1"
closes: RE-U2, RE-U3, RE-U4
governing_contract: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.6
status: DRAFT_FOR_HMR_REVIEW
implementation_status: NOT_AUTHORISED
---

# Supplemental Electrolyte Evidence v0.1

Closes the three blocking gaps in workstream C. **No band below is derived by analogy from potassium-high, sodium-low or calcium-high rules.** Each direction was researched independently against UK sources.

**Evidence labels:** `[E]` evidence-supported · `[C]` accepted clinical convention · `[J]` HealthIQ clinical judgement · `[U]` unresolved.

---

## 1. Hypokalaemia (RE-U2 — CLOSED at `[E]`)

### 1.1 Severity bands

| Band | Threshold | Class |
|---|---|---|
| Mild | K⁺ 3.0–3.4 mmol/L | `[E]` |
| Moderate | K⁺ 2.5–2.9 mmol/L | `[E]` |
| Severe | K⁺ <2.5 mmol/L | `[E]` |

Consistent across multiple independent UK NHS trust and health board guidelines: NHS Gloucestershire, Royal Cornwall, NHS Grampian, RUH Bath and York.

### 1.2 Urgency time bands

| Threshold | Band | Rationale | Source |
|---|---|---|---|
| K⁺ <2.5 | **Same day** | Severe hypokalaemia can cause life-threatening arrhythmia and respiratory muscle weakness. UK laboratory practice telephones all results below 2.5 to the requesting location or out-of-hours service, and urgent admission should be considered | RUH Bath PATH-017; York Hospitals `[E]` |
| K⁺ 2.5–2.9 | **Within days** | Duty biochemists review results below 2.9; results 2.5–2.8 may be telephoned at the clinical biochemist's discretion — i.e. clinically actionable but not automatically same-day | York Hospitals `[E]` |
| K⁺ 3.0–3.4 | **Within weeks** | Usually asymptomatic; managed by treating the underlying cause, reviewing diuretics, and repeat testing with creatinine, sodium and bicarbonate | Gloucestershire; GPnotebook `[E]` |

### 1.3 Context and artefact caveats

| ID | Caveat | Class |
|---|---|---|
| K-LOW-C1 | **Digoxin and underlying cardiac disease raise risk at any degree of hypokalaemia.** Even mild hypokalaemia carries increased risk in these groups | `[E]` |
| K-LOW-C2 | Magnesium deficiency exacerbates potassium wasting and makes hypokalaemia refractory. Magnesium should be requested with any hypokalaemia | `[E]` |
| K-LOW-C3 | Commonly drug-induced — thiazide and loop diuretics, steroids, beta-2 agonists, insulin, theophylline | `[E]` |
| K-LOW-C4 | In heart failure and post-MI, a target of at least 4.0 mmol/L is advocated, so an "in-range" potassium of 3.6 may be inadequate in these groups. Contract §3.1 in-range-findings rule applies | `[C]` |
| K-LOW-C5 | Unlike hyperkalaemia, spurious hypokalaemia is uncommon; sample handling artefact acts in the opposite direction | `[C]` |

### 1.4 Safety without symptoms or examination

**Partially safe — and this is the most important qualification in this document.**

York's guidance states explicitly that the biochemical severity scale **is arbitrary and serves only as a guide**, and that the severity of hypokalaemia is predominantly defined by symptoms and ECG changes `[E]`.

| Band | Safe without symptoms/ECG? | Required behaviour |
|---|---|---|
| <2.5 | **Yes, to escalate.** UK labs telephone these regardless of clinical detail | Same-day band may fire on the value alone |
| 2.5–2.9 | **Safe to flag, not to grade.** The band is defensible; the true severity is not determinable | Within-days band fires; output must state that severity depends on symptoms and ECG, which HealthIQ has not assessed |
| 3.0–3.4 | **Safe to flag, not to reassure** | Within-weeks band fires; **reassurance is prohibited** where K-LOW-C1 or K-LOW-C4 groups cannot be excluded |

**K-LOW-SAFE-1 `[E]`** — HealthIQ must never state or imply that a hypokalaemia is mild in consequence. It may state the concentration band. The consequence depends on cardiac status, digoxin use and ECG, none of which HealthIQ holds. **Declared unsafe-without-context under contract §27 for the 3.0–3.4 band only, on test (c): missing cardiac and digoxin status materially changes the action category.**

---

## 2. Hypernatraemia (RE-U3 — CLOSED at `[C]`, with a flag)

### 2.1 Evidence position — weaker than the other two, stated plainly

**No UK national guideline bands hypernatraemia by severity.** The best available UK anchors are a professional clinical reference used in UK practice (Patient.info doctor-facing article) and health board guidance (NHS Greater Glasgow & Clyde). Numeric intermediate bands in the wider literature originate from ICU cohort studies, not UK primary-care guidance.

This closure is therefore **`[C]` grade, not `[E]`**, and the HMR should record it as such rather than treat it as equivalent to the hypokalaemia and hypocalcaemia closures.

### 2.2 Severity bands

| Band | Threshold | Class |
|---|---|---|
| Definition | Na⁺ >145 mmol/L | `[E]` — consistently defined |
| Mild | 146–150 mmol/L | `[C]` |
| Moderate | 151–155 mmol/L | `[C]` |
| Severe | >155 mmol/L | `[C]` |
| Critical | >170 mmol/L | `[C]` — NHS GGC cites this level as the example of severe cases requiring specific fluid strategy |

### 2.3 Urgency time bands

| Threshold | Band | Rationale | Source |
|---|---|---|---|
| Na⁺ ≥155 | **Same day** | UK guidance directs seeking specialist advice where sodium is 155 mmol/L or more, where a clinical cause is not apparent, or where oral rehydration is not possible | Patient.info (UK doctor reference) `[C]` |
| Na⁺ >160 | **Same day** — reinforced | Severe symptoms are usually only found with acute and large rises above 160 mmol/L | Patient.info `[C]` |
| Na⁺ 146–154 | **Within days** | `[J]` — see HYPERNA-J1 below |

**HYPERNA-J1 `[J]`** — The 146–154 band is placed at *within days* rather than *within weeks* on the following reasoning, which is HealthIQ judgement and must be adjudicated: hypernatraemia is relatively rare in primary care and more common in hospital where homeostatic mechanisms are impaired `[E]`. In an ambulatory adult, hypernatraemia of any degree implies impaired thirst, impaired access to water, or excessive free-water loss. **The finding's significance derives from what it implies about the person, not from the concentration.** A conventional mild/moderate/severe reading would understate that.

### 2.4 Context and artefact caveats

| ID | Caveat | Class |
|---|---|---|
| NA-HIGH-C1 | Hypernatraemia is rare in ambulatory primary care; its presence is itself a signal | `[E]` |
| NA-HIGH-C2 | Common precipitants include gastrointestinal fluid loss, pyrexia, hyperglycaemia, lactulose and diuretics | `[E]` |
| NA-HIGH-C3 | Rate of correction is critical — reduction should not exceed roughly 10 mmol/L per day. **HealthIQ must never advise on correction** | `[E]` |
| NA-HIGH-C4 | Elderly and cognitively impaired people are at disproportionate risk through impaired thirst and access to water | `[E]` |
| NA-HIGH-C5 | Unlike hyponatraemia, no common analytical artefact inflates sodium. Note the reverse dependency: severe hypertriglyceridaemia falsely *lowers* sodium (XD-ARTEFACT-1) | `[C]` |

### 2.5 Safety without symptoms or examination

| Band | Safe without symptoms? | Required behaviour |
|---|---|---|
| ≥155 | **Yes, to escalate** | Same-day band fires on the value |
| 146–154 | **Safe to flag; the band placement is judgement** | Within-days band fires; output must state that hypernatraemia usually reflects fluid balance or access to water and that assessment requires clinical review |

**NA-HIGH-SAFE-1 `[C]`** — Safe to flag at all levels. **Not** declared unsafe-without-context, because the finding does not require symptoms to be interpretable — but the *explanation* is materially incomplete without hydration and cognitive context.

---

## 3. Hypocalcaemia (RE-U4 — CLOSED at `[E]`)

### 3.1 Severity bands — adjusted calcium only

**Uncorrected calcium may not be banded.** Contract §8.1 applies: calcium without albumin is an insufficient-data output, not a finding.

| Band | Threshold (adjusted) | Class |
|---|---|---|
| Definition | Adjusted Ca²⁺ below the local reference lower limit (commonly 2.20 mmol/L; one UK pathway uses <2.14 to define new adult hypocalcaemia) | `[E]` |
| Mild | Adjusted Ca²⁺ >1.9 mmol/L **and asymptomatic** | `[E]` — Society for Endocrinology |
| Severe | Adjusted Ca²⁺ <1.9 mmol/L **and/or symptomatic at any level below the reference range** | `[E]` — Society for Endocrinology |

The Society for Endocrinology Endocrine Emergency Guidance (2016, addendum 2019) is a **national UK specialist society source** and defines severe hypocalcaemia as a **medical emergency**.

### 3.2 Urgency time bands

| Threshold | Band | Rationale | Source |
|---|---|---|---|
| Adjusted Ca²⁺ <1.9 | **Same day** | Explicitly a medical emergency; IV calcium gluconate with ECG monitoring is indicated | Society for Endocrinology `[E]` |
| Adjusted Ca²⁺ ≤1.8 | **Same day** — reinforced | UK regional pathway uses ≤1.8 and/or symptomatic as its urgent trigger | Sheffield/Barnsley pathway `[E]` |
| Adjusted Ca²⁺ 1.9–2.1 | **Within days** | Below the level at which discharge is considered safe post-operatively; supplementation is escalated in this range | Society for Endocrinology; NHS GGC `[E]` |
| Adjusted Ca²⁺ 2.1 to lower reference limit | **Within weeks** | Recheck within one week is the post-operative discharge standard; in a non-operative setting this maps to routine investigation | Society for Endocrinology `[E]` |

### 3.3 Context and artefact caveats

| ID | Caveat | Class |
|---|---|---|
| CA-LOW-C1 | **Albumin adjustment is mandatory.** Contract §8.1 insufficient-data consequence | `[E]` |
| CA-LOW-C2 | Symptoms typically develop below 1.9 mmol/L, **but the threshold varies and symptoms also depend on the rate of fall** | `[E]` |
| CA-LOW-C3 | Magnesium must be checked; hypomagnesaemia causes refractory hypocalcaemia | `[E]` |
| CA-LOW-C4 | Drug causes include long-term PPIs (via hypomagnesaemia), loop diuretics, anticonvulsants, bisphosphonates, calcitonin, cinacalcet and denosumab | `[E]` |
| CA-LOW-C5 | Vitamin D deficiency is a common contributor; note HealthIQ has **not** adopted vitamin D bands (CN-U4) | `[E]` |
| CA-LOW-C6 | Chronic kidney disease and dialysis populations are managed under separate guidance and are outside this ruleset | `[E]` |
| CA-LOW-C7 | Cuff or tourniquet technique affects the measured value | `[C]` |

### 3.4 Safety without symptoms or examination

**This is the domain's most serious limitation and must be recorded prominently.**

The Society for Endocrinology definition is *"serum calcium <1.9 mmol/L **and/or symptomatic at any level below the reference range**"*. The second limb is a symptom criterion. HealthIQ cannot evaluate it.

| Band | Safe without symptoms? | Required behaviour |
|---|---|---|
| <1.9 adjusted | **Yes, to escalate** | Same-day band fires on the value alone |
| 1.9 to lower reference limit | **NO — HealthIQ will systematically under-detect emergencies in this range** | Band fires at within days or weeks per §3.2, and the output **must** state that hypocalcaemia at any level below the reference range is treated as an emergency if symptomatic, list the recognised symptoms (muscle cramps, paraesthesia, tetany, carpopedal spasm), and direct urgent review if any are present |

**CA-LOW-SAFE-1 `[E]` — declared unsafe-without-context under contract §27, test (c).** A person with adjusted calcium of 2.05 mmol/L and carpopedal spasm meets a national emergency definition that HealthIQ cannot detect. The mitigation is symptom-conditional user-facing language, not a lower band and not suppression.

**CA-LOW-SAFE-2 `[J]`** — This is the clearest case in the landscape where a rule's source definition includes a limb HealthIQ structurally cannot evaluate. It should be treated as a reference example when other domains are audited for the same pattern.

---

## 4. Summary of closures

| Gap | Status | Evidence grade | Residual |
|---|---|---|---|
| RE-U2 hypokalaemia | **CLOSED** | `[E]` — multiple concordant UK trust guidelines | Biochemical banding is explicitly arbitrary without symptoms/ECG; 3.0–3.4 band declared unsafe-without-context |
| RE-U3 hypernatraemia | **CLOSED with flag** | `[C]` — no UK national guideline bands this direction | 146–154 band placement is HealthIQ judgement (HYPERNA-J1) requiring adjudication |
| RE-U4 hypocalcaemia | **CLOSED** | `[E]` — Society for Endocrinology national emergency guidance | Symptom limb of the severe definition is structurally undetectable; declared unsafe-without-context |

**No band in this document was derived by analogy from another electrolyte or another direction.** Each was researched independently and the differing evidence grades reflect genuinely differing UK evidence availability, not differing effort.

---

## 5. Consequences for the renal/electrolyte ruleset

1. RE-F4 (hypokalaemia), RE-F6 (hypernatraemia) and RE-F8 (hypocalcaemia) now have governed bands and may be graded.
2. Three new same-day rules are added to the Tier 0 specification-only register: K⁺ <2.5, Na⁺ ≥155, adjusted Ca²⁺ <1.9. **This raises the renal/electrolyte Tier 0 count from 8 to 11 and the landscape total from 20 to 23** — which strengthens rather than weakens the XD-T0-1 argument that this domain should not be released with Tier 0 suppressed.
3. Two new unsafe-without-context declarations are required under contract §27: hypokalaemia 3.0–3.4, and hypocalcaemia above 1.9.
4. Magnesium is confirmed as a required companion request for both hypokalaemia and hypocalcaemia — a recommendation, not a modifier, since neither finding is uninterpretable without it.

---

## 6. Evidence table

| Source | Used for |
|---|---|
| NHS Gloucestershire Hospitals — management of hypokalaemia | Mild/moderate/severe bands |
| Royal Cornwall Hospitals — management of hypokalaemia in adults V4.0 (2025) | Band confirmation |
| NHS Grampian — acute hypokalaemia guideline | Band confirmation; primary and secondary care scope |
| RUH Bath PATH-017 — hypokalaemia, a guide for GPs | <2.5 telephoned; urgent admission consideration; digoxin/cardiac risk |
| York Hospitals — hypokalaemia in primary care | Laboratory telephoning thresholds; **explicit statement that biochemical severity is arbitrary without symptoms and ECG** |
| GPnotebook / Primary Care Notebook | Management by band; ≥4.0 target in heart failure and post-MI |
| Patient.info (UK doctor reference) — hypernatraemia | ≥155 specialist advice; >160 symptom threshold; rarity in primary care |
| NHS Greater Glasgow & Clyde — management of hypernatraemia | Severe case management; correction rate ≤10 mmol/L/day |
| **Society for Endocrinology — Emergency management of acute hypocalcaemia in adult patients (2016, addendum 2019)** | Mild >1.9 asymptomatic; severe <1.9 and/or symptomatic = medical emergency; 1.9–2.1 escalation; recheck within one week above 2.1 |
| NHS Greater Glasgow & Clyde — management of hypocalcaemia | Symptom threshold and rate-of-fall dependence; 1.9–2.2 escalation |
| Sheffield/Barnsley adult hypocalcaemia pathway | <2.14 definition; ≤1.8 and/or symptomatic urgent; drug causes |
| Doncaster & Bassetlaw / Kent & Medway acute hypocalcaemia guidance | Reference range confirmation; mild usually asymptomatic |

---

## 7. Sign-off

| Field | Value |
|---|---|
| HMR name / registration | ☐ |
| Hypokalaemia bands accepted | ☐ |
| Hypernatraemia bands accepted **at `[C]` grade** | ☐ |
| HYPERNA-J1 (146–154 at within days) adjudicated | ☐ ACCEPT / ☐ AMEND TO WITHIN WEEKS |
| Hypocalcaemia bands accepted | ☐ |
| CA-LOW-SAFE-1 symptom-conditional language approved | ☐ |
| K-LOW-SAFE-1 no-mild-reassurance rule approved | ☐ |
| Three new Tier 0 specification-only rules registered | ☐ |
| Signature / date | ☐ |
