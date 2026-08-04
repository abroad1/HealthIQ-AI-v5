---
document_id: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001-REVIEW-V04
title: Confirmatory Independent Medical Review — Prioritisation Contract v0.4
reviews: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.4
compares_against: HEALTHIQ-CROSS-DOMAIN-PRIORITY-VALIDATION-REPORT-001 v0.1
review_type: CONFIRMATORY (not a fresh full review)
verdict: VALIDATE_WITH_REQUIRED_REVISIONS
---

# Confirmatory Review — Contract v0.4

## 0. Summary

All six amendments and both structural findings from the cross-domain validation report are incorporated. Two of them (A1, A6) are incorporated in a form that improves on what I proposed. The document is materially stronger than v0.3 and the clinical model is not in question.

Four new defects were introduced by the revisions. Two are material: an internal conflict between the co-lead rule and the co-lead cap (**N2**), and an unscoped insufficient-data output class that could displace a Tier 0 lead (**N4**). Both are sentence-level. Neither requires redesign.

The verdict is `VALIDATE_WITH_REQUIRED_REVISIONS`. **N1 must be closed before the haematology pilot specification is authored** — it is one clause. N2 and N4 must be closed before that pilot's acceptance scenarios are finalised, because haematology is the domain most likely to trigger both.

---

## 1. Amendment disposition

| ID | Amendment | Status | Where | Assessment |
|---|---|---|---|---|
| A1 | Indeterminate severity, arithmetic deferred | **RESOLVED — improved** | §4.9, §6.1, §18.25 | See §2 below |
| A2 | Cross-domain urgency time bands and lead handling | **RESOLVED** | §4.1, §7.2, §7.4, §18.24 | Four common bands defined; §7.2 orders on band first, restricts severity to within-domain, and mandates co-leads on ties; §4.2 states severity methods are not directly comparable across domains. Complete. |
| A3 | Calculated long-term risk as a severity method | **RESOLVED** | §4.2 | Added to the method list, with the clause that low immediate urgency must not be presented as low clinical importance. That second sentence was not in my proposal in that form and is a better formulation. |
| A4 | Uninterpretable-without-modifier; not-assessable handling | **RESOLVED** | §8 (two new clauses), §16.2, §5 | Both halves present: marker–modifier pairs route to insufficient-data rather than low confidence, and unevaluable combination criteria are reported as *not assessable* rather than *not met*. HEP-MISS-1 correctly promoted out of the hepatic asset. See N3 on placement. |
| A5 | Domain-conditional marker meaning | **RESOLVED** | §9.6, §18.27 | Albumin named as the reference case with its three roles enumerated. |
| A6 | Cross-domain consolidation | **RESOLVED — improved** | §9.5 | The added qualifier — a constituent meeting Tier 0/1 may be absorbed only where the consolidated finding *fully preserves that urgency and action requirement* — is more precise than my "may not be absorbed". It permits the clinically correct thrombocytopenia-plus-hepatic consolidation while keeping the safety property. Good judgement. |
| — | Prohibition on universalising the hepatic Tier 1 floor | **RESOLVED** | §18.23, §21.2, §21.5 | Prohibited as a behaviour, required to be relabelled hepatic-specific before hepatic ratification, and §21.5 generalises the principle to all future domains. Three-point closure; stronger than requested. |
| — | Haematology as first detailed domain | **RESOLVED** | §21.1, §21 preamble | The preamble states the sequence proceeds by dependency and model-testing value "rather than by the first observed regression case", which correctly records *why* hepatic was displaced. §21.1's rationale matches the report. |

**Result: 8 of 8 incorporated.**

---

## 2. On the A1 deferral

The contract declines my proposed lower-plausible-tier-plus-one rule and instead states (§4.9) that no universal arithmetic rule is authorised in v0.4, requiring each domain to define a governed indeterminate-severity rule, with conservative clinical adjudication until it exists.

**This is the right call and I withdraw the arithmetic proposal.** My rule was derived from a single domain (thyroid) and generalised without cross-domain testing — precisely the failure mode §21.5 now prohibits. Deferring it to governed domain rules is consistent with the contract's own refusal of universal severity formulae in §4.2, and inconsistent only with my own overreach.

