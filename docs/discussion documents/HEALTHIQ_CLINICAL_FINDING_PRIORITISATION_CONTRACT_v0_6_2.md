---
document_id: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001
title: HealthIQ Clinical Finding Prioritisation Contract
version: "0.6.2"
status: CLINICALLY_RATIFIED_SUBJECT_TO_TARGETED_DOCUMENT_CORRECTION
owner: HealthIQ Head of Medical Research
product_authority: Anthony
scope: Clinical prioritisation, concern-set construction, lead selection, and presentation authority
implementation_status: NOT_AUTHORISED
regulatory_status: OPEN_SPECIALIST_REVIEW_REQUIRED
supersedes: "0.6.1"
---

# HealthIQ Clinical Finding Prioritisation Contract v0.6.2

> **v0.6.2 revision note — targeted closure amendment.** Issued to record two clinical adjudications that were the last open clinical items in the package, and one presentation-policy correction. No substantive new clinical policy is introduced beyond the two ratified closures themselves; v0.7 is therefore not warranted.
>
> 1. **B1 — hepatic Tier 1 floor: CLOSED, `CLINICALLY_ADJUDICATED`.** The BSG position is adopted literally. Any out-of-range core hepatic analyte produces **one consolidated Tier 1 hepatic finding** unless a more urgent governed hepatic rule applies. No magnitude-gated alternative is retained and the floor is no longer described as unresolved anywhere in this package.
> 2. **A8 — vitamin D: CLOSED, `CLINICALLY_ADJUDICATED`.** A narrow governed rule is authorised (see the cross-domain ruleset §9). Vitamin D is **removed from quarantine**.
> 3. **§15.2** now records the ratified hepatic presentation decision, scoped to the hepatic domain only.
>
> **No clinical adjudication from this package remains open.**
>
> **v0.6.1 revision note.** This is a **wording and status correction only**. No clinical policy has changed and no new clinical policy has been introduced; v0.7 is therefore not warranted.
>
> Three corrections were required to align v0.6 with product decisions ratified after it was issued:
> 1. §26.2 — `pregnant` and `may_be_pregnant` are treated identically for clinical interpretation.
> 2. §26.3 — the unknown-pregnancy-status clause is reframed as an **interim defensive** provision pending questionnaire enforcement, rather than a standing expectation.
> 3. §27.4 — sex is now available by design in the standard product flow; the missing-sex provision is retained as a **defensive fallback** for malformed or legacy requests only.
>
> Ancestry remains uncaptured and no ancestry-specific adjustment is authorised.
>
> **Amendment note (from v0.6).** v0.6 incorporates only the changes authorised by the HMR six-domain reconciliation: A7 (distinct missing-modifier consequences), A8 (governed derivation obligation), A9 (empty Tier 0 as a legitimate outcome), the interim pregnancy output policy, and the context-free unsafe-rule declaration requirement. The proposed universal cross-domain lead distinguishers are **not** included and remain unratified.
>
> Sections 1–25 retain their v0.5 numbering so that existing domain rulesets' cross-references stay valid. The two new policies are added as §26 and §27 rather than inserted mid-document.

## 1. Purpose

This contract defines the clinical policy HealthIQ must use to transform blood-panel data into a clinically prioritised concern set.

It replaces the concept of ranking raw markers or signal frames by a single universal score.

The contract governs:

- the unit that may be prioritised;
- the clinical dimensions that must remain separate;
- how urgency, severity and tiers are assigned;
- how supporting markers may affect interpretation;
- how multiple frames are consolidated;
- how findings enter the concern set;
- how one orienting lead is surfaced;
- how contextual findings are prevented from displacing direct concerns;
- how confidence affects explanation without controlling prominence;
- how phenotype and IDL outputs relate to direct findings;
- how no-concern outputs avoid false reassurance;
- how urgent findings require an operational escalation pathway;
- how indeterminate severity is represented when a required discriminator is unavailable;
- how urgency is expressed on a common cross-domain time-to-action scale;
- how long-term calculated risk may constitute severity;
- how uninterpretable-without-modifier findings are handled;
- how domain-conditional marker meaning and cross-domain consolidation are governed;
- what remains subject to domain-specific, regulatory and product ratification.

This document is a clinical-policy draft. It does not authorise implementation or release.

## 2. Governing principle

HealthIQ must prioritise the clinical problem that matters most, not the marker with the greatest amount of supporting information.

The system must distinguish:

1. clinical consequence;
2. urgency;
3. severity;
4. actionability;
5. interpretive confidence;
6. analytical reliability;
7. persistence and trend;
8. whether a finding is direct, combination-derived, explanatory, contextual, phenotype-level or system-level.

These dimensions must not be collapsed into one undifferentiated ranking score.

## 3. Unit of prioritisation

### 3.1 Canonical unit

The canonical unit of prioritisation is a:

> **consolidated clinical finding or pattern**

It is not:

- a raw biomarker;
- a signal row;
- an investigation frame;
- a WHY hypothesis;
- a phenotype label;
- an IDL record;
- a narrative section.

A consolidated clinical finding may arise from:

- one abnormal marker;
- one in-range marker that is clinically abnormal in context;
- several markers forming a recognised pattern;
- a clinically meaningful combination;
- a change over time;
- one marker with several alternative interpretations;
- a direct abnormality plus explanatory context.

