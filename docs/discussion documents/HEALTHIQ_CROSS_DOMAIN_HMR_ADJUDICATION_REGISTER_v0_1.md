---
document_id: HEALTHIQ-CROSS-DOMAIN-HMR-ADJUDICATION-REGISTER-001
title: HealthIQ Cross-Domain HMR Adjudication Register
version: "0.1"
governing_contract: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.6
status: DRAFT_FOR_HMR_DECISION
implementation_status: NOT_AUTHORISED
---

# Cross-Domain HMR Adjudication Register v0.1

Every unresolved clinical-policy decision from the HMR six-domain reconciliation, with a recommended disposition.

**Recommendations are advisory.** Items marked `ANTHONY: REQUIRED` are product-authority decisions and are **not** decided here. Items marked `REG/LEGAL: REQUIRED` need specialist review that this team is not qualified to provide.

**Blocking** means the final consolidated ruleset cannot be ratified until the item is closed.

**Evidence labels:** `[E]` · `[C]` · `[J]` · `[U]`.

---

## A. Clinical evidence decisions

### A1 — Hypokalaemia bands
- **Options:** (a) adopt 3.0–3.4 / 2.5–2.9 / <2.5; (b) reject and research further.
- **Evidence:** `[E]` — five concordant UK NHS trust and health board guidelines.
- **Safety:** York guidance states the biochemical scale is arbitrary without symptoms and ECG. Adopting the bands as *concentration* bands is safe; adopting them as *consequence* bands is not.
- **Recommended:** **Adopt**, with K-LOW-SAFE-1 (no "mild consequence" language) and an unsafe-without-context declaration for 3.0–3.4.
- Anthony: no · Reg/legal: no · **Blocking: was yes — now CLOSED**

### A2 — Hypernatraemia bands
- **Options:** (a) adopt 146–150 / 151–155 / >155 with ≥155 same-day; (b) adopt only the ≥155 same-day rule and leave the rest ungraded; (c) decline the finding class.
- **Evidence:** `[C]` — **no UK national guideline bands this direction.** Anchors are a UK professional reference and health board guidance.
- **Safety:** (b) leaves a finding that can be created but not graded, which contract §18 prohibits. (c) discards a finding that in an ambulatory adult signals impaired thirst or water access.
- **Recommended:** **(a), recorded explicitly as `[C]` grade**, not as equivalent to A1 and A3.
- Anthony: no · Reg/legal: no · **Blocking: was yes — now CLOSED with flag**

### A3 — Hypocalcaemia bands
- **Options:** (a) adopt Society for Endocrinology mild/severe with the 1.9–2.1 intermediate; (b) research further.
- **Evidence:** `[E]` — national UK specialist society emergency guidance.
- **Safety:** The severe definition includes *"symptomatic at any level below the reference range"*, which HealthIQ cannot evaluate. **HealthIQ will systematically under-detect emergencies between 1.9 and the lower reference limit.**
- **Recommended:** **Adopt**, with mandatory symptom-conditional language (CA-LOW-SAFE-1) and an unsafe-without-context declaration.
- Anthony: no · Reg/legal: no · **Blocking: was yes — now CLOSED**

### A4 — HYPERNA-J1: placement of Na⁺ 146–154
- **Options:** (a) within days; (b) within weeks.
- **Evidence:** `[J]`. Reasoning: hypernatraemia is rare in ambulatory primary care `[E]`, so its presence implies impaired thirst or water access rather than a mild biochemical deviation.
- **Safety:** (b) risks understating a finding whose significance is what it implies about the person. (a) risks over-escalating a value that may reflect transient dehydration.
- **Recommended:** **(a) within days.** This is the least confident recommendation in the register and is offered for challenge.
- Anthony: no · Reg/legal: no · **Blocking: yes**

### A5 — Severe-anaemia same-day threshold (HAEM-U1)
- **Options:** (a) set a threshold; (b) leave HAEM-U-SD-5 unpopulated so anaemia caps at within days; (c) import oncology grading.
- **Evidence:** `[U]`. WHO's 2024 guideline **declines** to establish an outcome-linked severity classification and records that such an association "would be of great value" — i.e. it does not exist.
- **Safety:** (c) is an unlabelled import from a different clinical context and is prohibited by contract §18. (b) means a haemoglobin of 55 g/L cannot reach same day.
- **Recommended:** **(a), by documented clinical adjudication under contract §13**, not by citation — no citation exists. Record explicitly as adjudicated rather than evidence-derived.
- Anthony: no · Reg/legal: no · **Blocking: yes**

