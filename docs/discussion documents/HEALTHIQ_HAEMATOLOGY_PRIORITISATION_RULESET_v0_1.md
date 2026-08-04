---
document_id: HEALTHIQ-HAEM-RULESET-001
title: HealthIQ Haematology Prioritisation Ruleset
version: "0.1"
workstream: A
governing_contract: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.5
governing_spec: HEALTHIQ-PARALLEL-DOMAIN-PRIORITY-AUTHORING-001 v0.1
status: DRAFT_FOR_CENTRAL_RECONCILIATION
implementation_status: NOT_AUTHORISED
---

# Haematology Prioritisation Ruleset v0.1

> **Contract availability note (applies to all six workstreams).** Contract v0.5 was not supplied with this commission; only v0.4 was available. This ruleset has been authored against v0.4 plus the v0.5 principle summary in authoring spec §2, which incorporates the previously identified corrections (uncapped same-day co-equal group; per-domain indeterminate-severity rules; governed marker–modifier pairs; distinct no-concern and insufficient-data outputs). **Every clause below must be re-checked against the actual v0.5 text at reconciliation.** No rule here depends on a v0.5 provision not summarised in spec §2.

**Evidence labels:** `[E]` evidence-supported · `[C]` accepted clinical convention · `[J]` HealthIQ clinical judgement · `[U]` unresolved.

---

## 1. Scope and exclusions

**In scope:** adults ≥18. Haemoglobin, MCV, platelets, total white cell count, absolute neutrophil count, lymphocytes, monocytes, eosinophils, reticulocytes where available, red cell indices (MCH, MCHC, RDW).

**Out of scope:** paediatric and neonatal counts; pregnancy (physiological dilutional anaemia and gestational thrombocytopenia change every threshold below) `[E]`; haemoglobinopathy diagnosis; leukaemia/lymphoma classification; coagulation; blood film morphology interpretation (HealthIQ does not receive films); post-chemotherapy and post-transplant counts `[J]`.

**Boundary statement.** This domain supplies severity bands consumed by hepatic (platelets), iron (Hb, MCV), inflammatory (Hb, WCC) and nutritional (Hb, MCV). Those domains may reference these bands. **No other domain may define its own competing haematological bands** — contract §9.6.

---

## 2. Clinician first-look hierarchy

| Tier of attention | Markers | Basis |
|---|---|---|
| **First look** | Haemoglobin, MCV, platelets, total WCC, **absolute** neutrophil count | Spec §6.4; standard FBC triage `[C]` |
| **Conditional — on abnormal first look** | Reticulocytes, MCH, MCHC, RDW, lymphocyte/monocyte/eosinophil absolute counts | `[C]` |
| **Low yield in isolation** | MCHC, RDW, basophils, differential percentages | `[C]` |
| **Never used alone** | Percentage differentials — prohibited as a substitute for absolute counts (contract §18.28) | `[E]` |

**HAEM-FL-1 `[C]`** — The first-look set is a *staging* rule for attention, not a permission to discard the rest. Conditional markers enter as soon as any first-look marker is abnormal, or where a governed combination rule requires them.

**HAEM-FL-2 `[E]`** — Absolute neutrophil count, never neutrophil percentage. A normal-looking percentage against a low total WCC conceals severe neutropenia; this is the domain's single most consequential presentation error.

---

## 3. Canonical finding taxonomy

Per contract §3.1, these are consolidated findings, not one-per-marker.

| ID | Finding | Constituents |
|---|---|---|
| HAEM-F1 | Anaemia (with red-cell size subtype) | Hb + MCV ± indices ± reticulocytes |
| HAEM-F2 | Isolated macrocytosis | MCV raised, all other FBC normal |
| HAEM-F3 | Isolated microcytosis | MCV low, Hb normal |
| HAEM-F4 | Thrombocytopenia | Platelets |
| HAEM-F5 | Thrombocytosis | Platelets |
| HAEM-F6 | Neutropenia | Absolute neutrophil count |
| HAEM-F7 | Leucocytosis | WCC ± differential absolute counts |
| HAEM-F8 | Lymphocytosis / lymphopenia | Absolute lymphocyte count |
| HAEM-F9 | Eosinophilia | Absolute eosinophil count |
| **HAEM-F10** | **Multi-lineage cytopenia** | Two or more of: low Hb, low platelets, low neutrophils |
| HAEM-F11 | Indeterminate cytopenia | A cytopenia where the discriminating marker is absent (§6) |

