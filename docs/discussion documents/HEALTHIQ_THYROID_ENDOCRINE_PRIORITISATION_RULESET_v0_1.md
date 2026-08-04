---
document_id: HEALTHIQ-THYROID-ENDO-RULESET-001
title: HealthIQ Thyroid and Endocrine Prioritisation Ruleset
version: "0.1"
workstream: E
governing_contract: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.5
status: DRAFT_FOR_CENTRAL_RECONCILIATION
implementation_status: NOT_AUTHORISED
---

# Thyroid and Endocrine Prioritisation Ruleset v0.1

> **Contract availability note.** Authored against contract v0.4 plus the v0.5 principle summary in authoring spec §2. Re-check at reconciliation.

**Evidence labels:** `[E]` · `[C]` · `[J]` · `[U]`.

---

## 0. Evidence-base upgrade since the cross-domain validation

The cross-domain validation report recorded thyroid as having **the weakest evidence base of the nine domains**, resting on convention rather than a cited UK guideline. **That assessment is now superseded.** NICE NG145 provides direct UK guidance on subclinical hypothyroidism thresholds, TPO antibody use and pattern definitions `[E]`. The domain's evidence position is materially stronger than assumed, and the recommendation to sequence it late should be re-examined on that basis at reconciliation.

---

## 1. Scope and the domain's defining characteristic

**In scope:** TSH, free T4, free T3 where relevant, TPO antibodies.

**Out of scope:** pregnancy (trimester-specific ranges; misapplication causes both false alarm and false reassurance) `[E]`; paediatric; thyroid nodules and structural disease; thyroid emergencies (myxoedema coma, thyroid storm — clinical diagnoses HealthIQ cannot make); other endocrine axes (cortisol, PTH, sex hormones, IGF-1) — see §18 ENDO-U1.

### 1.1 Defining characteristic

**Severity in this domain is carried by the TSH/free T4 *relationship*, not by the TSH number.** NICE NG145 defines the patterns by relationship: low free T4 with high TSH is primary hypothyroidism; normal free T4 with high TSH is subclinical hypothyroidism; suppressed TSH with high free T4 or T3 is hyperthyroidism `[E]`.

**THY-P1 `[E]`** — A TSH value alone does not determine severity. A TSH of 12 with a low free T4 and a TSH of 12 with a normal free T4 are different findings with different management.

**THY-P2 `[E]`** — **Consequently this is the domain that generated the contract's indeterminate-severity provision.** Where free T4 is unavailable, the finding sits between two materially different states and neither escalating nor defaulting low is safe.

**THY-P3 `[J]`** — Urgency in this domain is genuinely low from biochemistry alone. Thyroid emergencies are clinical presentations, not laboratory values, and HealthIQ has no clinical observation.

---

## 2. Clinician first-look hierarchy

| Attention | Markers |
|---|---|
| **First look** | TSH, free T4 — inspected **together** `[E]` |
| **Conditional** | Free T3 (where TSH is suppressed and free T4 normal); TPO antibodies (once, in subclinical hypothyroidism) `[E]` |
| **Not repeated** | TPO antibodies — NICE directs measuring once and not repeating `[E]` |
| **Low yield alone** | TSH in isolation; free T3 routinely `[E]` |

**THY-FL-1 `[E]`** — NG145 directs contextualising before acting: repeat if mild or discordant, and check medications (amiodarone, lithium, biotin supplements), intercurrent illness and pregnancy status. HealthIQ holds none of these reliably — a standing limitation stated in output.

---

## 3. Canonical finding taxonomy

| ID | Finding | Pattern |
|---|---|---|
| THY-F1 | Overt (primary) hypothyroidism | TSH raised + free T4 low `[E]` |
| THY-F2 | Subclinical hypothyroidism | TSH raised + free T4 normal `[E]` |
| THY-F3 | Overt hyperthyroidism | TSH suppressed + free T4 or T3 raised `[E]` |
| THY-F4 | Subclinical hyperthyroidism | TSH suppressed + free T4 and T3 normal `[C]` |
| THY-F5 | **Indeterminate thyroid-axis abnormality** | TSH abnormal, free T4 unavailable |
| THY-F6 | Discordant thyroid-axis pattern | TSH and free T4 both raised, or both low |
| THY-F7 | Thyroid autoimmunity (contextual) | TPO antibodies positive |