### A6 — Subclinical hyperthyroidism bands (THY-U2)
- **Options:** (a) mirror the hypothyroid ≥10 structure; (b) adjudicate a threshold; (c) leave ungraded at within weeks.
- **Evidence:** `[U]`. NICE NG145 supplies the ≥10 mIU/L threshold for the **hypo-** direction only. **(a) is prohibited** — it is analogical import across a direction asymmetry (contract §18.24, §4.2).
- **Safety:** Untreated thyrotoxicosis carries cardiac and bone consequences; leaving the direction ungraded understates it.
- **Recommended:** **(c) for this version** — retain at within weeks, ungraded, with the asymmetry stated. Revisit with specialist endocrine input.
- Anthony: no · Reg/legal: no · **Blocking: no**

### A7 — Low-TSAT deficiency threshold (IRIN-U3)
- **Options:** (a) adopt a threshold; (b) rely on ferritin for the deficiency question and use TSAT only for the overload question.
- **Evidence:** `[E]` for TSAT >45% (overload). No comparable UK-cited low threshold found.
- **Safety:** (b) is safe because low ferritin is itself specific and highly actionable; the deficiency question does not depend on TSAT.
- **Recommended:** **(b).** TSAT remains the overload discriminator only.
- Anthony: no · Reg/legal: no · **Blocking: no**

### A8 — Vitamin D inclusion and bands (CN-U4)
- **Options:** (a) confirm bands against SACN/NICE and adopt; (b) formally exclude vitamin D as a finding-generating marker; (c) retain the current state — finding created, no governed band.
- **Evidence:** `[U]`. Commonly used UK thresholds were not confirmed to a national source in this exercise.
- **Safety:** **(c) is prohibited by contract §18** — presenting a finding with no governed severity or indeterminate disposition. Vitamin D is however clinically relevant to hypocalcaemia (CA-LOW-C5).
- **Recommended:** **(a) if a SACN or NICE source can be confirmed; otherwise (b)**, retaining vitamin D as contextual to hypocalcaemia only. Do not leave in state (c).
- Anthony: no · Reg/legal: no · **Blocking: yes**

### A9 — Bilirubin urgent threshold (HEP-U2)
- **Options:** (a) set a numeric total-bilirubin threshold; (b) require the conjugated fraction before the rule can fire.
- **Evidence:** `[E]` that unexplained clinical jaundice warrants immediate referral; UK guidance frames it **clinically**, and HealthIQ has no clinical observation.
- **Safety:** (b) would disable a Tier 0 rule on most panels, since split bilirubin is rarely ordered.
- **Recommended:** **(a) by documented adjudication**, firing on total bilirubin with a mandatory statement that the conjugated fraction was not measured.
- Anthony: no · Reg/legal: no · **Blocking: yes** (Tier 0 rule incomplete)

### A10 — CRP severity bands (IRIN-U2)
- **Options:** (a) adopt numeric bands; (b) keep CRP primarily contextual with promotion only on marked or persistent unexplained elevation.
- **Evidence:** `[U]`. No authoritative UK CRP severity banding found. HMR position in the reconciliation: **do not invent universal CRP bands.**
- **Safety:** (a) would generate high-volume, low-value Tier 1 output.
- **Recommended:** **(b)**, consistent with the HMR position. The "marked" threshold in IRIN-U-W-4 must be removed or adjudicated rather than left implicit.
- Anthony: no · Reg/legal: no · **Blocking: no**, provided IRIN-U-W-4 is resolved

---

## B. HMR policy decisions

### B1 — Hepatic Tier 1 floor (HEP-U1)
- **Options:** (a) adopt BSG Recommendation 4 literally — any out-of-range core hepatic analyte floors at Tier 1; (b) magnitude-gated variant, recorded as a documented departure from a grade B recommendation.
- **Evidence:** `[E]` both ways. BSG Rec 4 is grade B. BALLETS: fewer than 5% of adults with abnormal liver blood tests had specific liver disease; 1.3% needed immediate treatment. Roughly 30% of liver test requests at one UK trust contained an out-of-range result.
- **Safety:** (a) is high-fidelity, high-volume, low-yield. (b) is a knowing departure from a graded national recommendation and must be recorded as clinical adjudication under contract §13, never adopted silently for volume reasons.
- **Recommended:** **(a), with contract §15.2 Tier 1 volume control as the mitigation.** Volume is a presentation problem; departing from a grade B recommendation is a clinical one. If (b) is chosen, the departure and its reasoning must be documented in the override register.
- Anthony: **REQUIRED** — the volume consequence is a product decision even though the clinical choice is not · Reg/legal: no · **Blocking: yes**

