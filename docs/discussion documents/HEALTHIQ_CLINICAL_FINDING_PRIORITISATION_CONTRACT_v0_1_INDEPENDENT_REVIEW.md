---
document_id: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001-REVIEW
title: Independent Medical Red-Team Review of HealthIQ Clinical Finding Prioritisation Contract v0.1
reviews: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.1
reviewer_role: Independent medical research and red-team reviewer
status: REVIEW_COMPLETE
verdict: VALIDATE_WITH_REQUIRED_REVISIONS
---

# Independent Medical Red-Team Review — Prioritisation Contract v0.1

## 0. Reviewer verdict up front

`VALIDATE_WITH_REQUIRED_REVISIONS`

**The clinical architecture is sound.** The contract correctly identifies the structural defect in the previous model, correctly separates confidence from priority, correctly refuses a universal severity formula, correctly consolidates frames before ranking, and correctly demotes IDL display priority. On the questions that caused the UAT failure, this document gets the right answers for the right reasons.

**It is not yet safe to ratify**, for eleven defects set out in §2 and §3 below. Four of them are blocking. The most serious is not a threshold gap — the contract is honest that thresholds are deferred — but a **leakage path that allows interpretive confidence to re-enter prominence through the "clinical significance" dimension**, which would silently reproduce the original failure while appearing compliant with the contract's own prohibitions.

The second most serious is a **scope omission**: the contract does not address whether the functionality it defines constitutes a regulated medical device in the intended launch market. A document that assigns clinical urgency tiers and instructs users toward prompt clinical review is operating in territory where that question determines what evidence, validation, and post-market obligations attach to everything else in the document.

---

## 1. What the contract gets right

Recorded explicitly, because a red-team review that lists only faults gives a false impression of the document's quality.

| # | Strength | Comment |
|---|---|---|
| 1 | §3.1 unit of prioritisation | Naming the *consolidated clinical finding* as the canonical unit, and explicitly excluding signal rows, frames, hypotheses, and IDL records, resolves the frame-multiplication failure at its root rather than patching the symptom. This is the single best decision in the document. |
| 2 | §4 dimension separation | Ten-dimension separation with explicit "must not determine prominence" clauses is the correct clinical model. |
| 3 | §4.2 "No universal severity formula is authorised" | Correct and important. The listed metric types (ULN multiple, absolute concentration, absolute count, change from baseline, disease-stage band, direction-specific) cover the real cases. |
| 4 | §5 mandatory processing order | Making consolidation-before-ranking and urgency-independent-of-confidence into ordering constraints rather than aspirations is the right enforcement mechanism. |
| 5 | §8 supporting-marker policy | "Supporting markers must not be counted as votes" plus a closed list of the seven ways they *may* legitimately act is precise and auditable. |
| 6 | §11 analytical reliability | "Urgency remains based on the potential consequence" is the correct and non-obvious call. Many designs would demote on suspected artefact. |
| 7 | §12 final clause | Requiring the system to state when a change-based criterion could not be assessed is a genuine safety provision that most consumer products omit. |
| 8 | §13 phenotype policy | Correct in full. Deriving phenotype severity from constituents, and demoting static display priority to a within-tier tie-breaker, closes the IDL hero-slot defect. |
| 9 | §19.5 implementation gating | Six-condition gate with `NOT_AUTHORISED` status is appropriate governance for a clinical asset. |
| 10 | §17 threshold deferral | Refusing to invent numbers in a policy document is the right discipline. |

---

## 2. Blocking defects

These must be resolved before ratification. Each would, if left, permit a clinically unsafe output that is nonetheless contract-compliant.

### B1 — "Clinical significance" is an unclosed leakage path for confidence

**Where:** §4.3, §7.2 item 3.

§4.3 defines clinical significance as *"the likelihood that the finding represents a clinically meaningful problem."* That is a probability statement. §4.5 defines interpretive confidence as certainty about the explanation, and §10 forbids confidence from controlling prominence. But §7.2 places clinical significance third in the within-tier ordering key.

The failure mode: AST is absent. A rule author reasons that without AST the probability that this represents a meaningful hepatic problem is lower — muscle source not excluded, pattern less specific. Significance drops. Ordering drops. The contract's confidence prohibition has been honoured to the letter and defeated in substance. This is exactly the UAT failure re-entering through a side door, and it will be harder to detect the second time because the document will be cited as evidence that it cannot happen.