Reference-range exceedance is neither necessary nor sufficient for finding creation. Governed rules may create findings from in-range values where a recognised combination, demographic rule or trend criterion is met.

### 3.2 Examples

- ALT and ALP may form a hepatocellular, cholestatic or mixed liver-pattern finding.
- Ferritin and transferrin saturation may form an iron-overload or inflammatory-ferritin finding.
- Macrocytosis with anaemia or another cytopenia is different from isolated mild macrocytosis.
- Creatinine may form an acute-change finding only when a valid prior result exists.
- A platelet count within range may still generate a trend finding if it has fallen materially from baseline.
- Multiple MCV interpretation frames normally consolidate into one macrocytosis concern.

## 4. Mandatory clinical dimensions

Every consolidated finding must carry the following dimensions as separate properties.

### 4.1 Urgency

The time sensitivity of required action.

Urgency answers:

> How soon might this need clinical attention?

Urgency must be assigned through explicit, clinically governed rules.

Urgency must also be mapped onto one common cross-domain time-to-action band:

- same day;
- within days;
- within weeks;
- routine.

The time band represents when action is required, not how biologically severe the finding is.

### 4.2 Severity

The degree of abnormality or dysfunction using the metric appropriate to the finding.

Severity may depend on:

- multiples of ULN;
- absolute concentration;
- absolute cell count;
- percentage or absolute change from baseline;
- recognised disease-stage bands;
- synthetic-function impairment;
- combination patterns;
- direction-specific rules;
- calculated long-term risk, where the evidence base expresses consequence as future event probability rather than present dysfunction.

Where severity is expressed as long-term risk, low immediate urgency must not be presented as low clinical importance.

No universal severity formula is authorised.

Severity methods are domain-specific and are not directly comparable across unlike domains.

### 4.3 Clinical significance

Clinical significance means:

> Given that this finding is present as characterised, how consequential is this class of finding?

Clinical significance is a property of the finding itself, not of HealthIQ’s certainty in explaining it.

Absence, unavailability or ambiguity of supporting data must not reduce clinical significance. Such factors act only on interpretive confidence.

### 4.4 Actionability

Whether a useful action follows, such as:

- prompt review;
- further investigation;
- repeat or confirmation;
- medication review;
- exposure modification;
- monitoring;
- reassurance.

### 4.5 Interpretive confidence

How certain HealthIQ is about the explanation of the finding.

Interpretive confidence may be affected by:

- missing markers;
- contradictory markers;
- unresolved alternative causes;
- incomplete context;
- absent history;
- weak pattern specificity.

Interpretive confidence must affect explanation specificity and uncertainty wording.

It must not determine clinical prominence, tier or lead selection.

### 4.6 Analytical reliability

Whether the measured result may be affected by:

- haemolysis;
- platelet clumping;
- delayed processing;
- assay limitation;
- inappropriate reference range;
- sample contamination;
- other recognised pre-analytical or analytical artefact.

Analytical reliability is an annotation. It must not be used to reduce urgency or suppress a finding.

### 4.7 Persistence and trend

Whether the finding is:

- new;
- persistent;
- improving;
- worsening;
- recurrent;
- stable;
- impossible to assess because no valid prior result exists.

### 4.8 Contextual role

Whether the finding is:

- direct;
- combination-derived;
- explanatory;
- contextual;
- phenotype-level;
- system-level.

A finding that independently meets Tier 0 or Tier 1 criteria may not be assigned contextual role.

Contextual role is available only to findings that would otherwise sit in Tier 2 or Tier 3.

### 4.9 Indeterminate severity

Indeterminate severity applies where:

- a finding is clinically real or sufficiently plausible to require action;
- two or more materially different severity states remain possible;
- a named discriminating marker, modifier or context item is unavailable;
- neither blanket worst-case inheritance nor automatic low-severity defaulting is clinically safe.

An indeterminate finding must remain visible, state the plausible severity states, name the missing discriminator, recommend the discriminating test or information where appropriate, and retain any urgency floor that can already be established.

Indeterminate severity is a property of the finding. It must not be treated merely as low interpretive confidence.

No universal arithmetic rule for converting indeterminate severity into a concern tier is authorised.

Each domain must define a governed indeterminate-severity rule. Until that rule exists, the finding must be assigned conservatively through clinical adjudication and must not be suppressed.

Indeterminate severity is distinct from insufficient data. Where a marker is a valid measurement but cannot discriminate between materially different clinical states, the finding is indeterminate. Where a marker is not a clinical quantity at all without its governed modifier, the result is an insufficient-data output under §8 and §16.2. The applicable consequence must be declared per marker–modifier pair.

## 5. Clinical processing order

HealthIQ must apply the following sequence:

```text
raw markers and valid prior results
→ signal/frame evaluation
→ clinical finding consolidation
→ modifier and interpretability validation
→ urgency classification and time-to-action band
→ domain-specific severity or indeterminate-severity classification
→ recognised within-domain and cross-domain combination rules
→ clinical-significance and actionability assessment
→ initial concern-tier assignment
→ governed override application
→ interpretive-confidence assessment
→ analytical-reliability annotation
→ lead selection
→ phenotype/IDL coordination
→ presentation
```

The sequence is mandatory because:

- consolidation must happen before ranking;
- interpretability must be established before urgency or severity is assigned;
- urgency must not depend on confidence or reliability;
- severity must not depend on supporting-marker count;
- reliability modifies framing and confirmation advice, not priority;
- presentation must not reorder clinical priority.

## 6. Concern-tier assignment

HealthIQ will use one orienting lead over a clinically tiered concern set.

### 6.1 Tier-assignment algebra

Each finding receives:

- an urgency-derived tier;
- a severity-derived tier, or a governed indeterminate-severity disposition where severity cannot yet be resolved.

Where both tiers are available, the initial tier is the more serious of the two — that is, the numerically lower tier.

Where severity is indeterminate, the domain-specific indeterminate rule applies. A missing discriminator must not be treated as permission to default to the least serious plausible tier.

Clinical significance and actionability may promote a finding by at most one tier where an explicit governed rule permits it.

Clinical significance and actionability may not lower a finding below the floor set by urgency or severity.

Interpretive confidence, supporting-marker count, frame count, panel completeness and analytical reliability may not alter the assigned tier.

### 6.2 Tier 0 — Prompt clinical review

Reserved for findings meeting explicit, clinically ratified urgency criteria.

Tier 0 membership is determined solely by ratified clinical rules. Its observed firing rate is an empirical safety metric, not a design target.

A domain may have no Tier 0 content. An empty Tier 0 register is a clinical property of the domain, not a specification gap, and must not be treated as an omission during review. Domains with an empty Tier 0 register are not constrained by §17.

A Tier 0 finding must:

- be foregrounded;
- control the lead or co-lead set;
- use action-and-timeframe language;
- avoid unsupported diagnostic claims;
- include confirmation advice where artefact is plausible;
- follow a defined operational escalation pathway.

### 6.3 Tier 1 — Discuss or investigate

Findings that warrant active clinical review or further investigation but do not meet Tier 0 criteria.

### 6.4 Tier 2 — Monitor or recheck

Findings that are real and potentially useful but usually lower consequence.

### 6.5 Tier 3 — Contextual

Findings whose main value is to explain, refine or contextualise another concern.

Tier 3 findings:

- may not lead;
- may not compete independently with Tier 0–2 findings;
- should attach to the finding they help explain;
- must remain reconcilable with the raw result.

If a Tier 3 finding has no valid parent, it must not disappear. It must either:

- be presented in a distinct low-prominence contextual group; or
- be promoted to Tier 2 where it independently warrants monitoring or recheck.

## 7. Lead-selection policy

### 7.1 Core rule

The lead is selected from the highest non-empty concern tier.

### 7.2 Within-tier ordering

Within the highest non-empty tier:

1. cross-domain findings are ordered first by the common urgency time-to-action band;
2. severity is used for ordering only within the same clinical domain;
3. clinical significance;
4. actionability;
5. persistence or worsening trend;
6. directness of evidence;
7. deterministic tie-breaker only when clinically equivalent.

Severity values from unlike domains must not be compared directly.

Where findings from different domains share the same urgency time band and no governed cross-domain rule distinguishes them, they must be presented as co-leads rather than ordered arbitrarily.

### 7.3 Excluded inputs

The following must not determine lead selection:

- interpretive confidence;
- supporting-marker count;
- number of frames;
- panel completeness;
- analytical-reliability status;
- lexical signal identifiers;
- static IDL display priority;
- narrative prominence;
- editorial preference.

### 7.4 Co-leads

Co-leads may be used only when:

- two or more distinct Tier 0 or Tier 1 findings are clinically comparable;
- they represent materially different action pathways;
- forcing one winner would be arbitrary or misleading.

Anthony must ratify a maximum co-lead count for findings below the same-day urgency band.

The recommended maximum is two.

If more non-same-day findings qualify than the cap permits, one lead or bounded co-lead set is shown and the remaining findings remain visible within their tier.

The co-lead cap does not apply to findings requiring same-day action.

Where two or more findings require same-day action and no governed cross-domain rule distinguishes them, they must be presented as one co-equal same-day group with no internal ordering. No arbitrary cross-domain severity comparison is permitted.

## 8. Supporting-marker policy

Supporting markers must not be counted as votes.

Their mere number must have no effect on priority.

Supporting markers may affect a finding only when they:

- establish a recognised pattern;
- trigger a clinically governed combination rule;
- identify organ dysfunction;
- materially increase or reduce the consequence of the characterised finding;
- reveal an artefact;
- resolve a clinically meaningful ambiguity;
- alter the recommended action.

Missing supporting markers may lower interpretive confidence.

They must not lower severity, clinical significance, tier or lead eligibility merely because they are absent.

### 8.1 Missing-modifier consequences

Where a governed domain rule identifies a required modifier, its absence produces one of two consequences. The applicable consequence must be declared for every marker–modifier pair in the domain's register.

**Insufficient data** — where the marker is not a clinical quantity without the modifier. The finding is not created; an insufficient-data output is produced for that question under §16.2. Uncorrected calcium without albumin is the reference case.

**Indeterminate severity** — where the marker is a valid measurement that cannot discriminate between materially different management pathways. The finding is created and governed by §4.9. TSH without free T4 is the reference case.

Neither consequence may be used to suppress a finding, to reduce clinical significance, or to lower a finding below an urgency floor that has already been established.