**THY-CONS-1 `[E]`** — TSH and free T4 form **one** finding. They are never two concerns. This is the domain's basic consolidation rule and it is unusually clear-cut.

**THY-CONS-2 `[J]`** — TPO antibodies never form an independent finding. They refine prognosis within THY-F2 and inform the treatment discussion `[E]`.

**THY-CONS-3 `[E]`** — THY-F6 (discordant patterns) is a distinct finding class, not a variant of F1–F4. Both-raised or both-low patterns raise possibilities (assay interference, pituitary disease, non-thyroidal illness, biotin supplementation) that require specialist interpretation. **HealthIQ must not auto-explain these.**

---

## 4. Urgency rules and time bands

### 4.1 Same day

**None.** `[J]`

**THY-U-SD-NEG `[J]`** — Thyroid emergencies are clinical. No TSH or free T4 value generates a same-day action from biochemistry alone in a product with no clinical observation. Like iron/inflammatory, this is a positive finding: **the domain has an empty Tier 0 and is not blocked by contract §17.**

**`[U]` THY-U1** — Should a markedly suppressed TSH with markedly raised free T4 generate a within-days rather than within-weeks band? Untreated severe thyrotoxicosis carries cardiac risk. Flagged; currently within weeks.

### 4.2 Within days

| ID | Criterion | Basis |
|---|---|---|
| THY-U-D-1 | THY-F6 discordant pattern | Requires specialist interpretation; the differential includes pituitary disease `[C]` |

### 4.3 Within weeks

| ID | Criterion | Basis |
|---|---|---|
| THY-U-W-1 | THY-F1 overt hypothyroidism | Treatment indicated `[E]` |
| THY-U-W-2 | THY-F3 overt hyperthyroidism | `[E]` |
| THY-U-W-3 | THY-F2 with TSH ≥10 mIU/L | NICE: consider levothyroxine for adults with subclinical hypothyroidism and TSH ≥10 mIU/L on 2 occasions 3 months apart `[E]` |
| THY-U-W-4 | THY-F4 subclinical hyperthyroidism | `[C]` |
| THY-U-W-5 | THY-F5 indeterminate (see §6) | `[J]` |

### 4.4 Routine

| ID | Criterion | Basis |
|---|---|---|
| THY-U-R-1 | THY-F2 with TSH above the reference range but <10 mIU/L | NICE frames this as a symptom-dependent 6-month levothyroxine trial in under-65s, repeated 3 months apart — i.e. a discussion, not an intervention `[E]` |

**THY-U-NEG-1 `[E]`** — Mild subclinical hypothyroidism is common and often self-limiting. NICE requires confirmation on two occasions three months apart before treatment is considered at any threshold. A single mildly raised TSH is a repeat-and-discuss finding, not an abnormality requiring action.

---

## 5. Severity rules

**Severity method: pattern relationship, with a single numeric band inside the subclinical hypothyroid pattern. Multiples of a reference limit are prohibited and would be meaningless — TSH is logarithmically related to free T4.** `[C]`

| Pattern | Severity | Basis |
|---|---|---|
| Overt (F1, F3) | Higher — hormone level is outside range | `[E]` |
| Subclinical with TSH ≥10 (F2) | Intermediate — the NICE treatment-consideration threshold | `[E]` |
| Subclinical with TSH <10 (F2) | Lower — symptom- and antibody-dependent | `[E]` |
| Subclinical hyperthyroid (F4) | `[U]` THY-U2 — no numeric band set; the hyper- direction lacks a NICE equivalent of the ≥10 threshold |
| Discordant (F6) | Not gradable — routed on the requirement for specialist interpretation | `[C]` |

**THY-S-1 `[E]`** — **TSH ≥10 mIU/L is the only numeric severity boundary in this domain that rests on a UK guideline.** Every other numeric threshold that might be proposed here would be convention or judgement, and must be labelled as such.

**THY-S-2 `[C]`** — Direction asymmetry: the hyperthyroid direction carries a lower threshold for concern than the equivalent degree of hypothyroid abnormality, because untreated thyrotoxicosis carries cardiac and bone consequences. Not numerically bandable from cited UK sources; recorded as an ordering principle within §12.