**HAEM-CONS-1 `[C]`** — Hb and MCV consolidate into **one** anaemia finding with a subtype, never two.

**HAEM-CONS-2 `[E]`** — **HAEM-F10 is a single finding, not two or three.** Where two or more lineages are reduced, the individual cytopenias do not compete for concern slots; they are constituents. UK pathways treat combined cytopenias as a categorically different clinical situation from any single cytopenia, routing macrocytosis with any additional FBC abnormality to a separate pathway entirely `[E]`. This is the clearest case in the domain of contract §9.1 doing genuine clinical work: three individually low-tier cytopenias are collectively high-tier.

**HAEM-CONS-3 `[J]`** — Indices (MCH, MCHC, RDW) never form independent findings. They are contextual constituents of HAEM-F1/F2/F3.

---

## 4. Urgency rules and time bands

Contract §4.1 bands: **same day / within days / within weeks / routine.**

### 4.1 Same day

| ID | Criterion | Basis |
|---|---|---|
| HAEM-U-SD-1 | Platelets <20 × 10⁹/L (new) | New thrombocytopenia below 20 warrants urgent discussion with the on-call haematologist `[E]` |
| HAEM-U-SD-2 | Platelets <150 × 10⁹/L **with** new thrombosis or renal impairment | Same source explicitly names this combination `[E]` |
| HAEM-U-SD-3 | Absolute neutrophils <0.5 × 10⁹/L | Severe neutropenia; conventional threshold for urgent action `[C]` |
| HAEM-U-SD-4 | Three-lineage cytopenia (pancytopenia) | `[C]` |
| HAEM-U-SD-5 | Hb below the ratified severe-anaemia threshold | `[U]` — see §18 HAEM-U1 |

**All HAEM-U-SD rules are specification-only until contract §17 is ratified — see §13.**

### 4.2 Within days

| ID | Criterion | Basis |
|---|---|---|
| HAEM-U-D-1 | Platelets 20–49 × 10⁹/L | Urgent outpatient referral indicated below 50 `[E]` |
| HAEM-U-D-2 | Platelets 50–100 × 10⁹/L **with** another cytopenia, splenomegaly, lymphadenopathy, pregnancy or upcoming surgery | `[E]` |
| HAEM-U-D-3 | Two-lineage cytopenia | `[C]` |
| HAEM-U-D-4 | Absolute neutrophils 0.5–1.0 × 10⁹/L | `[C]` |
| HAEM-U-D-5 | Marked leucocytosis with abnormal differential pattern | `[U]` — threshold not set; see §18 |

### 4.3 Within weeks

| ID | Criterion |
|---|---|
| HAEM-U-W-1 | Platelets 50–100 × 10⁹/L, isolated `[E]` |
| HAEM-U-W-2 | New anaemia of any subtype without same-day features `[C]` |
| HAEM-U-W-3 | Macrocytosis **with** any other FBC abnormality `[E]` |
| HAEM-U-W-4 | New isolated microcytosis `[C]` |
| HAEM-U-W-5 | Persistent unexplained eosinophilia or lymphocytosis `[C]` |

### 4.4 Routine

| ID | Criterion |
|---|---|
| HAEM-U-R-1 | Isolated mild macrocytosis with an otherwise normal FBC `[E]` |
| HAEM-U-R-2 | Isolated thrombocytosis in a plausible reactive context `[C]` |
| HAEM-U-R-3 | Stable, previously investigated abnormality `[C]` |