Where a combination criterion cannot be evaluated because a required constituent is absent, the criterion must be reported as not assessable, not as not met.

### 8.2 Governed derivation obligation

Where a required modifier is derivable from markers present on the panel, it must be derived rather than reported unavailable. Failure to derive an available value is not a legitimate route to indeterminate severity or insufficient data.

Derivation is permitted only under a governed derivation contract. No value may be derived merely because a mathematical formula exists. Each authorised derivation must specify:

- the formula;
- the units of every input and of the output;
- the assay assumptions and any method dependence;
- the conditions under which the derivation is invalid;
- provenance and clinical source;
- version.

Derived values must be labelled as derived wherever they are used or presented.

Derivations without a governed contract are prohibited.

## 9. Frame-consolidation policy

### 9.1 Default rule

One analyte contributes one concern slot by default.

Multiple frames over the same primary analyte must consolidate before concern-tier assignment and lead selection.

### 9.2 Consolidated content

A consolidated finding may contain:

- the leading interpretation;
- alternative interpretations;
- missing discriminating tests;
- contradictions;
- contextual markers;
- recommended next steps.

### 9.3 Separation exception

Frames may remain separate only when they imply materially different clinical action pathways.

The governing test is:

> Would a clinician reasonably take materially different next actions depending on which frame is correct?

### 9.4 Severity inheritance

A consolidated finding inherits the highest clinically justified urgency and severity among its present constituent frames. This rule does not authorise worst-case inheritance for a missing discriminator.

Frame count must not increase prominence.

### 9.5 Cross-domain consolidation

Governed combination rules may consolidate findings across domain boundaries where the constituents form one recognised clinical entity or one clinically unified action pathway.

Cross-domain consolidation must be explicitly enumerated, preserve the highest urgency time band and tier floor, remain auditable, and must not hide a constituent that independently meets Tier 0 or Tier 1 criteria unless the consolidated finding fully preserves that urgency and action requirement.

### 9.6 Domain-conditional marker meaning

Where one marker carries different clinical meaning in different domains, each domain must declare its own interpretation and role.

No interpretation assigned in one domain may be applied globally.

Albumin is the reference example:

- hepatic synthetic-function marker;
- calcium modifier;
- negative acute-phase reactant.

## 10. Confidence policy

Interpretive confidence answers:

> How certain are we about what this finding means?

Clinical priority answers:

> How much does this finding matter if present as characterised?

The two must remain independent.

Confidence may control:

- strength of wording;
- presentation of alternatives;
- missing-test recommendations;
- whether interpretation is provisional;
- level of explanatory specificity.

Confidence may not control:

- whether the finding is shown;
- whether it enters Tier 0 or Tier 1;
- whether it becomes the lead;
- whether it receives urgent action language.

## 11. Analytical-reliability policy

Where a result may be artefactual:

- the finding remains visible;
- urgency remains based on potential consequence;
- confirmation advice is explicit;
- the system must not assert that the abnormality is genuine;
- the system must not silently demote the finding.

Analytical reliability must be represented as a separate annotation consumed by wording, confirmation and action guidance.

It must not be an input to urgency, severity or tier assignment.

## 12. Trend policy

HealthIQ must distinguish:

### 12.1 Change-defined findings

For some clinical rules, change over time is the finding.

Where a governed rule is change-defined:

- trend evaluation is mandatory;
- baseline-validity requirements must be defined by the domain rule;
- the age and comparability of the prior result must be checked;
- if no valid baseline exists, HealthIQ must state that the change-defined criterion could not be assessed.

### 12.2 Change-modified findings

For other findings, trend modifies the interpretation of an already-present single-timepoint abnormality.

Trend may affect within-tier ordering or act through a governed override subject to §13.

Trend may not lower a finding below the floor set by urgency or severity.

Absent baseline data must never be treated as evidence of stability.

## 13. Override policy

Overrides may move findings across tiers only when individually governed.

Every override must be:

- explicitly enumerated;
- attributable to a named clinical rule;
- supported by a cited source or documented clinical adjudication;
- versioned;
- auditable;
- directionally constrained.

No override may downgrade a finding below the floor set by urgency or severity.

A governed override may promote a finding across more than one tier where the cited clinical rule requires it.

Governed override application is the only permitted route for multi-tier promotion.

An override without a citable clinical basis or documented clinical adjudication is editorial preference and is prohibited.

## 14. Phenotype and IDL policy

Phenotype and IDL records are interpretive layers over direct findings.

They must not operate as an independent cross-severity ranking system.

Rules:

- direct findings and phenotypes must map to the same concern-tier framework;
- static display priority may operate only as a tie-breaker within the same tier and comparable severity;
- phenotype severity must derive from constituent findings;
- a broad phenotype may not outrank a more severe direct abnormality;
- system summaries are contextual by construction;
- where a phenotype explains the lead, it should be presented as context around the lead rather than as a competing concern.

## 15. Presentation policy

The interface must preserve the clinical concern structure.

### 15.1 Default presentation

- Highest-tier lead or bounded co-leads.
- Other Tier 0 findings visible without interaction.
- Tier 1 findings visible, subject to a ratified presentation-density rule.
- Tier 2 findings visible but visually de-emphasised.
- Tier 3 findings nested beneath their parent or placed in a distinct contextual group.
- Missing-data and analytical limitations shown explicitly.

