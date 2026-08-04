---
document_id: HEALTHIQ-SIX-DOMAIN-CLOSURE-REPORT-001
title: HealthIQ Six-Domain Clinical Closure Report
version: "0.1"
covers:
  - HEALTHIQ-ELECTROLYTE-SUPPLEMENTAL-EVIDENCE-001 v0.1
  - HEALTHIQ-CROSS-DOMAIN-HMR-ADJUDICATION-REGISTER-001 v0.1
  - HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.6
  - HEALTHIQ-CROSS-DOMAIN-RULESET-001 v0.2
status: CLOSURE_PACKAGE_COMPLETE
implementation_status: NOT_AUTHORISED
---

# Six-Domain Clinical Closure Report v0.1

One bounded closure package, as commissioned. No six separate review cycles were run and the six-domain review was not restarted.

---

## 1. Research gaps closed

### 1.1 The three blocking electrolyte gaps

| Gap | Status | Grade | Source |
|---|---|---|---|
| RE-U2 hypokalaemia bands | **CLOSED** | `[E]` | Five concordant UK NHS trust and health board guidelines |
| RE-U3 hypernatraemia bands | **CLOSED with flag** | `[C]` | UK professional reference + health board guidance. **No UK national guideline bands this direction** |
| RE-U4 hypocalcaemia bands | **CLOSED** | `[E]` | Society for Endocrinology national emergency guidance |

**No band was derived by analogy** from potassium, from sodium, or from the opposite direction of the same analyte. The differing evidence grades reflect genuinely differing UK evidence availability.

### 1.2 Three findings from the research worth surfacing

**Hypokalaemia banding is explicitly arbitrary without symptoms and ECG.** York's guidance says so in terms. HealthIQ may state the concentration band; it may not characterise the consequence as mild. Even mild hypokalaemia carries increased risk in people on digoxin or with cardiac disease.

**The severe-hypocalcaemia definition contains a limb HealthIQ cannot evaluate.** The Society for Endocrinology defines it as adjusted calcium <1.9 mmol/L **and/or symptomatic at any level below the reference range**. The second limb is a symptom criterion. **HealthIQ will systematically under-detect emergencies between 1.9 and the lower reference limit.** The mitigation is symptom-conditional user-facing language — not a lower band, and not suppression. This is the clearest case in the landscape of a source definition HealthIQ cannot fully implement, and it should be used as the reference example when other domains are audited for the same pattern.

**The closures increased the Tier 0 surface.** Three new same-day rules — K⁺ <2.5, Na⁺ ≥155, adjusted Ca²⁺ <1.9 — mean renal/electrolyte now holds eight governed same-day rules, six of them potentially life-threatening. **The supplemental research strengthened rather than weakened the case that this domain should not be released with Tier 0 suppressed.**

### 1.3 Contract v0.5 conformance — the sixth HMR closure item

The HMR reconciliation listed clause-level conformance against the actual v0.5 as a required closure. v0.5 was supplied during this exercise and the check is **complete**.

v0.5 differs from v0.4 in six substantive respects, all of which were the corrections raised at the v0.4 confirmatory review. **All six workstreams conform.** One documentation correction only: the hepatic ruleset must be relabelled to adopt v0.6 (contract §21.2).

### 1.4 Gaps NOT closed by this package

| Gap | Why not |
|---|---|
| Severe-anaemia threshold (A5) | **No citation exists.** WHO's 2024 guideline explicitly declines to establish an outcome-linked severity classification. This requires documented clinical adjudication, not research |
| Subclinical hyperthyroidism bands (A6) | NICE NG145 supplies the ≥10 threshold for the hypo- direction only. Mirroring it is prohibited analogical import |
| Vitamin D bands (A8) | Requires SACN/NICE confirmation, or formal exclusion of the marker |
| CRP severity bands (A10) | No authoritative UK banding exists. HMR position — do not invent one |
| Baseline-validity windows (B6) | No UK source found by any workstream, except the AKI windows |

Each is named, bounded, and either adjudicable or explicitly declined. None is an open-ended research question.

---

## 2. HMR recommendations ready for approval

Twelve recommendations are evidence-backed and ready for HMR signature. Full reasoning in the adjudication register.