---

## 6. Indeterminate-severity rules

**This domain generated contract §4.9. Its rules are therefore the reference implementation.**

| ID | Situation | Plausible states | Missing discriminator | Disposition |
|---|---|---|---|---|
| **THY-IND-1** | **TSH raised, free T4 unavailable** | Subclinical hypothyroidism (routine or within weeks) vs overt hypothyroidism (within weeks) | Free T4 | **THY-F5.** Band = **within weeks.** State both states. Name free T4 as the discriminating test and recommend it. **May not default to subclinical because it is commoner** `[J]` |
| THY-IND-2 | TSH suppressed, free T4 unavailable | Subclinical vs overt hyperthyroidism | Free T4 (and free T3) | THY-F5. Band = within weeks. Both states stated `[J]` |
| THY-IND-3 | TSH suppressed, free T4 normal, free T3 unavailable | Subclinical hyperthyroidism vs T3-toxicosis | Free T3 | Band = within weeks; T3 requested `[C]` |
| THY-IND-4 | Any abnormal pattern, treatment status unknown | Untreated disease vs treated disease under adjustment | Treatment status | **Do not assume untreated.** State that the result cannot be interpreted without knowing whether levothyroxine or antithyroid treatment is being taken `[E]` |
| THY-IND-5 | Any abnormal pattern, no repeat | Transient vs persistent | Second sample ≥3 months later | NICE requires confirmation on two occasions for subclinical treatment decisions `[E]`. Single result = repeat-and-discuss, never a treatment claim |

**THY-IND-1 rationale.** Subclinical hypothyroidism affects up to around 10% of iodine-sufficient populations `[C]`, so blanket escalation to the overt band would systematically over-call. But defaulting to subclinical would breach contract §6.1's prohibition on defaulting to the least serious plausible tier, and would understate a genuinely treatable condition. Within weeks is the band at which the two states converge on the same immediate action — obtain free T4 and discuss — which is why it is the safe disposition. **This is a governed domain rule under contract §4.9, not an arithmetic formula.**

---

## 7. Trend and baseline rules

**Classification: trend-important.**

| ID | Rule | Class |
|---|---|---|
| THY-T1 | NICE requires two results ≥3 months apart before subclinical treatment decisions `[E]` | `[E]` |
| THY-T2 | Mild subclinical abnormality frequently normalises spontaneously; a wait-and-see approach is standard `[C]` | `[C]` |
| THY-T3 | Rising TSH across serial results indicates progression toward overt disease and is a finding in its own right `[C]` | `[C]` |
| THY-T4 | Absent repeat is never evidence of transience `[E]` | `[E]` |
| THY-T5 | **No trend-based downgrade rule.** A normalising TSH may sit at a lower band by its own criteria; trend may not lower it below its floor | `[J]` |
| THY-T6 | Baseline validity: 3 months minimum interval per NICE; 24 months maximum for comparison `[J]` for the upper bound | `[E]`/`[J]` |

---

## 8. Modifier and interpretability rules

| Marker | Required modifier | Without it |
|---|---|---|
| **TSH** | **Free T4** | **Pattern not determinable.** Produces THY-F5 indeterminate, not a subclinical finding `[E]` |
| TSH suppressed + normal free T4 | Free T3 | T3-toxicosis not assessable `[C]` |
| Any pattern | Treatment status | Interpretation limited; must be stated `[E]` |
| Any pattern | Pregnancy status | **Interpretation unsafe** — see §10 |
| Subclinical hypothyroidism | TPO antibodies | Prognostic refinement unavailable; not blocking `[E]` |

**THY-MOD-1 `[E]`** — TSH without free T4 is the domain's defining marker–modifier case. Unlike calcium-without-albumin (where the value is not a clinical quantity), TSH alone **is** a real measurement — it just cannot discriminate between two management pathways. It therefore routes to **indeterminate severity (§6)**, not to insufficient data (contract §8). This distinction should be recorded centrally: two different missing-modifier consequences exist and the contract supports both.

---

## 9. Combination and override register