The same path exists for tier assignment if significance feeds tiering.

**Required revision.** Redefine clinical significance as a property of the *finding as characterised*, not of HealthIQ's certainty in characterising it — i.e. "given that this finding is present as described, how consequential is that class of finding." Then add an explicit prohibition:

> Clinical significance must be assessed on the assumption that the finding is as characterised. Absence, unavailability, or ambiguity of supporting data must not reduce clinical significance. Such factors act only on interpretive confidence.

Without this, §10 is unenforceable.

### B2 — The tier-assignment function is undefined, and it is the load-bearing element

**Where:** §5 (step "concern-tier assignment"), §6.

§6 describes what each tier means in prose. Nothing in the contract states how urgency, severity, significance, and actionability combine to produce a tier. §17.10 defers "cross-domain tier mapping" to research, which is correct for the *thresholds* — but the *form* of the mapping is a policy decision, not a research finding, and it belongs here.

Two mappings consistent with the current text produce different clinical behaviour:

- `tier = max(tier_from_urgency, tier_from_severity)` — a high-severity, low-urgency finding still reaches Tier 1.
- `tier = tier_from_urgency, modified by severity` — urgency dominates, and a very high ferritin with normal TSAT (high magnitude, low urgency) could land in Tier 2.

The contract does not say which. Domain rule authors will choose independently and inconsistently.

**Required revision.** Specify the mapping form, and specify that urgency sets a *floor* on tier which severity may raise but not lower. Recommended:

> Tier is the higher of the tier implied by urgency and the tier implied by severity. Clinical significance and actionability may raise a finding by at most one tier and may never lower it below the floor set by urgency.

The numeric bands remain deferred; the algebra must not be.

### B3 — No policy for the all-normal / no-foreground-concern case

**Where:** absent throughout. §15.13 prohibits presenting no foreground concern as proof nothing is wrong, but no section defines what the product *does* say.

This is the most frequent output a consumer blood-panel product will produce and the highest-consequence false-reassurance surface in the entire system. A contract that governs the rare Tier 0 case in detail and says nothing about the common all-clear case is inverted relative to actual risk exposure.

The specific hazards the contract must address:

- A panel that contains no abnormality is not a panel that excludes disease. The tests ordered bound what could have been found.
- §6.1 states Tier 0 is "normally empty." If the interface presents an empty Tier 0 as a positive safety signal, the product is making a claim it cannot support.
- A user with symptoms and a normal panel must not be discouraged from seeking review.

**Required revision.** Add a section defining the no-concern output: what is said, what limitation statement is mandatory, an explicit statement that normal results do not exclude conditions the panel does not test for, and a standing instruction that symptoms warrant clinical review irrespective of results. This section requires the same clinical sign-off as the Tier 0 language templates.

### B4 — Regulatory scope is not addressed

**Where:** absent. §19 covers clinical, product, and architecture authority but not regulatory status.

MHRA guidance is that standalone software with a medical purpose — software that analyses and interprets patient-specific data to make a diagnosis, or that produces an individual risk assessment — falls within the medical device definition and requires UKCA marking under UK MDR 2002 <cite index="61-1">apps and stand-alone software that gather data from a person and then analyse and interpret that data to make a diagnosis, prescribe a medicine, or recommend treatment are classified by MHRA as medical devices</cite>. MHRA also states plainly that <cite index="65-1">disclaimers such as "for informational purposes only" will not determine the outcome if the rest of the product's presentation suggests otherwise</cite>.

This contract defines a Tier 0 category whose stated output is action-and-timeframe instruction toward prompt clinical review, derived by rule from a person's laboratory data. Whether that constitutes a medical purpose is a determination for qualified regulatory advice, not for this reviewer and not for a clinical-policy document. But the question cannot remain unasked, because the answer changes the obligations attaching to everything else in the contract: clinical evaluation evidence, validation to intended purpose, post-market surveillance and incident reporting, and change control over the threshold assets.

**Required revision.** Add a section recording (a) that the regulatory status of this functionality in each intended launch market is an open question requiring specialist advice, (b) that ratification of this contract does not constitute a determination that the product falls outside device regulation, and (c) that the intended-purpose statement for the product must be reconciled with this contract before release. Flag that the non-diagnostic positioning asserted informally elsewhere in the platform documentation is a claim that must be defensible against the actual output this contract produces, not merely asserted in a disclaimer.

---

## 3. Required revisions — non-blocking but material