**HAEM-U-NEG-1 `[E]`** — Isolated macrocytosis with a normal remaining FBC does not generate urgency. UK guidance is explicit that where standard investigations are normal and there are no other blood count abnormalities, the patient has idiopathic macrocytosis and should be reassured that no further tests are needed, with monitoring in primary care every six to twelve months where no cause is found.

---

## 5. Severity rules

**Severity method for this domain is absolute cell count.** Multiples of the reference limit are prohibited here (contract §18.4, §18.24). A platelet count of 18 × 10⁹/L expressed as a fraction of the lower reference limit is meaningless; expressed as an absolute count it is immediately interpretable against published bands.

### 5.1 Platelets `[E]` for band boundaries

| Band | Range (× 10⁹/L) |
|---|---|
| Severe | <20 |
| Moderate | 20–49 |
| Mild | 50–100 |
| Borderline | 100–149 |
| Normal | 150–450 |
| Thrombocytosis | >450 `[C]` |

### 5.2 Haemoglobin `[E]` for the anaemia threshold, `[U]` for internal bands

Anaemia defined as Hb <130 g/L in men and <120 g/L in non-pregnant women (WHO, retained in the 2024 revision) `[E]`.

Severity sub-banding within anaemia is **not set in this version.** WHO's own guideline records that a clear association between anaemia severity and clinical outcome would be of value for classifying severity but does not itself establish one for individual clinical use `[E]`. Bands adopted from oncology grading systems would be an unlabelled import. **`[U]` HAEM-U1 — the Head of Medical Research must set the severe-anaemia threshold that triggers HAEM-U-SD-5.** Until then, HAEM-F1 is capped at "within days" and the gap is stated.

### 5.3 Absolute neutrophil count `[C]`

| Band | Range (× 10⁹/L) |
|---|---|
| Severe | <0.5 |
| Moderate | 0.5–0.99 |
| Mild | 1.0–1.5 |
| Normal | 1.5–7.5 |

**HAEM-S-1 `[U]`** — Benign ethnic neutropenia is common and shifts the lower limit in people of African and some Middle Eastern ancestry. HealthIQ does not reliably hold ancestry. Applying the standard band without qualification will over-call neutropenia in these groups. Flagged for adjudication; interim behaviour is to state the possibility in the explanation, never to adjust the band silently.

### 5.4 MCV `[E]` for the reference frame, `[J]` for banding

Reference range is age-dependent and generally around 83–101 fL `[E]`. Because UK guidance does not band macrocytosis by magnitude, bands here are HealthIQ judgement:

| Band | Range | Class |
|---|---|---|
| Mild macrocytosis | >ULN to 105 fL | `[J]` |
| Moderate | 105–115 fL | `[J]` |
| Marked | >115 fL | `[C]` — MCV above 115 fL is reported as more specific for B12/folate deficiency than other causes |

**HAEM-S-2 `[C]`** — At marked macrocytosis, contextual role is unavailable regardless of the rest of the FBC (see §10). This replaces the temporary 10%-of-ULN margin used in the earlier hepatic draft, which was explicitly labelled non-clinical and **must now be removed from that document** (spec §3.2).

**HAEM-S-3 `[E]`** — Severity is not the driver of macrocytosis management; **company on the FBC is.** Isolated macrocytosis of any degree routes differently from macrocytosis with any additional abnormality.

---

## 6. Indeterminate-severity rules

Per contract §4.9. Each entry names the finding, the missing discriminator and the governed disposition. No arithmetic tier formula is used.