| ID | Trigger | Direction | Effect | Basis |
|---|---|---|---|---|
| THY-OV-1 | TSH raised + free T4 low | Classify | THY-F1, within weeks | `[E]` |
| THY-OV-2 | TSH ≥10 + free T4 normal | Promote | THY-F2 to within weeks | `[E]` |
| THY-OV-3 | TSH suppressed + free T4 or T3 raised | Classify | THY-F3, within weeks | `[E]` |
| THY-OV-4 | TSH and free T4 both raised, or both low | Promote | THY-F6, within days, specialist interpretation | `[C]` |
| THY-OV-5 | Any thyroid abnormality + abnormal lipids | **Cross-domain** | Thyroid becomes a **secondary-cause exclusion** for the lipid finding. NICE directs excluding hypothyroidism before lipid specialist referral `[E]` | `[E]` |
| THY-OV-6 | Hypothyroid pattern + macrocytosis | **Cross-domain** | Thyroid contextual to the haematology finding; haematology primary | `[C]` |
| THY-OV-7 | Pregnancy known | **Suppress domain** | No thyroid finding issued; explicit statement that thyroid results require pregnancy-specific interpretation `[E]` |

**THY-OV-7 note.** This is a **domain suppression**, not a finding downgrade, and it is the one place in the six workstreams where a whole domain is withheld. It is justified because non-pregnant reference ranges are actively wrong in pregnancy, so the alternative is not a lower-confidence finding but a wrong one. **`[U]` THY-U3** — suppression is itself a clinical decision and must be adjudicated; a pregnancy-adjusted ruleset would be the better long-term answer.

---

## 10. Contextual markers and confidence-only factors

**Contextual:**

| Marker | Role | Becomes independent when |
|---|---|---|
| TPO antibodies | Prognostic refinement within THY-F2 `[E]` | Never — positive antibodies with normal TFTs are not a finding `[C]` |
| Free T3 | Constituent of THY-F3/F4 | Never independent `[C]` |
| Thyroid pattern in a lipid context | Secondary-cause exclusion (THY-OV-5) | Where it independently meets Tier 1 — then both stand |

**Confidence-only:** absent symptoms; absent medication history (amiodarone, lithium, biotin — biotin supplements cause assay interference and are increasingly common) `[E]`; intercurrent illness (non-thyroidal illness syndrome distorts TFTs) `[E]`; absent treatment status where THY-IND-4 does not fire; absent family or autoimmune history.

**THY-CONF-1 `[E]`** — Biotin interference deserves specific mention: it is common, over-the-counter, and produces patterns that mimic hyperthyroidism. It affects **confidence and the repeat recommendation**, never tier.

---

## 11. Concern-tier mapping and lead selection

| Tier | Content |
|---|---|
| **Tier 0** | **Empty** |
| Tier 1 | THY-F1, THY-F3, THY-F6; THY-F2 with TSH ≥10; THY-F4; THY-F5 indeterminate |
| Tier 2 | THY-F2 with TSH <10 |
| Tier 3 | TPO antibodies; free T3 as constituent; thyroid pattern as lipid secondary-cause context |

**THY-LEAD-1 `[C]`** — Within the domain, overt patterns lead over subclinical at the same band; the hyperthyroid direction leads over the hypothyroid direction at equivalent degree (THY-S-2).

**THY-LEAD-2 `[J]`** — THY-F5 indeterminate is lead-eligible. Indeterminacy is a property of the finding, not a demotion (contract §4.9).

**THY-LEAD-3** — Cross-domain contests resolve on the common time band only. With no Tier 0 content and most findings at within weeks, this domain will rarely lead a panel containing renal, electrolyte or haematological abnormality — which is clinically correct.

---

## 12. Tier 0 specification-only register

**Empty.** Not blocked by contract §17.

**THY-T0-1 `[J]`** — Together with iron/inflammatory, this makes thyroid a candidate for earlier release than its position in the authoring sequence implies. Combined with the §0 evidence-base upgrade, **the recommendation to sequence thyroid late should be revisited at reconciliation.**

---

## 13. Acceptance scenarios