### B2 — Potassium urgent threshold (RE-U1)
- **Options:** (a) UK Kidney Association ≥6.5; (b) CCS/KDIGO >6.0.
- **Evidence:** `[E]` both. UKKA classifies 6.0–6.4 as moderate with ECG and cardiac monitoring recommended at ≥6.0; the divergence is documented in the outpatient hyperkalaemia literature.
- **Safety:** HealthIQ operates with **no clinician in the loop and no ECG**. The UKKA threshold assumes a clinical pathway that can assess at 6.0–6.4. That assumption does not hold here.
- **Recommended:** **(b) >6.0 for same day**, on the grounds that the more conservative threshold better matches a context with no clinical assessment available. Record as a deliberate, reasoned departure from the UK national threshold with the reason stated.
- Anthony: no · Reg/legal: no · **Blocking: yes**

### B3 — Pregnancy policy adoption
- **Options:** (a) adopt the HMR interim policy — explicit out-of-scope output where known, assumption statement where unknown; (b) build pregnancy-adjusted rules now; (c) status quo of six uncoordinated exclusions.
- **Evidence:** `[E]` that pregnancy alters reference frameworks in five domains.
- **Safety:** (c) is unacceptable — silent suppression in one domain and silent misapplication in others. (b) is substantial separate work.
- **Recommended:** **(a).** Now incorporated as contract v0.6 §26. Requires each domain to declare whether pregnancy materially affects its reference framework.
- Anthony: **REQUIRED** for the user-facing wording · Reg/legal: **REQUIRED** — a declared population exclusion bears on intended-purpose wording · **Blocking: yes**

### B4 — Context-free unsafe-rule register
- **Options:** (a) adopt the three-part test and require per-domain registers; (b) leave to domain judgement.
- **Evidence:** `[J]`, but every workstream raised the issue independently.
- **Safety:** (b) risks both over-withholding and silent misapplication.
- **Recommended:** **(a).** Now contract v0.6 §27. Confirmed unsafe-without-context so far: hypokalaemia 3.0–3.4; hypocalcaemia above 1.9; calcium without albumin; AKI without baseline; thyroid without treatment status; INR without anticoagulation status; all pregnancy-affected findings.
- Anthony: no · Reg/legal: no · **Blocking: yes** — each domain must supply its register

### B5 — Sex and ancestry handling
- **Options:** (a) require explicit demographic capture before applying sex- or ancestry-specific thresholds; (b) apply the more conservative threshold and state the assumption; (c) apply a default silently.
- **Evidence:** `[E]` that sex-specific thresholds exist for haemoglobin and for TSAT/ferritin genotyping; `[E]` that ferritin expectations and neutrophil ranges differ by ancestry.
- **Safety:** **(c) is prohibited** by contract §18 (automatic sex or ancestry assumptions) and by the HMR rejection of the haematology sex-unknown default. (b) is defensible for sex; **for ancestry it is not**, because there is no "conservative" direction — adjusting risks under-calling in one group, not adjusting risks over-calling in another.
- **Recommended:** **Sex — (a) with (b) as interim**, i.e. state the assumption explicitly and treat the finding as indeterminate under §4.9 until sex is captured. **Ancestry — (a) only.** Do not adjust for ancestry at all without governed data; state the limitation.
- Anthony: **REQUIRED** — demographic capture is a product decision · Reg/legal: no · **Blocking: yes**

### B6 — Baseline-validity framework
- **Options:** (a) adopt the per-domain windows proposed by the workstreams; (b) research a governed framework.
- **Evidence:** `[J]` throughout. **No workstream found a UK source for baseline validity windows.** The AKI windows (48 hours, 7 days) are the exception and are `[E]`.
- **Safety:** An eight-month-old creatinine used as a 48-hour baseline would produce a false AKI finding or a false exclusion.
- **Recommended:** **(a) as interim, explicitly labelled adjudicated not evidence-derived**, with the AKI windows retained as `[E]`. Do not let interim windows harden into precedent (contract §18).
- Anthony: no · Reg/legal: no · **Blocking: no**, but must be labelled