### R1 — Contextual role can be assigned to a finding that independently warrants concern

**Where:** §4.8, §6.4.

§4.8 makes contextual role determine lead eligibility, and §6.4 states Tier 3 findings may not lead or compete independently. Nothing prevents a serious finding from being classified contextual. §16 handles this for the specific case ("mild macrocytosis: Tier 3 contextual *unless* other blood-count abnormalities...") but there is no general rule.

Concrete hazard: MCV 125 fL alongside a raised ALT. Both are compatible with an alcohol-related pattern, so a rule author attaches MCV to the liver finding as explanatory context. An MCV of 125 fL is not context; it is a finding requiring investigation in its own right.

**Revision.** Add to §4.8: *a finding that independently meets Tier 0 or Tier 1 criteria may not be assigned contextual role. Contextual role is available only to findings that would otherwise sit in Tier 2 or below.*

### R2 — Trend is permissive where it must be mandatory

**Where:** §12 — "Trend **may** modify priority."

For some criteria, change is not a modifier of a single-timepoint finding; it *is* the finding. NICE NG148 detects AKI by a creatinine rise of ≥26 µmol/L within 48 hours or ≥50% within 7 days <cite index="28-1">a rise in serum creatinine of 26 micromol/litre or greater within 48 hours, or a 50% or greater rise known or presumed to have occurred within the past 7 days</cite>. Hyperkalaemia guidance similarly notes that acute change may carry more weight than the absolute level.

"May modify" reads as optional enhancement. It must be mandatory where a governed rule is change-defined.

**Revision.** Distinguish two classes: *change-defined findings*, where trend evaluation is mandatory and the §12 not-assessable statement is compulsory when no baseline exists; and *change-modified findings*, where trend adjusts an existing finding. Add a rule on baseline validity — how old a prior result may be to serve as baseline for each rule class. An eight-month-old creatinine is not a 48-hour baseline.

### R3 — §16 acceptance case asserts an answer the policy cannot yet derive

**Where:** §16.

The contract states the required output is Tier 1 for the hepatic finding. But tier assignment depends on thresholds deferred to §17, and on the mapping form which B2 shows is unspecified. The acceptance case is therefore a fixed expected output, not a test of the policy.

The risk is calibration-to-target: the hepatic pilot authors know the answer must be Tier 1 and will select bands that produce it. That inverts the evidence relationship.

**Revision.** Reclassify §16 as a *regression fixture* — an output the system must not regress from — and add an explicit requirement that the hepatic pilot derive its bands from cited sources independently, then be checked against §16. If the independently derived bands do not produce Tier 1, that is a finding requiring clinical adjudication, not a reason to adjust the bands.

Separately: §16 asserts Tier 1 without stating the clinical basis. ALT at ~5.1× ULN sits above the 3× ULN level that UK guidance treats as clinically meaningful and well below the >10× ULN level that triggers same-day specialist discussion in NHS referral pathways. Tier 1 is defensible; the document should say why.

### R4 — Overrides are invoked but not constrained

**Where:** §5 ("recognised combination and override rules"), absent from §15.

Overrides are the most powerful mechanism in the system — they move findings across tiers — and the contract places no discipline on them. §15 prohibits fifteen things; none of them is an ungoverned override.

**Revision.** Add: overrides must be individually enumerated, each attributable to a named clinical rule with a cited source, versioned, and auditable. Add to §15: *an override without a citable clinical basis is editorial preference and is prohibited.* Add explicitly that **no override may downgrade a finding below the tier floor set by urgency** — currently there is no directional constraint at all, so a downgrade override is permitted by omission.

### R5 — In-range values cannot generate findings

**Where:** §4.2 severity presumes abnormality; §3.1 does not state that reference-range status is not the entry criterion.

Clinically important cases the contract currently cannot express:

- Ferritin within range in the presence of active inflammation, masking iron deficiency.
- TSH within range with abnormal free T4 — the pattern, not either value, is the finding.
- A platelet count within range that has halved since a prior panel.
- A "normal" result that is abnormal for the person's demographic or physiological state.

**Revision.** State in §3.1 that reference-range exceedance is neither necessary nor sufficient for finding creation, and that governed rules may create findings from in-range values where a recognised pattern, combination, or trend criterion is met.

### R6 — Co-lead policy has no bound

**Where:** §7.4 — "Co-leads must remain exceptional and bounded."