| # | Panel | Expected |
|---|---|---|
| AS-1 | TSH 14, free T4 8 (low) | **THY-F1**, Tier 1, within weeks. Overt hypothyroidism |
| AS-2 | TSH 14, free T4 15 (normal) | **THY-F2**, Tier 1, within weeks (TSH ≥10). NICE two-occasion requirement stated |
| AS-3 | TSH 6.2, free T4 15 (normal) | **THY-F2**, Tier 2, routine. Repeat in 3 months; symptom- and antibody-dependent discussion |
| AS-4 | **TSH 14, free T4 unavailable** | **THY-F5**, Tier 1, within weeks. **Both states stated.** Free T4 named and requested. May not default to subclinical. **Reference case for contract §4.9** |
| AS-5 | TSH <0.01, free T4 32 (raised) | **THY-F3**, Tier 1, within weeks |
| AS-6 | TSH <0.01, free T4 18 (normal), free T3 unavailable | THY-F4 with THY-IND-3 — T3-toxicosis not assessable. Tier 1 |
| AS-7 | TSH 12, free T4 28 — **both raised** | **THY-F6**, Tier 1, within days. Specialist interpretation. **Must not be auto-explained** |
| AS-8 | TSH 6.5, free T4 normal, TPO positive | THY-F2 Tier 2 with antibodies **contextual** — they inform the discussion, not a second finding |
| AS-9 | TSH 14, free T4 low, pregnancy known | **Domain suppressed** (THY-OV-7). Explicit statement that thyroid results require pregnancy-specific interpretation. No finding issued |
| AS-10 | TSH 8, free T4 normal, LDL 5.8 | Thyroid appears **twice in role**: THY-F2 Tier 2 in its own right, and as a secondary-cause exclusion attached to the lipid finding. **One finding, two presentations of the same fact** — not two concerns |
| AS-11 | TSH 8, free T4 normal, MCV 104, otherwise normal FBC | Haematology owns the macrocytosis; thyroid contextual to it (THY-OV-6). Thyroid also stands as THY-F2 Tier 2 |
| AS-12 | Normal TSH and free T4 | No-concern output; must state that a normal TFT at one timepoint does not exclude evolving thyroid disease, and that biotin or intercurrent illness can distort results |

---

## 14. No-concern and insufficient-data outputs

**No-concern — mandatory content:**
1. Normal thyroid function at one timepoint does not exclude evolving disease `[C]`.
2. Whether free T4 was measured; if not, that only TSH was assessed.
3. Biotin supplements and intercurrent illness can distort thyroid results `[E]`.
4. Symptoms warrant review irrespective of the summary.

**THY-NC-1 `[J]`** — "Your thyroid is normal" is prohibited where free T4 was not measured.

**Insufficient data:** minimum viable assessment is **TSH**. TSH alone routes to THY-F5 indeterminate rather than to insufficient data (THY-MOD-1). Insufficient data fires where pregnancy status is unknown **and** an abnormal pattern is present — `[U]` THY-U4, since pregnancy status is usually unknown and this rule as stated would fire constantly. Interim: state the limitation rather than suppress.

---

## 15. Cross-domain boundaries

| Marker | This domain's role | Other domain primary when | Disposition |
|---|---|---|---|
| Thyroid pattern | Primary | Cardiometabolic — as a secondary cause of dyslipidaemia `[E]` | **Attach contextually** to the lipid finding; thyroid finding also stands in its own right |
| Thyroid pattern | Primary | Haematology — as a cause of macrocytosis | Attach contextually; haematology primary for the MCV finding |
| Free T4 / T3 | Constituent | — | Owned here |
| TPO antibodies | Contextual | — | Owned here |

**THY-XD-1 `[J]`** — AS-10 demonstrates a pattern the central register must handle: a single finding that legitimately appears both as its own concern and as context for another domain's concern. This is **not** duplication. It must be presented so the reader understands it is one fact, not two problems.

---

## 16. Prohibited behaviours (domain additions)

1. Reporting a subclinical or overt classification from TSH alone.
2. Defaulting an isolated raised TSH to subclinical because it is commoner.
3. Auto-explaining a discordant (THY-F6) pattern.
4. Applying non-pregnant reference ranges where pregnancy is known.
5. Presenting TPO antibodies as an independent finding.
6. Asserting a treatment claim from a single result — NICE requires two occasions.
7. Expressing thyroid severity as multiples of a reference limit.
8. Importing the hepatic Tier 1 floor.
9. Assuming a patient is untreated.
10. Presenting AS-10's dual role as two separate concerns.