| ID | Situation | Plausible states | Missing discriminator | Disposition |
|---|---|---|---|---|
| HAEM-IND-1 | Low Hb, MCV unavailable | Iron-deficiency pattern (weeks) vs B12/folate pattern (weeks, different tests) vs marrow pathology (days) | MCV | Present as anaemia, subtype undetermined. Urgency floor = within weeks. State all three pathways, request MCV. **May not default to the most common** `[J]` |
| HAEM-IND-2 | Low total WCC, no differential | Severe neutropenia (same day) vs lymphopenia (weeks) | Absolute neutrophil count | **Insufficient data for the neutrophil question** (§8) — the low WCC finding stands, but neutropenia is reported as *not assessable*, not as absent. Explicitly request the differential `[J]`, on the strength of HAEM-FL-2 |
| HAEM-IND-3 | Macrocytosis, no B12/folate | Nutritional (weeks) vs alcohol/liver (weeks) vs myelodysplastic (days if other counts abnormal) | Other FBC lineages — usually present | Where the rest of the FBC is available and normal → resolves to HAEM-F2. Where it is not, indeterminate: floor at within weeks `[E]`-informed |
| HAEM-IND-4 | Thrombocytopenia, no prior count | New (higher urgency) vs long-standing (lower) | Baseline | **Must be treated as new.** Contract §18.9 forbids treating absent baseline as evidence of stability `[E]` |
| HAEM-IND-5 | Cytopenia with no film available | Reactive vs primary marrow process | Blood film | Film is never available to HealthIQ. This is a standing limitation, stated in every cytopenia output, not a per-case indeterminacy `[J]` |

**HAEM-IND-PRINCIPLE `[J]`** — In every entry above the disposition is *floor at the lower plausible urgency and state the higher*, never *escalate to the highest* and never *default to the lowest*. Contract §18.25 prohibits the first; §6.1 prohibits the second.

---

## 7. Trend and baseline rules

**Domain classification: trend-important** (not trend-essential; the findings exist cross-sectionally).

| ID | Rule | Class |
|---|---|---|
| HAEM-T1 | A new cytopenia is materially more concerning than a stable long-standing one. UK referral guidance keys on *new* thrombocytopenia `[E]` | `[E]` |
| HAEM-T2 | Rate of fall matters independently of the absolute count. A platelet count of 90 that was 300 three months ago is a different finding from a stable 90 `[C]` | `[C]` |
| HAEM-T3 | A count that has halved but remains in range may still form a finding — contract §3.1 in-range rule `[C]` | `[C]` |
| HAEM-T4 | No trend-based downgrade rule is defined for this domain. A stable cytopenia may sit at a lower urgency band by its own criteria, but trend may not lower it below its floor (contract §12.2) | `[J]` |
| HAEM-T5 | **Baseline validity: 12 months** for cytopenia chronicity; 3 months for rate-of-change assessment | `[J]` — no UK source specifies; flagged |

---

## 8. Modifier and interpretability rules

Marker–modifier pairs per contract §8. Absence of the modifier produces an **insufficient-data output for that question**, not a low-confidence finding.

| Marker | Required modifier | Without it |
|---|---|---|
| Total WCC | Absolute differential | Neutropenia and lymphopenia questions are **not assessable** `[E]` |
| Hb (for subtype) | MCV | Anaemia stands; subtype not assessable `[C]` |
| Hb (for anaemia definition) | Sex | Anaemia cannot be defined — thresholds are sex-specific `[E]`. Where sex is unknown, use the lower (female) threshold and state the assumption `[J]` |
| MCV (for pathway selection) | Remaining FBC lineages | Isolated-versus-not cannot be determined; do not assume isolated `[E]` |
| Platelets (for genuineness) | — | Not a modifier pair, but see §9 |

**HAEM-MOD-1 `[E]`** — Not-assessable is reported as not assessable, never as not met. A missing differential does not mean neutrophils are normal.

---

## 9. Combination and override register

All promotion-only. Each is enumerable, sourced and directionally constrained per contract §13.