### 15.2 Tier 1 volume control

Anthony must ratify:

- the number of Tier 1 findings shown fully expanded;
- the compact grouping behaviour above that number;
- the maximum presentation density.

Compression may alter presentation density only.

It may not:

- reorder findings;
- remove findings;
- lower tiers;
- conceal that additional Tier 1 findings exist.

#### 15.2.1 Hepatic Tier 1 presentation — ratified

Hepatic Tier 1 abnormalities are presented as **one consolidated hepatic finding**, with supporting hepatic abnormalities **nested beneath it**.

Individual hepatic analytes do not occupy separate concern slots.

Constraints:

- nesting may not reorder findings, remove findings, lower any tier, or conceal that nested abnormalities exist;
- an abnormality that independently meets Tier 0 or Tier 1 criteria **in another domain** may not be absorbed into the hepatic finding (§4.8);
- the consolidated finding inherits the highest urgency band among its present constituents (§9.4);
- a minor abnormality must not be described as urgent merely because it enters Tier 1. Tier 1 means the abnormal result warrants discussion or investigation (§6.3).

**Scope limitation.** This clause establishes hepatic presentation only. It does **not** establish a universal Tier 1 density rule, and no other domain may adopt hepatic-style consolidation on the strength of it. Broader cross-domain Tier 1 presentation-density decisions remain open under §15.2.

### 15.3 Language

Language must:

- distinguish urgency from diagnosis;
- state action and timeframe where needed;
- communicate uncertainty;
- avoid false reassurance;
- avoid unnecessary alarm;
- explain why a finding is prominent;
- avoid implying completeness where the panel was incomplete.

## 16. No-concern, all-normal and insufficient-data output policy

HealthIQ must define two distinct governed output classes.

### 16.1 No-concern or low-concern output

This applies to panels containing:

- no Tier 0 or Tier 1 findings;
- only Tier 2 findings;
- only Tier 3 findings;
- no out-of-range values, where the available panel is sufficient for the assessment being described.

This output must not state or imply:

- that no disease is present;
- that the user is medically well;
- that symptoms are explained or excluded;
- that conditions not tested by the panel have been ruled out.

The output must state, in appropriate user-facing language:

1. what was and was not identified from the supplied results;
2. that normal or low-concern results do not exclude conditions the panel did not test for;
3. that missing markers or missing history may limit assessment;
4. that ongoing, severe or concerning symptoms warrant clinical review irrespective of the result summary;
5. what, if anything, is worth monitoring or discussing routinely.

### 16.2 Insufficient-data output

This applies where incomplete data prevents meaningful assessment of one or more clinically important questions, including where a present marker is uninterpretable without a named governed modifier.

The assessment limitation must lead the affected finding or domain output, not follow a reassuring summary of that affected area.

Where the panel also contains Tier 0 or Tier 1 findings, those findings remain governed by the normal lead-selection rules. The limitation must be stated alongside the affected finding or domain and must not displace a higher-priority lead.

The whole-output insufficient-data class applies only where no Tier 0 or Tier 1 finding is present.

It must state:

1. what could not be assessed;
2. which missing markers, history, timing or baseline data caused the limitation;
3. what conclusions must not be drawn;
4. what additional information would enable assessment;
5. that symptoms or clinical concern warrant review irrespective of the incomplete result set.

The insufficient-data output must not be presented as a no-concern or low-concern result.

Both output classes require the same clinical governance and versioning as Tier 0 language.

## 17. Tier 0 operational pathway

Tier 0 is not merely a wording class.

Before Tier 0 can be implemented, HealthIQ must define and ratify:

- the exact action the user is instructed to take;
- the required timeframe;
- confirmation advice for common artefact-prone results;
- whether acknowledgement is requested or recorded;
- whether any follow-up mechanism exists;
- whether any circumstance permits contact with another party;
- what is recorded for audit;
- what happens if later information shows the result was artefactual;
- legal, duty-of-care and support implications.

The Tier 0 pathway requires joint clinical, product, regulatory and legal review.

No Tier 0 production release is authorised without this pathway.

A domain with an empty Tier 0 register (§6.2) is not constrained by this section.

Where Tier 0 content exists but the pathway is not ratified, the affected findings must be withheld with an explicit, auditable statement. They must not be demoted to Tier 1 or to any lower tier.

## 18. Prohibited behaviours

The following are prohibited:

1. Ranking by supporting-marker count.
2. Using interpretive confidence as a prominence multiplier.
3. Allowing missing supporting data to reduce clinical significance.
4. Applying multiples of ULN universally across domains.
5. Allowing lexical ordering before clinical differentiators are exhausted.
6. Allowing static IDL priority to select the lead across severity levels.
7. Allowing multiple frames of one analyte to occupy multiple concern slots by default.
8. Suppressing a finding because confidence is low.
9. Treating absent baseline data as evidence of stability.
10. Treating panel completeness as clinical importance.
11. Letting presentation logic reorder clinically prioritised findings.
12. Treating tier thresholds as ordinary product configuration.
13. Using unsupported diagnostic language.
14. Presenting no foreground concern as proof that no clinically important issue exists.
15. Escalating common artefact-prone results without confirmation guidance.
16. Allowing contextual or system-level findings to outrank direct higher-severity abnormalities.
17. Assigning contextual status to a finding that independently meets Tier 0 or Tier 1.
18. Using an ungoverned or unsourced override.
19. Allowing an override to lower a finding below its urgency or severity floor.
20. Silently dropping an orphan Tier 3 finding.
21. Treating an in-range value as incapable of forming a clinical finding.
22. Presenting a change-defined condition as assessed when no valid baseline exists.
23. Applying a hepatic-style “any abnormality equals Tier 1” rule outside a domain-specific governed rule.
24. Comparing severity values directly across unlike domains.
25. Applying worst-case severity inheritance automatically when a discriminating marker is missing.
26. Treating a marker as interpretable when its required governed modifier is absent.
27. Applying one domain’s interpretation of a marker globally.
28. Using percentage white-cell differentials in place of absolute counts.
29. Applying a fixed ordering of biomarker classes or clinical domains.
30. Deriving a modifier value without a governed derivation contract, or presenting a derived value without labelling it as derived.
31. Reporting a modifier as unavailable when it is derivable from markers present on the panel.
32. Treating an indeterminate-severity finding as an insufficient-data output, or the reverse, where the domain register declares otherwise.
33. Applying non-pregnant reference rules to a person known to be pregnant.
34. Silently suppressing a finding on the grounds of pregnancy, or of any other out-of-scope population.
35. Applying a rule declared unsafe without clinical context when that context is unavailable.
36. Treating an empty Tier 0 register as a specification gap.

## 19. Initial hepatic regression fixture

The following case is a regression fixture.

It is not the source from which hepatic thresholds may be reverse-engineered.

### 19.1 Inputs

- ALT: 250 U/L
- ALT ULN: 49 U/L
- ALP: 46 U/L
- ALP ULN: 116 U/L
- R-value: approximately 12.9
- Bilirubin: normal
- GGT: normal
- AST: absent
- MCV: 99.5 fL
- MCV ULN: 96 fL
- Transferrin: mildly low

### 19.2 Required non-regression behaviour

- Consolidated lead finding: marked hepatocellular enzyme elevation.
- Expected concern tier: Tier 1 — discuss/investigate, subject to independent hepatic rule derivation and adjudication.
- Interpretive confidence: reduced for precise aetiological characterisation because AST is absent.
- Clinical significance and priority: not reduced merely because AST is absent.
- MCV: does not occupy multiple concern slots.
- Mild macrocytosis: contextual unless other blood-count abnormalities create a separate clinically meaningful pattern.
- Mildly low transferrin: contextual unless an independent iron, protein or liver pattern justifies separate concern status.
- IDL phenotype: may contextualise but may not displace the direct hepatic finding.
- No urgent diagnostic claim is authorised from these results alone.

### 19.3 Evidence discipline

The hepatic pilot must derive thresholds independently from cited evidence.

After derivation, the rules must be tested against this fixture.

If independently derived rules do not produce the expected Tier 1 result, the discrepancy requires clinical adjudication. Thresholds must not be adjusted merely to force the expected answer.

## 20. Domain-research requirements

This contract does not define numerical thresholds.

The following governed domain work is required before production implementation:

1. Hepatic severity, urgency, R-value and synthetic-function rules.
2. Electrolyte absolute thresholds and artefact rules.
3. Renal change-defined and single-timepoint rules.
4. Haematology and cytopenia severity rules.
5. Iron, ferritin, transferrin saturation and inflammatory-context rules.
6. Endocrine direction-specific rules.
7. Cardiometabolic and lipid risk-trigger rules.
8. Inflammatory-marker significance rules.
9. Nutritional-marker severity and actionability rules.
10. Cross-domain tier mapping.
11. Phenotype severity derivation.
12. Demographic and contextual modifiers.
13. Baseline-validity rules by domain.
14. Trend and persistence policy.
15. Tier 0 and no-concern language templates.
16. Clinical review and versioning cadence.
17. Tier 0 operational escalation pathway.
18. Governed indeterminate-severity rules by domain.
19. Marker–modifier registers with declared consequence class per pair (§8.1).
20. Governed derivation contracts for every authorised derived value (§8.2).
21. Unsafe-without-context registers by domain (§27).

Vitamin D is no longer listed as an unresolved domain-research item. A governed UK threshold has been adopted under the A8 adjudication and the marker is removed from quarantine.

## 21. Detailed domain-authoring sequence

The cross-domain breadth validation established that detailed authoring must proceed by dependency and model-testing value rather than by the first observed regression case.

### 21.1 First detailed domain — haematology

Haematology is first because it:

- is present on most routine panels;
- establishes severity bands required by hepatic, iron, inflammatory and nutritional domains;
- tests clinician first-look hierarchy;
- tests absolute-count severity;
- tests multi-lineage consolidation;
- tests contextual-versus-independent boundaries;
- supplies governed MCV, platelet, haemoglobin, white-cell and absolute-neutrophil rules;
- supplies a governed indeterminate-severity rule for the domain;
- distinguishes specification-only Tier 0 rules from release-authorised rules;
- supplies a marker–modifier register with a declared consequence class per pair;
- supplies an unsafe-without-context register.

Tier 0 haematology behaviour remains blocked until the operational pathway in §17 is ratified.

### 21.2 Second detailed domain — hepatic

The existing hepatic research is retained.

Before ratification it must:

- adopt v0.6.2;
- label the reference-range Tier 1 floor as hepatic-specific;
- remove temporary haematology thresholds;
- close or preserve explicit haematology dependencies;
- distinguish specification-only Tier 0 rules from release-authorised rules.

### 21.3 Third detailed package — renal and electrolytes

Renal and electrolyte rules should be authored as one coordinated package because renal function and electrolyte disturbance materially condition each other.

This package requires longitudinal baseline policy, artefact-confirmation rules and Tier 0 operational readiness.

### 21.4 Later domains

Recommended subsequent order:

1. iron;
2. inflammatory;
3. thyroid and endocrine;
4. cardiometabolic;
5. nutritional.

This is a clinical authoring order, not a sprint estimate or implementation commitment.

### 21.5 Breadth protection

No detailed domain ruleset may convert a domain-specific convention into a universal rule without cross-domain validation and explicit contract amendment.

## 22. Regulatory status and intended purpose

The regulatory status of this functionality is an open question requiring specialist advice in each intended launch market.

This contract assigns:

- patient-specific clinical concern tiers;
- urgency classes;
- action-and-timeframe guidance;
- prioritised interpretation of laboratory data.

Ratification of this clinical contract does not determine that HealthIQ falls outside medical-device or software-as-a-medical-device regulation.

Non-diagnostic or informational disclaimers do not by themselves settle regulatory status. The actual intended purpose, claims, outputs and user journey must be assessed together.

Before release, HealthIQ must:

1. obtain specialist regulatory advice;
2. document the intended-purpose statement;
3. reconcile that statement with the outputs authorised by this contract;
4. determine applicable clinical-evaluation, validation, quality, post-market and change-control obligations;
5. confirm whether Tier 0 functionality is permissible within the chosen product and regulatory model.

Regulatory review may constrain:

- tier naming;
- urgency wording;
- action recommendations;
- supported users;
- market scope;
- release sequence.

## 23. Governance and authority

### 23.1 Clinical authorship

The HealthIQ Head of Medical Research owns this policy and the clinical threshold assets derived from it.

Any individual providing clinical ratification must have appropriate qualifications, competence and scope for the decisions being ratified.

### 23.2 Independent medical validation

An independent medical reviewer must:

- challenge the clinical assumptions;
- verify evidence use;
- identify unsafe generalisation;
- test challenge cases;
- review false-reassurance and over-escalation risks.

### 23.3 Product ratification

Anthony must ratify:

- the lead-plus-tiered-concern-set product model;
- maximum co-lead count;
- tier visibility;
- Tier 1 volume-control behaviour;
- user-facing tier names;
- missing-data transparency;
- no-concern presentation;
- governance authority;
- threshold versioning and auditability.

### 23.4 Regulatory validation

A qualified regulatory adviser must assess intended purpose, market classification and release obligations.

### 23.5 Architecture hardening

Claude Code must validate:

- repository compatibility;
- contract impact;
- data-flow boundaries;
- consolidation location;
- versioning requirements;
- IDL and frontend dependencies;
- migration and regression risk.

Claude Code does not validate clinical truth or regulatory classification.

### 23.6 Implementation authority

No Cursor implementation prompt may be issued until:

1. independent medical validation is complete;
2. Head of Medical Research reconciliation is complete;
3. Anthony has ratified the product decisions;
4. the regulatory workstream has established any constraints material to design;
5. architecture hardening is complete;
6. the hepatic pilot has a clinically governed specification;
7. acceptance scenarios are approved;
8. the Tier 0 operational pathway is defined if Tier 0 is in implementation scope.

## 24. Monitoring and review

HealthIQ must monitor:

- Tier 0 firing rate;
- Tier 1 volume;
- no-concern output frequency;
- override firing;
- artefact-warning frequency;
- co-lead frequency;
- clinical-review escalations;
- false-positive and false-negative safety signals.

Observed firing rates are empirical safety indicators, not targets.

Unexpected over-firing or under-firing must trigger clinical review.

Thresholds, overrides, language and concern-set rules must be versioned and reviewable.


## 25. Status and next action

Current status:

`CLINICALLY_VALIDATED_FOR_DOMAIN_AUTHORING_WITH_CLOSURE_AMENDMENTS`

Confirmatory independent medical review established that:

- all six cross-domain amendments and both structural findings were correctly incorporated in v0.4;
- no further independent medical review is required after the v0.5 clause corrections;
- the core clinical model is validated;
- the remaining v0.4 defects were clause-level and are closed in v0.5.

Head of Medical Research confirmation (v0.5):

- interpretability now precedes urgency and severity classification;
- every domain must provide an indeterminate-severity rule;
- the ordinary co-lead cap does not apply to same-day findings;
- multiple indistinguishable same-day findings form one co-equal group without internal ordering;
- insufficient-data limitations apply to the affected finding or domain and cannot displace Tier 0 or Tier 1 leads;
- severity inheritance applies to present constituents and does not authorise worst-case inference from missing discriminators.

Next actions:

v0.6 additionally incorporates, on HMR authority from the six-domain reconciliation:

- A7 — distinct missing-modifier consequences (§4.9, §8.1);
- A8 — governed derivation obligation, with a mandatory derivation contract (§8.2);
- A9 — empty Tier 0 register as a legitimate domain outcome (§6.2, §17);
- interim pregnancy output policy (§26);
- context-free unsafe-rule declaration requirement (§27).