The safety properties I was protecting are preserved without the arithmetic:
- §4.9 requires the finding to remain visible, state the plausible states, name the missing discriminator, and retain any established urgency floor.
- §6.1 states a missing discriminator is not permission to default to the least serious plausible tier — this closes the downgrade route.
- §18.25 prohibits automatic worst-case inheritance — this closes the escalation route.
- §4.9 states indeterminate severity is a property of the finding and must not be treated merely as low interpretive confidence — this closes the ambiguity with §4.5.

Both failure directions are blocked without a formula. That is a better outcome than my proposal.

---

## 3. New defects

### N1 — No domain is required to produce an indeterminate-severity rule

**Severity: required before the haematology pilot specification is authored.**

§4.9 obliges each domain to define a governed indeterminate-severity rule. Neither §20 (domain-research requirements, seventeen items) nor §21.1 (what haematology must supply) lists it. The obligation exists in §4.9 and appears nowhere in the two places a domain author will actually work from.

This matters immediately: haematology has clear indeterminate cases. A low haemoglobin with MCV unavailable is compatible with several severity dispositions; a low total white count without a differential cannot distinguish severe neutropenia from lymphopenia. A pilot spec written against §20 and §21.1 will not know it owes a rule.

**Required correction.** Add "indeterminate-severity rules by domain" to the §20 list, and add "supplies a governed indeterminate-severity rule for the domain" to §21.1's bullet list. Two lines.

### N2 — The co-lead rule and the co-lead cap conflict

**Severity: material. Required before haematology acceptance scenarios are finalised.**

§7.4 contains two rules that cannot both be satisfied:

- *"If more findings qualify than the cap permits, one lead or bounded co-lead set is shown and the remaining findings remain visible within their tier."*
- *"Where two findings from different domains both require same-day action and no governed cross-domain rule distinguishes them, both must be shown as co-leads. No arbitrary severity comparison is permitted."*

With three same-day findings across three domains and a ratified cap of two, the first rule requires selecting two — and the only available basis for selecting which two is the cross-domain severity comparison the second rule, §7.2 and §18.24 all prohibit. The contract mandates an action it also forbids.

This is not hypothetical for the first pilot domain. Haematology routinely produces multiple simultaneous same-day findings: severe thrombocytopenia with severe neutropenia, or a multi-lineage cytopenia alongside a separately qualifying count. Adding a hepatic or electrolyte Tier 0 to the same panel reaches three trivially.

**Required correction.** State that the co-lead cap does not apply to same-day findings, and that where more same-day findings qualify than the cap permits they are presented as a single co-equal same-day group with no internal ordering. This preserves both principles: the cap continues to govern the ordinary Tier 1 case where orientation matters, and the same-day case is never resolved arbitrarily. The alternative — relaxing the no-arbitrary-comparison rule — would reintroduce the defect the whole model exists to prevent.

Note this also resolves X1 from the validation report more cleanly than the interim position I proposed. Two Tier 0 findings in different domains become an undifferentiated same-day group by rule rather than by exception.

### N3 — Interpretability validation is sequenced after severity classification

**Severity: minor. Recommended.**

§5 runs `domain-specific severity or indeterminate-severity classification → modifier and interpretability validation`. Under §8, a marker uninterpretable without its named modifier produces an insufficient-data output, not a finding. Classifying the severity of an uncorrected calcium before establishing that uncorrected calcium is not a clinical quantity is backwards, and it leaves a severity value attached to a finding that should not exist.

**Recommended correction.** Move modifier and interpretability validation to run immediately after consolidation and before urgency and severity classification. Nothing downstream depends on the current order.

### N4 — The insufficient-data output class is unscoped and can displace a Tier 0 lead

**Severity: material.**

§16.2 states the insufficient-data output *"must lead with the assessment limitation, not with a reassuring findings summary"*, and applies *"where incomplete data prevents meaningful assessment of one or more clinically important questions"*.

The trigger is per-question; the presentation instruction reads as whole-output. A panel containing a Tier 0 potassium and an uninterpretable calcium satisfies §16.2's trigger. Read literally, the response then leads with the calcium limitation rather than the potassium — which contradicts §7.1 (lead from the highest non-empty tier) and §6.2 (a Tier 0 finding must be foregrounded and control the lead).

The word "reassuring" suggests the clause was written with the no-concern case in view, and that is the case where leading with the limitation is exactly right. But the scope is not stated, and a domain author or presentation designer will read it as written.