| ID | Trigger | Direction | Effect | Basis |
|---|---|---|---|---|
| HAEM-OV-1 | Any two lineages reduced | Promote | Form HAEM-F10; band ≥ within days | `[C]` |
| HAEM-OV-2 | Three lineages reduced | Promote | HAEM-F10; band = same day | `[C]` |
| HAEM-OV-3 | Macrocytosis + any other FBC abnormality | Reclassify | Leaves HAEM-F2; becomes HAEM-F1 or F10 | `[E]` |
| HAEM-OV-4 | Thrombocytopenia + new thrombosis or renal impairment | Promote | Same day | `[E]` |
| HAEM-OV-5 | Platelets 50–100 + another cytopenia, splenomegaly, lymphadenopathy, pregnancy or upcoming surgery | Promote | Within days | `[E]` |
| HAEM-OV-6 | Anaemia + low MCV | Consolidate | Single iron-pattern finding; hand to iron domain for aetiology (§16) | `[C]` |
| HAEM-OV-7 | Anaemia + high MCV | Consolidate | Single B12/folate-pattern finding; hand to nutritional domain | `[E]` |
| HAEM-OV-8 | Thrombocytopenia + abnormal hepatic analytes | **Cross-domain consolidate** — see §16 and central register | Consolidates into the hepatic fibrosis finding, preserving the higher urgency band | `[E]` |

**No downgrade overrides are defined for this domain.**

---

## 10. Contextual-marker rules

| Marker | Usual role | Boundary at which it becomes independent |
|---|---|---|
| MCH, MCHC | Contextual to HAEM-F1 | Never independent `[J]` |
| RDW | Contextual | Never independent `[J]` |
| MCV | Contextual to a hepatic or nutritional finding **only** where mild and the rest of the FBC is normal | Moderate band or above; or any other FBC abnormality `[E]`/`[J]` |
| Platelets | Contextual to a hepatic fibrosis finding | Any platelet band at moderate or below (<50 × 10⁹/L), or any same-day criterion — contract §4.8 forbids contextual status then `[E]` |
| Reticulocytes | Contextual to HAEM-F1 | Where markedly raised with anaemia, suggests haemolysis or bleeding — becomes a constituent, not context `[C]` |

**HAEM-CTX-1 `[E]`** — This is the boundary that failed in the original UAT case. A marker may be contextual only within a stated band. Outside it, contract §4.8 prohibits contextual assignment.

---

## 11. Confidence-only factors

Affect wording and specificity; never tier, prominence or lead (contract §4.5, §10).

- No blood film available (standing limitation, HAEM-IND-5)
- No reticulocyte count
- No prior counts
- No symptoms (bleeding, infection, fatigue)
- No medication history (chemotherapy, clozapine, methotrexate, carbimazole)
- No ancestry information (HAEM-S-1)
- Unknown splenomegaly or lymphadenopathy status

**HAEM-CONF-1 `[E]`** — None of these may reduce a finding's tier. All are common; a rule that demoted findings on their absence would demote nearly every haematological finding HealthIQ produces.

---

## 12. Concern-tier mapping

Initial tier = the more serious of urgency-derived and severity-derived (contract §6.1).

| Tier | Haematology content |
|---|---|
| **Tier 0** | All HAEM-U-SD criteria — severe thrombocytopenia, severe neutropenia, pancytopenia, thrombocytopenia with thrombosis/renal impairment |
| **Tier 1** | All HAEM-U-D and HAEM-U-W criteria — moderate/mild cytopenias, new anaemia, macrocytosis with other abnormality, new microcytosis |
| **Tier 2** | Isolated mild macrocytosis with normal FBC `[E]`; reactive thrombocytosis; stable previously investigated abnormality |
| **Tier 3** | Red cell indices; differential percentages; MCV within the contextual band when attached to a hepatic or nutritional parent |

**HAEM-TIER-1 — explicit anti-universalisation statement.** Isolated mild macrocytosis sits at **Tier 2, with reassurance available**, on direct UK guidance `[E]`. The hepatic domain's rule that any out-of-range analyte floors at Tier 1 **does not apply here and must not be imported.** This is the load-bearing counterexample recorded in the cross-domain validation and in contract §18.23.

---

## 13. Tier 0 specification-only register

Per contract §17, no Tier 0 content may be released until the operational escalation pathway is ratified.