"Bounded" without a number is not a bound. §19.3 sends co-lead policy to product ratification, which is right, but the contract should state the constraint form.

**Revision.** State that a maximum co-lead count must be set at ratification, that it applies to Tier 0 and Tier 1 only, and that where more findings qualify than the cap permits the system presents one lead and the remainder as visible Tier 1 concerns rather than expanding the lead set. Recommended cap: two. Three orienting concerns is not orientation.

### R7 — No volume control on Tier 1

**Where:** §14 — "other Tier 0 and Tier 1 concerns visible without interaction."

With a broad panel, Tier 1 could hold eight findings. Eight concerns visible without interaction dilutes the lead to invisibility and produces exactly the undifferentiated-list failure that §6's tiering exists to prevent. UK laboratory alerting practice has long recognised the corresponding hazard: alert lists should be kept small so that clinical needs are met <cite index="44-1">without raising the risk of information overload</cite>.

**Revision.** Define a compression rule: above a ratified count, Tier 1 concerns beyond the first N are summarised in a compact grouped form with full detail one interaction away. Compression must be by presentation density only and must never reorder or remove findings — which §15.10 already requires.

### R8 — "Tier 0 is normally empty" is an assumption presented as a property

**Where:** §6.1.

This sentence is a prediction about threshold calibration, not a fact about the tier. Two hazards. If thresholds are later set to satisfy the sentence, the system has been tuned to a design assumption rather than to clinical criteria. If Tier 0 turns out to fire in a materially non-trivial fraction of panels, the sentence becomes a false internal reassurance that suppresses scrutiny of the escalation pathway.

**Revision.** Replace with a measurable statement: *Tier 0 membership is determined solely by ratified urgency criteria. Expected Tier 0 firing rate is an empirical property to be measured and reviewed, not a design target.* Add a monitoring requirement: if the observed rate falls outside an expected band, that triggers clinical review of the thresholds in either direction — over-firing risks alarm fatigue and health-service burden; under-firing risks missed escalation.

### R9 — No escalation pathway is defined for Tier 0

**Where:** §6.1 requires "action-and-timeframe language"; §17.14 defers language templates. Neither addresses what happens operationally.

For a consumer product with no clinician in the loop, a Tier 0 finding raises questions the contract does not touch: what specifically is the user told to do; is there any follow-up or acknowledgement; what happens if the user does not act; is there any circumstance in which a third party is contacted; what is the position if the underlying result is later shown to be artefactual. Laboratory practice treats critical-result communication as a closed-loop process with defined recipients and recording; a consumer product has no equivalent loop by default.

**Revision.** Add a Tier 0 operational-pathway requirement to §17. This is a clinical, product, legal, and duty-of-care question jointly, and it should be scoped before the hepatic pilot rather than after, because it may constrain what Tier 0 can be permitted to contain.

### R10 — Analytical reliability is positioned before urgency in the processing order

**Where:** §5.

The sequence runs `analytical reliability checks → urgency rules`. §11 states correctly that urgency remains based on potential consequence regardless of artefact suspicion. But a step that runs *before* urgency and produces a reliability judgement will, in implementation, be treated as an input to urgency. The ordering and the policy pull in opposite directions.

**Revision.** Either move reliability assessment to run in parallel and attach as an annotation consumed only at the language and confirmation-advice stage, or state explicitly in §5 that the reliability step produces an annotation which the urgency step must not read. Given §11's clarity, this is a wording fix — but it is the kind of wording fix that determines what gets built.

### R11 — Orphan Tier 3 findings are undefined

**Where:** §6.4, §14.

Tier 3 findings "should be attached to the finding they help explain" and are "nested beneath the concern they explain." Nothing defines behaviour when a contextual finding has no parent — a mildly low transferrin on a panel with no hepatic, iron, or inflammatory concern to attach to.

**Revision.** Define the orphan case: either promote to Tier 2 with de-escalating language, or present in a distinct low-prominence group. Silent disappearance is not acceptable — §15.13's spirit requires that the user can reconcile what the product says with the raw values they can see.

---

## 4. Observations not requiring revision