**Required correction.** Scope §16.2 to the affected finding or domain. Add: where a panel contains both Tier 0 or Tier 1 findings and areas of insufficient data, the findings are presented under normal lead-selection rules and the limitation is stated alongside them; the whole-output insufficient-data class applies only where no Tier 0 or Tier 1 finding is present. This preserves the clause's actual purpose — preventing "we couldn't assess" from reading as "we found nothing" — without letting it override tier structure.

---

## 4. Specific checks requested

| Check | Result |
|---|---|
| New route for missing data to suppress an important finding | **One found — N4.** Not suppression by omission; suppression by displacement. §8's routing of uninterpretable markers to insufficient-data is correctly non-suppressive, since §16.2 requires the limitation to be stated. |
| Arbitrary cross-domain severity comparison | **None introduced.** Blocked at §4.2, §7.2, §7.4 and §18.24 independently. But N2 creates a case where the contract *requires* an outcome only obtainable by such a comparison — the prohibition holds and the mandate is unsatisfiable, which is why N2 is a conflict rather than a leak. |
| Inappropriate automatic worst-case escalation | **None.** §18.25 and §4.9 both block it. One clarification worth making: §9.4 (a consolidated finding inherits the highest severity among constituent frames) and §18.25 are not in conflict — §9.4 governs frames that are all present, §18.25 governs missing discriminators — but a domain author could read them as competing. A parenthetical in §9.4 restricting it to present constituents would remove the doubt. Recommended, not required. |
| Conflict between co-lead rules and maximum co-lead count | **Yes — N2.** |
| Ambiguity between indeterminate severity and interpretive confidence | **None.** §4.9's closing sentence and §6.1's anti-default clause close it from both directions. This was the sharpest risk in the A1 rewrite and it has been handled. |
| New contradiction in processing order or tier algebra | **One minor — N3.** Note also that v0.4 moves governed override application to *after* initial tier assignment (§5), which resolves the §5/§13 sequencing inconsistency raised at v0.2. That fix is confirmed. Tier algebra in §6.1 is otherwise unchanged and remains sound. |

---

## 5. Defect summary

| ID | Defect | Class | Section |
|---|---|---|---|
| N1 | No domain required to produce an indeterminate-severity rule | Required before pilot authoring | §4.9, §20, §21.1 |
| N2 | Co-lead rule conflicts with co-lead cap for same-day findings | Required before pilot acceptance scenarios | §7.4 |
| N3 | Interpretability validation sequenced after severity classification | Recommended | §5 |
| N4 | Insufficient-data output unscoped; can displace a Tier 0 lead | Required | §16.2 |

Four corrections. N1 is two lines. N2, N3 and N4 are one clause each.

---

## VERDICT: VALIDATE_WITH_REQUIRED_REVISIONS

Required: **N1, N2, N4.** Recommended: **N3**, plus the §9.4 parenthetical.

The verdict is not `VALIDATE` because N2 is a live internal contradiction in a rule the first pilot domain will exercise routinely, and N4 permits a Tier 0 finding to be displaced from the lead by a presentation clause. Both are one-clause fixes and neither reflects a problem with the model.

### Readiness to govern the Haematology Clinical Prioritisation Pilot Specification

**Yes, conditional on N1.**

- **N1 must be closed first.** It is two lines, and without it the pilot spec will not know it owes an indeterminate-severity rule for a domain that plainly needs one.
- **N2 and N4 must be closed before the pilot's acceptance scenarios are finalised**, not before authoring begins. Haematology is the domain most likely to generate multiple simultaneous same-day findings (N2) and the domain where a missing differential or missing MCV creates partial-assessment output (N4). Acceptance scenarios written against the current text would encode both defects as expected behaviour.
- **N3 can be closed at any point** before implementation.
- Everything else the pilot needs is in place: §4.1 time bands, §4.9 indeterminate severity, §8's marker–modifier and not-assessable rules, §9.5 cross-domain consolidation, §18.28 (absolute counts, not percentage differentials), and §21.1's scope list.
- **§17 remains the binding constraint on release, not on authoring.** Tier 0 haematology content — severe cytopenias, multi-lineage cytopenia — may be specified but not released until the operational pathway is ratified. §21.1 states this correctly, and §21.2's requirement to distinguish specification-only from release-authorised Tier 0 rules should be applied to haematology as well, not only to hepatic. Worth adding to §21.1 alongside N1.

No further independent medical review of the contract is required. Confirmation by the Head of Medical Research that the four clauses read as intended closes this out.