| ID | Recommendation | Grade |
|---|---|---|
| A1 | Adopt hypokalaemia bands, with no mild-consequence language | `[E]` |
| A2 | Adopt hypernatraemia bands, **recorded as `[C]` grade** | `[C]` |
| A3 | Adopt hypocalcaemia bands, with symptom-conditional language | `[E]` |
| A6 | Leave subclinical hyperthyroidism ungraded at within weeks — do not mirror the hypo- threshold | `[E]` reasoning |
| A7 | Withdraw the low-TSAT requirement; deficiency runs on ferritin, TSAT is the overload discriminator only | `[E]` |
| A10 | CRP remains primarily contextual; promotion on persistence only | HMR position |
| B4 | Adopt the three-part unsafe-without-context test and per-domain registers | `[J]`, six-domain convergence |
| B6 | Retain baseline windows as interim, explicitly labelled adjudicated | `[J]` |
| B7 | Thyroid-only scope with the limitation stated; extension is new authoring | `[J]` |
| — | Contract A7 — distinct missing-modifier consequences | `[E]` |
| — | Contract A8 — governed derivation obligation with a mandatory derivation contract | `[C]` |
| — | Contract A9 — empty Tier 0 register as a legitimate outcome | `[J]` |

**Four require HMR adjudication rather than approval**, because no citation exists and a decision must be recorded under contract §13: **A5** (severe-anaemia threshold), **A9** (bilirubin urgent threshold), **B2** (potassium threshold), **A4** (hypernatraemia 146–154 placement).

**Two are recommendations against which I expect challenge, and should be read as such:**

- **B2** — I recommend the CCS/KDIGO **>6.0** threshold over the UK Kidney Association's ≥6.5. The UKKA threshold assumes a clinical pathway that can assess a person at 6.0–6.4. HealthIQ has no clinician and no ECG. This is a deliberate, reasoned departure from a UK national threshold and must be recorded as one.
- **B1** — I recommend adopting the hepatic Tier 1 floor **literally**, with volume control as the mitigation. Volume is a presentation problem; departing from a grade B national recommendation is a clinical one. The opposite choice is defensible but must be documented as a departure, never adopted silently for volume reasons.

---

## 3. Decisions requiring Anthony

Eight product-authority decisions. **None has been decided here.** Each is recorded with the clinical constraint that bounds it.

| ID | Decision | Blocking |
|---|---|---|
| P1 | Same-day co-equal group presentation, including at three or more members | No |
| **P2** | **Tier 1 volume control** — load-bearing if the hepatic Tier 1 floor is adopted literally | **Yes** |
| P3 | Dual-role presentation — one fact appearing as its own concern and as another domain's context | No |
| P4 | Disease-name communication policy | No |
| P5 | No-concern limitation presentation — six domain statements on a fully normal panel | No |
| P6 | Release sequencing for domains with and without Tier 0 | No |
| **P7** | **Pregnancy out-of-scope user-facing wording** | **Yes** |
| **P8** | **Demographic capture for sex; whether ancestry is captured at all** | **Yes** — without sex capture, sex-dependent findings remain indeterminate |

P8 deserves a note. Without governed sex data, haemoglobin findings sit permanently in indeterminate severity. That is safe but degraded, and it affects a marker present on nearly every panel.

---

## 4. Decisions requiring regulatory or legal review

| ID | Decision | Blocking |
|---|---|---|
| **R1** | Tier 0 action-and-timeframe guidance — **23 rules now exist** | **Yes for any Tier 0 release** |
| **R2** | Individual cardiovascular risk calculation | **Yes for that capability** — quarantined meanwhile |
| **R3** | FIB-4 | **Yes for that capability** — quarantined meanwhile |
| R4 | Consumer disease-name outputs | Yes |
| **R5** | Declared population exclusions and intended-purpose wording | **Yes** |
| **R6** | **Whether renal/electrolytes may be released with Tier 0 suppressed** | **Yes** |

**R6 is the package's single most consequential open item.** The clinical position, unchanged and now reinforced by the supplemental evidence: a product that can identify a potassium of 6.8, a potassium of 2.3, a sodium of 122, a sodium of 158 or an adjusted calcium of 1.7, and has no governed way to act on any of them, is in a worse position than one that does not measure them. That is not a threshold question and cannot be resolved clinically alone.

R2 and R3 are handled by quarantine rather than by blocking the whole package: the *findings* still run, and only the *derived scores* are withheld. Lipid findings fire on named NICE referral thresholds; hepatic fibrosis findings fire on AST:ALT ratio and platelets.

---