---

## 17. Unresolved questions

| ID | Question | Blocking |
|---|---|---|
| THY-U1 | Should marked thyrotoxicosis reach within days rather than within weeks? | Yes |
| THY-U2 | Subclinical hyperthyroidism has no NICE numeric equivalent of the ≥10 threshold | Yes |
| THY-U3 | **Pregnancy: is domain suppression (THY-OV-7) safe, or is a pregnancy-adjusted ruleset required before launch?** | **Yes** |
| THY-U4 | Pregnancy status is usually unknown. Does an abnormal pattern with unknown pregnancy status warrant a limitation statement (interim position) or suppression? | **Yes** |
| ENDO-U1 | **Scope: does this workstream cover other endocrine axes (cortisol, PTH, sex hormones, IGF-1)?** The spec says "where sufficient evidence exists". This version covers thyroid only. Cortisol and PTH in particular are common on private panels and have no rules here | **Yes — scope-determining** |
| THY-U5 | Should HealthIQ name Hashimoto's or Graves' in consumer output, given both require more than biochemistry? | Yes — communication |
| THY-U6 | Given §0 and the empty Tier 0, should thyroid be re-sequenced earlier? | Yes — sequencing |

**ENDO-U1 is the workstream's largest gap.** The authoring spec §3.5 permits "other endocrine markers already within the HealthIQ priority landscape where sufficient evidence exists". This version has restricted itself to thyroid because PTH interpretation is inseparable from calcium (owned by workstream C) and cortisol interpretation depends on timing and dynamic testing HealthIQ cannot perform. **Both decisions need ratifying rather than assuming.**

---

## 18. Evidence table

| Source | Used for |
|---|---|
| **NICE NG145 — Thyroid disease: assessment and management** | Pattern definitions; TSH ≥10 treatment-consideration threshold; two-occasions-3-months requirement; 6-month trial in under-65s with TSH <10 and symptoms; TPOAb measured once and not repeated; contextualisation for medication, illness and pregnancy |
| NICE CG181 | Hypothyroidism as a secondary cause of dyslipidaemia requiring exclusion before lipid referral |
| Subclinical hypothyroidism literature | Prevalence up to ~10% in iodine-sufficient populations; spontaneous normalisation `[C]` |

**Gaps:** no UK numeric banding for subclinical hyperthyroidism; no UK guidance on interpreting TFTs without clinical context; no rules authored for non-thyroid endocrine axes.

---

## 19. Clinical sign-off

| Field | Value |
|---|---|
| Version | 0.1 |
| Contract authored against | v0.4 + v0.5 summary — re-check required |
| HMR name / registration | ☐ |
| THY-U3 / U4 (pregnancy) | ☐ SUPPRESS / ☐ ADJUSTED RULESET — reason: |
| THY-U1, U2 | ☐ |
| **ENDO-U1 (scope beyond thyroid)** | ☐ THYROID ONLY / ☐ EXTEND — axes: |
| THY-U6 (re-sequencing) | ☐ |
| THY-IND-1 confirmed as the §4.9 reference implementation | ☐ |
| Empty Tier 0 confirmed | ☐ |
| Signature / date | ☐ |

---

## VERDICT: READY_FOR_CENTRAL_RECONCILIATION

Thyroid itself is complete and, contrary to the cross-domain validation's expectation, well supported by a direct UK guideline. THY-IND-1 is offered as the reference implementation of contract §4.9 and should be reviewed as such, since other domains' indeterminate rules were written against the same pattern.

The verdict is not `REQUIRES_ADDITIONAL_DOMAIN_RESEARCH` because the unresolved items are scope and adjudication questions rather than missing evidence: ENDO-U1 asks what this workstream should cover, and THY-U3/U4 ask how pregnancy should be handled. Both are decisions, not research. If ENDO-U1 is resolved in favour of extending to other endocrine axes, this workstream will need to be reopened and that extension should be treated as new authoring, not as a revision.