The proposed universal cross-domain lead distinguishers — organ dysfunction over marker abnormality, irreversible over reversible harm, direct over derived measurement — are **not** incorporated. They remain unratified. Equal time-band cross-domain findings continue to resolve as co-leads or, at same-day, as one co-equal group (§7.4).

v0.6.2 additionally records:

- **B1 closed** — the hepatic Tier 1 floor adopts the BSG position literally, presented as one consolidated nested hepatic finding (§15.2.1);
- **A8 closed** — a narrow governed vitamin D rule is authorised and the marker is removed from quarantine;
- **no clinical adjudication from this package remains open.**

v0.6.1 records, on product authority:

- `pregnant` and `may_be_pregnant` are clinically identical (§26.2);
- the unknown-pregnancy-status clause is an interim defensive provision, pending questionnaire enforcement that is **not yet implemented** (§26.3);
- sex is available by design; missing-sex handling is a defensive fallback only (§27.4);
- ancestry is not captured and no ancestry adjustment is authorised (§27.4).

Next actions:

1. Final independent cross-domain consistency review of contract v0.6.2, consolidated ruleset v0.4, adjudication register v0.3 and closure report v0.3.
2. Incorporate the supplemental electrolyte evidence and the closed HMR adjudications into the renal/electrolyte, haematology, hepatic and nutritional domain rulesets.
3. Continue specialist regulatory review in parallel.
4. Retain the hepatic ruleset as parked domain evidence pending haematology dependencies.
5. Do not author implementation work until the governance conditions in §23.6 are met.

---

## 26. Interim pregnancy policy

### 26.1 Status

No pregnancy-adjusted clinical interpretation is authorised in this version. Pregnancy materially alters the reference framework in the hepatic, haematological, renal/electrolyte, thyroid and cardiometabolic domains, and applying non-pregnant rules to a pregnant person produces both false alarm and false reassurance.

This is an interim policy. A pregnancy-specific ruleset is separate work and is not required in order to complete the non-pregnant adult ruleset.

### 26.2 Where pregnancy is known or possible

A declared status of `pregnant` and a declared status of `may_be_pregnant` are treated **identically** for all clinical interpretation purposes. Both require pregnancy-sensitive handling. No rule may distinguish between them.

Affected findings must produce an explicit out-of-scope, specialist-rules-required output.

That output must:

- state that the result has not been interpreted;
- state that pregnancy changes the applicable reference framework for the affected domain;
- name the affected domain or domains;
- direct the person to their maternity or clinical team;
- remain visible in the output.

Silent suppression is prohibited. A withheld interpretation must be visible as a withheld interpretation.

### 26.3 Where pregnancy status is unknown — interim defensive provision

Pregnancy status is a mandatory question in the target product flow, and a missing answer is intended to block upload and analysis. **That enforcement is not yet implemented.** This clause therefore governs the interim state and any malformed or legacy request.

Where status is unknown and the assumption materially affects the domain, the output must state that interpretation assumes non-pregnant adult reference rules.

This statement is required only for domains that have declared pregnancy as a material reference-framework dependency. It is not a universal disclaimer.

This clause is a defensive fallback, not a standing expectation. It must not be cited as authority for operating without pregnancy status once enforcement exists.

### 26.4 Domain obligation

Each domain must declare whether pregnancy materially affects its reference framework, and if so which findings are affected.

---

## 27. Context-free operation and unsafe-without-context rules

### 27.1 Principle

Most source guidance assumes a clinician holding history, symptoms, examination findings, medication list and prior results. HealthIQ frequently holds none of these.

Missing clinical context normally limits explanation specificity and interpretive confidence. It does not normally lower prominence, tier or lead eligibility (§4.5, §10).

### 27.2 The unsafe-without-context test

A rule is unsafe without clinical context — as distinct from merely lower-confidence — only where the missing item:

- changes whether the measured value is interpretable at all; or
- changes the applicable reference framework; or
- materially changes the action category the finding implies.

Where none of these applies, the rule runs and the missing context affects wording only.

### 27.3 Declaration requirement

Each domain must enumerate its unsafe-without-context rules in an explicit register, stating for each: the rule, the missing context item, which of the three tests it meets, and the required behaviour when the context is absent.

A rule not listed in the register is deemed safe to run without context and must not be silently withheld.

### 27.4 Reference examples

- pregnancy status, where it changes the reference framework (§26);
- treatment status for thyroid patterns;
- anticoagulation status for INR-dependent hepatic criteria;
- albumin for calcium interpretation;
- a valid prior creatinine for change-defined renal criteria.

**Biological sex.** Sex required for laboratory interpretation is a mandatory question in the standard product flow and is available by design. Domain rules may assume it is present. The missing-sex provisions in the domain registers are retained as a **defensive fail-closed fallback** for malformed or legacy requests only, and must not be treated as a normal operating mode.

**Ancestry.** Ancestry is not captured. No ancestry-specific reference adjustment is authorised in any domain under any circumstances. Where a source guideline specifies an ancestry-dependent threshold, the limitation must be stated and the unadjusted threshold applied.

### 27.5 Prohibition

Absence of context must not be used as a general route to withholding findings. Withholding is authorised only for rules declared under §27.3 or populations declared out of scope under §26.

---