| Rule | Status |
|---|---|
| HAEM-U-SD-1 (platelets <20) | **Specification-only** |
| HAEM-U-SD-2 (platelets + thrombosis/renal) | **Specification-only** |
| HAEM-U-SD-3 (neutrophils <0.5) | **Specification-only** |
| HAEM-U-SD-4 (pancytopenia) | **Specification-only** |
| HAEM-U-SD-5 (severe anaemia) | **Specification-only and threshold-blocked** (HAEM-U1) |

All Tier 1 and below content is release-eligible subject to normal governance.

**HAEM-T0-1 `[J]`** — Where Tier 0 is suppressed for release, the finding is **not** silently demoted to Tier 1. It is withheld from the automated output and the domain operates with an explicit statement that HealthIQ does not issue urgent-escalation guidance. Demotion would breach contract §18.19.

---

## 14. Lead-selection examples

| Panel | Lead | Reason |
|---|---|---|
| Platelets 18, Hb 128 (M), MCV 92 | Severe thrombocytopenia | Same day outranks the borderline Hb `[E]` |
| Hb 95, MCV 78, platelets normal | Anaemia, microcytic subtype — **one** finding | Consolidation; iron domain supplies aetiology |
| MCV 99.5, everything else normal | No lead from this domain | Tier 2; if another domain has a Tier 0/1 finding, MCV is contextual `[E]` |
| MCV 99.5, platelets 140, Hb 118 (F) | Multi-lineage — **one** finding, within days | HAEM-OV-1; the individual values would each be low-tier `[C]` |
| Neutrophils 0.4, all else normal | Severe neutropenia | Same day `[C]` |
| WCC 3.1, no differential | Low WCC finding + **neutropenia not assessable** | HAEM-IND-2 |

---

## 15. No-concern and insufficient-data outputs

### 15.1 No-concern (contract §16.1)

Mandatory haematology content:
1. A normal FBC does not exclude haematological disease. Marrow disorders can present with a normal count `[C]`.
2. No blood film was examined — standing limitation.
3. Which lineages were assessed and which were not (e.g. no differential ⇒ no neutrophil assessment).
4. Symptoms — unexplained bruising, bleeding, recurrent infection, persistent fatigue, night sweats, weight loss — warrant review irrespective of a normal count `[C]`.

**HAEM-NC-1 `[J]`** — The phrase "your blood is healthy", or equivalent, is prohibited.

### 15.2 Insufficient data (contract §16.2)

Fires where: no differential with an abnormal WCC; Hb without sex; MCV without the remaining lineages when macrocytosis is present.

Minimum viable haematology assessment: **Hb + MCV + platelets.** Without all three, issue an insufficient-data output for the domain rather than a partial finding.

**HAEM-ID-1 `[J]`** — Where the panel contains a Tier 0 or Tier 1 finding elsewhere, the haematology insufficient-data statement is presented *alongside* that finding and does not take the lead. This implements the scoping correction to contract §16.2.

---

## 16. Cross-domain consolidation and shared markers

| Marker | This domain's role | Boundary at which another domain becomes primary | Disposition |
|---|---|---|---|
| Platelets | Cytopenia severity | Hepatic becomes primary where hepatic analytes are abnormal **and** platelets are ≥50 × 10⁹/L | **Consolidate** into the hepatic fibrosis finding, preserving the higher urgency band. Below 50, haematology remains primary and consolidation is prohibited (contract §4.8) `[E]` |
| MCV | Macrocytosis severity | Hepatic or nutritional where mild and isolated | **Attach contextually**, within the §10 band only |
| Hb | Anaemia definition and severity | Iron (microcytic subtype), nutritional (macrocytic subtype), inflammatory (normocytic with raised CRP) | **Consolidate** — one anaemia finding; the other domain supplies aetiology, not a second concern |
| WCC / neutrophils | Cytopenia and leucocytosis | Inflammatory where raised with CRP | **Attach contextually** to the inflammatory finding; haematology remains primary for any cytopenia |
| Reticulocytes | Anaemia response | — | Constituent |

**HAEM-XD-1 `[E]`** — Anaemia must never appear twice. If both this domain and iron produce an anaemia concern, they have failed to consolidate.

---