## 5. Readiness of contract v0.6 and consolidated ruleset v0.2

### 5.1 Contract v0.6

Built as a governed delta on the **actual v0.5**, not on a reconstruction. Contains only HMR-authorised changes:

- **§4.9, §8.1** — A7, distinct missing-modifier consequences
- **§8.2** — A8, derivation obligation with a mandatory derivation contract specifying formula, units, assay assumptions, invalidity conditions, provenance and version
- **§6.2, §17** — A9, empty Tier 0 register
- **§26** — interim pregnancy policy
- **§27** — context-free unsafe-rule declaration requirement
- **§18.30–36** — seven consequent prohibitions
- **§20.19–21, §21.1** — consequent domain-research and haematology-scope items

**The proposed universal cross-domain lead distinguishers are not included.** They remain unratified, as directed.

Sections 1–25 retain v0.5 numbering so that existing domain rulesets' cross-references stay valid; the two new policies are appended as §26 and §27 rather than inserted mid-document. This is deliberate: renumbering a governed asset referenced by six domain files would invalidate every cross-reference in them.

**Ready for review.**

### 5.2 Consolidated ruleset v0.2

Every item in the commission is addressed: supplemental electrolyte evidence incorporated (§4); accepted rules separated from unresolved decisions throughout; unsourced thresholds removed or quarantined (§5, eight entries); interim pregnancy policy adopted with all six domains declaring materiality (§6); twelve unsafe-without-context rules registered (§7); shared-marker ownership and boundaries preserved (§8); Tier 0 corrected to 23 and all specification-only (§12); CV risk and FIB-4 quarantined (§10); thyroid-only limitation stated (§11); acceptance-test matrix expanded from 12 to 21 scenarios (§15); complete unresolved-decision register (§14).

**Ready for review.**

### 5.3 What a final consistency review should target

1. **§5 quarantine list** — confirm that no quarantined threshold has survived anywhere in the six domain files.
2. **UWC register completeness** — twelve rules are declared; contract §27.3 deems everything unlisted safe to run without context, so an omission has consequences.
3. **Tier 0 count** — verify 23 against the six domain files individually.
4. **XD-AS-16** — the acceptance scenario asserting that uncorrected calcium of 1.75 produces insufficient data and **no finding**, despite being below any emergency threshold. This is the hardest consequence of contract §8.1 and the one most likely to be argued with.
5. **Hepatic v0.2 relabel** to v0.6 (XD-CONF-1).

---

## 6. Summary position

| Question | Answer |
|---|---|
| Research gaps closed? | Three blocking electrolyte gaps closed; two at `[E]`, one at `[C]` with a flag. Contract v0.5 conformance closed |
| Model in question? | **No.** Conformance check found no non-conformance across six workstreams |
| Redesign required? | **No** |
| Blocking items remaining | 11 — four HMR adjudications, five HMR policy decisions, three product, four regulatory (overlapping) |
| Nature of remaining work | **Adjudication and ratification, not research** |

---

## VERDICT: READY_FOR_FINAL_INDEPENDENT_CONSISTENCY_REVIEW

Contract v0.6 and consolidated ruleset v0.2 are ready for one final independent cross-domain consistency review.

The verdict is not `REQUIRES_FURTHER_BOUNDED_CLOSURE` because every gap that drove the previous verdicts is now either closed or converted from a research question into a named decision with a recommended disposition and an identified owner. The three electrolyte band sets are sourced. The v0.5 conformance check is done. Nothing remaining requires further evidence-gathering except A8 (vitamin D), which is a confirm-or-exclude decision rather than open research.

It is not `UNSAFE_TO_PROGRESS` because progression here means a consistency review, not release. Every capability that would be unsafe to release — all 23 Tier 0 rules, cardiovascular risk calculation, FIB-4 — is quarantined and explicitly cannot be released without the named regulatory approvals.

**Two caveats on that verdict, both of which the reviewer should carry forward rather than treat as settled.**

The hypernatraemia bands are `[C]` grade because no UK national guideline bands that direction. They should not be presented alongside the hypokalaemia and hypocalcaemia closures as though the three are equivalent — they are not, and A4 in particular rests on my judgement rather than on evidence.

R6 remains open and is not made less urgent by anything in this package. The electrolyte research increased the number of life-threatening results HealthIQ can detect and cannot act on, from five to eight. Closing the research gap has sharpened that question rather than resolving it.