- **§4.2 and §4.3 boundary.** Even after B1 is fixed, severity and clinical significance will overlap in practice, and both feed §7.2. Watch for double-counting during the hepatic pilot. Worth a worked example in the pilot spec showing a case where the two diverge.
- **§18 hepatic pilot choice is correct.** It contains the failure case, has an existing R-value computation, has strong UK guideline support, and exercises both the confidence-versus-priority separation and the contextual-attachment rules. No better first domain exists. One caution: hepatic is a domain where multiples-of-ULN *works*, so the pilot will not stress-test §4.2's central claim that no universal formula is authorised. Electrolytes should be the second domain, not a later one, because that is where universal scoring fails hardest and where the contract's most important prohibition gets its real test.
- **§19.4 Claude Code scope.** The boundary — architecture hardening, explicitly not clinical truth — is correctly drawn and should be preserved verbatim.
- **§19.1 clinical ownership.** The contract assigns ownership to the Head of Medical Research. It does not state that the holder must be a registered clinician with relevant scope of practice. For a document that assigns urgency tiers, that should be stated rather than assumed.

---

## 5. Defect summary

| ID | Defect | Class | Section |
|---|---|---|---|
| B1 | Clinical significance leaks confidence into prominence | Blocking | §4.3, §7.2 |
| B2 | Tier-assignment function undefined | Blocking | §5, §6 |
| B3 | No all-normal / no-concern policy | Blocking | absent |
| B4 | Regulatory scope not addressed | Blocking | absent |
| R1 | Contextual role assignable to serious findings | Required | §4.8, §6.4 |
| R2 | Trend permissive where it must be mandatory | Required | §12 |
| R3 | Acceptance case asserts an underivable answer | Required | §16 |
| R4 | Overrides unconstrained and undirected | Required | §5, §15 |
| R5 | In-range values cannot generate findings | Required | §3.1, §4.2 |
| R6 | Co-lead cap unspecified | Required | §7.4 |
| R7 | No Tier 1 volume control | Required | §14 |
| R8 | "Tier 0 normally empty" is an assumption stated as a property | Required | §6.1 |
| R9 | No Tier 0 operational escalation pathway | Required | §6.1, §17 |
| R10 | Reliability sequenced before urgency | Required | §5 |
| R11 | Orphan Tier 3 findings undefined | Required | §6.4, §14 |

---

## 6. Recommended disposition

1. Resolve B1–B4. B1 and B2 are wording and algebra changes and can be done immediately. B3 requires clinical drafting. B4 requires specialist regulatory advice and is the long pole — start it now, in parallel, because it may constrain the hepatic pilot's permitted outputs.
2. Resolve R1–R11 in a v0.2 revision.
3. Re-issue as v0.2 for a short confirmatory review rather than a full re-review — the architecture is not in question, only these defects.
4. Do not begin the hepatic pilot specification until B2 is resolved. The pilot cannot assign tiers under an undefined mapping, and a pilot built against an implicit mapping will harden that mapping by default.
5. Schedule electrolytes as the second pilot domain for the reason in §4.

---

## 7. Evidence sources used in this review

- NICE NG148. Acute kidney injury: prevention, detection and management — change-based AKI detection criteria (R2).
- British Society of Gastroenterology. Newsome PN et al., *Gut* 2018;67(1):6–19 — pattern-based abnormal liver blood test pathways (R3).
- NHS Devon (North & East) abnormal LFT referral guidance; NHS Specialist Pharmacy Service liver function interpretation — ULN-multiple escalation levels (R3).
- UK Kidney Association hyperkalaemia guideline — severity banding, acute-change significance, pseudohyperkalaemia exclusion (R2, R10).
- Tillman J, Barth JH; ACB National Audit Group. A survey of laboratory 'critical (alert) limits' in the UK. *Ann Clin Biochem* 2003;40:181–4 — alert-list size and information overload (R7).
- Royal College of Pathologists guidance on alert systems and communication of unexpected findings — closed-loop critical result communication (R9).
- MHRA. Medical device stand-alone software including apps (including IVDMDs); UK MDR 2002 — device qualification of interpretive software (B4).

---

## VERDICT: VALIDATE_WITH_REQUIRED_REVISIONS

The clinical model is correct and should be retained without redesign. Four blocking defects and eleven required revisions must be resolved before ratification and before the hepatic pilot specification is authored.

The judgement underlying this verdict: v0.1 fixes the failure it was written to fix, and does so at the right level of abstraction. Its remaining weaknesses are almost entirely omissions rather than errors — things the document does not say, which will be decided by default during implementation if they are not decided here. B1 is the exception and the one to prioritise: it is not an omission but an open path back to the original defect, and it is the kind of path that closes quietly and reopens under delivery pressure.