## 17. Prohibited behaviours (domain-specific additions to contract §18)

1. Using percentage differentials in place of absolute counts.
2. Expressing haematological severity as multiples of a reference limit.
3. Importing the hepatic Tier 1 floor into this domain.
4. Treating a cytopenia as isolated without checking the other lineages.
5. Presenting multi-lineage cytopenia as separate findings.
6. Treating a missing differential as evidence that neutrophils are normal.
7. Assigning contextual role to MCV above the mild band, or to platelets below 50 × 10⁹/L.
8. Adjusting the neutrophil band for presumed ancestry without governed data.
9. Treating absent prior counts as evidence of chronicity.
10. Issuing reassurance for isolated macrocytosis without stating what was and was not excluded.

---

## 18. Unresolved questions

| ID | Question | Blocking |
|---|---|---|
| HAEM-U1 | Severe-anaemia Hb threshold for same-day escalation. No UK guideline sets one for individual clinical use | **Yes** — HAEM-U-SD-5 incomplete |
| HAEM-U2 | Benign ethnic neutropenia handling without ancestry data | **Yes** — risk of systematic over-calling |
| HAEM-U3 | Leucocytosis threshold for within-days escalation | Yes |
| HAEM-U4 | Whether HealthIQ produces any finding for isolated lymphocytosis, given its differential includes conditions requiring specialist assessment | Yes, for scope |
| HAEM-U5 | Baseline validity windows (HAEM-T5) — judgement, not sourced | No |
| HAEM-U6 | Pregnancy — currently excluded. Is exclusion safe, or does it produce silent gaps? | Yes |
| HAEM-U7 | Whether thrombocytosis warrants any finding at all in a consumer product given its reactive commonality | No |

---

## 19. Evidence table

| Source | Used for |
|---|---|
| Barts Health NHS Trust — haematology advice and guidance | Platelet bands; thrombocytopenia + thrombosis/renal rule; pseudothrombocytopenia |
| King's Health Partners — adult haematology GP referral guide | Platelet referral bands; bleeding risk below 20 |
| NHS Scotland Right Decisions / RefHelp — isolated macrocytosis; macrocytic anaemia | HAEM-U-R-1; HAEM-OV-3; Tier 2 placement |
| NHS Highland — macrocytosis guideline | MCV reference range; monitoring interval |
| NHS Kernow — macrocytosis referral criteria | Artefactual MCV elevation |
| WHO — Guideline on haemoglobin cutoffs to define anaemia (2024) | Anaemia definition; explicit absence of an outcome-linked severity classification |
| BSH/BCSH — cobalamin and folate disorders | MCV >115 fL specificity |
| Newcastle Hospitals adult haematology guidelines | General referral framing |

**Gaps:** no UK source bands anaemia severity for individual care; no UK source bands macrocytosis by magnitude; neutropenia bands are convention rather than a cited UK guideline.

---

## 20. Clinical sign-off

| Field | Value |
|---|---|
| Ruleset version | 0.1 |
| Contract version authored against | v0.4 + v0.5 principle summary — **must be re-checked against actual v0.5** |
| HMR name / registration | ☐ |
| HAEM-U1 (severe anaemia threshold) | ☐ |
| HAEM-U2 (ethnic neutropenia) | ☐ |
| HAEM-U3, U4, U6 | ☐ |
| All `[J]` items individually reviewed | ☐ |
| Override register approved as versioned asset | ☐ |
| Tier 0 specification-only register confirmed | ☐ |
| Signature / date | ☐ |

---

## VERDICT: READY_FOR_CENTRAL_RECONCILIATION

Two blocking unresolved items (HAEM-U1, HAEM-U2) are threshold adjudications, not structural gaps — the finding taxonomy, urgency bands, consolidation rules and contextual boundaries are complete and internally consistent. The domain supplies the bands that four other workstreams depend on, and those bands (platelets, MCV) are the ones that are evidence-supported. The two gaps are in anaemia severity and neutrophil ancestry adjustment, neither of which is a dependency of another domain.