### B7 — Endocrine scope beyond thyroid (ENDO-U1)
- **Options:** (a) thyroid only, with the limitation declared; (b) extend to cortisol, PTH, sex hormones, IGF-1.
- **Evidence:** `[J]`. PTH interpretation is inseparable from calcium (owned by renal/electrolytes); cortisol requires timing and dynamic testing HealthIQ cannot perform.
- **Safety:** (b) as an extension of the current workstream would be under-researched. Presenting (a) as "endocrine coverage" would overstate scope.
- **Recommended:** **(a)**, with an explicit statement in the consolidated ruleset that thyroid-only coverage does not constitute endocrine coverage. Any extension is **new authoring**, not a revision.
- Anthony: no · Reg/legal: no · **Blocking: no**, provided the limitation is stated

### B8 — CRP role and escalation policy
- Covered at A10. **Recommended:** CRP remains primarily contextual.
- Anthony: no · Reg/legal: no · **Blocking: no**

---

## C. Product-authority decisions — ANTHONY: REQUIRED

**Not decided here.** Recorded with the clinical constraint that bounds each.

| ID | Decision | Clinical constraint |
|---|---|---|
| **P1** | Same-day co-equal group presentation, including at three or more members | Contract §7.4: no internal ordering, no cross-domain severity comparison. Artefact-confirmation wording must survive inside the group |
| **P2** | Tier 1 volume control | Load-bearing if B1(a) is adopted. Contract §15.2: compression may not reorder, remove, lower tiers or conceal that further findings exist |
| **P3** | Dual-role presentation (XD-DUAL-1) — a finding appearing as its own concern and as another domain's context | Must read as one fact, not two problems |
| **P4** | Disease-name communication policy — haemochromatosis, familial hypercholesterolaemia, Hashimoto's, Graves', myelodysplasia | Each requires more than biochemistry. Contract §18.13 prohibits unsupported diagnostic language |
| **P5** | No-concern limitation presentation — six domain-specific "does not exclude" statements on a fully normal broad panel | Contract §16.1 requires all of them. Presentation must not make them unreadable |
| **P6** | Release sequencing for domains with and without Tier 0 | Iron/inflammatory and thyroid have empty Tier 0 registers and are releasable without §17 |
| **P7** | Pregnancy out-of-scope user-facing wording | Contract §26.2 requires visibility, not suppression |
| **P8** | Demographic capture for sex, and whether ancestry is captured at all | B5. Without capture, sex-dependent findings remain indeterminate |

---

## D. Regulatory and legal — REG/LEGAL: REQUIRED

| ID | Decision | Why | Blocking |
|---|---|---|---|
| **R1** | Tier 0 action-and-timeframe guidance | Contract §17 and §22.5. **23 Tier 0 rules now exist** across the landscape (up from 20 after the electrolyte closures) | **Yes for Tier 0 release** |
| **R2** | Individual cardiovascular risk calculation | Closest thing in the landscape to MHRA's paradigm case of software producing an individual risk assessment | **Yes for that capability** |
| **R3** | FIB-4 | Calculated score with referral implications | **Yes for that capability** |
| **R4** | Consumer disease-name outputs | Interacts with P4 | Yes |
| **R5** | Declared population exclusions and intended-purpose wording | Pregnancy (§26), dialysis/transplant, paediatric. A declared exclusion is part of intended purpose | Yes |
| **R6** | **RE-U6 — whether renal/electrolytes may be released with Tier 0 suppressed** | Joint clinical, product, regulatory and legal. **The register's single most consequential open item** | **Yes** |

**On R6.** The clinical position from workstream C, endorsed by the HMR and reaffirmed here: a product that can identify a potassium of 6.8, a sodium of 122 or an adjusted calcium of 1.7 and has no governed way to act on it is in a worse position than one that does not measure them. This is not a threshold question and cannot be resolved clinically alone.

---

## E. Blocking summary

| Category | Blocking items |
|---|---|
| Clinical evidence | A4, A5, A8, A9 |
| HMR policy | B1, B2, B3, B4, B5 |
| Product | P2 (if B1(a)), P7 |
| Regulatory/legal | R1, R5, R6 — plus R2 and R3 for their specific capabilities |

**Closed by this package:** A1, A2 (with flag), A3.

---

## F. Sign-off

| Field | Value |
|---|---|
| HMR name / registration | ☐ |
| A4 · A5 · A8 · A9 adjudicated | ☐ |
| B1 hepatic Tier 1 floor | ☐ LITERAL / ☐ MODIFIED — reason: |
| B2 potassium threshold | ☐ ≥6.5 / ☐ >6.0 — reason: |
| B3–B7 adjudicated | ☐ |
| Product items referred to Anthony | ☐ |
| Regulatory items referred | ☐ |
| A5, A9, B2 recorded as documented adjudications under §13 | ☐ |
| Signature / date | ☐ |
